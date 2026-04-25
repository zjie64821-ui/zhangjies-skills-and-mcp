# Word Document Toolkit

Create, edit, and analyze .docx files with tracked changes support.

## Decision Tree
- **Read/Analyze**: `pandoc --track-changes=all file.docx -o output.md`
- **Create New**: Use docx-js (JavaScript) with Document, Paragraph, TextRun → Packer.toBuffer()
- **Edit Existing**: Use OOXML manipulation:
  1. Unpack: `python ooxml/scripts/unpack.py <file> <dir>`
  2. Edit XML with Document library (Python)
  3. Pack: `python ooxml/scripts/pack.py <dir> <file>`
- **Redlining (tracked changes)**: Minimal, precise edits only marking changed text

## Key File Structure (unpacked)
- `word/document.xml` - main content
- `word/comments.xml` - comments
- `word/media/` - embedded images
- Tracked changes: `<w:ins>` (insertions), `<w:del>` (deletions)

## Convert to Images
```bash
soffice --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

## Dependencies
- pandoc, docx (npm), LibreOffice, poppler-utils, defusedxml

## User Request
$ARGUMENTS
