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
if 'niveles_desbloqueados' not in st.session_state:
    st.session_state.niveles_desbloqueados = 1  # Inicia con el nivel 1 desbloqueado

# --- 2. BASE DE DATOS DE PREGUNTAS (10 Niveles, 5 preguntas c/u) ---
base_preguntas = {
    1: [ # NIVEL 1: Fundamentos (Ley 29783)
        {"escenario": "¿Cuál es el objetivo principal de la Ley 29783 de SST?", "opciones": ["Promover una cultura de prevención", "Pagar los seguros médicos"], "correcta": "Promover una cultura de prevención", "explicacion": "El fin supremo de la ley es promover una cultura de prevención de riesgos laborales en el país."},
        {"escenario": "Según el Principio de Prevención, ¿quién garantiza que los medios y condiciones protejan la vida de los trabajadores?", "opciones": ["El Estado", "El Empleador"], "correcta": "El Empleador", "explicacion": "El empleador es quien garantiza en el centro de trabajo las condiciones que protejan la salud y bienestar."},
        {"escenario": "¿Cuál es el ámbito de aplicación de la Ley 29783?", "opciones": ["Solo el sector privado", "Todos los sectores (público, privado, FFAA)"], "correcta": "Todos los sectores (público, privado, FFAA)", "explicacion": "La ley tiene alcance universal en el territorio peruano, abarcando incluso a trabajadores por cuenta propia."},
        {"escenario": "Situación o característica intrínseca de algo capaz de ocasionar daño:", "opciones": ["Peligro", "Riesgo"], "correcta": "Peligro", "explicacion": "El peligro es la fuente. El riesgo es la probabilidad de que esa fuente cause daño."},
        {"escenario": "¿Qué es un Accidente de Trabajo?", "opciones": ["Suceso repentino por causa o con ocasión del trabajo", "Cualquier lesión ocurrida en las 24 horas del día"], "correcta": "Suceso repentino por causa o con ocasión del trabajo", "explicacion": "Debe existir un nexo causal entre la labor encomendada y la lesión sufrida."}
    ],
    2: [ # NIVEL 2: Gestión Minera y Operativa (D.S. 024-2016-EM)
        {"escenario": "¿A qué actividades aplica el D.S. 024-2016-EM?", "opciones": ["Minería y actividades conexas", "Exclusivamente a la extracción en tajo abierto"], "correcta": "Minería y actividades conexas", "explicacion": "Aplica a actividades mineras superficiales, subterráneas y conexas como transporte y comedores."},
        {"escenario": "Plazo máximo para reportar un accidente mortal a las autoridades competentes:", "opciones": ["24 horas", "72 horas"], "correcta": "24 horas", "explicacion": "Los accidentes mortales deben ser reportados dentro de las 24 horas de ocurridos al MINEM y SUNAFIL."},
        {"escenario": "¿Quién aprueba el Programa Anual de Seguridad y Salud Ocupacional?", "opciones": ["El Comité de SST", "El Gerente General"], "correcta": "El Comité de SST", "explicacion": "Es función principal del Comité de SST aprobar y vigilar el cumplimiento del Programa Anual."},
        {"escenario": "Derecho clave del trabajador ante un peligro inminente y no controlado:", "opciones": ["Retirarse del área de trabajo", "Continuar usando doble EPP"], "correcta": "Retirarse del área de trabajo", "explicacion": "Si una tarea implica riesgo inminente, el trabajador puede suspenderla sin temor a represalias."},
        {"escenario": "La desviación de un estándar seguro en el entorno de trabajo se denomina:", "opciones": ["Acto Subestándar", "Condición Subestándar"], "correcta": "Condición Subestándar", "explicacion": "Las condiciones están ligadas al entorno o a los equipos, los actos están ligados al comportamiento."}
    ],
    3: [ # NIVEL 3: Comité de Seguridad y Salud en el Trabajo
        {"escenario": "¿A partir de cuántos trabajadores es obligatorio conformar un Comité de SST?", "opciones": ["20 a más trabajadores", "50 a más trabajadores"], "correcta": "20 a más trabajadores", "explicacion": "Con 20 o más trabajadores se exige un Comité. Con menos de 20, se elige un Supervisor de SST."},
        {"escenario": "¿Cómo debe ser la composición del Comité de SST?", "opciones": ["Paritaria", "Mayoría sindical"], "correcta": "Paritaria", "explicacion": "Debe tener igual número de representantes del empleador y de los trabajadores."},
        {"escenario": "¿Cómo se elige a los representantes de los trabajadores ante el Comité?", "opciones": ["Elección secreta y directa", "Designación del Gerente"], "correcta": "Elección secreta y directa", "explicacion": "Los trabajadores eligen a sus representantes de forma democrática."},
        {"escenario": "¿Cuál es la frecuencia obligatoria de las reuniones ordinarias del Comité de SST?", "opciones": ["Mensual", "Trimestral"], "correcta": "Mensual", "explicacion": "El CSST debe reunirse ordinariamente una vez al mes, y extraordinariamente cuando ocurra un accidente grave."},
        {"escenario": "Duración del mandato de los representantes de los trabajadores en el Comité:", "opciones": ["1 a 2 años", "Indefinido"], "correcta": "1 a 2 años", "explicacion": "El mandato dura entre uno y dos años según lo determinen en la elección."}
    ],
    4: [ # NIVEL 4: IPERC y Jerarquía de Controles
        {"escenario": "¿Cuál es el primer escalón en la Jerarquía de Controles?", "opciones": ["Eliminación", "Sustitución"], "correcta": "Eliminación", "explicacion": "La eliminación del peligro desde el diseño es la medida más efectiva."},
        {"escenario": "¿Cuál es el último escalón en la Jerarquía de Controles?", "opciones": ["EPP", "Controles Administrativos"], "correcta": "EPP", "explicacion": "El Equipo de Protección Personal es la última barrera de defensa entre el trabajador y el peligro."},
        {"escenario": "Herramienta obligatoria a llenar ANTES de iniciar cualquier tarea rutinaria en minería:", "opciones": ["IPERC Continuo", "Auditoría de Línea Base"], "correcta": "IPERC Continuo", "explicacion": "El IPERC Continuo es el análisis diario y dinámico de los riesgos en el punto exacto de trabajo."},
        {"escenario": "¿Quiénes elaboran el IPERC Continuo en campo?", "opciones": ["Los trabajadores que ejecutarán la labor", "El Ingeniero de Seguridad desde la oficina"], "correcta": "Los trabajadores que ejecutarán la labor", "explicacion": "Los propios trabajadores lo llenan, con la verificación posterior del supervisor."},
        {"escenario": "¿En qué situación es OBLIGATORIO actualizar el IPERC de Línea Base?", "opciones": ["Anualmente o tras un accidente", "Solo cuando cambia el Gerente"], "correcta": "Anualmente o tras un accidente", "explicacion": "Debe actualizarse como mínimo cada año o cuando las condiciones cambien o falle un control."}
    ],
    5: [ # NIVEL 5: Trabajos de Alto Riesgo
        {"escenario": "Documento indispensable para autorizar un Trabajo de Alto Riesgo:", "opciones": ["PETAR", "Checklist de Vehículo"], "correcta": "PETAR", "explicacion": "El Permiso Escrito de Trabajo de Alto Riesgo autoriza la ejecución de actividades críticas."},
        {"escenario": "Altura mínima obligatoria para considerar un Trabajo en Altura y requerir arnés:", "opciones": ["1.80 metros", "2.50 metros"], "correcta": "1.80 metros", "explicacion": "A partir de 1.80m (o en excavaciones profundas), se requieren controles contra caídas."},
        {"escenario": "Acción crítica antes y durante el ingreso a un Espacio Confinado:", "opciones": ["Monitoreo de gases y oxígeno", "Colocar ventiladores domésticos"], "correcta": "Monitoreo de gases y oxígeno", "explicacion": "Se debe asegurar que la atmósfera sea respirable y libre de gases explosivos/tóxicos."},
        {"escenario": "Requisito de personal obligatorio para un Trabajo en Caliente:", "opciones": ["Vigía de fuego con extintor", "Supervisor de RRHH"], "correcta": "Vigía de fuego con extintor", "explicacion": "El vigía monitorea el área durante el trabajo y hasta tiempo después de finalizado."},
        {"escenario": "¿Quiénes firman obligatoriamente el PETAR en campo antes de iniciar?", "opciones": ["El Supervisor del trabajo y el Jefe de Área", "Solo el trabajador"], "correcta": "El Supervisor del trabajo y el Jefe de Área", "explicacion": "El PETAR requiere la validación en sitio de la supervisión responsable."}
    ],
    6: [ # NIVEL 6: Aislamiento y Bloqueo de Energía (LOTO)
        {"escenario": "¿Qué significan las siglas LOTO?", "opciones": ["Lock Out / Tag Out", "Level Of Technical Operations"], "correcta": "Lock Out / Tag Out", "explicacion": "Se traduce como Bloqueo (Candado) y Etiquetado (Tarjeta) de energías peligrosas."},
        {"escenario": "Primer paso del procedimiento general de bloqueo LOTO:", "opciones": ["Preparación e información a involucrados", "Cortar el cable eléctrico"], "correcta": "Preparación e información a involucrados", "explicacion": "Antes de intervenir, todo el personal del área debe saber qué equipo será desenergizado."},
        {"escenario": "¿La tarjeta de advertencia reemplaza al candado de bloqueo?", "opciones": ["No, el candado es obligatorio e irremplazable", "Sí, si no hay candados disponibles"], "correcta": "No, el candado es obligatorio e irremplazable", "explicacion": "La tarjeta informa, pero el candado aísla físicamente la energía."},
        {"escenario": "¿Quién es la única persona autorizada para retirar un candado personal?", "opciones": ["El trabajador dueño del candado", "El Gerente de Operaciones"], "correcta": "El trabajador dueño del candado", "explicacion": "Nadie puede retirar el candado de otra persona, salvo estrictos protocolos de emergencia."},
        {"escenario": "Paso crítico FINAL luego de bloquear, antes de meter las manos al equipo:", "opciones": ["Prueba de energía cero (Disipación)", "Limpiar el área con agua"], "correcta": "Prueba de energía cero (Disipación)", "explicacion": "Siempre se debe verificar que las energías residuales (presión, gravedad, voltaje) hayan sido eliminadas."}
    ],
    7: [ # NIVEL 7: Salud Ocupacional
        {"escenario": "Límite máximo permisible de exposición al ruido para una jornada de 8 horas:", "opciones": ["85 decibeles (dB)", "100 decibeles (dB)"], "correcta": "85 decibeles (dB)", "explicacion": "Por encima de 85 dB es obligatorio el uso de protección auditiva y monitoreo."},
        {"escenario": "¿Quién asume el costo de los Exámenes Médicos Ocupacionales (EMO)?", "opciones": ["El Empleador al 100%", "Descuento por planilla al trabajador"], "correcta": "El Empleador al 100%", "explicacion": "El empleador está obligado a cubrir el costo íntegro de la vigilancia médica."},
        {"escenario": "Objetivo de implementar rotación de tareas y pausas activas:", "opciones": ["Prevenir riesgos disergonómicos", "Reducir el salario"], "correcta": "Prevenir riesgos disergonómicos", "explicacion": "Ayuda a evitar lesiones musculoesqueléticas por movimientos repetitivos o posturas forzadas."},
        {"escenario": "Enfermedad pulmonar ocupacional crónica común en la minería por exposición a polvo:", "opciones": ["Neumoconiosis / Silicosis", "Tétanos"], "correcta": "Neumoconiosis / Silicosis", "explicacion": "Causada por la inhalación prolongada de polvo de sílice cristalina."},
        {"escenario": "¿Quiénes tienen acceso a los resultados detallados del examen médico del trabajador?", "opciones": ["Solo el Médico Ocupacional y el trabajador", "El Gerente General y RRHH"], "correcta": "Solo el Médico Ocupacional y el trabajador", "explicacion": "La información médica es estrictamente confidencial. La empresa solo recibe el certificado de aptitud."}
    ],
    8: [ # NIVEL 8: Inspecciones y Auditorías
        {"escenario": "Objetivo principal de una inspección de seguridad en campo:", "opciones": ["Identificar actos y condiciones subestándares", "Sancionar económicamente"], "correcta": "Identificar actos y condiciones subestándares", "explicacion": "Buscan detectar desviaciones antes de que se conviertan en incidentes o accidentes."},
        {"escenario": "Inspección que obedece a un cronograma y formato previamente establecido:", "opciones": ["Inspección Planeada", "Inspección Inopinada"], "correcta": "Inspección Planeada", "explicacion": "Las planeadas están en el programa anual; las inopinadas son sorpresivas."},
        {"escenario": "Método visual común para asegurar que herramientas manuales fueron inspeccionadas cada mes:", "opciones": ["Uso de cintas de color del mes", "Grabado láser"], "correcta": "Uso de cintas de color del mes", "explicacion": "Facilita a los supervisores identificar visualmente equipos con inspección vigente."},
        {"escenario": "¿Qué acción inmediata sigue tras hallar una condición de riesgo inminente en una inspección?", "opciones": ["Paralizar la labor y aplicar medidas correctivas", "Tomar una foto y seguir trabajando"], "correcta": "Paralizar la labor y aplicar medidas correctivas", "explicacion": "Si la vida está en riesgo, la paralización es obligatoria hasta controlar la condición."},
        {"escenario": "¿Cuál es la frecuencia de ejecución de las Auditorías Externas del SGSST en Minería?", "opciones": ["Dentro de los primeros tres meses de cada año", "Cada cinco años"], "correcta": "Dentro de los primeros tres meses de cada año", "explicacion": "Para evaluar la eficacia del sistema del año anterior según el D.S. 024."}
    ],
    9: [ # NIVEL 9: Investigación de Accidentes
        {"escenario": "El propósito principal de investigar un accidente de trabajo es:", "opciones": ["Identificar causas raíces para evitar que se repita", "Buscar a quién despedir"], "correcta": "Identificar causas raíces para evitar que se repita", "explicacion": "La investigación no busca culpables, busca fallas en el Sistema de Gestión."},
        {"escenario": "Suceso con potencial de causar daños graves o mortales, pero que finalmente NO produjo lesiones:", "opciones": ["Incidente Peligroso", "Accidente Leve"], "correcta": "Incidente Peligroso", "explicacion": "Es una alerta máxima del sistema. Requiere investigación inmediata aunque no haya heridos."},
        {"escenario": "Metodología estructurada altamente recomendada para investigar causas sistémicas:", "opciones": ["ICAM / Árbol de Causas", "Lluvia de ideas"], "correcta": "ICAM / Árbol de Causas", "explicacion": "Métodos como ICAM ayudan a llegar a las fallas organizacionales y factores humanos."},
        {"escenario": "Factores personales o del trabajo que originan directamente los actos/condiciones subestándares:", "opciones": ["Causas Básicas", "Causas Inmediatas"], "correcta": "Causas Básicas", "explicacion": "Las inmediatas son el acto/condición; las básicas son el 'por qué' (falta de conocimiento, diseño deficiente)."},
        {"escenario": "¿A quién se debe entregar la estadística de siniestralidad obligatoriamente?", "opciones": ["Al Ministerio de Trabajo / Autoridad Minera", "A la prensa local"], "correcta": "Al Ministerio de Trabajo / Autoridad Minera", "explicacion": "El Estado consolida esta información a través del registro oficial de accidentes."}
    ],
    10: [ # NIVEL 10: Respuesta a Emergencias y MATPEL
        {"escenario": "¿Qué significan las siglas MATPEL?", "opciones": ["Materiales Peligrosos", "Mantenimiento Técnico de Peligros"], "correcta": "Materiales Peligrosos", "explicacion": "Sustancias que por su naturaleza pueden causar daños a la salud o ambiente."},
        {"escenario": "En el Rombo NFPA 704, ¿qué indica el cuadrante de color ROJO?", "opciones": ["Inflamabilidad", "Riesgo a la Salud"], "correcta": "Inflamabilidad", "explicacion": "Azul es Salud, Rojo es Inflamabilidad, Amarillo Inestabilidad, Blanco Específico."},
        {"escenario": "Fuego originado por equipos o tableros eléctricos energizados corresponde a:", "opciones": ["Fuego Clase C", "Fuego Clase A"], "correcta": "Fuego Clase C", "explicacion": "Requiere agentes extintores no conductores (ej. CO2, PQS)."},
        {"escenario": "Prioridad número UNO ante cualquier emergencia o desastre operativo:", "opciones": ["Salvar y proteger la vida humana", "Salvar la maquinaria costosa"], "correcta": "Salvar y proteger la vida humana", "explicacion": "La vida de los trabajadores siempre prima sobre la continuidad operativa o los activos."},
        {"escenario": "Instalación hermética en minería subterránea que provee oxígeno y seguridad ante incendios/gases:", "opciones": ["Estación de Refugio", "Polvorín"], "correcta": "Estación de Refugio", "explicacion": "Diseñadas para sostener la vida humana de forma autónoma hasta que llegue el rescate minero."}
    ]
}

