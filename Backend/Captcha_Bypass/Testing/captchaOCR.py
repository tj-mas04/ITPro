from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image_path = r"C:\Users\ASUS\Documents\ITProfound\dev\Backend\securimage_show.png"
image = Image.open(image_path).convert("L")
image = image.filter(ImageFilter.MedianFilter())
# image = image.point(lambda x: 0 if x < 160 else 255, '1')  # Binarization

custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
captcha_text = pytesseract.image_to_string(image, config=custom_config).strip()

print(f"Detected CAPTCHA: '{captcha_text}'")


# import requests
# from PIL import Image, ImageFilter, ImageEnhance
# import pytesseract
# from io import BytesIO

# # Step 1: Setup session
# session = requests.Session()

# # Step 2: Define URLs
# base_url = "https://scr.sci.gov.in"  # Replace with the actual domain
# captcha_url = f"{base_url}/scrsearch/vendor/securimage/securimage_show.php"
# submit_url = f"{base_url}/scrsearch/?p=pdf_search/home/"  # Replace with actual form action

# # Step 3: Download CAPTCHA image
# response = session.get(captcha_url, stream=True)
# img = Image.open(BytesIO(response.content)).convert("L")

# # Step 4: Preprocess
# img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
# img = img.filter(ImageFilter.MedianFilter())
# img = img.point(lambda x: 0 if x < 160 else 255, '1')

# # Step 5: OCR
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
# captcha_text = pytesseract.image_to_string(img, config=config).strip()

# print(f"[INFO] Solved CAPTCHA: {captcha_text}")

# # Step 6: Prepare form data
# form_data = {
#     "captcha": captcha_text,
# }

# # Step 7: Submit the form
# resp = session.post(submit_url, data=form_data)

# # Step 8: Scrape the content
# if resp.status_code == 200:
#     print("[SUCCESS] Scraped page:")
#     print(resp.text[:1000])  # Print first 1000 characters
# else:
#     print("[FAILURE] Submission failed")

