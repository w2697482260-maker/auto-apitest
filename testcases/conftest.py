"""
测试用例conftest
公共fixtures配置
"""
import os
import pytest
import allure
from config import config
from api.bos import BOSAuthAPI, BOSEquityAPI
from api.admin import AdminAuthAPI, AdminManagementAPI
from api.staff import StaffAuthAPI, StaffEquityAPI
from utils.data_handler import DataHandler
from utils.logger import logger


@pytest.fixture(scope="session")
def env():
    """获取当前测试环境"""
    return config.get_current_env()


@pytest.fixture(scope="session")
def data_handler():
    """数据处理工具实例"""
    return DataHandler()


# ==================== BOS端 Fixtures ====================

@pytest.fixture(scope="session")
def bos_auth_api():
    """BOS认证API实例"""
    base_url = config.get_base_url('bos')
    return BOSAuthAPI(base_url)


@pytest.fixture(scope="session")
def bos_equity_api():
    """BOS股权API实例"""
    base_url = config.get_base_url('bos')
    return BOSEquityAPI(base_url)


@pytest.fixture(scope="session")
def bos_admin_token(bos_auth_api):
    """BOS管理员登录并返回token"""
    user = config.get_user('bos_users', 'admin_user')
    logger.info(f"BOS管理员登录: {user['username']}")

    resp = bos_auth_api.login(user['username'], user['password'])
    token = resp.get('data', {}).get('token')

    yield token

    # 登出
    try:
        bos_auth_api.logout()
    except:
        pass


@pytest.fixture(scope="function")
def bos_admin_session(bos_equity_api, bos_admin_token):
    """BOS管理员会话（function级别，每个用例独立）"""
    bos_equity_api.set_token(bos_admin_token)
    yield bos_equity_api


# ==================== Admin端 Fixtures ====================

@pytest.fixture(scope="session")
def admin_auth_api():
    """Admin认证API实例"""
    base_url = config.get_base_url('admin')
    return AdminAuthAPI(base_url)


@pytest.fixture(scope="session")
def admin_management_api():
    """Admin管理API实例"""
    base_url = config.get_base_url('admin')
    return AdminManagementAPI(base_url)


@pytest.fixture(scope="session")
def admin_super_token(admin_auth_api):
    """Admin超级管理员登录并返回token"""
    user = config.get_user('admin_users', 'super_admin')
    logger.info(f"Admin超管登录: {user['username']}")

    resp = admin_auth_api.login(user['username'], user['password'])
    token = resp.get('data', {}).get('token')

    yield token

    try:
        admin_auth_api.logout()
    except:
        pass


@pytest.fixture(scope="function")
def admin_super_session(admin_management_api, admin_super_token):
    """Admin超管会话"""
    admin_management_api.set_token(admin_super_token)
    yield admin_management_api


# ==================== Staff端 Fixtures ====================

@pytest.fixture(scope="session")
def staff_auth_api():
    """Staff认证API实例"""
    base_url = config.get_base_url('staff')
    return StaffAuthAPI(base_url)


@pytest.fixture(scope="session")
def staff_equity_api():
    """Staff股权API实例"""
    base_url = config.get_base_url('staff')
    return StaffEquityAPI(base_url)


@pytest.fixture(scope="session")
def staff_token(staff_auth_api):
    """员工登录并返回token"""
    user = config.get_user('staff_users', 'employee_01')
    logger.info(f"员工登录: {user['username']}")

    resp = staff_auth_api.login(user['username'], user['password'])
    token = resp.get('data', {}).get('token')

    yield token

    try:
        staff_auth_api.logout()
    except:
        pass


@pytest.fixture(scope="function")
def staff_session(staff_equity_api, staff_token):
    """员工会话"""
    staff_equity_api.set_token(staff_token)
    yield staff_equity_api


# ==================== 数据清理 Fixtures ====================

@pytest.fixture(scope="function")
def cleanup_equity_plans(bos_admin_session):
    """清理测试创建的股权计划"""
    created_plan_ids = []

    yield created_plan_ids

    # 清理
    for plan_id in created_plan_ids:
        try:
            logger.info(f"清理股权计划: {plan_id}")
            bos_admin_session.delete_equity_plan(plan_id)
        except Exception as e:
            logger.warning(f"清理股权计划失败: {e}")


# ==================== Allure报告增强 ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """用例执行结果处理"""
    outcome = yield
    report = outcome.get_result()

    # 添加用例描述到报告
    if report.when == "call":
        # 添加环境信息
        allure.dynamic.parameter("环境", config.get_current_env())

        # 失败截图/日志
        if report.failed:
            # 可以在这里添加失败时的额外信息
            pass


def pytest_configure(config):
    """Pytest配置钩子"""
    # 添加自定义标记说明
    config.addinivalue_line(
        "markers", "bos: BOS端测试用例"
    )
    config.addinivalue_line(
        "markers", "admin: Admin端测试用例"
    )
    config.addinivalue_line(
        "markers", "staff: Staff端测试用例"
    )


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成后的处理
    用于修改用例名称、添加标记等
    """
    for item in items:
        # 设置用例中文名称
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
