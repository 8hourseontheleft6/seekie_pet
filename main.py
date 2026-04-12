#!/usr/bin/env python3
"""
桌面宠物机器人 - 最终版
机器人在菜单栏上移动，检测用户鼠标和键盘活动

版本: 3.0.4 (输入活动检测版)
功能: 检测鼠标和键盘活动，10秒无活动则进入睡眠状态
"""

import tkinter as tk
import threading
import time
import random
import os
from PIL import Image, ImageDraw, ImageTk
import pystray
from pystray import MenuItem as item
from ctypes import windll, Structure, c_ulong, byref

# ==================== 配置常量 ====================
CAR_SIZE = 50
INITIAL_POSITION = 75
INITIAL_SPEED = 1.5
MOVE_INTERVAL = 20
MIN_SPEED = 0.5
MAX_SPEED = 5.0
SPEED_INCREMENT = 0.5
TASKBAR_HEIGHT = 40
VERTICAL_OFFSET = -5
INACTIVITY_THRESHOLD = 10  # 10秒无输入活动进入睡眠

class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_ulong),
        ('dwTime', c_ulong)
    ]

class DesktopPetCar:
    def __init__(self):
        self.window = None
        self.canvas = None
        self.icon = None
        self.running = True
        
        # 状态变量
        self.position = INITIAL_POSITION
        self.direction = 0
        self.speed = INITIAL_SPEED
        self.is_moving = False
        self.move_end_time = 0
        self.last_move_time = time.time()
        
        # 输入活动检测
        self.last_input_time = self._get_last_input_time()
        self.is_sleeping = False
        
        # 图片资源
        self.robot_image = None
        self.robot_photo = None
        self.sleep_image = None
        self.sleep_photo = None
        
        # 初始化
        self._init_window()
        self._load_images()
        self._init_tray()
        
        # 启动线程
        self._start_threads()
    
    # ==================== 初始化方法 ====================
    
    def _init_window(self):
        """初始化透明窗口"""
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
            width=CAR_SIZE,
            height=CAR_SIZE,
            highlightthickness=0,
            bg='black'
        )
        self.canvas.pack()
        
        # 设置透明色
        self.window.attributes('-transparentcolor', 'black')
        
        # 设置初始位置
        self._update_window_position()
    
    def _load_images(self):
        """加载机器人图片和睡眠图片"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 加载机器人图片
        robot_path = os.path.join(current_dir, "main_pic", "Robot_50x50.png")
        print(f"加载机器人图片: {robot_path}")
        
        if os.path.exists(robot_path):
            self.robot_image = Image.open(robot_path)
            print("✓ 机器人图片加载成功")
        else:
            print("⚠ 机器人图片不存在，使用后备图标")
            self.robot_image = self._create_robot_image()
        
        # 加载睡眠图片
        sleep_path = os.path.join(current_dir, "main_pic", "Sleep.png")
        print(f"加载睡眠图片: {sleep_path}")
        
        if os.path.exists(sleep_path):
            self.sleep_image = Image.open(sleep_path)
            print("✓ 睡眠图片加载成功")
        else:
            print("⚠ 睡眠图片不存在，创建后备睡眠图标")
            self.sleep_image = self._create_sleep_image()
        
        # 转换为Tkinter格式
        self.robot_photo = ImageTk.PhotoImage(self.robot_image)
        self.sleep_photo = ImageTk.PhotoImage(self.sleep_image)
        
        # 初始绘制
        self._draw_current()
    
    def _create_robot_image(self):
        """创建后备机器人图标"""
        img = Image.new('RGBA', (CAR_SIZE, CAR_SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([10, 10, 40, 40], fill='#4169E1', outline='#1E3A8A', width=2)
        draw.rectangle([15, 15, 25, 25], fill='#FFFFFF', outline='#1E3A8A', width=1)
        draw.rectangle([30, 15, 35, 20], fill='#FF6B6B', outline='#CC5555', width=1)
        return img
    
    def _create_sleep_image(self):
        """创建后备睡眠图标"""
        img = Image.new('RGBA', (CAR_SIZE, CAR_SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制睡眠状态的机器人（闭眼）
        draw.rectangle([10, 10, 40, 40], fill='#4169E1', outline='#1E3A8A', width=2)
        
        # 闭眼（两条横线）
        draw.rectangle([15, 17, 25, 19], fill='#FFFFFF', outline='#1E3A8A', width=1)
        draw.rectangle([30, 17, 35, 19], fill='#FFFFFF', outline='#CC5555', width=1)
        
        # ZZZ睡眠符号
        draw.text((20, 30), "Zz", fill='#FFFFFF', font=None)
        
        return img
    
    def _init_tray(self):
        """初始化系统托盘"""
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
            "桌面宠物机器人 (输入检测版)",
            menu
        )
        
        self.tray_thread = threading.Thread(target=self.icon.run, daemon=True)
        self.tray_thread.start()
    
    def _start_threads(self):
        """启动所有线程"""
        self.animation_thread = threading.Thread(target=self._animation_loop, daemon=True)
        self.input_detection_thread = threading.Thread(target=self._input_detection_loop, daemon=True)
        
        self.animation_thread.start()
        self.input_detection_thread.start()
    
    # ==================== 输入活动检测方法 ====================
    
    def _get_last_input_time(self):
        """获取系统最后输入时间（毫秒）"""
        try:
            lastInputInfo = LASTINPUTINFO()
            lastInputInfo.cbSize = c_ulong(8)  # 结构体大小
            
            if windll.user32.GetLastInputInfo(byref(lastInputInfo)):
                return lastInputInfo.dwTime
            else:
                return 0
        except:
            return 0
    
    def _get_idle_time(self):
        """获取系统空闲时间（秒）"""
        try:
            last_input = self._get_last_input_time()
            current_time = windll.kernel32.GetTickCount()
            
            if last_input == 0:
                return 0
            
            idle_time = (current_time - last_input) // 1000  # 转换为秒
            return idle_time
        except:
            return 0
    
    def _check_input_activity(self):
        """检查输入活动"""
        idle_time = self._get_idle_time()
        
        # 检查是否有输入活动
        if idle_time == 0:
            # 有输入活动
            if self.is_sleeping:
                print("检测到输入活动，从睡眠状态唤醒")
                self.is_sleeping = False
                self._draw_current()
        else:
            # 检查是否应该进入睡眠状态
            if not self.is_sleeping and idle_time > INACTIVITY_THRESHOLD:
                print(f"系统{idle_time}秒无输入活动，进入睡眠状态")
                self.is_sleeping = True
                self._draw_current()
    
    def _input_detection_loop(self):
        """输入检测循环"""
        print("启动输入活动检测...")
        print(f"检测阈值: {INACTIVITY_THRESHOLD}秒无输入活动进入睡眠")
        print("检测类型: 鼠标和键盘活动")
        
        while self.running:
            try:
                self._check_input_activity()
                time.sleep(1)  # 每秒检查一次
            except Exception as e:
                print(f"输入检测错误: {e}")
                time.sleep(5)
    
    # ==================== 核心功能方法 ====================
    
    def _update_window_position(self):
        """更新窗口位置"""
        if not self.window:
            return
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # 限制在右半边
        max_x = screen_width - CAR_SIZE
        x_pos = int((self.position - 50) / 50 * (max_x / 2) + (max_x / 2))
        y_pos = screen_height - TASKBAR_HEIGHT - CAR_SIZE + VERTICAL_OFFSET
        
        self.window.geometry(f"+{x_pos}+{y_pos}")
    
    def _draw_current(self):
        """绘制当前状态（机器人或睡眠）"""
        if not self.canvas:
            return
        
        self.canvas.delete("all")
        
        if self.is_sleeping:
            # 绘制睡眠图片
            if self.sleep_photo:
                self.canvas.create_image(
                    CAR_SIZE // 2,
                    CAR_SIZE // 2,
                    image=self.sleep_photo,
                    tags="sleep"
                )
        else:
            # 绘制机器人图片
            if self.robot_photo:
                self.canvas.create_image(
                    CAR_SIZE // 2,
                    CAR_SIZE // 2,
                    image=self.robot_photo,
                    tags="robot"
                )
    
    # ==================== 控制方法 ====================
    
    def _toggle_visibility(self, icon, item):
        """切换窗口可见性"""
        if self.window.winfo_viewable():
            self.window.withdraw()
        else:
            self.window.deiconify()
    
    def _increase_speed(self, icon, item):
        """增加速度"""
        self.speed = min(MAX_SPEED, self.speed + SPEED_INCREMENT)
    
    def _decrease_speed(self, icon, item):
        """减小速度"""
        self.speed = max(MIN_SPEED, self.speed - SPEED_INCREMENT)
    
    def _quit_app(self, icon, item):
        """退出应用"""
        self.running = False
        if self.icon:
            self.icon.stop()
        if self.window:
            self.window.quit()
    
    # ==================== 动画循环方法 ====================
    
    def _animation_loop(self):
        """动画循环"""
        while self.running:
            try:
                current_time = time.time()
                
                # 只有在非睡眠状态时才检查移动
                if not self.is_sleeping:
                    # 检查是否应该开始移动
                    if not self.is_moving and (current_time - self.last_move_time) > MOVE_INTERVAL:
                        self._start_moving(current_time)
                    
                    # 如果正在移动，更新位置
                    if self.is_moving:
                        self._update_movement(current_time)
                else:
                    # 睡眠状态下停止移动
                    if self.is_moving:
                        self.is_moving = False
                        self.direction = 0
                        print("进入睡眠状态，停止移动")
                
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
        self.window.after(0, self._draw_current)
    
    # ==================== 公共方法 ====================
    
    def run(self):
        """运行应用"""
        try:
            self.window.mainloop()
        except KeyboardInterrupt:
            self._quit_app(None, None)

# ==================== 主函数 ====================

def main():
    """主函数"""
    print_header()
    
    pet = DesktopPetCar()
    pet.run()

def print_header():
    """打印程序头信息"""
    print("=" * 50)
    print("桌面宠物机器人 v3.0.4 (输入活动检测版)")
    print("=" * 50)
    print("功能特点:")
    print("- 检测鼠标和键盘活动，10秒无活动进入睡眠")
    print("- 睡眠状态下显示Sleep.png图片")
    print("- 输入活动后自动唤醒")
    print("- 限制在屏幕右半边移动")
    print("- 大约每20秒移动一次")
    print("=" * 50)
    print("应用将在系统托盘中运行")
    print("右键点击托盘图标可以控制机器人")
    print("=" * 50)

if __name__ == "__main__":
    main()
