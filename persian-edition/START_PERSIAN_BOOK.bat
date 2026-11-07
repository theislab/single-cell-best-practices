@echo off
setlocal
cd /d "%~dp0"
if not exist "logs" mkdir "logs"
set "PYTHONUTF8=1"
set "PYTHONUNBUFFERED=1"
where py >nul 2>&1
if not errorlevel 1 (
  py -3 tools\local_book.py start
) else (
  python tools\local_book.py start
)
set "BOOK_EXIT=%ERRORLEVEL%"
rem Server output remains visible; use Ctrl+C to stop.
echo Exit code: %BOOK_EXIT%
echo Logs: %CD%\logs
pause
exit /b %BOOK_EXIT%
