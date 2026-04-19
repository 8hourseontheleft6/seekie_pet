#!/usr/bin/env python3
"""
测试最终修复 - 验证图片加载和运动控制
"""

import sys
import os
import time
import threading

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_final_fix():
    """测试最终修复"""
    print("=" * 50)
    print("测试最终修复 - 验证图片加载和运动控制")
    print("=" * 50)
    
    try:
        from main_refactored import DesktopPetRobot
        
        print("创建机器人实例...")
        pet = DesktopPetRobot()
        print("✓ 机器人实例创建成功")
        
        # 检查图片是否加载
        print("\n检查图片加载:")
        if pet.robot_photo:
            print("✓ 机器人图片已加载")
        else:
            print("❌ 机器人图片未加载")
            
        if pet.sleep_photo:
            print("✓ 睡眠图片已加载")
        else:
            print("❌ 睡眠图片未加载")
        
        # 检查初始状态
        print(f"\n初始状态:")
        print(f"  位置: {pet.position}")
        print(f"  方向: {pet.direction}")
        print(f"  速度: {pet.speed}")
        print(f"  是否移动: {pet.is_moving}")
        print(f"  是否睡眠: {pet.is_sleeping}")
        
        # 运行5秒钟，观察运动
        print("\n运行5秒钟，观察运动状态...")
        
        # 在后台线程中运行主循环
        def run_main():
            try:
                pet.run()
            except Exception as e:
                print(f"运行错误: {e}")
        
        main_thread = threading.Thread(target=run_main, daemon=True)
        main_thread.start()
        
        # 记录初始状态
        initial_position = pet.position
        initial_moving = pet.is_moving
        
        # 等待5秒，每1秒检查一次状态
        for i in range(5, 0, -1):
            print(f"等待 {i} 秒... 位置: {pet.position:.1f}, 移动: {pet.is_moving}")
            time.sleep(1)
        
        # 检查状态变化
        print(f"\n状态变化:")
        print(f"  初始位置: {initial_position:.1f}")
        print(f"  最终位置: {pet.position:.1f}")
        print(f"  位置变化: {abs(pet.position - initial_position):.1f}")
        print(f"  初始移动状态: {initial_moving}")
        print(f"  最终移动状态: {pet.is_moving}")
        
        # 检查是否曾经移动过
        if abs(pet.position - initial_position) > 0.1:
            print("✓ 机器人移动正常")
        else:
            print("⚠ 机器人可能没有移动")
        
        # 检查运动控制
        if pet.is_moving:
            print("⚠ 机器人仍在移动（可能不会自动停止）")
        else:
            print("✓ 机器人停止移动正常")
        
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
    success = test_final_fix()
    sys.exit(0 if success else 1)
