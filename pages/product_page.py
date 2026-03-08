# pages/product_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class ProductPage:
    """Страница товара"""

    URL_TEMPLATE: str = (
        "https://shop.mts.ru/product/{product_id}"
    )

    BUY_BUTTON = (By.CSS_SELECTOR, ".buy-button")
    CART_LINK = (By.CSS_SELECTOR, "a.btn-group__btn")
    PROMO_INPUT = (By.CSS_SELECTOR, "input#promo-info-promocode")
    PROMO_APPLY_BTN = (By.CSS_SELECTOR, ".purchase-info__btn-icon")
    CHECKOUT_BUTTON = (
        By.CSS_SELECTOR, "button.basket-promo-info__button"
    )
    DISCOUNT_ELEMENTS = (
        By.CSS_SELECTOR,
        "p.basket-discount-list__item-text--value"
    )
    PRICE_ORIGINAL = (
        By.CSS_SELECTOR, "div.purchase-info__fill-price-sum"
    )
    PRICE_TOTAL = (
        By.CSS_SELECTOR, "div.purchase-info__total-sum"
    )

    PROMO_CODE: str = "MTS57"
    PRODUCT_ID: str = (
        "smartfon-huawei-nova-13-pro-12-512-gb-lte-chernyj"
    )

    def __init__(
        self, driver, waiter: WebDriverWait = None,
        product_id: str = ""
    ):
        self.driver = driver
        self.waiter = waiter or WebDriverWait(driver, 10)
        if product_id:
            self.URL = self.URL_TEMPLATE.format(
                product_id=product_id
            )

    @allure.step("Открыть товар: {product_id}")
    def open(self, product_id: str = ""):
        if product_id:
            self.URL = self.URL_TEMPLATE.format(
                product_id=product_id
            )
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

    @allure.step("Нажать 'Купить'")
    def click_buy(self):
        buy_btn = self.waiter.until(
            EC.element_to_be_clickable(self.BUY_BUTTON)
        )
        buy_btn.click()
        return self

    @allure.step("Добавить в корзину")
    def add_to_cart(self):
        cart_btn = self.waiter.until(
            EC.element_to_be_clickable(self.CART_LINK)
        )
        cart_btn.click()
        return self

    @allure.step("Дождаться корзины")
    def wait_basket_loaded(self):
        self.waiter.until(
            EC.presence_of_element_located(self.CHECKOUT_BUTTON)
        )
        return self

    @allure.step("Получить значение промокода")
    def get_promo_value(self) -> str:
        return self.driver.find_element(
            *self.PROMO_INPUT
        ).get_attribute('value') or ""

    @allure.step("Применить промокод: {code}")
    def apply_promo(self, code: str):
        promo_input = self.driver.find_element(*self.PROMO_INPUT)
        if not promo_input.get_attribute('value'):
            promo_input.send_keys(code)
            apply_btn = self.driver.find_element(
                *self.PROMO_APPLY_BTN
            )
            apply_btn.click()
        return self

    @allure.step("Проверить промокод: {code}")
    def is_promo_applied(self, code: str) -> bool:
        return code in self.get_promo_value()

    @allure.step("Извлечь цену")
    def extract_price(self, text: str) -> int:
        if not text:
            return 0
        return int(''.join(c for c in text if c.isdigit()))

    @allure.step("Получить скидку на товары")
    def get_discount_products(self) -> int:
        elems = self.driver.find_elements(*self.DISCOUNT_ELEMENTS)
        return self.extract_price(
            elems[0].text
        ) if len(elems) > 0 else 0

    @allure.step("Получить скидку по промокоду")
    def get_discount_promo(self) -> int:
        elems = self.driver.find_elements(*self.DISCOUNT_ELEMENTS)
        return self.extract_price(
            elems[1].text
        ) if len(elems) > 1 else 0

    @allure.step("Получить цену без скидок")
    def get_price_original(self) -> int:
        return self.extract_price(
            self.driver.find_element(
                *self.PRICE_ORIGINAL
            ).text
        )

    @allure.step("Получить итоговую цену")
    def get_price_total(self) -> int:
        return self.extract_price(
            self.driver.find_element(
                *self.PRICE_TOTAL
            ).text
        )

    @allure.step("Проверить расчёт скидки")
    def verify_discount_calculation(self) -> bool:
        original = self.get_price_original()
        discount_prod = self.get_discount_products()
        discount_promo = self.get_discount_promo()
        total = self.get_price_total()
        return total == original - discount_prod - discount_promo
