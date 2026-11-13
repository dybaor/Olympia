@echo off
title Dau Truong Tri Thuc - Olympic Knowledge Arena
cd /d "%~dp0"

:: Tu dong mo trinh duyet sau 2 giay
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:8000"

:: Kiem tra neu co Python thi chay Python, neu khong co thi chay ban Portable EXE
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [THONG BAO] Phat hien Python, dang khoi chay tu source code...
    python run_arena.py
) else (
    echo [THONG BAO] May tinh khong co Python. Dang khoi chay ban Standalone Portable EXE...
    if exist "dist\ArenaOlympic\ArenaOlympic.exe" (
        cd dist\ArenaOlympic
        ArenaOlympic.exe
    ) else (
        echo [ERROR] Khong tim thay file thuc thi Portable!
        pause
    )
)
