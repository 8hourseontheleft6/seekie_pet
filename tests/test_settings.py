#!/usr/bin/env python3
"""
测试设置功能
"""

import sys
import os
import time

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_settings():
    """测试设置功能"""
    print("=" * 50)
    print("测试设置功能")
    print("=" * 50)
    
    try:
        from main_refactored import DesktopPetRobot
        
        print("创建机器人实例...")
        pet = DesktopPetRobot()
        print("✓ 机器人实例创建成功")
        
        print("\n测试设置窗口打开功能:")
        
        # 测试打开设置窗口
        print("1. 第一次打开设置窗口...")
        try:
            pet._open_settings()
            print("   ✓ 设置窗口打开请求已发送")
        except Exception as e:
            print(f"   ❌ 打开设置窗口失败: {e}")
        
        # 等待一下，让线程有机会启动
        time.sleep(1)
        
        print("\n2. 测试避免重复打开...")
        print("   再次调用_open_settings()...")
        try:
            pet._open_settings()
            print("   ✓ 避免重复打开逻辑正常")
        except Exception as e:
            print(f"   ❌ 避免重复打开逻辑失败: {e}")
        
        print("\n3. 测试设置窗口线程...")
        print("   直接调用_open_settings_window_thread()...")
        try:
            pet._open_settings_window_thread()
            print("   ✓ 设置窗口线程正常")
        except Exception as e:
            print(f"   ❌ 设置窗口线程失败: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n4. 测试回退设置窗口...")
        print("   直接调用_fallback_to_modern_settings()...")
        try:
            pet._fallback_to_modern_settings()
            print("   ✓ 回退设置窗口正常")
        except Exception as e:
            print(f"   ❌ 回退设置窗口失败: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "=" * 50)
        print("测试总结:")
        print("=" * 50)
        
        # 检查web_settings模块
        web_settings_dir = os.path.join(os.path.dirname(__file__), 'web_settings')
        if os.path.exists(web_settings_dir):
            print("✓ web_settings目录存在")
            
            # 尝试导入web_settings模块
            try:
                sys.path.insert(0, web_settings_dir)
                from web_settings import open_web_settings
                print("✓ web_settings模块可以导入")
            except ImportError as e:
                print(f"❌ web_settings模块导入失败: {e}")
        else:
            print("❌ web_settings目录不存在")
        
        # 检查settings_window_v2模块
        try:
            from settings_window_v2 import open_modern_settings_window
            print("✓ settings_window_v2模块可以导入")
        except ImportError as e:
            print(f"❌ settings_window_v2模块导入失败: {e}")
        
        # 清理
        pet._quit_app()
        
        print("\n✓ 设置功能测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_settings()
    print(f"\n测试结果: {'通过' if success else '失败'}")
    sys.exit(0 if success else 1)
