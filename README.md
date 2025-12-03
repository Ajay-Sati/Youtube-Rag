# Youtube-Rag

### YouTube RAG – Chat with Any Video
This project is a Retrieval-Augmented Generation (RAG) application that allows users to interact with YouTube videos using AI. By simply pasting a YouTube link, the system extracts the video ID, fetches its transcript, creates a dedicated vector database, and enables users to chat with the video’s content. Along with conversational querying, the application also provides automatically generated summaries and detailed notes for easier understanding and revision.

#### Features
The application enables users to paste any YouTube link, from which it automatically extracts the video ID and prepares all required backend processing. Once the video content is indexed, users can ask questions directly related to the video, allowing the AI to generate context-aware responses based strictly on the transcript. In addition to conversational interaction, the system can produce concise summaries as well as organized notes derived from the video content, making it useful for study, research, or quick learning.

#### How It Works
When a user provides a YouTube URL, the system identifies and extracts the video ID from the link. It then fetches the full transcript of the video, cleans the text, breaks it into manageable chunks, and converts each chunk into vector embeddings. These embeddings are stored in a vector database that is uniquely created for that video. During interaction, user queries are converted into embeddings, matched semantically against the stored vectors, and then used as contextual input for the LLM. This creates a retrieval-augmented pipeline where answers, summaries, and notes are grounded in the original video content.

#### Tech Stack
The project is built using Python as the core programming language. Large Language Models (such as Gemini, Llama, Mistral, or any selected model) are used to generate responses and summaries. A vector database such as ChromaDB or FAISS stores semantic embeddings for retrieval. YouTube transcripts are obtained through the YouTube Transcript API. The user interface is designed using Streamlit or FastAPI, depending on the implementation.
