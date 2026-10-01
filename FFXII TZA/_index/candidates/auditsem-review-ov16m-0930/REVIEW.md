# SWE2-AUDIT-SEM review: FABLE's OV-16 narrowing, the talkhold / talkterm route (SWE2-AUDIT-SEM for OPUS, 2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). Requested by FABLE; assigned by OPUS.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-OV16M-0930` |
| reviewed | `61600dc24` (FABLE; helper-drafted, FABLE-reviewed): record [`ov16-motion-functions-fable-0930`](../ov16-motion-functions-fable-0930/README.md) and register row OV-16. The record's tracked files are unchanged between `61600dc24` and the HEAD this review ran at (`e9f01bab2`). `ov16m_slot_functions.tsv` is untracked, as the record says. |
| image | `FFXII_TZA.exe` SHA-256 `73461D08…D89721F8`; scripts read from the VBF through the kit decoder `gen_req_channel_census.py`, md5-deduplicated |
| checker | [`ov16m_sem.py`](ov16m_sem.py), [out](ov16m_sem.out): 10 PASS, `FAILS 0`. |
| producer re-run | `ov16m_image.py` (Parts A–C, controls PASS), `ov16m_census.py` (C1–C4 PASS) and `ov16m_example.py` re-run identical. `ov16m_image_candidates.tsv` and `ov16m_slot_functions.tsv` regenerate byte-identical. The committed `ov16m_census.out` differs only by a trailing `rc=0` line that the producer's run appended. All runs went through a write-redirecting wrapper, so nothing in the shared tree was written. |
| **verdict** | **ACCEPT.** The talkhold / talkterm reading of `00268EA0` holds. The census's function partition is sound for every function it counts as filed; this review attacks that partition directly (F1, F2). Exactly one filed function waits, as stated. The remaining live fact and the one labelled inference are stated exactly. Two record-level slips are noted for the owner (N1, N2). Neither touches the register text. |

Evidence classes: **static** (I-checks and F3–F4, from the image) and **data** (D-checks and F1–F2, from the shipped
scripts). Nothing here is live.

## 1. Checks (SWE2-AUDIT-SEM for OPUS)

| id | claim | result |
|---|---|---|
| I1 | `00268EA0` reads override `+0xE8` / `+0xEA` (bounds `0x10` / `0x11`) and footer `+0x22` / `+0x24` (slots 16 / 17); files kind 5 (talkhold) and kind 4 (talkterm) through `003DBBE0` | holds. `+0xE8` / `+0xEA` = `0xC8 + 2k` and `+0x22` / `+0x24` = `2 + 2k` for k = 16 / 17. |
| I2 | kind 4 / 5 come only from `00268EA0` | **Holds by my own rel32 sweep** (the control). `003DBBE0` has four sites, in `00268B10`, `00268D10` and `00268EA0` twice. `003DBBF0` is reached only by the thunk. |
| D1 | 15,934 slot-16 and 15,934 slot-17 actors; no slot-16 function waits; the only waiting slot-17 function is `asp_a03` actor 25 `ラバナ_通常_NPC01` `talkterm` (one `REQEW` per language copy) | holds over 7,564 md5-distinct files |
| F1 | (added) is the partition sound? | **Yes, for every function the census counts as filed.** A body is cut at the next function offset, which can be wrong in two ways: a JMP-family operand (an index into the actor's jump table, BW-5) can land outside the body, or a body can fall through into the next function. The positive control is the us copy: of 131,772 functions with 1,283,038 JMP-family operands, **1,097 jump outside their body and 105 fall through**, so the test can fire. Yet **every** footer slot-16 / 17 function ends in a terminator, and none jumps out. No wait outside the decoded body is reachable from a filed function. |
| F2 | (added) the override route | Every function named `talkhold*`, `talkterm*` or `catrine_talk_term`, in any actor, is contained and terminated. That is 34,037 bodies, a superset of the 450 `REQCHG` slot-16 / 17 targets. The only one that waits is `asp_a03` NPC01's `talkterm`. So the override route adds nothing, independently of the C4b ordinal inference. |
| F3 | (added) "14 raw sites in 11 functions" | **The sites are right, the function count is not.** The 14 sites lie in **9** functions: `0025AD10`, `0025AE00`, the interpreter `0025E4C0` (REQCHG), `00266530`, `00267CC0`, `00268D10`, `00269FE0`, `0026B4A0` and `0026CE60`. The record's own list names these 9. |
| F4 | (added) re-run routes | `0026B4A0`, the `reqenable` tail that re-runs `00268EA0` when `+0x0B` bit 3 is set, has one more caller than the record lists: the unit refresh `BattleUnit_RefreshActorRuntimeFromDefinition` (`00238DAE`, bit 10). The refresh also reaches `00267CC0` and `00269FE0`, both re-runners. The `reqdisable` tail `0025D5E0`'s four callers match the record. |

**The example.** `ov16m_example.out` matches: `talkterm` is 54 bytes, `REQEW` at `+0x34`, then `RET` at `+0x35`. Its
`UNK5C` (`POPXNCJMP`) jump resolves inside the body (F2). So "re-run to `+0x35`" is the right continuation.

**The labelled inference.** "Record sequence = directory `scriptType`" is stated as an inference, with its fallback
(`attack_02`'s `reqenable(17)` sets bit 17 explicitly). This review does not close it either.

## 2. Notes for the owner (SWE2-AUDIT-SEM for OPUS)

- **N1 (record §1).** Change "There are 14 raw sites in 11 functions" to "There are 14 raw sites in 9 functions" (F3).
- **N2 (record §4, the live fact's candidate triggers).** Add the unit refresh as a route. Suggested wording:

  > the unit refresh `00238BF0`, which reaches `00268EA0` through `0026B4A0` (bit 10), `00267CC0` and `00269FE0`

  The register row's trigger list ("while `00268EA0` re-runs or `reqdisable(17)` / `reqenable(17)` fires") already
  covers it generically and needs no change.
- **N3 (record §3, C1).** C1 shows that the partition covers every instruction once. It does not show that function
  bodies are self-contained. F1 shows that the corpus has out-of-body jumps and fall-throughs (1,097 / 105 in the us
  copy), so the C2 positive-control count (32,374) is a count over cut bodies, not over reachable code. The filed
  population is clean (F1), so the result stands. Cite F1 next to C1 as the containment control.

Routing: N1–N3 go to FABLE. This review edits no page or register row.