# --- 3. DISEÑO DE LA INTERFAZ Y BARRA LATERAL ---
with st.sidebar:
    st.title("🧑‍🔧 Perfil Operativo")
    st.subheader(f"Puntos Totales: 🏆 {st.session_state.puntos}")
    st.subheader(f"Vidas: {'❤️' * st.session_state.vidas}{'🖤' * (3 - st.session_state.vidas)}")
    st.progress(st.session_state.niveles_desbloqueados / 10, text=f"Progreso: {st.session_state.niveles_desbloqueados}/10 Niveles")
    
    st.divider()
    st.markdown("**Sistema de Gestión (Niveles)**")
    
    # Generador automático de botones para los 10 niveles
    for i in range(1, 11):
        esta_desbloqueado = i <= st.session_state.niveles_desbloqueados
        icono = "🔓" if esta_desbloqueado else "🔒"
        tipo_boton = "primary" if st.session_state.nivel_actual == i else "secondary"
        
        # Nombres acortados para la barra lateral
        nombres_niveles = ["Fundamentos", "Gestión D.S. 024", "Comité SST", "IPERC", "Trabajos Alto Riesgo", "Bloqueo LOTO", "Salud Ocupacional", "Inspecciones", "Inv. Accidentes", "Emergencias"]
        
        if st.button(f"{icono} N{i}: {nombres_niveles[i-1]}", key=f"btn_n{i}", disabled=not esta_desbloqueado, use_container_width=True, type=tipo_boton):
            st.session_state.nivel_actual = i
            st.session_state.pregunta_actual = 0
            st.rerun()

