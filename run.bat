@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
set PYTHONPATH=%cd%
streamlit run app.py
pause
