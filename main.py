import re
import sys
from datetime import datetime
import pandas as pd
import pdfplumber

def clean_name(desc: str) -> str:
    """Strip action prefixes like 'Paid to', 'Paidto', 'Received from', etc."""
    cleaned = re.sub(
        r"^(Paid\s*to|Received\s*from|Self\s*transfer\s*to|Transferred\s*to)\s*",
        "",
        desc,
        flags=re.IGNORECASE,
    )
    return cleaned.strip()

def format_date(raw_date: str) -> str:
    """Convert raw dates like '01Jul,2026' or '01 Jul, 2026' to 'DD/MM/YYYY'."""
    clean = re.sub(r"[,\s]+", " ", raw_date).strip()
    try:
        dt = datetime.strptime(clean, "%d %b %Y")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        m = re.match(r"(\d{1,2})([A-Za-z]{3})\s*(\d{4})", clean.replace(" ", ""))
        if m:
            day, month, year = m.groups()
            dt = datetime.strptime(f"{day} {month} {year}", "%d %b %Y")
            return dt.strftime("%d/%m/%Y")
        return raw_date

def parse_gpay_pdf(pdf_path: str) -> pd.DataFrame:
    txn_start_re = re.compile(
        r"^(\d{1,2}\s*[A-Za-z]{3},?\s*\d{4})\s+(.+?)\s+([₹Rs\+\-]?\s*[\d,]+(?:\.\d{1,2})?)$"
    )

    records = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for raw_line in text.splitlines():
                line = raw_line.strip()
                if not line:
                    continue

                match = txn_start_re.match(line)
                if match:
                    raw_date = match.group(1).strip()
                    raw_desc = match.group(2).strip()
                    raw_amt = match.group(3).strip()

                    records.append(
                        {
                            "Name": clean_name(raw_desc),
                            "Amount": re.sub(r"[₹Rs\s,]", "", raw_amt),
                            "Date": format_date(raw_date),
                        }
                    )

    return pd.DataFrame(records, columns=["Name", "Amount", "Date"])

def main():
    if len(sys.argv) < 3:
        print("Usage: python parse_gpay.py <input.pdf> <output.csv|output.xlsx>")
        sys.exit(1)

    pdf_file, out_file = sys.argv[1], sys.argv[2]
    df = parse_gpay_pdf(pdf_file)

    if df.empty:
        print("No transactions found. Please verify the input PDF.")
        return

    if out_file.lower().endswith(".xlsx"):
        df.to_excel(out_file, index=False)
    else:
        df.to_csv(out_file, index=False)

    print(f"Successfully saved {len(df)} transactions to '{out_file}'.")
    print(df.head())

if __name__ == "__main__":
    main()