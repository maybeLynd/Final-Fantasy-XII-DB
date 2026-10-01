# SWE2-AUDIT-SEM review — SWE2-EC7's R1 span row "SQEX SEAD, UC-1 body in its span" (1, C) (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `SWE2-EC7-REQ-AUDITSEM-UC1-SPAN-SEAD-0929` |
| reviewed | `9e90a97ea` (author **SWE2-EC7**) — [`ec7-uc1-span-rows-0929/README.md`](../ec7-uc1-span-rows-0929/README.md), the row on `sead-function-identification.md`, `members/sead-span-uc1.tsv` |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT** |

## 1. The four tests, re-derived for `007EE7C0` (SWE2-AUDIT-SEM)

The shared re-runs are in [`../auditsem-review-uc1-span-ppfx-0930/`](../auditsem-review-uc1-span-ppfx-0930/REVIEW.md).
The replay on a clean extract of `2c840bfe4` gives an identical `uc1-span-tests.tsv` and an identical
`t2-compare.txt`.

- **Test 1.** `007EE7C0` lies between the listed SEAD members `007EE730` and `007EE800`, inside `007A4380`–`007F41A0`.
- **Test 2.** `select_audio_libraries.py`, with the body in its population, admits it (1136 → 1137). Every assertion
  holds, and the outbound (53 targets) and globals controls are byte-identical. The replay and the HEAD re-run agree.
- **Test 3.** My own reference hunt (`uc1_own.py` S / `uc1_own2.py` S2) finds:
  - one rip-relative `lea rax, [007EE7C0]` at `007EC4F1`, inside the span;
  - no rel32 or jcc site;
  - no VA64 cell;
  - one 4-byte RVA occurrence at `00D8A838`, inside a DIR64-relocated qword. That makes it a pointer half, which the
    record's rule drops.

  The body has no calls.
- **Test 4.** The note carries "1 UC-1 bodies admitted to frontier 2026-09-28, dispositioned by span 2026-09-29", and the
  members file has 1.

## 2. The body (SWE2-AUDIT-SEM)

`007EE7C0` (57 B) is a three-way position setter on `[rcx+0x138]`. It returns 0 in every case.

| `r8d` | effect |
|---|---|
| 0 | `mov [rcx+0x138], edx` (set) |
| 1 | `add [rcx+0x138], edx` (relative) |
| 2 | `[rcx+0x138] = [[rcx+0x60]+0x18] − edx` (from the end) |

That is the seek-callback shape, and its address is taken inside the SEAD span (`007EC4F1`). It is consistent with a
SEAD stream callback, and nothing ties it to game code.
