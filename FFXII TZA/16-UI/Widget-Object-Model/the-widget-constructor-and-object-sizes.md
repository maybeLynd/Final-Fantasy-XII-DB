---
system: The widget constructor, and what an object's size tells you
category: 16-UI
status: "DOCUMENTED — every register row is closed (UQ-187..UQ-190 answered 2026-09-17); the SECTION-04 return/receiver additions were accepted by a non-author review (SWE2-AUDIT-SPEC, FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929: the section-04 evidence package byte-verified, receiver audit 16/16). Owner re-status 2026-09-30 (OPUS)"
owner_layer: CodeDomain — UI object model
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: "additive-annotation delta - every function this document cites whose record differs between the stamped snapshot and GN161's gained a plate comment and tags ONLY (empty comment before, tag set a subset, checked field by field), and this document makes no uncorrected absence claim about any of them; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30"
    verified: "1 cited address(es) among the 128 records changed across GN158..GN161; each differs only in comment and tags; 0 live absence claims (check_stranded_absence.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS"
    adjudicated: OPUS-REQ-FABLE-DELTA-RELIANCE-BASIS; re-measured and applied for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708, on SNAPSHOT-IDENTITY - replaced rather than re-targeted because that basis is FALSE for this document, which cites a record that changed
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-widget-constructor-pass-1
  crossref_clean: false
  reopened_count: 1
---

# The widget constructor, and what an object's size tells you

This document was reached from a *pair frontier* row — `+0x61B0`, two touchers, no document naming
both. **The two functions turn out not to share a field at all in the way the row implies: one
constructs the other's object and hands it an argument.** The link is a `lea rip` and an immediate,
neither of which is a struct-field reference, so no field census could see it.

**Extents checked**: `002465F0` 395 B, complete, ends `ret` at `0024677A`; `00245000` 31 B, complete;
`00276650` 282 B, complete; `00273A20` 9 B and `00244F00` 68 B, complete; sites in `00279E20`
(3006 B) read in context.

## 1. What the player sees

Every menu, window and panel in the game is one of these objects. **A parent builds its children
inside its own allocation** — the battle command window's sub-panels are not separately allocated,
they are slices of the parent — and the constructor **calls the new object's handler once, during
construction**, so its initialization-message handler runs before its parent's constructor has returned. This is not proof that a frame/tick has elapsed.

## 2. Native mechanism

### 2.1 One constructor, and it takes the object's size as an argument

`002465F0(object, size, handler, locals, flag)`:

```asm
00246607  mov   rbx, r8                  ; save the handler before r8 is reused
00246612  movsxd r8, edx                 ; the SIZE becomes memset's count
00246618  xor   edx, edx                 ; fill = 0
0024661D  mov   rdi, rcx
00246626  call  0x861ec0                 ; memset(object, 0, size)
0024662B  test  rbx, rbx
0024662E  lea   rax, [rip + 0x37ebfb]    ; = 005C5230, the default handler
00246635  cmove rbx, rax
00246641  mov   qword ptr [rdi], rbx     ; the handler is installed at object + 0
```

then a fixed header initialisation, and finally:

```asm
00246738  mov   rax, rbx
0024673B  test  rbx, rbx
00246740  lea   rdx, [rsp + 0x20]
00246745  mov   rcx, rdi
00246748  call  rax                      ; the handler runs once, here
```

**So the second argument is a byte count, not an offset.** That is the single fact the whole
document turns on, and it is worth stating how it was nearly missed — see 6.

`00245000` (31 B, complete) is a thin wrapper: it sets the fifth argument to `1`, calls `002465F0`,
and **returns the object pointer**, which is why callers can write `mov rdi, rax` straight after.

### 2.1a. The raw initializer and wrappers have different return guarantees

SECTION-04 (2026-09-22) checked the complete original initializer and native controls.
`002465F0` leaves RAX from its final timing predicates, not a restored object pointer;
selected cases return 1 and 0. *(Anchored 2026-09-30, OPUS: after the handler call, RAX is `001EDDA0`'s answer
when that is non-zero (`0024674A`, `00246751 jne` to the epilogue), otherwise `00314960`'s (`00246753`); nothing
after that writes RAX before `0024677A ret`. The SECTION-04 native control W04-4 ran the 1 and 0 cases,
[review](../../_experiments/evidence/continuation-section04-widget-receiver/REVIEW.md).)* `00245000` and `00244F50` explicitly restore the object in
RAX. Caller code must not treat a direct `002465F0` return as the object address.

### 2.1b. A message, a consumer and an asset widget are three different objects

The [title asset case](the-title-asset-singleton-and-its-distinct-consumer.md) corrects two
canonical field supports. `003939F7` reads the message in RBX; `00393A23` is an arithmetic
LEA after RBX was cleared. Valid asset-widget reads later use a pointer separately loaded
from `02AEE4C0`. Matching offsets or visiting every body that mentions a global cannot
establish receiver identity. Selected fixed-offset support is now independently checked;
this is not a general whole-game scanner certification.

### 2.2 The header the constructor always writes

