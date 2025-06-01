from selenium.webdriver.common.by import By


class CreatePetLocators:
    CREATE_PET_BUTTON = (By.XPATH,
                         "//button[@class='p-button p-component p-button-icon-only p-button-rounded p-button-primary p-button-outlined']")

    NAME_FIELD = (By.XPATH, "//input[@class='p-inputtext p-component w-full']")
    AGE_FIELD = (By.XPATH, "//input[@class='p-inputtext p-component p-inputnumber-input']")
    TYPE_DROPDOWN = (By.XPATH, "//span[@class='p-dropdown-label p-inputtext p-placeholder']")
    GENDER_FIELD = (By.XPATH, "//span[@aria-label='Select a Gender']")
    SUBMIT_BUTTON = (By.XPATH, "//button[@class='p-button p-component p-button-success']")

    PET_TYPES = {
        'dog' : (By.XPATH, "//li[@id='pv_id_4_0']"),
        'cat' : (By.XPATH, "//li[@id='pv_id_4_1']"),
        'reptile' : (By.XPATH, "//li[@id='pv_id_4_2']"),
        'hamster' : (By.XPATH, "//li[@id='pv_id_4_3']")
    }

    GENDERS = {
        'male' : (By.XPATH, "//li[@id='pv_id_5_0']"),
        'female' : (By.XPATH, "//li[@id='pv_id_5_1']")
    }
