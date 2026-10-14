# W6 — 从已有资料写论文

## 何时用

手上有代码、数据、图表、笔记,但缺成文的论文。用户说「我有数据」「整理成论文」「把实验写成 paper」「资料都在这儿了」。

这是最省时的一条路:东西已经有了,缺的是盘点和补齐。

## 步骤

```
1 of 5  资产盘点     → ASSETS_INVENTORY.md
2 of 5  缺口分析     → GAP_ANALYSIS.md
3 of 5  自动补缺     → 按缺口调对应工作流的步骤
4 of 5  论文撰写     → paper/main.md
5 of 5  打磨导出     → REVIEW_REPORT.md + paper/main.docx
```

## 各步骤

### 步骤 1 — 资产盘点

扫描工作区,把找到的东西分类登记。

注意:隐藏目录(`.xy/`、`.git/` 等)不计入交付产物。交付审计按非隐藏文件对账,记忆文件放明处会被误算成产物。`[Modex]`

产出 `ASSETS_INVENTORY.md`:

```markdown
| 类别 | 路径 | 状态 | 可用性 |
|------|------|------|--------|
| 代码 | code/main.py | 可运行 | 高 |
| 数据 | data/raw.csv | 完整 | 高 |
| 图表 | figures/fig1.png | 无图注 | 中 |
| 结果 | RESULTS.md | 缺问题3 | 中 |
| 笔记 | notes.md | 草稿 | 低 |
```

闸门:
```yaml
- {kind: machine, check: required_files, files: [ASSETS_INVENTORY.md]}
- {kind: machine, check: min_size, file: ASSETS_INVENTORY.md, bytes: 300}
- {kind: falsifiable_check, claim: 表里每条路径都真实存在}
```

### 步骤 2 — 缺口分析

对照 `paper-writing.md` 或 `modeling-comp.md` 的步骤清单,逐项标「有 / 缺 / 不适用」。

产出 `GAP_ANALYSIS.md`:

```markdown
| 论文要素 | 现状 | 处置 |
|---------|------|------|
| 核心主张 | 缺 | 需与用户确认 |
| 实验数据 | 有 | 直接用 |
| 数据图表 | 部分有 | 补问题3的图 |
| 方法描述 | 有代码无文字 | 从 code/ 抽取 |
| 对比基线 | 缺 | 需补跑 |
```

闸门:
```yaml
- {kind: machine, check: required_files, files: [GAP_ANALYSIS.md]}
- {kind: semantic, claim: 「需与用户确认」的条目已逐条问过, verify_by: 用户验收}
```

### 步骤 3 — 自动补缺

按 `GAP_ANALYSIS.md` 的「补」项,调对应工作流的单个步骤。不是跑整条流水线,只补缺的那几步。

比如缺图,就跑 `modeling-comp.md` 的步骤 5;缺代码结果,就跑步骤 4。

闸门:按所调步骤各自的闸门执行。

### 步骤 4 — 论文撰写

调用:`nature-writing`

产出 `paper/main.md`。方法节从 `code/` 反推,不要凭印象写。代码里没有的技巧不要写进方法节。

闸门:
```yaml
- {kind: machine, check: min_size, file: paper/main.md, bytes: 4000}
- {kind: machine, check: regex, file: paper/main.md, pattern: '^##\s+(Introduction|Methods|Results|Discussion|References)', min_matches: 4}
- {kind: falsifiable_check, claim: 方法节描述的每一步都能在 code/ 找到对应}
```

### 步骤 5 — 打磨导出

同 `paper-writing.md` 步骤 6。

## 陷阱

| 陷阱 | 后果 | 对策 |
|------|------|------|
| 图表无图注 | 读者看不懂 n 是多少 | 补图注,写明样本量与来源 |
| 代码与描述不符 | 复现失败 | 以代码为准重写方法节 |
| 数据来源不明 | 无法追溯 | 标来源,不明就写不明 |
| 缺基线还写「效果显著」 | 结论无支撑 | 补基线,或改成描述性表述 |
