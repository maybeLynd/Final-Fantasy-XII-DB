# No-reference bodies homed on exception-funclets-and-lazy-static-guards.md by the table or code that reaches them (FABLE, 2026-10-03)

SWE2-EC7 handed FABLE the no-reference remainder on 2026-10-03 (`Database/Tools/work/SWE2-EC7/handoff_noref_to_fable_1003.tsv`). No document cites these functions as a row, and no census-listed instruction calls or jumps to them. I took the rows without the `rtti` column (176 bodies) and swept the certified image for every reference to each entry: absolute qwords and 32-bit image-relative values outside `.text` and `.pdata`, rip-relative operands in `.text` (a raw rel32 sweep, decoded at the instruction start), `[reg+RVA]` forms, and the `FuncInfo` unwind and catch maps that name the exception funclets. I grouped the bodies by the table or function holding the reference and read every listing whole. This record holds the 33 bodies whose referencing table or function this page documents. The full census, with every unhosted body and its reason, is `C:\t\noref_census.tsv`.

## Host choice (FABLE)

The 33 bodies are reached only through exception funclets in the block `00896280`-`008A6960`, the block this page documents as a population. 32 are the tail-jump targets of cleanup funclets (`lea rcx,[rdx+X]` or `mov rcx,[rdx+X]` then `jmp`). One, `00206CD0`, is called by a catch funclet. I found every funclet's parent from its own data. The funclet's image-relative address sits in an action field of an unwind map, or in a catch-handler field of a try-block map, and that map belongs to the FuncInfo (magic `0x19930522`) that the parent function's own `.pdata` unwind record names. The page explains this ABI (RDX = parent frame, cleanup funclets tail-jump into the destructor) and the FuncInfo layout. The parents themselves are spread over many subsystems, so one row per parent's page would scatter a single mechanism.

## What the bytes say (FABLE)

Most of the bodies are container or allocator releases: when a begin pointer is non-null, they call slot 3 of an embedded allocator object with the pointer and the byte span. The span is rounded to the element size by a multiply-high division (0x118, 0x220, 0x3C, 0x318, 0x24, 0x128, 0xA, 0x28, 0x30) or by masking low bits. The others are: releases through slot 2 of an object and then slot 0 of the object it returns; two bodies that call import slots and then slot 2 through a virtual-base offset; small field clears; and two bodies that store an `.rdata` address at `+0` and, on a flag bit, tail-jump through an import slot. `001A2830` alone is reached from 76 funclets.

## Rows (FABLE)

33 rows, 126 interior anchors, page `24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md`. Each row's reference is checked at the bytes by `apply.py`.

| function | reference kind | reached from | anchors |
|---|---|---|---|
| `00195360` | funclet | funclet `00896DB0` (FuncInfo of `00197A50`, field `01D56674`) | 4 |
| `001953A0` | funclet | funclet `008968BC` (FuncInfo of `00194B00`, field `01D55F50`) | 5 |
| `001953F0` | funclet | funclet `0089690C` (FuncInfo of `00194CD0`, field `01D55E6C`) | 5 |
| `0019A4F0` | funclet | funclet `00896D00` (FuncInfo of `0019AA20`, field `01D5657C`) | 1 |
| `0019DD30` | funclet | funclet `00896EB0` (FuncInfo of `0019D740`, field `01D56E1C`) | 4 |
| `0019DD90` | funclet | funclet `00896EF0` (FuncInfo of `0019E010`, field `01D56DA0`) | 3 |
| `001A2830` | funclet | funclet `00897020` (FuncInfo of `001A2130`, field `01D57A90`) | 4 |
| `001A28D0` | funclet | funclet `0089711C` (FuncInfo of `001A2F70`, field `01D58300`) | 4 |
| `001A2D50` | funclet | funclet `00897065` (FuncInfo of `001A2130`, field `01D57AB0`) | 5 |
| `001A2E10` | funclet | funclet `00897110` (FuncInfo of `001A2F70`, field `01D582F8`) | 4 |
| `001AADE0` | funclet | funclet `00897410` (FuncInfo of `001ADD30`, field `01D594AC`) | 5 |
| `001AAEE0` | funclet | funclet `0089727C` (FuncInfo of `001AA840`, field `01D588AC`) | 3 |
| `001AE130` | funclet | funclet `008974EC` (FuncInfo of `001AE550`, field `01D599F8`) | 4 |
| `001BCD90` | funclet | funclet `00897BF8` (FuncInfo of `001BCE30`, field `01D5B804`) | 5 |
| `001BE990` | funclet | funclet `00897CA0` (FuncInfo of `001BE730`, field `01D5BB84`) | 5 |
| `001DE300` | funclet | funclet `0089840A` (FuncInfo of `001DE5D0`, field `01D5E13C`) | 3 |
| `001DE330` | funclet | funclet `00898480` (FuncInfo of `001DEE90`, field `01D5E27C`) | 3 |
| `001DE360` | funclet | funclet `00898E31` (FuncInfo of `002002E0`, field `01D6102C`) | 3 |
| `001E1B20` | funclet | funclet `008984FC` (FuncInfo of `001E1670`, field `01D5EA5C`) | 4 |
| `001E1C60` | funclet | funclet `0089850C` (FuncInfo of `001E1670`, field `01D5EA64`) | 3 |
| `001E76B0` | funclet | funclet `00898660` (FuncInfo of `001E7480`, field `01D5EDBC`) | 4 |
| `001F5080` | funclet | funclet `0089899C` (FuncInfo of `001F4DA0`, field `01D60588`) | 4 |
| `001F50E0` | funclet | funclet `008989AC` (FuncInfo of `001F4DA0`, field `01D60590`) | 4 |
| `001FC2E0` | funclet | funclet `00898AAC` (FuncInfo of `001FC640`, field `01D60E9C`) | 3 |
| `00204540` | funclet | funclet `00899A08` (FuncInfo of `0020A800`, field `01D62684`) | 4 |
| `00204590` | funclet | funclet `008999D0` (FuncInfo of `0020A800`, field `01D62664`) | 4 |
| `00206CD0` | funclet | funclet `008996A0` (FuncInfo of `00206AD0`, field `01D62FF0`) | 5 |
| `0020C860` | funclet | funclet `00899B00` (FuncInfo of `0020C730`, field `01D63F4C`) | 3 |
| `0020C880` | funclet | funclet `00899B10` (FuncInfo of `0020C730`, field `01D63F54`) | 3 |
| `00211A60` | funclet | funclet `00899CE0` (FuncInfo of `002116B0`, field `01D64904`) | 4 |
| `0021EBC0` | funclet | funclet `0089A090` (FuncInfo of `0021E090`, field `01D670A4`) | 4 |
| `005DDAE0` | funclet | funclet `0089D990` (FuncInfo of `0060B980`, field `01DA3738`) | 2 |
| `00681840` | funclet | funclet `008A0030` (FuncInfo of `00684D10`, field `01DB6808`) | 5 |

