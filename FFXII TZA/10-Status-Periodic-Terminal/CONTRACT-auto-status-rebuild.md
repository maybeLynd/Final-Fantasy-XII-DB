---
contract: rebuild a character's derived auto-status set from three sources and apply only what changed
category: 10-Status-Periodic-Terminal
scope: family
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md
entries: ["0030FED0", "0030E130", "002FEF30", "0031E9A0", "00322C50", "00323890"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 70 addresses cited - 2 data, 11 entry, 57 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-auto-status-rebuild-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the auto-status rebuild

`BattleStats_RecomputeDerivedStateAndAutoStatuses` (`0030FED0`, 1,787 B) throws a character's derived
status set away and builds it again from scratch, then applies **only the difference**. Everything
that can grant a passive status — the character's own definition, what they are wearing, what they
have licensed — is read in one pass, and nothing incremental is maintained anywhere.

The first contract in `10-Status-Periodic-Terminal`.

## 1. Purpose

To state exactly what contributes to the derived set, in what order, and what the function does and
does not touch — **including the thing it does not do at all**, which is compute a stat.

**It computes no stat contribution on any path read here.** `equipment-slots-and-the-single-stat-
rebuild.md` describes equipping as throwing "the character's entire effective-stat state away", and
a reader will look for that formula in this function's equipment loop. It is not there: that loop
accumulates auto-statuses. Four calls in the apply tail — `0030E130` twice, `002FEF30` and
`0030E060` — were not read, so *"no stat work happens anywhere in `0030FED0`"* is **not** claimed;
what is claimed is that none of the three accumulation loops does any.

## 2. Interface

| | |
|---|---|
| entry | `0030FED0` — `rcx` = the `BattleStatsRecord`, `edx` = a flag word |
| `edx` | **a second parameter this contract did not have** (corrected 2026-09-12): `0030FEF8 mov r15d, edx` / `or r15d, 0x202`, and that word is what every status-cascade call below passes as its sixth argument. A reimplementation taking one parameter compiles and passes `0x202` where the caller asked for more |
| returns | nothing used |
| writes | `+0x78` through the applier, **and `+0x48`, `+0x4C`, `+0x06`, `+0x40`–`+0x44` directly** (§7a), and whatever `0030E130` and `0030E360` touch |

## 3. Types

| field | width | role |
|---|---|---|
| `BattleStatsRecord +0x78` `statusLayerDerived` | `uint8[16]` | the **current** derived set — 128 bits, one per status |
| `BattleStatsRecord +0x50` `equipmentSlots` | `uint16[5]` | the five equipment ids |
| `BattleStatsRecord +0x194` `licenceOwnedBits` | `uint8[46]` | one bit per licence node, ids `0..360` |
| `EquipmentDefinitionRecord +0x1A` | `uint8` | the status an item grants, `0xFF` for none |

The scratch bitmaps are stack locals: `rsp+0x40` the newly accumulated set, `rsp+0x50` the additions,
`rsp+0x60` the removals. **128 bits is the status space** — sixteen bytes diffed (`r10 = 0x10` at
`003102EA`) and an apply loop bounded at `cmp edi, 0x80` (`0031039D`).

## 4. Preconditions · postconditions · invariants

**No preconditions.** The record pointer is not checked before the accumulation loops.

**The invariant is that the derived set is a pure function of its ~~three~~ sources** — *which sources depends on the
record's kind: a kind-1 record accumulates from the owning unit's `+0xE80` bitmap in place of the definition row
(§5, §7)* *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 305 and the s24 exposure study.)*. Nothing adds to
`+0x78` incrementally; every path that could change a contributor calls this function, which is why
the referenced page's trigger list is long and why every entry in it "invalidates and rebuilds".

**Postcondition:** `0030E130` has been called exactly once per changed bit — never for an unchanged
one.

~~**Corrected 2026-09-12 by execution: `+0x78` does NOT equal the accumulation when this function
returns.**~~ *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 305 and the s24 exposure study.)* **That 2026-09-12 result was an artefact of its fixture: both runs behind it scripted the
applier `0030E130`. With the applier real, `+0x78` equals the accumulation on return**, in both an add case and a
remove case ([s24 exposure study](../_index/candidates/s24-runtime-per-invariant-exposure.md); EXP-104's `apply-set78`
agrees). What stays true is the narrower statement that follows. It is **this function's own instructions** that
never assign `+0x78`; the applier does, with `bts` at `0030E212` and `btr` at `0030E239`. The paragraph's
remaining text is kept as the record of the scripted measurement: The diff at `00310310`–`00310336` reads the stack accumulator, xors it against `+0x78`,
and stores only `added` and `removed` to two more stack buffers. **Nothing assigns `+0x78` here.**
Whatever updates the derived set does so inside the applier, one changed bit at a time; a
reimplementation that copies the accumulation back diverges, and the control that did exactly that
failed on 19 of 719 lines. **And four more things are true afterwards** (corrected
2026-09-12, §7a): the mode-5 pass has run over the unit's `+0xE90`, the spawn record and the stats
record have exchanged bytes in both directions, and **current HP, current MP and the word at `+0x06`
have each been clamped and written**.

**The invariant above is about the derived set, not about the record.** A reimplementation may rely
on `+0x78` being a pure function of its sources; it may not rely on the rest of the record being
untouched.

## 5. State

Read: the character's definition row **or the owning unit's `+0xE80` bitmap, by kind** (§7), the
five equipment rows, the licence node rows, `+0x78`, and — in the stages §7a adds — the unit's
`+0xE90`, the spawn record's `+0x78`–`+0x7C`, and the record's `+0x24`, `+0x28`, `+0x37`, `+0x3C`,
`+0x48`, `+0x4C`, `+0x64`, `+0x6C`, `+0x7C`.

Written: `+0x78` through the applier, **`+0x40`–`+0x44`, `+0x48`, `+0x4C` and `+0x06` directly**, the
spawn record's `+0x78`–`+0x7C`, and whatever the applier and the cascade touch.

**Corrected 2026-09-12.** This section said "**Unchanged:** every other field of the record". That is
true of the accumulation loops, which do write only to the stack, and false of the function.

**The three accumulation loops write only to the stack** — that part stands, and is what makes the
diff in §7 a diff rather than a read-back.

## 6. Relationships

- **Consumers of the derived set** are the status system generally; this contract does not enumerate
  them.
- `00322C50` `BattleEncodedId_IsValidForClass` gates equipment ids, `0031E9A0` gates equipment rows,
  `00323890` gates licence rows.
- The status-write cascade `0030E360` and `0030E130` own what applying a status means; they are
  cited, not specified here.

## 7. State transitions

**Corrected 2026-09-12 (`OPUS-AUTOSTATUS-ISOLATED`), from a read of the whole body.** What follows
described a **kind-0 record only**, stopped at the applier, and understated two of its own loops.
The corrections are marked; all of them are **static**, from the shipping image — nothing here has
been executed (§13).

**The accumulation source depends on the record's kind byte, and the two sources share nothing.**

*Kind 1 — a spawn-backed record* (`0031001A`–`0031006F`). The definition row is **never read**.
Instead the owning battle unit is resolved (`0031B860`) and **128 bits at `[unit + 0xE80]`** are
walked one byte at a time with a rotating byte mask, each set bit setting the same bit in the
accumulator. A reimplementation built from the sections below gives a spawn-backed combatant the
party's accumulation and no statuses at all.

*Kind 0 — from the character's own definition row* (`0030FF6C`–`00310018`). The row is reached
through the **authored-table lookup shape** (`CONTRACT-authored-table-row-lookup.md`): the registry
slot, its `+0x0C` reference, `0020E600` **twice**, and stride `[+0x08]` times the record's `+0x04`.
**On a failed resolve the row pointer becomes 0 and the two masks are read from addresses `0x50` and
`0x54`** — the same guard-that-does-not-guard that shape's §10.1 records.

Two 32-bit masks at row `+0x50` and `+0x54` — 64 bits — **walked differently from each other**, which
this section had as one loop. `+0x50` goes **two bits per iteration** (`rol r9d, 1` twice,
`add r8d, 2`, `cmp r8d, 0x20`). `+0x54` goes **one bit per iteration** (`inc r8d`, `rol r10d, 1`,
`sub r9, r13`) and computes its byte index with the **signed-division idiom** — `test r8d, r8d` /
`lea eax, [r8+7]` / `sub edx, 8` / `sar eax, 3` — which its own bounds make unreachable, since `r8d`
starts at `0x20` and only rises. Both set the accumulator bit by `shr 3` / `and 7` / `bts`.

*From the five equipment slots* (`00310071`–`00310121`). For each of five `uint16` ids at `+0x50`:
validate with `BattleEncodedId_IsValidForClass(6, id, 0)`; resolve the row from registry slot
`02EBF0F8` at `base + (id - 0x1000) * stride`; **require `0031E9A0(row) == 3`**; take `byte [row +
0x1A]`; skip `0xFF`; set that bit.

*From the owned licence nodes* (`00310140`–`003102DF`). For each id `0..360`, test the bit in
`+0x194`; resolve the node row from registry slot `02EBF038` **through the same shape, resolving
twice**; **require `00323890(row[+5]) == 2`**; then contribute **up to EIGHT statuses** — corrected
2026-09-12; this section said only "contribute". The row carries eight `uint16` fields at `+0x08`,
`+0x0A`, `+0x0C`, `+0x0E`, `+0x10`, `+0x12`, `+0x14` and `+0x16` (`003101A4`, `003101CA`, `003101F0`,
`00310216`, `0031023C`, `00310262`, `00310288`, `003102AE`), and each one that is **not `0xFFFF`** is
a status index whose bit is set. **One licence node can therefore grant eight statuses**, and a
reimplementation reading one field gives seven of them away.

**This lookup has no bounds check against the table's record count** — see §10.

**The diff, and it is a real diff** (`00310310`–`00310336`), sixteen bytes at a time:

```
changed = new ^ current          00310316
added   = changed & new          00310324   -> rsp+0x50
removed = changed & current      00310320   -> rsp+0x60
```

**The apply** (`00310340`–`003103A3`), one pass over 128 status indices, testing the two masks:

| | |
|---|---|
| bit in `added` | `0030E130(stats, index, 0, r15, 3)` — the fifth argument is **3** |
| bit in `removed` | `0030E130(stats, index, 0, r15, 1)` — the fifth argument is **1** |

Then `002FEF30(stats, 0, 0)` once (`003103AD`).

## 7a. And then it keeps going — four stages this contract did not have

**Added 2026-09-12 (`OPUS-AUTOSTATUS-ISOLATED`), and corrected the same day by executing it.** §7
ended at the call above. The function does not: `003103B2` tests the record again and runs four more
stages, each re-testing the kind byte and **re-resolving the owning unit** rather than reusing the
earlier result.

> **The kind it tests for is ONE.** `0030FF12 lea r13d, [rax+1]` sets the comparand, so
> `003103BB cmp byte ptr [rbx+5], r13b` / `jne 003104BF` sends **every record that is not
> spawn-backed straight to the clamps** — which is where that jump lands, not past them. A first
> draft of this section read it as kind 0; the differential failed on 612 of 730 lines.

