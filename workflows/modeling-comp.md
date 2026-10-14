# W2 — 数学建模竞赛

## 何时用

数模竞赛论文,国赛、美赛、深圳杯、华为杯等。用户说「写数模」「比赛」「竞赛论文」。

与一般论文的区别:赛题给定、时间有限(3–4 天)、评审重实效轻理论深度。

## 步骤

1 of 9  赛题分析 → PROBLEM_ANALYSIS.md
2 of 9  文献速查 → literature_brief.json
3 of 9  数据理解 → DATA_CHECK.md
4 of 9  建模方案 → MODELING_REPORT.md
5 of 9  求解实现 → code/ + RESULTS.md
6 of 9  架构图 → figures/workflow.png
7 of 9  初稿 → paper/main.md
8 of 9  自审 → REVIEW_REPORT.md
9 of 9  定稿 → paper/main_final.md + 附件包

## 各步骤

### 步骤 1 — 赛题分析

产出 PROBLEM_ANALYSIS.md: 题目要求拆解、评分要点推测、必做项/选做项、时间分配建议。

### 步骤 2 — 文献速查

轻量版调研,只找核心方法。产出 literature_brief.json。

嵌入检索策略(PubMed/arXiv/Scholar):
- PubMed: 生物医学类,用 Biopython Entrez
- arXiv: 数学/CS类,用 HTTP API
- Scholar: 通用,需 scholarly 库

### 步骤 3 — 数据理解

产出 DATA_CHECK.md。赛题数据常见问题与应对:
- 单位不明 → 从附件推断,写进假设
- 缺失值 → 插补并记录方法
- 异常值 → 3σ 检测
- 时间序列不等间隔 → 插值

### 步骤 4 — 建模方案

产出 MODELING_REPORT.md。常见模型决策:
- 优化 → LP/IP/NLP/GA
- 预测 → ARIMA/XGBoost/LSTM
- 评价 → AHP/熵权法/TOPSIS
- 分类 → K-means/DBSCAN
- 网络 → Dijkstra/最大流
- 仿真 → 蒙特卡洛/排队论

### 步骤 5 — 求解实现

产出 code/ + RESULTS.md + figures/。

图表生成后立即自检(刻度重叠、图例遮挡、标签裁切),自动修复最多3轮,检测代码同 data-figures.md 步骤4。

### 步骤 6 — 架构图/流程图

产出 figures/workflow.png。用 graphviz 绘制建模流程、算法流程、网络拓扑。

### 步骤 7 — 初稿

产出 paper/main.md。数模标准结构:摘要、问题重述、问题分析、模型假设、符号说明、模型建立与求解、模型评价、参考文献、附录。

### 步骤 8 — 自审

产出 REVIEW_REPORT.md,红队六角色。数模特有检查项:
- 问题均有明确回答
- 图表有编号说明
- 代码可运行且输出一致
- 假设写全、符号无遗漏

### 步骤 9 — 定稿

产出 paper/main_final.md + submission/ 附件包(论文PDF、代码ZIP、承诺书)。

用 pandoc 转 PDF:
pandoc paper/main_final.md -o submission/论文.pdf --pdf-engine=xelatex -V CJKmainfont=SimSun

## 时间分配(美赛4天)

Day 1 前半天: 步骤1-3 (12%)
Day 1 后半天-Day 2: 步骤4-5 (40%)
Day 3: 步骤6-7 (30%)
Day 4 上午: 步骤8 (10%)
Day 4 下午: 步骤9 (8%)
