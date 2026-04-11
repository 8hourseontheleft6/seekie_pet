#!/usr/bin/env python3
"""
清理图片边缘 - 确保机器人图片边缘完全透明，避免黑边问题
"""

import os
from PIL import Image

def clean_image_edges(input_path, output_path, threshold=10):
    """
    清理图片边缘，将接近透明的像素设为完全透明
    
    参数:
    - input_path: 输入图片路径
    - output_path: 输出图片路径
    - threshold: 透明度阈值 (0-255)，低于此值的alpha通道设为0
    """
    print(f"清理图片边缘: {input_path}")
    
    try:
        # 打开图像
        img = Image.open(input_path)
        print(f"原始图像尺寸: {img.size}, 模式: {img.mode}")
        
        # 确保图像是RGBA模式
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            print(f"转换图像模式为: RGBA")
        
        # 获取图像数据
        data = img.getdata()
        
        # 创建新图像数据
        new_data = []
        cleaned_pixels = 0
        
        for pixel in data:
            r, g, b, a = pixel
            
            # 如果alpha值低于阈值，设为完全透明
            if a < threshold:
                new_data.append((r, g, b, 0))
                cleaned_pixels += 1
            else:
                new_data.append(pixel)
        
        # 创建新图像
        cleaned_img = Image.new('RGBA', img.size)
        cleaned_img.putdata(new_data)
        
        # 保存清理后的图像
        cleaned_img.save(output_path, 'PNG')
        
        print(f"清理完成: {cleaned_pixels}个像素被设为完全透明")
        print(f"已保存清理后的图像: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"清理图像时出错: {e}")
        return False

def process_robot_images():
    """处理机器人图片"""
    print("=" * 50)
    print("机器人图片边缘清理工具")
    print("=" * 50)
    
    # 确保main_pic目录存在
    os.makedirs("main_pic", exist_ok=True)
    
    # 定义文件路径
    source_100x100 = os.path.join("main_pic", "Robot_100x100.png")
    source_50x50 = os.path.join("main_pic", "Robot_50x50.png")
    cleaned_50x50 = os.path.join("main_pic", "Robot_50x50_cleaned.png")
    
    # 检查源图像是否存在
    if not os.path.exists(source_100x100):
        print(f"错误: 未找到100x100图像: {source_100x100}")
        return False
    
    if not os.path.exists(source_50x50):
        print(f"错误: 未找到50x50图像: {source_50x50}")
        return False
    
    # 备份原始50x50图像
    import shutil
    backup_path = os.path.join("main_pic", "Robot_50x50_original.png")
    shutil.copy2(source_50x50, backup_path)
    print(f"已备份原始50x50图像到: {backup_path}")
    
    # 清理50x50图像边缘
    print("\n清理50x50图像边缘...")
    success = clean_image_edges(source_50x50, cleaned_50x50, threshold=30)
    
    if success:
        # 用清理后的图像替换原始图像
        shutil.copy2(cleaned_50x50, source_50x50)
        print(f"\n已用清理后的图像替换原始图像")
        
        # 显示文件信息
        original_size = os.path.getsize(backup_path)
        cleaned_size = os.path.getsize(source_50x50)
        print(f"文件大小: {original_size/1024:.1f}KB → {cleaned_size/1024:.1f}KB")
        
        print("\n" + "=" * 50)
        print("清理完成!")
        print("现在重新运行桌面宠物机器人应该没有黑边了")
        print("=" * 50)
        
        return True
    else:
        print("清理失败")
        return False

def main():
    """主函数"""
    success = process_robot_images()
    
    if success:
        print("\n使用方法:")
        print("1. 重新运行桌面宠物机器人: python main.py")
        print("2. 如果仍有黑边，可以调整阈值重新运行此脚本")
        print("3. 运行: python clean_image_edges.py")
    else:
        print("\n处理失败，请检查错误信息")

if __name__ == "__main__":
    main()
