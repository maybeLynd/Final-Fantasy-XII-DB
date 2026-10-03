---
contract: allocate actor records of four different sizes in one block and carve each one's interior by its sequence
category: 04-Actor-Entity
scope: family
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 04-Actor-Entity/battleunit-slot-pool-and-actor-class.md
entries: ["00267A20", "00266AD0", "00266530"]  # <- corrected 2026-10-02, OPUS - 00267A20 is an interior address of 002679F0 (section 7)
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 69 addresses cited - 5 data, 8 entry, 54 interior, 2 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-actor-pool-pass-1    # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the actor record pool and its region map

**`ActorStorageRecord` is not a uniform array element.** Records come in four interior layouts and
**six different sizes**, they are allocated together in one block, and every consumer reaches them
through a pointer table rather than by multiplying an index by a stride. A reconstruction that
declared `ActorStorageRecord record[n]` would be wrong about the memory and right about nothing.

## 1. Purpose

To state the per-sequence sizes, where they come from, and the two tables that carry them — because
per-kind sizes are exactly the thing a layout database exists to preserve, and this one is authored
data in `.data`, not a constant in the code.

## 2. Interface

| | |
|---|---|
| allocate the pool | `00267A20` (inside `ActorStorage_AllocateAndInitializeRecords`) |
| carve one record | `00266AD0`, the region map |
| initialise one record | `00266530` `ActorStorage_InitializeRecord`, which calls the region map |

## 3. Types

**The per-sequence descriptor table at `0x01E0C328`, four bytes per sequence, eight sequences:**

| | |
|---|---|
| `+0x00` `u8` | the **layout class**, `0..3` — which of the region map's four arms carves this record |
| `+0x01` `u8` | the **sub flag**, `0` or `1` — selects `0xC8` or `0xA0` in the region map |
| `+0x02` `u16` | the **record size** |

Read out of `.data`, the eight entries are:

| seq | layout | sub | size |
|---|---|---|---|
| 0 | 0 | 0 | `0x328` |
| 1 | 1 | 0 | `0x3A8` |
| 2 | 1 | 1 | `0x330` |
| 3 | 2 | 0 | `0x348` |
| 4 | 2 | 1 | `0x2D0` |
| 5 | 3 | 0 | `0x6E0` |
| 6 | 3 | 0 | `0x6E0` |
| 7 | 3 | 1 | `0x668` |

**The layout column reproduces the region map's jump table exactly** — `00266BA4` sends sequences
0 / 1,2 / 3,4 / 5,6,7 to `00266AFB` / `00266B15` / `00266B36` / `00266B54`, and the table's `+0x00`
column is `0 / 1,1 / 2,2 / 3,3,3`. Two independent structures agreeing is what makes this a
descriptor table rather than three unrelated bytes.

**`0x6E0` is the LARGEST size, not the stride.** The store declares `ActorStorageRecord` at `0x6E0`,
which is correct as a maximum extent and is what sequences 5 and 6 use.

## 4. Preconditions · postconditions · invariants

**Invariant: a record is always reached through the pointer table, never by stride.** The allocator
writes `pool + 8 + index*8` (`00267AF5`) and `ActorStorage_InitializeRecord` reads exactly that
(`0026656A`, `mov rbx, qword ptr [rdx + r10*8 + 8]`). Variable sizes force this, and it is the single
most important structural fact in this contract.

**Postcondition of allocation:** one block holds a header, then every record, 16-byte aligned, with
a pointer to each at `pool + 8 + i*8`; the per-layout-class counts are tallied at `+0x1D0 + class*2`.

## 5. State

The descriptor table is authored and never written. The pool is allocated once and zeroed.

## 6. Relationships

- **`00266AD0` is the region map**, and the interior pointers it plants — `+0xA0`, `+0xA8`, `+0xB8`,
  `+0xC0` — are already declared in the store as interior pointers. This contract explains *why*
  they differ per record: they are set by whichever of the four arms the sequence selects.
- **`MovementContext` at `+0x120` and `SecondaryContext` at `+0x350`** are the regions those
  pointers address on the arms that plant them; on other arms `+0xB8` or `+0xC0` is set to NULL.

## 7. State transitions

**Allocation**, `ActorStorage_AllocateAndInitializeRecords` `002679F0` (436 B) — **`00267A20`, which this section used to name here, is an interior address of that body, not a function**:

```
total = 0
for seq in 0 .. sequenceCount-1:                     00267A41
    size  = u16 [01E0C32A + seq*4]                   the per-sequence size
    count = u16 [countTable + seq*2]                 an authored per-sequence count
    total += ((size + 15) >> 4) * count << 4         00267A50-00267A5C: ROUND UP TO 16, then multiply
total += 2 * roundUp16(8*definitionValueTotal + 8)   00267A65-00267A73
block = allocate(total)                              00267A79
memset(block, 0, total)                              00267A8B
```

**Where the inputs come from, and both were already in the store.** `r12 = *(rcx)` at `002679F0` is
`ActorManagerSlot +0x00` `theBoundDefinitionPayload`, so **the per-sequence counts are authored
per-area data** and the count table is that payload's own, at its `+0x14` offset. `r11d = [rcx+0x20]`
at `00267A11` is `ActorManagerSlot +0x20` `definitionValueTotal` — declared as *"the sum of every u16
in the definition payload's counted section, computed at bind"* — and the header is `2 ×
roundUp16(8 × that + 8)`, which is a pointer table of eight bytes per record and a second table of
the same size. `ActorManagerSlot +0x08` `recordPool` is declared as the pointer to this very block.

then a second pass fills the pointer table and tallies counts:

```
for seq:
    class = u8 [01E0C328 + seq*4]                    00267AD0
    counts[class] += count                           00267AD4  (+0x1D0 + class*2)
    for each record of this sequence:
        pointerTable[i++] = cursor                   00267AF5
        cursor += roundUp16(size)
