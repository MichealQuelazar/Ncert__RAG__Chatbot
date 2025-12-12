# 📚 NCERT Q&A Web Application

> A production-ready, full-stack web application for AI-powered question-answering based on NCERT Physics Class 12 textbooks using RAG (Retrieval-Augmented Generation).

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-red.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Overview

This application transforms NCERT textbooks into an intelligent Q&A system. Ask questions in natural language and get accurate answers with source citations.

## 🏗️ Architecture

- **Backend**: FastAPI (REST API)
- **Frontend**: Flask (Web Interface)
- **Vector Database**: ChromaDB
- **LLM**: Groq (Llama3)
- **Embeddings**: Ollama (nomic-embed-text)

## Project Structure

```
├── backend/
│   ├── api/
│   │   ├── models.py          # Pydantic models
│   │   └── routes.py          # API endpoints
│   ├── services/
│   │   ├── vector_db_service.py   # Vector DB operations
│   │   └── qa_service.py          # Q&A logic
│   ├── config/
│   │   └── settings.py        # Configuration
│   └── main.py                # FastAPI app
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css      # Styles
│   │   └── js/
│   │       └── app.js         # Frontend logic
│   ├── templates/
│   │   └── index.html         # Main page
│   └── app.py                 # Flask app
├── utils/
│   └── vector_db_maker.py     # Vector DB creation
└── requirements.txt
```

## Prerequisites

1. **Python 3.8+**
2. **Ollama** - Install from [ollama.ai](https://ollama.ai)
3. **Groq API Key** - Get from [console.groq.com](https://console.groq.com)

## Installation

1. Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Ollama and pull the embedding model:
```bash
ollama pull nomic-embed-text
```

3. Create `.env` file from example:
```bash
cp .env.example .env
```

4. Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_actual_api_key_here
```

## Setup Vector Database

Before running the application, create the vector database from PDFs:

```bash
python utils/vector_db_maker.py
```

This will process the NCERT PDF files and create a vector database in the `vector_db` directory.

## Running the Application

### Option 1: Run Both Servers Separately

**Terminal 1 - Start Backend (FastAPI):**
```bash
python backend/main.py
```
Backend will run on http://localhost:8000

**Terminal 2 - Start Frontend (Flask):**
```bash
python frontend/app.py
```
Frontend will run on http://localhost:5000

### Option 2: Using Uvicorn and Flask CLI

**Backend:**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
flask --app frontend/app run --host 0.0.0.0 --port 5000
```

## Usage

1. Open your browser and navigate to http://localhost:5000
2. Enter your question in the text box
3. Click "Ask Question"
4. View the answer and retrieved source documents

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints

**POST /api/v1/ask**
```json
{
  "question": "What is Newton's first law?"
}
```

Response:
```json
{
  "answer": "...",
  "retrieved_documents": [
    {
      "page": "42",
      "link": "NCERT-Class-12-Physics-Part-1.pdf",
      "snippet": "..."
    }
  ]
}
```

**GET /api/v1/health**
```json
{
  "status": "healthy",
  "message": "Service is running",
  "vector_db_loaded": true
}
```

## Configuration

Edit `backend/config/settings.py` or use environment variables to configure:

- `GROQ_API_KEY`: Your Groq API key
- `VECTOR_DB_PATH`: Path to vector database
- `EMBEDDING_MODEL`: Ollama embedding model
- `LLM_MODEL`: Groq LLM model
- `RETRIEVAL_K`: Number of documents to retrieve
- `CHUNK_SIZE`: Text chunk size for processing
- `CHUNK_OVERLAP`: Overlap between chunks

## Features

- ✅ Modular architecture with separation of concerns
- ✅ RESTful API with FastAPI
- ✅ Modern web interface with Flask
- ✅ RAG-based question answering
- ✅ Document retrieval with re-ranking
- ✅ Source document display
- ✅ Health check endpoints
- ✅ Error handling
- ✅ Responsive design
- ✅ Example questions
- ✅ Status indicator

## Troubleshooting

**Vector database not found:**
- Run `python utils/vector_db_maker.py` to create it

**Ollama connection error:**
- Make sure Ollama is running: `ollama serve`
- Check if model is installed: `ollama list`

**Backend connection error:**
- Ensure backend is running on port 8000
- Check BACKEND_URL in frontend configuration

## License

MIT
