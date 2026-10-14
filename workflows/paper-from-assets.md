# W6 — 从已有资料写论文

## 何时用

用户已经完成实验/代码/数据分析,手里有结果,只差成文。用户说「我有数据/代码/图」「整理成论文」「把实验结果写成paper」。

不适用:还没开始实验 → W1 或 W9;只有想法没有数据 → W1。

## 步骤

```
1 of 5  资产盘点         → ASSETS_INVENTORY.md
2 of 5  补足证据         → EVIDENCE_GAP.md + 补充实验
3 of 5  故事重构         → STORY_PLAN.md
4 of 5  论文撰写         → paper/main.md
5 of 5  终审             → paper/main.docx + FINAL_CHECK.md
```

## 各步骤

### 步骤 1 — 资产盘点

**操作:**

1. **列出所有已有资产:**

   **代码类:**
   - 模型实现在哪个文件?
   - 训练脚本是否能重跑?
   - 评估脚本是否输出所有指标?
   - 超参数记录在哪里?

   **数据类:**
   - 数据集来源(公开 / 自建)?
   - 数据预处理步骤记录在哪?
   - 训练/验证/测试集划分比例?
   - 数据统计(样本量/分布/缺失率)?

   **结果类:**
   - 主要实验的结果表格/图表
   - 消融实验结果
   - 与基线方法对比
   - 实验日志/记录本

2. **评估完整性** — 对照论文必需内容:

   | 内容 | 已有? | 缺失? |
   |------|-------|-------|
   | 方法描述 | ✓ 代码注释 | ✗ 算法伪代码 |
   | 主要结果 | ✓ 准确率表格 | ✗ 统计显著性检验 |
   | 消融实验 | ✓ 部分组件 | ✗ 完整ablation |
   | 可视化 | ✓ loss曲线 | ✗ 案例分析图 |
   | 基线对比 | ✓ 2个基线 | ✗ SOTA方法对比 |

3. **输出 ASSETS_INVENTORY.md**:
   ```markdown
   ## 已有资产
   
   ### 代码
   - `src/model.py`: 模型实现(500行)
   - `train.py`: 训练脚本(可重跑)
   - `eval.py`: 评估脚本
   
   ### 数据
   - Dataset: ImageNet subset (50k images)
   - Split: 70% train / 15% val / 15% test
   - Preprocessing: 记录在 `data/preprocess.py`
   
   ### 结果
   - 主实验: `results/main_results.csv`
   - 消融实验: `results/ablation.csv`
   - 图表: `figures/` (5张PNG)
   
   ## 完整性评估
   
   ✓ 已充分: 模型实现、主要结果、部分消融
   ⚠ 需补充: 统计检验、完整消融、案例分析
   ✗ 缺失: 与SOTA对比、失败案例分析
   ```

闸门:
```yaml
- {kind: machine, check: required_files, files: [ASSETS_INVENTORY.md]}
- {kind: machine, check: min_size, file: ASSETS_INVENTORY.md, bytes: 600}
- {kind: semantic, claim: 代码是否可重跑, verify_by: 用户确认}
```

---

### 步骤 2 — 补足证据

**操作:**

1. **识别证据缺口** — 论文需要但手头没有的:

   **必需补充(不补无法投稿):**
   - 统计显著性检验(t-test / Wilcoxon)
   - 完整消融实验(每个组件的贡献)
   - 与当前SOTA方法对比
   - 误差分析或失败案例

   **建议补充(提升可信度):**
   - 不同随机种子的结果(报告均值±标准差)
   - 超参数敏感性分析
   - 跨数据集泛化性验证
   - 可视化(注意力图 / 特征图)

   **可选补充(锦上添花):**
   - 用户研究
   - 在线实验/A/B测试
   - 理论分析(收敛性证明等)

2. **制定补充计划**:
   ```markdown
   ## 必须补充
   
   ### 1. 统计显著性 (预计1天)
   - 工具: scipy.stats.ttest_ind
   - 对比组: 我们的方法 vs 最强基线
   - 重复次数: 5次不同随机种子
   
   ### 2. 完整消融 (预计2天)
   缺失组件:
   - [ ] 去掉注意力机制
   - [ ] 去掉残差连接
   - [ ] 去掉预训练
   
   ### 3. SOTA对比 (预计3天)
   需要复现的方法:
   - [ ] MethodA (2023, NeurIPS)
   - [ ] MethodB (2024, ICML)
   ```

