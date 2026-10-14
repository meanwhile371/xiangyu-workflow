# xiangyu-workflow

工作流调度台 — 常驻本机的学术写作流水线编排层

## 简介

一套工作流调度层，用户说「写数模」「写论文」「继续上次」，它负责选工作流、报进度、要确认、跑步骤、卡质量、落盘状态。

工作流本身不重复实现已有能力，而是把现有技能编排成一条有依赖、有闸门、有记忆的流水线。

## 功能特性

- **进度外置**：进度写在磁盘上，换会话、换天、换窗口都能读回来
- **产物按事实判定**：一步是否完成，只看文件是否真的出现或变更
- **确定性校验只读**：查询永不写盘、永不调用模型、永不重启流程

## 支持的工作流

| 编号 | 工作流 | 触发语 |
|------|--------|--------|
| W1 | 论文写作 | 写论文、写paper、写SCI、投稿 |
| W2 | 数学建模竞赛 | 写数模、比赛、竞赛论文、美赛、国赛 |
| W3 | 文献综述 | 综述、文献调研、related work |
| W4 | 开题报告 | 开题、proposal、学位论文开题 |
| W5 | 课程论文 | 课程论文、结课论文、大作业论文 |
| W6 | 从已有资料写论文 | 我有数据/代码/图、整理成论文 |
| W7 | 数据与图表 | 跑数据分析、出图、改图 |
| W8 | 审稿与返修 | 审稿意见、rebuttal、返修、被拒了 |
| W9 | 全流程 | 从零到投稿、全流程 |

## 目录结构

```
xiangyu-workflow/
├── SKILL.md              # 技能主文件
├── references/           # 参考文档
│   └── protocol.md      # 状态文件schema、记忆段格式、质量闸写法
├── workflows/            # 工作流定义
│   ├── paper-writing.md
│   ├── modeling-comp.md
│   ├── literature-review.md
│   ├── thesis-proposal.md
│   ├── course-paper.md
│   ├── paper-from-assets.md
│   ├── data-figures.md
│   ├── review-rebuttal.md
│   └── full-pipeline.md
└── scripts/              # 辅助脚本
    └── check_state.py   # 只读校验，输出进度摘要
```

## 使用方法

详见 SKILL.md 文件。

## 来源说明

骨架取自 Modex-MH-Agent(明珩科技)反编译得到的编排机制。

## License

MIT

