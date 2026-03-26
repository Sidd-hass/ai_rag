# from fastapi import FastAPI, UploadFile, File

# from app.pdf_loader import load_pdf
# from app.embeddings import get_embeddings
# from app.vector_store import get_vector_store, load_vector_store
# from app.rag_pipeline import split_docs
# from app.llm import load_llm
# from typing import List


# app = FastAPI()

# # Global objects
# vector_store = None
# llm = load_llm()


# @app.get("/")
# def health():
#     return {"status": "running"}



# @app.post("/upload")
# async def upload_pdf(files: List[UploadFile] = File(...)):

#     uploaded_files = []

#     for file in files:
#         path = f"uploads/{file.filename}"

#         # save file
#         with open(path, "wb") as f:
#             f.write(await file.read())

#         # load + process
#         docs = load_pdf(path)
#         chunks = split_docs(docs)

#         # append to vector DB
#         get_vector_store(chunks, embeddings)

#         uploaded_files.append(file.filename)

#     return {"message": f"Uploaded files: {uploaded_files}"}

# @app.post("/ask")
# def ask(question: str):

#     vector_store = load_vector_store(embeddings)

#     docs = vector_store.similarity_search(question, k=3)

#     context = "\n".join([d.page_content for d in docs])

#     sources = list(set([d.metadata.get("source") for d in docs]))

#     prompt = f"""
#     You are a helpful AI assistant.

#     Use the context to answer the question.

#     Context:
#     {context}

#     Question:
#     {question}
#     """

#     answer = llm.invoke(prompt)

#     return {
#         "answer": answer,
#         "sources": sources
#     }





from fastapi import FastAPI, UploadFile, File
from typing import List
import os

from app.pdf_loader import load_pdf
from app.embeddings import get_embeddings
from app.vector_store import get_vector_store, load_vector_store
from app.rag_pipeline import split_docs
from app.llm import load_llm

app = FastAPI()

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
    files: list[UploadFile] = File(..., description="Upload multiple PDF files")
):
    uploaded_files = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Read file once
        content = await file.read()

        # Save file
        with open(file_path, "wb") as f:
            f.write(content)

        # Load + process
        docs = load_pdf(file_path)
        chunks = split_docs(docs)

        # Store in vector DB
        get_vector_store(chunks, embeddings)

        uploaded_files.append(file.filename)

    return {
        "message": "Files uploaded successfully",
        "files": uploaded_files
    }


@app.post("/ask")
def ask(question: str):

    vector_store = load_vector_store(embeddings)

    docs = vector_store.similarity_search(question, k=3)

    context = "\n".join([d.page_content for d in docs])

    sources = list(set([d.metadata.get("source") for d in docs]))

    prompt = f"""
You are a helpful AI assistant.

Use the context to answer the question.

Context:
{context}

Question:
{question}
"""

    answer = llm.invoke(prompt)

    return {
        "answer": answer,
        "sources": sources
    }