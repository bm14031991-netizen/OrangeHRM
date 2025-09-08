from faker import Faker

faker = Faker()

def employee_name():
    first = faker.first_name()
    last = faker.last_name()
    middle = ""  # можно добавить faker.first_name() при необходимости отчества
    full = f"{first} {last}".strip()
    return first, middle, last, full
