from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


import time

from pages.BasePage import BasePage


class LoginPage(BasePage):
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M")
    d_string = now.strftime("%d.%m.%Y")


    def switch_to_window_1(self):
        self.switch_to_windows(1)


    def switch_to_window_0(self):
        self.switch_to_windows(0)


    def assert_invalid_credentials(self):
        try:
            time.sleep(1)
            self.driver.find_element(By.XPATH, f'//div[@role="alert"]//p[contains(., "Invalid credentials")]')
            return True
        except TimeoutException:
            return False

    def go_to_pim(self):
        self.click((By.XPATH, '//*[@href="/web/index.php/pim/viewPimModule"]'))