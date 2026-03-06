#!/usr/bin/env python3
"""
考勤表生成助手
用法：python3 main.py
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COURSES_JSON = os.path.join(BASE_DIR, 'data', 'courses.json')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'template', '考勤表模板.docx')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

from parse_outline import extract_courses_from_pdf, save_courses
from course_db import load_courses, get_course_by_code
from input_parser import parse_user_input
from generate_docx import fill_attendance_template


def update_database(pdf_path):
    print("正在解析大纲...")
    courses = extract_courses_from_pdf(pdf_path)
    save_courses(courses, COURSES_JSON)
    print(f"数据库更新完成，共 {len(courses)} 门课程")


def main():
    if not os.path.exists(TEMPLATE_PATH):
        print(f"错误：模板文件不存在 {TEMPLATE_PATH}")
        print("请将 Word 模板放到 template 文件夹，并重命名为 '考勤表模板.docx'")
        print("\n提示：先运行 inspect_template.py 检查模板结构")
        return

    if not os.path.exists(COURSES_JSON):
        print("未找到课程数据库，请先提供维修工程教学大纲 PDF 路径：")
        pdf = input("PDF 路径：").strip().strip('"').strip("'")
        if not os.path.exists(pdf):
            print(f"文件不存在：{pdf}")
            return
        update_database(pdf)

    courses = load_courses(COURSES_JSON)

    while True:
        print("\n" + "=" * 50)
        print("考勤表生成助手")
        print("1. 更新课程数据库（重新解析大纲）")
        print("2. 生成考勤表")
        print("3. 检查模板结构")
        print("4. 退出")
        choice = input("请选择操作：").strip()

        if choice == '1':
            pdf = input("请输入 PDF 路径：").strip().strip('"').strip("'")
            if os.path.exists(pdf):
                update_database(pdf)
                courses = load_courses(COURSES_JSON)
            else:
                print(f"文件不存在：{pdf}")

        elif choice == '2':
            print("\n请按以下格式输入（输入完成后按两次回车）：")
            print("---")
            print("课程代码：A-030")
            print("培训日期：2026-03-06")
            print("培训时间：14:00-16:00")
            print("教员姓名：张三")
            print("培训地点：3号教室")
            print("学员名单：")
            print("1001\t李雷")
            print("1002\t韩梅梅")
            print("---")

            lines = []
            empty_count = 0
            while True:
                line = input()
                if line.strip() == '':
                    empty_count += 1
                    if empty_count >= 1:
                        break
                else:
                    empty_count = 0
                    lines.append(line)

            user_text = '\n'.join(lines)
            user_info = parse_user_input(user_text)

            if not user_info['code']:
                print("错误：未提供课程代码")
                continue

            course = get_course_by_code(user_info['code'], courses)
            if not course:
                print(f"错误：未找到课程代码 {user_info['code']}")
                print("已有课程代码：")
                for c in courses[:10]:
                    print(f"  {c['code']} - {c['name']}")
                if len(courses) > 10:
                    print(f"  ...共 {len(courses)} 门课程")
                continue

            filename = f"{user_info['date']}_{user_info['code']}_考勤表.docx"
            output_path = os.path.join(OUTPUT_DIR, filename)

            try:
                fill_attendance_template(TEMPLATE_PATH, output_path, course, user_info)
                print(f"\n生成成功！文件: {output_path}")
            except Exception as e:
                print(f"生成失败：{e}")
                import traceback
                traceback.print_exc()

        elif choice == '3':
            from inspect_template import inspect_template
            inspect_template(TEMPLATE_PATH)

        elif choice == '4':
            break
        else:
            print("无效选择")


if __name__ == '__main__':
    main()
