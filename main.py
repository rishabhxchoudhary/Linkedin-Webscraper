from dotenv import load_dotenv
import os
import time, os 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import random
import pickle

retrieveCookies = False
driver = webdriver.Chrome()

stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

class LinkedinBot:
    MAX_SEARCH_TIME = 10 * 60 * 60 # can change this to be longer or shorter
    def __init__(self,username=None,password=None):
        self.username = username
        self.password = password

        self.options = self.browser_options()
        self.browser = driver
        self.browser.set_window_position(1, 1)
        self.browser.maximize_window()
        self.wait = WebDriverWait(self.browser, 5)

        self.authenticate(username, password)

    def browser_options(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        return options

    def authenticate(self, username, password):
        self.browser.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
        if not retrieveCookies:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            print("Logged in to Linkedin Using Cookies")
        else:
            try:
                user_field = self.browser.find_element("id","username")
                pw_field = self.browser.find_element("id","password")
                login_button = self.browser.find_element("xpath", '//*[@id="organic-div"]/form/div[3]/button')
                user_field.send_keys(username)
                user_field.send_keys(Keys.TAB)
                time.sleep(0.25)
                pw_field.send_keys(password)
                time.sleep(0.25)
                login_button.click()
                time.sleep(0.25)
                print("Logged in to Linkedin using credentials.")
                pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
                print("Rerun the script with retrieveCookies = False to use cookies next time.")
                exit()
            except TimeoutException:
                print("TimeoutException: Could not find login fields")
                exit()
            except KeyboardInterrupt:
                print("KeyboardInterrupt: Exiting")
                pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
                exit()
    def work(self,num_pages):
        for n in range(1, num_pages+1):
            self.browser.get("https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=FACETED_SEARCH&page=" + str(n))
            time.sleep(2)
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            message_buttons = [btn for btn in all_buttons if btn.text == "Message"]
            for i in range(len(message_buttons)):
                self.browser.execute_script("arguments[0].click();", message_buttons[i])
                time.sleep(2)

                main_div = self.browser.find_element("xpath", "//div[starts-with(@class, 'msg-form__msg-content-container')]")
                self.browser.execute_script("arguments[0].click();", main_div)

                paragraphs = self.browser.find_elements(By.TAG_NAME, "p")
                all_span = self.browser.find_elements(By.TAG_NAME, "span")
                all_span = [s for s in all_span if s.get_attribute("aria-hidden") == "true"]

                idx = [*range(3,23,2)]
                greetings = ["Hello", "Hi", "Hey", "Ahoy", "Yo yo", "Sup"]
                all_names = []
                
                for j in idx:
                    name = all_span[j].text.split(" ")[0]
                    all_names.append(name)
                    
                greetings_idx = random.randint(0, len(greetings)-1)
                message = greetings[greetings_idx] + " " + all_names[i] + ", Sorry, I didn't mean to bother you, I'm just building a Linkedin Web Scraper Bot and testing its' capabilities."
                paragraphs[-5].clear()
                paragraphs[-5].send_keys(message)
                time.sleep(2)

                close_button = driver.find_element(By.XPATH, "//button[.//span[text()='Close your draft conversation']]")
                self.browser.execute_script("arguments[0].click();", close_button)
                try:
                    discard_button = driver.find_element(By.XPATH, "//button[.//span[text()='Discard']]")
                    self.browser.execute_script("arguments[0].click();", discard_button)
                    time.sleep(2)
                except:
                    pass
        pass

if __name__ == "__main__" :
    load_dotenv()
    LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
    LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
    assert LINKEDIN_USERNAME, "Please set the LINKEDIN_USERNAME environment variable"
    assert LINKEDIN_PASSWORD, "Please set the LINKEDIN_PASSWORD environment variable"
    bot = LinkedinBot(LINKEDIN_USERNAME, LINKEDIN_PASSWORD)
    bot.work(100)

