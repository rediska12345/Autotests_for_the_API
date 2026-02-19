import allure
import requests
from urls import Urls
from generators import generate_random_string


class TestUserCreation:

    @allure.title('Создание уникального пользователя')
    @allure.description('Проверка, что нового пользователя можно создать и сервер возвращает 200')
    def test_create_unique_user_success(self):
        email = f"{generate_random_string(10)}@yandex.ru"
        password = generate_random_string(10)
        name = generate_random_string(10)
        payload = {"email": email, "password": password, "name": name}

        response = requests.post(Urls.REGISTER_USER, json=payload)

        assert response.status_code == 200 and response.json().get("success") is True

    @allure.title('Создание пользователя, который уже зарегистрирован')
    @allure.description('Проверка, что при попытке создать существующего пользователя возвращается 403 Forbidden')
    def test_create_existing_user_failed(self, existing_user_data):
        payload = existing_user_data

        response = requests.post(Urls.REGISTER_USER, json=payload)

        assert response.status_code == 403
        assert response.json().get("message") == "User already exists"

    @allure.title('Создание пользователя без одного из обязательных полей')
    @allure.description('Проверка, что если не заполнить одно из полей, возвращается 403 Forbidden')
    def test_create_user_missing_field_failed(self):
        email = f"{generate_random_string(10)}@yandex.ru"
        password = generate_random_string(10)
        payload = {"email": email, "password": password}

        response = requests.post(Urls.REGISTER_USER, json=payload)

        assert response.status_code == 403
        assert response.json().get("message") == "Email, password and name are required fields"