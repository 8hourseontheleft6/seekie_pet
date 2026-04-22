"""移动逻辑模块"""

import random
import time
from utils.logger import info, error


class MovementController:
    """控制机器人移动"""
    
    def __init__(self, config):
        self.config = config
        self.position = 75
        self.direction = 0
        self.speed = config.robot.move_speed
        self.is_moving = False
        self.last_move_time = time.time()
        self.target_position = 75
    
    def update(self, current_time, is_sleeping):
        """更新移动状态，返回是否需要重绘"""
        if is_sleeping:
            if self.is_moving:
                self.is_moving = False
                self.direction = 0
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
        
        self.target_position = random.uniform(50, 100)
        self.direction = 1 if self.target_position > self.position else -1
        
        info(f"开始移动: 方向={self.direction}, 目标={self.target_position:.1f}")
    
    def _update_position(self, current_time):
        """更新位置"""
        self.position += self.direction * self.speed * 0.05
        
        # 检查是否到达目标
        if (self.direction > 0 and self.position >= self.target_position) or \
           (self.direction < 0 and self.position <= self.target_position):
            self.position = self.target_position
            self.is_moving = False
            self.direction = 0
            info(f"到达目标位置: {self.target_position:.1f}")
        
        # 边界检查
        if self.position < 50:
            self.position = 50
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
