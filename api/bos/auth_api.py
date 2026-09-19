"""
BOS端认证API
"""
import allure
from api.base_api import BaseAPI


class BOSAuthAPI(BaseAPI):
    """BOS端认证API"""

    @allure.step("BOS端登录")
    def login(self, username: str, password: str) -> dict:
        """
        BOS端登录
        :param username: 用户名
        :param password: 密码
        :return: 登录响应数据
        """
        payload = {
            "username": username,
            "password": password
        }

        response = self.client.post('/api/bos/auth/login', json=payload)
        self.assertions.assert_status_code(response, 200, "登录接口状态码验证")

        resp_json = response.json()

        # 根据实际接口调整
        if resp_json.get('code') == 0:
            token = resp_json.get('data', {}).get('token')
            if token:
                self.set_token(token)
            return resp_json
        else:
            raise Exception(f"登录失败: {resp_json.get('message', '未知错误')}")

    @allure.step("BOS端登出")
    def logout(self) -> dict:
        """BOS端登出"""
        response = self.client.post('/api/bos/auth/logout')
        self.assertions.assert_status_code(response, 200, "登出接口状态码验证")

        self.token = None
        self.client.token = None

        return response.json()

    @allure.step("获取用户信息")
    def get_user_info(self) -> dict:
        """获取当前登录用户信息"""
        response = self.client.get('/api/bos/auth/userinfo')
        self.assertions.assert_status_code(response, 200, "获取用户信息状态码验证")
        return response.json()

    @allure.step("刷新Token")
    def refresh_token(self) -> dict:
        """刷新Token"""
        response = self.client.post('/api/bos/auth/refresh')
        self.assertions.assert_status_code(response, 200, "刷新Token状态码验证")

        resp_json = response.json()
        if resp_json.get('code') == 0:
            new_token = resp_json.get('data', {}).get('token')
            if new_token:
                self.set_token(new_token)

        return resp_json
