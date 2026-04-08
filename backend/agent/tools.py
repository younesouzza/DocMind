from langchain_community.tools import DuckDuckGoSearchRun

class AgentTools:
    def __init__(self):
        self.web_search = DuckDuckGoSearchRun()
    
    def search_web(self, query: str) -> str:
        """Searches the web for current information"""
        try:
            print(f" [Web Search] Query: {query}")
            result = self.web_search.run(query)
            print(f" [Web Search] Found {len(result)} characters")
            return result
        except Exception as e:
            print(f" [Web Search] Error: {str(e)}")
            return f"Web search failed: {str(e)}"
    
    def search_documents(self, rag_engine, query: str, k: int = 3) -> list:
        """Searches uploaded documents via RAG"""
        print(f"[Doc Search] Query: {query}")
        results = rag_engine.search(query, k=k)
        print(f"[Doc Search] Found {len(results)} chunks")
        return results