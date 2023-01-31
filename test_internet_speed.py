import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
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
        self.results = None
        self.run_test()
        self.tweet_at_provider()

    def run_test(self):
        time.sleep(2)
        run_test_button = self.driver.find_element(by=By.CSS_SELECTOR, value=('a[aria-label="start speed test - '
                                                                              'connection type multi"]'))
        run_test_button.click()
        self.get_speed_results()

    def get_speed_results(self):
        while not self.results:
            time.sleep(3)
            try:
                download_speed_el = self.driver.find_element(by=By.CSS_SELECTOR, value='span[class="result-data-large '
                                                                                       'number result-data-value '
                                                                                       'download-speed"]')
                upload_speed_el = self.driver.find_element(by=By.CSS_SELECTOR, value='span[class="result-data-large '
                                                                                     'number result-data-value '
                                                                                     'upload-speed"]')
            except NoSuchElementException:
                pass
            else:
                if download_speed_el.text != "--" and upload_speed_el.text != "--":
                    data_sponsor_el = self.driver.find_element(By.CSS_SELECTOR, value='a[class="js-data-sponsor"]')
                    isp_el = self.driver.find_element(By.CSS_SELECTOR, value=('div[class="result-label '
                                                                              'js-data-isp"]'))
                    self.results = dict(download=float(download_speed_el.text),
                                        upload=float(upload_speed_el.text),
                                        data_sponsor=data_sponsor_el.text,
                                        isp=isp_el.text)

    def tweet_at_provider(self):
        print("Will tweet results...")
