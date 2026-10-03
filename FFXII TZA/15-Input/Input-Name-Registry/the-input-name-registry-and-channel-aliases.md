---
system: The input name registry — every bindable name, and which are aliases
category: 15-Input
status: AUDITED
owner_layer: PrimaryOwner:Input
evidence_tier: 1
readiness: DIFFERENTIAL TESTED
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 40 addresses cited - 15 data, 15 entry, 8 interior, 2 literal, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-12
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-input-name-registry-pass-1
  crossref_clean: true
  reopened_count: 0
function_families:
  - "PInputs semantic-name-registry initialisers | C | members/pinputs-semantic-registry-initialisers.tsv | 319 | not this game's code: compiler-generated dynamic-initialiser stubs, one per static node of the five PInputs semantic name registries this page and its contract document. PROVED BY FORM - 319 members, all 32 bytes, ONE instruction form (sub rsp,0x28 / lea rcx,[node] / call <insert> / lea rcx,[dtor] / add rsp,0x28 / jmp 00808B90); only the three operands vary. CONTROL: every callee is one of the five documented registry appends - 00879570 PInputChannelSemantic x143, 00876C80 PInputKeySemantic x97, 008768A0 PInputJoypadButtonSemantic x44, 008760A0 PInputTypeSemantic x25, 00876490 PInputAxisSemantic x10 - and every tail-jump is 00808B90, the atexit wrapper. THE BOUNDARY: the form is the toolchain's; a reconstruction declaring the same statics gets these from its own compiler. SIBLINGS, NOT MEMBERS: the 56 NameRegistryEntry initialisers of the same shape are the existing Generated-Families family (ctor 005FDCB0, registry 02CBF998 - a different registry); the 110 name-only class registrations tail-jump 00639450 instead; 44 assorted statics sit in the generic dynamic-initialiser family on static-initialisers-and-teardowns.md. NOT dispositioned: the five registry appends, the per-node teardowns, and the node semantics this page owns. Selector: 24-Compiler-And-CRT-Runtime/Static-Initialization-And-Teardown/members/select_static_init_form.py"
---

# The input name registry — every bindable name, and which are aliases

## 1. What the player sees

Edit `keymap.ini` by hand and you can write `Button_Square`, `Button_X`, `Button_0` **or**
`Button_LeftMB` — and the game will bind all four to the same thing, because on this build they *are*
the same thing. The PlayStation names, the Xbox names, the bare numbers and (for three of them) the
mouse buttons are **synonyms for one channel**.

**There are 143 names a binding can use, and only 113 distinct channels behind them.** This document
lists every name, gives its numeric value, and says exactly which names collapse together.

## 2. Where the names live, and why they are recoverable without running the game

Two 132-byte functions — `00879570` and `00876C80` — are **registry inserts** for a
string-keyed singly-linked list with duplicate rejection:

```c
int Register(Node *self)                          /* 00879570 / 00876C80 */
{
    const char *key = self->name_08;
    if (!key) return 0x11;                        /* null key   */
    for (Node *n = g_head; n; n = n->next_10)
        if (!strcmp(n->name_08, key)) return 0x12;/* duplicate  */
    self->next_10 = g_head;
    g_head = self;                                /* push front */
    return 0;
}
```

The `strcmp` is **inlined** as `movzx edx,[rax] / movzx ecx,[rax+r8]` with `r8 = key - n->name_08`,
so it does not appear as a call to anything and no string-function xref finds it.

Every caller is a CRT static initialiser of one shape:

```asm
0016C380  sub  rsp, 0x28
0016C384  lea  rcx, [rip + …]      ; -> 01F47508, the node, in .data
0016C38B  call 0x879570            ; register it
0016C390  lea  rcx, [rip + …]      ; -> the destructor
0016C39B  jmp  0x808b90            ; atexit
```

> **So the whole registry is in the image, even though the list itself is not.** The two list heads
> are written once at startup and never appear in the file; what the image contains is the
> **registrations**. `named_registry.py` walks the callers, recovers each node from its `lea`, and
> dereferences `node->name_08`. **240 of 240 names recovered, 0 unrecovered.**

The same 32-byte initialiser shape covers all five PInputs semantic registries — channel, key,
joypad button, type and axis — **319 stubs in total**, declared as the `PInputs
semantic-name-registry initialisers` family in this page's frontmatter (2026-09-16, SWE2-EC7's
disposition of the 530-body static-init form; see
[select_static_init_form.py](../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Teardown/members/select_static_init_form.py)).
The family's callee column is the registry each node registers into.

Both heads were the database's **most-read unexplained globals**: `02EB9D80` ranked **#1** in
[`UNEXPLAINED-GLOBALS.md`](../../_index/UNEXPLAINED-GLOBALS.md) with 148 readers, and `02EB83B8`
ranked **#3** with 102. They are the two list heads.

### The node

| offset | field | evidence |
|---|---|---|
| `+0x00` | type pointer (a vtable) | RTTI at `vtable − 8` |
| `+0x08` | `const char *name` | the key `Register` compares |
| `+0x10` | `next` — zero in the image, linked at startup | `self->next_10 = g_head` |
| `+0x18` | **`int32 value`** — the semantic's numeric code | §3, §4 |

**Records are 32 bytes and the arrays are contiguous at that stride**, verified: the 97 key nodes run
`01F456C8` … `01F462C8` with **one** distinct stride, `0x20`, and the span implies exactly 97.

RTTI names both types:

```
01CD89D8 -> .?AVPInputKeySemantic@PInputs@Phyre@@       97 nodes,  head 02EB83B8, insert 00876C80
01CD9908 -> .?AVPInputChannelSemantic@PInputs@Phyre@@  143 nodes,  head 02EB9D80, insert 00879570
```

**The key registry is a strict subset of the channel registry.** All 97 key names appear in both;
the channel registry adds 46 button/mouse names and nothing else. *(Measured: `B ⊆ A` is true, names
only in B = 0, names only in A = 46.)*

## 3. `PInputKeySemantic` — 97 records

`Empty = 0`, then **`Key_A = 28` through `Key_AccentGrave = 123`, contiguous with no gaps** — 96
values plus the sentinel.

| | |
|---|---|
| lowest | `Empty = 0`, `Key_A = 28`, `Key_B = 29`, `Key_C = 30` |
| highest | `Key_Right_Control = 120`, `Key_Right_Shift = 121`, `Key_Right_Alt = 122`, `Key_AccentGrave = 123` |

Full list with node addresses: [`input-name-registry.tsv`](input-name-registry.tsv).

## 4. `PInputChannelSemantic` — 143 names, 113 channels, 16 alias groups

**Thirty of the 143 names are synonyms.** Every alias group, with its channel value:

| value | names that all mean this channel |
|---:|---|
| 11 | `Button_0` = `Button_LeftMB` = `Button_Square` = `Button_X` |
| 12 | `Button_1` = `Button_A` = `Button_Cross` = `Button_MiddleMB` |
| 13 | `Button_2` = `Button_B` = `Button_Circle` = `Button_RightMB` |
| 14 | `Button_3` = `Button_Triangle` = `Button_Y` |
| 15 | `Button_4` = `Button_L1` = `Button_LB` |
| 16 | `Button_5` = `Button_R1` = `Button_RB` |
| 17 | `Button_6` = `Button_L2` = `Button_LT` |
| 18 | `Button_7` = `Button_R2` = `Button_RT` |
| 19 | `Button_8` = `Button_Back` = `Button_Select` |
| 20 | `Button_9` = `Button_Start` |
| 21 | `Button_10` = `Button_L3` = `Button_LS` |
| 22 | `Button_11` = `Button_R3` = `Button_RS` |
| 23 | `Button_12` = `Button_Up` |
| 24 | `Button_13` = `Button_Right` |
| 25 | `Button_14` = `Button_Down` |
| 26 | `Button_15` = `Button_Left` |

**Channels 11–26 are the sixteen pad buttons**, named four ways: bare index, Xbox letter,
PlayStation glyph, and — for 11, 12 and 13 only — a mouse button.