3. **执行补充实验** — 按计划跑实验:
   - 记录所有超参数
   - 保存原始输出日志
   - 整理成表格/图表

4. **输出 EVIDENCE_GAP.md + 补充结果**

闸门:
```yaml
- {kind: machine, check: required_files, files: [EVIDENCE_GAP.md]}
- {kind: falsifiable_check, claim: 必需补充项已完成}
- {kind: semantic, claim: 统计检验p值<0.05, verify_by: 检查结果文件}
```

---

### 步骤 3 — 故事重构

**操作:**

**常见问题:** 实验顺序 ≠ 论文顺序

实验时你可能是:
```
1. 先试了简单baseline
2. 发现不work,加了注意力
3. 又加了残差连接
4. 最后发现预训练很重要
```

但论文应该是:
```
1. 介绍问题和挑战
2. 提出完整方法(注意力+残差+预训练)
3. 消融实验证明每个组件的必要性
4. 与baseline和SOTA对比
```

1. **重构叙事线** — 从结果倒推故事:

   **问自己:**
   - 这个工作的核心贡献是什么?(一句话)
   - 为什么之前的方法做不到?(指出limitation)
   - 我们的方法如何解决?(关键创新点)
   - 实验如何证明?(最convincing的结果是哪个?)

2. **设计证据链**:
   ```markdown
   ## 故事主线
   
   问题: 现有方法在小样本场景下性能急剧下降
   ↓
   洞察: 关键在于如何利用预训练知识
   ↓
   方法: 提出自适应特征融合模块
   ↓
   证明: 
   - 主实验: 小样本场景下提升15% (Table 1)
   - 消融: 每个组件都必要 (Table 2)
   - 泛化: 跨3个数据集验证 (Table 3)
   - 可视化: 注意力确实关注关键区域 (Figure 2)
   ```

3. **规划章节内容**:
   ```markdown
   ## Introduction (为什么重要)
   - 第1段: 领域背景
   - 第2段: 现有方法的局限(引出小样本问题)
   - 第3段: 我们的贡献(三点)
   
   ## Methods (怎么做的)
   - 整体框架 + Figure 1
   - 模块A: 特征提取
   - 模块B: 自适应融合(核心创新)
   - 模块C: 分类器
   
   ## Results (有没有用)
   - 4.1 小样本主实验 (核心结果)
   - 4.2 消融实验 (证明设计合理)
   - 4.3 跨数据集泛化 (证明鲁棒)
   - 4.4 可视化分析 (直观展示)
   
   ## Discussion (为什么work)
   - 与SOTA对比分析
   - 失败案例与局限
   - 未来方向
   ```

4. **输出 STORY_PLAN.md**

闸门:
```yaml
- {kind: machine, check: required_files, files: [STORY_PLAN.md]}
- {kind: falsifiable_check, claim: 每个claim都有对应的实验证据}
```

---

### 步骤 4 — 论文撰写

**操作:**

**关键原则: 从代码反推方法,不凭印象写**

1. **Methods 从代码反推:**

   ```python
   # 读代码
   class MyModel(nn.Module):
       def __init__(self, embed_dim=256, num_heads=8):
           self.attention = MultiHeadAttention(embed_dim, num_heads)
           self.ffn = FeedForward(embed_dim, hidden_dim=1024)
   
   # 写成方法描述
   "我们的模型包含多头注意力层(d=256, h=8)和前馈网络(隐藏层1024维)..."
   ```

   **避免:** 凭印象写"我们使用了先进的注意力机制" — 读者看不懂

2. **Results 从实验日志提取:**

   ```python
   # 读日志
   2024-10-14 10:23:45 - Epoch 50/50
   2024-10-14 10:23:45 - Train Loss: 0.234
   2024-10-14 10:23:45 - Val Acc: 87.3%
   2024-10-14 10:23:45 - Test Acc: 85.6%
   
   # 写成结果描述
   "在测试集上,我们的方法达到85.6%准确率,
   优于baseline的78.2%(提升7.4个百分点,p<0.01)"
   ```

   **数字要对得上** — 论文里的每个数字必须可追溯到实验记录