# --- 4. LÓGICA DEL MOTOR DE PREGUNTAS ---
# Recuperar la lista de preguntas del nivel actual
preguntas = base_preguntas[st.session_state.nivel_actual]

if st.session_state.vidas <= 0:
    st.error("💀 ¡Incidente Reportado! Te quedaste sin vidas. Debes reiniciar la inducción.")
    if st.button("Volver a Inducción"):
        st.session_state.vidas = 3
        st.session_state.puntos = 0
        st.session_state.pregunta_actual = 0
        st.session_state.nivel_actual = 1
        st.session_state.niveles_desbloqueados = 1
        st.rerun()

elif st.session_state.pregunta_actual >= len(preguntas):
    st.success(f"🎉 ¡Has aprobado el Nivel {st.session_state.nivel_actual}!")
    st.balloons()
    
    # Lógica para desbloquear el siguiente nivel
    siguiente_nivel = st.session_state.nivel_actual + 1
    
    if siguiente_nivel <= 10:
        if st.session_state.niveles_desbloqueados < siguiente_nivel:
            st.session_state.niveles_desbloqueados = siguiente_nivel
            
        st.info(f"🔓 ¡Nivel {siguiente_nivel} Desbloqueado!")
        if st.button(f"🚀 Iniciar Nivel {siguiente_nivel}", type="primary"):
            st.session_state.nivel_actual = siguiente_nivel
            st.session_state.pregunta_actual = 0
            st.rerun()
    else:
        st.warning("🏆 ¡CERTIFICACIÓN COMPLETADA! Eres un experto en Cultura de Seguridad 4.0.")

