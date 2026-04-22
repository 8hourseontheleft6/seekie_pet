"""动画管理模块"""

import os
from PIL import Image, ImageTk, ImageDraw
from utils.logger import info, error


class AnimationManager:
    """管理动画加载和播放"""
    
    def __init__(self, config):
        self.config = config
        self.robot_photo = None
        self.sleep_photo = None
        self.animation_frames = []
        self.current_frame = 0
        self.is_hovering = False
        self.animation_running = False
    
    def load_images(self):
        """加载所有图片资源"""
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # 加载机器人图片
            self.robot_photo = self._load_single_image(
                os.path.join(current_dir, "main_pic", "Robot_50x50.png"),
                "机器人图片"
            )
            
            # 加载睡眠图片
            self.sleep_photo = self._load_single_image(
                os.path.join(current_dir, "main_pic", "Sleep.png"),
                "睡眠图片"
            )
            
            # 加载动画精灵图
            self._load_animation_sprite(current_dir)
            
            info(f"图片加载完成: 机器人={self.robot_photo is not None}, "
                 f"睡眠={self.sleep_photo is not None}, "
                 f"动画帧={len(self.animation_frames)}")
            
        except Exception as e:
            error(f"图片加载失败: {e}")
            self._create_default_images()
    
    def _load_single_image(self, path, name):
        """加载单张图片"""
        if os.path.exists(path):
            img = Image.open(path)
            if img.size != (self.config.robot.robot_size, self.config.robot.robot_size):
                img = img.resize((self.config.robot.robot_size, self.config.robot.robot_size), 
                                 Image.Resampling.LANCZOS)
            info(f"[成功] {name}加载成功: {path}")
            return ImageTk.PhotoImage(img)
        else:
            error(f"[警告] {name}不存在: {path}")
            return None
    
    def _load_animation_sprite(self, current_dir):
        """加载动画精灵图"""
        animation_path = os.path.join(current_dir, "main_pic", "see-left-and-right.png")
        info(f"加载动画精灵图: {animation_path}")
        
        if os.path.exists(animation_path):
            sprite_sheet = Image.open(animation_path)
            info(f"精灵图尺寸: {sprite_sheet.size}")
            
            frame_height = 50
            frame_width = 50
            total_frames = sprite_sheet.height // frame_height
            
            info(f"检测到 {total_frames} 帧动画 (每帧{frame_width}x{frame_height})")
            
            self.animation_frames = []
            for i in range(total_frames):
                frame = sprite_sheet.crop((0, i * frame_height, frame_width, (i + 1) * frame_height))
                if frame.size != (self.config.robot.robot_size, self.config.robot.robot_size):
                    frame = frame.resize((self.config.robot.robot_size, self.config.robot.robot_size), 
                                         Image.Resampling.LANCZOS)
                self.animation_frames.append(ImageTk.PhotoImage(frame))
            
            info(f"[成功] 动画精灵图加载成功，共{len(self.animation_frames)}帧")
        else:
            error("[警告] 动画精灵图不存在，创建默认动画")
            self._create_default_animation()
    
    def _create_default_images(self):
        """创建默认图片（当图片文件不存在时）"""
        try:
            size = self.config.robot.robot_size
            
            # 默认机器人图片
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.rectangle([10, 10, 40, 40], fill='#4169E1', outline='#1E3A8A', width=2)
            self.robot_photo = ImageTk.PhotoImage(img)
            
            # 默认睡眠图片
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.rectangle([10, 10, 40, 40], fill='#4169E1', outline='#1E3A8A', width=2)
            draw.line([15, 17, 25, 17], fill='#FFFFFF', width=3)
            draw.line([30, 17, 35, 17], fill='#FFFFFF', width=3)
            self.sleep_photo = ImageTk.PhotoImage(img)
            
            self._create_default_animation()
            info("使用默认图片")
        except Exception as e:
            error(f"创建默认图片失败: {e}")
    
    def _create_default_animation(self):
        """创建默认动画"""
        try:
            size = self.config.robot.robot_size
            self.animation_frames = []
            
            for i in range(6):
                img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                draw.rectangle([10, 10, 40, 40], fill='#4169E1', outline='#1E3A8A', width=2)
                
                eye_offset = (i - 2.5) * 3
                left_eye_x = 20 + eye_offset
                right_eye_x = 30 + eye_offset
                
                draw.ellipse([left_eye_x, 15, left_eye_x + 5, 20], fill='white')
                draw.ellipse([right_eye_x, 15, right_eye_x + 5, 20], fill='white')
                
                self.animation_frames.append(ImageTk.PhotoImage(img))
            
            info(f"创建默认动画，共{len(self.animation_frames)}帧")
        except Exception as e:
            error(f"创建默认动画失败: {e}")
            self.animation_frames = []
    
    def get_current_photo(self, is_sleeping):
        """获取当前应显示的图片"""
        if is_sleeping and self.sleep_photo:
            return self.sleep_photo
        elif self.is_hovering and self.animation_frames:
            if self.current_frame < len(self.animation_frames):
                return self.animation_frames[self.current_frame]
        return self.robot_photo
    
    def next_frame(self):
        """切换到下一帧"""
        if not self.animation_frames:
            return
        self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
    
    def start_hover(self):
        """开始悬停动画"""
        self.is_hovering = True
        self.animation_running = True
        self.current_frame = 0
    
    def stop_hover(self):
        """停止悬停动画"""
        self.is_hovering = False
        self.animation_running = False
