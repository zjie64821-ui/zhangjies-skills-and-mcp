#!/usr/bin/env python3
"""
DOCX 格式克隆渲染器 — 根据格式档案和内容生成格式完全一致的 Word 文档
用法: python3 format_cloner.py <format_profile.json> <output.docx>

工作原理:
1. 读取格式档案（从样本文档中提取的格式信息）
2. 根据内容指令构建新文档
3. 精确应用样本文档的每一个格式参数
"""

import sys
import json
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm, Inches, Emu, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_ORIENT


ALIGNMENT_MAP = {
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
    "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
    "distribute": WD_ALIGN_PARAGRAPH.DISTRIBUTE,
}


def cm_to_emu(cm):
    """厘米转 EMU"""
    if cm is None:
        return None
    return int(cm / 2.54 * 914400)


def pt_to_emu(pt):
    """磅转 EMU"""
    if pt is None:
        return None
    return int(pt * 12700)


def apply_page_setup(doc, page_setup_list):
    """应用页面设置"""
    for i, sec_data in enumerate(page_setup_list):
        if i == 0:
            section = doc.sections[0]
        else:
            # 添加新节
            doc.add_section()
            section = doc.sections[-1]

        if sec_data.get("page_width_cm"):
            section.page_width = Cm(sec_data["page_width_cm"])
        if sec_data.get("page_height_cm"):
            section.page_height = Cm(sec_data["page_height_cm"])
        if sec_data.get("top_margin_cm"):
            section.top_margin = Cm(sec_data["top_margin_cm"])
        if sec_data.get("bottom_margin_cm"):
            section.bottom_margin = Cm(sec_data["bottom_margin_cm"])
        if sec_data.get("left_margin_cm"):
            section.left_margin = Cm(sec_data["left_margin_cm"])
        if sec_data.get("right_margin_cm"):
            section.right_margin = Cm(sec_data["right_margin_cm"])
        if sec_data.get("header_distance_cm"):
            section.header_distance = Cm(sec_data["header_distance_cm"])
        if sec_data.get("footer_distance_cm"):
            section.footer_distance = Cm(sec_data["footer_distance_cm"])


def apply_paragraph_format(paragraph, fmt):
    """应用段落格式"""
    pf = paragraph.paragraph_format

    if fmt.get("alignment") and fmt["alignment"] in ALIGNMENT_MAP:
        pf.alignment = ALIGNMENT_MAP[fmt["alignment"]]

    if fmt.get("line_spacing"):
        pf.line_spacing = fmt["line_spacing"]

    if fmt.get("line_spacing_rule"):
        rule_str = fmt["line_spacing_rule"]
        rule_map = {
            "SINGLE (1)": WD_LINE_SPACING.SINGLE,
            "ONE_POINT_FIVE (1)": WD_LINE_SPACING.ONE_POINT_FIVE,
            "DOUBLE (2)": WD_LINE_SPACING.DOUBLE,
            "AT_LEAST (3)": WD_LINE_SPACING.AT_LEAST,
            "EXACTLY (4)": WD_LINE_SPACING.EXACTLY,
            "MULTIPLE (5)": WD_LINE_SPACING.MULTIPLE,
        }
        for key, val in rule_map.items():
            if key in rule_str:
                pf.line_spacing_rule = val
                break

    if fmt.get("space_before_pt"):
        pf.space_before = Pt(fmt["space_before_pt"])
    if fmt.get("space_after_pt"):
        pf.space_after = Pt(fmt["space_after_pt"])
    if fmt.get("first_line_indent_cm"):
        pf.first_line_indent = Cm(fmt["first_line_indent_cm"])
    if fmt.get("left_indent_cm"):
        pf.left_indent = Cm(fmt["left_indent_cm"])
    if fmt.get("right_indent_cm"):
        pf.right_indent = Cm(fmt["right_indent_cm"])


def apply_run_format(run, font_info):
    """应用 run 级别字体格式"""
    if font_info.get("name_ascii"):
        run.font.name = font_info["name_ascii"]
    if font_info.get("size_pt"):
        run.font.size = Pt(font_info["size_pt"])
    if font_info.get("bold") is not None:
        run.font.bold = font_info["bold"]
    if font_info.get("italic") is not None:
        run.font.italic = font_info["italic"]
    if font_info.get("underline") is not None:
        run.font.underline = font_info["underline"]
    if font_info.get("color_rgb"):
        run.font.color.rgb = RGBColor.from_string(font_info["color_rgb"])
    if font_info.get("superscript"):
        run.font.superscript = True
    if font_info.get("subscript"):
        run.font.subscript = True


