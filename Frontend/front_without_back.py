import streamlit as st
import requests
import json
import os

st.set_page_config(page_title='RAG application')
st.title("📘 Motors Co. Chatbot")

API_URL='http://127.0.0.1:8989/chat'

with st.sidebar:

    st.header('Choose between OpenAI, Groq, or Llama.')
    st.write('API Keys would be required for OpenAI and Groq but not for Llama')
    Models=['OpenAI','Groq','Llama']
    selection = st.selectbox('Select:',Models)
    # if selection == "OpenAI" or selection == "Groq":
    # OR 
    if selection in ['OpenAI','Groq']:
        #API_KEY = st.text_area('Enter API key :', height= 69 , placeholder='Ch4I82jw9bt70ri')
        user_api_key = st.text_input('Enter API key :', placeholder='Ch4I82jw9bt70ri')

    # if st.button("Save API Key"):
    #     if API_KEY:
    #         # save to .env file
    #         with open(".env", "w") as f:
    #             f.write(f"API_KEY={API_KEY}\n")
    #         st.success("✅ API Key saved to .env file!")
    #     else:
    #         st.warning("Please enter a valid API key.")    
    if user_api_key:
        # Save API key into .env file
        with open(".env", "w") as f:
            f.write(f"GROQ_API_KEY={user_api_key}\n")
    
        # Update environment variable for current session
        os.environ["GROQ_API_KEY"] = user_api_key
        st.success("✅ API key saved and loaded!")
       
from Backend.back import qa_chain
query = st.text_area("Ask me about Electronics and Motors Company insights:")
src=st.checkbox('Give Sources')
if st.button('Ask agent'):
    if query.strip():
        result = qa_chain.invoke({"question": query})#query instead of question in case of RetreivalQA
        
        st.subheader("Answer")
        st.write(result["answer"])#result instead of answer in case of RetreivalQA

        if src:
            with st.expander("📌 Sources Info"):
                for doc in result["source_documents"]:
                    source = doc.metadata.get("source", "Unknown Source")
                    page = doc.metadata.get("page", "Unknown Page")
                    #print(f"Source: {source}, Page: {page}")
                    st.write(f"Source: {source}, Page: {page}")
    
    else:
        st.markdown(f'Kinfly enter your **question**')            