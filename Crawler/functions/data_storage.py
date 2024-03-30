import json

tags_crawled = []
tags_to_crawl = []

stories_crawled = []
stories_to_crawl = []

def check_tag_available(tag):
    return not(tag in tags_crawled)

def check_story_available(story):
    return not(story in stories_crawled)

JSON_DB_PATH = './story_data.json'
MAX_DEPTH = 1

def clear_db():
    with open(JSON_DB_PATH, "w") as f:
        pass
    
    with open(JSON_DB_PATH, "a") as f:
        f.write("[")

def append_data(record):
    with open(JSON_DB_PATH, "a") as f:
        f.write("\n")
        json.dump(record, f)
        f.write(",")

def reopen_db():
    # Read the content of the file
    with open(JSON_DB_PATH, 'r') as file:
        content = file.read()

    # Replace the last character with ']'
    if content:
        content = content[:-1] + ','
    else:
        content = "["

    # Write the modified content back to the file
    with open(JSON_DB_PATH, 'w') as file:
        file.write(content)


def close_db():
    # Read the content of the file
    with open(JSON_DB_PATH, 'r') as file:
        content = file.read()

    # Replace the last character with ']'
    if content:
        content = content[:-1] + ']'

    # Write the modified content back to the file
    with open(JSON_DB_PATH, 'w') as file:
        file.write(content)

def old_stories():
    with open(JSON_DB_PATH, 'r') as file:
        global stories_crawled, stories_to_crawl
        data = json.load(file)

        if data:
            global stories_crawled, stories_to_crawl, tags_crawled, tags_to_crawl

            stories_crawled.clear()
            stories_to_crawl.clear()
            
            tags_to_crawl.clear()
            tags_crawled.clear()
            # Extract all "a" values using list comprehension
            full_stories_to_crawl = [item for item in data]

            while full_stories_to_crawl:
                current = full_stories_to_crawl.pop(0)

                # add to crawled stories
                stories_crawled.append(current["link"])

                # add all recommended stories to story_to_crawl
                if "recommended_stories" in current:
                    recommended = current["recommended_stories"]
                    depth = current["depth"]

                    while recommended:
                        each_rec = recommended.pop(0)
                        stories_to_crawl.append((each_rec, depth + 1))


        #print(f"inside func: {stories_crawled}")

old_stories()