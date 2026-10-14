# W1 — 论文写作

## 何时用

从零开始写一篇学术论文,或把已有的草稿/结果整理成稿。用户说「写论文」「写paper」「写SCI」「帮我写一篇关于X的论文」。

不适用:需要先做完整文献调研再定选题 → W9;已有数据代码只差成文 → W6;只改语言 → 直接润色。

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

**操作:**

1. **头脑风暴阶段** — 与用户探讨:
   - 你想解决什么问题?
   - 为什么这个问题值得研究?
   - 现有方法有什么局限?
   - 你的想法与众不同在哪里?

2. **深度调研阶段** — 评估可行性:
   - 该领域当前研究热点是什么?
   - 最近3年有什么重要进展?
   - 你的切入点是否已有人做过?
   - 目标期刊的接收标准是什么?

3. **输出 IDEA_BRIEF.md**,包含:
   ```markdown
   ## 研究问题
   [一句话:本研究要回答什么问题]
   
   ## 为什么是现在
   [领域发展到什么阶段,为什么此时研究这个问题有意义]
   
   ## 核心主张
   1. [主张1:你要证明的第一个关键结论]
   2. [主张2:...]
   
   ## 目标期刊层级
   - 理想投稿:Nature 大子刊 / Science Advances
   - 合格线:Cell Reports / eLife / 领域Top期刊
   ```

闸门:
```yaml
- {kind: machine, check: min_size, file: IDEA_BRIEF.md, bytes: 600}
- {kind: machine, check: regex, file: IDEA_BRIEF.md, pattern: '^##\s*(研究问题|核心主张)'}
- {kind: semantic, claim: 研究问题是否窄到可以回答, verify_by: 用户验收}
```

---

### 步骤 2 — 文献与新颖性

**操作:**

1. **多源检索** — 在以下数据库搜索相关文献:
   - PubMed / PMC (生物医学)
   - arXiv (计算机/物理)
   - Google Scholar (全领域)
   - 领域专属数据库 (IEEE Xplore / ACM DL / Scopus)

2. **真实性验证** — 逐条核对:
   - 能否通过 DOI 或标题在权威源找到?
   - 作者姓名、年份、卷期是否准确?
   - 摘要与标题是否匹配?
   
   **绝对禁止:**
   - 杜撰作者、标题、DOI、卷期、年份
   - 检索不到就写「未检索到可靠来源」,不推断

3. **输出 literature.md**,每条记录:
   ```markdown
   ### [序号] 标题
   - **作者**: FirstAuthor et al.
   - **年份**: 2024
   - **出处**: Nature Machine Intelligence, 6(1), 123-135
   - **DOI**: 10.1038/xxxxx
   - **与本工作关系**: [这篇做了什么,为什么相关,与我们的区别]
   ```

闸门:
```yaml
- {kind: machine, check: required_files, files: [literature.md]}
- {kind: machine, check: min_entries, file: literature.md, min: 15}
- {kind: falsifiable_check, claim: 每条文献都可溯源（有 DOI 或可检索标题）}
```

---

### 步骤 3 — 论证结构

**操作:**

1. **设计论证链** — 规划如何从问题到结论:
   - Introduction: 从宽到窄,收束到你的研究问题
   - Methods: 按执行顺序,不按类别分组
   - Results: 按逻辑顺序展示证据,不按时间顺序
   - Discussion: 从你的发现出发,逐层扩展到领域意义

2. **每节写一段计划**,格式:
   ```markdown
   ## Introduction
   本节要论证:[研究问题的重要性和紧迫性]
   证据来源:[引用哪几篇文献,自己有什么数据支撑]
   与下一节衔接:[如何过渡到 Methods]
   ```

3. **输出 PAPER_PLAN.md**

闸门:
```yaml
- {kind: machine, check: min_size, file: PAPER_PLAN.md, bytes: 800}
- {kind: falsifiable_check, claim: 每个核心主张都能在计划里找到对应的证据来源}
```

---

### 步骤 4 — 初稿

**操作:**

