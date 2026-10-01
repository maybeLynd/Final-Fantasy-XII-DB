# Goal revision — modding-grade → reconstruction-grade → parity-certified

**Sealed 2026-09-08.** Authority for the expanded goal is
[`../../../RECONSTRUCTION-CHARTER.md`](../../../RECONSTRUCTION-CHARTER.md).
This document is the audit that produced the revision: what the project already satisfied, what had
to change, and the dependency-aware roadmap from here.

> **The database is not restarted, replaced, or migrated.** Its evidence standard, tier hierarchy,
> dispositions, indexes, audit history and tooling are the reason the expanded goal is reachable at
> all. What changed is the **completion bar**, not the foundation.

---

## 1. What the goal was, and what it now is

**Was:** *"a complete, evidence-backed reference to how FFXII TZA actually works at the native-code
level, written so a modder can open any folder and learn a system well enough to change it
correctly."*

**Now:** that standard is retained **verbatim as Level 1**, and two levels are added above it.

| level | name | bar |
|---|---|---|
| **L1** | **MODDING-GRADE** | What the system does · what owns it · where the code/data/scripts/resources live · what state matters · what regenerates or overwrites it · what native transitions exist · where intervention is safe, where dangerous · what downstream behaviour changes. **This is the existing standard and it is not weakened.** |
| **L2** | **RECONSTRUCTION-GRADE** | L1 **plus** enough to reproduce the behaviour independently: semantic interface, parameters, return semantics, types, layouts, fields, ownership, lifetime, init, destruction, callers, callees, globals, state machines, pre/postconditions, invariants, side effects, scripts, resources, RNG, serialization, timing, failure paths, edge states, runtime evidence, a behavioural contract. |
| **L3** | **PARITY-CERTIFIED** | Independently implemented and compared against the original within explicitly stated parity dimensions, with remaining untested state space and known differences tracked. |

**Modding does not become a side effect of reconstruction.** L2 knowledge makes modding *more*
powerful — it is what lets a modder answer "if data and script cannot achieve this, what must be
extended or replaced?" — so §25 of the charter is a first-class requirement, not a courtesy.

---

## 2. The correction this audit makes to my own previous assessment

On 2026-09-08 an earlier pass in this session wrote, in `PROGRAM-STATE.md`, that the database was
*"breadth-complete and depth-shallow"* and framed it as **one leg of three**, with the implication
that the modding standard had been superseded.

**Both framings were wrong and are withdrawn.**

- **The methodology is already reconstruction-grade in the places that are hardest to retrofit.**
  `EVIDENCE-STANDARD.md` already defines an 11-tier hierarchy **including tier 10 runtime evidence**,
  a banned-evidence list, falsification duty, a status lifecycle with reopening triggers, permanent
  correction records, positive controls on absence claims, and noise-floor requirements. That is the
  expensive part of a reconstruction-grade standard and it exists.
- **The disposition policy already anticipates charter §6.** `COMPLETION-PLAN.md` §3 argues, in its
  own words, that citing 11,836 generic-shape functions *"would satisfy the metric and betray the
  mission"*, and defines **A individually explained / B class-explained / C dispositioned** with a
  stated bar for each. The charter's A/B/C are the same three. Only **D** was missing.
- **What is genuinely shallow is narrower than "depth"**: type recovery for game structures,
  behavioural contracts, and runtime validation. Those three, not the documentation as a whole.

---

## 3. Gap analysis against the expanded goal

### ALREADY SATISFIED — do not rebuild

| requirement | where it already lives |
|---|---|
| Provenance, confidence, supersession (§12) | `EVIDENCE-STANDARD.md`: tiers 1–11, *Status lifecycle*, *Corrections are permanent record*, *The GFZ itself is a claim* |
| Runtime evidence as a recognised tier (§16) | tier 10, already defined — **unused, not absent** |
| Do not confuse classification with understanding (§5, §29) | `COMPLETION-PLAN.md` §3, in almost the charter's words |
| A/B/C completion dispositions (§6) | `COMPLETION-PLAN.md` §3, frontmatter-declared, counts reproducible |
| Automation of high-volume research (§18) | ~40 scripts in `Tools/analysis-kit/gfz-scripts/` |
| Instrument-failure discipline (§16 cross-validation) | `RULES.md` *Instrument findings — how measurement goes wrong*; positive-control rule |
| Cross-linking, first generation (§11) | `ADDRESS-INDEX.md`, `CALL-CHAINS.md`, `NAME-EQUIVALENCES.tsv`, `ASSET-FORMATS.md`, `GLOSSARY.md` |
| Original vs extension separation (§24) | the database describes the original; `XIIOnlineNet`/`ENetServer` are separate trees |

