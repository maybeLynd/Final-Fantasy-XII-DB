# SWE2-AUDIT-SPEC review: OPUS homing rows (opus-arm-catalogue-slice-d-ids-108-139-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-ARM-CATALOGUE-SLICE-D-IDS-108-139-HOMING-10` · Package: `_index/candidates/opus-arm-catalogue-slice-d-ids-108-139-homing-1002/` · Page: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-D-ids-108-139.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh (verify mode) -> exit 0, `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0`.
- `rows.json`: 1 row, 5 anchors; rejected 0, missing 0.
- **Entry.** The row states none, and the class file lists no direct callers. The raw census finds one: `001C0DBA jne 0x1c0960`, in `001C0DB0` (`mov rcx,[rip+..]; test rcx,rcx; jne`). That is a conditional tail-jump the homing census missed. The row claims nothing about entry, so this is a note for the class file, not a row defect.
- **Host fit.** The body calls `001A9930` and `001BF8B0` (and `00210EB0`), and the page documents them, so the homing premise holds.
- **Semantic pass, all 1 row (299 B, read in full).** Exact, apart from the base item below:
  - the null `001A9930()` early return;
  - the sentinel walk (`rdi = rsi+0x28`, first node `[rsi+0x30]`, next through `0016D6D0`);
  - the object `+0x100` non-null test and the byte compare of string `[node+0x20]` against `001A9930()+0x241`;
  - `0016DA60(node, rcx+0x28)`;
  - the string free when `[node+0x30]-[node+0x20] > 1` (signed `jle`) and the begin pointer is non-null, through `[node+0x38]` slot `+0x18`;
  - the 0x48-byte node free through `[rcx+0x50]` slot `+0x18`;
  - `001BF8B0(rcx, obj+0x100, obj+0x108)`, `00210EB0` on a non-null re-read of `+0x100`, and `00809950(obj, 0x118)`.

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing (row `001C0960`, write base).** The decrement is `001C09F4 dec dword ptr [rsi + 0x48]`, with `rsi` = incoming `rcx` (`001C0979 mov rsi, rcx`). The row writes "for it, it decrements dword `+0x48`" straight after naming the node, so the write reads as node `+0x48`, which is past the 0x48-byte node. Likewise "first node qword `+0x30`" is `[rsi+0x30]` (`001C098A`), not `+0x30` of the list head at `rcx+0x28`.

Replacement wording: "(first node qword `+0x30`," becomes "(first node qword `rcx+0x30`,", and "for it, it decrements dword `+0x48`," becomes "for it, it decrements dword `rcx+0x48`,". The rest of the row stands. The producer applies the narrowing and re-runs `interior_applier.py --apply`.
