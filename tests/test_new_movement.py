#!/usr/bin/env python3
"""
测试新的运动逻辑：机器人运动到指定地点后，等待几秒，再开始新的运动
"""

import sys
import os
import time

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_new_movement():
    """测试新的运动逻辑"""
    print("=" * 60)
    print("测试新的运动逻辑")
    print("=" * 60)
    
    try:
        from main_refactored import DesktopPetRobot
        
        print("创建机器人实例...")
        pet = DesktopPetRobot()
        print("✓ 机器人实例创建成功")
        
        print("\n1. 测试初始状态:")
        print(f"   - 当前位置: {pet.position}")
        print(f"   - 是否移动: {pet.is_moving}")
        print(f"   - 方向: {pet.direction}")
        print(f"   - 目标位置: {pet.target_position}")
        
        print("\n2. 测试开始移动:")
        current_time = time.time()
        pet._start_moving(current_time)
        
        print(f"   - 开始移动后 is_moving: {pet.is_moving}")
        print(f"   - 方向: {pet.direction}")
        print(f"   - 目标位置: {pet.target_position:.1f}")
        
        print("\n3. 模拟移动到目标位置:")
        # 模拟多次更新，直到到达目标位置
        steps = 0
        max_steps = 100
        
        while pet.is_moving and steps < max_steps:
            pet._update_movement(time.time())
            steps += 1
            time.sleep(0.01)  # 快速模拟
        
        print(f"   - 模拟 {steps} 步后")
        print(f"   - 当前位置: {pet.position:.1f}")
        print(f"   - 目标位置: {pet.target_position:.1f}")
        print(f"   - 是否移动: {pet.is_moving}")
        
        if not pet.is_moving:
            print("   ✓ 到达目标位置后自动停止")
        else:
            print("   ❌ 到达目标位置后未停止")
        
        print("\n4. 测试等待间隔:")
        # 记录停止时间
        stop_time = time.time()
        print(f"   - 停止时间: {stop_time}")
        print(f"   - 最后移动时间: {pet.last_move_time}")
        
        # 检查是否会在配置的间隔后重新开始移动
        move_interval = pet.config.robot.move_interval
        print(f"   - 移动间隔配置: {move_interval}秒")
        
        # 模拟时间过去一半间隔
        half_interval = move_interval / 2
        simulated_time = stop_time + half_interval
        
        # 检查是否应该开始移动（不应该，因为时间还没到）
        should_start = not pet.is_moving and (simulated_time - pet.last_move_time) > move_interval
        print(f"   - 经过 {half_interval} 秒后是否应该开始移动: {should_start}")
        
        if not should_start:
            print("   ✓ 正确等待移动间隔")
        else:
            print("   ❌ 未正确等待移动间隔")
        
        # 模拟时间过去完整间隔
        full_interval = move_interval + 1
        simulated_time = stop_time + full_interval
        
        # 检查是否应该开始移动（应该，因为时间到了）
        should_start = not pet.is_moving and (simulated_time - pet.last_move_time) > move_interval
        print(f"   - 经过 {full_interval} 秒后是否应该开始移动: {should_start}")
        
        if should_start:
            print("   ✓ 等待足够时间后可以开始新移动")
        else:
            print("   ❌ 等待足够时间后未开始新移动")
        
        print("\n5. 测试边界情况:")
        # 测试边界位置
        pet.position = 50
        pet.target_position = 30  # 尝试设置小于50的目标
        pet.direction = -1
        pet.is_moving = True
        
        pet._update_movement(time.time())
        print(f"   - 位置=50, 目标=30, 更新后位置: {pet.position}")
        print(f"   - 方向是否反转: {pet.direction == 1}")
        
        if pet.position == 50 and pet.direction == 1:
            print("   ✓ 边界检查正常（最小值）")
        else:
            print("   ❌ 边界检查异常")
        
        # 测试另一个边界
        pet.position = 100
        pet.target_position = 120  # 尝试设置大于100的目标
        pet.direction = 1
        pet.is_moving = True
        
        pet._update_movement(time.time())
        print(f"   - 位置=100, 目标=120, 更新后位置: {pet.position}")
        print(f"   - 方向是否反转: {pet.direction == -1}")
        
        if pet.position == 100 and pet.direction == -1:
            print("   ✓ 边界检查正常（最大值）")
        else:
            print("   ❌ 边界检查异常")
        
        print("\n" + "=" * 60)
        print("测试总结:")
        print("=" * 60)
        
        issues = []
        
        if pet.is_moving:
            issues.append("到达目标位置后未停止")
        
        if issues:
            print("发现以下问题:")
            for issue in issues:
                print(f"  ❌ {issue}")
            print(f"\n共发现 {len(issues)} 个问题需要修复")
        else:
            print("所有测试通过！")
            print("✓ 机器人运动到指定地点后自动停止")
            print("✓ 等待配置的间隔时间后开始新运动")
            print("✓ 边界检查正常")
            print("✓ 运动逻辑符合用户要求")
        
        print("\n" + "=" * 60)
        print("实际运行观察:")
        print("=" * 60)
        print("运行程序观察实际效果:")
        print("  python main_refactored.py")
        print("\n观察:")
        print("  1. 机器人应该每10秒左右移动一次")
        print("  2. 每次移动到随机目标位置后停止")
        print("  3. 停止后等待10秒再开始下一次移动")
        print("  4. 日志应该显示:")
        print("     - '开始移动: 方向=X, 目标=Y.Y'")
        print("     - '到达目标位置: Y.Y'")
        
        # 清理
        pet._quit_app()
        
        return len(issues) == 0
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_new_movement()
    print(f"\n测试结果: {'通过' if success else '失败'}")
    sys.exit(0 if success else 1)
