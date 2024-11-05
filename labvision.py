# labvision.py

from groq import Groq
import os
from apikey import groq_apikey

# Configuración de la clave API para Groq
os.environ['GROQ_API_KEY'] = groq_apikey

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_image(image_url):
    """
    Función que envía una URL de imagen a la API de Groq para análisis.
    Devuelve la descripción de la imagen proporcionada por el modelo.
    
    Args:
        image_url (str): URL de la imagen a analizar.
    
    Returns:
        str: Descripción proporcionada por el modelo.
    """
    completion = client.chat.completions.create(
        model="llama-3.2-90b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe lo que ves en la imagen"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    # Obtener la descripción de la imagen correctamente
    return completion.choices[0].message.content  # Accede a .content directamente
