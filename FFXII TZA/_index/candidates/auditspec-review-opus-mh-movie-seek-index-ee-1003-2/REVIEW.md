# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-mh-movie-seek-index-ee-1003-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MH-MOVIE-SEEK-INDEX-EE-1003-2-47359` · Package: `_index/candidates/opus-mh-movie-seek-index-ee-1003-2/` (package last changed at `793e20e74`; reviewed at HEAD `85ecbde72`) · Page: `17-Presentation-Rendering/Movie-Containers/mh-movie-seek-index.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row. It was read clause by clause against a raw capstone decode of the certified image. This session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. The row holds as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0` and exited 0.
- **Counts.** 1 row with 5 anchors. The README's `Missing: 0` matches `rows.json`.

**`008001B0`**: exact. The clauses follow the body in order.

- **Array at [o+0xA0].**
  - `008001B7`-`008001E3`: end = [o+0xA0] + 8·`cdqe`(dword +0xAC + dword +0xA8). The loop compares with `cmp`/`je`/`jne`, an equality test.
  - A null p is skipped (`008001FA`).
  - The count is `movsxd` dword [p+0x3C] with `jle` (signed, `008001FC`-`00800202`).
  - Each non-null qword in [p+0x30] gets `call [[x]]` with `edx` = 1 (`00800211`-`00800225`).
  - Then `00210EB0([p+0x30])` and `00809950(p, 0x40)` (`0080022C`-`0080023D`).
- `00800247`/`0080024E`: `00210EB0([o+0xA0])`.
- **q = [o+0x80].** Non-null q: slot +0 with 1 on each non-null qword from [q+0x28] to [q+0x30], then `00210EB0([q+0x28])` and `00809950(q, 0x38)` (`00800253`-`008002AC`).
- **r = [o+0x78].** `00210EB0` is called on [r+0x38], [r+0x40] and [r+0x48]. Each slot's zeroing store comes after the call that consumed it (`008002CE` after `008002C3`, `008002DB` after `008002D2`, `008002E7` after `008002DF`). Then `00809950(r, 0x50)` (`lea edx,[rdi+0x50]` with `edi` = 0).
- **[o+0x88], [o+0x90], [o+0x98].** Each non-null one is passed to `008000C0`, `007FFDD0` or `008003A0`, then to `00809950` with 0x40, 0x38 or 0x38 (`008002F3`-`00800356`).
- **t = [o+0x70].** `00210EB0([t+0x28])`, `00210EB0([t+0x38])`, `00809950(t, 0x48)` (`0080035B`-`0080037E`).
- **Tail.** `00800383`-`0080038D`: `rcx` = o+0x20, `jmp 007FFEE0`.

The row names the callees only, with their arguments, so no callee body was needed.

## SWE2-AUDIT-SPEC limits

- Body statements only. This review does not interpret the members as seek-index tables, or `00809950` as a sized delete.
- The applier reported `ALREADY`, so the page text was taken to be the `rows.json` text.
