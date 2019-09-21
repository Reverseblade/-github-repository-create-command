import os
import sys

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import config

from pages import LoginPage
from pages import CreateRepositoryPage
from pages import TwoWayAuthenticationPage

import logging
logging.basicConfig(level=logging.INFO)

# handle argument
if len(sys.argv) <= 1:
    raise Exception('Please enter your project name')
project_name = str(sys.argv[1])

# set driver
chrome_options = Options()
if config.IS_HEADLESS:
    chrome_options.add_argument("--headless")

executable_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'chromedriver'
    )

driver = webdriver.Chrome(
        executable_path=executable_path,
        options=chrome_options
    )

def handle_login_page(driver):
    login_page = LoginPage(driver)
    try:
        login_page.open()
        login_page.username_input.type(config.GITHUB_USERNAME)
        login_page.password_input.type(config.GITHUB_PASSWORD)
        login_page.submit_button.click()
    except TimeoutException:
        login_page.close()
        raise TimeoutException('The repository named {} already exists \
                            on this account'.format(project_name))
    else:
        logging.info('Logged in to Github OK!')
        return login_page.driver

def handle_two_way_auth_page(driver):
    two_way_auth_page = TwoWayAuthenticationPage(driver)
    try:
        auth_code = input('Enter your verification code: ')
        two_way_auth_page.input_box.type(auth_code)
        two_way_auth_page.verify_button.click()
    except TimeoutException:
        raise TimeoutException('The repository named {} already exists \
                           on this account'.format(project_name))
    else:
        logging.info('two-way authentication OK!')
        return two_way_auth_page.driver

def handle_create_repository_page(driver):
    create_repository_page = CreateRepositoryPage(driver)
    try:
        create_repository_page.open()
        create_repository_page.select_private_radio.click()
        create_repository_page.repository_name_input.type(project_name)
        create_repository_page.submit_button.click()
    except TimeoutException:
        create_repository_page.close()
        raise TimeoutException('The repository named {} already exists \
                            on this account'.format(project_name))
    else:
        if config.HAS_TWO_WAY_AUTHENTICATION and create_repository_page.has_verify_error_text:
            driver = handle_two_way_auth_page(driver)

        new_repository_url = 'https://github.com/{0}/{1}'.format(
                config.GITHUB_USERNAME,
                project_name
            )

        create_repository_page.close()

        if driver.current_url != new_repository_url:
            raise Exception('Failed to create a new Github repository')
        else:
            logging.info('New github repository named {} created'.format(project_name))
            return driver

def redirect_errors(driver, action):
    if action == 'two_way_auth':
        driver
        



# login to Github
driver = handle_login_page(driver)

# two-way authentication
if config.HAS_TWO_WAY_AUTHENTICATION:
    driver = handle_two_way_auth_page(driver)

# create a new repository
driver = handle_create_repository_page(driver)