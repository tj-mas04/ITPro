from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import mss
from mss import tools
from PIL import Image, ImageEnhance, ImageFilter
import google.generativeai as genai


chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://scr.sci.gov.in/scrsearch/")
time.sleep(5)

try:
    captcha = driver.find_element(By.ID, "captcha_image")
    print("CAPTCHA image found.")
except:
    print("CAPTCHA image not found.")
    driver.quit()
    exit()

# ========== GEMINI OCR & CAPTCHA SOLVE LOOP ==========

GOOGLE_API_KEY = "AIzaSyCUcjaE6qjusGsSEGRY5aFK24kdg5D_z-A"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

max_attempts = 10
solved = False

for attempt in range(max_attempts):
    # Take screenshot of captcha
    print(f"Attempt {attempt+1} to solve CAPTCHA...")
    monitor = {"top": 784, "left": 662, "width": 140, "height": 40}
    image_path = r"C:\Users\ASUS\Documents\ITProfound\dev\Backend\region_capture.png"
    with mss.mss() as sct:
        sct_img = sct.grab(monitor)
        tools.to_png(sct_img.rgb, sct_img.size, output=image_path)
        print(f"Screenshot saved to: {image_path}")

    # OCR using Gemini
    image = Image.open(image_path)
    image = Image.open(image_path).convert("L")
    image = image.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    
    response = model.generate_content([image, "This image is a CAPTCHA. Please read and extract the alphanumeric text clearly."])
    captcha_text = response.text.strip()
    print(f"Attempt {attempt+1}: Extracted CAPTCHA text: {captcha_text}")

    # Enter captcha and try to submit
    try:
        input_field = driver.find_element(By.ID, "captcha")
        input_field.clear()
        input_field.send_keys(captcha_text)
        print("CAPTCHA text entered: " + captcha_text)
        driver.find_element(By.ID, "main_search").click()
        time.sleep(3)  # Wait for page to respond

        # Check if captcha was solved (captcha image disappears or error message not present)
        try:
            # If captcha image is still present, it means captcha failed
            driver.find_element(By.ID, "captcha_image")
            print("CAPTCHA not solved, retrying...")
        except:
            print("CAPTCHA solved!")
            solved = True
            break
    except Exception as e:
        print(f"Failed to enter CAPTCHA: {e}")
        # driver.quit()
        exit()

if not solved:
    print("Failed to solve CAPTCHA after multiple attempts.")
    # driver.quit()
    exit()

# ...continue with your logic after captcha

driver.find_element(By.ID, "main_search").click()

# driver.quit()
