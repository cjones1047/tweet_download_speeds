import time
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import dotenv


class TestInternetSpeed:

    def __init__(self):
        dotenv.load_dotenv()
        self.twitter_email = os.getenv("TWITTER_EMAIL")
        self.twitter_username = os.getenv("TWITTER_USERNAME")
        self.twitter_password = os.getenv("TWITTER_PASSWORD")
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
                    time.sleep(2)
                    isp_el = self.driver.find_element(By.CSS_SELECTOR, value=('div[class="result-label '
                                                                              'js-data-isp"]'))
                    self.results = dict(download=float(download_speed_el.text),
                                        upload=float(upload_speed_el.text),
                                        isp=isp_el.text)
                    print(self.results)

    def tweet_at_provider(self):
        self.driver.execute_script("window.open('');")
        twitter_tab = self.driver.window_handles[1]
        self.driver.switch_to.window(twitter_tab)
        self.driver.get("https://twitter.com/")
        time.sleep(3)
        login_el = self.driver.find_element(by=By.CSS_SELECTOR, value='a[href="/login"]')
        login_el.click()
        time.sleep(1)
        username_input_el = self.driver.find_element(by=By.CSS_SELECTOR, value='input[autocomplete="username"]')
        username_input_el.click()
        username_input_el.send_keys(self.twitter_email, Keys.ENTER)
        time.sleep(1)
        username_confirm_el = self.driver.find_element(by=By.CSS_SELECTOR, value='input[data-testid='
                                                                                 '"ocfEnterTextTextInput"]')
        username_confirm_el.click()
        username_confirm_el.send_keys(self.twitter_username, Keys.ENTER)
        time.sleep(1)
        password_input_el = self.driver.find_element(by=By.CSS_SELECTOR, value='input[autocomplete="current-password"]')
        password_input_el.click()
        password_input_el.send_keys(self.twitter_password, Keys.ENTER)
        time.sleep(3)
        tweet_text_el = self.driver.find_element(by=By.CSS_SELECTOR, value='div[aria-label="Tweet text"]')
        tweet_text_el.click()

        message = (f"Hey @{self.results['isp'].title()} thanks for following "
                   f"through on download/upload speeds of {self.results['download']}/{self.results['upload']} mbps. "
                   f"I won't be looking anywhere else for internet.")

        tweet_text_el.send_keys(message)
        tweet_button_el = self.driver.find_element(by=By.CSS_SELECTOR, value='div[data-testid="tweetButtonInline"]')
        tweet_button_el.click()
