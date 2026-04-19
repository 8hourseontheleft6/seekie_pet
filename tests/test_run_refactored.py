#!/usr/bin/env python3
"""
测试运行重构版程序
"""

import sys
import os
import threading
import time

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_run_refactored():
    """测试运行重构版程序"""
    print("=" * 50)
    print("测试运行重构版程序")
    print("=" * 50)
    
    try:
        from main_refactored import DesktopPetRobot, main
        
        print("✓ 导入成功")
        
        # 创建机器人实例
        print("创建机器人实例...")
        pet = DesktopPetRobot()
        print("✓ 机器人实例创建成功")
        
        # 检查图片是否加载
        print("\n检查图片加载状态:")
        if pet.robot_photo:
            print("✓ 机器人图片已加载")
        else:
            print("❌ 机器人图片未加载")
            
        if pet.sleep_photo:
            print("✓ 睡眠图片已加载")
        else:
            print("❌ 睡眠图片未加载")
        
        # 检查窗口是否创建
        print("\n检查窗口状态:")
        if pet.window:
            print(f"✓ 窗口已创建，标题: {pet.window.title()}")
        else:
            print("❌ 窗口未创建")
            
        if pet.canvas:
            print("✓ 画布已创建")
        else:
            print("❌ 画布未创建")
        
        # 检查托盘图标
        print("\n检查托盘图标:")
        if pet.icon:
            print("✓ 托盘图标已初始化")
        else:
            print("❌ 托盘图标未初始化")
        
        # 运行几秒钟然后退出
        print("\n" + "=" * 50)
        print("程序将运行5秒钟进行测试...")
        print("=" * 50)
        
        # 在后台线程中运行主循环
        def run_main():
            try:
                pet.run()
            except Exception as e:
                print(f"运行错误: {e}")
        
        main_thread = threading.Thread(target=run_main, daemon=True)
        main_thread.start()
        
        # 等待5秒
        for i in range(5, 0, -1):
            print(f"等待 {i} 秒...")
            time.sleep(1)
        
        # 退出程序
        print("\n测试完成，退出程序...")
        pet._quit_app()
        
        print("✓ 测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_run_refactored()
    sys.exit(0 if success else 1)
