#SCI Site Scaper + PDF Downloader

import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Constants
BASE_URL = "https://www.sci.gov.in"
JUDGMENTS_URL = BASE_URL + "/#1697446384453-9aeef8cc-5f35"
DOWNLOAD_DIR = os.path.abspath("pdfs")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Set up visible Chrome (not headless)
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')


def scrape_judgment_links():
    """Scrape all Supreme Court judgment view links."""
    resp = requests.get(JUDGMENTS_URL, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    judgments_div = soup.find('div', class_='gen-list over-y-scroll no-border no-bg padding-0 border-radius-medium arrow-list')
    judgment_links = []

    if judgments_div:
        for li in judgments_div.find_all('li'):
            a_tag = li.find('a')
            if not a_tag:
                continue

            href = a_tag['href']
            full_link = BASE_URL + href if href.startswith('/') else href

            case_text = a_tag.get_text(separator=" ", strip=True)
            file_tag = case_text.split(' - ')[0].strip().replace(' ', '_').replace('/', '_')
            filename = f"{file_tag[:100]}.pdf"

            judgment_links.append({
                'url': full_link,
                'filename': filename
            })
    return judgment_links


def download_pdf_from_iframe(driver, view_url, filename):
    """Extract the iframe PDF URL and download the file using requests."""
    try:
        driver.get(view_url)
        time.sleep(3) 

        iframe = driver.find_element("tag name", "iframe")
        pdf_url = iframe.get_attribute("src")

        if not pdf_url:
            print(f"[!] No iframe PDF found for: {view_url}")
            return

        resp = requests.get(pdf_url, stream=True, timeout=15)
        if resp.status_code == 200:
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            with open(filepath, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    f.write(chunk)
            print(f"✅ Downloaded: {filename}")
        else:
            print(f"[!] PDF download failed ({resp.status_code}): {pdf_url}")

    except Exception as e:
        print(f"[X] Error downloading from {view_url}: {e}")


def download_all_supreme_court_pdfs():
    judgment_links = scrape_judgment_links()
    print(f"Found {len(judgment_links)} judgments.")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    for item in judgment_links:
        print(f"Processing: {item['url']}")
        download_pdf_from_iframe(driver, item['url'], item['filename'])

    driver.quit()
    print("✅ All downloads complete.")


if __name__ == "__main__":
    download_all_supreme_court_pdfs()
