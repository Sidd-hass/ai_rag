from langchain_community.vectorstores import FAISS
import os

VECTOR_PATH = "vector_db"


def get_vector_store(chunks, embeddings):

    if os.path.exists(VECTOR_PATH):

        vector_store = FAISS.load_local(
            VECTOR_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        # 🔥 ADD new documents instead of replacing
        vector_store.add_documents(chunks)

    else:
        vector_store = FAISS.from_documents(chunks, embeddings)

    # save after update
    vector_store.save_local(VECTOR_PATH)

    return vector_store


def load_vector_store(embeddings):

    if os.path.exists(VECTOR_PATH):
        return FAISS.load_local(
            VECTOR_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    return None