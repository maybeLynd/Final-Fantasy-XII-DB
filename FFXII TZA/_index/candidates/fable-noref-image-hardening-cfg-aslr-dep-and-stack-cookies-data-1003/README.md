# No-reference bodies homed on image-hardening-cfg-aslr-dep-and-stack-cookies.md by the table or code that reaches them (FABLE, 2026-10-03)

SWE2-EC7 handed FABLE the no-reference remainder on 2026-10-03 (`Database/Tools/work/SWE2-EC7/handoff_noref_to_fable_1003.tsv`). No document cites these functions as a row, and no census-listed instruction calls or jumps to them. I took the rows without the `rtti` column (176 bodies) and swept the certified image for every reference to each entry: absolute qwords and 32-bit image-relative values outside `.text` and `.pdata`, rip-relative operands in `.text` (a raw rel32 sweep, decoded at the instruction start), `[reg+RVA]` forms, and the `FuncInfo` unwind and catch maps that name the exception funclets. I grouped the bodies by the table or function holding the reference and read every listing whole. This record holds the 66 bodies whose referencing table or function this page documents. The full census, with every unhosted body and its reason, is `C:\t\noref_census.tsv`.

## Host choice (FABLE)

The 66 bodies are the code pointers of the scalar-conversion tree. Each is loaded by `lea` at +0x8D of a 383-byte registrar in `005850F0`-`00592770` and stored at qword `+0x28` of that registrar's tree node, the node the registrar inserts under the sentinel `01F2CDA0`. This page declares the registrars as EC-7 family C, explains the tree in its 145-teardowns section and the S-3 answer, and links `members/guard-adapter-registrars.tsv`, whose `stored_code_pointer` column lists every one of them. It says outright that the routines themselves were not dispositioned. The 66 are the 68 distinct stored code pointers less `00594350` and `00594EB0`, which EC7-45/47 already homed here. The handoff note put the block at 77; the census counts 66 bodies in `005928F0`-`00595D70`.

## What the bytes say (FABLE)

Every routine has one prologue: n = dword `[r8]`, the source `rcx` and destination `rdx` each get one of two offsets (dword `+8` of qword `[r9+8]` and dword `+0x48` of qword `[r9+0x10]`, chosen by byte `[r8+0xC]`), and the strides are dwords `[r8+4]` and `[r8+8]`. The routines differ only in the element step: sign or zero extension, plain copies, `cvtdq2ps`/`cvtdq2pd` and `cvtsi2ss`/`cvtsi2sd` conversions, truncating `cvttss2si`/`cvttsd2si` with a byte, word or dword store of the low part, the unsigned 64-bit sequences that subtract and re-add 2^63 (`00D27A70`, `00D27A60`) or add 2^64 (`008C5B60`, `00D27A68`), non-zero tests that write 0 or 1, and 16-byte stores built on the stack with a zero high qword. The float and double sources and destinations use a loop unrolled four times plus a remainder loop. The constants are `.rdata`, so their values are stated.

## Rows (FABLE)

66 rows, 218 interior anchors, page `24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`. Each row's reference is checked at the bytes by `apply.py`.

