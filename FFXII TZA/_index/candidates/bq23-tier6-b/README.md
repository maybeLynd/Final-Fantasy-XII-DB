# BQ-23: the nine unmatched OrderedContainerRuntime members are EASTL and Phyre trees, not the C++ standard library (FABLE, Claude Opus 5.5, 2026-09-27)

**Question (BQ-23):** the untested `CxxStandardLibrary` sub-labels, checked against upstream source at tier 6.

The earlier record ([`bq23-tier6/`](../bq23-tier6/bq23_tier6.py), 2026-09-27) left 9 `OrderedContainerRuntime`, 9
`ContainerAllocatorSupport` and 21 `StdRegex.Runtime` members unmatched. It also routed an EASTL relabel for 18
members, which SWE2-EC7 has since applied (`FRONTIER-REQ-SWE2-EC7-EASTL-RBTREE-RELABEL`).

**Result: all nine unmatched ordered-container members are now matched, and none is MSVC STL.**

| members | what they are | discriminator |
|---|---|---|
| `001FDA60`, `001FD9A0`, `001FDAC0`, `00200140` | EASTL `rbtree::DoNukeSubtree` (three destroy a nested vector/string in the value first) | recurse on `[node+0]` (right), keep `[node+8]` (left), free through the rbtree's allocator slot `+0x18`, loop until null |
| `001FC3A0` | the same loop inlined from the root at `+0x18` (clear / destructor; recursion through `001FDA60`) | as above |
| `001FC770`, `001FF990` | EASTL `rbtree::DoCopySubtree` | allocate through slot `+0x10` (or DoCreateNode `001FFAB0`), copy parent and the colour byte `+0x18`, recurse on the source's `[+0]`, walk its `[+8]` |
| `005A7BF0` (insert, caller `005A9560`), `0067F9D0` | a packed-colour red-black tree with **Phyre's `PRedBlackTreeNode` layout**: children `+0`/`+8`, parent\|colour at `+0x10` (colour in bit 0), key at node `+0x18` | the class descriptor carries this base at `+8` (RTTI) with its `PHashEntryConstKey` at `+0x20` = node `+0x18`; the claim is the node type, not that these trees hold descriptors |

**The MSVC shape is excluded, with a control.** MSVC's `_Tree::_Erase` stops at the `_Isnil` byte (`+0x19`), not at
null. The three members the earlier record matched to MSVC `_Tree` (`00712F60`, `0071E500`, `0079BA10`) fail the
EASTL shape (V4).

## Control

`bq23_ordered_residue.py` (4 checks, FAILS 0; output `bq23_ordered_residue.out`):
- **V1:** the relabel landed, 18 EASTL / 12 CxxStandardLibrary.
- **V2:** the seven EASTL routines.
- **V3:** the packed-colour pair.
- **V4:** the MSVC sensitivity control.

## What this changes

`CxxStandardLibrary.OrderedContainerRuntime` now holds 12 members:
- 3 are MSVC `_Tree`;
- **7 more are EASTL** and 2 are Phyre, so the relabel should extend to them. That is routed to SWE2-EC7, the label
  owner. The label table is not edited here.

## Still open (BQ-23)

- **`ContainerAllocatorSupport`, 9 members.** A lead, not a claim: six are small node builders.
  - `00714860`, `007148C0`, `00714920` and `0071F180` set three node pointers to the container head.
  - `0075EE00` and `00786980` set next/prev, with a null argument meaning self.
  - Both shapes fit MSVC's `_Buynode0`. But their allocation-failure path calls `_invalid_parameter_noinfo_noreturn`,
    not `_Xbad_alloc`, and the v140 (VS2015 Update 3) headers are not on this machine to check against.
  - `00203490`, `00204E50` and `00205330` sit in the `<regex>` span.
- **`StdRegex.Runtime`, 21 members.** These are MSVC `<regex>` template instantiations. Matching them needs the
  VS2015 `<regex>` source.

## Limits

Static, against upstream source at tier 6: EASTL's `rbtree.h` DoNukeSubtree / DoCopySubtree, and MSVC `<xtree>`
`_Erase`. Phyre's SDK source is not available, so the Phyre attribution rests on the RTTI class name and the layout
match.
