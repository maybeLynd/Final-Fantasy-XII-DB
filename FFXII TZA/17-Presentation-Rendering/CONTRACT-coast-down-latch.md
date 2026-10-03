---
contract: glide a stopped character to a halt by replaying a cached heading and a decaying speed
category: 17-Presentation-Rendering
scope: transition
readiness: DIFFERENTIAL TESTED   # the latch; its tail's two callees are supplied as oracles — see §13
confidence: PROVEN
implements: 17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md
entries: ["00424080"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 92 addresses cited - 6 data, 8 entry, 75 interior, 3 literal, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-coast-down-latch-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the coast-down latch

`Movement_ModifyHeadingSpeedForObjectState` (`00424080`, 427 B) sits on the seam between presentation
and movement. It takes a record id and a heading and speed **by address**, and either overwrites them
with a replay of what the character was doing before it stopped, or caches what they currently hold.
It is a two-state machine with one edge each way and every constant in it is a literal.

## 1. Purpose

A character that stops does not stop instantly on screen: it glides. The glide is not animated and
not simulated — it is the last heading held constant while the last speed is multiplied by `0.83`
every call, until the speed falls to `0.05` and control returns to movement.

## 2. Interface

| | |
|---|---|
| entry point | `00424080` (427 B) |
| calling convention | Microsoft x64 |
| parameters | `cx` = record id, **signed 16-bit** (`0042408A movsx rax, cx`); `rdx` = pointer to the caller's heading; `r8` = pointer to the caller's speed |
| return type | none used |
| return semantics | the operation communicates entirely through the two pointers |
| side | in-out: both `*rdx` and `*r8` are read on one path and written on the other |

## 3. Types

`CharacterRenderRecord`, addressed as `*(char**)0x022C6F28 + id * 0x740`.

**The two motion blocks are mirrors, and this is the structural claim that matters.** The cache
operation is a single 16-byte move, so `+0x610` and `+0x620` have the same shape:

| live | cached | member | note |
|---|---|---|---|
| `+0x610` | `+0x620` | heading | `float` |
| `+0x614` | `+0x624` | speed | `float`; the cached one decays |
| `+0x618` | `+0x628` | speed scale | `float` |
| `+0x61C` | `+0x62C` | flags | `uint16`; **bit 0 is the latch** |

Also read: `+0x000` the record id (`-1` means a free slot), `+0x006` a latch precondition, `+0x0CC`
the subtype, `+0x284` the object flags, `+0x457` a stop-frame counter.

## 4. Preconditions · postconditions · invariants

**Preconditions.** The record id must name a live slot: `0042409F cmp word ptr [rbx], -1 / je` exits
otherwise, writing nothing. The id is sign-extended, so a negative id indexes backwards from the pool
base — nothing rejects it.

**`rdx` and `r8` must be non-NULL, and nothing checks them.** Added 2026-09-11 after a contract-first
probe needed the answer and the text did not have it: the prologue runs `movsx rax, cx`,
`mov rsi, r8`, the record lookup, and the `-1` test, with **no test of either pointer**; both are
dereferenced unconditionally on the paths that use them. A reimplementation that adds a null guard is
more forgiving than the original.

**Postconditions.** ~~Exactly one of three things happens:~~ **FOUR, and the fourth runs after two
of the other three — CORRECTED 2026-09-11 by executing the function.** The three are: the latch is
serviced (heading and speed overwritten from the cache, speed decayed), the latch is armed (same,
plus bit 0 set), or the live block is cached and the caller's values are kept. **The fourth is the
tail at `0042419F`** — see §7a.

> ### ⚠ The invariant is false, and the branch targets say so
>
> ~~**Invariant.** The caller's heading and speed are never both left untouched *and* uncached;
> every path through a live record either replays or caches.~~
>
> **The five arming conditions do not share an exit.** §10.1 lists them "each with its exit" and
> this invariant assumed those exits were the same place. They are two places:
>
> ```
> 00424129  je  0042419F    condition 1 (+0x284 & 0x08000000) fails -> the TAIL, nothing cached
> 00424130  jne 0042419F    condition 2 (+0x006 == -1)        fails -> the TAIL, nothing cached
> 00424135  jne 00424182    condition 3 (subtype == 0x10)     fails -> CACHE
> 00424142  jp  00424182    condition 4 (speed == 0.0f)       fails -> CACHE
> 00424144  jne 00424182
> 00424156  jb  00424182    condition 5 (stop-frame counter)  fails -> CACHE
> ```
>
> So for a record whose object flag `0x08000000` is clear, or whose `+0x006` is not `−1`, **the
> operation neither replays nor caches**: the caller's heading and speed arrive and leave unchanged
> and both motion blocks are untouched — except for whatever the tail then does to the speed scale.
>
> **How it was established.** A reconstruction that sends conditions 1 and 2 to the cache — the
> reading this invariant encodes — was built and run against the shipped body: **7 of 70 cases
> disagree**, on the record's own bytes. The corrected reconstruction agrees on all 70.
>
> The corrected invariant: *every path through a live record either replays, or caches, or leaves
> both blocks alone; and every path except servicing continues into the tail.*

## 5. State

| | fields | evidence |
|---|---|---|
| read | `+0x000`, `+0x006`, `+0x0CC`, `+0x284`, `+0x457`, both motion blocks, `*rdx`, `*r8`, the global at `01DFE0B4` | `0042409F`, `0042412B`, `004240AE`, `0042411F`, `0042414D`, `00424182`, `00424146` |
| written | one motion block, `*rdx`, `*r8` | `0042418C`–`0042419B`, `004240E6`, `00424173` |
| allocated / deallocated | none | |

## 6. Relationships

Calls `0020E600` after the latch logic to resolve `+0x010` when `+0x0C4 != -1` — the presentation
entry path, ~~outside this transition~~ the fourth stage of this transition *(answered: see §7a, added 2026-09-11 - it runs on every path except servicing; 2026-10-02, OPUS)*.

## 7. State transitions

```
            latch clear ──[five conditions, §10.1]──> latch SET
            latch set   ──[cachedSpeed <= 0.05f]────> latch clear
```

**Servicing (bit 0 set).** `cachedSpeed *= 0.83f`; `*rdx = cachedHeading`; `*r8 = cachedSpeed`; then
if `0.05f >= cachedSpeed`, clear bit 0 of `+0x62C`.

**Arming.** Same replay, and bit 0 of `+0x62C` is set.

**Caching (conditions not met).** The whole 16-byte live block is copied to the cached block;
`liveHeading = *rdx`; `liveSpeed = *r8`; bit 0 of the **live** word `+0x61C` is cleared.

> **The cache path never writes `+0x62C`.** It clears bit 0 at `+0x61C` and the 16-byte copy that
> preceded it is what carries a cleared word into `+0x62C`. A reimplementation that models only
> `+0x62C`, or that copies the block member by member, never releases the latch on this path and the
> character glides forever.

## 7a. The fourth stage — ADDED 2026-09-11

`0042419F`–`00424212`, gated on `record + 0xC4 != -1`. **It runs on every path except servicing** —
after arming, after caching, and directly when arming condition 1 or 2 fails (§4). Servicing jumps
past it (`00424108 jb 00424216` and `0042411A jmp 00424216`).

```
0042419F  cmp dword [rbx+0xC4], -1 / je exit
004241A8  mov ecx, [rbx+0x10]      ; the record's own dword
004241AB  call 0020E600
004241B6  mov rcx, [rax+0xDA8]     ; NO null test on the result — see below
004241BD  call 0051B9E0            ; (that, record+0xC4)
004241C2  test rax, rax / je exit  ; only THIS result is checked
004241C7  mov ecx,[rax+0x378] / add ecx,[rax+0x370] / movsxd rax, ecx / je exit
004241D8  cmp byte [rax+1], 1 / jne exit          ; the SUM is used as an ADDRESS
004241DE  lea eax,[rbp-0x35] / cmp eax,1 / jbe    ; subtype 0x35 or 0x36
004241E6  cmp ebp, 0xD / jne                      ; subtype 0x0D
004241EB  mov dword [rsi], 0                      ; 0x0D: the CALLER'S SPEED IS ZEROED
004241F3  mov dword [rdi+8], 0x3F800000           ; otherwise: speed scale := 1.0f
004241FC  mulss [rdi+8], 0.9f ; then [rsi] *= [rdi+8]   ; 0x35/0x36: scale and apply
```

**Three things a reader needs from this.**

1. **The caller's speed can be zeroed here**, for subtype `0x0D`, after the operation has already
   written it once. A reimplementation stopping at §7's three outcomes returns the coasting speed
   where the original returns zero.
2. **`[rdi + 8]` is two different fields.** `rdi` is `record + 0x610` everywhere except the arming
   path, which rebases it to `record + 0x620` at `00424158`. So the speed-scale write lands on the
   **live** block after a cache and on the **cached** block after an arm — one instruction, two
   destinations, decided by a branch two hundred bytes earlier.
3. **`0020E600`'s result is dereferenced unchecked.** `004241B6 mov rcx, [rax + 0xDA8]` follows the
   call with no `test`. §4 records two unchecked pointer parameters; this is a third unchecked
   dereference, and a NULL there is an unconditional access violation in the shipped game. The
   differential suite deliberately does **not** drive it: there is no behaviour to compare, only a
   crash on both sides, and a case that crashes both is not a test.

**`0020E600` and `0051B9E0` are both read now** (2026-09-13, `FABLE-REQ-OPUS-COASTDOWN-LOOKUP`).
`0020E600` is `ImageAddress_ResolveRuntimePointer` (§15a). **`0051B9E0` is a 5-byte tail jump to
`0051F240`, `PresentationEntryReferenceContainer_ResolveEntryById`, 138 bytes, re-derived here rather
than taken from the summary:**

```
0051F24A  mov r8d,[rcx+4] / shl r8d,0x1E / sar r8d,0x1E   ; kind = sign-extended 2-BIT field
0051F25B  test r8d,r8d / je  -> kind 0 : rbx = 003AB7F0([rcx+8]) + id*0x30
0051F260  cmp  r8d,1   / jne -> return 0                  ; ONLY kinds 0 and 1 resolve
0051F266  movzx ecx,di                                    ; kind 1 : rbx = [r9+8] + id*0x30
0051F291  test rbx,rbx / je  -> return 0
0051F2A3  test byte [rbx],2 / je -> skip refresh
0051F2A8  rcx=[rbx+0x10] / call 003AB7F0 / add eax,[rbx+0x20] / movsxd / mov [rbx+0x18],rcx
0051F2BB  return [rbx+0x18]                               ; the CACHED pointer, not the entry
```

**Four things this settles that the contract could not say while it was an oracle.**

1. **No bound check of any kind.** The id is `movzx ecx, di` — **the low 16 bits of `edx`** — scaled
   by `lea rcx,[rcx+rcx*2]; shl 4`, i.e. **× `0x30`**, and added to the base. There is no capacity
   compare, no generation compare, no table length. **Whatever id arrives is an offset.**
2. **`record + 0xC4` is compared as a full dword and consumed as a word.** `0042419F` and `00424236`
   both test `cmp dword [rbx+0xC4], -1`, but only `di` reaches the lookup. An id of `0x00010000` is
   not `-1`, is not skipped, and resolves as **entry 0**. A reimplementation that narrows to 16 bits
   at the compare, or widens to 32 at the index, diverges from the original on exactly those values.
3. **The returned pointer is the entry's cache, not the entry.** The 0x30-byte entry carries flags at
   `+0x00`, a handle at `+0x10`, the cached pointer at `+0x18` and a delta at `+0x20`; `0051F2BB`
   returns `[rbx+0x18]`. That is why §7a's tail reads `+0x370`/`+0x378` off the result — those are
   offsets into the *resolved object*, not into a 0x30-byte entry.
4. **The refresh is the same sign-extended-32-bit idiom as `0020E600`.** `add eax, [rbx+0x20]` then
   `movsxd rcx, eax`: a 32-bit sum widened to 64. §7a already flags the caller's
   `mov ecx,[rax+0x378] / add ecx,[rax+0x370] / movsxd rax, ecx` as "the SUM is used as an ADDRESS";
   **it is the subsystem's addressing convention, not a local quirk**, and it is where a 64-bit
   reimplementation silently stops matching above 2 GiB.

**The null-table fault is real and is narrower than "a null table crashes".** With kind 0 and a null
table pointer, `rbx = 0 + id*0x30`, so the `test rbx, rbx` guard **passes for any nonzero id** and
`0051F2A3 test byte [rbx], 2` dereferences a near-null address. **Id 0 returns 0 safely; every other
id faults.** The guard tests the computed address, not the base.

**And `00424230`'s default is permissive, which matters to the contract's outcome set.** It returns
**`1`** both when `[rcx+0xC4] == -1` (`00424240`) and when the lookup returns null (`0042425F`), and
only otherwise returns `0041C760(resolved) & 1`. **A missing entry and a failed lookup are reported as
the same success as a set bit** — so a reimplementation that returns 0 on "not found" inverts the
behaviour on both paths.

## 8. Script · resource · event interactions

None. ~~The subtype at `+0x0CC` comes from authored data~~ *(corrected 2026-09-27, OPUS, on FABLE's BT-4 record [`bt4-event-motion-slots/`](../_index/candidates/bt4-event-motion-slots/README.md)): the subtype at `+0x0CC` is the render record's current event, stored by `00424D80` (`00424FAB`) from posted events - posted by the engine (`0x200D` terminal-status recovery, `0x2010` the mount in turbo, `0x4035` / `0x4036` combat stance) or by script verbs. What is authored is the motion each character's `.ca` holds at that slot.* This operation only compares it.

## 9. Determinism

**RNG** — none. **Timing** — the decay is per *call*, not per second, so the glide length is frame-rate
dependent by construction. **Threading** — none.
**Floating point** — the "not moving" test is `ucomiss` against zero with both `jp` and `jne` taken to
the cache path, so a NaN speed caches and **negative zero arms**. The release compares `0.05f` against
the decayed speed with `comiss` / `jb`, so the latch releases when `cachedSpeed <= 0.05f` — the
boundary value releases.

## 10. Failure paths and edge conditions

1. **Arming requires FIVE conditions, not three.** ~~The document lists the first three.~~ *(answered: see the record-array page, which now lists all five; 2026-10-02, OPUS)* All five, in
   order, each with its exit:
   `+0x284 & 0x08000000` (`0042411F test / je`); `+0x006 == -1` (`0042412B cmp / jne`);
   `(subtype & 0xFFF) == 0x10` (`004240B5 and ebp, 0xfff`, `00424132 cmp ebp, 0x10 / jne`);
   **the caller's speed is exactly `0.0f`** (`00424137 movss xmm1, [r8]`, `0042413F ucomiss` with
   `jp`/`jne`); and **the stop-frame counter has reached the threshold** —
   `00424146 imul eax, dword ptr [rip+...], 0x1e` against the time base at `01DFE0B4`, then
   `0042414D movsx ecx, byte ptr [rbx + 0x457]` and `00424154 cmp ecx, eax / jb`.
2. **The stop-frame counter is sign-extended and then compared unsigned, and it IS reachable --
   the writer drives it there itself.** `movsx` widens a signed byte, `jb` is an unsigned branch, so
   a negative counter becomes a huge unsigned value and **passes** the threshold test. This contract
   previously left reachability open pending the writer. **ANSWERED 2026-09-11 (OPUS-PROBE-COASTDOWN).
   `+0x457` has exactly one writer in the image**, `00425C3A` in `FUN_004256e0`:

   ```
   00425C25  imul   ecx, dword ptr [01DFE0B4], 0x5a      ; 90 x timeBase = 180
   00425C2C  movsx  eax, byte ptr [rdi + 0x457]
   00425C33  inc    eax
   00425C35  cmp    eax, ecx
   00425C37  cmovb  ecx, eax                             ; saturate at 180
   00425C3A  mov    byte ptr [rdi + 0x457], cl           ; ...into a SIGNED BYTE
   ```

   **The saturation bound cannot fit the field it saturates into.** The counter is clamped to ~~180~~ `90 x timeBase`, which is 180 when the time base is 2; at the image value 1 the clamp is 90, which fits, and the byte never wraps *(corrected 2026-10-02, OPUS: `004256E0`+0x545 `imul ecx, dword ptr [01DFE0B4], 0x5a`)*; at 180 it is
   stored in an `int8` whose maximum is 127, so on the 128th increment `cl` is `0x80` and the next
   `movsx` reads **-128**. From then on the value is negative, the unsigned `cmp`/`jb` at
   `00424154` always falls through, and **the arming threshold is satisfied permanently for that
   record**. A character stopped for 128 calls arms its coast-down on every subsequent call regardless
   of how long it has actually been still.

   This is a defect in the original, not in the reading: the same routine tests the counter against
   `0x1e x timeBase` at `00425C42`, so 30 and 90 are deliberate multiples of one base and only the
   storage width is wrong. **A reimplementation must reproduce the wrap**, because clamping correctly
   at 127 -- or widening the field -- changes when characters glide.

   **It is not one counter but two, and they are a pair.** `+0x456` is a sibling with the identical
   idiom and the identical overflow (`00425BC8`-`00425BE3`), and `00425C63` clears **both** with a
   single `mov word ptr [rdi + 0x456], bp` (`bp` zeroed at `004257B7`). A reimplementation that splits
   them into two independent fields loses the atomic reset.

   **The time base is read at two widths in that one function** -- `dword` at `00425BC8` and
   `00425C25`, signed **byte** at `00425BED` (`movsx eax, byte ptr [01DFE0B4]`). ~~Its value is `2`, so~~ It holds `1` in the image and `2` once `001EDDC0` runs with a non-zero argument (the 60 fps switch); either value fits a byte, so *(corrected 2026-10-02, OPUS: the one writer `001EDDC0`+0x32 sits behind `001EDDC0`+0x6 `je`, taken when `ecx` is 0)*
   the readings agree today; a reimplementation that types the global once must still know both
   accesses exist.

   **The rule this generalises to, with its negative control.** An image-wide sweep for byte stores of
   a clamped register found 21 sites. The defect is *not* "the bound exceeds 127" -- `003F9AF0` clamps
   to `0x80` and stores a byte, and is **correct**, because it reads the field with `movzx`: the field
   is unsigned and 128 fits. The defect is **a bound above 127 combined with a signed read**, and on
   that rule only the `+0x456`/`+0x457` pair fails. The sweep's positive control is the pair itself.
3. **A negative record id is not rejected.** `movsx rax, cx` then `imul rax, 0x740` addresses before
   the pool.
4. **The decay runs on the arming call too** — the arm path multiplies by `0.83f` before publishing,
   so the first replayed speed is already decayed once.

## 11. Observable behaviour

On screen: a character that stops glides and halts; with the latch forced clear it stops dead. In
memory: while gliding, `+0x624` falls geometrically by `0.83` per call and `+0x62C` bit 0 is set; on
the call where `+0x624 <= 0.05`, the bit clears. Both are directly readable from the record.

## 12. Reproduction formula

```
modifyHeadingSpeed(id, pHeading, pSpeed):
    rec = *(char**)0x022C6F28 + (int16)id * 0x740
    if *(int16*)rec == -1: return
    subtype = (*(int16*)(rec+0xCC)) & 0xFFF
    if (*(uint16*)(rec+0x62C)) & 1:                       # servicing
        s = *(float*)(rec+0x624) * 0.83f
        *(float*)(rec+0x624) = s
        *pHeading = *(float*)(rec+0x620)
        *pSpeed   = s
        if 0.05f >= s: *(uint16*)(rec+0x62C) &= ~1
    else:
        armed = (*(uint32*)(rec+0x284) & 0x08000000)
             && *(int16*)(rec+6) == -1
             && subtype == 0x10
             && *pSpeed == 0.0f
             && (uint32)(int8)*(rec+0x457) >= (uint32)(*(uint32*)0x01DFE0B4 * 30)
                 /* timeBase is 2 -- ONE writer in the image, 001EDDF2 stores the        */   /* <- corrected 2026-10-02, OPUS - the image holds 1; 001EDDC0+0x32 stores 2 only when 001EDDC0 is entered with a non-zero ecx (the 60 fps switch), so the threshold is 30 or 60 */
                 /* constant -- so the threshold is 60. The counter saturates at 180 in  */
                 /* an int8, so it turns negative on the 128th call and this test then   */
                 /* passes forever. See section 10.2; the wrap is load-bearing.          */
        if armed:
            s = *(float*)(rec+0x624) * 0.83f
            *(float*)(rec+0x624) = s
            *pHeading = *(float*)(rec+0x620)
            *pSpeed   = s
            *(uint16*)(rec+0x62C) |= 1
        else:
            memcpy(rec+0x620, rec+0x610, 16)              # ONE move - see §7
            *(float*)(rec+0x610) = *pHeading
            *(float*)(rec+0x614) = *pSpeed
            *(uint16*)(rec+0x61C) &= ~1                   # the LIVE word
```

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent.** (2026-09-11)

The shipped 427 bytes have been executed at their real virtual address under Unicorn against an
independent reconstruction. This section previously read *"Empty"*; that remains true of the live
class and is now false of the isolated class. Every claim is still decoded from the verified image,
including all four constants: `0.83f` at `00D12434`, `0.05f` at `008F30E8`, `0.9f` at `008FCC8C`,
and the time base at `01DFE0B4`, which holds `1` in the shipped image so the default threshold is
30 — all four re-read from the image on every harness run rather than inherited.

**Instrument:** [`Reconstruction/Tests/Differential/diff_coast_down.py`](../../../Reconstruction/Tests/Differential/diff_coast_down.py)
against [`Reconstruction/Game/Presentation/coast_down.c`](../../../Reconstruction/Game/Presentation/coast_down.c).

**Result: 70 cases, 70 comparisons, 0 mismatches**, with 39 distinct outcomes, 44 cases leaving the
latch set and 50 writing a non-zero speed back. Every value crosses as a **bit pattern** and each
comparison covers the caller's heading and speed *and* all 32 bytes of the two motion blocks.

| what was executed | outcome |
|---|---|
| a free slot (`+0x00 == -1`) writing nothing at all | **agrees** |
| a 24-call glide, driven call by call from a speed of 100 down through the release | **agrees** |
| the release boundary, at the value whose decay lands on `0.05f` and one ULP either side | **agrees** |
| all five arming conditions, each failed **alone** with the other four satisfied | **agrees**, and it is what exposed the two-exit asymmetry in §4 |
| a NaN speed (caches) and a negative zero (arms) | **agrees** — §9's claim, executed |
| the `+0x457` counter at `−128`, `−1`, `0`, `29`, `30`, `31`, `127` against time bases 1, 2 and 5 | **agrees**, including the §10.2 wrap where a negative byte arms |
| the cache path releasing the latch **through the 16-byte block copy**, with `+0x62C` bit 0 planted set | **agrees** |
| a negative record index landing on the record before the pool centre | **agrees** |
| the §7a tail on both entry paths, through each subtype branch and each of its three early exits | **agrees** |

**The harness was shown to have teeth on the finding that matters.** A reconstruction encoding the
old invariant — conditions 1 and 2 falling into the cache like the other three — disagrees on **7 of
70** cases, on the record's own bytes.

### What this does NOT show

- **Nothing was drawn and no character moved.** This is a presentation-side operation and the
  harness compares numbers.
- **The decay is per *call*.** §9 says the glide length is frame-rate dependent by construction; the
  suite drives calls, so it reproduces the decay and says nothing about how many calls a frame makes.
- **`0020E600` and `0051B9E0` are supplied**, so the tail's *decision* is established ~~and those two~~
  ~~functions are not~~ *(answered: see §7a and §15a - both read 2026-09-13; supplying them here is a harness choice; 2026-10-02, OPUS)*.
- **The `+0x457` writer at `004256E0` was read, not run.** §10.2's wrap is established for the
  *reader*; that the writer drives it there is still a reading.

### What is still owed, and it is live-only

1. **Does a real character reach 128 stopped calls?** §10.2 says the counter then arms permanently.
   A watch on one record's `+0x457` across a character standing still would settle whether the
   defect is reachable in play or only in principle.
2. **Which subtypes occur.** The tail's `0x0D` branch zeroes the caller's speed; nothing here shows
   that any real render record carries subtype `0x0D`.
3. ~~**What `0020E600` and `0051B9E0` are**~~ *(answered: see §7a - `0020E600` is `ImageAddress_ResolveRuntimePointer`, `0051B9E0` a tail jump to `0051F240`; 2026-10-02, OPUS)*, which is static work rather than live, and out of this
   package's scope rather than blocked.

Queued; the live-automation pause stands.

<!-- OPUS-MUT-S13-RESTATE -->
### Mutation campaign, re-run 2026-09-12 on the full literal surface

**56 generated points: 41 KILLED · 1 SURVIVED · 5 EQUIVALENT · 9 NO_BUILD · 0 TIMEOUT · 0 INVALID. Verdict `FAIL`.**
Receipts: `Database/Tools/work/OPUS/litsuffix/coast_down2` (ignored path). Instrument: `Reconstruction/Tests/mutation_test.py`. The table for every pilot, and the four kinds a survivor can be, are on [`MUTATION-CAMPAIGNS.md`](../../../Reconstruction/MUTATION-CAMPAIGNS.md).

One **real gap**, closed: `objectFlags & 0x08000000` → `& 0x08000001` survived because gate 1 was only ever failed with `obj_flags = 0`, which fails both masks. Bit 0 alone fails the first and passes the second, and that case kills it. The remaining survivor is **kind C, undefined behaviour**: `memcpy(&rec->live.heading, heading, 4)` → `5` reads one byte past a `float` and writes it onto `speed` at `+0x04`, which **the next statement overwrites whole**. No case can see it, and none should be contrived to.

## 14. Unresolved

1. ~~**Who writes `+0x457`**~~ — **answered in §10.2** (OPUS-PROBE-COASTDOWN, 2026-09-11); this entry
   was stale. `00425C3A` is the only byte writer and it drives the counter negative itself.
   *Confirmed 2026-09-22 (SWE2-CONTRACT-COASTDOWN-ATTACHLINK):* the store is
   `cl = min_unsigned(old+1, dword[01DFE0B4]*90)` — an **unsigned** `cmovb`, so with `timeBase=2`
   the byte walks `0,1,…,0x7F,0x80` then snaps to `0xB4` and stays: a **negative fixed point of
   −76**, not a ramp through the negatives. `(uint32)(int8)` of it is ≥ 60 from the 60th call and
   forever after; §10.2 is reachable and permanently latched. The pair word-store `00425C63`
   (`mov word [rdi+0x456], bp`, `bp` zeroed) is the atomic reset of both counters.
2. **`+0x006` is the record's owner link — the id of the record this one is a piece of.**
   *Answered 2026-09-22 (SWE2-CONTRACT-COASTDOWN-ATTACHLINK):* the three real-value writers all do
   `movzx eax, word [src]` → `mov word [dst+6], ax` — the **source record's `+0x000` id** into the
   target's `+0x006` — inside the piece-attach commits `0042F2A0` (`0042F2E6`), `0042F77A`
   (`0042F83E`) and `0042F93B` (`0042FAAE`), each paired with `src+0x18 → dst+0x2C4` and a
   `00426E40(owner, piece)` call, matching the attach step the record page names ("`piece+6 =
   owner's id`"). The three `-1` stores — `00421C9C`, `0042CA15`, `0042CC70`, all
   `or eax, -1` → `[rec+6]` beside `+0x2F0 = 0xFFFF` and a `0041EC00` projected-origin update —
   are the detach/orphan paths, and `0041F730` seeds `-1` at reset among the six head words.
   So the latch precondition `+0x006 == -1` reads **"this record is not an attached piece"** —
   pieces ride their owner's transform and must not arm an independent coast-down. (Byte writes
   to `+6` in `003DC340`/`0051C3F1`/`0051CCAE` touch other record types sharing these functions,
   not this field.)
3. **`+0x0CC` is the record's current render-event word; `& 0xFFF` strips the kind nibble and
   `0x10` is an event index, not an object type.** *Answered 2026-09-22:* bits 12–15 of `+0xCC`
   are the event kind and the low 12 bits the index (the render-event selection evidence; the
   priority bytes at `01F00410` are indexed by the same 12 bits). So the four speed rules key on
   event indices: `0x0D` zeroes the caller's speed in the tail, `0x35`/`0x36` are the indices the
   selection policy normalises kind-4 events to (`0x2035`/`0x2036`), and `0x10` is the only index
   that can arm the latch. **What index `0x10` is on screen remains unnamed** — no event-index
   name table has been found. The one lead: the battle-mode mount posts actor event `0x2010`
   (kind 2, index `0x10`) when its turbo starts (`0030400A`–`0030403B`); whether that post is the
   word stored here is not traced.

## 15. Evidence

> **The tier column was reworded 2026-09-11**, as in the gambit walk and the target buffer: every
> row read *"static, isolated original code"* while §13 read *"Empty"*, consistent only if the
> phrase meant *the shipped bytes, read*. Now that they have been **run**, `static` (decoded) and
> `executed` (run and compared against a reconstruction) are distinguished. No confidence changes.

| claim | evidence | tier | confidence |
|---|---|---|---|
| the record is `pool + id*0x740` and the id is signed | `0042408A movsx rax, cx`, `00424091 imul rbx, rax, 0x740`, `00424098 add rbx, [rip→022C6F28]`; **executed** with a negative index landing on the record before the pool centre | 1 (static + **executed**) | PROVEN |
| the decay is `0.83f` | `004240D8 mulss xmm0, [rip→00D12434]`, and that dword reads `0x3F547AE1`; **executed** over a 24-call glide compared as bit patterns | 1 (static + **executed**) | PROVEN |
| the release threshold is `0.05f` and the boundary releases | `004240EE movss xmm0, [rip→008F30E8]` = `0x3D4CCCCD`, `00424100 comiss` / `00424108 jb`; **executed** at the value whose decay lands exactly on `0.05f` and one ULP either side | 1 (static + **executed**) | PROVEN |
| five arming conditions | `0042411F`, `0042412B`, `00424132`, `0042413F`, `00424154`; **executed** with each failed alone — **and they do NOT share an exit**, which is what falsified §4's invariant. Conditions 1 and 2 skip the cache entirely | 1 (static + **executed**) | PROVEN |
| the motion blocks are 16-byte mirrors | `00424182 movups xmm0, xmmword ptr [rdi]` at `+0x610` then `00424185 movups xmmword ptr [rbx + 0x620], xmm0`; **executed** with all 32 bytes compared after every call | 1 (static + **executed**) | PROVEN |
| the cache path clears the LIVE flags word | `0042419B and word ptr [rdi + 0xc], ax` with `rdi` from `004240C7 lea rdi, [rbx + 0x610]` | 1 (static + **executed**) | PROVEN |
| a NaN speed caches and a negative zero arms | `0042413F ucomiss` with **both** `jp` and `jne` leaving to the cache path; **executed** with the two cases differing only in the speed's bit pattern | 1 (static + **executed**) | PROVEN |
| the stop-frame counter is sign-extended then compared unsigned | `0042414D movsx` then `00424154 cmp / jb`; **executed** at `−128`, `−1`, `0`, `29`, `30`, `31`, `127` against three time bases | 1 (static + **executed**) | PROVEN |
| there is a fourth stage after every path except servicing | `0042419F`–`00424212`; **executed** on both entry paths, through each subtype branch and each of its three early exits. See §7a | 1 (static + **executed**) | PROVEN |
| `0020E600`'s result is dereferenced unchecked | `004241AB call` then `004241B6 mov rcx, [rax+0xDA8]` with no `test` — **deliberately not executed**: a NULL there is an access violation on both sides and a case that crashes both is not a test | 1 (static) | PROVEN |
| what `0020E600` and `0051B9E0` are | ~~**not established** — supplied as oracles, bodies not read~~ **`0020E600` IS established, and has been since before this row was written** — it is `ImageAddress_ResolveRuntimePointer`, read whole and executed by [the authored-table row lookup](../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md): `mov eax, ecx` / `add rax, [01F83530]` / `ret`, three instructions (§15a). **`0051B9E0` is now read too** (2026-09-13): a 5-byte tail jump to `0051F240`, `PresentationEntryReferenceContainer_ResolveEntryById`, 138 bytes — 2-bit kind field at `+4`, id taken as the LOW 16 BITS scaled by `0x30`, **no capacity or generation check**, cache refresh at `+0x18` when the entry's bit 1 is set, and the returned pointer is the entry's **cache**, not the entry. §7a. | **1** (static, isolated original code) | **PROVEN** |
| `+0x006` is the piece's owner-record link (`-1` = unattached, the latch precondition) and `+0x0CC` is the current render-event word (kind nibble + 12-bit index) | three id-stores `0042F2E6`/`0042F83E`/`0042FAAE` (`movzx eax, word [src]` → `[dst+6]`, beside `src+0x18`→`+0x2C4` and `call 00426E40`); three `-1` detach stores `00421C9C`/`0042CA15`/`0042CC70`; `+0xCC` read as `movsx`/`and 0xFFF` at `004240AE`/`004240B5` and written by the event-selection path (`00424D80` at `00424FAB`) | 1 (static) | PROVEN |
| nothing observed live | — | none | — |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every cited instruction was read at its address, and the two float constants were dereferenced rather
than trusted.

| claim | image |
|---|---|
| the record is `pool + id*0x740`, id **signed** | `0042408A movsx rax, cx`; `00424091 imul rbx, rax, 0x740` |
| the decay is `0.83f` | `004240D8 mulss xmm0, [rip → 00D12434]`, and that dword is `3F547AE1` = **0.82999998** |
| the release threshold is `0.05f` | `004240EE movss xmm0, [rip → 008F30E8]` = `3D4CCCCD` = **0.05000000** |
| a NaN caches, a negative zero arms | `0042413F ucomiss xmm1, xmm0` then **both** `00424142 jp` and `00424144 jne` to the cache path. Unordered → `jp` taken; `−0.0` vs `+0.0` → equal and ordered, so **neither** is taken and the latch arms |
| sign-extended, then compared **unsigned** | `0042414D movsx ecx, byte [rbx+0x457]` — a *byte*, sign-extended — then `00424154 cmp ecx, eax` / `00424156 **jb**` |
| the motion blocks are 16-byte mirrors | `00424182 movups xmm0, [rdi]` / `00424185 movups [rbx+0x620], xmm0`, with `rdi = rbx + 0x610` from `004240C7` |
| the cache path clears the live flags word | `0042419B and word [rdi+0xc], ax` |
| `0020E600`'s result is dereferenced unchecked | `004241AB call 0020E600`, then one unrelated `mov edx, [rbx+0xc4]`, then `004241B6 mov rcx, [rax+0xda8]` — **no `test` between them** |

**The `movsx`/`jb` pair is worth spelling out**, because it is the same shape this sweep has found in
three other contracts: a *negative* stop-frame count sign-extends to a very large unsigned value, so
`jb` is **not** taken and the latch **arms** rather than caching. The signedness of the extension and
the signedness of the comparison disagree, and the behaviour at the boundary follows the comparison.

### The `0020E600` row was stale, and the answer was already in this database

§15 listed `0020E600` as *"not established — supplied as oracles, bodies not read"*. It **is**
established: [`CONTRACT-authored-table-row-lookup`](../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md)
names it `ImageAddress_ResolveRuntimePointer`, reads it whole and executes it. It is three
instructions:

```asm
0020E600  mov eax, ecx                 ; zero-extend the 32-bit reference
0020E602  add rax, qword [01F83530]    ; + the global base
0020E609  ret
```

> **This sharpens the unchecked dereference rather than softening it.** That contract also
> establishes that the global at `01F83530` is ~~**zero for the whole life of the shipped process** —
> `01F83530` has no writer in the image~~ **zero at image load** — so `resolve(x)` is just `(uint32)x`. A zero or small reference
> therefore makes `004241B6` read `[0 + 0xDA8]`: **a near-null dereference with no test in front of
> it**, not merely an unvalidated pointer.
> *Scope restated 2026-09-26 (FABLE, Claude Opus 5.5), on the reconciliation in
> [the authored-table row lookup](../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md) §7:* "zero
> for the whole life" and "no writer in the image" are too strong. `01F83530` is **zero at image load**. One in-image
> store route reaches it: the texture-id table writer, bounded only from above, stores a pointer into the cell at id
> `0xFFFB`. That route is undriven by every id producer read, so zero for the process's life is **supported, not
> proven**. The near-null dereference below holds on the load-time base and on every state that route leaves
> untouched.

~~The row is corrected to **PARTLY ESTABLISHED**; **`0051B9E0` remains genuinely unread**~~ — **superseded 2026-09-13: it is read, see §7a.** It was left
as it stands.

**Not claimed:** no live observation. *(`0051B9E0` is no longer an oracle — 2026-09-13.)*

## 16. Parity plan

`STATE-TRANSITION` — drive a character to a stop and assert bit 0 of `+0x62C` sets, then that it
clears on the call where `+0x624 <= 0.05`.
`CALCULATION` — assert the speed sequence is geometric with ratio `0.83` from the value at arming.
`EDGE-CASE` — a speed of `-0.0f` must arm and a NaN must cache; a `+0x624` of exactly `0.05f` must
release.
`TIMING` — the decay is per call, so a parity run must match call counts, not elapsed time.

**Three of the four are done offline** — see §13. Per-dimension verdicts are declared by the harness
and generated into [`PARITY-STATUS.md`](../_index/PARITY-STATUS.md): `CALCULATION`, `STRUCTURAL`,
`STATE-TRANSITION` and `EDGE-CASE` covered; `TIMING` **not** covered, deliberately — the suite drives
calls and so reproduces the decay, but says nothing about how many calls a real frame makes, which is
the whole of that plan item. `INTEGRATION` and `PRESENTATION` are not covered either: nothing is
drawn and no caller runs.

**Five things a reimplementer must take from this contract that the old plan did not name:**

1. **Conditions 1 and 2 skip the cache.** Sending all five failures to the same place writes the
   record on two paths where the original leaves it alone. See §4's correction box.
2. **Implement the tail (§7a).** It runs on every path except servicing and it can zero the
   caller's speed.
3. **`[rdi + 8]` is the live speed scale after a cache and the cached one after an arm.**
4. **Reproduce the counter wrap.** Clamping the `+0x457` counter correctly at 127, or widening the
   field, changes when characters glide. §10.2 is a defect in the original and it is load-bearing.
5. **Do not add null checks.** Three pointers are dereferenced unguarded — the two parameters and
   `0020E600`'s result. A reimplementation that guards them is more forgiving than the shipped game;
   that may be the right choice, and it is a divergence to record rather than a fix to make quietly.

## 17. Related

- `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md` §"The
  coast-down latch, exactly" — which this formalises, and whose arming list is ~~three of the five~~ all five *(answered: see the record-array page's latch section; 2026-10-02, OPUS)*.
- `_types/types.tsv` — `CharacterRenderRecord`; the mirrored blocks and `+0x61C` were added from this
  work.

## SWE2-EC7-90 update (2026-09-20) - `003AEF20` two-field liveness measured

`003AEF20` (14 B) is the liveness predicate the latch callers
run: 1 only when `dword[rcx]` and `qword[rcx + 0x18]` are both
nonzero - call-free.
Interior anchor `003AEF26` (the second test).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Movement — CLIENT, two edges, and they are the seam the page opens with.**
- The entry point `Movement_ModifyHeadingSpeedForObjectState` (`00424080`) is filed in the movement layer.
- Its caller is `Movement_ComputeDeltaFromHeadingSpeed` (`002E4380`): the latch runs inside the movement delta
  computation.
- It calls this page's resolver `0051B9E0` (`004241BD`).

The delta computation itself is owned by `CONTRACT-heading-speed-to-position-delta`; this contract owns only the
latch it consults.

**Resource — CLIENT, sixteen edges, through three helpers this page reads.**
- **`003AB7F0`, the section resolver the kind-0 arm calls (`0051F25B`, `0051F2A8`), has ten resource callers.**
  They include `ResourceTable_ResolveEntryByIndex`, `ResourceEntry_GetResolvedBasePointer`,
  `ResourceEntry_FindSectionIndexAndOffset` and the `0051FBB0`-`0051FF30` render-record resolvers. It is the resource
  layer's own section addressing, reused here.
- **The event store `00424D80`** (the writer of `+0x0CC`) calls the resource-section helpers `00409090`,
  `00409210`, `00409FA0` and `00409FD0`.
- **The `+0x457` writer `004256E0`** calls `ResourceEntry_GetResolvedBasePointer` and `00409F50`.

The addressing is documented in `resource-section-addressing` and `CONTRACT-resource-entry-tree`; no resource
format is defined here.

*Tier 2: ledger names, sizes and `edges.tsv`, with the call sites this page already prints; no new body read for
this note.*
