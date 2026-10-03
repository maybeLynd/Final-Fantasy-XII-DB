---
contract: unlock a bazaar good from loot sold, sell it once, and decide whether it ever comes back
category: 12-Items-Equipment-Shops-License
scope: family
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 12-Items-Equipment-Shops-License/the-bazaar-recipe-unlock-and-purchase.md
entries: ["0030B1D0", "0030B33F", "0030B570", "003008A0", "003108ED"]  # <- corrected 2026-10-02, OPUS: per section 2, 0030B1D0 is 0x50 into the purchase entry 0030B180 and 0030B33F is the loop body of the refresh entry 0030B270; 003108ED is the refresh call site inside the sale commit 00310870
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 49 addresses cited - 3 data, 8 entry, 38 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-bazaar-unlock-and-purchase-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the bazaar unlock and purchase

A bazaar good becomes available when enough of three specific loots has been sold, and buying it
takes the availability away again. Whether it can ever come back is decided by **two bits and where
they are stored**, and that is the question this contract exists to settle.

The first contract in `12-Items-Equipment-Shops-License`.

## 1. Purpose

To state the unlock predicate, what a purchase consumes, and — because the team has the question open
as **FZ-3** — whether a one-time good survives a save and reload. **§7 answers FZ-3 from containment
arithmetic rather than observation**, and §13 names the one assumption that leaves.

## 2. Interface

| | |
|---|---|
| refresh availability | **`0030B270`**, called only from ~~`BattleIdClassD_RefreshPrerequisiteRuntimeFlags`~~ the sale commit `Shop_CommitSaleItemAndGil` (`00310870`), at `003108ED`. *(corrected 2026-10-02, OPUS: `retool.py callers 0030B270`; `0030B270` is itself `BattleIdClassD_RefreshPrerequisiteRuntimeFlags`, the-bazaar-recipe-unlock-and-purchase.md §2.3–§2.4)* `0030B33F` is the loop BODY, not the entry |
| purchase | **`0030B180`** — `rcx` = the encoded good id. This row said `0030B1D0`, which is `0x50` into the body: past the prologue, past the gate and past the state-pointer setup. Corrected 2026-09-12 by execution |
| script-set availability | `0030B570`, reached through `0032AB50(good, bool)` |
| zero a loot tally | `003008A0(loot, 0, absolute = 1, 3)` |

## 3. Types

| | |
|---|---|
| the goods table | registry slot `02EBF058`; row index is **`id - 0xD000`** (`0030B1F4`), the category-13 base |
| the good's flag byte | `BattleSystemState + 0x59C8 + row` |
| the loot's sold tally | one byte per loot id in the loot class's region B of the same block |

**The flag byte's three bits**: bit 0 *unlocked at least once*, bit 1 *available now*, bit 2 read by
the shop UI's own record.

**And both of those live inside the save payload.** `BattleSystemState` is a declared sub-object of
`SavePayload` at `+0x4E48C`, so the flag byte is at payload `+0x53E54 + row` — `0x4E48C + 0x59C8`
computed, and it matches what the referenced page states independently. The 128 rows end at
`+0x53ED4`, well inside the payload's `0x56490`. §7 turns on this. *(**Size corrected 2026-09-21 (OPUS)**, from `0x564D0`, an overstatement of exactly `0x40`. `SavePayload`'s declared size is `0x56490` in `_types/types.tsv` and the bazaar system page already flagged this figure as mine to fix. **The containment this section turns on is unaffected**: `0x53ED4 < 0x56490`, so the offset is inside the payload under the corrected size as well - which is why this is a wrong number rather than a wrong conclusion. Consumed from `ASTRA-RETURN-OPUS-CONTRACT-LIVE-REUSE`.)*

## 4. Preconditions · postconditions · invariants

**Refresh, `0030B270` — re-derived and executed 2026-09-12.** The loop reads the row count from
the registry's `+0x04`, and for each row builds the goods row at index `i & 0xFFF` and the flag
byte at `[02EBF190] + i + 0x59C8`. The predicate has **four** clauses, each of which alone
rejects:

1. **not repeatable AND already unlocked** — `row[+0x14] & 1` against the flag's bit 0
   (`0030B33F`–`0030B34C`);
2. **already available** — the flag's bit 1 (`0030B352`);
3. **all three thresholds are zero** — `row[+0x18]`, `+0x1C`, `+0x20` (`0030B35F`–`0030B36F`).
   **A row that requires nothing is REJECTED, not granted**, which is the clause a reading of
   the prose does not produce;
4. **any loot's tally below its threshold**, the tally being `-1` for the `0xFFFF` sentinel or
   an id outside the class window, `0` for an out-of-range index or a class record with no
   handler, and otherwise the handler's answer.

All four passed: `flag |= 3` (`0030B461`) — **both bits at once**.

The first two loots are queried by inlined copies of `0030ADC0` and the third by a call to it.
**The call passes `0` in `edx` where the inlined copies pass `3`, and it makes no difference**:
`0030AE1A` overwrites `edx` with `3` before the tail jump, so the second parameter is dead.

The older summary of this predicate, cited rather than re-derived, read: the row is repeatable **or** has never been
unlocked; availability is not already set; the row has a recipe; and each of the three required
loots' sold tallies meets its threshold. All met → `flag |= 3`.

**The invariant that matters: bit 0 is never cleared anywhere in this family.** The purchase clears
bit 1 alone — `and byte ptr [rsi + 0x59c8], 0xfd` at `0030B203`, and `0xFD` is `~0x02`.

## 5. State

Read and written: the good's flag byte and the three loots' sold tallies, both inside
`BattleSystemState` and therefore inside the save payload. The goods table is authored and never
written.

## 6. Relationships

