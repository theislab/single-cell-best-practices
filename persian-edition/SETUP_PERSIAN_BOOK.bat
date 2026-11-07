@echo off
setlocal
cd /d "%~dp0"
if not exist "logs" mkdir "logs"
set "PYTHONUTF8=1"
set "PYTHONUNBUFFERED=1"
set "BOOK_PYTHON="
python -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>&1
if not errorlevel 1 set "BOOK_PYTHON=python"
if defined BOOK_PYTHON goto run_book
for %%V in (3.14 3.13 3.12 3.11 3) do (
  py -%%V -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>&1
  if not errorlevel 1 (
    set "BOOK_PYTHON=py -%%V"
    goto run_book
  )
)
echo ERROR: No usable Python 3.11+ interpreter was found.
echo Check python --version and py -0p. Install Python 3.12+ if necessary.
pause
exit /b 1
:run_book
%BOOK_PYTHON% tools\local_book.py setup > "logs\setup.log" 2>&1
set "BOOK_EXIT=%ERRORLEVEL%"
type "logs\setup.log"
echo Exit code: %BOOK_EXIT%
echo Logs: %CD%\logs
pause
exit /b %BOOK_EXIT%
