---
system: A typed list, measured once and built in one allocation
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS, on SWE2-CONTRACT's reconciliation): residue reconciled 2026-09-30 (SWE2-CONTRACT, DD batch 6) - slot flag bit 7, the sub-image record's fields, the load menu's resources 111 and 127 and the image-creation calls answered from the image and existing records; EW-6 part (b) disposed SUPERSEDED by FABLE 2026-09-26; no open item is left on the page and the owner read is done; ~~why ids 3 and 6 are both empty (the open half of UQ-76) has no static reader and waits on an authored census~~ (UQ-76 answered 2026-09-22 by the authored census, closed 2026-09-25); UQ-75, UQ-77, UQ-78 answered 2026-09-17
owner_layer: none — the decoder carries no ledger owner, and a caller is not evidence of one
evidence_tier: 1
level: L1
readiness: SEMANTICALLY IDENTIFIED
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 102 addresses cited - 8 data, 32 entry, 59 interior, 3 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-30
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-typed-list-pass-1
  crossref_clean: false
  reopened_count: 0
---

# A typed list, measured once and built in one allocation

## 1. What the player sees

Almost everything FFXII shows you that was *authored* rather than computed — a menu's contents, a
panel's parts, the pieces of a composed screen — is written down as **a list of items, each of a
kind**. The engine reads that list twice: once to add up how much room the items need, and once to
build them. **Then it makes exactly one allocation** for the whole thing.

That matters for anyone changing authored content: **an item's kind decides how much space it
costs**, two of the nine kinds cost nothing at all, and the list is walked by *each item saying how
long it is* — so an item of an unknown kind is skipped safely rather than derailing the rest.

## 2. Where it sits

`002432B0` (609 B) is called by **108 distinct functions** — 36 owned by `UI` and 72 unowned —
from **113 call sites** (~~108 sites~~: five of the 108 call it twice; corrected 2026-09-13,
§9). **No document had cited it when this was written** (2026-09-08; one cites it now — §9). It carries no ledger owner; **this document is filed under the resource
pipeline because of what it does, not because of who calls it** — a caller is not evidence of
ownership.

```c
void FUN_002432B0(Out *out /*rcx*/, Owner *obj /*rdx*/, int32_t index /*r8d*/, void *ctx /*r9*/);
```

## 3. Finding the list

```asm
002432C8  mov  ecx, [rdx + 0x20]          ; an offset stored on the object
002432D1  call ImageAddress_ResolveRuntimePointer      ; arena + offset -> the TABLE
002432D6  lea  r10, [rbx + rbx*4]         ; index * 5   -> the record is 5 dwords, 20 bytes
002432DA  mov  esi, [rax + r10*4]         ; record.dword0
002432DE  mov  ecx, [rax + r10*4 + 0x10]  ; record.dword4 -- an offset
002432E3  and  esi, 0x3ff                 ; the low TEN BITS are the ITEM COUNT
002432F2  lea  ebx, [rsi*8]               ; running total starts at count * 8
002432F9  call ImageAddress_ResolveRuntimePointer      ; arena + dword4 -> the ITEM BYTES
```

**The outer table is 20-byte records**, one per index, and the record holds **a count in the low ten
bits of its first dword** (so at most 1,023 items) and **an arena offset to the item bytes in its
fifth**. Both offsets go through the same `ImageAddress_ResolveRuntimePointer` the
[authored data table registry](authored-data-table-registry.md) documents — this is the same
addressing scheme.

## 4. The walk: every item says how long it is

```asm
00243340  movzx eax, byte [r8 + 1]        ; the item's TYPE, at +1
00243345  dec eax / cmp eax, 8 / ja       ; types 1..9; anything else contributes 0
0024334E  jmp  [table at 00243514]        ; -> a size
00243379  movzx ecx, byte [r8]            ; the item's OWN LENGTH, at +0
0024337D  add  ebx, eax                   ; accumulate the size its type costs
0024337F  add  r8d, ecx                   ; advance by its own length
00243382  sub  rdx, 1 / jne               ; count times
```

**Two bytes carry the whole format.** `item[0]` is the item's byte length and `item[1]` is its type.
**Items are variable-length and self-describing**, so an unrecognised type costs zero space and the
walk still steps over it correctly.

## 5. The nine types, with their exact sizes and constructors

Both jump tables are image-base-relative and were resolved with a tool:
sizes at `00243514`, constructors at `00243538`.

> **`verify_doc_addresses` flags both as `.text` addresses inside no function, and asks for the
> context.** Here it is: the function body is `002432B0` + 609 bytes, ending at **`00243511`** — so
> **both tables sit immediately past it**, which is exactly the *"jump table after a function"* case
> the gate names as legitimate. Confirmed rather than left as an open hit.

| type | node size | constructor | constructor size |
|---:|---:|---|---:|
| 1 | `0x20` (32) | `0029ECB0` | 116 B |
| 2 | `0x40` (64) | `0029F4C0` | 177 B |
| **3** | **0** | **none** | — |
| 4 | `0x20` (32) | `0029ED40` | 9 B |
| 5 | `0x30` (48) | `0029FEB0` | 174 B |
| **6** | **0** | **none** | — |
| 7 | `0xA0` (160) | `0029F130` | 841 B |
| 8 | `0x20` (32) | `0029F930` | 264 B |
| 9 | `0x40` (64) | `0029F4C0` | 177 B |

> **Types 3 and 6 cost nothing and build nothing.** They occupy their length in the authored bytes,
> advance the walk, and produce no node at all. **They are not errors** — they take the same
> `xor eax, eax` arm the out-of-range default takes, which is why an unknown type is harmless.
>
> **Types 2 and 9 are aliases**: same size, same constructor. Nothing here says why there are two
> codes for one thing.
>
> **Type 7 is the heavy one** — 160 bytes and an 841-byte constructor, five times the next largest.

## 5b. What the types ARE — the list is a UI composition

**All six constructors have exactly one caller**, `002432B0`, so they are private to this decoder
and reading them is reading the format's vocabulary.

| type | size | constructor | what it builds |
|---:|---:|---|---|
| **1** | `0x20` | `0029ECB0` | **a 192-byte Widget**, through the factory `00244F50` with proc `0029E7D0`, stored at node `+0x18` |
| 2 | `0x40` | `0029F4C0` | **a SPRITE** — one sub-image of a named atlas, a frame index, four corner colours; drawn in the batch (§5e) |
| **3** | 0 | none | nothing at all |
| **4** | `0x20` | `0029ED40` | **9 bytes: `node[+0x18] = 0`** — occupies a node and builds nothing |
| **5** | `0x30` | `0029FEB0` | **TEXT** — see below |
| **6** | 0 | none | nothing at all |
| 7 | `0xA0` | `0029F130` | **a PERCENTAGE BAR** — two three-piece strips, a value against a maximum of 100, an optional overlay from a second atlas at a random phase (§5e) |
| **8** | `0x20` | `0029F930` | **A NESTED LIST** — recurses into the decoder |
| 9 | `0x40` | `0029F4C0` | same constructor as type 2; **drawn singly** through the float emitter `002D8D10` where type 2 is batched (§5e) |

### Type 1 — a widget

```asm
0029ECE4  mov  ecx, 0xc0                 ; 192 bytes
0029ECF1  lea  rdx, [0029E7D0]           ; the proc
0029ECF8  call 0x244f50                  ; the widget factory
0029ED0B  mov  [rdi + 0x18], rbx         ; the widget hangs on the node
```

`00244F50` is the widget factory
[the unowned-code census](../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md)
§6 reads in full. **A type-1 item is a widget of a fixed size with a fixed proc.**

### Type 5 — text, resolved through the st2e high pool

```asm
0029FED8  movzx eax, byte [rdi + 0x10]   ; an opacity/scale byte
0029FEDE  je   default                   ; 0 means "use the default"
0029FEEA  divss xmm0, [008F3134]         ;   / 100.0
0029FEF4  movss xmm0, [01CEBBA8]         ; default = 1.0
0029FEFC  movss [rbx + 0x28], xmm0

0029FF42  mov  ecx, [rdi + 0x14]         ; the STRING ID
0029FF45  cmp  ecx, -1 / je              ; -1 means no string
0029FF4A  call 0x2f9920                  ; the st2e HIGH-pool resolver
0029FF4F  mov  [rbx + 0x18], rax         ; the resolved text on the node
```

