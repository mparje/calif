import streamlit as st
import openai
import PyPDF4
from textblob import TextBlob
from textblob import TextBlob

def polarity_score(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    return polarity


# Set up the OpenAI API with the provided API key
api_key = st.text_input("Enter your OpenAI API key:")
openai.api_key = api_key

# Define a function to extract text from a PDF file
def extract_text_from_pdf(file):
    pdf_reader = PyPDF4.PdfFileReader(file)
    num_pages = pdf_reader.getNumPages()
    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()
    return text

# Define a function to generate a quality score for the text
def generate_quality_score(text):
    # Use TextBlob to get a polarity score for the text
    blob = TextBlob(text)
    polarity_score = blob.sentiment.polarity

    # Use OpenAI's GPT-3 to get a coherence score for the text
    prompt = f"Please rate the coherence of the following text on a scale of 1 to 5, with 5 being highly coherent and 1 being not coherent: \n{text}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    coherence_score = int(response.choices[0].text.strip())

    # Calculate the overall quality score
    quality_score = (polarity_score + coherence_score) / 2

    return quality_score

# Define a function to handle the file upload and quality score generation
def handle_file_upload():
    file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if file is not None:
        text = extract_text_from_pdf(file)
        quality_score = generate_quality_score(text)
        st.write(f"The quality score for the PDF is {quality_score}")
        st.write("Justification:")
        st.write("- The polarity score (based on sentiment analysis) is", polarity_score)
        st.write("- The coherence score (based on OpenAI's GPT-3) is", coherence_score)

# Define a main function to run the program
def main():
    handle_file_upload()

if __name__ == "__main__":
    main()
