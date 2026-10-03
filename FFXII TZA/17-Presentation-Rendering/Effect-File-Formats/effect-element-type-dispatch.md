---
system: Effect element type dispatch — the switch tables behind an effect's per-frame work
category: 17-Presentation-Rendering
status: DOCUMENTED — the last open box, what 002F2530 does beyond its entry (UQ-206: the shared motion integrator), answered 2026-09-17; §2.8 census re-walked and the step's role corrected 2026-09-29 (FABLE, GI-8 / GI-9)
owner_layer: CodeDomain:Presentation (effects) — no PrimaryOwner tag on most members
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 205 addresses cited - 8 data, 96 entry, 85 interior, 16 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_kind: reproduction
  last_pass_by: OPUS
  last_pass_state: opus-effect-dispatch-pass-1 - both dispatchers decoded from the shipped image and both counts reproduce EXACTLY, not approximately. 002F3BC0: the bound is `cmp eax,0xD1` / `ja 002F3E37`, so 210 types, and the two-level table resolves to 48 slots of which slot 47 is the default arm - **47 types with their own case and 163 to the default**, precisely as written, with the first five arms calling 002F2D60 / 00442520 / 00448DE0 / 004427A0 / 00445310 in the page's own order. 0043EBF0: `add eax,-0x42` / `cmp eax,0x69` admits types 0x42-0xAB as written, its table has 19 slots of which slot 18 is the reject arm, and **18 types have a handler**, precisely as written. THREE FACTS STRONGER THAN THE PAGE CLAIMS, all verified here: the 47 case targets are 47 DISTINCT addresses and the 18 are 18 distinct addresses, so no two types share a handler in either table; the two sets are DISJOINT - zero types appear in both - so "47 + 18" really is 65 distinct types and every one of the 18 reaches 0043EBF0 through the default arm, which the page implies but does not state; and the sub-range bounds are not arbitrary, being exactly the minimum and maximum of its own handled set (0x42 is handled and alone at the bottom; 0xAB is handled and the top). The 18 otherwise cluster in contiguous runs - 0x68-0x6B, 0x70-0x74, 0xA3-0xAB less 0xA5. ONE COMPLETENESS NOTE, NOT A DEFECT: section 2.1 names the byte map at 002F3F48 but not the dword target table at 002F3E88 that the second level indexes; likewise 0043ECC4 / 0043EC78 for the sub-range. The page calls the structure "two-level", so nothing it says is wrong. NOT CHECKED: the update-routine table and its shared base routine, the callers, the frame counter at +0x3C, and every open item the page lists as unread. # <- corrected 2026-10-02, OPUS - the 47 step case blocks call only 41 distinct functions (0044CC10, 00455390 and 00457E10 are shared), so types do share step handlers
  crossref_clean: false
  reopened_count: 0
---

# Effect element type dispatch

