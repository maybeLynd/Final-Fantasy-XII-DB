@echo off
rem Stop the dashboard supervisor and server (the listener on 127.0.0.1:8765) and nothing else.
cd /d "%~dp0"
rem the supervisor first, or it would start a new server as soon as the listener stops
if exist ..\work\dashboard\supervisor.pid (
    for /f %%s in (..\work\dashboard\supervisor.pid) do (
        echo stopping dashboard supervisor pid %%s
        taskkill /pid %%s /t /f >nul 2>&1
    )
    del ..\work\dashboard\supervisor.pid >nul 2>&1
)
for /f "tokens=5" %%p in ('netstat -ano ^| findstr /r /c:"127\.0\.0\.1:8765 .*LISTENING"') do (
    echo stopping dashboard pid %%p
    taskkill /pid %%p /f >nul 2>&1
)
echo dashboard stopped (or was not running).
