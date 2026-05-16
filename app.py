import streamlit as st
import time

st.set_page_config(page_title="HSEQ Academy 4.0", page_icon="👷‍♂️", layout="centered")

# --- 1. GESTIÓN DEL ESTADO (Memoria del juego) ---
if 'puntos' not in st.session_state:
    st.session_state.puntos = 0
if 'vidas' not in st.session_state:
    st.session_state.vidas = 3
if 'pregunta_actual' not in st.session_state:
    st.session_state.pregunta_actual = 0
if 'nivel_actual' not in st.session_state:
    st.session_state.nivel_actual = 1
if 'nivel_2_desbloqueado' not in st.session_state:
    st.session_state.nivel_2_desbloqueado = False

# --- 2. BARRA LATERAL (Perfil y Progreso) ---
with st.sidebar:
    st.title("🧑‍🔧 Tu Perfil")
    st.subheader(f"Puntos: 🏆 {st.session_state.puntos}")
    st.subheader(f"Vidas: {'❤️' * st.session_state.vidas}{'🖤' * (3 - st.session_state.vidas)}")
    
    st.divider()
    st.markdown("**Árbol de Habilidades**")
    
    # Botones de navegación en el menú lateral
    if st.button("🔓 Nivel 1: Fundamentos", use_container_width=True, type="primary" if st.session_state.nivel_actual == 1 else "secondary"):
        st.session_state.nivel_actual = 1
        st.session_state.pregunta_actual = 0
        st.rerun()
        
    if st.button("🔓 Nivel 2: Operaciones Críticas" if st.session_state.nivel_2_desbloqueado else "🔒 Nivel 2: Bloqueado", 
                 use_container_width=True, 
                 disabled=not st.session_state.nivel_2_desbloqueado,
                 type="primary" if st.session_state.nivel_actual == 2 else "secondary"):
        st.session_state.nivel_actual = 2
        st.session_state.pregunta_actual = 0
        st.rerun()

# --- 3. BASE DE DATOS DE PREGUNTAS (Por Niveles) ---
preguntas_n1 = [
    {
        "escenario": "Camión de acarreo con fallas en el sistema de frenos.",
        "opciones": ["Es un Peligro", "Es un Riesgo"],
        "correcta": "Es un Peligro",
        "explicacion": "El camión con fallas es la fuente con potencial de daño."
    },
    {
        "escenario": "Volcadura del camión y lesión grave del operador.",
        "opciones": ["Es un Peligro", "Es un Riesgo"],
        "correcta": "Es un Riesgo",
        "explicacion": "Es la probabilidad + consecuencia de que el peligro se materialice."
    }
]

preguntas_n2 = [
    {
        "escenario": "Paso 1 del procedimiento LOTO (Aislamiento y Bloqueo de Energía):",
        "opciones": ["Apagar el equipo", "Preparación y Aviso"],
        "correcta": "Preparación y Aviso",
        "explicacion": "Antes de tocar el interruptor, debes conocer el tipo de energía y avisar a todo el personal afectado."
    }
]

# Seleccionar qué preguntas mostrar según el nivel actual
preguntas = preguntas_n1 if st.session_state.nivel_actual == 1 else preguntas_n2

# --- 4. LÓGICA DEL JUEGO ---
if st.session_state.vidas <= 0:
    st.error("💀 ¡Te quedaste sin vidas! Un error en campo no perdona.")
    if st.button("Reiniciar Capacitación"):
        st.session_state.vidas = 3
        st.session_state.puntos = 0
        st.session_state.pregunta_actual = 0
        st.session_state.nivel_actual = 1
        st.rerun()

elif st.session_state.pregunta_actual >= len(preguntas):
    st.success(f"🎉 ¡Nivel {st.session_state.nivel_actual} completado con éxito!")
    st.balloons()
    
    # Lógica de transición de niveles
    if st.session_state.nivel_actual == 1:
        st.session_state.nivel_2_desbloqueado = True
        st.info("🔓 ¡Has desbloqueado el Nivel 2!")
        if st.button("🚀 Iniciar Nivel 2", type="primary"):
            st.session_state.nivel_actual = 2
            st.session_state.pregunta_actual = 0
            st.rerun()
    else:
        st.write("¡Felicidades! Has completado todo el entrenamiento disponible por ahora.")

else:
    st.title(f"Nivel {st.session_state.nivel_actual} 🎯")
    q = preguntas[st.session_state.pregunta_actual]
    
    st.info(f"**Escenario {st.session_state.pregunta_actual + 1}:** {q['escenario']}")
    
    # DISEÑO FLUIDO: Usamos columnas para colocar los botones uno al lado del otro
    col1, col2 = st.columns(2)
    
    # Este espacio vacío sirve para mostrar el mensaje de acierto/error sin descuadrar la pantalla
    espacio_mensaje = st.empty()
    
    opcion_elegida = None
    
    with col1:
        if st.button(q['opciones'][0], use_container_width=True):
            opcion_elegida = q['opciones'][0]
    with col2:
        if st.button(q['opciones'][1], use_container_width=True):
            opcion_elegida = q['opciones'][1]

    # Evaluación instantánea
    if opcion_elegida:
        if opcion_elegida == q['correcta']:
            espacio_mensaje.success(f"✅ ¡Correcto! +10 pts. \n\n*Nota:* {q['explicacion']}")
            st.session_state.puntos += 10
        else:
            espacio_mensaje.error(f"❌ Incorrecto. Pierdes una vida. \n\n*Corrección:* {q['explicacion']}")
            st.session_state.vidas -= 1
            
        # Avanzamos la pregunta internamente
        st.session_state.pregunta_actual += 1
        
        # Hacemos una pausa para que el trabajador pueda leer la explicación antes de pasar
        time.sleep(2.5) 
        
        # Forzamos la recarga de la pantalla con la nueva pregunta
        st.rerun()
