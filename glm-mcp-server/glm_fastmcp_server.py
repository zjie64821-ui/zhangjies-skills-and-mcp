#!/usr/bin/env python3
"""GLM MCP Server - 使用FastMCP"""
import os
import sys
import base64

if sys.platform == "win32":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# 加载环境变量（优先使用.env文件）
load_dotenv('.env')

# 创建FastMCP服务器实例
mcp = FastMCP(
    name="glm-mcp",
    instructions="使用GLM-4.6V模型分析图像文件"
)

@mcp.tool()
def analyze_image(
    image_path: str,
    prompt: str = "请详细描述这张图片的内容"
) -> str:
    """
    使用GLM-4.6V模型分析本地图像文件
    
    Args:
        image_path: 图像文件的绝对路径
        prompt: 分析图像的提示词
    
    Returns:
        GLM模型的分析结果
    """
    try:
        from zhipuai import ZhipuAI
        
        # 读取图像并转换为base64
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
            data_url = f"data:image/jpeg;base64,{image_data}"
        
        # 调用GLM API
        client = ZhipuAI(
            api_key=os.getenv('GLM_API_KEY'),
            base_url=os.getenv('GLM_API_BASE', 'https://open.bigmodel.cn/api/paas/v4/')
        )
        
        response = client.chat.completions.create(
            model=os.getenv('GLM_IMAGE_MODEL', 'glm-4.6v'),
            messages=[{
                'role': 'user',
                'content': [
                    {'type': 'image_url', 'image_url': {'url': data_url}},
                    {'type': 'text', 'text': prompt}
                ]
            }],
            temperature=0.3,
            max_tokens=8000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"图像分析失败: {str(e)}"

# 运行服务器
if __name__ == "__main__":
    mcp.run()
