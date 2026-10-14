# xiangyu-workflow

工作流调度台 — 常驻本机的学术写作流水线编排层

## ⚠️ 重要提示

**本工作流依赖 13 个外部技能包才能正常运行。使用前必须先安装依赖！**

👉 **[查看完整依赖列表和安装方法](DEPENDENCIES.md)**

核心依赖包括：
- `nature-writing` / `nature-polishing` - 论文写作与润色
- `nature-academic-search` / `citation-check-skill` - 文献检索与验证
- `academic-paper-reviewer` - 论文评审
- `deep-research` / `brainstorming` - 研究与策划
- `nature-figure` / `matplotlib-fix` - 图表制作与修复

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

## 快速开始

### 1. 安装本技能

```bash
# 克隆到 Claude 技能目录
git clone https://github.com/meanwhile371/xiangyu-workflow.git ~/.claude/skills/xiangyu-workflow
```

### 2. 安装依赖技能

**必须完成此步骤！** 详见 [DEPENDENCIES.md](DEPENDENCIES.md)

推荐通过 Claude Desktop 技能市场安装 Anthropic 官方技能包。

### 3. 验证安装

重启 Claude Desktop 后，在对话中输入：

```
使用 xiangyu-workflow 开始一个论文写作项目
```

如果提示缺少某个技能，请返回第 2 步安装对应依赖。

## 目录结构

```
xiangyu-workflow/
├── README.md             # 本文件
├── DEPENDENCIES.md       # 依赖技能清单（必读）
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

典型用法：
```
# 启动论文写作工作流
写论文

# 查看当前进度
现在做到哪一步

# 继续上次中断的工作
继续上次
```

## 工作流原理

每个工作流分为多个步骤，每步：
1. 检查上游产物是否齐全
2. 向用户展示确认卡（范围、预计时间、产出）
3. 调用对应技能执行任务
4. 通过质量闸验收产物
5. 更新状态文件 `.xy/STATE.json`

状态持久化在磁盘，进度不依赖对话记忆。

## 来源说明

骨架取自 Modex-MH-Agent(明珩科技)反编译得到的编排机制。

## 问题排查

**Q: 提示"技能不存在"或"编排技能外"**

A: 说明对应技能未安装。请查看 [DEPENDENCIES.md](DEPENDENCIES.md) 并安装所有依赖技能。

**Q: 工作流卡在某一步不推进**

A: 检查 `.xy/STATE.json` 和 `.xy/JOURNAL.md`，确认上游产物是否真的生成。

**Q: 如何重置工作流状态**

A: 删除项目目录下的 `.xy/` 文件夹即可重新开始。

## License

MIT

## 贡献

欢迎提交 Issue 和 Pull Request！