1. **按计划逐节撰写**,遵循 **Context → Content → Conclusion** 结构:
   - **段首句**:交代背景,告诉读者为何要读这段
   - **段中**:给出数据、论证、推导
   - **段末句**:总结结论或过渡到下一段

2. **各节写作要点:**

   **Abstract (150-250词)**:
   - 第1句:领域背景与问题
   - 第2-3句:现有方法的局限
   - 第4句:我们做了什么
   - 第5-6句:主要结果(带数字)
   - 第7句:意义与影响

   **Introduction**:
   - 从宽到窄:领域现状 → 具体问题 → 我们的贡献
   - 每段末句过渡,不能突然跳转
   - 末段明确列出贡献点(numbered list)

   **Methods**:
   - 按执行顺序写,不按模块分类
   - 每个子方法开头说明"为什么需要这一步"
   - 参数设置要说明依据

   **Results**:
   - 每个小节只论证一个点
   - 先描述现象,再解释原因
   - 数字要具体:不说"显著提升",说"从68%提升到79%"

   **Discussion**:
   - 第1段:重申主要发现
   - 中间段:与现有工作对比,解释差异
   - 倒数第2段:局限性(为何重要但未解决)
   - 最后1段:未来方向

3. **输出 paper/main.md**

闸门:
```yaml
- {kind: machine, check: required_files, files: [paper/main.md]}
- {kind: machine, check: min_size, file: paper/main.md, bytes: 4000}
- {kind: machine, check: regex, file: paper/main.md, pattern: '^##\s+(Introduction|Methods|Results|Discussion|References)', min_matches: 4}
```

---

### 步骤 5 — 图表

**操作:**

1. **规划图表** — 每个图必须回答:
   - 这个图论证什么结论?
   - 不看正文,图注能否独立理解?
   - 是否有更简洁的表达方式?

2. **制作要求:**

   **数据完整性:**
   - 样本量 n 必须标注
   - 误差棒说明类型(SD / SEM / 95% CI)
   - 数据来源可追溯

   **视觉规范:**
   - 色盲友好配色(避免纯红绿对比)
   - 字号在最终尺寸下可读(≥7pt)
   - 无图文交叉、图例不遮挡数据
   - 矢量格式(PDF/SVG),不用JPEG

   **Python 示例:**
   ```python
   import matplotlib.pyplot as plt
   import seaborn as sns
   
   # 设置期刊风格
   sns.set_context("paper")
   sns.set_palette("colorblind")
   
   fig, ax = plt.subplots(figsize=(3.5, 2.625))  # Nature单栏尺寸
   
   # 绘图...
   
   # 保存
   plt.tight_layout()
   fig.savefig('figures/fig1.pdf', dpi=300, bbox_inches='tight')
   ```

3. **图注格式:**
   ```markdown
   **Figure 1. [一句话总结这个图说明了什么]**
   a, [子图a的描述]. Error bars, SEM; n=20 samples.
   b, [子图b的描述]. Data from [来源].
   ```

4. **自检清单:**
   - [ ] 图文无交叉(标签不盖住数据点)
   - [ ] 坐标轴标签完整(单位、变量名)
   - [ ] 图例位置合理
   - [ ] 灰度打印仍可区分
   - [ ] 文件大小合理(<5MB per figure)

闸门:
```yaml
- {kind: machine, check: glob_count, glob: figures/*.pdf, min: 2}
- {kind: falsifiable_check, claim: 正文引用的每个图号都能在 figures/ 找到}
- {kind: semantic, claim: 无图文交叉、图例不遮挡数据, verify_by: 人眼}
```

**图文交叉修复方案:**
如果图表出现重叠问题,按以下步骤修复:

```python
# 方案1: 调整布局
plt.tight_layout()  # 自动调整间距
# 或
fig.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)

# 方案2: 手动移动图例
ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))

# 方案3: 缩小字号
ax.tick_params(labelsize=8)
ax.set_xlabel('Label', fontsize=9)

# 方案4: 增大画布
fig.set_size_inches(4.0, 3.0)  # 稍微加宽
```

---

### 步骤 6 — 打磨与自审

**操作:**

