import sys
import json
from typing import Dict, Any, Optional, List
import asyncio

# 尝试导入依赖模块
try:
    from mcp.server import Server
    from mcp import types
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    # 在MCP模式下不使用print，避免干扰stdio通信

try:
    from zhipuai import ZhipuAI
    ZHIPUAI_AVAILABLE = True
except ImportError:
    ZHIPUAI_AVAILABLE = False
    # 在MCP模式下不使用print，避免干扰stdio通信

from config import config
from logger import logger
from image_processor import ImageProcessor
from utils import (
    create_success_response,
    create_error_response,
    create_validation_error_response,
    is_valid_temperature,
    validate_required_params
)

class GLMMcpServer:
    """智谱 GLM MCP 服务器"""
    
    def __init__(self):
        # 检查依赖是否可用
        if not MCP_AVAILABLE:
            # 在MCP模式下不使用print，避免干扰stdio通信
            raise ImportError("MCP module is required")
        
        self.server = Server("glm-mcp")
        self.client: Optional[ZhipuAI] = None
        self._setup_client()
        self._register_tools()
    
    def _setup_client(self):
        """设置智谱 AI 客户端"""
        if not config.validate_config():
            logger.error("配置验证失败，请检查 GLM_API_KEY 等配置")
            logger.error("验证错误详情:", **{"errors": config.get_validation_errors()})
            return
        
        try:
            logger.info("正在初始化智谱 AI 客户端...")
            logger.debug("客户端配置", **{
                "api_base": config.glm_api_base,
                "model": config.glm_image_model
            })
            
            if not ZHIPUAI_AVAILABLE:
                logger.warning("智谱 AI SDK 未安装，无法初始化客户端")
                self.client = None
                return
            
            self.client = ZhipuAI(
                api_key=config.glm_api_key,
                base_url=config.glm_api_base
            )
            
            # 测试客户端连接
            logger.info("智谱 AI 客户端初始化成功")
            logger.debug("客户端已准备就绪")
            
        except Exception as e:
            logger.log_exception(e, {"context": "Initializing Zhipu AI client"})
            logger.error(f"智谱 AI 客户端初始化失败: {e}")
            self.client = None
    
    def _register_tools(self):
        """注册所有工具"""
        self._register_read_image_tool()
    
    def _register_read_image_tool(self):
        """注册图像分析工具"""
        
        # 注册工具列表处理器
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """处理工具列表请求"""
            return [
                types.Tool(
                    name="read_image",
                    description="使用 GLM-4.6V 模型分析本地图像",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "image_path": {
                                "type": "string",
                                "description": "图像文件路径"
                            },
                            "prompt": {
                                "type": "string",
                                "description": "分析提示文本"
                            },
                            "temperature": {
                                "type": "number",
                                "description": "温度参数 (0.0-2.0)",
                                "default": 0.8
                            },
                            "max_tokens": {
                                "type": "integer",
                                "description": "最大输出令牌数",
                                "default": 1000
                            }
                        },
                        "required": ["image_path", "prompt"]
                    }
                )
            ]
        
        # 注册工具调用处理器
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            """处理工具调用请求"""
            if name == "read_image":
                return await self._analyze_image(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
        
        # 确保处理器被正确注册
        logger.info("图像分析工具已注册")
    
    async def _test_list_tools(self) -> List[types.Tool]:
        """测试方法：直接返回工具列表"""
        return [
            types.Tool(
                name="read_image",
                description="使用 GLM-4.6V 模型分析本地图像",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "image_path": {
                            "type": "string",
                            "description": "图像文件路径"
                        },
                        "prompt": {
                            "type": "string",
                            "description": "分析提示文本"
                        },
                        "temperature": {
                            "type": "number",
                            "description": "温度参数 (0.0-2.0)",
                            "default": 0.8
                        },
                        "max_tokens": {
                            "type": "integer",
                            "description": "最大输出令牌数",
                            "default": 1000
                        }
                    },
                    "required": ["image_path", "prompt"]
                }
            )
        ]
    
    async def _analyze_image(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """分析图像"""
        image_path = arguments.get("image_path")
        prompt = arguments.get("prompt")
        temperature = arguments.get("temperature", 0.8)
        max_tokens = arguments.get("max_tokens", 1000)
        
        params = {
            "image_path": image_path,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # 参数验证
        validation_error = validate_required_params(params, ["image_path", "prompt"])
        if validation_error:
            logger.log_tool_call("read_image", params, error=validation_error)
            return [types.TextContent(type="text", text=json.dumps(create_validation_error_response("parameters", validation_error), ensure_ascii=False))]
        
        if not is_valid_temperature(temperature):
            error_msg = f"温度参数必须在 0.0-2.0 之间，当前值: {temperature}"
            logger.log_tool_call("read_image", params, error=error_msg)
            return [types.TextContent(type="text", text=json.dumps(create_validation_error_response("temperature", error_msg), ensure_ascii=False))]
        
        if not ImageProcessor.validate_image_file_static(image_path):
            error_msg = f"图像文件不存在或格式不支持: {image_path}"
            logger.log_tool_call("read_image", params, error=error_msg)
            return [types.TextContent(type="text", text=json.dumps(create_error_response(error_msg), ensure_ascii=False))]
        
        if not self.client:
            error_msg = "智谱 AI 客户端未初始化"
            logger.log_tool_call("read_image", params, error=error_msg)
            return [types.TextContent(type="text", text=json.dumps(create_error_response(error_msg), ensure_ascii=False))]
        
        try:
            # 获取图像信息
            image_info = ImageProcessor.get_image_info_static(image_path)
            logger.info(f"开始分析图像: {image_info}")
            logger.debug("图像分析参数", **{
                "image_path": image_path,
                "image_info": image_info,
                "temperature": temperature,
                "max_tokens": max_tokens
            })
            
            # 创建图像 data URL
            image_data_url = ImageProcessor.create_image_data_url_static(image_path)
            if not image_data_url:
                error_msg = "图像编码失败"
                logger.log_tool_call("read_image", params, error=error_msg)
                return [types.TextContent(type="text", text=json.dumps(create_error_response(error_msg), ensure_ascii=False))]
            
            logger.debug("图像编码成功", **{"data_url_length": len(image_data_url)})
            
            # 调用智谱 GLM 模型
            logger.info("正在调用智谱 GLM API...")
            api_params = {
                "model": config.glm_image_model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "prompt_length": len(prompt)
            }
            
            response = self.client.chat.completions.create(
                model=config.glm_image_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": image_data_url}},
                            {"type": "text", "text": prompt}
                        ]
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )
            
            logger.log_api_call(
                method="POST",
                url=config.glm_api_base,
                status_code=200
            )
            
            result = response.choices[0].message.content
            logger.info("图像分析成功完成")
            logger.debug("分析结果", **{"result_length": len(result)})
            logger.log_tool_call("read_image", params, result=result)
            
            return [types.TextContent(type="text", text=json.dumps(create_success_response(result), ensure_ascii=False))]
            
        except Exception as e:
            logger.log_exception(e, {
                "context": "Image analysis",
                "image_path": image_path,
                "prompt": prompt
            })
            error_msg = f"图像分析失败: {str(e)}"
            logger.log_tool_call("read_image", params, error=error_msg)
            return [types.TextContent(type="text", text=json.dumps(create_error_response(error_msg), ensure_ascii=False))]
    
    async def run_async(self):
        """异步运行 MCP 服务器"""
        try:
            logger.info("启动 GLM MCP 服务器")
            logger.info("服务器信息", **{
                "version": "1.0.0",
                "name": "glm-mcp",
                "python_version": sys.version,
                "platform": sys.platform
            })

            from mcp.server.stdio import stdio_server
            logger.info("服务器正在运行，等待工具调用...")

            async with stdio_server() as (read_stream, write_stream):
                # 创建启用工具功能的初始化选项
                init_options = self.server.create_initialization_options()
                init_options.capabilities.tools = {"listChanged": True}

                await self.server.run(
                    read_stream,
                    write_stream,
                    init_options
                )

        except KeyboardInterrupt:
            logger.info("服务器被用户中断")
        except Exception as e:
            logger.log_exception(e, {"context": "Server runtime"})
            logger.error(f"服务器运行失败: {e}")
            raise
    
    def run(self):
        """运行 MCP 服务器"""
        try:
            asyncio.run(self.run_async())
        except KeyboardInterrupt:
            logger.info("服务器被用户中断")
            sys.exit(0)
        except Exception as e:
            logger.log_exception(e, {"context": "Server runtime"})
            logger.error(f"服务器运行失败: {e}")
            sys.exit(1)