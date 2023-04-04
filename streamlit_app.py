import PyPDF2
import re
import spacy
import streamlit as st

# Prompt the user for their PDF file
file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Set up the NLP model
nlp = spacy.load("en_core_web_sm")

# Define a function to extract text from a PDF file
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Define a function to score the quality of the argumentation in a text
def score_argumentation(text):
    # Split the text into sentences
    sentences = re.split(r"\.|\!|\?", text)

    # Calculate the average length of a sentence
    sentence_lengths = [len(sentence.split()) for sentence in sentences]
    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)

    # Calculate the percentage of sentences that are complex
    num_complex_sentences = 0
    for sentence in sentences:
        doc = nlp(sentence)
        num_clauses = len([token for token in doc if token.dep_ == "mark"])
        if num_clauses > 2:
            num_complex_sentences += 1
    percent_complex_sentences = num_complex_sentences / len(sentences)

    # Determine if the text has a clear thesis statement
    thesis_statement = None
    for sentence in sentences:
        if "thesis" in sentence.lower() or "argument" in sentence.lower():
            thesis_statement = sentence
            break

    # Determine if the text provides sufficient evidence to support its thesis
    evidence = None
    for sentence in sentences:
        if "evidence" in sentence.lower():
            evidence = sentence
            break

    # Determine if the text provides sufficient counterarguments
    counterarguments = None
    for sentence in sentences:
        if "counterargument" in sentence.lower() or "refutation" in sentence.lower():
            counterarguments = sentence
            break

    # Score the text based on the Harvard criteria
    score = 0
    if avg_sentence_length < 25:
        score += 1
    if percent_complex_sentences < 0.3:
        score += 1
    if thesis_statement is not None:
        score += 1
    if evidence is not None:
        score += 1
    if counterarguments is not None:
        score += 1

    return score

# Define a function to handle the file upload and argumentation scoring
def handle_file_upload():
    if file is not None:
        text = extract_text_from_pdf(file)
        score = score_argumentation(text)
        st.write(f"The quality of the argumentation in this text is {score}/5.")
    else:
        st.write("Please upload a PDF file.")

# Define a main function to run the program
def main():
    handle_file_upload()

if __name__ == "__main__":
    main()