- **Upstream:** selling loot moves the tallies; `0032AB50` lets a script set availability directly,
  but only for rows whose `+0x14` bit 1 permits it — the seven Grimoires, which have no recipe.
- **Downstream:** the shop UI reads bit 2.

## 7. State transitions — and FZ-3

**Purchase**, `0030B180`:

0. **`00322C50(0x12, id, 0)` — and a zero answer returns 0 having touched nothing**
   (`0030B18A`–`0030B1A1`). The first argument is the BAZAAR CLASS NUMBER, the same `0x12`
   the class-record array carries for nibble 13. **This step was missing from this section.**
1. the state byte is **derived here, not passed in**: `[02EBF190] + (id & 0xFFF)`
   (`0030B1B3`–`0030B1C1`);
2. resolve the goods row from registry slot `02EBF058` at index `id - 0xD000` on the
   ZERO-EXTENDED 16-bit id (`0030B1CD`–`0030B1FD`); on any resolution failure the row pointer
   becomes NULL (`0030B201`) and the code continues — **into three reads of that NULL**, at
   `+0x16`, `+0x1A` and `+0x1E`. Nothing tests it. See §10;
3. `flag &= ~2` — **bit 0 survives** (`0030B203`);
4. for each of the three recipe loots: `003008A0(loot, 0, 1, 3)`, writing the sold tally to
   **absolute zero** (`0030B20C`–`0030B220` and the two that follow);
5. return 1.

**Corrected 2026-09-12 by execution.** Steps 0 and 1 were absent and the entry address was
`0x50` too high. A reconstruction built from the old step list — no gate, the state passed in —
differs from the shipped code on 140 of the suite's 215 lines.

**So a purchase leaves the good in the state: unlocked-once yes, available no, tallies zero.**

**FZ-3 — does a one-time good come back after a save and reload?** No, and the reason is arithmetic
rather than observation:

- both the flag byte and the tallies are inside `BattleSystemState`, which is a declared sub-object of
  `SavePayload` (§3), so **both are written to the save file and restored from it**;
- ~~on reload, refresh runs over every row.~~ on reload nothing recomputes the flag bytes: refresh `0030B270` has one caller, the sale commit `00310870` at `003108ED`, so it runs only after a sale and the loaded bytes stand *(corrected 2026-10-02, OPUS: checked by `retool.py callers 0030B270`; the-bazaar-recipe-unlock-and-purchase.md §2.3)*. When a later sale runs it: For a row that is **not** repeatable, the first clause of
  its predicate — *repeatable or never unlocked* — is false, because bit 0 survived the purchase.
  The row is rejected before any tally is consulted;
- and even for a repeatable row, the three tallies were zeroed, so the thresholds must be earned
  again.

**The two mechanisms are independent and either alone would suffice**, which is what makes the answer
robust to one of them being misread.

**Script-set availability**, `0030B570`: writes bit 1 from a boolean **only when the row's `+0x14`
bit 1 is set** (`0030B5F6`–`0030B619`). It does not consult bit 0, so a script can make a
never-unlocked good available.

## 8. Script · resource · event interactions

The goods table is authored, reached through the registry like the other authored tables. The
script entry is `0032AB50`, gated per row as above.

## 9. Determinism

Fully deterministic given the state block.

## 10. Failure paths and edge conditions

**All three entry points reach a NULL goods row and none of them tests it.** When the registry
pointer at `02EBF058` is null, or the reference at its `+0x0C` resolves to zero, the row
register is zeroed (`0030B201`, `0030B333`, `0030B5F4`) and the code reads on: purchase reads
`+0x16`, `+0x1A`, `+0x1E` of it, refresh reads `+0x14`, and the script path reads `+0x14`.
**Executed 2026-09-12** with a page planted at address zero so the two sides could be compared:
they compute the same addresses and read the same bytes. **The shipped process has nothing
mapped at zero**, so what that establishes is the arithmetic, not that the path survives.
This is the same class as `OPUS-NOTICE-REWARDNULL` and the preparation family's row lookup.

- **A failed row resolution does not abort the purchase.** `0030B201` sets the row pointer to zero
  and execution continues to `0030B203`, which clears the flag bit anyway, and then to
  `0030B20C`, which reads the recipe loot ids **through that null pointer**. The bit clear happens
  before the reads, so a purchase with an unresolvable row still consumes availability.
- **A repeatable row's purchase is silent about repeatability**: bit 0 is set on both kinds and only
  the predicate distinguishes them.
- Nothing reports a failure at any point in this family.

## 11. Observable behaviour

