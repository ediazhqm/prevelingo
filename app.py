import streamlit as st
import time

st.set_page_config(page_title="HSEQ Academy 4.0 - Camino del Dragón", page_icon="🐉", layout="centered")

# --- 1. GESTIÓN DEL ESTADO ---
if 'puntos' not in st.session_state: st.session_state.puntos = 0
if 'vidas' not in st.session_state: st.session_state.vidas = 3
if 'pregunta_actual' not in st.session_state: st.session_state.pregunta_actual = 0
if 'nivel_actual' not in st.session_state: st.session_state.nivel_actual = 1
if 'esferas' not in st.session_state: st.session_state.esferas = []

# --- 2. BASE DE DATOS (3 Niveles, 3 preguntas c/u) ---
base_preguntas = {
    1: [ # NIVEL 1: Auditoría
        {"escenario": "¿Con qué frecuencia se deben auditar los SGSST en empresas de alto riesgo?", "opciones": ["Cada 2 años", "Anualmente"], "correcta": "Anualmente", "explicacion": "El D.S. 024 exige auditorías anuales para evaluar la eficacia del sistema."},
        {"escenario": "¿Quién puede ser auditor externo según el D.S. 024?", "opciones": ["Un auditor registrado en el MTPE", "El supervisor de seguridad"], "correcta": "Un auditor registrado en el MTPE", "explicacion": "Debe ser un profesional independiente y debidamente registrado."},
        {"escenario": "¿Cuál es el fin último de una auditoría?", "opciones": ["Sancionar al trabajador", "Mejorar la eficacia del sistema"], "correcta": "Mejorar la eficacia del sistema", "explicacion": "La auditoría identifica brechas para la mejora continua del PHVA."}
    ],
    2: [ # NIVEL 2: Fiscalización
        {"escenario": "¿Qué entidad es la autoridad central de fiscalización en SST en Perú?", "opciones": ["SUNAFIL", "Ministerio de Salud"], "correcta": "SUNAFIL", "explicacion": "SUNAFIL es la autoridad responsable de la inspección del trabajo y SST."},
        {"escenario": "¿Las actuaciones de fiscalización de SUNAFIL requieren aviso previo?", "opciones": ["Sí, 48 horas antes", "No, son inopinadas"], "correcta": "No, son inopinadas", "explicacion": "La fiscalización busca verificar las condiciones reales, por lo que son sorpresivas."},
        {"escenario": "¿Qué ocurre si una empresa impide la fiscalización?", "opciones": ["Se reprograma la visita", "Es considerada una infracción muy grave"], "correcta": "Es considerada una infracción muy grave", "explicacion": "La obstrucción a la labor inspectiva es una falta de alta penalidad."}
    ],
    3: [ # NIVEL 3: Inspecciones de Seguridad
        {"escenario": "¿Cuál es la diferencia principal entre una inspección y una auditoría?", "opciones": ["La inspección es puntual/campo, la auditoría es sistémica", "Ninguna, son iguales"], "correcta": "La inspección es puntual/campo, la auditoría es sistémica", "explicacion": "La inspección detecta condiciones inseguras inmediatas; la auditoría evalúa el diseño del sistema."},
        {"escenario": "¿Qué herramienta es vital para asegurar que las herramientas manuales fueron inspeccionadas?", "opciones": ["Código de colores mensual", "Solo revisión visual"], "correcta": "Código de colores mensual", "explicacion": "El uso de cintas o marcas de color permite identificar rápidamente si la herramienta pasó inspección."},
        {"escenario": "¿Qué acción sigue tras detectar una condición subestándar en una inspección?", "opciones": ["Registrarla para el informe mensual", "Corregirla de inmediato y si es grave, paralizar"], "correcta": "Corregirla de inmediato y si es grave, paralizar", "explicacion": "Ante un riesgo inminente, la prioridad es la protección de la vida."}
    ]
}

# --- 3. INTERFAZ Y LÓGICA ---
st.title("🐉 HSEQ Academy: Camino del Guerrero")
st.sidebar.markdown(f"### 🟠 Esferas recolectadas: {len(st.session_state.esferas)}/3")
st.sidebar.write(" ".join(st.session_state.esferas))

# Pantalla de finalización
if st.session_state.nivel_actual > 3:
    st.success("¡FELICIDADES! Has reunido las 3 esferas del dragón.")
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJ4dGg1eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l41lTjJp8whYyG2uQ/giphy.gif")
    st.header("¡Apareció Shenlong! Tu nivel en Seguridad y Normatividad es experto.")
    if st.button("Reiniciar camino"):
        st.session_state.nivel_actual = 1
        st.session_state.esferas = []
        st.rerun()

else:
    preguntas = base_preguntas[st.session_state.nivel_actual]
    q = preguntas[st.session_state.pregunta_actual]
    
    titulos = ["Auditoría del SGSST", "Fiscalización (SUNAFIL)", "Inspecciones de Campo"]
    st.subheader(f"Nivel {st.session_state.nivel_actual}: {titulos[st.session_state.nivel_actual - 1]}")
    st.info(f"**Pregunta {st.session_state.pregunta_actual + 1}/3:** {q['escenario']}")
    
    opcion = st.radio("Selecciona una opción:", q['opciones'])
    
    if st.button("Validar Respuesta"):
        if opcion == q['correcta']:
            st.session_state.puntos += 10
            st.success("¡Correcto! +10 pts")
            time.sleep(1)
            st.session_state.pregunta_actual += 1
        else:
            st.session_state.vidas -= 1
            st.error(f"¡Incidente! {q['explicacion']}")
            time.sleep(2)
        
        # Verificar si terminó el nivel
        if st.session_state.pregunta_actual >= 3:
            st.balloons()
            st.session_state.esferas.append("🟠")
            st.session_state.nivel_actual += 1
            st.session_state.pregunta_actual = 0
            st.rerun()
        
        if st.session_state.vidas <= 0:
            st.error("💀 Sin vidas. Reiniciando camino...")
            st.session_state.vidas = 3
            st.session_state.nivel_actual = 1
            st.session_state.esferas = []
            st.rerun()
