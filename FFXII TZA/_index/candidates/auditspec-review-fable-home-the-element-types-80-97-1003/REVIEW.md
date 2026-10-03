# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-element-types-80-97-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-ELEMENT-TYPES-80-97-1003` · Package: `_index/candidates/fable-home-the-element-types-80-97-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-80-97.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 6 rows were read in full against the listings, 4,155 bytes in total (944 + 551 + 937 + 619 + 291 + 813). Each sentence holds clause by clause, including FABLE's four corrections (that the `.data` vector `01E02830..3C` is read before the reset call, and that the both-W paths fall through).

Every caller is an element program in this page's type table (lines 169–172). The two shared helpers are called mostly from that table's programs. All six fit.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 6 functions, 30 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 189, and the rows at lines 195–200 match `rows.json` byte for byte.
- **rows.json.** 6 rows, 30 anchors. Rejected 0, skipped 0, missing 0. Corrections 4 (`0047BFB0`, `00487D60`, `0048D240`, `0048F790`); the corrected texts are the ones on the page.
- **The `.data` vector, a premise of all six.**
  - A writer scan of every listed function's rip-relative operands landing in `01E02830..01E0283F` finds 1,451 references. Its writers are:
    - `004BF500` (`004C07D2`–`004C0879`), which writes `+0`, `+4` and `+8` only;
    - `0022CB90`, which stores 1.0 at `01E0283C` and zeroes `+0` to `+8`;
    - `0022CC20`, which copies the 16 bytes at `008C5FD0` over all four.
  - `008C5FD0` reads `[0.0, 0.0, 0.0, 1.0]`.
  - So `01E0283C` is always 1.0, and after each `0022CC20` call the first three floats are 0. The sentences rely on both facts: "z = x" after a reset, "float(n) - 1.0" through `01E0283C`, and "t + a t^3…" with the `01E0283C` multiply.
- **`0047BFB0` (0x3B0 B): exact.**
  - Before the reset (`0047C089` = +0xD9), `c8` = `[01E02838]` + `0x4096cbe4` goes to `02064CC8`, `c0` = `[01E02830]` + `0x3fc90fdb` to `CC0`, and `[01E02834]` + `0x40490fdb` to `CC4`. `CCC` gets `(1.0 + 2π) - 1.0`, and `DD4` gets W + 0x80.
  - `comiss` / `seta` gives `0x4096cbe4 > x`, which is stored masked at `DC8`. When it equals W, x -= 2π.
  - The three tests are written to `DC8`, `DCC` and `DD0`, followed by +0x1B2.
  - The y/z arms: `DC8` ≠ W gives `x + c0`; only `DCC` ≠ W gives `c0 - x` through +0x214; otherwise z = `c0 - (x - c0)`, then +0x23B, then the `DD0` test.
  - The degree-9 odd polynomial with `0xbe2aaaa4` / `0x3c08873e` / `0xb94fb21f` / `0x362e9c14` (also stored at `02064B04`) goes to `CB0` and `CB4`.
- **`00487D60` (0x227 B): exact.**
  - `02064B10` = `((b > a) << 4 + (a == b)) << 3`, and D = that AND `[02064DE0]`.
  - The both-W path: q = a/b, or `0x7F7FFFFF` from `00900360` when b = 0; then `trunc(q + [01E02830]) * b` goes to `CC0`, a -= it, and the call at +0xD8 falls through to `00487E4C`.
  - The C loop subtracts each entry's word `+4` with `jg`, a signed "not above 0" test.
  - The C == W arm calls +0x1E8 when b = 0 and +0x1FA when `0 > b`.
- **`00487F90` (0x3A9 B): exact.**
  - x -= `CC0`, then +0x32.
  - Four `comiss` / `ucomiss` pairs write `B10`..`B16` as `0x80|8`. `DC8` and `DCC` are masked by W + 0x80.
  - After +0x17C, `DD0` = `B16` AND `DD4`.
  - The y/z arms go through +0x1F3 and +0x21A, as the sentence says.
