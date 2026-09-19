"""
快速启动示例
演示如何使用框架进行测试
"""
import pytest
from config import config
from api.bos import BOSAuthAPI, BOSEquityAPI
from utils.data_handler import DataHandler
from utils.logger import logger


def quick_start_example():
    """快速开始示例"""

    # 1. 获取配置
    base_url = config.get_base_url('bos')
    user = config.get_user('bos_users', 'admin_user')

    logger.info(f"测试环境: {config.get_current_env()}")
    logger.info(f"BOS URL: {base_url}")

    # 2. 创建API实例
    auth_api = BOSAuthAPI(base_url)
    equity_api = BOSEquityAPI(base_url)

    # 3. 登录
    logger.info("步骤1: 登录BOS系统")
    login_resp = auth_api.login(user['username'], user['password'])
    token = login_resp['data']['token']
    equity_api.set_token(token)
    logger.info(f"✓ 登录成功, Token: {token[:20]}...")

    # 4. 生成测试数据
    logger.info("步骤2: 生成测试数据")
    dh = DataHandler()
    plan_data = dh.generate_equity_plan_data(stock_type='hk_us')
    plan_data['stock_type'] = 'HK_US'
    logger.info(f"✓ 测试数据: {plan_data['plan_name']}")

    # 5. 创建股权计划
    logger.info("步骤3: 创建港美股股权计划")
    create_resp = equity_api.create_equity_plan(plan_data)
    if create_resp['code'] == 0:
        plan_id = create_resp['data']['plan_id']
        logger.info(f"✓ 计划创建成功: {plan_id}")

        # 6. 查询计划详情
        logger.info("步骤4: 查询计划详情")
        detail_resp = equity_api.get_equity_plan_detail(plan_id)
        if detail_resp['code'] == 0:
            logger.info(f"✓ 计划详情: {detail_resp['data']}")

        # 7. 清理数据
        logger.info("步骤5: 清理测试数据")
        equity_api.delete_equity_plan(plan_id)
        logger.info(f"✓ 计划已删除: {plan_id}")

    # 8. 登出
    logger.info("步骤6: 登出")
    auth_api.logout()
    logger.info("✓ 登出成功")

    logger.info("=" * 60)
    logger.info("快速开始示例执行完成！")
    logger.info("=" * 60)


if __name__ == '__main__':
    """
    直接运行此文件进行快速测试：

    python examples/quick_start.py
    """
    quick_start_example()