Addresses the sentences cite besides each row's own function and anchors: `00194B00`, `00194CD0`, `0019E010`, `001A2130`, `001A2F70`, `001AA840`, `001ADD30`, `001AE550`, `001BCE30`, `001BE730`, `001DE180`, `001DE200`, `001DE280`, `001E1670`, `001E7480`, `001F4DA0`, `001FC640`, `002002E0`, `00209360`, `0020A800`, `0021E090`, `0060B980`, `00684D10`, `008968BC`, `0089690C`, `00896D00`, `00896DB0`, `00896EB0`, `00896EF0`, `00897020`, `00897065`, `00897110`, `0089711C`, `0089727C`, `00897410`, `008974EC`, `00897BF8`, `00897CA0`, `0089840A`, `00898480`, `008984FC`, `0089850C`, `00898660`, `0089899C`, `008989AC`, `00898AAC`, `00898E31`, `008996A0`, `008999D0`, `00899A08`, `00899B00`, `00899B10`, `00899CE0`, `0089A090`, `0089D990`, `008A0030`, `008C25E8`, `008C2600`, `008C26D0`, `008C2700`, `008C27C8`, `008C3178`, `008F3428`, `008F3D48`, `008F4310`, `00900A20`, `00900A48`, `00905538`, `009062E8`, `00906340`, `00906380`, `00906BB0`, `01D55E6C`, `01D55F50`, `01D5657C`, `01D56674`, `01D56DA0`, `01D56E1C`, `01D57A90`, `01D57AB0`, `01D582F8`, `01D58300`, `01D588AC`, `01D594AC`, `01D599F8`, `01D5B804`, `01D5BB84`, `01D5E13C`, `01D5E27C`, `01D5EA5C`, `01D5EA64`, `01D5EDBC`, `01D60588`, `01D60590`, `01D60E9C`, `01D6102C`, `01D62664`, `01D62684`, `01D62FF0`, `01D63F4C`, `01D63F54`, `01D64904`, `01D670A4`, `01DA3738`, `01DB6808`. These are referencing functions, tables, cells, stored values, callees and import slots. Run the neighbour pre-check (`xlayer_full` edge tokens on these new cites) before publishing.

## Neighbour-gate corrections (FABLE)

The 2026-10-03 neighbour pre-check refused the first draft with 5 unaccounted neighbours (11 edges into Input, Platform, PlatformOnlineAchievements, Save_Load_Settings and StoryEvent). Every one came from a funclet's parent function cited by entry in the phrase "the FuncInfo that `<parent>`'s unwind record names". The parent neither calls the funclet nor the body; it only owns the FuncInfo. So the 9 affected rows now name the parent by role and cite its FuncInfo by address instead: "the FuncInfo `<FuncInfo>` that the funclet's parent function's .pdata unwind record names".

| row | parent (in `ref.parent`, still checked) | FuncInfo now cited |
|---|---|---|
| `00195360` | `00197A50` | `008F3428` |
| `0019A4F0` | `0019AA20` | `008F3D48` |
| `0019DD30` | `0019D740` | `008F4310` |
| `001DE300` | `001DE5D0` | `00900A20` |
| `001DE330` | `001DEE90` | `00900A48` |
| `00206CD0` | `00206AD0` | `00905538` |
| `0020C860` | `0020C730` | `009062E8` |
| `0020C880` | `0020C730` | `009062E8` |
| `00211A60` | `002116B0` | `00906BB0` |

