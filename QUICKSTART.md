# QuickStart — 安全顶会研究,5 分钟上手

> 一页纸让你跑起来。完整 19 步分步指南见 [`HOWTO.md`](HOWTO.md)。
> 三个工具的分工:🎓 opencode = 学生(干活)· 🧑‍🏫 Claude Code = 导师(把关)·
> 🔍 Codex = 审稿人(判定)。只有一个工具也能用(见文末)。

---

## 一次性设置(做一次,之后不用管)

**1. 装 skill**
- 🧑‍🏫 Claude Code:`/plugin marketplace add waterwoods-ai/academic-research-skills` → `/plugin install academic-research-skills@academic-research-skills`
- 🔍 Codex:`codex plugin marketplace add waterwoods-ai/academic-research-skills-codex --ref dev` → `codex plugin add ars-codex@ars-codex`
- 🎓 opencode(可选):把 fork 的 5 个 skill symlink 进 `~/.claude/skills/`(见 HOWTO Step 0.4)

**2. 建项目 + 锚文件**(让 skill 在你论文目录里确定性加载)
```bash
mkdir my-paper && cd my-paper
cp security-track/templates/project-anchor-CLAUDE.md ./CLAUDE.md   # Claude 读
cp security-track/templates/project-anchor-AGENTS.md ./AGENTS.md   # Codex/opencode 读
# 编辑两个文件,填三行:target venue / 当前阶段 / 论文路径
```

**3. 冒烟测试**(在项目目录里问一句,验证 skill 生效)
```text
What is the NDSS Major Revision process, and which Big-4 venues still have one?
```
答对要点(只有 NDSS 还有 Major Revision;S&P 2024 起 Accept/Reject;USENIX '26 取消)= 就绪。

---

## 最短可用路径(照抄即可,`<venue>` 换成如 `NDSS 2027`)

| 你在做什么 | 复制这段(前缀:Claude 用 `/ars-`,Codex/opencode 用裸别名) |
|---|---|
| **找课题** 🎓 | `ars-lit-review <你的方向>, ensure broad coverage` |
| **定课题** 🧑‍🏫🚦 | `Verify the research topic viability (go/no-go): <RQ>` |
| **提/评方法** 🎓 | `Evaluate the novelty and contribution of my method: <描述>` |
| **精读一篇论文** | `Peruse this paper: <path> — full single-paper dissection` |
| **设计实验** 🎓🧑‍🏫🚦 | `Design validation experiments for this method`(导师审后你标 FROZEN) |
| **跑实验** 🎓 | `Implement and run the experiments`(数字只进 `./ledger/`) |
| **写论文** 🎓 | `ars-full — target venue: <venue>` |
| **模拟审稿** 🔍 | `ars-reviewer — target venue: <venue>, paper: ./paper.tex` |
| **改完复审** 🔍 | `ars-reviewer re-review`(零参数,读 `ars-review/`) |
| **投稿前终审** 🧑‍🏫🚦 | `/ars-reviewer — target venue: <venue>, judge blind` |
| **投稿规划** 🧑‍🏫🚦 | `Plan my submission to <venue>` |
| **收到审稿意见** | `ars-revision-coach — venue: <venue>, decision: <判定档>` + 粘意见 |

🚦 = 你拍板的门(agent 只提名)。

---

## 五条铁律(体系替你守,你知道就好)

1. **novelty 永远 search-bounded**——"就我们检索范围内没有",不说"绝对首个"。
2. **数字只来自执行日志**(`./ledger/`)——论文里每个数不能凭空。
3. **成功标准设计时冻结**——改进只许改方法,不许挪标准(防死循环)。
4. **改方法要防偷梁换柱**——替换方法自动剥名搜先例;是 in-toto/SLSA 换名 = RENAME,不算贡献。
5. **截稿只认日历文件**——超 7 天自动重拉,绝不凭记忆报日期。

---

## 三个高频陷阱(直接抄答案)

- **S&P 判定只有 Accept/Reject**——它给你 Major Revision 就是错的(只有 NDSS 有)。
- **`ars-reviewer` 会给 Major Revision 而 re-review 给 Accept**——正常:re-review 只判冻结清单(收敛),全新评审是全面检查(覆盖)。见 HOWTO Step 17。
- **Codex 更新拿不到新内容**——上游版本号不 bump,强制清缓存:`rm -rf ~/.codex/plugins/cache/ars-codex && codex plugin marketplace upgrade ars-codex && codex plugin add ars-codex@ars-codex`。

---

## 只有一个工具?

- **只有 Claude Code**:学生步骤也在这跑(前缀 `/ars-*`);审稿建议仍换 Codex 保独立,至少投稿前终审换。
- **只有 Codex**:全程裸别名(`ars-reviewer ...`,**不要加斜杠**);高利害终审建议换 Claude Code。

下一步:打开 [`HOWTO.md`](HOWTO.md) 看完整 19 步 + 每步的产出物和决定门。
