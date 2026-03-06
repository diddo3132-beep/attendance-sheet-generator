#!/usr/bin/env python3
"""解析用户输入的培训信息"""
import re


def parse_user_input(text):
    lines = text.strip().split('\n')
    info = {
        'code': None,
        'date': None,
        'time': None,
        'instructor': None,
        'location': None,
        'students': []
    }
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if line.startswith('课程代码：') or line.startswith('课程代码:'):
            info['code'] = line.split('：' if '：' in line else ':')[1].strip()
        elif line.startswith('培训日期：') or line.startswith('培训日期:'):
            info['date'] = line.split('：' if '：' in line else ':')[1].strip()
        elif line.startswith('培训时间：') or line.startswith('培训时间:'):
            info['time'] = line.split('：' if '：' in line else ':')[1].strip()
        elif line.startswith('教员姓名：') or line.startswith('教员姓名:'):
            info['instructor'] = line.split('：' if '：' in line else ':')[1].strip()
        elif line.startswith('培训地点：') or line.startswith('培训地点:'):
            info['location'] = line.split('：' if '：' in line else ':')[1].strip()
        elif line.startswith('学员名单：') or line.startswith('学员名单:'):
            j = i + 1
            while j < len(lines) and lines[j].strip():
                stu_line = lines[j].strip()
                parts = re.split(r'[\t ]+', stu_line)
                if len(parts) >= 2:
                    info['students'].append({'id': parts[0], 'name': parts[1]})
                j += 1
            i = j - 1
        i += 1
    return info
