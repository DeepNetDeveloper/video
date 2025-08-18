@echo off
echo 🎬 Video Retalking - Quick Launch
echo ================================
echo.
echo Activating conda environment and starting app...
echo.

call conda activate retalking
if errorlevel 1 (
    echo ❌ Failed to activate conda environment 'retalking'
    echo Please make sure the environment exists and conda is properly installed.
    pause
    exit /b 1
)

echo ✅ Environment activated
echo 🚀 Starting Gradio interface...
echo.
echo 📱 Open your browser and go to: http://localhost:7860
echo 🔄 Press Ctrl+C to stop the server
echo.

python app.py

if errorlevel 1 (
    echo.
    echo ❌ Error occurred while running the app
    pause
)