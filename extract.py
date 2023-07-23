# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import openpyxl

# Path to the Chrome WebDriver
driver_path = "chromedriver.exe"

# Configure Chrome options for the WebDriver
chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-blink-features=AutomationControlleD")
chrome_options.add_argument("--disable-notifications")

# Initialize the Chrome WebDriver and set the URL of the website
services = Service(driver_path)
url = "http://www.google.com/"
keyword = input("Enter keyword: ")
driver = webdriver.Chrome(options=chrome_options, service=services)
driver.get(url)
sleep(2)

# Find the search bar using its ID and send the keyword
find_search_bar = driver.find_element(By.ID, 'APjFqb')
find_search_bar.send_keys(keyword)
find_search_bar.send_keys(Keys.ENTER)
driver.implicitly_wait(10)

# Click on 'More places' to load additional results
more = driver.find_element(By.XPATH, "//span[contains(text(), 'More places')]")
more.click()
sleep(2)

# Find all hotel boxes on the page
boxes = driver.find_elements(By.XPATH, "//div[@jscontroller='AtSb']")

# Get the total number of pages to scrape from the pagination element
page_count_container = driver.find_element(By.XPATH, "//tr[@jsname='TeSSVd']")
page = page_count_container.find_elements(By.TAG_NAME, 'td')
page_count = len(page) - 3

# Initialize an Excel workbook and sheet to store the extracted data
workbook = openpyxl.Workbook()
sheet = workbook.active

# Loop through each box on the page and extract hotel details
for box in boxes:
    each_hotel = box.find_element(By.XPATH, ".//a[1]").text
    hotel_list = each_hotel.split("\n")
    sheet.append(hotel_list)

# Save the extracted data to an Excel file
workbook.save('hotels.xlsx')

# Go to the next page and continue extraction for multiple pages
driver.find_element(By.XPATH, "//span[text()='Next']").click()
for idx, _ in enumerate(range(page_count)):
    driver.implicitly_wait(10)
    sleep(2)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    for box in boxes:
        try:
            each_hotel = box.find_element(By.XPATH, "//div[@class='rllt__details']").text
        except:
            sleep(3)
            # Wait for the element to be located in case of StaleElementReferenceException
            ignored_exceptions=(NoSuchElementException, StaleElementReferenceException,)
            wait = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='rllt__details']")))
            each_hotel = element.text
        hotel_list = each_hotel.split("\n")
        sheet.append(hotel_list)

    # Save the extracted data from each page to separate Excel files
    workbook.save('hotels' + str(idx) + '.xlsx')
    driver.find_element(By.XPATH, "//span[text()='Next']").click()

print("Extraction done")
