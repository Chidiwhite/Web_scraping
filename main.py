from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from time import sleep

class Monitor(webdriver.Chrome):
    def __init__(self, driver_path = r"C:/SeleniumWebdrivers/chromedriver.exe"):
        # Add chrome options
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-blink-features=AutomationControlleD") 
        chrome_options.add_argument("--disable-notifications")
        # Adding chrome profile path
        chrome_options.add_argument("user-data-dir=/Users/H-P/AppData/Local/Google/Chrome/User Data/Default") 
        chrome_options.add_argument("profile-directory=chidi")
        self.driver_path = driver_path
        self.service = Service(self.driver_path)
        super(Monitor, self).__init__(service=self.service, options=chrome_options)

    def data_file(self):
        # Read data from 'info.csv' file into a DataFrame
        df = pd.read_csv('info.csv')
        return df

    def land_first_page(self):
        # Open the Facebook Marketplace page
        self.get("https://wwww.facebook.com/marketplace")
        self.implicitly_wait(10)

    def search_product(self):
        # Search for a product based on the data from the CSV file
        search_bar = self.find_element(By.XPATH, "//input[@aria-label='Search Marketplace']")
        sleep(1)
        df = self.data_file()
        search_bar.send_keys(df.loc[0, 'product'])
        sleep(1)
        search_bar.send_keys(Keys.ENTER)

    def notify(self):
        try:
            # Click the "Notify Me" button if it exists
            notify_button = self.find_element(By.XPATH, "//div[@aria-label='Notify Me']")
            notify_button.click()
        except:
            # If "Notify Me" button does not exist, click the "Edit Alert" button to update the alert
            edit = self.find_element(By.XPATH, "//div[@aria-label='Edit Alert']")
            edit.click()
    
    def price(self):
        # Set the price range for the alert based on data from the CSV file
        notify_box = self.find_element(By.XPATH, "//div[@class='x1yztbdb']")
        data = self.data_file()
        min_price = notify_box.find_element(By.XPATH, ".//input[@aria-label='Minimum range']")
        max_price = notify_box.find_element(By.XPATH, ".//input[@aria-label='Maximum range']")
        min_price.clear()
        sleep(2)
        max_price.clear()
        sleep(2)
        min_price.send_keys(str(data.loc[0, 'min_price']))
        sleep(2)
        max_price.send_keys(str(data.loc[0, 'max_price']))
        
    def location_filters(self):
        # Set location filters for the alert based on data from the CSV file
        df = self.data_file()
        location_box = self.find_element(By.XPATH, "//div[@class='xp7jhwk x1n0m28w']")
        location_box.click()
        self.implicitly_wait(3)
        location_input = self.find_element(By.XPATH, "//label[@aria-label='Location']")
        location_input.send_keys(str(df.loc[0, 'state']))
        sleep(2)
        location_list_box = self.find_element(By.XPATH, "//ul[contains(@aria-label, 'suggested searches')]")
        try:
            # If the suggested locations are available, select the first one from the list
            location_list_box = self.find_element(By.XPATH, "//ul[contains(@aria-label, 'suggested searches')]")
            location_list = location_list_box.find_elements(By.TAG_NAME, "li")
            location_list[0].click()
        except:
            # If no suggested locations are available, try another method to locate the element and click it
            location_list = self.find_element(By.XPATH, "//div[@class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x78zum5 x1a2a7pz xh8yej3']")
            location_list.click()

    def Radius(self):
        # Set the distance radius for the alert based on data from the CSV file
        df = self.data_file()
        dis = str(df.loc[0, 'kilometer'])
        distance_box = self.find_element(By.XPATH, "//label[@aria-label='Radius']")
        distance_box.click()
        sleep(3)
        self.execute_script("window.scrollBy(0, 100);")
        radii_box = self.find_element(By.XPATH, "//div[@class='x1qjc9v5 x3vj7og x78zum5 xdt5ytf x1n2onr6 x1al4vs7']")
        radii = radii_box.find_element(By.XPATH, f".//span[contains(text(), '{dis}')]")
        radii.click()
        
    def save(self):
        # Click the "Save" button to save the alert settings
        _save = self.find_element(By.XPATH, "//div[@aria-label='Save']")
        _save.click()
        
    def create_alert(self):
        try:
            # Click the "Create Alert" button if it exists
            alert = self.find_element(By.XPATH, "//div[@aria-label='Create Alert']")
            alert.click()
        except:
            # If "Create Alert" button does not exist, click the "Update Alert" button to update the alert
            update = self.find_element(By.XPATH, "//div[aria-label='Update Alert']")
            update.click()

    def run(self):
        # Run the Facebook Marketplace alert monitor
        self.land_first_page()
        self.search_product()
        self.notify()
        self.price()
        self.location_filters()
        self.Radius()
        self.save()
        self.create_alert()
        print("Alert created successfully")
        sleep(5)

if __name__ == '__main__':
    Monitor().run()
