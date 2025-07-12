@echo off
setlocal

:: This script sets up the Python virtual environment
:: and installs the required dependencies.
set VENV_DIR=.venv
set REQUIREMENTS_FILE=requirements.txt

echo Setting up Python environment...

:: Create virtual environment
py -m venv %VENV_DIR%

:: Activate virtual environment
call "%VENV_DIR%\Scripts\activate.bat"

:: Install dependencies from requirements.txt
pip install -r %REQUIREMENTS_FILE%

:: Install thronin as an editable package
pip install -e .

:: Deactivate virtual environment
call deactivate

echo Environment setup complete.

endlocal
pause
