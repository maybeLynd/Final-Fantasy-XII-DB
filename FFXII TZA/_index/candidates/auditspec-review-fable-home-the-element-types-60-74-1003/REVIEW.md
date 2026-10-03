# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-element-types-60-74-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-ELEMENT-TYPES-60-74-1003` · Package: `_index/candidates/fable-home-the-element-types-60-74-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `e0e99b7c6`; the package is unmodified in the working tree) · Page: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-60-74.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 23 rows were read against the bytes, not just the 10 the request asks for, and every sentence holds. Every body is entered only from `004B1190`, which this page names in its own type table as the program element type `0x60` runs ("`004B1190`: line strip + textured strip"). That is a body statement, so the hosts fit.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 23 functions, 101 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section is on the page under the heading at line 374, and all 23 rows (lines 380-402) match `rows.json` byte for byte. The committed `.out` (`DRY`) predates the apply.
- **rows.json.** 23 rows, 101 anchors. Rejected 0, skipped 0, missing 0. 1 FABLE correction (`004B0F60`).
- **Callers.** `edges.tsv` and the raw E8/E9 index (`tools/rawcalls.py`) give `004B1190` as the only caller of every body. Each site was confirmed by the applier as a direct call.
- **`004B0F60` (0x229 B, the corrected row).** Traced branch by branch:
  - The head: `0x3F000000` goes to `02064B04`, W+1 to `02064DC8`, W+`0xE0` to `02064DD8` and `a - b` (`subss`) to `02064B10`. Then `cmp word 02064DD0, W+1` / `je 004B1184` returns.
  - `and r8w, word 02064B10` / `02064DC8` = W+`0x118`.
  - On `02064DD8 == W` and `02064DD4 != W`, `004B10EF` returns when `02064DCC == W`, and otherwise adds `02064DCC - 1` to `dx` and stores it.
  - On both W, `ucomiss b, 0`: the ordered-equal arm stores `0x7F7FFFFF` (`00900360`), else `a/b`, to `02064B00`. Then `cvttss2si(q + [01E02830])`, back to float, times b. The product goes to `02064CC0` and `a - product` to `02064CB0`. The call at `004B1063` is +0x103 (`0022CC20`, which copies the 16 bytes at `008C5FD0` over `01E02830`).
  - At `004B107E`, `02064DCC != W` truncates a in place. The loop then runs `ax = word [02064E34 + (movsx dx)*16]`, `r8w -= ax`, `ax` to `02064DD0`, `jns`. Then `dec dx` goes to `02064DC8` and `r8w` to `02064DD4`.
  - `02064DCC == W` gives `r = a/[02064CB8]` (max on zero) to `02064B00` and `r + [01E02834]` to `02064CB4`. Then `call 0022CC40` at +0x1F1 on an ordered zero, and `call 0022CC30` at +0x203 when `comiss 0, b` is above (negative). Then `cvttss2si` in place.
  - The sentence is exact. It leaves out the second, identical `0x3F000000` store at `004B1001`, which changes nothing.
  - The correction note is also right: `004BF500` writes `01E02830`/`01E02834` at `004C07DA`-`004C0856`. `0022CB90` also writes it; the note does not mention that writer, and nothing depends on it.
- **The R-register rows `004B97F0`, `004B9C50`, `004B9CA0`, `004B9CF0`.**
  - The gate is `cmp dword 02064AFC, 0`, and the zero arm stores (or returns) 1.0 (`01CEBBA8`).
  - The other arm computes `ecx = (((v >> 0x12) ^ v) >> 4) & 1` and `eax = ((v & 0x3FFFFF) | 0x1FC00000) * 2` (`add eax, eax`), ORs them, stores the result to `01E02828` and reloads it as a float.
  - The destinations are `xmm0`, `[rcx]`, `[rcx+4]` and `[rcx+8]`, as each row says.
- **The compare rows `004B9D80`, `004B9E60`.**
  - `004B9D80`: the equal flags e0/e1/e2 come from `ucomiss` with `jp` going to 0. The `cmova` terms are `b2>a2` 4, `b1>a1` 8 and `b0>a0` 0x10. The sum is then built as `((G + e0)*2 + e1)*2 + e2)*2`. That gives `0x80/0x40/0x20` for the three greater-than tests and `8/4/2` for the equalities. An unordered pair sets CF and ZF, so it adds nothing.
  - `004B9E60`: `(b > a ? 0x10 : 0) + e`, shifted left 2, gives `0x40` and 4.
  - Both match.
- **The divide rows.**
  - `004B9870`: `ucomiss xmm2, 0`. `jp` and `jne` both go to `divss xmm1, xmm2`, so only an ordered equal (including -0.0) stores `0x7F7FFFFF`. "compares equal to 0.0" is exact.
- **The rest.** Each of these was read in full and matches its sentence: `004B9840` (add), `004B9B50` (product), `004B9B80`, `004B9BF0` and `004B9C20` (scale by `[r8]`, `[r8+0xC]` and `[r8+4]`), `004B9BC0` (scale by `xmm2`) and `004B9E30` (subtract `xmm2`). So do the multiply-adds `004B9A10`, `004B9A30`, `004B9A90` and `004B9AF0` (plus `02064B20`-`02064B2C`), and `004B9890` (×16.0 `01CEBC84`, `cvttss2si`). The table reads `004B98F0`, `004B99D0` and `004B99F0` are also exact: `shl edx, 4` then `movsxd`, at `02064E34`/`02064E34`/`02064E38`, storing a word to `[rcx]`, a dword to `[rcx+4]` and a qword to `[rcx+8]`.
- **Host fit.** `004B1190` is cited on this page in the `0x60` row of the type table as that type's program. It is not a neighbour or boundary line. Apart from `_index/ADDRESS-INDEX.md`, no other page cites any of the 23 bodies.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC advisories (not defects)

- The bodies are VU-instruction primitives of the microprogram `004B1190`. They act on the microprogram working registers `02064B00`-`02064E30`, which `17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md` (§3/§4, line 382) describes, and on the R register `01E02828`. This page does not discuss those cells. A one-line pointer from the section intro to that page would help a reader. The batch-4 re-homes put other microprogram helpers on that page (`004CF230`, from `004C8320`). Those were moved only because their first host cited the caller as a foreign mention, which is not the case here.