> **`002F9920` is the resolver [`EXP-002`](../_experiments/EXP-002-st2e-group-tables.md) mapped in
> a live process** — the pool whose slot `n` holds ids from `n × 10,000`. **So an authored text
> item carries a string id, and that id is looked up in the table that experiment enumerated.** The
> static format and the live table meet here.

```
opacity = (item[+0x10] == 0) ? 1.0 : item[+0x10] / 100.0     a percentage in one byte
string  = (item.dword[+0x14] == -1) ? none : st2e_high(item.dword[+0x14])
```

`item[+0x11]` is a mode byte: **`0x10` becomes `0x20` and `0x11` becomes `0x21`** at node `+0x2C`,
and any other value leaves it as copied.

### Type 8 — a list that references another list

```asm
0029F950  mov  ecx, [rdx + 0x20]         ; THE SAME table offset the outer decoder used
0029F959  movzx ebx, word [rsi + 0xc]    ; an INDEX, u16 at item +0x0C
0029F95D  call ImageAddress_ResolveRuntimePointer
0029F96A  lea  r10, [rbx + rbx*4]        ; index * 5 -- the SAME 20-byte record stride
          ... then calls 002432B0
```

> **A type-8 item names another record in the same table by index and decodes it.** Lists compose
> out of lists, which is why the decoder takes a context argument (`r9`) and why types 8 and 1 are
> the only ones that receive it.

### And it closes a loose end from §7

§7 records that the outer decoder **clears bits 6–15** of every node's `+0x08` with
`and dword [rbx+8], 0xFFFF003F`. **The constructors fill them back in.** Type 5 does it explicitly:

```asm
0029FF08  movzx eax, word [rdi + 0x12] / shl eax, 6
0029FF0F  xor  eax, [rbx + 8] / and eax, 0xffc0 / xor [rbx + 8], eax
```

`0xFFC0` is exactly the complement of `0x3F` in the low 16 bits — **the decoder clears the field
and the per-type constructor owns it.** That is a division of labour, not a discarded value.

## 5c. Types 2, 9 and 7 — a sprite out of a named UI atlas

`EV-1` asked what the remaining types are. **Types 2 and 9 are a sprite drawn from a named
texture atlas**, and the naming machinery is shared with type 7.

### The atlas is found by name, and the name is cached

`002A0060` (140 B) resolves the item's `u16` at `+0x0C` into an atlas object:

```text
[ctx + 8]  ->  ImageAddress_ResolveRuntimePointer  ->  an array of 16-BYTE name records
record = base + id * 16
    +0x00 .. +0x0D   the atlas NAME, inline, NUL-terminated
    +0x0E            1 once resolved
    +0x0F            the slot index it resolved to
```

If `+0x0E` is already 1 the cached slot is **revalidated** — the slot's own name is compared
against the record's with the same inlined `movzx`/`movzx` idiom the input name registry uses —
and only re-looked-up when it no longer matches. **The cache is checked, not trusted.**

### The registry itself is 64 slots, and it is BSS

```text
0024A5F0(i)     ->  0208F580 + i * 0x48          the slot
0024A610(name)  ->  linear scan of 64 slots, stride 0x48
                    slot + 0x00   the name, inline
                    slot + 0x38   bit 0x20 set means OCCUPIED
                    slot + 0x20   the atlas object
```

