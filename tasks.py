from nytimes import NyTimes

from RPA.Browser.Selenium import Selenium

browser = Selenium()
from time import sleep


def main():
    try:
        nt = NyTimes(browser, ['Business'], 3, "usa")
        nt.set_section()
        nt.set_data_range()
        nt.set_search_query()
        nt.get_results()
    finally:
        browser.close_all_browsers()

if __name__ == "__main__":
    main()
