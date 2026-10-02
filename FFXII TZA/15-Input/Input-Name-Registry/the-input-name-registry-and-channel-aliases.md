---
system: The input name registry — every bindable name, and which are aliases
category: 15-Input
status: AUDITED
owner_layer: PrimaryOwner:Input
evidence_tier: 1
level: L2
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
