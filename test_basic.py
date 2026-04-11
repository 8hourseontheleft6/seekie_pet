#!/usr/bin/env python3
"""
基本功能测试
测试桌面宠物小车的基本功能，不启动GUI
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_import():
    """测试导入"""
    print("测试导入...")
    try:
        from main import DesktopPetCar
        print("✓ 导入成功")
        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False

def test_class_creation():
    """测试类创建"""
    print("\n测试类创建...")
    try:
        from main import DesktopPetCar
        
        # 创建实例但不启动窗口
        class MockTk:
            def __init__(self):
                self.title_called = False
                self.geometry_called = False
                self.overrideredirect_called = False
                self.attributes_called = False
            
            def title(self, title):
                self.title_called = True
                
            def geometry(self, geometry):
                self.geometry_called = True
                
            def overrideredirect(self, flag):
                self.overrideredirect_called = True
                
            def attributes(self, **kwargs):
                self.attributes_called = True
        
        # 模拟Tkinter
        import main
        original_Tk = main.tk.Tk
        main.tk.Tk = MockTk
        
        try:
            pet = DesktopPetCar()
            print("✓ 类创建成功")
            
            # 检查基本属性
            assert hasattr(pet, 'position'), "缺少position属性"
            assert hasattr(pet, 'direction'), "缺少direction属性"
            assert hasattr(pet, 'speed'), "缺少speed属性"
            assert hasattr(pet, 'car_size'), "缺少car_size属性"
            print("✓ 基本属性存在")
            
            return True
        finally:
            # 恢复原始Tk
            main.tk.Tk = original_Tk
            
    except Exception as e:
        print(f"✗ 类创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_methods():
    """测试方法"""
    print("\n测试方法...")
    try:
        from main import DesktopPetCar
        
        # 创建模拟实例
        pet = DesktopPetCar.__new__(DesktopPetCar)
        pet.position = 50
        pet.direction = 1
        pet.speed = 2
        pet.car_size = 32
        
        # 测试速度调整方法
        pet.speed = 5
        pet.increase_speed(None, None)
        assert pet.speed == 6, f"速度增加失败: {pet.speed}"
        print("✓ increase_speed 方法正常")
        
        pet.decrease_speed(None, None)
        assert pet.speed == 5, f"速度减少失败: {pet.speed}"
        print("✓ decrease_speed 方法正常")
        
        # 测试边界
        pet.speed = 10
        pet.increase_speed(None, None)
        assert pet.speed == 10, f"速度上限检查失败: {pet.speed}"
        print("✓ 速度上限检查正常")
        
        pet.speed = 1
        pet.decrease_speed(None, None)
        assert pet.speed == 1, f"速度下限检查失败: {pet.speed}"
        print("✓ 速度下限检查正常")
        
        return True
        
    except Exception as e:
        print(f"✗ 方法测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("桌面宠物小车 - 基本功能测试")
    print("=" * 50)
    
    tests_passed = 0
    tests_total = 3
    
    # 运行测试
    if test_import():
        tests_passed += 1
    
    if test_class_creation():
        tests_passed += 1
    
    if test_methods():
        tests_passed += 1
    
    # 输出结果
    print("\n" + "=" * 50)
    print(f"测试结果: {tests_passed}/{tests_total} 通过")
    
    if tests_passed == tests_total:
        print("✓ 所有基本功能测试通过!")
        return 0
    else:
        print("✗ 部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
