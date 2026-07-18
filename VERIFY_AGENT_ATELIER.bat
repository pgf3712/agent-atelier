@echo off
setlocal
title Verify Agent Atelier
cd /d "%~dp0"
set "PYTHONPATH=%~dp0src"

echo [1/4] Running deterministic tests...
python -m unittest discover -s tests -v
if errorlevel 1 goto :failed

echo [2/4] Compiling Python sources...
python -m compileall -q src tests
if errorlevel 1 goto :failed

echo [3/4] Checking browser JavaScript...
where node >nul 2>&1
if errorlevel 1 (
  echo Node.js was not found. Install it to validate web/app.js locally.
  goto :failed
)
node --check web\app.js
if errorlevel 1 goto :failed

echo [4/4] Running deterministic evaluation...
python -m agent_atelier.evaluate_cli
if errorlevel 1 goto :failed

echo.
echo Agent Atelier verification passed.
pause
exit /b 0

:failed
echo.
echo Verification failed. Read the error above before publishing.
pause
exit /b 1
