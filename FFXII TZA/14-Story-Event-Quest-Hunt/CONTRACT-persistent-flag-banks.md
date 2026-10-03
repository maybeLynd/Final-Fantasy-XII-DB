---
contract: The persistent flag banks — query, set, and the authored gate that chooses between a flag and a schedule
category: 14-Story-Event-Quest-Hunt
scope: subsystem
readiness: CONTRACT READY
confidence: PROVEN
implements: persistent-flag-banks.md
entries: [0032A8A0, 0032A930, 0032A9A0, 0032AA00, 0032AA60, 0032AAD0, 0032AB60, 0032ABF0, 0032AC70, 0032ACF0, 0032AD70, 0032ADF0, 00377970, 00379160, 00377440, 002EF2D0, 002EF2B0]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 27 addresses cited - 3 data, 22 entry, 2 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-08
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-persistent-flag-banks-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the persistent flag banks

> **The fourth behavioural contract in this database, and the first over a category that is at
> disposition A for its entire owned population** — all 15 functions the ledger assigns to
> `Story_Event_Quest_Hunt` have been read individually. It formalises
> [`persistent-flag-banks.md`](persistent-flag-banks.md) and
> [`event-memory-at-actor-bind.md`](event-memory-at-actor-bind.md).
>
> **Readiness is `CONTRACT READY`, not `RECONSTRUCTION READY`** — §13 carries no LIVE observation. Nothing here has
> been observed in a live process, and the charter's readiness gate requires it.

## 1. Purpose

Remembers **what has already happened in the story**, permanently, as bits. ~~Six banks~~ Five banks of flags (six accessor families - `Bank512`'s Low and High pairs share one region, section 3) *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V1, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))* live
inside the save payload, so setting one *is* writing save state — there is no separate "story
progress" structure that the save mirrors. A seventh mechanism, reached through the same authored
gate, is **not** a flag at all: it answers from a schedule of thresholds, and its answer can go
back to false.

## 2. Interface

Every entry point is MS x64, takes its id in `ecx`, and touches the payload only through
`SaveImage_GetPersistentPayloadBase` (`002EF2B0`).

| operation | entry | signature | returns |
|---|---|---|---|
| authored gate | `0032A8A0` (122 B) | `(uint16 encodedId ecx)` | `eax` = 0/1 |
| query Bank2048 | `0032A930` (100 B) | `(int id ecx)` | `eax` = 0/1 |
| query Bank64A | `0032A9A0` (93 B) | `(int id ecx)` | `eax` = 0/1 |
| query Bank64B | `0032AA00` (93 B) | `(int id ecx)` | `eax` = 0/1 |
| query Bank512 low half | `0032AA60` (100 B) | `(int id ecx)` — `id` 0…0xFF | `eax` = 0/1 |
| query Bank512 high half | `0032AAD0` (104 B) | `(int id ecx)` — **adds `0x100` itself** | `eax` = 0/1 |
| set Primary | `0032AB60` (121 B) | `(int id ecx, int value edx)` | — |
| set Bank2048 | `0032ABF0` (119 B) | `(int id ecx, int value edx)` | — |
| set Bank64A / 64B | `0032AC70` / `0032ACF0` (116 B) | `(int id ecx, int value edx)` | — |
| set Bank512 low / high | `0032AD70` / `0032ADF0` (119/123 B) | `(int id ecx, int value edx)` | — |
| authored threshold schedule | `00377970` (127 B) | `(int index ecx)` | `eax` = 0/1 |
| apply the new-game flag list | `00379160` (86 B) | `()` | — |
| reset payload + apply list | `002EF2D0` (38 B) | `()` | — |
| event-memory id absent? | `00377440` (62 B) | `(int id ecx)` | `eax` = **1 when ABSENT** |

**`value` is a boolean, not a bit.** Every setter branches `test r8d, r8d` and takes the `or` arm on
non-zero, the `and`-with-complement arm on zero. **There is no "toggle" and no read-modify-return.**

**`00377440`'s polarity is inverted and load-bearing** — it returns `1` when the id is *not* in the
list. A reimplementation that returns "found" will invert every decision at its call site.

**There is no query for Primary.** Primary is read only through the authored gate at `0032A8A0`;
the other ~~five banks~~ four banks have a dedicated query (five query functions, two of them `Bank512`'s) *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V1, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))* and Primary does not.

## 3. Types

**`PersistentFlagPayload`, size `0x1538`** (5,432 bytes) — in `_types/`. The size is not inferred:
`002EF2D0` clears exactly that many bytes in one `memset` at `002EF2DB`/`002EF2E8`.

```
base = SaveImage_GetPersistentPayloadBase() = SaveImage_GetActiveBuffer() + 0x200
                                            (002EF2B0 -> 002EF640 -> 0x02164280)

  +0x1044   i32     active or pending field (area) id
  +0x1060 .. +0x1064   a byte-flag cluster; +0x1062 alone has 29 access sites
  +0x1384   u8[8]   Bank64A     ids 0..0x3F
  +0x138C   u8[8]   Bank64B     ids 0..0x3F
  +0x1394   u8[32]  UNEXPLAINED - 256 flags' worth, no accessor by either route   [AA-5]
  +0x13B4   u8[256] Bank2048    ids 0..0x7FF
  +0x14B4   u8[64]  Bank512     ids 0..0x1FF   (Low = 0..0xFF, High adds 0x100 itself)
  +0x14F4   u8[64]  Primary     ids 2..0x1FF
  +0x1534   u8[4]   UNEXPLAINED - the payload's last four bytes                   [AA-8]
                                                                  ends at +0x1537
```

**`Bank512` is one region with two accessor pairs, not two banks.** `0032AAD0` carries a literal
`lea eax, [rcx + 0x100]`; both halves index `+0x14B4`.

> **441 of 5,432 bytes are declared — 8.1 %.** The rest is reported by `types_index.py` as
> three undeclared gaps totalling 4,991 bytes, and `441 + 4,991 = 5,432` exactly. **Nine
> tenths of the persistent payload has no known accessor**, and the store says so rather than
> rounding the record up to “understood”. The ~~six~~ five banks *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V1, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))* are what is mapped; they are not what
> the payload mostly is.

