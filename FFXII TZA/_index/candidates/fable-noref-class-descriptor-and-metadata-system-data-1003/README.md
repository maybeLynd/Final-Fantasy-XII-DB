# No-reference bodies homed on class-descriptor-and-metadata-system.md by the table or code that reaches them (FABLE, 2026-10-03)

SWE2-EC7 handed FABLE the no-reference remainder on 2026-10-03 (`Database/Tools/work/SWE2-EC7/handoff_noref_to_fable_1003.tsv`). No document cites these functions as a row, and no census-listed instruction calls or jumps to them. I took the rows without the `rtti` column (176 bodies) and swept the certified image for every reference to each entry: absolute qwords and 32-bit image-relative values outside `.text` and `.pdata`, rip-relative operands in `.text` (a raw rel32 sweep, decoded at the instruction start), `[reg+RVA]` forms, and the `FuncInfo` unwind and catch maps that name the exception funclets. I grouped the bodies by the table or function holding the reference and read every listing whole. This record holds the 13 bodies whose referencing table or function this page documents. The full census, with every unhosted body and its reason, is `C:\t\noref_census.tsv`.

## Host choice (FABLE)

Every body is stored into a class or member-descriptor static by a registrar this page tabulates (some cells are bare table cells). `00675740` covers `00677A50` and `008B1D50`. `006A72B0` covers `006A77C0` and `006A77F0`. `006AE350` covers `006AF4E0`. The Point3/Quat/Vector registrars `006B0B20`/`006B0EC0` cover the four float setters, and `006B33F0` (PMatrix4x3) covers `006B3AA0`. The magic static `006372B0` covers `008AF500`. The guarded registration stubs (this page's family) and the other registrars cover the array-member accessors `005C4CC0` (72 sites) and `00671250` (10 sites).

## What the bytes say (FABLE)

These are small accessors: string length + 1 of a tagged pointer, low-bit stripping, count with bit 31 cleared, data pointer by inline-or-heap size, indexed 16-byte element address, float setters, a 12-byte copy, and exit routines that restore a static's `.rdata` address.

## Rows (FABLE)

13 rows, 31 interior anchors, page `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`. Each row's reference is checked at the bytes by `apply.py`.

| function | reference kind | reached from | anchors |
|---|---|---|---|
| `005C4CC0` | code | `005B5130` + 0x2BB | 1 |
| `00671250` | code | `005EFE60` + 0x203 | 5 |
| `00677A50` | code | `00675740` + 0x393 | 3 |
| `006A77C0` | code | `006A72B0` + 0xB1 | 5 |
| `006A77F0` | code | `006A72B0` + 0xF4 | 3 |
| `006AF4E0` | code | `006AE350` + 0x1BF | 2 |
| `006B2E60` | code | `006B0EC0` + 0x413 | 1 |
| `006B2E70` | code | `006B0B20` + 0x1D6 | 1 |
| `006B2E80` | code | `006B0B20` + 0x295 | 1 |
| `006B2E90` | code | `006B0B20` + 0x354 | 1 |
| `006B3AA0` | code | `006B33F0` + 0x1D6 | 4 |
| `008AF500` | code | `006372B0` + 0x48 | 1 |
| `008B1D50` | code | `00675740` + 0x1FB | 3 |

Addresses the sentences cite besides each row's own function and anchors: `005B5130`, `005EFE60`, `00632A10`, `00633770`, `006372B0`, `00675740`, `006A72B0`, `006AE350`, `006B0B20`, `006B0EC0`, `006B33F0`, `00808B90`, `00D26BE0`, `00D6C378`, `01F2E0D0`, `02CB3AD0`, `02CB3B30`, `02CECB08`, `02D3E9D0`, `02E4D790`, `02E4D798`, `02E4FA98`, `02E50968`, `02E509C8`, `02E50A28`, `02E51028`, `02E51728`. These are referencing functions, tables, cells, stored values, callees and import slots. Run the neighbour pre-check (`xlayer_full` edge tokens on these new cites) before publishing.

## Verification (FABLE)

[`apply.py`](apply.py) is the sibling contract (`fable-noref-dyngeo-instance-family-1003/apply.py`) with the owner-token check replaced by a reference check. It refuses to write until all of these pass:

- the page is clean (`git status --short`), and there is at least one row;
- each function is a certified function-list entry that the page does not already cite;
- each sentence has no pipe and is under 1,200 characters;
- each anchor is an instruction boundary strictly inside its function and decodes to the recorded mnemonic;
- each row's reference holds or forms the body's address at the bytes (the kinds are listed in the script's docstring);
- the page cites, outside the new section, the table or function each row names as the reference.

With `--apply` it appends one section, `## No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)`, holding an italic note and the table `| function | size | what the body does | interior anchors |`; anchor cells read Interior anchor `X`. The append keeps the page's line endings and is idempotent: an identical block prints `ALREADY`. The script prints `FAILS n` last.

The dry run is [`apply_dryrun.out`](apply_dryrun.out): `VERIFY 13 functions, 31 anchors, 13 references, page 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md (CRLF)`, `FAILS 0`.

Controls, run on 2026-10-03 with the same `apply.py` from a temporary record that was deleted afterwards:

- one defect per check: a registrar store target off by 8, a swapped registrar, a funclet slot moved one entry, a swapped funclet parent, a table index off by one, a swapped CatchableType, a changed store operand, a wrong mnemonic, a pipe and an uncited token. Each printed its own `VERIFY FAIL` and a non-zero `FAILS`.
- zero rows printed `FAILS 1`, and a dirty page (`the-game-is-a-phyre-application.md`) was refused with `page is dirty`.
- on a copy of this page (`--test-copy`, which skips only the git check), the first `--apply` printed `PATCHED` and the second `ALREADY`. The original bytes are a prefix of the result, and no lone LF appeared in a CRLF page.

## Limits (FABLE)

These are body statements, not meanings. A value read from `.data` is named by address and never stated as a constant. Where a body is reached from several places, the row names one checked reference and counts the rest. The section is appended at publish time, and the publish gates (neighbour pre-check, `verify_doc_addresses`) run on the result. Nothing here is committed. The page and the register are untouched.

## Consumer check (FABLE)

affected: Database/FFXII TZA/22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md

- consumer: this page's new section `No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)`: revised-here (13 rows added; no existing text changed).
- consumer: section `All 15 adapters (OPUS)` (cites `006B0B20`): agrees. The new rows for `006B2E70`, `006B2E80`, `006B2E90` name `006B0B20` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: section `All 15 adapters (OPUS)` (cites `006B0EC0`): agrees. The new row for `006B2E60` names `006B0EC0` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: section `All 15 adapters (OPUS)` (cites `006B33F0`): agrees. The new row for `006B3AA0` names `006B33F0` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: section `All 43 stubs (OPUS)` (cites `005B5130`): agrees. The new row for `005C4CC0` names `005B5130` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: section `All 43 stubs (OPUS)` (cites `005EFE60`): agrees. The new row for `00671250` names `005EFE60` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: section `All 43 stubs (OPUS)` (cites `006A72B0`): agrees. The new rows for `006A77C0`, `006A77F0` name `006A72B0` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: section `All 43 stubs (OPUS)` (cites `006AE350`): agrees. The new row for `006AF4E0` names `006AE350` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: section `SWE2-EC7-119 update (2026-09-21) - the asset-reference registrations measured` (cites `00675740`): agrees. The new rows for `00677A50`, `008B1D50` name `00675740` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: section ``+0x58`, and what selects between its 124 values (OPUS, re-measured 2026-09-25)` (cites `006372B0`): agrees. The new row for `008AF500` names `006372B0` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: the sibling record `fable-noref-class-descriptor-and-metadata-system-1003` (the RTTI rows, its own section): agrees. No function appears in both records.

run: apply.py at 3f236eea3 (dry run FAILS 0)
