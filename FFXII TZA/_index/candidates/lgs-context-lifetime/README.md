# LegacyPs2GsTextureContext: its release, a second instance, and +0x1C0 as an owned pointer (OPUS, 2026-09-28)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**What was wrong.** The types row said:
- "one heap instance, cached at 0209A670";
- release "none identified - 0026E20C clears the global ... no deallocation of the 0x240 block was found".

The field row `addend01C0` said "ADDRESS TERM, NOT A POINTER" (OPUS, 2026-09-19).

**What the image says** ([`lgs_lifetime.py`](lgs_lifetime.py), L1-L6, FAILS 0).

| check | finding |
|---|---|
| L1 | `003EC860(cell, callback)` destroys a cell: it runs the callback on `*cell`, frees `*cell` through `003697F0`, then nulls the cell |
| L2 | both builders release the previous instance before allocating. `0026E760` does it on `0209A670`. `0026E7D0` does it on `0209A670` and `0209A668`, then builds a **second** 0x240 context and stores it at `0209A668` |
| L3 | `0026EDB0` is the destructor. It calls the function pointer at +0x128, then the ICF-folded `ret 0` `0016D6A0` on each of the two 0x68 chunk records at +0x40, so the element type's destructor is a no-op |
| L4 | the constructor stores `002F5450` at +0x128 |
| L5 | `002F5450` frees the owned blocks through `003EC8A0`: +0x1C0, +0x1C8, +0x1D0 and each record's +0xC0, +0x1D8, the +0x1E0 / +0x1E8 pairs, +0x210 and +0x218. It also releases +0x168 and +0x150 |
| L6 | +0x1C0 is `003EC8D0(6, count * 0x70)`, stored at `002F6F76`. It is an owned pointer; the one `add` read uses it as a base |

**The changes.**
- **`LegacyPs2GsTextureContext` types row.**
  - The release chain replaces "none identified" (struck).
  - The instance cell names the second instance, at `0209A668`.
  - `0026E20C`'s null store stays described as a defaults reset.
- **`LegacyPs2GsNestedChunkRecord68`:** its destructor cell is the no-op `0016D6A0`. The chunk pointers are borrowed.
- **Field rows.**
  - +0x128 is the teardown callback.
  - +0x1C0 is corrected from `addend01C0 uint64` to `ownedBlock01C0 void*`. The old text is struck and kept as WAS.
  - The other freed pointers note their release.

No page states the old claims.

**Run receipt.** Run verified at 8c37324ed:
- `lgs_lifetime.py` S FAILED before the patch and FAILS 0 after it;
- `types_index.py --validate` 0 errors;
- `check_type_refs.py` 0 dangling;
- `lgs_nested68.py` FAILS 0.

## Two more release cells, bounded (OPUS, 2026-09-28)

[`bounded_lifetimes.py`](bounded_lifetimes.py) (C1 / C2 / S, FAILS 0) takes an exhaustive rip-relative census of the
two cells over the listed bodies.
- **`Category`, table cell `02EAD008`.**
  - It has one writer: `007AAAA2` in the builder `007AAA40`.
  - The builder has one caller, `007A50E7`, and overwrites the cell without reading or releasing an earlier table.
  - No listed code frees the table or its entries. They live for the process if the build runs once; a second build
    would leak the first. Whether it runs again is not established.
- **`PendingCompletionQueue01F81248`, cell `01F81248`.**
  - It is written once, by the lazy ensure `001BDA50` after its null test, and otherwise only read by the getter.
  - It is built at most once and never nulled or freed in listed code.
  - A release by a getter caller is not excluded.

Both types' release cells now carry these bounded statements in place of plain "none identified".

## Three child release cells (OPUS, 2026-09-28)

[`lgs_children_lifetime.py`](lgs_children_lifetime.py) (R1-R3, S; FAILS 0).
- **`RenderCommandBuffer`: resolved.** `003EC8A0`, now read, frees through `003697F0` and nulls the cell. So its
  builders' first call is the release of the previous block.
- **`LegacyPs2GsReferenceDescriptor`: none of its own.** The context's teardown never touches +0x178. That is consistent
  with the array being an interior pointer into the loaded block, so its storage goes with that block.
- **`LegacyPs2GsSourceTextureRecord`: bounded.**
  - The teardown passes the +0x150 container to `00468060` -> `00467CB0`.
  - That path only unlinks and frees the nodes of the list at `02EBB6A0` that name the container (`00536140`).
  - Neither the container nor its record bank is freed there, so their release stays not established.

## InputManager (OPUS, 2026-09-28)

[`input_manager_lifetime.py`](input_manager_lifetime.py) (I1 / I2 / S, FAILS 0).
- **I1.** `001955F0`, which the row had left unread, is a scalar deleting destructor. It restores the vtable and, when
  flag bit 0 is set, calls the sized `operator delete` on 0x40 bytes. It releases no member.
- **I2.** The singleton cell `01F7FFE0` is written once, after its null test, and never cleared in listed code. So
  nothing in listed code destroys the singleton through its cell. Destruction through the getter's pointer is not
  excluded.

## ActiveLogWidget40C8 (OPUS, 2026-09-28)

[`active_log_widget_lifetime.py`](active_log_widget_lifetime.py) (W1-W3, S; FAILS 0) checks the row's presumption that the
widget "rides the widget hierarchy's recursive teardown". It holds.
- **W1.** The builder attaches the widget as a child of the manager's +0x1080 widget.
- **W2.** The widget release `00245020`, with +0x40 bit 5 clear, tail-jumps to `002482E0`.
- **W3.** `002482E0` frees a whole subtree: children first, then each widget's +0x60 block and the widget itself, through
  `003697F0`.

So the widget's release is its parent's. When the parent is released is not established.

## A stale child release cell (OPUS, 2026-09-28)

`BootSubBlock0338` has three elements embedded in `BootSingleton01F7F598`. Its release cell still said "the owner's
destructor is itself unestablished". The owner's cell is an established NONE: its cell `01F7F598` has one install-only
writer, `00189067`, so it is never released.

The stale clause is struck and the lifetime propagated: the elements live for the process.

[`lifetime_propagation.py`](lifetime_propagation.py) (P1) is the regression. No embedded type may call its owner's release
unestablished when the owner's cell leads with an established status. It reads each cell's leading status, not words in
its history. It FAILS on the pre-patch `types.tsv` (`--types`) and passes after.

## The source-texture record bank (OPUS, 2026-09-28)

[`source_bank_lifetime.py`](source_bank_lifetime.py) (B1 / B2 / S, FAILS 0) narrows the release cell further.
- **B1: the bank is freed on rebuild.** The container initialiser `00467D20` frees the previous bank at container+8
  (`003EC8A0`) before allocating the next, `count * 0x60`.
- **B2: a container destructor exists.** `00467B30` runs the container's +0x10 callback and then frees +8. It is wrapped by
  the destroy-cell `00467B20`, and neither has a direct caller.

What releases the context's own +0x150 container, or its bank at teardown, is still not established.