## 4. Preconditions · postconditions · invariants

**Preconditions.** The active save buffer must exist; every accessor calls `002EF2B0`
unconditionally and does not null-check the result.

**Postconditions.** A setter with `value != 0` leaves exactly one bit set and nothing else changed;
with `value == 0`, exactly one bit clear. A query returns `0` or `1` and writes nothing.

**Invariants.**

```
byteOffset = bankBase + (id >> 3)          bit = 1 << (id & 7)
query(id)  = (payload[byteOffset] & bit) != 0
set(id,1)  : payload[byteOffset] |=  bit
set(id,0)  : payload[byteOffset] &= ~bit
```

- **The bit arithmetic is signed-safe by construction.** Every accessor computes
  `cdq ; and edx,7 ; add eax,edx ; and eax,7 ; sub eax,edx ; sar ecx,3` rather than a plain shift —
  the compiler's signed division idiom, which is why §10's negative-id path lands where it does
  instead of faulting.
- **Ids 0 and 1 never touch storage.** The gate answers `true` for 0 and `false` for 1 before any
  bank is consulted, and `PersistentFlag_SetPrimary` rejects both (`id - 2u > 0x1FD`).
- **A flag never goes back on its own.** No code path clears a bank wholesale except the new-game
  `memset`; the only clear is an explicit `set(id, 0)`.

## 5. State

| | detail |
|---|---|
| **read** | the payload, through `002EF2B0`; `02ADD0D0` (the new-game list); `02ADD0A8` (the event-memory list); the authored threshold table and `FieldData_GetVariable0` (`00265270`) |
| **written** | the payload only. **No global is written by any accessor.** |
| **allocated** | none — the payload is a fixed region of the save image at `0x02164280 + 0x200` |
| **deallocated** | none |

## 6. Relationships

```
authored script / event / world logic
  -> PersistentFlag_QueryPrimaryOrAuthoredThresholdGate(encodedId)      32 callers
     -> bit 14 set   : PersistentFlag_QueryAuthoredThresholdSchedule(index)
     -> bit 14 clear : 0 -> true, 1 -> false, else Primary bit at +0x14F4

new game
  -> 002EF2D0 : memset(payloadBase, 0, 0x1538), then TAIL-JUMP
     -> 00379160 : for each u16 id in mapjumpgroupinit.bin, SetPrimary(id, 1)

save
  -> SaveImage_FinalizeHeaderAndChecksum -> gate(0x400B), then the payload is written
```

**One caller is not story logic at all:** `InputGameplay_ArbitrateDigitalInputAndModalState`.
**Story flags participate in input arbitration.** EH funclet edges excluded throughout.

## 7. State transitions

The banks have no state machine. **The schedule does**, and it is a parity:

```
answer = false
for each u16 entry in the schedule:
    if (int16)progress < (entry & 0x7FFF) : stop, return answer
    answer = !answer                                  TOGGLE at every threshold passed
    if (int16)entry < 0                   : stop, return answer      bit 15 ends the list
```

> **So an authored condition can be true only *between* two story points.** On at the first
> threshold, off at the second, on again at the third. **A flag cannot express that**, which is the
> whole reason the gate has two modes.

## 8. Script · resource · event interactions

**Two shipped files, both resource `kind 9`, both published by an address-taken ten-byte setter
installed in `WorldAreaField_RequestAuthoredMapTables` (`00378540`):**

| request | publisher | global | file | size |
|---|---|---|---|---|
| `(9, 0x28 = 40)` | `00378B90` | `02ADD0D0` | `mapjumpgroupinit.bin` | 116 B — room for 53 ids |
| `(9, 0x29 = 41)` | `00378A50` | `02ADD0A8` | `eventmemorylist.bin` | 26 B — room for 8 ids |

Both carry an 8-byte header, a `u16` count at `+8`, and `u16` entries from `+0x0A`. **Sizes are
capacities; the count field is what the loops trust.** The ids themselves are unread — `DS-1`.

**Encoded gate ids observed across the gate's 32 call sites:**

```
threshold queries (bit 14 set)   0x4004 0x4006 0x4007 0x4008 0x4009 0x400A 0x400B
                                 0x400C 0x400D 0x4010 0x4011 0x4067   and 0xFFFF
Primary bank reads (bit 14 clear)  0x0001 0x0002 0x0054 0x005E 0x006F 0x0107
```

`0xFFFF` is a **sentinel used by nine sites**: bit 14 is set, so it is a threshold query with index
`0x3FFF`, which fails the entry-count bound. `gate(0xFFFF)` is therefore **false**.

## 9. Determinism

**RNG:** none in the accessors. One *writer* is downstream of a roll —
`BattleUnit_TryTriggerNearbyAuthoredFieldAction` sets a `Bank512Low` bit after a 75/25 MT19937 draw,
so a Bank512 bit is not a pure function of player action. **Timing:** none; every accessor is
straight-line. **Threading:** no synchronisation primitive appears in any of the seventeen entries,
and **single-threaded access is not proven.**

## 10. Failure paths and edge conditions

**Every bound test fails closed on the upper end** — the query returns `0`, the setter returns
having written nothing. On the **lower** end they do not all agree, and the disagreement is exact:

| accessor | bound test | negative id |
|---|---|---|
| `QueryBank2048` | `cmp ecx,0x800 / jl` **+ `test ecx,ecx / js`** | rejected |
| `QueryBank512Low` / `High` | `cmp ecx,0x100 / jl` **+ `js`** | rejected |
| `SetPrimary` | `lea eax,[rcx-2] ; cmp eax,0x1FD / ja` — **unsigned** | rejected |
| `SetBank2048` | `cmp ecx,0x7FF / ja` — **unsigned** | rejected |
| `SetBank512Low` / `High` | `cmp ecx,0xFF / ja` — **unsigned** | rejected |
| **`QueryBank64A` / `64B`** | `cmp ecx,0x40 / jl` — **signed, no `js`** | **ACCEPTED** |
| **`SetBank64A` / `64B`** | `cmp ecx,0x40 / jge` — **signed, no `js`** | **ACCEPTED** |

