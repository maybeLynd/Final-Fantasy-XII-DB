# No-reference bodies homed on CONTRACT-authored-table-row-lookup.md by the table or code that reaches them (FABLE, 2026-10-03)

SWE2-EC7 handed FABLE the no-reference remainder on 2026-10-03 (`Database/Tools/work/SWE2-EC7/handoff_noref_to_fable_1003.tsv`). No document cites these functions as a row, and no census-listed instruction calls or jumps to them. I took the rows without the `rtti` column (176 bodies) and swept the certified image for every reference to each entry: absolute qwords and 32-bit image-relative values outside `.text` and `.pdata`, rip-relative operands in `.text` (a raw rel32 sweep, decoded at the instruction start), `[reg+RVA]` forms, and the `FuncInfo` unwind and catch maps that name the exception funclets. I grouped the bodies by the table or function holding the reference and read every listing whole. This record holds the 1 bodies whose referencing table or function this page documents. The full census, with every unhosted body and its reason, is `C:\t\noref_census.tsv`.

## Host choice (FABLE)

The only reference is in `0020D2F0`, which forms the body's address in `rcx` for its indirect `call r9` (with `edx` = 1). This page says `0020D2F0` builds the object through `LoadLibrary` of `atiadlxx.dll`.

## What the bytes say (FABLE)

It sign-extends `ecx` and tail-jumps through the import slot `008C2B40`.

## Rows (FABLE)

1 rows, 1 interior anchors, page `02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md`. Each row's reference is checked at the bytes by `apply.py`.

| function | reference kind | reached from | anchors |
|---|---|---|---|
| `0020D7B0` | code | `0020D2F0` + 0x340 | 1 |

Addresses the sentences cite besides each row's own function and anchors: `0020D2F0`, `008C2B40`. These are referencing functions, tables, cells, stored values, callees and import slots. Run the neighbour pre-check (`xlayer_full` edge tokens on these new cites) before publishing.

## Verification (FABLE)

[`apply.py`](apply.py) is the sibling contract (`fable-noref-dyngeo-instance-family-1003/apply.py`) with the owner-token check replaced by a reference check. It refuses to write until all of these pass:

- the page is clean (`git status --short`), and there is at least one row;
- each function is a certified function-list entry that the page does not already cite;
- each sentence has no pipe and is under 1,200 characters;
- each anchor is an instruction boundary strictly inside its function and decodes to the recorded mnemonic;
- each row's reference holds or forms the body's address at the bytes (the kinds are listed in the script's docstring);
- the page cites, outside the new section, the table or function each row names as the reference.

With `--apply` it appends one section, `## No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)`, holding an italic note and the table `| function | size | what the body does | interior anchors |`; anchor cells read Interior anchor `X`. The append keeps the page's line endings and is idempotent: an identical block prints `ALREADY`. The script prints `FAILS n` last.

The dry run is [`apply_dryrun.out`](apply_dryrun.out): `VERIFY 1 functions, 1 anchors, 1 references, page 02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md (LF)`, `FAILS 0`.

Controls, run on 2026-10-03 with the same `apply.py` from a temporary record that was deleted afterwards:

- one defect per check: a registrar store target off by 8, a swapped registrar, a funclet slot moved one entry, a swapped funclet parent, a table index off by one, a swapped CatchableType, a changed store operand, a wrong mnemonic, a pipe and an uncited token. Each printed its own `VERIFY FAIL` and a non-zero `FAILS`.
- zero rows printed `FAILS 1`, and a dirty page (`the-game-is-a-phyre-application.md`) was refused with `page is dirty`.
- on a copy of this page (`--test-copy`, which skips only the git check), the first `--apply` printed `PATCHED` and the second `ALREADY`. The original bytes are a prefix of the result, and no lone LF appeared in a CRLF page.

## Limits (FABLE)

These are body statements, not meanings. A value read from `.data` is named by address and never stated as a constant. Where a body is reached from several places, the row names one checked reference and counts the rest. The section is appended at publish time, and the publish gates (neighbour pre-check, `verify_doc_addresses`) run on the result. Nothing here is committed. The page and the register are untouched.

## Consumer check (FABLE)

affected: Database/FFXII TZA/02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md

- consumer: this page's new section `No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)`: revised-here (1 rows added; no existing text changed).
- consumer: section `The image-address base: what the image initialises, and what later code could write — reconciled 2026-09-24 (FABLE, Claude Opus 5.5)` (cites `0020D2F0`): agrees. The new row for `0020D7B0` names `0020D2F0` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: the resource-request-queue page's note that `0020D7B0` is an address-taken `malloc` wrapper: agrees, but that page is not affected.

run: apply.py at 3f236eea3 (dry run FAILS 0)
