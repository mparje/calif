import io
from PyPDF2 import PdfReader
import openai
import streamlit as st

# Solicita al usuario que ingrese su clave API de OpenAI
api_key = st.text_input("Ingrese su clave API de OpenAI:")
openai.api_key = api_key

# Función para extraer texto de un archivo PDF
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Función para evaluar la calidad argumentativa del texto utilizando OpenAI
def evaluate_argumentative_quality(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=(
            f"Evalúa la calidad argumentativa de este texto:\n"
            f"{text}\n"
            f"Criterios de evaluación: claridad, relevancia, evidencia, persuasión, respuesta a objeciones, originalidad y utilidad práctica.\n"
        ),
        max_tokens=1024,
        temperature=0.5,
        n = 1,
        stop=None,
        timeout=60,
    )
    quality = response.choices[0].text
    explanation = "Evaluación realizada utilizando el modelo de lenguaje GPT-3 de OpenAI."
    return quality, explanation

# Función para manejar la carga de archivos y la evaluación
def handle_file_upload():
    file = st.file_uploader("Subir un archivo PDF", type=["pdf"])
    if file is not None:
        text = extract_text_from_pdf(file)
        if st.button("Evaluar"):
            quality, explanation = evaluate_argumentative_quality(text)
            st.write(f"Calidad argumentativa: {quality}")
            st.write(explanation)

# Función principal para ejecutar la aplicación Streamlit
def main():
    handle_file_upload()

if __name__ == "__main__":
    main()
