import pytest

from pages.LoginPage import LoginPage
from pages.DashboardPage import DashboardPage
from pages.PimPage import PimPage
from pages.EmployeeProfile_page import EmployeeProfilePage
from utils.data_generator import employee_name


class TestNonExistentEmployee:

    @pytest.mark.negative

    def test_search_non_existent_employee(self, create_driver_orange):

        self.login_page = LoginPage(create_driver_orange)
        self.pim = PimPage(create_driver_orange)
        self.dashboard = DashboardPage(create_driver_orange)
        self.employee = EmployeeProfilePage(create_driver_orange)
        self.login_page.go_to_pim()
        first = employee_name()
        self.pim.search_employee_by_non_existent_name(first)
        self.pim.assert_no_records_found()
        self.pim.assert_browser_logs()

        pass
