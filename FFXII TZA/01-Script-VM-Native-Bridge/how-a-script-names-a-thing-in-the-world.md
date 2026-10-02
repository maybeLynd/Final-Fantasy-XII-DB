---
system: How a script names a thing in the world — and where a treasure chest ends up
category: 01-Script-VM-Native-Bridge
status: AUDITED — the last open box, what a record holds once a map is loaded (UQ-58), answered 2026-09-17: the declared fields, a holder mask at +0x20, a 16-bit stamp, three untouched offsets
owner_layer: Script_VM_Native_Bridge — from the ledger, not inferred from callers
evidence_tier: 1
level: L1
readiness: SEMANTICALLY IDENTIFIED
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 98 addresses cited - 21 data, 27 entry, 40 interior, 9 literal, 1 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-13
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-script-entity-resolver-pass-1 - every static figure reproduces (68/104/240 bytes, the table base and both its ends past SizeOfRawData, the decoder's single caller, all four constants, and x and z dividing by the SAME 10.0); CORRECTED: the eleven users are twenty call sites and ten of them are verb callbacks covering SEVEN named verbs - the five bind verbs plus modelreadsync and unkCall_5cb - with three more verb ids reaching it through the shared puppetbind result; and the unreachable je would return the TABLE POINTER, not null. The game was NOT launched and section 4b is untouched
  crossref_clean: true
  reopened_count: 0
---

# How a script names a thing in the world — and where a treasure chest ends up

## 1. What the player sees

A zone script says *"put the chest here"*, *"attach this character to that spot"*, *"bind the
puppet"*. For any of that to work the script must be able to **name a particular thing in a
particular map** — and it does, with a single number.

The number is not an index. It carries **a slot and a stamp**, and the engine checks the stamp
before it will use the slot. Name something that has been replaced since the script was written and
the engine hands back nothing at all, rather than the wrong object.

And when the thing being placed is a **treasure chest**, its whole position in the world — where it
stands and which way it faces — is **five bytes** of authored data.

## 2. One number, checked before use

`002E97C0` (68 B) turns a script's entity id into a record pointer. **Eleven functions use it, over
twenty call sites**, and **ten of the eleven are verb callbacks covering seven named verbs**:
**`setuptreasure`, `puppetbind`, `bindp`, `bindh`, `bindc`** — the whole *bind* family — and also
**`modelreadsync`** and **`unkCall_5cb`**, which are not bind verbs (§9). Counting verb ids rather
than verbs it is ten, because `003463F0` is the result of `puppetbind`, `puppetbind_41c` and
`puppetbind_41d` alike. It is uncited by any document until now.

```asm
002E97C6  test ecx, ecx / je            ; id 0 is never valid
002E97CC  and  eax, 0x7fff              ; the slot
002E97D1  cmp  eax, 0x80 / jae          ; ...must be under 128
002E97D8  shl  rax, 6                   ; x 64 -- the record stride
002E97DC  lea  rcx, [0215FDA0]          ; the table
002E97E8  mov  edx, [rax + 0x24]        ; the stamp, high half
002E97EB  movzx ecx, word [rax + 0x1a]  ;           low half
002E97EF  shl  edx, 0x10 / or edx, ecx
002E97F4  bts  edx, 0xf                 ; bit 15 is always set in a valid id
002E97F8  cmp  r8d, edx
002E97FB  cmovne rax, r9                ; mismatch -> NULL
```

**The id is the record's own identity, read back and compared:**

```
id  ==  ( u16[rec + 0x24] << 16 )  |  ( u16[rec + 0x1A] | 0x8000 )
slot =  id & 0x7FFF,  and the slot must be < 128
```

> **This is a generation-checked handle.** The low half carries the slot with **bit 15 set as a
> tag**; the high half is a stamp the record keeps at `+0x24`. A stale id addresses a live slot and
> **fails the comparison**, so the caller gets `NULL` rather than somebody else's object.

**The table is 128 records of 64 bytes at `0x0215FDA0`** — 8,192 bytes, and it is **past the end of
`.data`'s file image**, so it is empty in the executable and built at load. Nothing static can say
what is in it.

> **`002E97E6 je` is unreachable.** It tests the flags from `add rax, rcx`, and `rcx` is a fixed
> non-zero table base, so the sum is never zero. Compiler output, reproduced here because a
> reimplementation that omits it is still correct and one that *acts* on it is not.

## 3. A treasure's place in the world is five bytes

`setuptreasure` (verb `0x2BE`, handler `00355210`, 240 B) is the one caller of `002FAF60` (104 B) —
the decoder is **not shared**, it belongs to this verb.

```asm
002FAF60  movsx eax, word [rcx + 4]     ; X, signed 16-bit
002FAF6B  divss xmm0, [008F8180]        ;   / 10.0
002FAF73  movss [rdx], xmm0
002FAF77  movsx eax, word [rcx + 6]     ; Z, signed 16-bit
002FAF7B  mov dword [rdx + 4], 0        ; Y = 0
002FAF82  mov dword [rdx + 0xC], 0x3F800000   ; W = 1.0
002FAF90  divss xmm0, [008F8180]        ;   / 10.0
002FAF98  movss [rdx + 8], xmm0
002FAF9D  movzx eax, byte [rcx + 8]     ; the facing
002FAFA1  and  eax, 0x3F                ;   low SIX bits
002FAFA4  neg  eax
002FAFB2  divss xmm0, [008F6D54]        ;   / 60.0
002FAFBA  mulss xmm0, [01CEBC78]        ;   x 2*pi
002FAFC2  movss [r8], xmm0
```

**Every constant resolved with a tool:** `008F8180` = `10.0`, `008F6D54` = `60.0`,
`01CEBC78` = `6.2831855` (2π).

```
x       = (int16)spot[+0x04] / 10.0
y       = 0.0                              always -- the chest is placed on the plane
z       = (int16)spot[+0x06] / 10.0
w       = 1.0
heading = -( spot[+0x08] & 0x3F ) / 60.0 * 2*pi     radians
```

> ### `spot` is NOT the entity record — corrected 2026-09-08 by a live read
>
> An earlier revision of this section named these offsets `rec[...]`, which reads as the record
> `002E97C0` returns. **It is a different object**: the decoder is called with the result of
> `002650B0`, and the entity record's `+0x00` and `+0x08` are **linked-list pointers**, proven by
> reading the table in a live process (§4b). Same offsets, different structure — and naming them
> `rec` in a formula was an error that a reimplementer would have followed straight into a crash.

> ### The position is in tenths, and the facing is one of sixty
>
> **`x` and `z` are signed 16-bit tenths of a world unit** — a range of ±3276.7 with a resolution of
> 0.1. **`y` is not stored at all**; it is written as zero.
>
> **The facing is six bits divided by sixty.** Codes `0..59` step the full circle in **exactly 6°**;
> codes `60..63` are representable and divide past a whole turn. **A six-bit field with a
> sixty-value range** — the two do not match, and that is what the bytes say.

## 4. What `setuptreasure` does, in order

```c
void setuptreasure(void *ctx /*rcx*/, Actor *actor /*rdx*/, int32_t *args /*r8*/)
{
    Record *rec = ScriptEntity_Resolve(args[0]);     /* 002E97C0 */
    if (!rec) { FUN_0026E060(); return; }            /* the not-found path */

    void *spot = FUN_002650B0(FUN_002640C0(), ctx, args[2]);   /* args[2]: `[rbx+8]` */
    FUN_0026A320(actor, 1);

    FUN_002FAF60(spot, &pos, &heading);              /* the five bytes, decoded */
    FUN_0026AF80(actor, pos.x, pos.y, pos.z);        /* place it            (Movement) */
    Actor_SetFacingHeading_Variant1(actor, heading); /* 0026B620            (Movement) */
    Actor_SetDesiredMovementHeading(actor, heading); /* 0026A0D0            (Movement) */
    FUN_0026DAC0(actor, -1.0f);                      /* 01CEBC9C = -1.0 */
    FUN_002E28E0(actor, rec);                        /* bind the record, 2,026 B */
    FUN_002EC5B0(actor, 0x10);                       /* a mode word         (Movement) */
}
```

**The facing is set twice**, through two different named entry points — `Actor_SetFacingHeading_Variant1`
and `Actor_SetDesiredMovementHeading` — with **the same value**. A chest is placed already pointing
where it will stay, with no turn to play out.

## 4b. The table, read live — 128 slots on a free list

Read in a running process at the **title screen**, with the harness's controls passing.
[`EXP-003`](../_experiments/EXP-003-script-entity-table.md).

**All 128 records are pre-initialised, and every one self-validates**: `+0x1A` holds the slot's own
index, so `id = 0x8000 | slot` resolves for all 128 of them. **The stamp at `+0x24` is `0` in every
record** — one distinct value across the whole table.

**Only nine byte offsets differ between the 128 records**: `0..3`, `8..11`, and `26`. Everything
else is identical, and the pattern is unambiguous:

```
slot 0   +0x00  00 00 00 00 ...   +0x08  e0 fd 15 02   -> 0x0215FDE0 = slot 1
slot 1   +0x00  a0 fd 15 02       +0x08  20 fe 15 02   -> 0x0215FDA0 = slot 0, 0x0215FE20 = slot 2
slot 127 +0x00  20 1d 16 02       +0x08  00 00 00 00   -> 0x02161D20 = slot 126, and NULL
```

> **`+0x00` is `prev` and `+0x08` is `next`.** The 128 records are chained into a **doubly-linked
> list**, head at slot 0 with a null `prev` and tail at slot 127 with a null `next` — **the entire
> pool, free.** Which is exactly what a table should look like with no map loaded.

| offset | at the title screen | reading |
|---|---|---|
| `+0x00` | pointer to the previous record | `prev` |
| `+0x08` | pointer to the next record | `next` |
| `+0x1A` | the slot's own index, 0–127 | the handle's low half |
| `+0x1E` | `0xFFFF` in all 128 | ~~unknown, uniform~~ the sub-record index, `0xFFFF` none *(answered: `002EB625`–`002EB63D` index the 0x120-byte table at `02161DA0` with it; the 2026-09-18 declaration below; 2026-10-02, OPUS)* |
| `+0x24` | `0` in all 128 | the handle's high half |
| everything else | zero | unread |

**The pool is fixed at 128 and the records are 64 bytes** — so a map can name **at most 128
entities**, and that is a hard limit rather than a soft one.

> **What this does NOT establish:** that `+0x24` increments. The resolver's *compare-before-use* is
> proven from the code; **that the stamp ever changes is not observed** — one reading, one value.
> Calling it a "generation" is a reading, and it is labelled as one.
> *Superseded 2026-09-14 (FABLE, UQ-59): the increment is in the code, in both the allocator and the release. See §6.*

### Declared in the store — 2026-09-18 (SWE2-STRUCT-NAMEBINDING-ENTRY)

The 128-entry table is now a store type: **`NameBindingEntry`** (`0x40`), `PARRAY 0x0215FDA0
stride=0x40 count=128`. It is what `SecondaryContext`'s `boundRecord` (`element +0x08`) points at.
Beyond the link/stamp fields above, the allocator (`002E25E0`) and release (`002E9360`) bodies add:
`+0x10` auxHandle (released through `00369800` when nonzero), `+0x14` boundId (the key every
find-by-id walk compares), `+0x18` stateFlags (bit 1 = ready, `002E4C20`), `+0x19` pinFlags
(bits 0-1 gate cleanup, `002E3E0B`), `+0x1C` refcount, `+0x1E` subTableIndex (into the
`0x120`-stride table at `02161DA0` — which begins exactly where the 128 × 0x40 span ends),
`+0x28` requestMask / `+0x2C` readyMask (per-selector bits set by `002EB9D0`), and `+0x30`/`+0x34`/`+0x38`
subResourceIds (released one by one through `003A0F80`).

### The `+0x1E` sub-record is declared too — 2026-09-18 (SWE2-STRUCT-NBE-SUBTABLE-RECORD)

`subTableIndex` selects into **`NameBindingSubRecord`** (`0x120`), `PARRAY 0x02161DA0
stride=0x120 count=32` — the stride appears as `lea rxx,[rax+rax*8]; shl 5` in all nine
validated accessors, and the count is the init loop's `cmp r8d,0x20` bound (`002EA3B9`)
and the `002E6570` reset sweep's. Every accessor validates `subrec+0x5C == entry+0x24`
before touching the record — the generation-stamp defence — and `002EAEB0` re-stamps the
sub-record when it re-lists the owner. The allocator `002E2660` pops the free head
`0215FD70`, cross-writes the two indices (`sub+0x20` slot → `entry+0x1E`; `entry+0x1A`
→ `sub+0x22` owner slot), copies the stamp to `+0x5C`, and zeroes both 32-lane arrays.

The record is a per-binding **bit-channel state**: three source masks `+0x24` registered /
`+0x28` requested / `+0x34` preRegistered are OR'd into the "permitted" union; `+0x2C`
serviced is set by the teardown `002EAFA0` and cleared by the request `002EB690`;
`+0x38`/`+0x3C`/`+0x40` are the live masks (written by-name `002ECAB0` and by-entry
`002ECA30`, read `002E9C60`/`002E3F00`/`002EB890`), `+0x44` a one-shot latch
(`002ECBA0`), `+0x48..+0x57` a 128-bit group bitset (`002EB690` writes `1<<bit` into
`+0x48 + group*4`), `+0x60..+0xDC` the 32-lane value-id array guarded by `+0x24`
(consumed by `002EE1D0` → `CharacterRenderRecord +0x42C/+0x430`, `002E4E50`, and the
`002ECBE0` walk → `0036C5D0`), and `+0xE0..+0x11F` the 32-lane per-bit refcount array
(`002EB690` +=delta, `002EB890` decrements; at ≤0 the bit is re-zeroed if still live in
`+0x38|+0x3C` else torn down via `002EAFA0`). The record is doubly-linked twice: primary
`+0x00`/`+0x08` on heads `0215FD68`/`0215FD70`/`0215FD80` (`002EB690` migrates a record
to `0215FD80` the first time an unpermitted bit is requested) and an embedded node
`+0x10`/`+0x18` on head `0215FD90` (`002EAFA0` pushes when a registered bit is serviced).
Owner release `002E9360` runs `002EAFA0` over all 32 bits. `+0x30` and `+0x58` stay
UNRESOLVED (allocator zero only); `+0x3C`'s writer is not among the 16 RIP-relative
referencers — likely a computed-base write.

## 4c. The `002E28E0` exclusive subtree — all 11 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the record bind **11 frontier functions**. Every member body
was disassembled from the shipping image within its declared extent (2026-09-14). This answers
UQ-60's open half: **~~the fourteen keyed values land~~ thirteen of the fourteen keyed values land *(corrected 2026-10-02, OPUS: `0x09042A2E` is fetched at `002E2EE5` and its result is never used before the next call, `002E2EEA`–`002E2EF2`; UQ-60's answer)* in the actor's `+0xB8` steering record, the
`+0xC0` render link, and the render record itself** — `0x09000606` → `+0xE0`; `0x09000707` × a
`.rdata` constant → `+0xE4` (pushed through `002E86B0` by `00263640`); `0x09001F20`/`0x09002021`
→ `+0x98`/`+0x9C` via `0026AA30`; `0x09001D1E` → `00269E60`; `0x600A1244`'s integer → `+0x151`
bit 7 via `0026AF40`; the bit15-selected pair `0x01002D4F`/`0x01002E50` (or `0x01002143`/
`0x01002244` when the field bit is clear) → `0026B2E0`; and `0x09002322`/`0x09002423`/
`0x09002524` × ~~`30.0f`~~ **`50.0f` (`008F3130`, loaded at `002E2F06`)** become three frame counts for `0026A370`
*(corrected 2026-09-14, FABLE: the `30.0f` at `008F8D80` is loaded at `002E2B0A`–`002E2B3B` on the render-record
fallback path, not for these counts; `0x09002322` → `edx`, `0x09002524` → `r8d`, `0x09002423` → `r9d`,
`002E2F9A`–`002E2FA5`)*. Around them the bind sets
`rec[4] = [rbx+0x14]` and `rec[8] = rbx`, mirrors record bytes into the render record
(`+0x10>>4` → `+0xC1`, `+0x14F>>3` → `+0x413`, `+0x150` → `+0x40C`), back-links the actor at
render `+0x108`, and refreshes position/visibility.

