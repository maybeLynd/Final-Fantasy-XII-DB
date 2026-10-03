---
system: The text-element dispatch table — how the residual drawing cluster is entered
category: 99-Unresolved-Residual
status: AUDITED — which text each drawer owns is answered by builder (GJ-7) and the four kinds are named (GJ-8); SD-106 (the five 002B3280 sites) and SD-107 (no traced code builds a kind-1 element, static) are answered; the residue prose carried by SWE2-CONTRACT's DD batch 19 (owner re-status 2026-10-01, OPUS; documented_rule READY).
owner_layer: CodeDomain — residual; ancestors owned by UI
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 002AC5F0, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity.py GN161 -> PARENT, control passed) - and check_stranded_absence.py, sweeping the GN160 resolved set which strictly CONTAINS all 30, reports no live absence claim on any line of this document
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    voided_by: any delta that REMOVES or REWRITES a comment, tag, name, prototype or body range - re-run the additivity test at each checkpoint
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-text-dispatch-pass-1 - the table, both null rows, the single image-wide pointer to the orphan, the caller counts 2/3/5 and both column bases all reproduce; the boundary argument is now exact because the powers of ten are NINE u32 occupying 36 bytes immediately after the 96-byte table; section 4's listing of 002ABF20 omits its null test, so section 3 is right and section 4 is short; and the signed selector is bounded by nothing in any of the three dispatchers, which makes obj[+0xA3] in 0..3 an unproven precondition rather than a checked one
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record opus-text-dispatch-pass-1; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# The text-element dispatch table — how the residual drawing cluster is entered

> ~~The largest unclassified function in the game is not called by name from anywhere.~~ *(corrected 2026-10-02, OPUS: `002AC5F0` is classified at GN162 (§1) and has seven direct callers; it is the column-1 and column-2 handlers, not it, that are reached through the table)* It is reached
> through a **twelve-slot handler table** selected by **one signed byte on the object being drawn** -
> four kinds, three operations each — and three tiny dispatchers that do nothing but index it and
> tail-jump.

**PARTIAL.** *(answered: see the front matter, now `status: AUDITED`; 2026-10-02, OPUS)* The dispatch architecture, the selector, the table and all three dispatchers are read at
tier 1. ~~**Which text each drawer is responsible for remains open** (`PROPOSED-repos9e-6`), though §6~~
~~narrows it.~~ *(Corrected 2026-09-30, SWE2-DATA: GJ-7 answered it on 2026-09-25, by builder (§7).)*

## 1. Why this document exists

`002AC5F0` — 7,489 bytes, the largest body still residual at the survey and classified at GN162 as `UI.Text.ControlCodeInterpreter` — has a signature and no
decode. Three cheap routes into it are closed, and closing them is a result:

| Route | Result |
|---|---|
| Imports called (slot-keyed census) | **zero**, for all four font drawers |
| Strings referenced directly | **zero**, for all four |
| Strings one or two calls below | **one**, `"display : draw Font"` — shared by all four, so it discriminates nothing |
| Named or owned callers | **none**; every caller is an unnamed, unowned residual |

> **The IAT census works because the OS boundary is outside the engine's control. This cluster never
> touches it.** That is why the best instrument in this project cannot reach here, and why the way in
> had to be the data rather than the code.

## 1b. What the player sees (SWE2-DATA, 2026-09-30)

Every text element this table serves carries one of four kinds, and the kind decides which routine draws it (§7, GJ-7):

- **The message window's page text** is kind 0, drawn by `002A9F00`.
- **The message window's run elements** are kind 3, drawn by `002AAE40`.
- **Screen labels** (menus, the world map, the level-up screen, the HUD and more) are kind 2. This table draws nothing for them; the byte-charset renderer `002B0280` does.
- **Kind 1** has a drawer, `002AA800`, but no builder has been found, so no shipped text is known to use it (SD-107).
  *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19): SD-107 is answered by the record published in
  `59ec09a95`. No traced code builds a kind-1 text element. See the SD-107 note in §7.)*

## 2. The way in was a pointer table

`002AAE40` has **zero callers**. A verified scan for 8-byte pointers to it found exactly one, at
`.rdata` `0x00916518` — and immediately after that address sits a table of
`1, 10, 100, 1000, ... 100000000`, **the powers of ten**. Immediately before it sits the handler
table.

That run is the entry point to the whole cluster.

## 3. The table: four kinds x three operations

```
009164C0   002A9980   002A8C50   002A9F00      <- kind 0
009164D8   002A9980   002A8C50   002AA800      <- kind 1
009164F0   (null)     (null)     (null)        <- kind 2
00916508   (null)     (null)     002AAE40      <- kind 3
```

**Four rows of three, 96 bytes, ending exactly where the powers-of-ten table begins.** Kinds 0 and 1
are identical in columns 0 and 1 and differ only in column 2; **kind 2 has no handlers at all, and
kind 3 has only a column-2 handler.**

> **CORRECTED 2026-09-03.** This section first reported *two* rows, having read only as far as the
> last non-null entry before the gap. **The null rows are part of the table** -- they are why every
> dispatcher null-tests the loaded pointer -- and `002AAE40`, the orphan of section 2, is **kind 3
> column 2**. Reading a table to its last non-null entry is not reading the table.

## 4. Three dispatchers, one selector

All three are tiny, do nothing but index the table, and key on **the same byte**:

```asm
; 002B3930 -- column 0, unconditional, 32 bytes
movsx rax, byte ptr [rcx + 0xA3]      ; the selector, SIGNED
lea   rdx, [rax + rax*2]              ; row = kind * 3
lea   rax, [rip -> 009164C0]          ; column 0
mov   rax, [rax + rdx*8]
test  rax, rax
je    ret
jmp   rax                             ; tail-call
```

```asm
; 002ABF20 -- column 1, unconditional, 65 bytes
mov   rax, [0209CC40]                 ; the cluster's shared context
movsx r8d, word ptr [rcx + 0x8C]
mov   qword ptr [0209CC48], 0
mov   dword ptr [rax + 0x10D8], r8d   ; publish obj[0x8C] into the context
movsx rax, byte ptr [rcx + 0xA3]
lea   r8, [rax + rax*2]
lea   rax, [rip -> 009164C8]          ; column 1
mov   rax, [rax + r8*8]
test  rax, rax                        ; omitted from this listing -- §10
je    ret
jmp   rax
```

`002ABEC0` (83 B) is the **guarded** twin of `002ABF20` — same publish, same column — behind

```asm
cmp byte ptr [rcx + 0xAC], 1
je  dispatch
cmp dword ptr [01E0CDC8], 0
je  skip                              ; neither condition -> do nothing
```

| Dispatcher | Column | Guard | Callers |
|---|---:|---|---:|
| `002B3930` | 0 | none | 2 |
| `002ABF20` | 1 | none | 3 |
| `002ABEC0` | 1 | `obj[0xAC] == 1` **or** the global `01E0CDC8` is set | 5 |

~~**No dispatcher references column 2** by address, and the consequence is section 6b: two of the three~~
~~column-2 handlers are **unreachable**.~~ *(Corrected 2026-09-30, SWE2-DATA: §6b is withdrawn. The slot-2 dispatcher `002AF960` indexes column 2, so all three handlers are reachable.)*

> **The selector is read with `movsx` and never bounds-checked.** A negative or out-of-range
> `obj[0xA3]` indexes outside the twelve slots; the only protection is the null test on the loaded
> pointer, which will not catch a garbage pointer.

## 4a. What the guard gates — ANSWERED 2026-09-21 (FABLE): a frame-rate suppression, and only one of its two terms is live

> **Name corrected 2026-09-21 (FABLE), same day.** This section first called `01F82E38` a "2x
> render-scale mode". It is the **`FrameLimit` time base** — `01DFE0B4` is the frame base, *1 at
> 30 fps and 2 at 60*, named that in `what-the-engine-fixes-at-boot.md` and in the per-frame gate
> page, and section 13b of the boot contract already reported `EXP-001` varying it. **Every
> measurement below stands; the label and what it implied do not.** The guard is suppressed by the
> frame rate the game is running at, not by a resolution setting.

Section 4 records `002ABEC0`'s guard as a disjunction and leaves both terms unnamed. Both are now
read to their sources. **The global is a scoped latch the message window sets and puts back; the
object byte is a test no code in the image satisfies.**

### The latch is the message window's, and it lasts one message (FABLE, 2026-09-21)

