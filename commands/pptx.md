# PowerPoint Presentation Toolkit

Create, edit, and analyze .pptx files.

## Reading Content
- Text extraction: `python -m markitdown file.pptx`
- Raw XML: unpack with `python ooxml/scripts/unpack.py <file> <dir>`

## Creating New (without template)
Use html2pptx workflow:
1. Design HTML slides (720pt x 405pt for 16:9)
2. Convert with html2pptx.js library
3. Validate with thumbnails: `python scripts/thumbnail.py output.pptx`

## Design Principles
- Match palette to content/subject matter
- Web-safe fonts only: Arial, Helvetica, Georgia, Verdana, etc.
- Clear visual hierarchy through size, weight, color
- Two-column layout preferred for charts/tables (never stack vertically)

## Creating from Template
1. Extract text: `python -m markitdown template.pptx > content.md`
2. Create thumbnails: `python scripts/thumbnail.py template.pptx`
3. Analyze and create template inventory
4. Create outline with template mapping
5. Rearrange: `python scripts/rearrange.py template.pptx working.pptx 0,34,34,50`
6. Extract inventory: `python scripts/inventory.py working.pptx text-inventory.json`
7. Generate replacement JSON
8. Apply: `python scripts/replace.py working.pptx replacement-text.json output.pptx`

## Editing Existing
1. Unpack: `python ooxml/scripts/unpack.py <file> <dir>`
2. Edit XML files
3. Validate: `python ooxml/scripts/validate.py <dir> --original <file>`
4. Pack: `python ooxml/scripts/pack.py <dir> <file>`

## Convert to Images
```bash
soffice --headless --convert-to pdf template.pptx
pdftoppm -jpeg -r 150 template.pdf slide
```

## User Request
$ARGUMENTS
