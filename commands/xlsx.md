# Excel Spreadsheet Toolkit

Create, edit, and analyze .xlsx files with formulas and formatting.

## Critical Rules
- **ALWAYS use Excel formulas**, never hardcode calculated values
- Zero formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)
- Recalculate after creating: `python recalc.py output.xlsx` (uses LibreOffice)

## Libraries
- **pandas**: data analysis, bulk operations, simple export
- **openpyxl**: formulas, formatting, Excel-specific features

## Financial Model Color Coding
- Blue text (0,0,255): hardcoded inputs
- Black text (0,0,0): formulas/calculations
- Green text (0,128,0): links from other worksheets
- Red text (255,0,0): external links
- Yellow background: key assumptions

## Number Formatting
- Years: text strings ("2024" not "2,024")
- Currency: $#,##0, specify units in headers
- Percentages: 0.0% format
- Negatives: parentheses (123) not -123

## Workflow
1. Choose tool: pandas for data, openpyxl for formulas/formatting
2. Create/Load workbook
3. Add data, formulas, formatting
4. Save
5. Recalculate: `python recalc.py output.xlsx`
6. Verify and fix any errors from JSON output

## User Request
$ARGUMENTS
