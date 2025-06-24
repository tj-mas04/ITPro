import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyCUcjaE6qjusGsSEGRY5aFK24kdg5D_z-A"  

def solve_captcha_with_gemini(image_url, api_key):
    """Solves a CAPTCHA image using Gemini.

    Args:
        image_url: The URL of the CAPTCHA image.
        api_key: Your Google Gemini API key.

    Returns:
        The solved CAPTCHA text, or None if it couldn't be solved.
    """

    try:
        response = requests.get(image_url, stream=True, verify=False)
        response.raise_for_status()  
        image = Image.open(BytesIO(response.content)).convert('L')
        image.save("captcha.png") 

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash') 

        contents = Image.open("captcha.png")

        response = model.generate_content(contents, stream=False)
        captcha_text = response.text.strip()  

        print(f"Gemini's CAPTCHA guess: {captcha_text}") 

        return captcha_text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CAPTCHA image: {e}")
        return None
    except Exception as e:
        print(f"Error solving CAPTCHA with Gemini: {e}")
        return None


def bypass_captcha(url, google_api_key):
    """Bypasses the CAPTCHA on the specified webpage.

    Args:
        url: The URL of the webpage with the CAPTCHA.
        google_api_key: Your Google Gemini API key.
    """
    chrome_options = Options()
    # chrome_options.add_argument("--headless=new") # Use the new headless mode which is more stable. Requires Chrome 109+
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("--disable-dev-shm-usage")  
    chrome_options.add_argument("--window-size=1920,1080") 



    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        captcha_image_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "captcha_image"))
        )
        captcha_image_url = captcha_image_element.get_attribute("src")

        captcha_text = solve_captcha_with_gemini(captcha_image_url, google_api_key)

        if captcha_text:
            captcha_input = driver.find_element(By.ID, "captcha")
            captcha_input.send_keys(captcha_text)

            search_button = driver.find_element(By.ID, "main_search")
            search_button.click()

            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "https://scr.sci.gov.in/scrsearch/?p=pdf_search/home/"))  # Replace with a suitable element on the result page.
            )
            print("Captcha bypassed and search initiated successfully.")


        else:
            print("Failed to solve CAPTCHA.")


    except Exception as e:
        print(f"An error occurred during the browser automation: {e}")

    finally:
        driver.quit()



if __name__ == "__main__":
    target_url = "https://scr.sci.gov.in/scrsearch/"
    bypass_captcha(target_url, GOOGLE_API_KEY)