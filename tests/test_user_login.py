import allure
import requests
from urls import Urls
from generators import generate_random_string


class TestUserLogin:

    @allure.title('Вход под существующим пользователем')
    @allure.description('Проверка, что существующий пользователь может войти в систему')
    def test_login_existing_user_success(self, existing_user_data):
        payload = {"email": existing_user_data["email"], "password": existing_user_data["password"]}

        response = requests.post(Urls.LOGIN_USER, json=payload)

        assert response.status_code == 200
        assert response.json().get("success") is True
        assert response.json().get("accessToken") is not None

    @allure.title('Вход с неверным логином и паролем')
    @allure.description('Проверка, что вход с неправильными данными возвращает 401 Unauthorized')
    def test_login_wrong_credentials_failed(self):
        wrong_email = f"{generate_random_string(10)}@yandex.ru"
        wrong_password = generate_random_string(10)
        payload = {"email": wrong_email, "password": wrong_password}

        response = requests.post(Urls.LOGIN_USER, json=payload)

        assert response.status_code == 401
        assert response.json().get("message") == "email or password are incorrect"