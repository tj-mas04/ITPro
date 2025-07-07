import os
import json
from PyPDF2 import PdfReader

# Define input and output folders
pdf_folder = r"Backend\Orders_PDFs"
output_folder = r"Backend\Orders_PDFs\Extracted"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Iterate through each PDF in the folder
for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        output_filename = filename.replace(".pdf", ".json")
        output_path = os.path.join(output_folder, output_filename)

        try:
            reader = PdfReader(pdf_path)
            text = ""

            for page in reader.pages:
                text += page.extract_text() or ""

            # Prepare JSON data
            data = {
                "filename": filename,
                "page_count": len(reader.pages),
                "content": text.strip()
            }

            # Save as JSON
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✅ Extracted: {filename} -> {output_path}")

        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")
