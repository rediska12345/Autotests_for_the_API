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

        response = requests.post(Urls.ORDERS, json=payload, headers=headers)

        assert response.status_code == 200
        assert response.json().get("success") is True
        assert response.json().get("order").get("number") is not None

    @allure.title('Создание заказа без авторизации')
    @allure.description('Проверка, что неавторизованный пользователь может создать заказ')
    def test_create_order_without_auth_success(self, ingredient_hashes):
        payload = {"ingredients": ingredient_hashes[:2]}

        response = requests.post(Urls.ORDERS, json=payload)

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title('Создание заказа с ингредиентами')
    @allure.description('Проверка, что заказ с валидными ингредиентами успешно создается')
    def test_create_order_with_ingredients_success(self, user_data, ingredient_hashes):
        _, _, _, access_token = user_data
        headers = {"Authorization": access_token}
        payload = {"ingredients": [ingredient_hashes[0]]}

        response = requests.post(Urls.ORDERS, json=payload, headers=headers)

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title('Создание заказа без ингредиентов')
    @allure.description('Проверка, что заказ без ингредиентов вернет ошибку 400 Bad Request')
    def test_create_order_no_ingredients_failed(self, user_data):
        _, _, _, access_token = user_data
        headers = {"Authorization": access_token}
        payload = {"ingredients": []}

        response = requests.post(Urls.ORDERS, json=payload, headers=headers)

        assert response.status_code == 400
        assert response.json().get("message") == "Ingredient ids must be provided"

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    @allure.description('Проверка, что передача невалидного хеша ведет к ошибке 500 Internal Server Error')
    def test_create_order_invalid_hash_failed(self, user_data, invalid_hash):
        _, _, _, access_token = user_data
        headers = {"Authorization": access_token}
        payload = {"ingredients": [invalid_hash]}

        response = requests.post(Urls.ORDERS, json=payload, headers=headers)

        assert response.status_code == 500