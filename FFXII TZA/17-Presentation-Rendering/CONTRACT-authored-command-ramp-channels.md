---
contract: set and advance the five per-slot linear ramps an authored presentation command drives
category: 17-Presentation-Rendering
scope: subsystem
readiness: DIFFERENTIAL TESTED # diff_ramp_channels.py, 483 commands / 129 compared lines / 0 mismatches, mutants killed (SWE2-CONTRACT, 2026-09-13, a27b5cc5)
confidence: PROVEN
implements: 17-Presentation-Rendering/README.md
entries: ["003B5890", "003B6890", "003B6950", "003B69B0", "003B6A10", "003B6A90"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 96 addresses cited - 16 data, 42 entry, 36 interior, 2 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-ramp-channels-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the authored-command ramp channels

> **Two of the ~~five~~ four setters are not in the function census** *(corrected 2026-10-02, OPUS: §2's four - `004173D0`+0x57 and `00417460`+0x57 call `003B6A90` / `003B6A10`, `00417440`+0x17 and `004174D0`+0x17 tail-jump to `003B69B0` / `003B6950`; the fifth channel's writer `003B5D40` is a direct call at `0041D560`+0x87, not a setter of this kind)*, and they are exactly the two reached by
> a tail `jmp` rather than a `call`. `003B69B0` and `003B6950` were found through
> [the referenced-but-unlisted census](../99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md);
> their two siblings, `003B6A90` and `003B6A10`, were in the list all along.

> **Scope key set to `subsystem` on 2026-09-22 (FABLE), on
> `OPUS-REQ-FABLE-RAMP-CHANNELS-SCOPE-NOT-A-GRAMMAR-VALUE`.** It read `state machine`, which is not
> one of the four values the contract template defines (`operation`, `family`, `transition`,
> `subsystem`) and was therefore **invisible to every census that reads the key** — S-48 was scored
> SCOPE-SHORT for that and for nothing else.
>
> **`subsystem`, not `transition`, and the reason is §4 rather than the entry count.** §7 is a state
> machine on two levels — slot `free`/`live`, channel `idle`/`ramping`/`suspended` — and §4 carries
> ordering *across* operations that a narrower scope would leave unstated: a setter call with
> `steps == 0` **cancels** a ramp an earlier setter started (§4.2), and whether the counter advances
> at all is decided by the tick's two gates (§4.4). Setter and tick therefore cannot be contracted
> separately. For calibration, the database's two `transition` contracts are each one operation plus
> the state change it triggers, at one and two entries; this is six.
>
> *The old token described §7 accurately — it simply was not in the grammar
> (`_templates/CONTRACT.md` line 4: `scope: operation | family | subsystem | transition`). Whether
> the template should gain a fifth value is a template change and is routed, not taken here.*
>
> **The reason is recorded in this body rather than as a trailing `#` comment beside the key, and
> NOT because a comment would break the census — it would not.** `knowledge_db.py`'s `frontmatter()`
> strips a trailing comment deliberately, carrying a note that leaving one in had once made `level`
> read as `L2   # calculation parity only, …` and split a census bucket in two. *I checked the
> parser before writing this sentence, having first written the opposite.* The reason to keep the
> key bare is narrower: the value is the thing a reader compares against the template's four, and
> one contract already carries a paragraph-long comment there that every hand-run `grep`-and-tally
> over the corpus reports as its own bucket.

## 1. The table

`003B6890` allocates it lazily: if `[02B40528]` is null it allocates **`0x8C00`** bytes, stores the
pointer, then loops **`0x50` times clearing bit 0 of two records per iteration**, stepping `0x1C0`.

**160 records of `0xE0` bytes.** `160 × 0xE0 = 0x8C00` — the allocation is the extent, with nothing
left over — and the advance in §3 independently counts `0xA0 = 160`.

## 2. Setting a ramp

Four authored-command classes drive four channels, one each:

| class | setter | in the census | counter | value(s) | delta(s) |
|---|---|---|---|---|---|
| `0x0D` | `003B6A90` | yes | `+0x00` | `+0x50`, `+0x54` | `+0x60`, `+0x64` |
| **`0x0E`** | **`003B69B0`** | **no** | `+0x01` | `+0x70` | `+0x74` |
| `0x0F` | `003B6A10` | yes | `+0x02` | `+0x58`, `+0x5C` | `+0x68`, `+0x6C` |
| **`0x10`** | **`003B6950`** | **no** | `+0x03` | `+0x78` | `+0x7C` |

A fifth channel — counter `+0x43`, value `+0x98`, delta `+0x9C` — is advanced by the same tick and
**no authored-command class here writes it**.

```
set(id, steps, target):                      # 003B69B0, 003B6950; the pairs take two targets
    rec = table + (id & 0xFF) * 0xE0
    if rec[0x10] != id:      return          # wrong or unallocated slot: NOTHING is written
    if steps == 0:
        rec.value   = target
        rec.counter = 0                      # immediate, not "256 steps"
        return
    rec.counter = steps                      # a BYTE: 1..255
    rec.delta   = (target - rec.value) * (1.0f / steps)   # reciprocal first (003B69E8), then multiply (003B69EC) - 2026-09-25, OPUS block 321
```

**`steps` is a byte and `0` means immediate.** The delta is computed once, from the value the
channel holds **at the moment of the call** — so re-setting a ramp mid-flight re-bases from wherever
it has reached, which is correct, and is also the only thing that keeps it from drifting.

## 3. Advancing

`003B5890`, once per tick, over the whole table:

```
for rec in table[0 .. 159]:                  # rdx = 0xA0
    if not (rec[0x40] & 1):        continue  # slot not enabled
    if (rec[0x41] | globalGate) & 1: continue # per-slot pause OR the global gate at [02B40524]
    for ch in (0x00, 0x02, 0x01, 0x03, 0x43):
        if rec.counter[ch] != 0:
            rec.value[ch] += rec.delta[ch]   # both components, for the two pair channels
            rec.counter[ch] -= 1
```

**The channels are advanced in the order `0, 2, 1, 3, 0x43`** — the two pair channels first. Nothing
depends on that order here, and it is recorded because a reimplementation that reorders it is only
safe while that stays true.

## 4. The properties a reimplementation must preserve

1. **The identity guard writes nothing.** `rec[0x10] != id` returns before any store — not a
   clamp, not a default.
2. **`steps == 0` is immediate**, and it also clears the counter, so an in-flight ramp on that
   channel is cancelled rather than blended.
3. **The value is never clamped to the target.** Landing on it depends entirely on the counter
   reaching zero after exactly `steps` additions. `value + steps * ((target - value) * (1 / steps))` in
   float arithmetic is **not exactly `target`**, so the final value is within rounding of the
   target and not equal to it.
4. **A paused slot does not accumulate.** The counter is only decremented on ticks that pass both
   gates, so pausing lengthens a ramp in wall time rather than skipping it.
   *Scope, 2026-09-25 (FABLE, Claude Opus 5.5), on OPUS block 301:* this holds on the **frame-tick route** (`003B5890`)
   only. The direct route `003B5C00(handle)` tests neither the per-slot pause `+0x41` nor the global gate (§5). A paused
   slot stepped through it **does** accumulate, which is how a fast-forwarded presentation entry advances a paused ramp.
5. **Counters are bytes.** 255 steps is the ceiling and there is no saturation check in the setter.

## 5. What is not established

- [x] **UQ-191.** **What any channel controls on screen.** Two pairs and three singles, all floats, all
      unnamed. ~~**The record's other 0x60 bytes are unread.**~~ *(answered: see §14 item 5, mostly mapped 2026-09-20; 2026-10-02, OPUS)*
      *Narrowed 2026-09-14 (FABLE, UG-1):* **the table is the character shadow-object pool.** It has the same pointer
      `02B40528`, 160 × `0xE0`, allocator `003B56D0` and free `003B6000` that
      [the character render record array](Character-Render-Records/the-character-render-record-array.md) §13 and
      [the render record pool lifecycle](CONTRACT-render-record-pool-lifecycle.md) step 7 identify as the object behind a render
      record's `+0x114` shadow handle. So every channel is a tween on one character's shadow. Which shadow property each
      channel drives ~~stays open, because the shadow draw that consumes the floats is unread on both pages~~ *(answered: see the consumer read just below and §14 item 1, resolved 2026-09-20; 2026-10-02, OPUS)*.
      *Consumer read 2026-09-20 (SWE2-CONTRACT):* the draw **is** read — `003B62D0` whole (EXP-108 executed
      it natively and measured the same arithmetic). What each channel feeds, structurally:

      | channel | value field(s) | consumed as |
      |---|---|---|
      | 0 (`0x0D`) | `+0x50`, `+0x54` | the rotated 2D offset added to the bone-blended anchor → `out+0x50`/`+0x58` |
      | 2 (`0x0F`) | `+0x58`, `+0x5C` | multiplies the descriptor extents (`rsi+0x18`/`+0x1C` × `+0x08` × `+0x44`) → `out+0x34`/`+0x38` — the quad's X/Y scale |
      | 1 (`0x0E`) | `+0x70` | added to the actor's heading `actor+0x124` with `+0xBC` → `out+0x24` — the shadow's own rotation |
      | 3 (`0x10`) | `+0x78` | multiplies the `+0x0C` × `rsi+0x0C` × `+0x2C` × 0.25 product → `out+0x28` — a gain term (opacity/strength is the best-fit reading; the out field itself is still unnamed) |
      | `+0x43` | `+0x98` | eased through LUT row 5 (`0046FAE0(1, 2, x)`, 60 entries at `01F20E60`), then blends all four channel values toward the `+0x80`–`+0x94` snapshot set AND blends the anchor between the two bones `+0x3C`/`+0x3E` — **this is the consumer of UG-3's cross-fade weight** |

      The anchor itself: `00421FF0(actor, bone)` resolves the two model bones on the character's skeleton
      (`actor+0x18` → `0020E600` → `+0xD98` → `002ED570` → `00370F60`); `+0x38`/`+0x3A` pick whether the
      anchor lerps or snaps; the rotated `(ch0.x + +0x18, ch0.y)` term is added on top using the
      `01F004E0` sin LUT keyed by `actor+0x124`. `+0x40` bit `0x20` forces the morph complete (values
      used directly, `f = 1`); bit `0x40` selects where `out+0x54` comes from (`r14+0x34` vs the
      `00264670` kind-3 read). The blended results are also written back into `+0xC0`–`+0xD4` — the
      cache `003B5D40` snapshots when it starts a new cross-fade, closing the loop.
      ***ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: in the PC build the channels control nothing visible.** Their one consumer, the shadow draw `003B62D0`, has one caller, `003B6020`, which copies the draw's output record into the PS2 command ring (`02EBEFC0`) and submits it through `003A1DB0`. The submit's publisher `0036F360` reads only the ring's last DMA tag and leaves offset, count and `0x100` in the one cell `02EBA3F8`, and no function that references the ring reads it back. The mapping above is therefore what the channels meant to the PS2 blob shadow; `out+0x28` is a component of a VU data vector in a packet no PC code consumes. [Record and control](../_index/candidates/uq191-shadow-channels-pc/README.md) (5 checks, FAILS 0).*
- [x] **Who drives the gate at `[02B40524]`.** The dword *before* the table pointer — this page
      previously named it `[02B4052C]`, which is the pointer's own high dword. Bit 0 is OR-ed into
      every slot's pause test here; bit 1 is read at `003B620E` inside `003B6020`; `003B6930` is
      its setter (`gate = (gate & (arg >> 2)) | (arg & 3)`); and every allocator call clears it.
      **What calls `003B6930`, and what `003B6020` does with bit 1, are open.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (UG-2):* **bit 1 is a global "hide every
      shadow" switch, and bit 0 is never set.**
      - `003B6930` has exactly five direct calls and no other reference (no RIP-relative operand, qword or RVA32 anywhere in
        the image names it). Every call passes **4** or **6**. Through `gate = (gate & (arg >> 2)) | (arg & 3)`, 4 clears
        bit 1 and 6 sets it, and both keep bit 0. The only other writer is the allocator's reset to 0 (`003B6890`). **So
        bit 0, the "suppress every ramp" test in §3, is 0 for the life of the process.**
      - Each call is paired with `003AFD30`, which stores 1 with arg 4 and 0 with arg 6 into `02B3F554` — `+4` of the V2
        pool's 32-byte header `02B3F550`–`02B3F56F`, beside the 32-slot `0x70`-stride table `02B3F570` (the other shadow
        pool on the record page; EXP-113's V2 pool). The paired sites pass 1/0, but `003B8670`'s site at `003B9708`
        passes `r12d` — a mode value, not only a bool. `02B3F554` has **no reader in any static form** — operand scan,
        qword scan, imm64 materialization, `lea`-of-header and all nine table walkers all negative (§14 row 2, censused
        2026-09-20); the V1 gate's consumer (`003B6020`'s bit-1 test) has no V2 counterpart in `.text`.
      - The drivers: the presentation reset `0024D9C0` (on, `0024DA2A`–`0024DA33`; reached from the area unload `002628B0`,
        see [the world tick](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)); `003B8670`, on at
        `003B9705`–`003B9712` and off at `003B9752`–`003B975E`; and `00520800`, on or off by byte `+3` of its record when
        byte `+2` is `0xFF` (`00520806`–`00520840`). ~~reached from `003601D0`, `00360710` and `00360A50`~~ *(corrected
        2026-09-14 after `AUDITSEM-CONTRA-FABLE-UG2-CALLERS`: those three, with `002628B0`, are the callers of `0024D9C0`.)*
        `00520800` has **no direct caller** (raw call index). Its primary reach is the presentation-command
        dispatch: `CharacterRenderSystem_Initialize` registers it as **command id `0x34`** in handler bank
        `02CA4410` (`00426B5C`–`00426B66`), and the stream drains invoke it through invoker-table entry
        `01EFFAF0[0x34]` = `004177B0` — see the render-event page's handler-array section. Its address is also
        stored as a 32-bit value at `01CC74B4` and `01CC78B4` in `.rdata` (byte scan of the image) — a second,
        not-yet-decoded `{u32,u32}` record table, not the dispatch itself. The auditor also listed
        `01FC3E8C` in `.data`, but that address is past `.data`'s raw extent (`01F7E400`), so no static value can be stored
        there, and a byte scan finds only the two `.rdata` entries plus an unrelated `.pdata` word.
      - **What bit 1 does:** in `003B6020` (called from `00521440`), a slot whose own `+0x41` or the global gate has bit 1 set
        is skipped before `003B62D0` builds its output (`003B620A`–`003B6224`; `003B62D0` interior read 2026-09-17, SWE2-FRONTIER: 1,301 B — `00421FF0` ×2 first at [`003B634F`](../_index/ADDRESS-INDEX.md), `0046FAE0`/`003B6BF0`/`00264670`). The advance `003B5890` tests only bit 0,
        so hidden shadows keep ramping.
