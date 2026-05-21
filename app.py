import streamlit as st
import time
import random

st.set_page_config(page_title="PREVELINGO", page_icon="🐉", layout="centered")

# --- 1. GESTIÓN DEL ESTADO ---
if 'idx' not in st.session_state: st.session_state.idx = 0 
if 'vidas' not in st.session_state: st.session_state.vidas = 3
if 'esferas' not in st.session_state: st.session_state.esferas = []

# --- 2. BASE DE DATOS (Teoría del PDF integrada) ---
preguntas = [
    {"pregunta": "¿Qué caracteriza la labor de un auditor según la normativa?", "opciones": ["Es independiente e íntegra", "Busca sancionar al personal", "Es una actividad administrativa"], "correcta": "Es independiente e íntegra"},
    {"pregunta": "¿Qué resulta al comparar una evidencia contra un criterio?", "opciones": ["Un Hallazgo / No Conformidad", "Una sanción económica", "Un reporte de gastos"], "correcta": "Un Hallazgo / No Conformidad"},
    {"pregunta": "¿Cuál es la meta principal de una auditoría de SST?", "opciones": ["Realizar una inspección de rutina", "Mejorar el SGSST y prevenir riesgos", "Cumplir por obligación"], "correcta": "Mejorar el SGSST y prevenir riesgos"},
    {"pregunta": "¿Qué entidad actúa como árbitro de la seguridad laboral en Perú?", "opciones": ["Ministerio de Educación", "SUNAFIL", "Municipalidad"], "correcta": "SUNAFIL"},
    {"pregunta": "¿Cómo son usualmente las visitas de fiscalización?", "opciones": ["Programadas con meses de aviso", "Inopinadas", "Por solicitud del cliente"], "correcta": "Inopinadas"},
    {"pregunta": "¿Qué verifica la fiscalización de SUNAFIL?", "opciones": ["El horario de almuerzo", "El cumplimiento de la normatividad", "La infraestructura de oficinas"], "correcta": "El cumplimiento de la normatividad"},
    {"pregunta": "¿Cuál es la frecuencia del check-list pre-operacional?", "opciones": ["Trimestral", "Mensual", "Diaria"], "correcta": "Diaria"},
    {"pregunta": "¿Qué metodología se usa para examinar situaciones críticas?", "opciones": ["Lluvia de ideas", "Observación Planeada (OPT)", "Auditoría externa"], "correcta": "Observación Planeada (OPT)"},
    {"pregunta": "¿Qué sigue tras la ejecución de una inspección?", "opciones": ["Establecer y seguir planes de acción", "Archivar sin revisar", "Ignorar las desviaciones"], "correcta": "Establecer y seguir planes de acción"}
]

# --- 3. LÓGICA DE INTERFAZ ---
st.title("🐉 HSEQ Academy: Camino a Shenlong")
st.sidebar.subheader(f"Esferas: {' '.join(st.session_state.esferas)}")
st.sidebar.write(f"Vidas: {'❤️' * st.session_state.vidas}")

# --- PANTALLA DE VICTORIA ---
if st.session_state.idx >= len(preguntas):
    st.balloons()
    st.success("¡FELICIDADES! Has reunido las 3 esferas.")
    
    # Representación visual de Shenlong usando texto y emojis (100% visible)
    st.markdown("""
    ### ¡SHENLONG HA APARECIDO! 🐉✨
    
    # 🐉🐉🐉🐉🐉🐉
    # 🐉   🔥🐲🔥   🐉
    # 🐉   ✨✨✨   🐉
    # 🐉🐉🐉🐉🐉🐉
    
    Tu conocimiento en Auditoría, Fiscalización e Inspección es nivel experto.
    """)
    
    if st.button("Reiniciar camino"):
        st.session_state.idx = 0
        st.session_state.esferas = []
        st.session_state.vidas = 3
        st.rerun()

# --- MODO JUEGO ---
else:
    q = preguntas[st.session_state.idx]
    
    # Barajar opciones al cargar la pregunta
    if f"ops_{st.session_state.idx}" not in st.session_state:
        opts = q['opciones'][:]
        random.shuffle(opts)
        st.session_state[f"ops_{st.session_state.idx}"] = opts
    
    st.subheader(f"Pregunta {st.session_state.idx + 1} de 9")
    st.write(f"**{q['pregunta']}**")
    
    opcion = st.radio("Elige una opción:", st.session_state[f"ops_{st.session_state.idx}"], key=f"q_{st.session_state.idx}")
    
    if st.button("Validar Respuesta"):
        if opcion == q['correcta']:
            st.success("✅ ¡Correcto!")
            # Ganar esfera cada 3 preguntas (Auditoría, Fiscalización, Inspecciones)
            if (st.session_state.idx + 1) % 3 == 0:
                st.session_state.esferas.append("🟠")
            st.session_state.idx += 1
            time.sleep(1)
            st.rerun()
        else:
            st.session_state.vidas -= 1
            st.error("❌ ¡Incorrecto!")
            if st.session_state.vidas <= 0:
                st.session_state.idx = 0
                st.session_state.vidas = 3
                st.session_state.esferas = []
            st.rerun()
