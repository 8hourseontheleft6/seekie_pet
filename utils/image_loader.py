"""
图片加载器 - 增强版
提供图片加载、缓存和错误处理功能
"""

import os
from typing import Optional, Tuple, Dict
from PIL import Image, ImageDraw
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ImageType(Enum):
    """图片类型枚举"""
    ROBOT = "robot"
    SLEEP = "sleep"
    TRAY = "tray"
    ICON = "icon"

@dataclass
class ImageCacheItem:
    """图片缓存项"""
    image: Image.Image
    path: str
    size: Tuple[int, int]
    timestamp: float

class ImageLoader:
    """图片加载器"""
    
    def __init__(self, base_dir: str = "main_pic"):
        # 转换为绝对路径
        if not os.path.isabs(base_dir):
            # 相对于当前工作目录
            current_working_dir = os.getcwd()
            self.base_dir = os.path.join(current_working_dir, base_dir)
        else:
            self.base_dir = base_dir
            
        self.cache: Dict[str, ImageCacheItem] = {}
        self.default_colors = {
            'robot': '#4169E1',
            'sleep': '#6495ED',
            'tray': '#1E90FF'
        }
        
        # 确保目录存在
        os.makedirs(self.base_dir, exist_ok=True)
        logger.info(f"图片加载器初始化，基础目录: {self.base_dir}")
        logger.info(f"当前工作目录: {os.getcwd()}")
    
    def get_image_path(self, image_type: ImageType, filename: Optional[str] = None) -> str:
        """获取图片路径"""
        if filename:
            return os.path.join(self.base_dir, filename)
        
        # 默认文件名
        defaults = {
            ImageType.ROBOT: "Robot_50x50.png",
            ImageType.SLEEP: "Sleep.png",
            ImageType.TRAY: "robot-icon.png",
            ImageType.ICON: "Robot_50x50.png"
        }
        
        image_path = os.path.join(self.base_dir, defaults.get(image_type, "Robot_50x50.png"))
        logger.debug(f"获取图片路径: {image_type.value} -> {image_path}")
        return image_path
    
    def load_image(self, image_type: ImageType, size: Optional[Tuple[int, int]] = None, 
                   filename: Optional[str] = None) -> Optional[Image.Image]:
        """加载图片"""
        try:
            image_path = self.get_image_path(image_type, filename)
            
            # 检查缓存
            cache_key = f"{image_path}_{size}"
            if cache_key in self.cache:
                logger.debug(f"从缓存加载图片: {cache_key}")
                return self.cache[cache_key].image.copy()
            
            # 加载图片
            if os.path.exists(image_path):
                image = Image.open(image_path)
                logger.info(f"图片加载成功: {image_path} ({image.size})")
            else:
                logger.warning(f"图片不存在，创建默认图片: {image_path}")
                image = self.create_default_image(image_type, size)
            
            # 调整大小
            if size and image.size != size:
                image = self.resize_image(image, size)
                logger.debug(f"图片调整大小: {image.size} -> {size}")
            
            # 转换为RGBA模式（确保透明度支持）
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
                logger.debug(f"图片转换为RGBA模式")
            
            # 缓存图片
            import time
            self.cache[cache_key] = ImageCacheItem(
                image=image.copy(),
                path=image_path,
                size=size or image.size,
                timestamp=time.time()
            )
            
            return image
            
        except Exception as e:
            logger.error(f"加载图片失败: {e}")
            return self.create_default_image(image_type, size)
    
    def create_default_image(self, image_type: ImageType, size: Optional[Tuple[int, int]] = None) -> Image.Image:
        """创建默认图片"""
        size = size or (50, 50)
        color = self.default_colors.get(image_type.value, '#4169E1')
        
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        if image_type == ImageType.ROBOT:
            # 创建机器人图标
            self._draw_robot(draw, size, color)
        elif image_type == ImageType.SLEEP:
            # 创建睡眠图标
            self._draw_sleep_robot(draw, size, color)
        elif image_type == ImageType.TRAY:
            # 创建托盘图标
            self._draw_tray_icon(draw, size, color)
        else:
            # 创建默认图标
            self._draw_default_icon(draw, size, color)
        
        logger.info(f"创建默认图片: {image_type.value} {size}")
        return image
    
    def _draw_robot(self, draw: ImageDraw.Draw, size: Tuple[int, int], color: str):
        """绘制机器人"""
        width, height = size
        padding = max(2, min(width, height) // 10)
        
        # 机器人身体
        body_rect = [padding, padding, width - padding, height - padding]
        draw.rectangle(body_rect, fill=color, outline=self._darken_color(color), width=2)
        
        # 机器人眼睛
        eye_size = max(2, min(width, height) // 6)
        left_eye = [width // 3, height // 3]
        right_eye = [2 * width // 3, height // 3]
        
        draw.rectangle(
            [left_eye[0] - eye_size//2, left_eye[1] - eye_size//2,
             left_eye[0] + eye_size//2, left_eye[1] + eye_size//2],
            fill='#FFFFFF', outline=self._darken_color(color), width=1
        )
        
        draw.rectangle(
            [right_eye[0] - eye_size//2, right_eye[1] - eye_size//2,
             right_eye[0] + eye_size//2, right_eye[1] + eye_size//2],
            fill='#FFFFFF', outline=self._darken_color(color), width=1
        )
        
        # 机器人嘴巴
        mouth_y = 2 * height // 3
        draw.line(
            [width // 3, mouth_y, 2 * width // 3, mouth_y],
            fill='#FFFFFF', width=2
        )
    
    def _draw_sleep_robot(self, draw: ImageDraw.Draw, size: Tuple[int, int], color: str):
        """绘制睡眠机器人"""
        width, height = size
        padding = max(2, min(width, height) // 10)
        
        # 机器人身体
        body_rect = [padding, padding, width - padding, height - padding]
        draw.rectangle(body_rect, fill=color, outline=self._darken_color(color), width=2)
        
        # 闭眼（横线）
        eye_y = height // 3
        draw.line(
            [width // 3 - 5, eye_y, width // 3 + 5, eye_y],
            fill='#FFFFFF', width=3
        )
        
        draw.line(
            [2 * width // 3 - 5, eye_y, 2 * width // 3 + 5, eye_y],
            fill='#FFFFFF', width=3
        )
        
        # ZZZ睡眠符号
        from PIL import ImageFont
        try:
            font = ImageFont.truetype("arial.ttf", max(8, height // 6))
        except:
            font = None
        
        draw.text(
            (width // 2, 2 * height // 3),
            "Zz", fill='#FFFFFF', font=font, anchor="mm"
        )
    
    def _draw_tray_icon(self, draw: ImageDraw.Draw, size: Tuple[int, int], color: str):
        """绘制托盘图标"""
        width, height = size
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 2 - 2
        
        # 圆形背景
        draw.ellipse(
            [center_x - radius, center_y - radius,
             center_x + radius, center_y + radius],
            fill=color, outline=self._darken_color(color), width=2
        )
        
        # 机器人简图
        robot_size = radius // 2
        draw.rectangle(
            [center_x - robot_size, center_y - robot_size,
             center_x + robot_size, center_y + robot_size],
            fill='#FFFFFF', outline=self._darken_color(color), width=1
        )
    
    def _draw_default_icon(self, draw: ImageDraw.Draw, size: Tuple[int, int], color: str):
        """绘制默认图标"""
        width, height = size
        draw.rectangle([0, 0, width, height], fill=color)
        
        # 添加"S"字母
        from PIL import ImageFont
        try:
            font = ImageFont.truetype("arial.ttf", max(12, min(width, height) // 2))
        except:
            font = None
        
        draw.text(
            (width // 2, height // 2),
            "S", fill='#FFFFFF', font=font, anchor="mm"
        )
    
    def resize_image(self, image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        """调整图片大小"""
        return image.resize(size, Image.Resampling.LANCZOS)
    
    def _darken_color(self, color: str, factor: float = 0.7) -> str:
        """加深颜色"""
        try:
            from PIL import ImageColor
            rgb = ImageColor.getrgb(color)
            darkened = tuple(int(c * factor) for c in rgb)
            return f'#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}'
        except:
            return '#1E3A8A'  # 默认深蓝色
    
    def clear_cache(self, older_than: Optional[float] = None):
        """清理缓存"""
        import time
        current_time = time.time()
        
        if older_than is None:
            self.cache.clear()
            logger.info("图片缓存已清空")
        else:
            # 清理过期缓存
            keys_to_remove = []
            for key, item in self.cache.items():
                if current_time - item.timestamp > older_than:
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                del self.cache[key]
            
            logger.info(f"清理了 {len(keys_to_remove)} 个过期缓存项")
    
    def get_image_info(self, image_path: str) -> Optional[Dict]:
        """获取图片信息"""
        try:
            if os.path.exists(image_path):
                with Image.open(image_path) as img:
                    return {
                        'path': image_path,
                        'size': img.size,
                        'mode': img.mode,
                        'format': img.format,
                        'width': img.width,
                        'height': img.height
                    }
        except Exception as e:
            logger.error(f"获取图片信息失败: {e}")
        
        return None
    
    def validate_image(self, image_path: str, expected_size: Optional[Tuple[int, int]] = None) -> bool:
        """验证图片"""
        try:
            info = self.get_image_info(image_path)
            if not info:
                return False
            
            # 检查格式
            if info['format'] not in ['PNG', 'JPEG', 'GIF']:
                logger.warning(f"不支持的图片格式: {info['format']}")
                return False
            
            # 检查大小
            if expected_size and info['size'] != expected_size:
                logger.warning(f"图片大小不匹配: {info['size']} != {expected_size}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"验证图片失败: {e}")
            return False

# 全局图片加载器实例
_image_loader: Optional[ImageLoader] = None

def get_image_loader(base_dir: str = "main_pic") -> ImageLoader:
    """获取全局图片加载器"""
    global _image_loader
    if _image_loader is None:
        _image_loader = ImageLoader(base_dir)
    return _image_loader

def load_robot_image(size: Optional[Tuple[int, int]] = None) -> Optional[Image.Image]:
    """加载机器人图片"""
    loader = get_image_loader()
    return loader.load_image(ImageType.ROBOT, size)

def load_sleep_image(size: Optional[Tuple[int, int]] = None) -> Optional[Image.Image]:
    """加载睡眠图片"""
    loader = get_image_loader()
    return loader.load_image(ImageType.SLEEP, size)

def load_tray_image(size: Optional[Tuple[int, int]] = None) -> Optional[Image.Image]:
    """加载托盘图片"""
    loader = get_image_loader()
    return loader.load_image(ImageType.TRAY, size)
