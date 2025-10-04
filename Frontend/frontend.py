# frontend.py
import streamlit as st
import requests
import os

st.set_page_config(page_title='RAG application')
st.title("📘 Motors Co. Chatbot")

#Two different endpoints
API_URL1="http://127.0.0.1:8000/set_key"
API_URL2="http://127.0.0.1:8000/chat"

query = st.text_input("Ask me about Electronics and Motors Company insights:")
src=st.checkbox('Give Sources')
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

    if st.button("Save API Key"):
        if user_api_key:
            api_stat=requests.post(API_URL1,json={"api_key" : user_api_key})
            if api_stat.status_code == 200:
                st.success(api_stat.json()["api_status"])
        elif user_api_key != "" :
            st.warning("❌ Please enter your API key ")

    # if st.button("Save API Key"): # We directly using text_input instead of text_area where w just click enter and text inside text_input is sent 
    #     if API_KEY:
    #         # save to .env file
    #         with open(".env", "w") as f:
    #             f.write(f"API_KEY={API_KEY}\n")
    #         st.success("✅ API Key saved to .env file!")
    #     else:
    #         st.warning("Please enter a valid API key.")    
    


if st.button("Ask Agent"):
    if query:
        if src: 
            response = requests.post(API_URL2, json={"question": query,"source" : src})
            if response.status_code == 200:
                st.subheader("Answer")
                st.write(response.json()["answer"])
                with st.expander("📌 Sources Info"):
                    sorc=response.json()["sources"]
                    for src in sorc:
                        st.write(f'Source: {src["source"]}, Page: {src["page"]}')
                    #st.write(f"Source: {sorc}, Page: {pg}")
    
            else:
                st.error("Error from backend!")
        else:
            response = requests.post(API_URL2, json={"question": query,"source" : src})
            if response.status_code == 200:
                st.subheader("Answer")
                st.write(response.json()["answer"])
            else:
                st.error("Error from backend!")
    

#now, this :
# sorc=response.json()["sources"]
# st.write(sorc)
#    it writes the list like:
# [
# 0:{
# "source":"Siemens_SIMOTICS_Motors_catalog_2018.pdf"
# "page":121
# }
# 1:{
# "source":"Siemens_SIMOTICS_Motors_catalog_2018.pdf"
# "page":8
# }
# 2:{
# "source":"Siemens_SIMOTICS_Motors_catalog_2018.pdf"
# "page":541
# }
# 3:{
# "source":"Siemens_SIMOTICS_Motors_catalog_2018.pdf"
# "page":529
# }
# ]

#streamlit run Frontend\frontend.py
