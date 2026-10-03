# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-gil-storage-clamp-and-every-path-that-mo-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-GIL-STORAGE-CLAMP-AND-EVERY-PATH-THAT` · Package: `_index/candidates/fable-gil-storage-clamp-and-every-path-that-mo-homing-1003/` · Page: `13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md` (commit eea05327e; reviewed at HEAD f8b2904c0, package and page unchanged since and unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 3 functions, 13 anchors`, `ALREADY` and `FAILS 0`. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 3 rows and 13 anchors, `mode: homing`. Rejected 0, skipped 0, missing 0, corrections 0. All 3 rows are on the page at lines 523–525 (heading at line 517), byte for byte.
- Semantic pass: **every row** was read clause by clause against `disw.py` output of the certified image (SHA256 73461D08...).
  - **`00300490`: exact.** `[rsp+0x20] = r8d` is the 5th argument (`00300494`). Then `r9d = 4`, `r8d = 0`, and `call 003008A0` (`003004A2`), whose result is returned.
  - **`0030DD70`: exact.**
    - `cmp [01EEBCFC], ebx` / `jle` is a signed "greater than 0" gate (`0030DD7E`; the rip target was recomputed).
    - Each iteration calls `003008A0(movzx bx, 0x63, 0, 1, 0)`: `lea edx, [r9+0x62]` with `r9d = 1`, and `[rsp+0x20] = edi = 0`.
    - Then `inc ebx`, `cmp ebx, [01EEBCFC]` re-read, and `jl` (signed).
    - No return value is set of its own.
  - **`0032A810`: exact.** `00300B80(rcx, rdx, 0)`, then `test eax, eax` / `cmovs eax, 0`. A negative 32-bit result becomes 0.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
