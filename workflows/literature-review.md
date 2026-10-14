# W3 — 文献综述

## 何时用

需要系统性梳理某领域的研究现状,写综述论文或学位论文的文献回顾章节。用户说「综述」「文献调研」「写 related work」。

不适用:只是补几条引用 → 直接检索;写完整论文需要文献支撑 → W1 或 W9。

## 步骤

```
1 of 5  检索             → literature_raw.json
2 of 5  真实性验证       → literature_verified.json
3 of 5  主题聚类         → CLUSTERS.md
4 of 5  综述撰写         → review/main.md
5 of 5  引用格式         → review/main.docx
```

## 各步骤

### 步骤 1 — 检索

**操作:**

1. **确定检索范围** — 与用户明确:
   - 时间范围(如近5年 / 近10年 / 不限)
   - 文献类型(期刊论文 / 会议论文 / 综述 / 全部)
   - 语言限制(仅英文 / 中英文)
   - 领域边界(狭义主题 / 广义领域)

2. **多源检索策略:**

   **生物医学领域:**
   ```
   PubMed: (keyword1[Title/Abstract]) AND (keyword2[Title/Abstract])
   过滤: 近5年 + Review + English
   ```

   **计算机领域:**
   ```
   Google Scholar: "machine learning" AND "optimization"
   arXiv: cs.LG + 按引用量排序
   DBLP: 顶会论文(ICML/NeurIPS/ICLR)
   ```

   **交叉领域:**
   ```
   Scopus: TITLE-ABS-KEY(keyword1 AND keyword2)
   Web of Science: 按被引频次降序
   ```

3. **初筛标准** — 快速判断是否相关:
   - 标题是否直接相关?
   - 摘要是否包含核心方法/结果?
   - 是否高影响力期刊/会议?
   - 引用量是否足够(领域依赖)?

4. **输出 literature_raw.json**,每条记录:
   ```json
   {
     "id": 1,
     "title": "...",
     "authors": ["FirstAuthor", "SecondAuthor"],
     "year": 2024,
     "venue": "Nature Machine Intelligence",
     "doi": "10.1038/xxxxx",
     "abstract": "...",
     "search_source": "PubMed",
     "search_query": "...",
     "relevance_note": "与本综述的关系"
   }
   ```

闸门:
```yaml
- {kind: machine, check: required_files, files: [literature_raw.json]}
- {kind: machine, check: min_entries, file: literature_raw.json, min: 30}
```

---

### 步骤 2 — 真实性验证

**操作:**

1. **逐条核对** — 确保每条文献真实存在:
   
   **通过 DOI 验证:**
   ```
   访问 https://doi.org/[DOI]
   确认:标题、作者、年份是否匹配
   ```

   **通过标题验证:**
   ```
   在 Google Scholar 搜索完整标题(加引号)
   对比:作者列表、出处、年份
   ```

2. **分类打标:**
   - `verified`: DOI可访问或标题完全匹配
   - `unverifiable`: 检索不到或信息不全
   - `suspicious`: 年份/作者/出处有矛盾

3. **处理 unverifiable 条目:**
   - 二次检索:尝试不同数据库
   - 替换:找同主题的可验证文献
   - 删除:实在找不到就舍弃

4. **输出 literature_verified.json**,增加 `verification_status` 字段

闸门:
```yaml
- {kind: machine, check: required_files, files: [literature_verified.json]}
- {kind: falsifiable_check, claim: verified 条目比例 ≥ 90%}
```

**绝对禁止:**
- 保留无法验证的文献
- 根据摘要"推测"完整信息
- 从非权威源补全信息

---

### 步骤 3 — 主题聚类

**操作:**

1. **识别研究主题** — 从文献中提取:
   - 方法类别(如:深度学习 vs 传统统计)
   - 应用场景(如:医疗诊断 vs 药物发现)
   - 理论基础(如:贝叶斯 vs 频率派)

2. **构建主题簇** — 每个簇包含:
   ```markdown
   ## 簇1:基于深度学习的方法
   
   ### 方法脉络
   - 2018-2020: 卷积网络主导(代表工作:Paper A, Paper B)
   - 2021-2023: Transformer 崛起(代表工作:Paper C, Paper D)
   - 2024至今: 多模态融合(代表工作:Paper E)
   
   ### 共识
   - 深度学习优于传统方法(证据:Paper A, C, E)
   - 数据量是关键瓶颈(所有工作都提到)
   
   ### 分歧
   - 模型可解释性的重要性(Paper B认为关键,Paper D认为次要)
   - 小样本学习的可行性(Paper C乐观,Paper E悲观)
   
   ### 未解问题
   - 如何在保持性能的同时提升可解释性?
   - 跨领域迁移的理论保证?
   ```

3. **绘制知识图谱** — 可选,如果文献量大:
   ```python
   import networkx as nx
   import matplotlib.pyplot as plt
   
   # 构建引用网络
   G = nx.DiGraph()
   for paper in papers:
       G.add_node(paper['id'], label=paper['title'][:30])
       for ref in paper['references']:
           if ref in papers:
               G.add_edge(paper['id'], ref)
   
   # 识别关键节点(高被引)
   centrality = nx.betweenness_centrality(G)
   ```

