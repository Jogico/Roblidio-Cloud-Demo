# ==============================================================================
# CODIGO CUANTICO LAB - PROYECTO PAULA (TAXOL)
# FASE 2: Simulación Cuántica con PSI4 + Qiskit VQE
# ==============================================================================

import psi4
import numpy as np
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PSI4Driver
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.algorithms import GroundStateEigensolver
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit_algorithms.utils import algorithm_globals
from qiskit.primitives import Estimator
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD

print("⚛️ CodigoCuanticoLab: Fase 2 - Simulación Cuántica del Benceno (Taxol)")
print("=" * 80)

# ==============================================================================
# PASO 1: DEFINIR LA MOLÉCULA CON PSI4
# ==============================================================================
print("\n📋 Paso 1: Definiendo la molécula de Benceno (C6H6)...")

# Configuración del Benceno
driver = PSI4Driver.from_molecule(
    psi4.geometry("""
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
)

print("✅ Molécula definida: Benceno (C6H6)")

# ==============================================================================
# PASO 2: CONVERTIR A PROBLEMA CUÁNTICO
# ==============================================================================
print("\n🔬 Paso 2: Convirtiendo a problema de segunda cuantización...")

problem = driver.run()
print(f"✅ Problema creado:")
print(f"   Número de orbitales espaciales: {problem.num_spatial_orbitals}")
print(f"   Número de partículas: {problem.num_particles}")

# ==============================================================================
# PASO 3: MAPEO A QUBITS (Jordan-Wigner)
# ==============================================================================
print("\n💻 Paso 3: Mapeando a qubits con Jordan-Wigner...")

mapper = JordanWignerMapper()
second_q_ops = problem.second_q_ops()
hamiltonian = mapper.map(second_q_ops[0])

num_qubits = hamiltonian.num_qubits
print(f"✅ Hamiltoniano creado:")
print(f"   Número de qubits necesarios: {num_qubits}")

# ==============================================================================
# PASO 4: CONFIGURAR VQE
# ==============================================================================
print("\n⚙️ Paso 4: Configurando VQE...")

algorithm_globals.random_seed = 42

initial_state = HartreeFock(
    num_spatial_orbitals=problem.num_spatial_orbitals,
    num_particles=problem.num_particles,
    qubit_mapper=mapper,
)

ansatz = UCCSD(
    num_spatial_orbitals=problem.num_spatial_orbitals,
    num_particles=problem.num_particles,
    excitations="sd",
    qubit_mapper=mapper,
    initial_state=initial_state,
)

print(f"✅ Ansatz configurado: UCCSD")
print(f"   Número de parámetros variacionales: {ansatz.num_parameters}")

optimizer = SLSQP(maxiter=50)
estimator = Estimator()

vqe = VQE(
    estimator=estimator,
    ansatz=ansatz,
    optimizer=optimizer,
    initial_point=np.zeros(ansatz.num_parameters),
)

print(f"✅ VQE configurado")

# ==============================================================================
# PASO 5: CORRER VQE
# ==============================================================================
print("\n🚀 Paso 5: Corriendo VQE (simulación cuántica)...")
print("   Esto puede tardar 1-5 minutos...")

ground_state_solver = GroundStateEigensolver(mapper, vqe)
ground_state_result = ground_state_solver.solve(problem)

print(f"\n✅ ¡VQE completado!")
energy_hartree = ground_state_result.total_energies[0]
print(f"   Energía del estado fundamental: {energy_hartree:.6f} Hartree")
print(f"   Energía en eV: {energy_hartree * 27.2114:.4f} eV")

# ==============================================================================
# GUARDAR RESULTADOS
# ==============================================================================
import json

results = {
    "molecule": "Benceno (fragmento del Taxol)",
    "energy_hartree": float(energy_hartree),
    "energy_eV": float(energy_hartree * 27.2114),
    "num_qubits": num_qubits,
    "num_parameters": ansatz.num_parameters,
}

with open("taxol_vqe_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\n✅ Resultados guardados en 'taxol_vqe_results.json'")

print("\n" + "=" * 80)
print("🎉 ¡SIMULACIÓN CUÁNTICA COMPLETADA!")
print("=" * 80)
print(f"\n📊 RESUMEN:")
print(f"   Molécula: Benceno (C6H6)")
print(f"   Método: VQE + UCCSD")
print(f"   Motor clásico: PSI4")
print(f"   Qubits simulados: {num_qubits}")
print(f"   Energía fundamental: {energy_hartree:.6f} Hartree")
print(f"   Energía en eV: {energy_hartree * 27.2114:.4f} eV")
print("=" * 80)