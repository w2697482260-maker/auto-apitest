"""
Admin端测试用例
"""
import pytest
import allure


@allure.feature("Admin端")
@allure.story("审批管理")
@pytest.mark.admin
class TestAdminApproval:
    """Admin端审批功能测试"""

    @allure.title("查看待审批列表")
    @allure.description("测试管理员查看待审批的股权计划列表")
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_get_pending_approvals(self, admin_super_session):
        """查看待审批列表"""

        params = {
            'status': 'PENDING',
            'page': 1,
            'page_size': 20
        }

        with allure.step("查询待审批列表"):
            resp = admin_super_session.get_pending_approvals(params)

        with allure.step("验证查询成功"):
            assert resp['code'] == 0
            assert 'data' in resp
            assert 'list' in resp['data']

    @allure.title("审批通过股权计划")
    @allure.description("测试管理员审批通过股权计划")
    @pytest.mark.p0
    def test_approve_equity_plan_pass(self, admin_super_session):
        """审批通过股权计划"""

        plan_id = "test_plan_id"  # 实际测试需要先创建待审批的计划

        with allure.step("审批通过"):
            resp = admin_super_session.approve_equity_plan(
                plan_id=plan_id,
                approved=True,
                comment="审批通过"
            )

        with allure.step("验证审批结果"):
            # 根据实际接口响应调整
            pass

    @allure.title("审批拒绝股权计划")
    @allure.description("测试管理员审批拒绝股权计划")
    @pytest.mark.p0
    def test_approve_equity_plan_reject(self, admin_super_session):
        """审批拒绝股权计划"""

        plan_id = "test_plan_id"

        with allure.step("审批拒绝"):
            resp = admin_super_session.approve_equity_plan(
                plan_id=plan_id,
                approved=False,
                comment="不符合审批要求"
            )

        with allure.step("验证审批结果"):
            pass


@allure.feature("Admin端")
@allure.story("员工管理")
@pytest.mark.admin
class TestAdminEmployee:
    """Admin端员工管理测试"""

    @allure.title("查询员工列表")
    @allure.description("测试查询员工列表")
    @pytest.mark.p0
    def test_get_employee_list(self, admin_super_session):
        """查询员工列表"""

        params = {
            'page': 1,
            'page_size': 20
        }

        with allure.step("查询员工列表"):
            resp = admin_super_session.get_employee_list(params)

        with allure.step("验证查询成功"):
            assert resp['code'] == 0
            assert 'data' in resp

    @allure.title("创建员工")
    @allure.description("测试创建新员工")
    @pytest.mark.p1
    def test_create_employee(self, admin_super_session, data_handler):
        """创建员工"""

        employee_data = data_handler.generate_employee_data()

        with allure.step("创建员工"):
            resp = admin_super_session.create_employee(employee_data)

        with allure.step("验证创建成功"):
            assert resp['code'] == 0
            assert 'data' in resp