| cluster | members | role | interior |
|---|---|---|---|
| binder | `002E28E0` (2,026 B) | the bind itself — links `[actor+0xC0]`'s render record, fills `+0xE0`/`+0xE4`/`+0x98`/`+0x9C` and the three frame counts from the fourteen keys, then the position/visibility tail | `002E29E9` (`mov byte [rcx+0xC1], dl` — first render-field mirror) |
| steering sinks | `00263640` (31 B), `0026AA30` (34 B) | kind-`0x60` gates: `00263640` loads `rbp+0xE4` into `xmm1` and tail-jumps `002E86B0`; `0026AA30` stores `xmm1`/`xmm2` at `rbp+0x98`/`+0x9C` | `00263651` (`movss` of `+0xE4`) / `0026AA41` (`movss` to `+0x98`) |
| record flag | `0026AF40` (36 B) | clears bit 7 of `[actor+0xC0]+0x151`, then sets it iff `edx≠0` — the `0x600A1244` flag | `0026AF4C` (`and byte [r8+0x151], 0x7F`) |
| bind prep | `002EA2A0` (120 B) | computes `edx = ((rec+0x14F>>1)&1) | (rec+0x12≥0x10)` → `00426C90` on the render record when ready, then `00263A30` with the actor's id/kind | `002EA301` (`call 00426C90`) |
| flagged pair setters | `003E3570` (17 B), `003E36A0` (17 B) | `or [rcx], 0x100` + `xmm1`/`xmm2` → `+0x18`/`+0x1C`; `or [rcx], 0x80` + pair → `+0x10`/`+0x14` — dirty-flagged float-pair writes | `003E3576` / `003E36A6` |
| render fronts | `003E6BF0` (12 B), `003E6BE0` (12 B) | `+0x580`-biased fronts tail-jumping the pair setters — write render `+0x590`/`+0x594` (flag `0x80`) and `+0x598`/`+0x59C` (flag `0x100`) | `003E6BF7` (`jmp 003E36A0`) / `003E6BE7` (`jmp 003E3570`) |
| slot init | `003E7500` (149 B), `004700C0` (23 B), `0051E140` (39 B) | `003E7500` indexes the `0x150`-stride slot array at `02B59D80` (index from `0031B750` of `[actor+0x30]`): sets `+0`=1/`+4`=render id/`+8`=0, back-links the slot index at render `+0x6A4`, memsets `+0xC0`×`0x80`, then `004700C0` inits the `+0x20` sub-record (`+0x10`=id, `0xFFFF` sentinel) and `0051E140` the `+0x70` sub-record (six `0xFF`/`0xFFFF` sentinels) | `003E755A` (`mov [r8+0x6A4], edx` — the back-link) / `004700D3` (`mov [rcx+0x10], edx`) / `0051E152` (`mov word [rcx+0x19], 0xFF`) |

