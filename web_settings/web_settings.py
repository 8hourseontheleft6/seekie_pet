#!/usr/bin/env python3
"""
Seekie Web Settings - 基于Web技术的现代化设置窗口
使用Flask作为后端，HTML/CSS/JavaScript作为前端
"""

import json
import os
import sys
import threading
import webbrowser
from flask import Flask, render_template, request, jsonify

class WebSettingsApp:
    def __init__(self, config_path="../config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.app = Flask(__name__)
        self.setup_routes()
        
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
                    "window_title": "Seekie Setup",
                    "theme": "lemon-yellow"
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
    
    def setup_routes(self):
        """设置Flask路由"""
        
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
        @self.app.route('/api/config', methods=['GET'])
        def get_config():
            return jsonify(self.config)
        
        @self.app.route('/api/config', methods=['POST'])
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
        
        @self.app.route('/api/test-hotkey', methods=['POST'])
        def test_hotkey():
            # 这里可以添加测试快捷键的功能
            return jsonify({"success": True, "message": "快捷键测试功能待实现"})
    
    def run(self, host='127.0.0.1', port=5000):
        """运行Web应用"""
        # 在后台线程中启动Flask应用
        flask_thread = threading.Thread(
            target=lambda: self.app.run(
                host=host, 
                port=port, 
                debug=False, 
                use_reloader=False
            ),
            daemon=True
        )
        flask_thread.start()
        
        # 打开浏览器
        url = f"http://{host}:{port}"
        print(f"Seekie设置窗口已启动: {url}")
        webbrowser.open(url)
        
        # 保持主线程运行
        try:
            flask_thread.join()
        except KeyboardInterrupt:
            print("\n正在关闭设置窗口...")

def open_web_settings():
    """打开Web设置窗口"""
    try:
        # 确保模板目录存在
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        if not os.path.exists(template_dir):
            print(f"错误: 模板目录不存在: {template_dir}")
            return
        
        app = WebSettingsApp()
        app.run()
    except Exception as e:
        print(f"打开Web设置窗口失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 独立运行测试
    open_web_settings()
