"""测试 generate_docx 模块"""
import sys
import os
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(BASE, "template", "考勤表模板.docx")


class TestGenerateDocx(unittest.TestCase):
    def test_fill_attendance_template(self):
        if not os.path.isfile(TEMPLATE):
            self.skipTest("需要 template/考勤表模板.docx，请先运行 create_template.py")
        from generate_docx import fill_attendance_template
        from docx import Document

        course = {
            "code": "T-001",
            "name": "测试课程",
            "hours": "4",
            "content": "测试内容",
        }
        user_info = {
            "date": "2026-03-10",
            "time": "09:00-12:00",
            "instructor": "王老师",
            "location": "101 教室",
            "students": [
                {"id": "1001", "name": "张三"},
                {"id": "1002", "name": "李四"},
            ],
        }
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "out.docx")
            fill_attendance_template(TEMPLATE, out, course, user_info)
            self.assertTrue(os.path.isfile(out))
            doc = Document(out)
            table = doc.tables[0]
            self.assertEqual(table.rows[0].cells[2].text.strip(), "测试课程")
            self.assertEqual(table.rows[0].cells[11].text.strip(), "T-001")
            self.assertEqual(table.rows[7].cells[1].text.strip(), "1001")
            self.assertEqual(table.rows[7].cells[3].text.strip(), "张三")


if __name__ == "__main__":
    unittest.main()
