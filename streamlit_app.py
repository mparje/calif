import PyPDF2
import openai
import streamlit as st
import uuid
from textblob import TextBlob

# Prompt the user for their API key
api_key = st.text_input("Enter your OpenAI API key:")

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

# Define a function to generate an evaluation of the argumentative quality of the text
def evaluate_quality(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    if polarity > 0.2 and subjectivity > 0.4:
        return "Good"
    elif polarity < -0.2 and subjectivity > 0.4:
        return "Poor"
    else:
        return "Neutral"

# Define a function to handle the file upload and evaluation generation
def handle_file_upload():
    file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if file is not None:
        text = extract_text_from_pdf(file)
        st.write("Argumentative quality evaluation:")
        evaluation = st.selectbox("Select a quality rating:", ["Good", "Neutral", "Poor"])
        justification = st.text_area("Justify your rating:")
        st.write("Evaluation:", evaluation)
        st.write("Justification:", justification)

# Define a main function to run the program
def main():
    handle_file_upload()

if __name__ == "__main__":
    main()
