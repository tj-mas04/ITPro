# gradio_ui.py

import gradio as gr
import os
import requests
from pathlib import Path

PDF_DIR = Path(r"C:\Users\ASUS\Documents\ITProfound\dev\Backend\pdfs")
API_URL = "http://127.0.0.1:8000/scrape-download"

def trigger_scraper():
    """Calls the FastAPI scraper endpoint and returns response"""
    try:
        resp = requests.get(API_URL)
        return resp.json()["message"]
    except Exception as e:
        return f"Error: {e}"

def list_pdfs():
    """Lists all downloaded PDF filenames"""
    if not PDF_DIR.exists():
        return []
    return sorted([f.name for f in PDF_DIR.glob("*.pdf")])

def display_pdf(filename):
    if not filename:
        return "<p><i>No PDF selected</i></p>"

    filepath = PDF_DIR / filename

    if filepath.exists():
        iframe_path = filepath.as_posix()
        html = f"""
        <iframe src="file://{iframe_path}" width="100%" height="600px" style="border:1px solid #aaa;">
        This browser does not support PDFs. <a href="file://{iframe_path}">Download PDF</a>.
        </iframe>
        """
        return html
    else:
        return "<p><b>❌ Error:</b> File not found</p>"



with gr.Blocks(title="Supreme Court Judgment Downloader") as demo:
    gr.Markdown("## 📄 Supreme Court Judgment Downloader")

    with gr.Row():
        scrape_btn = gr.Button("🔄 Scrape & Download Judgments")
        status_box = gr.Textbox(label="Status", interactive=False)

    with gr.Row():
        pdf_list = gr.Dropdown(label="Downloaded PDFs", choices=list_pdfs())
        open_pdf = gr.Button("📂 Open PDF")

    pdf_viewer = gr.HTML(label="PDF Viewer")

    scrape_btn.click(fn=trigger_scraper, outputs=status_box).then(fn=list_pdfs, outputs=pdf_list)
    open_pdf.click(fn=display_pdf, inputs=pdf_list, outputs=pdf_viewer)

demo.launch(allowed_paths=["../Backend/pdfs"])
