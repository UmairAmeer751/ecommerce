"""
NexShop Selenium Test Suite — FA23-BCS-209
------------------------------------------
Requirements:  pip install selenium webdriver-manager pytest
Run locally:   pytest tests/test_selenium.py -v
Run vs Docker: BASE_URL=http://localhost pytest tests/test_selenium.py -v
"""
import os
import time
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.environ.get('BASE_URL', 'http://localhost')


@pytest.fixture(scope='module')
def driver():
    """Headless Chrome driver shared across all tests in the module."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1280,900')
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()


# ══════════════════════════════════════════════════════════════
# TEST 1 — Verify Homepage Loads
# ══════════════════════════════════════════════════════════════
class TestHomepage:

    def test_homepage_title(self, driver):
        """Page title must contain 'NexShop'."""
        driver.get(BASE_URL)
        assert 'NexShop' in driver.title, f"Unexpected title: {driver.title}"

    def test_homepage_hero_heading(self, driver):
        """H1 hero heading must be visible on the page."""
        driver.get(BASE_URL)
        h1 = driver.find_element(By.TAG_NAME, 'h1')
        assert h1.is_displayed()
        assert len(h1.text) > 0

    def test_navbar_present(self, driver):
        """Navigation bar must be present and visible."""
        driver.get(BASE_URL)
        navbar = driver.find_element(By.CLASS_NAME, 'navbar')
        assert navbar.is_displayed()


# ══════════════════════════════════════════════════════════════
# TEST 2 — Validate Product Display (Frontend → Backend API)
# ══════════════════════════════════════════════════════════════
class TestProductDisplay:

    def test_products_are_loaded(self, driver):
        """Product cards must appear after API fetch completes."""
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 20)
        cards = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-card'))
        )
        assert len(cards) >= 1, "Expected at least 1 product card"

    def test_products_have_titles(self, driver):
        """Each product card must display a non-empty product title."""
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-card')))
        titles = driver.find_elements(By.CLASS_NAME, 'product-title')
        assert len(titles) > 0
        for title in titles:
            assert len(title.text.strip()) > 0

    def test_products_have_prices(self, driver):
        """Each product card must display a price."""
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-card')))
        prices = driver.find_elements(By.CLASS_NAME, 'product-price')
        assert len(prices) > 0


# ══════════════════════════════════════════════════════════════
# TEST 3 — Add to Cart & Cart Modal Behaviour
# ══════════════════════════════════════════════════════════════
class TestCartBehaviour:

    def test_add_to_cart_increments_badge(self, driver):
        """Clicking 'Add to Cart' must increment the cart badge count."""
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 20)
        add_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-add')))
        add_btn.click()
        time.sleep(0.5)
        badge = driver.find_element(By.ID, 'cart-count')
        assert badge.text == '1', f"Expected badge '1', got '{badge.text}'"

    def test_cart_modal_opens_on_click(self, driver):
        """Clicking the cart icon must open the cart modal."""
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.ID, 'cart-btn')))
        driver.find_element(By.ID, 'cart-btn').click()
        modal = driver.find_element(By.ID, 'cart-modal')
        assert modal.is_displayed(), "Cart modal did not open"

    def test_cart_modal_closes_on_x(self, driver):
        """Clicking the × button must close the cart modal."""
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.ID, 'cart-btn')))
        driver.find_element(By.ID, 'cart-btn').click()
        time.sleep(0.3)
        driver.find_element(By.ID, 'close-cart').click()
        time.sleep(0.3)
        modal = driver.find_element(By.ID, 'cart-modal')
        assert not modal.is_displayed(), "Cart modal should be closed"
