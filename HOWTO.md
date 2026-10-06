# HOWTO — 研究组协作分步指南:Codex(顾问 + Reviewer #2)× Claude Code(研究员 + 协调)× GLM(研究员 + 实验)

> 只想 5 分钟跑起来?看 [`QuickStart-security.md`](QuickStart-security.md)。本文件是完整参考。
>
> 想要**一步一步被带着走**(而不是照这 19 步自己推进)?说 `Be my security research mentor` 或 `一步一步指导我` —— 触发 `security_mentor_protocol`:有状态、一次一步、苏格拉底式,从选题带到投稿,进度存 `paper_progress.md` 可随时停/续。它和 `ars-plan`(一次性出整篇计划)相反。
>
> 从零到投稿的完整操作手册。每一步标明 **用哪个工具/agent**、**复制哪段 prompt**(全英文,可直接粘贴)、
> **产出什么文件**、**你要做什么决定**。本文件在两个 fork 中同源:本仓库(Claude Code 插件)与
> `academic-research-skills-codex`(Codex 插件)。安装细节见 `security-track/README.md`。
>
> **本平台角色**:Claude Code 是 🔬 **研究员 + 协调**:把 Codex 的研究计划拆成子计划(`subplans/`)并给各 agent 写任务简报;做文献(Step 1a/1b)、自己的想法(`ideas_claude.md`)、方法论核查、GLM 想法的检索查新、结果分析与 `claims.md`;写 `research_question.md`、`contribution_card.md` 和论文;把你的决定记进 `decisions.md`(见「谁做哪一步」)。
> 若你只有 Claude Code 一个工具,🧪 想法与实验步骤、🧭 计划与审稿步骤也可在 Claude Code 里跑(用同样的 prompt,
> 前缀改为对应 `/ars-*` 命令),但每次核查都换新会话,🧭 审稿步骤尽量换到不同模型家族以保持独立性。
>
> 图例:🧭 Codex(顾问 + Reviewer #2:计划、意见、审稿)  🔬 Claude Code(研究员 + 协调:文献、核查、分析、写作)  🧪 GLM(研究员 + 实验:想法、方法、全部实验)  🚦 你的决定门  📄 产出文件

---

## 为什么这样分工(三个 agent 的研究组,按 `orchestration.md`;角色 2026-10-06 由 Tom 重新分配)

| 角色 | 工具 | 问的问题 | 负责 | 只写这些文件 |
|---|---|---|---|---|
| PI | 你 | 我们到底要做出什么贡献? | 方向、安全范围、批准研究计划、设计冻结、每次算力启动、结论与 claim | — |
| 🧭 顾问 + Reviewer #2 | Codex(一个线程) | 完整的研究计划是什么?这道门我的专业意见是什么?这篇为什么该被拒? | 开题时写完整研究计划、定题后修订;每道门给专业意见;用检索到的文献攻击 novelty,审威胁模型、方法论、统计、评估和贡献;审稿轮;拒稿理由登记;逐句核对引用;投稿前终审。不写代码、不跑实验、不写论文正文 | `research_plan.md` `reviews/`(`advisor_opinions.md` `reject_reasons.md`)`ars-review/` |
| 🔬 研究员 + 协调 | Claude Code | 计划怎么拆成能做的子计划?方法站得住吗?新吗?结果说明了什么? | 子计划与任务简报;文献(选题侦察、系统综述、Elicit / Zotero API、检索子代理);自己的想法;方法论核查;检索查新(查 GLM 的想法,自己的由 Codex 查);结果分析与 claims 登记;研究问题、贡献卡和论文;记录你的决定 | `subplans/` `decisions.md` `research_question.md` `contribution_card.md` `claims.md` `ideas_claude.md` `verification/` `gap_registry.md` `literature.md` `literature/` `paper/` |
| 🧪 研究员 + 实验 | GLM(opencode) | 真正的攻防问题是什么?什么新方法能解决?它管用吗? | 想法;威胁模型与攻击面;提出新方法(novelty-engine);冻结前的实验计划;实现并在 gpu1 上跑全部实验(tmux、主机资源限制);运行台账、结果、方法变更记录、artifact | `rq_cards.md` `security/` `novelty_engine/` `candidate_cards.md`;冻结前的 `screening_plan.md` `validation_plan.md`;`method_changelog.md`、代码(`src/` `experiments/`)、`tests/`、`ledger/`、`results/`、artifact |

四条纪律:
- **任何关键结果都不只一个负责人**:每项都有主责和独立核查(见下表);谁都不核查自己的工作。Claude 核查 GLM 的威胁模型、方法、实验设计和实现;Codex 核查 Claude 的文献、分析、结果解释和论文;Claude 核查 Codex 的计划;GLM 给审稿做第二读,并核对相关工作里写的差异。
- **新颖性只认检索到的文献**:凭记忆说"没人做过"只算线索。Claude 和 GLM 各自在自己的文件里出想法,谁都不查自己想法的新颖性:Claude 查 GLM 的,Codex 查 Claude 的。
- **Codex 只计划和评审,不参与创造**:不出想法、不写代码、不跑实验、不写论文正文,所以能审别人的代码和结果。它只开一个线程(VS Code 只能开一个 Codex 窗口;Tom 2026-10-06 决定):审稿简报只列要审的文件,每条意见必须注明依据的文件和章节(新颖性意见还要附检索到的论文),没有出处的意见不算。投稿前终审(Step 17)也在同一个会话里做——它看过审稿轮,所以是最终检查、不是盲审,记录里写明。
- **方向文件只按你的决定改**:`research_plan.md`、`research_question.md`、`contribution_card.md`、`claims.md` 只在 Claude 把你的原话(日期、取代了什么)记进 `decisions.md` 之后,由该文件的写入者修改;其他 agent 只写自己的文件,意见写进报告。

所有交接都通过**磁盘文件**,零对话依赖。三个 agent 都装了 ARS / security-track skill。完整规则(核查矩阵、claims 登记、拒稿理由登记、Gate 1–4、拒绝时怎么分派):`security-track/references/lab_orchestration_protocol.md`。

### 谁做哪一步

| Step | 谁做 | 谁独立核查 |
|---|---|---|
| 0.5 总体研究计划(开题) | 🧭 Codex 写 `research_plan.md` | 🔬 Claude 核查,并把阶段 A 拆成子计划 `subplans/`;🚦 你批准 |
| 1a 选题侦察(只在没有题目时) | 🔬 Claude(`find-research-topic`,只能在 Claude Code 跑) | 在 1b 中核查 |
| 1b 系统综述 + gap 登记(接着 1a 的文件做) | 🔬 Claude(`ars-lit-review`) | 🧭 Codex(补漏文献,带检索证据) |
| 2 想法:RQ 卡片 + 威胁模型草图 | 🧪 GLM 写 `rq_cards.md`;🔬 Claude 独立写 `ideas_claude.md` | 在 Step 3 中核查 |
| 3 选题把关(Gate 1:>30 篇直接相关、最接近 5 篇、差异写清) | 🔬 Claude 检索查新 GLM 的卡片;🧭 Codex 查新 Claude 的想法 | 🧭 Codex:专业意见 + 用检索到的文献试图推翻 novelty;🚦 你选定 1 个问题 |
| 4 落定课题 | 🔬 Claude 按你的决定写 `research_question.md` | — |
| 4.5 修订研究计划 | 🧭 Codex 按选定的问题修订 `research_plan.md` | 🔬 Claude 核查,并写阶段 B–C 的子计划;🚦 你批准 |
| 5a 生成候选 | 🧪 GLM(novelty-engine);🔬 Claude 可在 `ideas_claude.md` 补候选 | 在 Step 6 中查新 |
| 5b 候选卡 + 筛选计划(DRAFT) | 🧪 GLM | 🔬 Claude(方法论) |
| 6 审候选与计划(Gate 2:威胁模型) | 🧭 Codex(Reviewer #2 + 专业意见) | 🔬 Claude 查新 GLM 的候选并核查威胁模型,🧭 Codex 查新 Claude 的候选;🚦 你选候选并冻结 |
| 7 修卡 | 🧪 GLM | 🔬 Claude |
| 7.5 筛选(gpu1) | 🧪 GLM 实现并运行;写 `method_changelog.md` | 🔬 Claude 先核查实现,再分析结果,按你的决定写 `contribution_card.md`;🚦 你确认方法 |
| 8 验证计划(DRAFT) | 🧪 GLM | 🔬 Claude(方法论) |
| 9 审设计 → 冻结 | 🧭 Codex(审查 + 专业意见) | 🚦 你冻结 |
| 10 实现与运行(gpu1) | 🧪 GLM | 🔬 Claude(运行前核查实现和 S5 运行前检查) |
| 11 改进(最多 3 轮) | 🧪 GLM | 🔬 Claude(方法变更溯源) |
| 12 检查点(Gate 3:实验有效性) | 🔬 Claude 分析结果、找根因 | 🧭 Codex 专业意见;🚦 你决定继续 / pivot / 报告 |
| 12.5 消融 | 🧪 GLM 运行 | 🔬 Claude 分析 |
| 13 写论文(先过 Gate 4:贡献) | 🔬 Claude | 🧭 Codex(Gate 4 意见;逐句核对引用) |
| 14、16 审稿 | 🧭 Codex(Reviewer #2) | 🧪 GLM(第二读) |
| 15 修改 | 🔬 Claude;实验项交 🧪 GLM | 🧭 Codex 复审文字项(Step 16);实验项由 🔬 Claude 核查 |
| 17 投稿前终审 | 🧭 Codex,同一个会话(看过审稿轮,不是盲审;记录里写明) | 🚦 你 |
| 17.2 审计 + artifact | 🧪 GLM | 🔬 Claude(干净检出重跑) |
| 17.5 复盘 | 🔬 Claude | 🚦 你(审提议的 knowledge_index 增补) |
| 18 投稿规划 | 🧭 Codex(顾问)起草;截稿只认 `deadlines_current.md` | 🔬 Claude 对照该文件核对日期;🚦 你选轮次 |
| 19 真实审稿 | 🔬 Claude(revision coach) | 🧭 Codex(对 rebuttal 给意见) |

- 每段 prompt 发给上表「谁做」那一列的 agent(步骤标题里也标了),文件名不变。各步的核查和意见用下面两段通用 prompt,把 `<…>` 换成该步的文件。
- **某个 agent 拒绝任务时,不要把同一请求原样转给另一个 agent。** 由 Claude 拆分:文献与解释 → Claude,威胁模型与攻击面 → GLM,防御实现 → GLM,分析与统计 → Claude,计划与评审 → Codex;潜在敏感的执行(如对目标的攻击执行)、或超出 `AUTHORIZED_RESEARCH.md`(模板在 `security-track/templates/`)的部分 → 停下,交你决定。Claude 把拒绝、分派和你的决定记进 `decisions.md`。
- 只有一两个工具时:角色可以合并,核查不能省——每次核查换新会话,只给产出物不给推理过程。

**通用核查 prompt**(🔬 Claude 核查别人的产出;每次换新会话,只给文件不给推理过程):

```text
Independent check — you did not produce these files: <files>. Check them as the row "<item>" of the independent-check matrix in lab_orchestration_protocol.md requires. Write ./verification/<step>-<item>.md: one finding per line with the file and section it rests on and a PASS / FIX verdict; any novelty finding cites the retrieved paper (title, authors, year, identifier). Do not edit the files under review.
```

**通用专业意见 prompt**(🧭 Codex,每道门):

```text
As my research advisor and Reviewer #2, give your professional opinion at <step / gate> on: <files>. Judge these files, not anyone's summary of them. Cite the file and section for every point, and a retrieved paper for every novelty objection — no citation, no objection. End with go / revise / stop and the deciding reason. Append it to ./reviews/advisor_opinions.md (date, step, files read) and add each reason to reject to ./reviews/reject_reasons.md. Do not edit the files under review.
```

---

## 阶段 0 · 一次性环境准备

**Step 0.1 各工具装好 skill**

- 🔬 Claude Code:`/plugin marketplace add waterwoods-ai/academic-research-skills` → `/plugin install academic-research-skills@academic-research-skills`
- 🧭 Codex(顾问 + Reviewer #2):`codex plugin marketplace add waterwoods-ai/academic-research-skills-codex --ref dev` → `codex plugin add ars-codex@ars-codex`
- 🧪 GLM(opencode):它从 `~/.claude/skills/` 发现 skill。把 fork 的 6 个 skill 目录 symlink 进去(5 个 ARS / security-track + 生成器 `novelty-engine`;另外 3 个选题 skill 需要浏览器,opencode 用不了,不必链接;**本机配置,不随仓库分发,换机器重做**):
  ```bash
  SRC=/path/to/academic-research-skills   # 你 clone 的 fork(dev 分支)
  cd ~/.claude/skills
  for s in academic-paper academic-paper-reviewer academic-pipeline deep-research security-track novelty-engine; do
    ln -sfn "$SRC/$s" "$s"; done
  ls -la ~/.claude/skills | grep -E 'academic|security|novelty'    # 6 个链接指向 live fork,无悬空
  ```

**Step 0.2 建项目目录 + 锚文件(各 agent 都读,确定性加载 skill;锚文件里有各角色只写哪些文件)**

```bash
mkdir my-paper && cd my-paper
cp $SRC/security-track/templates/project-anchor-CLAUDE.md ./CLAUDE.md   # Claude Code 读
cp $SRC/security-track/templates/project-anchor-AGENTS.md ./AGENTS.md   # Codex + opencode 读
```
编辑两个文件填三行:target venue、当前阶段、论文路径。以后**每个 agent 都在这个目录里启动**。

或者一条命令做完 Step 0.1 的链接检查 + Step 0.2(已有的锚文件不会被覆盖;默认建在 `~/Documents/research/` 下,用 `--dest` 改):
```bash
python3 $SRC/security-track/scripts/init_project.py --name my-paper --venue "<venue year, e.g. NDSS 2027>" --dest .
```

**Step 0.3 各工具冒烟测试**(每个工具问同一句,应去读 playbook 而非凭记忆答):

```text
What is the NDSS Major Revision process, and which Big-4 venues still have one?
```

正确答案要点:只有 NDSS 还有;S&P 2024 起 Accept/Reject;USENIX '26 取消;CCS 只有 Minor revision。三个工具都答对 = 环境就绪。

---

## 开题 · 总体研究计划(Step 0.5)

**Step 0.5 🧭 Codex 写总体研究计划(🔬 Claude 核查并拆子计划)** 🚦

🧭 Codex:

```text
As my research advisor, write ./research_plan.md. My area and resources: <area; testbeds / devices / datasets / time>. Cover: the problem area and why it matters for security; 2–4 candidate research questions; the phases (A topic, B method, C experiments, D paper, E submission), each with milestones and one testable success criterion; the compute budget on gpu1; the main risks and the fallback for each; target venue options with deadlines taken only from deadlines_current.md. Write no code and no paper text. Stop for my approval.
```

🔬 Claude 核查计划 + 拆阶段 A 子计划:

```text
Check ./research_plan.md as the row "Full research plan" of the independent-check matrix in lab_orchestration_protocol.md requires (feasibility against my resources and the gpu1 budget; a testable success criterion per phase) and write the findings to ./verification/0.5-research_plan.md. Then break Phase A into sub-plans in ./subplans/: one file per task naming the agent, input files, output file, stop point and success criterion; cover every Phase A item and add nothing the plan does not ask for.
```
📄 `research_plan.md`、`verification/0.5-research_plan.md`、`subplans/`(阶段 A)。🚦 **你批准**计划:Claude 把你的原话记进 `decisions.md`;以后改计划也先记决定。子计划是否完整覆盖计划,由 Codex 核对(核查矩阵 "Sub-plans")。

---

## 阶段 A · 选题(Step 1–4.5)

> **从零开始,先看你手里有什么:**
>
> | 你现在有 | 从哪里进 |
> |---|---|
> | 只有一个大方向,没有题目 | Step 1a(Claude Code:`find-research-topic <大方向>`)拿 3–7 个候选题目,选一个再做 1b;1a 写下的论文和 LEAD gap 就是 1b 的起点 |
> | 有具体方向,没有论文 | 直接 Step 1b——ARS 自己检索,不需要你提供文献 |
> | 有方向 + 自己攒的论文(Zotero / PDF 文件夹) | Step 1b,在 prompt 里写明论文位置;它们就是起始语料,ARS 先筛你的,再补检索没覆盖的部分 |
> | 有一篇想在其上改进的基线论文 | Step 1–4 照常定题;到 Step 5 先跑 `novelty-filter <论文>` 建 limitation 列表(5a 的方式 B 从它出发) |
> | 已经有自己的方法 | 跳到 Step 5 的 `Evaluate…` 分支 |

**Step 1 🔬 Claude 文献阶段:1a 侦察(可选)→ 1b 系统综述 + gap 登记(🧭 Codex 补漏)**

1a 和 1b 是同一个阶段,共用一份论文清单 `literature.md` 和一份 `gap_registry.md`:1a 管「广」(只有大方向时找候选题目),1b 管「深」(题目定了以后系统检索、核验引用、把 gap 补齐)。1b 不重做 1a 已经做过的检索。

**1a 侦察(只在没有题目时;仅 Claude Code)**

```text
find-research-topic <broad area>. Besides the report, write the stage files: save every kept paper to ./literature.md and save every candidate's gap to ./gap_registry.md as a LEAD entry (signals, evidence papers, the queries and dates that found it).
```
📄 `runs/<日期>-<slug>/report.md`(3–7 个排序的候选题目)、`literature.md`、`gap_registry.md`(LEAD 条目)。🚦 你选一个候选,1b 在它上面做深。

**1b 系统综述 + gap 登记(所有工具)**

```text
ars-lit-review <the chosen topic, or your area>, ensure broad coverage.
Corpus first: treat the papers already in ./literature.md (and the Zotero collection <name>, if I name one) as the pre-screened corpus. Screen them with the same inclusion criteria first and record which came from there, then search only for what they do not cover. Do not repeat queries already recorded in ./runs/*/ledger.md. Run the ancestor query (no year filter, no buzzwords) and the adjacent-method-family query.
Write the gap registry to ./gap_registry.md: complete every LEAD entry to the full form or drop it with the reason. Each gap must carry: the search that failed to fill it (queries, indexes, date), the nearest-miss papers and why each falls short, and the security question the gap blocks.
Save every included paper to the same ./literature.md (citation, one-line finding, which gap it bears on); do not start a second list — later steps read it.
```
📄 `gap_registry.md`(全部是完整条目,没有 LEAD)、`literature.md`。你的动作:划掉不感兴趣的;没检索证据的 gap 让它补检索。
🧭 Codex 补漏:通用专业意见 prompt,`<step / gate>` = Step 1b,`<files>` = `literature.md` `gap_registry.md`,重点找漏掉的论文(每篇附检索证据)。

> **说明(见 `topic_scouting_overlay.md`)**:1a 的 `open / narrow / saturated` 只是扫描级线索,不是 novelty 结论;LEAD 条目要在 1b 补齐三项才算 gap。题目已定、要系统化的 gap 证据也可以加跑 `research-gaps`(Elicit API,结果归档到 Zotero),它的结果同样写进这两个文件。Codex / opencode 没有浏览器:跳过 1a,直接 1b。

> 顺带:agent 按你的子领域从 `knowledge_index.md` 加载该领域的审稿门槛(adaptive-eval / 测床+物理后果 / OTA 对标 in-toto/SLSA 等),S1–S3/S7 全程套用。

**Step 2 🧪 GLM 课题延伸(RQ 卡片 + 威胁模型草图)+ 🔬 Claude 独立出想法**

🧪 GLM:

```text
Extend research topics from ./gap_registry.md. My resources: <honestly list: testbeds / devices / dataset access you have>.
Write ranked RQ cards to ./rq_cards.md — each with a threat-model sketch, contribution type (attack / defense / measurement / tool; note CCS rejects SoK), target-venue fit, feasibility against my resources, and the supported assumption, confirmed limitation or located observation it builds on (no dogma is required). Compare security impact, feasibility and the prior-work delta separately; do not use an aggregate score as evidence.
```

🔬 Claude(独立做,不看 GLM 的卡片):

```text
Without reading ./rq_cards.md, write your own research ideas from ./gap_registry.md and ./literature.md to ./ideas_claude.md, as cards in the same format: threat-model sketch, contribution type, target-venue fit, feasibility against my resources (<same list>), and the assumption, limitation or observation each builds on. Do not judge their novelty yourself — Codex verifies it in Step 3.
```
📄 `rq_cards.md`、`ideas_claude.md`

**Step 3 🔬 Claude 查新 + 🧭 Codex 把关选题(go / no-go;Gate 1)** 🚦

🔬 Claude 查新 GLM 的卡片:

```text
Novelty check of GLM's ./rq_cards.md against ./gap_registry.md for a Big-4 security venue.
For each of the top-3 RQs: retrieve the 5–10 most-cited and most-recent Big-4/tier-2 papers and rule SATURATED (name the papers) / MISFRAMED (restate the better question) / VIABLE (name the open territory). Then identify any source-backed assumption worth challenging, or the confirmed limitation/located observation motivating the RQ. Zero supported assumptions is valid; distinguish explicit assumptions, shared dependencies and unverified hypotheses. Then run the topic verification gate (topic_verification_gate.md) on the top RQ: answer the 12 questions with evidence and a pass / weak / fail status each, freeze them, and give a go / revise / stop verdict with the deciding question. Write your verdicts to ./verification/3-rq_novelty.md; do not edit GLM's cards.
```

🧭 Codex 查新 Claude 的想法 + 给专业意见:

```text
As my research advisor and Reviewer #2 (Gate 1): read ./rq_cards.md, ./ideas_claude.md, ./gap_registry.md and ./verification/3-rq_novelty.md. Try to invalidate the novelty of the top RQs with retrieved papers — no citation, no objection. Verify the novelty of each idea in ./ideas_claude.md by your own retrieval (NOVEL-WITHIN-SEARCH / INCREMENTAL / KNOWN, nearest prior work cited). Then give your professional opinion: which question to pursue, go / revise / stop, and the deciding reason. Append it to ./reviews/advisor_opinions.md; do not edit the files under review.
```
🚦 **你决定**:选定 1 个 RQ(来自 `rq_cards.md` 或 `ideas_claude.md`),go / pivot / stop。这道门防止在饱和方向烧半年。还想要一个盲评:Claude Code 里的 `verify-research-topic` 走 ChatGPT 盲评,只看设计事实、不看你的答案,再按证据逐条对账。

**Step 4 🔬 Claude 落定课题(按你的决定)**

```text
Record my decision in ./decisions.md (my words, the date, what it supersedes). Then finalize RQ-<n> per ./verification/3-rq_novelty.md and ./reviews/advisor_opinions.md. Write ./research_question.md: the RQ, threat model, the supported assumption or limitation/observation IDs (with evidence status), target venue, why it fits that venue, and the topic-gate verdict with its date (copied from ./verification/3-rq_novelty.md).
```
📄 `decisions.md`、`research_question.md`

**Step 4.5 🧭 Codex 按选定的问题修订研究计划(🔬 Claude 核查并写阶段 B–C 子计划)** 🚦

🧭 Codex:

```text
As my research advisor, revise ./research_plan.md for the research question now fixed in ./research_question.md (my decision is in ./decisions.md): phases B (method), C (experiments), D (paper) and E (submission) with milestones and one testable success criterion each, the gpu1 compute budget, the risks, and the target venue with its deadline from deadlines_current.md. Mark what changed from the previous version. Stop for my approval.
```

🔬 Claude:

```text
Check the revised ./research_plan.md as in Step 0.5 and write the findings to ./verification/4.5-research_plan.md. Then write the sub-plans for Phases B–C in ./subplans/, one file per task as in Step 0.5.
```
📄 `research_plan.md`(修订版)、`subplans/`(阶段 B–C)。🚦 **你批准**(Claude 记进 `decisions.md`)。

---

## 阶段 B · 方法与 novelty(Step 5–7.5)

**Step 5 🧪 提出方法 / 深化你的方法 → 候选卡**

从零提方法的顺序:**5a 生成**(三条证据驱动路线 + 统一检查,最多留 3 个不同机制的候选)→ **5b 候选卡 + 筛选计划**(Claude 核方法论)→ Step 6 Claude 查新 + Codex(Reviewer #2)审 → Step 7 修卡 → **Step 7.5 便宜实验筛选,选定 1 个** → Contribution Card。
已经有自己的方法:跳过 5a 和 7.5,在 5b 用 `Evaluate…` 那段让 🔬 Claude 直接写 `contribution_card.md`。

实证/测量/SoK 型贡献如果不需要新方法,按 `research_loop_protocol.md` S3 的 contribution-type 分支写 Contribution Card,用可复现的测量/分析协议和证据义务替代方法形式化;不强造算法或基线提升目标,直接进入对应 S4 验证路线。

**5a 🧪 GLM 运行生成器 `novelty-engine`**(三个工具都能用;🔬 Claude 可另在 `ideas_claude.md` 补候选,它们的新颖性在 Step 6 由 Codex 查)

```text
Run novelty-engine candidate generation for the RQ in ./research_question.md. Inputs (direct route): the papers in ./literature.md, the gaps in ./gap_registry.md, and — when available — a confirmed limitation list (./runs/*/weaknesses.md from novelty-filter, or ./limitation_ledger.md), and located logs/measurements/deployment evidence or ./observation_ledger.md. The topic-gate verdict recorded in ./research_question.md stands in for Phase 0; do not re-run it.
Read novelty-engine/references/evidence_driven_ideation.md. Use each route whose evidence exists, and record why any route is skipped.
Mode A, assumption-breaking: Phase 1 — extract source-backed assumptions and breaking points with EXPLICIT / SHARED-DEPENDENCY / HYPOTHESIS labels. Zero supported assumptions is valid; hypotheses stay in a probe queue. Stop for my choice of supported premises. Phase 2 — pre-check the breaking points. Phase 3A — propose distinct methods using structurally suitable mechanisms from adjacent or distant fields; distance is not a quality gate. State transfer assumptions and adaptation costs.
Mode B, limitation-driven: Phase 3B — propose up to three supported, distinct mechanisms (zero is valid with a probe/evidence-gap note) that remove the causes of the confirmed limitations of the strongest baseline. One mechanism may resolve several limitations; do not produce one patch per limitation. If there is no confirmed limitation list, build one from the strongest baseline paper first and show it to me.
Mode C, observation-driven: Phase 3C — record observation provenance/status, proposed causes, plausible alternatives and discriminating probes in ./novelty_engine/03_hybrid_methods/observation_ledger.md. Generate a method only when the evidence supports a concrete mechanism hypothesis. Missing artifacts yield a probe plan, not invented findings; a new RQ/threat model returns to Step 2.
Phase 3.5, every candidate from applicable routes: write its candidate card (origin IDs, evidence status, cause and rival explanation, mechanism, borrowed components, new assumptions/costs, own claims, security consequence, nearest prior work, decisive test and pass/drop criteria). Re-check the mechanism and knowledge delta using ancestor and adjacent-method queries; run security framing and feasibility checks. UNCERTAIN retrieval stays pending. Merge equivalent mechanisms, preserve provenance, and shortlist at most three eligible candidates without route quotas. Stop for my choice of shortlist. Track proposed/eligible/tested IDs and decisions in candidates.md; unrun tests are NOT RUN, and LLM scores are not execution evidence.
Phase 4: formalize each shortlisted candidate far enough to implement its decisive test (definitions, assumptions, algorithm + complexity). Keep all outputs in ./novelty_engine/; write candidates.md here, but do not write the root-level candidate_cards.md or contribution_card.md yet.
```
📄 `novelty_engine/03_hybrid_methods/candidates.md`(候选卡 + shortlist + 被淘汰的及原因)、`hybrid_methods.md`、`limitation_driven_methods.md`、`observation_ledger.md`、`observation_driven_methods.md`(只输出有依据的路线)、`02_novelty_check/novelty_verification.md`、`04_formal_spec/formal_specification.md`。Claude Code 里各角色作为独立子代理运行;Codex / opencode 逐个角色顺序执行。

> 可选(仅 Claude Code):`novelty-filter <基线论文>`(原名 develop-novel-method)——只过滤、不生成。**5a 之前跑**:它的 `runs/<日期>-method-<slug>/weaknesses.md` 就是方式 B 要的 limitation 列表。**5a 之后跑**:对 `candidates.md` 里的候选做一遍更强的查新(Elicit + Litmaps + 两个盲评模型),结论写回候选卡。

**5b 🧪 GLM 候选卡 + 筛选计划(🔬 Claude 核方法论)**

```text
From ./novelty_engine/03_hybrid_methods/candidates.md and ./novelty_engine/04_formal_spec/formal_specification.md, write ./candidate_cards.md: one card per shortlisted candidate (at most three). Each card carries its origin IDs/evidence status, cause and rival explanation, new assumptions/costs and borrowed components; its OWN 1–3 falsifiable claims; the novelty verdict per claim (NOVEL-WITHIN-SEARCH / INCREMENTAL / KNOWN from real retrieval against Big-4 + tier-2 literature, nearest prior work cited); the security consequence; the formalization (algorithm + complexity) plus the threat model; honest weaknesses; and its cheapest decisive test with a numeric pass criterion.
Then write ./screening_plan.md, marked DRAFT and shared by all candidates: the development data (it can never become the held-out), the strongest baseline to reproduce, the ONE comparison criterion used to choose between candidates, and the implementation and tuning budget per candidate (the same for all).
```
📄 `candidate_cards.md`、`screening_plan.md (DRAFT)`。规则:判 KNOWN 的候选当场丢弃,不为了"代表某种生成方式"而保留。
🔬 Claude 核方法论:通用核查 prompt,`<files>` = `candidate_cards.md` `screening_plan.md`,`<item>` = "Method and formalization" 和 "Experiment design"(两行各写一份)。

自带方法时改用这一段,交给 🔬 Claude(`contribution_card.md` 是它的文件;不写候选卡,不筛选):

```text
Evaluate the novelty and contribution of my method: <description>
Write ./contribution_card.md with: 3–5 falsifiable claims; per-claim novelty verdict NOVEL-WITHIN-SEARCH / INCREMENTAL / KNOWN from real retrieval against Big-4 + tier-2 literature with the nearest prior work cited; a positioning table vs the 3–5 closest methods; a one-paragraph delta statement in the community's own terms; formalization (math or algorithm + complexity) plus the threat model; honest weaknesses; and a security framing check (framing chain + SECURITY FRAMING RISK verdict + each claim's novelty type) per security_framing_protocol.md.
```
📄 `contribution_card.md`。规则:判 KNOWN 的 claim 当场丢弃;INCREMENTAL 需给出定位论证。

> **精读单篇论文(单篇,非综述)** — 用关键词 `peruse` 触发:
> ```text
> Peruse this paper: <path or title> — full single-paper dissection per paper_dissection_protocol.md
> ```
> 产出该篇的 8 问骨架、论证链与最弱环、Introduction P1–P7 标注、以及它的 evaluation 会招来哪些审稿人问题。
> (需要多篇检索/覆盖面用 `ars-lit-review` + 「确保覆盖全面」;`ars-3w` 是轻量筛选。)

**Step 6 🧭 Codex 审候选与筛选计划(🔬 Claude 先查新;Gate 2)** 🚦

🔬 Claude 先做:通用核查 prompt,`<files>` = `candidate_cards.md`(自带方法时 `contribution_card.md`),`<item>` = "Novelty of GLM's ideas and candidates"(每条 claim 的新颖性判定用真实检索重新核验)和 "Threat model"(Gate 2)。

🧭 Codex(Reviewer #2 + 专业意见):

```text
As Reviewer #2 and my research advisor, review ./candidate_cards.md and ./screening_plan.md, with Claude's checks in ./verification/ (if I brought my own method, review ./contribution_card.md the same way instead). For each candidate: try to invalidate each novelty verdict with a retrieved paper (do not trust the earlier searches); verify the novelty of any candidate Claude added in ./ideas_claude.md by your own retrieval. Which claim would a Big-4 reviewer kill first, and with which of the standard rejection anchors? Is the security consequence real, or only a better number? Is the formalization actually a method (algorithm + threat model) or still a sketch? Is the decisive test really decisive, with a numeric pass criterion? For the screening plan: is it fair to every candidate (same data, same baseline, same budgets), and is the development data disjoint from anything that could later serve as the held-out? Write your review and professional opinion to ./reviews/advisor_opinions.md and each reason to reject to ./reviews/reject_reasons.md; do not edit the files under review.
```
🚦 **你决定**:哪些候选进筛选(可以砍到 1–2 个),或退回 Step 5。批准后把 `screening_plan.md` 文件头改为 `FROZEN <date>`——之后不再改数据、判据和预算。

**Step 7 🧪 GLM 按审查意见修卡(🔬 Claude 核查)**

```text
Revise ./candidate_cards.md per the Step 6 reviews in ./verification/ and ./reviews/advisor_opinions.md.
```
🔬 Claude 用通用核查 prompt 复核修改过的候选卡。自带方法时:🔬 Claude 按同样的审查意见修 `contribution_card.md`(顶部标 M-v1 版本号),🧪 GLM 写 `method_changelog.md` 的 M-v1 条目,跳过 Step 7.5。

**Step 7.5 🧪 GLM 便宜实验筛选(gpu1)→ 🔬 Claude 分析 → 选定 1 个方法** 🚦

🧪 GLM:

```text
Run the candidate screening in ./screening_plan.md (FROZEN) on gpu1. First reproduce the strongest baseline on the development data and log it in ./ledger/. Then, for each candidate in ./candidate_cards.md, implement it only as far as its cheapest decisive test needs, within the frozen budget, and stop for Claude's implementation check before the first candidate run. Then run each test on the development data — never on held-out data. Log one ledger entry per run: candidate id, planned vs executed, raw log path, and the verdict against the candidate's own pass criterion (GOOD / ENGINEER / BAD; a BAD candidate gets a root-cause note). Do not change the plan or any pass criterion after seeing results. Stop when every run is logged.
After I confirm the selected candidate: complete its formalization (the theorem or bound its claims need) in ./novelty_engine/04_formal_spec/formal_specification.md; write ./method_changelog.md with the M-v1 entry; and mark the runners-up in ./candidate_cards.md as reserve, with their screening results. Update the evidence summary in ./novelty_engine/03_hybrid_methods/candidates.md with tested IDs, ledger links, MET/UNMET/INCONCLUSIVE results and the selected ID; keep unrun tests as NOT RUN. Investigate failure causes and feed them back into generation.
```
🔬 Claude 在第一个候选运行前核查实现:通用核查 prompt,`<files>` = 代码 + `candidate_cards.md` `screening_plan.md`,`<item>` = "Implementation"。

🔬 Claude 分析并推荐:

```text
Analyse the screening in ./ledger/ against ./screening_plan.md (FROZEN): recompute each verdict from the raw logs, then recommend ONE candidate by the frozen comparison criterion (on a tie, the simpler one or the one with weaker assumptions) and stop for my confirmation. Do not infer publication readiness from a model score.
After I confirm and GLM has completed the formalization: record my decision in ./decisions.md, then write ./contribution_card.md for the selected method with the eight Contribution Card items of research_loop_protocol.md §S3, tagged M-v1, taking the formalization from ./novelty_engine/04_formal_spec/formal_specification.md and checking it as the "Method and formalization" row of the independent-check matrix requires.
```
📄 `ledger/`(筛选记录)、`contribution_card.md`(M-v1,Claude 写)、`method_changelog.md`(GLM 写)。🚦 **你决定**:确认选哪一个。全部 BAD 时不降标准:带着失败原因回 5a,或请 Claude 分析根因、Codex 给意见。落选的候选留作后备,论文里可如实报告筛了几个、为什么选这个。

---

## 阶段 C · 实验:设计 → 冻结 → 执行 → 改进(Step 8–12)

**Step 8 🧪 GLM 起草验证计划(按论文类型的反驳表;🔬 Claude 核方法论)**

```text
Design validation experiments for the method in ./contribution_card.md. First classify the paper type (attack / defense / measurement / tool / CPS / IoT / ML-for-security / theory) and pick the matching row of the S4 refutation table in research_loop_protocol.md. Write ./validation_plan.md: per claim — the experiment or proof obligation, metrics, NUMERIC success criteria, strongest published baselines correctly tuned, ablations, statistical plan (seeds, repetitions, tests), and the artifact / open-science plan. Apply the evaluation-integrity rules (research_integrity_protocol.md §2): plan to report ALL testbeds/datasets/devices with regressions disclosed (no cherry-picking), fix a held-out split that method development never touches (it must be disjoint from the development data in ./screening_plan.md), and set a utility non-regression bound. Mark the file DRAFT.
```
📄 `validation_plan.md (DRAFT)`
🔬 Claude 核方法论:通用核查 prompt,`<files>` = `validation_plan.md`,`<item>` = "Experiment design"(可行性、统计、对每个基线和候选公平、held-out 不相交)。

**Step 9 🧭 Codex 审设计并给专业意见 → 冻结** 🚦

```text
Review ./validation_plan.md as Reviewer #2 and my research advisor, with Claude's methodology check in ./verification/. Check: does each claim's validation survive the specific refutation a Big-4 reviewer of THIS paper type will attempt (adaptive adversary for defenses; real target end-to-end for attacks; artifact-ruling-out for measurement; real testbed + physical consequence for CPS; device diversity for IoT; base rates + temporal split for ML detection; proof for theory)? Are the success criteria numeric and pre-registered? Are the baselines the strongest published ones? Write your review and professional opinion to ./reviews/advisor_opinions.md. Do not change the criteria yourself — propose, and I decide.
```
🚦 **DESIGN FREEZE**:你批准后把文件头改为 `FROZEN <date>`。**此后成功标准终身不动;改进循环只许改方法。** 冻结的 `validation_plan.md` 就是这次实验的**预注册卡**(research_integrity_protocol.md §1):此后每个上报的数字都要能追溯到它;出结果后再动判据是 HARKing——只能走有记录的、人把关的 RE-FREEZE,不能悄悄改。

**Step 10 🧪 GLM 实现并运行(gpu1,tmux + 主机资源限制;GLM 是台账和复现清单的唯一写入者;🔬 Claude 先核查实现)**

```text
Implement and run the experiments in ./validation_plan.md (FROZEN) on gpu1. Implement first and stop for Claude's implementation check (the S5 pre-run checks) before any run. Then re-run the strongest baseline in this environment and log it in ./ledger/ — every gain is measured against that reproduced number, never a paper-reported one. Screen candidate changes on a development subset (never the held-out split) before full runs. Maintain ./ledger/ as the provenance ledger: one entry per run with experiment id → claim id, planned vs executed (name every deviation), raw log path, verdict against the pre-registered criterion (MET / UNMET / INCONCLUSIVE), and any negative or surprising result. Numbers in any later document may come only from this ledger.
```
🔬 Claude 运行前核查:通用核查 prompt,`<files>` = 代码(`src/` `experiments/` `tests/`)+ `validation_plan.md` `contribution_card.md` `security/`,`<item>` = "Implementation"(对照方法和威胁模型读代码;S5 运行前检查)。
📄 `ledger/`。你的动作:抽查日志与台账一致。

**Step 11 🧪 GLM 改进循环(仅当有 UNMET;🔬 Claude 核查变更溯源)**

```text
The criterion for <claim-k> is UNMET per ./ledger. Improve the method: name the deficiency with ledger evidence; make ONE targeted change with a mechanism hypothesis ("criterion X fails because Y; change Z addresses Y"); re-run only the affected experiments plus a regression check on previously-MET criteria; log M-v<N+1> in ./method_changelog.md (Claude then updates the method description and version tag in ./contribution_card.md to match — the card always describes the current method). The success criteria in ./validation_plan.md are frozen — do not touch them. IF the change introduces a new MECHANISM (not tuning) — especially a substitute to rescue a failing result — it MUST first pass method_change_provenance.md: (1) scenario fidelity (does it still solve the ORIGINAL problem, or silently redefine it?); (2) prior-art identity (strip any new name and search — a renamed known method, e.g. a "new" OTA signing scheme = in-toto/SLSA/TUF/Uptane, is a RENAME not a contribution); (3) honest outcome: ADOPT+CITE with the novelty claim dropped, or a proven genuine delta re-verified NOVEL-WITHIN-SEARCH. Record the verdict (RENAME / GENUINE-DELTA / ADOPT-AND-CITE) in the changelog.
```
🔬 Claude 核查每次改动:通用核查 prompt,`<files>` = `method_changelog.md` 的新条目 + 改动的代码,`<item>` = "Method and formalization",并对照 `method_change_provenance.md` 复核三项检查和 RENAME / GENUINE-DELTA / ADOPT-AND-CITE 判定;通过后更新 `contribution_card.md` 的方法描述和版本号。
🚦 **3 轮硬上限**后停下,进 Step 12。

**Step 12 🔬 Claude 检查点分析(每 3 轮改进后,或改进达标后;Gate 3;🧭 Codex 给意见)** 🚦

```text
Checkpoint analysis. Read ./validation_plan.md (FROZEN), ./ledger/, ./method_changelog.md. Is the method converging on the frozen criteria, or are we chasing? First diagnose the ROOT CAUSE of any unmet criterion from ./ledger/ (bug? mis-tuned baseline? wrong assumption? mechanism gap?) — a negative result is a lead to investigate, not a stopping point. Then recommend exactly one of: authorize 3 more iterations (pursue the root cause and improve) / pivot back to method design (replace an unpromising approach, keep the problem) / report what works and what does not — but ONLY once the root cause is understood and a fix is either found or proven out of reach, never as a "just honestly report the negative" shortcut (integrity holds: numbers from ./ledger, criteria frozen, no cherry-picking). Then stress-test the method + ledger package as if you were the panel: what is the fatal objection, if any, before we spend effort writing the paper? Write the analysis to ./verification/12-checkpoint.md and update the evidence and status lines in ./claims.md.
```
🧭 Codex 给意见:通用专业意见 prompt,`<step / gate>` = Step 12 / Gate 3,`<files>` = `validation_plan.md` `ledger/` `method_changelog.md` `verification/12-checkpoint.md` `claims.md`(统计从 ledger 原始输出重算;每条 claim 对照证据挑战)。
🚦 **你决定**:继续 / pivot / 如实报告。

**Step 12.5 🧪 GLM 消融与简化(所有判据达标后必做——即使第一次就达标、没进过改进循环;🔬 Claude 分析)**

```text
All frozen criteria in ./validation_plan.md are MET per ./ledger. Run S6a from research_loop_protocol.md: (1) run the pre-registered ablations, one component at a time, and log each in ./ledger/; (2) if a component does not contribute, propose the simplified method — it replaces the current one ONLY if strictly better (or equal and simpler) on development data under the pre-registered metric, otherwise keep the current method; (3) if the method was replaced, re-run the ablations on the new method and update ./method_changelog.md to the new version (Claude updates ./contribution_card.md). Do not touch the held-out split. If more than one candidate was GOOD, confirm which one was selected on development data and why (ledger entry). End with the source-of-gain table.
```
📄 `ledger/` 里的消融记录 + source-of-gain 表。这是论文消融表的唯一来源。
🔬 Claude 分析:从 `ledger/` 原始输出重算消融结果和 source-of-gain 表,写进 `claims.md`;方法若被替换,更新 `contribution_card.md`。

---

## 阶段 D · 论文与评审循环(Step 13–17)

**Step 13 🔬 Claude 写论文(先过 Gate 4;🧭 Codex 核对引用)**

写之前先过 Gate 4:🧭 Codex 用通用专业意见 prompt,`<step / gate>` = Gate 4,`<files>` = `contribution_card.md` `claims.md`(安全社区为什么在乎?之前不知道什么?贡献属于哪一类?Reviewer #2 先打哪里?)。答不出令人信服的答案就不开写。

```text
ars-full — target venue: <venue year>
Materials: ./contribution_card.md (claims spine, current method version), ./method_changelog.md (what changed and why), ./ledger/ (all numbers), ./validation_plan.md, ./research_question.md, ./literature.md and ./gap_registry.md (related work).
Security-paper structure (Intro / Threat Model / Design / Implementation / Evaluation / Discussion / Related Work / Ethics Considerations), numeric citations, double-blind, within the venue page budget. Every number must trace to a ledger entry. Output ./paper.tex.
```
📄 `paper.tex`。🧭 Codex 随后逐句核对引用(SUPPORTED / PARTIALLY SUPPORTED / UNSUPPORTED),结果写进 `reviews/`。

> 可选润色:草稿成形后跑一遍 **`academic-humanizer`**(security 校准见 `security_humanizing_overlay.md`)——去 AI 味、把动词强度对齐证据,**只降不升(never inflate)**,绝不动数字 / 引用 / CVE-ATT&CK id / scope hedge。这是**内容冻结后**的语言润色,不是改内容;会议论文跳过 Layer 6(NSF/NIH grant 模式)。

**Step 14 🧭 Codex(Reviewer #2)首轮评审(自动建档;🧪 GLM 对同一稿第二读,列出分歧)**

```text
ars-reviewer — target venue: <venue year>, paper: ./paper.tex
```
📄 `ars-review/round-1/`:`decision.md`(判定 + 编号任务清单)、`compliance.md`(Phase-0 表)、稿件快照、`state.json`。
你的动作:**先看 Phase-0**——有 FAIL 先修合规(桌拒救不回来);再看任务清单。核对一眼 `round-1/` 里的实际文件名(agent 未必严格照约定命名)。

**Step 15 🔬 Claude 按清单修改 + 写 changelog**(实验项交 🧪 GLM,由 🔬 Claude 核查;通用版:不必先自己读 round-N 的文件)

```text
A reviewer round has just been written to ./ars-review/. Find the latest round-N/ directory and read everything in it (the decision/review file, any verdict or traceability record, the compliance check).

Phase 1 — report, no edits: (a) the overall decision and how many tasks are resolved / partially / not resolved / newly raised; (b) every open item with its ID, one-line residual gap, and the evidence class needed to close it (text change / experiment run recorded in ./ledger/ / code or artifact / formalization); (c) group open items into A = compliance or desk-reject risks, B = text-only fixes, C = anything needing an experiment or artifact, D = idea-level (the method itself is judged weak — not its write-up, not its evidence).

Phase 2 — execute A then B only, text-only, touching nothing outside those items and never editing the reviewer's files. Recompile and report the exact page count.

Phase 3 — STOP: for each cluster-C item say in one line whether it is load-bearing for the target venue's contribution or removable by honest re-scoping; for each cluster-D item state the root cause in one line and the one targeted method change you would try. Never patch a D item in prose. Then wait for my decision on which to run, which to re-scope, and which D items go back to the method.

Throughout: maintain ./ars-review/round-N/changelog.md with one line per item `ID → section/line → change`; experiment items must later cite their ledger run; re-scoped items must read `substituted: <what> — reason: <why>`. Manuscript numbers only from ./ledger/. End with: done / awaiting my decision / page count.
```
🚦 Phase 3 停下后你回复决定(如 `Run REV-001, REV-002; re-scope REV-006`),它继续执行 cluster C(实验项交 🧪 GLM,走 Step 10–11 的台账规则)。**cluster D(方法本身被判弱)不在稿子里修**:回 Step 11 改方法(过 provenance guard)→ 新方法只有在开发集上严格更好才替换,否则保留原方法并把异议写成 limitation / 收窄 claim → 若方法变了,重跑 Step 12.5 消融 → 重写受影响章节 → 再 Step 16。上限 2 轮,之后停下:🧭 Codex 给意见,🚦 你决定。
📄 `round-N/changelog.md`。规则:实验项必须引用 ledger run;替代方案必须显式写明,不许静默跳过。

**Step 16 🧭 Codex(Reviewer #2)零参数复审 → 循环至收敛**

```text
ars-reviewer re-review
```
它从工作区读 venue/清单/路径,优先采用 Claude 写的 `changelog.md`;只逐项判 RESOLVED / NOT;禁止对旧文本提新异议;输出到 `round-2/`。**重复 Step 15–16 直到 CONVERGED。**

**Step 17 🧭 Codex 投稿前终审(高利害;同一个 Codex 会话:它看过审稿轮,所以是最终检查、不是盲审,记录里写明)**

```text
ars-reviewer — target venue: <venue year>, paper: ./paper.tex, final review
Final pass before submission: run Phase-0, the security sprint contract, and the full five-persona panel with the venue's exact decision vocabulary. You ran the review rounds in ./ars-review/, so this is not a blind review: say so in the record, and judge the paper as it now stands, not only the items raised before.
```
🚦 **你决定**:投,或再修一轮。这次终审不是盲审;它的独立性来自分工:Codex 没写论文、没跑实验。

- **预期管理:终审可能给出 Major Revision——这不与 re-review 的 CONVERGED 矛盾。** re-review 只判冻结清单(收敛机制),
  终审是全新 7 维度全面评审(覆盖机制),会发现 round-1 从未列出的问题。处理:把它当作**新的冻结清单**跑一个
  收缩周期(Step 15 → 16 re-review → 收敛),再让 Codex 终审一次。**停止规则**:收敛后的全新终审最多两次;
  若第二次仍产生**不同种类**的新 must-fix,视为审稿人方差而非论文缺陷——参考 Codex 的意见,由你决定是否投稿。真实 PC 也互不一致;
  两个 Accept 级判定 + 一个异议是正常可投状态。让 Claude 用 Step 15 提示词读取新轮次,并按「覆盖缺口 /
  重提已解决项 / 重提有意重定范围项」分类后再决定修哪些、驳哪些。

---

**Step 17.2 🧪 GLM 投稿前完整性审计 + artifact 打包(两个交付物:论文 和 代码;🔬 Claude 干净检出重跑)**

```text
Run the pre-submission 4-check audit from research_integrity_protocol.md §3 and write the result to ./ledger/audit.md: (1) score re-verification — from a clean checkout of the artifact, run its own scripts and confirm every number in ./paper.tex reproduces; (2) specification compliance — the code obeys the task rules and the threat model as stated; (3) reference verification — every citation exists and every CVE / ATT&CK id resolves; (4) method-code alignment — compare the Method section against the code and list every mismatch. Then package the artifact: code as run, scripts that regenerate every table and figure from the raw outputs, a README with exact commands and environment, anonymized for double-blind review. Report PASS/FAIL per check; do not fix silently — list what failed.
```
🔬 Claude 核查:从干净检出把 4 项审计重跑一遍(通用核查 prompt,`<item>` = "Reproducibility")。
🚦 任何一项 FAIL 都先修再投。📄 `ledger/audit.md` + 打包好的 artifact 目录。

**Step 17.5 🔬 Claude 每轮评审 / 投稿决定后:蒸馏经验(L2 retrospective)**

```text
Run the S8.5 retrospective: distill this review round / decision into
knowledge_notes/<project>.md — framing that survived at which venue, which
rejection anchor fired, what was ruled out and why — and PROPOSE (do not
auto-apply) a knowledge_index edit. Mark it provisional. Also run the
integrity self-audit (research_integrity_protocol.md §3): did any number come
from a best single run instead of the seed distribution? any tuning on the
reported test set? any held-out/test-data use left undisclosed? does the
released artifact match the paper's method? Record any near-miss.
```

- 📄 `knowledge_notes/<项目>.md` + 提议的 knowledge_index 增补(交你审,不自动写)
- 意义:你每篇论文学到的东西(哪个 framing 在 NDSS 活下来、哪条 anchor 触发)沉淀进活知识层,下一篇更准。单项目=假设,第二个项目确认才升为定律。

## 阶段 E · 投稿与真实评审(Step 18–19)

**Step 18 🧭 Codex(顾问)投稿规划(🔬 Claude 核对截稿日期)**

```text
Plan my submission to <venue>: which cycle, deadline only from deadlines_current.md (refresh if stale), a work-back schedule, and the submission-logistics checklist for this venue (registration freeze, per-author cap, per-author attestations, artifact deadline). Write it to ./reviews/submission_plan.md.
```
🔬 Claude 核对:计划里的每个日期都和 `security-track/references/deadlines_current.md` 一致(Fetched 超过 7 天先刷新再核对)。
🚦 **你决定**:投哪轮。

**Step 19 真实审稿意见到达**

🔬 Claude(revision coach;🧭 Codex 对 rebuttal 草稿给意见):

```text
ars-revision-coach — venue: <venue year>, decision: <decision tier>
<paste the decision letter verbatim>
Produce the Revision Roadmap and the response-package structure for this venue's decision tier (verbatim criteria + change list + per-criterion mapping + diff), plus a work-back schedule against the resubmission window.
```
rebuttal 草稿写好后:🧭 `ars-rebuttal-audit — venue: <venue year>` + 意见 + 草稿(venue 硬规则:S&P 500 词、禁未经要求的新材料)。多轮机制细节见 `major_revision_playbook.md`。

---

## 随手工具(不走全流程时)

| 需要 | 用法 | 谁 |
|---|---|---|
| 精读单篇论文(非综述) | `Peruse this paper: <path> — full single-paper dissection` | 🧪/🔬 |
| 快速三维扫一批论文 | `ars-3w <主题>`(WHY/HOW/WHAT 筛选) | 🔬 |
| 查某子领域的审稿门槛 | 直接问「NDSS 对 side-channel 论文的评估门槛」(读 knowledge_index) | 🔬 |
| 只查截稿/选会 | 直接问(日历自动刷新,>7 天先重拉) | 🧭(🔬 核对日期) |
| 改方法时防"偷梁换柱" | 自动触发:改进/替换方法时走 method_change_provenance(剥名搜先例→RENAME 判定) | 🧪(🔬 核查) |
| 自检 skill 是否完好 | `bash security-track/tests/run_all_checks.sh`(behavior + workspace + knowledge 三项静态校验) | 你 |

## 冷启动与维护

- **冷启动**:任何工具从流程中段开新会话时,若项目目录有锚文件(Step 0.2)则自动加载 skill;否则首条消息显式调用——Claude `/academic-research-skills:security-track <request>`,Codex `$security-track <request>`,opencode 用任一 `ars-*` 别名开场。
- **更新(skill 每次改动后,三边一起做)**:
  - 🔬 Claude Code:`/plugin update academic-research-skills`(物化拷贝,需手动刷新)
  - 🧭 Codex:`codex plugin marketplace upgrade ars-codex && codex plugin add ars-codex@ars-codex`(同上)。**注意**:上游插件版本号(0.1.24)由 upstream 拥有,我们不 bump(bump 会破坏零冲突同步)。若 upgrade 后仍是旧内容(security-track 改动没生效),强制清缓存重装:`rm -rf ~/.codex/plugins/cache/ars-codex && codex plugin marketplace upgrade ars-codex && codex plugin add ars-codex@ars-codex`
  - 🧪 opencode:**无需操作**——symlink 直读 fork,`git pull` 后即最新
  三个安装是三份独立拷贝;只更新一边会造成各 agent 跑在不同版本的协议上。
  上游更新(2026-10-06 起不再合并,只审阅后移植):在 `dev` 上运行 `git upstream-review`,列出上次审阅之后的上游改动和文件。逐项决定:移植 / 改写后移植 / 不要(写明原因);手工移植后跑 `bash security-track/tests/run_all_checks.sh` 和 `compare_upstream_lints.sh`,把结论写进 `UPSTREAM.md` 的审阅记录,并更新「上次审阅的上游提交」。截稿日历照旧按 >7 天规则自动刷新。
  最后 `git push origin dev`,并按上面的「更新」把三个工具刷新一遍。
- **CI 邮件** = 上游质量门在审我们的定制,按报错修。
