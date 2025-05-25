@echo off
REM Activate the virtual environment, start the Flask web app, and open it in the browser
cd /d %~dp0
call btg_env\Scripts\activate.bat
set FLASK_APP=webapp.py
start "" http://127.0.0.1:5000/
python -m flask run