1. **A second status pass, at mode 5** (`003103E0`–`00310413`). For each of **thirty-two bits of
   `[unit + 0xE90]`** that is set: `0030E360(record, 0, bitIndex, 0, …, flags, 5)`. **Mode 5** — a
   mode neither this contract nor `CONTRACT-hp-write-and-lethal-transition.md`, which uses modes 0
   and 3, has a meaning for. *(2026-09-15, FABLE, static: mode 5 sets the bit in `+0x38`, the immunity
   word — jump table `0030E88C` entry 5 → `0030E557` — and mode 3 refuses a bit set there (`0030E531`;
   [the definition-record flag pair](../04-Actor-Entity/the-definition-record-flag-pair.md)). This pass therefore
   re-installs the foe's scripted status immunities after the stat rebuild has zeroed `+0x38`.)*
2. **The spawn record and the stats record exchange five bytes — in ONE direction, chosen by a
   flag.** `0031043A test byte ptr [unit->+0x6A0], 0x80` picks: set, the **spawn record's**
   `+0x78`–`+0x7C` go into the stats record's `+0x40`–`+0x44` and the arm ends `0031047E jmp
   003104BF`, straight to the clamps; clear, the stats record's `+0x40`–`+0x44` go into the spawn
   record's `+0x78`–`+0x7C` (`00310480`–`003104BC`). Each byte goes through its own reload of
   `+0x6A0`. **They are alternatives, not stages 2 and 3**, and both are five bytes — a first draft
   of this section had four one way and the two as a sequence.
3. **Three clamps, which write the record directly** (`003104BF`–`0031058E`+):
   - **current HP** `+0x48` against the **same cap the HP write computes** — `(+0x64 | +0x3C)`, bit
     `0x10000` giving `max(hp, 1)`, otherwise `maxHp` doubled when bit `0x1C` is set — stored at
     `00310508`;
   - **current MP** `+0x4C` against a cap from `+0x28`, gated on the sign of `+0x6C` and on `+0x7C`;
   - a third signed word at `+0x06` against `+0x28 × +0x37`.

**So a status change can lower HP here, in the rebuild.** That is worth carrying into the HP write's
contract, whose "the store is the only write of `+0x48`" is a statement about *that* path and must
not be read as one about the field.

**A status present both before and after is not touched at all.** That is the point of the diff and
it is the ordering guarantee a reconstruction must keep: rebuilding the set is not the same as
reapplying it, and a reimplementation that cleared and re-added would fire every side effect the
cascade has.

## 8. Script · resource · event interactions

All three contributors are authored: the definition row, the equipment definition table
(`02EBF0F8`) and the licence node table (`02EBF038`), each reached through the registry with the
`AuthoredTableHeader` idiom. Nothing here loads them.

## 9. Determinism

Fully deterministic given the record and the three tables.

## 10. Failure paths and edge conditions

- **A null or unresolvable table yields a fallback row**, not a skip: both the equipment path
  (`003100DF`) and the licence path (`0031018F`) set the row pointer to `r14` and continue into the
  gate call. What `r14` holds at that point was not established.
- **The licence node lookup is unbounded.** `imul edx, ebp` at `00310187` with no comparison against
  the table's count at `[table + 4]` — the only `cmp` on the index in the loop body is the loop's own
  `cmp ebp, 0x169`. Since the id space is 361 and `license_data.bin` declares 360 records, a set bit
  for node 360 reads one record past the end. **Whether that bit is reachable is open**
  (`OPUS-NOTICE-NODE360`), and the bit is tested before the row is computed, so an unreachable bit
  costs nothing.
- **The status index is treated as signed** in the apply loop (`test edi, edi` / `jns` /
  `lea eax, [rdi+7]` / `sub ecx, 8` / `sar eax, 3` — a signed divide by 8), although the loop only
  produces `0..127`.
- Nothing reports any of this; the function has no failure return.

## 11. Observable behaviour

Not established. What would be observable: removing a piece of equipment that grants a status
removes exactly that status and leaves a same-named status granted by a licence in place, because
the diff sees the accumulated bit still set.

## 12. Reproduction formula

> **This sketch is the kind-0 accumulation and the apply, and nothing else** (marked 2026-09-12).
> It omits the second parameter (§2), the kind-1 source (§7), seven of a licence node's eight
> contributions (§7), and the four stages after the apply (§7a) — including the three clamps that
> write the record. **Do not implement from this block alone.** It is kept because the diff and the
> apply below are still exactly right.

```c
void RecomputeDerivedStateAndAutoStatuses(BattleStatsRecord *s, uint32_t flags /* OR 0x202 */)
{
    uint8_t next[16] = {0};

    if (s->kind == 1) {                        /* SPAWN-BACKED: a different source entirely */
        for (int i = 0; i < 128; i++)          /* 128 bits at unit->+0xE80 */
            if (test(unit_of(s)->autoMaskE80, i)) set(next, i);
    } else {
        for (int i = 0; i < 32; i += 2)        /* the definition row's two 32-bit masks */
            if (row->mask50 & bit(i))   set(next, base + i);
        /* ... and the +0x54 half, ONE bit per iteration ... */
    }

    for (int k = 0; k < 5; k++) {              /* the five equipment slots */
        uint16_t id = s->equipmentSlots[k];
        if (!IsValidForClass(6, id, 0)) continue;
        Row *r = equip_row(id);                /* base + (id - 0x1000) * stride */
        if (kind_of(r) != 3) continue;
        uint8_t st = r->autoStatusId;
        if (st != 0xFF) set(next, st);
    }

    for (int n = 0; n < 361; n++) {            /* the owned licence nodes */
        if (!test(s->licenceOwnedBits, n)) continue;
        Row *r = node_row(n);                  /* UNBOUNDED - see section 10 */
        if (gate(r) != 2) continue;
        for (int f = 0; f < 8; f++) {          /* EIGHT fields, +0x08 .. +0x16 */
            uint16_t st = r->grants[f];
            if (st != 0xFFFF) set(next, st);
        }
    }

    uint8_t added[16], removed[16];
    for (int b = 0; b < 16; b++) {
        uint8_t ch = next[b] ^ s->statusLayerDerived[b];
        added[b]   = ch & next[b];
        removed[b] = ch & s->statusLayerDerived[b];
    }
    for (int i = 0; i < 128; i++) {
        if (test(added, i))   ApplyStatus(s, i, 0, ctx, 3);
        if (test(removed, i)) ApplyStatus(s, i, 0, ctx, 1);
    }
    Finalise(s, 0, 0);
}
```

## 13. Runtime validation

**Evidence class: isolated original-code, over the whole function. Live capture: still absent.**
(2026-09-12)

**What ran:** `0030FED0` entire, as shipped bytes under Unicorn at its real virtual address. Eight
callees are supplied as scripted oracles at their own real addresses — `0031B860`, `00322C50`,
`0031E9A0`, `00323890`, `0030E130`, `0030E360`, `002FEF30`, `0030E060` — and **the resolver
`0020E600` is deliberately NOT stubbed**, so the real three instructions run inside all three
authored-table lookups. **What did not run:** anything inside those eight, and no caller.

**Instrument:**
[`diff_auto_status.py`](../../../Reconstruction/Tests/Differential/diff_auto_status.py) against
[`auto_status.c`](../../../Reconstruction/Game/Status/auto_status.c).

**Result: 1463 commands, 1055 compared lines, 0 mismatches** — 275 applier calls, 36 cascade calls
at mode 5, and six traces over a null row.

### Four things the static read got wrong, and the run found

The six corrections §7 and §7a carry were read out of the body before this pilot was built. **Four
more were wrong, and only executing them showed it:**

| what the reading said | what the run showed |
|---|---|
| the second half runs for a kind-0 record | it runs for **kind 1**; `lea r13d, [rax+1]` is the comparand, and every other kind lands **on** the clamps rather than past them |
| `+0x78` holds the accumulation afterwards | **nothing writes it back**; the diff stores only `added` and `removed`, both to the stack |
| the spawn record gives four bytes and the stats record five | **five each way** |
| the two copies are stages 2 and 3 | they are **alternatives**, chosen by `test byte ptr [spawn], 0x80`, and the first ends in a jump to the clamps |
| the equipment gate receives the resolved row | it receives the row **ADDRESS** (`003100E2 mov rcx, rdi`), which is **0** when the resolve failed — so a caller that has a real page at address zero must still pass the zero, not a pointer into it |

That is the argument for executing a contract rather than reading it carefully: the reading was done
with the body open, in one sitting, by someone looking for exactly these things, and it still got
**five** of them backwards. The last one came from a case added for a different reason — one that
runs before any fixture reset, where all three registry slots are still null.

### The positive control

Two of the four were re-applied as the reading had them, rebuilt from a deleted executable, and
re-run:

| control | result |
|---|---|
| the second half gated on kind 0 | **FAIL**, 612 of 730 lines |
| the accumulation copied back into `+0x78` | **FAIL**, 19 of 719 lines |

### The mutation campaign

**149 mutants: 129 KILLED, 15 SURVIVED, 5 EQUIVALENT, 0 INVALID,
0 NO_BUILD**, with `production_inputs_stable: true` and all four input hashes re-checked
against the files as published.

**Three rounds, and each round's survivors were read one at a time rather than in bulk.** The first
left 29, the second 27, this one 15. What the middle round bought was not a better score but
a list of things the fixture could not distinguish, every one of which turned out to be a real gap:
the copy length was invisible because the dump printed five bytes and the copy is five; no HP sat
**between** the undoubled and doubled caps, which is the only range where the doubling bit changes
the outcome at all; no MP or `+0x06` word sat at 1 with the gate closed, where a cap of 0 and a cap
of 1 differ; the third clamp had never seen the gate bytes vary; and the copy flag had never been
driven at a value whose low bit differs from `0x80`.

**What survives is either this reconstruction's own framing or a property the original shares.**

- **The freeze bit makes the HP clamp a no-op.** Its cap *is* the current HP, so `hp > cap` can
  never hold, and every mutant of `(hp < 1) ? 1 : hp` — in both the cap and the re-derivation — is
  equivalent. That is a fact about the game, not a gap: **status bit 16 does not lower HP here.**
- **A status id above 127 lands in the next buffer, and the diff overwrites it.** The sentinels
  `0xFF` and `0xFFFF` can be widened without effect because a bit set past the accumulator falls
  into `added`, which the diff then recomputes. The original does exactly this, into its own stack
  frame.
- **The frame's size and layout constants** drive the accumulator, `added` and `removed` together,
  so moving them moves everything consistently.
- **The `map`-returns-NULL fallbacks** are scaffolding the original has no equivalent of: it reads
  the address whatever it is. Nothing in this address space can reach them.

### 13a. The three gates, executed — 2026-09-18 (OPUS, consuming SWE2-ORACLE's EXP-100)

EXP-100 ran `00322C50`, `0031E9A0` and `00323890` — and their sub-bodies `0031E9F0` and `003241D0` —
as shipped bytes inside the subject, **40/40 cases, 13/13 mutants, two processes, 8 real bodies**.
The gates are no longer oracles. **Both writers still are**, and §13's live-only paragraph is
otherwise unchanged.

**Finding 3 is already in this contract, twice.** §7 requires `00323890(row[+5]) == 2` and §15a cites
the instruction — `00310192 movzx ecx, byte [rdi+5]` / `call 00323890` / `0031019B cmp eax, 2`. That
the gate receives a **byte** rather than the row pointer or the licence id was read from the call
site when this contract was written, and the execution confirms it. Recorded as confirmation.

#### What being scripted actually hid: the equipment window is data, not a constant

`00322C50` dispatches on its first argument through a jump table (`00322C5A lea eax, [rcx-1]` /
`cmp eax, 0x1f` / `ja`), and the equipment arm at `00322D02` is:

```asm
00322D02  mov  rax, [rip + 0x2b9c3ef]   ; -> 02EBF0F8, the table pointer
00322D09  mov  edx, 0x1000              ; lower bound
00322D0E  test rax, rax / je 0x322d21   ; null table
00322D13  mov  eax, [rax + 4]           ; the COUNT
00322D16  lea  ecx, [rax + 0x1000]      ; upper bound
```

with the shared tail at `0032302E`: `cmp ebx, edx` / `jl` refuses below, `lea eax, [rcx-1]` /
`cmp ebx, eax` / `jg` refuses above. **So an equipment id is valid over `[0x1000, 0x1000 + count)`,
and the count is the live table's own `+4` — not a compiled-in bound.** Two things follow that a
scripted gate could not show:

- **Both comparisons are signed.** A negative id refuses at the *lower* bound; an unsigned
  reimplementation would treat it as huge and refuse at the *upper* one. Same answer today, different
  answers if the window ever reaches the top of the range.
- **A null table is an empty window, not an open one.** The `00322D21` arm computes
  `ecx = 0 + 0x1000` with `rax` zero, so lower and upper coincide and **nothing is valid** — the
  refusal is by arithmetic rather than by a guard.

#### The two classifier chains, and which gate value contributes

- **Equipment:** `row+9 ≤ 0x1A` maps through a byte table and a jump table to classes 1–9, and the
  gate collapses those to `≤0 → 0`, `1–5 → 1`, `6 → 2`, `7–9 → 3`. **The subject bits at
  `acc[row+0x1A]` are taken only when the gate answers 3**; `0xFF` in the status byte is a no-op
  sentinel.
- **Licence:** `003241D0` classifies `(b−1) ≤ 0x1D` into `0x15`–`0x1E`, and `00323890` maps
  `class − 0x15 ≤ 9` onto gates `{0,1,2,3}`, else −1. **Only gate 2 contributes**, which is §7's
  `== 2` requirement arrived at from the other side.
- **The walk is `id = 0..360` inclusive** over the owned bitmap. Id 361 is never probed; an unowned
  id produces no gate call at all; and an absent licence table still calls the gate once per owned id
  with byte 0, which answers −1.

#### One cross-experiment corroboration worth recording

`00322C50`'s fall-through arm calls `00309440`, decrements, and **re-enters its own jump table**
(`00322C7E`–`00322C8B`). That is the class-number indirection EXP-092 measured from the bazaar side,
where `00309440` reads `fam[id>>12]+0x38` and re-dispatches. **Two experiments in different
subsystems have now driven the same mechanism**, which is worth more than either alone:
[`CONTRACT-bazaar-unlock-and-purchase.md`](../12-Items-Equipment-Shops-License/CONTRACT-bazaar-unlock-and-purchase.md)
§13a holds the other half.

#### Crossing into Presentation — the same classifier answers a loot question

Naming `0031E9F0` above imported its one Presentation caller, and the edge is worth the sentence it
costs. `Loot_DeriveWorldPickupPresentationTier` (227 B, owned by Presentation) calls it at
**`00319AC0`** and buckets the answer immediately — `test eax, eax` / `jle`, then `cmp eax, 5`, which
is the same class-5 boundary the gate above collapses to 1. **It reaches the classifier the same way
this contract does, too:** `00319AA6 lea edx, [rbx - 0x1000]` takes an equipment id off the same
`0x1000` base and multiplies by the table's row stride at `[rsi+8]` before asking.

**This page is the SERVICE and owns nothing in Presentation.** The crossing is that a loot pickup's
presentation tier is derived from the equipment classifier the auto-status gate uses — one
classifier, two consumers, and the equipment id space is shared between them.

*The far end is named by symbol rather than by address, and that was measured rather than assumed:
writing it as an address would import a CoreRuntimeScheduling edge this page does not mention, so
closing one finding would have opened another. The call site is an interior address and is safe to
cite.*

#### Consumed on EXP-100's evidence, not re-derived here

Findings 5–10 — the kind-byte halves, the `prior[16]` diff at `rec+0x78` with add/remove modes, the
five-byte spawn exchange and its direction bit, the hp/mp/word clamps and the two deny bytes, and the
`| 0x202` flag propagation — are taken on the experiment's evidence and **were not re-read from the
image in this pass**. The four claims above are the ones this section stands behind at tier 1.

### 13b. Notify (`002FEF30`), executed — 2026-09-18 (OPUS, consuming SWE2-ORACLE's EXP-103)

§14 listed `002FEF30` as one of the four apply-tail calls this contract specified only by its
argument shape. **It is now executed from shipped bytes** — 31/31 cases, 15/15 mutants killed, three
independent processes, with eleven closure bodies (`RESOLVE`, `FIND`, `VALID`, `EQGATE`, `EQCLASS`,
both magic-multiplies, the pool getters and the resolver base accessor) all running real code.

**Adopted at tier 1 (isolated original-code), not at tier 0.** Two sinks were scripted with argument
capture — `003105D0` and `00307D10` — so as published this section established *that the tail is
reached and with what arguments*, and nothing about what those two bodies do.

> **That boundary is closed, the same day, by §13d.** EXP-104 executes both of them from shipped
> bytes, so the tail's effects are no longer taken on argument capture alone. The sentence is kept
> rather than rewritten because §13b's *own* evidence still stops where it stopped; what changed is
> that another package went further.

**Two sites were re-read from the image in this pass** rather than taken on the experiment's word,
because three separate corrections rest on them:

```
002FF58F  xor  ebp, ebp                    ; the bitmask walks start at index 0
002FF596  mov  [rsp+0xD8], edi             ; ad8 is spilled here ...
002FF5A7  mov  r15d, 1                     ; ... and r15d is reloaded to 1
002FF7A7  mov  eax, [rsp+0xD8]             ; ... and read back unconditionally
002FF7AE  add  r11d, eax                   ; into the second clamped sum
```

**One fact collapses three earlier misreads.** `ebp` is zeroed and `r15d` reloaded to `1` before the
walks, so: the walks start at index **0**, not 5; the bit test is `1 << i`, not an accumulated gate
value; the tail's zero-writes really write **0**; and `flag5c`/`flag64` compare against zero, which
makes both flags **live** rather than dead.

| what the pilot model said | what execution measured |
|---|---|
| `out[0]`'s lower bound is the gate-2 accumulator | **the bound is `1`** — `r15d` is reloaded; the accumulated `a20` survives in `out[0x0F]` |
| `out[0x10]` is a leftover accumulator, branch-dependent | **`ad8`, unconditionally** — pinned by `kind0-out10-quirk` and `kind0-gate2-arm` |
| `0x7FFF` replaces the bound | **a second, conditional write** — `[1, 9999]` (kind 0) or `[1, 1e9]` first, then `0x7FFF` when `flag5c` is set |
| FIND-miss faults through the tail | **FIND-miss and an explicit `rdx` skip the tail entirely** — no unit writes, no sink tokens |

**`gate2` means `t9 == 0x12` exactly.** EQCLASS is a two-stage dispatch — byte table `t9 -> selector`,
then a dword-RVA jump table `selector -> arm` — and EQGATE maps classes 1-5 to gate 1, 6 to gate 2,
7-9 to gate 3. Only `t9 = 0x12` reaches class 6.

**The fault surface is asserted, not assumed.** A null equip table is *tolerated* by VALID arm 6
(returns 0), while a null `[0x2EBF130]` definition table or a null resolver base **faults at the
first row-field read**, at addresses the harness pins.

> **What this does not settle.** The two scripted sinks, as above; and the experiment's own
> `bodies.json` records measured spans and hashes for the eleven real bodies, so the closure is
> checkable — but a body that shipped bytes execute correctly under thirty-one constructed inputs is
> still a body exercised at thirty-one points, not a proof of totality.

### 13c. The resolver family, executed with no stubs at all — 2026-09-18 (OPUS, consuming EXP-102)

Seventeen bodies of the `0031B7xx`/`00263Exx`/`003588xx` lookup layer, **every one of them shipped
bytes — this package has no scripted boundary anywhere**: 52/52 cases, 16/16 mutants, three
processes. That is the strongest class available short of live runtime, and it matters here because
this layer is already consumed by reconstructed CombatFormula and status paths, where a wrong failure
encoding propagates silently.

**The failure encoding is `-1`, not `0`.** `0031B8E0` has four early-outs and all four converge on

```
0031B93E  or   eax, 0xFFFFFFFF
```

so KIND encodes "no object" as `0xFFFFFFFF`, matching `00263E50`'s null-chain convention — while the
*scan and accessor* half of the same family encodes it as `0`. **Two conventions live side by side in
one neighbourhood**, and a reimplementation that picks one for all of them is wrong half the time.

**RESOLVE really is called twice with the same argument**, and the repetition is not redundant:

```
0031B906  mov  ecx, [rax+0x0C]  ;  first resolve
0031B909  call 0020E600
0031B90E  test rax, rax
0031B911  je   0031B93E         ;  a REAL early-out between the two
0031B91A  mov  ecx, [rax+0x0C]  ;  second resolve, identical argument
0031B91D  call 0020E600
```

`[02EBF130]` is re-read between them, so the second call is what the row addressing consumes.

**And one thing the experiment did not name, which the bytes make plain.** The row address is
computed in **32 bits and used as a pointer**:

```
0031B929  movzx edx, word [rcx+8]     ; stride
0031B92D  imul  edx, ebx              ; * id
0031B930  add   eax, edx              ; 32-bit add - the upper half of rax is ZEROED
0031B932  je    0031B93E              ; and the fail test is on THIS sum being zero
0031B934  movzx eax, byte [rax+7]     ; read through the truncated value
```

`add eax, edx` zero-extends into `rax`, so the field read goes through **the low 32 bits of the
resolved base plus the scaled id**. That is consistent with `0020E600`'s base-relative pointer
scheme, and it is a constraint a 64-bit reimplementation will not reproduce by accident: keeping the
full pointer changes both the address and the zero test.

**Other measured semantics adopted:** `VALID`'s auto-detect arm re-dispatches through `jt[cls-1]`
after calling `CLS(id)`; `HDEC`'s family mask is four bits but only families `< 5` are accepted, and
it checks **tag staleness last**, so a structurally valid record with a dead element still reaches
the tag compare at `elem+0x16`; `0031B7E0`'s gate is bit `0x10` of the byte at `[0x2089340]`, and
with it clear the handle is never decoded at all.

> **The boundary here is different in kind from §13a and §13b: there isn't one.** No stub, no
> scripted sink. What remains is coverage, not disclosure — fifty-two constructed inputs across
> seventeen bodies is a large exercise, and still an exercise.

### 13d. The five sinks, executed — 2026-09-18 (OPUS, consuming EXP-104)

**This is the section that closes the write side.** SINK `00307D10`, TAIL `0030E060`, RESET
`003105D0`, APPLY `0030E130` and CASCADE `0030E360` all run from shipped bytes — 65/65 cases, 22/22
mutants, three processes — together with twenty-nine resolver/pool bodies inherited from EXP-101/102
and every quiet-zone helper each subject calls.

**Two sinks §13b could only name are now executed**, and so are both writers §13a listed as owed.

Corrections this pins, each to a branch or constant site:

- **APPLY's gate global is `0x2EBF040`**, not `0x2EBF047` — arm `0x1D`, bound by `dword[tab+4]`.
- **`0030FED0` recursively calls APPLY and then NOTIFY**, and **the nested calls read memory the
  apply has already mutated** — the model has to carry mutated state into the nested call, not a
  snapshot. A reconstruction that evaluates arguments eagerly gets different answers.
  *Scope, because the two statements sit in one document:* this is about the **order** in which the
  nested calls observe state, and says nothing about **which** locations `0030FED0` writes. §15's
  claim that nothing writes `+0x78` outside the apply is untouched — the apply is precisely where
  that write lives, and it is the write these nested calls then see.
- **NOTIFY clears `obj+0x24..0x47` and then rebuilds conditionally**, measured here for the first
  time; §13b's constructor view did not reach it.
- **CASC's `is34` (action ∈ {3,4}) gates both the `sb8` wrapper and the eligibility block**, and the
  `E9A` arms read `u2+5` rather than the resolved record of `f2`.
- **`unit+0` and `unit+4` are one qword**, shaped by three qword masks.

**A cross-contract join, unlooked-for.** `00290B90` walks a list rooted at
`qword[0x209BE80] + 0x10F10`. That is `ManagerSingleton0209BE80 +0x10F10`, which the type store
declared the same day from an entirely separate census as a null-tested pointer with six reads and no
observed writer — **this names it: it is a list root, and this is its reader.**

> **The boundary moved; it did not vanish.** ~~Four~~ ~~Three~~ carriers are still scripted
> returns — ~~`0024FE30`~~ (EXP-198: it is a 0x24-byte dispatch thunk, not a 950-body carrier —
> the tree figure covered its callees), ~~`00300FC0`~~ (EXP-198: 0x173-byte detach/unlink carrier,
> executed with `00301140`), `003112F0` — along with
> the notify formatter `003BBD00` and the CRT `memset`/`sqrtf` thunks, which **jump into unresolved
> IAT hint/name data** and so cannot execute at all outside a loaded process. So the contract can now
> say what a status application *does to the unit*, and still cannot say what those ~~four~~ ~~three~~
> remaining carriers decide. *(Amended: `0017D470` executed as shipped bytes by EXP-197 — it is a 0x14-byte
> accessor, `d[001D50D0()+0xC20]` returning the lazy singleton's mode dword, called twice per
> `0030B7F0` owner-flag composition. Amended again: `0024FE30` and `00300FC0` executed as shipped
> bytes by EXP-198 — §13g.)*

### 13e. `0031B860`, the shared reverse lookup, executed — 2026-09-18 (OPUS, consuming EXP-101)

§13's run listed `0031B860` among eight scripted oracles, and that sentence is still an accurate
record of *that* run. **It is no longer an accurate description of what is known.** EXP-101 executes
it from shipped bytes with both pool helpers real — 19/19 cases, 12/12 mutants, three processes —
and the whole function is eighty-three bytes, so every claim below was **re-read here rather than
adopted on report**. All six hold.

```
0031B882  test eax, eax
0031B884  jle  0031B8A6          ; a negative or zero count returns 0, on the FIRST read
0031B88D  test rax, rax
0031B890  je   0031B89B          ; element-null skips to the increment
0031B892  cmp  qword [rax+0x698], rdi     ; THE MATCH IS A FULL QWORD
0031B899  je   0031B8A8
0031B89D  call 00236850          ; the count is re-read EVERY iteration
```

- **The match is a full qword.** `cmp qword ptr [rax+0x698], rdi` — a reimplementation comparing the
  low 32 bits finds a unit that is not the owner whenever two records share a low half. This is the
  single most consequential line in a primitive with **35 CombatFormula callers**.
- **The count is re-read every iteration** (`00236850` at `0031B87D` *and* `0031B89D`), so the loop
  observes a pool that shrinks underneath it. Hoisting it into a local is a behavioural change, not
  an optimisation.
- **There is no base-null guard, and the index is guarded on both sides.** With `base = 0` the
  element-null skip only catches `i = 0`, because that is the one index whose computed pointer is
  itself 0; `i = 1` dereferences `0xF50 + 0x698` and faults. **The guard that exists protects the
  index, and the one a reader assumes exists — on the base — does not.**
- The getter's own refusal arm is unreachable from this caller, since the loop keeps `0 <= i <
  count`; EXP-101 reaches it with direct calls instead.

**And it corroborates §13c from the other side.** This function returns **0** on both failure paths
(`0031B86E` for a null argument, `0031B8A6` for not-found) — never `-1`. §13c records that the
scan/accessor half of this family encodes "no object" as `0` while `KIND` encodes it as `-1`;
`0031B860` is the scan half, measured independently, agreeing.

> **What this does not change.** The oracle lists in §13 and in
> `CONTRACT-experience-and-licence-award.md` §13 stay as written: they record what those runs
> stubbed, and they were true. What is no longer true is the *implication* that the stub's behaviour
> was a fixture choice — for this one callee it is now measured.

### 13f. The owner-check family and two arm carriers, executed — EXP-197

The cascade's owner-check quad and the two small arm carriers EXP-104 stubbed as `~sb9`/`~sb8`/
`~s014`/`~s99b` now run as shipped bytes on the member-block-chain driver (271/271 cases,
stable ×3, byte-identical `result.json`; `NATIVE-REPLAY`, `live_game: false`):

- **`0030B770`** composes the global flag word: bit0 `d[02089340] & 0x3080`, bit1 `b[022C2158] & 1`,
  bits 2/3/4 = `d[02089340]` bits 10/9/11.
- **`0030B7F0(objrow, edx)`** composes per-object flags — low word from `d[obj]`/`b[obj+4]` and
  `d[022C2160]` (−5 must exceed 1 unsigned, so values 5 and 6 suppress bit3), bit4 from the linked
  record's `b5==0 && b4==0x1A`; **high word** from `0017D470()`: ==1 → hi bit0 (record `b5==0` gated),
  ==2 → hi bit1. `0017D470` runs **twice** per call.
- **`0030B9B0`** returns 1 iff either composer's **low** word is nonzero; **`0030B8E0`** returns 1
  iff `0030B7F0`'s **high** word is nonzero (the `0030B770` word's high half is structurally 0).
  Both feed `edi/ebx` from `0030AB40(row, row2) > 1` — the relation-pair classifier returning
  `(computed == expected) + 1` ∈ {1,2}.
- **`0017D470`** is `d[001D50D0() + 0xC20]` — a mode dword off the lazily-allocated singleton
  `q[01F81428]` (alloc path `00210EC0`+`001CCB20` is stubbed but driven and observed).
- **`00300140(objrow, edx)`** — the unlink-mark carrier: conditional `003105D0` on `edx`, clears
  `q[+0x6F8]`/`d[+0x748]`/`d[+0x770]`/`q[+0x750]`/`d[+0x74C]`, `d[+0x788] &= ~0x400`,
  `d[+0x6B0] &= ~2`, sets `d[obj+4] |= 0x200000`, and clears `q[obj]` bit14 **only when the
  `w[obj+0xBA0]` sentinel does not match** (`0x113` with bit14 set, `0x95` without).
- **`003299B0(objrow, edx=msg, r8d)`** — `edx==-1` is a pure no-op; otherwise
  `ebx = (edx & 0xFFF) >= 0x100 ? edx | 0x5000 : edx`, `002EB030` stamps the entity node
  (`b[+0xD] &= ~1`, `b[+0xF5] = 0xFF`, `d[+0xEC] = 0`, `d[+0xF0] = ebx`, optional `002EB0D0` kick
  when `b[+0x18] != 1`), then `d[obj+0x5C] = ebx` and `d[obj+0x2C]` cleared.

This also closes the record's scope error: `0017D470` was never a "context carrier" — it is the
mode accessor behind `0030B7F0`, and `00301140`/`00312280`/`00300FC0` share one unlink-carrier
tail family (kept scripted for the next package rather than split across cases).

### 13g. The unlink-carrier family and the `0024FE30` dispatch, executed — EXP-198

The two unlink carriers and the dispatch thunk now run as shipped bytes on the
member-block-chain driver (300/300 cases, stable ×3, byte-identical `result.json`;
`NATIVE-REPLAY`, `live_game: false`), with twenty-one leaf/helper callees promoted
real and the heavy subtrees (`003105D0`, `00238BF0`, `00311F70`, `0023B040`,
`002ECF10`, `002EBB80`, the `0024FE70` query, the lock pair) kept scripted as
disclosed boundaries:

- **`00300FC0(obj, edx)`** — `edx==0` + linked rec + `b5==0` + `b4∈[0x1B,0x27]` →
  `003105D0(obj)` + tail `003138D0(0)`. Otherwise the full teardown:
  `00310780` → `002ED180` → flag masks (`q[obj] &= 0xFFFFFFFDFFE7FFFD`,
  `d[obj+4] &= ~4`) → entity writes `0026DAC0`/`0026A330` → `003219D0` capability
  scan → `002372E0`/`00237260`/`002373C0`/`003272E0` set `d[02089340]` bits
  `0x400`/`0x200`/`0x800`/`0x100` with `0035C8A0(0xB/0x18/0x17)` posting
  `d[022C83E8]` flags `2`/`1`/`0x10`. The `0x400`/`0x200` arms tail-jump to
  `0023B040`; the `edx==0` tail runs `0030D9A0()==1` + `0031B770(b[glob+0x5AD5])==obj`
  → `003138D0(0)` + `0023B040`.
- **`00310780`** — contributor accounting: `0031B7E0(d[obj+0x710])` row, iff
  `q[obj]` bit22 and `d[row2+0xEA4]` has `1<<b[obj+0xEA9]`: `b[row2+0xEA8]--`,
  `d[row2+0xEA4] &= ~bit`. Then `q[obj] &= 0xFFFFFFFFEFFFFFDF`,
  `0030C970(b[obj+0x694])` + `b[obj+0x694]=0xFF`, `00319420(&obj+0x6B0)`,
  `00319140(obj,1)`, `00317E50` iff `w[+0x714]==0x414E`.
- **`003138D0(arg)`** — mode-1-gated (`0030D9A0` bit-map of `d[glob+0x5B04]`):
  `0031B8C0(3)` row lookup, sentinel bail on `w[+0xBA0]==0x113`/`w[+0x714]==0x113`,
  `0031B7E0` twice, `00311CF0`, then `w[glob+0x5AD0] ^= (w ^ arg) & 1` — arg 0
  clears bit0, keeps the rest.
- **`00301140(obj)`** — bail iff `(d[rec+0x64]|d[rec+0x3C]) & 0x80000003`; else the
  full release: `002E9600` (+`00311F70` on bit26), `00238BF0`, `003105D0`, the
  inline `00300140`-class field clears, `002EACD0`→`003B02A0`, `002E8060`,
  string select `q[+0x6E8]` = `0x1EEC3C0`/`0x1EEC410` by `b[rec+5]`,
  `002ECF10`, `003299B0(obj,0x200D)` real, `00319E30`,
  `d[+0xDD0] = 0032A150() − int(1.0×−30.0)×5` (`0032A150` = `d[0208D45C]`),
  `003125E0` → `0026DC60` → `002EBB80`.
- **`003125E0`** — flag-word composer: `d[obj]` bits 11/10/9 → out 1/2/3,
  `d[obj+4]` bit2 → out bit5, cap `d[q[obj+0x6A0]]` bits `0x10`/`0x8` → out 6/7.
- **`0024FE30(ecx, edx)`** — `(ecx>>0x1C)&0xF`: `1`→`002FD0C0` (`02EC32E0`
  stride-0x38), `7`→`003B2830` (`02EBE5E0` stride-0x30, writes `w[hit+0x378]=3`),
  `5`/`6`/`9`→`003B1260` (`02EBEC00` stride-0x30), else 0. Match path:
  `0036C1D0` lock → `0024FE70` query → `0036C140` unlock → ret 1. Tables are
  shipped-zero BSS; positive results are fixture-driven.

Two null-guard facts worth the record: `00300FC0`'s edx==0 head checks
`q[obj+0x698]` but the shared full path re-reads it unguarded at `0030105A`
(fault proven), and `00301140` derefs the record at `00301150` before any check
(fault proven). And a fixture correction now canonical: `00322C50` kind-2 is the
**FOED** descriptor `q[02EBF130]` — the foe-table range bound, reused by
`003219D0`'s capability check.

~~`00312280` (EXP/LP guest-share distribution) is split out as EXP-199.~~ —
**executed by EXP-199 — §13h.**

### 13h. The EXP/LP guest-share distributor `00312280`, executed — EXP-199

The EXP-198 deferred sibling now runs as shipped bytes (326/326 cases, stable
×3, byte-identical `result.json`; `NATIVE-REPLAY`, `live_game: false`):

- **`00312280(rcx=peer, rdx=objrow)`** — head: `rec=q[rdx+0x698]`; iff rec
  nonnull, `b[rec+5]==1`, peer nonnull, `b[peer+5]==0` → `00317ED0(rdx)`; then
  always `003171C0(rdx)` (both scripted). Gate: return on `rec==0`,
  `b[rec+5]!=1`, or `b[rdx+0xE9A]&8`. Scan arm iff `(e9a&5)==5`, or
  `((d[rec+0x64]|d[rec+0x3C])&2 && e9a&2)`, or `peer!=0 && b[peer+5]==0`:
  for `i=0..8`, `00320AB0(i,3)` resolves `glob+8+map*0x1C8`
  (`map=b[glob+0x5A7E+i*2]`); retained iff `(d[+0x64]|d[+0x3C])&0x80000003==0`
  or `00377C20()!=0`, stashed at `q[022C1740+j*8]` (cap 9).
- **Per guest:** `ebx=clamp(002F8BB0(row,rdx),0,999999)`,
  `esi=clamp(002F90C0(row,rdx),0,999)` — arg2 is the member/object row,
  not the record (corrected by EXP-200); both were scripted retkey-driven
  at this checkpoint, executed real by EXP-200 (§13i);
  `b[row+0x69]&0x10 || b[row+0x79]&0x10` consumes LP — no `d[+0x190]` write,
  `00316A50` gets edx=0, `r12 += b[row+0x1C2]*lp*5` feeds the source FP
  tail. `00236780()==0` gate → `d[+0x18C]=min(+ebx,0x5F5E0FF)`;
  `d[+0x190]=min(+esi,0x1869F)`; `00316A50(lp,0xB)` scripted; level-up loop
  `while 0<002F8F20(lvl)<=d[+0x18C]: lvl++` (`002F8F20` real — measured curve
  L2=169, L3=386, L4=736), then `0030C650(row,lvl,0)` scripted.
- **Source tail** (runs even with zero guests): `exp/lp` from
  `002F8BB0(0,rdx)`/`002F90C0(0,rdx)` (exp suppressed when `00236780()!=0`),
  `0028FB80(d[rec+8],exp,lp)` scripted; FP contribution
  `(b[rec+0x1C2]-b[rec+0x88])*d[q[rec+0xE78]+0x30]+d[q[rec+0xE70]+0x30]+r12`
  → `max(00253690()+contrib,0)` → `00254EE0`/`00469E80` (scripted); position
  chain `00319490`→`003180F0`→`00319CA0` scripted; `00265020(q[rec+0x10])`
  real; `00317090` scripted; `00808C40` cookie epilogue scripted.
- **`00236780()`** — `d[q[02EBF190]+4] >> 0xE & 1` — the EXP-suppression flag
  on the same `glob` context block the guest scan uses; set via
  `globb={5:0x40}` in the harness.

Harness corrections recorded in the EXP-199 record: the guest table is
`glob` (`q[02EBF190]`), not a separate `02ECF190` block; the stash base is
`022C1740`; `0030C650`'s `lc650` REAL entry was dead (SCR shadows it —
removed); `002F8F20` curve values were re-measured from executed bytes.

The share-formula bodies `002F8BB0`/`002F90C0` — ~~deep `0020E600`
machinery trees~~ (that scope fear did not materialise; no callee of either
formula reaches that tree) — **executed by EXP-200 — §13i.**

### 13i. The share-formula family `002F8BB0`/`002F90C0`, executed — EXP-200

The two share calculators EXP-199 scripted now run as shipped bytes
(360/360 cases, stable ×3, byte-identical `result.json`; `NATIVE-REPLAY`,
`live_game: false`), plus leaf helpers `00313800` (leader byte
`b[glob+0x5AD5]` → `00320890`), `00320890` (`b[glob+0x5A48+i*2]` byte→index
scan, `0xFF`/miss → −1) and `00264150` (global LP-suppress leaf
`b[020AA2AA]` — ships 0):

- **`002F8BB0(guest, objrow)`** — EXP share. Guest arm: `b5==0`,
  `0031B860` owner resolution required, `b4` outside `[0x1B,0x27]`,
  flags `(d64|d3C)&0x80000003==0`. Mode split on `0030D9A0()==1`:
  - *member-share (mode≠1):* `ebp` counts `0031B810(i)` hits over four
    `b[glob+0x5A5A+i*2]` member-map slots (member's own rec must pass the
    same flags/`b5`/`b4` gates; null rec counts; **`ebp==0` returns 0 —
    the entire compute is skipped**). Else
    `esi = ((b[rec+0x1C2]-b[rec+0x88])*d[e78+0x34] + d[e70+0x34]) / ebp`,
    **signed idiv truncating toward zero**; negatives pass through to the
    caller's clamp.
  - *leader (mode==1):* `idx = 00320890(b[glob+0x5AD5])`; guest must equal
    `00320AB0(idx,1)`'s member-map row else 0; `rcx==0` takes the full
    undivided value.
  - Guest mods: `b[+0x6B]|b[+0x7B]&8` → ×2; `&0x20` → 0.
- **`002F90C0(guest, objrow)`** — LP share. `00264150()!=0` → 0. Same guest
  gates except **no owner resolution** (unlinked guests get LP) and the
  `b4` acceptance set is `0x1A`/`<=6`/`>=0x28`. Formula
  `(b1C2-b88)*b[e78+0x2F] + b[e70+0x2F]` — **byte-width rates, no member
  divide, no mode split**. Guest mods: `&0x10` on `+0x6B`/`+0x7B` → ×2.
- **Semantic find:** the retain-scan flags `(d64|d3C)&0x80000003` re-gate
  inside both formulas — a `00377C20`-retained flagged guest is stashed but
  awarded 0. Retention is not payment.
- **Member-count subtlety:** `002367A0` matches `w[rec+4]` (word), so a
  `b5==1` record can never match a byte map value — the sourced row never
  counts itself; linked guest rows do (their `w+4==0`).

All EXP-199 `d228-*` asserted values survive byte-exact under real formula
inputs (`oar4` "link" rows supply the owner scan; `memslots` supplies the
member map).

### 13j. The display-request queue `003BBD00` family, executed — EXP-201

The "formatter family" pointer in the EXP-200 resume note resolves to the
**battle display-request queue** — the 64-entry 0x50-byte ring at
`q[02B457D0]` (index byte `02B443C0`) that carries damage numbers, reward
strings and icons toward the UI. Executed as shipped bytes (394/394,
stable ×3; sealed receipt `r-95260e713b7dba43` in `_experiments/evidence/receipts/`;
`NATIVE-REPLAY`, `live_game: false`):

- **`003284D0(obj, dl)`** — type-2 wrapper: `002FA3B0(q[obj+0x10])` distance
  gate; on pass enqueues `{subobj, movzx(dl), type 2}`.
- **`002FA3B0`** — distance gate: `003272A0` (`b[02089340]&0x10` → refresh
  camera vec3 `01EBBB00` from `q[gate+0x10]` pos), `00265020` reads
  `q[obj+0xB8]` vec3 when `(b[obj+3]>>5)-1 ∈ {0,2}` — **rejected classes
  leave a zeroed vec → dist 0 → in-range**; y forced 0; `003A1920`→`sqrtf`
  vs camera cell; return `dist < 24.0` strictly.
- **`003BBD00(req)`** — allocator: null table/occupied probe slot → byte
  `0xFF`; type-2 pre-gate `0035D330(0x1A,req+8)` rejects when
  `b[blk+0x24]==0xFF`; 64-slot scan marks same-obj categories; cat derive
  from marked classes else `rand()&1` → **cat ∈ {1,3}** only; type-2 second
  scan bumps every live type-2 `w3A += 3` and seeds `d[slot+0x44]` =
  `max(same-obj w38<=0 d44)+3`; `00506700` inits; second `rand()&0x1F` →
  scale `S = 1.0 + (rand&0x1F)*0.03125` multiplying the per-cat corner pair
  `T={(0,0),(-16,-16),(16,16),(16,-16),(-16,16)}` → `d[+0x14]/d[+0x18]`;
  `b[+0x3E]=cat`; index advances mod 64; returns `old|0x20`.
- **`00506700`** — clears 0x50, `w3A=1`, packed obj id `+8`, type `+0x3C`;
  type-0 formats `d[req+8]` via `003EFD00` into `+0x40`, name
  `"battle_4_c"`; type-1 name `"battle_4_p"` + byte-pair style lookups;
  type-2 name from `0035D330` resource (`w3A=3`, `b3D=4`, flag-dispatched
  colour `&2→1`/`&4→0x12`/`&8→0xB6`/`&0x10→0xF3`) + `002B3050` string.
- **`003EFD00(dst,val,width,zpad)`** — signed decimal writer; `val<=0` →
  empty string (count loop skipped, not a sign handler); pad fill `' '`/`'0'`
  by r9; divisor table `0xD11CE0`; returns total width written.
- **`0028FBE0`** — type-0-only dispatch: `b[+0xC]==0 && d[+8]!=0` →
  `003589B0` id → `00296280` scan → controller `q[q[0209BE80]+0x10F78]` →
  subtype jump table (7 arms → `296E90`/`297040` variants).
- **`0035D330(kind,id)`** — fills `d[022CA520]`/`+4`, calls `0031C5D0`;
  negative return memsets the 0x98 block to zeros (the `b24` 0xFF gate then
  **passes** — `bd00-t2neg`).

Corrections of record: the return is a byte — stale cookie bits ride upper
rax on `0xFF` paths; `02089340` is a shared dword (`0030B770` bits vs the
`&0x10` gate); `randn` call counts distinguish the cat-derive vs rand
paths.

### 13k. The type-0/type-1 post wrappers and the live `0028FBE0` dispatch — EXP-202

The remaining two wrappers of the display-request family now run as
executed entries (407/407, stable ×3; `NATIVE-REPLAY`, `live_game: false`):

- **`003283D0(obj, num, r8, r9)`** — type-0 number post: `edi = r8*2 | r9`;
  the subtype byte is **`b[01EED300 + (edi + off)*4]`** — byte 0 of a
  16-entry dword table (`02 04 01 03 06 08 05 07 …`), where `off = 4` iff
  `(rec==0 || b[rec+5]!=0) && 00263C20(q[obj+0x10]) != 3`; `d[req+8]` is
  `abs(edx)` (`cdq/xor/sub` — negative inputs format positive).
- **`00328480(obj, edx)`** — type-1 post: same gate → `{subobj, edx,
  type 1}`; `b[slot+0x3F] = b[req+8]`; `0024A5A0("battle_4_p")` + subtype
  byte-pair `w[0E02780 + b3f*2]` → two `002DD7E0` lookups → `d[+0xC]/+0x10`
  (`0x80808080` on miss; the type-0 style dwords at `0E027A8` always miss —
  e.g. `0x4F2B039D`).
- **`0028FBE0`'s 7-arm dispatch is now observed firing** (fixtures plant
  `00296280`'s `0209BFBE..0209C2BE`/`0xC0`-stride table entry —
  `b[e-0x58]|b[e] & 2`, id at `d[e+0x32]`, returns `e-0x7E` — and the
  `q[0209BE80]`→`q[+0x10F78]` controller chain): arm table `0x28FC8C` maps
  `[0,4]→00297040(0)`, `[1,5]→00296E90`, `[2,6]→00297040(1)`, `[3]→no-op`;
  subtype `8` makes `subtype-1 > 6` and skips dispatch entirely. Every
  subtype in the exercised set (`1,2,4,6,7,8`) was driven end-to-end —
  `d3d0-arm0/arm3/sub8` prove the full selection, not just the default arm.
- **Subtype feeding the dispatch is the record-aware `off`:** `d3d0-rec`
  (live `b5==0` rec → off 0 → subtype 2) vs `d3d0-near` (no rec → off 4 →
  subtype 6) vs `d3d0-c20` (`b[subobj+0xE]&0xF==3` → off 0 → subtype 2) —
  the byte is a *table lookup*, not `edi`, and the two quads of the table
  select different presentation arms.
- Still scripted: `00296E90`/`00297040` (the dispatch sinks — consumer
  side, next candidates), `0031C5D0`, `002B3050`.

### 13l. The dispatch consumers `00296E90`/`00297040`, executed — EXP-203

The two `0028FBE0` arm sinks now run as shipped bytes (418/418, stable ×3;
`NATIVE-REPLAY`, `live_game: false`). Both are flag-setters over a
`0x160`-stride slot array inside the `q[0209BE80]+0x10F78` handler object:

- **`00296E90(ctrlsub, id)`**: `idx = 00273320(id)` (still scripted);
  `idx<0` or null `ctrlsub` → no writes; else
  `w[idx*0x160+0x318] |= 0x10` and `w[+0x350] = 0` (OR-accumulate —
  `0x40` preset yields `0x50`).
- **`00297040(ctrlsub, id, flag)`**: `flag==0` → `w318 |= 0x20`,
  `w354 = 0`; `flag!=0` → gated on `b[idx*0x160+0x31E] != 3`, then
  `w318 |= 0x40`, `w356 = 0`. All six subtype arms now verified by real
  writes (`d3d0-*` assert `w318` bits `0x10`/`0x20`/`0x40` or untouched).
- Correction of record: EXP-202's own `d3d0-*`/`d480-*` assert group sat
  outside the EXP-201 elif predicate and ran vacuously in the `7926c92cd`
  run — the probes were right, the wiring was dead; the predicate now
  covers the names and the asserts observe real memory. `00273320`
  (id→slot-index resolver) is now the deepest scripted edge inside the
  dispatch consumers.

### 13m. The `00273320` id→slot resolver, executed — EXP-204

The last scripted edge inside the dispatch consumers now runs as shipped
bytes (424/424, stable ×3; `NATIVE-REPLAY`, `live_game: false`):

- **`00273320(id)`**: `id==0` → `-1` before any table read; else
  `n = movsx word [022C8064]` (signed — `0xFFFF` suppresses the scan),
  probes `0035BB00(i)` = `d[022C8084 + i*0xC0]` for `i < n`, first dword
  match → `i`, miss → `-1`. **The count is re-read after every probe** —
  the loop bound is live state, not a latched value.
- **`0035BB00(idx)`** = `d[022C8084 + idx*0xC0]`; **`0035BB60()`** =
  `movsx w[022C8064]`. Both cells are BSS (ship zero) — in shipped-static
  state every resolve returns `-1`, so the sinks' `w318` writes are
  suppressed until the table is populated; the `t3320` fixture raises it.
- The whole post path is now native end-to-end: `003283D0`/`00328480`/
  `003284D0` → `002FA3B0` → `003BBD00` → `00506700` → `0028FBE0` →
  `00296E90`/`00297040` → `00273320`. `d3d0-*` dispatch cases carry a
  real nonzero packed id (`w[subobj] = 0x1234`) so `00296280` match and
  `00273320` resolve both execute genuinely.
- Correction of record: the resolver's cells are `022C8064`/`022C8084`
  (an earlier transcription read `02282064`/`02282084`); it is a
  `0xC0`-stride dword-key scan distinct from `00296280`'s own
  `0209BFBE` table.
- Still scripted on this path: `0031C5D0`, `002B3050` — both confined to
  the type-2 arm now.

### 13n. The `0031C5D0` resource resolver, executed — EXP-205

- `0031C5D0` — the deep descriptor resolver the real `0035D330` calls to
  fill the `022CA520` block — is promoted to executed bytes (EXP-205,
  `EXP-205-resource-resolver-exec.md`), along with its `002F9860` bucket
  leaf. `003BBD00`'s type-2 pre-gate and `00506700`'s type-2 arm now run
  the real resolution twice per post.
- Semantics: `d[blk]` is the kind, dispatched over a 32-entry jump table
  (`kind-1 > 0x1F` → validate path → `-2`). Kind 1 is an auto-kind arm —
  `00309440` reads `d[01EEBCF8 + (w6>>0xC)*0x58]` = `5+hi-nibble`,
  rewrites `d[blk]` and re-dispatches. Validator `00322C50(0x1A,id)`
  gates on `q[02EBF118]` non-null and `id < d[T1+4]` — **`02EBF118` is
  `CASCD`, the per-bit cascade table**; the kind-0x1A L1 rows are the
  cascade rows. The arm resolves `w[row]` packed hi5→T2-table / lo11→T3-
  entry → `q[blk+0x18]` resource pointer, `b[row+2]` → `b[blk+0x24]` (the
  `0xFF` gate byte `003BBD00` checks), `002F9860(w[row+0xA])` →
  `q[blk+0x10]` (shipped-default `0x1CEB638` under null buckets), and
  `b25 = ((w6>>0xD)&1) | (b[row+0x24]<<1 & 0x1E)` → `00506700`'s four-bit
  colour dispatch `{0x12,0xB6,0xF3}`. A null T2 index table is graceful —
  `q18=0`, rest resolves, ret `0`. Negative ret → `0035D330` memsets the
  blk and the `0xFF` gate *passes*.
- Still scripted on this path: `002B3050` alone (~131-body CRT subtree —
  a separately bounded package).

### 13o. The `002B3050`/`002B3120` evaluator shell, executed — EXP-206

- `002B3050` — the last scripted edge — is not a formatter but a 0xC0B
  wrapper over worker `002B3120`; both are now executed bytes (EXP-206,
  `EXP-206-evaluator-shell-exec.md`). `00506700`'s type-2 arm calls
  `2B3050(0, str, slot+0x40, slot+0x42)`: `002AC1E0` inits a 0xD0 state
  struct; `0039BAD0(ctx)` byte query; if `00254A10()==0 && bl==7`,
  `bts d[state+0x64].0xB` + `0039C4A0(bit)` → `q[state+0x80]`; then
  `002B3120` — null `q[state+0x28]` → two zero words/ret 0, else it
  copies the struct and calls the real evaluator `002B24B0` (stubbed —
  the CRT subtree), then **`w[outW1]=cvtt(f0)`, `w[outW2]=cvtt(f1)`** —
  two truncated floats, the string's measured dimensions — and returns
  `movsx b[rsp+0x50]`. The str pointer reaches the evaluator through
  the `[rsp+0x50]` cell and the result byte overwrites it.
- **Every body on the display post path now executes as shipped
  bytes.** Remaining stubs are only the `002B24B0` evaluator core and
  five leaf helpers (`2AC1E0`/`39BAD0`/`254A10`/`39C4A0`/cookie).

### 13p. The `002B24B0` line-layout wrapper, executed — EXP-207

- `002B24B0` itself is now executed bytes (EXP-207,
  `EXP-207-line-layout-wrapper-exec.md`). It **snapshots the shared
  text context `q[0209CC40]`** — `d10D8`/`f10E8`/`q10C8`/`b10FC`/
  `b10FF` plus outer `q[0209CC48]` swapped to null mid-eval — clears
  the accumulators (`d10FC` dword store = bulk clear `+0x10FC..0x10FF`),
  runs the inner measurers `002B2150`/`002AF340` (boundary-stubbed),
  applies **`ceilf`** to both measure floats (`f[+0x54]`/`f[+0x58]`),
  distributes `d10EC`→`+0x60`, `d10F0`→`+0x5C`, `b10FD`→`+0x50` (the
  return byte), `b1100`→`+0x51`, merges `acc+ec > f54 → f54=acc+ec`
  else `f60=f54−acc` (strict `>`, equal goes else), accumulates
  `f10F4 += 2*d[01E0CDC0]*s34*s38` when `b10FE` (`+32·scale` shipped),
  and restores every saved field. `+0x10EC` is dual-read as dword and
  float — the running-total/max semantics of the multi-line measure.
- The display path is now native **through the evaluator itself**;
  only the inner glyph-run measurers and five leaf helpers remain
  boundary stubs.

### 13q. The segment-string walkers `002B2150`/`002AF340`, executed — EXP-208

Both inner measurers promoted to shipped bytes (plus the `0xD0` state
initializer `002AC1E0`): **450/450, stable ×3, hash `78ec7301…`**
(`_experiments/EXP-208-segment-string-walkers-exec.md`). The helper
subtree stays bounded — control decode `002AC2F0`, interpreter
`002AC5F0`, tag-`0xE` adjuster `002B3E30`, and the `17Fxxx` font shims
are scripted boundaries; `memcmp`, `0020E600`, `ceilf` math and the
cookie run native.

- `002B2150(&state, cursor, &w, &h)` is the single-line walker: it
  saves `b10FC`/`b10FF`, `q[0209CC48]` (cleared mid-walk), the font
  `+0x28` getter/setter pair, `q[0209E598]` and the `0209CC60` scratch
  band, and restores all on exit. Heavy bytes (`>0x0F`) run the
  decode→elemb→remap→`0x80000000` flag chain (flag set → `b10FC=1` and
  the `×2.3f` scale advance when already `2`; clear → `b10FC=2`);
  lite bytes hit the `q10C8` match-word gate or `002AC5F0`. It returns
  **bytes consumed** and writes `f[r8]`/`f[r9]` — `r9` is `&ctx+0x10E8`
  in the `2B24B0` call, which is why that field doubles as the
  line-height slot.
- `002AF340(&state, cursor, &params, gate)` is the multiline variant:
  per-node `f10 += f[0209CC68]`, `f14 = max(f[0209CC64])`; **tag 3 is a
  line break** (`f20`/`f30`/`f34` max-merge + line reset); **tag 2 is a
  nested `2B2150` inline measure** (`b1102=1`, outs merge into `f10`/
  `f14`, `ctx+0x10E8` tracks the max nested height); **tag `0xE` calls
  `002B3E30`**; NUL or an `r15`-`memcmp` match runs the **final flush**
  — critically, a `2AC5F0`-returns-0 break **skips it**, leaving
  `f30`/`f34` at 0. It returns the heavy-node count (`r12d`), or `-1`
  under the r9 gate.
- `b10FC` writes persist out of `2AF340` — save/restore of the mode
  bytes is `2B2150`'s layer, not this one's.
- `bd00-t2` now end-to-end native: `2B58B0` resolves the name pointer,
  `2B3050` walks `\x05\x00` through both real walkers, the
  `af340f` accumulators land `17.9/4.2` through the NUL flush, `ceilf`
  → `18/5` pixels in the slot.

### 13r. The text-control interpreter `002AC5F0`, executed — EXP-209

The interpreter below the walkers promoted to shipped bytes, plus five
leaf helpers (`00229E40` global-dword, `0024ABA0` const-float,
`002B1F20`, `002B2C50`, `002B2D20`): **455/455, stable ×3, hash
`4cca9cf5…`** (`_experiments/EXP-209-text-control-interpreter-exec.md`).
The deep subtree stays bounded — `002A9F00`, `002B2DF0`, `002B43C0`,
`002AB820`, `003FFDF0`, `002B3E30`, `002AC2F0` and the `17Fxxx` shim
family are scripted boundaries.

- `002AC5F0(state, &cursor_cell, params, &aux)` — `rdx` is **&cursor**
  (a cell), not the char pointer the walkers take. `*aux = 0`; `b==0`
  → ret 0; `q[state+0x10C8]` match-word → ret 0; else a 15-entry jump
  table at `0x2AE334` dispatches tags `1..0xF`.
- **Tag 5 (space/advance):** `24ABA0` shipped `448/448=1.0` × const
  `15.0f` → `f[0209CC68]=15` advance, `17F880` → `f[0209CC64]` height;
  `b[ctxo+0x10FC]=0`, `b[ctxo+0x1100]=1`, `d[aux]=1`, cursor+1, and a
  **nested `2B2150`** under `ctx48==0` (`r9=0` — the height-out write
  tolerates it). A `\x05` run measures **15×7 px** through real
  `ceilf` — replacing EXP-208's stub-driven `18/5`.
- **Tag 14 (parameterized):** `003FFDF0` parse → `b1101=1`, `b10FE`
  from the parse dword; `002B2DF0` wrap; **returns 0** — `002AF340`'s
  `0xE` post-break `002B3E30` fires through that break, not a direct
  call. `b10FE` feeds `002B24B0`'s `+32*scale` accumulate.
- **Tags 8/9:** cursor `+3`/`+1`, ret 1. **Tags 11–13:** no-op ret 0 →
  caller break. Tags 1/4/6/7 share `0x2ACB96`; tag 15 re-dispatches
  through a second table at `0x2AE370`.
- The interpreter's ctx marks (`b10FC`, `b1100`, `b1101`, `b10FE`,
  `f10EC`/`f10F4`) target the **global** `q[0209CC40]` object and
  persist; the walkers' save/restore covers the passed state.
- `b10FD` (the `2B3120` return byte) is read-only across the family —
  real streams return `eax = 0`; earlier nonzero returns were stub
  artifacts.

### 13s. Every `002AC5F0` arm exercised — EXP-210

No new bodies promoted; all 15 dispatch arms now executed through
direct `2AC5F0` entry (`ccp` cursor-cell fixture): **466/466, stable
×3, hash `8b721870…`**
(`_experiments/EXP-210-remaining-interpreter-arms-exec.md`).

- **Shared advance arm `0x2ACB96` (tags 1/4/6/7):** advance =
  `17F920(0/1)` for tags 1/4, shipped `10.0f` const for tag 6,
  `d[01E02E14]==7 ? 0x1A : int(24ABA0·10.0)` for tag 7 — all `×f34·f38`
  into `f[cc68]`; height `int(17F880) ×f34·f3C` (note the different
  `+0x3C` scale and the integer truncation vs tag 5's float).
- **Tag 2 returns 1** — nested `2B2150` on `cursor+1`, results folded
  into `f[params]`/`f[params+4]`, `b1102=1`, `cc60`-band and `e598`
  cleared; `b[state+0xAA]>0` overrides `f[params]`; `q[state+0x20]!=0`
  → the `17F850`/`17FA10`/`2AB820`/`17FB00` tail block.
- **Tag 3 = line break:** cursor+1, `e598`/`b10FC` cleared, ret 0.
- **Tag 10 mutates the string:** scans `cursor+1` for `02`/`05`, nulls
  the hit byte, nested-measures, restores it; `f10F0`/`f10F8` updated.
- **Tag 15 re-dispatches** on the next byte through the second-level
  kind table `0x2AE3FC` + jump table `0x2AE370` (`idx ≤ 0x50`).

### 13t. Tag-15 second-level sub-arms — EXP-211

Two decoders promoted real (`003FFAB0` param decode, `0039BA00`
escape-table lookup over the runtime BSS table `0x2AEE870` — planted
via the `ba00t` fixture); 35 sub-arm cases through direct `2AC5F0`
entry: **503/503, stable ×3, hash `d3378248…`**
(`_experiments/EXP-211-tag15-second-level-arms-exec.md`).

- The jump table is **kind-indexed**: `idx = sub − 0x20`,
  `kind = b[0x2AE3FC + idx]`, `target = base + d[0x2AE370 + 4·kind]` —
  sub bytes share arms (`0x25`/`0x26`/`0x27` = the align family
  `2B1F20` dispatches on; `0x2C`/`0x2F`/`0x3B`/`0x70` = one param-skip;
  `0x40`–`0x6B` = a catch-all through `2AEB20`).
- Executed arms: quoted-skip `"`, param-skips, `$` field write, `#`
  escape/world-wrap marks, `!` font select (+2 cursor), align
  `%`/`&`/`'`, `(`/`7` h/v-scale `÷24`/`÷100`, space ` ` advance×kern,
  `)` colour (top byte preserved from `b33`), `+` alpha hi-nib merge,
  `-` `3FFC60`+`2AE610`, `1` `3FFF10` skip, `3` scale pair, `4`/`5`/`6`
  field/param writes, `o` word param, `2` inline `cc68` advance,
  `V` aux clear, `0x40`–`0x6B` catch-all, `0x30`/`0x5F` ret-1.
- **Correction of record:** the semantic asserts for every
  `b3120-*`/`b3050-*`/`b24b0-*`/`b2150-*`/`af340-*`/`c5f0-*` case were
  dead since EXP-206 (nested under an outer elif that omitted those
  prefixes). Now live; `229E40` reads `d[01E02814]` (not `01E02E14` as
  §13s states), the prologue zeroes `d[r9]`, `2B3050`'s `39C4A0`
  result lands `state+0x60`, and `2B24B0`'s `b1100→+0x51` copy is gated
  on `b10FE`.

### 13u. Tag-15 deep param-parser family — EXP-212

All nine deep parsers the tag-15 sub-arms call promoted real —
`003FFEE0` (`"` quoted-skip), `003FFBC0` (`)` colour decode with
`39BA00` escape), `003FFD70` (`*` icon header: `w44`/`w48`/`rest`
outs, `ret=len+3`), `003FFC60` (`-`), `003FFCE0` (`.`/`l`),
`003FFDA0` (`3` scale pair `÷10.0f`), `003FFB00` (`o`/`8` word),
`003FFB90` (`m`/`n` skip), `003FFF10` (`1` skip) — plus the remaining
dark kind arms exercised: `519/519, stable ×3, hash dc081df2…`
(`_experiments/EXP-212-deep-param-parser-family-exec.md`).

- `.`/`8`/`9`/`:`/`<`/`=` are parse-and-write or parse-then-early-ret-1
  arms (`state+0x70==0` gate for `.`, `2639E0` zero ret for `8`,
  `263990` zero ret for `>`); `9`/`:`/`<`/`=` write `bAB`–`bAE`.
- `?` runs a `0xD0` state copy + `2AE450` publish (`b10FC=1`, `bA9=0`,
  `d[aux]=1`); `>` chains `263990`/`2B41F0` on `q[e312+0x78]`.
- **`*` correction of record:** both nested `2B2150` walks (on `rest`
  and `rest+w48`) are **unconditional** — `w48<len`/`w44<len` gate only
  the byte suppresses; the second suppress target is `rest[w48+w44]`.
  Heavy bytes in the icon blob need the real decode chain
  (`e312q0x60`/`c2f0`/`eflags`). `ctx48!=0` publishes via `2A9F00` and
  restores ctxo `d10D8`/`d10DC`/`f10E4`.
- New scripted boundaries (disclosed): `263990`, `2B41F0`, `2AE450`.
  The `*` icon-fit clamp reads `2B43C0` stub rets; `l`'s `2B4730` tail
  and `8`'s nonzero `2639E0` path stay fixture-dark.

### 13v. Tag-15 resource-lookup chain — EXP-213

The `!`/`8`/`>` arms' resolvers promoted real — `0039BA30` (font-record
scan over inline BSS table `0x2AEE810`), `00263990` (`>` named-record:
`w[obj+0x102]<0` → `q[obj+0xF8]` direct, else the shared chain),
`002639E0` (`8` index), `0032A930` (alloc-bitmap bit-test over
`2EF2B0()`=`0x2164480`, bit at `+0x13B4`), `003EAC10` (pair-table
`q[0x2B5E0D8]`, `entry[2·idx+flag]` **returns a dword used as a string
pointer**): `521/521, stable ×3, hash 2b0f36d4…`
(`_experiments/EXP-213-resource-lookup-chain-exec.md`).

