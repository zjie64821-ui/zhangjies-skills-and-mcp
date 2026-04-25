#!/usr/bin/env python3
"""
DOCX 格式提取器 — 从任意 DOCX 文档中提取完整格式档案
用法: python3 format_extractor.py <input.docx> [output.json]

输出: JSON 格式档案，包含页面设置、段落样式、字体、字号、行距、缩进等全部格式信息
"""

import sys
import json
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm, Inches, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH


def emu_to_cm(emu):
    """将 EMU 单位转换为厘米"""
    if emu is None:
        return None
    return round(emu / 914400 * 2.54, 2)


def emu_to_pt(emu):
    """将 EMU 单位转换为磅"""
    if emu is None:
        return None
    return round(emu / 12700, 1)


def alignment_name(align):
    """对齐方式枚举转字符串"""
    mapping = {
        WD_ALIGN_PARAGRAPH.LEFT: "left",
        WD_ALIGN_PARAGRAPH.CENTER: "center",
        WD_ALIGN_PARAGRAPH.RIGHT: "right",
        WD_ALIGN_PARAGRAPH.JUSTIFY: "justify",
        WD_ALIGN_PARAGRAPH.DISTRIBUTE: "distribute",
    }
    return mapping.get(align, str(align) if align else None)


def extract_font(run):
    """提取 run 级别的字体信息"""
    font = run.font
    return {
        "name_ascii": font.name,
        "name_eastasia": getattr(font, '_element',
                                  {}).get(qn('w:eastAsia')) if False else None,
        "size_pt": emu_to_pt(font.size) if font.size else None,
        "bold": font.bold,
        "italic": font.italic,
        "underline": font.underline,
        "color_rgb": str(font.color.rgb) if font.color and font.color.rgb else None,
        "superscript": font.superscript,
        "subscript": font.subscript,
    }


def extract_paragraph_format(para):
    """提取段落格式"""
    pf = para.paragraph_format
    return {
        "alignment": alignment_name(pf.alignment),
        "line_spacing": pf.line_spacing,
        "line_spacing_rule": str(pf.line_spacing_rule) if pf.line_spacing_rule else None,
        "space_before_pt": emu_to_pt(pf.space_before) if pf.space_before else None,
        "space_after_pt": emu_to_pt(pf.space_after) if pf.space_after else None,
        "first_line_indent_cm": emu_to_cm(pf.first_line_indent) if pf.first_line_indent else None,
        "left_indent_cm": emu_to_cm(pf.left_indent) if pf.left_indent else None,
        "right_indent_cm": emu_to_cm(pf.right_indent) if pf.right_indent else None,
    }


def extract_page_setup(doc):
    """提取页面设置"""
    sections = []
    for i, section in enumerate(doc.sections):
        sec = {
            "section_index": i,
            "page_width_cm": emu_to_cm(section.page_width),
            "page_height_cm": emu_to_cm(section.page_height),
            "top_margin_cm": emu_to_cm(section.top_margin),
            "bottom_margin_cm": emu_to_cm(section.bottom_margin),
            "left_margin_cm": emu_to_cm(section.left_margin),
            "right_margin_cm": emu_to_cm(section.right_margin),
            "header_distance_cm": emu_to_cm(section.header_distance),
            "footer_distance_cm": emu_to_cm(section.footer_distance),
            "gutter_cm": emu_to_cm(section.gutter),
            "orientation": str(section.orientation) if section.orientation else None,
        }
        # 页眉页脚内容
        if section.header and section.header.paragraphs:
            sec["header_text"] = " | ".join(
                p.text for p in section.header.paragraphs if p.text.strip()
            )
        if section.footer and section.footer.paragraphs:
            sec["footer_text"] = " | ".join(
                p.text for p in section.footer.paragraphs if p.text.strip()
            )
        sections.append(sec)
    return sections


