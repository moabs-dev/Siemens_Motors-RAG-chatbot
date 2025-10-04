
import fitz  # PyMuPDF

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# --- Run it ---
pdf_path = "dc_machines.pdf"
text = extract_text_from_pdf(pdf_path)
print("Total characters:", len(text))

chunks = chunk_text(text, chunk_size=1000, overlap=200)
print("Total chunks:", len(chunks))
print("First chunk preview:\n", chunks[0][:300])