- `!` now runs the real font-record scan (`w6` count, `d[rbx]` strides,
  `wC>0x30 && d30==0x8000` match) before `q68`/`q60` and the `254A10`
  mode split.
- `8`/`>` nonzero-resolve tails run native for the first time:
  `0xD0`+`0x80` state copies, NUL-scan, suppress `r13[len]`, `2B41F0`
  measure → `w[copy+0x1c]`, unconditional nested `2B2150` on the
  resource, then the shared `2A9F00` publish + ctxo restore.
- Corrections of record: `39BA30`'s table is inline at `0x2AEE810`
  (not a pointer); `e312q`-style name resolution requires fixture
  allocs ordered before the preset loop.

### 13w. Measure wrappers `2B41F0`/`2B43C0` — EXP-214

Both measure wrappers promoted real — `002B41F0` (default-state
template: `861EC0` memset + `39C4A0` pick → `q[copy+0x60]` flag desc,
NUL-scan, ctxo `10C8` swap) and `002B43C0` (caller-state `0xD0` copy,
installs `orig_rsp+0x18` into `q[ctxo+0x10C8]`) — both tail into the
already-real `2AF340` evaluator: `521/521, stable ×3, hash
76e775e1…` (`_experiments/EXP-214-measure-wrapper-chain-exec.md`).

