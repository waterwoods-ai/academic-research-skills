# HowTo — Claude Code 分步指南(从零到投稿)

> 安装见 [`security-track/README.md`](security-track/README.md)。本文假设插件已装好、已开新 session。
> 图例:🚦 = 人工决定门(agent 只提名,你拍板);📄 = 该步产出的存档物。
> 通用规则:涉及投稿/审稿的输入**永远写明 `target venue: <会议> <年份>`**;
> 截稿日期只认日历文件;已在某步有产出的信息不需要重复提供。
> **冷启动规则**:新会话从流程中段切入时(没有从 Step 1 开场),首条消息用
> 显式调用 `/academic-research-skills:security-track <request>`(或用任一 `/ars-*` 命令开场) 保证 skill 加载;
> 同一会话内的后续普通 prompt 自动继承。做过 Step 0.3 锚文件的项目目录可免。

---

## 阶段 0 · 一次性准备

**Step 0.1 确认安装**:新开 session,ask: `What is the NDSS Major Revision process?`。
agent 去读 `major_revision_playbook.md` 作答 = 正常;凭记忆直接答 = 覆盖层没生效,回 README 查安装。

**Step 0.2 首跑验证(建议)**:拿任一篇公开安全论文跑一次
`/ars-reviewer — target venue: NDSS 2027`,对照四点:①质量评审前出现 Phase-0
合规表;②预提交出现 `threat_model_soundness` 等维度名;③面板为 5 个安全
persona;④判定只用 NDSS 四档词汇。四点全过,体系可信,开始正式使用。

**Step 0.3 项目锚文件(强烈建议,一次一分钟)**:把 skill 自带的模板
`security-track/templates/project-anchor-CLAUDE.md` 复制到你的论文项目目录并改名
`CLAUDE.md`,填上 venue / 阶段 / 论文路径。此后该目录里的**每个新会话都确定性
加载 security-track**,与 prompt 措辞无关——这是三层保险里唯一 100% 的一层。

---

## 阶段 A · 选题(找课题 → 定课题 → 确认可做)

**Step 1 文献综述与 gap 登记**

```text
/ars-lit-review <your area, e.g. ICS sensor anomaly detection>, ensure broad coverage
```

- 📄 产出:文献综述 + gap 登记册——每个 gap 带三件套:失败的检索记录、
  最近似论文及其不足、该 gap 卡住的安全问题
- 你的动作:通读 gap 册,划掉不感兴趣的;没有检索证据的"gap"要求它补检索

**Step 2 课题延伸(RQ 生成)**

```text
Extend research topics from these gaps. My resources: <honestly list: testbeds / devices / dataset access you have>
```

- 📄 产出:RQ 卡片(威胁模型草图 + 贡献类型 + 目标会议适配 + 可行性),
  按 影响×可行性×新鲜度 排序
- 🚦 你的决定:选 1–2 个候选。资源栏 agent 替你答不了,如实填

**Step 3 课题可行性判定(go/no-go)**

```text
Verify the research topic viability (go/no-go): <selected RQ>
```

- 📄 产出:三选一判定 + 证据——SATURATED(点名占坑论文)/
  MISFRAMED(给出重述)/ VIABLE(点名空白地带)
- 🚦 你的决定:go / pivot / stop。这道门防止在饱和方向烧半年

**Step 4 找突破点(dogma 提取)**

```text
What unstated assumptions do prior works in this area share? Which one is most worth challenging?
```

- 📄 产出:共识假设清单(例:"防御者假设攻击者碰不到训练数据")
- 你的动作:选定要打破的那条——**打破被点名的 dogma 是最强 novelty 来源**

---

## 阶段 B · 方法(Propose 或深化评估)

**Step 5 提出方法 / 评估你的方法**

```text
Propose a new method for RQ-<n>                       ← from scratch
Evaluate the novelty and contribution of my method: <description>   ← bring your own method
```

- 📄 产出:**Contribution Card**——3–5 条可证伪 claim、每条的 novelty 判定
  (来自真实检索,判 KNOWN 当场丢弃)、与最近方法的逐维定位表、
  数学/算法形式化 + 威胁模型、诚实弱点清单
- 你的动作:确认形式化符合你的本意;INCREMENTAL 的 claim 要么给出定位论证要么砍

**Step 6 确定"有效"的检验标准**

agent 按论文类型自动选反驳标准(S4 反驳表,219 篇获奖论文校准):
防御类=扛住 adaptive attacker / 攻击类=真实目标端到端 / 测量类=排除假象 /
CPS=真测床+物理后果 / 工具类=真实软件胜最强基线 / 理论类=证明而非实验。

- 你的动作:确认这个 bar 对——它将同时是你的实验标准和将来审你的标准

