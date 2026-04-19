#!/usr/bin/env python3
"""
最终测试 - 直接运行重构版程序
"""

import sys
import os
import time

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """主函数"""
    print("=" * 50)
    print("最终测试 - 直接运行重构版程序")
    print("=" * 50)
    
    try:
        # 导入并运行主函数
        from main_refactored import main as run_main
        
        print("程序将运行10秒钟...")
        print("请检查:")
        print("1. 屏幕右下角是否出现机器人窗口")
        print("2. 系统托盘是否出现机器人图标")
        print("3. 右键点击托盘图标是否有菜单")
        print("=" * 50)
        
        # 在子进程中运行程序
        import subprocess
        import threading
        
        # 启动程序
        proc = subprocess.Popen([sys.executable, "main_refactored.py"], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True)
        
        # 读取输出的线程
        def read_output(pipe, label):
            for line in pipe:
                print(f"[{label}] {line}", end='')
        
        stdout_thread = threading.Thread(target=read_output, args=(proc.stdout, "OUT"))
        stderr_thread = threading.Thread(target=read_output, args=(proc.stderr, "ERR"))
        stdout_thread.daemon = True
        stderr_thread.daemon = True
        stdout_thread.start()
        stderr_thread.start()
        
        # 等待10秒
        for i in range(10, 0, -1):
            print(f"等待 {i} 秒...")
            time.sleep(1)
        
        # 终止程序
        proc.terminate()
        proc.wait(timeout=5)
        
        print("\n" + "=" * 50)
        print("测试完成")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
