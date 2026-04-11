@echo off
echo 正在启动桌面宠物小车...
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
    echo 安装Pillow库...
    pip install pillow
)

pip show pystray >nul 2>&1
if errorlevel 1 (
    echo 安装pystray库...
    pip install pystray
)

REM 运行应用
echo.
echo 启动桌面宠物小车...
echo 应用将在系统托盘中运行
echo 右键点击托盘图标可以控制小车
echo.
python main.py

pause
