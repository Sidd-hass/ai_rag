import os
from langchain_ollama import OllamaLLM

def load_llm():

    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    llm = OllamaLLM(
        model="mistral",
        base_url=base_url
    )

    return llm