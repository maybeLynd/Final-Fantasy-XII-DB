# No-reference bodies homed on the-ordered-render-command-list.md by owning class (FABLE, 2026-10-03)

SWE2-EC7 handed FABLE the no-reference remainder on 2026-10-03 (`Database/Tools/work/SWE2-EC7/handoff_noref_to_fable_1003.tsv`). No document cites these functions and nothing calls them directly. The entry route is a vtable slot. I took only the bodies that `rtti-methods.tsv` lists (column 6 = `rtti`), read each listing whole from the certified image, and wrote one sentence per body. Owning class and slot come from `homing_rtti_noref_1003.tsv` (and `h211/callers.tsv` for the `PCaller` templates).

## Host choice (FABLE)

The owning classes are `GiSetRtForRtSampling`, `GiBeginScene` and `GiEndScene` (slot 1). The page with sections on the `Gi*` family, `17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md`, is dirty in the working tree (`git status --short` prints ` M`, with an empty content diff: a line-ending state left by a peer). By rule it is not used. This page is the next-best host: its UQ-231 answer names all three classes with their vtables (`00902F28`, `00904488`, `009044A0`) as `GeometryInstance`-derived two-slot classes.

## What the bytes say (FABLE)

**What the rows say.** All three are slot-1 forwarders into the object passed in `rdx`. `GiBeginScene` and `GiEndScene` tail-jump to that object's slots 38 and 37. `GiSetRtForRtSampling` tail-jumps to its slot 7 with the command's qwords `+8` and `+0x10` as arguments. The rows do not name the class of the `rdx` object.

## Rows (FABLE)

3 rows, 8 interior anchors, page `17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md`.

| function | owner token checked on the page | anchors |
|---|---|---|
| `001F16A0` | `GiSetRtForRtSampling` | 4 |
| `001FBD70` | `GiBeginScene` | 2 |
| `001FBE40` | `GiEndScene` | 2 |

## Verification (FABLE)

[`apply.py`](apply.py) refuses to write until all of these pass:

- the page is clean (`git status --short`), and there is at least one row;
- each function is a certified function-list entry that the page does not already cite;
- each sentence has no pipe and is under 1,200 characters;
- each anchor is an instruction boundary strictly inside its function and decodes to the recorded mnemonic;
- the page cites each row's owner token.

With `--apply` it appends one section, `## No-reference bodies homed by owning class (FABLE, 2026-10-03)`. That section holds an italic note and the table `| function | size | what the body does | interior anchors |`. The append keeps the page's line endings and is idempotent: an identical block prints `ALREADY`. The script prints `FAILS n` last.

The dry run is [`apply_dryrun.out`](apply_dryrun.out): `VERIFY 3 functions, 8 anchors, page 17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md (LF)`, `FAILS 0`.

Controls, run on 2026-10-03 against copies (`--test-copy`, which skips only the git check):

- on a copy of the page: the first `--apply` prints `PATCHED` and the second prints `ALREADY`. The original bytes are a prefix of the result, and the line-ending counts are unchanged in kind.
- on a temporary record seeded with a wrong mnemonic, an entry-address anchor, a pipe and an unknown owner token: it printed four kinds of VERIFY FAIL and `FAILS 6`.
- with zero rows: it printed `FAILS 1`.
- pointed at the dirty Gi page: it refused with `page is dirty` and `FAILS 1`.

The temporary record was deleted afterwards.

## Limits (FABLE)

These are body statements, not meanings. A value read from `.data` is stated by address and never as a constant. The section is appended at publish time, and the publish gates (neighbour pre-check, `verify_doc_addresses`) run on the result. Nothing here is committed. The page and the register are untouched.

## Consumer check (FABLE)

affected: Database/FFXII TZA/17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md

- consumer: this page's new section `No-reference bodies homed by owning class (FABLE, 2026-10-03)`: revised-here (3 rows added; no existing text changed).
- consumer: the UQ-231 answer (sixteen `GeometryInstance`-derived `Gi*` classes with two slots each): agrees. These are slot 1 of three of them.
- consumer: the Gi family page's `members/geometry-instance-vtable-slots.tsv` rows for the three bodies (slot 1; 13, 13 and 21 B): agrees. Sizes and slots match, and that page is not touched.

run: apply.py at d02293770 (dry run verified 3 functions, 8 anchors, page 17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md (LF); FAILS 0)
