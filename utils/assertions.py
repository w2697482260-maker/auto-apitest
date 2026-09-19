"""
断言工具模块
"""
import allure
from typing import Any, Union
from .logger import logger


class Assertions:
    """断言工具类"""

    @staticmethod
    def assert_equal(actual, expected, msg=""):
        """断言相等"""
        try:
            assert actual == expected, f"{msg} - 预期: {expected}, 实际: {actual}"
            logger.info(f"✓ 断言通过: {msg or '值相等'}")
            with allure.step(f"断言: {msg or '验证相等'}"):
                allure.attach(f"预期: {expected}\n实际: {actual}", "断言结果", allure.attachment_type.TEXT)
        except AssertionError as e:
            logger.error(f"✗ 断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_not_equal(actual, expected, msg=""):
        """断言不相等"""
        try:
            assert actual != expected, f"{msg} - 值不应该相等: {actual}"
            logger.info(f"✓ 断言通过: {msg or '值不相等'}")
        except AssertionError as e:
            logger.error(f"✗ 断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_in(member, container, msg=""):
        """断言包含"""
        try:
            assert member in container, f"{msg} - {member} 不在 {container} 中"
            logger.info(f"✓ 断言通过: {msg or '包含检查'}")
        except AssertionError as e:
            logger.error(f"✗ 断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_not_in(member, container, msg=""):
        """断言不包含"""
        try:
            assert member not in container, f"{msg} - {member} 不应该在 {container} 中"
            logger.info(f"✓ 断言通过: {msg or '不包含检查'}")
        except AssertionError as e:
            logger.error(f"✗ 断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_true(condition, msg=""):
        """断言为真"""
        try:
            assert condition is True, f"{msg} - 条件应该为True"
            logger.info(f"✓ 断言通过: {msg or '条件为真'}")
        except AssertionError as e:
            logger.error(f"✗ 断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_false(condition, msg=""):
        """断言为假"""
        try:
            assert condition is False, f"{msg} - 条件应该为False"
            logger.info(f"✓ 断言通过: {msg or '条件为假'}")
        except AssertionError as e:
            logger.error(f"✗ 断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_is_none(obj, msg=""):
        """断言为None"""
        try:
            assert obj is None, f"{msg} - 对象应该为None, 实际为: {obj}"
            logger.info(f"✓ 断言通过: {msg or '对象为None'}")
        except AssertionError as e:
            logger.error(f"✗ 断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_is_not_none(obj, msg=""):
        """断言不为None"""
        try:
            assert obj is not None, f"{msg} - 对象不应该为None"
            logger.info(f"✓ 断言通过: {msg or '对象不为None'}")
        except AssertionError as e:
            logger.error(f"✗ 断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_greater(a, b, msg=""):
        """断言大于"""
        try:
            assert a > b, f"{msg} - {a} 不大于 {b}"
            logger.info(f"✓ 断言通过: {msg or '大于检查'}")
        except AssertionError as e:
            logger.error(f"✗ 断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_less(a, b, msg=""):
        """断言小于"""
        try:
            assert a < b, f"{msg} - {a} 不小于 {b}"
            logger.info(f"✓ 断言通过: {msg or '小于检查'}")
        except AssertionError as e:
            logger.error(f"✗ 断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_status_code(response, expected_code: int, msg=""):
        """断言HTTP状态码"""
        actual_code = response.status_code
        try:
            assert actual_code == expected_code, f"{msg} - 状态码预期: {expected_code}, 实际: {actual_code}"
            logger.info(f"✓ 状态码断言通过: {actual_code}")
            with allure.step(f"验证状态码: {expected_code}"):
                allure.attach(f"状态码: {actual_code}", "状态码验证", allure.attachment_type.TEXT)
        except AssertionError as e:
            logger.error(f"✗ 状态码断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_response_success(response, msg="接口返回成功"):
        """断言响应成功（通用）"""
        Assertions.assert_status_code(response, 200, msg)
        try:
            resp_json = response.json()
            # 根据实际接口规范调整，这里假设成功标志是 code=0 或 success=true
            if 'code' in resp_json:
                assert resp_json['code'] == 0, f"业务代码不为0: {resp_json}"
            elif 'success' in resp_json:
                assert resp_json['success'] is True, f"success不为true: {resp_json}"
            logger.info(f"✓ 接口响应成功")
        except Exception as e:
            logger.error(f"✗ 接口响应断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_json_contains(response, key: str, msg=""):
        """断言JSON响应包含指定key"""
        try:
            resp_json = response.json()
            assert key in resp_json, f"{msg} - 响应中不包含key: {key}"
            logger.info(f"✓ JSON包含key: {key}")
        except Exception as e:
            logger.error(f"✗ JSON断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_json_value(response, key: str, expected_value: Any, msg=""):
        """断言JSON响应中指定key的值"""
        try:
            resp_json = response.json()
            actual_value = resp_json.get(key)
            assert actual_value == expected_value, f"{msg} - key '{key}' 预期: {expected_value}, 实际: {actual_value}"
            logger.info(f"✓ JSON值断言通过: {key} = {expected_value}")
        except Exception as e:
            logger.error(f"✗ JSON值断言失败: {str(e)}")
            raise
