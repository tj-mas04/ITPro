import os
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()

URL = "https://scr.sci.gov.in/scrsearch/vendor/securimage/securimage_show.php?017a03cb2d4936a7bb033b7ee2c693c3"
NUM_IMAGES = 25
SAVE_DIR = "Backend\Captcha_Bypass\Testing\gemini_vs_llama\downloaded_captchas"
os.makedirs(SAVE_DIR, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)
time.sleep(1)

# Format: (left, top, width, height)
REGION = (830, 552, 268, 89)

for i in range(NUM_IMAGES):
    print(f"[{i+1}/{NUM_IMAGES}] Capturing image...")

    time.sleep(1.5)

    screenshot = pyautogui.screenshot(region=REGION)

    filename = os.path.join(SAVE_DIR, f"captcha_{i+1}.png")
    screenshot.save(filename)
    print(f"✅ Saved: {filename}")

    driver.refresh()

driver.quit()
print("✅ All CAPTCHA images captured.")
