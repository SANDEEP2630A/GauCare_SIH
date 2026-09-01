@echo off
echo ===================================
echo   Starting MastiSense servers...
echo ===================================

:: Start Backend (Django) in new window
echo Starting Backend on http://127.0.0.1:8000 ...
start "MastiSense Backend" cmd /k "cd backend && venv313\Scripts\activate && python manage.py runserver 127.0.0.1:8000"

:: Wait a moment for backend to start
timeout /t 3 /nobreak >nul

:: Start Frontend (Vite) in new window
echo Starting Frontend on http://localhost:3000 ...
start "MastiSense Frontend" cmd /k "npm run dev"

echo.
echo Both servers are starting!
echo   Backend:  http://127.0.0.1:8000
echo   Frontend: http://localhost:3000
echo.
echo Close the server windows or press Ctrl+C to stop.
pause
