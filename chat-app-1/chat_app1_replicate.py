"""
From https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
"""

import os, sys
import streamlit as st
from dotenv import load_dotenv, find_dotenv
import replicate

_ = load_dotenv(find_dotenv()) # read local .env file


REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")
MODEL = "meta/meta-llama-3-8b-instruct"


st.title("My Chatbot")



if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        for event in replicate.stream(
           MODEL,
            input={
                "prompt": prompt,
                "temperature": 0.5,
                "max_tokens": 1024,
                "top_p": 1,
                "stream": True,
            },
        ):
            # full_response += event["choices"][0]["delta"]["content"] or ""
            full_response += str(event) or ""
            message_placeholder.markdown(full_response + "▌")
        ##
            
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})