# HOWTO — 三方协作分步指南:opencode(学生)× Claude Code(导师)× Codex(审稿人)

> 从零到投稿的完整操作手册。每一步标明 **用哪个工具/agent**、**复制哪段 prompt**(全英文,可直接粘贴)、
> **产出什么文件**、**你要做什么决定**。本文件在两个 fork 中同源:本仓库(Claude Code 插件)与
> `academic-research-skills-codex`(Codex 插件)。安装细节见 `security-track/README.md`。
>
> **本平台角色**:Claude Code 在此流程中是 🧑‍🏫 **导师**(Step 3/6/9/12/17/18);
> 若你只有 Claude Code 一个工具,🎓 学生步骤也可在 Claude Code 里跑(用同样的 prompt,
> 前缀改为对应 `/ars-*` 命令),但建议 🔍 审稿人步骤仍换到不同模型家族(Codex)以保持独立性。
>
> 图例:🎓 opencode(学生,执行)  🧑‍🏫 Claude Code(导师,判断)  🔍 Codex(审稿人,判定)  🚦 你的决定门  📄 产出文件

---

## 为什么这样分工

| 角色 | 工具 | 干什么 | 为什么是它 |
|---|---|---|---|
| 🎓 学生 | opencode | 检索、写卡片、写代码跑实验、维护台账、改稿、写 changelog——所有**执行密集型**工作 | 通过 `~/.claude/skills` 加载全套 ARS + security-track;模型可换、上下文大、成本低 |
| 🧑‍🏫 导师 | Claude Code | 5 道决定门**之前**的把关:选题值不值、novelty 诚不诚实、实验设计能否扛住反驳——**判断密集型** | 完整 ARS 机制(真多次独立调用、盲态隔离强、novelty-engine);最强推理 |
| 🔍 审稿人 | Codex | 论文成稿**之后**的正式模拟评审 + re-review 循环——**判定型**,不讨论只对清单 | **不同模型家族**:没参与设计、对学生思路无"母爱";天然实现跨模型评审 |

三条纪律:**审稿人绝不参与设计**(S7 之后才进场);**导师绝不改稿**(只写批注到文件,改动全由学生执行);**决定门不外包**(五道门是你的,三个模型只提名)。
三方全部通过**磁盘文件**交接,零对话依赖。

---

## 阶段 0 · 一次性环境准备

**Step 0.1 三个工具都装好 skill**

- 🧑‍🏫 Claude Code:`/plugin marketplace add waterwoods-ai/academic-research-skills` → `/plugin install academic-research-skills@academic-research-skills`
- 🔍 Codex:`codex plugin marketplace add waterwoods-ai/academic-research-skills-codex --ref dev` → `codex plugin add ars-codex@ars-codex`
- 🎓 opencode:它从 `~/.claude/skills/` 发现 skill。把 fork 的 5 个 skill 目录 symlink 进去(**本机配置,不随仓库分发,换机器重做**):
  ```bash
  SRC=/path/to/academic-research-skills   # 你 clone 的 fork(dev 分支)
  cd ~/.claude/skills
  for s in academic-paper academic-paper-reviewer academic-pipeline deep-research security-track; do
    ln -sfn "$SRC/$s" "$s"; done
  ls -la ~/.claude/skills | grep -E 'academic|security'    # 5 个链接指向 live fork,无悬空
  ```

**Step 0.2 建项目目录 + 锚文件(三方都读,确定性加载 skill)**

```bash
mkdir my-paper && cd my-paper
cp $SRC/security-track/templates/project-anchor-CLAUDE.md ./CLAUDE.md   # Claude Code 读
cp $SRC/security-track/templates/project-anchor-AGENTS.md ./AGENTS.md   # Codex + opencode 读
```
编辑两个文件填三行:target venue、当前阶段、论文路径。以后**每次都在这个目录里启动三个工具**。

**Step 0.3 各工具冒烟测试**(每个工具问同一句,应去读 playbook 而非凭记忆答):

```text
What is the NDSS Major Revision process, and which Big-4 venues still have one?
```

正确答案要点:只有 NDSS 还有;S&P 2024 起 Accept/Reject;USENIX '26 取消;CCS 只有 Minor revision。三个工具都答对 = 环境就绪。

---

## 阶段 A · 选题(Step 1–4)

**Step 1 🎓 文献综述 + gap 登记**

```text
ars-lit-review <your area, e.g. physics-based sensor spoofing detection for ICS>, ensure broad coverage.
Write the gap registry to ./gap_registry.md — each gap must carry: the search that failed to fill it (queries, indexes, date), the nearest-miss papers and why each falls short, and the security question the gap blocks.
```
📄 `gap_registry.md`。你的动作:划掉不感兴趣的;没检索证据的 gap 让它补检索。

**Step 2 🎓 课题延伸(RQ 卡片)**

