---
contract: Initialise one actor storage record over memory that is already zero, reading a kind byte the carve loop wrote
category: 04-Actor-Entity
scope: subsystem
readiness: CONTRACT READY
confidence: PROVEN
implements: 04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md
entries: ["00266530"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image. §4 carries the page's own corrected
    reading rather than a fresh derivation, and says so per claim in §15; **what is measured here is
    the movement half of the `EH-1` correspondence**, read in the same session from
    `Actor_GetWorldPosition`'s 61 bytes. **This records checks performed on that date, not the method
    of the original derivation**, which is on the record page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-actor-storage-init-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — actor storage record initialisation

> **Authored 2026-09-22 by FABLE.** S-13's contract column carries one contract over its three
> pages, and that one implements the slot-pool page. **This takes the storage-record page**, the
> only one of the three with no contract; the manager-record page is S-52's since the split.
>
> Written against FRONTIER's adequacy test. **`AR-1` and `AR-2` are a pair no single body states:**
> what the masks in *this* function mean is decided entirely by what its *caller* did to the memory
> first.

## 1. Purpose

Turn one slot of a freshly allocated pool into an actor's storage record.

## 2. Interface

```c
void ActorStorage_InitializeRecord(Ctx *ctx, RecordTable *tbl, int index)   /* 00266530, 1,439 B */
```

Called by `ActorStorage_AllocateAndInitializeRecords` (`002679F0`) once per record.

## 3. Types

```
RecordTable            an 8-byte header then an array of pointers: record = *(tbl + index*8 + 8)
actor storage record   41 fields, +0x00 .. +0x11C  (a LOWER BOUND, not the size)
  +0x00   u16   the record's OWN slot index -- written at 002665EB, not first (CON-168)
  +0x03   u8    packed kind byte: READ three times here, written by the carve loop (AR-3)
  +0xB8   ptr   context pointer -- read, never written here
```

## 4. Preconditions · postconditions · invariants

### The five cross-operation invariants

**AR-1 — The memory is already ZERO when this runs, and that is the caller's doing.** The sole
caller allocates the whole pool in one block and `memset`s it to zero immediately before calling
this routine on every record. *The precondition is not checked here and cannot be seen here.*

**AR-2 — So the read-modify-write masks preserve NOTHING, and the recycler reading is refuted.**
On zeroed memory `and byte [rec + 0x14], 0x7F` and a plain store are **equivalent**. The mask forms
are how the compiler updates bit-fields in bytes that are already live — several of them are this
function updating **its own** earlier work, not a previous occupant's.

> **This is the page's own correction and it is worth carrying as an invariant rather than as
> history.** *The instruction forms are exactly as first published; only the conclusion drawn from
> them was wrong.* **A reimplementation that faithfully reproduces the masks is right; one that
> infers a pool-recycling lifecycle from them is wrong about the whole subsystem** — and the
> instructions alone cannot tell the two apart, which is why `AR-1` has to be stated with them.

**AR-3 — `+0x03` is an INPUT here, not an output.** The carve loop writes it **before** this routine
runs; this routine **reads it three times and never writes it**. *So the kind byte is decided
upstream, and anything downstream that gates on it is reading a value this initialiser only
consumes.*

**AR-4 — The record stores its own slot index, and the table indexes records individually.**
`record = *(tbl + index*8 + 8)` — an array of pointers behind an 8-byte header, so records are
separately allocated — and ~~the first field written is~~ the routine writes `+0x00 = index`. *(Corrected 2026-09-29, OPUS, falsification pass 1, `CON-168`: the index store `mov word ptr [rbx], r10w` is at `002665EB`, after six record stores - `+0x14` masked first, then `+0xEC` and `+0xF5` - and the calls `00266AD0` and `00266BD0` with the record. It is not the first field written. The record still carries its own index.)* *A record therefore knows
where it lives without the table, which is what lets it be passed around alone.*

**AR-5 — `+0x11C` is a LOWER BOUND, and six spans inside it are unrecovered rather than absent.**
The extent is where the highest field this routine touches ends; ~~**no allocation site was read**~~ *(answered: see the record's true size, CLOSED 2026-09-23, §14; 2026-10-02, OPUS)*.
Six spans — including 88 bytes at `+0x60`–`+0xB8` and 44 at `+0xC0`–`+0xEC` — are ~~simply not~~
~~touched by the initialiser~~ ~~**not touched by `00266530`'s own stores**~~ not touched by `00266530`'s own stores, except `+0xC8`–`+0xEB`, which it fills with `0xFFFF` *(corrected 2026-10-02, OPUS: `0026689A`–`002668B0` `rep stosw` with `rdi = rbx + 0xC8`, `ecx = 0x12`)*. *Corrected 2026-09-25 (FABLE, Claude Opus 5.5), on
OPUS block 296:* its callees write into them.
- **`003DB580`**, called with the record at `002667D7`, writes byte `+0x88` (`003DB594`), dword `+0x24` (`003DB59B`),
  byte `+0x89` (`003DB59E`) and word `+0x60` = `0xFF00` (`003DB62F`). EXP-112 executed that callee and observed
  those stores.
- **`003DBCF0`**, reached through `ActorResource_SubmitRequestDescriptor` with the record unchanged in `rcx`, writes
  byte `+0x60` (`003DBD7E`).
- **What still stands.** The type store declares these fields. The lower-bound point stands, and the gaps at
  `+0x84`, `+0x8A`, `+0x9C` and `+0xB0` remain unrecovered. *The type store records them as gaps rather than closing the record at
`0x11C`.*

## 5. State

**Owned:** the record's fields, for the duration of the call. **Read, never written:** `+0x03` and
the context pointer at `+0xB8`.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-actor-record-pool-and-region-map.md`](CONTRACT-actor-record-pool-and-region-map.md) — S-13's other contract, implementing the slot-pool page |
| **Split off** | [`CONTRACT-manager-slot-entry-tables.md`](CONTRACT-manager-slot-entry-tables.md) — S-52 since 2026-09-22; a closed island sharing zero data cells with this side |
| **Consumes `+0x03`** | [`CONTRACT-heading-speed-to-position-delta.md`](../06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md) — **if** `EH-1` holds; see §14 |

## 7. State transitions

*allocate the pool and zero it → per record: write the slot index, then the flag and pointer blocks,
reading `+0x03` and `+0xB8` without writing them.*

## 8. Script · resource · event interactions

None directly.

## 9. Determinism

Deterministic. No generator is drawn.

## 10. Failure paths and edge conditions

- **None are checked here.** This routine takes a valid table and index and does not validate them;
  its safety rests entirely on `AR-1`'s caller.

## 11. Observable behaviour

None directly. This is the moment an actor's storage exists.

## 12. Reproduction formula

Zero a record, run the initialiser, and assert each masked byte equals what a plain store would have
produced (`AR-2`). Pre-set `+0x03` and assert it is **unchanged** afterwards (`AR-3`). Assert
`+0x00` equals the index argument (`AR-4`). Assert the six named spans are untouched (`AR-5`).

## 13. Runtime validation

**None by this contract.** S-13's runtime cell is not addressed here. *Stated rather than left blank
so a CONTRACT READY header is not read as evidence of execution.*

## 14. Unresolved

- [x] ~~**`EH-1` — whether the storage record and the movement actor are the SAME type.**~~
      **CLOSED 2026-09-23 (SWE2-CONTRACT) — the page resolved it PROVEN on 2026-09-08 and this
      contract never imported it.** The owning page's §11 answer does not wait on the
      bridging-body test this contract proposed: the carve loop **writes `+0x03` itself**
      (`00267AFA`–`00267B13`: `(kindCode << 5) | (sequence & 0x1F)`), so the byte the movement
      gate masks with `0xE0` is authored inside this subsystem's own allocator — the storage
      record and the movement actor share one field with one writer, which is stronger evidence
      of one type than a hand-off site would be. Re-verified at the instructions this pass:
      `r9b = group & 0x1F` OR'd into the low five bits, `byte[r8] << 5` (the descriptor's class
      code) into the top three.
- [x] ~~The record's true size~~ — **CLOSED 2026-09-23 (SWE2-CONTRACT): per-class authored
      strides — matching the page's EH-2 answer (720–1,760 bytes by kind) and adding the
      descriptor address.** The sole caller `002679F0` walks a static descriptor table at
      `0x1E0C328` — 4-byte entries `{u8 classByte, ~~u8 pad~~ u8 subFlag, u16 stride}` *(corrected 2026-10-02, OPUS: `00266B83` reads `+1`: 1 selects the `0xA0` resource step, set on rows 2, 4 and 7)* — and carves each
      group's records at `align16(stride)` in one zeroed pool. Decoded table (raw stride →
      aligned):

      | group | classByte | raw | carved stride | class (`byte & 7`) |
      |---|---|---|---|---|
      | 0 | `0x00` | `0x328` | `0x330` | 0 |
      | 1 | `0x01` | `0x3A8` | `0x3B0` | 1 |
      | 2 | `0x01` | `0x330` | `0x330` | 1 |
      | 3 | `0x02` | `0x348` | `0x350` | 2 |
      | 4 | `0x02` | `0x2D0` | `0x2D0` | 2 |
      | 5 | `0x03` | `0x6E0` | `0x6E0` | 3 |
      | 6 | `0x03` | `0x6E0` | `0x6E0` | 3 |
      | 7 | `0x03` | `0x668` | `0x670` | 3 |
      | 8–11 | `0x14`/`0x02`/`0x14`/`0x1A` | `0x0000` | — | reserved — no records carved |

      So `+0x11C` is a lower bound on the **shared prefix** this initialiser writes; the real
      records are `0x2D0`–`0x6E0` depending on class, and **class-3 records are the `0x6E0`/
      `0x670` allocations** — large enough to hold the movement context. The carve also
      *explains* `+0x03`: `(class << 5) | (group index & 0x1F)`.
      *Residual:* the six unrecovered spans' contents stay open (AR-5) — they sit inside the
      class-3 `0x6E0` extent this initialiser never touches.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| `EH-1`'s movement half | [the locomotion contract](../06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md) `LD-2`, where that body was read in full this session and both offsets taken off the same register — **cited by contract, not re-derived** | 1 |
| `AR-1`, `AR-2` — zeroed memory and the refuted recycler | [the record page](Actor-Storage-Record/the-record-behind-every-actor.md) §2, **corrected 2026-09-08** — carried, not re-derived | 1 |
| `AR-3`, `AR-4`, `AR-5` — the input byte, the table shape, the bound | [the record page](Actor-Storage-Record/the-record-behind-every-actor.md) §§3–4 | 1 |
| record size is per-class authored: descriptor table `0x1E0C328` `{u8 class, u8, u16 stride}` — class 3 strides `0x6E0`/`0x670`, classes 0–2 `0x2D0`–`0x3B0`; `+0x03` written `(class<<5)\|(group&0x1F)` | `002679F0` decoded whole — `00267A41`/`00267ACA` descriptor reads, `00267AF5` pointer-table store, `00267AE8`–`00267B13` the `+0x03` compose | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on `AR-1` through `AR-5`. **`AR-2` is the one that
misleads a reader rather than a port**: the masks reproduce correctly either way, but the lifecycle
inferred from them changes what the rest of the subsystem is thought to do. **`AR-5` is the one a
port closes prematurely** — treating `0x11C` as the size.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **ActorEntity — internal.** The record, its table and the initialiser are this category's own.
- **Movement — the OTHER side of `EH-1`, and deliberately not asserted.** The locomotion contract's
  `LD-2` is cited **by contract and not by address** for what it measured about
  `Actor_GetWorldPosition`'s own two reads — that body is a 79-caller hub and citing it here would
  import its whole client set for a fact this document only borrows. **This contract does not claim
  the two types are one**, which is precisely §14's point *(answered: §14's `EH-1` item is CLOSED 2026-09-23 — the owning page resolved it PROVEN; 2026-10-02, OPUS)*.
- **Every other layer reached is MECHANICAL**, through this body's own callees. *Only the
  initialiser is cited by address. Note the page's own warning: this function holds the image base in
  a register and addresses globals through it, a form RIP-relative datasets cannot see — so any
  "which globals does it touch" answer from that source is incomplete by construction, and none is
  relied on here.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document — the defect measured in
> `../_index/candidates/fable-crossings-prose-false-clears.tsv` — so these are discharged by the
> paragraphs above and not by a stray noun. *"Actor" and "movement" would otherwise each be cleared
> by the word alone.*

## 17. Related

- [The record behind every actor](Actor-Storage-Record/the-record-behind-every-actor.md) — the mechanism
- [Contract — the actor record pool and region map](CONTRACT-actor-record-pool-and-region-map.md) — S-13's other
- [Contract — heading, speed and the position delta](../06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md) — `EH-1`'s movement side

## Falsification pass 1 — 2026-09-29 (OPUS): AR-4's ordering refuted; the rest survives

**Attack.** AR-1 to AR-5 became checks that fail if the shipping image says otherwise. Script:
`Tools/analysis-kit/gfz-scripts/falsify_actor_storage_init.py`, output `falsify_actor_storage_init.out`, image `73461d08…`,
0 BROKEN.

| # | Clause attacked | Result |
|---|---|---|
| S0 | §2 size and caller | **survives**: 1,439 B, called only from `002679F0` |
| S1 | AR-1 | **survives**: `002679F0` calls `memset` before its first call to `00266530` |
| S2 | AR-3 | **survives**: `+0x03` is read three times through `rbx` and never written |
| S3 | AR-4 "the first field written is `+0x00`" | **REFUTED**: the index store is at `002665EB`, after six record stores (`+0x14` first) and two calls. `CON-168` |
| S4 | AR-5 | ~~**survives**~~ **refuted in part**: the body's own stores end at `0x11C` and touch ~~neither `+0x60`-`+0xB7` nor `+0xC0`-`+0xEB`~~ no byte of `+0x60`-`+0xB7`, but do fill `+0xC8`-`+0xEB` *(corrected 2026-10-02, OPUS: `002668B0` `rep stosw`, eighteen words of `0xFFFF`)*; `003DB580` writes `+0x24`, `+0x60`, `+0x88` and `+0x89` |

Consumer record: [`_index/candidates/actor-storage-init-falsification-pass-1-0929/`](../_index/candidates/actor-storage-init-falsification-pass-1-0929/README.md).

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it; this section names the initialiser's two Movement callees.*

**Movement — SERVICE (2 edges).** `ActorStorage_InitializeRecord` (`00266530`) calls `00265FF0`, the 1,339-byte Movement body that initialises the movement context reached through the record's pointer at `+0xB8` (a header at `+0x100`..`+0x110`, then two sub-records of one layout at `+0x120` and `+0x1A0`, as the context census page reads it), and `00268380`, a 420-byte Movement body that branches on the record's type bits (byte `+3` shifted right by 5) and reads float fields through the pointers at `+0xB8` and `+0xC0`. The initialiser hands the new record to the movement layer to seed its locomotion context; the movement side owns that context's layout, and this contract still does not claim `EH-1`'s two types are one.
