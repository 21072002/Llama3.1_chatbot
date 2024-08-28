import os
import json
import streamlit as st
from groq import Groq

#streamlit page config
st.set_page_config(
    page_title="Groq Streamlit",
    page_icon="🦙",
    layout="centered",
    
)

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

#initialize chat history as streamlit session state if not present
if "chat_history" not in st.session_state:
  st.session_state.chat_history = []

#streamlit page title
st.title("Llama 3.1 chatbot 🦙")

#display chat history 
for messege in st.session_state.chat_history:
    with st.chat_message(messege["role"]):
        st.markdown(messege["content"])

#input field for user message
user_prompt = st.chat_input("Ask LLama...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role":"user", "content": user_prompt})
    
    #send user message to LLM get a responce
    messages = [
        {"role": "system", "content": "you are a helpful assistant"},
        *st.session_state.chat_history
    ]

    responce = client.chat.completions.create(
        model= "llama-3.1-8b-instant",
        messages= messages
    )

    assistant_responce = responce.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_responce})


    #display the responce
    with st.chat_message("assistant"):
        st.markdown(assistant_responce)

