"""
配置模块
统一管理环境配置、用户配置、业务配置
"""
import os
import yaml
from pathlib import Path


class ConfigManager:
    """配置管理器"""

    def __init__(self):
        self.config_dir = Path(__file__).parent
        self._env_config = None
        self._user_config = None
        self._business_config = None
        self._current_env = None

    def load_yaml(self, file_name):
        """加载YAML配置文件"""
        file_path = self.config_dir / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    @property
    def env_config(self):
        """获取环境配置"""
        if self._env_config is None:
            self._env_config = self.load_yaml('env_config.yaml')
        return self._env_config

    @property
    def user_config(self):
        """获取用户配置"""
        if self._user_config is None:
            self._user_config = self.load_yaml('user_config.yaml')
        return self._user_config

    @property
    def business_config(self):
        """获取业务配置"""
        if self._business_config is None:
            self._business_config = self.load_yaml('business_config.yaml')
        return self._business_config

    def get_current_env(self):
        """获取当前环境"""
        if self._current_env is None:
            # 优先从环境变量读取
            env = os.getenv('TEST_ENV')
            if not env:
                env = self.env_config.get('current_env', 'test')
            self._current_env = env
        return self._current_env

    def get_env_config(self, platform):
        """
        获取指定平台的环境配置
        :param platform: bos/admin/staff
        :return: 平台配置字典
        """
        current_env = self.get_current_env()
        env_data = self.env_config['environments'].get(current_env, {})
        return env_data.get(platform, {})

    def get_base_url(self, platform):
        """获取指定平台的基础URL"""
        config = self.get_env_config(platform)
        return config.get('base_url', '')

    def get_user(self, platform, user_type):
        """
        获取用户信息
        :param platform: bos_users/admin_users/staff_users
        :param user_type: admin_user/normal_user等
        :return: 用户信息字典
        """
        users = self.user_config.get(platform, {})
        return users.get(user_type, {})

    def get_stock_type_config(self, stock_type):
        """
        获取股票类型配置
        :param stock_type: hk_us/unlisted/a_stock
        :return: 股票类型配置字典
        """
        stock_types = self.business_config.get('stock_types', {})
        return stock_types.get(stock_type, {})


# 全局配置实例
config = ConfigManager()