- [x] **Who drives channel `+0x43`.** No authored-command class in the `00417xxx` family writes it.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (UG-3):* **it is a cross-fade weight,
      started by `003B5D40(handle, n)`,** whose one caller is `0041D560` (`0041D5E7`). It copies the six floats at
      `+0xC0`–`+0xD4` into `+0x80`–`+0x94` (a snapshot), sets counter `+0x43 = n`, value `+0x98 = 0.0` and delta
      `+0x9C = 1.0 / n` (computed through the VU0 register cells `022D914C` / `022D9148`), and applies the first step at
      once (`003B5D5C`–`003B5E0B`). The weight therefore runs from 0 toward 1 across `n` steps away from the snapshot.
      The reset `003B67F0` (one caller, `003723B0`) and the allocator `003B56D0` zero it. ~~What consumes the weight is~~
      ~~unread, as UG-1 is.~~ *(answered: see the `+0x43` / `+0x98` row of UQ-191's consumer table above - `003B62D0` eases it through LUT row 5 and blends toward the snapshot, consumer read 2026-09-20; 2026-10-02, OPUS)*
- [x] **`rec[0x10]`** — compared against the command's id byte, so it is the slot's own id, but
      **what allocates a slot and assigns it is not read here.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (UG-4):* `003B56D0(renderRecordIndex)`
      takes the first slot whose enable bit is clear. It stores `rec[0x10] = generation << 8 | slot` from the counter
      `02B40520` (incremented per allocation, wrapping past `0xFFFFFF` to 1) and returns that handle
      (`003B5719`–`003B5756`). It also records the render record index at `+0x04` and the two model bones at `+0x3C` /
      `+0x3E`. The render record keeps the handle at `+0x114` from promotion until `003B6000` frees it
      ([the render record pool lifecycle](CONTRACT-render-record-pool-lifecycle.md) step 7). **So the guard in §2 is a
      generation check:** the low byte picks the slot, and the upper 24 bits reject a handle from an earlier occupant.
- [x] Whether the advance is once per rendered frame or once per some other tick. **`003B5890`'s
      callers were not followed.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (UG-5): **not once per rendered frame. It is
      once per character-update pass, and a presented frame can hold two.*** Static only.
      - **The only route in** (raw call index): `003B5890` ← `00426090` (`00426112`) ← `RenderSystem_RunCharacterUpdatePipeline`
        `003323D0` ← two frame-mode bodies ([what happens between two frames](../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md)):
        - the field frame, mode 2 `0022A770`, once, when `00358290()` is non-zero (`0022AC03`–`0022AC07`);
        - the full menu, mode 3 `0022B8C0`, at two sites: `0022BA70` when `00181DD0()` is non-zero, and `0022BBCF` in the
          "CLOSE FULLMENU" branch taken when `002E05C0()` returns 0 (`0022BB62`–`0022BB69`). The first site falls through to
          the test for the second, so **a closing full-menu pass can advance every ramp twice.**
      - **The step ignores time.** Each call subtracts 1 from a byte counter and adds a stored increment (§3). No frame delta
        is read, so a ramp's wall-clock length is its step count times the rate of these calls.
      - **A second stepping route, found the same day by following the channel-`+0x43` writers (correcting "the only
        route" above, which holds for `003B5890` only):** `003B5C00(handle)` applies the same five-channel step to one
        slot. It checks only the handle match and the enable bit, and tests neither the per-slot pause `+0x41` nor the global
        gate. It is called from `0041C850` (`0041C8E6`) and `PresentationEntry_RebuildAndFastForwardToTime` `0041D820`
        (`0041D9C6`). **A fast-forwarded presentation entry steps its ramp outside the frame tick,** and a paused slot
        still advances on that route.
      - **One animate call can run the frame dispatch twice.** The frame step `0017D6E0` calls the dispatch
        `0022A490`. On its first pass it may raise a repeat request (`001E0550`, when `001E05F0()` holds: a comparison of
        the accumulator `01F82D28` against `001E04F0`'s value, enabled by byte `01E02801`). The byte is 1 at load and toggled by `001D1660` (`sete` at `001D47F1`); the accumulator is written by `001E03F0` (`001E04B4`, `001E04CB`) and `001E05F0` (`001E0610`). The dispatcher latches the
        request (`001E0560` at `0022A705`: `01F82D30 |= 01F82D31`), and seven sites can clear it first (`001E0580`, e.g.
        `0022A6C1`). If it is still latched after the pass, `0017D6E0` resets (`001E0590`), zeroes the delta
        (`0017D850` `xorps xmm7, xmm7`) and dispatches again (`0017D853`). The request is not re-raised on the second pass
        (`0017D731` `cmp ebx, 1`), so there are at most two passes. Because the ramp step ignores the delta, **a ramp
        advances on both.**
      - **Not established:** ~~what `00358290`, `00181DD0` and `002E05C0` test (they gate the call, not the step);~~ *(answered: see §14 item 3, all three read 2026-09-20; 2026-10-02, OPUS)* what the
        accumulator comparison measures (a frame-time catch-up is the obvious reading and is not asserted); how often the
        repeat fires in play. The last is a live question.

## 6. Relationships

**Callers of the advance.** `003B5890` has one route in: `00426090` (`00426112`) ←
`RenderSystem_RunCharacterUpdatePipeline` `003323D0`, called by the field frame `0022A770` once and
by the full-menu frame `0022B8C0` at two sites — a closing menu pass can advance every ramp twice
(§5, UG-5). A second stepping route runs outside the tick entirely: `003B5C00(handle)` applies the
same five-channel step to one slot, called by `0041C850` (`0041C8E6`) and
`PresentationEntry_RebuildAndFastForwardToTime` `0041D820` (`0041D9C6`).

**The four setters are authored-command handlers** — classes `0x0D`/`0x0E`/`0x0F`/`0x10` of the
`00417xxx` dispatch family reach `003B6A90`/`003B69B0`/`003B6A10`/`003B6950`; the two missing from
the census are the two reached by tail `jmp`. The fifth channel's writer is `003B5D40(handle, n)`,
reached from `0041D560` (`0041D5E7`); `003B67F0` resets it from `003723B0`.

**The two pair-class callbacks, by address (added 2026-09-19, FABLE; both read whole).** Class `0x0D` is `004173D0`
and class `0x0F` is `00417460`, 110 bytes each and identical but for the setter they call. Each takes the **shadow
handle from the presentation entry's `+0x35C`** - when that is -1 the character has no shadow slot and the command
does nothing - the step count from command byte `+2`, and the two targets from the command's floats at `+4` and
`+8`, which it packs as `(a, b, 0, 1)` for the setter. The setters `003B6A90` / `003B6A10` (117 / 119 B, read whole)
first check the slot still belongs to that handle (`slot +0x10`); with a step count of 0 they **snap** the pair and
clear the countdown, otherwise they store the count and a per-step delta `(target - current) * (1 / steps)` — the reciprocal is taken first (`003B69E8`), then multiplied (`003B69EC`); corrected 2026-09-25 (FABLE, Claude Opus 5.5), on OPUS block 321.

**Slot lifetime.** `003B56D0(renderRecordIndex)` takes the first slot whose enable bit is clear and
mints `rec[0x10] = generation << 8 | slot` from the serial counter `02B40520` (wraps to 1 past
`0xFFFFFF`); `003B6000` frees. The render record keeps the handle at `+0x114`
([the render record pool lifecycle](CONTRACT-render-record-pool-lifecycle.md) step 7).

**The gate word `02B40524`.** Written by `003B6930` (`gate = (gate & (arg >> 2)) | (arg & 3)`; all
five call sites pass `4` or `6`, clearing or setting bit 1) and cleared by the allocator. Its
drivers are the presentation reset `0024D9C0` (via the area unload `002628B0`), `003B8670`, and
`00520800` (presentation-command id `0x34`, dispatched via invoker table `01EFFAF0[0x34]` = `004177B0` →
bank `02CA4410[0x34]`; no direct caller — the `.rdata` words `01CC74B4`/`01CC78B4` are a second undecoded
reference). Bit 1
is consumed by `003B6020` at `003B620E` (called from `00521440`); **bit 0 is never set for the life
of the process** — every known writer leaves it clear.

## 7. State transitions

```
slot:      free  (enable +0x40 bit0 clear, rec[0x10] stale)
             -- 003B56D0: first free slot, rec[0x10] := gen<<8|slot, +0x04/+0x3C/+0x3E --> live
live -> free: 003B6000 (render record drops +0x114)
channel:   idle  (counter == 0)
             -- setter, steps > 0 --> ramping  (counter := steps; delta := (target-value)*(1.0f/steps))
             -- setter, steps == 0 --> idle    (value := target; counter := 0 — cancels, not blends)
ramping    -- tick passing both gates, counter decremented to 0 --> idle, value within float rounding of target
ramping    -- +0x41 bit0 set OR gate 02B40524 bit0 set --> suspended (counter held; wall time lengthens)
suspended  -- pause bit cleared --> ramping, resumes mid-count
```

A handle presented to a setter while its slot is free or re-occupied by a later generation fails the
`rec[0x10]` guard and transitions nothing.

## 8. Script · resource · event interactions

The four setters are the write side of **authored presentation commands**: a script command of class
`0x0D`–`0x10` carries ~~`(slot id, steps, target)`~~ `(steps, target)` and no slot id; the callback takes the slot handle from the presentation entry's `+0x35C` *(corrected 2026-10-02, OPUS: `004173D0`+0x13 `mov eax, dword ptr [r8 + 0x35c]`, `004173D0`+0x2E `movzx edx, byte ptr [rcx + 2]`; section 6)* — the two pair classes carry two targets — and
lands through the `00417xxx` dispatch. The fifth channel is event-driven rather than
command-driven: `PresentationEntry_RebuildAndFastForwardToTime` reaches it through `003B5D40` /
`003B5C00`. The gate is driven by presentation events — area unload (`0024D9C0` via `002628B0`),
`003B8670`, and the record-dispatched `00520800`. No archive or save data participates; the records
live in the presentation-owned pool `02B40528`.

## 9. Determinism

- **RNG** — none; no stream is drawn.
- **Timing / ordering** — once per **character-update pass**, not per presented frame: the field
  frame calls it once; a closing full-menu pass can call it twice; the `003B5C00` route steps one
  slot outside the tick. The step reads no frame delta, so wall-clock length is `steps` × call
  rate. All arithmetic is single-precision float in a fixed channel order — deterministic given the
  same set calls.
- **Threading** — not established. The bodies take no lock; which thread runs the character-update
  pass is a scheduler property outside this contract.

## 10. Failure paths and edge conditions

- **Wrong or stale handle** — `rec[0x10] != id` returns before any store: nothing is written and no
  error is raised. The upper 24 bits are a generation check, so a handle minted by a slot's earlier
  occupant is refused silently.
- **`steps == 0`** — the immediate arm: `value := target`, `counter := 0`. An in-flight ramp on that
  channel is cancelled outright.
- **Counter ceiling** — the counter is a byte, 1..255, with no saturation check in the setter.
- **Paused slot** — `+0x41` bit 0 or gate bit 0 skips the decrement: the ramp lengthens in wall
  time rather than skipping steps. Bit 1 of either word is a *hide* consumed by `003B6020`, not a
  pause — hidden shadows keep ramping.
- **Landing** — the value is never clamped to the target: after exactly `steps` additions it is
  within float rounding of it, not equal to it.
- **Allocator re-entry** — `003B6890` runs the alloc sequence only while `[02B40528]` is null; a
  second call on an allocated table does nothing.

## 11. Observable behaviour

Every measurable effect lives in the 160 × `0xE0` record block behind `[02B40528]`: the channel
value/counter/delta fields, the enable bits at `+0x40`, the pause bits at `+0x41`, and the gate word
at `02B40524`. The pool is the character shadow-object pool (§5, UG-1), so each channel tweens one
character's shadow — which property is §14's first row. `diff_ramp_channels.py` compares the record
region and the gate digest-for-digest, which is what makes the untested dimensions below measurable
at all.

## 12. Reproduction formula

```
alloc (003B6890):  if [02B40528] == 0:
                       p = lock(); alloc(0x8C00); unlock()      # 160 records x 0xE0, exactly
                       [02B40528] = p
                       [02B40520] = 0; [02B40524] = 0           # serial counter and gate
                       for i in 0..0x4F:                        # 0x50 passes, two records each
                           rec[2i].+0x40 &= ~1; rec[2i+1].+0x40 &= ~1   # stride 0x1C0

set (003B69B0 / 003B6950; pairs 003B6A10 / 003B6A90 take two targets in xmm2/xmm3):
    rec = [02B40528] + (id & 0xFF) * 0xE0
    if rec[0x10] != id: return                                 # generation guard - writes NOTHING
    if steps == 0: rec.value = target; rec.counter = 0; return
    rec.counter = steps                                        # a byte: 1..255
    rec.delta   = (target - rec.value) * (1.0f / steps)        # reciprocal-multiply, NOT (t-v)/steps

tick (003B5890), once per character-update pass:
    for i in 0..159:                                           # edx = 0xA0
        rec = [02B40528] + i * 0xE0
        if not (rec[0x40] & 1):              continue          # slot not enabled
        if (rec[0x41] | [02B40524]) & 1:     continue          # per-slot pause OR global gate
        for ch in (0x00, 0x02, 0x01, 0x03, 0x43):              # pair channels first, then 0x43
            if rec.counter[ch] != 0:
                rec.value[ch] += rec.delta[ch]                 # both components, for the pairs
                rec.counter[ch] -= 1
```

The reciprocal-multiply is load-bearing, not a stylistic choice: `(target - value) / steps` and
`(target - value) * (1.0f / steps)` differ by one ulp for most non-dyadic operands, and the harness
carries eight discriminating cases that catch a literal-division reconstruction.

## 13. Runtime validation

**Evidence class: isolated original-code execution.** `diff_ramp_channels.py`
(SWE2-CONTRACT, 2026-09-13, `a27b5cc5`) drives all six entry points under Unicorn at their real
virtual addresses and compares the slot block, the gate and every returned value against the
independent MSVC reconstruction: **483 commands, 129 compared lines, 0 mismatches.** Both
census-missing tail-jump setters are driven at `003B69B0` and `003B6950`; the allocator runs both
arms — the null-pointer call emits the real `lock`/`alloc(0x8C00)`/`unlock` extern trace, the
already-allocated call makes none.

| claim | how it was observed live | date | result |
|---|---|---|---|
| all six entries behave as §1–§4 state | Unicorn execution of the shipped bodies vs the reconstruction | 2026-09-13 | 129/129 lines equal |
| the gate cell is `02B40524`, not `02B4052C` | a canary planted at `02B4052C` corrupted the table pointer's high dword before the first comparison — a dead-cell write | 2026-09-13 | corrected in place; OPUS adjudicated `dd620542` |
| the reciprocal-multiply claim discriminates | a literal-division mutant first survived on dyadic operands; eight discriminating float pairs added, mutant now fails by exactly 1 ulp | 2026-09-13 | mutant killed |
| the allocator clears the gate | a gate-clearing mutant fails the two post-ALLOC state hashes | 2026-09-13 | mutant killed |

**Still not executed.** The consumers — `003B6020`'s bit-1 arm and the shadow draw that reads the
floats — are not in this harness *(answered: see the `EXP-108` section below, which runs `003B6020` and `003B62D0` from shipped bytes; 2026-10-02, OPUS)*; `TIMING` in the parity sense (two advances per closing-menu
frame) is read statically in §9, not measured.

## 14. Unresolved

1. ~~**Which shadow property each channel drives** — UG-1 narrowed the pool to the character
   shadow-object pool; the draw that consumes the floats is unread on both pages.~~ **Resolved
   2026-09-20** — `003B62D0` read whole (EXP-108 executed it and measured the same arithmetic);
   the channel map is in §5 under UQ-191: ch0 rotated anchor offset, ch2 quad extents, ch1
   rotation offset, ch3 the `+0x28` gain term, `+0x43` the eased cross-fade weight. Structural
   residue: the `out` record's own field names (`+0x28` opacity vs other gain) and `rsi`'s
   descriptor-field names stay interpretive — the arithmetic is proven, the labels are not.
2. ~~**What `02B3F554` means** — `003AFD30` stores 1/0 beside the 32-slot shadow table `02B3F570`; no
   RIP-relative reader is recorded.~~ **Censused to the boundary 2026-09-20** — it is `+4` of the V2
   pool's 32-byte header: `+0` (`02B3F550`) is the serial counter `003AF340` bumps into
   `serial<<8|slot` generation tickets at slot `+4` (the same scheme as this pool's `rec[0x10]`), and
   `+0x10` (`02B3F560`) is a 16-byte field `003AFD40` fills from a caller's `xmm`. Init `003AFCD0`
   (from `CharacterRenderSystem_Initialize`) sets the flag to 1; the setter's five call sites pass
   **mode values** — 0 at ~~three~~ two sites (`003B8670`+0x10E4, `00520800`+0x36), 1 on `00520800`'s record-`+3`-nonzero path and at the presentation reset `0024D9C0`+0x65 *(corrected 2026-10-02, OPUS: `mov ecx, 1` precedes the call at `0024D9C0`+0x65, `xor ecx, ecx` the calls at `003B8670`+0x10E4 and `00520800`+0x36)*, and `r12d` at
   `003B9708` in `003B8670` — so "1/0" was a simplification. **The reader census is now total and
   negative**: no operand reference in any form (data_xref_scan over all bodies), no imm64
   materialization, no moffs absolute, no `.data`/`.rdata` qword pointer to the address or to either
   writer, no `lea` of the header base `02B3F550` at all, and all nine `lea 02B3F570` walkers —
   `003AF340`/`003AFB30`/`003AFBE0`/`003AFC10`/`003AFC30`/`003AFC80`/`003AFD00`/`003AFD50`/`003AFD80` —
   read slot-positive offsets only. Best-fit reading: the V2 pool's own enable flag, driven in
   lockstep with the V1 hide gate `02B40524` (4→1 shown, 6→0 hidden) — **published but consumed by
   nothing in `.text`**; its consumer is outside static addressing or does not exist. The header's
   `+0x10` xmm field is likewise write-only, which strengthens "published state" over "missed reader".
3. ~~**What `00358290`, `00181DD0` and `002E05C0` test** — they gate the tick's call sites, not the
   step itself.~~ **All three read 2026-09-20:**
   - `00358290` (13 B) returns `(u16[022C7F92] >> 1) & 1` — **aux-mask bit 1 of render-pass enable
     entry 0** (the high `u16` of `022C7F90[0]`; the pass-enable table and its accessor family are
     in [the frame between frames](../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md)
     §512 and [the world tick](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)).
   - `00181DD0` (21 B) returns `byte[lazySingleton + 0x118]` — `001EBA40()` lazily builds a
     `0x2E0`-byte object at `01F82E18` and this getter reads its `+0x118` state byte (already
     EC7-documented in [the field runtime pass](../04-Actor-Entity/the-field-runtime-pass.md));
     the singleton's subsystem is still unnamed.
   - `002E05C0` (23 B) returns **`00253C20() == 0`** — `00253C20` is `(manager[0209BE80]->+0xAA44
     != 0) && (last UI request 02092730 ∈ {0, 3})` via thunk `0035D050`→`00290410`, so the gate
     passes when the singleton's `+0xAA44` flag dword is **clear** or the last posted UI request
     was **not** 0 or 3. `02092730` is the last posted UI request id
     ([the world tick](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md));
     `0209BE80` is the manager singleton tainted through 136 bodies in
     [the per-frame update gate](../00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md).
   ~~Residual: the `+0x118` byte's meaning and `+0xAA44`'s flag semantics stay open — the gates are
   named, the flag values are not.~~ **Both named 2026-09-20:** `+0x118` is the **handbook monster
   viewer's model-open flag** — `001EB9C0` sets it after the staged loader accepts the request
   (handle kept at `+0x130`, keyed by `001C6320()` at `+0x120`), and `001EB940`/`001EB7B0` clear it
   while closing the slot through `002EEB20` — the singleton `01F82E18` is the viewer object itself
   ([the handbook's monster viewer](../16-UI/Handbook/the-handbooks-monster-viewer.md); verified by
   re-reading the ctor `001EB190`, all three writer methods and the five `+0x118` readers — so
   `00181DD0`'s gate fires the full-menu call only while a viewer model is open). `+0xAA44` is
   `ManagerSub0209BE80_A0D0 + 0x974` — the `initDwordAA44` **ready dword of the `003F80D0` group**
   (per-frame group `0x0040`): written `1` by the construction battery at `0028F911` and again by
   `0035C560`'s `00290430(1)`, read only by `00290410` (the `0035D050` thunk `00253C20` reaches it
   through). No static write ever stores 0 — the field is a one-way "the `003F80D0` subsystem is
   up" marker, 0 only until the battery runs.
4. **How often the repeat-dispatch fires in play** — the latch mechanism is read (§5, UG-5); its
   frequency is a live question, not measurable statically.
5. ~~**The record's remaining ~`0x60` bytes** — unread beyond the channel fields and the `+0x3C`/`+0x3E`
   bone indices.~~ **Mostly mapped 2026-09-20:** `+0x30`/`+0x34` are the saved UV-offset snapshot
   (`003B5CE0` copies `+0x48`/`+0x4C` there before writing new ones — its reader is unfound);
   `+0x38`/`+0x3A` are the current/previous blend selectors (`003B5CE0` shifts `+0x38`→`+0x3A`);
   `+0x44`/`+0x48`/`+0x4C` are UV scale/offset (setters `003B6BD0`, `003B5CE0`); `+0x80`–`+0x94`
   is the cross-fade B-set; `+0xA0`–`+0xB8` is a `+0x40`-flag-mode snapshot buffer (`003B5E20`);
   `+0xBC` is an extra rotation offset (setter `003B6B60`); `+0xC0`–`+0xD4` is `003B62D0`'s
   computed-state cache; `+0x08`/`+0x0C`/`+0x14`/`+0x18`/`+0x20`–`+0x28`/`+0x2C` are the
   scalar/vec3 fields `003B62D0` multiplies into the out record (leaf setters `003B6B10`,
   `003B6B30`, `003B6B80`, `003B6BB0`). **`+0x30`/`+0x34` reader censused to the boundary
   2026-09-20 — there is none.** Every accessor resolves the record itself from
   `[02B40528]` via the `(cl=slot, ecx=serial)` + `imul 0xE0` pattern, so the 21-body
   census is total with no rec-by-pointer escape: `003B62D0` reads the *current*
   `+0x48`/`+0x4C` and the selector fields `+0x38`/`+0x3A`/`+0x3C`/`+0x3E` but never the
   saved snapshot; `003B5D40`, `003B5E20`, the six leaf setters, `003B6900`/`003B6930`,
   `003B56D0`, `003B6000`, `003B5890`, `003B6890`, `003B69B0`/`003B6950` and `003B8670`
   touch no `+0x30`/`+0x34` either~~. One writer (`003B5CE0`)~~, except the allocator `003B56D0`, which zeroes the pair *(corrected 2026-10-02, OPUS: `003B56D0`+0x17C `mov qword ptr [rbx + 0x30], rsi`)*. One value writer (`003B5CE0`), zero readers — a
   published-but-unread snapshot, the same evidence class as the V2 mode dword
   `02B3F554` (item 2). **`+0x1C` and `+0xD8`–`+0xDF` closed the same day:** `+0x1C` is
   allocator-zeroed — `003B56D0`'s `mov qword [rbx+0x1c], rsi` is the compiler merging
   the `+0x20` vec3.x zero-init with an adjacent dead store — and no body reads it or
   writes it non-zero, so it is an unused dword between `+0x18` and the `+0x20` vec3.
   `+0xD8`–`+0xDF` is touched by *nothing*, not even the allocator (whose init sweep
   ends at ~~`+0x9C`~~ `+0xD4`: it also writes `+0xBC`..`+0xD4` *(corrected 2026-10-02, OPUS: `003B56D0`+0x180 through `003B56D0`+0x1A7 `mov dword ptr [rbx + 0xd4], 0x3f800000`)*; the highest written field anywhere is `003B62D0`'s `+0xD4` cache
   float): 8 genuine tail bytes of the `0xE0` slot — source padding or a reserved tail
   member no code path explains.

## 15. Evidence

> **Numbered 15 on purpose.** `parity_status.py` reads a contract's claim list from a heading that
> literally begins `## 15.`, and REFUSES a harness whose `CONTRACT_MAP` has drifted from it. This
> section was `## 6.` until 2026-09-13, so `diff_ramp_channels.py` could not be cross-checked against
> it at all — the tool found no claims and reported every harness entry as unmatched. The claim
> column below is now **the harness's own wording**, because a cross-check between two differently
> worded lists is not a cross-check.

| claim | evidence | tier |
|---|---|---|
| 160 records of 0xE0 behind a lazily allocated pointer at 02B40528 | `003B6890`: `0x8C00` allocation, `0x50` iterations clearing two records at `0x1C0` stride; and `003B5890`'s `mov edx, 0xa0` | 1 |
| set(id, steps, target) writes NOTHING when rec[0x10] != id | full disassembly of `003B69B0` and `003B6950` | 1 |
| steps == 0 sets the value immediately and clears the counter, cancelling an in-flight ramp | full disassembly of `003B69B0` and `003B6950` | 1 |
| otherwise counter := steps and delta := (target - value) × (1 / steps) — reciprocal-multiply, corrected 2026-09-25 | full disassembly of `003B69B0` and `003B6950` | 1 |
| the tick advances every enabled, unpaused slot's five channels by value += delta with counter -= 1, in channel order 0, 2, 1, 3, 0x43 | full disassembly of `003B5890`, including its two gates | 1 |
| the fifth channel (+0x43 counter, +0x98 value, +0x9C delta) is advanced by the same tick and no authored-command class here writes it | advanced at `003B5948`-`003B5965`; no `00417xxx` callback writes `+0x98` | 2 |
| the allocator's lock/alloc(0x8C00)/unlock sequence runs only while the pointer is null, then zeroes the two dwords at 02B40520/24 and sweeps the enable bits | `003B6890` | 1 |
| the three tick-call-site gates' predicates | all three read whole 2026-09-20 — `00358290` = aux-mask bit 1 of pass-enable entry 0 (`022C7F92`); `00181DD0` = `byte[lazy 0x2E0 singleton + 0x118]` via `001EBA40`; `002E05C0` = `00253C20()==0` where `00253C20` is `(manager[0209BE80]+0xAA44 != 0) && (last UI request 02092730 ∈ {0,3})`; flag semantics named the same day — `+0x118` = the monster viewer's model-open flag (`001EB9C0` sets on loader accept, `001EB940`/`001EB7B0` clear via `002EEB20` close; ctor, writers and five readers re-read), `+0xAA44` = `ManagerSub0209BE80_A0D0+0x974` `initDwordAA44`, the `003F80D0` group's one-way ready dword (written only 1 at `0028F911` and `0035C560`→`00290430(1)`; read only by `00290410`; no static 0 write) | 1 |
| the five channels feed `003B62D0` as: ch0 (+0x50/0x54) a heading-rotated 2D offset added to the bone-blended anchor (out+0x50/0x58); ch2 (+0x58/0x5C) the quad extents (out+0x34/0x38); ch1 (+0x70) a rotation offset on the actor heading (out+0x24); ch3 (+0x78) a factor of the out+0x28 product; and +0x43 (+0x98) an eased cross-fade weight (LUT row 5 via 0046FAE0) blending all four toward the +0x80–0x94 snapshot and the anchor between bones +0x3C/+0x3E | full disassembly of `003B62D0` 2026-09-20; same arithmetic measured natively by EXP-108 | 1 |
| every record byte has a censused accessor or a named disposition | accessor census 2026-09-20: all 21 `02B40528`-referencing bodies read; `+0x30`/`+0x34` (saved UV offset) and `+0x3A` (previous blend selector) written by `003B5CE0`, `+0xA0`–`+0xB8` snapshot buffer by `003B5E20`, `+0xBC` by `003B6B60`, `+0x44` by `003B6BD0`; `+0x30`/`+0x34` reader census closed same day — every accessor resolves the pool itself via `(cl=slot, ecx=serial)` + `imul 0xE0`, no rec-by-pointer escape; `003B62D0` reads `+0x48`/`+0x4C`/`+0x38`/`+0x3A`/`+0x3C`/`+0x3E` and no other body touches `+0x30`/`+0x34`: one writer, zero readers, a published-but-unread snapshot; `+0x1C` allocator-zeroed and never read nor written non-zero (an unused dword whose zero-store the compiler merged with `+0x20`'s), `+0xD8`–`+0xDF` touched by nothing including the allocator — 8 tail bytes of the `0xE0` slot | 2 |
| the V2 pool's gate cell `02B3F554` is a written mode dword with no reader in any static form | total census 2026-09-20 — operand scan (2 writers only: `003AFCD0` init-1 from `CharacterRenderSystem_Initialize`, `003AFD30` setter at five sites passing 0/1/`r12d`), qword scan, imm64 materialization, moffs, `lea`-of-`02B3F550` and all nine `lea 02B3F570` walkers all negative; header `+0x10` xmm field likewise write-only | 1 |
| **what any channel controls, what the gate is, who assigns rec[0x10], and whether the tick is per-frame** | **established 2026-09-14/20** — channels: the `003B62D0` consumer map (row above); gate: enable `+0x40` bit 0, pause `+0x41|02B40524` bit 0, hide same bit 1 (UG-2); rec[0x10]: `003B56D0` generation ticket (UG-4); tick cadence: per character-update pass, up to twice a frame (UG-5) | none |

## 16. Related

- [`../99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md`](../99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md) — where the two missing setters were found
- [`README.md`](README.md) — the presentation category

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT and SERVICE, 47 edges.**
  - Cited ramp functions are called by `MainLoop_UpdateAndRenderFrame` (7) and core bodies of 2,001 bytes (4), 404 bytes (4), 465 bytes (4) and 463 bytes (3).
  - They call core helpers of 9 bytes (4), 17 bytes (2) and 277 bytes (2), and bodies of 79 and 96 bytes.

- **Resource — MECHANICAL (SWE2-EC7-170, 24 edges).** `003E4890`'s resolve leg
  names `0020E600` (the image-address codec `002ED570`/`00409D60`/`0051FE30`/
  `0051FF30` also consume on the Resource layer), `003E6DA0` (itself calling
  `002ED570`) and `004256E0` (`00409600`/`00409F50`) — Resource-layer fan-in on
  the codec and the lookup, no resource relationship to the ramp contract.
  Edge list from `edges.tsv` 2026-09-22.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT (36 edges through 19 of this page's functions).** The ActorEntity layer reaches this page at `002628B0`, `00263560`, `00265200`, `003B8670` and 15 more. `FUN_002628b0` is the worked example, read in full - it is a 1,689-byte manager routine that indexes `02098E10` at the **`0x288` stride** - the same records the manager indexer walks - in a `0x50`-byte frame with a stack cookie; **5 of the 24 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Developer — SERVICE.** `0017D6E0` on this page calls `FUN_001c2f50`, owned by that layer. What it reaches is a string-assembling routine over the EASTL allocator at `008F6600`, the globals at `01F8127C` / `01DF6E38` / `01DF6E40` and the static empty buffer `02EBA2E0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — SERVICE.** `002628B0` on this page calls `PartyFocus_ClearCurrentActorIfEligible`, owned by that layer. What it reaches is a 103-byte guard that needs `002671F0(0)` and a non-zero packed handle at `[022C7FE0]` before clearing through `003588B0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Platform — SERVICE.** `001E03F0` on this page calls `FUN_005cc930`, owned by that layer. What it reaches is a high-resolution counter read: it calls the import at `008C2188` and converts the unsigned 64-bit result to double with the `2^64` fixup at `00D27A68`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — SERVICE.** `0022A770` on this page calls `FUN_00316930`, owned by that layer. What it reaches is a 287-byte walk of the same `[022C2550]` table against the data at `01EED130`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — MECHANICAL (SWE2-CONTRACT 2026-09-15, 24 edges).** Every edge is the frame tick, not the
ramp machinery: `003601D0` (the frame-advance body this contract's table feeds) calls ten
`00360xxx`/`002DFxxx`/`00363xxx` Audio fade-and-mix helpers, `002628B0` calls `00360B50`/`00360DD0`/
`003636A0`, `001D1660` calls `001DBB00`/`002DEBA0`, `003B8670` calls `002DF660`/`003B3EA0`, and the
five `003D7Cxx`/`00332C40` callers reach `00181DD0`. Audio fades are ticked by the same frame bodies
that advance the authored-command channels — shared cadence, no audio ownership crossing.

**Input — MECHANICAL (SWE2-CONTRACT 2026-09-15, 20 edges).** The same frame tick:
`0022A770`/`0022B8C0` (the per-frame bodies the harness exercises) call the input-rebuild family —
`InputGameplay_RebuildFrameSnapshotFromChannelHistory`, `InputControl_SetOneShotFrameCallback`,
`InputGameplay_RebuildRemappedTransitionMaskState`, the `0035AExx`/`0035FF90`/`0017DE60` helpers and
the remapped-history-mask getters — 19 of 20 edges through those two bodies, plus `0035B5D0` via
`002628B0`. Input history is rebuilt on the same cadence the channels advance on; no input-side
relationship to the ramp semantics.

**Movement — MECHANICAL (SWE2-CONTRACT 2026-09-15, 16 edges).** The same frame tick: `003B8670` calls five
`0024Bxxx`/`00265200`/`0026AF80` movement helpers (5 edges), `002628B0` calls `00379070`/`003791C0`/
`0026A1D0`/`003DAA20`/`003792D0` (5), `0022B8C0` calls `00263560`/`0037CF00` (2) and shares
`00263560` with `002628B0`, `003B62D0` calls `00264670`. The ramp channel bodies run on the frame
that also steps movement — cadence adjacency, no locomotion semantics in the ramp contract.


### Interior citation — frontier hub `0046FAE0` (2026-09-18, SWE2-EC7)

`0046FAE0` — 84 B, 8 callers: the ramp-table index the channels share.
`(edx*3 + r8d)` composes a channel key, `× 0x1E0` strides the `01F20E60` row
block, and `int(xmm0 * (01F20A98 - 1))` clamped `[0, count-1]` selects the
float at `[row + idx*4]` — [`0046FB2E`](../_index/ADDRESS-INDEX.md). The
normalised-position lookup feeding the ramp evaluators.

**CombatAI — MECHANICAL (SWE2-EC7-34, 1 edge).** `003E7DE0` — the shared authored-command callee this page cites inside the `00332C40` handler — is called by `00308610` on the CombatAI layer. Shared-helper fan-in; no CombatAI relationship to the ramp channels.

**Gameplay — MECHANICAL (SWE2-EC7-34, 1 edge).** `00308610` — the CombatAI caller above — also reaches one callee on the Gameplay layer. Same shared-helper fan-in one hop further out; no gameplay relationship to the ramp channels.


## The consumer pass executed — [`EXP-108`](../_experiments/EXP-108-ramp-channel-consumers-exec.md), folded in 2026-09-19 (OPUS)

`EXP-108` ran the 160-slot draw pass `003B6020` (677 B) and the `0xA0` record builder `003B62D0`
(1,301 B) from shipped bytes, with the swap, ring terminator, LUT lookup and resolvers real.
**Isolated original-machine-code execution — it establishes what these bodies compute, not which
slots the game fills.**

### The slot gate is three tests, and the first is an ENABLE

```
003B6200  test  byte ptr [rbx + 0x40], 1
003B6204  je    0x3b629f                     ; bit 0 CLEAR -> SKIP THE SLOT
003B620A  movzx eax, byte ptr [rbx + 0x41]
003B620E  or    eax, dword ptr [02B40524]    ; the slot's hide byte OR the global gate
003B6214  test  al, 2
003B6216  jne   0x3b629f                     ; bit 1 in EITHER -> hidden
003B621C  mov   ecx, dword ptr [rbx + 0x10]  ; the channel id
003B6224  call  003B62D0                     ; ... build the record
```

**`+0x40` bit 0 is an enable: a slot with it clear is skipped.** That is the opposite polarity to a
"suppress" flag, and it is a *different byte* from the `+0x41` pause bit this contract already
documents — the two are adjacent and easy to conflate.

> **This does not touch the "bit 0 is never set" finding in §3.** That one is about the **global
> gate cell `[02B40524]`**, whose bit 0 is OR-ed into the *pause* test and is never set for the
> life of the process. The enable above is the **slot's own `+0x40`**. Two different objects, and
> both readings stand.

**The hide is an OR across both**: `(b[slot+0x41] | d[02B40524]) & 2`. Bit 1 set in *either* hides
the slot; **the gate's bit 0 alone does not hide anything**, which is consistent with §3.

**The channel id is echo-validated.** The builder recomputes `rslot = slots + u8(ecx) * 0xE0` and
requires `d[rslot+0x10] == ecx`, so **the table is self-describing and a mismatched index
early-outs** rather than reading a neighbouring record. A reconstruction that indexes without the
echo will silently accept a stale id.

### What the pass returns is a leftover, not a status

A disabled slot leaves `eax` untouched; a hidden slot leaves `eax = b41 | gate`. **The pass's
return value is whatever the last such slot left behind** — an all-hidden pass returns `2`. It is
not a count and not an error code, and nothing should be built on it.

### Every produced record costs a buffer swap

`003A1DB0` runs after the head template **and** after each copied record, so successive `0xA0`
records land in **alternating draw buffers and each buffer keeps only its most recent record**.
This is a throughput property a reimplementation cannot ignore: writing all records into one buffer
changes what is drawn.

The ring terminator `0036F360` appends at `r9` when `edx < 0x200` and **overwrites the last entry
otherwise** — a silent truncation at the bound, not an append failure. Its four rip-relative
operands all touch the single cell `02EBA3F8`, which ends at `0x100` every time single-threaded.

### The LUT index is symmetric-clamped, and the count is a dword

```
0046FAF9  imul rdx, rcx, 0x1e0          ; row = (3*edx + r8d) * 0x1E0
0046FB0A  lea  ecx, [r8 - 1]            ; cnt - 1
0046FB19  cvttss2si eax, xmm1           ; (cnt-1) * x, truncated
0046FB1F  cmovs eax, r9d                ; negative -> 0
0046FB23  cmp  eax, ecx
0046FB25  jbe  0046FB2B                 ; above cnt-1 -> cnt-1
```

**The count is the dword at `01F20A98` (= 60), not the byte at `…A97`** — an off-by-one-address
reading that a byte-sized census would reproduce. Clamping is symmetric: `cmovs` at the bottom,
`jbe` at the top, so out-of-range inputs saturate rather than wrap.

### The rest, as measured

- **The blend picks on three slot words.** `w3a == w38` takes a direct object copy (`r14` when
  `w3c == w38` too, else `r15`); `w38 == w3c` with `w3a` apart blends `xmm2*r15 + xmm3*r14`; all
  three distinct blends `xmm2*r14 + xmm3*r15`. **The operands swap between the two blend arms** —
  the single easiest thing to get backwards here.
- **The slot writeback is the PRE-transform row** `+0xC0..+0xD4`, stored interleaved
  (`C0, C4, D0, C8, CC, D4`) and written *before* the `f48`/`f4C` offset-scale, the actor-angle add
  and the `+0x50`/`+0x58` rotation. So the cached row is not the drawn row.
- **The trig index** is `cvttss2si(f124 / 2π × 32768)` with cosine via a `+0x2000` LUT offset, both
  masked `& 0x7FFF`.

*(OPUS 2026-09-19, on `REQ-OPUS-RAMP-CONSUMERS-FINDINGS` from SWE2-ORACLE. The gate sequence, the
echo check and the LUT clamp re-read from the image; the apparent clash between the new `+0x40`
enable and §3's never-set bit 0 is resolved above — they are different objects.)*


## What gates the pass, and the two shadow pools — [`EXP-113`](../_experiments/EXP-113-shadow-sync-stage-exec.md), folded in 2026-09-19 (OPUS)

The consumer pass above does not run on its own. `00428E40` is the stage gate, and **it guards both
the record walk and the ramp pass in one body**:

```
00428E44  mov  rax, qword ptr [022C6F28]        ; the render-system singleton
00428E4B  cmp  byte ptr [rax + 0x48842], 1
00428E52  jne  0x428e6b                          ; -> return, nothing runs
00428E54  cmp  byte ptr [rax + 0x48843], 0
00428E5B  jne  0x428e6b
00428E5D  call 0x426420                          ; the record walk
00428E66  jmp  0x521440                          ; -> tail into 003B6020, the pass
```

**The gate is two bytes and they are tested against different values** — `+0x48842 == 1` *and*
`+0x48843 == 0`. A model that treats it as one enable byte runs the pass in a state the engine
would not. The walk `00426420` re-tests both, because it is reachable independently of the stage
dispatcher.

> The singleton is `022C6F28` — the same pool object whose lifecycle
> [the render-record pool contract](CONTRACT-render-record-pool-lifecycle.md) documents, and whose
> `+0x48830`/`+0x48828` cells are named in its §20. The stage flags live in the same tail block.

### The per-record flag gate is four bits, and all four must be SET

`00426340` admits a record only if every one of these holds — written as four separate branches,
not one mask:

| test | site | meaning |
|---|---|---|
| `test al, 4` / `je` | `00426374` | `+0x284` bit 2 set |
| `cmp word ptr [rbx+6], -1` / `jne` | `0042637C` | the word at `+6` is `-1` |
| `test byte ptr [rbx+0x2AE], 2` / `jne` | `00426387` | `+0x2AE` bit 1 **clear** |
| `test al, al` / `jns` | `00426390` | `+0x284` bit 7 set |
| `test al, 0x40` / `je` | `00426394` | `+0x284` bit 6 set |
| `bt eax, 0xC` / `jae` | `00426398` | `+0x284` **bit 12** set |

So the `+0x284` condition is exactly `(f & 0x10C4) == 0x10C4`. **`EXP-113`'s "four-bit mask" is a
faithful model** — every branch requires its bit set, so the conjunction collapses to that one
comparison — but the two extra conditions at `+0x06` and `+0x2AE` are *not* part of it and are
easy to lose when the mask is written down alone.

### Two shadow pools, addressed differently, with generations in different places

This is the part a reconstruction gets wrong by symmetry:

| | `003B6900` (V1, the `0xE0` pool) | `003AFD00` (V2, the `0x70` pool) |
|---|---|---|
| base | `add r9, qword ptr [02B40528]` — **a pointer load** | `lea r8, [02B3F570]` — **an in-image table** |
| stride | `0xE0` | `0x70` |
| generation | `cmp dword ptr [r9 + 0x10], ecx` | `cmp dword ptr [rax + 4], ecx` |
| on mismatch | early-out | `cmovne rax, 0`, then a null test |

**Both validate `handle = (gen << 8) | slot` before writing, and a stale handle silently no-ops** —
no error, no log. The `0x70` table is the same one `EXP-109`'s handle clear `003AFBE0` indexes, so
the two passes agree on it.

### Verb ordering

`V1(h, 6)` and `V2(h, 0)` are **unconditional** for every synced record that has a handle; the
`V1(h, 4)`, LOD and `V2(h, 1)` updates happen only for records passing the full gate above. And
`b[+0xC0] & 0x18` **skips the mode/LOD update entirely** (`004263A8`), while `b[+0xC0] & 2` selects
the constant `f[+0x27C]` over the computed LOD (`004263BB`). A record can therefore be synced,
handled and still never have its LOD touched.

*(OPUS 2026-09-19, on `REQ-OPUS-SHADOW-SYNC-FINDINGS` from SWE2-ORACLE. All six findings re-read
from the image; the bit-12 test is a `bt`, which is why a byte-wide mask reading would miss it.)*


## The computed LOD and the field sync — [`EXP-114`](../_experiments/EXP-114-shadow-lod-compute-exec.md), folded in 2026-09-19 (OPUS)

`EXP-114` executed the computed-LOD side of the shadow path — the branch the previous section shows
`b[+0xC0] & 2` selects against. Four of its six findings are adopted as measured. **One is
corrected, and the correction changes what a field means.**

### `slot+0xB0` is an ANGLE IN RADIANS, not a fade rate

```
003B5F0F  movzx eax, word ptr [rdx + 0x32]   ; a 16-bit field of the argument
003B5F13  sar   ax, 6                        ; ARITHMETIC right shift - signed, 1/64 units
003B5F17  cwde
003B5F18  movd  xmm0, eax
003B5F1C  cvtdq2ps xmm0, xmm0
003B5F1F  mulss xmm0, dword ptr [00D115B0]   ; SCALAR multiply
003B5F27  movss dword ptr [r9 + 0xb0], xmm0
```

**`00D115B0` holds `0.017453291`, which is π/180.** Not `0x3CC00000`/`0.0234` — the bytes are
`34 FA 8E 3C`, and the four bytes immediately after it are the ASCII `"sabf"`, so **the cell is a
lone dword sitting in front of string data and cannot be a vec4**. Consistently, the instruction is
`mulss` and not `mulps`: a packed multiply there would fold string bytes into lanes 1–3.

> **So the field is an angle.** `arg+0x32` is a **signed 16-bit angle in 1/64 of a degree**;
> `sar 6` recovers whole degrees, `cwde` keeps the sign, and π/180 converts to radians. `slot+0xB0`
> is that angle in radians, and `003B5E82` propagates it to `+0x70` and `+0x90`.
> **`EXP-114` reads the constant as "a per-tick fade rate", which would make `+0xB0` a rate rather
> than an angle — a different field with different units feeding different arithmetic.** The
> `sar`-not-`shl` half of that finding is right and is what exposed the rest.

### `arg+0x54` is a seventh payload dword

```
003B5F4E  mov eax, dword ptr [rdx + 0x54]
003B5F51  mov dword ptr [r9 + 0xac], eax
```

The hand decode had `+0x14`. It is `+0x54`, **distinct from the `+0x4C..+0x5C` group** already
documented, and it lands at `slot+0xAC`.

### The clamp bounds come from the shared `vf00` image

`xmm6 = 1.0` (`003B5AE6`, from `01EF93FC`) and `xmm3 = 0.0` (`003B5B5A`, from `01EF93F0`) — **the
fade ceiling and floor are loaded from memory, not assembled from immediates**, and the memory is
the software `vf00` image that `0036DD80` resets to `[0, 0, 0, 1]` from the `.rdata` constant at
`008C5FD0`.

> **This is the same cell as the point transform's forced `w`.** See
> [`CONTRACT-transform-primitives` §15b](../00-Engine-Core-Runtime/CONTRACT-transform-primitives.md),
> written the same day: one 16-byte global serves as the transform's `w` source *and* as this
> path's clamp bounds. It has three writers and all three store the architectural `[0, 0, 0, 1]`,
> so both readers see the constant they expect — but **a reconstruction that gives each subsystem
> its own private copy has two objects where the engine has one.**

### The rest, as measured

- **The distance is three-component**, `dx² + dy² + dz²` from `G_C[0..2]` — and `G_C[0]` is then
  **overwritten by the result**, so the vector left at `022D8FB0` is
  `[result, dy², dz², total]`. **It is not a clean vec4 and must not be read as one.**
- **`1 / bits2f(edx)` overflows to `+inf` for small `edx`** — the "rate" field is a float
  *reinterpret* of the integer, not an integer divide, so `edx = 5` is `5 × 1.4e-45` and the
  reciprocal saturates into `f[+0x9C]`/`f[+0x98]`.
- **Only lane 0 of the computed vector escapes** — every exit uses `movss` from memory, which zeroes
  bits 32–127, and the tail's `movd`/`movss` pair returns lane 0 alone.

*(OPUS 2026-09-19, on `REQ-OPUS-SHADOW-LOD-FINDINGS` from SWE2-ORACLE. The constant was read out of
the image rather than taken from the finding, which is what exposed π/180 and the string bytes
behind the claimed vec4.)*


## The pass's own tail resolvers — [`EXP-120`](../_experiments/EXP-120-exp108-tail-resolvers-exec.md), folded in 2026-09-19 (OPUS)

The consumer-pass section above left three boundaries scripted. **All three are now closed and all
three were thin** — `002ED570` in `EXP-117`, and `003E56A0` / `00370F60` here, at 24 and 61 bytes.
Together with `EXP-119`'s pair, that is **five "deep subtree" annotations that were overestimates**;
the pattern is worth naming, because it points the wrong way from the usual residual error.

### `003E56A0` takes one argument, not two

```
003E56A0  mov   rdx, qword ptr [rcx + 0x400]   ; the FIRST instruction overwrites rdx
003E56A7  test  rdx, rdx / jne
003E56AC  xor   eax, eax / ret                 ; no table -> 0
003E56AF  movzx eax, word ptr [rdx + 2]
003E56B3  add   eax, edx                       ; + the table pointer's own LOW DWORD
003E56B5  cdqe
```

**Callers pass a second value in `edx` and the body destroys it before reading it.** The function is
`resolve_table_cursor(rec)`, arity one — the traced second argument in `EXP-108` and `EXP-109` is
noise, and a reimplementation should not carry a parameter the engine ignores.

**And the return is a sign-extended 32-bit sum**: `add eax, edx` is 32-bit, `cdqe` fills the high
half. Whenever `low32(table) + offset ≥ 0x80000000` the result is negative. **This is the second
instance of that exact idiom today** — see
[`CONTRACT-render-record-pool-lifecycle` §21](CONTRACT-render-record-pool-lifecycle.md), where arm 3
computes its table pointer the same way. **Both rely on the table living in the low 2 GB, and
neither says so.**

### `00370F60`'s sentinel is 16 bits wide and its index is 64

```
00370F66  movsxd rbx, edx          ; the index, SIGN-EXTENDED to 64 bits
00370F69  mov    eax, 0xffff
00370F6E  cmp    bx, ax            ; ... but only the LOW 16 BITS are tested
00370F71  je     0x370f95          ;     -> return 0
00370F81  imul   rax, rbx, 0x290   ; ... and the FULL rbx indexes
00370F88  sub    rax, -0x80        ;     + 0x80
```

**The guard and the use disagree about width.** `0x0001FFFF` is rejected although it is not `-1`,
and `0xFFFF0000` passes the guard and then indexes **65,536 records backward**. A reimplementation
that writes `if (idx == -1) return 0;` accepts and rejects a different set of inputs than the
engine does.

*(OPUS 2026-09-19, on `REQ-OPUS-EXP108-TAIL-RESOLVERS-FINDINGS` from SWE2-ORACLE. Both bodies read
in full — 24 and 61 bytes, so "in full" is cheap here.)*

## SWE2-EC7-27 update (2026-09-18) — `002DF660` sequence-stamped forward

`002DF660` (30 B) reads `dword[0215EFDC]`, increments and republishes
the counter, then tail-jumps `001DC2E0` passing the pre-increment value
in `ecx` — the sequence stamp the `003B8670` ramp caller attaches to
each forwarded command. Interior anchor `002DF673` (the counter store).

## SWE2-EC7-34 update (2026-09-19) - `00332C40`

`00332C40` (857 B) is an authored command handler - `test byte[rcx+9]&4` gate, `003E7DE0`/`003A1070`/`0046C8D0`/`003616F0`/`002DF150` plus the `00332Exx` internal arms. Interior anchor `00332CC4` (an `003E7DE0` call).

## SWE2-EC7-41 update (2026-09-19) - `003723B0`

`003723B0` (343 B) is a ramp-channel body - `022C6F28`, `0020E600` quadruple/`00409270`/`00409300`/`003B67F0`. Interior anchor `003723BF` (a `0020E600` call).

## SWE2-EC7-47 update (2026-09-19) - `003B5C00`

`003B5C00` (214 B) is a call-free `02B40528`+`0xE0`-stride record updater - `+0x10`==key check, `+0x40` bit-0 gate, decrements byte counters `+0..+3` ~~and folds `+0x60`/`+0x64`/`+0x68`/`+0x6C`/`+0x70`/`+0x74`/`+0x78`/`+0x7C` deltas into the `+0x50`/`+0x54`/`+0x58`/`+0x5C`/`+0x70`/`+0x78` float pairs.~~ and `+0x43`, five channels: counter `+0` folds `+0x60`/`+0x64` into `+0x50`/`+0x54`, `+2` folds `+0x68`/`+0x6C` into `+0x58`/`+0x5C`, `+1` folds `+0x74` into `+0x70`, `+3` folds `+0x7C` into `+0x78`, and `+0x43` folds `+0x9C` into `+0x98` *(corrected 2026-10-02, OPUS: the fifth channel is `003B5C00`+0xB0..+0xCD, `movzx ecx, byte ptr [rax + 0x43]` through `movss dword ptr [rax + 0x98], xmm0`; the five-channel step section 6 states)*. Interior anchor `003B5C03` (the `imul` index).

## SWE2-EC7-51 update (2026-09-19) - `00360B50`

`00360B50` (173 B) is an Audio fade-and-mix helper `002628B0` calls - `002DEC20`/`002DEC70`/`002DEDE0`/`002DEE90`/`003697F0`. Interior anchor `00360B90` (a `002DEC20` call).

## SWE2-EC7-53 update (2026-09-19) - `003B5E20`

`003B5E20` (473 B) is the `+0x40`-flag-mode snapshot buffer the contract names, call-free - `r9 = cl*0xE0 + 02B40528` with `[r9+0x10]==cl` check, per-flag-bit snapshot copies `+0xA0`->`+0x50`/`+0x80`, `+0xB0`->`+0x70`/`+0x90`, `+0xA8`->`+0x58`/`+0x88`. Interior anchor `003B5E5B` (the first snapshot store).


## SWE2-EC7-53 update (2026-09-19) - `00409300`

`00409300` (451 B) is a ramp-channel body - `0046D110`/`0046D380`/`0046D560`/`0046D8E0`/`0046D920`/`00808C40`. Interior anchor `0040941B` (a `0046D560` call).

## SWE2-EC7-54 update (2026-09-19) - `0046D560`

`0046D560` (464 B) is a call-free `01F004E0` table evaluator - `divss` normalize by `01CEBC78`, `00D10820` scale, `cvttss2si` + `&0x7FFF` index, `ecx=0x2000`. Interior anchor `0046D5C7` (the `01F004E0` table read).

## SWE2-EC7-60 update (2026-09-19) - `003B67F0`

`003B67F0` (155 B) is the `003B56D0`-paired reset the ramp contract names - call-free `1.0f` defaults at `+0x58`/`+0x5C`/`+0x78`/`+0x88`/`+0x8C`/`+0x94`/`+0xC8`/`+0xCC`/`+0xD4`. Interior anchor `003B683B` (the `+0x5C` = 1.0f store).


## SWE2-EC7-70 update (2026-09-19) - `00409270` tagged-index decode measured

`00409270` (34 B) is the index decode the ramp-channel and frame bodies
share: `dword[+4] != 2` or `edx >= [+0xC]` returns 0; otherwise it reads
`dword[rcx + edx*4 + 0x40]`, shifts it right `0xC`, and adds the record's
low dword (`movsxd rax, r8d` - the object sits below 4GB, so the low dword
is the address). The `>>12` extracts a packed field offset the `+0x40`
table stores.
Interior anchor `00409287` (the `[rax + rcx*4 + 0x40]` table read).

## SWE2-EC7-84 update (2026-09-20) - `0046E420` slot linker measured

`0046E420` (144 B) is the two-slot link pass the ramp callers run:
`edx` != -1 gates `002ED570(rcx)` + `003713C0(rec)`; the `word[rdi+8]`
slot resolves the same way into `0020E620(sub, sub2)` stored at
`[rdi+0xC]`, and the `word[rdi+0x10]` slot links through
`00372F60(rdi, rbx)` - each `-1` word skips its half.
Interior anchor `0046E472` (the `0020E620` call).

## SWE2-EC7-89 update (2026-09-20) - `003B81A0` + `003B5310` measured

`003B81A0` (179 B) is the request toggle the ramp callers run: a
live `[02B40538]` is torn down first (`003ABCA0()`, slot cleared,
`003ACA90(8)` and `003ACA90(0x10)`); when `ecx` is nonzero it then
builds a 0x50 request (`00861EC0` zero, `0x100FF06` tag, byte
flags, a 1.0f pair from `00900320`), `003AB960` submits it into
`02B40538`, and `003ACA80(8)`/`003ACA80(0x10)` re-arm - under a
stack cookie.
Interior anchor `003B81C4` (the `003ABCA0` call).

`003B5310` (39 B) is the bit-1 setter the ramp callers run: when
`02B40518`'s bit 1 differs from `ecx`, the bit is flipped in
place and the body tails `003B4FD0`.
Interior anchor `003B5322` (the flip sequence).


## SWE2-EC7-90 update (2026-09-20) - `003AFB30` five-channel rate tick measured

`003AFB30` (176 B) is the rate-accumulator tick the ramp callers
run: `ecx` keys the 0x70-stride record in `02B3F570`
(`dword[+4]` must match), and each of the five countdown bytes
at `+0x1C`/`+0x1D`/`+0x1E`/`+0x54`/`+0x55` that is nonzero
decrements while its rate field (`+0x2C`/`+0x30`/`+0x38`/`+0x48`/
`+0x4C`) adds into the paired accumulator (`+0x24`/`+0x28`/
`+0x34`/`+0x3C`/`+0x44`) - five independent rate channels per
record.
Interior anchor `003AFB5B` (the first channel arm).

`0041ADA0` (1535 B) is the channel-step driver `0041C850` calls at `0041C8BF`: `0046D110` frames the scratch, `byte[rsi+8] & 2` and `word[rsi+0x50] != -1` gate, `0046E8B0([rsi+0x60], [rsi+0x68])` resolves the channel record, then `0020E600` x10 over `[rax+0x84]`-family fields and `0041A8E0` x9 per-channel steps with `0041D6F0`, `0041D180`, `0046D380` - the ramp-channel apply behind the fast-forward path.

Interior anchor `0041ADE6` (function `0041ADA0`).

`0041D6F0` (154 B) is the channel-record copy `0041ADA0` and `00418880` share: `0020E600([rcx+0xA0])` resolves twice, `00409270` on `[rbx+0x27E]` then `00409300` - copying `rbx+0xC0` or the stack xmmword into `[rbx+0xF0]` depending on `byte[rbx+0x28B] & 4` - the slot-field update helper.

Interior anchor `0041D715` (function `0041D6F0`).

`0046E8B0` (13 B) is the handle guard `0041ADA0` and `00418880` call: `edx == -1` returns 0, otherwise tail `002ED570` - the invalid-handle short-circuit in front of the resolve.

Interior anchor `0046E8B8` (function `0046E8B0`).

`0041A8E0` (1207 B) is the channel evaluator `0041ADA0` runs: `[rdx+0x34] == 1` takes the early path, `00409150` walks the `0x80000000`-sentinel list, `0041B460`/`0041B3A0`/`0041B920`/`0041BB00`/`00409170`/`0041BA10`/`0041BC40` step the authored channels, and the tail closes with `cvtdq2ps`/`subss`/`divss`/`mulss`/`addss` - the normalized `t` interpolated back into the channel value, returned in `xmm0`.

Interior anchor `0041A91C` (function `0041A8E0`).

`0041B460` (123 B) is the operand decoder `0041A8E0` and `0041A7F0` call per channel step: `[rdx]` below `0x80000000` keeps the operand inline at `rdx+0xC`, otherwise `[rdx+0xC] * 0x1C` indexes the block at `rdx+0x10`; `byte[r8+3]` picks the 8-byte column, `[r9+0x30]` and `word[r8]` build the cursor into the record, `byte[r9] & 0x40` returns zero, a negative `cl` reads the word pair `<<8` against `byte[r8+2]`, and `r10d` is added on the way out - the channel value's fetch half, call-free.

Interior anchor `0041B4A2` (function `0041B460`).

`0041C410` (666 B) is the rebuild dispatcher `002EE3E0`, `00422EB0` and `PresentationEntry_RebuildAndFastForwardToTime` `0041D820` itself call: two `00229EA0` mode reads against `+0x6E0`, flag bits 1/0x17/0x12 at `+0xC`, `003E7D10(3)`, `+0xC0` bit 0x40, the `+0x340` float, mode `02CA83F4` with `+0x284` bit 0x8000000 and `word[+6] == -1`, then `word[+0x24] == 1` opens the arm - `0041CFC0`, `0041D820`, `0041DA90`, `0041DD40`, `004255B0` run the ramp re-emit under the entry's gates.

Interior anchor `0041C564` (function `0041C410`).

`0042F030` (349 B) is the ramp tick `00426090` calls: `02CA48F8` global - `[rbx - 0x1C]` decrements while `[rbx - 0x14] + [rbx - 0x18]` accumulates, `0046FB40` is poked per step, `xmm7` seeded from `00D12470` - the channel ramp's per-frame accumulator.

Interior anchor `0042F09A` (function `0042F030`).

`003AFD00` (44 B) is the low-nibble write `00421280`/`00426340` call: `cl x 0x70` indexes `02B3F570`, `[rax + 4] == ecx` keeps the record (else null), and `byte[rax + 0x20] = (byte & 0xF0) | (dl & 0xF)` splices the ramp nibble - the channel record's flag merge.

Interior anchor `003AFD21` (function `003AFD00`).

`004255B0` (298 B) is the angle-sector classify `0041C410` runs on `[rcx+0x2E0]`'s record: `003E58B0` reads the current value into xmm7, `dword[+0x23C]` is the limit unless `byte[+0x62C] & 1` or `003AEF20(+0x550)` clears it to 0; a `+0x420` bound rejects, else `(+0x244 - +0x124) x 0xB40000`'s wrap normalizes into a 5-bucket range test (`008F3138`/`00902EF0`/`00D12438`/`00D12444` thresholds, sectors 1-5) and the bucket tail-jumps `003E4890` - the ramp channel's quantised heading pick.

Interior anchor `004255F3` (function `004255B0`).

`00418750` (294 B) is the step-down `0041DA90` runs on `r8`'s record: `byte[+8] & 2` and `word[+4] == 1` with `dword[rcx+0xC] & 0x40000` clear admit; `[+0x20] / word[+0x1A]` rates into `+0xC`/`+0x10` (clamped by `00D12310`, bounded by `word[+0x16]`/`word[+0x18]`), `byte[rdx+0x96] & 0x40` forces `+0xC - 1.0`; `word[+0x5E]` counts down and at 0 expires `word[+4] = 2` with `+0x5E = -1`, clearing `+0x96` bits 4/6 - the channel's decrement-and-end leg.

Interior anchor `004187D4` (function `00418750`).

`003E4890` (67 B) is the resolve-and-publish leg `004255B0` tail-jumps into and `004256E0` calls: `003E6DA0(edx)` yields the keyed record (null exits), `dword[+0x14]` is then resolved twice through `0020E600` - once tested for null, once for real - and `0051A920(record2, edi)` consumes the pair - the ramp channel's quantised pick turned into the emitted command.

Interior anchor `003E48AC` (function `003E4890`).

`003E4890` (67 B) is the resolve-and-publish leg `004255B0` tail-jumps into and `004256E0` calls: `003E6DA0(edx)` yields the keyed record (null exits), `dword[+0x14]` is then resolved twice through `0020E600` - once tested for null, once for real - and `0051A920(record2, edi)` consumes the pair - the ramp channel's quantised pick turned into the emitted command.

Interior anchor `003E48AC` (function `003E4890`).

`0041BDC0` (276 B) is the mask-filtered emit `00418880` runs: `word[rdx+0x96] &= ~0x80` clears the busy bit and `003AB7F0([rcx+0x2B0])` + `dword[rbx+0x2B8]` locate the `0x108`-stride records counted by `word[+0x2BC]`; on each whose `(dword[[r8+0x70] + 4] >> 4) & 3` kind is 1, an 8-bit ladder doubles through `edi` testing `word[rbp+0x102] >> 7 & word[(dword[rbp+0xFC] + r13) + 2]` per bit and firing `0041B650(slot, r12, word[rbx], 0)` on the hits, `rbx` walking `0x1C` strides - the channel-mask fan-out behind the ramp's per-record arm.

Interior anchor `0041BE82` (function `0041BDC0`).

`0051A920` (258 B) is the channel-select commit `003E4890` runs: `edx - 1` picks which signed word of `+8`/`+0xA`/`+0xC`/`+0xE` supplies the value (out-of-range exits), `byte[+0x17] |= 1` marks it, and when it differs from `dword[+4]` the word stores, `byte[+0x15] |= 8` raises the dirty bit and `0020E600([+0x10])` resolves the target; `cvtdq2ps x 0.05f`/`x 0.01f` scale it into the `[rbx+0x14]`-counted `0x70`-stride output rows' `+0`/`+8` floats - the ramp write one channel select performs.

Interior anchor `0051A98A` (function `0051A920`).

`00372F60` (193 B) is the cross-row backpatch `0046E420` runs: `[rbp+0x84]`/`[rbx+0x84]` resolve through `0020E600` into two `0x290`-stride row tables, and for each of `[rbp+0x8A]` link words the target row's `+0x27C` word (when not `0xFFFF`) is `0020E620`-resolved and stored to `+0x278` - wiring each linked record's resolved address

Interior anchor `00372FC2` (function `00372F60`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page traces the ramp step from its frame drivers down to the channels, so it cites frame, menu and area bodies
by construction. Their other neighbours are listed here; none is a ramp-channel relationship.

**UI — MECHANICAL, eleven edges.**
- The `003F80D0` group's ready setter `0035C560` calls `0028F8B0`, `00290430` and `003C5E40`.
- The mode read `00229EA0` is also asked by the menu bodies `002468A0` and `00246C20`.
- `RenderCommand_SubmitCurrentBufferAndSwap` is also called by the text interpreter (`002AC5F0`, `002AF960`).
- The full-menu predicate `00181DD0` has a menu caller, `0024B9B0`.
- The field frame `0022A770` calls the menu body `00254E50`.
- The `vf00` reset `0036DD80` is reached from `0035DCC0`.

The menu pages own the menus.

**WorldAreaField — MECHANICAL, nine edges.**
- The area unload `002628B0` (a caller of the presentation reset `0024D9C0`) calls `00378230`, `003DFA50` and
  `003EAA00`.
- The field frame `0022A770` and `MainLoop_UpdateAndRenderFrame` run `World_UpdateSimulationTick`.
- `003775D0` calls the audio fade helper `002DEE90`.
- `003601D0` calls `00331920`.
- The request toggle's teardown `003ABCA0` and the field fill `003AFD40` are reached from `00378230` / `00378120`.

The tick order is `the-world-tick-and-the-field-frame`'s.

**Script_VM_Native_Bridge — CLIENT, eight edges.** Script handlers reach bodies this page cites:
- the audio fade leaf `002DEDE0`, from `00345010`, `00350EC0` and `0050E960`;
- the mode read `00229EA0`, from `00354D00`;
- the kind-3 read `00264670`, from `00343520`;
- the close-full-menu predicate `002E05C0`, from `0050D1E0`;
- `00360710` (a `0024D9C0` caller), from `0034ECF0`;
- `003A1070` (the `00332C40` handler's callee), from `00357040`.

Those are script verbs using the same helpers, owned by the script VM pages.

**Save_Load_Settings — DEPENDENCY, four edges.**
- The frame step `0017D6E0` calls `SaveloadManager_GetSingleton` and `SaveloadManager_ProcessPendingCaptureCopy`.
- The area unload `002628B0` calls `SaveImage_GetPersistentPayloadBase`.
- `003601D0` calls `SaveImage_ClearActiveRuntimeBuffer`.

The frame and the area unload service the save layer too; the save pages own what they copy.

**StoryEvent — MECHANICAL, two edges.** The channel-record copy's other user `00418880` calls `001EC6B0` and
`001ED240`, both filed StoryEvent.

**Gameplay — MECHANICAL, one edge.** `BattleUnit_UpdateCombatFrame` calls `BattleUnit_DispatchActorPresentationEvent`,
the shared authored-command callee this page cites.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page reads them; no new body read (OPUS, 2026-09-29,
pass-22 debt `42a617a9a`).*

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../_index/candidates/fable-contract-authored-command-ramp-channels-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001DC2E0` | 78 B | calls `00210B30` with the incoming argument registers unchanged, then returns `00211270(result, rcx, edx, r8, r9d)` with the incoming `rcx` in `rdx`, `edx` in `r8d`, `r8` in `r9` and `r9d` as the fifth (stack) argument | `001DC2FF`, `001DC307`, `001DC314` |
| `001EB7B0` | 79 B | stores `edx` at dword `rcx+0x11C`; when dword `+0x130` is not -1, zeroes byte `+0x118`, calls `002EEB20(dword +0x130)`, then stores qword -1 at `+0x130`, dword -1 at `+0x120` and 0 in byte `+0x26E`; on both paths tail-jumps `001EB9C0(rcx)` | `001EB7B9`, `001EB7C5`, `001EB7D1`, `001EB7D6`, `001EB7FA` |
| `002EE3E0` | 70 B | calls `003EC580(movsx cx)` and, when that is non-null, `00422D50` on it; when that second result is non-null, clears bit `0x800000` of its dword `+0xC`, calls `0041C410` on it and then sets that bit again; a null at either step returns without further work | `002EE3E7`, `002EE3F9`, `002EE406`, `002EE410`, `002EE415` |
| `00345010` | 70 B | takes `eax = 00267E10(r9)`, replacing it with `002DEC00()` when negative (`jns`), and calls `002DEDE0(eax)`; then, when `00267310(byte rdx+0x15)` is non-zero, tail-jumps `00360960(-1, 0, 0)`, else returns | `0034501C`, `00345023`, `0034502C`, `00345035`, `0034504B` |
| `00350EC0` | 107 B | returns 0 when the dword `[r8]` is negative (signed); otherwise, when `00267310(byte rdx+0x15)` is non-zero, calls `002DEDE0(dword [r8])` and `00360960(-1, 0, 0)` and returns 0, and when it is 0 returns 1 if `002DED60(dword [r8])` is non-zero and 0 otherwise (`cmovne`) | `00350ECF`, `00350EE5`, `00350EF0`, `00350EFD`, `00350F1B` |
| `003AFD50` | 37 B | indexes the `0x70`-byte entries at `02B3F570` by the zero-extended `cl` and, when the entry's dword `+4` equals `ecx`, stores the float `xmm1` at its `+8`; otherwise does nothing | `003AFD53`, `003AFD57`, `003AFD63`, `003AFD66`, `003AFD6F` |
| `003AFD80` | 73 B | indexes the `0x70`-byte entries at `02B3F570` by the zero-extended `cl` and, when the entry's dword `+4` equals `ecx` and the float `rdx+4` differs from (or is unordered with) the entry's float `+0x10`, stores that float at `+0x10` and 1.0 (`01CEBBA8`) divided by it at `+0x14`; otherwise does nothing | `003AFD95`, `003AFDAB`, `003AFDBA`, `003AFDBE`, `003AFDC3` |
| `003B6A10` | 119 B | forms the record `movzx(cl) * 0xE0 + qword 02B40528` and returns unless its dword `+0x10` equals `ecx`; when `dl` is non-zero, stores `dl` in byte `+2` and writes (float `[r8]` minus float `+0x58`) and (float `[r8+4]` minus float `+0x5C`), each times 1.0 (`01CEBBA8`) divided by `dl`, to `+0x68` and `+0x6C`; when `dl` is 0, zeroes byte `+2` and copies dwords `[r8]` and `[r8+4]` to `+0x58` and `+0x5C` | `003B6A22`, `003B6A42`, `003B6A55`, `003B6A6B`, `003B6A7A` |
| `003B6A90` | 117 B | forms the record `movzx(cl) * 0xE0 + qword 02B40528` and returns unless its dword `+0x10` equals `ecx`; when `dl` is non-zero, stores `dl` in byte `+0` and writes (float `[r8]` minus float `+0x50`) and (float `[r8+4]` minus float `+0x54`), each times 1.0 (`01CEBBA8`) divided by `dl`, to `+0x60` and `+0x64`; when `dl` is 0, zeroes byte `+0` and copies dwords `[r8]` and `[r8+4]` to `+0x50` and `+0x54` | `003B6AA2`, `003B6AC1`, `003B6AD4`, `003B6AEA`, `003B6AF8` |
| `003B6BB0` | 28 B | forms the record `movzx(cl) * 0xE0 + qword 02B40528` and, when its dword `+0x10` equals `ecx`, stores the float `xmm1` at `+0x2C`; otherwise does nothing | `003B6BB3`, `003B6BC1`, `003B6BC6` |
| `003B6BD0` | 28 B | forms the record `movzx(cl) * 0xE0 + qword 02B40528` and, when its dword `+0x10` equals `ecx`, stores the float `xmm1` at `+0x44`; otherwise does nothing | `003B6BD3`, `003B6BE1`, `003B6BE6` |
| `003B6BF0` | 43 B | returns 0 when `cx` is -1; otherwise forms the record `movsx(cx) * 0x740 + qword 022C6F28` and returns 0 when that is null or its dword `+0x284` is 0, else tail-jumps `003E6F70` with `rcx` = the record | `003B6BFD`, `003B6C0B`, `003B6C0D`, `003B6C16` |
| `00422EB0` | 117 B | returns 0 when dword `rcx+0xC4` is -1; otherwise takes `p = 0051B9E0(qword +0xDA8 of 0020E600(dword rcx+0x10), dword rcx+0xC4)` and calls `0041CA70(p)`, then, when qword `p+0x368` is non-zero and bit `0x100` of dword `p+0xC` is clear, calls `0041C410(p)` and returns 1, else returns 0 | `00422EDF`, `00422EEF`, `00422EF8`, `00422F04`, `00422F15` |
| `0046D8E0` | 54 B | multiplies the float `rcx+0x3C` (read once, before any store) by the four floats at `rdx`, `rdx+4`, `rdx+8` and `rdx+0xC` and stores the products at `rcx+0x30`, `+0x34`, `+0x38` and `+0x3C` | `0046D8EB`, `0046D8EF`, `0046D8FC`, `0046D906`, `0046D910` |
| `0046D920` | 41 B | multiplies the float `rcx+0x3C` by the three floats at `rdx`, `rdx+4` and `rdx+8` and stores the products at `rcx+0x30`, `+0x34` and `+0x38`, leaving `+0x3C` unchanged | `0046D92B`, `0046D92F`, `0046D939`, `0046D943` |
| `0046FB40` | 100 B | with `n` = dword `01F20530` (decoded 0x32), truncates `(n - 1) * xmm0` to an integer `i`, using 0 when it is negative and `n - 1` when it is above `n - 1` (unsigned compare), and copies the three dwords at index `3i`, `3i+1`, `3i+2` of the dword table `01F20540` to `rdx`, `rdx+4` and `rdx+8` | `0046FB5F`, `0046FB65`, `0046FB6C`, `0046FB84`, `0046FB9F` |
