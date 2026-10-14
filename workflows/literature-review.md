# W3 — 文献综述

## 何时用

写综述文章、related work 章节,或做选题前的文献调研。用户说「综述」「文献调研」「related work」「这个方向做过什么」。

## 步骤

```
1 of 5  检索        → literature_raw.json
2 of 5  真实性验证   → literature_verified.json
3 of 5  主题聚类     → CLUSTERS.md
4 of 5  综述撰写     → review/main.md
5 of 5  引用格式     → review/main.docx
```

## 各步骤

### 步骤 1 — 检索

调用:`nature-academic-search` 或 `deep-research`

产出 `literature_raw.json`,每条:标题、作者、年、出处、标识符、摘要、检索来源。

闸门:
```yaml
- {kind: machine, check: required_files, files: [literature_raw.json]}
- {kind: machine, check: min_entries, file: literature_raw.json, min: 20}
- {kind: machine, check: json_parses, file: literature_raw.json}
```

### 步骤 2 — 真实性验证

调用:`citation-check-skill`

逐条核对能否在权威源找到。分三类打标:`verified`、`unverifiable`、`suspicious`。

产出 `literature_verified.json`。

闸门:
```yaml
- {kind: machine, check: required_files, files: [literature_verified.json]}
- {kind: falsifiable_check, claim: 无 verified 状态的条目进入后续步骤}
```

这是本工作流的硬闸。未经核实的条目一律不得进入综述正文。检索不到就标注,不补写。

### 步骤 3 — 主题聚类

调用:`deep-research`synthesis 阶段(或 `academic-research-skills:synthesis_agent`)

产出 `CLUSTERS.md`:每个簇的方法脉络、代表工作、共识、分歧、未解问题。

闸门:
```yaml
- {kind: machine, check: min_size, file: CLUSTERS.md, bytes: 1000}
- {kind: semantic, claim: 簇的划分有依据,不是按年份硬切, verify_by: 用户验收}
```

### 步骤 4 — 综述撰写

调用:`nature-writing`(paper_type=review)

产出 `review/main.md`。按主题组织,不按时间罗列。每段前述某条脉络的现状,段中给对比与证据,段末给判断。

闸门:
```yaml
- {kind: machine, check: min_size, file: review/main.md, bytes: 5000}
- {kind: machine, check: contains, file: review/main.md, text: 参考文献}
- {kind: falsifiable_check, claim: 每个论断都有引用编号支撑}
```

### 步骤 5 — 引用格式

调用:`nature-citation`

产出 `review/main.docx`,目标期刊或学位的引用格式统一。

闸门:
```yaml
- {kind: machine, check: required_files, files: [review/main.docx]}
- {kind: falsifiable_check, claim: 正文引用编号与参考文献列表一一对应}
```

## 依赖

`literature_raw.json → literature_verified.json → CLUSTERS.md → review/main.md → main.docx`

`literature_verified.json` 改了,后面全部失效。这是有意为之:核实的结论变了,基于旧结论写的综述就不可信。
