# app.py
import streamlit as st
import PyPDF2
from transformers import pipeline

# Load summarizer model (Hugging Face)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

st.title("📄 AI PDF Summarizer")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    # Extract text
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.subheader("Extracted Text")
    st.write(pdf_text[:1000] + "..." if len(pdf_text) > 1000 else pdf_text)

    # Summarize
    if st.button("Summarize"):
        summary = summarizer(pdf_text[:2000], max_length=200, min_length=50, do_sample=False)
        st.subheader("Summary")
        st.write(summary[0]['summary_text'])
