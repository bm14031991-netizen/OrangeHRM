import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC


def user_end_to_end():
    import config.conf_user as orange_positive
    a = [orange_positive.user1]
    USERNAME = random.choices(a)
    return USERNAME

def user_for_negative():
    import config.conf_user as orange_negative
    a = [orange_negative.user2]
    USERNAME = random.choices(a)
    return USERNAME


def placeholder_input_without_enter(driver, ID, value):
    find_el = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//*[@placeholder="{ID}"]')))
    find_el.clear()
    find_el.send_keys(value)


def onclick_click(driver, onclick):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'''//*[@onclick="{onclick}"]'''))).click()


def login_click(driver, text):
    time.sleep(1)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//button[@type="submit" and text()="{text}"]'))).click()


def param_auth(driver, URL, USERNAME, PASSWORD):
    driver.get(URL)
    placeholder_input_without_enter(driver, "Username", USERNAME)
    placeholder_input_without_enter(driver, "Password", PASSWORD)
