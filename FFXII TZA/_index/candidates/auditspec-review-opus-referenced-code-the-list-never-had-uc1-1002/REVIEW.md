# SWE2-AUDIT-SPEC review: OPUS UC-1 rows (opus-referenced-code-the-list-never-had-uc1-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-REFERENCED-CODE-THE-LIST-NEVER-HAD-UC1-1002` · Package: `_index/candidates/opus-referenced-code-the-list-never-had-uc1-1002/` · Page: `99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh (verify mode) -> exit 0, `VERIFY 53 functions, 186 anchors / ALREADY / FAILS 0`.
- `rows.json`: 53 rows, 186 anchors; rejected 0, missing 0, skipped 6 (4 single-`jmp` thunks, `0017E760`/`0017E780` dropped for the neighbour gate).
- Test 3 (series break): the literal phrase "UC-1 body admitted to frontier 2026-09-28, explained by interior citation" is in **53 of 53** rows, once each, always followed by ` 2026-10-03`. The page states the count once, in the heading "## 53 UC-1 game-code bodies explained by interior citation (OPUS, 2026-10-02)". The heading date (10-02) and the phrase date (10-03) differ. This is cosmetic.
- Test 2 (semantic pass): **17 rows** were read clause by clause against the certified image, from the applier's own extents (`check_dispositions.load_functions`, `family_prover.load_image`) with rip targets resolved. The 17 are `00125743`, `001DDAC0`, `00269E00`, `002E4C90`, `002E5B00`, `002EC3C0`, `002ECD20`, `002FE7D0`, `003594C0`, `0037AA00`, `003B6950`, `0055B310`, `00710000`, `008858B0`, `00892990`, `00893AC0` and `00895570`. Every body clause is exact. Checked in detail:
  - `001DDAC0`: `comiss`/`jb` and `jbe` polarity, the NaN path, and `+0x14` overwritten on the first path.
  - `002E5B00`: `[rsp+0x28]` is entry+0x28, the fifth argument; no frame.
  - `002FE7D0`: truncation happens before the `imul` by the `cwde` word; the compare is signed `jl`.
  - `003594C0`: the `cmovne` reads flags from `test dl,dl`.
  - `0055B310`: the signed `jge 0x20` on byte `+0x408` and the xor-mask nibble copy.
  - `008858B0`: the stack slots are 5th to 8th arguments, `setbe` includes unordered, and the 8-byte abs mask.
  - `00893AC0`: `cdq`/`xor`/`sub` abs, then `idiv`.
  - `00895570`: `seta` minus `seta`.
- Test 1 (entry statements), **all 53 rows**, checked at the bytes:
  - **20 "entered from / by a jump from" rows.** Every site decodes to a `call`/`jmp` whose target is the body. The two `0037C3F0` call sites (+0x150 and +0x1F8) lie past that function's recorded 248-byte extent, but they decode in its linear flow after the `jmp rcx` table dispatch. The statement holds.
  - **2 table rows.** Qwords `01EEC568` = `002FE7D0` and `01F003A0` = `004223F0`.
  - **31 "no direct reference was found (call/jump, rip-reference and table scans)" rows.** An image-wide raw census was run over the executable sections: `E8`/`E9`/`0F 8x`/`EB`/`7x` targets; qwords equal to the start; 32-bit image-relative values equal to the start; and every rip-disp32 candidate, decoded in its container. **15 of the 31 are referenced.** See the defect. The other 16 are clean. Their raw hits are not references: `00125753`'s RVA bytes sit inside string data and an unrelated `lea`, and the `.pdata` hits for `0031AD90`/`003F5030` are the previous function's EndAddress.
- "Starts right after a `ret` / `int3` padding / not 16-byte aligned": every such clause matches the preceding bytes (for example, `00125743` follows `0F 77 C3` (`emms; ret`) at `00125740`, and `002ED250` follows the `ret` at `002ED24F`).

## SWE2-AUDIT-SPEC narrowing / notes