## 5. Modding notes

- **A chest's spot is five bytes**: two `int16` tenths and one byte whose low six bits are the
  facing. Move a chest by editing `+0x04`/`+0x06`; turn it with `+0x08`.
- **Height is not authored.** `y` is written as `0.0` every time, so a chest cannot be raised by
  this path — whatever puts it at the right height happens elsewhere.
- **A facing code of 60–63 is past a full turn.** `60/60 × 2π` is exactly one revolution; the
  authoring tool presumably never emits them, and the engine does not clamp.
- **Entity ids are checked against the record's own stamp.** Reusing an id whose stamp has moved
  returns `NULL`, not the wrong object. **At the title screen every stamp is `0`**, so
  `0x8000 | slot` resolves for all 128 slots and the check protects nothing yet.
- **A map can name at most 128 entities.** The pool is fixed, 64 bytes per record, and the
  resolver refuses any slot ≥ 128.
- **Bit 15 of a valid id is always set.** An id with that bit clear can never resolve.

## 6. What is not known

- [x] ~~**UQ-58.** **What a record holds once a map IS loaded.** §4b establishes the empty state; the 46~~
      bytes that are zero throughout at the title screen are still unread. `ER-1`.
      ***ANSWERED 2026-09-17 (FABLE): a bound record is the `NameBindingEntry` the store declares, plus a holder mask at `+0x20`, a stamp that is sixteen bits wide, and three offsets nothing touches.** The 2026-09-18 declaration on this page names `+0x00` prev, `+0x08` next, `+0x10` auxHandle, `+0x14` boundId, `+0x18` stateFlags, `+0x19` pinFlags, `+0x1A` own slot, `+0x1C` refcount, `+0x1E` subTableIndex, `+0x24` stamp, `+0x28` requestMask, `+0x2C` readyMask and `+0x30`..`+0x3B` the three subResourceIds; the allocator `002E25E0` zeroes exactly `+0x10`, `+0x14` (the id), `+0x18`, `+0x1C`, `+0x1E` (set to the free index), `+0x20`, `+0x26`, `+0x28`..`+0x2F`, `+0x30`..`+0x3B` (`002E25FA`..`002E262B`). What that leaves: **`+0x20` is a word of per-selector holder bits.** `002EB540` inserts the entry into the list headed at `0215FD78`, sets pinFlags bit 3 and sets bit `selector` of the word (`bts`, `002EB5B1`..`002EB5B9`); `002EAE20` does the same insertion and sets bit 0 (`002EAE87`); `002E3E20(selector, direction)` walks the list headed at `0215FD58` and clears that bit when the direction is positive or the whole word when it is negative (`002E3E50`, `002E3E58`), then, when refcount `+0x1C` is not positive, the word is empty and pinFlags bits 0..1 are clear, calls the re-lister `002EAEB0` (`002E3E5C`..`002E3E6E`): an entry is held while any selector's bit is up, and released when the last one drops. `002E6EB0` also packs the word into the high half of the tag it hands the resource requester `0032E620` (`002E6FC3`..`002E6FCA`). **The stamp is sixteen bits.** The allocator, the release `002E9360` (`002E944E`) and the re-lister `002EAEB0` (`002EAEFF`) each increment the dword `+0x24` and then zero the word `+0x26`, so the high half of the dword is always 0 and the stamp is the u16 that fits the handle's high half. **`+0x1B`, `+0x22` and `+0x3C` are touched by nothing** in the module `002E2000`..`002EC000`: every `+0x22` and `+0x3C` access there belongs to the `0x120`-byte sub-record (`002E9470`, `002E3F00`, `002E4000`, `002EB890`, which read `+0x5C` beside them) or to another object (`002E6900`, `rbx-0x10`), and `+0x1B` has no access at all. Static, module-wide offset census and the bodies read.*