```text
Extend research topics from ./gap_registry.md. My resources: <honestly list: testbeds / devices / dataset access you have>.
Write ranked RQ cards to ./rq_cards.md — each with a threat-model sketch, contribution type (attack / defense / measurement / tool; note CCS rejects SoK), target-venue fit, feasibility against my resources, and the dogma it challenges if any. Rank by impact × feasibility × freshness.
```
📄 `rq_cards.md`

**Step 3 🧑‍🏫 导师把关选题(go / no-go)** 🚦

```text
Mentor review of ./rq_cards.md and ./gap_registry.md for a Big-4 security venue.
For each of the top-3 RQs: retrieve the 5–10 most-cited and most-recent Big-4/tier-2 papers and rule SATURATED (name the papers) / MISFRAMED (restate the better question) / VIABLE (name the open territory). Then tell me which unstated assumption (dogma) shared by prior work is most worth challenging. Write your verdicts as annotations into ./rq_cards.md; do not rewrite the student's cards.
```
🚦 **你决定**:选定 1 个 RQ,go / pivot / stop。这道门防止在饱和方向烧半年。

**Step 4 🎓 落定课题**

```text
Finalize RQ-<n> per the mentor annotations in ./rq_cards.md. Write ./research_question.md: the RQ, threat model, the dogma being challenged, target venue, and why it fits that venue.
```
📄 `research_question.md`

---

## 阶段 B · 方法与 novelty(Step 5–7)

**Step 5 🎓 提出方法 / 深化你的方法 → Contribution Card**

```text
Propose a new method for the RQ in ./research_question.md          ← from scratch
   (or) Evaluate the novelty and contribution of my method: <description>   ← bring your own
Write ./contribution_card.md with: 3–5 falsifiable claims; per-claim novelty verdict NOVEL-WITHIN-SEARCH / INCREMENTAL / KNOWN from real retrieval against Big-4 + tier-2 literature with the nearest prior work cited; a positioning table vs the 3–5 closest methods; a one-paragraph delta statement in the community's own terms; formalization (math or algorithm + complexity) plus the threat model; and honest weaknesses.
```
📄 `contribution_card.md`。规则:判 KNOWN 的 claim 当场丢弃;INCREMENTAL 需给出定位论证。

**Step 6 🧑‍🏫 导师审 novelty 与贡献** 🚦

```text
Mentor review of ./contribution_card.md. Independently re-verify each novelty verdict by real retrieval (do not trust the student's search). Which claim would a Big-4 reviewer kill first, and with which of the eight standard rejection anchors? Is the delta statement honest or inflated? Is the formalization actually a method (algorithm + threat model) or still a sketch? Annotate the card in place; do not rewrite it.
```
🚦 **你决定**:批准卡片,或退回 Step 5。

**Step 7 🎓 按批注修卡**

```text
Revise ./contribution_card.md per the mentor annotations. Keep an M-v1 version tag at the top; every later method change bumps the version and is logged in ./method_changelog.md.
```

---

## 阶段 C · 实验:设计 → 冻结 → 执行 → 改进(Step 8–12)

**Step 8 🎓 起草验证计划(按论文类型的反驳表)**

```text
Design validation experiments for the method in ./contribution_card.md. First classify the paper type (attack / defense / measurement / tool / CPS / IoT / ML-for-security / theory) and pick the matching row of the S4 refutation table in research_loop_protocol.md. Write ./validation_plan.md: per claim — the experiment or proof obligation, metrics, NUMERIC success criteria, strongest published baselines correctly tuned, ablations, statistical plan (seeds, repetitions, tests), and the artifact / open-science plan. Mark the file DRAFT.
```
📄 `validation_plan.md (DRAFT)`

**Step 9 🧑‍🏫 导师审设计 → 冻结** 🚦

```text
Review ./validation_plan.md as the mentor. Check: does each claim's validation survive the specific refutation a Big-4 reviewer of THIS paper type will attempt (adaptive adversary for defenses; real target end-to-end for attacks; artifact-ruling-out for measurement; real testbed + physical consequence for CPS; device diversity for IoT; base rates + temporal split for ML detection; proof for theory)? Are the success criteria numeric and pre-registered? Are the baselines the strongest published ones? Annotate in place. Do not change the criteria yourself — propose, and I decide.
```
🚦 **DESIGN FREEZE**:你批准后把文件头改为 `FROZEN <date>`。**此后成功标准终身不动;改进循环只许改方法。**

**Step 10 🎓 实现并运行(Codex 主场也可,但为保持单一作者建议仍由学生做)**

```text
Implement and run the experiments in ./validation_plan.md (FROZEN). Maintain ./ledger/ as the provenance ledger: one entry per run with experiment id → claim id, planned vs executed (name every deviation), raw log path, verdict against the pre-registered criterion (MET / UNMET / INCONCLUSIVE), and any negative or surprising result. Numbers in any later document may come only from this ledger.
```
📄 `ledger/`。你的动作:抽查日志与台账一致。

**Step 11 🎓 改进循环(仅当有 UNMET)**

