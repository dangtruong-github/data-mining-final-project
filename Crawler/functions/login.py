from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

from dotenv import load_dotenv

###### Environment variables ######
# Load environment variables from the .env file
load_dotenv()

def login(driver, timeout_value):
    # Access the variables using os.environ.get
    USERNAME = os.environ.get("USER_NAME")
    PASSWORD = os.environ.get("PASSWORD")

    # Find the button by its class name
    login_button = WebDriverWait(driver, timeout_value).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[3]/div/div[2]/main/div/div/div/div/button"))
    )

    # Click the button
    login_button.click()

    username_fill = WebDriverWait(driver, timeout_value).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[3]/div/div[2]/main/div/div/div/div/form/div/div[1]/input"))
    )

    username_fill.send_keys(USERNAME)

    password_fill = WebDriverWait(driver, timeout_value).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[3]/div/div[2]/main/div/div/div/div/form/div/div[2]/div/input"))
    )

    password_fill.send_keys(PASSWORD)

    login_button = WebDriverWait(driver, timeout_value).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[3]/div/div[2]/main/div/div/div/div/form/input"))
    )

    login_button.click()

    return driver
