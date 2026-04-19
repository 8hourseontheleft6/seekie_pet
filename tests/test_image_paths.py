#!/usr/bin/env python3
"""
测试图片路径和加载
"""

import os
import sys

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_image_paths():
    """测试图片路径"""
    print("=" * 50)
    print("测试图片路径")
    print("=" * 50)
    
    # 当前工作目录
    cwd = os.getcwd()
    print(f"当前工作目录: {cwd}")
    
    # main_pic目录
    main_pic_dir = os.path.join(cwd, "main_pic")
    print(f"main_pic目录: {main_pic_dir}")
    print(f"目录是否存在: {os.path.exists(main_pic_dir)}")
    
    # 检查main_pic中的文件
    if os.path.exists(main_pic_dir):
        files = os.listdir(main_pic_dir)
        print(f"main_pic中的文件: {files}")
        
        # 检查每个文件
        for filename in files:
            filepath = os.path.join(main_pic_dir, filename)
            print(f"\n文件: {filename}")
            print(f"  完整路径: {filepath}")
            print(f"  是否存在: {os.path.exists(filepath)}")
            print(f"  文件大小: {os.path.getsize(filepath) if os.path.exists(filepath) else 'N/A'} 字节")
    
    print("\n" + "=" * 50)
    print("测试图片加载器路径")
    print("=" * 50)
    
    try:
        from utils.image_loader import ImageType, ImageLoader
        
        loader = ImageLoader()
        
        # 测试机器人图片路径
        robot_path = loader.get_image_path(ImageType.ROBOT)
        print(f"机器人图片路径: {robot_path}")
        print(f"路径是否存在: {os.path.exists(robot_path)}")
        
        # 测试睡眠图片路径
        sleep_path = loader.get_image_path(ImageType.SLEEP)
        print(f"睡眠图片路径: {sleep_path}")
        print(f"路径是否存在: {os.path.exists(sleep_path)}")
        
        # 测试托盘图片路径
        tray_path = loader.get_image_path(ImageType.TRAY)
        print(f"托盘图片路径: {tray_path}")
        print(f"路径是否存在: {os.path.exists(tray_path)}")
        
        # 尝试加载图片
        print("\n" + "=" * 50)
        print("测试图片加载")
        print("=" * 50)
        
        robot_image = loader.load_image(ImageType.ROBOT, (50, 50))
        if robot_image:
            print(f"机器人图片加载成功，大小: {robot_image.size}")
            print(f"图片模式: {robot_image.mode}")
        else:
            print("机器人图片加载失败")
        
        sleep_image = loader.load_image(ImageType.SLEEP, (50, 50))
        if sleep_image:
            print(f"睡眠图片加载成功，大小: {sleep_image.size}")
            print(f"图片模式: {sleep_image.mode}")
        else:
            print("睡眠图片加载失败")
            
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_relative_paths():
    """测试相对路径"""
    print("\n" + "=" * 50)
    print("测试相对路径")
    print("=" * 50)
    
    # 测试从不同目录加载
    test_paths = [
        "main_pic/Robot_50x50.png",
        "./main_pic/Robot_50x50.png",
        os.path.join(os.getcwd(), "main_pic", "Robot_50x50.png"),
        "Robot_50x50.png",
    ]
    
    for path in test_paths:
        print(f"\n路径: {path}")
        print(f"是否存在: {os.path.exists(path)}")
        if os.path.exists(path):
            try:
                from PIL import Image
                img = Image.open(path)
                print(f"  可以打开，大小: {img.size}")
                img.close()
            except Exception as e:
                print(f"  打开失败: {e}")

if __name__ == "__main__":
    test_image_paths()
    test_relative_paths()
