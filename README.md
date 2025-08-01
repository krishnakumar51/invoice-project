# 🧾 Invoice Extractor

This Streamlit-based app uses Google Gemini (via `google-generativeai`) to automatically extract structured data from scanned or digital invoice PDFs. It supports:

- 🧠 Multi-invoice extraction (batch upload)
- 📊 CSV and JSON export of structured results
- 📂 Local `.env` or deployment `secrets.toml` support
- ⚡️ Gemini 2.0 Flash-Lite for fast and accurate output
- ✅ No vector DBs, only OCR + structured parsing

---

## 📸 Sample Output

| File                       | Invoice No | Date       | Billed To     | Total   |
|---------------------------|------------|------------|---------------|---------|
| invoice_Aaron_39519.pdf   | 1001329    | 2023-05-04 | Avery Corp    | $875.00 |

---

## 🛠️ Setup & Run Locally

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/invoice-project.git
cd invoice-extractor-gemini
````

### 2. Install Dependencies

```bash
pip install -e .
```

### 3. Create `.env`

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

Or, for Streamlit Cloud:

Use `secrets.toml`:

```toml
# .streamlit/secrets.toml
GOOGLE_API_KEY = "your_gemini_api_key_here"
```

### 4. Run App

```bash
streamlit run app.py
```

---

## 📁 Directory Structure

```
.
├── app.py                  # Main Streamlit app
├── utils.py                # Extraction logic with Gemini + schema
├── json/                   # Auto-saved extracted JSON files
├── table/                  # Final CSV output
├── invoices/               # Sample pdf for invoice generation   
├── .env                    # Local environment variables
├── .streamlit/secrets.toml# Streamlit deployment secrets (optional)
├── pyproject.toml          # Package definition
└── README.md
```

---

## 📦 Outputs

* Structured data saved to:

  * `json/invoice_<name>.json` (one per file)
  * `table/invoices_extracted.csv` (combined)
* You can also download CSV via UI.

---

## 💬 Prompt Template (internally used)

Gemini is prompted with the following:

```
You are an invoice-parsing assistant.
Extract exactly these fields from the invoice text and return ONLY valid JSON:
...
```

Uses LangChain's `StructuredOutputParser` for schema validation.

---

## 🔐 Security

* No files leave your machine (unless deployed)
* Gemini is only called with necessary prompt + OCR text

---

## 🧠 Model Used

* `gemini-2.0-flash-lite`
* Inference via `google-generativeai` Python SDK

---

## 📃 License

MIT – Free to use, fork, or extend.

````