def find_matching_style_para(paragraphs, style_name):
    """在格式档案中找到匹配样式的段落格式"""
    for p in paragraphs:
        if p.get("style_name") == style_name and p.get("format"):
            return p
    return None


def find_first_content_para(paragraphs, style_name):
    """找到第一个有内容的指定样式段落（用于获取字体信息）"""
    for p in paragraphs:
        if p.get("style_name") == style_name and p.get("text_preview", "").strip():
            return p
    return None


def build_document(profile, content_sections):
    """
    根据格式档案和内容构建新文档

    content_sections 格式:
    [
        {
            "style": "Heading 1",           # 使用哪个样式
            "text": "第一章 绪论",           # 文本内容
            "runs": [                        # 可选：分 run 控制格式
                {"text": "第一章 ", "font_override": {...}},
                {"text": "绪论", "font_override": {...}},
            ]
        },
        ...
    ]
    """
    doc = Document()

    # 应用页面设置
    apply_page_setup(doc, profile.get("page_setup", []))

    # 构建样式映射
    styles_map = profile.get("styles", {})
    paras_profiles = profile.get("paragraphs", [])

    for section_data in content_sections:
        style_name = section_data.get("style", "Normal")
        text = section_data.get("text", "")

        # 尝试使用文档中已有的样式
        try:
            para = doc.add_paragraph(style=style_name)
        except KeyError:
            para = doc.add_paragraph()

        # 查找匹配的格式档案
        ref_para = find_matching_style_para(paras_profiles, style_name)
        if ref_para:
            apply_paragraph_format(para, ref_para["format"])

            # 如果没有自定义 runs，用参考段落的字体格式
            if not section_data.get("runs") and ref_para.get("runs"):
                run = para.add_run(text)
                if ref_para["runs"]:
                    apply_run_format(run, ref_para["runs"][0])
            elif not section_data.get("runs"):
                run = para.add_run(text)
                # 尝试从样式中获取字体信息
                if style_name in styles_map:
                    style_font = styles_map[style_name].get("font", {})
                    apply_run_format(run, style_font)
        else:
            # 没有找到匹配的段落格式，尝试从样式中获取
            run = para.add_run(text)
            if style_name in styles_map:
                style_info = styles_map[style_name]
                if "paragraph_format" in style_info:
                    apply_paragraph_format(para, style_info["paragraph_format"])
                if "font" in style_info:
                    apply_run_format(run, style_info["font"])

        # 处理自定义 runs
        if section_data.get("runs"):
            for run_data in section_data["runs"]:
                run = para.add_run(run_data.get("text", ""))
                if run_data.get("font_override"):
                    apply_run_format(run, run_data["font_override"])

    return doc


def build_from_instruction(profile, instruction_file):
    """
    从 JSON 指令文件构建文档

    指令文件格式:
    {
      "output_path": "output.docx",
      "content": [
        {"style": "Heading 1", "text": "标题"},
        {"style": "Normal", "text": "正文内容"},
        {"style": "Heading 2", "text": "子标题"},
        {"style": "Normal", "text": "更多内容"}
      ]
    }
    """
    with open(instruction_file, 'r', encoding='utf-8') as f:
        instruction = json.load(f)

    doc = build_document(profile, instruction.get("content", []))

    output_path = instruction.get("output_path", "output.docx")
    doc.save(output_path)
    print(f"文档已生成: {output_path}")
    print(f"段落数: {len(instruction.get('content', []))}")
    return output_path


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print("  python3 format_cloner.py <format_profile.json> <instruction.json>")
        print("  python3 format_cloner.py <format_profile.json> <output.docx> --empty")
        print()
        print("--empty 模式: 生成一个空白模板（只含页面设置和样式定义）")
        sys.exit(1)

    profile_path = sys.argv[1]
    second_arg = sys.argv[2]

    with open(profile_path, 'r', encoding='utf-8') as f:
        profile = json.load(f)

    if "--empty" in sys.argv:
        # 生成空白模板
        doc = Document()
        apply_page_setup(doc, profile.get("page_setup", []))
        doc.save(second_arg)
        print(f"空白模板已生成: {second_arg}")
    else:
        # 从指令文件构建
        build_from_instruction(profile, second_arg)


if __name__ == "__main__":
    main()
