---
system: Script variables — the six storage classes behind PUSHV / POPV, and where each one lives
category: 01-Script-VM-Native-Bridge
status: AUDITED
owner_layer: Script_VM_Native_Bridge — the resolver and the opcodes; the banks belong to world persistence
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the variable resolver 00262440 and its four callers read in full; the two class jump tables
    decoded from the image; the six base pointers traced to their installers in the binder and the
    manager runtime initialiser; every us .ebp script's descriptor table decoded (1,114 files) and the
    decompiler's scope enum (ff12-script CScriptContainer.h) matched against the engine's class numbers
corpus_validated: "1114 / 1115 us .ebp scripts, 2026-09-11 (evt_t0020 is not an EBP2 container)"
last_reviewed: 2026-09-11
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-script-variables-pass-1
  crossref_clean: true
  last_pass_kind: falsification
---

# Script variables — the six storage classes behind `PUSHV` / `POPV`, and where each one lives

> **A script variable is a 32-bit descriptor in the script image, and the descriptor's class says
> which of six memory homes the value lives in.** Two of the homes are the *save image* — the
> `global` class addresses the persistent payload directly, the `scratch2` class a bank that world
> persistence exports and imports per area group — one is a per-field bank cleared on every field
> transition, and three are inside the loaded script image itself. Which class a variable has is
> authored: it is the keyword the script's source used.

## 1. What the player sees

Everything a script remembers: whether a chest was opened, which cutscene take has played, a
counter an event increments, a flag a quest sets in one area and tests in another. When such a value
survives a save it is because its class is `global` or `scratch2`; when it is gone after a map change
it was `file`, `local` or `scratch1`. The decompiler prints the class as the declaration keyword —
`import scratch1 short scratch1_var_1 = 0x10;`, `int file_var_s0_1; // pos: 0xc0`,
`float local_var_s4f5_1; // pos: 0x40` — and the engine reads the same three bits.

## 2. Native mechanism

### 2.1 The opcodes

Six of the interpreter's opcodes go through one resolver, `FUN_00262440`
(`ScriptVariable_Resolve` below), called with the **ActorManagerSlot** in `rcx` (the interpreter's
`r13`, [§14 of the interpreter page](worldactor-scriptvm-interpreter.md)), the **actor record** in
`rdx` (`r15`), the value stack in `r8`, the variable index in `r9w` (the opcode's 16-bit operand,
`bx`) and a 0x30-byte out-record on the caller's stack:

| opcode | mnemonic | handler | what it does with the resolved variable |
|---|---|---|---|
| `0x48` | `PUSHV` | `00267FC0` | loads it by width (`u8`/`s8`/`u16`/`s16`/`s32`/`f32`, the descriptor's top nibble selects the case) and pushes it as int (tag 1) or float (tag 2) |
| `0x49` | `POPV` | `00267E60` | pops the stack top, coerces to the variable's kind (`cvttss2si` / `cvtdq2ps`) and stores it through `0026D530`; ~~the slot's `+0x28` index and a flag from the pop select a notification (`0032F240`)~~ *(corrected 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's POPV-lookup return)* when the slot's `+0x28` is 1–3 and the pop's flag is clear it calls the read-only lookup `0032F240`, whose returned id `POPV` discards (the store overwrites `eax` first), so no notification is emitted on this path |
| `0x4A` | `PUSHDBG` | `0026178F` | resolves the variable with a static string table in the fifth argument — a debug print path |
| `0x4B` | `PUSHP` | `00268100` | pushes a **reference**: the descriptor with the width-scaled element index added and the **width nibble** forced to 7, tag 1 — this is how an array element is passed. ~~the class forced to 7~~ **the class is *preserved*** (`and r9d, 0x7000000` / `or r8d, r9d`); `0x70000000` is bits 28–30, the **width** field — corrected 2026-09-13, §9. *(Qualified 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's reference-carry return; static, [`script-vm-arith-consumers`](../../_index/candidates/script-vm-arith-consumers/README.md) R.)* Both hold only while the 24-bit offset plus the width-scaled index stays in `0`–`0xFFFFFF`. The add is a plain 32-bit `add r8d, edx` after the mask, and nothing masks the sum before the store (`00268194`). So `02FFFFFF` + 1 packs as `73000000`, class 3, and `02000000` − 1 as `FFFFFFFF`, class 7 and width 15. The byte at `+0x44` keeps the original width. These are calculations; no shipped reference of either kind is claimed. |
| `0x46` | `DVAR` | `00261742` | pops one int and calls `0016D6A0` as `(slot.+0x28, poppedInt, &02099D48)` — that callee's body is `C2 00 00`, **`ret 0`**, so `DVAR` is inert. ~~that callee is the CFG stub~~ — it is the **folded no-op** carrying at least three proven identities ([`B-2/a`](../../_index/OPEN-QUESTIONS.md)); naming it "the CFG stub" is the reading that row warns against. Corrected 2026-09-13, §9 |
| `0x62` | `INCINITTAG` | — | not a variable opcode; listed on the interpreter page |

### 2.2 The descriptor

The slot's `+0x78` (`payloadSectionE`, the binder's rebase of the image header's `+0x28` — [the
section_000 sheet](../../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md)
lists it as "u32 count then 8-byte records") is the **variable descriptor table**. The resolver
reads `[table + index*8 + 4]`, the first dword of record *index* after the count:

```
bits  0..23   offset     byte offset inside the class's home (24 bits)
bits 24..26   class      0 global · 1 file · 2 local · 3 (unused) · 4 scratch1 · 5 scratch2 · 7 array
bit  27       float      1 = the value is float32 (pushed with tag 2)
bits 28..31   width      0 u8 · 1 s8 · 2 u16 · 3 s16 · 4 s32 · 5 f32
```

The decompiler's `enVarScope` (`CScriptContainer.h`: `GLOBAL = 0, FILE = 1, LOCAL = 2,
SCRATCHPAD1 = 4, SCRATCHPAD2 = 5, TABLE = 7`) is the same numbering — its authors read the same
switch. Class 7 is an **array**: the offset points at a header in the image — element descriptor
dword at `+0`, dimension count `u16` at `+4`, dimensions from `+8` — the resolver pops one index per
dimension from the value stack, **clamps** each into `[0, dim-1]` (`cmovns` / `cmovl`, `002624D2`–
`00262537`: an out-of-range script index reads the edge element, it does not fault), flattens
row-major, and then resolves the element's class with the same six-way switch. *(Qualified 2026-09-28,
FABLE, Claude Opus 5.5, on ASTRA's array-clamp return; static,
[`script-array-clamp`](../../_index/candidates/script-array-clamp/README.md).)* The clamp is
`min(max(index, 0), dim - 1)` with the dimension read as a signed dword, so the edge element is read only when the dimension is
1 or more. A dimension of 0 gives index -1, one element before the array, and ~~a negative dimension gives `dim - 1`~~ a
negative dimension gives `dim - 1` computed in 32 bits: -2 gives -3, but a dimension of `INT_MIN` (`80000000`) wraps, because the
dword load zero-extends and `lea eax, [rsi - 1]` keeps the low dword, so every index reads element +2147483647 *(corrected
2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's signed-minimum return; static,
[`script-array-signedmin`](../../_index/candidates/script-array-signedmin/README.md))*. This stage rejects neither. "Does not fault" describes the clamp, not a storage-safety guarantee, and whether any shipped array has a
dimension of 0 or less is not claimed. *(Qualified 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's flatten-width return; static, [`script-vm-arith-consumers`](../../_index/candidates/script-vm-arith-consumers/README.md) F.)* The flatten runs in 32 bits. It walks the dimensions last first, from product 1 and sum 0, with `imul eax, r8d` / `imul r8d, esi` / `add r10d, eax` (`0026251F`–`00262527`), so the product and the sum wrap modulo 2^32. The sum is stored as a dword at record `+0x1C` (`00262672`) and read back sign-extended (`0026D537`). A per-axis clamp therefore does not make the flat index non-negative: dimensions 65536 × 65536 with indices (32768, 0) give `80000000`, which is read as INT_MIN. That is a calculation; no shipped array of that size is claimed.

**A store saturates by width, and the s16 range is off by one** *(FABLE, Claude Opus 5.5, 2026-09-28; static,
[`script-store-saturation`](../../_index/candidates/script-store-saturation/README.md); ASTRA executed the store leaf in
isolation).* `POPV` writes through `0026D530`, which takes the width from bits 28..31 and clamps before storing:
- u8 into `[0, 255]`, s8 into `[-128, 127]`, u16 into `[0, 65535]`;
- s32 and f32 copied as a raw dword;
- widths 6 and 7: nothing stored.

The s16 arm (`0026D5C4`) clamps into **`[-32767, +32768]`** and stores the low word, not the usual `[-32768, 32767]`.
`PUSHV`'s s16 read sign-extends (`0026802F`). So a script that stores +32768 (or more) into an s16 variable reads back
**-32768**, the one case where a store flips the sign; a store of -32768 reads back -32767. Whether any shipped script
stores such a value is not claimed.

**The conversion comes first.** For an integer variable, `POPV` converts a float operand with `cvttss2si` (`00267F4C`)
*before* the clamp. That truncates toward zero, and turns any float at or above 2^31 into `0x80000000`. So 1.75 stores 1,
and the largest float below 2^31 stores 255 into a u8. But 2^31 itself stores **0** into a u8 and `0x8001` into an s16: one
step larger lands at the bottom of the range instead of the top. (Static; ASTRA executed the stage in isolation. The
`0x80000000` result assumes the invalid exception is masked.) In the other direction, an int stored into a **float**
variable goes through `cvtdq2ps` (`00267ED2`). That rounds by MXCSR's rounding mode rather than truncating, and the f32
store copies the result as it is. Ints up to 2^24 convert exactly, but 16,777,217 becomes 16,777,216 under
round-to-nearest and 16,777,218 under round-up. Round-up means toward +infinity for negative ints too, so it shrinks their
magnitude: −16,777,219 becomes −16,777,220 under round-to-nearest (a tie, resolved to the even significand) and
−16,777,218 under round-up *(added 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's negative-rounding return; static,
[`script-float-rounding-signed`](../../_index/candidates/script-float-rounding-signed/README.md))*. The game's MXCSR is not
established here.

### 2.3 The six homes, from the two jump tables

The resolver has two class switches — one for scalars (`002626A8`) and one for the element of an
array (`00262690`) — with the same six targets, decoded from the image rather than read off the
listing order:

| class | keyword | base pointer | installed by | what it is |
|---|---|---|---|---|
| 0 | `global` | slot `+0x48` | the binder `0026CAF8`: `SaveImage_GetPersistentPayloadBase()` (`002EF2B0` = active buffer `+0x200`) | **the save payload itself.** Shipped scripts declare 9,448 globals at 587 distinct offsets, `+0x200`–`+0xCF4` of the payload (586 of the 587 above `+0x200`; the one at `+0` is the kind-3 operand bank the save page already knows) |
| 1 | `file` | slot `+0x40` | `ActorSystem_InitializeManagerRuntime` `0026D2F6`: `payload + [payload + 0x38]`, only when the slot's `+0x40` is still NULL (the binder zeroes it at `0026CAF4`) | a data area **inside the loaded script image** (header `tableOff38`) — per script, gone when the image is |
| 2 | `local` | the callback at slot `+0x98` = `00264E30` | the binder `0026CB76` | `[slot + 0x50] + [[record + 0x40] + 0x1C]`: the image's `+0x48` region (~~it begins with the name pool~~ **the local-variable storage**, `+0x44` bytes, zero in the file; the name pool is the next field `+0x4C` — corrected 2026-09-12 from a census of all 1,114 images, [the section-000 page](../../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md)) plus a per-actor offset taken from the actor's authored entry (`record + 0x40`, its `+0x1C` — ff12-script's `stackBegin`) — **per actor, inside the image** |
| 3 | — | `img + [img + 0x40]`, where `img = *(slot + 0)` | resolved inline (`002625D9`/`00262633`) | a second in-image area (header `tableOff40` — **the msp region**, what a `0x03xxxxxx` packed reference addresses; the trap table lives there, corrected 2026-09-12); **no shipped script declares a class-3 variable** |
| 4 | `scratch1` | slot `+0x58` = `02099DF0` | the binder `0026CB2D` | a 0x200-byte static bank, `memset` to zero by `WorldPersistence_ResetBanksForFieldTransition` (`0026DB80`) on **every** field transition and at initialisation (`00268353`); **not referenced by the export/import pair** — per-field scratch |
| 5 | `scratch2` | slot `+0x60` = `02099FF0` | the binder `0026CB38` | the **group persistent bank**: exported to the save image by `0025D8E0` and imported by `00269A20` ([the save payload map](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md) `+0xE040` / `+0x2E250`); cleared on a field transition when the destination field's **persistence group** differs from the previous field's (§2.5), and unconditionally when transition option bit 3 is set — per-group scratch that survives saves |

Widths in the corpus (descriptor census, [`script-variables-by-script.tsv`](script-variables-by-script.tsv)):

| class | variables | scripts | distinct offsets | offset range | widths |
|---|---:|---:|---:|---|---|
| 0 `global` | 9,448 | 738 | 587 | `0x0`, `0x200`–`0xCF4` | u8 4,478 · s8 1,508 · u16 139 · s16 648 · s32 1,002 · f32 1,673 |
| 1 `file` | 9,995 | 936 | 757 | `0x0`–`0x1674` | u8 2,494 · s8 3,244 · u16 28 · s16 417 · s32 2,028 · f32 1,784 |
| 2 `local` | 15,766 | 930 | 199 | `0x0`–`0x216` | u8 2,624 · s8 5,204 · u16 129 · s16 138 · s32 3,889 · f32 3,782 |
| 4 `scratch1` | 2,292 | 750 | 74 | `0x0`–`0xD9` | s16 2,044 · s32 103 · u8 101 · f32 24 · s8 17 · u16 3 |
| 5 `scratch2` | 2,343 | 328 | 77 | `0x2`–`0xC8` | u8 952 · s16 858 · s8 306 · f32 174 · s32 53 |
| 7 array | 3,622 | 639 | — | headers `0x510`–`0x45BC0` | elements: 1,956 `file` + 182 two-dimensional, 881 `global`, 489 `local` + 10 two-dimensional, 95 `scratch2`, 9 `scratch1` |

The class-4 and class-5 totals equal the decompiler's `import scratch1` (2,292) and `import
scratch2` (2,343) declaration counts exactly, which is the check that the class numbers and the
keywords are the same thing.

### 2.4 The global class is a map of the save payload nobody had

[`script-global-variables-by-offset.tsv`](script-global-variables-by-offset.tsv) lists every payload
offset a shipped script declares as a `global`, with how many scripts declare it and at what widths.
The save payload field map has **one** row between `+0x200` and `+0xD00` (`+0xA00`), because its
census follows the buffer getters and this region is reached only through the slot's `+0x48` by the
resolver: **`+0x200`–`+0xCF4` of the persistent payload is the script-global variable space**, ~~0xAF5~~ 0xAF6 *(corrected 2026-10-02, OPUS: the last declared global is a `u16` at `+0xCF4` in 101 shipped scripts, [`script-global-variables-by-offset.tsv`](script-global-variables-by-offset.tsv), so the space runs to `+0xCF5`)*
bytes that scripts own and the engine never interprets. The offsets are a shared authored table, not
per-script choices: **no offset is declared at two different widths anywhere in the corpus**, one
offset is declared by 575 scripts, and 110 by a single script. Which script owns which byte, and where the
decompiler's flag names come from, is a cross-reference for the save page to take (FZ-22).

### 2.5 What a field "group" is — the map-reference row's persistence group id (FZ-24, 2026-09-12)

`WorldPersistence_ResetBanksForFieldTransition` (`0026DB30`) clears `scratch1` unconditionally
(`0026DB80`), then decides `scratch2` (`0026DB8A`–`0026DC2E`):

```
old = row(WorldTransition_GetPreviousFieldId()).+6        ; payload +0x104C -> [02099D88] rows, 8 bytes each
new = row(WorldTransition_GetActiveOrPendingFieldId()).+6 ; payload +0x1044
if new != old:
    if !(payload.+0x1062 & 0x20): WorldTransition_ClearFlag1062_Bit04()   ; clears mask 0xFB of +0x1062
    memset(02099FF0, 0, 0x200)                                            ; scratch2 cleared
if WorldTransition_GetOptions() & 8: memset(02099FF0, 0, 0x200)          ; payload +0x1054 bit 3 forces it
```

The rows are the **map-reference table** — the loaded file image at `02099D88` whose header `+4`
locates 8-byte rows indexed by field id ([the field-environment page](../../03-World-Area-Field/choosing-the-field-environment-variant.md)), and the word at `+6` is exactly what
`MapRef_GetPersistenceGroupId` (`00264F90`, 49 B, inlined here) returns; the row's `+0` is
`MapRef_GetPrimaryFieldValue` and its `+2` the environment-variant selector. So a **group is the
set of fields sharing one persistence group id in the map-reference file**, and `scratch2` is the
bank a script keeps while the player stays inside that set — across saves, because the bank rides
the save image. Persistent flag `+0x1062` bit 5 does *not* gate the clear (an earlier reading here
said it did — corrected): it gates only the `ClearFlag1062_Bit04` call. Which fields share which
group id is authored in that file and not decoded here; the accessor's nineteen callers
([the field-record table page](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md)) include `WorldTransition_StageFieldTransition` and
`SaveImage_FinalizeHeaderAndChecksum`, so the same id also reaches the save header.

**The load flag `0209AC10` and the only scripts that read it (2026-09-13).** The other `scratch2` reset,
`00268320`, keeps the bank when the dword `0209AC10` is non-zero (F-3). The save controller sets that dword to 1 on its
restore path (`00582E98`); staging field `0xC` and call id `0x05BF` (`00355E80` → `00287D00(0)`) set it to 0, and call id
`0x05BE` (`00355940` → `00286000`) returns it to the script. In the 1,114 decompiled `us` scripts the two calls occur
**only in the 100 `tri_*` scripts, three times each and always in the actor `トライアル監督`** (trial director): `0x05BE` in
`init()` and in `main(1)`, `0x05BF` once in `main(1)` after its entry sequences. Where the flag reads 0, those branches
run the stage-entry work (fade-out, HUD and battle suspension in `init`; message, full-screen-menu and music sequences in
`main`); the clear then makes the next entry run them. So in the shipped scripts the flag is consumed by the Trial Mode
director alone, and a set flag skips its entry sequences once. Census:
[`restore-flag-script-uses/census.py`](../../_experiments/evidence/restore-flag-script-uses/census.py) →
[`census.out.txt`](../../_experiments/evidence/restore-flag-script-uses/census.out.txt) (control: `mapsoundplay(` 3,838).
When a real load runs these relative to the area controller's restore route is ASTRA's `L-13`.

## 3. Key addresses

| address | role |
|---|---|
| `00262440` | `ScriptVariable_Resolve` (`FUN_00262440`, 591 B): descriptor → (kind, address); the two class switches at `002626A8` (scalar) and `00262690` (array element) |
| `00267FC0` / `00267E60` / `00268100` | `PUSHV` / `POPV` / `PUSHP` bodies |
| `00264E30` | the `local` resolver installed at slot `+0x98`: `[slot+0x50] + [[record+0x40]+0x1C]` |
| `0026C8C0` | `ActorManager_BindLoadedDefinitionPayload` — installs `+0x48` (`0026CAF8`), `+0x58` / `+0x60` (`0026CB26`–`0026CB38`), `+0x78` (`0026CB60`–`0026CB6B`), `+0x98` (`0026CB6F`–`0026CB76`), zeroes `+0x40` (`0026CAF4`) |
| `0026CE60` | `ActorSystem_InitializeManagerRuntime` — fills `+0x40` from the image's `+0x38` offset when NULL (`0026D2E7`–`0026D2F6`) |
| `02099DF0` / `02099FF0` | the `scratch1` / `scratch2` banks, 0x200 bytes each |
| `0026DB30` | `WorldPersistence_ResetBanksForFieldTransition` — the unconditional `scratch1` clear |
| `00268320` | `WorldPersistence_ResetBanksAndMarkInitializationState` — clears `02099FF0` only when `0209AC10` is zero **and** `01E0C3EC` is not, then clears `02099DF0` unconditionally (`00268336`–`00268359`, both `0x200` through `00861EC0`); sets payload `+0x1061` when a fresh read of `0209AC10` is zero. `0209AC10` is 1 after the save controller's restore path (`00582E98`) and 0 after staging field `0xC` (`00314754`); `01E0C3EC` is 1 in the image and after staging field `0xC` (`00314759`), 0 after `00584210` (`00584386`) — so a load keeps `scratch2` and a return to field `0xC` wipes it (F-3, weather page) |
| `0025D8E0` | `WorldPersistence_ExportGroupPersistentBank` — reads `02099FF0`, writes the caller's buffer (`0025D8F7 movups xmm0, [rax]`) |
| `00269A20` | `WorldPersistence_ImportGroupPersistentBank` — reads the caller's buffer, writes `02099FF0` (`00269A37 movups xmm0, [rcx]` → `00269A41 movups [rax-0x80], xmm0`). Both copy 4 × `0x80` = `0x200` bytes |

## 4. Data structures and formulas

```
descriptor = u32 [slot+0x78 + 4 + index*8]
class      = descriptor >> 24 & 7;  width = descriptor >> 28;  isFloat = descriptor >> 27 & 1
base       = { 0: [slot+0x48], 1: [slot+0x40], 2: ([slot+0x98])(slot, record), 3: img + [img+0x40],
               4: [slot+0x58], 5: [slot+0x60] }[class]        /* img = *(slot + 0) */

/* class 7: the header is at img + (descriptor & 0xFFFFFF); the element descriptor is its +0,
   the dimension count u16 its +4, the dimensions from +8. The resolver clamps each popped
   index into [0, dim-1] and flattens row-major into flatIndex, which it returns SEPARATELY.
   flatIndex is 32-bit arithmetic (imul / add, wrapping), stored at +0x1C as a dword and read sign-extended (2026-09-28).
   [0, dim-1] holds only for dim >= 1; below that the result is max(index, 0) < dim ? max(index, 0) : signed32(low32(dim - 1)),
   so dim 0 gives -1 and dim INT_MIN gives INT_MAX (section 2.2). */

address    = base + (elementDescriptor & 0xFFFFFF)            /* the element BASE, not the element */
element    = address + flatIndex * sizeof(width)              /* the HANDLER scales, not the resolver */

PUSHV: push (isFloat ? tag 2 : tag 1) the value loaded at `element` by `width`
POPV:  store the popped value at `element`
```

> **The scaling is the part a reimplementation drops.** The resolver hands back a base address and
> a flattened *index*; every loader then applies its own `× 1 / × 2 / × 4` — `[rcx + rax]`,
> `[rax + rcx*2]`, `[rax + rcx*4]` in `PUSHV`, and an explicit `add edx, edx` / `lea edx, [rdx*4]`
> switch in `PUSHP`. **And the push tag comes from bit 27, never from the width nibble** — the two
> fields are independent and nothing cross-checks them (§9, 2026-09-13).

## 5. Call chain

`WorldActorScriptVM_InterpretBytecode` (`0025E4C0`) → `PUSHV`/`POPV`/`PUSHP`/`PUSHDBG` handlers →
`ScriptVariable_Resolve` (`00262440`) → the class base (one of the slot's six pointers, or the
callback `00264E30`) → the value stack push (`00267F90` / `00267F60`) or the store (`0026D530`).

## 6. Modding notes

- A `global` variable is a byte range in the save payload; a mod that wants persistent state has
  0xAF5 bytes there that the shipped scripts have already parcelled out (the TSV says which), and the
  region is saved and loaded verbatim.
- `scratch2` survives saves and area changes *within a group*; `scratch1` does not survive an area
  change; `file` and `local` do not survive the script image. Choosing the keyword chooses the
  lifetime.
- Array indices are clamped, not checked: an out-of-range read returns the edge element silently ~~.~~ when the dimension is 1 or more; a dimension of 0 reads one element before the array *(corrected 2026-10-02, OPUS: `0026250A`–`00262518` clamp with a signed `cmovl`, §2)*.

## 7. What is not known

- [x] ~~The actor's authored entry at `record + 0x40` beyond its `+0x1C` — what else it holds and who
      builds it.~~ **ANSWERED 2026-09-11:** the image's `tableOff18` entry, `0x30` bytes, planted by
      `ActorStorage_InitializeRecord` — [the binding page](how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md)
      §2.1; its unread bytes are FZ-25. **FZ-23.**
- [x] ~~The save payload's `+0x200`–`+0xCF4` cross-referenced to the scripts that own each byte, and to
      the decompiler's flag names.~~ **ANSWERED 2026-09-12:** the region is on
      [the save payload map](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md)
      §2.2 with the ownership tables beside this page; the decompiler's names are a tool-side table
      (`globalMap`), recorded as such; meanings are FZ-27. **FZ-22.**
- [x] ~~The group word at a field entry's `+6` and the persistent flag `+0x1062` bit 5 that together gate
      the `scratch2` clear — what a "group" is in authored terms.~~ **ANSWERED 2026-09-12:** the
      map-reference row's persistence group id (§2.5); bit 5 gates only the flag clear. Which fields
      share a group is authored in the map-reference file, not decoded. **FZ-24.**
- [x] ~~**UQ-48.** Class 3's in-image area (`tableOff40`): no shipped script uses it; whether a tool ever emitted it.~~
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5), to the edge of the evidence.** Static.
      - **The engine supports class 3.** Both resolver paths compute its base as `img + dword[img + 0x40]`, with
        `img = [slot]` (`002625D9`–`002625DF` and `00262633`–`00262636`, re-read today). The shared tail then adds the
        24-bit offset and tests the float bit (`00262639`–`00262644`), exactly as for the other classes.
      - **No shipped script declares a class-3 variable.** The census in §9 finds 0 of 43,466 descriptors, and OPUS
        re-derived that total independently on 2026-09-13.
      - The area itself is not dead: it is the msp region, which `0x03xxxxxx` packed references address and where the
        trap table lives (§2).
      - Whether an authoring tool ever emitted a class-3 declaration is outside what the shipped data can show. The
        shipped scripts are the only corpus, and they carry none. For reconstruction, the rule is a working resolver
        path with no shipped user; keep it, and do not treat its absence from the data as absence from the engine.
- [x] ~~`POPV`'s notification path (`0032F240`, gated on the slot's `+0x28` being 1–3) — unread.~~
      **READ 2026-09-13 (OPUS): it is a two-table lookup returning a notification id, or `-1` when
      the slot has none.** All 32 bytes:

      ```asm
      0032F240  movsxd rax, ecx                                  ; the slot's +0x28
      0032F243  lea    rcx, [00120000]                           ; the image base
      0032F24A  cmp    byte [rax + rcx + 0x21A6D18], 0           ; enable byte at 022C6D18 + i
      0032F252  je     0032F25C
      0032F254  mov    eax, dword [rcx + rax*4 + 0x21A6D28]      ; id dword at 022C6D28 + i*4
      0032F25B  ret
      0032F25C  or     eax, -1                                   ; not registered
      0032F25F  ret
      ```

      So there are **two parallel tables** — a one-byte *registered* flag at **`022C6D18`** and a
      four-byte *id* at **`022C6D28`** — both indexed by the same `+0x28`, and the function is a
      guarded read of the second through the first.
      **The tables hold five entries, not three.** `0032F850` bounds the index with
      `cmp rbx, 5 / jae` before writing, and it is the **register/unregister pair**: it stores `1` at
      `0032F8B6` and `0` at `0032F88D` into the enable byte. `0032ED80` (1,001 B) and `0032F430`
      (654 B) also write it, from a register (`bpl`). **`POPV`'s 1–3 gate is the caller's, not the
      table's** — the table is indexed `0..4` and this bullet's parenthesis describes where `POPV`
      looks rather than how far the array reaches.
      **AND NOTHING IS REGISTERED IN THE SHIPPED IMAGE.** `022C6D18` and `022C6D28` both lie past
      `.data`'s raw size (`01F7E400`), so the loader zeroes them: until one of the three writers runs,
      **every slot's enable byte is `0` and `0032F240` returns `-1` for all five.** The notification
      is a runtime registration, not authored data — which is why no table contents can be read out
      of the file.
      *Qualified 2026-09-28 (FABLE, Claude Opus 5.5, on ASTRA's POPV-lookup return;
      [`script-store-saturation`](../../_index/candidates/script-store-saturation/README.md)):* **`POPV` discards the id.**
      After the call it goes straight to the store, and `0026D530` overwrites `eax` at `0026D53B` before anything reads it.
      So on `POPV`'s path the lookup has no effect and nothing is notified. Other callers do use the id: the voice verbs
      read a manager's slot id from it.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The descriptor layout and the six homes | `00262440` read in full; the jump tables at `002626A8` / `00262690` decoded from the image | 1 | PROVEN |
| Where each base pointer comes from | `0026C8C0` at the cited sites; `0026CE60` at `0026D2E7`–`0026D2F6`; `00264E30` (13 bytes) | 1 | PROVEN |
| `scratch1` is cleared on every field transition, `scratch2` on a persistence-group change or transition option bit 3; only `02099FF0` is exported | `0026DB30` read whole; `00264F90` / `00264F10`; every `.text` reference to `02099DF0`, `02099FF0` and `02099D88` listed (`ripscan`); `0025D8E0` / `00269A20` reference `02099FF0` only | 1 | PROVEN (static) |
| The corpus numbers | 1,114 descriptor tables decoded; the two TSVs beside this page | 1 | PROVEN |
| The keyword ↔ class identity | class-4 and class-5 totals equal the decompiler's `scratch1` / `scratch2` declaration counts (2,292 / 2,343); `enVarScope` in `CScriptContainer.h` | 1 | PROVEN |
| What a `global` at a given offset means | **not established** | — | UNKNOWN |

## 9. Related

- [The interpreter](worldactor-scriptvm-interpreter.md) — §13 the register file, §14 the context is the manager slot
- [The actor manager slot](../../04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md) — the six pointers
- [The section_000 sheet](../../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md) — the header offsets the binder rebases
- [The save payload map](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md) — the persistent payload and the group bank

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

**The census reproduces exactly — every number of it.** Re-derived from the two TSVs beside this
page without reference to the prose:

| | |
|---|---|
| the six class totals and their script counts (12 figures) | **12 / 12 exact** |
| the classes sum to the descriptor total | **43,466 = 43,466**, no unclassified remainder |
| class 3 | **genuinely 0** — no shipped script declares one |
| `global` distinct offsets / above `+0x200` / range / declarations | **587 · 586 · `0x0` and `0x200`–`0xCF4` · 9,448** |
| the six width totals | **4,478 / 1,508 / 139 / 648 / 1,002 / 1,673**, summing to 9,448 |
| "no offset is declared at two different widths" | **0 rows list more than one width** |
| "one offset is declared by 575 scripts, and 110 by a single script" | **575 and 110** |

The machine side is just as exact: descriptor at `[table + index*8 + 4]` (`0026247C`), class
`>> 24 & 7` (`00262484`/`0026248A`), offset 24 bits (`002624A7`), float **bit 27** (`00262644
bt r12d, 0x1b`), the array header's element descriptor at `+0`, dimension count `u16` at `+4`,
dimensions from `+8` (`002624B3`–`002624C6`), the clamp by `cmovns`/`cmovl` across
`002624D2`–`00262537`, and all six width cases exactly as §2.2 tabulates them — `movzx`/`movsx`
byte, `movzx`/`movsx` word, `mov` dword, `movss`. **Both jump-table addresses check out**: the
`jne` at `00262499` sends a non-array class to `002625E7`, whose `lea` resolves the table to
**`002626A8`** (scalar), and the post-walk path at `0026255B` resolves to **`00262690`**
(array element) — the assignment §2.3 gives.

Three things were wrong, all in the same place: **the parts that say what to *build*.**

### ⚠ `PUSHP` forces the width nibble, not the class

§2.1 said the reference descriptor has "the class forced to 7 (`or r8d, 0x70000000`)". The class
field is bits 24–26 — `0x07000000` — by §2.2's own table. `0x70000000` is bits 28–30: the
**width**. And the code does not force the class, it **keeps** it:

```asm
00268158  and  r8d, 0xffffff        ; the 24-bit offset
0026815f  and  r9d, 0x7000000       ; the element's CLASS, preserved
00268166  add  r8d, edx             ; + the width-scaled index
00268169  or   r8d, r9d             ; class put back
0026816c  or   r8d, 0x70000000      ; WIDTH := 7
```

**Width 7 is outside the `0..5` every loader accepts** — `PUSHV` and `PUSHP` both open
`cmp …, 5` / `ja` — so a width-7 descriptor cannot be loaded as a value, which is exactly what
makes it a reference marker. The class has to survive because the reference still has to know which
of the six homes it points into.

> A reimplementation following the old sentence would write `0x07000000`, and the engine would read
> the result as **class 7 — an array** — with the original width intact. Both sevens exist on this
> page and they are different fields.

### ⚠ §4's formula stops one step short for every array element

It gave `address = base + (descriptor & 0xFFFFFF)` with "class 7: after the index walk" as a
parenthetical. The resolver returns the element **base** and the flattened **index** as two separate
fields, and the *handler* combines them:

```asm
; PUSHV, by width
00268004  movzx ecx, byte  ptr [rcx + rax]        ; u8  - x1
00268026  movzx ecx, word  ptr [rax + rcx*2]      ; u16 - x2
00268048  mov   ecx, dword ptr [rax + rcx*4]      ; s32 - x4
; PUSHP does the same scaling explicitly
00268142  add   edx, edx                          ; x2
00268146  lea   edx, [rdx*4]                      ; x4
```

For a scalar the flattened index is `0`, so nothing shows; **for an array element of any width above
a byte the formula is short by `flatIndex × width`.** Corrected in §4.

### ⚠ The push tag is bit 27, and it is never checked against the width

`PUSHV` reads the width nibble from the out-record's `+0x18` to choose the *load*, and reads the
kind word at `+4` — which the resolver sets from **bit 27 alone** — to choose the *tag*:

```asm
00262644  bt    r12d, 0x1b / jae         ; bit 27 -> kind 2, else kind 1
00268062  movsx ecx, word ptr [rbp-0x2c] ; the kind, NOT the width
```

So width and float-ness are **independent fields**, and nothing reconciles them. A descriptor with
width `4` (`s32`) and bit 27 set loads an integer and pushes it **tagged float**; width `5` with bit
27 clear loads a float and pushes it **tagged int**. In both cases the 4 bytes are copied
unreinterpreted. No shipped descriptor is claimed to do this — the point is that **the encoding
permits it and the engine does not object**, so a validator that derives one field from the other
would be inventing a rule.

### The resolver inlines the value-stack pop — and confirms the stack contract from a third site

Array indices are not popped by calling `00267E10`; the resolver open-codes it, and the open-coding
matches instruction for instruction:

```asm
002624D2  mov   eax, dword ptr [r14]              ; depth
002624DA  jle   0x26250a                          ; empty -> index 0, SILENTLY
002624E4  movzx ecx, byte ptr [rdx + r14 + 4]     ; the tag array at +4
002624ED  je    0x26257d                          ; tag 1 -> mov  eax, [r14 + rdx*4 + 0x184]
002624F6  je    0x262571                          ; tag 2 -> cvttss2si from the same array
002624FB  call  0x8620c0                          ; anything else reports, code 1
```

That is a **third** independent confirmation of
[the value-stack layout](../Spawn-Verbs/the-script-to-native-calling-convention.md) — tag array at
`+0x04`, payload at `+0x184` stride 4, **tag 1 = int32, tag 2 = float32**, bad tag reports with code
`1`. An empty stack silently yields index 0, matching the silent underflow recorded there. *(2026-09-29, FABLE, Claude Opus
5.5, [`PKG-TECH-SCRIPTVM-VALUE`](../../_index/completion-packages/PKG-TECH-SCRIPTVM-VALUE.md) T4; control `script-vm-arith-consumers` U.)* A bad tag does not stay
on the stack. Every pop stores the decremented count before its tag test (`002624E1` here, `00267E1F` in the int pop
helper), so the entry is consumed and read as int 0 (`00267E3B`). The comparator reads it as float 0.0 (`0025D875`,
from the `xorps xmm6, xmm6` at `0025D767`). The "report" is the retail no-op bailout `008620C0`, so nothing stops.

**`PUSHV` and `PUSHP` also re-check the capacity inline** — `cmp eax, 0x3f` / `jge` before both the
int and the float store (`00268073`, `002680B1`, `00268173`) — so **a script variable pushed at
depth 63 is dropped as silently as any other push.**

### The 0x30-byte out-record, mapped

§2.1 mentions "a 0x30-byte out-record on the caller's stack" and never says what is in it. Both
callers read it by offset, so it is a contract:

| offset | width | what |
|---|---|---|
| `+0x00` | u8 | constant **6** (`00262667`) — see below |
| `+0x04` | u16 | **kind**: `1` int, `2` float, from bit 27 |
| `+0x08` | u16 | the first word of the record `rbp` holds on return |
| `+0x0A` | u16 | the variable index, the opcode's operand (`0026248D`) |
| `+0x0C` | u32 | the **original** descriptor (`00262492`) |
| `+0x10` | u64 | the resolved **base** address (`00262661`) |
| `+0x18` | u32 | the **element** descriptor — what the width nibble is read from (`0026266E`) |
| `+0x1C` | u32 | the flattened element index (`00262672`) |

> **That `+0x00` answers a loose end elsewhere.** The value stack's second byte array at `+0x44` is
> written `6` by both generic pushes; `PUSHV` writes it from **this field**
> (`00268090 movzx eax, byte ptr [rbp - 0x30]` → `[rcx + rbx + 0x44]`). So the `6` is not a magic
> constant in the push helpers — it is this record's `+0x00`, and the array records where a stack
> value came from. **~~What the other values of that byte are is still unknown.~~** *(corrected 2026-10-02, OPUS: `PUSHV`'s value is always 6 — the resolver writes `+0x00 = 6` at `00262667` on its only exit — and the one other value source is `PUSHP`, which stores the descriptor's width nibble 0..5 there (`00268118`–`00268150`, `00268185`); one reader, `00263450`, called from `00353D10`)*

### Two smaller notes

`0016D6A0`'s body is `C2 00 00` — **`ret 0`**, confirmed from the image. `DVAR` calls it with
**three** arguments, `(slot.+0x28, poppedInt, &02099D48)`: a data pointer, not a string and not a
`0x40000`-style integer, so it is a **fourth argument shape** for the folded no-op beyond the three
[`B-2/a`](../../_index/OPEN-QUESTIONS.md) catalogues. The array header's base is `*(slot + 0)`
(`002624B0 add rcx, qword ptr [rdi]`), which §2.2 left as "in the image"; §2.3's class-3 row called
the same pointer `payload`, which collides with the *save* payload two rows above it — renamed `img`.

**Not claimed:** §2.4's ownership cross-reference, §2.5's group logic, the base-pointer installers and
the `POPV` notification path were not re-derived. Nothing was executed or observed live; the corpus
figures are re-derived from the TSVs beside this page, not from the `.ebp` files.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **Party — SERVICE.**
  - The header parser `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) sets `PartyControl_SetMovementSuppressionBit`
    and reads `PartyFocus_GetCurrentPackedActorHandle`.
  - `ActorSystem_InitializeManagerRuntime` commits a pending party focus handle.
  - `WorldPersistence_ResetBanksForFieldTransition` (`0026DB30`) resets party focus (`PartyFocus_ResetState`).

  **The storage classes a field transition resets include the party focus.**
- **Presentation — SERVICE and CLIENT.** `0026C8C0` sets the character fade parameters (`CharacterRenderConfig_*Fade*`,
  `CharacterRenderSystem_SetFade*`). The slot accessor `0032F240` is read by a 511-byte Presentation body.
- **Movement — SERVICE and CLIENT.**
  - `0026C8C0` sets `Movement_SetRequestedSpeed`.
  - The interpreter `WorldActorScriptVM_InterpretBytecode` is run by `WorldActor_UpdateRuntimeAndScriptExecutionState`.
  - `VMValueStack_PushFloat32Bits` (`00267F60`) is also called by four Movement-filed bodies (88–233 B), which push floats onto the script stack. Which verbs they serve is not read.
- **Resource — SERVICE.** The `atelload.c` loader `0032F430` calls three Resource helpers (80–340 B).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Input — CLIENT.** `FUN_00226be0`, owned by that layer, calls `00358940` on this page. That caller
is the **28-id system-mode request registry**: it keys on `1 << id` against the bit word at
`01FD46D4` (`00226C03`–`00226C08`) and resolves an actor record through `00358940` at two sites in a
1,936-byte body. The crossing is that the registry consults this page's function, **not that this
page owns anything in Input** — `00358940` is `ActorEntity`'s and appears here only in the
opcode-arm census. Its own callees are not named, per the 2026-09-16 refinement of the crossing rule.
Read from the shipping bytes 2026-09-16 (FABLE), closing one of the five pass-22 findings `OPUS`
measured RED at `HEAD`.

**Audio — CLIENT.** `FUN_00261f90`, owned by that layer, calls `002EF2B0` on this page. That caller is a per-object audio state step: it needs `[obj+0x28] == 0` and bit 6 of `byte[obj+0x10]` clear, then sets bit 5 of that same byte and notifies through `0037C910`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — SERVICE.** `00584210` on this page calls `FUN_00316810`, owned by that layer. What it reaches is an achievement-table scan over `01EED078` against the `.rdata` table at `00D10460`, bounded at `0x7FFE`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**RNG_Random_Selection — SERVICE.** `00584210` on this page calls `RNG_MT19937_Seed`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00863D30` - onto the CRT's Mersenne Twister seed; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).
- **SaveLoad — CLIENT (2 edges).** 2 inbound (SaveLoad bodies `00280140` call page-cited `WorldPersistence_ResetBanksAndMarkInitializationState` (00268320), `SaveImage_GetPersistentPayloadBase` (002EF2B0)). Substantive edges include `WorldPersistence_ResetBanksAndMarkInitializationState` (00268320) is called by `00280140`; the remaining edges run through shared helpers the page cites.
- **Save_Load_Settings — CLIENT and SERVICE (9 edges).** 3 inbound (Save_Load_Settings bodies `SaveImage_FinalizeHeaderAndChecksum` (00583D60), `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (00584210), `SaveLoad_ControllerLifecycleHandler` (00582860) call page-cited `MapRef_GetPersistenceGroupId` (00264F90), `WorldPersistence_ImportGroupPersistentBank` (00269A20), `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (00584210)); 6 outbound (page-cited `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (00584210), `WorldPersistence_ResetBanksAndMarkInitializationState` (00268320), `ActorManager_BindLoadedDefinitionPayload` (0026C8C0) call Save_Load_Settings bodies `SaveImage_GetPersistentPayloadBase` (002EF2B0), `SaveImage_GetActiveRuntimeBuffer` (002EF640), `SaveTransitionMetadata_RestoreFromRecord` (002EF410)). Substantive edges include `MapRef_GetPersistenceGroupId` (00264F90) is called by `SaveImage_FinalizeHeaderAndChecksum` (00583D60); `WorldPersistence_ImportGroupPersistentBank` (00269A20) is called by `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (00584210); `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (00584210) is called by `SaveLoad_ControllerLifecycleHandler` (00582860); `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (00584210) calls `SaveTransitionMetadata_RestoreFromRecord` (002EF410); the remaining edges run through shared helpers the page cites.
- **Story_Event_Quest_Hunt — CLIENT and SERVICE (13 edges).** 12 inbound (Story_Event_Quest_Hunt bodies `PersistentFlag_QueryBank64B` (0032AA00), `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0), `PersistentFlag_QueryBank64A` (0032A9A0) call page-cited `SaveImage_GetPersistentPayloadBase` (002EF2B0)); 1 outbound (page-cited `ActorManager_BindLoadedDefinitionPayload` (0026C8C0) call Story_Event_Quest_Hunt bodies `EventMemory_QueryDefinitionIdAbsent` (00377440)). Substantive edges include `ActorManager_BindLoadedDefinitionPayload` (0026C8C0) calls `EventMemory_QueryDefinitionIdAbsent` (00377440); the remaining edges run through shared helpers the page cites.
- **UI — CLIENT and SERVICE (2 edges).** 1 inbound (UI bodies `0029C530` call page-cited `MapRef_GetPersistenceGroupId` (00264F90)); 1 outbound (page-cited `ActorSystem_InitializeManagerRuntime` (0026CE60) call UI bodies `00253A30`). Substantive edges include `MapRef_GetPersistenceGroupId` (00264F90) is called by `0029C530`; `ActorSystem_InitializeManagerRuntime` (0026CE60) calls `00253A30`.
## The `0025E4C0` exclusive subtree — all 5 members bound (SWE2-FRONTIER, followup queue)

