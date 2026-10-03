# No-reference bodies homed on phyre-subsystem-map.md by owning class (FABLE, 2026-10-03)

SWE2-EC7 handed FABLE the no-reference remainder on 2026-10-03 (`Database/Tools/work/SWE2-EC7/handoff_noref_to_fable_1003.tsv`). No document cites these functions and nothing calls them directly. The entry route is a vtable slot. I took only the bodies that `rtti-methods.tsv` lists (column 6 = `rtti`), read each listing whole from the certified image, and wrote one sentence per body. Owning class and slot come from `homing_rtti_noref_1003.tsv` (and `h211/callers.tsv` for the `PCaller` templates).

## Host choice (FABLE)

`005A0240` is slot 2 of `PIChildClassVisitor` and of two classes derived from it (`PDeleteChildrenVisitor`, `PFindNestedClassVisitor`). This is the only content page that names `PIChildClassVisitor`, in its reflection and type-system row. The class-descriptor page does not name the visitor, so that page fails the owner-name test.

## What the bytes say (FABLE)

**What the body is.** It is a 7-byte forwarder from slot 2 to slot 1 of the same vtable, with every argument register unchanged. Its one anchor is the `jmp`, the only instruction strictly inside the body.

## Rows (FABLE)

1 rows, 1 interior anchors, page `22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md`.

| function | owner token checked on the page | anchors |
|---|---|---|
| `005A0240` | `PIChildClassVisitor` | 1 |

## Verification (FABLE)

[`apply.py`](apply.py) refuses to write until all of these pass:

- the page is clean (`git status --short`), and there is at least one row;
- each function is a certified function-list entry that the page does not already cite;
- each sentence has no pipe and is under 1,200 characters;
- each anchor is an instruction boundary strictly inside its function and decodes to the recorded mnemonic;
- the page cites each row's owner token.

With `--apply` it appends one section, `## No-reference bodies homed by owning class (FABLE, 2026-10-03)`. That section holds an italic note and the table `| function | size | what the body does | interior anchors |`. The append keeps the page's line endings and is idempotent: an identical block prints `ALREADY`. The script prints `FAILS n` last.

The dry run is [`apply_dryrun.out`](apply_dryrun.out): `VERIFY 1 functions, 1 anchors, page 22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md (LF)`, `FAILS 0`.

Controls, run on 2026-10-03 against copies (`--test-copy`, which skips only the git check):

- on a copy of the page: the first `--apply` prints `PATCHED` and the second prints `ALREADY`. The original bytes are a prefix of the result, and the line-ending counts are unchanged in kind.
- on a temporary record seeded with a wrong mnemonic, an entry-address anchor, a pipe and an unknown owner token: it printed four kinds of VERIFY FAIL and `FAILS 6`.
- with zero rows: it printed `FAILS 1`.
- pointed at the dirty Gi page: it refused with `page is dirty` and `FAILS 1`.

The temporary record was deleted afterwards.

## Limits (FABLE)

These are body statements, not meanings. A value read from `.data` is stated by address and never as a constant. The section is appended at publish time, and the publish gates (neighbour pre-check, `verify_doc_addresses`) run on the result. Nothing here is committed. The page and the register are untouched.

## Consumer check (FABLE)

affected: Database/FFXII TZA/22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md

- consumer: this page's new section `No-reference bodies homed by owning class (FABLE, 2026-10-03)`: revised-here (1 rows added; no existing text changed).
- consumer: the reflection and type-system row (`PIChildClassVisitor` among 22 classes): agrees. The row is unchanged, and the new section adds the one body.

run: apply.py at d02293770 (dry run verified 1 functions, 1 anchors, page 22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md (LF); FAILS 0)
