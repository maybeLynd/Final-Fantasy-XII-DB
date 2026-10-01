# SWE2-AUDIT-SEM review — FABLE's static answers RC-12, RC-13, RC-14, and RC-13's proposed OUT OF EVIDENCE BOUNDARY disposition (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-RC121314-0930` |
| reviewed | `82cb3490a` (author **FABLE**) — [`rc121314-fable-0930/README.md`](../rc121314-fable-0930/README.md); and the RC-13 row's proposed disposition in `_index/OPEN-QUESTIONS.md` at HEAD (row text by SWE2-CONTRACT; judged here only against the guard and FABLE's evidence) |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8`, image base `0x120000`; decompiled `us` corpus (1,114 scripts) |
| tree at review | HEAD `d3e855f21` |
| not used as evidence | SWE2-ORACLE's `rc12-footer-channels-runstate-0930` (OPUS-operated lane), which the row also cites |
| **verdict** | **ACCEPT-WITH-NARROWING** — RC-12 and RC-14 reproduce and survive the counterexample search; RC-13's census is adequate for a *descriptive* convention with one wording narrowing. **The proposed OUT OF EVIDENCE BOUNDARY disposition for RC-13 is not signed**: it is the wrong status class (§4). |

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

`rc12_special_slots.py`, `rc13_channels.py` and `rc14_runstate.py` run from the record folder, exit 0, and match the
committed `.out` line for line ([`producer_rerun.out`](producer_rerun.out)).

## 2. RC-12 — the 1-based slot formula and `00263D40` (question 1) (SWE2-AUDIT-SEM)

Read by hand ([`rc12_14_reads.py`](rc12_14_reads.py), [out](rc12_14_reads.out)).
- **The wait-resolver control.** `0025E17B mov eax, 0xB` / `0025E180 cmp ax, word [rcx + rbx]` / `jge` (count must
  exceed 11), then `0025E186 movsx r12d, word [rcx + rbx + 0x18]`. That is `c = 11` read at `2·(c + 1) = 0x18`, so
  `t = c + 1 = 12`, the `mapjump` slot. The formula `t = c + 1 = disp / 2` holds.
- **`00263D40` is a multi-list accessor**, as stated. It returns −1 unless `word [block] > 3`. `esi = r8d` is the list
  index and `rdi = r9d` the item. The loop `00263D90`–`00263D9F` skips `esi + 1` count-prefixed lists
  (`rcx += 2·(n + 1)`), and `00263DA8` returns `word [list + 2 + 2·item]` when `item < n`.

RC-12 stands, within its two stated limits (slot 18 has no shipped declaration; lists 1–4 are not decoded).

## 3. RC-14 — the two promoters and the missed-writer question (question 3) (SWE2-AUDIT-SEM)

- **Both are real 1 → 2 promoters of entries.** `003DB240 cmp byte [rcx], 1` / `jne` / `003DB245 mov byte [rcx], 2` /
  `add rcx, 0x14`, over `movzx eax, byte [rbx + 0x89]` entries from `[rbx + 0xA0] + 0x11`, gated by `byte [rbx + 0x63]`
  and followed by `call 003DB6E0` and `shr byte [rbx + 0x63], 1`. `003DBCA7`–`003DBCB7` is the same loop, reached only
  when `003DBCF0` returns 1 and the target differs from the requester (`003DBC7F`–`003DBC87`).
- **A writer both sweeps miss?** The shape the record names — a pointer advanced by `0x11` and stored through, in a
  function that does not walk the table — was swept directly, image-wide, with no function list
  ([`rc14_preadvanced.py`](rc14_preadvanced.py), [out](rc14_preadvanced.out)). There are 233 `add r, 0x11` /
  `lea r, [r + 0x11]` instructions. Following each for 40 instructions finds **exactly three** byte stores through the
  advanced register: `003DB245`, `003DBB35`, `003DBCAC` (all three are also the positive controls). So the joint blind
  spot of the structural and displacement censuses holds no further writer of this form.

RC-14 stands. The limit remains for a pointer advanced by a computed amount, or held in memory between the advance and
the store.

## 4. RC-13 — is the census enough, and the proposed disposition (question 2) (SWE2-AUDIT-SEM)

**The census answers a descriptive question, not a normative one.** The re-run shows the parsed share per channel
(1: 26,879 / 30,724 = 87%; 2: 85%; 3: 83%; 4: 89%; 5: 92%; 7: 73%) and the function-name shares. Two of the labels
overreach the data:
- channel 1 "the actor's own behaviour" rests on a long tail. The largest name-prefix share is 8% (`setEventLight`);
- channel 7 "reset, cancel and cleanup" covers about half the parsed calls (`リセット` 27%, `ポイントキャンセル` 15%,
  `clear` 8%). The rest includes positioning (`コカ渡岸位置` 12%, `コカ渡岸移動` 5%) and `入手` 8%.

As a statement of how shipped scripts use channels (dominant uses, with shares), the census is enough. The `reqArr`
12% is disclosed, as it should be. As a rule an author must follow, it is not claimed, and the record says so ("an
authored convention, not an engine rule").

**The proposed OUT OF EVIDENCE BOUNDARY disposition does not meet the class it names.** The FRONTIER ruling that created
the status (`register-triage/batch-K-scope-rulings.md`, Extension 2026-09-27b) and `check_questions.py` define OEB as
*a fact about the BUILD whose only carrier is an artefact outside the admitted evidence base (a debug build never
shipped, a comparison build the program does not admit)*. They state it is **not** a synonym of NO ADMISSIBLE SOURCE,
which covers *a fact about PEOPLE (a designer's name or intent)*.

The row's residue is "an author's intent in using a channel for its own logic". That is a fact about people, so OEB
is the wrong word for it. The row also fails OEB's guard condition 1: it names no excluded artefact ("no static fact
decides and no run-time observation would add" is not a named source).

What the evidence supports, for SWE2-CONTRACT to choose:
- **(a)** **ANSWERED** for the question as asked — what a channel means to an author, read from the shipped corpus as
  dominant-use shares. The residue sentence stays as a limit.
- **(b)** **NO ADMISSIBLE SOURCE** for the intent residue alone, if that residue is kept as the row's question. That
  needs NAS's own guard: the mechanism cited (the priority-only scheduling), the inadmissible source named (the
  designers' intent, carried by no shipped artefact), the negative checked (FABLE's census) and a non-author signature.
  I would sign (b) for the intent residue on FABLE's evidence. I do **not** sign OEB.

## 5. Narrowings and the routed disposition (SWE2-AUDIT-SEM)

- **N1 — RC-13 table (FABLE's record) and the page section 8 text.** Channel 1: replace "the default: the actor's own
  behaviour" with *"the default and largest channel: the actor's own behaviour (movement, turns, doors, event lights;
  no single function above 8% of its calls)"*. Channel 7: replace "reset, cancel and cleanup" with *"mostly reset,
  cancel and cleanup (about half its parsed calls), also some repositioning and item hand-overs"*.
- **D1 — RC-13 row status (SWE2-CONTRACT).** Do not apply OUT OF EVIDENCE BOUNDARY. Apply (a) ANSWERED with the residue
  as a limit, or (b) NO ADMISSIBLE SOURCE for the intent residue, under its four-condition guard, with this record as
  the non-author signature for (b).

## 6. Not reviewed here (SWE2-AUDIT-SEM)

- The page section 2.4 clamp of channels 16 and 17 to the top channel (cited, not re-read).
- Whether both `World_UpdateSimulationTick` call sites of `003DB1F0` run every tick (the record's own open point).
- ORACLE's record on the same rows.
