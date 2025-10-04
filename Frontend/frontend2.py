import streamlit as st
import requests

st.set_page_config(page_title='RAG application')
st.title("📘 Motors Co. Chatbot")

# API_URL1 = "http://127.0.0.1:8000/set_key"
# API_URL2 = "http://127.0.0.1:8000/chat"
# following lines used when using docker, otherwise above lines are ok 

API_URL1 = "http://backend:8000/set_key"
API_URL2 = "http://backend:8000/chat"

query = st.text_area("Ask me about Electronics and Motors Company insights:")
src = st.checkbox('Give Sources')

with st.sidebar:
    st.header('Choose between OpenAI, Groq, or Llama.')
    st.write('API Keys are required for OpenAI and Groq but not for Llama')

    Models = ['OpenAI', 'Groq', 'Llama']
    selection = st.selectbox('Select:', Models)

    user_api_key = ""
    if selection in ['OpenAI', 'Groq']:
        user_api_key = st.text_area('Enter API key :', height=69, placeholder='Ch4I82jw9bt70ri')

    if st.button("Save API Key"):
        if user_api_key.strip():
            try:
                api_stat = requests.post(API_URL1, json={"api_key": user_api_key})
                if api_stat.status_code == 200:
                    st.success(api_stat.json()["api_status"])
                else:
                    st.error(f"Failed to save key: {api_stat.json().get('detail', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Could not connect to backend: {e}")
        else:
            st.warning("❌ Please enter your API key ")

# ---- Main Chat Section ----
if st.button('Ask Bot'):
    if query.strip():
        try:
            response = requests.post(API_URL2, json={"question": query, "source": src})

            if response.status_code == 200:
                st.subheader("Answer")
                st.write(response.json()["answer"])

                if src:
                    with st.expander("📌 Sources Info"):
                        sorc = response.json()["sources"]
                        for s in sorc:
                            st.write(f'Source: {s["source"]}, Page: {s["page"]}')

            elif response.status_code == 401:
                st.warning("❌ Invalid API key, please try again.")

            elif response.status_code == 502:
                st.error("⚠️ Cannot reach Groq servers right now.")

            else:
                st.error(f"Error from backend: {response.json().get('detail', 'Unknown')}")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Could not connect to backend: {e}")

    else:
        st.write('Kindly enter your question')
