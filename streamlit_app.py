import PyPDF2
import openai
import streamlit as st

# Prompt the user for their API key
api_key = st.text_input("Ingrese su clave API de OpenAI:")

# Set up the OpenAI API with the provided API key
openai.api_key = api_key

# Define a function to extract text from a PDF file
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfFileReader(file)
    num_pages = pdf_reader.getNumPages()
    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()
    return text

# Define a function to evaluate the quality of an argument
def evaluar_argumento(argumento):
    # Realizamos una evaluación de la coherencia, la claridad, la relevancia y la validez lógica del argumento
    # y devolvemos un puntaje en función de su calidad global.
    # Esto es solo una implementación básica, y se podría adaptar según las necesidades específicas.

    # Evaluación de la coherencia
    coherencia_score = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Evaluación de la coherencia del argumento:\n\n{argumento}\n",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text.strip()

    # Evaluación de la claridad
    claridad_score = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Evaluación de la claridad del argumento:\n\n{argumento}\n",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text.strip()

    # Evaluación de la relevancia
    relevancia_score = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Evaluación de la relevancia del argumento:\n\n{argumento}\n",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text.strip()

    # Evaluación de la validez lógica
    logica_score = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Evaluación de la validez lógica del argumento:\n\n{argumento}\n",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text.strip()

    # Devolvemos un puntaje promedio para el argumento
    puntaje = (float(coherencia_score) + float(claridad_score) + float(relevancia_score) + float(logica_score)) / 4.0
    return puntaje

# Define a function to handle the file upload and argument evaluation
def handle_file_upload():
    file = st.file_uploader("Cargar un archivo PDF", type=["pdf"])
    if file is not None:
        text = extract_text_from_pdf(file)
        argumento = st.text_area("Ingrese el argumento a evaluar:")
        if st.button("Evaluar"):
            puntaje = evaluar_argumento(argumento)
            st.write(f"Puntaje del argumento: {puntaje:.2f}")

# Define a main function to run the program
def main():
    handle_file_upload()

    if name == "main":
    main()
