# PDF Processing Toolkit

Comprehensive PDF manipulation using Python libraries and CLI tools.

## Libraries & Tools
- **pypdf**: merge, split, rotate, metadata, encrypt/decrypt
- **pdfplumber**: text extraction (with layout), table extraction → pandas DataFrame
- **reportlab**: create new PDFs (Canvas or Platypus)
- **pytesseract + pdf2image**: OCR scanned PDFs
- **CLI**: `pdftotext` (poppler), `qpdf`, `pdftk`

## Quick Reference
| Task | Tool | Key API |
|------|------|---------|
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` → pandas |
| Merge PDFs | pypdf | `PdfWriter().add_page()` |
| Split PDFs | pypdf | iterate `reader.pages` |
| Create PDF | reportlab | `SimpleDocTemplate` / `Canvas` |
| OCR scanned | pytesseract | `convert_from_path()` → `image_to_string()` |
| Watermark | pypdf | `page.merge_page(watermark)` |
| Password | pypdf | `writer.encrypt(user_pw, owner_pw)` |
| CLI merge | qpdf | `qpdf --empty --pages f1.pdf f2.pdf -- out.pdf` |

## User Request
$ARGUMENTS
