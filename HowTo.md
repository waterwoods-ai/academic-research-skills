# HowTo — 在 Claude Code 中使用(安全顶会研究全流程)

> 安装见 [`security-track/README.md`](security-track/README.md)。本文假设插件已装好
> (`/plugin install academic-research-skills@academic-research-skills`)、已开新 session。
> 全程默认:你的论文任务面向安全顶会(四大 + tier-2),security-track 覆盖层自动叠加。

## 核心习惯(先记这三条)

1. **涉及投稿/审稿的请求,永远写明目标会议**:`target venue: NDSS 2027`。
   判定词汇、Phase-0 检查项、页数预算都依赖它。
2. **截稿日期永远不要接受凭记忆的回答**——agent 被规定只从
   `security-track/references/deadlines_current.md` 引用,超 7 天会先刷新。
   如果它直接报了日期又没提日历,值得警惕。
3. **审稿第二轮起用 re-review + 冻结清单**,不要重新跑全量评审(防死循环,见下)。

## 日常场景速查

| 场景 | 输入 | 背后生效的机制 |
|---|---|---|
| 选会/投稿规划 | 直接问,或 `/ars-plan` | venue 档案 + 实时截稿日历 |
| 文献综述 | `/ars-lit-review <主题>`,加一句「确保覆盖全面」 | 6 透镜视角检索 + 未用检索追问 |
| 大纲 | `/ars-outline — target venue: ...` | 安全论文结构(Threat Model / Ethics 章) |
| 全文写作 | `/ars-full — target venue: ...` | numeric 引用、双盲写法、页数预算 |
| 模拟审稿 | `/ars-reviewer — target venue: ...` + 论文 | Phase-0 合规 → 安全合同盲态预提交 → 5 人安全面板 → 会议判定词汇 |
| 修改后复审 | `/ars-reviewer` re-review + **粘贴上轮判定原文** | 只判任务清单、禁止新异议、二元收敛 |
| 收到真实审稿意见 | `/ars-revision-coach` + decision letter | 按 venue+判定档的 Roadmap + 响应包结构 + 倒排时间表 |
| 检查 rebuttal 草稿 | `/ars-rebuttal-audit` + 意见 + 草稿 | venue 硬规则审计(S&P 500 词、禁未经要求新材料) |
| 摘要/引用检查/格式转换 | `/ars-abstract`、`/ars-citation-check`、`/ars-format-convert` | stock ARS + numeric 引用覆盖 |

## 完整研究闭环(S0–S8)

从零开始一个课题,或在任意阶段切入(协议:`security-track/references/research_loop_protocol.md`):

```text
S0  「验证这个课题是否可做:<主题>」            → go/no-go(饱和/错框/可行)
S1  /ars-lit-review <主题>,确保覆盖全面        → gap 登记(每个 gap 带检索证据)
S2  「基于这些 gap 延伸课题」                   → RQ 卡片(威胁模型草图+会议适配+可行性)
S3  「评估我的方法的 novelty 和 contribution」  → Contribution Card(search-bounded 判定)
    或「为 RQ-2 提出新方法」
S4  「为这个方法设计验证实验」                  → 按论文类型的反驳表 + 冻结成功标准
S5  「实现并运行实验」                          → 溯源台账(数字只来自执行日志)
S6  「结果不达标,改进方法」                    → 有界循环:每轮一个针对性修改,≤3 轮强制人工检查点
S7  /ars-reviewer(方法+台账包)                → 投稿前对抗压测
S8  /ars-full → Phase-0 → /ars-reviewer → 投稿  → 多轮评审生命周期按 playbook
```

Claude Code 独有优势:装了 **novelty-engine 插件**的话,S0–S4 自动用它的
8-agent 机制(topic_verifier / math_formalizer / experiment_falsifier 等),
security-track 在其上叠加安全校准。

## 审稿死循环的正确解法(重要)

第一轮 `/ars-reviewer` 拿到判定后,**保存输出**。此后每一轮:

```text
/ars-reviewer re-review — target venue: NDSS 2027
上轮判定与任务清单(原文):<粘贴>
修改说明:T1 → §4.2 增加 adaptive 实验;T2 → ...
修改稿:<全文或文件路径>
```

规则已由机制冻结:只对清单逐项判 RESOLVED/NOT、禁止对旧文本提新异议、
判定收敛即终止。如果它违规冒出新问题,引用规则让它重来。

## 首次使用的四点验证

跑一次 `/ars-reviewer — target venue: NDSS 2027` + 任一篇安全论文,确认:

1. 质量评审**之前**出现 Phase-0 合规表(P0-1~P0-7 PASS/FAIL)
2. 盲态预提交出现 `threat_model_soundness` 等安全维度名(出现 `methodology_rigor` = 合同没加载)
3. 面板 = PC Chair + CPS + IoT + Adversarial-ML + 威胁模型质疑者
4. 判定只用 NDSS 四档词汇(换 S&P 目标应只剩 Accept/Reject)

## 维护

```bash
git sync-upstream        # 同步上游 + 自动刷新截稿日历(在仓库目录内执行)
/plugin update academic-research-skills   # Claude Code 内更新插件
```

- 收到 GitHub Actions 失败邮件 = 上游 CI 在审我们的定制,按报错修即可
  (skill 元数据契约:SKILL.md 必须声明 `data_access_level` + `task_type`)
- 排名快照(`conference_ranking_2025.json`)每年随源更新一次
- 明确不是安全研究的任务,说一句即可回退 stock ARS 行为
