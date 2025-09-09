from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.BasePage import BasePage


class PimPage(BasePage):

    ADD_BTN = (By.XPATH, '//*[@class="orangehrm-header-container"]//*[@type="button"]')

    # Поля формы создания сотрудника
    FIRST_NAME = (By.NAME, 'firstName')
    LAST_NAME = (By.NAME, 'lastName')
    SAVE_BTN = (By.XPATH, '//button[@type="submit"]')
    PERSONAL_DETAILS = (By.XPATH, '//*[@class="oxd-text oxd-text--h6 orangehrm-main-title"]')

    # Поиск в списке сотрудников
    EMPLOYEE_NAME_FILTER = (By.XPATH, '//*[@class="orangehrm-employee-form"]//*[@class="oxd-input oxd-input--active"]')
    EMPLOYEE_ID = (By.XPATH, '//div[contains(@class, "oxd-input-group__label-wrapper")]//label[text()="Employee Id"]//following::input[@class="oxd-input oxd-input--active"]')
    SEARCH_BTN = (By.XPATH, '//button[@type="submit"]')
    TABLE_ROWS = (By.XPATH, '//div[]')
    SEARCH_INPUT = (By.XPATH, '//input[@placeholder="Type for hints..."]')
    ERROR_MESSAGE = (By.XPATH, '//*[contains(@class,"oxd-input-field-error-message") and text()="Employee Id already exists"]')
    EDIT_BTN = (By.XPATH, '//*[@type="button"]//*[@class="oxd-icon bi-pencil-fill"]')
    MATERIAL_STS = (By.XPATH, '//label[text()="Marital Status"]/ancestor::div[contains(@class,"oxd-input-group")]//div[@class="oxd-select-text-input"]')
    SINGLE = "Single"

     # f'//div[contains(@class, "oxd-select-dropdown")]//*[contains(text(),"Single")]')




    def click_add(self):
        self.click(self.ADD_BTN)

    def create_employee(self, first_name: str, last_name: str):
        self.input_wait(self.FIRST_NAME, first_name)
        self.input_wait(self.LAST_NAME, last_name)
        self.click_script(self.SAVE_BTN)
        self.find_element_display(self.PERSONAL_DETAILS)

        # если ошибка "Employee Id already exists"
        if self.assert_element(self.ERROR_MESSAGE):
            self.refresh_page()
            self.input_wait(self.FIRST_NAME, first_name)
            self.input_wait(self.LAST_NAME, last_name)
            self.click_script(self.SAVE_BTN)
            self.find_element_display(self.PERSONAL_DETAILS)
        # возвращаем имя
        return first_name

    def create_employee_negative(self, first_name: str):
        self.input_wait(self.FIRST_NAME, first_name)
        self.click_script(self.SAVE_BTN)

        # если ошибка "Employee Id already exists"
        if self.assert_element(self.ERROR_MESSAGE):
            self.refresh_page()
            self.input_wait(self.FIRST_NAME, first_name)
            self.click_script(self.SAVE_BTN)
        self.assert_requiered_field()

    def search_employee_by_name(self, first_name: str):
        self.input_wait(self.SEARCH_INPUT, first_name)
        self.click_wait(self.SEARCH_BTN)
        self.assert_user_name(first_name)


    def edit_employee(self):
        self.click(self.EDIT_BTN)
        # self.click(self.MATERIAL_STS)
        self.click_wait(self.MATERIAL_STS)
        self.class_wait_listbox_click("oxd-select-option", "Single")
        self.click_script(self.SAVE_BTN)
        self.assert_succes_save()


    def search_employee_by_non_existent_name(self, first_name: str):
        self.input_wait(self.SEARCH_INPUT, first_name)
        self.click_wait(self.SEARCH_BTN)


    def assert_no_records_found(self):
        elem = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, f'//*[contains(@class, "oxd-text--toast")]')
            )
        )
        assert elem is not None, f"Сотрудник с именем найден в таблице"

    def assert_browser_logs(self):
        logs = self.driver.get_log("browser")
        assert all("SEVERE" not in entry["level"] for entry in logs), f"Ошибки в консоли: {logs}"

    def search_employee_by_id(self, employee_id: str):
        self.input(self.EMPLOYEE_ID, employee_id)
        self.click(self.SEARCH_BTN)
        self.assert_user_id(employee_id)


    def assert_user_id(self, employee_id: str):
        self.find_element_display((By.XPATH, f'//*[@class="oxd-table-card"]//*[text()="{employee_id}"]'))

    def assert_user_name(self, first_name: str):
        elem = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, f'//*[@class="oxd-table-card"]//*[contains(text(), "{first_name}")]')
            )
        )
        assert elem is not None, f"Сотрудник с именем {first_name} не найден в таблице"


    def assert_succes_save(self):
        elem = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, f'//div[contains(@class, "content--success")]')
            )
        )
        assert elem is not None, f"Ошибка сохранения"

    def assert_requiered_field(self):
        elem = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, f'//*[contains(@class, "oxd-input-field-error-message")]')
            )
        )
        assert elem, f"Required field"


    def is_employee_in_table(self, full_name: str) -> bool:
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        names = [" ".join(r.text.splitlines()[0].split()) for r in rows if r.text.strip()]
        return any(full_name in n for n in names)
