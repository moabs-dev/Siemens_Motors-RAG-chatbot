              
# 
# ---------- Step 1: Imports ----------
#Situation: Your currently installed version of Keras is Keras 3, but this is not yet supported in Transformers. Please install the backwards-compatible tf-keras package with `pip install tf-keras`.
#Situation: Xet Storage is enabled for this repo, but the 'hf_xet' package is not installed. Falling back to regular HTTP download. For better performance, install the package with: `pip install huggingface_hub[hf_xet]` or `pip install hf_xet`
#Situation: ImportError: Could not import faiss python package. Please install it with `pip install faiss-gpu` (for CUDA supported GPU) or `pip install faiss-cpu` (depending on Python version).
from langchain_community.document_loaders import PyMuPDFLoader #pip install langchain pypdf pymupdf sentence-transformers  -U langchain-huggingface

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
import os

pdf_path = "Siemens_SIMOTICS_Motors_catalog_2018.pdf"   # put your PDF here

def extract_clean_text(ab):
    # ---------- Step 2: Load PDF ----------
    loader = PyMuPDFLoader(ab)
    docs = loader.load()
    
    print(f"✅ Loaded {len(docs)} pages from PDF.")
    
    # ---------- Step 3: Text Cleaning ----------
    cleaned_docs = []
    for d in docs:
        text = d.page_content.strip()
        if not text:
            continue
    
        # Flatten newlines
        text = text.replace("\n", " ")
    
        # Remove figure/table references like "Figure 1.3", "Table 2.1"
        words = []
        skip_next = False
        for w in text.split():
            if w.lower().startswith(("figure","table","Figure","Table")):
                skip_next = True   # also skip next token (usually the number)
                continue
            if skip_next:
                skip_next = False
                continue
            words.append(w)
    
        d.page_content = " ".join(words).strip()
        if d.page_content:  # keep only non-empty
            cleaned_docs.append(d)
    
    print(f"📖 After cleaning: {len(cleaned_docs)} pages retained.")
    return cleaned_docs


def chunk_text(cd,chnk,ovrlp):
    # ---------- Step 4: Split into Chunks ----------
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chnk,   # adjustable (try 500–1500 depending on model/context)
        chunk_overlap=ovrlp
    )
    
    chunks = text_splitter.split_documents(cd)
    print(f"✂️ Split into {len(chunks)} chunks.")
    return chunks #its length shows 567(# of pages)

# ---------- Step 5: Inspect Sample ----------
print("\n🔍 Sample chunk:\n")
ex=extract_clean_text(pdf_path)
ch=chunk_text(ex,1000,500)
print(ch[0].page_content[:800])   # preview first 800 characters
 
output_folder="faiss_index"
def build_embd_faiss_index(model,chnk):
    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name=model)
    
    # Build FAISS index
    vectorstore = FAISS.from_documents(chnk, embeddings)
    
    # Save index locally
    vectorstore.save_local(output_folder)
    return vectorstore

if os.path.exists('faiss_index'):
    pass
else:
    out=build_embd_faiss_index("all-MiniLM-L6-v2",ch)

#can use any of the embeddings

# embeds=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
# vect=FAISS.from_documents(ch,embeds)
# vect.save_local('tring')



