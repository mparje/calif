import PyPDF2
import openai
import streamlit as st

# Solicita al usuario su clave API de OpenAI
api_key = st.text_input("Ingresa tu clave API de OpenAI:")

# Configura la API de OpenAI con la clave API proporcionada
openai.api_key = api_key

# Define una función para extraer texto de un archivo PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Define una función para generar respuestas a preguntas de usuario utilizando la API de ChatGPT
def generate_answer(question, text):
    max_context_length = 4096 - len(question) - 30
    truncated_text = text[:max_context_length]
    prompt = f"{truncated_text}\n\nPregunta: {question}\nRespuesta:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    answer = response.choices[0].text.strip()
    return answer

# Define una función para evaluar la comprensión del usuario basándose en el texto proporcionado
def evaluate(text):
    num_questions = 0
    num_correct = 0
    total_score = 0
    questions = [
        "¿Cuál es el tema principal del texto?",
        "¿Cuál es la tesis del autor?",
        "¿Cuáles son los argumentos que utiliza el autor para sostener su tesis?",
        "¿Cuáles son las conclusiones del autor?",
        "¿Cuál es tu opinión sobre el texto?",
    ]
    for question in questions:
        user_answer = st.text_input(question)
        if user_answer:
            num_questions += 1
            answer = generate_answer(question, text)
            if answer.lower() == user_answer.lower():
                num_correct += 1
                total_score += 2
            elif user_answer.lower() in answer.lower():
                total_score += 1
    if num_questions == 0:
        return "Por favor, responde al menos una pregunta para evaluar tu comprensión."
    else:
        score = round((total_score / (num_questions * 2)) * 10, 2)
        return f"Tu calificación es: {score}/10"

# Define una función para manejar la carga de archivos y la generación de respuestas
def handle_file_upload():
    file = st.file_uploader("Sube un archivo PDF", type=["pdf"])
    if file is not None:
        text = extract_text_from_pdf(file)
        st.write(evaluate(text))

# Llama a la función handle_file_upload para ejecutar la aplicación
handle_file_upload()
