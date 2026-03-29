from fastapi import FastAPI, UploadFile, File
from typing import List
import os

from app.pdf_loader import load_pdf
from app.embeddings import get_embeddings
from app.vector_store import get_vector_store, load_vector_store
from app.rag_pipeline import split_docs
from app.llm import load_llm
from fastapi import Body
from fastapi.responses import StreamingResponse
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
import json

app = FastAPI()
chat_histories = {}  # Store chat histories by session_id

# Ensure upload directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Global objects
llm = load_llm()
embeddings = get_embeddings()   # ✅ FIXED (was missing)


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/upload")
async def upload_pdf(
    # 'files' must match the key name in your Postman/cURL request
    files: List[UploadFile] = File(..., description="Upload multiple PDF files")
):
    uploaded_filenames = []
    all_chunks = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save the file to disk
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # 1. Load the PDF
        docs = load_pdf(file_path)
        
        # 2. Split into chunks
        chunks = split_docs(docs)
        
        # Collect all chunks into one list
        all_chunks.extend(chunks)
        uploaded_filenames.append(file.filename)

    # 3. Update Vector Store ONCE after all files are processed
    if all_chunks:
        get_vector_store(all_chunks, embeddings)

    return {
        "message": f"Successfully processed {len(uploaded_filenames)} files",
        "files": uploaded_filenames
    }


@app.post("/ask")
async def ask(
    question: str = Body(..., embed=True), 
    session_id: str = Body("default_session", embed=True)
):
    # 1. Handle Chat History (Point 6)
    if session_id not in chat_histories:
        chat_histories[session_id] = ChatMessageHistory()
    
    history = chat_histories[session_id]
    
    # 2. Vector Search
    vector_store = load_vector_store(embeddings)
    docs = vector_store.similarity_search(question, k=3)
    context = "\n".join([d.page_content for d in docs])
    sources = list(set([d.metadata.get("source") for d in docs]))

    # 3. Format History for the Prompt
    history_str = ""
    for msg in history.messages[-6:]:  # Last 6 turns
        role = "User" if isinstance(msg, HumanMessage) else "Assistant"
        history_str += f"{role}: {msg.content}\n"

    # 4. Improved Prompt (Point 7)
    prompt = f"""
You are a professional AI Assistant. Use the context and chat history to answer.
If the answer isn't in the context, say you don't know.

---
CHAT HISTORY:
{history_str}

---
CONTEXT:
{context}

---
QUESTION: {question}
ANSWER:"""

    # 5. Streaming Generator (Point 8)
    async def stream_generator():
        full_response = ""
        # .stream() comes from your updated OllamaLLM in llm.py
        for chunk in llm.stream(prompt):
            full_response += chunk
            yield chunk  # Send token to client
        
        # After stream finishes, save the full exchange to memory
        history.add_user_message(question)
        history.add_ai_message(full_response)

    return StreamingResponse(stream_generator(), media_type="text/plain")