> ### The four `Bank64` accessors are the only ones that let a negative id through
>
> Seven of eleven reject negatives, by two different mechanisms — an added `js`, or an unsigned
> compare. **The four `Bank64` accessors use a signed compare and add no `js`.** Working the
> signed-division idiom through by hand:
>
> ```
> id =    -1  ->  byte offset   +0  ->  payload +0x1384   bit index -1  (shl by 31 -> mask 0)
> id =    -8  ->  byte offset   -1  ->  payload +0x1383
> id =   -16  ->  byte offset   -2  ->  payload +0x1382
> id = -1024  ->  byte offset -128  ->  payload +0x1304
> ```
>
> `movsxd rcx, edi` sign-extends it, and `or byte [rax + rcx + 0x1384], bl` **writes before the
> bank** — into ~~the unmapped payload stretch between `+0x1164` and `+0x1384`~~ the payload below the bank, at `+0x1384` + trunc(id / 8), with no lower bound in the code (the `cmp ecx, 0x40` / `jge` at `0032AC77` / `0032AC7A` is signed, so every negative id passes; id -4096 reaches `+0x1184`, and a span such as `+0x1164`-`+0x1384` belongs to a set of ids, not to the setter) *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V11, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*, which is save state
> like everything else in the payload.
>
> **This is a latent property of the accessor, not a demonstrated bug.** No caller was found that
> passes a negative: the ids in the two shipped lists are `u16` and reach `SetPrimary`
> zero-extended. ~~**Whether any authored path can produce a negative id is not established**~~ — and a
> reimplementation that adds the missing guard would be *more* defensive than the original, which
> is a parity difference and must be declared. `DX-1`.
>
> **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): no authored path reaches a `Bank64` accessor at all, with any
> id.** Three steps:
> 1. **The four accessors have exactly six call sites** in the raw call index: `0032A9A0` ← `0034D953`,
>    `0032AA00` ← `0034DDC3`, `0032AC70` ← `0034CA37` / `0034D1A4`, and `0032ACF0` ← `0034CD57` / `0034D614`.
>    These are the six `shutoral` verb handlers `0x2F8`–`0x2FD`
>    ([the bank page](persistent-flag-banks.md) §8). No rip-relative reference to any accessor exists, and no
>    64-bit pointer to one. The only other occurrences of their RVAs are `.pdata` entries and chained-unwind
>    records `{begin, end, unwind}` in `.rdata`, which are exception metadata, not calls.
> 2. **None of the six verbs is called by any shipped script.**
>    `members/bank64_verb_census.py` decodes every shipped `section_000` script
>    image, all language copies: 10,036 scripts and 27,623,415 CALL-family sites. It finds **zero** sites for
>    each of `0x2F8`–`0x2FD`. Its controls are found: `settalknpcname` `0x399` at 513 sites (the `us` copy's 57,
>    nine times over), and the load-mode setter `0x7067` in `ttl_a01` and `ttl_c01`.
> 3. The domain is CALL-family sites with an immediate verb id, which is the form the census decodes.
>
> *So the negative-id path is unreachable in the shipped game, and the declared parity difference is a difference
> in code nothing shipped runs.*

> ### Sharpened by execution — only a negative id that is a MULTIPLE OF 8 writes anything
>
> §17's differential test ran these accessors as shipped, and the acceptance is much wider
> than the damage. `SetBank64A` **accepts 77 of 153 test ids, including all 67 negatives** —
> but the mask is `shl bl, cl` on an **8-bit** register, and the shift count is masked to five
> bits, so a bit index outside `0..7` yields **zero** and the `or` writes nothing.
>
> Working it through: for a negative id, `adj = 7` and `bit = ((id + 7) & 7) - 7`, which is in
> range **only when `id` is a multiple of 8**. So:
>
> ```
> id = -1, -17, -63     accepted, mask 0, WRITES NOTHING
> id = -8               writes bit 0 of payload +0x1383
> id = -16              writes bit 0 of payload +0x1382
> id = -64              writes bit 0 of payload +0x137C
> id = -1024            writes bit 0 of payload +0x1304
> id = -4096            writes bit 0 of payload +0x1184
> ```
>
> **A negative id writes only when it is a multiple of 8, and then it writes bit 0 of the byte
> at `base + id/8`.** Over the test's id set that is **12 distinct offsets, from `0x1383` down
> to `0x0FE0`** — 932 bytes before the bank. *That span is the test id set's, not a bound: the setter has none, and ids -1 to -7 write nothing (their bit index is negative, so the shifted mask is 0).* *(clarified 2026-10-02, FABLE, on OPUS's byte verdict C-V11, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))* The earlier reading was right about where a write
> lands and silent about how few ids produce one; this is the correction.

> ### CORRECTED 2026-09-08 — `SetBank64B`'s negatives do NOT land where `SetBank64A`'s do
>
> The paragraph above says a negative id writes *“into the unmapped payload stretch between
> `+0x1164` and `+0x1384`”*. **That is true of `SetBank64A` and false of `SetBank64B`**, and
> the difference is simply the eight bytes between their bases. It went unnoticed because
> only `64A` had been reimplemented; running the other member of the pair settles it.
>
> **Eight negative ids given to `SetBank64B` write inside `Bank64A`** — a bank with its own
> accessors, its own meaning and its own readers:
>
> ```
> SetBank64B(-64)  ->  payload +0x1384 bit 0  =  Bank64A flag 0
> SetBank64B(-56)  ->  payload +0x1385 bit 0  =  Bank64A flag 8
> SetBank64B(-48)  ->  payload +0x1386 bit 0  =  Bank64A flag 16
> SetBank64B(-40)  ->  payload +0x1387 bit 0  =  Bank64A flag 24
> SetBank64B(-32)  ->  payload +0x1388 bit 0  =  Bank64A flag 32
> SetBank64B(-24)  ->  payload +0x1389 bit 0  =  Bank64A flag 40
> SetBank64B(-16)  ->  payload +0x138A bit 0  =  Bank64A flag 48
> SetBank64B(-8)   ->  payload +0x138B bit 0  =  Bank64A flag 56
> ```
>
> **Measured by running the shipped accessor, not derived:** every id in `-1024..-1` was
> executed under emulation against a zero payload and the changed byte read back.
> **128 of the 1,024 write — exactly the multiples of 8** — confirming the mask rule above
> with a denominator. `SetBank64A`'s 128 writes span `+0x1383` down to `+0x1304` and **none
> of them lands in any named bank**; `SetBank64B`'s span `+0x138B` down to `+0x130C`, and
> **eight land in `Bank64A`**.
>
> **So the two are not equivalent hazards.** One writes into payload nobody has claimed; the
> other can flip a flag another accessor reads. `DX-1` still asks whether an authored path
> can produce a negative id at all — that is unchanged, and nothing here shows one can.

