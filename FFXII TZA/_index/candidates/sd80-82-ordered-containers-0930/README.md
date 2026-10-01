# SD-80 and SD-82: the fourteen MSVC tree bodies read, and no single-direction EASTL rotation anywhere (OPUS, 2026-09-30)

Register rows SD-80 and SD-82 were registered by SWE2-DATA:
- **SD-80** ([the-msvc-ordered-container-runtime.md](../../../24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md)
  section 7) asks what the fourteen profiled MSVC `std::_Tree` bodies do, read end to end.
- **SD-82** ([the-ordered-container-runtime.md](../../../24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-ordered-container-runtime.md)
  section 7) asks whether any body inlines a single EASTL rotation direction, or any body over 20,000 bytes inlines one.

This record is static. The checker is `sd80_82_trees.py` (output `sd80_82_trees.out`, `FAILS 0`). It uses
`Tools/analysis-kit/gfz-scripts/retool.py` and the rotation matcher's `pe` module from
`_index/candidates/rc22-34-resource-readers-0930/`.

## SD-80: what the fourteen do (OPUS)

**The node layout.** `_Left +0x00`, `_Parent +0x08`, `_Right +0x10`, `_Color +0x18` (1 = black), `_Isnil +0x19`,
value from `+0x20`. The tree object holds the head node at `+0` and the size at `+8`. The head's `_Parent` is the
root, its `_Left` the leftmost node and its `_Right` the rightmost.

**How they were read.**
- **S1: nine by identity with a read body.** Nine of the fourteen are instruction for instruction the body of a
  sibling. The siblings were either read whole by the page (`00714B60`, `0079B930`) or are read here (`00714980`,
  `00799BD0`). Rip displacements and call targets are masked for the comparison. Each call target is then the
  same-role body of the profiled body's own instantiation (A, B or C). For example, B's erase-range calls B's tidy
  `0071F3A0` and B's node erase `0071F590`.
- **S2–S6: five read directly** (with one proven identical to a read body).

| body | instantiation | what it is | how |
|---|---|---|---|
| `0071F240` | A / B (shared) | `_Lrotate`: y = x->_Right, x->_Right = y->_Left, parent relinked (root when x is the head's `+8`), y->_Left = x. Same code as C's `00799BD0` | S1, S2 |
| `0071F590` | B | `erase(iterator)`: `0079BA10` plus the value destructor before the free. Otherwise it differs only in register allocation | S6 |
| `0079BA10` | C | `erase(iterator) → iterator`: successor first (the right subtree's minimum, else climb), then unlink. With two children, the successor is spliced in and the colours (`+0x18`) swapped. Then leftmost / rightmost are refreshed; if the erased colour is black, the fix-up loop recolours and rotates (`00799C30` / `00799BD0`); the node is freed, the size (`tree+8`) decremented and the successor returned | read whole, S5 |
| `00714BE0`, `00714C60` | A | `_Tidy`, identical to the read `00714B60` | S1 |
| `0079B0D0` | C | `_Tidy`, identical to `00714B60`, calling C's subtree erase | S1 |
| `00714980` | A | `_Erase(subtree)`: while the node is not nil, recurse on `_Right`, step to `_Left`, free | read, S3 |
| `0071F1E0` | B | the same, plus the value destructor `0071EE70(node+0x20)` before each free (the only difference) | S3 |
| `00799B80` | C | identical to `00714980` | S1 |
| `0071EE70` | B | `pair<string, string>::~pair`: the second string (`+0x20`), then the first (`+0`). A capacity (`+0x18`) of 16 or more releases the heap buffer through `001DFA10` (capacity + 1); then capacity = 15, size = 0, buffer[0] = 0 | read, S4 |
| `00714CE0`, `00715110`, `007151F0` | A | `erase(first, last)`, identical to the read `0079B930`: a whole range goes to that map's own tidy, otherwise the node erase `00714DC0` loops | S1 |
| `0071F4B0` | B | the same, to B's tidy `0071F3A0` and node erase `0071F590` | S1 |

- **For modding.** The page's role labels, previously from store offsets, all hold on a read. The three
  instantiations share one code shape. Only B, the `string → string` map, destroys its values.
- **Direction named.** The page's §3 table calls `0071F240` "rotation, pair A — the mirror". Read, it is the left
  rotation of the shared A / B pair, and `00714B00` is the right one.

## SD-82: no single-direction EASTL rotation anywhere (OPUS)

- **B1: the sweep without a size cap.** DATA's matcher (`crt_rbtree_checks.py` E4) is re-run over all 38,161 bodies,
  including the 8 over 20,000 bytes, and single-shape hits are recorded too.
  - **12 bodies** match either EASTL rotation shape (children `+0` / `+8`, parent `+0x10`).
  - **Both shapes:** only the four already known, `0016D840`, `0016DA60`, `0067F700` and `0067F9D0`.
  - **One shape:** the two EASTL rotation functions themselves, `0016D780` and `0016D7E0`, and six others.
- **B2: the six are not EASTL.**
  - **Four are MSVC-layout code.** They test the `_Isnil` byte at `+0x19` and keep the parent at `+8`: the
    `_Rrotate` copies `00714B00` / `00799C30`, and the inserts `00712F60` / `0071E500`. The MSVC right rotation's
    store order happens to match the EASTL signature.
  - **Two are not tree code.** `00207DE0` allocates a 0x30 record and links it. `00820D00` pushes 16-byte stack slots
    and calls on.
- **So:** no body in the image inlines a single EASTL rotation direction, and none over 20,000 bytes inlines either.

## Limits (OPUS)

- **The matcher is a store-order signature.** A rotation compiled with a different store order would not match
  (as for E4).
- **Body list.** The sweep covers the `pe` module's 38,161 function bodies. Code outside that list is not swept.
- **SD-81** (the 99 EASTL callers' purposes and value types) is **not** addressed here.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register rows belong to SWE2-DATA's pages.
