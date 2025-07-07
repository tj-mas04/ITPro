#RUN API : uvicorn sciAPI:app --reload

from fastapi import FastAPI
from sciScraper import download_all_supreme_court_Judgments
from sciScraper import download_all_supreme_court_orders
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Supreme Court PDF Scraper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/scrape-download_Judgments_and_Orders")
def trigger_scraper():
    try:
        judgment_count = download_all_supreme_court_Judgments()
        order_count = download_all_supreme_court_orders()
        return {"status": "success", "message": f"Downloaded {judgment_count} judgments and {order_count} orders"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
