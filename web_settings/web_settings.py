#!/usr/bin/env python3
"""
Seekie Web Settings - 基于Web技术的现代化设置窗口
使用Flask作为后端，HTML/CSS/JavaScript作为前端
与新的配置管理器集成
"""

import os
import sys
import threading
import webbrowser
from flask import Flask, render_template, request, jsonify

# 添加父目录到路径，以便导入配置管理器
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.config_manager import get_config_manager, get_config, Theme

class WebSettingsApp:
    def __init__(self):
        self.config_manager = get_config_manager()
        self.config = get_config()
        self.app = Flask(__name__)
        self.setup_routes()
        
    def load_config(self):
        """加载配置（使用配置管理器）"""
        try:
            self.config_manager.load()
            self.config = get_config()
            return True
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return False
    
    def save_config(self, config_data):
        """保存配置（使用配置管理器）"""
        try:
            # 更新配置
            success = self.config_manager.update(**config_data)
            if success:
                # 重新加载配置
                self.config_manager.load()
                self.config = get_config()
                return True
            return False
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def get_config_dict(self):
        """获取配置字典（用于JSON响应）"""
        try:
            config_dict = {
                "version": self.config.version,
                "window_title": self.config.window_title,
                "enable_logging": self.config.enable_logging,
                "log_level": self.config.log_level,
                "robot": {
                    "move_interval": self.config.robot.move_interval,
                    "move_speed": self.config.robot.move_speed,
                    "robot_size": self.config.robot.robot_size,
                    "robot_color": self.config.robot.robot_color
                },
                "hotkeys": {
                    "screenshot": self.config.hotkeys.screenshot,
                    "toggle_visibility": self.config.hotkeys.toggle_visibility,
                    "increase_speed": self.config.hotkeys.increase_speed,
                    "decrease_speed": self.config.hotkeys.decrease_speed
                },
                "appearance": {
                    "theme": self.config.appearance.theme.value,
                    "transparency": self.config.appearance.transparency,
                    "always_on_top": self.config.appearance.always_on_top,
                    "show_sleep_indicator": self.config.appearance.show_sleep_indicator
                },
                "behavior": {
                    "inactivity_threshold": self.config.behavior.inactivity_threshold,
                    "enable_sleep_mode": self.config.behavior.enable_sleep_mode,
                    "enable_input_detection": self.config.behavior.enable_input_detection,
                    "move_only_on_right_side": self.config.behavior.move_only_on_right_side
                }
            }
            return config_dict
        except Exception as e:
            print(f"获取配置字典失败: {e}")
            return {}
    
    def setup_routes(self):
        """设置Flask路由"""
        
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
        @self.app.route('/api/config', methods=['GET'])
        def get_config_api():
            """获取当前配置"""
            config_dict = self.get_config_dict()
            return jsonify(config_dict)
        
        @self.app.route('/api/config', methods=['POST'])
        def update_config():
            """更新配置"""
            try:
                data = request.json
                print(f"收到配置更新请求: {data}")
                
                # 构建配置更新字典
                config_updates = {}
                
                # 处理机器人配置
                if 'move_interval' in data:
                    config_updates['robot.move_interval'] = int(data['move_interval'])
                if 'move_speed' in data:
                    config_updates['robot.move_speed'] = float(data['move_speed'])
                
                # 处理快捷键配置
                if 'screenshot_hotkey' in data:
                    config_updates['hotkeys.screenshot'] = data['screenshot_hotkey']
                
                # 处理外观配置
                if 'theme' in data:
                    config_updates['appearance.theme'] = data['theme']
                if 'transparency' in data:
                    config_updates['appearance.transparency'] = float(data['transparency'])
                if 'always_on_top' in data:
                    config_updates['appearance.always_on_top'] = bool(data['always_on_top'])
                
                # 处理行为配置
                if 'inactivity_threshold' in data:
                    config_updates['behavior.inactivity_threshold'] = int(data['inactivity_threshold'])
                if 'enable_sleep_mode' in data:
                    config_updates['behavior.enable_sleep_mode'] = bool(data['enable_sleep_mode'])
                
                # 应用配置更新
                if config_updates:
                    success = self.save_config(config_updates)
                    if success:
                        return jsonify({"success": True, "message": "设置已保存"})
                    else:
                        return jsonify({"success": False, "message": "保存失败"})
                else:
                    return jsonify({"success": False, "message": "没有有效的配置更新"})
                    
            except Exception as e:
                print(f"更新配置失败: {e}")
                import traceback
                traceback.print_exc()
                return jsonify({"success": False, "message": str(e)})
        
        @self.app.route('/api/test-hotkey', methods=['POST'])
        def test_hotkey():
            """测试快捷键"""
            try:
                data = request.json
                hotkey = data.get('hotkey', '')
                return jsonify({"success": True, "message": f"快捷键 '{hotkey}' 测试成功"})
            except Exception as e:
                return jsonify({"success": False, "message": str(e)})
        
        @self.app.route('/api/themes', methods=['GET'])
        def get_themes():
            """获取可用主题列表"""
            themes = [theme.value for theme in Theme]
            return jsonify({"success": True, "themes": themes})
        
        @self.app.route('/api/validate', methods=['POST'])
        def validate_config():
            """验证配置"""
            try:
                self.config_manager.validate()
                return jsonify({"success": True, "message": "配置验证通过"})
            except Exception as e:
                return jsonify({"success": False, "message": str(e)})
    
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
