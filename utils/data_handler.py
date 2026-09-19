"""
数据处理工具模块
"""
import json
import yaml
import random
import string
from datetime import datetime, timedelta
from typing import Any, Dict, List
from pathlib import Path
from faker import Faker


class DataHandler:
    """数据处理工具类"""

    def __init__(self):
        self.faker = Faker('zh_CN')

    @staticmethod
    def load_json(file_path: str) -> Dict:
        """加载JSON文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def load_yaml(file_path: str) -> Dict:
        """加载YAML文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    @staticmethod
    def save_json(data: Dict, file_path: str):
        """保存为JSON文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def save_yaml(data: Dict, file_path: str):
        """保存为YAML文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    @staticmethod
    def extract_json_value(json_data: Dict, json_path: str) -> Any:
        """
        从JSON中提取值（支持嵌套）
        :param json_data: JSON数据
        :param json_path: 路径，如 "data.user.name"
        :return: 提取的值
        """
        keys = json_path.split('.')
        value = json_data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            elif isinstance(value, list) and key.isdigit():
                value = value[int(key)]
            else:
                return None
        return value

    @staticmethod
    def replace_variables(template: str, variables: Dict) -> str:
        """
        替换模板中的变量
        :param template: 模板字符串，如 "Hello ${name}"
        :param variables: 变量字典
        :return: 替换后的字符串
        """
        result = template
        for key, value in variables.items():
            result = result.replace(f"${{{key}}}", str(value))
        return result

    @staticmethod
    def generate_random_string(length: int = 8, include_digits: bool = True) -> str:
        """生成随机字符串"""
        chars = string.ascii_letters
        if include_digits:
            chars += string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def generate_random_number(min_val: int = 1, max_val: int = 100) -> int:
        """生成随机数字"""
        return random.randint(min_val, max_val)

    @staticmethod
    def generate_timestamp(format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
        """生成当前时间戳"""
        return datetime.now().strftime(format_str)

    @staticmethod
    def generate_date(days_offset: int = 0, format_str: str = '%Y-%m-%d') -> str:
        """
        生成日期
        :param days_offset: 天数偏移量（正数为未来，负数为过去）
        :param format_str: 日期格式
        :return: 日期字符串
        """
        target_date = datetime.now() + timedelta(days=days_offset)
        return target_date.strftime(format_str)

    def generate_employee_data(self) -> Dict:
        """生成员工测试数据"""
        return {
            'employee_id': f'E{self.generate_random_number(10000, 99999)}',
            'name': self.faker.name(),
            'email': self.faker.email(),
            'phone': self.faker.phone_number(),
            'department': random.choice(['技术部', '市场部', '人力资源部', '财务部']),
            'join_date': self.generate_date(-random.randint(30, 1000))
        }

    def generate_equity_plan_data(self, stock_type: str = 'hk_us') -> Dict:
        """
        生成股权计划测试数据
        :param stock_type: 股票类型
        :return: 股权计划数据
        """
        return {
            'plan_name': f'测试股权计划_{self.generate_random_string(6)}',
            'plan_type': random.choice(['RSU', 'OPTION', 'SAR', 'ESPP']),
            'stock_type': stock_type,
            'grant_date': self.generate_date(30),
            'vesting_start_date': self.generate_date(60),
            'vesting_period': random.choice([1, 2, 3, 4]),
            'cliff_period': random.choice([0, 1]),
            'grant_amount': self.generate_random_number(1000, 10000),
            'exercise_price': round(random.uniform(1.0, 100.0), 2)
        }

    @staticmethod
    def compare_dicts(dict1: Dict, dict2: Dict, ignore_keys: List[str] = None) -> bool:
        """
        比较两个字典是否相等（可忽略指定key）
        :param dict1: 字典1
        :param dict2: 字典2
        :param ignore_keys: 忽略的key列表
        :return: 是否相等
        """
        ignore_keys = ignore_keys or []

        keys1 = set(dict1.keys()) - set(ignore_keys)
        keys2 = set(dict2.keys()) - set(ignore_keys)

        if keys1 != keys2:
            return False

        for key in keys1:
            if dict1[key] != dict2[key]:
                return False

        return True
