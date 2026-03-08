
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
import pytest


@allure.step("Извлечь цену: {text}")
def extract_price(text: str) -> int:
    """Извлекает число из строки типа '59 990 ₽'"""
    if not text:
        return 0
    return int(''.join(c for c in text if c.isdigit()))


@allure.feature("Поиск")
@pytest.mark.ui
class TestSearch:

    @allure.story("Очистка поиска")
    @allure.title("Проверка очистки поля")
    def test_search_clear(self, driver) -> None:
        """Проверка ввода и очистки поля поиска"""
        waiter = WebDriverWait(driver, 10)
        from pages.main_page import MainPage
        page = MainPage(driver, waiter)

        with allure.step("Открыть и ввести запрос"):
            page.open().close_all_popups().search(
                "Samsung Galaxy"
            )
            assert page.get_search_value() == "Samsung Galaxy"

        with allure.step("Очистить поле"):
            page.clear_search()
            assert page.get_search_value() == ""

    @allure.story("Раскладка клавиатуры")
    @allure.title("Поиск с коррекцией раскладки")
    def test_search_keyboard_layout(self, driver) -> None:
        """Проверка поиска с учетом раскладки клавиатуры"""
        waiter = WebDriverWait(driver, 10)
        from pages.main_page import MainPage
        main = MainPage(driver, waiter)

        with allure.step("Выполнить поиск"):
            search = main.open().search("шзрщту").submit_search()
            search.wait_products_loaded()
            assert search.get_product_count() > 0

    @allure.story("Сортировка")
    @allure.title("Проверка сортировки по убыванию")
    def test_search_sorting_descending(self, driver) -> None:
        """Проверка сортировки товаров: Сначала дорогие"""
        waiter = WebDriverWait(driver, 10)
        from pages.search_page import SearchPage
        page = SearchPage(driver, waiter)

        with allure.step("Переход на страницу поиска"):
            page.open(query=SearchPage.SEARCH_QUERY)

        with allure.step("Закрыть окно региона"):
            try:
                close_btn = waiter.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR,
                         ".mtsds-button.confirm-region__close")
                    )
                )
                close_btn.click()
            except TimeoutException:
                pass

        with allure.step("Закрыть куки"):
            try:
                cookie_btn = waiter.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR,
                         ".cookies-massage__btn.mtsds-button--"
                         "color--alternative")
                    )
                )
                cookie_btn.click()
            except TimeoutException:
                pass

        with allure.step("Дождаться загрузки карточек"):
            waiter.until(
                EC.presence_of_all_elements_located(
                    page.PRODUCT_CARD
                )
            )

        with allure.step("Нажать на сортировку"):
            table = waiter.until(
                EC.element_to_be_clickable(page.SORTING_BUTTON)
            )
            table.click()

        with allure.step("Выбрать 'Сначала дорогие'"):
            dev = waiter.until(
                EC.element_to_be_clickable(
                    page.SORTING_EXPENSIVE
                )
            )
            dev.click()

        with allure.step("Дождаться исчезновения спиннера"):
            try:
                WebDriverWait(driver, 15).until(
                    EC.invisibility_of_element_located((
                        By.CSS_SELECTOR,
                        ".mtsds-spinner."
                        "mtsds-spinner--color-black."
                        "mtsds-spinner--size-m"
                    ))
                )
            except TimeoutException:
                pass

        with allure.step("Дождаться загрузки после сортировки"):
            waiter.until(
                EC.presence_of_all_elements_located(
                    page.PRODUCT_CARD
                )
            )

        with allure.step("Найти все карточки товаров"):
            product_cards = driver.find_elements(
                *page.PRODUCT_CARD
            )

        with allure.step("Извлечь все цены"):
            prices = []
            for card in product_cards:
                try:
                    price_elem = card.find_element(
                        *page.PRICE_VALUE
                    )
                    price_text = price_elem.text
                    price_clean = ''.join(
                        char for char in price_text
                        if char.isdigit()
                    )
                    price = (
                        int(price_clean) if price_clean else None
                    )
                    if price is not None:
                        prices.append(price)
                except Exception:
                    continue

        with allure.step("Проверка: количество цен = карточкам"):
            assert len(prices) == len(product_cards)

        with allure.step("Проверка: цены по убыванию"):
            for i in range(len(prices) - 1):
                assert prices[i] >= prices[i + 1]


