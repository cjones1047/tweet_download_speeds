import time
# from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class TestInternetSpeed:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        speed_test_url = "https://www.speedtest.net/"
        self.driver.get(speed_test_url)
        self.run_test()

    def run_test(self):
        time.sleep(2)
        run_test_button = self.driver.find_element(by=By.CSS_SELECTOR, value=('a[aria-label="start speed test - '
                                                                              'connection type multi"]'))
        run_test_button.click()
