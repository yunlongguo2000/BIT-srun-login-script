@echo off
setlocal enabledelayedexpansion
if exist "f:\BIT-srun-login-script\autoload.pid" (
    for /f "delims=" %%i in (f:\BIT-srun-login-script\autoload.pid) do set pid=%%i
    echo Read PID: !pid!
    if not "!pid!"=="" (
        echo Terminating process with PID: !pid!
        taskkill /PID !pid! /F
        del "f:\BIT-srun-login-script\autoload.pid"
    ) else (
        echo PID file is empty or invalid.
    )
) else (
    echo autoload.pid does not exist, nothing to do.
)
pause