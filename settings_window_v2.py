#!/usr/bin/env python3
"""
Seekie Setup v2 - 现代化设置窗口
参考现代音乐播放器界面风格，更加美观简洁
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os
import threading
from PIL import Image, ImageTk

class ModernSeekieSetup:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.window = None
        self.current_page = "general"  # 当前页面
        
        # 颜色主题
        self.colors = {
            "bg_primary": "#1e1e1e",      # 主背景色（深灰）
            "bg_secondary": "#2d2d2d",    # 次要背景色
            "bg_card": "#252525",         # 卡片背景色
            "text_primary": "#ffffff",    # 主要文字色
            "text_secondary": "#b3b3b3",  # 次要文字色
            "accent": "#1db954",          # 强调色（Spotify绿）
            "accent_hover": "#1ed760",    # 强调色悬停
            "border": "#404040",          # 边框色
            "slider_track": "#535353",    # 滑块轨道
            "slider_thumb": "#ffffff",    # 滑块拇指
        }
    
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 创建默认配置
                default_config = {
                    "move_interval": 20,
                    "move_speed": 1.5,
                    "screenshot_hotkey": "ctrl+j",
                    "window_title": "Seekie Setup"
                }
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)
                return default_config
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {
                "move_interval": 20,
                "move_speed": 1.5,
                "screenshot_hotkey": "ctrl+j",
                "window_title": "Seekie Setup"
            }
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def create_window(self):
        """创建现代化设置窗口"""
        self.window = tk.Tk()
        self.window.title(self.config.get("window_title", "Seekie Setup"))
        self.window.geometry("800x500")
        self.window.resizable(False, False)
        self.window.configure(bg=self.colors["bg_primary"])
        
        # 设置窗口图标
        try:
            self.window.iconbitmap(default='icon.ico')
        except:
            pass
        
        # 创建主容器
        main_container = tk.Frame(self.window, bg=self.colors["bg_primary"])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # 侧边栏
        self.create_sidebar(main_container)
        
        # 内容区域
        self.content_frame = tk.Frame(main_container, bg=self.colors["bg_primary"])
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建页面
        self.create_general_page()
        
        # 绑定窗口关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_sidebar(self, parent):
        """创建侧边栏"""
        sidebar = tk.Frame(parent, bg=self.colors["bg_secondary"], width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # 应用标题
        title_frame = tk.Frame(sidebar, bg=self.colors["bg_secondary"], height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="Seekie",
            font=("Segoe UI", 24, "bold"),
            fg=self.colors["accent"],
            bg=self.colors["bg_secondary"]
        )
        title_label.pack(pady=(20, 5))
        
        subtitle_label = tk.Label(
            title_frame,
            text="桌面宠物机器人",
            font=("Segoe UI", 10),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_secondary"]
        )
        subtitle_label.pack()
        
        # 导航按钮
        nav_items = [
            ("general", "⚙️", "常规设置"),
            ("appearance", "🎨", "外观设置"),
            ("hotkeys", "⌨️", "快捷键"),
            ("about", "ℹ️", "关于")
        ]
        
        self.nav_buttons = {}
        
        for item_id, icon, text in nav_items:
            btn_frame = tk.Frame(sidebar, bg=self.colors["bg_secondary"])
            btn_frame.pack(fill=tk.X, padx=10, pady=2)
            
            btn = tk.Button(
                btn_frame,
                text=f"  {icon}  {text}",
                font=("Segoe UI", 11),
                fg=self.colors["text_primary"],
                bg=self.colors["bg_secondary"],
                bd=0,
                padx=15,
                pady=10,
                anchor="w",
                cursor="hand2",
                command=lambda id=item_id: self.switch_page(id)
            )
            btn.pack(fill=tk.X)
            
            # 绑定悬停效果
            btn.bind("<Enter>", lambda e, b=btn: self.on_nav_hover(e, b, True))
            btn.bind("<Leave>", lambda e, b=btn: self.on_nav_hover(e, b, False))
            
            self.nav_buttons[item_id] = btn
        
        # 底部版本信息
        version_frame = tk.Frame(sidebar, bg=self.colors["bg_secondary"])
        version_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        version_label = tk.Label(
            version_frame,
            text="v3.2.0",
            font=("Segoe UI", 9),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_secondary"]
        )
        version_label.pack()
    
    def on_nav_hover(self, event, button, is_hover):
        """导航按钮悬停效果"""
        if is_hover:
            button.config(bg="#3d3d3d")
        else:
            button.config(bg=self.colors["bg_secondary"])
    
    def switch_page(self, page_id):
        """切换页面"""
        self.current_page = page_id
        
        # 更新按钮状态
        for btn_id, btn in self.nav_buttons.items():
            if btn_id == page_id:
                btn.config(bg="#3d3d3d", fg=self.colors["accent"])
            else:
                btn.config(bg=self.colors["bg_secondary"], fg=self.colors["text_primary"])
        
        # 清除内容区域
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # 加载对应页面
        if page_id == "general":
            self.create_general_page()
        elif page_id == "appearance":
            self.create_appearance_page()
        elif page_id == "hotkeys":
            self.create_hotkeys_page()
        elif page_id == "about":
            self.create_about_page()
    
    def create_general_page(self):
        """创建常规设置页面"""
        # 页面标题
        title_label = tk.Label(
            self.content_frame,
            text="常规设置",
            font=("Segoe UI", 20, "bold"),
            fg=self.colors["text_primary"],
            bg=self.colors["bg_primary"]
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # 运动设置卡片
        movement_card = self.create_card("运动设置")
        
        # 运动间隔设置
        interval_frame = tk.Frame(movement_card, bg=self.colors["bg_card"])
        interval_frame.pack(fill=tk.X, pady=(0, 20))
        
        interval_label = tk.Label(
            interval_frame,
            text="运动间隔",
            font=("Segoe UI", 11),
            fg=self.colors["text_primary"],
            bg=self.colors["bg_card"]
        )
        interval_label.pack(anchor="w")
        
        interval_desc = tk.Label(
            interval_frame,
            text="控制机器人两次移动之间的等待时间",
            font=("Segoe UI", 9),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_card"]
        )
        interval_desc.pack(anchor="w", pady=(0, 10))
        
        self.interval_var = tk.IntVar(value=self.config.get("move_interval", 20))
        
        # 滑块和数值显示
        slider_frame = tk.Frame(interval_frame, bg=self.colors["bg_card"])
        slider_frame.pack(fill=tk.X)
        
        interval_slider = tk.Scale(
            slider_frame,
            from_=5,
            to=60,
            orient=tk.HORIZONTAL,
            variable=self.interval_var,
            length=400,
            bg=self.colors["bg_card"],
            fg=self.colors["text_primary"],
            highlightthickness=0,
            troughcolor=self.colors["slider_track"],
            sliderrelief="flat",
            command=lambda v: self.update_interval_label()
        )
        interval_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.interval_value_label = tk.Label(
            slider_frame,
            text=f"{self.interval_var.get()} 秒",
            font=("Segoe UI", 11, "bold"),
            fg=self.colors["accent"],
            bg=self.colors["bg_card"],
            width=8
        )
        self.interval_value_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # 运动速度设置
        speed_frame = tk.Frame(movement_card, bg=self.colors["bg_card"])
        speed_frame.pack(fill=tk.X, pady=(0, 20))
        
        speed_label = tk.Label(
            speed_frame,
            text="运动速度",
            font=("Segoe UI", 11),
            fg=self.colors["text_primary"],
            bg=self.colors["bg_card"]
        )
        speed_label.pack(anchor="w")
        
        speed_desc = tk.Label(
            speed_frame,
            text="控制机器人移动的速度",
            font=("Segoe UI", 9),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_card"]
        )
        speed_desc.pack(anchor="w", pady=(0, 10))
        
        self.speed_var = tk.DoubleVar(value=self.config.get("move_speed", 1.5))
        
        # 滑块和数值显示
        speed_slider_frame = tk.Frame(speed_frame, bg=self.colors["bg_card"])
        speed_slider_frame.pack(fill=tk.X)
        
        speed_slider = tk.Scale(
            speed_slider_frame,
            from_=0.5,
            to=5.0,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            resolution=0.1,
            length=400,
            bg=self.colors["bg_card"],
            fg=self.colors["text_primary"],
            highlightthickness=0,
            troughcolor=self.colors["slider_track"],
            sliderrelief="flat",
            command=lambda v: self.update_speed_label()
        )
        speed_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.speed_value_label = tk.Label(
            speed_slider_frame,
            text=f"{self.speed_var.get():.1f}",
            font=("Segoe UI", 11, "bold"),
            fg=self.colors["accent"],
            bg=self.colors["bg_card"],
            width=8
        )
        self.speed_value_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # 按钮区域
        button_frame = tk.Frame(self.content_frame, bg=self.colors["bg_primary"])
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        # 保存按钮
        save_button = tk.Button(
            button_frame,
            text="保存设置",
            font=("Segoe UI", 11, "bold"),
            fg="white",
            bg=self.colors["accent"],
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2",
            command=self.save_settings
        )
        save_button.pack(side=tk.RIGHT)
        
        # 应用按钮
        apply_button = tk.Button(
            button_frame,
            text="应用",
            font=("Segoe UI", 11),
            fg=self.colors["text_primary"],
            bg=self.colors["bg_card"],
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.apply_settings
        )
        apply_button.pack(side=tk.RIGHT, padx=(0, 10))
        
        # 取消按钮
        cancel_button = tk.Button(
            button_frame,
            text="取消",
            font=("Segoe UI", 11),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_card"],
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.window.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=(0, 10))
    
    def create_appearance_page(self):
        """创建外观设置页面"""
        # 页面标题
        title_label = tk.Label(
            self.content_frame,
            text="外观设置",
            font=("Segoe UI", 20, "bold"),
            fg=self.colors["text_primary"],
            bg=self.colors["bg_primary"]
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # 提示信息
        info_label = tk.Label(
            self.content_frame,
            text="外观设置功能正在开发中...",
            font=("Segoe UI", 12),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_primary"]
        )
        info_label.pack(anchor="w", pady=20)
        
        info_desc = tk.Label(
            self.content_frame,
            text="未来版本将支持主题切换、透明度调整等功能",
            font=("Segoe UI", 10),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_primary"]
        )
        info_desc.pack(anchor="w")
    
    def create_hotkeys_page(self):
        """创建快捷键页面"""
        # 页面标题
        title_label = tk.Label(
            self.content_frame,
            text="快捷键设置",
            font=("Segoe UI", 20, "bold"),
            fg=self.colors["text_primary"],
            bg=self.colors["bg_primary"]
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # 快捷键卡片
        hotkey_card = self.create_card("截图快捷键")
        
        # 快捷键设置
        hotkey_frame = tk.Frame(hotkey_card, bg=self.colors["bg_card"])
        hotkey_frame.pack(fill=tk.X, pady=20)
        
        hotkey_label = tk.Label(
            hotkey_frame,
            text="打开截图软件的快捷键",
            font=("Segoe UI", 11),
            fg=self.colors["text_primary"],
            bg=self.colors["bg_card"]
        )
        hotkey_label.pack(anchor="w")
        
        hotkey_desc = tk.Label(
            hotkey_frame,
            text="按下组合键来设置快捷键",
            font=("Segoe UI", 9),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_card"]
        )
        hotkey_desc.pack(anchor="w", pady=(0, 10))
        
        self.hotkey_var = tk.StringVar(value=self.config.get("screenshot_hotkey", "ctrl+j"))
        
        # 快捷键输入框
        hotkey_entry_frame = tk.Frame(hotkey_frame, bg=self.colors["bg_card"])
        hotkey_entry_frame.pack(fill=tk.X)
        
        hotkey_entry = tk.Entry(
            hotkey_entry_frame,
            textvariable=self.hotkey_var,
            font=("Segoe UI", 12),
            fg=self.colors["text_primary"],
            bg=self.colors["bg_secondary"],
            bd=0,
            insertbackground=self.colors["text_primary"],
            selectbackground=self.colors["accent"],
            width=30,
            justify="center"
        )
        hotkey_entry.pack(pady=10)
        
        # 快捷键格式提示
        format_hint = tk.Label(
            hotkey_frame,
            text="格式: ctrl+key, alt+key, shift+key (例如: ctrl+j, alt+s, shift+f1)",
            font=("Segoe UI", 9),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_card"]
        )
        format_hint.pack(anchor="w")
        
        # 预设快捷键按钮
        preset_frame = tk.Frame(hotkey_frame, bg=self.colors["bg_card"])
        preset_frame.pack(fill=tk.X, pady=(20, 0))
        
        preset_label = tk.Label(
            preset_frame,
            text="预设快捷键:",
            font=("Segoe UI", 10),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_card"]
        )
        preset_label.pack(anchor="w", pady=(0, 5))
        
        preset_buttons_frame = tk.Frame(preset_frame, bg=self.colors["bg_card"])
        preset_buttons_frame.pack(fill=tk.X)
        
        presets = ["ctrl+j", "alt+s", "shift+f1", "ctrl+shift+s"]
        
        for preset in presets:
            btn = tk.Button(
                preset_buttons_frame,
                text=preset,
                font=("Segoe UI", 9),
                fg=self.colors["text_primary"],
                bg=self.colors["bg_secondary"],
                bd=0,
                padx=15,
                pady=5,
                cursor="hand2",
                command=lambda p=preset: self.set_preset_hotkey(p)
            )
            btn.pack(side=tk.LEFT, padx=(0, 10))
    
    def create_about_page(self):
        """创建关于页面"""
        # 页面标题
        title_label = tk.Label(
            self.content_frame,
            text="关于 Seekie",
            font=("Segoe UI", 20, "bold"),
            fg=self.colors["text_primary"],
            bg=self.colors["bg_primary"]
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # 关于卡片
        about_card = self.create_card("桌面宠物机器人")
        
        # 应用信息
        info_frame = tk.Frame(about_card, bg=self.colors["bg_card"])
        info_frame.pack(fill=tk.X, pady=20)
        
        app_name = tk.Label(
            info_frame,
            text="Seekie - 桌面宠物机器人",
            font=("Segoe UI", 16, "bold"),
            fg=self.colors["accent"],
            bg=self.colors["bg_card"]
        )
        app_name.pack(anchor="w", pady=(0, 10))
        
        version = tk.Label(
            info_frame,
            text="版本: 3.2.0 (设置窗口版)",
            font=("Segoe UI", 11),
            fg=self.colors["text_primary"],
            bg=self.colors["bg_card"]
        )
        version.pack(anchor="w", pady=(0, 5))
        
        description = tk.Label(
            info_frame,
            text="一个轻量级的桌面宠物应用，显示一个机器人在菜单栏区域移动，\n"
                 "支持输入活动检测、睡眠模式、快捷键功能和设置窗口。",
            font=("Segoe UI", 10),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_card"],
            justify="left"
        )
        description.pack(anchor="w", pady=(0, 20))
        
        # 功能列表
        features = [
            "🤖 智能机器人在菜单栏区域移动",
            "😴 10秒无输入活动进入睡眠状态",
            "🔔 检测到输入活动后自动唤醒",
            "⌨️ 可自定义快捷键打开截图软件",
            "⚙️ 图形化设置界面，自定义运动参数",
            "📁 配置文件管理，支持热重载"
        ]
        
        for feature in features:
            feature_label = tk.Label(
                info_frame,
                text=f"• {feature}",
                font=("Segoe UI", 10),
                fg=self.colors["text_secondary"],
                bg=self.colors["bg_card"],
                justify="left"
            )
            feature_label.pack(anchor="w", pady=2)
        
        # 作者信息
        author_frame = tk.Frame(about_card, bg=self.colors["bg_card"])
        author_frame.pack(fill=tk.X, pady=(20, 0))
        
        author_label = tk.Label(
            author_frame,
            text="作者: DeepSeek AI (NGC2237-Albus辅助)",
            font=("Segoe UI", 10),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_card"]
        )
        author_label.pack(anchor="w")
        
        license_label = tk.Label(
            author_frame,
            text="许可证: 仅供学习和娱乐使用",
            font=("Segoe UI", 10),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_card"]
        )
        license_label.pack(anchor="w", pady=(5, 0))
    
    def create_card(self, title):
        """创建卡片容器"""
        card = tk.Frame(self.content_frame, bg=self.colors["bg_card"], bd=1, relief="flat")
        card.pack(fill=tk.X, pady=(0, 20))
        
        # 卡片标题
        if title:
            title_label = tk.Label(
                card,
                text=title,
                font=("Segoe UI", 12, "bold"),
                fg=self.colors["text_primary"],
                bg=self.colors["bg_card"]
            )
            title_label.pack(anchor="w", padx=20, pady=(15, 10))
        
        # 卡片内容容器
        content_container = tk.Frame(card, bg=self.colors["bg_card"])
        content_container.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        return content_container
    
    def update_interval_label(self):
        """更新间隔标签"""
        self.interval_value_label.config(text=f"{self.interval_var.get()} 秒")
    
    def update_speed_label(self):
        """更新速度标签"""
        self.speed_value_label.config(text=f"{self.speed_var.get():.1f}")
    
    def set_preset_hotkey(self, preset):
        """设置预设快捷键"""
        self.hotkey_var.set(preset)
    
    def save_settings(self):
        """保存设置"""
        self.config["move_interval"] = self.interval_var.get()
        self.config["move_speed"] = round(self.speed_var.get(), 1)
        self.config["screenshot_hotkey"] = self.hotkey_var.get().lower()
        
        if self.save_config():
            messagebox.showinfo("成功", "设置已保存！\n需要重启程序使部分设置生效。")
            self.window.destroy()
        else:
            messagebox.showerror("错误", "保存设置失败！")
    
    def apply_settings(self):
        """应用设置（不关闭窗口）"""
        self.config["move_interval"] = self.interval_var.get()
        self.config["move_speed"] = round(self.speed_var.get(), 1)
        self.config["screenshot_hotkey"] = self.hotkey_var.get().lower()
        
        if self.save_config():
            messagebox.showinfo("成功", "设置已应用！\n需要重启程序使部分设置生效。")
        else:
            messagebox.showerror("错误", "应用设置失败！")
    
    def on_closing(self):
        """窗口关闭事件"""
        self.window.destroy()
    
    def run(self):
        """运行设置窗口"""
        self.create_window()
        self.window.mainloop()

def open_modern_settings_window():
    """打开现代化设置窗口（供主程序调用）"""
    try:
        setup = ModernSeekieSetup()
        setup.run()
    except Exception as e:
        print(f"打开现代化设置窗口失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 独立运行测试
    open_modern_settings_window()