- [x] **Which end of the free list the allocator pops, and therefore whether `+0x00` is next or prev.** `EW-3`.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (EW-3): `+0x08` is next and `+0x00` is prev, as
  `ER-1` named them. Both observations are right; the live order is what one allocate-then-free cycle leaves.*
  - **The allocator** `002E25E0` pops the head pointer `[0215FD60]`. The new head is the popped record's **`+0x08`**
    (`002E25F6`, `002E2618`). It unlinks the record through `+0x08` and `+0x00` and increments the stamp `+0x24`
    (`002E25EC`).
  - **The release** `002E9360` **pushes** at the same head: `[rec+0x00] = 0`, `[rec+0x08] =` old head, old head's
    `+0x00` = rec, head = rec (`002E943C`–`002E945E`). It also increments `+0x24` (`002E944B`).
  - **Initialisation** (`002EA320`) links slot `k`'s `+0x00` to `k−1` and its `+0x08` to `k+1`, with head = slot 0
    (`002EA3CB`–`002EA3EC`, `002EA417`). That is `ER-1`'s order.
  - **Why the live table is reversed.** If map load allocates the records from the head (slot 0, 1, 2, …) and releases
    them in the same order, each release pushes on top of the last. The head ends at slot 127, every `+0x08` points one
    slot lower, every `+0x00` one higher, and slot 0's `+0x08` is null. That is exactly EXP-007's read.
  - **The stamp does change.** Every allocation and every release increments `+0x24`, which bears on the next box.
