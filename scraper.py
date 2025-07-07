import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Setup download directory
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Configure headless Chrome with PDF auto-download
def setup_browser(download_dir):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    prefs = {
        "download.default_directory": download_dir,
        "plugins.always_open_pdf_externally": True,
        "download.prompt_for_download": False
    }
    options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(options=options)

# Fetch HTML with requests and return BeautifulSoup object
def fetch_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

# Extract PDF links from Delhi High Court
def extract_delhi_links():
    base_url = "https://delhihighcourt.nic.in/web/judgement/fetch-data"
    soup = fetch_soup(base_url)
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.endswith(".pdf"):
            full_url = f"https://delhihighcourt.nic.in{href}" if not href.startswith("http") else href
            links.append(full_url)
    return links

# Extract PDF links from Telengana High Court
def extract_telangana_links():
    base_url = "https://tshc.gov.in/showList?id=2"
    soup = fetch_soup(base_url)
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if ".pdf" in href.lower():
            full_url = href if href.startswith("http") else f"https://tshc.gov.in/{href}"
            links.append(full_url)
    return links

# Extract PDF links from Jammu & Kashmir High Court
def extract_jk_links():
    base_url = "https://jkhighcourt.nic.in/"
    soup = fetch_soup(base_url)
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if ".pdf" in href.lower():
            full_url = href if href.startswith("http") else f"https://jkhighcourt.nic.in/{href}"
            links.append(full_url)
    return links
# Extract PDF links from Sikkim High Court
def extract_sikkim_links():
    base_url = "https://hcs.gov.in/hcs/"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(base_url)
    time.sleep(3)

    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    links = []
    for link in driver.find_elements(By.CSS_SELECTOR, "a"):
        href = link.get_attribute("href")
        text = link.text.strip()
        if href and href.endswith(".pdf") and "judgment" in text.lower():
            links.append((text, href))
    driver.quit()
    return links

# Download PDF using Selenium (handles iframe if needed)
def download_pdf(driver, pdf_url):
    try:
        print(f"📥 Downloading: {pdf_url}")
        driver.get(pdf_url)
        time.sleep(4)  # wait for download to complete
    except Exception as e:
        print(f"❌ Failed to download {pdf_url}: {e}")

def main():
    driver = setup_browser(DOWNLOAD_DIR)

    courts = {
        "Delhi High Court": extract_delhi_links,
        "Telangana High Court": extract_telangana_links,
        "Jammu & Kashmir High Court": extract_jk_links,
        "Sikkim High Court": extract_sikkim_links

    }

    for court_name, extract_fn in courts.items():
        print(f"\n🔍 Scraping: {court_name}")
        try:
            links = extract_fn()
            print(f"🧾 Found {len(links)} PDF links.")
            for i, pdf_link in enumerate(links[:5], start=1):  # Limit to first 5 for testing
                print(f"({i}) {pdf_link}")
                download_pdf(driver, pdf_link)
        except Exception as e:
            print(f"⚠️ Error with {court_name}: {e}")

    driver.quit()
    print("\n✅ Done. Check the 'downloads' folder.")

if __name__ == "__main__":
    main()

