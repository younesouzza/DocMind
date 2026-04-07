# backend/api/query.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rag import rag_engine  

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def query_documents(request: QueryRequest):
    try:
        results = rag_engine.search(request.question, k=3)
        
        if not results:
            return {"answer": "No relevant documents found.", "sources": []}
        
        context_text = "\n\n".join([r['content'] for r in results])
        
        answer = rag_engine.generate_answer(request.question, context_text)
        
        sources = [
            {"filename": r['metadata']['filename'], "snippet": r['content'][:100]} 
            for r in results
        ]
        
        return {
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))