**`0208F580` is past `.data`'s raw content**, so the shipped file contains no names here — reading
it from the image returns the following section's bytes. Read from a running game at the
front-end, **21 of the 64 slots are occupied** (live read 2026-09-08, harness-launched and read-only; recorded in `_index/AUDIT-LOG.md` under *2026-09-08 — the format's vocabulary was in BSS*, commit `7593db615`; no EXP record carries it):

| | |
|---|---|
| windows and frames | `bt_win_0_c` `cm_win_c` `w_line01` `party_grd_2` `shape` |
| icons and cursors | `buttonicon` `icons_c` `cursol_4_p` `keyboard` `mini_face_c` |
| screens | `battle_4_c` `battle_4_p` `partytop_4_c` `partytop_8_c` `lic_4_c` `extra_c` `title_logo` |
| text and localisation | `s_font_c` `Loca_8_c` `LocaBack_c` |
| targeting | `targetline_p` |

> **These are the UI's texture atlases**, and they are what the typed list is composed of. The
> list decoder at `002432B0` had 36 of its 108 callers owned by `UI`; this is why.

### The sub-image is a two-level lookup on a 16-bit code

With `T = atlas[+0x20] + 0x30` and the authored code at item `+0x0E`:

```text
page  = u16[T + 0x14 + (code >> 8) * 2]
entry = u16[T + 0x14 + (page + (code & 0xFF)) * 2]
rec   = T + u16[T + 0x10] + entry * 8          an 8-byte sub-image record
```

**Validated live against three atlases** (the same 2026-09-08 read and AUDIT-LOG block). `buttonicon` has `u16[T+0x10] = 64` and code `0` lands
on `7A 00 64 00 1C C0 01 0B`; `s_font_c` and `title_logo` both have `48`. **The record's fields
are not named here** — the first two `u16`s differ per atlas and nothing read says what they are.

> *Answered 2026-09-30 (SWE2-CONTRACT, DD batch 6, `_index/candidates/swe2contract-ddres-b6-0930/` `b6_typed_list.py` S1–S4, L1; static):* the sentence above
> is superseded and kept as written. Types 2/9 (`0029F4F1`–`0029F50F`) and type 7 (`0029F176`–`0029F1B1`) index the
> same array, `T + u16[T+0x10] + entry × 8`, and type 7 unpacks each record as `u16 +0`, `u16 +2`, then two 12-bit
> fields from the dword at `+4` (bits 0–11 and 12–23, `0029F206`–`0029F22F`); byte 7 is the default opacity both
> constructors fall back to (`0029F531`, `0029F1E0`). §5e reads the four as the sub-image's x, y, width and height in
> the atlas (FABLE, from the bar drawer). The `buttonicon` example above decodes to x 122, y 100, 28 × 28, default
> opacity `0x0B`.

**Byte 7 of that record is a default the authored data can decline**: if item `+0x12` is `0xFF`
the node takes `rec[7]`, otherwise it takes `(item[+0x12] & 0xFF)`.

Then four authored dwords are copied straight across — item `+0x14` `+0x18` `+0x1C` `+0x20` into
node `+0x28` `+0x2C` `+0x30` `+0x34` — and the node ends `+0x3A = node[+0x2B]`, `+0x3B = 0x80`.

### Type 7 names TWO atlases, and the second is optional

`0029F130` (841 B) begins exactly as types 2/9 do — same `002A0060` call, result at node
`+0x28` — and then does the **whole name-resolve dance a second time** on its own `u16`, guarded
by `cmp ebp, 0xFFFF`: **`0xFFFF` means "no second atlas"**. It also sets a marker the other
constructors do not:

```asm
0029F150  or dword ptr [rcx + 0x20], 0x2000000
```

**What its remaining ~700 bytes do is not read**, so type 7 is **partially** identified: it is an
item with one required and one optional atlas reference. Naming it from that would be the tidy
story the evidence does not support.

*Superseded 2026-09-17 by §5e (UQ-75, FABLE): the rest of `0029F130` builds a percentage bar. The paragraph above is
kept as written. (Marked 2026-09-30, SWE2-CONTRACT, DD batch 6.)*

> ### A lookup that cannot report failure
>
> `0024A610` returns `eax = 0` when the name is **not found**, and `eax = r10d` on a match — and
> `r10d` starts at 0. **"Not found" and "slot 0" are the same answer.** The caller stores it as
> the cached handle and dereferences it, so **a name that is absent resolves to whatever occupies
> slot 0** (`buttonicon` in the observed run) rather than failing. That is what the code does;
> **whether any authored name is ever absent is not established.**
> *(Superseded by part (a) below, SWE2-DATA 2026-09-18: three authored names are never registered. Marked
> 2026-09-30, SWE2-CONTRACT.)*
>
> *`EW-6` narrowed 2026-09-14 (FABLE), from the only two resolve sites (`002A0060` and `0029F130`'s optional second
> atlas at `0029F370`–`0029F3DE`; `0024A610` has no other raw call site):*
>
> - **A miss is not remembered.** Both sites set the record's `+0x0E = 1` and store the returned index (0) in `+0x0F`.
>   On the next resolve the cached slot 0 is revalidated: if slot 0 is free (`+0x38` bit 5 clear) or its name differs
>   from the record's, the scan runs again. An absent name is therefore looked up on **every** resolve until some slot
>   carries it, and from then on it resolves correctly. The one exception is a name equal to slot 0's own, which is
>   not a miss.
> - **The slot handed back on a miss is not checked for occupancy.** `0024A5F0(0)` returns `0208F580` whatever its
>   bit 5 says. For types 2/9 the caller then reads `[atlas + 0x20]` (§5c), which is whatever that slot last held.
> - **`0xFFFF` is a different answer, and it is a null.** `002A0060` returns 0 for id `0xFFFF` before any lookup,
>   and type 7 stores a null second atlas at node `+0x90` (`r8` was zeroed at `0029F188`) and skips its sub-image
>   read (`0029F3E8`). The authored "no atlas" is therefore distinguishable; only a *named* miss collapses onto
>   slot 0. The first `002A0060` call in `0029F130` dereferences its result (`0029F16F`) without that test, so a
>   required atlas id of `0xFFFF` would fault there. Whether any file authors one is part of the question below.
> - **The names that can occupy a slot are not a closed static set.** `0024A4E0` is the only writer of a slot name.
>   Its ten raw call sites, and the 31 call sites of its four wrappers (`00249380`, `002493D0`, `0024A440`,
>   `0024A480`), mostly pass image literals. Those are either the 22-entry name block at `01E0C1E0`–`01E0C288`
>   (`targetline_p` … `keyboard`; read at `00280750`, `002467A0`, `00291F20`, `002A799F`, `002CF2E1`, `002CF305`,
>   `003C63D1`) or direct strings (`tuto_win_c`, `Loca_8_c`, `lic_8_c`, `handbook2_c`, `hb_tex`, …). Three kinds of
>   site do not pass a literal:
>   - `00406D48` and `004070A1` take the name from a loaded file's own row: the name at the resolved pointer, the
>     image at `+0x10`.
>   - `003C2824` formats it as `loca_%d_%d` (`00D11630`) from authored fields.
>
>   Seven `002493D0` sites are not traced to a literal here. Four load the name through a register (`00393490`
>   `[rbx-8]` beside the id at `[rbx-0x10]`, `0039354B`, `003C1DD0`, `00563010`), which may still be a static
>   table. Three load it outside the 200-byte window read (`002CBD85`, `00556541`, `0056172E`).
>
> **Still open.** (a) Whether any 16-byte name record in a shipped list file names an atlas that nothing ever
> registers, a permanent miss. The registered side includes file-supplied and formatted names, so this cannot be
> settled from the image alone; it is routed to DATA (`FABLE-REQ-SWE2-DATA-ATLAS-NAME-CLOSURE`). (b) Whether a
> present name is ever resolved *before* its atlas is registered, a transient miss. That depends on load order in
> play and is not inferred here.
>
> ***ANSWERED 2026-09-18 (SWE2-DATA), part (a): three authored names are permanent misses.*** The census walks
> **every** shipped `MRP\0` typed list — the 116 standalone `mrp_menu/*.mrp` files **and** all 228 embedded units
> inside the ten locale `packfiles/mrppack_ys.bin` packs (23 units each, 21 in `in_sdver`), each unit sliced at the
> next unit offset — decodes the name array at `[+0x08..+0x10)` (16-byte records; bounds consistent in all 344
> blobs, zero malformed files), walks all 7,665 outer records' 30,546 self-sized items, and resolves every type-2/9/7
> atlas index. Reproducible sheet: [`members/atlas-name-census.tsv`](members/atlas-name-census.tsv) via
> [`gen_atlas_name_census.py`](members/gen_atlas_name_census.py).
>
> - **20,459 atlas references resolve to 28 distinct names; zero indices are out of bounds and zero required
>   `+0x0C` ids are `0xFFFF`** — the unguarded-deref path in `0029F130` can never fire on shipped data. All 20
>   standalone-file type-7 items carry `+0x40 = 0xFFFF` (no second atlas); pack unit 01's 258 type-7s author
>   `+0x40 = 0x0001` (`battle_4_c`, same as the required id).
> - **25 names are registered literals** — covered by the `01E0C1E0` block, the `00D231C0`/`00393460`-family
>   static tables, or direct wrapper-call-site strings: `battle_4_c`, `battle_4_p`, `buttonicon`, `cursol_4_p`,
>   `dataface_c`, `extra_c`, `gameover_c`, `hand_4_c`, `icons_c`, `itemgra_c`, `keyboard`, `lic_4_c`,
>   `lic_b_4_c`, `lic_b_8_c`, `map_gra_c`, `medal_c`, `mini_face_c`, `partytop_4_c`, `partytop_8_c`, `q_img_c`,
>   `q_under_c`, `s_font_c`, `shop_8_c`, `title_logo`, `w_icon_p`. The seven sites the narrowing left untraced
>   all resolve to literals (`0056172E` → `lic_8_c2`; `00556541` → `lic_4_c`; `002CBD85` → `shop_8_c`;
>   `00393490`/`0039354B`/`003C1DD0`/`00563010` → record tables that are themselves literal arrays at
>   `00D11C88`, `00D23628`, `00D23668`, `00D237E0`, `00D23D80`, `00D231C0`, `00D23250`).
> - **0 names come from the file-row path** — `00406D48`/`004070A1` read rows out of `0051EDC0`'s four resource
>   objects, which `00280980` fills with **mrppack units 13–16**; the row table is header `+0x24` count /
>   `+0x28` offset / 12-byte rows with the name at `row+8` (`002A00F0` relocates `row+8` table-relative). Every
>   shipped unit 13–16 in all ten packs has `+0x24 = 0` — the path is real but **authored-empty**.
> - **0 names match `loca_%d_%d`** — no authored name takes the formatted-locale shape `003C2824` produces.
> - **3 names have no registration anywhere: `logo_s_c`** (`e3_logo.mrp`, 10 locales), **`nowload_c`**
>   (`nowload.mrp`, 10), **`title_c`** (`title.mrp` + `title_fore3.mrp`, 16 files). Items reference them;
>   no literal, table, row or format supplies them, and `0024A610`'s byte-exact scan finds nothing — every
>   resolve permanently misses onto slot 0.
>
> Supplementary: the arrays declare 48 distinct names but items reference only 28 — 20 names are authored yet
> never indexed (including `faceunder` in mrppack units 14/15, `window_8_c`, `sort_cha_c`, and the lowercase
> `loca_8_c`/`locaback_c`, which would miss `0024A610`'s case-sensitive compare against the registered
> `Loca_8_c`/`LocaBack_c` if any item ever indexed them). Part (b) — a *transient* miss before registration —
> remains a load-order question, not inferred here.
>
> *Disposed 2026-09-26 (FABLE, register row EW-6, SUPERSEDED under the runtime rule): part (b) is a load-order
> observation on a tier-1 mechanism and is not queued. One precision, static (SWE2-CONTRACT 2026-09-30, `b6_typed_list.py` R1):
> the name record's cache heals on its next resolve, but a node built on a miss keeps the slot it was given (node
> `+0x18` for types 2/9, `+0x28` for type 7) until its list is decoded again. `002A0060`'s only callers are the two
> constructors and `001D7150` (which resolves items of its own list), and no list drawer calls `002A0060` or
> `0024A610`.*

## 5d. The file the list lives in, and how its atlases are filled — 2026-09-13

*FABLE, reviewing ASTRA's [spawn page §23](../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)
(`ASTRA-REQ-FABLE-LOAD-MATERIALIZATION`); every address re-read from the image. It connects §3's `obj` and §5c's
`ctx` to a loaded file.*

