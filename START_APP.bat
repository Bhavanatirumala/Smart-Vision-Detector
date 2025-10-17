@echo off
title Smart Vision Detector
echo.
echo ========================================
echo    Smart Vision Detector
echo ========================================
echo.
echo Starting the application...
echo The app will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the app when done
echo ========================================
echo.

cd /d "%~dp0"
python -m streamlit run app_simple.py --server.headless true

pause

