import os                          #for the access to make folder
import requests                    #request of url
import time                        # for the time
from selenium import webdriver     #using driver
from selenium.webdriver.common.by import By     # for tags
import pandas as pd # for the csv


def extract_data(driver, folder):       # extracting data using the drivers
    img_sources = []
    videos = []
    links = []
    texts = []

    # Extract image sources
    for img in driver.find_elements(By.TAG_NAME, 'img'):
        img_url = img.get_attribute('src')
        img_sources.append(img_url)
        download_image(img_url, folder)

    # Extract videos
    for video in driver.find_elements(By.TAG_NAME, 'video'):
        video_url = video.get_attribute('src')
        videos.append(video_url)
    # Extract videos from iframe tags
    for iframe in driver.find_elements(By.TAG_NAME, 'iframe'):
        if iframe.get_attribute('src'):
            videos.append(iframe.get_attribute('src'))

    # Extract links
    for link in driver.find_elements(By.TAG_NAME, 'a'):
        link_url = link.get_attribute('href')
        links.append(link_url)

    # Extract text
    for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div']:
        for element in driver.find_elements(By.TAG_NAME, tag):
            texts.append(element.text)

    return img_sources, videos, links, texts

def download_image(url, folder):
    try:
        filename = os.path.join(folder, url.split('/')[-1].split('?')[0])   #url and check for null
        with open(filename, 'wb') as f:
            response = requests.get(url)
            if response.status_code == 200:         # status ok
                f.write(response.content)
            else:
                print(f"Failed to download image from {url}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {url}: {e}")
    except FileNotFoundError as e:
        print(f"Error: The specified folder '{folder}' does not exist.")

def save_to_csv(data, filename):                                # make file and data into the file
    df = pd.DataFrame(data, columns=['Value'])
    df.to_csv(filename, index=True)
    print(f"Data saved to {filename}")


def scroll_to_bottom(driver):
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait for some time for the new content to load
    time.sleep(2)

def scrape_and_save(url, folder):
    options = webdriver.ChromeOptions()  # using chorme drivers
    options.add_argument('headless')  # like without CSS in the webpage
    driver = webdriver.Chrome(options=options)  # using driver to control
    driver.get(url)

    try:
        # Scroll to the bottom of the page
        for _ in range(5):
            scroll_to_bottom(driver)
            img_sources, videos, links, texts = extract_data(driver, folder)


        save_to_csv(img_sources, 'image_data.csv')
        save_to_csv(videos, 'video_data.csv')
        save_to_csv(links, 'link_data.csv')
        save_to_csv(texts, 'text_data.csv')
    finally:
        driver.quit()

if __name__ == "__main__":
    url = 'https://mastodon.social/explore'
    folder = 'images'
    if not os.path.exists(folder):
        os.makedirs(folder)
    scrape_and_save(url, folder)




# Author: OpenAI's GPT-3.5 model
# Code Title: Web Scraping Script with Selenium
