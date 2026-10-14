# 协议 — 状态、记忆、闸门

本文档定义 xiangyu-workflow 落盘格式。所有工作流共用。

## 1. STATE.json

```json
{
  "schema": 1,
  "project": "2026-数模国赛-A题",
  "workflow": "W2",
  "mode": "collab",
  "created": "2026-10-13T10:00:00+08:00",
  "updated": "2026-10-13T14:22:00+08:00",
  "runs": [
    {
      "step": 1,
      "skill": "comp-prob-analysis",
      "status": "done",
      "scope": "full",
      "started": "2026-10-13T10:00:00+08:00",
      "ended": "2026-10-13T10:35:00+08:00",
      "outputs": ["PROBLEM_ANALYSIS.md", "CAPABILITY_CHECKLIST.json"],
      "gate": {"passed": true, "checks": ["file_exists", "min_size", "has_questions"]}
    }
  ],
  "artifacts": [
    {
      "path": "PROBLEM_ANALYSIS.md",
      "produced_by": "comp-prob-analysis",
      "inputs": [],
      "sha256": "…",
      "size": 12345,
      "at": "2026-10-13T10:35:00+08:00"
    },
    {
      "path": "figures/q2_trend.png",
      "produced_by": "comp-figure",
      "inputs": ["RESULTS.md@sha256:9f3c…"],
      "sha256": "…",
      "size": 88213,
      "at": "2026-10-13T12:10:00+08:00"
    }
  ],
  "decisions": [
    {
      "topic": "第二问的需求量来源",
      "choice": "B",
      "rejected": ["A"],
      "evidence": "报告试算表明 A 口径与附件数据不一致",
      "at": "2026-10-13T10:40:00+08:00"
    }
  ],
  "flags": {
    "stale": ["figures/q2_trend.png"],
    "pending_gates": [{"step": 5, "skill": "comp-code", "reason": "RESULTS.md 未含代码块"}]
  }
}
```

字段约定:

- `scope` 取 `full` / `focused` / `skipped`
- `status` 取 `pending` / `running` / `done` / `failed` / `skipped`
- `inputs` 写 `路径@sha256:前缀`,不写裸路径 —— 否则比对不出内容变化
- `flags.stale` 是派生值,可由 `artifacts` 重算;允许冗余存放,校验时以重算为准

## 2. 内容哈希

`sha256(文件字节)`,定长截断到 16 位十六进制存入 `inputs`。

目录型产物(如 `figures/`)按 `排序后的 (相对路径, 文件哈希)` 序列再哈希,避免文件遍历顺序影响结果。

不用 mtime。理由:复制、解压、同步、Git 检出都会改 mtime 而不改内容,也会改内容而不改 mtime。

## 3. 失效传递

```python
def stale_cascade(artifacts, changed):
    stale, queue = set(), [changed]
    while queue:
        cur = queue.pop()
        for a in artifacts:
            if cur in own_inputs(a) and a.path not in stale:
                stale.add(a.path)
                queue.append(a.path)
    return stale
```

`own_inputs(a)` 取 `a.inputs` 的路径部分(剥掉哈希)。改了 `RESULTS.md`,`figures/*.png` 因为声明依赖它而失效,`paper/main.md` 若引用图号也随之失效。

失效只标记,不重跑。重跑要用户确认。

## 4. 决定日志

只在两种情况下写 `decisions`:

1. **用户在多个方案中选了一个** —— 记 `choice` 和 `rejected`
2. **用户明确否决某个方案** —— 记 `choice` 为空、`rejected` 含被否方案

关键点:报告里已经写了倾向、已经选好的方案,**恰恰是要抽出来的**。`[Modex]`

原因很实际:每步可能由新的进程执行,新进程读不到上一轮对话,只会读文件。报告若写「建议采用方案 A(备选 B、C)」,不抽出来,下一步的执行者可能把 B 又提一遍。

主题归一化:`第二问的需求量来源`、`问题二需求量来源`、`Q2 需求量口径` 应归到同一 topic。去空格、去标点、统一数字写法后比较。归一化失败时宁可新建一条,不要强行合并。

## 5. 记忆段

```markdown
<!-- XY_MEMO:BEGIN -->
## 已确认的决定（不得推翻）
- **第二问需求量来源**:B（⛔ 已否决:A，不要重新提出）

## 已完成
- [整步] 步骤1 问题分析 → PROBLEM_ANALYSIS.md（10-13）
- [局部] 步骤4 建模 → 仅问题2方案

## ⚠ 依赖已过期
- **figures/q2_trend.png** ← RESULTS.md 已变更，需重跑

## 下一步
步骤5 代码实现 → 待用户确认
<!-- XY_MEMO:END -->
```

写入规则:

1. 只替换 `BEGIN`/`END` 之间的内容,块外不动
2. 整体重写,不追加
3. 超 3000 字符时按「过期警告 > 决定 > 最近 5 条已完成」的优先级保留
4. 找不到标记块时,在文件末尾新建,不要插入到中间

## 6. 质量闸写法

每步在对应工作流文件里声明检查项。三种类型:

```yaml
gate:
  - kind: machine
    check: required_files
    files: [PROBLEM_ANALYSIS.md, CAPABILITY_CHECKLIST.json]
  - kind: machine
    check: min_size
    file: PROBLEM_ANALYSIS.md
    bytes: 800
  - kind: machine
    check: regex
    file: PROBLEM_ANALYSIS.md
    pattern: '^#{1,6}\s+(?:问题\s*[一二三四五六七八九十\d]+|第\s*\d+\s*问|[Qq]\s*\d+)'
    min_matches: 2
  - kind: machine
    check: glob_count
    glob: figures/q*.png
    min: 2
  - kind: falsifiable_check
    claim: 图 3 纵轴单位与正文一致
    verify_by: 人眼比对
  - kind: semantic
    claim: 结论回答了原问题
    verify_by: 用户验收
```

约定:

- `machine` 不通过 → 该步标 `failed`,挂待处理卡
- `falsifiable_check` 不通过 → 标 `failed` 并写明是哪个断言
- `semantic` 永不自动通过 → 进确认卡,用户点头才算过
- 检查无数据源时,写 `[CHECK_UNAVAILABLE]` 并说明缺什么,不要默认通过

## 7. 只读校验

`scripts/check_state.py` 只读。它的三条禁令:

- 不写任何文件
- 不调用模型
- 不重启或回滚任何步骤

它输出:完成进度、当前步骤、过期产物、待处理卡。UI 显示可核验的事实,而不是模型编出来的评分。`[Modex]`

## 8. 中断恢复

三种恢复路径,任何一种都要先清掉暂停标记,否则流程会在下一步立刻停住。`[Modex]`

| 路径 | 触发 |
|------|------|
| 心跳重连 | 上次进程被杀,状态仍是 `running` |
| 重启恢复 | 用户重新打开项目 |
| 检查点续跑 | 用户在确认卡上点了「继续」 |

恢复动作:把 `running` 的 run 置为 `failed`(标注「中断」),清暂停标记,重算 stale,重写记忆段。