**Other edges.** `gate(0xFFFF)` is false (§8). A schedule offset of `0` means "no schedule" and
returns false. `QueryBank512High` adds `0x100` itself, so passing an already-offset id reads the
wrong half.

## 11. Observable behaviour

- A story beat that has happened stays happened across save and load, because the bit **is** the
  save state rather than a copy of it.
- **A new game is not blank**: the payload is zeroed and then ~~the ids in `mapjumpgroupinit.bin` are
  switched on~~ 52 of the 53 ids in `mapjumpgroupinit.bin` are switched on - its first id, 0, is dropped by `SetPrimary`, which accepts 2 to 0x1FF *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V2, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))* - before the first frame.
- An NPC line that is available only *between* two story points is a threshold schedule, not a
  flag (§7).
- A condition an author wants always-true or always-false is written as id `0` or id `1`, and never
  reaches storage.

## 12. Reproduction formula

```c
/* bit address, every bank */          byte = base + (id >> 3);  mask = 1 << (id & 7);
/* encoded gate id */                  idx  = v & 0x3FFF;  threshold = (v & 0x4000) != 0;
/* gate */                             threshold ? schedule(idx)
                                       : idx == 0 ? 1 : idx == 1 ? 0
                                       : idx < 0x200 ? primaryBit(idx) : 0;
/* Bank512 high half */                effective = id + 0x100;
/* Primary setter bound */             reject if (unsigned)(id - 2) > 0x1FD;
/* schedule */                         parity of thresholds passed, bit 15 ends the list;
/* new game */                         memset(base, 0, 0x1538); for each id: setPrimary(id, 1);
```

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent, and this is the gate the
subsystem fails.**

**RECLASSIFIED 2026-09-12 (`OPUS-S13-CLASSIFY-THREE`).** This section read *"None. Empty
deliberately"*, which was true of the **live** half only: the bank accessors have been executed
against the shipped bytes, and the contract was being scored `nothing executed` with a passing
harness beside it.

**Instrument:** [`diff_flag_banks.py`](../../../Reconstruction/Tests/Differential/diff_flag_banks.py)
against [`flag_banks.c`](../../../Reconstruction/Game/Story/flag_banks.c).
**Re-run 2026-09-12: 8064 comparisons, 0 mismatches** — including the negative ids that write
*below* their bank base, which the suite enumerates on the reference side rather than avoiding.

**Nothing about the live gap changes.** The three cheap confirmations below remain exactly as
valuable; an isolated run cannot tell you what a story flag holds in a running game.

Every claim above is static. The cheapest confirmations, in order: read `0x02164280 + 0x200 +
0x14F4` in a live process and confirm a known story flag's bit; step `0032A8A0` with `0x400B` at a
save and confirm the schedule arm is taken; confirm the payload is zero at `+0x1394..+0x13B3` on a
fresh game. **One attach answers all three.**

<!-- OPUS-MUT-S13-RESTATE -->
### Mutation campaign, re-run 2026-09-12 on the full literal surface

**57 generated points: 55 KILLED · 0 SURVIVED · 1 EQUIVALENT · 0 NO_BUILD · 0 TIMEOUT · 1 INVALID. Verdict `INCOMPLETE`.**
Receipts: `Database/Tools/work/OPUS/litsuffix/flag_banks` (ignored path). Instrument: `Reconstruction/Tests/mutation_test.py`. The table for every pilot, and the four kinds a survivor can be, are on [`MUTATION-CAMPAIGNS.md`](../../../Reconstruction/MUTATION-CAMPAIGNS.md).

**No survivors.** The one `INVALID` is a mutation of the payload size that the driver's own guard rejects before any comparison, which is why the verdict is `INCOMPLETE` rather than `PASS` — the instrument will not call a run complete that it could not read end to end.

## 14. Unresolved

1. **What each bank is *for*.** `Bank512` is confirmed (authored field-action / trigger state);
   `Bank2048`, `64A` and `64B` still have **no engine consumer at all**. `AA-2`.
   **ANSWERED 2026-09-21 (SWE2-CONTRACT) — the "no engine consumer" clause is wrong for
   `Bank2048`, and the whole item is settled:**
   - `Bank2048` is **the set of NPC names the player has been told** — the sibling page's
     2026-09-18 correction ([persistent-flag-banks.md](persistent-flag-banks.md)), which the
     operand-level caller census here reproduces exactly: `QueryBank2048` `0032A930` has seven
     call sites in five functions — the display-name resolver `00263990` and its by-id twin
     `002639E0` (each strips bit 14 of the actor's `+0x102` name id, queries the bit, and passes
     `(id, flag)` to `003EAC10` — the bit selects the second string of name pair `id`), the two
     name-source readers `002B9C70`/~~`002BA548`~~ `002BA530` (`002BA548` is an instruction inside it) *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V4, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*, and script accessor `0034E980`; `SetBank2048`
     `0032ABF0` has three — the message-window opener `002E16B0` (`SetBank2048(actor +0x102, 1)`)
     and script accessors `0034DFA0`/`0034E320`. The index space is the NPC-name dictionary's —
     which is why it needs 2,048 bits.
   - `Bank64A`/`Bank64B` **do** have no engine consumer — proven, not asserted: the complete
     caller set is the six `shutoral*` verb result-callbacks `0x2F8`–`0x2FD` (§14 `DX-1`), and
     zero authored call sites for those verbs exist across the 1,114 decoded `us` scripts. They
     are script-facing storage for a verb family shipped scripts never invoke.
