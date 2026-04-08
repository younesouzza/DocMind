from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agent.agent import DocMindAgent  
from rag import rag_engine

router = APIRouter()


agent = DocMindAgent(rag_engine)

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def query_documents(request: QueryRequest):
    try:
        
        result = agent.query(request.question)
        
        return {
            "answer": result['answer'],
            "source_type": result['source_type'],  
            "sources": result['sources']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))