`01E0CDC8` has, image-wide, **two writes and six reads across four functions**, and **both writes are
in `002A6190`** — the message-window procedure. That procedure dispatches on `[rdx] - 1` against
`0x14` (`002A61B1`) through the 21-entry table at `002A698C`, and both writes fall inside the arm the
table entry for **message id 2** alone selects, entered at `002A6412`:

```asm
002A6459  mov  ecx, dword ptr [rdi + 0xb4]
002A645F  call 001EDEC0
002A6464  mov  dword ptr [01E0CDC8], eax     ; the latch is SET from a predicate
002A646A  test eax, eax
002A646C  je   002a6514                      ; ... and a zero skips the arm's own body
   ...
002A6522  mov  esi, 1
002A6531  cmp  dword ptr [01E0CDC8], ebx     ; ebx = 0 since 002A6418
   ...
002A65D8  mov  dword ptr [01E0CDC8], esi     ; ... and PUT BACK to 1 on the way out
002A65DE  call 002A3F90
```

So the cell is **not an enable that someone turns on**. It is **1 at rest** — it ships as `1` in raw
`.data` and the only arm that disturbs it restores it before returning — and it is driven to `0` only
for the span of one window's id-2 message. This is the same save/reset/restore discipline
[section 3e of the drawing-context page](the-shared-drawing-context.md) found in `002B24B0`, applied
to a global instead of a field.

**The same latch gates four more sites**, so one window's id 2 turns off a family of draws at once:
`002A7720` tests it three times (`002A774B`, `002A779C`, and `002A77F7`, immediately after its own
`call 002ABEC0` at `002A77F2`), and the column-1 kind-0 handler `002A8C50` tests it once at
`002A8D37`.

### What the predicate answers — the `FrameLimit` time base (FABLE, 2026-09-21)

`001EDEC0` is 40 bytes and reads no record at all. It is a three-way predicate over two globals and
**bit 0 of its argument**:

```asm
001EDEC0  cmp dword ptr [01F82E38], 0   ; scale mode active?   <- answered 2026-10-02, OPUS: the FrameLimit time base, not a scale mode (name corrected 2026-09-21 above)
001EDEC7  je  001edee2                  ;   no  -> return 1
001EDEC9  cmp dword ptr [01DFE0C0], 0   ; suppressed?
001EDED0  je  001ededa
001EDED2  mov ecx, 1                    ;   yes -> return 1
001EDED7  mov eax, ecx
001EDED9  ret
001EDEDA  not ecx                       ; else -> return (~arg) & 1
001EDEDC  and ecx, 1
001EDEDF  mov eax, ecx
001EDEE1  ret
001EDEE2  mov eax, 1
001EDEE7  ret
```

`01F82E38` is the **time-base-switched flag** — set exactly when `FrameLimit` selects the 60 fps base: 13 readers, one writer, `001EDDC0` at `001EDDE8`,
which is the boot body [the boot contract's section 13c](../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md)
now reads out. It lives in `.data`'s **virtual tail with no raw bytes**, so it **initialises to 0** —
a disassembler that reads its file offset prints garbage for it, and this document's first pass did.
`01DFE0C0` is the mode's **suppressor**: 3 readers, one writer, the 7-byte setter `001EDEF0`, called
only from `00184960`, which sets it to `1` on entry (`0018496D`) and clears it (`001849A2`) unless its
argument is `1` and `byte [001EBA40() + 0x118]` is zero. It **ships as `1`**.

So the predicate says: **"1 unless the ~~2x scale mode~~ 60 fps time base is on *(answered: see "Name corrected 2026-09-21" above; 2026-10-02, OPUS)*, unsuppressed, and bit 0 of the argument is
set."** Its argument is the window's `+0xB4`. Two sibling predicates read the same pair — `001EDDA0`
(the same two globals in the other order, returning 0 in the same case) and `001EDE80` (returning
`0022A080() + 0022A030()` in that case and `1` otherwise).

### The object byte is a test nothing satisfies (FABLE, 2026-09-21)

`002ABEC0`'s `rcx` is **not the widget**. Its ~~nine callers~~ callers *(corrected 2026-10-02, OPUS: five functions, six rel32 sites — the 5 of §4's table)* pass the widget's embedded text-draw block
at `+0xC0`, `+0xD0` or `+0xE0`, or a stack local — established on
[the request-router page](../../16-UI/Request-Router/ui-request-router.md). So `[rcx + 0xAC]` is a
field of that block, and the widget contract's `+0xAC` (always `6`) is a **different byte of a
different object at the same offset**.

Sweeping byte writes at all four displacements the block can be reached through:

| displacement | what it reaches | writes | who |
|---|---|---|---|
| `+0xAC` | the block through a pointer to itself | 10 | 6 in the widget constructors `002465F0` / `002477A0` / `00247810`, writing `6` or `0xF9` **to the widget base**; 2 in `002B0280`, an `inc`/clear counter on an object whose other fields are `+0x98`..`+0xC0` (its *context* pointer is a separate register); 2 in `00784E80` / `00786DD0`, outside this layer |
| `+0x16C` | block embedded at widget `+0xC0` | 5 | all in `001AD780`, `006FD110`, `00760700` — outside this layer |
| `+0x17C` | block embedded at widget `+0xD0` | 2 | `006FF900`, `00760700` — outside this layer |
| `+0x18C` | block embedded at widget `+0xE0` | **0** | — |

The block's own initialiser `002B3400` writes `+0x8C` (`002B3469`) and `+0xA3` (`002B3470`) and
**does not write `+0xAC`**. The three stack-local instances never touch the displacement their block's
`+0xAC` would occupy — `002A3250`'s `[rsp+0x130]` block would put it at `[rsp+0x1DC]`, `002A5590`'s
`[rbp-0x40]` at `[rbp+0x6C]`, `002A6C40`'s `[rsp+0x60]` at `[rsp+0x10C]`, and none of the three frames
addresses those, nor clears the local.

**So no site in the image sets that byte to `1`.** On the embedded instances it holds whatever the
enclosing widget's construction left; on the three stack instances it is frame residue. The first
term of the guard is compiled-in and is not satisfied on purpose anywhere.

### What this means for column 1 (FABLE, 2026-09-21)

`002ABEC0` therefore dispatches **for every one of its five callers, always**, except inside message
id 2 of a message window whose `+0xB4` has bit 0 set, while the 60 fps time base is in effect and
unsuppressed. `obj[0xAC] == 1` is a **per-object exemption from that refusal** that nothing claims.

Read the other way round, the answer to "a condition under which column 1 runs at all" is that
**there is no such condition in the ordinary case** — the guarded dispatcher and its unguarded twin
`002ABF20` behave identically until the message window suppresses the scaled text draw for the span
of one message. That is a *narrower* statement than section 4's table implies, and it is the one the
bytes support.

**A label this correction touches, and does not settle.**
[the-shared-dialog-widgets.md](../../16-UI/Shared-Dialogs/the-shared-dialog-widgets.md) reads
`001EDEC0` on `+0xB4` as a "(window record)" resolve in `0057C8C0`'s id 2. The call is real and the
placement is right — it is the **same id-2 idiom** as here — but `001EDEC0` resolves nothing and reads
only bit 0 of its argument, so `+0xB4` is not shown to be a record by that call. That page is not
mine; routed rather than edited.

## 5. The shared context

Both column-1 dispatchers write `(int16)obj[0x8C]` into `[0209CC40] + 0x10D8` **before** tail-jumping,
and clear `[0209CC48]`. `0209CC40` is referenced at **121 sites** across the cluster — it is the
common object the handlers work through, and the dispatchers' only job besides dispatching is to
publish one field of the element into it.

## 6. What the columns are — narrowed, not closed

Two of the three identify themselves from what their handlers touch:

- **Column 0 → `002A9980`, and `002A9980` takes the address of the powers-of-ten table** at
  `0x00916520`. **Column 0 is numeric formatting**, and it is *shared by kinds 0 and 1*.
- **Column 1 → `002A8C50`, and `002A8C50` is one of the seven callers of `002AC5F0`**, the big font
  drawer. **Column 1 is text drawing**, also shared by kinds 0 and 1.
- **Column 2 is the kind-specific operation** - `002A9F00` for kind 0, `002AA800` for kind 1, `002AAE40` for kind 3 - and
  `002A9F00` is *also* a caller of `002AC5F0`.

