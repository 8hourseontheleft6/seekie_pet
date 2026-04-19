@echo off
chcp 65001 >nul
echo ========================================
echo Seekie Pet 启动器
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

echo.
echo ========================================
echo 选择启动版本
echo ========================================
echo 1. 原版 (main.py) - 稳定版
echo    - 版本: 3.2.0 (Web设置窗口版)
echo    - 特点: 经过充分测试，功能完整
echo.
echo 2. 重构版 (main_refactored.py) - 开发版
echo    - 版本: 3.3.0 (模块化重构版)
echo    - 特点: 模块化架构，增强功能
echo.
echo 3. 自动选择 (推荐)
echo    - 优先尝试重构版，失败则使用原版
echo.
set /p choice="请选择 (1/2/3，默认3): "

if "%choice%"=="" set choice=3
if "%choice%"=="1" goto run_original
if "%choice%"=="2" goto run_refactored
if "%choice%"=="3" goto run_auto

:run_auto
echo.
echo ========================================
echo 自动选择模式
echo ========================================
echo 优先尝试重构版...
echo.
python main_refactored.py
if errorlevel 1 (
    echo.
    echo ========================================
    echo 重构版启动失败，使用原版...
    echo ========================================
    echo.
    python main.py
)
goto end

:run_original
echo.
echo ========================================
echo 启动原版 (稳定版)
echo ========================================
echo.
python main.py
goto end

:run_refactored
echo.
echo ========================================
echo 启动重构版 (开发版)
echo ========================================
echo.
python main_refactored.py
goto end

:end
pause
