---
name: pptx
description: >
  PowerPoint presentation (.pptx) processing toolkit. TRIGGER when the user needs to: create,
  edit, analyze, or design PowerPoint presentations; convert PPTX to/from other formats;
  work with slide layouts, templates, themes, or speaker notes.
  DO NOT trigger for PDF or Word presentations.
---

# PPTX Toolkit

## Reading Content
- Text: `python -m markitdown file.pptx`
- Raw XML: `python ooxml/scripts/unpack.py <file> <dir>`
- Key: `ppt/slides/slide{N}.xml`, `ppt/notesSlides/`, `ppt/media/`

## Creating New (html2pptx workflow)
1. Design HTML slides (720pt x 405pt for 16:9)
2. Convert with html2pptx.js: `node html2pptx.js`
3. Validate: `python scripts/thumbnail.py output.pptx`

## Design Principles
- Match palette to content subject
- Web-safe fonts: Arial, Helvetica, Georgia, Verdana
- Two-column layout for charts/tables (never stack vertically)
- 18 color palettes available (Teal & Coral, Black & Gold, etc.)

## Creating from Template
1. Extract text + thumbnails
2. Analyze → template inventory
3. Outline with template mapping
4. Rearrange: `python scripts/rearrange.py template.pptx working.pptx 0,34,50`
5. Extract inventory: `python scripts/inventory.py working.pptx text-inventory.json`
6. Replace text: `python scripts/replace.py working.pptx replacement.json output.pptx`

## Editing Existing
Unpack → Edit XML → Validate (`python ooxml/scripts/validate.py`) → Pack

## User Request
$ARGUMENTS
