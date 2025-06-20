from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

BASE_URL = "https://www.advocatekhoj.com"
ANNOUNCEMENT_URL = BASE_URL + "/library/judgments/announcement.php"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def scrape_judgments():
    resp = requests.get(ANNOUNCEMENT_URL, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    table = soup.find('table', attrs={'cellpadding': '7', 'cellspacing': '2'})
    judgments = []

    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) < 2:
            continue
        
        date = tds[0].get_text(strip=True)
        link_tag = tds[1].find('a')
        if link_tag:
            title = link_tag.get_text(strip=True)
            href = link_tag['href']
            full_link = BASE_URL + href if href.startswith('/') else href
        else:
            title = None
            full_link = None
        
        judgments.append({
            'date': date,
            'case_title': title,
            'judgment_link': full_link
        })
    
    return judgments

@app.get("/judgments")
def get_judgments():
    return scrape_judgments()