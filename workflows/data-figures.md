# W7 — 数据与图表

## 何时用

需要跑数据分析、出论文级图表、修图表排版。用户说「跑一下数据」「出个图」「图重叠了」「改图」。

可作为独立工作流,也可作为 W1/W2/W5 的插入步骤。

## 步骤

```
1 of 4  数据检查     → DATA_CHECK.md
2 of 4  分析         → 分析脚本 + outputs/
3 of 4  出图         → figures/
4 of 4  排版自检     → 修复后的 figures/
```

## 各步骤

### 步骤 1 — 数据检查

先看数据,再看问题。

产出 `DATA_CHECK.md`:字段含义、缺失值、异常值、样本量、时间跨度、已知局限。

闸门:
```yaml
- {kind: machine, check: required_files, files: [DATA_CHECK.md]}
- {kind: falsifiable_check, claim: 每个字段的含义有依据,不是猜的}
```

字段含义不明时问用户,不要假设。假设错了解释全错。

### 步骤 2 — 分析

产出分析脚本与 `outputs/`。每个数值输出同时落一份 CSV,放在同目录,文件名与主输出一致(除扩展名)。

所有 Python 脚本开头加 UTF-8 包装:

```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
```

闸门:
```yaml
- {kind: machine, check: dir_exists, dir: outputs}
- {kind: machine, check: glob_count, glob: outputs/*.csv, min: 1}
- {kind: falsifiable_check, claim: 每个统计量可用脚本复算}
```

### 步骤 3 — 出图

产出 `figures/*.png`(或 `.pdf`)。

图的三条要求:

1. 标注、图例、标题不得与图形元素重叠
2. 图例、轴标签、色条、子图间距边界清晰
3. 字号在目标版面宽度下可读

闸门:
```yaml
- {kind: machine, check: glob_count, glob: figures/*.png, min: 1}
- {kind: semantic, claim: 无图文交叉, verify_by: 人眼}
```

### 步骤 4 — 排版自检

生成后立即自检。检测到图文交叉或比例失衡时,自动修复重出,不提交有问题的图。

常见问题与修法:

| 问题 | 修法 |
|------|------|
| 图例遮挡数据 | 图例移到图外,或调整 `bbox_to_anchor` |
| 刻度标签重叠 | 旋转标签,或缩短标签,或改字号 |
| 子图间距过小 | `plt.tight_layout()` 或 `constrained_layout` |
| 中文字符变方框 | 设 `font.sans-serif` 为中文字体 |
| 色条压住子图 | `pad` 调大,或改用共享色条 |
| 保存后边缘被裁 | `bbox_inches='tight'` |

重叠或遮挡反复修不好时,转 `matplotlib-fix`。

闸门:
```yaml
- {kind: semantic, claim: 逐图看过后确认无交叉, verify_by: 人眼}
```

## 交付

每个图配一段图注:图是什么、n 多少、数据来源、误差棒含义。图注写在正文里,不嵌在图内。
