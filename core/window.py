"""窗口管理模块"""

import tkinter as tk
from utils.logger import info, error


class WindowManager:
    """管理机器人窗口"""
    
    def __init__(self, config):
        self.config = config
        self.window = None
        self.canvas = None
    
    def create_window(self):
        """创建并初始化窗口"""
        try:
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
                width=self.config.robot.robot_size,
                height=self.config.robot.robot_size,
                highlightthickness=0,
                bg='black'
            )
            self.canvas.pack()
            
            # 设置透明色
            self.window.attributes('-transparentcolor', 'black')
            
            # 设置初始位置（右下角）
            self._set_initial_position()
            
            info("窗口初始化完成")
            return self.window, self.canvas
            
        except Exception as e:
            error(f"窗口初始化失败: {e}")
            raise
    
    def _set_initial_position(self):
        """设置窗口初始位置到右下角"""
        if not self.window:
            return
        
        try:
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            
            car_size = self.config.robot.robot_size
            taskbar_height = 40
            vertical_offset = -5
            
            # 初始位置在右下角（位置75对应中间偏右）
            initial_position = 75
            if self.config.behavior.move_only_on_right_side:
                max_x = screen_width - car_size
                x_pos = int((initial_position - 50) / 50 * (max_x / 2) + (max_x / 2))
            else:
                max_x = screen_width - car_size
                x_pos = int((initial_position - 50) / 50 * max_x)
            
            y_pos = screen_height - taskbar_height - car_size + vertical_offset
            
            self.window.geometry(f"+{x_pos}+{y_pos}")
            info(f"窗口初始位置设置: x={x_pos}, y={y_pos}")
        except Exception as e:
            error(f"设置初始位置失败: {e}")
    
    def update_position(self, position):
        """更新窗口位置"""
        if not self.window:
            return
        
        try:
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            
            car_size = self.config.robot.robot_size
            taskbar_height = 40
            vertical_offset = -5
            
            if self.config.behavior.move_only_on_right_side:
                max_x = screen_width - car_size
                x_pos = int((position - 50) / 50 * (max_x / 2) + (max_x / 2))
            else:
                max_x = screen_width - car_size
                x_pos = int((position - 50) / 50 * max_x)
            
            y_pos = screen_height - taskbar_height - car_size + vertical_offset
            
            self.window.after(0, lambda: self.window.geometry(f"+{x_pos}+{y_pos}"))
        except Exception as e:
            pass
    
    def bind_mouse_events(self, on_enter, on_leave):
        """绑定鼠标事件"""
        if self.canvas:
            self.canvas.bind("<Enter>", on_enter)
            self.canvas.bind("<Leave>", on_leave)
    
    def draw(self, photo):
        """绘制图片到画布"""
        if not self.canvas or not photo:
            return
        
        self.canvas.delete("all")
        self.canvas.create_image(
            self.config.robot.robot_size // 2,
            self.config.robot.robot_size // 2,
            image=photo
        )
    
    def toggle_visibility(self):
        """切换窗口可见性"""
        if not self.window:
            return
        
        if self.window.winfo_viewable():
            self.window.withdraw()
            info("窗口隐藏")
        else:
            self.window.deiconify()
            info("窗口显示")
    
    def run(self):
        """运行窗口主循环"""
        if self.window:
            self.window.mainloop()
    
    def quit(self):
        """退出窗口"""
        if self.window:
            self.window.quit()
