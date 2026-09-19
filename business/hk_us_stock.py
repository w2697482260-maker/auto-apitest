"""
港美股业务流程封装
"""
import allure
from utils.logger import logger


class HkUsStockBusiness:
    """港美股业务流程类"""

    def __init__(self, bos_api, admin_api, staff_api):
        """
        初始化
        :param bos_api: BOS端API实例
        :param admin_api: Admin端API实例
        :param staff_api: Staff端API实例
        """
        self.bos_api = bos_api
        self.admin_api = admin_api
        self.staff_api = staff_api

    @allure.step("完整的港美股股权授予流程")
    def complete_grant_flow(self, plan_data: dict, employee_ids: list) -> dict:
        """
        完整的港美股股权授予流程
        1. BOS创建计划
        2. BOS提交审批
        3. Admin审批通过
        4. BOS批量授予
        5. Staff查看股权

        :param plan_data: 股权计划数据
        :param employee_ids: 员工ID列表
        :return: 流程结果
        """
        result = {}

        # 1. 创建港美股计划
        logger.info("步骤1: BOS创建港美股计划")
        plan_data['stock_type'] = 'HK_US'
        create_resp = self.bos_api.create_equity_plan(plan_data)
        assert create_resp['code'] == 0, f"创建计划失败: {create_resp}"
        plan_id = create_resp['data']['plan_id']
        result['plan_id'] = plan_id
        logger.info(f"计划创建成功: {plan_id}")

        # 2. 提交审批
        logger.info("步骤2: 提交审批")
        submit_resp = self.bos_api.submit_equity_plan(plan_id)
        assert submit_resp['code'] == 0, f"提交审批失败: {submit_resp}"
        logger.info("提交审批成功")

        # 3. Admin审批通过
        logger.info("步骤3: Admin审批通过")
        approve_resp = self.admin_api.approve_equity_plan(plan_id, True, "审批通过")
        logger.info("审批通过")

        # 4. 批量授予
        logger.info("步骤4: 批量授予股权")
        grant_data = {
            'plan_id': plan_id,
            'stock_type': 'HK_US',
            'grants': [
                {
                    'employee_id': emp_id,
                    'grant_amount': 1000,
                    'grant_price': plan_data.get('exercise_price', 10.0)
                }
                for emp_id in employee_ids
            ]
        }
        grant_resp = self.bos_api.batch_grant(grant_data)
        assert grant_resp['code'] == 0, f"批量授予失败: {grant_resp}"
        result['grant_ids'] = grant_resp['data'].get('grant_ids', [])
        logger.info(f"批量授予成功: {len(employee_ids)}人")

        # 5. Staff查看股权
        logger.info("步骤5: 员工查看股权")
        equity_resp = self.staff_api.get_my_equity()
        result['staff_equity'] = equity_resp['data']
        logger.info("员工查看股权成功")

        return result

    @allure.step("港美股归属与行权流程")
    def vesting_and_exercise_flow(self, equity_id: str, exercise_amount: int) -> dict:
        """
        港美股归属与行权流程
        1. 查看归属时间表
        2. 等待归属（模拟）
        3. 行权
        4. 查看行权历史

        :param equity_id: 股权ID
        :param exercise_amount: 行权数量
        :return: 流程结果
        """
        result = {}

        # 1. 查看归属时间表
        logger.info("步骤1: 查看归属时间表")
        schedule_resp = self.staff_api.get_vesting_schedule(equity_id)
        result['vesting_schedule'] = schedule_resp['data']

        # 2. 行权
        logger.info("步骤2: 提交行权申请")
        exercise_resp = self.staff_api.exercise(equity_id, exercise_amount)
        assert exercise_resp['code'] == 0, f"行权失败: {exercise_resp}"
        result['exercise_id'] = exercise_resp['data'].get('exercise_id')
        logger.info(f"行权成功: {exercise_amount}股")

        # 3. 查看行权历史
        logger.info("步骤3: 查看行权历史")
        history_resp = self.staff_api.get_exercise_history()
        result['exercise_history'] = history_resp['data']

        return result
