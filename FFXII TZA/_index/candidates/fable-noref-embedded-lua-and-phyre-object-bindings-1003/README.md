# No-reference bodies homed on embedded-lua-and-phyre-object-bindings.md by owning class (FABLE, 2026-10-03)

SWE2-EC7 handed FABLE the no-reference remainder on 2026-10-03 (`Database/Tools/work/SWE2-EC7/handoff_noref_to_fable_1003.tsv`). No document cites these functions and nothing calls them directly. The entry route is a vtable slot. I took only the bodies that `rtti-methods.tsv` lists (column 6 = `rtti`), read each listing whole from the certified image, and wrote one sentence per body. Owning class and slot come from `homing_rtti_noref_1003.tsv` (and `h211/callers.tsv` for the `PCaller` templates).

## Host choice (FABLE)

The owning classes are the concrete `PCaller` templates (`PMethodCallerConcrete<...>` and `PFunctionCallerConcrete<...>`, slot 2). This page's `PCaller` section names them as the C++ side of the binding interface, and SWE2-EC7 homed twelve siblings here in EC7-211 (`884bb7763`). I copied the shape of those rows, but the rows go into a new FABLE section rather than into EC7's paragraph run.

## What the bytes say (FABLE)

**What the bytes changed in the hand-off's shape note.** EC7's note (slot 2; bound pointer at `+8`; target in `rdx`; arguments from the fifth-argument cursor, 8 bytes each; doubles narrowed with `cvtpd2ps`; returns 0) holds for the three void thunks here (`00610D00`, `006C0640`, `006C0680`). It does not hold for the other 24, which return a value. Each of those runs a tag test after the call. When the fourth argument `r9` is non-NULL and the third argument `r8` equals a fixed address (6 rows), a fixed address with bit 0 set (`or rax, 1`; 15 rows), or the result of a descriptor getter (`006B33F0`, `006B1600`, `006AE780`; 3 rows, two of them with bit 0 set), the thunk stores qword 0 at `[r9]` and the result at `[r9+8]` and returns 1. Every other path returns 0. Two further departures are stated per row. The six `PFunctionCallerConcrete` thunks have no NULL test of `rdx`. The seven by-value returns (`PTypedObject`, `Vector3`) pass a 16-byte stack buffer as the hidden return slot (in `rdx`, or in `rcx` for the function caller `007A3200`) and copy 16 bytes to `[r9+8]`. The compared addresses are `.data` objects. The class-descriptor page's descriptor tables name eleven of them (`02CAD840` PAnimationClip, `02E4E430` PTypedObject, `02D3E680` PAssetReference, `02E4D630` PString, `02E41470` PScript, `02E4EAF0` PEntity, `02E4FF60` PNameComponent, `02E518D0` PNode, `02EA5560` PInputMapper, `02EA5380` PApplicationViewport, `02EA9400` PDebugUtils). Three (`02CF8470`, `02CF8980`, `02CF8A80`) are named nowhere, so the rows give only the address. The rows compare the address. They never read the object's contents, so nothing mutable is stated as a constant.

## Rows (FABLE)

27 rows, 135 interior anchors, page `22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md`.

