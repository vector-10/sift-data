import re
from datetime import datetime


def parse_invoice(text: str) -> dict:
    result = {
        "invoice_number": None,
        "date": None,
        "vendor": None,
        "amount": None
    }
    
    # Invoice number patterns
    invoice_patterns = [
        r'Invoice\s*#?\s*:?\s*([A-Z0-9-]+)',
        r'INV[-\s]?(\d+)',
    ]
    for pattern in invoice_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result["invoice_number"] = match.group(1)
            break
    
    # Date patterns
    date_patterns = [
        r'Date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(\d{4}-\d{2}-\d{2})',
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            result["date"] = match.group(1)
            break
    
    # Amount patterns
    amount_patterns = [
        r'Total\s*:?\s*\$?\s*([\d,]+\.?\d*)',
        r'Amount\s*:?\s*\$?\s*([\d,]+\.?\d*)',
    ]
    for pattern in amount_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result["amount"] = float(match.group(1).replace(',', ''))
            break
    
    # Vendor (first line or company name)
    vendor_match = re.search(r'^(.+?)(?:\n|$)', text.strip())
    if vendor_match:
        result["vendor"] = vendor_match.group(1).strip()
    
    return result