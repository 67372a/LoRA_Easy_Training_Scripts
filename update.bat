@echo off
cd /d %~dp0

set PATH=%USERPROFILE%\.local\bin;%PATH%
git pull
python update.py
pause
