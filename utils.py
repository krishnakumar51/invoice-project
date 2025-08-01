import os
import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY", None)
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env or secrets.toml")

# JSON schema for invoice fields
schemas = [
    ResponseSchema(name="invoice_no", description="Invoice number (string)"),
    ResponseSchema(name="date", description="Invoice date in YYYY-MM-DD format"),
    ResponseSchema(name="billed_to", description="Company or person being billed"),
    ResponseSchema(name="address", description="Billing address"),
    ResponseSchema(
        name="line_items",
        description="Array of objects with 'description', 'quantity', 'unit_price', and 'amount'"
    ),
    ResponseSchema(name="subtotal", description="Subtotal amount (number)"),
    ResponseSchema(name="discount", description="Discount amount (number)", nullable=True),
    ResponseSchema(name="shipping", description="Shipping cost (number)", nullable=True),
    ResponseSchema(name="total", description="Total amount (number)"),
    ResponseSchema(name="notes", description="Additional notes (string)", nullable=True),
    ResponseSchema(name="terms", description="Payment terms or order ID (string)", nullable=True),
]

parser = StructuredOutputParser.from_response_schemas(schemas)
format_instructions = parser.get_format_instructions()

SYSTEM_PROMPT = f"""
You are an invoice-parsing assistant.
Extract **exactly** these fields from the invoice text and return ONLY valid JSON:

{format_instructions}

Invoice text:
{{text}}
"""

def get_pdf_text(pdf_path: str) -> str:
    """Extracts text from all pages of a PDF file."""
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + "\n"
    return full_text

def extract_invoice_data(pdf_path: str) -> dict:
    """Uses Gemini to extract structured invoice data from a PDF."""
    text = get_pdf_text(pdf_path)
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    prompt = SYSTEM_PROMPT.replace("{text}", text)
    response = model.generate_content(prompt)
    return parser.parse(response.text)
