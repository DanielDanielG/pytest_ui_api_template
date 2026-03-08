# pages/main_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class MainPage:
    """Главная страница"""

    URL: str = "https://shop.mts.ru/"

    SEARCH_INPUT = (
        By.CSS_SELECTOR, ".search-form-field__input"
    )
    SEARCH_POPUP_INPUT = (
        By.CSS_SELECTOR, ".search-popup-result-block__input"
    )
    SEARCH_BUTTON = (
        By.CSS_SELECTOR, ".search-popup-result-block__button"
    )
    CLEAR_BUTTON = (
        By.CSS_SELECTOR, ".input-field__clear-field"
    )
    REGION_CLOSE = (
        By.CSS_SELECTOR, ".confirm-region__close"
    )
    COOKIE_BTN = (
        By.CSS_SELECTOR,
        ".cookies-massage__btn.mtsds-button--color--alternative"
    )

    def __init__(self, driver, waiter: WebDriverWait = None):
        self.driver = driver
        self.waiter = waiter or WebDriverWait(driver, 10)

    @allure.step("Открыть главную страницу")
    def open(self):
        self.driver.get(self.URL)
        return self

    @allure.step("Закрыть попапы")
    def close_all_popups(self):
        try:
            self.waiter.until(
                EC.element_to_be_clickable(self.REGION_CLOSE)
            ).click()
        except Exception:
            pass
        try:
            self.waiter.until(
                EC.element_to_be_clickable(self.COOKIE_BTN)
            ).click()
        except Exception:
            pass
        return self

    @allure.step("Выполнить поиск: {query}")
    def search(self, query: str):
        self.close_all_popups()
        self.waiter.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        ).click()
        popup_input = self.waiter.until(
            EC.element_to_be_clickable(self.SEARCH_POPUP_INPUT)
        )
        popup_input.clear()
        popup_input.send_keys(query)
        return self

    @allure.step("Очистить поле поиска")
    def clear_search(self):
        self.driver.find_element(*self.CLEAR_BUTTON).click()
        return self

    @allure.step("Отправить поисковый запрос")
    def submit_search(self):
        from pages.search_page import SearchPage
        self.driver.find_element(*self.SEARCH_BUTTON).click()
        return SearchPage(self.driver, self.waiter)

    @allure.step("Получить значение поиска")
    def get_search_value(self) -> str:
        popup_input = self.driver.find_element(
            *self.SEARCH_POPUP_INPUT
        )
        return popup_input.get_attribute("value") or ""
