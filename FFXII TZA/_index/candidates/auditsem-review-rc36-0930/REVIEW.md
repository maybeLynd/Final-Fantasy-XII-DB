# SWE2-AUDIT-SEM review — FABLE's RC-36 answer: a marker's `+0x0C` label is drawn by `003C25BD` and aimed at by `003BEB06` (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-RC36-0930` |
| reviewed | `9a4cd5784` (author **FABLE**) — [`rc36-lmap-label-fable-0930/README.md`](../rc36-lmap-label-fable-0930/README.md), `FINDINGS.md`, `classify.py`, `rc36_label_readers.py` |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT** |

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

`classify.py` and `rc36_label_readers.py` re-run identically: exit 0, `FAILS 0` ([`producer_rerun.out`](producer_rerun.out)).
Both depend on `Tools/work/FABLE/…` (gitignored): `tk` from `takebacks`, and `pub140-scratch/tools/rawcalls.json`. So
they re-run only on this machine. That is the portability gap already routed as
`AUDITSEM-REQ-FABLE-DDRULE-T-TOOLSWORK-0930`; it is not re-filed here.

## 2. Question 1 — is `r15` at `003C25BD` a B marker, and does the label reach the drawn row? (SWE2-AUDIT-SEM)

Own reads: [`rc36_reads.py`](rc36_reads.py), [out](rc36_reads.out), and [`rc36_own.py`](rc36_own.py), [out](rc36_own.out).

- **`r15` is the point argument.** In `003C2320` it is written only at `003C2354` (`mov r15, rdx`) and restored at
  `003C2645`. `003C23C5` sends every non-zero kind (`r8`) to the arm that reaches `003C25BD`.
- **The only non-zero kind is B.**
  - `003C2320` has one caller, `003BE554` (no qword names it). That caller passes `rdx = [triple − 8]` and
    `r8d = [triple]` from the triple array.
  - The array is filled in `003C1A20`: the kind comes from `003BF430`'s out-slot, or is 0 on the `003BE1E0` path, and a
    null point is skipped (`003C1BC3` `test r13, r13` / `je`).
  - `003BF430` writes 3 only on its null-return path (`003BF46F`, then `003BF515` `xor eax, eax`). It writes 0 with an
    A point, `rec + 4 + 24·i` (`003BF4CC`), and 1 with a B point, `rec + 4 + 24·countA + 24·(i − countA)`
    (`003BF4F9`).
  - So a non-null point with a non-zero kind is a B marker.
- **The label reaches the draw.**
  - `003C2629` `call 002F9920` and `003C262E` store the string at row `+0x10`.
  - The label pass loads `[rdi + 0x10]` into `[rsp + 0x58]` (`004045E3`–`004045E7`) and passes `r9 = rsp + 0x30` to
    `002D8670` (`0040469E`–`004046AB`). `002D8670` reads the text at `[r9 + 0x28]` (`002D8718`), which is that slot.
  - The locked-text drop is as stated: when `00254A10` answers 0, a string equal to text `0x3EC` is nulled
    (`0040467F`–`00404695`).

  One wording point in `FINDINGS.md`, which does not change the answer: the pass draws row `+0x10` for **every** row.
  Byte `+2 == 1` (`004045EC`) selects only the marker's centring and the grey colour (`0x80404040` unless row `+0x1C`
  bit 0), so zone rows draw their `+0x10` name too.
- **The cursor reader.** `003BE950` splits on the triple kind at `003BEA7E`–`003BEA86`: kind 0 goes to `003BEAAC`
  (`word [+0xC]`, a zone), and a non-zero kind to `003BEB06` (`dword [+0xC]`, after a `0037EB70` call at `003BEB01`), as classified.

## 3. Question 2 — the other `+0xC` loads, including `003BE8DA` (SWE2-AUDIT-SEM)

I spot-read the rows that carry the verdict's weight.

- **`003C23CB` / `003C23F3`.** These are the kind-0 arm of the same emitter, so they read A.
- **`003C25A4`.** It reads `word [rax + 0xC]` on the `003BDDE0` result for the marker's `+0x14`. The code does not
  check the kind; the record says so, and says it rests on the data (106 zone, 5 `0xFF`, 0 marker).
- **`003BE8DA`.** This is the uncertain case, and its mechanism is real:
  - `003BE810` passes `r8 = rsp + 0x34` to `003BDDE0` (`003BE8B9`) and never writes that slot itself.
  - `003BDDE0` writes its `r8` out-slot only at `003BDE7F`, on the success path. On the kind ≠ 0 path, `003BDF06`
    overwrites `r15` (the saved out-pointer) with byte `+0x11`, so that path cannot write it.
  - `003BE8C9`–`003BE8D5` then call `003BCBA0` when `[rsp + 0x30] != 0` and `[rsp + 0x34] == 0`. With a stale 0 in the
    slot, a B point would be read as a field id.
  - "Could, depending on stack contents and gate state" is the right strength.

## 4. Question 3 — is P4's narrowing right? (SWE2-AUDIT-SEM)

Yes. The kind ≠ 0 arm runs `003C248F` → `003C253F` (the `003BDDE0` call) → `003C255F` → `003C2565` `jne 003C25BD`.
The label read therefore sits in the same arm, past P4's window. SWE2-CONTRACT has already applied the narrowing to
`lmap_readers.py`'s P4 docstring, to its record and to lmap §10.5 (line 551), and the RC-36 row cites it. Nothing more
is needed.

## 5. Strongest counterexample tried (SWE2-AUDIT-SEM)

I looked for a reader of B `+0xC` outside the emitter's one caller. The emitter has one rel32 caller and no qword or
thunk route (section K of [`rc36_own.out`](rc36_own.out)). The triple array's kinds are only 0, 1, or 3 with a null
point. No other B-typed flow was found.

The record's stated limit stands: a wholesale copy read at another offset, a byte-width read, or a point handed over
through a structure field outside the closure.