| field | value | anchor |
|---|---|---|
| `+0x00` | the handler, or `005C5230` when null | `00246641` |
| `+0x40` | flags, `or 0x80A`, with bit `0x20000` from a global and bit `0x4000` cleared | `00246653`, `002466D1` |
| `+0x44` | low word set to `0x64` = 100; bits `0x70000` cleared | `002466FA`, `00246670` |
| `+0x48` | `00915198` — a fixed table pointer | `00246687` |
| `+0x98` | `0` | `00246711` |
| `+0x9C` | `0x800080` | `00246717` |
| `+0xA0` | `0x80` | `0024670A` |
| `+0xA1` | `0xFF80` | `002466E6` |
| `+0xAC`, `+0xAD` | `6` or `0xF9` (`-7`), chosen by two bits of `+0x44` — **which this constructor has already cleared**, so the value is always `0` and **both bytes always receive `6`**. `00246670` clears bits `0x70000`; `0024667E`-`00246684` reads those same bits back (`shl edx,0xd / sar edx,0x1d`). The `0xF9` arm is **unreachable from this function**. Corrected 2026-09-08; found because six mutants across the reconstruction's copy of this branch compiled to byte-identical code, which only happens when the compiler proves the code dead. See `WD-1` | `002466C1`, `002466CB` |
| `+0xB8` | `0x3F800000` — **1.0f** | `00246700` |
| `+0xB4` | `1`, but only inside `World_UpdateSimulationTick` and only at 60 Hz in mode 0 — **this is a half-rate phase counter**, see §3a *(2026-09-30, OPUS: §3a is [the widget contract's](CONTRACT-widget-object.md), where "60 Hz in mode 0" is HALFRATE (`01F82E38` set, `01DFE0C0` clear); the same reading as `UQ-188` in §7)* | `0024675C` |

**Every widget in the game starts with a `1.0f` at `+0xB8` and a `100` at `+0x44`.**

> **The handler installed at `+0x00` answers a numbered message protocol**, enumerated over the whole
> population in [the widget message protocol](the-widget-message-protocol.md): **297 constructor transfer
> sites, 267 distinct handlers, 32 distinct message ids** (regenerated 2026-09-15 on the proc-slot
> rule; was 280 call sites / 251). The census below counts 49 sites because it
> looks only at direct `00245000` / `002465F0` calls; **most widgets are built through `00244F50`**,
> which forwards its `rdx` to the same constructor.

### 2.3 The census: 49 sites, 26 object sizes

`Tools/work/h78/widget_constructor_sites.tsv` — every call of `00245000` or `002465F0`, with the
handler recovered from the preceding `lea r8, [rip …]` and the size from the preceding
`mov edx, imm`.

| | |
|---|---:|
| call sites | **49** |
| distinct object sizes | **26** |
| sites where no size was recovered | 2 |
| sites where no handler was recovered | 2 |

Sizes: `0xC0`, `0xC8`, `0xD0`, `0xD8`, `0xE8`, `0xF0`, `0x100`, `0x110`, `0x148`, `0x158`, `0x160`,
`0x190`, `0x1C0`, `0x1E0`, `0x2B8`, `0x3D0`, `0x4A0`, `0x4C0`, `0x500`, `0x650`, `0x1110`, `0x1620`,
`0x2DC0`, `0x3010`, `0x61F0`, `0xBC08`.

**The four sites that failed are reported rather than dropped.** A recovered size requires a literal
`mov edx, imm` within nine instructions and no intervening `call`; a size computed at runtime, or
passed through, is not recovered and is left blank. **The handler rule needs a window of at least
sixteen instructions** — stated here 2026-09-13 because it was not, and nine gives five blanks
instead of two (§9).

> **The four blanks are two sites, both wrappers (2026-09-17, FABLE, `UQ-190`).** `00244FCD` is the factory
> `00244F50` calling the constructor with its own arguments, and `00245011` is the in-place constructor
> `00245000` doing the same with caller-owned storage; the size and handler live one frame up. The
> factory's own callers, which this census never keyed on, are 203 functions at 240 sites; four compute
> their size instead of passing a literal (`UQ-190`, §7).

## 3. The `+0x61B0` case: what the frontier row actually was

`00276650` builds a `0x61F0`-byte object whose handler is `00279E20`:

```asm
002766D1  lea   r8, [rip + 0x3748]      ; = 00279E20, the handler
002766D8  mov   edx, 0x61f0             ; the object's size
002766DD  mov   rcx, rsi
002766E0  call  0x245000
002766E5  and   dword ptr [rsi + 0x61cc], 0xfffffeff
002766F7  mov   qword ptr [rsi + 0x61b0], rdi     ; arg 2, stored for the handler
0027670D  mov   word ptr [rsi + 0x61b8], r14w     ; = 1
```

and `00279E20`, running as that handler, reads it back and passes it down:

```asm
0027A58D  mov   rax, qword ptr [rbx + 0x61b0]
0027A594  mov   qword ptr [rdi + 0x2fe8], rax     ; into the child
0027A59B  mov   ecx, dword ptr [rbx + 0x61bc]
0027A5A1  mov   dword ptr [rdi + 0x2fe0], ecx
```

**So the two functions are a constructor and its handler, and `+0x61B0` is the argument passed
between them.** The census saw "one write, one read" and inferred a shared field; the actual
relation is a construction handoff.

### 3.1 The children live inside the parent

```asm
0027A410  imul  rax, rcx, 0x3010        ; index * child size
0027A417  lea   rcx, [rbx + 0xc0]       ; the child array starts at parent + 0xC0
0027A421  add   rcx, rax
0027A428  mov   edx, 0x3010
0027A42D  call  0x245000                ; constructed IN PLACE
0027A439  mov   rdi, rax
```

**`0xC0 + 2 × 0x3010 = 0x60E0` exactly**, and `0x60E0` is independently the base of a sub-object that
`00279E20` takes the address of at **seven** `lea rcx, [rbx + 0x60E0]` sites, passing it to
`00273A20` (9 B: `cmp qword ptr [rcx], rax`, an is-non-null test) and `00244F00`.

> **So the array holds at most two children — three would need `0x90F0`, past the end of a `0x61F0`
> object — and the layout leaves room for exactly two.** That is an **arithmetic bound, not a loop
> bound.** There is no loop here: the index is `0027A409 and ecx, r15d`, and `r15d` is `1` on three
> paths but `esi` at `0027A1D6`. **The count is constrained by the geometry and not read from the
> code**, and this document does not claim otherwise.

Both parent and child keep this pointer near the end of their block — `0x61F0 − 0x61B0 = 0x40`,
`0x3010 − 0x2FE8 = 0x28`.

## 4. Why this matters to the field censuses

**A displacement is only meaningful within one object type, and this gives object types a size.**
Any function that appears as a `handler` in the census receives, as `rcx`, an object of the size on
that row — so its `[rcx + disp]` accesses are fields of a known-size object, and two functions with
the same displacement but different object sizes are **not** touching the same field.

**And it is a third way for a field access to be invisible to a displacement census**, distinct from
the two already recorded:

| mode | why the census misses it | example |
|---|---|---|
| base materialised by `lea` | later accesses carry a small or zero displacement | `lea r12, [r14 + 0x2348]`, then `[r12 - 0x24]` |
| offset folded into a scaled index | no displacement in the instruction at all | `add rax, 0xcd; imul rax, rax, 0x2c` |
| **size or offset passed as a value** | **the constant is an immediate to `mov`, never an address** | **`mov edx, 0x61f0; call 0x245000`** |

**The third mode is the one that hides whole objects rather than single fields**, because the
constant that would tell you the object's extent never appears in a memory operand anywhere.

**A scan for the first mode, run over the whole image for this record:** only **4 functions** take a
`lea` into `[0x6000, 0x6400]`, at 11 sites, and **two of those are 32-bit `lea ecx, …`** — arithmetic
on an id, not an address (`00322C50` computes an encoded-id base of `0x6000`; that function is read
in the authored-table registry document). **Of the transitive callees reached from the two functions
that do receive `parent + 0x60E0` — 10 functions to depth 3 — none accesses `+0xD0`**, which is where
`+0x61B0` would appear through that base. **So for this field the first mode is measured absent
rather than assumed absent** — but "no writer found" remains not a finding.

## 4a. Call chain (OPUS, 2026-09-30)

From the facts this page and its §7 answers cite:

- **Construction.** A caller builds a widget through one of three doors:
  - the factory `00244F50`: ~~203 functions at 240 sites~~ 247 call/jmp sites in 206 functions at HEAD (UQ-190
    counted 240 in 203 on the 2026-09-17 function list) *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../../_index/candidates/auditspec-review-dd-1599-a-0930/REVIEW.md) correction wording)*, 0 rewritten to `0xC0`, pool or heap;
  - the in-place constructor `00245000`: caller-owned storage, fifth argument 1;
  - `002465F0` directly.

  All three end in `002465F0`, which zeroes `size` bytes (`00246626`), installs the handler at `+0` (default
  `005C5230`), writes the header of §2.2, and calls the handler once (`00246748`).
