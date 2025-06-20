from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sciScraper import download_all_supreme_court_pdfs

app = FastAPI(title="Supreme Court PDF Scraper API")

# # # Optional: Allow frontend tools like Gradio/React to access it
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# @app.get("/scrape-judgments")
# def scrape_judgments():
#     """
#     Trigger the scraping and downloading of Supreme Court judgment PDFs.
#     Returns list of status messages for each file.
#     """
#     results = download_all_supreme_court_pdfs()
#     return {"message": "Scraping completed", "results": results}



from fastapi.responses import FileResponse
import os

PDF_DIR = os.path.abspath("pdfs")  # This is your download path

@app.get("/view-pdf/{filename}")
def view_pdf(filename: str):
    file_path = os.path.join(PDF_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, media_type='application/pdf', filename=filename)
    return {"error": f"File '{filename}' not found"}


