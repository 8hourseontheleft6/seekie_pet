"""窗口检测模块 - 检测路径上的窗口，避免穿过"""

import ctypes
from ctypes import wintypes
from utils.logger import info, debug, error

# Windows API 常量
HWND_TOPMOST = -1
SW_SHOWNA = 8

# 窗口样式常量
WS_VISIBLE = 0x10000000
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

# 窗口矩形结构
class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]

# 加载user32
user32 = ctypes.windll.user32


def get_visible_windows():
    """获取所有可见窗口的矩形区域"""
    windows = []
    
    def enum_callback(hwnd, lparam):
        if not user32.IsWindowVisible(hwnd):
            return True
        
        # 跳过桌面和任务栏
        length = user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return True
        
        # 获取窗口标题
        title_buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, title_buffer, length + 1)
        title = title_buffer.value
        
        # 跳过无标题或系统窗口
        if not title or title in ("", "Program Manager", "桌面"):
            return True
        
        # 获取窗口矩形
        rect = RECT()
        if user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            # 跳过最小化窗口（位置在屏幕外）
            if rect.left < -32000 or rect.top < -32000:
                return True
            
            # 跳过太小的窗口（可能是托盘图标等）
            width = rect.right - rect.left
            height = rect.bottom - rect.top
            if width < 100 or height < 50:
                return True
            
            windows.append({
                'hwnd': hwnd,
                'title': title,
                'left': rect.left,
                'top': rect.top,
                'right': rect.right,
                'bottom': rect.bottom,
                'width': width,
                'height': height,
            })
        
        return True
    
    # 枚举窗口
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(WNDENUMPROC(enum_callback), 0)
    
    return windows


class WindowDetector:
    """窗口检测器 - 检测机器人路径上的窗口"""
    
    def __init__(self, config):
        self.config = config
        self._last_windows = []  # 缓存上次检测结果
        self._cache_time = 0
        self._cache_duration = 0.5  # 缓存0.5秒
    
    def get_windows_on_path(self, robot_x, robot_y, robot_width, robot_height, direction):
        """
        检测机器人移动路径上是否有窗口
        
        参数:
            robot_x: 机器人当前x坐标（屏幕像素）
            robot_y: 机器人当前y坐标（屏幕像素）
            robot_width: 机器人宽度
            robot_height: 机器人高度
            direction: 移动方向（1=右, -1=左）
        
        返回:
            (blocked, stop_x) - (是否被阻挡, 应停止的x坐标)
        """
        import time
        current_time = time.time()
        
        # 使用缓存
        if current_time - self._cache_time < self._cache_duration:
            windows = self._last_windows
        else:
            windows = get_visible_windows()
            self._last_windows = windows
            self._cache_time = current_time
        
        # 机器人区域
        robot_left = robot_x
        robot_right = robot_x + robot_width
        robot_top = robot_y
        robot_bottom = robot_y + robot_height
        
        # 检查每个窗口是否在路径上
        for win in windows:
            # 跳过完全在机器人后面的窗口
            if direction > 0 and win['right'] <= robot_left:
                continue  # 窗口在左边，向右移动不撞
            if direction < 0 and win['left'] >= robot_right:
                continue  # 窗口在右边，向左移动不撞
            
            # 检查垂直重叠（窗口和机器人在同一高度范围）
            vertical_overlap = (
                win['top'] < robot_bottom and 
                win['bottom'] > robot_top
            )
            
            if not vertical_overlap:
                continue
            
            # 检查水平重叠
            if direction > 0:
                # 向右移动：窗口在机器人右边且重叠
                if win['left'] > robot_left and win['left'] < robot_right + 200:
                    # 窗口在路径上，停在窗口左边
                    stop_x = win['left'] - robot_width - 5  # 留5像素间距
                    debug(f"窗口阻挡向右移动: '{win['title']}' at x={win['left']}, 停在x={stop_x}")
                    return True, stop_x
            else:
                # 向左移动：窗口在机器人左边且重叠
                if win['right'] < robot_right and win['right'] > robot_left - 200:
                    # 窗口在路径上，停在窗口右边
                    stop_x = win['right'] + 5  # 留5像素间距
                    debug(f"窗口阻挡向左移动: '{win['title']}' at x={win['right']}, 停在x={stop_x}")
                    return True, stop_x
        
        return False, None
    
    def is_window_blocking(self, robot_x, robot_y, robot_width, robot_height):
        """检查机器人当前位置是否被窗口覆盖（被压在下面）"""
        windows = get_visible_windows()
        
        robot_left = robot_x
        robot_right = robot_x + robot_width
        robot_top = robot_y
        robot_bottom = robot_y + robot_height
        
        for win in windows:
            # 检查窗口是否覆盖机器人位置
            if (win['left'] < robot_right and 
                win['right'] > robot_left and 
                win['top'] < robot_bottom and 
                win['bottom'] > robot_top):
                return True, win
        
        return False, None