> **Kinds 0 and 1 share how they format numbers and how they draw text, and differ only in a third
> operation.** Whatever distinguishes them is in column 2 — ~~the one column no dispatcher reaches~~
> **and a dispatcher DOES reach it (corrected 2026-09-16, OPUS; see §6b)**.

This narrows `PROPOSED-repos9e-6` without closing it: `002AC5F0` is entered from **column 1 for both
kinds** and from **column 2 of kind 0**, so it is not specific to one text kind — which is consistent
with it being the largest of the four and the one six other functions call. *(Closed 2026-09-25 by builder under GJ-7, §7; pointer added 2026-09-30, SWE2-DATA.)*

## 6b. ~~Two of the three column-2 handlers are unreachable~~ — WITHDRAWN 2026-09-16, they are entries in an indexed table

Nothing indexes column 2, so the only route to a column-2 handler is a direct call. Testing all three
against **unbounded** scans -- every `E8` and `E9` displacement in `.text`, plus every verified 8-byte
pointer in every non-`.text` section:

| Column-2 handler | `E8` calls | `E9` jumps | pointers to it |
|---|---:|---:|---|
| `002A9F00` (kind 0) -- **control** | **8** | 0 | its table slot only |
| `002AA800` (kind 1) | **0** | **0** | its table slot only |
| `002AAE40` (kind 3) | **0** | **0** | its table slot only |

> ~~**`002AA800` (1,598 B) and `002AAE40` (2,440 B) cannot be reached.** Their only reference in the
> entire image is a table slot that no code indexes. That is **4,038 bytes of unreachable code**.~~
>
> **WITHDRAWN 2026-09-16 (OPUS). The counts above are right; the premise under them is false, and it
> was mine.** *"Nothing indexes column 2, so the only route to a column-2 handler is a direct call"*
> assumes a route would have to materialise the handler's address somewhere a scan can see. This one
> never does. `002AF960` loads the **image base** and then calls through an index:
>
> ```asm
> 002AFB6C  lea  rdi, [rip - 0x18FB73]        ; = 00120000, the image base
> 002AFCB1  call qword ptr [rdi + r9*8 + 0x7F64D0]
> ```
>
> `00120000 + 0x7F64D0 = 009164D0`, and that table is **sparse**, which is why it reads as empty from
> either end:
>
> | index | entry |  | index | entry |
> |---:|---|---|---:|---|
> | 0 | `002A9F00` |  | 4–8 | null |
> | 1 | `002A9980` |  | 9 | **`002AAE40`** |
> | 2 | `002A8C50` |  | 10 | `0000000A00000001` — not an address; the table ends |
> | 3 | **`002AA800`** |  |  | |
>
> **Both "unreachable" handlers are entries in an indexed table.** The E8/E9/pointer counts in the
> table above stay exactly as measured — there is no direct call and no stored pointer — and that is
> the point: **an indexed call through a register-held image base materialises the target nowhere**,
> so every instrument that looks for the address returns zero, correctly, and the conclusion drawn
> from four zeros was still wrong.
>
> FABLE found this and retracted a five-instrument claim of their own on the same idiom within the
> hour (`f2e6ae19`); `check_absence_claims.py` now carries a fifth instrument and a one-hop table walk
> for exactly this class, with `002AAE40` as its control. The lesson is not that a scan was weak — it
> is that **four instruments that all look for the target address are one instrument**, and a
> "control" drawn from the same family cannot show otherwise. `002A9F00`'s eight calls made the
> measurement look controlled while every arm of it shared the blind spot.

**The control is what makes this a measurement.** `002A9F00` sits in the same column of the same
table, and the same scan finds eight calls to it -- it survives because it is *also* called directly,
which makes its table slot redundant rather than load-bearing.

> ~~**A zero from an instrument that reports eight for a sibling in the identical position is
> evidence.** Kind 0's column-2 entry is reachable *despite* the table, not through it.~~
> **Corrected 2026-09-16 (OPUS):** it is reachable through the table *as well* — `002A9F00` is entry
> 0 of the same indexed table. The eight direct calls are real and so is the indexed route; what the
> sibling controlled for was the SCAN, not the premise.

## 6c. `GJ-7` narrowed, and one of its four drawers is not a drawer (FABLE, 2026-09-21)

`GJ-7` asks which text each of **four font drawers** owns. Read side by side, they are not four peers,
and the table is emptier than "four kinds x three operations" suggests.

### The table as bytes (FABLE, 2026-09-21)

| kind | column 0 | column 1 | column 2 |
|---|---|---|---|
| 0 | `002A9980` | `002A8C50` | `002A9F00` |
| 1 | `002A9980` | `002A8C50` | `002AA800` |
| 2 | — | — | — |
| 3 | — | — | `002AAE40` |

**Kind 2 is entirely null, and kind 3 has only its third column.** Of twelve slots, ~~five are filled by~~
~~four distinct bodies.~~ seven are filled by five distinct bodies *(corrected 2026-10-02, OPUS: the table at `009164C0` read as qwords: `002A9980` ×2, `002A8C50` ×2, `002A9F00`, `002AA800`, `002AAE40`)*. This is not a gap in the reading: `002ABEC0` and its twin both `test rax, rax`
after the load and return on zero (`002ABF08`), so the dispatchers are written for exactly this.

### `002AC5F0` is the layer above them, not the fourth of them (FABLE, 2026-09-21)

Section 6 places `002AC5F0` as the "big font drawer" reached from column 1 and from kind 0's column 2.
Profiled against the three column-2 bodies, it is a different kind of thing:

| | instructions | distinct callees | context fields it touches |
|---|---|---|---|
| `002A9F00` | 511 | 13 | `+0x10D8`, `+0x10DC`, `+0x10E4`, `+0x10FC` |
| `002AA800` | 329 | 14 | none |
| `002AAE40` | 505 | 16 | `+0x10E8`, `+0x10FC` |
| `002AC5F0` | **1,658** | **44** | all six |

It calls **`002A9F00` four times** (`002ACABD`, `002AD728`, `002ADABA`, `002ADFED`), and it alone
carries the `003FFAxx` family — nineteen calls to `003FFAB0` and ten more across `003FFB00`..`003FFF10`,
the control-code handlers the control-code page documents. **So it sits above the emitters and drives
one of them**, which is why it was never specific to a text kind: it is not a sibling in that table.

### The two table-only bodies (FABLE, 2026-09-21)

`002AA800` and `002AAE40` have **zero direct call sites in the image**. Nothing calls them by name;
they are reached only through the kind table. `002A9F00` is the opposite — **eight direct call sites in
three functions** on top of its table slot — so *it* is the shared per-glyph emitter and the other two
are genuinely kind-specific.

All three funnel into the same final step, `002AC2F0` (8 callers), and all three call the same render
wrappers `0017F7C0`, `0017F8C0`, `0017FC90` and `0020E600` — thin bodies that fetch a singleton through
`001B5FA0` and tail-jump into `001E9xxx`. **The one structural difference between them: `002AA800`
does not call `002AC5F0`, and the other two do.**

### And three call sites turn the reveal off explicitly (FABLE, 2026-09-21)

`002B0280` is one of `002A9F00`'s three direct callers, and at each of its three sites it writes
`0x7D00` into the context's `+0x10DC` **immediately before the call**:

| write | call |
|---|---|
| `002B16FD  mov dword ptr [ctx + 0x10dc], 0x7d00` | `002B1707  call 002A9F00` |
| `002B1759  mov dword ptr [ctx + 0x10dc], 0x7d00` | `002B1763  call 002A9F00` |
| `002B1919  mov dword ptr [ctx + 0x10dc], 0x7d00` | `002B1923  call 002A9F00` |

Section 3g of [the drawing-context page](the-shared-drawing-context.md) reads `+0x10DC` as the
reveal's full-opacity counter with 32,000 meaning "unlimited". These three are that mechanism's
**opt-out, used deliberately**: text drawn through `002B0280` is never typed out.

### What `GJ-7` still wants (FABLE, 2026-09-21)

Naming the *content* of kind 0 versus kind 1 versus kind 3 needs the kinds named, which is `GJ-8` —
`obj[0xA3]`'s domain — and that is routed, not guessed here. *(Answered since: GJ-8 on 2026-09-23 (§8b) and GJ-7 on 2026-09-25 (§7); pointer added 2026-09-30, SWE2-DATA.)* What this section settles is the shape
the question should be asked in: **three emitters, one of which is shared, under one control-code
engine; and any answer that treats `002AC5F0` as a fourth parallel drawer is answering about the wrong
object.**

