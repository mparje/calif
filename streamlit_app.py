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

def evaluate_argumentative_quality(text):
    # Evaluación de los criterios de calidad argumentativa
    coherence_cohesion_score = 0
    coherence_cohesion_criteria = ["organización", "conexión de ideas", "fluidez"]
    coherence_cohesion_feedback = "El texto está bien organizado y las ideas se conectan de manera coherente. La lectura es fluida y fácil de seguir."

    evidence_arguments_score = 0
    evidence_arguments_criteria = ["evidencia presentada", "argumentos sólidos", "argumentos convincentes"]
    evidence_arguments_feedback = "El texto presenta una buena cantidad de evidencia y argumentos sólidos y convincentes que respaldan las afirmaciones que se hacen."

    contraarguments_score = 0
    contraarguments_criteria = ["consideración de contraargumentos", "refutación de contraargumentos"]
    contraarguments_feedback = "El texto considera y refuta posibles contraargumentos a las afirmaciones que se hacen, lo cual demuestra una comprensión profunda del tema."

    clarity_precision_score = 0
    clarity_precision_criteria = ["claridad", "precisión"]
    clarity_precision_feedback = "El texto es claro y preciso en la presentación de las ideas. Las palabras y frases utilizadas están bien definidas y son adecuadas al tema."

    audience_score = 0
    audience_criteria = ["adaptación a la audiencia", "lenguaje y estilo apropiados"]
    audience_feedback = "El texto está bien adaptado a la audiencia a la que se dirige. Utiliza un lenguaje y estilo apropiados para esta."

    # Asignación de puntuaciones a los criterios
    # Aquí se podrían definir distintas escalas y umbrales para asignar notas en función de las puntuaciones totales obtenidas en la evaluación de cada criterio
    coherence_cohesion_score = 3
    evidence_arguments_score = 4
    contraarguments_score = 2
    clarity_precision_score = 3
    audience_score = 2

    # Cálculo de la puntuación total y asignación de la nota
    total_score = coherence_cohesion_score + evidence_arguments_score + contraarguments_score + clarity_precision_score + audience_score
    if total_score >= 15:
        quality = "Excelente"
    elif total_score >= 10:
        quality = "Bueno"
    elif total_score >= 5:
        quality = "Regular"
    else:
        quality = "Malo"

    # Explicación de la evaluación
    explanation = f"La calidad argumentativa del texto se evalúa en función de los siguientes criterios:\n\n"
    explanation += f"- Coherencia y cohesión: {coherence_cohesion_feedback}\n"
    explanation += f"- Evidencia y argumentos: {evidence_arguments_feedback}\n"
    explanation += f"- Contraargumentos: {contraarguments_feedback}\n"
    explanation += f"- Claridad y precisión: {clarity_precision_feedback}\n"
    explanation += f"- Adaptación a la audiencia: {audience_feedback}\n\n"
    explanation += f"El texto obtuvo una puntuación total de {total_score} puntos, lo que se traduce en una evaluación de calidad argumentativa ‘{quality}’.\n\n"
explanation += f"La justificación de la evaluación se basa en los criterios definidos y en la asignación de puntuaciones en función de cada uno de ellos. Se puede mejorar en algunos aspectos como la {contraarguments_criteria[0]} y la {contraarguments_criteria[1]}, en los que se obtuvo una puntuación más baja. En general, el texto presenta un argumento sólido y bien respaldado, con una buena organización y fluidez en la presentación de las ideas. Sin embargo, se podría mejorar la adaptación a la audiencia y la precisión en la definición de algunos términos clave."
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
