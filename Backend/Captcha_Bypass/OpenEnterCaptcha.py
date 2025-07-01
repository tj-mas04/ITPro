import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image, ImageEnhance, ImageFilter
import mss
from mss import tools
import google.generativeai as genai


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please check your .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    return webdriver.Chrome(options=chrome_options)

driver = init_driver()
driver.get("https://scr.sci.gov.in/scrsearch/")
time.sleep(5)

try:
    driver.find_element(By.ID, "captcha_image")
    print("CAPTCHA image found.")
except Exception as e:
    print(f"CAPTCHA image not found: {e}")
    driver.quit()
    exit()


def capture_captcha_screenshot(path, region):
    with mss.mss() as sct:
        sct_img = sct.grab(region)
        tools.to_png(sct_img.rgb, sct_img.size, output=path)
        print(f"Screenshot saved to: {path}")

def preprocess_image(path):
    image = Image.open(path).convert("L")
    image = image.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    return image

#RUN WITH GROQ AND EVALUATE GROG AND GEMINI
#FAIL AND SECCESS RATES

def solve_captcha_with_gemini(image):
    prompt = "This image is a CAPTCHA. Read and extract the alphanumeric text clearly."
    response = model.generate_content([image, prompt])
    return response.text.strip()

def enter_captcha_text(driver, text):
    input_field = driver.find_element(By.ID, "captcha")
    input_field.clear()
    input_field.send_keys(text)
    driver.find_element(By.ID, "main_search").click()

max_attempts = 10
captcha_image_path = r"C:\Users\ASUS\Documents\ITProfound\dev\Backend\region_capture.png"
screenshot_region = {"top": 784, "left": 662, "width": 140, "height": 40}
solved = False

for attempt in range(1, max_attempts + 1):
    print(f"\nAttempt {attempt} to solve CAPTCHA...")

    capture_captcha_screenshot(captcha_image_path, screenshot_region)
    image = preprocess_image(captcha_image_path)
    captcha_text = solve_captcha_with_gemini(image)
    print(f"Extracted CAPTCHA text: {captcha_text}")

    try:
        enter_captcha_text(driver, captcha_text)
        time.sleep(3)

        try:
            driver.find_element(By.ID, "captcha_image")
            print("CAPTCHA not solved.")

            try:
                close_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-close[data-bs-dismiss="modal"]')
                close_button.click()
                print("Invalid CAPTCHA dialog closed.")
                time.sleep(1)
            except Exception as e:
                print(f"Close button not found or already closed: {e}")

        except:
            print("CAPTCHA solved!")
            solved = True
            break

    except Exception as e:
        print(f"Failed to enter CAPTCHA: {e}")
        break

if not solved:
    print("❌ Failed to solve CAPTCHA after multiple attempts.")
    driver.quit()
    exit()

# ========== 5. CONTINUE POST CAPTCHA ==========

print("✅ Proceeding with search results...")
# driver.quit()
