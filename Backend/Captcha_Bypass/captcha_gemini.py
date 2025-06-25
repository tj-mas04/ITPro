import google.generativeai as genai
import os
from PIL import Image

GOOGLE_API_KEY = "AIzaSyCUcjaE6qjusGsSEGRY5aFK24kdg5D_z-A"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

image_path = r"C:\Users\ASUS\Documents\ITProfound\dev\Backend\region_capture.png"
image = Image.open(image_path)

response = model.generate_content(
    [image, "Extract the text from this image."]
)

print(response.text)