- [x] ~~**UQ-59.** **Whether the stamp at `+0x24` ever changes.** Observed once, `0` in all 128.~~
  **Answered 2026-09-14 (FABLE): yes. It changes on every allocation and every release. The reading of `0` is the
  pool before its first allocation.**
  - **The code.** The pool head `0215FD60` has exactly three writers image-wide:
    - the initialiser `002EA320`;
    - the allocator `002E25E0`, which runs `inc dword [rec+0x24]` at `002E25EC`;
    - the release `002E9360`, which runs `inc dword [rec+0x24]` at `002E944B`.
    No other instruction in the image writes it `rip`-relative.
  - **The title read is the initialiser's order.** EXP-003 recorded slot 0 with a null `+0x00`, `+0x08` pointing to
    slot 1, and slot 127 with a null `+0x08`. That is what `002EA320` builds, and the initialiser never touches
    `+0x24`. All-zero stamps are therefore what the pool reads before anything has been allocated from it.
  - **The in-world read cannot be the initialiser's order.** EXP-007 recorded slot 0 with a null `+0x08`, and slot
    `k`'s `+0x08` pointing to slot `k−1`. Of the three head writers, only the release produces that order. It pushes
    each record onto the head, so slot 0 was pushed onto an empty list and every later slot on top of the one
    before. A record reaches the release only after the allocator has taken it. So each of those records has had its
    stamp incremented at least twice since the title screen.
  - **Not read live:** the in-world stamp values themselves, which EXP-007 did not label. The stamp is a full
    `dword`: the release compares it as one (`002E949A`). The allocator clears the word at `+0x26` right after the
    increment (`002E2613`), so only the low 16 bits can carry past an allocation.
- [x] ~~**UQ-60.** **What `002E28E0` does with the record.** 2,026 bytes, unread.~~
      **ANSWERED 2026-09-14 (FABLE), by §4c (SWE2-FRONTIER) with two corrections from the body.**
      §4c reads where the keyed values land: steering record `+0xB8`, the `+0xC0` render link, and the render record.
      Re-reading the fetch sequence `002E2E6F`–`002E2FA5` against it:
      - `0x09001F20` / `0x09002021` → `0026AA30` (`+0x98` / `+0x9C`).
      - The bit-15-selected pair → `0026B2E0`.
      - `0x09001D1E` → `00269E60`.
      - `0x600A1244` (through the integer getter `003E6310`) → `0026AF40`.
      - `0x09002322` / `0x09002423` / `0x09002524`, each × **`50.0`** (not `30.0`), → `0026A370`.
      - **`0x09042A2E` is fetched and discarded.** Its `003E6150` call at `002E2EE5` is followed directly by the
        next key's integer call (`002E2EEA`–`002E2EF2`). No store of `xmm0` comes between them, so the value is
        never used.

      So thirteen of the fourteen keys have a destination, and the fourteenth is a dead read.
      **SHAPE READ 2026-09-13 (OPUS): its dominant activity is fetching FOURTEEN keyed parameters
      for ONE object, and it is by far the heaviest user of the accessor that does it.**
      `003E6150(u16 id, u32 key)` resolves an object by the 16-bit id through `002EDBD0` — returning
      **`0.0f` when the id resolves to null** — and then selects which parameter to return by
      comparing the 32-bit key against **30 distinct constants**. It is called from **11 functions
      over 28 sites image-wide, and `002E28E0` is 12 of those 28** — 43% of every use in the image.
      **The id is the same for all twelve; the KEY is what varies.** The register holding the id
      (`si`) is unchanged across the calls, while `edx` is loaded with a fresh literal each time:
      `0x09000606`, `0x09000707`, `0x09001F20`, `0x09002021`, `0x01002D4F`, `0x01002E50`,
      `0x01002143`, `0x01002244`, `0x09001D1E`, `0x09042A2E`, `0x600A1244`, `0x09002322`,
      `0x09002423`, `0x09002524`.
      **The key is opaque and must stay that way.** The pairs look decomposable — several are
      consecutive (`1F20`, `2021`, `2322`, `2423`, `2524`) — but `003E6150` never shifts or masks it:
      it compares the **whole 32-bit value** (`cmp ebx, 0x9001112`, `cmp ebx, 0x9000101`, …). Reading
      structure into those bytes would be inventing a format the code does not use.
      **Its other data source is the character render system.** `002E28E0` adds `[022C6F28]` to
      offsets at six sites; that global is written by `CharacterRenderSystem_AllocateAndInitialize`
      and `00332440`, both `Presentation`, and read by **370 functions** — it is the render system's
      base pointer, not something private to this path. It also writes `01F7F508` twice and uses the
      `.rdata` constant `30.0f` at `008F8D80` *(answered: only on the render-record fallback path, `002E2B0A`–`002E2B3B`; the three frame counts use `50.0f` at `008F3130`, `002E2F06`; 2026-10-02, OPUS)*.
      **NOT read: what it does with the fourteen values.** The body is 2,026 bytes and only its
      skeleton is established here — the accessor it leans on, the object it asks about, the count and
      identity of the keys, and the systems it touches. **That is a shape, not a semantics**, and the
      bullet stays open until the fourteen destinations are read *(answered: read by §4c and the UQ-60 answer above; 2026-10-02, OPUS)*.
- [x] ~~**What `002EC5B0(actor, 0x10)` sets.** 31 bytes, `Movement`, unread.~~
      **READ 2026-09-13 (OPUS): it sets the movement body's `maskA`, and it OVERWRITES it.** All
      31 bytes are a two-hop guarded store:

      ```asm
      002EC5B0  mov  rax, [rcx + 0xC0]      ; actor -> movement slot
      002EC5B7  test rax, rax / je ret
      002EC5BC  mov  rax, [rax + 0x138]     ; -> the allocated movement body
      002EC5C3  test rax, rax / je ret
      002EC5C8  mov  [rax + 0x110], edx     ; maskA = arg
      002EC5CE  ret
      ```

      `+0xC0` then `+0x138` is the movement body chain that
      [`CONTRACT-movement-body-pool.md`](../06-Movement-And-Navigation/CONTRACT-movement-body-pool.md)
      specifies — *"`+0x138` holds the allocation's result"*, *"every consumer guards each hop"* — and
      this function is one of those consumers, guarding both. `+0x110` is named in
      [the pool page](../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md)'s
      field map as **`u32 maskA`** (beside `+0x114 maskB`).
      **So `002EC5B0(actor, 0x10)` writes `maskA = 0x10`.** The instruction is `mov`, **not `or`** —
      it replaces the whole mask rather than setting bit 4, so any other bit standing in `maskA` is
      cleared by this call. A reconstruction that implemented it as a bit-set would silently preserve
      state the engine drops.
      **It is safe on an actor with no body.** Both hops are null-guarded and the function simply
      returns, so calling it before allocation is a no-op rather than a fault — which is what makes it
      callable from a script verb path.
