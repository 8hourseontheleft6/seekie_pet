#!/usr/bin/env python3
"""
图片处理脚本 - 将100x100图像压缩适配到50x50空间
"""

import os
from PIL import Image, ImageDraw
import sys

def create_sample_100x100_image():
    """创建一个示例的100x100机器人图像（如果不存在）"""
    print("创建示例100x100机器人图像...")
    
    # 创建一个100x100的透明背景图像
    img = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制一个更大的机器人（100x100版本）
    # 身体
    draw.rectangle([20, 20, 80, 80], fill='#4169E1', outline='#1E3A8A', width=4)
    
    # 头部/屏幕区域
    draw.rectangle([30, 25, 70, 45], fill='#2E4B8F', outline='#1E3A8A', width=2)
    
    # 眼睛
    draw.ellipse([35, 30, 45, 40], fill='#00FF00', outline='#00CC00', width=2)  # 左眼绿色
    draw.ellipse([55, 30, 65, 40], fill='#00FF00', outline='#00CC00', width=2)  # 右眼绿色
    
    # 嘴巴（微笑）
    draw.arc([40, 45, 60, 55], 0, 180, fill='#FF6B6B', width=3)
    
    # 轮子
    draw.ellipse([25, 70, 45, 90], fill='#333333', outline='#000000', width=2)  # 左轮
    draw.ellipse([55, 70, 75, 90], fill='#333333', outline='#000000', width=2)  # 右轮
    
    # 保存为100x100版本
    output_path = os.path.join("main_pic", "Robot_100x100.png")
    img.save(output_path, 'PNG')
    print(f"已创建示例图像: {output_path}")
    
    return output_path

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
    print("图像处理工具 - 将100x100图像适配到50x50空间")
    print("=" * 50)
    
    # 确保main_pic目录存在
    os.makedirs("main_pic", exist_ok=True)
    
    # 定义文件路径
    source_100x100 = os.path.join("main_pic", "Robot_100x100.png")
    source_50x50 = os.path.join("main_pic", "Robot_50x50.png")
    
    # 检查100x100图像是否存在
    if not os.path.exists(source_100x100):
        print(f"未找到100x100图像: {source_100x100}")
        print("请将你的100x100机器人图像放入 main_pic/Robot_100x100.png")
        print("或者按回车键创建示例图像...")
        
        # 等待用户输入
        try:
            input("按回车键继续创建示例图像，或按Ctrl+C取消...")
        except KeyboardInterrupt:
            print("\n已取消")
            return
        
        # 创建示例图像
        source_100x100 = create_sample_100x100_image()
    
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
        
        print("\n现在你可以:")
        print("1. 运行桌面宠物机器人: python main.py")
        print("2. 查看处理后的图像")
        print("3. 如果需要，替换main_pic/Robot_100x100.png为你自己的图像")
        print("   然后重新运行此脚本: python process_image.py")
    else:
        print("处理失败，请检查错误信息")

if __name__ == "__main__":
    main()