- **The battle-menu instance (§3, §7).** UI requests 1 and 4 run `0035D660` → `0028FD50`, which raises bit 4 of HUD
  `+0x10F68`. The UI update group `00290CF0` then runs `00276650`, which calls `00245000` with `0x61F0` and handler
  `00279E20`. That handler builds its two `0x3010` children in place through `00245000` (`0027A42D`).
- **Every frame.** The list drain `00248030` reconciles generations on `+0x40` bit 17 and advances the half-rate
  counter `+0xB4`. Its readers `00241D40` and `00252030` gate their update on `001EDEC0(+0xB4)` (UQ-188). A widget's
  handler receives the numbered messages of [the message protocol](the-widget-message-protocol.md).

## 5. Modding notes

- **Every widget's size is a literal `mov edx, imm` at its construction site**, so the object layout
  budget is patchable per widget type — and `002465F0` zeroes exactly that many bytes.
- **The handler is stored at `object + 0`** and is called once during construction. Replacing the
  `lea r8, [rip …]` at a construction site redirects that widget's behaviour entirely.
- **A null handler becomes `005C5230`**, so a widget can never have an absent handler.
- **`+0xB8` is `1.0f` and `+0x44`'s low word is `100`** on every widget, whatever its type.

## 6. Corrections made during this read

**Three, all caught before anything was written down.**

- **`edx` is a size, not an offset.** The scan that produced the 49 sites originally labelled the
  column `offset`, and the reading built on it was "the offset where the state block lives".
  `00246612 movsxd r8, edx` into a `memset` count settles it. **A column name is a claim.**
- **`00861EC0` is not a function body.** It is the first entry of a block of `jmp qword ptr [rip …]`
  import thunks; its IAT slot is `008C2A60` and the ledger's `memset` name comes from the import
  table. The zeroing claim rests on **the import name plus the argument pattern** (`dest, 0, count`),
  **not on a body anyone read** — the body is in a system DLL. This is exactly the thunk ambiguity
  the named-not-cited checker warns about, met in the wild.
- **"Two children" was nearly asserted from a mask.** `and ecx, r15d` looked like `and ecx, 1` until
  `r15d` was traced to all four of its assignments and one of them is `mov r15d, esi`.

## 7. What is not known

