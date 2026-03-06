#!/usr/bin/env python3
"""从维修工程教学大纲 PDF 中提取课程信息"""
import re
import json
import os
import sys

try:
    import pdfplumber
except ImportError:
    os.system(f"{sys.executable} -m pip install pdfplumber")
    import pdfplumber


def clean_content(text):
    """清洗教学内容文本"""
    lines = text.split('\n')
    cleaned = []
    skip_patterns = re.compile(
        r'版本/修订|维修工程教学大纲|CSS-DEP-JXDG|^\d+\s*/\s*\d+$|^\d+$'
        r'|此页有意留空白|备注|注：|复训|页眉|页码',
        re.IGNORECASE
    )
    for line in lines:
        line = line.strip()
        if not line or skip_patterns.search(line):
            continue
        line = re.sub(r'[\|\+\-\:\—]+', ' ', line)
        line = re.sub(r'\s+', ' ', line).strip()
        if line:
            cleaned.append(line)
    return '；'.join(cleaned)


def extract_courses_from_pdf(pdf_path):
    courses = []
    with pdfplumber.open(pdf_path) as pdf:
        pages_text = [page.extract_text() or '' for page in pdf.pages]

    full_text = '\n'.join(pages_text)
    course_blocks = re.split(r'(?=\n\s*课程名称\s+)', full_text)

    for block in course_blocks:
        if not block.strip():
            continue

        name_match = re.search(r'课程名称\s+([^\n]+)', block)
        if not name_match:
            continue
        name = name_match.group(1).strip()

        code_match = re.search(r'课程代码\s+([A-Z0-9\-]+)', block)
        if not code_match:
            continue
        code = code_match.group(1).strip()

        hours_match = re.search(r'课时\s+(\d+)', block)
        hours = hours_match.group(1).strip() if hours_match else ""

        content_pattern = r'教学内容\s+([\s\S]+?)(?=\n\s*(?:考核方式|复训间隔|课程名称|$))'
        content_match = re.search(content_pattern, block, re.DOTALL)
        content = clean_content(content_match.group(1)) if content_match else ""

        courses.append({
            'code': code,
            'name': name,
            'hours': hours,
            'content': content
        })

    return courses


def save_courses(courses, json_path='data/courses.json'):
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)
