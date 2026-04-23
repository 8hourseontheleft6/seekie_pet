"""机器人主类 - 整合所有模块"""

import time
import threading
from utils.logger import info, error, debug
from config.config_manager import get_config_manager, get_config
from core.window import WindowManager
from core.animation import AnimationManager
from core.movement import MovementController
from core.input_detection import InputDetector
from core.hotkeys import HotkeyManager
from core.tray import TrayManager
from core.settings import SettingsManager


class DesktopPetRobot:
    """桌面宠物机器人 - 整合所有模块"""
    
    def __init__(self):
        self.config_manager = get_config_manager()
        self.config = get_config()
        self.running = True
        self._animation_id = None  # 动画ID，用于管理动画播放
        self._redraw_lock = threading.Lock()  # 重绘锁，避免频闪
        
        # 初始化各模块
        self.window_mgr = WindowManager(self.config)
        self.anim_mgr = AnimationManager(self.config)
        self.movement = MovementController(self.config)
        self.input_detector = InputDetector(self.config)
        self.hotkey_mgr = HotkeyManager(self.config)
        self.tray_mgr = TrayManager(self.config)
        self.settings_mgr = SettingsManager()
        
        # 初始化组件
        self._init_components()
        
        # 启动线程
        self._start_threads()
        
        info("桌面宠物机器人初始化完成")
    
    def _init_components(self):
        """初始化所有组件"""
        # 创建窗口
        self.window_mgr.create_window()
        
        # 绑定鼠标事件
        self.window_mgr.bind_mouse_events(self._on_mouse_enter, self._on_mouse_leave)
        
        # 加载图片
        self.anim_mgr.load_images()
        
        # 初始绘制
        self._redraw()
        
        # 创建系统托盘
        self.tray_mgr.create({
            'toggle_visibility': self._toggle_visibility,
            'increase_speed': self.movement.increase_speed,
            'decrease_speed': self.movement.decrease_speed,
            'open_settings': self.settings_mgr.open,
            'reload_config': self._reload_config,
            'quit': self._quit_app
        })
    
    def _start_threads(self):
        """启动后台线程"""
        try:
            # 动画/移动循环
            self.animation_thread = threading.Thread(target=self._animation_loop, daemon=True)
            self.animation_thread.start()
            
            # 输入检测循环
            if self.config.behavior.enable_input_detection:
                self.input_thread = threading.Thread(target=self._input_loop, daemon=True)
                self.input_thread.start()
            
            # 快捷键监控
            self.hotkey_thread = threading.Thread(target=self._hotkey_loop, daemon=True)
            self.hotkey_thread.start()
            
            info("线程启动完成")
        except Exception as e:
            error(f"线程启动失败: {e}")
    
    def _redraw(self):
        """重绘窗口（使用锁避免频闪）"""
        with self._redraw_lock:
            photo = self.anim_mgr.get_current_photo(self.input_detector.is_sleeping)
            self.window_mgr.draw(photo)
    
    def _on_mouse_enter(self, event):
        """鼠标进入事件"""
        if self.input_detector.is_sleeping:
            return
        
        robot_size = self.config.robot.robot_size
        in_region = (0 <= event.x <= robot_size and 0 <= event.y <= robot_size)
        
        info(f"鼠标位置: x={event.x}, y={event.y}, 图片尺寸={robot_size}x{robot_size}")
        
        if in_region:
            info("鼠标在机器人图片区域内，触发动画")
            self.anim_mgr.start_hover()
            self._redraw()
            self._start_animation_playback()
    
    def _on_mouse_leave(self, event):
        """鼠标离开事件"""
        info("鼠标离开机器人")
        self.anim_mgr.stop_hover()
        self._redraw()
    
    def _start_animation_playback(self):
        """启动动画播放（使用Tkinter after）"""
        if not self.anim_mgr.animation_frames or not self.anim_mgr.animation_running:
            return
        
        # 使用动画ID来管理，避免重复启动
        if hasattr(self, '_animation_id') and self._animation_id:
            self.window_mgr.window.after_cancel(self._animation_id)
        
        def _animate():
            if not self.anim_mgr.animation_running:
                return
            
            self.anim_mgr.next_frame()
            self._redraw()
            
            if self.anim_mgr.animation_running:
                self._animation_id = self.window_mgr.window.after(500, _animate)  # 降低到500ms
            else:
                self._animation_id = None
        
        self._animation_id = self.window_mgr.window.after(0, _animate)
    
    def _toggle_visibility(self, icon=None, item=None):
        """切换窗口可见性"""
        self.window_mgr.toggle_visibility()
    
    def _reload_config(self, icon=None, item=None):
        """重新加载配置"""
        try:
            self.config_manager.load()
            self.config = get_config()
            self.movement.sync_speed_from_config()
            
            info("配置重新加载完成")
            info(f"运动间隔: {self.config.robot.move_interval}秒")
            info(f"运动速度: {self.movement.speed}")
            info(f"截图快捷键: {self.config.hotkeys.screenshot}")
        except Exception as e:
            error(f"重新加载配置失败: {e}")
    
    def _quit_app(self, icon=None, item=None):
        """退出应用"""
        info("正在退出应用...")
        self.running = False
        
        self.hotkey_mgr.unregister_all()
        self.tray_mgr.stop()
        self.window_mgr.quit()
        
        info("应用已退出")
    
    def _animation_loop(self):
        """动画循环（20FPS）"""
        config_check_counter = 0
        
        while self.running:
            try:
                current_time = time.time()
                
                # 定期检查配置
                config_check_counter += 1
                if config_check_counter >= 100:
                    self._check_config_update()
                    config_check_counter = 0
                
                # 更新移动
                redraw_needed = self.movement.update(
                    current_time, 
                    self.input_detector.is_sleeping
                )
                
                if redraw_needed:
                    self.window_mgr.update_position(self.movement.position)
                    self._redraw()
                
                time.sleep(0.05)
                
            except Exception as e:
                error(f"动画错误: {e}")
                time.sleep(1)
    
    def _input_loop(self):
        """输入检测循环"""
        info("启动输入活动检测...")
        info(f"检测阈值: {self.config.behavior.inactivity_threshold}秒无输入活动进入睡眠")
        
        while self.running:
            try:
                changed = self.input_detector.check_activity()
                if changed:
                    self._redraw()
                time.sleep(1)
            except Exception as e:
                error(f"输入检测错误: {e}")
                time.sleep(5)
    
    def _hotkey_loop(self):
        """快捷键监控循环"""
        info("启动快捷键监控...")
        self.hotkey_mgr.register_all()
        
        try:
            while self.running:
                time.sleep(1)
        except Exception as e:
            error(f"快捷键监控错误: {e}")
    
    def _check_config_update(self):
        """检查配置更新"""
        try:
            self.config_manager.load()
            self.config = get_config()
            self.config_manager.validate()
            self.movement.sync_speed_from_config()
            debug("配置检查完成")
        except Exception as e:
            error(f"检查配置更新失败: {e}")
    
    def run(self):
        """运行应用"""
        try:
            info("启动桌面宠物机器人...")
            self.window_mgr.run()
        except KeyboardInterrupt:
            info("接收到键盘中断，正在退出...")
            self._quit_app()
        except Exception as e:
            error(f"应用运行错误: {e}")
            self._quit_app()
