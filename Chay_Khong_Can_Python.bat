@echo off
setlocal
title Dau Truong Tri Thuc - Olympic Arena (Standalone)
cd /d "%~dp0"

echo ======================================================================
echo    DAU TRUONG TRI THUC - OLYMPIC KNOWLEDGE ARENA (STANDALONE)
echo    Che do chay truc tiep - Khong can cai dat Python!
echo ======================================================================
echo.

start http://localhost:8000

if exist "dist\Olympic_Portable\Olympic_Portable.exe" (
    cd /d "%~dp0dist\Olympic_Portable"
    Olympic_Portable.exe
) else if exist "dist\OlympicArena\OlympicArena.exe" (
    cd /d "%~dp0dist\OlympicArena"
    OlympicArena.exe
) else (
    echo [ERROR] Khong tim thay file thuc thi Portable!
    pause
)
