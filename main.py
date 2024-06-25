from dotenv import load_dotenv
import os
import time, os 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
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
            except TimeoutException:
                print("TimeoutException: Could not find login fields")
                exit()
            except KeyboardInterrupt:
                print("KeyboardInterrupt: Exiting")
                pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
                exit()
    def work(self):
        time.sleep(50)
        pass

if __name__ == "__main__" :
    load_dotenv()
    LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
    LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
    assert LINKEDIN_USERNAME, "Please set the LINKEDIN_USERNAME environment variable"
    assert LINKEDIN_PASSWORD, "Please set the LINKEDIN_PASSWORD environment variable"
    bot = LinkedinBot(LINKEDIN_USERNAME, LINKEDIN_PASSWORD)
    bot.work()

