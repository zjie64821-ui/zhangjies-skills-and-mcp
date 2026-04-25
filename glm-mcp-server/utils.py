#!/usr/bin/env python3
"""
工具函数模块
提供各种实用工具函数
"""

import os
import sys
import json
import time
import hashlib
import platform
import subprocess
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

try:
    from logger import logger
    LOGGER_AVAILABLE = True
except ImportError:
    import logging
    logger = logging.getLogger(__name__)
    LOGGER_AVAILABLE = False

class SystemUtils:
    """系统工具类"""
    
    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """获取系统信息"""
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'hostname': platform.node(),
            'working_directory': os.getcwd(),
            'script_directory': os.path.dirname(os.path.abspath(__file__))
        }
    
    @staticmethod
    def check_dependencies() -> Dict[str, bool]:
        """检查依赖包"""
        dependencies = {
            'requests': False,
            'PIL': False,
            'dotenv': False,
            'mcp': False,
            'zhipuai': False
        }
        
        try:
            import requests
            dependencies['requests'] = True
        except ImportError:
            pass
        
        try:
            from PIL import Image
            dependencies['PIL'] = True
        except ImportError:
            pass
        
        try:
            from dotenv import load_dotenv
            dependencies['dotenv'] = True
        except ImportError:
            pass
        
        try:
            import mcp
            dependencies['mcp'] = True
        except ImportError:
            pass
        
        try:
            import zhipuai
            dependencies['zhipuai'] = True
        except ImportError:
            pass
        
        return dependencies
    
    @staticmethod
    def is_windows() -> bool:
        """检查是否为 Windows 系统"""
        return platform.system().lower() == 'windows'
    
    @staticmethod
    def is_admin() -> bool:
        """检查是否具有管理员权限"""
        try:
            if SystemUtils.is_windows():
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.getuid() == 0
        except:
            return False

class FileUtils:
    """文件工具类"""
    
    @staticmethod
    def ensure_directory(directory: str) -> bool:
        """确保目录存在"""
        try:
            os.makedirs(directory, exist_ok=True)
            if LOGGER_AVAILABLE:
                logger.info(f"目录已确保存在: {directory}")
            return True
        except Exception as e:
            if LOGGER_AVAILABLE:
                logger.error(f"创建目录失败: {e}")
            return False
    
    @staticmethod
    def get_file_hash(file_path: str, algorithm: str = 'md5') -> Optional[str]:
        """获取文件哈希值"""
        try:
            hash_obj = hashlib.new(algorithm)
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except Exception as e:
            if LOGGER_AVAILABLE:
                logger.error(f"计算文件哈希失败: {e}")
            return None
    
    @staticmethod
    def get_file_size_formatted(file_path: str) -> str:
        """获取格式化的文件大小"""
        try:
            size = os.path.getsize(file_path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.2f} {unit}"
                size /= 1024.0
            return f"{size:.2f} TB"
        except Exception as e:
            if LOGGER_AVAILABLE:
                logger.error(f"获取文件大小失败: {e}")
            return "Unknown"
    
    @staticmethod
    def clean_filename(filename: str) -> str:
        """清理文件名，移除非法字符"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename.strip()
    
    @staticmethod
    def get_unique_filename(file_path: str) -> str:
        """获取唯一的文件名"""
        if not os.path.exists(file_path):
            return file_path
        
        base, ext = os.path.splitext(file_path)
        counter = 1
        while os.path.exists(f"{base}_{counter}{ext}"):
            counter += 1
        return f"{base}_{counter}{ext}"

class NetworkUtils:
    """网络工具类"""
    
    @staticmethod
    def check_internet_connection(timeout: int = 5) -> bool:
        """检查网络连接"""
        try:
            import requests
            response = requests.get('https://www.baidu.com', timeout=timeout)
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def get_local_ip() -> str:
        """获取本地IP地址"""
        try:
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return local_ip
        except:
            return "127.0.0.1"
    
    @staticmethod
    def is_port_open(port: int, host: str = '127.0.0.1') -> bool:
        """检查端口是否开放"""
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((host, port))
                return result == 0
        except:
            return False

class JsonUtils:
    """JSON工具类"""
    
    @staticmethod
    def safe_loads(json_str: str, default: Any = None) -> Any:
        """安全地加载JSON字符串"""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            if LOGGER_AVAILABLE:
                logger.error(f"JSON解析失败: {e}")
            return default
    
    @staticmethod
    def safe_dumps(obj: Any, indent: int = 2) -> str:
        """安全地序列化对象为JSON字符串"""
        try:
            return json.dumps(obj, ensure_ascii=False, indent=indent)
        except Exception as e:
            if LOGGER_AVAILABLE:
                logger.error(f"JSON序列化失败: {e}")
            return "{}"

class TimeUtils:
    """时间工具类"""
    
    @staticmethod
    def get_timestamp() -> int:
        """获取当前时间戳"""
        return int(time.time())
    
    @staticmethod
    def get_formatted_time(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """获取格式化的时间字符串"""
        return datetime.now().strftime(format_str)
    
    @staticmethod
    def parse_time(time_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
        """解析时间字符串"""
        try:
            return datetime.strptime(time_str, format_str)
        except ValueError as e:
            if LOGGER_AVAILABLE:
                logger.error(f"时间解析失败: {e}")
            return None

class ProcessUtils:
    """进程工具类"""
    
    @staticmethod
    def run_command(command: Union[str, List[str]], timeout: int = 30) -> Dict[str, Any]:
        """运行命令并返回结果"""
        try:
            if isinstance(command, str):
                command = command.split()
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'success': result.returncode == 0,
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': command
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'return_code': -1,
                'stdout': '',
                'stderr': f'Command timeout after {timeout} seconds',
                'command': command
            }
        except Exception as e:
            return {
                'success': False,
                'return_code': -1,
                'stdout': '',
                'stderr': str(e),
                'command': command
            }
    
    @staticmethod
    def kill_process(pid: int) -> bool:
        """终止进程"""
        try:
            if SystemUtils.is_windows():
                subprocess.run(['taskkill', '/F', '/PID', str(pid)], check=True)
            else:
                subprocess.run(['kill', '-9', str(pid)], check=True)
            return True
        except:
            return False

class ValidationUtils:
    """验证工具类"""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """验证URL格式"""
        try:
            from urllib.parse import urlparse
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """验证邮箱格式"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_api_key(api_key: str) -> bool:
        """验证API密钥格式"""
        if not api_key or len(api_key) < 10:
            return False
        
        # 检查是否包含常见的API密钥格式
        api_key = api_key.strip()
        return (
            api_key.startswith('sk-') or  # OpenAI格式
            len(api_key) >= 20 or         # 一般长度要求
            any(c.isalnum() for c in api_key)  # 包含字母数字
        )