> **Effect elements have no vtables.** Each object's **first byte is its type, 0–`0xD1`**, and every per-type
> behaviour is a `switch` on that byte: one table for the ~~per-frame~~ step *(the element's birth - corrected 2026-09-29, §2.1)* and one for the update routines. The update
> routines all start from one base routine. This page records the tables' shape. It is the class-like structure in
> which the `0x440000`–`0x45FFFF` and `0x520000`–`0x52FFFF` bodies are the "methods".

~~**PARTIAL.**~~ **DOCUMENTED.** *(corrected 2026-10-02, OPUS: the page's front matter says `status: DOCUMENTED`)* Read:
- the two full-range dispatchers and the sub-range fallback;
- their callers;
- the ~~frame counter~~ birth step *(corrected 2026-10-02, OPUS: §2.1's correction - `002F3BC0` runs once per element, at birth)*.

Not read:
- ~~what any individual element type is;~~ *(answered: see UQ-204, answered 2026-09-27 - a table of what each of the 65 types puts on screen; 2026-10-02, OPUS)*
- the element object's layout beyond the fields cited;
- ~~the link from the EFX chunk runs to element creation.~~ *(answered: see §2.8 - the chain is closed end to end; 2026-10-02, OPUS)*

*"Effect" is a working name.* It comes from `002F2530`'s label *effect frame advance* on the
[game-settings page](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md) and from
the sub-resource path below. ~~The type values have not yet been matched to authored effect data.~~ *(answered: see §2.8 - the dispatch key is the authored byte; 2026-10-02, OPUS)*

## 1. What the player sees

Spell and ability effects animating frame by frame. Each piece of an effect carries a type byte with 210 possible values. The code gives 47 of them their own frame
step and 18 more a fallback handler, and the type decides what the piece does each frame.

## 2. Native mechanism

### 2.1 The ~~per-frame~~ birth step (corrected 2026-10-02, OPUS: it runs once per element) — `002F3BC0`

> **Corrected 2026-09-29 (FABLE, GI-9 / GI-11): the step runs once, at the element's birth, not every frame.** Every
> arm first calls `002F2D60`, which zeroes the age `+0x3C` / `+0x40` and the update count `+0x48` (`002F30DA`, `002F30DE`,
> `002F3128`), and the dispatcher's one driver `00441B30` runs it on an element it has just taken off the owner's free
> list `+0x120` (`00441BEC`–`00441C0D`, call `00441E71`). The per-frame work is the update (§2.2) and the walk (§2.4).
> Check K1 / K13 of [`gi_effects_checks.py`](../../_index/candidates/gi-0929-effects/gi_effects_checks.py).

`002F3BC0(element)`:
1. Loads the type byte (`002F3BCA`) and bounds it at `0xD1` (`002F3BD0`).
2. Branches through a two-level table: a byte map at `002F3F48` (jump-table data inside `.text`,
   `002F3BDB`–`002F3BE2`), then one call per case: `002F2D60`, `00442520`, `00448DE0`, `004427A0`, `00445310`, … 
   (`002F3BFB`–`002F3C63`).
3. **47 types have a case.** Every other type goes to the default arm at `002F3E37`, which calls the
   **sub-range dispatcher `0043EBF0`** (`002F3E3A`).
4. Then, unless `00314960()` is 0 or `001EDDA0()` is non-zero, adds **1.0 to the element's float `+0x3C`**
   (`002F3E41`–`002F3E60`), the element's frame counter.
5. Stores `00250000()` into word `+0x224` and clears word `+0x226` (`002F3E65`–`002F3E73`).

`0043EBF0` accepts types `0x42`–`0xAB` only (`add eax, -0x42` / `cmp eax, 0x69`, `0043EBF3`–`0043EBF6`).
**18 of them have a handler.** Examples are `005222D0`, `00522AB0`, `0052A130` and `0052ADF0`; the last two are the
effect constructors that pop the arena selection only on allocation failure
([memory page](../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md)).
The rest return 0 (`0043EC75`).

### 2.2 The update routines — `002F3910`

`002F3910(element)` has the same byte bound and a two-level table: byte map `002F3AEC`, offsets `002F3A2C`, both
jump-table data inside `.text` (`002F3910`–`002F3939`).
**47 types reach 38 distinct routines** (some types share one). Every other type goes to the default `0043EAB0`.
**Type 0's arm is `002F2530` itself** (`002F393C`), **and the other 37 routines all call it.** A typical member (`003D9000`) is:

```
r = 002F2530(element, …)          the shared base
if (r != 0) specific(element)     the type's own work
return r
```

The same 56-byte form occurs **51 times image-wide**, each with its own `specific` call. That is more than this table's
38 routines, so some members are reached another way (not traced).

### 2.3 Who drives them

| dispatcher | callers (raw E8/E9 index) |
|---|---|
| `002F3BC0` (~~frame~~ birth step *(corrected 2026-10-02, OPUS: §2.1)*) | `00441B30` only (`00441E71`) |
| `002F3910` (update) | `0043EF40` (`0043EFBA`), `00442310` (`00442354`) |
| `00441B30` (element loop) | `003A8AE0` (`003A8C19`), `0043EF40` (`0043F1DB`) |
| `003A8AE0` | `003A8950`, `003A8DD0`, `0046EFD0` (`0046F218`), `00538820` (`005388D6`) |
| `0043EF40` | `003A8390`, `0043F450` |

`0046EFD0` and `00538820` belong to the **sub-resource instance walker**. On the
[ownerless-functions page](../../00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md)
§12, a render object's resource sub-objects of kind 2 go to the action-timeline interpreter, and kinds ≤ 1 and 3 to
`00538820`. So effect elements are driven from that same sub-resource mechanism, through `003A8AE0`.

### 2.4 The per-frame walk — instance list → instance → element chains → `002F4020`

*Added 2026-09-13 (FABLE), after the exclusive-subtree census showed `003A72F0` owning 139 frontier functions.*

**The instance list.** `003A8D80` (reached through the thunk `003A72F0`, called from `0024D370` at `0024D499`) does
the following:
1. Loads `[02EBEF88]`, then its `+8` (`003A8D84`–`003A8D8B`).
2. For each node, loads the next pointer from `+8` (`003A8DA0`) and stores the node into `02EBEF80`, the "current
   instance" (`003A8DA4`).
3. Calls `00441970(node)` (`003A8DAB`).

The ten functions `0024B270`–`0024F4D0` (at `0024B385`, `0024B65D`, … `0024F59C`) write `02EBEF88` (an eleventh writer outside the range, `003B8260` at `003B860D`, was added 2026-09-14 per AUDITSEM-CONTRA-FABLE-EFX-REGISTRY); they are the list's
maintenance and are not read here.

**One instance, `00441970`.** It returns at once unless `+0x118` is non-null (`00441976`). Then:
1. **If byte `+0x36A` bit 0 of the action context `[02F97348]` is clear** (`0044198E`): it switches on the definition
   byte `[[+0x108] + 0x44]` over `0x40`–`0xD0` (`00441998`–`004419CE`; byte map `00441A98` and offsets `00441A90`, jump-table data
   inside `.text`).
2. **Otherwise** it sets the render byte `02AEE910` from the definition's `+0x4A` / `+0x4C` or from `020926F8`
   (`004419D0`–`00441A0E`).
3. **It then walks ~~one of two element chains~~** the instance's one doubly-linked element list, forward from head `+0x118` or backward from tail `+0x128`, but only on the step-2 path or for the six kinds `0x40`, `0x41`, `0xA1`, `0xA2`, `0xA5`, `0xD0`; every other kind returns without walking *(corrected 2026-10-02, OPUS: `00441970`+0x3C..+0x5E switch, other kinds to the tail at +0x119; `002F31C0`+0x90..+0xC4 unlinks through `+0x28` prev / `+0x30` next with head `+0x118` and tail `+0x128`; section 2.8)* (`00441A15`–`00441A82`), calling `002F4020(element, instance)` on each:
   - the chain at `+0x118`, linked through element `+0x30`, when `[[+0x100] + 0x2C4] & 3` is clear;
   - otherwise the chain at `+0x128`, linked through element `+0x28`.

**One element, `002F4020` — the third type dispatcher.** The census in §8 missed it because its bound is a global,
not an immediate.
1. **Type bound.** It returns unless the element's type byte lies between `[022BE7D8]` and `[01EEBAE0]` (= `0xD1`)
   (`002F402A`–`002F4045`).
2. **Stamp check.** It returns unless the element's `+0x224` stamp is 0 or `001EDDA0()` is non-zero (`002F404B`–`002F405B`).
3. **Rate gate.** When the definition byte `[+0x20] + 0x4D` is non-zero, it advances the word `+2`, compares it with
   `0x4D ×` a multiplier from `001EDDA0()`, and keeps a skip bit in byte `+1` bit 0 (`002F4070`–`002F40E6`). So an
   element can run at a fraction of the frame rate.
4. **The switch.** It calls `003A3D10(definition + 0x75)` (`002F40F4`), then switches on `type − 1` for types 1–`0xD1`
   (byte map `002F443C` and offsets `002F4380`, both jump-table data inside `.text`; `002F40F9`–`002F4124`).
   **46 distinct arm calls**: 45 per-type routines in `00442550`–`00465680`, all frontier, and one arm folded onto the
   empty `0016D6A0` (`002F4357`). Unhandled types call `0043ED30` (`002F4364`).
5. It calls `003A3D10` again (`002F436B`).

**Three type dispatchers, three roles, one type space.** For an element, `002F4020` is the per-frame work under the
instance walk. `002F3BC0` (§2.1, from `00441B30`) and `002F3910` (§2.2, from `0043EF40` / `00442310`) serve other paths.
Which of those paths is update, draw or creation ~~is **not read**~~ *(answered: see §2.1 and §2.5 - the step is birth, `005004C0` creation, the update and the walk the per-frame work; 2026-10-02, OPUS)*. *(Narrowed 2026-09-13, §2.5: creation is a fourth dispatcher, `005004C0`, on byte `+0x44`.)* The 45 routines of `002F4020` are the core of the
139 functions that `003A72F0` exclusively owns.

### 2.5 The type × method matrix — 2026-09-13 (FABLE)

**Every element type is a small class whose methods are selected by switch.** A fourth 210-case dispatcher,
`005004C0`, switches on the byte at `+0x44` (`0050050B`–`0050052F`), with a sub-range partner `00538910` for
`0x42`–`0xAB` (`00538910`–`00538939`). `003A9A70` writes that byte and then calls it (`003A9A8F`, `003A9AAD`). Its other
callers are `003A99F0` (after a `memcpy`) and `003A9BA0`, reached from the EFX data parse `003EDAD0` / `003ED8A0` and
from ~~instance creation~~ the context rebase arms of the per-frame effect pass `0024D540` (`0024D540`+0x114) and of `0024D970` (`0024D970`+0x26), which pass the relocation delta *(corrected 2026-10-02, OPUS: `003A9BA0` adds the delta to each element pointer and calls `005004C0`; `0024D540`+0x16 drains the draw list)*. **So it is the setup method**, run when an element is built. The step,
update and walk methods of §2.1–§2.4 run later.

Decoding the jump tables (the step, update, walk and setup dispatchers; a seventh method, `002F31C0` - **the element's release**: type teardown, unlink from the owner's active list, push onto its free list; read whole 2026-09-19, [an effect element, frame by frame](an-effect-element-frame-by-frame.md) section 3 - over types
`0x40`–`0xD1`, called from `002F2530`, `003A8DD0`, `003A92D0` and `00442600`; and the five `0x42`-based sub-range tables,
three of which — `0043EAB0`, `0043ED30`, `0043E9C0` — were found by the switch-family census and added the same day) and following each non-default arm to the function it jumps to or calls
([`members/effect_type_methods.py`](members/effect_type_methods.py) → [`members/effect-type-methods.tsv`](members/effect-type-methods.tsv)):

| method (dispatcher) | type byte | handlers | frontier |
|---|---|---:|---:|
| step 002F3BC0 | element `+0` | 41 | 41 |
| update 002F3910 | element `+0` | 38 | 37 |
| walk 002F4020 (type - 1) | element `+0` (switch on `type − 1`) | 46 | 45 |
| setup 005004C0 (+0x44) | definition `+0x44` | 38 | 38 |
| sub-step 0043EBF0 | `+0` − `0x42` | 18 | 16 |
| sub-setup 00538910 (+0x44) | `+0x44` − `0x42` | 18 | 18 |
| sub-update 0043EAB0 | `+0` − `0x42` (update's default) | 18 | 18 |
| sub-walk 0043ED30 | `+0` − `0x42` (walk's default) | 18 | 18 |
| seventh 002F31C0 | element `+0` − `0x40` | 6 | 6 |
| sub-seventh 0043E9C0 | `+0` − `0x42` | 9 | 9 |

**248 distinct handler functions, 244 of them on the frontier**, for 65 types with at least one dedicated arm. The only function on more than one method is the empty `ret 0` stub `0016D6A0`, which three arms (walk and two sub-range tables) use as a no-op. ~~Within the step, update and walk methods each type has its own function.~~ The step and update methods share too: 47 step cases call 41 functions (`0x80`/`0x82`/`0x83` share `0044CC10`, `0x8C`/`0x94`/`0x95`/`0x97` `00455390`, `0x8F`/`0x90` `00457E10`) and 47 update cases reach 38 *(corrected 2026-10-02, OPUS: decoded from the case blocks of `002F3BC0` and `002F3910`)*. ~~The setup method alone~~ The setup method also
shares handlers between types (7 of its 38 serve more than one type, e.g. `00538EB0` for types 6 and 7). A type's
step, update and walk handlers are consecutive functions; that is noted here as a reading aid and is not the evidence,
which is the tables. Types 1–5, for instance:

| type | step | update | walk | setup |
|---|---|---|---|---|
| `0x01` | `00442520` | `004424E0` | `00442550` | `00538A60` |
| `0x02` | `00448DE0` | `00448D70` | `004490D0` | `00538AB0` |
| `0x03` | `004427A0` | `00442760` | `004427D0` | `00538B80` |
| `0x04` | `00445310` | `004452D0` | `004453D0` | `00538C80` |
| `0x05` | `00449970` | `00449930` | `00449AB0` | `00538DB0` |

**What this gives the frontier:** a role coordinate (type, method) for each of the 244 frontier handlers, so they can be
read one type at a time. ~~What each type draws is not read~~ — **type `0x05`'s walk is read below** — and neither is
the default path of each dispatcher (`002F3E37`, `002F3A27`, ~~`002F435E`~~, `005006A9` → `00538910`); **`002F435E`
is read below too.**

### `002F435E` is not a stub — it is a second, letter-keyed dispatch (FABLE, Claude Opus 5, 2026-09-20)

The default arm of `002F4020` calls **`0043ED30`**, the 133-byte jump-table leaf this page already lists at the
bottom as "a call-free jump-table leaf". It is a **second dispatch on the same byte**:

```asm
0043ED30  movzx eax, byte ptr [rcx]   ; the element's type byte
0043ED33  add   eax, -0x42            ; 0x42 = 'B'
0043ED36  cmp   eax, 0x69 / ja        ; so 0x42 .. 0xAB
0043ED44  movzx eax, byte ptr [... 0x31EE04 + eax]   ; byte table, 0x6A wide
0043ED4D  mov   edx, dword ptr [... 0x31EDB8 + eax*4] ; 19 jump slots
0043ED58  jmp   rdx
```

Decoded, the byte table routes **eighteen** codes and sends everything else to one shared default:

| type code | arm | | type code | arm |
|---|---|---|---|---|
| `'B'` `0x42` | `0043EDAF` | | `0xA3` | **`00524A50`** |
| `'h'` `0x68` | **`00522D80`** | | `0xA4` | **`00522300`** |
| `'i'` `0x69` | **`00523D30`** | | `0xA6` | **`00524E30`** |
| `'j'` `0x6A` | **`00526080`** | | `0xA7` | **`00526A10`** |
| `'k'` `0x6B` | `0043ED91` | | `0xA8` | **`005271D0`** |
| `'p'` `0x70` | `0043ED82` → `0016D6A0` | | `0xA9` | `0043ED87` |
| `'q'` `0x71` | `0043ED96` | | `0xAA` | `0043ED8C` |
| `'r'` `0x72` | `0043ED9B` | | `0xAB` | `0043EDA0` |
| `'s'` `0x73` | `0043EDA5` | | | |
| `'t'` `0x74` | `0043EDAA` | | | |

**So an effect element's type is a character code, not a small enum** — and the outer dispatcher agrees: `002F4020`
opens by bounding the same byte between a **runtime** low at `[022BE7D8]` and a fixed high of `0xD1`
(`002F402A`–`002F4045`), returning outside that band before anything else happens.

**This is the coordinate the five large bodies on this page were missing.** `00522300`, `00522D80`, `00523D30`,
`00524E30` and `005271D0` are all in the 39-body entry-only queue below; each is now addressable as *the handler for
one type code*, which is the role a reader needs before opening a 1,500-byte body.

#### The first arm: type `'h'` sweeps ten sentinel-gated slots — `00522D80`, 1,531 B (partial, FABLE)

*Read for its shape, not whole.* `rdi` is the element and `r14 = qword[element + 0x20]` ~~its owner~~ its definition *(corrected 2026-10-02, OPUS: `002F2D60`+0x3B `mov qword ptr [rcx + 0x20], rax` stores the instance's `+0x108` definition there)*, the same two
fields type `0x05`'s walk uses — **so the arms share an element layout.**

**Two thirds of the body is one pattern, unrolled ten times.** After an opening `002F1F40` and a sentinel test on
`dword[element + 0x1F0]`, it walks **ten slots of the owner at stride `0x50`** — `+0x170`, `+0x1C0`, `+0x210`,
`+0x260`, `+0x2B0`, `+0x300`, `+0x350`, `+0x3A0`, `+0x3F0` — and for each one:

```asm
0042FDB0(owner + 0x170 + n*0x50, dword[element + 0x44])   ; the transform workbench, with the element's expression id   ; <- corrected 2026-10-02, OPUS - owner is the definition and +0x44 the element's current frame, trunc(+0x3C) or its loop remainder (002F2530+0xB4..+0xFA); 0042FDB0+0x15 keeps it as the time argument of 004314E0
cmp dword ptr [rsp + 0x24], 0x80808080 / je               ; skip this slot when it is UNSET
0026EE00(...)                                             ; compose
00462260(...)
```

**`0x80808080` is the unset marker** — four `0x80` bytes, a packed default — and it is tested ten times, once per
slot plus the opening one. So a type-`'h'` element applies **its authored expression to up to ten transform slots**,
skipping whichever the data leaves unset.

**The tail starts a second phase.** It copies **two global 4×4 matrices** (`02AEEC00`–`02AEEC2F` and
`02AEE960`–`02AEE99F`) onto the stack, evaluates the integer authored expression again —
`004314E0(owner + 0x80, dword[element + 0x44])` — and iterates over `owner + 0x59A`. *That phase is not read.*

#### All eight arms are that one shape, repeated a type-specific number of times (FABLE)

*Measured across ~~the whole leaf~~ the eight arms in bold above after reading `'h'`: **12,463 bytes in eight bodies, and one pattern.*** *(corrected 2026-10-02, OPUS: the leaf routes nine more types through its jmp stubs to bodies of their own - `0047BFA0`, `005294F0`, `0052A360`, `0052B080`, `0052D920`, `0052EA90`, `00528150`, `00528B50` and `0052C070`, decoded at `0043ED30`+0x14..+0x28; most of them also call `0042FDB0` and test `0x80808080`)* Every arm
opens with the same sentinel test on the element's `+0x1F0` and then sweeps owner slots at **stride `0x50`**, each
slot handed to `0042FDB0` with the element's ~~expression id~~ current frame *(corrected 2026-10-02, OPUS: `002F2530`+0xB4..+0xFA stores `trunc(+0x3C)`, or its remainder by the definition's loop length, in `+0x44`; `0042FDB0`+0x15 passes it on as the key time)* from `+0x44` and **skipped when `0x80808080` comes back**.

| type code | handler | size | slot sweeps | bytes per sweep |
|---|---|---:|---:|---:|
| `'j'` `0x6A` | `00526080` | 855 B | **2** | — |
| `0xA3` | `00524A50` | 462 B | **3** | 154 |
| `0xA7` | `00526A10` | 844 B | **4** | 211 |
| `0xA4` | `00522300` | 1,268 B | **6** | 211 |
| `'h'` `0x68` | `00522D80` | 1,531 B | **10** | 153 |
| `'i'` `0x69` | `00523D30` | 1,511 B | **10** | 151 |
| `0xA6` | `00524E30` | 2,966 B | **19** | 156 |
| `0xA8` | `005271D0` | 3,026 B | **19** | 159 |

**Size tracks the count, and the pairs prove it:** the two ten-sweep arms are 1,531 and 1,511 bytes, the two
nineteen-sweep arms 2,966 and 3,026 — within a few per cent of each other, at roughly **150-160 bytes per sweep
block** once the prologue and tail are allowed for. *The arms with the fewest sweeps carry proportionally more
overhead, which is the expected shape when a fixed prologue is divided by a small count.*

**Only the starting slot and the base register are type-specific**, never the stride: `'h'` sweeps from
`r14 + 0x170`, `0xA8` from `r14 + 0xD0`, `'i'` from `rsi + 0x90` — all stepping `0x50`.

So **five of this page's large entry-only bodies and three smaller siblings are one mechanism, not eight**: an
element type says *how many* of the owner's transform slots it touches and *where it starts*, and the data says
which of those slots are set.

#### What the type code selects: a shared finaliser and a type-specific pair (FABLE)

*The matched pairs were the cheap way in, and they answer it.* Inside a pair the call profiles are **identical**
— `'h'` and `'i'` each make ten `0042FDB0`, ten `0026EE00`, ten `00462260` and five `004309C0` calls — and the only
difference is the tail. Six of the eight arms end the same way: **one shared finaliser** and then **two
type-specific routines**, all in the `0054xxxx` band.

| type code | handler | shared | the type's own pair |
|---|---|---|---|
| `'h'` `0x68` | `00522D80` | `00540F40` | `00541DB0`, `00542100` |
| `'i'` `0x69` | `00523D30` | `00540F40` | `00543940`, `005439D0` |
| `0xA3` | `00524A50` | `00540F40` | `00544590`, `00544A50` |
| `0xA6` | `00524E30` | `00540F40` | `00544CE0`, `00544D30` |
| `'j'` `0x6A` | `00526080` | `00540DB0` | `00545EF0`, `005466E0` |
| `0xA8` | `005271D0` | `00540F40` | `00547350`, `005473A0` |
| `0xA4` | `00522300` | — | **none** |
| `0xA7` | `00526A10` | — | **none** |

**The pairs rise monotonically with the handler address** — `0x541DB0` < `0x543940` < `0x544590` < `0x544CE0` <
`0x545EF0` < `0x547350`, in the same order as `00522D80` < `00523D30` < `00524A50` < `00524E30` < `00526080` <
`005271D0`. Handler and terminal were emitted in the same source order, one block per type. *That is independent
evidence that the eight are siblings generated from one family, not eight functions that happen to share a shape.*

So the element's character code selects **which pair of `0054xxxx` routines consumes the transforms**, while the
sweep that prepares them is common.

~~**`0xA4` and `0xA7` emit nothing — read the same day.**~~ *Corrected 2026-09-27 (FABLE, Claude Opus 5.5): both emit
([UQ-204 record](../../_index/candidates/uq204-element-type-emits/README.md), control `uq204_emits.py` E4). `00522300` calls `003A3010` at `005227C5`,
a raw packet that the PC drain never submits. `00526A10` calls `003A34D0` at `00526D2D`, a GiVmax running program
`004ECC50`. What stands below is that neither reaches a `0054xxxx` terminal.* They make the *same kinds* of calls as the other six —
`0026EE00` to compose, `0042FDB0` on the workbench, `00462260`, and the authored-expression evaluators `004309C0`,
`00431830`, `00430B90` and `004314E0` — but reach **no terminal**, and no tail call either: **every `jmp` target in
both bodies lies inside the body**, so each ends at its security-cookie check and returns. ~~*These two element types
run the whole sweep-and-expression machinery and put nothing on the draw list* — they contribute **state, not
draws**, which is the real split in the family and the reason their sizes never fitted the per-sweep ratio.~~ *(Struck
2026-09-27: they do append to the draw list, through the calls named above.)*

*One more asymmetry worth recording:* the nineteen-sweep arms call `0026EE00` **nineteen** times but `0042FDB0` only
**ten**, so their sweep composes more often than it works the bench — the two are not one-to-one there as they are
in the ten-sweep arms.

#### Where it all ends: a global draw list (FABLE)

**The shared finaliser is a front, not the work.** `00540F40` (118 B) computes one argument and tail-calls:

```asm
00540F65  call 0024E460 ; jne ->   ebx = 2
00540F6E  call 003A3D20 ; jne ->   ebx = 2      (either predicate sets bit 1)
00540F80  call 003A2C70 ; or eax, ebx           (the flags word)
00540F96  call 00540DB0                          (a, b, c, d, flags)
```

— and `00540DB0` is **exactly the routine the `'j'` arm calls directly**. So `'j'` is not a different mechanism: it
supplies its own flags instead of letting `00540F40` compute them.

**`00540DB0` (389 B) is an append to a global list.**

```asm
00540DBF  movzx r10d, word ptr [02F8F2C6]   ; the entry counter
00540DC9  mov   rax, qword ptr [02F8F2F8]   ; the list base
00540DD0  and   r9d, 0xFFFFFF               ; the flags, 24 bits
00540DDD  lea   r8, [r10 + r10*4]           ; counter * 5
00540DE1  inc   r10w                        ; ... and the counter advances
00540DE5  lea   rdi, [rax + r8*8]           ; base + counter * 0x28
00540DE9  mov   word ptr [02F8F2C6], r10w
```

So the entry is **40 bytes (`0x28`)**: `qword[+0]` zero, the **24-bit ~~flags~~ sort key** *(corrected 2026-10-02, OPUS: the merge sort compares it, `003A3A50`+0x103 and +0x233; below)* at `+8` with a nibble from
`byte[02AEE910]` shifted into the top byte at `+0xB`, the second argument at `+0xC`, and a zero `qword` at `+0x10`.
The body then recomputes the same three predicates for a **second** entry.

**That closes the cluster end to end.** An effect element's character type code picks a pair of `0054xxxx` routines;
those routines sweep the owner's transform slots at stride `0x50`, skipping the ones the data leaves at
`0x80808080`, applying the element's authored expression; and the finaliser appends 40-byte entries to the draw list
at `[02F8F2F8]`, each carrying a 24-bit ~~flags word~~ sort key *(corrected 2026-10-02, OPUS: `003A3A50`+0x103 `mov eax, dword ptr [rsi + r9 + 8]`; `00540DB0`+0x44 stores it)*.

##### The list has twenty-four appenders and ~~no reader~~ one reader, the drain `003A3740` (FABLE, same day; heading corrected 2026-09-25)

*A census of the counter, run to find the consumer, corrects a reading of the paragraph above.* `00540DB0` is **one
appender of twenty-four**, not the appender. A rip census of `02F8F2C6` finds **48 accesses in 24 functions, and
every one of the 24 both reads and writes it** — most of them in a `0039Dxxx`–`003A0xxx` band running the same
idiom. **No function reads the counter without appending**, so there is no consumer that merely inspects the count.

The base `02F8F2F8` is written **exactly once** — an initialisation. And the header around it,
`02F8F2C0`–`02F8F2FF`, carries **several** such counters, `02F8F2D0` alone taking 18 writes, so this is a
**multi-list header**, not one list.

~~**Where a frame drains or rewinds these lists is not found — but it must exist.**~~ *(Superseded below: the reset is `003A3670`, the rewind `003A3A00`, the drain `003A3740`.)* No rip-relative store ever writes
the counter an immediate, and no store anywhere in `02F8F2B0`–`02F8F2C7` covers its two bytes (the nearest are a
`dword` at `+0xC0` and a `byte` at `+0xC5`). *And none of the appenders bounds it.* Three read independently —
`00540DB0`, `0039D6C0`, `0039D970` — and each one loads `word[02F8F2C6]`, forms `base + counter * 0x28` and writes,
with **no compare against a capacity**:

```asm
0039D6D3  movzx eax, word ptr [02F8F2C6]
0039D6DD  mov   rdi, qword ptr [02F8F2F8]
0039D6E4  lea   rbx, [rax + rax*4]          ; counter * 5
0039D6E8  mov   qword ptr [rdi + rbx*8], 0  ; ... * 8 = counter * 0x28
```

An unbounded append with no reset would overrun the list inside a single frame. ~~So the rewind exists and is
reached through a computed address.~~

> ### Withdrawn the same day, and the reset is plain (FABLE)
>
> **There is a rip-relative reset and I missed it.** `003A3670` — the same function that writes the list base —
> does `xor eax, eax` and then **`mov word ptr [02F8F2C6], ax`** at `003A36DF`. My scan looked for a store of an
> **immediate**, and the zero arrived in a **register**. *That is the second time in an hour I searched a spelling
> instead of an effect* — the first was classifying appenders by the mnemonic `inc`, which missed `00540DB0`'s
> register increment. Same root cause, and the fix is the same: match on what the instruction **does** to the
> address, not on how it is written.
>
> **What `003A3670` actually is: the allocator.** It takes `0x190000` bytes for this list (`02F8F2F8`) and
> `0xC8028` for a second (`02F8F300`), stores a count at `02F8F2C0`, and zeroes `02F8F2C6` together with several
> neighbours.
>
> **And that gives the capacity.** `0x190000 / 0x28` = **40,960 entries**, while the counter is **16-bit and can
> reach 65,535**, so an unchecked append could overrun the buffer if nothing rewound it. Since `003A3670` allocates,
> it is initialisation rather than a per-frame rewind — and the claim that the rewind must be reached through a
> computed address is **withdrawn**, not qualified.

##### And the per-frame rewind is `003A3A00` (FABLE, same day)

*Found by re-running the census the two misses argued for: classify each of the 24 writes by the **value that
reaches the address**, not by the mnemonic or the operand form. Controls — `003A3670` must come out RESET and
`00540DB0` BUMP — both pass.* The split is **21 BUMP, 2 RESET, 1 unresolved**, and the second RESET is the answer.

**`003A3A00` (74 B) allocates nothing.** It reloads the second list's base from `02F8F308` into the cursor
`02F8F2D0`, computes that region's end into `02F8F2D8`, **zeroes `word[02F8F2C6]`** and `byte[02F8F2C5]`, and clears
bit 0 of `word[02F8F310]`:

```asm
003A3A00  mov  r8, qword ptr [02F8F308]     ; the second list's base
003A3A0E  mov  qword ptr [02F8F2D0], r8     ; ... becomes its cursor
003A3A20  xor  eax, eax
003A3A26  mov  word ptr [02F8F2C6], ax      ; the counter, rewound
003A3A42  mov  qword ptr [02F8F2D8], rcx    ; base + rounded size = the end
```

That is a **begin-frame**, and it has a single caller, `0024D540`. **So the list is rewound every frame after all,
and the 40,960 entries are a per-frame budget rather than a lifetime one.** The question this subsection opened
twice, and answered wrongly once, is closed.

##### The drain, and where the whole list sits in the frame (FABLE, same day)

**`0024D540` is the frame's draw setup.** Its callers are **`MainLoop_Draw`** and
**`MainLoop_UpdateAndRenderFrame`**, and it runs five resets in order:

```asm
0024D54C  call 002D7FC0
0024D551  call 003B3D20
0024D556  call 003A3740      ; the DRAIN
0024D55B  call 003A3A00      ; the REWIND
0024D560  call 0039D200
```

**The third is the drain — and it is the one entry the effect census could not resolve.** `003A3740` reads the
counter at entry, walks the entries (`add rbx, 0x28` / `inc ebp` / `cmp ebp, edx` / `jl`, with `edx` the count it
read), and before writing a counter value back it records a **high-water mark**: `ecx` = cursor `02F8F2D0` minus
base `02F8F308`, compared against `02F8F2F0` and kept by `cmova`.

So the per-frame order is **drain, then rewind**, both inside the main loop's draw setup — which places the whole
mechanism: the element arms append during the frame, `003A3740` submits what was appended, `003A3A00` rewinds for
the next one, and the engine keeps the peak usage.

> *Qualifying my own sentence above.* This subsection earlier said "no function reads the counter without appending,
> so there is no consumer that merely inspects the count". The first clause is literally true and the second reads
> as more than it should: **the consumer exists and is `003A3740`**, which both reads *and* writes the counter and
> was therefore classified with the appenders by a read/write split. A drain looks exactly like an appender to that
> classifier.

**The drain in full** *(completed 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 280)*:
- **Empty list.** A zero counter returns at once (`003A3744`–`003A374E`).
- **Range pass.** Otherwise the drain calls `003A3A50(0, n − 1)` over the entries' index range (`003A3754`–`003A3760`).
- **Per-entry dispatch.** Each entry is handed to the function pointer at its own `+0x10`, with the entry's `+0x00` as the
  argument, when that pointer is non-null (`003A38BA`–`003A38C6`). The draw is therefore dispatched per entry, not by type.
- **Emptying.** The counter is written back from `r15w`, which is zeroed at `003A37B0` and never set again. So the store at
  `003A393F` empties the list; the rewind `003A3A00` then resets the cursors.
- **Statistics.** The drain records the last and peak entry counts at `02F8F2CC` / `02F8F2CE` (`003A3968`, `003A3973`). It
  records the last and peak side-buffer bytes at `02F8F2E8` / `02F8F2F0` (`003A3950`, `003A3957`).
- **Type-store name.** The header `02F8F2C0`… is declared as `EffectDrawListHeader02F8F2C0`.

##### What the type-specific pair actually does — measure, build a VIF packet, wrap it as a `GiVmax` command (FABLE, Claude Opus 5, 2026-09-20)

*This closes three of the things this page left open: what the type's own pair of `0054xxxx` routines does, what
`003A3740` submits each entry to, and what the second list at `02F8F2D0` holds.*

**The small member of every pair is a size measurer, and all six return 16-byte units.** Each ends `shr <reg>, 4`,
six times out of six, and each returns **zero** when nothing is set — which is what makes the arm skip the draw:

| type | measurer | size | what it counts |
|---|---|---:|---|
| `'h'` `0x68` | `00541DB0` | 79 B | `0x230`, plus `0xB0` for the **first** set slot and `0xC0` for each further one, over **3** slots from `owner+0x140` at stride `0x50`; zero when `byte[owner+0x38]` is clear |
| `'i'` `0x69` | `00543940` | 87 B | `(dword[arg2] + 0x78) << 4`, plus `0x190` per set slot, over **4** slots at `+0x740`, `+0x790`, `+0x7E0`, `+0x830` |
| `0xA3` | `00544590` | 68 B | `0x130`, plus `0x10 × ((count − 1) / 20 + 1)` from `dword[owner]` |
| `0xA6` | `00544CE0` | 68 B | `0x40`, plus `0x180` first / `0x190` further, over **4** slots at stride `0x100` |
| `0xA8` | `00547350` | 76 B | `0x40`, plus `0x2D0` first / `0x2E0` further, over **4** slots at stride `0x110` |
| `'j'` `0x6A` | `00545EF0` | 191 B | a nested walk stepping `0x15`, `0x60` per inner item |

**In every one of the first/further pairs the first set slot costs exactly `0x10` less** — `0xB0`/`0xC0`,
`0x180`/`0x190`, `0x2D0`/`0x2E0`. One quadword, emitted once: a shared prologue. *That the same `0x10` gap appears in
three independently sized types is what makes "prologue" a reading rather than a guess.*

**The arm bump-allocates that many 16-byte units from the second list, and silently draws nothing if it will not
fit.** From type `'h'`'s tail:

```asm
0052329D  call 00541DB0                    ; the size, in 16-byte units
005232D2  movsxd rcx, eax  /  shl rcx, 4
005232D9  add   rcx, qword ptr [02F8F2D0]  ; the cursor 003A3A00 rewinds every frame
005232E0  cmp   rcx, qword ptr [02F8F2D8]  ; ... against the end it computes
005232E7  jae   00523364                   ; DOES NOT FIT -> straight to the epilogue
005232FE  call  00542100(cursor, owner, &count, &params)
00523303  cmp   dword ptr [rsp + 0x28], 0  ; the builder's own count
00523308  mov   qword ptr [02F8F2D0], rax  ; ... and it returns the new cursor
0052330F  je    00523364                   ; built nothing -> epilogue
```

**So `02F8F2D0` / `02F8F2D8` is the frame's packet arena** — the region this page already knew was reloaded from
`02F8F308` and rewound by `003A3A00`, without knowing what filled it. **An element that arrives after the arena is
full is dropped without a diagnostic**, which is the failure mode a reimplementation has to keep.

**What the builder writes is a chunk table.** `00542100` (1,588 B, read for its emits and its tail, not whole)
returns the caller's cursor untouched when `byte[owner+0x38]` is clear. Otherwise it copies a `0x200`-byte template
from `02AEB610` and a second from `02AEB820` onto the stack, folds in a block of `xmm` rows from its fourth
argument (`r9 + 0x00` … `r9 + 0x100`),
and writes **16-byte descriptors** at the head of the block:

| field | width | role |
|---|---|---|
| `+0x00` | word | the payload length, in **16-byte units** |
| `+0x03` | byte | the tag, in the **high nibble** — `0x10` = inline, `0x30` = referenced |
| `+0x04` | dword | a **compressed pointer** from `RuntimePointer_EncodeImageAddress` (`0020E620`) |
| `+0x08` | qword | the chunk's own 8-byte VIF prefix |

For type `'h'` it lays down **five** of them — tag bytes written at `+0x13` and `+0x33` (referenced) and `+0x43`
(inline, length 0) at `00542443`, `005424AE` and `00542472` — with the payload from `+0x50`, which is what the
first descriptor's `+4` points at. The tail patches the leading length (`00542712`, `shr r8d, 4` then a `word`
store) and reports a count through its third argument.

**And `00540DB0` turns that table into a `GiVmax` command.** The 118-byte "shared finaliser" `00540F40` only computes
the flags word and forwards its four arguments unchanged; `00540DB0` is where the work is, and its second argument
is the **length of the descriptor table in 16-byte units** — `5` for type `'h'`, which is exactly the five
descriptors above:

```asm
00540E36  call 0020E680                    ; a 16-byte node -> the record's +0x18
00540E47  call 001DB7E0                    ; a 0x640 GiVmax command, stored at node+8
00540E4C  shl  r12d, 4                     ; the table's byte length
   per descriptor, by its tag nibble:
     1  001DB340(cmd, desc + 8, len*0x10 + 8)        ; appended IN PLACE, advance 8 + that
     3  0019C5A0(len*0x10 + 8); copy qword[desc+8]; memcpy the payload behind it;
        001DB340(cmd, copy, len*0x10 + 8)            ; advance 0x10
00540F30  jmp  0020E670                    ; = a thunk to 001FB840
```

`001DB7E0` is `001DB840`'s sibling: it takes the same `0x640` bytes from the same arena and constructs the same
`GiVmax` (`001DB220`, vtable `009007E8`), but appends **no** packets of its own. And `0020E670` is a **thunk to
`001FB840`**, which promotes `node+8` to `node+0` and tail-jumps the command's slot 0 — `001DB550`, the VIF1
interpreter.

**`001DB7E0` has exactly two callers, and they differ only in when the replay is submitted.** `00540C70` (317 B,
one caller, `0051CDE0`) runs the *same* walk over a chunk table — `0020E680` for the node, `001DB7E0`, the two tag
arms, `0020E670` at `00540D92` — and then **tail-jumps `0020E630(node, 2)`** at `00540DA8` instead of appending a
draw-list record. *So the immediate/deferred split the [VIF1 / VU1 layer](../Legacy-PS2-GS/the-vif1-vu1-layer.md)
§2.1c describes for `003A35E0` versus `003A34D0` exists inside this family too*: `00540C70` submits now,
`00540DB0` files the node at `record+0x18` and lets `003A3740` submit it in sort order.

> **So an effect element's draw is a VIF1 packet, and this cluster and the
> [VIF1 / VU1 layer](../Legacy-PS2-GS/the-vif1-vu1-layer.md) are one path.** The element measures its packet, builds
> it into the frame arena, wraps it in a `GiVmax`, **runs it immediately** — the microprogram executes inside the
> element arm — and leaves the *GS replay* to be submitted when `003A3740` drains the entry it appended. That
> answers "what `003A3740` submits each entry to": `0020E630(node, mode)`, and from there the route the
> [Gi family page](../Gi-Render-Commands/gi-render-command-family.md) §12c and §12e read out.

**The record's `+8` is the sort key, not a flags word.** This page called it "the 24-bit flags"; the merge sort
`003A3A50` compares **`dword[record + 8]`** (`003A3B53`, `003A3C83`), and type `'h'` computes what it passes there
from a float — `cvttss2si(value × 1/width)` at `0052334E`–`00523354`. With `byte[02AEE910]`'s nibble OR'd into the
top byte at `+0xB`, the field sorts **by display layer first and by that 24-bit number within a layer**. The real
flags word is the separate `dword[+0x20]` that `00540F40` computes.

**One inconsistency, stated rather than smoothed over.** `dword[descriptor+4]` is written through
`RuntimePointer_EncodeImageAddress` (`ecx − dword[01F83530]`) and read back by `00540DB0` **raw**, as the `memcpy`
source (`00540EB8`, `00540ED2`) — no call to the matching decoder `ImageAddress_ResolveRuntimePointer` (`0020E600`,
`ecx + qword[01F83530]`). **The scheme is certainly live:** `003E6680` decodes `dword[characterRenderRecord + 0x2FC]`
and passes the result, with the count at `+0x300`, to `0051CDE0` — the one caller of the immediate appender
`00540C70` — and `00544590` decodes `dword[owner + 0x64]` and then **discards the result**. *The only reading under
which all three sites are correct is `[01F83530] == 0` at run time.* ~~The image's
static bytes there are `0005FBBA0005FB90`, which cannot be a base — adding it would put the pointer past the address
space — so the global is written at run time by a path a rip-relative sweep cannot see (a register-based struct
init).~~ **Corrected 2026-09-25 (FABLE, Claude Opus 5.5): those "static bytes" were read at a file offset past
`.data`'s raw backing, where the file holds unrelated data. The loader zero-fills that part of `.data`, so the image
initialises `01F83530` to 0.** There is no evidence of a register-based initialiser. *(Scope corrected 2026-09-25, FABLE, Claude Opus 5.5: `01F83530` is **zero at image load**, because it lies past
`.data`'s file-backed extent. That is separate from whether later code can write it, and one in-image store route
can. The texture-id table writer `00210570`, reached through GiSetTexture's execute, bounds its id only from above
with a signed compare, so id `0xFFFB` stores a pointer into `01F83530`. That was replayed on the unmodified bytes.
The id producers read keep ids below `0x4000` at the shipped frame width, so the route is **undriven, not
absent**. "Zero for the process's life" is supported, not proven. See [the row-lookup contract](../../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md) §7, the reconciliation.)*
~~*I have not established its run-time value, and the raw use is the only reason to think it is zero.*~~ *Its
run-time value in play is still not observed live.*

**And the templates are the startup packet objects, so each type's microprograms are named.** `02AEB610` and
`02AEB820` are two of the 77 rows the
[VIF1 / VU1 layer](../Legacy-PS2-GS/the-vif1-vu1-layer.md)'s template census decodes; §2.4b there reads the rest of
this chain and gives the map — type `'h'` installs `004DF440` and `004E0F70`, `'i'` installs `004DCC00` and
`004DDDF0`, `0xA3` installs `004DB350`, `0xA6` and `0xA8` share `004DA8A0`, and `'j'` installs `004D7BF0`. **The
copied template carries the MPG descriptor verbatim**, which is how the program reaches the packet at all: the
builder only re-points the *data* descriptor at what it has just written.

**Not read here:** `002D7FC0`, `003B3D20` and `0039D200`, the other three resets; what `word[02F8F310]` bit 0 means;
the body of `00542100` between its templates and its tail, including what its fourth argument's `xmm` rows
are; the five other types' builders, which are only assumed to follow `'h'` because their measurers do; what any of
the seven microprograms draws.

> *Instrument note.* The first split of these 24 classified appenders by the text `inc` and **missed `00540DB0`
> itself**, which increments in a register and stores back. The read/write column is the discriminator, not the
> mnemonic — a reminder that a classifier built from one example inherits that example's spelling.

**Not read here:** the per-type `0054xxxx` pairs themselves; what `0xA4` and `0xA7` do instead *(read 2026-09-27, the
UQ-204 record)*; the three predicates
`0024E460` *(answered: see its frontier note below; 2026-10-02, OPUS)*, `003A3D20`, `003A2C70`; ~~the drain end of the list~~ *(answered: see "The drain in full" above; 2026-10-02, OPUS)*; which of the two dispatches in `002F4020` runs first
for a given byte, and therefore which codes ever reach this leaf in practice — the leaf covers `0x42`–`0xAB`, the
outer bound is `[022BE7D8]`–`0xD1`, and the overlap is not the whole of either.

### What type `0x05` draws — `00449AB0`, 1,741 B, read whole 2026-09-20 (FABLE, Claude Opus 5)

*One of the 39 bodies over 1,024 bytes that a DOCUMENTED page names at its entry and nowhere else — the
sub-population `check_entry_only_sizes.py` calls a mention "without qualification". This one is no longer.*

**It refuses early, twice.** `byte[element] == 0` returns at once; and with the owner's
`byte[+0x4A] & 0x1C == 0xC` it also needs `dword[element + 0x40]` non-zero. Then `dword[owner + 0x5A0]` must resolve
to a pointer, or it returns.

**It composes a transform into a global scratch.** The scratch is `[01FD4A78] + 0x800`, taken once at entry.
`0039B620(dword[element + 0x290])` runs first; then `002F1F40(element, element + 0x230, stack)` and
`0026EE00(scratch + 0x40, element + 0x240, stack)`; then four `movaps` copy ~~`element + 0x250 … +0x27F`~~ `element + 0x250 … +0x28F` *(corrected 2026-10-02, OPUS: `00449AB0`+0xB4..+0xD7 read `+0x250`, `+0x260`, `+0x270` and `+0x280`)* — a
4×4 matrix — into `scratch + 0x00 … +0x3F`.

**It assembles a render-state byte bit by bit.** `scratch + 0x1F1` is built with the copy-these-bits idiom
(`xor` / `and mask` / `xor`), repeated: bits 0-2 from `byte[owner + 0x4A] >> 2`, then bits 3, 4, 5 and 6 each from
`byte[owner + 0x590]`, one mask at a time (`00449B93`–`00449C10`). *Nothing is copied wholesale* — every bit is
placed individually, which is why the run is long and why a reader skimming it sees noise.

**Its numbers are authored expressions, not constants.** The body calls `004309C0` four times and `00431830` twice
— the float and integer **authored-expression evaluators**
([how an authored number gets its randomness](../../02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md)
names `004309C0` as the float twin of `004314E0`, 89 callers) — and `0042FDB0`, a transform-workbench member. *So a
type-`0x05` element's parameters are resolved per draw and may be randomised, rather than read from the file as
values.*

**Then it emits.** The tail (`0044A11C`–`0044A15B`) is four steps:

```asm
0044A124  call 004314E0          ; the INTEGER expression, on owner+0x30 with element's dword +0x44
0044A134  mov  [02AEE900], eax   ; byte[owner + 0x49] >> 5
0044A13A  mov  [02AEE908], rcx   ; the evaluated integer
0044A148  mov  ecx, dword ptr [r14 + rax*4 + 0x5A0]   ; rax = element's dword +0x294 - the resource INDEX
0044A15B  call 004355D0          ; (resolved resource, scratch)
```

So the element carries an **index into the owner's resource table** at `+0x294`, and the draw is handed to
`004355D0` — the composer [the two transform primitives](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md)
already reads, which composes `02AEEBF0` with the element's matrix. Two values reach it out of band, through the
globals `02AEE900` and `02AEE908`.

**Not read here:** `0039B620`, `002F1F40`, `0026EE00` and `004355D0` beyond their roles; what the `+0x1F1` bits mean
to the emitter; the four resolve-and-branch blocks between the state assembly and the tail.

### The queue this came from — 39 large bodies cited only at their entry (FABLE)

Regenerable with `check_entry_only_sizes.py --db <db> --list`; **86,255 bytes** in total, biggest first. ~~Nine~~ Twelve *(corrected 2026-10-02, OPUS: the table that follows has twelve rows, each naming its page)* are
named by a page in this folder or its neighbours, which is why the lane starts here:

| body | size | the DOCUMENTED page that names its entry |
|---|---:|---|
| `0053F490` | 5,417 B | `Character-Render-Records/the-bone-trails.md` |
| `005271D0` | 3,026 B | this page |
| `00524E30` | 2,966 B | this page |
| `00230C10` | 2,018 B | `PS2-Image-Data-Formats/loader-bound-bin-families` |
| `00449AB0` | 1,741 B | this page — **read above** |
| `00522D80` | 1,531 B | this page |
| `00523D30` | 1,511 B | this page |
| `00366B80` | 1,420 B | `Widget-Object-Model/the-widget-constructor-and-object-sizes.md` |
| `00522300` | 1,268 B | this page |
| `002C2F90` | 1,110 B | `Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md` |
| `005742D0` | 1,097 B | `99-Unresolved-Residual/the-unresolved-158.md` |
| `005599D0` | 1,025 B | `License-Board-View/the-license-board-grid-build-and-its-change-sweep.md` |

*Re-checked 2026-09-20 (FABLE, Claude Opus 5), which the paragraph below asks for: the queue is now **40** bodies
and **25** of them report no citer. Part of that movement is an artefact of this page — `0040B780`, `007E0B60` and
`006515C0` now resolve **to this page** as their citer, because the sentence below **names them** while saying they
have none. Naming an address in prose to record that nothing cites it makes the page cite it, and the instrument
cannot tell the two apart. All three are still unread here, and still the largest entry-only bodies in the database;
only the bucket changed.*

*And the queue measures citation, not explanation.* Its largest row, `0040B780`, **already has a documented role**:
[the per-model oscillator subsystem](../Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md) names it the
**blend apply**, called as `0040B780(record, entry, t)` when `0 < t < 1`, and lists it among the bodies it reads as
translated VU0 assembly. `007E0B60` is likewise named in `18-Audio/sead-function-identification.md` and `006515C0`
in `CONTRACT-render-record-pool-lifecycle.md`. So a row here means *no DOCUMENTED page cites an address inside it*,
which is a property of citations; it is **not** evidence that nothing is understood about the body, and a reader
should check the other pages before opening one.*

The other 27 *(of the first run's 39; the re-check above counts 25 of 40 - scope named 2026-10-02, OPUS)* report **"no DOCUMENTED citer found"** — the largest being `0040B780` (8,458 B), `007E0B60` (6,716 B)
and `006515C0` (4,129 B) — which means the tool counted them entry-only from a citer that is no longer DOCUMENTED.
*Those need the re-check the tool asks for before anyone reads them*, because the queue's own premise may not hold
for them.

### 2.6 The `+0x48` kind fronts — `003A4290` / `003A56F0`

A second, unrelated dispatch family lives in the same effect block. Two large functions
(`003A4290` = 4782 B, `003A56F0` = 4594 B) carry **structurally parallel** three-level switch
families — same selector byte, same 14-kind outer table, same two inner tables nested inside the
kind-6 arm. Full case maps are in [switch-family-3a42-3a56.tsv](members/switch-family-3a42-3a56.tsv).

- **Selector:** signed byte `[object + 0x48] − 1`, bounded to `0xD` (`003A4308`–`003A432B`,
  `003A578C`). This is **not** the element-type byte — the object type is not established.
- **Outer tables:** `003A5540` (14 cases → 12 targets) and `003A68E4` (14 cases → 12 targets).
  **Kinds 9 and 13 share one arm** in both fronts (`003A4338` / `003A5799`); **kinds 3 and 11
  share one arm** in both fronts (`003A4455` / `003A5885`). Every other kind has its own arm —
  kind 12 is `003A54DD` in `003A4290` (calls `00250010`, then copies the scratch triple
  `+0x30`/`+0x34`/`+0x38` back into the object, `003A54DD`–`003A5506`) and the 163 B
  `003A6792` in `003A56F0`; kind 14 is `003A5490` / `003A6835`. There is no default arm in the
  table — a selector outside 1–14 falls out at the bound check.
- **Inner tables (inside each kind-6 arm, ~3.3–3.4 KB):** a 40-case/35-target table
  (`003A46BA` → `003A5578`; `003A5A68` → `003A691C`) and a 10-case/7-target table
  (`003A50E7` → `003A5618`; `003A642D` → `003A69BC`). The kind-6 object carries its own
  subtype field the inner tables key on.
- **Per-kind helpers repeat across both fronts** — `003A3FD0` (kind 1), `003A6BA0` (kind 2),
  `003A40F0` (kind 4), `003590D0` (kind 5), `003A6FC0` (kind 7), `003A6C30` (kinds 8/10),
  `0026E350` (kind 10), `003B2CA0` + `0057A040` (kind 14) — so the two fronts are the same
  operation applied to the same 14 object kinds, differing in what each does with the result.

**How the fronts differ.** `003A56F0` is the *compute/query* front: its caller `002F3360` (itself a
3-way front on byte `[rcx+0x90]` — kinds 1/2 handled inline, default → `003A56F0` at `002F33EA`)
passes `movsx` byte `[r11+0x13B]` and id `[r8+0x44]`, and `003A56F0` writes its result xmmword into
the caller's `rdi + 0x30` out-param plus global `022D92F0` (`002F33EF`–`002F33FB`). `002F3360`'s
callers are spread wide (`003D92C0`, `0045E3C0`, `0045F140`, `00523380` ×2) — a general
query interface. `003A56C0` is a tail thunk into `003A56F0` used by the `00537xxx` record-store
family. `003A4290` instead loads a 16-byte scratch record via `00430B90` on `[rdx+0xFC]` at entry —
the *load/init* front — and is reached by **four tail-jumps in the same `00537xxx` record-store
family** that drives `003A56C0`: `jmp 003A4290` at `00537C6E` (in `00537C50`), `00537EFE` (in
`00537EE0`), `00537F5E` (in `00537F40`), `0053879E` (in `00538780`). The earlier "no call site"
claim rested on a linear sweep that halted at an undecodable byte; the per-function census
corrects it — `003A4290` is the `00537xxx`-driven twin of `003A56F0`, not an orphan.

**Not read:** the inner-table subtype selectors, the kind-3/6 arm interiors, and every per-kind
helper body. The roles above are arm-level call signatures only.

### 2.7 The `0x50`-kind record store — `00500980` load front, `00500850` destroy front (SWE2-FRONTIER, switch-families package)

A second, independent store keeps the `0x50`–`0x59` record kinds — a base-relative
intrusive list headed at `02EBEF70` whose nodes are reached by handle through
`0020E600` (resolve) and written back by `0020E620` (store), never by raw pointer. Each node
carries the stream key it was loaded under: `{+0xC u16 key, +0xE u8 kind, +0xF u8 sub}`
(matched at `003A9F10`–`003A9F28` in `003A9EF0`, `003A9E23`–`003A9E39` in `003A9E00`). Three
entry points own the list:

- **`003A9EF0` (714 B) — find-or-create.** The stream's first four bytes are the key; on a
  hit it calls `00500980(node, stream+4)` and returns the load's advanced cursor
  (`003A9F3F`–`003A9F47`). On a miss it re-dispatches the kind byte `stream+2` − `0x50`
  through its own RVA table `003AA1BC` (site `003A9F6C`): each arm is
  `new(size)` → `ctor(node, &key)` → `load(node, stream+4)` — e.g. kind `0x54` allocates
  `0x190`, runs ctor `004354E0`, loads via `00436D00` (`003A9F78`–`003A9F9D`) — then links
  the node at `02EBEF70` when the list is empty (`003AA10E`–`003AA11E`).
- **`003A9E00` (210 B) — find-and-destroy one node** matching a key argument
  (`003A9E55` unlink, then the `00500850` destroy front).
- **`003A9D00` (242 B) — destroy-all walk** of the same list, unlinking each node
  (`003A9D30`–`003A9D8D`) through `00500850`.

Both fronts dispatch on `node+0xE` with `movsx`/`−0x50`/bound-9 (`00500984`–`0050098E`,
`00500856`–`00500863`). **`00500980` (176 B) is a pure table — every arm is
`call kind_loader` then `mov rdx, rax` + `ret` (`005009AB` ff.), so it returns the cursor
the loader advanced past its record.** **`00500850` (262 B) is the mirror: each arm calls
the kind's *destroy* body then tail-jumps `003697F0`** — the null-guarded node free
(`test rcx,rcx; jmp 00369860`, `003697F0`–`003697FC`). The two fronts cover the same type
space, as the paired kind tables show:

| kind `+0xE` | node size (miss path) | ctor | load (`00500980` arm) | destroy (`00500850` arm) | record shape |
|---|---|---|---|---|---|
| `0x50` | `0x48` | `005019D0` | `00502CB0` | `00501950` (thunk `00501A40`) | group/parent record: `count16`→`+0x38`, two `count8`→`+0x3A`/`+0x3B`, `dword`→`+0x3C`, then N×`0x70` records copied to `[+0x10]` and M/K child refs resolved `003AA280` as kinds `0x52`/`0x53` into `[+0x28]`/`[+0x30]` (`00502CCA`–`00502E7C`) |
| `0x51` | `0x1C` | `00503790` | `00503880` | `00503830` | two base-relative object refs at `[+0x18]` — resolve-and-free the old referents (`0020E600`×2 + `003697F0`, `005038A9`–`005038C3`), then `0036A100` + `00861EBA` load of the new ones; flag `+0x16 bit 0` gates the free |
| `0x52` | `0x1D0` | `00500B70` | `00500C00` | `00500AA0` (thunk `00500BF0`) | large flat record: kind byte stored masked-`0x3F`→`+0xA0` with its bit6/bit7 unpacked to `+0x1C8`/`+0x1CA` (`00500C39`–`00500C58`), words to `+0x1CC`/`+0x1CE`/`+0xA8`/`+0xAA` mirrored to `+0xA4`/`+0xA6`, a flag byte `ptr+2 & 8` on a pointer loaded at `00500CB5`/`00503E7E` mirrors into `+0xA3 bit 0` (`00500CBC`–`00500CD2`), inner dispatch on `+0xA2` |
| `0x53` | `0xC0` | `005014B0` | `00501520` | `00501440` (thunk `00501510`) | string-bearing record: `001837A0`/`00183760` string helpers around `0036A100` + `00861EBA` (`0050158F` ff.); tail fixups `002D81D0`, `003A22A0`, `003A1DB0` |
| `0x54` | `0x190` | `004354E0` | `00436D00` | `004352C0` (thunk `004355C0`) | the mesh record — §22.2 of the residual page walks it field by field |
| `0x55` | `0x20` | `00503C50` | `00503CD0` | `00503CA0` | counted fixed-size array: `count16`→`+0x10`, `0036A100(count·48)` → `[+0x18]`, `00861EBA` from `stream+4` (`00503CFC`–`00503D27`) |
| `0x56` | `0x20` | `00503D50` | `00503E30` | `00503DE0` | pointer-carrying record, `00503880`'s shape — resolve/free old referents, then resolve-store + alloc + `00861EBA` the new (`00503E49`–`00503F30`) |
| `0x57` | `0x30` | `00503F50` | `00504060` | `00504000` | same shape as `0x56` plus `003D7F30`/`003D7CE0` resource lookups around the copy (`00504078`–`0050412E`) |
| `0x58` | `0x20` | `00504170` | `00504230` | `005041F0` | single blob: `dword count`→`+0x10`, `dword bytes`→`+0x14`, buffer `0020E620(0036A100(size))` → `[+0x18]`, `00861EBA` from `stream+0x10` (`00504245`–`005042A2`) |
| `0x59` | `0x30` | `005042C0` | `00504350` | `00504320` | string/wstring record: `0036C1D0`/`0036C140` pool helpers around `0036A100`/`0036A190` + `00861EBA` (`00504374`–`00504432`) |

**Every loader runs its kind's destroy body first** — `00502CB0` opens with
`call 00501950` (`00502CCA`), `00500C00` with `call 00500AA0` (`00500C1E`), `00501520` with
`call 00501440` (`00501535`), `00436D00` with `call 004352C0` (`00436D20`) — so a
`00500980` reload is a reset-and-reload in place, which is what makes the `003A9EF0` hit
path safe to call on a live node. The full per-case evidence table is
[switch-family-record-store-5x.tsv](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/members/switch-family-record-store-5x.tsv).
Field-level reads inside the `0x56`/`0x57`/`0x59` loaders are call-shape only — their
offset maps are not walked.

### 2.8 The authored type byte — corpus census and the element-`+0` copy (SWE2-DATA, 2026-09-16)

> **Census re-walked 2026-09-29 (FABLE, GI-8) - the figures below undercounted.** The walk that produced them
> ([effect_type_usage.py](members/effect_type_usage.py)) reads every file as one chunk stream from `+0x10`. An `.efb`
> is not one: it carries its EFX streams as embedded blobs ([EFX and EFB](efx-and-efb-effect-containers.md) §3), so all
> 410 `.efb` walks stopped at the first blob header; and 531 further EFX streams ship **embedded in `.cm` model files
> (144) and `.mpk` map-control plans (387)**. [`type_census.py`](members/type_census.py) walks every stream to its
> declared size (header `+0xC`; all 3,698 + 531 end exactly there) and, as its positive control, reproduces every row of
> the earlier tsv with the earlier walk. Result ([type_census.tsv](members/type_census.tsv)): **55 distinct types in
> 48,868 `0xA00` records over 4,229 files** (the payload's first byte is 0 in all of them), and **53,351 `0x800`
> chunks**, subtypes still `0`–`8`. **`0x04` (173 chunks) and `0xA3` (447) are authored** after all; the ten types no
> shipped effect uses are `0x03`, `0x07`, `0x08`, `0x70`, `0x81`, `0x8A`, `0x97`, `0xA0`, `0xA4`, `0xA9`. *Which loader
> caller takes the `.mpk` streams is not traced here; the model path `003B38B0` → `003EDAD0` is on
> [the FEF and motion entries page](../Model-And-Motion-Formats/fef-and-motion-entries.md).* The superseded figures are
> kept, struck, below.

**Where the type byte lives in the files.** Walking all **3,698** shipped `.efx`/`.efb` (the
[effect-mesh census corpus](effect-mesh-records-kind-54.md); `Tools/work/DATA/mesh54/fx_all`):

- **`0xA00` chunks carry the element type at chunk `+0xE`** — the third byte of the record header
  `{u16 id, u8 type, u8 pad}` at `+0xC`; the payload proper begins at `+0x10`, and its first byte
  is `0` in **all ~~31,635~~ 48,868 records**. The `+0xE` histogram spans `0x00`–`0xD1` with **~~53~~ 55 distinct
  values** — the authored type population (~~[effect-type-authored-usage.tsv](members/effect-type-authored-usage.tsv),
  generator [effect_type_usage.py](members/effect_type_usage.py)~~ superseded 2026-09-29 by [type_census.tsv](members/type_census.tsv),
  generator [type_census.py](members/type_census.py)).
- **`0x800` chunks never carry an element type.** Their `+0xE` is a sub-record **subtype** bounded
  `0`–`8` over all **~~32,639~~ 53,351** chunks — a different record class (the 320-entry table at
  `02EBEF90` via `003A9730`, subtype bound at `00442460`), not a small-type family.

**Every authored type has its own code path.** Of the ~~53, **42**~~ **55, 40** carry dedicated arms in the step /
update / walk / setup dispatchers, and **all ~~11~~ 15 remaining types** (`0x42`, `0x68`–`0x6B`,
`0x71`–`0x74`, **`0xA3`**, `0xA6`–`0xA8`, `0xAA`, `0xAB`) sit inside the `0x42`–`0xAB` sub-range *(corrected 2026-09-29: the
earlier list already named 14, not 11; the new population adds `0x04` to the main-range and `0xA3` to the sub-range types)* and carry
dedicated arms in *all four* sub-dispatchers (`0043EBF0`, `00538910`, `0043EAB0`, `0043ED30`). No
authored type falls through to a true default. Usage is skewed hard: ~~type `0xA2` alone is 6,235
chunks in 1,952 files; type `0x05` (the kind-`0x54` mesh element) is 5,164 in 1,088; three types
are authored exactly once (`0x62`, `0x8B`, `0x8E`) and five appear in a single file each.~~ **(2026-09-29)** the largest are
`0x02` (7,523 chunks), `0x8C` (7,509), `0xA2` (6,303 in 2,018 files) and `0x05` (5,204 in 1,115); **one type, `0x8B`, is
authored exactly once, in one file** (`0x62` has 2, `0x8E` 136).

**Who installs it into the element.** The chain is closed end to end:

```
0xA00 chunk +0xE  (authored file byte)
  → 003A9A70 publishes the record and writes it into definition +0x44
  → instance +0x108 holds the definition
  → 002F2D60 stores [instance+0x108] into element +0x20, then at
    002F30F2/002F30F6 copies [element+0x20]+0x44 into element +0
```

`002F2D60` is the type-`0x00` step arm **and** the shared step-base routine — every one of the 47
step case handlers calls it (call sites `002F3BFB`, `00442529`, `004427A9`, …). Its prologue wires
the fresh element to its spawn record `[instance+0x100]` → `element+0x18`, its instance → `+0x8`,
its definition → `+0x20`, and ~~clears the flag byte `+0x1`~~ clears bits 1 and 2 of the flag byte `+0x1` *(corrected 2026-10-02, OPUS: `002F2D60`+0x44 `and byte ptr [rcx + 1], 0xf9`)*; the tail of the same body fills the
element's transform block and defaults the colour word `+0x1F0` to `0x80808080` (the dominant value
of the mesh `+0x28` array) before stamping the type byte. So the element's dispatch key **is** the
authored byte, installed by the routine all step arms share.

**The `00441970` definition-kind switch** (the addendum's second table). When the action-context
byte `[02F97348]+0x36A` bit 0 is **set**, every instance sets the render byte `02AEE910` and walks
its element chains unconditionally. When that bit is **clear**, `00441970` switches on the
definition kind `[[instance+0x108]+0x44]` over `0x40`–`0xD0` — and the switch is **degenerate**:
exactly two targets ([effect-kind-441970.tsv](members/effect-kind-441970.tsv), generator
[effect_kind_switch.py](members/effect_kind_switch.py)):

| kind | arm |
|---|---|
| `0x40`, `0x41`, `0xA1`, `0xA2`, `0xA5`, `0xD0` | `004419D0` — set `02AEE910` from def `+0x4A`/`+0x4C` (or `020926F8`), then walk the element chains |
| all other kinds (139 of 145) | `00441A89` — the function tail (`add rsp,0x20 / pop rdi / ret`): **the chains are not walked at all** |

So the definition kind decides *whether the instance's elements step at all* on a frame the global
bit doesn't force — six kinds walk, the rest are skipped.

## 3. Key addresses

| address | role |
|---|---|
| `002F3BC0` | ~~per-frame~~ step (birth) dispatcher (47 cases; default → `0043EBF0`; frame counter `+0x3C`) |
| `0043EBF0` | sub-range dispatcher for types `0x42`–`0xAB` (18 handlers) |
| `002F3910` | update dispatcher (47 types → 38 routines; default `0043EAB0`) |
| `002F2530` | the shared base of every update routine |
| `00441B30` | element loop |
| `003A8AE0` | loop entry from the sub-resource walker |
| `003A8D80` / `003A72F0` | the instance-list walk (`02EBEF88`, current instance `02EBEF80`) |
| `00441970` | one instance: kind switch, element chains `+0x118` / `+0x128` |
| `002F4020` | the third type dispatcher: rate gate, 46 arms, default `0043ED30` |

## 4. Data structures

```
element  +0x00  u8   type, 0..0xD1
         +0x3C  f32  frame counter, +1.0 per step (unless paused)   <- corrected 2026-10-02, OPUS - += dt in every update (002F2530+0x52); the step adds 1.0 once, at birth, and only when 00314960() is non-zero and 001EDDA0() is 0 (002F3BC0+0x281..+0x2A0); 001EDDA0 is the frame-rate test (0 only while 01F82E38 is set by 001EDDC0+0x28 and 01DFE0C0 is 0), not a pause
         +0x224 u16  stamp from 00250000(), set each step
         +0x226 u16  cleared each step
```

## 6. Type groups read so far

| group | page | status |
|---|---|---|
| `0x00`–`0x0A` (base + first derived) | [the-element-types-00-0a](the-element-types-00-0a.md) | method vocabulary + per-type record maps read; ~~step/update tail helpers and emit calls `not read`~~ step/update tails read on an-effect-element-frame-by-frame.md (nine tails and the shared helper `0044B960`), emits in UQ-204 *(answered: see those pages; 2026-10-02, OPUS)* |
| `0x60`–`0x74` (main `0x60`–`0x67` + sub `0x68`–`0x74`) | [the-element-types-60-74](the-element-types-60-74.md) | record maps + helper roles (PRNG `0044B960`, deferred-free queue `0024B1C0`); `0x70` confirmed definition-only; tails `not read` |
| `0x80`–`0x97` | [the-element-types-80-97](the-element-types-80-97.md) | shared-method band: sibling types share step/update/setup; variant-selector walks found (record flag bytes `+0x294`/`+0x2A4`/`+0x330`/`+0x337` pick emit paths) |
| `0x40`–`0x42`, `0xA0`–`0xAB`, `0xD0`–`0xD1` | [the-element-types-40-42-a0-ab-d0-d1](the-element-types-40-42-a0-ab-d0-d1.md) | completes all 65 handled types; `0xD0`/`0xD1` carry their payload in the seventh method; `0x41`/`0xD0` share the 5 B update stub `00464F10` |

## 7. What is not known

- [x] **UQ-204 — ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5): what each of the 65 types puts on screen is a table**
      ([record](../../_index/candidates/uq204-element-type-emits/README.md), `uq204-element-type-emits.tsv`, control `uq204_emits.py`). The counts:
      - 7 GiPrim types and 2 sprite types;
      - 43 GiVmax runs of a named VU1 program (their shapes are UQ-213's, per program);
      - 6 raw GS packets, which the PC build never submits;
      - 7 state-only types.
      *The selector half, kept:* **HALF ANSWERED 2026-09-16 (SWE2-DATA).** Which authored data selects the type:
      the `0xA00` chunk's record-header byte at `+0xE`, proven corpus-wide (§2.8) and copied to
      element `+0` by `002F2D60` (`002F30F2`). ~~*Not* answered: what each of the types is.~~ *(answered: see the UQ-204 answer above; 2026-10-02, OPUS)*
- [x] **UQ-205 ANSWERED 2026-09-16 (SWE2-DATA).** The tables are
      [effect-type-methods.tsv](members/effect-type-methods.tsv) — 210 rows, all ten dispatchers
      including walk `002F4020` and the shared-routine groups (e.g. `00538EB0` serves types
      `0x06`/`0x07`; the five `0x80`–`0x97` rows share `0044CC10`/`00450480`/`00539320`) —
      plus [effect-kind-441970.tsv](members/effect-kind-441970.tsv) for the definition-kind
      switch.
- [x] ~~**UQ-206.** What `002F2530` does, beyond being every update routine's base.~~
      *Narrowed 2026-09-14 (FABLE): the entry and the lifetime logic are read; the per-frame body is not.* The 2,094-byte
      body opens with the gates and bookkeeping every element update shares:
      1. **A pending hold.** While word `+0x224` is set, a 7-byte query runs first.
         - A non-zero answer lets the update continue with the word still set.
         - Otherwise the word is cleared, and the update continues only if the 27-byte runtime query answers non-zero
           (`002F2550`–`002F2572`).
      2. **Once per game frame.** If `+0x38` already equals ~~the global frame stamp `[02EBEF88]`~~ the frame stamp `dword [[02EBEF88]]`, the first dword of the current context's `+0x1B8` block that `02EBEF88` points to *(corrected 2026-10-02, OPUS: `002F2530`+0x44 `mov rax, qword ptr [02EBEF88]`, +0x4B `mov ecx, dword ptr [rax]`, +0x4D `cmp dword ptr [rbx + 0x38], ecx`; `0024D540`+0xC6 `lea rax, [rdi + 0x1b8]` is what +0xCD stores)*, it returns 0. Otherwise
         `+0x3C += dt`, the float in `xmm2` (`002F2574`–`002F2587`).
      3. **A half-rate gate** for element types `0x67`–`0x74` in the bit set `0x341B`, when a 27-byte runtime query
         answers 0. Such an element skips the frame while `trunc(+0x3C)` is odd (`002F2595`–`002F25B0`).
      4. **Expiry.** With a non-zero lifetime `+0x4C`, once the even-rounded `trunc(+0x3C)` exceeds it, the element is
         released through ~~the 394-byte kind-3 release and~~ the type's seventh method (`002F25C5`–`002F25D8`), **after
         the 394-byte child-spawn slot routine `003A8950` runs with trigger 3 - that routine spawns and releases nothing
         itself; the release is `002F31C0` (corrected 2026-09-29, OPUS falsification pass 1, `CON-179`)**. The update
         returns 0.
      5. **Whole frames.** Otherwise `n = trunc(+0x3C) − +0x44`. If `n ≤ 0` it returns 0. Else it increments `+0x48`, stores
         the current frame in `+0x40`, and advances `+0x44` (`002F25E4`–`002F262A`).
      6. **The body.** It then samples the element's tracks through a 155-byte key sampler (three consecutive calls from
         `002F2693`), and reaches the completion calls near its end (`002F2C69`, `002F2C76`).
      **Not read:** the track semantics between steps 5 and 6, and the definition byte `+0x44 == 0xA0` branch at
      `002F262D`.
      ***ANSWERED 2026-09-17 (FABLE): beyond the gates, `002F2530` is the shared motion integrator: it samples the element's three motion tracks, then, once per whole frame, rotates and advances the position on the workbench row, applies a floor arm chosen by the definition, wraps the angle accumulators, refreshes attachments and finally decides completion.** *The `0xA0` branch*: when the definition byte `+0x44` (at `[element + 0x20] + 0x44`) is `0xA0` or more the body is skipped and the frame count returned (`002F262D`..`002F2637`). *Sampling*: the key sampler `004309C0(track, frame +0x44)` runs on the definition's track block `[element + 0x20]` at `+0x00`, `+0x20` and `+0x10` (`002F2693`..`002F26C5`), and the results are cached as `+0x1F8` = track 0 times `+0x50`, `+0x200` = track 2 plus `+0x58`, `+0x1FC` = track 1 plus `+0x54` (`002F26CA`..`002F2707`), with the difference of tracks 0 and 2 scaled by `[008C5F6C]` (degrees to radians) as the turn and `+0x1FC` scaled by `-0.1` (`[00900308]`) as the per-frame vertical term. *Per whole frame* (`n` from step 5, loop `002F2750`..`002F2B84`): the workbench row `022D92E0` receives `+0xB0` plus `+0xC0`, directly when track 0 is exactly zero (`002F2750`..`002F27C9`) and otherwise after `003A2B20` has rotated `+0xB0` by the turn and `003A2900` has run on it (`002F27CE`..`002F2864`); the vector `(0, vertical, 0, w)` at `022D92F0` is then added (`002F286C`..`002F28D7`), so the velocity gains the vertical term and the position the velocity, and `+0x6C` is set to `1.0` on one arm (`002F2963`). The definition byte `+0x45` picks the floor arm: 1 compares the height `002F3750(element, context)` with `+0x64` and, when above it, negates the vertical velocity `+0xB4` (sign mask `[01CEBDA0]`) and damps it by byte `+0x46` percent (`[008F3134]` = 100) (`002F2A00`..`002F2A4E`), a bounce; 2 makes the same test and, when above, ends the element through `002F3890`, `003A8950(3, element)` and `002F31C0` (`002F2A50`..`002F2A5F`, `002F2D37`..`002F2D52`). The three angle accumulators `+0xE0`, `+0xE4`, `+0xE8` are then wrapped by one turn, `[01CEBC78]` = 2π down and `[00915624]` = -2π up (`002F2AE9`..`002F2B77`). *After the loop*: flag byte `+1` bit 1 resolves an attachment through `003A8240(context +0x1C, +0x204)` and bit 2 through `003A8F80(+0x218, +0x21E, +0x21C)` checked by `00441EE0(result, +0x210) == 1` (`002F2B8A`..`002F2C4D`). *Completion*: with the definition's `+0x44` at zero, and either ~~the pause predicate~~ the frame-rate test `001EDDA0` true *(corrected 2026-10-02, OPUS: it returns 0 only while `[01F82E38]` is set and `[01DFE0C0]` is 0, `001EDDA0`+0x0..+0x12; the 60 fps arm `001EDDC0`+0x28 sets `01F82E38`)* or `+0x40` bit 0 clear, ~~the element is released (`002F3890`) and completed with kind 2~~ **`002F3890` shifts the position history (`+0x70` to
`+0x80`, the parent-transformed `+0x60` to `+0x70`) and copies the colour `+0x1F0` to `+0x1F4` - it releases nothing - and
the child-spawn slots run with trigger 2; the definition's `+0x44` is the element type, so this is type `0x00`'s own
spawn step, with no cull (corrected 2026-09-29, OPUS falsification pass 1, `CON-179`; precision on SWE2-AUDIT-SPEC's
batch-7 review: this gate reads definition `+0x44` at `002F2C51`, while the dispatcher `002F3910` reads the element's
byte 0, and the two agree through the constructor copy `002F30F2`)** (`003A8950`, `002F2C4D`..`002F2C76`). *Return*: when ~~the pause predicate~~ the frame-rate test `001EDDA0` *(corrected 2026-10-02, OPUS: not a pause, as above)* is false, the owner record at `[[element + 8] + 0x10]` supplies its bytes `+0x3AC`, `+0x3AE`, `+0x3A2` and, unless the element type is `0xD1`, `001EDBB0(+0x40, byte)` may veto the frame with 0 (`002F2C7B`..`002F2CC1`); otherwise the whole-frame count is returned. The callees are named here by what this body does with them; their own bodies were not read. Static, the 2,094-byte body read end to end.*
- [x] **UQ-207 ANSWERED 2026-09-15 (OPUS) — they walk the *same* list with the same
      per-node call. The only difference is where the step comes from: `0043EF40` is **caller-timed**
      and `00442310` is **self-timed at a fixed wall-clock rate**.**
      - **The loop is identical in both.** Head `rcx = [obj+0x118]`, next `rbx = [node+0x30]`,
        `rdx = obj`, then `002F3910(node, obj, xmm2)` per node — `0043EFB0`–`0043EFC5` and
        `00442341`–`0044235F`. Both bail early when `[obj+0x100]` is null.
      - **`0043EF40` passes its caller's float straight through.** Incoming `xmm1` is saved to
        `xmm6` (`0043EF5D`) and handed over as `movaps xmm2, xmm6` (`0043EFB4`), loop-invariant.
      - **`00442310` has no float parameter and builds the step itself:** `xmm6 = [01CEBC08]`
        (`.rdata`, `2.0f`) once, then **every iteration** reloads `xmm2 = [01DFE0BC]` and multiplies
        (`00442341`, `00442350`). The step is **`2.0 × [01DFE0BC]`**.
      - **And `01DFE0BC` is already identified — it is the reciprocal of the frame-rate scale.**
        `Z-11` reads the triple `{01DFE0B4 int mode, 01DFE0B8 scale, 01DFE0BC reciprocal}`, written
        together by `001EDDC0` as `{2, 2.0, 0.5}` and shipping as `{1, 1.0, 1.0}`; `K-8` shows all
        three writes happen once at startup and never during play; `Z-10` settles that it is
        **frame-rate compensation, not a speed selector**.
      - **So `00442310`'s step is `2.0` at 30 fps and `1.0` at 60 fps** — half the advance per tick
        at twice the tick rate, i.e. **the same advance per unit of wall-clock time**. That is the
        multiply-by-the-reciprocal idiom `Z-10` describes, and this is a use of that triple on the
        effect side rather than a new finding about it.
      - **The rest of `0043EF40` is not shared at all.** It carries a stack cookie, and before the
        loop it gates on `[obj+0x1B0]`: non-zero calls `00250000`, and if that returns `0` it clears
        `+0x1B0`, calls `001EDDA0`, and returns `1` when *that* returns `0`
        (`0043EF63`–`0043EF86`). After the loop it continues — `+0x139`, then `[+0x2C]` against
        `(float)[+0x28]`. **`00442310` ends at its loop and does nothing else**, so `0043EF40` is the
        full per-frame update and `00442310` a bare pump. **UQ-207.**

## 8. Evidence

- **Dispatcher census** (`Database/Tools/work/FABLE/pub140-scratch/tools/fx_dispatchers.py`): scans every listed function
  for `movzx eax, byte [rcx]` bounded at `0xD1` with a two-level jump table. It finds exactly `002F3910` and
  `002F3BC0`; `0043EBF0`'s sub-range form was read by hand.
- **Callers:** the raw E8/E9 index, one target per command.
- **The 51-member 56-byte form:** the image-wide form census (`Database/Tools/work/FABLE/accessor-family/arch_forms.txt`,
  form #14).

## 9. Related

- [EFX and EFB effect containers](efx-and-efb-effect-containers.md): the file side.
- [Where the game's memory comes from](../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md): the effect constructors' arena selection.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — CLIENT.** `FUN_0031adb0`, owned by that layer, calls `003590D0` on this page. That caller is a 1,790-byte routine with a stack cookie and a `0x80`-byte frame; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — CLIENT (19 edges through 7 of this page's functions).** The Party layer reaches this page at `003590D0`, `003589B0`, `00265020`, `0031ADB0` and 3 more. `FUN_00303cc0` is the worked example, read in full - it is a 205-byte step that runs only when the mode query answers **2**, and then works through selector `3`; **5 of the 15 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `Loot_FindOverlappingPickupIndex`, owned by that layer, calls `00265020` on this page. That caller is the pickup-overlap search: it takes the actor's position from the unit's `[+0x10]`, then scans the **parallel arrays at `022BE7F0` and `022BE800`** - a presence byte per slot and a `0x20`-byte record per slot - against the radius it is given; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT.** `FUN_0024b9b0`, owned by that layer, calls `001EDDA0` on this page. That caller is a 1,500-byte routine whose second argument being **8** short-circuits it to a single arm before any of the rest runs; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**ActorEntity — SERVICE (SWE2-CONTRACT 2026-09-15, 22 edges).** The dispatch bodies resolve the
actors their elements attach to: `003A40F0`/`003A56F0` call `ActorHandle_ResolveRegistryEntryByPackedId`
`003588B0` and `Actor_GetWorldPosition` `00265020`; `003A4290`/`003A56F0` call
`ActorHandle_EncodeRegistryEntry` `003589B0`, `ActorManager_GetRecordByOrdinal` `00358940`,
`00263FF0` and `00263C30`. The ten caller-direction edges are ActorEntity bodies
(`ActorManager_RunFieldRuntimePass`, `ActorManager_BindLoadedDefinitionPayload`, …) sharing the
`003590D0` focus-handle getter. An element's world anchor is an actor — the handle/position lookups
are the crossing; the `003590D0` callers are shared-accessor fan-in.

**Movement — SERVICE (SWE2-CONTRACT 2026-09-15, 18 edges).** `003A4290`/`003A56F0` call Movement
helpers `0026E350` and `00264670` (which itself calls `00231820`/`00231900`) while positioning
elements. The fourteen caller edges are Movement bodies sharing `003590D0`
(`Movement_UpdateSteeringTowardTarget`, `PartyFollow_SolveFormation`, `BattleUnit_CanAdvanceCombatNavigation`,
`Movement_SetRequestedSpeed`, …) plus `WorldActor_UpdateRuntimeAndScriptExecutionState` sharing
`001EDDA0`. The two callee lookups are real service calls; the callers are `003590D0`/`001EDDA0`
fan-in.

**Audio — MECHANICAL (SWE2-CONTRACT 2026-09-15, 6 edges).** `003B99D0` shares `001EDDA0`/`003A3FD0`/`003A6BA0` (3
edges); `00362850` shares `00265020`/`003590D0` (2); `0024D540` calls `003B3D20` (1). Shared
helper fan-in only.

**CoreRuntimeScheduling — MECHANICAL (SWE2-EC7-167, 29 edges).** `00181DD0` — the allocator
batch-132's `02B4D7D0` issuer `003D7FF0` calls — is itself called by `0022B8C0` on that layer;
the remaining edges are the shared allocator/pump callers (`0019C5A0`, `001DB220`, `001DB340`
callees `001A1470`, +25 more). The pointer codec `0020E600`/`0020E620` this page names is named
substrate and excluded as a subject. Shared-runtime fan-in only; no scheduling responsibility
in the dispatch.

**StoryEvent — MECHANICAL (SWE2-EC7-190, 2 edges).** This page's spot gate `001EDBB0` and StoryEvent's `001ED240` share two callees: the string-ref builder `001C50C0` and the mode check `001EC560`. The crossing is shared-helper fan-in - both callers consume the same query helpers, not a shared responsibility for the gate.

*Added 2026-09-29 (FABLE, GI follow-up): the layer the GI answers widened on this page's audit.*

**Resource — SERVICE, CLIENT and MECHANICAL (16 edges).** Resource bodies call effect bodies on this page: the management-table slot release `003B37E0` (slot = the id's low six bits, `0x38` stride) calls `0024F4D0` and then `0024F410` on the slot's `+0x18` object before returning the slot to its free list, and the effect-source initialiser `00409FE0` calls `003B38B0` once it has resolved the entry's sections. In the other direction, the shader-material body `00366B80` calls `0024A5A0`, a name-keyed lookup over a 64-entry registry, and `003B8260` and `00421E20` call `ResourceTable_ResolveEntryByIndex` (`002ED570`). The remaining edges are resource bodies calling the two allocator entries this page cites for its record builds: `0036A100` (allocate from the engine pool, with a fallback pool, and stamp the block header) is called by `00249210`, `0024EF90` and `0024F240`, and its flagged thunk `0036A190` by `00249210`, `0024A1D0`, `00259DF0`, `0032E7C0`, `00379E90`, `00384420` and `0051ED10`. The resource layer creates and releases the effect objects that sit in its tables, and the effect dispatch looks up names and entries through that layer; the allocator edges are shared memory machinery with no shared ownership.

*Added 2026-09-29 (FABLE, pass-22 debt).*

**Script_VM_Native_Bridge — CLIENT and MECHANICAL (57 edges: 54 verb handlers calling six accessors this page cites).** Nothing on this page calls into the script layer; every edge is a verb handler calling a shared accessor the dispatch bodies also use. Verb names are from [the verb table](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv); the six accessors were read, the handlers are identified by that table and not read one by one.
- *`Actor_GetWorldPosition` `00265020`, 23 edges - CLIENT.* The position verbs `getx`/`gety`/`getz` and their twins, `getangle`, `getlength2`/`getlength3`, `checkdistance`/`checkdistance3d`, `rturna`, `normalclipzx`, `usemapid`/`partyusemapid`, `offsetsoftimage`, the battle-script `btlAtelGetMyPosX`/`Y`/`Z` and `debug_getucpcpos` read an actor's position through the getter an element's world anchor uses (representative: `checkdistance3d` `00350DD0`).
- *`InputDevice_QueryAvailabilityState_Always1` `0053DD10`, 17 edges - MECHANICAL.* The body is `mov eax, 1; ret`. The script's sync polls (`modelreadsync`, `musicreadsync`, `effectreadsync`, `voicereadsync`, `motionreadsync`, `entryreadsync` and others), `captureactor` and a few debug verbs call it as a gate that always answers 1 (in `modelreadsync` `00341840` the test at `00341876` always takes the same arm); this page cites it only as a callee of the type arm `00462540`. One constant body reached under unrelated names; no relationship.
- *`PartyFocus_GetCurrentPackedActorHandle` `003590D0`, 14 edges - CLIENT.* A 7-byte read of `[022C7FE0]`. Verbs that act on the controlled character (`ucsetpos`, `ucmovesync`, the four `checkdistance` forms, `talktreasure`/`talktreasureafter`, `hideparty_without_uc`, `setupsummonforevent`, `debug_isucpc`/`debug_getucpc`/`debug_getucpcpos`) read the same focus handle the two anchor fronts use as their kind-5 helper.
- *`00203170`, 1 edge (`seteventlightdir` `00356160`) - MECHANICAL.* The 44-byte identity-matrix store: four 16-byte rows copied from ~~`008C5F80`..`008C5FD0`~~ *(corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's auditsem-review-p22-fable-0930 §2 N2:)* `008C5F80`, `008C5F90`, `008C5FB0` and `008C5FD0` (not a contiguous run) to `[rcx]`.
- *`00264670`, 1 edge (`getgroundy` `00343520`) - CLIENT.* The verb pushes, as a float, the same movement-context `+0xD4` value the floor probe `002F3750` reads (`0034352C`-`0034353C`).
- *`0036A100`, 1 edge (`debug_tkmalloc_4` `0050D8F0`) - MECHANICAL.* The allocator the kind loaders of the node table (`0x51`-`0x59` rows) size their blocks with.

## The `0052A130` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0052A130` (~776 B) — `002F2D60(rcx)` non-zero gate
(`0052A139`/`0052A13E`).

| member | role | interior |
| --- | --- | --- |
| `00547DD0` | `rax = rsp` EH-frame body (`00547DD0`/`00547DDF`) | [`00547DD0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `002F2D60`.

## Interior citation — frontier hub `002F2D60` (2026-09-17, SWE2-EC7)

`002F2D60` — 1,111 B, 41 frontier callers at census; case-arm 1 of the `002F3BC0` dispatcher per
§2.1. Interior verified: [`002F2DD6`](../../_index/ADDRESS-INDEX.md) is
`movzx ecx, byte [rsi+0x283]` — the body initialises the `rcx` out-record from `rdx` (links
`rdx`'s `+0x100`/`+0x108`, copies the `+0x80`/`+0x90` quads to `+0x60`/`+0xB0`, ~~clears `+1` bits~~ ANDs `+1` with `0xF9`, clearing bits 1 and 2 *(corrected 2026-10-02, OPUS: `002F2D60`+0x44)*
~~`0xF9`~~), then switches on the source's `+0x283` subtype byte over `{2,6,7,9,10}` to fill
variant-specific tails (`+0x210`..), finishing with a `003A8950` call when the linked record's
`+0x44` byte is clear and a final `+0x208` field write from a global object's `+0x1C`.

NOT claimed: the five subtype arms' field semantics (each is a different element presentation)
or which record type carries `+0x283`; the dispatcher's other 46 arms are likewise not covered
by this read. (Page status PARTIAL: this citation is evidence-bearing once the page's own
readiness lands, not an A-measurement today.)


## Interior citation — frontier hub `003A8240` (2026-09-18, SWE2-EC7)

`003A8240` — 71 B, 10 callers; the attachment resolver `002F2530` calls on flag byte `+1`
bit 1. Interior verified: it walks the intrusive list at `02EBEF98` via `[rax+0xF0]`
(`003A8253`–`003A827F`), accepting the node whose `word [+0x100]` matches `ecx` AND whose
`[+0xE0]` sub-record's `word [+0xC0]` matches `edx`
([`003A8255`–`003A827A`](../../_index/ADDRESS-INDEX.md)). Two-key lookup: list position then
sub-record tag.


### Interior citation — frontier hub `00264670` (2026-09-18, SWE2-EC7)

`00264670` — 35 B, 7 callers: the kind-`0x60` gated float getter the
positioning arm calls — `(byte[rcx+3] & 0xE0) == 0x60` or 0.0f, then
`movss xmm0, [[rcx+0xB8] + 0xD4]` at
[`00264686`](../../_index/ADDRESS-INDEX.md) — the `+0xD4` field the battle-unit
map names `movementStateD4Snapshot`.

## SWE2-EC7-33 update (2026-09-19) - `00523380`

`00523380` (2,160 B) is the type-dispatch element walker - 11 `004309C0` calls plus `0042FDB0`/`0026EE00`/`00462260`/`00430B90`/`003D8E50`. Interior anchor `005233FC` (a `004309C0` call).

## SWE2-EC7-33 update (2026-09-19) - `004453D0`

`004453D0` (1,914 B) is the same walker shape - `004309C0`/`0036DD80`/`0026EE00`/`004314E0`/`00430B90` with the `00861F08`/`00861F0E` trig pair. Interior anchor `004459FE` (a `004309C0` call).

## SWE2-EC7-33 update (2026-09-19) - `0045F140`

`0045F140` (**1,213 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 983 B, a wrong literal in the batch-33 append — the body is 1,213 B per the function list*) is the same shape - `004309C0`/`00430B90`/`00861F14`/`0036A190`/`002F31C0`/`0046F4B0`/`0046D0C0`. Interior anchor `0045F184` (a `00430B90` call).

## SWE2-EC7-33 update (2026-09-19) - `0045E3C0`

`0045E3C0` (**1,213 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 931 B, a wrong literal in the batch-33 append — the body is 1,213 B per the function list*) is the same shape - `004309C0`/`00430B90`/`0044B960`/`004314E0`/`0042FDB0`/`0026EE00`/`0039ADE0`. Interior anchor `0045E404` (a `00430B90` call).

## SWE2-EC7-35 update (2026-09-19) - `00522AB0`

`00522AB0` (712 B) is an element-type dispatch body - `01CEBBA8` rdata, `003D8E50`/`003A6E60` triples plus `00542060`/`00541E00`/`00523380`/`003A3E20`/`002F2D60`. Interior anchor `00522AB9` (an `003D8E50` call).

## SWE2-EC7-37 update (2026-09-19) - `003ED8A0`

`003ED8A0` (552 B) is the effect-file data parse - `02096D30`/`02096887`/`02096D34` (the effect camera), `003A9510`/`003A7CB0`/`003A75B0`/`0039D430`/`003CC0F0`/`003829D0`/`003A98D0`. Interior anchor `003ED909` (a `003A9510` call).

## SWE2-EC7-37 update (2026-09-19) - `004352C0`

`004352C0` (537 B) is an element-record fill - `0020E600` 22-times/`003697F0` 11-times/`0020E620` 11-times fan-out, the `0020E600`/`0020E620` image-pointer pair family. Interior anchor `004352D9` (an `0020E600` call).

## SWE2-EC7-39 update (2026-09-19) - `0057A040`

`0057A040` (432 B) is an effect-element body - `01CEBB60`/`01F44830`/`0209AC30`, `002465C0`/`0055F730` pairs plus `00203170`/`00561CA0`/`00561D30`/`0024E3F0`/`00202D70`. Interior anchor `0057A088` (a `00203170` call).

## SWE2-EC7-40 update (2026-09-19) - `003A8390`

`003A8390` (373 B) is an effect-element body - `01DFE0B4`/`02EBEF80`/`02EBEF88`, `003697F0` pair plus `001EDDA0`/`0043EF40`/`003A92D0`/`003A8130`. Interior anchor `003A839E` (an `001EDDA0` call).

## SWE2-EC7-40 update (2026-09-19) - `00538EB0`

`00538EB0` (373 B) is an effect-element sibling - `004304F0` 14-times plus `00430AF0`/`0042FCF0` triples and `00500470`/`00431770`. Interior anchor `00538EC9` (a `00500470` call).

## SWE2-EC7-41 update (2026-09-19) - `003A6C30`

`003A6C30` (352 B) is an effect-element body - `01F44830`/`02096B24`/`022C6F28`/`02F97348`, `003A5640`/`00421E20`/`00808C40`. Interior anchor `003A6CB8` (a `003A5640` call).

## SWE2-EC7-43 update (2026-09-19) - `004427D0`

`004427D0` (277 B) is the `0x03` effect-element dispatch body - `01F44830`/`02AEE900`/`02AEE908`, `0026EE00`/`002F1F40`/`0039B620`/`0039C4C0`/`004314E0`/`00808C40`. Interior anchor `00442805` (a `0026EE00` call).

## SWE2-EC7-43 update (2026-09-19) - `003A40F0`

`003A40F0` (295 B) is an effect-element body - `022C6F28`/`02F97348`, `00250010`/`00265020`/`002E9B80`/`003588B0`/`0036E4B0`/`0036E4E0`/`0036E620`. Interior anchor `003A412E` (a `00250010` call).

## SWE2-EC7-43 update (2026-09-19) - `00538C80`

`00538C80` (291 B) is an effect-element body - `0042FCF0`/`004304F0`/`00430AF0`/`00431770`/`00500470`. Interior anchor `00538C99` (a `0042FCF0` call).

## SWE2-EC7-44 update (2026-09-19) - `003A2900`

`003A2900` (265 B) is a body - `0036DD90`/`0036DDA0` pair. Interior anchor `003A2993` (a `0036DD90` call).

## SWE2-EC7-45 update (2026-09-19) - `00538B80`

`00538B80` (249 B) is an effect-element body - `0042FCF0`/`004304F0`/`00430AF0`/`00431040`/`00431580`/`00500470`. Interior anchor `00538B9E` (a `0042FCF0` call).

## SWE2-EC7-47 update (2026-09-19) - `004354E0`

`004354E0` (219 B) is a body - `0020E620` single call. Interior anchor `004354F2` (the `0020E620` call).

## SWE2-EC7-47 update (2026-09-19) - `003D7CE0`

`003D7CE0` (212 B) is a body - `00181DD0` single call. Interior anchor `003D7D97` (the `00181DD0` call).

## SWE2-EC7-48 update (2026-09-19) - `00500AA0`

`00500AA0` (207 B) is a body - `00183720`/`003697F0`. Interior anchor `00500AC7` (an `00183720` call).

## SWE2-EC7-49 update (2026-09-19) - `00538AB0`

`00538AB0` (196 B) is a body - `0020E620`/`003AA280`/`0042FCF0`/`004304F0`/`00430AF0`/`00500470`. Interior anchor `00538ABF` (a `0020E620` call).

## SWE2-EC7-51 update (2026-09-19) - `00442550`

`00442550` (173 B) is the `0x01` per-type effect arm - `0026EE00`/`002F1F40`/`0039B620`/`0039C550`/`004314E0`. Interior anchor `00442576` (a `0026EE00` call).

## SWE2-EC7-52 update (2026-09-19) - `00541E00`

`00541E00` (593 B) is an element-type dispatch body - `003D8E50` five times plus `00380800`. Interior anchor `00541E22` (a `003D8E50` call).


## SWE2-EC7-52 update (2026-09-19) - `0046F4B0`

`0046F4B0` (1511 B) is an element-type dispatch sibling of `0045F140`'s shape - `0036DD80`/`00861F14` triple plus `022D91E0`/`022D9230` tables. Interior anchor `0046F580` (a `0036DD80` call).

## SWE2-EC7-54 update (2026-09-19) - `003A75B0`

`003A75B0` (312 B) is an effect-file data-parse body - `0020E600`/`00333C00`/`003697F0` plus `02EBEFA8`/`02F97340`. Interior anchor `003A7602` (a `0020E600` call).

## SWE2-EC7-57 update (2026-09-19) - `00503F50`

`00503F50` (171 B) is an effect-element `0x57`-kind body - `0020E600`/`0020E620`/`003697F0`/`003D7F30`. Interior anchor `00503F67` (a `0020E620` call).

## SWE2-EC7-61 update (2026-09-19) - `00542060`

`00542060` (153 B) is an element-type dispatch body - `003D8E50` single call plus `01CEBB70`/`01CEBBA8`. Interior anchor `0054207E` (a `003D8E50` call).

## SWE2-EC7-62 update (2026-09-19) - `00503790`

`00503790` (150 B) is the `0x51`-tag element body - `0020E600`/`0020E620`/`003697F0`. Interior anchor `005037A7` (a `0020E620` call).



## SWE2-EC7-63 update (2026-09-19) - `00503D50`

`00503D50` (144 B) is the `0x56`-tag element body - `0020E600`/`0020E620`/`003697F0`. Interior anchor `00503D62` (a `0020E620` call).



## SWE2-EC7-65 update (2026-09-19) - `0043EAB0`

`0043EAB0` (136 B) is a call-free jump-table leaf - `add r8,r9; jmp r8`, arms *(eighteen - ten listed here; also `00528AB0`, `005291C0`, `0052A0F0`, `0052ADB0`, `0052BF70`, `0052D370`, `0052E3F0` and `0047BDA0`, `0043EAB0`+0x2B..+0x80; the table's 18; 2026-10-02, OPUS)* `jmp 00522290`/`00522A70`/`00523BF0`/`005247C0`/`00524D30`/`00525D10`/`00526970`/`005270D0`/`005C5230`/`00528050`. Interior anchor `0043EAD8` (the `jmp r8` dispatch).



## SWE2-EC7-65 update (2026-09-19) - `00539320`

`00539320` (136 B) is an effect-element shared-row body - `0042FCF0`/`004304F0`/`00430AF0`/`00500470`. Interior anchor `0053932F` (a `00500470` call).



## SWE2-EC7-65 update (2026-09-19) - `00431580`

`00431580` (135 B) is an effect-element body - `0020E600` single call. Interior anchor `00431596` (a `0020E600` call).



## SWE2-EC7-65 update (2026-09-19) - `00561CA0`

`00561CA0` (135 B) is a call-free fixed-point offset - `byte[+0x554]` `movsx` x `r8d`, `[01F2CACC]` `sar`, `cvtdq2ps`/`mulss`/`addss`, `0209AC30`. Interior anchor `00561CC1` (the `byte[+0x554]` load).



## SWE2-EC7-65 update (2026-09-19) - `00561D30`

`00561D30` (135 B) is a call-free fixed-point offset sibling - `byte[+0x555]` field, same `01F2CACC`/`mulss`/`addss` shape. Interior anchor `00561D51` (the `byte[+0x555]` load).



## SWE2-EC7-66 update (2026-09-19) - `0043ED30`

`0043ED30` (133 B) is a call-free jump-table leaf - `jmp rdx`, arms `00522300`/`00522D80`/`00523D30`/`00524A50`/`00524E30`/`00526080`/`00526A10`/`005271D0` (unhandled-type arm, `0043EAB0` sibling). Interior anchor `0043ED58` (the `jmp rdx` dispatch).


## SWE2-EC7-67 update - `003A6FC0`

`003A6FC0` (130 B) is an effect-element body - `00202D70` plus `0209A670`/`0209A71C` (word-index `0x70`-stride record into `[rdx+0x1C0]`, `[rax+rcx*8+2]` offset walk). Interior anchor `003A7029` (a `00202D70` call).

## SWE2-EC7-67 update - `003A92D0`

`003A92D0` (128 B) is the `0x40`-`0xD1` effect-dispatch arm - `002F31C0` single call, tail `004FF360`. Interior anchor `003A9326` (a `002F31C0` call).

## SWE2-EC7-67 update - `00504170`

`00504170` (128 B) is an effect-element body - `0020E620` x3/`0020E600` x2/`003697F0`. Interior anchor `00504187` (a `0020E620` call).

## SWE2-EC7-77 update (2026-09-20) - `0024E460` capability-word range check measured

`0024E460` (79 B) is the predicate the effect dispatchers call:
`00862C40(&a, &b)` fills two stack slots; only when `a == 0` and
`02F97340` is a `byte==7` record does the range test run -
`(word[rec+4] - 0x240) <= 0x133` returns 1. Every other shape returns
0, so it is a feature check on the `02F97340` object, not a flag read.
Interior anchor `0024E46E` (the `00862C40` call).

## SWE2-EC7-82 update (2026-09-20) - `0046EF10` recursive child dispatch measured

`0046EF10` (179 B) is the sub-object walker the dispatch callers
run: `byte[rdx+0x283] >= 2` with a live `word[+0x286]` resolves
`003A8240(word[rsi+8] | r8d<<8, word[+0x286])`, and a null resolve
runs `003A8020` with `movsx byte[+0x10]`; then the eight
`word[rbx+0x288+i*2]` slots each index the `01E97F10` vtable pointer
array (`[[rax] + id*8]`) and recurse into `0046EF10` - the element's
per-child fan-out.
Interior anchor `0046EF53` (the `003A8240` resolve).

## SWE2-EC7-83 update (2026-09-20) - `00441EA0` + `0043F2B0` measured

`00441EA0` (57 B) is the kind-dependent word fetch the dispatch
callers run: `[rcx+0x130]` then `[+0x18]` must both be live, and on
`byte[+0x283] > 1` kind 7 returns `word[rdx+0x204]`, all others
`word[rax+0x286]` - 0 on every dead path.
Interior anchor `00441ECE` (the `+0x286` fetch arm).

`0043F2B0` (411 B, stack-cookie) is the element validation pass:
`rbx = [01F85340]+0x2D0` unless `byte == 0xFF` swaps to
`[rcx+0x100]+0x2B4`; `byte-1` kind 0/1 builds the `01EB8A40`/`01EB9EB0`
constants frame and runs `0039AF70` -> `00398F90` -> `002F1D90`,
comparing the result against `[rbx+4]`/`[rbx+8]` (kind 0 wants
`low < x <= high`, kind 1 the outside band); `byte[+1] & 1` then runs
`0039B550` -> `00399600` and bounds both `word[+0x40]`/`word[+0x42]`
into `[0x6000, 0xA000]`. Returns 1 only when every armed check passes.
Interior anchor `0043F326` (the `0039AF70` call).

## SWE2-EC7-87 update (2026-09-20) - `003E5600` vec4-out build measured

`003E5600` (146 B) is the 16-byte out-record the dispatch callers
run: when `[rcx+0x400]` is live the `word[+2]`-relative record at
`+0xD4` supplies the first three dwords; a dead record zeroes
them; `[rdx+0xC]` always takes 1.0f. The body then runs
`003E5FA0(rcx, 0, &stack)` and `0046D0C0(rdx, &stack, rdx)` to
commit - all under a stack cookie.
Interior anchor `003E566A` (the `003E5FA0` call).

## SWE2-EC7-90 update (2026-09-20) - `003B15C0` + `003B0220` + `003A8F80` measured

`003B15C0` (239 B) is the pointer-keyed removal the dispatch
callers run: the `02EBE5E0` table is scanned for `qword[+0x10]`
matching `rcx`; a same-key sibling in state 5/6 with a live `+8`
releases through `0024EE60`, otherwise `0024F410(+8)` runs; the
tail then `movups`-compacts the table and clears `02EBEBB0`.
Interior anchor `003B1605` (the matched arm).

`003B0220` (119 B) is the sibling removal over `02EBEC08`: the
keyed slot whose `+8` pointer matches `rcx` is deleted by a
`rep movsq` shift over the 36 0x18-stride entries and
`02EBEF48` is cleared.
Interior anchor `003B024A` (the matched arm).

`003A8F80` (62 B) is the keyed chain find the dispatch callers
run: the `[02EBEF88+8]` list is walked for a node with
`dword[+0x1C] == ecx`, `byte[+0x1A] == dl` and
`byte[+0x1B] == r8b` - returning the node or 0.
Interior anchor `003A8FB1` (the matched arm).

## SWE2-EC7-93 update (2026-09-20) - `0036E620` + `0036E4B0` measured

`0036E620` (22 B) is the 64-entry dword lookup `003A40F0` calls:
`ecx <= 0x3F` indexes `020C9FE0` by dword, anything larger answers 0.
Interior anchor `0036E62F` (the indexed load).

`0036E4B0` (22 B) is the sibling table at `020C9A60`: same `ecx <=
0x3F` bound, same dword index, same 0 on overflow - a second constant
table consulted by the same dispatch callers.
Interior anchor `0036E4BF` (the indexed load).

## SWE2-EC7-99 update (2026-09-20) - `002D7D90` measured

`002D7D90` (106 B) is the slot install `0024D370` calls:
`00182B20` resolves `rdx` first, its result feeds
`002D7E30`'s notify, then the 48-stride `0209F6B0` entry
for index `ecx` takes `rdi` at `+0x10`, `r8d` at `+0x1C`
and `r9d` at `+0x20` - the three-field publish a display
slot receives.
Interior anchor `002D7DEF` (the `+0x10` pointer store).

## SWE2-EC7-110 update (2026-09-20) - `001DB840` measured

`001DB840` (502 B) is the
bucketed effect-record composer
`003A2F70`, `003A33B0`,
`003A34D0` and `003A35E0` run.
`0016D6A0(1)` takes the
allocator lock, `001A1470(
01F7F4C0, 0x640)` allocates,
and `001DB220` constructs;
the pointer parks at `[rsi +
8]`. `0024D140(&rsp58)`
produces the float stored to
`[+0x634]`, `byte[+0x630]`
latches `eax != 0`, and
`[+8]`/`[+0x10]` take the
incoming dword/qword. Globals
`01F82D08` / `01F82D0C` stage
`r14d`/`ebp` for the first
16-byte insert: the bucket
index is `dword[+0x1C] mod
dword[+0x18]` (hard-bounded
`cmp eax, 0x40` + null-write
trap), an empty bucket gets
`dword[+0x18] * 16` bytes from
`001A1470` plus an
`0016D6A0` unlock, and the
`movups` lands at
`bucket[remainder * 16]`
before `dword[+0x1C]++`. The
`01DFD038`/`01DFD040` pair
(`r15` staged) drives an
identical second insert, then
`001DB340(rbx)` runs twice
(the second only when the
`[rsp + 0x80]` qword is live),
`002105C0()` answers
`byte[+0x638]`, and the tail
`001FB840(rsi)` submits.
Interior anchor `001DB8F9`
(the `div` bucket-index fold).

`001DB7E0` (86 B) is the
alloc-and-construct kernel
`00540C70` and `00540DB0`
run: `0016D6A0(1)` locks,
`001A1470(01F7F4C0, 0x640)`
allocates the same 0x640
record, `001DB220` constructs
when the allocation lands, and
`[rdi + 8]` receives the
result either way - the
no-compose sibling of
`001DB840`.
Interior anchor `001DB7FE`
(the `mov edx, 0x640` size
constant).

## SWE2-EC7-111 update (2026-09-20) - `0019C5A0` measured

`0019C5A0` (47 B) is the
locked alloc `00540C70` and
`00540DB0` run beside
`001DB7E0`:
`001A1470(01F7F4C0, ecx)`
takes the size in `ecx`, then
`0016D6A0` on the same
allocator releases the lock
and the raw block returns -
the allocate-half of the
0x640 record pair the effect
dispatchers build on.
Interior anchor `0019C5AF`
(the `001A1470` call).

## SWE2-EC7-113 update (2026-09-21) - `00862BF0` measured

`00862BF0` (14 B) is the
global field getter
`0024D370` and `003A3740`
run: it loads the object at
`01F7F4D8` and returns
`dword[object + 0x94]` -
two instructions, call-free.
Interior anchor `00862BF7`
(the `+0x94` read).

## SWE2-EC7-121 update (2026-09-21) - `0062C300` measured

`0062C300` (90 B) is the
slot-claim validator
`00604750` and `006515C0`
call: `edx` must fall
below `max(1, [+0x18] &
0x7FFFFFFF)` else it
returns 3; the `[+0x20]`
qword-pair table's
`edx * 2` slot must be
non-null else it returns
`0x15`; on success it sets
`slot+8 = 1` and returns
0.
Interior anchor `0062C34F`
(the `slot+8` store).

## SWE2-EC7-122 update (2026-09-21) - `00625EC0` measured

`00625EC0` (8 B) is the
`[+0x48] != 0` predicate
its eight callers -
`005D14C0`, `005DD5E0`,
`005F01B0`, `005FE200`,
`00604750`, `006097B0`,
`006515C0`, `0065D310` -
run before touching the
slot table; two
instructions, `cmp` +
`setne`.
Interior anchor `00625EC4`
(the `setne`).

## SWE2-EC7-123 update (2026-09-21) - `0061D960` measured

`0061D960` (85 B) is the
populate-and-ready body that
raises the `+0x48` flag
`00625EC0` tests: when the
`+0x20` list (count `+0x18`
under `btr 0x1f`, inline
slot else heap) is empty it
runs `0061F070` with the
`[rbx]` argument first, then
sets `+0x48 = 1` either way.
Its callers `00604750`,
`006097B0`, `006515C0` run
it before the slot-table
walks - the flag is the
"table populated" mark.
Interior anchor `0061D994`
(the `0061F070` call).

## SWE2-EC7-124 update (2026-09-21) - `0061F070` measured

`0061F070` (400 B) is the
populate `0061D960` runs
before raising `+0x48`:
`[rcx] = (edx + 0xF) & ~0xF`
slots; the shared device
accessor's `+0x108` device;
any old `+0x10`
array is freed with
`00584730`; `0017D260`
allocates `count*0x10`; then
per slot `vtable[+0x18]`
creates a buffer,
`vtable[+0x50]` reads its
desc into `+0x30`,
`0061C550` names it
`"PConstantBuffer"`
(`00D3B118`), and `+8` is
cleared. A negative create
exits 9.
Interior anchor `0061F192`
(the `vtable[+0x18]`
create in the loop).

## SWE2-EC7-125 update (2026-09-21) - the matrix inverse, the pump-submit, and the record copies measured

`006090B0` (1,617 B) is the
SSE 4x4 matrix inverse the
dispatch path shares: it
computes the full cofactor
expansion in xmm registers
(rows of `movups`/`movaps`,
the cross terms built with
`mulss`/`addss`/`subss`),
forms the determinant in
`xmm2`, loads `1.0f` from
`01CEBBA8` into `xmm1`, and
divides at `0060934C` to
scale the adjugate. Five
callers - `00602EA0`,
`00604750`, `006515C0`,
`00652A90`, `0065D720` -
reach it for effect-space
transforms. Interior anchor
`0060934C` (the reciprocal
divide).

`006097B0` (187 B) is the
pump-then-submit wrapper
`00604750` runs per record:
`00625EC0` tests the slot's
ready predicate; when not
ready `0061D960` populates
and raises `+0x48`; the next
record index is computed,
then the body waits while
the record's `+0xC` counter
stays positive by repeatedly
calling `005CCB80`, calls
`00626060`, and stamps
`+8 = 1` on success.
Interior anchor `00609835`
(the `005CCB80` wait).

`005DF3E0` (1,072 B) is the
big effect-record copy
`00604750` uses: roughly
0x594 bytes moved
field-by-field - the flat
0x100-byte head as dwords,
a qword and two dwords at
`+0x100`..`+0x10C`, the
`+0x110`..`+0x1E0` and
`+0x1E0`..`+0x2A0` subrecords
(the latter through
`005DEC50`), then the tail
dwords `+0x560`..`+0x590`
and byte `+0x574`. Interior anchor `005DF76C` (the
`005DEC50` call).

`005DEC50` (1,924 B) is the
sub-record copy `005DF3E0`
and `006084B0` share: the
same dword-by-dword pattern
covering a ~0x190-byte
element header block, with
no calls of its own until
the tail - a pure structure
clone the copy path relies
on for the nested piece.
Interior anchor `005DED05`
(a mid-block dword store).

## SWE2-EC7-126 update (2026-09-21) - the element-list reset and the indexed element fetch measured

`0062B7B0` (183 B) is the
list reset the teardown
(`005FE200`, `00616420`)
and record paths share:
`0062B020` runs first,
`+0x48` is zeroed, then each
of the `[rbx+0x18]`-count
(masked) entries in the
inline-or-heap 0x10-stride
array at `+0x20` gets its
non-null pointer's
`vtable[+0x10]` called and
the slot cleared; finally
`+0x10` is freed through
`00584730` and zeroed.
Returns 0. Interior anchor
`0062B821` (the per-entry
`vtable[+0x10]` call).

`00626060` (188 B) is the
indexed element fetch
`006097B0` calls after the
wait: `edx` past the
`+0x18`-masked count exits
3; the inline-or-heap array
at `+0x20` must hold a
non-null entry at `idx*16`
or it exits 0x15; when
`+0x3C` bit 16 is clear it
once-logs `"Performance..."`
(`00D55300`) through
`005CDAA0`; the result
`[r8] = +0x10 + idx * [rbx]`
is the element's computed
address. Interior anchor
`006260F9` (the once-log
call).

`0054FE00` (485 B) is a `00538910` sub-setup handler (`+0x44`-keyed): after the `00500470` prelude, three `0xF0`-stride slots from `+0xD0` each take `0042FCF0` three times (fields `-0x50`, `+0`, `+0x50` of the slot), then a `00430AF0` ladder runs `+0x350`, `+0x390`, `+0x3D0`, `+0x410` and onward — one type's grouped field-init ladder.

Interior anchor `0054FE30` (function `0054FE00`).

`0054FFF0` (528 B) is the sibling `00538910` handler: `00500470` then a flat `0042FCF0`/`004304F0`/`00430AF0` ladder across `+0x80`, `+0x90`, `+0xE0`, `+0x130`, `+0x180`, `+0x190`, `+0x1D0`, `+0x1E0`, `+0x220`, `+0x230` — every fixed field initialized in order, no slot loop.

Interior anchor `0055004A` (function `0054FFF0`).

`00550200` (500 B) is the third sibling `00538910` handler: the same `00500470` prelude and the same `0042FCF0`/`004304F0`/`00430AF0` ladder over `+0x80` through `+0x230` — the shared field-init shape with its own field set.

Interior anchor `0055021D` (function `00550200`).

`0054EA70` (206 B) is a `00538910` sub-setup handler (`+0x44`-keyed): `00500470` then a flat `0042FCF0`/`004304F0`/`00430AF0` ladder over `+0x80`, `+0xD0`, `+0x120`, `+0x170`, `+0x1C0`, `+0x200`, `+0x210`, `+0x250`, `+0x290` and `+0x380`-`+0x3BC`, closed by `00431770`.

Interior anchor `0054EAD3` (function `0054EA70`).

`0054EB40` (455 B) is a `00538910` sub-setup handler: `00500470`, a 3-iteration `0xF0`-stride slot loop of three `0042FCF0` each (`rbx-0x50`/`rbx`/`rbx+0x50` from `+0x50`), a flat `004304F0` block over `+0x440`-`+0x500`, a `0xF0`-stride `00431770` loop, and `00430AF0` on `+0x7C0`/`+0x8C0` — the batch's two-loop sibling.

Interior anchor `0054EC26` (function `0054EB40`).

`0054ED10` (349 B) is a `00538910` sub-setup handler: `00500470`, the same 3-iteration `0xF0`-slot `0042FCF0` loop, then a 4-iteration `0x80`-stride loop of three `004304F0` each (`rdi-0x40`/`rdi`/`rdi+0x40`), and `00431770` on `+0x890` — no `00430AF0` at all.

Interior anchor `0054EDBE` (function `0054ED10`).

`0054EED0` (401 B) is a `00538910` sub-setup handler: `00500470`, the 3-iteration `0xF0`-slot `0042FCF0` loop from `+0xD0`, then a flat `00430AF0`/`004304F0` ladder over `+0x350`, `+0x390`, `+0x3D0`, `+0x410`, `+0x450`-`+0x690`, `+0x780`, `+0x870`, `+0x960` and `+0xA60`, closed by `00431770`.

Interior anchor `0054EFA6` (function `0054EED0`).

`0054F070` (318 B) is a `00538910` sub-setup handler: `00500470` then a flat ladder — `0042FCF0` on `+0x80`, a `004304F0` run over `+0x90`-`+0x120` and `+0x250`-`+0x300`, `00430AF0` on `+0x340`-`+0x410` — closed by `00431770`.

Interior anchor `0054F10B` (function `0054F070`).

`0054F1B0` (192 B) is a `00538910` sub-setup handler: `00500470` then a short flat ladder — `0042FCF0`/`004304F0` over `+0x80`, `+0x90`, `+0xD0`-`+0x130`, `+0x180`, `+0x1D0` and `+0x2CC`, `00430AF0` once, `00431770` closing.

Interior anchor `0054F213` (function `0054F1B0`).

`0054F270` (212 B) is a `00538910` sub-setup handler: `00500470`, fixed `0042FCF0`/`004304F0`/`00430AF0` on `+0x80`-`+0xF0` and `+0x140`/`+0x1C0`, then an 8-iteration loop of `004304F0(rbx) + 00430AF0(rdi)` with `rbx += 0x10` and `rdi += 0x40` — the counted pair ladder — and `00431770` on `+0x3C0`.

Interior anchor `0054F2C7` (function `0054F270`).

`0054F350` (457 B) is a `00538910` sub-setup handler: `00500470`, the 3-iteration `0xF0`-stride slot loop of three `0042FCF0` each from `+0xD0` (the `0054FE00` shape), then a long flat `00430AF0` ladder over `+0x350`, `+0x390`, `+0x3D0`, `+0x410` and onward through `+0xB70`, closed by `00431770`.

Interior anchor `0054F442` (function `0054F350`).

`0054F520` (472 B) is a `00538910` sub-setup handler: `00500470` then a flat ladder — `0042FCF0` on `+0x80`, `+0xD0`, `+0x120`, a `004304F0`/`00430AF0` mix over `+0x170`-`+0x470`, `+0x560`, `+0x650`, `+0x740` and `+0x85C`, with `00431770` four times inside the tail.

Interior anchor `0054F60F` (function `0054F520`).

`0054F700` (192 B) is a `00538910` sub-setup handler: `00500470` then a short flat ladder — `004304F0`/`00430AF0` over `+0x80`, `+0x90`, `+0xD0`, `+0x110`-`+0x200` and `+0x30C`, `00431770` closing — the smallest sibling alongside `0054F1B0`.

Interior anchor `0054F763` (function `0054F700`).

`0054F7C0` (486 B) is a `00538910` sub-setup handler: `00500470` then a flat ladder — `0042FCF0` on `+0x80`, `+0xC0`, `+0x100`, `004304F0`/`00430AF0` over `+0x140`-`+0x550`, `+0x640`, `+0x730` and `+0x890`, `00431770` three times in the tail.

Interior anchor `0054F8AF` (function `0054F7C0`).

`0054F9B0` (556 B) is a `00538910` sub-setup handler: `00500470` then the longest flat ladder — `0042FCF0` on `+0x80`, `+0xC0`, `+0x100`, `004304F0`/`00430AF0` over `+0x140`-`+0x570`, `+0x660`, `+0x750` and `+0x8A0`, `00431770` three times — the `0054F7C0` shape stretched one field row further.

Interior anchor `0054FAC9` (function `0054F9B0`).

`0054FBE0` (542 B) is a `00538910` sub-setup handler: `00500470` then a flat ladder — `0042FCF0` on `+0x80`, `+0x90`, `+0xD0`-`+0x120`, `004304F0` over `+0x170`-`+0x4F0`, `00430AF0` once, `00431770` on `+0x500`, `+0x5F0` and `+0x6E0`, returning `rdi+0x7F4`.

Interior anchor `0054FCEB` (function `0054FBE0`).

`00524E30` (2966 B) is a `0043ED30` sub-walk arm (`+0` - `0x42` keyed): publishes `02F8F2D0` into `02CA8528`, gates on `byte[rcx]`, reads `dword[+0x44]`, then the shared element ladder - `0026EE00` x19, `0042FDB0` x10, `00462260` x9, `00430B90`, `00431830`, `003A3CF0`, `005011A0`, `0020E600` - one type's draw/update body.

Interior anchor `005255C3` (function `00524E30`).

`005271D0` (3026 B) is a `0043ED30` sub-walk arm: same `02F8F2D0` publish and `byte[rcx]`/`+0x44` prologue, the same `0026EE00` x19 / `0042FDB0` x10 / `00462260` x9 ladder with `00430B90`, `00431830`, `003A3CF0` and one `0020E600` - the sibling draw body.

Interior anchor `00527972` (function `005271D0`).

`0052C070` (3790 B) is a `0043ED30` sub-walk arm: the same publish (`02F8F2D0` -> `02CA8A58`, `rcx` -> `02CA8520`, `[rcx+0x20]` -> `02CA8528`), `byte[rcx]` gate, then a `[+0x20]+0xB50` walk through the `0026EE00` x19 / `0042FDB0` x10 / `00462260` x9 ladder plus `00430B90`, `00431830`, `004309C0`, `0024E460`, `00202D70`.

Interior anchor `0052C773` (function `0052C070`).

`0052D920` (2373 B) is a `0043ED30` sub-walk arm: `02F8F2D0` publish, `byte[rcx]` gate, then the shorter `004309C0` x8 ladder with `0026EE00` x4, `0042FDB0` x4, `00202D70` x4, `00462260` x3, `00431830`, `00430B90`, `00203170`, `004314E0`, `0024E640` - the compact sibling.

Interior anchor `0052DD14` (function `0052D920`).

`0052EA90` (2401 B) is a `0043ED30` sub-walk arm: `02F8F2D0` publish, `[rcx+0x20]` held, `+0x230` scratch, the same `004309C0` x8 / `0026EE00` x4 / `0042FDB0` x4 / `00202D70` x4 / `00462260` x3 ladder as `0052D920` with `00203170`/`004314E0`/`0020E600` - the second compact sibling.

Interior anchor `0052EECE` (function `0052EA90`).

`004434D0` (3681 B) is the callee `004453D0` (type-0x04 walk arm) runs per record, also reached by `00447020`/`00447ED0`: `byte[rcx+0x1F0]` counts a loop over `02AEEDB0`-indexed records through `0039B960` x9, `0039AF70`, `00432300`, `00396FD0`, `003CBCA0` and the `00443xxx`/`00444xxx` local arms - the grouped record-emit body.

Interior anchor `004439AE` (function `004434D0`).

`00540FD0` (3548 B) is the integrator `00523380` calls: `byte[+0x38]` set, then a velocity-accumulate ladder - `+0x114 += +0x11C * +0x10`, `+0x110 += +0x118 * +0xC`, `+0x3C += +0x40 * [rcx]`, `+0x54 += +0x5C * +8` and onward over the `+0x100`-`+0x120`/`+0x40`-`+0x60` field pairs, `00861F14` for the scaled tail.

Interior anchor `00541457` (function `00540FD0`).

`00447ED0` (2350 B) is a `002F4020` type arm: `byte[rcx]` gate, `dword[+0x270]`/`+0x274` both required nonzero, `[rcx+0x20]` held, then `00861F08`/`00861F0E` x3, `0026EE00`, `004309C0`, `00431830`, `004314E0`, `00434A70`, `00434900`, `002F1F40` - one element type's gated work arm (also a `004434D0` caller).

Interior anchor `00448314` (function `00447ED0`).

`00462540` (2921 B) is a `002F4020` type arm: `byte[rcx]` gate, `dword[+0x44]` read, then `0026EE00`/`00430B90`/`00462260`/`00431830`/`0042FDB0`/`0053DD10`/`003A3CF0`/`002F1F40`/`0024E640` - the type's update body.

Interior anchor `00462B72` (function `00462540`).

`00463460` (2216 B) is a `002F4020` type arm: `byte[rcx]` gate, then `0026EE00` x6, `00430B90`/`00462260` x4, `00431830`, `0042FDB0`, `003A3CF0`, `002F1F40` and the `004637xx` local arms - the smallest of the three batch siblings.

Interior anchor `00463A0D` (function `00463460`).

`00540F40` (118 B) is the flag-fold helper the `0043ED30`/`002F4020` arms share: `0024E460()` or `003A3D20()` nonzero folds `ebx` to 2, the result is OR'd into `003A2C70()`'s return, and the folded value is passed through to `00540DB0` with the caller's `rcx`/`edx`/`r8d`/`r9d` restored - the family-wide precondition gate.

Interior anchor `00540F80` (function `00540F40`).

`005011A0` (8 B) is the `+0x1CA` accessor the sub-walk arms share: `movsx eax, word[rcx+0x1CA]; ret` - a two-instruction signed-word field read.

Interior anchor `005011A7` (function `005011A0`).

`00501190` (8 B) is the `+0x1C8` sibling accessor: `movsx eax, word[rcx+0x1C8]; ret` - the same two-instruction signed-word read one field down.

Interior anchor `00501197` (function `00501190`).

`00442F30` (1437 B) is the bounded reduce `004453D0`/`00447020`/`00447ED0` run: `r8d` indexes 16-byte records at `022D8F10` (`movsxd` + `shl 4`), `xmm12` accumulates from `xorps`, `0x7FFFFFFFFFFFFFFF` and `0x7F7FFFFF` constants drive an abs/clamp, `0036DD80` x3 and `00861F14` x2 close the pass.

Interior anchor `00443213` (function `00442F30`).

`00399110` (411 B) is the weighted transform kernel the same type arms call: an `r8d`-counted loop over `[rcx+rdx]` 16-byte records, each lane `shufps`-broadcast against the `022D91B0`-`022D91D0` weights with `mulps`/`mulss`/`addss` accumulation into `022D91A0` and `022D9300` - a pure SSE matrix-vector pass, no calls.

Interior anchor `003991D6` (function `00399110`).

`004332B0` (1402 B) is the byte-channel expander `004434D0` and `00444340` share: `dword[rcx]` indexes the `022D8F10` table into `022D8F90`, `[r8]`'s vector stages into `022D8FA0`, `eax` publishes to `[rdx]`, then the `022D8F10` 16-byte block is `psrldq`-unpacked byte-by-byte into the `022D8F91`-`022D8F9B` odd fields - the wide form of the keyed expander.

Interior anchor `00433570` (function `004332B0`).

`00396FD0` (207 B) is the record compactor behind the same arms: `022D8F10`-base indices `r8d`/`r9d` fold through `or`/`dec`, `[rcx]` qwords write into `[rcx-8]` slots while `022D8FA0`/`022D94A0` counters stride - a call-free indexed copy loop.

Interior anchor `00397038` (function `00396FD0`).

`0054D740` (1517 B) is the transform publish `0052EA90` runs: `[rdx+0x130]` and `[rdx+0x140]` stage to `02AEBE80`/`02AEBF20`, the products `+0xC4*+0xCC`, `+0xC8*+0xCC` and `+0xB0*+0x6C` publish to `02AEBE94`-`02AEBE9C`, `[rsi]`'s vector lands at `02AEBEA0`, then `0020E620` x4 and `00861EBA` x2 close the pass.

Interior anchor `0054DACC` (function `0054D740`).

`0054D610` (292 B) is the pair-scan `0052EA90` runs: `dword[rcx+0xA4]` counts the loop, `[rcx+0x190]` heads the record list, `[rdx]+0x27` shifts to a x16 base, and an unrolled-by-two `((n-2)>>1)+1` loop reads `word[rcx]`/`word[rcx+4]` pairs off each `[r10+0x80]` record - a call-free counted scan.

Interior anchor `0054D6A4` (function `0054D610`).

`0054BD40` (292 B) is the same pair-scan in `0052D920`'s layout: `word[rcx+0x52]` counts, `[rcx+0x108]` heads the list, the same `+0x27` x16 base and unrolled-by-two `word` pair reads over `[r10+0x80]` records - identical shape, different field offsets.

Interior anchor `0054BDD4` (function `0054BD40`).

`0054BE70` (1485 B) is the `02AEBE80` publish `0052D920` runs: `[rdx+0xD0]`/`+0xE0` vectors stage to `02AEBE80`/`02AEBF20`, `+0xF4` lands at `02AEBE90`, the `+0xC8*+0xF0`/`+0xCC*+0xF0` products at `02AEBE94`/`98`, then `0020E620` x4 and `00861EBA` x2 close - the `0054D740` sibling with the `+0xF0` scale field.

Interior anchor `0054C1E2` (function `0054BE70`).

`0054B3E0` (2389 B) is the table stage `0052C070` runs: an unrolled 3x `0x80`-stride `movups` loop copies `02AEC4B0` into the `[rbp+0x200]` scratch frame, then `0020E620` runs six times over the staged constants - the arm's coefficient-table load.

Interior anchor `0054B663` (function `0054B3E0`).

`0054B3A0` (64 B) is the offset sum `0052C070` runs: `0x4F0` base plus a 4-slot `0x110`-stride scan where each nonzero `[rcx]` folds `+0x2E0` (first hit `+0x2D0`) into the running offset, `shr eax,4` out - the record-size compute, call-free.

Interior anchor `0054B3BE` (function `0054B3A0`).

`005473A0` (1549 B) is the table stage `005271D0` runs: the same `0x80`-stride `movups` copy shape over `02AE9EE0` with a 2-count, then `0020E620` x3 - the sibling coefficient load.

Interior anchor `00547532` (function `005473A0`).

`00547350` (76 B) is the offset sum `005271D0` runs: `0x40` base, `0x3C` slots at `0x110` stride, each nonzero `[rcx]` folding `+0x2E0`/first-hit `+0x2D0`, `cmovne`-selected then `shr 4` - the `0054B3A0` shape on a wider window.

Interior anchor `00547379` (function `00547350`).

`00544D30` (942 B) is the table stage `00524E30` runs: the same `0x80`-stride `movups` copy shape over `02AE9D50` with a 3-count, then `0020E620` x3 - the third coefficient-load sibling.

Interior anchor `00544E24` (function `00544D30`).

`00544CE0` (68 B) is the offset sum `00524E30` runs: 4 slots at `0x100` stride, nonzero `[rcx]` folding `+0x190`/first-hit `+0x180` into `r9d`, `cmovne` + `shr 4` - the same fold-shape on the `+0x100` layout.

Interior anchor `00544CFF` (function `00544CE0`).

`00541DB0` (79 B) is the offset sum `00522D80` runs: `byte[rcx+0x38]` gates the whole body, then `0x230` base plus a 3-slot `0x50`-stride scan over `+0x140`, nonzero entries folding `+0xC0`/first-hit `+0xB0`, `shr 4` - the fourth fold sibling.

Interior anchor `00541DD8` (function `00541DB0`).

`0053AB10` (52 B) is a `005004C0` `+0x44`-keyed setup handler: `00500470` prelude, one `0042FCF0(rdi+0x80, edx)` field init, returns `rdi+0xE0` - the minimal ladder.

Interior anchor `0053AB1F` (function `0053AB10`).

`0053AA30` (136 B) is a `005004C0` `+0x44`-keyed setup handler: `00500470` prelude, five `00430AF0` inits at `+0x80`/`+0xC0`/`+0x100`/`+0x140`/`+0x1A0` and two `004304F0` at `+0x180`/`+0x190`, returns `rdi+0x250`.

Interior anchor `0053AA77` (function `0053AA30`).

`0053A900` (207 B) is a `005004C0` `+0x44`-keyed setup handler: `00500470` prelude, a 4-iteration `0042FCF0` loop at `0x50` stride from `+0x80`, then a grouped `00430AF0`/`004304F0`/`00431770` loop over `+0x2C0`/`+0x300`/`+0x500` - the looped sibling.

Interior anchor `0053A973` (function `0053A900`).

`00446050` (3792 B) is the workbench emitter `00447020` and `00447ED0` share: `[rdx]`'s four sign-extended dwords stage into `022D8F90`/`022D8FA0`/`022D8FB0`/`022D8FC0`, the `022D8F10` block's bytes scatter through `psrldq` shifts into the `022D8F91`+ stride-2 fields, and five `0036DD80` calls punctuate the block - a call-light staging body over the `022D8Fxx` shared workbench.

Interior anchor `00446826` (function `00446050`).

`00447020` (2062 B) is a `002F4020` type arm: `byte[rcx]` gate plus `dword[+0x268]`/`+0x26C` both required nonzero, `r15 = [rcx+0x20]`, `004314E0(r15+0x30, [rcx+0x44])` publishes its index to `02AEE908`, then the `004309C0`/`0026EE00`/`0042FDB0`/`0039B620` ladder plus the `00446050`/`004434D0`/`00442F30`/`00444340` emit bodies - the grouped work arm.

Interior anchor `004470BB` (function `00447020`).

`005294F0` (2124 B) is the heavy arm `0043ED30` runs: `00861EC0` clears a `0x1B0` frame, `byte[rdi]` and `dword[rdi+0x48] >= 1` gate, `r12 = [rdi+0x20]`, and the `004309C0` x15 ladder runs `[rdi+0x44]`-keyed at `[r12+0x140]`/`+0x150`+ with `0026EE00` x11, `0042FDB0` x10, `00532E80`/`005325D0`/`00533250`/`00540F40` - the default sub-walk's work body.

Interior anchor `0052958E` (function `005294F0`).

`00528150` (1716 B) is the sibling `0043ED30` arm: `byte[rcx]` gate, `rdi = [rcx+0x20]`, `0042FDB0(rdi+0x80, [rcx+0x44])` first, a `+0x1F0` `0x80808080` sentinel routed through `0026EE00`, then `005479B0`/`00547A00`/`0024E2E0`, `00462260` x3, `003A3CF0` x2 and `00540C20` over a `004309C0` x4/`0026EE00` x7 ladder - the paired default-arm body.

Interior anchor `005281B9` (function `00528150`).

`0045DD10` (1709 B) is a `002F4020` type arm seeding `02AE8940`: `byte[rcx]` gate, `rsi = [rcx+0x20]`, `02AE8940`/`02AE8950` xmmwords zeroed and `02AE894C`/`02AE895C` set to 1.0f, `004314E0(rsi+0x5A0)` clamped `<= 0x80` publishes to `02AE8960`, `004314E0(rsi+0x5B0)` next, then the `004309C0` x13/`0026EE00`/`0042FDB0` ladder with `00399600`/`0039A9B0`/`003A34D0` - the `02AE89xx`-global arm.

Interior anchor `0045DD8F` (function `0045DD10`).

`00460170` (1607 B) is a `002F4020` type arm publishing to `02CA5EE0`: `rcx` lands at `02CA5EE0`, `[rcx+0x20]` at `02CA5EE8`, `02AEC660` at `02CA5EF0`, `02CA5F14`/`02CA5F78` zeroed, then `004309C0` x7 keyed by `[rcx+0x44]` at `[rcx+0x20]+0x170`/`+0x180`/`+0x190` stores floats into `[02CA5EF0]+0x40`/`+0x44`+ - the accumulating arm.

Interior anchor `004601CD` (function `00460170`).

`004595C0` (1542 B) is a `002F4020` mode-switch arm: `byte[rcx]` gate, `[rcx+0x250]`..`+0x280` copied to the frame, and `byte[rbx+0x4A] >> 2 & 7` selects the variant - `00434A70`, `00397910` x2, `0039B960` x4 or `00394DA0` - over a `004309C0` x4/`0026EE00`/`0042FDB0` ladder with `0020E600` x5 and `003A33B0` x2 - the keyed-variant arm.

Interior anchor `00459645` (function `004595C0`).

`003A33B0` (280 B) is the shared record allocator the `0045xxxx`/`00460170` type arms all call: `word[02F8F2C6]` counts the `0x28`-stride slots at `[02F8F2F8]`, the count bumps and the fresh slot is zeroed, `ecx & 0xFFFFFF` lands at `+8`, a `02AEE910` nibble shifts into `+0xB`, `+0xC` = 8, then `0024E460` and a `02AEF418`/`02AEF41C` flag fold into `+0x20` before `0020E680` and `001DB840` run against the `01EFAC20` table indexed by `02AEE900` - the arms' one entry point for stamping an element record.

Interior anchor `003A341C` (function `003A33B0`).

`00533250` (2251 B) is the counted emit stage `005294F0` runs: `inc [r8]` ticks the pass counter, a 3x `0x80`-stride `movups` loop stages `02AECAD0` into the frame, a `r8d < eax` counted walk runs the body, and `0020E620` x3 plus `00462260` x9 close - the coefficient-table load's emit half.

Interior anchor `00533843` (function `00533250`).

`005325D0` (2219 B) is the sibling emit stage `005294F0` runs: identical shape - `inc [r8]`, the 3x `0x80`-stride `movups` stage over `02AEBBC0`, the counted walk, `0020E620` x3 and `00462260` x9 - the paired table on the second constant block.

Interior anchor `00532BA3` (function `005325D0`).

`00523D30` (1511 B) is a `0043ED30` sub-walk arm: `002F1F40` prelude, then `0026EE00` x10 and `0042FDB0` x10 with `00462260` x10 over the `004309C0` x5/`004314E0`/`00431830` x2 ladder, `00543940`/`005439D0`/`00202B70`/`00540F40` inside - the default arm's mid-weight sibling.

Interior anchor `00523DA9` (function `00523D30`).

`00456F30` (1393 B) is a `002F4020` type arm: `byte[rcx]` gate, `byte[rdi+0x384] & 6` test, `byte[rdi+0x4A]` keyed `00434A70`/`00434900`/`00398030`/`0039B620`/`0039B550`/`003970A0`/`00397910` ladder with `004309C0` x4, `0026EE00` x3, `0042FDB0` x2, `0020E600` x4, `003A33B0` x2 (the shared allocator) and `004574B0` - the flag-gated variant arm.

Interior anchor `00456FC3` (function `00456F30`).

`0052B080` (1346 B) is a `0043ED30` sub-walk arm: `byte[rcx]` gate, `002F1F40` prelude, `0026EE00`/`0042FDB0`/`00462260` x10 triples over the `004314E0`/`00434A70`/`00434900`/`00398030`/`0039B620`/`0039B550` ladder with `0054A980`/`0054AA90`/`00540F40` - the `00523D30` shape on the second arm.

Interior anchor `0052B10E` (function `0052B080`).

`0052A360` (1330 B) is a `0043ED30` sub-walk arm: `byte[rcx]` gate and the same `0026EE00`/`0042FDB0`/`00462260` x10 triple ladder, with `00547D80`/`005480E0`/`00540F40` as its local bodies - the third sibling of the default-arm family.

Interior anchor `0052A3E0` (function `0052A360`).

`00522300` (1268 B) is a `0043ED30` sub-walk arm: `byte[rcx]` gate, `0042FDB0` x5 and `0026EE00` x6 up front, then `00462260` x4, `00430B90` x3, `004309C0` x3, `004314E0`/`00431830` x3, `0020E600` and `003A3010` - the `0042FDB0`-led variant.

Interior anchor `0052233F` (function `00522300`).

`0045D2F0` (1235 B) is a `002F4020` type arm: `byte[rcx]` gate, `004314E0` x3 first, `byte[rdi+0x49]` keyed, `00430B90`/`0042FDB0` x2/`0026EE00` x5, then the `00434A70`/`00434900`/`00398030`/`0039B620`/`0039B550`/`003970A0`/`00397910` ladder with `00399600`, `003A34D0` x2, `0039A9B0` and `003A35E0` - the `004314E0`-led variant arm.

Interior anchor `0045D331` (function `0045D2F0`).

`003A3010` (385 B) is the tagged packet emitter the `0044D4A0`/`00453150`/`00460BC0`/`00522300` arms share: the `02F8F2D0` arena cursor is `& ~0xF` aligned and bound-checked against `02F8F2D8`, the record takes tag word 3 at `+0`/`+0xC`, `+0x14 &= 0x3FFF | 0x20000000`, `+0x10 = 0x8001`, bytes `+3 = 0x10`/`+0xF = 0x50`, `+0x18 = 0xEE` and `+0x53 = 0x30`, `(edx & 0xF)`-adjusted `00861EBA` copies the payload in, `0020E620` on `rbx+0x60` lands the result at `+0x54`, then `02F8F2D0` advances by the aligned span - the emit half of the frame's packet arena.

Interior anchor `003A3150` (function `003A3010`).

`005480E0` (2334 B) is the row-stage and emit body `0052A360` runs: `inc [r8]` ticks the pass counter, the `[rdx+0xB0]`..`[+0x140]` movaps rows stage into `02AE8670`..`02AE8730`, and the tail writes the `{+3 = 0x10, +0xC = 0x404, +0xF = 1}` record with `0020E620` landing `+4` - the constant-table staging arm's emit close.

Interior anchor `005489C4` (function `005480E0`).

`0054AA90` (1614 B) is the resolve-and-stage body `0052B080` runs: `0020E600` resolves `[rdx+0x148]`'s head dword and `[+8]` before `inc [rbx]`, the `[rsi+0x90]`.. rows stage into `02AECD70`.., and the same `{+3 = 0x10, +0xC = 0x404, +0xF = 1}` record closes through `0020E620` - the resolved variant of the staging arm.

Interior anchor `0054B0A3` (function `0054AA90`).

`004574B0` (1219 B) is the `00456F30` type arm's worker: `byte[rcx]` gate, `[rcx+0x250]`..`[+0x280]` rows staged to the frame, `([rdi+0x4A] >> 2) & 7` selects the arm, then the `00434A70`/`00434900`/`00398030`/`0039B620`/`0039B550`/`003970A0`/`00397910` ladder with `004309C0` x4, `0042FDB0` x2, `004314E0` x2, `0026EE00` x3, `0020E600` x2, `003A33B0` and the cookie check - the mode-decoded ladder body under the flag-gated arm.

Interior anchor `00457536` (function `004574B0`).

`005439D0` (1186 B) is the tile-copy body `00523D30` runs: a 3-iteration `0x80`-stride `movups` loop stages `02AEB0F0` into the frame (`edi = 3` bound), `0020E620` x3 resolves, and the `{+3 = 0x10, +0xC = 0x404, +0xF = 1}` record closes - the coefficient-table staging arm under the default sub-walk.

Interior anchor `00543E27` (function `005439D0`).

`0045BFB0` (1176 B) is a `002F4020` type arm's worker: `byte[rcx]` gate, `00430B90` prelude, `004309C0` x2/`0042FDB0` x2/`004314E0` x2 with `0026EE00` x5 and `002F1F40`, then the `00434A70`/`00434900`/`00398030`/`0039B620`/`0039B550`/`003970A0`/`00397910` ladder with `00399600`, `003A34D0` x2, `0039A9B0`, `003A35E0` and the cookie check - the `0042FDB0`-weighted ladder sibling.

Interior anchor `0045C24F` (function `0045BFB0`).

`0044DD00` (1106 B) is a `002F4020` type arm's worker: `byte[rcx]` gate, the `0044E160` early helper, `004314E0` x2/`004309C0`/`002F1F40`/`0026EE00` x2, then the shared `00434A70`/`00434900`/`00398030`/`0039B620`/`0039B550`/`003970A0`/`00397910`/`00399600`/`003A34D0` x2/`0039A9B0`/`003A35E0` ladder with the cookie check - the `0044E160`-keyed sibling.

Interior anchor `0044DD67` (function `0044DD00`).

`0044E530` (1089 B) is a `002F4020` type arm's worker: identical ladder shape, `0044E980` as the early helper - the `0044E980`-keyed sibling of `0044DD00`.

Interior anchor `0044E597` (function `0044E530`).

`0045C980` (1073 B) is a `002F4020` type arm's worker: `byte[rcx]` gate, `004314E0` x3/`004309C0` x3/`0042FDB0` x2/`0026EE00` x5/`002F1F40`, then the shared ladder - the `004309C0`-weighted sibling.

Interior anchor `0045CA54` (function `0045C980`).

`0044CC50` (1071 B) is a `002F4020` type arm's worker: identical ladder shape, `0044D080` as the early helper - the `0044D080`-keyed sibling of `0044DD00`.

Interior anchor `0044CCB7` (function `0044CC50`).

`00450550` (1007 B) is a `002F4020` type arm's worker: `byte[rcx]` gate, `byte[rbx+0x49]` keyed, `byte[rbx+0x25C] & 1` test, `00450940` early helper, `004314E0` x2/`004309C0` x4/`002F1F40`/`0026EE00` x2, then the `00434A70`/`00434900`/`00398030`/`0039B620`/`0039B550`/`003970A0`/`00397910`/`00399600`/`003A34D0` x2/`0039A9B0`/`003A35E0` ladder with the cookie check - the `00450940`-keyed sibling.

Interior anchor `00450817` (function `00450550`).

`00456720` (985 B) is a `002F4020` type arm's worker: `byte[rcx]` gate, `byte[rbx+0x4A]` keyed with `byte[rbx+0x2BD]` read, `0042FDB0` and `0020E600` x4 up front, `003A2F70`/`003A33B0` mid-ladder, then the shared `00434A70`/`00398030`/`0039Bxxx`/`003A34D0` ladder - the resolve-calling sibling.

Interior anchor `004569A3` (function `00456720`).

`00451180` (938 B) is a `002F4020` type arm's worker: `byte[rcx]` gate, `byte[rbx+0x49]` keyed, `byte[rbx+0x244] & 1` test, `00451530` early helper, `004314E0` x2/`004309C0` x3/`002F1F40`/`0026EE00` x2, then the shared ladder - the `00451530`-keyed sibling.

Interior anchor `00451402` (function `00451180`).

`0044D4A0` (926 B) is a `002F4020` type arm's worker: `byte[rcx]` gate, `byte[rdi+0x49]` keyed with `byte[rbp+0x37]` read, `004314E0` x2/`004309C0` x2/`002F1F40`/`0026EE00` x2, the shared ladder, and `003A3010`/`003A2D80` closing - the packet-emitter-calling sibling, one of `003A3010`'s four drivers.

Interior anchor `0044D78A` (function `0044D4A0`).

`0044E980` (974 B) is the early helper `0044E530` calls: `byte[rcx]` gate, `004314E0` x2/`002F1F40`/`0026EE00`, then the full shared `00434A70`/`00434900`/`00398030`/`0039B620`/`0039B550`/`003970A0`/`00397910`/`00399600`/`003A34D0` x2/`0039A9B0`/`003A35E0` ladder with the cookie check - the `0044E530` arm's first stage, ladder-shaped itself.

Interior anchor `0044EC41` (function `0044E980`).

`0044E160` (970 B) is the early helper `0044DD00` calls: identical ladder shape to `0044E980` - the `0044DD00` arm's first stage.

Interior anchor `0044E41D` (function `0044E160`).

`003A2F70` (154 B) is the shared mid-ladder helper eight `0045xxxx` type arms (`00455560`, `004559C0`, `00455DB0`, `00456720`, `0045A220`, `0045A6A0`, `0045AEF0`, `0045B2B0`) call: `ecx`/`edx`/`r8`/`r9` args are marshalled onto the stack for `0020E680`, then `001DB840` runs the second stage - the element arms' two-call field step.

Interior anchor `003A2F94` (function `003A2F70`).

`00450940` (918 B) is the early helper the `00450550` arm calls: `byte[rcx]` gate, then `004314E0` x2/`004309C0` x3/`002F1F40`/`0026EE00` resolve and the shared `00434A70`/`00434900`/`00398030`/`0039B620`/`0039B550`/`003970A0`/`00397910`/`00399600`/`003A34D0` x2/`0039A9B0`/`003A35E0` ladder runs under the cookie check - the `00450550` arm's first stage.

Interior anchor `0045097C` (function `00450940`).

`0044D080` (915 B) is the early helper the `0044CC50` arm calls: `byte[rcx]` gate, `002F1F40`/`0026EE00`/`00434A70`/`00434900`/`00398030`/`004314E0`, then the shared `0039B620`/`0039B550`/`003970A0`/`00397910`/`00399600`/`003A34D0` x2/`0039A9B0`/`003A35E0` ladder with the cookie check - the `0044CC50` arm's first stage.

Interior anchor `0044D202` (function `0044D080`).

`00528B50` (907 B) is the `0043ED30` dispatch arm's worker: `byte[rcx]` gate, `0042FDB0` x3 and `0026EE00` x4/`002F1F40`/`00462260` x2 up front, `004314E0`/`00430B90` x2/`004309C0` x5/`00431830` x2/`0020E600`/`003A34D0` through the middle, cookie-checked - the dispatch table's `0042FDB0`-keyed arm.

Interior anchor `00528B8F` (function `00528B50`).

`00547A00` (889 B) is the sub-arm `00528150` calls: `movups` loads `[r9]`/`[r9+0x10]`/`[r9+0x20]` into the frame, `word[r8-2]` compares the tag, and `0020E620` x3 resolves the record fields - the `00528150` family's vector-loading resolver.

Interior anchor `00547AC2` (function `00547A00`).

`00460BC0` (874 B) is the `002F4020` type arm's worker: `byte[rcx]` gate, `004314E0` x2/`004309C0` x3/`00430B90` x2/`0039AF70`/`00398F90`/`002F1F40`/`0026EE00` x2, `0039B550`/`003A34D0` mid-ladder, and `003A3010`/`003A2D80` closing under the cookie check - the packet-emitter-calling sibling, another of `003A3010`'s drivers.

Interior anchor `00460BFF` (function `00460BC0`).

`00526080` (855 B) is the `0043ED30` dispatch arm's worker: `002F1F40`/`0026EE00` x2/`0042FDB0`/`00462260`/`00431830`/`00430B90`/`00203170`/`00202D70` x2/`004314E0` up front, `00545EF0`/`005466E0`/`0024E460`/`00540DB0` closing, cookie-checked - the dispatch table's `00540DB0`-calling arm.

Interior anchor `005260BF` (function `00526080`).

`00526A10` (844 B) is the `0043ED30` dispatch arm's worker: `0042FDB0` x3, `0026EE00` x4, `002F1F40`, `00462260` x2, `004314E0`, `00430B90`, `004309C0` x6, `00431830` x2, `0020E600` and `003A34D0` under the cookie check - the table's `004309C0`-heavy sibling of `00528B50`.

Interior anchor `00526A4F` (function `00526A10`).

`00451530` (793 B) is the early helper the `00451180` arm calls: `004309C0` x2/`002F1F40`/`0026EE00` resolve, then the shared `00434A70`/`00434900`/`00398030`/`004314E0`/`0039B620`/`0039B550`/`003970A0`/`00397910`/`00399600`/`003A34D0` x2/`0039A9B0`/`003A35E0` ladder with the cookie check - the `00451180` arm's first stage.

Interior anchor `0045159E` (function `00451530`).

`005466E0` (1735 B) is the heavy resolver the `00526080` arm calls: `0020E620` x3 and `0020E600` across 1,735 bytes with `00861EBA` copies - the dispatch family's largest single-record resolve pass.

Interior anchor `00546958` (function `005466E0`).

`00448DE0` (739 B) is the `0x02` type arm the dispatcher `002F3BC0` names third: `002F2D60`, `00449560`, `003A6E60` x5, `0020E600` x6, `00314960` and `001EDDA0` run the element's emit - the type-2 handler's measured body.

Interior anchor `00448DF6` (function `00448DE0`).

`00501950` (122 B) is the owned-pointer teardown the dispatch's three teardown sites `005019D0`/`00502CB0`/`005032D0` call: `byte[+0x40] & 1` skips straight to the clear, otherwise each non-null field `+0x10`/`+0x18`/`+0x28`/`+0x20`/`+0x30` goes through `003697F0`, then all six plus `+0x38` are zeroed and `word[+0x40]` loses bit 0 - the element record's release-all.

Interior anchor `00501976` (function `00501950`).

`00441F10` (606 B) is the additive channel fold `00441B30` calls inside its element loop: `rdx` null-gates, `[rcx+0x100]`'s `byte[+0x2C5]` bit 0x1 opens nine `addss` pairs folding `rdx+0xB0`..`+0xD8` into `rcx+0x90`..`+0xB8` with `+0x9C` forced to 1.0, bit 0x2 opens the `rdx+0x1F8` `mulss`/`addss` triple into `+0xF4`..`+0x108` and further bits open more lanes, then `jmp 0026EE00` finishes - the pose accumulator's per-bit blend.

Interior anchor `00442018` (function `00441F10`).

`0053A3B0` (535 B) is the bank apply `005004C0` calls: `00500470` on `rbp`, `00430AF0` x4 over `+0x80`/`+0xC0`/`+0x100`/`+0x140`, a 3x3 nested loop strides `0042FCF0` over `+0x180` at 0x50, then `+0x450`/`+0x4A0` `0042FCF0`, `+0x4F0` `004304F0`, `+0x500`.. on - the effect record's per-mode sub-apply.

Interior anchor `0053A3CF` (function `0053A3B0`).

`00464F20` (501 B) is the flag copy `002F3BC0` calls: `002F2D60` gates, then `[r9+0x140]`/`+0x141` copy to `[rbx+0x230]`/`+0x231` and `[r9+0x142]`'s two low bits pack into `word[rbx+0x232]` one position apart (`& 0xFFFE`/`& 1`, `>> 1 & 1`/`& 0xFFFD`/`<< 1`) - the element's flag projection.

Interior anchor `00464F29` (function `00464F20`).

`00524A50` (462 B) is the record copier `0043ED30` calls: `002F1F40` packs `[rcx+0x70]` against `rsi = [rcx+0x20]`, `dword[+0x1F0] != 0x80808080` runs `0026EE00` on the scratch block, `0042FDB0(rsi+0x80, [rbx+0x44])` resolves, and a second `0x80808080` sentinel test feeds `00462260`/`00540F40`/`00544590`/`00544A50` - the element's field-copy arm.

Interior anchor `00524A8E` (function `00524A50`).

`0053A1E0` (455 B) is the slot-table init `005004C0` calls: `00500470` gates, then `00430AF0(edx)` runs on the `+0x80`/`+0xC0`/`+0x100`/`+0x140` slots and a 3-iteration `0x50`-stride loop calls `0042FCF0` over `+0x180`, with `004304F0`/`00431770` finishing - the element's batched-slot setup.

Interior anchor `0053A1FF` (function `0053A1E0`).

`00457E10` (452 B) is the enable applier `002F3BC0` calls: `002F2D60` gates, `rbp = [rdi+0x20]`, and `byte[rbp+0x384]` bits 8/0x10 each run `003A6E60(ecx=2)` then write `byte[rdi+0x2AC]` bit 0 - the element's flag-to-bit projection.

Interior anchor `00457E19` (function `00457E10`).

`00457980` (1154 B) is the large update arm `00456EF0`/`00457E10` call: `00430B90` builds from `[rdi+0xD0]` into the stack frame, `movdqa` stores to `[rbx+0x110]`, `byte[rdi+0x49] & 8` writes `022D92E0`, and `003970F0`/`00397910`/`00397ED0`/`00398480`/`00398F90`/`0039ADE0`/`0039AF70`/`003A8950`/`0042FDB0`/`004314E0`/`005002E0`/`002F31C0`/`002F3570`/`002F35C0`/`0026EE00`/`00808C40` run the full element update.

Interior anchor `004579C2` (function `00457980`).

`00544A50` (647 B) is the record clone `00524A50` calls: `ebx = 2` rounds of `0x80`-stride `movups` copy `02AEA270` into `[rsp+0x20]` (a 2x0x80 template), then `0020E600`/`0020E620` resolves work the copy - the element's template-block clone.

Interior anchor `00544BA1` (function `00544A50`).

`0046D950` (448 B) is the call-free angle evaluator `00523380` calls: `[rdx]` components divide by `01CEBC78`, `cvttss2si` + `& 0x7FFF` index the `01F004E0` LUT against `ecx = 0x2000`, `cvtps2pd`/`mulsd`/`addsd` lerp `x*x` into `[r8]`, then `+4`/`*[rdx]`/`+8` finish - the element's table-lookup trigonometry.

Interior anchor `0046D993` (function `0046D950`).

`00461090` (441 B) is the flag compute `002F3BC0` calls: `002F2D60` gates, `rdi = [rbx+0x20]`, `byte[rdi+0x1B4] & 4` gates, `word[rdi+0x1CE] >> 5 & 1` feeds `00376350` into `[rbx+0x294]`, then `00377010`/`003770D0`/`00377100`/`00399600`/`0039B550`/`0044B960`/`00462160`/`001827B0`/`00808C40` run the per-flag arms - the element's flag evaluator.

Interior anchor `004610B0` (function `00461090`).

`00377100` (38 B) is the call-free slot writer `00461090`/`00461270` call: `cl * 0x90` (`r8*9*2*8`) indexes the `02ADBB40` table, `ecx != 0` and `dword[slot] == ecx` guard, then `movups` stores the caller's 16 bytes at `+0x70` - the keyed vector write.

Interior anchor `00377116` (function `00377100`).

`003770D0` (34 B) is the call-free scalar twin of `00377100`: same `cl * 0x90` index into `02ADBB40`, same `ecx != 0 && dword[slot] == ecx` guard, but stores `edx` at `+4` - the keyed scalar write.

Interior anchor `003770E6` (function `003770D0`).

`0045A050` (419 B) is the flag arm `002F3BC0` calls: `002F2D60` gates, `rsi = [rbx+0x20]`, `byte[rsi+0x2A4] & 8` runs `003A6E60(2)` whose `al & 1` merges into bit 0 of `byte[rbx+0x2A4]` (cleared first by `& 0xFE`), `& 0x10` selects the next arm, and `0045AA50`/`0044B960`/`003D8E50`/`003A6E60`/`0020E600` finish - the element's flag propagation.

Interior anchor `0045A059` (function `0045A050`).

`00455390` (419 B) is the sibling flag arm `002F3BC0` calls: identical skeleton to `0045A050` (`002F2D60` gate, `byte[+0x2A4]` bit tests, `003A6E60` merge) but the commit runs `0045B640` instead of `0045AA50` - the paired element-flag evaluator.

Interior anchor `00455399` (function `00455390`).

`0045B640` (1154 B) is the evaluator `00455390` commits to (also called by `0045B260`): `00430B90(&frame, [rcx+0x20] + 0xD0, [rcx+0x44])` computes the element vector, `movdqa` stores it at `[rbx+0x110]`, and `byte[rdi+0x49] & 8` gates a publish that adds `[rbx+0xE0]` into the `022D92E0`/`022D92F0` accumulator block - the element's compute-and-accumulate.

Interior anchor `0045B682` (function `0045B640`).

`0045AA50` (1154 B) is the twin evaluator `0045A050` commits to (also called by `0045A010`): identical skeleton to `0045B640` - same `00430B90` compute into `[rbx+0x110]`, same `byte[rdi+0x49] & 8` publish into `022D92E0` - the paired element evaluator on the sibling flag arm.

Interior anchor `0045AA92` (function `0045AA50`).

`00459420` (403 B) is the third flag arm `002F3BC0` calls: `002F2D60` gates, `rsi = [rbx+0x20]`, `byte[rsi+0x2A7]` bits 1/2/4 each run `003A6E60(2)` whose `al & 1` merges into `byte[rbx+0x2A4]` bits 0/1/2 (`& 0xFE`/`& 0xFD`/`& 0xFB` clears first), and `00459BD0`/`0044B960`/`003D8E50`/`0020E610` commit - the `+0x2A7`-sourced sibling of `0045A050`/`00455390`.

Interior anchor `00459429` (function `00459420`).

`00459BD0` (1086 B) is the third evaluator twin `00459420` commits to (also `004593E0`): identical `00430B90` compute into `[rbx + 0x110]` with the `byte[rdi + 0x49] & 8` publish into `022D92E0`, then a long tail of `004314E0`/`0042FDB0`/`0026EE00`/`0039xxxx`/`005002E0`/`003A8950` - the `+0x2A7`-armed element evaluator.

Interior anchor `00459C14` (function `00459BD0`).

`00442170` (367 B) is the mode dispatch `00441B30` calls: `[rcx + 0x100]`'s `byte[+0x282] <= 8` selects an arm of the `0x4422E0` jump table; each arm zeroes/fills `+0x80`..`+0x9C` (mode 0 writes `+0x9C` = 1.0f) then calls one of `005315B0`/`0052F780`/`00531DB0`/`00530770`/`0052FCA0`/`00530230`/`005318A0`/`00530E40` - the element's eight-way post-pass.

Interior anchor `004421DE` (function `00442170`).

`00530770` (1715 B) is the widest of `00442170`'s eight post-pass arms: `[rcx + 0x100]` record, `cvttss2si` on `xmm1`, three `00430B90` vector computes over `[rsi + 0xB0]`/`[+0x2DC]`/`[+0x31C]`, then the shared `00397910`/`00398030`/`00398480`/`00398F90`/`0039ADE0`/`0039AF70`/`003A2440`/`003A2570`/`003A27C0`/`003A2B20`/`003A6E60`/`003D8E50`/`004309C0`/`0052F560` tail publishing through `022D92E0..F0` - arm 0's full pass.

Interior anchor `005307CC` (function `00530770`).

`0052FCA0` (1421 B) is a `00442170` post-pass arm: same `00430B90` preamble into the shared `0039xxxx`/`003A2xxx`/`0052F560` tail, without `003A6E60`/`003A6E60`/`004314E0` - the leaner variant of arm 0's publish.

Interior anchor `0052FD00` (function `0052FCA0`).

`00530230` (1338 B) is a `00442170` post-pass arm: `00430B90` vector compute then the shared publish tail, omitting `003A2570` and `003A6E60` - a third mode's variant.

Interior anchor `00530290` (function `00530230`).

`00531DB0` (1329 B) is a `00442170` post-pass arm: `00430B90` preamble plus the shared `0039xxxx`/`003A2xxx`/`0052F560` tail - the fourth mode's publish.

Interior anchor `00531E0C` (function `00531DB0`).

`0052F780` (1312 B) is a `00442170` post-pass arm: same `00430B90` + shared-tail shape as the other arms - the fifth mode's publish.

Interior anchor `0052F7D9` (function `0052F780`).

`005318A0` (1288 B) is a `00442170` post-pass arm: `00430B90` preamble, the only arm that also calls `004314E0` alongside `003A6E60` in the shared tail - the sixth mode's publish.

Interior anchor `005318EE` (function `005318A0`).

`005315B0` (740 B) is the leanest `00442170` post-pass arm: `00430B90` then a reduced tail (`00397910`/`00398030`/`00398480`/`0039AF70`/`003A2440`/`003A27C0`/`003A2B20`/`004309C0`/`0052F560` only) - the seventh mode's publish.

Interior anchor `005315F4` (function `005315B0`).

`00431610` (344 B) is the mode fetch `00431770` calls: `byte[rcx + 0xA0] - 1` splits arms 1/2/3; the fall-through arm runs `0020E620` pairs into `[rbx + 0xBC]`/`[+0xC0]`, `byte[+0xA5]` gates `003AA280(0x50)` - the element record's per-mode float pull.

Interior anchor `00431639` (function `00431610`).

`00545EF0` (191 B) is the 0x6A ('j') footprint computer `00526080` runs: call-free - `esi = [rcx+0x10]` rows, `edx = ([rcx+0x1C] + 0x17) << 4` base, then a `r9d = [rcx+0x14]`-wide cell loop adds `0x60` per cell plus, when `[rcx+0x64] & 2`, a 0x16-clamped row product `*16` - the type's allocation size, not its fields.

Interior anchor `00545F57` (function `00545EF0`).

`00539030` (316 B) is the ~~`+0x44 = 0x47`~~ `+0x44 = 0x08` *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type 0x08 here)* creation arm (`005004C0` stub 8): `00500470` prelude, `003AA280`x2, `0042FCF0`x4/`004304F0`x3/`00430AF0`x9 over `+0x80`-`+0x448`.

Interior anchor `0053904D` (function `00539030`).

`00539740` (302 B) is the ~~`+0x44 = 0x52`~~ `+0x44 = 0x89` *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type 0x89 here)* creation arm (`005004C0` stub 19): `00500470` prelude, `003AA280`x2, `0042FCF0`x2/`004304F0`x10/`00430AF0`x3 over `+0x80`-`+0x2E8`.

Interior anchor `0053975D` (function `00539740`).

`00539610` (302 B) is the ~~`+0x44 = 0x51`~~ `+0x44 = 0x88` *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type 0x88 here)* creation arm (`005004C0` stub 18): `00500470` prelude, `0020E620`x2/`003AA280`x2, `0042FCF0`x2/`004304F0`x9/`00430AF0`x3 over `+0x80`-`+0x2C0`.

Interior anchor `0053962D` (function `00539610`).

`00539870` (260 B) is the ~~`+0x44 = 0x53`~~ `+0x44 = 0x8A` *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type 0x8A here)* creation arm (`005004C0` stub 20): `00500470` prelude, `003AA280`x2, `0042FCF0`x2/`004304F0`x7/`00430AF0`x3 over `+0x80`-`+0x2D0`.

Interior anchor `0053988D` (function `00539870`).

`00538DB0` (254 B) is the ~~`+0x44 = 0x44`~~ `+0x44 = 0x05` *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type 0x05 here)* creation arm (`005004C0` stub 5): `00500470` prelude, `0020E620`/`003AA280`/`0042FCF0`/`004304F0`x2/`00430AF0`x3 over `+0x80`-`+0x620`, `00431770` closer, tail-jumps `00538E7E`.

Interior anchor `00538DD7` (function `00538DB0`).

`00539170` (246 B) is the ~~`+0x44 = 0x48`~~ `+0x44 = 0x0A` *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type 0x0A here)* creation arm (`005004C0` stub 9): `00500470` prelude, `0020E620`x2/`003AA280`x2, `0042FCF0`x2/`004304F0`x3/`00430AF0`x5 over `+0x80`-`+0x2C0`.

Interior anchor `0053918D` (function `00539170`).

`005393B0` (232 B) is the ~~`+0x44 = 0x4E`~~ `+0x44 = 0x85` *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type 0x85 here)* creation arm (`005004C0` stub 15): `00500470` prelude, `003AA280`x2, `0042FCF0`x2/`004304F0`x3/`00430AF0`x5 over `+0x80`-`+0x2C8`.

Interior anchor `005393CD` (function `005393B0`).

`00539E90` (225 B) is the ~~`+0x44 = 0x5B`/`0x5C` shared~~ `+0x44 = 0x91`/`0x92` shared *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type 0x91 here)* creation arm (`005004C0` stubs 28 and 29): `00500470` prelude, `0020E620`/`003AA280`/`0042FCF0`/`004304F0`x2/`00430AF0`x3 over `+0x80`-`+0x2C0`, `00431770`, tail-jumps `00539F41`.

Interior anchor `00539EB7` (function `00539E90`).

`00539DA0` (225 B) is the ~~`+0x44 = 0x59`/`0x5A` shared~~ `+0x44 = 0x8F`/`0x90` shared *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type 0x8F here)* creation arm (`005004C0` stubs 26 and 27): `00500470` prelude, `0020E620`/`003AA280`/`0042FCF0`/`004304F0`/`00430AF0`x3 over `+0x80`-`+0x3A0`, `00431770`x2, tail-jumps `00539E51`.

Interior anchor `00539DC7` (function `00539DA0`).

`00539C10` (223 B) is the ~~`+0x44 = 0x56`~~ `+0x44 = 0x8D` *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type 0x8D here)* creation arm (`005004C0` stub 23): `00500470` prelude, `0020E620`/`003AA280`/`0042FCF0`/`004304F0`x3/`00430AF0`x5 over `+0x80`-`+0x350`, `00431770`, tail-jumps `00539CD2`.

Interior anchor `00539C2D` (function `00539C10`).

`00539F80` (222 B) is the ~~`+0x44 = 0x5F`~~ `+0x44 = 0x97` *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type 0x97 here)* creation arm (`005004C0` stub 32): `00500470` prelude, `003AA280`/`0042FCF0`/`004304F0`/`00430AF0`x3 over `+0x80`-`+0x2C0`, `00431770`, tail-jumps `0053A02F`.

Interior anchor `00539FAD` (function `00539F80`).

`00539980` (218 B) is the ~~`+0x44 = 0x4D`/`0x54` shared~~ `+0x44 = 0x84`/`0x96` shared *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type 0x84 here)* creation arm (`005004C0` stubs 14 and 21): `00500470` prelude, `0020E620`x2/`003AA280`x2, `0042FCF0`/`004304F0`x4/`00430AF0`x3 over `+0x80`-`+0x240`.

Interior anchor `0053999D` (function `00539980`).

`00539B30` (211 B) is the ~~`+0x44 = 0x58`/`0x5D`/`0x5E` shared~~ `+0x44 = 0x8C`/`0x94`/`0x95` shared *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type 0x8C here)* creation arm (`005004C0` stubs 25, 30, 31): `00500470` prelude, `0020E620`/`003AA280`/`0042FCF0`/`004304F0`/`00430AF0`x3 over `+0x80`-`+0x2B0`, `00431770`, tail-jumps `00539BD3` - the family's widest sharing, three types one body.

Interior anchor `00539B57` (function `00539B30`).

`00539A60` (204 B) is the ~~`+0x44 = 0x57`~~ `+0x44 = 0x8B` *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type 0x8B here)* creation arm (`005004C0` stub 22): `00500470` prelude, `003AA280`x2, `0042FCF0`/`004304F0`x4/`00430AF0`x3 over `+0x80`-`+0x218`.

Interior anchor `00539A7D` (function `00539A60`).

`005394A0` (178 B) is the ~~`+0x44 = 0x4F`~~ `+0x44 = 0x86` *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type 0x86 here)* creation arm (`005004C0` stub 16): `00500470` prelude, `0042FCF0`x2/`004304F0`x5/`00430AF0`x3 over `+0x80`-`+0x260`.

Interior anchor `005394BD` (function `005394A0`).

Six more `005004C0` creation arms sit inside the 0x60-0x74 type block and
are measured in full under [the-element-types-60-74](the-element-types-60-74.md):
`0053A120` (types 0x60/0x62, stubs 33/35, anchor `0053A13D`), `0053A060`
(0x61, stub 34, anchor `0053A07D`), `0053A5D0` (~~0x65~~ **0x67**, stub 38, anchor
`0053A5FD`), `0053A6F0` (~~0x66~~ **0xA0**, stub 39, anchor `0053A70D`), `0053A790`
(~~0x67~~ **0xA1**, stub 40, anchor `0053A7AD`) and `0053A840` (~~0x68~~ **0xA2**, stub 41, anchor
`0053A86B`). **Corrected 2026-09-29 (FABLE, GI-10):** by `005004C0`'s table and `members/effect-type-methods.tsv`, `0x65`
and `0x66` use `0053A1E0` / `0053A3B0`, `0x68` has no main-range setup, and the last three arms belong to `0xA0`-`0xA2`
(check K14 of [`gi_effects_checks.py`](../../_index/candidates/gi-0929-effects/gi_effects_checks.py)). All six run the `00500470` prelude plus the `0042FCF0`/
`004304F0`/`00430AF0` field-init ladder; `0053A5D0` and `0053A840` close
through `00431770`.

`0047BE20` (331 B) is a `0043EBF0` gated record arm: `002F2D60` gate, `02F97348` mode byte >=0xA selects `[rdx+0x124..0x12C]` floats else 1.0f defaults, XOR-folds a `0x7F`-masked byte pair off `+0x122`/`+0x123` into the record tail, `0020E620` registers `[rdx+0x80]`, `003D7FF0` packs the record to `[rbx+0x230]`, `00377190` a second index to `[rbx+0x234]`, `003D8D70` closes.

Interior anchor `0047BE49` (function `0047BE20`).

`00377190` (148 B) is the handle-slot issuer `00463FF0`/`00464B30`/`00464F20`/`0047BE20` call on the `02ADBFE0` table (128 entries x 0x20, `[rax]` zero = free): serial `02ADBFC4` increments (wraps at 0xFFFFFF), packs `(serial<<8)|slot` into `[rax]`, stores the caller's pointer at `+8`, and links the node into the `02ADBFC8`/`02ADBFD0` pair (first-node write or append through `+0x18`/`+0x10`) - the effect family sibling of `003B4160`'s `02B404E0` allocator.

Interior anchor `003771B6` (function `00377190`).

`003D7FF0` (402 B) is the record issuer `003E7140`/`0047BE20` call on the `02B4D7D0` table (32 entries x 0x60, `dword[+4]` occupied): `byte[rcx+0xE]==2` + `byte[02B4D7A2]` nonzero early-outs; `00181DD0` allocates into `+0x50`, serial `02B4D7A4` packs `(serial<<8)|slot` into `+4`, the 32-byte source record copies to `+0x30`/`+0x40` (2 movups), `byte[+0x3E]==2` clamps `dword[+0x40]` to <=3, then `0020E620` registers `02B4E3D0[eax*8]+0x80` - the packet record the dispatch arms issue.

Interior anchor `003D806F` (function `003D7FF0`).

`00449970` (310 B) is the `002F2D60`-gated float translate `002F3BC0` calls: a zero return early-outs; `0044A180` prepares `r14`, then four passes step `rsi+0x278` at 0xF0 stride - each `[rdi-4]`/`[rdi]` float pair goes through `003D8E50` when nonzero and writes the results into `rbx-4`/`rbx` at `r14+0x29C`, zero floats storing literal 0 - the type's four-slot float block publish.

Interior anchor `004499E2` (function `00449970`).

`00503A80` (284 B) is the op-stream scanner the type-0x02 walk `004490D0` calls: for `ebx` under `word[rbp+0x10]`, the `0020E600` table's `ebx x 0x10` record switches on `byte[+8]` - kind 0 adds `byte[+9]` to the running total and remembers `ebx` in `r15` while the sum stays under `esi`, kind 1 re-jumps `ebx = sword[+0xC] - 1`, kind 2 compares `byte[r14+3]`'s parity; the exits write `byte[r14]` = final slot, `byte[r14+1]` = remainder, `byte[r14+2]` = best `r15`, and the return is the `r15`-indexed record pointer - the element stream's skip-list step.

Interior anchor `00503AC3` (function `00503A80`).

`00503A80` (284 B) is the op-stream scanner the type-0x02 walk `004490D0` calls: for `ebx` under `word[rbp+0x10]`, the `0020E600` table's `ebx x 0x10` record switches on `byte[+8]` - kind 0 adds `byte[+9]` to the running total and remembers `ebx` in `r15` while the sum stays under `esi`, kind 1 re-jumps `ebx = sword[+0xC] - 1`, kind 2 compares `byte[r14+3]`'s parity; the exits write `byte[r14]` = final slot, `byte[r14+1]` = remainder, `byte[r14+2]` = best `r15`, and the return is the `r15`-indexed record pointer - the element stream's skip-list step.

Interior anchor `00503AC3` (function `00503A80`).

`00376350` (280 B) is the `02ADBB40` slot issuer `00461090`'s flag arms call: eight `0x90`-stride slots scan for `dword[slot] == 0`; a free one takes `(++02ADBB34 wrapped at 0xFFFFFF) << 8 | slot` as its handle with `02ADBB30` bumped, `dword[+4]` = `edx`, the flag word `+0x54` cleared of bit 3 and given bit 2, `+0x70` taking the caller's 16-byte vec and the rest zeroed; `r8d` nonzero builds the `0x01020001` command (byte `+0x24` = 9, `+0x27` masked `& 3 | 0x40`) through `00861EC0`/`003AB960` with its result parked at `+0x50` - the keyed allocation `00377100`'s `+0x70` store writes into.

Interior anchor `00376448` (function `00376350`).

`002F3750` (265 B) is the `+0x220` scalar `002F2530` computes per element: when `byte[[rcx+0x20]+0x4B]` ~~lacks bit `4`~~ lacks bit 2 (mask `0x04`) *(corrected 2026-10-02, OPUS: `002F3750`+0x2A `test byte ptr [rdi + 0x4b], 4`)* the answer is `float[[rcx+0x20]+0x70]`; otherwise `byte[+0x4F] & 0x7F` dispatches - `0` copies `+0x70` verbatim, `1` runs `003A3FD0(sbyte[rdx+0x13B])`, `2` runs `003A6BA0(sbyte[rdx+0x13B])`, either guarded by `001EDDA0` plus a `dword[rcx+0x48] > 1`/`> 3` check, and a resolved index (`!= 0xFFFF`) pulls the `x 0x740` `022C6F28` record whose `+0x284` must be nonzero for `00264670([record+0x108])` to add onto `+0x70`; the result stores to `float[rcx+0x220]` and returns - the per-element height/scale the frame walk publishes.

Interior anchor `002F3790` (function `002F3750`).

`00523C30` (246 B) is the element field commit `0043EBF0` runs when `002F2D60` passes: `[rdi+0x20]`'s bytes `+0x874`/`+0x875` and words `+0x870`, `+0x87C`/`+0x87D`/`+0x87E` copy into the `[rdi+0x230]` block at `+0`, `+0x730`, `+8`, `+0x744`, `+0x794` (1.0f staging via `xmm6`), `003D8E50` runs four times across the block, `005439A0`/`00524320` close it and `[rbx+0x14]` lands at `[rdi+0xAC0]` - `1` on commit, early-out on the gate.

Interior anchor `00523C39` (function `00523C30`).

`00366690` (80 B) is the shared angle wrap: `xmm0` (degrees) scales by `pi/180` (`* 3.1415927`, `/ 180.0`), then two loops add `+2pi` while below `-pi` and `-2pi` while above `+pi` - the degree-to-radian normalize-to-`[-pi, pi]` the glyph, effect and map-ctrl callers share.

Interior anchor `003666C0` (function `00366690`).

`003B2CA0` (60 B) is the handle lookup over the sixty-four-entry `02EBDBC0` table: `rax` walks 0x28-stride rows to `02EBE5C8`, rows with `dword[-8]` set whose `qword[+0]` matches `rcx` return `02EBDBC0 + idx*0x28`, else 0 - the occupied-flag scan the stop-registry and effect-dispatch callers run.

Interior anchor `003B2CB0` (function `003B2CA0`).

`003E4F50` (278 B) is the emit-position fetch: `[rcx+0x400]`'s chain node must carry a nonzero `word[+0x12]`; then its `+0xD0/+0xD4/+0xD8` vec3 copies to `rbx` with `+0xC` = 1.0f, `0046D100` + `0046D0C0` build the local basis, and the `[rdi+0x670]` position adds on top - the world-space source point the effect-dispatch callers share.

Interior anchor `003E4FC7` (function `003E4F50`).

`0052ADF0` (609 B) is the element build behind the type dispatch: gated on `002F2D60(rcx)`, it mirrors the source record's `+0x7DC..+0x7E8` parameter block into the runtime block at `rdi+0x280` (eight `003D8E50`-evaluated float fields including the inverted `1 - x` at `+0x144`), unpacks flag bits out of `+0x7DD`/`+0x5AA`/`+0x69A`/`+0x78A`/`+0x7E8` into `+0x153`..`+0x15C` with a `003A6E60(2)` side call when `+0x7E8` bit 0 is armed, allocates the `+0x7DE`-count payload through `0036A190` - the `0036C140`/`002F31C0` arm returns 0 on failure - copies the `+0x7F0` bytes into it with `00861EBA`, links `+0x148`/`+0x3F0`, and finishes through `0054A9C0`/`0052B5E0` returning 1.

Interior anchor `0052B019` (function `0052ADF0`).

`003A3D30` (230 B) is the vec2 reciprocal `003A4290` calls for its aspect terms: it divides `1.0` by each of `[rdx]`'s first two floats (raw vector kept at `022D92E0`, quotients at `022D92F0`/`022D92F8`/`022D9198`), runs `0036DDA0` when a quotient is `0` and `0036DD90` when it is negative, then writes the corrected two-float result to `[rcx]`

Interior anchor `003A3DB7` (function `003A3D30`).

`001EDBB0` (204 B) is the spot gate `002F2530` consults: under `[01F82E38]` it runs `001EC560`, `001C50C0`s a string ref and `01CCEBD2`-compares it to `"spc_z0000"`, optionally vtable-`+0x18`-emitting the remainder; it returns 1 only when the name matched and `[01EF9218] == 8` with `ebx == 0x39F`, or on the `esi == 1`/`ebx == 0x14A` arm - the 'is this the special zone/id combination' check

Interior anchor `001EDBF6` (function `001EDBB0`).

`003A7730` (181 B) is the copy-in element emit `003ED8A0` runs for table-driven payloads: `[rcx]` byte selects the `003A78A0` table, `00334000(table, [rcx+1])` get-or-creates the `0x320` slot, `0046F380(slot, [rcx+2], sbyte[rcx+3], len - 0xC)` resolves the destination cursor, `00861EBA` copies the `rsi+0x10` payload in, and `004FF320(dst, 02EBB738 + dst)` registers it - returning `rsi + len`, the consumed cursor

Interior anchor `003A7792` (function `003A7730`).

`003A7DC0` (181 B) is the sibling emit `003ED8A0` runs for the chain-tracked kind: `[rcx]` byte indexes the `[[02EBEFA0]]` pointer table for the old slot `rsi`, `003A7BE0([rcx], [rcx+2], len)` allocates the replacement `rdi`, `00861EBA` copies `r14+4` in, `004FF270` registers under `02EBB738 + rdi`, then the `[[02EBEF98]]` chain is walked via `+0xF0` next pointers and every `+0xE0` field matching the old slot is repointed to the new - a copy with back-pointer fixup, returning `r14 + 4 + len`

Interior anchor `003A7E40` (function `003A7DC0`).

`00528090` (177 B) is the four-lane renormalise `0043EBF0` runs when the `002F2D60` gate passes: `00528820` rebuilds the element first, then four lanes (`src = [rbx+0x20] + 0x538 + i*0xF0`, `dst = rbx + 0x230 + i*8`) each fold two floats - a `0.0` source writes `0` outright, anything else is `003D8E50`-renormalised into the destination pair

Interior anchor `005280E0` (function `00528090`).

`003A7BE0` (198 B) is the `02EBEFA0` slot-table register `003A7DC0` calls: a zero `ecx` scans slots 1..`0x7F` for an empty qword cell, a nonzero `ecx` frees the existing entry through `003697F0` and clears the slot; then `0036A100(esi)` builds the record, `bx` stamps `+0xC0` and `bpl` `+0xC2`, and the pointer commits at `table[rdx*8]` - the element's allocate-or-replace cell emit

Interior anchor `003A7C39` (function `003A7BE0`).

`00462480` (177 B) is the `002F3BC0` arm for its type's variance refresh: `002F2D60` gates (zero returns inline), `004630D0` runs the prelude, then four iterations walk the element's `+0x20` table at `+0x4D8` in `0xF0` strides - each float pair writes to `rbx+0x294` as-is-zero or a fresh `003D8E50()` value when the source lane is nonzero

Interior anchor `004624E1` (function `00462480`).

`004633A0` (177 B) is a `002F3BC0` arm of the same four-lane variance-refresh family: `002F2D60` gate, `00463D20` prelude, four `0xF0`-stride source rows from `+0x5C8` writing the `+0x294` destination pairs through `003D8E50` when nonzero

Interior anchor `00463401` (function `004633A0`).

`0052BFB0` (177 B) is a `0043EBF0` sub-range arm of the same family: `002F2D60` gate, `0052CF60` prelude, four source rows at `+0x758` refreshing the element's `+0x284` pairs through `003D8E50` when nonzero

Interior anchor `0052C011` (function `0052BFB0`).

`00524D70` (177 B) is a `0043EBF0` sub-range arm of the same family: `002F2D60` gate, `005259E0` prelude, the `+0x758` rows refreshing `+0x234` through `003D8E50` when nonzero

Interior anchor `00524DD1` (function `00524D70`).

`00527110` (177 B) is the sibling `0043EBF0` arm with the same lane pair: `002F2D60` gate, `00527DC0` prelude, `+0x758` rows refreshing `+0x234` through `003D8E50` when nonzero

Interior anchor `00527171` (function `00527110`).

`00445310` (177 B) is the dispatcher's case-arm-5 refresh (`002F3BC0` names it fifth): `002F2D60` gate, `00445B50` prelude, four `0xF0`-stride rows from `+0x378` refreshing the element's `+0x270` pairs through `003D8E50` when nonzero

Interior anchor `00445371` (function `00445310`).

`00446F60` (177 B) is a `002F3BC0` arm of the same family: `002F2D60` gate, `00447830` prelude, `+0x3D8` source rows refreshing `+0x288` through `003D8E50` when nonzero

Interior anchor `00446FC1` (function `00446F60`).

`00447E10` (177 B) is a `002F3BC0` arm of the same family: `002F2D60` gate, `00448800` prelude, `+0x3D8` source rows refreshing `+0x280` through `003D8E50` when nonzero

Interior anchor `00447E71` (function `00447E10`).

`0052CF60` (1025 B) is the transform-commit prelude `0052BFB0` runs before its four-lane refresh: `[rcx+0x60]` stages into the `02CA8500`/`022D92E0` shared bank with per-lane accumulation, `0039AF70`/`00398F90` on the `[rcx+0x10]` child produce the `02CA8500` result committed to `[rax+0x70]` and `[rdx+0x70]`/`+0x80`; a `[rdx+0xBE1]` flag adds the `02AEDF20`-delta offset rows into `022D91B0`/`022D91C0` with a `0036DD80` squared-length pass, `[rax+0x4A] & 0x1C` chooses whether `00397ED0` runs `child+0x40` into `rbx+0x240`, `[rax+0x4B] & 2` picks `003970F0` over `0039ADE0` on `rdx+0x120`, and the staged matrix lands at `rbx+0x270` with `+0x27C` = `1.0f`

Interior anchor `0052D011` (function `0052CF60`).

`005259E0` (813 B) is the sibling prelude `00524D70` runs: the same `02CA8470`/`022D92E0` staging and `0039AF70`/`00398F90` child transform committed to `[rdx+0x70]`, then the `[rax+0xA51]` flag gates an extended path - `022D91B0`/`022D91C0` offset rows, a squared-magnitude through `00861F14`, a `comiss` clamp against `022D91E0`, and the folded scalar written to `rbx+0x250`; without the flag `+0x250` simply gets `1.0f`

Interior anchor `00525A88` (function `005259E0`).

`0036B080` (165 B) is the bit-gated aggregate `003A3670` runs: bit `ecx` of `022D89B8` guards and `ecx <= 0xE` selects the `022D7FD0 + ecx*0xA8` row; a dirty `+2` byte walks the `[rbx+0x90]` chain via `0020E600`, summing `[+0x18]` into `+0x64` and max-ing into `+0x8C` before clearing the dirty byte; returns `+0x8C`, or 0 when the bit is off

Interior anchor `0036B0ED` (function `0036B080`).

`003A93F0` (156 B) is the `[02EBEF88]+8`-list scan `0024B9B0` runs: each node's `[+0x100]` record must carry `byte[+0x283] == 2`, then `003A8240([rbx+0x1C], word[rax+0x286])` resolves a target that must have `byte[+0xC2] == 0` and `byte[+0x118]` in {3, 0xB}; a node whose `[+0x108]` record carries `+0x44` in {0xA1, 0x40} is stored to `02EBEF80` and handed to `00442310` - the filtered pick pass over the element list.

Interior anchor `003A942E` (function `003A93F0`).

`003A2BD0` (152 B) is the submit pump `003A3740` calls: `00865320()` + `00865360(2)` bracket, `001FBE50()`, then `0039D0C0(0, 0x3FFF, 0x200, {1,0}, 0)` submits the `0x1C0`+`0x40` block; `001FBD80(2)` and the `byte[02F8F310] & 1` lane picks `00862FD0`+`00863010(2)` or `00862E50`+`00862E90(2)`, closing with `00865130` + tail `00865170(2)` - worker-pool plumbing around one submit.

Interior anchor `003A2C0C` (function `003A2BD0`).

`003D8DE0` (58 B) is the keyed vector store into the `02B4D7D0` element row table: `(cl*3)*0x20` selects the row, the row's `+4` dword must equal `ecx`, and three dwords then copy from `rdx` into `+0x10`, `+0x14` and `+0x18` - key mismatch returns untouched; the value-update half of the parameter surface `003D8E20`'s `+0x30` float write and `003D8D70`'s `+0x3F` byte write sit beside.

Interior anchor `003D8E05` (function `003D8DE0`).

`003D8D70` (41 B) is the sibling keyed byte store on `02B4D7D0`: the same `(cl*3)*0x20` row selection and `+4` key check gate a `dl` write to row `+0x3F` - the flag-byte lane of the element-parameter update family `0047BDA0`/`0047BE20` and `003E6910` share.

Interior anchor `003D8D95` (function `003D8D70`).

`003A3E20` (12 B) is the two-field record stamp half the dispatch's callers funnel through: `dword[rcx+0x44]` sets to `-1` and `word[rcx+0x42]` takes `dx` - the invalidation+index write `003D9040`, the `0045D`/`00522`/`0053` widget arms and `005386F0` all share before continuing their own tails.

Interior anchor `003A3E27` (function `003A3E20`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-effect-element-type-dispatch-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001DB340` | 134 B | divides dword `rcx+0x1C` by dword `rcx+0x18` (unsigned) and writes 0 to address 0 when the quotient is 0x40 or more; when the qword at `rcx+0x20` + quotient*8 is null, fills it with `001A1470(qword 01F7F4C0, dword rcx+0x18 << 4)` and calls `0016D6A0(qword 01F7F4C0, that block)`; then stores the 16-byte pair (qword `rdx`, dword `r8d`) at 16-byte entry (dword `rcx+0x1C` modulo dword `rcx+0x18`) of that block and increments dword `rcx+0x1C` | `001DB35F`, `001DB364`, `001DB387`, `001DB3B4`, `001DB3B8` |
| `0020E610` | 8 B | returns 1 when `ecx` is zero, else 0 | `0020E612`, `0020E614` |
| `00231820` | 105 B | with `R` = qword `rcx+0x10` + `r8w`*0x20 and `V` = qword `rcx+8` + signed word `R+0x10`*0x10: when `r8w` is non-negative and float `R+4` is above 0.001 (`008C5B2C`), stores to float `rdx+4` the value float `V+4` + ((float `V+8` - float `rdx+8`) * float `R+8` + (float `V` - float `rdx`) * float `R`) / float `R+4`; otherwise stores float `rdx+4` back unchanged | `00231829`, `00231849`, `00231873`, `0023187D`, `00231883` |
| `0024B1C0` | 43 B | when word `02092168` is below 0x100 (unsigned), stores `rcx` to the qword at `02091150` + word*8 and increments word `02092168`; otherwise tail-jumps to `003697F0(rcx)` | `0024B1CC`, `0024B1CF`, `0024B1DF`, `0024B1E3` |
| `002F3890` | 122 B | copies dword `rcx+0x1F0` to `+0x1F4`; moves the 16 bytes at `+0x70` to `+0x80` and stores into `+0x70` the 16 bytes at `+0x60` when qword `+0x10` is null, otherwise a stack copy of `+0x60` after `0039AF70(qword +0x10)` and `00398F90(copy, copy)` | `002F38AE`, `002F38BB`, `002F38D6`, `002F38EA`, `002F38F2` |
| `00333C00` | 113 B | for each of the 0x1D dwords at `rcx+0x2C` (stride 4): when `0020E600(dword)` is non-null, calls `0046F370` and then `003697F0` on `0020E600(dword)` and stores `0020E620(0)` back into the dword | `00333C22`, `00333C36`, `00333C45`, `00333C51`, `00333C5F` |
| `00350DD0` | 238 B | computes `r` = `00267DB0(r9)`, `S` = `00358940(002640C0(), 00267E10(r9))` and `P` = `003588B0(003590D0())`; when `P` and `S` are both non-null, reads three floats through `00265020(S, ...)` and tail-jumps to `0026B4E0(rcx, 1)` when `r*r` is above their squared distance to the three floats at qword `P+0xB8`, otherwise (also when `P` or `S` is null) to `0026B4E0(rcx, 0)` | `00350E10`, `00350E1F`, `00350E47`, `00350E98`, `00350EB9` |
| `00377010` | 119 B | selects the 0x90-byte row `02ADBB40` + (low byte of `ecx`)*0x90 and, when `ecx` is non-zero and equals the row's dword `+0`, copies bit 0 of word `[rdx]` into bit 0 and bit 0 of word `rdx+4` into bit 1 of word `+0x54`, dwords `rdx+0x14` to `rdx+0x20` into `+0x40` to `+0x4C` and dwords `rdx+8` to `rdx+0x10` into `+0x34` to `+0x3C`; otherwise returns without writing | `00377028`, `0037702D`, `0037703B`, `00377050`, `00377058` |
| `0039D430` | 68 B | copies the 64 bytes at `rcx` to `02AEE9E0`, `02AEE9F0`, `02AEEA00` and `02AEEA10`, calls `0039AFA0()` and tail-jumps to `003970A0(02AEECB0)` | `0039D437`, `0039D458`, `0039D45F`, `0039D46F` |
| `003A5640` | 126 B | with `i` = `ecx` (0 when `ecx` is -1) and `G` = qword `02F97348`: when word `G+0x378` has bit 0x200, returns -1 if `i` is not below dword `02096B24` (signed) and otherwise `002E9B80(dword 02096A24 + i*4)`; else when byte `[G]` is 3 returns dword `G+0x10+i*4`; else returns `002E9B80` of dword `G+0x90+i*4`, or of dword `G+0x10+i*4` when that is zero | `003A5652`, `003A565C`, `003A566B`, `003A5686`, `003A56AC` |
| `003A7CB0` | 78 B | walks the qword slots at offsets 0 to 0x3F8 (stride 8, loop bound 0x400) of the table at qword `[qword 02EBEFA0]` and, for each non-null slot, calls `003697F0(slot)` and zeroes the slot | `003A7CCA`, `003A7CD3`, `003A7CE2`, `003A7CEA` |
| `003A9510` | 79 B | walks the qword slots at offsets 8 to 0x9F8 (stride 8, loop bound 0xA00) of the table at qword `[qword 02EBEF90]` and, for each non-null slot, calls `003697F0(slot)` and zeroes the slot | `003A952B`, `003A9534`, `003A9543`, `003A954B` |
| `003A98D0` | 79 B | walks the qword slots at offsets 8 to 0x17F8 (stride 8, loop bound 0x1800) of the table at qword `[qword 02EBEF78]` and, for each non-null slot, calls `003697F0(slot)` and zeroes the slot | `003A98EB`, `003A98F4`, `003A9903`, `003A990B` |
| `003A99F0` | 117 B | calls `003A9AD0(word [rcx], sign-extended byte rcx+2, edx)`; when that returns null, returns null; otherwise calls `00861EBA(result, rcx+4, edx)` and `005004C0(result, dword 02EBB738 + low dword of result)` and returns `rcx+4+edx` | `003A9A12`, `003A9A1D`, `003A9A39`, `003A9A49`, `003A9A57` |
| `003CC0F0` | 57 B | zeroes dword `rcx+0xC0`, calls `00202C70(rcx+0x20, rdx)` and tail-jumps to `00202D50(rcx+0x60, rdx)` | `003CC0FD`, `003CC10E`, `003CC124` |
| `003D8E20` | 41 B | selects the 0x60-byte row `02B4D7D0` + (low byte of `ecx`)*0x60 and, when its dword `+4` equals `ecx`, stores `xmm1` to its float `+0x30`; otherwise writes nothing | `003D8E37`, `003D8E3A`, `003D8E43` |
| `003D9040` | 119 B | zeroes qword `rcx+0x330` and dword `+0x338`; returns 0 when `002F2D60(rcx)` is zero; otherwise calls `003A3E20(rcx+0x2D0, 0)` and `003D92C0(rcx)`, and when byte `[qword 02F97348]` is 1 increments byte `+0x37A` of that block and calls `002EA8B0(3, 1)` when the result is 1; returns 1 | `003D905F`, `003D9070`, `003D9078`, `003D9089`, `003D90A7` |
| `003E7140` | 198 B | when dword `rcx+0x448` is non-zero calls `003D8300` on it; copies dword `+0x44C` to `+0x448`; builds a stack record with floats `xmm1`, `xmm2`, `xmm3` at `+0`, `+4`, `+8`, byte `+0xC` with bits 0-5 cleared and bit 6 set, byte `+0xD` ANDed with 0x80, byte `+0xE` = 2 and dword `+0x10` = the sixth (stack) argument when it is below 4 (signed), else 0; and stores `003D7FF0(record)` to dword `+0x44C` | `003E717F`, `003E7191`, `003E71BB`, `003E71D5`, `003E71DA` |
| `00431040` | 56 B | calls `00430A60(rcx, xmm1)` and `00430A60(rcx+0x10, xmm1)` and tail-jumps to `00430A60(rcx+0x20, xmm1)` | `00431051`, `0043105D`, `00431073` |
| `0043E9C0` | 89 B | when byte `[rcx]` minus 0x42 is at most 0x61 (unsigned, types 0x42 to 0xA3), reads a byte map and then an offset table indexed by it and jumps to the selected arm; the arms are tail jumps, with `rcx` and `rdx` unchanged and `r8`/`r9` overwritten (jump target, image base), to `00524A10`, `00526040`, `0016D6A0`, `0047BF70`, `005294B0`, `0052A340`, `0052B060`, `0052D8E0` and `0052EA50`, plus the `ret` at `0043EA18`; per the tables (not the listing) only types 0x42 (`0047BF70`), 0x6A (`00526040`), 0x6B (`005294B0`), 0x70 (`0016D6A0`), 0x71 (`0052A340`), 0x72 (`0052B060`), 0x73 (`0052D8E0`), 0x74 (`0052EA50`) and 0xA3 (`00524A10`) take a tail jump, and every other type returns | `0043E9C6`, `0043E9D4`, `0043E9E8`, `0043E9EB`, `0043EA18` |
| `00448D70` | 103 B | calls `002F2530` with the incoming arguments and returns 0 when it returns 0; otherwise, when word `+0x180` of qword `rcx+0x20` has bit 0x800, adds the truncated `xmm2` to byte `rcx+0x2A1`, then calls `00449560(rcx)` and returns the `002F2530` result | `00448D85`, `00448D8E`, `00448DA9`, `00448DB7`, `00448DC0` |
| `00455560` | 1112 B | with `D` = qword `rcx+0x20`, runs `00398030` on a stack copy `M` of the 64 bytes at `rcx+0x250` with `02AEEC30`, `02AEEC70` or `02AEEA60` when bits 2-4 of byte `D+0x4A` are 1, 2, or 4/5 (after `00434900(M)`/`00434A70(M)`); calls `0039B620(dword rcx+0x290)`, `0039B550(02AEECB0)`, `00397910(stack, M, 02AE0310)`; returns unless byte `D+0x240` is 2 or 4 and `00431830(D+0x1A0, out, 0, dword rcx+0x44)` is non-null; fills globals `02AEE908`, `02AEE900`, `02AE0370`, `02AE0360`, `02AE02B0`, `02AE02B4` and `02AE02A0` to `02AE02AC`; when `E` = `0020E600` of the dword at `D+0x2A0` indexed by dword `rcx+0x298` is non-null, calls `0039B550(02AEECB0)` and, by bits 1-2 of byte `D+0x294` (0: nothing; 1: dword `02AE0280` = 0; 2: = 2; 3: twice, with 2 then 0), `003A2F70(dword 02AE0268, dword 02AE026C, 00499A20, 02AE0278, 0x118, 0020E600(dword E+0x10), dword E+0x14)` when byte `D+0x24A` AND 7 is zero, else `003A33B0(s, ...)` with those arguments, `s` = `0039A9B0(rcx+0x230)` when byte `D+0x4B` bit 0 is set, else dword `+4` of the buffer passed to `00399600(rcx+0x230, buffer)` (returning when that call is non-zero) | `0045560E`, `00455652`, `004556A7`, `00455923`, `0045598A` |
| `004559C0` | 870 B | with `D` = qword `rcx+0x20`, runs `00398030` on a stack copy `M` of the 64 bytes at `rcx+0x250` with `02AEEC30`, `02AEEC70` or `02AEEA60` when bits 2-4 of byte `D+0x4A` are 1, 2, or 4/5 (after `00434900(M)`/`00434A70(M)`); calls `0039B620(dword rcx+0x290)`, `0039B550(02AEECB0)`, `00397910(stack, M, 02AE01E0)`; returns unless byte `D+0x240` is 2 or 4 and `00431830(D+0x1A0, out, 0, dword rcx+0x44)` is non-null; fills globals `02AEE908`, `02AEE900`, `02AE0240`, `02AE0230`, `02AE0180`, `02AE0184` and `02AE0170` to `02AE017C`; when `E` = `0020E600` of the dword at `D+0x2A0` indexed by dword `rcx+0x298` is non-null, calls between `003A3D00(byte D+0x74)` and `003A3D00(0)` `003A2F70(dword 02AE0138, dword 02AE013C, 00497AC0, 02AE0148, 0x118, 0020E600(dword E+0x10), dword E+0x14)` when byte `D+0x24A` AND 7 is zero, else `003A33B0(s, ...)` with those arguments, `s` = `0039A9B0(rcx+0x230)` when byte `D+0x4B` bit 0 is set, else dword `+4` of the buffer passed to `00399600(rcx+0x230, buffer)` (returning when that call is non-zero), with `0039B550(02AEECB0)` first on that path | `00455A67`, `00455AAB`, `00455C15`, `00455C50`, `00455CF3` |
| `0045A220` | 1152 B | returns at once when byte `[rcx]` is 0; otherwise, with `D` = qword `rcx+0x20`, runs `00398030` on a stack copy `M` of the 64 bytes at `rcx+0x250` with `02AEEC30`, `02AEEC70` or `02AEEA60` when bits 2-4 of byte `D+0x4A` are 1, 2, or 4/5 (after `00434900(M)`/`00434A70(M)`); calls `0039B620(dword rcx+0x290)`, `0039B550(02AEECB0)`, `00397910(stack, M, 02AE3020)`; returns unless byte `D+0x250` is 2 or 4 and `00431830(D+0x1B0, out, 0, dword rcx+0x44)` is non-null; fills globals `02AEE908`, `02AEE900`, `02AE3080`, `02AE3070`, `02AE2FC0`, `02AE2FC4`, `02AE2FCC` and `02AE2FB0` to `02AE2FBC`; when `E` = `0020E600` of the dword at `D+0x2B0` indexed by dword `rcx+0x298` is non-null, calls `0039B550(02AEECB0)` and, by bits 1-2 of byte `D+0x2A4` (0/1: dword `02AE2F90` = 0; 2: = 2; 3: twice, with 2 then 0), `003A2F70(dword 02AE2F78, dword 02AE2F7C, 004AAFC0, 02AE2F88, 0x118, 0020E600(dword E+0x10), dword E+0x14)` when byte `D+0x25A` AND 7 is zero, else `003A33B0(s, ...)` with those arguments, `s` = `0039A9B0(rcx+0x230)` when byte `D+0x4B` bit 0 is set, else dword `+4` of the buffer passed to `00399600(rcx+0x230, buffer)` (returning when that call is non-zero) | `0045A246`, `0045A31E`, `0045A462`, `0045A607`, `0045A66E` |
| `0045A6A0` | 937 B | returns at once when byte `[rcx]` is 0; otherwise, with `D` = qword `rcx+0x20`, runs `00398030` on a stack copy `M` of the 64 bytes at `rcx+0x250` with `02AEEC30`, `02AEEC70` or `02AEEA60` when bits 2-4 of byte `D+0x4A` are 1, 2, or 4/5 (after `00434900(M)`/`00434A70(M)`); calls `0039B620(dword rcx+0x290)`, `0039B550(02AEECB0)`, `00397910(stack, M, 02AE2130)`; returns unless byte `D+0x250` is 2 or 4 and `00431830(D+0x1B0, out, 0, dword rcx+0x44)` is non-null; fills globals `02AEE908`, `02AEE900`, `02AE2190`, `02AE2180`, `02AE20D0`, `02AE20D4`, `02AE20DC` and `02AE20C0` to `02AE20CC`; takes `E` = `0020E600` of the dword at `D+0x2B0` indexed by dword `rcx+0x298` when byte `D+0x2A4` has bit 0, else by `n` = truncated float `02AE20DC` (returning when `n` is above 3, unsigned, else subtracting `n` from that float); when `E` is non-null calls `003A2F70(dword 02AE2088, dword 02AE208C, 004A8B00, 02AE2098, 0x118, 0020E600(dword E+0x10), dword E+0x14)` when byte `D+0x25A` AND 7 is zero, else `003A33B0(s, ...)` with those arguments, `s` = `0039A9B0(rcx+0x230)` when byte `D+0x4B` bit 0 is set, else dword `+4` of the buffer passed to `00399600(rcx+0x230, buffer)` (returning when that call is non-zero), with `0039B550(02AEECB0)` first on that path | `0045A6C3`, `0045A903`, `0045A928`, `0045A9A3`, `0045AA16` |
| `0045AEF0` | 867 B | with `D` = qword `rcx+0x20`, runs `00398030` on a stack copy `M` of the 64 bytes at `rcx+0x250` with `02AEEC30`, `02AEEC70` or `02AEEA60` when bits 2-4 of byte `D+0x4A` are 1, 2, or 4/5 (after `00434900(M)`/`00434A70(M)`); calls `0039B620(dword rcx+0x290)`, `0039B550(02AEECB0)`, `00397910(stack, M, 02AE32A0)`, `00397910(02AEEA20, M, M)`, `00397910(02AEDDF0, M, 02AE3250)`; returns unless byte `D+0x240` is 2 or 4 and `00431830(D+0x1A0, out, 0, dword rcx+0x44)` is non-null; fills globals `02AEE908`, `02AEE900`, `02AE3300`, `02AE32F0`, `02AE3240`, `02AE3244` and `02AE3230` to `02AE323C`; when `E` = `0020E600` of the dword at `D+0x2A0` indexed by dword `rcx+0x298` is non-null, calls `003A2F70(dword 02AE31F8, dword 02AE31FC, 004ADD10, 02AE3208, 0x128, 0020E600(dword E+0x10), dword E+0x14)` when byte `D+0x24A` AND 7 is zero, else `003A33B0(s, ...)` with those arguments, `s` = `0039A9B0(rcx+0x230)` when byte `D+0x4B` bit 0 is set, else dword `+4` of the buffer passed to `00399600(rcx+0x230, buffer)` (returning when that call is non-zero), with `0039B550(02AEECB0)` first on that path | `0045AFDF`, `0045AFF6`, `0045B006`, `0045B19E`, `0045B227` |
| `0045B2B0` | 902 B | with `D` = qword `rcx+0x20`, runs `00398030` on a stack copy `M` of the 64 bytes at `rcx+0x250` with `02AEEC30`, `02AEEC70` or `02AEEA60` when bits 2-4 of byte `D+0x4A` are 1, 2, or 4/5 (after `00434900(M)`/`00434A70(M)`); copies the three 16-byte rows of `00397910(02AEEBF0, M, T)`, each passed through `0039B960`, to `02AE33A0`, `02AE33B0`, `02AE33C0`; calls `0039B620(dword rcx+0x290)`, `0039B550(02AEECB0)`, `00397910(stack, M, 02AE33E0)`; returns unless byte `D+0x240` is 2 or 4 and `00431830(D+0x1A0, out, 0, dword rcx+0x44)` is non-null; fills globals `02AEE908`, `02AEE900`, `02AE3440`, `02AE3430`, `02AE338C` and `02AE3370` to `02AE337C`; when `E` = `0020E600` of the dword at `D+0x2A0` indexed by dword `rcx+0x298` is non-null, calls `003A2F70(dword 02AE3338, dword 02AE333C, 004B0230, 02AE3348, 0x118, 0020E600(dword E+0x10), dword E+0x14)` when byte `D+0x24A` AND 7 is zero, else `003A33B0(s, ...)` with those arguments, `s` = `0039A9B0(rcx+0x230)` when byte `D+0x4B` bit 0 is set, else dword `+4` of the buffer passed to `00399600(rcx+0x230, buffer)` (returning when that call is non-zero), with `0039B550(02AEECB0)` first on that path | `0045B371`, `0045B3A5`, `0045B492`, `0045B581`, `0045B60A` |
| `00463FF0` | 81 B | returns 0 when `002F2D60(rcx)` is zero; otherwise clears bit 0 of byte `rcx+0x248`, zeroes dword `+0x244`, calls `004649A0(rcx)` and `00377190(rcx)`, then sets bit 1 of byte `+0x248`, stores the `00377190` result to dword `+0x24C` and returns 1 | `00464000`, `00464008`, `0046401C`, `00464029`, `00464030` |
| `00464B30` | 66 B | returns 0 when `002F2D60(rcx)` is zero; otherwise zeroes dword `rcx+0x234`, stores `00377190(rcx)` to dword `+0x238`, sets bit 0 of byte `+0x23C` and returns 1 | `00464B40`, `00464B4B`, `00464B55`, `00464B5A`, `00464B61` |
| `00465680` | 13 B | sets bit 0x80 of word `rcx+0x232` (ORs it with 0x80 loaded at the entry) | `00465685` |
| `004FF270` | 55 B | dispatches on byte `rcx+0xC2`: tail-jumps to `00537C80` for 0, `00537FA0` for 1, `00538350` for 2 and `005387B0` for 3, with `rcx`, `rdx` and `r9` unchanged (`r8` is overwritten by the selector arithmetic), and returns `rcx` for any other value | `004FF278`, `004FF289`, `004FF28F`, `004FF293`, `004FF2A2` |
| `00501440` | 108 B | calls `003697F0` on qword `rcx+0x20` and on qword `rcx+0x18` when each is non-null; when qword `+0xB8` is non-null calls `00183720` on it and on qword `+0xB0` and zeroes qword `+0xB8`; then zeroes dwords `+0x10` and `+0xA8` and qword `+0x20` | `00501452`, `00501460`, `00501471`, `0050147D`, `00501494` |
| `005014B0` | 94 B | stores `0020E620(0)` to dwords `rcx+0` and `rcx+4`, zeroes dword `+8` and copies word `[rdx]` to word `+0xC` and bytes `rdx+2` and `rdx+3` to bytes `+0xE` and `+0xF`; zeroes qwords `+0x20`, `+0x18` and `+0xB8` and tail-jumps to `00501440(rcx)` | `005014C9`, `005014D0`, `005014DB`, `005014F5`, `00501509` |
| `005019D0` | 104 B | stores `0020E620(0)` to dwords `rcx+0` and `rcx+4`, zeroes dword `+8` and copies word `[rdx]` to word `+0xC` and bytes `rdx+2` and `rdx+3` to bytes `+0xE` and `+0xF`; clears bit 0 of word `+0x40`, zeroes qwords `+0x10`, `+0x18`, `+0x20`, `+0x28` and `+0x30` and tail-jumps to `00501950(rcx)` | `005019E9`, `005019FB`, `00501A0D`, `00501A22`, `00501A33` |
| `00503830` | 78 B | when bit 0 of byte `rcx+0x16` is clear and `0020E600(dword rcx+0x18)` is non-null, calls `003697F0` on that result; then stores `0020E620(0)` to dword `+0x18`, zeroes dword `+0x10` and word `+0x14` and clears bit 0 of word `+0x16` | `0050383D`, `00503857`, `00503863`, `0050386B`, `00503874` |
| `00503C50` | 79 B | stores `0020E620(0)` to dwords `rcx+0` and `rcx+4`, zeroes dword `+8` and copies word `[rdx]` to word `+0xC` and bytes `rdx+2` and `rdx+3` to bytes `+0xE` and `+0xF`; then zeroes qword `+0x18` and dword `+0x10` | `00503C69`, `00503C70`, `00503C7B`, `00503C92`, `00503C96` |
| `00503DE0` | 71 B | when bit 0 of byte `rcx+0x18` is clear and `0020E600(dword rcx+0x10)` is non-null, calls `003697F0` on that result; then clears bit 0 of byte `+0x18`, stores `0020E620(0)` to dword `+0x10` and zeroes dword `+0x14` | `00503DED`, `00503E07`, `00503E13`, `00503E17`, `00503E1A` |
| `00504000` | 93 B | calls `003697F0(0020E600(dword rcx+0x28))` when that lookup is non-null and stores `0020E620(0)` to dword `+0x28`; when dword `+0x14` is non-zero and byte `+0x18` is 1 or 3, calls `003D7F30(byte +0x18, dword +0x14)`; then zeroes qword `+0x10` | `00504021`, `00504030`, `00504044`, `0050404C`, `00504053` |
| `005041F0` | 50 B | calls `003697F0(0020E600(dword rcx+0x18))` when that lookup is non-null, then zeroes qword `rcx+0x10` | `00504204`, `00504211`, `00504218` |
| `005042C0` | 82 B | stores `0020E620(0)` to dwords `rcx+0` and `rcx+4`, zeroes dword `+8` and copies word `[rdx]` to word `+0xC` and bytes `rdx+2` and `rdx+3` to bytes `+0xE` and `+0xF`; then zeroes qword `+0x28`, byte `+0x14` and dword `+0x10` | `005042D9`, `005042E0`, `005042EB`, `00504302`, `00504309` |
| `00532E80` | 104 B | with `n` = word `rcx+0xB0`, computes (dword `[rdx]` + 1 + `n`*0x20) * 0x10, adds (`n` + 6) * 0x50 once for each non-zero dword among `r8+0x88`, `r8+0x8C` and `r8+0x90`, and returns the 32-bit sum shifted right by 4 | `00532E94`, `00532E9B`, `00532EB2`, `00532EC9`, `00532EE0` |
| `00538A60` | 66 B | calls `00500470` with the incoming `rcx` and `edx`, then `0042FCF0(rcx+0x80, edx)` and `004304F0(rcx+0xD0, edx)`, and returns `rcx+0xF0` | `00538A6F`, `00538A7D`, `00538A8B`, `00538A95` |
| `00540C20` | 76 B | takes entry word `02F8F2C6` of the 0x28-byte array at qword `02F8F2F8` and increments the word; stores `rcx` to its qword `+0`, `r9d` AND 0xFFFFFF to dword `+8`, ORs byte `02AEE910` shifted left 4 into byte `+0xB`, stores `edx` to dword `+0xC` and zeroes qword `+0x10` | `00540C42`, `00540C4A`, `00540C4D`, `00540C5B`, `00540C5F` |
| `00543940` | 87 B | computes (dword `[rdx]` + 0x78) * 0x10, adds 0x190 for each non-zero dword among `rcx+0x740`, `+0x790`, `+0x7E0` and `+0x830`, and returns the 32-bit sum shifted right by 4 | `0054394E`, `0054395C`, `00543982`, `00543990`, `00543993` |
| `005439A0` | 38 B | zeroes dwords `rcx+0x14` and `rcx+4` and stores 1.0 (`01CEBBA8`) divided by (dword `[rcx]` + 1, converted to float) to float `+0x18` | `005439AD`, `005439B6`, `005439B9`, `005439BC`, `005439C0` |
| `00544590` | 68 B | calls `0020E600(dword rcx+0x64)` without using its result and returns 0x13 when dword `[rcx]` is 0, else 0x13 + (dword - 1) / 20 (unsigned) + 1 | `005445A2`, `005445AB`, `005445B4`, `005445B8`, `005445CB` |
| `005479B0` | 73 B | walks the four words at `rcx+2`, `+0x92`, `+0x122` and `+0x1B2` (stride 0x90) and returns 0 when all are zero, else (0x40 + 0xF0 for the first non-zero word + 0x100 for each further one) shifted right by 4 | `005479C7`, `005479DA`, `005479E8`, `005479F1`, `005479F5` |
| `00547D80` | 77 B | with `n` = dword `rcx+0x140`, computes (dword `[rdx]` + 0x18 + `n`*0x27) * 0x10, adds `n`*0xC0 for each non-zero byte among `rcx+0x78`, `+0x79` and `+0x7A`, and returns the 32-bit sum shifted right by 4 | `00547D8F`, `00547D96`, `00547D99`, `00547DB7`, `00547DC7` |
| `0054A980` | 64 B | computes (dword `[rdx]` + 0x3F) * 0x10, adds 0xC0 for each non-zero byte among `rcx+0x156`, `+0x157` and `+0x158`, and returns the 32-bit sum shifted right by 4 | `0054A988`, `0054A995`, `0054A9AA`, `0054A9B8`, `0054A9BC` |
| `005F01B0` | 111 B | returns at once when `rcx` is null; otherwise, for each of `edx` (unsigned) 0x50-byte entries from `rcx`, calls `0062B7B0(entry)` when `00625EC0(entry)` returns a non-zero byte and then `00616420(entry)`; finally calls `00584730(rcx)` | `005F01B3`, `005F01E3`, `005F01EF`, `005F01F7`, `005F020A` |

`0051CDE0` (998 B) is the element-parameter fill `003E6680` runs: a u16 index selects the `0x740`-stride record off `022C6F28`, `02CA8428` folds in, `01F2B349..4D` byte-table reads pair with `02AEDD30`..`02AEDEA0` vec4 banks, and `00540C70`, `003E5770` (x2), `001FBD80`, `0039D3F0`, `001EDDA0`/`001FBE50` route the result into the element rows - the staged parameter write this dispatch family's callers share.

Interior anchor `0051D043` (function `0051CDE0`).

## Homed bodies re-homed here for host fit (FABLE, 2026-10-03; move drafted by OPUS)

*Each body below was homed on another page by FABLE's homing stream (cloud-drafted, FABLE-verified). SWE2-AUDIT-SPEC reviewed its sentence, site and anchors exact, and rejected only the host: that page cites the caller as a foreign or boundary mention (commit `4522aeff6`). The row is moved here because this page cites the caller in its own text. The sentence is unchanged except where `moves.json` records a bits-as-values edit. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`move_rows.py`](../../_index/candidates/opus-fable-home-host-moves-1003/move_rows.py): every site transfers to its function, this page cites the caller outside this section, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors | moved from |
|---|---|---|---|---|---|
| `003A7950` | 109 B | `003ED8A0` + 0x135 | with `t` = qword `02EBEFA8` and `k` = byte `rcx+1`, when qword `t+8+k*8` is non-null passes it to `003A7950` + 0x33 and then `003A7950` + 0x3B, then, re-reading `t` from `02EBEFA8` for each access, stores 0 to qword `t+8+k*8` and decrements dword `[t]`; returns `rcx+2` on both paths | Interior anchor `003A7976`; Interior anchor `003A7983`; Interior anchor `003A798B`; Interior anchor `003A7997`; Interior anchor `003A79A7` | [gambit-evaluation-and-enmity](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) |
| `003A7A50` | 73 B | `003ED8A0` + 0x142 | copies the 0x2C bytes at `rcx+4` into the buffer returned by `003A7A50` + 0xE(byte `rcx+1`), passes that buffer (with 0 in `edx`) to `003A7A50` + 0x37, and returns `rcx+0xA4` | Interior anchor `003A7A5E`; Interior anchor `003A7A69`; Interior anchor `003A7A81`; Interior anchor `003A7A87`; Interior anchor `003A7A8C` | [gambit-evaluation-and-enmity](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) |
| `003A7AA0` | 53 B | `003ED8A0` + 0x1C7 | when qword `02EBEFA8` `+8` + byte `rcx+1` times 8 holds a non-null qword, calls `003A7AA0` + 0x26 with it and the zero-extended byte `rcx+2`; returns `rcx+3` on both paths | Interior anchor `003A7AB9`; Interior anchor `003A7AC1`; Interior anchor `003A7AC6`; Interior anchor `003A7ACB` | [gambit-evaluation-and-enmity](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) |
| `003A92B0` | 24 B | `003ED8A0` + 0x1D1 | calls `003A92B0` + 0x9(`rcx`) and returns `rcx+2` | Interior anchor `003A92B9`; Interior anchor `003A92BE` | [gambit-evaluation-and-enmity](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) |

## Homed bodies re-homed here for host fit (FABLE, 2026-10-03; AUDIT-SPEC batch 4)

*Each body below was homed on another page by FABLE's homing stream (cloud-drafted, FABLE-verified). SWE2-AUDIT-SPEC reviewed its sentence, site and anchors exact, and rejected only the host: that page cites the caller as a foreign or boundary mention (commit `95d495604`). The row is moved here because this page cites the caller in its own text. The sentence is unchanged. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`move_rows.py`](../../_index/candidates/fable-home-host-moves-b4-1003/move_rows.py): every site transfers to its function, this page cites the caller outside this section, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors | moved from |
|---|---|---|---|---|---|
| `0044D460` | 54 B | `002F3BC0` + 0xCA | calls `0044D460` + 0x9 with `rcx` unchanged and, when it returns 0 in `eax`, returns that 0; otherwise calls `0044D460` + 0x1B with the original `rcx`, then `0044D460` + 0x20 with no arguments set, stores that call's `eax` into dword `rcx+0x258` (original `rcx`) and returns 1 | Interior anchor `0044D469`; Interior anchor `0044D470`; Interior anchor `0044D47B`; Interior anchor `0044D485`; Interior anchor `0044D48B` | [CONTRACT-boot-fixups](../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md) |
| `0044ED90` | 54 B | `002F3BC0` + 0xF1 | calls `0044ED90` + 0x9 with `rcx` unchanged and, when it returns 0 in `eax`, returns that 0; otherwise calls `0044ED90` + 0x1B with the original `rcx`, then `0044ED90` + 0x20 with no arguments set, stores that call's `eax` into dword `rcx+0x244` (original `rcx`) and returns 1 | Interior anchor `0044ED99`; Interior anchor `0044EDA0`; Interior anchor `0044EDAB`; Interior anchor `0044EDB5`; Interior anchor `0044EDBB` | [CONTRACT-boot-fixups](../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md) |
| `0044F930` | 54 B | `002F3BC0` + 0xFE | calls `0044F930` + 0x9 with `rcx` unchanged and, when it returns 0 in `eax`, returns that 0; otherwise calls `0044F930` + 0x1B with the original `rcx`, then `0044F930` + 0x20 with no arguments set, stores that call's `eax` into dword `rcx+0x454` (original `rcx`) and returns 1 | Interior anchor `0044F939`; Interior anchor `0044F940`; Interior anchor `0044F94B`; Interior anchor `0044F955`; Interior anchor `0044F95B` | [CONTRACT-boot-fixups](../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md) |
| `00451140` | 54 B | `002F3BC0` + 0x118 | calls `00451140` + 0x9 with `rcx` unchanged and, when it returns 0 in `eax`, returns that 0; otherwise calls `00451140` + 0x1B with the original `rcx`, then `00451140` + 0x20 with no arguments set, stores that call's `eax` into dword `rcx+0x290` (original `rcx`) and returns 1 | Interior anchor `00451149`; Interior anchor `00451150`; Interior anchor `0045115B`; Interior anchor `00451165`; Interior anchor `0045116B` | [CONTRACT-boot-fixups](../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md) |
| `00451890` | 54 B | `002F3BC0` + 0x125 | calls `00451890` + 0x9 with `rcx` unchanged and, when it returns 0 in `eax`, returns that 0; otherwise calls `00451890` + 0x1B with the original `rcx`, then `00451890` + 0x20 with no arguments set, stores that call's `eax` into dword `rcx+0x290` (original `rcx`) and returns 1 | Interior anchor `00451899`; Interior anchor `004518A0`; Interior anchor `004518AB`; Interior anchor `004518B5`; Interior anchor `004518BB` | [CONTRACT-boot-fixups](../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md) |
| `00453CB0` | 54 B | `002F3BC0` + 0x14C | calls `00453CB0` + 0x9 with `rcx` unchanged and, when it returns 0 in `eax`, returns that 0; otherwise calls `00453CB0` + 0x1B with the original `rcx`, then `00453CB0` + 0x20 with no arguments set, stores that call's `eax` into dword `rcx+0x244` (original `rcx`) and returns 1 | Interior anchor `00453CB9`; Interior anchor `00453CC0`; Interior anchor `00453CCB`; Interior anchor `00453CD5`; Interior anchor `00453CDB` | [CONTRACT-boot-fixups](../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md) |
| `004548F0` | 54 B | `002F3BC0` + 0x159 | calls `004548F0` + 0x9 with `rcx` unchanged and, when it returns 0 in `eax`, returns that 0; otherwise calls `004548F0` + 0x1B with the original `rcx`, then `004548F0` + 0x20 with no arguments set, stores that call's `eax` into dword `rcx+0x290` (original `rcx`) and returns 1 | Interior anchor `004548F9`; Interior anchor `00454900`; Interior anchor `0045490B`; Interior anchor `00454915`; Interior anchor `0045491B` | [CONTRACT-boot-fixups](../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md) |
| `0045BF50` | 87 B | `002F3BC0` + 0x1E8 | calls `0045BF50` + 0x9 with `rcx` unchanged and, when it returns 0 in `eax`, returns that 0; otherwise stores 0x10001 into dword `rcx+0x24C` (original `rcx`), calls `0045BF50` + 0x2C and `0045BF50` + 0x37 with no arguments set, storing their `eax` into dwords `rcx+0x244` and `rcx+0x248` in that order, then calls `0045BF50` + 0x45 with the original `rcx` and returns 1 | Interior anchor `0045BF60`; Interior anchor `0045BF72`; Interior anchor `0045BF81`; Interior anchor `0045BF8F`; Interior anchor `0045BF95` | [CONTRACT-boot-fixups](../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md) |
| `0045C920` | 87 B | `002F3BC0` + 0x1F5 | calls `0045C920` + 0x9 with `rcx` unchanged and, when it returns 0 in `eax`, returns that 0; otherwise stores 0x10001 into dword `rcx+0x24C` (original `rcx`), calls `0045C920` + 0x2C and `0045C920` + 0x37 with no arguments set, storing their `eax` into dwords `rcx+0x244` and `rcx+0x248` in that order, then calls `0045C920` + 0x45 with the original `rcx` and returns 1 | Interior anchor `0045C930`; Interior anchor `0045C942`; Interior anchor `0045C951`; Interior anchor `0045C95F`; Interior anchor `0045C965` | [CONTRACT-boot-fixups](../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md) |
| `0045D290` | 87 B | `002F3BC0` + 0x202 | calls `0045D290` + 0x9 with `rcx` unchanged and, when it returns 0 in `eax`, returns that 0; otherwise stores 0x10001 into dword `rcx+0x24C` (original `rcx`), calls `0045D290` + 0x2C and `0045D290` + 0x37 with no arguments set, storing their `eax` into dwords `rcx+0x244` and `rcx+0x248` in that order, then calls `0045D290` + 0x45 with the original `rcx` and returns 1 | Interior anchor `0045D2A0`; Interior anchor `0045D2B2`; Interior anchor `0045D2C1`; Interior anchor `0045D2CF`; Interior anchor `0045D2D5` | [CONTRACT-boot-fixups](../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md) |
| `0045DCA0` | 112 B | `002F3BC0` + 0x20C | calls `0045DCA0` + 0x9 with `rcx` unchanged and, when it returns 0 in `eax`, returns that 0; otherwise calls `0045DCA0` + 0x26 with (`rcx+0x2A0`, 0), stores 0x10001 into dword `rcx+0x2F0` (original `rcx` throughout), calls `0045DCA0` + 0x3A, `0045DCA0` + 0x45 and `0045DCA0` + 0x50 with no arguments set, storing their `eax` into dwords `rcx+0x254`, `rcx+0x258` and `rcx+0x25C` in that order, then calls `0045DCA0` + 0x5E with the original `rcx` and returns 1 | Interior anchor `0045DCB0`; Interior anchor `0045DCC6`; Interior anchor `0045DCD0`; Interior anchor `0045DCF8`; Interior anchor `0045DCFE` | [CONTRACT-boot-fixups](../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md) |
| `0045E8C0` | 112 B | `002F3BC0` + 0x216 | calls `0045E8C0` + 0x9 with `rcx` unchanged and, when it returns 0 in `eax`, returns that 0; otherwise calls `0045E8C0` + 0x26 with (`rcx+0x2A0`, 0), stores 0x10001 into dword `rcx+0x2F0` (original `rcx` throughout), calls `0045E8C0` + 0x3A, `0045E8C0` + 0x45 and `0045E8C0` + 0x50 with no arguments set, storing their `eax` into dwords `rcx+0x254`, `rcx+0x258` and `rcx+0x25C` in that order, then calls `0045E8C0` + 0x5E with the original `rcx` and returns 1 | Interior anchor `0045E8D0`; Interior anchor `0045E8E6`; Interior anchor `0045E8F0`; Interior anchor `0045E918`; Interior anchor `0045E91E` | [CONTRACT-boot-fixups](../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md) |
