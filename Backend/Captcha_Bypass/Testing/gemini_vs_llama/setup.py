import os
import base64
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq
from PIL import Image

load_dotenv()

# ==== Setup Gemini ====
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

def solve_with_gemini(image_path):
    # Load image using PIL
    image = Image.open(image_path)

    prompt = "This image is a CAPTCHA. Read and extract the alphanumeric text clearly. Output only the code as a string."
    
    # Gemini expects [image, prompt] as input
    response = gemini_model.generate_content([image, prompt])
    return response.text.strip()

# ==== Setup LLaMA ====
llama_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def solve_with_llama(image_path):
    base64_img = encode_image(image_path)
    chat_completion = llama_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Read and extract the alphanumeric text clearly. Consider it as a single string without spaces. Just return the text without any additional information."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_img}",
                        },
                    },
                ],
            }
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
    )
    return chat_completion.choices[0].message.content.strip()