- [x] ~~What kind of widget the `0x61F0` object is. `BattleMenu_UpdateCommandSelectionAndDispatch`
      (`002778C0`) is one of the 49 constructors and sits in the same address family, which is
      **suggestive and not evidence**; nothing read here names this object.~~ **Answered 2026-09-12 (FABLE): the battle
      menu.** Traced from its request rather than its address: the routes of UI requests 1 and 4 (`0035D660` → `0028FD50`) store the request id at HUD `[0209BE80] + 0x10F60` and set bit 4 of `+0x10F68` (`0028FD57`–`0028FD65`); the UI update group `00290CF0` (the per-frame gate's `0x2000` group) takes that bit (`00290D31`–`00290D39`), refuses while a UI request is posted (`02092730`, `00290D3F`), and builds the object at HUD `+0xAB30` through `00276650` with the id word `+0x10F60` (`00290D8F`–`00290DC0`), then clears bits 4 and 10 (`00290DC7`). UI request 1 is the Battle Menu open (the
      router's identified-requests table, triggered by the Decide mask or Square), so the `0x61F0` object with handler
      `00279E20` is **the battle menu widget**, and request 4 opens the same widget with its own id.
- [x] ~~**UQ-187.** What `00915198` (the fixed `+0x48` table) holds.~~
      *Narrowed 2026-09-14 (FABLE), not answered:* it is the **default animation record**, the one a widget's `+0x48` points at until an
      animation is started. Three sites load it:
      - the constructor `002465F0` (`00246677`);
      - the animation starter `00246AD0` (`00246B9C`), which uses it unless the widget supplies its own
        ([starting a widget animation](starting-a-widget-animation-and-the-millisecond-that-becomes-frames.md));
      - `00247570` (`00247578`), which puts it back.
      ***NARROWED 2026-09-17 (FABLE): the record's consumed layout is read, and the two `1` words are consumed by nothing found.** Three functions read the record a widget's `+0x48` (and, once started, `+0x68`) points at: the starter `00246AD0` reads `u16 +2` (the duration); the evaluator `00244A20` reads **byte `+0`** (a mode, used unless `+0x7C` bit 6 supplies an inline 3-bit mode, `00244A54`–`00244A61`), **byte `+0xA`**, **byte `+0xB`** and **byte `+0xC`** (each decremented - per-channel selectors, `00244A80`, `00244C66`, `00244CCF`) and **float `+0x10`** (`00244D32`). In `00915198` every one of those is zero: mode 0, duration 0, selectors 0, `0.0f` - **the default record is a no-op animation**, which is why a widget can carry it from construction. The `u32 1` at `+4` and the `u32 1` at `+0x18` have no reader among the three consumers, and a scan for reads through `+0x68`'s pointee over the UI range finds none; what they would select is not readable from a reader that does not exist. Cross-linked with `UQ-184`.*
      ***NARROWED 2026-09-17 (FABLE, second pass): the two `1` words are one field.** The record is two `0x14`-byte halves, forward at `+0` and backward at `+0x14`: the backward starter `00244DD0` binds `+0x68` to `+0x48 + 0x14` (`00244E80`..`00244E88`, default `009151AC`) and reads its duration at `+2` (`00244E9C`), so `+4` and `+0x18` are the same `u32 +4` of each half. What that word selects is still unread: the curve kind the stepper hands `00248F40` is bits 10..13 of the widget's `+0x80` (`00246CD5`), not the record. See [the animation page](starting-a-widget-animation-and-the-millisecond-that-becomes-frames.md)'s `UQ-184`.*
      ***ANSWERED 2026-09-17 (FABLE): `00915198` is the default transition descriptor, two `0x14`-byte halves (forward at `+0`, backward at `+0x14`) whose every consumed field is zero, and the one word left, `u32 +4` of each half, is read by nothing in the image.** The halves are the animation page's finding (UQ-184): the forward starter binds `+0x68` to the record and the backward starter to the record plus `0x14`, so the two `1` words at `+4` and `+0x18` are the same field of the two halves. Its readers were searched three ways. A rip-relative census over `00915198`..`009151BF` finds exactly four references, all to the halves' bases: the constructor `002465F0` (`00246677`), the forward starter `00246AD0` (`00246B9C`), the resetter `00247570` (`00247578`) and the backward starter `00244DD0` (`00244E59`, at `+0x14`); no instruction addresses `+4` or `+0x18` directly. A register-tracked scan over every function in the image for a load through widget `+0x48` or `+0x68`, or of the default record's address, followed by a read at `+4`..`+7` or `+0x18`..`+0x1B` of the pointee, finds reads in 34 functions, none in the widget or menu ranges and all at `+0x18`..`+0x1A` of other object types. And the stepper's curve kind, the field a `1` there would most plausibly be, comes from the widget's own `+0x80` bits 10..13 (`00246CD5`), not from the record. So the word is a format slot the build carries without reading, value 1 in both halves of the default. Static, the three searches and the consumers read.*

      Its first 32 bytes are `u16 0`, **`u16 0`** (the duration field at `+2`, so a zero-length default), `u32 1`, twelve
      zero bytes, `u32 1` at `+0x18`, and `u32 0`. What the two `1` words select was not read.
- [x] ~~**UQ-188.** What the two globals at `0024665F` and `00246753` gate.~~
      *Narrowed 2026-09-14 (FABLE), not answered: both are creation-context flags copied into the new widget; what the widget does with
      them was not read.*
      - **Near `0024665F`: widget `+0x40` bit 17.** The constructor `002465F0` copies bit 0 of `0208ED5C` into `+0x40` bit 17
        (`00246639`–`00246650`). When `0208F560` is non-zero (`00246659`) it writes the same bit again (`00246665`–`0024666D`).
        Four functions touch the pair:
        - `002481A0` flips `0208ED5C` and sets `0208F560 = 1`, and `00248190` clears `0208F560`. They are called in six
          matched pairs from `0025058D`–`00250914`, so widgets built inside such a bracket see the flipped value.
        - `00244630` sets `0208ED5C = (arg != 0)` (one call, `00228204`), and `00244620` reads it (`0022899C`).
      - **At `00246753`: widget `+0xB4 = 1`.** This is set when `001EDDA0()` returns 0, which happens only in **HALFRATE**
        ([settings page](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)), **and**
        `00314960()` is non-zero. `00314960` returns `022C2548`, which `World_UpdateSimulationTick` sets to 1 at `00314047`
        and restores at `0031435D`. So the flag marks a widget created inside the world tick while the game runs at half rate.
      ***ANSWERED 2026-09-17 (FABLE): a generation tag and a half-rate drain counter.** *`+0x40` bit 17* has no memory-operand reader anywhere in the image (`test [+0x40], 0x20000` and byte `+0x42` both absent) and exactly one register-form reader: the list drain `00248030`, which loads `+0x40`, does `shr 17 / and 1` and compares the bit with the LIVE `0208ED5C` (`00248073`–`00248080`, and again per child at `002480A7`–`002480B2`, `0024811F`, `0024814E`). A widget whose captured bit equals the current global is skipped; the others are processed - detached through `002482E0` and, when `+0x40` bit 10 is set, walked into their children. So the bit is the widget's **creation generation**, captured from `0208ED5C` at construction (the bracket `002481A0`/`00248190` flips it around six build sequences), and the drain is the reconcile that removes widgets built under the other generation - the protocol page's *message 2, generation reconcile* seen from the flag's side. *`+0xB4`* is a **half-rate drain counter**: the constructor writes `1` when the widget is built inside the world tick at HALFRATE; every drain then calls `001EDDA0()` and, when it returns non-zero (full rate), resets `+0xB4` to 0, otherwise increments it (`00248044`–`00248059`, and the same per list member). Its two readers, `00241D40` (`0024218B`) and `00252030` (`002521DD`), pass it to `001EDEC0(n)` and skip their update when it returns 0: `001EDEC0` returns 1 when the QPC timer is not armed (`01F82E38 == 0`) or `01DFE0C0` is set, else `~n & 1` - so at half rate a widget's per-frame work runs on EVEN drain counts only, and a widget born inside the half-rate tick starts at 1 to land on the alternate phase. Static, bodies read; readers found by a two-form scan (memory operand and register-shift) over the UI range and image-wide.*
- [x] ~~**UQ-189.** What `+0x61CC`'s bits mean — it is the busiest field in the record (54 census sites) and this~~
      document only observes bits `0x100`, `0x400`, `0x800`, `0x1000` being set and cleared.
      ***NARROWED 2026-09-17 (FABLE): the word is a per-message request register, and every bit's writer and consumer is placed; what the messages mean in player terms is the protocol page's unresolved ids.** All 54 image-wide accesses are in four functions - the handler `00279E20` (48), the constructor `00276650` (3), the battle-command reader `00276D30` (2) and `0027AA70` (1). The handler dispatches message ids 1–52 through the byte table at `0027AA38` and the 22-entry jump table at `0027A9E0`; assigning each site to its arm gives: **message 2** (the reconcile arm, `0027A032`–`0027A756`) tests and CLEARS `0x400`, `0x800`, `0x1000`, `0x20`, `0x10`, `0x40` and sets `0x80` and `0x08` along its path - it is the consumer; the raisers are single-bit arms: **42** sets `0x800`, **24** and **49** clear it (49 also stops the animation through `00273A20`/`00244F00`); **50** sets `0x1000` and stores its payload byte at `+0x61E2`; **41** sets `0x20`; **37** clears `0x08`; **48** copies its payload's bit 0 into **bit 13 (`0x2000`)** and **bit 4 (`0x10`)**; **33** copies `payload+0x10` bit 0 into **bit 2**, which **47** reads back (`shr 2`) to derive the words at `+0x61B8`/`+0x61BA`; **46** toggles through a register. Outside the handler: the constructor sets `0x400` and clears `0x100` (so `0x400` is the *first reconcile after construction* one-shot), `00276D30` and `0027AA70` set `0x40` (consumed by the reconcile) and `00276D30` tests `0x2000` (`002775E7`) - the bit message 48 raised. Bits `0x01`, `0x200` and above `0x2000` are never touched. **Residue:** the protocol page lists ids 24, 33, 37, 41, 42, 46–50 as UNRESOLVED, so the bits are named by the message that raises them, not by what the player did.*
      ***ANSWERED 2026-09-17 (FABLE): the bits are a per-message request register, and the narrowing below places every one of them: each bit is raised by one message arm of the handler `00279E20` (42, 50, 41, 48, 33, 46, the constructor and `00276D30`) and consumed by the reconcile arm, message 2, which tests and clears them along its path; the byte table `0027AA38` and the 22-entry jump table `0027A9E0` are the handler's own dispatch tables, cited as tables.** What the raising messages mean in player terms is [the message protocol page](the-widget-message-protocol.md)'s set of unresolved ids, a question of that page, not of this word. Static, all 54 accesses assigned to their arms.*
- [x] ~~**UQ-190.** The two construction sites whose size, and the two whose handler, were not recoverable.~~
      ***ANSWERED 2026-09-17 (FABLE): the two sites are the same two, and both are wrappers forwarding their own parameters.** Site `00244FCD` is inside the factory `00244F50`: it passes `edx = edi` (the factory's own `ecx`, 0 rewritten to `0xC0`), `r8 = rbp` (its `rdx`, the handler) and `r9 = rsi` (its `r8`, the context), with the fifth argument 1 on the pool path and 0 on the heap path through `002497B0`. Site `00245011` is inside `00245000`, a nine-instruction in-place constructor: `rcx` is caller-owned storage, `edx`, `r8` and `r9` pass straight through, and the fifth argument is always 1, so bit 14 of `+0x40` means storage the widget does not own, for an embedded widget as much as for a pool slot. Its two callers build a `0xBC08`-byte widget in place at parent `+0x1B0` plus parity times `0xBC10`, inside the `0x179E0`-byte objects of `002B6350` (handler `002B7B80`, `002B6474`) and `002B9D30` (handler `002BAF80`, `002B9E59`): each call toggles bit 2 of the parent's `+0x179D2` and builds into the sub-widget the new parity selects, a double-buffered pair. So nothing was missing at either site; the census keyed on literals, and at these two the size and handler are the wrapper's arguments. A 2026-09-17 recount of the factory's own callers finds 203 functions and 240 sites; all but four pass a literal size, and the four compute it: `00570BF0` passes `rbx*2 + 0xF0`, `005781A0` passes `rdi*8 + 0x100`, `00564AC0` is itself a wrapper passing `max(0x188, edx)` with the handler from its own `r9`, and `00406E80` picks `0x1F8` with `004079A0` or `0x278` with `00407590` by a branch. Static, bodies read.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The second argument is a byte count | `00246612 movsxd r8, edx` feeding the `00246626` call, with `00246618 xor edx, edx` as the fill | 1 |
| The handler is stored at `+0` and defaulted | `0024662E`–`00246641` | 1 |
| The handler is invoked during construction | `00246738`–`00246748` | 1 |
| `00245000` returns the object | `00245016 mov rax, rbx` after `00245006 mov rbx, rcx` | 1 |
| `00276650` installs `00279E20` for a `0x61F0` object | `002766D1`, `002766D8`, `002766E0` | 1 |
| `+0x61B0` is written by the constructor and read by the handler | `002766F7` and `0027A58D` | 1 |
| Children are built in place at `parent + 0xC0`, stride `0x3010` | `0027A410`–`0027A42D` | 1 |
| `0x60E0` is independently a sub-object base | seven `lea rcx, [rbx + 0x60e0]` sites, and the complete 9-byte body of `00273A20` | 1 |
| 49 sites, 26 sizes | `widget_constructor_sites.tsv`, generated over 38,161 functions with a body | 2 |

**Control on the `lea`-alias absence.** The claim is that nothing reaches `+0x61B0` through a
materialised base. The same scan **positively returns** 11 sites in 4 functions in that displacement
window, and correctly separates the two 32-bit `lea ecx` arithmetic uses from the 64-bit address
uses — so it is not silently returning nothing. The transitive scan likewise **positively decodes**
10 functions before reporting zero hits at `+0xD0`.

**Limit on the census.** The size is recovered by a backwards scan for a literal `mov edx, imm`
within nine instructions, stopping at any intervening `call`. **It is a pattern match, not dataflow**,
and the four blank cells are its measured failure rate at these sites — not a claim that they are
rare elsewhere.

## 9. Related

- [`../the-selection-the-menu-publishes.md`](../the-selection-the-menu-publishes.md) — the menu layer
  above these objects
- [`../Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`](../Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md)
  — authored layout parameters
- [`../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)
  — `00322C50`, the 32-bit `lea ecx, [rax + 0x6000]` that the alias scan correctly excluded

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py --addr 002465F0 --addr 005C5230` run first, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment.)*

Every stated extent is exact — `002465F0` **395**, `00245000` **31**, `00276650` **282**,
`00273A20` **9**, `00244F00` **68**, `00279E20` **3006** — and `005C5230`, the default handler, is
**3 bytes**: `xor eax, eax` / `ret`.

§2.2's header anchors reproduce:

```asm
0024664A  and   ecx, 0x20000                      ; the bit from a global
00246653  or    ecx, 0x80a                        ; the +0x40 flags
00246660  mov   dword ptr [rdi + 0x40], ecx
00246670  and   dword ptr [rdi + 0x44], 0xfff8ffff ; ~0xFFF8FFFF = 0x70000, bits 16-18
00246677  lea   rax, [rip + 0x6ceb1a]             ; -> 00915198, the fixed table pointer
```

### The census reproduces, value for value

Re-derived by scanning every function body for a `call` to `00245000` or `002465F0`:

| | page | measured |
|---|--:|--:|
| call sites | 49 | **49** |
| distinct object sizes | 26 | **26** |
| sites with no size recovered | 2 | **2** |

**And the twenty-six sizes match one for one** — `0xC0` through `0xBC08`, the whole list. The
size rule as stated (*a literal `mov edx, imm` within nine instructions, no intervening `call`*)
reproduces its figure exactly, which is what a stated rule is for.
`Tools/work/h78/widget_constructor_sites.tsv` holds **49 rows**, blank on **2** sizes and **2**
handlers, agreeing with §2.3.

### The handler rule is the one that cannot be reproduced from the text

§2.3 gives a window for the **size** rule and **none for the handler**. Applying the same nine
instructions to the handler yields **five** blanks, not two — the extra three being `002B6474`,
`002B9E59` and `002C0F8A`. They are not failures of the census:

```asm
002B6465  mov  edx, 0xbc08          ; the size, 9 back
   … 16 instructions back from the call …
           lea  r8, [rip …]          ; -> 002B7B80, EXACTLY the TSV's handler
002B6474  call 0x245000
```

For two of the three the `lea r8, [rip …]` sits **sixteen** instructions before the call and
resolves to **precisely the handler the TSV records** (`002B7B80`, `002BAF80`). So the census is
right and **the method as written does not pin it**: a reader following the page gets 47 handlers by
one reading and 44 by another, with nothing in the text to choose between them. One clause fixes it,
and §2.3 now carries it.

> Worth separating from a defect. **The numbers are correct, the TSV backs them, and the size rule is
> reproducible as written.** What failed is the *description* of the second rule — which matters
> exactly as much as the figure does on a page whose whole case is that the census is checkable.

**Not claimed:** §3's `+0x61B0` reading, §3a's half-rate phase counter *([the contract's](CONTRACT-widget-object.md) §3a; OPUS 2026-09-30)* and §6 were not re-derived;
the handler population and the message protocol belong to
[the widget message protocol](the-widget-message-protocol.md) and were not touched. Nothing was
executed or observed live.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role |
|---|---:|---|
| `002B6DB0` | 1033 | widget message body (jump table present, not decoded): `[rbx+0xC8..0xD8]` fields, `00403600`, `002B7210`, `002B6950`, `002B6AE0`, selector resolve `001EDEC0`, `005C5230` |
| `002BA310` | 543 | child-widget create+attach: `[rdi+0xC0]`/`[+0x3D8]`, factory `00244F50`, `002432B0`, `00264150`/`00264770`, `0024ABC0`, `002BA530`, `002D4930`/`002D46F0` |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** A cited function is called by `BattleStats_ModifyStatusLayerStateAndProcessSideEffects`, `BattleStats_RecomputeDerivedStateAndAutoStatuses` and `BattleUnit_RunPeriodicCombatMaintenance`.
- **Script_VM_Native_Bridge - CLIENT (21 edges).** `00203170`, `00264150`, `00265860`, `00265880` (+4 more) are called by bodies filed to Script_VM_Native_Bridge: `0033FAA0`, `00341CB0`, `00345800`, `00346FA0` (+17 more) - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (4 edges).** `0032E400`, `0032E620`, PartyFocus_GetCurrentPackedActorHandle (`003590D0`) are called by bodies filed to World: `0025E400`, `002623A0`, `00378540` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (19 edges).** `00264150`, `002F9920`, `0030CBE0`, `0032E400` (+2 more) are called by bodies filed to WorldAreaField: BattleSystem_RunFieldFrameOrchestrator (`00234590`), MapRef_BeginLoadResources (`00268750`), `003319D0`, `00378030` (+5 more); `002B7B80`, `002BAF80`, `0031BAC0`, `003C05F0` (+1 more) reach bodies filed to WorldAreaField: FieldData_GetActiveFieldRecordBit15 (`00313F60`), WorldTransition_GetActiveOrPendingFieldId (`003148F0`), `00377750` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - SERVICE and MECHANICAL (4 edges).** `00234590` reaches `SpawnGroup_DispatchPendingCompletionSignals` (`00307030`), while `Spawn_ValidateCandidateDistanceToPlayers` (`00234DA0`), `SpawnLifecycle_CheckAndRetireByNativeRange` (`002350C0`) and `00233780` call the shared accessors `00313F60`/`003148F0`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT.** `BattleUnit_ApplyUnitDefinition`, owned by that layer, calls `00322C50` on this page. That caller is the definition apply, and the split is the id: **`definition >> 8`** chooses the authored table while **`definition & 0xFF`** indexes it, which is the same high-byte/low-byte division the record initialiser uses; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `BattleStats_RebuildEffectiveStatsAndAffinityState`, owned by that layer, calls `00322C50` on this page. That caller is the effective-stats re-form, and it says where its output lives: with no explicit destination it writes the record's **own `+0x24` block, `0x24` bytes wide**, and the block at `+0x50`, taking its mode from the flag word at `+0x3C`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Items_Equipment_Shops_License — CLIENT.** `Equipment_CheckItemEligibleForSlot`, owned by that layer, calls `00322C50` on this page. That caller is the slot-eligibility test: the slot index is bounded at 4, the sentinel id `0xFFFF` fails, the item record's `byte[+7] >> 5` must equal the asked-for slot, and when a character record is supplied its `byte[+4]` selects the per-character equip mask that `byte[+9]` is bit-tested against; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Movement — CLIENT.** `FUN_0031bac0`, owned by that layer, calls `00322C50` on this page. That caller is a 668-byte steering computation in a `0x138`-byte frame with a stack cookie, working from the vector at `[+0]`/`[+8]` against the constants `0.6`, `0.8`, `1.0` and `-1.0`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `Reward_ComputeLicensePointsForRecipient`, owned by that layer, calls `00264150` on this page. That caller is the licence-point computation, and it states the formula: the recipient must pass `byte[+5] == 0`, a `byte[+4]` kind test and the `+0x3C`/`+0x64` pair against `0x80000003`, after which the award is `(byte[+0x1C2] - byte[+0x88]) x byte[[+0xE78] + 0x2F] + byte[[+0xE70] + 0x2F]`, **doubled** when bit 4 of the recipient's `byte[+0x6B]` or `byte[+0x7B]` is set; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Story_Event_Quest_Hunt — SERVICE.** `002BA530` on this page calls `PersistentFlag_QueryBank2048`, owned by that layer. What it reaches is the 2,048-bit bank query, and it states its own range: an id at or above **`0x800`** or below zero answers false without touching the bank; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT and MECHANICAL (SWE2-CONTRACT 2026-09-15, 66 edges).** The widget
constructor runs inside the render layer it builds for: the input-consumer state machines
`002BAF80`/`002B7B80` and the analog cursor `002BC3E0` each drive ~5 of this page's bodies and
receive `00404230` back; ~28 edges are `001EDDA0`/`001EDEC0` frame-helper fan-in from render bodies
(`005269B0`/`00528AF0`/`004FF110`/`003D92C0`/`00448DE0`/`002F3BC0`/`003337B0`/`003A8AE0`/`0046EFD0`,
the effect-dispatch `002F4020`, ScreenCapture `002D2DB0`, ShaderMaterial `00366B80`, …); `0024ABC0`
is called by `003F1530`/`003F0610`/`caseD_1`; and `002D46F0`/`00314960`/`00264770` round out the
rest. The constructor is widget-layer machinery the render pass calls directly — the
`001EDDA0`/`001EDEC0` share is mechanical cadence, the state-machine edges are the real client
relationship.

**CoreRuntimeScheduling — MECHANICAL (SWE2-CONTRACT 2026-09-15, 23 edges).** 17 edges are `001EDDA0`/`001EDEC0`
frame-helper calls; 4 are the `0020E600`/`0020E620` image-pointer pair; the last two are `00265860`/
`00265880` reaching `001EDDA0`. Mechanical infrastructure.

**Items_Equipment_Shops_License — MECHANICAL (SWE2-CONTRACT 2026-09-15, 13 edges).** All 13 edges are items-layer
bodies (`BattleStats_SetEquipmentSlotByMappedId`, `BattleIdClassD_*`, `InventoryDerivedIndex_UpdateOnPresenceTransition`,
`Equipment_CheckItemEligibleForSlot`, `Equipment_CheckMatchingSecondaryPartnerSelectedOrOwned`,
`BattleStats_HasRequiredLicenseForAction`/`ForEquipment`, `BattleStats_SetLicenseNodeStateAndApplySideEffects`,
`BattleStats_CheckLicenseNodeAcquireReason`) sharing the single cited helper `00322C50`. Pure fan-in.

**CombatAI — MECHANICAL (SWE2-CONTRACT 2026-09-15, 10 edges).** All 10 edges are `BattleEnmity_*`,
`GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders`,
`GambitConfig_ClassifyActionTargetPairCompatibility` and `AiOrder_EvaluateTargetSelector` sharing
`00322C50`.

**Party — MECHANICAL (SWE2-CONTRACT 2026-09-15, 9 edges).** All 9 edges are `PartyConfiguration_*` and
`PartyFocus_SelectAndRequestDefaultActor` bodies sharing `00322C50`.

**CombatAction — CLIENT and MECHANICAL (SWE2-CONTRACT 2026-09-15, 9 edges).** `002778C0` calls
`BattleUnit_IssueCommandByFocusHandlesWithOptionalPartyFanout` and `BattleUnit_IssueCommandByFocusHandles`
(the constructor's command-issue path — the substantive edge); the other 7 are
`BattleAction_CheckActionAvailabilityReason`, `BattleAction_CheckGlobalCategoryDisableReason`,
`BattleAction_CheckDefinitionCategoryAvailability`, `BattleAction_GetSubtype3Field22OrFFFF`,
`BattleAction_GetPrimaryRangeScalar`, `0030CBE0` and `0030DB70` sharing `00322C50`.

**PlatformOnlineAchievements — MECHANICAL (SWE2-EC7-40, 1 edge).** `0046B1A0`, called by this page's
`005781A0` section body, is also called by a PlatformOnlineAchievements-filed body; the crossing is
shared-helper fan-in, not that this page owns anything in that layer.

**Resource — SERVICE (SWE2-EC7-157, 15 edges).** Batch-122's `003C1F00` resolves its slot index through `00249180`/`003697F0`/`00249210`, whose edges reach the resource layer (`00249210` callee `0032E400`/`0032E620`); shared-helper fan-in, not a shared responsibility.

**SaveLoad — CLIENT (SWE2-EC7-157, 1 edge).** `00249210` — called by this page's `003C1F00` — is itself called by the save layer's `00582790`; fan-in only.

## SWE2-EC7-30 update (2026-09-18) — `002904D0` `+0x10F78` forward (via `00276D30`/`002778C0`/`00279E20`)

`002904D0` (36 B) — reached through `00276D30`, `002778C0` and
`00279E20` — is the two-argument forward onto the `0209BE80` bank's
`+0x10F78` sub-object: null object returns 0, otherwise
`00297170(sub, arg1, arg2)` runs with the argument registers swapped
into place. Interior anchor `002904EF` (the `jmp 00297170` tail).
## SWE2-EC7-31 update (2026-09-18) — `00254550` bit test (via `00290CF0`) + `002481A0` toggle-and-flag

`00254550` (9 B) — reached through `00290CF0`, `00273950`,
`00276D30`, `00279E20` and `0027AA70` — is the shared bit-test
predicate the update groups call: `bt ecx, edx; setb al` — true
when bit `edx` of the `ecx` mask is set, nothing more. Interior
anchor `00254552` (the `bt` itself).

`002481A0` (18 B) is the flag pair the widget phase code toggles:
`dword[0208ED5C] ^= 1` flips the phase word, then
`dword[0208F560] = 1` sets the dirty marker the next pass reads.
Interior anchor `002481A7` (the `0208F560` store).

## SWE2-EC7-33 update (2026-09-19) - `003F0610`

`003F0610` (3,084 B) is the chain-flash widget builder - `"chain_item"`, `"targetline_p"`, `"chainflash"` strings, 8 `0024ABC0` calls plus `00202C90`/`00202B70`/`00203170`. Interior anchor `003F077A` (a `0024ABC0` call).

## SWE2-EC7-33 update (2026-09-19) - `002BC3E0`

`002BC3E0` (**1,422 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,300 B, a wrong literal in the batch-33 append — the body is 1,422 B per the function list*) is a kind<=0x26 widget dispatcher - per-kind byte `r8+rax+0x19C998` and dword `r8+rax*4+0x19C970` tables, then `00403600`/`002B7210`/`002B6AE0`/`002B6950`/`001EDEC0`. Interior anchor `002BC950` (the cookie-check call site).

## SWE2-EC7-33 update (2026-09-19) - `002B6DB0`

`002B6DB0` (1,033 B) is the same dispatcher shape - `cmp 0x26`, `r8+rax+0x1971E4`/`r8+rax*4+0x1971BC` tables, `[rbx+0xD4] = 0x64` default. Interior anchor `002B71AB` (the cookie-check call site).

## SWE2-EC7-33 update (2026-09-19) - `003F1530`

`003F1530` (**1,027 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 881 B, a wrong literal in the batch-33 append — the body is 1,027 B per the function list*) is the presentation widget body the settings table lists - `00203170`/`00183280`/`00202D70`/`003F3D80`/`003590D0`/`002714E0`/`002714C0`. Interior anchor `003F15FD` (a `00183280` call).

## SWE2-EC7-37 update (2026-09-19) - `002B7210`

`002B7210` (578 B) is a widget constructor op - a single `002B69B0` call inside a long field-init run. Interior anchor `002B725F` (the `002B69B0` call).

## SWE2-EC7-38 update (2026-09-19) - `004079A0`

`004079A0` (464 B) is the `0x1F8` widget procedure the page names - `02B62D80`/`02092730`/`01DFE0B4`, `00407720` triple plus `00407B70`/`00253BC0`/`003946B0`/`00407F90`/`00861EC0`. Interior anchor `004079F6` (a `00407720` call).

## SWE2-EC7-40 update (2026-09-19) - `005781A0`

`005781A0` (360 B) is a widget-constructor body - `01F44830`, `002B39A0` sextuple plus `0046B1A0`/`00244F50`/`00808C40`. Interior anchor `00578228` (a `002B39A0` call).

## SWE2-EC7-54 update (2026-09-19) - `002B69B0`

`002B69B0` (301 B) is a call-free progress ratio - `((word[r8+0x9C]>>1) - [r8+0xC8]) * 0x64 / [r8+0xD4]` then `*r9d/5` via the `0x66666667` magic. Interior anchor `002B69E4` (the `idiv`).

## SWE2-EC7-55 update (2026-09-19) - `00407B70`

`00407B70` (279 B) is a widget procedure body - `002E04E0`/`00394690`/`003C5FB0`/`00407C90` plus `0208EA28`. Interior anchor `00407B8A` (a `00394690` call).

## SWE2-EC7-57 update (2026-09-19) - `003F3D80`

`003F3D80` (185 B) is a presentation widget body - `00202B70`/`00203170`/`00808C40` plus `01F44830`. Interior anchor `003F3DB9` (a `00203170` call).

## SWE2-EC7-62 update (2026-09-19) - `004FF110`

`004FF110` (146 B) is a widget-constructor body - `001EDDA0`/`00314960`/`00537C20`/`00537EA0`/`00538280`/`005386F0` plus `01CEBBA8`. Interior anchor `004FF142` (a `005386F0` call).



## SWE2-EC7-64 update (2026-09-19) - `005386F0`

`005386F0` (141 B) is a widget-constructor body - `003A3E20`/`004309C0`. Interior anchor `00538716` (a `004309C0` call).


## SWE2-EC7-68 update (2026-09-19) - `00394690` counted pointer-array getter

`00394690` (28 B) is the counted element getter the widget
constructors and the storage-completion record call: the bound is
`(dword[rcx+0x50] >> 2) & 0xFFFF`, an in-range `edx` returns
`qword[[rcx+0x60] + edx*8]`, and an out-of-range index returns
NULL. Call-free. Interior anchor `003946A4` (the element load).

## SWE2-EC7-70 update (2026-09-19) - `00394660` kind-4 member getter measured

`00394660` (41 B) is `00394690`'s sibling accessor: the same `edx <
([+0x50] >> 2) & 0xFFFF` bound over the `[+0x60]` pointer table, then the
type filter `byte[entry+8] & 0x3C == 4` before returning `entry[+0x18]` -
the kind-4 member path beside `00394690`'s plain get.
Interior anchor `0039467B` (the `and al, 0x3c` type filter).

## SWE2-EC7-71 update (2026-09-19) - `002B6AE0` paired-field setter measured

Measured on `the-map-screens-and-their-shared-map-data.md` (PARTIAL -
non-bearing); mirrored here beside the sibling `002B69B0` accessor.

`002B6AE0` (99 B) is the two-word setter the map screens share: copies
`word[+0xC8]` and `word[+0xCC]` to the stack, runs
`002B69B0(&a, &b, rcx, edx)` to adjust the pair, writes the signed
results back as dwords at `+0xC8`/`+0xCC`, and stores `edx` at `+0xD4`.
Interior anchor `002B6B17` (the `002B69B0` call).

## SWE2-EC7-71 update (2026-09-19) - `00202C50` snapshot copier measured

`00202C50` (31 B) is the `00216FC0` snapshot copier the widget builders
call: fills the 16-byte stack temp through `00216FC0(&tmp)` then
`movups` it into `[rcx]` - the shared lazy-value fetch for the
`00202xxx` accessor family.
Interior anchor `00202C5E` (the `00216FC0` call).

## SWE2-EC7-85 update (2026-09-20) - `00403600` rect-record build measured

`00403600` (51 B) is the three-word record build the widget callers
run: `[rcx]` zeroes, `word[+4]` takes `[[rdx+0x20]+0x14]`, and
`word[+6]` takes `cvttsd2si([[rdx+0x20]+0x16] * const_double)` -
a scaled-dimension fold, call-free.
Interior anchor `00403622` (the `mulsd`).

## SWE2-EC7-88 update (2026-09-20) - `003C2190` + `003C02B0` measured

`003C2190` (21 B) is the four-arg forward the widget callers
run: `003C1F00([02B457E0], rcx, rdx, r8d)` - the shared table
plus the argument triple re-ordered for the callee.
Interior anchor `003C21A0` (the `003C1F00` tail).

`003C02B0` (129 B) is the index-write fetch over
`[02B457E0+0xE8]`: `ebx` must sit below the `dword` bound in
the `word[+8]`-relative list; `bx` and `byte[r8]` are written
to the `rdx` out words, `dword[r8+4]` resolves through
`002F9920` into `[rdi+8]` when not -1, `003C05F0(ebx)` fills
`[rdi+0x10]`, and the body returns 1.
Interior anchor `003C030B` (the `002F9920` call).

## SWE2-EC7-90 update (2026-09-20) - `003A3E20` two-field reset measured

`003A3E20` (12 B) is the record reset the widget callers run:
`dword[+0x44]` is set to -1 and `word[+0x42]` takes `dx` - a
two-field write, call-free.
Interior anchor `003A3E27` (the word write).

## SWE2-EC7-92 update (2026-09-20) - `003936B0` + `00393630` measured

`003936B0` (134 B) builds the three-element code table the
`00252030` constructor passes to `003BB630`: for `dl` = 0, 1, 2 it
selects `0x3C4` / `0xE240` / `0x8398` (kinds 2-4 share `0x8398`,
anything else 0), then returns `003BB630(table, 3) + 0x2400` under a
stack cookie.
Interior anchor `0039371A` (the `003BB630` call).

`00393630` (126 B) is the name-length clamp: `edx < 0x40` returns
`rcx` untouched; an over-long name loads the six-byte canned string at
`014BB630` into a stack buffer, NUL-terminates at +6, and reports
through `0017D2E0(rbx, msg)` before returning `rbx`.
Interior anchor `00393693` (the `0017D2E0` call).

## SWE2-EC7-99 update (2026-09-20) - `002DD8B0` measured

`002DD8B0` (85 B) is the corner-expand `003F0610` calls:
four integer arguments convert to floats and write the four
`0x30`-stride corner points of a rectangle - `(edx, r9d)`
at `+0x20`, `(edx, arg5)` at `+0x50`, `(r8d, r9d)` at
`+0x80`, `(r8d, arg5)` at `+0xB0` - the rect-to-quad
expansion the widget layout records run.
Interior anchor `002DD8DC` (the `+0x84` store).

## SWE2-EC7-100 update (2026-09-20) - `002B6950` measured

`002B6950` (95 B) is the centred-box rect `002B6DB0` and
`002BC3E0` call: `edx - r9d - 0x18` and `r8d - arg5 -
0x18` seed the `x`/`y`, `0x18`/`0x18` the `w`/`h`, and any
axis whose offset exceeds `0x18` recentres to
`(extent - box) / 2` with the box span - the 24-unit
centred-inset the widget bounds compute.
Interior anchor `002B6978` (the `0x18` stores).

## SWE2-EC7-104 update (2026-09-20) - `00271050` measured

`00271050` (44 B) is the packed-record header
write `00404230` runs on a widget buffer: the
record at `[rcx + 0x30]` gets `+0x00 = 0`,
`+0x04 = 0x13000000`, `+0x08 = 0x10000000`,
and `+0x0C = ((dword[rcx + 0x10] - ptr - 0x10)
>> 4) | 0x50000000` - the same
`0x50000000`-tagged count field `002712E0`
seals, written here with the two fixed type
words.
Interior anchor `0027106D` (the `0x13000000`
write).

`003C1F00` (450 B) is the two-slot lookup `003C2190` calls: `rcx+0x120`'s two `0xA8`-stride entries are counted (`ebx < 2` gates), `02B457E0`'s `[+0xE8]` + `word[rax+8]` forms the index base, then `00249180`/`003697F0`/`00249210` resolve the slot - the constructor's paired-record selector.

Interior anchor `003C200D` (function `003C1F00`).

