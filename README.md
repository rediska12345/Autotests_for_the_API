# Autotests_for_the_API Stellar Burgers
Этот проект содержит автоматические тесты для проверки API сервиса [Stellar Burgers](https://stellarburgers.education-services.ru/). Тесты покрывают функциональность создания пользователя, авторизации и создания заказов.

## Структура проекта
- `tests/` - тесты
- `generator.py` - генераторы тестовых данных
- `url.py` - URL endpoints
- `conftest.py` - фикстуры pytest
- `requirements.txt` - зависимости

### Запуск всех тестов
pytest

#### Запуск с генерацией Allure отчета
pytest tests/ -v -s --alluredir=allure-results

##### Просмотр Allure отчета
allure serve allure_results
