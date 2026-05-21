import streamlit as st
import time

st.set_page_config(page_title="HSEQ Academy 4.0", page_icon="🐉", layout="centered")

# --- 1. GESTIÓN DEL ESTADO ---
if 'idx' not in st.session_state: st.session_state.idx = 0 
if 'vidas' not in st.session_state: st.session_state.vidas = 3
if 'esferas' not in st.session_state: st.session_state.esferas = []

# --- 2. BASE DE DATOS ---
preguntas = [
    {"pregunta": "¿Qué caracteriza la labor de un auditor según la normativa?", "opciones": ["Es independiente e íntegra", "Busca sancionar al personal"], "correcta": "Es independiente e íntegra"},
    {"pregunta": "¿Qué resulta al comparar una evidencia contra un criterio?", "opciones": ["Un Hallazgo / No Conformidad", "Una sanción económica"], "correcta": "Un Hallazgo / No Conformidad"},
    {"pregunta": "¿Cuál es la meta principal de una auditoría de SST?", "opciones": ["Mejorar el SGSST y prevenir riesgos", "Realizar una inspección de rutina"], "correcta": "Mejorar el SGSST y prevenir riesgos"},
    {"pregunta": "¿Qué entidad actúa como árbitro de la seguridad laboral en Perú?", "opciones": ["SUNAFIL", "Ministerio de Educación"], "correcta": "SUNAFIL"},
    {"pregunta": "¿Cómo son usualmente las visitas de fiscalización?", "opciones": ["Inopinadas", "Programadas con meses de aviso"], "correcta": "Inopinadas"},
    {"pregunta": "¿Qué verifica la fiscalización de SUNAFIL?", "opciones": ["El cumplimiento de la normatividad", "El horario de almuerzo"], "correcta": "El cumplimiento de la normatividad"},
    {"pregunta": "¿Cuál es la frecuencia del check-list pre-operacional?", "opciones": ["Diaria", "Trimestral"], "correcta": "Diaria"},
    {"pregunta": "¿Qué metodología se usa para examinar situaciones críticas?", "opciones": ["Observación Planeada (OPT)", "Lluvia de ideas"], "correcta": "Observación Planeada (OPT)"},
    {"pregunta": "¿Qué sigue tras la ejecución de una inspección?", "opciones": ["Establecer y seguir planes de acción", "Archivar sin revisar"], "correcta": "Establecer y seguir planes de acción"}
]

# --- 3. INTERFAZ ---
st.title("🐉 HSEQ Academy: Camino a Shenlong")
st.sidebar.subheader(f"Esferas: {' '.join(st.session_state.esferas)}")
st.sidebar.write(f"Vidas: {'❤️' * st.session_state.vidas}")

# --- 4. LÓGICA DE FLUJO ---
# Si aún no llegamos a la pregunta 9, mostramos el juego
if st.session_state.idx < len(preguntas):
    q = preguntas[st.session_state.idx]
    
    st.subheader(f"Pregunta {st.session_state.idx + 1} de 9")
    st.write(f"**{q['pregunta']}**")
    
    opcion = st.radio("Elige:", q['opciones'], key=f"q_{st.session_state.idx}")
    
    if st.button("Validar Respuesta"):
        if opcion == q['correcta']:
            st.success("✅ ¡Correcto!")
            # Ganar esfera en la pregunta 3, 6 y 9
            if (st.session_state.idx + 1) % 3 == 0:
                st.session_state.esferas.append("🟠")
            
            st.session_state.idx += 1
            time.sleep(0.5)
            st.rerun()
        else:
            st.session_state.vidas -= 1
            st.error("❌ ¡Incorrecto!")
            if st.session_state.vidas <= 0:
                st.session_state.idx = 0
                st.session_state.vidas = 3
                st.session_state.esferas = []
            st.rerun()

# Si llegamos a la pregunta 9 (idx == 9), mostramos el éxito
else:
    st.balloons()
    st.success("¡FELICIDADES! Has reunido las 3 esferas.")
    st.image("https://media.giphy.com/media/l41lTjJp8whYyG2uQ/giphy.gif")
    st.header("¡Apareció Shenlong! Has completado el entrenamiento.")
    
    if st.button("Reiniciar camino"):
        st.session_state.idx = 0
        st.session_state.esferas = []
        st.session_state.vidas = 3
        st.rerun()
