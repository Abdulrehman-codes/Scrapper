import os                          #for the access to make folder
import requests                    #request of url
from bs4 import BeautifulSoup      # static page parser
from selenium import webdriver     #using driver
from selenium.webdriver.common.by import By     # for tags
import pandas as pd # for the csv

def get_html(url):
    response = requests.get(url)
    return response.text        #return url as plain text

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

def extract_data(html, folder):
    options = webdriver.ChromeOptions()     # using chorme drivers
    options.add_argument('headless')        # like without CSS in the webpage
    driver = webdriver.Chrome(options=options)  # using driver to control
    driver.get(url)

    soup = BeautifulSoup(html, 'html.parser')   # parsing the Static HTML to the library
    img_sources = []
    for img in soup.find_all('img', src=True):      # searching for the Tags
        img_url = img['src']
        img_sources.append(img_url)
        download_image(img_url, folder)
    videos = [video['src'] for video in soup.find_all('video', src=True)]   # searching for video tag

    for iframe in driver.find_elements(By.TAG_NAME, 'iframe'):
        if iframe.get_attribute('src'):
            videos.append(iframe.get_attribute('src'))

    links = [link['href'] for link in soup.find_all('a', href=True)]    # searching for the links
    texts = []
    for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div']:    # searching for texts
        texts.extend([text.get_text() for text in soup.find_all(tag)])
    return img_sources, videos, links, texts

def save_to_csv(data, filename):                                # make file and data into the file
    df = pd.DataFrame(data, columns=['Value'])
    df.to_csv(filename, index=True)
    print(f"Data saved to {filename}")

def scrape_and_save(url, folder):           # main calling of all functions
    html = get_html(url)
    img_sources, videos, links, texts = extract_data(html, folder)
    save_to_csv(img_sources, 'image_data.csv')
    save_to_csv(videos, 'video_data.csv')
    save_to_csv(links, 'link_data.csv')
    save_to_csv(texts, 'text_data.csv')

if __name__ == "__main__":
    url = 'https://www.politifact.com'
    folder = 'images'
    if not os.path.exists(folder):
        os.makedirs(folder)
    scrape_and_save(url, folder)


# Author: OpenAI's GPT-3.5 model
# Code Title: Web Scraping Script with BeautifulSoup and Selenium
