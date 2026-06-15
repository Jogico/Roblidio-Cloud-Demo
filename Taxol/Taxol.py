# ==============================================================================
# CODIGO CUANTICO LAB - PROYECTO PAULA (TAXOL)
# FASE 1: Geometría Clásica y Extracción de Sitio Activo
# ==============================================================================

from rdkit import Chem
from rdkit.Chem import AllChem, Draw
from rdkit.Chem import rdFreeSASA
import numpy as np
import json

# 1. CARGA DE LA MOLÉCULA (TAXOL / PACLITAXEL)
# SMILES canónico del Paclitaxel
taxol_smiles = "CC1=C2C(C(=O)C3(C(CC4C(C3C(C(C2(C)C)(CC1OC(=O)C(C(C5=CC=CC=C5)NC(=O)C6=CC=CC=C6)O)O)OC(=O)C)O)C)OC(=O)C7=CC=CC=C7)(C(C=C(C)C4O)C)O"

print("⚛️ CodigoCuanticoLab: Cargando estructura de Taxol...")
mol = Chem.MolFromSmiles(taxol_smiles)

if mol is None:
    raise ValueError("Error: No se pudo generar la molécula desde el SMILES.")

# 2. OPTIMIZACIÓN GEOMÉTRICA CLÁSICA (3D)
# Añadimos hidrógenos y generamos conformación 3D
mol = Chem.AddHs(mol)
print(" Generando geometría 3D y optimizando clásicamente (MMFF94)...")

# Usamos MMFF94 para una optimización rápida y robusta de la geometría
AllChem.EmbedMolecule(mol, randomSeed=42)
AllChem.MMFFOptimizeMolecule(mol)

print(f"✅ Molécula optimizada. Átomos totales: {mol.GetNumAtoms()}")

# 3. EXTRACCIÓN DEL SITIO ACTIVO (ANILLO DE OXETANO)
# En el Taxol, el anillo de oxetano (D-ring) es crucial para su actividad anticancerígena.
# Los átomos clave del anillo de oxetano en la nomenclatura estándar son C4, C5, C20 y O4.
# En el índice de RDKit (basado en el orden del SMILES), los identificaremos por su entorno.

def get_oxetane_ring_indices(mol):
    """Identifica los índices de los átomos del anillo de oxetano (4 miembros con 1 oxígeno)."""
    for ring in mol.GetRingInfo().AtomRings():
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        # Buscamos un anillo de 4 átomos que contenga exactamente 1 oxígeno
        oxygen_count = sum(1 for atom in ring_atoms if atom.GetSymbol() == 'O')
        if len(ring) == 4 and oxygen_count == 1:
            return list(ring)
    return None

oxetane_indices = get_oxetane_ring_indices(mol)

if oxetane_indices:
    print(f" Sitio Activo (Anillo de Oxetano) encontrado en los índices: {oxetane_indices}")
    
    # Extraemos el fragmento para la simulación cuántica
    # (En un entorno real, aquí usaríamos PySCF/Qiskit Nature para mapear este fragmento)
    active_site_atoms = [mol.GetAtomWithIdx(i) for i in oxetane_indices]
    print("🔬 Átomos del sitio activo:")
    for atom in active_site_atoms:
        print(f"   - {atom.GetSymbol()} (Índice: {atom.GetIdx()}, Carga formal: {atom.GetFormalCharge()})")
else:
    print("⚠️ No se encontró el anillo de oxetano. Revisar estructura.")

# 4. PREPARACIÓN PARA FASE 2 (QISKIT NATURE / VQE)
print("\n Preparando Hamiltoniano para simulación cuántica (Fase 2)...")
print("💡 Siguiente paso: Mapear este fragmento usando Jordan-Wigner y correr VQE en Qiskit.")

# Guardamos la geometría del sitio activo en un formato estándar (XYZ) para PySCF/Qiskit
with open("taxol_active_site.xyz", "w") as f:
    f.write(f"{len(oxetane_indices)}\n")
    f.write("Taxol Oxetane Ring - CodigoCuanticoLab Active Site\n")
    conf = mol.GetConformer()
    for idx in oxetane_indices:
        atom = mol.GetAtomWithIdx(idx)
        pos = conf.GetAtomPosition(idx)
        f.write(f"{atom.GetSymbol()} {pos.x:.6f} {pos.y:.6f} {pos.z:.6f}\n")

print("✅ Archivo 'taxol_active_site.xyz' generado. Listo para Qiskit Nature.")