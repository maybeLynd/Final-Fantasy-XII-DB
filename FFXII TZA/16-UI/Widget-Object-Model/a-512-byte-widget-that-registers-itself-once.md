---
system: A 512-byte widget that registers itself once
category: 16-UI
status: AUDITED — the registrar, the latch, the kind-1 and kind-18 arms and the reachability read; the last box (UQ-182, the DT-1 residual count) closed by citation 2026-09-17, tracked on DT-1's row
owner_layer: none — neither the registrar nor the handler carries a ledger owner
evidence_tier: 1
readiness: SEMANTICALLY IDENTIFIED
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 49 addresses cited - 4 data, 12 entry, 32 interior, 1 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-08
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-512-byte-widget-pass-1
  crossref_clean: false
  reopened_count: 0
---

# A 512-byte widget that registers itself once

## 1. What the player sees

Some part of the interface is built the first time something asks for it, and not again while it
exists — because the act of building it sets the very flag that decides whether to build it.
**And it can be taken down: message 18 clears the flag, and the next request builds it again.**

> **Corrected 2026-09-13 (§10).** This section read *"built **exactly once per run** … and then
> never again … nothing will make a second one"*. The handler's own message-18 arm zeroes the
> latch (`0056622D`–`0056622F`), so the widget is built once **per lifetime**, not once per run.

## 2. The registrar is four instructions and a latch

`00565DD0` (38 B) is the only function in the image that names `00565E00`:

```c
void RegisterOnce(void)                              /* 00565DD0 */
{
    Obj *o = *(Obj **)0x0209AC30;
    if (o->_0x168 != 0) return;                      /* already built */
    /* tail-jump */ Widget_Construct(0x200, &FUN_00565E00, NULL);   /* 00244F50 */
}
```

`00244F50` is the widget factory — **already read in full** by
[the unowned-code census](../../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md)
§6, and recorded in `_types/` as `Widget`'s allocation site with `002465F0` as its constructor. It is
cited here, not re-derived.

> **`0x200` bypasses the pool by construction.** The factory's table serves requests of `0x120`
> bytes and under; **512 is over it**, so this widget always comes from the heap arm. The 112-slot
> table is irrelevant to this construction, which a reader tracing the call would not otherwise
> guess.

## 3. The latch closes from the other side

`00565E00` (1,914 B) dispatches on the **first dword of its second argument**:

```asm
00565E27  mov ecx, [rdx]            ; the message kind
00565E29  cmp ecx, 8  / jg          ; > 8  -> one arm
00565E32  je                        ; == 8 -> another
00565E38  cmp ecx, 1  / jne         ; != 1 -> default
          ; kind == 1:
00565E50  mov [rax + 0x168], rdi    ; store SELF into 0x0209AC30->+0x168
00565E57  call 0x2CD510
```

**Kind 1 writes the exact field `00565DD0` tests.** Registration and the handler's kind-1 arm are two
halves of one latch: the registrar refuses while `+0x168` is non-null, and the handler is what makes
it non-null.

**Only the kind-1 arm is read.** `kind > 8`, `kind == 8` and the default are named and unread.

> **⚠ And the unread band is where the latch is released (2026-09-13, §10).** Past `kind > 8` the
> handler tests `0x11F`, then does `sub ecx, 9 / cmp ecx, 9 / ja` and jumps through a **ten-entry
> table at `0056657C`** — kinds **9–18**. So the arms are `1`, `8`, `0x11F`, seven distinct targets
> among `9`–`18` (`11`, `15`, `17` fall through to the default) and the default itself: **ten arms
> plus a default, not four.** Kind **18** is the teardown, and it clears `+0x168`.

## 4. Reachability, on four instruments

`00565E00` was the **second-largest function in this database that no document had ever cited** —
`DT-1`. Every instrument was run, each with a control that is positive for that instrument:

| instrument | result | control |
|---|---:|---|
| `E8 call` | **0** | `001DE4F0` → 1 |
| `E9 jmp` | **0** | `001D1660` → 1 |
| code memory-operand | **1** — the `lea` at `00565DE4` | `02ADD0A8` → 3 |
| raw data-section qword | **0** | `005C5230` → **2,527 slots** |

> **A `call`-only query would have called it unreachable, and a vtable scan would have agreed.** It
> is reached exactly once, as an argument.

## 5. A correction to a measured fact

The census §6 records the factory's table pointer as **`0x02093958`**. **It is `0x0208EA58`.**

```
00244F7F   48 8b 1d d2 9a e4 01     mov rbx, qword ptr [rip + 0x1E49AD2]
           next instruction 0x00244F86  +  0x1E49AD2  =  0x0208EA58
```

`0x02093958` **appears nowhere in the function's 175 bytes** — every RIP-relative operand in the body
was resolved with a tool and there is exactly one, giving `0x0208EA58`. The difference is `0x4F00`,
which is not a transposition.

