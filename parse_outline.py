#!/usr/bin/env python3
"""从课程大纲 PDF 中提取课程信息，支持通过 config/parse_config.json 自定义解析规则"""
import re
import json
import os
import sys

try:
    import pdfplumber
except ImportError:
    os.system(f"{sys.executable} -m pip install pdfplumber")
    import pdfplumber

_BASE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_CONFIG = {
    "block_split": "课程名称",
    "name": {"pattern": r"课程名称\s+([^\n]+)"},
    "code": {"pattern": r"课程代码\s+([A-Za-z0-9\-]+)"},
    "hours": {"pattern": r"课时\s+(\d+)"},
    "content_end_keywords": ["考核方式", "复训间隔", "课程名称"],
    "skip_in_content": [
        "版本/修订", "此页有意留空白", "备注", "注：", "页眉", "页码",
        r"^\d+\s*/\s*\d+$", r"^\d+$"
    ],
}


def _load_parse_config():
    path = os.path.join(_BASE, "config", "parse_config.json")
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            return {**_DEFAULT_CONFIG, **cfg}
        except (json.JSONDecodeError, TypeError):
            pass
    return _DEFAULT_CONFIG


def clean_content(text, skip_patterns=None):
    """清洗教学内容文本"""
    cfg = _load_parse_config()
    skip = skip_patterns or cfg.get("skip_in_content", _DEFAULT_CONFIG["skip_in_content"])
    pat_str = "|".join(f"({s})" for s in skip)
    regex = re.compile(pat_str, re.IGNORECASE)
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line or regex.search(line):
            continue
        line = re.sub(r"[\|\+\-\:\—]+", " ", line)
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            cleaned.append(line)
    return "；".join(cleaned)


def extract_courses_from_pdf(pdf_path):
    cfg = _load_parse_config()
    block_split = cfg.get("block_split", "课程名称")
    name_pat = cfg.get("name", {}).get("pattern", _DEFAULT_CONFIG["name"]["pattern"])
    code_pat = cfg.get("code", {}).get("pattern", _DEFAULT_CONFIG["code"]["pattern"])
    hours_pat = cfg.get("hours", {}).get("pattern", _DEFAULT_CONFIG["hours"]["pattern"])
    content_end = cfg.get("content_end_keywords", _DEFAULT_CONFIG["content_end_keywords"])
    content_end_re = "|".join(re.escape(k) for k in content_end)

    courses = []
    with pdfplumber.open(pdf_path) as pdf:
        pages_text = [page.extract_text() or "" for page in pdf.pages]
    full_text = "\n".join(pages_text)
    split_re = rf"(?=\n\s*{re.escape(block_split)}\s+)"
    course_blocks = re.split(split_re, full_text)

    for block in course_blocks:
        if not block.strip():
            continue
        name_m = re.search(name_pat, block)
        if not name_m:
            continue
        name = name_m.group(1).strip()
        code_m = re.search(code_pat, block)
        if not code_m:
            continue
        code = code_m.group(1).strip()
        hours_m = re.search(hours_pat, block)
        hours = hours_m.group(1).strip() if hours_m else ""
        content_pat = rf"教学内容\s+([\s\S]+?)(?=\n\s*(?:{content_end_re}|$))"
        content_m = re.search(content_pat, block, re.DOTALL)
        content = clean_content(content_m.group(1)) if content_m else ""
        courses.append({"code": code, "name": name, "hours": hours, "content": content})
    return courses


def save_courses(courses, json_path="data/courses.json"):
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)
