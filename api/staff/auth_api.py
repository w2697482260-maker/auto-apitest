"""
Staff端认证API
"""
import allure
from api.base_api import BaseAPI


class StaffAuthAPI(BaseAPI):
    """Staff端认证API"""

    @allure.step("Staff端登录")
    def login(self, username: str, password: str) -> dict:
        """
        Staff端登录
        :param username: 用户名
        :param password: 密码
        :return: 登录响应数据
        """
        payload = {
            "username": username,
            "password": password
        }

        response = self.client.post('/api/staff/auth/login', json=payload)
        self.assertions.assert_status_code(response, 200, "登录接口状态码验证")

        resp_json = response.json()

        if resp_json.get('code') == 0:
            token = resp_json.get('data', {}).get('token')
            if token:
                self.set_token(token)
            return resp_json
        else:
            raise Exception(f"登录失败: {resp_json.get('message', '未知错误')}")

    @allure.step("Staff端登出")
    def logout(self) -> dict:
        """Staff端登出"""
        response = self.client.post('/api/staff/auth/logout')
        self.assertions.assert_status_code(response, 200, "登出接口状态码验证")

        self.token = None
        self.client.token = None

        return response.json()
