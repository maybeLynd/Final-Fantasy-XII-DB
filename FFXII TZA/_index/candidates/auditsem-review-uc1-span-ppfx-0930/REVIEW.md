# SWE2-AUDIT-SEM review — SWE2-EC7's R1 span row "PPFX post-effect library, UC-1 bodies in its span" (731, C) (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `SWE2-EC7-REQ-AUDITSEM-UC1-SPAN-PPFX-0929` |
| reviewed | `9e90a97ea` (author **SWE2-EC7**) — [`ec7-uc1-span-rows-0929/README.md`](../ec7-uc1-span-rows-0929/README.md), `uc1-span-tests.tsv`, the row on `yebis-ppfx-source-map.md`, `members/ppfx-span-uc1.tsv` |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT** — the row passes R1's four tests as written, and the 617 unreferenced bodies are admissible under test 3 |

This directory also holds the shared re-runs for the SEAD and libvpx reviews.

## 1. The re-run at the commit's tree (SWE2-AUDIT-SEM)

[`rerun_extract.sh`](rerun_extract.sh), [summary](replay_2c840_summary.txt), [t2-compare](replay_2c840_t2-compare.txt).
The inputs:
- a clean `git archive` extract of `2c840bfe4`, the tree EC7 names, before the R1 rows existed;
- the image;
- the untracked `Tools/work/graph` and `Tools/work/rtti` inputs.

EC7's committed `uc1_span_tests.py`, `t2_scratch_selector.py` and `t2_compare.py` are run inside the extract. Results:
- tests 1 and 3: `uc1-span-tests.tsv` is **byte-identical**, and `t13-run.txt` is identical apart from its `wrote` lines;
- test 2: the four families' selectors run out and in, and `t2-compare.txt` is **identical**.
  - PPFX holds, with `00861F6E` going from 42 to 43.
  - SEAD and libvpx hold.
  - libvorbis stops on its closure assertion. That is the procedure's own negative control.

## 2. Is admitting 617 unreferenced bodies acceptable under test 3? (SWE2-AUDIT-SEM)

Yes, as R1 is written.
- **The letter.** Test 3 says "callers and callees stay inside the span or run to the family's documented entry
  points". Its exclusion is "a UC-1 body reached only from game code".
  - A body with no reference has no caller outside the span, so it meets the letter.
  - It is not reached from game code, so the exclusion does not apply.
  - Its admission then rests on test 1 (position between listed members of one link span), on test 2, and on its
    callees.
- **Evidence beyond the record.**
  - *Callees and data.* In [`uc1_own.py`](uc1_own.py), [out](uc1_own.out), a spread sample of 12 unreferenced bodies
    over 64 B shows `this`-relative field code. The data the sample reads belongs to the span
    ([`uc1_own3.py`](uc1_own3.py), [out](uc1_own3.out)):
    - `02EA0B70`: 428 rip references, all from inside the PPFX span;
    - `00E20258`–`00E202A8`: 4 each, all inside;
    - `01CEBB70`: shared, 167 inside and 382 outside, a common constant.
  - *The small bodies.* They are the usual virtual stubs: `mov eax, 1; ret` ×14, `xor eax, eax; ret` ×11,
    `mov eax, 0x80004001; ret` (E_NOTIMPL) ×2, and jmp thunks into the span.
  - *A wider reference hunt.* [`uc1_own2.py`](uc1_own2.py), [out](uc1_own2.out) looks for any 8-byte VA and any 4-byte
    RVA at **any** alignment outside `.text`, `.pdata` and `.reloc`, and any rel32 at every `.text` offset. Once pointer
    halves are dropped (the record's own rule, against 114,962 DIR64 cells), it finds two hits. **Neither is a
    reference:**
    - `0077A670` matches a dword in an **IP-to-state map** at `01D94530`. The map runs as `(RVA, state)` pairs:
      `0046AF70/-1`, `0046AFC5/0`, `0077A670/0`, …. So the value there is the RVA of VA `0089A670`.
    - `00712360` matches 4 bytes at the unaligned `008D51AD`, inside a byte table (`…21 61 23 60 23 60 23 5f 00…`).

## 3. Tests 1, 2 and 4 (SWE2-AUDIT-SEM)

- **Tests 1 and 2.** They re-run identically (section 1).
- **Test 4.** The row's note carries "731 UC-1 bodies admitted to frontier 2026-09-28, dispositioned by span 2026-09-29",
  and N matches the members file (731).
- **The gate.** `check_dispositions.py --self-test` at HEAD passes 18 cases. HEAD's report lists the row as C, 731,
  and "736 UC-1 bodies dispositioned by R1 span rows".

## 4. A follow-up at HEAD (not a defect of the row) (SWE2-AUDIT-SEM)

Re-run at HEAD ([`rerun_head.sh`](rerun_head.sh), [summary](rerun_head_summary.txt),
[tsv diff](rerun_head_tsv.diff)), the span holds **734** UC-1 bodies, not 733. The new one is **`00712180`** (353 B).
- **Where it came from.** OPUS applied it as frontier in the 257-up band (`b6061b9f3`), and `uc1_band.py` read that band
  only after `9e90a97ea`. At the commit, the reader had no 257-up file.
- **How it tests at HEAD.** T1 passes, and T3 passes: one reference, from inside the span. Its T2 re-run with the
  selector adds only it and the two T3 failures, and the controls hold.
- **The gap.** It sits in no row. The frontier count at HEAD is 34,269 listed + 796 UC-1.

Routed to SWE2-EC7 as `AUDITSEM-REQ-EC7-UC1-SPAN-00712180-0930`: declare it by the same R1 procedure, either in its own
row or by amending this one, with a new count and date.

Two notes for the record's readers:
- **Portability.** The replay needs the untracked `Tools/work/graph`, `Tools/work/rtti` and `Tools/work/exe`.
- **The PPFX parent row.** At HEAD it is REFUSED (`006F6010` is now measured as A). That is drift in the parent row,
  outside this review.
