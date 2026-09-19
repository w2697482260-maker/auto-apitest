"""
BOS端 - 未上市股权业务测试用例
"""
import pytest
import allure
from utils.data_handler import DataHandler


@allure.feature("BOS端")
@allure.story("未上市股权管理")
@pytest.mark.bos
@pytest.mark.unlisted
class TestBOSUnlistedStock:
    """BOS端未上市股权业务测试"""

    @allure.title("创建未上市股权计划")
    @allure.description("测试创建未上市类型的股权计划")
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_create_unlisted_equity_plan(self, bos_admin_session, data_handler, cleanup_equity_plans):
        """创建未上市股权计划"""

        plan_data = data_handler.generate_equity_plan_data(stock_type='unlisted')
        plan_data['stock_type'] = 'UNLISTED'
        plan_data['market'] = 'PRIVATE'
        plan_data['currency'] = 'CNY'

        with allure.step("创建未上市股权计划"):
            resp = bos_admin_session.create_equity_plan(plan_data)

        with allure.step("验证计划创建成功"):
            assert resp['code'] == 0
            plan_id = resp['data'].get('plan_id')
            assert plan_id is not None
            cleanup_equity_plans.append(plan_id)

    @allure.title("查询未上市股权计划列表")
    @allure.description("测试查询未上市股权计划列表")
    @pytest.mark.p0
    def test_get_unlisted_plan_list(self, bos_admin_session):
        """查询未上市股权计划列表"""

        params = {
            'stock_type': 'UNLISTED',
            'page': 1,
            'page_size': 10
        }

        with allure.step("查询未上市计划列表"):
            resp = bos_admin_session.get_equity_plan_list(params)

        with allure.step("验证查询结果"):
            assert resp['code'] == 0
            assert 'data' in resp

    @allure.title("未上市股权估值更新")
    @allure.description("测试更新未上市股权的估值")
    @pytest.mark.p1
    def test_update_unlisted_valuation(self, bos_admin_session, data_handler, cleanup_equity_plans):
        """未上市股权估值更新"""

        # 创建未上市计划
        plan_data = data_handler.generate_equity_plan_data(stock_type='unlisted')
        plan_data['stock_type'] = 'UNLISTED'
        create_resp = bos_admin_session.create_equity_plan(plan_data)
        plan_id = create_resp['data']['plan_id']
        cleanup_equity_plans.append(plan_id)

        # 更新估值
        update_data = {
            'valuation': 15.5,
            'valuation_date': data_handler.generate_date(0)
        }

        with allure.step("更新估值"):
            resp = bos_admin_session.update_equity_plan(plan_id, update_data)

        with allure.step("验证更新成功"):
            assert resp['code'] == 0
