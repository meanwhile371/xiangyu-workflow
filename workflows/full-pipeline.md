# W9 — 全流程

## 何时用

从零开始、目标明确要投出去。用户说「全流程」「从零到投稿」「做个完整研究」。

这条路最长,跨天甚至跨周。状态文件是关键 —— 中途换会话不会丢进度。

## 步骤

```
1 of 8  选题        → IDEA_BRIEF.md
2 of 8  深度调研     → research/ + literature_verified.json
3 of 8  实验设计     → EXPERIMENT_PLAN.md
4 of 8  实验执行     → code/ + RESULTS.md + figures/
5 of 8  论文规划     → PAPER_PLAN.md
6 of 8  初稿        → paper/main.md
7 of 8  自审        → REVIEW_REPORT.md
8 of 8  改进循环     → paper/main_v2.md → ... → vN
```

## 与单点工作流的关系

这条路不重写实现,是把几条工作流接起来:

| 本流程步骤 | 实际执行 |
|-----------|---------|
| 1–2 | `paper-writing.md` 步骤 1–2 |
| 3–4 | `data-figures.md` + 实验代码 |
| 5–6 | `paper-writing.md` 步骤 3–4 |
| 7–8 | `review-rebuttal.md` + 六角色红队 |

调度层只负责衔接和状态,不重复定义各步骤的闸门。

## 跨会话恢复

长期项目最关键的能力。新会话开始时:

1. 读 `.xy/STATE.json`,得到已完成步骤和产物清单
2. 读记忆段,得到已确认的决定
3. 重算 stale,得到哪些产物因上游变更失效
4. 报给用户:进度、待办、失效项
5. 等用户点下一步

不要凭对话猜进度。对话已经没了,磁盘还在。

## 检查点

每完成一步写一次盘。跨会话前额外做一次:

```markdown
【检查点】步骤 4 of 8 完成
已完成：选题、调研、实验设计、实验执行
产物：IDEA_BRIEF.md, literature_verified.json, EXPERIMENT_PLAN.md, code/, RESULTS.md, figures/
决定：方法采用 X 而非 Y（证据：预实验显示 X 在 n=50 下更稳）
失效：无
下一步：步骤 5 论文规划
```

这段同时写进 `JOURNAL.md` 和记忆段。后者只保留决定与指针,前者留全文。

## 改进循环的收敛

步骤 8 最多 4 轮,或到「本轮无新增实质问题」为止。

每轮记录:本轮发现的问题、已改的、未改的及原因。连续两轮无新增实质问题时停止 —— 再改下去是打磨措辞,不是提升质量。

闸门:
```yaml
- {kind: machine, check: glob_count, glob: 'paper/main_v*.md', min: 1}
- {kind: machine, check: required_files, files: [REVIEW_REPORT.md]}
- {kind: semantic, claim: 未处理的问题都有书面理由, verify_by: 用户验收}
```

## 中断

三种恢复路径都要先清暂停标记,否则流程会在下一步立刻停住。`[Modex]`

| 路径 | 触发 | 动作 |
|------|------|------|
| 心跳重连 | 上次进程被杀,run 仍是 running | 置 failed 并标「中断」 |
| 重启恢复 | 用户重新打开项目 | 从 STATE 重算,不重跑已完成的 |
| 检查点续跑 | 用户点「继续」 | 从下一未完成步骤起 |