## 6d. Key addresses (SWE2-DATA, 2026-09-30)

| address | role |
|---|---|
| `009164C0` | the handler table: four kinds by three columns, 24-byte rows |
| `002B3930` / `002ABF20` / `002ABEC0` | the column-0 and column-1 dispatchers (§4) |
| `002AF960` | the slot-2 dispatcher: indexes column 2 by kind |
| `002A9980` / `002A8C50` | columns 0 and 1: numeric format, text draw |
| `002A9F00` / `002AA800` / `002AAE40` | the column-2 emitters for kinds 0, 1 and 3 |
| `002AC5F0` | the control-code engine above the emitters (§6c) |
| `002B3400` | stamps kind 2 (§8b) |
| `002DD680` / `002B0280` | the kind-2 path outside the table: stamp follower and byte-charset renderer |

## 6e. Call chain (SWE2-DATA, 2026-09-30)

```
builders (002B3C30 / 002B3D50, 002A4830, 002B3400) set obj+0xA3 = kind
002B3930 / 002ABF20 / 002ABEC0 -> [009164C0 + kind*24 + col*8]  (columns 0, 1)
002AF960 -> [009164D0 + kind*24]                                 (column 2)
  kind 0 -> 002A9F00 <-> 002AC5F0      kind 3 -> 002AAE40 -> 002AC5F0      kind 1 -> 002AA800
kind 2: 002B3400 -> 002DD680 -> 002B0280, or 002B0280 directly
```

The edges are the call sites §4, §6c, §8b and `_index/candidates/dd-data-3-0930/dispatch_checks.py` cite.

## 6f. Modding notes (SWE2-DATA, 2026-09-30)

- The selector `+0xA3` is read with `movsx` and never bounded (§4). A value of 2, or 4 and above, on an element that reaches the unguarded column-2 call at `002AFCB1` calls through a null or out-of-table slot (§8b).
- Screen labels (kind 2) do not pass through this table, so hooks on its handlers do not see them. Hook `002B0280` instead.

## 7. What is not known

- **`GJ-7` — Which text each of the four font drawers is responsible for.** `PROPOSED-repos9e-6` stands; §6
  narrows `002AC5F0`'s entry points but does not name its output. **Narrowed again 2026-09-21 (FABLE),
  §6c: there are three emitters, not four** — `002AC5F0` is the control-code engine above them and
  calls `002A9F00` four times. `002AA800` and `002AAE40` have **zero direct callers** and are reached
  only through the kind table; `002A9F00` has eight and is shared. **Kind 2's row is entirely null.**
  Naming the content of each kind now depends on `GJ-8`, not on reading more of these bodies.
  **Narrowed again 2026-09-25 (FABLE, Claude Opus 5.5): kind 2 is stamped on the game's own byte-charset text.**
  `002B3400` stamps kind 2 (`GJ-8`). Wherever it appears beside the `ex` test (three of the twelve sites), it is on
  the not-`ex` arm, and `ex` strings are UTF-16 and go to `003649A0`
  ([the glyph page](how-a-line-of-text-becomes-glyph-quads.md), UQ-361). At one site the one-byte-charset renderer
  `002B0280` follows it directly. At the other two, `002DD680` follows it~~, and that body is not read here~~. *(Corrected 2026-09-30, SWE2-DATA: `002DD680` calls `002B0280` at `002DD784`, so those two sites reach the byte-charset renderer too; `_index/candidates/dd-data-3-0930/dispatch_checks.py` D3.)* So the
  null row fits a kind whose text is handed to a byte-charset path rather than drawn through this table. That is
  shown for one site. ~~*Still open:* which on-screen strings become kind 0 and which kind 1.~~
  **ANSWERED the same day (FABLE, Claude Opus 5.5), at the level of who builds each kind.** Static; from the raw
  call index of each builder.
  - **Kind 0 (`002A9F00`) is the message window's page text.** Only `002B3C30` and `002B3D50` build it. Their direct
    callers are `002A1B00`, the message-window text-slice copy (UQ-361 on the glyph page), and `002A3250`, the
    window-open reconfigure. They are also reached through the generic constructor `002B32D0`, whose wrapper
    `002B32C0` is called only from `002A3250`, `002A6A80` and `002A6C40`, the message-window cluster. A second
    wrapper, `002B3280`, adds five sites outside it: one each in the `00227xxx` and `00241xxx` ranges, and three in `0057Cxxx`.
  - **Kind 3 (`002AAE40`) is the message window's run elements.** Only `002A4830`, inside `002A6190`, builds it
    (`GJ-8`).
  - **Kind 2 (the null row) is screen label text.** `002B3400` stamps it for 21 sites in 19 functions: menus, the
    world map, the level-up UI, the HUD and more. Its text takes the byte-charset path, as above.
  - **Kind 1 (`002AA800`) has no builder.** No cluster code writes 1 (`GJ-8`).

  *Not named:* what the five `002B3280` sites display. **SD-106** (SWE2-DATA, 2026-09-30).
  *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19): SD-106 is ANSWERED 2026-09-30 (OPUS `349fc1359`,
  [record](../../_index/candidates/sd106-measure-sites-0930/README.md)). The five sites measure a message line and
  the confirm dialog's caption and choices. See the SD-106 box below.)*
- ~~**Why column 2 exists at all**, given that nothing indexes it (section 6b). Whether it was reached
  by a dispatcher that was removed, or never wired, is not established.~~ **Dissolved 2026-09-16
  (OPUS): the question rested on the false premise §6b now withdraws.** `002AF960` indexes the table
  at `009164D0`, so column 2 is wired and the open question is the ordinary one — *what* each handler
  does, not why it exists.
- ~~**`GJ-8` — What `obj[0xA3]`'s four kinds are.** The selector's domain is four rows wide; nothing read here
  names any of them.~~ **ANSWERED 2026-09-23 (SWE2-CONTRACT), §8b — the kinds are emit-pipeline
  identities, named by who builds them and which column-2 body they get:** kind 3 is the
  message-window run (built only inside `002A6190`'s element builder `002A4830`, emitter
  `002AAE40` which calls `002AC5F0`); kind 2 is the handler-less element (the block's own
  initialiser `002B3400` — 19 callers — and its row is null in all three columns, so it dispatches
  nothing and reaching `002AFCB1` on it would `call` a null); kind 0 is the full-pipeline element
  (`002B3C30`/`002B3D50`, emitter `002A9F00` cooperating with `002AC5F0`); kind 1 is the
  control-code-free sibling (`002AA800` — the one emitter that does not call `002AC5F0`) that no
  cluster-side code ever instantiates (`GJ-11`). The image carries no designer-facing names —
  these are mechanism names, and kind 1's instantiation path is the honest residual. *(Pointer 2026-10-01
  (SWE2-CONTRACT for OPUS, DD batch 19): that residual is SD-107, answered by the record published in `59ec09a95`.
  No traced code builds a kind-1 text element. See the SD-107 note below.)*
- `GJ-9` — ~~**What `obj[0xAC]` and the global `01E0CDC8` gate** in the guarded dispatcher — a condition under
  which column 1 runs at all.~~ **ANSWERED 2026-09-21 (FABLE), section 4a**: the global is the message
  window's scoped time-base latch, `1` at rest and driven to `0` only for the span of one id-2
  message; the object byte is a test **no site in the image writes `1` to**. Column 1 runs
  unconditionally for all five callers outside that span.
- ~~**`GJ-10` — What `[0209CC40]` is**, beyond being the cluster's shared context with 121 reference sites, and
  what `+0x10D8` means to the handlers that consume it.~~
  **ANSWERED 2026-09-21 — this bullet was stale, corrected 2026-09-22 (FABLE).** The answer lives on
  [the shared drawing context](the-shared-drawing-context.md), the page named after this very global:
  `0209CC40` holds a **static `.bss` block at `0209D490`, `0x1108` bytes**, `memset`-zeroed and published
  by the 69-byte `FUN_002B3550`, the image's **only** writer of the pointer; and §3g reads `+0x10D8`,
  `+0x10DC` and `+0x10E4` as the **progressive text reveal**.
  > *Left open here, this bullet cost a full re-derivation of that page on 2026-09-22 — the register
  > already said ANSWERED and named the owning page. **When a page bullet and the register disagree,
  > the register is the one to believe.***
