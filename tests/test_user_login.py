import allure
import requests
from urls import Urls
from generators import generate_random_string


class TestUserLogin:

    @allure.title('Вход под существующим пользователем')
    @allure.description('Проверка, что существующий пользователь может войти в систему')
    def test_login_existing_user_success(self, existing_user_data):
        payload = {"email": existing_user_data["email"], "password": existing_user_data["password"]}
        
        with allure.step('Отправить запрос на вход с существующим пользователем'):
            response = requests.post(Urls.LOGIN_USER, json=payload)
        
        with allure.step('Проверить, что вход выполнен успешно'):
            assert response.status_code == 200
            response_data = response.json()
            assert "accessToken" in response_data
            assert "refreshToken" in response_data
            assert response_data.get("user").get("email") == existing_user_data["email"]
            assert response_data.get("user").get("name") == existing_user_data["name"]

    @allure.title('Вход с неверным логином и паролем')
    @allure.description('Проверка, что вход с неправильными данными возвращает 401 Unauthorized')
    def test_login_wrong_credentials_failed(self):
        wrong_email = f"{generate_random_string(10)}@yandex.ru"
        wrong_password = generate_random_string(10)
        payload = {"email": wrong_email, "password": wrong_password}
        
        with allure.step('Отправить запрос на вход с неверными учетными данными'):
            response = requests.post(Urls.LOGIN_USER, json=payload)
        
        with allure.step('Проверить, что сервер возвращает ошибку 401'):
            assert response.status_code == 401
            assert response.json().get("message") == "email or password are incorrect"