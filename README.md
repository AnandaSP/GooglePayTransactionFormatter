# Google Pay Statement to CSV/Excel Converter

A lightweight Python tool to parse transaction statements exported from Google Pay in PDF and convert into clean `.csv` or `.xlsx` files.

## Output Format

The output is structured with the following 4 columns:

| Name | Amount | Date | Type |
| :--- | :--- | :--- | :--- |
| Alice | 200 | 01/07/2026 | Debit |
| Bob | 1200 | 01/07/2026 | Debit |
| Chloe | 500 | 02/07/2026 | Credit |

- **Name**: Recipient or sender name (prefixes like `Paid to`, `Received from`, `Sent to` are stripped).
- **Amount**: Numeric transaction amount without currency symbols (`₹`, `Rs.`) or commas.
- **Date**: Transaction date in `DD/MM/YYYY` format.
- **Type**: `Debit` (for `Paid to`, `Sent to`, `Self transfer`) or `Credit` (for `Received from`).

---

## Installation

Clone or download the project files and install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### Export to CSV
```bash
python parse_gpay.py statement.pdf output.csv
```

### Export to Excel
```bash
python parse_gpay.py statement.pdf output.xlsx
```
