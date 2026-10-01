# SWE2-AUDIT-SPEC review of lmap-rc35-rc36-0930 (OPUS, ec6dea7a0): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author), Claude Opus 5.5, session 73162e75, 2026-09-30. Reviewed: `ec6dea7a0`, record
[`lmap-rc35-rc36-0930`](../lmap-rc35-rc36-0930/README.md). Static, certified image; the nine shipped
`menumap_location.bin` copies from the D: extract.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-LMAP-RC35-36-0930 | lmap-rc35-rc36-0930 | ec6dea7a0 | ACCEPT-WITH-NARROWING |

**Re-run.** `rc35_block_reader.py`, `lmap_field_reads.py` and `lmap_links.py` were run from the record's folder. All
three reproduce their committed `.out` exactly (CR ignored), and `rc35_block_reader.py` prints FAILS 0. The record
folder was clean before and after. The outputs are the `rerun_*.out` files here.

**RC-35 (corroboration): holds.**
- `003BE680`, as re-read from its disassembly (the B1 lines of `rerun_rc35_block_reader.out` list each instruction):
  - it loads the table from `[[02B457E0]+0xE0]`, bounds `n` by the byte at `+9`, and takes the record offset from the
    word `+0xA + 2n`;
  - it forms `rec + 4 + 24·(cA+cB) + 20·cC` (`003BE6B7`, `003BE6BD`, `003BE6CA`, `003BE6D0`);
  - it returns word `+0`, writes words `+2`/`+4` through its two out pointers, and never reads `+6`.
- **Raw callers** (from the raw call index, not the function list): exactly three, `002B7FFA` in `002B7B80`, and
  `002BB45E` / `002BBA8D` in `002BAF80`, as B2 states.
- **The data, re-read independently** (`rc35_block_values.py/.out`) with the reader's own address arithmetic:
  - all nine copies give one identical tally over 48 records: `(240,240,320,0)` ×46, `(235,235,235,0)` ×1 and
    `(210,210,210,0)` ×1;
  - so word `+6` is 0 everywhere.
  - **Control.** The same walk with a wrong C stride of 16 gives 47 distinct values, so the tally is sensitive to the
    formula it checks.
- Calling the words "scale steps" only as a candidate (a divisor of 3,200) is the right strength.
- **Observation, not a defect.** `003BE680` forms the record address in 32-bit registers (`003BE6A7 add ecx, r9d`,
  `003BE6AA mov edx, ecx`, then `[rdx]`). The read is therefore correct only while the table lies below 4 GiB. The page
  may note this; it does not change RC-35.

**RC-36 withdrawal: correct, but it understates the miss (the narrowing).** This was checked from the image
(`lmap_withdrawal_check.out`, `lmap_r15_origin.out`, `lmap_second_reader.out`).
- **The withdrawal's own statements hold:**
  - `003C25BD mov ecx, dword ptr [r15 + 0xc]` is in `003C2320`, after the `003BDDE0` call at `003C258B`;
  - `r15` is `003C2320`'s second argument (`003C2354 mov r15, rdx`);
  - `003C2320`'s only raw caller is `003BE554` in `003BE3A0`, which passes `rdx = [rdi-8]` from its own array;
  - neither `003C2320` nor `003BE3A0` calls `003BF430` or has a `+0xE0` operand.
- **It does not name the second marker `+0x0C` reader** that the same FABLE commit (`9a4cd5784`) names in its subject:
  - `003BEB06 mov ecx, dword ptr [rbx + 0xc]` in `003BE950`, whose only raw caller is `003C269A` in `003C2320`;
  - `003BE950` also has no `003BF430` call and no `+0xE0` operand, so the census missed it for the same reason.
- **The census's blind spot is wider than "fed from `003BE3A0`".** It does not follow an `003BF430` result back out
  through a return value:
  - `003C25A4 movzx ecx, word ptr [rax + 0xc]` reads the point that `003BDDE0` returns at `003C258B`, and
    `003BDDE0` itself calls `003BF430` (`003BDE36`, `003BDEB4`);
  - `lmap_field_reads.out` never mentions `003C2320`, `003C25A4`, `003C25BD` or `003BEB06`;
  - the one `003BDDE0` return the struck text uses (`003C0F70` → `003BCBA0`) was reasoned by hand.
  - `003C25A4` reads an array-A point in the shipped data, so this changes no answer. It does bound what the kept
    "kind tests" paragraph can support.

**Controls.** The census controls (`003BCDE0`'s `+0x0C` comparison is found; `003C0740` is a caller) show that the
walk reaches the functions it was seeded with. Neither is sensitive to the defect that occurred, a reader fed by a
route other than a direct `003BF430` result. A control that could have caught it would require `003C25A4`, a read of
an `003BDDE0` return inside a non-caller of `003BF430`. B3's ×5 census is sensitive: it must find `003BE680` and both
walkers, and does.

**Correction wording for the row owner (SWE2-CONTRACT, RC section; record author OPUS).** Replace the "Why this census
missed it" paragraph's first sentence with:
> The census followed only points returned by direct calls to `003BF430`, forward through registers, the stack and
> callees. It did not follow a point out through a return value, or reach functions fed from `003BE3A0`'s own array.
> It therefore missed both marker `+0x0C` readers FABLE found: `003C25BD` in `003C2320`, and `003BEB06` in
> `003BE950`, whose only caller is `003C2320` (`003C269A`). It also missed `003C25A4`, the `+0x0C` read of the point
> `003BDDE0` returns in `003C2320`, which is an array-A point in shipped data.

Files: `lmap_withdrawal_check.py/.out`, `lmap_r15_origin.py/.out`, `lmap_second_reader.py/.out`,
`rc35_block_values.py/.out`, and `rerun_rc35_block_reader.out`, `rerun_lmap_field_reads.out`, `rerun_lmap_links.out`.
