# No-reference bodies homed on class-descriptor-and-metadata-system.md by owning class (FABLE, 2026-10-03)

SWE2-EC7 handed FABLE the no-reference remainder on 2026-10-03 (`Database/Tools/work/SWE2-EC7/handoff_noref_to_fable_1003.tsv`). No document cites these functions and nothing calls them directly. The entry route is a vtable slot. I took only the bodies that `rtti-methods.tsv` lists (column 6 = `rtti`), read each listing whole from the certified image, and wrote one sentence per body. Owning class and slot come from `homing_rtti_noref_1003.tsv` (and `h211/callers.tsv` for the `PCaller` templates).

## Host choice (FABLE)

The owning classes are the reflection descriptor templates (`PClassDescriptorAbstract`, `...Concrete`, `...ForType`, `...Header`, `...WithoutDefaultConstructor`, `PClassDescriptorWrapper`) and `PNamedSemanticDescriptorForType` / `...ForDynamicType`. The rows are their slots 4, 8, 10, 11, 14 and 15. This page documents those descriptor classes, and its per-member sections are organised by descriptor vtable slot.

## What the bytes say (FABLE)

**What the rows say, by slot.** Slot 10 bodies (8) store into a caller-supplied object when `rdx` is non-NULL (mostly zeros; `0xFF`, 10, 1 and self-links appear in three of them) and return 1. Slot 11 bodies (9) call one to three helpers on the object in `rdx`, store the `PAnimationHierarchyNode` vtable address (`00D312F0`, from `members/rtti-class-vtables.tsv`), or unlink a two-way list node, and return 1. Slot 8 bodies (2) return a qword of `[rdx]` or `[rdx+8]` (0 for NULL). Slot 14 (`006AA7F0`) walks a strided array and returns 0. Slot 15 (`005A3EA0`) tail-jumps through a function-pointer FIELD at `+0x100` of the descriptor, not through its vtable. Slot 4 (`006B2E40`) tail-jumps to `006843D0` with the arguments moved down one register. None of the 22 is in a declared member list on this page (`members/*.tsv`, checked against all of them except the generated `phyre-class-descriptor-vtable.tsv` slot map).

## Rows (FABLE)

22 rows, 87 interior anchors, page `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`.

| function | owner token checked on the page | anchors |
|---|---|---|
| `005A1110` | `PClassDescriptorAbstract` | 5 |
| `005A1580` | `PClassDescriptorAbstract` | 3 |
| `005A2280` | `PClassDescriptorAbstract` | 3 |
| `005A3EA0` | `PClassDescriptorHeader` | 4 |
| `005A44E0` | `PClassDescriptorConcrete` | 3 |
| `005D2C60` | `PClassDescriptorWithoutDefaultConstructor` | 4 |
| `006110B0` | `PClassDescriptorWithoutDefaultConstructor` | 5 |
| `00613530` | `PClassDescriptorWithoutDefaultConstructor` | 5 |
| `0062F880` | `PClassDescriptorWithoutDefaultConstructor` | 5 |
| `00688000` | `PClassDescriptorAbstract` | 4 |
| `006A9450` | `PClassDescriptorAbstract` | 3 |
| `006AA6C0` | `PClassDescriptorAbstract` | 4 |
| `006AA7F0` | `PClassDescriptorAbstract` | 5 |
| `006B2E40` | `PClassDescriptorWrapper` | 2 |
| `006CD6A0` | `PNamedSemanticDescriptorForType` | 3 |
| `006CE820` | `PClassDescriptorConcrete` | 4 |
| `006D98C0` | `PNamedSemanticDescriptorForType` | 3 |
| `006D9E80` | `PClassDescriptorHeader` | 4 |
| `008773B0` | `PClassDescriptorAbstract` | 4 |
| `008775E0` | `PClassDescriptorAbstract` | 5 |
| `008779E0` | `PClassDescriptorWithoutDefaultConstructor` | 5 |
| `00879980` | `PClassDescriptorConcrete` | 4 |

Addresses the sentences cite besides the row's own function and anchors: `005A9D80`, `005A9E70`, `00616B40`, `00619070`, `0062BAB0`, `006843D0`, `00691DF0`, `006A4710`, `006A49A0`, `006AAA50`, `006ACA70`, `00878070`, `00D312F0`. These are callees, compared or stored addresses, and `.data` bytes. Run the neighbour pre-check (`xlayer_full` edge tokens on these new cites) before publishing.

## Verification (FABLE)

[`apply.py`](apply.py) refuses to write until all of these pass:

- the page is clean (`git status --short`), and there is at least one row;
- each function is a certified function-list entry that the page does not already cite;
- each sentence has no pipe and is under 1,200 characters;
- each anchor is an instruction boundary strictly inside its function and decodes to the recorded mnemonic;
- the page cites each row's owner token.

With `--apply` it appends one section, `## No-reference bodies homed by owning class (FABLE, 2026-10-03)`. That section holds an italic note and the table `| function | size | what the body does | interior anchors |`. The append keeps the page's line endings and is idempotent: an identical block prints `ALREADY`. The script prints `FAILS n` last.

The dry run is [`apply_dryrun.out`](apply_dryrun.out): `VERIFY 22 functions, 87 anchors, page 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md (CRLF)`, `FAILS 0`.

Controls, run on 2026-10-03 against copies (`--test-copy`, which skips only the git check):

- on a copy of the page: the first `--apply` prints `PATCHED` and the second prints `ALREADY`. The original bytes are a prefix of the result, and the line-ending counts are unchanged in kind.
- on a temporary record seeded with a wrong mnemonic, an entry-address anchor, a pipe and an unknown owner token: it printed four kinds of VERIFY FAIL and `FAILS 6`.
- with zero rows: it printed `FAILS 1`.
- pointed at the dirty Gi page: it refused with `page is dirty` and `FAILS 1`.

The temporary record was deleted afterwards.

## Limits (FABLE)

These are body statements, not meanings. A value read from `.data` is stated by address and never as a constant. The section is appended at publish time, and the publish gates (neighbour pre-check, `verify_doc_addresses`) run on the result. Nothing here is committed. The page and the register are untouched.

## Consumer check (FABLE)

affected: Database/FFXII TZA/22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md

- consumer: this page's new section `No-reference bodies homed by owning class (FABLE, 2026-10-03)`: revised-here (22 rows added; no existing text changed).
- consumer: DK-2's answer that slot 10 of `WithoutDefaultConstructor<T>` constructs in place: agrees. The slot-10 rows here state stores into a caller-supplied object, and the rows name no purpose.
- consumer: the R2 family `PClassDescriptorConcrete<T> placement default constructors, slot 10` (`members/pclassdescriptorconcrete-placement-default-ctors.tsv`): agrees. None of the eight slot-10 bodies here is a member, and the family list is unchanged.
- consumer: `members/phyre-class-descriptor-vtable.tsv` (the generated slot map that lists `005A1580`, `005A2280`, `005A44E0`, `006AA6C0` and others in its per-class slot columns): agrees. This record does not edit it.

run: apply.py at d02293770 (dry run verified 22 functions, 87 anchors, page 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md (CRLF); FAILS 0)
