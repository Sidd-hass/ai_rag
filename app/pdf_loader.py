# from langchain_community.document_loaders import PyPDFLoader


# def load_pdf(file_path):
#     loader = PyPDFLoader(file_path)
#     documents = loader.load()
#     return documents

from langchain_community.document_loaders import PyPDFLoader

def load_pdf(path):

    loader = PyPDFLoader(path)
    docs = loader.load()

    # attach filename metadata
    for doc in docs:
        doc.metadata["source"] = path

    return docs