import fitz  # PyMuPDF for PDF processing
from transformers import pipeline

summarizer = pipeline('summarization')

def process_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    notes = summarizer(text, max_length=300, min_length=50, do_sample=False)
    return notes[0]['summary_text']

# Example usage:
# notes = process_pdf('example.pdf')
