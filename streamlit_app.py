import PyPDF2
import openai
import streamlit as st

# Solicita al usuario que ingrese su clave API de OpenAI
api_key = st.text_input("Ingrese su clave API de OpenAI:")
openai.api_key = api_key

# Función para extraer texto de un archivo PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Función para evaluar la calidad argumentativa del texto utilizando OpenAI
def evaluate_argumentative_quality(text):
    prompt = f"Por favor, evalúe la calidad argumentativa del siguiente texto:\n\n{text}\n\nCalidad argumentativa:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    quality = response.choices[0].text.strip()
    explanation = f"La explicación de la evaluación es: {response.choices[0].text.strip()}"
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
