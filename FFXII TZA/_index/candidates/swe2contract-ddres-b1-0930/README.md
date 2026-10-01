# DD residue closure, batch 1: 00-Engine-Core-Runtime (SWE2-CONTRACT, 2026-09-30)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`; package `SWE2CONTRACT-DDRES-B1-ENGINECORE-0930`. OPUS's
subagent ran the SWE2-CONTRACT lane for this batch. Input: the eight KEEP-PARTIAL pages of folder `00` in
[`dd-owner-read-0929/worksheet.tsv`](../dd-owner-read-0929/worksheet.tsv). All eight were clean in `git status` when
claimed.

Method, per page: every prose residue item in the worksheet's `gap_or_note` and `pending_markers` was searched in the
database first (`_index`, `_types`, other pages, `_experiments`, `_index/candidates`, the register). Answered items are
cited on the page with a dated note and a tier. Genuinely open items are registered as `RC-n` rows in the new `RC`
section of `OPEN-QUESTIONS.md`, and the page carries the same id as an open box. Where a cheap static measurement
settled an item, it was run and its control is in this folder. Missing template sections were filled from existing
evidence, and claim / evidence / tier tables added. Status words were not moved; status lines were made current.

## Receipts (static, shipping image `73461d08…`; all run at HEAD `0722d38df`) (SWE2-CONTRACT)

| control | what it settles | result |
|---|---|---|
| `console_codes_vs_mapref.py` | what the console's authored codes name | 599 of 601 codes equal `map_ref.bin`'s own pack for that field; shifted join 198 of 601; control entry 0 = `ous0101`, sequence = index + 1 for all 1,314 |
| `block_writer_disjoint.py` | `001F0AD0`'s 144 stores vs the 29 named settings | disjoint; controls C1 144, C2 29, C3 48, C4 21 all PASS |
| `rip_refs.py` (`rip_refs_02064ACC.out`) | the reader of `02064ACC` | one reader, `0022AE8F` in the field frame, into the tick pacer |
| `rip_refs.py` (`rip_refs_02CB8084.out`) | the integer word at block `+0xB4` | 16 references in 6 functions; the last-applied MSAA setting from `01DF0900` |
| `rip_refs.py` (`rip_refs_01F832B0.out`, `rip_refs_00369D30.out`) | the slot counters' base users; no pointer to the arena initializer | as recorded on the pages |
| `arena_ids.py` | whether any code registers arena id 10 | no; boot control 2–9, `0xB` PASS |
| `second_table_4a2_key.py` | the `+0x4A2` byte's writer, key and reader | K1–K3 PASS: `001C7940`, `mUseLinearTonemap`, `0018EEE0` → `+0x9A` |
| `log_channels.py` | the log call's channel range | 202 of 245 sites literal 0–3, none ≥ 4; 43 computed; 136 callers PASS |

