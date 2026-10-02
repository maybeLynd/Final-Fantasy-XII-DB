# SD-62: what the root's lists and the `01F2E780` structure chain (SWE2-ORACLE, 2026-09-30)

Register row SD-62 ([how-a-class-registers-its-array-members-and-annotations.md](../../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/how-a-class-registers-its-array-members-and-annotations.md)
section 7) was narrowed by OPUS ([`sd62-static-array-elements-0930`](../sd62-static-array-elements-0930/README.md),
`e2777d3c8`, accepted by SWE2-AUDIT-SPEC). It left one question open: what the lists chain. This record reads the link
writers and names one element type per list. It also finds that one slot attribution in OPUS's F3 belongs to the
neighbouring object.

**Evidence class: static only.** Pinned instructions in the certified image, read through `retool.py`. Nothing is
executed and nothing is live. Checker: `sd62_registry_lists.py`, output `sd62_registry_lists.out`, checks L1-L8 and
control C1, `FAILS 0`. **Proposed status: ANSWERED for the chaining question**, with the limits below.

## The root `01F2E330`: three list heads, three element types (SWE2-ORACLE)

The root has three `{next, prev}` heads, at `+0x00`, `+0x10` and `+0x28`. `+0x20` is a registration-phase dword. The
static bytes and every rip store self-link all three heads.

| head | what it chains | link | writer (static) | readers |
|---|---|---|---|---|
| `+0x10` | **class descriptors** whose owner (`descriptor +0x70`) is the root | `descriptor +0x50` | `00639160` (L1) | `008AF490` (exit: deleting destructor `vt+0x38` when `+0xFC` bit 0), `00637A70` (size and offset pass over the `+0x78` base chain), `00638C90` (unregister-all) (L2) |
| `+0x28` | **other owner objects**: owners that are not the root, linked when they receive their first descriptor | the owner's own `+0x00` node | `00639160` at `0063924C`-`00639277` (L3) | `00638C90` has an owner-unlink arm (`00638D6B`-`00638D89`), but it walks only root `+0x10`, whose descriptors carry owner = root when linked, so it is not shown to unlink a non-root owner. No unlinker of root `+0x28` is shown. (L3) |
| `+0x00` | **nothing**: it is the root's own membership node, the one that would put it on `+0x28` | - | only the self-link initialisers. There are 30 rip stores to `+0x00`/`+0x08`, all of the root's own address (L4). `00639160` skips the root at `0063925B` (L3). | - |

**The link writer is `00639160(owner, descriptor)`** (L1). It has 12 call sites. Among them are `00636280`, a
module's batch registration, and `00635B80`, which registers `PWorld`.
- If the descriptor's base class (`+0x78`) has the same owner, the descriptor's `+0x50` node goes right after the
  base's node. Otherwise it goes at the front of the owner's `+0x10` list, as `[head+0]`. That makes it the first
  node the `+0x00` walkers `008AF490` / `00637A70` / `00638C90` visit (`0063922E`-`00639244`).
- A duplicate name, found by `0063BA10`, is refused through `005CDAA0`.
- Owner phase `+0x20 == 1` re-runs the size pass `0063E410`. Phase 2 reports an error.

The descriptor constructor `00632D80` only self-links `+0x50` and stores the owner at `+0x70`. That agrees with
SWE2-AUDIT-SPEC's review. List membership is `00639160`'s work, not the constructor's.

## `01F2E780`: a name index over class descriptors, not a record on `PWorld` (SWE2-ORACLE)

- **L5: it is a 0x30-byte balanced-tree header.** Its initialisers (`00638F00`, and inline in `00636280`) write exactly
  `01F2E780`-`01F2E7A8`, six qwords, every one `01F2E780`. The image bytes agree. `+0x18` is the tree root that
  `006311D0` / `006314B0` walk. Its exit destructor is `008AFDE0` → `0067F580(01F2E780)`.
- **L7: its elements are class descriptors, keyed by name.**
  - Insert: `006388C0(descriptor)` keys the node at `descriptor +0x08` with `+0x20` = hash(name) and `+0x28` = the
    name (`+0x30`), then calls `006314B0`.
  - Remove: `00638F00(descriptor)` passes `descriptor +0x08` to the tree remover `0067FE20`.
  - Find: `006311D0` compares the hash dword at node − 8 + 0x20, then the names with `strcmp`.
  - `00636280` removes a same-named old descriptor from the tree before it registers the new one.
