import streamlit as st
import os
from groq import Groq
from apikey import groq_apikey  # Importar la clave de API desde apikey.py

# Configuración de la página
st.set_page_config(
    page_title="Asistente Médico Virtual",
    page_icon="🏥",
    layout="wide"
)

# Estilos CSS personalizados
# Forzar tema claro
# Forzar tema claro y personalizar área de chat

# Forzar tema claro y personalizar áreas completas
st.markdown("""
    <style>
        /* Forzar fondo blanco en todo el contenedor */
        [data-testid="stAppViewContainer"] {
            background-color: #ffffff !important;
        }
        
        /* Estilo para el header (barra superior) */
        [data-testid="stHeader"] {
            background-color: #bbdefb !important;
            border-bottom: 1px solid #90caf9;
        }
        
        /* Estilo para el footer (barra inferior) */
        footer {
            background-color: #bbdefb !important;
            border-top: 1px solid #90caf9;
            padding: 0 !important; /* Eliminar el padding de la barra inferior */
        }
        
        /* Color del texto en el header y footer */
        [data-testid="stHeader"] button [data-testid="stMarkdown"] p,
        footer [data-testid="stMarkdown"] p {
            color: #1976d2 !important;
        }
        
        [data-testid="stToolbar"] {
            background-color: #bbdefb !important;
        }
        
        /* Sidebar (área izquierda) */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #90caf9;
        }
        
        /* Personalización del área de input del chat */
        [data-testid="stChatInput"] {
            background-color: #ffffff !important;
            border: 1px solid #90caf9 !important;
            border-radius: 10px !important;
            padding: 8px !important;
            box-shadow: none !important;  /* Elimina el borde negro o sombra que puede estar apareciendo */
        }
        
        [data-testid="stChatInput"] > div {
            background-color: #bbdefb !important;
        }
        
        /* Color negro para el texto del input y mayor tamaño */
        [data-testid="stChatInput"] input {
            color: #0000FF !important;
            font-size: 1.1em !important;
            font-weight: 500 !important;
        }
        
        [data-testid="stChatInput"] input::placeholder {
            color: #64b5f6 !important;
        }
        
        /* Estilo para los elementos del sidebar */
        .css-1d391kg, .css-1544g2n {
            background-color: #ffffff !important;
        }
        
        .stButton>button {
            background-color: #1976d2;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
        }
        
        /* Encabezado */
        .app-header {
            background-color: #bbdefb;
            padding: 1rem;
            margin-bottom: 2rem;
            border-bottom: 1px solid #90caf9;
        }
        
        /* Advertencia médica */
        .medical-warning {
            background-color: #ffffff;
            color: #2c3e50;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            border-left: 5px solid #1976d2;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* Chat messages */
        [data-testid="stChatMessage"] {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            border: 1px solid #90caf9;
        }
        
        /* Títulos */
        h1, h2, h3 {
            color: #1976d2;
        }
        
        /* Links */
        a {
            color: #1976d2;
        }
        
        /* Selector de especialidad */
        .stSelectbox [data-baseweb="select"] {
            background-color: #ffffff;
        }
        
        /* Botón Deploy y otros elementos de la barra superior */
        [data-testid="stToolbar"] button,
        [data-testid="baseButton-headerNoPadding"] {
            background-color: #bbdefb !important;
            color: #1976d2 !important;
            border: 1px solid #90caf9 !important;
        }
        
        /* Ajustes para mejorar la legibilidad del texto en general */
        .stMarkdown {
            color: #000000;
        }
    </style>
""", unsafe_allow_html=True)



client = Groq(api_key=groq_apikey)

# Prompt inicial para configurar el comportamiento del asistente médico
SISTEMA_PROMPT = """Eres un asistente médico virtual diseñado para proporcionar información médica general y orientación básica. 
Importantes consideraciones:
1. Siempre aclara que no reemplazas la consulta con un profesional médico real.
2. En casos de emergencia, indica que deben buscar atención médica inmediata.
3. Proporciona información basada en evidencia médica actualizada.
4. Mantén un tono profesional pero amable y empático.
5. Si no estás seguro de algo, indícalo claramente.
6. Evita dar diagnósticos definitivos, en su lugar, sugiere posibles causas y recomienda consultar a un médico.
7. Proporciona información sobre prevención y hábitos saludables cuando sea apropiado."""