### PARTIALLY SATISFIED — extend, do not replace

| requirement | what exists | what is missing |
|---|---|---|
| Maturity levels (§2) | modding-grade is the de facto standard | L2/L3 were undefined — **now defined, §1 above** |
| Readiness ladder (§5) | `status:` = DOCUMENTED / PARTIAL / REOPENED / AUDITED | no rung for semantic identity, signature, type, dependency, runtime, contract, reconstruction, parity |
| Coverage metrics (§13) | `COVERAGE-DIMENSIONS.md` (built 2026-09-08) covers discovery, identity, citation, callgraph, globals, contracts, runtime | no type, script/opcode, state-machine, resource-correlation, implementation, differential or parity dimensions |
| Global read/write knowledge (§10) | `Tools/work/h78/rip_data_refs.tsv`, 164,489 rows; **`globals_index.py` built this block** | not cross-linked *into* documents; 96.4 % of globals still explained by nothing |
| Cross-linking (§11) | address/call/name indexes | no type ↔ field ↔ global ↔ state-machine ↔ script ↔ resource ↔ contract ↔ parity graph |
| Full-game coverage (§15) | 26 categories, all populated | depth per category varies by an order of magnitude |

### MISSING — must be created

| requirement | note |
|---|---|
| **Behavioural contracts (§9)** | **0 of 211 documents.** No template, no linter, no coverage dimension. The single largest gap. |
| **Type recovery as a completion dimension (§8)** | Phyre's reflected schema exists (680 members / 246 classes). **FFXII's own structures have no equivalent** — 680 offset literals scattered through prose, never collected. |
| **Disposition D — explicit unresolved exception (§6)** | A/B/C exist; D does not. Without it, an unresolvable operation has nowhere to live except silence. |
| Reconstruction-grade function record (§7) | no representation for signature, pre/post, invariants, allocations, threading, edge states |
| Source reconstruction (§20) | no tree, no architecture |
| Differential/parity framework (§22, §23) | none; the existing `ENetServer/scratchpad` suites test the multiplayer DLL, not parity |

### NEEDS REVISION — documents that would otherwise contradict each other

| document | change |
|---|---|
| `README.md` | goal statement names only the modding standard |
| `COMPLETION-PLAN.md` | *"what done means"* stops at the 30-pass final audit; needs L2/L3 criteria and disposition D |
| `PROGRAM-STATE.md` | contains the withdrawn "one leg of three / depth-shallow" framing (§2 above) |
| `RECONSTRUCTION-CHARTER.md` | written earlier this session; implies modding is displaced |
| `.claude/skills/goal/SKILL.md` | carries an 11-rung ladder; the charter's is 13 rungs |

### NEEDS NEW TOOLING

`contract_coverage.py` · a type/struct store and `types_index.py` · runtime capture harness over the
already-wired Cheat Engine / Ghidra-debugger MCP servers · differential harness · cross-link graph
builder. **None requires abandoning an existing tool.**

---

## 4. The revised completion bar

**Database (goal 1).** Every behaviourally meaningful authored operation ends in exactly one of:

- **A — individually understood**, at a depth proportionate to its role;
- **B — proven member of an understood semantic family**, with the shared shape, the enumeration
  method and a reproducible count stated;
- **C — proven implementation machinery** (compiler, runtime, plumbing, thunk, template, vendor),
  with the upstream named and the boundary stated;
- **D — explicit unresolved exception**, *visible in coverage rather than absent from it*.

**The disqualifying justification is now named.** *"This function probably isn't interesting to
modders"* is no longer sufficient. The question is:

> **Could ignorance of this operation prevent us from reproducing FFXII correctly?**
> If **yes** or **unknown**, it stays on the reconstruction frontier.

**Major systems additionally require**, for L2: reconstruction-grade types, relationships,
behavioural contracts, runtime evidence, and script/data/resource integration.

**Reconstruction (goals 2–3).** An increasing portion of behaviour implemented independently and
validated against the original, until the integrated runtime reproduces required behaviour without
relying on unknown original implementation for reconstructed systems.

---

## 5. The thirteen-rung ladder

Replaces the eleven-rung version written earlier this session.

```text
DISCOVERED → CLASSIFIED → SEMANTICALLY IDENTIFIED → SIGNATURE RESOLVED → TYPE RESOLVED
→ DEPENDENCIES RESOLVED → BEHAVIORALLY UNDERSTOOD → RUNTIME VALIDATED → CONTRACT READY
→ RECONSTRUCTION READY → IMPLEMENTED → DIFFERENTIAL TESTED → PARITY CERTIFIED
```

