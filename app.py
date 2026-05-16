import streamlit as st
import time

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="HSEQ Academy 4.0", page_icon="👷‍♂️", layout="centered")

# --- 2. GESTIÓN DEL ESTADO (Memoria del juego) ---
# Aquí guardamos los puntos y vidas del trabajador mientras navega
if 'puntos' not in st.session_state:
    st.session_state.puntos = 0
if 'vidas' not in st.session_state:
    st.session_state.vidas = 3
if 'pregunta_actual' not in st.session_state:
    st.session_state.pregunta_actual = 0

# --- 3. BARRA LATERAL (Perfil y Progreso) ---
with st.sidebar:
    st.title("🧑‍🔧 Tu Perfil")
    st.subheader(f"Puntos Totales: 🏆 {st.session_state.puntos}")
    st.subheader(f"Vidas: {'❤️' * st.session_state.vidas}{'🖤' * (3 - st.session_state.vidas)}")
    
    st.divider()
    st.markdown("**Árbol de Habilidades**")
    st.button("🔓 Nivel 1: Fundamentos", use_container_width=True, type="primary")
    st.button("🔒 Nivel 2: Operaciones", use_container_width=True, disabled=True)
    st.button("🔒 Nivel 3: Resp. Emergencias", use_container_width=True, disabled=True)

# --- 4. CONTENIDO PRINCIPAL: MÓDULO 1.1 ---
st.title("Nivel 1: Identificando al Enemigo 🎯")
st.markdown("Bienvenido al módulo básico. En terreno, confundir un **Peligro** con un **Riesgo** puede ser fatal. Demuestra que sabes la diferencia.")

# Base de datos de preguntas (Diccionario de Python)
preguntas = [
    {
        "escenario": "Camión de acarreo con fallas en el sistema de frenos operando en rampa.",
        "opciones": ["Es un Peligro", "Es un Riesgo"],
        "respuesta_correcta": "Es un Peligro",
        "explicacion": "El camión con fallas es la **fuente o situación** con potencial de daño (Peligro)."
    },
    {
        "escenario": "Volcadura del camión durante la bajada y lesión grave del operador.",
        "opciones": ["Es un Peligro", "Es un Riesgo"],
        "respuesta_correcta": "Es un Riesgo",
        "explicacion": "La volcadura y lesión son la **probabilidad + consecuencia** de que el peligro se materialice (Riesgo)."
    },
    {
        "escenario": "Ruido de 95 dB en la zona de chancado primario.",
        "opciones": ["Es un Peligro", "Es un Riesgo"],
        "respuesta_correcta": "Es un Peligro",
        "explicacion": "El ruido es el agente físico presente en el ambiente (Peligro)."
    }
]

# Lógica de fin de juego
if st.session_state.vidas <= 0:
    st.error("💀 ¡Te quedaste sin vidas! Un error en campo no perdona. Repasa la matriz IPERC y vuelve a intentarlo.")
    if st.button("Reiniciar Módulo"):
        st.session_state.vidas = 3
        st.session_state.puntos = 0
        st.session_state.pregunta_actual = 0
        st.rerun()

elif st.session_state.pregunta_actual >= len(preguntas):
    st.success(f"🎉 ¡Módulo completado! Excelente trabajo. Puntos finales: {st.session_state.puntos}")
    st.balloons()
    if st.button("Volver a jugar"):
        st.session_state.pregunta_actual = 0
        st.rerun()

# Lógica del cuestionario interactivo
else:
    q = preguntas[st.session_state.pregunta_actual]
    
    st.info(f"**Escenario {st.session_state.pregunta_actual + 1}:** {q['escenario']}")
    
    # Formulario para evitar recargas hasta que el usuario confirme
    with st.form(key=f"form_{st.session_state.pregunta_actual}"):
        respuesta_usuario = st.radio("¿Qué representa esta condición?", q['opciones'], index=None)
        submit_button = st.form_submit_button(label="Comprobar Respuesta")

    if submit_button:
        if respuesta_usuario == None:
            st.warning("⚠️ Selecciona una opción antes de comprobar.")
        elif respuesta_usuario == q['respuesta_correcta']:
            st.success("✅ ¡Correcto! +10 puntos.")
            st.caption(f"💡 *Nota técnica:* {q['explicacion']}")
            st.session_state.puntos += 10
            st.session_state.pregunta_actual += 1
            time.sleep(2) # Pausa dramática breve
            st.rerun() # Recarga la app para mostrar la siguiente pregunta
        else:
            st.error("❌ Incorrecto. Pierdes una vida.")
            st.caption(f"💡 *Corrección:* {q['explicacion']}")
            st.session_state.vidas -= 1
            time.sleep(2)
            st.rerun()