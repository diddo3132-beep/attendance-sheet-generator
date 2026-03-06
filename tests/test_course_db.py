"""测试 course_db 模块"""
import sys
import os
import json
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from course_db import load_courses, get_course_by_code


class TestCourseDb(unittest.TestCase):
    def test_get_course_by_code(self):
        courses = [
            {"code": "T-001", "name": "Python 入门", "hours": "8", "content": ""},
            {"code": "a-030", "name": "安全培训", "hours": "4", "content": ""},
        ]
        self.assertEqual(get_course_by_code("T-001", courses)["name"], "Python 入门")
        self.assertEqual(get_course_by_code("t-001", courses)["name"], "Python 入门")
        self.assertEqual(get_course_by_code("A-030", courses)["name"], "安全培训")
        self.assertIsNone(get_course_by_code("X-999", courses))

    def test_load_courses(self):
        data = [
            {"code": "C1", "name": "课程一", "hours": "2", "content": ""},
        ]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            path = f.name
        try:
            loaded = load_courses(path)
            self.assertEqual(len(loaded), 1)
            self.assertEqual(loaded[0]["code"], "C1")
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
