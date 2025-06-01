from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class LoginLocators:
    LOGIN_FIELD = (By.XPATH, '//*[@id="login"]')
    PASSWORD_FIELD = (By.XPATH, '//*[@id="password"]/input')
    SUBMIT_BUTTON = (By.XPATH, "//button[@class='p-button p-component']")
    LOGIN_LOGO = (By.XPATH, '//*[@id="app"]/main/fieldset/legend')
    AFTER_LOGIN_URL = 'http://34.141.58.52:8080/#/profile'
    EMPTY_LOGIN_ERROR_MESSAGE = (By.XPATH, "//div[@class='text-red-500']")
    EMPTY_PASSWORD_ERROR_MESSAGE = (By.XPATH, "//div[@class='text-red-500']")
