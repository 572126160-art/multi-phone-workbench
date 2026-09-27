@echo off
chcp 65001 >nul
title 多手机工作台

set "DIR=%~dp0"
set "BRIDGE=%DIR%bridge.py"
set "URL=https://raw.githubusercontent.com/572126160-art/multi-phone-workbench/main/bridge.py"

echo 正在检查最新版...
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -Uri '%URL%' -OutFile '%BRIDGE%' -UseBasicParsing } catch { exit 1 }"

if errorlevel 1 (
  echo.
  echo 无法连接 GitHub，尝试运行本地已下载版本...
)

where py >nul 2>nul
if %errorlevel%==0 (
  py "%BRIDGE%"
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    python "%BRIDGE%"
  ) else (
    echo.
    echo 没有检测到 Python。
    echo 请先安装 Python 3，并勾选 Add Python to PATH。
    pause
  )
)