def extract_styles(doc):
    """提取文档中定义的样式"""
    styles_info = {}
    for style in doc.styles:
        if style.type is not None:  # 跳过 None 类型
            style_data = {
                "style_id": style.style_id,
                "name": style.name,
                "type": str(style.type),
                "base_style": style.base_style.name if style.base_style else None,
                "builtin": style.builtin,
            }
            # 段落样式提取格式
            if hasattr(style, 'paragraph_format') and style.paragraph_format:
                pf = style.paragraph_format
                style_data["paragraph_format"] = {
                    "alignment": alignment_name(pf.alignment),
                    "line_spacing": pf.line_spacing,
                    "line_spacing_rule": str(pf.line_spacing_rule) if pf.line_spacing_rule else None,
                    "space_before_pt": emu_to_pt(pf.space_before) if pf.space_before else None,
                    "space_after_pt": emu_to_pt(pf.space_after) if pf.space_after else None,
                    "first_line_indent_cm": emu_to_cm(pf.first_line_indent) if pf.first_line_indent else None,
                }
            # 字体样式
            if hasattr(style, 'font') and style.font:
                f = style.font
                style_data["font"] = {
                    "name": f.name,
                    "size_pt": emu_to_pt(f.size) if f.size else None,
                    "bold": f.bold,
                    "italic": f.italic,
                    "color_rgb": str(f.color.rgb) if f.color and f.color.rgb else None,
                }
            styles_info[style.name] = style_data
    return styles_info


def extract_paragraphs(doc, max_paragraphs=200):
    """提取段落内容和格式（限制数量避免过大）"""
    paragraphs = []
    for i, para in enumerate(doc.paragraphs[:max_paragraphs]):
        para_data = {
            "index": i,
            "style_name": para.style.name if para.style else None,
            "text_preview": para.text[:100] if para.text else "",
            "format": extract_paragraph_format(para),
            "runs": [],
        }
        for run in para.runs:
            run_data = extract_font(run)
            run_data["text_preview"] = run.text[:50] if run.text else ""
            para_data["runs"].append(run_data)
        paragraphs.append(para_data)
    return paragraphs


def extract_tables(doc, max_tables=20):
    """提取表格格式"""
    tables = []
    for i, table in enumerate(doc.tables[:max_tables]):
        table_data = {
            "table_index": i,
            "rows": len(table.rows),
            "cols": len(table.columns),
            "style": table.style.name if table.style else None,
            "alignment": str(table.alignment) if table.alignment else None,
            "cells_sample": [],
        }
        # 提取前 3 行的单元格格式作为样本
        for row_idx, row in enumerate(table.rows[:3]):
            for col_idx, cell in enumerate(row.cells):
                for para in cell.paragraphs:
                    if para.text.strip():
                        table_data["cells_sample"].append({
                            "row": row_idx,
                            "col": col_idx,
                            "text_preview": para.text[:60],
                            "format": extract_paragraph_format(para),
                            "runs": [
                                {**extract_font(r), "text_preview": r.text[:30]}
                                for r in para.runs[:3]
                            ] if para.runs else [],
                        })
                        break
        tables.append(table_data)
    return tables


def build_format_profile(doc_path):
    """构建完整的格式档案"""
    doc = Document(doc_path)

    profile = {
        "source_file": str(doc_path),
        "format_version": "1.0",
        "page_setup": extract_page_setup(doc),
        "styles": extract_styles(doc),
        "paragraphs": extract_paragraphs(doc),
        "tables": extract_tables(doc),
    }

    # 统计信息
    profile["stats"] = {
        "total_paragraphs": len(doc.paragraphs),
        "total_tables": len(doc.tables),
        "total_sections": len(doc.sections),
        "styles_used": list(set(
            p.style.name for p in doc.paragraphs
            if p.style and p.text.strip()
        )),
    }

    return profile


def main():
    if len(sys.argv) < 2:
        print("用法: python3 format_extractor.py <input.docx> [output.json]")
        print("  不指定 output.json 时输出到 stdout")
        sys.exit(1)

    doc_path = sys.argv[1]
    if not Path(doc_path).exists():
        print(f"文件不存在: {doc_path}")
        sys.exit(1)

    profile = build_format_profile(doc_path)
    json_str = json.dumps(profile, ensure_ascii=False, indent=2)

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
        Path(output_path).write_text(json_str, encoding='utf-8')
        print(f"格式档案已保存到: {output_path}")
        print(f"页面设置: {len(profile['page_setup'])} 个节")
        print(f"段落分析: {profile['stats']['total_paragraphs']} 个段落")
        print(f"表格分析: {profile['stats']['total_tables']} 个表格")
        print(f"使用的样式: {profile['stats']['styles_used']}")
    else:
        print(json_str)


if __name__ == "__main__":
    main()