`WorldActorScriptVM_InterpretBytecode` (`0025E4C0`, ~7.9 KB of body) is the
interpreter loop this page's §5 call chain names. The body is one long
opcode-arm run: each arm fetches through `008620C0`, pops operands through the
`00267E10`/`00267F90`/`00267F60`/`00267FC0`/`00267E60` stack helpers, works
through the `003DB2A0`–`003DBDC0` conversion family, and reports faults through
`00358940`/`003589E0` with a `lea r8` source-string. The operand stack is the
record this page documents: depth at `[sp + 0]`, per-slot **type byte** at
`+4 + i` and **dword value** at `+0x184 + i×4` — type `1` is `int32`, type `2`
is `float32`.

| member | role | interior |
| --- | --- | --- |
| `0025B400` (108 B) | `WorldActorScriptVM_ServiceRequestWaitState` — the `wait`-family poll: request slot `[+0xA8] + byte[+0x11] × 40`, if `+0x14 == 4` computes `pending − [+0x58]` elapsed and calls `003DC050`; `0xFF` → keep waiting (return 1), else `003DB2A0` and mark `+0x14 = 1` | [`0025B41D`](../../_index/ADDRESS-INDEX.md) |
| `0025D740` (413 B) | the three-way compare engine behind the six relational opcodes (called 6×) — pops both operands; both type-1 → integer `cmp3` (-1/0/1 via `cmovl`), ~~mixed → `cvttss2si`/`cvtdq2ps` promotion~~ any other pair → the int side converted with `cvtdq2ps` (the `cvttss2si` arms at `0025D813`/`0025D827` sit inside the integer path, which is entered only when both tags are 1, so they are not reached from it; corrected 2026-09-28, FABLE, Claude Opus 5.5, [`script-vm-arith-consumers`](../../_index/candidates/script-vm-arith-consumers/README.md) C) → the `ucomiss`/`comiss` float path (`cmova`), where any NaN returns +1; stack underflow → `008620C0(1)` | [`0025D813`](../../_index/ADDRESS-INDEX.md) |
| `00267560` (85 B) | the "both operands int?" predicate the int-ALU arms call — depth < 2 → `008620C0(1)`; returns 1 iff the two top type bytes are both 1 | — |
| `002659F0` (48 B) | the debug/trace marker — `rec = 02098E10 + byte[+0x15] × 0x288`; when `rec+0x10 < 0x80` or `rec+0x11 & 2` is clear it ORs `dx` into the VM flag word `+0x24`, bumps `+0x10`, and sets `rec+0x11` bit 1 | — |
| `00268A80` (129 B) | pop-one-operand adapter — pops TOS into `r8` (type 1 raw, type 2 `cvttss2si`, else `008620C0(1)`), then tail-jumps `00268B10(vm, arg2, popped, r9d)` | [`00268AEB`](../../_index/ADDRESS-INDEX.md) |

