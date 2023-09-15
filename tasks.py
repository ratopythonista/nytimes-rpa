from time import sleep
from datetime import date, timedelta

from RPA.Browser.Selenium import Selenium

browser_lib = Selenium()

def select_section(section_list: list):
    section_map = [
        'Arts', 'Business', 'Movies', 'New York',
        'Opinion', 'Sports', 'Travel', 'U.S.', 'World'
    ]

    browser_lib.click_button('//*[@id="site-content"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div/button')
    for section in section_list:
        section_xpath = lambda x: f'//*[@id="site-content"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/ul/li[{x}]/label/input'
        browser_lib.click_button(section_xpath(section_map.index(section) + 2))
    browser_lib.click_button('//*[@id="site-content"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div/button')

def select_data_range(months: int):
    today = date.today()
    months = 1 if months <= 1 else months
    start_date = today - timedelta(days=30*months)
    browser_lib.click_button('//*[@id="site-content"]/div[1]/div[1]/div[2]/div/div/div[1]/div/div/button/label')
    browser_lib.input_text('id:startDate', start_date.strftime("%m/%d/%Y"))
    browser_lib.input_text('id:endDate', today.strftime("%m/%d/%Y"))
    browser_lib.press_keys('id:endDate', "ENTER")

def open_the_website(url):
    browser_lib.open_available_browser(url)


def search_for(term):
    input_field = "id:searchTextField"
    browser_lib.input_text(input_field, term)
    browser_lib.press_keys(input_field, "ENTER")

def complience():
    browser_lib.click_button('//*[@id="complianceOverlay"]/div/button')

def store_screenshot(filename):
    browser_lib.screenshot(filename=filename)

def main():
    try:
        open_the_website("https://www.nytimes.com/search")
        sleep(1)
        complience()
        search_for("brazil")
        sleep(1)
        select_section(["Business"])
        sleep(1)
        select_data_range(3)
        sleep(1)
        store_screenshot("output/test.png")

    finally:
        browser_lib.close_all_browsers()

if __name__ == "__main__":
    main()