```

**Carving**, `00266AD0` (211 B), dispatching on `(record[+3] & 0x1F)` through the eight-entry jump table at
`00266BA4`:

| arm | `+0xB8` | `+0xC0` | `+0xA0` |
|---|---|---|---|
| `00266AFB` | `0` | `0` | `rec+0x120` |
| `00266B15` | `rec+0x120` | `0` | `rec+0x1A0` |
| `00266B36` | `rec+0x120` | `0` | `rec+0x140` |
| `00266B54` | `rec+0x120` | `rec+0x350` | `rec+0x4D8` |

and then, common to all four, `+0xA8 = +0xA0 + (subFlag ? 0xA0 : 0xC8)` (`00266B83`–`00266B9B`),
with the sub flag read from `01E0C329 + seq*4` — the same table's `+0x01` column.

**Every interior pointer is record-relative.** Nothing here allocates, and nothing points outside
the record.


## 7a. What execution measured — [`EXP-107`](../_experiments/EXP-107-record-pool-region-map-exec.md), folded in 2026-09-19 (OPUS)

`EXP-107` ran **the two shipped bodies themselves** — `002679F0` (436 B) and `00266AD0` (211 B) —
against fixtures, with the CRT `memset` thunk entry-intercepted and the indirect allocator at
`qword[mgr+0x88]` replaced by a stub returning a fixture pool: 27/27 functional cases and 26/26
mutants over four processes.

> **This is ISOLATED ORIGINAL-MACHINE-CODE EXECUTION, and it is its own evidence class.** It is not
> the live game and it is not static reading. It proves what these two bodies compute for the inputs
> given; it proves nothing about which inputs the game supplies. Every row below is labelled with
> what it therefore does and does not license. Each claim was additionally re-read from the bytes
> here before being written into this contract.

### What execution CONFIRMED, changing nothing

| claim | this contract already said it | execution |
|---|---|---|
| the dispatch is on the **group index**, `(record[+3] & 0x1F)` | §7, *"dispatching on `(record[+3] & 0x1F)`"* | the three high bits are the kind and do not reach the dispatch — `pk=0xE2` behaves as `pk=2`, `pk=0x65` as `pk=5` |
| **the sub-flag addend polarity** | §7, *"`+0xA8 = +0xA0 + (subFlag ? 0xA0 : 0xC8)`"* | `cmp byte,1 / mov eax,0xC8 / jne / mov eax,0xA0` at `00266B83`–`00266B93`: flag `1` takes the **smaller** `0xA0` |
| one shipped table, `01E0C328`, stride 4 | §7 reads `+0` as the class and `+2` as the size at `seq*4` | `lea r8, [01E0C328]` at `00267ABB` with `add r8, 4` per group; `00266AD0` reads the `+1` byte of the same record |

**`EXP-107`'s finding 2 is filed by its author as "inverted from the naive reading", and against
this contract it is a confirmation, not a correction: §7 already had the polarity right.** It is
recorded because an independent execution agreeing with a static reading is worth more than either
alone — and because the naive reading is the one a reconstructor will write by reflex.

### What execution ADDED

**The packed byte is built in two stores, and the first is dead** (`00267AFA`–`00267B13`):

```
00267AFA  movzx ecx, byte ptr [rdx + 3]
00267AFE  and   cl, 0xe0
00267B01  or    cl, r9b          ; r9b = i & 0x1F, the GROUP index
00267B04  mov   byte ptr [rdx + 3], cl      ; <- STORE 1, never read back
00267B07  and   cl, 0x1f
00267B0A  movzx eax, byte ptr [r8]          ; the kind, from TAB[i].kind
00267B0E  shl   al, 5
00267B11  or    cl, al
00267B13  mov   byte ptr [rdx + 3], cl      ; <- STORE 2 wins
```

**`record[+3] = (kind << 5) | (i & 0x1F)`.** Store 1 is overwritten in the same iteration by store 2
— the value survives in `cl`, the memory write does not — and the `and cl, 0xE0` feeding it is
discarded by the `and cl, 0x1F` three instructions later. *(`EXP-107` cites this `and` at `0267B00`;
it is at `00267AFE`, and `00267B00` is not an instruction boundary.)*

**The record count is written to `pool[0]` BEFORE the record loop** — `mov dword ptr [r14], eax` at
`00267AA5`, with the pointer table starting at `pool+8` (`mov qword ptr [r14 + rax*8 + 8], rdx`,
`00267AF5`).

> **A zero header offset makes record 0 overwrite the count.** The record cursor is `rdx = r14 +
> edi` (`00267A9F`–`00267AA2`); with `edi == 0` record 0 sits at `pool+0` and its `record[+3]` write
> lands on byte 3 of the count. `EXP-107` drives it: `count = 0xFFFFFFFE` collapses the header size
> to zero and `pool[0]` reads back `0x00FFFFFE`. **This is a consequence of the arithmetic, not an
> observed game state** — nothing here says a shipped descriptor can produce `edi == 0`.

**The kind tally for kinds 4–7 is dead.** `add word ptr [r15 + rax*2 + 0x1D0], cx` (`00267AD4`)
writes `mgr+0x1D0 + 2*kind`; the prefix loop that follows (`00267B3A`–`00267B61`, four iterations
from `r15+0x1D0` writing `[rax+8]`) overwrites `mgr+0x1D8`–`0x1DE`, which is exactly where kinds
4–7 land. **Only kinds ≥ 8 would survive, and the shipped table uses kinds 0–3 only** — so the dead
writes are unreachable with shipped data, and a reconstruction that implements the tally faithfully
and the prefix loop faithfully gets the same answer either way.

**The region map returns the `+0xA8` pointer** in `rax` (`00266B9B`–`00266BA2`), and the allocator
returns the pool (`mov rax, r14`, `00267B89`). On the `seq > 7` exit the region map returns the
masked group index itself — `and eax, 0x1F` at `00266AD9` zero-extends, so for the reachable range
that equals `EXP-107`'s *"`cdqe(seq)`"*.

**Group indices beyond 7 are legal inputs to the allocator.** The group loop is bounded by the
descriptor's own group count (`cmp r10d, r13d`, `00267B35`) and the table cursor advances `add r8, 4`
with **no bound against the table's eight entries**. `EXP-107` drives group 16 and observes both the
out-of-table read and the `i & 0x1F` packing.

> **So `01E0C328` is eight entries by data, not by construction.** A descriptor declaring more than
> eight groups reads past it, and the region map then takes its `seq > 7` exit for those records —
> they are allocated and packed but never carved. **Whether any shipped descriptor does this is not
> established here and is listed in §14.**

### What execution did NOT settle

**§15's `+0x064`–`+0x078` negative is untouched by `EXP-107`.** That claim is about which functions
access a span of `ActorStorageRecord`, and replaying these two bodies cannot reach it. It stands as
§14 already corrects it — the span is the script VM register file — and `EXP-107` neither supports
nor weakens the remainder.

Two mutants are excluded as provably equivalent rather than surviving, which is a statement about
the suite and not about the engine: the dead store above, and `&0x1F` versus `&0x0F` at the sub-flag
read, indistinguishable because only `seq <= 7` reaches it.

*(OPUS 2026-09-19, on `REQ-OPUS-RECORD-POOL-FINDINGS` from SWE2-ORACLE. Every finding re-read from
the bytes before adoption; two citation slips in the source experiment noted inline.)*


## 7b. The record constructor — [`EXP-112`](../_experiments/EXP-112-actor-record-init-exec.md), folded in 2026-09-19 (OPUS)

`ActorStorage_InitializeRecord` `00266530` (1,439 B) is the per-record initialiser the allocator
calls in its final loop (`00267B79`). `EXP-112` executed it; **the same evidence-class caveat as
§7a applies** — it proves what the body computes for the inputs planted, not which inputs the game
supplies, and §7b's limitations at the end are part of the finding rather than a disclaimer.

### The descriptor has TWO counts, and conflating them was the error

This is the correction `EXP-112` records, and it is worth stating as layout rather than as a fix:

| descriptor field | read | what it bounds |
|---|---|---|
| `+0x00` u16 | `movzx eax, word ptr [rsi]` — `002668DF`, `00266714` | **an entity/field count.** `>= 0xA` gates **only** boundary site 1 (`002668E7`); `>= 8` selects the entity stride, `0x30` against `0x20` (`0026671A`–`00266729`) |
| u16 at `+ s32 [desc+0x14]` | `movsxd rax, [r12+0x14]` then `movzx r13d, word ptr [rax + r12]` — `00267A20`–`00267A25` | **the group count**, the allocator's loop bound; the per-group counts follow it at stride 2 |
| s32 `+0x18` | `movsxd rcx, [rsi+0x18]` — `00266710` | the offset to the entity array the stride above indexes |

**`w[desc+0]` is not the group count.** The two live at different offsets, bound different loops,
and are compared against different constants. Nothing downstream changes, because the allocator
always used the second and the constructor always used the first — but a reconstruction that reads
one descriptor field and uses it for both gets the wrong entity stride *and* the wrong group count
from the same mistake.

### The subflag index is the GROUP, here too

```
0026656F  movzx eax, byte ptr [rbx + 3]
00266577  and   eax, 0x1f                                  ; the GROUP index
00266588  movzx edx, byte ptr [r11 + rax*4 + 0x1cec329]    ; 01E0C329 + group*4
00266591  cmp   edx, 1
00266596  lea   r15d, [r13 + 6]                            ; sub-flagged: r15 = 6
0026659A  mov   eax, 0xa
0026659F  sub   edx, 1
002665A2  je    0x2665a6                                   ; sub-flagged: keep ebp
002665A4  mov   ebp, eax                                   ; otherwise ebp = 0xA
```

So the constructor's `& 0x1F` **bounds the subflag-table index only** — `00266AD0` and the kind
init re-read `record[+3]` and mask again for themselves — and sub-flagged groups take the smaller
`r15 = 6` / `ebp = 8` init, matching §7a's *"sub-flagged groups get the smaller `+0xA8`"*.

> **A terminology correction to the experiment, because this contract's §7a turns on it.**
> `EXP-112` finding 8 reads *"subflag==1 **kinds** are exactly {2,4,7}"*. They are **groups**. The
> index is `record[+3] & 0x1F`, which §7a establishes is the group and explicitly not the kind —
> the kind lives in the three high bits and never reaches this table. The set `{2,4,7}` is right;
> the word is not, and it is the one word §7a exists to fix.

### The rest of what execution measured

**The literal-word arms are unreachable.** `rep stosw` with `ecx = 0x12` writes `0xFFFF` over
`+0xC8`–`+0xEB` at `002668B0`, before any site reads that span, so every `w[+0xE6/0xDA/0xCA/0xCC/
0xDC]` a later site tests is always `0xFFFF` and the `movzx` literal arm never runs **under this
constructor**.

**The link write-in is unconditional; the swap-out is dead.** `b[+0x12]` is preset to `0xFF`, so
the old-record eviction never fires, while `q[0209A1F0 + link*8] = record` runs for every link
`0..0x7F` (`00266760`, `0026677C`). *That table is reached image-base-relatively —
`[r11 + rax*8 + 0x1F7A1F0]` with `r11 = 00120000` — so it is invisible to any sweep for `0209A1F0`
as a constant, which is the idiom `check_imagebase_relative_refs.py` exists for.*

**The registration cell** is `q[+0xF8] = 02F8F2A0` (`002666B4`) with `d[02F8F2A0] = 0`; the cell is
BSS and stays zeroed. **The A8 clear stride is `0x28`** over `b[+0x88]` slots. **The cls60 "call
sites" are flag operations** — `or`/`and` on `d[+0x1C]`, where site 6's success path clears the bit
site 5 set.

### What is NOT established, and is load-bearing

**Two scripted boundaries are unreachable from this entry** — `00268EA0` (`b[+0xB]&8` is masked off
earlier) and `003DBDC0` (`b[+0x63] == 0` skips the queue walk before its call site). **"Unreachable
from this constructor" is not "dead":** another caller may reach both, and `EXP-112` did not look.

**`q[01F83530]` was planted zero, making the pointer resolve an identity.** A non-zero live base
offsets every site compare and argument read uniformly, so the site *arithmetic* is measured and
the site *targets* are not. **`b[+0x63]` is always 0 under this constructor**, so the queue walk
body is executed only to its early exit — the walk itself remains unexecuted and is not described
here.

*(OPUS 2026-09-19, on `REQ-OPUS-ACTOR-RECORD-INIT-FINDINGS` from SWE2-ORACLE. Each finding re-read
from the bytes; the descriptor's two counts stated as layout rather than as a correction, and one
terminology slip corrected against §7a.)*

## 7c. Removal order, the release gate's two callers, and the ordinal / row / preset bindings (OPUS, 2026-10-02)

Incorporated from FABLE's independent reviews of three ASTRA packets, all ACCEPT-WITH-NARROWING:
[`notification-retirement-order`](../_index/candidates/fable-review-astra-notification-retirement-order-1002/),
[`request-cancel-notification`](../_index/candidates/fable-review-astra-request-cancel-notification-1002/) and
[`actor-directory-kind-proof`](../_index/candidates/fable-review-astra-actor-directory-kind-proof-1002/). OPUS re-read
the removal, the index leaf and the notification's refusals at the bytes on 2026-10-02. The release gate's mode-4
caller and the directory bindings stand on FABLE's review evidence (`rv_actordir.py`, 69 / 69 PASS).

**Removal (`003DB2A0`).**
- Index `0xFF` returns a constant 1 and does nothing else.
- A removed index that is not the list head does not walk the list. Every pass hands the removed index itself to
  `003DB550` (the record page's removal table states the three outcomes).
- The mode-3 end notification through `003DC0D0` is attempted **before** the removed index is relinked onto the free
  list (`003DB650`) and published at `+0x60`. Its result is discarded.
- The removal returns entry `+0x12` bit 0.

**The notification's refusals (`003DBCF0`).** The record `003DC0D0` builds carries function id 0 at `+4`.
- `003DBCF0` checks that id against the count at `[actor+0x48]` first: a zero count returns 3.
- It then checks the free head `actor+0x60`: `0xFF` returns 2.
- Neither refusal makes a call or writes the object.

**The release gate's second caller.** The gate is reached from RET's removal and from `003DB420` mode 4 (the
`freqcancel` verbs).
- **Range.** Channels run from `byte actor+0x88 - 1` down to `max(0, signed edx)`. Both compares are signed 64-bit.
  Each channel is gated by the entry snapshot of `word actor+6`, at bit (channel mod 32).
- **Selection.** The state filter `r14d` = (`r8d` != 4 ? `r8d` : 0). The recycler takes the first nonzero
  `byte entry+0x11`, following each entry's `+0` link, with the walk bounded by `byte actor+0x89`. It takes at most
  one entry per channel per call.
- **Removal.** It completes only when the selected index is the head of the list named by `entry+2`, or by
  `actor+0x61` when `+0x10` is 4.
- **Return.** EAX 1 on every normal path.

**Ordinal, row and preset.**
- The allocator `002679F0` publishes `pool[1 + ordinal]` row by row. Ordinal i is in row k exactly when
  sum(counts[:k]) <= i < sum(counts[:k+1]). The counts are the u16 entries after the group count at descriptor +
  s32 `[desc+0x14]`.
- Nothing bounds the published ordinals by N = manager `+0x20`. N covering sum(counts) is a precondition.
- The initializer `00266530` binds record `+0x40` = desc + s32 `[desc+0x18]` + 4 + 48*i (32*i when WORD `[desc+0]` < 8).
- The preset leaf `00266BD0` switches on the GROUP (record `+3` & 0x1F), not on the kind:
  - groups 5 and 6 store `0x00030004` (group 5 also sets `+0x14` bit 7);
  - group 7 stores `0x00034C85` and sets `+0x14` bit 7;
  - group 0 stores 0, groups 1-2 store `0x38`, groups 3-4 store `0x40`.
- The initializer clears `+0x0B` bit 3 before its two `00268EA0` call sites. It therefore never files talkhold /
  talkterm itself unless a callee sets that bit.
- The directory WORD `+4` (scriptType) is read nowhere on this path.

**Limits kept.** All of this is static and conditional. Natural reachability of the cancel path and the end
notification's timing stay open where the register rows OV-10 and OV-16 leave them.

## 8. Script · resource · event interactions

The sizes and layout classes are authored data in `.data`; the per-sequence counts come from a table
the allocator is handed. Nothing in this family loads either.

## 9. Determinism

Fully deterministic given the two tables.

## 10. Failure paths and edge conditions

- **The region map has no default arm.** `(record[+3] & 0x1F)` above 7 is rejected by
  `cmp eax, 7` / `ja` at `00266ADC`, which returns with **no interior pointer set at all** — leaving
  `+0xA0`, `+0xA8`, `+0xB8`, `+0xC0` at whatever they held, which after the pool memset is NULL.
- **Sequences 5 and 6 are identical** in all three columns. Nothing here distinguishes them; the
  difference, if any, is in the counts or in what occupies them.
- The allocation has no failure path read here: the result of the allocator call is used without a
  null test at `00267A85`.

## 11. Observable behaviour

Not established. What would be observable: the pool's total size, which §7's formula predicts
exactly from the two tables — one read of the allocation size against the computed sum would confirm
the whole of §7 at once.

## 12. Reproduction formula

```c
/* desc[seq] = { u8 layoutClass; u8 subFlag; u16 size; }   at 0x01E0C328 */