Shared callees deliberately outside the census: the operand-stack helpers
`00267E10`/`00267F90`/`00267F60`/`00267FC0`/`00267E60`/`00267DB0`/`00267F60`,
the conversion family `003DB2A0`/`003DB420`/`003DB550`/`003DB6E0`/`003DB640`/
`003DBDC0`/`003DBF60`, `0020E600`/`0020E620`, `008620C0` (fetch/fault),
`00358940`/`003589E0` (error string path), `00262440`, `00268100`, `0025AF60`,
`00268850`, `00268EA0`, `00358940`. The opcode-arm census itself belongs to the
root's own documentation, not to this binding.

## The `00267E60` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00267E60` (~194 B) — variable-class body under a full register save.

| member | role | interior |
| --- | --- | --- |
| `0026D530` | tagged-pointer decode — `qword[+0x10]`, `movsxd +0x1C`, `dword[+0x18] >> 0x1C` vs 5 (`0026D530`/`0026D542`) | [`0026D530`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-22 update (2026-09-18) — `003DB550`/`003DB640` row accessors

`003DB550` (35 B) is the row accessor for the interpreter's `*20`-stride
record table: `edx == 0xFF` or `rcx == 0` -> null; else `movsxd rax, edx`,
`rax*5` then `[rcx+0xA0] + rax*4` — index*20 into the record bank. Interior
anchor `003DB560` (the stride multiply).

`003DB640` (13 B) is the flag test on the same row format: `bt word[rcx+6],
edx; setb al` — the +0x6 flag-word bit read the variable-storage predicates
share. Interior anchor `003DB646`.

## SWE2-EC7-42 update (2026-09-19) - `003DB420`

`003DB420` (304 B) is a script-variable conversion-family member - `003DB2A0` single call. Interior anchor `003DB506` (the `003DB2A0` call).

## SWE2-EC7-92 update (2026-09-20) - `0037DC30` indexed record reset measured

`0037DC30` (132 B) is the two-index table reset `0032ED80` calls:
`ecx >= 5` is rejected, the `02CDB89` table is addressed by
`class*0x3D0 + slot*0xF0`, `00861EC0` clears the 0xF0 record, `+0xEC`
is set to -1, and a non-null `+8` pointer is released through
`003697F0` before `+0`/`+8` are zeroed.
Interior anchor `0037DC6F` (the `00861EC0` clear call).

## SWE2-EC7-94 update (2026-09-20) - `003590E0` measured

`003590E0` (101 B) is the state-block reset `002695A0` and
`0026DB30` run: it zeroes the five `02CDBFxx`/`02CDC0xx` dwords
and the `02CDC01C` byte, clears a four-byte run at `02CDBF03`,
calls `004745B0` on the `02CDBE9B` object, and finally clears the
`02CDC1E1` qword.
Interior anchor `0035912B` (the `004745B0` call).

## SWE2-EC7-98 update (2026-09-20) - `002E15D0` measured

`002E15D0` (28 B) is the state-block reset `0026A5F0` and
`0026DB30` call: `byte[0215F1A0]`, `dword[0215F1A4]`,
`dword[0215F1A8]` and `byte[0215F1A1]` are zeroed in four
stores - the small global block the storage-class layer
clears on reset.
Interior anchor `002E15D2` (the first clear).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-script-variables-and-their-storage-class-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00267560` | 85 B | when the dword at `rcx` is below 2 (signed) calls a 14-byte helper with 1 and returns 0; otherwise compares the bytes at `rcx + 4 + (n - 1)` and `rcx + 4 + (n - 2)`, with n that dword, and returns 1 when they are equal and both are 1, else 0 | `0026756E`, `00267577`, `0026758F`, `0026759D`, `002675AA` |
| `004745B0` | 21 B | stores the dwords 1 at `+0x0`, `0x12` at `+0x4` and 0 at `+0xC` of `rcx`, leaving `+0x8` untouched | `004745B6`, `004745BD` |
