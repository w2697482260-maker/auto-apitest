"""
未上市股权业务流程封装
"""
import allure
from utils.logger import logger


class UnlistedStockBusiness:
    """未上市股权业务流程类"""

    def __init__(self, bos_api, admin_api, staff_api):
        self.bos_api = bos_api
        self.admin_api = admin_api
        self.staff_api = staff_api

    @allure.step("未上市股权完整流程")
    def complete_unlisted_flow(self, plan_data: dict, employee_ids: list) -> dict:
        """
        未上市股权完整流程
        1. 创建未上市股权计划
        2. 提交审批
        3. Admin审批
        4. 授予股权
        5. 更新估值

        :param plan_data: 股权计划数据
        :param employee_ids: 员工ID列表
        :return: 流程结果
        """
        result = {}

        # 1. 创建未上市计划
        logger.info("步骤1: 创建未上市股权计划")
        plan_data['stock_type'] = 'UNLISTED'
        plan_data['market'] = 'PRIVATE'
        create_resp = self.bos_api.create_equity_plan(plan_data)
        assert create_resp['code'] == 0, f"创建计划失败: {create_resp}"
        plan_id = create_resp['data']['plan_id']
        result['plan_id'] = plan_id
        logger.info(f"未上市计划创建成功: {plan_id}")

        # 2. 提交审批
        logger.info("步骤2: 提交审批")
        submit_resp = self.bos_api.submit_equity_plan(plan_id)
        assert submit_resp['code'] == 0, f"提交审批失败: {submit_resp}"

        # 3. 审批通过
        logger.info("步骤3: Admin审批通过")
        approve_resp = self.admin_api.approve_equity_plan(plan_id, True, "未上市计划审批通过")

        # 4. 批量授予
        logger.info("步骤4: 批量授予未上市股权")
        grant_data = {
            'plan_id': plan_id,
            'stock_type': 'UNLISTED',
            'grants': [
                {
                    'employee_id': emp_id,
                    'grant_amount': 500,
                    'grant_price': plan_data.get('exercise_price', 1.0)
                }
                for emp_id in employee_ids
            ]
        }
        grant_resp = self.bos_api.batch_grant(grant_data)
        result['grant_ids'] = grant_resp['data'].get('grant_ids', [])
        logger.info(f"批量授予成功: {len(employee_ids)}人")

        return result

    @allure.step("未上市股权估值更新流程")
    def valuation_update_flow(self, plan_id: str, new_valuation: float) -> dict:
        """
        未上市股权估值更新流程
        :param plan_id: 计划ID
        :param new_valuation: 新估值
        :return: 更新结果
        """
        result = {}

        logger.info(f"更新未上市股权估值: {plan_id} -> {new_valuation}")

        from utils.data_handler import DataHandler
        dh = DataHandler()

        update_data = {
            'valuation': new_valuation,
            'valuation_date': dh.generate_date(0)
        }

        update_resp = self.bos_api.update_equity_plan(plan_id, update_data)
        assert update_resp['code'] == 0, f"估值更新失败: {update_resp}"
        result['updated'] = True
        logger.info("估值更新成功")

        # 验证更新
        detail_resp = self.bos_api.get_equity_plan_detail(plan_id)
        result['current_valuation'] = detail_resp['data'].get('valuation')

        return result
