# No-reference bodies homed on choosing-the-field-environment-variant.md by the table or code that reaches them (FABLE, 2026-10-03)

SWE2-EC7 handed FABLE the no-reference remainder on 2026-10-03 (`Database/Tools/work/SWE2-EC7/handoff_noref_to_fable_1003.tsv`). No document cites these functions as a row, and no census-listed instruction calls or jumps to them. I took the rows without the `rtti` column (176 bodies) and swept the certified image for every reference to each entry: absolute qwords and 32-bit image-relative values outside `.text` and `.pdata`, rip-relative operands in `.text` (a raw rel32 sweep, decoded at the instruction start), `[reg+RVA]` forms, and the `FuncInfo` unwind and catch maps that name the exception funclets. I grouped the bodies by the table or function holding the reference and read every listing whole. This record holds the 1 bodies whose referencing table or function this page documents. The full census, with every unhosted body and its reason, is `C:\t\noref_census.tsv`.

## Host choice (FABLE)

`MapRef_BeginLoadResources` (`00268750`), the `map_ref.bin` loader this page names in its MRF row, stores the body's address at stack `+0x40` just before its `0036C1D0` call. No other reference exists.

## What the bytes say (FABLE)

It resolves the dword offset at `+0x14` of the loaded image (`02099D88`) to a pointer and stores it to `02099D90`.

## Rows (FABLE)

1 rows, 3 interior anchors, page `03-World-Area-Field/choosing-the-field-environment-variant.md`. Each row's reference is checked at the bytes by `apply.py`.

| function | reference kind | reached from | anchors |
|---|---|---|---|
| `002678A0` | code | `00268750` + 0x54 | 3 |

Addresses the sentences cite besides each row's own function and anchors: `00268750`, `0036C1D0`, `02099D88`, `02099D90`. These are referencing functions, tables, cells, stored values, callees and import slots. Run the neighbour pre-check (`xlayer_full` edge tokens on these new cites) before publishing.

## Verification (FABLE)

[`apply.py`](apply.py) is the sibling contract (`fable-noref-dyngeo-instance-family-1003/apply.py`) with the owner-token check replaced by a reference check. It refuses to write until all of these pass:

- the page is clean (`git status --short`), and there is at least one row;
- each function is a certified function-list entry that the page does not already cite;
- each sentence has no pipe and is under 1,200 characters;
- each anchor is an instruction boundary strictly inside its function and decodes to the recorded mnemonic;
- each row's reference holds or forms the body's address at the bytes (the kinds are listed in the script's docstring);
- the page cites, outside the new section, the table or function each row names as the reference.

With `--apply` it appends one section, `## No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)`, holding an italic note and the table `| function | size | what the body does | interior anchors |`; anchor cells read Interior anchor `X`. The append keeps the page's line endings and is idempotent: an identical block prints `ALREADY`. The script prints `FAILS n` last.

The dry run is [`apply_dryrun.out`](apply_dryrun.out): `VERIFY 1 functions, 3 anchors, 1 references, page 03-World-Area-Field/choosing-the-field-environment-variant.md (LF)`, `FAILS 0`.

Controls, run on 2026-10-03 with the same `apply.py` from a temporary record that was deleted afterwards:

- one defect per check: a registrar store target off by 8, a swapped registrar, a funclet slot moved one entry, a swapped funclet parent, a table index off by one, a swapped CatchableType, a changed store operand, a wrong mnemonic, a pipe and an uncited token. Each printed its own `VERIFY FAIL` and a non-zero `FAILS`.
- zero rows printed `FAILS 1`, and a dirty page (`the-game-is-a-phyre-application.md`) was refused with `page is dirty`.
- on a copy of this page (`--test-copy`, which skips only the git check), the first `--apply` printed `PATCHED` and the second `ALREADY`. The original bytes are a prefix of the result, and no lone LF appeared in a CRLF page.

## Limits (FABLE)

These are body statements, not meanings. A value read from `.data` is named by address and never stated as a constant. Where a body is reached from several places, the row names one checked reference and counts the rest. The section is appended at publish time, and the publish gates (neighbour pre-check, `verify_doc_addresses`) run on the result. Nothing here is committed. The page and the register are untouched.

## Consumer check (FABLE)

affected: Database/FFXII TZA/03-World-Area-Field/choosing-the-field-environment-variant.md

- consumer: this page's new section `No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)`: revised-here (1 rows added; no existing text changed).
- consumer: section `(page head)` (cites `00268750`): agrees. The new row for `002678A0` names `00268750` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.

run: apply.py at 3f236eea3 (dry run FAILS 0)
