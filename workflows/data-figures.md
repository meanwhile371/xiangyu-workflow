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

### 步骤 4 — 排版自检与修复

生成后立即自检。检测到图文交叉或比例失衡时,自动修复重出,不提交有问题的图。

#### 4.1 自动检测清单

每张图保存前,用代码检查以下项目:

```python
def check_tick_overlap(ax):
    """检测 x 或 y 轴刻度标签是否重叠"""
    fig = ax.get_figure()
    fig.canvas.draw()
    
    for axis in [ax.xaxis, ax.yaxis]:
        labels = [t.get_window_extent() for t in axis.get_ticklabels()]
        for i in range(len(labels)-1):
            if labels[i].overlaps(labels[i+1]):
                return True, f"{axis.axis_name}轴刻度重叠"
    return False, ""

def check_legend_overlap(ax):
    """检测图例是否与数据点/线重叠"""
    legend = ax.get_legend()
    if legend is None:
        return False, ""
    
    legend_bbox = legend.get_window_extent()
    
    for line in ax.get_lines():
        line_bbox = line.get_window_extent()
        if legend_bbox.overlaps(line_bbox):
            return True, "图例遮挡数据线"
    
    for collection in ax.collections:
        for path in collection.get_paths():
            path_bbox = path.get_extents()
            if legend_bbox.overlaps(path_bbox):
                return True, "图例遮挡散点"
    
    return False, ""

def check_label_clipping(fig):
    """检测轴标签或标题是否超出画布"""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bbox = fig.get_tightbbox(renderer)
    fig_bbox = fig.bbox
    
    if bbox.xmin < 0 or bbox.ymin < 0 or bbox.xmax > fig_bbox.width or bbox.ymax > fig_bbox.height:
        return True, "标签超出画布边界"
    return False, ""

def check_subplot_spacing(fig):
    """检测多子图间距是否过小"""
    if len(fig.axes) < 2:
        return False, ""
    
    fig.canvas.draw()
    bboxes = [ax.get_window_extent() for ax in fig.axes]
    
    for i in range(len(bboxes)):
        for j in range(i+1, len(bboxes)):
            dx = min(abs(bboxes[i].x1 - bboxes[j].x0), abs(bboxes[j].x1 - bboxes[i].x0))
            dy = min(abs(bboxes[i].y1 - bboxes[j].y0), abs(bboxes[j].y1 - bboxes[i].y0))
            
            if dx < 20 or dy < 20:
                return True, f"子图{i}与{j}间距过小"
    return False, ""
```

#### 4.2 自动修复方案

| 问题 | 修法 |
|------|------|
| x轴刻度重叠 | `plt.xticks(rotation=45, ha='right')` 或减少刻度 |
| y轴刻度重叠 | `ax.yaxis.set_major_locator(MaxNLocator(nbins=5))` |
| 图例遮挡数据 | `ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')` |
| 标签被裁切 | `plt.savefig(..., bbox_inches='tight', pad_inches=0.1)` |
| 子图间距过小 | `plt.tight_layout(pad=1.5)` |
| 中文变方框 | `plt.rcParams['font.sans-serif'] = ['SimHei']` |
| 色条压住子图 | `plt.colorbar(..., pad=0.05, shrink=0.8)` |

#### 4.3 修复循环

```python
def fix_and_save(fig, output_path, max_iterations=3):
    """自动检测并修复图表问题,最多尝试3次"""
    for iteration in range(max_iterations):
        issues = []
        
        for ax in fig.axes:
            overlap, msg = check_tick_overlap(ax)
            if overlap:
                issues.append(('tick_overlap', ax, msg))
            
            overlap, msg = check_legend_overlap(ax)
            if overlap:
                issues.append(('legend_overlap', ax, msg))
        
        clip, msg = check_label_clipping(fig)
        if clip:
            issues.append(('label_clip', None, msg))
        
        spacing, msg = check_subplot_spacing(fig)
        if spacing:
            issues.append(('subplot_spacing', None, msg))
        
        if not issues:
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"✓ 图表通过检查: {output_path}")
            return True
        
        print(f"第 {iteration+1} 轮修复: {len(issues)} 个问题")
        for issue_type, ax, msg in issues:
            print(f"  - {msg}")
            apply_fix(issue_type, ax, fig)
        
        fig.canvas.draw()
    
    print(f"⚠ 经 {max_iterations} 轮修复仍有问题,保存当前版本并标记")
    fig.savefig(output_path.replace('.png', '_NEEDS_MANUAL_FIX.png'), dpi=300, bbox_inches='tight')
    return False

def apply_fix(issue_type, ax, fig):
    """应用对应修复"""
    if issue_type == 'tick_overlap':
        if ax.xaxis.get_ticklabels():
            plt.setp(ax.xaxis.get_ticklabels(), rotation=45, ha='right')
        if ax.yaxis.get_ticklabels():
            from matplotlib.ticker import MaxNLocator
            ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    
    elif issue_type == 'legend_overlap':
        legend = ax.get_legend()
        if legend:
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    elif issue_type == 'subplot_spacing':
        fig.tight_layout(pad=1.5)
```

#### 4.4 使用示例

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, y, label='数据')
ax.set_xlabel('时间')
ax.set_ylabel('数值')
ax.legend()

fix_and_save(fig, 'figures/result.png')
```

#### 4.5 人工验收清单

机器检查通过后,人眼最终验收:

- [ ] 图例、标签、标题无遮挡
- [ ] 所有文字在目标版面宽度下可读
- [ ] 色条范围合理
- [ ] 多子图对齐整齐
- [ ] 无不必要的空白边缘

闸门:
```yaml
- {kind: machine, check: glob_count, glob: figures/*_NEEDS_MANUAL_FIX.png, max: 0}
- {kind: semantic, claim: 逐图看过后确认无交叉, verify_by: 人眼}
```

## 交付

每个图配一段图注:图是什么、n 多少、数据来源、误差棒含义。图注写在正文里,不嵌在图内。