> ### The mouse buttons are not separate channels
>
> `Button_LeftMB`, `Button_MiddleMB` and `Button_RightMB` resolve to **11, 12 and 13** — the same
> channels as Square/Cross/Circle. On this build a binding cannot distinguish a left click from a
> Square press at the channel layer. **That is what the registry says; whether anything downstream
> separates them is not established** — `DM-1`.
>
> **`DM-1` ANSWERED 2026-09-22 (FABLE): downstream separates them completely — and this box stays
> true.** Mouse buttons are codes **1–3** on their own backend and array; pad buttons are **11–27**
> on another; `001E0E00(i)` is a dedicated mouse accessor. **But no name reaches codes 1–3**, so
> `Button_LeftMB` binds the **pad**. See the section below.

The remaining 97 channel names are the key names of §3, at the same values.

## `DM-1` answered — downstream separates them completely, and no name reaches the separation (FABLE, 2026-09-22)

§4's box is right as written and needs no correction: *at the channel layer* a binding cannot tell a
left click from a Square press. **Downstream is a different layer, and there the two are not merely
distinguishable — they never touch.**

### The two bands read different devices out of different arrays (FABLE, 2026-09-22)

| | mouse | pad |
|---|---|---|
| control codes | **1–3** | **11–27** |
| backend | `0079E6D0` `InputBackend_IsPrimaryControlCode1To3Active` | `0079E650` `InputBackend_IsControlCode11To27ActiveAnyDevice` |
| device it reads | `[rcx + 0x150]`, the mouse | the **18** slots at `[rcx + 0x88]`, any of them |
| byte it tests | `[code − 1 + dev + 0x1E0]` | `[code − 0x0B + slot + 0x30]` |
| its own guard | `lea eax, [rdx-1]` / `cmp eax, 3` | `lea ecx, [rdx-0xb]` / `cmp ecx, 0x11` |

**No device pointer, no array and no code is shared between them.** The transition pass `0079D010`
fills both halves separately in one loop: it queries the mouse at `+0x150` with channels **11–13**
(`0079D147 lea edx, [r13 + 0xb]`, `r13` = 0–2) and publishes the result to `[+0x1E0 + r13]` with the
previous level at `+0x1E3` (`0079D15B`, `0079D16F`, `0079D194`), while the pad half uses `+0x88`
with its previous level at `+0x41`. *So the mouse's channels 11–13 are the **mouse device's own**
numbering, and what leaves the pass is a code in **1–3**.*

### And there is a dedicated mouse accessor, which is the direct answer (FABLE, 2026-09-22)

`0079E6D0` has **7** call sites against `0079E650`'s **5**, and the difference is the whole point:
four of each are inside `InputManager_TranslateBindingProfileToControlState` and one of each is the
`00197990` tail-jump — but **two callers of the mouse band sit outside the input manager entirely**,
and the pad band has none.

```asm
001E0E00  mov ebx, ecx                 ; i
001E0E08  call <the input-manager getter>
001E0E0D  lea edx, [rbx + 1]           ; code = i + 1   -> 1, 2, 3
001E0E10  mov rcx, [rax + 0xDF8]
001E0E17  call 0079E6D0                ; the mouse-only backend
```

**`001E0E00(i)` is “is mouse button `i` down”**, 37 bytes, and it cannot reach a pad button: `i + 1`
lands in 1–3 and `0079E6D0` refuses anything else on its own guard. *It is already cited in use —
[the battle text banks](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md)
records `001E0E00` twice in the input battery that drives bank-playback decisions.* **So a consumer
does separate a click from a face button, and one of them is in the shipped message path.**

### The sting, and it is the part `DM-1` did not ask for (FABLE, 2026-09-22)

**No name reaches codes 1–3.** Over all 143 channel names the only value below 11 is `Empty = 0`;
**the lowest named value above zero is 11**. Meanwhile `Button_LeftMB` is channel **11**, and `DM-3`
establishes that a channel value *is* the `keymap.ini` control code — so a binding written
`Button_LeftMB` dispatches to the **11–27 pad band** and reads **pad button 0**, exactly as
`Button_Square` does.

> **So both halves of the apparent paradox are true at once.** *At the naming layer* the four names
> on channel 11 are genuinely indistinguishable — and they all bind the **pad**. *At the backend
> layer* the mouse is a separate device on a separate code range with its own accessor. **The
> mouse's real buttons are reachable only through `001E0E00`, never through a binding**, because the
> band they live in carries no registry name at all. `Button_LeftMB` is a name for a pad button.

> **Scope.** Static reading of `0079D010`, `0079E6D0`, `0079E650` and `001E0E00`, plus a call-site
> sweep over the two backends; the registry values are re-read from the image against §1/§4's
> published 143 nodes / 113 distinct / range 0–123. Nothing is observed live, and *whether a click
> and a face button feel different in play* is not a question this settles — only that the code
> keeps them apart and that one shipped consumer reads the mouse directly. **NATIVE/STATIC.**



## 5. This corrects the keymap document, in two places

[`keymap-ini-file-format-and-default-controls.md`](../Binding-Profiles/keymap-ini-file-format-and-default-controls.md)
§3 records:

> `01F45700` · `PInputKeySemantic` member records · **95 × 32 B** · descending `123 … 29` ·
> `{value, typeRef, namePtr, 0}`

**The stride and the value range are right; the count and the field order are not.**

**The count.** The table is **97 records**, `01F456C8` … `01F462C8`, values `123 … 28` plus
`Empty = 0`. The documented span `01F45700`–`01F462C0` is anchored on the **`value` field at
node + 0x18**, not on the node base, and it stops one record short at each end. The arithmetic
reconciles exactly:

```
documented : 01F45700 .. 01F462C0   ->  95 records, values 123 .. 29
actual     : 01F456C8 .. 01F462C8   ->  97 records, values 123 .. 28  and  Empty = 0
missing    : Empty (0) at the low end, Key_A (28) at the high end
```

> **`Key_A` was outside the documented run.** The name string was in the document's own string-run
> entry (`01CD84D8`, *"`Key_A` … `Key_Right_Alt`"*), but the member record was not counted. Counting
> a table by subtracting two endpoint addresses fails silently by one at each end; **enumerating the
> members counts them.**

**The field order.** The node is `{typeRef, namePtr, next, value}`, not `{value, typeRef, namePtr, 0}`:

```
01F462C8  01CD89D8  01CD870C  00000000  0000001C     ; Key_A, value 28
01F45E68  01CD89D8  01CD85F4  00000000  0000003F     ; Key_0, value 63
01F456C8  01CD89D8  01CD81A4  00000000  00000000     ; Empty, value 0
```

**Nothing else in that document depends on the order**, and its `keymapCode = PInputKeySemantic − 1`
mapping — verified there 28 of 28 against the shipped defaults — is untouched by either correction.

## 6. And it answers one of its open questions

That document's §7 asks:

> *"What the 1–3 and 11–27 bands are. … the reflection tables for `PInputMouseButtonSemantic` and
> `PInputJoypadButtonSemantic` **give conflicting values** under one record framing."*

**The 11–26 band is the sixteen pad buttons, and the values do not conflict — they are aliases.**
Mouse and joypad names live in **one** channel space and deliberately share values; a framing that
expects two disjoint tables will always read that as a conflict. §4 is the table.

~~**The 1–3 band is still open**~~ **Codes 1–3 answered 2026-09-12 (FABLE): the three mouse buttons.** `InputBackend_IsPrimaryControlCode1To3Active` (`0079E6D0`) returns byte `+0x1E0 + (code − 1)` of the device at backend `+0x150`, and `0079D010` fills those three bytes by asking that device for **channels 11, 12 and 13** (`lea edx, [r13 + 0xB]`, loop bound 3, `0079D140`–`0079D1A3`) — the channels whose registered aliases include the mouse buttons — storing a byte only when the state changed. So control codes 1–3 are `Mouse1`–`Mouse3` (the never-iterated name table at `01DF1360`) read from input device **type 0** — backend `+0x150` is filled by `0079A430` with `00796FC0(0, 0)`, the first registered device whose type method returns 0, while types 3 and 4 are looked up per player (`0079DE7A`, `0079E10C`); that type 0 is the mouse rests on the channel aliases and the name table, not on a read type enum *(wording narrowed the same day)* — separately from the pad band 11–26 that shares those channel numbers. **27 is still open** — no registered channel name carries a value in `1 … 10`
or `27`, so whatever those codes are, they are not named channels. `DM-2`.

