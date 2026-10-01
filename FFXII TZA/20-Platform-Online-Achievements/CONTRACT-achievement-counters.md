---
contract: move an achievement's counter or fire it, under a layout an authored table dictates
category: 20-Platform-Online-Achievements
scope: family
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md
entries: ["00316A50", "003166F0", "00315E90", "003165C0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 45 addresses cited - 3 data, 7 entry, 34 interior, 1 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-achievement-counters-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the achievement counter family

Gameplay tells this family "achievement `n`, amount `x`". What happens next is decided entirely by
**an authored table**: whether the amount is a trigger or an increment, how wide the counter is,
where in the save it lives, and whether it fires at all.

**Scope, stated first.** The counter update, the counter read and the descriptor gates are specified
here. `00315E90`'s store dispatches on the mode byte through an **eight-arm jump table** (`cmp eax, 7`
/ `ja` at `00315F03`, table at `0x120000 + 0x1F6098`) and `003165C0` walks a relative-offset chain at
`022C2550`; **neither is specified** — they are named and bounded, and each arm's behaviour is open.

The first contract in `20-Platform-Online-Achievements`.

## 1. Purpose

To state the parts a reconstruction must get exactly right — the two paths, the saturation, the id
bound and the authored layout — and to be explicit about the part that is not read.

## 2. Interface

| | |
|---|---|
| update | `00316A50` `AchievementCounter_UpdateAndMaybeFire` — `cl` = achievement id, `edx` = amount |
| read | `003166F0` — `cl` = id, returns the counter in `eax`, `-1` on rejection |
| **evaluate and award** | `00315E90` — **`cl` = id ALONE.** Checks the awarded bit, then dispatches on the descriptor's `+0x02` through the eight-arm jump table at `00316098`. **It is not a store and `edx` is never read** — see the box below |
| **store a counter value** | `00316BF0` — `cl` = id, `edx` = value; writes at the counter's own width. **Missing from this contract until 2026-09-12** |
| fire helper | `003165C0` — `cl` = id |

> **Crossing into Presentation — the debug menu reads the counters (FINAL-AUDIT pass 22, FABLE, 2026-09-14).** The read
> `003166F0` has one caller outside this family. It is the developer debug-menu renderer, `DebugMenu_Render`
> ([what the console tunes](../00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md)), which the
> ledger files under Presentation. For ids **0, 1, 2, 3, 4 and 11** it calls `003165C0(id)` and then `003166F0(id)`. It
> prints the pair through `"%s%s %d/%d"` (`00900258`, via `0019C5D0`), the counter first and `003165C0`'s return second
> (`001CFB11`–`001CFB2C`, and the `mov cl, n` arms at `001CFB31`–`001CFB5D`). The renderer only reads, and nothing on
> that path writes a counter. The format suggests the second number is a target; that is **not established**, and
> `003165C0` stays unspecified, as the scope note says.

> ### ⚠ `00315E90` is not the store, and the real store was missing
>
> **CORRECTED 2026-09-12 (`OPUS-ACHIEVE-ISOLATED`), from the bodies.** This contract called
> `00315E90` the store and gave it `edx` = value. Reading it:
>
> - it rejects `cl >= 0x1F`, then for an id below `0x1E` tests that id's bit in the awarded bitset at
>   `saveBase + 0x3844` and **returns if it is already set** (`00315EDF`);
> - otherwise it reads the descriptor's `+0x02` and, when that is `<= 7`, jumps through the eight-arm
>   table at `00316098` (`00315F0C`–`00315F17`);
> - each arm decides whether the achievement is now COMPLETE — arm 0 takes a threshold from
>   `003165C0`, falls back to the descriptor's `+0x04`, reads the counter through `00316760`, and
>   compares;
> - **`edx` is never read, and nothing is written to a counter anywhere in it.**
>
> **The eight-arm dispatch this contract describes is real** — it just belongs to a completion check,
> not to a store. The store is **`00316BF0`**, which this contract did not mention at all: it
> validates the id, reads the `kind` byte, and writes a **word** for kind 2 or a **dword** for kind 4.
>
> ### And the award is decided BEFORE the new value is stored
>
> In the update path the two are called back to back — `00316BC1 call 00315E90`, then
> `00316BCC call 00316BF0` with the new value. `00315E90` reaches the counter through `00316760`,
> which calls the read `003166F0`. **So the completion check sees the counter as it was before this
> update**, and an achievement whose counter crosses its threshold is awarded on the *next* update
> rather than the one that crossed it.
>
> That is the mechanism, read from the call order; whether it is intended is not established here.
> A reimplementation that stored first and checked second would award one update earlier and pass any
> test that only inspects counters.

