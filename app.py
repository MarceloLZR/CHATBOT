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
st.markdown("""
    <style>
        .app-header {
            display: flex;
            align-items: center;
            gap: 20px;
            padding: 1rem;
            margin-bottom: 2rem;
        }
        .logo-container {
            width: 100px;
            height: 100px;
        }
        .logo-container img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
        .title-container {
            flex-grow: 1;
        }
        .medical-warning {
            background-color: #e3f2fd;
            color: #1565c0;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
            border-left: 5px solid #1565c0;
            font-size: 16px;
        }
        .important-text {
            color: #d32f2f;
            font-weight: bold;
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

# Función para generar respuestas
def generar_respuesta(prompt, historial):
    mensajes = [{"role": "system", "content": SISTEMA_PROMPT}]
    
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

# Inicializar el historial de chat en la sesión si no existe
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

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
            respuesta = generar_respuesta(prompt, st.session_state.mensajes)
            st.write(respuesta)
    
    st.session_state.mensajes.append({"content": respuesta, "is_user": False})

# Barra lateral con información y configuraciones
with st.sidebar:
    st.title("ℹ️ Información")
    # Usamos st.sidebar.image y luego HTML para dar margen
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
    
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.mensajes = []
        st.rerun()

    especialidad = st.selectbox(
        "Área de interés",
        ["Medicina General", "Pediatría", "Cardiología", "Nutrición", "Dermatología"]
    )