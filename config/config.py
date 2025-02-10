import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class TestConfig:
    """测试框架配置类"""
    
    # ============================
    # 浏览器基础配置
    # ============================
    
    # 浏览器类型：chromium(谷歌内核), firefox(火狐), webkit(Safari内核)
    browser_type: str = "webkit"
    
    # 是否使用无头模式（不显示浏览器界面）
    headless: bool = False
    
    # 操作延迟时间(毫秒)，用于减缓自动化操作速度，方便调试
    slow_mo: int = 0
    
    # 浏览器视窗大小
    viewport_width: int = 1920
    viewport_height: int = 1080
    
    # ============================
    # 超时配置（毫秒）
    # ============================
    
    # 元素等待超时时间
    timeout: int = 10000
    
    # 页面加载超时时间
    navigation_timeout: int = 30000
    
    # ============================
    # 测试报告配置
    # ============================
    
    # 测试失败时是否自动截图
    screenshot_on_failure: bool = True
    
    # 测试失败时是否保存录像
    video_on_failure: bool = False
    
    # 截图保存目录
    screenshot_dir: str = "reports/screenshots"
    
    # 视频保存目录
    video_dir: str = "reports/videos"
    
    # ============================
    # 重试机制配置
    # ============================
    
    # 失败重试次数
    retry_count: int = 3
    
    # 重试间隔时间（秒）
    retry_delay: float = 1.0
    
    # ============================
    # 测试环境URL配置
    # ============================
    
    # 各环境基础URL配置
    base_urls: Dict[str, str] = None
    
    def __post_init__(self):
        """
        初始化配置后的处理：
        1. 设置各环境URL
        2. 创建必要的目录结构
        """
        # 配置各环境URL
        self.base_urls = {
            # 测试环境
            "test": {
                "baidu": "https://www.baidu.com",
                "google": "https://www.google.com",
            },
            # 预发布环境
            "staging": {
                "baidu": "https://test.baidu.com",
                "google": "https://test.google.com",
            },
            # 生产环境
            "prod": {
                "baidu": "https://www.baidu.com",
                "google": "https://www.google.com",
            }
        }
        
        # 创建必要的目录
        os.makedirs(self.screenshot_dir, exist_ok=True)
        os.makedirs(self.video_dir, exist_ok=True)
    
    def get_browser_launch_options(self) -> Dict[str, Any]:
        """
        获取浏览器启动选项
        :return: 浏览器启动配置字典
        """
        return {
            "headless": self.headless,
            "slow_mo": self.slow_mo,
            "args": [
                "--start-maximized",  # 最大化启动
                "--disable-infobars",  # 禁用浏览器正在被自动化程序控制的提示
                "--no-sandbox",  # 禁用沙箱模式
                "--disable-setuid-sandbox",  # 禁用setuid沙箱
                "--disable-dev-shm-usage",  # 禁用/dev/shm使用
            ]
        }
    
    def get_context_options(self) -> Dict[str, Any]:
        """
        获取浏览器上下文选项
        :return: 上下文配置字典
        """
        return {
            "viewport": {
                "width": self.viewport_width,
                "height": self.viewport_height,
            },
            "record_video_dir": self.video_dir if self.video_on_failure else None,
            "accept_downloads": True,  # 允许下载
            "ignore_https_errors": True,  # 忽略HTTPS错误
            "java_script_enabled": True,  # 启用JavaScript
        }
    
    def get_url(self, env: str, key: str) -> str:
        """
        获取指定环境的URL
        :param env: 环境名称 (test/staging/prod)
        :param key: URL键名
        :return: 对应的URL
        """
        return self.base_urls.get(env, {}).get(key, "") 