**`obj` is a loaded resource buffer, and both of its lookups use it.** The save/load controller's resource setup
`00582790` requests resource **111** (kind 7) through `003933F0` into its `+0x108`; `00583040` passes that buffer in
the constructor locals of `0057EDB0` (`00583181`–`005831A3`), whose message 1 hands it to `002432B0` as `obj`
(`0057EE3A`–`0057EE57`). Inside `002432B0`, `obj` (`r14`, `002432CE`) is both the table source (`[obj + 0x20]`,
§3) and the `rdx` given to each item constructor (`0024344B`…), which for types 2/9 becomes `002A0060`'s `ctx` —
so §5c's `[ctx + 8]` is the same file's `+8`.

**The file is relocated once, on load.** The resource member callback `00249660` passes the buffer to `002A00F0`,
which returns at once when byte `+3` is 1, and otherwise rewrites four file-relative references into the
engine's encoded image addresses (`RuntimePointer_EncodeImageAddress` `0020E620` subtracts the low 32 bits of
`01F83530`; `ImageAddress_ResolveRuntimePointer` `0020E600` adds them back to the full base), then sets byte `+3 = 1`:

| header field | origin added before encoding | what reads it |
|---|---|---|
| `+0x08` | the buffer | `002A0060`: 16-byte atlas-name records (§5c) |
| `+0x20` (`002A1A80`), count `+0x1C` | the buffer | `002432B0`: the 20-byte outer records (§3) |
| each outer record `+0x10` | **that record's own address** (`002A1AC3`–`002A1AD9`) | `002432B0`: the item bytes (§3) |
| `+0x28`, count `+0x24` | the buffer | the file-row atlas registration table: `00406D48`/`004070A1` walk it through `0051EDC0`'s four resource objects (mrppack units 13–16, stored by `00280980`); rows with tag `+0x00 == 1` register through `0024A440` with flags `2`, name = resolved `row+8`, image string at name `+0x10`; **every shipped unit has count 0** — authored-empty |
| each `+0x28` row `+0x08` (12-byte rows) | **the table's base**, not the row (`002A0141`–`002A0150`) | the row's atlas-name string; the image string follows 16 bytes later (`00406D31`/`0040708A`, `rcx = name + 0x10`) |

So the file stores its item offsets relative to their own record and the second table's offsets relative to that
table — a modder moving records must respect both origins. Both counts are compared unsigned; outer-record indices are
sign-extended from 32 bits (`002A1AC0`). Nothing checks an offset or count against the file size, and calling
`002A1A80` alone skips the byte-`+3` guard.

**An atlas slot is a partial reset, then a prepared image.** `0024A4E0(name, flags)` scans the 64 × `0x48` registry
(§5c) for `+0x38` bit 5 clear, four slots per iteration; all busy returns 0. It copies the name up to its NUL with no
length check (a null name zeroes `+0x00`/`+0x08`), sets `+0x38 = (old & 0x3FF10) | (flags & 0xF) | 0xA0` — bit 5
occupied, bit 7 set, bit 6 cleared — zeroes `+0x28` and `+0x40`, and counts in `02090780`. The rest of the record is
not cleared. The image member callback `00249670` then calls `0024A1D0(slot, buffer)`: with `H = buffer + 0x10` it
stores the buffer at `+0x18` and **`H` at `+0x20`** (so §5c's `T = atlas[+0x20] + 0x30` is `buffer + 0x40`), copies
header bits 20–25 of `[H+0x18]` into flags bits 8–13 (the format) and bits 51–54 into bits 14–17, formats the slot's
name as `%s` or, when `+0x40` is non-zero, `%s%03d` (`009153E4`), stores `00181520(slot)` at `+0x44`, and prepares
format `0x13` (`00181250`, `00181000`) or `0x14` (`00181190`, `00180E70`, with an allocation through `0036A190`);
**every returning path then sets bit 6** (`0024A427`), so bit 6 does not show that a format arm ran. The request
router's shared fullscreen arm clears bit 7 of five named slots and the fullscreen widget's message 18 sets it again
([request router](../16-UI/Request-Router/ui-request-router.md) §2); what bit 7 gates is not read.

*Answered 2026-09-30 (SWE2-CONTRACT, DD batch 6, `_index/candidates/swe2contract-ddres-b6-0930/` `b6_typed_list.py` B1–B8, E1–E3; static): bit 7 puts an
atlas in the texture-memory layout pass.* `0024A710(k)` walks slots 0 to 62 (63 iterations from `0208F5B8`, stride
`0x48`; slot 63 is never visited) and takes a slot only when its flags hold bits 5, 6 and 7 and the caller's bit `k`
(`mov ebx, 0xE0` / `bts ebx, ecx`, then `and` / `cmp` / `jne` at `0024A793`–`0024A799`). For each one it reads the
image's width and height (`H+0x14`, `H+0x16`), queues its transfers through `0024AF50` from a running base that starts
at `0x3520`, and stores a packed texture descriptor at slot `+0x30` (`0024A99C`). The sprite emitter `002D9380` reads
that descriptor and the format bits from the node's slot (`002D944A`, `002D946D`, `002D948D`; the drawer passes node
`+0x18` at `002437B9`). An atlas whose bit 7 is clear is left out of the next layout pass. Its eight direct call sites
pass `k` = 1 (six sites), 0 (`0025290D`) or 2 (`00252965`). Every immediate write of the bit in `0027F5D0`–`002D7600`
(29 sites) follows a `0024A5A0` find-by-name, which returns null on a miss (`0024A5E4`), unlike `0024A610`. So the
fullscreen arm that clears bit 7 of five named atlases drops them from the layout until message 18 sets it again
(the fullscreen proc's arm at `0027F7DA`, or the config screen's `00281E00`; `00280DE0` and `002D70F0` also clear
some of the five — per `auditspec-review-ddres-b6-0930`).
**Not claimed:** what `0024AF50` emits, when the layout pass runs relative to a draw, or that no other code reads the
bit. The sweep sees immediate operands only, and `0024A710` itself reads the flags through a register mask.

For the load menu, the image request is resource **127** named **`dataface_c`** (`00D23D80`, `00D23EB8`) — an atlas
name of the same family as the front-end's `mini_face_c` (§5c's live table). **Not established:** which archive files
indices 111 and 127 are, what table B holds, and what the native image-creation calls do.

*Answered 2026-09-30 from existing records (SWE2-CONTRACT, DD batch 6; the sentence above is kept as written):*
- *Resources:* kind 7 id 111 is `in\Mrp_Menu\save_load.mrp` and id 127 is `in\Tm2_Menu\DataFace_c.tm2`, a TIM2
  image. They come from SWE2-DATA's path-array reader `kind7.py` (`_index/candidates/rc22-34-resource-readers-0930/`,
  commit `1261e2044`), re-run in `b6_typed_list.py` K1–K3. The control is id `0xBF`, `Loca.mrp`, which the cl2 page traces.
- *Table B:* the `+0x28` file-row registration table in the table above (SWE2-DATA 2026-09-18). It is authored-empty in
  every shipped unit.
- *Image creation:* the format-`0x13` and format-`0x14` arms are traced to their native boundary in
  [spawn placement §23.4](../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) (ASTRA). There,
  `00181250` and `00181190` round the dimensions up to a power of two and call `00184140` / `00183EE0`, then
  `001B21D0`, and `00181000` / `00180E70` feed the colour table in groups through `0017F3B0`.
  [The cl2 page](PS2-Image-Data-Formats/cl2-menu-colour-tables.md) (RC-30, 2026-09-30) establishes that `0017F3B0`
  builds each palette row as a texture of the `RGBA8` format object. The graphics-device calls below those stay
  separate native boundaries, as §23.4 states.

## 5e. What the drawers say: sprites, a bar, and the record's other dwords — 2026-09-17 (FABLE)

The constructors are private to the decoder, but the **nodes are read by the two list drawers next to it**,
`002435C0` and `00243C00`, which walk the node array at list `+0x10`, skip nodes whose `+0x8` bit 0 is
clear, and dispatch on the type nibble (`+0x8` bits 2..5): 2 to a batched sprite run, 4 to `0029ED30` (a
`jmp` through node `+0x18`), 5 to the text drawer `0029FBD0` (`002435C0` only), 7 to `0029ED50`, 9 to
`0029F5D0`. The third reader, `00243860`, handles type 5 alone. Ids 1, 3, 6 and 8 have no drawer arm.

