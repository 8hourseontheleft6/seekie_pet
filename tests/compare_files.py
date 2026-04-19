#!/usr/bin/env python3
"""
比较两个主文件
"""

import os
import sys

def compare_files():
    """比较文件"""
    print("=" * 50)
    print("主文件比较")
    print("=" * 50)
    
    # 文件大小
    main_size = os.path.getsize("main.py")
    refactored_size = os.path.getsize("main_refactored.py")
    
    print(f"文件大小:")
    print(f"  main.py: {main_size:,} 字节")
    print(f"  main_refactored.py: {refactored_size:,} 字节")
    print(f"  差异: {refactored_size - main_size:,} 字节")
    
    # 读取文件内容
    with open("main.py", "r", encoding="utf-8") as f:
        main_content = f.read()
    
    with open("main_refactored.py", "r", encoding="utf-8") as f:
        refactored_content = f.read()
    
    # 行数比较
    main_lines = main_content.count('\n')
    refactored_lines = refactored_content.count('\n')
    
    print(f"\n行数比较:")
    print(f"  main.py: {main_lines} 行")
    print(f"  main_refactored.py: {refactored_lines} 行")
    print(f"  差异: {refactored_lines - main_lines} 行")
    
    print("\n" + "=" * 50)
    print("功能对比")
    print("=" * 50)
    
    print("\n1. main.py - 原版 (v3.2.0):")
    print("   ✅ Web设置窗口版")
    print("   ✅ 经过充分测试")
    print("   ✅ 功能完整稳定")
    print("   ✅ 直接运行 run.bat")
    print("   ✅ 用户熟悉")
    
    print("\n2. main_refactored.py - 重构版 (v3.3.0):")
    print("   ✅ 模块化架构")
    print("   ✅ 增强的错误处理")
    print("   ✅ 改进的配置管理")
    print("   ✅ 智能图片加载")
    print("   ✅ 完整的日志系统")
    print("   ⚠️  需要更多测试")
    print("   ✅ 运行 run_refactored.bat")
    
    print("\n" + "=" * 50)
    print("使用建议")
    print("=" * 50)
    
    print("\n对于普通用户:")
    print("  推荐使用 main.py (原版)")
    print("  - 运行: python main.py 或 run.bat")
    print("  - 稳定可靠，功能完整")
    
    print("\n对于开发者或想要新功能的用户:")
    print("  可以尝试 main_refactored.py (重构版)")
    print("  - 运行: python main_refactored.py 或 run_refactored.bat")
    print("  - 模块化架构，便于维护和扩展")
    
    print("\n" + "=" * 50)
    print("当前状态")
    print("=" * 50)
    
    # 检查配置文件
    config_exists = os.path.exists("config.json")
    print(f"配置文件: {'✅ 存在' if config_exists else '❌ 不存在'}")
    
    # 检查图片目录
    main_pic_exists = os.path.exists("main_pic")
    print(f"图片目录: {'✅ 存在' if main_pic_exists else '❌ 不存在'}")
    
    if main_pic_exists:
        files = os.listdir("main_pic")
        print(f"图片文件: {len(files)} 个文件")
        for file in files:
            print(f"  - {file}")
    
    print("\n两个版本共享:")
    print("  ✅ 相同的配置文件 (config.json)")
    print("  ✅ 相同的图片资源 (main_pic/)")
    print("  ✅ 相同的依赖要求")
    
    return True

if __name__ == "__main__":
    compare_files()
