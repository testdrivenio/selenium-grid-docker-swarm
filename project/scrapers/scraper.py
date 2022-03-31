import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


def get_driver(address):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    # initialize driver
    driver = webdriver.Remote(
                command_executor=f'http://{address}:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME)
    return driver


def connect_to_base(browser):
    base_url = "https://en.wikipedia.org/wiki/Special:Random"
    connection_attempts = 0
    while connection_attempts < 3:
        try:
            browser.get(base_url)
            # wait for table element with id = 'content' to load
            # before returning True
            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.ID, "content"))
            )
            return True
        except Exception as e:
            print(e)
            connection_attempts += 1
            print(f"Error connecting to {base_url}.")
            print(f"Attempt #{connection_attempts}.")
    return False


def parse_html(html):
    # create soup object
    soup = BeautifulSoup(html, "html.parser")
    output_list = []
    # parse soup object to get wikipedia article url, title, and last modified date
    article_url = soup.find("link", {"rel": "canonical"})["href"]
    article_title = soup.find("h1", {"id": "firstHeading"}).text
    article_last_modified = soup.find("li", {"id": "footer-info-lastmod"}).text
    article_info = {
        "url": article_url,
        "title": article_title,
        "last_modified": article_last_modified,
    }
    output_list.append(article_info)
    return output_list


def get_load_time(article_url):
    try:
        # set headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
        }
        # make get request to article_url
        response = requests.get(
            article_url, headers=headers, stream=True, timeout=3.000
        )
        # get page load time
        load_time = response.elapsed.total_seconds()
    except Exception as e:
        print(e)
        load_time = "Loading Error"
    return load_time


def write_to_file(output_list, filename):
    for row in output_list:
        with open(Path(BASE_DIR).joinpath(filename), "a") as csvfile:
            fieldnames = ["url", "title", "last_modified"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(row)