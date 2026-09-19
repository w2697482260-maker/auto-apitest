"""
BOS端股权计划API（包含港美股、未上市、A股）
"""
import allure
from api.base_api import BaseAPI


class BOSPlanAPI(BaseAPI):
    """BOS端股权计划API"""

    @allure.step("创建港美股股权计划")
    def create_hk_us_plan(self, plan_data: dict) -> dict:
        """创建港美股股权计划"""
        plan_data['stock_type'] = 'HK_US'
        response = self.client.post('/api/bos/plan/create', json=plan_data)
        self.assertions.assert_status_code(response, 200, "创建港美股计划状态码验证")
        return response.json()

    @allure.step("创建未上市股权计划")
    def create_unlisted_plan(self, plan_data: dict) -> dict:
        """创建未上市股权计划"""
        plan_data['stock_type'] = 'UNLISTED'
        response = self.client.post('/api/bos/plan/create', json=plan_data)
        self.assertions.assert_status_code(response, 200, "创建未上市计划状态码验证")
        return response.json()

    @allure.step("创建A股股权计划")
    def create_a_stock_plan(self, plan_data: dict) -> dict:
        """创建A股股权计划"""
        plan_data['stock_type'] = 'A_STOCK'
        response = self.client.post('/api/bos/plan/create', json=plan_data)
        self.assertions.assert_status_code(response, 200, "创建A股计划状态码验证")
        return response.json()