# 创建全局工具实例
system_utils = SystemUtils()
file_utils = FileUtils()
network_utils = NetworkUtils()
json_utils = JsonUtils()
time_utils = TimeUtils()
process_utils = ProcessUtils()
validation_utils = ValidationUtils()

# 便捷函数
def get_system_info() -> Dict[str, str]:
    return system_utils.get_system_info()

def check_dependencies() -> Dict[str, bool]:
    return system_utils.check_dependencies()

def is_windows() -> bool:
    return system_utils.is_windows()

def ensure_directory(directory: str) -> bool:
    return file_utils.ensure_directory(directory)

def get_file_hash(file_path: str, algorithm: str = 'md5') -> Optional[str]:
    return file_utils.get_file_hash(file_path, algorithm)

def get_file_size_formatted(file_path: str) -> str:
    return file_utils.get_file_size_formatted(file_path)

def safe_loads(json_str: str, default: Any = None) -> Any:
    return json_utils.safe_loads(json_str, default)

def safe_dumps(obj: Any, indent: int = 2) -> str:
    return json_utils.safe_dumps(obj, indent)

def get_timestamp() -> int:
    return time_utils.get_timestamp()

def get_formatted_time(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    return time_utils.get_formatted_time(format_str)

def is_valid_url(url: str) -> bool:
    return validation_utils.is_valid_url(url)

def is_valid_email(email: str) -> bool:
    return validation_utils.is_valid_email(email)

def is_valid_api_key(api_key: str) -> bool:
    return validation_utils.is_valid_api_key(api_key)

# MCP 响应函数
def create_success_response(data: Any) -> Dict[str, Any]:
    """创建成功响应"""
    return {
        "success": True,
        "data": data,
        "timestamp": get_timestamp()
    }

def create_error_response(message: str, error_code: str = "UNKNOWN_ERROR") -> Dict[str, Any]:
    """创建错误响应"""
    return {
        "success": False,
        "error": message,
        "error_code": error_code,
        "timestamp": get_timestamp()
    }

def create_validation_error_response(message: str) -> Dict[str, Any]:
    """创建验证错误响应"""
    return {
        "success": False,
        "error": message,
        "error_code": "VALIDATION_ERROR",
        "timestamp": get_timestamp()
    }

def is_valid_temperature(temperature: float) -> bool:
    """验证温度参数是否有效"""
    return isinstance(temperature, (int, float)) and 0.0 <= temperature <= 2.0

def validate_required_params(params: Dict[str, Any], required_keys: List[str]) -> Optional[str]:
    """验证必需参数是否存在"""
    missing_keys = [key for key in required_keys if key not in params or params[key] is None]
    if missing_keys:
        return f"缺少必需参数: {', '.join(missing_keys)}"
    return None

if __name__ == "__main__":
    # 测试工具函数
    print("=== 工具函数测试 ===")
    
    # 系统信息
    print("\n系统信息:")
    sys_info = get_system_info()
    for key, value in sys_info.items():
        print(f"  {key}: {value}")
    
    # 依赖检查
    print("\n依赖检查:")
    deps = check_dependencies()
    for dep, available in deps.items():
        print(f"  {dep}: {'✓' if available else '✗'}")
    
    # 时间信息
    print(f"\n当前时间: {get_formatted_time()}")
    print(f"时间戳: {get_timestamp()}")
    
    # 验证测试
    print(f"\nURL验证:")
    test_urls = ['https://www.baidu.com', 'invalid-url', 'ftp://test.com']
    for url in test_urls:
        print(f"  {url}: {'✓' if is_valid_url(url) else '✗'}")
    
    print(f"\n邮箱验证:")
    test_emails = ['test@example.com', 'invalid-email', 'user@domain.co.uk']
    for email in test_emails:
        print(f"  {email}: {'✓' if is_valid_email(email) else '✗'}")
    
    print("\n工具函数测试完成！")