"""
Flask frontend application
"""
from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1")

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """Handle question submission"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400
        
        # Send request to FastAPI backend
        response = requests.post(
            f"{BACKEND_URL}/ask",
            json={"question": question},
            timeout=30
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                'error': f'Backend error: {response.status_code}',
                'detail': response.text
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Failed to connect to backend',
            'detail': str(e)
        }), 503
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'detail': str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Backend unavailable: {str(e)}'
        }), 503

if __name__ == '__main__':
    port = int(os.getenv('FRONTEND_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
