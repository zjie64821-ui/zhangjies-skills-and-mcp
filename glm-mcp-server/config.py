import os
from typing import Optional, List, Dict, Any

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

try:
    from logger import logger
    LOGGER_AVAILABLE = True
except ImportError:
    LOGGER_AVAILABLE = False
    import logging
    logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        self._load_config()
        self._validation_errors = []
    
    def _load_config(self):
        """加载配置文件"""
        try:
            # 加载环境变量，按优先级：系统环境变量 > 执行目录 .env > 项目根目录 .env
            current_dir_env = os.path.join(os.getcwd(), '.env')
            project_root_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
            
            # 检查是否要求必须使用环境变量
            require_env_vars = os.getenv('REQUIRE_ENV_VARS', 'true').lower() == 'true'
            
            if require_env_vars:
                # 强制使用环境变量（推荐的安全模式）
                if LOGGER_AVAILABLE:
                    logger.info("Using environment variables only (REQUIRE_ENV_VARS=true)")
                    logger.info("GLM_API_KEY source: " + ("Environment variable" if os.getenv('GLM_API_KEY') else "Not set"))
            else:
                # 兼容模式：允许从 .env 文件读取
                if DOTENV_AVAILABLE:
                    # 先加载项目根目录的 .env
                    if os.path.exists(project_root_env):
                        if LOGGER_AVAILABLE:
                            logger.log_file_operation("load_config", project_root_env, True)
                        load_dotenv(project_root_env)
                    else:
                        if LOGGER_AVAILABLE:
                            logger.log_file_operation("load_config", project_root_env, False, "File not found")
                    
                    # 再加载执行目录的 .env（会覆盖项目根目录的同名变量）
                    if os.path.exists(current_dir_env):
                        if LOGGER_AVAILABLE:
                            logger.log_file_operation("load_config", current_dir_env, True)
                        load_dotenv(current_dir_env)
                    else:
                        if LOGGER_AVAILABLE:
                            logger.log_file_operation("load_config", current_dir_env, False, "File not found")
                else:
                    # 如果 dotenv 不可用，直接读取 .env 文件
                    self._load_env_manually(project_root_env)
                    self._load_env_manually(current_dir_env)
            
            # 记录配置来源信息
            if LOGGER_AVAILABLE:
                api_key_source = "Environment variable" if os.getenv('GLM_API_KEY') else "Not configured"
                logger.info(f"Configuration loaded successfully")
                logger.info(f"GLM_API_KEY source: {api_key_source}")
                logger.info(f"GLM_API_BASE: {self.glm_api_base}")
                logger.info(f"GLM_IMAGE_MODEL: {self.glm_image_model}")
            # 在MCP模式下不使用print，避免干扰stdio通信

        except Exception as e:
            if LOGGER_AVAILABLE:
                logger.log_exception(e, {"context": "Loading configuration"})
            # 在MCP模式下不使用print，避免干扰stdio通信
            self._validation_errors.append(f"配置加载失败: {str(e)}")
    
    def _load_env_manually(self, env_file: str):
        """手动加载 .env 文件"""
        if not os.path.exists(env_file):
            return
        
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        except Exception as e:
            if LOGGER_AVAILABLE:
                logger.warning(f"Failed to load {env_file} manually: {e}")
            # 在MCP模式下不使用print，避免干扰stdio通信
    
    @property
    def glm_api_key(self) -> Optional[str]:
        return os.getenv('GLM_API_KEY')
    
    @property
    def glm_api_base(self) -> str:
        return os.getenv('GLM_API_BASE', 'https://open.bigmodel.cn/api/paas/v4')
    
    @property
    def glm_image_model(self) -> str:
        return os.getenv('GLM_IMAGE_MODEL', 'glm-4.6v')
    
    @property
    def log_level(self) -> str:
        return os.getenv('LOG_LEVEL', 'INFO')
    
    def get_config_summary(self) -> Dict[str, Any]:
        """获取配置摘要（用于调试）"""
        return {
            "glm_api_base": self.glm_api_base,
            "glm_image_model": self.glm_image_model,
            "log_level": self.log_level,
            "api_key_set": bool(self.glm_api_key),
            "working_directory": os.getcwd(),
            "config_file_directory": os.path.dirname(os.path.abspath(__file__))
        }
    
    def validate_config(self) -> bool:
        """验证配置是否完整"""
        self._validation_errors = []
        
        # 检查必需的配置项
        if not self.glm_api_key:
            self._validation_errors.append("GLM_API_KEY 未设置")
            logger.error("GLM_API_KEY is not configured")
        
        # 检查 API URL 格式
        if not self.glm_api_base.startswith('http'):
            self._validation_errors.append("GLM_API_BASE 格式不正确")
            logger.error("GLM_API_BASE format is invalid")
        
        # 检查模型名称
        if not self.glm_image_model:
            self._validation_errors.append("GLM_IMAGE_MODEL 未设置")
            logger.error("GLM_IMAGE_MODEL is not configured")
        
        # 记录验证结果
        if self._validation_errors:
            logger.log_config_validation(self._validation_errors)
            return False
        
        logger.info("Configuration validation passed")
        logger.debug("Configuration summary", **self.get_config_summary())
        return True
    
    def get_validation_errors(self) -> List[str]:
        """获取验证错误列表"""
        return self._validation_errors

# 全局配置实例
config = Config()