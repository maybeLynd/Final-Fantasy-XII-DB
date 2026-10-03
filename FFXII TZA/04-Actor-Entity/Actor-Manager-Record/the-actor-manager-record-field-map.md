---
system: The ActorManagerSlot (0x288, five at 02098E10) — a field map from every reached accessor
category: 04-Actor-Entity
status: AUDITED
owner_layer: PrimaryOwner:ActorEntity — the world tick owns the two bytes it tests
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: two enumerations with controls - an absolute-address scan of the five-slot array
    02098E10..02099AB8 (control 02089340, 126 references) and a typed field scan seeded by the
    bound-slot global 02099D70 with argument and return propagation for three hops (control
    002640D0's read of +0x28 after loading the global); the bind ActorManager_BindLoadedDefinitionPayload
    read for the fields it writes through its computed slot pointer
last_reviewed: 2026-09-10
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-actor-manager-record-field-map-pass-1
  last_pass_kind: authored
  crossref_clean: true
  reopened_count: 0
---

# The ActorManager record — a field map from every reached accessor

> Five 648-byte slots at `02098E10` are the actor managers the world tick walks; slot 0 is the
> primary manager that runs the field frame. `OPUS-CONTRA-REC60` was a claim about this record read
> as a claim about the actor storage record. This page lists every offset any reached function
> touches — 57 of them, from 122 functions on two routes — and the bind that
> initialises a slot.

## 1. What the player sees

Nothing directly; the record is the per-manager control block. What it drives is visible: whether
a manager is live (`+0x10` bit 0), whether it runs the fifteen extra sub-steps (`+0x201`), and which
definition payload it is bound to (`+0x00`).

## 2. Native mechanism

### 2.1 How the accessors were found

**Two routes.** The array is at a fixed image address, so most code reaches a slot by an
absolute `[rip + X]` reference into `02098E10 + slot × 0x288` — the absolute-address scan lists
those (offset = `(X − 02098E10) mod 0x288`, slot = the quotient). The *bound* slot is also kept in
the global `02099D70` (written by the bind at `0026C911` and by fifteen other functions), and the
typed scan follows a register loaded from it through `mov` / `lea` / `add`, into callees through
argument registers and back through `rax`; three hops.

| | count |
|---|---|
| bound-slot route: access rows / functions / offsets | 167 / 91 / 50 (72 at the seed, 95 through propagation) |
| array route: references / functions / offsets | 51 / 31 / 17 |
| offsets touched on either route | 57 |

> **These five bound-slot figures are as of this table's authorship and still reproduce, but the TSV beside it has grown since.** §2.6 added the interpreter's argument seed on 2026-09-11 — **27 rows**, taking the file to **194**. Excluding those, the file gives exactly 167 / 91 / 50 / 72 / 95. See the falsification pass for why the `57` is the one number a reader should *not* recompute from the file.
| controls | `002640D0` reads `+0x28` after loading `02099D70` (found); `02089340` for the absolute scan (126 references) |

**What the enumeration cannot see:** indexed forms, pointers stored into other objects, and
anything below the third hop; the array route sees only literal slot addresses, so a function that
computes `02098E10 + i × 0x288` (the bind, `0026C8FE`–`0026C90E`; the tick's slot loop) is cited from
its own read instead.

> **What a census like this cannot see (2026-09-11, OPUS-NOTICE-CENSUSWRITES).** Seeds: the absolute five-slot array and the accessors named in §2.1; the slot's constructors are reached only where they take the slot in an argument register.
> A scan seeded on *accessors* reaches *consumers*: a constructor that builds the record before
> any accessor can return it is reached only if it is seeded on its own. So the **reads** below are
> the well-covered side and the **writes** are under-covered wherever a constructor or an
> index-derived writer sits outside the seeds — do not rest an absence-of-writer claim on this
> TSV alone; pair it with a displacement scan of the candidate writers.

### 2.2 The bind, `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`, 1,330 B)

`rdi = 02098E10 + slot × 0x288` (`0026C8FE`–`0026C90E`), stored to `02099D70` (`0026C911`). It
zeroes the eight qwords `+0x244`–`+0x27C` (`0026C918`–`0026C949`), clears bit 2 of `+0x200`
(`0026C950`), writes the slot index at `+0x28` (`0026C957`) and the payload pointer at `+0x00`
(`0026C95A`), and later fills the pointer block `+0x50` / `+0x58` / `+0x60` / `+0x68`
(`0026CB17`–`0026CB43`) and zeroes `+0x1E0` (`0026CB1F`). **This is the qword write at `+0x60`
that `OPUS-CONTRA-REC60` attributed to the actor storage record**; the storage record's `+0x60` is
its byte free-list head ([the actor storage record](../Actor-Storage-Record/the-record-behind-every-actor.md) §13, §17 CORRECTED).

### 2.3 The field map

Width is the most common operand size at that offset; "w / r / abs" counts distinct functions on the
bound-slot route (writes, reads) and on the array route.

| offset | width | type | name (source) | w / r / abs | writers (bound) | readers (bound) | array-route references |
|---|---|---|---|---|---|---|---|
| `+0x000` | 8 | ptr | **the bound definition payload (`rdx` of the bind, `0026C95A`)** | 2 / 10 / 5 | ~~`003DD1F0` (`003DD1FB`); `003DA2D0` (`003DA2DB`)~~ *(corrected 2026-10-02, OPUS: census artefacts — both store an entry's `+0x10` rate, `movss [rcx + (ch + 0x10) × 24]`, `003DD1F0`–`003DD1FB`, `003DA2D0`–`003DA2DB`)* | `003565C0` (`003565E8`); `0050D8F0` (`0050D91D`); +8 more | `0025AFC0` (`0025AFD7`); `0025B250` (`0025B260`); +3 more |
| `+0x008` | 8 |  | *not named by any page* | 0 / 1 / 0 |  | `ActorManager_GetRecordByOrdinal` `00358940` (`00358940`) |  |
| `+0x010` | 1 | u32 | **status bits — bit 0 = slot live** ([page](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)) | 0 / 2 / 6 |  | `002642C0` (`002642CA`); `00264390` (`002643A8`) | `0025B500` (`0025B52C` +2); `0025C830` (`0025D3D1` +2); +4 more |
| `+0x012` | 1 |  | *not named by any page* | 0 / 1 / 0 |  | `003565C0` (`003565E2`) |  |
| `+0x014` | 1 |  | *not named by any page* | 2 / 0 / 0 | `0026C5D0` (`0026C606`); `0026C3E0` (`0026C410`) |  |  |
| `+0x016` | 1 |  | *not named by any page* | 2 / 0 / 0 | `0026B8A0` (`0026B8A4`); `0026B8C0` (`0026B8C4`) |  |  |
| `+0x017` | 1 |  | *not named by any page* | 1 / 0 / 0 | `0034A250` (`0034A26D` +1) |  |  |
| `+0x018` | 2 |  | ~~*not named by any page*~~ the side-A reverse-lookup words (`003DA4B9`) *(answered: CONTRACT-manager-slot-entry-tables.md, and FH-1's 2026-09-27 note — named by the store; 2026-10-02, OPUS)* | 4 / 0 / 0 | `003DA370` (`003DA3A2`); `003DA400` (`003DA4B9`); `003DA000` (`003DA005`); +1 more |  |  |
| `+0x01A` | 2 |  | *not named by any page* | 2 / 0 / 0 | `003DA370` (`003DA3A6`); `003DA000` (`003DA009`) |  |  |
| `+0x01C` | 2 | s16 | **the shake driver that owns output channel 0** — an ordinal 0-3, written at `003DD2EC`; negative = none [shake](#the-camera-shake-fields-0x1c-0xf0-and-0x170-opus-2026-09-19) | 3 / 0 / 0 | `003DD230` (`003DD2EC`); `003DCF60` (`003DCF65`); `003DD350` (`003DD36E`) |  |  |
| `+0x01E` | 2 | s16 | **the shake driver that owns output channel 1** [shake](#the-camera-shake-fields-0x1c-0xf0-and-0x170-opus-2026-09-19) | 1 / 0 / 0 | `003DCF60` (`003DCF69`) |  |  |
| `+0x020` | 4 |  | *not named by any page* | 0 / 1 / 0 |  | `0025AE00` (`0025AE16` +1) |  |
| `+0x028` | 4 | u32 | **the manager index (slot number), written at bind `0026C957`** ([page](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)) | 0 / 52 / 0 |  | `00229FA0` (`00229FDE`); `002640D0` (`002640D7`); +50 more |  |
| `+0x040` | 8 |  | *not named by any page* | 0 / 1 / 0 |  | `002650B0` (`002650FC`) |  |
| `+0x048` | 8 |  | *not named by any page* | 0 / 1 / 4 |  | `002650B0` (`002650E8`) | `00264640` (`00264651`); `FieldData_GetVariable0` `00265270` (`00265279`); +2 more |
| `+0x058` | 8 | ptr | **pointer block: `02099DF0` (`0026CB2D`)** | 0 / 0 / 2 |  |  | `00264D20` (`00264D2E`); `0026ADC0` (`0026ADCE`) |
| `+0x060` | 8 | ptr | **pointer block: `02099FF0` (`0026CB38`) — the qword `OPUS-CONTRA-REC60` mistook for the storage record's `+0x60`** | 0 / 0 / 2 |  |  | `00264800` (`0026480E`); `0026AD10` (`0026AD1E`) |
| `+0x098` | 8 |  | *not named by any page* | 0 / 1 / 0 |  | `002650B0` (`00265113`) |  |
| `+0x0A0` | 8 |  | *not named by any page* | 0 / 2 / 1 |  | `00264D60` (`00264D60`); `002673A0` (`002673A0`) | `0026C880` (`0026C88A`) |
| `+0x0A8` | 8 |  | *not named by any page* | 0 / 1 / 1 |  | `00264D90` (`00264D90`) | `0026C8A0` (`0026C8AA`) |
| `+0x0B0` | 8 |  | **the bound script's section_006 (TIM2 texture block)**, set by `0026C860`; FH-1 2026-09-27 | 0 / 9 / 1 |  | `002C8BC0` (`002C8D26`); `0034ADA0` (`0034AE91`); +7 more | `0026C860` (`0026C86A`) |
| `+0x0B8` | 8 |  | *not named by any page* | 1 / 3 / 0 | `003E92F0` (`003E9303`) | `003E92F0` (`003E92F6`); `003E9320` (`003E935B`); +1 more |  |
| `+0x0C0` | 4 |  | *not named by any page* | 1 / 2 / 0 | `003E92F0` (`003E9312`) | `003E9320` (`003E93AA` +1); `003E9550` (`003E955A`) |  |
| `+0x0D8` | 8 |  | *not named by any page* | 0 / 5 / 1 |  | `003DA300` (`003DA300`); `003DA330` (`003DA330`); +3 more | `0026CE00` (`0026CE0A`) |
| `+0x0E0` | 8 |  | **the bound script's section_009 (CAM7 camera table)**, setter `0026CE20` — folded base, see §2.7 | 0 / 0 / 1 |  |  | `0026CE20` (`0026CE2A`) |
| `+0x0F0` | 8 | ptr | **the authored camera-shake bank** — null disables shake entirely; count at `+4`, 16-byte entries, data id at `+0x14 + 16*i` [shake](#the-camera-shake-fields-0x1c-0xf0-and-0x170-opus-2026-09-19) | 0 / 3 / 1 |  | `003DD230` (`003DD245` +1); `003DD320` (`003DD325`); +1 more | `0026D3A0` (`0026D3AA`) |
| `+0x0F8` | 8 |  | **the bound script's section_011 (SHK1 shake curves)**, setter `0026D3C0` — folded base, see §2.7 | 0 / 0 / 1 |  |  | `0026D3C0` (`0026D3CA`) |
| `+0x100` | 8 |  | *not named by any page* | 0 / 1 / 1 |  | `00263F80` (`00263F80`) | `0026CE40` (`0026CE4A`) |
| `+0x108` | 8 |  | **qword setter `ActorManager_SetResourceTeardownCallback` `00268630` — folded base, see §2.7** | 0 / 0 / 1 |  |  | `00268630` (`0026863A`) |
| `+0x110` | 4 |  | *not named by any page* | 1 / 0 / 0 | `003DA400` (`003DA471`) |  |  |
| `+0x114` | 4 |  | *not named by any page* | 1 / 2 / 0 | `003DA400` (`003DA47D`) | `003DA400` (`003DA4B1`); `003DA570` (`003DA586`) |  |
| `+0x118` | 2 |  | *not named by any page* | 4 / 0 / 0 | `003DA370` (`003DA3B1`); `003DA400` (`003DA484`); `003DA4D0` (`003DA4E8`); +1 more |  |  |
| `+0x11A` | 2 |  | *not named by any page* | 3 / 0 / 0 | `003DA370` (`003DA3AA`); `003DA400` (`003DA462`); `003DA000` (`003DA014`) |  |  |
| `+0x11C` | 4 |  | *not named by any page* | 1 / 0 / 0 | `003DA400` (`003DA44D`) |  |  |
| `+0x120` | 4 |  | *not named by any page* | 1 / 0 / 0 | `003DA400` (`003DA48C`) |  |  |
| `+0x124` | 1 |  | *not named by any page* | 1 / 0 / 0 | `003DA400` (`003DA497`) |  |  |
| `+0x130` | 2 |  | *not named by any page* | 2 / 0 / 0 | `003DA370` (`003DA3B8`); `003DA000` (`003DA01B`) |  |  |
| `+0x132` | 2 |  | *not named by any page* | 2 / 0 / 0 | `003DA370` (`003DA3BF`); `003DA000` (`003DA022`) |  |  |
| `+0x148` | 2 |  | *not named by any page* | 2 / 0 / 0 | `003DA370` (`003DA3C6`); `003DA000` (`003DA029`) |  |  |
| `+0x14A` | 2 |  | *not named by any page* | 2 / 0 / 0 | `003DA370` (`003DA3CD`); `003DA000` (`003DA030`) |  |  |
| `+0x160` | 2 |  | *not named by any page* | 2 / 0 / 0 | `003DA370` (`003DA3D4`); `003DA000` (`003DA037`) |  |  |
| `+0x162` | 2 |  | *not named by any page* | 2 / 0 / 0 | `003DA370` (`003DA3DB`); `003DA000` (`003DA03E`) |  |  |
| `+0x170` | 4 | u32 | **shake driver 0 — the authored data id**, copied from the bank at `003DD2B1`. Base of an array of **four drivers, stride `0x18`** [shake](#the-camera-shake-fields-0x1c-0xf0-and-0x170-opus-2026-09-19) | 1 / 0 / 0 | `003DD230` (`003DD2B1`) |  |  |
| `+0x174` | 4 | s32 | **shake driver 0 — the output channel**; a negative argument is replaced by `005C5230()` at `003DD265` [shake](#the-camera-shake-fields-0x1c-0xf0-and-0x170-opus-2026-09-19) | 1 / 2 / 0 | `003DD230` (`003DD2C0`) | `003DD230` (`003DD2E4`); `003DD350` (`003DD366`) |  |
| `+0x178` | 2 | u16 | **shake driver 0 — the state word**: 0 inactive, 1 running (`003DD2A9`), 2 finished. **Non-zero is evaluated, including 2** [shake](#the-camera-shake-fields-0x1c-0xf0-and-0x170-opus-2026-09-19) | 3 / 0 / 0 | `003DD230` (`003DD2A9`); `003DD320` (`003DD338`); `003DCF60` (`003DCF6D`) |  |  |
| `+0x17A` | 2 | s16 | **shake driver 0 — the bank index** the data id was read from (`003DD2B8`) [shake](#the-camera-shake-fields-0x1c-0xf0-and-0x170-opus-2026-09-19) | 2 / 0 / 0 | `003DD230` (`003DD2B8`); `003DCF60` (`003DCF74`) |  |  |
| `+0x17C` | 4 | f32 | **shake driver 0 — the time argument** the starter was given (`003DD293`, `movss`) [shake](#the-camera-shake-fields-0x1c-0xf0-and-0x170-opus-2026-09-19) | 1 / 0 / 0 | `003DD230` (`003DD293`) |  |  |
| `+0x180` | 4 | f32 | **shake driver 0 — the rate**, initialised to `1.0f` at `003DD2C7` and scaled each frame at `003DD093` [shake](#the-camera-shake-fields-0x1c-0xf0-and-0x170-opus-2026-09-19) | 1 / 0 / 0 | `003DD230` (`003DD2C7`) |  |  |
| `+0x190` | 2 |  | *not named by any page* | 1 / 0 / 0 | `003DCF60` (`003DCF7B`) |  |  |
| `+0x192` | 2 |  | *not named by any page* | 1 / 0 / 0 | `003DCF60` (`003DCF82`) |  |  |
| `+0x1A8` | 2 |  | *not named by any page* | 1 / 0 / 0 | `003DCF60` (`003DCF89`) |  |  |
| `+0x1AA` | 2 |  | *not named by any page* | 1 / 0 / 0 | `003DCF60` (`003DCF90`) |  |  |
| `+0x1C0` | 2 |  | *not named by any page* | 1 / 0 / 0 | `003DCF60` (`003DCF97`) |  |  |
| `+0x1C2` | 2 |  | *not named by any page* | 1 / 0 / 0 | `003DCF60` (`003DCF9E`) |  |  |
| `+0x1C8` | 0 |  | *not a field — the `lea` at `00259652` is a foreign array's loop bound, never dereferenced (§2.7)* | 0 / 0 / 1 |  |  | `00259620` (`00259652`) |
| `+0x1E0` | 4 | ~~u64~~ u32 *(corrected 2026-10-02, OPUS: a dword counter — `002630B7 dec dword ptr [r14 + 0x1E0]`; the bind's qword store `0026CB1F` zeroes `+0x1E4` with it)* | **zeroed at bind (`0026CB1F`)** | 0 / 0 / 4 |  |  | `002628B0` (`00262EB8` +2); `00263050` (`002630C5` +2); +2 more |
| `+0x200` | 1 | u8 | **bit 2 cleared at bind (`0026C950`)** | 2 / 0 / 1 | `0034AD70` (`0034AD79`); `0034B1C0` (`0034B1C9`) |  | `00264830` (`00264830` +1) |

### 2.4 The `+0x110`–`+0x1D0` band is two arrays of four 24-byte entries

The field map above lists this band as twenty-five separate scalars, most of them paired words at a
regular spacing nobody had explained. They are not scalars. `+0x110` and `+0x170` are each an array
of four `ActorManagerSlotEntry`, 24 bytes per element, and together they tile the band exactly.

**The element size is proven by the index pre-multiply, not by the spacing of the offsets.** x86
scale factors stop at 8, so a compiler reaches a 24-byte element by multiplying the index by three
first: `FUN_003DA400` computes `lea rdi, [rsi + rsi*2]` at `003DA446` and only then addresses
`[rbx + rdi*8 + 0x110]`, giving an effective stride of 3 x 8 = 24. `FUN_003DD230` does the same at
`003DD28C` for the `+0x170` array. Reading a stride off the gaps between offsets would have been
guessing; this is the instruction saying it.

**The count is four, proven twice independently.** Each builder rejects its call unless the entry
index is 0..3 — `cmp esi, 3` then an unsigned `ja` to the exit at `003DA41A`, and `cmp edi, 3` at
`003DD26C`. Separately, two other functions rewrite the `element+0x8` / `element+0xA` pair for every
entry with literal displacements and then stop: `FUN_003DA370` writes `0x118/0x11A`, `0x130/0x132`,
`0x148/0x14A`, `0x160/0x162`, and `FUN_003DCF60` writes the same four for the B side. Those literal
sequences are what the field map had recorded as unexplained paired words.

**The two extents abut exactly**: `0x110 + 4 x 24 = 0x170`. Neither derivation was aimed at the
other, and the twenty-five scalar rows the arrays replace tile the two ranges with no row left over
and no row falling outside — which is the check that would have caught a wrong stride.

The element layout, from the two builders:

| offset | size | ctype | what the instruction shows |
|---|---|---|---|
| `+0x00` | 4 | `uint32` | copied from the definition table: `003DA456 mov edx, dword ptr [rcx + rax*8 + 0x14]`, `rcx` from the slot's definition pointer, `rax` = 2 x the record index |
| `+0x04` | 4 | `int32` | a caller argument clamped non-negative (`003DA46E cmovns ecx, eax` after `xor ecx, ecx`), read straight back to index a `uint16` slot **in the container**: `[slot + v*2 + 0x18]` for A, `[slot + v*2 + 0x1C]` for B |
| `+0x08` | 2 | `uint16` | initialised to the literal `1`; this is the member the two unrolled updaters rewrite |
| `+0x0A` | 2 | `uint16` | the bounded record selector — the call is rejected unless it is below the count at `definitionTable+4` (`003DA434`, `003DD27E`) |
| `+0x0C` | 4 | `float` | caller-supplied, `movss` from `xmm2` / `xmm6` |
| `+0x10` | 4 | `float` | initialised to `0x3F800000`, which is `1.0f` |
| `+0x14` | 1 | `uint8` | cleared by the A builder at `003DA497`; **the B builder has no such write** |
| `+0x15` | 3 | — | unknown span; nothing observed touches it, so it is not recorded as padding |

Two things this does **not** settle. Whether the band is two arrays of four or one array of eight
split by role is not decidable from layout — what favours two is that each unrolled updater covers
exactly one half and stops. And the `+0x14` byte is written only on the A path; that is evidence of
presence there, not evidence the B entries lack the member, since the stride is 24 either way.

What separates the two arrays is which definition pointer they read and which lookup slot they write
back into: A guards on `+0xD8` and writes `+0x18`, B guards on `+0xF0` and writes `+0x1C`. That
guard is also what resolved `+0xF0` — it is dereferenced and compared against zero as a qword, so it
is a pointer, the counterpart of `+0xD8`.

~~The names of the members remain open;~~ *(answered: CONTRACT-manager-slot-entry-tables.md names them — `definitionValue`, `lookupIndex`, `recordIndex`, `clock`, `rate`, `clockRunning`; 2026-10-02, OPUS)* the layout does not depend on them.

### 2.5 What nobody reaches

23 ranges totalling 373 bytes have no access on either route (the eight bind-zeroed
qwords counted as covered). The ones of 32 bytes or more: ~~`+0x68`–`+0x97` (48 B),~~ `+0x244`–`+0x287` (68 B) *(corrected 2026-10-02, OPUS: `+0x68`–`+0x8F` is written by the bind — `0026CB43`, `0026CB4E`, `0026CB6B`, `0026CB59`, `0026CAE6` — and `+0x68` / `+0x70` are read by the interpreter at `00261855` / `0026187D`; whether `+0x90`–`+0x97` is reached is not settled here)*.
*`+0x201`–`+0x243` was listed here before the folded-base sweep: `+0x201` has a reader and
`+0x204`–`+0x243` is cleared at bind — both reached through folded-base addresses the
displacement census cannot see (§2.7).*

### 2.6 The interpreter's view of the slot, and the six variable homes — 2026-09-11 (FABLE-BF3)

The script interpreter receives this slot as its first argument (`r13`;
[the interpreter page](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md)
§14) and reaches thirteen offsets through it — `+0x000`, `+0x008`, `+0x028`, `+0x040`, `+0x048`,
`+0x058`, `+0x060`, `+0x068`, `+0x070`, `+0x078`, `+0x080`, `+0x098`, `+0x201` — 28 accesses in six
functions, appended to the census with the route `argseed 0025E4C0:0`. The table's cells above were
not re-counted for that route; these rows are additional readers of the offsets named.

Six of those pointers are the homes of script variables, resolved by class from the descriptor table
at `+0x078` ([the storage-class page](../../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md)):

| offset | store name | class | what it points at |
|---|---|---|---|
| `+0x040` | `UNRESOLVED` | 1 `file` | `payload + [payload + 0x38]`, filled by `ActorSystem_InitializeManagerRuntime` (`0026D2F6`) when the binder's zero is still there |
| `+0x048` | `table256` | 0 `global` | the persistent save payload (`002EF2B0`); the 256-entry operand bank is its first 0x200 bytes, and script globals occupy `+0x200`–`+0xCF4` beyond it |
| `+0x050` | `payloadSectionA` | 2 `local` (base) | the image's `+0x48` region; `00264E30` adds the actor entry's `+0x1C` |
| `+0x058` | `bank64` | 4 `scratch1` | `02099DF0`, cleared on every field transition |
| `+0x060` | `bank32` | 5 `scratch2` | `02099FF0`, the group persistent bank the save image carries |
| `+0x078` | `payloadSectionE` | — | the variable descriptor table itself |
| `+0x098` | `UNRESOLVED` | 2 `local` (resolver) | `00264E30`, installed at `0026CB76` |

The "64 / 32 uint16 entries" the accessor pairs index in `+0x058` / `+0x060` are the banks' native
readers; the scripts address the same banks byte-wise through the resolver, at 74 and 77 distinct
offsets respectively. Store names are OPUS's to change (FABLE-REQ-OPUS-SLOT-VARHOMES).

### 2.7 The folded-base sweep — six fields the displacement census could not see — 2026-09-16 (SWE2-STRUCT)

`FABLE-REQ-SWE2-STRUCT-FOLDED-BASE-FIELD-CENSUS`, worked on this array. A `lea REG,[rip+d]`
whose target is `02098E10 + slot*0x288 + k` folds `k` into the link-time constant; the access that
follows is `[REG + idx]` with **no displacement**, invisible to every `[reg+disp]` census — including
the two that built the table above. FABLE's scan found 28 such `lea` sites at 18 distinct offsets;
seven had no row. All seven were read at the instruction level. Verdicts:

| offset | verdict | what the instruction shows |
|---|---|---|
| `+0x013` | **uint8** | slot-indexed getter `002673F0`: `movsxd rax,ecx / imul rcx,rax,0x288 / movzx eax,[rcx+rax]` — read-only |
| `+0x0E0` | **qword** | setter stub `0026CE20`: stores `rdx` — section_009 from its handler `0032FAC0`; no reader through the slot (readers use `022C6D58[m]`) |
| `+0x0F8` | **qword** | setter stub `0026D3C0`: stores `rdx` — section_011 from its handler `003316B0`; readers use `022C6DD0[m]` |
| `+0x108` | **qword** | `ActorManager_SetResourceTeardownCallback` `00268630`: stores `rdx`. The name claims a function pointer; the body proves a qword store and no more |
| `+0x1C8` | **refused** | the `lea` at `00259652` → `020994E8` is the loop bound of a foreign `0x860`-stride array ~~at `02098428`~~ whose cursor starts at `02098428`, element 0's `+0x708`; the array is two elements at `02097D20`, ending `02098DE0` before the slot array *(corrected 2026-10-02, OPUS: `002593D0` / `00259470` copy `0x860` bytes between `02097D20` and `02098580`)* (`cmp rdi,rbp` at `002597B9`) — the address is compared, never dereferenced. A folded-base `lea` is *address-taken*, not a field access |
| `+0x1DE` | **uint16** | `movzx word[rdi]` on slots 0 and 3 in `0026DC70`/`0026DD50`, gated by `test byte[rdi-0x1CE],1` (the `+0x10` live bit); compared against `word[+0x1D6]` plus itself |
| `+0x1D6` | **uint16** | the `word[rdi-8]` half of that pair — a second offset the same folded base revealed |
| `+0x204` | **uint8[64]** | `ActorManager_BindLoadedDefinitionPayload` clears eight qwords `+0x204..+0x243` on slots 0–3 (`rax` from `02099014`, step `0x288`, bound `020997AC`, `rbx` xor-zeroed), under `test ecx,ecx`. Bulk storage; element type unknown |

Six field rows were added to `_types/fields.tsv` (`+0x013`, `+0x0E0`, `+0x0F8`, `+0x108`, `+0x1D6`,
`+0x1DE`, `+0x204`); `+0x1C8` is refused above. **The general defect stays open:** FABLE's shape
cluster scan lists 122 other candidate constants clusters where the same folding may hide fields —
a census extension, not part of this package.


## 3. Key addresses

| address | what |
|---|---|
| `02098E10` | the five-slot array, stride `0x288` ([the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §2) |
| `02099D70` | the bound-slot pointer; written by the bind and fifteen more |
| `0026C8C0` | `ActorManager_BindLoadedDefinitionPayload` — §2.2 |
| `002640D0` | the three-instruction reader of `+0x28` used as the scan's control |
| `0025D9E0` | `ActorManager_RunFieldRuntimePass` — a writer of `02099D70` |

### The `0026C8C0` exclusive subtree — all 14 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the bind **14 frontier functions**, all called by the root
directly (`edges.tsv`: `0026C8C0 →` each). Roles below are what the bodies do; interior cites are
one instruction inside each declared extent (`interior_cite.py scan`; no boundary crossings).

| cluster | members | role | interior |
|---|---|---|---|
| kind-`0xD`/`0xE` registrations | `0025A990` (155 B), `0025AA30` (155 B) | twin stubs: skip if `02099DD0`/`02099DD8` is already set, else `00369760` on kinds `0xD`/`0xE`, then the `0036Cxxx` name/alloc sequence and `0036C660` — registering the name strings `00915710` (`EVTMEM`) and `00915718` | `0025A9A3` / `0025AA43` |
| block init | `0026FFA0` (283 B), `002700C0` (43 B) | the first walks the `00915790` string table and the `01CEBD30`/`01CEBDB0` blocks writing `02F8F220`; the second folds `arg & 1` into `02F8F23D` | `0026FFA8` / `002700C2` |
| gated flag writers | `002EBDB0` (33 B), `002EC5A0` (7 B), `002ECB70` (37 B), `00360110` (8 B) | flag cells under `0215FD58`/`0215FD68` guards, a plain byte store to `0215FD55`, and a clear of `022CB726` — bind-time state resets | `002EBDB7` / `002EC5A6` / `002ECB77` / `00360117` |
| fade config | `002EDA50`, `002EDA60` (9 B each) | `CharacterRenderConfig_GetBuiltInFadeStartDistance`/`...FadeWidth` — the built-in fade constants the bind stamps onto the record | `002EDA58` / `002EDA68` |
| table queries | `00377440` (62 B), `00377480` (61 B) | `EventMemory_QueryDefinitionIdAbsent` reads the `EVTMEM` publisher cell `02ADD0A8`; its sibling bounds-checks `02ADD100` — the `navimapdata` cell the `00378540` installer publishes ([field-record-table §2a](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md)) | `00377447` / `00377487` |
| record scans | `0036E3B0` (170 B), `003DD790` (69 B) | a 31-entry scan (`r10d = 0x1F`) over the `02B5xxxx` table, and a stride-`0x1C0` indexed walk of `02B581AD`/`02B58A60` | `0036E3B3` / `003DD79D` |

So the bind does more than fill the pointer block: it re-registers the `EVTMEM`-side resource
names, primes its own flag cells, stamps the built-in fade distances, and consults the same
map/event tables the boot installer published — the definition payload is bound against the live
field state, not in a vacuum.

## 4. Data structures and formulas

```
ActorManagerSlot (0x288) x5 at 02098E10; bound slot in 02099D70   (the type's one name is ActorManagerSlot - the store's, the tooling's and the prose's; this folder and its census file keep 'record' in their file names only)
  +0x000 ptr  bound definition payload      +0x010 u32 status (bit 0 live)     +0x028 u32 manager index
  +0x050 +0x058 +0x060 +0x068 ptr  the pointer block from the bind
  +0x1E0 u64 zeroed at bind                 +0x200 u8 (bit 2 cleared at bind)   +0x201 u8 sub-step opt-in   <- corrected 2026-10-02, OPUS - +0x1E0 is a u32 counter (002630B7 dec dword); the bind's qword store 0026CB1F zeroes +0x1E0 and +0x1E4
  +0x244..+0x27C u64[8] zeroed at bind
```

## 5. Call chain

Bind → the slot (§2.2) → `02099D70`; the world tick reads `+0x10` and `+0x201` per slot and calls the
per-record post-pass; everything else in the table reaches a slot through `02099D70` or a literal
slot address.

## 6. Modding notes

- **Do not confuse this record with the actor storage record**: same offsets, different objects; a
  patch aimed at the storage record's `+0x60` that lands here overwrites a pointer.
- **Slot 0 is the primary manager**; the array route shows which functions address slots 1–4
  literally (the `slot` column of the access table).

## 7. What is not known

- [x] **FH-1.** **The names of the offsets no page names** — starting with `+0xB0` (9 readers), `+0xD8` *(closed — the register row is WITHDRAWN.)*
  (5) and `+0x18` / `+0x118` (4 writers each). The `+0x11x`–`+0x1Cx` band is no longer among them as
  a *structural* unknown: it resolved to two arrays of four 24-byte entries (§2.4), and the paired
  words that looked unexplained are one member of a repeating element. What is still missing there
  is naming, not layout. **FH-1.**
  **NARROWED 2026-09-27 (OPUS):** the offsets this box started from are named. +0xD8, +0x18 and the +0x11x-+0x1Cx band were named by the store before today. +0xB0 is the bound script's section_006 TIM2 texture block, which the gauge-label verbs 0x1BC-0x1BE read. The slot carries eight section pointers, each set by a 5-instruction setter stub from its section handler: sec 2 -> +0xA0 (zone message bank), 3 -> +0xA8 (field-sign captions), 6 -> +0xB0, 8 -> +0xD8, 9 -> +0xE0 (CAM7 camera table, formerly write-only), 10 -> +0xF0, 11 -> +0xF8 (SHK1 shake curves, formerly write-only), 12 -> +0x100. Lifetime: the bind zeroes +0xA0-+0xB8, +0xE0 and +0xF8. The teardown 0032ED80 clears sections 8-12 through their setters with 0, but for sections 2, 3 and 6 it releases the section and clears only the global mirror (022C6CA0 / 022C6CC8 / 022C6CF0). Those three slot fields keep the old pointer until the next bind; whether a reader runs in that window is not claimed. Still unnamed: +0x12 / +0x13 / +0x17 bytes; the counters +0x24 / +0x38 / +0x1E0 / +0x1E4 / +0x202; +0xB8 (nullable pointer); +0xC8 / +0xD0 (bind-zeroed); +0x108 (the teardown-callback slot, write-only); +0x1E8 / +0x1F8 / +0x1FC / +0x284; the two 64-byte bind-zeroed blocks +0x204 / +0x244; and the unobserved +0x2C / +0x3C / +0x90 / +0xC4 / +0x1EC. Control _index/candidates/fh1-slot-sections/fh1_slot_sections.py (5 checks, FAILS 0).
- [x] **FH-2.** **What the pointer block `+0x50`–`+0x68` points at** beyond the two `.data` addresses and the
  payload-relative pointer. **FH-2.**
  **ANSWERED 2026-09-14 (FABLE).** A static read of the bind and the readers. Two peer pages already named
  the targets ([the interpreter](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md)
  slot table, and §2 above); this ties each to the write that fills it. `r15` is the bound image and `rdi`
  the slot (`0026CB04`–`0026CB43`):
  - **`+0x50`** = image + `u32 [image + 0x48]` (`0026CB04`–`0026CB17`): the **local-variable section**.
    The class-2 resolver `00264E30` returns `[slot + 0x50] + i32 [[entry + 0x40] + 0x1C]`, the actor's own
    offset into it (`00264E30`–`00264E38`).
  - **`+0x58`** = `02099DF0` (`0026CB26`–`0026CB2D`): scratch bank 1, cleared on every field transition.
  - **`+0x60`** = `02099FF0` (`0026CB31`–`0026CB38`): scratch bank 2, the group bank the save image carries.
  - **`+0x68`** = image + `i32 [image + 0x20]` (`0026CB3C`–`0026CB43`): the **int constant pool**. `PUSHI`
    loads `[slot + 0x68]` and pushes `i32 [pool + operand × 4 + 4]` (`00261855`–`0026185C`).
  - The same run of writes goes on past the question's range:
    - `+0x70` = image + `[+0x24]`, the float pool `PUSHF` reads (`0026187D`–`00261884`);
    - `+0x80` = image + `[+0x2C]`, the tag table;
    - `+0x78` = image + `[+0x28]`, the variable descriptor table;
    - `+0x98` = the resolver `00264E30` itself (`0026CB6F`–`0026CB76`).
  - **Not claimed:** nothing was executed, and the section layouts behind `+0x50` and `+0x68` beyond
    these reads are not mapped here.
- [x] **FH-3.** **Who writes `02099D70` besides the bind** (fifteen functions, `globals_index`), and whether *(closed — the register row is WITHDRAWN.)*
  the bound slot ever differs from slot 0 in play. **FH-3.**
  *Partly answered 2026-09-14 (FABLE); the register row is PARTIAL (FH-3):* **`02099D70` is a scoped "current manager"
  binding, not a mode.** A RIP-relative census gives 33 stores in ~~17~~ 16 functions *(corrected 2026-10-02, OPUS: the stores to `02099D70`, the bind `0026C8C0` among them; no image-base-relative form exists)*. **Twelve functions save, bind and restore:**
  each loads the old value, stores its slot, does its work and stores the old value back. They are `0025AFC0`,
  `ActorManager_RunFieldRuntimePass` `0025D9E0`, `0025E400`, `002623A0`, `00263050`, `00263230`, `00263AC0`, `00264050` (binds
  its argument, or slot 0 `02098E10` when null, and restores on each of three exits), `0026C3E0`, `0026C5D0` (two pairs),
  `ActorSystem_InitializeManagerRuntime` `0026CE60` and `0026E060`. The bind itself (`0026C911`) is paired with `0026CDC0` in
  the same function. The area unload `002628B0` stores once inside its slot loop (`00262938`). **Only one path binds
  without restoring:** the 8-byte setter `0026A480`, called by `0035A270` and `0035AB50`, each binding the manager
  `00263FF0(id)` returns (`0035A284`–`0035A28F`, `0035AB64`–`0035AB6F`). **So the bound slot leaves slot 0 transiently in
  every per-slot pass, and persistently only after one of those two functions,** whose triggers were not read. Whether they
  run in ordinary play is the remaining half.
  *Corrected 2026-09-14 (FABLE, second read): the two callers of the 8-byte setter restore too.* `0035A270` and `0035AB50`
  each save the old binding through the 8-byte getter `002640C0` into `r12`, bind, and at their single exit tail-jump the
  setter with `r12` (`0035A281` / `0035A388`–`0035A392`; `0035AB61` / `0035AC50`–`0035AC5A`). Both are called only inside
  scopes that restore again: the save/bind/restore body `0025AFC0` (`0025AFEC`, `0025B028`) and the area unload.
  **The one store that is not undone is the unload's own.** `002628B0(slot)` binds a live slot at `00262938`, does its
  unload, and never writes the global back. Its callers are `ActorResource_BeginManagerResourceSetLoad` (`0032FCF6`) and
  `0025BFB0` (`0025C036`). So the binding stays on slot *k* after an unload of slot *k*, until the next scoped pass;
  that pass restores to *k*, not to 0. Whether a manager resource-set load runs for a slot other than 0 in ordinary
  play is the remaining half.
  *Narrowed the same day: the non-zero-slot loads are script-driven and on ordinary paths.*
  - `ActorResource_BeginManagerResourceSetLoad` has one caller, `WorldSimulation_ProcessDeferredModeRequest(slot, request)`.
  - That function's eight call sites pass these slots:
    - slot 0 from `World_UpdateSimulationTick`;
    - **slot 1** from `ActorManager_RunFieldRuntimePass` during the primary manager's start-up, with request `0xD4`
      (`0025DAE1`–`0025DAED`);
    - **slot 3** from the result handler of verb `0x0198` **`summoneventread`**, with the popped request (`0035359E`–`003535A3`),
      and from `003C9FD0`;
    - a script-supplied slot from verbs `0x00E7` **`eventread`** and `0x00E8` **`eventread_e8`**, and from the debug verb
      `0x202D`;
    - the special-sequence initialiser's own slot.
  - So the binding is left on slot 1 or 3 whenever such a request arrives while that slot is live, because the unload binds
    only a live slot (`0026292C`).
  - That a summon or event read lands on a live slot is the one runtime condition not shown here.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| Every row of the table | `actor-manager-record-accesses.tsv` (bound route); the absolute-address scan's rows (array route) | 1 | PROVEN |
| The bind's writes | `0026C8FE`–`0026C95A`, `0026CB17`–`0026CB43` | 1 | PROVEN |
| The two names from the world tick | [the world-tick page](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) | 1 | PROVEN (by reference) |
| The untouched ranges | absence on both routes with passing controls | 1 | PROVEN (for those routes) |

## 9. Related

- [`../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) — the tick that walks the five slots.
- [`../Actor-Storage-Record/the-record-behind-every-actor.md`](../Actor-Storage-Record/the-record-behind-every-actor.md) — the record this one was confused with.

## Falsification pass 1 — 2026-09-13 (OPUS)

| claim | measured |
|---|---|
| bound-slot route: **167** rows / **91** functions / **50** offsets, **72** at the seed and **95** propagated | **167 / 91 / 50 / 72 / 95** — every one exact |
| the band is two arrays of four 24-byte entries, `+0x110` and `+0x170` | `0x110 + 4 × 24 = 0x170` and `0x170 + 4 × 24 = 0x1D0` — the two extents abut and the band closes |
| the stride is proven by the index pre-multiply | `003DA446 lea rdi, [rsi + rsi*2]`, and `003DD28C lea rsi, [rdi + rdi*2]` for the B array — both exact |
| the count is four, bounded at each builder | `003DA41A cmp esi, 3` and `003DD26C cmp edi, 3` — both exact |
| the two unrolled updaters write `0x118/0x11A`, `0x130/0x132`, `0x148/0x14A`, `0x160/0x162` | **exactly those eight displacements in `003DA370` and no others**, and `003DCF60` writes `0x178/0x17A`, `0x190/0x192`, `0x1A8/0x1AA`, `0x1C0/0x1C2` — **the A set plus `0x60`** |

The updaters carry a proof the page does not draw out: both sequences start at **element `+0x08`**
(`0x110 + 8` and `0x170 + 8`) and step by **24** four times. **The element offset, the stride and the
count all fall out of the displacement list alone**, independently of the pre-multiply — two
derivations of the same layout that were not aimed at each other, which is the same standard §2.4
sets for itself.

*(And `02098E10 + 5 × 0x288 = 02099AB8`, so the five-slot array ends well before the bound-slot
global at `02099D70` — they do not overlap.)*

### The evidence file has grown, and the `57` now reproduces for the wrong reason

`actor-manager-record-accesses.tsv` holds ~~**194** rows today~~ **194** rows at this pass (204 on 2026-10-02, measured), not 167 *(corrected 2026-10-02, OPUS: the file on disk)*. §2.6 added the interpreter's
argument seed on 2026-09-11 (`4e8b832`), and **27 rows carry its note**. `194 − 27 = 167`, and with
those rows excluded every figure in §2.1 comes back exactly. **§2.1 is correct as authored; it simply
predates §2.6.**

One number deserves a warning, because it is the one a reader would check first:

- §2.1 says **57** offsets are touched "on either route" — that is the **bound-slot 50 ∪ array 17**,
  with ten shared.
- The TSV contains **only the bound-slot route**. Its offsets are the bound-slot **50** plus the **7
  new ones the argseed rows introduced** — which is also **57**.

**The same number, from a different sum, over a file that does not contain the route the number is
about.** A reader recomputing `57` from the TSV would confirm §2.1 and conclude the file covers both
routes. It does not; the array route's 51 references are not in it at all.

> This is what makes an evidence file stop being evidence: not that it is wrong, but that it drifted
> until a check against it passes for a reason unrelated to the claim. The fix is the annotation in
> §2.1, not a change to either number — both are right about what they describe.

**Not claimed:** the array-route figures (51 / 31 / 17) were **not** verified, because the file beside
the page does not carry that route and this pass did not rebuild the absolute-address scan. §2.1's
own warning stands untouched — the census is seeded on accessors, so writes remain under-covered, and
nothing here turns an absent writer into an absence of writers. §§2.2, 2.3, 2.5 and 2.6 were not
re-derived; nothing was executed or observed live.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — SERVICE.** `0025D9E0` on this page calls `FUN_00234150`, owned by that layer. What it reaches is a 104-byte registration helper that takes the `.text` address `002FED60` as a callback and gates on `byte[+0] & 0x10` of what `0031B810` returns; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Items_Equipment_Shops_License — CLIENT.** `Inventory_QueryOwnedCountIncludingReservedActionItems`, owned by that layer, calls `0031B810` on this page. That caller is the owned-count query for an item id, which returns `-1` for the sentinel id `0xFFFF`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — SERVICE.** `002628B0` on this page calls `PartyFocus_ClearCurrentActorIfEligible`, owned by that layer. What it reaches is a 103-byte guard that needs `002671F0(0)` and a non-zero packed handle at `[022C7FE0]` before clearing through `003588B0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — CLIENT.** `FUN_001da220`, owned by that layer, calls `00265270` on this page. That caller is a 102-byte gate over three conditions in order - two state queries and the current area id being **zero** - and it does nothing at all unless all three agree; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `Reward_ComputeExperienceForRecipient`, owned by that layer, calls `0031B810` on this page. That caller is the experience computation for one recipient: it needs `byte[rec+5] == 0` and takes its context from `0031B860`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**StoryEvent — CLIENT.** `FUN_001ed240`, owned by that layer, calls `00265270` on this page. That caller is a 2,192-byte cutscene-override table: it matches the current area id against hard-coded values such as `0xD70` and `0xD48`, the story-progress word selected by `[01DFE40C]` out of `01F832B0` against a step number, the model's name against string literals such as `g0999` and `c1004`, and the animation time against a window, returning a small override index when all four agree; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Story_Event_Quest_Hunt — CLIENT.** `PersistentFlag_QueryBank512High`, owned by that layer, calls `002EF2B0` on this page. That caller is one of **twelve persistent-flag bank accessors** - the query and set pairs over the 64-, 512- and 2,048-bit banks and the primary/authored pair - every one of which takes its base from this page's payload accessor, which is why the whole flag family is indexed off the save image; the layer's two remaining edges here are `PersistentFlag_QueryAuthoredThresholdSchedule`, which asks this page's field-variable getter for the value it walks a list of 15-bit authored thresholds against and returns the parity of, and `EventMemory_QueryDefinitionIdAbsent`, the linear scan of the table at `[02ADD0A8]` that returns 1 when an id is *not* present; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — SERVICE.** `002E09A0` on this page calls `FUN_00254b50`, owned by that layer. What it reaches is a 263-byte entry that masks its id to `0x7FFF` and takes one of two paths on `[02092734] == 1`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Movement — SERVICE (SWE2-CONTRACT 2026-09-15, 33 edges measured).** This page's bodies drive the
movement layer directly: `00263230`/`0026C3E0`/`0026C5D0`/`0026C8C0` call
`Movement_SetRequestedSpeed` `0026D6F0` (4 edges); `00263050`/`00263230`/`0026C5D0` call `002EBE50`;
`0025D9E0` and `0025E4C0` bracket `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00`;
`0025E400`/`002623A0` call `002E5180`; `002628B0` alone calls six Movement helpers
(`0026A1D0`, `003791C0`, `003DAA20`, `00379070`, `00263560`, `003792D0`). The caller-direction edges
are the mirror image: `PartyFollow_SolveFormation`, `0031B810`'s callers `00310920` (interior read 2026-09-17, SWE2-FRONTIER: 1,028 B — `003272A0` first at [`00310957`](../../_index/ADDRESS-INDEX.md), `00263F40` ×6 + `0026B620`/`0026B0C0` ×4 — a Movement-side resolver walking this record family)/`00313670` and
`Movement.CharacterPresentation.BindingInitialization` `002E28E0` consult this page's records.
Actor management and locomotion are one pipeline — the record accessors the movement pass drives
are the crossing.

**Presentation — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 24 edges).** `0026C8C0`
(`ActorManager_BindLoadedDefinitionPayload`) applies the render-fade configuration family —
`CharacterRenderSystem_SetFadeWidth`/`SetFadeStartDistance` plus the six
`CharacterRenderConfig_*` default/built-in getters and setters — when a definition payload is bound;
`002628B0` calls `CharacterRenderSystem_RefreshDistanceCullEnable` and the pending-record flush
`002E65A0`. Caller-side, Presentation bodies reach this page through the shared
`00263FF0`/`00358940` accessors (`003A56F0`, `00465120`, `003A4290` — the twin `+0x48`-kind
dispatch fronts, selector bound [`003A4308`](../../_index/ADDRESS-INDEX.md) — `00465690`
(interior read 2026-09-17, SWE2-FRONTIER — a render-config commit body: `002F1F40` at
[`004656F1`](../../_index/ADDRESS-INDEX.md), then `00465CD0` ×8 / `003A6BA0` ×5 / `002E9B80` ×5 /
`003A2B20` ×4 over the config record; `002F1F40` itself read — a transform compose, alternating
`0039AF70`/`00398F90` (the point-transform/`w`-twin pair) and `0039B550`, beginning
`002F1FFD`),
`PendingMaskedRecordMaterializationSweep` `003DD4C0`) and `0031B810` is consulted by
`BattleUnit_BroadcastPartyCombatTargetRelation` and `PartyCombat_UpdateStanceState`.

**Party — SERVICE, fuller than the single bullet above (SWE2-CONTRACT 2026-09-15, 16 edges).**
Beyond `00358B40`, this page's bodies call `PartyFocus_GetCurrentPackedActorHandle` `003590D0` ten
times (from `0025D9E0`/`0025E400`/`002623A0`/`00263050`/`00263230`/`00263AC0`),
`PartyFocus_CommitPendingPackedActorHandle_Thunk` `00358BB0` three times, and
`PartyControl_SetMovementSuppressionBit` `00359200` twice. The actor-manager record is where party
focus handles are read, committed and suppressed — the crossing is the focus-handle protocol, not
shared ownership.

**CombatFormula — MECHANICAL (SWE2-CONTRACT 2026-09-15, 36 edges).** All 36 edges are CombatFormula bodies calling
the page's cited owner resolvers `0031B860` (35) and `0031B810` (1): `BattleFormula_*`,
`BattleStats_ModifyHPAndProcessLethalState`, `BattleRuntime_MarkTargetHistoryBit`,
`BattleFormula_SelectPoachRewardItem95_5`, etc. The record map's `0031B860`/`0031B810` entries are
the shared "find owning battle unit" accessors every stats body calls — fan-in, not a formula
relationship the field map owns.

**Input — MECHANICAL (SWE2-CONTRACT 2026-09-15, 9 edges).** `Input.ActorControlMaskPropagationRuntime` `00226BE0`
trades calls with `00263230`/`00263FF0`/`0026A1D0`/`00358940`/`003590D0` (5 edges);
`InputGameplay_ArbitrateDigitalInputAndModalState` shares `00264640`/`00265270`;
`Input.CommandGateBoundarySupport` `002E09A0` shares `00263FF0`; `0035B5D0` is called by `002628B0`.
Shared control-mask/accessor fan-in.

**Audio — MECHANICAL (SWE2-CONTRACT 2026-09-15, 6 edges).** Audio bodies share the page's cited generic helpers; no
audio relationship to the record map.

**Platform — CLIENT.** `001B1960`, owned by that layer, calls `001B1440` — the record-map helper
(`001814F0` → `001B1240` chain context) this page names; the platform layer consults it during its
own record work. Fan-in, not shared ownership. Read from `edges.tsv` 2026-09-17 (SWE2-FRONTIER).

**Script_VM_Native_Bridge — MECHANICAL (SWE2-EC7-170, 207 edges).** The
`0046BD60` enumeration's helpers `00263FF0`, `00358940` and `002EA6A0` are
consumed across the bridge layer (`0033F7F0`, `0025E4C0`, `00345CD0`,
`00267420`, `0050D5E0`, +202 more) — the `0026xxxx`/`0035xxxx` accessor
family's fan-in, no bridge relationship to the record map. Edge list from
`edges.tsv` 2026-09-22.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. The 2026-09-19 RNG note above sits under a heading the crossings gate does not read, so it is restated here.*

**CombatAI — CLIENT (10 edges).** `AiTargetSelector_ResolveOperandValue` (`00321190`) calls the three bounded variable-home getters `00264640` (256 u16 entries, the block pointer at `02098E58`), `00264800` (32 entries, `02098E70`) and `00264D20` (64 entries, `02098E68`), each of which returns 0 unless the bind flag at `02098E20` is set; `AiOrder_EvaluateTargetSelector` (`00301AD0`) and `AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus` (`0030F130`) call `BattleUnit_FindMappedDefinitionSelectorByIndex` (`0031B810`), and `00301AD0` also calls `BattleUnit_GetPartyLeader` (`003272A0`); `AiOrder_EvaluateAndResolveActionTarget` (`003014C0`), `00301AD0` and `BattleUnit_SelectAndCommitNextAction` (`00305AB0`) call `FieldData_GetActiveFieldRecordBit15` (`00377C20`); and the UI-filed `BattleMenu_BuildCommandEntryList` (`0031EB20`), cited here for its `+0x1F0` load, calls `GambitConfig_ClassifyActionTargetPairCompatibility` (`00327A10`). The gambit target selector reads script variable homes that this record's bind installs, and it resolves units and the leader through the same accessors the field map cites; the AI owns none of the record.

**CoreRuntimeScheduling — CLIENT and SERVICE, MECHANICAL (10 edges).** `001EDDA0` is itself filed to that layer: a 27-byte predicate over two globals (`01DFE0C0`, `01F82E38`) that the shake sampler `0037D1F0`, the actor-record gate `004FE930` and the Presentation bodies `0051D310` and `00524320` call, and that the frame-count scalers `00265860` and `00265880` call to decide whether to multiply a count by the frame multiplier at `01DFE0B4`. The boot init burst `0017D4C0` calls the 8-byte lookup adapter `001B1C00`; the field frame `0022A770` calls `00229FA0`, which publishes whether the manager slot still matches the expected index; the cutscene gate's outer body `001EC760` calls `FieldData_GetVariable0` (`00265270`); and the area unload `002628B0` calls `00229EE0`, a 9-byte store of the field frame's per-frame step value at `02064AC8`. Each edge is a scheduler-side helper or frame body sharing a small predicate, getter or setter with this record's readers; none of it is a field of the record.

**RNG_Random_Selection — SERVICE (1 edge).** The shake sampler `0037D1F0` calls `RNG_MT19937_NextFloatClosed` (`00379CE0`), a five-byte jump into the gameplay Mersenne Twister. A camera shake draws from the gameplay stream; this is the crossing the 2026-09-19 note records, and its determinism consequences are routed there.

**Spawn_Encounter_Lifecycle — CLIENT (6 edges).** `SpawnGroup_DispatchPendingCompletionSignals` (`00307030`) calls `0026ADC0`, the setter that writes a u16 into the 64-entry variable home; `SpawnUnit_FinalizeSpawnEntryActivation` calls `BattleUnit_SetupEngagedActionState` (`002FED60`); `Spawn_ValidateCandidateDistanceToPlayers` (`00234DA0`) and `SpawnLifecycle_CheckAndRetireByNativeRange` (`002350C0`) call `0031B810`; and `Spawn_TrySelectCandidatePosition` (`00234AF0`) and `002350C0` call `003272A0`. The spawn lifecycle publishes a group's completion into a script variable home this record binds, and checks candidate positions and retirement ranges against units and the party leader resolved through the page's accessors.

**Status_Periodic_Terminal — CLIENT (9 edges).** `BattleUnit_RecoverFromTerminalStatusSetIfClear` (`00301140`) calls `00311F70`, a Movement-filed 448-byte body that asks the battle mode and compares an actor's world position; `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` (`002F9400`), `BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`), `BattleStats_RemoveStatusesFromMaskAndRecompute` (`0030F690`), `BattleStats_RecomputeDerivedStateAndAutoStatuses` (`0030FED0`) and `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` call the owner resolver `BattleStats_FindOwningBattleUnit` (`0031B860`); and `0030E360`, `0030F690` and `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`) call `00377C20`. The status and periodic bodies find the owning unit through the same resolver every stats body uses and read the field's action-permission bit; that is fan-in on shared accessors, not a status field in this record.

## The `00229FA0` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`00229FA0` (135 B) publishes "the manager slot still matches the expected
index" into `[01F7F4F4]` via `001831D0`. The logic: `0017FFA0()` (`[01F7F4FC]`)
nonzero → publish 1 (`00229FAD`–`00229FB6`); else `002640C0()` fetches the
record — null → publish 0 (`0022A017`); else `edi = 0017FF90()` (the expected
index `[01DF08F0]`, `-1` → publish 0 at `00229FDC`), `[rbx+0x28]` (the
manager-index field above) → `0032F240`, equal → publish 1 (`00229FEA`–
`00229FFD`), else publish 0 (`0022A002`–`0022A012`).

| member | role | interior |
| --- | --- | --- |
| `0017FF90` (7 B) | static getter — `[01DF08F0]` (the expected index) | [`0017FF90`](../../_index/ADDRESS-INDEX.md) |
| `0017FFA0` (7 B) | static getter — `[01F7F4FC]` (the ready flag) | [`0017FFA0`](../../_index/ADDRESS-INDEX.md) |
| `001831D0` (7 B) | static setter — `[01F7F4F4] = ecx` (the published state) | [`001831D0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `002640C0` (record fetch), `0032F240`
(index resolve).

## The `003E9550` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`003E9550` (22 B): `[rcx+0xB8]` null → tail `002A3600` (`003E9560`); a
repeated `002E1040` → `word[rax+0x54]` compare against `ebx` / `edi`
(×4: `003E9588`/`003E95F0`/`003E9650`/`003E969F`), `byte[r9+0x3F3]`
gate (`003E9605`), `xmm3 = [rbx+4]` / `xmm2 = [rbx]` with
`divss xmm0, [01DFE0BC]` (`003E96BB`–`003E96C7`), `002A26A0`
(`003E96DE`).

| member | role | interior |
| --- | --- | --- |
| `002A3600` (71 B) | the null-`+0xB8` tail — `lea 0209C510` buffer (`002A3609`), `001814F0(edx)` (`002A3622`), `byte[rax]` → `byte[[rbx+8]]` copy (`002A362C`–`002A3637`), `byte[rcx+0x3F3]` → `r10d` (`002A3650`) | [`002A3622`](../../_index/ADDRESS-INDEX.md) |
| `001814F0` (44 B) | lookup+format adapter — `001B1C00` ×2 (`001814F8`/`00181502`), tail `001B1240` (`00181511`) | [`00181511`](../../_index/ADDRESS-INDEX.md) |
| `001B1240` (375 B) | `shape%d` name formatter — `0017D2E0` sprintf with `008F8128` = `"shape%d"` (`001B1272`–`001B127D`), `001EDF00` EASTL string init with `008F6600` (`001B1282`–`001B128D`) | [`001B1272`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `002E1040`, `002A26A0`, `001B1C00`,
`0017D2E0`, `001EDF00`, `001B1440`. `001814F0` → `001B1240` is a
member→member tail edge.

## The `003E9320` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`003E9320` (213 B) — an actor-manager op with two arms:
`002E1040` (`003E9347`), then either `002A3830` (`003E93B5`) or
`002A3650` (`003E93D0`), `003E9570` (`003E93E7`), `002E1040` again
(`003E93EE`).

| member | role | interior |
| --- | --- | --- |
| `002A3650` (74 B) | record publish — `rcx = 0209C510` (`002A366D`), `qword[rdx] = rax` (`002A367B`), `r10b` gate (`002A367E`), `word[rdx+0x16] = ax` / `word[rdx+0x14] = r9w` (`002A368B`/`002A368F`), tail `002A7A60` (`002A3694`) | [`002A368B`](../../_index/ADDRESS-INDEX.md) |
| `002A3830` (139 B) | record-publish twin + flag — `byte[rcx+0x3F3] = al` first (`002A3842`), then the same `0209C510` registry link, `word[+0x16]`/`+0x14` writes (`002A387B`/`002A3880`) | [`002A3842`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `002E1040`, `003E9570`, `002A7A60`.
The `0209C510` cell is the shared registry both members publish into.

## The `002642C0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`002642C0` (~190 B) — `byte[+0x10] & 1` gate then `movsxd edx` indexed
walk over `[rcx]` (`002642CA`/`002642CE`/`002642D7`).

| member | role | interior |
| --- | --- | --- |
| `00264260` (93 B) | the twin arm — same `byte[+0x10] & 1` gate and `movsxd edx` index (`0026426A`/`0026426E`) | [`0026426A`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The `00259620` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00259620` (~300 B) — record init: seeds `float -1.0` over the
`02098428` block (`00259637`/`0025963F`).

| member | role | interior |
| --- | --- | --- |
| `0032B8B0` | clamped intensity setter — `byte[rcx] = 0`, `[+0x3C] = maxss(0, minss(1.0, xmm1*0.5 + 0.245…))` (`0032B8B0`/`0032B8D6`) | [`0032B8D6`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The `003DA330`/`003DA370` exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)

`003DA330` (~384 B) — manager-record body.

| member | role | interior |
| --- | --- | --- |
| `002567E0` | `rax = rsp` `0x60` frame, `r14d = 0` walk counter (`002567E0`/`002567F3`) | [`002567E0`](../../_index/ADDRESS-INDEX.md) |

`003DA370` (~119 B) — manager-record body.

| member | role | interior |
| --- | --- | --- |
| `00257830` | `020963F8`/`020964E0` scratch clears; `movsxd r9d << 6` into `02096370` — 64-byte stride records (`00257836`/`00257852`) | [`00257836`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The `003DA400`/`003DD230`/`003E92F0` exclusive-subtree triple — all 3 roots bound (SWE2-FRONTIER, followup queue)

`003DA400` (~167 B) — `movsxd rsi, r9d`, `rbx = rcx` (`003DA40A`/`003DA40D`).

| member | role | interior |
| --- | --- | --- |
| `00257230` | `ecx x 0xBB0` record base + `r8d` sign gate — 2,992-byte stride (`00257230`/`0025723D`) | [`00257230`](../../_index/ADDRESS-INDEX.md) |

`003DD230` (~81 B) — four-register body (`003DD230`/`003DD241`).

| member | role | interior |
| --- | --- | --- |
| `0037DCF0` | `ecx x 0x3D0` into `02ADD980` + `movsxd r8d` — 976-byte stride (`0037DCF0`/`0037DD04`) | [`0037DCF0`](../../_index/ADDRESS-INDEX.md) |

`003E92F0` (~141 B) — `qword[+0xB8]` non-null gate (`003E92F6`/`003E9301`).

| member | role | interior |
| --- | --- | --- |
| `002A7950` | `rsi = rcx` record body (`002A795F`) | [`002A795F`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — frontier hub `002E9B80` (2026-09-18, SWE2-EC7)

`002E9B80` — 41 B, 6 A-measured callers; the two-level dword getter the field map's readers
chain through. Interior verified: `003588B0(ecx)` resolves the manager/side-object
(`002E9B84`), then `[rax + 0xC0]` must be non-null and its `[0]` dword is returned
([`002E9B9A`](../../_index/ADDRESS-INDEX.md)); either null leg returns `-1`. The `0xC0` link is the secondary
context record ~~this map's own `+0xC0` entries describe~~ an actor record's `+0xC0` points at (`rec + 0x350`), not this slot's `+0xC0` *(corrected 2026-10-02, OPUS: `003588B0` returns an actor record — `00358909 mov rax, [rcx + rbx*8 + 8]` out of the slot's pool `[slot + 8]`, generation-checked at `00358913` — and `002E9B8E` reads its `+0xC0`)* — `-1` is the caller-visible "no
record" sentinel, distinct from a stored `-1`.


## Interior citation — frontier hub `002E1040` (2026-09-18, SWE2-EC7)

`002E1040` — 52 B, 14 callers; the 8-row clamped table index. Interior verified:
negative `ecx` becomes 0 (`002E1042`–`002E1046`), `ecx > 7` clamps to 7
(`002E1058`–`002E105F`), and `0215F200 + ecx*0x68` returns the row
(`imul rax, rax, 0x68` at [`002E1050`](../../_index/ADDRESS-INDEX.md)). Eight manager-record
rows of `0x68` bytes, index always in range.

## Interior citation — frontier hub `003A6BA0` (2026-09-18, SWE2-EC7)

`003A6BA0` — 132 B, 10 callers; the manager record's mode-dispatched index→value getter.
`r8 = [02FA7348]` (a data pointer stored inside the image's `.pdata` range — the load is
real; the address is a deliberate citation, not unwind evidence); when `word [r8+0x378]`
carries `0x200`, the index (`-1` reads `[r8+0x90]`,
else `[r8+idx*4+0x10]`) is passed to `002E9B80` ([`003A6C12`](../../_index/ADDRESS-INDEX.md))
and `-1` maps to failure. Without `0x200`, a `byte [r8] == 3` fast path returns
`[r8+idx*4+0x10]` directly; otherwise the index is bounds-checked against `dword [02096B24]`
and translated through the `02096A24` dword table before the same `002E9B80` call. Three
distinct storage layouts behind one accessor — the mode word chooses which.


### Interior citation — frontier hub `003A2B20` (2026-09-18, SWE2-EC7)

`003A2B20` — 53 B, 24 callers: the splat-scale the config-record compose runs
×4. `xmm1 = [rcx]` is multiplied by `shufps(xmm0, xmm0, 0)` — a lane-0 splat of
the `022D8F30`-family global — at [`003A2B47`](../../_index/ADDRESS-INDEX.md);
the product is stored both back to `[rcx]` and to ``022D92E0``, and the
`movsxd` of the stack dword lands in ``022D8F30``. A scale-and-publish
step in the manager record's transform compose.

### Interior citation — frontier hubs `00369760`, `001C00B0` (2026-09-18, SWE2-EC7)

`00369760` — 96 B, 5 callers: bit-gated record check — `bt dword[022D89B8],
r9` must be set and `r9 <= 0xE`, resolves the `0xA8`-stride record at
`022D7FD0`, validates `[+0x10] == [+0x90]` against `[+0x98]`, then calls
`0036A570(ecx=r9, edx=0x3F)` at [`00369772`](../../_index/ADDRESS-INDEX.md)
and returns 0.

`001C00B0` — 250 B, 5 callers (`001B1240` above): `std::map`/`set`
lower-bound — walks the red-black tree comparing each node's `[+0x20..0x28]`
key span against the search range with `00861ED2` (`memcmp`) at
[`001C0118`](../../_index/ADDRESS-INDEX.md), keeps the last `rbp`
candidate, re-verifies it once, and writes either the node pointer or the
end sentinel to `[r15]`.
## SWE2-EC7-20 update (2026-09-18) — `004FF0D0` mid-instruction fragment

`004FF0D0` (56 B) is the `+0xC2` kind dispatcher the `003Axxxx` manager-record
getters reach: `rax = [rcx+0xE0]` fetches the record, `byte[rax+0xC2]` selects
four tail arms — 0 → `00537BA0`, 1 → `00537CC0`, 2 → `00537FF0`, 3 → `005383B0` —
with any other value returning 0. Interior anchor `004FF0D7` (the `+0xC2` kind
read). Callers `003A4290`/`003A56F0`/`003A7EE0`/`003A8290` — the record-getter
cluster this page's field map documents.

## SWE2-EC7-21 update (2026-09-18) — `0046BA50` mod-128 arm + `00426650` slot resolve + `004220F0` mode gate

`0046BA50` (49 B) is the flag-gated record/global select: `call 00263FF0` fetches
the context record, `test [rax+0x10], 1` chooses between `[rax+0x1F0]` (the
record's far field) and, when the bit is clear, `&02CA6050` after zeroing that
global — the pointer the manager-record arms consume. Interior anchor `0046BA5F`
(the `+0x1F0` load). Callers `0031EB20`/`0035E5F0`/`00465120`/`00465690` —
including this page's `00465120`/`00465690` manager-record arms.

`00426650` (288 B) is the two-hop `022C6F28`-row resolver the getter cluster
drives: `word[rcx]` sign-extends × `0x740` into the pool, `00421D70` rates the
row, and a `0xFFFF` word mismatch publishes `{row, ax}` plus flag 1 into the out
record; the walk repeats on `word[rbx+8]` for a second row, then `word[rbx+8]` /
`word[rbx+0xA]` feed two `0042EF90` continuation calls — the results land in the
`[rsi]`/`[rdi]` pair-outs. Interior anchor `0042669B` (the `imul 0x740` stride).
Callers `003A4290`/`003A56F0`/`003A6DF0` — the record-getter cluster.

`004220F0` (119 B) is the `-1`-gated resolve-and-dispatch: `ebx = [rcx+0x18]`,
`0020E600` resolves `[rcx+0x10]`, `002ED570` fetches `[rax+0xD98]`'s `ebx`-th row,
and a non-null row forwards `{row, ebp, esi, rdi}` into `003710E0`; any `-1` or
null short-circuits to `eax = 0`. Interior anchor `00422104` (the `+0x18` index
load). Callers `003A4290`/`003A56F0`/`00421E20`/`0051D310`/`00524320`.

## SWE2-EC7-33 update (2026-09-19) - `0051D310`

`0051D310` (2,121 B) is the record field-map's deep walker - `003AB7F0`/`0020E600`/`0046FBB0`/`0051E510`/`00428940`/`003B6B30`/`003B6B10`/`0036DD80`. Interior anchor `0051D507` (a `0036DD80` call).

## SWE2-EC7-33 update (2026-09-19) - `00524320`

`00524320` (**1,122 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,007 B, a wrong literal in the batch-33 append — the body is 1,122 B per the function list*) is the same map's element pass - `004309C0`/`0042FDB0`/`0026EE00`/`00430B90`/`0020E600`/`00431830`/`004220F0`. Interior anchor `005243CB` (a `004309C0` call).

## SWE2-EC7-34 update (2026-09-19) - `005383B0`

`005383B0` (830 B) is an actor-record deep walker - `[rcx+0xE0]` object, `004FE930` gate, `+0x110` record, `003A56C0`/`003A2B20`/`004FE710`/`004FE4E0`/`0043EEB0`/`002F1D90`. Interior anchor `005383DF` (the `004FE930` call).

## SWE2-EC7-36 update (2026-09-19) - `00465CD0`

`00465CD0` (650 B) is an actor-manager record body - `022C6F28`/`01CEBBA8`/`008C5F78`, `00428CD0`/`00428AF0`/`003E5E70`/`003E5E50`. Interior anchor `00465E98` (a `00428CD0` call).

## SWE2-EC7-36 update (2026-09-19) - `00537FF0`

`00537FF0` (647 B) is an actor-record deep walker - `01CEBBA8`/`01CEBC08`, `0043EEB0`/`003A56C0`/`003A2B20`/`002F1EC0`/`002F1D90` pairs. Interior anchor `0053801F` (a `0043EEB0` call).

## SWE2-EC7-37 update (2026-09-19) - `003DD4C0`

`003DD4C0` (511 B) is the `PendingMaskedRecordMaterializationSweep` the page names - `02B581A0`/`02B58A60`, `0036C1D0`/`0036B160`/`0036C140` pairs plus `0032F240`/`0032F170`/`0032F290`/`00263FF0`. Interior anchor `003DD53C` (a `0032F240` call).

## SWE2-EC7-38 update (2026-09-19) - `00537CC0`

`00537CC0` (466 B) is an actor-manager record body - `022D92E0`/`022D92E4`/`022D92E8` fields, `003A56C0` pair plus `004FE930`/`004309C0`/`0036DD80`/`003A2B20`/`004FEAD0`. Interior anchor `00537CE3` (a `004FE930` call).

## SWE2-EC7-44 update (2026-09-19) - `0035E5F0`

`0035E5F0` (253 B) is a body - `003588B0`/`0046B560`/`0046BA50`/`0046BA90`. Interior anchor `0035E61A` (a `003588B0` call).

## SWE2-EC7-49 update (2026-09-19) - `0025E400`

`0025E400` (188 B) is an `ActorManager_RunFieldRuntimePass` member - `002E5180`/`003588B0`/`00358940`/`003590D0`/`003DA2F0`/`003DD210`. Interior anchor `0025E415` (the `002E5180` call).

## SWE2-EC7-50 update (2026-09-19) - `00313670`

`00313670` (181 B) is a `0031B810`-caller mirror body - `00311F70`/`0031B810`/`003272A0`/`00377C20`. Interior anchor `0031369A` (a `00311F70` call).

## SWE2-EC7-51 update (2026-09-19) - `00421D70`

`00421D70` (172 B) is the `0x740`-stride pool rater - `0020E600`/`002ED570`. Interior anchor `00421D8F` (a `0020E600` call).

## SWE2-EC7-52 update (2026-09-19) - `004FEAD0`

`004FEAD0` (1430 B) is an actor-manager record body - `00398480`/`00538320`/`00537F70`/`005382F0` plus `022D92E0`/`022D92E4`/`022D92F0` fields. Interior anchor `004FEAF9` (a `00398480` call).

## SWE2-EC7-53 update (2026-09-19) - `004FE4E0`

`004FE4E0` (545 B) is an actor-record walker sibling of `004FE710`'s shape - `0036DD80`/`00398F90`/`0039AF70`/`003A2440`/`003A2B20`/`004309C0`/`00808C40`/`00861F08`/`00861F0E` plus `022D92E0`-`022D92F0` tables. Interior anchor `004FE58A` (a `0036DD80` call).


## SWE2-EC7-53 update (2026-09-19) - `004FE710`

`004FE710` (529 B) is an actor-record walker sibling of `004FE4E0`'s shape - `0036DD80`/`00398F90`/`0039AF70`/`003A2440`/`003A2B20`/`004309C0`/`00808C40`/`00861F08`/`00861F0E` plus `022D92E0`-`022D92F0` tables. Interior anchor `004FE7B9` (a `0036DD80` call).


## SWE2-EC7-53 update (2026-09-19) - `004FE930`

`004FE930` (413 B) is the actor-record gate the page names - `00250000`/`00430B90`/`001EDDA0` plus `02064AB0`. Interior anchor `004FE94A` (a `00250000` call).


---

## The camera-shake fields — `+0x1C`, `+0xF0` and `+0x170` (OPUS, 2026-09-19)

Nine rows above left the *not named by any page* column on FABLE's request
`FABLE-REQ-OPUS-ACTOR-MANAGER-SLOT-SHAKE-FIELDS`, which proposed names from the camera-shake
reading published at `16888155b`. **Every offset and width in that proposal verifies from the
bytes. Two of the names do not, and are corrected here rather than adopted.**

### The array

`+0x170` is the base of **four shake drivers of `0x18` bytes each**. Two functions fix that
independently:

```
003DD320  cmp  edx, 3                              ; the stop path bounds-checks the ordinal
003DD323  ja   0x3dd340
003DD325  cmp  qword ptr [rcx + 0xf0], 0           ; ... and the bank gate
003DD32D  je   0x3dd340
003DD332  lea  rdx, [rax + rax*2]                  ; 3*ordinal
003DD338  mov  word ptr [rcx + rdx*8 + 0x178], ax  ; *8 -> stride 0x18, state <- 0

003DD0AC  add  rbx, 0x18                           ; the per-frame walk, from rsi+0x178
003DD0B0  cmp  edi, 4
003DD0B3  jl   0x3dd044
```

| driver field | offset | set where |
|---|---|---|
| authored data id | `+0x00` | `003DD2B1`, from the bank |
| output channel | `+0x04` | `003DD2C0` |
| state | `+0x08` | `003DD2A9` (=1), `003DD338` (=0), `0037D224` (=2) |
| bank index | `+0x0A` | `003DD2B8` |
| time | `+0x0C` | `003DD293` |
| rate | `+0x10` | `003DD2C7` (=`1.0f`) |

### The bank at `+0xF0`, exactly as proposed

```
003DD245  mov   r14, qword ptr [rcx + 0xf0]     ; the bank
003DD27E  cmp   ebp, dword ptr [r14 + 4]        ; COUNT AT +4
003DD282  jae   0x3dd2f6
003DD290  add   rax, rax                        ; index*2 ...
003DD29F  mov   edx, dword ptr [r14 + rax*8 + 0x14]   ; ... *8 -> 16-BYTE ENTRIES, id at +0x14
```

**A null bank disables shake outright** — the per-frame driver `003DCFB0` returns at `003DCFCE`
before touching a driver, and both the start and stop paths re-test it.

### Correction 1 — `+0x1C`/`+0x1E` are indexed by channel, not by draw

The request reads *"the channel that owns draw 0 / draw 1"*. **It is the other way round.** The
starter's last act is:

```
003DD2E4  movsxd rax, dword ptr [rbx + rsi*8 + 0x174]   ; rax = the driver's CHANNEL
003DD2EC  mov    word ptr [rbx + rax*2 + 0x1c], di      ; [0x1C + 2*channel] <- the DRIVER ORDINAL
```

**The channel is the index and the driver ordinal is the value.** The per-frame reader agrees: at
`003DCFF0` it loads `word [rsi+0x1C + 2*i]`, treats a negative as empty (`js`), and uses the value
to compute `3*v` — a driver subscript, not a channel. So these two words are a **channel-to-driver
ownership map**, and the direction matters to anyone reconstructing it: written the other way, a
second shake on the same channel would corrupt a different driver's slot.

### Correction 2 — `+0x174` is the channel, not a "draw tag"

It is the fifth argument of the starter, and when it arrives negative it is replaced by the return
of `005C5230` (`003DD265`), which is the retail stub `xor eax, eax` / `ret`, so the default is always
channel 0 (*2026-09-26, FABLE*). A default is what a channel selector has and a tag does not. It
is then used as the subscript in correction 1. **Named `the output channel`.**

### Refinement — the record table is at ~~`02ADD990`~~ `02ADD980` (corrected 2026-10-02, OPUS), and `+0x28` indexes it

The request says `+0x28` *"is also the record index into the five-record shake table at
`02ADDA34`"*. The index claim holds and the base is off by `0xA4`:

```
0037D1F6  movsxd rax, ecx              ; ecx = [slot + 0x28]
0037D1F9  imul   r8, rax, 0x3d0        ; 0x3D0 per record
0037D208  movsxd rax, r9d              ; the driver ordinal
0037D20B  imul   rsi, rax, 0xf0        ; 0xF0 per driver
0037D212  lea    rax, [rip + 0x2760777]  ; 02ADD990  <- THE BASE   <- corrected 2026-10-02, OPUS - not the base: 02ADD990 = 02ADD980 + 0x10, driver block 0; the same function's 0037D243 lea r9, [02ADD980] reads each record's header qwords (0037D25F, 0037D267), and 0037DCFA uses 02ADD980
```

`0x3D0 = 4 * 0xF0 + 0x10`, which is the four driver blocks plus a sixteen-byte record header, and
`02ADDA34` is ~~`+0xA4`~~ `+0xB4` inside record 0, driver 0's `+0xA4` *(corrected 2026-10-02, OPUS: the record base is `02ADD980`, its sixteen-byte header first)* — a field of the table, not its base. `+0x28` already carried
a name (*the manager index*); this adds what it additionally indexes rather than renaming it.

### What is still not named

**The `0x10` remainder of each `0x3D0` record, and `0xC8` of each `0xF0` driver block, are
unread.** The block's accumulator at `+0xC8` and its `0x10`-stride parameter table at `+0x14` are
identified by use in `0037D1F0`; the rest is not, and no name is offered for it here. **The four
rows this request asked about are named; the block they point into is not explained.**

*(OPUS 2026-09-19, on `FABLE-REQ-OPUS-ACTOR-MANAGER-SLOT-SHAKE-FIELDS`. Verified against `003DD230`
(start), `003DD320` (stop), `003DCFB0` (per-frame) and `0037D1F0` (sampler). See also
[CONTRACT-gameplay-generators.md §12c](../../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md),
where the same sampler turns out to be the sole consumer of the gameplay MT float draw.)*

## SWE2-EC7-54 update (2026-09-19) - `003A2440`

`003A2440` (290 B) is an actor-record walker body - `00250010`/`00398470`/`003A27C0`/`00808C40` plus `01F44830` cookie. Interior anchor `003A247A` (a `00250010` call).

## SWE2-EC7-55 update (2026-09-19) - `003A27C0`

`003A27C0` (242 B) is an actor-record walker body - `00861F14` single call plus `00900360`/`01CEBD80`/`01EF93FC`/`022D9198`. Interior anchor `003A283C` (a `00861F14` call).



## SWE2-EC7-64 update (2026-09-19) - `0043EEB0`

`0043EEB0` (140 B) is an actor-record body - `0036DD80` single call plus `022D92E0`-`022D92EC` quad. Interior anchor `0043EF27` (a `0036DD80` call).


## SWE2-EC7-72 update (2026-09-19) - `0046B560` status-flag sweep measured

`0046B560` (292 B) is the four-unit flag sweep the manager record runs:
for `ebp` 0..3, `00263FF0(ebp)` resolves the unit and when `byte[+0x10]`
bit 0 is set it walks `word[+0x1DE]`..`+0x1D6` clearing `byte[+9]` bit 1
through `00358940`; then `ecx` mode - `0` ORs bit 1 on the arg plus
`r12d` `r15[]` entries through `003588B0` and runs `0046BE80` four
times, `1`/`2`/`3-4` run `0046BAC0`/`0046BD60` three times - the
clear-and-restamp pair on the units' flag bytes.
Interior anchor `0046B5CC` (the `and byte [rax+9], 0xfd` clear).

## SWE2-EC7-73 update (2026-09-19) - `003A56C0` field-load forwarder measured

`003A56C0` (39 B) is the forwarder the manager-record bodies call:
loads `edx = [rdx+0xFC]` and `r8 = movsx byte[rdx+0x102]`, keeps `r9`
stack-spilled, and calls `003A56F0(rcx, edx, r8, movsx)` - the
`+0xFC`/`+0x102` field pair loader.
Interior anchor `003A56DD` (the `003A56F0` call).

## SWE2-EC7-74 update (2026-09-19) - `002F1EC0` vec4 accumulate measured

`002F1EC0` (121 B) is the `022D92E0` accumulator: `[rcx]` and `[rdx]`
movups into the record, then lane-wise `addss`/`shufps` folds write
`[rcx]+[rdx]` componentwise into `022D92E0`..`+0xEC`, and the updated
record movups back to `[rcx]` - the vec4 running-sum the manager
bodies share.
Interior anchor `002F1ED5` (the first `addss` fold).

## Crossing accounted 2026-09-19 (FABLE): RNG_Random_Selection

**RNG_Random_Selection - SERVICE.** The shake sampler `0037D1F0` on this page calls `00379CE0`, a five-byte jump to the
gameplay Mersenne Twister's closed-interval float. This is the page's own finding - a camera shake draws from the
gameplay stream - named as the crossing it is; the consequences for determinism are routed in
`FABLE-REQ-OPUS-SHAKE-IS-A-CONSUMER-OF-THE-GAMEPLAY-MT-STREAM` and `FABLE-REQ-ASTRA-MT-CURSOR-ACROSS-A-CAMERA-SHAKE`.

## SWE2-EC7-85 update (2026-09-20) - `0041E490` paired-helper tail measured

`0041E490` (57 B) is the two-call forward the manager callers run:
`003AB880(rdx)` then `003AB940(rdx)` on the argument record, then a
tail `00409D60([rdi+0xD90], rdx)` through the owner's `+0xD90` table.
Interior anchor `0041E4C4` (the `00409D60` tail).

## SWE2-EC7-87 update (2026-09-20) - `003D9B80` runtime-record reset measured

`003D9B80` (182 B) is the large reset the manager-map callers
run: `0032B790(rcx+0x2B0)` clears the sub-record, `[+0x190]`
loses `0x2D00` and gains bit 7, `[01EFE990]` and `[+0x1AC]` are
armed, `+0x1DC`/`+0x2A4`/`+0x1F4`/`+0x1FC`/`+0x204`/`+0x21C`/
`+0x2A8` zero, `+0x208`/`+0x20C` take -1.0f, `+0x214` takes
1.0f, `+0x1C8` takes -1, and `003D9C40(rbx)` finishes.
Interior anchor `003D9C1F` (the `003D9C40` call).

## SWE2-EC7-88 update (2026-09-20) - `003D9C40` six-edge length pass measured

`003D9C40` (473 B) is the polyline edge pass the `003D9B80` reset
tails into: six consecutive point pairs on 0xC stride from `+0x10`
take `00861F14(dx^2 + dy^2)`, each length lands in the point's
third float (`+0x18`, `+0x24`, ... `+0x54`), then all six are
divided by their sum; `+0x1D0` is zeroed unconditionally at index
3 while `+0x1D4` (indices 1-2) and `+0x1D8` (indices 4-5) zero on
the `dword[+0x2A0]` parity gate - a normalized edge-length record.
Interior anchor `003D9D31` (a `00861F14` call).

## SWE2-EC7-90 update (2026-09-20) - `003A69F0` three-table keyed resolve measured

`003A69F0` (428 B) is the keyed resolve the manager callers
run: `edx` selects one of three word tables
(`01EFAC60`/`01EFAC80`/`01EFAC90`), `ecx` must not be -1, and
the `022C6F28 + ecx*0x740` record must pass its `+0x284` gate;
`003A6E60` maps the `01EFAC7C`-indexed byte to a word-table
entry written at `+0x40`, the `0x100` value submits through
`00421E20` and anything else through `00426770`, with `+0x44`
taking the result key - returning 1 on a completed submit.
Interior anchor `003A6ABA` (the `00421E20` call).

## SWE2-EC7-97 update (2026-09-20) - `002EB930` measured

`002EB930` (146 B) is the double-dispatch teardown `0026B0C0`
and `002E28E0` call: `rcx`'s `[+0xC0]` word must resolve, then
the `0x740`-stride record is checked twice - each pass needs
`[+0x284] != 0` and runs `004288B0(rcx, -1)`, the second as a
tail `jmp` - the two-shot -1-parameter call the manager record
runs on teardown.
Interior anchor `002EB979` (the first `-1` arm).

## SWE2-EC7-98 update (2026-09-20) - `002E1F40` + `002E1E00` measured

`002E1F40` (52 B) and `002E1E00` (52 B) are the twin clamped
byte writers `00348DF0` and `0034ADA0` call: `ecx` is
clamped to `[0, 7]` (negative becomes 0, above 7 becomes 7)
and `dl` lands at `ecx*0x68` into an eight-slot `0x68`-
stride table - `002E1F40` at `0215F23C`, `002E1E00` at
`0215F238`, the two arms' different `rip` displacements
resolving to the same base - the paired slot writes the
manager record applies.
Interior anchors `002E1F70` and `002E1E30` (the indexed
stores).

## SWE2-EC7-101 update (2026-09-20) - `002A7A60` measured

`002A7A60` (98 B) is the indexed record fetch `002A3650`
and `002A3830` call: `[[rcx]+0x10]`'s `word[+0x14]`-indexed
entry plus `word[+0x16]` selects an `8`-stride record in
`[[rcx]+0x18]`; `+0x18`/`+0x1A` take its first two words,
`+0x1C`/`+0x1E` take the `0xFFF`-split of its `+4` dword,
and a `0xFF` `byte[+0xD]` absorbs `byte[+7]` - the
dual-nibble packed fetch the field map routes through.
Interior anchor `002A7A88` (the record read).

## SWE2-EC7-105 update (2026-09-20) - `00263E40` measured

`00263E40` (14 B) is the indexed pointer
`003DBCF0`, `0050D8F0` and `0050DAD0` call:
`rcx + dword[rcx + 0x4C] + movsxd(edx)` -
the variable-row offset arithmetic that
reaches into the record's trailing region.
Interior anchor `00263E44` (the `+0x4C`
offset add).

`00542740` (4603 B) is the `022D8F90` counter arm `00524320` runs when `r9d` is nonzero: `[rcx+4] + 1` capped at `0x20` publishes into `022D8F90` and back to `+4`, the `+0xB0` vector loads, then `00861F14` x9 with `0046F460`, `00202E10`, `00202B70` and the `00543xxx` local arms - the element pass's capped-counter field arm.

Interior anchor `005434F5` (function `00542740`).

`0026D3E0` (303 B) is the per-record dispatch `0026CE60` runs over `[rcx+0x78]`'s `dword[rax]`-counted list: each entry `0020E600`-decodes `dword[rbx]` twice, `edi = [rsi]` dereferences `0x7000000`-tagged handles through `r12`, `word[rbp+r12]` + `00358940` fetch the record, and `(edi>>24)&7` (<=5) selects a six-arm jump-table tail - the manager init's per-entry value-kind apply.

Interior anchor `0026D45F` (function `0026D3E0`).

`0046BD60` (284 B) is the filtered sub-record enumerator `0046B560` runs: `00263FF0` yields the record (exit unless `byte[+0x10] & 1`); `word[+0x1DE]` to `word[+0x1DE] + word[+0x1D6]` indices resolve through `00358940`, skipping entries with `byte[+0x18] == 1`, `00263C20 == 6`, `byte[+0xE] & 0x20` clear, or failed `002E9FE0`/`002EA6A0`; survivors with `00263BE0 == 1` still need `002647B0` or `002675C0` true; the emit packs `((word[+0x16] & 0x7FF) << 4 | (r12 & 0xF)) << 16 | index` into `[rax+0x1F0]`'s list - the manager's collected (record-id, class, slot) triples.

Interior anchor `0046BDDF` (function `0046BD60`).

`0046BD60` (284 B) is the filtered sub-record enumerator `0046B560` runs: `00263FF0` yields the record (exit unless `byte[+0x10] & 1`); `word[+0x1DE]` to `word[+0x1DE] + word[+0x1D6]` indices resolve through `00358940`, skipping entries with `byte[+0x18] == 1`, `00263C20 == 6`, `byte[+0xE] & 0x20` clear, or failed `002E9FE0`/`002EA6A0`; survivors with `00263BE0 == 1` still need `002647B0` or `002675C0` true; the emit packs `((word[+0x16] & 0x7FF) << 4 | (r12 & 0xF)) << 16 | index` into `[rax+0x1F0]`'s list - the manager's collected (record-id, class, slot) triples.

Interior anchor `0046BDDF` (function `0046BD60`).

`0024DCE0` (231 B) is the `ecx`-mode probe `00524320` runs: mode 3 walks the `00263FF0()`/`00263C30()` count of `00358940`/`003589B0` entries, calls `002E9B80` on each and counts how many pass before the tally reaches `edx` (a final `002E9B80` on the last qualifier must not be `-1`); mode 2 answers via `003A4220(edx)`; mode 0 requires `02F97348` non-null and tail-jumps `003A3FD0(-1)`; anything else returns `-1`

Interior anchor `0024DD74` (function `0024DCE0`).

`0046BE80` (215 B) is the filtered index pack `0046B560` runs: iterates slots ~~`[+0x1D6] .. +0x1D6+[+0x1DE]`~~ `[+0x1DE] .. [+0x1DE] + [+0x1D6]` *(corrected 2026-10-02, OPUS: `0046BEA0` loads the start from `+0x1DE`, `0046BEAC` the count from `+0x1D6`)* of the `00263FF0()` manager object, `00358940`-resolves each, keeps only entries with `byte[+0x18] != 1`, a live `002E97B0` result whose first dword != -1, and `byte[+9]` bit 1 clear - packing `((+0x16 & 0x7FF) << 4 | (+0x15 & 0xF)) << 0x10 | u16[+0x00]` into `[+0x1F0]` and counting in `ebp`

Interior anchor `0046BED5` (function `0046BE80`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-actor-manager-record-field-map-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00263AC0` | 118 B | returns 0 for a null `rcx` and returns byte `rcx+0xF` zero-extended when it is not 2; when it is 2 it saves qword `02099D70`, stores `02098E10` there, calls `003590D0` (`rcx` unchanged) and, when that returns non-zero r, `003588B0(r)` (else uses 0), restores `02099D70`, and returns 1 when `rcx` equals that result, else 2 | `00263AD3`, `00263AEF`, `00263B01`, `00263B0D`, `00263B1E` |
| `002A26A0` | 122 B | returns at once when bit 7 of byte `rcx+0x3F3` is set; otherwise sets bit 3 of that byte and takes the `0x60`-byte entry e at `qword rcx+0x3F8 + 0x60*edx` (sign-extended); when the sixth (stack) argument is 0 it clears bit `0x10` of dword `e+8` and stores `xmm2`/`xmm3` to floats `e+0x24`/`e+0x28`; else it sets that bit, stores the fifth (stack) argument's low word to word `e+0x5C`, the old floats `e+0x24`/`e+0x28` to `e+0x48`/`e+0x50`, `xmm2` and `xmm3` minus those old floats to `e+0x4C`/`e+0x54`, 0 to word `e+0x58` and the sixth argument's low word to word `e+0x5A` | `002A26A9`, `002A26AD`, `002A26CD`, `002A26DC`, `002A2715` |
| `00345CD0` | 336 B | takes three floats f1, f2, f3 from three successive `00267DB0(r9)` calls and a value v from `00267E10(r9)`, and returns when a = `00359CA0(v, 1, 1)` is null or `002EA6A0(a)` is 0; otherwise calls `00264420(a)` (b), `0030BEB0(a)` (d), `0035A720(a, 0)`, `002ECF10(a, b, 2)`, then calls `00267F60(r9, x)` four times with x = f3, f2, f1 and the `003590B0()` result, then `00357A20(rcx, a, r8, r9)` with the incoming `rcx`, `r8`, `r9`, `002EB430(00263F40(a))`, `0026C120(a, 2)` and `00269D80(a, 1, d)` | `00345D2B`, `00345D46`, `00345D7F`, `00345DC2`, `00345DEF` |
| `00537BA0` | 117 B | returns 1 when `004FE930(rcx)` is 0; otherwise calls `003A56C0(qword rcx+0xE0 + 0xD0, rcx, rcx+0x110, stack buffer)` and returns 0 when that is 0, else calls `004FEAD0(rcx, buffer)` and returns 1 | `00537BB9`, `00537BC3`, `00537BE2`, `00537BF3`, `00537BF8` |
