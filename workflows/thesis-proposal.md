# W4 — 开题报告

## 何时用

学位论文开题、课题申报书、研究计划。用户说「开题」「开题报告」「proposal」「研究计划」。

## 步骤

```
1 of 4  背景与文献     → BACKGROUND.md
2 of 4  研究问题与方案  → PROPOSAL.md
3 of 4  技术路线图     → figures/技术路线.png
4 of 4  导出           → PROPOSAL.docx
```

## 各步骤

### 步骤 1 — 背景与文献

调用:`nature-academic-search` → `citation-check-skill`

产出 `BACKGROUND.md`:领域现状、已有工作、遗留问题、本课题的切入口。

闸门:
```yaml
- {kind: machine, check: min_size, file: BACKGROUND.md, bytes: 1500}
- {kind: machine, check: min_entries, file: BACKGROUND.md, min: 15}
- {kind: falsifiable_check, claim: 文献可溯源}
```

### 步骤 2 — 研究问题与方案

产出 `PROPOSAL.md`,结构对齐 `templates/RESEARCH_CONTRACT_TEMPLATE.md` 的模式:

```markdown
## 1 研究问题
## 2 核心主张
## 3 方法概要
## 4 实验/研究设计
## 5 已有基础与条件
## 6 预期成果
## 7 可行性与风险
## 8 进度安排
## 9 参考文献
```

为什么只留一个选题:候选方向往往有八到十个,全留在上下文里会污染工作记忆。定下一个,其余归档进 `alternatives/`,需要时再取。

闸门:
```yaml
- {kind: machine, check: min_size, file: PROPOSAL.md, bytes: 2500}
- {kind: machine, check: regex, file: PROPOSAL.md, pattern: '^##\s*\d+\s', min_matches: 6}
- {kind: semantic, claim: 研究问题可回答、可验证, verify_by: 用户验收}
```

### 步骤 3 — 技术路线图

产出 `figures/技术路线.png`,drawio 绘制。

闸门:
```yaml
- {kind: machine, check: glob_count, glob: 'figures/*技术路线*.png', min: 1}
- {kind: semantic, claim: 图中环节与 PROPOSAL.md 第 4 节一致, verify_by: 人眼}
```

### 步骤 4 — 导出

产出 `PROPOSAL.docx`。DOCX 渲染有若干坑:公式转图片、编号列表在转换后重排、表格跨页断行。转换后必须逐页看一遍。

闸门:
```yaml
- {kind: machine, check: required_files, files: [PROPOSAL.docx]}
- {kind: semantic, claim: 转换后公式、编号、表格均正常, verify_by: 人眼查页}
```