4. **输出 CLUSTERS.md**

闸门:
```yaml
- {kind: machine, check: required_files, files: [CLUSTERS.md]}
- {kind: machine, check: min_size, file: CLUSTERS.md, bytes: 2000}
- {kind: falsifiable_check, claim: 每个簇至少包含5篇文献}
```

---

### 步骤 4 — 综述撰写

**操作:**

1. **组织结构** — 综述不按时间罗列,按主题组织:

   **好的结构:**
   ```
   1. Introduction
      - 领域定义与范围
      - 为何需要这篇综述
   
   2. 方法分类
      2.1 传统统计方法
      2.2 机器学习方法
      2.3 深度学习方法
   
   3. 应用领域
      3.1 医疗诊断
      3.2 药物发现
   
   4. 挑战与未来方向
   ```

   **避免的结构:**
   ```
   1. 2018年的研究
   2. 2019年的研究
   3. 2020年的研究  ❌ 流水账
   ```

2. **写作要点:**

   **每段结构:**
   - 首句:该段要讨论的方法/问题
   - 中间:列举代表工作,说明各自贡献
   - 末句:总结共识或指出分歧

   **引用格式:**
   ```
   - 单一来源:Smith et al. (2024) 发现...
   - 多个来源支持同一观点:多项研究(refs 1,3,5)表明...
   - 对比不同观点:A认为X(ref 2),但B认为Y(ref 4)
   ```

   **避免:**
   - 仅罗列标题和作者
   - 没有批判性分析
   - 遗漏重要工作

3. **关键段落:**

   **Introduction 末段** — 明确综述范围:
   ```
   本综述聚焦于[具体主题],覆盖[时间范围],
   包括[哪些方面],不包括[哪些方面]。
   我们组织结构如下:[简述各节内容]。
   ```

   **每个主题节末段** — 总结与过渡:
   ```
   综上,该方法的优势在于[X],但局限在于[Y]。
   接下来我们转向[下一个主题]。
   ```

   **Discussion/Conclusion** — 指出未来方向:
   ```
   当前研究的主要空白包括:
   1. [问题1]:现有工作都忽略了...
   2. [问题2]:尽管有初步尝试(ref X),但仍未解决...
   ```

4. **输出 review/main.md**

闸门:
```yaml
- {kind: machine, check: required_files, files: [review/main.md]}
- {kind: machine, check: min_size, file: review/main.md, bytes: 5000}
- {kind: falsifiable_check, claim: 每篇verified文献都在正文中被引用}
```

---

### 步骤 5 — 引用格式

**操作:**

1. **生成参考文献列表** — 按目标格式:

   **APA 7th:**
   ```
   Smith, J., & Doe, A. (2024). Title of the paper. 
   Journal Name, 12(3), 123-135. 
   https://doi.org/10.xxxx/xxxxx
   ```

   **Nature:**
   ```
   1. Smith, J. & Doe, A. Title of the paper. 
      Journal Name 12, 123-135 (2024).
   ```

   **IEEE:**
   ```
   [1] J. Smith and A. Doe, "Title of the paper," 
       Journal Name, vol. 12, no. 3, pp. 123-135, 2024.
   ```

2. **格式转换工具:**
   ```bash
   # Markdown → Word (带引用)
   pandoc review/main.md \
     --citeproc \
     --bibliography=literature_verified.bib \
     --csl=apa.csl \
     -o review/main.docx
   
   # Markdown → LaTeX
   pandoc review/main.md \
     --natbib \
     -o review/main.tex
   ```

3. **最后检查:**
   - [ ] 参考文献按字母/序号排序
   - [ ] 每条引用格式统一
   - [ ] 正文引用与列表对应
   - [ ] DOI链接可点击
   - [ ] 无重复条目

4. **输出 review/main.docx**

闸门:
```yaml
- {kind: machine, check: required_files, files: [review/main.docx]}
- {kind: semantic, claim: 引用格式符合目标期刊要求, verify_by: 用户验收}
```

---

## 依赖关系

```
literature_raw.json → literature_verified.json → CLUSTERS.md → review/main.md → review/main.docx
```

改 CLUSTERS.md 后必须重跑 review/main.md,这是最常见的失效点。

---

## 质量标准

**优秀综述的特征:**
1. **批判性**: 不只罗列,要评价优劣
2. **系统性**: 覆盖主要工作,不遗漏重要文献
3. **前瞻性**: 指出未来方向,不只总结过去
4. **可读性**: 按主题组织,不按时间流水账

**常见问题:**
- 引用过时(>10年的工作占比过高)
- 只引用高影响因子期刊(忽略领域专业期刊)
- 缺乏批判性(所有工作都说"很好")
- 结构混乱(主题交叉,逻辑不清)

---

## 时间估算

- 步骤1-2: 2-5天(取决于文献量)
- 步骤3: 1-2天
- 步骤4-5: 3-7天

总计: 1-2周(小综述) / 3-6周(大综述)
