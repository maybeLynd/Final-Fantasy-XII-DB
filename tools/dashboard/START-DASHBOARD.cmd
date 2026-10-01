@echo off
rem FF12 database dashboard - read-only, loopback only (http://127.0.0.1:8765/).
rem Double-click to start. The page picks up a new generation within ~5 s.
rem Builds are also refreshed by the fleet controller (board transitions + 30 min).
cd /d "%~dp0"

netstat -ano | findstr /r /c:"127\.0\.0\.1:8765 .*LISTENING" >nul 2>&1
if %errorlevel%==0 (
    start "" http://127.0.0.1:8765/
    exit /b 0
)

rem Rebuild once so a fresh checkout is never empty, then serve CURRENT only.
python build_views.py
rem supervise.py runs server.py and restarts it by itself whenever the dashboard code changes (no manual restart).
start "FF12-Dashboard" /min cmd /c "python supervise.py --root ..\work\dashboard >> ..\work\dashboard\server.log 2>&1"
timeout /t 2 /nobreak >nul
start "" http://127.0.0.1:8765/
