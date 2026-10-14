# W5 — 课程论文

## 何时用

结课论文、课程报告、大作业论文。用户说「课程论文」「结课」「大作业」。

不执行顶刊对标。按课程要求交付,尺度以课程评分标准为准。

## 步骤

```
1 of 4  提纲         → OUTLINE.md
2 of 4  撰写         → paper/main.md
3 of 4  审查         → AUDIT_REPORT.md
4 of 4  导出         → paper/main.docx
```

可选插入:若课程要求数据分析,在步骤 1 与 2 之间插入 `data-figures.md` 的步骤 1–3。

## 各步骤

### 步骤 1 — 提纲

产出 `OUTLINE.md`:章节、每节要点、字数分配、参考文献初步清单。

闸门:
```yaml
- {kind: machine, check: min_size, file: OUTLINE.md, bytes: 400}
- {kind: machine, check: regex, file: OUTLINE.md, pattern: '^#{1,3}\s*\d'}
```

### 步骤 2 — 撰写

产出 `paper/main.md`,按提纲扩写。

闸门:
```yaml
- {kind: machine, check: min_size, file: paper/main.md, bytes: 3000}
- {kind: machine, check: contains, file: paper/main.md, text: 参考文献}
- {kind: falsifiable_check, claim: 正文字数与课程要求相符}
```

### 步骤 3 — 审查

调用:`academic-paper-reviewer`(轻量模式)

产出 `AUDIT_REPORT.md`:结构完整性、引用规范、事实性错误、语言问题。

闸门:
```yaml
- {kind: machine, check: required_files, files: [AUDIT_REPORT.md]}
- {kind: semantic, claim: 审查意见逐条有处理, verify_by: 用户验收}
```

### 步骤 4 — 导出

产出 `paper/main.docx`。DOCX 转换后逐页检查公式与表格。

闸门:
```yaml
- {kind: machine, check: required_files, files: [paper/main.docx]}
```

## 与其他工作流的差别

| 项 | W1 论文写作 | W5 课程论文 |
|----|------------|------------|
| 对标 | Nature 大子刊 | 课程评分标准 |
| 文献量 | 15 条以上、逐条核实 | 课程要求为准 |
| 图表 | 论文级 | 说明清楚即可 |
| 审稿 | 六角色红队 | 轻量审查 |
| 迭代 | 多轮打磨 | 一轮审查 |