- Every measure call inside the `*`/`8`/`>` deep tails now runs real —
  the `*` arm's two suppress-measures (`rest[w48]` → `2B43C0(rest)`;
  `rest[w48+w44]` → `2B43C0(rest+w48)`) each execute a full glyph walk.
- Correction of record: the real wrappers' `0x200`+ frames pushed the
  deepest nested decode below the harness stack floor — stack map
  extended 1 MB; the `*` suppress/measure order is now verified from
  call args (w48 first, w48+w44 second).
- Still scripted: `2A9F00` publish, `2AE450`, `808C40` cookie,
  `39C4A0` (its return feeds `q[copy+0x60]` via `s39c4a0_ret`).

### 13x. Publish/draw helpers `2A9F00`/`2AE610`/`2AE450`/`39BB00` — EXP-215

The publish tail went real — `002A9F00` glyph-run publisher (per-glyph
`17F8C0` remap, `20E600` glyph-row, quad-command records into the
`q[0209CC50]` display-list cursor, `d[ctxo+0x10D4]` batch counter,
real `2AC5F0` re-interpret of embedded `0x0F` codes), `002AE610`
`-`-decoration measure+publish (state copy, `39C4A0` pick, real
`3FFC60` re-parse, `d44&0x800`-gated deep measure), `002AE450`
`?`-arm sprite draw (`39BB00` mode dispatch real → `q[0208EA90]`/
`q[0208EAA8]`/`q[q[0209AC30]+0x338]` BSS singletons → sprite record →
metric dword → `f[0209CC60/64/68]`): `521/521, stable ×3, hash
6a5b2d66…` (`_experiments/EXP-215-publish-draw-helpers-exec.md`).

- The `*`/`8`/`>` publish call sites (`0x2AD728`, `0x2ADABA`,
  `0x2ADFED`), the `-` arm's `2AE610` tail, and the `?` arm's sprite
  draw all execute shipped bytes end-to-end now.
- Corrections of record: `2AE610` reads the `39C4A0` font record on
  **both** paths (`s39c4a0_ret` required unconditionally); the publish
  consumes its own `2AC2F0` decode per glyph (`f2ac` `c2f0` 2→3);
  Unicorn fault-hook RIP can lag up to ~0x380 inside a translation
  block — trust `ibs` bytes at RIP, not file disasm at the VA.
- New boundaries: `2AFDC0` render submit, `17FC90` quad build,
  `17F7C0` emit — all sinks whose return values are unused.
- Still scripted: `2B4730`/`3A1DB0` display-list append (unplanted
  `q[0209CC48]`/`q[0209E5A0]` globals), `2AEB20`, `2B1FB0`, the
  `17Fxxx` font shims, `39C4A0`, `2AC2F0`, `808C40`.

### 13y. Display-list append `2B4730`/`3A1DB0`/`36F360` — EXP-216

The append chain went real — `002B4730` drains the publish cursor into
`q[0209E5A0]` command records (`count|0x10000000` header, `0x6C008150`
cmd word, `0x10000000`/`0x15000000`/`0x13000000` terminator,
`q[ctx48+8]` align-add, `ecx`-gated slot-table cursor restore),
`003A1DB0` double-buffer ring flip (`d[02EBEFF0]` toggle, record count
from the current slot's pointer pair, other slot's cursor reset),
`0036F360` command-stream terminator (`0x30000000` last-record check,
`0x200` cap, `q[r9]=0x10000000` patch, `d[02EBA3F8]` bookkeeping):
`523/523, stable ×3, hash d0bdfc30…`
(`_experiments/EXP-216-display-list-append-exec.md`).

- Two direct-entry cases (`b4730-flush` ecx=1, `b4730-noflip` ecx=0)
  exercise the full body — inherited cases never reach the publish
  `d10D4>=0x14` batch threshold.
- Corrections of record: `q[ctx48+8]` is an align-add cell, not a
  pointer chase (needs the `ctx48o` object fixture); `36F360`'s several
  bookkeeping accesses all resolve to the single cell `0x2EBA3F8`.
- New fixtures: `ctx48o` object + `+8` cell, `b4730p` ring layout
  (`02EBEFC0`…`02EBEFF0`), `q[0209E5A0]` list buffer.
- Still scripted: `2AFDC0`/`17FC90`/`17F7C0` emit sinks, `2AEB20`,
  `2B1FB0`, `17Fxxx` font shims, `39C4A0`, `2AC2F0`, `808C40`.

### 13z. Measure/skip helper `2B1FB0` — EXP-217

`002B1FB0` promoted real — standalone measure/skip helper (memset
`0xD0` default state, `39C4A0` pick stored-unread, `b[arg]` dispatch:
`>0xF` → `2AC2F0` decode, `<=0xF` → real `2AC5F0` interpreter, returns
bytes consumed). All callees already mapped; two direct-entry cases
(`b1fb0-c5` kind-`'m'` real skip, `b1fb0-dec` decode-stub path) cover
both sides — none of its seven static callers are on the harness paths
yet: `525/525, stable ×3, hash 9ba88990…`
(`_experiments/EXP-217-measure-skip-helper-exec.md`).

- Still scripted: `2AFDC0`/`17FC90`/`17F7C0` emit sinks, `2AEB20`,
  `17Fxxx` font shims, `39C4A0`, `2AC2F0`, `808C40`.

### 13aa. Cookie leaf, font select, `?`-arm submitter, soft-reset — EXP-218

Five more bodies promoted real in the same harness: `00808C40`
(`__security_check_cookie` — the compare/rotate leaf now runs shipped
bytes on every cookie-protected exit; the report path is never taken),
`0039C4A0` (BSS font-record select `q[02AEE800]`/`q[02AEE808]`),
`002B1ED0` (ctx metric soft-reset — `d44&0x800` picks the
`17F980`/`17F960` vs `17F8A0`/`17F880` method pair, both landing on
`f[0209CC70]`/`f[0209CC74]`), `002AFDC0` (the `?`-arm quad submitter —
real command records into the publish cursor, unconditional
`2B4730(1)` flush, device emit tail), `002DD8B0` (vertex-format leaf):
`525/525, stable ×3, hash bb2d38d2…`
(`_experiments/EXP-218-cookie-fontsel-submit-exec.md`).

- Correction of record: the EXP-216 ebx-tail slot model was wrong —
  the ring-pair array `02EBEFC0 + d[02EBEFF0]*24` supplies the
  restored cursors, not `02EDF9C0`/`02EDF050`. The `b4730-`/`b1fb0-`
  assert blocks had been dead since creation (missing from the assert
  elif's prefix tuple); they are live now.
- Still scripted: `2DD860`/`181560` emit helpers, the
  `181xxx`/`1Bxxxx` render-device subtree (`1B1C00` singleton getter
  → `q[01F811E8]`), `17FC90`/`17F7C0`, `2AEB20`, `17Fxxx` font shims,
  `2AC2F0`.

### 13ab. Kind-`0x1C` catch-all `2AEB20` + emit internals — EXP-219

The nested `0x1C`-arm worker and the emit plumbing it shares with the
publisher are now real: `002AEB20` (462 insns — sub-kind flag dispatch
via `2AB8F0`/`1E0C10`/`1E0C30`/`2DDC50`/`180150`/`228480`/`2441E0`
leaf chain, byte-table record index into `ctxo+idx*24`, pre-loop
publish globals from `arr[cnt-1]` → `f[0209CC60/64/68]`, `cnt-1` quad
records at `q[0209CC50]` stride `0x70`, real `2B4730(1)` tail flush,
`eax=2` consumed), `0017FC90`+`1B5FA0`+`1E9C40` (quad UV/scale write
into `q[01F811F8]+0x137C`), `0017F7C0` (0xA0 matrix copy → `1E8070`
submit — the deep apply stays scripted `s1e8070`), `002DD860` +
`202B70` + `217060` (corner emit → 4×4 mat×vec → projective divide):
`525/525, stable ×3, hash c7d7db08…`
(`_experiments/EXP-219-kind1C-catchall-emit-internals-exec.md`).

- Correction of record: the scripted `2AEB20` had claimed `eax=3`
  consumed — the real body returns 2 (`q[ccp]+=2`, `nstr+3`).
- Correction of record: `1E0C10`'s singleton is `q[01F7FFE0]` and
  `1E0C30`'s `q[02EA5368]` (earlier estimates were off; exact
  RIP-relative decode is the authority).
- `q[state+0x20]` (the `2DD860` matrix) is a semantic null-gate — it
  must stay null in cases asserting the `0x20`-tail skipped
  (`c5f0-tag2`); the identity-matrix fixture `emat` is opt-in.
- Still scripted: `1E8070`, `181560` + the six `181xxx` device
  wrappers (`q[01F811E8]` render-device object unplanted), `17Fxxx`
  font shims, `2AC2F0`.

### 13ac. Vertex-batch submitter `1E8070` + the `17Fxxx` metric/getter family — EXP-220

EXP-219's deepest scripted boundary and the whole font-metric shim
family are now real: `001E8070` (278 insns — `d[state+0x9C]` mod `0x1C`
→ `1E94E0` ext-record, 2×3 vertex expansion into `0x3C`-byte records
appended to `q[dev+0x10]`'s vector with `1E7A20` realloc, per-vertex
bounds into slot `d[dev+0x20]` at `+0x2324..+0x233C` comparing raw
stream floats, `b[+0x2349]` derived-flag arm, `f[dev+0x137C]` scale
reset), `001E7A20` (vector `_Emplace_reallocate` — allocator vtable
`+0x10`/`+0x18` scripted), `001E94E0` (lazy record getter at
`dev+0xF68+idx*36`, flag-0 init `19C5D0`/`1C5F20` scripted), the nine
`17Fxxx` thunks → `1E93C0`/`1E9450`/`1E9580`/`1E9610`/`1E9840`/
`1E9BD0`/`1E9860`/`5C52D0`/`848C20` (metric map `q[01F81200]` →
`1B51C0` find → `ceilf(d[val+X]/f[val+0x34])` or `f[00901990]`=23.0
miss const; codepoint remap → `1FDEC0` inline map; `q[dev+0x28]`
saved-ctx getter/setter), and leaves `1B5FB0`/`1B51C0`/`1B1620`/
`1FDDB0`/`225670`/`79CFA0`/`225690`/`79E3C0`/`16D6A0`:
`536/536, stable ×3` (+11 cases)
(`_experiments/EXP-220-vertex-submit-metrics-family-exec.md`).

- Correction of record: `17F880` is `ceilf(d[val+0x30]/f[val+0x34])`
  — the stub's flat 6.5 understated it; the fixture's `13/2.0` yields
  `7.0`. `17F920`'s arms are `d[+0x20]`/`d[+0x1C]` (6/5 here).
- Correction of record: `1E8070`'s bounds accumulate the **raw**
  stream floats `f[st+0x1C+k*4]`/`f[st+0x2C+k*4]`, not the computed
  positions; the B-mirror min_y lives at `(slot+0xCD)*0x2C`.
- Still scripted: `181560` + the six `181xxx` device wrappers,
  `1E94E0`'s flag-0 init callees (`19C5D0`/`1C5F20`), allocator vtable
  fns, `2AC2F0`, sibling thunks `17F850`/`17FA10`/`17FB00`/`17FD30`.

### 13ad. Render-device op tail `181xxx` → `1Bxxxx` — EXP-221

The emit tail's last scripted boundary — the six device-op wrappers —
now runs shipped bytes through `001B1C00` (`q[0x1F811E8]` render-device
singleton): `001B1910`/`001B0100` reset (slot-clear loop over
`dev+0x2328` stride `0x58` to cursor `d[+0x3928]`, memset `+0x3930`
×`0x178`, four `0x80` seeds at `+0x3A4C..0x3A58`), `001B2410`
texture-region props (`+0x3930/+0x3934`, name copy `17D2E0`→`16D670`
CRT-options→scripted `scrtfmt` sink on the `q[0x8C2F08]` target, stack
args → `+0x3AA0`/`+0x3A38..0x3A48`), `001B2490` mode table
(`d[0x8F80F8+edx*4]` → `+0x3A60`; `tbl[3]=2`), `001B06D0`/`001AED50`
slot-vector append+`vector<0x30>` realloc (fn-ptr allocator `+8`/`+0x18`,
cap 2→4→8 verified byte-for-byte), `001B22D0`/`001B22E0` qword stores
(`+0x3A68`/`+0x3A70`): `540/540, stable ×3` (+4 cases)
(`_experiments/EXP-221-render-device-op-tail-exec.md`).

