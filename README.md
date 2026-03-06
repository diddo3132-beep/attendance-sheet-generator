# 考勤表生成助手 / Attendance Sheet Generator

通用的培训考勤表自动生成工具。从课程大纲 PDF 中提取课程信息，结合用户输入的培训数据，自动填充 Word 考勤表模板。适用于各类培训、讲座、会议的签到表制作。

A general-purpose tool for generating training attendance sheets. It extracts course data from syllabus PDFs and fills Word templates automatically.

## 功能 / Features

- **PDF 大纲解析** — 从课程大纲 PDF 中批量提取课程代码、名称、课时、教学内容（需包含「课程名称」「课程代码」「课时」「教学内容」等字段）
- **考勤表自动填充** — 根据选定课程和学员名单，自动填充 Word 模板
- **图形界面** — 基于 tkinter 的 GUI，支持下拉选课、粘贴学员名单、一键生成
- **Windows 打包** — 可通过 PyInstaller 打包为单文件 .exe

## 安装 / Installation

```bash
pip install python-docx pdfplumber
```

## 快速开始 / Quick Start

### 1. 准备模板

首次使用可运行 `python create_template.py` 生成通用模板，或将自己的 Word 模板放入 `template/` 文件夹并命名为 `考勤表模板.docx`。

模板要求：第一个表格 27 行 x 13 列，结构见 `generate_docx.py` 注释。

### 2. 导入课程数据

在 GUI 的「导入大纲」中，选择课程大纲 PDF。PDF 需包含「课程名称」「课程代码」「课时」「教学内容」等标准字段。

### 3. 生成考勤表

选择课程、填写日期/教员/地点、粘贴学员名单（每行：工号 Tab 姓名），点击生成。

## 项目结构 / Project Structure

```
attendance_tool/
├── app.py               # GUI 主程序
├── main.py              # 命令行主程序
├── create_template.py   # 生成通用模板
├── generate_docx.py     # Word 模板填充
├── parse_outline.py     # PDF 大纲解析
├── input_parser.py      # 用户输入解析
├── course_db.py         # 课程数据库
├── inspect_template.py  # 模板结构检查工具
├── build.bat            # Windows 打包脚本
├── template/            # 模板目录
├── data/                # 课程数据
└── output/              # 生成的考勤表
```

## 在 Windows 上打包为 .exe

1. 安装 Python 3.8+（勾选 Add to PATH）
2. 双击 `build.bat`
3. 在 `dist/` 中获取 `考勤表助手.exe`

## 许可证 / License

[MIT License](LICENSE)
