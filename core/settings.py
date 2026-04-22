"""设置窗口管理模块"""

import threading
import os
import sys
from utils.logger import info, error


class SettingsManager:
    """管理设置窗口"""
    
    def __init__(self):
        self.settings_window = None
    
    def open(self):
        """打开设置窗口"""
        try:
            # 避免重复打开
            if self.settings_window:
                try:
                    self.settings_window.window.lift()
                    self.settings_window.window.focus_force()
                    return
                except:
                    pass
            
            thread = threading.Thread(target=self._open_thread, daemon=True)
            thread.start()
        except Exception as e:
            error(f"打开设置窗口失败: {e}")
    
    def _open_thread(self):
        """在线程中打开设置窗口"""
        try:
            web_settings_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'web_settings')
            if os.path.exists(web_settings_dir):
                sys.path.insert(0, web_settings_dir)
                try:
                    from web_settings import open_web_settings
                    open_web_settings()
                    info("Web设置窗口已打开")
                    return
                except ImportError as e:
                    error(f"导入Web设置窗口失败: {e}")
            
            # 回退到现代化设置窗口
            self._fallback_to_modern()
            
        except Exception as e:
            error(f"打开设置窗口线程失败: {e}")
            self._fallback_to_modern()
    
    def _fallback_to_modern(self):
        """回退到现代化设置窗口"""
        try:
            from settings_window_v2 import open_modern_settings_window
            open_modern_settings_window()
            info("现代化设置窗口已打开")
        except Exception as e:
            error(f"打开现代化设置窗口失败: {e}")