@allure.feature("Корзина")
@pytest.mark.ui
class TestCart:

    @allure.story("Счётчик корзины")
    @allure.title("Проверка обновления счётчика")
    def test_cart_counter_update(self, driver) -> None:
        """Проверка обновления счётчика корзины"""
        waiter = WebDriverWait(driver, 10)
        from pages.search_page import SearchPage
        page = SearchPage(driver, waiter)

        with allure.step("Переход на страницу"):
            page.open(query=SearchPage.SEARCH_QUERY)

        with allure.step("Закрыть окно региона"):
            try:
                close_btn = waiter.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, ".confirm-region__close")
                    )
                )
                close_btn.click()
            except TimeoutException:
                pass

        with allure.step("Закрыть куки"):
            try:
                cookie_btn = waiter.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR,
                         ".cookies-massage__btn.mtsds-button--"
                         "color--alternative")
                    )
                )
                cookie_btn.click()
            except TimeoutException:
                pass

        with allure.step("Дождаться загрузки карточек"):
            waiter.until(
                EC.presence_of_all_elements_located(
                    page.PRODUCT_CARD
                )
            )

        with allure.step("Счётчик корзины скрыт"):
            counter = driver.find_element(*page.CART_COUNTER)
            assert "display: none" in counter.get_attribute(
                "style"
            )

        with allure.step("Найти первую карточку"):
            product_card = driver.find_element(*page.PRODUCT_CARD)

        with allure.step("XPath для кнопки добавления"):
            xpath = page.BUY_BUTTON_XPATH

        with allure.step("Ждать появления кнопки и нажать"):
            buy_button = WebDriverWait(product_card, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)
                )
            )
            buy_button.click()

        with allure.step("Проверка обновления счётчика"):
            waiter.until(EC.visibility_of(counter))
            assert counter.text.strip() == "1"


@allure.feature("Промокоды")
@pytest.mark.ui
class TestPromo:

    @allure.story("Применение промокода")
    @allure.title("Проверка промокода и расчёта скидки")
    def test_promo_and_discount_calculation(
        self, driver
    ) -> None:
        """Проверка промокода и расчёта скидки"""
        waiter = WebDriverWait(driver, 10)
        from pages.product_page import ProductPage
        page = ProductPage(driver, waiter)

        with allure.step("Переход на страницу товара"):
            page.open(ProductPage.PRODUCT_ID)

        with allure.step("Закрыть окно региона"):
            try:
                close_btn = waiter.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR,
                         ".mtsds-button.confirm-region__close")
                    )
                )
                close_btn.click()
            except TimeoutException:
                pass

        with allure.step("Закрыть куки"):
            try:
                cookie_btn = waiter.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR,
                         ".cookies-massage__btn.mtsds-button--"
                         "color--alternative")
                    )
                )
                cookie_btn.click()
            except TimeoutException:
                pass

        with allure.step("Нажать 'Купить'"):
            buy_button = waiter.until(
                EC.element_to_be_clickable(page.BUY_BUTTON)
            )
            buy_button.click()

        with allure.step("Нажать 'В корзину'"):
            cart_button = waiter.until(
                EC.element_to_be_clickable(page.CART_LINK)
            )
            cart_button.click()

        with allure.step("Ждать появления кнопки оформления"):
            waiter.until(
                EC.presence_of_element_located(
                    page.CHECKOUT_BUTTON
                )
            )

        with allure.step("Проверить поле промокода"):
            promo_input = driver.find_element(*page.PROMO_INPUT)
            promo_value = promo_input.get_attribute('value')

        with allure.step("Если поле пустое — ввести промокод"):
            if not promo_value or promo_value.strip() == "":
                promo_input.send_keys(ProductPage.PROMO_CODE)
                apply_btn = driver.find_element(
                    *page.PROMO_APPLY_BTN
                )
                apply_btn.click()

        with allure.step("Финальная проверка промокода"):
            final_value = promo_input.get_attribute('value')
            assert ProductPage.PROMO_CODE in final_value, (
                f"Ожидали '{ProductPage.PROMO_CODE}', "
                f"получили '{final_value}'"
            )

        with allure.step("Проверка расчёта скидки"):
            discount_elems = driver.find_elements(
                *page.DISCOUNT_ELEMENTS
            )
            discount_products = page.extract_price(
                discount_elems[0].text
            ) if len(discount_elems) > 0 else 0

            discount_promo = page.extract_price(
                discount_elems[1].text
            ) if len(discount_elems) > 1 else 0

            price_original = page.get_price_original()
            price_total = page.get_price_total()

            expected_total = (
                price_original - discount_products -
                discount_promo
            )
            assert price_total == expected_total, (
                f"Ошибка: {price_original} - {discount_products} - "
                f"{discount_promo} != {price_total}"
            )
