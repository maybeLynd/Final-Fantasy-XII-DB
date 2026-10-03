# Reconstruction readiness, pass 2: `FFXII TZA/01-Script-VM-Native-Bridge/` (`01-scriptvm`)

| | |
|---|---|
| Stream | R2 (reconstruction readiness, pass 2), per [`docs/cloud-briefs/re-readiness-r2.md`](../../docs/cloud-briefs/re-readiness-r2.md), part A |
| Working for | FABLE |
| Pass 1 | [`cloud-reports/re-readiness/01-scriptvm.md`](../re-readiness/01-scriptvm.md) (2026-10-02, snapshot `86b70c69`) |
| This pass | 2026-10-03, snapshot `b23bdddd` (synced from XIIOnline `f9d9053b9`) |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every verdict quotes a page or a register row and gives its current location. No executable, Ghidra or live game was used. |

## How to read the citations

A citation is `ALIAS:line` against the **current** snapshot. Line numbers moved since pass 1: most pages lost their
`level:` front-matter line on 2026-10-02 (so many lines are one lower), and several pages gained sections. The paths
are relative to `FFXII TZA/01-Script-VM-Native-Bridge/`. `REG` is `FFXII TZA/_index/OPEN-QUESTIONS.md`, cited by
row id. Pages in other categories are given as paths from `FFXII TZA/` and were **not** audited for this report.

| alias | page | lines now |
|---|---|---:|
| `README` | `README.md` | 50 |
| `DT` | `scriptvm-native-dispatch-table.md` | 1,186 |
| `WAIT` | `verbs-that-only-wait-and-verbs-that-do-nothing.md` | 397 |
| `NAMES` | `how-a-script-names-a-thing-in-the-world.md` | 610 |
| `C-INT` | `CONTRACT-interpreter-core.md` | 320 |
| `C-NCL` | `CONTRACT-native-command-lifecycle.md` | 289 |
| `C-BR` | `CONTRACT-script-to-native-bridge.md` | 471 |
| `INT` | `Interpreter-Core/worldactor-scriptvm-interpreter.md` | 1,148 |
| `RES` | `Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md` | 192 |
| `REQ` | `Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md` | 257 |
| `BIND` | `Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md` | 543 |
| `VARS` | `Interpreter-Core/script-variables-and-their-storage-classes.md` | 635 |
| `ATEL` | `ATEL-Control-Modules/the-ctrl-module-debug-companions.md` | 934 |
| `NCL` | `Native-Command-Lifecycle/native-command-lifecycle.md` | 813 |
| `VD` | `Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md` | 1,533 |
| `C-VD` | `Verb-Dispatch/CONTRACT-verb-dispatch-abi.md` | 686 |
| `POP` | `Verb-Dispatch/the-shape-of-the-verb-population.md` | 498 |
| `REACH` | `Verb-Dispatch/what-each-script-verb-touches.md` | 383 |
| `CC` | `Spawn-Verbs/the-script-to-native-calling-convention.md` | 898 |
| `BP` | `Party-Presentation-Verbs/how-a-script-changes-the-battle-party.md` | 187 |
| `READIN` | `Party-Presentation-Verbs/the-party-read-in-state-machine.md` | 441 |
| `STDM` | `Party-Presentation-Verbs/the-party-standard-motion-verbs.md` | 541 |
| `LOOKS` | `Party-Presentation-Verbs/how-a-script-changes-how-the-party-looks.md` | 647 |

**Method.** I read pass 1's §2 (gaps S-1 to S-31 and G-1 to G-18) and its §3.1 value contradictions (C-V1 to C-V60).
I diffed the folder and the register between pass 1's snapshot `86b70c69` and this one: 24 files, 640 lines added,
204 removed. Every gap was then re-checked against the current page text, whether or not its lines changed. Pass 1's
68 stale-text items (§3.2, C-S1 to C-S68) are not re-audited here. Where a stale line now contradicts a newer
answer, it is listed as a new DOC gap.

---

## 1. Summary

**Pass-1 gaps: 49** (31 stated by the pages, 18 structural).

| verdict | count | ids |
|---|---:|---|
| CLOSED | **3** | S-3, S-10, G-8 |
| NARROWED | **8** | S-2, S-17, S-27, G-1, G-3, G-7, G-13, G-14 |
| OPEN | **34** | S-1, S-4, S-5, S-6, S-8, S-9, S-11 to S-16, S-18 to S-24, S-26, S-28 to S-31; G-2, G-5, G-6, G-9, G-10, G-11, G-15, G-16, G-17, G-18 |
| WRONG-IN-PASS-1 | **4** | S-25, G-4 (wholly); S-7, G-12 (in part, with a residue still open) |

**OPEN and NARROWED gaps by class** (42): STATIC 29 · RUNTIME 6 · DATA 4 · DOC 3. A gap with a mixed residue is
counted under its main class; §2 gives each one's class.

**New gaps: 9** (STATIC 5 · DOC 3 · DATA 1 · RUNTIME 0).

**Pass-1 value contradictions (C-V1 to C-V60), follow-up:** **41 resolved** on the pages since pass 1, nearly all
by OPUS's dated 2026-10-02 corrections. **19 remain**: 16 unchanged, 2 resolved only in part (C-V44, C-V45) and 1
narrowed (C-V29). See §2.3.

**Rating: NOT YET (unchanged from pass 1).** The machinery that runs a script is now very close to READY. Most of the
decisive pass-1 contradictions (the default opcode arm, arithmetic typing, the family-table initialiser, the
`cmdState+0x08` width, the `+0x15` writers and values, the unknown-tag pop, the `+0x44` byte) are settled on the pages.
What still decides the rating is G-1, the verb bodies: of about 1,886 callback functions, about 140 have gained a
one-sentence body description since pass 1, and most of those sentences name their callees only by call site.
By part: value stack and calling convention **READY** (was MOSTLY); variables **READY** (was MOSTLY); dispatch and
lifecycle **MOSTLY**, with a shorter list; request scheduling **MOSTLY**; interpreter **MOSTLY** (was NOT YET);
verbs **NOT YET**. See §4.
