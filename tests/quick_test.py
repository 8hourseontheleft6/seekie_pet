#!/usr/bin/env python3
"""
快速测试重构版程序
"""

import sys
import os
import threading
import time

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """主函数"""
    try:
        from main_refactored import DesktopPetRobot
        
        print("=" * 50)
        print("快速测试重构版程序")
        print("=" * 50)
        
        # 创建机器人实例
        print("创建机器人实例...")
        pet = DesktopPetRobot()
        print("✓ 机器人实例创建成功")
        
        # 运行3秒钟
        print("\n程序将运行3秒钟...")
        
        # 在后台线程中运行主循环
        def run_main():
            try:
                pet.run()
            except Exception as e:
                print(f"运行错误: {e}")
        
        main_thread = threading.Thread(target=run_main, daemon=True)
        main_thread.start()
        
        # 等待3秒
        for i in range(3, 0, -1):
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
    success = main()
    sys.exit(0 if success else 1)
