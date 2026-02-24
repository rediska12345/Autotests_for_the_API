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
        
        with allure.step('Отправить запрос на создание нового пользователя'):
            response = requests.post(Urls.REGISTER_USER, json=payload)
        
        with allure.step('Проверить, что пользователь успешно создан'):
            assert response.status_code == 200
            response_data = response.json()
            assert "accessToken" in response_data
            assert "refreshToken" in response_data
            assert response_data.get("user").get("email") == email
            assert response_data.get("user").get("name") == name

    @allure.title('Создание пользователя, который уже зарегистрирован')
    @allure.description('Проверка, что при попытке создать существующего пользователя возвращается 403 Forbidden')
    def test_create_existing_user_failed(self, existing_user_data):
        payload = existing_user_data
        
        with allure.step('Отправить запрос на создание уже существующего пользователя'):
            response = requests.post(Urls.REGISTER_USER, json=payload)
        
        with allure.step('Проверить, что сервер возвращает ошибку 403'):
            assert response.status_code == 403
            assert response.json().get("message") == "User already exists"

    @allure.title('Создание пользователя без поля email')
    @allure.description('Проверка, что если не заполнить email, возвращается 403 Forbidden')
    def test_create_user_missing_email_failed(self):
        password = generate_random_string(10)
        name = generate_random_string(10)
        payload = {"password": password, "name": name}
        
        with allure.step('Отправить запрос на создание пользователя без email'):
            response = requests.post(Urls.REGISTER_USER, json=payload)
        
        with allure.step('Проверить, что сервер возвращает ошибку 403'):
            assert response.status_code == 403
            assert response.json().get("message") == "Email, password and name are required fields"

    @allure.title('Создание пользователя без поля password')
    @allure.description('Проверка, что если не заполнить password, возвращается 403 Forbidden')
    def test_create_user_missing_password_failed(self):
        email = f"{generate_random_string(10)}@yandex.ru"
        name = generate_random_string(10)
        payload = {"email": email, "name": name}
        
        with allure.step('Отправить запрос на создание пользователя без password'):
            response = requests.post(Urls.REGISTER_USER, json=payload)
        
        with allure.step('Проверить, что сервер возвращает ошибку 403'):
            assert response.status_code == 403
            assert response.json().get("message") == "Email, password and name are required fields"

    @allure.title('Создание пользователя без поля name')
    @allure.description('Проверка, что если не заполнить name, возвращается 403 Forbidden')
    def test_create_user_missing_name_failed(self):
        email = f"{generate_random_string(10)}@yandex.ru"
        password = generate_random_string(10)
        payload = {"email": email, "password": password}
        
        with allure.step('Отправить запрос на создание пользователя без name'):
            response = requests.post(Urls.REGISTER_USER, json=payload)
        
        with allure.step('Проверить, что сервер возвращает ошибку 403'):
            assert response.status_code == 403
            assert response.json().get("message") == "Email, password and name are required fields"