# Siemens Motors RAG Chatbot 🚀

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-teal.svg)](https://fastapi.tiangolo.com/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50+-red.svg)](https://streamlit.io/)  
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-yellow.svg)](https://www.langchain.com/)  
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)  

---

## 📌 Overview

**Siemens Motors RAG Chatbot** is a **context-aware AI assistant** built for Siemens Motors employees.  
Instead of searching through long catalogs, employees can directly ask questions about the catalog, and the chatbot answers contextually.

This project leverages:

- **LangChain** as the backbone for orchestration  
- **FAISS** as the vector database  
- **HuggingFace embeddings** for semantic search  
- **Groq LLMs** (but also supports OpenAI and Ollama)  
- **FastAPI** for the backend  
- **Streamlit** for the frontend  
- **Docker** for containerization  

---

## 📂 Folder Structure

```
project-root/
│── .env                  # API keys (OpenAI, Groq, HuggingFace, etc.)
│── docker-compose.yml    # Defines backend + frontend services
│── LICENSE               # MIT License
│── motors-catalog.pdf    # Catalog data used for embeddings
│── errorFaced.txt        # Notes on encountered errors during dev
│── outputs/              # Sample outputs & screenshots
│
├── Backend/
│   ├── backend.py        # Core LLM, retriever, memory setup
│   ├── backend2.py       # API endpoints (uses functions from backend.py)
│   ├── back.py           # LLM chain logic (ConversationalRetrievalChain)
│   ├── requirements.txt  # Backend dependencies
│   ├── Dockerfile        # Backend Dockerfile
│
├── Frontend/
│   ├── frontend.py       # Streamlit frontend
│   ├── frontend2.py      # Modified Streamlit frontend
│   ├── requirements.txt  # Frontend dependencies
│   ├── Dockerfile        # Frontend Dockerfile
│
├── database_creation/
│   ├── text_extract.py   # Extract text & chunk from PDF
│   ├── test1.py          # Experimental database creation
│
├── faiss_index/          # Vector DB built from catalog
│
└── outputs/              # Validation screenshots & test runs
```

---

## ⚙️ Workflow

1. **Database Creation**  
   - PDF catalog is processed → chunked → embeddings generated using HuggingFace.  
   - FAISS index is saved inside `faiss_index/`.

2. **Backend (FastAPI)**  
   - Exposes endpoints:  
     - `/set_key` → set API key (overrides `.env`)  
     - `/chat` → handle user queries, return answer + sources  

3. **Frontend (Streamlit)**  
   - UI where employees set API key & chat with the bot.  
   - For each query → frontend sends it to backend → backend retrieves relevant chunks → passes to LLM → returns contextual answer.

4. **Models Supported**  
   - Groq (`ChatGroq`)  
   - OpenAI (`ChatOpenAI`)  
   - Ollama (`ChatOllama`)  

---

## 🐳 Running with Docker

### 1. Build & Run with Compose
```bash
docker-compose up --build
```

This will start:
- **Backend** → http://localhost:8000  
- **Frontend** → http://localhost:8501  

### 2. Using Pre-built Images
Pull directly from Docker Hub:

```bash
docker pull moeenabbas/rag_on_seimens_catalog-backend:latest
docker pull moeenabbas/rag_on_seimens_catalog-frontend:latest
```

Then run:
```bash
docker-compose up -d
```

---

## 🛠️ Setup without Docker (Development Mode)

1. Clone the repository:
```bash
git clone https://github.com/moabs-dev/siemens-motors-rag-chatbot.git
cd siemens-motors-rag-chatbot
```

2. Setup Backend:
```bash
cd Backend
pip install -r requirements.txt
uvicorn backend2:app --reload
```

3. Setup Frontend:
```bash
cd ../Frontend
pip install -r requirements.txt
streamlit run frontend2.py
```

---

## 🔑 Environment Variables

Add a `.env` file in the root with your keys:
```env
OPENAI_API_KEY=your_openai_key_here
GROQ_API_KEY=your_groq_key_here
HUGGINGFACEHUB_API_TOKEN=your_hf_key_here
```

---

## 📸 Outputs

Screenshots & validation examples are inside the `outputs/` folder:
- Valid API key test  
- Example Q&A workflow  
- Error handling for invalid key  

---

## 🧩 Customization

- Replace `motors-catalog.pdf` with your own documents.  
- Re-run `database_creation/text_extract.py` to regenerate FAISS index.  
- Swap models in `backend.py` (`ChatGroq`, `ChatOpenAI`, or `ChatOllama`).  
- Extend memory type, chain type (`stuff`, `map_reduce`, etc.) depending on complexity.  

---

## 📄 License

This project is licensed under the **MIT License** – free to use, modify, and distribute.

---

## 🙌 Credits

Developed by **Moeen Abbas**  
Built with **LangChain, HuggingFace, Groq, OpenAI, FastAPI, Streamlit, and Docker**.