| function | reference kind | reached from | anchors |
|---|---|---|---|
| `005928F0` | registrar | `005853F0` + 0x8D | 3 |
| `00592960` | registrar | `005856F0` + 0x8D | 3 |
| `005929D0` | registrar | `005859F0` + 0x8D | 4 |
| `00592AD0` | registrar | `00585B70` + 0x8D | 4 |
| `00592BD0` | registrar | `00585CF0` + 0x8D | 3 |
| `00592C60` | registrar | `00585E70` + 0x8D | 3 |
| `00592CD0` | registrar | `005865F0` + 0x8D | 3 |
| `00592D40` | registrar | `005868F0` + 0x8D | 3 |
| `00592DB0` | registrar | `00586EF0` + 0x8D | 3 |
| `00592E30` | registrar | `00587070` + 0x8D | 3 |
| `00592EA0` | registrar | `00586170` + 0x8D | 3 |
| `00592F10` | registrar | `00587AF0` + 0x8D | 3 |
| `00592F80` | registrar | `00587DF0` + 0x8D | 4 |
| `00593080` | registrar | `00587F70` + 0x8D | 4 |
| `00593180` | registrar | `005880F0` + 0x8D | 3 |
| `00593210` | registrar | `00588270` + 0x8D | 3 |
| `00593280` | registrar | `00588CF0` + 0x8D | 3 |
| `005932F0` | registrar | `00588FF0` + 0x8D | 4 |
| `005933F0` | registrar | `00589170` + 0x8D | 4 |
| `005934F0` | registrar | `005892F0` + 0x8D | 3 |
| `00593570` | registrar | `00589470` + 0x8D | 3 |
| `005935E0` | registrar | `00588570` + 0x8D | 3 |
| `00593650` | registrar | `0058A1F0` + 0x8D | 4 |
| `00593730` | registrar | `0058A370` + 0x8D | 4 |
| `00593820` | registrar | `0058A4F0` + 0x8D | 3 |
| `005938A0` | registrar | `0058A670` + 0x8D | 3 |
| `00593910` | registrar | `0058A970` + 0x8D | 3 |
| `00593980` | registrar | `005877F0` + 0x8D | 3 |
| `005939F0` | registrar | `00589EF0` + 0x8D | 3 |
| `00593A60` | registrar | `0058B3F0` + 0x8D | 4 |
| `00593B60` | registrar | `0058B570` + 0x8D | 4 |
| `00593C60` | registrar | `0058B6F0` + 0x8D | 3 |
| `00593CE0` | registrar | `0058B870` + 0x8D | 3 |
| `00593D50` | registrar | `0058BCF0` + 0x8D | 3 |
| `00593E30` | registrar | `0058BE70` + 0x8D | 3 |
| `00593F10` | registrar | `0058BFF0` + 0x8D | 3 |
| `00593FF0` | registrar | `0058C170` + 0x8D | 3 |
| `005940D0` | registrar | `0058C2F0` + 0x8D | 3 |
| `005941B0` | registrar | `0058C470` + 0x8D | 3 |
| `00594290` | registrar | `0058C5F0` + 0x8D | 3 |
| `00594430` | registrar | `0058C8F0` + 0x8D | 4 |
| `00594600` | registrar | `0058CA70` + 0x8D | 3 |
| `005946E0` | registrar | `0058CBF0` + 0x8D | 4 |
| `00594860` | registrar | `0058CD70` + 0x8D | 4 |
| `00594970` | registrar | `0058CEF0` + 0x8D | 3 |
| `00594A50` | registrar | `0058D070` + 0x8D | 3 |
| `00594B30` | registrar | `0058D1F0` + 0x8D | 3 |
| `00594C10` | registrar | `0058D370` + 0x8D | 3 |
| `00594CF0` | registrar | `0058D4F0` + 0x8D | 3 |
| `00594DD0` | registrar | `0058D670` + 0x8D | 3 |
| `00594FA0` | registrar | `0058D970` + 0x8D | 3 |
| `00595080` | registrar | `0058DAF0` + 0x8D | 4 |
| `00595260` | registrar | `0058DC70` + 0x8D | 3 |
| `00595340` | registrar | `0058DDF0` + 0x8D | 4 |
| `005954D0` | registrar | `0058DF70` + 0x8D | 4 |
| `005955F0` | registrar | `0058E9F0` + 0x8D | 3 |
| `005956E0` | registrar | `0058EB70` + 0x8D | 3 |
| `005957D0` | registrar | `0058ECF0` + 0x8D | 3 |
| `00595840` | registrar | `0058FEF0` + 0x8D | 3 |
| `005958C0` | registrar | `0058F170` + 0x8D | 3 |
| `00595930` | registrar | `00590DF0` + 0x8D | 4 |
| `00595A60` | registrar | `00590F70` + 0x8D | 4 |
| `00595B90` | registrar | `0058EE70` + 0x8D | 3 |
| `00595C00` | registrar | `005850F0` + 0x8D | 3 |
| `00595C70` | registrar | `00586BF0` + 0x8D | 4 |
| `00595D70` | registrar | `00586D70` + 0x8D | 4 |

