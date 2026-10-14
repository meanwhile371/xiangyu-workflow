# 依赖的技能包

xiangyu-workflow 是一个工作流编排层，它调用以下技能来完成具体任务。**使用本工作流前必须先安装这些依赖技能。**

## 必需技能

### 1. Anthropic 官方技能包

这些技能来自 Anthropic 官方 skills 仓库，需要通过 Claude Desktop 的技能市场或手动安装：

| 技能名 | 用途 | GitHub 链接 |
|--------|------|------------|
| `nature-writing` | 论文写作 | https://github.com/anthropics/anthropic-skills |
| `nature-polishing` | 论文润色 | https://github.com/anthropics/anthropic-skills |
| `nature-academic-search` | 文献检索 | https://github.com/anthropics/anthropic-skills |
| `nature-citation` | 引用格式 | https://github.com/anthropics/anthropic-skills |
| `nature-figure` | Nature 级图表 | https://github.com/anthropics/anthropic-skills |
| `nature-response` | 审稿回复 | https://github.com/anthropics/anthropic-skills |
| `academic-paper-reviewer` | 论文评审 | https://github.com/anthropics/anthropic-skills |
| `deep-research` | 深度研究 | https://github.com/anthropics/anthropic-skills |
| `brainstorming` | 头脑风暴 | https://github.com/anthropics/anthropic-skills |
| `humanizer-zh` | 去 AI 痕迹（中文） | https://github.com/anthropics/anthropic-skills |

### 2. 社区技能

| 技能名 | 用途 | GitHub 链接 | 安装方法 |
|--------|------|------------|----------|
| `citation-check-skill` | 引用验证 | *需要查找* | 手动安装到 `~/.claude/skills/` |
| `matplotlib-fix` | 图文修复 | *需要查找* | 手动安装到 `~/.claude/skills/` |
| `scipilot-figure-skill` | 科研绘图 | *需要查找* | 手动安装到 `~/.claude/skills/` |

## 安装方法

### 方法 1：通过 Claude Desktop 技能市场（推荐）

1. 打开 Claude Desktop
2. 进入 Settings → Skills
3. 搜索并安装上述 Anthropic 官方技能

### 方法 2：手动从 GitHub 安装

```bash
# 克隆 Anthropic 官方技能仓库
git clone https://github.com/anthropics/anthropic-skills.git

# 将需要的技能复制到 Claude 技能目录
cp -r anthropic-skills/nature-writing ~/.claude/skills/
cp -r anthropic-skills/nature-polishing ~/.claude/skills/
# ... 其他技能类似
```

### 方法 3：检查已安装技能

在 Claude 中询问：
```
列出所有已安装的技能
```

或检查技能目录：
```bash
ls ~/.claude/skills/
```

## 验证安装

安装完成后，在 Claude 中测试：

```
使用 xiangyu-workflow 开始一个论文写作项目
```

如果提示缺少某个技能，请按上述方法安装对应技能。

## 可选优化

为了获得最佳体验，建议同时安装：
- **MCP 服务器**：用于 GitHub 集成、文献数据库访问等
- **Zotero 插件**：用于文献管理集成

## 问题排查

**Q: 提示"技能不存在"或"编排技能外"**

A: 说明对应技能未安装或路径不正确。检查：
1. 技能是否在 `~/.claude/skills/` 目录下
2. 技能目录结构是否正确（需要 `SKILL.md` 或 `manifest.yaml`）
3. 重启 Claude Desktop 让技能生效

**Q: anthropic-skills 仓库无法访问**

A: 使用代理或从镜像站下载：
```bash
# 使用代理
export http_proxy=http://127.0.0.1:33210
export https_proxy=http://127.0.0.1:33210
git clone https://github.com/anthropics/anthropic-skills.git
```

## 更新日志

- 2026-10-14: 初始版本，列出 13 个依赖技能
