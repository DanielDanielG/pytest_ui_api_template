"""Фикстуры pytest для UI тестов"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from typing import Generator


def pytest_configure(config) -> None:
    """Регистрация маркеров pytest"""
    config.addinivalue_line("markers", "ui: UI тесты")
    config.addinivalue_line("markers", "api: API тесты")


@pytest.fixture
def driver() -> Generator[webdriver.Chrome, None, None]:
    """Фикстура: создание драйвера Chrome"""
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    browser.implicitly_wait(4)
    browser.maximize_window()
    yield browser
    browser.quit()
