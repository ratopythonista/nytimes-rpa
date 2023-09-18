import re
from time import sleep
from datetime import date, timedelta

import requests
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

NYTIMES_SEARCH_URL = "nytimes.com/search"

class NyTimes:
    def __init__(self, browser: Selenium, section_list: list, months: int, query: str) -> None:
        self.browser = browser
        self.section_list = section_list
        self.months = months
        self.query = query
        self.browser.open_available_browser(NYTIMES_SEARCH_URL)
        sleep(3)
        self.__by_pass_complience()
        self.__strip_site()

    def __by_pass_complience(self):
        overlay = self.browser.get_webelement("id:complianceOverlay")
        button: WebElement = self.browser.get_webelement("tag:button", overlay)
        button.click()

    def __strip_site(self):
        self.data_range: WebElement = self.browser.get_webelement('xpath://button[@data-testid="search-date-dropdown-a"]')
        self.section: WebElement = self.browser.get_webelement('xpath://button[@data-testid="search-multiselect-button"]')
        sleep(2)

    def set_section(self):
        self.section.click()
        sleep(1)
        section_options = self.browser.get_webelement('xpath://ul[@data-testid="multi-select-dropdown-list"]')
        element: WebElement
        section_options_map = {}
        for element in self.browser.find_elements('xpath://input[@data-testid="DropdownLabelCheckbox"]', section_options):
            section_options_map[element.get_attribute("value").split("|")[0]] = element
        for section_to_select in self.section_list:
            section_option: WebElement = section_options_map.get(section_to_select)
            if section_option:
                section_option.click()
        sleep(1)

    def set_data_range(self):
        today = date.today()
        months = 1 if self.months <= 1 else self.months
        start_date = today - timedelta(days=30*months)
        self.data_range.click()
        specific_dates: WebElement = self.browser.get_webelement('xpath://button[@aria-label="Specific Dates"]')
        specific_dates.click()
        self.browser.input_text('id:startDate', start_date.strftime("%m/%d/%Y"))
        self.browser.input_text('id:endDate', today.strftime("%m/%d/%Y"))
        self.browser.press_keys('id:endDate', "ENTER")

    def set_search_query(self):
        input_field = "id:searchTextField"        
        self.browser.input_text(input_field, self.query)
        self.browser.press_keys(input_field, "ENTER")
        sleep(5)

    def get_results(self):
        search_result: list[WebElement] = self.browser.get_webelements('xpath://li[@data-testid="search-bodega-result"]')
        news_csv = f"news-{self.query.replace(' ', '_')}-{self.months}-{'_'.join(self.section_list)}.csv"
        for content in search_result:
            date = content.find_element(By.TAG_NAME, "span").text
            title = content.find_element(By.TAG_NAME, "h4").text
            image = content.find_elements(By.TAG_NAME, "img")
            section, description, author = [p.text for p in content.find_elements(By.TAG_NAME, "p")]
            image_title = ""
            if image:
                image_title = f"images/{title.replace(' ', '-')}.jpg"
                url = image[0].get_attribute("src")
                response = requests.get(url)
                with open(image_title, "wb") as f:
                    f.write(response.content)
            title_on_description = description.count(title)
            money_on_title_or_description = re.findall(
                r'\$\d+\.\d+|\$[\d{1,3}\,]*\.\d{2}|\d+\sdollars|\d+\sUSD', title + description
            )
            with open(news_csv, "a") as f:
                f.write(f"""{';'.join([
                    title, date, description, image_title, 
                    str(title_on_description), str(bool(money_on_title_or_description))
                ])}\n""")

            