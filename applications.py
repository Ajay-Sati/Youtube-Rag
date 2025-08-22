import re
import os
import time
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import wave
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()


api_key= os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise  ValueError("API key  not found")

client= genai.Client(api_key=api_key)

# Function to extract video ID from a YouTube URL (Helper Function)
def extract_video_id(url):
    """
    Extracts the YouTube video ID from any valid YouTube URL.
    """
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if match:
        return match.group(1)
    match_shorts = re.search(r"shorts\/([0-9A-Za-z_-]{11})", url)
    if match_shorts:
        return match_shorts.group(1)
    st.error("Invalid YouTube URL. Please enter a valid video link.")
    return None


# Function to get transcript from YouTube using your exact proxy code
def get_transcript(video_id, language):
    """
    Fetches the transcript for a given video ID and language using the specified proxy.
    This function uses the exact proxy implementation as requested.
    """
    ytt_api = YouTubeTranscriptApi(
        proxy_config=WebshareProxyConfig(
            proxy_username="mqmgcmwa",
            proxy_password="sxo9voiyqrhj",
        )
    )
    try:
        transcript = ytt_api.fetch(video_id, languages=language)
        time.sleep(5)
        return transcript
    except Exception as e:
        print(f"Error fetching {video_id}: {e}")


# Function to translate transcript to English using the prompt from your notebook
def translate_transcript(transcript):
    """
    Translates the transcript to English using the Gemini API.
    """
    if not transcript:
        return None
    try:
        prompt = f"""you are an expert translator with deep cultural and linguistic knowledge.
        I will provide you with a transcript. Your task is to translate it into english with absolute accuracy, preserving:
        - Full meaning and context (no omissions, no additions).
        - Tone and style (formal/informal, emotional/neutral as in original).
        - Nuances, idioms, and cultural expressions (adapt appropriately while keeping intent).
        - Speaker’s voice (same perspective, no rewriting into third-person).
        Do not summarize or simplify. The translation should read naturally in the target language but stay as close as possible to the original intent.
        Here is the transcript to translate:{transcript}"""
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt
        )
        return response.text
    except Exception as e:
        st.error(f"Translation failed: {e}")
        return None


# Function to get important topics using the prompt from your notebook
def get_important_topics(transcript):
    """
    Extracts important topics from the transcript.
    """
    if not transcript:
        return None
    try:
        prompt = f"Based on the following transcript, identify and list the most important topics discussed:\n\n{transcript}"
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt)

        return response.text
    except Exception as e:
        st.error(f"Failed to extract topics: {e}")
        return None


# Function to generate a podcast script using the prompt from your notebook
def generate_podcast_script(transcript):
    """
    Generates a two-person podcast script from the transcript.
    """
    if not transcript:
        return None
    try:
        prompt = f"""
        You are a podcast scriptwriter. Your task is to convert the following YouTube video transcript into an engaging podcast summary.
        The podcast will feature two people:
        1.  **Anchor:** The host who asks questions and guides the conversation.
        2.  **Expert:** The person who provides the information based on the transcript.
        The script should summarize the key points of the video in a natural, conversational dialogue. The Expert's answers must be derived solely from the information in the transcript provided below.
        Format the output clearly with speaker labels (e.g., "Anchor:" and "Expert:").
        Here is the transcript:
        {transcript}
        """
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt)
        return response.text
    except Exception as e:
        st.error(f"Failed to generate podcast script: {e}")
        return None



# Function to create text chunks for vector store
def create_chunks(transcript):
    """
    Splits the transcript into smaller chunks.
    """
    if not transcript:
        return None
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    docs = text_splitter.create_documents([transcript])
    return docs


# Function to create and return a vector store
def create_vector_store(docs):
    """
    Creates a Chroma vector store from the given text chunks.
    """
    if not docs:
        return None
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = Chroma.from_documents(docs, embeddings)
        return vector_store
    except Exception as e:
        st.error(f"Failed to create vector store: {e}")
        return None
