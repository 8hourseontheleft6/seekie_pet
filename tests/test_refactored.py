#!/usr/bin/env python3
"""
测试重构版功能
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_config_manager():
    """测试配置管理器"""
    print("=" * 50)
    print("测试配置管理器")
    print("=" * 50)
    
    try:
        from config.config_manager import get_config_manager, get_config
        
        # 获取配置管理器
        manager = get_config_manager()
        print("✓ 配置管理器获取成功")
        
        # 加载配置
        config = get_config()
        print("✓ 配置加载成功")
        
        # 打印配置信息
        print(f"版本: {config.version}")
        print(f"窗口标题: {config.window_title}")
        print(f"运动间隔: {config.robot.move_interval}秒")
        print(f"运动速度: {config.robot.move_speed}")
        print(f"截图快捷键: {config.hotkeys.screenshot}")
        print(f"主题: {config.appearance.theme.value}")
        print(f"透明度: {config.appearance.transparency}")
        
        # 验证配置
        if manager.validate():
            print("✓ 配置验证成功")
        else:
            print("⚠ 配置验证失败")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置管理器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_logger():
    """测试日志记录器"""
    print("\n" + "=" * 50)
    print("测试日志记录器")
    print("=" * 50)
    
    try:
        from utils.logger import setup_logging, info, error, warning
        
        # 设置日志
        logger = setup_logging(level="INFO", enable_file=False, enable_console=True)
        print("✓ 日志记录器设置成功")
        
        # 测试日志记录
        info("信息级别日志测试")
        warning("警告级别日志测试")
        error("错误级别日志测试")
        
        print("✓ 日志记录测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 日志记录器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_loader():
    """测试图片加载器"""
    print("\n" + "=" * 50)
    print("测试图片加载器")
    print("=" * 50)
    
    try:
        from utils.image_loader import load_robot_image, load_sleep_image
        
        # 测试加载机器人图片
        robot_image = load_robot_image((50, 50))
        if robot_image:
            print(f"✓ 机器人图片加载成功，大小: {robot_image.size}")
        else:
            print("⚠ 机器人图片加载失败，使用默认图片")
        
        # 测试加载睡眠图片
        sleep_image = load_sleep_image((50, 50))
        if sleep_image:
            print(f"✓ 睡眠图片加载成功，大小: {sleep_image.size}")
        else:
            print("⚠ 睡眠图片加载失败，使用默认图片")
        
        print("✓ 图片加载器测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 图片加载器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_import():
    """测试主程序导入"""
    print("\n" + "=" * 50)
    print("测试主程序导入")
    print("=" * 50)
    
    try:
        # 尝试导入主程序类
        from main_refactored import DesktopPetRobot
        
        print("✓ 主程序类导入成功")
        
        # 检查类的方法（包括私有方法）
        all_methods = dir(DesktopPetRobot)
        print(f"✓ 找到 {len(all_methods)} 个方法")
        
        # 检查必需的方法（包括私有方法）
        required_methods = ['run', '_init_window', '_load_images', '_init_tray']
        missing_methods = [m for m in required_methods if m not in all_methods]
        
        if missing_methods:
            print(f"⚠ 缺少方法: {missing_methods}")
            return False
        else:
            print("✓ 所有必需方法都存在")
            return True
            
    except Exception as e:
        print(f"❌ 主程序导入测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("Seekie Pet 重构版功能测试")
    print("=" * 50)
    
    tests = [
        ("配置管理器", test_config_manager),
        ("日志记录器", test_logger),
        ("图片加载器", test_image_loader),
        ("主程序导入", test_main_import),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n正在测试: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results.append((test_name, False))
    
    # 打印测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    all_passed = True
    for test_name, success in results:
        status = "✓ 通过" if success else "❌ 失败"
        print(f"{test_name}: {status}")
        if not success:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有测试通过！重构版功能正常。")
        print("可以运行 'python main_refactored.py' 启动应用。")
    else:
        print("⚠ 部分测试失败，请检查错误信息。")
        print("可以尝试运行原版 'python main.py'。")
    
    print("=" * 50)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
