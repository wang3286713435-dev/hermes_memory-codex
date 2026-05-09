@echo off
setlocal

cd /d "%~dp0\..\.."

set RALPH_ACTIVE=1
if "%RALPH_MAX_ITERATIONS%"=="" set RALPH_MAX_ITERATIONS=10

set STATE_FILE=.claude\context\runtime\ralph-state.json
if exist "%STATE_FILE%" del "%STATE_FILE%"

for /f %%i in ('powershell -NoProfile -Command "Get-Date -AsUTC -Format yyyy-MM-ddTHH:mm:ssZ"') do set NOW=%%i
(
  echo {
  echo   "iteration": 0,
  echo   "startedAt": "%NOW%",
  echo   "lastRunAt": "%NOW%",
  echo   "lastFindingsCount": null,
  echo   "maxIterations": %RALPH_MAX_ITERATIONS%
  echo }
) > "%STATE_FILE%"

claude --print-output-format text < .claude\ralph\PROMPT.md
