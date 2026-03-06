"""测试 input_parser 模块"""
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from input_parser import parse_user_input


class TestParseUserInput(unittest.TestCase):
    def test_parse_full_input(self):
        text = """
课程代码：T-001
培训日期：2026-03-10
培训时间：09:00-12:00
教员姓名：王老师
培训地点：101 教室
学员名单：
1001	张三
1002	李四
"""
        info = parse_user_input(text)
        self.assertEqual(info["code"], "T-001")
        self.assertEqual(info["date"], "2026-03-10")
        self.assertEqual(info["time"], "09:00-12:00")
        self.assertEqual(info["instructor"], "王老师")
        self.assertEqual(info["location"], "101 教室")
        self.assertEqual(len(info["students"]), 2)
        self.assertEqual(info["students"][0], {"id": "1001", "name": "张三"})
        self.assertEqual(info["students"][1], {"id": "1002", "name": "李四"})

    def test_parse_english_colon(self):
        text = "课程代码: A-030\n培训日期: 2026-03-06"
        info = parse_user_input(text)
        self.assertEqual(info["code"], "A-030")
        self.assertEqual(info["date"], "2026-03-06")

    def test_parse_students_space_separated(self):
        text = "学员名单：\n1001 张三\n1002 李四"
        info = parse_user_input(text)
        self.assertEqual(
            info["students"],
            [{"id": "1001", "name": "张三"}, {"id": "1002", "name": "李四"}],
        )

    def test_parse_empty(self):
        info = parse_user_input("")
        self.assertIsNone(info["code"])
        self.assertEqual(info["students"], [])


if __name__ == "__main__":
    unittest.main()
