import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from risk_analytics import BanCoppelRiskManager

# --- CONFIGURACIÓN DE PANTALLA ---
st.set_page_config(page_title="BanCoppel Quantum Sentinel", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #33ff33; }
    .stButton>button { background-color: #33ff33; color: black; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Quantum-Risk-Sentinel | BanCoppel")

# --- BARRA LATERAL (CONEXIÓN) ---
st.sidebar.header("⚙️ Conectividad")
opciones_motor = ["Qiskit Aer (Simulador)", "ibm_marrakesh", "ibm_fez", "ibm_kingston", "Clásico"]
engine_selected = st.sidebar.selectbox("Seleccionar Motor", opciones_motor)

if 'risk_manager' not in st.session_state:
    st.session_state.risk_manager = BanCoppelRiskManager()

# Lógica de conexión
backend_activo = None
if "ibm_" in engine_selected:
    with st.sidebar:
        with st.spinner("Conectando..."):
            backend_activo = st.session_state.risk_manager.conectar_a_backend(engine_selected)
            if backend_activo:
                st.success(f"ONLINE: {engine_selected}")
                st.session_state.active_backend = backend_activo

tab1, tab2, tab3, tab4 = st.tabs(["🎯 Individual", "📊 Masivo", "📋 Ejecutivo", "📈 Reportes IBM Real"])

with tab1:
    st.subheader("Simulador de Cliente Único")
    col1, col2, col3 = st.columns(3)
    with col1: cap = st.slider("Capacidad", 0.0, 1.0, 0.7)
    with col2: vol = st.slider("Volatilidad", 0.0, 1.0, 0.3)
    with col3: hist = st.slider("Historial", 0.0, 1.0, 0.9)

    if st.button('🚀 Ejecutar Auditoría Individual'):
        vector = [cap * np.pi, vol * np.pi, hist * np.pi]
        es_cuantico = "ibm_" in engine_selected
        
        try:
            res = st.session_state.risk_manager.run_stress_test(
                vector, use_quantum=es_cuantico, backend=st.session_state.get('active_backend')
            )
            
            st.metric("Riesgo", f"{res['Probabilidad']:.2%}")
            if es_cuantico: st.warning(f"ID: {res['Job_ID']}")
            
            # Calcular Pérdida Esperada para la gráfica (Monto ficticio de 10000)
            perdida_esperada = res['Probabilidad'] * 10000
            
            # La gráfica vive AQUÍ ADENTRO para que no marque error
            fig = px.line(y=np.random.normal(perdida_esperada, 500, 100), title="Stress Test")
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Error: {e}")
            
# ============================================================
# PESTAÑA 2: AUDITORÍA MASIVA (100% CARTERA) - CONEXIÓN REAL RESTAURADA
# ============================================================
with tab2:
    st.subheader("📊 Auditoría de Cartera Cuántica")
    archivo = st.file_uploader("Cargar Cartera BanCoppel (.csv)", type="csv")
    
    if archivo is not None:
        df_base = pd.read_csv(archivo)
        
        if st.button("🚀 Iniciar Auditoría de Cartera"):
            # Limpieza inmediata de estados previos para asegurar la trazabilidad limpia
            if 'df_auditoria' in st.session_state:
                del st.session_state['df_auditoria']
                
            # DECLARACIÓN DE GOBERNANZA IDÉNTICA A LA PESTAÑA 1
            # Evaluamos la cadena del motor de la barra lateral para abrir el canal de IBM Real
            es_cuantico = "ibm_" in engine_selected
            backend_activo = st.session_state.get('active_backend')
            
            with st.spinner("Estableciendo enlace con Aer y ejecutando matriz..."):
                try:
                    riesgos = []
                    df_audit = df_base.copy()
                    
                    # Procesamiento iterativo sobre tu risk_manager original para blindar los cálculos
                    for i, row in df_audit.iterrows():
                        # REGLA DE ORO: Multiplicación explícita por PI para el posicionamiento en el Espacio de Hilbert
                        vector = [
                            float(row['Capacidad_Pago']) * np.pi, 
                            float(row['Volatilidad_Sector']) * np.pi, 
                            float(row['Historial_Lealtad']) * np.pi
                        ]
                        
                        # Invocación directa al motor sin alterar las ecuaciones ni los buffers de reserva
                        res = st.session_state.risk_manager.run_stress_test(
                            vector, use_quantum=es_cuantico, backend=backend_activo
                        )
                        riesgos.append(res['Probabilidad'])
                    
                    # Inyección de resultados al ledger de control de la sesión
                    df_audit['Riesgo'] = riesgos
                    st.session_state['df_auditoria'] = df_audit
                    
                    st.success(f"✅ Auditoría completada con éxito. Enlace cuántico real: {es_cuantico}")
                    st.dataframe(df_audit[['ID_Cliente', 'Monto_Credito', 'Riesgo']])
                    
                    
                    
                except Exception as e:
                    st.error(f"Error de ejecución en la tómbola: {e}")
                    st.stop()
                    
                      
                    
                                                                                                                   
with tab3:
    st.header("📋 Resumen para Comité de Riesgos")

    if 'df_auditoria' in st.session_state:
        df_final = st.session_state['df_auditoria']

        # 1. CÁLCULOS BASE
        df_final['Exp_Bruta'] = df_final['Riesgo'] * df_final['Monto_Credito']
        total_bruto = df_final['Exp_Bruta'].sum()
        
        LGD = 0.45
        total_neto = total_bruto * LGD
        reserva_sugerida = total_bruto * 1.10

        # 2. IDENTIFICACIÓN DE PELIGROS (EL BLOQUE QUE PREGUNTASTE)
        # Umbral de Alerta Roja: 20% (Solo para perfiles críticos)
        peligrosos = df_final[df_final['Riesgo'] >= 0.20]
        num_peligrosos = len(peligrosos)
        
        # Métricas de Variabilidad
        riesgo_max = df_final['Riesgo'].max()
        riesgo_min = df_final['Riesgo'].min()
        max_credito_riesgo = df_final.loc[df_final['Riesgo'].idxmax(), 'Monto_Credito']

        # ==========================================
        # UI EJECUTIVA: INDICADORES PRINCIPALES
        # ==========================================
        c1, c2, c3 = st.columns(3)
        c1.metric("Exposición Bruta", f"${total_bruto:,.2f}")
        c2.metric("Pérdida Esperada (EL)", f"${total_neto:,.2f}")
        c3.metric("Reserva Recomendada", f"${reserva_sugerida:,.2f}")

        st.divider()

        # ==========================================
        # ANÁLISIS DE PUNTOS CRÍTICOS
        # ==========================================
        st.subheader("⚠️ Análisis de Puntos Críticos")
        cp1, cp2, cp3 = st.columns(3)
        
        cp1.write(f"**Clientes en Alerta:** {num_peligrosos}")
        cp2.write(f"**Riesgo Máximo:** {riesgo_max:.2%}")
        cp3.write(f"**Riesgo Mínimo:** {riesgo_min:.2%}")
        
        if num_peligrosos > 0:
            st.warning(f"Se detectaron {num_peligrosos} perfiles que superan el umbral de criticidad del 20%. El crédito con mayor impacto potencial es de ${max_credito_riesgo:,.2f}.")
        else:
            st.success("No se detectaron perfiles por encima del umbral crítico de colapso (20%).")

        st.divider()

        # ==========================================
        # 📌 NOTAS DE AUDITORÍA (LAS 3 JUSTIFICACIONES)
        # ==========================================
        st.subheader("📌 Notas de Auditoría")
        st.write(f"""
        * **Exposición Bruta (${total_bruto:,.2f}):** Representa el capital total en riesgo directo. Es el indicador primario de volatilidad para la cartera de 100 clientes.
        
        * **Pérdida Esperada (${total_neto:,.2f}):** Es el ajuste contable bajo estándares Basilea III. Indica la pérdida real estimada tras aplicar el factor de recuperación (LGD) del 55%.
        
        * **Reserva Recomendada (${reserva_sugerida:,.2f}):** Capital de salvaguarda calculado sobre la exposición bruta más un buffer prudencial del 10% para cubrir desviaciones no lineales.
        """)

        # ==========================================
        # DICTAMEN FINAL
        # ==========================================
        st.success(f"""
        **Dictamen Final:** Se recomienda una provisión de **${reserva_sugerida:,.2f}**. Este monto asegura la solvencia institucional ante los casos críticos detectados por el motor cuántico, blindando la operación de BanCoppel.
        """)
    else:
        st.warning("⚠️ El sistema requiere la ejecución de la auditoría en la Pestaña 2.")
        
# ============================================================
# TAB 4 - VALIDACIÓN EJECUTIVA IBM REAL
# COMPARATIVO AER vs IBM QUANTUM
# ============================================================

with tab4:

    st.header("⚛️ Validación Ejecutiva IBM Quantum")

    st.markdown("""
    Esta sección ejecuta un análisis consolidado de cartera
    utilizando hardware cuántico real de IBM.
    
    La auditoría masiva permanece en AerSimulator.
    
    Aquí únicamente se evalúa el estado global de riesgo
    de la cartera completa.
    """)

    # ========================================================
    # VALIDAR AUDITORÍA PREVIA
    # ========================================================

    if 'df_auditoria' not in st.session_state:

        st.warning(
            "⚠️ Primero ejecuta la auditoría de cartera en TAB 2."
        )

    else:

        df_exec = st.session_state['df_auditoria']

        # ====================================================
        # MÉTRICAS CONSOLIDADAS
        # ====================================================

        riesgo_promedio = float(
            df_exec['Riesgo'].mean()
        )

        volatilidad_promedio = float(
            df_exec['Volatilidad_Sector'].mean()
        )

        exposicion_total = float(
            df_exec['Monto_Credito'].sum()
        )

        # ====================================================
        # NORMALIZACIÓN FINANCIERA
        # ====================================================

        exposicion_normalizada = min(
            exposicion_total / 1000000,
            1.0
        )

        # ====================================================
        # VECTOR EJECUTIVO
        # ====================================================

        vector_ejecutivo = [

            riesgo_promedio,
            volatilidad_promedio,
            exposicion_normalizada

        ]

        st.subheader("📌 Vector Ejecutivo")

        st.write({

            "Riesgo_Promedio":
                round(riesgo_promedio, 4),

            "Volatilidad_Promedio":
                round(volatilidad_promedio, 4),

            "Exposición_Normalizada":
                round(exposicion_normalizada, 4)

        })

        st.divider()

        # ====================================================
        # BOTÓN EJECUCIÓN IBM
        # ====================================================

        if st.button("🚀 Ejecutar Stress Executive en IBM REAL"):

            es_cuantico = "ibm_" in engine_selected

            backend_activo = st.session_state.get(
                'active_backend'
            )

            if not es_cuantico:

                st.error(
                    "⚠️ Selecciona un backend IBM real en la barra lateral."
                )

            elif backend_activo is None:

                st.error(
                    "⚠️ No existe conexión activa con IBM."
                )

            else:

                with st.spinner(
                    "Ejecutando análisis ejecutivo en IBM Quantum..."
                ):

                    try:

                        # ====================================
                        # EJECUCIÓN IBM REAL
                        # ====================================

                        resultado_ibm = (

                            st.session_state
                            .risk_manager
                            .run_stress_test(

                                vector_ejecutivo,

                                use_quantum=True,

                                backend=backend_activo
                            )
                        )

                        # ====================================
                        # RESULTADOS IBM
                        # ====================================

                        riesgo_ibm = (
                            resultado_ibm['Probabilidad']
                        )

                        stress_ibm = (
                            resultado_ibm['Stress_Index']
                        )

                        job_id = (
                            resultado_ibm['Job_ID']
                        )

                        # ====================================
                        # CÁLCULOS FINANCIEROS
                        # ====================================

                        # ====================================
                        # CLIENTES CRÍTICOS IBM
                        # ====================================

                        # ====================================
                        # UMBRAL DINÁMICO IBM
                        # ====================================

                        umbral_ibm = max(

                            riesgo_ibm * 2.5,

                            0.15

                        )
                        
                        clientes_criticos = df_exec[
                            df_exec['Riesgo'] >= umbral_ibm
                        ]

                        # ====================================
                        # EXPOSICIÓN CRÍTICA
                        # ====================================

                        exposicion_critica = clientes_criticos[
                            'Monto_Credito'
                        ].sum()

                        # ====================================
                        # EXPOSICIÓN ESPERADA IBM
                        # ====================================

                        exposicion_esperada = (

                            exposicion_critica
                            * riesgo_ibm
                            * 0.45
                 )           

                        reserva_ibm = (
                            exposicion_esperada * 1.15
                        )
                        
                        umbral_ibm = max(

                         riesgo_ibm * 2.5,

                        0.15

                        )

                        alertas_ibm = len(

                            df_exec[
                                df_exec['Riesgo'] >= umbral_ibm
                            ]
                        )

                        st.info(f"""

                        IBM Quantum detectó únicamente
                        {alertas_ibm} perfiles con sensibilidad sistémica elevada.

                        La reserva táctica se calcula exclusivamente
                        sobre la exposición de dichos clientes críticos,
                        no sobre la totalidad de la cartera.

                        """)
                        
                        # ====================================
                        # DISPLAY EJECUTIVO
                        # ====================================

                        st.success(
                            "✅ IBM Quantum completó el análisis."
                        )

                        st.info(
                            f"🆔 JOB ID IBM: {job_id}"
                        )

                        c1, c2, c3 = st.columns(3)

                        c1.metric(

                            "Exposición Esperada IBM",

                            f"${exposicion_esperada:,.2f}"
                        )

                        c2.metric(

                            "Alertas Críticas IBM",

                            f"{alertas_ibm} clientes"
                        )

                        c3.metric(

                            "Reserva IBM Recomendada",

                            f"${reserva_ibm:,.2f}"
                        )

                        st.divider()

                        # ====================================
                        # COMPARATIVO
                        # ====================================

                        st.subheader(
                            "📊 Comparativo Aer vs IBM"
                        )

                        col_aer, col_ibm = st.columns(2)

                        with col_aer:

                            st.markdown(
                                "### 🖥️ AerSimulator"
                            )

                            st.write(
                                f"Riesgo Promedio: "
                                f"{riesgo_promedio:.2%}"
                            )

                            st.write(
                                f"Exposición Total: "
                                f"${exposicion_total:,.2f}"
                            )

                        with col_ibm:

                            st.markdown(
                                "### ⚛️ IBM Quantum"
                            )

                            st.write(
                                f"Stress Ejecutivo: "
                                f"{stress_ibm:.2f}%"
                            )

                            st.write(
                                f"Reserva Recomendada: "
                                f"${reserva_ibm:,.2f}"
                            )

                        st.divider()

                        # ====================================
                        # DICTAMEN EJECUTIVO
                        # ====================================

                        st.success(f"""

                        Dictamen Ejecutivo Quantum:

                        El hardware cuántico IBM detectó un
                        índice de estrés sistémico de
                        {stress_ibm:.2f}%.

                        Se recomienda una reserva preventiva
                        de capital por
                        ${reserva_ibm:,.2f}.

                        JOB ID:
                        {job_id}

                        """)

                    except Exception as e:

                        st.error(
                            f"❌ Error IBM Quantum: {e}"
                        )