2. The 32-byte gap at `+0x1394`–`+0x13B3`, 256 flags' worth, no accessor by either route. `AA-5`.
   **DISPOSITIONED 2026-09-21 (SWE2-CONTRACT) — dead space by all three access routes.** The
   payload lives at the fixed address `02164280 + 0x200 = 02164480` (`SaveImage_GetActiveBuffer`
   is `lea rax, [02164280]`, not a pointer load), so the gap is absolute `02165814`–`02165833`.
   Operand-level census of all `call 002EF2B0`/`call 002EF640`/`call 002EF2D0` sites (163 calls
   in ~~104~~ 98 functions *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V13, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*): zero mem operands with a displacement in `0x1394`–`0x13B3`
   (payload-relative) or `0x1594`–`0x15B3` (buffer-relative); zero rip-relative operands resolve
   anywhere into the payload at all — every access is helper-mediated. No `lea` forms a pointer
   into the range, so indexed access is excluded too. The bytes exist only to be zeroed by the
   `0x1538` memset — reserved/unused space between `Bank64B` and `Bank2048`, not a bank.
3. The payload's last four bytes at `+0x1534`. Extent closed, meaning unknown. `AA-8`.
   **ANSWERED 2026-09-21 (SWE2-CONTRACT) — one byte is the saved music-override id, one is a
   second written byte, two are untouched tail.** Full census of all three access routes:
   - `+0x1534` — **the saved music-override id**, gated by `+0x1063` bit `0x40` (the pairing
     [how-the-music-changes-when-you-change-area](../18-Audio/how-the-music-changes-when-you-change-area.md)
     names: when the bit is set the track comes from `+0x1534` and the field-to-track map is
     skipped). Six accessors, every one `call 002EF2B0` then `[rax+0x1534]` beside a `+0x1063`
     bit-`0x40` test or update: readers `0025DBB6` / `00262029` / `0026DE41` (`movzx` → arg of
     `003EAA70`, the music-id resolver); writers `00262A76` (`bpl`, which is zero there, so this writer clears the byte, as [the flag-bank page](persistent-flag-banks.md) says *(clarified 2026-10-02, FABLE, on OPUS's byte verdict C-V12, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*), `0026A73D` (`0`, beside
     `and +0x1063, 0xBF`), `0026A75B` (`bl`, beside `or +0x1063, 0x40`).
   - `+0x1535` — a second byte: sole writer `002EF370` (~~`buffer+0x1735 = cl`~~ `buffer+0x1735 = bl`, its first argument), ~~whose only caller
     is the session-counter function at `002DDB4A` (writes `bl` after updating the `0215E6E0`
     word counters)~~. No reader found in the census.
     *Corrected 2026-09-26 (FABLE, Claude Opus 5.5), AA-8: there are two callers.* The session-counter
     function reaches it at `002DDB4A` with `bl` = the constant 1 (`mov ebx, 1` at `002DDAC4`, on every path). The
     script verb `0x20D1` `debug_setscreenmode` tail-jumps to it with the popped integer (`0050D192`). An image-wide
     census confirms no reader at any width
     ([flag banks §7, AA-8](persistent-flag-banks.md)).
   - `+0x1536`, `+0x1537` — **no access by any route** (the only `0x1536`/`0x1735` dword
     coincidences in `.text` are immediates in unrelated instructions). True tail padding.
4. Which ids the two shipped lists carry. `DS-1`. **ANSWERED 2026-09-21 (SWE2-CONTRACT),
   both files decoded.** `mapjumpgroupinit.bin` (`FLAGDEF1`, 116 B, u16 count **53** at `+8`,
   entries from `+0x0A`): **`0x0000` first** — *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 306; the shipped file re-decoded.)* — then `0x0056`, `0x0065`, `0x0066`, `0x0070`, `0x0079`, `0x007A`, `0x0080`,
   `0x00FC`, `0x0108`, `0x010B`, `0x010C`, `0x011C`, `0x012C`–`0x0134` (nine consecutive),
   `0x0136`, `0x0137`, `0x013A`–`0x0155` (twenty-eight consecutive), `0x0158` — ~~all inside
   `SetPrimary`'s accepted range `2..0x1FF`~~ **52 of the 53 inside** `SetPrimary`'s accepted range `2..0x1FF`.
   The leading `0x0000` is dropped by its `id − 2 > 0x1FD` (unsigned) bound, so `00379160` feeding each to
   `SetPrimary(id, 1)` sets **52** Primary bits at new game. That is the figure
   [the persistent-flag-banks page](persistent-flag-banks.md)'s DS-1 answer already gives. `eventmemorylist.bin` (`EVMEMLST`, 26 B, count **8**):
   `0x0000`, `0x0031`, `0x029C`, `0x029E`, `0x030E`, `0x0367`, `0x0368`, `0x0390` — and its
   consumer is **not** a setter loop but the membership predicate `00377440` (returns 0 when
   the queried id is listed), so the list is a denylist-shaped lookup; id `0x0000` in it is a
   real entry even though `SetPrimary`'s `id-2u` bound would reject it — it never reaches
   `SetPrimary`.
