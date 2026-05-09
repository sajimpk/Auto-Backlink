@echo off
REM Backlink Generator Batch File for Windows
REM This makes it easy to run the Python script

setlocal enabledelayedexpansion

if "%~1"=="" (
    echo.
    echo Backlink Generator Tool
    echo =======================
    echo.
    echo Usage:
    echo   backlink.bat ^<domain^> [options]
    echo.
    echo Examples:
    echo   backlink.bat example.com
    echo   backlink.bat example.com --test
    echo   backlink.bat example.com --test --output backlinks.csv
    echo.
    python backlink-generator.py
) else (
    python backlink-generator.py %*
)

pause
