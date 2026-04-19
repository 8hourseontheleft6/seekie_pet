#!/usr/bin/env python3
"""
桌面宠物机器人 - 重构版
使用模块化结构，增强错误处理和配置管理

版本: 3.3.2 (模块化重构版 - 修复所有问题)
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import setup_logging, get_logger, info, error, debug, warning
from config.config_manager import get_config_manager, get_config
from utils.image_loader import load_robot_image, load_sleep_image, load_tray_image

import tkinter as tk
import threading
import time
import random
import subprocess
import queue
from PIL import ImageTk
import pystray
from pystray import MenuItem as item
from ctypes import windll, Structure, c_ulong, byref
import keyboard

logger = get_logger()

class DesktopPetRobot:
    """桌面宠物机器人 - 重构版"""
    
    def __init__(self):
        self.config_manager = get_config_manager()
        self.config = get_config()
        
        # 初始化状态
        self.window = None
        self.canvas = None
        self.icon = None
        self.running = True
        
        # 机器人状态
        self.position = 75  # 初始位置
        self.direction = 0
        self.speed = self.config.robot.move_speed
        self.is_moving = False
        self.last_move_time = time.time()
        self.target_position = self.position  # 初始目标位置
        
        # 输入检测状态
        self.last_input_time = self._get_last_input_time()
        self.is_sleeping = False
        
        # 图片资源
        self.robot_photo = None
        self.sleep_photo = None
        
        # 初始化组件
        self._init_components()
        
        # 启动线程
        self._start_threads()
        
        info("桌面宠物机器人初始化完成")
    
    def _init_components(self):
        """初始化组件"""
        self._init_window()
        self._load_images()
        self._init_tray()
    
    def _init_window(self):
        """初始化窗口"""
        try:
            self.window = tk.Tk()
            self.window.title("桌面宠物机器人")  # 使用固定标题，与原版一致
            self.window.overrideredirect(True)
            self.window.attributes('-topmost', True)  # 与原版一致，总是置顶
            
            # 设置透明度
            try:
                self.window.attributes('-alpha', 0.99)  # 与原版一致
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
            
            # 设置初始位置
            self._update_window_position()
            
            info("窗口初始化完成")
            
        except Exception as e:
            error(f"窗口初始化失败: {e}")
            raise
    
    def _load_images(self):
        """加载机器人图片和睡眠图片"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # 加载机器人图片
            robot_path = os.path.join(current_dir, "main_pic", "Robot_50x50.png")
            info(f"加载机器人图片: {robot_path}")
            
            if os.path.exists(robot_path):
                from PIL import Image
                robot_image = Image.open(robot_path)
                # 调整大小
                if robot_image.size != (self.config.robot.robot_size, self.config.robot.robot_size):
                    robot_image = robot_image.resize((self.config.robot.robot_size, self.config.robot.robot_size), Image.Resampling.LANCZOS)
                self.robot_photo = ImageTk.PhotoImage(robot_image)
                info("[成功] 机器人图片加载成功")
            else:
                error("[警告] 机器人图片不存在，使用后备图标")
                # 使用图片加载器创建默认图片
                robot_image = load_robot_image((self.config.robot.robot_size, self.config.robot.robot_size))
                if robot_image:
                    self.robot_photo = ImageTk.PhotoImage(robot_image)
            
            # 加载睡眠图片
            sleep_path = os.path.join(current_dir, "main_pic", "Sleep.png")
            info(f"加载睡眠图片: {sleep_path}")
            
            if os.path.exists(sleep_path):
                from PIL import Image
                sleep_image = Image.open(sleep_path)
                # 调整大小
                if sleep_image.size != (self.config.robot.robot_size, self.config.robot.robot_size):
                    sleep_image = sleep_image.resize((self.config.robot.robot_size, self.config.robot.robot_size), Image.Resampling.LANCZOS)
                self.sleep_photo = ImageTk.PhotoImage(sleep_image)
                info("[成功] 睡眠图片加载成功")
            else:
                error("[警告] 睡眠图片不存在，创建后备睡眠图标")
                # 使用图片加载器创建默认图片
                sleep_image = load_sleep_image((self.config.robot.robot_size, self.config.robot.robot_size))
                if sleep_image:
                    self.sleep_photo = ImageTk.PhotoImage(sleep_image)
            
            # 初始绘制
            self._draw_current()
            
        except Exception as e:
            error(f"图片加载失败: {e}")
            # 创建默认图片
            try:
                from PIL import Image, ImageDraw
                # 创建默认机器人图片
                img = Image.new('RGBA', (self.config.robot.robot_size, self.config.robot.robot_size), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                draw.rectangle([10, 10, 40, 40], fill='#4169E1', outline='#1E3A8A', width=2)
                self.robot_photo = ImageTk.PhotoImage(img)
                
                # 创建默认睡眠图片
                img = Image.new('RGBA', (self.config.robot.robot_size, self.config.robot.robot_size), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                draw.rectangle([10, 10, 40, 40], fill='#4169E1', outline='#1E3A8A', width=2)
                draw.line([15, 17, 25, 17], fill='#FFFFFF', width=3)
                draw.line([30, 17, 35, 17], fill='#FFFFFF', width=3)
                self.sleep_photo = ImageTk.PhotoImage(img)
                
                info("使用默认图片")
            except:
                pass
    
    def _init_tray(self):
        """初始化系统托盘"""
        try:
            # 加载托盘图片 - 使用robot-icon.png
            current_dir = os.path.dirname(os.path.abspath(__file__))
            tray_path = os.path.join(current_dir, "main_pic", "robot-icon.png")
            
            if os.path.exists(tray_path):
                from PIL import Image
                tray_image = Image.open(tray_path)
                # 调整大小为64x64
                tray_image = tray_image.resize((64, 64), Image.Resampling.LANCZOS)
                info(f"托盘图标加载成功: {tray_path}")
            else:
                # 使用图片加载器创建默认图片
                tray_image = load_tray_image((64, 64))
                if not tray_image:
                    # 创建默认托盘图片
                    from PIL import Image, ImageDraw
                    tray_image = Image.new('RGB', (64, 64), color='white')
                    draw = ImageDraw.Draw(tray_image)
                    draw.rectangle([20, 20, 44, 44], fill='#4169E1', outline='#1E3A8A', width=2)
                info("使用默认托盘图标")
            
            # 创建菜单
            menu = (
                item('显示/隐藏', self._toggle_visibility),
                item('速度加快', self._increase_speed),
                item('速度减慢', self._decrease_speed),
                item('---', None),
                item('打开设置', self._open_settings),
                item('重新加载配置', self._reload_config),
                item('---', None),
                item('退出', self._quit_app)
            )
            
            self.icon = pystray.Icon(
                "desktop_pet_robot",
                tray_image,
                "桌面宠物机器人 (重构版)",
                menu
            )
            
            self.tray_thread = threading.Thread(target=self.icon.run, daemon=True)
            self.tray_thread.start()
            
            info("系统托盘初始化完成")
            
        except Exception as e:
            error(f"系统托盘初始化失败: {e}")
    
    def _start_threads(self):
        """启动线程"""
        try:
            self.animation_thread = threading.Thread(target=self._animation_loop, daemon=True)
            self.input_detection_thread = threading.Thread(target=self._input_detection_loop, daemon=True)
            self.hotkey_thread = threading.Thread(target=self._hotkey_monitor_loop, daemon=True)
            
            self.animation_thread.start()
            if self.config.behavior.enable_input_detection:
                self.input_detection_thread.start()
            self.hotkey_thread.start()
            
            info("线程启动完成")
            
        except Exception as e:
            error(f"线程启动失败: {e}")
    
    # ==================== 核心功能方法 ====================
    
    def _update_window_position(self):
        """更新窗口位置"""
        if not self.window:
            return
        
        try:
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            
            # 计算位置
            car_size = self.config.robot.robot_size
            taskbar_height = 40
            vertical_offset = -5
            
            if self.config.behavior.move_only_on_right_side:
                # 限制在右半边
                max_x = screen_width - car_size
                x_pos = int((self.position - 50) / 50 * (max_x / 2) + (max_x / 2))
            else:
                # 全屏幕
                max_x = screen_width - car_size
                x_pos = int((self.position - 50) / 50 * max_x)
            
            y_pos = screen_height - taskbar_height - car_size + vertical_offset
            
            # 在主线程中更新窗口位置
            self.window.after(0, lambda: self.window.geometry(f"+{x_pos}+{y_pos}"))
        except Exception as e:
            # 如果窗口已销毁，忽略错误
            pass
    
    def _draw_current(self):
        """绘制当前状态"""
        if not self.canvas:
            return
        
        self.canvas.delete("all")
        
        if self.is_sleeping and self.config.behavior.enable_sleep_mode:
            # 绘制睡眠图片
            if self.sleep_photo:
                self.canvas.create_image(
                    self.config.robot.robot_size // 2,
                    self.config.robot.robot_size // 2,
                    image=self.sleep_photo,
                    tags="sleep"
                )
        else:
            # 绘制机器人图片
            if self.robot_photo:
                self.canvas.create_image(
                    self.config.robot.robot_size // 2,
                    self.config.robot.robot_size // 2,
                    image=self.robot_photo,
                    tags="robot"
                )
    
    # ==================== 控制方法 ====================
    
    def _toggle_visibility(self, icon=None, item=None):
        """切换窗口可见性"""
        if self.window.winfo_viewable():
            self.window.withdraw()
            info("窗口隐藏")
        else:
            self.window.deiconify()
            info("窗口显示")
    
    def _increase_speed(self, icon=None, item=None):
        """增加速度"""
        self.speed = min(5.0, self.speed + 0.5)
        info(f"速度增加至: {self.speed}")
    
    def _decrease_speed(self, icon=None, item=None):
        """减小速度"""
        self.speed = max(0.5, self.speed - 0.5)
        info(f"速度减小至: {self.speed}")
    
    def _open_settings(self, icon=None, item=None):
        """打开设置窗口"""
        try:
            # 避免重复打开多个设置窗口
            if hasattr(self, 'settings_window') and self.settings_window:
                try:
                    # 尝试将现有窗口提到前面
                    self.settings_window.window.lift()
                    self.settings_window.window.focus_force()
                    return
                except:
                    pass

            # 在新线程中打开设置窗口，避免阻塞主线程
            settings_thread = threading.Thread(target=self._open_settings_window_thread, daemon=True)
            settings_thread.start()
        except Exception as e:
            error(f"打开设置窗口失败: {e}")
    
    def _open_settings_window_thread(self):
        """在新线程中打开设置窗口"""
        try:
            # 动态导入Web设置窗口模块
            import sys
            import os

            # 添加Web设置窗口目录到Python路径
            web_settings_dir = os.path.join(os.path.dirname(__file__), 'web_settings')
            if os.path.exists(web_settings_dir):
                sys.path.insert(0, web_settings_dir)

                try:
                    from web_settings import open_web_settings
                    open_web_settings()
                    info("Web设置窗口已打开")
                except ImportError as e:
                    error(f"导入Web设置窗口失败: {e}")
                    # 回退到现代化设置窗口
                    self._fallback_to_modern_settings()
            else:
                error(f"Web设置窗口目录不存在: {web_settings_dir}")
                self._fallback_to_modern_settings()

        except Exception as e:
            error(f"打开设置窗口线程失败: {e}")
            import traceback
            traceback.print_exc()
            self._fallback_to_modern_settings()
    
    def _fallback_to_modern_settings(self):
        """回退到现代化设置窗口"""
        try:
            from settings_window_v2 import open_modern_settings_window
            open_modern_settings_window()
            info("现代化设置窗口已打开")
        except Exception as e:
            error(f"打开现代化设置窗口失败: {e}")
    
    def _reload_config(self, icon=None, item=None):
        """重新加载配置"""
        try:
            self.config_manager.load()
            self.config = get_config()
            
            # 更新动态配置
            self.speed = self.config.robot.move_speed
            
            info("配置重新加载完成")
            info(f"运动间隔: {self.config.robot.move_interval}秒")
            info(f"运动速度: {self.speed}")
            info(f"截图快捷键: {self.config.hotkeys.screenshot}")
            
        except Exception as e:
            error(f"重新加载配置失败: {e}")
    
    def _quit_app(self, icon=None, item=None):
        """退出应用"""
        info("正在退出应用...")
        self.running = False
        
        # 清理快捷键
        try:
            keyboard.unhook_all()
        except:
            pass
        
        if self.icon:
            self.icon.stop()
        if self.window:
            self.window.quit()
        
        info("应用已退出")
    
    # ==================== 输入检测方法 ====================
    
    class LASTINPUTINFO(Structure):
        _fields_ = [
            ('cbSize', c_ulong),
            ('dwTime', c_ulong)
        ]
    
    def _get_last_input_time(self):
        """获取系统最后输入时间"""
        try:
            lastInputInfo = self.LASTINPUTINFO()
            lastInputInfo.cbSize = c_ulong(8)
            
            if windll.user32.GetLastInputInfo(byref(lastInputInfo)):
                return lastInputInfo.dwTime
            else:
                return 0
        except:
            return 0
    
    def _get_idle_time(self):
        """获取系统空闲时间"""
        try:
            last_input = self._get_last_input_time()
            current_time = windll.kernel32.GetTickCount()
            
            if last_input == 0:
                return 0
            
            idle_time = (current_time - last_input) // 1000
            return idle_time
        except:
            return 0
    
    def _check_input_activity(self):
        """检查输入活动"""
        if not self.config.behavior.enable_input_detection:
            return
        
        idle_time = self._get_idle_time()
        
        if idle_time == 0:
            # 有输入活动
            if self.is_sleeping:
                info("检测到输入活动，从睡眠状态唤醒")
                self.is_sleeping = False
                self._draw_current()
        else:
            # 检查是否应该进入睡眠状态
            if not self.is_sleeping and idle_time > self.config.behavior.inactivity_threshold:
                info(f"系统{idle_time}秒无输入活动，进入睡眠状态")
                self.is_sleeping = True
                self._draw_current()
    
    # ==================== 快捷键方法 ====================
    
    def _register_hotkeys(self):
        """注册快捷键"""
        try:
            # 注册截图快捷键
            if self.config.hotkeys.screenshot:
                keyboard.add_hotkey(self.config.hotkeys.screenshot, self._take_screenshot)
                info(f"快捷键注册成功: {self.config.hotkeys.screenshot} - 打开截图软件")
            
            # 注册其他快捷键
            if self.config.hotkeys.toggle_visibility:
                keyboard.add_hotkey(self.config.hotkeys.toggle_visibility, self._toggle_visibility)
            
            if self.config.hotkeys.increase_speed:
                keyboard.add_hotkey(self.config.hotkeys.increase_speed, self._increase_speed)
            
            if self.config.hotkeys.decrease_speed:
                keyboard.add_hotkey(self.config.hotkeys.decrease_speed, self._decrease_speed)
                
        except Exception as e:
            error(f"快捷键注册失败: {e}")
    
    def _take_screenshot(self):
        """执行截图操作"""
        try:
            info(f"检测到{self.config.hotkeys.screenshot}快捷键，正在打开截图软件...")
            
            # 尝试多种截图方式
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
    
    # ==================== 动画循环方法 ====================
    
    def _animation_loop(self):
        """动画循环"""
        config_check_counter = 0
        
        while self.running:
            try:
                current_time = time.time()
                
                # 定期检查配置更新
                config_check_counter += 1
                if config_check_counter >= 100:  # 5秒检查一次
                    self._check_config_update()
                    config_check_counter = 0
                
                # 只有在非睡眠状态时才检查移动
                if not self.is_sleeping:
                    # 检查是否应该开始移动
                    if not self.is_moving and (current_time - self.last_move_time) > self.config.robot.move_interval:
                        self._start_moving(current_time)
                    
                    # 如果正在移动，更新位置
                    if self.is_moving:
                        self._update_movement(current_time)
                else:
                    # 睡眠状态下停止移动
                    if self.is_moving:
                        self.is_moving = False
                        self.direction = 0
                        info("进入睡眠状态，停止移动")
                
                time.sleep(0.05)  # 20FPS
                
            except Exception as e:
                error(f"动画错误: {e}")
                time.sleep(1)
    
    def _start_moving(self, current_time):
        """开始移动"""
        self.is_moving = True
        self.last_move_time = current_time
        
        # 设置目标位置（50-100之间的随机值）
        self.target_position = random.uniform(50, 100)
        self.direction = 1 if self.target_position > self.position else -1
        
        info(f"开始移动: 方向={self.direction}, 目标={self.target_position:.1f}")
    
    def _check_config_update(self):
        """检查并应用配置更新"""
        try:
            # 重新加载配置文件
            self.config_manager.load()
            self.config = get_config()
            
            # 验证配置
            self.config_manager.validate()
            
            # 应用配置更新到当前实例
            self._apply_config_updates()
            
            debug("配置检查完成")
            
        except Exception as e:
            error(f"检查配置更新失败: {e}")
    
    def _apply_config_updates(self):
        """应用配置更新到当前实例"""
        try:
            # 更新速度
            self.speed = self.config.robot.move_speed
            
            # 更新其他配置
            # 这里可以添加其他需要动态更新的配置项
            
            debug(f"配置已应用: 速度={self.speed}")
            
        except Exception as e:
            error(f"应用配置更新失败: {e}")
    
    def _update_movement(self, current_time):
        """更新移动"""
        # 更新位置
        self.position += self.direction * self.speed * 0.05
        
        # 检查是否到达或超过目标位置
        if (self.direction > 0 and self.position >= self.target_position) or \
           (self.direction < 0 and self.position <= self.target_position):
            # 到达目标位置，停止移动
            self.position = self.target_position  # 精确设置到目标位置
            self.is_moving = False
            self.direction = 0
            info(f"到达目标位置: {self.target_position:.1f}")
        
        # 边界检查（防止超出范围）
        if self.position < 50:
            self.position = 50
            self.direction = 1
        elif self.position > 100:
            self.position = 100
            self.direction = -1
        
        # 更新窗口位置
        self._update_window_position()
        
        # 重绘机器人（确保在主线程中执行）
        if self.window:
            try:
                self.window.after(0, self._draw_current)
            except Exception as e:
                # 如果窗口已销毁，忽略错误
                pass
    
    # ==================== 线程循环方法 ====================
    
    def _input_detection_loop(self):
        """输入检测循环"""
        info("启动输入活动检测...")
        info(f"检测阈值: {self.config.behavior.inactivity_threshold}秒无输入活动进入睡眠")
        
        while self.running:
            try:
                self._check_input_activity()
                time.sleep(1)
            except Exception as e:
                error(f"输入检测错误: {e}")
                time.sleep(5)
    
    def _hotkey_monitor_loop(self):
        """快捷键监控循环"""
        info("启动快捷键监控...")
        self._register_hotkeys()
        
        try:
            while self.running:
                time.sleep(1)
        except Exception as e:
            error(f"快捷键监控错误: {e}")
    
    # ==================== 公共方法 ====================
    
    def run(self):
        """运行应用"""
        try:
            info("启动桌面宠物机器人...")
            self.window.mainloop()
        except KeyboardInterrupt:
            info("接收到键盘中断，正在退出...")
            self._quit_app()
        except Exception as e:
            error(f"应用运行错误: {e}")
            self._quit_app()

def print_header():
    """打印程序头信息"""
    config = get_config()
    
    print("=" * 50)
    print("桌面宠物机器人 v3.3.2 (模块化重构版 - 修复所有问题)")
    print("=" * 50)
    print("功能特点:")
    print("- 模块化结构，代码更清晰")
    print("- 增强的错误处理和日志记录")
    print("- 改进的配置管理")
    print(f"- 运动间隔: {config.robot.move_interval}秒")
    print(f"- 运动速度: {config.robot.move_speed}")
    print(f"- 截图快捷键: {config.hotkeys.screenshot}")
    print(f"- 主题: {config.appearance.theme.value}")
    print(f"- 透明度: {config.appearance.transparency}")
    print(f"- 睡眠模式: {'启用' if config.behavior.enable_sleep_mode else '禁用'}")
    print(f"- 输入检测: {'启用' if config.behavior.enable_input_detection else '禁用'}")
    print("=" * 50)
    print("修复的问题:")
    print("- 设置功能正常打开")
    print("- 托盘图标使用robot-icon.png")
    print("- 运动到目标位置后停止，等待10秒再开始新运动")
    print("- 修复线程错误")
    print("=" * 50)
    print("应用将在系统托盘中运行")
    print("右键点击托盘图标可以控制机器人")
    print("=" * 50)

def main():
    """主函数"""
    # 设置日志
    from utils.logger import setup_logging
    setup_logging(level="INFO", enable_file=True, enable_console=True)
    
    # 打印头信息
    print_header()
    
    # 创建并运行机器人
    try:
        pet = DesktopPetRobot()
        pet.run()
    except Exception as e:
        error(f"应用启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