### Types 2 and 9 are one sprite node, drawn two ways

| node | from | meaning |
|---|---|---|
| `+0x18` | item `u16 +0xC` via `002A0060` | the atlas |
| `+0x20` | item `u16 +0xE` | the 8-byte sub-image record (§5c lookup) |
| `+0xA` | item `u16 +0x10` | a frame index; the drawers read the record `+0xA` records on from `+0x20` |
| `+0x39` | item `u16 +0x12`, or byte 7 of the indexed record when it is `0xFF` | opacity; two nibbles, the high one indexes a per-atlas byte table (`0024374E`..`0024377D`) |
| `+0x28`..`+0x37` | item `+0x14`..`+0x23` | **four corner colours, RGBA** — `002D9380` unpacks them byte by byte into four vertices (`002D95CE`, `002D9618`, and on) |
| `+0x3A`, `+0x3B`, `+0x38` | first colour's fourth byte, `0x80`, `0` | |

Type 2 nodes are emitted in a run: `002D9C40` opens it, `002D9380` takes each node, and the inner loop
continues while the next node's nibble is still 2 (`002437D8`..`002437F0`); `002D9B00` closes it. A type
9 node is emitted alone by `0029F5D0` through the float-coordinate emitter `002D8D10`, with the widget's
`+0x5A` word saved, zeroed for the call and restored (`00243651`..`00243670`). **That is the whole
difference: 9 is a sprite drawn individually.**

### Type 7 is a percentage bar

`0029F130` fills the node with one atlas (`+0x28`) and **two strips of three sub-images each** — item
`u16 +0x18`/`+0x1A`/`+0x1C` and `+0x2C`/`+0x2E`/`+0x30`, each record unpacked as `{u16 x, u16 y, w:12,
h:12}` into `+0x4C`..`+0x63` and `+0x68`..`+0x7F` (`0029F202`..`0029F368`) — with an opacity byte
(`+0x44`, `+0x45`), a `u16` (`+0x48`, `+0x4A`) and a colour word (`+0x64`, `+0x88`) per strip. It sets a
**value at `+0x18` to 0 and a maximum at `+0x1C` to 100**. The optional second atlas (item `+0x40`,
`0xFFFF` = none, §5c) carries one sub-image (item `+0x42`), an opacity (`+0x46`), a colour (`+0x98`) and a
**random start phase**: `+0xA` = `rand()` (IAT `008C3098`, the CRT) modulo the sub-image's width
(`0029F437`..`0029F453`).

The drawer `0029ED50` clamps the value into the range 0..maximum (`0029ED98`..`0029EDA3`) and hands each
strip to `002A0180` with that length: the left cap at the origin, the middle stretched to the length less
the cap (`002A0212`..`002A0249`), the right cap at the end (`002A024E` on). Two strips drawn to a value
against 100 is a gauge; **which gauge an authored item is, only the files say.** No type-checked writer of
`+0x18` exists (`002482E0`, the release, is the only code that singles out 7); the value is set by index.

### The outer record's other dwords (UQ-77) and the four copied words (UQ-78)

The builder returns the record itself (`002434FB`). **87 of its 110 callers** copy `u16 +4`, `+6`, `+8`,
`+0xA` into their widget's `+0x98`, `+0x9A`, `+0x9C`, `+0x9E` (`0029E7FC`..`0029E828` is the pattern), the
fields the [widget contract](../16-UI/Widget-Object-Model/CONTRACT-widget-object.md) shows holding
`0x200`/`0x1C0` at `+0x9C`/`+0x9E`: **dwords 1 and 2 are x, y, width, height.** Dword 3 has one reader,
`002BF3D0`: it builds a throwaway `0xC0` widget, decodes the list into it, copies the 20-byte record to its
caller's buffer, stores dword 3 in `01E0CE88` and destroys the widget (`jmp 00245020`). `002BE0A0` calls
it for lists 0, 1 and 8; the four readers of `01E0CE88` (`002BDE62`, `002BDF52`, `002BE5E0`, `002BE75D`)
add it to a y coordinate or to an offset accumulated in `01E0CE98`: **a vertical placement offset.** The
copied records themselves are read back by nothing in the UI ranges. **Bits 10..27 of dword 0 reach
nothing**: the builder consumes bits 0..9 and bit 28, and no caller reads the first dword again.

The four copied words are **x, y (signed) and width, height (unsigned)**: the type-2 drawer passes them
sign- and zero-extended as the emitter's stack arguments (`00243787`..`002437B4`), the type-9 drawer
converts them to floats (`0029F63B`..`0029F671`), the text handler adds `+0xC`/`+0xE` to its run origin
and compares `+0x12` with the measured height (`00243978`..`002439A5`), the bar drawer takes `+0xC`/`+0xE`
as its origin (`0029ED78`).

*Count note (SWE2-CONTRACT, 2026-09-30, `b6_typed_list.py` C1):* `002432B0` has 113 direct call sites in 108 functions, the
figures §2 and §9 give. The "110 callers" above is FABLE's count and states no unit, so the 87 is not re-derived here.

## 6. One allocation for the pointers and the nodes together

The running total **starts at `count * 8`** and then adds each item's size, so a single block holds
**both the pointer array and every node**:

```
total = count * 8  +  sum over items of size[type]

if total == 0:  out->list = NULL and nothing is built
else:           out->list = alloc(total)              (002497B0)
                the first count*8 bytes are the pointer array
                the nodes follow, packed in walk order
```

**A list whose every item is type 3 or 6 still allocates `count * 8`** — the pointer array exists
even when nothing is built for it to point at.

## 7. What each node carries from the authored item

```asm
002433EB  mov  [rbx], rdi                 ; +0x00  the authored item's own address
002433E8  mov  [rbx + 8], edx             ; +0x08  (overwritten immediately below)
002433EE  mov  ecx, [rdi] / shr ecx, 6 / and ecx, 0x3C
002433F6  mov  [rbx + 8], ecx             ; +0x08  bits 2..5 from item.dword0 bits 8..11
002433FB  shr  eax, 0x1C / xor / and 1 / xor
00243405  mov  [rbx + 8], eax             ; +0x08  bit 0 = item.dword0 bit 28
00243424  mov  [rbx + 0xa], dx            ; +0x0A  the item's index in the list
00243428  and  dword [rbx + 8], 0xFFFF003F
0024340C  mov  [rbx + 0xc], ax            ; +0x0C  u16 item[+0x04]
00243414  mov  [rbx + 0xe], ax            ; +0x0E  u16 item[+0x06]
0024341C  mov  [rbx + 0x10], ax           ; +0x10  u16 item[+0x08]
0024342F  mov  [rbx + 0x12], ax           ; +0x12  u16 item[+0x0A]
```

**Four `u16` fields are copied straight across** from item `+0x04`, `+0x06`, `+0x08`, `+0x0A` into
node `+0x0C`, `+0x0E`, `+0x10`, `+0x12`. The `+0x08` dword is a **packed flags word**, assembled
with the `x ^ ((x ^ v) & mask)` bitfield-insert idiom and then masked with `0xFFFF003F`, which
**clears bits 6–15** — so bits 6–15 of that word are deliberately not carried over.

The same idiom builds `out->flags` at the top of the function: **bits 2–17 hold the count**, bit 1
is set unconditionally, and **bit 0 is copied from bit 28 of the outer record's first dword**.

## 7b. Key addresses (SWE2-CONTRACT, 2026-09-30)

*Collected from §2–§7 for the DD owner read. Each row is read in the section named, or pinned in `b6_typed_list.py`.*

