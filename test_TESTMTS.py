from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import (
    expected_conditions as EC)
from selenium.webdriver.chrome.service import (
    Service as ChromeService)
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(
    service=ChromeService(
        ChromeDriverManager().install()))
driver.maximize_window()
waiter = WebDriverWait(driver, 2)


def test_search_clear():

    # Переход на страницу

    driver.get("https://shop.mts.ru/  ")

    # Закрыть окно региона

    close_btn = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             ".mtsds-button.confirm-region__close")))
    close_btn.click()
    cookie_btn = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             ".cookies-massage__btn."
             "mtsds-button--color--alternative")))
    cookie_btn.click()

    # Найти поиск и кликнуть по нему

    inputs = driver.find_element(
        By.CSS_SELECTOR, ".search-form-field__input")
    inputs.click()

    # Ввести текст

    waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             ".search-popup-result-block__input")
        ))
    XX = driver.find_element(
        By.CSS_SELECTOR, ".search-popup-result-block__input")
    XX.clear()
    XX.send_keys("Samsung Galaxy")

    assert XX.get_attribute("value") == "Samsung Galaxy"

    # Yfqnb ryjgre jxbcnrb gjkz b yf;fnm

    driver.find_element(
        By.CSS_SELECTOR, ".input-field__clear-field").click()
    waiter.until(lambda d: XX.get_attribute("value") == "")
    assert XX.get_attribute("value") == ""
    driver.quit()


def test_search_keyboard_layout():

    # Переход на страницу

    driver.get("https://shop.mts.ru/  ")

    # Закрыть окно региона

    close_btn = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             ".mtsds-button.confirm-region__close")))
    close_btn.click()
    cookie_btn = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             ".cookies-massage__btn."
             "mtsds-button--color--alternative")))
    cookie_btn.click()

    # Найти поиск и кликнуть по нему

    inputs = driver.find_element(
        By.CSS_SELECTOR, ".search-form-field__input")
    inputs.click()

    # Ввести текст

    waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             ".search-popup-result-block__input")
        ))
    XX = driver.find_element(
        By.CSS_SELECTOR, ".search-popup-result-block__input")
    XX.clear()
    XX.send_keys("шзрщту")
    assert XX.get_attribute("value") == "шзрщту"
    SearchButton = driver.find_element(
        By.CSS_SELECTOR,
        ".search-popup-result-block__button")
    SearchButton.click()

    # Шаг 2: Дождаться загрузки карточек товаров
    waiter.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".v2-search__product-card")))

    # Шаг 3: Найти все карточки товаров
    product_cards = driver.find_elements(
        By.CSS_SELECTOR, ".v2-search__product-card")

    # === ПРОВЕРКА 1: Список карточек не пустой ===
    assert len(product_cards) > 0
    print(f"Найдено карточек товаров: {len(product_cards)}")

    # === ПРОВЕРКА 2: В атрибутах id карточек есть слово
    # "iphone" (НЧЛ 7) ===
    ids_with_iphone = []
    for card in product_cards:
        element_id = card.get_attribute("id")
        if element_id and "iphone" in element_id.lower():
            ids_with_iphone.append(element_id)

    assert len(ids_with_iphone) == len(product_cards)
    driver.quit()


def test_search_AC():

    # Переход на страницу

    driver.get(
        "https://shop.mts.ru/search/?TYPE=products&q=iphone  ")

    # Закрыть окно региона

    close_btn = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             ".mtsds-button.confirm-region__close")))
    close_btn.click()
    cookie_btn = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             ".cookies-massage__btn."
             "mtsds-button--color--alternative")))
    cookie_btn.click()

    # Шаг 2: Дождаться загрузки карточек товаров

    waiter.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".v2-search__product-card")))

    # Шаг 3: Найти табличку сортировки нажать на нёё

    table = driver.find_element(
        By.XPATH, "//div[contains(@class, 'mtsds-dropdown__control-blende')]")
    table.click()

    # Шаг 4: Выбрать значение Сначала дорогие

    DEV = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//span[contains(@class, "
            "'mtsds-dropdown-select__list-item-label-name') "
            "and contains(normalize-space(.), 'Сначала дорогие')]"
        ))
        )
    DEV.click()
    # Шаг 5: Дождаться исчезновения спиннера загрузки
    # Это гарантирует, что сортировка применилась и
    # карточки перерисовались с новыми ценами

    WebDriverWait(driver, 15).until(
        EC.invisibility_of_element_located((
            By.CSS_SELECTOR,
            ".mtsds-spinner."
            "mtsds-spinner--color-black."
            "mtsds-spinner--size-m"
        )))

    # Шаг 5: Дождаться загрузки карточек товаров
    # после сортировки
    waiter.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".v2-search__product-card")))

    # Шаг 6: Найти все карточки товаров
    product_cards = driver.find_elements(
        By.CSS_SELECTOR, ".v2-search__product-card")

    # Шаг 7: Функция извлечения цены
    def extract_price(card):
        price_elem = card.find_element(
            By.CSS_SELECTOR, ".price__value")
        price_text = price_elem.text
        price_clean = ''.join(
            char for char in price_text if char.isdigit())
        return int(price_clean) if price_clean else None

    # Шаг 8: Извлечь все цены
    prices = [extract_price(card) for card in product_cards]
    prices = [p for p in prices if p is not None]

    # Проверка 1: количество цен соответствует карточкам
    assert len(prices) == len(product_cards)

    # Проверка 2: цены по убыванию
    for i in range(len(prices) - 1):
        assert prices[i] >= prices[i + 1]
    driver.quit()


