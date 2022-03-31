import sys
from time import sleep

from scrapers.scraper import get_driver, connect_to_base, parse_html



def run_process(rowser):
    if connect_to_base(browser):
        print(f'Scraping random Wikipedia page...')
        sleep(2)
        html = browser.page_source
        return parse_html(html)
    else:
        print("Error connecting to Wikipedia")
        return False


if __name__ == '__main__':
    browser = get_driver(sys.argv[1])
    data = run_process(browser)
    print(data)
    browser.quit()
    print(f'Finished!')