- **`GJ-11` — Which code sets each kind.** **ANSWERED 2026-09-22 (FABLE): `+0xA3` is not one field.** The 13 writer bodies span five owner domains — `UI.Text`, `Presentation`, `Audio`, third-party `PPFX`, and two `BitfieldStateAlgorithm` bodies — and cluster-side code writes only **0, 2 and 3**. See the section above.

> **Every bullet in this section now carries its `GJ-` id, added 2026-09-22 (FABLE) on `AUDITSPEC-REQ-FABLE-REGISTER-71-OPEN-ITEMS`.** They were all registered already — the ids simply were not *in* the bullets, so a census that looks for an id in the item could not see them and fell back to matching this page's filename in the register, which for this page matched nothing. **An id-keyed register only works if the id is where the reader is.**
 Ten byte-writes to `+0xA3` exist image-wide; the four in this
  cluster's address neighbourhood write **0, 0, 2 and 3**, and the writer of **1** is in `Audio`, which
  may be a different structure at the same offset. ~~**Not resolved, and not assumed.**~~ *(Corrected 2026-09-30, SWE2-DATA: resolved by GJ-11's answer in the next section. `+0xA3` is not one field, and cluster-side code writes only 0, 2 and 3.)*

- [x] **What the five `002B3280` sites display.** The wrapper builds kind-0 elements outside the message window: one site each in the `00227xxx` and `00241xxx` ranges and three in `0057Cxxx`. Their callers are not read for what they show. **SD-106** (SWE2-DATA, 2026-09-30). *(SD-106 answered 2026-09-30 by OPUS `349fc1359`, [record](../../_index/candidates/sd106-measure-sites-0930/README.md).)*
- [x] **Whether anything instantiates kind 1.** The kind-1 emitter `002AA800` is wired in the table, and no plain byte write of 1 to `+0xA3` in the cluster reaches it (§8b). A writer outside the cluster, or a non-plain write, is not ruled out. **SD-107** (SWE2-DATA, 2026-09-30). *(SD-107 answered 2026-09-30 by SWE2-STRUCT for OPUS `59ec09a95`, [record](../../_index/candidates/sd7-sd107-closure-0930/README.md); register restated 2026-10-01 by OPUS for SWE2-DATA: no traced code builds a kind-1 text element (static).)*
  *Answer note 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19): answered 2026-09-30 by SWE2-STRUCT for OPUS,
  published in `59ec09a95`, [record `sd7-sd107-closure-0930`](../../_index/candidates/sd7-sd107-closure-0930/README.md)
  (`sd7_sd107_closure.py`, FAILS 0). **No traced code builds a kind-1 text element.** Of the 74 register-sourced
  `+0xA3` stores left open, exactly two write a lone byte there (`00780079`, `00780729`). Both fill `+0xA0`–`+0xA3` of
  a PPFX effect object as one 4-byte colour tuple. The other 72 are dword or qword stores at `+0xA0`, so they touch
  `+0xA3` only as a field's top byte, and none has a text element's float layout. The non-plain writes are the
  `Presentation` bit-0 `or` / `and` operations on a different structure (GJ-11, §8b). The record names its limits:
  whole-element copies and read-modify-write forms lie outside its census, and a copy would need a kind-1 source first.
  Rechecked independently in this batch:
  [`b19_checks.py`](../../_index/candidates/swe2contract-ddres-b19-0930/b19_checks.py) B1-B2. Image-wide there are
  exactly five immediate byte stores at `+0xA3`: the four builders write 0, 0, 2 and 3, and the one immediate 1 is
  `007E7401` in `007E73F0`, which is not a text builder (GJ-11 lists it as `Audio`). In player terms, no on-screen
  text takes the drawer that skips control codes. The box is ticked when SWE2-DATA restates the register row.*

## `GJ-11` answered — `+0xA3` is not one field, and no cluster-side code writes kind 1 (FABLE, 2026-09-22)

An image-wide displacement sweep for **byte** accesses at `+0xA3` — two arms, every listed function
decoded from its entry plus a linear pass over the `.text` no listed function covers, with
`002B3470` planted as a known positive and reported **PRESENT** — finds **14 writes and 20 reads**.

> **That reconciles with §7's “ten” exactly.** Four of the fourteen are **read-modify-write bit
> operations** (`or byte […], 1` at `00500CC2`; `and byte […], 0xFE` at `00500B52`, `00500BB6`,
> `00500CCB`). **10 plain writes + 4 bitwise = 14.** The earlier count was of plain writes.

### The thirteen writer bodies span five owner domains (FABLE, 2026-09-22)

Taken from the database's own ownership data rather than from address locality:

| writer | value | owner / domain |
|---|---|---|
| `002A49CA` in `002A4830` | **3** | `UI.Text.ControlCodeHandler` — **this cluster** |
| `002B3470` in `002B3400` | **2** | the block's own initialiser |
| `002B3C40` in `002B3C30` | **0** | cluster neighbourhood |
| `002B3D78` in `002B3D50` | **0** | cluster neighbourhood |
| `00500B52` `00500BB6` `00500CC2` `00500CCB` | bit 0 | **`Presentation`** |
| `007E7401` in `007E73F0`, `007E785C` in `007E7540` | **1**, reg | **`Audio`** |
| `00780729` in `00780590` | reg | **`ThirdParty.Rendering.PPFX`** |
| `00780079` in `0077FFE0` | reg | `NativeDispatch…` |
| `002475EC` in `002475D0`, `0024768D` in `00247680` | reg | `NativeInline.NoCall.**BitfieldStateAlgorithm**` |

**So `+0xA3` is shared by several unrelated structures and is not one field.** *The clearest case
needs no argument from locality at all:* `00780590` is **third-party PPFX/Yebis middleware**, whose
object cannot be this game's text element. **And the `Presentation` group treats the byte as a
flag** — `or …, 1` / `and …, 0xFE` sets and clears **bit 0**, which is not how a `0..3` selector is
written; `and 0xFE` would turn a kind 3 into a kind 2.

> **§7's refusal to assume was right, and can now be stated positively.** The writer of `1` at
> `007E7401` is **`Audio`-owned by the ledger**, not merely “in Audio” by address — so it is a
> different structure at the same offset, and `GJ-11` no longer has to leave that open.

### What that does to `GJ-8` (FABLE, 2026-09-22)

**Only `0`, `2` and `3` are ever written by code owned by this cluster.** The selector's domain is
four rows wide and **no cluster-side site writes `1`** — *the same shape `GJ-9` found at `+0xAC`,
which is a test no site in the image writes `1` to.* **`GJ-8` still needs the kinds named**, but its
domain is now bounded by what is actually authored rather than by the table's width. *(Pointer 2026-10-01
(SWE2-CONTRACT for OPUS, DD batch 19): GJ-8 is ANSWERED 2026-09-23 (§8b). The four kinds are named by their builders
and their column-2 bodies.)*

> **A discriminator that FAILED, recorded so the next reader does not repeat it.** My first test was
> *“does the writer reach the cluster's shared context `0209CC40`?”*. **It failed its own control:**
> `002B3400`, which is this block's own initialiser, never references that global — the writers act
> on the object, not on the shared context. The result was discarded and the ownership data used
> instead.

## 8b. `GJ-8` answered — the four kinds are emit-pipeline identities (SWE2-CONTRACT, 2026-09-23)

The selector at `+0xA3` is consumed twice: by the three column-0/1 dispatchers, and by the emit
dispatch at `002AFCA5`–`002AFCB1` inside `002AF960`, which does `movsx rax, byte [rbx+0xA3]` /
`lea r9,[rax+rax*2]` / `call qword [rdi + r9*8 + 0x7F64D0]` with `rdi` = the image base — i.e.
`call table_009164C0[kind*3 + 2]`, **column 2, by the same selector**. The emit path runs inside
the frame's render publication (`002AF960` fills the `0209CC40`-context fields `+0x10D4..+0x10E8`,
publishes `0209CC48`/`0209CC50`/`0209E5A0` render-buffer records and a `0x47`-opcode command
record, then dispatches). Its callers are `002A4541`, `002A4B3E`, `002A4E2E` and `002D8620` —
the per-element emit loop.

Naming each kind by what is actually wired:

- **Kind 0 — the full-pipeline element.** Written by `002B3C30` (`002B3C40`) and `002B3D50`
  (`002B3D78`), which the `002B32xx` shared wrapper (`002B3354`/`002B3384`) and the widget-side
  builders at `002A1C86` and `002A3551` call. Full row: numeric format (`002A9980`), text draw
  (`002A8C50`), and emitter `002A9F00` — which cooperates with the control-code engine
  (`002AC5F0` calls `002A9F00` four times, §6c).
