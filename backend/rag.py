import os 
import pymupdf
import docx
import pytesseract
from PIL import Image
from sentence_transformers import SentenceTransformer
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from .config import settings


class Rag_engine :
    def init(self):
        print("loading rag engine")


        self.spliter = RecursiveCharacterTextSplitter(chunk_size= settings.CHUNK_SIZE ,chunk_overla= settings.CHUNK_OVERLAP )

        self.embeder = SentenceTransformer(settings.EMBEDDING_MODEL)


        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)

        self.collection = self.client.get_or_create_collection(
            name="docmind_collection",
            metadata={"hnsw:space": "cosine"}
        )
        self.llm =ChatOllama(model= settings.LLM_MODEL , base_url= settings.ollama_base_url )

    def doc_loader(self, file_path: str , filename: str) -> str:

        ext = os.path.splitext(filename)[1]

        try:
            if ext == ".pdf" : 
                return self.load_pdf(file_path)
            elif ext == ".docx":
                return self.load_docx(file_path)
            elif ext == ".txt":
                return self.load_txt(file_path)
            elif ext in [".png", ".jpg", ".jpeg" ] :
                return self.load_image(file_path)
            else:
                raise ValueError(f"unseported file type: {ext}")
            
        except Exception as e:
            raise Exception(f"failes to load {filename}")

    
    def load_pdf(self, file_path: str)->str :
        text = ""

        doc = pymupdf.open(file_path)
        for pages in doc :
            text += pages.get_text()
        doc.close()
        return text
    
    def load_docx(self , file_path: str)->str :
        text = ""
        doc = docx.Document(file_path)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return '\n'.join(text)
    

    
    def load_txt(self, filepath: str)->str:

        with open(filepath , 'r') as file:
            text = file.read()

        return text
    
    def load_image(self, filepath: str)->str:
        try:
            text = pytesseract.image_to_string(Image.open(filepath))
            return text
        except Exception as e:
            return print(f"error extracting text from image {e}")
        
    def ingest_file(self , file_path: str, file_name: str, doc_id: int)->int:

        text = self.doc_loader(file_path, file_name)

        if not text or len(text.strip())==0:
            return 0
        
        chunks = self.spliter.split_text(text)

        for i, chunk in enumerate[chunks]:
            embedding = self.embeder.encode(chunk).tolist()
            chroma_id = f"{doc_id}{i}"

            self.collection.add(
                id = chroma_id,
                embeddings = [embedding],
                documents= [chunk],
                metadatas= [{"doc_id" : doc_id , "filename": file_name}]
            )

        return len(chunks)
    
    def search(self , query : str , k : int =3 )->list:

        query_embedding = self.embeder.encode(query).tolist()

        results = self.collection.query(
            query_embeddings= [query_embedding],
            n_results= [k]
        )


        #output format

        return[
            {"content" : doc , "metadata": meta}
            for doc, meta in zip(results['documents'][0], results['metadatas'][0])

        ]
    
    def generate_answer(self, query : str, context : str) ->str:

        template = """ you are a helpfull research assistant. Answer based only on the context bellow .
        if the answer is not in the context , "i cannot find this information in the documents."

        Context : {context}
        Question : {question}

        Answer : 
        """

        promt = ChatPromptTemplate.from_template(template)
        chain = promt|self.llm
        response = chain.invoke({"context": context , "question" : query })
        return response.content
    

rag_engine = Rag_engine()







        



        

        


        






    