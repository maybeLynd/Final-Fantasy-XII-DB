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

---

## 2. Pass-1 gaps

Abbreviations for the 15-Input pages: **SUB** = `15-Input/CONTRACT-input-subsystem.md`; **PAD** =
`15-Input/how-a-gamepad-becomes-a-controller-object.md`; **STK** =
`15-Input/Input-Stack/input-stack-device-channel-and-bindings.md`; **BPC** =
`15-Input/Binding-Profiles/CONTRACT-binding-profiles.md`; **BPR** =
`15-Input/Binding-Profiles/binding-profiles-remapping-and-control-state.md`; **KMI** =
`15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md`; **NRC** =
`15-Input/Input-Name-Registry/CONTRACT-input-name-registry.md`; **NRS** =
`15-Input/Input-Name-Registry/the-input-name-registry-and-channel-aliases.md`; **CAP** =
`15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md`; **R2T** =
`15-Input/Modal-Toggles/r2-force-fight-toggle.md`; **REG** = `_index/OPEN-QUESTIONS.md`.

The class column applies to what is still missing (OPEN or NARROWED); it is blank for CLOSED and WRONG-IN-PASS-1.

### 2.1 Gaps the pages state themselves (pass 1 §2.1)

| id | verdict | evidence (quote + `page:line`) | still missing | class |
|---|---|---|---|---|
| G-L1 no live frame order | OPEN | "**Anything live.** No frame order here has been observed in a running process. Readiness is `CONTRACT READY`, not `RECONSTRUCTION READY`." (SUB:415-416) | any live capture of the §3 order | RUNTIME |
| G-L2 GG-1 reader placement | NARROWED | Register GG-1: "**ANSWERED 2026-09-28 (SWE2-FRONTIER ruling …): 50 of 51 readers statically placed, and `003C87B0` is placed on its arbiter and world-tick paths. The residue is bounded and owned: `003C87B0`'s paths through `00254B40` and the widget message-1/12/18 handlers are runtime-only**" (REG:3349, status cell) | `003C87B0`'s placement on its `00254B40` and widget message-1/12/18 paths; the live values of the `0022AB83` gates ("the game's MXCSR and the accumulator's live values are unobserved", SUB:348-349). SUB's own GG-1 bullet is stale (new gap N1) | RUNTIME |
| G-L3 GG-3 residue | OPEN | "**Not established:** the real handler's behaviour inside a live widget tree, and which frames reach the walk in play." (SUB:394-395) | unchanged | RUNTIME |
| G-L4 assignment never observed live | OPEN | "**Not validated:** assignment, the conflict swap, publication, the pair swap, the three-bank poll order, and channel timing. **No experiment has driven `00198A00` or observed `01F80130` change.**" (BPC:486-487) | unchanged | RUNTIME |
| G-L5 translator and assigner not reimplemented | OPEN | "One operation of the write path is done; assignment (`00198A00`) and the translator (`00197160`) are not, and nothing here has been observed in a live process." (BPC:655-657) | a reconstruction and differential test of `00197160` and `00198A00` | STATIC |
| G-L6 pad polls, `EnumObjects`, mouse/keyboard arms, removal | NARROWED | The mouse arm is now read: `00797460` "entered from `00796230` + 0x3C", which calls DirectInput slots `+0x58` (with `01CC7130`), `+0x68` (with qword `02EA5248` and 6) and `+0x38` (PAD:260). The pad polls are named, but only on KMI: "The XInput and Steam polls fill slots 0–15 only … The DirectInput poll alone copies `rgbButtons[16]` into slot 16" (KMI:884-886). The record `_index/candidates/dm2-code27/README.md` gives their addresses (`007A2140`, `007A1CD0`, `007A1A50`). | PAD still says "**Not read:** the mouse and keyboard arms; each kind's poll; the `EnumObjects` callback; what happens on removal." (PAD:123) and "Whether the duplicates cause doubled input depends on each kind's poll, which is still not read." (PAD:243). Not stated: the polls' stick and trigger stores; the `EnumObjects` callback; what a removed pad's poll does; whether duplicate Steam objects double input. PAD lacks a pointer to KMI:884-886. | STATIC |
| G-L7 AU-4 blocks 2 and 3 | CLOSED | Register AU-4: "**ANSWERED 2026-09-26 (OPUS), STATIC: three blocks of three `InputBindingRecord`s, and the stated end is a record's axis table, not a short third block.** … Blocks 2 and 3 therefore hold three records each, like block 1." (REG:492) | — (BPR's own AU-4 section is stale, new gap N7) | |
| G-L8 UQ-146 dangling stack return | OPEN | Register UQ-146: "**SUPERSEDED 2026-09-27 (FABLE …) under the runtime rule; live carrier FABLE-REQ-ASTRA-UQ146-IN-PROCESS-FORMATTER-READ.**" (REG:2860); KMI: "What remains is a property of the installed `ucrtbase.dll`, not of this executable, and only an in-process observation can settle it." (KMI:1022-1023) | whether `ucrtbase`'s frames clobber the buffer before the `%s` is read | RUNTIME |
| G-L9 UQ-147 leader / mode-1 counterpart | NARROWED | Register UQ-147: "the mode-1 counterpart is the Esper summon sequence's acting member (+0x5AD5 on the battle-state block page, writer and clearer named). Whether initialized gameplay reaches the null-leader state is live and carried by FABLE-REQ-ASTRA-LEADER-STATS-NULL" (REG:2861). CAP: "So a unit that `003272A0` returns always has a non-null `+0x698`." (CAP:1185) | the live check; CAP lists the routes its typed census cannot see (CAP:1189-1192) | RUNTIME |
| G-L10 name-registry integration | OPEN | "**One of the five is reconstructed**; the other four are understood and not reimplemented." (NRS:331-332); "**Still not reconstructed**, which is a different thing" (NRC:302) | reimplementation of the destructor, the two lookups and the enumerator | STATIC |
| G-L11 no analog names | OPEN | "**Anything about axes.** Every name recovered is a button or a key." (NRS:402) | unchanged; the axis indices exist only as the kind-3 `subKind` of binding records (KMI:952) | STATIC |
| G-L12 `0023C5C0`'s screen, command `0x2CA1`, row 0 | NARROWED | The screen is now identified on another page: the Controls pane's record walk sends "kinds 1-2 -> `0023C5C0` (key-bind rows)" (`19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md:203-207`) | BPR still says "Which screen `0023CE10` builds, and what `0x2CA1` and row 0 are, are not read." (BPR:790-791). Not stated anywhere read: what command `0x2CA1` and row 0 are. BPR lacks the pointer. | STATIC |
| G-L13 `001967D0` with a 1–3 code | OPEN | "what it then does with a 1–3 code was not read in this pass." (KMI:251-252) | the body after the `(code - 1) < 3` test | STATIC |
| G-L14 `001E0C10`'s eleven callers | OPEN | "Its eleven callers (`00276AF6` … `00393C6E`) were not each read." (KMI:902-903) | unchanged | STATIC |
| G-L15 mouse wheel channel; accumulator consumers | OPEN | "the device driver was not read to confirm channel 3." (BPR:1062) | the mouse device's channel 3; any reader of `[01F7FFE0]+0x0C` / `+0x10` (none is named) | STATIC |
| G-L16 rumble cut-off in wall time | NARROWED | Still "The update rate per second is not read here." (BPR:365). The poll rate is now stated per frame: "The poll runs once per dispatcher frame in modes 2, 3 and 5" (STK:270). SD-9 adds that the worker deadline "paces nothing" (STK:532-534). | the dispatcher's frames per second in play. KMI ties `FrameLimit` 30/60 to the frame base (KMI:454-456), but no page links that to the input poll | RUNTIME |
| G-L17 meaning of `+0x3A` bits | OPEN | "The reading of the bits as \"battle menu\" and \"menu or locked\" comes from the slot names, not from a live observation." (KMI:939) | live confirmation | RUNTIME |
| G-L18 UQ-152 bound | OPEN | Register UQ-152 is ANSWERED (REG:2866), but its bound stands: "**An indirect call from inside a thread cone into one of the four would not appear here.**" (R2T:515) | an indirect-call resolution over the thread cones | STATIC |
