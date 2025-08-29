import re

import time
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_chroma import Chroma
from google import genai

import os
from dotenv import load_dotenv


import requests
from io import BytesIO

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
    st.error("Invalid YouTube URL. Please enter a valid video link.")
    return None

# function to get summary transcript from the video.
def get_transcript(video_id, language):
    ytt_api = YouTubeTranscriptApi(
    proxy_config=WebshareProxyConfig(
        proxy_username="uovoumor",
        proxy_password="udk28jufv40l",
    )
)

    try:
        transcript = ytt_api.fetch(video_id, languages=[language])
        full_transcript = " ".join([i.text for i in transcript])
        time.sleep(10)  # wait 5 seconds between requests
        return full_transcript
    except Exception as e:
        st.error(f"Error fetching {video_id}: {e}")


# Initialize Gemini model via LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.2
)

def translate_transcript(transcript: str) -> str:
    try:
        # Define translation prompt
        prompt = ChatPromptTemplate.from_template("""
        You are an expert translator with deep cultural and linguistic knowledge.
        I will provide you with a transcript. Your task is to translate it into English with absolute accuracy, preserving:
        - Full meaning and context (no omissions, no additions).
        - Tone and style (formal/informal, emotional/neutral as in original).
        - Nuances, idioms, and cultural expressions (adapt appropriately while keeping intent).
        - Speaker’s voice (same perspective, no rewriting into third-person).
        Do not summarize or simplify. The translation should read naturally in the target language but stay as close as possible to the original intent.

        Transcript:
        {transcript}
        """)

        # Create a runnable chain
        chain = prompt | llm

        # Run chain
        response = chain.invoke({"transcript": transcript})

        return response.content

    except Exception as e:
        st.error(f"Translation failed: {e}")







# Function to get important topics using the prompt from your notebook
def get_important_topics(transcript):
    try:
        prompt = ChatPromptTemplate.from_template("""
        You are an assistant that extracts the 5 most important topics discussed in a video transcript or summary.
        
        Rules:
        - Summarize into exactly 5 major points.
        - Each point should represent a key topic or concept, not small details.
        - Keep wording concise and focused on the technical content.
        - Do not phrase them as questions or opinions.
        - Output should be a numbered list.
        - show only points that are discussed in the transcript.
        Here is the transcript:
        {transcript}
        """)
        # creating chains
        chain = prompt | llm

        # Run chain
        response = chain.invoke({"transcript": transcript})

        return response.content

    except Exception as e:
        st.error(f"Failed to extract topics: {e}")




# Function to generate Notes using the prompt from your notebook
def generate_notes(transcript):
    """
    Generates a two-person podcast script from the transcript.
    """
    if not transcript:
        return None
    try:
        prompt = ChatPromptTemplate.from_template("""
        You are an AI note-taker. Your task is to read the following YouTube video transcript 
        and produce well-structured, concise notes.
        
        ⚡ Requirements:
        - Present the output as **bulleted points**, grouped into clear sections.
        - Highlight key takeaways, important facts, and examples.
        - Use **short, clear sentences** (no long paragraphs).
        - If the transcript includes multiple themes, organize them under **subheadings**.
        - Do not add information that is not present in the transcript.
        
        Here is the transcript:
        {transcript}
        """)
        # creating chains
        chain = prompt | llm

        # Run chain
        response = chain.invoke({"transcript": transcript})

        return response.content

    except Exception as e:
        st.error(f"Failed to extract topics: {e}")





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



#RAG FUNCTION.
def rag_answer(question, vectorstore):
    # Search in vector DB
    results = vectorstore.similarity_search(question, k=4)
    context_text = "\n".join([res.page_content for res in results])

    # Build RAG prompt
    prompt = ChatPromptTemplate.from_template("""
            You are a kind, polite, and precise assistant.
            - Begin with a warm and respectful greeting (avoid repeating greetings every turn).
            - Understand the user’s intent even with typos or grammatical mistakes.
            - Answer ONLY using the retrieved context.
            - If answer not in context, say:
              "I couldn’t find that information in the database. Could you please rephrase or ask something else?"
            - Keep answers clear, concise, and friendly.

            Context:
            {context}

            User Question:
            {question}

            Answer:
            """)

    # creating chains
    chain = prompt | llm

    # Run chain
    response = chain.invoke({"context": context_text, "question": question})
    return response.content




