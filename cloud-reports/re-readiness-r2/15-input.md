# Reconstruction readiness, pass 2 — `FFXII TZA/15-Input/`

| | |
|---|---|
| Stream | R2 (reconstruction readiness, pass 2), per [`docs/cloud-briefs/re-readiness-r2.md`](../../docs/cloud-briefs/re-readiness-r2.md), part A |
| Lane | FABLE (cloud session r2-16) |
| Pass 1 | [`cloud-reports/re-readiness/15-input.md`](../re-readiness/15-input.md) (2026-10-01, rated **MOSTLY**) |
| Date | 2026-10-03 |
| Snapshot | this repo's text snapshot (synced from XIIOnline `f9d9053b9`); no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every verdict quotes or paraphrases a page, with its location. |

Citation form: `page:line`, with the path relative to `FFXII TZA/`. Pass 1 limited "not stated" to the 15-Input pages
and the one 16-UI section they defer to. This pass reads the current 15-Input pages and the register
(`_index/OPEN-QUESTIONS.md`). It also follows pass-1 gaps to other systems' pages when a page there now carries the
answer. In that case the verdict says the 15-Input page lacks the pointer (class DOC).

Pages re-read: `15-Input/README.md`, `CONTRACT-input-subsystem.md`, `how-a-gamepad-becomes-a-controller-object.md`,
`Input-Stack/input-stack-device-channel-and-bindings.md`, `Binding-Profiles/CONTRACT-binding-profiles.md`,
`Binding-Profiles/binding-profiles-remapping-and-control-state.md`,
`Binding-Profiles/keymap-ini-file-format-and-default-controls.md`, `Input-Name-Registry/CONTRACT-input-name-registry.md`,
`Input-Name-Registry/the-input-name-registry-and-channel-aliases.md`,
`Gameplay-Capability-Policy/capability-inhibition-policy.md`, `Modal-Toggles/r2-force-fight-toggle.md`. Pages outside
15-Input that were followed are cited where used.

---

## 1. Summary

**Pass-1 gaps: 52** (18 page-stated G-L, 7 G-A, 6 G-B, 5 G-C, 5 G-D, 2 G-E, 9 contradictions G-*x).

| verdict | count | ids |
|---|---:|---|
| **CLOSED** | **10** | G-L7, G-B5, G-B6, G-C1x, G-C2x, G-C3x, G-C4x, G-C5x, G-C6x, G-C7x |
| **NARROWED** | **15** | G-L2, G-L6, G-L9, G-L12, G-L16, G-A3, G-A4, G-A5, G-B3, G-B4, G-C4, G-C5, G-D2, G-E1, G-C8x |
| **OPEN** | **26** | G-L1, G-L3, G-L4, G-L5, G-L8, G-L10, G-L11, G-L13, G-L14, G-L15, G-L17, G-L18, G-A1, G-A2, G-A6, G-B1, G-B2, G-C1, G-C2, G-C3, G-D1, G-D3, G-D4, G-D5, G-E2, G-C9x |
| **WRONG-IN-PASS-1** | **1** | G-A7 |

The 41 gaps still OPEN or NARROWED, by the class of their remaining part:

| class | OPEN | NARROWED |
|---|---:|---:|
| STATIC | 20 | 9 |
| RUNTIME | 5 (G-L1, G-L3, G-L4, G-L8, G-L17) | 3 (G-L2, G-L9, G-L16) |
| DATA | 0 | 1 (G-A4) |
| DOC | 1 (G-C9x) | 2 (G-C8x, G-D2) |

**New gaps: 12**, of which **DOC 8**, **STATIC 4**, RUNTIME 0, DATA 0. Seven of the DOC gaps are stale text: a
contract or section that still lists as open something another page or the register has since answered. The other
DOC gap and the four STATIC gaps are disagreements between pages, or callees that are named but not described.

**Rating: MOSTLY (pass 1: MOSTLY).** Unchanged. The register closed several rows behind pass-1 gaps (AU-4, GG-1, C-7,
DM-1, DM-3, the binding contract's §14 items), and three of pass 1's contradictions were corrected at the bytes on
2026-10-01. The two whole-function blockers are only narrowed, not closed: the arbiter's decision logic, and the
pad and backend device bodies. See §4.

