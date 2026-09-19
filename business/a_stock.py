"""
A股业务流程封装
"""
import allure
from utils.logger import logger


class AStockBusiness:
    """A股业务流程类"""

    def __init__(self, bos_api, admin_api, staff_api):
        self.bos_api = bos_api
        self.admin_api = admin_api
        self.staff_api = staff_api

    @allure.step("A股完整授予流程")
    def complete_a_stock_flow(self, plan_data: dict, employee_ids: list) -> dict:
        """
        A股完整授予流程（遵循A股交易规则）
        1. 创建A股计划（数量必须是100的倍数）
        2. 提交审批
        3. Admin审批
        4. 授予股权（验证100倍数规则）

        :param plan_data: 股权计划数据
        :param employee_ids: 员工ID列表
        :return: 流程结果
        """
        result = {}

        # 1. 创建A股计划
        logger.info("步骤1: 创建A股股权计划")
        plan_data['stock_type'] = 'A_STOCK'
        plan_data['market'] = 'SH'  # 上交所
        plan_data['currency'] = 'CNY'

        # A股规则：授予数量必须是100的倍数
        grant_amount = plan_data.get('grant_amount', 1000)
        plan_data['grant_amount'] = (grant_amount // 100) * 100

        create_resp = self.bos_api.create_equity_plan(plan_data)
        assert create_resp['code'] == 0, f"创建A股计划失败: {create_resp}"
        plan_id = create_resp['data']['plan_id']
        result['plan_id'] = plan_id
        logger.info(f"A股计划创建成功: {plan_id}, 授予数量: {plan_data['grant_amount']}")

        # 2. 提交审批
        logger.info("步骤2: 提交审批")
        submit_resp = self.bos_api.submit_equity_plan(plan_id)
        assert submit_resp['code'] == 0, f"提交审批失败: {submit_resp}"

        # 3. 审批通过
        logger.info("步骤3: Admin审批通过")
        approve_resp = self.admin_api.approve_equity_plan(plan_id, True, "A股计划审批通过")

        # 4. 批量授予（遵循100倍数规则）
        logger.info("步骤4: 批量授予A股（遵循100倍数规则）")
        grant_data = {
            'plan_id': plan_id,
            'stock_type': 'A_STOCK',
            'grants': []
        }

        for emp_id in employee_ids:
            # 每人授予数量也必须是100的倍数
            amount = 1000  # 默认1000股
            grant_data['grants'].append({
                'employee_id': emp_id,
                'grant_amount': amount,
                'grant_price': plan_data.get('exercise_price', 10.0)
            })

        grant_resp = self.bos_api.batch_grant(grant_data)
        assert grant_resp['code'] == 0, f"批量授予失败: {grant_resp}"
        result['grant_ids'] = grant_resp['data'].get('grant_ids', [])
        logger.info(f"A股批量授予成功: {len(employee_ids)}人")

        return result

    @allure.step("A股数量校验测试")
    def validate_a_stock_amount_rule(self, plan_data: dict) -> dict:
        """
        测试A股授予数量必须是100倍数的规则
        :param plan_data: 股权计划数据
        :return: 校验结果
        """
        result = {}

        logger.info("测试A股100倍数规则")

        # 测试1: 非100倍数应该失败
        plan_data['stock_type'] = 'A_STOCK'
        plan_data['grant_amount'] = 150  # 不是100的倍数

        try:
            create_resp = self.bos_api.create_equity_plan(plan_data)
            if create_resp['code'] != 0:
                result['validation_works'] = True
                logger.info("✓ 非100倍数校验生效")
            else:
                result['validation_works'] = False
                logger.warning("✗ 非100倍数校验未生效")
        except Exception as e:
            result['validation_works'] = True
            result['error'] = str(e)
            logger.info(f"✓ 非100倍数被拒绝: {e}")

        return result
