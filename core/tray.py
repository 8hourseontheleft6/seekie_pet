"""系统托盘管理模块"""

import threading
from PIL import Image
import pystray
from pystray import MenuItem as item
from utils.logger import info, error


class TrayManager:
    """管理系统托盘"""
    
    def __init__(self, config):
        self.config = config
        self.icon = None
        self.tray_thread = None
    
    def create(self, callbacks):
        """创建系统托盘图标
        
        Args:
            callbacks: 包含回调函数的字典
                - toggle_visibility: 切换可见性
                - increase_speed: 增加速度
                - decrease_speed: 减小速度
                - open_settings: 打开设置
                - reload_config: 重新加载配置
                - quit: 退出应用
        """
        try:
            # 加载托盘图片
            import os
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            tray_path = os.path.join(current_dir, "main_pic", "robot-icon.png")
            
            if os.path.exists(tray_path):
                tray_image = Image.open(tray_path)
                tray_image = tray_image.resize((64, 64), Image.Resampling.LANCZOS)
                info(f"托盘图标加载成功: {tray_path}")
            else:
                from utils.image_loader import load_tray_image
                tray_image = load_tray_image((64, 64))
                if not tray_image:
                    from PIL import ImageDraw
                    tray_image = Image.new('RGB', (64, 64), color='white')
                    draw = ImageDraw.Draw(tray_image)
                    draw.rectangle([20, 20, 44, 44], fill='#4169E1', outline='#1E3A8A', width=2)
                info("使用默认托盘图标")
            
            # 创建菜单
            menu = (
                item('显示/隐藏', callbacks['toggle_visibility']),
                item('速度加快', callbacks['increase_speed']),
                item('速度减慢', callbacks['decrease_speed']),
                item('---', None),
                item('打开设置', callbacks['open_settings']),
                item('重新加载配置', callbacks['reload_config']),
                item('---', None),
                item('退出', callbacks['quit'])
            )
            
            self.icon = pystray.Icon(
                "desktop_pet_robot",
                tray_image,
                "桌面宠物机器人",
                menu
            )
            
            self.tray_thread = threading.Thread(target=self.icon.run, daemon=True)
            self.tray_thread.start()
            
            info("系统托盘初始化完成")
            
        except Exception as e:
            error(f"系统托盘初始化失败: {e}")
    
    def stop(self):
        """停止系统托盘"""
        if self.icon:
            self.icon.stop()