- **Kind 1 — the control-code-free sibling, never instantiated.** Identical columns 0/1, but its
  emitter `002AA800` is the only one of the three that **never calls `002AC5F0`** — it resolves a
  per-element resource (`[rcx+0x44]>>11 & 1` selects the `0039C4A0` lookup, `0020E600` resolves
  `[rax+0x14]`), seeds `23.0f` at `r14+4`, and walks the raw string itself. `GJ-11` established no
  cluster-side code writes `1` — the shipped flow has no control-code-free elements, so `002AA800`
  is reachable through the table but unused in practice.
- **Kind 2 — the handler-less element.** `002B3400` (the block's own initialiser — 19 callers,
  ~~gated on `00254A10()==0`, i.e. region word `01E02814`, shipped `0x0A`~~) writes `2` at `002B3470`. *(Corrected 2026-09-30, SWE2-DATA: the stamp is unconditional. The `00254A10() == 0` test gates only the branch that sets flag `0x800` and resolves `+0x60` when byte `+0xA6` is 7. The predicate reads the mode dword `01E02814` through a one-instruction getter; its `.data` initial value is `0x0A`, and with that value the predicate is 1 and the branch is skipped. `_index/candidates/dd-data-3-0930/dispatch_checks.py` D1, D2.)*
  Its row is null in **all three columns**, so every dispatcher's null test skips it: a kind-2
  element formats nothing, draws nothing, and emits nothing through this table. Whatever renders
  kind-2 content is outside the dispatch — and if a kind-2 element ever reached `002AFCB1`, the
  unguarded indexed call would jump through a null. The emit path's implicit precondition is
  `+0xA3 ∈ {0, 1, 3}` — the same unbounded-selector hazard §3 already flags.
- **Kind 3 — the message-window run.** Written at `002A49CA` inside `002A4830`, whose **only**
  caller is `002A6329` inside `002A6190` — the message-window procedure (the same body whose
  id-2 arm drives `01E0CDC8`, §4a). `002A4830` iterates `[rcx+0x3C2]` elements and builds the
  colour-modulated record (RGBA from `[r13+0x90..0x93]` scaled by `[r13+0x5A]>>7`). Kind 3 has
  only column 2 wired — `002AAE40`, which **does** call `002AC5F0` — because the window supplies
  its own layout and the format/draw columns don't apply.

**What this does to `GJ-7`.** The drawer-to-text mapping gains its first concrete half: `002AAE40`
serves the message window's own elements; `002A9F00` serves every kind-0 element (the general
tagged-text case) plus its direct callers; `002AA800` is the provisioned-but-uninstantiated raw
variant. The residual that remains is naming *which* on-screen strings funnel into kind 0 versus
kind 1 — the kinds are now identified~~, the string census is not done~~. *(Corrected 2026-09-30, SWE2-DATA: GJ-7 answered it by builder on 2026-09-25 (§7). Kind 0 is the message window's page text, and kind 1 has no builder.)*

**Residuals, kept honest.** (a) The image has no vocabulary for the kinds — these are mechanism
names, and any richer naming would be inference. (b) Kind 1's instantiation path is unfound: if a
kind-1 element is ever authored it is created by a writer outside the `+0xA3` byte-write census's
cluster, or the selector is set by a non-plain write (the `Presentation` group's `or`/`and` bit-0
ops write the same offset on a different structure). Registered as **SD-107** (SWE2-DATA, 2026-09-30). (c) The emit dispatch is unguarded — a
selector of 2, or ≥4, at `002AFCB1` is a wild call; shipped code never produces one cluster-side.
*(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19): (b) is SD-107, answered by the record published in
`59ec09a95`. The writers outside the cluster and the non-plain writes are typed, and none builds a kind-1 text
element. See the SD-107 note in §7.)*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `01E0CDC8` has 2 writes and 6 reads, both writes in `002A6190` | rip-relative sweep of every function body, write/read split by operand position | 1 |
| Both writes are in the **message id 2** arm | the 21-entry table at `002A698C` decoded, targets mapped to ids; `002A6412` is id 2's and is the greatest target below `002A6464` | 1 |
| `01F82E38` initialises to **0** | it lies past `.data`'s `SizeOfRawData` in the section header — no raw bytes back it | 1 |
| `01DFE0C0` ships as **1** | raw `.data` bytes at its file offset, with the raw-backing test stated per cell | 1 |
| Nothing writes `1` to the block's `+0xAC` | byte-write sweep at `+0xAC`, `+0x16C`, `+0x17C`, `+0x18C` — every embedded base ~~the nine callers use~~ its callers use *(corrected 2026-10-02, OPUS: five functions, six sites)* — plus the three stack frames read at their own displacements | 1 |
| The four drawers call no imports | indirect-call census against every resolved IAT slot | 1 |
| The four reference no strings directly | rip-relative operand scan over each body | 1 |
| Only `"display : draw Font"` appears within two calls | downward call-cone walk, 161 functions below `002AC5F0` | 1 |
| `002AAE40` has one pointer in the image, at `00916518` | 8-byte scan of every non-`.text` section, **each hit verified by reading the value back through its VA** | 1 |
| The table is four rows of three at `009164C0` | the qwords read from the image, to the start of the powers-of-ten table | 1 |
| Stride 3, selector `byte [rcx+0xA3]`, signed | `movsx` + `lea rdx,[rax+rax*2]` in all three dispatchers | 1 |
| Three dispatchers, columns 0/1/1 | the `lea` target of each: `009164C0`, `009164C8`, `009164C8` | 1 |
| `002ABEC0`'s guard | `cmp byte [rcx+0xAC],1` / `cmp dword [01E0CDC8],0` | 1 |
| Column 0 is numeric | `002A9980` takes the address of the powers-of-ten table at `00916520` | 1 |
| Column 1 reaches the font drawer | `002A8C50` is a direct caller of `002AC5F0` | 1 |
| `0209CC40` has 121 reference sites | image-wide rip-relative sweep | 1 |

**Controls.** The absence claim *"no dispatcher references column 2"* is a measurement: the same sweep
that found one reference to `009164C0` and two to `009164C8` found **zero** to `009164D0`, so the zero
comes from an instrument that demonstrably reports non-zero for its siblings. *(Pointer 2026-10-01
(SWE2-CONTRACT for OPUS, DD batch 19): the zero stands, but the absence claim does not. §6b is WITHDRAWN
(2026-09-16): `002AF960` indexes column 2 through the image base (`002AFCB1`), which leaves no address reference for
this sweep to find.)*

**A correction made while producing this document.** The first pointer scan reported `002AAE40`'s
pointer at a decimal offset I converted to hex twice, wrongly, and dumped the wrong neighbourhood
twice before noticing the value at the address was not the value the scan claimed. The fix was to
make the scan **verify each hit by reading it back through the VA it reports** rather than trusting
the arithmetic that produced it.

> **An instrument that computes an address should be made to read it back.** The check costs one line
> and turns a silent arithmetic error into an assertion.

## 9. Related

- [`how-a-line-of-text-becomes-glyph-quads.md`](how-a-line-of-text-becomes-glyph-quads.md) — the glyph pipeline below these handlers, and the `"display : draw Font"` scope that names all four drawers.
- [`numeric-formatting-and-character-mapping.md`](../../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md) — column 0's subject.
- [`ui-request-router.md`](../../16-UI/Request-Router/ui-request-router.md) — the UI-owned ancestors of this cluster.

## 10. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only — the shipped image and the function list. Nothing executed.)*

### ✔ The table, the orphan and the boundary all reproduce

| claim | measured |
|---|---|
| four rows of three at `009164C0`, **96 bytes** | **exactly**, including **both null rows** and `002AAE40` at kind 3 column 2 |
| kinds 0 and 1 identical in columns 0 and 1 | `002A9980` / `002A8C50` in both; column 2 differs (`002A9F00` vs `002AA800`) |
| exactly **one** 8-byte pointer to `002AAE40` image-wide, at `.rdata 00916518` | **one, at `00916518`** — the scan re-run over every section |
| the table ends **exactly** where the powers of ten begin | the table ends at **`00916520`** and the powers of ten start there |
| the three dispatchers' caller counts **2 / 3 / 5** | **2 / 3 / 5** |
| `002B3930` indexes column 0 | `lea rax, [rip + 0x662B7D]` → **`009164C0`** |
| `002ABF20` indexes column 1 and publishes `obj[0x8C]` | `lea rax, [rip + 0x66A574]` → **`009164C8`**, and its two globals resolve to **`0209CC40`** and **`0209CC48`** |

