import pytest

from pages.LoginPage import LoginPage
from pages.DashboardPage import DashboardPage
from pages.PimPage import PimPage
from pages.EmployeeProfile_page import EmployeeProfilePage
from utils.data_generator import employee_name


@pytest.mark.Smoke
@pytest.mark.Regression
class TestPolyDocAddAssignKDUWithoutRecordStateNameCode:

    @pytest.mark.uipolylkv

    def test_create_edit_employee_and_validate_ui(self, create_driver_orange):
        self.login_page = LoginPage(create_driver_orange)
        self.pim = PimPage(create_driver_orange)
        self.dashboard = DashboardPage(create_driver_orange)
        self.employee = EmployeeProfilePage(create_driver_orange)
        self.login_page.go_to_pim()
        first, middle, last, full = employee_name()
        self.pim.click_add()
        self.pim.create_employee(first, last)
        pass
