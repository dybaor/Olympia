@echo off
title Dau Truong Tri Thuc - Olympic Arena (Standalone)
cd /d "%~dp0"

echo ======================================================================
echo    DAU TRUONG TRI THUC - OLYMPIC KNOWLEDGE ARENA (STANDALONE)
echo    Che do chay truc tiep - Khong can cai dat Python!
echo ======================================================================
echo.

:: Tu dong mo trinh duyet sau 2 giay
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:8000"

:: Khoi chay ban Standalone Portable EXE
cd dist\ArenaOlympic
ArenaOlympic.exe

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Ung dung gap su co khi khoi chay.
    pause
)