| address | role | where read |
|---|---|---|
| `002432B0` | the decoder: measure, allocate once, build | §3–§7 |
| `00243514` / `00243538` | the size and constructor jump tables | §5 |
| `0029ECB0`, `0029F4C0`, `0029ED40`, `0029FEB0`, `0029F130`, `0029F930` | constructors for types 1, 2/9, 4, 5, 7, 8 | §5b, §5e |
| `002497B0` | the single allocation (`002433A5`) | §6 |
| `002A0060` | resolves an item's atlas-name record to a slot, cached and revalidated | §5c |
| `0024A610` / `0024A5F0` | the slot scan (a miss returns index 0) and index-to-slot | §5c |
| `0024A5A0` | find a slot by name (a miss returns null); used by every bit-7 writer | §5d, B7–B8 |
| `0024A4E0` | registers an atlas name in a free slot | §5d |
| `0024A1D0` | binds a TIM2 buffer to a slot (header at `+0x20`, formats `0x13` / `0x14`) | §5d |
| `0024A710` | the texture-memory layout pass over slots with bits 5, 6, 7 and `k` | §5d, B1–B6 |
| `0208F580` | the 64-slot atlas registry (BSS, stride `0x48`); `02090780` its count | §5c |
| `00249660` / `002A00F0` / `002A1A80` | the list file's completion callback and relocator | §5d |
| `00249670` | the image completion callback, calls `0024A1D0` | §5d |
| `002435C0`, `00243C00`, `00243860` | the list drawers | §5e |
| `002D9C40` / `002D9380` / `002D9B00` | the sprite run: open, emit, close | §5e, E1–E3 |
| `0029ED50` → `002A0180` | the bar drawer and its strip drawer | §5e |
| `0029F5D0` → `002D8D10` | the single-sprite (type 9) drawer and the float emitter | §5e |
| `002482E0` | the release (singles out type 7) | §5e |

## 7c. Call chain (SWE2-CONTRACT, 2026-09-30)

*Edges re-read with `retool.py callers` at the time of writing; the load-menu path is §5d's.*

```text
load:    00582860 -> 00582790 -> 003933F0 -> 00249320 (kind 7 id 111, completion 00249660 -> 002A00F0 -> 002A1A80)
                              -> 00393460 -> 002493D0 -> 0024A4E0 (register 'dataface_c')
                                                     (id 127, completion 00249670 -> 0024A1D0)
build:   00583040 -> 0057EDB0 (message 1) -> 002432B0 -> 002497B0
                                                     -> constructors (00243538) -> 002A0060 -> 0024A610 / 0024A5F0
                                                                                 -> 0029F930 -> 002432B0 (nested)
draw:    002435C0 / 00243C00 -> 002D9C40, 002D9380, 002D9B00 (type 2); 0029ED30 (4); 0029FBD0 (5); 0029ED50 (7); 0029F5D0 (9)
layout:  0022B0B0 / 0022B6E0 / 0022B7E0 / 0022B8C0 / 0022BC20 / 001D72F0 -> 00252840..00252A70 -> 0024A710 -> 0024AF50
release: 002482E0
```

`002432B0` has 108 calling functions (§9). The table shows the load-menu instance only. One further reader of the
list bytes bypasses the decoder: `001D7150` (called from `0017F770`) takes a list file from `0027E9D0` and resolves the
atlases of its items with `002A0060` itself.

## 8. Modding notes

- **An item's type decides its cost**, and the table in §5 is exact. Changing a type changes the
  allocation size, and the engine recomputes it — there is no stored size to keep in sync.
- **Items are self-describing.** `item[0]` is the length. Get that wrong and the walk desynchronises
  for every item after it; get the *type* wrong and only that item is affected.
- **Types 3 and 6 are free.** They are the safe way to leave a placeholder in an authored list.
- **The count is ten bits — at most 1,023 items.** Bits 10–27 of the record's first dword are read by
  nothing (§5e); bit 28 of it reaches the output flags.
- **Bits 6–15 of each node's `+0x08` are cleared** whatever the authored bytes said.

## 9. What is not known

- [x] **What the list is a list *of*** — **§5b, 2026-09-08.** A **UI composition**: widgets,
      text resolved through the st2e high pool, and nested lists.
- [x] ~~**UQ-75.** **What types 2/9 and 7 build.** `0029F4C0` (via `002A0060`) and `0029F130` (841 B, the~~
      160-byte type) are **still unidentified** — two of the nine. `EV-1`.
      ***ANSWERED 2026-09-17 (FABLE): types 2 and 9 build a sprite node; type 7 builds a percentage bar.** Types 2/9 (`0029F4C0`, node `0x40`): `+0x18` the atlas from item `u16 +0xC` through `002A0060`; `+0x20` the 8-byte sub-image record for item `u16 +0xE` (the §5c lookup); `+0xA` a frame index from item `u16 +0x10`, by which the drawers index further records from `+0x20`; `+0x39` an opacity byte from item `u16 +0x12` or, when that is `0xFF`, byte 7 of the indexed record; `+0x28`..`+0x37` four `u32` from item `+0x14`..`+0x23`, with `+0x3A` the fourth byte of the first, `+0x3B = 0x80`, `+0x38 = 0`. The sprite emitter `002D9380` unpacks those four words byte by byte into four vertices (`002D95CE`, `002D9618`, and on), so they are **four corner colours, RGBA**. Type 7 (`0029F130`, node `0xA0`): the same atlas at `+0x28`, then **two strips of three sub-images each**, item `u16 +0x18`/`+0x1A`/`+0x1C` and `+0x2C`/`+0x2E`/`+0x30`, each record unpacked as `{u16 x, u16 y, w:12, h:12}` into `+0x4C`..`+0x63` and `+0x68`..`+0x7F`, each strip with an opacity byte (`+0x44`, `+0x45`), a `u16` (`+0x48`, `+0x4A`) and a colour word (`+0x64`, `+0x88`); a **value at `+0x18` (built as 0) against a maximum at `+0x1C` (built as 100)**; and an optional second atlas at `+0x90` (item `u16 +0x40`, `0xFFFF` = none) whose sub-image (item `+0x42`) gets an opacity at `+0x46`, a colour at `+0x98` and a **random start phase**: `+0xA` = CRT `rand()` (IAT `008C3098`) modulo the sub-image's width (`0029F437`..`0029F453`). Its drawer `0029ED50` clamps the value to the range 0..max (`0029ED98`..`0029EDA3`) and hands each strip to `002A0180`, which draws the left cap, a middle stretched to the value and the right cap. That is the shape of a gauge; which gauge each authored item is, the files say. Static, constructors and drawers read.*