Addresses the sentences cite besides each row's own function and anchors: `005850F0`, `005853F0`, `00585570`, `005856F0`, `00585870`, `005859F0`, `00585B70`, `00585CF0`, `00585E70`, `00585FF0`, `00586170`, `005865F0`, `00586770`, `005868F0`, `00586A70`, `00586BF0`, `00586D70`, `00586EF0`, `00587070`, `005871F0`, `00587370`, `005877F0`, `00587AF0`, `00587C70`, `00587DF0`, `00587F70`, `005880F0`, `00588270`, `005883F0`, `00588570`, `00588CF0`, `00588E70`, `00588FF0`, `00589170`, `005892F0`, `00589470`, `005895F0`, `00589770`, `00589EF0`, `0058A1F0`, `0058A370`, `0058A4F0`, `0058A670`, `0058A7F0`, `0058A970`, `0058B3F0`, `0058B570`, `0058B6F0`, `0058B870`, `0058B9F0`, `0058BB70`, `0058BCF0`, `0058BE70`, `0058BFF0`, `0058C170`, `0058C2F0`, `0058C470`, `0058C5F0`, `0058C8F0`, `0058CA70`, `0058CBF0`, `0058CD70`, `0058CEF0`, `0058D070`, `0058D1F0`, `0058D370`, `0058D4F0`, `0058D670`, `0058D970`, `0058DAF0`, `0058DC70`, `0058DDF0`, `0058DF70`, `0058E9F0`, `0058EB70`, `0058ECF0`, `0058EE70`, `0058F170`, `0058FBF0`, `0058FD70`, `0058FEF0`, `00590370`, `00590DF0`, `00590F70`, `005910F0`, `00591570`, `005919F0`, `00591B70`, `00591CF0`, `00591E70`, `00591FF0`, `00592170`, `005922F0`, `00592470`, `005925F0`, `00592770`, `008C5B60`, `00D27A60`, `00D27A68`, `00D27A70`, `01F2CDA0`. These are referencing functions, tables, cells, stored values, callees and import slots. Run the neighbour pre-check (`xlayer_full` edge tokens on these new cites) before publishing.

## Verification (FABLE)

[`apply.py`](apply.py) is the sibling contract (`fable-noref-dyngeo-instance-family-1003/apply.py`) with the owner-token check replaced by a reference check. It refuses to write until all of these pass:

