from bs4 import BeautifulSoup
import requests

base_url = "https://scr.sci.gov.in"
session = requests.Session()
resp = session.get(f"{base_url}/scrsearch")

soup = BeautifulSoup(resp.text, "html.parser")
form = soup.find("form")
print("Form action:", form.get("action"))
