# Affected-consumer check: PH-2 answered; the cluster-header contract's "none of it is in the image" corrected (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `ph2_header_swap_members.py` beside this file (10 checks, FAILS 0).

The contract's §14 item 2 (OPUS, 2026-09-15) said the static constructor builds an empty descriptor and that the
member list "is populated afterwards, at runtime, and none of it is in the image". The first half holds. The second
does not. The member lists the walk visits are filled by image code with constant arguments:
- `PClusterHeaderBase` has 18 members;
- `PClusterHeaderD3D11` has 3;
- `PClusterHeader` has none of its own.

Each member is a dword swapped in place. Together they are 21 dwords, all `0x54` bytes of the header. OPUS's
`s49-header-i1-static-bound.md` (2026-09-25) had already read the members; it never reached the contract or the
register row.

This pass adds who runs the registrations: `PUtilitySerialization`'s init slot, which the engine-init walk calls. It
also adds an image-wide absence sweep with a positive control. The run-time order against the first header load is
not read and stays open.

| consumer | what it said | state |
|---|---|---|
| `22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md` §14 item 2 heading | ADVANCED; "the descriptor's CONTENTS are still not in the image" | revised-here (heading kept as history; the dated answer is beneath it) |
| same item, the "WHY THIS DOES NOT REOPEN §13" bullet | "none of it is in the image. The row's premise was right and stays right" | revised-here (struck, corrected beside it) |
| same item, "Still open" bullet | the member list's runtime contents | revised-here (struck; the run-time order is what stays open) |
| same page §13a "What did not become established" | the fixture proves the swap for a descriptor "of that shape rather than the shape the game constructs" | revised-here (dated note: the shape is now read statically, and the fixture's five members are a subset of the 21) |
| same page §15 evidence ledger | no row for the member lists | revised-here (row added, PROVEN, static) |
| same page §13 (the quoted premise and FABLE's 2026-09-16 "premise is false" note) | the `.bss` premise | agrees (already superseded in place; untouched) |
| `_index/candidates/s49-header-i1-static-bound.md` | 21 members, `0x00`–`0x53`, each with the `bswap` leaf | agrees (the control re-derives it from the bytes) |
| `_experiments/EXP-094-phyre-header-exec.md`, member-node bullet | "member registration is deferred finalize machinery too deep to replay" | agrees as a replay-scope decision: it explains why the fixture spliced its own nodes, and the static bound already measures that fixture against the real list. Not edited. |
| `00-Engine-Core-Runtime/Object-Model/rtti-vtable-object-model.md` (the `PH-2` example) | the `.bss` premise was false; the object is named statically | agrees |
| `22-Middleware-PhyreEngine/Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md` | `ByteSwapBlock(&DAT_02CAA0A0, hdr, 1)` "flip the whole header"; the descriptor is the header's swap descriptor | agrees ("whole" is what the 21 members cover) |
| `_index/L2-VERDICTS.md` S-49 | extents `PClusterHeaderBase` 0x48 / `PClusterHeaderD3D11` 0x54 from the constructors | agrees (the control's P1 reads the same constructor arguments) |
| `_index/PARITY-STATUS.md` (the static-constructor row) | NOT EXERCISED | agrees (nothing here executes) |
| `_index/OPEN-QUESTIONS.md` PH-2 | PARTIAL; "the descriptor's CONTENTS are still not in the image" | revised-here (ANSWERED; the previous status kept as history) |
