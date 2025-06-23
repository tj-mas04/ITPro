from fastapi import FastAPI
from sciScraper import download_all_supreme_court_pdfs
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Supreme Court PDF Scraper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/scrape-download")
def trigger_scraper():
    try:
        count = download_all_supreme_court_pdfs()
        return {"status": "success", "message": f"Downloaded {count} judgments"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
