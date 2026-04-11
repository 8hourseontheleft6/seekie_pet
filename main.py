#!/usr/bin/env python3
"""
桌面宠物小车 - 二轮小车在菜单栏上移动
一个轻量级的桌面宠物应用，显示一个二轮小车在系统托盘区域移动
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
        self.position = 0  # 小车在菜单栏上的位置 (0-100)
        self.direction = 1  # 移动方向: 1=向右, -1=向左
        self.speed = 2  # 移动速度
        self.car_size = 32  # 小车大小
        
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
        
        # 设置窗口大小和位置
        self.window.geometry(f"{self.car_size}x{self.car_size}+100+100")
        
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
    
    def draw_car(self):
        """在画布上绘制二轮小车"""
        self.canvas.delete("all")
        
        # 小车主体 (矩形)
        body_width = self.car_size - 10
        body_height = self.car_size // 2
        body_x = 5
        body_y = (self.car_size - body_height) // 2
        
        # 绘制车身
        self.canvas.create_rectangle(
            body_x, body_y,
            body_x + body_width, body_y + body_height,
            fill='#FF6B6B',  # 红色
            outline='#CC5555',
            width=2,
            tags="car"
        )
        
        # 绘制车轮
        wheel_radius = 6
        wheel_y = body_y + body_height + 2
        
        # 左轮
        self.canvas.create_oval(
            body_x + 5, wheel_y - wheel_radius,
            body_x + 5 + wheel_radius*2, wheel_y + wheel_radius,
            fill='#333333',  # 黑色
            outline='#000000',
            width=1,
            tags="car"
        )
        
        # 右轮
        self.canvas.create_oval(
            body_x + body_width - 5 - wheel_radius*2, wheel_y - wheel_radius,
            body_x + body_width - 5, wheel_y + wheel_radius,
            fill='#333333',  # 黑色
            outline='#000000',
            width=1,
            tags="car"
        )
        
        # 绘制车窗
        window_width = body_width // 3
        window_height = body_height // 2
        window_x = body_x + body_width - window_width - 5
        window_y = body_y + 5
        
        self.canvas.create_rectangle(
            window_x, window_y,
            window_x + window_width, window_y + window_height,
            fill='#87CEEB',  # 天蓝色
            outline='#5D9BBA',
            width=1,
            tags="car"
        )
    
    def create_tray_icon(self):
        """创建系统托盘图标"""
        # 创建托盘图标图像
        image = Image.new('RGB', (64, 64), color='white')
        draw = ImageDraw.Draw(image)
        
        # 绘制小车图标
        draw.rectangle([10, 20, 54, 40], fill='#FF6B6B', outline='#CC5555', width=2)
        draw.ellipse([15, 45, 25, 55], fill='#333333', outline='#000000', width=1)
        draw.ellipse([39, 45, 49, 55], fill='#333333', outline='#000000', width=1)
        draw.rectangle([40, 22, 50, 30], fill='#87CEEB', outline='#5D9BBA', width=1)
        
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
        self.speed = min(10, self.speed + 1)
    
    def decrease_speed(self, icon, item):
        """减小小车速度"""
        self.speed = max(1, self.speed - 1)
    
    def random_position(self, icon, item):
        """将小车移动到随机位置"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = random.randint(0, screen_width - self.car_size)
        y = random.randint(0, screen_height - self.car_size)
        
        self.window.geometry(f"+{x}+{y}")
    
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
            text="桌面宠物小车",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        tk.Label(
            about_window,
            text="一个轻量级的桌面宠物应用\n\n"
                 "二轮小车会在你的菜单栏区域移动\n"
                 "你可以通过系统托盘图标控制它\n\n"
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
        sys.exit(0)
    
    def animate(self):
        """动画循环 - 让小车在屏幕边缘移动"""
        while self.running:
            try:
                # 获取屏幕尺寸
                screen_width = self.window.winfo_screenwidth()
                screen_height = self.window.winfo_screenheight()
                
                # 计算新位置 (在屏幕底部边缘移动，模拟菜单栏)
                taskbar_height = 40  # 假设任务栏高度
                y_pos = screen_height - taskbar_height - self.car_size
                
                # 更新水平位置
                self.position += self.direction * self.speed
                
                # 边界检查
                if self.position <= 0:
                    self.position = 0
                    self.direction = 1  # 向右转
                elif self.position >= 100:
                    self.position = 100
                    self.direction = -1  # 向左转
                
                # 计算实际x坐标
                max_x = screen_width - self.car_size
                x_pos = int(self.position / 100 * max_x)
                
                # 更新窗口位置
                self.window.geometry(f"+{x_pos}+{y_pos}")
                
                # 偶尔随机改变方向
                if random.random() < 0.01:  # 1% 的几率
                    self.direction *= -1
                
                # 重绘小车 (偶尔)
                if random.random() < 0.05:  # 5% 的几率
                    self.window.after(0, self.draw_car)
                
                time.sleep(0.05)  # 控制动画速度
                
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
    print("启动桌面宠物小车...")
    print("应用将在系统托盘中运行")
    print("右键点击托盘图标可以控制小车")
    
    pet = DesktopPetCar()
    pet.run()

if __name__ == "__main__":
    main()
