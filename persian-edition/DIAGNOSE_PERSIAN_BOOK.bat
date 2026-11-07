@echo off
setlocal
cd /d "%~dp0"
if not exist "logs" mkdir "logs"
set "PYTHONUTF8=1"
set "PYTHONUNBUFFERED=1"
where py >nul 2>&1
if not errorlevel 1 (
  py -3 tools\local_book.py diagnose > "logs\diagnose.log" 2>&1
) else (
  python tools\local_book.py diagnose > "logs\diagnose.log" 2>&1
)
set "BOOK_EXIT=%ERRORLEVEL%"
type "logs\diagnose.log"
echo Exit code: %BOOK_EXIT%
echo Logs: %CD%\logs
pause
exit /b %BOOK_EXIT%
