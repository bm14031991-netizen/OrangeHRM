from datetime import datetime, timedelta
import dateutil.relativedelta
import selenium

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
import time



class BasePage:

    def __init__(self, driver, wait=18):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, wait)
        self.actions = ActionChains(driver)
        # self.session_id = driver.session_id

    def _open(self, url):
        self.driver.get(url)

    def find_element(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))

    def find_element_display(self, locator):
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(locator))

    def find_wait_element(self, locator):
        time.sleep(1)
        self.wait.until(EC.visibility_of_element_located(locator))

    def id_find_element(self, ID):
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))

    def name_find_element(self, name):
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@name="{name}"]')))

    def onclick_find_element(self, name):
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@onclick="{name}"]')))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def click_script(self, locator):
        find_el = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", find_el)

    def script_class_display_none_poly(self):
        self.driver.execute_script(f'document.getElementsByClassName("loading-modal")[0].style.display="none"')

    def script_class_display_none(self):
        find_el = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(((By.XPATH, '//*[@class="loading-modal"]'))))
        find_el.value_of_css_property('display: none;')

    def click_wait_script(self, locator):
        find_el = self.wait.until(EC.element_to_be_clickable(locator))
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", find_el)

    def display_none(self):
        # Ждём до 10 секунд или до тех пор, пока элемент не исчезнет, Если элемент исчезнет раньше, то выполнение кода продолжится немедленно
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="pre-loader" and @style="display: block;"]')))


    def click_wait(self, locator):
        time.sleep(1)
        self.wait.until(EC.visibility_of_all_elements_located(locator))
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def click_wait_list_with_scroll(self, locator):
        time.sleep(1)

        # Находим элемент, который должен быть кликабельным
        element = self.wait.until(EC.element_to_be_clickable(locator))

        try:
            # Прокручиваем страницу до элемента с использованием JavaScript
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

            # После прокрутки выполняем обычный клик
            element.click()

        except selenium.common.exceptions.ElementClickInterceptedException:
            # Если элемент перекрыт, выполняем клик с помощью JavaScript
            self.driver.execute_script("arguments[0].click();", element)

    def click_wait_some(self, locator):
        time.sleep(5)
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(locator)).click()

    def id_wait_text_el(self, ID):
        time.sleep(4)
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]//*'))).click()

    def switch_to_frame_base(self):
        self.switch_iframe((By.TAG_NAME, 'iframe'))


    def is_elem_displayed(self, webelement):
        try:
            return webelement.is_displayed()
        except StaleElementReferenceException:
            return False
        except NoSuchElementException:
            return False
        except ElementClickInterceptedException:
            return False

    def _highlight_element(self, webelement, color):
        original_style = webelement.get_attribute("style")
        new_style = "background-color:yellow;border: 1px solid " + color + original_style
        self.driver.execute_script(
            "var tmpArguments = arguments;setTimeout(function () {tmpArguments[0].setAttribute('style', '"
            + new_style + "');},0);", webelement)
        self.driver.execute_script(
            "var tmpArguments = arguments;setTimeout(function () {tmpArguments[0].setAttribute('style', '"
            + original_style + "');},500);", webelement)

    def click_and_enter(self, locator):
        find_el = self.wait.until(EC.element_to_be_clickable(locator)).click()
        find_el.send_keys(Keys.ENTER)

    def clear(self, locator):
        self.wait.until(EC.presence_of_element_located(locator)).clear()

    def clear_wait(self, locator):
        time.sleep(1)
        self.wait.until(EC.presence_of_element_located(locator)).clear()

    def clear_and_enter(self, locator):
        find_el = self.wait.until(EC.presence_of_element_located(locator)).clear()
        find_el.send_keys(Keys.ENTER)

    def clear_and_enter_wait(self, locator):
        time.sleep(1)
        find_el = self.wait.until(EC.presence_of_element_located(locator)).clear()
        find_el.send_keys(Keys.ENTER)

    def for_wait_click(self, For):
        time.sleep(4)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@for="{For}"]'))).click()

    def for_click(self, For):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@for="{For}"]'))).click()

    def input(self, locator, value):
        find_el = self.wait.until(EC.presence_of_element_located(locator))
        find_el.clear()
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)

    def Input_with_verification(self, locator, value):
        find_el = self.wait.until(EC.presence_of_element_located(locator))
        find_el.clear()
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)
            # Проверка введенного значения
        entered_value = find_el.get_attribute("value")
        assert entered_value == value, f"Введенное значение ({entered_value}) не соответствует ожидаемому ({value})"


    def input_test(self, locator, value):
        find_el = self.wait.until(EC.presence_of_element_located(locator))
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)

    def input_wait(self, locator, value):
        time.sleep(1)
        find_el = self.wait.until(EC.presence_of_element_located(locator))
        find_el.clear()
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)

    def input_without_clear(self, locator, value):
        find_el = self.wait.until(EC.presence_of_element_located(locator))
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)

    def input_without_enter(self, locator, value):
        find_el = self.wait.until(EC.presence_of_element_located(locator))
        find_el.clear()
        find_el.send_keys(value)


    def input_without_clear_and_enter(self, locator, value):
        find_el = self.wait.until(EC.presence_of_element_located(locator))
        find_el.send_keys(value)

    def input_wait_listbox(self, locator, value):
        find_el = self.wait.until(EC.presence_of_element_located(locator))
        find_el.clear()
        find_el.send_keys(value)
        time.sleep(1)
        find_el.send_keys(Keys.ENTER)

    def input_wait_listbox_2(self, locator, value):
        find_el = self.wait.until(EC.presence_of_element_located(locator))
        find_el.clear()
        find_el.send_keys(value)
        time.sleep(3)
        find_el.send_keys(Keys.ENTER)

    def input_wait_listbox_and_without_clear(self, locator, value):
        find_el = self.wait.until(EC.presence_of_element_located(locator))
        find_el.send_keys(value)
        time.sleep(1)
        find_el.send_keys(Keys.ENTER)

    def input_double_enter(self, locator, value):
        find_el = self.wait.until(EC.presence_of_element_located(locator))
        find_el.clear()
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)
        time.sleep(1)
        find_el.send_keys(Keys.ENTER)

    def input_and_submit(self, locator, value):
        find_field = self.wait.until(EC.presence_of_element_located(locator))
        find_field.click()
        find_field.clear()
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)

    def delete_and_input(self, locator, value):
        find_field = self.wait.until(EC.element_to_be_clickable(locator))
        find_field.click()
        find_field.send_keys(Keys.CONTROL + "a")
        find_field.send_keys(Keys.DELETE)
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)

    def click_and_input(self, locator, value):
        find_el = self.driver.find_element(*locator)
        find_el.click()
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)

    def switch_iframe(self, locator):
        self.driver.switch_to.frame(self.driver.find_element(*locator))

    def alert_accept(self):
        self.driver.switch_to.alert.accept()

    def alert_dismiss(self):
        self.driver.switch_to.alert.dismiss()

    def switch_back_iframe(self):
        self.driver.switch_to.default_content()

    def script(self, locator):
        self.driver.execute_script(locator)

    def script_input_value(self, ID, value):
        self.driver.execute_script(f'document.getElementById("{ID}").value = "{value}"')

    def script_name_input_value(self, name, value):
        self.driver.execute_script(f'document.getElementsByName("{name}")[0].value = "{value}"')

    def script_name_input_value_kendo(self, name, value):
        self.driver.execute_script(f"""
            var input = document.getElementsByName("{name}")[0];
            var widget = $(input).data("kendoNumericTextBox");
            if (widget) {{
                widget.value({value});
                widget.trigger("change");
            }} else {{
                input.value = "{value}";
            }}
        """)

    def script_unblock_and_input(self, ID, value):
        self.driver.execute_script(f'document.getElementById("{ID}").style.display="block"')
        find_field = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_field.click()
        find_field.clear()
        self.driver.execute_script(f'document.getElementById("{ID}").style.display="block"')
        find_field = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_field.send_keys(value)
        # find_field.send_keys(Keys.ENTER)

    def script_unblock_and_input_enter(self, ID, value):
        self.driver.execute_script(f'document.getElementById("{ID}").style.display="block"')
        self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_field = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_field.click()
        find_field.clear()
        self.driver.execute_script(f'document.getElementById("{ID}").style.display="block"')
        find_field = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)


    def script_wait_unblock_and_input_enter(self, ID, value):
        time.sleep(1)
        self.driver.execute_script(f'document.getElementById("{ID}").style.display="block"')
        self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_field = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_field.click()
        find_field.clear()
        self.driver.execute_script(f'document.getElementById("{ID}").style.display="block"')
        find_field = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)

    def script_input_value_click_enter(self, ID, value):
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_el.click()
        self.driver.execute_script(f'document.getElementById("{ID}").value = "{value}"')
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_el.send_keys(Keys.ENTER)

    def script_wait_input_value_click_enter(self, ID, value):
        time.sleep(1)
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_el.click()
        self.driver.execute_script(f'document.getElementById("{ID}").value = "{value}"')
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_el.send_keys(Keys.ENTER)

    def script_input_value_click_without_enter(self, ID, value):
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_el.click()
        self.driver.execute_script(f'document.getElementById("{ID}").value = "{value}"')
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))

    def script_name_input_value_click_enter(self, name, value):
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@name="{name}"]')))
        find_el.click()
        self.driver.execute_script(f'document.getElementsByName("{name}")[0].value = "{value}"')
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@name="{name}"]')))
        find_el.send_keys(Keys.ENTER)

    def script_input_value_enter(self, ID, value):
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        self.driver.execute_script(f'document.getElementById("{ID}").value = "{value}"')
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_el.send_keys(Keys.ENTER)

    def script_input_value_click(self, ID, value):
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_el.click()
        self.driver.execute_script(f'document.getElementById("{ID}").value = "{value}"')


    def script_with_clear(self, locator, locator2):
        time.sleep(1)
        self.driver.execute_script(locator)
        self.wait.until(EC.presence_of_element_located(locator2)).clear()
        self.driver.execute_script(locator)

    def id_wait_input(self, ID, value):
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_el.clear()
        find_el.send_keys(Keys.HOME)
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)

    def id_input(self, ID, value):
        self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_el.clear()
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)

    def id_input_without_enter(self, ID, value):
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_el.clear()
        find_el.send_keys(value)

    def id_input_and_submit_without_enter(self, ID, value):
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_el.click()
        find_el.clear()
        find_el.send_keys(value)

    def id_input_and_submit(self, ID, value):
        find_field = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        find_field.click()
        find_field.clear()
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)

    def id_clear(self, ID):
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]'))).clear()

    def id_contains_input_and_submit(self, ID, value):
        find_field = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[contains(@id,"{ID}")]')))
        find_field.click()
        find_field.clear()
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)

    def id_and_id_click(self, ID, ID2):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{ID}"]//*[@id="{ID2}"]'))).click()

    def id_and_id_wait_click(self, ID, ID2):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{ID}"]//*[@id="{ID2}"]'))).click()

    def id_id_input(self, ID, ID2, value):
        find_el = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{ID}"]//*[@id="{ID2}"]')))
        find_el.clear()
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)

    def id_id_wait_input(self, ID, ID2, value):
        time.sleep(1)
        find_el = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{ID}"]//*[@id="{ID2}"]')))
        find_el.clear()
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)

    def id_click(self, ID):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{ID}"]'))).click()

    def id_click_enter(self, ID):
        find_el = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{ID}"]'))).click()
        find_el.send_keys(Keys.ENTER)

    def id_wait_click(self, ID):
        time.sleep(3)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{ID}"]'))).click()

    def id_wait_listbox_click(self, ID, text):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[@id="{ID}"]//li[text()='{text}']'''))).click()

    def contains_id_wait_listbox_click(self, ID, text):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[contains(@id, "{ID}")]//li[text()='{text}']'''))).click()


    def class_wait_listbox_click(self, CLASS, text):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[contains(@class, "{CLASS}")]//*[text()='{text}']'''))).click()

    def id_wait_text_click(self, ID, text):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[@id="{ID}"]//*[text()='{text}']'''))).click()

    def id_contains_text_click(self, ID, text):
        self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, f'''//*[@id="{ID}"]//*[contains(text(),'{text}')]''')))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[@id="{ID}"]//*[contains(text(),'{text}')]'''))).click()

    def id_wait_contains_text_click(self, ID, text):
        time.sleep(1)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'''//*[@id="{ID}"]//*[contains(text(),'{text}')]'''))).click()

    def class_waiting_for_loading_person(self, CLASS):
        time.sleep(1)
        self.wait.until(EC.invisibility_of_element_located((By.XPATH,f'//div[@class="{CLASS}"]')))

    def id_wait_contains_text_click_with_scroll(self, ID, text):
        time.sleep(1)
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'''//*[@id="{ID}"]//*[contains(text(),'{text}')]''')))

        # Прокрутка до элемента с использованием JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

        # После прокрутки выполняем клик
        element.click()

    def href_wait_contains_text_click_with_scroll(self, href, text):
        time.sleep(1)
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'''//*[contains(@href,"{href}") and contains(text(),"{text}")]''')))

        # Прокрутка до элемента с использованием JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

        # После прокрутки выполняем клик
        element.click()

    def scroll_to_element(self, href, text):
        time.sleep(1)
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'''//*[contains(@href,"{href}") and contains(text(),"{text}")]''')))

        # Прокрутка до элемента с использованием JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

        # После прокрутки выполняем клик
        element.click()

    def id_wait_title_click(self, ID, text):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[@id="{ID}"]//*[@title='{text}']'''))).click()

    def id_wait_contains_listbox_click(self, ID, text):
        time.sleep(2)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'''//*[@id="{ID}"]//li[contains(text(),'{text}')]'''))).click()

    def id_wait_contains_span_click(self, ID, text):
        time.sleep(2)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'''//*[@id="{ID}"]//span[contains(text(),'{text}')]'''))).click()


    def id_wait_contains_listbox_select_desired_and_click(self, ID, executors_list):
        if isinstance(executors_list, str):
            executors_list = [executors_list]
        print(f"Получен executors_list: {executors_list}")
        time.sleep(2)
        xpath = f'''//*[@id="{ID}"]//li'''
        elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        for executor in executors_list:
            for element in elements:
                try:
                    if executor in element.text:
                        executor_xpath = f'{xpath}[contains(text(), \'{executor}\')]'
                        self.wait.until(EC.element_to_be_clickable((By.XPATH, executor_xpath))).click()
                        print(f"Значение '{executor}' найдено и кликнуто")
                        return
                except Exception as e:
                    print(f"Ошибка при клике на '{executor}': {e}")
        print(f"Ни одно значение из {executors_list} не найдено")

    def id_contains_wait_contains_listbox_click(self, ID, text):
        time.sleep(2)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'''//*[contains(@id,"{ID}")]//li[contains(text(),'{text}')]'''))).click()

    def v_id_wait_contains_listbox_click(self, ID, text):
        time.sleep(2)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'''//*[@id="{ID}"]//li[contains(text(),'{text}') and @class="k-item k-state-focused"]'''))).click()

    def id_contains_onclick_click(self, ID, onclick):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="{ID}"]//*[contains(@onclick,"{onclick}")]'))).click()

    def contains_onclick_click(self, onclick, FIO):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[contains(@onclick,"{onclick}")]//*[contains(text(),"{FIO}")]'))).click()

    def id_contains_onclick_script_click(self, ID, onclick):
        find_el = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="{ID}"]//*[contains(@onclick,"{onclick}")]')))
        self.driver.execute_script("arguments[0].click();", find_el)

    def id_wait_contains_onclick_click(self, ID, onclick):
        time.sleep(1)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="{ID}"]//*[contains(@onclick,"{onclick}")]'))).click()

    def id_href_click(self, ID, href):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{ID}"]//*[@href="{href}"]'))).click()

    def id_wait_href_click(self, ID, href):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{ID}"]//*[@href="{href}"]'))).click()

    def id_contains_id_and_listbox_click(self, ID, ID2, text):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//*[@id="{ID}"]//*[contains(@id,"{ID2}") and text()="{text}"]'))).click()

    def id_wait_contains_id_and_listbox_click(self, ID, ID2, text):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//*[@id="{ID}"]//*[contains(@id,"{ID2}") and text()="{text}"]'))).click()

    def id_qtip_click(self, ID, qtip):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{ID}"]//*[@data-qtip="{qtip}"]'))).click()

    def id_wait_qtip_click(self, ID, qtip):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{ID}"]//*[@data-qtip="{qtip}"]'))).click()

    def name_input(self, name, value):
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@name="{name}"]')))
        find_el.clear()
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)

    def name_wait_input(self, name, value):
        time.sleep(1)
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@name="{name}"]')))
        find_el.clear()
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)

    def name_input_and_submit(self, name, value):
        find_field = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@name="{name}"]')))
        find_field.click()
        find_field.clear()
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)

    def name_input_without_enter(self, name, value):
        find_field = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@name="{name}"]')))
        find_field.click()
        find_field.clear()
        find_field.send_keys(value)

    def name_wait_input_without_enter(self, name, value):
        time.sleep(1)
        find_field = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@name="{name}"]')))
        find_field.click()
        find_field.clear()
        find_field.send_keys(value)

    def name_input_without_clear(self, name, value):
        find_field = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@name="{name}"]')))
        find_field.click()
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)

    def name_clear(self, name):
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@name="{name}"]'))).clear()

    def name_wait_clear(self, name):
        time.sleep(1)
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@name="{name}"]'))).clear()

    def name_click(self, name):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@name="{name}"]'))).click()

    def name_wait_click(self, name):
        time.sleep(3)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@name="{name}"]'))).click()

    def contains_text_click(self, text):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[contains(text(),"{text}")]'))).click()

    def contains_id_click(self, ID):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[contains(@id,"{ID}")]'))).click()

    def contains_wait_id_click(self, ID):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[contains(@id,"{ID}")]'))).click()

    def contains_id_contains_onclick(self, ID, onclick):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//*[contains(@id,"{ID}")]//*[contains(@onclick,"{onclick}")]'))).click()

    def contains_wait_id_contains_onclick(self, ID, onclick):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//*[contains(@id,"{ID}")]//*[contains(@onclick,"{onclick}")]'))).click()

    def contains_id_and_text_click(self, ID, text):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[contains(@id,"{ID}") and contains(text(),"{text}")]'))).click()

    def contains_wait_id_and_text_click(self, ID, text):
        time.sleep(1)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[contains(@id,"{ID}") and contains(text(),"{text}")][last()]'))).click()

    def contains_id_text(self, ID, text):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[contains(@id,"{ID}")]//*[text()="{text}"]'))).click()

    def contains_wait_id_text(self, ID, text):
        time.sleep(1)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[contains(@id,"{ID}")]//*[text()="{text}"]'))).click()

    def contains_id_contains_text(self, ID, text):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[contains(@id,"{ID}")]//*[contains(text(),"{text}")]'))).click()

    def contains_id_input_text(self, ID, value):
        find_field = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[contains(@id,"{ID}")]')))
        find_field.click()
        find_field.clear()
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)

    def contains_class_input_value(self, CLASS, value):
        find_field = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[contains(@class,"{CLASS}")]'))).click()
        find_field.click()
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)

    def contains_class_input_text(self, CLASS, text, value):
        find_field = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[contains(@class,"{CLASS}")]//*[@placeholder="{text}"]')))
        find_field.click()
        find_field.clear()
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)


    def contains_wait_id_contains_text(self, ID, text):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[contains(@id,"{ID}")]//*[contains(text(),"{text}")]'''))).click()

    def contains_id_and_qtip_click(self, ID, qtip):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[contains(@id,"{ID}") and @data-qtip="{qtip}"]'))).click()

    def contains_wait_id_and_qtip_click(self, ID, qtip):
        time.sleep(1)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[contains(@id,"{ID}") and @data-qtip="{qtip}"]'))).click()

    def contains_href_and_contains_text(self, href, text):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//*[contains(@href,"{href}") and contains(text(),"{text}")]'))).click()

    def contains_class_click(self, name):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[contains(@class,"{name}")]'))).click()

    def contains_wait_class_click(self, name):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[contains(@class,"{name}")]'))).click()

    def contains_wait_href_and_contains_text(self, href, text):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//*[contains(@href,"{href}") and contains(text(),"{text}")]'))).click()

    def aria_controls_click(self, name):
        self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, f'//*[@aria-controls="{name}"]')))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@aria-controls="{name}"]'))).click()

    def aria_controls_wait_click(self, name):
        time.sleep(6)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@aria-controls="{name}"]'))).click()

    def aria_controls_contains_wait_click(self, name):
        time.sleep(6)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[contains(@aria-controls, "{name}")]'))).click()

    def aria_controls_wait_click_enter(self, name):
        time.sleep(1)
        find_el = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@aria-controls="{name}"]')))
        find_el.click()
        find_el.send_keys(Keys.ENTER)

    def aria_controls_listbox_click(self, name, text):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@aria-controls="{name}"]//*[text()="{text}"]'))).click()

    def aria_controls_listbox_wait_click(self, name, text):
        time.sleep(1)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@aria-controls="{name}"]//*[text()="{text}"]'))).click()

    def contains_id_contains_href_click(self, ID, href):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[contains(@id,"{ID})"]//*[contains(@href,"{href}")]'))).click()

    def contains_wait_id_contains_href_click(self, ID, href):
        time.sleep(1)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[contains(@id,"{ID}")]//*[contains(@href,"{href}")]'))).click()

    def aria_controls_input(self, name, value):
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@aria-controls="{name}"]')))
        find_el.clear()
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)

    def aria_controls_wait_input(self, name, value):
        time.sleep(1)
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@aria-controls="{name}"]')))
        find_el.clear()
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)

    def aria_owns_input(self, name, value):
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@aria-owns="{name}"]')))
        find_el.clear()
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)
        find_el.send_keys(Keys.ENTER)

    def aria_owns_wait_input(self, name, value):
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@aria-owns="{name}"]')))
        find_el.clear()
        find_el.send_keys(value)
        time.sleep(1)
        find_el.send_keys(Keys.ENTER)

    def aria_owns_wait_input_without_enter(self, name, value):
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@aria-owns="{name}"]')))
        find_el.clear()
        find_el.send_keys(value)

    def aria_owns_click(self, name):
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@aria-owns="{name}"]'))).click()

    def aria_owns_wait_click(self, name):
        time.sleep(1)
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@aria-owns="{name}"]'))).click()

    def Medical_History_Search_Setting(self, name, text):
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, f'//*[@class="{name}"]//*[text()="{text}"]'))).click()

    def Search_button_clikc(self,name,text):
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@type="{name}"]//*[@class="{text}"]'))).click()

    def contains_aria_owns_click(self, name):
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[contains(@aria-owns,"{name}")]'))).click()

    def contains_aria_owns_wait_click(self, name):
        time.sleep(1)
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[contains(@aria-owns,"{name}")]'))).click()

    def aria_owns_listbox_click(self, name, text):
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, f'//*[@aria-owns="{name}"]//*[text()="{text}"]'))).click()

    def aria_owns_wait_listbox_click(self, name, text):
        time.sleep(1)
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, f'//*[@aria-owns="{name}"]//*[text()="{text}"]'))).click()

    def onclick_input(self, onclick, value):
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@onclick="{onclick}"]')))
        find_el.clear()
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)

    def onclick_wait_input(self, onclick, value):
        time.sleep(1)
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@onclick="{onclick}"]')))
        find_el.clear()
        find_el.send_keys(value)
        find_el.send_keys(Keys.ENTER)

    def onclick_input_without_enter(self, onclick, value):
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@onclick="{onclick}"]')))
        find_el.clear()
        find_el.send_keys(value)

    def onclick_input_and_submit(self, onclick, value):
        find_field = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@onclick="{onclick}"]')))
        find_field.click()
        find_field.clear()
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)

    def onclick_click(self, onclick):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[@onclick="{onclick}"]'''))).click()
        # self.driver.execute_script('arguments[0].click()', find_el)

    def onclick_contains_click(self, onclick):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[contains(@onclick,"{onclick}")]'''))).click()

    def onclick_wait_click(self, onclick):
        time.sleep(2)
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'''//*[@onclick="{onclick}"]'''))).click()

    def onclick_wait_contains_click(self, onclick):
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[contains(@onclick,"{onclick}")]'''))).click()

    def class_and_text_click(self, class_name, text):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'''//*[@class="{class_name}" and text()="{text}"]'''))).click()

    def class_contains_text_click(self, class_name, text):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'''//*[@class="{class_name}"]"//*[contains(text(),"{text}")]'''))).click()

    def class_contains_text(self, class_name, text):
        return self.wait.until(EC.presence_of_element_located(
            (By.XPATH, f'//*[@class="{class_name}"]//*[contains(text(),"{text}")]')))

    def class_wait_contains_text_click(self, class_name, text):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'''//*[@class="{class_name}"]//*[contains(text(),"{text}")]'''))).click()

    def class_and_text_wait_click(self, class_name, text):
        time.sleep(1)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'''//*[@class="{class_name}" and text()="{text}"]'''))).click()

    def class_text_click(self, class_name, text):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'''//*[@class="{class_name}"//*[text()="{text}"]'''))).click()

    def class_wait_text_click(self, class_name, text):
        time.sleep(1)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'''//*[@class="{class_name}"]//*[text()="{text}"]'''))).click()

    def tag_click(self, tag):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[@tag="{tag}"]'''))).click()

    def tag_wait_click(self, tag):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[@tag="{tag}"]'''))).click()

    def href_click(self, href):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[@href="{href}"]'''))).click()

    def href_wait_click(self, href):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[@href="{href}"]'''))).click()

    def contains_href_click(self, href):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[contains(@href,"{href}")]'''))).click()

    def contains_wait_href_click(self, href):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[contains(@href,"{href}")]'''))).click()

    def contains_aria_controls_click(self, aria_controls):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'''//*[contains(@aria-controls,"{aria_controls}")]'''))).click()

    def contains_aria_controls_wait_click(self, aria_controls):
        time.sleep(1)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'''//*[contains(@aria-controls,"{aria_controls}")]'''))).click()

    def contains_aria_controls_contains_text_click(self, aria_controls, text):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'''//*[contains(@aria-controls,"{aria_controls}")]//*[contains(text(),"{text}")]'''))).click()

    def contains_aria_controls_contains_text_wait_click(self, aria_controls, text):
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'''//*[contains(@aria-controls,"{aria_controls}")]//*[contains(text(),"{text}")]'''))).click()

    def placeholder_input_input_without_clear(self, placeholder, value):
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@placeholder="{placeholder}"]')))
        find_el.clear()
        find_el.send_keys(value)

    def placeholder_wait_input_without_clear(self, placeholder, value):
        time.sleep(1)
        find_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@placeholder="{placeholder}"]')))
        find_el.send_keys(value)


    def switch_to_windows(self, number):
        self.driver.switch_to.window(self.driver.window_handles[number])

    def switch_to_windows2(self, number):
        try:
            self.driver.switch_to.window(self.driver.window_handles[number])
            return True
        except TimeoutException:
            return False

    def switch_to_windows_new(self, number):
        self.wait.until(EC.new_window_is_opened(self.driver.window_handles))
        self.driver.switch_to.window(self.driver.window_handles[number])


    def is_present(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))


    def datetime_now(self):
        now = datetime.now()
        dt_string = now.strftime("%d.%m.%Y %H:%M")
        return dt_string
        # a = now + timedelta(hours=-1)
        # dt_string = a.strftime("%d.%m.%Y %H:%M")
        # return dt_string

    def time_now(self):
        now = datetime.now()
        # a = now + timedelta(hours=-1)
        t_string = now.strftime("%H:%M")
        return t_string

    "<--------------------------------->"
    def datetime_today(self):
        now = datetime.now()
        dt_string = now.strftime("%d.%m.%Y")
        return dt_string

    def daytime_ago(self):
        now = datetime.now()
        a = now + timedelta(days=-1)
        dt_string = a.strftime("%d.%m.%Y %H:%M")
        return dt_string

    def day1_ago(self):
        now = datetime.now()
        a = now + timedelta(days=-1)
        dt_string = a.strftime("%d.%m.%Y")
        return dt_string

    def two_day_ago(self):
        now = datetime.now()
        a = now + timedelta(days=-2)
        dt_string = a.strftime("%d.%m.%Y")
        return dt_string

    def three_day_ago(self):
        now = datetime.now()
        a = now + timedelta(days=-3)
        dt_string = a.strftime("%d.%m.%Y")
        return dt_string

    def three_day_forward(self):
        now = datetime.now()
        a = now + timedelta(days=+3)
        dt_string = a.strftime("%d.%m.%Y")
        return dt_string

    def four_day_forward(self):
        now = datetime.now()
        a = now + timedelta(days=+4)
        dt_string = a.strftime("%d.%m.%Y")
        return dt_string

    def now_time_plus_one_hour(self):
        now = datetime.now()
        a = now + timedelta(hours=+1)
        dt_string = a.strftime("%d.%m.%Y %H:%M")
        return dt_string

    def now_time_minus_one_hour(self):
        now = datetime.now()
        a = now + timedelta(hours=-1)
        dt_string = a.strftime("%d.%m.%Y %H:%M")
        return dt_string

    def secondhours(self):
        now = datetime.now()
        dt_string = now.strftime("%d.%m.%Y %H:%M")
        return dt_string

    def time_oclock_or_half(self):
        now = datetime.now()
        dt_string = now.strftime("%H:%M")
        if now.strftime("%H:00") <= dt_string < now.strftime("%H:29"):
            a = now.strftime("%H:30")
            return a
        else:
            a = now.strftime("%H:00")
            return a

    def time_quarter_or_half(self):
        now = datetime.now()
        dt_string = now.strftime("%H:%M")
        if dt_string < now.strftime("%H:15"):
            a = now.strftime("%H:00 - %H:15")
            return a
        elif now.strftime("%H:15") <= dt_string < now.strftime("%H:30"):
            a = now.strftime("%H:15 - %H:30")
            return a
        elif now.strftime("%H:30") <= dt_string < now.strftime("%H:45"):
            a = now.strftime("%H:30 - %H:45")
            return a
        else:
            a = now.strftime("%H:45")
            return a

    def time_quarter_or_half_after_30minutes(self):
        now = datetime.now()
        a = now + dateutil.relativedelta.relativedelta(minutes=30)
        dt_string = a.strftime("%H:%M")
        if dt_string < now.strftime("%H:15"):
            a = now.strftime("%H:00 - %H:15")
            return a
        elif now.strftime("%H:15") < dt_string < now.strftime("%H:30"):
            a = now.strftime("%H:15 - %H:30")
            return a
        elif now.strftime("%H:30") < dt_string < now.strftime("%H:45"):
            a = now.strftime("%H:30 - %H:45")
            return a
        else:
            a = now.strftime("%H:45")
            return a


    def assert_element(self, locator):
        try:
            self.wait.until(EC.presence_of_element_located(locator))
        except (TimeoutException):
            return False
        return True

    def assert_id_element(self, ID):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{ID}"]')))
        except (TimeoutException):
            return False
        return True


    def date_now(self):
        now = datetime.now()
        dt_string = now.strftime("%d.%m.%Y")
        return dt_string

    def date_now2(self):
        now = datetime.now()
        dt_string = now.strftime("%Y/%m/%d")
        return dt_string

    def date_now_without_zero(self):
        now = datetime.now()
        dt_string = now.strftime("%#d.%m.%Y")
        return dt_string

    def year_only(self):
        now = datetime.now()
        dt_string = now.strftime("%Y")
        return dt_string

    def datemonth_only(self):
        now = datetime.now()
        dt_string = now.strftime("%d.%m")
        return dt_string

    def date_only(self):
        now = datetime.now()
        dt_string = now.strftime("%d")
        return dt_string

    def date_only_without_zero(self):
        now = datetime.now()
        dt_string = now.strftime("%#d")
        return dt_string

    def date_after(self):
        now = datetime.now()
        a = now + dateutil.relativedelta.relativedelta(days=1)
        dt_string = a.strftime("%d.%m.%Y")
        return dt_string

    def day_after2(self):
        now = datetime.now()
        a = now + dateutil.relativedelta.relativedelta(days=2)
        dt_string = a.strftime("%d")
        return dt_string

    def date_after3(self):
        now = datetime.now()
        a = now + dateutil.relativedelta.relativedelta(days=3)
        dt_string = a.strftime("%d.%m.%Y")
        return dt_string

    def date_after7(self):
        now = datetime.now()
        a = now + dateutil.relativedelta.relativedelta(days=7)
        dt_string = a.strftime("%d.%m.%Y")
        return dt_string

    def date_after8(self):
        now = datetime.now()
        a = now + dateutil.relativedelta.relativedelta(days=7)
        dt_string = a.strftime("%d.%m.%Y")
        return dt_string

    def day_after1(self):
        now = datetime.now()
        a = now + dateutil.relativedelta.relativedelta(days=1)
        dt_string = a.strftime("%d")
        return dt_string

    def date_after2_without_zero(self):
        now = datetime.now()
        a = now + dateutil.relativedelta.relativedelta(days=2)
        dt_string = a.strftime("%#d")
        return dt_string

    def month_ago(self):
        now = datetime.now()
        a = now + dateutil.relativedelta.relativedelta(months=-1)
        dt_string = a.strftime("%d.%m.%Y")
        return dt_string

    def years_ago(self):
        now = datetime.now()
        a = now + dateutil.relativedelta.relativedelta(years=-1)
        dt_string = a.strftime("%d.%m.%Y")
        return dt_string

    def after_month(self):
        now = datetime.now()
        a = now + dateutil.relativedelta.relativedelta(months=1)
        dt_string = a.strftime("%d.%m.%Y")
        return dt_string

    def after_month_without_zero(self):
        now = datetime.now()
        a = now + dateutil.relativedelta.relativedelta(months=1)
        dt_string = a.strftime("%#d.%m.%Y")
        return dt_string

    def day_ago(self):
        now = datetime.now()
        a = now + timedelta(days=-1)
        dt_string = a.strftime("%d.%m.%Y")
        return dt_string

    def day42_ago(self):
        now = datetime.now()
        a = now + timedelta(days=-42)
        dt_string = a.strftime("%d.%m.%Y")
        return dt_string

    def time_exactly_now(self):
        now = datetime.now()
        t_string = now.strftime("%H:00")
        return t_string

    def time_1hours_ago(self):
        now = datetime.now()
        a = now + timedelta(hours=-1)
        t_string = a.strftime("%H:00:00")
        return t_string

    def datehours_now(self):
        now = datetime.now()
        dt_string = now.strftime("%d.%m.%Y")
        return dt_string

    def first_day(self):
        now = datetime.now()
        dt_string = now.strftime("01.%m.%Y")
        return dt_string

    def first_day_last_month(self):
        now = datetime.now()
        month = now.strftime("%#m")
        m = int(month) - 1
        a = now.strftime(f"%Y/{m}/1")
        return a

    def first_day_year(self):
        now = datetime.now()
        dt_string = now.strftime("01.01.%Y")
        return dt_string

    def begin_of_the_year(self):
        # Возвращает строку с датой 1 января текущего года
        return datetime(datetime.now().year, 1, 1).strftime("%d.%m.%Y")

    def year_18ago(self):
        now = datetime.now()
        a = now + dateutil.relativedelta.relativedelta(years=-18)
        dt_string = a.strftime("01.01.%Y")
        return dt_string

    def year_19ago(self):
        now = datetime.now()
        a = now + dateutil.relativedelta.relativedelta(years=-19)
        dt_string = a.strftime("01.01.%Y")
        return dt_string

    def year_17ago(self):
        now = datetime.now()
        a = now + dateutil.relativedelta.relativedelta(years=-17)
        dt_string = a.strftime("01.01.%Y")
        return dt_string

    def wait_until_element_to_be_clickable(self, locator):
        # Ожидание, пока элемент станет кликабельным
        try:
            # Ожидаем, что кнопка станет кликабельной
            clickable_element = WebDriverWait(self, 60).until(
                EC.element_to_be_clickable(locator)
            )

            # Дальнейшие действия с элементом (клик)
            clickable_element.click()
        except Exception as e:
            # Если произошла ошибка при ожидании, выводим сообщение об ошибке
            print("Ошибка при ожидании кликабельности элемента:", e)

    def send_keys_escape(self):
        self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)

    def refresh_page(self):
        self.driver.refresh()

