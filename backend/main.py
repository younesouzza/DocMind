from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import init_db
from api import upload, query

app = FastAPI(title="DocMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()
    print("Database initialized")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "DocMind"}

app.include_router(upload.router, prefix="/api")
app.include_router(query.router, prefix="/api")