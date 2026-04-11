#!/usr/bin/env python3
"""
桌面宠物小车 - 二轮小车在菜单栏上移动
一个轻量级的桌面宠物应用，显示一个二轮小车在系统托盘区域移动

版本: 2.0.4
修改日期: 2026-04-11
修复: 修复小车启动位置问题，启动时直接出现在右下角菜单栏
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
        self.position = 75  # 小车在菜单栏上的位置 (50-100，限制在右半边)
        self.direction = 0  # 移动方向: 1=向右, -1=向左, 0=停止
        self.speed = 0.3  # 移动速度 (降低速度)
        self.car_size = 48  # 小车大小（从32增加到48，让车身更清晰）
        self.last_move_time = time.time()  # 上次移动时间
        self.move_interval = 60  # 移动间隔(秒)，大约一分钟
        self.is_moving = False  # 是否正在移动
        
        # 创建主窗口
        self.create_window()
        
        # 创建系统托盘图标
        self.create_tray_icon()
        
        # 启动动画线程
        self.animation_thread = threading.Thread(target=self.animate, daemon=True)
        self.animation_thread.start()
    
    def create_window(self):
        """创建透明窗口"""
        self.window = tk.Tk()
        self.window.title("桌面宠物小车")
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
        
        # 绘制小车
        self.draw_car()
        
        # 更新窗口以获取正确的尺寸信息
        self.window.update()
        
        # 计算初始位置（右下角菜单栏区域）
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # 限制在右半边（初始位置在75，即右半边的中间偏右）
        max_x = screen_width - self.car_size
        # 将75的位置映射到屏幕右半边的x坐标
        x_pos = int((self.position - 50) / 50 * (max_x / 2) + (max_x / 2))
        
        # 保持在底部菜单栏区域，调整垂直偏移让小车在合适位置
        taskbar_height = 40
        vertical_offset = -5  # 负偏移，让小车更低
        y_pos = screen_height - taskbar_height - self.car_size + vertical_offset
        
        # 设置窗口位置
        self.window.geometry(f"+{x_pos}+{y_pos}")
    
    def draw_car(self):
        """在画布上绘制蓝色小方块"""
        self.canvas.delete("all")
        
        # 蓝色小方块 - 简单的正方形
        square_size = self.car_size - 12  # 方块大小，留出边距
        square_x = 6
        square_y = 6
        
        # 绘制蓝色小方块
        self.canvas.create_rectangle(
            square_x, square_y,
            square_x + square_size, square_y + square_size,
            fill='#4169E1',  # 皇家蓝
            outline='#1E3A8A',  # 深蓝色边框
            width=2,  # 边框宽度
            tags="car"
        )
        
        # 如果正在移动，添加滚动效果（旋转的小方块）
        if self.direction != 0:
            # 根据方向添加滚动效果线
            line_count = 3
            line_spacing = square_size // (line_count + 1)
            
            for i in range(1, line_count + 1):
                line_x = square_x + i * line_spacing
                
                if self.direction == 1:  # 向右滚动
                    # 向右滚动的斜线
                    self.canvas.create_line(
                        line_x, square_y + 4,
                        line_x + 4, square_y + square_size - 4,
                        fill='#87CEEB',  # 浅蓝色
                        width=1,
                        tags="car"
                    )
                else:  # 向左滚动
                    # 向左滚动的斜线
                    self.canvas.create_line(
                        line_x, square_y + 4,
                        line_x - 4, square_y + square_size - 4,
                        fill='#87CEEB',  # 浅蓝色
                        width=1,
                        tags="car"
                    )
        
        # 添加小方块内部的装饰点
        dot_positions = [
            (square_x + square_size//3, square_y + square_size//3),
            (square_x + 2*square_size//3, square_y + square_size//3),
            (square_x + square_size//3, square_y + 2*square_size//3),
            (square_x + 2*square_size//3, square_y + 2*square_size//3)
        ]
        
        for dot_x, dot_y in dot_positions:
            self.canvas.create_oval(
                dot_x - 2, dot_y - 2,
                dot_x + 2, dot_y + 2,
                fill='#FFFFFF',  # 白色
                outline='#1E3A8A',
                width=1,
                tags="car"
            )
    
    def create_tray_icon(self):
        """创建系统托盘图标"""
        # 创建托盘图标图像
        image = Image.new('RGB', (64, 64), color='white')
        draw = ImageDraw.Draw(image)
        
        # 绘制蓝色小方块图标
        draw.rectangle([20, 20, 44, 44], fill='#4169E1', outline='#1E3A8A', width=2)
        
        # 添加装饰点
        draw.ellipse([26, 26, 30, 30], fill='#FFFFFF', outline='#1E3A8A', width=1)
        draw.ellipse([34, 26, 38, 30], fill='#FFFFFF', outline='#1E3A8A', width=1)
        draw.ellipse([26, 34, 30, 38], fill='#FFFFFF', outline='#1E3A8A', width=1)
        draw.ellipse([34, 34, 38, 38], fill='#FFFFFF', outline='#1E3A8A', width=1)
        
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
            "desktop_pet_car",
            image,
            "桌面宠物小车",
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
        """增加小车速度"""
        self.speed = min(2.0, self.speed + 0.1)  # 最大速度2.0
    
    def decrease_speed(self, icon, item):
        """减小小车速度"""
        self.speed = max(0.1, self.speed - 0.1)  # 最小速度0.1
    
    def random_position(self, icon, item):
        """将小车移动到随机位置（限制在右半边）"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # 限制在右半边
        min_x = screen_width // 2
        max_x = screen_width - self.car_size
        x = random.randint(min_x, max_x)
        
        # 保持在底部菜单栏区域，调整垂直偏移让小车在合适位置
        taskbar_height = 40
        vertical_offset = -5  # 负偏移，让小车更低（原15太高，导致小车埋在菜单栏以下）
        y = screen_height - taskbar_height - self.car_size + vertical_offset
        
        self.window.geometry(f"+{x}+{y}")
        
        # 更新位置变量（50-100范围）
        self.position = 50 + ((x - min_x) / (max_x - min_x)) * 50
    
    def show_about(self, icon, item):
        """显示关于信息"""
        about_window = tk.Toplevel(self.window)
        about_window.title("关于桌面宠物小车")
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
            text="桌面宠物小方块 v2.0.4",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        tk.Label(
            about_window,
            text="一个轻量级的桌面宠物应用\n\n"
                 "蓝色小方块会在你的菜单栏区域滚动\n"
                 "你可以通过系统托盘图标控制它\n\n"
                 "版本: 2.0.4 (蓝色小方块设计)\n"
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
        """动画循环 - 让小车在屏幕右半边偶尔移动"""
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
                    # 调整垂直偏移，让小车在合适位置
                    taskbar_height = 40  # 假设任务栏高度
                    vertical_offset = -5  # 负偏移，让小车更低（原15太高，导致小车埋在菜单栏以下）
                    y_pos = screen_height - taskbar_height - self.car_size + vertical_offset
                    
                    # 更新水平位置（限制在50-100范围内，即右半边）
                    self.position += self.direction * self.speed
                    
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
                        self.direction = 0  # 停止移动，显示正面视角
                        print("停止移动")
                    
                    # 计算实际x坐标（只使用右半边屏幕）
                    max_x = screen_width - self.car_size
                    # 将50-100的位置映射到屏幕右半边的x坐标
                    x_pos = int((self.position - 50) / 50 * (max_x / 2) + (max_x / 2))
                    
                    # 更新窗口位置
                    self.window.geometry(f"+{x_pos}+{y_pos}")
                    
                    # 重绘小车以更新轮子显示
                    self.window.after(0, self.draw_car)
                else:
                    # 不在移动时，确保方向为0（正面视角）
                    if self.direction != 0:
                        self.direction = 0
                        self.window.after(0, self.draw_car)
                
                time.sleep(0.5)  # 降低更新频率，节省资源
                
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
    print("启动桌面宠物小方块 v2.0.4...")
    print("更新: 蓝色小方块在菜单栏上滚来滚去")
    print("修复: 小车启动位置问题（启动时直接出现在右下角菜单栏）")
    print("应用将在系统托盘中运行")
    print("右键点击托盘图标可以控制小车")
    print("=" * 40)
    print("功能特点:")
    print("- 限制在屏幕右半边移动")
    print("- 大约每分钟移动一次")
    print("- 蓝色小方块，简洁美观")
    print("- 移动时有滚动效果")
    print("- 48像素大小，适合菜单栏")
    print("=" * 40)
    
    pet = DesktopPetCar()
    pet.run()

if __name__ == "__main__":
    main()
