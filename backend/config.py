import os 
from dotenv import load_dotenv


class Settings :
    ollama_base_url : str = "http://localhost:11434"
    LLM_MODEL : str = "llama3.2"
    EMBEDDING_MODEL : str = "all-MiniLM-L6-v2"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///" + os.path.join(os.path.dirname(__file__), "../data/docmind.db").replace("\\", "/"))
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", os.path.join(os.path.dirname(__file__), "../data/chroma"))


    CHUNK_SIZE: int =500
    CHUNK_OVERLAP: int = 50
    TOP_K_RESULTS: int = 3
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", os.path.join(os.path.dirname(__file__), "../data/uploads"))

settings = Settings()