## 3. Types

| | |
|---|---|
| `AchievementDescriptor` | `0x00D10460`, 30 entries of 8 bytes, in `.rdata` |
| `AchievementState` | `SaveImage_GetActiveBuffer() + 0x3844`, 40 bytes: `+0x3844` award bitmap (4 B, `bts`-only), `+0x3848` kind-7 flag bitmap (4 B, `bts`/`btr` — reversible), `+0x384C` counter block (`0x20`) |

**The descriptor decides the storage.** `kind` is the counter's **width in bytes** on the accumulate
path, `+0x01` is the counter's **byte offset** inside the save block, `mode` selects the test on the
trigger path and the arm on the store path, and `threshold` is compared **only on mode 1**.

## 4. Preconditions · postconditions · invariants

**The id is bounded at 30 before anything else happens**, in all three entry points:
`cmp cl, 0x1e` / `jae` at `00316A50`, ~~`cmp esi, 0x1e` / `jae` at `00315EB0`~~ **`cmp cl, 0x1f` / `jae` at `00315E90`**,
and both `cmp dil, 0x1f` and `cmp dil, 0x1e` at `0031670B`–`00316715`. *Corrected 2026-09-25 (FABLE, Claude Opus 5.5),
on OPUS block 301.* The evaluator `00315E90`'s own first instruction bounds the id at **31**. Its `cmp esi, 0x1e` at
`00315EB0` is an inner branch: id 30 passes the entry and only skips the bitmap read (`jae 00315EE5`). So this entry
point admits one more id than the other two. An out-of-range id is rejected silently; the read
returns `-1`.

**Invariant: a counter never wraps.** The accumulate path saturates at the signed maximum of its
declared width — `0x7FFF` for `kind == 2` (`00316B8B`) and `0x7FFFFFFF` for `kind == 4` (`00316BA9`)
— by testing `amount > MAX - current` **before** adding, so the addition itself cannot overflow.
**Any other `kind` adds with no clamp at all** (`00316BBB`), and no shipped descriptor has one.

## 5. State

Read: the descriptor table (never written — it is `.rdata`). Read and written: `AchievementState`.
Nothing else.

## 6. Relationships

- **Upstream:** every gameplay system that moves a counter — the catalogue page names Rewards,
  Combat and Movement.
- **Downstream:** the Steam User Stats interface, reached through the store's mode arms.
- **The layout link runs backwards from the usual direction.** Code normally reads authored data;
  here authored data decides *where in the save file* the code writes. Changing a descriptor's
  `+0x01` moves a counter.

## 7. State transitions

`00316A50`, after the id bound:

**Trigger path — `kind == 0`** (`00316A81` `cmp byte [desc], 0`):

| mode | behaviour |
|---|---|
| `0` | fire unconditionally through `003165C0` (`00316A99` → `00316AF4`) |
| `1` | fire **only if the amount equals `threshold`** — `cmp edx, dword [desc+4]` at `00316AA6`, `jne` away |
| anything else | **return without firing** (`00316AA0` `jne 00316BD1`) |

Of the nineteen trigger descriptors, one is mode 1 (`threshold` 53375) and three are mode 0; the rest
carry modes 2, 5, 6 and 7 and therefore **never fire through this function**. That is why their
`+0x04` values look arbitrary: nothing reads them.