- Correction of record: `1819A0`'s name-copy arm **does** fire — the
  name is the wrapper's `r8` forwarded as `1B2410`'s `r9` (the earlier
  resume note read the wrapper's own `r9`). `181460` is a `(edx−2)×3`
  nested emit loop, not a thin forwarder.
- Still scripted: `181330`→`1B03D0` (the deep tail op), the `q[0x8C2F08]`
  CRT callee (`scrtfmt` bounded-copy sink), slot-vector allocator slots,
  `19C5D0`/`1C5F20`, `2AC2F0`, sibling thunks.

### 13ae. Control-code decoder `2AC2F0` + `254A10` — EXP-222

The `>0xF` heavy-char decode boundary inside the text walkers now runs
shipped bytes: `002AC2F0` (187 insns) decodes `b[cursor]` — printable
arm `esi = b−0x20` (+1), tag arm `esi = b[cursor+1]−0x20 +
d[0x916570|0x9165B0 | (al&0xF)*4]` (+2, shipped 16-dword tables, BSS
`d[0x209CC38]` selects) — then publishes the `0x209CC30`/`0x209CC60..7C`
globals: real `39C4A0` font pick → `q[ctx+0x60]`, scripted `17FD30`
setter, real `17F980/17F960`/`17F8A0/17F880` metric pair on
`d[ctx+0x44]&0x800`, `20E600` element row → `q[0x209D698]`, `17F8C0`
glyph remap, `17F9C0` kern or `(q[r14]>>0x20)&0x1F` fallback, the
`17F8E0`→`1E9780`→`1FDDD0` two-level devsub map find → `1E9BD0` ceilf
kern2 when `17F940()&&rbx&&d[rbx+0x20]≠−1`, `17FAE0` publishing `rbx`
into `q[dev1+0x28]`, the `splat(f34)`-scaled quad at `0x209CC60` and the
bA9 writeback. `00254A10` is the lang-set check (`d[0x1E02814] ∈
{0,7,8,10,11}` via `bt 0xD81`, 55 call sites). Result: `540/540, stable
×3`, hash `ff908d9c` (`_experiments/EXP-222-control-code-decoder-exec.md`).

- Correction of record: the `s254a10` stub's default-0 polarity was
  inverted — real `254A10` returns 1 for `d[0x1E02814]==0`, so every
  `254a10==0` arm previously ran under a value the shipped body never
  produces there; those cases now plant `e2814v=1`. This surfaces a
  dead shipped arm: `254a10()==0 && 229e40()==7 → 0x1A` can never fire
  because lang 7 is a set member (`c5f0-tag7a` now asserts the real
  60.0, not the stub-fiction 156).
- Still scripted: `17FD30` (`s17fd30` ×19), `1B03D0`, `scrtfmt`, the
  allocator sinks, `1E94E0`'s flag-0 init pair, sibling thunks
  `17F850`/`17FA10`/`17FB00`.

### 13af. EXP/LP-share accessor tail `312280` — EXP-223

The six scripted boundaries inside `00312280`'s distribution tail now
run shipped bytes: `00253690` FP-total getter (`d[q[0x02092758]+8]`),
`00254EE0` FP setter (delta → `316A50(cl=6|7 on full ecx, |delta|)` →
clamp+store `[0,0x5F5E0FF]`), `0028FB80` paired source-share
(`00289D00` ×2 into `q[0x0209BE80]+0x5380`, r9d=0 EXP / 1 LP),
`00469E80` delta notifier (`ecx>0` → `0046AB10`), `00317090` FP-stat
add (`(d[+0x1C2]−d[+0x88])·w[e78+0]+w[e70+0]` → `253770`→`316A50(0x11)`),
`003171C0` member-seen (`316A50(4,1)` early, `263C20!=3` gate,
`w[e68+0x52]!=0xFFFF` → `253750`→`315820` counter
`b[q[0x020927C0]+id+0x3404]`). New fixtures: `fptot` (FP-total object),
`msgtab`/`e68w52`/`objlink` (message-counter path), `fbdev` (paired-slot
device), `e78w`/`e70w` multipliers; `rargs` widened to 5 columns for the
r9 pair-selector. Result: `541/541, stable ×3`, hash `91bdc2e8` (+1
case `d228-msg`) (`_experiments/EXP-223-explp-share-tail-exec.md`).

- Correction of record: `254EE0`'s `mov cl,6|7` patches only the low
  byte — `316A50` receives `ecx = (value & ~0xFF) | kind`, not an
  isolated kind; `3171C0`'s `316A50(4,1)` is an unconditional
  per-member tick fired before its gates.
- Still scripted: `317ED0`, `316A50` (all notifies recorded), the
  `319490`→`3377C0` entity-context chain plus `3180F0`/`319CA0`,
  `46AB10`, `s7ed0`, allocator sinks.

### 13ag. Member-slot accessor tail `317930`/`318B40`/`31A630` — EXP-224

The member/foe slot-write gate and rebalance chain under `0023AC80` +
`0031A630` now runs shipped bytes: `00317930` slot-accept probe
(sentinel table `0x20107E8` → `322C50(6,id)` memt range → `a5`-gated
`309EC0` free-count → memt row `b7>>5 == cursor` + cursor-1 pair-tag
compare → `323C60`), `00318B40` pair rebalance (`w[pair]`==FFFF →
unconditional normalize `0x1000`; memt `b[+0x11]`/`b[+9]` tag compare →
clear/self-reset), `00324100` effective grade (`324020` popcount floor
+ bits 18..30 → `308FF0`), `00324020` (**popcount** of `rec+0x194`
bits 0..17 — not a highest-bit scan), `00323C60` allow-check
(`322C50(1,id)` auto-class → `b7&0x10` → `323BB0` bitmap ∩), `003243F0`
unlink helper, `0030C650` level-set growth (FOED row + `grwd`
`2F9A60`/`2F9B20` zero-growth passthrough + own `fed0(*,0)`),
`00323910` license grant/revoke, `00308FF0` grade (`d138` row
`b[+0x1E]`∈{5,6}→`b[+0xA]`), `00308040`/`00308130` accessors.
`322C50` is a 31-entry kind jump table (kind-6 = memt
`[0x1000,0x1000+d[+4])`; kind-1 auto-resolves class via `309440`,
`page=id>>12`, `class=d[0x1EEBCC0+page*0x58+0x38]`); `309EC0`'s page-1
dispatch is shipped-authored (`q[0x1EEBD18+8]` word table, handler
`2FD8D0` mode-0 = cap−count). Result: `541/541, stable ×3`, hash
`afa50681` (`_experiments/EXP-224-member-slot-accessor-tail-exec.md`).

- Corrections of record: `324020` is a popcount; `317930`'s `322C50`
  kind is constant 6 (`lea ecx,[r8+6]` reads a zeroed r8); `309EC0`
  free-count 0 vetoes `31A630` (`a630r9-clamp` now asserts real −1, no
  writes); `31A630` calls `318B40` after every write including the
  FFFF-sentinel arm, and `318B40` normalizes `w[slots0]` FFFF→0x1000
  unconditionally; real `30C650` emits its own `fed0(*,0)`.
- New fixtures: `memt`/`memt_rows` (`q[0x2EBF0F8]`, rows at
  `id−0x1000`), `m98d` (`q[0x2EBF098]` class-7 range), `grwd`
  (`q[0x2EBF108]`, `c228` default), `d138` wired into `o4100-*`/
  `g3910-grade*`. Foe-path slot ids re-ranged `0x501/0x502`→
  `0x1101/0x1102` (real kind-6 range rejects the stub-fiction ids).
- Still scripted: `30FED0` (`fed0` ×173), `316A50`, `30F9A0`/`30C410`,
  `3008A0`, `31B860`, `324470`, the `3105D0`/`313F60`/`300E40`/
  `2E42D0`/`2699D0`/`2ECEC0` teardown sinks, the `317ED0`/`319490`→
  `3377C0`/`3180F0`/`319CA0` entity-context chain, `46AB10`,
  allocator sinks.

### 13ah. Unlink/teardown leaf family `2ECF10`/`313F60`/`17FD30`/`2699D0`/`2ECEC0` — EXP-225

The unlink/teardown leaf family reached by `003243F0` + `0031A630` now
runs shipped bytes: `002ECF10` unlink leaf (`q[obj+0xC0]` null
early-out; the `b[obj]&0x40` arm → `426130`/`427320` stays gated),
`00313F60` (**thunk `jmp 0x377C20`**), `00377C20` can-use flag
(`3148F0()` row index `d[0x21654C4]` BSS-zero →
`w[q[0x2ADD100]+8+row*3]>>15` — existing `cd_words`/`cd_idx` fixtures;
`cd7c20` tag ×101), `0017FD30` flag wrapper → `001E9D20` map-find+set
on the `q[0x1F811F8]` device singleton (**null-map early-out also
zeroes `dev1+0..+0x24`** — stub-era shim skipped it), `002699D0` →
`002EB430` teardown writes (`b[obj+0xD]&=0xFE`, `b[+0xF5]=0xFF`,
`d[+0xEC]=0`, `d[+0xF0]=0x1001`; `2EB0D0` only when `b[+0x18]==1`),
`002ECEC0` element teardown (`q[0x22C6F28]+idx*0x740`, `+0x284` gate →
`003AEEF0(+0x550)` bounded chain-clear, new `u43f0-ec` deep case).
Result: `542/542, stable ×3`, hash `9ed60fb8`
(`_experiments/EXP-225-unlink-teardown-leaf-exec.md`).

- Corrections of record: `3243F0`'s `300E40` gate is
  `d[q[obj+0x698]+0x64] & 0x80000003` (linked-object flag, not
  `rec+0x3C`), then `313F60` ret, then `byte[obj]&2`; `313F60` ret is
  `377C20` table bit15 — default `cd_words=[0x8000]*8` → ret 1
  (skip arm), `cd_words=[0]` plants the run arm.
- New fixtures: `objc0` (`d[objent+0xC0]` link idx), `ecarr`
  (`q[0x22C6F28]` element array, stride `0x740`, `chain` nodes marker
  `+0`/next `+0x48` for `3AEEF0`).
- Still scripted: `30FED0` (`fed0` ×196), `316A50` (×56), `3105D0`
  (×28), `2EB0D0` (`kb0d0` ×26 — `2EB430`'s sink), `319490`, `2E42D0`,
  `3B02A0`, `46AB10`, `426130`/`427320`, the `317ED0`/`3180F0`/
  `319CA0` entity-context chain, allocator sinks.

### 13ai. Per-kind stat accumulator `316A50` + `315E90`/`316BF0` helpers — EXP-226

The ×56 stat-accumulate sink now runs shipped bytes. `00316A50`
`(cl=kind<0x1E, edx=delta)` dispatches over the shipped kind-descriptor
table `0xD10460` (30 entries × 8B: `{b0=mode, b1=slot-off,
b2=cmp-mode, d4=cmp-val}`): mode≠0 → arm-2 accumulate (`3166F0` get →
saturating add, mode2→u16 `[0,0x7FFF]`, mode4→u32 `[0,0x7FFFFFFF]`,
cmp3→`bts ebx,delta−0xE2`, cmp8→skip) → `00315E90` achieved-gate →
`00316BF0` write-back at `q[020927C0]+0x384C+off`; mode==0 → arm-1
compare (`edi≥3165C0?:d4` or equality) → achieved → inline bit-set +
notify. `00315E90` pre-checks the achieved-bit
`b[q[020927C0]+k/8+0x3844]` (set → bail) then dispatches modes
{0→`316760≥3165C0?:d4`, 2→`309EC0` range scan, 3→popcount,
5→`3160C0`, 6→`3161A0`, 7→rel-ptr+`315420`; 1/4 reserved} → set bit +
`008632B0(d[0xD10550+k*4])` (scripted `b32b0` ×55). `003165C0` =
4-level rel-word chain over `q[0x22C2550]` + kind-bitmap select;
`00316760` = `3166F0` with kinds-5/8 array fallback. Corrections:
kind is **low byte `cl`** (`254EE0` `cl`-patch records rcx=0x506 →
kind 6 path); `315E90` gates the **pre-write** stored value;
achieved-bit dedup is real (`d228-2g`'s second `316A50(0xB)` bails);
`q[020927C0]` now default-planted 0x3900 (`+0x3404` counters,
`+0x3844` achieved-bits, `+0x384C` slots — one physical table).
Result: `542/542, stable ×3`, hash `8e870d84`
(`_experiments/EXP-226-stat-accumulator-316A50-exec.md`).

- Still scripted: `30FED0` (`fed0` ×196), `2EB0D0`
  (`kb0d0` ×26), `319490`, `2E42D0`, `3B02A0`, `46AB10`, **`8632B0`
  (`b32b0` ×55 — new boundary, `316A50`'s UI notify sink)**,
  `317ED0`/`3180F0`/`319CA0`, `426130`/`427320`, allocators.

### 13aj. Object reset `3105D0` + embedded-ctx compose — EXP-227

The ×28 object reset now runs shipped bytes. `003105D0` gates on
`q[obj+0x698]` then runs the full teardown: `310780(obj)` detach
(stub-era hidden — `u0fc0-fast`'s `l310780` pin corrected 0→1) →
mode-byte clears `b[+0x694..0x696]`=FF via `30C970` (`bc970` ×88,
args now real) → `00300280` (`w[+0xDC8]`→`3008A0` registry dispatch
→`309F30`→`2FD8D0`/`2FD150` null-table early-outs → `w[+0xDC8]`=FFFF;
`d[+0xE58]`≠0 → `253690`+`254EE0` clamp) → header masks
`q[obj] &= 0xFFFFBFF75FFFCFFF` + `d[obj+4] &= 0xFFDFFF7F` +
`q[obj] &= 0xFFF3FFFFFEFFFFFF` → `16D6A0` noop → live element loop
`236820(i)`: `d[elem+0xEA0] &= ~(1<<b[obj+0xEA9])` over `OBJARR` →
`316CF0` memset `obj+0x778..0x97F` (bit0 latch preserved) →
`+0x718`/`+0x728` → `+0x730`/`+0x740` copies + field resets
(`w[+0x714]`=FFFF, `d[+0x700] &= ~3`, `q[+0x708]`/`d[+0x710]`/
`d[+0x75C]`/`q[+0x760]`/`q[+0x768]`/`q[+0x6D0]`/`q[+0x6D8]`/
`b[+0x6B4]`/`w[+0x6B7]` cleared) → `3291B0(obj+0x80)` ctx reset
(`3839F0` FF-fill `obj+0x200..0x27F`, 16B copies `+0xD0`→`+0x100`/
`+0x110`) → `33C9B0` (`336710` stack compose + `33E1F0` — deep arm
gated off `q[0x2089340]`-path null singleton; unconditional
`and [q[obj+0x1E0]]`/`[+0x21]` mask writes). Shipped-ordering
correction: `l01140-rel`'s `d[+0x788]` ends 0 — `301140`'s `&~0x400`
runs before `316CF0`'s memset. `a630r9` `a08a0`/`v2fd8d0`/`m2fd150`
pins +1 on teardown arms (real `300280` dispatch). New fixture cells
`q[obj+0x1E0]`/`q[obj+0x1E8]` under `objlink`. Result: `542/542,
stable ×3`, hash `dfe49da6`
(`_experiments/EXP-227-object-reset-3105D0-exec.md`).

- Still scripted: `30FED0` (`fed0` ×196), `2EB0D0` (`kb0d0` ×26),
  `319490` (×19), `2E42D0` (×18), `3B02A0`, `46AB10`, `8632B0`
  (`b32b0`), `30C970` (`bc970`), `319420`, `319140`, `238BF0`,
  `317ED0`/`3180F0`/`319CA0`, `426130`/`427320`, allocators.

### 13ak. Status recompute `30FED0` — EXP-228

The ×196 recompute — this contract's subject — now runs shipped bytes
end to end. `0030FED0` (`rcx`=record, `edx`=flags → internally
`flags|0x202`, bit9 = the `30E130` anti-recursion suppressor):

- **Bitmap build** (16-byte stack map): `b[rec+5]==0` →
  `row = 20E600(d[FOED+0xC]) + w[FOED+8]*b[rec+4]`, bits 0-63 =
  `d[row+0x50]`/`d[row+0x54]`; `b[rec+5]==1` → `31B860(rec)` owner →
  OR `owner+0xE80` (member arm exercised on `ac80-member*`:
  4× `b860` per call — head resolve + two tail resolves +
  `30E060`'s internal one).
- **Equip slots:** `w[rec+0x50..0x58]` ×5, each `322C50(6,id)` →
  `memt` double-hop → `31E9A0(row)==3` && `b[row+0x1A]!=0xFF` → `bts`.
  `0031E9A0`/`0031E9F0` promoted real: `b[row+9]`≤0x1A → shipped jump
  table `0x1FEA50/0x1FEA74` → class 0-8 → {0,1,2,3} (×61 in-suite).
- **License loop** `i<0x169` over `rec+0x194` bits → `abild` row →
  `323890(b[row+5])==2` gate → `w[row+8..0x16]` `!=0xFFFF` → `bts`
  (`l323890` ×33 real).
- **Diff dispatch:** `added = new&~(rec+0x78)` → `30E130(...,mode3)`,
  `removed = ~new&(rec+0x78)` → `mode1` — refines EXP-148 (which
  recorded only the mode-3 arm). `30E130` scripted `e130` (×0 — no
  fixture produced a diff; honest empty-operand run), `2FEF30`
  scripted `fef30` ×196.
- **Member tail:** `bt d[owner+0xE90],i<0x20` → `30E360(...,mode5)`
  per set bit (fired ×4-5 per call on `f3f0-*` planted bits);
  `b[q[owner+0x6A0]]&0x80` selects the `+0x78..0x7C` ↔ `rec+0x40..0x44`
  copy direction.
- **Field tail:** `d[+0x48]` clamp vs `d[+0x24]` (`flags&0x10000` →
  min 1; `bt flags,0x1C` doubles), `w[+0x4C]`/`w[+6]` vs `w[+0x28]`
  under `b[+0x6C]`-sign/`b[+0x7C]` gates with `b[+0x37]` multiplier,
  then `30E060` (`n0e060` real).

Corrections: five `b860` pins +1 (`30E060` calls `31B860`
unconditionally at `0x30E084` — the stub hid it); `a630r9-nomatch`
`e6820` 2→4 (the second full OBJARR scan). No new fixtures — the
`memt`/`abild`/`foed` `mkdesc` plumbing and `q[objrow+0x6A0]` under
`objlink` already covered every table path. Result: `542/542,
stable ×3`, hash `73bde5c4`
(`_experiments/EXP-228-status-recompute-30FED0-exec.md`).

- Still scripted (post-EXP-228): `30E130` (`e130`), `2EB0D0`
  (`kb0d0` ×26), `319490` (×19), `2E42D0` (×18), `3B02A0`, `46AB10`,
  `8632B0` (`b32b0`), `30C970` (`bc970`), `319420`, `319140`,
  `238BF0`, `317ED0`/`3180F0`/`319CA0`, `426130`/`427320`,
  allocators. (`2FEF30`/`fef30` promoted in §13al.)

### 13al. Derived-stat rebuild `2FEF30` + scale leaves — EXP-229

The once-per-recompute accumulator `30FED0` tails into — the routine
that *produces* the `rec+0x24..0x47` block this contract's §13ak diff
and field-tail clamps read — now runs shipped bytes
(`NATIVE-REPLAY`). Signature shape `(rec, rsi=out, r8=slots)`:
`rdx==0` → `31B860` owner resolve + `d[rec+0x3C]` saved; `rsi==0` →
`out = rec+0x24`; `r8==0` → slots `rec+0x50`. Then
`out = rec+0x24..0x47` **zeroed** and rebuilt:

- **Foe arm** (`b[rec+5]==0`): `foed` row `b[rec+4]` → HP acc =
  `2F8E50(d[rec+8], b[row+0x18], b[row+0x19])` (`(a*(r8+1)*b)/100`
  magic-div `0x51EB851F`), MP acc = `2F9180(w[rec+0xC], b[row+0x1D])`
  (x·y/100), `d[rsi+0x14] |= d[row+0x4C]`, `d[rsi+0x18] |=
  d[row+0x48]`, float stat seeds `cvttss2si` `f[rec+0x10..0x1C]`.
  `rsp+0x5C` = 1 iff `(b[rec+4]-0x1B)<=0xC` — foe-class second HP
  clamp (`min 0x7FFF`).
- **Member arm** (`b[rec+5]==1`): `memd` row `b[rec+4]` fans out to
  **three chained growth descriptors** — `q[02EBF148]` row
  `w[memd+0x22]`, `q[02EBF140]` row `w[memd+0x24]`, `q[02EBF150]` row
  `w[memd+0]` — and scales growth fields by level delta
  `b[rec+0x1C2] - b[rec+0x88]`: `d/d140[+0x20]*Δ + d/d148[+0x20]` →
  HP, `w[+0x24]` pair → MP, `b[+0x26..0x2B]` pairs + `w[rec+0x8/0xA/
  0xC/0xE/0x16]` → the five stat accs.
- **Equip loop** ×5 over `w[slots+2i]`: `322C50(6,id)` → `memt` row
  → `31E9A0` class dispatch → `sub = 20E600(d[row+0x28])` bonus
  record: `w[sub]/w[sub+2]` → HP/MP, `b[sub+4..7]` → stat accs,
  `d[sub+0xC]`/`d[sub+8]` → `or d[rsi+0x14]`/`or d[rsi+0x18]`,
  `b[sub+0x10..0x14]` → `or b[rsi+0x1C..0x20]`.
- **Status-bit fold:** shipped `.rdata` index tables `0xD10290`/
  `0xD102A0`/`0xD102B0` (16/16/12) map set bits in `rec+0x68..0x7F`
  to `q[02EBF040]` (`sttd`) rows → `w[row+4]` folded into HP/MP/SPD
  accs. `q[02EBF040]` null + set bit → `w[4]` fault (fail-closed).
- **Tail clamps → `rsi` block:** `d[rsi]` HP floor 1, cap `0x270F`
  (`0x3B9ACA00` flag-gated; `min 0x7FFF` second pass on `rsp+0x5C`),
  `w[rsi+4]` MP `[0,0x3E7]`, `b[rsi+6..9]` stats `[0,0x63]`,
  `b[rsi+0xA]` ≤3.

Semantics that moved the contract: `d[rec+0x3C]` is a **rebuilt
output**, not an input — it is `or`'d from `d[foerow+0x48]` /
equip-bonus `d[sub+8]` inside the zeroed range, so `3243F0`'s
`d[q[obj+0x698]+0x64] | d[+0x3C]` `→ 313F60 → 300E40` gate consumes
the real value. `300530`'s stat-decrease reconcile (`e360` mode3 at
`0x3007CF`) now legitimately fires once per `ac80-foe` rebuild
(`d[rec+0x48]` ≤ saved). `ac80-member-nulld` faults at `0x2FF158`
(`w[r13+0x22]` on null `MEMD` row) — inside `30FED0`→`2FEF30`,
ahead of `23AC80`'s own member deref; shipped order, not stub order.

New fixtures: `mkdesc` defaults on `q[02EBF148]`/`140`/`150` (elemb
`0x82000/83000/84000`, stride `0x40`) and `q[02EBF040]` (`sttd`,
elemb `0x80000`, stride `0x20`, count `0x100`) — zeroed rows,
`case["x"]=None` override selects the null-desc arm. Result:
`542/542, stable ×3`, hash `85e8d6f9`
(`_experiments/EXP-229-derived-stats-2FEF30-exec.md`).

### 13am. Mode-byte clear `30C970` + release guards — EXP-230

The teardown callee `3105D0`/`310780` invoke on the object's old
`+0x694`/`+0x695`/`+0x696` mode bytes — §13aj's `bc970` sink — now
runs shipped bytes. `cl` selects a `0x30`-byte row in the 32-entry
`.data` table `0x022C17B0` (BSS-zeroed shipped); `cl==0xFF` or
`cl>0x1F` is a **full no-op** (pinned on `u0fc0-def`'s `0x27` call).

On a live index (`cl<=0x1F`):

- **Unlink** the row from two intrusive lists — `q[row]`/`q[row+8]`
  `prev`/`next`, null-link head fixups write `q[022BE978]` /
  `q[022BEB88]`, then the row's own links clear.
- **Release** `d[row+0x28]` / `d[row+0x24]` through guard thunks —
  `325A00` (`ecx`∉{0, `0x80000000`, `0x80000001`} → `3DC780`; `ecx` = 1 included) and `317EC0` (`ecx`∉{0,-1} →
  `42FCC0`), both promoted real; their deeper arms stay scripted
  (`v3dc780`/`v42fcc0`, ×0 on zeroed rows).
- **Notify** `306570(31B7E0(d[row+0x20]))` only when `d[row+0x18]≠0`
  (`v306570` scripted, ×0).
- **Reset** the row: `d[+0x2C] &= ~0x1F` (low-5 flag bits),
  `w[+0x1C]=0xFFFF`, `d[+0x28]=0x80000000`, `d[+0x24]=0xFFFFFFFF`,
  links/`q[+0x14]`/`d[+0x10]`/`d[+0x20]`=0 — pinned on `a630r9-swap`
  row 0.

Adjacent getter `30CA50` (not yet a sink target): `b[rcx+0x695]` ≤0x1F
→ `d[row+0x24]` else −1 — the mode-byte → row-handle read.

In-suite args: `cl`=0 ×87, `cl`=0x27 ×1. `l30c970` ×88, guards ×87
each, all deeper arms ×0, zero regressions. Result: `542/542,
stable ×3`, hash `44df2284`
(`_experiments/EXP-230-mode-byte-clear-30C970-exec.md`).

### 13an. Detach siblings `308270`/`319140`/`319420` — EXP-231

The three per-release teardown calls around `bc970` — the last
scripted internals of the `310780`/`300FC0` detach path — now run
shipped bytes:

- **`00308270`(obj)** — `bt q[obj],0x16` gate: `d[+0x28]`=0 →
  `30C970(b[obj+0x695])` → `b[+0x695]`=0xFF → `w[+0xDC8]`/`d[+0xE58]`
  from `0x22C1DB0` row `b[obj+0xEA9]` → `30EDA0` snapshot copy
  `q[obj+0xB88]`→`obj+0x730` (0x480) → `q[obj] &=
  ~0x0000400000400000` (bits 46,22) → `d[+0x690]`=0. Bit22 survives
  only in `u0fc0-def` at read time — the body ran once real
  (`l30eda0` ×1); its mask explains `u0fc0-def`'s qmask
  `0xFFFFBFF9EFA7FFDD` (previously stub-hidden).
- **`00319140`(obj,edx)** — `edx&1` → `290B90(d[obj+8])` entity-list
  flag set (**scripted `s290b90`** — shipped-null `q[0x209BE80]`
  head deref would fault; no live list under fixtures); `edx&2` →
  `3BBC80(q[obj+0x10])` 64-entry ring clear on `q[0x2B457D0]` (real,
  null-safe — ×0, all calls are `edx=1`).
- **`00319420`(obj+0x6B0)** — `d[+0xC4]`∉{0,-1} → `2EAEA0`→`24FE30`
  id dispatch; then `d[+0xC4]`=−1 (pinned). Empty-operand — no
  fixture plants `d[obj+0x774]`.

Object teardown is now real end to end except the `290B90` list-flag
boundary and the `317E50`/`b7e50` sink (never called in-suite).
Result: `542/542, stable ×3`, hash `f9fac9da`
(`_experiments/EXP-231-detach-siblings-exec.md`).

### 13ao. UI notify gate `8632B0` + `20CE00` — EXP-232

The `316A50` family's UI message sink — the ×55 `b32b0` scripted
boundary — now runs shipped bytes:

- **`008632B0`(ecx=msgid)** — `20CE00()` singleton → null → ret;
  else `20CE60(ctx, msgid)` tail dispatch. ×55 real.
- **`0020CE00`** — `return q[0x1F83450]` singleton getter. ×55 real.
- **`0020CE60`** stays scripted (`v20ce60`, ×0): msgid×`0x198` row
  latch (`b[+0x190]`, `d[+0x194]`) + armed-`b[ctx+0x18]` vtable
  forward of `q[row+8]` — needs a UiManager fixture. Sole caller is
  `8632B0`, so the boundary is exactly scoped.

New default fixture: `q[0x1F83450]`=0 — the shipped `.data` bytes
there are stale non-pointer data (init publishes the real object);
null is the honest pre-init state and turns the gate into a verified
no-op. Zero regressions. Result: `542/542, stable ×3`, hash
`deb5a557`
(`_experiments/EXP-232-ui-notify-gate-8632B0-exec.md`).

### 13ap. Node teardown `2EB0D0` + `427xxx` flag writers — EXP-233

The `2EB430` family's node teardown — `kb0d0`, ×26 scripted — now
runs shipped bytes: `rdx` null → ret (24/26 calls); live node →
`269D60` flag fold, `b[+0x11]` bit-4/3 gated `2EDCC0`/`314D30`,
ecarr arm (`row = q[0x22C6F28] + w[node]*0x740`, `d[+0x284]` gate)
dispatching `427320` (**scripted `v427320`** — the edi-switch
equipment/visual-set applier; recorded `v427320(elem2, 0x1001)`),
`w[+0x2A]`-sign-selected `4278B0`/`427880`/`4272C0`, `r9` arm
`427860`, tail `4272A0`; then node reset (`d[+0x14/18/1C]`=-1.0,
`w[+0x2A]`=FFFF, `b[+0x11]` clears). `u43f0-ec`'s live path folds
elem2 `d[+0x294]` to **0x401080** real (pinned); `k99b0-kick`'s
`0xDEAD` sentinel became a real `objc0` node. Result: `542/542,
stable ×3`, hash `875e09ae`
(`_experiments/EXP-233-node-teardown-2EB0D0-exec.md`).

### 13aq. Entity node clear `2E42D0` + `427280` fold — EXP-234

The `3243F0` teardown's per-release entity-node clear — `r2e42d0`,
×18 scripted — now runs shipped bytes: `q[ent+0xC0]` link node →
null/`d[node]==-1`/sign gate → `row = q[0x22C6F28] + w[node]*0x740`,
`d[row+0x284]` gate → `427280(row)` fold (`d[+0x294] &= 0xFFFDFA5F
|= 4`) whose `jmp 422C20` dereg tail (`20E600`/`51BA40` resolver
subtree) is the new scripted boundary `v422c20` — then
`d[ent+0xEC] = 0`. 17 of 18 calls early-out on the null link;
`u43f0-ec`'s `objc0`+`ecarr` path runs the full arm, and because
`2E42D0` precedes `2EB0D0` in `3243F0`'s flow, elem2's `d[+0x294]`
pin moved **0x401080 → 0x401084**. `422C20` was never
harness-reached before — every path to it sat behind the scripted
`2E42D0` — so the interception is exactly scoped. Result:
`542/542, stable ×3`, hash `07c5f87a`
(`_experiments/EXP-234-ent-node-clear-2E42D0-exec.md`).

### 13ar. Position broadcast gate `319490` — EXP-235

`312280`'s position gate — `s9490`, ×19 scripted — now runs shipped
bytes end to end up to the broadcast boundary: `3590D0()` ctx-id
(`d[0x22C7FE0]`) → `b[0x2089340]&0x10` enable → `3588B0` class-table
resolution (cls `(id>>16)&0xF`, idx `cx`, gen `w[+0x16]` vs
`(id>>20)&0x7FF`) → `263E30(ctx)` = `q[ctx+0x30]` node → `b[node]&8`
→ `3377C0(ctx-or-0, &vec4)` with `vec4 = {x,y,z, 1.0f}` — the
`0x1CEBBA8` literal pinned real. The broadcast itself is the new
scripted boundary `v3377c0` (spatial query + per-entity
classification — `391D10`/`3920F0`/`314EB0`/`313F80` subtree, five
image callers). `d228-pos`/`d228-pos2` resolve a live ctx through a
new `ctx4` `n30` node fixture — `v3377c0`'s rcx is a real node, not
zero. Result: `542/542, stable ×3`, hash `6a1b9b14`
(`_experiments/EXP-235-pos-gate-319490-exec.md`).

### 13as. Broadcast-rate gate `317ED0` — EXP-236

The rate throttle `312280` runs on each share-tick when source and
peer both qualify (`q[+0x698]` rec with `b[rec+5]`==1, peer
`b[+5]`==0) — `s7ed0`, ×1 scripted — now runs shipped bytes on
`d228-gaterc`: epoch A `b[obj+0x56]` vs `d[0x22C3168]` in-sync arm
increments `d[0x22C315C]` (clamped 0x3E6/0x3E7 on `229E40`'s lang
dword), epoch B `w[e68+0x40]` vs `d[0x22C316C]` increments
`d[0x22C3160]`, then `3183D0` LCG tick → LCG%100 rate flag `bl`
(sub-5% or ≥40% on `b[0x22C3178]&1`) → `28EF70(d[0x22C315C], bl,
d[0x22C3158])` flag push → tail `d[0x22C3178]|=bl`,
`d[0x22C3168]=b[obj+0x56]`. The `28EF70`/`28EF00` flag sinks —
each called from exactly this one site, both dereferencing
BSS-null `q[0x209BE80]` — are the new disclosed boundaries
`v28ef70` (×1, args `(1,0,0)` pinned) / `v28ef00` (×0,
epoch-mismatch arm). `229E40` was already real (EXP-209); it now
fires twice per pass. Result: `542/542, stable ×3`, hash
`ff72b856` (`_experiments/EXP-236-rate-gate-317ED0-exec.md`).

### 13at. Entity-gate pair `2E9780` + `26D6F0` — EXP-237

The `b[+3]&0xE0==0x60` gate pair `300FC0`'s tail calls per teardown
(`b9780`/`b6f0`, ×8 each scripted) now runs shipped bytes: `2E9780`
the flag probe (`q[+0xC0]` node → `b[node+0x11]>>6&1`, null-guarded)
and `26D6F0` the float/param update (`q[+0xB8]` desc → `f[+0x24]`/
`f[+0xD0]` writes, `b[+0xC]` arm, `2E9BB0`/`2EC5B0` flag sinks —
still scripted `b9bb0`/`bc5b0`). All 8 calls take the gate-fail
early-out under fixtures (`ent_b` never planted on u0fc0 — the
shipped gate now decides, so a `b[ent+3]`=0x60 fixture exercises
the real pass arm). Result: `542/542, stable ×3`, hash `a136ab9a`
(`_experiments/EXP-237-gate-pair-2E9780-exec.md`).

### 13au. Registered-language resolver `39BAD0` — EXP-238

The `rcx`→slot resolver the display/text family uses (`3BBD00`,
`2BD4D0`, `2B3050`, `2B3420` siblings) now runs shipped bytes: scans
slots **1..7** of the shared `0x2AEE810` 8-slot table for a low-dword
match against `edx=low32(rcx)`, returns the index or 0 (`rcx=0`
early-outs). `s39bad0`×8 → `l39bad0`×8. The two `b3050-*` cases that
need `ret==7` (system-language arm: `bts d[state+0x44], 0xB` + second
`39C4A0` when `254A10()==0`) plant a **disclosed `bad0t` fixture**
(`{7: 0x44}`) — the real scan now computes 7 from table state rather
than a stub declaring it. `b3050-run` and the `bd00-t2*`/`d4d0-near`
callers get real-0 on the BSS-zero table = stub-equivalent. Slot 0 is
never compared (eax starts at 1). Result: `542/542, stable ×3`, hash
`e156ff72` (`_experiments/EXP-238-registered-language-39BAD0-exec.md`).

### 13av. Entity-node bit-3 writer `2EBB80` — EXP-239

`301140`'s teardown reaches `2EBB80` through the real `26DC60`
trampoline (`jmp 0x2EBB80`) — `bbb80`×7 → `l2ebb80`×7. Body: same
`b[+3]&0xE0==0x60` gate as §13at → `q[+0xC0]` node (null-guarded) →
`b[node+0x10]` bit-3 fold from `dl&1` → `jmp 2E8FD0` tail. All 7
calls run the gate-fail early-out (`ent_b`+3 never planted on the
l01140 family) — stub-identical output, shipped-gate authority;
caller at `0x3012F6` discards `eax` so the real body's `movzx`
clobber is unobservable. New scripted boundary `v2e8fd0` ×0 — the
pass-arm second-level node walk (`3E6A60`/`2E8CE0`/`2EE190`/
`2E8AC0`/`2E8A70` subtree), scripted eagerly so a future
`b[ent+3]=0x60` fixture surfaces it rather than silent execution.
Result: `542/542, stable ×3`, hash `9af86e31`
(`_experiments/EXP-239-node-bit3-2EBB80-exec.md`).

### 13aw. Pass-arm sinks `2E9BB0`/`2EC5B0` real; pass arms exercised — EXP-240

The `b[+3]&0xE0==0x60` pass arms left unexercised by §13at/§13av now
run shipped bytes: `u0fc0-m1` plants `ent_b={3:0x60}` + new `desc8`
(`q[ent+0xB8]` desc → `q[desc+0xF0]` float cell) + `objc0` node +
`objc0q` (`q[node+0x138]` flag target) — `26D6F0`'s full pass arm
executes: `f[q[desc+0xF0]+0x24]`/`f[desc+0xD0]`=xmm6, `f[tgt+0xC8]`=
const³·xmm6, then **real** `2E9BB0` (`d[tgt+0x110]` getter) →
`ebx&~4`, `xmm6==0` → `ebx|=4` → **real** `2EC5B0` writes
`d[tgt+0x110]=4` (pinned). `l01140-bbb1` plants the same gate +
`objc0` → `2EBB80`'s fold lands `b[node+0x10]=8` (pinned) then
tail-calls `v2e8fd0` — now ×1 with real args `(ent, dl=8)`. `2E8FD0`
itself stays scripted (second-level node subtree). Result:
`542/542, stable ×3`, hash `0fcf1ce5`
(`_experiments/EXP-240-pass-arm-sinks-2E9BB0-2EC5B0-exec.md`).

### 13ax. fbdev device-list scan `290B90` — EXP-241

The largest remaining scripted tag is real: `290B90` (`l290b90` ×34)
scans the device list at `q[q[0x209BE80]+0x10F10]` for
`d[node+0x810]==ecx` (`319140`'s `edx&1` arm passes `d[obj+8]`),
folds `w[node+0x850]` 2→3 on a match, returns 1/0. The existing
`fbdev` fixture (widened 0x6000→0x12000 for the `+0x10F10` head)
now carries `"nodes":[{id,w850}]` list chaining on `q[+0x868]`. 33
cases plant `fbdev=1` (present object, empty list → real-0); the
sole `ecx=9` caller `u0fc0-s800` plants `{id:9,w850:2}` and the real
match arm folds `w[+0x850]`→3 — pinned. Blast radius checked: every
other `q[0x209BE80]` reader (`290Bxx`/`290Cxx` siblings; `28EF70`/
`28EF00` were scripted at the time — promoted real in EXP-242) is
scripted or has no harness-reached caller. Result:
`542/542, stable ×3`, hash `1ba3c747`
(`_experiments/EXP-241-fbdev-scan-290B90-exec.md`).

### 13ay. Broadcast flag sinks `28EF70`/`28EF00` — EXP-242

The `317ED0` broadcast-rate sinks surfaced as boundaries in EXP-236
are real now that `fbdev` plants their `q[0x209BE80]` object:
`28EF70` (`l28ef70` ×1 on `d228-gaterc`) calls `28F0C0` — whose
`ecx!=0` arm notifies through `253770` → `jmp 316A50` (real since
EXP-226), stores `w[+0x7C78]`=low16(ecx), `d[+0x7C7C]`|=1 &=~8 —
then folds `d[+0x7C7C]` bit 1 := `edx&1` and stores `w[+0x7C82]`=r8w.
Shipped-computed pins on the planted call `(1,0,0)`:
`w[+0x7C78]`==1, `d[+0x7C7C]`==1, `w[+0x7C82]`==0. `28EF00`
(`l28ef00` ×0, the epoch-mismatch arm — `d[+0x7C7C]`=0 then |=8 |=1
plus `w` stores) promoted alongside; `28F0C0`'s `ecx==0`
`273A20`/`244F00` slot-clear tail stays unexplored (not reached).
Result: `542/542, stable ×3`, hash `92012b09`
(`_experiments/EXP-242-broadcast-flag-sinks-28EF70-28EF00-exec.md`).

### 13az. Gauge-event post `28F1F0` — EXP-243

`28F1F0` (`l28f1f0` ×7, former `q28f1f0`) is real: `296280(ecx)`
scans the four-entry channel table `0x209BF66..0x209C2BE` (0xC0
stride — an entry participates only when `b[e-0x58]&2` or `b[e]&2`,
then `d[e+0x32]`==ecx → `e-0x7E`); miss → `2962C0` default slot
`0x209C240` gated on `d[+0xB0]`!=0 && ==ecx; pass → `3F8980` posts
the `{edx,r8d}` pair through `q[obj+0x38]` (or `obj+0x58` when
r9d!=0). The whole table region is shipped **BSS** (`.data` raw ends
at canonical `0x1F7E400`), so under shipped-zero state the scan
misses, the default gate fails, and the body early-outs — stub-
equivalent observably, shipped-computed now; a planted table row or
default-slot dword exercises the real post arm. `l296280` ×24 (17
pre-existing silent-real callers surfaced by listing), `l2962c0`
×7, `l3f8980` ×0. Result: `542/542, stable ×3`, hash `0e1b4ed7`
(`_experiments/EXP-243-gauge-event-post-28F1F0-exec.md`).

### 13ba. Flag-dispatch `2548F0` — EXP-244

`2548F0` (`l2548f0` ×4, former `b48f0`) is real — a flag→bit-op
dispatcher on the `u0fc0` teardown path: `ecx!=0` picks `2E1C20`
(set) else `2E1CA0` (clear), then four `(slot 8, bit)` ops on the
BSS cell `d[0x215F1E0]`: bits {8,9,0xB,6}. All four `u0fc0` callers
pass `ecx=1`, so `d[0x215F1E0]`==`0xB40` after — pinned
(`l2e1c20` ×16, `l2e1ca0` ×0 clear arm disclosed). Siblings
triaged/deferred: `36C140` infinite-loops (`jmp $`) on an empty
deferred-call stack — the stub is load-bearing; `36C1D0` dispatches
on caller return-address bytes; `23B040`/`238BF0` medium/large.
Result: `542/542, stable ×3`, hash `16c6d974`
(`_experiments/EXP-244-flag-dispatch-2548F0-exec.md`).

### 13bb. Mask classifier `23B040` — EXP-245

`23B040` (`lb040` ×3, former `b040`) is real — the `300FC0`-tail
eligibility classifier: `b[0x2089340]&0x40`/`&0x600` epoch masks,
`303EC0` (`30D9A0`==2) + `313F60` guards, then `3272A0` ctx-row
lookup; on a live row the deep arms run `2E8100`/`322600`/`322920`
kind tests and the `0x8800403B`/`0x80000003` rec-flag folds. The
tail unconditionally publishes `3592C0`(bit1 of `b[0x22C8005]`),
`359200`(bit1 of `d[0x22C8000]` + conditional `3588B0`), and
`26BD40`(`setne b[0x209A2C5]`). Under the u0fc0 fixtures no ctx
chain is planted → `3272A0`→0 → early-out; the deep arms stay ×0
(`l2e8100`/`l322600`/`l322920` REAL-listed for a future resolving
fixture). Result: `542/542, stable ×3`, hash `df9917f4`
(`_experiments/EXP-245-mask-classifier-23B040-exec.md`).

### 13bc. Dedup-ring inserter `46AB10` — EXP-246

`46AB10` (`l6ab10` ×12, former `q6ab10`) is real — the dedup ring
the stat-change notifiers (`46A800`/`46A630`/`469E80`) tail into:
`d[r8+0x28]` cap → scripted `31B860` owner scan → `469570`
resolver (×12, REAL-listed — returns 1 on null desc so insertion
proceeds; the shipped `mov eax,1` epilogue corrected an earlier
"null == skip" misread that faulted at `0x46ABB3`) → `20E600`
index → `b[elem+width*edi+4]&1` picks dedup-scan vs insert. The
real **insert arm** runs on all 12 cases: ring row at
`0x2EBB560 + cursor*0x20` gets `w=edx`, `q+8=rcx`, `d+4=32A150()`,
cursor `(d[0x2EBB54C]+1) mod 10` — all pinned shipped-computed on
`e360-mode-pair`. `5369C0` insert-notify stays a scripted boundary
(`s5369c0`, stack-arg fragile, sole caller `0x46AC66`). New
`q6desc` fixture plants `q[0x2EBF018]` (BSS-null shipped → the
unfixed read would fault) on exactly the 12 calling cases.
Scripted `b860` count pins +2 per case (real-called scans).
Result: `542/542, stable ×3`, hash `25a8ffb1`
(`_experiments/EXP-246-dedup-ring-46AB10-exec.md`).

### 13bd. Spatial broadcast `3377C0` — EXP-247

`3377C0` (`l377c0` ×19, former `v3377c0` bespoke stub removed) is
real — the spatial broadcast `319490` tails into at `0x31950C`.
All 19 calls take the guard early-out (`rcx==0` ×17, `q[ctxn30
+0x10]==0` ×2 → ret 0). Correction of record: the stub's
`s9490_ret=1` was synthetic — with the real body `312280` skips
`3180F0`/`319CA0`, so `d228-pos`/`pos2` honestly show
`s80f0`/`s9ca0` ×0; the vec4-w pin moved to the caller's stack
frame (`0x3F800000` shipped literal). Deep arms (`265090` pos
getter → `236820`/`31ABE0`/`2EA7F0` gate → `391D10`/`3920F0`
query → `263E30`/`314EB0`/`313F80` per-entity loop → ret 2 /
`337700` fallback) are mapped but unexercised — they need an
entity-list fixture (`q[ctxn30+0x10]` link, `n30` past `+0xEA9`,
`d[0x208E6A0]`/`q[0x208E688]` pool, query containers).
Result: `542/542, stable ×3`, hash `2d95f2de`
(`_experiments/EXP-247-spatial-broadcast-3377C0-exec.md`).

### 13be. `3377C0` deep scaffolding — fallback tail `337700` real — EXP-248

The entity-list fixture from §13bd's deferred list is planted on
`d228-pos`/`d228-pos2` (`q[n30+0x10]` context link, `n30` widened to
`0xF00`, `b[n30+0xEA9]=1` selecting `oar4` row 1 — moved off row 0
after it collided with `objlink`'s source row — `clstab` class-4 →
ctx0). The deep path now executes shipped bytes end to end:
`265090`/`3DA710` pos+radius fetch (×4), `236820` row resolve,
`31ABE0`→`3588B0`→`263FF0` class-table id resolve (first *live*
resolve), `2EA7F0` eligibility gate (ret 0 on `ctx0` → empty result
set), then the **`337700` fallback tail** — second `265090` fetch,
`391410` early-out on null grid `q[0x2AEDFB0]` (honest: unplanted),
`384130` xz-pack, scripted `s383f10` → `0xFF` → ret 0. `383F10`
stays scripted: its inner call goes through IAT slot `q[0x8C2C10]`
holding RVA `0x1CCF034` — `.rdata` data, not code.
Result: `542/542, stable ×3`, hash `992180aa`
(`_experiments/EXP-248-3377C0-fallback-tail-337700-exec.md`).
Still unclaimed: `391D10`/`3920F0` query arms and the per-entity
loop (need populated query containers), `383F10` real,
`3180F0`/`319CA0` (scripted ×0), live-game reachability.

### 13bf. `0046AB10` dedup-ring scan arm — EXP-249

Three new direct-entry cases (`q6dup-hit`/`q6dup-miss`/
`q6dup-stale`, direct on `0046AB10`) exercise the dedup-ring scan
arm deferred by EXP-246: `q6desc.elf` sets the element flag byte so
`b[elemb+4]&1` at `0046ABB3` selects the scan; `q6ring` pre-seeds
rows at `02EBB560+slot*0x20`; `q6now` plants `d[0208D45C]` (the
`0032A150` "now"). Shipped predicate: a matching row
(`q[+8]`==payload, `w[+0]`==tag) suppresses the notify iff
`d[01DFE0B4]*0x1C2 + d[row+4] > now` — the shipped constant is 1,
so the window is `0x1C2` ticks. Hit → ret 0 with no write and no
`s5369c0`; stale/miss → the real insert arm (cursor write, mod-10
advance via the `0x66666667` divide, `s5369c0` notify). `s5369c0`
count 12→14. All three arm outcomes pinned on row/cursor memory and
notify args.
Result: `545/545, stable ×3`, hash `9423b774`
(`_experiments/EXP-249-46AB10-dedup-scan-arm-exec.md`).
Still unclaimed: the `b[rax+4]&0x20` mid-gate (needs a `0031B860`
hit), `005369C0` real, live-game reachability.

### 13bg. Small-wrapper sweep + `0046AB10` cap arm — EXP-250

Nine bounded bodies promoted to shipped-byte execution on existing
fixtures: `0031B8C0` (roster-slot → battle unit thunk over real
`00263750`/`00263E30`), `002FA390`→`002F8E90` (mode-flag classifier,
ret 1 matching the retired `qfa390_ret`), `002FA540`→`00320450`→
`00329A20` (early-out on `b[rcx]&0x10==0`), and the bit-op family
`00254850` (ten `002E1C20` sets on slot 8) / `00254940`→`002547D0`
(eight more bits via the `002E1CA0` select). New direct-entry case
`q6dup-cap` closes `0046AB10`'s last entry arm: `d[r8+0x28]=0x1FF`
exits before the resolver — no `l69570`, no ring write, no notify.
Correction of record: `u0fc0-fastt`/`u0fc0-mtail`'s
`w[glob+0x5AD0]==2` pin measured a stub-fed write arm — real
`0031B8C0` returns null on empty roster slot 3, so `003138D0`
je-skips the `^=(w^esi)&1` write; pins retargeted to the unchanged
planted `3`.
Result: `546/546, stable ×3`, hash `3d2df53a`
(`_experiments/EXP-250-small-wrapper-sweep-exec.md`).
Still unclaimed: `002F8E90`'s alternates, the remaining stub census
(`v422c20`, `v427320`, `b6fa0`, `n12f0`, `b1dbdb0`, `b1850`,
`b1f70`, `s181330`, `b3b02a0`), `00383F10` real (unbound IAT data
target), live-game reachability.

### 13bh. `0031B8C0` nonnull arm + `00311CF0` unit-mode publish — EXP-251

`ctx4` gained `None` = empty roster slot and `n30` gained `q698` =
linked flag node. On `u0fc0-fastt`/`u0fc0-mtail`: roster slot 3
holds an actor whose `q[+0x30]` unit carries `d[+8]=0x12340000`;
`g272f0=0x10` + `clstab={4:ctx0}` make `0031B7E0`'s flag-set arm
resolve the cid through `003588B0`/`00263FF0` to ctx0's unit (rdi)
— twice — so the full shipped `00311CF0` command-issue path runs
(`b1cf0` boundary removed; never fired in the suite before):
`w[glob+0x5AD0] &= 0xFFFE`, `w[rdi+0xBA0]=0x113`,
`d[rdi+0x6B0]&=~2`, `d[rdi+0xBB8]=0x12340000`, `w[rdi+0xBA4]|=0x8000`,
`q[rdi]|=0x4000`, tail `00317E60`→`0025AAD0(1,0)`; `003138D0`'s xor
(`esi=0`) then holds the toggle at `2` — the pre-EXP-250 value, now
produced by two shipped writers. `u0fc0-mtail`'s `flg` pin corrected
to `0x110` (it reads `d[02089340]` itself, which now carries the
planted `0x10` bit).
Result: `546/546, stable ×3`, hash `943cc4c7`
(`_experiments/EXP-251-31B8C0-roster-nonnull-arm-exec.md`).
Still unclaimed: `00311CF0`'s `edi==0`/stack-arg/`00377C20`/`0x113`-
skip arms and the `00311B20` caller, `00317E60`'s `b[rax]&8` arm,
`0031B8C0` `ecx>3`.

### 13bi. `0046AB10` owner-scan mid-gate exits — EXP-252

The stat-change notifier's owner question now runs shipped on both
answers. New `q6own` fixture plants `q[q6s+8]` as an `oar4` row's
linked rec so the already-REAL `0031B860` (REAL since EXP-192) hits:
`00236850()`/`00236820(i)` walk → `q[row+0x698]==arg` → ret row.
Three direct-entry cases: `q6mid-g3080` (`d[02089340]&0x3080` →
`jne 0046AC7A`), `q6mid-b20` (`b[row+4]&0x20` via the row `flags`
qword byte 4 → same exit), `q6mid-ok` (both clear → `00469570` runs,
its own `0031B860` pair executes — `b860`×3 total — then the insert
arm writes `w[02EBB560]==0x1234`, cursor `0→1`, `s5369c0` fires).
**Correction of record:** the `0046AC7A` epilogue does not clear
`rax` — the exits return `0031B860`'s owner row, not 0; the pin
asserts `ret==row`.
Result: `549/549, stable ×3`, hash `148a3c80`
(`_experiments/EXP-252-46AB10-midgate-exits-exec.md`).
Still unclaimed: `00469570`'s hit-arm verdict semantics,
`0031B860`'s scan-miss arm, `005369C0` real body, ring cursor wrap,
`d[01DFE0B4]!=1` window coefficient.

### 13bj. `00469570` owner-verdict arms — EXP-253

The resolver's owner rows and veto consult now run shipped. New
`q6own0` plants `q[q6s+0]` (`rdx`/`rsi` carrier); `oar4` spec `ci0`
leaves `q[row+0x10]` null. `q6mid-rsi`: null `q[q6s+8]` → `0046AB10`'s
own scan skipped entirely (`test rcx,rcx; je`) → rsi arm: `0031B860`
×2 on the +0 rec → `q[02EBF188]`=row → `q[row+0x10]` nonnull →
`002FA3B0(ci)` → nonzero → insert. `q6mid-noci`: rdi-arm hit with
`q[row+0x10]==0` → `mov eax,1` → **proceed without consult** —
`002FA3B0` is only consulted when the owner row carries client-info;
`lfa3b0` absent, insert still fires. `q6mid-ok` pinned the owner cell
`q[02EBF188]`=row and `002FA3B0`'s arg=`q[row+0x10]`.
Result: `551/551, stable ×3`, hash `f8606e0f`
(`_experiments/EXP-253-469570-owner-verdict-exec.md`).
Still unclaimed: `002FA3B0` ret-0 veto, `00469570`'s
`b[elem+3]>=0x80` early-proceed and desc-null arms, `005369C0` real,
`q[02EBF188]` consumers.

### 13bk. `002FA3B0` veto arm — EXP-254

The resolver's distance-gate veto now runs shipped through
`0046AB10`. `q6mid-veto` plants the owner row's client-info vec3
~100 units from `vec3[01EBBB00]` (zeroed camera origin): rdi-arm
hit → `q[02EBF188]`=row → `002FA3B0(ci)` → `00265020` copy →
`003A1920`/`sqrtf` → `24.0 > 100` false → **ret 0** → `je 0046AC7A`.
The three `0046AB10` exits now have distinct pinned identities:
cap → 0, mid-gate → owner row (carried rax), veto → 0 (from
`test eax`). Owner cell still stores the row before the consult.
Result: `552/552, stable ×3`, hash `d58645cb`
(`_experiments/EXP-254-2FA3B0-veto-arm-exec.md`).
Still unclaimed: `002FA3B0`'s `b[obj+3]>>5` rejection arm, dist==24.0
boundary through `0046AB10`, `q[02EBF188]` consumers, `005369C0` real.

### 13bl. `00469570` early arms + direct probes — EXP-255

`q6desc` gains `"b3"` (`b[elemb+3]`); `q6arg` hands an `oar4` rec to
register args. `q6mid-g80`: `b[elemb+3]=0x80` → `00469570` ret 1
before any owner lookup — `q[02EBF188]` stays null, `002FA3B0`
unconsulted, `0046AB10` proceeds to the ring (`e600`×6 total: 4 in
the resolver + 2 in `0046AB10`'s own `0046AB83` resolve). Direct-entry
`q69570-null`/`q69570-rsi` prove desc-null falls *to* the owner arms
(not an early ret): rdi/rsi pairs each store `q[02EBF188]` and reach
`002FA3B0` → ret 1. The resolver's decision table is now fully
pinned: `>=0x80` early-proceed, miss/null-ci → ret 1, ci →
`002FA3B0` verdict; `0046AB10` refuses only on `ret==0`.
Result: `555/555, stable ×3`, hash `a1c54544`
(`_experiments/EXP-255-469570-early-arms-exec.md`).
Still unclaimed: ~~rsi-arm null-ci → rdi fallthrough~~ **(pinned
§13bm)**, `q[02EBF188]` consumers, `005369C0` real.

### 13bm. `00469570` rsi→rdi fallthrough + `00426FA0` — EXP-256

`q6mid-fall` plants `q[q6s+8]`=rec2 (`0046AB10`'s carrier) and
`q[q6s+0]`=rec1 (`00469570`'s rsi carrier) with `oar4` row 1 carrying
`ci0` (null client-info). The rsi-arm hit stores
`q[02EBF188]`=row1, sees the null ci, and **falls through to the rdi
arm** — which re-resolves rec2, stores `q[02EBF188]`=row2, and
consults `002FA3B0(ci2)` → nonzero → ring insert + notify.
`b860` order pinned: `[46AB10 scan: rec2, rsi: rec1, rdi: rec2 pair]`.
`00426FA0` promoted real (`b6fa0` retired): `w[rcx]` index →
`q[022C6F28]+idx*0x740` row → `00426220` signature gate → on ret 0
`d[row+0x284]|=0x100000` + `b[row+0xC0]&=0xBF`; leaf arm pinned on
`u43f0-ec` (`w[row+8]`==-1 skips the child walk and the
`0042EF90`/`0042DE90` enqueue, which faulted on the zeroed fixture —
stack-set structure not modelled, arm unclaimed).
Result: `556/556, stable ×3`, hash `9174099b`
(`_experiments/EXP-256-469570-fall-426FA0-exec.md`).
Still unclaimed: `00426FA0`'s child/enqueue arms and `00426220`'s
signature-compare arms, `q[02EBF188]` consumers, `005369C0` real.

### 13bn. `00422C20` dereg + `00427320` edi-switch — EXP-257

Both remaining `u43f0-ec` singles promoted real. `00422C20`
(element-row deregistration): the three slot fields `d[+0xC4]`/
`d[+0xC8]`/`d[+0x18]` planted -1 → the `0020E600`→`0051BA40`/
`002ED570` resolver arms skipped; the clear block runs —
`q[+0x68]/+0xD8/+0xE0/+0xF0/+0xF8]`=0, `d[+0x23C]`=0,
`b[+0xC0]&=0xBF`, `d[+0x69C]`=`0020E620(0)`=`−d[01F83530]`=
`0xBFFFF000` (the BSS base counter reads `0x40001000`). `00427320`
(edi-class applier): `003E7D10` row-0 empty → misses the
`0x2005`/`0x2006` arms → `00420890` default (`002ED500(0)` zero-out
→ `d[+0x110]`=0) → `00423790` ret 1 (`d[+0xC4]`==-1 early path) →
class-1 switch arm (`(edi>>0xC)&0xF`==1): `0020E600`×2 and
`d[elem2+0x294] |= 8`, pinned as `0x401084`→`0x40108C` through the
downstream `4278B0`/`427860`/`4272A0` folds.
Result: `556/556, stable ×3`, hash `4499a6ef`
(`_experiments/EXP-257-422C20-427320-singles-exec.md`).
Still unclaimed: `00422C20`'s resolver arms (need planted
`q[elem+0xDA8]`/`+0xD98` list heads — `0051F240` derefs `rcx+4`),
`00427320`'s `0x2005`/`0x2006`/`bt`-gated arms, `005369C0` real.

### 13bo. `00422C20` `+0xC4`/`+0xC8` resolver arms — EXP-258

§13bn's unclaimed resolver arms now run shipped bytes via four
direct-entry `d422c20-*` cases on a planted mode-1 slot container
(`dcntr` fixture). `d[elem+0x10]` is an **elemb byte offset** —
`0020E600(off)`=`q[01F83530]`+off, inverse of `0020E620`. The
resolved element's `q[+0xDA8]` container dispatches on
`d[C+4]&3` (signed): mode 1 → `0051F240` indexes `q[C+8]`+slot×0x30
descriptors directly, returning `q[desc+0x18]` (`b[desc]&2` would
mean an indirect `003AB7F0` resolve). `0051BA40` then resets that
record (`0041CF00` → `0041CB90` ~0x390-byte wipe) and releases
descriptor `A[d[record]]` through `0051F190`/`0051F4C0` — a w-index
unlink with `d[C+0x1C]`/`d[C+0x20]` head/tail fixups and
`d[C+0x14]`--. Pinned: `+0xC4` arm alone writes `w[+0xCC]`=-1; the
popped descriptor's `q[+0x18]` survives; mode 2 makes `0051F240`
ret 0 so reset+release are skipped **but the slot fields still
retire**. Clear block runs identically with arms live
(`d[+0x69C]`=`0xBFFFF000`).
Result: `560/560, stable ×3`, hash `316e49c0`
(`_experiments/EXP-258-422C20-resolver-arms-exec.md`).
Still unclaimed: `00422C20`'s `+0x18` arm (`002ED570` container
tables), `0051BA40` mode-0/`b[desc]&2` arms, `0041CF00`'s
`w[R+0x28]`/`d[R+0xC]&0x1000` arms, `003AB7F0`, `005369C0` real,
`003B02A0` (`b3b02a0` ×14 — needs a modelled `36BC60` heap).

### 13bp. `00422C20` `+0x18` arm — `002ED570` — EXP-259

The last `00422C20` resolver arm runs shipped bytes on two new
`d422c20-18*` cases (`dcntr` gained a second container at
`q[elem+0xD98]`). `002ED570(C2, slot)` resolves two
`003AB7F0`-tagged bases (low-2-bit tag: `0`=direct ptr — used here,
nonzero=`0036B130` handle resolve — corrected by §13bq/EXP-260;
no `2/3` null arm exists): `q[C2+0x30]`→`q[C2+0x38]`
row base (stride `0x10`, `d[row+slot*0x10]`==-1 → ret 0) and
`q[C2+8]`→`q[C2+0x10]` sub base (stride `0x20`,
`d[sub+(slot>>d[C2+0x4C])*0x20+0x10]` → `0020E600` element), ret
`element + (d[C2+0x50]&slot)*d[C2+0x48]` → `00422C20` writes
`d[ret] &= ~8`. **Asymmetry pinned:** `d[elem+0x18]` is never
retired — read once into `edi`, no `-1` write-back, unlike
`+0xC4`/`+0xC8`.
Result: `562/562, stable ×3`, hash `a0d627ef`
(`_experiments/EXP-259-422C20-d18-arm-exec.md`).
Still unclaimed (superseded — see §13bq): `003AB7F0`'s
handle-resolve arm, `002ED570`'s nonzero shift/mask/stride paths
and null-base arms — all closed by EXP-260 — `0041CF00`'s
row-loop/`0x1000` arms, `0051BA40` mode-0/`&2` arms, `005369C0`,
`003B02A0`.

### 13bq. `002ED570` arm variants + `003AB7F0` handle resolve — EXP-260

Four more `d422c20-18*` cases run shipped bytes on the `c2`
fixture's remaining arms, with one correction of record:
`003AB7F0` has **no** `&3`-discriminated null arms — any nonzero
low-2-bits takes `0036B130(edx)`, which rejects `ecx==0`,
`cl&3==0`, `ecx<0x100000`, `(ecx&~3)==0`, else returns
`q[ecx&~3 +8]+0x40` (handle = `header|lowbits`, 32-bit arithmetic,
headers must sit below 4 GiB); `003AB7F0` nulls resolved values
`≤0x40`. New pins: the sub index is `slot>>d[C2+0x4C]` while the
row index is the **raw** slot (`-18sh`); the return is
`element + (d[C2+0x50]&slot)*d[C2+0x48]` — an element-relative
write offset (`-18mm` writes `element+0x10`, base dword untouched);
handles with tags 1 and 3 resolve identically (`-18tag`); null
base cells skip `003AB7F0` entirely so `q[C2+0x38]`/`q[C2+0x10]`
keep cached bases (`-18noc`).
Result: `566/566, stable ×3`, hash `2b472799`
(`_experiments/EXP-260-2ED570-arm-variants-exec.md`).
Still unclaimed: `0036B130`'s rejection arms (resolved `≤0x40`,
sub-`0x100000` handles), `002ED610`'s caller — **closed by
§13br/EXP-261** — `0041CF00`'s
row-loop/`0x1000` arms, `0051BA40` mode-0/`&2` arms, `005369C0`,
`003B02A0`.

### 13br. `002ED610` caller-side walk — EXP-261

The `002ED570` caller runs shipped bytes on five `d2ed610-*`
cases (`ecarr` + `dcntr`/`c2` fixtures). `002ED610(cx, dx)`:
`row = q[022C6F28] + sx(cx)*0x740` gated on `d[row+0x284]` (cmove
to null), `d[row+0x18]` is the `C2` slot (`-1` → ret 0; the second
`cmp ebx,-1` at `0x2ED658` is dead — rbx survives `0020E600`),
`elem = 0020E600(d[row+0x10])`, `002ED570(q[elem+0xD98], slot)` →
ret `0020E600(d[ret+0x84]) + dx*0x290`. Resolve-only — no writes
besides the `C2` base stores. **`d2ed610-dead`/`-neg1` pin an
unguarded null deref:** dead row or `cx==-1` → `rax=0` → `d[0x18]`
at `0x2ED648` faults — recorded by fault PC, no page-0 fixture
fabricated.
Result: `571/571, stable ×3`, hash `0040634e`
(`_experiments/EXP-261-2ED610-caller-walk-exec.md`).
Still unclaimed: caller census / live reachability of the crash
arms, `0036B130` rejection arms, `0051BA40` mode-0/`&2`,
`0041CF00` row-loop/`0x1000`, `005369C0`, `003B02A0`.

### 13bs. `0051BA40`/`0051F240` mode-0 + `&2` arms, `0041CF00` block loop / `0x1000` arm — EXP-262

Six new `d422c20-*` cases on the `dcntr`/`c2` fixtures run shipped
bytes (`_experiments/EXP-262-51BA40-41CF00-arms-exec.md`):

- **`0051F240` mode dispatch** — `d[C+4]&3`: mode 0 resolves the
  descriptor-array base `q[C+8]` through `003AB7F0` before indexing
  (`-mode0`); mode 3 joins mode 2 in returning 0 (`-mode3` — the
  `00422C20` slot retire still runs; container mode doesn't gate
  deregistration).
- **`b[desc]&2` lazy record pointer** — `q[desc+0x18]` is
  **overwritten** with `sx(3AB7F0(q[desc+0x10]) + d[desc+0x20])` on
  each lookup (`-c4ind`): the reset lands on the re-resolved record
  and `0051F190`'s release key comes from `d[r2]`, not the planted
  pointer.
- **`0041CF00` block loop** — `w[R+0x28]` counts `0xA0`-stride
  subrecord resets at `R+0x38` (`-c4rows`, two blocks pinned).
  `w[blk+4]` stores the pre-loop `ecx` (**always 0** — `r8d` is the
  real counter, never stored). `0041CB90`'s tail writes skip
  `+0x30..+0x2AF`, so the loop's writes survive; `0041CB90` also
  retires `q[R+0x330]`/`d[R+0x338]` itself.
- **`d[R+0xC]&0x1000` arm** — `002ED570(q[R+0x330], d[R+0x338])` on
  the record's own container → `00372280` (`-c4rc2`): list at
  `20E600(d[E+0x84])+w[E+0x88]*0x290`, `w[E+0x8A]` word entries, each
  word indexes a `0x290` row getting `w[+0x280]&=~0x10`, four zeros
  (`q[+0x1A4]`/`d[+0x1A0]`/`d[+0x1C0]`/`q[+0x1C4]`) and two `1.0f`
  writes (`d[+0x1AC]`/`d[+0x1CC]`). The word list is embedded in the
  same `0x290` array it indexes.
- **`d[R+0x338]==-1` crash arm** — rcx stays 0 → `00372280(0)`
  reads `d[0x84]` unguarded — pinned by `expect_fault=0x37228D`
  (`-c4f0`); no page-0 fixture.

Result: `577/577, stable ×3`, hash `1d1a86bf`; faults 26
(+1 case × mem+uc). Still unclaimed: `0051BA40`'s `edx==-1` /
`0051F080` / `0041D220` arms, mode-0 tagged array bases,
`00372280` null-base arms and multi-entry lists, live reachability
of the `372280(0)` crash, `005369C0`, `003B02A0`.

### 13bt. `0051BA80` insert front — cap gate + populate-fail arms — EXP-263

The "deeper `0051BA40` body" was misattributed — `0051BA40` ends at
`0x51BA76`; `0051BA80` is a distinct 5-arg **insert**: `edx==-1` →
`0051F150` cap gate (`d[C+0x14]>=d[C+0x10]` → `-10`) →
`0041CB90` stack-record reset → `0041D220(&tmp, src)` populate →
`ebx==-1` → `0051F080` alloc → `0051F240` → `0x390` record copy →
`0041CA70` → `d[rec]=ebx` ret key. Three new `d51ba80-*` cases on
the `dcntr` fixture + a new `src` (arg5 source-spec) fixture run
shipped bytes
(`_experiments/EXP-263-51BA80-insert-front-exec.md`):

- **`0051F150`** — capacity gate returning `-10` when
  `d[C+0x14]>=d[C+0x10]`, else the free cursor `d[C+0x18]`
  (`-cap`: full container → ret `-1`, nothing else runs).
- **`0041D220(rec, src)`** — deep populate: `d[rec+0xC]|=0x100001`,
  `q[rec+0x330]=q[src+8]`/`d[rec+0x338]=d[src+0x14]` (seeds
  EXP-262's `0x1000` arm), `00409210` obj init, `00409F50` =
  `002ED570` doc-resolve wrapper (`dx==-1` → 0), `00409A30`/
  `00409660` tagged-section scans (`"CMF@"`/`"PRF@"`/`"MRF@"`),
  `0041CA70` tail → ret 1 only when `q[rec+0x368]` got set. Every
  callee is null-safe except `00409210`'s `ff15[008C2F70]` IAT
  call — the slot resolves to data in replay, so it was planted to
  a heap `ret` byte (**disclosed synthetic import boundary**; the
  shipped init body still executes — a `02B62E20` static sentinel
  overwrite pins it ran twice).
- **Populate-fail paths** — `-pop0` (`edx==-1`, `w[src+0x10]=-1`):
  `0041D220` ret 0 → ret `-1` with **no descriptor allocated** —
  `0051F080` never runs on `-1`+fail. `-dereg` (`edx=1`, same
  failing src): `0051F240`→`0041CF00` reset + `0051F190` release of
  the existing descriptor run **before** ret `-1` — populate
  failure on an occupied slot deregisters it.
- **`0051F080`/`0051F410`/`0051F380`** mapped for the deferred
  happy path: `0051F410` cap-gates, `d[C+0x14]++`, returns the
  cursor then scans for the next free desc; `0051F080` marks
  `d[desc]|=1` (`|=2` on `r9b&2` — the `&2` flag's producer),
  `d[desc+4]=slot|0x10000`, pre-resolves `q[+0x18]` with the
  `&2` formula, `0051F380` tail-links; `zx` indexing strips bit 16
  — key high bits are a generation/tag namespace.

Result: `580/580, stable ×3`, hash `d7f7cf78`; faults 26
unchanged. Still unclaimed: the happy insert path (needs planted
`PRF@`/`MRF@` section directories + `00409C30` match rows —
deferred), `0041D220` hit-path internals, `0046E420`→`3713C0`,
`0041CFC0`, `005369C0`, `003B02A0`.

### What is still owed, and it is live-only

~~Every gate and both writers are scripted here~~ — **the three GATES ran as shipped bytes on
2026-09-18 (§13a)**, and ~~both writers are still scripted~~ — **both writers, and the other three
sinks, ran as shipped bytes the same day (§13d)**. What remains unshown is no longer the write side:
it is what the four scripted carriers decide, and **§11's live-only observation is unchanged** —
nothing here runs inside a real frame, against real neighbouring state, at real timing.

## 14. Unresolved

- The four calls in the apply tail: `0030E130` (specified only by its two argument shapes here) and
  `0030E060`. ~~`002FEF30`~~ — **executed from shipped bytes 2026-09-18, see §13b**, with its two
  tail sinks (`003105D0`, `00307D10`) still scripted and therefore still owed.
- What `r14` holds on the fallback paths.
- What the gate values `3` (equipment rows) and `2` (licence rows) distinguish — FABLE's.
- Where the **stat** contribution lives, if the referenced page's description is accurate.

## 15. Evidence

Static, from the shipping image (`73461D08…`). `0030FED0` was disassembled and its three
accumulation loops, its diff and its apply loop read instruction by instruction across four
packages; the byte counts (`0x10`) and loop bounds (`0x20`, `5`, `0x169`, `0x80`) are read from the
compares, not assumed.

The most useful thing here is the negative in §1: this function does not compute a stat
contribution, and a reader sent to it for one will not find it.

**Claim table added 2026-09-12 (`OPUS-S15-CLAIM-TABLES-SIX`).** The prose above states the method
and is kept; this enumerates the claims so a pilot's `CONTRACT_MAP` can be derived from them.
**This function has never been executed** (§13), so no row claims more than static evidence.

| claim | evidence | tier | confidence |
|---|---|---|---|
| the derived set is a pure function of its sources, never updated incrementally | in `0030FED0`, nothing writes `+0x78` outside the apply — the diff at `00310310`–`00310336` reads it and the store lives in the callee `0030E130`; the accumulations write only to the stack. **The sources are not always three**: a kind-1 record accumulates from the unit's `+0xE80` instead (row below) | 1 (isolated original-code) | PROVEN |
| the status space is 128 bits | sixteen bytes diffed (`r10 = 0x10` at `003102EA`) and an apply loop bounded at `cmp edi, 0x80` (`0031039D`) | 1 (isolated original-code) | PROVEN |
| the character's own row contributes 64 bits from two masks | `0030FF6C`–`0030FFD2` and the same again from `+0x54`: `rol r9d, 1` twice, `add r8d, 2`, `cmp r8d, 0x20` | 1 (isolated original-code) | PROVEN |
| each of the five equipment slots contributes at most one status, from row +0x1A, and 0xFF means none | `00310071`–`00310121`, with `BattleEncodedId_IsValidForClass(6, id, 0)` and the row resolved at `base + (id - 0x1000) * stride` | 1 (isolated original-code) | PROVEN |
| an equipment row contributes only when its gate returns exactly 3 | `0031E9A0(row) == 3` | 1 (isolated original-code) | PROVEN |
| the licence contribution walks ids 0 to 360 against the owned bits at +0x194 | `00310140`–`003102DF`, bound `0x169` read from the compare | 1 (isolated original-code) | PROVEN |
| a licence row contributes only when its gate returns exactly 2 | `00323890(row[+5]) == 2` | 1 (isolated original-code) | PROVEN |
| the licence lookup has no bounds check against the table's record count | no compare stands between the id and the indexed load — see §10 | 1 (static) | PROVEN |
| the apply is a DIFF, not a reapply | `00310310`–`00310336`: `changed = new ^ current`, `added = changed & new`, `removed = changed & current`, sixteen bytes at a time | 1 (isolated original-code) | PROVEN |
| the applier is called once per CHANGED bit, with 3 for an addition and 1 for a removal | `0030E130(stats, index, 0, r15, 3)` and `(…, 1)` in the single pass at `00310340`–`003103A3` | 1 (isolated original-code) | PROVEN |
| the tail calls 002FEF30 exactly once | `003103AD` | 1 (isolated original-code) | PROVEN |
| this function computes no stat contribution | the negative in §1: nothing in the three accumulations (`0030FF6C`–`003102DF`) or the apply (`00310310`–`003103A3`) of `0030FED0` touches a stat field | 1 (static) | PROVEN |
| the entry takes a SECOND parameter, a flag word | `0030FEF8 mov r15d, edx` / `or r15d, 0x202`; that word is the sixth argument of every cascade call. **This contract had one parameter until 2026-09-12** | 1 (isolated original-code) | PROVEN |
| a kind-1 record accumulates from 128 bits at [unit + 0xE80] and never reads a definition row | `0031001A`–`0031006F`, reached by the kind test at `0030FF1F`. **This contract described the kind-0 path only** | 1 (isolated original-code) | PROVEN |
| the definition row and the licence rows are reached through the authored-table lookup shape, resolving twice | `0030FF2B`–`0030FF65` and `00310154`–`0031018A`, both the idiom `CONTRACT-authored-table-row-lookup.md` specifies, and both leaving a null row pointer that is then read from | 1 (isolated original-code) | PROVEN |
| the two definition masks are walked differently from each other | `+0x50` two bits per iteration (`rol r9d, 1` at `0030FFA2`/`0030FFC7`, `add r8d, 2` at `0030FFCA`); `+0x54` one bit per iteration (`0031000F`/`00310012`) with a signed-division byte index `0030FFFA sar eax, 3` its own bounds make unreachable | 1 (static) | PROVEN |
| one licence node can grant EIGHT statuses | eight `uint16` fields at row `+0x08` through `+0x16`, each skipped when it is `0xFFFF`, at `003101A4`–`003102AE`. **This contract said only "contribute"** | 1 (isolated original-code) | PROVEN |
| the function does not end at the applier: four further stages follow | §7a — a mode-5 pass over `[unit + 0xE90]`, two byte exchanges with the spawn record, and three clamps that write `+0x48`, `+0x4C` and `+0x06` | 1 (isolated original-code) | PROVEN |
| a status change can lower current HP here rather than in the HP write | `003104BF`–`00310508` recomputes the HP write's own cap and stores the clamped value | 1 (isolated original-code) | PROVEN |
| the second half is gated on kind ONE, and every other kind lands on the clamps | `0030FF12 lea r13d, [rax+1]` sets the comparand and `003103BB` / `jne 003104BF` jumps **into** the clamps. Executed at kinds 0, 1 and 2; the control that gated it on kind 0 failed on 612 of 730 lines | 1 (isolated original-code) | PROVEN |
| nothing writes the accumulation back into +0x78 | `00310310`–`00310336` stores only `added` and `removed`, both to the stack. Executed; the control that copied it back failed on 19 of 719 lines | 1 (isolated original-code) | PROVEN |
| the spawn record and the stats record exchange FIVE bytes, in one direction chosen by a flag | `0031043A test byte ptr [spawn], 0x80`, and the set arm ends `0031047E jmp 003104BF`. Executed with the flag set, clear, and with no spawn record at all | 1 (isolated original-code) | PROVEN |
| the equipment gate receives the row ADDRESS, which is zero when the resolve failed | `003100E2 mov rcx, rdi`. Executed with all three registry slots null, where the original passes 0 and a fixture pointer into its own page-zero would not | 1 (isolated original-code) | PROVEN |
| nothing observed at runtime | — see §13 | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

`0030FED0` decoded whole — 1,787 bytes, **506 instructions**, per function rather than by a linear
sweep. Every structural claim reproduced **at the address it names**:

| claim | found |
|---|---|
| sixteen bytes diffed, `r10 = 0x10` at `003102EA` | `003102EA mov r10d, 0x10` |
| the apply loop bounded at `cmp edi, 0x80` (`0031039D`) | `0031039D cmp edi, 0x80` — and a second bound `00310069 cmp edx, 0x80` on the kind-1 path |
| the licence walk runs ids 0…360, bound `0x169` | `003102D9 cmp ebp, 0x169` |
| a licence row contributes only when `00323890(row[+5]) == 2` | `00310192 movzx ecx, byte [rdi+5]` / `call 00323890` / `0031019B cmp eax, 2` |
| the equipment gate `0031E9A0(row) == 3` | called **once** |
| **the tail calls `002FEF30` exactly once** | **×1** — `BattleStats_RebuildEffectiveStatsAndAffinityState` |

### The negative claim, with every compare enumerated

*"The licence lookup has no bounds check against the table's record count."* A negative needs a
control, so rather than assert an absence I printed **every** `cmp`/`test` in the walk
`00310140`–`003102DF`. There are thirteen: the owned-bit test `[rax+rbx+0x194]`, two null tests, the
gate `== 2`, the **eight** sentinel compares, and the loop bound `0x169`. **None compares the id
against a record count.** The claim holds, and the list is the evidence rather than the conclusion.

### Trap — the `0xFFFF` sentinel is not an immediate in the loop

§15 says the eight `uint16` fields are *"each skipped when it is `0xFFFF`"*. **Grepping the walk for
`0xFFFF` finds nothing**: the sentinel is hoisted once, `0031012E mov r12d, 0xffff`, and the loop
compares `cmp ax, r12w` eight times — at `003101A8`, `1CE`, `1F4`, `21A`, `240`, `266`, `28C`, `2B2`,
evenly spaced `0x26` apart, reading `[rdi+8]`, `[rdi+0xA]` … `[rdi+0x16]`. **Eight fields,
`+0x08`–`+0x16`, exactly as claimed** — and `r12` is written nowhere else in the 1,787 bytes. Recorded
because a reader checking the immediate would conclude the sentinel is absent.

Each surviving status is set with `bts` into a stack bitmap at `[rsp+0x40]` via `shr rax, 3` /
`and edx, 7` — the 128-bit space addressed byte-and-bit, consistent with the sixteen-byte diff.

### Cross-contract join: this is what the status write's terminal tail calls

[`CONTRACT-status-write.md`](CONTRACT-status-write.md) §15a corrected `0030E816` from *"the
do-nothing target"* to **the shared tail every terminal case reaches**, and the call it makes under
`bt eax, 9` clear is `0030E828 call 0030FED0` — **this contract's subject**. Read from this side, the
edge is one of **22 call sites in 12 functions**, among them:

| caller | sites |
|---|---:|
| `BattleUnit_ExecuteDirectStateCommandOrder` | **12** |
| `BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`) | 1 — **the status-write subject, at `0030E828`** |
| `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (`0030E130`) | 1 |
| `BattleStats_RemoveAllMode0StatusesAndRecompute`, `…RemoveStatusesFromMaskAndRecompute`, `SpawnUnit_FinalizeSpawnEntryActivation`, `BattleFormula_ApplyTargetResult`, `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth`, `BattleStats_SetEquipmentSlotBy…` ×2, `FUN_0030C470` | 1 each |

> **The two contracts call each other.** This subject calls `0030E130` and `0030E360` (the status
> write) to apply each changed bit, and `0030E360`'s own terminal tail calls back into this subject.
> Neither document recorded the return edge; both now do.

**Not claimed:** no live observation and no execution — the claims above are static re-derivation of
an isolated-original-code contract, and §13 is unchanged.

## 16. Parity plan

Reproduce: the three sources and their two gate values, the 128-bit space, and above all **the diff**
— a reimplementation that cleared and reapplied would fire every side effect of the status cascade on
every equipment change.

## 17. Related

- `12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md`
- `_types` — `BattleStatsRecord +0x78`, `+0x50`, `+0x194`; `EquipmentDefinitionRecord +0x1A`

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

The rebuild is reached from, and reaches, four other layers.

- **Items_Equipment_Shops_License — the rebuild's triggers.** `BattleStats_RecomputeDerivedStateAndAutoStatuses`
  (`0030FED0`) and `BattleStats_FindOwningBattleUnit` (`0031B860`) are both called from:
  - the three equipment-slot setters `BattleStats_SetEquipmentSlotByStatsIndex`, `…ByMappedId` and `…Direct`;
  - the licence-node setter `BattleStats_SetLicenseNodeStateAndApplySideEffects`.

  So equipping an item or learning a licence node runs this operation
  ([equipment slots and the single-stat rebuild](../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md)).
- **Rewards_Progression_Economy.**
  - The level-up path `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` calls both functions.
  - The 432-byte level-rank caller of `BattleStats_ComputeLicenseDerivedRank` calls `0030FED0`.
  - `Reward_ComputeExperienceForRecipient` calls `0031B860`.
  - The status changer `0030E360` calls `BattleUnit_ProcessDefeatRewardsAndLoot` when a change is lethal.
- **ActorEntity and Gameplay — the class test.** `BattleEncodedId_IsValidForClass` (`00322C50`), which the rebuild
  uses, has callers across the unit model:
  - `BattleSlotMap_InitializeMappingClasses`, `BattleUnit_ApplyUnitDefinition`, `BattleGroup_RefreshFourActorDefinitions`,
    `BattleUnit_FindByDefinitionSelector` and `BattleUnit_FindMappedDefinitionSelectorByIndex`;
  - `BattleSlotMap_ResolveMappedBattleSlot`;
  - the 8,136-byte unnamed body that also calls `BattleDefinition_MapByte9ToRuntimeCategory` through a 68-byte adapter.

  The stats rebuild `BattleStats_RebuildEffectiveStatsAndAffinityState` and the status paths
  `0030E130` / `0030E360` also call it, together with `BattleUnit_UpdateEngagementStateFlag` and
  `BattleUnit_DispatchActorPresentationEvent`. `0030E360` also calls `00300FC0`, which cancels the unit's current
  action and sets its movement speed.
- **Movement.** Two locomotion bodies (706 B and 89 B) call `0031B860` to find the unit that owns a stats record, and
  two more (668 B and 419 B) call the class test. Those are lookups on the same records; whether any of them leads to
  a rebuild is not read.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `BattleEnmity_AnyAboveThreshold`, owned by that layer, calls `00322C50` on this page. That caller is the threshold scan over the same enmity bytes at `[+0x6A0] + 0x19`, id by id; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT (35 edges, one fan-in).** All 35 edges are CombatFormula bodies calling `0031B860` on this page: the reverse lookup from a stats record to its owning battle unit that this page documents. `BattleStats_ReconcileCurrentHpToEffectiveMaximum` is the worked example - it needs the owning unit before it can compare the effective maximum against `dword[+0x48]`. The crossing is **one shared primitive with 35 callers**, not 35 separate relationships, and naming a single body would say less than the count does. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT.** `BattleMenu_BuildCommandEntryList`, owned by that layer, calls `00322C50` on this page. That caller is the command-list build, and the ceiling is in the first instruction: the menu kind is bounded at **`0x22`** into a jump table, after which `dword[+0x40]` is zeroed and `dword[+0x44]` set to `-1` before any entry is written; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

*Almost every subject below is cited only in section 13, where the harness runs the rebuild's downstream tail from shipped bytes (release and teardown carriers, the EXP/LP share, the display-request queue, the text interpreter and the render-device ops). The edges are those executed bodies' other callers and callees; the rebuild itself owns none of them.*

**Audio — SERVICE and OUT-OF-SCOPE (6 edges).** The level-set growth body `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` and `BattleFormula_ApplyTargetResult` `003112F0` both call the Audio-owned bodies `002DF220` (an id-gated request: it returns early for `-1`) and `003A1180` (it returns `-1` at once when its first query answers non-zero); the vertex-batch submitter `001E8070` calls the four-byte field getter `00225690`; the Audio body `00362850` calls `Actor_GetWorldPosition` `00265020`. The first four are the level-up and result-apply paths calling into that layer (what the two bodies play or post is not read here); the last two are shared leaves (a field getter and the actor position read) and carry no rebuild meaning.

**Combat — MECHANICAL (1 edge).** `003206E0`, filed to that label, calls `ActorWork_GetBattleUnitRaw` `00263E30`, the raw unit getter the harness ran in section 13bg. It is one more caller of a shared unit accessor.

**CoreRuntimeScheduling — MECHANICAL and OUT-OF-SCOPE (8 edges).** `00254A10`, `002AC5F0` and `EnemyChain_UpdateOnDefeat` `00317ED0` call the global-dword leaf `00229E40`; `00301140`, `BattleUnit_ComputePartyBattleStance` `00308130` and the dedup-ring inserter `0046AB10` call `GameClock_GetRawTickCounter` `0032A150`; `0017D4C0` (the boot path that calls the boot fixer) calls the render-device op `001B1C00`; `MainLoop_UpdateAndRenderFrame` `0022B8C0` calls the bit-select helper `002E1CA0`. These are a tick read, a global read and two frame-level callers of leaves the harness executed; none decides anything the rebuild does.

**Input and InputGameplay — CLIENT, OUT-OF-SCOPE (14 edges).** `InputManager_TranslateBindingProfileToControlState` `00197160`, `00197790` and `00197800` call the lazy singleton accessor `001D50D0`; the inline-glyph drawer `002AEB20` calls `001E0C10`, `001E0C30` and the escape-code dispatch `002AB8F0` (the button-glyph lookup); `00226BE0` and `002E09A0` call the handle resolver `00263FF0`, and `00226BE0` also calls `PartyRoster_GetActorBySlot` `00263750`; `InputGameplay_ArbitrateDigitalInputAndModalState` `00253C70` calls `FieldData_GetActiveFieldRecordBit15` `00377C20` and its jump `00313F60`; the capability reconciliation `00313A00` calls `002E1C20`, `002E1CA0` and `00377C20`. The input layer reaches the same singleton, handle, roster and field-bit leaves the harness ran, and the text drawer asks it for a glyph; no input state feeds the rebuild.

**Party — CLIENT and SERVICE (68 edges).** The class test `BattleEncodedId_IsValidForClass` `00322C50` is called by nine roster bodies (`PartyConfiguration_AddSelector07To25ToAvailablePrimaryIndex` `003170E0`, `0031AC00`, `PartyConfiguration_CollectRuntimeRosterSelectors0To3` `0031B510`, `PartyFocus_SelectAndRequestDefaultActor` `00326500` and five more); `PartyRoster_GetActorBySlot` `00263750`, `ActorHandle_EncodeRegistryEntry` `003589B0`, `ActorWork_GetBattleUnitRaw` `00263E30` and `Actor_GetWorldPosition` `00265020` are called by the roster, focus and leader bodies (`003261D0`, `003273D0`, `00269C70`, `0050C610`, `0031B7E0`, `003272A0`, `00359150` among them); the release carriers `00300FC0`, `00310780`, `0030C970`, `00311B20` and `003138D0` call `BattleUnit_ResolveByFocusHandle` `0031B7E0`, `PartyFocus_GetCurrentPackedActorHandle_Thunk` `003272E0` or `PartyControl_RecomputeSuppressionFromLeaderBattleState` `0023B040`; `0023B040` calls `BattleUnit_GetPartyLeader` `003272A0` and the two suppression setters `00359200` and `003592C0`; the `resetJobs` body `00328BD0` calls `0030FED0` and `003138D0`. When a unit is released the carriers re-resolve the leader and focus and recompute party suppression, and the roster bodies share this page's class test and unit accessors; the only call into the rebuild itself is `resetJobs`.

**Platform and PlatformOnlineAchievements — SERVICE (35 edges).** The EXP/LP distributor `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` and `GameState_SetGil` `00254EE0` call the per-kind stat accumulator `00316A50`; `00316A50` calls `00315E90`, `003165C0`, `003166F0`, `00316BF0` and the notify gate `008632B0`; `00315E90` (the achieved-bit pre-check) calls `00315420`, `003160C0`, `003161A0`, `003165C0`, `003166F0`, `00316760` and `008632B0`, and is called by `00316930`; `008632B0` calls the singleton getter `0020CE00` and `0020CE60` and is called by `003162E0` and `00316440`; `00316760` is called by `00316810` and `00316C60`; `0020CE00` is called by `00863240` and `00863280`; the singleton allocator path `001CCB20` calls the platform timer `005CC930`. A reward or gil change feeds the achievement counters, which test the achieved bit and post through the notify gate `008632B0` (sections 13ai and 13ao); the timer edge is the singleton's allocation path, not rebuild behaviour.

**Presentation — CLIENT, SERVICE and OUT-OF-SCOPE (283 edges).** Most edges are the render and text machinery's own callers of bodies the harness executed: `CharacterRenderHierarchy_TraverseIndexDepthFirst` `0042EF90` (44 callers, among them `00425FB0`, `00429020` and `0042C8F0`), the signature gate `00426220` (30 callers) and `00426FA0` (called by `RenderRecords_ProcessDirtyState` `00427DE0` and four more), reached in section 13bm; `RenderCommand_SubmitCurrentBufferAndSwap` `003A1DB0` (16 callers, and it calls `GraphicsCommand_PublishCompletedBatchState100` `0036F360`); the render-device ops `001B1C00`, `001B06D0`, `001B1910`, `001B2410`, `001B2490`, `001B22D0`, `001B22E0`, `001B0100` and `001AED50`, called by the device bodies `00180E70`, `001D72F0`, `001D76A0` and their siblings; the text interpreter and its helpers `002AC5F0`, `002AC2F0`, `002AE450`, `002AE610`, `002AEB20`, `002A9F00`, `002B1F20`, `002B1FB0`, `002B2150`, `002B4730`, `0039C4A0` and the `0017F7C0`/`0017FC90`/`0017FD30` metric family, called by the text screens `002AAE40`, `002AFDC0`, `002B0280` and `002B4810`; the tag-15 parsers `003FFAB0` through `003FFF10`; the lookup `002DD7E0` (10 callers, `00245170` to `004048E0`) and the named-resource lookup `0024A5A0` (6 callers); `00265020`, `00263FF0` and `003589B0`, called by presentation bodies such as `003A4290`, `003A56F0` and `00465120`; `002EB0D0`, which calls the eight node-flag writers `004270A0` to `004278B0`. The edges that carry rebuild-tail meaning are few: `00301140` calls `BattleUnit_ComputePresentationSuppressionMask` `003125E0` when a unit recovers from a terminal status; `00312280` calls `Reward_PublishExpLpPresentation` `0028FB80`, which calls `00289D00`; `Loot_CreateWorldPickup` `00319CA0` calls `Loot_DeriveWorldPickupPresentationTier` `00319A20`; the reaction submitters `003283D0`, `BattleUnit_SubmitResultReactionMode` `00328480` and `003284D0` call `BattlePresentation_EnqueueReactionWithRandomizedVariant` `003BBD00`, which calls `00506700` and `0028FBE0`; `PartyCombat_UpdateStanceState` `00307E70`, `003125E0`, `BattleUnit_BroadcastPartyCombatTargetRelation` `00313B30` and `AddMotion_ApplyBonePose` `003714A0` call `00377C20`. The rebuild's tail posts result reactions, EXP/LP numbers and pickup tiers to the presentation queue and recomputes a unit's display suppression; the rest is that layer's text and render machinery calling helpers the harness happened to execute.

**Resource — SERVICE (1 edge).** The display-entry builder `00506700` calls the named-resource lookup `0024A5A0` (`"battle_4_p"` in section 13k). A display request resolves its sprite resource by name; the rebuild owns no resource.

**Save_Load_Settings — CLIENT, OUT-OF-SCOPE (8 edges).** `SaveStorageQueue_ControllerStateHandler` `005823B0` and `SaveLoad_ControllerLifecycleHandler` `00582860` call the bit helpers `002E1C20` and `002E1CA0`; `SaveImage_FinalizeHeaderAndChecksum` `00583D60` calls the EXP-suppression flag read `00236780`; `SaveSlotMetadata_BuildSubmissionDescriptor` `005832B0` calls the language-set check `00254A10`; `00581930` calls `002DD7E0`; `PersistentFlag_QueryBank2048` `0032A930` calls `SaveImage_GetPersistentPayloadBase` `002EF2B0`. The save layer shares these flag and lookup leaves, and the persistent-flag test reads its bank out of the save image; nothing in the save path runs the rebuild.

**Script_VM_Native_Bridge — CLIENT (116 edges).** Script verb handlers call the shared leaves the harness ran: `Actor_GetWorldPosition` `00265020` (23 handlers, among them `0033FD60`, `00344AF0`, `0050E060`), `PartyRoster_GetActorBySlot` `00263750` (20, among them `003415D0`, `00342250`, `003537D0`), the handle resolver `00263FF0` (20, among them `0033F7F0`, `00348130`, `0050D0C0`), `ActorHandle_EncodeRegistryEntry` `003589B0` (12), the unlink leaf `002ECF10` (10), `BattleStats_GetByMappedBattleSlot` `00320AB0` (7, the `0050FD00` to `0050FF20` run), `002EB430` (6), `00377C20` (4), `0026DAC0` and `003A1920` (3 each), `00229E40` (2), and one each for `00264150`, `002E8060`, `002E9600`, `002EB030`, `0032A930` and `008632B0`. Script verbs resolve actors, positions and roster slots through the same accessors and set the same entity flags; the edges are fan-in on those leaves, not a script route into the rebuild.

**Spawn_Encounter_Lifecycle — CLIENT (19 edges).** `Spawn_TrySelectCandidatePosition` `00234AF0`, `Spawn_ValidateCandidateDistanceToPlayers` `00234DA0` and `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` call `00265020`, `003272A0`, `0031B810` and `00313F60`, and `00308040` calls `00234DA0` back; `SpawnKeep_RotatePersistenceBanksForAreaTransition` `00233780`, `Spawn_SelectAndPrepareAutomaticEntry` `00235720` and `SpawnEntry_GetElapsedTicksSinceLastDeath` `00235FB0` call `0032A150`; `Spawn_CountActiveCapTrackedActors` `00308D90` calls `00236820` and `00236850`; `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` calls `BattleUnit_RefreshActorRuntimeFromDefinition` `00238BF0` and `0030FED0`; `002398F0` calls the level-rank body `0030C470`; `SpawnGroup_RecordMemberDeathAndHandleCompletion` `00306F00` calls `BattleUnit_DispatchActorPresentationEvent` `003299B0`. Spawn activation runs the rebuild once for a new unit; the other edges are the spawn layer using the same leader, position, tick and unit accessors.

**Story_Event_Quest_Hunt — SERVICE (2 edges).** The tag-15 resolvers `00263990` and `002639E0` call `PersistentFlag_QueryBank2048` `0032A930`. A text escape code can depend on a persistent story flag (section 13v); this is in the text tail, not the rebuild.

**WorldAreaField — DEPENDENCY and CLIENT (27 edges).** `00307D10`, `0030D9A0`, `0030E360`, `00311B20`, `00311CF0`, `00312280` and `003125E0` call `FieldData_GetActiveFieldRecordBit15` `00377C20`, and `00237260`, `002372E0`, `002373C0`, `0023B040`, `00320450`, `003243F0` and `00329A20` call its jump `00313F60`; `00377C20` calls `WorldTransition_GetActiveOrPendingFieldId` `003148F0` and is called by `BattleSystem_InitializeAreaState` `002342F0`; `BattleSystem_RunFieldFrameOrchestrator` `00234590` calls `00237260`, `0023B040`, `00300140`, `00313F60`, `0031B770`, `003272A0`, `0032A150` and `0035C8A0`; `005369C0` calls `MapRef_GetAreaArdFieldResourceIndex` `00264ED0` and `003148F0`; `0057FB00` calls `00264150`. The release, status-change and reward bodies consult the field record's bit 15 before acting, and the field frame is the per-frame caller of several carriers the harness ran.