- [x] ~~**What `002650B0` returns** — the object the placement is decoded from — and why
      `args[2]` selects it. `args[1]` is not read on this path at all.~~
      **ANSWERED 2026-09-13 (OPUS): it returns `base(selector) + offset`, where `args[2]` carries
      BOTH — a 3-bit pool selector in the top byte and a 24-bit byte offset below it.** The whole
      function is one packed-field decode:

      ```asm
      002650B6  mov  r10, [rcx]            ; the object's first field, kept for arm 3
      002650B9  mov  eax, r8d
      002650BC  sar  eax, 0x18             ; args[2] >> 24
      002650C2  and  eax, 7                ; selector 0..7
      002650C8  cmp  eax, 5
      002650CB  ja   0026516C              ; 6 and 7 are the default arm
      002650DA  mov  r8d, [rcx + rax*4 + 0x145180]   ; the jump table at 00265180
      002650E5  jmp  r8                    ; RVA + image base
      ```

      Every arm then does the same two instructions — `and eax, 0x00FFFFFF` and `add rax, base` — so
      the low 24 bits are a **byte offset into whichever pool the selector names**:

      | `args[2] >> 24 & 7` | base the offset is added to |
      |---:|---|
      | 0 | `[obj + 0x48]` |
      | 1 | `[obj + 0x40]` |
      | 2 | the result of calling the **function pointer at `[obj + 0x98]`** with `obj` |
      | 3 | `[obj] + [[obj] + 0x40]` — a base reached through the object's first field |
      | 4 | `[obj + 0x58]` |
      | 5 | `[obj + 0x60]` |
      | 6, 7 | **zero** — `xor ecx, ecx`, so the offset is returned as an absolute value |

      **So "the object the placement is decoded from" is not one object.** It is one of six pools
      hanging off the same host — four plain pointer fields, one obtained by an indirect call, one
      two levels deep — and `args[2]` names the pool and the position within it in a single dword.
      That is why `args[1]` is never read on this path: **the selector and the offset both live in
      `args[2]`.**
      **The default arm is not an error path.** Selectors 6 and 7 return the raw 24-bit value with a
      base of zero, which is a well-formed answer for a caller passing an absolute rather than a
      pooled reference — so a reconstruction must implement it rather than assert.
- [x] ~~**UQ-61.** **What the `-1.0f` at `0026DAC0` means.**~~ **Answered 2026-09-14 (FABLE):** it makes the chest **a body that other bodies are pushed off, and that is never pushed itself**.
      - **What the setter writes.** `0026DAC0(actor, v)` (68 B) stores `v` at `+0x148` of the actor's `+0xC0` object, then copies it to `+8` of the movement body that object links at `+0x138`. That `+8` is the separation weight of [the movement body pool](../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md) §2.7.
      - **How the separation pass treats a negative weight.** The contact resolver reads both bodies' weights (`00315017`, `0031502A`). It negates them only when **both** are negative, and sets both to 1 when they are equal and zero (`0031501D`–`0031506E`). A single negative weight therefore reaches the weight rule `00314E10`, whose last step gives that body a share of 0 (`00314E96`–`00314EA3`, UQ-104). The other body takes the whole separation.
      - **The mask agrees.** The verb's next call, `002EC5B0(actor, 0x10)`, gives the chest priority bit 4 in the same rule, so it outranks a party member's bit 2 before the weight clamp is even reached.
      - **Other callers.** −1.0 is passed at one other site (`00301037`). Two script-facing entries pass an integer operand as a float (`0034DEC3`, `0050E830`), and three computed callers pass derived values.
- [x] ~~**UQ-62.** **Whether the other four `bind*` verbs decode a placement too.**~~ They share the resolver and
      **not** the decoder — `002FAF60` has exactly one caller.
      **CONFIRMED AND ENUMERATED 2026-09-13 (OPUS): the bind is shared five ways, the decode is
      shared none.**
      **`002FAF60` really does have exactly one caller** — `00355210` — and it is not reachable any
      other way either: its 64-bit pointer value and its 32-bit RVA each occur **zero** times
      anywhere in the file, so no table installs it and no `lea` takes it.
      **The record bind `002E28E0` has five callers**, and four of them are installed as function
      pointers in `.data` — the shape of a handler slot:

      | caller | size | installed as a pointer at | calls the decoder? |
      |---|---:|---|---|
      | `00355210` | 240 B | `.data@01EF2EE0` | **yes** |
      | `003409F0` | 340 B | `.data@01EED890` | no |
      | `00342640` | 163 B | `.data@01EED8A0` | no |
      | `0050D810` | 73 B | `.data@01F26740` | no |
      | `0037B4D0` | 3,175 B | — *(not installed anywhere)* | no |

      **So every caller of the bind reaches it, and exactly one of them decodes a placement first.**
      The bullet's inference — *"they share the resolver and NOT the decoder"* — is correct, and it is
      now a census rather than an inference: the decoder's caller set is `{00355210}` by direct call
      **and** by indirect reachability, which the original claim did not test.
      **One caller is not a dispatched verb.** `0037B4D0` (3,175 B) appears in no pointer slot; it
      calls the bind directly. **So "the other four bind\* verbs" is four only if that one is counted
      among them, and it is not installed the way the other four are** — worth settling before the
      count is quoted as four handlers.
      **Answered 2026-09-14 (FABLE): no. Of the bind verbs, only `setuptreasure` decodes a placement.** The count
      question above is settled by the verb-table join further down this page, not by the bind's caller list.
      - **The bind verbs** are `bindp`, `bindh`, `bindc` and `puppetbind`. Their six callbacks are `003409F0`,
        `00342640`, `00345A60`, `00344550`, `00344200` and `003463F0`.
      - **None of the six decodes a placement.** None calls the decoder. None contains a `divss`, `mulss` or
        `cvtsi2ss`, and none contains the `0x3F` facing mask. Only one `xmm` register is touched across all six: a
        `movaps` in `bindp`'s result.
        - The decoder itself divides x and z by `10.0`, masks the facing with `0x3F`, divides by `60.0` and
          multiplies by `2π`. Those are the operations searched for.
      - **Their direct callees don't either.** The resolver, eight small helpers of 7 to 170 bytes, and the
        111-byte callee of `puppetbind`'s result were all checked. None contains any
        of those instructions.
        - The one larger callee, the 997-byte part-slot function that `bindh`'s and `bindc`'s results share,
          touches `xmm` three times, and none of the three is a divide, a multiply or a conversion.
        - Its 15 callees were not read.
      - **So the difference is real.** The bind verbs attach an entity the script already names. They do not place
        one from authored tenths and a facing byte.
