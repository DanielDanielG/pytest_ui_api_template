# pages/search_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class SearchPage:
    """Страница поиска"""

    URL_TEMPLATE: str = (
        "https://shop.mts.ru/search/?TYPE=products&q={query}"
    )

    PRODUCT_CARD = (
        By.CSS_SELECTOR, ".v2-search__product-card"
    )
    SORTING_BUTTON = (
        By.XPATH, "//div[contains(@class, 'mtsds-dropdown__control-blende')]"
    )
    SORTING_EXPENSIVE = (
        By.XPATH,
        "//span[contains(@class, "
        "'mtsds-dropdown-select__list-item-label-name') "
        "and contains(normalize-space(.), 'Сначала дорогие')]"
    )
    PRICE_VALUE = (By.CSS_SELECTOR, ".price__value")
    CART_COUNTER = (
        By.CSS_SELECTOR,
        ".cart-button .mdsx-counter-button__quantity"
    )
    BUY_BUTTON_XPATH = (
        """.//button[contains(., 'Купить') or """
        """contains(., 'В корзину') or contains(., 'Предзаказ') """
        """or contains(., 'Добавить')]"""
    )

    SEARCH_QUERY: str = "iphone"
    EXPECTED_COUNTER: str = "1"

    def __init__(
        self, driver, waiter: WebDriverWait = None, query: str = ""
    ):
        self.driver = driver
        self.waiter = waiter or WebDriverWait(driver, 10)
        if query:
            self.URL = self.URL_TEMPLATE.format(query=query)

    @allure.step("Открыть поиск: {query}")
    def open(self, query: str = ""):
        if query:
            self.URL = self.URL_TEMPLATE.format(query=query)
        self.driver.get(self.URL)
        self._close_popups()
        return self

    def _close_popups(self):
        try:
            self.waiter.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".confirm-region__close")
                )
            ).click()
            self.waiter.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     ".cookies-massage__btn.mtsds-button--"
                     "color--alternative")
                )
            ).click()
        except Exception:
            pass

    @allure.step("Дождаться загрузки товаров")
    def wait_products_loaded(self):
        self.waiter.until(
            EC.presence_of_all_elements_located(self.PRODUCT_CARD)
        )
        return self

    @allure.step("Получить карточки товаров")
    def get_product_cards(self) -> list:
        return self.driver.find_elements(*self.PRODUCT_CARD)

    @allure.step("Получить количество товаров")
    def get_product_count(self) -> int:
        return len(self.get_product_cards())

    @allure.step("Сортировать: Сначала дорогие")
    def sort_by_expensive(self):
        # Ждём кнопку сортировки и кликаем
        sorting_btn = self.waiter.until(
            EC.element_to_be_clickable(self.SORTING_BUTTON)
        )
        sorting_btn.click()

        # Ждём опцию и кликаем
        option = self.waiter.until(
            EC.element_to_be_clickable(self.SORTING_EXPENSIVE)
        )
        option.click()

        # Ждём обновления списка товаров
        self.waiter.until(
            EC.presence_of_all_elements_located(self.PRODUCT_CARD)
        )
        return self

    @allure.step("Извлечь цены")
    def get_prices(self) -> list[int]:
        prices: list[int] = []
        for card in self.get_product_cards():
            try:
                price_elem = card.find_element(*self.PRICE_VALUE)
                price_text = price_elem.text
                price_clean = ''.join(
                    c for c in price_text if c.isdigit()
                )
                if price_clean:
                    prices.append(int(price_clean))
            except Exception:
                continue
        return prices

    @allure.step("Получить счётчик корзины")
    def get_cart_counter(self):
        return self.driver.find_element(*self.CART_COUNTER)

    @allure.step("Проверить скрытость счётчика")
    def is_cart_counter_hidden(self) -> bool:
        counter = self.get_cart_counter()
        style = counter.get_attribute("style")
        return "display: none" in style if style else True

    @allure.step("Добавить товар в корзину")
    def add_first_product_to_cart(self):
        cards = self.get_product_cards()
        if not cards:
            raise Exception("Нет товаров")
        buy_btn = WebDriverWait(cards[0], 5).until(
            EC.presence_of_element_located(
                (By.XPATH, self.BUY_BUTTON_XPATH)
            )
        )
        buy_btn.click()
        return self

    @allure.step("Дождаться обновления счётчика: {expected_value}")
    def wait_cart_counter_updated(self, expected_value: str = "1"):
        counter = self.get_cart_counter()
        self.waiter.until(EC.visibility_of(counter))
        assert counter.text.strip() == expected_value
        return self
