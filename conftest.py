import pytest
import requests
from urls import Urls
from generators import register_new_user_and_return_data


@pytest.fixture
def user_data():
    user_info = register_new_user_and_return_data()
    if user_info is None:
        pytest.fail("Не удалось создать тестового пользователя")

    email, password, name = user_info

    login_payload = {"email": email, "password": password}
    login_response = requests.post(Urls.LOGIN_USER, json=login_payload)

    if login_response.status_code != 200:
        pytest.fail("Не удалось авторизоваться для получения токена")

    access_token = login_response.json().get("accessToken")

    yield email, password, name, access_token

    if access_token:
        headers = {"Authorization": access_token}
        requests.delete(Urls.USER, headers=headers)


@pytest.fixture
def existing_user_data(user_data):
    email, password, name, _ = user_data
    return {"email": email, "password": password, "name": name}


@pytest.fixture
def ingredient_hashes():
    response = requests.get(Urls.INGREDIENTS)
    if response.status_code == 200:
        data = response.json()
        return [ingredient["_id"] for ingredient in data.get("data", [])]
    else:
        return ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]


@pytest.fixture
def invalid_hash():
    return "invalid1234567890hash"