5. Whether any authored path can pass a negative id to a `Bank64` accessor. `DX-1`.
   **ANSWERED 2026-09-21 (SWE2-CONTRACT) — the hazard is real, and no shipped authored path
   exists.** The complete caller set into the four accessors is six verb result-callbacks
   (operand-level census over all 38,161 bodies; the edges.tsv rows naming `002EF2B0` are the
   *accessors'* own calls to the payload-base helper, not inbound edges): `0032AC70` ←
   `0034CA20`/`0034D190`, `0032ACF0` ← `0034CD40`/`0034D600`, `0032A9A0` ← `0034D940`,
   `0032AA00` ← `0034DDB0` — verbs `0x2F8`–`0x2FD` (`isshutoralappear`, `clear-`, `set-`,
   `isshutoralenable`, `clear-`, `set-`). Every one of the six is `call 00267E10; mov ecx,
   eax; jmp/call accessor` — the popped 32-bit value reaches the signed `cmp ecx,0x40` guard
   **unmasked**, and `PUSHII` sign-extends, so a negative id is expressible in the ISA. But
   the authored corpus never exercises it: **zero call sites for all six verbs across the
   1,114 decoded `us` scripts** (symbolic-stack census; the two raw `CALL 0x2F8` byte patterns
   in `pla_a06.ebp` sit inside the image's header/pool region, not instruction space). The
   negative-write the fixture demonstrates therefore stays a fixture-only behaviour — an
   accessor property with no shipped trigger.
6. Whether hunts and the bestiary use these banks or separate storage. `AA-7` — **neither
   `"bestiary"` nor `"hunt"` appears anywhere in the image**, so if they exist they are authored
   data, not native systems.
   **ANSWERED 2026-09-21 (SWE2-CONTRACT, folding
   [event-memory-at-actor-bind.md](event-memory-at-actor-bind.md) §3 — the halves split):**
   **hunts** are script conventions over these banks — no native hunt system exists; **the
   bestiary is native and separate** — the Clan Primer's monster records live in a 512-byte
   sighting/defeat block at save payload `+0xB404`, keyed by the `.ard` class row's word `+0x52`
   (Clan Primer entry id, 0–376). The "neither appears in the image" clause is correct as far as
   it goes but was the refuted half's residue: no string says "bestiary" because the code keys
   it by number, not because the storage is absent.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| ~~six~~ five banks (six accessor families), offsets and sizes *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V1, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))* | both routes to the payload censused — through `002EF2B0` and through the raw buffer, 36 displacements, none in the `AA-5` gap | 1 | PROVEN |
| the two routes, re-counted here | **`002EF2B0`: 121 `E8` call sites, 0 `E9`. `002EF640`: 40 `E8`, 0 `E9`.** Controls positive for both instruments | 1 | PROVEN |
| payload is `0x1538` bytes | `mov r8d, 0x1538` at `002EF2DB` feeding `memset` | 1 | PROVEN |
| bit arithmetic identical in all six | read from each accessor body — the signed-division idiom `cdq`/`sar …,3` sits at `0032A94E`/`0032A960`, `0032A9B7`/`0032A9C9`, `0032AA17`/`0032AA29`, `0032AA7E`/`0032AA90`, `0032AAF2`/`0032AB04`, `0032AB78`/`0032AB8F`, `0032AC06`/`0032AC1D`, `0032AC83`/`0032AC9A`, `0032AD03`/`0032AD1A`, `0032AD86`/`0032AD9D`, `0032AE0A`/`0032AE21` across the eleven accessors | 1 | PROVEN |
| encoded id: bit 14 selects, 0/1 hardwired | `0032A8A0` body; `bt ecx, 0xE`. **Differentially tested 2026-09-08** as op 11: **87 encoded ids × 3 payloads = 261 comparisons, 0 mismatches**, with **42 of the 87 carrying bit 14** so both arms are taken. Also read from the body: `id >= 0x200` fails closed, and the fall-through is bit `id & 7` of `payload[0x14F4 + (id >> 3)]` — the Primary bank | 1 | PROVEN |
| the schedule is a parity | `00377970` body, toggling on each entry, bit 15 terminal | 1 | PROVEN |
| new game applies an authored list | `002EF2D0` memset + tail-jump to `00379160` | 1 | PROVEN |
| the two shipped files and their sizes | path array with two controls; all twelve `FileSizeTable_*.fst` agree | 1 (corpus) | PROVEN |
| the two shipped lists' ids — `mapjumpgroupinit.bin` carries 53: `0x0000`, then 52 ids `0x0056`–`0x0158` in `SetPrimary` range, so 52 are set *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 306; the shipped file re-decoded.)*; `eventmemorylist.bin` carries 8 including `0x0000`, consumed by membership predicate `00377440`, not a setter | both files decoded: `FLAGDEF1`+u16 count 53 at `+8`, entries `+0x0A` → `00379160`→`SetPrimary(id,1)`; `EVMEMLST`+count 8 → `00377440` returns 0 on membership (§14 `DS-1`, 2026-09-21) | 1 (corpus + static) | PROVEN |
| four `Bank64` accessors accept negatives | signed `jl`/`jge` with no `js` — `0032A9A4`/`0032A9A7`, `0032AA04`/`0032AA07`, `0032AC77`/`0032AC7A`, `0032ACF7`/`0032ACFA` — against seven siblings that reject by `js` (`0032A945`, `0032AA75`, `0032AAE5`) or unsigned compares (~~`0032A8C6`,~~ `0032AB6F`, `0032ABFD`, `0032AD7D`, `0032ADFD`; `0032A8C6` is the gate's own `jb` after `cmp edi, 0x200`, not a sibling's bound test *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V6, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*) | 1 | PROVEN |
| a negative id writes before the bank | `movsxd rcx, edi` then `or byte [rax+rcx+0x1384], bl` | 1 (static) | VERY HIGH |
| the only paths into a `Bank64` accessor are six verb result-callbacks (verbs `0x2F8`–`0x2FD`), each passing a raw `00267E10` pop unmasked — and zero authored call sites for all six verbs exist across 1,114 decoded scripts | operand-level caller census over all 38,161 bodies (`0032AC70`←`0034CA20`/`0034D190`, `0032ACF0`←`0034CD40`/`0034D600`, `0032A9A0`←`0034D940`, `0032AA00`←`0034DDB0`); handler bodies are `call 00267E10; mov ecx,eax; jmp accessor`; symbolic-stack authored census zero hits (§14 `DX-1`, 2026-09-21) | 1 (static + corpus) | PROVEN |
| the `+0x1394`–`+0x13B3` gap has no accessor by any route, and `+0x1534` is the saved music-override id (gated by `+0x1063` bit `0x40`), `+0x1535` is a written-only byte, `+0x1536`/`+0x1537` are untouched tail | payload base is static `02164280+0x200` (`002EF640` is `lea`); operand census over all 163 helper-call sites in ~~104~~ 98 functions *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V13, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))* — zero disps in `0x1394`–`0x13B3`/`0x1594`–`0x15B3`, zero rip-rel operands into the payload, no `lea` into the gap; six `+0x1534` accessors all `call 002EF2B0`-mediated and paired with `+0x1063` bit `0x40` (§14 items 2–3, 2026-09-21) | 1 (static) | PROVEN |
| `Bank2048` is the NPC-name-reveal bank with real engine consumers; `Bank64A`/`Bank64B` are script-facing only (six `shutoral*` verb callbacks, zero authored call sites); hunts are script conventions over these banks while the bestiary is a separate native 512-byte block at payload `+0xB404` keyed by class row `+0x52` | E8/E9 rel32 sweep of `.text` — `0032A930`: 7 sites in `00263990`/`002639E0`/`002B9C70`/~~`002BA548`~~`002BA530` *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V4, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*/`0034E980`; `0032ABF0`: 3 sites in `002E16B0`/`0034DFA0`/`0034E320`; Bank64 callers exactly the six verbs (§14 `DX-1`); sibling-page answers folded (§14 items 1 and 6, 2026-09-21) | 1 (static + corpus) | PROVEN |
| any runtime observation | **none exists** | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### The eleven accessors, every bound test read from its own body

