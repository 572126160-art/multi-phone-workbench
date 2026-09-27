@echo off
title Multi Phone Workbench
cd /d "%~dp0"

echo =====================================
echo Multi Phone Workbench Launcher
echo =====================================
echo.

echo Downloading latest bridge.py...
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; $ErrorActionPreference='Stop'; try { Invoke-WebRequest 'https://raw.githubusercontent.com/572126160-art/multi-phone-workbench/main/bridge.py' -OutFile 'bridge.py' -UseBasicParsing; Write-Host 'Download OK' } catch { Write-Host 'Download failed:' $_.Exception.Message; exit 2 }"

if not exist "bridge.py" goto DOWNLOAD_FAIL

echo.
echo Starting workbench...
py "bridge.py"
if %errorlevel%==0 goto END

python "bridge.py"
if %errorlevel%==0 goto END

echo.
echo Python could not be started.
echo Please install Python 3 and enable Add Python to PATH.
goto END

:DOWNLOAD_FAIL
echo.
echo bridge.py was not downloaded.
echo Please check your internet connection and GitHub access.
goto END

:END
echo.
echo If the browser did not open, send me a screenshot of this window.
echo.
pause
