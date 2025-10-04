#So for the Ollama to work, you have to basically, I'll provide the link, you have to go to the link, whether you have a Windows, Linux, or Macbook, according to that, download the Allama and then double click or run as administrator that extension and install the Allama. After, make sure to recognize or watch over what's the location of that folder and after that, you have to locate that whichever location that was and see if the Allama.exe extension is still there. If it's there, copy part of that folder, the folder which was installed when you were installing and then we have to click the window plus R which will give us a small window with which we can type sys sysdm.cpl and enter which will give us another window and we from there, we have to go to advanced and then environment variables. In the system, when we have gone to the environment variables, we just go to the system variable and find the path and click edit and then click new and then paste the full folder path and then okay okay okay and then restart our PowerShell or CMD and now check if it works using ollama.serve and all
#
import os
from dotenv import load_dotenv #pip install dotenv langchain langchain_community langchain_huggingface langchain_groq sentence-transformers faiss-cpu
#from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq

# Load API key
load_dotenv()  # expects OPENAI_API_KEY/GROQ_API_KEY in .env

# ---- Step 1: Load FAISS index ----
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)


# ---- Step 2: Setup retriever ----
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})  # top 4 chunks

# ---- Step 3: Setup memory ----
memory = ConversationBufferMemory( # memory guide: https://python.langchain.com/docs/versions/migrating_memory/
    memory_key="chat_history",
    #output_key="result",#result in case of RetreicalQA
    output_key="answer",
    return_messages=True
)

# # ---- Step 4: Setup LLM (OpenAI GPT/Ollama) ----
# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
# llm = ChatOllama(model="llama3.1")

# ---- Step 4: Setup LLM (Groq) ----
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # options: llama-3.1-70b-versatile, mixtral-8x7b, gemma-7b
    temperature=0
)

# # ---- Step 4: Build RetrievalQA chain ----
# qa_chain = RetrievalQA.from_chain_type(  # I dismissed this chain bcz I had to use memory which doesnt work well with RetreivalQA
#     llm=llm,
#     retriever=retriever,
#     memory=memory,
#     chain_type="stuff",  # simple concatenation
#     return_source_documents=True
# )
# print(qa_chain.input_keys)
# print(qa_chain.output_keys)

qa_chain = ConversationalRetrievalChain.from_llm( #This used bcz it includes more contextual memory
    llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    #output_key="result",
    chain_type="stuff"
)

def get_chain():
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    chain=ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        chain_type="stuff"
    )
    return chain

# print(qa_chain.input_keys)  # These tells us that how would be parse input as well as output properly 
# print(qa_chain.output_keys)
######################## You could try "map_reduce" or "refine" if the chunks are big or if answers require more reasoning in chain parameters.


# No need of below code : It was just to check if code and API were working


# # ---- Step 5: Ask a question ----
# query = "What does The maximum admissible friction energy depends on?"
# result = qa_chain({"query": query})

# print("\n=== Answer ===")
# print(result["result"])

# print("\n=== Sources ===")
# # for doc in result["source_documents"]:
# #     print(doc.metadata, " -> ", doc.page_content[:200], "...")

# #wrong:
# # print(f'Source: {result['source_documents'][Document[metadata]]['source']}')

# for doc in result["source_documents"]:
#     source = doc.metadata.get("source", "Unknown Source")
#     page = doc.metadata.get("page", "Unknown Page")
#     print(f"Source: {source}, Page: {page}")