**The boundary argument is now exact.** The powers of ten are **nine `u32`**, not qwords —
`1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000` — so they occupy **36 bytes** from
`00916520`. The 96-byte table and the 36-byte constant run abut with no gap, which is what makes
"the table ends where the powers of ten begin" a measurement rather than an impression.

### ➕ §4's listing for `002ABF20` is missing three instructions

As printed, `002ABF20` runs `mov rax, [rax + r8*8]` straight into `jmp rax` — no null test *(answered: see §4's listing, which now carries the `test rax, rax` / `je` pair; 2026-10-02, OPUS)*. The bytes
have one: `test rax, rax` / `je 0x2ABF60` / `ret` at `002ABF58`–`002ABF60`. **So §3's claim that the
null rows "are why every dispatcher null-tests the loaded pointer" is correct, and it is §4's
transcription that is short.** Worth fixing because the two sections otherwise contradict each other
and the reader has no way to tell which is right.

### ○ The selector is signed and **nothing bounds it**

All three dispatchers load it with **`movsx`** — §4 says so — and none of the three compares it
against 4 or against 0. The row index is `selector × 3` and the load is `[base + row×8 + column]`, so
**a selector outside `0..3` reads outside the 96 bytes**, and the *only* thing standing between that
and an indirect jump is the null test on whatever was read. For a negative selector that memory is
the `.rdata` **before** the table; for a large one it is the powers of ten, which are **non-zero
u32 pairs** — a value the null test does not catch.

**This is a contract fact, not a bug report**: the dispatchers' precondition is that `obj[+0xA3]`
is in `0..3`, and it is enforced by whoever writes the byte, not here. **Who writes `+0xA3` was not
censused in this pass**, so the precondition is recorded as unproven rather than asserted to hold.
*(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19): censused since. GJ-11 (ANSWERED 2026-09-22) found that
cluster-side code writes only 0, 2 and 3 to `+0xA3`, all inside `0..3`. §8b gives the narrower precondition of the
column-2 call (`0`, `1` or `3`). SD-107 (record in `59ec09a95`) finds no writer of a kind-1 text element.)*

**Not claimed.** Which text each drawer handles — `PROPOSED-repos9e-6` is untouched, and **no handler
body was read here**. Whether the column-2 handlers are reachable — §6b's argument rests on "no
dispatcher references column 2 by address", which this pass did **not** re-derive. Nothing executed.
*(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19): both are settled since. GJ-7 is ANSWERED 2026-09-25 by
builder (§7). Column 2 is reachable: §6b is WITHDRAWN (2026-09-16), because `002AF960` indexes column 2 through the
image base.)*

*(Pass 22 adjacency, 2026-09-14: the dispatch-table handlers yield to `CoreRuntimeScheduling`
mid-text — `002A8C50` calls `001EDDA0`, `002A9F00`/`002AA800`/`002AAE40` call `0020E600`, and
`001EDDA0` is itself called by `00265880`/`00265860` and `Movement` `0025DF00` (7 edges) — and
`002A9980` reads `Input` `001E0A10` (1). The handlers are the same character-walk family the
sibling glyph pages document, so they inherit that walk's yield points; the input read is a
text-advance check, not an ownership edge.)*

*(Pass 22 live-graph sweep 2, 2026-09-15: `0025DF00` — the movement-side caller of `001EDDA0`
— is itself called by `ActorEntity` `0025D9E0` and calls `003DB640` (7 edges into the actor
layer) — one more shared-helper hop between the dispatch table and the actor bodies.)*

*(Pass 22 live-graph sweep 3, 2026-09-15: `0025D9E0` — the actor caller of `0025DF00` — calls
`Gameplay` `00234150` and `Party` `003590D0` (2 edges); same shared-helper hop, one layer
further.)*

*(Pass 22 live-graph sweep 4, 2026-09-15: `00234150` and `003590D0` reach `CombatAction`
`00308010`/`002FED60` and two more (4 edges) — the gameplay/party callees carry combat neighbours
of their own.)*

*(Pass 22 live-graph sweep 5, 2026-09-15: `002FED60`/`00308010` are called by `Spawn_Encounter_Lifecycle` `0023A410` (2 edges) — the combat callees are shared with spawn\ncode, one more hop out.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — SERVICE.** A cited function calls `BattleStats_RecomputeDerivedStateAndAutoStatuses`.
- **Script_VM_Native_Bridge — SERVICE, 23 edges, one subject.** `0025DF00` — the movement-side pump already traced in the sweep notes above — calls `0025E4C0` (`WorldActorScriptVM_InterpretBytecode`), `00267420` (`ScriptVM_WaitList_HasAnyActorChannelActive`), `00357760` and `00357770`. The crossing is that the loop ticks the script interpreter and polls the actor-channel wait list between drawing steps; a script VM sits behind the pump, not just movement code.

### Three more, from section 4a's sources (FABLE, 2026-09-21)

- **Developer — MECHANICAL.** `001EBA40` is the singleton the suppressor's only caller `00184960`
  reads a byte from (`[001EBA40() + 0x118]`) before deciding whether to clear `01DFE0C0`. This page
  cites it to say **what the condition reads**, not to describe it; one accessor, no shared
  responsibility.
- **Resource — MECHANICAL.** `001AD780` appears in section 4a only as one of the byte writers the
  `+0x16C` displacement sweep returned, and it is there to be **ruled out**: it writes
  `[rcx + rdx + 0x16c]` on an object of that layer, not on this cluster's text-draw block. A negative
  result's listing, not a crossing.
- **Story_Event_Quest_Hunt — MECHANICAL.** `002A3F90` is the call the message window's id-2 arm
  makes immediately after restoring the latch (`002A65DE`), quoted so the restore's position in the
  arm is visible. Its callee `0032A8A0` is that layer's; nothing on this page reads its behaviour.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — SERVICE.** `0023A410` on this page calls `BattleStats_SetCurrentHP`, owned by that layer. What it reaches is **eight bytes** that turn the delta-based HP path into an absolute set: it subtracts `dword[+0x48]` from the value it is given and jumps straight into the modification entry point - which is what fixes `+0x48` as the current value; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**Audio — MECHANICAL, 21 edges.** `007E7540` calls `007B58C0`, `007CF980`, `007CFD00`, `007CFE60` and 12 more; `001EDDA0` is called by `003B99D0`; `ActorManager_RunFieldRuntimePass` (`0025D9E0`) calls `00261F90`; `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) is called by `00362850`; `007E73F0` is called by `007BFD00`; `007E7540` is called by `007B52B0`.

**Developer — MECHANICAL, 1 edge.** `001EBA40` is called by `001C6320`.

**Resource — MECHANICAL, 1 edge.** `001AD780` is called by `001A7A50`.

**Save_Load_Settings — MECHANICAL, 6 edges.** `ActorManager_RunFieldRuntimePass` (`0025D9E0`) calls `SaveImage_GetPersistentPayloadBase` (`002EF2B0`), `SaveWrite_GetBusyFlag` (`00583920`); `001EDEC0` is called by `SaveLoad_ControllerLifecycleHandler` (`00582860`); `00254A10` is called by `SaveSlotMetadata_BuildSubmissionDescriptor` (`005832B0`); `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (`0032A8A0`) calls `SaveImage_GetPersistentPayloadBase` (`002EF2B0`); `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (`0032A8A0`) is called by `SaveImage_FinalizeHeaderAndChecksum` (`00583D60`).

**Story_Event_Quest_Hunt — MECHANICAL, 2 edges.** `002A3F90` calls `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (`0032A8A0`); `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (`0032A8A0`) calls `PersistentFlag_QueryAuthoredThresholdSchedule` (`00377970`).

**UI — MECHANICAL, 87 edges.** `001EDEC0` is called by `00252030`, `00276D30`, `0027C870`, `00299090` and 9 more; `00254A10` is called by `00273E30`, `00295D90`, `00298250`, `002A4430` and 8 more; `002B3400` is called by `00243860`, `0027AD70`, `002A86A0`, `003EE420` and 4 more; `002475D0` is called by `00296960`, `00298250`, `0029C770`, `0029C9D0` and 1 more; `00247680` is called by `005599D0`, `0055A1F0`, `0056B4D0`; `002A8C50` calls `002ABF70`, `002AC5F0`, `002B2150`; `002AC2F0` is called by `002AE610`, `002AF340`, `002B2150`; `0017F8C0` is called by `002AF340`, `002B2150`; `001E0A10` is called by `00284EC0`, `0029B870`; `002A6190` calls `002A4430`, `002A4830`; `002A9F00` is called by `002AC5F0`, `002AE610`; `002AAE40` calls `002AC5F0`, `002B2150`; `002AC5F0` calls `002AE610`, `002B2150`; `002AC5F0` is called by `002AF340`, `002B2150`; `002AF960` is called by `002A4430`, `002A4830`; `002B0280` calls `002AE610`, `002B2150`; `002B0280` is called by `00243860`, `002A86A0`; `002B24B0` calls `002AF340`, `002B2150`; `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (`0032A8A0`) is called by `00281AE0`, `0029C530`; `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) is called by `00299BD0`, `002C7660`; `0039C4A0` is called by `002AC5F0`, `002AE610`; `003FFAB0` is called by `002A86A0`, `002AC5F0`; `001EDDA0` is called by `0024B9B0`; `001EDE80` is called by `003FA790`; `002465F0` is called by `00247AE0`; `002A4830` calls `002AF960`; `002A9F00` calls `002AC5F0`; `002AF960` calls `002B2150`; `002B3C30` calls `002B2150`; `002B3D50` calls `002B2150`; `003FFB00` is called by `002AC5F0`; `003FFF10` is called by `002AC5F0`.

