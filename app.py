import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time
from youtube_transcript_api import YouTubeTranscriptApi
from applications import (
    extract_video_id,
    get_transcript,
    translate_transcript,
    create_chunks,
    create_vector_store,
    generate_podcast_script,
    get_important_topics
)

# --- Page Configuration ---
st.set_page_config(
    page_title="VidSynth AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --- Sidebar ---
with st.sidebar:
    st.title("🎬 VidSynth AI")
    st.markdown("---")
    st.markdown("Transform any YouTube video into key topics, a podcast, and a searchable chatbot.")
    st.markdown("""
        **How to use:**
        1.  Paste a YouTube video URL.
        2.  Enter the video's language code (e.g., 'en' for English, 'hi' for Hindi).
        3.  Click 'Synthesize Content'.
        4.  Explore the generated content and chat with the video!
    """)
    st.markdown("---")
    st.info("Developed with Streamlit and Google Gemini.")


# --- Main Application ---
st.title("YouTube Content Synthesizer")
st.markdown("Enter a video URL and its language to get started.")

# --- Input Form ---
with st.form("input_form"):
    youtube_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    language = st.text_input("Video Language Code", placeholder="e.g., en, hi, es, fr", value="en")
    submit_button = st.form_submit_button(label="✨ Synthesize Content")


# --- Processing Logic ---
if submit_button:
    if youtube_url and language:
        video_id = extract_video_id(youtube_url)
        st.success(video_id)
        if video_id:
            with st.spinner("Step 1/5: Fetching transcript... 📜"):
                ytt_api = YouTubeTranscriptApi()
                try:
                    transcript = ytt_api.fetch(video_id, languages=[language])
                    print(transcript)
                    time.sleep(10)  # wait 5 seconds between requests
                except Exception as e:
                    print(f"Error fetching {video_id}: {e}")






