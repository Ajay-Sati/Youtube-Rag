import streamlit as st

from supporting_functions import (
    extract_video_id,
    get_transcript,
    translate_transcript,
    generate_notes,
    create_chunks,
    create_vector_store,
    get_important_topics,
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
        video_id = extract_video_id(youtube_url)
        if video_id:
            with st.spinner("Step 1/3: Fetching transcript... 📜"):
                full_transcript = get_transcript(video_id, language)

                if language != "en":
                    with st.spinner("Step 1.5/3: Translating into English... 🌎"):
                        full_transcript = translate_transcript(full_transcript)

            # Save transcript for both tasks
            st.session_state.full_transcript = full_transcript

            # --- If Chat Option ---
            if task_option == "Chat with Video":
                with st.spinner("Step 2/3: Creating chunks and vector store... 📚"):
                    chunks = create_chunks(full_transcript)
                    vectorstore = create_vector_store(chunks)
                    st.session_state.vectorstore = vectorstore

                # Initialize a new chat session for the processed video
                st.session_state.messages = []
                st.success("✅ Video ready for chat! Scroll down to start chatting.")

            # --- If Summary + Podcast Option ---
            elif task_option == "Notes For You":
                with st.spinner("Step 2/3: Extracting Important Topics..."):
                    imp_topics = get_important_topics(full_transcript)
                    st.subheader("📌 Important Topics")
                    st.write(imp_topics)

                with st.spinner("Step 3/3: Notes For you ️"):
                    script= generate_notes(full_transcript)
                    st.write(script)

                st.success("✅ Summary and Notes Generated!")

# --- Chatbot Section ---
if task_option == "Chat with Video" and "vectorstore" in st.session_state:
    st.divider()
    st.subheader("💬 Chat with the Video")

    # Display chat history. Using .get() ensures it works on the first run
    for message in st.session_state.get("messages", []):
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    prompt = st.chat_input("Ask me anything about the video...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            response = rag_answer(prompt, st.session_state.vectorstore)
            st.write(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
