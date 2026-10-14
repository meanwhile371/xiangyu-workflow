# W8 — 审稿与返修

## 何时用

收到审稿意见要写回复、论文被拒要重投、要自己先审一遍。用户说「审稿意见」「rebuttal」「返修」「被拒了」「response letter」。

## 步骤

```
1 of 3  意见拆解     → REVIEW_DECODED.md
2 of 3  逐条回应     → RESPONSE.md
3 of 3  改稿         → paper/main_v2.md
```

## 各步骤

### 步骤 1 — 意见拆解

调用:`nature-response`

把每条审稿意见拆成:审稿人原话、真实关切、可执行的行动、可否反驳。

产出 `REVIEW_DECODED.md`:

```markdown
| # | 审稿人原话 | 真实关切 | 行动 | 立场 |
|---|-----------|---------|------|------|
| R1.1 | 样本量偏小 | 结论稳健性 | 补敏感性分析 | 接受 |
| R1.2 | 与 Smith2023 未比较 | 基线缺失 | 补对比实验 | 接受 |
| R2.1 | 方法不新 | 创新性 | 原文已说明差异，加对比表 | 部分反驳 |
| R2.2 | 英文表达 | 语言 | 全文润色 | 接受 |
```

闸门:
```yaml
- {kind: machine, check: required_files, files: [REVIEW_DECODED.md]}
- {kind: machine, check: min_size, file: REVIEW_DECODED.md, bytes: 500}
```

拆解时不要漏条目。审稿人提了五条就拆五条,哪怕某条看起来不重要。

### 步骤 2 — 逐条回应

产出 `RESPONSE.md`。每条回应三段:感谢并复述关切、说明做了什么、指出改在哪。

规则:

1. 反驳必须给证据,不给情绪
2. 做不到的说明为什么,不硬答
3. 每条回应都指向正文的具体位置(节号、行号、页号)

闸门:
```yaml
- {kind: machine, check: required_files, files: [RESPONSE.md]}
- {kind: falsifiable_check, claim: RESPONSE.md 的条目数等于 REVIEW_DECODED.md 的条目数}
- {kind: falsifiable_check, claim: 每条回应引用的正文位置真实存在}
```

条目数对齐是可机检的。数量不符说明有意见没回应。

### 步骤 3 — 改稿

调用:`nature-polishing` → `nature-writing`(按需)

产出 `paper/main_v2.md`。改动留痕,便于生成 diff 给编辑看。

闸门:
```yaml
- {kind: machine, check: required_files, files: [paper/main_v2.md]}
- {kind: semantic, claim: 每条「接受」的意见都在改稿中有对应修改, verify_by: 用户验收}
```

## 反驳的边界

可以反驳:审稿人误读了论文、要求超出本文范围、给的方法不适用且有依据说明。

不建议反驳:语言问题、格式问题、补充对照的要求、审稿人指出的真实缺陷。

反驳的写法:先承认对方关切合理,再给证据说明为什么本文的处理是恰当的,最后说明已增加什么消除歧义。不要写「审稿人显然没有理解」这类句子。

## 被拒后

若整体被拒要重投,回到 `paper-writing.md` 的步骤 3(论证结构)。重投换刊时,故事主线要按新刊的定位重排,不能只换模板。
