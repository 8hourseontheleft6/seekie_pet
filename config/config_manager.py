"""
配置管理器 - 增强版
提供配置加载、保存、验证和版本管理功能
"""

import json
import os
import logging
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# 配置版本
CONFIG_VERSION = "3.3.0"

class Theme(Enum):
    """主题枚举"""
    LEMON_YELLOW = "lemon-yellow"
    SKY_BLUE = "sky-blue"
    APPLE_GREEN = "apple-green"
    PURPLE_DREAM = "purple-dream"
    SUNSET_ORANGE = "sunset-orange"
    DEEP_BLUE = "deep-blue"
    DARK_MODE = "dark-mode"

@dataclass
class RobotConfig:
    """机器人配置"""
    move_interval: int = 20  # 运动间隔（秒）
    move_speed: float = 1.5  # 运动速度
    robot_size: int = 50     # 机器人大小
    robot_color: str = "#4169E1"  # 机器人颜色（后备）
    
@dataclass
class HotkeyConfig:
    """快捷键配置"""
    screenshot: str = "ctrl+j"  # 截图快捷键
    toggle_visibility: str = ""  # 显示/隐藏快捷键
    increase_speed: str = ""    # 加速快捷键
    decrease_speed: str = ""    # 减速快捷键
    
@dataclass
class AppearanceConfig:
    """外观配置"""
    theme: Theme = Theme.LEMON_YELLOW
    transparency: float = 0.99  # 窗口透明度
    always_on_top: bool = True  # 始终置顶
    show_sleep_indicator: bool = True  # 显示睡眠指示器
    
@dataclass
class BehaviorConfig:
    """行为配置"""
    inactivity_threshold: int = 10  # 无活动阈值（秒）
    enable_sleep_mode: bool = True  # 启用睡眠模式
    enable_input_detection: bool = True  # 启用输入检测
    move_only_on_right_side: bool = True  # 仅在右半边移动
    