**World — MECHANICAL, 3 edges.** `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) is called by `0025E400`, `002623A0`; `ActorManager_RunFieldRuntimePass` (`0025D9E0`) calls `0025E400`.

**WorldAreaField — MECHANICAL, 8 edges.** `ActorManager_RunFieldRuntimePass` (`0025D9E0`) calls `002677B0`, `WorldTransition_GetOptions` (`003148D0`), `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`), `WorldTransition_SetOptions` (`00314DA0`) and 3 more; `ActorManager_RunFieldRuntimePass` (`0025D9E0`) is called by `World_UpdateSimulationTick` (`00314020`).

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-text-element-dispatch-table-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `002477A0` | 108 B | when `rcx` is non-null, replaces bits 16-18 of dword `rcx+0x44` with `dx AND 7` and reads them back; with bit 18 set it stores 0xF9 to byte `+0xAD` when bit 17 is set and 0xF9 to byte `+0xAC` when bit 16 is set, leaving each byte unchanged otherwise; with bit 18 clear it stores 0xF9 (bit 17 set) or 6 (clear) to byte `+0xAD` and 0xF9 (bit 16 set) or 6 (clear) to byte `+0xAC`; a null `rcx` returns at once | `002477A8`, `002477B8`, `002477C4`, `002477CE`, `002477F2` |
| `0029B870` | 720 B | with `w` = word `02F9736A`, `v` = word `02F9736C` and `b` = signed byte `rcx+0xB48`, tests `w` in turn against word `01E0C2A4` (0x4000), bit 15, mask 0xA0, word `01E0C2A0` (0x2000), 0x400 and 0x800 for the codes 3, 8, 6, 2, 4, 5: on a match it returns the code when qword `rcx+0xB20` is null or `[rcx+0xB20](qword rcx+0xB30, code, b, b)` is non-zero, and on a zero result returns 0 for code 3 but goes on to the next test for the others; past the tests `x`, `y` = bit 6 minus bit 4 of `w`, `v`, and when `e` = `001E0A10()` is non-zero `y` -= `e` and `x` becomes 0 if `001E0E30()` (called either way) is non-zero, else `x` -= `e`; `n` = `002975B0(rcx, b, x, y)`; it returns 0 when `x` and `y` are both 0; when `n` equals `b` it returns 7 if `0029B790(rcx, 7, n)` is non-zero, else 0; otherwise it returns 0 when `0029B790(rcx, 1, n)` is zero, and else ANDs word `+0x318` of 0x160-byte entry `b` with 0xFFFB, ORs 4 into that word of entry `n`, stores `n` to byte `rcx+0xB48` and returns 1 | `0029B889`, `0029B8BC`, `0029BA69`, `0029BAAC`, `0029BB12` |
| `0029C770` | 216 B | with `w` = `rcx+0x180`, returns 0 when `00273A20(w)` is non-zero; otherwise calls `00245000(w, 0xC0, 005C5230, 0)`, `002974E0(rcx, rcx+0x218)`, `002475D0(w, 0)`, `00247930(w, 9)`, `00247570(w, 002735E0(0))`, `00244960(rcx, w)` and `00246AC0(w)`, ORs 0x80 into word `rcx+0x318+0x160*i` for `i` below unsigned byte `rcx+0xB42`, and returns 1 | `0029C787`, `0029C7AF`, `0029C7F2`, `0029C820`, `0029C838` |
| `0029C9D0` | 219 B | with `w` = `rcx+0xC0`, returns 0 when `00273A20(w)` is non-zero; otherwise calls `00245000(w, 0xC0, 005C5230, 0)`, `002974E0(rcx, rcx+0x158)`, `002475D0(w, 0)`, `00247930(w, 9)`, `00247570(w, 002735E0(0))`, `00244960(rcx, w)` and `00246AC0(w)`, calls `00247930(rcx+0x7C0+0xD8*i, 0xB)` for `i` below unsigned byte `rcx+0xB42`, and returns 1 | `0029C9E7`, `0029CA0F`, `0029CA52`, `0029CA89`, `0029CA9B` |
| `00299090` | 1040 B | switches on dword `[rdx]` through a byte map at `002994BC` and a dword offset table at `002994A0` (read from the image, not the listing); only 0x1, 0x2, 0x6, 0xF, 0x14 and 0x1D have arms: 0x1 calls `002432B0(rcx+0x50, qword +8 of qword 0209AC30, 0x32, rcx)`, stores `0028F830(dword [rdx+8])` as the state record at `+0xC0` with byte `[rdx+8]` in its byte `+0`, calls `00247570(rcx, 002735E0(5))`, stores the `002432B0` result's words `+4`, `+8`, `+0xA` at `+0x98`, `+0x9C`, `+0x9E` and the low word of dword `[rdx+0x10]` at `+0x9A`, calls `00247930(rcx, 3)`, re-seeds the record when its byte `+1` differs from word `+0x80` of its `0xC0`-byte entry in the `0035D320()` table, sets the colour dwords `+0x28`..`+0x34` of qword `+0x18` of qword `rcx+0x60`, and either clears the record again or calls `00225580` with the record's byte `+0x13`, depending on the entry's dword `+0x20` bits 6 and 9 and its words `+0x7C`/`+0x7E` against `0x4000`; 0x2, only when `001EDEC0(dword +0xB4)` is non-zero and word `+0xC8` is 0, calls `002986E0(rcx, entry+0x20)` and `00297290(record+0x18, rcx)` (after `00246AC0(rcx)` when bit 0 of the record's word `+2` is clear) or, once word `+0xCA` has counted to 4, `00244DD0(rcx)`, under the same entry tests and bits 0 and 1 of word `+2`; 0x6 clears bit 26 of dword `+0x20` of qword `[qword rcx+0x60]`, re-seeds the record when its byte `+1` differs from the entry's byte `+0x80` or bit 1 of its word `+2` is set, then sets bit 0 of word `+2` and stores `0xFFFF` to word `+4`; 0xF sets bit 1 and 0x14 clears bit 0 of the record's word `+2`; 0x1D stores 1 to word `+0xC8`; these arms return 0, and every other value, in range or not, calls `005C5230(rcx)` and returns its result | `002990AC`, `002990D1`, `00299333`, `00299406`, `00299488` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-the-text-element-dispatch-table-1002/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `002A2860` | 70 B | `002A6190` + 0x79A | returns when word `rcx+0x3F0` is 0 or below (signed); otherwise zeroes byte `+0x3F3` and word `+0x3F0`, passes qword `+0x3F8` to the call at `002A2860` + 0x2A and tail-jumps (`002A2860` + 0x3B) with qword `+0x400` | Interior anchor `002A2871`; Interior anchor `002A2875`; Interior anchor `002A287C`; Interior anchor `002A288A`; Interior anchor `002A289B` |
