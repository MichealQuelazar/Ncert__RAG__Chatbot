"""
Question-Answering service for generating responses
"""
from typing import List, Dict
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from backend.services.vector_db_service import VectorDBService

class QAService:
    def __init__(self, vector_db_service: VectorDBService, groq_api_key: str, llm_model: str):
        self.vector_db_service = vector_db_service
        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model=llm_model
        )
        self.prompt_template = ChatPromptTemplate.from_template(
            """Answer the question based ONLY on the following context:
{context}

Question: {question}

Provide a clear and concise answer. If the context doesn't contain enough information to answer the question, say so."""
        )
    
    def generate_answer(self, question: str) -> Dict[str, any]:
        """Generate an answer for the given question"""
        if not self.vector_db_service.is_ready():
            raise ValueError("Vector database service is not ready")
        
        try:
            # Retrieve and re-rank documents
            retrieved_docs = self.vector_db_service.get_relevant_documents(question)
            
            # Collect document information
            doc_info = []
            for doc in retrieved_docs:
                page_number = doc.metadata.get('page', 'N/A')
                doc_link = doc.metadata.get('source', 'N/A')
                doc_info.append({
                    "page": str(page_number),
                    "link": doc_link,
                    "snippet": doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content
                })
            
            # Combine the content of the retrieved documents
            context = "\n\n".join([doc.page_content for doc in retrieved_docs])
            
            # Prepare the prompt with the retrieved context
            formatted_prompt = self.prompt_template.format(context=context, question=question)
            
            # Generate the response using Groq API
            response = self.llm.invoke(formatted_prompt)
            
            # Extract the content from the AIMessage
            answer = response.content if hasattr(response, 'content') else str(response)
            
            return {
                "answer": answer,
                "retrieved_documents": doc_info
            }
        except Exception as e:
            print(f"Error in generate_answer: {str(e)}")
            raise
