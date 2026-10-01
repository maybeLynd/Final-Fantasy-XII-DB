# S-13 runtime: per-invariant stub exposure for EXP-107 / EXP-112, and AR-5's "untouched" contradicted by EXP-112's own observation (OPUS, 2026-09-25, block 296)

**Row:** S-13, actor storage, manager slots and unit pool. The runtime cell is MIXED, with the qualifier "no
per-invariant stub-exposure analysis yet". The contracts are `CONTRACT-actor-storage-record-initialisation.md`
(AR-1..AR-5, FABLE) and `CONTRACT-actor-record-pool-and-region-map.md`. EXP-061 is also named in the cell, but its
record states that it has no contract: it covers MP writers. This note scores nothing.

## What each record substitutes

| record | real | substituted |
|---|---|---|
| **EXP-107** | allocator `002679F0` and region map `00266AD0` | the per-record ctor `00266530` is scripted (arguments captured); `memset` `00861EC0` is an import thunk; the indirect allocator `q[mgr+0x88]` is planted and returns the fixture pool |
| **EXP-112** | ctor `00266530` (1,439 B) plus its real callees, including `003DB580` (SINIT) | `00265FF0`, `00265B60`, `00268380` ×2, `002681E0`, `003DBB60` ×4; `00268EA0` / `003DBDC0` are scripted but dead |

**Where each scripted callee's writes land** (read 2026-09-25). All of them receive `rcx = record` from the ctor.

| callee | writes |
|---|---|
| `00265B60` | the object at `[rec+0xC0]` (the SecondaryContext region), not the header |
| `00265FF0` | the context at `[rec+0xB8]` (`r14`), not the header |
| `002681E0` | `[rec+0xC0]+0x153`, and `[[rec+0xC0]+0x138]+0x80`; not the header |
| `00268380` | no direct store; its callees `003DA710` / `006C0520` / `003DB130` / `003DB120` / `003DAF20` were not read |
| `003DBB60` | forwards to `003DBCF0(rec, …)`, which **writes `byte [rec+0x60]`** (`003DBD7E`) |

## Per invariant

| inv. | executed by | can a substitution reach it? |
|---|---|---|
| **AR-1** memory is zero because the caller memsets it | EXP-107: the allocator's `memset` call is executed as an import thunk (arguments captured) | import-class only |
| **AR-2** the masks preserve nothing | EXP-112: the ctor's own mask forms on zeroed memory | **no** |
| **AR-3** `+0x03` is read, never written, by this routine | EXP-112: the ctor's own body | **no** for the ctor's instructions. The scripted callees write their sub-objects (above), not `+0x03` |
| **AR-4** the record stores its slot index; the table indexes records | EXP-107 carve + EXP-112's `+0x00 = index` | **no** |
| **AR-5** the extent is a lower bound, and six spans, "including 88 bytes at `+0x60`–`+0xB8`", are "not touched by the initialiser" | EXP-112 | **contradicted, see below** |
| pool contract: records are reached through the pointer table; the region map's interior pointers | EXP-107 (real allocator and carve) | **no**. The scripted ctor does not touch the table |

## AR-5 contradicted by EXP-112's own observation

EXP-112 ran `003DB580` (SINIT) **real**, and its record observes `b[+0x88] = r15`, `d[+0x24] = 0`, `b[+0x89] = ebp`
and `w[+0x60] = 0xFF00`. Its "A8 clear stride" finding is also over the `b[+0x88]` slots. Those are writes into the
88-byte `+0x60`–`+0xB8` span that AR-5 calls untouched by the initialiser. The scripted `003DBB60` → `003DBCF0` path
also writes `byte [rec+0x60]`.

- **The type store is already right:** `+0x60` `entryFreeListHead`, `+0x88` `slotCountA8`, `+0x89` `slotCountA0`,
  `+0x8C` / `+0x94` channel tails and heads, and so on.
- **AR-5's sentence is true only of `00266530`'s own instructions.** The initialisation it performs, through the
  callees it makes, writes the span.
- **What still holds:** the real gap rows (`+0x84`, `+0x8A`, `+0x9C`, `+0xB0`: "no censused access") and the
  lower-bound point.
- **Routed to FABLE (contract owner):** restate AR-5 as "not touched by the routine's own stores; its callees `003DB580`
  and `003DBCF0` write `+0x24`, `+0x60`, `+0x88`, `+0x89`".

## For the scorer

- No application stub reaches AR-1..AR-4 or the pool contract's pointer-table invariant.
- AR-5 needs a wording correction, not an execution.
- `00268380`'s callee chain is the one unread branch: it receives the record, and whether it writes the header is not
  established.
- `live_game` is false.
