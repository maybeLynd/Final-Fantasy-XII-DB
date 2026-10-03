# No-reference bodies homed on dyngeo-instance-family.md by owning class (FABLE, 2026-10-03)

SWE2-EC7 handed FABLE the no-reference remainder on 2026-10-03 (`Database/Tools/work/SWE2-EC7/handoff_noref_to_fable_1003.tsv`). No document cites these functions and nothing calls them directly. The entry route is a vtable slot. I took only the bodies that `rtti-methods.tsv` lists (column 6 = `rtti`), read each listing whole from the certified image, and wrote one sentence per body. Owning class and slot come from `homing_rtti_noref_1003.tsv` (and `h211/callers.tsv` for the `PCaller` templates).

## Host choice (FABLE)

The owning class is `PrimitiveRendererD3D11`, 12 of its slots. The page with a section on the class, `gi-render-command-family.md` (§10, §13b), is dirty in the working tree (` M`, empty content diff). This page is the next-best host. Its contract-match table lists `PrimitiveRendererD3D11` slots 0/1, 4, 6, 8, 15 and 35, and it already homes `006CA760`, `006CAC30`, `006CAF40` and `006CAEB0` from the same vtable.

## What the bytes say (FABLE)

**What the rows say.** `006CA650` (slot 2) is the `+0xC0` twin of the homed `006CA760` (`+0xB8`). It is built from `+0x18864` and a dword index shifted by 15 instead of `+0x10880` and a stride of `0x7FE0`. Slots 41/43 (`006CA6F0`/`006CA680`) and 42 (`006CB590`) call slots 14 and 15 of the object at `[[this+0x848]+0x110]`, indexed by dwords `+0xA0`/`+0xB0` into the qword arrays at `+0x90`/`+0xA8`. Slot 14 (`006CAB50`) calls the renderer's own slot 15 with `r8d` and `r9d` repeated as stack arguments 5 and 6. That reproduces the `(1, 6, 7, 6, 7, x)` argument pattern this page reads at slot 15. The rest are field stores, and two of them (`006CAD50`, `006CAE70`) set no return value. In `006CADB0` both bytes it reads are in `.data`, so the row states no value for them.

## Rows (FABLE)

12 rows, 42 interior anchors, page `16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md`.

| function | owner token checked on the page | anchors |
|---|---|---|
| `006CA650` | `PrimitiveRendererD3D11` | 4 |
| `006CA680` | `PrimitiveRendererD3D11` | 5 |
| `006CA6F0` | `PrimitiveRendererD3D11` | 5 |
| `006CAB50` | `PrimitiveRendererD3D11` | 4 |
| `006CAC10` | `PrimitiveRendererD3D11` | 1 |
| `006CAD30` | `PrimitiveRendererD3D11` | 2 |
| `006CAD50` | `PrimitiveRendererD3D11` | 5 |
| `006CAD90` | `PrimitiveRendererD3D11` | 2 |
| `006CADB0` | `PrimitiveRendererD3D11` | 4 |
| `006CAE70` | `PrimitiveRendererD3D11` | 2 |
| `006CAE90` | `PrimitiveRendererD3D11` | 3 |
| `006CB590` | `PrimitiveRendererD3D11` | 5 |

Addresses the sentences cite besides the row's own function and anchors: `01F2EEB8`, `02E5BDDC`. These are callees, compared or stored addresses, and `.data` bytes. Run the neighbour pre-check (`xlayer_full` edge tokens on these new cites) before publishing.

## Verification (FABLE)

[`apply.py`](apply.py) refuses to write until all of these pass:

- the page is clean (`git status --short`), and there is at least one row;
- each function is a certified function-list entry that the page does not already cite;
- each sentence has no pipe and is under 1,200 characters;
- each anchor is an instruction boundary strictly inside its function and decodes to the recorded mnemonic;
- the page cites each row's owner token.

With `--apply` it appends one section, `## No-reference bodies homed by owning class (FABLE, 2026-10-03)`. That section holds an italic note and the table `| function | size | what the body does | interior anchors |`. The append keeps the page's line endings and is idempotent: an identical block prints `ALREADY`. The script prints `FAILS n` last.

The dry run is [`apply_dryrun.out`](apply_dryrun.out): `VERIFY 12 functions, 42 anchors, page 16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md (LF)`, `FAILS 0`.

Controls, run on 2026-10-03 against copies (`--test-copy`, which skips only the git check):

- on a copy of the page: the first `--apply` prints `PATCHED` and the second prints `ALREADY`. The original bytes are a prefix of the result, and the line-ending counts are unchanged in kind.
- on a temporary record seeded with a wrong mnemonic, an entry-address anchor, a pipe and an unknown owner token: it printed four kinds of VERIFY FAIL and `FAILS 6`.
- with zero rows: it printed `FAILS 1`.
- pointed at the dirty Gi page: it refused with `page is dirty` and `FAILS 1`.

The temporary record was deleted afterwards.

## Limits (FABLE)

These are body statements, not meanings. A value read from `.data` is stated by address and never as a constant. The section is appended at publish time, and the publish gates (neighbour pre-check, `verify_doc_addresses`) run on the result. Nothing here is committed. The page and the register are untouched.

## Consumer check (FABLE)

affected: Database/FFXII TZA/16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md

- consumer: this page's new section `No-reference bodies homed by owning class (FABLE, 2026-10-03)`: revised-here (12 rows added; no existing text changed).
- consumer: the contract-match slot table (slots 0/1, 4, 6, 8, 15, 35): agrees. No row changes, and the new slots are 2, 7, 9, 10, 11, 12, 14, 32, 36, 41, 42 and 43.
- consumer: the slot-15 reading `006CAB80(1, 6, 7, 6, 7, x)`: agrees. Slot 14 forwards `(a, b, c, e)` as `(a, b, c, b, c, e)`, which is the same argument shape.
- consumer: the homed `006CA760` row (`+0xB8` staging pointer): agrees. `006CA650` is stated separately for `+0xC0`.

run: apply.py at d02293770 (dry run verified 12 functions, 42 anchors, page 16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md (LF); FAILS 0)
