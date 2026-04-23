@echo off
chcp 65001 >nul
echo ========================================
echo Seekie Pet - 重构版启动脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.6或更高版本
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖...
pip show pillow >nul 2>&1
if errorlevel 1 (
    echo 安装Pillow...
    pip install pillow
)

pip show pystray >nul 2>&1
if errorlevel 1 (
    echo 安装pystray...
    pip install pystray
)

pip show keyboard >nul 2>&1
if errorlevel 1 (
    echo 安装keyboard...
    pip install keyboard
)

pip show flask >nul 2>&1
if errorlevel 1 (
    echo 安装Flask...
    pip install flask
)

echo.
echo ========================================
echo 启动Seekie Pet重构版...
echo ========================================
echo.

REM 运行重构版
python main_refactored.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo 重构版启动失败，尝试使用原版...
    echo ========================================
    echo.
    python main.py
)

pause
