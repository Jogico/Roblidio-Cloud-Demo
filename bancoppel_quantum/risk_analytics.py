# ============================================================
# RISK_ANALYTICS.PY - SISTEMA DE AUDITORÍA PROFUNDA
# BANCOPPEL QUANTUM RISK SENTINEL
# OPTIMIZADO PARA IBM REAL (JOB MASIVO ÚNICO)
# ============================================================

import numpy as np
import time
import os
import csv
import json
from datetime import datetime

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from qiskit_ibm_runtime import (
    QiskitRuntimeService,
    SamplerV2 as Sampler
)

# ============================================================
# CLASE PRINCIPAL
# ============================================================

class BanCoppelRiskManager:

    """
    Arquitectura híbrida cuántico-clásica
    para auditoría financiera masiva.
    """

    # ========================================================
    # INIT
    # ========================================================

    def __init__(self):

        # ====================================================
        # IBM CREDENTIALS
        # ====================================================

        self.IBM_API_KEY = "pRRjSlltOBU3vMRowReYX2nLbpA8x1Bwbcww7J1v2fSE"

        self.IBM_INSTANCE = (
            "crn:v1:bluemix:public:quantum-computing:"
            "us-east:a/f7958597d5c94b27bf5bcbf1891a5e42:"
            "03e7666f-4e2e-44cd-a90c-5996e8380fb8::"
        )

        self.ibm_input_id = "V-2026-BANCOPPEL-QC-AUDIT-PM"

        self.service = None

        # ====================================================
        # PESOS DINÁMICOS
        # ====================================================

        self.peso_reciente = 1.0
        self.peso_historico = 0.2

        # ====================================================
        # LEDGER CSV
        # ====================================================

        self.csv_log_file = "traceability_log.csv"

        self.init_traceability_ledger()

    # ========================================================
    # TRACEABILITY LEDGER
    # ========================================================

    def init_traceability_ledger(self):

        if not os.path.exists(self.csv_log_file):

            with open(
                self.csv_log_file,
                mode='w',
                newline=''
            ) as file:

                writer = csv.writer(file)

                writer.writerow([

                    "Timestamp",
                    "IBM_Input_ID",
                    "Vector_Input",
                    "Quantum_Collapse_Counts",
                    "Prob_Base",
                    "Prob_Final",
                    "Audit_Status"

                ])

    # ========================================================
    # LOG TRANSACTION
    # ========================================================

    def registrar_transaccion_log(
        self,
        vector,
        counts,
        p_base,
        p_final
    ):

        with open(
            self.csv_log_file,
            mode='a',
            newline=''
        ) as file:

            writer = csv.writer(file)

            writer.writerow([

                datetime.now().isoformat(),
                self.ibm_input_id,
                str(vector),
                str(counts),
                p_base,
                p_final,

                "RISK_ALERT"
                if p_final > 0.10
                else "STABLE"

            ])

    # ========================================================
    # IBM CONNECTION
    # ========================================================

    def conectar_ibm(self):

        try:

            self.service = QiskitRuntimeService(

                channel="ibm_quantum_platform",

                token=self.IBM_API_KEY,

                instance=self.IBM_INSTANCE
            )

            return True

        except Exception:

            return False

    # ========================================================
    # CONNECT BACKEND
    # ========================================================

    def conectar_a_backend(
        self,
        nombre_backend
    ):

        try:

            if self.service is None:

                if not self.conectar_ibm():

                    return None

            backend = self.service.backend(
                nombre_backend
            )

            return backend

        except Exception:

            return None

    # ========================================================
    # CREATE RISK CIRCUIT
    # ========================================================

    def crear_circuito_riesgo(
        self,
        vector
    ):

        qc = QuantumCircuit(3)

        # ====================================================
        # NORMALIZACIÓN
        # ====================================================

        v_norm = [v * 0.35 for v in vector]

        # ====================================================
        # ENCODE
        # ====================================================

        qc.ry(v_norm[0] * np.pi, 0)
        qc.ry(v_norm[1] * np.pi, 1)
        qc.ry(v_norm[2] * np.pi, 2)

        # ====================================================
        # ENTANGLEMENT
        # ====================================================

        qc.cx(0, 1)
        qc.cx(1, 2)

        # ====================================================
        # MEASURE
        # ====================================================

        qc.measure_all()

        return qc

    # ========================================================
    # SINGLE EXECUTION
    # ========================================================

    def run_stress_test(
        self,
        vector,
        use_quantum=True,
        backend=None
    ):

        job_id = "N/A"

        try:

            # =================================================
            # SIMULADOR
            # =================================================

            if not use_quantum or backend is None:

                return self.ejecutar_simulador(vector)

            # =================================================
            # CIRCUITO
            # =================================================

            qc = self.crear_circuito_riesgo(vector)

            circuito = transpile(

                qc,
                backend,
                optimization_level=3
            )

            # =================================================
            # SAMPLER
            # =================================================

            sampler = Sampler(mode=backend)

            # =================================================
            # JOB
            # =================================================

            job = sampler.run([circuito])

            job_id = job.job_id()

            # =================================================
            # RESULT
            # =================================================

            result = job.result()

            counts = result[0].data.meas.get_counts()

            return self.analisis_deep_audit(

                counts,
                backend.name,
                job_id,
                vector

            )

        except Exception:

            return self.ejecutar_simulador(vector)

    # ========================================================
    # MASIVE AUDIT - IBM REAL
    # UN SOLO JOB PARA TODA LA CARTERA
    # ========================================================

    def run_massive_audit(

        self,
        df_clientes,
        backend

    ):

        try:

            print("\n================================")
            print("AUDITORÍA MASIVA CUÁNTICA")
            print("================================\n")

            # ================================================
            # VALIDACIÓN
            # ================================================

            if backend is None:

                return None

            # ================================================
            # CIRCUITOS
            # ================================================

            circuitos = []

            vectores = []

            # ================================================
            # GENERAR CIRCUITOS
            # ================================================

            for _, row in df_clientes.iterrows():

                vector = [

                    float(row['Capacidad_Pago']),
                    float(row['Volatilidad_Sector']),
                    float(row['Historial_Lealtad'])

                ]

                vectores.append(vector)

                qc = self.crear_circuito_riesgo(
                    vector
                )

                circuito = transpile(

                    qc,
                    backend,
                    optimization_level=1

                )

                circuitos.append(circuito)

            print(
                f"✅ Circuitos generados: "
                f"{len(circuitos)}"
            )

            # ================================================
            # SAMPLER
            # ================================================

            sampler = Sampler(mode=backend)

            # ================================================
            # JOB ÚNICO IBM
            # ================================================

            job = sampler.run(circuitos)

            job_id = job.job_id()

            print(f"\n🆔 JOB MASIVO: {job_id}")

            print("\n⏳ IBM procesando cartera...\n")

            # ================================================
            # RESULTADOS
            # ================================================

            result = job.result()

            riesgos = []

            # ================================================
            # PROCESAMIENTO MASIVO
            # ================================================

            for idx, r in enumerate(result):

                counts = r.data.meas.get_counts()

                vector = vectores[idx]

                analisis = self.analisis_deep_audit(

                    counts,

                    backend.name,

                    job_id,

                    vector

                )

                riesgos.append(
                    analisis["Probabilidad"]
                )

            print("\n✅ AUDITORÍA FINALIZADA\n")

            return riesgos

        except Exception as e:

            print(
                f"\n❌ ERROR AUDITORÍA MASIVA:\n{e}"
            )

            return None

    # ========================================================
    # AER SIMULATOR
    # ========================================================

    def ejecutar_simulador(
        self,
        vector
    ):

        try:

            simulator = AerSimulator()

            qc = self.crear_circuito_riesgo(
                vector
            )

            circuito = transpile(
                qc,
                simulator
            )

            job = simulator.run(

                circuito,
                shots=1024

            )

            counts = job.result().get_counts()

            return self.analisis_deep_audit(

                counts,

                "AerSimulator",

                "SIM-2026-VAL",

                vector

            )

        except Exception:

            return None

    # ========================================================
    # CORE FINANCIAL ANALYSIS
    # ========================================================

    def analisis_deep_audit(

        self,
        counts,
        b_name,
        job_id,
        vector

    ):

        # ====================================================
        # TOTAL SHOTS
        # ====================================================

        total = sum(counts.values())

        # ====================================================
        # ESTADOS CRÍTICOS
        # ====================================================

        r_critico = counts.get("111", 0)

        r_alto = (

            counts.get("110", 0)
            + counts.get("101", 0)
            + counts.get("011", 0)

        )

        # ====================================================
        # PROBABILIDAD BASE
        # ====================================================

        prob_base = (

            (
                r_critico * self.peso_reciente
            )

            +

            (
                r_alto * 0.45
            )

        ) / total

        # ====================================================
        # SEVERIDAD PERFIL
        # ====================================================

        severidad_perfil = (
            sum(vector) / len(vector)
        )

        # ====================================================
        # ESCALAMIENTO FINANCIERO
        # ====================================================

        if severidad_perfil > 0.48:
    
            prob_final = (

        0.03
        + (prob_base * 0.18)

    )

        else:

            prob_final = 0.015

        # ====================================================
        # NORMALIZACIÓN
        # ====================================================

        prob_final = min(
            prob_final,
            0.95
        )

        # ====================================================
        # TRACEABILITY
        # ====================================================

        self.registrar_transaccion_log(

            vector,

            counts,

            prob_base,

            prob_final

        )

        # ====================================================
        # OUTPUT
        # ====================================================

        return {

            "Probabilidad":
                float(prob_final),

            "Motor":
                b_name,

            "Job_ID":
                job_id,

            "IBM_Input_ID":
                self.ibm_input_id,

            "Stress_Index":
                float(prob_final * 100)
        }
