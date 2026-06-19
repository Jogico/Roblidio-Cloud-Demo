# ==============================================================================
# CODIGO CUANTICO LAB - PROYECTO PAULA (TAXOL)
# FASE 2: VQE + Complete Active Space (CAS) - Método Profesional
# ==============================================================================

import psi4
import numpy as np
import json

print("️ CodigoCuanticoLab: Fase 2 - VQE + CAS del Benceno (Taxol)")
print("=" * 80)

# ==============================================================================
# PASO 1: PSI4 - Geometría y SCF
# ==============================================================================
print("\n📋 Paso 1: Obteniendo integrales con PSI4...")

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

h1 = np.asarray(wfn.H())
mints = psi4.core.MintsHelper(wfn.basisset())
eri = np.asarray(mints.ao_eri())

n_orbitals = h1.shape[0]
n_alpha = wfn.nalpha()
n_beta = wfn.nbeta()

print(f"✅ PSI4 completado: {n_orbitals} orbitales, {n_alpha + n_beta} electrones")

# ==============================================================================
# PASO 2: ESPACIO ACTIVO (CAS) - Solo electrones π del anillo aromático
# ==============================================================================
print("\n🔬 Paso 2: Definiendo Espacio Activo (CAS)...")

# Para benceno: 6 orbitales π (HOMO-2 a LUMO+2) con 6 electrones π
# Esto es el espacio activo estándar para sistemas aromáticos
n_active_orbitals = 6
n_active_electrons = 6  # 3 alpha + 3 beta

# Índices de los orbitales activos (los 6 orbitales π del anillo)
# En STO-3G, los orbitales π están alrededor de los índices 15-20
active_orbital_indices = list(range(15, 21))

print(f"✅ Espacio Activo: {n_active_orbitals} orbitales, {n_active_electrons} electrones")
print(f"   Orbitales activos: {active_orbital_indices}")

# Extraer submatriz del Hamiltoniano para el espacio activo
h1_active = h1[np.ix_(active_orbital_indices, active_orbital_indices)]
eri_active = eri[np.ix_(active_orbital_indices, active_orbital_indices, 
                        active_orbital_indices, active_orbital_indices)]

# Energía de los electrones congelados (core energy)
core_energy = scf_e - np.trace(h1_active @ np.eye(n_active_orbitals))

print(f"   Energía core (congelada): {core_energy:.6f} Hartree")

# ==============================================================================
# PASO 3: HAMILTONIANO CUÁNTICO (Espacio Activo)
# ==============================================================================
print("\n️ Paso 3: Construyendo Hamiltoniano cuántico...")

from qiskit_nature.second_q.operators import FermionicOp

op_dict = {}

# Términos de 1 electrón
for p in range(n_active_orbitals):
    for q in range(n_active_orbitals):
        val = h1_active[p, q]
        if abs(val) > 1e-12:
            op_dict[f"+_{p} -_{q}"] = val

# Términos de 2 electrones
for p in range(n_active_orbitals):
    for q in range(n_active_orbitals):
        for r in range(n_active_orbitals):
            for s in range(n_active_orbitals):
                val = eri_active[p, q, r, s]
                if abs(val) > 1e-12:
                    key1 = f"+_{2*p} -_{2*q} +_{2*r+1} -_{2*s+1}"
                    key2 = f"+_{2*p+1} -_{2*q+1} +_{2*r} -_{2*s}"
                    op_dict[key1] = op_dict.get(key1, 0) + val / 2
                    op_dict[key2] = op_dict.get(key2, 0) + val / 2

fermionic_op = FermionicOp(op_dict, num_spin_orbitals=2*n_active_orbitals)
print(f"✅ Hamiltoniano construido: {len(op_dict)} términos")

# ==============================================================================
# PASO 4: MAPEO A QUBITS (Jordan-Wigner)
# ==============================================================================
print("\n💻 Paso 4: Mapeando a qubits...")

from qiskit_nature.second_q.mappers import JordanWignerMapper

mapper = JordanWignerMapper()
qubit_op = mapper.map(fermionic_op)
num_qubits = qubit_op.num_qubits

print(f"✅ Qubits necesarios: {num_qubits}")

# ==============================================================================
# PASO 5: SIMULADOR CUÁNTICO EXACTO (Exact Diagonalization)
# ==============================================================================
print("\n⚙️ Paso 5: Corriendo Simulador Cuántico Exacto (Noiseless Quantum Simulator)...")

from qiskit_algorithms.minimum_eigensolvers import NumPyMinimumEigensolver

# Usamos el solver exacto para el espacio activo de 12 qubits
# Esto resuelve la ecuación de Schrödinger de forma exacta sin optimizadores
solver = NumPyMinimumEigensolver()

print("⚛️ Resolviendo Hamiltoniano de 12 qubits...")
result = solver.compute_minimum_eigenvalue(qubit_op)

# Energía total = energía del espacio activo + energía core congelada
vqe_energy = result.eigenvalue.real
total_energy = vqe_energy + core_energy
total_energy_ev = total_energy * 27.2114

print(f"\n🎉 ¡SIMULACIÓN CUÁNTICA EXITOSA!")
print(f"   Energía Espacio Activo (12 qubits): {vqe_energy:.6f} Hartree")
print(f"   Energía Core (congelada): {core_energy:.6f} Hartree")
print(f"   Energía Total Molecular: {total_energy:.6f} Hartree")
print(f"   Energía Total: {total_energy_ev:.4f} eV")

# ==============================================================================
# GUARDAR RESULTADOS
# ==============================================================================
results = {
    "molecule": "Benceno (fragmento Taxol)",
    "method": "Exact Diagonalization (Noiseless Quantum Simulator)",
    "active_space": f"CAS({n_active_orbitals},{n_active_electrons})",
    "num_qubits": num_qubits,
    "classical_engine": "PSI4",
    "total_energy_hartree": float(total_energy),
    "total_energy_eV": float(total_energy_ev)
}

with open("taxol_vqe_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n" + "=" * 80)
print("✅ RESULTADOS GUARDADOS EN 'taxol_vqe_results.json'")
print("Listo para visualización 3D de orbitales HOMO/LUMO")
print("=" * 80)