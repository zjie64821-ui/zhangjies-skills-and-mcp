---
name: xlsx
description: >
  Excel spreadsheet (.xlsx) processing toolkit. TRIGGER when the user needs to: create, edit,
  analyze spreadsheets; work with Excel formulas, formatting, charts, or financial models;
  process CSV data into Excel; perform data analysis with pandas/openpyxl.
  Also trigger for data analysis tasks that would benefit from spreadsheet output.
  DO NOT trigger for pure CSV reading without Excel-specific features.
---

# XLSX Toolkit

## Critical Rules
- **ALWAYS use Excel formulas**, never hardcode calculated values
- Zero formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)
- Recalculate after save: `python recalc.py output.xlsx` (LibreOffice)

## Libraries
- **pandas**: data analysis, bulk ops, `pd.read_excel()`, `df.to_excel()`
- **openpyxl**: formulas, formatting, `Workbook()`, `load_workbook()`

## Financial Model Color Coding
- Blue (0,0,255): hardcoded inputs
- Black (0,0,0): formulas
- Green (0,128,0): cross-sheet links
- Red (255,0,0): external links
- Yellow bg: key assumptions

## Number Format
- Years: text strings | Currency: $#,##0 + units in headers
- Percentages: 0.0% | Negatives: parentheses | Multiples: 0.0x

## Workflow
1. Choose: pandas (data) or openpyxl (formulas/formatting)
2. Create/Load → Modify → Save → Recalculate → Verify

## User Request
$ARGUMENTS