| function | owner token checked on the page | anchors |
|---|---|---|
| `005CBE30` | `PMethodCallerConcrete` | 5 |
| `00610D00` | `PMethodCallerConcrete` | 5 |
| `0063E490` | `PFunctionCallerConcrete` | 5 |
| `0063E580` | `PMethodCallerConcrete` | 5 |
| `0063E6D0` | `PMethodCallerConcrete` | 5 |
| `0065E4B0` | `PMethodCallerConcrete` | 5 |
| `00677DE0` | `PFunctionCallerConcrete` | 5 |
| `00677E50` | `PMethodCallerConcrete` | 5 |
| `00677EC0` | `PMethodCallerConcrete` | 5 |
| `00677F30` | `PMethodCallerConcrete` | 5 |
| `0067F4D0` | `PMethodCallerConcrete` | 5 |
| `00686010` | `PFunctionCallerConcrete` | 5 |
| `00686070` | `PMethodCallerConcrete` | 5 |
| `006A6800` | `PMethodCallerConcrete` | 5 |
| `006ACBB0` | `PFunctionCallerConcrete` | 5 |
| `006ACCC0` | `PMethodCallerConcrete` | 5 |
| `006AF810` | `PMethodCallerConcrete` | 5 |
| `006B01A0` | `PFunctionCallerConcrete` | 5 |
| `006B6270` | `PMethodCallerConcrete` | 5 |
| `006C0640` | `PMethodCallerConcrete` | 5 |
| `006C0680` | `PMethodCallerConcrete` | 5 |
| `007A3200` | `PFunctionCallerConcrete` | 5 |
| `007A3260` | `PMethodCallerConcrete` | 5 |
| `007A34D0` | `PMethodCallerConcrete` | 5 |
| `007A3540` | `PMethodCallerConcrete` | 5 |
| `007A35A0` | `PMethodCallerConcrete` | 5 |
| `008742A0` | `PMethodCallerConcrete` | 5 |

Addresses the sentences cite besides the row's own function and anchors: `006AE780`, `006B1600`, `006B33F0`, `02CAD840`, `02CF8470`, `02CF8980`, `02CF8A80`, `02D3E680`, `02E41470`, `02E4D630`, `02E4E430`, `02E4EAF0`, `02E4FF60`, `02E518D0`, `02EA5380`, `02EA5560`, `02EA9400`. These are callees, compared or stored addresses, and `.data` bytes. Run the neighbour pre-check (`xlayer_full` edge tokens on these new cites) before publishing.

## Verification (FABLE)

[`apply.py`](apply.py) refuses to write until all of these pass:

- the page is clean (`git status --short`), and there is at least one row;
- each function is a certified function-list entry that the page does not already cite;
- each sentence has no pipe and is under 1,200 characters;
- each anchor is an instruction boundary strictly inside its function and decodes to the recorded mnemonic;
- the page cites each row's owner token.

With `--apply` it appends one section, `## No-reference bodies homed by owning class (FABLE, 2026-10-03)`. That section holds an italic note and the table `| function | size | what the body does | interior anchors |`. The append keeps the page's line endings and is idempotent: an identical block prints `ALREADY`. The script prints `FAILS n` last.

The dry run is [`apply_dryrun.out`](apply_dryrun.out): `VERIFY 27 functions, 135 anchors, page 22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md (LF)`, `FAILS 0`.

Controls, run on 2026-10-03 against copies (`--test-copy`, which skips only the git check):

- on a copy of the page: the first `--apply` prints `PATCHED` and the second prints `ALREADY`. The original bytes are a prefix of the result, and the line-ending counts are unchanged in kind.
- on a temporary record seeded with a wrong mnemonic, an entry-address anchor, a pipe and an unknown owner token: it printed four kinds of VERIFY FAIL and `FAILS 6`.
- with zero rows: it printed `FAILS 1`.
- pointed at the dirty Gi page: it refused with `page is dirty` and `FAILS 1`.

The temporary record was deleted afterwards.

## Limits (FABLE)

These are body statements, not meanings. A value read from `.data` is stated by address and never as a constant. The section is appended at publish time, and the publish gates (neighbour pre-check, `verify_doc_addresses`) run on the result. Nothing here is committed. The page and the register are untouched.

## Consumer check (FABLE)

affected: Database/FFXII TZA/22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md

- consumer: this page's new section `No-reference bodies homed by owning class (FABLE, 2026-10-03)`: revised-here (27 rows added; no existing text changed).
- consumer: EC7-211's shape paragraph on this page (`005CC180` ... `00684AB0`): agrees. It is scoped to the twelve thunks listed under it, which are void method callers plus the slot-1 `00684AB0`. The return-1 tag test and the missing NULL test of the function callers are stated per row in the new section, and EC7's text is left as it is.
- consumer: the class-descriptor page's descriptor-address tables (`02E4E430` PTypedObject and the others named above): agrees. The rows cite the addresses only.

run: apply.py at d02293770 (dry run verified 27 functions, 135 anchors, page 22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md (LF); FAILS 0)
