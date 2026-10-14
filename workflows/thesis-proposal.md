# W4 — 开题报告

## 何时用

学位论文开题、课题申报书、研究计划。用户说「开题」「开题报告」「proposal」「研究计划」。

## 步骤

1 of 4  背景与文献 → BACKGROUND.md
2 of 4  研究问题与方案 → PROPOSAL.md
3 of 4  技术路线图 → figures/技术路线.png
4 of 4  导出 → PROPOSAL.docx

## 各步骤

### 步骤 1 — 背景与文献

产出 BACKGROUND.md: 领域现状、已有工作、遗留问题、本课题的切入口。

嵌入文献检索与验证逻辑:

1. PubMed 检索(医学/生物):
   - 用 Biopython Entrez 模块
   - esearch → 获取 PMID 列表
   - efetch → 获取摘要和元数据
   - 验证: 作者、年份、DOI 是否一致

2. arXiv 检索(数学/CS/物理):
   - 用 HTTP API 查询
   - 解析 XML 响应获取标题、作者、摘要
   - 验证: arXiv ID 格式、作者列表

3. CrossRef DOI 验证:
   - 用 CrossRef API 验证 DOI 是否存在
   - 检查标题、作者、年份是否匹配
   - 获取正式引用格式

4. Google Scholar 检索(通用):
   - 用 scholarly 库(如已安装)
   - 获取标题、作者、年份、引用数
   - 交叉验证其他来源

最低要求: 15 篇文献,每篇必须包含标题、作者、年份,至少一个可验证的标识符(PMID/DOI/arXiv ID)。

闸门:
- {kind: machine, check: min_size, file: BACKGROUND.md, bytes: 1500}
- {kind: machine, check: min_entries, file: BACKGROUND.md, min: 15}
- {kind: falsifiable_check, claim: 文献可溯源,每条有 PMID/DOI/arXiv ID}

### 步骤 2 — 研究问题与方案

产出 PROPOSAL.md,标准结构:

1 研究问题
2 核心主张
3 方法概要
4 实验/研究设计
5 已有基础与条件
6 预期成果
7 可行性与风险
8 进度安排
9 参考文献

为什么只留一个选题: 候选方向往往有八到十个,全留在上下文里会污染工作记忆。定下一个,其余归档进 alternatives/,需要时再取。

闸门:
- {kind: machine, check: min_size, file: PROPOSAL.md, bytes: 2500}
- {kind: machine, check: regex, file: PROPOSAL.md, pattern: '##\s*\d+\s', min_matches: 6}
- {kind: semantic, claim: 研究问题可回答、可验证, verify_by: 用户验收}

### 步骤 3 — 技术路线图

产出 figures/技术路线.png。用 graphviz 或 matplotlib 绘制:

示例(用 graphviz):
from graphviz import Digraph
dot = Digraph(comment='技术路线')
dot.attr(rankdir='LR')
dot.node('A', '数据收集')
dot.node('B', '预处理')
dot.node('C', '模型训练')
dot.node('D', '结果验证')
dot.edges(['AB', 'BC', 'CD'])
dot.render('figures/技术路线', format='png', cleanup=True)

闸门:
- {kind: machine, check: glob_count, glob: 'figures/*技术路线*.png', min: 1}
- {kind: semantic, claim: 图中环节与 PROPOSAL.md 第4节一致, verify_by: 人眼}

### 步骤 4 — 导出

产出 PROPOSAL.docx。用 pandoc 转换:

pandoc PROPOSAL.md -o PROPOSAL.docx --reference-doc=template.docx

转换后检查项:
- 公式是否正确渲染(可能转为图片)
- 编号列表是否保持顺序
- 表格是否跨页断行
- 图片是否正常嵌入

闸门:
- {kind: machine, check: required_files, files: [PROPOSAL.docx]}
- {kind: semantic, claim: 转换后公式、编号、表格均正常, verify_by: 人眼查页}
