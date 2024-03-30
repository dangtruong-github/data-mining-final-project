from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import os
import time
from urllib.parse import unquote
from .data_storage import tags_crawled, tags_to_crawl, stories_crawled, stories_to_crawl, check_story_available, check_tag_available, MAX_DEPTH
from .story_crawling_test import story_crawling

def stories_from_tags(driver, link, timeout_value, depth):
    driver.get(link)

    # crawl tags
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

    print("finish tags of tags")
        
    # Iterate through stories
    #time.sleep(1000)

    stories_wrapper = None
    try:
        stories_wrapper = WebDriverWait(driver, timeout=timeout_value).until(
            EC.presence_of_element_located((By.CLASS_NAME, "browse-results"))
        )
    except Exception as e:
        print(e)

    story_titles = None
    try:
        story_titles = WebDriverWait(stories_wrapper, timeout_value).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "browse-story-item"))
        )
    except Exception as e:
        print(e)
    
    print(f"story titles: {len(story_titles)}")
    #time.sleep(1000)

    for story_title in story_titles:
        a_elem = None

        try:
            a_elem = WebDriverWait(story_title, timeout_value).until(
                EC.presence_of_element_located((By.TAG_NAME, "a"))
            )
        except Exception as e:
            print(f"Error getting a elem: {e}")
            continue

        href_value = None
        try:
            href_value = a_elem.get_attribute("href")
        except Exception as e:
            print(f"Error getting href: {e}")
            continue

        # key = story_title.text

        # check if this story is crawled
        if type(href_value) == type(None) or check_story_available(href_value) == False:
            continue

        stories_to_crawl.append((href_value, depth))  

    while stories_to_crawl:
        story_link, current_depth = stories_to_crawl.pop(0)

        print(f"story link: {story_link}")

        # check if this story is crawled
        if check_story_available(story_link) == False:
            continue

        # print(f"story: {story_link}")

        #stories_crawled.append(story_link)
        driver = story_crawling(driver=driver, link=story_link, timeout_value=100, depth=current_depth)        

    #time.sleep(1000)

    return driver