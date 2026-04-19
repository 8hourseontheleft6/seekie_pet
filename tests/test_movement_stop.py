#!/usr/bin/env python3
"""
测试运动停止功能
"""

import sys
import os
import time
import threading

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_movement_stop():
    """测试运动停止功能"""
    print("=" * 50)
    print("测试运动停止功能")
    print("=" * 50)
    
    try:
        from main_refactored import DesktopPetRobot
        
        print("创建机器人实例...")
        pet = DesktopPetRobot()
        print("✓ 机器人实例创建成功")
        
        print("\n测试运动控制:")
        
        # 模拟开始移动
        current_time = time.time()
        print(f"当前时间: {current_time}")
        
        # 手动调用开始移动
        pet._start_moving(current_time)
        print(f"开始移动后 is_moving: {pet.is_moving}")
        print(f"移动方向: {pet.direction}")
        print(f"移动结束时间: {pet.move_end_time}")
        print(f"移动持续时间: {pet.move_end_time - current_time:.1f}秒")
        
        # 模拟多次更新移动
        print("\n模拟移动过程:")
        for i in range(1, 6):
            # 模拟时间流逝
            simulated_time = current_time + i
            print(f"\n第{i}秒:")
            print(f"  模拟时间: {simulated_time}")
            print(f"  移动结束时间: {pet.move_end_time}")
            print(f"  是否应该停止: {simulated_time > pet.move_end_time}")
            
            # 更新移动
            pet._update_movement(simulated_time)
            print(f"  更新后 is_moving: {pet.is_moving}")
            print(f"  更新后位置: {pet.position:.1f}")
            print(f"  更新后方向: {pet.direction}")
            
            if not pet.is_moving:
                print("  ✓ 机器人已停止移动")
                break
        
        # 检查最终状态
        print(f"\n最终状态:")
        print(f"  is_moving: {pet.is_moving}")
        print(f"  方向: {pet.direction}")
        print(f"  位置: {pet.position:.1f}")
        
        if not pet.is_moving:
            print("✓ 运动停止功能正常")
        else:
            print("❌ 运动停止功能异常 - 机器人仍在移动")
        
        # 测试睡眠状态下的运动停止
        print("\n测试睡眠状态下的运动停止:")
        pet.is_sleeping = True
        pet.is_moving = True  # 手动设置为移动状态
        
        # 检查动画循环逻辑
        print(f"睡眠状态下 is_sleeping: {pet.is_sleeping}")
        print(f"睡眠状态下 is_moving: {pet.is_moving}")
        
        # 模拟动画循环中的睡眠状态处理
        if pet.is_sleeping and pet.is_moving:
            print("❌ 睡眠状态下机器人仍在移动")
        else:
            print("✓ 睡眠状态下机器人停止移动")
        
        # 清理
        pet._quit_app()
        
        return not pet.is_moving
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_movement_stop()
    print(f"\n测试结果: {'通过' if success else '失败'}")
    sys.exit(0 if success else 1)
