# Security Track — 安装与使用

> 本 fork 在上游 ARS（4 个 skill）之上增加第 5 个 skill `security-track`：
> 面向安全顶会（四大 + tier-2）研究的覆盖层，校准方向为 CPS / IoT / AI 安全。
> 上游文件零改动（唯一例外：`marketplace.json` 注册行），`main` 分支保持
> upstream 纯净镜像，全部定制在 `dev` 分支（GitHub 默认分支已设为 `dev`）。

## 这个 skill 包含什么

| 文件 | 内容 |
|---|---|
| `SKILL.md` | 触发条件 + 对 stock ARS 的覆盖规则（引用格式、论文结构、审稿面板、双盲、截稿铁律） |
| `references/big4_venue_profiles.md` | 四大会档案：格式 / 判定机制 / AE / 伦理（经官方 CFP 逐条核实，2023–2027 各版） |
| `references/security_paper_conventions.md` | 安全论文行文规范：Threat Model 章、三方向评估门槛、责任披露、匿名化清单 |
| `references/security_reviewer_personas.md` | 5 人安全审稿面板 + 八条标准拒稿锚点 |
| `references/major_revision_playbook.md` | 四大会多轮评审实战手册：rebuttal / revision / re-review 机制 + ARS 模式映射 |
| `references/perspective_retrieval_protocol.md` | 视角驱动检索协议（STORM 检索侧机制改造，opt-in） |
| `references/conference_ranking_2025.json` | 22 会 CIF 排名快照（源：jianying.space，每年更新） |
| `references/deadlines_current.md` | 截稿日历（**生成文件，勿手改**，源：sec-deadlines.github.io） |
| `scripts/fetch_deadlines.py` | 截稿日历拉取脚本（每次 `git sync-upstream` 自动执行） |
| `contracts/reviewer/security_full.json` | 安全顶会版 sprint contract（盲态预提交标尺；Schema 13.2 验证通过，F 条件语法与上游一致） |
| `references/research_loop_protocol.md` | 研究闭环协议：S0 选题→S1 gap→S2 课题延伸→S3 方法提出/评估（novelty+contribution）→S4 证伪实验设计→S5 执行→S6 有界改进循环→S7 对抗压测→S8 论文 |

## 安装（Claude Code）

```
# 若装过 upstream 版，先移除（marketplace 同名会冲突）
/plugin marketplace remove academic-research-skills

# 方式 A：从 GitHub 安装（默认分支已是 dev，直接装到本版本）
/plugin marketplace add waterwoods-ai/academic-research-skills

# 方式 B：本机开发者模式——本地 clone 作为 marketplace，编辑即生效
/plugin marketplace add /path/to/academic-research-skills

# 安装
/plugin install academic-research-skills@academic-research-skills
```

装完**开新 session** 生效。验证：问一句「NDSS 的 Major Revision 流程是什么」，
agent 应去读 `major_revision_playbook.md` 而非凭记忆作答。

更新：GitHub 源用 `/plugin update academic-research-skills`；
本地路径源无需重装，重开 session 即可。

## 使用

**自动激活**：论文任务涉及安全会议即触发（会议名、threat model、CPS/IoT/
AI security 等触发词，见 `SKILL.md` frontmatter）。用户档案为安全研究方向时，
所有论文任务默认按安全会议处理；明确说明非安全研究则回退 stock 行为。

**与 ARS 命令的配合**（overlay 自动叠加，无需额外指定）：

| 你要做的事 | 用法 | overlay 提供 |
|---|---|---|
| 选会 / 投稿规划 | 直接提问，或 `/ars-plan` | venue 档案 + 实时截稿日历 |
| 文献综述 | `/ars-lit-review`；说「确保覆盖全面」触发视角检索协议 | 6 透镜查询扩展 + 未用检索追问 |
| 写作 / 大纲 | `/ars-outline`、`/ars-full` | 安全论文结构、numeric 引用、双盲清单 |
| 模拟审稿 | `/ars-reviewer` | 5 人安全面板 + 目标会议的准确判定词汇 |
| 收到审稿意见 | `/ars-revision-coach` | 按 venue+判定档定制的 Roadmap 与响应包结构 |
| 检查 rebuttal 草稿 | `/ars-rebuttal-audit` | 按 venue 硬规则审计（S&P 500 词等） |
| 延伸课题 / 提方法 / 评估 novelty / 设计并跑实验 / 改进方法 | 直接说明所处阶段（如「评估我的方法的 novelty」） | 研究闭环协议 S0–S8，改进循环硬上限 3 轮 + 人工检查点 |

**截稿日期铁律**：日期只从 `references/deadlines_current.md` 引用；超过 7 天
先运行 `python3 security-track/scripts/fetch_deadlines.py`（需网络 +
Python 3.10+ / pyyaml）；拉取失败时明确说明日历过期，绝不凭模型记忆报日期。

## 维护（fork 工作流）

```bash
git sync-upstream   # 拉 upstream → ff-only 更新 main → 推送 → 合并进 dev → 刷新截稿日历
```

- 定制永远走加法：新文件放本目录；不改上游文件（`marketplace.json` 的
  一行注册是唯一例外，冲突时保留双方条目即可）。
- `conference_ranking_2025.json`：排名源每年更新一次，届时重新快照。
- venue 档案钉的是结构性事实；页数限制、轮次数会漂移，临近投稿时以当年 CFP 为准。
