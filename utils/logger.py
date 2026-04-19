"""
日志记录器 - 增强版
提供文件和控制台日志记录功能
"""

import logging
import os
import sys
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler

class Logger:
    """日志记录器"""
    
    def __init__(self, name: str = "seekie_pet", log_dir: str = "logs", 
                 max_file_size: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5):
        self.name = name
        self.log_dir = log_dir
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        self.logger: Optional[logging.Logger] = None
        
        # 创建日志目录
        os.makedirs(log_dir, exist_ok=True)
        
    def setup(self, level: str = "INFO", enable_file: bool = True, 
              enable_console: bool = True) -> logging.Logger:
        """设置日志记录器"""
        # 创建logger
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        
        # 清除现有的处理器
        self.logger.handlers.clear()
        
        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 文件处理器
        if enable_file:
            log_file = os.path.join(self.log_dir, f"{self.name}.log")
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=self.max_file_size,
                backupCount=self.backup_count,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            self.logger.addHandler(file_handler)
        
        # 控制台处理器
        if enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
            self.logger.addHandler(console_handler)
        
        return self.logger
    
    def get_logger(self) -> logging.Logger:
        """获取日志记录器"""
        if self.logger is None:
            return self.setup()
        return self.logger
    
    def log_startup(self):
        """记录启动信息"""
        if self.logger:
            self.logger.info("=" * 50)
            self.logger.info("Seekie Pet 启动")
            self.logger.info(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.logger.info("=" * 50)
    
    def log_shutdown(self):
        """记录关闭信息"""
        if self.logger:
            self.logger.info("=" * 50)
            self.logger.info("Seekie Pet 关闭")
            self.logger.info(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.logger.info("=" * 50)
    
    def log_error_with_traceback(self, error: Exception, context: str = ""):
        """记录错误和堆栈跟踪"""
        if self.logger:
            if context:
                self.logger.error(f"{context}: {error}")
            else:
                self.logger.error(f"错误: {error}")
            
            import traceback
            self.logger.debug(f"堆栈跟踪:\n{traceback.format_exc()}")
    
    def log_config_change(self, config_name: str, old_value, new_value):
        """记录配置变更"""
        if self.logger:
            self.logger.info(f"配置变更: {config_name} = {old_value} -> {new_value}")
    
    def log_performance(self, operation: str, duration: float):
        """记录性能信息"""
        if self.logger:
            self.logger.debug(f"性能: {operation} 耗时 {duration:.3f}秒")
    
    def cleanup_old_logs(self, days_to_keep: int = 30):
        """清理旧日志文件"""
        try:
            import glob
            from datetime import datetime, timedelta
            
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # 查找所有日志文件
            log_files = glob.glob(os.path.join(self.log_dir, "*.log*"))
            
            for log_file in log_files:
                try:
                    # 获取文件修改时间
                    mtime = datetime.fromtimestamp(os.path.getmtime(log_file))
                    
                    if mtime < cutoff_date:
                        os.remove(log_file)
                        if self.logger:
                            self.logger.info(f"清理旧日志文件: {log_file}")
                except Exception as e:
                    if self.logger:
                        self.logger.warning(f"无法清理日志文件 {log_file}: {e}")
                        
        except Exception as e:
            if self.logger:
                self.logger.error(f"清理旧日志失败: {e}")

# 全局日志记录器实例
_logger_instance: Optional[Logger] = None

def get_logger(name: str = "seekie_pet", **kwargs) -> logging.Logger:
    """获取全局日志记录器"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = Logger(name, **kwargs)
    return _logger_instance.get_logger()

def setup_logging(level: str = "INFO", enable_file: bool = True, 
                  enable_console: bool = True, **kwargs) -> logging.Logger:
    """设置全局日志记录"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = Logger(**kwargs)
    return _logger_instance.setup(level, enable_file, enable_console)

# 便捷函数
def info(msg: str, *args, **kwargs):
    """记录信息级别日志"""
    logger = get_logger()
    logger.info(msg, *args, **kwargs)

def debug(msg: str, *args, **kwargs):
    """记录调试级别日志"""
    logger = get_logger()
    logger.debug(msg, *args, **kwargs)

def warning(msg: str, *args, **kwargs):
    """记录警告级别日志"""
    logger = get_logger()
    logger.warning(msg, *args, **kwargs)

def error(msg: str, *args, **kwargs):
    """记录错误级别日志"""
    logger = get_logger()
    logger.error(msg, *args, **kwargs)

def critical(msg: str, *args, **kwargs):
    """记录严重级别日志"""
    logger = get_logger()
    logger.critical(msg, *args, **kwargs)

def exception(msg: str, *args, **kwargs):
    """记录异常级别日志"""
    logger = get_logger()
    logger.exception(msg, *args, **kwargs)
