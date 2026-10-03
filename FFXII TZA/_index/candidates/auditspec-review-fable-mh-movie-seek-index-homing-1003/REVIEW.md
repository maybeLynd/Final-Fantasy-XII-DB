# SWE2-AUDIT-SPEC review: FABLE cloud-drafted F-homing rows (fable-mh-movie-seek-index-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-MH-MOVIE-SEEK-INDEX-HOMING-1003` · Package: `_index/candidates/fable-mh-movie-seek-index-homing-1003/` · Page: `17-Presentation-Rendering/Movie-Containers/mh-movie-seek-index.md` (commit `b7c6eb07d`, reviewed at HEAD `81a9fa56d`; the package is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- **Applier.** `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 3 functions, 15 anchors`, `ALREADY`, `FAILS 0`, and wrote nothing. The section is on the page at line 293, and every sentence is on the page verbatim.
- **rows.json.** 3 rows, 15 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **Semantic pass.** All 3 rows were read clause by clause against `disr.py` output of the certified image.
  - `00211B60`:
    - `00211AC0` gets the incoming `rcx`/`edx` untouched (`mov edi, edx` / `mov rbx, rcx`).
    - `test dil, 1` / `je` skips both calls.
    - `test dil, 4` / `jne` chooses `0016D6A0(rcx, 0x158)` at +0x3E. Otherwise it calls `00584730(rcx)` at +0x2E.
    - Every path returns `mov rax, rbx`.
    - Exact.
  - `006792C0`:
    - `00D6CD90` goes to `[rcx]`, then `005CD700(rcx+0x48)` and byte `+0x50` = 0, then `005CD700(rcx+0x30)` and byte `+0x38` = 0.
    - Finally `lea rax, [00D6CD78]` / `mov [rdi], rax`, so `rax` holds `00D6CD78` at the `ret`.
    - Exact.
  - `00679330`: the same sequence, then `test dil, 1` / `je` around `free(rcx, 0x60)` (`00809950`), and `mov rax, rsi` returns `rcx`. Exact.
- Limits: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