else:
    # Mostrar el encabezado del nivel actual
    titulos = ["Fundamentos Legales (Ley 29783)", "Gestión Operativa (D.S. 024-2016-EM)", "Comité de Seguridad y Salud", "IPERC y Controles", "Trabajos de Alto Riesgo", "Aislamiento y Bloqueo (LOTO)", "Salud Ocupacional", "Inspecciones de Seguridad", "Investigación de Siniestros", "Respuesta a Emergencias"]
    
    st.title(f"Nivel {st.session_state.nivel_actual}: {titulos[st.session_state.nivel_actual - 1]} 🎯")
    
    q = preguntas[st.session_state.pregunta_actual]
    st.info(f"**Pregunta {st.session_state.pregunta_actual + 1} de 5:** \n\n{q['escenario']}")
    
    # Diseño de botones fluidos
    col1, col2 = st.columns(2)
    espacio_mensaje = st.empty()
    opcion_elegida = None
    
    with col1:
        if st.button(q['opciones'][0], use_container_width=True):
            opcion_elegida = q['opciones'][0]
    with col2:
        if st.button(q['opciones'][1], use_container_width=True):
            opcion_elegida = q['opciones'][1]

    # Validación instantánea de respuestas
    if opcion_elegida:
        if opcion_elegida == q['correcta']:
            espacio_mensaje.success(f"✅ ¡Correcto! +10 pts. \n\n*Nota:* {q['explicacion']}")
            st.session_state.puntos += 10
        else:
            espacio_mensaje.error(f"❌ Subestándar detectado. Pierdes una vida. \n\n*Corrección:* {q['explicacion']}")
            st.session_state.vidas -= 1
            
        st.session_state.pregunta_actual += 1
        time.sleep(3.5) # Pausa ampliada para que puedan leer bien la retroalimentación normativa
        st.rerun()
