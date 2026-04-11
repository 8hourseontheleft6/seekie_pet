#!/usr/bin/env python3
"""
桌面宠物机器人 - 机器人在菜单栏上移动
一个轻量级的桌面宠物应用，显示一个机器人在系统托盘区域移动

版本: 3.0.0
修改日期: 2026-04-11
更新: 重大更新 - 使用Robot.png图片代替蓝色小方块
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import sys
import os
from PIL import Image, ImageDraw, ImageTk
import pystray
from pystray import MenuItem as item
import webbrowser

class DesktopPetCar:
    def __init__(self):
        self.window = None
        self.icon = None
        self.running = True
        self.position = 75  # 机器人在菜单栏上的位置 (50-100，限制在右半边)
        self.direction = 0  # 移动方向: 1=向右, -1=向左, 0=停止
        self.speed = 1.5  # 移动速度
        self.car_size = 50  # 机器人大小（匹配图片尺寸50x50）
        self.last_move_time = time.time()  # 上次移动时间
        self.move_interval = 20  # 移动间隔(秒)，大约一分钟
        self.is_moving = False  # 是否正在移动
        
        # 图片相关变量（稍后初始化）
        self.robot_image = None
        self.robot_photo = None
        
        # 创建主窗口
        self.create_window()
        
        # 加载机器人图片（必须在窗口创建后）
        self.load_robot_image()
        
        # 创建系统托盘图标
        self.create_tray_icon()
        
        # 启动动画线程
        self.animation_thread = threading.Thread(target=self.animate, daemon=True)
        self.animation_thread.start()
    
    def load_robot_image(self):
        """加载机器人图片（必须在Tk窗口创建后调用）"""
        try:
            # 尝试从main_pic目录加载Robot_50x50.png
            # 使用绝对路径确保能找到文件
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "main_pic", "Robot_50x50.png")
            
            print(f"尝试加载图片路径: {image_path}")
            print(f"文件是否存在: {os.path.exists(image_path)}")
            
            if os.path.exists(image_path):
                self.robot_image = Image.open(image_path)
                print(f"成功加载机器人图片: {image_path}")
            else:
                # 如果文件不存在，创建一个简单的机器人图标作为后备
                print(f"图片文件不存在: {image_path}，使用后备图标")
                self.robot_image = Image.new('RGBA', (50, 50), (0, 0, 0, 0))
                draw = ImageDraw.Draw(self.robot_image)
                # 绘制简单的机器人图标
                draw.rectangle([10, 10, 40, 40], fill='#4169E1', outline='#1E3A8A', width=2)
                draw.rectangle([15, 15, 25, 25], fill='#FFFFFF', outline='#1E3A8A', width=1)
                draw.rectangle([30, 15, 35, 20], fill='#FF6B6B', outline='#CC5555', width=1)
        except Exception as e:
            print(f"加载图片错误: {e}，使用后备图标")
            self.robot_image = Image.new('RGBA', (50, 50), (0, 0, 0, 0))
            draw = ImageDraw.Draw(self.robot_image)
            draw.rectangle([10, 10, 40, 40], fill='#4169E1', outline='#1E3A8A', width=2)
        
        # 转换为Tkinter可用的格式（必须在Tk窗口创建后）
        self.robot_photo = ImageTk.PhotoImage(self.robot_image)
        
        # 重新绘制机器人
        self.draw_car()
    
    def create_window(self):
        """创建透明窗口"""
        self.window = tk.Tk()
        self.window.title("桌面宠物机器人")
        self.window.overrideredirect(True)  # 移除窗口边框
        self.window.attributes('-topmost', True)  # 保持在最前面
        self.window.attributes('-transparentcolor', 'white')  # 设置透明色
        
        # 创建画布
        self.canvas = tk.Canvas(
            self.window, 
            width=self.car_size, 
            height=self.car_size,
            highlightthickness=0,
            bg='white'
        )
        self.canvas.pack()
        
        # 注意：这里不立即绘制，等图片加载后再绘制
        
        # 更新窗口以获取正确的尺寸信息
        self.window.update()
        
        # 计算初始位置（右下角菜单栏区域）
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # 限制在右半边（初始位置在75，即右半边的中间偏右）
        max_x = screen_width - self.car_size
        # 将75的位置映射到屏幕右半边的x坐标
        x_pos = int((self.position - 50) / 50 * (max_x / 2) + (max_x / 2))
        
        # 保持在底部菜单栏区域，调整垂直偏移让机器人在合适位置
        taskbar_height = 40
        vertical_offset = -5  # 负偏移，让机器人更低
        y_pos = screen_height - taskbar_height - self.car_size + vertical_offset
        
        # 设置窗口位置
        self.window.geometry(f"+{x_pos}+{y_pos}")
    
    def draw_car(self):
        """在画布上绘制机器人图片"""
        if not self.robot_photo:
            return  # 图片未加载，跳过绘制
        
        self.canvas.delete("all")
        
        # 绘制机器人图片
        self.canvas.create_image(
            self.car_size // 2,  # x位置居中
            self.car_size // 2,  # y位置居中
            image=self.robot_photo,
            tags="car"
        )
        
        # 注意：移除了方向指示器箭头，保持机器人图片干净
    
    def create_tray_icon(self):
        """创建系统托盘图标"""
        if not self.robot_image:
            # 如果图片未加载，创建简单的托盘图标
            image = Image.new('RGB', (64, 64), color='white')
            draw = ImageDraw.Draw(image)
            draw.rectangle([20, 20, 44, 44], fill='#4169E1', outline='#1E3A8A', width=2)
            tray_image = image
        else:
            # 使用机器人图片作为托盘图标，调整图片大小为64x64
            tray_image = self.robot_image.resize((64, 64), Image.Resampling.LANCZOS)
        
        # 创建菜单
        menu = (
            item('显示/隐藏', self.toggle_visibility),
            item('速度加快', self.increase_speed),
            item('速度减慢', self.decrease_speed),
            item('随机位置', self.random_position),
            item('关于', self.show_about),
            item('退出', self.quit_app)
        )
        
        # 创建系统托盘图标
        self.icon = pystray.Icon(
            "desktop_pet_robot",
            tray_image,
            "桌面宠物机器人",
            menu
        )
        
        # 在单独的线程中运行托盘图标
        self.tray_thread = threading.Thread(target=self.icon.run, daemon=True)
        self.tray_thread.start()
    
    def toggle_visibility(self, icon, item):
        """切换窗口可见性"""
        if self.window.winfo_viewable():
            self.window.withdraw()
        else:
            self.window.deiconify()
    
    def increase_speed(self, icon, item):
        """增加机器人速度"""
        self.speed = min(5.0, self.speed + 0.5)  # 最大速度5.0
    
    def decrease_speed(self, icon, item):
        """减小机器人速度"""
        self.speed = max(0.5, self.speed - 0.5)  # 最小速度0.5
    
    def random_position(self, icon, item):
        """将机器人移动到随机位置（限制在右半边）"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # 限制在右半边
        min_x = screen_width // 2
        max_x = screen_width - self.car_size
        x = random.randint(min_x, max_x)
        
        # 保持在底部菜单栏区域，调整垂直偏移让机器人在合适位置
        taskbar_height = 40
        vertical_offset = -5  # 负偏移，让机器人更低
        y = screen_height - taskbar_height - self.car_size + vertical_offset
        
        self.window.geometry(f"+{x}+{y}")
        
        # 更新位置变量（50-100范围）
        self.position = 50 + ((x - min_x) / (max_x - min_x)) * 50
    
    def show_about(self, icon, item):
        """显示关于信息"""
        about_window = tk.Toplevel(self.window)
        about_window.title("关于桌面宠物机器人")
        about_window.geometry("300x200")
        about_window.resizable(False, False)
        
        # 居中显示
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() - about_window.winfo_width()) // 2
        y = (about_window.winfo_screenheight() - about_window.winfo_height()) // 2
        about_window.geometry(f"+{x}+{y}")
        
        # 添加内容
        tk.Label(
            about_window,
            text="桌面宠物机器人 v3.0.0",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        tk.Label(
            about_window,
            text="一个轻量级的桌面宠物应用\n\n"
                 "机器人会在你的菜单栏区域移动\n"
                 "你可以通过系统托盘图标控制它\n\n"
                 "版本: 3.0.0 (重大更新: 使用Robot.png图片)\n"
                 "作者: 桌面宠物项目",
            justify=tk.LEFT
        ).pack(pady=10, padx=20)
        
        tk.Button(
            about_window,
            text="关闭",
            command=about_window.destroy
        ).pack(pady=10)
    
    def quit_app(self, icon, item):
        """退出应用"""
        self.running = False
        if self.icon:
            self.icon.stop()
        if self.window:
            self.window.quit()
        # 不要直接调用sys.exit(0)，这会导致托盘图标错误
        # 让主循环自然结束
    
    def animate(self):
        """动画循环 - 让机器人在屏幕右半边偶尔移动"""
        while self.running:
            try:
                current_time = time.time()
                
                # 检查是否应该开始移动（大约每分钟一次）
                if not self.is_moving and (current_time - self.last_move_time) > self.move_interval:
                    self.is_moving = True
                    self.last_move_time = current_time
                    # 随机决定移动距离和方向
                    move_duration = random.uniform(5, 15)  # 移动5-15秒
                    self.move_end_time = current_time + move_duration
                    
                    # 在右半边范围内随机选择目标位置 (50-100)
                    target_position = random.uniform(50, 100)
                    
                    # 决定移动方向
                    if target_position > self.position:
                        self.direction = 1  # 向右
                    else:
                        self.direction = -1  # 向左
                    
                    print(f"开始移动: 方向={self.direction}, 目标位置={target_position:.1f}")
                
                # 如果正在移动，更新位置
                if self.is_moving:
                    # 获取屏幕尺寸
                    screen_width = self.window.winfo_screenwidth()
                    screen_height = self.window.winfo_screenheight()
                    
                    # 计算新位置 (在屏幕底部边缘移动，模拟菜单栏)
                    # 调整垂直偏移，让机器人在合适位置
                    taskbar_height = 40  # 假设任务栏高度
                    vertical_offset = -5  # 负偏移，让机器人更低
                    y_pos = screen_height - taskbar_height - self.car_size + vertical_offset
                    
                    # 更新水平位置（限制在50-100范围内，即右半边）
                    self.position += self.direction * self.speed * 0.05  # 调整速度因子
                    
                    # 边界检查（限制在右半边）
                    if self.position < 50:
                        self.position = 50
                        self.direction = 1  # 向右转
                    elif self.position > 100:
                        self.position = 100
                        self.direction = -1  # 向左转
                    
                    # 检查是否到达移动结束时间
                    if current_time > self.move_end_time:
                        self.is_moving = False
                        self.direction = 0  # 停止移动
                        print("停止移动")
                    
                    # 计算实际x坐标（只使用右半边屏幕）
                    max_x = screen_width - self.car_size
                    # 将50-100的位置映射到屏幕右半边的x坐标
                    x_pos = int((self.position - 50) / 50 * (max_x / 2) + (max_x / 2))
                    
                    # 更新窗口位置
                    self.window.geometry(f"+{x_pos}+{y_pos}")
                    
                    # 重绘机器人
                    self.window.after(0, self.draw_car)
                else:
                    # 不在移动时，确保方向为0
                    if self.direction != 0:
                        self.direction = 0
                        self.window.after(0, self.draw_car)
                
                time.sleep(0.05)  # 高帧率流畅动画（约20FPS）
                
            except Exception as e:
                print(f"动画错误: {e}")
                time.sleep(1)
    
    def run(self):
        """运行应用"""
        try:
            self.window.mainloop()
        except KeyboardInterrupt:
            self.quit_app(None, None)

def main():
    """主函数"""
    print("启动桌面宠物机器人 v3.0.0...")
    print("重大更新: 使用Robot.png图片作为桌面宠物")
    print("优化: 高帧率流畅动画（约20FPS）")
    print("应用将在系统托盘中运行")
    print("右键点击托盘图标可以控制机器人")
    print("=" * 40)
    print("功能特点:")
    print("- 限制在屏幕右半边移动")
    print("- 大约每分钟移动一次")
    print("- 使用自定义Robot.png图片")
    print("- 高帧率流畅动画（约20FPS）")
    print("- 50x50像素大小，适合菜单栏")
    print("=" * 40)
    
    pet = DesktopPetCar()
    pet.run()

if __name__ == "__main__":
    main()
