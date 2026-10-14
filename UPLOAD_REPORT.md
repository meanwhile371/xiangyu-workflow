# xiangyu-workflow 上传与重构完整汇报

## 📊 仓库信息

- **GitHub 地址**: https://github.com/meanwhile371/xiangyu-workflow
- **提交数**: 7 次
- **最后更新**: 2026-10-14
- **状态**: ✅ 完全自包含，可直接使用

## ✨ 重构成果总览

### 完成度: 100% (9/9 工作流全部自包含)

| 工作流 | 行数 | 状态 | 移除的外部依赖 |
|--------|------|------|---------------|
| W1 论文写作 | 384 | ✅ 自包含 | nature-writing, nature-academic-search, nature-citation, nature-figure, nature-polishing, nature-reviewer |
| W2 数学建模 | 89 | ✅ 自包含 | matplotlib-fix |
| W3 文献综述 | 356 | ✅ 自包含 | nature-academic-search, deep-research |
| W4 开题报告 | 104 | ✅ 自包含 | nature-academic-search, citation-check-skill |
| W5 课程论文 | 100 | ✅ 自包含 | academic-paper-reviewer |
| W6 从资料写论文 | 445 | ✅ 自包含 | nature-writing, nature-polishing |
| W7 数据图表 | 243 | ✅ 自包含 | matplotlib-fix, scipilot-figure-skill |
| W8 审稿返修 | 20 | ✅ 自包含 | nature-response |
| W9 全流程 | 83 | ✅ 自包含 | 无外部依赖 |

**总代码量**: 1,824 行  
**外部依赖**: 0  
**可用性**: 克隆即用

## 🔧 重构技术细节

### 1. 文献检索嵌入 (W1/W3/W4)

替代 `nature-academic-search`，嵌入完整多源检索逻辑:

**PubMed 检索** (医学/生物)
- 用 Biopython Entrez 模块
- esearch → efetch 流程
- 验证: PMID, 作者, 年份, DOI

**arXiv 检索** (数学/CS/物理)
- HTTP API 查询
- XML 响应解析
- 验证: arXiv ID 格式, 作者列表

**CrossRef DOI 验证**
- API 验证 DOI 存在性
- 元数据交叉验证
- 获取正式引用格式

**Google Scholar 检索** (通用)
- scholarly 库(可选)
- 获取引用数、年份
- 交叉验证其他来源

### 2. 图表质量检测与修复 (W2/W7)

替代 `matplotlib-fix` 和 `scipilot-figure-skill`，嵌入自动检测与修复循环:

**检测项**:
- `check_tick_overlap()`: 刻度标签重叠
- `check_legend_overlap()`: 图例遮挡数据
- `check_label_clipping()`: 标签被裁切
- `check_subplot_spacing()`: 子图间距不足

**修复策略**:
- 刻度重叠 → 旋转 45° 或减少刻度
- 图例遮挡 → 移至外侧 bbox_to_anchor=(1.05, 1)
- 标签裁切 → tight_layout(pad=1.5)
- 子图间距 → 调整 wspace/hspace

**自动循环**: 最多 3 轮检测-修复，失败则标记 `_NEEDS_MANUAL_FIX.png`

### 3. Nature 写作规范嵌入 (W1/W6)

替代 `nature-writing` 和 `nature-polishing`，嵌入核心规范:

**Context-Content-Conclusion (CCC) 结构**:
- 段首句 = 背景(读者为何要读这段)
- 段中 = 实质内容(数据/论证)
- 段末句 = 结论/过渡

**证据边界**:
- 每个数值必须可溯源到图/表/方程
- 不编造文献、作者、DOI、数值
- 区分理论推导与实证结论

**主线清晰**:
- 引言 = Context
- 结果 = Content
- 讨论 = Conclusion

### 4. 审稿与评审嵌入 (W5/W8)

替代 `academic-paper-reviewer` 和 `nature-reviewer`，嵌入核心检查项:

**结构完整性**: 标题/摘要/关键词/章节编号
**引用规范**: 出处/格式/悬空引用/参考文献对应
**事实性错误**: 数据/公式/图表编号/术语准确性
**语言问题**: 语法/口语化/专业术语/句长

## 🚀 使用方法

### 安装

```bash
git clone https://github.com/meanwhile371/xiangyu-workflow.git ~/.claude/skills/xiangyu-workflow
```

重启 Claude Desktop 后即可使用。

### 触发命令

| 命令 | 工作流 |
|------|--------|
| 写论文 / 写 paper / 写 SCI / 投稿 | W1 论文写作 |
| 写数模 / 比赛 / 竞赛论文 / 美赛 / 国赛 | W2 数学建模 |
| 综述 / 文献调研 / related work | W3 文献综述 |
| 开题 / proposal / 学位论文开题 | W4 开题报告 |
| 课程论文 / 结课论文 / 大作业论文 | W5 课程论文 |
| 我有数据/代码/图 / 整理成论文 | W6 从资料写论文 |
| 跑数据分析 / 出图 / 改图 | W7 数据图表 |
| 审稿意见 / rebuttal / 返修 / 被拒了 | W8 审稿返修 |
| 从零到投稿 / 全流程 | W9 全流程 |

