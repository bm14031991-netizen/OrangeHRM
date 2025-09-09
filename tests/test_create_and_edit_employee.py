import pytest

from pages.LoginPage import LoginPage
from pages.DashboardPage import DashboardPage
from pages.PimPage import PimPage
from pages.EmployeeProfile_page import EmployeeProfilePage
from utils.data_generator import employee_name


class TestCreateEditEmployee:

    @pytest.mark.e2e

    def test_create_and_edit_employee(self, create_driver_orange):

        self.login_page = LoginPage(create_driver_orange)
        self.pim = PimPage(create_driver_orange)
        self.dashboard = DashboardPage(create_driver_orange)
        self.employee = EmployeeProfilePage(create_driver_orange)
        self.login_page.go_to_pim()
        first, middle, last, full = employee_name()
        self.pim.click_add()
        self.pim.create_employee(first, last)
        self.login_page.go_to_pim()
        self.pim.search_employee_by_name(first)
        self.pim.edit_employee()

        pass