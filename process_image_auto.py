#!/usr/bin/env python3
"""
自动图片处理脚本 - 将100x100图像压缩适配到50x50空间（无交互）
"""

import os
from PIL import Image

def resize_and_save_image(input_path, output_path, target_size=(50, 50)):
    """将图像调整大小并保存"""
    print(f"处理图像: {input_path}")
    
    try:
        # 打开图像
        img = Image.open(input_path)
        print(f"原始图像尺寸: {img.size}, 模式: {img.mode}")
        
        # 调整大小到目标尺寸，使用高质量的重采样算法
        resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # 保存调整大小后的图像
        resized_img.save(output_path, 'PNG')
        print(f"已保存调整大小后的图像: {output_path}, 尺寸: {resized_img.size}")
        
        return True
        
    except Exception as e:
        print(f"处理图像时出错: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("自动图像处理工具")
    print("将100x100图像适配到50x50空间")
    print("=" * 50)
    
    # 确保main_pic目录存在
    os.makedirs("main_pic", exist_ok=True)
    
    # 定义文件路径
    source_100x100 = os.path.join("main_pic", "Robot_100x100.png")
    source_50x50 = os.path.join("main_pic", "Robot_50x50.png")
    
    # 备份原始50x50图像（如果存在）
    if os.path.exists(source_50x50):
        backup_path = os.path.join("main_pic", "Robot_50x50_backup.png")
        import shutil
        shutil.copy2(source_50x50, backup_path)
        print(f"已备份原始50x50图像到: {backup_path}")
    
    # 检查100x100图像是否存在
    if not os.path.exists(source_100x100):
        print(f"错误: 未找到100x100图像: {source_100x100}")
        print("请确保已将Robot_100x100.png放入main_pic目录")
        return False
    
    # 调整大小并保存为50x50版本
    success = resize_and_save_image(source_100x100, source_50x50, (50, 50))
    
    if success:
        print("\n" + "=" * 50)
        print("处理完成!")
        print(f"1. 原始图像: {source_100x100}")
        print(f"2. 调整大小后: {source_50x50} (50x50)")
        print("=" * 50)
        
        # 显示文件大小信息
        if os.path.exists(source_100x100):
            size_100 = os.path.getsize(source_100x100)
            size_50 = os.path.getsize(source_50x50)
            print(f"文件大小: {size_100/1024:.1f}KB → {size_50/1024:.1f}KB")
        
        print("\n现在可以运行桌面宠物机器人: python main.py")
        return True
    else:
        print("处理失败")
        return False

if __name__ == "__main__":
    main()