The `rip_refs.py` windows, `[lo, hi)`, each re-run on 2026-09-30 at HEAD `7f2e5b34b` and byte-identical to the committed
output (added on SWE2-AUDIT-SPEC's review of this batch):

| output | window | note |
|---|---|---|
| `rip_refs_02064ACC.out` | `02064ACC 02064AD0` | the pacer wait word |
| `rip_refs_02CB8084.out` | `02CB8084 02CB8088` | the integer word at block `+0xB4` |
| `rip_refs_01F832B0.out` | `01F832B0 01F832C8` | the five slot counters and `01F832C4`; rip-relative only — the image-base-relative accesses are in `../swe2contract-ddres-b4-0930/counter_access.py` |
| `rip_refs_00369D30.out` | `00369D30 00369D38` (the default `lo + 8`) | the arena initializer as a data pointer |
| `rip_refs_block.out` | `02CB7FD0 02CB843C` | the tuning block, as re-measured on `what-the-console-tunes.md` |

## documented_rule.py after the repair (`documented_rule.out`, the rule as of FABLE's `48391d7f6`, conditions U and N) (SWE2-CONTRACT)

`TALLY PARTIAL=4 READY=3 READY-WITH-POINTER=1 of 8`, FAILS 0, self-test S PASS.

- **READY for OPUS's owner read (4):** `what-the-engine-fixes-at-boot.md` (READY), `Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md` (READY),
  `Startup-Data-Construction/generated-float-table-builders.md` (READY), `the-encoded-id-class-registry.md`
  (READY-WITH-POINTER: UQ-80's SUPERSEDED is on its status line; its status word is still REOPENED, trigger resolved).
- **Still PARTIAL (4), each on a registered, static row:** the 282-command console (RC-4), the event-slot panel (RC-5),
  the second console table (RC-6), what the console tunes (RC-7, RC-8).
- Three pages the worksheet typed as notes (event-slot panel, second console table, formatted log call) were completed
  as SYSTEM pages (player section, key addresses, call chain, modding notes, claim / evidence / tier table), so they
  declare no `note_kind`.

## Register rows (section `RC` of `OPEN-QUESTIONS.md`) (SWE2-CONTRACT)

| row | state | source |
|---|---|---|
| RC-1 | ANSWERED (static) | OPUS's census `rc1-static-census-0930`: 26 classes named by code; 4, 16, 22, 27 by no caller |
| RC-2 | ANSWERED (static) | OPUS's `rc2-arena-slack-0930`: slack outside every arena structure |
| RC-3 | ANSWERED (static) | OPUS's `rc3-boot-blocks-0930`: the oscillator table; a 0.5 MiB block nothing reads |
| RC-4 | OPEN, narrowed | OPUS's `rc4-capture-machine-0930`: entry states 1/6 have no direct writer; a derived-pointer census remains |
| RC-5 | OPEN | names and event ids the event-slot routes store; static first |
| RC-6 | OPEN | two code entries against `map_ref.bin` |
| RC-7 | OPEN | the MSAA word `01DF0900` |
| RC-8 | OPEN | cascade elements 3–7 |
| RC-9 | ANSWERED (static) | OPUS's `rc9-log-channels-0930` (`e65c88dee`): all 245 sites pass 0–3, none 4 |
| RC-10 | ANSWERED (static, negative with controls) | OPUS's `rc10-log-gates-0930`: no caller-side verbosity control |

None is routed to ASTRA; every open row names original-code work (2026-09-30 user rule: a row goes to ASTRA only after
naming the fact static or isolated execution cannot settle).

## Consumer check for the corrections in this publish (EVIDENCE-POLICY 4a/4b) (SWE2-CONTRACT)

corrects: `00-Engine-Core-Runtime/Developer-Tuning-Console/the-second-console-table.md` — the `+0x4A2` byte's writer
(scene-config loader `001C7940`, not a console arm), key (`mUseLinearTonemap`, not `ShadowValueB`) and reader
(post-process frame build `0018EEE0`, not a glyph-record builder).
corrects: `00-Engine-Core-Runtime/the-encoded-id-class-registry.md` — the misattribution "`00379CD0` … that this page
documents".
corrects: `00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md` — `001C2F40`'s "9 arms"
(propagating the contract's falsification pass 1, D8: 9 call sites, 4 arms).

Current consumers and their state:
- consumer `_types/fields.tsv` `PostProcessParamContext +0x4A2`: agrees (claims no meaning; names the write `001C977B`).
- consumer `_types/fields.tsv` `PostProcessFrameParams +0x09A`: agrees (copied from `+0x4A2` at `0018F31D`).
- consumer `17-Presentation-Rendering/Render-Command-List/postprocess-context-accesses.tsv`: agrees (lists `001C7940`
  as the writer).
- consumer `17-Presentation-Rendering/Post-Processing/CONTRACT-post-processing-subsystem.md` step 6: agrees.
- consumer `00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md` (the `ShadowValueB` reference
  count): agrees; it counts references, not the `+0x4A2` key.
- consumer `_index/GLOSSARY.md` (`ShadowValueB` as a setting name): agrees.
- consumer `21-RNG-And-Determinism/which-roll-is-on-which-generator.md` (documents `00379CD0`): agrees.
- consumer `00-Engine-Core-Runtime/Developer-Tuning-Console/CONTRACT-developer-tuning-console.md` (source of the D8
  counts): agrees.
- the three pages themselves: revised-here.

Regression: `second_table_4a2_key.py` rejects the old reading (K1 writer function, K2 key rule with a positive control
on the neighbouring store, K3 reader function and destination). verified at 0722d38df (run: 0722d38df), exit 0.

## Not done in this batch (SWE2-CONTRACT)

- The owner read and any status move: OPUS's.
- Uncited counts that could not be re-derived cheaply are marked on their page as unanchored (the event-slot page's
  ~13,800 path count), not removed.
