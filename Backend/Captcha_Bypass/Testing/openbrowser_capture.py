from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import mss
from mss import tools

# Step 1: Configure Chrome in Selenium
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Ensure consistent layout

driver = webdriver.Chrome(options=chrome_options)

# Step 2: Open the target URL
driver.get("https://scr.sci.gov.in/scrsearch/")

# Step 3: Wait for CAPTCHA image to load
# Increase delay if your system is slow or network latency is high
time.sleep(5)

# Optional: Ensure image is loaded
try:
    captcha = driver.find_element(By.ID, "captcha_image")
    print("CAPTCHA image found.")
except:
    print("CAPTCHA image not found.")
    driver.quit()
    exit()

# Step 4: Take region screenshot using mss
# Adjust the values (top, left) based on DevTools measurement
monitor = {"top": 784, "left": 662, "width": 140, "height": 40}

with mss.mss() as sct:
    sct_img = sct.grab(monitor)
    tools.to_png(sct_img.rgb, sct_img.size, output="region_capture.png")
    print("Screenshot saved as region_capture.png")

# Optional: driver.quit()