size_t total = header_size;
for (int s = 0; s < nseq; s++)
    total += ((desc[s].size + 15) & ~15u) * count[s];

char *cursor = block + header_size;
for (int s = 0, i = 0; s < nseq; s++) {
    counts[desc[s].layoutClass] += count[s];
    for (int k = 0; k < count[s]; k++, i++) {
        pointerTable[i] = cursor;
        cursor += (desc[s].size + 15) & ~15u;
    }
}
```

## 13. Runtime validation

**The REGION MAP stands on TWO tiers. It was executed 2026-09-12 as the thirtieth differential
pilot (`OPUS-ACTORPOOL-ISOLATED`) — evidence class: isolated original-code — and it was then
**observed live** in [`EXP-026`](../_experiments/EXP-026-actor-region-live.md): method C, read-only
process observation, two zone states, 40 samples each. Neither tier covers everything, and the
limit is the same for both: the pool allocation and the record initialiser were exercised by
NEITHER, and nothing below claims otherwise.**

<!-- `observed live` above must stay on ONE line: check_gate26's LIVE_RE carries a literal space,
     so a markdown wrap between the two words silences a true live claim. That is the same defect
     class as the EXP-061 pass-6 false positive FABLE reviewed on 2026-09-16, where a wrapped
     "is not" hid a refusal from a line-based classifier. Re-wrapping this paragraph is a
     behaviour change, not formatting. -->

<!-- The limit sentence is also deliberately NOT worded "has not been observed in the running
     game": that phrase is check_gate26's LIVE_DENIED_RE, which is tested BEFORE LIVE_RE, so
     stating the limitation in those words would have forced the section back to ISOLATED while
     every word of it stayed true. -->


`Reconstruction/Tests/Differential/diff_actor_pool.py` runs `00266AD0` as shipped bytes under
Unicorn at its real virtual address — including its own compiler jump table at `00266BA4` and the
descriptor table at `01E0C328` — against `Reconstruction/Game/Actor/actor_pool.c`, built by MSVC at
`/W4 /O2`. **There is no oracle and no stub**: the function calls nothing.

    diff_actor_pool  : 218 compared lines, 0 mismatches, 104 region images,
                       20 calls that left a pointer UNTOUCHED
    negative controls: eight - an out-of-range sequence zeroing the pointers (20 lines); the
                       sequence byte taken without its mask (16); arms 1 and 2 merged (16); the
                       sub flag tested for non-zero (24); the descriptor's layout byte read where
                       its sub byte belongs (35); arm 3's +0xC0 given the cursor (29); the jump
                       table paired one step off (36); the carve started at 0x100 (84)
    mutation campaign: 35 mutants, 32 KILLED, 1 SURVIVED, 2 NO_BUILD, inputs stable and hashes re-checked

**The two tables were decoded from the image rather than cited.** The jump table at `00266BA4`
holds eight RVAs over four arm bodies — `0 / 1,2 / 3,4 / 5,6,7` — and the descriptor table's layout
column reads `0 / 1,1 / 2,2 / 3,3,3`. §3 says two independent structures agreeing is what makes the
descriptor a descriptor; **both were read out and they do agree**.

**One thing the run makes explicit that §7 left implicit: the out-of-range path writes NOTHING.**
`00266ADF` is an unsigned `ja` over the masked sequence, and a record whose sequence exceeds 7 keeps
whatever its four region pointers already held — not zeros, not defaults. The fixture poisons all
four before every call, so "left alone" is a different observation from "written with zero", and 20
of the suite's calls come back carrying the poison. A reconstruction that zeroed them instead
differs on exactly those 20 lines.

**And one that sharpens a claim: the sub flag is compared against 1 EXACTLY** (`00266B83
cmp byte, 1`). A value of 2, or 0xFF, takes the same arm as 0. A reconstruction testing it for
non-zero differs on 24 lines.

**What this run does not establish.**

- ~~**Nothing here has been observed in a running game.**~~ *(answered: the region map was observed live afterwards in `EXP-026`, §13's opening; 2026-10-02, OPUS)* The check below still stands.
- **The pool allocation ~~`00267A20`~~ `002679F0` *(answered: §7 — `00267A20` is an interior address of it; 2026-10-02, OPUS)* and the record initialiser `00266530` are out of scope.** The
  first is the allocator and the second is 0x300+ bytes over six callees; §15's rows about sizes,
  rounding, counts and the header are **unchanged by this run** and remain static.
- The region map is one pure function. That it writes the right four pointers says nothing about
  **who calls it, when, or whether the regions it names are used as this contract reads them.**

**Still wanted from a running game**, unchanged: read the pool's allocation size. §7 predicts it
exactly from the descriptor table and the bound payload's counts, so a single number confirms the
sizes, the rounding, the counts and the header together — or falsifies the reading in one step.

**CORRECTED 2026-09-11.** An earlier revision called this check decisive for the whole of §7. It is
decisive **for the area observed**. The counts come from the bound definition payload, which is
per-area authored data, so the pool size is not a constant and one reading does not generalise to
every area. It is still the cheapest possible confirmation of the arithmetic, which is why it stays
first.

Requested from ASTRA; not claimed by me.

### The first live observation — [`EXP-026`](../_experiments/EXP-026-actor-region-live.md), linked 2026-09-14 (OPUS)

**Method C, ordinary UI input and read-only process observation. This does not change the evidence-class statement above for the pool allocation or the record initialiser, which were not observed.** Two zone states were sampled 40 times each — Stepping and Rabanastre Eastgate — with the actor anchored independently by active `BattleUnit` slot 0 and by membership of manager 0's pointer table:

| observation | Stepping | Eastgate |
|---|---:|---:|
| sequence (`byte3 & 31`) | 5 | 7 |
| captured record extent | `0x6E0` | `0x668` |
| `A0` − actor base | `0x4D8` | `0x4D8` |
| `A8` − actor base | `0x5A0` | `0x578` |
| `B8` − actor base | `0x120` | `0x120` |
| `C0` − actor base | `0x350` | `0x350` |

All 40 samples in each capture match their column, so the per-sequence extents and array counts §3 decodes from the descriptor table now have a live positive control in two states — and the two states differ in exactly the arm the map selects on, which is what makes it a control rather than a single reading repeated.

**What it does NOT establish, in the record's own terms.** The actor address and table ordinal changed across the transition; that identifies different storage selections and **not** the freeing of the old record or lifetime continuity — the capture never reads the old address after zoning. The four bytes at `+60..63` were unchanged in both states, which does **not** demonstrate byte independence, free-list mutation, allocation or recycling. The wait cursor sat inside its array in every sample, and no drive-loop trace establishes its intermediate values or its scheduling. **No allocator or destructor claim is promoted by this.** Static writer evidence is still what §7 and §10 owe.

## 14. Unresolved

- What distinguishes sequences 5 and 6, whose descriptors are identical.
- ~~The header size~~ — **resolved**: `2 × roundUp16(8 × definitionValueTotal + 8)`, two tables of
  eight bytes per record. What the **second** table holds is still open; the first is the record
  pointer table.
- ~~The per-sequence count table's location~~ — **resolved**: inside the bound definition payload
  (`ActorManagerSlot +0x00`) at its `+0x14` offset. Its own layout is the payload's, not this
  family's.
- Why layout class 0 leaves both `+0xB8` and `+0xC0` NULL.
- **Whether any shipped descriptor declares more than eight groups.** `EXP-107` shows the allocator accepts them and reads past `01E0C328`, and that the region map then never carves those records (§7a). The bound is the descriptor's group count, which is authored per area and has not been censused.
- ~~**`+0x064`–`+0x078` is probably permanently zero**~~ — **RESOLVED 2026-09-12,
  `OPUS-CONTRA-RECORDPOOL-VMREGS`. The span is the script VM's register file.** Four `int32` at
  `+0x64`–`+0x70` (`vmRegI0..I3`) and four `float` at `+0x74`–`+0x80` (`vmRegF0..F3`), written by
  opcode handlers `0x36`–`0x3D` and read by `0x3E`–`0x45`, with the dispatch table verified at
  `00261DF8` rather than inferred from address order. The rows are in `_types/fields.tsv`.

  **§15's ruling on those accesses is wrong, and this is the correction.** It ruled out "five
  consecutive dwords on `r15`" in `WorldActorScriptVM_InterpretBytecode` as sitting on other
  objects. **`r15` IS the record**: the interpreter `0025E4C0` sets `r15 = rdx` at `0025E4D5`; it has
  exactly **one** direct caller, `0025E0D3`, which sets `rdx = rdi` at `0025E0CD`; and twenty-six
  bytes earlier that same `rdi` goes to `003DB2A0` as `rcx`, whose prologue takes `rbx = rcx` and
  whose body writes the record's own `+0x60` free-list head. Corroboration: the interpreter's first
  act is `movzx edx, byte [rdx+0x14]`, and `+0x14` is the flag byte the channel selector `003DB6E0`
  sets and clears.

  **What survives is the part that was measured, and it is worth separating from the part that was
  inferred.** The construction-path negative below is **correct**: the allocator, the initialiser
  and the region map genuinely do not write the span — which is precisely why a sweep anchored on
  construction found nothing, and why the absence looked like reservation. *A negative over the
  wrong set of writers is not a negative; it is a statement about the set.* The span is written
  every time a script executes one of sixteen opcodes.

- **`+0x064`–`+0x078`, twenty bytes, is written by none of the three construction paths** — three
  named negatives rather than an absence of looking. `ActorStorage_AllocateAndInitializeRecords`
  allocates and zeroes; `ActorStorage_InitializeRecord`'s displacements through `rbx` step
  `0x58 → 0x88 → 0xA8 → 0xB8`, skipping the span entirely; and the region map `00266AD0` touches only
  `+0x20`, `+0x80`, `+0x188` on its source and `+0xA0`, `+0xA8`, `+0xB8`, `+0xC0`, `+0x120` on the
  record. **This is no longer an open question and the hypothesis it once carried is retired**
  (2026-09-12): the bullet above resolves the span as the script VM's register file, so a record's
  twenty bytes are zero only until a script executes one of sixteen opcodes on it. What stands here
  is the narrower fact the sweep actually measured — **construction does not write the span** — which
  is why an absence over the construction set looked like reservation. The old discriminator
  ("read those twenty bytes in any live record; all-zero supports reserved") is **withdrawn**: an
  all-zero reading now means only that the record's script has not run one of those opcodes yet, and
  `EH-3` no longer needs re-scoping to it.
  > *EH-3 answered 2026-09-12 (FABLE). **ADJUDICATED AND FOLDED BY OPUS 2026-09-13** — main finding accepted and re-verified, harmlessness conclusion refused; see below.* **The span
  > is declared, and it has a second writer the three construction paths never reach.** `_types/
  > fields.tsv` now places the VM register file at `+0x064`–`+0x083` (`vmRegI0`–`vmRegI3`,
  > `vmRegF0`–`vmRegF3`, OPUS rows of 2026-09-11), and `types_index.py --validate` reports **no gap**
  > between `+0x02C` and `+0x084`: the record's undeclared bytes are now twelve gaps totalling 34
  > (`+0x023`, `+0x02C`, `+0x084`, `+0x08A`, `+0x09C`, `+0x0B0`, `+0x0CA`, `+0x0DA`, `+0x0E0`, `+0x0E4`,
  > `+0x0F0`, `+0x11C`), so the row's "20-byte span worth a package" no longer exists. The
  > register-file reading is confirmed from the code: the interpreter keeps the file through its
  > second argument (`r15 = rdx`, `POPI0` at `00261624 mov [r15+0x64], eax`, `POPF0` at `00261668`),
  > and that argument is the record `ActorManager_RunFieldRuntimePass` walks at `02098E10 +
  > idx·0x288` (`0025D9EF`, `0025D9F6`) and hands down through `WorldActor_UpdateRuntimeAndScript
  > ExecutionState` (`0025E0D3`). **The second writer:** `ActorManager_BindLoadedDefinitionPayload`
  > (`0026C8C0`), reached from `ActorResource_OnDefinitionPayloadLoaded` (`0032F966`) with the
  > record index in `ecx`, computes the same record (`0026C8FE`–`0026C90E`) and, after planting the
  > declared `+0x48` / `+0x50` / `+0x58` pointers, stores **five more qwords over the register file**:
  > `+0x60` ← `&02099FF0` (`0026CB38`), `+0x68` ← payload + header `+0x20` (`tableOff20`), `+0x70`
  > ← payload + `+0x24` (`tableOff24`), `+0x78` ← payload + `+0x28` (`tableOff28`), `+0x80` ←
  > payload + `+0x2C` (`tableOff2C`) (`0026CB3C`–`0026CB6B`). A function-list-independent census
  > finds **no load** of `+0x60`, `+0x68`, `+0x70`, `+0x78` or `+0x80` as a qword through any record
  > route — the base table, the `0x288` stride, the accessors' return or the `[actor + 0xB8]`
  > pointer — in the binder's family or anywhere else, so the five copies are ~~**dead stores** that~~
  > ~~the register file overwrites as soon as a script pops a register.~~ *(answered: see "CORRECTED 2026-09-20 (SWE2-CONTRACT)" below — the stores land on the slot, and the interpreter loads `+0x68` / `+0x70` at `00261855` / `0026187D`; 2026-10-02, OPUS)* What the three construction
  > paths missed is therefore a bind-time writer of a region that is a union in time: sub-table
  > pointers at load, VM registers thereafter.

  **ACCEPTED IN ITS MAIN FINDING, AND ITS HARMLESSNESS CONCLUSION REFUSED — OPUS, 2026-09-13.**
  The union-in-time reading is right and re-verified at the image: `0026C8FE lea rdi, [02098E10]`
  with `0026C907 imul r8, rbp, 0x288` and `0026C90E add rdi, r8` makes `rdi` **the record**, and the
  five stores are at `0026CB38`, `0026CB43`, `0026CB4E`, `0026CB59` and `0026CB6B`.

  **But the argument for "harmless" covers only the register file, and the FIRST of the five stores
  does not land inside it.** `mov qword ptr [rdi + 0x60], rax` writes **eight bytes at `+0x60`**, so
  it covers `+0x60`-`+0x67`: all of `+0x64` `vmRegI0`, and below it **four declared fields that are
  not VM registers at all** —

  | offset | field | live byte writers |
  |---|---|---|
  | `+0x060` | `entryFreeListHead` | `003DB3F9` `ActorResource_RemoveActiveEntry`, `003DBD7E` `ActorResource_AllocateAndSubmitEntry`, `003DC160` `ActorResource_UnlinkEntryAndMarkFree` |
  | `+0x061` | `detachedEntryListHead` | `003DB35E`, `003DB980` `ActorResource_InsertEntryFromDescriptor` |
  | `+0x062` | `selectedEntryIndex` | `003DB764` `ActorResource_SelectPendingEntryForExecution` |
  | `+0x063` | `entryListFlags` | `003DB3F5` `or byte ptr [rbx+0x63], 2`, and `003DB25A` / `003DB28E` `shr` |

  Those four hold the resource-entry list heads and are maintained by a live, named family. The
  binder writes the low half of `&02099FF0` over them. **"The register file overwrites the dead
  stores as soon as a script pops a register" cannot be the answer for these**, because nothing the
  script VM does touches `+0x60`-`+0x63`.

  > **CORRECTED 2026-09-20 (SWE2-CONTRACT): the overlap described above never happens.** The four
  > byte fields and `+0x64` `vmRegI0` are `ActorStorageRecord` fields; the store lands on an
  > `ActorManagerSlot`, whose `+0x60` is the 8-byte `groupPersistentBank` field — one field of
  > the slot's own layout, not a clobber of the record's. See the RESOLVED note below for the
  > full provenance chain.

  **What the entry on those lists points AT** (OPUS 2026-09-16, and this is a join onto published
  prior art rather than a fresh reading). `ActorResourceEntry +0x06` was UNRESOLVED with the note
  that the remover treats a value other than `0x8000` as "something that needs releasing" — right
  about the branch, silent about the value. The value is an **actor ordinal**. `003DB366`–`003DB37F`
  gates on `cmp word [rdi+6], 0x8000` *and* `byte [rdi+0x10] == 3` before calling `003DC0D0`, which
  passes `word [entry+6]` as argument 2 and `dword [entry+8]` as argument 1 to the resolver
  `003587C0`. That resolver is `movsxd rbx, edx` / `00263FF0` / `mov rcx, [rax+8]` / reject
  negative / reject `>= [rcx]` / `mov rax, [rcx + rbx*8 + 8]`, and `00263FF0` is
  `movsxd rax, ecx; imul rax, 0x288; add 02098E10` — the **actor-manager slot array** already
  documented at [the world tick](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)
  (stride `0x288`) and already known as a *(manager index, ordinal)* resolver at
  [how a character turns](../06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md).
  So `(entry+0x08, entry+0x06)` is the same actor-reference pair `Movement_SetSteeringTargetActorRef`
  (`0026ADF0`) stores as `(+0x04, +0x00)`, and the house name for this half is already `ordinal`
  (`ActorWaitSlot +0x24 targetOrdinal`). **`0x8000` is the "no actor" sentinel**: the free-list build
  seeds the dword at `+0x04` with `0x80000000`, which is `resourceId` 0 and ordinal `0x8000`.
  `ActorResourceEntry` completes at 8 / 8.

  > **DECLARED 2026-09-17 (SWE2-STRUCT, `OPUS-REQ-STRUCT-ACTOR-RESOURCE-ENTRY-UNDECLARED-FIELDS`).**
  > The release path's three reads are now rows: **`+0x03` `requesterWaitSlot`** (byte — the
  > requester's `currentWaitSlot`, record `+0x11`), **`+0x08` `requesterManagerIndex`** (dword —
  > the requester's own manager index, `dword[r13+0x28]` at `002689D9`/`002689DF`), and
  > **`+0x0C` `requesterReturnPc`** (dword — the requester's pc minus its bytecode base,
  > `0026898F`/`002689BC`). The release (`003DC0D0`) resolves `(+0x08, +0x06)` back to the
  > **requesting** actor and files request `0x402` on it, carrying the wait slot at
  > descriptor `+2`, the manager index at `+0xC`, and the return pc at `+0x10`. The entry's
  > only undeclared byte is now the `+0x13` tail. One correction this settles: the
  > script-binds page's descriptor table had `+0xC` carrying the pc offset — the binary puts
  > the pc offset at descriptor `+0x10` (→ entry `+0x0C`) and the manager index at `+0xC`
  > (→ entry `+0x08`); the table is corrected there.

  > **RESOLVED — the ordering question dissolves on object identity (SWE2-CONTRACT, 2026-09-20).**
  > The question as posed has no answer to give, because the premise is a type confusion: the
  > store does not land on the object that owns the lists at all.
  >
  > `rdi` in `ActorManager_BindLoadedDefinitionPayload` is an **`ActorManagerSlot`**, not an
  > `ActorStorageRecord`: `0026C8FE`/`0026C907`/`0026C90E` compute `02098E10 + ebp·0x288` — the
  > same array `00263FF0` resolves and the same object this contract's own `ActorManagerSlot
  > +0x048` row already pins. The field map confirms it independently: every store in the body
  > lands on a *slot* field — `+0x00` `boundDefinitionPayload`, `+0x20` `definitionValueTotal`
  > (the summed `+0x14`-table words), `+0x28` `slotIndex`, `+0x48` `persistentPayloadBase`,
  > `+0x50` `localClassBase`, `+0x58` `fieldScratchBank`, `+0x88` `recordPoolAllocator`,
  > `+0x98` `localVariableResolver`, `+0xA0`/`+0xA8`/`+0xB0`/`+0xB8` nulled at `0026CC49`–
  > `0026CC5E`. On that object `+0x60` is **`groupPersistentBank`** — a PROVEN 8-byte field
  > holding the `02099FF0` bank pointer, installed by this very store and live under the
  > world-persistence pair (`_types/fields.tsv`). The `+0x60` store is not a clobber of four
  > byte fields; it is the legitimate install of the sixth qword of the slot's `+0x58`..`+0x80`
  > descriptor/bank block.
  >
  > The four byte fields the item worried about — `entryFreeListHead`, `detachedEntryListHead`,
  > `selectedEntryIndex`, `entryListFlags` — and `+0x64` `vmRegI0` live on the
  > **`ActorStorageRecord`**, a different object the binder never touches. The chain is fully
  > enumerable: `FUN_003db580` is the image's *only* `+0x60`/`+0x61` seed (`mov word [r10+0x60],
  > 0xFF00` at `003DB62F`), called exactly once, inside `ActorStorage_InitializeRecord`
  > (`002667D7`), on `rbx` = a packed-table record (`manager+0x1F0`, built by
  > `ActorStorage_AllocateAndInitializeRecords` at `00267AF5`). Every `ActorResource_*` list op
  > receives a *record* as `rcx`: `AllocateAndSubmitEntry` gets it from `003587C0` —
  > `slot+0x08` `recordPool`'s element — inside `ActorResource_StartEntryScriptExecution`, or
  > from `SubmitRequestDescriptor`'s record argument; `InsertEntryFromDescriptor` runs only
  > from `AllocateAndSubmitEntry`. The VM's `r15` is likewise a record: `0025DB2B`–`0025DB43`
  > passes the *slot* (`rcx=rbx`) to `00358940`, and the record it returns
  > (`word[payload+0x50]`-indexed `recordPool` element) becomes `rdx` into
  > `WorldActor_UpdateRuntimeAndScriptExecutionState` — the walked object is the slot, the
  > handed-down object is its `recordPool` element. That conflation — walked vs handed-down —
  > is what made the store look like it covered `vmRegI0`.
  >
  > **So there is no ordering to establish:** no entry-list state ever exists on the slot, so
  > the store cannot reach the lists no matter when it runs. The reconstruction guidance stands
  > but for the right reason — a reconstruction *must* perform the `+0x60` install
  > (`groupPersistentBank` is a live field), and must not mistake the slot's `+0x60` for the
  > record's `+0x60`. It also follows that the "dead stores overwritten by the register file"
  > reading above was built on the same conflation: the slot's `+0x68`/`+0x70`/`+0x78`/`+0x80`
  > are `payloadSectionC`/`payloadSectionD`/`variableDescriptorTable`/`payloadSectionF` — slot
  > fields, not register bytes; the register file `+0x64`..`+0x83` exists only on the record.

## 15. Evidence

**The `+0x064`–`+0x078` negative carries a positive control and a closed set, because a negative
without one is just a failed search.** The set swept was *closed*: every function containing an
address this store already cites for an `ActorStorageRecord` field — 48 functions, so membership is
proven rather than guessed. Inside it, 18 instructions access `+0x64`–`+0x77`, and **every one was
ruled out by binding its base register**: five consecutive dwords on `r15` and two qwords on `r13` in
`WorldActorScriptVM_InterpretBytecode` sit on other objects — **the `r15` half of this is WRONG and
is corrected in §14: `r15` is the record, and those five dwords are the VM register file. The `r13`
half is not re-examined here**; `0026CB43`/`0026CB4E` write through
`rdi`, which this store's own `ActorManagerSlot +0x048` row pins to an `ActorManagerSlot` by its
neighbouring store at `0026CAFD`; and `00265B0B`'s `rax` is the null-tested return of `00359B80`
(`00265AED`), not the record — the record in that function is `rbx`, which the same body reads at
`+0x3`, `+0x12`, `+0x1C`, `+0x30` and `+0x38`. **Positive control:** the identical sweep over the
identical set at the *declared* displacement `+0x60` returns 17 accesses, so the instrument does find
record-relative accesses when they exist.

**A discarded instrument, recorded so it is not rebuilt.** The first attempt anchored on any base
register that also carried a "characteristic" `ActorStorageRecord` displacement (`+0x30`, `+0x50`,
`+0x58`, `+0x60`, `+0x88`, `+0xA8`, `+0xB8`). Those offsets are generic: the top hits were
`vp8_get_frame` and `vp8_decode_frame`, the video decoder. It has no discriminating power and was
thrown away rather than filtered by hand.


Static, from the shipping image (`73461D08…`). The descriptor table was **read out of `.data`**, all
eight entries; the allocator and the region map were disassembled and read; and the layout column was
checked against the jump table at `00266BA4` decoded separately. The agreement between those two —
`0 / 1,1 / 2,2 / 3,3,3` in the table and the same grouping in the jump table — is the evidence that
the first byte is a layout class rather than an unrelated field.

**Claim table added 2026-09-12 (`OPUS-S15-CLAIM-TABLES-SIX`).** The prose above states the method
and the two instruments, one of which was discarded, and is kept. This enumerates the claims so a
pilot's `CONTRACT_MAP` can be derived from them rather than asserted. **Nothing here has been
executed** (§13), so no row claims more than static evidence. *(answered: §13 — executed 2026-09-12 as the region-map pilot and observed live in `EXP-026`; 2026-10-02, OPUS)*

| claim | evidence | tier | confidence |
|---|---|---|---|
| the descriptor table at 01E0C328 is four bytes per sequence for eight sequences | all thirty-two bytes read out of `.data`, and every field used by a decoded instruction | 1 (static) | PROVEN |
| the table's first byte is a layout class, not an unrelated field | its column `0 / 1,1 / 2,2 / 3,3,3` reproduces the region map's jump table at `00266BA4` exactly — two independent structures agreeing. **Both decoded from the image 2026-09-12** rather than cited. The run also shows the region map never reads that byte, only `+0x01`, so the agreement is corroboration and not causation | 1 (isolated original-code) | PROVEN |
| 0x6E0 is the largest record size and not a stride | sequences 5 and 6 use it; the other six sizes differ, and the pointer table exists because of that | 1 (static) | PROVEN |
| a record is always reached through the pointer table at pool + 8 + index × 8, never by stride | the allocator writes it at `00267AF5` and `ActorStorage_InitializeRecord` reads exactly that at `0026656A` | 1 (static) | PROVEN |
| each record size is rounded up to 16 before being multiplied by its count | `00267A50`–`00267A5C` | 1 (static) | PROVEN |
| the per-sequence counts are authored per-area data, not constants | `002679F0` takes `ActorManagerSlot +0x00`, the bound definition payload, and the count table is that payload's own at `+0x14` | 1 (static) | PROVEN |
| the header is two tables of roundUp16(8 × definitionValueTotal + 8) | `00267A65`–`00267A73`; the first table is the record pointer table and **what the second holds is open** (§14) | 1 (static) | HIGH |
| the pool tallies per-layout-class counts at +0x1D0 + class × 2 | `00267AD0`–`00267AD4` | 1 (static) | PROVEN |
| the region map's four arms write +0xB8, +0xC0 and +0xA0 as record-relative offsets, and an out-of-range sequence writes NOTHING | the four arms at `00266AFB`, `00266B15`, `00266B36`, `00266B54`. **Executed 2026-09-12**: every sequence 0-9 plus 0x1F, 0x20, 0x21, 0x27, 0x28, 0x80 and 0xFF, with all four pointers poisoned first so an untouched one is distinguishable from a zeroed one. A reconstruction that zeroed them on the out-of-range path differs on 20 lines | 1 (isolated original-code) | PROVEN |
| +0xA8 is +0xA0 plus 0xC8 or 0xA0, chosen by the descriptor's sub flag **compared against 1 exactly** | `00266B83`–`00266B9B` against `01E0C329 + seq × 4`. **Executed 2026-09-12** at sub values 0, 1, 2 and 0xFF for every sequence, each entry differing from its neighbours so a reconstruction reading the wrong row is visible. Testing the flag for non-zero differs on 24 lines | 1 (isolated original-code) | PROVEN |
| none of the three construction paths writes +0x64–0x78 | **re-established 2026-09-12 by falsification pass 1 (§15a), because the original closed set covered only TWO of the three paths.** Swept directly: `002679F0`, `00266530` and `00266AD0` have **zero** accesses in `+0x64`–`+0x77`, with 31, 152 and 20 register-based memory operands respectively as the control. **The span itself is the script VM's register file** (§14) — this claim is about construction only | 1 (static) | PROVEN |
| the binder's `+0x60` store installs `ActorManagerSlot` `groupPersistentBank` and cannot reach the record entry lists — the §14 ordering item dissolves on object identity, not sequencing | `rdi = 02098E10 + ebp·0x288` is the `ActorManagerSlot` (`0026C8FE`/`0026C907`/`0026C90E`, the `00263FF0` array); every store in the body lands on a declared slot field, and `+0x60` is the PROVEN `groupPersistentBank` install. The `+0x60`/`+0x61`/`+0x62`/`+0x63`/`+0x64` byte and register fields belong to `ActorStorageRecord`: `FUN_003db580` is the image's only `+0x60` seed (`003DB62F`, sole caller `002667D7`), every `ActorResource_*` op's `rcx` traces to a `slot+0x08` `recordPool` element (`00358940`/`003587C0`) or a `manager+0x1F0` packed record — never to a `02098E10` slot; the binder itself nulls slot `+0xA0`/`+0xA8`/`+0xB0`/`+0xB8` at `0026CC49`–`0026CC5E` | 1 (static) | PROVEN |
| nothing observed at runtime | — see §13 | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS), SURVIVED

### The finding: the closed set did not cover the claim's own scope

§15's negative ranges over **three** construction paths. Its evidence is a sweep over *"every
function containing an address this store already cites for an `ActorStorageRecord` field — 48
functions, so membership is proven rather than guessed"*.

**Re-derived from the store and the current census, that set is still exactly 48 — and
`002679F0 ActorStorage_AllocateAndInitializeRecords` is not in it.** It cannot be: the allocator
cites no `ActorStorageRecord` field, which is precisely why a set built that way is closed against
the *store* and not against the *claim*. **One of the three paths was never swept.**

**Swept directly, and the claim holds:**

| function | accesses at `+0x64`–`+0x77` | register-based memory operands, as a control |
|---|---:|---:|
| `002679F0` **the path that was missing** | **0** | 31 |
| `00266530` `ActorStorage_InitializeRecord` | **0** | 152 |
| `00266AD0` the region map | **0** | 20 |

The control matters: a sweep that found nothing in a function it could not read would look identical.
All three are read, and none touches the span **on any base register** — which is a stronger result
than the original, because it needs no register-binding argument at all.

### The two supporting counts are not reproducible from the document

§15 cites *"18 instructions access `+0x64`–`+0x77`"* and a positive control at `+0x60` *"returning 17
accesses"*. An independently written sweep over the identical 48 functions — any base register other
than `rsp`/`rbp`/`rip`, no index — returns **19** in the span, and **13** at exactly `+0x60` or **27**
across `+0x60`–`+0x63`. **None of those is 18 or 17.**

That is not evidence the document is wrong. It is evidence that **the surviving instrument's filter
is not written down**: the prose specifies the *discarded* instrument in detail and says only that
the survivor was "the identical sweep over the identical set". **A control nobody else can regenerate
is weaker than it looks**, and the direct sweep above is what now carries the claim.

### The rest of the pass

| claim | the killer | what the binary says |
|---|---|---|
| the region map's four arms write `+0xB8`, `+0xC0`, `+0xA0` | the §7 table's cells are wrong | **holds, every cell.** `00266AFB` zeroes both; `00266B15` and `00266B36` zero `+0xC0` and write `rec+0x120`; `00266B54` writes `rec+0x120` and `add rax, 0x230` → **`rec+0x350`**; `00266B79` writes `+0xA0` for all four |
| the sub flag is compared **against 1 exactly** | it is a truth test | **holds.** `00266B83 cmp byte [→01E0C329 + seq*4], 1` / `jne` → `0xC8`, else `0xA0`. The table base resolves through `r9 = 0x120000` |
| each record size is rounded up to 16 before the multiply | the rounding is after, or absent | **holds.** `00267A50 add ecx, 0xF` / `shr ecx, 4` / `imul ecx, eax` / `shl ecx, 4` |
| `00267A20` is a function entry | it is, and the census is missing it | **it is not, and the document already says so** — §2 marks it *"inside `ActorStorage_AllocateAndInitializeRecords`"*. The census is right. **But it sits in `entries:`**, which elsewhere holds function entry points, and a tool that resolves that list will not find it |

> **Cross-contract check, and it agrees.**
> [`CONTRACT-movement-body-pool`](../06-Movement-And-Navigation/CONTRACT-movement-body-pool.md)
> states that `+0xC0` is planted by **only one** of these four arms, so records of the other three
> layouts can never have a collision body. Read at the instructions, three arms write a literal `0`
> into `+0xC0` and the fourth writes `rec+0x350` — **the two contracts say the same thing**, and the
> body pool's precondition test at `002E3506`–`002E3513` is what turns it into behaviour.

> **Still unexecuted for the paths this pass touched.** Three of §15's claims carry isolated
> original-code evidence; the negative and the arithmetic do not, and this pass did not run them —
> it read instructions. `crossref_clean` stays **false**: `audit_crossrefs.py` reports three
> `UNACCOUNTED NEIGHBOUR` findings for this document, and dispositioning them was not part of it.

## 16. Parity plan

Reproduce: the variable record sizes from the table rather than a compiled-in constant, the round-up
to 16 **before** multiplying by the count, the pointer table, and the region map's four arms with the
sub-flag selection. A reconstruction using a uniform `0x6E0` stride would allocate 2.3 times the
memory and place every record at the wrong address.

## 17. Related

- `04-Actor-Entity/battleunit-slot-pool-and-actor-class.md`
- `_types` — `ActorStorageRecord`, `MovementContext`, `SecondaryContext`, `ActorResourceEntry`,
  `ActorWaitSlot`

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Party — SERVICE.** `0026C8C0` on this page calls `PartyControl_SetMovementSuppressionBit`, owned by that layer. What it reaches is a 76-byte bit setter over the mask at `[022C8000]`: it sets or clears bit `cl` according to its first argument; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — SERVICE (SWE2-CONTRACT 2026-09-15, 8 edges).** `0026C8C0` — the bind-loaded-definition-payload body
this contract cites — applies the render-fade configuration family:
`CharacterRenderSystem_SetFadeWidth`/`SetFadeStartDistance` plus the six `CharacterRenderConfig_*`
default/built-in getters and setters. Pool binding publishes fade parameters to the render layer —
a real configuration crossing, small and named.

**Roster-pass neighbours (SWE2-EC7, edges from `edges.tsv`, MECHANICAL).** The `00268690`/
`00268530` four-slot roster passes this page now measures name the pool's shared helpers, and
each carries standing neighbour traffic this page must name:

- **Audio — SERVICE (1 edge).** The roster-collect `0025D9E0` calls `00261F90` on that layer —
  a service consult inside the sweep, not an audio relationship this page owns.
- **CombatAction — CLIENT (3 edges).** `002ECF10` is called by `002FED60` and `003589B0` by
  `00319F50`/`00325260` — battle-side fan-in on the shared apply and reducer helpers.
- **Gameplay — CLIENT and SERVICE (4 edges).** `0025D9E0` calls `00234150`; the `00268530`
  apply-pass calls `0030BFB0`, which itself reaches `00308040`; `003589B0` is also called by
  `0031ADB0`. Shared-helper traffic in both directions.
- **Movement — CLIENT and SERVICE (19 edges).** The pool helpers are movement-adjacent:
  `0025D9E0` calls `0025DF00`, `0025E4C0` is called by the same `0025DF00`, and `00263FF0` is
  called by `002E28E0`/`00392740` among fifteen further edges — locomotion consumers reading
  pool records.
- **Save_Load_Settings — SERVICE (3 edges).** `0025D9E0` calls `002EF2B0` and `00583920`, and
  `0026C8C0` calls `002EF2B0` — save/load consults on pool records.
- **Script_VM_Native_Bridge — CLIENT (99 edges).** The pool accessors are the native bridge's
  read surface: `0025AD10` is called by `0034FA70`, `0025AF60` by `0025E4C0`, and `0025E4C0`
  itself calls `0025B400`/`0025D740` — 95 further edges of the same verb fan-in class, not
  shared ownership.
- **Status_Periodic_Terminal — CLIENT (1 edge).** `002ECF10` is also called by `00301140` —
  one periodic-status consumer of the same apply helper.
- **World — CLIENT and SERVICE (3 edges).** `0025D9E0` calls `0025E400`, which `00358940` also
  calls (with `002623A0` further upstream) — world-side fan-in on the same resolve.
- **WorldAreaField — SERVICE (11 edges).** `0025C830` calls `00377C20` and `0025D9E0` calls
  `002677B0`/`003148D0`/`003148F0` among seven further edges — the field layer's row helpers
  consulted from inside the roster pass.


*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Input — CLIENT (4 edges).** The input-domain body `00226BE0` (`Input.ActorControlMaskPropagationRuntime`) calls the slot-array address `00263FF0` (`02098E10` plus the index times `0x288`), `ActorManager_GetRecordByOrdinal` (`00358940`) and the secondary-context chase `00359B80`; the input command-gate body `002E09A0` also calls `00263FF0`. Input propagates its per-actor mask by walking the manager slots and records through this contract's own resolvers, so it is a reader of the pool, not an owner of any region of it.

**Story_Event_Quest_Hunt — SERVICE (1 edge).** The definition binder `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) calls `EventMemory_QueryDefinitionIdAbsent` (`00377440`), the 62-byte query over the `EVTMEM` publisher cell `02ADD0A8`. At bind time the pool asks the event-memory table whether a definition id is absent; the table is the story layer's, and the binder only consumes its answer.

