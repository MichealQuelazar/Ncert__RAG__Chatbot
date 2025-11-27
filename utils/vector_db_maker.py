"""
Utility script for creating and updating vector database from PDF documents
"""
import os
import sys
import pdfplumber
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.config.settings import settings

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF page by page"""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                yield page_num, text

def process_pdf(pdf_path, chunk_size=None, chunk_overlap=None):
    """Process a single PDF into document chunks"""
    chunk_size = chunk_size or settings.CHUNK_SIZE
    chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    documents = []
    for page_num, page_text in extract_text_from_pdf(pdf_path):
        chunks = text_splitter.split_text(page_text)
        for chunk in chunks:
            doc = Document(
                page_content=chunk,
                metadata={
                    "source": pdf_path,
                    "page": page_num
                }
            )
            documents.append(doc)
    
    print(f"✓ Created {len(documents)} chunks from {pdf_path}")
    return documents

def process_multiple_pdfs(pdf_paths):
    """Process multiple PDFs into document chunks"""
    all_documents = []
    for pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            print(f"✗ Warning: {pdf_path} not found, skipping...")
            continue
        documents = process_pdf(pdf_path)
        all_documents.extend(documents)
    return all_documents

def process_and_store(pdf_paths, vector_db_path=None):
    """Process PDFs and store in vector database"""
    vector_db_path = vector_db_path or settings.VECTOR_DB_PATH
    
    print(f"\n{'='*60}")
    print("Vector Database Creation")
    print(f"{'='*60}\n")
    
    embeddings = OllamaEmbeddings(
        model=settings.EMBEDDING_MODEL,
        show_progress=True
    )
    
    print("Processing PDFs...")
    all_documents = process_multiple_pdfs(pdf_paths)
    
    if not all_documents:
        print("✗ No documents to process!")
        return
    
    print(f"\nTotal documents: {len(all_documents)}")
    
    # Check if the vector database already exists
    if os.path.exists(vector_db_path):
        print(f"\n✓ Existing vector database found at {vector_db_path}")
        print("Updating with new documents...")
        vector_db = Chroma(
            persist_directory=vector_db_path,
            embedding_function=embeddings
        )
        vector_db.add_documents(all_documents)
    else:
        print(f"\nCreating new vector database at {vector_db_path}...")
        vector_db = Chroma.from_documents(
            documents=all_documents,
            embedding=embeddings,
            persist_directory=vector_db_path
        )
    
    vector_db.persist()
    print(f"\n{'='*60}")
    print(f"✓ Successfully processed {len(pdf_paths)} PDFs")
    print(f"✓ Vector database saved to: {vector_db_path}")
    print(f"{'='*60}\n")

def main():
    """Main function to run the vector database creation"""
    # List of PDF files to process
    pdf_paths = [
        "NCERT-Class-12-Physics-Part-1.pdf",
        "NCERT-Class-12-Physics-Part-2.pdf"
    ]
    
    # Optional: custom vector database path
    vector_db_path = "vector_db"
    
    process_and_store(pdf_paths, vector_db_path)

if __name__ == "__main__":
    main()