- the page is clean (`git status --short`), and there is at least one row;
- each function is a certified function-list entry that the page does not already cite;
- each sentence has no pipe and is under 1,200 characters;
- each anchor is an instruction boundary strictly inside its function and decodes to the recorded mnemonic;
- each row's reference holds or forms the body's address at the bytes (the kinds are listed in the script's docstring);
- the page cites, outside the new section, the table or function each row names as the reference.

With `--apply` it appends one section, `## No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)`, holding an italic note and the table `| function | size | what the body does | interior anchors |`; anchor cells read Interior anchor `X`. The append keeps the page's line endings and is idempotent: an identical block prints `ALREADY`. The script prints `FAILS n` last.

The dry run is [`apply_dryrun.out`](apply_dryrun.out): `VERIFY 66 functions, 218 anchors, 66 references, page 24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md (LF)`, `FAILS 0`.

Controls, run on 2026-10-03 with the same `apply.py` from a temporary record that was deleted afterwards:

- one defect per check: a registrar store target off by 8, a swapped registrar, a funclet slot moved one entry, a swapped funclet parent, a table index off by one, a swapped CatchableType, a changed store operand, a wrong mnemonic, a pipe and an uncited token. Each printed its own `VERIFY FAIL` and a non-zero `FAILS`.
- zero rows printed `FAILS 1`, and a dirty page (`the-game-is-a-phyre-application.md`) was refused with `page is dirty`.
- on a copy of this page (`--test-copy`, which skips only the git check), the first `--apply` printed `PATCHED` and the second `ALREADY`. The original bytes are a prefix of the result, and no lone LF appeared in a CRLF page.

## Limits (FABLE)

These are body statements, not meanings. A value read from `.data` is named by address and never stated as a constant. Where a body is reached from several places, the row names one checked reference and counts the rest. The section is appended at publish time, and the publish gates (neighbour pre-check, `verify_doc_addresses`) run on the result. Nothing here is committed. The page and the register are untouched.

## Consumer check (FABLE)

affected: Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md

- consumer: this page's new section `No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)`: revised-here (66 rows added; no existing text changed).
- consumer: section `(page head)` (cites `005850F0`): agrees. The new rows for `005928F0`, `00592960`, `005929D0`, `00592AD0`, `00592BD0`, `00592C60`, `00592CD0`, `00592D40`, `00592DB0`, `00592E30`, `00592EA0`, `00592F10`, `00592F80`, `00593080`, `00593180`, `00593210`, `00593280`, `005932F0`, `005933F0`, `005934F0`, `00593570`, `005935E0`, `00593650`, `00593730`, `00593820`, `005938A0`, `00593910`, `00593980`, `005939F0`, `00593A60`, `00593B60`, `00593C60`, `00593CE0`, `00593D50`, `00593E30`, `00593F10`, `00593FF0`, `005940D0`, `005941B0`, `00594290`, `00594430`, `00594600`, `005946E0`, `00594860`, `00594970`, `00594A50`, `00594B30`, `00594C10`, `00594CF0`, `00594DD0`, `00594FA0`, `00595080`, `00595260`, `00595340`, `005954D0`, `005955F0`, `005956E0`, `005957D0`, `00595840`, `005958C0`, `00595930`, `00595A60`, `00595B90`, `00595C00`, `00595C70`, `00595D70` name `005850F0` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: section `(page head)` (cites `01F2CDA0`): agrees. The new rows for `005928F0`, `00592960`, `005929D0`, `00592AD0`, `00592BD0`, `00592C60`, `00592CD0`, `00592D40`, `00592DB0`, `00592E30`, `00592EA0`, `00592F10`, `00592F80`, `00593080`, `00593180`, `00593210`, `00593280`, `005932F0`, `005933F0`, `005934F0`, `00593570`, `005935E0`, `00593650`, `00593730`, `00593820`, `005938A0`, `00593910`, `00593980`, `005939F0`, `00593A60`, `00593B60`, `00593C60`, `00593CE0`, `00593D50`, `00593E30`, `00593F10`, `00593FF0`, `005940D0`, `005941B0`, `00594290`, `00594430`, `00594600`, `005946E0`, `00594860`, `00594970`, `00594A50`, `00594B30`, `00594C10`, `00594CF0`, `00594DD0`, `00594FA0`, `00595080`, `00595260`, `00595340`, `005954D0`, `005955F0`, `005956E0`, `005957D0`, `00595840`, `005958C0`, `00595930`, `00595A60`, `00595B90`, `00595C00`, `00595C70`, `00595D70` name `01F2CDA0` only as the place that holds or forms the body's address, which the dry run checks at the bytes; nothing in the section changes.
- consumer: the family C frontmatter line ("NOT dispositioned: the 68 conversion routines themselves"): agrees. The rows explain 66 bodies and leave family membership unchanged; the other two were homed by EC7-45/47.
- consumer: the S-3 answer ("there are 68 routines"): agrees. `members/guard-adapter-registrars.tsv` holds 68 distinct stored code pointers: these 66, `00594350` and `00594EB0`.
- consumer: the direction bullet (`+0x18` source, `+0x20` destination, from `00594EB0`/`00594350`): agrees. For example, `005928F0` reads a byte and writes a word, and the members file pairs it with `PInt16` (the descriptor fetched first, stored at `+0x20`) and `PChar`.

run: apply.py at 3f236eea3 (dry run FAILS 0)
