
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import allure


class BasketPage:
    """Страница корзины"""

    URL: str = "https://shop.mts.ru/personal/basket"
    CART_COUNTER = (
        By.CSS_SELECTOR,
        ".cart-button .mdsx-counter-button__quantity"
    )

    def __init__(
        self, driver, waiter: WebDriverWait = None
    ) -> None:
        self.driver = driver
        self.waiter = waiter or WebDriverWait(driver, 10)

    @allure.step("Открыть корзину")
    def open(self) -> "BasketPage":
        self.driver.get(self.URL)
        return self

    @allure.step("Получить значение счётчика")
    def get_cart_counter_value(self) -> str:
        return self.driver.find_element(
            *self.CART_COUNTER
        ).text.strip()

    @allure.step("Проверить видимость счётчика")
    def is_cart_counter_visible(self) -> bool:
        return self.driver.find_element(
            *self.CART_COUNTER
        ).is_displayed()
