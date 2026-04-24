"""移动逻辑模块"""

import random
import time
from utils.logger import info, error, debug


class MovementController:
    """控制机器人移动"""
    
    def __init__(self, config, window_detector=None):
        self.config = config
        self.window_detector = window_detector
        self.position = 75
        self.direction = 0
        self.speed = config.robot.move_speed
        self.is_moving = False
        self.last_move_time = time.time()
        self.target_position = 75
        self._blocked_by_window = False  # 是否被窗口阻挡
        self._screen_x = 0  # 当前屏幕x坐标（像素）
        self._block_retry_count = 0  # 被挡后重试计数
    
    def set_screen_x(self, screen_x):
        """设置当前屏幕x坐标"""
        self._screen_x = screen_x
    
    def update(self, current_time, is_sleeping):
        """更新移动状态，返回是否需要重绘"""
        if is_sleeping:
            if self.is_moving:
                self.is_moving = False
                self.direction = 0
                self._blocked_by_window = False
                info("进入睡眠状态，停止移动")
            return False
        
        redraw_needed = False
        
        # 检查是否应该开始移动
        if not self.is_moving and (current_time - self.last_move_time) > self.config.robot.move_interval:
            self._start_moving(current_time)
            redraw_needed = True
        
        # 如果正在移动，更新位置
        if self.is_moving:
            self._update_position(current_time)
            redraw_needed = True
        
        return redraw_needed
    
    def _start_moving(self, current_time):
        """开始移动"""
        self.is_moving = True
        self.last_move_time = current_time
        self._blocked_by_window = False
        self._block_retry_count = 0
        
        # 被窗口挡住后，允许全屏移动（0-100）
        self.target_position = random.uniform(0, 100)
        self.direction = 1 if self.target_position > self.position else -1
        
        info(f"开始移动: 方向={self.direction}, 目标={self.target_position:.1f}")
    
    def _update_position(self, current_time):
        """更新位置"""
        # 如果被窗口阻挡，不移动
        if self._blocked_by_window:
            return
        
        # 计算新位置
        new_position = self.position + self.direction * self.speed * 0.05
        
        # 检查窗口阻挡（如果有窗口检测器）
        if self.window_detector and self._screen_x > 0:
            robot_size = self.config.robot.robot_size
            screen_width = 1920
            screen_height = 1080
            try:
                import tkinter as tk
                temp = tk.Tk()
                screen_width = temp.winfo_screenwidth()
                screen_height = temp.winfo_screenheight()
                temp.destroy()
            except:
                pass
            
            taskbar_height = 40
            vertical_offset = -5
            y_pos = screen_height - taskbar_height - robot_size + vertical_offset
            
            # 计算新位置的屏幕x（全屏范围0-100）
            max_x = screen_width - robot_size
            new_screen_x = int((new_position - 0) / 100 * max_x)
            
            # 检测路径上是否有窗口
            blocked, stop_x = self.window_detector.get_windows_on_path(
                self._screen_x, y_pos, robot_size, robot_size, self.direction
            )
            
            if blocked:
                # 被窗口阻挡，换方向走
                self._block_retry_count += 1
                self.direction *= -1  # 反向
                
                # 计算停的位置（窗口边缘）
                stop_position = max(0, min(100, (stop_x - 0) / max_x * 100))
                self.position = stop_position
                
                # 设置新目标（反方向）
                if self.direction > 0:
                    self.target_position = random.uniform(stop_position + 5, 100)
                else:
                    self.target_position = random.uniform(0, stop_position - 5)
                
                info(f"窗口阻挡，换方向: 方向={self.direction}, 新目标={self.target_position:.1f}")
                return
        
        # 更新位置
        self.position = new_position
        
        # 检查是否到达目标
        if (self.direction > 0 and self.position >= self.target_position) or \
           (self.direction < 0 and self.position <= self.target_position):
            self.position = self.target_position
            self.is_moving = False
            self.direction = 0
            self._blocked_by_window = False
            info(f"到达目标位置: {self.target_position:.1f}")
        
        # 边界检查（全屏0-100）
        if self.position < 0:
            self.position = 0
            self.direction = 1
        elif self.position > 100:
            self.position = 100
            self.direction = -1
    
    def increase_speed(self):
        """增加速度"""
        self.speed = min(5.0, self.speed + 0.5)
        info(f"速度增加至: {self.speed}")
    
    def decrease_speed(self):
        """减小速度"""
        self.speed = max(0.5, self.speed - 0.5)
        info(f"速度减小至: {self.speed}")
    
    def sync_speed_from_config(self):
        """从配置同步速度"""
        self.speed = self.config.robot.move_speed
