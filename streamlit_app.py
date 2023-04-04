import PyPDF2
import openai
import streamlit as st

# Prompt the user for their API key
api_key = st.text_input("Enter your OpenAI API key:")

# Define a function to extract text from a PDF file
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Define a function to evaluate the argumentative quality of the text
def evaluate_argumentative_quality(text):
    prompt = f"Please evaluate the argumentative quality of the following text:\n\n{text}\n\nQuality:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    quality = response.choices[0].text.strip()
    return quality

# Define a function to handle the file upload and answer generation
def handle_file_upload():
    file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if file is not None:
        text = extract_text_from_pdf(file)

        if st.button("Evaluate"):
            quality = evaluate_argumentative_quality(text)
            st.write(f"Argumentative Quality: {quality}")

# Define a main function to run the program
def main():
    handle_file_upload()

if __name__ == "__main__":
    main()
