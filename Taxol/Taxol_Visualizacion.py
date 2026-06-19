# ==============================================================================
# CODIGO CUANTICO LAB - PROYECTO PAULA (TAXOL)
# VISUALIZACIÓN 3D DE ORBITALES MOLECULARES (Datos Exactos de PSI4)
# ==============================================================================

import psi4
import numpy as np
import json

print("⚛️ CodigoCuanticoLab: Visualización 3D de Orbitales del Benceno")
print("=" * 80)

# ==============================================================================
# PASO 1: RECALCULAR CON PSI4 (Para obtener coeficientes de orbitales)
# ==============================================================================
print("\n📋 Paso 1: Calculando orbitales moleculares con PSI4...")

mol_benceno = psi4.geometry("""
    C  0.000000  1.397000  0.000000
    C  1.209165  0.698500  0.000000
    C  1.209165 -0.698500  0.000000
    C  0.000000 -1.397000  0.000000
    C -1.209165 -0.698500  0.000000
    C -1.209165  0.698500  0.000000
    H  0.000000  2.484000  0.000000
    H  2.151000  1.242000  0.000000
    H  2.151000 -1.242000  0.000000
    H  0.000000 -2.484000  0.000000
    H -2.151000 -1.242000  0.000000
    H -2.151000  1.242000  0.000000
    symmetry c1
    0 1
""")

psi4.set_options({'basis': 'sto-3g', 'reference': 'rhf'})
scf_e, wfn = psi4.energy('scf', return_wfn=True)

print(f"✅ Energía SCF exacta: {scf_e:.6f} Hartree")

# ==============================================================================
# PASO 2: EXTRAER COEFICIENTES DE ORBITALES (HOMO y LUMO)
# ==============================================================================
print("\n🔬 Paso 2: Extrayendo coeficientes de orbitales moleculares...")

# Obtener matriz de coeficientes MO
C = np.asarray(wfn.Ca())
n_orbitals = C.shape[1]
n_alpha = wfn.nalpha()

# HOMO: Orbital ocupado más alto (índice n_alpha - 1)
# LUMO: Orbital virtual más bajo (índice n_alpha)
homo_idx = n_alpha - 1
lumo_idx = n_alpha

homo_coeff = C[:, homo_idx]
lumo_coeff = C[:, lumo_idx]

homo_energy = wfn.epsilon_a().to_array()[homo_idx]
lumo_energy = wfn.epsilon_a().to_array()[lumo_idx]

print(f"✅ HOMO (Orbital {homo_idx}): {homo_energy:.6f} Hartree")
print(f"✅ LUMO (Orbital {lumo_idx}): {lumo_energy:.6f} Hartree")
print(f"✅ Gap HOMO-LUMO: {(lumo_energy - homo_energy) * 27.2114:.4f} eV")

# ==============================================================================
# PASO 3: GUARDAR DATOS PARA VISUALIZACIÓN 3D
# ==============================================================================
print("\n💾 Paso 3: Guardando datos para visualización 3D...")

# Coordenadas atómicas
coords = []
for i in range(mol_benceno.natom()):
    coords.append({
        'atom': mol_benceno.label(i),
        'x': mol_benceno.x(i),
        'y': mol_benceno.y(i),
        'z': mol_benceno.z(i)
    })

# Datos completos
visualization_data = {
    "molecule": "Benceno (C6H6) - Fragmento del Taxol",
    "method": "RHF/STO-3G (Exacto)",
    "energy_hartree": float(scf_e),
    "energy_eV": float(scf_e * 27.2114),
    "homo": {
        "orbital_index": homo_idx,
        "energy_hartree": float(homo_energy),
        "energy_eV": float(homo_energy * 27.2114),
        "coefficients": homo_coeff.tolist()
    },
    "lumo": {
        "orbital_index": lumo_idx,
        "energy_hartree": float(lumo_energy),
        "energy_eV": float(lumo_energy * 27.2114),
        "coefficients": lumo_coeff.tolist()
    },
    "atoms": coords,
    "basis_set": "STO-3G",
    "num_orbitals": n_orbitals
}

with open("taxol_orbitals_data.json", "w") as f:
    json.dump(visualization_data, f, indent=2)

print("\n" + "=" * 80)
print("✅ DATOS DE VISUALIZACIÓN GUARDADOS")
print("=" * 80)
print(f"Archivo: 'taxol_orbitals_data.json'")
print(f"Energía exacta: {scf_e:.6f} Hartree")
print(f"Gap HOMO-LUMO: {(lumo_energy - homo_energy) * 27.2114:.4f} eV")
print("\nPróximo paso: Crear visualización 3D interactiva con Plotly")
print("=" * 80)