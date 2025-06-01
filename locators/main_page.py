from selenium.webdriver.common.by import By


class MainPageLocators:
    DELETE_BUTTONS = (By.XPATH, "//button[@class='p-button p-component p-button-danger']")
    SUCCESS_DELETE_MESSAGE = (By.XPATH, "//div[@class='p-toast-message-content']")
    CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[@class='p-button p-component p-confirm-popup-accept p-button-sm']")
