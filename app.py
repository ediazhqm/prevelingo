import streamlit as st
import time

st.set_page_config(page_title="HSEQ Academy 4.0", page_icon="🐉", layout="centered")

# --- 1. GESTIÓN DEL ESTADO ---
if 'puntos' not in st.session_state: st.session_state.puntos = 0
if 'vidas' not in st.session_state: st.session_state.vidas = 3
if 'idx' not in st.session_state: st.session_state.idx = 0  # Índice global de preguntas (0 a 8)
if 'esferas' not in st.session_state: st.session_state.esferas = []

# --- 2. BASE DE DATOS TEÓRICA (Basado en tu PDF) ---
# 3 preguntas de Auditoría, 3 de Fiscalización, 3 de Inspecciones
preguntas = [
    # AUDITORÍA
    {"pregunta": "¿Qué caracteriza la labor de un auditor según la normativa?", "opciones": ["Es independiente e íntegra", "Busca sancionar al personal"], "correcta": "Es independiente e íntegra"},
    {"pregunta": "¿Qué resulta al comparar una evidencia contra un criterio?", "opciones": ["Un Hallazgo / No Conformidad", "Una sanción económica"], "correcta": "Un Hallazgo / No Conformidad"},
    {"pregunta": "¿Cuál es la meta principal de una auditoría de SST?", "opciones": ["Mejorar el SGSST y prevenir riesgos", "Realizar una inspección de rutina"], "correcta": "Mejorar el SGSST y prevenir riesgos"},
    # FISCALIZACIÓN
    {"pregunta": "¿Qué entidad actúa como árbitro de la gran minería en SST?", "opciones": ["SUNAFIL", "Ministerio de Educación"], "correcta": "SUNAFIL"},
    {"pregunta": "¿Cómo son usualmente las visitas de fiscalización?", "opciones": ["Inopinadas", "Programadas con meses de aviso"], "correcta": "Inopinadas"},
    {"pregunta": "¿Qué verifica la fiscalización de SUNAFIL?", "opciones": ["El cumplimiento de la normatividad", "El horario de almuerzo"], "correcta": "El cumplimiento de la normatividad"},
    # INSPECCIONES
    {"pregunta": "¿Cuál es la frecuencia del check-list pre-operacional?", "opciones": ["Diaria", "Trimestral"], "correcta": "Diaria"},
    {"pregunta": "¿Qué metodología se usa para examinar situaciones críticas?", "opciones": ["Observación Planeada (OPT)", "Lluvia de ideas"], "correcta": "Observación Planeada (OPT)"},
    {"pregunta": "¿Qué sigue tras la ejecución de una inspección?", "opciones": ["Establecer y seguir planes de acción", "Archivar sin revisar"], "correcta": "Establecer y seguir planes de acción"}
]

# --- 3. INTERFAZ ---
st.title("🐉 HSEQ Academy: Camino a Shenlong")
st.sidebar.subheader(f"Esferas: {' '.join(st.session_state.esferas)}")
st.sidebar.write(f"Vidas: {'❤️' * st.session_state.vidas}")

# --- 4. LÓGICA DE FLUJO ---
if st.session_state.idx < len(preguntas):
    q = preguntas[st.session_state.idx]
    
    # Categorización visual basada en el índice
    cat = "Auditoría" if st.session_state.idx < 3 else "Fiscalización" if st.session_state.idx < 6 else "Inspecciones"
    st.subheader(f"Nivel: {cat}")
    st.write(f"**Pregunta {st.session_state.idx + 1}/9:** {q['pregunta']}")
    
    seleccion = st.radio("Elige una opción:", q['opciones'], key=f"radio_{st.session_state.idx}")
    
    if st.button("Validar Respuesta"):
        if seleccion == q['correcta']:
            st.session_state.puntos += 10
            st.success("✅ ¡Correcto!")
            
            # Ganar esfera cada 3 preguntas
            if (st.session_state.idx + 1) % 3 == 0:
                st.balloons()
                st.session_state.esferas.append("🟠")
            
            time.sleep(1)
            st.session_state.idx += 1
            st.rerun()
        else:
            st.session_state.vidas -= 1
            st.error("❌ ¡Incorrecto!")
            if st.session_state.vidas <= 0:
                st.warning("💀 Has agotado tus vidas. Reiniciando...")
                time.sleep(2)
                st.session_state.puntos = 0
                st.session_state.vidas = 3
                st.session_state.idx = 0
                st.session_state.esferas = []
            st.rerun()

else:
    # Pantalla final de victoria
    st.image("https://media.giphy.com/media/l41lTjJp8whYyG2uQ/giphy.gif")
    st.success("¡FELICIDADES! Has reunido las 3 esferas. ¡Shenlong ha aparecido y te otorga el dominio de la prevención!")
    if st.button("Reiniciar misión"):
        st.session_state.idx = 0
        st.session_state.esferas = []
        st.session_state.puntos = 0
        st.rerun()
