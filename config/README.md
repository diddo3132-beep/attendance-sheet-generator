# 解析配置

若你的课程大纲 PDF 格式与默认不同，可复制 `parse_config.example.json` 为 `parse_config.json` 并修改匹配规则。

| 字段 | 说明 |
|------|------|
| block_split | 用于分割课程块的标题（默认「课程名称」） |
| name.pattern | 课程名称的正则，需含一个捕获组 |
| code.pattern | 课程代码的正则，需含一个捕获组 |
| hours.pattern | 课时的正则，需含一个捕获组 |
| content_end_keywords | 教学内容结束前的关键词列表 |
| skip_in_content | 教学内容中要过滤掉的关键词或正则列表 |

`parse_config.json` 已在 .gitignore 中，不会提交到仓库。