- **`0048D240` (0x26B B): exact.**
  - D = `(b > a) << 7` AND (W + 0xE0), and I = W + 1. When `DD0` == W + 1, it stores C = W and returns.
  - n = W + 0x1C2 goes to I. The both-W path calls +0x103 and falls through to `0048D35E`, reloading `dx` = n.
  - The C loop runs from entry n while the result stays non-negative (`jns`).
  - The C == W arm calls +0x219 and +0x22B.
- **`0048F790` (0x123 B): exact.**
  - The tests are `2π > x` and `x > [01E02830]`. `n = cvttss2si(x * 0.159155)`.
  - The `DC8` == W arm does `CC0` = `n * 2π`, x -= `CC0`, and the tail `jmp 0022CC20` at +0xBD.
  - The second arm stores `(0 > x + 2π)` masked at `DC8` and `float(n) - [01E0283C]` at `CC0`. It re-enters the multiply at `0048F831` when the mask equals W + 0x80; otherwise it adds 2π to x.
- **`004AD9E0` (0x32D B): exact.**
  - It copies eight 16-byte entries from `02064E30` + (`movsx [r9]` + 0x13) × 16 to `r8+0x140`.
  - Calls at +0xA8, +0xC1 and +0xDA, `00203080` each, on the stated triples.
  - m is the 5th argument, `[rsp+0xB0]` after five pushes plus `sub 0x60`. `ja 2` is unsigned, and the sign flips use the `01CEBDA0` mask.
  - The absolute values come from `andps` with the `01CEBD80` mask in double precision.
  - The m-selected quotient is 0 for other m (`xorps xmm6`). It is passed in `xmm2` to the three `00202FE0` calls (+0x271, +0x284, +0x297), followed by `00202B10` ×3 (+0x2A5, +0x2B7, +0x2C9).
  - The final 48-byte copy goes to entry `[r9]` + 0x13.
- **entered_from.** The raw byte scan confirms each named site:
  - `0047C8E9` = `0047C360` + 0x589;
  - `00488CAD` = `00488340` + 0x96D;
  - `00489452` = `00488340` + 0x1112;
  - `0048E247` = `0048D4B0` + 0xD97;
  - `0047C8BC` = `0047C360` + 0x55C;
  - `004AE712` = `004ADD10` + 0xA02.

  Other callers: `0047BFB0` has 33 call sites and `0048F790` 16, in `0047C360`, `00482860`, `00485790`, `0048AF70`, `0048D4B0`, `0048F8C0`, `004930A0` and `004B1190`. `004AD9E0` has 8 sites, all in `004ADD10`.
- **Host fit.** The callers are this page's element programs (table at lines 169–172): `0047C360` is `0x8B`, `00488340` is `0x85`, `0048D4B0` is `0x96` and `004ADD10` is `0x94`. Of the shared helpers' other callers, `00482860`, `00485790`, `0048AF70`, `0048F8C0` and `004930A0` are also programs in that table. Only `004B1190` is not, and `generated-float-table-builders.md` profiles it as a large non-builder. These are the programs' own math subroutines. They fit.
- **Advisory (not a defect).** In `004AD9E0`, "copies the 48 bytes at `r8+0x180` back to the table at the same index" is exact about the index, but "back" can suggest the bytes' own source entries. Those were entries index + 4 to index + 6, and the write goes to entries index to index + 2. Suggested: "copies the 48 bytes at `r8+0x180` to the first three of those eight entries".
- **Advisory (not a defect).** `0048D240` is named before this package, but only in a pass-22 crossing list on `99-Unresolved-Residual/README.md` (line 532, "`0022CC20` is called by … `0048D240`"). A list mention is not a host, so the homing stands.
- **Advisory (tool).** The applier's caller test is a substring test that the applied row satisfies by itself. Every caller here is also cited in the page's type table.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
