# Google Pay Statement to CSV/Excel Converter

A lightweight Python tool to parse transaction statements exported from Google Pay in PDF and convert into clean `.csv` or `.xlsx` files.

## Output Format

The output is structured with the following 3 columns:

| Name | Amount | Date |
| :--- | :--- | :--- |
| Alice | 200 | 01/07/2026 |
| Bob | 1200 | 01/07/2026 |

- **Name**: Recipient or sender name (strips prefixes like `Paid to`, `Received from`, `Paidto`).
- **Amount**: Numeric transaction amount without currency signs (`₹`, `Rs.`) or commas.
- **Date**: Formatted as `DD/MM/YYYY`.

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
