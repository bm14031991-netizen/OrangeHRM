from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class EmployeeProfilePage(BasePage):
    # Пример редактируемого поля: Job Title или статус (в демо — вкладка Job)
    JOB_TAB = (By.XPATH, "//a[normalize-space()='Job']")
    JOB_TITLE_DROPDOWN = (By.XPATH, "//label[normalize-space()='Job Title']/following::div[contains(@class,'oxd-select-wrapper')][1]")
    JOB_TITLE_OPTION_ANY = (By.XPATH, "//div[@role='listbox']//span[@class='oxd-select-option']/span")  # выберем первый доступный
    JOB_SAVE = (By.XPATH, "//button[@type='submit']")

    TOAST_SUCCESS = (By.XPATH, "//p[contains(@class,'oxd-toast-content-text') and contains(.,'Success')]")

    def open_job_tab(self):
        self.click(self.JOB_TAB)

    def change_any_job_title(self):
        self.click(self.JOB_TITLE_DROPDOWN)
        self.click(self.JOB_TITLE_OPTION_ANY)

    def save_job(self):
        self.click(self.JOB_SAVE)

    def success_toast_visible(self) -> bool:
        return self.exists(self.TOAST_SUCCESS)