§10's table was re-derived by disassembling all eleven and, for each, taking the first `cmp` followed
by a conditional branch and scanning the **whole** body for a `js`:

| accessor | bound test | branch | `js`? | negative id |
|---|---|---|---|---|
| `QueryBank2048` | `cmp ecx, 0x800` | `jl` signed | **yes** | rejected |
| `QueryBank512Low` | `cmp ecx, 0x100` | `jl` signed | **yes** | rejected |
| `QueryBank512High` | `cmp ecx, 0x100` | `jl` signed | **yes** | rejected |
| `SetPrimary` | `cmp eax, 0x1FD` | `ja` **unsigned** | no | rejected |
| `SetBank2048` | `cmp ecx, 0x7FF` | `ja` **unsigned** | no | rejected |
| `SetBank512Low` | `cmp ecx, 0xFF` | `ja` **unsigned** | no | rejected |
| `SetBank512High` | `cmp ecx, 0xFF` | `ja` **unsigned** | no | rejected |
| **`QueryBank64A`** | `cmp ecx, 0x40` | `jl` signed | **no** | **ACCEPTED** |
| **`QueryBank64B`** | `cmp ecx, 0x40` | `jl` signed | **no** | **ACCEPTED** |
| **`SetBank64A`** | `cmp ecx, 0x40` | `jge` signed | **no** | **ACCEPTED** |
| **`SetBank64B`** | `cmp ecx, 0x40` | `jge` signed | **no** | **ACCEPTED** |

**Four accepted, seven rejected** — and the seven split exactly as §10 says: **three** by an added
`js`, **four** by an unsigned compare. Every constant matches too.

> **This is what a negative claim with controls looks like when it holds.** "These four let a
> negative through" is only worth something beside the seven that do not, *and* beside the fact that
> the seven use **two different** mechanisms — so the four are not merely missing one guard, they are
> the only members of the family that chose the signed comparison without the sign test.

### The two call-site censuses, and a cross-contract corroboration

| | E8 `call` | E9 `jmp` | functions |
|---|---:|---:|---:|
| `002EF2B0` | **121** | **0** | 70 |
| `002EF640` | **40** | **0** | 28 |

Both counts reproduce exactly, including the **zero** tail-jumps — which matters, because counting
only `call` has silently dropped tail-`jmp` users elsewhere in this database, and here there are none
to drop.

> **`002EF2B0`'s 70 functions is the same figure this sweep derived independently** while auditing
> `CONTRACT-battle-target-buffer`, where `002EF2B0` appears as that document's *positive control*.
> Two contracts, two purposes, one number.

`002EF2DB mov r8d, 0x1538` confirms the payload size.

**Not claimed:** nothing here is a runtime observation, and *whether any caller actually passes a
negative id* remains `UNKNOWN` — the accessors' willingness to accept one is established; a caller
that does is not.

## 16. Parity plan

**Testable now, statically:** `STRUCTURAL` (payload layout vs `_types/`), `CALCULATION` (bit
address for every id in every bank; the encoded-gate decode; the schedule parity over a synthetic
threshold list; the Primary bound).

**Requires the running game:** `STATE-TRANSITION` (does a story beat set the bit we predict),
`INTEGRATION` (does a save round-trip preserve it), `PRESENTATION`.

**Will not be tested, and why:** `TIMING` — every accessor is straight-line with no time base.
`RNG` — the accessors draw none; the one RNG-fed *writer* belongs to `07-Combat-Action`.

> **A parity claim covering only the first group must say so.** Reproducing the bit address for all
> 4,096 ids proves the arithmetic and says nothing about whether the right bit is set when Vaan
> leaves Rabanastre.

## 17. All eleven bank accessors reimplemented and differential-tested — 2026-09-08

**Reconstruction:** [`../../../Reconstruction/Game/Story/flag_banks.c`](../../../Reconstruction/Game/Story/flag_banks.c)
**Test:** [`../../../Reconstruction/Tests/Differential/diff_flag_banks.py`](../../../Reconstruction/Tests/Differential/diff_flag_banks.py)

| | |
|---|---:|
| operations covered | **all 11 bank accessors** — 5 queries, 6 setters |
| ids | 153, of which **67 negative** |
| cases | 2,601 |
| payloads | 3 — all-zero, all-ones, pseudo-random |
| **comparisons** | **7,803** |
| **mismatches** | **0** |