**Where the database actually sits.** Almost everything documented is at **BEHAVIORALLY UNDERSTOOD**
or below. **RUNTIME VALIDATED** is reached by 13 of 211 documents (6.16 %). **CONTRACT READY** is
reached by none.

---

## 6. Parity dimensions — tracked separately, never as one word

```text
STRUCTURAL · CONTRACT · STATE-TRANSITION · CALCULATION · RNG · SERIALIZATION
TIMING · INTEGRATION · PRESENTATION · EDGE-CASE · FULL SUBSYSTEM
```

"Mostly works" is not a parity status. Record what was tested and what was not.

---

## 7. Roadmap — ten tracks, with real dependencies

Tracks run in parallel; the arrows are hard dependencies, not scheduling preferences.

```text
A  DATABASE BREADTH            ──┐
B  SEMANTIC DEPTH              ──┼──► G  BEHAVIORAL CONTRACTS ──► H  SOURCE RECONSTRUCTION
C  TYPE RECONSTRUCTION         ──┤                                      │
D  CALL/DATA/STATE RELATIONS   ──┤                                      ▼
E  SCRIPT + RESOURCE INTEGRATION ─┘                              I  DIFFERENTIAL / PARITY
F  RUNTIME VALIDATION ───────────────────────────────────────────►      │
                                                                        ▼
                                                            J  INTEGRATED RUNTIME
```

| track | state | next concrete action |
|---|---|---|
| **A** breadth | strongest track; 26/26 categories populated | continue `coverage_balance.py` ordering, but no longer the default block |
| **B** semantic depth | 4.43 % of 28,661 authored functions carry a semantic name | apply disposition **B** at family scale — the 11,836 generic-shape functions are the volume |
| **C** type reconstruction | **store built 2026-09-08** — `_types/`, `types_index.py`, validator. 1 type, 40 fields, 99.9 % of `GameSettingConfig` declared, 0 errors | seed the next types: input binding record, music run, post-process context |
| **D** relationships | `globals_index.py` shipped this block | cross-link globals into documents; 96.4 % explained by nothing |
| **E** script + resource | 1,115 EBP scripts censused; 18/48 formats | continue `ASSET-FORMATS.md` ordering |
| **F** runtime validation | **harness built 2026-09-08** — `runtime_probe.py`, read-only, two mandatory controls, refusal path tested. `EXP-001` designed, **PENDING**. Coverage unmoved at 13/211 (6.16 %) | **run `EXP-001`** — needs `FFXII_TZA.exe` launched, then one command |
| **G** contracts | **template + 1 contract at `CONTRACT READY`** (`GameSettingConfig`), 1 of 211 systems (0.47 %) | the remaining three near-ready systems; none can pass the readiness gate until `F` runs |
| **H** source reconstruction | not started | first pilot after G produces two contracts |
| **I** differential/parity | not started | harness after H |
| **J** integrated runtime | not started | far |

**Critical path to the first parity-certified subsystem:** `C` and `F` are the true blockers.
A contract without types is prose, and a contract without runtime evidence cannot be trusted at
§26's gate.

### First reconstruction-ready candidates

Chosen because each already has exact types, offsets, formulas and consumers written down — they
need **types formalised and runtime confirmation**, not new discovery.

1. **`GameSetting.ini` config object** — 31 settings, full key/value schema, preset matrix, defaults,
   consumer chain, and a fully-read two-mode consumer (`FrameLimit`).
2. **Input binding profiles** — record layout, translator formula, active-low mask, analog scaling.
3. **The music field→track table** — exact packed layout, stride, ladder walk, and the progress
   variable that keys it.
4. **The Lua loader chain** — every function in the chain identified, mode argument read, header
   fingerprint recovered.

**None is runtime validated. All four are `BEHAVIORALLY UNDERSTOOD`, none is `CONTRACT READY`.**

---

## 8. What this revision deliberately did not do

- **No schema migration.** The Markdown-plus-TSV model represents everything the database currently
  knows. It cannot represent contracts or types well — so those get *new* stores, rather than the
  existing corpus being converted. Charter §3's rule (*"do not migrate merely because another
  architecture would also work"*) is respected.
- **No renaming or reorganisation of existing documents.**
- **No new percentage.** `COVERAGE-DIMENSIONS.md` still emits no composite score.
- **No claim that any subsystem is reconstruction-ready.** Four are named as *candidates*, and the
  gate they fail — runtime validation — is stated.
