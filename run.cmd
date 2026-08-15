@echo off
setlocal
cd /d "%~dp0"

REM Greenroom needs to be served over HTTP rather than opened as a file.
REM IndexedDB is scoped per origin, and file:// does not give the parent app
REM and Chart Builder a shared one -- so the song library bridge between them
REM only works when both come from the same http:// address.

set "PORT=8777"
set "PY="

where python >nul 2>&1 && set "PY=python"
if not defined PY (where py >nul 2>&1 && set "PY=py")

if not defined PY (
  echo.
  echo   Python was not found on your PATH.
  echo   Install it from https://www.python.org/downloads/ and run this again.
  echo.
  pause
  exit /b 1
)

echo.
echo   Greenroom is running at:  http://127.0.0.1:%PORT%/
echo.
echo   Keep this window open while you use the app.
echo   Close it, or press Ctrl+C, to stop.
echo.

start "" "http://127.0.0.1:%PORT%/"
%PY% -m http.server %PORT% --bind 127.0.0.1
