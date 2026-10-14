# W2 — 数学建模竞赛

## 何时用

数学建模竞赛,含国赛(全国大学生数学建模竞赛)、美赛(MCM/ICM)、研究生数学建模、各类校赛。用户说「写数模」「A题」「比赛」「美赛」「国赛」。

这是一条最长的流水线,九步。每一步的产出是下一步的硬输入。

## 步骤总表

```
1 of 9  赛题解析        → PROBLEM_ANALYSIS.md + CAPABILITY_CHECKLIST.json
2 of 9  数据与统计      → data/ + STATS_NOTES.md
3 of 9  建模方案        → MODELING_REPORT.md
4 of 9  代码实现        → code/ + RESULTS.md
5 of 9  数据图表        → figures/q*.png
6 of 9  架构图/流程图   → figures/架构图.png（drawio）
7 of 9  论文撰写        → paper/main.md
8 of 9  编译导出        → paper/main.pdf 或 .docx
9 of 9  自审与改进      → REVIEW_REPORT.md + 改进稿
```

依赖链:

```
PROBLEM_ANALYSIS.md → MODELING_REPORT.md → RESULTS.md → figures/ → paper/main.md → main.pdf
```

`MODELING_REPORT.md` 变更必须重跑 `RESULTS.md`,否则图用的是旧模型假设。这是本工作流最常见的失效源。

## 各步骤

### 步骤 1 — 赛题解析

产出 `PROBLEM_ANALYSIS.md` + `CAPABILITY_CHECKLIST.json`。

`PROBLEM_ANALYSIS.md` 结构:

```markdown
## 问题一
### 问题重述
### 关键变量与约束
### 目标
## 问题二
...
<!-- FIGURE_MANIFEST
| 拟放章节 | 对应问题 | 图内容 | 数据来源 |
|---------|---------|--------|---------|
| 问题二求解 | 问题二 | 需求量趋势 | RESULTS.md |
-->
```

`CAPABILITY_CHECKLIST.json` 逐条列:完成这道题需要什么能力、每项现在是否具备、缺的怎么补。

闸门:
```yaml
- {kind: machine, check: required_files, files: [PROBLEM_ANALYSIS.md, CAPABILITY_CHECKLIST.json]}
- {kind: machine, check: min_size, file: PROBLEM_ANALYSIS.md, bytes: 1000}
- {kind: machine, check: regex, file: PROBLEM_ANALYSIS.md,
   pattern: '^#{1,6}\s+(?:问题\s*[一二三四五六七八九十\d]+|第\s*\d+\s*问|[Qq]\s*\d+)', min_matches: 2}
- {kind: machine, check: contains, file: PROBLEM_ANALYSIS.md, text: FIGURE_MANIFEST}
- {kind: semantic, claim: 每个问题的目标函数和约束写清了, verify_by: 用户验收}
```

问题标题匹配要求能认出「问题一」「第 2 问」「Q3」「Problem 4」这几种写法。

### 步骤 2 — 数据与统计

产出 `data/`(清洗后数据)+ `STATS_NOTES.md`。

`STATS_NOTES.md` 每条统计量写明:来源文件、样本量 n、计算方法、异常值处理。

闸门:
```yaml
- {kind: machine, check: dir_exists, dir: data}
- {kind: machine, check: min_size, file: STATS_NOTES.md, bytes: 400}
- {kind: falsifiable_check, claim: 每个统计量都能在 data/ 里复算出来}
```

无原始数据时,不得生成数值。缺数据就写「缺 X,未做推断」。

### 步骤 3 — 建模方案

产出 `MODELING_REPORT.md`,每个问题一节:模型选择理由、数学表达、假设、求解思路、备选方案对比。

闸门:
```yaml
- {kind: machine, check: min_size, file: MODELING_REPORT.md, bytes: 1500}
- {kind: machine, check: regex, file: MODELING_REPORT.md, pattern: '^#{2,3}\s*问题', min_matches: 2}
- {kind: machine, check: contains, file: MODELING_REPORT.md, text: 假设}
- {kind: semantic, claim: 模型与问题的匹配关系说清了, verify_by: 用户验收}
```

### 步骤 4 — 代码实现

产出 `code/` + `RESULTS.md`。`RESULTS.md` 里每个数值都要能追到某一支脚本加某一次运行。

