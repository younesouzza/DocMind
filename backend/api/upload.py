# backend/api/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Document, get_db
from rag import rag_engine  
import shutil
import os
from config import settings

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Save File
    os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_FOLDER, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save file")

    db_doc = Document(filename=file.filename, file_path=file_path)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    try:
        chunk_count = rag_engine.ingest_file(file_path, file.filename, db_doc.id)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"RAG Ingestion failed: {str(e)}")

    return {
        "message": "Document processed successfully",
        "filename": file.filename,
        "chunks_created": chunk_count,
        "doc_id": db_doc.id
    }