> **THE TWO BOUNDS ARE DIFFERENT AND ONE ID FALLS IN THE GAP — `EXP-089`, consumed 2026-09-16 (OPUS),
> verified from the authority image rather than adopted.** The first instruction of each entry point
> is its own bound and they do not agree:
>
> ```
> 00315E90  cmp cl, 0x1f / jae     evaluate  accepts id < 0x1F   (0..30)
> 00316A50  cmp cl, 0x1e / jae     update    accepts id < 0x1E   (0..29)
> ```
>
> **So `id 30` EVALUATES AND CAN NEVER UPDATE.** It evaluates against descriptor-**overrun** bytes —
> past the table's last row, where the award-code dword aliases into the kind/mode fields and reads
> as kind 1 / mode 0 — and any counter write it would imply is refused one function earlier. This
> contract already states both numbers separately (§4's `cl >= 0x1F` then `< 0x1E`, §7's
> `if (id >= 30) return` for `00316A50`, §12's pair at `0031670B`/`00316711`); what it never said is
> that **they are not the same bound**, and §16 asked a reimplementer to reproduce "the id bound" as
> though there were one. A reconstruction that picks either number and uses it in both places is
> wrong in one of them, and wrong only for a single id — which is exactly the kind of difference a
> fixture that tests 0 and 29 will never show.
>
> **Two more measured behaviours this contract did not carry:** a threshold-crossing award **lands
> one update late**, because the order is read → add-by-kind → evaluate → store and the evaluation
> sees the pre-add counter; and **mode 8's update still performs the counter READ** before skipping
> the evaluate and store, so it is not a no-op at the memory-traffic level even though it changes
> nothing.

**Accumulate path — `kind != 0`** (`00316B51`):

```
current = Read(id)                     00316B55 -> 003166F0
mode 0 : saturating add by kind        00316B7E
mode 3 : bts current, (amount - 0xE2)  00316B73   <- a BITSET, not an add
mode 8 : return without storing        00316B6F
other  : store current unchanged       00316B71
Store(id, result)                      00316BBD -> 00315E90
```

**Mode 3 is not an accumulation at all** — it sets bit `amount - 0xE2` in the counter, so that
counter is a set of things seen rather than a count of them, and the bias means the amounts it
receives start at `0xE2`.

**The read**, `003166F0`: resolve the save buffer, form `base + 0x384C`, take `kind` from the
descriptor, and read **`byte [desc+1]` bytes into that block at the width `kind` names** — a `dword`
read on the `kind == 4` arm (`0031673B`), a narrower one on the `kind == 2` arm. Any other kind
returns `-1`.

## 8. Script · resource · event interactions

The descriptor table is authored data in `.rdata` and is never written. It is not reached through the
registry — it is a direct image address, unlike most authored tables in this database.

## 9. Determinism

Fully deterministic given the save state and the amount.

## 10. Failure paths and edge conditions

- **Every rejection is silent.** An out-of-range id, an unhandled mode, a `kind` the read does not
  recognise — all return without a diagnostic, and the read's `-1` is indistinguishable from a
  counter legitimately holding `-1` if any ever did.
- **A saturated counter is indistinguishable from an exactly-full one.** Nothing records that a clamp
  occurred.
- **Mode 1's equality test means an amount that overshoots never fires.** `cmp` / `jne`, not `jge`:
  a trigger whose amount passes its threshold in one step is lost.
- The catalogue page records a separate concern — that a shared session advancing counters on several
  clients would unlock repeatedly — which is downstream of this family and not addressed here.

## 11. Observable behaviour

Not established. What would be observable: a `kind == 2` counter stops at 32,767 and stays there; a
mode-1 achievement does not fire if its amount jumps past the threshold.

## 12. Reproduction formula

```c
void AchievementCounter_UpdateAndMaybeFire(uint8_t id, int32_t amount)
{
    if (id >= 30) return;                                   /* 00316A50 */
    const AchievementDescriptor *d = &desc[id];             /* 00D10460 + id*8 */

    if (d->kind == 0) {                                     /* trigger */
        if (d->mode == 0)                    Fire(id);
        else if (d->mode == 1 && amount == d->threshold) Fire(id);
        return;                                             /* every other mode: nothing */
    }

    int32_t v = Read(id);                                   /* 003166F0 */
    switch (d->mode) {
    case 0:
        if (d->kind == 2) v = (amount > 0x7FFF     - v) ? 0x7FFF     : v + amount;
        else if (d->kind == 4) v = (amount > 0x7FFFFFFF - v) ? 0x7FFFFFFF : v + amount;
        else v += amount;                                   /* no clamp */
        break;
    case 3: v |= 1 << (amount - 0xE2); break;               /* a bitset */
    case 8: return;
    default: break;                                         /* stored unchanged */
    }
    Store(id, v);                                           /* 00315E90 */
}
```

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent.** (2026-09-12)

Three of the family's four bodies run at their real virtual addresses under Unicorn — the read
`003166F0`, the update `00316A50` and the store `00316BF0` — with the descriptor table mapped at
`00D10460` and the award-code table at `00D10550`, because each reaches them rip-relatively and
takes no table argument.

**Instrument:** [`diff_achievement_counters.py`](../../../Reconstruction/Tests/Differential/diff_achievement_counters.py)
against [`achievement_counters.c`](../../../Reconstruction/Game/Platform/achievement_counters.c).

**Result: 215 commands, 113 compared lines, 0 mismatches** — 15 distinct read values, 19 distinct
counter images, 4 distinct bitset images (so awards were recorded rather than merely attempted) and
6 traces carrying an award call.

~~**`00315E90` is answered, not run**, and `003165C0` likewise: the first dispatches through an
eight-arm table into per-achievement completion logic and the second walks a chain into another
subsystem's structure. Reproducing either would be testing something else.~~ Their *influence* is
driven — the lookup's threshold at zero and non-zero, and the order in which the awarder is called.

> **CORRECTED 2026-09-16 (OPUS). BOTH WERE RUN, AND THE ARGUMENT FOR NOT RUNNING THEM DID NOT
> SURVIVE SOMEBODY RUNNING THEM.** [`EXP-089`](../_experiments/EXP-089-achievement-evaluate-award.md)
> (SWE2-ORACLE, 2026-09-15, method B, isolated original-code under Unicorn against the shipping EXE)
> takes *"evaluate+award `00315E90`, fire helper `003165C0`, plus the whole bounded call surface"* as
> its subject and reports **54/54 cases pass, 9/9 byte-level mutants detected**.
>
> **The struck sentence is the most interesting of the four corrections made at this HEAD**, because
> it was not a stale date or a forgotten qualifier — it was a *reasoned prediction that reproducing
> these two would be testing something else*, and an experiment three days later reproduced them.
> The prediction is preserved above rather than deleted: a contract that argued a thing was not worth
> executing, and was then shown otherwise, is evidence about how this database reasons.
>
> Found by `check_experiments.py`, which lists EXP-089 under **NOT CITED — a RUN experiment its
> contract never names** *and exits 0*. Isolated original-code is still not live evidence.

### What the run established that reading had put in the wrong row

**The width claim and the saturation claim are one fact read twice, and both halves are now driven.**
Kind 2 is read `movsx word` and stored `mov word`; kind 4 is a dword; and the update saturates at
`0x7FFF` and `0x7FFFFFFF`, the signed maxima of exactly those widths. A value too large for a word is
stored under kind 2 and read back truncated and sign-extended, and both caps are approached from just
below and from far above.

**The negative clamp is not uniform**, which a reimplementation would tidy away. Kinds 2 and 4 reach
`add ebx, edi / jns` and clamp a negative sum to zero; the fall-through arm adds and does not.
Driven on all three.

**A faithfulness bug of mine that only the trace caught.** `003166F0` and `00316BF0` both call
`002536A0` at their very first instruction, *before* any range or kind test — so a rejected id still
makes the call. The reconstruction deferred it into the counter access, which produced identical
counters and a different call sequence on three cases. A state-only comparison would have passed.

### How far the instrument itself has been tested

**57 mutants: 47 KILLED · 6 EQUIVALENT · 2 SURVIVED · 2 NO_BUILD · 0 TIMEOUT · 0 INVALID.**
Production inputs verified stable, all four hashes checked against the working tree afterwards.

**Both survivors are the same provable equivalence**: the negative clamp's `value < 0` widened to
`value < 1`. The two differ only at `value == 0`, where both leave it zero. No case can distinguish
them and none should be contrived to.

**The redundant range test is now proven redundant by the compiler.** The read tests the id twice —
`>= 0x1F` at `0031670B` and `>= 0x1E` at `00316711`, both jumping to the same rejection — and
mutating either the constant or the comparison of the *first* test comes back **byte-identical**.
MSVC eliminates it entirely, which is an independent confirmation of a reading this contract could
otherwise only assert.

**The first campaign had three more survivors and each was a missing case, not a missing check:**

| what survived | why no case reached it |
|---|---|
| the second range test widened to `>` | nothing planted a real descriptor at id **30**, so the mutant read zeros and returned `-1` exactly as the original does. A descriptor is now planted one past the range, where only a widened bound can see it |
| `return -1` for a kind that stores nothing | no case ever read an id whose `kind` was `0` — every id read had a counter |
| the store's range test widened to `>` | the same id-30 gap, on the other entry point |

Each of the three is a case the suite should always have had, and all three are now killed. The
pattern is worth naming: **a bound is only tested by an input that sits on the wrong side of it**,
and a fixture that cannot express such an input makes the bound untestable rather than correct.

### What is still owed, and it is live-only

Unchanged: whether any of these counters is non-zero in a running game, and whether the award path
reaches a platform service at all. The descriptor table is `.rdata` and was read in full here, so
nothing about the widths or offsets is waiting on a capture.

Two checks, and the first needs no game at all:

1. **The descriptor table is `.rdata` at a fixed address**, so the eleven counters' widths and
   offsets in §3 can be confirmed by anyone with the executable — as they were here. What a live
   check adds is only whether the save block at `+0x3844` holds what the descriptors say it should:
   read 40 bytes after earning a counter achievement and confirm the value moved at the declared
   offset and width.
2. **The saturation.** A `kind == 2` counter held at `0x7FFF` across further increments.

Requested from ASTRA; not claimed by me.

## 14. Unresolved

- ~~The eight mode arms of the store `00315E90` — named and bounded, not specified.~~
  **CLOSED 2026-09-23 (SWE2-CONTRACT): all eight arms decoded.** The table at `00316098` holds
  eight dword RVAs added to `r15`; `00316045` is the shared award tail (`id < 30` →
  `bts [slot + id/8 + 0x3844], id&7` the unlocked bitmap, then `008632B0` with the descriptor's
  platform payload `[r15 + r14*4 + 0xBF0550]`):

  | mode | arm | behaviour |
  |---|---|---|
  | 0 | `00315F19` | counter ≥ threshold → award (threshold = `003165C0(id)`, falling back to descriptor `+4` when 0) |
  | 1 | `0031607D` | **no-op** — the epilogue itself |
  | 2 | `00315F46` | descriptor `+4` is a packed word pair `[lo,hi)`; loops `00309EC0(i)` over the range and awards only if **every** entry tests nonzero — a collect-all-in-range check |
  | 3 | `00315F87` | counts the low-16 set bits of `003166F0(id)` (the `shl`/`and`/`cmove` loop `00315FB0`–`00315FCB`) and awards when the count ≥ `003165C0(id)`, defaulting to `0x10` — a bit-count threshold |
  | 4 | `00315FDC` | predicate `003160C0()` → award if true |
  | 5 | `00315FEB` | predicate `003161A0()` → award if true |
  | 6 | `00315FFA` | walks the `022C2550` word-offset chain (same shape as `003165C0`), bounds-checks descriptor `+4` against `word[rax+2]`, fetches `word[rcx + rdx*2 + 4]` and calls `00315420` on it — award if `> 0` |
  | 7 | `0031607D` | **no-op** — shares mode 1's epilogue |
- ~~`003165C0`'s chain walk at `022C2550`.~~ **CLOSED 2026-09-23 (SWE2-CONTRACT): already
  specified by the EC7-26 update below, re-verified against the body.** `022C2550` holds the
  root pointer; the walk is **four** word-relative hops (`movzx word; add` — a zero word exits
  with 0) into the counter record `r10`, then `cl >= 0x20` rejects, `bt [r10+4], cl` must be
  set, and the popcount-below loop (`rol`-`and`-`cmove` at `00316640`–`00316659`) maps the bit
  index to `dword [r10 + r9*4 + 8]` — the stored counter. The EC7 note says "three" hops; the
  verified count is four (`003165DA`/`003165E3`/`003165EC`/`003165F5`), same mechanism.
- [x] ~~Which achievement each descriptor index is~~ — **CLOSED 2026-09-23 (SWE2-CONTRACT) by
      reference:** the join was completed by the catalogue page's AB-2 (2026-09-17) — the static
      record array at `01DFE410` (41 × `0x198` `{qword counter_id; tag*; inline title}`) maps
      every record to its counter id and `ACH_*` identifier; the full table is
      [`members/achievement-descriptors.tsv`](members/achievement-descriptors.tsv). The
      descriptor index *is* the counter id the TSV's `counter_id` column carries.
- [x] ~~The four bytes between the unlocked bitmap and the counter block, which nothing observed
      touches.~~ **CLOSED 2026-09-23 (SWE2-CONTRACT): they are a SECOND bitmap — the kind-7
      flag bank, and it is touched.** `+0x3848`–`+0x384B` hold 32 more per-id bits, byte-indexed
      `id/8` (`id < 0x1E` bounded like the award bank). Written by `00315B50`'s `cl==7` arm
      (`00315C7F`–`00315CA7`: `esi = id&7`, `bts` when the value arg is non-zero else `btr` —
      **reversible**, unlike the award bitmap's `bts`-only writes) and read back by `003157E7`'s
      `cl==7` arm (`00315805`: byte fetch → `0031573F` `test bit id&7 → bool`). So the
      `AchievementState` block is `+0x3844` award bitmap (4 B, set-only) + `+0x3848` flag bitmap
      (4 B, set-and-clear) + `+0x384C` counter block (`0x20`) = the stated 40 bytes exactly.
      The earlier "nothing touches" was a displacement census that predated the kind-7 arms.

## 15. Evidence

Static, from the shipping image (`73461D08…`). All four entry points were disassembled and read, and
**all 30 descriptors were read out of `.rdata`** rather than sampled — that read is what established
`kind` as a width and `+0x01` as an offset, and what showed the eleven counters tile the block.

**Claim table added 2026-09-12 (`OPUS-ACHIEVE-ISOLATED`).** The paragraph above states the method;
the table enumerates the claims so `diff_achievement_counters.py` can map to them. Row 2 credits this
section: `kind` was already established as a width here, and the pilot's contribution is that the
saturation caps are the signed maxima of those same widths — a second, independent reading of the
same byte.

| claim | evidence | tier | confidence |
|---|---|---|---|
| the descriptor table is 30 entries of 8 bytes at 00D10460 | all 30 read out of `.rdata`. Executed — driven at id 29 and at id 30 with a real descriptor planted there, so a widened bound reads it and the original does not | 1 (isolated original-code) | PROVEN |
| the first descriptor byte is the counter's WIDTH: 2 is a signed word, 4 a signed dword | `0031674A movsx ebx, word` / `00316C45 mov word` against `0031673B mov ebx, dword` / `00316C30 mov dword`. Executed — each read back at its own width, and an over-wide value truncated | 1 (isolated original-code) | PROVEN |
| update saturates at 0x7FFF for kind 2 and 0x7FFFFFFF for kind 4 | `00316B8B` and `00316BA9`. Executed at both caps from either side. **These are the signed maxima of the two widths above**, which is why the width is a reading and not a guess | 1 (isolated original-code) | PROVEN |
| a sum that goes negative is clamped to zero on kinds 2 and 4 but NOT on the fall-through | `00316B9F`/`00316BA1` versus `00316BBB`. Executed on all three arms | 1 (isolated original-code) | PROVEN |
| submode 3 treats the amount as a bit index biased by 0xE2, and submode 8 stores nothing | `00316B73 lea eax, [rdi - 0xE2]` then `bts`; `00316B6F`. Executed, with the counter compared either side | 1 (isolated original-code) | PROVEN |
| when the id has no counter, submode 0 fires on a threshold and submode 1 on an exact match | `00316AF4` against `00316AA6`. Executed at, below and above the threshold, and one either side of the exact match | 1 (isolated original-code) | PROVEN |
| the fire lookup supplies the threshold when it is non-zero | `00316AF8` then `00316B01`. Executed at zero and non-zero with the descriptor's own threshold set differently, so the two sources are distinguishable | 1 (isolated original-code) | PROVEN |
| the store is 00316BF0, not 00315E90 | `00315E90` takes the id alone, tests the awarded bit and dispatches on `+0x02` through the eight-arm table at `00316098`; it writes no counter and never reads `edx`. `00316BF0` is the store. **See the box in §2** | 1 (isolated original-code) | PROVEN |
| any runtime observation | — | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### Confirmed at the byte level

The descriptor table at `00D10460` is in **`.rdata`**, **30 entries of 8 bytes**, and the two entries
immediately after it (`01 00 00 00 02 00 00 00`, `03 00 00 00 04 00 00 00`) are plainly a different
structure — so the boundary is visible in the data, not merely asserted. Every cited instruction is
where the document puts it:

| claim | image |
|---|---|
| saturate at `0x7FFF` for kind 2 | `00316B8B mov eax, 0x7fff` |
| saturate at `0x7FFFFFFF` for kind 4 | `00316BA9 mov eax, 0x7fffffff` |
| clamp negatives on kinds 2 and 4 | `00316B9F jns 00316BBD` — and its target is **past** `00316BBB` |
| …but **not** on the fall-through | `00316BBB add ebx, edi`, which the `jns` jumps over |
| submode 3 biases by `0xE2` | `00316B73 lea eax, [rdi - 0xe2]` |

### Derived from the table: the counter block is `0x20` bytes, and only 11 ids have one

Reading all 30 first bytes gives the population the *"when the id has no counter"* claim is about,
which the document never numbers:

| width byte | meaning | ids |
|---|---|---:|
| `2` | signed word | **7** |
| `4` | signed dword | **4** |
| `0` | **no counter** | **19** |

**So 11 of 30 ids carry a counter and 19 do not.** And the second descriptor byte — the counter's
offset — falls out as a packed layout:

```
+0x00 +0x02 +0x04 +0x06 +0x08 +0x0A +0x0C    seven int16   (ids 0-4, 13, 14)
+0x0E                                         two bytes, unused - alignment
+0x10 +0x14 +0x18 +0x1C                       four int32    (ids 11, 6, 7, 17)
```

**The counter block is `0x20` bytes**: seven words end at `+0x0D`, and the dwords start at the next
4-byte boundary rather than at `+0x0E`. That gap is not a field — it is what the alignment of the
first `int32` costs — and a reconstruction that packed the dwords at `+0x0E` would place all four
counters wrong while every individual claim in §15 still held.

**Not claimed:** no runtime observation; §15's `UNKNOWN` row stands.

## 16. Parity plan

Reproduce: ~~the id bound~~ **the TWO id bounds and the gap between them** (see below), the two paths and their gate values, the saturation **tested before the add**
rather than after, mode 3's bitset with its `0xE2` bias, mode 1's equality rather than threshold
comparison, and above all the fact that the counter layout comes from the descriptor table and not
from a compiled-in map.

## 17. Related

- `20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md`
- `_types` — `AchievementDescriptor`, `AchievementState`

## SWE2-EC7-26 update (2026-09-18) — `003165C0` bit-index to counter read

`003165C0` (172 B) resolves the `022C2550` root through three
word-relative offset hops (`word[r] + r`, a zero hop returns 0) into
the counter record, rejects `cl >= 0x20`, requires `bt [r10+4], cl`
set, then rotates a 1-bit mask `cl` times accumulating the
popcount-below into `r9d` and returns `dword[r10 + r9*4 + 8]` — the
bit-index to stored-counter mapping. Interior anchor `00316617` (the
`bt` test).

## SWE2-EC7-102 update (2026-09-20) - `00282DD0` measured

`00282DD0` (28 B) is the `0xC0`-stride slot getter
`003162E0` and `00316760` call:
`rcx = ecx * 3 << 6` (`ecx * 0xC0`) and the return
is `*(0209AC30) + 0x408 + rcx` - the indexed
slot-address composer the counter walks share.
Interior anchor `00282DE4` (the `shl`).
