from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import os
import time
from urllib.parse import unquote
from .data_storage import tags_crawled, tags_to_crawl, stories_crawled, stories_to_crawl, check_story_available, check_tag_available, MAX_DEPTH
from .story_crawling import story_crawling

def stories_from_tags(driver, link, timeout_value, depth):
    driver.get(link)

    if depth < MAX_DEPTH:
        types_tag = WebDriverWait(driver, timeout_value).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div[1]/div[1]/div[2]/div/div"))
        )

        #print("here")
        
        # Locate all ul elements inside the div
        a_elements = types_tag.find_elements(By.TAG_NAME, "a")

        # Iterate through each tags --> save tags to iterate later  
        for a_element in a_elements:
            # Get the href attribute value
            href_value = a_element.get_attribute('href')

            if type(href_value) is type(None):
                continue

            tag = unquote(href_value.split("/")[-1])

            # check if this tag is crawled
            if check_tag_available(tag) == False:
                continue

            # print(f"href_value: {href_value}, span text: {tag}")

            tags_to_crawl.append((tag, depth + 1))

    #print("finish tags")
        
    # Iterate through stories
    #time.sleep(1000)

    story_titles = WebDriverWait(driver, timeout_value).until(
        EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[4]/div/div[1]/div[2]/main/div/article/div[1]/div/div/a"))
    )

    for story_title in story_titles:
        href_value = story_title.get_attribute('href')

        # key = story_title.text

        # check if this story is crawled
        if check_story_available(href_value) == False:
            continue

        stories_to_crawl.append((href_value, 0))  

    while stories_to_crawl:
        story_link, depth = stories_to_crawl.pop(0)

        print(f"story link: {story_link}")

        # check if this story is crawled
        if check_story_available(story_link) == False:
            continue

        # print(f"story: {story_link}")

        story_crawling(driver=driver, link=story_link, timeout_value=100, depth=depth)        

    #time.sleep(1000)

    return driver