# Función para generar respuestas según la especialidad seleccionada
def generar_respuesta(prompt, historial, especialidad):
    mensajes = [{"role": "system", "content": SISTEMA_PROMPT}]
    
    # Adaptar el comportamiento según la especialidad seleccionada
    if especialidad:
        especialidad_prompt = f"Actúa como un especialista en {especialidad}. Responde basándote en esa especialidad."
        mensajes.append({"role": "system", "content": especialidad_prompt})
    
    for mensaje in historial:
        mensajes.append({
            "role": "user" if mensaje["is_user"] else "assistant",
            "content": mensaje["content"]
        })
    
    mensajes.append({"role": "user", "content": prompt})
    
    chat_completion = client.chat.completions.create(
        messages=mensajes,
        model="mixtral-8x7b-32768",
        temperature=0.7,
        max_tokens=2048
    )
    
    return chat_completion.choices[0].message.content

# Inicializar las variables de estado en la sesión
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

if "especialidad" not in st.session_state:
    st.session_state.especialidad = None

if "especialidad_anterior" not in st.session_state:
    st.session_state.especialidad_anterior = None

# Header con logo y título
st.markdown("""
    <div class="app-header">
        <div class="title-container">
            <h1>🏥 VITAL BOT: Asistente Médico Virtual</h1>
        </div>
    </div>
""", unsafe_allow_html=True)

# Mensaje de advertencia con nuevo diseño
st.markdown("""
    <div class="medical-warning">
        ⚕️ Este asistente proporciona información médica general y orientación básica.
        <br><span class="important-text">Nota importante:</span> Este servicio no sustituye la consulta con un profesional médico.
        <br><span class="important-text">En caso de emergencia, busque atención médica inmediata.</span>
    </div>
""", unsafe_allow_html=True)

# Área de chat
for mensaje in st.session_state.mensajes:
    with st.chat_message("user" if mensaje["is_user"] else "assistant"):
        st.write(mensaje["content"])

# Input del usuario
if prompt := st.chat_input("Describe tus síntomas o haz una pregunta médica..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    st.session_state.mensajes.append({"content": prompt, "is_user": True})
    
    with st.chat_message("assistant"):
        with st.spinner("Analizando tu consulta..."):
            respuesta = generar_respuesta(prompt, st.session_state.mensajes, st.session_state.especialidad)
            st.write(respuesta)
    
    st.session_state.mensajes.append({"content": respuesta, "is_user": False})

# Barra lateral con información y configuraciones
with st.sidebar:
    st.title("ℹ️ Información")
    st.sidebar.markdown("""
        <div style="display: flex; justify-content: center; margin-left: 30px;">
    """, unsafe_allow_html=True)

    st.sidebar.image("vitalbot.jpg", width=100)

    st.sidebar.markdown("""
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### Sobre este asistente
    Este asistente médico virtual puede ayudarte con:
    - Información general sobre condiciones médicas
    - Orientación sobre síntomas comunes
    - Consejos de prevención y vida saludable
    - Información sobre medicamentos generales
    
    ### ⚠️ Limitaciones
    - No puede diagnosticar enfermedades
    - No reemplaza la consulta médica profesional
    - No puede recetar medicamentos
    - No maneja emergencias médicas
    
    ### 🚨 En caso de emergencia
    Contacta inmediatamente a servicios de emergencia o acude al centro médico más cercano.
    """)

    # Área de selección de especialidad en la barra lateral
    especialidad = st.selectbox(
        "Área de interés",
        ["Medicina General", "Pediatría", "Cardiología", "Nutrición", "Dermatología"]
    )
    
    # Verificar si la especialidad cambió
    if st.session_state.especialidad != especialidad:
        st.session_state.mensajes = []  # Limpiar la conversación si cambia la especialidad
        st.session_state.especialidad_anterior = st.session_state.especialidad  # Actualizar la especialidad anterior
        st.session_state.especialidad = especialidad  # Actualizar la especialidad actual
    
    # Botón para limpiar la conversación
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.mensajes = []
        st.rerun()