---

## 阶段 C · 实验(设计 → 执行 → 改进)

**Step 7 设计实验(预注册 + 冻结)**

```text
Design validation experiments for this method
```

- 📄 产出:验证计划——每条 claim 的实验、指标、**数值化成功标准**、
  最强基线、消融、统计计划(种子/重复/检验)、artifact 计划
- 🚦 你的决定:**DESIGN FREEZE**。仔细审成功标准——批准后终身冻结,
  改进循环只许改方法、不许挪标准

**Step 8 执行实验**

```text
Implement and run the experiments
```

- 📄 产出:代码 + **溯源台账**(实验号→claim 号、计划 vs 实际、原始日志
  位置、MET/UNMET/INCONCLUSIVE)
- 你的动作:抽查日志与台账一致;记住铁律——论文里的数字只准来自台账,
  负结果记录在案不许删

**Step 9 改进循环(仅当有 UNMET)**

```text
The criterion for <claim-2> is unmet — improve the method
```

- 每轮机制:点名缺陷 → **一个**针对性修改(带机制假设)→ 只重跑受影响
  实验 + 回归检查 → 记入方法版本链(M-v2、M-v3…)
- 🚦 **3 轮硬上限**后强制检查点,三选一:再授权 3 轮 / pivot 回 Step 5 /
  接受负结果如实报告(台账里的负结果是可发表内容)

---

## 阶段 D · 论文与投稿

**Step 10 投稿前对抗压测**

```text
/ars-reviewer — target venue: <venue>, review target: method + experiment ledger (no paper yet)
```

- 目的:趁便宜暴露致命异议;发现的问题按 Step 9 的方式修一轮

**Step 11 写作**

```text
/ars-full — target venue: <venue>
Materials: Contribution Card + provenance ledger + outline (if any)
```

- 📄 产出:安全论文结构全文(Threat Model / Ethics 章、numeric 引用、
  双盲写法、页数预算)

**Step 12 首轮模拟评审(自动建档)**

```text
/ars-reviewer — target venue: <venue>, paper: ./paper.tex
```

- 📄 自动建 `ars-review/` 工作区:`round-1/decision.md`(判定+编号任务
  清单)、`compliance.md`(Phase-0 表)、稿件快照、`state.json`
- 你的动作:先看 Phase-0——有 FAIL 先修合规(桌拒救不回来),再看任务清单

**Step 13 修改与复审,直到收敛**

改论文,然后**零参数**:

```text
/ars-reviewer re-review
```

- venue/清单/路径全部从工作区读;修改映射由 agent diff 稿件快照自动生成,
  你一行确认(也可自己维护 `round-N/changelog.md`,存在则优先)
- 机制保证:只判清单、禁止对旧文本提新异议、判定收敛即终止。
  循环 Step 13 直到 CONVERGED

**Step 14 选轮次与投稿**

```text
Plan my submission to <venue>
```

- 截稿从日历读取(过期自动刷新);倒排时间表;投稿事务(注册冻结、
  篇数上限、逐人签署)查 venue 档案 Submission logistics 行
- 🚦 你的决定:投哪轮、是否赶得上

**Step 15 真实审稿意见到达**

```text
/ars-revision-coach — venue: <venue>, decision: <decision tier>
<paste the decision letter verbatim>
```

- 📄 产出:按 venue+判定档的 Revision Roadmap + 响应包结构(USENIX 四件套
  惯例)+ 按重投窗口倒排的时间表
- rebuttal 草稿写好后用 `/ars-rebuttal-audit` 过一遍 venue 硬规则
  (S&P 500 词、禁未经要求的新材料);多轮机制细节见
  `major_revision_playbook.md`(只有 NDSS 还有 Major Revision)

---

## 附:场景速查(不走全流程时单点使用)

| 需要 | 输入 |
|---|---|
| 只查截稿/选会 | 直接问(日历自动刷新) |
| 只出大纲 | `/ars-outline — target venue: ...` |
| 只出摘要 / 查引用 / 转格式 | `/ars-abstract`、`/ars-citation-check`、`/ars-format-convert` |
| 快速三问扫一篇论文 | `/ars-3w <paper>` |

## 附:维护

```bash
git sync-upstream                          # 同步上游 + 刷新截稿日历(仓库目录内)
/plugin update academic-research-skills    # 更新插件
```

CI 失败邮件 = 上游质量门在审我们的定制,按报错修(skill 元数据契约:
`data_access_level` + `task_type`)。排名快照每年随源更新。非安全研究任务
说一句即可回退 stock 行为。Claude Code 独有:装了 novelty-engine 插件时,
阶段 A/B 自动用它的 8-agent 机制,本覆盖层叠加安全校准。
