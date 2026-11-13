start_bat = """@echo off
setlocal
title Dau Truong Tri Thuc - Olympic Knowledge Arena
cd /d "%~dp0"

echo ======================================================================
echo    DAU TRUONG TRI THUC - OLYMPIC KNOWLEDGE ARENA
echo ======================================================================
echo.

start http://localhost:8000

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [THONG BAO] Phat hien Python, dang khoi chay he thong...
    python run_arena.py
) else (
    echo [THONG BAO] May tinh khong co Python. Dang khoi chay ban Standalone Portable EXE...
    if exist "dist\\OlympicArena\\OlympicArena.exe" (
        cd /d "%~dp0dist\\OlympicArena"
        OlympicArena.exe
    ) else if exist "dist\\ArenaOlympic\\ArenaOlympic.exe" (
        cd /d "%~dp0dist\\ArenaOlympic"
        ArenaOlympic.exe
    ) else (
        echo [ERROR] Khong tim thay file thuc thi Portable!
        pause
    )
)
"""

portable_bat = """@echo off
setlocal
title Dau Truong Tri Thuc - Olympic Arena (Standalone)
cd /d "%~dp0"

echo ======================================================================
echo    DAU TRUONG TRI THUC - OLYMPIC KNOWLEDGE ARENA (STANDALONE)
echo    Che do chay truc tiep - Khong can cai dat Python!
echo ======================================================================
echo.

start http://localhost:8000

if exist "dist\\OlympicArena\\OlympicArena.exe" (
    cd /d "%~dp0dist\\OlympicArena"
    OlympicArena.exe
) else if exist "dist\\ArenaOlympic\\ArenaOlympic.exe" (
    cd /d "%~dp0dist\\ArenaOlympic"
    ArenaOlympic.exe
) else (
    echo [ERROR] Khong tim thay file thuc thi Portable!
    pause
)
"""

with open('start_arena.bat', 'wb') as f:
    f.write(start_bat.replace('\r\n', '\n').replace('\n', '\r\n').encode('ascii'))

with open('Chay_Khong_Can_Python.bat', 'wb') as f:
    f.write(portable_bat.replace('\r\n', '\n').replace('\n', '\r\n').encode('ascii'))

print("Updated bat files successfully.")
