import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image, ImageEnhance, ImageFilter
import mss
from mss import tools
from dotenv import load_dotenv
from groq import Groq

# ===== 1. Load Environment Variables =====
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ API key not found. Please check your .env file.")

client = Groq(api_key=GROQ_API_KEY)

# ===== 2. Init WebDriver =====
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

# ===== 3. Screenshot and Preprocess =====
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
    image.save(path)  # Save preprocessed image for Groq
    return path

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# ===== 4. Solve CAPTCHA with Groq LLaMA-4 =====
def solve_captcha_with_llama(image_path):
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Read and extract the alphanumeric text clearly. Consider it as a single string without spaces. Just return the text without any additional information."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
    )
    return response.choices[0].message.content.strip()

def enter_captcha_text(driver, text):
    input_field = driver.find_element(By.ID, "captcha")
    input_field.clear()
    input_field.send_keys(text)
    driver.find_element(By.ID, "main_search").click()

# ===== 5. Main CAPTCHA Solving Loop =====
max_attempts = 10
captcha_image_path = r"C:\Users\ASUS\Documents\ITProfound\dev\Backend\region_capture.png"
screenshot_region = {"top": 784, "left": 662, "width": 140, "height": 40}
solved = False

for attempt in range(1, max_attempts + 1):
    print(f"\nAttempt {attempt} to solve CAPTCHA...")

    capture_captcha_screenshot(captcha_image_path, screenshot_region)
    processed_image_path = preprocess_image(captcha_image_path)
    captcha_text = solve_captcha_with_llama(processed_image_path)
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

# ===== 6. Continue After CAPTCHA =====
print("✅ Proceeding with search results...")
# driver.quit()