## 6b. Correction — they are not byte-identical, and the difference is the point

**This page said *“two byte-identical 132-byte functions”*. They are not.** Comparing all
132 bytes: **four differ, in two adjacent pairs** — the low halves of two RIP-relative
displacements. Resolved with capstone, never by hand:

```text
00879570  +29   mov rbx, [rip + 0x26407EC]   -> 02EB9D80
          +106  mov [rip + 0x264079F], r11   -> 02EB9D80
00876C80  +29   mov rbx, [rip + 0x2641714]   -> 02EB83B8
          +106  mov [rip + 0x26416C7], r11   -> 02EB83B8
```

**Each names its own list head, once to read and once to write.** That is the entire
difference between the two registries' inserts, and it is also why `globals_index.py`
reports **exactly one writer** for each head — `02EB9D80` 1 writer / 148 readers,
`02EB83B8` 1 writer / 102 readers.

> The claim was directionally right and factually wrong, and the corrected version is
> **stronger**: *identical apart from the two displacements that select the registry* says
> what *byte-identical* could not, because byte-identical functions could not address two
> different lists.

### The subsystem is five paired functions, not one

| channel | key | size | differing bytes |
|---|---|---:|---|
| `008794F0` | `00876C00` | 122 | 8 |
| **`00879570`** | **`00876C80`** | **132** | **4** |
| `00879600` | `00876D10` | 103 | 2 |
| `00879670` | `00876D80` | 222 | 8 |
| `00879760` | `00876E60` | 87 | 2 |

**Every difference is a pair of adjacent bytes.** *(Enumeration method: the readers of each
head from `globals_index.py`, intersected with the functions inside the two address runs.)*

**All five are now read** — 2026-09-08:

| channel | key | size | what it is |
|---|---|---:|---|
| `008794F0` | `00876C00` | 122 | **scalar deleting destructor** — installs the vtable, **unlinks the node from the list**, then `operator delete(this, 0x20)` when the low bit of the second argument is set |
| **`00879570`** | **`00876C80`** | **132** | **the insert** — this contract |
| `00879600` | `00876D10` | 103 | **find by name, out-parameter form** — writes the node or `NULL` and returns **`0x13` when not found**, `0` when found |
| `00879670` | `00876D80` | 222 | **enumerate into a flat array** — counts the list, and only when the count differs from the caller's does it allocate `count * 8`, free the old array and refill; then walks the list writing each node pointer in order |
| `00879760` | `00876E60` | 87 | **find by name, pointer-returning form** — `NULL` for a `NULL` name and `NULL` when absent; no status code |

**`0x13` is a fourth return code, NOT_FOUND** — the family is `0x00` OK, `0x11` NULL_KEY,
`0x12` DUPLICATE, `0x13` NOT_FOUND, and **the insert can never return the fourth**. **The
enumerator's count field carries an ownership bit**: it frees the previous array only when
**bit 31 of the count is clear**, so a caller can hand in a borrowed array by setting it.

Each key-side twin was checked to reference **its own** head `02EB83B8` and its own vtable
`01CD89D8`, so the pairing is verified rather than inherited. **One of the five is
reconstructed**; the other four are understood and not reimplemented. [the contract](CONTRACT-input-name-registry.md) §6.


## `DM-3` answered — the node value IS the keymap control code, and that holds for buttons too (FABLE, 2026-09-22)

§7 declined to assume that the keymap document's `keymapCode = PInputKeySemantic − 1` carries over
from the 28 keys to the 46 `Button_*` channels. **It does carry over, and the reason it does is that
there is no offset to carry: the value this registry stores at node `+0x18` is the keymap control
code itself.**

### The keys, against the keymap document's own worked examples (FABLE, 2026-09-22)

Those examples were derived the other way round — from the shipped `keymap.ini` defaults and the
band table — so they are an independent check on this registry, not a restatement of it.

| keymap code | key the keymap document names | node `+0x18` here |
|--:|---|--:|
| 28 / 31 / 50 / 46 | `A` `D` `W` `S` *(the WASD check)* | **28 / 31 / 50 / 46** |
| 91 / 92 / 93 / 94 | `Left` `Right` `Up` `Down` | **91 / 92 / 93 / 94** |
| 65 / 66 / 67 | `F1` `F2` `F3` *(`Speed1/2/3`)* | **65 / 66 / 67** |
| 80 | `Space` *(`Circle`)* | **80** |
| 118 | `Left Shift` *(`WalkMode`)* | **118** — `Key_Left_Shift` |

**Thirteen of thirteen identical, none off by one.** So `keymapCode = PInputKeySemantic − 1` is a
statement about the **enum ordinal**, and the number this registry stores has the − 1 already
applied. *Read against `keymap.ini`, the registry value needs no adjustment at all.*

### The buttons, and the one value that settles it (FABLE, 2026-09-22)

The keymap document routes control codes by band — **1–3**, **11–27** and **28–152** — and says in
terms that **codes 4–10 are polled by nothing**. §4's sixteen pad channels are **11–26**.

| reading | button values landing inside the non-keyboard band 11–27 |
|---|--:|
| **value used as the code** *(no offset)* | **46 of 46** |
| value − 1 used as the code | 42 of 46 |

**The four that fail are the whole argument.** `Button_0` = `Button_LeftMB` = `Button_Square` =
`Button_X` is channel **11**; under a − 1 it would be code **10**, which falls in the dead range the
keymap document says nothing polls. **A binding on the pad's first face button would never fire.**
So the offset cannot apply to buttons, and it does not apply to keys either — the same rule governs
both, and the rule is identity.

> **A second reading agrees, and it costs nothing to state.** All **97** names present in *both*
> registries carry the **same** number in each: the difference `PInputKeySemantic −
> PInputChannelSemantic` is **0 for 97 of 97**. So a key's channel value and its key value are one
> number, which is why a single `keymap.ini` code space can address keys and pad buttons together.

