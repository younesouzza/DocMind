from .tools import AgentTools

class DocMindAgent:
    def __init__(self, rag_engine):
        self.rag_engine = rag_engine
        self.tools = AgentTools()
        
        self.FALLBACK_PHRASES = [
            "cannot find this information",
            "not in the context",
            "i don't have access",
            "no information available"
        ]
    
    def _should_fallback_to_web(self, answer: str) -> bool:
        """Check if LLM indicates it couldn't answer from docs"""
        answer_lower = answer.lower()
        return any(phrase in answer_lower for phrase in self.FALLBACK_PHRASES)
    
    def query(self, question: str) -> dict:
        """
        Agent decision flow:
        1. Try to answer from documents
        2. If docs fail or insufficient → Fallback to web search
        3. Return answer with source type
        """
        print(f"\n[Agent] Received question: {question}")
        
        # Search Documents
        doc_results = self.tools.search_documents(self.rag_engine, question)
        
        if doc_results:
            # Try to answer from docs
            context_text = "\n\n".join([r['content'] for r in doc_results])
            answer = self.rag_engine.generate_answer(question, context_text)
            
            # Check if answer is sufficient
            if not self._should_fallback_to_web(answer):
                print("[Agent] Answered from documents")
                return {
                    "answer": answer,
                    "source_type": "document",
                    "sources": [
                        {"source": r['metadata']['filename'], "snippet": r['content'][:150]}
                        for r in doc_results
                    ]
                }
            else:
                print("[Agent] Docs insufficient, falling back to web...")
        
        else:
            print("[Agent] No documents found, searching web...")
        
        # Fallback to Web Search
        web_context = self.tools.search_web(question)
        web_answer = self.rag_engine.generate_answer(question, web_context)
        
        print("[Agent] Answered from web search")
        return {
            "answer": web_answer,
            "source_type": "web",
            "sources": [{"source": "Web Search", "snippet": web_context[:200]}]
        }