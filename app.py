
import streamlit as st
from streamlit import spinner
from streamlit.web.server.server import server_port_is_manually_set
import time

from supporting_functions import (
     extract_video_id,
     get_transcript,
     translate_transcript,
     generate_notes,
     get_important_topics,
     create_chunks,
     create_vector_store,
     rag_answer
)


# --- Sidebar (Inputs) ---
with st.sidebar:
    st.title("🎬 VidSynth AI")
    st.markdown("---")
    st.markdown("Transform any YouTube video into key topics, a podcast, or a chatbot.")
    st.markdown("### Input Details")

    youtube_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    language = st.text_input("Video Language Code", placeholder="e.g., en, hi, es, fr", value="en")

    task_option = st.radio(
        "Choose what you want to generate:",
        ["Chat with Video", "Notes For You"]
    )

    submit_button = st.button("✨ Start Processing")
    st.markdown("---")
    # The "New Chat" button has been removed from here.

# --- Main Page ---
st.title("YouTube Content Synthesizer")
st.markdown("Paste a video link and select a task from the sidebar.")




# --- Processing Flow ---
if submit_button:
    if youtube_url and language:
        video_id= extract_video_id(youtube_url)
        if video_id:
            with spinner("Step 1/3 : Fetching Transcript....."):
                full_transcript= get_transcript(video_id, language)

                if language!="en":
                    with spinner("Step 1.5/3 : Translating Transcript into English, This may take few moments......"):
                        full_transcript= translate_transcript(full_transcript)


            if task_option=="Notes For You":
                with spinner("Step 2/3: Extracting important Topics..."):
                    import_topics= get_important_topics(full_transcript)
                    st.subheader("Important Topics")
                    st.write(import_topics)
                    st.markdown("---")

                with spinner("Step 3/3 : Generating Notes for you."):
                    notes= generate_notes(full_transcript)
                    st.subheader("Notes for you")
                    st.write(notes)

                st.success("Summary and Notes Generated.")

            if task_option == "Chat with Video":
                with st.spinner("Step 2/3: Creating chunks and vector store...."):
                    chunks = create_chunks(full_transcript)
                    vectorstore = create_vector_store(chunks)
                    st.session_state.vector_store = vectorstore
                    with open(r"c:\Users\acer\Desktop\Youtube rag Live Class\.cursor\debug.log", "a") as f:
                        f.write(f'{{"id":"log_app_vectorstore_created","timestamp":{{"$date":{int(time.time() * 1000)}}},"location":"app.py:74","message":"Vector store created","data":{{"vectorstore_exists": "vectorstore" in st.session_state}},"sessionId":"debug-session","runId":"run1","hypothesisId":"D"}}\n')
                st.session_state.messages=[]
                st.success('Video is ready for chat.....')


# chatbot session
if task_option=="Chat with Video" and "vector_store" in st.session_state:
    st.divider()
    st.subheader("Chat with Video")

    # Display the entire history
    for message in st.session_state.get('messages',[]):
        with st.chat_message(message['role']):
            st.write(message['content'])

    # user_input
    prompt= st.chat_input("Ask me anything about the video.")
    if prompt:
        st.session_state.messages.append({'role':'user','content':prompt})
        with st.chat_message('user'):
            st.write(prompt)

        with st.chat_message('assistant'):
           with open(r"c:\Users\acer\Desktop\Youtube rag Live Class\.cursor\debug.log", "a") as f:
               f.write(f'{{"id":"log_app_rag_answer_call","timestamp":{{"$date":{int(time.time() * 1000)}}},"location":"app.py:97","message":"Calling rag_answer","data":{{"prompt":prompt, "vectorstore_exists": "vector_store" in st.session_state}},"sessionId":"debug-session","runId":"run1","hypothesisId":"D"}}\n')
           response= rag_answer(prompt,st.session_state.vector_store)
           st.write(response)
           with open(r"c:\Users\acer\Desktop\Youtube rag Live Class\.cursor\debug.log", "a") as f:
               f.write(f'{{"id":"log_app_rag_answer_response","timestamp":{{"$date":{int(time.time() * 1000)}}},"location":"app.py:98","message":"rag_answer response","data":{{"response_length":len(response)}},"sessionId":"debug-session","runId":"run1","hypothesisId":"C"}}\n')
        st.session_state.messages.append({'role': 'assistant', 'content':response})