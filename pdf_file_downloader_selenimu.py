from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0 Safari/537.36")
driver = webdriver.Chrome(options=options)

# Start Chrome
# driver = webdriver.Chrome()

page_url = 'https://www.biorxiv.org/content/10.1101/2025.07.10.664210v1'
# Load dynamic website
driver.get(page_url)

# Wait for JS to load
time.sleep(5)  # Better: use WebDriverWait

# Extract links
links = driver.find_elements(By.TAG_NAME, "a")
for link in links:
    print(link.get_attribute("href"))
    if str(link.get_attribute("href")).lower().endswith('.pdf'):
        print(link)

driver.quit()