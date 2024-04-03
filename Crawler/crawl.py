from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import os
import time

from dotenv import load_dotenv

from functions import login, nav_tags, close_db, clear_db, reopen_db, stories_crawled, old_stories

###### Environment variables ######
# Load environment variables from the .env file
load_dotenv()

# Access the variables using os.environ.get
USERNAME = os.environ.get("USER_NAME")
PASSWORD = os.environ.get("PASSWORD")

###### Setup chrome driver ######
# Ignore certificate errors
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Set the path to your chromedriver executable
chrome_driver_path = os.path.join(os.getcwd(), "other", "chromedriver-win64", "chromedriver.exe")

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

# Open the webpage
driver.get("https://www.wattpad.com/login")

timeout_value = 10000

# clear_db()
# reopen_db()

old_stories()

print(f"Stories crawled: {len(stories_crawled)}")

driver = login(driver=driver, timeout_value=timeout_value)

driver = nav_tags(driver=driver, timeout_value=timeout_value)

#close_db()

time.sleep(1000)

# Close the browser
driver.quit()
