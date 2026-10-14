# W1 — 论文写作

## 何时用

从零开始写一篇学术论文,或把已有的草稿/结果整理成稿。用户说「写论文」「写paper」「写SCI」「帮我写一篇关于X的论文」。

不适用:需要先做完整文献调研再定选题 → W9;已有数据代码只差成文 → W6;只改语言 → 直接用 `nature-polishing`。

## 步骤

```
1 of 6  选题与定位       → IDEA_BRIEF.md
2 of 6  文献与新颖性     → literature.md
3 of 6  论证结构         → PAPER_PLAN.md
4 of 6  初稿             → paper/main.md
5 of 6  图表             → figures/ + 图注
6 of 6  打磨与自审       → REVIEW_REPORT.md + paper/main.docx/pdf
```

## 各步骤

### 步骤 1 — 选题与定位

调用:`brainstorming` → `deep-research`

产出 `IDEA_BRIEF.md`,含:研究问题、为什么是现在、核心主张(claims)、目标期刊层级。

闸门:
```yaml
- {kind: machine, check: min_size, file: IDEA_BRIEF.md, bytes: 600}
- {kind: machine, check: regex, file: IDEA_BRIEF.md, pattern: '^##\s*(研究问题|核心主张)'}
- {kind: semantic, claim: 研究问题是否窄到可以回答, verify_by: 用户验收}
```

### 步骤 2 — 文献与新颖性

调用:`nature-academic-search` → `citation-check-skill`

产出 `literature.md`,每条记录:作者、标题、年、出处、与本工作的关系。

闸门:
```yaml
- {kind: machine, check: required_files, files: [literature.md]}
- {kind: machine, check: min_entries, file: literature.md, min: 15}
- {kind: falsifiable_check, claim: 每条文献都可溯源（有 DOI 或可检索标题）}
```

禁止:杜撰作者、标题、DOI、卷期、年份。检索不到就写「未检索到」,不做推断。

### 步骤 3 — 论证结构

调用:`nature-writing`(section=plan)

产出 `PAPER_PLAN.md`:每节一段,写清该节要论证什么、用什么证据、与前后节的衔接。

闸门:
```yaml
- {kind: machine, check: min_size, file: PAPER_PLAN.md, bytes: 800}
- {kind: falsifiable_check, claim: 每个核心主张都能在计划里找到对应的证据来源}
```

### 步骤 4 — 初稿

调用:`nature-writing`(按 manifest 加载 section 片段)

产出 `paper/main.md`。每节遵循 Context → Content → Conclusion:段首句交代背景,段中给数据和论证,段末句给结论或过渡。

闸门:
```yaml
- {kind: machine, check: required_files, files: [paper/main.md]}
- {kind: machine, check: min_size, file: paper/main.md, bytes: 4000}
- {kind: machine, check: regex, file: paper/main.md, pattern: '^##\s+(Introduction|Methods|Results|Discussion|References)', min_matches: 4}
```

### 步骤 5 — 图表

调用:`nature-figure` 或 `scipilot-figure-skill`

产出 `figures/` 与图注。每条图注写清:这是什么、样本量 n、数据来源、误差棒含义。

闸门:
```yaml
- {kind: machine, check: glob_count, glob: figures/*.png, min: 2}
- {kind: falsifiable_check, claim: 正文引用的每个图号都能在 figures/ 找到}
- {kind: semantic, claim: 无图文交叉、图例不遮挡数据, verify_by: 人眼}
```

图有重叠或遮挡时转 `matplotlib-fix`,修完重出自检。

### 步骤 6 — 打磨与自审

调用:`nature-polishing` → `academic-paper-reviewer` → `humanizer-zh`

产出 `REVIEW_REPORT.md`,以及导出的 `paper/main.docx` 或 `.pdf`。

自审用六角色红队,见 `references/protocol.md` 之外的本工作流约定:

| 角色 | 问题 |
|------|------|
| 矛盾查找 | 哪里自相矛盾?结论与引用证据不吻合处? |
| 审稿人 #2 | 方法缺陷?缺什么对照?哪里过于自信? |
| 反向推导 | 从结论倒推回假设,中间有断裂吗? |
| 破坏测试 | 什么真实场景下方法会灾难性失败? |
| 假设压力测试 | 最脆弱的 3 条假设是什么? |
| 观点刷新 | 看完所有证据,什么应改变当前判断? |

闸门:
```yaml
- {kind: machine, check: required_files, files: [REVIEW_REPORT.md]}
- {kind: semantic, claim: 六角色逐条有回应, verify_by: 用户验收}
```

## 依赖关系

```
IDEA_BRIEF.md → literature.md → PAPER_PLAN.md → paper/main.md → figures/ → 终稿
```

改上游任一环,下游全部标 stale。改 `PAPER_PLAN.md` 后 `paper/main.md` 必须重跑,这是最常见的失效点。

## 差距分析

步骤 6 之后附一段对标,五个维度各写「当前 → 目标 → 差距」,不做安慰性表述:

1. 故事完整性:主线是否清晰,假设→论证→结论是否自洽
2. 方法创新性:与现有方法的边界在哪,创新点说清没有
3. 验证力度:数据、消融、基线是否充分
4. 图表质量:信息密度、可读性、美学
5. 写作质量:摘要是否一击即中,引言是否讲清「为什么是现在」

对标层级:Nature 大子刊为主要对标,Science Advances / Cell Reports / eLife 为合格线。
