@echo off
setlocal

:: This script activates the Python virtual environment,
:: checks for updates, and then runs the main.py script.

set VENV_DIR=.venv
set MAIN_SCRIPT=src\thronin\main.py
set UPDATE_CHECK_SCRIPT=src\thronin\check_for_updates.py

echo Running Thronin...

:: Step 1: Activate virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment. Exiting.
    goto :script_end
)
echo Virtual environment activated.

:: Step 2: Perform update check using the Python script
echo.
echo Checking for updates...

:: Check if the update check script exists
if not exist "%UPDATE_CHECK_SCRIPT%" (
    echo Error: Update check script "%UPDATE_CHECK_SCRIPT%" not found in the current directory.
    echo Please ensure "check_for_updates.py" is in the same folder as this batch script.
    goto :skip_update_check
)

:: Use the virtual environment's Python to run the update check script
for /f "delims=" %%a in ('cmd /c ""%VENV_DIR%\Scripts\python.exe" "%UPDATE_CHECK_SCRIPT%""') do set "UPDATE_STATUS=%%a"

:: Check the exit code of the Python script (ERRORLEVEL)
:: 100 indicates an update is available (custom code from Python script)
:: 0 indicates no update needed or check couldn't be performed (no error)
:: Any other non-zero indicates an error during the Python script execution

if %ERRORLEVEL% equ 100 (
    echo.
    echo ==========================================================
    echo !!! A NEW VERSION OF THRONIN IS AVAILABLE ON GITHUB !!!
    echo !!! Please visit the GitHub repository to update.    !!!
    echo ==========================================================
    echo.
    pause
    goto :script_end
) else if %ERRORLEVEL% neq 0 (
    echo Error during update check. See messages above. Continuing anyway.
) else (
    echo %UPDATE_STATUS%
)

echo.

:skip_update_check
:: Step 3: Run main.py using the virtual environment's Python executable
echo Running %MAIN_SCRIPT%...
"%VENV_DIR%\Scripts\python.exe" "%MAIN_SCRIPT%"
if %errorlevel% neq 0 (
    echo Error: The Python script '%MAIN_SCRIPT%' encountered an error.
    echo Please review the output above for details.
) else (
    echo Script finished successfully.
)

:: Step 4: Deactivate virtual environment
echo.
echo Deactivating virtual environment...
call deactivate
if %errorlevel% neq 0 (
    echo Warning: Failed to deactivate virtual environment.
) else (
    echo Virtual environment deactivated.
)

echo.
echo --- Script Execution Complete ---
echo.

:script_end
endlocal
pause
