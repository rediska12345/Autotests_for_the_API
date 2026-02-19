import requests
import random
import string
from urls import Urls


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def register_new_user_and_return_data():
    email = f"{generate_random_string(10)}@yandex.ru"
    password = generate_random_string(10)
    name = generate_random_string(10)

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(Urls.REGISTER_USER, json=payload)

    if response.status_code == 200:
        return email, password, name
    else:
        return None