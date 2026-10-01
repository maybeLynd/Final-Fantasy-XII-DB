# SECTION-11/12 overlay: per-token drop dispositions (SWE2-FRONTIER, 2026-09-26)

Gate file for `overlay-publication-plan.md` ruling 2, produced by the named publisher before the
S11/S12 commits. Census: `overlay_drop_census.py` run 2026-09-26 — four carrier files, 57 dropped
address tokens, 0 dropped EXP ids, 0 dropped invariant ids. Reviews behind the publish: OPUS type
reviews (`section11-opus-type-review.md`, `section12-opus-type-review.md`, ACCEPT), FABLE semantic
review (`section11-12-fable-semantic-review.md`, ACCEPT), AUDIT-SPEC first-line audit
(`FABLE-REQ-AUDITSPEC-FIRST-LINE-AUDIT-OF-UPDATES-11-AND-12`, ACCEPT — every cited original site
decoded real).

Every dropped token below was read against HEAD and the worktree overlay. Method note: the
overlays condensed whole `asm` listings into prose and moved instruction-site detail into the
committed evidence bundles (`continuation-section11-script-resume/original_disassembly.txt`,
`continuation-section12-actor-request-waits/original_disassembly.txt`, `opcode_dispatch_lengths.tsv`,
and the actor-storage/actor-manager access TSVs). "Restated" means the claim survives in the
published text; site-level bytes live in the pinned bodies that ride the commit.

## `01-Script-VM-Native-Bridge/CONTRACT-interpreter-core.md` (S11+S12, 12 tokens)

| token | disposition |
|---|---|
| `0025E59D` `0025E5A9` `0025E5AD` | **restated** — decoder entry listing condensed; the mechanism survives ("opcodes >63 still reach an opcode-indexed length lookup"; "`0x47` itself is length-1"; the guard-page control faulting at `0025E5AF` reading PC+2). Listing bytes pinned in `original_disassembly.txt`. |
| `0025E5A1` | **restated** — the saved-opcode claim survives as "`0025E613` performs the common length advance" (reload of the saved opcode); site pinned in evidence. |
| `0025E5D4` | **restated** — V-4's out-of-range `ja` target claim survives in prose. |
| `0025E5EA` | **restated** — the own-length-lookup fallthrough claim survives generalized. |
| `0025E62A` `0025E631` `0025E641` `0025E644` | **restated** — epilogue listing condensed into I-4 (`0025E60A` stop request vs `0025E613` advance-only); the per-opcode lengths are the committed `opcode_dispatch_lengths.tsv`. |
| `0026121A` `002618A8` | **restated** — dispatch-table cells (`0x2A..0x2C`, `0x51`/`0x60`) moved to `opcode_dispatch_lengths.tsv` in the riding evidence folder. |

## `01-Script-VM-Native-Bridge/CONTRACT-script-to-native-bridge.md` (S11, 21 tokens)

| token | disposition |
|---|---|
| `0025B400` | **restated at finer grain** — the kind-4 service is now cited as `0025B41D cmp byte [entry+0x14], 4` → `0025B428`–`0025B435` deadline arithmetic. |
| `0025DF00` | **restated elsewhere** — the runnable-request driver remains cited in `CONTRACT-interpreter-core.md` (`0025DF00` selects the request → `0025E4C0` executes) and in the section-11 evidence. |
| `00262440` `00268094` | **restated** — the slot-fill claim survives in the entry-layout prose (`+0x00` union / `+0x16` visit-park marker). |
| `00263450` `0026345F` `00353D10` | **restated** — the "no encoded kind" sentinel and its peek reader survive as the kind-sentinel prose; callee interiors pinned in `original_disassembly.txt`. |
| `00267F78` `00267F9D` `00267FC0` `00267FE4` `00268100` `00268124` `0026812C` `0026812E` `00268140` `00268185` | **restated / consolidated** — the operand-kind byte `+0x44` claim survives generalized ("descriptor byte0 vs a separate typed-load selector; complete enum remains unresolved" — honestly narrowed, not lost); the PUSHV six-arm jump table `00267FC0` remains cited in `scriptvm-verb-dispatch-and-parameter-encoding.md` and `script-variables-and-their-storage-classes.md`. |
| `0026CC0D` | **restated elsewhere** — `ActorManager_BindLoadedDefinitionPayload`'s `+0x15` init store survives in `actor-manager-slot-accesses.tsv` row 135. |
| `00270000` | **restated** — the no-compare census claim survives; the sweep bound lives in the evidence run manifests. |
| `003DBDC0` `003DBE0C` | **restated** — the `record+0x58` record-tick / arming claim survives as the kind-4 deadline-arithmetic row. |

## `01-Script-VM-Native-Bridge/Native-Command-Lifecycle/native-command-lifecycle.md` (S11, 5 tokens)

| token | disposition |
|---|---|
| `0025F7B2` `00261CC0` | **restated** — the enqueue-arm zeroing claim survives in prose; the store sites are pinned in `original_disassembly.txt`. |
| `0026230B` | **restated** — the keep-running store ("poll returned bit 0 set → `state[0x15]=1`") survives at line ~371. |
| `00266624` `0026CC0D` | **restated elsewhere** — the two `+0x15` init stores survive in `actor-storage-record-accesses.tsv` (row 1079) and `actor-manager-slot-accesses.tsv` (row 135). |

## `04-Actor-Entity/the-field-runtime-pass.md` (S12, 19 tokens)

| token | disposition |
|---|---|
| `0025E03B` `0025E040` `0025E045` `0025E04B` `0025E04F` `0025E053` | **restated** — the find-or-block listing condensed; the wait-slot `+0x14`/`+0x27` blocked-mark claims survive in the new gate table (rows 4–7). |
| `0025E069` `0025E08A` `0025E08F` `0025E09F` `0025E0A9` `0025E0B0` | **restated** — the four wait-gate rows survive in the new decision table (`003DB640` channel bit, `00267420`/`002674B0` ordered lists, `003DC050` absent-notification, `003DB2A0` blocked-path removal — all still named). |
| `0025E0D3` | **restated** — the `InterpretBytecode(slot, record, waitslot)` call survives in the drive-loop prose. |
| `0026747D` `00267494` `003DB646` `003DB649` `003DC03A` `003DC0AB` | **restated** — callee-interior site addresses; the callee functions remain named in the gate table, interiors pinned in the section-12 `original_disassembly.txt`. |

**Status: every dropped token is disposed — none silently. No token needed a text restore:** the
two overlay files kept or generalized every claim HEAD carried, with instruction-site evidence in
the committed bundles. Two claims were honestly narrowed (`+0x44` enum marked unresolved; the
"first frame" narrowing is the section-04 analogue already reviewed). Spot-check basis: all 57
tokens read at HEAD and in the worktree on 2026-09-26; clusters share a disposition only where the
removed text was a single contiguous block.
