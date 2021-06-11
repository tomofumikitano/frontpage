#!/usr/bin/env python3
import string
import random
import pytest
from selenium import webdriver

BASE_URL = "http://localhost:8000/feeds"

VALID_FEED_URLS = [
    'https://lobste.rs/t/python.rss',
    'https://www.theguardian.com/football/rss',
    'https://srad.jp/sradjp.rss',
    'https://www.newsweekjapan.jp/column/rss.xml',
]

# TODO
INVALID_FEED_URLS = [
]


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Firefox()
    yield driver
    driver.close()


@pytest.fixture(scope="session")
def test_user():
    """
    Returns username something like testuser_5924 with 16-character password
    """
    username = 'testuser_' + \
        ''.join(random.SystemRandom().choice(string.digits) for _ in range(4))
    password = ''.join(random.SystemRandom().choice(
        string.ascii_letters + string.digits) for _ in range(16))
    print(f"Created {username} with password {password}")
    return (username, password)


def test_index(driver):
    driver.get(BASE_URL)
    assert "Frontpage" in driver.title


def test_register(driver, test_user):
    (username, password) = test_user
    driver.get(BASE_URL + "/register")
    assert "Register" in driver.title

    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password1').send_keys(password)
    driver.find_element_by_name('password2').send_keys(password)
    driver.find_element_by_id('register').click()
    assert f'Hello {username}!' in driver.page_source

    driver.get(BASE_URL + "/logout")
    assert 'Logout successfull' in driver.page_source


def _login(driver, test_user):
    (username, password) = test_user
    driver.get(BASE_URL + "/login")
    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_id('login_button').click()


def test_login(driver, test_user):
    driver.get(BASE_URL + "/login")
    assert "Login" in driver.title

    _login(driver, test_user)
    assert f'Welcome back {test_user[0]}!' in driver.page_source

    driver.get(BASE_URL + "/logout")
    assert 'Logout successfull' in driver.page_source


def test_create(driver, test_user):
    if 'Add Feed' not in driver.page_source:
        _login(driver, test_user)
    driver.get(BASE_URL + "/create")
    assert 'Edit Feed' in driver.title

    for url in VALID_FEED_URLS:
        print(url)
        driver.get(BASE_URL + "/create")
        driver.find_element_by_name('url').send_keys(url)
        # TODO - Rename saveBtn to save_button
        driver.find_element_by_id('saveBtn').click()
        assert 'Subscribed to ' in driver.page_source
