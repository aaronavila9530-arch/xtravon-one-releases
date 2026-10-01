@echo off
setlocal

cd /d "%~dp0.."

echo.
echo === Compilando XTRAVON ONE con PyInstaller ===
python -m PyInstaller --clean --noconfirm XTRAVON_ONE.spec
if errorlevel 1 (
    echo.
    echo ERROR: Fallo PyInstaller.
    exit /b 1
)

echo.
echo === Compilando instalador con Inno Setup ===
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "%CD%\installer\XTRAVON_ONE.iss"
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    "C:\Program Files\Inno Setup 6\ISCC.exe" "%CD%\installer\XTRAVON_ONE.iss"
) else (
    echo.
    echo ERROR: No se encontro ISCC.exe de Inno Setup 6.
    echo Instale Inno Setup o compile manualmente el archivo installer\XTRAVON_ONE.iss.
    exit /b 1
)

if errorlevel 1 (
    echo.
    echo ERROR: Fallo Inno Setup.
    exit /b 1
)

echo.
echo Instalador generado en:
echo %CD%\installer\Output\XTRAVON_ONE_Setup_1.0.0.exe
endlocal
