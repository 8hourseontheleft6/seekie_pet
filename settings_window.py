#!/usr/bin/env python3
"""
Seekie Setup - 桌面宠物机器人设置窗口
简洁美观的设置界面，参考Microsoft Word编辑器风格
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import threading

class SeekieSetup:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.window = None
        
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
        """创建设置窗口"""
        self.window = tk.Tk()
        self.window.title(self.config.get("window_title", "Seekie Setup"))
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        
        # 设置窗口图标（如果有的话）
        try:
            self.window.iconbitmap(default='icon.ico')
        except:
            pass
        
        # 设置窗口背景色（浅灰色，类似Word）
        self.window.configure(bg='#f0f0f0')
        
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题标签
        title_label = ttk.Label(
            main_frame,
            text="Seekie Setup",
            font=("Segoe UI", 16, "bold"),
            foreground="#2E74B5"  # Word蓝色
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 分隔线
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # 运动间隔设置
        interval_frame = ttk.LabelFrame(main_frame, text="运动设置", padding="10")
        interval_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # 运动间隔标签和滑块
        interval_label = ttk.Label(
            interval_frame,
            text="两次运动之间的间隔（秒）:",
            font=("Segoe UI", 10)
        )
        interval_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.interval_var = tk.IntVar(value=self.config.get("move_interval", 20))
        interval_slider = ttk.Scale(
            interval_frame,
            from_=5,
            to=60,
            orient=tk.HORIZONTAL,
            variable=self.interval_var,
            length=300,
            command=lambda v: self.update_interval_label()
        )
        interval_slider.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.interval_value_label = ttk.Label(
            interval_frame,
            text=f"{self.interval_var.get()} 秒",
            font=("Segoe UI", 9, "bold"),
            foreground="#2E74B5"
        )
        self.interval_value_label.grid(row=1, column=1, padx=(10, 0))
        
        # 运动速度设置
        speed_label = ttk.Label(
            interval_frame,
            text="运动速度:",
            font=("Segoe UI", 10)
        )
        speed_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        self.speed_var = tk.DoubleVar(value=self.config.get("move_speed", 1.5))
        speed_slider = ttk.Scale(
            interval_frame,
            from_=0.5,
            to=5.0,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            length=300,
            command=lambda v: self.update_speed_label()
        )
        speed_slider.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.speed_value_label = ttk.Label(
            interval_frame,
            text=f"{self.speed_var.get():.1f}",
            font=("Segoe UI", 9, "bold"),
            foreground="#2E74B5"
        )
        self.speed_value_label.grid(row=3, column=1, padx=(10, 0))
        
        # 快捷键设置
        hotkey_frame = ttk.LabelFrame(main_frame, text="快捷键设置", padding="10")
        hotkey_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        hotkey_label = ttk.Label(
            hotkey_frame,
            text="打开截图软件的快捷键:",
            font=("Segoe UI", 10)
        )
        hotkey_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.hotkey_var = tk.StringVar(value=self.config.get("screenshot_hotkey", "ctrl+j"))
        hotkey_entry = ttk.Entry(
            hotkey_frame,
            textvariable=self.hotkey_var,
            font=("Segoe UI", 10),
            width=20
        )
        hotkey_entry.grid(row=0, column=1, padx=(10, 0))
        
        hotkey_hint = ttk.Label(
            hotkey_frame,
            text="格式: ctrl+key, alt+key, shift+key (例如: ctrl+j, alt+s)",
            font=("Segoe UI", 8),
            foreground="#666666"
        )
        hotkey_hint.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        # 保存按钮
        save_button = ttk.Button(
            button_frame,
            text="保存设置",
            command=self.save_settings,
            style="Accent.TButton"
        )
        save_button.grid(row=0, column=0, padx=(0, 10))
        
        # 取消按钮
        cancel_button = ttk.Button(
            button_frame,
            text="取消",
            command=self.window.destroy
        )
        cancel_button.grid(row=0, column=1, padx=(10, 0))
        
        # 应用按钮
        apply_button = ttk.Button(
            button_frame,
            text="应用",
            command=self.apply_settings
        )
        apply_button.grid(row=0, column=2, padx=(10, 0))
        
        # 配置网格权重
        main_frame.columnconfigure(0, weight=1)
        interval_frame.columnconfigure(0, weight=1)
        hotkey_frame.columnconfigure(0, weight=1)
        
        # 设置样式
        self.setup_styles()
        
        # 绑定窗口关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """设置Tkinter样式"""
        style = ttk.Style()
        
        # 设置主题
        style.theme_use('clam')
        
        # 配置标签框架样式
        style.configure(
            'TLabelframe',
            background='#f0f0f0',
            bordercolor='#d0d0d0'
        )
        style.configure(
            'TLabelframe.Label',
            background='#f0f0f0',
            foreground='#2E74B5',
            font=('Segoe UI', 10, 'bold')
        )
        
        # 配置按钮样式
        style.configure(
            'TButton',
            font=('Segoe UI', 10),
            padding=6
        )
        
        # 强调按钮样式（保存按钮）
        style.configure(
            'Accent.TButton',
            background='#2E74B5',
            foreground='white',
            font=('Segoe UI', 10, 'bold')
        )
        style.map(
            'Accent.TButton',
            background=[('active', '#1C5A9E'), ('pressed', '#16487D')]
        )
        
        # 配置标签样式
        style.configure(
            'TLabel',
            background='#f0f0f0',
            font=('Segoe UI', 10)
        )
        
        # 配置滑块样式
        style.configure(
            'Horizontal.TScale',
            background='#f0f0f0'
        )
    
    def update_interval_label(self):
        """更新间隔标签"""
        self.interval_value_label.config(text=f"{self.interval_var.get()} 秒")
    
    def update_speed_label(self):
        """更新速度标签"""
        self.speed_value_label.config(text=f"{self.speed_var.get():.1f}")
    
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

def open_settings_window():
    """打开设置窗口（供主程序调用）"""
    try:
        setup = SeekieSetup()
        setup.run()
    except Exception as e:
        print(f"打开设置窗口失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 独立运行测试
    open_settings_window()
