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

        # Build HTML table
        table_html = """
        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width:100%;">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Case Title</th>
                    <th>Judgment Link</th>
                </tr>
            </thead>
            <tbody>
        """

        for j in data:
            table_html += f"""
            <tr>
                <td>{j['date'] or ''}</td>
                <td>{j['case_title'] or ''}</td>
                <td><a href="{j['judgment_link'] or '#'}" target="_blank">View Judgment</a></td>
            </tr>
            """

        table_html += "</tbody></table>"

        return table_html

    except Exception as e:
        return f"<p style='color:red;'>Error: {e}</p>"

# Gradio interface
with gr.Blocks(title="Supreme Court Judgments Dashboard") as demo:
    gr.Markdown("# ⚖️ Supreme Court Judgments Dashboard")
    gr.Markdown("Fetch and explore recent Supreme Court judgments.")

    # CSS to style and ensure min height for spinner visibility
    gr.Markdown("""
    <style>
    #judgment-container {
        height: 500px;
        border: 1px solid #ddd;
        padding: 10px;
        overflow-y: auto;
    }
    table {
        font-size: 14px;
    }
    th {
        background-color: #f2f2f2;
    }
    tr:hover {
        background-color: #f9f9f9;
    }
    </style>
    """)

    with gr.Row():
        search_box = gr.Textbox(label="Search Case Title", placeholder="Type part of the case title...")
        date_box = gr.Textbox(label="Filter by Date", placeholder="Example: 10 June 2025")
        refresh_btn = gr.Button("Fetch Judgments")

    judgment_html = gr.HTML(value="<p style='text-align:center;'>No judgments loaded yet.</p>", elem_id="judgment-container")

    # Button triggers fetch + display
    refresh_btn.click(
        fn=filter_and_format_judgments,
        inputs=[search_box, date_box],
        outputs=judgment_html
    )

    # Auto update when inputs change
    search_box.change(
        fn=filter_and_format_judgments,
        inputs=[search_box, date_box],
        outputs=judgment_html
    )
    date_box.change(
        fn=filter_and_format_judgments,
        inputs=[search_box, date_box],
        outputs=judgment_html
    )

demo.launch(share=True)
