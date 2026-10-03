# No-reference bodies homed on native-command-lifecycle.md by the table or code that reaches them (FABLE, 2026-10-03)

SWE2-EC7 handed FABLE the no-reference remainder on 2026-10-03 (`Database/Tools/work/SWE2-EC7/handoff_noref_to_fable_1003.tsv`). No document cites these functions as a row, and no census-listed instruction calls or jumps to them. I took the rows without the `rtti` column (176 bodies) and swept the certified image for every reference to each entry: absolute qwords and 32-bit image-relative values outside `.text` and `.pdata`, rip-relative operands in `.text` (a raw rel32 sweep, decoded at the instruction start), `[reg+RVA]` forms, and the `FuncInfo` unwind and catch maps that name the exception funclets. I grouped the bodies by the table or function holding the reference and read every listing whole. This record holds the 5 bodies whose referencing table or function this page documents. The full census, with every unhosted body and its reason, is `C:\t\noref_census.tsv`.

## Host choice (FABLE)

All five bodies are callback cells of the native-command tables this page lays out: the family-0 table `0x01EED700` and the shared table `0x01F26720`. A record is 0x20 bytes, with begin at `+8`, poll at `+0x10` and result at `+0x20`, and the count is the dword at `+0`. Each row names the cell, the record index and the command id the index gives, and `apply.py` checks the cell address against base + field + 0x20 * index and the index against the count. The handler bodies cited around these records live on subsystem pages, but this page explains the tables.

## What the bytes say (FABLE)

Two bodies are result callbacks that call one helper and tail-jump to another (`00341D00`, `00352390`). One is a begin callback that stores a 16-bit result to `[r8]`. Two are poll callbacks that return 0 or 1 from a status call on dword `[r8]`. `0050ED10` fills the poll field of two records of the shared table.

## Rows (FABLE)

5 rows, 21 interior anchors, page `01-Script-VM-Native-Bridge/Native-Command-Lifecycle/native-command-lifecycle.md`. Each row's reference is checked at the bytes by `apply.py`.

| function | reference kind | reached from | anchors |
|---|---|---|---|
| `00341D00` | slot | cell `01EF1200` of `01EED700` | 4 |
| `00345A30` | slot | cell `01EEE488` of `01EED700` | 5 |
| `0034AA70` | slot | cell `01EF2AF0` of `01EED700` | 4 |
| `00352390` | slot | cell `01EF04C0` of `01EED700` | 3 |
| `0050ED10` | slot | cell `01F26B10` of `01F26720` | 5 |

Addresses the sentences cite besides each row's own function and anchors: `0025C0F0`, `0026BE50`, `002E08C0`, `002E1130`, `0035A090`, `0035A660`, `003631A0`, `00363B20`, `003C5DF0`, `003C5E00`, `01EED700`, `01EEE488`, `01EF04C0`, `01EF1200`, `01EF2AF0`, `01F26720`, `01F26B10`, `01F26F90`. These are referencing functions, tables, cells, stored values, callees and import slots. Run the neighbour pre-check (`xlayer_full` edge tokens on these new cites) before publishing.

## Verification (FABLE)

[`apply.py`](apply.py) is the sibling contract (`fable-noref-dyngeo-instance-family-1003/apply.py`) with the owner-token check replaced by a reference check. It refuses to write until all of these pass:

- the page is clean (`git status --short`), and there is at least one row;
- each function is a certified function-list entry that the page does not already cite;
- each sentence has no pipe and is under 1,200 characters;
- each anchor is an instruction boundary strictly inside its function and decodes to the recorded mnemonic;
- each row's reference holds or forms the body's address at the bytes (the kinds are listed in the script's docstring);
- the page cites, outside the new section, the table or function each row names as the reference.

With `--apply` it appends one section, `## No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)`, holding an italic note and the table `| function | size | what the body does | interior anchors |`; anchor cells read Interior anchor `X`. The append keeps the page's line endings and is idempotent: an identical block prints `ALREADY`. The script prints `FAILS n` last.

The dry run is [`apply_dryrun.out`](apply_dryrun.out): `VERIFY 5 functions, 21 anchors, 5 references, page 01-Script-VM-Native-Bridge/Native-Command-Lifecycle/native-command-lifecycle.md (LF)`, `FAILS 0`.

Controls, run on 2026-10-03 with the same `apply.py` from a temporary record that was deleted afterwards:

- one defect per check: a registrar store target off by 8, a swapped registrar, a funclet slot moved one entry, a swapped funclet parent, a table index off by one, a swapped CatchableType, a changed store operand, a wrong mnemonic, a pipe and an uncited token. Each printed its own `VERIFY FAIL` and a non-zero `FAILS`.
- zero rows printed `FAILS 1`, and a dirty page (`the-game-is-a-phyre-application.md`) was refused with `page is dirty`.
- on a copy of this page (`--test-copy`, which skips only the git check), the first `--apply` printed `PATCHED` and the second `ALREADY`. The original bytes are a prefix of the result, and no lone LF appeared in a CRLF page.

## Limits (FABLE)

These are body statements, not meanings. A value read from `.data` is named by address and never stated as a constant. Where a body is reached from several places, the row names one checked reference and counts the rest. The section is appended at publish time, and the publish gates (neighbour pre-check, `verify_doc_addresses`) run on the result. Nothing here is committed. The page and the register are untouched.

## Consumer check (FABLE)

affected: Database/FFXII TZA/01-Script-VM-Native-Bridge/Native-Command-Lifecycle/native-command-lifecycle.md

- consumer: this page's new section `No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)`: revised-here (5 rows added; no existing text changed).
- consumer: section `Sixteen families, four distinct tables` (cites `01EED700`): agrees. The new rows for `00341D00`, `00345A30`, `0034AA70`, `00352390` name `01EED700` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: section `Sixteen families, four distinct tables` (cites `01F26720`): agrees. The new row for `0050ED10` names `01F26720` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: the `+24` slot note (unused in all records): agrees. No row touches `+0x18`.

run: apply.py at 3f236eea3 (dry run FAILS 0)
