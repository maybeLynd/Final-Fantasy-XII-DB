# A-drift round 5: the 13 rows refused after OPUS's re-status batches 8-14, repaired (OPUS for SWE2-EC7, 2026-10-01)

*FABLE (and with it SWE2-EC7) is inactive until its reset. The user asked OPUS to carry the A-drift pairing in the
meantime (2026-10-01). This round uses EC7's own pipeline from
[`ec7-dd-adrift-pairing-0930`](../ec7-dd-adrift-pairing-0930/README.md) unchanged: `exact_remove.py`, then the named
selectors, then dated row notes. The only difference is OPUS's tag on the notes. All figures come from a clean export of
HEAD `a369d32e8` ([`opx_export.sh`](opx_export.sh)).*

## What moved F (OPUS)

At `a369d32e8`, `check_dispositions` refused 13 family rows, each because members were measured A. Six OPUS re-status
commits made 18 members A by interior citation:

| commit | page re-statused | members made A |
|---|---|---|
| `6d9fb5a1f` | third-party middleware inventory | 8 |
| `d526b865b` | authored data table registry | 3 |
| `95cf8c42f` | gambit evaluation and enmity | 2 |
| `56a49cc8c` | script VM interpreter; the field runtime pass | 1; 1 |
| `dd651efd2` | authored reference lifetime evidence | 2 |
| `eef738450` | capability-inhibition policy | 1 |

Every member, with its page and interior address, is in [`pairing-round5.tsv`](pairing-round5.tsv). F went
**4,764 → 8,335** across those commits. That drop is the dashboard's latest dip.

## The repair (OPUS)

**Stage 1, exact removal.** `exact_remove.py` deleted the 18 A members and set each row's count
([`stage1.txt`](stage1.txt)). It reported no refusal of any other kind.

**Stage 2, the named selectors.** Each was re-run on the repaired export, identity selectors first and the derived one
last. Membership deltas against `a369d32e8` are in [`memdiff.txt`](memdiff.txt):
- **Reproduced stage 1 exactly** (they drop just the A members and admit nothing): `select_verb_adapters.py` (its
  leftovers file is unchanged too), `select_audio_libraries.py` (Tremor, libvorbis; its other files are unchanged),
  `select_zlib.py`, `select_ppfx.py`. The CallResultTailCall and DoubleCallResultTailCallSavedThis files were also
  reproduced, by `select_frontier_form_clusters.py` and `_3.py`.
- **`select_documented_global_leafs.py` stays at 230.** It drops `003204B0` (A) and binds `003DE970` again. EC7 dropped
  that body on 2026-09-29 because its target's citing page, the field runtime pass, was REOPENED. That page is DOCUMENTED
  again (`56a49cc8c`). The count guard stays 230; its comment gets the round-5 line.
- **`select_explained_callee_adapters.py` (DERIVED, run last) goes 489 → 488.** It drops the three A members. It
  admits `00263860` and `003DCCF0`, whose single callees (`002E9660`, `003DCD00`) became A in batch 8 (`d526b865b`).
- **Exact removal only** (no selector writes these files): CallThenReturnZero and StaticHandleReplaceWithPreRelease.
  The xc-registered teardowns row also stays exact: its named selector rewrites every XC-array cluster file, so EC7's
  round-1 practice is kept.
- **Dear ImGui context object stays exact.** `select_imgui.py` stops with an `AssertionError`
  ([`select_imgui-at-repair.out`](select_imgui-at-repair.out)): line 169 requires the context-object body `00791D80`
  to be a member, and that body is now A. Changing that assertion is EC7's selector work, routed below.

**Stage 3, row notes.** Each row's count is set and a dated sentence is appended
([`round5_notes.py`](round5_notes.py)). The notes contain no addresses, because a hex word in a row note reads as a
citation.

**Bringing it to the live tree.** The live checkout uses `core.autocrlf=true` and has mixed line endings, so the export
files are not copied over. [`replay_lines.py`](replay_lines.py) replays the line-level change from the export's base to
its result onto each live file and keeps every untouched line byte-for-byte. It refuses any file whose live content
differs from the base: 0 of 19 were refused. Every target path was clean and unchanged from `a369d32e8` to the live HEAD.

## Seen and not applied: form-cluster drift that predates this round (OPUS)

On the untouched `a369d32e8` export, the form selectors already disagree with two committed files:
- `select_frontier_form_clusters_3.py` drops `002DEBB0`, `002E05C0` and `004735E0` from
  NativeAdapter.CallBoolNormalizeReturnSete (5 → 2).
- `select_frontier_form_clusters.py` admits `00251E80` and `003CA2F0` to NativeAdapter.NullableGlobalTailDispatch
  (10 → 12).

Neither row is refused, and neither movement comes from A-drift. Both files are left as committed and routed to SWE2-EC7.
(At that HEAD the same selectors also admit 47 more bodies across six files. Those admissions come only from the 13
refused rows' members counting as frontier, which is the order trap EC7 recorded in round 4. They disappear once stage 1
runs.)

## Figures (OPUS)

The `check_dispositions` summary before ([`check_dispositions-before.txt`](check_dispositions-before.txt)) and after
([`check_dispositions-after.txt`](check_dispositions-after.txt)):

| | before | after |
|---|---|---|
| frontier (F) | 8,335 | **4,505** |
| B / C | 1,382 / 15,719 | 3,240 / 17,691 |
| rows accepted / refused | 323 / 13 | **336 / 0** |

A is 9,629 both times. `check_family_forms` gives MISMATCH 0 families
([`check_family_forms-after.txt`](check_family_forms-after.txt)).

run: exact_remove.py, the eight selectors and round5_notes.py on a clean export of a369d32e8 (FAILS 0); replay_lines.py onto the live tree (FAILS 0)

## Routed (OPUS)

- **SWE2-EC7, when it resumes:**
  - the `select_imgui.py` assertion;
  - the pre-existing CallBoolNormalizeReturnSete and NullableGlobalTailDispatch drift;
  - a review of this round's use of its pipeline.
- **SWE2-AUDIT-SPEC:** review (OPUS-lane production).
- **Practice from here (OPUS).** Each OPUS re-status publish now carries its own A-drift pairing, so F no longer dips
  between a re-status and its repair.
