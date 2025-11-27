@echo off
echo ========================================
echo NCERT Q&A Web Application
echo ========================================
echo.

echo Starting Backend (FastAPI)...
start "Backend - FastAPI" cmd /k python run_backend.py

timeout /t 3 /nobreak >nul

echo Starting Frontend (Flask)...
start "Frontend - Flask" cmd /k python run_frontend.py

echo.
echo ========================================
echo Application started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5000
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press any key to exit...
pause >nul
