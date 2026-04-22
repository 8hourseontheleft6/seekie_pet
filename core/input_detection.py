"""输入检测模块"""

import time
from ctypes import windll, Structure, c_ulong, byref
from utils.logger import info, error


class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_ulong),
        ('dwTime', c_ulong)
    ]


class InputDetector:
    """检测系统输入活动"""
    
    def __init__(self, config):
        self.config = config
        self.is_sleeping = False
    
    def get_idle_time(self):
        """获取系统空闲时间（秒）"""
        try:
            lastInputInfo = LASTINPUTINFO()
            lastInputInfo.cbSize = c_ulong(8)
            
            if windll.user32.GetLastInputInfo(byref(lastInputInfo)):
                current_time = windll.kernel32.GetTickCount()
                return (current_time - lastInputInfo.dwTime) // 1000
            return 0
        except:
            return 0
    
    def check_activity(self):
        """检查输入活动，返回是否从睡眠状态变化"""
        if not self.config.behavior.enable_input_detection:
            return False
        
        idle_time = self.get_idle_time()
        was_sleeping = self.is_sleeping
        
        if idle_time == 0:
            if self.is_sleeping:
                info("检测到输入活动，从睡眠状态唤醒")
                self.is_sleeping = False
        else:
            if not self.is_sleeping and idle_time > self.config.behavior.inactivity_threshold:
                info(f"系统{idle_time}秒无输入活动，进入睡眠状态")
                self.is_sleeping = True
        
        return was_sleeping != self.is_sleeping