- [x] ~~**UQ-63.** **Any runtime observation of this path.** None exists; the group-table read that answered
      `AY-10` touched a different structure.~~ **SUPERSEDED** (2026-09-14, FABLE; EVIDENCE-STANDARD addendum 2026-09-15bk,
      kind (c)). The resolver's checks are tier-1 static proofs (§7). The table it resolves against has since been read live
      twice: at the title screen (EXP-003, §4b) and in-world (EXP-007). The stamp's movement is shown statically (UQ-59).
      Nothing on the page waits on a further observation of the path.

## 7. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the id is a generation-checked handle | `002E97E8`–`002E97FB`: the record's own `+0x24`/`+0x1A` recombined and compared, `cmovne` to NULL | 1 | PROVEN |
| slot = `id & 0x7FFF`, bounded at 128 | `and eax, 0x7fff` / `cmp eax, 0x80 / jae` | 1 | PROVEN |
| bit 15 is always set in a valid id | `bts edx, 0xF` before the comparison | 1 | PROVEN |
| the table is 128 × 64 bytes at `0x0215FDA0` | `shl rax, 6` and the bound; base resolved with a tool | 1 | PROVEN |
| eleven users, ~~five of them named verbs~~ seven named verbs over twenty sites *(corrected 2026-10-02, OPUS: `retool.py callers 002E97C0`: eleven functions, twenty sites, ten of them verb callbacks; §9)* | `edges.tsv` with EH callers excluded, joined to the verb table | 1 | PROVEN |
| `x`/`z` are int16 tenths, `y` is always 0 | `movsx` + `divss` by `10.0` at `008F8180`; `mov dword [rdx+4], 0` | 1 | PROVEN |
| `heading = -(n & 0x3F)/60 × 2π` | `and 0x3F` / `neg` / `divss [008F6D54]=60.0` / `mulss [01CEBC78]=2π` | 1 | PROVEN |
| the decoder is treasure-only | `002FAF60` has exactly one caller | 1 | PROVEN |
| the facing is set twice with one value | `0026B620` and `0026A0D0` both take `[rsp+0x20]` | 1 | PROVEN |
| the pool is 128 records on a doubly-linked free list | live read: slot 0 null-`prev`, slot 127 null-`next`, every link lands on an adjacent record | 10 | PROVEN |
| all 128 self-validate at the title screen | the resolver's own rule applied to the live table, 128 of 128 | 10 | PROVEN |
| `+0x24` is a generation that increments | `inc dword [rec+0x24]` in the allocator (`002E25EC`) and the release (`002E944B`); the pool head's only three writers are those two and the initialiser; EXP-007's in-world link order is the release's (UQ-59) | 1 | PROVEN |
| what a record holds with a map loaded | **not established** *(answered: UQ-58, 2026-09-17, §6; 2026-10-02, OPUS)* | — | UNKNOWN |
| any runtime observation | **none exists** *(answered: the title-screen read of all 128 records, two rows above, tier 10; 2026-10-02, OPUS)* | — | UNKNOWN |

## 8. Related

- [Verb dispatch and parameter encoding](Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md) — how the verb and its arguments arrive
- [The encoded-id class registry](../00-Engine-Core-Runtime/the-encoded-id-class-registry.md) — a *different* id scheme, in the battle layer
- [Spawn placement and retirement](../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) — placement for a different kind of body

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only. **The game was not launched**: §4b's live read stands exactly as recorded and none of
it is re-tested. `check_already_answered.py` run on the addresses this pass touches.)*

### Every static figure reproduces

| claim | measured |
|---|---|
| `002E97C0` is 68 B, `002FAF60` 104 B, `00355210` 240 B | **68 / 104 / 240** |
| the resolver's asm (§2) | **exact**, instruction for instruction, including `bts edx, 0xF` and the `cmovne` to `r9` |
| the table base `0215FDA0` | `lea rcx, [rip + 0x1E765BD]` at `002E97DC` → **`0215FDA0`** |
| the table is past `.data`'s file image | **both ends are**: `0215FDA0` and its last byte `02161D9F` sit beyond `SizeOfRawData` |
| `002FAF60` has exactly one caller | **1 site, 1 function** — `00355210` |
| `008F8180` = 10.0, `008F6D54` = 60.0, `01CEBC78` = 2π, `01CEBC9C` = −1.0 | **all four resolved from the displacements and read from the image** |
| `x` and `z` both divide by 10.0 | **the same address** for both `divss` — `002FAF6B` and `002FAF90` resolve to `008F8180` alike |
| `00355210` is reached through the dispatch table, not by a call | **0 rel32 callers** |

### ✔ The unreachable `je`, sharpened

§2 notes `002E97E6 je` is unreachable because `add rax, rcx` can never be zero. True — and the
consequence is worth one more line: its target `002E9803` is a **bare `ret`**, so it would return
**`rax`, the table pointer**, not the `r9` NULL the two real failure paths return. A reimplementation
that *acts* on that branch does not merely add a case; it returns a **non-null wrong pointer** where
every other failure returns null. That is why the page is right that omitting it is safe and honouring
it is not.

### ✖ Corrected: seven named verbs, not five — and twenty sites, not eleven

Joining the eleven users to the verb table by `begin` / `poll` / `result` / `arg_handler`:

| verb | id | which slot |
|---|---|---|
| `bindp` | `000C` | poll `003409F0` **and** result `00342640` |
| `bindh` | `00D7` | result `00345A60` |
| `bindc` | `0200` | result `00344550` |
| `setuptreasure` | `02BE` | poll `00354A40` **and** result `00355210` |
| `puppetbind` | `041B` | poll `00344200` **and** result `003463F0` |
| **`modelreadsync`** | `00C0` | poll `00341840` |
| **`unkCall_5cb`** | `05CB` | poll `003418B0` |