- [x] **UQ-76.** ~~**Why types 2 and 9 are aliases**, and why 3 and 6 both mean "nothing".~~ **ANSWERED — both halves,
      closed 2026-09-25 by FABLE (Claude Opus 5.5) after re-running the census; the answers are FABLE's 2026-09-17
      (2/9) and SWE2-DATA's 2026-09-22 (3/6), which never reached this box.**
      - **2 and 9:** they share a constructor but not a drawer. 2 is a batched sprite run (`002D9380`); 9 is a
        sprite emitted alone through the float-coordinate emitter `002D8D10`.
      - **3 and 6:** neither reaches a constructor, drawer or release arm. In the shipped corpus type **6**
        occurs 46 times, always a type-5-shaped text record whose string id is `0xFFFFFFFF`: a text slot the
        authoring tool blanked. Type **3** never ships, and neither does type 9.
      - The census, recounted from [`members/listtype-census.tsv`](members/listtype-census.tsv) and
        [`members/listtype-census-embedded.tsv`](members/listtype-census-embedded.tsv): 344 units, every walk
        clean, types {1: 2661, 2: 20181, 4: 2017, 5: 4484, 6: 46, 7: 278, 8: 879}.
      ***PARTIAL 2026-09-17 (FABLE): the 2/9 half is answered; the 3/6 half has no reader to ask.** Types 2 and 9 share a constructor but not a drawer. The list drawers `002435C0` and `00243C00` dispatch on the node's type nibble (`+0x8` bits 2..5): type 2 opens a sprite run (`002D9C40`) and emits consecutive type-2 nodes in one batch through `002D9380` until the next node's nibble differs (`002437D8`..`002437F0`), while type 9 is emitted alone through the float-coordinate emitter `002D8D10` (`0029F5D0`), with the widget's `+0x5A` word swapped out for the call. So 9 is a sprite drawn individually and 2 a sprite drawn in the batch. Ids 3 and 6 reach no constructor arm (the `00243449` table sends both to `0024349F`), no drawer arm (2, 4, 5, 7, 9 in `002435C0`; 2, 4, 7, 9 in `00243C00`; 5 alone in `00243860`) and no release arm (`002482E0` singles out 7 only). Nothing in the image tells them apart, so why the format carries two empty ids is not a static question; whether shipped files use either is routed to DATA (`FABLE-REQ-SWE2-DATA-LIST-TYPE-ID-CENSUS`).*
      ***NARROWED 2026-09-18 (FABLE), authored data: the lists are the twelve `MRP` files, and the record's bits 10..27 are its own index; whether 3 or 6 occur is not settled.** Resource 111 (kind 7) is `mrp_menu/save_load.mrp` (2,848 bytes, `FileSizeTable_US.fst` row 7 entry 111, one file of that size under the menu root), a file whose magic is `MRP` and whose header carries the outer count at `+0x1C` (9) and the outer table at `+0x20` (`0x30`); the twelve `.mrp` files under `myoshiok/us/mrp_menu` share the layout, 149 outer records in all. In every one of the 149 records the first dword's bit 28 is set and its bits 10..27 hold the record's own index (0, 1, 2, ... in each file), so the field the engine never reads is an index the authoring wrote. The item walk could not be reproduced from the files alone: taking the fifth dword as an offset from any fixed base walks at most 57 of the 149 records cleanly, so the item bytes are addressed through the runtime arena (`ImageAddress_ResolveRuntimePointer`) in a way the file does not state, and the type census that would settle 3 and 6 waits on that resolution. DATA from the archive.*
      ***CENSUS 2026-09-18 (SWE2-DATA, [listtype-census.tsv](members/listtype-census.tsv) via [gen_listtype_census.py](members/gen_listtype_census.py)): types 3 and 6 never ship — and neither does 9.** The arena resolution turned out not to be needed: the item bytes are a **contiguous stream starting at the end of the outer table**, each item `{u8 length, u8 type}` self-sizing, and walking `sum(count)` items lands on the `+0x08` items-blob-end offset within a zero pad of 0/4/8/12 bytes in **all 116 shipped `.mrp` files** (every locale's `mrp_menu` set, 1,458 outer records, 5,223 items — the gaps are all-zero alignment, never overshot). Type histogram: **{1: 265, 2: 3093, 4: 20, 5: 1483, 7: 20, 8: 342}** — no 3, no 6, and no 9 anywhere in the standalone set, so the batch-drawn sprite (2) is the only sprite the `mrp_menu` files author. *Corrected 2026-09-20 (SWE2-DATA, `AUDITSEM-CONTRA-DATA-LISTTYPE-TYPE6-MRPPACK`): the "no shipped file" conclusion was scoped to the 116 standalone files. Over the wider corpus — the same 116 `.mrp` plus all 228 embedded `mrppack_ys.bin` units (the 344 blobs the atlas-name census walks; type histogram {1: 2661, 2: 20181, 4: 2017, 5: 4484, 6: 46, 7: 278, 8: 879}) — **type 6 does ship: 46 items — one in pack unit 01 (all ten packs) and four in unit 21 (the nine 23-unit packs; `in_sdver` ships 21 units and has no unit 21)** (`#unit01` at e.g. `+0x1150`, `#unit21` at `+0x6F2C`/`+0x6FE8`/`+0x70A4`/`+0x7160`). With no constructor/drawer/release arm reading type 6, those items are **authored-but-inert** — only **type 3 is truly absent corpus-wide**, and type 9 remains absent everywhere too.* *Read 2026-09-22 (SWE2-DATA, [listtype-census-embedded.tsv](members/listtype-census-embedded.tsv) via [gen_listtype_census_embedded.py](members/gen_listtype_census_embedded.py)): all 46 type-6 items are 0x18 bytes in the **type-5 text shape** — `{s16 x,y; u16 w,h; u32 colour 0x80808080; u8 0x64 opacity; 3 zero pad bytes; u32 stringId = 0xFFFFFFFF}` — i.e. **a text item authored with no string** (`+0x14 = −1`, the type-5 "no string" sentinel). Type 6 is the compiler's disabled-text placeholder: it occupies its length, advances the walk, and could draw nothing even if a constructor existed. That explains why the vocabulary carries two empty ids — 6 is authored (a blanked text slot), 3 is not authored anywhere.* `max (dword0 >> 10) & 0x3FFFF` = **59** (the 60-record `party_book` index), consistent with the index reading. One correction to the narrowing above: bit 28 is **not** set in every record — 55 of 1,458 records carry it clear, all in `party_book` (records 5, 25, 28, 40 — including `us`), `title` (record 3) and `title_fore3` (record 3); the flag is a per-record authored choice, not a constant. Authored-data census, reproducible.*
- [x] ~~**What `[obj + 0x20]` is** — the offset that finds the outer table.~~ **Answered 2026-09-13 (§5d):** `obj` is a
      loaded list file; `+0x20` is its header's outer-table reference (count at `+0x1C`), made an encoded image
      address by `002A1A80` when the file is prepared; each record's `+0x10` is relative to that record.
- [x] ~~**UQ-77.** **What bits 10–27 of the outer record's first dword hold**, and the other three dwords of it.~~
      ***ANSWERED 2026-09-17 (FABLE): dwords 1 and 2 are the owning widget's rectangle, dword 3 a placement offset, bits 10..27 unread.** The builder returns the record (`002434FB`, `rax = r12`), and 87 of its 110 callers copy `u16 +4`, `+6`, `+8`, `+0xA` into their widget's `+0x98`, `+0x9A`, `+0x9C`, `+0x9E` (`0029E7FC`..`0029E828` is the pattern), the fields the widget contract shows holding `0x200`/`0x1C0` at `+0x9C`/`+0x9E`: **x, y, width, height**. Dword 3 has one reader, `002BF3D0`, a peek that builds a throwaway `0xC0` widget, decodes the list into it, copies the 20-byte record to its caller's buffer, stores dword 3 in `01E0CE88` and destroys the widget (`jmp 00245020`); `002BE0A0` calls it for lists 0, 1 and 8, and the four readers of `01E0CE88` (`002BDE62`, `002BDF52`, `002BE5E0`, `002BE75D`) add it to a y coordinate or to an accumulated offset in `01E0CE98`, a vertical placement. The three copied records are read back by nothing in the UI ranges. Dword 0: the builder consumes bits 0..9 (the count) and bit 28, and no caller reads the record's first dword again, so **bits 10..27 reach nothing**. Static.*
- [x] ~~**UQ-78.** **What the four copied `u16` fields mean.**~~
      ***ANSWERED 2026-09-17 (FABLE): x, y (signed) and width, height (unsigned).** The type-2 drawer passes node `+0xC` and `+0xE` sign-extended and `+0x10`, `+0x12` zero-extended as the emitter's stack arguments (`00243787`..`002437B4`, into `002D9380`); the type-9 drawer converts the same four to floats for `002D8D10` (`0029F63B`..`0029F671`); the text handler adds `+0xC`/`+0xE` to its run origin and compares `+0x12` with the measured height (`00243978`..`002439A5`); the bar drawer takes `+0xC`/`+0xE` as its origin (`0029ED78`). So item `+4`/`+6` are a signed position and `+8`/`+0xA` an unsigned size, in the owner widget's space.*
- [x] ~~**UQ-79.** **Any runtime observation.** None exists.~~ **SUPERSEDED** (2026-09-14, FABLE; EVIDENCE-STANDARD
  addendum 2026-09-15bk, kind (c)). Every mechanism claim in §10 is tier 1 and PROVEN. The one UNKNOWN, what the types
  *mean*, is its own question on this page and would not be settled by observing the list being built.

## 10. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| ~~108 call sites, 36 UI-owned~~ 108 calling functions (113 call sites), 36 UI-owned | `edges.tsv` with EH callers excluded, grouped by owner | 1 | PROVEN |
| the outer record is 20 bytes | `lea r10, [rbx + rbx*4]` then `[rax + r10*4]` — index × 5 dwords | 1 | PROVEN |
| the count is the low 10 bits | `and esi, 0x3ff` | 1 | PROVEN |
| items are self-describing, length at `+0`, type at `+1` | `movzx eax, [r8+1]` dispatches; `movzx ecx, [r8]` advances | 1 | PROVEN |
| the nine type sizes | jump table at `00243514`, image-base-relative, resolved with a tool | 1 | PROVEN |
| the six constructors | jump table at `00243538`, same method | 1 | PROVEN |
| types 3 and 6 cost nothing and build nothing | both tables send them to the zero arm and the no-op arm | 1 | PROVEN |
| one allocation holds pointers and nodes | the total starts at `count * 8`; `[r15+0x10]` is indexed by 8 for pointers | 1 | PROVEN |
| bits 6–15 of node `+0x08` are cleared | `and dword [rbx+8], 0xFFFF003F` | 1 | PROVEN |
| ~~what the types mean~~ — superseded: §5b, §5e and UQ-75..78 name every type (2026-09-17 / 2026-09-22); marked 2026-09-30, SWE2-CONTRACT | ~~**not established**~~ constructors and drawers read | 1 | PROVEN |
| ~~any runtime observation~~ — superseded: the 2026-09-08 live read of the slot registry, §5c; marked 2026-09-30, SWE2-CONTRACT | ~~**none exists**~~ live read, read-only (AUDIT-LOG, `7593db615`) | 10 | OBSERVED |
| bit 7 gates the texture-memory layout pass | `b6_typed_list.py` B1–B8, E1–E3 | 1 | PROVEN |
| the sub-image record is `u16, u16, 12-bit, 12-bit, …, byte 7 opacity` | `b6_typed_list.py` S1–S4 | 1 | PROVEN |
| resources 111 / 127 are `save_load.mrp` / `DataFace_c.tm2` | SWE2-DATA `kind7.py`, `b6_typed_list.py` K1–K3 | 1 | PROVEN |

*(§10 narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../_index/candidates/auditspec-review-dd-02-restatus-0930/REVIEW.md) correction 1: the first row counts calling functions and sites as §2 does; the two rows SWE2-CONTRACT rewrote are re-cut to four cells, and the runtime row's tier is 10, not "live".)*

## 11. Related

- [The authored data table registry](authored-data-table-registry.md) — the same `ImageAddress_ResolveRuntimePointer` addressing
- [The VBF / st2e tables](VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) — another authored table reached the same way

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py --addr 002432B0` run first, per
[`EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment — and it is what
found the second correction below.)*

