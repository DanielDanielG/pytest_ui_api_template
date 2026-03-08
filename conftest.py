import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    """Фикстура: создание драйвера Chrome"""
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    browser.implicitly_wait(4)
    browser.maximize_window()
    yield browser
    browser.quit()
