@echo off
title Agent Atelier Preview
cd /d "%~dp0"
set "PYTHONPATH=%~dp0src"
python -m agent_atelier.preview
if errorlevel 1 (
  echo.
  echo Agent Atelier could not start. Check that Python is installed and available.
  pause
)
