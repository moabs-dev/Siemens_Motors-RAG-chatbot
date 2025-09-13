import streamlit as st #pip install streamlit
#from langchain.chat_models import ChatOpenAI
#from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load API keys from .env
load_dotenv()

# ---- Load FAISS index ----
#embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(
    "faiss_index", 
    embeddings,
    allow_dangerous_deserialization=True)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# ---- Setup LLM ----
# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # options: llama-3.1-70b-versatile, mixtral-8x7b, gemma-7b
    temperature=0
)


qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    return_source_documents=True
)

# ---- Streamlit UI ----
st.title("📘 DC Machines Chatbot")

query = st.text_input("Ask me anything about DC Machines:")

if query:
    result = qa_chain({"query": query})
    
    st.subheader("Answer")
    st.write(result["result"])
    
    with st.expander("📌 Sources Info"):
        for doc in result["source_documents"]:
            st.write(doc.page_content[:300] + "...")
