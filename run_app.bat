@echo off
echo Starting Smart Vision Detector...
python -m streamlit run app_simple.py --server.port 8501 --server.headless true
pause