`apply.py` now takes an optional `ref.funcinfo`. When it is present, the address must equal the FuncInfo that the parent's own .pdata unwind record names (the parent is still read from `ref.parent`). So each row's claim is checked as strictly as before, and the cited FuncInfo is checked at the bytes too. Control: a temporary record whose first row had the FuncInfo of `0019AA20` printed `FAILS 1`; that record was deleted. The other 24 rows still cite their parents by entry, and none of those adds an edge. The before and after text is in `rows.json` under `corrections`. The dry run is unchanged (FAILS 0).

## Verification (FABLE)

[`apply.py`](apply.py) is the sibling contract (`fable-noref-dyngeo-instance-family-1003/apply.py`) with the owner-token check replaced by a reference check. It refuses to write until all of these pass:

- the page is clean (`git status --short`), and there is at least one row;
- each function is a certified function-list entry that the page does not already cite;
- each sentence has no pipe and is under 1,200 characters;
- each anchor is an instruction boundary strictly inside its function and decodes to the recorded mnemonic;
- each row's reference holds or forms the body's address at the bytes (the kinds are listed in the script's docstring);
- the page cites, outside the new section, the table or function each row names as the reference.

With `--apply` it appends one section, `## No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)`, holding an italic note and the table `| function | size | what the body does | interior anchors |`; anchor cells read Interior anchor `X`. The append keeps the page's line endings and is idempotent: an identical block prints `ALREADY`. The script prints `FAILS n` last.

The dry run is [`apply_dryrun.out`](apply_dryrun.out): `VERIFY 33 functions, 126 anchors, 33 references, page 24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md (LF)`, `FAILS 0`.

Controls, run on 2026-10-03 with the same `apply.py` from a temporary record that was deleted afterwards:

- one defect per check: a registrar store target off by 8, a swapped registrar, a funclet slot moved one entry, a swapped funclet parent, a table index off by one, a swapped CatchableType, a changed store operand, a wrong mnemonic, a pipe and an uncited token. Each printed its own `VERIFY FAIL` and a non-zero `FAILS`.
- zero rows printed `FAILS 1`, and a dirty page (`the-game-is-a-phyre-application.md`) was refused with `page is dirty`.
- on a copy of this page (`--test-copy`, which skips only the git check), the first `--apply` printed `PATCHED` and the second `ALREADY`. The original bytes are a prefix of the result, and no lone LF appeared in a CRLF page.

## Limits (FABLE)

These are body statements, not meanings. A value read from `.data` is named by address and never stated as a constant. Where a body is reached from several places, the row names one checked reference and counts the rest. The section is appended at publish time, and the publish gates (neighbour pre-check, `verify_doc_addresses`) run on the result. Nothing here is committed. The page and the register are untouched.

## Consumer check (FABLE)

affected: Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md

- consumer: this page's new section `No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)`: revised-here (33 rows added; no existing text changed).
- consumer: section `3. Key addresses` (cites `00896280`): agrees. The new rows for `00195360`, `001953A0`, `001953F0`, `0019A4F0`, `0019DD30`, `0019DD90`, `001A2830`, `001A28D0`, `001A2D50`, `001A2E10`, `001AADE0`, `001AAEE0`, `001AE130`, `001BCD90`, `001BE990`, `001DE300`, `001DE330`, `001DE360`, `001E1B20`, `001E1C60`, `001E76B0`, `001F5080`, `001F50E0`, `001FC2E0`, `00204540`, `00204590`, `00206CD0`, `0020C860`, `0020C880`, `00211A60`, `0021EBC0`, `005DDAE0`, `00681840` name `00896280` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: section `3. Key addresses` (cites `008A6960`): agrees. The new rows for `00195360`, `001953A0`, `001953F0`, `0019A4F0`, `0019DD30`, `0019DD90`, `001A2830`, `001A28D0`, `001A2D50`, `001A2E10`, `001AADE0`, `001AAEE0`, `001AE130`, `001BCD90`, `001BE990`, `001DE300`, `001DE330`, `001DE360`, `001E1B20`, `001E1C60`, `001E76B0`, `001F5080`, `001F50E0`, `001FC2E0`, `00204540`, `00204590`, `00206CD0`, `0020C860`, `0020C880`, `00211A60`, `0021EBC0`, `005DDAE0`, `00681840` name `008A6960` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: the funclet ABI paragraphs (`### What a funclet is, in this binary`, `### The funclet ABI`): agrees. Each named cleanup funclet passes a parent-frame-relative pointer (from `rdx`) and tail-jumps, and the catch funclet `008996A0` calls its body after saving `rdx`.
- consumer: the `### The .pdata / FuncInfo record layout` instrument: agrees. Each row's parent FuncInfo is read through the parent's own unwind record and carries magic `0x19930522`.

run: apply.py at 3f236eea3 (dry run FAILS 0)
