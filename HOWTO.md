# HOWTO — 研究组协作分步指南:Claude Code(Director)× GLM(安全科学家)× Codex(研究工程师 + Reviewer #2)

> 只想 5 分钟跑起来?看 [`QuickStart-security.md`](QuickStart-security.md)。本文件是完整参考。
>
> 想要**一步一步被带着走**(而不是照这 19 步自己推进)?说 `Be my security research mentor` 或 `一步一步指导我` —— 触发 `security_mentor_protocol`:有状态、一次一步、苏格拉底式,从选题带到投稿,进度存 `paper_progress.md` 可随时停/续。它和 `ars-plan`(一次性出整篇计划)相反。
>
> 从零到投稿的完整操作手册。每一步标明 **用哪个工具/agent**、**复制哪段 prompt**(全英文,可直接粘贴)、
> **产出什么文件**、**你要做什么决定**。本文件在两个 fork 中同源:本仓库(Claude Code 插件)与
> `academic-research-skills-codex`(Codex 插件)。安装细节见 `security-track/README.md`。
>
> **本平台角色**:Claude Code 是 🧑‍🏫 **Director**:定研究问题、分派任务、追踪证据、写方向文件和论文、守 Gate 1–4(见「谁做哪一步」)。
> 若你只有 Claude Code 一个工具,🎓 执行步骤也可在 Claude Code 里跑(用同样的 prompt,
> 前缀改为对应 `/ars-*` 命令),但每次核查都换新会话,🔍 审稿步骤尽量换到不同模型家族以保持独立性。
>
> 图例:🎓 执行步骤(标题里写明交给 GLM / Codex)  🧑‍🏫 Claude Code(Director,判断)  🔍 Codex(Reviewer #2,判定)  🚦 你的决定门  📄 产出文件

---

## 为什么这样分工(三个 agent 的研究组,按 `orchestration.md`,2026-10-06 起)

| 角色 | 工具 | 问的问题 | 负责 | 只写这些文件 |
|---|---|---|---|---|
| PI | 你 | 我们到底要做出什么贡献? | 方向、安全范围、设计冻结、每次算力启动、结论与 claim | — |
| 🧑‍🏫 Director(兼文献与新颖性) | Claude Code | 我们在回答对的科学问题吗?别人做过了吗? | 研究问题、假设拆解、任务分派、证据追踪、决定记录、论文架构与写作、分歧裁决、门禁;用 Elicit / Zotero API、选题 skill 和检索子代理做文献综述与 novelty 报告 | `research_question.md` `contribution_card.md` `claims.md` `decisions.md` `method_changelog.md` `paper/` `gap_registry.md` `literature.md` `literature/` |
| 安全科学家 | GLM(opencode) | 真正的攻防问题是什么? | 威胁模型、攻击面、防御假设、研究假设、对抗用例、候选方法生成(novelty-engine)、实验设计;独立核查实现与结果解释 | `rq_cards.md` `security/` `novelty_engine/` `candidate_cards.md`;冻结前的 `screening_plan.md` `validation_plan.md` |
| 研究工程师 + 🔍 Reviewer #2 | Codex | 能用实验证明并复现吗?这篇为什么该被拒? | 实验框架、gpu1 运行、复现清单、统计、回归测试、artifact;作为 Reviewer #2:用检索到的文献攻击 novelty,审威胁模型、实验设计和论文,审稿轮,拒稿理由登记 | 代码、`tests/`、`ledger/`、`results/`、`reviews/`、`ars-review/` |

四条纪律:
- **任何关键结果都不只一个负责人**:每项都有主责和独立核查(见下表);核查者不核查自己做的东西。**Codex 当 Reviewer #2 时不审自己的代码和结果**(实现由 GLM 核查,统计与复现由 Director 核查),审稿工作放在和工程不同的 Codex 线程里做。
- **新颖性只认检索到的文献**:凭记忆说"没人做过"只算线索。
- **Reviewer #2 不参与产生想法、不写论文**;最终盲审(Step 17)用一个新的 GLM 会话——它没写论文,也没参加审稿轮。
- **方向文件只按你的决定改**:Director 先把你的原话记进 `decisions.md`,再改文件;其他 agent 只写自己的文件,意见写进报告。

所有交接都通过**磁盘文件**,零对话依赖。三个 agent 都装了 ARS / security-track skill。完整规则(核查矩阵、claims 登记、拒稿理由登记、Gate 1–4、拒绝时怎么分派):`security-track/references/lab_orchestration_protocol.md`。

### 谁做哪一步

| Step | 谁做 | 谁独立核查 |
|---|---|---|
| 0 选题侦察 | 🧑‍🏫 Director(`find-research-topic` 只能在 Claude Code 跑) | — |
| 1 文献 + gap | 🧑‍🏫 Director | 🔍 Codex(补漏文献,带检索证据) |
| 2 RQ 卡片 + 威胁模型草图 | GLM | Director |
| 3 选题把关(Gate 1:>30 篇直接相关、最接近 5 篇、差异写清) | 🧑‍🏫 Director | 🔍 Codex:用检索到的文献试图推翻 novelty |
| 4 落定课题 | 🧑‍🏫 Director 按你的决定写 `research_question.md` | — |
| 5a 生成候选 | GLM(novelty-engine) | Director(机制查新) |
| 5b 候选卡 + 筛选计划 | GLM | Codex(可实现性、统计、公平性) |
| 6 审候选与计划(Gate 2:威胁模型) | 🧑‍🏫 Director + 🔍 Codex | 🚦 你冻结 |
| 7 修卡 | GLM | Director |
| 7.5 筛选 | Codex(gpu1) | GLM(实现);Director 推荐,🚦 你选定 |
| 8 验证计划 | GLM | Codex |
| 9 冻结 | 🧑‍🏫 Director + 🔍 Codex | 🚦 你冻结 |
| 10–11 运行与改进 | Codex | GLM(实现)、Director(统计) |
| 12 检查点(Gate 3:实验有效性) | 🧑‍🏫 Director | GLM |
| 12.5 消融 | Codex | Director |
| 13 写论文(先过 Gate 4:贡献) | 🧑‍🏫 Director | 🔍 Codex(逐句核对引用) |
| 14、16 审稿 | 🔍 Codex | GLM(第二读) |
| 15 修改 | 🧑‍🏫 Director;实验项交 Codex | Codex 复核文字项;实验项由 GLM 复核 |
| 17 投稿前终审 | 新的 GLM 会话,盲审 | 🚦 你 |
| 17.2 审计 + artifact | Codex | Director(干净检出重跑) |
| 17.5 复盘、18 投稿规划、19 真实审稿 | 🧑‍🏫 Director | Codex(rebuttal 审查) |

- 步骤 prompt 里的 "Mentor" 就是 Director;其余 prompt 发给上表「谁做」那一列的 agent,文件名不变。
- **某个 agent 拒绝任务时,不要把同一请求原样转给另一个 agent。** 由 Director 拆分:文献 → Director,威胁模型 → GLM,防御实现与统计 → Codex;对目标的攻击执行、或超出 `AUTHORIZED_RESEARCH.md`(模板在 `security-track/templates/`)的部分交你决定。
- 只有一两个工具时:角色可以合并,核查不能省——每次核查换新会话,只给产出物不给推理过程。

---

## 阶段 0 · 一次性环境准备

**Step 0.1 各工具装好 skill**

- 🧑‍🏫 Claude Code:`/plugin marketplace add waterwoods-ai/academic-research-skills` → `/plugin install academic-research-skills@academic-research-skills`
- Codex(研究工程师):`codex plugin marketplace add waterwoods-ai/academic-research-skills-codex --ref dev` → `codex plugin add ars-codex@ars-codex`
- GLM(opencode):它从 `~/.claude/skills/` 发现 skill。把 fork 的 6 个 skill 目录 symlink 进去(5 个 ARS / security-track + 生成器 `novelty-engine`;另外 3 个选题 skill 需要浏览器,opencode 用不了,不必链接;**本机配置,不随仓库分发,换机器重做**):
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

## 阶段 A · 选题(Step 1–4)

> **从零开始,先看你手里有什么:**
>
> | 你现在有 | 从哪里进 |
> |---|---|
> | 只有一个大方向,没有题目 | 🧑‍🏫 Claude Code:`find-research-topic <大方向>` 拿 3–7 个候选题目,选一个再进 Step 1(它的 `runs/<日期>-<slug>/report.md` 是 Step 1 的输入) |
> | 有具体方向,没有论文 | 直接 Step 1——ARS 自己检索,不需要你提供文献 |
> | 有方向 + 自己攒的论文(Zotero / PDF 文件夹) | Step 1,在 prompt 里写明论文位置;ARS 先筛你的,再补检索没覆盖的部分 |
> | 有一篇想在其上改进的基线论文 | Step 1–4 照常定题;到 Step 5 先跑 `novelty-filter <论文>` 建 limitation 列表(5a 的方式 B 从它出发) |
> | 已经有自己的方法 | 跳到 Step 5 的 `Evaluate…` 分支 |

**Step 1 🧑‍🏫 Director 文献综述 + gap 登记(Codex 补漏)**

```text
ars-lit-review <your area, e.g. physics-based sensor spoofing detection for ICS>, ensure broad coverage.
If a find-research-topic report (./runs/*/report.md) or a research-gaps gap-report.md exists, start from it: carry its candidate gaps and evidence papers in, then complete each gap to the form below.
Write the gap registry to ./gap_registry.md — each gap must carry: the search that failed to fill it (queries, indexes, date), the nearest-miss papers and why each falls short, and the security question the gap blocks.
Save every included paper to ./literature.md (citation, one-line finding, which gap it bears on) — later steps read it.
```
📄 `gap_registry.md`、`literature.md`。你的动作:划掉不感兴趣的;没检索证据的 gap 让它补检索。

> **检索前端(Claude Code,见 `topic_scouting_overlay.md`)**:还没有题目 → `find-research-topic`(Elicit + Litmaps 浏览器侦察,出 3–7 个候选);题目已定、要系统化的 gap 证据 → `research-gaps`(Elicit API,需 Elicit Pro + `ELICIT_API_KEY`,结果归档到 Zotero)。它们的 `open / narrow / saturated` 只是扫描级线索,不是 novelty 结论;每个 gap 仍要补齐上面三项。**两条必跑检索**:不限年份、去掉流行词的「祖先检索」,以及不分应用领域的「相邻方法族检索」。Codex / opencode 没有浏览器,用 `ars-lit-review` + 这两条检索规则。

> 顺带:agent 按你的子领域从 `knowledge_index.md` 加载该领域的审稿门槛(adaptive-eval / 测床+物理后果 / OTA 对标 in-toto/SLSA 等),S1–S3/S7 全程套用。

**Step 2 🎓 GLM 课题延伸(RQ 卡片 + 威胁模型草图)**

```text
Extend research topics from ./gap_registry.md. My resources: <honestly list: testbeds / devices / dataset access you have>.
Write ranked RQ cards to ./rq_cards.md — each with a threat-model sketch, contribution type (attack / defense / measurement / tool; note CCS rejects SoK), target-venue fit, feasibility against my resources, and the supported assumption, confirmed limitation or located observation it builds on (no dogma is required). Compare security impact, feasibility and the prior-work delta separately; do not use an aggregate score as evidence.
```
📄 `rq_cards.md`

**Step 3 🧑‍🏫 Director 把关选题(go / no-go;Gate 1)** 🚦

```text
Mentor review of ./rq_cards.md and ./gap_registry.md for a Big-4 security venue.
For each of the top-3 RQs: retrieve the 5–10 most-cited and most-recent Big-4/tier-2 papers and rule SATURATED (name the papers) / MISFRAMED (restate the better question) / VIABLE (name the open territory). Then identify any source-backed assumption worth challenging, or the confirmed limitation/located observation motivating the RQ. Zero supported assumptions is valid; distinguish explicit assumptions, shared dependencies and unverified hypotheses. Then run the topic verification gate (topic_verification_gate.md) on the top RQ: answer the 12 questions with evidence and a pass / weak / fail status each, freeze them, and give a go / revise / stop verdict with the deciding question. Write your verdicts as annotations into ./rq_cards.md; do not rewrite the student's cards.
```
🚦 **你决定**:选定 1 个 RQ,go / pivot / stop。这道门防止在饱和方向烧半年。想要独立的第二意见:让另一个模型家族(🔍 Codex,或 Claude Code 里的 `verify-research-topic` 走 ChatGPT 盲评)只看设计事实、不看你的答案,再按证据逐条对账。

**Step 4 🧑‍🏫 Director 落定课题(按你的决定)**

```text
Finalize RQ-<n> per the mentor annotations in ./rq_cards.md. Write ./research_question.md: the RQ, threat model, the supported assumption or limitation/observation IDs (with evidence status), target venue, why it fits that venue, and the topic-gate verdict with its date (copied from the mentor annotation).
```
📄 `research_question.md`

---

## 阶段 B · 方法与 novelty(Step 5–7.5)

**Step 5 🎓 提出方法 / 深化你的方法 → 候选卡**

从零提方法的顺序:**5a 生成**(三条证据驱动路线 + 统一检查,最多留 3 个不同机制的候选)→ **5b 候选卡 + 筛选计划** → Step 6 Director + Reviewer #2 审 → Step 7 修卡 → **Step 7.5 便宜实验筛选,选定 1 个** → Contribution Card。
已经有自己的方法:跳过 5a 和 7.5,在 5b 用 `Evaluate…` 那段直接写 `contribution_card.md`。

实证/测量/SoK 型贡献如果不需要新方法,按 `research_loop_protocol.md` S3 的 contribution-type 分支写 Contribution Card,用可复现的测量/分析协议和证据义务替代方法形式化;不强造算法或基线提升目标,直接进入对应 S4 验证路线。

**5a 🎓 GLM 运行生成器 `novelty-engine`**(三个工具都能用)

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

**5b 🎓 GLM 候选卡 + 筛选计划(Codex 核查)**

```text
From ./novelty_engine/03_hybrid_methods/candidates.md and ./novelty_engine/04_formal_spec/formal_specification.md, write ./candidate_cards.md: one card per shortlisted candidate (at most three). Each card carries its origin IDs/evidence status, cause and rival explanation, new assumptions/costs and borrowed components; its OWN 1–3 falsifiable claims; the novelty verdict per claim (NOVEL-WITHIN-SEARCH / INCREMENTAL / KNOWN from real retrieval against Big-4 + tier-2 literature, nearest prior work cited); the security consequence; the formalization (algorithm + complexity) plus the threat model; honest weaknesses; and its cheapest decisive test with a numeric pass criterion.
Then write ./screening_plan.md, marked DRAFT and shared by all candidates: the development data (it can never become the held-out), the strongest baseline to reproduce, the ONE comparison criterion used to choose between candidates, and the implementation and tuning budget per candidate (the same for all).
```
📄 `candidate_cards.md`、`screening_plan.md (DRAFT)`。规则:判 KNOWN 的候选当场丢弃,不为了"代表某种生成方式"而保留。

自带方法时改用这一段(不写候选卡,不筛选):

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

**Step 6 🧑‍🏫 Director 审候选与筛选计划(🔍 Codex 独立攻击;Gate 2)** 🚦

```text
Mentor review of ./candidate_cards.md and ./screening_plan.md (if I brought my own method, review ./contribution_card.md the same way instead). For each candidate: independently re-verify each novelty verdict by real retrieval (do not trust the student's search). Which claim would a Big-4 reviewer kill first, and with which of the standard rejection anchors? Is the security consequence real, or only a better number? Is the formalization actually a method (algorithm + threat model) or still a sketch? Is the decisive test really decisive, with a numeric pass criterion? For the screening plan: is it fair to every candidate (same data, same baseline, same budgets), and is the development data disjoint from anything that could later serve as the held-out? Annotate the files in place; do not rewrite them.
```
🚦 **你决定**:哪些候选进筛选(可以砍到 1–2 个),或退回 Step 5。批准后把 `screening_plan.md` 文件头改为 `FROZEN <date>`——之后不再改数据、判据和预算。

**Step 7 🎓 GLM 按批注修卡**

```text
Revise ./candidate_cards.md per the mentor annotations. (If I brought my own method: revise ./contribution_card.md instead, keep an M-v1 version tag at the top, write ./method_changelog.md with the M-v1 entry, and skip Step 7.5.)
```

**Step 7.5 🎓 Codex 便宜实验筛选 → 选定 1 个方法** 🚦

```text
Run the candidate screening in ./screening_plan.md (FROZEN). First reproduce the strongest baseline on the development data and log it in ./ledger/. Then, for each candidate in ./candidate_cards.md, implement it only as far as its cheapest decisive test needs, within the frozen budget, and run that test on the development data — never on held-out data. Log one ledger entry per run: candidate id, planned vs executed, raw log path, and the verdict against the candidate's own pass criterion (GOOD / ENGINEER / BAD; a BAD candidate gets a root-cause note). Do not change the plan or any pass criterion after seeing results. Then recommend ONE candidate by the frozen comparison criterion (on a tie, the simpler one or the one with weaker assumptions) and stop for my confirmation.
After I confirm: write ./contribution_card.md for the selected method with the eight Contribution Card items of research_loop_protocol.md §S3, tagged M-v1; complete its formalization (the theorem or bound its claims need); write ./method_changelog.md with the M-v1 entry; and mark the runners-up in ./candidate_cards.md as reserve, with their screening results. Update the evidence summary in ./novelty_engine/03_hybrid_methods/candidates.md with tested IDs, ledger links, MET/UNMET/INCONCLUSIVE results and the selected ID; keep unrun tests as NOT RUN. Investigate failure causes and feed them back into generation; do not infer publication readiness from a model score.
```
📄 `ledger/`(筛选记录)、`contribution_card.md`(M-v1)、`method_changelog.md`。🚦 **你决定**:确认选哪一个。全部 BAD 时不降标准:带着失败原因回 5a,或找 Director。落选的候选留作后备,论文里可如实报告筛了几个、为什么选这个。

---

## 阶段 C · 实验:设计 → 冻结 → 执行 → 改进(Step 8–12)

**Step 8 🎓 GLM 起草验证计划(按论文类型的反驳表;Codex 核查)**

```text
Design validation experiments for the method in ./contribution_card.md. First classify the paper type (attack / defense / measurement / tool / CPS / IoT / ML-for-security / theory) and pick the matching row of the S4 refutation table in research_loop_protocol.md. Write ./validation_plan.md: per claim — the experiment or proof obligation, metrics, NUMERIC success criteria, strongest published baselines correctly tuned, ablations, statistical plan (seeds, repetitions, tests), and the artifact / open-science plan. Apply the evaluation-integrity rules (research_integrity_protocol.md §2): plan to report ALL testbeds/datasets/devices with regressions disclosed (no cherry-picking), fix a held-out split that method development never touches (it must be disjoint from the development data in ./screening_plan.md), and set a utility non-regression bound. Mark the file DRAFT.
```
📄 `validation_plan.md (DRAFT)`

**Step 9 🧑‍🏫 Director 审设计(🔍 Codex 独立攻击)→ 冻结** 🚦

```text
Review ./validation_plan.md as the mentor. Check: does each claim's validation survive the specific refutation a Big-4 reviewer of THIS paper type will attempt (adaptive adversary for defenses; real target end-to-end for attacks; artifact-ruling-out for measurement; real testbed + physical consequence for CPS; device diversity for IoT; base rates + temporal split for ML detection; proof for theory)? Are the success criteria numeric and pre-registered? Are the baselines the strongest published ones? Annotate in place. Do not change the criteria yourself — propose, and I decide.
```
🚦 **DESIGN FREEZE**:你批准后把文件头改为 `FROZEN <date>`。**此后成功标准终身不动;改进循环只许改方法。** 冻结的 `validation_plan.md` 就是这次实验的**预注册卡**(research_integrity_protocol.md §1):此后每个上报的数字都要能追溯到它;出结果后再动判据是 HARKing——只能走有记录的、人把关的 RE-FREEZE,不能悄悄改。

**Step 10 🎓 Codex 实现并运行(gpu1;Codex 是台账和复现清单的唯一写入者)**

```text
Implement and run the experiments in ./validation_plan.md (FROZEN). First re-run the strongest baseline in this environment and log it in ./ledger/ — every gain is measured against that reproduced number, never a paper-reported one. Screen candidate changes on a development subset (never the held-out split) before full runs. Maintain ./ledger/ as the provenance ledger: one entry per run with experiment id → claim id, planned vs executed (name every deviation), raw log path, verdict against the pre-registered criterion (MET / UNMET / INCONCLUSIVE), and any negative or surprising result. Numbers in any later document may come only from this ledger.
```
📄 `ledger/`。你的动作:抽查日志与台账一致。

**Step 11 🎓 Codex 改进循环(仅当有 UNMET)**

```text
The criterion for <claim-k> is UNMET per ./ledger. Improve the method: name the deficiency with ledger evidence; make ONE targeted change with a mechanism hypothesis ("criterion X fails because Y; change Z addresses Y"); re-run only the affected experiments plus a regression check on previously-MET criteria; log M-v<N+1> in ./method_changelog.md and update the method description and version tag in ./contribution_card.md to match (the card always describes the current method). The success criteria in ./validation_plan.md are frozen — do not touch them. IF the change introduces a new MECHANISM (not tuning) — especially a substitute to rescue a failing result — it MUST first pass method_change_provenance.md: (1) scenario fidelity (does it still solve the ORIGINAL problem, or silently redefine it?); (2) prior-art identity (strip any new name and search — a renamed known method, e.g. a "new" OTA signing scheme = in-toto/SLSA/TUF/Uptane, is a RENAME not a contribution); (3) honest outcome: ADOPT+CITE with the novelty claim dropped, or a proven genuine delta re-verified NOVEL-WITHIN-SEARCH. Record the verdict (RENAME / GENUINE-DELTA / ADOPT-AND-CITE) in the changelog.
```
🚦 **3 轮硬上限**后停下找 Director(Step 12)。

**Step 12 🧑‍🏫 Director 检查点(每 3 轮改进后,或改进达标后;Gate 3)** 🚦

```text
Mentor checkpoint. Read ./validation_plan.md (FROZEN), ./ledger/, ./method_changelog.md. Is the method converging on the frozen criteria, or are we chasing? First diagnose the ROOT CAUSE of any unmet criterion from ./ledger/ (bug? mis-tuned baseline? wrong assumption? mechanism gap?) — a negative result is a lead to investigate, not a stopping point. Then recommend exactly one of: authorize 3 more iterations (pursue the root cause and improve) / pivot back to method design (replace an unpromising approach, keep the problem) / report what works and what does not — but ONLY once the root cause is understood and a fix is either found or proven out of reach, never as a "just honestly report the negative" shortcut (integrity holds: numbers from ./ledger, criteria frozen, no cherry-picking). Then stress-test the method + ledger package as if you were the panel: what is the fatal objection, if any, before we spend effort writing the paper?
```
🚦 **你决定**:继续 / pivot / 如实报告。

**Step 12.5 🎓 Codex 消融与简化(所有判据达标后必做——即使第一次就达标、没进过改进循环)**

```text
All frozen criteria in ./validation_plan.md are MET per ./ledger. Run S6a from research_loop_protocol.md: (1) run the pre-registered ablations, one component at a time, and log each in ./ledger/; (2) if a component does not contribute, propose the simplified method — it replaces the current one ONLY if strictly better (or equal and simpler) on development data under the pre-registered metric, otherwise keep the current method; (3) if the method was replaced, re-run the ablations on the new method and update ./contribution_card.md and ./method_changelog.md to the new version. Do not touch the held-out split. If more than one candidate was GOOD, confirm which one was selected on development data and why (ledger entry). End with the source-of-gain table.
```
📄 `ledger/` 里的消融记录 + source-of-gain 表。这是论文消融表的唯一来源。

---

## 阶段 D · 论文与评审循环(Step 13–17)

**Step 13 🧑‍🏫 Director 写论文(先过 Gate 4;Codex 核对引用)**

```text
ars-full — target venue: <venue year>
Materials: ./contribution_card.md (claims spine, current method version), ./method_changelog.md (what changed and why), ./ledger/ (all numbers), ./validation_plan.md, ./research_question.md, ./literature.md and ./gap_registry.md (related work).
Security-paper structure (Intro / Threat Model / Design / Implementation / Evaluation / Discussion / Related Work / Ethics Considerations), numeric citations, double-blind, within the venue page budget. Every number must trace to a ledger entry. Output ./paper.tex.
```
📄 `paper.tex`

> 可选润色:草稿成形后跑一遍 **`academic-humanizer`**(security 校准见 `security_humanizing_overlay.md`)——去 AI 味、把动词强度对齐证据,**只降不升(never inflate)**,绝不动数字 / 引用 / CVE-ATT&CK id / scope hedge。这是**内容冻结后**的语言润色,不是改内容;会议论文跳过 Layer 6(NSF/NIH grant 模式)。

**Step 14 🔍 Codex(Reviewer #2)首轮评审(自动建档)**

```text
ars-reviewer — target venue: <venue year>, paper: ./paper.tex
```
📄 `ars-review/round-1/`:`decision.md`(判定 + 编号任务清单)、`compliance.md`(Phase-0 表)、稿件快照、`state.json`。
你的动作:**先看 Phase-0**——有 FAIL 先修合规(桌拒救不回来);再看任务清单。核对一眼 `round-1/` 里的实际文件名(agent 未必严格照约定命名)。

**Step 15 🧑‍🏫 Director 按清单修改 + 写 changelog**(实验项交 Codex;通用版:不必先自己读 round-N 的文件)

```text
A reviewer round has just been written to ./ars-review/. Find the latest round-N/ directory and read everything in it (the decision/review file, any verdict or traceability record, the compliance check).

Phase 1 — report, no edits: (a) the overall decision and how many tasks are resolved / partially / not resolved / newly raised; (b) every open item with its ID, one-line residual gap, and the evidence class needed to close it (text change / experiment run recorded in ./ledger/ / code or artifact / formalization); (c) group open items into A = compliance or desk-reject risks, B = text-only fixes, C = anything needing an experiment or artifact, D = idea-level (the method itself is judged weak — not its write-up, not its evidence).

Phase 2 — execute A then B only, text-only, touching nothing outside those items and never editing the reviewer's files. Recompile and report the exact page count.

Phase 3 — STOP: for each cluster-C item say in one line whether it is load-bearing for the target venue's contribution or removable by honest re-scoping; for each cluster-D item state the root cause in one line and the one targeted method change you would try. Never patch a D item in prose. Then wait for my decision on which to run, which to re-scope, and which D items go back to the method.

Throughout: maintain ./ars-review/round-N/changelog.md with one line per item `ID → section/line → change`; experiment items must later cite their ledger run; re-scoped items must read `substituted: <what> — reason: <why>`. Manuscript numbers only from ./ledger/. End with: done / awaiting my decision / page count.
```
🚦 Phase 3 停下后你回复决定(如 `Run REV-001, REV-002; re-scope REV-006`),它继续执行 cluster C(实验走 Step 10–11 的台账规则)。**cluster D(方法本身被判弱)不在稿子里修**:回 Step 11 改方法(过 provenance guard)→ 新方法只有在开发集上严格更好才替换,否则保留原方法并把异议写成 limitation / 收窄 claim → 若方法变了,重跑 Step 12.5 消融 → 重写受影响章节 → 再 Step 16。上限 2 轮,之后找 Director。
📄 `round-N/changelog.md`。规则:实验项必须引用 ledger run;替代方案必须显式写明,不许静默跳过。

**Step 16 🔍 Codex(Reviewer #2)零参数复审 → 循环至收敛**

```text
ars-reviewer re-review
```
它从工作区读 venue/清单/路径,优先采用 Director 写的 `changelog.md`;只逐项判 RESOLVED / NOT;禁止对旧文本提新异议;输出到 `round-2/`。**重复 Step 15–16 直到 CONVERGED。**

**Step 17 投稿前终审(高利害,由新的 GLM 会话盲审:它没写论文、没参加审稿轮)**

```text
/ars-reviewer — target venue: <venue year>, paper: ./paper.tex
Final independent pass before submission: run Phase-0, the security sprint contract, and the full five-persona panel with the venue's exact decision vocabulary. Do not read ./ars-review/ first — judge blind, then compare.
```
🚦 **你决定**:投,或再修一轮。两个模型家族独立收敛 = 你能拿到的最强投稿前信号。

- **预期管理:终审可能给出 Major Revision——这不与 re-review 的 CONVERGED 矛盾。** re-review 只判冻结清单(收敛机制),
  终审是全新 7 维度全面评审(覆盖机制),会发现 round-1 从未列出的问题。处理:把它当作**新的冻结清单**跑一个
  收缩周期(Step 15 → 16 re-review → 收敛),再换模型家族终审一次。**停止规则**:收敛后的全新终审最多两次;
  若第二次仍产生**不同种类**的新 must-fix,视为审稿人方差而非论文缺陷——按 Director 的判断,由你决定是否投稿。真实 PC 也互不一致;
  两个 Accept 级判定 + 一个异议是正常可投状态。让 Director 用 Step 15 提示词读取新轮次,并按「覆盖缺口 /
  重提已解决项 / 重提有意重定范围项」分类后再决定修哪些、驳哪些。

---

**Step 17.2 🎓 Codex 投稿前完整性审计 + artifact 打包(两个交付物:论文 和 代码)**

```text
Run the pre-submission 4-check audit from research_integrity_protocol.md §3 and write the result to ./ledger/audit.md: (1) score re-verification — from a clean checkout of the artifact, run its own scripts and confirm every number in ./paper.tex reproduces; (2) specification compliance — the code obeys the task rules and the threat model as stated; (3) reference verification — every citation exists and every CVE / ATT&CK id resolves; (4) method-code alignment — compare the Method section against the code and list every mismatch. Then package the artifact: code as run, scripts that regenerate every table and figure from the raw outputs, a README with exact commands and environment, anonymized for double-blind review. Report PASS/FAIL per check; do not fix silently — list what failed.
```
🚦 任何一项 FAIL 都先修再投。📄 `ledger/audit.md` + 打包好的 artifact 目录。

**Step 17.5 🧑‍🏫 Director 每轮评审 / 投稿决定后:蒸馏经验(L2 retrospective)**

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

**Step 18 🧑‍🏫 投稿规划**

```text
Plan my submission to <venue>: which cycle, deadline from the live calendar (refresh if stale), a work-back schedule, and the submission-logistics checklist for this venue (registration freeze, per-author cap, per-author attestations, artifact deadline).
```
🚦 **你决定**:投哪轮。

**Step 19 真实审稿意见到达**

🧑‍🏫 Director(rebuttal 草稿由 🔍 Codex 审):

```text
ars-revision-coach — venue: <venue year>, decision: <decision tier>
<paste the decision letter verbatim>
Produce the Revision Roadmap and the response-package structure for this venue's decision tier (verbatim criteria + change list + per-criterion mapping + diff), plus a work-back schedule against the resubmission window.
```
rebuttal 草稿写好后:🔍 `ars-rebuttal-audit — venue: <venue year>` + 意见 + 草稿(venue 硬规则:S&P 500 词、禁未经要求的新材料)。多轮机制细节见 `major_revision_playbook.md`。

---

## 随手工具(不走全流程时)

| 需要 | 用法 | 谁 |
|---|---|---|
| 精读单篇论文(非综述) | `Peruse this paper: <path> — full single-paper dissection` | 🎓/🧑‍🏫 |
| 快速三维扫一批论文 | `ars-3w <主题>`(WHY/HOW/WHAT 筛选) | 🎓 |
| 查某子领域的审稿门槛 | 直接问「NDSS 对 side-channel 论文的评估门槛」(读 knowledge_index) | 🧑‍🏫 |
| 只查截稿/选会 | 直接问(日历自动刷新,>7 天先重拉) | 🧑‍🏫 |
| 改方法时防"偷梁换柱" | 自动触发:改进/替换方法时走 method_change_provenance(剥名搜先例→RENAME 判定) | 🎓 |
| 自检 skill 是否完好 | `bash security-track/tests/run_all_checks.sh`(behavior + workspace + knowledge 三项静态校验) | 你 |

## 冷启动与维护

- **冷启动**:任何工具从流程中段开新会话时,若项目目录有锚文件(Step 0.2)则自动加载 skill;否则首条消息显式调用——Claude `/academic-research-skills:security-track <request>`,Codex `$security-track <request>`,opencode 用任一 `ars-*` 别名开场。
- **更新(skill 每次改动后,三边一起做)**:
  - 🧑‍🏫 Claude Code:`/plugin update academic-research-skills`(物化拷贝,需手动刷新)
  - 🔍 Codex:`codex plugin marketplace upgrade ars-codex && codex plugin add ars-codex@ars-codex`(同上)。**注意**:上游插件版本号(0.1.24)由 upstream 拥有,我们不 bump(bump 会破坏零冲突同步)。若 upgrade 后仍是旧内容(security-track 改动没生效),强制清缓存重装:`rm -rf ~/.codex/plugins/cache/ars-codex && codex plugin marketplace upgrade ars-codex && codex plugin add ars-codex@ars-codex`
  - 🎓 opencode:**无需操作**——symlink 直读 fork,`git pull` 后即最新
  三个安装是三份独立拷贝;只更新一边会造成各 agent 跑在不同版本的协议上。
  上游同步:在 `dev` 分支上运行 `git sync-upstream`(不切分支:快进 `main` → 推送 `main` → 合并进 `dev` → 刷新截稿日历 → 跑检查)。
  合并冲突只应出现在 `.claude-plugin/marketplace.json`:取上游的 `version` 和顶层描述,保留我们的插件描述和 skill 注册行;其它上游文件一律取上游版本。
  Claude fork 同步后再跑 `bash security-track/tests/compare_upstream_lints.sh`:与纯上游相比,只允许 `expected_upstream_lint_diffs.txt` 列出的 lint 有差异。
  最后 `git push origin dev`,并按上面的「更新」把三个工具刷新一遍。
- **CI 邮件** = 上游质量门在审我们的定制,按报错修。
