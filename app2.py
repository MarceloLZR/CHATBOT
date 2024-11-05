# app.py

import streamlit as st
from labvision import analyze_image
import os
from apikey import groq_apikey

# Configuración de la API de Groq
os.environ['GROQ_API_KEY'] = groq_apikey

def main():
    st.title("Chatbot Multimodal para Medicina")

    # Configuración de la barra lateral para elegir el modo
    mode = st.sidebar.selectbox("Selecciona el modo:", ["Información sobre Medicamentos", "Generador de Quiz"])

    # Prompt del sistema para la identificación de medicamentos
    system_prompt = (
        "Eres un asistente especializado en la identificación de medicamentos a partir de imágenes. "
        "Cuando recibas una imagen de un medicamento, deberás analizarla y proporcionar información sobre "
        "sus características, usos, y contraindicaciones. Asegúrate de que las respuestas sean precisas y claras. "
        "Si no se reconoce el medicamento, indica que la imagen no es clara o que el medicamento no está identificado."
    )

    # Prompt del sistema para el generador de quiz
    system_prompt_quiz = (
        "Eres un generador de quizzes especializado en temas médicos. Cuando recibas una imagen, "
        "analízala y crea una pregunta tipo quiz con 5 opciones de respuesta, incluyendo la correcta. "
        "No reveles la respuesta correcta inicialmente. Indica claramente las opciones en un formato numerado."
    )

    if mode == "Información sobre Medicamentos":
        st.header("Características, Usos y Contraindicaciones de Medicamentos")
        image_url = st.text_input("Introduce la URL de la imagen del medicamento:")
        if image_url:
            st.image(image_url, caption='Imagen del Medicamento', use_column_width=True)
            
            # Botón dedicado para generar información
            if st.button("Generar Información del Medicamento"):
                # Análisis de la imagen
                analyzed_image = analyze_image(image_url)
                
                # Supongamos que el análisis devuelve un diccionario con la información
                # Ejemplo de análisis ficticio basado en la imagen analizada
                medicamento_info = {
                    "Nombre": "Panadol para Niños",
                    "Características": "Botella rosa con etiqueta azul y blanco, diseñada para niños.",
                    "Usos": "Alivia el dolor leve a moderado, reduce la fiebre.",
                    "Contraindicaciones": "No usar en niños menores de 2 años o en caso de alergia al paracetamol."
                }

                # Formato de la respuesta en Markdown
                response = (
                    f"**Nombre del Medicamento:** {medicamento_info['Nombre']}\n\n"
                    f"**Características:**\n"
                    f"- {medicamento_info['Características']}\n\n"
                    f"**Usos:**\n"
                    f"- {medicamento_info['Usos']}\n\n"
                    f"**Contraindicaciones:**\n"
                    f"- {medicamento_info['Contraindicaciones']}"
                )
                
                # Mostrar la información en formato mejorado
                st.markdown(response)




    elif mode == "Generador de Quiz":
        st.header("Generador de Preguntas para Estudiantes")
        image_url = st.text_input("Introduce la URL de una imagen médica:")
        if image_url:
            st.image(image_url, caption='Imagen Médica', use_column_width=True)
            if st.button("Generar Pregunta"):
                # Análisis de la imagen
                analyzed_image = analyze_image(image_url)
                prompt = f"{system_prompt_quiz}\nImagen Análisis: {analyzed_image}\nGenera la pregunta."
                quiz_response = prompt
                st.write("Pregunta Generada:", quiz_response)

                # Pedir la respuesta correcta
                if st.button("Mostrar Respuesta Correcta"):
                    correct_prompt = f"Indica cuál es la respuesta correcta para la pregunta generada."
                    correct_response = correct_prompt
                    st.write("Respuesta Correcta:", correct_response)

if __name__ == "__main__":
    main()
