pip install -r requirements.txt
cls
@echo off
TITLE File Explorer Server
ECHO Khoi dong File Explorer server tai port 5006...

REM Chay ung dung Python tu moi truong ao voi tham so cong la 5006
python app.py 5006 --debug

ECHO Server da dung lai.
pause
