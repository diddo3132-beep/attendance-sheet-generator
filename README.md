# 考勤表生成助手 / Attendance Sheet Generator

一个用于航空维修培训的考勤表自动生成工具。从教学大纲 PDF 中提取课程信息，结合用户输入的培训数据，自动填充 Word 考勤表模板。

A tool for generating attendance sheets for aviation maintenance training. It extracts course data from a training syllabus PDF and fills a Word template automatically.

## 功能 / Features

- **PDF 大纲解析** — 从维修工程教学大纲 PDF 中批量提取课程代码、名称、课时、教学内容
- **考勤表自动填充** — 根据选定课程和学员名单，自动填充 Word 模板中的所有字段
- **图形界面** — 基于 tkinter 的 GUI，支持下拉选课、粘贴学员名单、一键生成
- **Windows 打包** — 可通过 PyInstaller 打包为单文件 .exe，双击即用

## 截图 / Screenshot

```
┌──────────────────────────────────────┐
│  考勤表生成助手                       │
├──────────┬───────────┬───────────────┤
│ 生成考勤表 │  导入大纲  │     设置      │
├──────────┴───────────┴───────────────┤
│ 课程代码: [A-030 - 航空安全基础培训 ▼] │
│ 课程名称: 航空安全基础培训             │
│ 培训日期: 2026-03-06  培训时间: 08:30  │
│ 教员姓名: ________   培训地点: _______ │
│ ┌──────────────────────────────────┐ │
│ │ 1001  李雷                       │ │
│ │ 1002  韩梅梅                     │ │
│ │ 1003  王明                       │ │
│ └──────────────────────────────────┘ │
│  [生成考勤表]  [清空学员]  [打开文件夹] │
└──────────────────────────────────────┘
```

## 安装 / Installation

### 方式一：直接运行 Python 脚本

```bash
# 安装依赖
pip install python-docx pdfplumber

# 启动 GUI
python app.py

# 或使用命令行模式
python main.py
```

### 方式二：在 Windows 上打包为 .exe

1. 确保已安装 Python 3.8+（安装时勾选 **Add Python to PATH**）
2. 双击运行 `build.bat`
3. 打包完成后，`dist/` 文件夹中即为可运行的 `考勤表助手.exe`

## 使用方法 / Usage

### 1. 准备模板

将考勤表 Word 模板放入 `template/` 文件夹，命名为 `考勤表模板.docx`。

模板要求：第一个表格为考勤表，包含 27 行 x 13 列的固定结构（含合并单元格）。

### 2. 导入课程数据

在 GUI 的"导入大纲"标签页中，选择维修工程教学大纲 PDF 文件，程序会自动提取所有课程信息并保存到 `data/courses.json`。

### 3. 生成考勤表

1. 从下拉框选择课程代码
2. 填写培训日期、时间、教员姓名、培训地点
3. 在学员名单框中输入学员信息（每行：工号 + Tab + 姓名，可从 Excel 直接复制粘贴）
4. 点击"生成考勤表"
5. 生成的文件保存在 `output/` 文件夹中

## 项目结构 / Project Structure

```
attendance_tool/
├── app.py               # GUI 主程序（tkinter）
├── main.py              # 命令行主程序
├── generate_docx.py     # Word 模板填充模块
├── parse_outline.py     # PDF 大纲解析模块
├── input_parser.py      # 用户输入解析模块
├── course_db.py         # 课程数据库管理
├── inspect_template.py  # 模板结构检查工具
├── build.bat            # Windows 打包脚本
├── requirements.txt     # Python 依赖
├── template/            # Word 模板目录
│   └── 考勤表模板.docx
├── data/                # 课程数据（自动生成）
└── output/              # 生成的考勤表
```

## 依赖 / Dependencies

- Python 3.8+
- [python-docx](https://python-docx.readthedocs.io/) — Word 文档读写
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF 文本提取
- tkinter — GUI（Python 内置）

## 许可证 / License

[MIT License](LICENSE)