1. **语言打磨:**
   - 删除冗余词汇:very / really / actually / in fact
   - 避免被动语态:用 "We found" 而非 "It was found"
   - 短句优先:单句不超过 30 词
   - 专业术语统一:第一次出现加括号注释

2. **六角色红队审查** — 从不同视角找问题:

   | 角色 | 问题 | 检查方法 |
   |------|------|----------|
   | 矛盾查找 | 哪里自相矛盾?结论与引用证据不吻合处? | 逐段对照引用文献 |
   | 审稿人 #2 | 方法缺陷?缺什么对照?哪里过于自信? | 逐节挑刺 |
   | 反向推导 | 从结论倒推回假设,中间有断裂吗? | 倒着读 Discussion |
   | 破坏测试 | 什么真实场景下方法会灾难性失败? | 想极端情况 |
   | 假设压力测试 | 最脆弱的 3 条假设是什么? | 列出所有假设 |
   | 观点刷新 | 看完所有证据,什么应改变当前判断? | 假装第一次看 |

3. **去 AI 痕迹** — 避免典型 AI 写作模式:
   - 不用"值得注意的是(notably)"开头
   - 不用"显著地(significantly)"修饰非统计结果
   - 不用"深入(delve into)" / "利用(leverage)"
   - 避免三段式万能结构(introduction-body-conclusion in every paragraph)
   - 数字要具体,不说"大幅提升",说"提升27%"

4. **输出 REVIEW_REPORT.md**,包含:
   ```markdown
   ## 五维差距分析
   
   ### 1. 故事完整性
   - 当前:[现状]
   - 目标:Nature大子刊标准
   - 差距:[具体缺什么]
   - 建议:[如何改进]
   
   ### 2. 方法创新性
   ...
   
   ### 3. 验证力度
   ...
   
   ### 4. 图表质量
   ...
   
   ### 5. 写作质量
   ...
   
   ## 六角色红队发现
   
   ### 矛盾查找
   - 问题1:[具体矛盾处]
   - 问题2:...
   
   ### 审稿人 #2
   ...
   ```

5. **导出终稿** — 生成投稿格式:
   ```bash
   # Markdown → Word
   pandoc paper/main.md -o paper/main.docx --reference-doc=template.docx
   
   # Markdown → PDF (需LaTeX)
   pandoc paper/main.md -o paper/main.pdf --pdf-engine=xelatex
   ```

闸门:
```yaml
- {kind: machine, check: required_files, files: [REVIEW_REPORT.md]}
- {kind: semantic, claim: 六角色逐条有回应, verify_by: 用户验收}
```

---

## 依赖关系

```
IDEA_BRIEF.md → literature.md → PAPER_PLAN.md → paper/main.md → figures/ → 终稿
```

改上游任一环,下游全部标 stale。改 `PAPER_PLAN.md` 后 `paper/main.md` 必须重跑,这是最常见的失效点。

---

## 差距分析标准

对标层级:
- **主要对标**: Nature Methods / Nature Biotechnology / Nature Machine Intelligence
- **合格线**: Science Advances / Cell Reports / eLife / PNAS

五个维度:
1. **故事完整性**: 主线清晰,假设→论证→结论自洽
2. **方法创新性**: 与现有方法边界清楚,创新点说清
3. **验证力度**: 数据集、消融实验、基线对比充分
4. **图表质量**: 信息密度高、可读性强、美学合格
5. **写作质量**: 摘要一击即中,引言讲清"为什么是现在"

---

## 常见问题

**Q: 如何判断文献够不够?**

A: 不看数量,看覆盖面:
- 领域奠基性工作(必引)
- 近3年相关工作(证明新颖性)
- 与你方法直接对比的工作(证明优势)
- 目标期刊近期发表的类似主题论文(证明契合度)

**Q: Introduction 写多长?**

A: 取决于期刊:
- Nature 正刊: 2-3段,极简
- Nature 大子刊: 4-6段
- 领域期刊: 1-1.5页

**Q: 如何处理审稿意见?**

A: 见 W8 — 审稿与返修工作流
