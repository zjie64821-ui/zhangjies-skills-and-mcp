#!/usr/bin/env python3
"""
GLM MCP 服务器主程序
用于在 Claude Code 中集成智谱 AI GLM-4.6V 的图像分析功能
"""

import sys
import os
import platform

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from logger import logger

# 尝试导入完整版本的服务器
try:
    from server import GLMMcpServer
    FULL_SERVER_AVAILABLE = True
except ImportError as e:
    FULL_SERVER_AVAILABLE = False
    logger.error(f"完整版服务器不可用: {e}")
    logger.error("请确保安装了所需依赖: pip install -r requirements.txt")
    logger.error("缺少的包可能包括: mcp, zai-sdk")

def print_system_info():
    """打印系统信息（用于调试）"""
    logger.info("=== 系统信息 ===")
    logger.info(f"操作系统: {platform.system()} {platform.release()}")
    logger.info(f"Python 版本: {platform.python_version()}")
    logger.info(f"架构: {platform.machine()}")
    logger.info(f"当前工作目录: {os.getcwd()}")
    logger.info(f"脚本目录: {os.path.dirname(os.path.abspath(__file__))}")
    logger.info("================")

def print_configuration_status():
    """打印配置状态"""
    logger.info("=== 配置状态 ===")
    config_summary = config.get_config_summary()
    for key, value in config_summary.items():
        logger.info(f"{key}: {value}")
    
    if config.validate_config():
        logger.info("✓ 配置验证通过")
    else:
        logger.error("✗ 配置验证失败")
        for error in config.get_validation_errors():
            logger.error(f"  - {error}")
    logger.info("================")

def print_usage_instructions():
    """打印使用说明"""
    logger.info("=== 使用说明 ===")
    logger.info("1. 确保已安装所需依赖: pip install -r requirements.txt")
    logger.info("2. 配置 API 密钥: 在 .env 文件中设置 GLM_API_KEY")
    logger.info("3. 运行服务器: python main.py")
    logger.info("4. 在 Claude Code 中使用 @图像 调用图像分析功能")
    logger.info("5. 查看 mcpserver.log 文件获取详细日志")
    logger.info("================")

def main():
    """主程序入口"""
    try:
        logger.info("=== GLM MCP 服务器启动 ===")
        print_system_info()
        print_configuration_status()
        print_usage_instructions()
        
        # 检查配置
        if not config.validate_config():
            logger.error("配置验证失败，请检查环境变量或 .env 文件中的 GLM_API_KEY")
            logger.error("需要的配置项：")
            logger.error("  - GLM_API_KEY: 智谱 AI API 密钥")
            logger.error("  - GLM_API_BASE: API 基础 URL (可选，默认: https://open.bigmodel.cn/api/paas/v4/chat/completions)")
            logger.error("  - GLM_IMAGE_MODEL: 图像模型 (可选，默认: glm-4.6v)")
            logger.error("详细错误信息:", **{"errors": config.get_validation_errors()})
            logger.error("请修复配置错误后重新运行程序")
            input("按回车键退出...")  # Windows 用户友好的退出方式
            sys.exit(1)
        
        # 创建并运行服务器
        if FULL_SERVER_AVAILABLE:
            logger.info("正在创建完整 MCP 服务器...")
            server = GLMMcpServer()
            
            logger.info("启动服务器，按 Ctrl+C 停止...")
            server.run()
        else:
            logger.error("完整版服务器不可用，无法启动")
            logger.error("请安装所需依赖: pip install -r requirements.txt")
            logger.error("然后重新运行程序")
            input("按回车键退出...")
            sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
        sys.exit(0)
    except Exception as e:
        logger.log_exception(e, {"context": "Main program execution"})
        logger.error(f"程序运行失败: {e}")
        logger.error("如果问题持续存在，请检查：")
        logger.error("1. 网络连接是否正常")
        logger.error("2. API 密钥是否正确")
        logger.error("3. 依赖包是否完整安装")
        logger.error("4. 查看 mcpserver.log 获取详细错误信息")
        input("按回车键退出...")  # Windows 用户友好的退出方式
        sys.exit(1)

if __name__ == "__main__":
    main()