- **L8: the key hash** is h0 = `0x7B5`, h = h × 33 + (c & 0x1F), over the name. It is the same hash OPUS saw in
  `0059B430`, which fetches this index through `00637440`. Its search call was not re-read here.
- **L6 differs from OPUS's F3.** The `PWorld` descriptor pointer and `"getInstanceCount"` sit at `01F2E7C0` /
  `01F2E7C8`. Those slots are `+0x10` / `+0x18` of a **separate record at `01F2E7B0`**, not `+0x40` / `+0x48` of
  `01F2E780`:
  - `01F2E7B0` has its own initialiser `00635B80` and its own exit destructor `008AF430`.
  - `00635B80` checks through `005A7A40` whether `PWorld` already has a method of that name. If it does not, it links
    `01F2E7B0` at the tail of the `PWorld` descriptor's `+0x90` list (`02CF8B10`).
  - `008AF430` unlinks that record and frees its `+0x18` when `+0x20` bit 0 is set.
  - So `01F2E7B0` is a method-registration record for `PWorld::getInstanceCount`.
  - `01F2E780`'s own initialisers never touch `01F2E7B0` or anything above it.

  The regression is L5 + L6: they reject reading those two slots as part of `01F2E780`. This also means the objects
  from `01F2E780` up do not follow the section's `0x50` stride: `01F2E780` is 0x30 bytes, and `01F2E7B0` is a record
  of at least 0x30 bytes. `00635B80` also sets its `+0x28` to `01F2E7E0` and writes `01F2E7E0` / `01F2E7E8`
  (`00D59070` / `0063BEF0`) on every path (`00635C2F`-`00635C52`). Whether the pair at `01F2E7E0` belongs to the
  record is not settled. The rest of the section 7 array was not re-read here.

## Controls (C1) and limits (SWE2-ORACLE)

- **C1:** over the reflection range `00630000`-`0063FFFF`, the scan looks for a node address (`lea r, [x+0x50]` or
  `add r, 0x50`) followed by a store of `r` that is not a self-link, stopping when `r` is redefined. It finds
  `00639160` and nothing else, and the gate pins the exact set (`fs == [00639160]`). Both shapes are exercised by
  positive controls inside `00639160` itself (`lea` at `00639212`/`00639231`, `add` at `0063921A`; store
  displacements below 10 print decimal, and the store regex accepts that). The shape is therefore detected, and the
  range has one `+0x50` inserter.
  - Outside that range the scan was not run. A descriptor linked by code elsewhere, or by a different instruction
    shape, would not be seen. This is a domain-limited negative.
- **Dynamic owners.** Which non-root owners exist at run time is not decided here. Examples are the `rdx` a module
  blob supplies to `00636280`, and the stack value `0059AC00` passes to the 385th constructor call. L3 shows only how
  they are chained.
- **The `+0x90` list** of a descriptor (methods, L6) and the descriptor's other self-linked heads (`+0x60`, `+0x80`,
  `+0xA0`, `+0xB0`) are outside this row.

## For SWE2-DATA (row text proposal, not applied here) (SWE2-ORACLE)

SD-62: the root `01F2E330` chains class descriptors on `+0x10` (node `+0x50`, writer `00639160`) and non-root
owner objects on `+0x28` (node `+0x00`). Its `+0x00` is its own never-linked node. `01F2E780` is a 0x30-byte
name-hash tree of class descriptors (node `+0x08`, key `+0x20` hash / `+0x28` name, insert `006388C0`, remove
`00638F00`). The `PWorld` / `"getInstanceCount"` slots belong to a separate method record at `01F2E7B0`, linked into
`PWorld`'s descriptor `+0x90` list by `00635B80`.

**Review:** SWE2-AUDIT-SPEC (`ORACLE-REQ-AUDITSPEC-SD62-0930`). **Row:** SWE2-DATA (`ORACLE-REQ-DATA-SD62-ROW-0930`).
