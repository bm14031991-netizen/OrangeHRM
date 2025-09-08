import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from pages import LoginPage
from start_browser import browser
from config.conf_user import *
from fixtures import LoginFixture as login
import pages.LoginPage as AuthLocator
import psutil
from selenium.common.exceptions import TimeoutException, WebDriverException


# Функция для получения списка текущих процессов Chrome
def get_current_chrome_processes():
    return {proc.pid for proc in psutil.process_iter(['pid', 'name']) if proc.info['name'] == 'chrome.exe' or proc.info['name'] == 'chrome'}

# Функция для завершения всех новых процессов Chrome, которые были запущены после инициализации
def kill_new_chrome_processes(initial_pids):
    current_pids = get_current_chrome_processes()
    new_pids = current_pids - initial_pids
    if new_pids:
        print(f"Killing new Chrome processes: {new_pids}")
    for pid in new_pids:
        try:
            psutil.Process(pid).kill()
        except psutil.NoSuchProcess:
            pass

# Фикстура для настроек Chrome при локальном запуске
@pytest.fixture(scope="session")
def get_chrome_options_local():
    options = ChromeOptions()
    options.add_argument('chrome')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    return options

# Фикстура для настроек Chrome при удалённом запуске
@pytest.fixture(scope="session")
def get_chrome_options_remote():
    options = ChromeOptions()
    options.add_argument('chrome')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", "137.0")
    options.set_capability("selenoid:options", {"enableVNC": True, "enableVideo": False})
    return options

# Фикстура для настроек Firefox при локальном запуске
@pytest.fixture(scope="session")
def get_firefox_options_local():
    options = FirefoxOptions()
    return options

# Добавление аргумента командной строки для выбора браузера
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")

# Унифицированная функция для настройки драйвера с повторной попыткой при TimeoutException
def driver_setup(auth_func, user_func, url, options_local, options_remote, marker_name):
    initial_pids = get_current_chrome_processes()  # Сохранение списка процессов Chrome перед запуском
    USERNAME = user_func()  # Выбор пользователя для авторизации

    # Определение URL для удаленного запуска в зависимости от маркера
    if marker_name in ["EndToEnd", "Negative"]:
        command_executor_url = "http://"
    else:
        command_executor_url = None

    MAX_RETRIES = 2  # Максимальное количество попыток
    attempts = 0

    driver = None  # Локальная переменная для хранения драйвера

    while attempts < MAX_RETRIES:
        try:
            # Создание драйвера в зависимости от выбранного режима (локальный или удалённый)
            if browser == "local":
                options = options_local
                driver = webdriver.Chrome(options=options)
            elif browser == "remote":
                options = options_remote
                driver = webdriver.Remote(
                    options=options,
                    command_executor=command_executor_url
                )


            driver.implicitly_wait(15)  # Установка неявного ожидания
            auth_func(driver, url, USERNAME, PASSWORD)  # Авторизация
            # AuthLocator.continue_in_version_is_out_of_date(driver)  # Ожидание и клик по элементу, если версия браузера устарела
            login.login_click(driver, " Login ")  # Клик по кнопке входа

            print(f"Successfully logged in and changed module (Attempt {attempts + 1}).")
            break  # Если успешный запуск, выходим из цикла

        except (TimeoutException, WebDriverException, Exception) as e:
            attempts += 1
            print(f"Attempt {attempts} failed with {type(e).__name__}: {e}")
            if driver:  # Закрываем драйвер, если он был создан
                driver.quit()
            kill_new_chrome_processes(initial_pids)  # Завершаем новые процессы Chrome
            if attempts == MAX_RETRIES:
                print(f"Max retries reached. Test failed with {type(e).__name__}.")
                raise e  # Пробрасываем исключение, если попытки исчерпаны

    yield driver  # Возвращаем драйвер тесту

    # Завершение работы драйвера после выполнения теста
    if driver:
        try:
            driver.execute_script("return document.readyState")  # Проверка состояния страницы
        except WebDriverException:
            print("Session lost during teardown.")
            pytest.fail("WebDriver session is unavailable. Test needs rerun.")
        finally:
            driver.quit()  # Закрываем драйвер
            kill_new_chrome_processes(initial_pids)  # Завершаем новые процессы Chrome


# Фикстуры, использующие универсальную функцию driver_setup
@pytest.fixture(scope="session")
def create_driver_orange(get_chrome_options_local, get_chrome_options_remote):
    yield from driver_setup(login.param_auth, login.user_end_to_end, BASE_URL, get_chrome_options_local, get_chrome_options_remote, "EndToEnd")


@pytest.fixture(scope="session")
def create_driver_orange_negative(get_chrome_options_local, get_chrome_options_remote):
    yield from driver_setup(login.param_auth, login.user_for_negative, BASE_URL, get_chrome_options_local, get_chrome_options_remote, "Negative")