> **Everything else in that section reproduces exactly**: 112 records, stride `0x120`, default size
> `0xC0`, the two free-slot conditions, the claim writing `+0xA2`, and the fall-through that sends
> both an oversize request and an exhausted table to the same heap arm. **One address in an
> otherwise-correct reading**, and it is corrected there rather than only here.

## 6. Modding notes

- ~~**`0x0209AC30->+0x168` is a one-shot latch.** Clearing it re-arms `00565DD0`; nothing else
  does.~~ **⚠ Corrected 2026-09-13 (§10): the handler clears it itself**, on **message 18**
  (`0056622D  xor ebx, ebx` / `0056622F  mov [rax + 0x168], rbx`). It is a *lifetime* flag, not a
  one-shot: build on demand, release on 18, build again on the next demand. Nothing **outside**
  these two functions touches the field — that part holds, and is now measured: **three
  instructions in two functions in the whole image.**
- **This widget is 512 bytes and never pooled.** Hooking the factory to watch the table will not see
  it.
- **The handler is reached only through the pointer the registrar passes.** There is no call site to
  hook.

## 7. What is not known

- [x] **What this widget is.** 1,914 bytes, ~~four~~ **ten** message arms plus a default (§10), and
      only the kind-1 and kind-18 arms read. The name would come from its other arms or from a
      string. `EJ-1`.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (EJ-1): the inventory category list — one
      row per item category the party currently holds.*
      - **Who opens it.** The only caller of the registrar `00565DD0` is the menu state machine `00281ED0` (`00282127`),
        reached through its request byte map `002825C0` for **request `0x4B8`** alone (the `0x4B3`–`0x53A` band of
        [the Config screen](../Config-Screen/the-config-screen-and-what-a-setting-change-runs.md) §7.1).
      - **What kind 1 builds.** After closing the latch and calling `002CD510` / `002CD4D0` (list setup on `+0xC0` /
        `+0xD0`, with 8), it tests the eight **inventory category flags** with `00252D10(bit)` (image block
        `+0x3244`, set by `002CD650` when a category's derived list is non-empty,
        [the save payload map](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md)
        `+0xB244`). For each set flag it appends a row `002CD3C0(request, text)` (`00565E78`–`00565F60`), in this order:

        | flag bit | category | row request | text id |
        |---:|---|---|---|
        | 7 | key items | `0x40F` | `0xBF3` |
        | 6 | loot | `0x40E` | `0xBF2` |
        | 5 | magicks / technicks | `0x40D` | `0xBF1` |
        | 4 | items | `0x409` | `0xBED` |
        | 1 | weapons | `0x405` | `0xBE9` |
        | 3 | ammunition | `0x408` | `0xBEC` |
        | 2 | armour | `0x406` | `0xBEA` |
        | 8 | accessories | `0x407` | `0xBEB` |

      - It then lays the list out through `002C9BF0`, passing `[01E0C3B0]` (24) and `1.0`.
      - **So a category the party owns nothing of never gets a row**, and the eight requests `0x405`–`0x40F` are the
        category choices.
      - **Not read:** whether rows display in append order, and the eight label strings (text ids `0xBE9`–`0xBF3`
        were not resolved). The name "inventory category list" rests on the flag mapping, not on a string.
- [x] ~~**What `0x0209AC30` is**, beyond holding this latch at `+0x168`.~~ **Answered elsewhere,
      and it was already there when this page was written (2026-09-13, §10):** it is the **UI
      request router's context object** — [the request router](../Request-Router/ui-request-router.md)
      reads its `+0xB8` / `+0xC0` pointer slots and its `+0x3F8` / `+0x400` request words, and
      records that **message-1 handlers publish *self* into `+0xB8` / `+0xC0`**. So `+0x168` is a
      *third* self-publication slot and §3's "latch" is this object's ordinary message-1 protocol,
      not a bespoke mechanism. **456 functions load `0209AC30`.**
