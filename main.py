#!/usr/bin/env python3
"""
桌面宠物机器人 v3.4.0 - 模块化重构版

将核心逻辑拆分为独立模块：
  - core/window.py: 窗口管理
  - core/animation.py: 动画管理
  - core/movement.py: 移动逻辑
  - core/input_detection.py: 输入检测
  - core/hotkeys.py: 快捷键
  - core/tray.py: 系统托盘
  - core/settings.py: 设置窗口
  - core/robot.py: 主类整合
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import setup_logging, get_logger, info
from config.config_manager import get_config
from core.robot import DesktopPetRobot

logger = get_logger()


def print_header():
    """打印程序头信息"""
    config = get_config()
    
    print("=" * 50)
    print("桌面宠物机器人 v3.4.0 (模块化重构版)")
    print("=" * 50)
    print("功能特点:")
    print("- 模块化结构，代码更清晰")
    print("- 增强的错误处理和日志记录")
    print("- 改进的配置管理")
    print(f"- 运动间隔: {config.robot.move_interval}秒")
    print(f"- 运动速度: {config.robot.move_speed}")
    print(f"- 截图快捷键: {config.hotkeys.screenshot}")
    print(f"- 主题: {config.appearance.theme.value}")
    print(f"- 透明度: {config.appearance.transparency}")
    print(f"- 睡眠模式: {'启用' if config.behavior.enable_sleep_mode else '禁用'}")
    print(f"- 输入检测: {'启用' if config.behavior.enable_input_detection else '禁用'}")
    print("=" * 50)
    print("应用将在系统托盘中运行")
    print("右键点击托盘图标可以控制机器人")
    print("=" * 50)


def main():
    """主函数"""
    setup_logging(level="INFO", enable_file=True, enable_console=True)
    print_header()
    
    try:
        pet = DesktopPetRobot()
        pet.run()
    except Exception as e:
        info(f"应用启动失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
