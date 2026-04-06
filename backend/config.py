import os 
from dotenv import load_dotenv


class Settings :
    ollama_base_url : str = "http://localhost:11434"
    LLM_MODEL : str = "llama3.2"
    EMBEDDING_MODEL : str = "all-MiniLM-L6-v2"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/docmind.db")
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./data/chroma")



    CHUNK_SIZE: int =500
    CHUNK_OVERLAP: int = 50
    TOP_K_RESULTS: int = 3

settings = Settings()