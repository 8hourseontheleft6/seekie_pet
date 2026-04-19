#!/usr/bin/env python3
"""
测试窗口显示
"""

import sys
import os
import time

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_window_display():
    """测试窗口显示"""
    print("=" * 50)
    print("测试窗口显示")
    print("=" * 50)
    
    try:
        # 导入必要的模块
        import tkinter as tk
        from PIL import Image, ImageTk
        
        # 创建简单窗口测试
        root = tk.Tk()
        root.title("窗口显示测试")
        root.geometry("300x200")
        
        # 尝试加载机器人图片
        try:
            from utils.image_loader import load_robot_image
            robot_image = load_robot_image((50, 50))
            if robot_image:
                photo = ImageTk.PhotoImage(robot_image)
                label = tk.Label(root, image=photo)
                label.image = photo  # 保持引用
                label.pack(pady=20)
                print("✓ 机器人图片加载并显示成功")
            else:
                print("❌ 机器人图片加载失败")
        except Exception as e:
            print(f"❌ 图片加载错误: {e}")
        
        # 添加说明标签
        label_text = tk.Label(root, text="如果看到机器人图片，说明图片加载正常")
        label_text.pack(pady=10)
        
        # 运行窗口3秒
        print("窗口将显示3秒钟...")
        root.after(3000, root.quit)
        root.mainloop()
        
        print("✓ 窗口显示测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 窗口显示测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_window_display()
    sys.exit(0 if success else 1)
