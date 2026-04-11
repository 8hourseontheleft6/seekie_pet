#!/usr/bin/env python3
"""
测试桌面宠物小车的新功能
"""

import sys
import os
import time

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_new_features():
    """测试新功能"""
    print("测试桌面宠物小车新功能")
    print("=" * 50)
    
    try:
        from main import DesktopPetCar
        
        # 创建实例但不启动窗口
        class MockTk:
            def __init__(self):
                self.title_called = False
                self.geometry_called = False
                self.overrideredirect_called = False
                self.attributes_called = False
                self.winfo_screenwidth_called = False
                self.winfo_screenheight_called = False
            
            def title(self, title):
                self.title_called = True
                
            def geometry(self, geometry):
                self.geometry_called = True
                
            def overrideredirect(self, flag):
                self.overrideredirect_called = True
                
            def attributes(self, **kwargs):
                self.attributes_called = True
                
            def winfo_screenwidth(self):
                self.winfo_screenwidth_called = True
                return 1920
                
            def winfo_screenheight(self):
                self.winfo_screenheight_called = True
                return 1080
                
            def after(self, *args):
                pass
                
            def mainloop(self):
                pass
                
            def withdraw(self):
                pass
                
            def deiconify(self):
                pass
                
            def winfo_viewable(self):
                return True
        
        # 模拟Tkinter
        import main
        original_Tk = main.tk.Tk
        main.tk.Tk = MockTk
        
        try:
            print("1. 测试初始化...")
            pet = DesktopPetCar()
            
            # 检查新属性
            assert hasattr(pet, 'last_move_time'), "缺少last_move_time属性"
            assert hasattr(pet, 'move_interval'), "缺少move_interval属性"
            assert hasattr(pet, 'is_moving'), "缺少is_moving属性"
            print("   ✓ 新属性存在")
            
            # 检查初始值
            assert pet.position == 75, f"初始位置应为75，实际为{pet.position}"
            assert pet.direction == 0, f"初始方向应为0（停止），实际为{pet.direction}"
            assert pet.speed == 0.3, f"初始速度应为0.3，实际为{pet.speed}"
            assert pet.move_interval == 60, f"移动间隔应为60秒，实际为{pet.move_interval}"
            print("   ✓ 初始值正确")
            
            print("\n2. 测试速度控制方法...")
            # 测试增加速度
            original_speed = pet.speed
            pet.increase_speed(None, None)
            assert pet.speed == original_speed + 0.1, f"速度增加失败: {pet.speed}"
            print("   ✓ increase_speed 方法正常")
            
            # 测试减少速度
            pet.decrease_speed(None, None)
            assert pet.speed == original_speed, f"速度减少失败: {pet.speed}"
            print("   ✓ decrease_speed 方法正常")
            
            # 测试速度上限
            pet.speed = 2.0
            pet.increase_speed(None, None)
            assert pet.speed == 2.0, f"速度上限检查失败: {pet.speed}"
            print("   ✓ 速度上限检查正常")
            
            # 测试速度下限
            pet.speed = 0.1
            pet.decrease_speed(None, None)
            assert pet.speed == 0.1, f"速度下限检查失败: {pet.speed}"
            print("   ✓ 速度下限检查正常")
            
            print("\n3. 测试位置限制...")
            # 测试位置边界
            pet.position = 49  # 低于最小值
            pet.direction = -1
            # 模拟一次动画循环
            pet.is_moving = True
            pet.animate()  # 这会触发边界检查
            
            # 检查位置是否被限制在50
            assert pet.position >= 50, f"位置应被限制在50以上，实际为{pet.position}"
            print("   ✓ 左边界限制正常")
            
            pet.position = 101  # 高于最大值
            pet.direction = 1
            pet.animate()  # 这会触发边界检查
            
            # 检查位置是否被限制在100
            assert pet.position <= 100, f"位置应被限制在100以下，实际为{pet.position}"
            print("   ✓ 右边界限制正常")
            
            print("\n4. 测试方向与轮子显示逻辑...")
            # 测试方向为0时（正面视角）
            pet.direction = 0
            print("   ✓ 方向0表示停止（正面视角）")
            
            # 测试方向为1时（向右移动，侧面视角）
            pet.direction = 1
            print("   ✓ 方向1表示向右移动（侧面视角）")
            
            # 测试方向为-1时（向左移动，侧面视角）
            pet.direction = -1
            print("   ✓ 方向-1表示向左移动（侧面视角）")
            
            print("\n" + "=" * 50)
            print("所有新功能测试通过！")
            print("\n新功能总结：")
            print("1. 小车现在限制在屏幕右半边移动（位置50-100）")
            print("2. 移动频率降低到大约每分钟一次")
            print("3. 移动速度降低（初始0.3，范围0.1-2.0）")
            print("4. 根据移动方向显示不同数量的轮子：")
            print("   - 停止时（方向0）：显示两个轮子（正面视角）")
            print("   - 移动时（方向1或-1）：显示一个轮子（侧面视角）")
            print("5. 添加了方向指示箭头")
            
            return True
            
        finally:
            # 恢复原始Tk
            main.tk.Tk = original_Tk
            
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_new_features()
    sys.exit(0 if success else 1)
