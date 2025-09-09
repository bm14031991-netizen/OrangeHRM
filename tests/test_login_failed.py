import pytest

from pages.LoginPage import LoginPage


class TestLoginFailed:

    @pytest.mark.negative

    def test_login_failed(self, create_driver_orange_negative):
        self.login_page = LoginPage(create_driver_orange_negative)
        self.login_page.assert_invalid_credentials()
        pass