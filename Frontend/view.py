# import gradio as gr
# import os

# PDF_DIR = os.path.abspath("C:\\Users\\ASUS\\Documents\\ITProfound\\dev\\Backend\\pdfs")

# def list_pdfs():
#     """List all PDF files in the pdfs directory."""
#     return sorted([
#         f for f in os.listdir(PDF_DIR)
#         if f.lower().endswith(".pdf")
#     ])

# def render_pdf(filename):
#     """Return an iframe HTML embedding the local PDF."""
#     pdf_path = os.path.join(PDF_DIR, filename)
#     if not os.path.exists(pdf_path):
#         return f"<p style='color:red;'>File not found: {filename}</p>"

#     return f"""
#     <iframe src="file:///{pdf_path}" width="100%" height="600px" style="border: none;"></iframe>
#     """

# with gr.Blocks(title="📄 PDF Judgment Viewer") as demo:
#     gr.Markdown("## 🧾 View Downloaded Supreme Court Judgments")
#     gr.Markdown("Select and view a judgment PDF from the local `pdfs/` folder.")

#     pdf_dropdown = gr.Dropdown(label="Select PDF", choices=list_pdfs())
#     load_button = gr.Button("📂 Load PDF")

#     pdf_output = gr.HTML()

#     # Load iframe when button is clicked
#     load_button.click(
#         fn=render_pdf,
#         inputs=pdf_dropdown,
#         outputs=pdf_output
#     )

#     # Refresh dropdown list on app load
#     demo.load(fn=list_pdfs, inputs=None, outputs=pdf_dropdown)

# demo.launch(share=True)

import gradio as gr
import requests

API_LIST = "http://127.0.0.1:8000/scrape-judgments"
API_PDF = "http://127.0.0.1:8000/view-pdf/"

def fetch_pdf_list():
    try:
        response = requests.get(API_LIST)
        response.raise_for_status()
        data = response.json()
        return [item['filename'] for item in data['results'] if item['status'] == 'Downloaded']
    except Exception as e:
        return [f"Error: {e}"]

def render_pdf(filename):
    return f"""
    <iframe src="{API_PDF}{filename}" width="100%" height="600px" style="border: 1px solid #ccc;"></iframe>
    """

with gr.Blocks(title="📄 Supreme Court Judgment Viewer") as demo:
    gr.Markdown("# ⚖️ Supreme Court Judgment PDFs Viewer")
    gr.Markdown("Use the dropdown below to view locally downloaded judgments.")

    pdf_selector = gr.Dropdown(label="📂 Select a PDF", choices=[], interactive=True)
    view_btn = gr.Button("🔍 View Judgment")
    pdf_display = gr.HTML()

    demo.load(fn=fetch_pdf_list, inputs=None, outputs=pdf_selector)
    view_btn.click(fn=render_pdf, inputs=pdf_selector, outputs=pdf_display)

demo.launch(share=True)