@dataclass
class AppConfig:
    """应用配置"""
    version: str = CONFIG_VERSION
    window_title: str = "Seekie Pet"
    enable_logging: bool = True
    log_level: str = "INFO"
    
    # 子配置
    robot: RobotConfig = None
    hotkeys: HotkeyConfig = None
    appearance: AppearanceConfig = None
    behavior: BehaviorConfig = None
    
    def __post_init__(self):
        """初始化子配置"""
        if self.robot is None:
            self.robot = RobotConfig()
        if self.hotkeys is None:
            self.hotkeys = HotkeyConfig()
        if self.appearance is None:
            self.appearance = AppearanceConfig()
        if self.behavior is None:
            self.behavior = BehaviorConfig()

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config: Optional[AppConfig] = None
        self.logger = logging.getLogger(__name__)
        
    def load(self) -> AppConfig:
        """加载配置"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 迁移旧版本配置
                data = self._migrate_config(data)
                
                # 创建配置对象
                self.config = self._dict_to_config(data)
                self.logger.info(f"配置加载成功: {self.config_path}")
                
            else:
                # 创建默认配置
                self.config = AppConfig()
                self.save()
                self.logger.info(f"创建默认配置: {self.config_path}")
                
        except Exception as e:
            self.logger.error(f"加载配置失败: {e}")
            # 使用默认配置
            self.config = AppConfig()
            
        return self.config
    
    def save(self) -> bool:
        """保存配置"""
        try:
            if self.config is None:
                self.config = AppConfig()
            
            # 确保版本是最新的
            self.config.version = CONFIG_VERSION
            
            # 转换为字典
            data = self._config_to_dict(self.config)
            
            # 保存到文件
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"配置保存成功: {self.config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"保存配置失败: {e}")
            return False
    
    def update(self, **kwargs) -> bool:
        """更新配置"""
        try:
            if self.config is None:
                self.load()
            
            # 更新配置
            for key, value in kwargs.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
                else:
                    # 尝试更新子配置
                    self._update_nested_config(key, value)
            
            return self.save()
            
        except Exception as e:
            self.logger.error(f"更新配置失败: {e}")
            return False
    
    def _update_nested_config(self, key: str, value: Any):
        """更新嵌套配置"""
        parts = key.split('.')
        if len(parts) == 2:
            parent, child = parts
            if hasattr(self.config, parent):
                parent_obj = getattr(self.config, parent)
                if hasattr(parent_obj, child):
                    setattr(parent_obj, child, value)
    
    def _migrate_config(self, data: Dict) -> Dict:
        """迁移旧版本配置"""
        version = data.get('version', '1.0.0')
        
        if version == '1.0.0' or version.startswith('3.2'):
            # 从3.2.x迁移到3.3.0
            migrated = {
                'version': CONFIG_VERSION,
                'window_title': data.get('window_title', 'Seekie Pet'),
                'enable_logging': True,
                'log_level': 'INFO',
                'robot': {
                    'move_interval': data.get('move_interval', 20),
                    'move_speed': data.get('move_speed', 1.5),
                    'robot_size': 50,
                    'robot_color': '#4169E1'
                },
                'hotkeys': {
                    'screenshot': data.get('screenshot_hotkey', 'ctrl+j'),
                    'toggle_visibility': '',
                    'increase_speed': '',
                    'decrease_speed': ''
                },
                'appearance': {
                    'theme': data.get('theme', 'lemon-yellow'),
                    'transparency': 0.99,
                    'always_on_top': True,
                    'show_sleep_indicator': True
                },
                'behavior': {
                    'inactivity_threshold': 10,
                    'enable_sleep_mode': True,
                    'enable_input_detection': True,
                    'move_only_on_right_side': True
                }
            }
            return migrated
        
        return data
    
    def _config_to_dict(self, config: AppConfig) -> Dict:
        """配置对象转换为字典"""
        data = asdict(config)
        
        # 处理枚举类型
        if 'appearance' in data and 'theme' in data['appearance']:
            if isinstance(data['appearance']['theme'], Theme):
                data['appearance']['theme'] = data['appearance']['theme'].value
        
        return data
    
    def _dict_to_config(self, data: Dict) -> AppConfig:
        """字典转换为配置对象"""
        # 处理主题枚举
        if 'appearance' in data and 'theme' in data['appearance']:
            theme_value = data['appearance']['theme']
            try:
                data['appearance']['theme'] = Theme(theme_value)
            except ValueError:
                data['appearance']['theme'] = Theme.LEMON_YELLOW
        
        # 创建配置对象
        config = AppConfig(
            version=data.get('version', CONFIG_VERSION),
            window_title=data.get('window_title', 'Seekie Pet'),
            enable_logging=data.get('enable_logging', True),
            log_level=data.get('log_level', 'INFO'),
            robot=RobotConfig(**data.get('robot', {})),
            hotkeys=HotkeyConfig(**data.get('hotkeys', {})),
            appearance=AppearanceConfig(**data.get('appearance', {})),
            behavior=BehaviorConfig(**data.get('behavior', {}))
        )
        
        return config
    
    def validate(self) -> bool:
        """验证配置"""
        if self.config is None:
            return False
        
        try:
            # 验证机器人配置
            if not (5 <= self.config.robot.move_interval <= 60):
                self.logger.warning(f"运动间隔超出范围: {self.config.robot.move_interval}")
                self.config.robot.move_interval = max(5, min(60, self.config.robot.move_interval))
            
            if not (0.5 <= self.config.robot.move_speed <= 5.0):
                self.logger.warning(f"运动速度超出范围: {self.config.robot.move_speed}")
                self.config.robot.move_speed = max(0.5, min(5.0, self.config.robot.move_speed))
            
            # 验证外观配置
            if not (0.1 <= self.config.appearance.transparency <= 1.0):
                self.logger.warning(f"透明度超出范围: {self.config.appearance.transparency}")
                self.config.appearance.transparency = max(0.1, min(1.0, self.config.appearance.transparency))
            
            return True
            
        except Exception as e:
            self.logger.error(f"配置验证失败: {e}")
            return False
    
    def export(self, export_path: str) -> bool:
        """导出配置"""
        try:
            if self.config is None:
                self.load()
            
            data = self._config_to_dict(self.config)
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"配置导出成功: {export_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"配置导出失败: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """导入配置"""
        try:
            if os.path.exists(import_path):
                with open(import_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.config = self._dict_to_config(data)
                return self.save()
            
            return False
            
        except Exception as e:
            self.logger.error(f"配置导入失败: {e}")
            return False

# 单例实例
_config_manager: Optional[ConfigManager] = None

def get_config_manager(config_path: str = "config.json") -> ConfigManager:
    """获取配置管理器实例"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_path)
        _config_manager.load()
    return _config_manager

def get_config() -> AppConfig:
    """获取当前配置"""
    manager = get_config_manager()
    return manager.config
