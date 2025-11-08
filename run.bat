@echo off

title LoRA Trainer - 67372a Fork - Refresh Branch
cd %~dp0
call venv\Scripts\activate
python main.py
pause
