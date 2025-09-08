from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class DashboardPage(BasePage):
    # Сайдбар со ссылкой PIM
    PIM_LINK = (By.XPATH, "//span[normalize-space()='PIM']")

    def go_to_pim(self):
        self.click(self.PIM_LINK)
        # Переход ведёт на страницу со списком сотрудников
        # URL содержит /pim/viewEmployeeList