闸门:
```yaml
- {kind: machine, check: dir_exists, dir: code}
- {kind: machine, check: required_files, files: [RESULTS.md]}
- {kind: machine, check: min_size, file: RESULTS.md, bytes: 800}
- {kind: machine, check: contains, file: RESULTS.md, text: '```'}
- {kind: falsifiable_check, claim: 论文里要用的每个结论数都出现在 RESULTS.md}
```

编码:所有 Python 脚本开头加 UTF-8 包装,中文路径用 `os.path.join` + `r'...'`。

```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
```

### 步骤 5 — 数据图表

产出 `figures/q1_*.png`、`figures/q2_*.png`,按问题编号前缀。

图名按章节标题归类,不按文件名前缀猜归属 —— 文件名可以乱起,章节标题是作者给的,更可信。`[Modex]`

闸门:
```yaml
- {kind: machine, check: glob_count, glob: figures/q*.png, min: 2}
- {kind: machine, check: min_size, file: figures/q1_*.png, bytes: 2048}
```

静态检查(崩溃恢复时用):只看 `figures/` 是否达到该步应有的产出规模。
动态检查(正常执行时用):看这一步前后文件增量的实际差异。`[Modex]`

两种检查不能混用。用动态检查判断崩溃恢复会误判,用静态检查判断偷懒会漏判。

图文交叉自检,发现重叠转 `matplotlib-fix`。

### 步骤 6 — 架构图/流程图

产出 `figures/架构图.png` 或 `figures/流程图.png`(drawio 绘制)。

闸门:
```yaml
- {kind: machine, check: glob_count, glob: figures/*架构图*.png, min: 1}
- {kind: semantic, claim: 图里的模块名与 code/ 实际结构一致, verify_by: 人眼}
```

若论文确实不含架构图,在 `MODELING_REPORT.md` 里显式声明「本论文无架构图」,该步骤按 `skipped` 记录,不算失败。

### 步骤 7 — 论文撰写

产出 `paper/main.md`。按竞赛论文标准结构:摘要、问题重述、问题分析、模型假设、符号说明、模型建立与求解(逐问)、模型检验、灵敏度分析、模型评价与推广、参考文献、附录。

闸门:
```yaml
- {kind: machine, check: min_size, file: paper/main.md, bytes: 6000}
- {kind: machine, check: contains, file: paper/main.md, text: 摘要}
- {kind: machine, check: contains, file: paper/main.md, text: 符号说明}
- {kind: machine, check: contains, file: paper/main.md, text: 参考文献}
- {kind: falsifiable_check, claim: 正文引用的每个图号、表号、公式号都存在}
```

页码字数预检:正文计到「附录」之前,图和公式按折算占用计入。中文稿与英文稿分别计数。这是一道保守的预检,只提示不阻断。

### 步骤 8 — 编译导出

中文稿走 LaTeX 出 PDF,或直接导 Word;英文稿同理。

产出 `paper/main.pdf` 或 `paper/main.docx`。

闸门:
```yaml
- {kind: machine, check: glob_count, glob: 'paper/main.pdf', min: 1}
- {kind: machine, check: min_size, file: paper/main.pdf, bytes: 50000}
- {kind: falsifiable_check, claim: PDF 页数在赛题限制内}
```

编译失败时,先修 LaTeX 而不是改内容。中文 LaTeX 用 XeLaTeX + ctex。

### 步骤 9 — 自审与改进

产出 `REVIEW_REPORT.md`,再走一轮改进循环,最多 4 轮。

每轮:按评审清单挑问题 → 逐条修改 → 重新编译 → 复查。

闸门:
```yaml
- {kind: machine, check: required_files, files: [REVIEW_REPORT.md]}
- {kind: semantic, claim: 评审意见逐条有处理记录, verify_by: 用户验收}
```

## 常见失效

| 现象 | 原因 | 处理 |
|------|------|------|
| 图对不上正文 | 改了建模未重跑代码 | 重跑步骤 4–5 |
| 符号前后不一致 | 符号说明未同步正文修改 | 改正文后重生成符号表 |
| 摘要与结论不符 | 结论后改但摘要没改 | 摘要放最后写 |
| 附录代码与 code/ 不符 | 手改了附录没改脚本 | 以 code/ 为准重贴 |
