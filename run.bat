@echo off

set CUDA_VISIBLE_DEVICES=0

title LoRA Trainer - 67372a Fork - Flux Branch
cd %~dp0
call venv\Scripts\activate
python main.py
pause