**Defect (test 1, 15 rows): "no direct reference was found" is false.** The census behind these heads, `Tools/work/OPUS/cloud/uc1_credible.py`, takes `direct` from `retool.scan()["calls"]`. That index does not include `0F 8x` conditional-jump rel32 sites, and the table scan only matches aligned qwords. The rows faithfully copy `uc1_credible.json` (`"direct": []`, verdict `FOLLOWS`), so the census is what is short. Each site below is an instruction boundary inside a listed function's extent, linearly decoded from that function's start:

| body | instruction-level evidence | replace "no direct reference was found (call/jump, rip-reference and table scans)" with |
|---|---|---|
| `00195340` | `.rdata` `01DEAAA0` = {0, RVA 0x75340, 0, RVA 0x1CCAAC0}: a C++ ThrowInfo whose catchable-type array `01DEAAC0` lists `.?AVbad_cast@std@@` and `.?AVexception@std@@`; `pmfnUnwind` (at `01DEAAA4`) = `00195340` | entered through the 32-bit image-relative destructor field at `01DEAAA4` of the C++ throw-info record for `std::bad_cast` at `01DEAAA0` |
| `002969D0` | `002905C3 jne 0x2969d0` (in `002905B0`, after `test rcx,rcx`) | entered by a conditional jump (`jne`) from `002905B0` + 0x13 |
| `002E4C90` | `002673DD je 0x2e4c90` (in `002673D0`) | entered by a conditional jump (`je`) from `002673D0` + 0xD |
| `002E5B00` | `0026A428 je 0x2e5b00` (in `0026A420`) | entered by a conditional jump (`je`) from `0026A420` + 0x8 |
| `002ED250` | `003EB8CC jge 0x2ed250` (in `003EB8C0`, `rcx` advanced by 0x10 first) | entered by a conditional jump (`jge`) from `003EB8C0` + 0xC |
| `002ED350` | `003EB96C jge 0x2ed350` (in `003EB960`) | entered by a conditional jump (`jge`) from `003EB960` + 0xC |
| `0031AD90` | `00359B8C jne 0x31ad90` (in `00359B80`, `rcx` = qword `+0x30` first) | entered by a conditional jump (`jne`) from `00359B80` + 0xC |
| `00365660` | `0029CCF5 jg 0x365660` (in `0029CCF0`) | entered by a conditional jump (`jg`) from `0029CCF0` + 0x5 |
| `00379F50` | `00379868 jne 0x379f50` (in `00379860`) | entered by a conditional jump (`jne`) from `00379860` + 0x8 |
| `0037AA00` | `003DEA12 jne 0x37aa00` (in `003DEA10`) | entered by a conditional jump (`jne`) from `003DEA10` + 0x2 |
| `003DCF20` | `003DC7C3 je 0x3dcf20` (in `003DC780`) | entered by a conditional jump (`je`) from `003DC780` + 0x43 |
| `003F5030` | `00290BF6 jne 0x3f5030` (in `00290BE0`) | entered by a conditional jump (`jne`) from `00290BE0` + 0x16 |
| `003F7000` | `00290953 jne 0x3f7000` (in `00290940`) | entered by a conditional jump (`jne`) from `00290940` + 0x13 |
| `004278D0` | `002EB4DA jne 0x4278d0` (in `002EB4A0`) | entered by a conditional jump (`jne`) from `002EB4A0` + 0x3A |
| `0042FCC0` | `00317EC6 ja 0x42fcc0` (in `00317EC0`) | entered by a conditional jump (`ja`) from `00317EC0` + 0x6 |

The clause after it ("it starts right after `int3` padding" / "a `ret`") is true and may stay. The body sentences of these rows are not affected: the three in the semantic sample (`002E4C90`, `002E5B00`, `0037AA00`) are exact. If citing a caller pulls a cross-layer edge into the page, write that caller as a plain address, as OPUS did for `0017E760`. The replacement must still name the site.

**Repair:** apply the 15 replacements, then re-run `interior_applier.py --apply` and the neighbour gate. Re-run `uc1_credible.py` with `0F 8x` jcc sites and 32-bit image-relative fields added to the census before the remaining F-unmet UC-1 bodies are drafted. A `FOLLOWS` verdict from the current census is not evidence of "no reference". The other 38 rows pass tests 1-3 as read. The producer repairs its own rows.
