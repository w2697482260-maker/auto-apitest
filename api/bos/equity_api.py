"""
BOS端股权API
"""
import allure
from typing import Dict, List, Optional
from api.base_api import BaseAPI


class BOSEquityAPI(BaseAPI):
    """BOS端股权管理API"""

    @allure.step("创建股权计划")
    def create_equity_plan(self, plan_data: Dict) -> dict:
        """
        创建股权计划
        :param plan_data: 股权计划数据
        :return: 创建结果
        """
        response = self.client.post('/api/bos/equity/plan/create', json=plan_data)
        self.assertions.assert_status_code(response, 200, "创建股权计划状态码验证")

        resp_json = response.json()
        self.assertions.assert_equal(resp_json.get('code'), 0, "创建股权计划业务码验证")

        return resp_json

    @allure.step("获取股权计划列表")
    def get_equity_plan_list(self, params: Optional[Dict] = None) -> dict:
        """
        获取股权计划列表
        :param params: 查询参数（分页、筛选等）
        :return: 计划列表
        """
        response = self.client.get('/api/bos/equity/plan/list', params=params)
        self.assertions.assert_status_code(response, 200, "获取计划列表状态码验证")
        return response.json()

    @allure.step("获取股权计划详情")
    def get_equity_plan_detail(self, plan_id: str) -> dict:
        """
        获取股权计划详情
        :param plan_id: 计划ID
        :return: 计划详情
        """
        response = self.client.get(f'/api/bos/equity/plan/{plan_id}')
        self.assertions.assert_status_code(response, 200, "获取计划详情状态码验证")
        return response.json()

    @allure.step("更新股权计划")
    def update_equity_plan(self, plan_id: str, plan_data: Dict) -> dict:
        """
        更新股权计划
        :param plan_id: 计划ID
        :param plan_data: 更新数据
        :return: 更新结果
        """
        response = self.client.put(f'/api/bos/equity/plan/{plan_id}', json=plan_data)
        self.assertions.assert_status_code(response, 200, "更新股权计划状态码验证")
        return response.json()

    @allure.step("删除股权计划")
    def delete_equity_plan(self, plan_id: str) -> dict:
        """
        删除股权计划
        :param plan_id: 计划ID
        :return: 删除结果
        """
        response = self.client.delete(f'/api/bos/equity/plan/{plan_id}')
        self.assertions.assert_status_code(response, 200, "删除股权计划状态码验证")
        return response.json()

    @allure.step("提交股权计划审批")
    def submit_equity_plan(self, plan_id: str) -> dict:
        """
        提交股权计划审批
        :param plan_id: 计划ID
        :return: 提交结果
        """
        response = self.client.post(f'/api/bos/equity/plan/{plan_id}/submit')
        self.assertions.assert_status_code(response, 200, "提交审批状态码验证")
        return response.json()

    @allure.step("批量授予股权")
    def batch_grant(self, grant_data: Dict) -> dict:
        """
        批量授予股权
        :param grant_data: 授予数据（包含员工列表、授予数量等）
        :return: 授予结果
        """
        response = self.client.post('/api/bos/equity/grant/batch', json=grant_data)
        self.assertions.assert_status_code(response, 200, "批量授予状态码验证")
        return response.json()

    @allure.step("获取授予记录")
    def get_grant_records(self, params: Optional[Dict] = None) -> dict:
        """
        获取授予记录
        :param params: 查询参数
        :return: 授予记录列表
        """
        response = self.client.get('/api/bos/equity/grant/records', params=params)
        self.assertions.assert_status_code(response, 200, "获取授予记录状态码验证")
        return response.json()

    @allure.step("撤销授予")
    def revoke_grant(self, grant_id: str, reason: str = "") -> dict:
        """
        撤销授予
        :param grant_id: 授予ID
        :param reason: 撤销原因
        :return: 撤销结果
        """
        payload = {"reason": reason}
        response = self.client.post(f'/api/bos/equity/grant/{grant_id}/revoke', json=payload)
        self.assertions.assert_status_code(response, 200, "撤销授予状态码验证")
        return response.json()
