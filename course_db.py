#!/usr/bin/env python3
"""课程数据库管理"""
import json


def load_courses(json_path='data/courses.json'):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_course_by_code(code, courses):
    code = code.strip().upper()
    for c in courses:
        if c['code'].strip().upper() == code:
            return c
    return None
