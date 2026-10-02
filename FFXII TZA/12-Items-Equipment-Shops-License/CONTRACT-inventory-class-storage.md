---
contract: read and change how many of an item the party holds, through the item id's class
category: 12-Items-Equipment-Shops-License
scope: family
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md
entries: ["002FD8D0", "002FD970", "002FD150", "002FD420", "003047F0", "00309440", "00309F30",
          "003008A0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 41 addresses cited - 1 data, 8 entry, 32 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-inventory-pass-1     # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — inventory class storage

An item id is `(class << 12) | index`. The class picks one of **fifteen descriptors**, and the
descriptor decides *everything else*: how many ids exist, which of two storage schemes holds them,
where that storage is, and whether the class works at all. **~~Two~~ Three of the fifteen answers are "it does
not work", and four more classes declare items with no storage behind them.** *(corrected 2026-10-02, OPUS: descriptor `+0x3C` is 0 on rows 5, 7 and 11, §10; the four storage-less classes 9, 10, 13 and 14 still grant through their `+0x48` handlers)*

A reimplementation that models inventory as one array of counts will be wrong for eight of the fifteen
classes.

## 1. Purpose

The id encoding and the class registry are [the item-id page's](item-id-encoding-and-equipment-compatibility.md).
This states the **storage** behind them: the descriptor's layout, the two schemes, the bit widths, the
cap, and what happens on the classes that have no handler — the parts a reimplementer needs and cannot
get from the encoding alone.

## 2. Interface

| | |
|---|---|
| the table | `01EEBCC0`, **15 rows** of `0x58` |
| class from an id | `id >> 12`, rejected when `> 0xE` (`00309F51`, `00309446`) |
| index from an id | `id & 0xFFF`, rejected when `>= descriptor->itemCount` |
| refused outright | `0xFFFF` by both entries. **`0x1000` (class 1, index 0) by the ±1 entry only** (`003008D8`–`003008E0` → `-1`, no store). The query entry `00309F30` has no such test and reads it (executed 2026-09-26, OPUS, §13) |
| query, packed | `002FD8D0` `InventoryPackedCountClass_QueryChannel` |
| query, bitset | `002FD970` `InventoryBitsetClass_QueryState` |
| mutate, packed | `002FD150` `InventoryPackedCountClass_MutateChannels` |
| mutate, bitset | `002FD420` `InventoryBitsetClass_MutateState` |
| clear all packed | `003047F0` |
| class id of a row | `00309440`, 30 bytes, returns `+0x38` |
| the ±1 entry point | `003008A0` `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` |
| a mode-1 wrapper of it | `00300BA0`, 28 bytes (read whole 2026-09-19): the first two arguments pass through, the third and fourth are the constants 1 and 1, and the wrapper's own third argument goes on the stack |

**Dispatch is per class, through a pointer in the descriptor** (~~`+0x50`~~ `+0x50` for a query, `+0x48` for a mutate *(corrected 2026-10-02, OPUS: checked at `00309F96` `mov rax, [rdx+0x50]` and `00300943`–`00300960` `mov rax, [rsi+0x48]` / `test` / `call rax`; CONTRACT-bazaar-unlock-and-purchase.md §13a)*), not by a switch. `rcx` is the
encoded id; `edx` is a **query kind**, `0..4`, and the kind chooses which of the class's arrays is read.

## 3. Types

`ItemClassDescriptor`, `0x58`, fifteen rows — in `_types`. The fields this contract depends on:

| | |
|---|---|
| `+0x08` | the word-addressed array. Packed classes: one `uint16` per item. Bitset classes: **16 bits per element**, `index >> 4` picks the word and `index & 15` the bit |
| `+0x10` | how many `uint16` **elements** `+0x08` holds — **not** the item count |
| `+0x20` | packed classes: the per-item **count byte**. Bitset classes: a **bit** array, `index >> 3` and `index & 7` |
| `+0x30` | a second byte-addressed bit array, bitset kind 4 only |
| `+0x38` | the registry class id — exactly `nibble + 5` for all fifteen rows |
| `+0x3C` | how many item ids the class defines |
| `+0x50` | ~~the handler, or **NULL**~~ the query handler, or **NULL**; the mutate handler is a second pointer at `+0x48` *(corrected 2026-10-02, OPUS: checked at `00300943`–`00300960`; CONTRACT-bazaar-unlock-and-purchase.md §13a)* |

**`+0x10` is the field a reimplementation gets wrong.** For packed classes it equals `+0x3C`; for every
bitset class it is `ceil(+0x3C / 16)` — 81 ids to 6 elements, 24 to 2, 256 to 16, 512 to 32, 32 to 2.
Sizing the array from `+0x3C` over-allocates the bitset classes sixteenfold **and mis-clears them**,
because the clear loop runs to `+0x10`.

**Who reads `+0x10` and `+0x38`, and why a census can miss them (added 2026-09-19, FABLE, on
`OPUS-REQ-FABLE-INVENTORYCLASS-AUTHORED-UNREAD-SPANS`).** Both fields have readers, but the readers address the table
through **shifted bases**, so a sweep keyed on `01EEBCC0` finds nothing: the clear-all loop `003047F0` walks the rows
from `lea 01EEBCD0` - `+0x10` is its `[rax]` and the `+0x08` pointer its `[rax - 8]` - zeroing `+0x10` words per class;
the temporary-state snapshot `0030FBE0` compares against `01EEBCD0` directly (class 0's count as a loop bound); and the
class-id reader `00309440` indexes from `lea 01EEBCF8`. **`+0x44` is different: zero in all fifteen rows of the image and
referenced by nothing** - the alignment gap between the dword at `+0x40` and the pointer at `+0x48`. *(A measurement
that finds it non-zero in 12 rows with 7 distinct values has read the low half of that pointer four bytes early: six
handlers and null.)*

**The layout confirms `+0x10` without any consumer.** The authored offsets at `+0x00` form one contiguous run - each
class's array starts where the previous one ends:

| class | 0 | 1 | 2 | 3 | 4 | 6 | 8 | 12 | end |
|---|---|---|---|---|---|---|---|---|---|
| `+0x00` | `0x4748` | `0x47C8` | `0x4B10` | `0x4F10` | `0x4F1C` | `0x4F20` | `0x4F40` | `0x4F80` | `0x4F84` |
| `+0x10` words | 64 | 420 | 512 | 6 | 2 | 16 | 32 | 2 | |

Every step is `2 x (+0x10)` bytes. The rebase pass `0030B6A0` adds the state block's base to these offsets (and to the
two auxiliary ones: class 0's `+0x28` = `0x57C0`, class 2's `+0x18` = `0x57C8`) and writes `+0x40` as the running sum of
`+0x3C` - the class's first item as an ordinal across all classes.

## 4. Preconditions · postconditions · invariants

**Preconditions.** The class must be `<= 14`; the index must be `< +0x3C`, tested against `count - 1`
as a **signed** compare (`00309F80`–`00309F82`), so a class with `itemCount == 0` rejects every id.

**Precondition: the storage pointers must have been bound.** All of `+0x08`, `+0x20` and `+0x30` are
**NULL in the image** for all fifteen classes — the table is static, the storage is bound at runtime —
and **every** handler null-tests before dereferencing.

**Invariant: the handler and the `+0x10 : +0x3C` ratio must agree.** One says how the bits are packed;
the other says how many were allocated. They are two statements of the same fact and nothing enforces
their consistency.

**Postcondition of a mutate: the stored count is at most 99** (§6).

## 5. State

The three arrays a class may own, and nothing else. The descriptor table itself is never written.

## 6. Relationships

**Dispatch is per class, through a function pointer in the descriptor at ~~`+0x50`~~ `+0x50` (query) or `+0x48` (mutate)** *(corrected 2026-10-02, OPUS: `00309F96`, `00300943`–`00300960`)* — not a switch —
so every operation below reaches its class's code the same way and the descriptor table is the only
thing that binds an id's class to an implementation. The encoded id splits into
`class = id >> 12` and `index = id & 0xFFF`, and both halves are validated against the descriptor
before anything is read (§2).

The ±1 entry point `003008A0` is the one caller that reaches these operations from outside the
subsystem; everything else in §2 is reached through the descriptor pointer.

**Added 2026-09-12 (`OPUS-CONTRA-SECTION-NUMBERS`)** — this contract had no `Relationships`, so every
later heading sat one number below the template. `check_gate26` reads section 13 and found
`Unresolved`; `parity_status` reads section 15 and would have found the parity plan. Nothing here is
new analysis; it restates §2's dispatch note where the template expects it.

## 7. State transitions — the cap, which is not where it looks

```
002FD204  cmp   ecx, 0x63        ; (current + delta) against 99
002FD207  jle   0x2fd220         ; under the cap
002FD209  mov   r8d, 0x63        ; else clamp
002FD20F  mov   byte ptr [r10], r8b
```

**The 99 cap is a decision in the writer, not a property of the field.** That byte holds 255 and the
`+0x08` owned field is ten bits wide and holds 1023. **Raising the cap is a code patch at `002FD209`,
not a data change** — the same shape as the stat cap, where raising an authored row past 99 changes
nothing because the clamp is in the rebuild.

**The packed word carries two counts.** `(reserved << 10) | (owned & 0x3FF)`, built at
`002FD28C`–`002FD294` and read three ways by the query kinds: kind 1 returns `owned`, kind 2 returns
`reserved`, and **kind 0 returns `owned - reserved`**. ~~That subtraction is the availability the~~
~~item-use path needs, because an item is reserved when the character commits and consumed later.~~ The high six bits are the **equipped** count, not an item-use reservation: equipping adds 1 on channel 2 (`0030C447`–`0030C45C`) and unequipping takes 1 (`0030F9D7`–`0030F9EB`), only for `0x1nnn` ids other than `0x1000` (`0030C426`–`0030C445`), while an item action takes from the owned count at once on channel 1 (`0030EF9F`–`0030EFB0`) and keeps its reservation on the unit at `+0xDC8`. So kind 0 is owned minus equipped, the free copies *(corrected 2026-10-02, OPUS: checked at those addresses; equipment-slots-and-the-single-stat-rebuild.md §3, using-an-item-is-an-action-that-costs-an-item.md §3)*.

## 8. Script · resource · event interactions

The descriptor table is authored and compiled into `.data`; the storage behind it is not.

## 9. Determinism

Total. No RNG, no timing, no threading.

## 10. Failure paths and edge conditions

**A NULL handler is not a crash.** Both call sites null-test ~~`+0x50` (`00309F9A`, `00300946`)~~ their own slot, the query entry `+0x50` (`00309F9A`) and the ±1 entry `+0x48` (`00300946`) *(corrected 2026-10-02, OPUS: checked at `00300943`–`00300960`)*, so a
query on a handler-less class returns `0` and a mutate does nothing.

**Four classes declare items that nothing can store.** Classes 9, 10, 13 and 14 have `itemCount` of
512, 256, 128 and 4095 with ~~**no handler and `+0x10 == 0`** — two independent fields agreeing. Those~~
~~ids pass the bound check and then reach nothing. **4,991 encodable, inert ids.**~~ `+0x10 == 0` and no **query** handler, so a query answers 0 — but each has a **mutate** handler at `+0x48`: `002FD530` (reward package: gil and nested items), `002FD640` (package selector), `002FD780` (bazaar good: its granted pairs) and `002FD880` (gil as the id, `(id & 0xFFF) × delta`, `002FD89A`–`002FD8B4`). They are grant-expanding classes, not inert ones *(corrected 2026-10-02, OPUS: descriptor `+0x48` of rows 9, 10, 13 and 14 read from `01EEBCC0`; item-id-encoding-and-equipment-compatibility.md §3)*.

**Three classes are simply empty** — 5, 7 and 11, `itemCount == 0`, rejecting every id.

## 11. Observable behaviour

Not established. What would be observable: an item count that stops rising at 99 while the field
behind it is nowhere near full.

## 12. Reproduction formula

```c
typedef struct {                 /* 0x58, fifteen rows at 01EEBCC0 */
    uint16_t *words;             /* +0x08  packed counts, or a 16-bit-word bitset */
    uint32_t  elements;          /* +0x10  COUNT OF WORDS, not of items */
    uint8_t  *auxA;              /* +0x20  count byte (packed) or bit array (bitset) */
    uint8_t  *auxB;              /* +0x30  bit array, bitset kind 4 only */
    uint32_t  classId;           /* +0x38  == (row + 5) */
    uint32_t  itemCount;         /* +0x3C  how many ids exist */
    QueryFn   handler;           /* +0x50  NULL on seven of fifteen */   // <- corrected 2026-10-02, OPUS: the query handler; the mutate handler is a separate pointer at +0x48 (00300943-00300960), null only on rows 5, 7, 11
} ItemClassDescriptor;

int Query(uint16_t id, int kind) {
    unsigned cls = id >> 12, idx = id & 0xFFF;
    if (cls > 14) return -1;
    ItemClassDescriptor *d = &table[cls];
    if ((int)idx > (int)d->itemCount - 1) return 0;
    if (!d->handler) return 0;                     /* silent, not an error */
    return d->handler(id, kind);
}

int PackedQuery(uint16_t id, int kind) {           /* 002FD8D0 */
    /* ... kind 1: w & 0x3FF   kind 2: w >> 10   kind 0: (w & 0x3FF) - (w >> 10) */
}
```

## 13. Runtime validation

**Evidence class: isolated original-code, over THREE of the seven entry points. Live capture: still
absent.** (2026-09-12)

**What ran:** the class reader `00309440`, the packed query `002FD8D0` and the bitset query
`002FD970`, at their real virtual addresses with the descriptor table at `01EEBCC0`.
**What did not:** ~~both mutators, the clear-all and the ±1 entry — they dispatch through the function~~
~~pointer at descriptor `+0x50`, which is a different shape and a different fixture.~~ *(answered: see the supersession directly below — on 2026-09-26 the ±1 entry `003008A0` and both mutators ran as native replay, 16 / 16; they dispatch through descriptor `+0x48`, not `+0x50` (`00300943`–`00300960`); only the clear-all `003047F0` has not run; 2026-10-02, OPUS)* Said here rather
than left to be inferred from a green result.

**Superseded for §4, 2026-09-26 (OPUS):**
[`s29-opus-replay-inventory-storage`](../_index/candidates/s29-opus-replay-inventory-storage/README.md) executes the ±1
entry `003008A0`, the query entry `00309F30` and all four storage handlers (`002FD150`, `002FD420`, `002FD8D0`,
`002FD970`). They run as native replay with **no stub**, over the storage bound by the shipped rebase `0030B6A0`.
**16 / 16.**
- **P3.** In the unbound image, every query kind and every channel returns without a fault or a store, for all eight
  storage classes.
- **P1 / P2.** Nibble 15 is refused by both entries. The last id is accepted, and the first past it is refused with no
  store. The count-0 classes 5, 7 and 11 refuse every id.
- **The postcondition.** Across 168 mutates (four channels × two modes × seven deltas, packed classes), every stored
  count is ≤ 99, and the cap is reached on the word and on the byte.
- **The invariant.** In every storage class, the first and the last id write inside the region that `+0x10` / `+0x3C`
  allocate, and the last id writes the last element. **Nothing enforces the agreement:** with class 3's handlers swapped
  to the packed pair, id 80 writes `+0x4FB0`, outside the class, and the call succeeds.
- **Not in §4, found by execution:** the ±1 entry also refuses id **`0x1000`** (`003008D8`–`003008E0`), and the query
  entry reads it (§2).

**Instrument:** [`diff_inventory_query.py`](../../../Reconstruction/Tests/Differential/diff_inventory_query.py)
against [`inventory_query.c`](../../../Reconstruction/Game/Items/inventory_query.c).

**Result: 170 commands, 146 compared lines, 0 mismatches** — 44 distinct packed answers out of 59,
bitset answers split 26 true to 41 false, and 2 of 20 class reads returning `-1`.

**Mutation campaign: 60 mutants, 45 KILLED, 0 SURVIVED**, 6 EQUIVALENT, 0 INVALID, 9 NO_BUILD, over
the reconstruction and its header, with `production_inputs_stable: true` and the four input hashes
re-checked against the files as published. Run twice — once on the first draft and again after the
claim table below was written — with identical counts.

**The six equivalences are worth naming, because three of them are the finding.** The mutants
`>> 31` → `>> 32`, `& 7` → `& 8` and `>>` → `<<` inside the byte-bitset sign correction all compile
**byte-identical** (`/Brepro`) to the unmutated build: the compiler can see the index is
non-negative and folds the whole correction away. That is what an unreachable branch looks like from
the outside, and it is independent confirmation of the claim below that the correction cannot fire.
The other three are the table address `01EEBCC0` — which this suite plants its own table for and
never dereferences — and the two mutants of the compile-time row-size assert.

### The packed word is a total, a reservation, and a difference

This is the finding, and the run is what produced it. `002FD8D0`'s four kinds are not four views of
one number:

| kind | what it returns |
|---|---|
| 1 | `word & 0x3FF` — the **total**, ten bits |
| 2 | `word >> 10` — the ~~**reserved**~~ **equipped** count, six bits *(corrected 2026-10-02, OPUS: channel 2 moves it on equip and unequip, `0030C447`–`0030C45C`, `0030F9D7`–`0030F9EB`; §7)* |
| **0** | **`(word & 0x3FF) − (word >> 10)`** — the **available** amount |
| 3 | a byte from a different array, at descriptor `+0x20` |

**Kind 0 is a subtraction** (`002FD952`–`002FD95B`), and the reconstruction first had it as "the
whole word" — which agreed on nothing and was corrected by the first run. The available figure is
**signed and observed negative** in this suite, so more may be reserved than held.

### Three bitsets in two shapes, and a correction that cannot fire

`002FD970` answers a bit from `+0x08` as a **uint16** array (kinds 0 and 1, index `>> 4`, bit
`& 0xF`), or from `+0x20` and `+0x30` as **byte** arrays (kinds 3 and 4, index `>> 3`, bit `& 7`).
Kind 2, and every unhandled kind, returns 0.

The two byte paths compute their index with the signed-division idiom — `cdq`, `and edx,7`, add,
`sar 3` — and the word path does not. **The correction can never fire**, because the index was masked
with `0xFFF` before it and is never negative. It is reproduced as written: a reimplementation that
dropped it would be right by accident, and wrong if the mask ever moved.

### One bound, on one entry point

The class reader rejects a class above `0x0E` and returns `-1`. **Neither query bounds the class at
all** — they index the descriptor table with whatever the top nibble gives them. Driven at class
`0x0E` and `0x0F`, where the three entry points disagree.

### What is still owed, and it is live-only

Unchanged: read `+0x08` for class 1 in a loaded game. Nothing here bears on it — every array in this
suite is planted, which is exactly why the NULL arms could be driven and the binding question could
not.

One check settles the largest remaining unknown and needs no particular save: **read `+0x08` for
class 1 in a loaded game.** Non-NULL names the binder's effect and confirms the runtime-binding
reading; NULL on a loaded game would mean the packed classes are bound later than expected, or not at
all. Queued as **class B** of `OPUS-REQ-ASTRA-TRIAGED-QUEUE`.

**Experiment records that name this contract** — found by `OPUS-CONTRACT-RUNTIME-AUDIT`, 2026-09-13. Each names this
contract in its own `contract:` frontmatter while this section did not cite it back.

- [`EXP-064`](../_experiments/EXP-064-resource-payer-controls.md) — **method B**, isolated original-code execution.

**None of these is a live run**, so none of them changes the evidence-class statement at the
top of this section. They are listed because a reader auditing what has been executed against
this contract should not have to find them from the experiment side only.

## 14. Unresolved

- ~~**Who binds `+0x08`, `+0x20` and `+0x30` at runtime, and from where.**~~ *(answered: see §3 — the rebase pass `0030B6A0` binds them, run from the state block's first bind `00233C10` and the save rebind `00238A80`; item-class-descriptor-accesses.tsv, its `+0x08`, `+0x20` and `+0x30` rows; 2026-10-02, OPUS)* Routed as
  `OPUS-REQ-FABLE-INVBINDER`. Both candidates I first named are eliminated: `003047F0` is the clearer
  and `00309440` is a 30-byte reader of `+0x38`.
- ~~Whether the four inert classes are unreleased content or an allocation that moved.~~ *(answered: see §10 — classes 9, 10, 13 and 14 are not inert; their `+0x48` mutate handlers expand a write into gil or nested items; 2026-10-02, OPUS)*
- The remaining bytes of the `0x58` descriptor.

## 15. Evidence

Static, from the shipping image (`73461D08…`). Both query handlers and the packed mutator were
disassembled and read; all fifteen rows' `+0x10`, `+0x38`, `+0x3C`, `+0x50`, `+0x20` and `+0x30` were
**read out of `.data`**, not inferred.

**Reader and writer were read separately and agree**, which is what raises the bit layout above an
inference: the queries take the word apart (`and 0x3FF`, `shr 0xa`) and the mutator builds it
(`shl r8w, 0xa`, `or r8w, cx`). **One claim was corrected this way**: `+0x20` was first recorded as a
per-item byte array from the packed handler alone, and the bitset handler addresses the same pointer
as bits — so the element depends on the class's handler and the field cannot be typed once.

**Claim table added 2026-09-12 (`OPUS-INVQUERY-ISOLATED`).** The prose above states the method and is
kept; this enumerates the claims so `diff_inventory_query.py` can map to them. "Executed" means the
shipped bytes ran under Unicorn at their real virtual addresses against the reconstruction — and only
for the **three read entry points**~~, which is why so many rows below are not exercised~~ *(answered: see §13's supersession of 2026-09-26 — the ±1 entry, the query entry and all four storage handlers have since run as native replay, 16 / 16; 2026-10-02, OPUS)*.

| claim | evidence | tier | confidence |
|---|---|---|---|
| an encoded id is a class in the top nibble and a twelve-bit index | `shr` by 12 at `00309443`, `002FD8D3`, `002FD973` in all three read bodies; `and 0xFFF` at `002FD8E6`/`002FD986` in the two query bodies — the class reader `00309440` extracts only the nibble and applies no index mask. Executed at class 0x0E and 0x0F and at index 0 and 0xFFF | 1 (isolated original-code) | PROVEN |
| the descriptor table is at 01EEBCC0 with 0x58 bytes per row | the rip-relative base and the `imul 0x58` in each body. Executed across sixteen planted rows, where a wrong stride reads a neighbour | 1 (isolated original-code) | PROVEN |
| the class reader returns the dword at +0x38 and rejects a class above 0x0E | `00309449` then `0030945A or eax, -1`. Executed on both sides of the bound | 1 (isolated original-code) | PROVEN |
| neither query bounds the class or the index | no compare stands between `shr 12` and the table index in `002FD8D0` or `002FD970`. Executed at class 0x0F, where the class reader returns −1 and both queries answer from row 15 | 1 (isolated original-code) | PROVEN |
| the packed word is ten bits of total and six of reserved, and kind 0 is their difference | `002FD952 and ecx, 0x3FF` · `002FD957 shr eax, 0xA` · `002FD95B sub ecx, eax`. Executed on words planted to make all three answers distinct, **including words where the difference is negative**. The contract first recorded kind 0 as the whole word; the differential run corrected it | 1 (isolated original-code) | PROVEN |
| kind 3 of the packed query reads the byte array at +0x20 | `002FD906`. Executed against a byte array whose values differ from the word array at the same index | 1 (isolated original-code) | PROVEN |
| the bitset is a uint16 array at +0x08 for kinds 0 and 1, a byte array at +0x20 for kind 3 and at +0x30 for kind 4 | `002FDA2F`, `002FD9F2`, `002FD9B4`. Executed at indices crossing both a byte and a word boundary, so the two shapes disagree | 1 (isolated original-code) | PROVEN |
| kind 2 and every unhandled kind answer 0, and so does a NULL array pointer | `002FD903` and `002FDA2C`, and the null test ahead of each dereference. Executed for every kind against each of the three pointers nulled in turn | 1 (isolated original-code) | PROVEN |
| the byte-bitset paths carry a signed-division correction the 0xFFF mask makes unreachable | `cdq` / `and edx, 7` / add / `sar 3` at `002FD9C4`–`002FD9D1` and `002FD9FE`–`002FDA0B` on both byte paths and on neither word path. Executed, and **mutation testing confirms the unreachability**: the three mutants of the correction (`>> 31` → `>> 32`, `& 7` → `& 8`, `>>` → `<<`) compile byte-identical, which is what an unreachable branch looks like from the outside | 1 (isolated original-code) | PROVEN |
| the index is rejected against +0x3C as a signed compare, so a class with itemCount 0 rejects every id | **raised from HIGH by falsification pass 1**: the mechanism is read whole at `00309F7B mov eax, [rdx+0x3c]` / `00309F7E **dec eax**` / `00309F80 cmp ecx, eax` / `00309F82 **jg**`. The `dec` is what makes it work — at `itemCount 0` the bound is `-1`, and `00309F75 and ecx, 0xfff` keeps the index non-negative, so **every id is rejected**. Still **not** in either query handler | 1 | PROVEN |
| +0x10 is an element count, not an item count, and is ceil(+0x3C / 16) for every bitset class | all fifteen rows' `+0x10` and `+0x3C` read out of `.data` | 1 (static) | PROVEN |
| the stored count is clamped to 99 in the writer, not in the field | `002FD204`–`002FD209`, in `002FD150`, ~~which this pilot does not execute~~ executed since by the 2026-09-26 replay, whose postcondition holds over 168 mutates *(answered: see §13; 2026-10-02, OPUS)* | 1 (static) | PROVEN |
| dispatch is per class through the handler pointer at +0x50, and **SEVEN** of the fifteen rows carry NULL | **CORRECTED 2026-09-12 by falsification pass 1 (§15a): the claim said four.** Re-read from `.data`, rows **5, 7, 9, 10, 11, 13 and 14** have `+0x50 == 0`; the other eight dispatch to `002FD8D0` (rows 0–2) or `002FD970` (rows 3, 4, 6, 8, 12) | 1 | PROVEN |
| **four rows declare items and still have no handler — 9, 10, 13 and 14** | **EXECUTED path, re-read 2026-09-12**: `+0x3C` is 512, 256, 128 and 4095 on those four while `+0x50` is NULL, so `00309F96 mov rax,[rdx+0x50]` / `test rax,rax` / `je 0x309FA9` returns the default for **every id in them**. The other three NULL rows (5, 7, 11) declare `itemCount 0` and reject on the bound first | 1 | PROVEN |
| all three storage pointers are NULL in the image and are bound at runtime | all fifteen rows' `+0x08`, `+0x20` and `+0x30` read out of `.data`. **Who binds them is §14's open question**; the differential fixture plants them | 1 (static) | PROVEN |
| any runtime observation | — see §13 | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS), ONE CLAIM REFUTED AND CORRECTED

### The refutation: seven NULL handlers, not four

§15 claimed *"four of the fifteen rows carry NULL"* at `PROVEN`. The descriptor table was re-read
out of `.data` at the base and stride the contract itself derives — `00309F67 lea rax, [rip →
01EEBCC0]` and `00309F63 imul rdx, rax, 0x58` — and **seven rows carry a NULL handler: 5, 7, 9, 10,
11, 13 and 14.**

**The four is a real set, and it is the interesting one**, which is very likely what was meant:

| rows | `+0x50` | `+0x3C` | what happens |
|---|---|---|---|
| 0, 1, 2 | `002FD8D0` | 64, 420, 512 | the packed-count handler |
| 3, 4, 6, 8, 12 | `002FD970` | 81, 24, 256, 512, 32 | the bitset handler |
| **9, 10, 13, 14** | **NULL** | **512, 256, 128, 4095** | **declare items and answer the default for every id** |
| 5, 7, 11 | NULL | 0 | reject on the bound before the handler is reached |

**Four rows declare items and have no handler** — reached at `00309F96 mov rax, [rdx+0x50]` /
`test rax, rax` / `je 0x309FA9`. The claim's number was right about a set and wrong about the
population, and the corrected row now says both.

### Claim 9 raised from HIGH, because the mechanism reads whole

```asm
00309F75  and  ecx, 0xfff              ; the index, masked to twelve bits - always non-negative
00309F7B  mov  eax, dword ptr [rdx + 0x3c]
00309F7E  dec  eax                      ; <- the bound is itemCount MINUS ONE
00309F80  cmp  ecx, eax
00309F82  jg   0x309fa9                 ; signed
```

**The `dec` is what makes the claim true.** At `itemCount 0` the bound is `-1`, and since the index
is masked non-negative, `jg` rejects **every** id. The signed compare matters only because the `dec`
can produce a negative bound — not because a negative index can ever arrive here.

### What else was checked and holds

`01EEBCC0` and the `0x58` stride are read straight from the addressing. The class nibble is rejected
above `0x0E` by `00309F45`–`00309F59` (`and ax, 0xF000` then `cmp ax, 0xE000 / ja`), and id `0xFFFF`
is refused first at `00309F3C`. **All forty-five storage pointers — `+0x08`, `+0x20` and `+0x30`
across all fifteen rows — are NULL in the image**, confirming that claim exactly. And `+0x10 ==
ceil(+0x3C / 16)` holds on every row that has the bitset handler: 81→6, 24→2, 256→16, 512→32, 32→2.

**Mechanical:** no body-size drift; banned-evidence sweep clean; all eight entries resolve —
`003008A0` with **25 callers** across four subsystems, which is why this table's correctness is not
a local matter.

## 16. Parity plan

Reproduce, hardest to notice first: the **`+0x10` ratio** (§3); the **99 clamp in the writer** rather
than in the field (§6); the ~~**`owned - reserved` availability**~~ **`owned - equipped` free count** *(corrected 2026-10-02, OPUS: §7)* of kind 0; the **silent zero** on a
NULL handler (§9); and ~~the **inert classes** — giving them working storage would make a~~
~~reimplementation more capable than the original in a way no test notices until something addresses one~~
~~of those 4,991 ids.~~ the **grant-expanding classes** 9, 10, 13 and 14: no storage and a query that answers 0, but a write through `+0x48` that grants gil or nested items — modelling them as inert breaks every bazaar purchase and reward bundle *(corrected 2026-10-02, OPUS: §10)*.

## 17. Related

- `12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md` — the encoding
- `12-Items-Equipment-Shops-License/using-an-item-is-an-action-that-costs-an-item.md` — the reserve
  and refund this storage records
- `_types/` — `ItemClassDescriptor`

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings are recorded in the registry, not here.*

- **CombatAction — CLIENT.** `BattleAction_PrepareExecutionResources` and `BattleAction_RefundReservedExecution…` move
  items through `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (`003008A0`) when an item action is reserved or
  refunded ([using an item is an action that costs an item](using-an-item-is-an-action-that-costs-an-item.md)).
- **CombatFormula — CLIENT.** `BattleFormula_ApplyTargetResult` grants stolen items through the same write.
- **Gameplay — CLIENT.** `00309440` (30 B) is called by `BattleEncodedId_IsValidForClass`. That is the case that maps an
  id and re-enters the switch
  ([the shared neighbours page](../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md)).
  `00309440` is also called by the 8,136-byte body that the licence functions reach.
- **CoreRuntimeScheduling — MECHANICAL.** `003008A0` reaches its tables through `ImageAddress_ResolveRuntimePointer`.
- **Movement — MECHANICAL.** `0046AB10` (the counted-record filler `0046A630` calls) is also called by
  Movement body `00469A50`. Shared-helper fan-in; it does not establish a Movement relationship to
  inventory storage.
- **Save_Load_Settings - CLIENT (1 edge).** `0030B6A0` is also called by bodies filed to save/load/settings: `00238A80` - shared machinery across the layer boundary, no shared ownership.

## SWE2-EC7-83 update (2026-09-20) - `0046A630` counted-record build measured

`0046A630` (85 B) is the stack-block builder the storage callers
run: a 0x38 block zeroes, `cx` (when not `0xFFFF`) and `edx` (when
non-zero) seed `+0x40`/`+0x44`, and `0046AB10(0x25 : 0x24 by
edx==1, &block)` fills it - both args false skips the call entirely.
Interior anchor `0046A67B` (the `0046AB10` call).