- [x] ~~**UQ-181.** **What `002CD510` does** on the kind-1 arm. Unread.~~ **Answered 2026-09-14 (FABLE):**
      it refreshes the inventory category flags and then sets a further band of bits in the same bitfield. All the
      bits live at image block `+0x3244`, and each is set through `00252D40(bit, 1)`.
      1. **The refresh.** It calls the 345-byte category refresh first, the same routine that sets bit *n* for each
         non-empty category (the save payload map's `+0xB244` row).
      2. **Three fixed bits:** `0x33`, `0x2A` and `0x2F`.
      3. **Three conditional bits:** `0x2E`, `0x31` and `0x2C`, set only when the signed byte at `0209A2A9` is
         non-zero (`002CD53D`–`002CD565`).
      4. **One mirror bit per held category.** It tests each category flag again and sets a matching bit:

         | category bit (`00252D10`) | category | bit set |
         |---:|---|---:|
         | 1 | weapons | `0x38` |
         | 3 | ammunition | `0x39` |
         | 2 | armour | `0x3A` |
         | 8 | accessories | `0x3A` |
         | 5 | magicks / technicks | `0x34` |
         | 4 | items | `0x35` |
         | 7 | key items | `0x36` |
         | 6 | loot | `0x37` |

         Armour and accessories share one bit.
      5. **A context byte.** Last, it stores `1` into byte `+0xDE8` of the object at `0209AC30`
         (`002CD63A`–`002CD641`).
      - **Not read:** what bits `0x2A`–`0x3A` gate, who reads them, what the byte at `0209A2A9` is, and what
        `+0xDE8` enables. The category names come from the save payload map. Nothing was executed.
- [x] ~~**UQ-182.** **The remaining 110 uncited residuals.** `DT-1`.~~
      **ANSWERED BY CITATION 2026-09-17 (FABLE): the population this row names is `DT-1`'s, it is tracked on `DT-1`'s own row, and nothing on this page can move it.** The *110* is `DT-1`'s 112 less the update gate's one and this page's one, the same population [the update-gate page](../../00-Engine-Core-Runtime/Per-Frame-Update-Gate/one-word-decides-which-fifteen-subsystems-tick.md)'s UQ-29 named as *111* and closed the same way. `DT-1` was re-measured on 2026-09-16 with `residual_crossref.py`, as [the residual page](../../99-Unresolved-Residual/the-unresolved-158.md) instructs: of the 139 residual functions, 131 are cited by some page and 8 by none; the 102 that left did so by pages being written, not by this widget's arms being read, and *cited* is not *understood*. A fresh run today is not evidence either way: the script's certified-parent input `residual_addrs.txt` is a one-byte file since 2026-09-16 16:15, so it reports zero residuals and rewrites its TSV empty (restored; noticed to SWE2-EC7). This page's own function, `00565E00`, left the uncited set when this page was written, which is the whole of what this page owes `DT-1`.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| `00565E00` has exactly one reference | **four instruments**, each with a positive control (§4) | 1 | PROVEN |
| the registrar is a latch on `+0x168` | `00565DD7 cmp qword [rax+0x168], 0 / jne` | 1 | PROVEN |
| the handler closes the same latch | `00565E50 mov [rax+0x168], rdi` on the kind-1 arm | 1 | PROVEN |
| the request is `0x200` and never pooled | `mov ecx, 0x200` at `00565DEB`; the factory's bound is `0x120` | 1 | PROVEN |
| the table pointer is `0x0208EA58` | raw bytes `48 8b 1d d2 9a e4 01`, displacement resolved with a tool | 1 | PROVEN |
| what the widget is | **not established** | — | UNKNOWN |
| any runtime observation | **none exists** | — | UNKNOWN |

## 9. Related

- [The widget message protocol](the-widget-message-protocol.md) — 32 ids over 267 handlers
- [Contract — the widget object](CONTRACT-widget-object.md) — the construction path this uses
- [Why the unowned code has no owner](../../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md) §6 — the factory, read in full

## 10. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first and read in full, **one address at a time**, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s amendment 2026-09-13b. `0209AC30`
returned ten documents, which is where §7's second unknown turned out to be answered.)*

### The reading reproduces, instruction for instruction, and so does the correction in §5

| claim | measured |
|---|---|
| `00565DD0` 38 B, `00565E00` 1,914 B, `00244F50` 175 B | **38 / 1,914 / 175** |
| the registrar loads `0209AC30`, tests `+0x168`, passes `0x200` and tail-jumps the factory | `00565DD0` → `0209AC30`; `00565DD7 cmp qword [rax+0x168], 0`; `00565DE4 lea rdx,[rip+0x15]` → **`00565E00`**; `00565DEB mov ecx, 0x200`; `00565DF0 jmp 0x244F50` |
| the handler dispatches on `[rdx]` and kind 1 stores self | `00565E27 mov ecx,[rdx]`; `00565E50 mov [rax+0x168], rdi`; `00565E57 call 0x2CD510` |
| the four instruments: `E8` 0, `E9` 0, memory-operand **1**, data qword 0 | **0, 0, 1** (the `lea` at `00565DE4`), **0** |
| §5: the factory's table pointer is `0208EA58`, not `02093958` | `00244F50` has **exactly one** `rip`-relative operand in its 175 bytes, at `00244F7F`, bytes `48 8b 1d d2 9a e4 01` → **`0208EA58`**; `02093958` does not occur in the body |

§5 is therefore confirmed as written, including its *"appears nowhere in the function's 175 bytes"*.

### ⚠ The widget is not built once per run — its own handler tears it down

§3 says *"only the kind-1 arm is read"*. The release is in the unread band:

```asm
005661E3  cmp   ecx, 0x11F
005661E9  jg    0x566552          ; default
005661EF  je    0x566476
005661F5  sub   ecx, 9
005661F8  cmp   ecx, 9
005661FB  ja    0x566552           ; default
0056620B  mov   ecx, [rdx + rax*4 + 0x44657C]   ; a TEN-entry table at 0056657C
00566215  jmp   rcx
          ; kind 18 lands here:
00566217  call  0x2922F0
0056621C  mov   ecx, 0x4B8
00566221  call  0x2814E0
00566226  mov   rax, [rip + 0x1B34A03]          ; 0209AC30
0056622D  xor   ebx, ebx
0056622F  mov   qword ptr [rax + 0x168], rbx    ; <- the latch, cleared
```

| kind | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | **18** |
|---|---|---|---|---|---|---|---|---|---|---|
| target | `00566451` | `00566275` | *default* | `005662A0` | `00566422` | `0056623D` | *default* | `0056615D` | *default* | **`00566217`** |

The table is followed immediately by `int3` padding, so ten entries is the whole of it.

> **Message 18 is the widget teardown, and the sibling page already says so** —
> [the widget message protocol](the-widget-message-protocol.md) speaks of *"a handler that relinks or
> frees nodes during message 18"*. So this is not an exotic arm: it is the standard destroy message,
> and this widget's destroy arm releases the registrar's latch. **§1's "nothing will make a second
> one" and §6's "nothing else does" are both refuted by the same three instructions**, in the band
> §3 declared unread. *The unread arm contained the refutation of the read one's conclusion.*

**What survives, measured rather than assumed:** nothing *outside* these two functions touches the
field. Sweeping every listed function for a load of `0209AC30` followed by a `+0x168` access returns
**three instructions in two functions** — the registrar's `cmp`, the kind-1 `mov`, and the kind-18
`mov`. The "nothing else does" half of §6 is true of the rest of the image; it was the handler itself
that was overlooked.

### §7's second unknown was answered before this page was written

`0209AC30` is the **UI request router's context object**.
[The request router](../Request-Router/ui-request-router.md) reads its `+0xB8` / `+0xC0` pointer
slots and its `+0x3F8` / `+0x400` request words, and records that **message-1 handlers publish self
into `+0xB8` / `+0xC0`** — the same idiom this page describes at `+0x168` and calls a latch. A sweep
finds **456 functions** loading the global, with offsets from `+0x4` to `+0xDED`. So §3's "latch" is
one instance of a documented protocol, and the interesting fact is not that a field is written but
**which slot this widget claims.**

### A fifth reference form, with a control

The instrument table's *"raw data-section qword — 0"* is correct, and incomplete: `00565E00` occurs
**three times as a 32-bit RVA** — twice in `.rdata`, once in `.pdata`. **Those are unwind and
exception metadata, not references**, and the control says so: `00565DD0`, `00328370` and `00512CD0`
— all frameless — occur **zero** times in that form, while `00244F50` occurs once. A function that
pushes six registers gets a `.pdata` entry; a leaf does not. **The reachability conclusion is
untouched**, but on x64 the runtime tables address code by 32-bit RVA, and a four-instrument sweep
that looks only for 64-bit pointers does not say so.

**Not claimed.** What the widget *is* — `EJ-1` stays open, now with eight unread arms rather than
three. What `002CD510`, `002922F0` or `002814E0(0x4B8)` do. Which message sender issues 18 to this
widget, or when. Whether `+0xB8` / `+0xC0` / `+0x168` are the only self-publication slots on the
router context — three are known, the rest of the 456 callers' offsets were listed, not read.
Nothing was executed and nothing was observed live.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Input — SERVICE.** `002814E0` on this page calls `FUN_001e0f20`, owned by that layer. What it reaches is a 21-byte forwarder: it calls `00198790` and tail-jumps to `001986D0` with the result; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — SERVICE.** `001D1660` on this page calls `FUN_002eeee0`, owned by that layer. What it reaches is a 295-byte step through a packed `(kind << 16) | index` id: when the index goes negative it looks the kind up in the **eight-entry `.rdata` table** at `00D0F870`, steps to the neighbouring kind modulo eight, and restarts the index at zero - so the id wraps across kinds rather than running off the end; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).
- **Items_Equipment_Shops_License - CLIENT (1 edge).** `002CD650` is called by bodies filed to Items_Equipment_Shops_License: InventoryDerivedIndex_AddPresentItem (`00252E60`) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT (1 edge).** `002814E0` is called by bodies filed to Save_Load_Settings: SaveLoad_ControllerLifecycleHandler (`00582860`) - shared machinery across the layer boundary, no shared ownership.

