import os
import json
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from utils import extract_invoice_data

# Setup environment & folders
load_dotenv()
os.makedirs("json", exist_ok=True)
os.makedirs("table", exist_ok=True)

st.set_page_config(page_title="Invoice Parser with Gemini")
st.title("PDF Invoice Extractor")
st.markdown("Upload multiple invoice PDFs. We'll parse & export their data using Gemini.")

# File uploader
pdf_files = st.file_uploader("Upload PDF invoices", type="pdf", accept_multiple_files=True)

if st.button("Extract Invoice Data") and pdf_files:
    records = []

    for uploaded_file in pdf_files:
        st.write(f"⏳ Processing `{uploaded_file.name}` …")
        
        # Save to disk
        local_path = os.path.join("json", uploaded_file.name)
        with open(local_path, "wb") as f:
            f.write(uploaded_file.read())

        # Extract data
        try:
            data = extract_invoice_data(local_path)
        except Exception as e:
            st.error(f"❌ Failed to extract data from `{uploaded_file.name}`: {e}")
            continue

        # Save JSON per file
        out_json = os.path.join("json", f"{os.path.splitext(uploaded_file.name)[0]}.json")
        with open(out_json, "w", encoding="utf-8") as jf:
            json.dump(data, jf, indent=2)

        # Prepare flat row for CSV
        record = {
            "file": uploaded_file.name,
            "invoice_no": data.get("invoice_no"),
            "date": data.get("date"),
            "billed_to": data.get("billed_to"),
            "address": data.get("address"),
            "subtotal": data.get("subtotal"),
            "discount": data.get("discount"),
            "shipping": data.get("shipping"),
            "total": data.get("total"),
            "notes": data.get("notes"),
            "terms": data.get("terms"),
            "line_items": json.dumps(data.get("line_items", [])),
        }
        records.append(record)

        st.success(f"✅ Done: `{uploaded_file.name}`")

    # Create final CSV
    if records:
        df = pd.DataFrame(records)
        csv_path = os.path.join("table", "invoices_extracted.csv")
        df.to_csv(csv_path, index=False)

        st.subheader("📊 Extracted Invoice Data")
        st.dataframe(df)

        st.download_button(
            label="⬇️ Download CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="invoices_extracted.csv",
            mime="text/csv"
        )

        st.success("✅ All done! JSON saved to `json/`, CSV saved to `table/`")
    else:
        st.warning("No valid invoice data extracted.")
