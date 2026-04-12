#!/usr/bin/env python3
"""
桌面宠物机器人 - 重构版
一个轻量级的桌面宠物应用，机器人在菜单栏上移动

版本: 3.0.1 重构版
功能: 只保留核心功能，简化代码结构
"""

import tkinter as tk
import threading
import time
import random
import os
from PIL import Image, ImageDraw, ImageTk
import pystray
from pystray import MenuItem as item

class DesktopPet:
    """桌面宠物机器人 - 重构版"""
    
    # 配置常量
    CAR_SIZE = 50
    INITIAL_POSITION = 75
    INITIAL_SPEED = 1.5
    MOVE_INTERVAL = 20
    MIN_SPEED = 0.5
    MAX_SPEED = 5.0
    SPEED_INCREMENT = 0.5
    TASKBAR_HEIGHT = 40
    VERTICAL_OFFSET = -5
    
    def __init__(self):
        self.window = None
        self.canvas = None
        self.icon = None
        self.running = True
        
        # 状态变量
        self.position = self.INITIAL_POSITION
        self.direction = 0
        self.speed = self.INITIAL_SPEED
        self.is_moving = False
        self.move_end_time = 0
        self.last_move_time = time.time()
        
        # 图片资源
        self.robot_image = None
        self.robot_photo = None
        
        # 初始化
        self._create_window()
        self._load_robot_image()
        self._create_tray_icon()
        
        # 启动动画线程
        self.animation_thread = threading.Thread(target=self._animation_loop, daemon=True)
        self.animation_thread.start()
    
    def _load_robot_image(self):
        """加载机器人图片"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "main_pic", "Robot_50x50.png")
            
            print(f"加载图片: {image_path}")
            print(f"文件存在: {os.path.exists(image_path)}")
            
            if os.path.exists(image_path):
                self.robot_image = Image.open(image_path)
                print("✓ 图片加载成功")
            else:
                print("⚠ 图片不存在，使用后备图标")
                self.robot_image = self._create_fallback_image()
        except Exception as e:
            print(f"✗ 加载图片错误: {e}")
            self.robot_image = self._create_fallback_image()
        
        # 转换为Tkinter格式
        self.robot_photo = ImageTk.PhotoImage(self.robot_image)
        self._draw_robot()
    
    def _create_fallback_image(self):
        """创建后备图标"""
        img = Image.new('RGBA', (self.CAR_SIZE, self.CAR_SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([10, 10, 40, 40], fill='#4169E1', outline='#1E3A8A', width=2)
        draw.rectangle([15, 15, 25, 25], fill='#FFFFFF', outline='#1E3A8A', width=1)
        draw.rectangle([30, 15, 35, 20], fill='#FF6B6B', outline='#CC5555', width=1)
        return img
    
    def _create_window(self):
        """创建透明窗口"""
        self.window = tk.Tk()
        self.window.title("桌面宠物机器人")
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        
        # 设置透明度
        try:
            self.window.attributes('-alpha', 0.99)
        except:
            pass
        
        # 创建画布
        self.canvas = tk.Canvas(
            self.window,
            width=self.CAR_SIZE,
            height=self.CAR_SIZE,
            highlightthickness=0,
            bg='black'
        )
        self.canvas.pack()
        
        # 设置透明色
        self.window.attributes('-transparentcolor', 'black')
        
        # 设置初始位置
        self._update_window_position()
    
    def _update_window_position(self):
        """更新窗口位置"""
        if not self.window:
            return
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # 限制在右半边
        max_x = screen_width - self.CAR_SIZE
        x_pos = int((self.position - 50) / 50 * (max_x / 2) + (max_x / 2))
        y_pos = screen_height - self.TASKBAR_HEIGHT - self.CAR_SIZE + self.VERTICAL_OFFSET
        
        self.window.geometry(f"+{x_pos}+{y_pos}")
    
    def _draw_robot(self):
        """绘制机器人"""
        if not self.canvas or not self.robot_photo:
            return
        
        self.canvas.delete("all")
        self.canvas.create_image(
            self.CAR_SIZE // 2,
            self.CAR_SIZE // 2,
            image=self.robot_photo,
            tags="robot"
        )
    
    def _create_tray_icon(self):
        """创建系统托盘图标"""
        if not self.robot_image:
            tray_image = Image.new('RGB', (64, 64), color='white')
            draw = ImageDraw.Draw(tray_image)
            draw.rectangle([20, 20, 44, 44], fill='#4169E1', outline='#1E3A8A', width=2)
        else:
            tray_image = self.robot_image.resize((64, 64), Image.Resampling.LANCZOS)
        
        # 简化菜单
        menu = (
            item('显示/隐藏', self._toggle_visibility),
            item('速度加快', self._increase_speed),
            item('速度减慢', self._decrease_speed),
            item('退出', self._quit_app)
        )
        
        self.icon = pystray.Icon(
            "desktop_pet_robot",
            tray_image,
            "桌面宠物机器人",
            menu
        )
        
        self.tray_thread = threading.Thread(target=self.icon.run, daemon=True)
        self.tray_thread.start()
    
    def _toggle_visibility(self, icon, item):
        """切换窗口可见性"""
        if self.window.winfo_viewable():
            self.window.withdraw()
        else:
            self.window.deiconify()
    
    def _increase_speed(self, icon, item):
        """增加速度"""
        self.speed = min(self.MAX_SPEED, self.speed + self.SPEED_INCREMENT)
    
    def _decrease_speed(self, icon, item):
        """减小速度"""
        self.speed = max(self.MIN_SPEED, self.speed - self.SPEED_INCREMENT)
    
    def _quit_app(self, icon, item):
        """退出应用"""
        self.running = False
        if self.icon:
            self.icon.stop()
        if self.window:
            self.window.quit()
    
    def _animation_loop(self):
        """动画循环"""
        while self.running:
            try:
                current_time = time.time()
                
                # 检查是否应该开始移动
                if not self.is_moving and (current_time - self.last_move_time) > self.MOVE_INTERVAL:
                    self._start_moving(current_time)
                
                # 如果正在移动，更新位置
                if self.is_moving:
                    self._update_movement(current_time)
                
                time.sleep(0.05)  # 20FPS
                
            except Exception as e:
                print(f"动画错误: {e}")
                time.sleep(1)
    
    def _start_moving(self, current_time):
        """开始移动"""
        self.is_moving = True
        self.last_move_time = current_time
        
        move_duration = random.uniform(5, 15)
        self.move_end_time = current_time + move_duration
        
        target = random.uniform(50, 100)
        self.direction = 1 if target > self.position else -1
        
        print(f"开始移动: 方向={self.direction}, 目标={target:.1f}")
    
    def _update_movement(self, current_time):
        """更新移动"""
        # 更新位置
        self.position += self.direction * self.speed * 0.05
        
        # 边界检查
        if self.position < 50:
            self.position = 50
            self.direction = 1
        elif self.position > 100:
            self.position = 100
            self.direction = -1
        
        # 检查是否到达移动结束时间
        if current_time > self.move_end_time:
            self.is_moving = False
            self.direction = 0
            print("停止移动")
        
        # 更新窗口位置
        self._update_window_position()
        
        # 重绘机器人
        self.window.after(0, self._draw_robot)
    
    def run(self):
        """运行应用"""
        try:
            self.window.mainloop()
        except KeyboardInterrupt:
            self._quit_app(None, None)

def main():
    """主函数"""
    print("=" * 50)
    print("桌面宠物机器人 v3.0.1 重构版")
    print("=" * 50)
    print("功能特点:")
    print("- 限制在屏幕右半边移动")
    print("- 大约每20秒移动一次")
    print("- 使用Robot.png图片")
    print("- 高帧率流畅动画 (20FPS)")
    print("- 50x50像素大小，适合菜单栏")
    print("=" * 50)
    print("应用将在系统托盘中运行")
    print("右键点击托盘图标可以控制机器人")
    print("=" * 50)
    
    pet = DesktopPet()
    pet.run()

if __name__ == "__main__":
    main()
