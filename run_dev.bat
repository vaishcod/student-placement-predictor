@echo off
echo ===================================================
echo 🔥 CareerLens AI Dev Server Suite
echo ===================================================
echo.
echo Launching backend and frontend in separate terminals...
echo.

:: Get the directory of this script
set SCRIPT_DIR=%~dp0

:: Launch backend in the root directory
start "CareerLens AI - Backend Server" cmd /k "cd /d %SCRIPT_DIR% && python -m uvicorn backend.main:app --host 0.0.0.0 --port 8080 --reload"

:: Launch frontend in the frontend directory
start "CareerLens AI - Next.js Frontend" cmd /k "cd /d %SCRIPT_DIR%frontend && npm run dev"

echo.
echo Launching web browser...
:: Wait 2 seconds for Next.js to start initializing and then open the browser automatically
timeout /t 2 /nobreak >nul
start http://localhost:3080

echo.
echo ---------------------------------------------------
echo Servers Started!
echo ---------------------------------------------------
echo Backend API Endpoint: http://localhost:8080
echo Frontend Application: http://localhost:3080
echo.
echo (You can close this window now. The servers will keep running in their own windows.)
pause
