"""
API基类
"""
from utils.http_client import HttpClient
from utils.logger import logger
from utils.assertions import Assertions


class BaseAPI:
    """API基类"""

    def __init__(self, base_url: str, timeout: int = 30):
        """
        初始化API
        :param base_url: 基础URL
        :param timeout: 超时时间
        """
        self.client = HttpClient(base_url, timeout)
        self.token = None
        self.assertions = Assertions()

    def set_token(self, token: str):
        """设置认证token"""
        self.token = token
        self.client.set_token(token)

    def get_token(self) -> str:
        """获取当前token"""
        return self.token

    def login(self, username: str, password: str) -> dict:
        """
        登录接口（子类需实现具体逻辑）
        :param username: 用户名
        :param password: 密码
        :return: 登录响应
        """
        raise NotImplementedError("子类需要实现login方法")

    def logout(self):
        """登出"""
        self.token = None
        self.client.token = None