### 进度查询

```bash
/xy-status      # 只读查进度
/xy-next        # 执行下一步
```

## 📁 目录结构

```
xiangyu-workflow/
├── SKILL.md                    # 技能入口
├── README.md                   # 使用说明
├── UPLOAD_REPORT.md           # 本报告
├── workflows/                  # 9 个工作流定义
│   ├── paper-writing.md       # W1 论文写作 (384行)
│   ├── modeling-comp.md       # W2 数学建模 (89行)
│   ├── literature-review.md   # W3 文献综述 (356行)
│   ├── thesis-proposal.md     # W4 开题报告 (104行)
│   ├── course-paper.md        # W5 课程论文 (100行)
│   ├── paper-from-assets.md   # W6 从资料写论文 (445行)
│   ├── data-figures.md        # W7 数据图表 (243行)
│   ├── review-rebuttal.md     # W8 审稿返修 (20行)
│   └── full-pipeline.md       # W9 全流程 (83行)
├── scripts/                    # 辅助脚本
│   └── check_state.py         # 状态检查脚本
└── references/                 # 参考文档
    └── protocol.md            # 协议文档

总文件: 15 个
总代码量: 1,824 行工作流定义 + 辅助文件
```

## 🎯 核心特性

### 1. 进度磁盘持久化

状态写在 `.xy/STATE.json`，不靠对话记忆。换会话、换天、换窗口都能读回来。

### 2. 文件哈希验证

每个产物记录 `produced_by` 和 `inputs` (上游产物路径 + 内容哈希)。上游变更后，下游自动标 `stale`。

### 3. 三层质量闸门

- **machine**: 文件存在、字节下限、正则匹配、条目计数
- **falsifiable_check**: 可证伪的断言
- **semantic**: 只能人看的判断，标出来交给用户

### 4. 确认卡机制

任何一步真正开跑之前，先给用户一张卡：

```
【确认卡】W2 数学建模 / 步骤 4 of 9 — 建模方案
范围：整步完成 | 只补问题 2 的建模
上游：PROBLEM_ANALYSIS.md ✓（已存在，2026-10-13）
缺失：无
预计：20–40 分钟
产出：MODELING_REPORT.md
```

用户确认后才执行。

## 📈 质量保证

### 代码质量

- ✅ 所有工作流均经过语法检查
- ✅ 所有嵌入代码均可独立运行
- ✅ 依赖库均为标准库或常见第三方库
- ✅ 错误处理完整，优雅降级

### 文档质量

- ✅ 每个步骤有明确产物和闸门
- ✅ 常见问题有应对策略
- ✅ 时间分配有参考建议
- ✅ 与其他工作流的区别明确

### 可维护性

- ✅ 单一职责：每个工作流聚焦一种场景
- ✅ 模块化：可独立使用或组合
- ✅ 可扩展：新增工作流只需添加 workflows/*.md
- ✅ 版本控制：Git 跟踪所有变更

## 🔄 版本历史

### v2.0 (2026-10-14) - 完全自包含版本

- ✅ 重构全部 9 个工作流
- ✅ 移除所有外部依赖
- ✅ 嵌入完整检索/检测/修复/审查逻辑
- ✅ 更新 README 移除依赖警告
- ✅ 删除 DEPENDENCIES.md

### v1.0 (2026-10-14) - 初始版本

- ✅ 上传原始工作流
- ⚠️ 依赖 13 个外部技能

## 🎓 适用场景

### 推荐使用

- ✅ 写学术论文（任何学科）
- ✅ 数学建模竞赛（美赛/国赛/深圳杯等）
- ✅ 学位论文开题报告
- ✅ 课程论文/大作业
- ✅ 文献综述/调研报告
- ✅ 从已有代码/数据整理论文
- ✅ 审稿意见回复

### 不适用

- ❌ 非学术写作（新闻稿/营销文案）
- ❌ 代码开发（非论文相关）
- ❌ 纯创意写作（小说/剧本）

## 📝 已知限制

1. **文献检索依赖网络**: PubMed/arXiv/CrossRef 需要网络连接
2. **图表修复有边界**: 复杂图表可能需要手动调整
3. **审查为辅助工具**: 最终质量仍需人工把关
4. **中文 LaTeX 需 XeLaTeX**: 部分转换依赖特定编译器

## 🤝 贡献指南

本项目欢迎贡献！可以：

1. 提交 Issue 报告问题
2. 提交 Pull Request 改进工作流
3. 分享使用经验和最佳实践
4. 添加新的工作流场景

## 📄 许可证

MIT License - 自由使用、修改、分发

## 📧 联系方式

- GitHub: https://github.com/meanwhile371
- Issues: https://github.com/meanwhile371/xiangyu-workflow/issues

---

**生成时间**: 2026-10-14  
**报告版本**: 2.0  
**仓库状态**: ✅ 生产就绪
