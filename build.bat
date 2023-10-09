@echo off
setlocal EnableDelayedExpansion

title build EquityHistory
cd /d %~dp0
if exist dist RMDIR /S /Q dist
python -m venv venv --clear
call venv/scripts/activate
python -m pip install -U pip
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
pyinstaller EquityHistory.spec
if exist build RMDIR /S /Q build
if exist dist start dist
pause