import sys
from time import sleep

from scrapers.scraper import get_driver, connect_to_base, parse_html


def run_process(browser, page_number=1):
    if connect_to_base(browser, page_number):
        print(f'Scraping page {page_number}...')
        sleep(2)
        html = browser.page_source
        return parse_html(html)
    else:
        return False


if __name__ == '__main__':
    try:
        # get driver
        browser = get_driver()
        # scrape and crawl
        data = run_process(browser, sys.argv[1])
        # exit
        browser.quit()
        # output
        print(data[0])
    except Exception as e:
        print(e)
