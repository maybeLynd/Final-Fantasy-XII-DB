# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-steal-roll-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-STEAL-ROLL-1003` · Package: `_index/candidates/fable-home-the-steal-roll-1003/` (committed in `60f3e63b3`, reviewed at HEAD `33eb7192f`; the package is unmodified in the working tree) · Page: `08-Combat-Formula/Steal/the-steal-roll.md`

## SWE2-AUDIT-SPEC verdict: REJECT

Both sentences are exact against the bytes, and both entered_from sites are direct transfers to the body. **Neither body belongs on this host.**

- The page cites `003939B0` only in a FINAL-AUDIT crossings line and as a co-caller of `002B5AB0`. `003939B0` has its own page.
- The page cites `0017FF20` only as a callee named in passing ("resolve names through `0017FDC0` / `0017FF20`") inside the EC7-107 note about `0023B530`. The fields `001DD0B0` reads are written by a setter stated on the developer-console page.

Both rows should move. Their text can move unchanged.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 2 functions, 10 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. Both rows are on the page (lines 432-433), identical to `rows.json`.
- **`001DD0B0` (0x5C B), read in full:**
  - `r8` = `rcx`, then `rcx` = qword `[01F82D20]`, and `cmp dword [rcx+8], 1`.
  - **Mode 1:** `mov eax, [r8+0x24] / cmp eax, [r8+0x20] / jae` is an unsigned test. It returns `(dword [e] << 16) | dword [e+4]`, where `e = [r8+0x28] + idx*0x1C` (`imul rdx, rax, 0x1C`).
  - **Mode 0** (`test eax, eax / jne`): `eax = [r8+0x34] + 1` (`inc eax`, 32-bit), then `cmp [r8+0x38], eax / jae` is unsigned. The same combination is read from `[r8+0x40]` at index `[r8+0x38]`.
  - **Every other case** (`001DD108`): `rcx` still holds the `[01F82D20]` object, and the body returns its dword `+4`.
  - All clauses and the five anchors are exact.
- **`00394380` (0x7B B), read in full:**
  - `call 00247780` at +0xE with `ecx` = 1.
  - Six qword zero stores cover `rsp+0x20..0x4F`, the 0x30-byte block.
  - `call 002F9860` at +0x38 with `ecx` = 0x890. Its result goes to block `+0`.
  - Block `+8` = `rcx` after `xor ecx, ecx` (0). Block `+0x10` = qword `0208EA28`. Block `+0x18` = `rbx` (the incoming `rcx`). Block `+0x20` = dword 0. Block `+0x2C` = dword 0x1002. Block `+0x28` = byte 2.
  - `call 00241C90` at +0x70 with `ecx` = 0 (not reassigned after `003943BD`) and `rdx` = `&block`. Its `rax` is returned.
  - Exact.
- **entered_from:**
  - `0017FF20` + 0x1A = `0017FF3A`, `jmp 001DD0B0`. `rcx` = the `001DDAB0` result, which is qword `[01F82D18]`, the `0x180`-byte display object (per the developer-console page). It is reached only when that pointer is non-null.
  - `003939B0` + 0x3E4 = `00393D94`, `call 00394380`.
- **Host fit: every citation of the callers on the page.**
  - `003939B0`: line 373 (`## Crossings into other layers — FINAL-AUDIT pass 22`, "`003939B0` calls `001EDE70`, a 7-byte getter") and line 411 (EC7-108 note: "`002B5AB0` ... the word-table text encoder `0023B530` and `003939B0` call"). Neither is a statement about `003939B0`'s body.
  - `003939B0` is the subject of `16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md`: "Selected handler ... `003939B0` at `00394571`" (line 42), receiver alias RSI (line 44). `CONTRACT-widget-object.md:185` calls it "a **different**, 0x1D0 consumer". `00394380` posts a request block of the 0x30-byte `00241C90` form for that consumer. It has nothing to do with the steal roll.
  - `0017FF20`: line 396 only, inside `## SWE2-EC7-107 update - 0023B530 measured`: "arms ... resolve names through `0017FDC0` / `0017FF20`". The body of `0017FF20` is stated on no page.
  - `001DD0B0` reads index fields `+0x24` (mode 1) and `+0x38` (mode 0), selected by dword `+8` of `[01F82D20]`. `001DC920` (31 B) writes exactly these fields under the same test: `cmp dword [rax+8], 0 / jne` writes `+0x24`, otherwise `+0x38`. `001DC920` is stated on `00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md` (line 599, "paired field setter"). That page also states `001DDAB0` (line 120) and identifies `01F82D18` (line 258).

## SWE2-AUDIT-SPEC repair

1. **`00394380`:** move the row unchanged to `16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md`, with entered_from `` `003939B0` + 0x3E4 ``. That page cites the caller in its handler table.
2. **`001DD0B0`:** move the row unchanged to `00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md`, next to the `001DC920` row (it reads what that setter writes).
   - That page does not cite `0017FF20` yet, so the move also homes the caller, `0017FF20` (36 B): "calls `001DDAB0`; when it returns null returns that null, otherwise calls `001DDAB0` again and tail-jumps to `001DD0B0` with the result in `rcx`". Anchors `0017FF24`, `0017FF2C` and `0017FF3A`.
   - Alternatively, keep `001DD0B0` here only after the page states `0017FF20`'s body. A callee named in passing does not host it.
3. Remove both rows from `the-steal-roll.md`. If no other row remains, remove the section heading, intro and table header too.

Limits: static evidence only. A cloud draft plus FABLE's re-read is not independent review; this record is.
