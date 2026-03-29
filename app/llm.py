import os
from langchain_ollama import OllamaLLM

def load_llm():
    """
    Initializes the Ollama LLM with streaming capabilities.
    """
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    llm = OllamaLLM(
        model="mistral",
        base_url=base_url,
        # Point 8: Enable streaming
        streaming=True, 
        # Optional: Adjust temperature for more creative (0.7) or factual (0.1) answers
        temperature=0.1 
    )

    return llm