"""
Staff端测试用例
"""
import pytest
import allure


@allure.feature("Staff端")
@allure.story("我的股权")
@pytest.mark.staff
class TestStaffEquity:
    """Staff端股权查看测试"""

    @allure.title("查看我的股权")
    @allure.description("测试员工查看自己的股权信息")
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_get_my_equity(self, staff_session):
        """查看我的股权"""

        params = {
            'page': 1,
            'page_size': 10
        }

        with allure.step("查询我的股权"):
            resp = staff_session.get_my_equity(params)

        with allure.step("验证查询成功"):
            assert resp['code'] == 0
            assert 'data' in resp

    @allure.title("查看股权详情")
    @allure.description("测试员工查看股权详细信息")
    @pytest.mark.p0
    def test_get_equity_detail(self, staff_session):
        """查看股权详情"""

        equity_id = "test_equity_id"  # 实际需要先获取有效的equity_id

        with allure.step("查询股权详情"):
            resp = staff_session.get_equity_detail(equity_id)

        with allure.step("验证查询结果"):
            # 根据实际情况调整
            pass

    @allure.title("查看归属时间表")
    @allure.description("测试员工查看股权归属时间表")
    @pytest.mark.p1
    def test_get_vesting_schedule(self, staff_session):
        """查看归属时间表"""

        equity_id = "test_equity_id"

        with allure.step("查询归属时间表"):
            resp = staff_session.get_vesting_schedule(equity_id)

        with allure.step("验证查询结果"):
            pass

    @allure.title("查看行权历史")
    @allure.description("测试员工查看历史行权记录")
    @pytest.mark.p1
    def test_get_exercise_history(self, staff_session):
        """查看行权历史"""

        params = {
            'page': 1,
            'page_size': 20
        }

        with allure.step("查询行权历史"):
            resp = staff_session.get_exercise_history(params)

        with allure.step("验证查询成功"):
            assert resp['code'] == 0


@allure.feature("Staff端")
@allure.story("股权行权")
@pytest.mark.staff
class TestStaffExercise:
    """Staff端行权功能测试"""

    @allure.title("股权行权")
    @allure.description("测试员工行使已归属的股权")
    @pytest.mark.p0
    def test_exercise_equity(self, staff_session):
        """股权行权"""

        equity_id = "test_equity_id"
        amount = 100

        with allure.step("提交行权申请"):
            resp = staff_session.exercise(equity_id, amount)

        with allure.step("验证行权结果"):
            # 根据实际情况调整
            pass
