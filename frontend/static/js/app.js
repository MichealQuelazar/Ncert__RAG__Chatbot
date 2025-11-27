const BACKEND_URL = '/';

// Check backend status on page load
window.addEventListener('DOMContentLoaded', checkBackendStatus);

async function checkBackendStatus() {
    const statusDot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');
    
    try {
        const response = await fetch(`${BACKEND_URL}health`);
        const data = await response.json();
        
        if (data.status === 'healthy' && data.vector_db_loaded) {
            statusDot.classList.add('online');
            statusText.textContent = 'System Ready';
        } else {
            statusDot.classList.add('offline');
            statusText.textContent = 'System Not Ready';
        }
    } catch (error) {
        statusDot.classList.add('offline');
        statusText.textContent = 'Backend Offline';
    }
}

function setQuestion(element) {
    document.getElementById('questionInput').value = element.textContent;
}

async function askQuestion() {
    const questionInput = document.getElementById('questionInput');
    const question = questionInput.value.trim();
    
    if (!question) {
        showError('Please enter a question');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    hideResults();
    hideError();
    
    try {
        const response = await fetch(`${BACKEND_URL}ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data);
        } else {
            showError(data.error || 'An error occurred while processing your question');
        }
    } catch (error) {
        showError('Failed to connect to the server. Please make sure the backend is running.');
    } finally {
        setLoadingState(false);
    }
}

function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const answerContent = document.getElementById('answerContent');
    const documentsContent = document.getElementById('documentsContent');
    
    // Display answer
    answerContent.textContent = data.answer;
    
    // Display documents
    documentsContent.innerHTML = '';
    data.retrieved_documents.forEach((doc, index) => {
        const docCard = createDocumentCard(doc, index + 1);
        documentsContent.appendChild(docCard);
    });
    
    resultsSection.style.display = 'block';
}

function createDocumentCard(doc, index) {
    const card = document.createElement('div');
    card.className = 'document-card';
    
    card.innerHTML = `
        <div class="document-header">
            <span class="document-page">Page ${doc.page}</span>
            <span class="document-link">${doc.link}</span>
        </div>
        <div class="document-snippet">${doc.snippet}</div>
    `;
    
    return card;
}

function showError(message) {
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
}

function hideError() {
    document.getElementById('errorSection').style.display = 'none';
}

function hideResults() {
    document.getElementById('resultsSection').style.display = 'none';
}

function setLoadingState(isLoading) {
    const askButton = document.getElementById('askButton');
    const buttonText = document.getElementById('buttonText');
    const buttonLoader = document.getElementById('buttonLoader');
    
    askButton.disabled = isLoading;
    buttonText.style.display = isLoading ? 'none' : 'inline';
    buttonLoader.style.display = isLoading ? 'inline-block' : 'none';
}

// Allow Enter key to submit (Shift+Enter for new line)
document.getElementById('questionInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        askQuestion();
    }
});