## Interior citation — frontier hub `00359B80` (2026-09-18, SWE2-EC7)

`00359B80` — 38 B, 6 A-measured callers; the `[+0x30]` field chase that forwards a sub-object
to `0031AD90`. Interior verified: null-guard on `rcx`, then `rcx = [rcx+0x30]`
([`00359B85`](../_index/ADDRESS-INDEX.md)), null-guard again, and the whole body is the
`jne 0031AD90` tail (`00359B8C`) — returns 0 when either link is absent. `0031AD90` itself is
an unlisted three-instruction leaf, `rax = rcx ? rcx + 0xED0 : NULL` (verified in the shipping
bytes — real code, not a function-census entry). The actor pool's secondary-context accessor
shape.

## SWE2-EC7-105 update (2026-09-20) - `0025AF60` measured

`0025AF60` (84 B) is the resolved word
write `0025AD10` and `0025E4C0` run: it
requires bit 15 of both `r8d` and `r9d`
armed and `edx <= 0x11`, picks
`ecx = sar(r8d, 0x10)` when `r8d` bit 14 is
clear else `[rcx + 0x28]`, calls
`003587C0(ecx, edx = r8w)` for the row
base, and stores `r9w` at
`word[rax + edx*2 + 0xC8]` - the
tagged-parameter write into the pool's
`+0xC8` word array.
Interior anchor `0025AF9C` (the `003587C0`
call).