> **Scope.** This compares the registry's stored values against the control codes the keymap
> document recovered; both are **NATIVE/STATIC** readings of the shipped image. It does not observe
> a binding being applied at run time. *`Key_Left_Control` and `Key_Right_Control` (codes 117 and
> 120 in that document's band table) are named in §3's own range line but were not part of this
> check.* **The control on the reader is §1/§4's published figures, reproduced from the image: 143
> channel nodes, 113 distinct values, range 0–123.**

## 7. What this does not claim


- ~~**That a channel value is what `keymap.ini` stores.** The keymap document establishes
  `keymapCode = PInputKeySemantic − 1` for keys and verified it 28 of 28; **no equivalent check was
  run here for the `Button_*` channels**, and this document does not assume the same offset applies.~~
  **`DM-3` ANSWERED 2026-09-22 (FABLE): a channel value IS what `keymap.ini` stores.** The node
  `+0x18` value equals the keymap control code on **13 of 13** of that document's worked examples,
  and all **46 of 46** button values land inside its non-keyboard band 11–27 while a − 1 would drop
  four of them into the range it says nothing polls. See the section above. `DM-3`.
- ~~**That the alias groups are indistinguishable downstream.**~~ *(Superseded: **`DM-1` ANSWERED 2026-09-22 (FABLE)** - downstream separates them completely, and no name reaches the mouse codes; see the `DM-1` section above. Struck 2026-10-01, OPUS.)* They are one channel at the registry;
  whether a consumer separates mouse from pad is unread. `DM-1`.
- **That 143 and 97 are the complete registries.** They are the complete sets of *static
  registrations found in the image*. A name registered at runtime from data would not appear, and
  nothing here rules that out.
- **Anything about axes.** Every name recovered is a button or a key. If analogue sticks have
  semantics, they are not in these two registries.

## 8. Reimplemented and differential-tested — 2026-09-08

**Reconstruction:** [`../../../Reconstruction/Game/Input/name_registry.c`](../../../../Reconstruction/Game/Input/name_registry.c)
**Test:** [`../../../Reconstruction/Tests/Differential/diff_name_registry.py`](../../../../Reconstruction/Tests/Differential/diff_name_registry.py)

`NameRegistry_Register` is reimplemented from §2 of this page and compared against the shipped 132
bytes at `00879570`, run in Unicorn at its real address. Both sides are handed **the same image
regions at the same virtual addresses** — the real 143-node array out of `.data` and the real name
strings out of `.rdata` — because the nodes reference each other and their names by absolute address.

```
cases                  : 154   (143 real nodes, 11 injected)
return codes           : OK x144, NULL_KEY x1, DUPLICATE x9
return-code mismatches : 0
resulting list         : reference 144 nodes, reconstruction 144 nodes, SAME ORDER
```

### Real data alone would have been a weak test

**Every registered name in the shipped image is distinct**, so a suite built only from real nodes
never once takes the duplicate path — it would report parity on error handling it never executed.
The suite therefore injects:

| injected | result | what it shows |
|---|---|---|
| re-register 8 nodes already inserted | `DUPLICATE` ×8 | the scan finds a node already in the list |
| a node whose name pointer is zero | `NULL_KEY` | the `0x11` path |
| a node whose name is a **copy** of `Button_R2` at a different address | `DUPLICATE` | **the comparison is a string comparison, not pointer identity** — the only case that can show this |
| a node with a name nothing else uses | `OK` | the insert still works after the failures |

> The reconstruction uses `strcmp` where the original inlines
> `movzx edx,[rax] / movzx ecx,[rax+r8]` with `r8 = key − name`. **That equivalence is proven by the
> copied-name case rather than assumed.**

### Readiness

This document moves to **`DIFFERENTIAL TESTED`** — for *this operation*. It is a one-operation
subsystem, so unlike the settings contract there is no larger surface being over-promised. What is
still missing is `INTEGRATION`: **the real registration order is the CRT initialiser order**, which
this test does not know and does not claim. Both sides are simply given the same shuffled order.

## 10. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment.)*

The registry was re-derived from `input-name-registry.tsv` and the node bytes in `.data`, and
**every count holds.**

| claim | measured |
|---|---|
| two registries, **143** and **97** nodes | **143** for `00879570`, **97** for `00876C80` |
| names unique within each | **143 / 143** and **97 / 97** distinct |
| "**143 names, only 113 distinct channels**" | node `+0x18` takes **113 distinct values** over the 143, range **0–123** |
| "**thirty of the 143 names are synonyms**" | `143 − 113` = **30** |
| "**16 alias groups**" | **16** channels carry more than one name |
| the groups account for the thirty | sizes `4, 4, 4, 3×8, 2×5`; `Σ(size − 1)` = **30**, exactly |

### §1's player-facing promise is checkable, and it checks

§1 tells a modder that `Button_Square`, `Button_X`, `Button_0` and `Button_LeftMB` all bind to one
thing. Grouping the 143 nodes by `+0x18`:

```
channel 11 : Button_0, Button_LeftMB, Button_Square, Button_X
channel 12 : Button_1, Button_A, Button_Cross, Button_MiddleMB
channel 13 : Button_2, Button_B, Button_Circle, Button_RightMB
```

**Channel 11 is exactly those four names and no others.** The sentence a player would read is the
same fact as the byte at `+0x18`, and the three four-name groups are precisely the three channels
that carry a mouse button as well as a pad button — which is why §1 could name four synonyms and not
three.

### Nothing to add

The channel field's offset — the one thing this pass was ready to contribute — is already given at
`+0x18` in §3's node table **and** in
[the contract](CONTRACT-input-name-registry.md)'s struct. Found by searching before claiming, per the
amendment.

**Not claimed:** §5's differential test, the `1–3` mouse-button answer and the injected-node harness
(154 cases = 143 real + 11 injected) were **not** re-run — this pass read the shipped nodes, not the
harness. Nothing was executed or observed live.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-input-name-registry-and-channel-alia-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001E0E00` | 37 B | calls the framework-singleton getter and returns `0079E6D0(qword +0xDF8 of that result, ecx + 1)`, zero-extending the returned byte `al` into `eax` | `001E0E08`, `001E0E0D`, `001E0E10`, `001E0E17`, `001E0E1C` |

## Per-member rows: which node each of the semantic-name initialisers registers (OPUS, 2026-10-03)

The family `PInputs semantic-name-registry initialisers` (frontmatter, 319 members) shares one 32-byte shape, stated here once and not repeated per row: `lea rcx, [node]` at + 0x4, a call to its registry's insert (section 2), `lea rcx, [teardown]`, and a tail jump to the CRT atexit registrar `00808B90`. What differs from member to member is the node that + 0x4 `lea` loads (and with it the name the node carries at qword `+0x8`, the key the insert compares), the insert called at + 0xB (one of five, the grouping below), and the teardown that + 0x10 `lea` hands to `00808B90` (each member has its own node-unlink teardown, listed in the members TSV's `dtor` column). The rows anchor the node `lea`; they do not state the teardown. Each row below anchors that `lea` (the member's distinguishing instruction) and states its node and the registered name. [`fam_rows.py`](../../_index/candidates/opus-ee-input-name-initialisers-1003/fam_rows.py) derives every row from the certified image and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-input-name-initialisers-1003/rows.tsv): a member whose body leaves the shape, a node that differs or a name that differs fails it (two controls, a swapped node and a moved anchor, are refused). These rows explain which name each initialiser registers. They follow SWE2-AUDIT-SPEC's ruling on per-member rows (`202e59a0a`): the shared shape earns nothing, and only the distinguishing anchor with its value counts.

### Registered through `008760A0`, the type-semantic list (`PInputTypeSemantic`) (25 nodes, OPUS)

| member | distinguishing instruction | node (the `lea` target) | name at the node's `+0x8` |
|---|---|---|---|
| 0016ABA0 | `0016ABA4` `lea` | `01F44DC0` | "JoypadAxis" |
| 0016ABC0 | `0016ABC4` `lea` | `01F44DA8` | "JoypadButton" |
| 0016ABE0 | `0016ABE4` `lea` | `01F44D90` | "Key" |
| 0016AC00 | `0016AC04` `lea` | `01F44F10` | "MotionAngularVelocityX" |
| 0016AC20 | `0016AC24` `lea` | `01F44F28` | "MotionAngularVelocityY" |
| 0016AC40 | `0016AC44` `lea` | `01F44F40` | "MotionAngularVelocityZ" |
| 0016AC60 | `0016AC64` `lea` | `01F44F58` | "MotionLinearAccelerationX" |
| 0016AC80 | `0016AC84` `lea` | `01F44F70` | "MotionLinearAccelerationY" |
| 0016ACA0 | `0016ACA4` `lea` | `01F44F88` | "MotionLinearAccelerationZ" |
| 0016ACC0 | `0016ACC4` `lea` | `01F44EF8` | "MotionQuatW" |
| 0016ACE0 | `0016ACE4` `lea` | `01F44EB0` | "MotionQuatX" |
| 0016AD00 | `0016AD04` `lea` | `01F44EC8` | "MotionQuatY" |
| 0016AD20 | `0016AD24` `lea` | `01F44EE0` | "MotionQuatZ" |
| 0016AD40 | `0016AD44` `lea` | `01F44DD8` | "MouseButton" |
| 0016AD60 | `0016AD64` `lea` | `01F44DF0` | "MouseDeltaX" |
| 0016AD80 | `0016AD84` `lea` | `01F44E08` | "MouseDeltaY" |
| 0016ADA0 | `0016ADA4` `lea` | `01F44E20` | "TouchDragX" |
| 0016ADC0 | `0016ADC4` `lea` | `01F44E38` | "TouchDragY" |
| 0016ADE0 | `0016ADE4` `lea` | `01F44E80` | "TouchPinch" |
| 0016AE00 | `0016AE04` `lea` | `01F44E98` | "TouchRotate" |
| 0016AE20 | `0016AE24` `lea` | `01F44E50` | "TouchTwoFingerDragX" |
| 0016AE40 | `0016AE44` `lea` | `01F44E68` | "TouchTwoFingerDragY" |
| 0016AE60 | `0016AE64` `lea` | `01F44FA0` | "VisionTrackerX" |
| 0016AE80 | `0016AE84` `lea` | `01F44FB8` | "VisionTrackerY" |
| 0016AEA0 | `0016AEA4` `lea` | `01F44FD0` | "VisionTrackerZ" |

### Registered through `00876490`, the axis-semantic list (`PInputAxisSemantic`) (10 nodes, OPUS)

| member | distinguishing instruction | node (the `lea` target) | name at the node's `+0x8` |
|---|---|---|---|
| 0016AF20 | `0016AF24` `lea` | `01F45008` | "Gyro" |
| 0016AF40 | `0016AF44` `lea` | `01F45128` | "XAxis_0" |
| 0016AF60 | `0016AF64` `lea` | `01F450C8` | "XAxis_1" |
| 0016AF80 | `0016AF84` `lea` | `01F45068` | "XAxis_2" |
| 0016AFA0 | `0016AFA4` `lea` | `01F45108` | "YAxis_0" |
| 0016AFC0 | `0016AFC4` `lea` | `01F450A8` | "YAxis_1" |
| 0016AFE0 | `0016AFE4` `lea` | `01F45048` | "YAxis_2" |
| 0016B000 | `0016B004` `lea` | `01F450E8` | "ZAxis_0" |
| 0016B020 | `0016B024` `lea` | `01F45088` | "ZAxis_1" |
| 0016B040 | `0016B044` `lea` | `01F45028` | "ZAxis_2" |

### Registered through `008768A0`, the joypad-button-semantic list (`PInputJoypadButtonSemantic`) (44 nodes, OPUS)

| member | distinguishing instruction | node (the `lea` target) | name at the node's `+0x8` |
|---|---|---|---|
| 0016B060 | `0016B064` `lea` | `01F456A8` | "Button_0" |
| 0016B080 | `0016B084` `lea` | `01F45308` | "Button_10" |
| 0016B0A0 | `0016B0A4` `lea` | `01F452A8` | "Button_11" |
| 0016B0C0 | `0016B0C4` `lea` | `01F45248` | "Button_12" |
| 0016B0E0 | `0016B0E4` `lea` | `01F45208` | "Button_13" |
| 0016B100 | `0016B104` `lea` | `01F451C8` | "Button_14" |
| 0016B120 | `0016B124` `lea` | `01F45188` | "Button_15" |
| 0016B140 | `0016B144` `lea` | `01F45648` | "Button_1" |
| 0016B160 | `0016B164` `lea` | `01F455E8` | "Button_2" |
| 0016B180 | `0016B184` `lea` | `01F45588` | "Button_3" |
| 0016B1A0 | `0016B1A4` `lea` | `01F45528` | "Button_4" |
| 0016B1C0 | `0016B1C4` `lea` | `01F454C8` | "Button_5" |
| 0016B1E0 | `0016B1E4` `lea` | `01F45468` | "Button_6" |
| 0016B200 | `0016B204` `lea` | `01F45408` | "Button_7" |
| 0016B220 | `0016B224` `lea` | `01F453A8` | "Button_8" |
| 0016B240 | `0016B244` `lea` | `01F45348` | "Button_9" |
| 0016B260 | `0016B264` `lea` | `01F45608` | "Button_A" |
| 0016B280 | `0016B284` `lea` | `01F455A8` | "Button_B" |
| 0016B2A0 | `0016B2A4` `lea` | `01F45368` | "Button_Back" |
| 0016B2C0 | `0016B2C4` `lea` | `01F455C8` | "Button_Circle" |
| 0016B2E0 | `0016B2E4` `lea` | `01F45628` | "Button_Cross" |
| 0016B300 | `0016B304` `lea` | `01F451A8` | "Button_Down" |
| 0016B320 | `0016B324` `lea` | `01F45508` | "Button_L1" |
| 0016B340 | `0016B344` `lea` | `01F45448` | "Button_L2" |
| 0016B360 | `0016B364` `lea` | `01F452E8` | "Button_L3" |
| 0016B380 | `0016B384` `lea` | `01F454E8` | "Button_LB" |
| 0016B3A0 | `0016B3A4` `lea` | `01F452C8` | "Button_LS" |
| 0016B3C0 | `0016B3C4` `lea` | `01F45428` | "Button_LT" |
| 0016B3E0 | `0016B3E4` `lea` | `01F45168` | "Button_Left" |
| 0016B400 | `0016B404` `lea` | `01F454A8` | "Button_R1" |
| 0016B420 | `0016B424` `lea` | `01F453E8` | "Button_R2" |
| 0016B440 | `0016B444` `lea` | `01F45288` | "Button_R3" |
| 0016B460 | `0016B464` `lea` | `01F45488` | "Button_RB" |
| 0016B480 | `0016B484` `lea` | `01F45268` | "Button_RS" |
| 0016B4A0 | `0016B4A4` `lea` | `01F453C8` | "Button_RT" |
| 0016B4C0 | `0016B4C4` `lea` | `01F451E8` | "Button_Right" |
| 0016B4E0 | `0016B4E4` `lea` | `01F45388` | "Button_Select" |
| 0016B500 | `0016B504` `lea` | `01F45688` | "Button_Square" |
| 0016B520 | `0016B524` `lea` | `01F45328` | "Button_Start" |
| 0016B540 | `0016B544` `lea` | `01F45568` | "Button_Triangle" |
| 0016B560 | `0016B564` `lea` | `01F45228` | "Button_Up" |
| 0016B580 | `0016B584` `lea` | `01F45668` | "Button_X" |
| 0016B5A0 | `0016B5A4` `lea` | `01F45548` | "Button_Y" |
| 0016B5C0 | `0016B5C4` `lea` | `01F45148` | "Empty" |

### Registered through `00876C80`, the key-semantic list (`PInputKeySemantic`) (97 nodes, OPUS)

| member | distinguishing instruction | node (the `lea` target) | name at the node's `+0x8` |
|---|---|---|---|
| 0016B5E0 | `0016B5E4` `lea` | `01F456C8` | "Empty" |
| 0016B600 | `0016B604` `lea` | `01F45E68` | "Key_0" |
| 0016B620 | `0016B624` `lea` | `01F45F88` | "Key_1" |
| 0016B640 | `0016B644` `lea` | `01F45F68` | "Key_2" |
| 0016B660 | `0016B664` `lea` | `01F45F48` | "Key_3" |
| 0016B680 | `0016B684` `lea` | `01F45F28` | "Key_4" |
| 0016B6A0 | `0016B6A4` `lea` | `01F45F08` | "Key_5" |
| 0016B6C0 | `0016B6C4` `lea` | `01F45EE8` | "Key_6" |
| 0016B6E0 | `0016B6E4` `lea` | `01F45EC8` | "Key_7" |
| 0016B700 | `0016B704` `lea` | `01F45EA8` | "Key_8" |
| 0016B720 | `0016B724` `lea` | `01F45E88` | "Key_9" |
| 0016B740 | `0016B744` `lea` | `01F462C8` | "Key_A" |
| 0016B760 | `0016B764` `lea` | `01F456E8` | "Key_AccentGrave" |
| 0016B780 | `0016B784` `lea` | `01F45B68` | "Key_Apostrophe" |
| 0016B7A0 | `0016B7A4` `lea` | `01F462A8` | "Key_B" |
| 0016B7C0 | `0016B7C4` `lea` | `01F45BA8` | "Key_Backslash" |
| 0016B7E0 | `0016B7E4` `lea` | `01F45C88` | "Key_Backspace" |
| 0016B800 | `0016B804` `lea` | `01F46288` | "Key_C" |
| 0016B820 | `0016B824` `lea` | `01F45B48` | "Key_Comma" |
| 0016B840 | `0016B844` `lea` | `01F46268` | "Key_D" |
| 0016B860 | `0016B864` `lea` | `01F459C8` | "Key_Delete" |
| 0016B880 | `0016B884` `lea` | `01F45A88` | "Key_Down" |
| 0016B8A0 | `0016B8A4` `lea` | `01F46248` | "Key_E" |
| 0016B8C0 | `0016B8C4` `lea` | `01F45A48` | "Key_End" |
| 0016B8E0 | `0016B8E4` `lea` | `01F45CA8` | "Key_Enter" |
| 0016B900 | `0016B904` `lea` | `01F45C08` | "Key_Equals" |
| 0016B920 | `0016B924` `lea` | `01F45E48` | "Key_Escape" |
| 0016B940 | `0016B944` `lea` | `01F45D08` | "Key_F10" |
| 0016B960 | `0016B964` `lea` | `01F45CE8` | "Key_F11" |
| 0016B980 | `0016B984` `lea` | `01F45CC8` | "Key_F12" |
| 0016B9A0 | `0016B9A4` `lea` | `01F45E28` | "Key_F1" |
| 0016B9C0 | `0016B9C4` `lea` | `01F45E08` | "Key_F2" |
| 0016B9E0 | `0016B9E4` `lea` | `01F45DE8` | "Key_F3" |
| 0016BA00 | `0016BA04` `lea` | `01F45DC8` | "Key_F4" |
| 0016BA20 | `0016BA24` `lea` | `01F45DA8` | "Key_F5" |
| 0016BA40 | `0016BA44` `lea` | `01F45D88` | "Key_F6" |
| 0016BA60 | `0016BA64` `lea` | `01F45D68` | "Key_F7" |
| 0016BA80 | `0016BA84` `lea` | `01F45D48` | "Key_F8" |
| 0016BAA0 | `0016BAA4` `lea` | `01F45D28` | "Key_F9" |
| 0016BAC0 | `0016BAC4` `lea` | `01F46228` | "Key_F" |
| 0016BAE0 | `0016BAE4` `lea` | `01F46208` | "Key_G" |
| 0016BB00 | `0016BB04` `lea` | `01F461E8` | "Key_H" |
| 0016BB20 | `0016BB24` `lea` | `01F45A68` | "Key_Home" |
| 0016BB40 | `0016BB44` `lea` | `01F461C8` | "Key_I" |
| 0016BB60 | `0016BB64` `lea` | `01F459E8` | "Key_Insert" |
| 0016BB80 | `0016BB84` `lea` | `01F461A8` | "Key_J" |
| 0016BBA0 | `0016BBA4` `lea` | `01F46188` | "Key_K" |
| 0016BBC0 | `0016BBC4` `lea` | `01F46168` | "Key_L" |
| 0016BBE0 | `0016BBE4` `lea` | `01F45BE8` | "Key_LeftBracket" |
| 0016BC00 | `0016BC04` `lea` | `01F45768` | "Key_Left_Alt" |
| 0016BC20 | `0016BC24` `lea` | `01F457A8` | "Key_Left_Control" |
| 0016BC40 | `0016BC44` `lea` | `01F45788` | "Key_Left_Shift" |
| 0016BC60 | `0016BC64` `lea` | `01F45AE8` | "Key_Left" |
| 0016BC80 | `0016BC84` `lea` | `01F46148` | "Key_M" |
| 0016BCA0 | `0016BCA4` `lea` | `01F45C28` | "Key_Minus" |
| 0016BCC0 | `0016BCC4` `lea` | `01F46128` | "Key_N" |
| 0016BCE0 | `0016BCE4` `lea` | `01F45888` | "Key_Numpad_0" |
| 0016BD00 | `0016BD04` `lea` | `01F459A8` | "Key_Numpad_1" |
| 0016BD20 | `0016BD24` `lea` | `01F45988` | "Key_Numpad_2" |
| 0016BD40 | `0016BD44` `lea` | `01F45968` | "Key_Numpad_3" |
| 0016BD60 | `0016BD64` `lea` | `01F45948` | "Key_Numpad_4" |
| 0016BD80 | `0016BD84` `lea` | `01F45928` | "Key_Numpad_5" |
| 0016BDA0 | `0016BDA4` `lea` | `01F45908` | "Key_Numpad_6" |
| 0016BDC0 | `0016BDC4` `lea` | `01F458E8` | "Key_Numpad_7" |
| 0016BDE0 | `0016BDE4` `lea` | `01F458C8` | "Key_Numpad_8" |
| 0016BE00 | `0016BE04` `lea` | `01F458A8` | "Key_Numpad_9" |
| 0016BE20 | `0016BE24` `lea` | `01F45848` | "Key_Numpad_Asterisk" |
| 0016BE40 | `0016BE44` `lea` | `01F457E8` | "Key_Numpad_Enter" |
| 0016BE60 | `0016BE64` `lea` | `01F45828` | "Key_Numpad_Minus" |
| 0016BE80 | `0016BE84` `lea` | `01F457C8` | "Key_Numpad_Period" |
| 0016BEA0 | `0016BEA4` `lea` | `01F45808` | "Key_Numpad_Plus" |
| 0016BEC0 | `0016BEC4` `lea` | `01F45868` | "Key_Numpad_Slash" |
| 0016BEE0 | `0016BEE4` `lea` | `01F46108` | "Key_O" |
| 0016BF00 | `0016BF04` `lea` | `01F460E8` | "Key_P" |
| 0016BF20 | `0016BF24` `lea` | `01F45A08` | "Key_PageDown" |
| 0016BF40 | `0016BF44` `lea` | `01F45A28` | "Key_PageUp" |
| 0016BF60 | `0016BF64` `lea` | `01F45B28` | "Key_Period" |
| 0016BF80 | `0016BF84` `lea` | `01F460C8` | "Key_Q" |
| 0016BFA0 | `0016BFA4` `lea` | `01F460A8` | "Key_R" |
| 0016BFC0 | `0016BFC4` `lea` | `01F45BC8` | "Key_RightBracket" |
| 0016BFE0 | `0016BFE4` `lea` | `01F45708` | "Key_Right_Alt" |
| 0016C000 | `0016C004` `lea` | `01F45748` | "Key_Right_Control" |
| 0016C020 | `0016C024` `lea` | `01F45728` | "Key_Right_Shift" |
| 0016C040 | `0016C044` `lea` | `01F45AC8` | "Key_Right" |
| 0016C060 | `0016C064` `lea` | `01F46088` | "Key_S" |
| 0016C080 | `0016C084` `lea` | `01F45B88` | "Key_Semicolon" |
| 0016C0A0 | `0016C0A4` `lea` | `01F45B08` | "Key_Slash" |
| 0016C0C0 | `0016C0C4` `lea` | `01F45C48` | "Key_Space" |
| 0016C0E0 | `0016C0E4` `lea` | `01F46068` | "Key_T" |
| 0016C100 | `0016C104` `lea` | `01F45C68` | "Key_Tab" |
| 0016C120 | `0016C124` `lea` | `01F46048` | "Key_U" |
| 0016C140 | `0016C144` `lea` | `01F45AA8` | "Key_Up" |
| 0016C160 | `0016C164` `lea` | `01F46028` | "Key_V" |
| 0016C180 | `0016C184` `lea` | `01F46008` | "Key_W" |
| 0016C1A0 | `0016C1A4` `lea` | `01F45FE8` | "Key_X" |
| 0016C1C0 | `0016C1C4` `lea` | `01F45FC8` | "Key_Y" |
| 0016C1E0 | `0016C1E4` `lea` | `01F45FA8` | "Key_Z" |

### Registered through `00879570`, the channel-semantic list (`PInputChannelSemantic`) (143 nodes, OPUS)

| member | distinguishing instruction | node (the `lea` target) | name at the node's `+0x8` |
|---|---|---|---|
| 0016C380 | `0016C384` `lea` | `01F47508` | "Button_0" |
| 0016C3A0 | `0016C3A4` `lea` | `01F47108` | "Button_10" |
| 0016C3C0 | `0016C3C4` `lea` | `01F470A8` | "Button_11" |
| 0016C3E0 | `0016C3E4` `lea` | `01F47048` | "Button_12" |
| 0016C400 | `0016C404` `lea` | `01F47008` | "Button_13" |
| 0016C420 | `0016C424` `lea` | `01F46FC8` | "Button_14" |
| 0016C440 | `0016C444` `lea` | `01F46F88` | "Button_15" |
| 0016C460 | `0016C464` `lea` | `01F47488` | "Button_1" |
| 0016C480 | `0016C484` `lea` | `01F47408` | "Button_2" |
| 0016C4A0 | `0016C4A4` `lea` | `01F47388` | "Button_3" |
| 0016C4C0 | `0016C4C4` `lea` | `01F47328` | "Button_4" |
| 0016C4E0 | `0016C4E4` `lea` | `01F472C8` | "Button_5" |
| 0016C500 | `0016C504` `lea` | `01F47268` | "Button_6" |
| 0016C520 | `0016C524` `lea` | `01F47208` | "Button_7" |
| 0016C540 | `0016C544` `lea` | `01F471A8` | "Button_8" |
| 0016C560 | `0016C564` `lea` | `01F47148` | "Button_9" |
| 0016C580 | `0016C584` `lea` | `01F47448` | "Button_A" |
| 0016C5A0 | `0016C5A4` `lea` | `01F473C8` | "Button_B" |
| 0016C5C0 | `0016C5C4` `lea` | `01F47168` | "Button_Back" |
| 0016C5E0 | `0016C5E4` `lea` | `01F473E8` | "Button_Circle" |
| 0016C600 | `0016C604` `lea` | `01F47468` | "Button_Cross" |
| 0016C620 | `0016C624` `lea` | `01F46FA8` | "Button_Down" |
| 0016C640 | `0016C644` `lea` | `01F47308` | "Button_L1" |
| 0016C660 | `0016C664` `lea` | `01F47248` | "Button_L2" |
| 0016C680 | `0016C684` `lea` | `01F470E8` | "Button_L3" |
| 0016C6A0 | `0016C6A4` `lea` | `01F472E8` | "Button_LB" |
| 0016C6C0 | `0016C6C4` `lea` | `01F470C8` | "Button_LS" |
| 0016C6E0 | `0016C6E4` `lea` | `01F47228` | "Button_LT" |
| 0016C700 | `0016C704` `lea` | `01F474A8` | "Button_LeftMB" |
| 0016C720 | `0016C724` `lea` | `01F46F68` | "Button_Left" |
| 0016C740 | `0016C744` `lea` | `01F47428` | "Button_MiddleMB" |
| 0016C760 | `0016C764` `lea` | `01F472A8` | "Button_R1" |
| 0016C780 | `0016C784` `lea` | `01F471E8` | "Button_R2" |
| 0016C7A0 | `0016C7A4` `lea` | `01F47088` | "Button_R3" |
| 0016C7C0 | `0016C7C4` `lea` | `01F47288` | "Button_RB" |
| 0016C7E0 | `0016C7E4` `lea` | `01F47068` | "Button_RS" |
| 0016C800 | `0016C804` `lea` | `01F471C8` | "Button_RT" |
| 0016C820 | `0016C824` `lea` | `01F473A8` | "Button_RightMB" |
| 0016C840 | `0016C844` `lea` | `01F46FE8` | "Button_Right" |
| 0016C860 | `0016C864` `lea` | `01F47188` | "Button_Select" |
| 0016C880 | `0016C884` `lea` | `01F474E8` | "Button_Square" |
| 0016C8A0 | `0016C8A4` `lea` | `01F47128` | "Button_Start" |
| 0016C8C0 | `0016C8C4` `lea` | `01F47368` | "Button_Triangle" |
| 0016C8E0 | `0016C8E4` `lea` | `01F47028` | "Button_Up" |
| 0016C900 | `0016C904` `lea` | `01F474C8` | "Button_X" |
| 0016C920 | `0016C924` `lea` | `01F47348` | "Button_Y" |
| 0016C940 | `0016C944` `lea` | `01F47528` | "Empty" |
| 0016C960 | `0016C964` `lea` | `01F46AE8` | "Key_0" |
| 0016C980 | `0016C984` `lea` | `01F46C08` | "Key_1" |
| 0016C9A0 | `0016C9A4` `lea` | `01F46BE8` | "Key_2" |
| 0016C9C0 | `0016C9C4` `lea` | `01F46BC8` | "Key_3" |
| 0016C9E0 | `0016C9E4` `lea` | `01F46BA8` | "Key_4" |
| 0016CA00 | `0016CA04` `lea` | `01F46B88` | "Key_5" |
| 0016CA20 | `0016CA24` `lea` | `01F46B68` | "Key_6" |
| 0016CA40 | `0016CA44` `lea` | `01F46B48` | "Key_7" |
| 0016CA60 | `0016CA64` `lea` | `01F46B28` | "Key_8" |
| 0016CA80 | `0016CA84` `lea` | `01F46B08` | "Key_9" |
| 0016CAA0 | `0016CAA4` `lea` | `01F46F48` | "Key_A" |
| 0016CAC0 | `0016CAC4` `lea` | `01F46368` | "Key_AccentGrave" |
| 0016CAE0 | `0016CAE4` `lea` | `01F467E8` | "Key_Apostrophe" |
| 0016CB00 | `0016CB04` `lea` | `01F46F28` | "Key_B" |
| 0016CB20 | `0016CB24` `lea` | `01F46828` | "Key_Backslash" |
| 0016CB40 | `0016CB44` `lea` | `01F46908` | "Key_Backspace" |
| 0016CB60 | `0016CB64` `lea` | `01F46F08` | "Key_C" |
| 0016CB80 | `0016CB84` `lea` | `01F467C8` | "Key_Comma" |
| 0016CBA0 | `0016CBA4` `lea` | `01F46EE8` | "Key_D" |
| 0016CBC0 | `0016CBC4` `lea` | `01F46648` | "Key_Delete" |
| 0016CBE0 | `0016CBE4` `lea` | `01F46708` | "Key_Down" |
| 0016CC00 | `0016CC04` `lea` | `01F46EC8` | "Key_E" |
| 0016CC20 | `0016CC24` `lea` | `01F466C8` | "Key_End" |
| 0016CC40 | `0016CC44` `lea` | `01F46928` | "Key_Enter" |
| 0016CC60 | `0016CC64` `lea` | `01F46888` | "Key_Equals" |
| 0016CC80 | `0016CC84` `lea` | `01F46AC8` | "Key_Escape" |
| 0016CCA0 | `0016CCA4` `lea` | `01F46988` | "Key_F10" |
| 0016CCC0 | `0016CCC4` `lea` | `01F46968` | "Key_F11" |
| 0016CCE0 | `0016CCE4` `lea` | `01F46948` | "Key_F12" |
| 0016CD00 | `0016CD04` `lea` | `01F46AA8` | "Key_F1" |
| 0016CD20 | `0016CD24` `lea` | `01F46A88` | "Key_F2" |
| 0016CD40 | `0016CD44` `lea` | `01F46A68` | "Key_F3" |
| 0016CD60 | `0016CD64` `lea` | `01F46A48` | "Key_F4" |
| 0016CD80 | `0016CD84` `lea` | `01F46A28` | "Key_F5" |
| 0016CDA0 | `0016CDA4` `lea` | `01F46A08` | "Key_F6" |
| 0016CDC0 | `0016CDC4` `lea` | `01F469E8` | "Key_F7" |
| 0016CDE0 | `0016CDE4` `lea` | `01F469C8` | "Key_F8" |
| 0016CE00 | `0016CE04` `lea` | `01F469A8` | "Key_F9" |
| 0016CE20 | `0016CE24` `lea` | `01F46EA8` | "Key_F" |
| 0016CE40 | `0016CE44` `lea` | `01F46E88` | "Key_G" |
| 0016CE60 | `0016CE64` `lea` | `01F46E68` | "Key_H" |
| 0016CE80 | `0016CE84` `lea` | `01F466E8` | "Key_Home" |
| 0016CEA0 | `0016CEA4` `lea` | `01F46E48` | "Key_I" |
| 0016CEC0 | `0016CEC4` `lea` | `01F46668` | "Key_Insert" |
| 0016CEE0 | `0016CEE4` `lea` | `01F46E28` | "Key_J" |
| 0016CF00 | `0016CF04` `lea` | `01F46E08` | "Key_K" |
| 0016CF20 | `0016CF24` `lea` | `01F46DE8` | "Key_L" |
| 0016CF40 | `0016CF44` `lea` | `01F46868` | "Key_LeftBracket" |
| 0016CF60 | `0016CF64` `lea` | `01F463E8` | "Key_Left_Alt" |
| 0016CF80 | `0016CF84` `lea` | `01F46428` | "Key_Left_Control" |
| 0016CFA0 | `0016CFA4` `lea` | `01F46408` | "Key_Left_Shift" |
| 0016CFC0 | `0016CFC4` `lea` | `01F46768` | "Key_Left" |
| 0016CFE0 | `0016CFE4` `lea` | `01F46DC8` | "Key_M" |
| 0016D000 | `0016D004` `lea` | `01F468A8` | "Key_Minus" |
| 0016D020 | `0016D024` `lea` | `01F46DA8` | "Key_N" |
| 0016D040 | `0016D044` `lea` | `01F46508` | "Key_Numpad_0" |
| 0016D060 | `0016D064` `lea` | `01F46628` | "Key_Numpad_1" |
| 0016D080 | `0016D084` `lea` | `01F46608` | "Key_Numpad_2" |
| 0016D0A0 | `0016D0A4` `lea` | `01F465E8` | "Key_Numpad_3" |
| 0016D0C0 | `0016D0C4` `lea` | `01F465C8` | "Key_Numpad_4" |
| 0016D0E0 | `0016D0E4` `lea` | `01F465A8` | "Key_Numpad_5" |
| 0016D100 | `0016D104` `lea` | `01F46588` | "Key_Numpad_6" |
| 0016D120 | `0016D124` `lea` | `01F46568` | "Key_Numpad_7" |
| 0016D140 | `0016D144` `lea` | `01F46548` | "Key_Numpad_8" |
| 0016D160 | `0016D164` `lea` | `01F46528` | "Key_Numpad_9" |
| 0016D180 | `0016D184` `lea` | `01F464C8` | "Key_Numpad_Asterisk" |
| 0016D1A0 | `0016D1A4` `lea` | `01F46468` | "Key_Numpad_Enter" |
| 0016D1C0 | `0016D1C4` `lea` | `01F464A8` | "Key_Numpad_Minus" |
| 0016D1E0 | `0016D1E4` `lea` | `01F46448` | "Key_Numpad_Period" |
| 0016D200 | `0016D204` `lea` | `01F46488` | "Key_Numpad_Plus" |
| 0016D220 | `0016D224` `lea` | `01F464E8` | "Key_Numpad_Slash" |
| 0016D240 | `0016D244` `lea` | `01F46D88` | "Key_O" |
| 0016D260 | `0016D264` `lea` | `01F46D68` | "Key_P" |
| 0016D280 | `0016D284` `lea` | `01F46688` | "Key_PageDown" |
| 0016D2A0 | `0016D2A4` `lea` | `01F466A8` | "Key_PageUp" |
| 0016D2C0 | `0016D2C4` `lea` | `01F467A8` | "Key_Period" |
| 0016D2E0 | `0016D2E4` `lea` | `01F46D48` | "Key_Q" |
| 0016D300 | `0016D304` `lea` | `01F46D28` | "Key_R" |
| 0016D320 | `0016D324` `lea` | `01F46848` | "Key_RightBracket" |
| 0016D340 | `0016D344` `lea` | `01F46388` | "Key_Right_Alt" |
| 0016D360 | `0016D364` `lea` | `01F463C8` | "Key_Right_Control" |
| 0016D380 | `0016D384` `lea` | `01F463A8` | "Key_Right_Shift" |
| 0016D3A0 | `0016D3A4` `lea` | `01F46748` | "Key_Right" |
| 0016D3C0 | `0016D3C4` `lea` | `01F46D08` | "Key_S" |
| 0016D3E0 | `0016D3E4` `lea` | `01F46808` | "Key_Semicolon" |
| 0016D400 | `0016D404` `lea` | `01F46788` | "Key_Slash" |
| 0016D420 | `0016D424` `lea` | `01F468C8` | "Key_Space" |
| 0016D440 | `0016D444` `lea` | `01F46CE8` | "Key_T" |
| 0016D460 | `0016D464` `lea` | `01F468E8` | "Key_Tab" |
| 0016D480 | `0016D484` `lea` | `01F46CC8` | "Key_U" |
| 0016D4A0 | `0016D4A4` `lea` | `01F46728` | "Key_Up" |
| 0016D4C0 | `0016D4C4` `lea` | `01F46CA8` | "Key_V" |
| 0016D4E0 | `0016D4E4` `lea` | `01F46C88` | "Key_W" |
| 0016D500 | `0016D504` `lea` | `01F46C68` | "Key_X" |
| 0016D520 | `0016D524` `lea` | `01F46C48` | "Key_Y" |
| 0016D540 | `0016D544` `lea` | `01F46C28` | "Key_Z" |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-input-name-registry-and-channel-alia-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `008760A0` | 132 B | reads the name pointer qword `[rcx+8]` and returns 0x11 when it is null; otherwise it walks the list whose head is qword `02EB8260`, following each node's qword `+0x10`, comparing the zero-terminated string at each node's qword `+8` byte by byte with the name, and returns 0x12 at the first equal string; when no node matches it stores the old head to qword `[rcx+0x10]`, stores `rcx` to `02EB8260` and returns 0 | `008760AE`, `008760E8`, `008760F5`, `00876100`, `0087610A` |
| `00876490` | 132 B | reads the name pointer qword `[rcx+8]` and returns 0x11 when it is null; otherwise it walks the list whose head is qword `02EB82D8`, following each node's qword `+0x10`, comparing the zero-terminated string at each node's qword `+8` byte by byte with the name, and returns 0x12 at the first equal string; when no node matches it stores the old head to qword `[rcx+0x10]`, stores `rcx` to `02EB82D8` and returns 0 | `0087649E`, `008764D8`, `008764E5`, `008764F0`, `008764FA` |
| `008768A0` | 132 B | reads the name pointer qword `[rcx+8]` and returns 0x11 when it is null; otherwise it walks the list whose head is qword `02EB8348`, following each node's qword `+0x10`, comparing the zero-terminated string at each node's qword `+8` byte by byte with the name, and returns 0x12 at the first equal string; when no node matches it stores the old head to qword `[rcx+0x10]`, stores `rcx` to `02EB8348` and returns 0 | `008768AE`, `008768E8`, `008768F5`, `00876900`, `0087690A` |
| `00876D80` | 222 B | counts the nodes of the list whose head is qword `02EB83B8` (links at qword `+0x10`); when the count differs from dword `[rdx]` it allocates the array with `0017D260(count*8, 8)` and zeroes it (a zero count uses a null array, and a failed allocation returns 0xd), calls `00584730` on the old qword `[rdx+8]` when that differs from the new array, is non-null and dword `[rdx]` is not negative, and stores the new array and count to `[rdx+8]` and `[rdx]`; it then writes each node pointer in list order into the array at `[rdx+8]` and returns 0 | `00876DB5`, `00876DCC`, `00876DD7`, `00876E15`, `00876E30` |
| `00879670` | 222 B | counts the nodes of the list whose head is qword `02EB9D80` (links at qword `+0x10`); when the count differs from dword `[rdx]` it allocates the array with `0017D260(count*8, 8)` and zeroes it (a zero count uses a null array, and a failed allocation returns 0xd), calls `00584730` on the old qword `[rdx+8]` when that differs from the new array, is non-null and dword `[rdx]` is not negative, and stores the new array and count to `[rdx+8]` and `[rdx]`; it then writes each node pointer in list order into the array at `[rdx+8]` and returns 0 | `008796A5`, `008796BC`, `008796C7`, `00879705`, `00879720` |
