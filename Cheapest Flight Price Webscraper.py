from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup



chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#Optional arguments to run code headless with  basic cookie detection bypass arguements. Comment these out to run program headless
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
chrome_options.add_argument('log-level=3')


#Driver Initialization
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver,5)

#Website Access
driver.get("https://flyflair.com/")
driver.implicitly_wait(10)

#Beginning the process of inputting correct data fields to each desired page
pop_up = driver.find_element(By.XPATH, "//button[text()='english']").click()
driver.find_element(By.XPATH,"//input[@placeholder='from']").click()
driver.find_element(By.XPATH,"//input[@placeholder='from']").send_keys("toronto")
tnt_element = wait.until(EC.element_to_be_clickable((By.XPATH,"//span[text()='toronto']")))
tnt_element.click()

time.sleep(1)

driver.find_element(By.XPATH,"//input[@placeholder='to']").click()
driver.find_element(By.XPATH,"//input[@placeholder='from']").send_keys("winnipeg")
driver.find_element(By.XPATH,"//span[text()='winnipeg']").click()


current = driver.find_element(By.XPATH,"//div[@class='DayPicker-Caption']").text
time.sleep(1)

while current != "august 2024":
    calendar_element= wait.until(EC.visibility_of_element_located((By.XPATH,"//span[@aria-label='Next Month']")))
    calendar_element.click()
    #driver.find_element(By.XPATH,"//span[@aria-label='Next Month']").click()
    current = driver.find_element(By.XPATH,"//div[@class='DayPicker-Caption']").text

time.sleep(2)

driver_element_from= wait.until(EC.element_to_be_clickable((By.XPATH,"//span[text()='28']")))
driver_element_from.click()

while current != "september 2024":
    calendar_element= wait.until(EC.visibility_of_element_located((By.XPATH,"//span[@aria-label='Next Month']")))
    calendar_element.click()
    current = driver.find_element(By.XPATH,"//div[@class='DayPicker-Caption']").text

time.sleep(1)

driver_element_to= wait.until(EC.element_to_be_clickable((By.XPATH,"//span[text()='2']")))
driver_element_to.click()
done_element = wait.until(EC.element_to_be_clickable((By.XPATH,"//span[text()='done']")))
done_element.click()
search_flights=wait.until(EC.element_to_be_clickable((By.XPATH,"//span[text()='search flights']")))
search_flights.click()


#Beginning of page redirect. Implement simple window switch for diver
time.sleep(2)
win1 = driver.current_window_handle
winlist = driver.window_handles
winlist.remove(win1)
driver.switch_to.window(winlist[0])

#Locate the lowest prices found inside flight prices page
startdate_button = driver.find_element(By.XPATH,"//button[@data-testid='date-8/28/2024']")
startdate_price = startdate_button.find_element(By.XPATH,"//div[@class='dv2__booking-carousel-item__price']")
startdate_price.get_attribute("innerHTML").replace('$','')

departdate_button = startdate_button = driver.find_element(By.XPATH,"//button[@data-testid='date-9/2/2024']")
departdate_price = startdate_button.find_element(By.XPATH,"//div[@class='dv2__booking-carousel-item__price']")

#Output the cheapest flight available to the command terminal line
print("Cheapest Flight is: $" + str(float(startdate_price.get_attribute("innerHTML").replace('$','')) + float(departdate_price.get_attribute("innerHTML").replace('$',''))))

#Close driver to free up resources
time.sleep(1)
driver.quit()