def test_cart_AC():
    # Переход на страницу

    driver.get(
        "https://shop.mts.ru/search/?TYPE=products&q=iphone  ")
    waiter = WebDriverWait(driver, 10)

    # Закрыть окно региона
    close_btn = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".confirm-region__close")))
    close_btn.click()
    cookie_btn = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             ".cookies-massage__btn."
             "mtsds-button--color--alternative")))
    cookie_btn.click()
    # Дождаться загрузки карточек
    waiter.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".v2-search__product-card")))

    # Счётчик корзины скрыт
    counter = driver.find_element(
        By.CSS_SELECTOR,
        ".cart-button .mdsx-counter-button__quantity")
    assert "display: none" in counter.get_attribute("style")

    # Найти первую карточку
    product_card = driver.find_element(
        By.CSS_SELECTOR, ".v2-search__product-card")

    # XPath для любой кнопки добавления в корзину
    xpath = """.//button[
        contains(., 'Купить') or
        contains(., 'В корзину') or
        contains(., 'Предзаказ') or
        contains(., 'Добавить')
    ]"""

    # Ждать появления кнопки
    buy_button = WebDriverWait(product_card, 5).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    buy_button.click()

    # Проверка обновления счётчика
    waiter.until(EC.visibility_of(counter))
    assert counter.text.strip() == "1"
    driver.quit()


def test_cart_AC1():
    # Переход на страницу

    driver.get(
        "https://shop.mts.ru/search/?TYPE=products&q=iphone  ")
    waiter = WebDriverWait(driver, 10)

    # Закрыть окно региона
    close_btn = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".confirm-region__close")))
    close_btn.click()
    cookie_btn = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             ".cookies-massage__btn."
             "mtsds-button--color--alternative")))
    cookie_btn.click()
    # Дождаться загрузки карточек
    waiter.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".v2-search__product-card")))

    # Счётчик корзины скрыт
    counter = driver.find_element(
        By.CSS_SELECTOR,
        ".cart-button .mdsx-counter-button__quantity")
    assert "display: none" in counter.get_attribute("style")

    # Найти первую карточку
    product_card = driver.find_element(
        By.CSS_SELECTOR, ".v2-search__product-card")

    # XPath для любой кнопки добавления в корзину
    xpath = """.//button[
        contains(., 'Купить') or
        contains(., 'В корзину') or
        contains(., 'Предзаказ') or
        contains(., 'Добавить')
    ]"""

    # Ждать появления кнопки
    buy_button = WebDriverWait(product_card, 5).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    buy_button.click()

    # Проверка обновления счётчика
    waiter.until(EC.visibility_of(counter))
    assert counter.text.strip() == "1"
    driver.quit()


def test_promo():
    # Функция извлечения цены из текста
    def extract_price(text):
        """Извлекает число из строки типа '59 990 ₽'
        или '20 000'"""
        if not text:
            return 0
        return int(''.join(c for c in text if c.isdigit()))

    # Переход на страницу

    driver.get(
        "https://shop.mts.ru/product/"
        "smartfon-huawei-nova-13-pro-12-512-gb-"
        "lte-chernyj  ")
    waiter = WebDriverWait(driver, 10)

    # Закрыть окно региона

    close_btn = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".confirm-region__close")))
    close_btn.click()

    # Закрыть куки

    cookie_btn = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             ".cookies-massage__btn."
             "mtsds-button--color--alternative")))
    cookie_btn.click()

    # Нажать "Купить"

    BUYBUTTON = driver.find_element(
        By.CSS_SELECTOR, ".buy-button")
    BUYBUTTON.click()

    # Нажать "В корзину"

    cart_button = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a.btn-group__btn')))
    cart_button.click()

    # Ждать появления кнопки "Перейти к оформлению"

    waiter.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "button.basket-promo-info__button")))
    print("Страница корзины загружена")

    # Проверить поле промокода

    promo_input = driver.find_element(
        By.CSS_SELECTOR, "input#promo-info-promocode")
    promo_value = promo_input.get_attribute('value')

    # Если поле пустое — ввести промокод и применить

    if not promo_value or promo_value.strip() == "":
        print("Поле пустое — вводим промокод MTS57...")
        promo_input.send_keys("MTS57")

        # Нажать кнопку применения (стрелка)
        apply_btn = driver.find_element(
            By.CSS_SELECTOR, ".purchase-info__btn-icon")
        apply_btn.click()
        print("Промокод применён!")

    # Финальная проверка: поле содержит "MTS57"

    final_value = promo_input.get_attribute('value')
    assert "MTS57" in final_value, (
        f"Ожидали 'MTS57', получили '{final_value}'")
    print(f"Промокод подтверждён: '{final_value}'")

    # НОВАЯ ЧАСТЬ: Проверка расчёта скидки

    print("\n Проверка расчёта скидки...")

    # 1. Скидка на товары (первый элемент с классом)
    discount_elems = driver.find_elements(
        By.CSS_SELECTOR,
        "p.basket-discount-list__item-text--value")
    discount_products = (
        extract_price(discount_elems[0].text)
        if len(discount_elems) > 0 else 0)

    # 2. Скидка по промокоду (второй элемент)
    discount_promo = (
        extract_price(discount_elems[1].text)
        if len(discount_elems) > 1 else 0)

    # 3. Цена без скидок
    price_original_elem = driver.find_element(
        By.CSS_SELECTOR,
        "div.purchase-info__fill-price-sum")
    price_original = extract_price(price_original_elem.text)

    # 4. Цена со скидками
    price_total_elem = driver.find_element(
        By.CSS_SELECTOR, "div.purchase-info__total-sum")
    price_total = extract_price(price_total_elem.text)

    # Проверка формулы: Цена без скидок - Скидки =
    # Итоговая цена

    expected_total = (
        price_original - discount_products - discount_promo)
    assert price_total == expected_total

    driver.quit()
