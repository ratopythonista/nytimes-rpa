

from nytimes import NyTimes
from robocorp.tasks import task

from RPA.Browser.Selenium import Selenium

browser = Selenium()

@task
def download_nytimes_news():
    try:
        nt = NyTimes(browser, ['Business'], 3, "usa")
        nt.set_section()
        nt.set_data_range()
        nt.set_search_query()
        nt.get_results()
    finally:
        browser.close_all_browsers()
