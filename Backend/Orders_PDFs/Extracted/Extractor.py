import os
import json
from pypdf import PdfReader

# Define input and output directories
pdf_folder = r"Backend\Orders_PDFs"
output_folder = r"Backend\Orders_PDFs\Extracted"

# Create the output directory if it does not exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all PDF files in the input directory
for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        output_filename = os.path.splitext(filename)[0] + ".json"
        output_path = os.path.join(output_folder, output_filename)

        try:
            reader = PdfReader(pdf_path)
            content = ""

            for i, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                content += page_text

            # Construct the JSON structure
            data = {
                "filename": filename,
                "page_count": len(reader.pages),
                "content": content.strip()
            }

            # Write the extracted data to a JSON file
            with open(output_path, "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=2, ensure_ascii=False)

            print(f"✅ Extracted: {filename} → {output_filename}")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
