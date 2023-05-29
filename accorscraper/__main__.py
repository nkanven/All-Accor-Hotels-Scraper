from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        self.image_prefix = ["ro", "sm", "br", "ba", "", "sl", "fe", "de", "sw"]

        self.start_url = "https://all.accor.com/gb/world/hotels-accor-monde.shtml"
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_argument("--headless")
        self.path = Service("chromedriver")
        self.driver = webdriver.Chrome(service=self.path, options=self.chrome_options)
        self.world_url = None
        self.parse_url = []
        self.city_url = ""

        self.driver.get(self.start_url)

        try:
            self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        except Exception:
            pass

    def launch(self) -> None:
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        urls = soup.find_all(class_="Teaser-link")
        for url in urls:
            href = url.get("href")
            print(href)
            self.driver.get(href)
            if href.find("/hotel/") != -1:
                self.get_hotel_details()
            self.launch()


    def get_hotels(self, city_url):
        self.driver.get(city_url)

    def get_hotel_details(self):
        details = {
            "hotel name": self.check_element("hotel--name"),
            "location": self.check_element("presentation__location"),
            "description": self.check_element("hotel-description", By.ID),
            "extra": self.check_element("extras__content"),
            "infos": self.check_element("infos__content")
        }
        print(details)

    def check_element(self, tag_name, by=By.CLASS_NAME):
        result = None
        try:
            result = self.driver.find_element(by, tag_name).text
        except NoSuchElementException:
            pass
        return result


sc = Scraper()
sc.launch()
