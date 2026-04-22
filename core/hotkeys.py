"""快捷键管理模块"""

import subprocess
import keyboard
from utils.logger import info, error, warning


class HotkeyManager:
    """管理全局快捷键"""
    
    def __init__(self, config):
        self.config = config
        self._registered = False
    
    def register_all(self):
        """注册所有快捷键"""
        try:
            if self.config.hotkeys.screenshot:
                keyboard.add_hotkey(self.config.hotkeys.screenshot, self._take_screenshot)
                info(f"快捷键注册成功: {self.config.hotkeys.screenshot} - 打开截图软件")
            
            if self.config.hotkeys.toggle_visibility:
                keyboard.add_hotkey(self.config.hotkeys.toggle_visibility, 
                                    lambda: info("切换可见性快捷键触发"))
            
            self._registered = True
            
        except Exception as e:
            error(f"快捷键注册失败: {e}")
    
    def unregister_all(self):
        """注销所有快捷键"""
        try:
            keyboard.unhook_all()
            self._registered = False
        except:
            pass
    
    def _take_screenshot(self):
        """执行截图操作"""
        try:
            info(f"检测到{self.config.hotkeys.screenshot}快捷键，正在打开截图软件...")
            
            methods = [
                (["SnippingTool.exe"], "Windows截图工具"),
                (lambda: keyboard.press_and_release('print screen'), "PrintScreen键"),
                (lambda: keyboard.press_and_release('windows+shift+s'), "Win+Shift+S快捷键"),
                (["mspaint.exe"], "画图工具")
            ]
            
            for method, name in methods:
                try:
                    if callable(method):
                        method()
                    else:
                        subprocess.Popen(method)
                    info(f"已启动: {name}")
                    return
                except:
                    continue
            
            warning("无法打开截图软件，请确保系统支持截图功能")
            
        except Exception as e:
            error(f"截图操作失败: {e}")
