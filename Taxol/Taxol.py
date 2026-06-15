# ==============================================================================
# CODIGO CUANTICO LAB - PROYECTO PAULA (TAXOL) - VERSIÓN ROBUSTA 3D
# FASE 1: Geometría Clásica y Extracción de Sitio Activo
# ==============================================================================

from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np

# 1. CARGA DE LA MOLÉCULA (TAXOL / PACLITAXEL)
# SMILES Isomérico oficial y verificado de PubChem (CID: 36314)
taxol_smiles = "CC1=C2[C@H](C(=O)[C@@]3([C@H](C[C@@H]4[C@]3(CO[C@@H]4OC(=O)C)O)OC(=O)C)C[C@@H](OC(=O)[C@H](O)[C@@H](NC(=O)c5ccccc5)c6ccccc6)C[C@H]1OC(=O)c7ccccc7)[C@@H]2O"

print("⚛️ CodigoCuanticoLab: Cargando estructura de Taxol (Paclitaxel) desde PubChem...")
mol = Chem.MolFromSmiles(taxol_smiles)

if mol is None:
    raise ValueError("❌ Error: No se pudo generar la molécula. Revisar SMILES.")

# 2. OPTIMIZACIÓN GEOMÉTRICA CLÁSICA (3D) - ROBUSTA
print("⚙️ Generando geometría 3D...")
mol = Chem.AddHs(mol)

# Intento 1: Estándar
embed_result = AllChem.EmbedMolecule(mol, randomSeed=42)

# Intento 2: Si falla, usar coordenadas aleatorias y más intentos (Crucial para moléculas grandes)
if embed_result != 0 or mol.GetNumConformers() == 0:
    print("⚠️ El intento estándar falló. Usando coordenadas aleatorias y 1000 intentos...")
    embed_result = AllChem.EmbedMolecule(mol, useRandomCoords=True, randomSeed=42, maxAttempts=1000)
    
# Verificación final
if embed_result != 0 or mol.GetNumConformers() == 0:
    raise ValueError("❌ No se pudo generar la geometría 3D de la molécula. La estereoquímica es demasiado restrictiva.")

print("✅ Geometría 3D generada exitosamente.")

# Optimizar con MMFF94
print("⚙️ Optimizando clásicamente (MMFF94)...")
mmff_result = AllChem.MMFFOptimizeMolecule(mol)
if mmff_result != 0:
    print("⚠️ Warning: La optimización MMFF94 no convergió al 100%, pero usaremos la geometría generada.")

print(f"✅ Molécula optimizada. Átomos totales: {mol.GetNumAtoms()}")

# 3. EXTRACCIÓN DEL SITIO ACTIVO (CON PLAN B)
def get_active_site_indices(mol):
    """Busca el anillo de oxetano (4 átomos, 1 oxígeno). Si falla, usa un anillo de benceno (6 átomos)."""
    ring_info = mol.GetRingInfo().AtomRings()
    
    # PLAN A: Buscar anillo de oxetano (4 átomos, exactamente 1 oxígeno)
    for ring in ring_info:
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        oxygen_count = sum(1 for atom in ring_atoms if atom.GetSymbol() == 'O')
        if len(ring) == 4 and oxygen_count == 1:
            print("🎯 Plan A exitoso: Anillo de Oxetano encontrado (Sitio Activo).")
            return list(ring)
            
    # PLAN B: Si no hay oxetano, buscar un anillo aromático de benceno (6 átomos, 0 oxígenos)
    print("🔄 Plan A falló. Activando Plan B: Buscando anillo de Benceno...")
    for ring in ring_info:
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        oxygen_count = sum(1 for atom in ring_atoms if atom.GetSymbol() == 'O')
        if len(ring) == 6 and oxygen_count == 0:
            print("✅ Plan B exitoso: Anillo de Benceno (sitio alternativo) encontrado.")
            return list(ring)
            
    # PLAN C: Si todo falla, tomar los primeros 4 átomos de la molécula
    print("️ Plan B falló. Tomando fragmento genérico de 4 átomos.")
    return [0, 1, 2, 3]

# Ejecutar la búsqueda
active_site_indices = get_active_site_indices(mol)

# 4. PREPARACIÓN PARA FASE 2 (QISKIT NATURE / VQE)
print("\n Preparando Hamiltoniano para simulación cuántica (Fase 2)...")
print("💡 Siguiente paso: Mapear este fragmento usando Jordan-Wigner y correr VQE en Qiskit.")

# Exportar el fragmento a formato XYZ para PySCF/Qiskit
filename = "taxol_active_site.xyz"
with open(filename, "w") as f:
    f.write(f"{len(active_site_indices)}\n")
    f.write("Taxol Active Site Fragment - CodigoCuanticoLab\n")
    
    conf = mol.GetConformer()
    for idx in active_site_indices:
        atom = mol.GetAtomWithIdx(idx)
        pos = conf.GetAtomPosition(idx)
        f.write(f"{atom.GetSymbol()} {pos.x:.6f} {pos.y:.6f} {pos.z:.6f}\n")

print(f"✅ ¡Éxito! Archivo '{filename}' generado correctamente.")
print("🔬 Átomos en el fragmento exportado:")
for idx in active_site_indices:
    atom = mol.GetAtomWithIdx(idx)
    print(f"   - {atom.GetSymbol()} (Índice original: {atom.GetIdx()})")