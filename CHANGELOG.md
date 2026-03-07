# 更新日志

## [0.2.0] - 2026-03

### 新增

- PDF 解析配置化：`config/parse_config.json` 支持自定义正则，适配不同大纲格式
- `config/parse_config.example.json` 与 `config/README.md` 配置说明
- README 增加适用场景、示例、配置说明
- GitHub Issue 模板（Bug / 功能建议）、PR 模板

---

## [0.1.0] - 2026-03

### 新增

- 从课程大纲 PDF 解析课程信息（课程名称、课程代码、课时、教学内容）
- Word 考勤表模板自动填充（27 行 x 13 列结构）
- tkinter GUI：导入大纲、生成考勤表、设置模板路径
- 命令行入口 `main.py`
- 通用模板生成脚本 `create_template.py`
- Windows 打包脚本 `build.bat`（PyInstaller）
- 单元测试（input_parser、course_db、parse_outline、generate_docx）
- 项目配置 `pyproject.toml`、贡献指南 `CONTRIBUTING.md`

### 说明

- 模板结构需与 `generate_docx.py` 中约定一致，可用 `inspect_template.py` 检查
- 首次使用可运行 `create_template.py` 生成默认模板
