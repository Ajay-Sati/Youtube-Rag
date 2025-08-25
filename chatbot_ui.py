import streamlit as st
import time


def stream_message(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.2)
    
    
# enter the messages to session
if "messages" not in st.session_state:
    st.session_state.messages = []

# title of the page
st.title("Welcome to my Chatbot")

# add sub header
st.subheader("Ask me anything!. I repeat what you say")

# add the new chat button in sidebar
with st.sidebar:
    new_chat = st.button("New Chat")
    
if new_chat:
    st.session_state.messages = []
    
# add the chat input at bottom
prompt = st.chat_input("Enter your message")

# print all the messages in session
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant"):
            st.write(message["content"])
            
# add the prompt to message history
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    # show the user message
    with st.chat_message("user"):
        st.write(prompt)

# ai message
    st.session_state.messages.append({"role": "assistant", "content": prompt})
    # show the ai message
    with st.chat_message("assistant"):
        st.write_stream(stream_message(prompt))
    