**`modelreadsync` and `unkCall_5cb` are not bind verbs**, so *"five of them are named script verbs …
the whole bind family"* both undercounts and mis-characterises: the resolver is the *script entity*
resolver, and a model-read wait uses it too. Three more **verb ids** reach it through one shared
result — `003463F0` serves `puppetbind` (`041B`), `puppetbind_41c` (`041C`) and `puppetbind_41d`
(`041D`) — so ten of the eleven users are verb callbacks and **`0037B4D0` is the only one with no
verb-table row.**

The user count is right; the **site** count is **20**, which the page does not give.

### ○ Two small readings

`002E97E8` is `mov edx, dword ptr [rax + 0x24]` — a **dword** load, not the `u16` §2's formula writes.
The following `shl edx, 0x10` discards the upper half, so the formula's result is the same; but a
record whose `+0x26` is non-zero is read and thrown away, and a reimplementation that declares the
field `u16` is describing the effect rather than the access.

§3's facing arithmetic is exactly as published, and the six-bits-against-sixty observation is worth
keeping: `and 0x3F` admits `0–63`, `divss` by `60.0` then `× 2π` makes 60 a full turn, so
**`60–63` are representable and over-rotate** — by 6°, 12° and 18° past the circle. The engine
does not clamp.

**Not claimed.** Nothing live — **§4b was not re-read and no process was started**, so the free-list,
the uniform `0xFFFF` at `+0x1E` and the all-zero stamp stand exactly as recorded, and `ER-1` and the
"does the stamp ever change" question stay open. `002E28E0`, `002EC5B0`, `002650B0`, `0026DAC0`
remain unread *(answered: the stamp increments, UQ-59 2026-09-14; `002E28E0` read by §4c and UQ-60; the other three read in §6; 2026-10-02, OPUS)*. Whether the other bind verbs decode a placement: the **decoder** still has one caller,
which is the same negative the page gives. Nothing was executed.

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Input — SERVICE.** `00291C80`, owned by that layer, calls this page's `0032E620` at
**`00291D04`**. The entry's first act is to publish its argument into a global
(`0032E634 mov dword […], ecx`), so the call is a **set**, not a query. **The crossing is that
Input drives this page's setter, not that this page owns anything in Input.**

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **Party and CombatAction — CLIENT.**
  - The heading setters `Actor_SetDesiredMovementHeading` and `Actor_SetFacingHeading_Variant1` are shared with
    `PartyControl_ApplyAnalogLocomotionToActor`, a 639-byte Party body and `Battle_ProcessActionTarget`.
  - The 31-byte `002EC5B0` is read by `PartyControl_ApplyAnalogLocomotionToActor` and
    `PartyFocus_ClearCurrentActorIfEligible`.
- **Party and Gameplay — SERVICE.** The 3,175-byte resolver `0037B4D0` asks `PartyRoster_IsFourSlotIndex`,
  `ActorHandle_GetPrimaryFormulaResourceByte26` and `WorldActor_GetDefinitionByte12OrMinus1`.
- **Resource — SERVICE.** `CharacterRenderRecord_RefreshFCPPayloadByRecordId` (`002EDBD0`) finds its section through
  `ResourceEntry_FindSectionPointerByTagAndName`.
- **Audio — SERVICE, not read.** `002E9360` calls a 233-byte Audio-filed body.
- **Movement — CLIENT and SERVICE (89 edges).** 48 inbound (Movement bodies `002E28E0`, `0034A940`, `0037D000` call page-cited `Actor_SetFacingHeading_Variant1` (0026B620), `Actor_SetDesiredMovementHeading` (0026A0D0), `0026AF80`); 41 outbound (page-cited `0037B4D0`, `002E28E0`, `00355210` call Movement bodies `002E28E0`, `002E3110`, `00268380`). Substantive edges include `00263640` is called by `002E28E0`; `00269E60` is called by `002E28E0`; `00269E60` calls `00268380`; `Actor_SetDesiredMovementHeading` (0026A0D0) is called by `0037D000`; the remaining edges run through shared helpers the page cites.
- **Presentation — CLIENT and SERVICE (28 edges).** 10 inbound (Presentation bodies `002E65A0`, `003E6150`, `0046CC70` call page-cited `CharacterRenderRecord_RefreshFCPPayloadByRecordId` (002EDBD0), `0032E620`, `003E6150`); 18 outbound (page-cited `002E28E0`, `00332440`, `00426C90` call Presentation bodies `00426FA0`, `CharacterRenderRecord_RefreshFCPPayloadByRecordId` (002EDBD0), `00427280`). Substantive edges include `002E28E0` calls `00427280`; `002E28E0` calls `Actor_RefreshPresentationVisibility` (002E8FD0); `002E28E0` calls `00426FA0`; `002E28E0` calls `0042FB80`.
- **Save_Load_Settings — CLIENT (1 edge).** 1 inbound (Save_Load_Settings bodies `002EF300` call page-cited `0032E620`). Substantive edges include `0032E620` is called by `002EF300`.
## SWE2-EC7-60 update (2026-09-19) - `002EB9D0`

`002EB9D0` (253 B) is the `+0x28`/`+0x2C` mask setter the script-names page names - `002E9920`/`002ED6F0`. Interior anchor `002EBA0C` (a `002E9920` call).


## SWE2-EC7-60 update (2026-09-19) - `002EB690`

`002EB690` (171 B) is a call-free selector-bit request - `r8d<<cl` into `[r10+rax*4+0x48]` requestMask, `~bit` AND into `+0x2C`, `0215FD68`/`70`/`80` head-pointer swaps. Interior anchor `002EB6C2` (the `or [r10+rax*4+0x48]` mask write).


## SWE2-EC7-70 update (2026-09-19) - `002EB540` NameBindingEntry find-or-create measured

`002EB540` (130 B) measured - **the page's holder-bit claim is exact**:
walks the `0215FD58` then `0215FD78` lists for the entry whose `+0x14`
equals `ecx`; on a miss it allocates through `002E25E0`, pushes the entry
onto the `0215FD78` head (with the old head's `+0` backlink), and ORs
`byte[+0x19]` bit 3 - the pin flag; then `bts word[+0x20], r10b` sets the
selector's holder bit either way.
Interior anchor `002EB5B5` (the `bts ecx, r10d` holder-bit set).
