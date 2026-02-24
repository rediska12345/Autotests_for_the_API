import allure
import requests
from urls import Urls


class TestOrderCreation:

    @allure.title('Создание заказа с авторизацией')
    @allure.description('Проверка, что авторизованный пользователь может создать заказ')
    def test_create_order_with_auth_success(self, user_data, ingredient_hashes):
        _, _, _, access_token = user_data
        headers = {"Authorization": access_token}
        payload = {"ingredients": ingredient_hashes[:2]}
        
        with allure.step('Отправить запрос на создание заказа с авторизацией'):
            response = requests.post(Urls.ORDERS, json=payload, headers=headers)
        
        with allure.step('Проверить, что заказ успешно создан'):
            assert response.status_code == 200
            assert response.json().get("success") is True
            assert response.json().get("order").get("number") is not None

    @allure.title('Создание заказа без авторизации')
    @allure.description('Проверка, что неавторизованный пользователь может создать заказ')
    def test_create_order_without_auth_success(self, ingredient_hashes):
        payload = {"ingredients": ingredient_hashes[:2]}
        
        with allure.step('Отправить запрос на создание заказа без авторизации'):
            response = requests.post(Urls.ORDERS, json=payload)
        
        with allure.step('Проверить, что заказ успешно создан'):
            assert response.status_code == 200
            assert response.json().get("success") is True
            assert response.json().get("order").get("number") is not None

    @allure.title('Создание заказа с ингредиентами')
    @allure.description('Проверка, что заказ с валидными ингредиентами успешно создается')
    def test_create_order_with_ingredients_success(self, user_data, ingredient_hashes):
        _, _, _, access_token = user_data
        headers = {"Authorization": access_token}
        payload = {"ingredients": [ingredient_hashes[0]]}
        
        with allure.step('Отправить запрос на создание заказа с одним ингредиентом'):
            response = requests.post(Urls.ORDERS, json=payload, headers=headers)
        
        with allure.step('Проверить, что заказ успешно создан'):
            assert response.status_code == 200
            assert response.json().get("success") is True
            assert response.json().get("order").get("number") is not None

    @allure.title('Создание заказа без ингредиентов')
    @allure.description('Проверка, что заказ без ингредиентов вернет ошибку 400 Bad Request')
    def test_create_order_no_ingredients_failed(self, user_data):
        _, _, _, access_token = user_data
        headers = {"Authorization": access_token}
        payload = {"ingredients": []}
        
        with allure.step('Отправить запрос на создание заказа без ингредиентов'):
            response = requests.post(Urls.ORDERS, json=payload, headers=headers)
        
        with allure.step('Проверить, что сервер возвращает ошибку 400'):
            assert response.status_code == 400
            assert response.json().get("message") == "Ingredient ids must be provided"

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    @allure.description('Проверка, что передача невалидного хеша ведет к ошибке 500 Internal Server Error')
    def test_create_order_invalid_hash_failed(self, user_data, invalid_hash):
        _, _, _, access_token = user_data
        headers = {"Authorization": access_token}
        payload = {"ingredients": [invalid_hash]}
        
        with allure.step('Отправить запрос на создание заказа с невалидным хешем ингредиента'):
            response = requests.post(Urls.ORDERS, json=payload, headers=headers)
        
        with allure.step('Проверить, что сервер возвращает ошибку 500'):
            assert response.status_code == 500