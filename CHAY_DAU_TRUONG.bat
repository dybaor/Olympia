@echo off
setlocal
title Dau Truong Tri Thuc - Olympic Knowledge Arena
cd /d "%~dp0"

echo ======================================================================
echo    DAU TRUONG TRI THUC - OLYMPIC KNOWLEDGE ARENA
echo ======================================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [THONG BAO] Khoi chay he thong thong qua Python...
    python run_arena.py
) else (
    echo [THONG BAO] Khoi chay ban Standalone Portable EXE...
    if exist "dist\OlympicArena\OlympicArena.exe" (
        cd /d "%~dp0dist\OlympicArena"
        OlympicArena.exe
    ) else if exist "dist\Olympic_Portable\Olympic_Portable.exe" (
        cd /d "%~dp0dist\Olympic_Portable"
        Olympic_Portable.exe
    ) else (
        echo [ERROR] Khong tim thay file thuc thi!
        pause
    )
)

