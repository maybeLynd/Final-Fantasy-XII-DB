# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-drawing-a-line-character-by-character-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-DRAWING-A-LINE-CHARACTER-BY-CHARACTER-094A1` · Package: `_index/candidates/opus-drawing-a-line-character-by-character-ee-1003/` (package last changed at `793e20e74`; reviewed at HEAD `85ecbde72`) · Page: `99-Unresolved-Residual/Glyph-Run-Rendering/drawing-a-line-character-by-character.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 4 template rows. The first was read clause by clause against a raw capstone decode of the certified image. The other three were proved equal to it, instruction by instruction, except for one operand that their sentences also change. This session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. Every row holds as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 4 functions, 20 anchors` / `ALREADY` / `FAILS 0` and exited 0.
- **Counts.** 4 rows with 5 anchors each, 20 in total. The README's `Missing: 3` matches the `missing` list in `rows.json` (`002986E0`, `006497E0`, `0064A500`).

**`00686830`** (full read): exact.

- `0068683F`-`0068684A` zero qwords [rcx], +8 and +0x10, and dword +0x18 (`edi` = 0).
- h = rdx+0x38 is stored at +0x20 (`0068684D`/`00686851`). qword [h] goes to +0x28, replaced by 0 through `cmove` when it equals h (`00686855`-`00686862`).
- The static `02D39A40` goes to +0x30 (`00686866`/`0068686D`).
- `00686871` calls `001B7CE0(rcx)`. A non-zero `al` skips to the tail (`00686876`/`00686878`).
- Loop body (`00686880`-`00686894`): a non-null +0x28 is replaced by the qword it points at, or by 0 when that equals +0x20 (`cmove`).
- The loop calls `001B7CE0` again and repeats on `al` == 0 (`0068689B`-`006868A2`). The body has no other conditional jump, so "no other exit" holds.
- `006868A7` calls `001AA0A0(rcx)` and the function returns `rbx` = `rcx`.

**Template equivalence.** `tdiff.py` compared the intdump of `00686830` with each of the other three bodies:

- `006868C0`: lengths 40/40, 1 differing instruction, +0x36 `lea rax,[rip->02D39A40]` against `[rip->02CB78A0]`.
- `00686950`: lengths 40/40, 1 differing instruction, the same slot, against `02CF1C40`.
- `006869E0`: lengths 40/40, 1 differing instruction, the same slot, against `02CF1A40`.

A character diff of the sentences against the `00686830` sentence finds one change in each, inside the static's address: `02D39A40` becomes `02CB78A0`, `02CF1C40` and `02CF1A40` respectively. Each sentence changes the same thing as its body.

The rows say nothing about what `001B7CE0` or `001AA0A0` do, beyond the byte test on the first one's result. So no callee body was needed.

## SWE2-AUDIT-SPEC limits

- Body statements only. This review does not interpret these as iterator constructors over a glyph list, or the four statics as type descriptors.
- The 3 missing functions were not reviewed. They are not in the package.
- The applier reported `ALREADY`, so the page text was taken to be the `rows.json` text.
