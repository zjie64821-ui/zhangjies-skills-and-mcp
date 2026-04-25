#!/usr/bin/env python3
"""
日志记录模块
提供统一的日志记录功能，支持文件和控制台输出
"""

import sys
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

class GLMLogger:
    """GLM MCP 服务器日志记录器"""
    
    def __init__(self, log_file: str = "mcpserver.log"):
        self.log_file = log_file
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger("glm_mcp_server")
        logger.setLevel(logging.DEBUG)

        # 避免重复添加处理器
        if logger.handlers:
            return logger

        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # 文件处理器
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 检查是否禁用控制台日志（MCP模式）
        # 当环境变量MCP_DISABLE_CONSOLE_LOG设置时，不添加控制台处理器
        if not os.environ.get('MCP_DISABLE_CONSOLE_LOG'):
            # 控制台处理器（仅在非MCP模式下）
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger
    
    def info(self, message: str, **kwargs):
        """记录信息级别日志"""
        self._log_with_context(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """记录警告级别日志"""
        self._log_with_context(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """记录错误级别日志"""
        self._log_with_context(logging.ERROR, message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """记录调试级别日志"""
        self._log_with_context(logging.DEBUG, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """记录严重错误级别日志"""
        self._log_with_context(logging.CRITICAL, message, **kwargs)
    
    def log_exception(self, exception: Exception, context: Dict[str, Any] = None):
        """记录异常信息"""
        error_msg = f"异常发生: {str(exception)}"
        if context:
            error_msg += f" | 上下文: {context}"
        
        self.error(error_msg)
        self.debug(f"异常详情: {exception.__class__.__name__}: {str(exception)}")
        
        # 记录完整的堆栈跟踪
        import traceback
        self.debug(f"堆栈跟踪:\n{traceback.format_exc()}")
    
    def _log_with_context(self, level: int, message: str, **kwargs):
        """带上下文的日志记录"""
        context_str = ""
        if kwargs:
            context_items = []
            for key, value in kwargs.items():
                if isinstance(value, dict):
                    context_items.append(f"{key}={value}")
                else:
                    context_items.append(f"{key}={value}")
            context_str = f" | {', '.join(context_items)}"
        
        full_message = f"{message}{context_str}"
        self.logger.log(level, full_message)
    
    def log_api_call(self, method: str, url: str, status_code: Optional[int] = None, 
                    response_time: Optional[float] = None, error: Optional[str] = None):
        """记录API调用日志"""
        log_message = f"API调用: {method} {url}"
        
        if status_code:
            log_message += f" | 状态码: {status_code}"
        if response_time:
            log_message += f" | 响应时间: {response_time:.2f}s"
        if error:
            log_message += f" | 错误: {error}"
        
        if status_code and status_code >= 400:
            self.error(log_message)
        else:
            self.info(log_message)
    
    def log_image_processing(self, image_path: str, operation: str, 
                           processing_time: Optional[float] = None, error: Optional[str] = None):
        """记录图像处理日志"""
        log_message = f"图像处理: {operation} | 文件: {image_path}"
        
        if processing_time:
            log_message += f" | 处理时间: {processing_time:.2f}s"
        if error:
            log_message += f" | 错误: {error}"
        
        if error:
            self.error(log_message)
        else:
            self.info(log_message)
    
    def log_tool_call(self, tool_name: str, params: dict, result: Optional[str] = None, error: Optional[str] = None):
        """记录工具调用日志"""
        log_message = f"工具调用: {tool_name}"
        
        if error:
            log_message += f" | 错误: {error}"
            self.error(log_message)
        else:
            if result:
                log_message += f" | 结果长度: {len(result)}"
            self.info(log_message)
    
    def log_config_change(self, key: str, old_value: Any, new_value: Any):
        """记录配置变更日志"""
        self.info(f"配置变更: {key} | 旧值: {old_value} | 新值: {new_value}")
    
    def log_file_operation(self, operation: str, file_path: str, success: bool, error: Optional[str] = None):
        """记录文件操作日志"""
        status = "成功" if success else "失败"
        log_message = f"文件操作: {operation} | 文件: {file_path} | 状态: {status}"
        
        if error:
            log_message += f" | 错误: {error}"
        
        if success:
            self.info(log_message)
        else:
            self.warning(log_message)
    
    def clear_log_file(self):
        """清空日志文件"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("")
            self.info("日志文件已清空")
        except Exception as e:
            self.error(f"清空日志文件失败: {e}")

# 创建全局日志记录器实例
logger = GLMLogger()

# 提供便捷的日志记录函数
def log_info(message: str, **kwargs):
    logger.info(message, **kwargs)

def log_warning(message: str, **kwargs):
    logger.warning(message, **kwargs)

def log_error(message: str, **kwargs):
    logger.error(message, **kwargs)

def log_debug(message: str, **kwargs):
    logger.debug(message, **kwargs)

def log_exception(exception: Exception, context: Dict[str, Any] = None):
    logger.log_exception(exception, context)

if __name__ == "__main__":
    # 测试日志记录功能
    logger.info("日志记录器测试")
    logger.warning("这是一个警告消息")
    logger.error("这是一个错误消息")
    logger.debug("这是一个调试消息")
    
    # 测试异常记录
    try:
        raise ValueError("测试异常")
    except Exception as e:
        logger.log_exception(e, {"context": "测试"})
    
    print("日志记录测试完成，请查看 mcpserver.log 文件")