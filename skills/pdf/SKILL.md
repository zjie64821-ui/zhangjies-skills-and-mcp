---
name: pdf
description: >
  PDF processing toolkit. TRIGGER when the user needs to: merge, split, extract text/tables/images from,
  create, OCR, watermark, encrypt/decrypt, rotate, or programmatically manipulate PDF files.
  Also trigger for converting PDFs to other formats or analyzing PDF content at scale.
  DO NOT trigger for reading a single PDF file (use the Read tool directly).
---

# PDF Processing Guide

## Python Libraries
- **pypdf**: merge (`PdfWriter.add_page()`), split, rotate, metadata, encrypt (`writer.encrypt()`), watermark (`page.merge_page()`)
- **pdfplumber**: text extraction (`page.extract_text()`), table extraction (`page.extract_tables()` → pandas)
- **reportlab**: create PDFs (Canvas for simple, Platypus/SimpleDocTemplate for multi-page)
- **pytesseract + pdf2image**: OCR scanned PDFs (`convert_from_path()` → `image_to_string()`)

## CLI Tools
- `pdftotext` (poppler): text extraction, `-layout` preserves layout
- `qpdf`: merge (`qpdf --empty --pages`), split, rotate, decrypt
- `pdftk`: merge, split (`burst`), rotate

## Quick Reference
| Task | Best Tool | Key API |
|------|-----------|---------|
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` → DataFrame |
| Merge | pypdf | `PdfWriter().add_page()` |
| Split | pypdf | iterate `reader.pages` |
| Create | reportlab | `SimpleDocTemplate` / `Canvas` |
| OCR | pytesseract | `convert_from_path()` → `image_to_string()` |
| Watermark | pypdf | `page.merge_page()` |
| Password | pypdf | `writer.encrypt()` |

## User Request
$ARGUMENTS
