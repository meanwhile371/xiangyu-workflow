# W5 — 课程论文

## 何时用

结课论文、课程报告、大作业论文。用户说「课程论文」「结课」「大作业」。

不执行顶刊对标。按课程要求交付,尺度以课程评分标准为准。

## 步骤

1 of 4  提纲 → OUTLINE.md
2 of 4  撰写 → paper/main.md
3 of 4  审查 → AUDIT_REPORT.md
4 of 4  导出 → paper/main.docx

可选插入: 若课程要求数据分析,在步骤1与2之间插入 data-figures.md 的步骤1-3。

## 各步骤

### 步骤 1 — 提纲

产出 OUTLINE.md: 章节、每节要点、字数分配、参考文献初步清单。

闸门:
- {kind: machine, check: min_size, file: OUTLINE.md, bytes: 400}
- {kind: machine, check: regex, file: OUTLINE.md, pattern: '#{1,3}\s*\d'}

### 步骤 2 — 撰写

产出 paper/main.md,按提纲扩写。

闸门:
- {kind: machine, check: min_size, file: paper/main.md, bytes: 3000}
- {kind: machine, check: contains, file: paper/main.md, text: 参考文献}
- {kind: falsifiable_check, claim: 正文字数与课程要求相符}

### 步骤 3 — 审查

产出 AUDIT_REPORT.md: 结构完整性、引用规范、事实性错误、语言问题。

嵌入轻量审查清单(课程论文级别,非顶刊标准):

结构完整性检查:
- 标题、摘要、关键词是否齐全
- 引言-正文-结论逻辑是否连贯
- 章节编号是否正确
- 参考文献格式是否统一

引用规范检查:
- 每处引用是否有出处
- 参考文献列表是否与正文引用对应
- 引用格式是否符合课程要求(APA/MLA/GB等)
- 是否有悬空引用(正文引了但列表里没有)

事实性错误检查:
- 数据、统计量是否有明显错误
- 公式、算法描述是否有逻辑矛盾
- 图表编号与正文引用是否一致
- 关键术语使用是否准确

语言问题检查:
- 是否有明显语法错误
- 是否有口语化表达
- 专业术语是否规范
- 句子是否过长或过于复杂

自动检测项:
- 字数统计
- 引用数量
- 图表数量
- 章节数量
- 重复段落检测(简单文本匹配)

闸门:
- {kind: machine, check: required_files, files: [AUDIT_REPORT.md]}
- {kind: semantic, claim: 审查意见逐条有处理, verify_by: 用户验收}

### 步骤 4 — 导出

产出 paper/main.docx。用 pandoc 转换:

pandoc paper/main.md -o paper/main.docx --reference-doc=template.docx

转换后检查:
- 公式是否正确渲染
- 表格是否正常
- 图片是否嵌入
- 格式是否符合课程要求

闸门:
- {kind: machine, check: required_files, files: [paper/main.docx]}

## 与其他工作流的差别

项 | W1 论文写作 | W5 课程论文
对标 | Nature 大子刊 | 课程评分标准
文献量 | 15条以上、逐条核实 | 课程要求为准
图表 | 论文级 | 说明清楚即可
审稿 | 六角色红队 | 轻量审查
迭代 | 多轮打磨 | 一轮审查
