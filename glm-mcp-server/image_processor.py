#!/usr/bin/env python3
"""
图像处理模块
提供图像编码、解码和处理功能
"""

import os
import base64
import mimetypes
from typing import Optional, Tuple, Dict, Any
from PIL import Image
import io

try:
    from logger import logger
    LOGGER_AVAILABLE = True
except ImportError:
    import logging
    logger = logging.getLogger(__name__)
    LOGGER_AVAILABLE = False

class ImageProcessor:
    """图像处理器"""
    
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        
        if LOGGER_AVAILABLE:
            logger.info("图像处理器初始化成功")
    
    def is_supported_format(self, file_path: str) -> bool:
        """检查文件格式是否支持"""
        _, ext = os.path.splitext(file_path.lower())
        return ext in self.supported_formats
    
    def get_file_size(self, file_path: str) -> int:
        """获取文件大小"""
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            if LOGGER_AVAILABLE:
                logger.error(f"获取文件大小失败: {e}")
            return 0
    
    def is_file_size_valid(self, file_path: str) -> bool:
        """检查文件大小是否有效"""
        size = self.get_file_size(file_path)
        return size <= self.max_file_size
    
    def validate_image_file(self, file_path: str) -> Tuple[bool, str]:
        """验证图像文件"""
        if not os.path.exists(file_path):
            return False, f"文件不存在: {file_path}"
        
        if not self.is_supported_format(file_path):
            return False, f"不支持的图像格式: {file_path}"
        
        if not self.is_file_size_valid(file_path):
            return False, f"文件大小超过限制 (最大 {self.max_file_size // (1024*1024)}MB)"
        
        try:
            # 尝试打开图像文件
            with Image.open(file_path) as img:
                img.verify()
            return True, "文件验证通过"
        except Exception as e:
            return False, f"图像文件损坏: {str(e)}"
    
    def encode_image_to_base64(self, file_path: str) -> Optional[str]:
        """将图像文件编码为 base64"""
        try:
            # 验证文件
            is_valid, message = self.validate_image_file(file_path)
            if not is_valid:
                if LOGGER_AVAILABLE:
                    logger.error(f"图像验证失败: {message}")
                return None
            
            # 读取文件并编码
            with open(file_path, 'rb') as image_file:
                image_data = image_file.read()
                encoded_string = base64.b64encode(image_data).decode('utf-8')
            
            # 获取 MIME 类型
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = 'image/jpeg'  # 默认类型
            
            return f"data:{mime_type};base64,{encoded_string}"
            
        except Exception as e:
            if LOGGER_AVAILABLE:
                logger.error(f"图像编码失败: {e}")
            return None
    
    def decode_base64_to_image(self, base64_string: str) -> Optional[Image.Image]:
        """将 base64 字符串解码为 PIL 图像对象"""
        try:
            # 移除 data URL 前缀
            if ',' in base64_string:
                base64_data = base64_string.split(',')[1]
            else:
                base64_data = base64_string
            
            # 解码 base64
            image_data = base64.b64decode(base64_data)
            
            # 创建图像对象
            image = Image.open(io.BytesIO(image_data))
            return image
            
        except Exception as e:
            if LOGGER_AVAILABLE:
                logger.error(f"Base64 解码失败: {e}")
            return None
    
    def resize_image(self, image: Image.Image, max_width: int = 1024, max_height: int = 1024) -> Image.Image:
        """调整图像大小"""
        try:
            # 计算新的尺寸
            width, height = image.size
            ratio = min(max_width / width, max_height / height)
            
            if ratio < 1:
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                return resized_image
            else:
                return image
                
        except Exception as e:
            if LOGGER_AVAILABLE:
                logger.error(f"图像调整大小失败: {e}")
            return image
    
    def compress_image(self, image: Image.Image, quality: int = 85) -> Optional[bytes]:
        """压缩图像"""
        try:
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=quality)
            return buffer.getvalue()
            
        except Exception as e:
            if LOGGER_AVAILABLE:
                logger.error(f"图像压缩失败: {e}")
            return None
    
    def get_image_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """获取图像信息"""
        try:
            with Image.open(file_path) as img:
                info = {
                    'filename': os.path.basename(file_path),
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height,
                    'file_size': self.get_file_size(file_path),
                    'has_transparency': img.mode in ('RGBA', 'LA') or 'transparency' in img.info
                }
                return info
                
        except Exception as e:
            if LOGGER_AVAILABLE:
                logger.error(f"获取图像信息失败: {e}")
            return None
    
    def process_image_for_api(self, file_path: str, max_size: int = 1024, quality: int = 85) -> Optional[Dict[str, Any]]:
        """处理图像以供 API 使用"""
        try:
            if LOGGER_AVAILABLE:
                logger.info(f"开始处理图像: {file_path}")
            
            # 验证文件
            is_valid, message = self.validate_image_file(file_path)
            if not is_valid:
                if LOGGER_AVAILABLE:
                    logger.error(f"图像验证失败: {message}")
                return None
            
            # 获取原始图像信息
            original_info = self.get_image_info(file_path)
            if not original_info:
                return None
            
            # 打开图像
            with Image.open(file_path) as img:
                # 调整大小
                resized_img = self.resize_image(img, max_size, max_size)
                
                # 压缩图像
                compressed_data = self.compress_image(resized_img, quality)
                if not compressed_data:
                    return None
                
                # 编码为 base64
                encoded_string = base64.b64encode(compressed_data).decode('utf-8')
                
                result = {
                    'base64': f"data:image/jpeg;base64,{encoded_string}",
                    'original_info': original_info,
                    'processed_size': resized_img.size,
                    'compressed_size': len(compressed_data),
                    'compression_ratio': len(compressed_data) / original_info['file_size'] if original_info['file_size'] > 0 else 0
                }
                
                if LOGGER_AVAILABLE:
                    logger.info(f"图像处理成功: {file_path}")
                    logger.info(f"原始尺寸: {original_info['size']}, 处理后尺寸: {resized_img.size}")
                    logger.info(f"压缩率: {result['compression_ratio']:.2%}")
                
                return result
                
        except Exception as e:
            if LOGGER_AVAILABLE:
                logger.error(f"图像处理失败: {e}")
            return None
    
    def create_thumbnail(self, file_path: str, size: Tuple[int, int] = (200, 200)) -> Optional[str]:
        """创建缩略图并返回 base64 编码"""
        try:
            with Image.open(file_path) as img:
                # 创建缩略图
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # 转换为 RGB 模式（如果需要）
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # 保存到缓冲区
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=80)
                
                # 编码为 base64
                encoded_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
                return f"data:image/jpeg;base64,{encoded_string}"
                
        except Exception as e:
            if LOGGER_AVAILABLE:
                logger.error(f"创建缩略图失败: {e}")
            return None

    @staticmethod
    def validate_image_file_static(file_path: str) -> bool:
        """验证图像文件（静态方法）"""
        processor = ImageProcessor()
        is_valid, _ = processor.validate_image_file(file_path)
        return is_valid
    
    @staticmethod
    def get_image_info_static(file_path: str) -> Optional[Dict[str, Any]]:
        """获取图像信息（静态方法）"""
        processor = ImageProcessor()
        return processor.get_image_info(file_path)
    
    @staticmethod
    def create_image_data_url_static(file_path: str) -> Optional[str]:
        """创建图像 data URL（静态方法）"""
        processor = ImageProcessor()
        return processor.encode_image_to_base64(file_path)

# 创建全局图像处理器实例
image_processor = ImageProcessor()

if __name__ == "__main__":
    # 测试图像处理功能
    test_image = "test_image.jpg"
    
    if os.path.exists(test_image):
        print("测试图像处理功能...")
        
        # 测试验证
        is_valid, message = image_processor.validate_image_file(test_image)
        print(f"文件验证: {is_valid}, {message}")
        
        # 测试编码
        encoded = image_processor.encode_image_to_base64(test_image)
        print(f"Base64 编码: {'成功' if encoded else '失败'}")
        
        # 测试图像信息
        info = image_processor.get_image_info(test_image)
        if info:
            print(f"图像信息: {info}")
        
        # 测试处理
        processed = image_processor.process_image_for_api(test_image)
        if processed:
            print(f"处理成功: 压缩率 {processed['compression_ratio']:.2%}")
        
    else:
        print(f"测试图像不存在: {test_image}")