```text
The criterion for <claim-k> is UNMET per ./ledger. Improve the method: name the deficiency with ledger evidence; make ONE targeted change with a mechanism hypothesis ("criterion X fails because Y; change Z addresses Y"); re-run only the affected experiments plus a regression check on previously-MET criteria; log M-v<N+1> in ./method_changelog.md. The success criteria in ./validation_plan.md are frozen — do not touch them.
```
🚦 **3 轮硬上限**后停下找导师(Step 12)。

**Step 12 🧑‍🏫 导师检查点(每 3 轮改进后,或改进达标后)** 🚦

```text
Mentor checkpoint. Read ./validation_plan.md (FROZEN), ./ledger/, ./method_changelog.md. Is the method converging on the frozen criteria, or are we chasing? Recommend exactly one of: authorize 3 more iterations / pivot back to method design with lessons recorded / accept-and-report honestly (negative results included). Then stress-test the method + ledger package as if you were the panel: what is the fatal objection, if any, before we spend effort writing the paper?
```
🚦 **你决定**:继续 / pivot / 如实报告。

---

## 阶段 D · 论文与评审循环(Step 13–17)

**Step 13 🎓 写论文**

```text
ars-full — target venue: <venue year>
Materials: ./contribution_card.md (claims spine), ./ledger/ (all numbers), ./validation_plan.md, ./research_question.md.
Security-paper structure (Intro / Threat Model / Design / Implementation / Evaluation / Discussion / Related Work / Ethics Considerations), numeric citations, double-blind, within the venue page budget. Every number must trace to a ledger entry. Output ./paper.tex.
```
📄 `paper.tex`

**Step 14 🔍 审稿人首轮评审(自动建档)**

```text
ars-reviewer — target venue: <venue year>, paper: ./paper.tex
```
📄 `ars-review/round-1/`:`decision.md`(判定 + 编号任务清单)、`compliance.md`(Phase-0 表)、稿件快照、`state.json`。
你的动作:**先看 Phase-0**——有 FAIL 先修合规(桌拒救不回来);再看任务清单。核对一眼 `round-1/` 里的实际文件名(agent 未必严格照约定命名)。

**Step 15 🎓 学生按清单修改 + 写 changelog**

```text
Revise ./paper.tex against ./ars-review/round-1/decision.md (closed-world: only the numbered tasks; anything else is optional and must be labeled so). If a task is wrong or infeasible, do NOT silently skip it — write the substitute and the reason. Write ./ars-review/round-1/changelog.md mapping every task ID to the exact change made (section + one line). Numbers still come only from ./ledger/.
```
📄 `round-1/changelog.md`

**Step 16 🔍 审稿人零参数复审 → 循环至收敛**

```text
ars-reviewer re-review
```
它从工作区读 venue/清单/路径,优先采用学生的 `changelog.md`;只逐项判 RESOLVED / NOT;禁止对旧文本提新异议;输出到 `round-2/`。**重复 Step 15–16 直到 CONVERGED。**

**Step 17 🧑‍🏫 投稿前终审(高利害,换模型家族再看一次)**

```text
/ars-reviewer — target venue: <venue year>, paper: ./paper.tex
Final independent pass before submission: run Phase-0, the security sprint contract, and the full five-persona panel with the venue's exact decision vocabulary. Do not read ./ars-review/ first — judge blind, then compare.
```
🚦 **你决定**:投,或再修一轮。两个模型家族独立收敛 = 你能拿到的最强投稿前信号。

---

## 阶段 E · 投稿与真实评审(Step 18–19)

**Step 18 🧑‍🏫 投稿规划**

```text
Plan my submission to <venue>: which cycle, deadline from the live calendar (refresh if stale), a work-back schedule, and the submission-logistics checklist for this venue (registration freeze, per-author cap, per-author attestations, artifact deadline).
```
🚦 **你决定**:投哪轮。

**Step 19 真实审稿意见到达**

🎓 或 🧑‍🏫 都可(判断为主时用导师):

```text
ars-revision-coach — venue: <venue year>, decision: <decision tier>
<paste the decision letter verbatim>
Produce the Revision Roadmap and the response-package structure for this venue's decision tier (verbatim criteria + change list + per-criterion mapping + diff), plus a work-back schedule against the resubmission window.
```
rebuttal 草稿写好后:🔍 `ars-rebuttal-audit — venue: <venue year>` + 意见 + 草稿(venue 硬规则:S&P 500 词、禁未经要求的新材料)。多轮机制细节见 `major_revision_playbook.md`。

---

## 冷启动与维护

- **冷启动**:任何工具从流程中段开新会话时,若项目目录有锚文件(Step 0.2)则自动加载 skill;否则首条消息显式调用——Claude `/academic-research-skills:security-track <request>`,Codex `$security-track <request>`,opencode 用任一 `ars-*` 别名开场。
- **更新**:Claude `/plugin update academic-research-skills`;Codex `codex plugin marketplace upgrade ars-codex && codex plugin add ars-codex@ars-codex`;opencode 跟随 symlink,`git pull` fork 即生效。上游同步:仓库内 `git sync-upstream`(自动刷新截稿日历)。
- **CI 邮件** = 上游质量门在审我们的定制,按报错修。
