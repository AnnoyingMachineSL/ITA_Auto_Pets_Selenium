from selenium.webdriver.common.by import By

class RegistrationConfig:
    REGISTRATION_BASE_URS = 'http://34.141.58.52:8080/#/register'
    LOGIN_FIELD = (By.XPATH, '//*[@id="login"]')
    PASSWORD_FIELD = (By.XPATH, "//input[@class='p-inputtext p-component']")
    CONFIRM_PASSWORD_FIELD = (By.XPATH, '//*[@id="confirm_password"]/input')
    SUBMIT_BUTTON = (By.XPATH, "//button[@class='p-button p-component']")
    REGISTRATION_LOGO = (By.XPATH, "//span[@class='p-fieldset-legend-text']")
    AFTER_REGISTRATION_URL = 'http://34.141.58.52:8080/#/profile'
    LOGIN_ERROR_MESSAGE = (By.XPATH, "//div[@class='text-red-500']")
    ERROR_MESSAGE_IN_DIFFERENT_PASSWORDS = (By.XPATH, "//div[@class='p-message-wrapper']")