# 贡献指南

欢迎参与考勤表生成助手项目。

## 如何贡献

1. **Fork** 本仓库
2. **克隆** 到本地：`git clone https://github.com/你的用户名/attendance-sheet-generator.git`
3. **创建分支**：`git checkout -b feature/你的功能名` 或 `fix/问题描述`
4. **修改代码**，保持风格一致
5. **运行测试**：`python -m unittest discover -s tests -v`
6. **提交**：`git commit -m "简短描述"`
7. **推送**：`git push origin feature/你的功能名`
8. 在 GitHub 上发起 **Pull Request**

## 代码风格

- Python：遵循 PEP 8，建议用 Black 格式化
- 注释与文档字符串：中文即可
- 提交信息：中文或英文均可，一句话说清改动

## 报告问题

- 使用 [Issues](https://github.com/diddo3132-beep/attendance-sheet-generator/issues) 提交 Bug 或建议
- Bug 请说明：系统环境、Python 版本、复现步骤、报错信息
- 功能建议请说明：使用场景与期望行为

## 开发环境

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v   # 运行测试
python app.py                # 启动 GUI
```

感谢你的贡献。
