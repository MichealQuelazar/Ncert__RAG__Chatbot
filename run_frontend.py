"""
Script to run the Flask frontend server
"""
import os
from frontend.app import app

if __name__ == "__main__":
    port = int(os.getenv('FRONTEND_PORT', 5000))
    print(f"Starting Flask frontend on http://localhost:{port}")
    print(f"Make sure the backend is running on port 8000")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True,
        use_reloader=True,
        extra_files=[]  # Prevent watching site-packages
    )
