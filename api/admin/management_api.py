"""
Admin端管理API
"""
import allure
from typing import Dict, Optional
from api.base_api import BaseAPI


class AdminManagementAPI(BaseAPI):
    """Admin端管理API"""

    @allure.step("获取员工列表")
    def get_employee_list(self, params: Optional[Dict] = None) -> dict:
        """获取员工列表"""
        response = self.client.get('/api/admin/employee/list', params=params)
        self.assertions.assert_status_code(response, 200, "获取员工列表状态码验证")
        return response.json()

    @allure.step("创建员工")
    def create_employee(self, employee_data: Dict) -> dict:
        """创建员工"""
        response = self.client.post('/api/admin/employee/create', json=employee_data)
        self.assertions.assert_status_code(response, 200, "创建员工状态码验证")
        return response.json()

    @allure.step("审批股权计划")
    def approve_equity_plan(self, plan_id: str, approved: bool, comment: str = "") -> dict:
        """
        审批股权计划
        :param plan_id: 计划ID
        :param approved: 是否批准
        :param comment: 审批意见
        :return: 审批结果
        """
        payload = {
            "approved": approved,
            "comment": comment
        }
        response = self.client.post(f'/api/admin/equity/plan/{plan_id}/approve', json=payload)
        self.assertions.assert_status_code(response, 200, "审批计划状态码验证")
        return response.json()

    @allure.step("获取待审批列表")
    def get_pending_approvals(self, params: Optional[Dict] = None) -> dict:
        """获取待审批列表"""
        response = self.client.get('/api/admin/approval/pending', params=params)
        self.assertions.assert_status_code(response, 200, "获取待审批列表状态码验证")
        return response.json()
