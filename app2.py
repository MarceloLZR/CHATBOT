import streamlit as st
import os
from groq import Groq
import base64
from PIL import Image
import io
import requests
from io import BytesIO
from apikey import groq_apikey  # Importar la clave de API desde apikey.py

# Configuración de la página
st.set_page_config(
    page_title="Asistente Médico con Análisis de Imágenes",
    page_icon="💊",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
        .body {
            color: #1f1f1f;  /* Cambia este valor por el color que desees */
        }
        h1, h2, h3, h4, h5, h6 {
            color: #007bff;  /* Cambia el color de los encabezados */
        }
        .app-header {
            display: flex;
            align-items: center;
            padding: 1rem;
            margin-bottom: 2rem;
            background-color: #f8f9fa; /* Color de fondo del encabezado */
            border-radius: 10px;
        }
        .upload-section {
            background-color: #e0f7fa; /* Color celeste claro */
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .analysis-section {
            background-color: #e1f5fe; /* Color celeste claro */
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border: 1px solid #e0e0e0;
        }
        .warning-text {
            color: #d32f2f;
            font-weight: bold;
        }
        .info-box {
            background-color: #b3e5fc; /* Color celeste */
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        .chat-message {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 5px;
        }
        .user-message {
            background-color: #b3e5fc; /* Color celeste claro */
        }
        .assistant-message {
            background-color: #e1f5fe; /* Color celeste claro */
        }
    </style>
""", unsafe_allow_html=True)


# Inicializar el cliente de Groq
client = Groq(api_key=groq_apikey)
# Prompt inicial para el asistente
SISTEMA_PROMPT = """Eres un asistente médico virtual especializado en análisis de medicamentos y consultas médicas generales.
Debes:
1. Proporcionar información precisa sobre medicamentos y sus usos
2. Advertir sobre la importancia de consultar profesionales médicos
3. Dar información sobre efectos secundarios y precauciones
4. Mantener un tono profesional pero amigable
5. Ser claro sobre las limitaciones del servicio"""

def get_image_from_url(url):
    """Descarga una imagen desde una URL"""
    try:
        response = requests.get(url)
        return Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"Error al descargar la imagen: {str(e)}")
        return None

def encode_image_to_base64(image):
    """Convierte una imagen a base64"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def analyze_medication_image(image_base64):
    """Analiza la imagen del medicamento usando Groq"""
    prompt = """Analiza esta imagen de medicamento y proporciona:
    1. Nombre del medicamento (si es visible)
    2. Dosis recomendada
    3. Frecuencia de uso
    4. Precauciones importantes
    5. Efectos secundarios comunes
    6. Interacciones medicamentosas
    7. Condiciones de almacenamiento"""
    
    try:
        respuesta = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image", "image": image_base64}
                    ]
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=2048
        )
        return respuesta.choices[0].message.content
    except Exception as e:
        return f"Error al analizar la imagen: {str(e)}"

def get_bot_response(prompt, history):
    """Genera una respuesta del chatbot"""
    mensajes = [{"role": "system", "content": SISTEMA_PROMPT}]
    
    for mensaje in history:
        mensajes.append({
            "role": "user" if mensaje["is_user"] else "assistant",
            "content": mensaje["content"]
        })
    
    mensajes.append({"role": "user", "content": prompt})
    
    try:
        respuesta = client.chat.completions.create(
            messages=mensajes,
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=2048
        )
        return respuesta.choices[0].message.content
    except Exception as e:
        return f"Error al generar respuesta: {str(e)}"

# Inicializar el estado de la sesión
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Título y descripción
st.markdown("""
    <div class="app-header">
        <h1>💊 Asistente Médico Virtual con Análisis de Imágenes</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="info-box">
        <p>Este asistente puede analizar imágenes de medicamentos y responder preguntas médicas generales.</p>
        <p class="warning-text">⚠️ IMPORTANTE: Esta herramienta es solo informativa. Siempre consulte a un profesional de la salud.</p>
    </div>
""", unsafe_allow_html=True)

# Sección de carga de imagen
with st.expander("📸 Análisis de Medicamentos por Imagen", expanded=True):
    tab1, tab2 = st.tabs(["Subir Imagen", "URL de Imagen"])
    
    with tab1:
        uploaded_file = st.file_uploader("Sube una imagen del medicamento", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Imagen cargada", use_column_width=True)
            if st.button("Analizar imagen subida"):
                with st.spinner("Analizando imagen..."):
                    image_base64 = encode_image_to_base64(image)
                    analysis = analyze_medication_image(image_base64)
                    st.markdown(analysis)
                    st.session_state.mensajes.append({"content": f"Análisis de imagen:\n{analysis}", "is_user": False})
    
    with tab2:
        image_url = st.text_input("Ingresa la URL de la imagen del medicamento")
        if image_url:
            if st.button("Analizar imagen desde URL"):
                with st.spinner("Descargando y analizando imagen..."):
                    image = get_image_from_url(image_url)
                    if image:
                        st.image(image, caption="Imagen descargada", use_column_width=True)
                        image_base64 = encode_image_to_base64(image)
                        analysis = analyze_medication_image(image_base64)
                        st.markdown(analysis)
                        st.session_state.mensajes.append({"content": f"Análisis de imagen:\n{analysis}", "is_user": False})

# Área de chat
st.markdown("### 💬 Chat Médico")

# Mostrar historial del chat
for mensaje in st.session_state.mensajes:
    with st.chat_message("user" if mensaje["is_user"] else "assistant"):
        st.write(mensaje["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tu pregunta médica aquí..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    st.session_state.mensajes.append({"content": prompt, "is_user": True})
    
    with st.chat_message("assistant"):
        with st.spinner("Procesando respuesta..."):
            respuesta = get_bot_response(prompt, st.session_state.mensajes)
            st.write(respuesta)
    
    st.session_state.mensajes.append({"content": respuesta, "is_user": False})

# Barra lateral
with st.sidebar:
    st.title("ℹ️ Información")
    st.markdown("""
    ### Capacidades del Asistente
    - Análisis de imágenes de medicamentos
    - Información sobre dosificación
    - Consultas médicas generales
    - Efectos secundarios y precauciones
    
    ### Recomendaciones
    - Usa imágenes claras y bien iluminadas
    - Incluye el empaque del medicamento
    - Sé específico en tus preguntas
    
    ### ⚠️ Limitaciones
    - No realiza diagnósticos
    - No reemplaza la consulta médica
    - No prescribe medicamentos
    """)
    
    if st.button("🗑️ Limpiar Conversación"):
        st.session_state.mensajes = []
        st.rerun()