`00268690` (187 B) is the roster-collect-and-dispatch `0025D9E0` runs on the four-entry `0209A1F0` party roster: each non-null record is `002EA6A0`-tested for aliveness and `003589B0`-reduced to a dword id appended to a stack list; when at least one slot produced an id the whole array is handed to `0036E700(0, count, &list, r15d)` - one shot converting the roster into a dispatched index array

Interior anchor `002686D0` (function `00268690`).

`00268530` (187 B) is the roster apply-pass `0025C830` runs on the same four `0209A1F0` slots: when a record's `+0x18` byte is 2 the record may be substituted by `003587C0([rbx+0x1A], [rbx+0x19])`, then `0030BFB0` reduces it to `sil`, `002ECF10(rbx, sil, ebp)` applies the pass parameter, and a live `[rbx+0xC0]` record has its `+0x154` byte rewritten as `(byte | 2) & ~1 | sil` - bit1 armed unconditionally, bit0 carrying the test result

Interior anchor `00268564` (function `00268530`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-contract-actor-record-pool-and-region-ma-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0026ADF0` | 49 B | when byte `rcx+3` AND 0xE0 equals 0x60, takes the qword at `+0xF0` of the qword at `rcx+0xB8` and stores `edx` to its dword `+0`, `r8d` to its dword `+4` and 1 to its byte `+0x2A`; otherwise returns without writing | `0026ADF4`, `0026ADF6`, `0026AE08`, `0026AE11`, `0026AE1C` |
| `0030BFB0` | 96 B | calls `ActorWork_GetBattleUnit` and returns 0 when the result is null or the `0x10` bit (bit 4) of its first byte is clear; otherwise, with `d` = its qword `+0x698`, returns bit 23 of the result's first dword when (`d` dword `+0x64` OR dword `+0x3C`) AND 0x8000201B is non-zero, else tail-jumps to `BattleUnit_ComputePartyBattleStance` (`rcx` = the result, `rdx` = `d`) when `d` is non-null and its byte `+5` is 0, and to `BattleUnit_HasNonPartyEngagementEvidence(result, 0)` otherwise | `0030BFB4`, `0030BFC1`, `0030BFD3`, `0030BFF9`, `0030C004` |
| `003DC0D0` | 93 B | calls `003587C0(dword rdx+8, word rdx+6)` and, when that returns non-null, builds a stack record (word `0x402`, then byte `rdx+3`, dword 0x80000000, byte 1, dword `rdx+8`, dword `rdx+0xC`) and calls `003DBCF0(result, &record, 1)`; a null result returns without the call | `003DC0E0`, `003DC0E8`, `003DC10E`, `003DC115`, `003DC122` |

## Homed bodies: functions reached only indirectly whose callees this page cites (OPUS, 2026-10-02, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted locally and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-contract-actor-record-pool-and-region-ma-homing-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00269060` | 33 B | calls `00268690(9)`, then tail-jumps to `00314DA0` with what `003148D0()` returns, bits `0x8` and `0x10` cleared | `00269064`, `00269069`, `0026906E`, `00269073`, `0026907C` |
| `003446D0` | 61 B | calls `00268530(00267E10(r9))`, then for indices 0 to 3 calls `00263750(index)` and, for each non-null result, `0035AE10(result, 1)` | `003446D9`, `003446E0`, `003446E9`, `003446FB`, `00344702` |
