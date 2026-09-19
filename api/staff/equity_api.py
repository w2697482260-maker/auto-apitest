"""
Staff端股权API
"""
import allure
from typing import Dict, Optional
from api.base_api import BaseAPI


class StaffEquityAPI(BaseAPI):
    """Staff端股权API"""

    @allure.step("查看我的股权")
    def get_my_equity(self, params: Optional[Dict] = None) -> dict:
        """查看我的股权"""
        response = self.client.get('/api/staff/equity/my', params=params)
        self.assertions.assert_status_code(response, 200, "查看我的股权状态码验证")
        return response.json()

    @allure.step("查看股权详情")
    def get_equity_detail(self, equity_id: str) -> dict:
        """查看股权详情"""
        response = self.client.get(f'/api/staff/equity/{equity_id}')
        self.assertions.assert_status_code(response, 200, "查看股权详情状态码验证")
        return response.json()

    @allure.step("行权")
    def exercise(self, equity_id: str, amount: int) -> dict:
        """
        行权
        :param equity_id: 股权ID
        :param amount: 行权数量
        :return: 行权结果
        """
        payload = {
            "equity_id": equity_id,
            "amount": amount
        }
        response = self.client.post('/api/staff/equity/exercise', json=payload)
        self.assertions.assert_status_code(response, 200, "行权状态码验证")
        return response.json()

    @allure.step("获取行权历史")
    def get_exercise_history(self, params: Optional[Dict] = None) -> dict:
        """获取行权历史"""
        response = self.client.get('/api/staff/equity/exercise/history', params=params)
        self.assertions.assert_status_code(response, 200, "获取行权历史状态码验证")
        return response.json()

    @allure.step("获取归属时间表")
    def get_vesting_schedule(self, equity_id: str) -> dict:
        """获取归属时间表"""
        response = self.client.get(f'/api/staff/equity/{equity_id}/vesting-schedule')
        self.assertions.assert_status_code(response, 200, "获取归属时间表状态码验证")
        return response.json()
