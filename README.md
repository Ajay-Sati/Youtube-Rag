# Youtube-Rag

📺 YouTube RAG – Chat with Any Video

A Retrieval-Augmented Generation (RAG) application that lets you chat with any YouTube video, generate summaries, and create notes — simply by pasting a YouTube URL.

The app extracts the video ID, fetches the transcript, builds a video-specific vector database, and enables AI-powered Q&A over the video content.

🚀 Features

Paste YouTube URL → Auto extract Video ID

Fetches transcript & creates a vector database automatically

Chat with the video (RAG-based Q&A)

Generate smart summaries

Generate topic-wise notes

Fast, accurate retrieval

Supports long videos

🧠 How It Works

User pastes a YouTube link

System extracts the video ID

Transcript is fetched using YouTube APIs

Transcript is cleaned, chunked, and converted into embeddings

A vector database is created for that specific video ID

User can now:

Ask questions

Request summaries

Generate notes

The AI model answers using RAG (retrieval + generation)

🛠️ Tech Stack

Python

LLMs / GenAI Models (e.g., Gemini, Llama, Mistral)

Vector Database (ChromaDB / FAISS / Pinecone)

YouTube Transcript API

Streamlit / FastAPI UI
