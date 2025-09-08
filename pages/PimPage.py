from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class PimPage(BasePage):

    ADD_BTN = (By.XPATH, '//*[@class="orangehrm-header-container"]//*[@type="button"]')

    # Поля формы создания сотрудника
    FIRST_NAME = (By.NAME, 'firstName')
    LAST_NAME = (By.NAME, 'lastName')

    SAVE_BTN = (By.XPATH, '//button[@type="submit"]')

    # Поиск в списке сотрудников
    EMPLOYEE_NAME_FILTER = (By.XPATH, '//*[@class="orangehrm-employee-form"]//*[@class="oxd-input oxd-input--active"]')
    SEARCH_BTN = (By.XPATH, "//button[.//span[normalize-space()='Search']]")
    TABLE_ROWS = (By.XPATH, "//div[@role='table']//div[@role='row' and descendant::div[@role='cell']]")

    REQUIRED_HINT = (By.XPATH, "//span[contains(@class,'oxd-input-field-error-message')][normalize-space()='Required']")

    def click_add(self):
        self.click(self.ADD_BTN)

    def create_employee(self, first_name: str, last_name: str):
        self.input(self.FIRST_NAME, first_name)
        self.input(self.LAST_NAME, last_name)
        self.click(self.SAVE_BTN)

    # def search_employee_by_name(self, full_name: str):
    #     # Фильтр автокомплит — вводим полное имя и подтверждаем
    #     field = self.input(self.EMPLOYEE_NAME_FILTER, full_name, clear=True)
    #     # Небольшой «естественный» ввод (автокомплит не критичен — просто жмём Search)
    #     self.click(self.SEARCH_BTN)

    def is_employee_in_table(self, full_name: str) -> bool:
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        names = [" ".join(r.text.splitlines()[0].split()) for r in rows if r.text.strip()]
        return any(full_name in n for n in names)

    def required_errors_present(self) -> bool:
        return self.exists(self.REQUIRED_HINT)
