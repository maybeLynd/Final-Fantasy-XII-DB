# No-reference bodies homed on the-fifteen-modules-registered-before-main.md by the table or code that reaches them (FABLE, 2026-10-03)

SWE2-EC7 handed FABLE the no-reference remainder on 2026-10-03 (`Database/Tools/work/SWE2-EC7/handoff_noref_to_fable_1003.tsv`). No document cites these functions as a row, and no census-listed instruction calls or jumps to them. I took the rows without the `rtti` column (176 bodies) and swept the certified image for every reference to each entry: absolute qwords and 32-bit image-relative values outside `.text` and `.pdata`, rip-relative operands in `.text` (a raw rel32 sweep, decoded at the instruction start), `[reg+RVA]` forms, and the `FuncInfo` unwind and catch maps that name the exception funclets. I grouped the bodies by the table or function holding the reference and read every listing whole. This record holds the 5 bodies whose referencing table or function this page documents. The full census, with every unhosted body and its reason, is `C:\t\noref_census.tsv`.

## Host choice (FABLE)

Each body is a stored value or an argument of a registration body this page tabulates. `00637F20` stores `00637350` to `01F2E3B0`. `00661A70` passes `0066F580` as the sixth argument of `006B6820`. `005A65B0` and five more pass `006CD4C0` as the fifth, `006D94E0` and ten more pass `00876870` as the fifth, and `006CE5B0` registers `008B70D0` with `00808B90`. `005C39B0` is left out: OPUS's rows of 2026-10-03 already cite it on this page as a stored value, and the contract refuses a function the page already cites.

## What the bytes say (FABLE)

Two bodies return a string pointer and its length + 1 through `rdx`/`r8` (`006CD4C0`, `00876870`). One looks a name up in a list. One forwards through slot 1 and returns 0x12 on a flag. One is an exit routine.

## Rows (FABLE)

5 rows, 21 interior anchors, page `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md`. Each row's reference is checked at the bytes by `apply.py`.

| function | reference kind | reached from | anchors |
|---|---|---|---|
| `00637350` | code | `00637F20` + 0x1ED | 5 |
| `0066F580` | code | `00661A70` + 0x47 | 5 |
| `006CD4C0` | code | `005A65B0` + 0x53 | 4 |
| `00876870` | code | `006D94E0` + 0x53 | 4 |
| `008B70D0` | code | `006CE5B0` + 0x77 | 3 |

Addresses the sentences cite besides each row's own function and anchors: `005A65B0`, `00637F20`, `00661A70`, `006AA200`, `006B6820`, `006CE5B0`, `006D94E0`, `00808B90`, `00D8A730`, `01F2E3B0`, `02D38DB8`, `02E5C938`. These are referencing functions, tables, cells, stored values, callees and import slots. Run the neighbour pre-check (`xlayer_full` edge tokens on these new cites) before publishing.

## Verification (FABLE)

[`apply.py`](apply.py) is the sibling contract (`fable-noref-dyngeo-instance-family-1003/apply.py`) with the owner-token check replaced by a reference check. It refuses to write until all of these pass:

- the page is clean (`git status --short`), and there is at least one row;
- each function is a certified function-list entry that the page does not already cite;
- each sentence has no pipe and is under 1,200 characters;
- each anchor is an instruction boundary strictly inside its function and decodes to the recorded mnemonic;
- each row's reference holds or forms the body's address at the bytes (the kinds are listed in the script's docstring);
- the page cites, outside the new section, the table or function each row names as the reference.

With `--apply` it appends one section, `## No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)`, holding an italic note and the table `| function | size | what the body does | interior anchors |`; anchor cells read Interior anchor `X`. The append keeps the page's line endings and is idempotent: an identical block prints `ALREADY`. The script prints `FAILS n` last.

The dry run is [`apply_dryrun.out`](apply_dryrun.out): `VERIFY 5 functions, 21 anchors, 5 references, page 22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md (CRLF)`, `FAILS 0`.

Controls, run on 2026-10-03 with the same `apply.py` from a temporary record that was deleted afterwards:

- one defect per check: a registrar store target off by 8, a swapped registrar, a funclet slot moved one entry, a swapped funclet parent, a table index off by one, a swapped CatchableType, a changed store operand, a wrong mnemonic, a pipe and an uncited token. Each printed its own `VERIFY FAIL` and a non-zero `FAILS`.
- zero rows printed `FAILS 1`, and a dirty page (`the-game-is-a-phyre-application.md`) was refused with `page is dirty`.
- on a copy of this page (`--test-copy`, which skips only the git check), the first `--apply` printed `PATCHED` and the second `ALREADY`. The original bytes are a prefix of the result, and no lone LF appeared in a CRLF page.

## Limits (FABLE)

These are body statements, not meanings. A value read from `.data` is named by address and never stated as a constant. Where a body is reached from several places, the row names one checked reference and counts the rest. The section is appended at publish time, and the publish gates (neighbour pre-check, `verify_doc_addresses`) run on the result. Nothing here is committed. The page and the register are untouched.

## Consumer check (FABLE)

affected: Database/FFXII TZA/22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md

- consumer: this page's new section `No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)`: revised-here (5 rows added; no existing text changed).
- consumer: section `Family members explained one by one: Phyre PAnimation module (OPUS, 2026-10-03, opus-member-modules-registered-before-main-phyre-panimation-module-1)` (cites `005A65B0`): agrees. The new row for `006CD4C0` names `005A65B0` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: section `Family members explained one by one: Phyre PGeometry module (OPUS, 2026-10-03, opus-member-modules-registered-before-main-phyre-pgeometry-module-1)` (cites `00661A70`): agrees. The new row for `0066F580` names `00661A70` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: section `Family members explained one by one: Phyre PLOD module (OPUS, 2026-10-03, opus-member-fteen-modules-registered-before-main-phyre-plod-module-1)` (cites `006D94E0`): agrees. The new row for `00876870` names `006D94E0` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: section `SWE2-EC7-50 update (2026-09-19) - `006AA280`` (cites `006CE5B0`): agrees. The new row for `008B70D0` names `006CE5B0` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: section `The `005A08E0` exclusive subtree — all 11 members bound (SWE2-FRONTIER, followup queue)` (cites `00637F20`): agrees. The new row for `00637350` names `00637F20` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: the OPUS rows that write `006B6820(..., 006CD4C0, ...)` and `006B6820(..., 00876870, ...)`: agrees. The fifth-argument position matches the new rows.

run: apply.py at 3f236eea3 (dry run FAILS 0)
