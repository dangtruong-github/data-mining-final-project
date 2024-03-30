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

def crawl_tags(left_container, timeout_value, depth):
    print("crawl tags of story")
    
    # Iterate through tags
    story_tags_wrapper = None

    try:
        story_tags_wrapper = WebDriverWait(left_container, timeout_value).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tag-items"))
        )
    except Exception as e:
        print(f"Error getting tags wrapper: {e}")
        return None

    story_tags = None
    try:
        story_tags = story_tags_wrapper.find_elements(By.TAG_NAME, "a")
    except Exception as e:
        print(f"Error getting a elem inside tags: {story_tags}")
        return None

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
        print("Error getting recommended stories", e)
        return None
    
    #time.sleep(1000)

    story_titles = None

    try: 
        story_titles = story_titles_wrapper.find_elements(By.TAG_NAME, "a")
        story_titles = WebDriverWait(story_titles_wrapper, timeout=timeout_value).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "clearfix"))
        )
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
            if check_story_available(href_value) == False or depth >= MAX_DEPTH:
                continue

            #print(f"href: {href_value}")

            stories_to_crawl.append((href_value, depth + 1))  
        except:
            continue

    print(f"Number of recommended stories: {len(recommended_stories)}")

    #time.sleep(1000)

    return recommended_stories

def story_crawling(driver, link, timeout_value, depth):
    if check_story_available(link) == False:
        return driver
    else:
        stories_crawled.append(link)
    
    driver.get(link)

    stories_data = {}
    stories_data["link"] = link
    stories_data["depth"] = depth

    #time.sleep(1000)

    left_container = None
    try: 
        left_container = WebDriverWait(driver, timeout=timeout_value).until(
            EC.presence_of_element_located((By.CLASS_NAME, "left-container"))
        )
    except Exception as e:
        print(f"error geting left container, {e}")
        return driver
        
    story_tags_list = crawl_tags(left_container=left_container, timeout_value=timeout_value, depth=depth)

    if type(story_tags_list) != type(None):
        stories_data["story_tags_list"] = story_tags_list

    # Crawl data from each individual story
    
    print("Start crawling story")

    story_info_wrapper = None
    try:
        story_info_wrapper = WebDriverWait(driver, timeout_value).until(
            EC.presence_of_element_located((By.CLASS_NAME, "story-header"))
        )
    except Exception as e:
        print(f"Error getting story info: {e}")
        return driver

    # Cover image
    try: 
        cover_img_wrapper = WebDriverWait(story_info_wrapper, timeout_value).until(
            EC.presence_of_element_located((By.CLASS_NAME, "story-cover"))
        )

        cover_img_tag = WebDriverWait(cover_img_wrapper, timeout_value).until(
            EC.presence_of_element_located((By.TAG_NAME, "img"))
        )
        
        cover_img = cover_img_tag.get_attribute('src')
        stories_data["cover_img"] = cover_img
        # print(f"Cover img: {cover_img}")
    except:
        pass

    # Title
    try:
        title_wrapper = WebDriverWait(story_info_wrapper, timeout_value).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sr-only"))
        )

        title = title_wrapper.text
        stories_data["title"] = title
        # print(f"Story title: {title}")
    except:
        pass

    # Story bagdes
    #story-badges
    print("crawl to badges")

    try:
        pass 
        story_badges_wrapper = WebDriverWait(left_container, timeout_value).until(
            EC.presence_of_element_located((By.CLASS_NAME, "story-badges"))
        )

        story_badges = WebDriverWait(story_badges_wrapper, timeout_value).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "tag-item"))
        )

        badges = []

        for each_badge in story_badges:
            badges.append(each_badge.text) 
        
        stories_data["badges"] = badges
    except:
        pass
    
    # Stats
    print("crawl to stats")
    try: 
        stats_wrapper = WebDriverWait(story_info_wrapper, timeout_value).until(
            EC.presence_of_element_located((By.TAG_NAME, "ul"))
        )

        stats_full = WebDriverWait(stats_wrapper, timeout_value).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "stats-item"))
        )

        for each_stat in stats_full:
            each_stat_span = each_stat.find_elements(By.TAG_NAME, "span")
            each_stat_title = each_stat_span[0].text
            each_stat_data = each_stat_span[1].text
            stories_data[each_stat_title] = each_stat_data
    except:
        pass

    if depth < MAX_DEPTH:
        recommended_stories = crawl_recommended_stories(driver=driver, timeout_value=timeout_value, depth=depth)
        
        if type(recommended_stories) != type(None):
            stories_data["recommended_stories"] = recommended_stories

    #print(f"{each_stat_title}: {each_stat_data}")
    reopen_db()
    append_data(stories_data)
    close_db()
    print("appended data")

    #time.sleep(1000)
    return driver