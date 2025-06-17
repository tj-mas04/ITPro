import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/judgments"

def fetch_judgments_from_api():
    """Get judgments data from the FastAPI server."""
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def filter_and_format_judgments(search_term, date_filter):
    try:
        data = fetch_judgments_from_api()
        
        # Apply search term filter
        if search_term:
            data = [
                j for j in data
                if search_term.lower() in (j['case_title'] or '').lower()
            ]
        
        # Apply date filter
        if date_filter:
            data = [
                j for j in data
                if date_filter in (j['date'] or '')
            ]

        # Format as a list of lists for Gradio DataFrame
        display_data = [
            [j['date'], j['case_title'], j['judgment_link']]
            for j in data
        ]

        return display_data

    except Exception as e:
        return [[f"Error: {e}", "", ""]]

# Gradio interface
with gr.Blocks(title="Supreme Court Judgments Dashboard") as demo:
    gr.Markdown("# ⚖️ Supreme Court Judgments Dashboard")
    gr.Markdown("Fetch and explore recent Supreme Court judgments.")

    with gr.Row():
        search_box = gr.Textbox(label="Search Case Title", placeholder="Type part of the case title...")
        date_box = gr.Textbox(label="Filter by Date", placeholder="Example: 10 June 2025")
        refresh_btn = gr.Button("Fetch Judgments")

    judgment_table = gr.Dataframe(
    headers=["Date", "Case Title", "Judgment Link"],
    datatype=["str", "str", "str"],
    interactive=False,
    wrap=True
    )


    # Button triggers fetch + display
    refresh_btn.click(
        fn=filter_and_format_judgments,
        inputs=[search_box, date_box],
        outputs=judgment_table
    )

    # Auto update when inputs change
    search_box.change(
        fn=filter_and_format_judgments,
        inputs=[search_box, date_box],
        outputs=judgment_table
    )
    date_box.change(
        fn=filter_and_format_judgments,
        inputs=[search_box, date_box],
        outputs=judgment_table
    )

demo.launch(share=True)