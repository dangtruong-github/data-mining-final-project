from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import os
import time
import json
from urllib.parse import unquote
from unidecode import unidecode
from .data_storage import tags_crawled, tags_to_crawl, stories_crawled, stories_to_crawl, check_story_available, check_tag_available, append_data, close_db, reopen_db, MAX_DEPTH

def crawl_tags(driver, timeout_value, depth):
    print("crawl tags of story")
    
    # Iterate through tags
    story_tags_wrapper = None

    try:
        story_tags_wrapper = WebDriverWait(driver, timeout_value).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tag-items"))
        )
    except Exception as e:
        print(f"Error: {e}")
        return None

    story_tags = None
    try:
        story_tags_wrapper.find_elements(By.TAG_NAME, "a")
    except Exception as e:
        print(f"Error getting a elem inside tags: {story_tags}")

    story_tags_list = []

    for story_tag in story_tags:
        #a_element = story_tag.find_element(By.TAG_NAME, "a")
        href_value = None
        try: 
            href_value = story_tag.get_attribute('href')

            tag = unquote(href_value.split("/")[-1])

            story_tags_list.append(tag)

            # check if this tag is crawled
            if check_tag_available(tag) == False or depth >= MAX_DEPTH:
                continue

            # print(f"href_value: {href_value}, span text: {tag}")

            tags_to_crawl.append((tag, depth + 1))
        except:
            continue

    return story_tags_list

def crawl_recommended_stories(driver, timeout_value, depth):
    print("crawl recommended stories")
        # Iterate through recommended stories
    story_titles_wrapper = None

    try:
        story_titles_wrapper = WebDriverWait(driver, timeout_value).until(
            EC.presence_of_element_located((By.CLASS_NAME, "story-list"))
        )
    except Exception as e:
        print("Error getting", e)
        return None

    #time.sleep(1000)

    #story_titles_wrapper = right_wrapper.find_element(By.CLASS_NAME, "story-list")

            # Retrieve the HTML code of the webpage
    #html_code = unidecode(driver.page_source)

    # Specify the file path where you want to save the text file
    #file_path = "./output.txt"

    # Open the file in write mode ('w')
    #with open(file_path, 'w') as file:
        # Write the string content to the file
        #file.write(html_code)

    #print(story_titles_wrapper, type(story_titles_wrapper))
    #time.sleep(1000)

    story_titles = None

    try: 
        story_titles = story_titles_wrapper.find_elements(By.TAG_NAME, "a")
    except Exception as e:
        print("Error: ", e)
        return None

    print("start crawling story titles")

    recommended_stories = []

    for story_title in story_titles:
        #print("crawling story titles")

        href_value = None

        try:
            href_value = story_title.get_attribute("href")            

            # key = story_title.text

            recommended_stories.append(href_value)

            # check if this story is crawled
            if check_story_available(href_value) == False:
                continue

            #print(f"href: {href_value}")

            stories_to_crawl.append((href_value, depth + 1))  
        except:
            continue

    return

def story_crawling(driver, link, timeout_value, depth):
    driver.get(link)

    stories_data = {}

    stories_data["link"] = link
    time.sleep(1000)

    story_tags_list = crawl_tags(driver=driver, timeout_value=timeout_value, depth=depth)

    if type(story_tags_list) != type(None):
        stories_data["story_tags_list"] = story_tags_list

    stories_data["depth"] = depth

    if depth < MAX_DEPTH:
        recommended_stories = crawl_recommended_stories(driver=driver, timeout_value=timeout_value, depth=depth)
        
        if type(recommended_stories) != type(None):
            stories_data["recommended_stories"] = recommended_stories
    # Crawl data from each individual story
    
    print("Start crawling story")

    # Cover image
    try: 
        cover_img_wrapper = WebDriverWait(driver, timeout_value).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div[1]/div[1]/img"))
        )

        cover_img = cover_img_wrapper.get_attribute('src')
        stories_data["cover_img"] = cover_img
        # print(f"Cover img: {cover_img}")
    except:
        pass

    # Title
    try:
        title_wrapper = WebDriverWait(driver, timeout_value).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div[1]/div[2]/span"))
        )

        title = title_wrapper.text
        stories_data["title"] = title
        # print(f"Story title: {title}")
    except:
        pass

    # Stats
    print("crawl to stats")
    try: 
        stats_full = WebDriverWait(driver, timeout_value).until(
            EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[4]/div/div/div/div[1]/div[2]/ul/li"))
        )

        for each_stat in stats_full:
            each_stat_span = each_stat.find_elements(By.TAG_NAME, "span")
            each_stat_title = each_stat_span[0].text
            each_stat_data = each_stat_span[1].text
            stories_data[each_stat_title] = each_stat_data
    except:
        pass
    
    #print(f"{each_stat_title}: {each_stat_data}")
    reopen_db()
    append_data(stories_data)
    close_db()
    print("appended data")

    return driver