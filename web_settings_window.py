#!/usr/bin/env python3
"""
Seekie Web Settings Window - 独立窗口版设置窗口
使用tkinterweb在tkinter窗口中显示HTML内容，不打开浏览器
"""

import json
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk
from tkinterweb import HtmlFrame
from flask import Flask, render_template, request, jsonify

class WebSettingsWindow:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.window = None
        self.html_frame = None
        self.flask_app = None
        self.flask_thread = None
        
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
    
    def create_flask_app(self):
        """创建Flask应用"""
        app = Flask(__name__)
        
        @app.route('/')
        def index():
            return render_template('index.html')
        
        @app.route('/api/config', methods=['GET'])
        def get_config():
            return jsonify(self.config)
        
        @app.route('/api/config', methods=['POST'])
        def update_config():
            try:
                data = request.json
                self.config.update(data)
                if self.save_config():
                    return jsonify({"success": True, "message": "设置已保存"})
                else:
                    return jsonify({"success": False, "message": "保存失败"})
            except Exception as e:
                return jsonify({"success": False, "message": str(e)})
        
        @app.route('/api/test-hotkey', methods=['POST'])
        def test_hotkey():
            # 这里可以添加测试快捷键的功能
            return jsonify({"success": True, "message": "快捷键测试功能待实现"})
        
        return app
    
    def start_flask_server(self, port=5001):
        """启动Flask服务器"""
        self.flask_app = self.create_flask_app()
        self.flask_app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)
    
    def create_window(self):
        """创建主窗口"""
        self.window = tk.Tk()
        self.window.title("Seekie Setup - 桌面宠物机器人设置")
        self.window.geometry("900x600")
        
        # 设置窗口图标
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "main_pic", "Robot_50x50.png")
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                self.window.iconphoto(True, icon)
        except:
            pass
        
        # 创建HTML框架
        self.html_frame = HtmlFrame(self.window)
        self.html_frame.pack(fill="both", expand=True)
        
        # 启动Flask服务器
        self.flask_thread = threading.Thread(
            target=self.start_flask_server,
            daemon=True
        )
        self.flask_thread.start()
        
        # 等待服务器启动
        import time
        time.sleep(1)
        
        # 加载页面
        self.html_frame.load_url("http://127.0.0.1:5001/")
        
        # 窗口关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        return self.window
    
    def on_closing(self):
        """窗口关闭事件处理"""
        if self.window:
            self.window.destroy()
        self.window = None
    
    def run(self):
        """运行窗口"""
        if not self.window:
            self.create_window()
        self.window.mainloop()

def open_web_settings_window():
    """打开Web设置窗口"""
    try:
        # 确保模板目录存在 - 尝试多个可能的路径
        possible_template_dirs = [
            os.path.join(os.path.dirname(__file__), '..', 'seekie-settings-electron', 'templates'),
            os.path.join(os.path.dirname(__file__), 'templates'),
            os.path.join(os.path.dirname(__file__), 'seekie-settings-electron', 'templates'),
        ]
        
        template_dir = None
        for dir_path in possible_template_dirs:
            if os.path.exists(dir_path):
                template_dir = dir_path
                break
        
        if not template_dir:
            print(f"错误: 找不到模板目录，尝试的路径: {possible_template_dirs}")
            return False
        
        print(f"找到模板目录: {template_dir}")
        
        # 设置Flask模板目录
        import sys
        sys.path.insert(0, os.path.dirname(template_dir))
        
        # 创建并运行窗口
        app = WebSettingsWindow()
        app.run()
        return True
    except Exception as e:
        print(f"打开Web设置窗口失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 独立运行测试
    open_web_settings_window()
