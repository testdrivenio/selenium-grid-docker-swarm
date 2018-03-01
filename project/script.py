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
    browser = get_driver()
    data = run_process(browser, sys.argv[1])
    browser.quit()
    print(f'Finished page {sys.argv[1]}')