3. **Figure 从已有图重制:**

   **已有的 matplotlib 图可能不符合期刊标准:**
   - 字号太小
   - 配色不色盲友好
   - 没有误差棒
   - 分辨率不够

   **重制清单:**
   ```python
   import matplotlib.pyplot as plt
   import seaborn as sns
   
   sns.set_context("paper")  # 期刊字号
   sns.set_palette("colorblind")  # 色盲友好
   
   fig, ax = plt.subplots(figsize=(3.5, 2.625))  # Nature单栏
   
   # 重新绘图...
   
   ax.set_xlabel('...', fontsize=9)
   ax.tick_params(labelsize=8)
   plt.tight_layout()
   fig.savefig('figures/fig1.pdf', dpi=300, bbox_inches='tight')
   ```

4. **写作顺序建议:**

   ```
   1. Methods (最简单,照着代码写)
   2. Results (照着实验记录写)
   3. Introduction (知道自己做了什么后再写背景)
   4. Discussion (知道结果后再解释)
   5. Abstract (最后写,浓缩全文)
   ```

5. **输出 paper/main.md**

闸门:
```yaml
- {kind: machine, check: required_files, files: [paper/main.md]}
- {kind: machine, check: min_size, file: paper/main.md, bytes: 5000}
- {kind: falsifiable_check, claim: Methods里的参数设置与代码一致}
- {kind: falsifiable_check, claim: Results里的数字与实验记录一致}
```

---

### 步骤 5 — 终审

**操作:**

1. **数值一致性核查:**

   **自动化脚本:**
   ```python
   import re
   
   # 提取论文中的数值
   paper_text = open('paper/main.md').read()
   paper_numbers = re.findall(r'\d+\.\d+%', paper_text)
   
   # 提取实验记录中的数值
   results = pd.read_csv('results/main_results.csv')
   
   # 对比
   for num in paper_numbers:
       if num not in results.values:
           print(f"WARNING: {num} 在实验记录中找不到!")
   ```

2. **代码-方法一致性:**

   **检查清单:**
   - [ ] 论文提到的每个模块在代码里都有
   - [ ] 超参数数值与代码/日志一致
   - [ ] 数据集划分比例正确
   - [ ] 训练轮次/batch size 等设置正确

3. **可重现性检查:**

   **必需文件:**
   ```
   ├── README.md (运行说明)
   ├── requirements.txt (依赖)
   ├── data/ (数据或下载脚本)
   ├── src/ (模型代码)
   ├── train.py (训练脚本)
   ├── eval.py (评估脚本)
   └── results/ (实验结果)
   ```

   **README 必须包含:**
   ```markdown
   ## 如何复现
   
   1. 环境: `pip install -r requirements.txt`
   2. 数据: `bash download_data.sh`
   3. 训练: `python train.py --config configs/main.yaml`
   4. 评估: `python eval.py --checkpoint checkpoints/best.pth`
   
   预期结果: Test Acc = 85.6% ± 0.3%
   ```

4. **输出 FINAL_CHECK.md + paper/main.docx**

闸门:
```yaml
- {kind: machine, check: required_files, files: [FINAL_CHECK.md, paper/main.docx]}
- {kind: falsifiable_check, claim: 代码可重跑且结果与论文一致}
- {kind: semantic, claim: 所有数值已核对, verify_by: 用户验收}
```

---

## 依赖关系

```
ASSETS_INVENTORY.md → EVIDENCE_GAP.md → STORY_PLAN.md → paper/main.md → 终审
                              ↓
                      补充实验(并行)
```

改 STORY_PLAN.md 后必须重写 paper/main.md。

---

## 常见陷阱

**陷阱1: 代码与论文不一致**

症状:
- 论文说用了BatchNorm,代码里是LayerNorm
- 论文说训练100 epoch,日志只有50 epoch
- 论文说用Adam优化器,代码用的SGD

后果: 无法复现,被拒稿或撤稿

解决: 步骤5的终审必须逐项核对

---

**陷阱2: 实验不足**

症状:
- 只跑了一次,没有多次重复
- 只在一个数据集上测试
- 没有消融实验

后果: 审稿人质疑结果可靠性

解决: 步骤2的补充实验必须完成

---

**陷阱3: 故事倒推不合理**

症状:
- Introduction提出的问题,Results没有回答
- 声称解决了X问题,但实验只测了Y
- 创新点与实验亮点对不上

后果: 审稿人认为逻辑混乱

解决: 步骤3的故事重构必须保证claim-evidence对应

---

## 时间估算

- 步骤1: 0.5天(盘点)
- 步骤2: 3-7天(补实验,视缺口大小)
- 步骤3: 1天(重构)
- 步骤4: 5-10天(写作)
- 步骤5: 1-2天(终审)

总计: 2-3周(资产齐全) / 4-6周(需大量补充)
