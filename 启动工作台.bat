@echo off
chcp 65001 >nul
title 多手机工作台 - 启动器
cd /d "%~dp0"

set "BRIDGE=%~dp0bridge.py"
set "URL1=https://raw.githubusercontent.com/572126160-art/multi-phone-workbench/main/bridge.py"
set "URL2=https://github.com/572126160-art/multi-phone-workbench/raw/refs/heads/main/bridge.py"

echo.
echo ===============================
echo   多手机工作台 - 正在启动
echo ===============================
echo.

echo [1/3] 正在下载最新版桥接器...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; try { Invoke-WebRequest -Uri '%URL1%' -OutFile '%BRIDGE%' -UseBasicParsing -TimeoutSec 15; exit 0 } catch { exit 1 }"

if errorlevel 1 (
  echo 第一个下载源失败，正在尝试备用源...
  powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; try { Invoke-WebRequest -Uri '%URL2%' -OutFile '%BRIDGE%' -UseBasicParsing -TimeoutSec 15; exit 0 } catch { exit 1 }"
)

if not exist "%BRIDGE%" (
  echo.
  echo [错误] bridge.py 下载失败。
  echo 请确认浏览器能正常访问 GitHub。
  echo.
  pause
  exit /b 1
)

echo [2/3] 正在检查 Python...
where py >nul 2>nul
if %errorlevel%==0 (
  set "PY=py"
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    set "PY=python"
  ) else (
    echo.
    echo [错误] 没有检测到 Python。
    echo 请安装 Python 3，并勾选 Add Python to PATH。
    echo.
    pause
    exit /b 1
  )
)

echo [3/3] 正在打开工作台...
echo 固定地址：http://127.0.0.1:8888
echo.
%PY% "%BRIDGE%"

echo.
echo 工作台已停止，或启动过程中出现错误。
echo 如果上面有红色/英文错误，请截图发给我。
echo.
pause
