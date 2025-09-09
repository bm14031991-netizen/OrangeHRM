# OrangeHRM
UiTests

Демо-стенд: https://opensource-demo.orangehrmlive.com/web/index.php/auth/login

## Функционал
- Page Object (Login, Dashboard, PIM, Employee Profile)
- E2E сценарий: логин → создание сотрудника → редактирование профиля → проверка в списке
- Негативные кейсы: неверный логин, Обязательные-поля при создании
- HTML-репорт и скриншоты при падении (`reports/screenshots`)
---

## Подготовка окружения

py -m venv .venv 

.\.venv/bin/activate  

pip install -r requirements.txt

## Запуск тестов

Убедитесь, что у проекта включён pytest

В PyCharm:
File → Settings → Tools → Python Integrated Tools.

В поле Default test runner выберите pytest.
