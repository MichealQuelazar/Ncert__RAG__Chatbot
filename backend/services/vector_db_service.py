"""
Vector database service for managing embeddings and retrieval
"""
import os
from typing import Optional
try:
    from langchain_ollama import OllamaEmbeddings
except ImportError:
    from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_groq import ChatGroq

class VectorDBService:
    def __init__(self, vector_db_path: str, embedding_model: str, groq_api_key: str, llm_model: str, retrieval_k: int = 5):
        self.vector_db_path = vector_db_path
        self.embedding_model = embedding_model
        self.groq_api_key = groq_api_key
        self.llm_model = llm_model
        self.retrieval_k = retrieval_k
        self.vector_db: Optional[Chroma] = None
        self.compression_retriever: Optional[ContextualCompressionRetriever] = None
        
    def load_vector_db(self) -> bool:
        """Load the vector database"""
        try:
            if not os.path.exists(self.vector_db_path):
                print(f"Warning: Vector database path '{self.vector_db_path}' does not exist")
                return False
                
            embeddings = OllamaEmbeddings(model=self.embedding_model)
            self.vector_db = Chroma(
                persist_directory=self.vector_db_path,
                embedding_function=embeddings
            )
            print(f"Vector database loaded successfully from {self.vector_db_path}")
            return True
        except Exception as e:
            print(f"Error loading vector database: {str(e)}")
            return False
    
    def setup_compression_retriever(self) -> bool:
        """Setup contextual compression retriever with re-ranking"""
        try:
            if self.vector_db is None:
                print("Vector database not loaded. Call load_vector_db() first.")
                return False
            
            llm = ChatGroq(
                groq_api_key=self.groq_api_key,
                model=self.llm_model
            )
            compressor = LLMChainExtractor.from_llm(llm)
            self.compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor,
                base_retriever=self.vector_db.as_retriever(search_kwargs={"k": self.retrieval_k})
            )
            print("Compression retriever setup successfully")
            return True
        except Exception as e:
            print(f"Error setting up compression retriever: {str(e)}")
            return False
    
    def get_relevant_documents(self, query: str):
        """Retrieve relevant documents for a query"""
        if self.compression_retriever is None:
            raise ValueError("Compression retriever not initialized")
        try:
            # Use invoke instead of deprecated get_relevant_documents
            return self.compression_retriever.invoke(query)
        except AttributeError:
            # Fallback for older versions
            return self.compression_retriever.get_relevant_documents(query)
    
    def is_ready(self) -> bool:
        """Check if the service is ready to handle queries"""
        return self.vector_db is not None and self.compression_retriever is not None
