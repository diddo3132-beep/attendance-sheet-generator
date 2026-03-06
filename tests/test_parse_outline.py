"""测试 parse_outline 模块"""
import sys
import os
import tempfile
import json
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parse_outline import save_courses, clean_content


class TestParseOutline(unittest.TestCase):
    def test_clean_content(self):
        text = "第一行\n版本/修订\n第二行\n  备注  \n第三行"
        out = clean_content(text)
        self.assertIn("第一行", out)
        self.assertIn("第二行", out)
        self.assertIn("第三行", out)
        self.assertNotIn("版本/修订", out)
        self.assertNotIn("备注", out)

    def test_save_courses(self):
        courses = [
            {"code": "T-001", "name": "测试课程", "hours": "4", "content": "内容"},
        ]
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "sub", "courses.json")
            save_courses(courses, path)
            self.assertTrue(os.path.isfile(path))
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data[0]["code"], "T-001")


if __name__ == "__main__":
    unittest.main()
