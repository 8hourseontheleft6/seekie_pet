#!/usr/bin/env python3
"""
快速运行重构版程序15秒
"""

import sys
import os
import subprocess
import time

def main():
    """主函数"""
    print("=" * 50)
    print("快速运行重构版程序15秒")
    print("=" * 50)
    
    try:
        # 启动程序
        proc = subprocess.Popen([sys.executable, "main_refactored.py"], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True,
                               bufsize=1,
                               universal_newlines=True)
        
        print("程序已启动，运行15秒...")
        print("请检查:")
        print("1. 屏幕右下角是否出现机器人窗口")
        print("2. 机器人是否在移动")
        print("3. 系统托盘是否有机器人图标")
        print("=" * 50)
        
        # 读取输出15秒
        start_time = time.time()
        while time.time() - start_time < 15:
            # 读取标准输出
            line = proc.stdout.readline()
            if line:
                print(f"[OUT] {line}", end='')
            
            # 读取标准错误
            line_err = proc.stderr.readline()
            if line_err:
                print(f"[ERR] {line_err}", end='')
            
            # 短暂休眠
            time.sleep(0.1)
        
        # 终止程序
        print("\n15秒结束，终止程序...")
        proc.terminate()
        proc.wait(timeout=5)
        
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
