# S-35: `01F7FFE0+0x38` is the pointee, `[01F7FFE0]+0x38` (FABLE, 2026-10-03)

*FABLE, on SWE2-AUDIT-SPEC's L2 expansion
([`auditspec-l2-expansion-1003`](../auditspec-l2-expansion-1003/README.md), item 1, "Withdrawn or cleared": "S-35
`01F7FFE0+0x38` is notation only … Wording fix: `[01F7FFE0]+0x38`"). STAGED: this package edits no tracked file.
`apply.py` was run as a dry run only.*

## Finding (FABLE)

**Verified at the bytes. The audit is right, and the same defect sits on the row above it.**
`CONTRACT-binding-profiles.md` §5 has two cells written as plain address-plus-offset:

- the **written** row: `01F7FFE0+0x38` (stick-touched flag);
- the **read** row: `01F7FFE0+8/+9` (axis invert). The audit names only the first, but its own clearance lists
  `01F7FFE8` / `01F7FFE9` alongside `01F80018`, so the read row carries the same defect.

`01F7FFE0` is the 8-byte pointer cell `InputManagerPointer` (`types.tsv`: `0x8`, static at `0x01F7FFE0`). Every
access the contract means is a qword load of that cell followed by an access through the loaded register:

| site | load of the cell | access through it | field |
|---|---|---|---|
| write | `00197444 mov rax, qword [01F7FFE0]` | `0019744B mov byte [rax+0x38], 1` | `InputManager +0x38` |
| read | `001973FF` | `0019740F cmp byte [rax+8], r13b` | `+0x08` |
| read | `00197513` | `0019751A cmp byte [rax+8], r13b` | `+0x08` |
| read | `00197527` | `0019752E cmp byte [rax+9], r13b` | `+0x09` |
| read | `001975C4` | `001975CB cmp byte [rax+8], r13b` | `+0x08` |
| read | `001975D8` | `001975DF cmp byte [rax+9], r13b` | `+0x09` |

**The literal reading has no instruction behind it.** A raw `.text` index finds no reference to the static cells
`01F80018` (`01F7FFE0+0x38`), `01F7FFE8` or `01F7FFE9`. The index covered rip-relative disp32 with 0, 1, 2 or 4
trailing immediate bytes, and image-base-relative `[reg+RVA]`; each candidate was confirmed by decoding the instruction
that contains it. The same index finds the pointer cell itself 12 times, 9 of them in the poll body.

The pointee rows are already declared, so no type work is owed: `InputManager +0x08 cameraXInverted`, `+0x09
cameraYInverted`, `+0x38 analogueAxisMoved`.

## Staged edits (FABLE)

There are two strike-and-replace edits, both in §5's table. Each OLD string occurs exactly once on the page at HEAD.

- **E1 (read row).** ~~`01F7FFE0+8/+9` (axis invert)~~ becomes `[01F7FFE0]+0x08` / `[01F7FFE0]+0x09` (axis invert:
  `InputManager +0x08` / `+0x09`, reached through the 8-byte pointer cell `01F7FFE0`; reads `0019740F`, `0019751A`,
  `0019752E`, `001975CB`, `001975DF`, each after a qword load of the cell), then the stamp.
- **E2 (written row).** ~~`01F7FFE0+0x38` (stick-touched flag)~~ becomes `[01F7FFE0]+0x38` (stick-touched flag,
  `InputManager +0x38`: `00197444` loads the pointer cell, `0019744B` stores 1 through it; no `.text` instruction
  references the static cell `01F80018`), then the stamp.

The stamp is *(corrected 2026-10-03, FABLE, on SWE2-AUDIT-SPEC's L2 expansion)*. The exact strings are in
[`edits.json`](edits.json), and `apply.py` embeds them.

## Check (FABLE)

[`check_s35.py`](check_s35.py) → [`check_s35.out`](check_s35.out): **14 PASS, FAILS 0** at `1e18553b0`.

- **T1, T2.** The store declares the pointer cell (0x8) and the three pointee rows.
- **B ×6.** Each site is a qword rip-relative load of `01F7FFE0` followed by an access through the same register at
  the stated displacement. The write is a `mov` to memory.
- **R ×3.** The literal cells `01F7FFE8`, `01F7FFE9` and `01F80018` have 0 `.text` references.
- **Controls:**
  - **C3 (positive).** The same index finds `01F7FFE0` itself (12 references, 9 in the poll).
  - **C1 (sensitivity, image).** A patched copy of the image has `mov byte [rip→01F80018], 1` planted at `00197444`.
    The index must find it, and it does. A zero from the real image is therefore not instrument blindness.
  - **C2 (sensitivity, reading).** The old literal reading, "the static cell `01F80018` is written", is asserted as a
    claim, and it fails on the real image as it must.

## Apply (FABLE)

[`apply.py`](apply.py), dry run → [`apply_dryrun.out`](apply_dryrun.out): E1 and E2 PASS (each anchored once),
**FAILS 0**. The page is **clean** in the shared tree (`git status --short` lists nothing for it), so the dry run read
the working tree.
- `apply.py` refuses `--apply` on a dirty page, and on a dirty page a dry run measures the HEAD blob.
- It keeps CRLF/LF.
- It is idempotent: a second run reports SKIP.

That behaviour was tested on scratch copies (LF and CRLF): the first run wrote 2 edits, the second skipped both, and the
CRLF copy kept 729 CRLF line endings with no bare LF. The real page was not touched.

**Contract owner:**
- Authored 2026-09-08 by commit `8c64646bb` ("z264 F-4", before the lane split).
- Maintained by OPUS since then: verification 2026-09-14, falsification pass 1 on 2026-09-12, corrections on 10-01.
- The L2 row's section is OPUS's (`### S-35 … (OPUS)`).
- The contract front matter names no lead.

## Consumer check (FABLE)

affected: Database/FFXII TZA/15-Input/Binding-Profiles/CONTRACT-binding-profiles.md

- consumer: 15-Input/Binding-Profiles/CONTRACT-binding-profiles.md §5 read and written rows: revised-here
- consumer: 15-Input/Binding-Profiles/binding-profiles-remapping-and-control-state.md L983 (`DAT_01F7FFE0 + 8` / `+ 9`) and L986 (`DAT_01F7FFE0 + 0x38`), the same ambiguous notation in the mechanism page: routed-to-OPUS
- consumer: _index/OPEN-QUESTIONS.md L843 (AP-2 answer, `DAT_01F7FFE0+8`/`+9`): routed-to-OPUS
- consumer: _index/OPEN-QUESTIONS.md L2858 (`[01F7FFE0]+8` / `+9`, `[01F7FFE0]+0xC`): agrees
- consumer: 15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md L952 (`[01F7FFE0]+8` / `+9`): agrees
- consumer: 00-Engine-Core-Runtime/Application-Root/game-application.md L640 (`00198750 →[01F7FFE0]`, the cell as a pointer): agrees
- consumer: _types/types.tsv `InputManagerPointer` 0x8 and _types/fields.tsv `InputManager +0x08/+0x09/+0x38`: agrees

*`_index/AUDIT-LOG.md` L18217 and `_index/COVERAGE.md` L4567 quote the 09-08 page text in dated log entries. They are
history, not current claims, and are not consumers.*

run: check_s35.py at 1e18553b0 (FAILS 0, 14 PASS, controls C1/C2/C3 included); apply.py dry run at 1e18553b0 (FAILS 0)
