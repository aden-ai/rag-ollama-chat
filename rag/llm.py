import requests
from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
OLLAMA_BASE_URL = "http://localhost:11434"

def check_ollama_health():
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
        if response.status_code == 200:
            data = response.json()
            models = [m["name"] for m in data.get("models", [])]
            return True, "Ollama is running", models
        return False, f"Error: {response.status_code}", []
    except requests.exceptions.RequestException as e:
        return False, f"Ollama not running: {e}", []


def get_llm(model_name: str, temperature: float = 0.2):
    return OllamaLLM(model=model_name, temperature=temperature)