> **It began as four and was completed to eleven on 2026-09-08**, because
> [the parity standard](../../../Reconstruction/PARITY-STANDARD.md)'s `FULL-SUBSYSTEM`
> criterion asks for every entry point of a subsystem, and a family missing seven of its
> eleven members cannot meet it. **Every bound test was re-read from the shipped bytes** for
> the seven new ones rather than copied from §10's table — and §10's table survived the
> re-reading exactly, while **its prose about where a negative write lands did not**.
>
> **`FULL-SUBSYSTEM` is still not covered, and now says by how much:** 11 of the **17** entry
> points this contract enumerates. The six outstanding are the authored gate (`0032A8A0`,
> partially reconstructed — its schedule arm needs authored data), the threshold schedule
> (`00377970`), the new-game list (`00379160`), the reset (`002EF2D0`), the event-memory
> predicate (`00377440`) and the payload-base helper (`002EF2B0`, executed as shipped on the
> reference side rather than reimplemented).

### What completing the family found

**`SetBank64B`'s negative ids do not land where `SetBank64A`'s do.** §10 generalised one
accessor's landing zone to all four, and eight of `64B`'s writes go **into `Bank64A`** — a
bank with its own readers. The correction is in §10 with the eight ids named. **It could not
have been found without running the second member of the pair.**

**The reference side runs three real functions, not one.** The accessors reach the payload
through `SaveImage_GetPersistentPayloadBase` (`002EF2B0`) and `SaveImage_GetActiveBuffer`
(`002EF640`); both are mapped and executed **as shipped**, and the harness simply puts its
payload at the address `002EF640` returns. **No stub is used anywhere in this test.**

### Three payloads, because one hides half the behaviour

A first run used one random payload and reported *“no byte changed”* for cases that had
plainly written: **an `or` that sets an already-set bit changes nothing**, and an `and` that
clears an already-clear bit changes nothing. A comparison of resulting memory cannot see a
no-op write. So every case runs three times — all-zero makes every `set(id, 1)` visible,
all-ones makes every `set(id, 0)` visible, pseudo-random is the mixed case.

**39 effective writes per value, and the symmetry is the check:** `SetPrimary` accepts 17 of
153 ids (all non-negative) and all 17 have a non-zero mask; `SetBank64A` accepts 77 and only
22 have one. The zero and ones passes report the same 39 because each id appears once with
each value — **a symmetry, and its absence would have been the bug.**

### Parity status, for these four operations only

`CALCULATION` and `STRUCTURAL` **pass**, over the id set above. `STATE-TRANSITION`,
`INTEGRATION`, `TIMING` and `PRESENTATION` are **untested and require the running game**.

> **The subsystem's readiness does not move.** Four of the seventeen entries are covered, over
> a synthetic payload, on a machine that never rendered a frame. `§13` is still empty and this
> contract is still `CONTRACT READY`. **A green differential test proves the algorithm, not
> the outcome.**

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings are recorded in the registry, not here.*

- **PlatformOnlineAchievements — CLIENT.** `FieldData_GetVariable0` (`00265270`) is read by two achievement-side
  bodies of 308 and 367 bytes. Both also call `00315420`, and the 367-byte body resolves the save buffer. **Two
  achievement-side bodies read a field variable.** Which achievements they serve is not read.
- **Audio — CLIENT, not read.** The 335-byte Audio-filed body calls `SaveImage_GetPersistentPayloadBase` (`002EF2B0`)
  and the field id.
- **ActorEntity - CLIENT (10 edges).** `00263990` is also called by bodies filed to ActorEntity: `0025C230`, `0025C830`, `00268D10` - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - CLIENT (2 edges).** `0032AA60`, `0032AD70` are also called by bodies filed to combat action: `002FA740`, `002F8060` - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT (2 edges).** `00265270`, `0032A8A0` are also called by bodies filed to input: `00253C70` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (5 edges).** `001EC560`, `00263990`, `002639E0` are also called by bodies filed to presentation: `001EDBB0` (Cutscene), `001F9B20`, `002B0280` (Rendering) - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (4 edges).** `00265270` is also called by bodies filed to resource: `001DA220`, `001DA970`; `00378540` reaches bodies filed to resource: `0032E400`, `0032E620` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (35 edges).** `002E16B0` is also called by bodies filed to script VM / native bridge: `0033F950`, `00348DF0`, `0034ADA0` - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CoreRuntimeScheduling — CLIENT.** `FUN_001ec760`, owned by that layer, calls `00265270` on this page. That caller is a 2,232-byte body behind the same `[01F82E38]` gate and the same `001EC560` predicate as the cutscene-override table, and it does nothing at all when either refuses; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (2 edges, one fan-in).** All 2 edges are UI bodies reaching `0032A8A0` on this page. `FUN_0029c530` is the worked example - it is a 569-byte message handler whose dispatch is a **descending chain of subtractions** - 1, 1, 1, then `0xB` - rather than a jump table, so the message ids it answers are 1, 2, 3 and 0xE. The crossing is **one shared subject with 2 callers on that layer**, not 2 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

## The `0032A8A0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0032A8A0` (`PersistentFlag_QueryPrimaryOrAuthoredThresholdGate`, ~~~127 B~~ 122 B, `0032A8A0`-`0032A919` `ret` *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V3, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*)
— `edi = ecx & 0x3FFF`; `bt ecx, 0xE` selects the authored gate
(`0032A8A8`/`0032A8AE`).

| member | role | interior |
| --- | --- | --- |
| `00377970` | `qword[02ADD0C8]` non-null walk (`00377976`/`00377982`) | [`00377976`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../_index/candidates/fable-home-contract-persistent-flag-banks-1002/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `002A3210` | 51 B | `002E16B0` + 0x2D7 | replaces bit 18 of dword `rcx+0x180` with bit 0 of `r9d` and sets its bit 17 (`bts`), stores `dl` at byte `rcx+0x174` and `r8b` at byte `rcx+0x175`, and writes the dword back | Interior anchor `002A321B`; Interior anchor `002A3222`; Interior anchor `002A322F`; Interior anchor `002A3234`; Interior anchor `002A323B` |