~~Not established.~~ *(answered in part: see the-bazaar-recipe-unlock-and-purchase.md §7, FZ-3 — an older `FFXII_004` loaded in a live process brought both regions back full, 18 nonzero flag bytes and 44 nonzero loot-sold counters, each matching the file's decoding (ASTRA, 2026-09-21); the purchase round trip below is still unobserved; 2026-10-02, OPUS)* What would be observable: a one-time good bought, then a save and reload, and the
good still gone — which is FZ-3 read directly rather than derived.

## 12. Reproduction formula

```c
void Bazaar_Purchase(uint16_t goodId)   // <- corrected 2026-10-02, OPUS: returns int; section 7 step 0 is missing here - if (!00322C50(0x12, goodId, 0)) return 0; before anything is touched (0030B194-0030B19F)
{
    Row *row = goods_row(goodId);              /* 02EBF058, index goodId - 0xD000 */
    state->goodFlags[row_index] &= ~2;         /* 0030B203 - bit 0 SURVIVES */
    SetLootSoldTally(row->loot0, 0, 1, 3);     /* 003008A0 */
    SetLootSoldTally(row->loot1, 0, 1, 3);
    SetLootSoldTally(row->loot2, 0, 1, 3);
}
```

## 13. Runtime validation

**Executed 2026-09-12 as the twenty-ninth differential pilot (`OPUS-BAZAAR-ISOLATED`). Evidence
class: isolated original-code. Not observed in a running game, and nothing below claims otherwise.**

`Reconstruction/Tests/Differential/diff_bazaar.py` runs all three entry points as shipped bytes
under Unicorn at their real virtual addresses — `0030B180` purchase, `0030B270` refresh, `0030B570`
script-set, and `0030ADC0`, the out-of-line tally query the third loot uses — against
`Reconstruction/Game/Items/bazaar.c`, built by MSVC at `/W4 /O2`. `0020E600` runs for real. Three
callees are oracles: the class record's own handler at `+0x50`, the tally write `003008A0`, and the
gate `00322C50`; every call to each is compared as a trace line, so an argument that changed would
fail even where no state does.

    diff_bazaar      : 297 compared lines, 0 mismatches, 107 flag-byte images,
                       29 rows accepted by the predicate, 76 oracle calls traced
    negative controls: eight, each a plausible misreading and three of them this contract's own
                       wording - a row with no thresholds granted (1 line); refresh raising
                       availability alone (133); purchase clearing both bits (126); purchase with
                       no gate, as section 7 described it (140); an unsigned bounds compare (1);
                       the class window closed with >= (1); the script path consulting bit 0 (1);
                       a tally equal to its threshold refused (13)
    mutation campaign: 75 mutants, 68 KILLED, 4 SURVIVED, 3 EQUIVALENT,
                       inputs stable and hashes re-checked

**Four things the run corrected, all of them found by reading the bytes the fixture needed rather
than by the fixture itself**, and all now carried in §2, §7 and §10: the purchase entry is
`0030B180` and not `0030B1D0`; it is **gated** by `00322C50(0x12, id, 0)` before anything else, a
step §7 did not have; its state byte is derived inside the function rather than passed in; and the
third loot's `xor edx, edx` is a dead store, because `0030ADC0` overwrites that register with `3`
before its tail jump. **The gate was worth 140 of 215 lines** — a reconstruction built from §7 as
written disagreed with the shipped code on two thirds of the suite.

**The predicate is re-derived here rather than cited.** §7 previously quoted it from another page,
with "has a recipe" as its third clause. What the code tests is that **not all three threshold
bytes are zero**, and a row that requires nothing is **rejected**. That is the one clause a reading
of the prose does not produce, and the control for it fails on exactly one line — the single case
built for it.

**Four campaigns, and each round found a different KIND of gap.**

**Round one left thirteen survivors, eleven of them one shape**: the row helper's own guards, none
of which the fixture could reach. A null registry is unreachable from refresh — it reads its row
count from that registry first and finds zero, so the loop never runs — and the fixture had never
sent purchase or the script path there. The first of the two resolves feeds only the null test, so
its offset is invisible unless `+0x0C` is zero while `+0x0D` is not. And `base == 0` returning 0 is
indistinguishable from falling through whenever the row index is zero. Cases for each close them.

**Round two left seven, and five of those were a defect in the HARNESS, not in the fixture.** The
driver planted its flag bytes and class records through the reconstruction's own macros, so a
mutation to `BZ_FLAG_BASE`, `BZ_CLASS_STRIDE` or `BZ_CLASS_HANDLER` moved the plant and the read
together and the offset under test became invisible. Every other driver in this suite carries the
comment *"deliberately literal, not the header's constants"*; this one did not, and the campaign is
what noticed. **An instrument that shares the subject's constants cannot measure them.**

**Round three left one more of the same family, and it needed the fixture's VALUE narrowed rather
than its offsets.** The handler pointer was planted as `0x1234ABCD`; read one byte off it still
found non-zero bytes and still looked like a handler. Planted as `0xCD` - one non-zero byte, the
lowest - an offset of `+0x51` reads zero and the difference is visible. **A wide fixture value can
hide an offset as effectively as a shared constant.**

**What survives is equivalent, by argument rather than by `/Brepro`.**

- `return -1` → `return -2`, twice. The tally query's refusals are compared against a threshold read
  as an unsigned byte, so **any negative is below every threshold** and no fixture can separate one
  from another. The `-1` is a convention of the code, not a fact this predicate can observe — a
  reimplementation may return any negative here and stay correct.
- `0xE000` → `0xE001` in the class window. The tested value is `id & 0xF000`, always a multiple of
  `0x1000`, so no input lies between the two thresholds.
- `0xFFFF` → `0x10000` for the sentinel. **The sentinel test is subsumed by the window test**: an id
  of `0xFFFF` has nibble `0xF`, which is already above `0xE000`, so removing the first test changes
  no answer. That is a fact about the shipped code, not about the fixture.

**What this run does not establish.**

- **Nothing here has been observed in a running game.** The two requests below stand.
- **FZ-3's save round trip is not executed.** What runs is the arithmetic: refresh, purchase,
  refresh, for a repeatable row and a one-time row, with the one-time row not coming back. The
  claim that both the flag byte and the tallies are written to and restored from the save file is
  **containment reasoning about `BattleSystemState`, unchanged by this run**, and §13's original
  assumption — that the save path writes the payload wholesale rather than selectively — is still
  untested.
- ~~**Three callees are scripted.**~~ **Superseded 2026-09-18 by EXP-092 (§13a): all three ran as
  shipped bytes.** What remains is the fixture boundary rather than the semantics — the family
  table's `+8` and `+0x20` data pointers are runtime-null in the shipped image and were planted,
  so the ARM SELECTION and the write rules are proved while the tables' provenance is not.
- **The null-row path is agreement about a fault, not its absence.** All three entry points reach a
  zero row and none tests it; the fixture maps a page at address zero so the two sides can be
  compared, and the shipped process has nothing mapped there.

**Still wanted from a running game:**

1. Break on `0030B270` and record how often it runs and with what row count — the predicate is
   cheap, but nothing here establishes **when** it is called, and "refresh is the only thing that
   raises availability" is a claim about callers, not about this body.
2. One save-and-reload around a one-time purchase, reading the flag byte before and after. That is
   the half of FZ-3 that no offline run can reach, and it is the only observation that would turn
   the containment argument into a measurement.

Requested from ASTRA; not claimed by me.

### 13a. The three callees, executed — 2026-09-18 (OPUS, consuming SWE2-ORACLE's EXP-092)

EXP-092 ran all sixteen bodies from shipped bytes — **80/80 cases, 11/11 mutants, zero stubs**. The
`UNKNOWN` row in §15 is retired and §14's first open item is answered. **Nothing in the ten findings
contradicts a claim this contract made**, which is worth stating plainly; what they expose is that
the word *tally* was doing two jobs here.

#### The contract said "tally" where the code has TWO tables, and the queries read the other one

`002FD150` — the class record's ~~`+0x50`~~ **`+0x48` (mutate)** handler of the item classes 5–7, 720 bytes; their `+0x50` (query) slot holds `002FD8D0` (shipped table `01EEBCC0`, read 2026-09-25 by FABLE, Claude Opus 5.5, on OPUS block 301) — selects a **channel** from `r9` at
`002FD198`–`002FD1B9`, and re-reading it settles the vocabulary:

| `r9` | table | what the arm answers |
|---:|---|---|
| `0` | `u16` at `[fam+8]` | `(w & 0x3FF) - (w >> 0xA)` — low10 minus hi6 (`002FD400`–`002FD405`) |
| `1` | `u16` at `[fam+8]` | `w & 0x3FF` — low10 (`002FD37C`) |
| `2` | `u16` at `[fam+8]` | `w >> 0xA` — hi6 (`002FD2A5`) |
| **`3`** | **`byte` at `[fam+0x20] + idx`** | the byte itself (`002FD1BF`–`002FD1D3`) |

**Both the refresh predicate and the purchase write use `r9 = 3`** — they read and clear the *byte*
table, and the `u16` at `fam+8` is untouched by this path. The family record stride is `0x58`
(`002FD187 imul rsi, rax, 0x58`, indexed by `id >> 12`, with `idx = id & 0xFFF`).

#### `(loot, 0, 1, 3)` decoded, which is §14's first item

The third argument is the **absolute/relative selector** and the fourth is the **channel**. In the
byte arm, `002FD1D7 test r8d, r8d` / `cmove` makes the written value `delta` when `r8 != 0` and
`old + delta` when it is zero; the value is then floored at 0 (`002FD1E2 jns`, else write 0) and
capped at `0x63` (`002FD204 cmp ecx, 0x63`). So `(loot, 0, absolute = 1, channel = 3)` writes
**byte `[fam+0x20] + idx] = 0`**, which is exactly what "zeroed absolutely" meant.

**And the return value is a re-read, not the written value.** Every arm reloads the table pointer and
reads the cell back out — `002FD1EC`/`002FD1F0` on the byte arm — so a reimplementation that returns
the value it just computed agrees only as long as the store and the reload cannot disagree.

#### Arm 1 is the only arm with side effects, and that is not visible from the call site

The `r9 = 1` arm, and only that arm, sets a bit in a bitmap at `[fam+0x30]` and then makes two calls
(`002FD355` and, under a further gate, `002FD369`). **The bit is set only when the new value exceeds
the old low10** (`002FD31E cmp r8d, r10d` / `jle` skips it). That is the discovery half of
`Inventory_ModifyEncodedItemAndUpdateDiscoveryState`'s name, and it means **the channel argument
selects side effects as well as a table** — a caller passing `1` where it meant `3` would not merely
write the wrong cell, it would announce a discovery.

#### The clamp in arm 1 goes UP, which is the reverse of the natural reading

`002FD2E9 cmp eax, r8d` / `002FD2EC jl` — when the new low10 is **below** the hi6 field, the write
takes `hi6`; otherwise it takes `min(new, 0x63)`. A reimplementation that reads "clamp to hi6" as an
upper bound inverts it. EXP-092 states this as finding 3 and the instructions agree.

#### Accepted without re-derivation here, and marked as such

Findings 4–10 — the shared `-1` sentinel logic, the class-number indirection through `00309440`, the
live-registry arm bound, the script-set `0xD000` precondition and the `(old & ~2) | ((edx&1) << 1)`
flag update, the sequence semantics, and the two `+0x48` handlers — are consumed on EXP-092's
evidence. **They were not re-read from the image in this pass**, and that is recorded rather than
implied: the four claims above are the ones this section stands behind at tier 1.

#### What did NOT become established

The fixture disclosure is the boundary. The family table's `+8` and `+0x20` data pointers are
**runtime-null in the shipped image** and were planted, so the arm selection and the write rules are
proved while **where those tables come from is not**. §10's null-row fault stays exactly as it was:
EXP-092 reproduces it as an `expect_fault` case, which is agreement about a fault rather than a
demonstration that the path is reachable — §14's third item is untouched.

## 14. Unresolved

- ~~What `003008A0`'s third and fourth arguments (`1`, `3`) select beyond "absolute".~~ **Answered 2026-09-18 (§13a): the third is the absolute/relative selector and the fourth picks the CHANNEL — `3` is the byte table at `fam+0x20`, not the `u16` tally at `fam+8`.**
- ~~Bit 2 of the flag byte, read only by the shop UI's record.~~ **Resolved 2026-09-22
  (SWE2-CONTRACT): it is the "newly unlocked" marker, and it is written, not just read.** A
  per-body census of every `+0x59C8` displacement in the image finds the complete lifecycle:
  `BattleIdClassD_GetRuntimeFlagBit2` `0030B4B0` returns `(flag >> 2) & 1` (`0030B502`–`0030B505`);
  `BattleIdClassD_SetRuntimeFlagBit2` `0030B630` writes `(val & 1) << 2` under
  `00322C50(1, id, 1)` (`0030B67E` `and 0xFB` / `0030B686` `or bl`); the recipe-refresh
  precheck `0057B6F0` walks the entry list and marks every unmarked good (`0057B743` getter →
  `0057B752` setter with `val = 1`); the shop transaction driver `0056D370` clears it
  (`0056D4C0`, `val = 0`); and the UI record builder `0031C5D0` folds all three flag bits into
  record `+0x44` (`0031DA69`–`0031DA9D`, bit 2 via `and eax, 4`). The refresh loop
  (`0030B29B`) tests bits 0 and 1 but never bit 2 — the marker is orthogonal to availability:
  set when the precheck first sees a good, cleared when the trade panel consumes it, surfaced
  to the UI as the record's bit 2. This matches the page's naming and adds the writer census.
- ~~Whether the null-row purchase path in §10 is reachable.~~ **Bounded 2026-09-22
  (SWE2-CONTRACT).** The whole-image census of `02EBF058` finds exactly one writer — the
  relocation binder `003845F0` invoked at `00236F6E` inside `00236C30`'s registration pass,
  which stores `movsxd [parent + 0xE8]` **unconditionally** (`003845F4`). The slot is null
  only if that parent resource field was zero at bind; no clearer or second writer exists.
  The second leg is narrower than §10's phrasing: the row resolver `0020E600` is
  ~~`ref + *(01F85530)`~~ `ref + *(01F83530)` (`0020E602`) *(corrected 2026-10-02, OPUS: checked at `0020E602` `add rax, qword ptr [01F83530]`)*, so a zero `+0x0C` reference resolves to the **base**, not
  NULL — the `je 0x30B201` fires only when `ref == -base` or the base itself is zero, i.e.
  the goods resource unbound. So the null path is reachable exactly in a
  goods-resource-absent state; the three entry points don't test it because registration is
  assumed to have run. EXP-092 already proved the fault arithmetic; this bounds the trigger.
  Residual: whether the goods resource can actually be absent in a shipped playthrough is a
  load-order question outside this census.
- **FZ-3's first mechanism assumes nothing re-clears bit 0 after a load. One function in the image would.**
  *(Added 2026-09-26, OPUS.)*
  - The inventory rebase `0030B6A0` **masks all 128 flag bytes at `+0x59C8` with `0xF8`**, which clears bits 0–2. It
    also **zeroes the tallies at `+0x57C8`** (ORACLE's EXP-189 correction).
  - Its two callers each run it on a block that is reset around it:
    - the binder `00233C10`'s unbound arm, where the full reset `00237DF0` (which memsets through `002370C0`) runs
      twice AFTER the rebase (BS-2; the order corrected 2026-09-29, OPUS, `CON-171`), so the reset erases what the
      mask did;
    - `SaveRuntime_RebindImageBackedGameplayState` `00238A80`, at the tail of the save-image init `002EF650`, which
      memsets the payload first.
  - So on those two paths the mask acts on zeros.
  - ~~Not read here: whether the load path restores the saved block before or after those calls.~~ **Read the same day
    (OPUS): on a valid restored image the rebase does not run, so bit 0 survives a load.**
    - In the `0xD8` handler `00280140`, after the load-status check `00280359 call 0032E4D0`, the runtime header is
      validated: `0028036E lea rcx, [SaveImage_GetActiveRuntimeBuffer() + 0x68]`, then `00280372 call 00255260`. That
      validator accepts magic `0x0131F3EA`.
    - **A valid header** takes `00280379 jne 002803B8`. That skips the reset `002EF650`, and with it `00238A80` → `0030B6A0`.
      It calls only the binder `00233C10`, whose bound-and-magic-right arm runs neither the reset nor the rebase (BS-2).
    - **An invalid header** falls into `0028037B call 002EF650`, the memset-then-rebind, so the mask acts on zeros.
  - So FZ-3's first mechanism holds on the load path as well. *This is static; the save round trip itself is still not
    executed.* The executed arithmetic of §7 is in `../_index/candidates/s30-opus-replay-bazaar-shipped/`.

## 15. Evidence

Static, from the shipping image (`73461D08…`). The purchase was disassembled and read; the refresh
predicate and the flag-bit meanings are cited from the referenced page rather than re-derived, and
where this contract and that page overlap they agree — including `0x4E48C + 0x59C8 = 0x53E54`, which
I computed independently of its statement there.

**Claim table added 2026-09-12 (`OPUS-S15-CLAIM-TABLES-SIX`).** The prose above states the method
and is kept; this enumerates the claims so a pilot's `CONTRACT_MAP` can be derived from them.
~~**Nothing here has been executed** (§13).~~ *(answered: see §13 — the twenty-ninth differential pilot of 2026-09-12 ran the three entry points as shipped bytes, 297 lines, and the rows below marked "isolated original-code" are executed; nothing is observed live; 2026-10-02, OPUS)* Two rows are cited from the referenced page rather than
re-derived, and they say so.

| claim | evidence | tier | confidence |
|---|---|---|---|
| the goods row index is the id minus 0xD000 | `0030B1F4`, against registry slot `02EBF058` | 1 (static) | PROVEN |
| the good's flag byte is at BattleSystemState + 0x59C8 + row | the displacement in `and byte ptr [rsi + 0x59c8], 0xfd` at `0030B203` | 1 (static) | PROVEN |
| the flag byte and the sold tallies are both inside the save payload | `BattleSystemState` is a declared sub-object of `SavePayload` at `+0x4E48C`, so the flag byte is at payload `+0x53E54 + row`, computed here and matching the referenced page independently; the 128 rows end at `+0x53ED4`, inside the payload's `0x56490` *(corrected from `0x564D0` on 2026-09-21 (OPUS); the row's verdict is unchanged because `0x53ED4 < 0x56490`)* | 1 (static) | PROVEN |
| a purchase clears bit 1 and never bit 0 | `0xFD` is `~0x02`, at `0030B203`; nothing in this family clears bit 0 | 1 (static) | PROVEN |
| a purchase zeroes all three recipe loots' sold tallies absolutely | `003008A0(loot, 0, 1, 3)` for the loots at row `+0x16`, `+0x1A`, `+0x1E`, at `0030B20C`–`0030B220` and the two that follow | 1 (static) | PROVEN |
| a failed row resolution does not abort the purchase | `0030B201` sets the row pointer to zero and execution continues into the flag clear | 1 (static) | PROVEN |
| a one-time good does not return after a save and reload | two independent mechanisms, either sufficient: bit 0 survives the purchase and fails the refresh predicate's first clause, and the tallies were zeroed so the thresholds must be earned again. **The ARITHMETIC is executed 2026-09-12** - refresh, purchase, refresh in one sequence, for a repeatable row and a one-time row, and the one-time row does not come back. **The save round trip itself is not executed**: what the run shows is that the predicate rejects the state a reload would restore, which is the half this contract can prove without a game | 1 (isolated original-code) | PROVEN |
| the refresh predicate is: repeatable or never unlocked, not already available, **at least one threshold non-zero**, and three loot thresholds met | **re-derived and executed 2026-09-12**, not cited: `0030B33F`-`0030B461`, each clause driven at the point where it alone decides. The third clause said "has a recipe"; what the code tests is that not all three threshold bytes are zero, and a row that requires nothing is REJECTED - a reconstruction that granted it differs on one line of the suite, the one built for it | 1 (isolated original-code) | PROVEN |
| a script can set availability only for rows whose +0x14 bit 1 is set | `0030B5F6`–`0030B619` in `0030B570`, reached through `0032AB50` | 1 (static) | PROVEN |
| script-set availability does not consult bit 0 | the same body `0030B570` (`0030B5F6`–`0030B619`): a never-unlocked good can be made available | 1 (static) | PROVEN |
| the purchase entry is 0030B180, and it is GATED before anything else | `00322C50(0x12, id, 0)` at `0030B198`; a zero answer returns 0 having touched nothing. §2 named `0030B1D0`, which is `0x50` past this. Executed: a reconstruction without the gate differs on 140 of 215 lines | 1 (isolated original-code) | PROVEN |
| the gate's first argument is the bazaar CLASS NUMBER | `0x12`, which is also the class-record array's `+0x38` for nibble 13 - the array at `01EEBCC0`, stride `0x58`, count at `+0x3C`, handler at `+0x50`, measured 2026-09-12 and confirmed by the predicate's own `imul rdx, rax, 0x58` at `0030B3A0` | 1 (isolated original-code) | PROVEN |
| the purchase's state byte is derived inside the function, not passed in | `0030B1B3`-`0030B1C1`: `[02EBF190] + (id & 0xFFF)` | 1 (isolated original-code) | PROVEN |
| refresh raises BOTH bits at once | `0030B461 or byte, 3`. A reconstruction setting availability alone differs on 133 lines | 1 (isolated original-code) | PROVEN |
| the third loot's tally query passes a DEAD argument | the two inlined copies pass `3` in `edx` and the call to `0030ADC0` passes `0` (`0030B452`), which `0030AE1A` overwrites with `3` before its tail jump. All three ask the same question | 1 (isolated original-code) | PROVEN |
| the class bounds check is a SIGNED compare against count - 1 | `cmp ecx, eax / jg` at `0030B3B6`, so a count of zero compares against `-1` and rejects every index. Executed at index == count - 1, which is the only place a stricter or unsigned reading disagrees | 1 (isolated original-code) | PROVEN |
| a tally query refuses in four different ways, and two of them are not the same | in `0030ADC0`: the `0xFFFF` sentinel (`0030ADC9`) and an id above the class window (`0030ADE6`) answer `-1` at `0030ADCE`; an out-of-range index (`0030AE0F`) and a record with no handler (`0030AE18`) answer `0` at `0030AE26`. Both are below any threshold, so **the difference is unobservable through this predicate** - which is why the exact sentinel value is a convention rather than a measured fact | 1 (isolated original-code) | PROVEN |
| every one of the three entry points reaches a NULL goods row and none tests it | `0030B201`, `0030B333`, `0030B5F4`. Executed with a page planted at address zero so the two sides are comparable; **the shipped process has nothing mapped there**, so this establishes the arithmetic and NOT that the path survives | 1 (isolated original-code) | PROVEN |
| what the three scripted callees do | **ANSWERED 2026-09-18 by EXP-092** (§13a): all three executed from shipped bytes, 80/80 cases and 11/11 mutants, zero stubs. The ~~`+0x50`~~ `+0x48` (mutate) handler is `002FD150` (corrected 2026-09-25), and its `r9` arm map is read from the dispatch at `002FD198`–`002FD1B9` | 1 (isolated original-code, hand-built fixtures) | PROVEN |
| flag byte bit 2 is the "newly unlocked" marker — written by `0030B630`, read by `0030B4B0`, bulk-marked by `0057B6F0`, cleared by `0056D370`, mirrored to UI record `+0x44` | whole-image `+0x59C8` displacement census (14 sites): `0030B502`–`0030B505`, `0030B67E`/`0030B686`, `0057B743`/`0057B752`, `0056D4C0`, `0031DA69`–`0031DA9D` | 1 (static) | PROVEN |
| `02EBF058` has exactly one writer — the `003845F0` relocation bind at `00236F6E`, unconditional — and `0020E600` is ~~`ref + *(01F85530)`~~ `ref + *(01F83530)` *(corrected 2026-10-02, OPUS: `0020E602`)*, so the §10 null path fires only in a goods-resource-absent state | image-wide rip-reference census of `02EBF058` (24 sites, one `lea` into the binder, no stores) plus `0020E600` read whole | 1 (static) | PROVEN (bounded) |
| nothing observed at runtime, and the containment argument carries one untested assumption | — see §13: that the save path writes the payload wholesale rather than selectively | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### Confirmed where each stands

| claim | image |
|---|---|
| the row index is the id minus `0xD000` | `0030B1F4 lea ecx, [rdi - 0xd000]` |
| the flag byte is at `BattleSystemState + 0x59C8 + row` | `0030B203 and byte ptr [rsi + 0x59c8], 0xfd` |
| a purchase clears bit 1 and never bit 0 | `0xFD` **is** `~0x02 & 0xFF` |
| refresh raises **both** bits at once | `0030B461 or byte ptr [rdi + 0x59c8], 3` — same displacement, both bits |
| the state byte is derived inside the function | `0030B1B8 movzx esi, bx` / `0030B1BB and esi, 0xfff` / `0030B1C1 add rsi, [rip → 02EBF190]` — `[02EBF190] + (id & 0xFFF)`, from `bx`, never an argument |
| the gate runs first | `0030B198 call 00322C50` before anything else |
| the class bound is a **signed** compare against count − 1 | `0030B3B1 mov eax, [rdx+0x3c]` / `0030B3B4 **dec eax**` / `0030B3B6 cmp ecx, eax` / `0030B3B8 **jg**` — with a count of 0 the comparand is `−1`, so every non-negative index is greater and **is rejected** |
| three entry points reach a NULL goods row untested | `0030B201`, `0030B333`, `0030B5F4`, each `xor` of the row register |

### This purchase *is* an authored-table row lookup, on one of the 40 registry slots

Read end to end, `0030B1AC`–`0030B1FD` is the shape
[`CONTRACT-authored-table-row-lookup`](../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md)
describes, instruction for instruction:

```asm
0030B1AC  mov   rax, [rip → 02EBF058]     ; the registry slot
0030B1C8  test  rax, rax / je 0030B201    ; the slot may be null
0030B1CD  mov   ecx, [rax + 0x0C]         ; the base-relative reference
0030B1D0  call  0020E600                  ; resolve it
0030B1D5  test  rax, rax / je 0030B201    ; the resolve may fail
0030B1F0  movzx ebx, word [rcx + 8]       ; the record stride, a u16 at +8
0030B1FA  imul  ebx, ecx                  ; × the row index
0030B1FD  add   ebx, eax                  ; + the resolved base
```

**`02EBF058` is one of the forty slots** that pass §15a's criterion in that contract — so the bazaar's
goods table is a member of the family, and every property established there applies here: the
unsigned bound, the three-byte stride reading, the one-sided guard.

> **And the family's known weakness is visible in this body.** Both `je`s land on `0030B201 xor ebx,
> ebx`, and execution **falls straight through** into `0030B203` and then `0030B20C movzx ecx, word
> [rbx + 0x16]` — with `ebx = 0`, a read of address **`0x16`**. §15's *"a failed row resolution does
> not abort the purchase"* and *"none tests it"* are the same fact seen twice, and the concrete
> consequence is a near-null read, not merely an unvalidated pointer.

**Not claimed:** the three scripted callees still run as oracles, nothing is observed at runtime, and
§13's untested containment assumption stands.

## 16. Parity plan

Reproduce: bit 0 surviving the purchase, the absolute zeroing of all three tallies, the `id - 0xD000`
index base, and the script gate's dependence on the row's own `+0x14` bit 1.

## 17. Related

- `12-Items-Equipment-Shops-License/the-bazaar-recipe-unlock-and-purchase.md`
- `11-Party/Battle-State-Block/the-battle-state-block-field-map.md`

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings are recorded in the registry, not here.*

- **CombatAction and CombatFormula — CLIENT of the item write.** `Inventory_ModifyEncodedItemAndUpdateDiscoveryState`
  (`003008A0`) is also used outside purchase:
  - `BattleAction_PrepareExecutionResources` reserves items with it, and `BattleAction_RefundReservedExecution…` gives
    them back;
  - `BattleFormula_ApplyTargetResult` grants stolen items with it.

  **A purchase, a use and a steal all move stock through the same write**, so its discovery-state update also runs on
  a steal.
- **ActorEntity, CombatAI, CombatAction, CombatFormula, Movement, Status_Periodic_Terminal and Gameplay — MECHANICAL.**
  `BattleEncodedId_IsValidForClass` (`00322C50`) is the shared id-validity query, with 71 callers, and this contract
  cites it. The crossings in these layers are its other callers:
  - the unit model;
  - the enmity readers and writers (`BattleEnmity_*`);
  - the gambit config;
  - the action-definition checks (`BattleAction_*`);
  - the stats rebuild;
  - two locomotion bodies;
  - the status paths;
  - the slot map.

  [The shared neighbours page](../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md)
  reads its jump table. The class-D functions this contract names are callers of the same query:
  `BattleIdClassD_ResetPurchasedEntryAndNestedPrerequisiteState` and `BattleIdClassD_SetRuntimeFlagBit1IfSupported`.
  `BattleIdClassD_RefreshPrerequisiteRuntimeFlags` uses `BattleEncodedId_DispatchQueryMode3`.
- **CoreRuntimeScheduling — MECHANICAL.** The four functions reach tables through `ImageAddress_ResolveRuntimePointer`.

`00325F40` (239 B) is the recipe/class indirection `002FD150` runs: `00322C50` fetch gates the body; the `(esi, ebx)` pair picks between handlers `00252E60` and `002535D0`; a u16 id whose top nibble is 1 takes the `02EBF0F8` row-byte lookup `(id-0x1000)*[+8] + resolved[+0x9]`; other kinds `<=0xA` fetch through the `01EED1B0[kind*2]` pointer table - both paths converge on the row fetch

Interior anchor `00325FDD` (function `00325F40`).

`002A1DC0` (194 B) is the gil-commit step `0056D370` runs on a purchase: gated on `0209C4C8` live and `+0xF4`/`+0xC0 & 3` clear, it flags `+0xF3` when `+0xEC + ecx` would exceed `0x5F5E0FF` (99,999,999), then `002524C0` applies - success commits `+0xC4 = +0xEC`, `+0xC8` = result, `+0xC0` = `(... & ~0x3E) | 1`, `+0xCC = 0x15`, `+0xD0` = tick `0208F570`; failure leaves `+0xF2 = 2`

Interior anchor `002A1E3B` (function `002A1DC0`).
- **Input - CLIENT (1 edge).** `0032E4D0` is also called by bodies filed to input: `00291D90` (UI) - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT (9 edges).** `00322C50` is also called by bodies filed to party: `003170E0`, `0031AC00`, `0031B510` - shared machinery across the layer boundary, no shared ownership.
- **PlatformOnlineAchievements - SERVICE (1 edge).** `0056D370` reaches bodies filed to PlatformOnlineAchievements: `00316A50` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (2 edges).** `0032E4D0` is also called by bodies filed to presentation: `003B21E0` (EffectRuntime), `003B25D0` - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (3 edges).** `0032E4D0` is also called by bodies filed to resource: `003EADE0`; `00236C30`, `00280140` reach bodies filed to resource: `003843F0`, `0032E4D0` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - SERVICE (1 edge).** `0056D370` reaches bodies filed to rewards/progression: `00253690` - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - CLIENT (4 edges).** `00233C10`, `00255260`, `002EF650` are also called by bodies filed to SaveLoad (save/load settings): `00280140` (RuntimeLifecycleSupport) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT and SERVICE (11 edges).** `00238A80` is also called by bodies filed to save/load/settings: `002EF650`; `00233C10`, `00238A80`, `00280140` reach bodies filed to save/load/settings: `002EF640`, `00255260` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (2 edges).** `0032AB50` is also called by bodies filed to script VM / native bridge: `0034C2C0`, `0034C710` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (5 edges).** `0031C5D0`, `00322C50` are also called by bodies filed to UI: `00273E30`, `002BFD20`, `0035D380` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT and SERVICE (3 edges).** `003845F0` is also called by bodies filed to World: `00238640` (Area), `003847B0` (Area); `00236C30` reaches bodies filed to World: `003847B0` (Area) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (9 edges).** `00236C30` is also called by bodies filed to WorldAreaField (world area): `00238850`; `00236C30`, `00280140` reach bodies filed to WorldAreaField (world area): `003845F0`, `003846F0`, `00267C90` - shared machinery across the layer boundary, no shared ownership.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-contract-bazaar-unlock-and-purchase-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00238640` | 19 B | tail-jumps `003845F0` with the address of the 8-byte entry at `02F973C0` indexed by the sign-extended `ecx` | `00238643`, `0023864A`, `0023864E` |
| `002524C0` | 60 B | returns 99,999,999 (`0x5F5E0FF`) when `ecx` is above it (signed) and 0 when `ecx` is negative; otherwise picks `edx` when `ecx + edx` is non-negative and `ecx` itself when that sum is negative, and returns the pick unless `ecx` plus the pick exceeds 99,999,999 (signed), in which case it returns 99,999,999 minus `ecx` | `002524C6`, `002524D7`, `002524E9`, `002524F2`, `002524F8` |
| `002535D0` | 189 B | uses `ecx` as an index (replaced by 0 after a call to `0016D6A0(0x200)` when above `0xB` unsigned, once for each of its two uses); resolves dword `+4` of the 8-byte entry at `02092760` through `0020E600` and scans the number of words given by dword `+0x47B8` of qword `020927C0` plus 4 times the index for one equal to `edx` shifted right by 16; the first match is overwritten with `0xFFFF` and followed by `002534C0` with the original `ecx` (not the clamped index), while no match or a count of 0 or less returns without either | `002535F2`, `0025363E`, `00253653`, `00253668`, `0025366D` |
| `0032AB50` | 14 B | tail-jumps `0030B570(ecx, 1 when edx is non-zero else 0)` | `0032AB54`, `0032AB56`, `0032AB59` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-contract-bazaar-unlock-and-purchase-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `002534C0` | 260 B | with `i` = `ecx`, an index above 0xB is replaced by 0 after a call `0016D6A0(0x200)` (made twice, once per use); takes the entry `e` = `02092760` + 8`i` and the counter cell `c` = qword `[020927C0]` + 4`i` + 0x47B8, and the word list `w` = `0020E600(dword [e+4])`; for each position `j` below dword `[c]` (signed) whose word `w[j]` is 0xFFFF, it re-decodes `w` and scans positions `j`+1 upward while below dword `[c]` for the first word that is not 0xFFFF: when one is found it moves it to `w[j]` and writes 0xFFFF in its place, and when none is found it stores `j` to dword `[c]` and returns; returns nothing | `002534DE`, `0025351A`, `00253544`, `0025357C`, `0025359F` |
