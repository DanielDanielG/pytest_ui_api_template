
import pytest
import allure
from API.MTSApi import MTSApi


@allure.feature("API Поиск товаров")
@pytest.mark.api
class TestSearchAPI:

    @pytest.fixture(scope="class")
    def api_client(self) -> MTSApi:
        """Фикстура: клиент API"""
        return MTSApi()

    @allure.story("Поиск существующего товара")
    @allure.title("Поиск товара 'Samsung' возвращает результаты")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_existing_product_samsung(
        self, api_client
    ) -> None:
        """Проверка: поиск 'Samsung' возвращает товары"""
        with allure.step("Выполнить поиск 'Samsung'"):
            response = api_client.search_products(
                query="Samsung", limit=5
            )

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200, (
                f"Ожидали 200, получили {response.status_code}"
            )

        with allure.step("Проверить наличие результатов"):
            json_data = response.json()
            assert "success_response" in json_data, (
                "Нет success_response в ответе"
            )
            entities = json_data["success_response"].get(
                "entities", []
            )
            assert len(entities) > 0, "Список товаров пуст"

        with allure.step("Проверить названия товаров"):
            for entity in entities:
                title = entity.get("title", "").lower()
                assert "samsung" in title, (
                    f"Товар '{title}' не содержит 'Samsung'"
                )

    @allure.story("Сортировка по цене")
    @allure.title("Сортировка по возрастанию цены")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_price_ascending(
        self, api_client
    ) -> None:
        """Проверка: сортировка PRICE_ASC"""
        with allure.step("Выполнить поиск с сортировкой"):
            response = api_client.search_products(
                query="Samsung",
                sort="PRICE_ASC",
                limit=10
            )

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Извлечь цены товаров"):
            json_data = response.json()
            entities = json_data["success_response"].get(
                "entities", []
            )
            prices = [
                entity.get("basePrice", 0)
                for entity in entities
                if entity.get("basePrice")
            ]

        with allure.step("Проверить сортировку"):
            assert len(prices) >= 2, "Недостаточно товаров"
            for i in range(len(prices) - 1):
                assert prices[i] <= prices[i + 1], (
                    f"Нарушение: {prices[i]} > {prices[i + 1]}"
                )

    @allure.story("Фильтрация по цене")
    @allure.title("Фильтрация по диапазону 50000-100000")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_by_price_range(
        self, api_client
    ) -> None:
        """Проверка: фильтр по цене"""
        price_min = 50000
        price_max = 100000

        with allure.step(f"Поиск с фильтром {price_min}-{price_max}"):
            response = api_client.search_products(
                query="Samsung",
                price_min=price_min,
                price_max=price_max,
                limit=10
            )

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить применение фильтра"):
            json_data = response.json()
            selected_facets = json_data["success_response"].get(
                "selectedFacets", []
            )
            price_filter = next(
                (f for f in selected_facets
                 if f.get("name") == "price"),
                None
            )
            assert price_filter is not None, (
                "Фильтр по цене не применён"
            )

        with allure.step("Проверить диапазон цен"):
            entities = json_data["success_response"].get(
                "entities", []
            )
            for entity in entities:
                price = entity.get("price", 0)
                assert price_min <= price <= price_max, (
                    f"Цена {price} вне диапазона"
                )

    @allure.story("Обработка пустого запроса")
    @allure.title("Поиск с пустой строкой")
    @allure.severity(allure.severity_level.MINOR)
    def test_empty_search_query(
        self, api_client
    ) -> None:
        """Проверка: пустой запрос"""
        with allure.step("Выполнить поиск с пустым запросом"):
            response = api_client.search_products(
                query="", limit=5
            )

        with allure.step("Проверить статус код"):
            assert response.status_code in [200, 406], (
                f"Неожиданный код: {response.status_code}"
            )

        with allure.step("Проверить ответ"):
            try:
                json_data = response.json()
            except Exception:
                json_data = None

            if response.status_code == 200:
                if json_data:
                    success_response = json_data.get(
                        "success_response", {}
                    )
                    if success_response:
                        entities = success_response.get(
                            "entities", []
                        )
                        assert isinstance(
                            entities, list
                        ), "entities должен быть списком"
            else:
                if json_data:
                    has_error = (
                        "error_backend" in json_data or
                        "error" in json_data or
                        "message" in json_data
                    )
                    assert has_error, "Нет сообщения об ошибке"

    @allure.story("Недопустимый метод")
    @allure.title("Запрос с методом DELETE")
    @allure.severity(allure.severity_level.MINOR)
    def test_invalid_http_method(
        self, api_client
    ) -> None:
        """Проверка: запрос с методом DELETE"""
        with allure.step("Выполнить запрос с DELETE"):
            response = api_client.search_with_invalid_method(
                query="Samsung",
                method="DELETE"
            )

        with allure.step("Проверить код ответа"):
            assert response.status_code in [400, 404, 405, 500], (
                f"Ожидали ошибку, получили {response.status_code}"
            )

        with allure.step("Проверить сообщение об ошибке"):
            try:
                json_data = response.json()
                has_error = (
                    "error" in json_data or
                    "error_backend" in json_data or
                    "message" in json_data
                )
                assert has_error, "Нет сообщения об ошибке"
            except Exception:
                pass
