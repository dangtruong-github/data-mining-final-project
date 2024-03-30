from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from unidecode import unidecode
from urllib.parse import unquote
import os
import json

from .stories_from_tags_test import stories_from_tags
from .data_storage import tags_crawled, tags_to_crawl, stories_crawled, stories_to_crawl, check_story_available, check_tag_available

def nav_tags(driver, timeout_value):    
    discover_btn = WebDriverWait(driver, timeout_value).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/nav[1]/ul/li[2]/button"))
    )

    discover_btn.click()

    story_types = WebDriverWait(driver, timeout_value).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/nav[1]/ul/li[2]/div[2]/div[2]/ul"))
    )

    # Locate all ul elements inside the div
    li_elements = story_types.find_elements(By.TAG_NAME, "li")

    # Iterate through each ul element
    for li_element in li_elements:
        # Locate the anchor (a) element inside the li element
        a_element = li_element.find_element(By.TAG_NAME, "a")

        # Get the href attribute value
        href_value = a_element.get_attribute('href')

        tag = unquote(href_value.split("/")[-1])

        tags_to_crawl.append((tag, 0))

    while tags_to_crawl:
        tag, depth = tags_to_crawl.pop(0)

        print(f"tag: {tag}")

        # check if this tag is crawled
        if check_tag_available(tag) == False:
            continue

        print(f"Tag crawling: {tag}, depth: {depth}")

        tags_crawled.append(tag)

        link = "https://www.wattpad.com/stories/" + tag

        # print(f"key: {tag}, value: {link}")
        stories_from_tags(driver=driver, link=link, timeout_value=timeout_value, depth=depth)

    return driver