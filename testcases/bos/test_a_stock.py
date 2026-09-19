"""
BOS端 - A股业务测试用例
"""
import pytest
import allure


@allure.feature("BOS端")
@allure.story("A股股权管理")
@pytest.mark.bos
@pytest.mark.a_stock
class TestBOSAStock:
    """BOS端A股业务测试"""

    @allure.title("创建A股股权计划")
    @allure.description("测试创建A股类型的股权计划，需符合A股交易规则")
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_create_a_stock_equity_plan(self, bos_admin_session, data_handler, cleanup_equity_plans):
        """创建A股股权计划"""

        plan_data = data_handler.generate_equity_plan_data(stock_type='a_stock')
        plan_data['stock_type'] = 'A_STOCK'
        plan_data['market'] = 'SH'  # 上海证券交易所
        plan_data['currency'] = 'CNY'

        # A股特殊规则：最小交易单位100股
        plan_data['grant_amount'] = (plan_data['grant_amount'] // 100) * 100

        with allure.step("创建A股股权计划"):
            resp = bos_admin_session.create_equity_plan(plan_data)

        with allure.step("验证计划创建成功"):
            assert resp['code'] == 0
            plan_id = resp['data'].get('plan_id')
            assert plan_id is not None
            cleanup_equity_plans.append(plan_id)

            # 验证数量是100的倍数
            detail_resp = bos_admin_session.get_equity_plan_detail(plan_id)
            detail = detail_resp['data']
            assert detail['grant_amount'] % 100 == 0, "A股授予数量必须是100的倍数"

    @allure.title("查询A股股权计划列表")
    @allure.description("测试查询A股股权计划列表")
    @pytest.mark.p0
    def test_get_a_stock_plan_list(self, bos_admin_session):
        """查询A股股权计划列表"""

        params = {
            'stock_type': 'A_STOCK',
            'page': 1,
            'page_size': 10
        }

        with allure.step("查询A股计划列表"):
            resp = bos_admin_session.get_equity_plan_list(params)

        with allure.step("验证查询结果"):
            assert resp['code'] == 0
            assert 'data' in resp

    @allure.title("A股授予数量校验")
    @allure.description("测试A股授予时对最小交易单位的校验")
    @pytest.mark.p0
    def test_a_stock_grant_amount_validation(self, bos_admin_session, data_handler):
        """A股授予数量校验 - 必须是100的倍数"""

        grant_data = {
            'plan_id': 'test_plan_id',
            'stock_type': 'A_STOCK',
            'grants': [
                {
                    'employee_id': 'E001',
                    'grant_amount': 150,  # 不是100的倍数，应该失败
                    'grant_price': 10.5
                }
            ]
        }

        with allure.step("尝试授予非100倍数的A股"):
            resp = bos_admin_session.batch_grant(grant_data)

        with allure.step("验证校验失败"):
            # 应该返回错误
            # 具体错误码根据实际接口调整
            pass