| claim | measured |
|---|---|
| `002432B0` is **609 B** | **609** |
| "36 owned by `UI` and 72 unowned" | **36 and 72**, and they sum to the **108** |

### ⚠ 108 is the caller count; the sites are 113

Scanning every function body for a `call`/`jmp` to `002432B0` returns **113 sites in 108 distinct
functions** — **five of the 108 call it twice**. The owner split is exactly right *as a function
count* (36 + 72 = 108); it is the word **sites** that does not fit it.

> The same slip as [the transform primitives](../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md)
> §2, corrected the same day, and the same amendment covers both:
> [*a count without its unit cannot be checked*](../_index/EVIDENCE-STANDARD.md) — here in the form
> where the unit is stated and is the wrong one.

### ⚠ "No document had cited it" was true, and is no longer

| document | first commit | |
|---|---|---|
| **this page** | `5afcc48`, 2026-09-08 | — |
| `how-a-class-registers-its-array-members-and-annotations.md` | `43adc03`, **34 commits later** | cites `002432B0` |

**This page came first**, so the claim was **correct when written**. It is now stale: one document
cites the function today. Tensed in §2 rather than struck — what changed is the database, not the
finding.

*(Second page in two days to carry this exact shape. `check_novelty_claims.py` flags them; the git
dates settle them; and in both cases the page was right and has simply been overtaken.)*

**Not claimed:** §3's record walk, the nine kinds and their sizes, the two-pass measure-then-build
and the one-allocation claim were **not** re-derived — this pass tested the function's identity and
its population, not what it decodes. Nothing was executed or observed live.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

**Presentation — CLIENT and SERVICE.**

- The format builders `00181000` and `00181250` are also used by a 667-byte Presentation body, and `00181190` calls a
  588-byte one.
- The image member callback's `0024A1D0` (`"%s%03d"`) calls five Presentation bodies (30–392 B).
- `0024A5F0` / `0024A610` / `002A0060` are read by an 841-byte body.
- The st2e group resolver `002F9920` is read by two bodies (426 B and 451 B).
- The arena entry `0036A190` has 17 Presentation callers (MECHANICAL).

**CoreRuntimeScheduling — MECHANICAL.**

- The item constructors and resolvers (`0029F130`, `0029F930`, `0029FEB0`, `002A0060`, `002432B0`, `002A00F0`,
  `002A1A80`, `002F9920`, `0057EDB0`) call the image-address resolver/encoder pair `0020E600` /
  `0020E620`, the shared codec §5d already describes — resolve/encode fan-out only, no scheduling claim.
- **Input — CLIENT (1 edge).** 1 inbound (Input bodies `00291D90` call page-cited `0024A440`). Substantive edges include `0024A440` is called by `00291D90`.
- **SaveLoad — CLIENT (3 edges).** 3 inbound (SaveLoad bodies `00582790`, `00280140` call page-cited `00245020`, `003933F0`, `00393460`). Substantive edges include `003933F0` is called by `00582790`; `00393460` is called by `00582790`; the remaining edges run through shared helpers the page cites.
- **Save_Load_Settings — CLIENT and SERVICE (5 edges).** 3 inbound (Save_Load_Settings bodies `SaveLoad_ControllerLifecycleHandler` (00582860), `SaveWrite_OperationStateCallback` (0057E4D0) call page-cited `00245020`, `00582790`, `SaveLoad_HandleStorageStatusResultAndAdvanceController` (00583040)); 2 outbound (page-cited `SaveLoad_HandleStorageStatusResultAndAdvanceController` (00583040) call Save_Load_Settings bodies `0057EC60`, `00581350`). Substantive edges include `00582790` is called by `SaveLoad_ControllerLifecycleHandler` (00582860); `SaveLoad_HandleStorageStatusResultAndAdvanceController` (00583040) is called by `SaveLoad_ControllerLifecycleHandler` (00582860); `SaveLoad_HandleStorageStatusResultAndAdvanceController` (00583040) calls `0057EC60`; `SaveLoad_HandleStorageStatusResultAndAdvanceController` (00583040) calls `00581350`; the remaining edges run through shared helpers the page cites.
- **UI — CLIENT and SERVICE (76 edges).** 71 inbound (UI bodies `002435C0`, `00243C00`, `002D28E0` call page-cited `00245020`, `002D9380`, `002D9B00`); 5 outbound (page-cited `002435C0`, `00243C00`, `0029ED50` call UI bodies `002D9380`, `002A0440`, `002D8D40`). Substantive edges include `00181000` is called by `00291010`; `00181000` is called by `002917E0`; `00181250` is called by `00291010`; `00181250` is called by `002917E0`; the remaining edges run through shared helpers the page cites.
- **World — CLIENT (2 edges).** 2 inbound (World bodies `003C63A0`, `00378540` call page-cited `0024A480`, `0036A190`). Substantive edges include `0024A480` is called by `003C63A0`; the remaining edges run through shared helpers the page cites.
- **WorldAreaField — CLIENT (6 edges).** 6 inbound (WorldAreaField bodies `003C0450`, `00576A50`, `MapRef_BeginLoadResources` (00268750) call page-cited `0036A190`, `002F9920`). Substantive edges include `002F9920` is called by `003C0450`; `002F9920` is called by `00576A50`; the remaining edges run through shared helpers the page cites.
- **Movement — SERVICE (5 edges).** 4 outbound (page-cited `MainLoop_UpdateAndRenderFrame` (0022B8C0), `MainLoop_Draw` (0022B0B0), `0022BC20` call Movement bodies `00263560`, `00357780`, `0037CF00`).
- **Party — SERVICE (2 edges).** 2 outbound (page-cited `MainLoop_UpdateAndRenderFrame` (0022B8C0), `0022BC20` call Party bodies `PartyFocus_CommitPendingPackedActorHandle_Thunk` (00358BB0)).
- **RNG_Random_Selection — MECHANICAL (2 edges).** 2 outbound (page-cited `0022B6E0`, `0022B7E0` call RNG_Random_Selection bodies `RNG_MT19937_NextU32_Thunk` (00379CD0)) - shared-helper call surface, not a RNG_Random_Selection relationship of this page's subjects.
