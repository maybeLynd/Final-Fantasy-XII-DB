---
system: The widget message protocol — the id space every menu answers
category: 16-UI
status: DOCUMENTED — no handler unread, every id of the 56-id recount named or dispositioned (section 10) and no residue sentence left without an answer, a pointer or a request id (owner re-status 2026-10-01, OPUS, on SWE2-CONTRACT's DD batch 10 and SWE2-STRUCT's DD batch 17, swe2struct-ddres-b17-0930) — the residue this line named is answered in place (SWE2-CONTRACT DD batch 10) - the handler table now holds 264 exact rows, no upper bound and 3 unparsed rows, all three read (a no-op, a thunk to it, and a thunk to 003EE420, which answers 1, 2 and 4); every id of the 56-id recount is named or dispositioned (section 10) (was — 24 handlers UNPARSED and several ids UNRESOLVED in the census)
owner_layer: PrimaryOwner:UI
evidence_tier: 1
level: L2
readiness: BEHAVIORALLY UNDERSTOOD
confidence: HIGH
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 224 addresses cited - 28 data, 109 entry, 87 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-08
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-widget-message-protocol-pass-1
  crossref_clean: false
  reopened_count: 0
---

# The widget message protocol — the id space every menu answers

## 1. What the player sees

Every window, list, panel, gauge and options row in FFXII — the main menu, the licence board, the
battle command window, the Config screen, the map — is the same kind of object underneath, and each
one is told what to do by a stream of small numbered messages: *you are being drawn now*, *your value
changed*, *the player pushed left*, *you are being closed*.

**A modder who wants a new panel to behave like the game's own panels has to answer the same
messages.** This document names them, says how many of the game's 267 panels answer each, and is
honest about the ones it could not read.

*Brought current 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17): no handler is left unread. DD batch 10 read the last
three unparsed rows (§3's note and the batch-10 section at the end, W1–W3), so the sentence above now describes how
the census was built, not an open item.*

## 2. The protocol

An object's handler sits at `+0x00` — the slot `002465F0` installs, per
[the widget constructor](the-widget-constructor-and-object-sizes.md) — and is called as:

```c
void handler(Widget *self, const WidgetMessage *msg);

struct WidgetMessage {          /* 24 bytes */
    int32_t id;                 /* +0x00 */
    /* +0x04 padding */
    uint64_t a;                 /* +0x08 */
    uint64_t b;                 /* +0x10 */
};
```

The 24-byte shape and the `id`-first layout come from
[the widget tree draw pass](../../99-Unresolved-Residual/the-widget-tree-draw-pass.md), which found
the draw pass sending three such records from `.rdata` (`009151C0` = 3, `009151D8` = 4,
`009151F0` = 5). The Config screen block found handlers building them on the stack instead — the
record is a value, not a shared constant.

## 3. How the population was enumerated

`Database/Tools/analysis-kit/gfz-scripts/widget_messages.py`, three passes, each with its own
denominator. Pass 3 (`--senders`) is §8.

**Pass 1 — who are the handlers?** One rule, per
[the widget contract](CONTRACT-widget-object.md) §15b: **a widget procedure is an address that
reaches a constructor's `proc` slot.** The instrument computes reaching definitions of the slot
register over each caller's control-flow graph — no list of installation idioms:

```
00244F50(size ecx, handler rdx, initmsg r8)     -> handler in RDX
002465F0(obj rcx, size edx, handler r8, …)      -> handler in R8
00245000(obj rcx, size edx, handler r8, …)      -> handler in R8   (thin wrapper)
```

| | |
|---|---:|
| constructor transfer sites found (`call` + `jmp`) | **297** |
| sites resolved to a `lea` def | **291** (98.0 %) |
| sites not fully resolved | 6 |
| **population used below** | **267** |

> ### What the CFG buys that the address-order scan could not see
>
> The old scan attributed to a call the last `lea` **before** it, then patched the gaps with a
> candidate list. The reaching-definitions pass replaces all of it: a handler chosen on a branch
> that jumps **backward** into a shared call site (`lea rdx, 0023B330` at `0023C0CD`, branch back
> to the call at `0023BFFF`) reaches the slot through the back-edge; a branch choosing between two
> handlers produces two reaching `lea` defs and both count (`multi`, 12 procedures); `jmp`
> tail-transfers are transfer sites like `call` (`tail`, 16); and a `mov rdx, r9` / `mov rdx, r15`
> def marks a **forwarder** whose callers are then asked the same question (`forwarded`, 5 — the
> `00564AC0` hop; the `00406E80` pair `00407590`/`004079A0` share their call site with a second
> reaching `lea`, so they count under `multi`). An address `lea`'d into a slot register but consumed by a *different*
> call simply does not reach a constructor — which is why `0027D700`/`0027D740`/`0027E3E0`/
> `0027E4E0`/`0027E7B0` drop out without needing a separate exclusion rule.

**Pass 2 — which ids does each handler answer?** MSVC emits two shapes, and some handlers use both:

```asm
; chain                                  ; dense switch
mov ecx, [rdx]                           mov eax, [rdx]
sub ecx, 1  ; je  -> id 1                dec eax
sub ecx, 3  ; je  -> id 4                cmp eax, 0x11
sub ecx, 6  ; je  -> id 10               ja  default
cmp ecx, 2  ; jne -> id 14               jmp [table + eax*4]     ; ids 1 … 18
```

Arms equal to the `ja` target are the default and are **dropped**, so a 23-slot table with 11 dead
rows reports 12 live ids, not 23.

| | count | of 267 |
|---|---:|---:|
| **EXACT** — chain decoded, or table arms resolved | **232** | 86.9 % |
| **UPPER BOUND** — dense switch, arm table not located | 11 | 4.1 % |
| **UNPARSED** — shape this tool cannot read | 24 | 9.0 % |

**The upper-bound rows are excluded from every count below.** A switch bounded at 52 does not mean
52 messages are answered, and an earlier version of this tool published a census in which it did.

*Brought current 2026-09-30 (SWE2-CONTRACT, DD batch 10, check W1): the table above is the 2026-09-15 regeneration.
[`widget-message-handlers.tsv`](widget-message-handlers.tsv) today holds **264 EXACT, 0 UPPER BOUND and 3 UNPARSED**
of the same 267. All three unparsed rows are read (the section at the end of this page), so no handler's id set is
unknown.*

Full table: [`widget-message-handlers.tsv`](widget-message-handlers.tsv).

## 4. The id space

**Denominator: the 232 handlers decoded exactly.**

> **The table below is preserved as written and its numbers are stale — re-derived 2026-09-20
> (FABLE, Claude Opus 5).** `widget-message-handlers.tsv` now holds **264** exactly-decoded
> handlers, not 232, as peers resolved rows through the day; every count here moved with it.
> Re-derived from the current table: **1** → 262 (99.2 %), **2** → 158, **3** → 29, **4** → 78,
> **5** → 4, **6** → 10, **7** → 2, **8** → 20, **9** → 18, **10** → 61, **11** → 4,
> **12** → 71, **14** → 62, **15** → 75, **16** → 42, **18** → 171, **19** → 35, **20** → 22,
> and the high band **285** → 3, **286** → 4, **287** → 3, **288** → 2, **289** → 1. *Those are
> ROW counts.* `286`'s four rows all forward the id rather than answering it, and the receiver they
> forward to is not a row at all — property 4 below.
>
> *That last row is an independent confirmation of the five-id band* — it comes from the handler
> table rather than from the dispatch reading above, and it names handlers for `286` and `288`
> without being asked to. **The shares are recomputed against 264**, so they are not comparable
> cell-by-cell with the percentages below.

| id | handlers | share | what it is, where known |
|---:|---:|---:|---|
| **1** | **222** | **95.7 %** | **CONSTRUCT** — sent by the constructor `002465F0`; §9 |
| **2** | 137 | 59.1 % | **GENERATION RECONCILE** — sent by `00248030`; §9 |
| 3 | 28 | 12.1 % | **draw: before content** — from the draw pass |
| **4** | 65 | 28.0 % | **draw: after content** — from the draw pass |
| 5 | 4 | 1.7 % | **draw: after children** — from the draw pass |
| 6 | 5 | 2.2 % | ~~UNRESOLVED~~ **ENABLED** — `002473F0` (`add ecx, 7` on a negated boolean), named 2026-09-13 (§9, `DL-1`) *(table brought current 2026-09-25, FABLE, Claude Opus 5.5)* |
| 7 | 2 | 0.9 % | ~~UNRESOLVED~~ **DISABLED** — the other value of the same sender, and `00247490`, named 2026-09-13 (§9, `DL-1`) *(table brought current 2026-09-25, FABLE, Claude Opus 5.5)* |
| **8** | 12 | 5.2 % | **FOCUS GAINED** — sent by the focus switch `00244830`, which sets `+0x40` bit 4 and stores the widget in `0208EBC0`; the record's second dword is a 0/1 flag (§9c, 2026-09-20) |
| **9** | 9 | 3.9 % | **FOCUS LOST** — the other half of the same switch, which clears `+0x40` bit 4 first (§9c, 2026-09-20) |
| **10** | 45 | 19.4 % | **sample directional input and change the value** — from the Config screen *(2026-09-28, FABLE, Claude Opus 5.5: the only sender is the focus notice `002481C0` - its `.rdata` record `{10}` has no other reference - so every handler receives it only as the focus top, at the frame positions of [gg1-static-order](../../_index/candidates/gg1-static-order/README.md); 16 readers of the input snapshot `02F9736A` read it in this arm, [record](../../_index/candidates/gg1-message10-readers/README.md))* |
| 11 | 2 | 0.9 % | ~~UNRESOLVED~~ **INPUT NOTICE DURING A TRANSITION** — `002481C0` sends `{11}` to the focus top when a node on its chain has `+0x40` bit 9, and `{10}` otherwise (§10, 2026-09-25) *(table brought current 2026-09-25, FABLE, Claude Opus 5.5)* |
| **12** | 66 | 28.4 % | **enable/disable: `self->disabledFlag = (msg->a == 1)`** — from the Config screen |
| 13 | 5 | 2.2 % | **notify, carrying a command id in `msg->a`** — from the Config screen |
| **14** | 55 | 23.7 % | ~~teardown-ish~~ **opening transition started** (corrected 2026-09-13 on `OPUS-DL1-MESSAGE14-RECEIVER`): its only framework sender, `00246AD0`, clears the close bit 6, sets `+0x7C` state 2 with direction +1, and sends record `01E0C0E0` = `{14}` as its last act (`00246BEF`–`00246C09`; the record's only reference). The Config brightness row's arm tail-calls `002470D0`, which pushes the widget onto the focus stack (`00244830`) — a receiver taking focus as it opens. The re-base of `0208F570` that `00228130` performs is **message 18**, not 14: its dispatch subtracts 1, 1 and 2 before `cmp ecx, 0xE` (`0022813B`–`00228159`), so it answers 1, 2, 4 and 18 |
| **15** | 63 | 27.2 % | **ABOUT TO BE DESTROYED**, self only — sent by `00244F00`; §9 |
| 16 | 35 | 15.1 % | ~~UNRESOLVED~~ **RESOURCE BATCH COMPLETE** — framework senders `00249410` / `002494F0` / `002495C0`, named 2026-09-13 (`DL-1`); also the most widely sent application message, ~~20 senders~~ 17 senders *(Corrected 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17): of the 20 sites, three are the framework senders themselves; §8's note)*; §8 *(table brought current 2026-09-25, FABLE, Claude Opus 5.5)* |
| **17** | 8 | 3.4 % | **POSITION TWEEN FINISHED** — `00246C20` channel 0, sent exactly when the eased value reaches `1.0` (§9a, 2026-09-20) |
| **18** | **151** | **65.1 %** | **BEING DESTROYED**, self and whole subtree — `00245020` then `002473B0`; §9 |
| 19 | 28 | 12.1 % | ~~UNRESOLVED~~ **TRANSITION FINISHED, FORWARD** — `00246C20` on a positive direction (above), named 2026-09-13 *(table brought current 2026-09-25, FABLE, Claude Opus 5.5)* |
| 20 | 18 | 7.8 % | ~~UNRESOLVED~~ **TRANSITION FINISHED, BACKWARD** — `00246C20` on a negative direction (above), named 2026-09-13 *(table brought current 2026-09-25, FABLE, Claude Opus 5.5)* |
| **21** / **22** / **23** | 1–3 each | ≤ 1.3 % | the other three **tween-channel** messages of `00246C20`: **22** = position tween stepped, **21** = extent tween stepped, **23** = scalar tween stepped (§9a, 2026-09-20) |
| **26** | 1–3 | ≤ 1.3 % | **a per-element QUERY**, not a notification — `{26, (i64)index}`, and the **return value is consumed**: non-zero releases a clip suspension raised under message 3 (§9d, 2026-09-20) |
| **29** | 1–3 | ≤ 1.3 % | **STATE CHANGED** — a **self-sent** notice with a zeroed record, from five independent senders, each as the last act of writing the object's own fields (§9f, 2026-09-20) |
| 25, 30 | 1–3 each | ≤ 1.3 % | 25 = animation step (§9); ~~**30** narrowed — two incompatible sender shapes, one of which consumes the return (§9f)~~ **30 is application-defined** — screen-only senders with per-screen payloads (§10, 2026-09-25) *(table brought current 2026-09-25, FABLE, Claude Opus 5.5)* |
| **24** | 5 | 2.2 % | **RELEASED** — sent by `002482E0` after the children are cleaned and self is unlinked, just before the handler slot is nulled; §9 (2026-09-13) |
| **53** | 1 | 0.4 % | **DESTROY REQUEST** — "tear yourself down"; both receivers answer with the destroy entry `00244F00` (§9e, 2026-09-20) |
| **285–289** | 1 each for 285/287/289; 286 and 288 have their own | 0.4 % | **not framework messages at all** — private per-screen channels with a different record shape; dispositioned as a family below (2026-09-20, **band corrected to five 2026-09-20**) |

**28 distinct ids in `1 … 30`, plus `53`, plus a five-value band at `285–289`.**

> **That sentence describes the table above, and the table is stale — carried here 2026-09-20
> (FABLE, Claude Opus 5).** ***The count is not mine.*** **OPUS reconciled it at `56` the same
> day**, in
> [`CONTRACT-widget-object.md` §15c](CONTRACT-widget-object.md), against the 264 `exact` rows of
> `widget-message-handlers.tsv`: ids **`1`–`53` except `27` and `28`**, plus the five at
> **`285`–`289`**. The 24-id gap is **ids `31`–`52`**, which this page has never listed, and §15c
> shows it is two different things — eleven handlers `widget_messages.py` *admits* it does not
> count, and six it reports confidently with one id each, the same pivot-only defect that hid
> `286` and `288`. *I re-ran the count myself before carrying it and got the same 264 and 56.*
>
> **What is a page-side matter rather than a recount:** §15c deliberately does not name those
> bodies, to avoid importing ten Items/Equipment/Shops/License edges and two CombatAction edges
> into a reconciliation section, and points at the rows instead — so the addresses stay in
> `widget-message-handlers.tsv`, and this note follows the same rule. **The shares in the table
> above are computed against 232 and are not comparable cell-by-cell with anything derived from
> 264.** And `DL-1`, which still counts "3 remain" against the old denominator, is corrected
> separately.

### `285`, `287`, `289` are private screen channels, not framework messages — 2026-09-20 (FABLE, Claude Opus 5)

*Dispositioned as a family. Each one's meaning is a question about one screen; what they have in common is a question
about the protocol, and that is the part that was worth answering.*

> **The band is five, not three — corrected 2026-09-20 (FABLE, Claude Opus 5) on
> `OPUS-NOTICE-FABLE-THE-HIGH-ID-BAND-HAS-FIVE-MEMBERS-NOT-THREE`.** This section was written
> around `285`, `287` and `289` because those were the ids the handler table carried. **`286`
> (`0x11E`) and `288` (`0x120`) have handlers too**, so the band is the contiguous run
> `285`–`289`. The handler table credits `286` to `005636F0`, `00563930`, `00563B10` and
> `00563D20` — four bodies of the license-board family, each ending `cmp eax, 0x11E` / `je`.
> **Those four FORWARD it; they do not receive it** (see the note below). `288` is answered by
> `0027F5D0` (`0027F860 cmp ecx, 0x120`) and by `002D70F0`, which
> reaches the same id by arithmetic: `002D7470 sub ecx, 0x12`, `002D7479 sub ecx, 1`, then
> `002D747E cmp ecx, 0x10D` — and `0x10D + 0x13` is `0x120`.
>
> **Why they were invisible, which is the reusable part:** both rows named only the **pivot** of
> their binary-search root, and the extractor records a pivot as an `exact` id rather than as a
> bound. *Any id recovered from a binary-search dispatch through that tool is a lower bound on the
> set, not the set.* **That mechanism is OPUS's**, read end to end across ten under-reporting rows
> and published the same day in [`CONTRACT-widget-object.md` §15c](CONTRACT-widget-object.md) and
> in the rows' own notes; the notice that reached me is one consequence of it, and §15c states
> outright that the six confident under-reports "supply `286` and `288`, completing the high band".
> What this section owes it is the correction below, not the discovery.
>
> **It strengthens this section's conclusion rather than weakening it.** A three-id scatter is thin
> evidence for "deliberately outside the table"; a **contiguous five-value block at `0x11D`, with
> 231 unused values between it and the low band**, is a second family with its own base, which is
> what "deliberately outside" means.

Three properties separate them from every id in `1 … 53`. **They were established for `285`, `287`
and `289`; `286` and `288` are not re-measured here**, so read the three below as holding of those
three ids, not of the whole band:

1. ~~**Exactly one receiver each** — `0055CD40` for 285 (`0x11D`), `00280DE0` for 287 (`0x11F`),
   `005691E0` for 289 (`0x121`), each an `exact`-decoded handler.~~ **WITHDRAWN 2026-09-20 (FABLE,
   Claude Opus 5): only `289` has one receiver.** The dispatch table this page consumes now lists
   **three** handlers for `285` — `003FF360`, `00557DB0`, `0055CD40` — and **three** for `287` —
   `00280DE0`, `002C2320`, `00565E00`. Only `289` is still singular.

   > *How I got this wrong is worth more than the count.* I first tested it with a raw `.text` scan
   > for `cmp r32, imm32` against `0x11D`–`0x121`, which returns extra sites and looks like a
   > refutation. It is **not** one: the cluster at `001ECBD5`, `001ECBED` and `001ECF15` lies inside
   > `001EC760`, whose same dispatch also compares `0x197`, `0x17A` and `0x1B9` — a different id
   > space reusing small integers. Having shown *that instrument* was unsuitable, **I reported the
   > property as surviving without running the suitable one**, which is the table itself.
   > **"The test I ran was invalid" is not "the claim is true".**
2. ~~**Tested before the table.** Each receiver reads the id (`mov eax, dword ptr [rdx]`) and takes a **dedicated `je`
   on its own large constant** — `0055CD53 cmp eax, 0x11D`, `00280DF1 cmp eax, 0x11F`, `00569204 cmp eax, 0x121` —
   *before* the `cmp` that bounds its ordinary small-id jump table (`0x16`, `0x12`, `0x19` respectively). They are
   deliberately outside the table, not overflowing it.~~ **WITHDRAWN 2026-09-20 (FABLE, Claude Opus 5).** OPUS found
   this while verifying the withdrawal above and filed it as
   `OPUS-FILE-CON-WIDGET-HIGH-BAND-PRETEST-REFUTED`; I read all five receivers before carrying it here, and it is
   wrong in three separate ways.

   **(a) The compare is not dedicated — it is the pivot of the dispatch root.** At `0055CD40` the very compare cited
   is the one that bounds the small-id table:

   ```asm
   0055CD4B  mov eax, dword ptr [rdx]
   0055CD53  cmp eax, 0x11d      ; the cited "dedicated" test ...
   0055CD58  jg  0x55db1d        ; ... whose OWN jg is the table's upper bound
   0055CD5E  je  0x55d84b        ; ... and whose je is simply this switch's far case label
   0055CD64  dec eax
   0055CD66  cmp eax, 0x16       ; the "ordinary small-id table" bound
   0055CD69  ja  0x55db1d
   ```

   One three-way split, not a test placed in front of a table. `00280DE0` (`0x11F` / `jg` / `je` / `dec` /
   `cmp 0x12`) and `005691E0` (`0x121` / `jg` / `je` / `dec` / `cmp 0x19`) have the identical shape.

   **(b) At `00557DB0` the large constant is tested LAST, not first.** Its root is `cmp ecx, 0xa`; `0x11D` is not
   reached until `00558598`, after `0xA`, `0x13`, `0xC`, `0xF`, `0x12` and `0x14` — six small ids ahead of it.

   **(c) At `003FF360` the constant `0x11D` never appears.** The id is decremented twice on the way down, so the
   site that selects 285 compares a different number entirely: `003FF784 sub ecx, 0x12`, `003FF78D sub ecx, 1`,
   `003FF796 cmp ecx, 0x10a` — and `0x10A + 0x13 = 0x11D`.

   **What this costs the section.** The dispatch shape is whatever MSVC emitted for each function's own case set, so
   it carries no information about whether an id was "deliberately outside the table" — and the property was read
   off the three receivers that happened to put their pivot first. *The claim was formed from three functions and
   refuted by the fourth and fifth; it never had the population behind it.* Property 3 is unaffected, and the
   band's contiguity is the stronger structural argument.
3. **A two-argument record.** Where a framework message carries a small flag at `+8`, these carry **two 64-bit
   arguments** at `+8` and `+0x10`. 287 even has a **private generic sender**: `002C9EB0(target, a, b)`, 101 bytes,
   whose entire body is `movsxd`/`movsxd` into `[rsp+0x28]`/`[rsp+0x30]`, `mov dword ptr [rsp+0x20], 0x11F`, and a
   call through `[target]` — a helper that exists for this one id.

   > **Narrowed 2026-09-20 (FABLE, Claude Opus 5), against my own reading.** "Where a framework
   > message carries a small flag at `+8`" is too strong. `005636F0`'s **message-1** arm reads
   > *both* slots — `00563726 mov eax, dword ptr [rdx + 0x10]` and `0056372F mov eax, dword ptr
   > [rdx + 8]` — so a framework message uses `+8` and `+0x10` too. What actually separates the
   > band is the **width**: the band's receivers read them as **qwords** (`0027F87C cmp rax, qword
   > ptr [rdx + 8]` for 288, `003FF7AF`/`003FF7B5` for 285, `0056538A cmp qword ptr [rdx + 0x10],
   > 0` for 286), where `005636F0` reads **dwords** out of the same offsets. That is still a real
   > difference — it is two 64-bit arguments against four 32-bit ones — but it is a difference of
   > argument type, not of whether arguments exist at all.
   >
   > **And the whole population says so, which I did not measure and OPUS did.**
   > [`CONTRACT-widget-object.md`](CONTRACT-widget-object.md) censuses every one of the 266 bodies
   > that reads the record: `payloadA` is read whole 64 times of 102, **narrower 38 times** (9 one-
   > byte, 9 two-byte, 20 four-byte) and **dereferenced as a pointer 20 times**; `payloadB` 19 of
   > 45 whole, 26 narrower, 7 dereferenced — and *every* dereference is an eight-byte `mov` while
   > *no* narrow read ever is. **The two populations do not overlap.** So the slot is discriminated
   > by the id across the whole protocol, and the band's qwords are one value of that
   > discrimination rather than a property that separates the band from everything else. My
   > single-arm reading is a corroborating instance of a measured rule, not the rule.

4. **`286`'s four table rows are FORWARDERS, not receivers — 2026-09-20 (FABLE, Claude Opus 5).**
   Each of `005636F0`, `00563930`, `00563B10` and `00563D20` sends `0x11E` to the *same* arm as ids
   `4`, `8`–`12`, `18` and `26`, and that arm is an epilogue **tail jump to `005651E0`**; the
   default beside it is `005C5230`, the folded `xor eax,eax; ret`. So the four rows say "this id is
   the parent's business", which is the opposite of a private channel, and they are why "one screen
   per id" had to go.

   **The receiver is `005651E0`, and it has no row of its own in `widget-message-handlers.tsv`** —
   it is named only inside those four rows' notes. *The table is not blind to the forwarding:* all
   four carry `source = forwarded`, where `003FF360` carries `direct` and `00285290` carries `tail`.
   What the table does not carry is the forward's **target** as a handler in its own right. It tests
   `0056537E cmp ecx, 0x11E` and its arm reads `0056538A cmp qword ptr [rdx + 0x10], 0` / `jl` — a
   **signed 64-bit argument**, which is what puts `286` in the band on the surviving property.

   > **How large is that census gap?** Bounded and small: I swept every `exact` row for
   > unconditional `jmp` targets that are function entries, dispatch on `dword ptr [rdx]` and are
   > not themselves rows, and the answer is **exactly two** — `005651E0` (from those four rows) and
   > `003EE420` (from `0027AD70`, answering ids 1, 2 and 4). The control is that the case which
   > motivated the sweep, `005651E0`, must come back, and it does. ***And the second hit is a
   > second control I did not plan:*** `003EE420` **was already known** — OPUS's row re-derivation
   > records `002985C0` as "a `jmp 003EE420` out of the table, the one genuinely open edge", so the
   > sweep recovers a case someone else found by an unrelated route and adds one. **So the table is
   > sound as a table and wrong as a receiver count**: "N handlers answer id X" counts *rows*, and
   > for `286` all four rows pass the id on.

**What `286` asks for — 2026-09-20 (FABLE, Claude Opus 5).** Following the forward gives the id a meaning, and
the mechanism behind it is documented on
[the shop table and its stock gates](../../12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md).
`005651E0`'s arm:

```asm
0056537E  cmp ecx, 0x11e / jne default
0056538A  cmp qword ptr [rdx + 0x10], 0 / jl default   payloadB must be >= 0 - then it is DISCARDED
00565395  mov rax, qword ptr [rdx + 8]                 payloadA is DEREFERENCED
0056539C  movzx edx, word ptr [rax + 8]
005653A0  call 00565720(self, thatWord)
```

and `00565720` releases the widget's built list at `+0xE0`, rebuilds it through the list builder `0057CF20` for
the selector byte the widget was constructed with, and resets every `+0xF0` record to `{ thatWord, -1, -1 }`. **So
`286` is "reset this list widget to the value payloadA carries, and rebuild its list"** — an invalidate-and-refresh,
which is why it has no reply and why the four rows above forward it to the object that owns the list.

**And `word[payloadA + 8]` is not an arbitrary field — it is a copy out of an encoded-id record.** The entry filler
`0057DED0` walks the source as 16-bit ids terminated by `0xFFFF`, resolves each through `0035D380(6, id)` — which
[`CONTRACT-encoded-id-space-and-class-registry.md`](../../00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md)
records as returning **the static `EncodedIdQueryRecord` at `022CA480`**, refilled per call — and copies fields
out: `qword[entry] = 002B58B0(qword[rec+0x18])` **the name pointer**, `word[entry+0xC] = word[rec+0x20]` **the
owned count**, `word[entry+0xE] = word[rec+0x24]` the mode-1 answer, three class bytes, and **`word[entry+8] =
word[rec+6]`**.

*So the word this message carries is `word[rec+6]` of the entry's own id record* — which is why a pointer to one
entry is a sensible payload and why the receiver takes a single word rather than the entry.

> **`word[rec+6]` IS named, and I should have cited it rather than written that it was not — amended 2026-09-21
> (FABLE, Claude Opus 5).** The sentence that stood here said it is "below the region the query-record field map
> covers and is not named here". That is true of the field-map **table**, which begins at `+0x10`, and misleading
> about the store:
> [`the-encoded-id-space-and-the-query-record.md`](../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)
> §2.4 names it three lines above that table — *"`+0` the class (dword), `+4` the row index (dword), **`+6` the
> id** (the high word of `+4` — the word-form wrapper stores `dx` there, `0035D396`)"*. **So the word this message
> carries is the encoded id of the list row**, and the id form writes only a word where the row form writes a dword
> row at `+4`, which is why one eight-byte header serves both wrappers. *A bounded claim about this page went out
> as a claim about the store: a reader chasing that word would have stopped here instead of turning to the page
> that answers it.*

The rest of the mechanism, including what the list is built from, how the selector chooses it, and why the entry's
`+0x10` carries the row's price whole or halved, is on
[the shop table and its stock gates](../../12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md).

**And the one sender that can be traced end to end NARROWS the payload to 32 bits before sending it.** This is the
part of `286` worth a reimplementation's attention, and it took four reads to be sure of, so the chain is given in
full.

`00566680` is created once, by `005665B0`, which is called by `00564E10` with the **list-owning widget as `rcx`**:

```asm
00564EC0  cmp qword ptr [rbx + 0xe0], 0 / je            the built list must exist
00564ED5  mov rcx, rbx / call 005665B0                  rbx = the owner, passed as the parent
005665E6  ...  an index computed from [parent+0xD8]'s +0xEC/+0xED/+0xEE/+0xF2/+0xF4
00566617  lea rdx, [rip + 0x62]                         = 00566680, the child's handler
0056661E  cdqe / shl rax, 5 / add rax, [rcx + 0xe0]     ENTRY POINTER = list base + index*0x20
00566631  mov qword ptr [r11 - 0x40], rax               block[1] = that pointer
00566655  mov ecx, 0xe8 / call 00244F50                 create the 0xE8-byte child
```

so the child's construct arm stores **`block[0]` = the parent into `+0xC0`** and **`block[1]` = a pointer to one
`0x20`-byte list entry into `+0xC8`** (`005668BB`–`005668D8`). `+0xC8` is written **once**, as a qword. Then the
`286` send, inside the child's **message-12** arm, reads it back as:

```asm
005667C5  movsxd rax, dword ptr [rdi + 0xc8]    48 63 87 C8 00 00 00   - the LOW 32 BITS, sign-extended
005667E4  mov dword ptr [rsp + 0x20], 0x11e
005667EC  mov qword ptr [rsp + 0x28], rax       payloadA
00566833  lea rdx, [rsp + 0x20] / call rax      rax = [[self+0xC0]] - the record shape is 002C9EB0's exactly
```

and the receiver dereferences it: `00565395 mov rax, qword ptr [rdx + 8]` / `0056539C movzx edx, word ptr
[rax + 8]`. **A word at `+8` of a `0x20`-byte list entry is exactly what `block[1]` points at**, so the two halves
fit — *except for the truncation*. **The payload is sound only while that list allocation lies below 2 GB.**

> **What is established and what is not.** Established: the sender's `+0xC8` holds a pointer, is written once, and
> is read narrowed; the receiver dereferences the payload. **Not** established: whether the allocation can ever sit
> above 2 GB — the list comes from `002497E0` and that is an allocator question, not a static one. *So this is
> reported as a narrowing with a stated precondition, not as a defect.* It is also the mirror of the population
> rule recorded in [`CONTRACT-widget-object.md`](CONTRACT-widget-object.md) — that every payload **dereference** is
> an eight-byte `mov` and no narrow read ever is. That rule was measured over **receivers**; this is a **sender**
> narrowing a value a receiver will dereference, which the rule does not cover.
>
> *I nearly closed this three ways by assumption.* First by reading the record stores as outgoing stack arguments
> to the `002527B0` call sitting between them — it takes three arguments and reads nothing above `r8`. Then by
> concluding, from the `movsxd`, that `+0xC8` held a small integer and the sender therefore could not be paired
> with this receiver. Then, having found the installer, by resting the pairing on `+0xE0`/`+0xD8`/`+0x180` matching
> between the parent and `00565720`'s object — **matching offsets are not identity**. What actually settles it is
> that `00564E10` hands `005665B0` the very object it has just tested `[rbx+0xE0]` on, and `00565720` is the code
> that fills that field; the offsets are corroboration, not the argument.

What each does, as far as the receivers were read:

| id | senders | what the receiver does with the record |
|---:|---|---|
| 285 | `002C2320`, `002CDF20`, `002CE370` | dispatches **`arg0 − 0xA`**, bounded `≤ 0x11`, over an **18-wide jump table** (`0055D84B`–`0055D86E`) — a sub-command space of `0x0A`…`0x1B` |
| 287 | `002C9EB0` (the generic sender) | accepts **`arg0 == 0x8000`** and **`0x8001`** and ignores every other value (`00281243`–`00281257`) |
| 289 | `005680E0`, `0056B4D0` | **ignores the record** — the senders zero it — and sets `byte[self + 0x331] = 6` when that byte is non-zero (`00569EE3`–`00569EEC`); `005680E0` gates the send on the **adjacent** `byte[self + 0x330]` and sends to **itself** |

**The disposition.** `DL-1` asks what the widget messages mean. These three are not widget messages in that sense:
they are one screen talking to itself over the handler's calling convention, with an id chosen above the framework
range precisely so it cannot collide. Naming each means reading three unrelated screens end to end, and doing that
would answer three screen questions rather than a protocol question. **The protocol question is closed here** — the
high range exists, it is one id per screen, its record shape differs, and its receivers dispatch it ahead of the
framework table. *The three individual meanings stay open and are recorded as such, not as unknown ids.*

*Pointer 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17): each meaning belongs to its screen's page, and those pages
now read them.* **285** is the reply a shared dialog (the Yes/No box `002CDF20`, the message box `002CE370`, or
`002C2320`) posts to the widget that opened it, `{285, the opener's code, the answer}`
([the licence-board widgets](../License-Board-View/the-license-board-screen-widgets.md) §8a, `GI-3`). **289** is the
gambit list's destroy notice to its editor child, which sets the child's `+0x331` to 6
([the gambit screens](../Gambit-Screens/the-gambit-screens.md), the `0x121` row). **287** is the code message that
`002C9EB0` builds; in the Config screen's procedure `00280DE0` its `0x8001` arm applies one change to every row
([the Config screen](../Config-Screen/the-config-screen-and-what-a-setting-change-runs.md) §7.1, "the batch twin").
Its arms in `002C2320` and `00565E00` belong to those screens' pages. *(Checks P1–P3.)*

> ### The shape of the distribution is the finding
>
> **Three ids — 1, 18 and 2 — are answered by more than half the widgets in the game**, and 1 by
> almost all of them. Six more (4, 12, 15, 14, 10, 16) sit between 16 % and 30 %. Everything else is
> a long tail answered by fewer than one widget in ten.
>
> **That is the shape of a lifecycle-plus-events protocol**, not a flat command set: a couple of
> messages every object must answer, a working set of about eight, and specialised messages for the
> handful of objects that need them. A reimplementation needs the first nine to get anything on
> screen; the tail can be filled in per widget.

### The three high ids are real, and they cost the tool a fix

`0055CD40` (3,564 B) tests `cmp eax, 0x11D` / `je` **before** falling into a 23-arm dense switch:

```asm
0055CD4B  mov  eax, [rdx]
0055CD53  cmp  eax, 0x11d          ; 285
0055CD58  jg   default
0055CD5E  je   0x55d84b            ; the outlier id, handled on its own branch
0055CD64  dec  eax
0055CD66  cmp  eax, 0x16
0055CD69  ja   default
0055CD82  jmp  rax                 ; the dense switch, ids 1 … 23
```

**A decoder that reads either shape alone reports a subset.** The first version of this tool listed
this handler as answering exactly one message, id 285, when it answers 285 **plus twelve of the
range 1–23**. Both decoders now run and their results are unioned.

## 5. What the ids mean, and what is honestly unknown

~~**Five of 32 ids have a meaning**~~ — **nine, as of §9 on 2026-09-08**, which added the four most
universal: 1 construct, 2 generation reconcile, 15 pre-destroy, 18 destroy-broadcast, each read from
the function that sends it. The other five were recovered elsewhere: 3, 4, 5 from the draw pass; 10, 12, 13 from the Config screen (14 only partially). The
enumeration above says **which handlers answer which id**; it does not say what any id means.

> **This document deliberately does not guess.** *"18 is answered by 65 % of widgets, so it is
> probably update"* is exactly the kind of sentence the confidence vocabulary exists to prevent.
> Naming `1`, `2`, `15` and `18` needs their handler bodies read, and that is `DL-1`.
>
> *Pointer 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17): all four are named from their senders in §9 (2026-09-08),
> and `DL-1` was answered for the whole 56-id recount on 2026-09-25 (§7's correction). Checks P6, P8.*

## 6. Controls

The decoder was validated against three handlers this database had already read **by hand**, in an
earlier block, for an unrelated reason:

| handler | read by hand | decoder |
|---|---|---|
| `0023B330` (Config brightness row) | 1, 4, 10, 12, 14 | **1, 4, 10, 12, 14** ✓ |
| `0023B6F0` (Config value rows) | 1, 4, 10, 12, 13 | **1, 4, 10, 12, 13** ✓ |
| `0023BD40` (the Config screen itself) | dispatches, `cmp eax, 0x11; ja` | **1 … 18** ✓ |

`0023B330` is the sharper of the three: it is reachable **only** as a candidate, so a tool without
the backward-jump pass would have scored two of three and looked fine.

> **One of those controls caught a real regression.** A first attempt at the dense decoder accepted
> a `cmp` followed by *any* `ja` within 120 instructions. It reported `0023B6F0` — whose five ids
> were known — as answering **ids 2 and 3**, because a distant unrelated `ja` bound to a `cmp` from
> the middle of the chain. **A relaxed pattern did not degrade to a weaker answer; it produced a
> confident wrong one.** The fix was to require the whole shape, jump table included.

## 7. What this does not claim

- ~~**Any meaning for ids 8, 9, 11, 17, 21–23, 26, 29, 30, 53, 285, 287, 289** — **14 of the 32** (recounted 2026-09-13 from
  the handler TSV: the census has no 27 or 28, which the old range `25–30` included; 6, 7, 14, 16, 19, 20, 25 were
  named that day). `DL-1`.
  (1, 2, 15, 18 and — since 2026-09-13 — 24 are named in §9; 3, 4, 5, 10, 12, 13 elsewhere.)~~ *Corrected 2026-09-30
  (SWE2-CONTRACT, DD batch 10): each of these is named or dispositioned. 8 and 9 are named in §9c, 17 and 21–23 in
  §9a, 26 in §10 (with its last two receivers read at the end of this page), 29 in §9f, 53 in §9e, 11 and 30 in §10, and
  285–289 in §4. `DL-1` was answered on 2026-09-25 for every id of the 56-id recount, 31–52 included.*
- ~~**That 251 is the number of widget handlers.** It is 239 confirmed plus 13 candidates, from 280
  constructor sites. Handlers installed by writing `[obj] = fn` directly, without a constructor call,
  would not appear at all — **not measured**, `DL-2`.~~ **`DL-2` answered 2026-09-13 (FABLE):** no direct installs were found, but the population has three other errors. **(1) Direct stores:** image-wide, a `lea reg, [rip + function]` followed within six instructions by `mov qword ptr [base], reg` occurs at 10 sites; none stores a widget procedure — the positive control `0027795C` is found, and the one population member among them, `0027D740`, goes into a battle-menu record. No widget procedure's address sits in a data qword (the two hits, `0017CDE0` in a vtable and `0057E8D0` inside exception-unwind data, are not install tables). **(2) Tail-jump constructor sites:** the census matched `call` only; **17** sites reach the factory by `jmp` (16 to `00244F50`, 1 to `00245000`), and **14** of their procedures are missing — `00285290`, `00291D90`, `0029E110`, `002C13C0`, `002C3560`, `002C4460`, `002CEB40`, `002CF740`, `00393EA0`, `00394130`, `003EF830`, `00406A60`, `00565E00`, `002985D0`. **(3) Forwarding wrappers:** `00564AC0` passes its `r9` to `00244F50` (`00564B4B`) for `005636F0`, `00563930`, `00563B10`, `00563D20` (from `00564B90`) and `0056E140` (from `0056DD50`); `00406E80` passes `r15` (`00407102`) for `00407590` and `004079A0` — **7** more. And **5 of the 13 candidates are not widget procedures**: `0027D700`, `0027D740`, `0027E3E0`, `0027E4E0`, `0027E7B0` take integer `edx`/`r8d` arguments. **So the constructor-reached population is 251 − 5 + 14 + 7 = 267** (the per-id shares were over the old 251 until the regeneration noted below). A shape census (reads `dword [rdx]` early, tail-jumps to `005C5230`) finds 148 procedures, 135 in the population, and every reference to its 13 others is one of the routes above or a direct call. **Limit:** a procedure pointer loaded from memory and stored, or passed through more than one register hop, escapes both instruments.
  **Regenerated 2026-09-15 (FRONTIER, `OPUS-REQ-SWE2-FRONTIER-WIDGETPROC-REGEN`):** `widget_messages.py`
  now implements exactly the §15b rule — reaching-definitions of the slot register over each caller's
  CFG, `call` + `jmp` transfers, `mov R, src` chains chased inside the body, one forwarding hop. The
  census reproduces all 21 verified additions and all 5 removals from the image alone: **267** over
  297 transfer sites (291 resolved), and the §4 shares above are restated over the new 232 EXACT
  handlers.
- ~~**That the 11 upper-bound handlers answer the ids their bound spans.** They are excluded from
  every count; their `ids` column in the TSV is a ceiling.~~ *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 10, W1):
  no upper-bound row remains. Peers resolved every arm table, so every such row is now `exact`.*
- ~~**That the 24 unparsed handlers answer nothing.** They are unreadable by this tool, which is a
  different statement, and the TSV says which of the two reasons applies to each.~~ *Corrected 2026-09-30
  (SWE2-CONTRACT, DD batch 10, W1–W3): three unparsed rows remain, and all three are read. `005C5230` is
  `xor eax, eax` / `ret` and answers nothing. `0017CDE0` is a jump to it. `002985C0` is a jump to `003EE420`, whose id
  chain answers **1, 2 and 4** and sends every other id to `005C5230`. They stay `unparsed` in the TSV only because
  none of the three has a dispatch of its own.*
- **Anything about ordering.** Nothing here establishes when a message is sent, only who answers it.
  *Pointer 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17): §9 reads when each lifecycle message is sent, and `DL-3`
  (answered 2026-09-13, at the end of §9) settles 15 before 18: the order is not guaranteed. Check P6.*

## 8. Who sends the messages — 2026-09-08

`widget_messages.py --senders` scans for the two shapes a message record can take:

```asm
mov  dword ptr [rsp+0x20], 1      ; built on the stack
lea  rdx, [rsp+0x20]
call rax                          ; rax = [obj], the handler

lea  rdx, [rip + …]               ; a CONSTANT record in .rdata: 00915070 = {18,0,0}
call rax
```

**163 send sites, 49 distinct ids.** Far fewer sites than the 267 handlers, because most delivery
goes through **broadcast helpers** — one site can reach every node in a subtree.

> ### A zero that could not be true
>
> A stack-only version of this scan found **zero senders for id 18** — a message **65.4 % of all
> handlers answer**. "Nobody sends it" was never a possible answer, so the zero meant the instrument
> was wrong, not the protocol. The missing shape is the static `.rdata` record, the same one the
> draw pass already used. **This is the fourth zero in this database that meant "wrong query".**

### The framework / application boundary

Splitting senders by where they live — the widget core is `00244000`–`00249000`, holding the
constructor, teardown, the traversal and the setters:

| origin | ids |
|---|---|
| **framework only** | 3, 5, 8, 9, 17, 18, 19, 24, 25 |
| **both** | 1, 2, 4, 12, 14, 15, 20, 23 |
| **application only** | 0, 10, 13, 16, 26, 29–53, 61, 92, 95, 114, 119, 192, 285–289 |

> **No id above 25 has a sender inside the widget core.** The low ids are the framework's own
> protocol; everything above is defined by the game code that uses it. Id **16** is the most widely
> sent application message — ~~**20 sites in 20 distinct functions**, all of them outside the core,
> clustered in `0037xxxx`–`003Cxxxx`.~~
>
> *Corrected 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17, checks C1–C5):* the same census, re-run, still finds
> 163 sites and 49 ids, and 20 sites of id 16 in 20 functions. But three of those are the framework's own
> batch-completion senders `00249410`, `002494F0` and `002495C0` (§9, *Resource-ready*). They lie just above the
> scan's core band end `00249000`, so the scan counted them as application code. That is also why the table puts 16
> under "application only": with the batch pool in the framework, 16 is a "both" id. **The application senders are
> 17, in 17 functions**, and 16 is still the most widely sent application id (the next is 32, with 11 sites). They
> are spread over `002Axxxx`–`002Bxxxx` (3), `0037xxxx` (5), `003Bxxxx`–`003Cxxxx` (3) and `0055xxxx`–`0057xxxx` (6).

## 9. The lifecycle, end to end

Four ids were named here first, and they are the four most universal ones; a fifth, **24**, joined them on
2026-09-13 from ASTRA's teardown reading ([spawn page §18](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)). **None was guessed; each was read
from the function that sends it.**

| id | share of handlers | sent by | meaning |
|---:|---:|---|---|
| **1** | **97.6 %** | `002465F0` at `00246748` | **construct** |
| **2** | 58.3 % | `00248030` | **generation reconcile** |
| **15** | 27.5 % | `00244F00` at `00244F34` | **about to be destroyed** — self only |
| **18** | **65.4 %** | `00245020`, then `002473B0` recursively | **being destroyed** — self and whole subtree |
| **24** | 2.4 % | `002482E0` at `002483B2` | **released** — the last message before the handler slot is cleared and the storage is freed |
| **6** / **7** | | `002473F0` at `0024744E` | **enabled** / **disabled** — bit 0 changed, subtree visited (2026-09-13). *Corrected 2026-09-20:* **one builder, not two.** `002473F0` computes the id branchlessly — `neg eax` / `sbb ecx, ecx` / `add ecx, 7` — so it sends 6 when its boolean argument is non-zero and 7 when it is zero; `00247490` takes the **record pointer** in `r8` and forwards the record it is handed to the subtree |
| **16** | 16.1 % | `00249410`, `002494F0`, `002495C0` | **resource batch complete** — the framework sender; ~~20 application senders not read~~ 17 application senders, read at the census level (*Corrected 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17): receivers and payloads in the batch-17 section at the end, C2–C5*) (added 2026-09-13) |
| **19** / **20** | 11.4 % / 6.2 % | `00246C20` at `00247039` / `0024706B` | **transition finished** forward (state 3) / backward (state 1) (added 2026-09-13) |
| **25** | | `00246C20` at `00246C51` | **animation step** — first act of each completion visit to an enabled widget (added 2026-09-13) |
| **17** / **22** | | `00246C20` at `00246D9F` / `00246DB7` | **position tween finished** / **position tween stepped** — channel 0; 17 exactly when the eased value reaches `1.0` (§9a, added 2026-09-20) |
| **21** | | `00246C20` at `00246EF8` | **extent tween stepped** — channel 1, every frame the channel runs; no separate finished id (§9a, added 2026-09-20) |
| **23** | | `00246C20` at `00246F9D` | **scalar tween stepped** — channel 2, every frame; the engine applies the value to no property, so the handler must (§9a, added 2026-09-20) |
| **8** / **9** | | `00244830` at `002448AD` / `0024487E` | **focus gained** / **focus lost** — the focus switch sets and clears `+0x40` bit 4 and moves `0208EBC0`; 8 carries a flag (§9c, added 2026-09-20) |
| **53** | | `00279E20` at `0027A0C0` | **destroy request** — "tear yourself down"; both receivers answer it by calling the destroy entry `00244F00` (§9e, added 2026-09-20) |

### 1 — construct

The constructor builds the record on its own stack and calls the handler as its last act:

```asm
0024660A  mov    dword ptr [rsp + 0x20], 1     ; id = 1
00246615  xorps  xmm0, xmm0
00246620  movdqu xmmword ptr [rsp + 0x28], xmm0 ; the other 16 bytes = 0
…
00246730  mov    eax, dword ptr [rsi + 0x10]   ; …except msg->b, from the caller's 4th argument
00246740  lea    rdx, [rsp + 0x20]
00246748  call   rax                           ; rax = the handler at object +0x00
```

**So `msg->b` on message 1 is the caller's `locals` argument** — the one datum a widget gets at birth
that its constructor did not compute.

### 2 — generation reconcile

> **Corrected 2026-09-13 (FABLE, on `ASTRA-CONTRA-FABLE-WIDGET-GENERATION`, re-read from the image).** This said
> `00248030` sends `{2,0,0}` to nodes whose bit 18 is **set** and then **clears** bit 17. Both are wrong: bit 18
> **suppresses** message 2, bit 17 is **re-stamped** with the current parity, and a stale node with bit 10 is
> **released** instead of messaged — a branch the page had not read.
>
> *Pointer 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17): the branch is read in the first bullet below, and §2a's
> replay of the original bytes observes it (case "bit 18": `C` is released, not messaged or stamped). Check P6.*

`00248030` (`HierarchyGenerationBitTraversalAndCallbackReconciliation`, 339 B) walks one root's tree. For each node
whose `+0x40` **bit 17** differs from the parity global `0208ED5C` (`00248073`–`00248080`):

- **bit 10 set** — a widget kept by teardown (below) — it caches the next sibling `+0x20` and the parent `+0x10`,
  **releases the node through `002482E0`** (`0024808C`–`00248097`), re-reads the parity, and continues at the cached
  sibling if that is stale, otherwise at the cached parent (`0024809C`–`002480D6`);
- **bit 10 clear** — it sets bit 2, and **only when bit 18 is clear** and a handler exists sends `{2,0,0}` (record
  `00915108`; `002480DB`–`002480F9`: `bt ecx, 0x12` / `jb` skips the call); then it **re-stamps bit 17 from the
  parity as it is after the callback** (`002480FB`–`00248110`).

A node whose bit 17 already matches is not handled, but its first child is still examined. **The walk is steered by
the stamps, not a full depth-first traversal** (`00248113`–`0024815C`): descend into a stale first child, else step
to a stale next sibling, else ascend to the parent — so a current sibling ends that sibling list's walk — and stop on
returning to the start node. Each node entered also gets its `+0xB4` (`halfRatePhase`) zeroed or incremented by
`001EDDA0()`.

**Where the parity changes.** The per-frame UI pass `00250540` (from `MainLoop_UpdateAndRenderFrame`, `0022BA45`)
flips it with `002481A0` (`0208ED5C ^= 1`, phase `0208F560 = 1`), runs `00248030` on each of the roots
`0208EA20`/`0208EA28`/`0208EA30` that has a first child (`0025061C`–`00250647`) and on `0208EA40` and `0208EA48`,
clears the phase (`00248190`), sends the focus notice (`002481C0`: up the chain from the focus top `0208EBC0` while
each node has bits 0 and 3, **11** ~~at the first with bit 9~~ **to the focus top** when a node on the way has bit 9, and **10** to the focus top if the root is
reached without one; *receiver corrected 2026-09-25, FABLE, Claude Opus 5.5: both tail-jump through the focus top's
own handler, `002481EC`–`0024820D`*), and only then
runs the completion pass over the roots (`00250675`–`0025068C`). **So a widget reached by the walk is stale once per
frame and receives 2 then, unless bit 18 is set.**

**The constructor seeds that same bit from that same global** — `002465F0` does
`eax = [0208ED5C]; shl ecx,0x11; xor [rdi+0x40] …`, which the widget-constructor document already
records as *"bit `0x20000` from a global"*. `0x20000` is bit 17. **Two documents, written for
different reasons, anchor the same bit to the same global.**

### 2a. Message 2 replayed from the original bytes, and the input swallow it drives every frame, paused or not — 2026-09-24 (FABLE, Claude Opus 5.5)

**Why this was re-run.** A pending answer to the input contract's `GG-3` described `00248030` in three
ways that contradict the section above. It said `bt [rbx+0x40], 0x12` *gates* the call, that the
following `and` *clears the latch*, and that the record is `00915058`. The static reading above had
already been corrected once (2026-09-13), so this time the walker was **executed** rather than
re-read.

**Method: original-code replay, bounded.**
[`members/generation_walker_replay.py`](members/generation_walker_replay.py) maps the shipping image at
its virtual addresses and runs the **unmodified** body of `00248030` (339 B, sha256 `5054f7ff…`). It
also runs its one callee `001EDDA0` for real, over planted trees. Every node's `obj+0` handler is an
**observation stub**: a lone `ret` whose entry records `rcx` and the 24-byte record at `rdx`. The
release call `002482E0` is stubbed the same way: it records the node and does **not** unlink it. The
parity global is 1 and every planted bit 17 is 0, so every node starts stale. Result:
[`generation_walker_replay.json`](members/generation_walker_replay.json).

| case | planted tree | observed from the original bytes |
|---|---|---|
| bit 18 | `R` → `A` (bit 18), `B`, `C` (bit 10) | message 2 to **`R` and `B` only**, each with record **`00915108` = `{2,0,0}`**. `A` gets **no call** but still has bit 2 set and bit 17 stamped. `C` is **released**, not messaged or stamped. |
| current tree | the same tree, with bit 17 already equal to the parity | **no call**. `R` is entered, and no child is visited. |
| subtrees | `A` (bit 18) has child `A1`, `C` (bit 10) has child `C1` | message 2 to **`R` and `A1`**. **A set bit 18 does not prune the subtree.** `C1` is never entered after `C`'s release. |
| handler flips parity | `B`'s handler flips `0208ED5C` inside its callback | `B`'s bit 17 takes the **new** parity (0); `R` and `A` keep the old one (1). The stamp reads the global **after** the callback (`002480FB`). |

**Controls.** Every case asserts its expected result. Two byte mutants of the walker must fail those
assertions, and both do (the JSON's `verdict` fields):
- `002480E5 jb → jae` inverts the polarity: only `A` is messaged.
- Nopping the reload at `002480FB` leaves the stamp to whatever the callee left in `edx`, and the
  planted stamps no longer come out.

A second run writes byte-identical JSON.

**So the transition above stands, with two refinements that are new.**
1. **Bit 18 mutes the node, not its branch.** The walk still descends into a suppressed node's
   children, and they receive message 2.
2. **The walker never writes bit 18.** Its value on exit equals its planted value in every case.
   The `and dword [rbx+0x40], 0xFFFDFFFF` at `00248101` is bit **17**. The next three instructions
   (`00248108`–`00248110`) re-stamp it from the parity.

Also, `00915058` is `{15,0,0}`, the destroy notice of §15/18 below, not message 2.

**Where message 2 meets the input subsystem.** The contract's I-5 swallow lives in the message-2 arm
of `002284F0`, the handler of the singleton widget `01FD4948`. That widget is created lazily by
`00228490` (`002284C0`–`002284D2`), whose only caller is `00228380`. The arbiter
`InputGameplay_ArbitrateDigitalInputAndModalState` reaches `00228380` at `00253CC3`. Its route into
the walk is static and short:
- **Message 1** (sent by the constructor as its last act, §1) runs `00248030` on `[0208EA40]`. Then,
  if the widget has no parent, it attaches itself as the **last child of the root `[0208EA48]`**:
  `0022867A`–`00228684` → `00244960` → `00248220`, which appends at the end of the sibling chain.
- **`00250540` walks `[0208EA48]` in both of its arms.** While the pause getter `0017E4E0` is
  non-zero, that root is the **only** one walked (`0025058D`–`00250599`). Otherwise it is walked
  after the other roots (`0025065C`). The mode-5 drain `002508E0` walks it too (`0025090F`).

**So the singleton receives message 2 once per walked frame, paused or not, unless its bit 18 is
set.** Every frame on that path the I-5 test runs: if the `+0x308` record of `0209AC30` is present
and the history mask (`0035EF10(0,0)`) equals the configured cancel word `01E0C2A4`, the arm zeroes
`02F97360`–`02F97398`.

**What the arm does around the swallow** (read, not executed):
- **Swallow.** The arm sets its state `+0xC0 = 1`. When `001EC5A0()` agrees, it sets bit 0 on the
  widget in slot 3 of `0215F200` (`002E2570(3, 1)`; message 1 clears the same bit with
  `002E2570(3, 0)`).
- **Next message 2.** On the next message 2, state 1 takes `00228599`–`002285C2`: `0017E500(0)`,
  `00244DD0` on `[01FD4940]` when present, `00245020(self)` (the teardown of §15/18), then state 3.
- **Message 10.** Message 10 (the focus notice `002481C0` sends, §9) arms the same state-1 path when
  cancel is held, without zeroing the snapshot.
- **Message 18.** Message 18 clears `01FD4948`, so `00228380` rebuilds the widget the next time it
  runs.

**Taken together: holding cancel wipes that frame's published input and schedules this widget's own
teardown one walk later.**

**Not established here.**
- ~~Which game screen this widget is. Its only creator is a capability-gated step on the arbiter's path
  that tail-jumps into the pause-menu registrar `002282F0`, but no string names it.~~ **Answered
  2026-09-25 (FABLE, Claude Opus 5.5): it is the pause menu's cancel-to-close guard.** `[01FD4940]`
  is the pause menu itself. `002282F0` creates it (`00228352`) as a `0xD0` widget whose handler is
  `00229590`, the body whose own debug strings read `"PauseMenu Create\n"` / `"PauseMenu Open\n"`.
  That handler also writes `01FD4940` (`002295F9`) and arms a **5-frame** reopen cooldown
  `01FD46FC = 5` (`002295EF`). Every arbiter pass, `00228380`:
  - creates this guard when absent;
  - counts the cooldown down while no pause menu exists (`00228405`);
  - opens the pause menu through `002282F0` when the cooldown reaches zero, if the capability-bit-21
    test allows.

  The guard's message-2 arm is therefore **"Cancel closes the pause menu"**. Cancel held while the
  `0209AC30` object's `+0x308` record exists wipes the frame's published input and sets state 1.
  The next walk's message 2 sees state 1 and closes the pause menu (`002285A9`–`002285B5`,
  `00244DD0([01FD4940])`), then tears the guard down (`00245020`). Because the guard sits on the one
  root walked while paused, this works **during** the pause, which is when it is needed. Static; not
  observed live.
- Which snapshot readers run after the walk in the same frame. That order is ASTRA's open request
  `FABLE-REQ-ASTRA-WHERE-THE-SNAPSHOT-READERS-SIT-RELATIVE-TO-THE-ARBITER`.
  *Pointer 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17): FABLE's static pass is done
  ([`fable-astra-live-facts-0930`](../../_index/candidates/fable-astra-live-facts-0930/README.md), `snap_order.py`).
  It places the four readers that have a direct-call path to a frame body. For the readers reached only through widget
  procedures and vtables, the order is run-time object state, so the request stays a runtime item under its own id.
  Check P5.*
- Anything live. The replay is one function over a synthetic tree, with an observer in place of a
  real handler. It is not a running input-widget test.

### 15 then 18 — destruction is two phases

```c
void Widget_Destroy(Widget *self)              /* 00244F00, 68 B */
{
    if (!self) return;
    self->flags40 |= 0x40;
    if ((self->flags40 & 0x21) == 0x21) return Sub_244DD0(self);   /* deferred path */
    if (self->handler) self->handler(self, &MSG_15);   /* 00915058 = {15,0,0} — SELF ONLY */
    Widget_Teardown(self);                             /* 00245020 */
}
```

`00245020` first runs the focus-removal helpers `002448D0` and `00244700(self, 1)`, then sends `{18,0,0}` (record
`00915070`) **to itself and to every descendant**, through the recursive broadcast at `002473B0` — it does *not* detach
the object; that happens later in `002482E0` (corrected 2026-09-13):

```asm
002473B6  mov  rax, [rcx]          ; the node's handler
002473B9  mov  rbx, [rcx + 0x18]   ; first child
002473C2  lea  rdx, [rip + …]      ; -> 00915070 = {18,0,0}
002473C9  call rax
002473D0  mov  rcx, rbx / call 002473b0    ; recurse into the child
002473D8  mov  rbx, [rbx + 0x20]           ; next sibling
```

**Both walkers save the first child (`+0x18`) before calling the node's handler, and read each child's next sibling
(`+0x20`) only after that child's recursion returns** (`00245047`–`00245069`, `002473B9`–`002473D8`) — so with a stable
tree the order is parent before descendants, but a handler that relinks or frees nodes during message 18 changes what
is visited; neither walker snapshots the subtree.

**Then the release, which runs the other way round (2026-09-13).** After the broadcast `00245020` re-reads `+0x40`
bit 5 (`00245072`): **set** → `002473F0(self, 0)`, clear bit 1, set bit 10, and the object is **kept**; **clear** →
tail-call `002482E0` (302 B), which

1. cleans the **children first**, saving each next sibling before recursing;
2. unlinks self from parent and siblings and decrements the parent's child count, releasing resources reached
   through `+0x60` when present;
3. sends **`{24,0,0}`** (record `00915040`) to its own handler (`002483B2`);
4. clears `+0x40` bit 10 and the low nibble of `+0x7C`, calls `00228450`, saves the pointer at **`+0x08`**, and nulls
   the handler slot `+0x00` (`002483B4`–`002483CE`);
5. releases the storage — `+0x40` bit 14 clear → `003697F0` (heap); set → clear bit 14 and byte `+0xA2` (pool) —
   and **tail-jumps to the saved `+0x08`** if it is non-null (`002483F8`–`00248405`). No argument is set up for that
   jump, and on the heap path `rcx` has been through `003697F0`, so this is not an ordinary `callback(self)`.

So **notification is parent-first and release is child-first**, with message 24 as each node's last word.

### Kept, then reclaimed — why rooted widgets are not freed at teardown (2026-09-13)

*Added by FABLE on `ASTRA-CONTRA-FABLE-WIDGET-ROOTS` and `ASTRA-REQ-FABLE-WIDGET-RETENTION` ([spawn page
§19–§21](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)), every address re-read from the image.*

**The roots are real objects.** `00247AE0` (1348 B, called from `00253970`) allocates the `0x7E00`-byte pool
(`0208EA58`), then builds three `0xC8`-byte widgets with procedure `002445D0` in a register loop — `rdi = 0208EA20`
(`00247D20`), `mov [rdi], rbx` (`00247D9F`), `rdi += 8` (`00247DAC`), `ebp = 3` iterations (`00247CF2`) — so it
stores `0208EA20`, **`0208EA28`** and `0208EA30`, with 0, 1, 2 in the constructor locals `[rsp+0x58]`; a fourth root
goes directly to `0208EA38` (`00247E11`). A scan for RIP-relative stores sees none of the loop's stores. **The widget
contract's §5 reading — `0208EA28` never written, NULL for the process — is contradicted**; that correction is its
owner's (`ASTRA-CONTRA-OPUS-WIDGET-ROOTS`). Whether initialisation completes with valid storage is not observed.

**The root procedure `002445D0`** sets `+0x40 |= 0x23` (bits 0, 1, 5) on message 1, stores the descriptor value at
`+0xC0`, and sets `+0x98 = 0`, `+0x9C = 0x200`, `+0x9E = 0x1C0` (from `01E0C1D8`/`01E0C1DC`); it returns 0 for every
message and handles no other.

**Attach passes bit 5 down.** `00248220(parent, child)` appends the child after the last sibling (`+0x20`/`+0x28`),
increments the parent's `+0x30`, sets `child+0x10 = parent`; if the parent has bit 5 it sets the child's and runs
`002463F0(grandchild, 002418E0, 1)` over each of the child's children — a pre-order visitor that sets bit 5 through
the subtree; if the parent has bit 0 and the child bit 1 it calls `002473F0(child, 1)`; and it sets the parent's
bit 13 (resort). `00244960(root, w)` attaches only when `w+0x10` is null. **`00247950(w, flag)` is an attach, not a
close:** it loads `*(0208EA28)` itself and, for a parentless `w`, replaces bit 1 with `flag & 1` and tail-calls
`00248220` (`0024795C`–`00247975`); a parented `w` goes to `00247870`. Neither path reaches teardown.

**So a widget attached under a root carries bit 5, and teardown keeps it.** After message 18, `00245020` takes the
bit-5 branch — `002473F0(self, 0)`, clear bit 1, set bit 10 — and does not call `002482E0`. **The storage is released
by the next reconcile that reaches the node stale**, through `00248030`'s bit-10 branch, and message 24 is sent then.
Because `00250540` flips the parity every frame and runs completion (which is where a deferred destroy's teardown
happens) after that frame's reconcile, that is normally the following frame; until then the node stays linked with
bit 10 set. Re-entrant callbacks and the stamp-steered walk can delay it; no frame guarantee is claimed.

**Enable notices — messages 6 and 7.** `002473F0(w, on)` and its recursive half `00247490`: a node with bit 1 set
whose bit 0 differs from `on` gets bit 0 = `on` and a message whose id is **6 when `on` is nonzero, 7 when zero**
(`0024740C`–`0024741B`: `neg` / `sbb` / `add 7`), then its children are visited with the same record; **a node that
fails the gate is not notified and its descendants are not visited** (`00247423`–`0024742F`, `002474AB`–`002474B7`).

### Completion — 25, then 19 or 20, and the deferred 18 (2026-09-13)

`00244980` (the completion pass; `00244970` is its five-byte thunk) visits a node. With bit 0 set it resorts the
children when bit 13 is set (`002479B0`, then clears bit 13), then calls `00246C20`; a nonzero return with the
**re-read** `+0x7C` low nibble equal to 1 ends the visit — bit 6 → tail-call `00245020`; else bit 5 →
`002473F0(self, 0)`; bit 1 cleared — **without visiting the children**. Otherwise (bit 0 clear, or no completion) it
recurses into the children, reading each next sibling after the child returns (`002449F4`–`00244A0F`).

### 9a. The property animation is three channels over one union — 2026-09-20 (FABLE, Claude Opus 5)

*What "runs the property animation" below actually is, and where messages 17, 21, 22 and 23 come from — four of the
fourteen ids `DL-1` still listed as unnamed. Each is read from the sender, which is this page's standing rule.*
*(Pointer 2026-10-01, SWE2-STRUCT for OPUS, DD batch 17: "still listed as unnamed" is the 2026-09-20 count; `DL-1`
was answered for every id on 2026-09-25, §7. Check P8.)*

**At most one channel runs per call.** After `{25}`, `00246C20` loads `ecx = dword[+0x80]` (`00246C89`) and tests
bits 0, 1 and 2 as an **if / else-if chain** — `and eax,1 / je 00246DC3`, then `and eax,2 / je 00246F04`, then
`and eax,4 / je 00246FA9`. So the three channels are alternatives, not a set, and that is what lets them share
storage: **`+0x84`…`+0x8E` is a union**, read as `int16` pairs by channels 0 and 1 and as `f32` by channel 2.

**All three share the same clock.** Duration `dword[+0x90]`, start tick `dword[+0x94]`, the millisecond clock
`[0208F570]`; a start tick further ahead than `clock + duration` is snapped back to `clock` (the stale-start clamp,
e.g. `00246CB3`–`00246CC1`); the elapsed value is scaled by the rate `xmm7` — `1.0f`, or `float[+0xB8]` when
`00229DF0()` is non-zero and `00229EA0()` is 2 (`00246C58`–`00246C7D`) — and handed with the curve kind
`(dword[+0x80] >> 10) & 0xF` to `00248F40`, which returns the eased fraction. *The curve kind comes from the widget's
own `+0x80`, not from the transition record* — the constructor page's `UQ-187` note says the same thing.

| channel | bit of `+0x80` | union view | what it writes | message |
|---|---|---|---|---|
| 0 | bit 0 | `i16 startX +0x84`, `i16 startY +0x86`, `i16 dX +0x8C`, `i16 dY +0x8E` | **position** `word[+0x98]`, `word[+0x9A]` | **17** on finish, **22** otherwise |
| 1 | bit 1 | `i16 +0x84`/`+0x86` anchor, `i16 startW +0x88`, `i16 startH +0x8A`, `i16 dW +0x8C`, `i16 dH +0x8E` | **extent** `word[+0x9C]`, `word[+0x9E]`, and `+0x98`/`+0x9A` when `+0x80` bits 8 / 9 are set | **21**, every frame |
| 2 | bit 2 | `f32 start +0x84`, `f32 delta +0x88`, `f32 current +0x8C` | `float[+0x8C]` only | **23**, every frame |

**Channel 0 — position, and the only one with a finished message.** The interpolating path multiplies each delta by
the eased value and adds the start (`00246D02`–`00246D59`); the snap path, taken when the eased value is exactly
`1.0` *or* the elapsed value has reached the duration, writes `start + delta` outright (`00246D5B`–`00246D7E`). Both
converge on `00246D7E ucomiss xmm6, xmm2`: **equal to `1.0` → clear bit 0 and send `{17}`** (record `00915138`,
`{17, 1}`); **otherwise send `{22}`** (record `00915150`). So 17 is a genuine completion notice and 22 is the
per-frame one, and the pair is what makes channel 0 different from the other two.

**An asymmetry worth a reimplementation's attention.** Channels 1 and 2 clear their bit on the **snap path**, which the
elapsed-versus-duration test reaches on its own (`00246EA0`, `00246F7E`), so they always terminate. Channel 0 clears
bit 0 **only on exact equality with `1.0`** (`00246D8C`, reached only through the `ucomiss` at `00246D7E`). A curve
mode that ran past its duration without returning exactly `1.0` would leave channel 0 writing the same end position
and re-sending `{22}` every frame forever. *Whether any of the sixteen curve kinds does that was not read* —
`00248F40` is not read here — so this is a shape in the control flow, not an observed hang.

> *Answered 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17, checks E1–E4): **no curve kind can do it.**
> `00248F40(kind, duration, elapsed)` tests `duration <= elapsed` first (`00248F44 cmp edx, r8d` / `jg`, signed) and
> then returns the constant `01CEBBA8`, which is exactly `1.0f`. It does this before it reads the kind: the first use
> of `ecx` is `00248F6A`. So once the duration is reached, every kind returns exactly `1.0`. (Kinds 1–5 have their
> own arms, and every other kind returns the linear `elapsed / duration`.) The snap test in `00246C20` compares the
> same two values (`00246CFA cmp dword [rbx+0x90], edi` / `jbe`), but **unsigned**. The two tests can disagree only
> when the scaled elapsed `edi` reads negative as a signed number. The rate cannot cause that: it is `1.0f`, or
> `1.0f / 00229E70()`, and `00229E70` replaces a value at or below zero with `1.0`. So it takes a scaled elapsed of
> 2^31 ticks or more, where `cvttss2si` returns `0x80000000`. Elapsed is `clock − start` in 32 bits, so that happens
> either when the start tick sits less than one duration ahead of the clock (it wraps, and clears once the clock
> passes the start), or when the first frame that runs the channel comes 2^31 scaled ticks or more after its start
> (about 24.8 days at rate 1.0). A frame that runs earlier ends the tween normally, because both tests agree below
> 2^31. Neither case depends on the curve kind. Whether either ever happens in play is run-time state; the static
> reading gives the curve kind no way to cause it.*

**Channel 1 — extent, with an anchor.** It computes `dW = round(dX × t) + startW` and `dH = round(dY × t) + startH`
(`00246E2E`–`00246E7E`), or the exact sums on the snap path, which also clears bit 1 (`00246EA0`). Then it re-reads
`+0x80`: **bit 8** → `word[+0x98] = word[+0x84] − dW`, **bit 9** → `word[+0x9A] = word[+0x86] − dH`, before storing
`+0x9C = dW` and `+0x9E = dH` (`00246EA7`–`00246EE8`). That is a widget growing from its far edge rather than its
origin — the position is moved back by exactly the amount the extent grew. **Both paths send `{21}`**: the running
path jumps past the bit-clear straight to the write-back (`00246E7E jmp 0x246EA7`), so there is no separate
finished id for this channel.

**Channel 2 — a float the engine does not apply.** `float[+0x8C] = float[+0x88] × t + float[+0x84]`
(`00246F6C`–`00246F90`), clearing bit 2 on the snap path (`00246F7E`), and **`{23}` either way**. Nothing in this
body reads `+0x8C` back or writes the value into a widget property. That is the reason 21 and 23 are sent every
frame while 17/22 distinguish: **for channels 1 and 2 the per-frame message is the only way the value reaches
anything**, so the handler is the applier.

**Corroboration from the other end, not from this body.** The starter `002468A0` (read by SWE2-EC7 on the object
contract, 2026-09-18) sets `+0x80 |= 1`, writes the deltas into `word[+0x84]`/`[+0x86]`/`[+0x8C]`/`[+0x8E]`, takes
`+0x94` from `[0208F570]` and `+0xB8` as the rate — and it decides whether to animate at all by comparing its target
against `word[+0x98]` / `word[+0x9A]`. An independent reading of the *start* of channel 0 that names the same fields
and the same destination. The root initialiser `002445D0` writes `+0x9C`/`+0x9E` as `0x200`/`0x1C0` — 512×448, the
screen — which is what fixes `+0x9C`/`+0x9E` as an extent rather than a second position.

**What this does not claim.** What the channel-2 float *is* (opacity and scale are both plausible and neither is
read here); the meaning of the `{17, 1}` and `{23, 1}` records' second dword, which is `1` for those two and `0` for
21, 22 and 25 and which no receiving arm was read for; and any receiving-side corroboration at all — all four
namings rest on the sender, as 14's does.

### 9f. Message 29 is a self-sent "state changed" — 2026-09-20 (FABLE, Claude Opus 5)

**Five independent senders, one shape.** Each writes fields of an object and then, as the last act of that write,
sends `{29}` with a **zeroed argument record** to **that same object**:

| sender | what it writes first | the send |
|---|---|---|
| `00276650` (the `ManagerSub0209BE80_AB30` builder) | `+0x61B0`, `+0x61B8`, `+0x61CC` | `00276737`–`00276752`, its final act before the cookie check |
| `002B7B80` | `+0xD2`, `+0x12A`, `+0xBBDA` | `002B7EF1`–`002B7F09` |
| `002BAF80` | `+0x12A`, `+0xBBDA` | `002BB334`–`002BB34F` |
| `002BC3E0` | `+0xD4`, `+0xD8` | `002BC4B9`–`002BC4DE` |
| `002B6DB0` | ~~(same band, not read whole)~~ `+0xD0` / `+0xD2` (the `+0xC0` child's metric pair from `00403600`, default `0x100` each), `+0xD4` = 100, then the viewport reconcile `002B7210`, then `+0xD8` = `0x100`; this is its id-14 arm *(Corrected 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17), S1–S4; see below the table)* | `002B6E99`–`002B6EA1` |

*Read 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17, S1–S4): `002B6DB0` is a **base procedure**, not a separate
object.* It dispatches on the message id (ids 1, 2, 3, 10, 14, 15, 29, 36, 39), it is not a row of the handler table,
and its only caller is the track map page's procedure `002B7B80`.
[The map screens](../Map-Screens/the-map-screens-and-their-shared-map-data.md) page already calls `002B6DB0` "the
page's command dispatcher". That procedure hands it its own `self` and
message at three sites, its default arm included (`002B8E27`). So the `{29}` it sends to `[self]` goes to `002B7B80`,
whose table sends 29 to that default, and so back into `002B6DB0`'s own id-29 arm (`002B6EAA`). That arm rebuilds the
24-pixel cell rectangle at `+0xF8` from the extent `+0x9C` / `+0x9E` and the pair `+0xD0` / `+0xD2` (through
`002B6950`), and clamps the cursor `+0xC8` / `+0xCC` into it. *This is a receiving side for 29, and it re-reads the
fields the send followed, which is what "re-read them" below predicts.*

In every one the receiver is the sender's own object (`mov rcx, rsi` / `rbx` / `r14`, the register the writes went
through) and the record's three argument words are cleared with the same `xorps xmm0, xmm0` / `movdqu` pair. **So 29
is an invalidation: "I have changed your fields, re-read them."** That is what lets a *builder* and a *mutator* send
the same id — `00276650` finishes construction with it, the `002B…` bodies finish a geometry change with it — and it
is why the record carries nothing: the receiver is expected to look at the object, not at the message.

*Note that this is a second, later notice than message 1.* The widget constructor `002465F0` has already sent `{1}`
by the time `00276650` sends `{29}`; construct says "you exist", 29 says "the fields are now set".

**Message 30 is narrowed, not named — its senders do not agree.** Of its three, `0029A0A0` sends it to **another
object** (`qword[rbp + 0x120]`, a delegate) and **consumes the return** (`0029A19C call rax` / `test eax, eax` /
`je`), while `002778C0` sends a **16-byte constant argument block** (`movdqa xmm0, [00915BC0]`, first dword 2) to
`rsi`, immediately after a `{31}` carrying a pointer. A query with a gating answer and a constant-payload
notification are not the same message used twice; until one of the two shapes is read through to its receiver, 30
gets no name.
*(Pointer 2026-10-01, SWE2-STRUCT for OPUS, DD batch 17: 30 was dispositioned on 2026-09-25 as an application-defined
id, each screen family defining its payload and answer, §10. Check P6.)*

**Message 11 has no sender either instrument can see.** Neither the `.rdata`-record scan nor the stack-immediate scan
finds one anywhere in the UI band — the static scan's only hits are at `00D9B184` and `00E1F634`, in `0071CE10` and
`0078C730`, far outside it and data that merely begins with an `11`. Its two `exact` receivers (`0023BD40`,
`0023CE10`) are real, so a sender exists; it writes the id **from a register**, which is the blind spot both scans
declare. That is a specific next instrument, not a mystery.
*(Pointer 2026-10-01, SWE2-STRUCT for OPUS, DD batch 17: the sender was found on 2026-09-25. It is the focus notice
`002481C0`, which reaches the handler by a tail `jmp` with the `.rdata` record `{11}`, §10. Check P6.)*

### 9e. Message 53 is a destroy request — 2026-09-20 (FABLE, Claude Opus 5)

*Named from the sender and from **both** receivers, which is one more corroboration than any other id on this page
has had.*

**The sender.** `00279E20`, the handler of `ManagerSub0209BE80_AB30`, has a one-shot arm gated on **bit 6 of
`dword[+0x61CC]`**, which it clears as it enters (`0027A060`–`0027A072`). It then walks **its two declared panels**,
`rbx + 0xC0 + i × 0x3010` for `i < 2`, and for each one that `00273A20` reports live (§9b) sends `{53, 0, 0, 0, 0}` to
that panel's handler (`0027A080`–`0027A0D0`). Immediately after the loop it does the same job *directly* to the object
at `rbx + 0x60E0`: `00273A20` first, then `00244F00` (`0027A0D2`–`0027A0E9`).

**Receiver one — the panel.** `00276D30` dispatches on `id − 1` against a `0x35`-wide table, so 53 is in range, and its
byte table gives it **jump slot 9, shared with no other id**. The arm is two instructions:

```asm
00277058  mov  rcx, rdi          ; self
0027705B  call 00244F00          ; the destroy entry - sends {15}, then the teardown
00277060  xor  eax, eax
```

**Receiver two — independently.** `0027AA70` (765 B, arms `1, 2, 12, 24, 53`) answers 53 at `0027AB9C` with
`lea rcx, [rdi + 0xC0]` / `call 00244F00` — the same destroy entry, applied to its own embedded child.

So **53 asks an object to tear itself down**, and it is categorically different from 15, 18 and 24, which *notify*
during a teardown that is already running. Routing it as a message rather than calling `00244F00` directly is what
lets the receiver choose — the panel destroys itself, `0027AA70` destroys a child instead — and the container's own
direct call on `+0x60E0` shows the difference deliberately: that object gets no say.

**A by-product worth recording, because a ruling of mine leans on it.** This arm is independent primary evidence for
the AB30 panel route: the handler's *own* loop is `+0xC0 + i × 0x3010` bounded at `i < 2`, and the very next thing it
touches is `+0x60E0` as a separate object — exactly the extent the
AB30/panel overlap ruling collapsed into one typed region row. That ruling cited the construction site
`0027A3F7`–`0027A42D`; this is a second, unrelated site in the same handler agreeing on the offset, the stride and
the count.

### 9c. Messages 8 and 9 are the focus switch — 2026-09-20 (FABLE, Claude Opus 5)

*The two largest ids `DL-1` had left — 8 on 23 handlers, 9 on 20 — read from one framework sender of 158 bytes.*

`00244830(outgoing, incoming, flag)` does three things and nothing else:

```asm
00244865  and   dword ptr [rcx + 0x40], 0xFFFFFFEF   ; outgoing: clear +0x40 bit 4
0024486C  mov   dword ptr [rsp + 0x20], 9            ; {9}
0024487E  call  rax                                  ; ... to the outgoing handler
00244887  mov   dword ptr [rsp + 0x20], 8            ; {8, flag != 0}
00244894  or    dword ptr [rbx + 0x40], 0x10         ; incoming: set +0x40 bit 4
002448AD  call  rax                                  ; ... to the incoming handler
002448AF  mov   qword ptr [rip + ...], rbx           ; 0208EBC0 = incoming
```

Either side may be null and is simply skipped. **`+0x40` bit 4 is "this widget holds the focus"**, held by at most
one widget, and `0208EBC0` is where that one is recorded. So **8 = focus gained** and **9 = focus lost**, and the
second dword of 8's record is `(flag != 0)` as a 0/1 — what the flag distinguishes is not read.

*Answered 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17, checks F1–F3): the flag says how the focus arrived.*
`00244830` has exactly two callers, the two named below. The pop `002448D0` passes **1** (`00244920`). It runs when
the focus holder is being torn down, and the incoming widget is the one under it on the stack, so `{8, 1}` means
*the focus has come back to you*. The push `002470D0` passes **0** (`0024711C`). It runs when a widget takes the focus
(`00244640` pushes it, and the old top is the outgoing side), so `{8, 0}` means *you have just taken the focus*. Like
the naming of 8 itself, this is read from the senders, the page's standing rule.

**The naming is corroborated by something written before it and not derived from it.** The object contract already
lists `0208EAC0` / `0208EBC0` / `0208EBC8` as **"the focus stack"**, and the spawn page already describes `002481C0`
as starting *"at focus `*(0208EBC0)`"*. This read arrives at the same place from the opposite direction — from the
messages rather than from the globals — and the two agree without either citing the other.

**The two callers are the pop and the push.** `002448D0`, which `00245020` runs *first* on every teardown, compares
the dying widget against `[0208EBC0]` and, when it matches, pops the stack (`0208EAC0` indexed by the depth at
`0208EBC8`, decremented at `0024490A`) and calls `00244830(dying, popped, 1)` — focus falls back to whatever held it
before. `002470D0` is the other caller and the only other reader of `0208EBC0` besides the getter `00244820` and the
walker `002481C0`. *So a widget cannot be destroyed while silently holding the focus*, which is the invariant the
ordering inside `00245020` exists to keep.

### 9d. Two more senders located, neither fully named — 2026-09-20 (FABLE, Claude Opus 5)

**Message 26 is a per-element query whose answer the layout uses.** Both senders — `002D2600` at `002D279E` and
`002D28E0` at `002D2B5C` — have the same shape: inside a loop bounded by `word[+0xE8]`, gated on **bit 17** of a
flags dword (`bt r15d, 0x11` / `test dword ptr [rsp+0x3C], 0x20000`), they build `{26, (i64)elementIndex}` and call
the handler — and then **take its return value** (`002D27A4 mov esi, eax`, `002D2B5E mov dword ptr [rsp+0x28], eax`).
When the bit is clear or the handler is null, a default is used instead (`002D27A8 mov esi, r12d`). A widget message
whose *return* is consumed is rare on this page, and it makes 26 a **query rather than a notification**. What the
returned value then selects is traced below; 26 is narrowed, not named.
*(Pointer 2026-10-01, SWE2-STRUCT for OPUS, DD batch 17: 26 was named on 2026-09-25 as a per-cell pre-draw hook,
§10, and its last two receivers were read in DD batch 10, W4. Check P6.)*

> **A RECEIVER, and it answers zero — 2026-09-21 (FABLE, Claude Opus 5).** Everything above is read from the two
> senders. `005651E0`'s `26` arm is the other half, and it does three things the sender side cannot show.
>
> **It treats payloadA as an element index into a list it owns.** `005653B7 mov rcx, qword ptr [rdx + 8]`, then
> `005653BE shl rbx, 5` / `005653C2 add rbx, qword ptr [rdi + 0xe0]` — the `0x20`-byte list that `00565720`
> rebuilds, described on
> [the shop table and its stock gates](../../12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md).
> It is gated on **bit 8** of the object's packed flags (`005653C9 test dword ptr [rdi + 0x180], 0x100`), and a
> clear bit takes the default exit.
>
> **It WRITES into the element it was asked about**, which a query is not obliged to do: a coordinate accumulated
> from `+0x9A` words of four objects — including the parent at `+0xC0` — lands as `byte[entry + 0x10]` (`1`, `2`,
> `3` or computed, at `005654E1`, `00565508`, `00565537`, `00565532`) with words at `+0x12` and `+0x14`; one
> branch writes `word[entry + 0x10] = 0xFC00` outright (`00565460`).
>
> **And it returns 0.** The exit loads `0056556D movsx eax, byte ptr [rbx + 0x11]` and
> `00565578 movzx edx, word ptr [rbx + 0x12]`, but those feed a write into the record at `[self + 0xD8]` —
> `00565581 mov word ptr [rcx + 0x114], ax`, `0056558A mov word ptr [rcx + 0x116], dx` — and the value actually
> returned is set three instructions later by `00565588 xor eax, eax`.
>
> ***So on this receiver the non-zero path above never runs***: the clip suspension raised under message 3 is not
> released by this element. *I had this arm written up as returning `byte[entry+0x11]`, because the exit opens by
> loading it; the `xor eax, eax` after the two stores is what decides. Reading the instruction one expects rather
> than the one that decides is how a sender-side claim gets inverted by a receiver-side note.*
>
> **Bound, and narrower than "one of six".** The handler table credits `26` to six rows, but **four of them
> forward it to the body above**: `005636F0`, `00563930`, `00563B10` and `00563D20` each send `0x1A` to the same
> arm as ids `4`, `8`–`12`, `18` and `286`, and that arm is a tail jump to `005651E0` — checked on all four
> rather than inferred from one. `005651E0` itself has no row. **So the receivers still unread are exactly two:
> `002D2DB0`, and `005691E0`**, which is the `289` receiver from the high-band family.

**Those two are now read, and the three receivers do three different things — 2026-09-21 (FABLE, Claude Opus 5).**

| receiver | where its elements live | what it answers |
|---|---|---|
| `005651E0` | a heap list at `[self + 0xE0]` | **always `0`** — it writes the layout triple into the element and publishes `byte[entry+0x11]` / `word[entry+0x12]` into `[self+0xD8] + 0x114`/`+0x116` |
| `005691E0` | an **inline** array at `self + (index + 0xB) * 0x20` — same `0x20` stride, no list pointer (`00568FF4`–`00568FFF`) | **passes `00568FE0`'s return through** |
| `002D2DB0` | none of its own | **delegates** to `[self + 0xC8]` and returns the delegate's answer |

**`005691E0`'s arm is four instructions** — `00569ED4 mov r8d, dword ptr [rdx + 8]`,
`00569EDA mov rdx, qword ptr [rdx + 0x10]`, `00569EDE call 00568FE0`, `00569EE3 jmp 00569EFC` — and the jump lands
on the shared epilogue **without** zeroing `eax`. *The contrast is visible inside its own jump table:* id `25`'s
arm at `00569EF7` calls the folded `005C5230` stub, which returns `0`, before falling into that same epilogue.

**`002D2DB0` reaches `26` by running subtraction, not a literal compare** — `sub 1`, `sub 1`, `sub 2`, `sub 1`,
then `002D2DFF cmp ecx, 0x15`, and `0x15 + 5 = 0x1A`. Its arm forwards the record intact through the delegate's
first slot (`002D2E21 mov rax, qword ptr [rcx]` / `002D2E29 call rax`) and jumps to `002D38CB`, **past** the
`002D38C9 xor eax, eax`, so the delegate's value survives. Both null checks — no delegate, or no slot — fall back
to `0`.

***So the non-zero consequence §9d describes can fire through two of the three and never through the first.*** A
message this page calls "a query rather than a notification" has **one receiver that answers, one that delegates
the answer, and one that declines by construction**.

> **One dead argument, checked rather than assumed.** `005691E0`'s arm loads payloadB as a pointer, which would
> imply a sender obligation `§9d` does not record — the senders build `{26, (i64)elementIndex}`. **It is dead:**
> `00568FE0` overwrites `rdx` at `0056903B` with `[rsi + 0xD8]` before reading it, nothing between entry and that
> store touches the incoming value, and the early-exit branch at `005691C8` is `xor eax, eax` / `ret`. So the arm
> loads a payload the callee discards. *`002D2DB0` passes the record through untouched, so it imposes nothing
> either.*
>
> **And the delegate is caller-supplied, which is why it cannot be named here.** `002D14E0` builds this widget
> — size `0x150`, handler `002D2DB0` at `002D14ED lea rdx, [rip + 0x18bc]` — creates **one** child of its own at
> `+0xC0` (size `0xC0`, handler `002D1420`), and then copies the delegate straight out of the construction
> descriptor: `002D16AC mov rax, qword ptr [rdi + 0x28]` / `002D16B0 mov qword ptr [rbx + 0xc8], rax`, beside
> `[rdi+8] → +0xD8` and `[rdi+0x20] → +0x120`. **`002D14E0` has six callers**, among them `0027AD70` and
> `0057C480` — both already cited on this page — so the object message `26` is forwarded to is **a different one
> per screen**, and a reimplementation has to carry the descriptor field rather than hard-code a target. *That
> `0057C480` is one of them is how this widget connects back to the shop-screen list machinery rather than being
> an unrelated body.* **The other four are deliberately not named here:** one of them reaches Audio, and importing
> a crossing into this page for a supporting detail is not worth the sentence it would cost.
>
> **And the pair is a grid origin, consumed by the sender in the same loop.** `+0x114`/`+0x116` are read by
> **both senders** immediately after they take the handler's return, and used as the **origin of a two-axis
> layout**: in `002D2600`, `002D27AB movsx ecx, word ptr [rbx + 0xea]` and `002D27BB imul ecx, eax` give
> `step × index`, then `002D27C6 add cx, word ptr [rbx + 0x114]` adds the origin and the result becomes one word
> of a local point; `002D27D6`/`002D27DD`/`002D27E0` do the same on the other axis with the step at `+0x100` and
> the origin at `+0x116`. `002D28E0` is instruction-for-instruction the same at `002D2B83`/`002D2B9D`. **So
> `point = step × index + origin`**, and *both* receivers write that origin — `005651E0` at `00565581`/`0056558A`,
> and the other through `00568FE0`.
>
> ***What is NOT established is the link.*** The receivers write the pair into the record at `[self + 0xD8]`; the
> senders read it off their own `self`. If those are the same object the loop closes, but **matching offsets are
> not identity** and nothing read here connects them — that is an ownership question rather than a semantic one,
> and it is the one thing still open on message `26`.
>
> *Answered 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17, checks L1–L9): **they are the same object, and the
> ownership is read from the build.*** Both receivers build their layout through `002432B0` with themselves as the
> owner (`00564010`, the four `00563xxx` rows' message-1 helper, and `005691E0` at `00569306` and the next two
> builds). `002432B0` passes the owner to the row builder `0029F930` (layout row kind 8), which creates the grid list
> through `002D14E0` with the owner as its `+0xC8` delegate. It stores the list at the row's `+0x18` and links it
> under the owner. Each receiver then copies that row's `+0x18` into its own `+0xD8` and sets the list's `+0xD8` to
> itself and the list's `+0x120` to its per-cell callback (`005640B7`–`005640E2`, `005693F6`–`00569416`). The
> senders run on that list: `002D1420`, the list's own draw child, passes its parent as `rbx`. A list sends 26 to its
> own handler `002D2DB0`, which hands it to the `+0xC8` delegate, that is, the receiver. The receiver writes
> `[self + 0xD8]` `+0x114` / `+0x116`, the list itself. The sender reads the origin back from its own `+0x114` /
> `+0x116`. The loop closes whenever the row the receiver copies is a kind-8 grid row, built by `0029F930`. Which row
> that is comes from the screen's layout data.

**What the answer selects — and an inference of mine that did not survive its own check.** The saved return is tested
at the bottom of each element's turn, and a non-zero answer runs `002D8BB0(x, 0)` before the flag is reset
(`002D285A`–`002D286D`; `002D2C97 cmp dword ptr [rsp+0x28], 0` / `je`, then `002D2CA5`, then `002D2CAC` clears it —
the two senders are instruction-for-instruction the same protocol). `002D8BB0(obj, mode)` is a **reference-counted
clip SUSPEND**: `mode 1` increments the byte counter `+0x5D` and, on the 0→1 edge, calls `00249FD0(0)`; `mode 0`
decrements it and, when it reaches zero, calls `00249FD0(obj + 0x48)` if `+0x5C` bit 17 is set and `00249FD0(0)`
otherwise. So the layout calls the **release** side once per element that answered non-zero.

> **Corrected within the day (FABLE).** *This paragraph first called `002D8BB0` a clip-rectangle **stack** with a push
> and a pop. The instructions above were right and the framing was backwards.* `00249FD0(rect)` does not simply
> "install" a rectangle: it builds an **enable flag** — `0` when the argument is null, and `0` again when all four
> words equal the stored default at `01E0C1D0` (the screen, `0x200` × `0x1C0`), otherwise `1` (`00249FD0`'s
> `cmove r10d, edi` chain at `0024A000`–`0024A031`) — and passes it as the fifth argument of `00184460`, which hands
> it on to the scissor pair `001B23E0` and `001E9F00`, the latter taking it as a **boolean** (`00184618 test ebx, ebx`
> / `setne bl`). So `00249FD0(0)` turns clipping **off**. The `0→1` edge therefore **suspends** clipping, and only the
> **last release restores** the object's own rect `+0x48` — and only when `+0x5C` bit 17 says it has one. The counter
> is a suspend depth, not a push depth, and a message-26 element answering non-zero **ends a suspension** rather than
> popping a clip it had pushed. *That also makes the unresolved half sharper rather than softer:* the decrement
> **underflows rather than guards** — `movsx eax, byte[+0x5D]` / `shl 8` / `dec` from a count of zero writes `0xFF`
> into the count and the `test eax, 0xFF00` / `jne` then returns — so an unmatched release does not merely do nothing,
> it leaves clipping suspended with a count of 255. Whatever raises the count for these elements is therefore
> load-bearing, and it is still not found.

**Found — it is in a different message, which is why no body balanced.** A census of **all 55** call sites of
`002D8BB0` (27 functions), reading the mode literal at each, splits them cleanly: **17 functions balance inside one
body**, one suspend against one release; ten do not; and exactly one is a **suspend with no release** — `0029A0A0`,
at `0029A2F8`. That site is the **last act of that handler's message-3 arm**, and its receiver is
**`widget + 0x38`**:

```asm
0029A1FB  mov  rdi, qword ptr [rbp + 0x38]     ; rbp = the widget (rcx at entry)
   ...                                         ; the arm's drawing work, through rdi
0029A2F0  mov  edx, 1
0029A2F5  mov  rcx, rdi
0029A2F8  call 002D8BB0                        ; suspend, then `jmp` to the return
```

**The layout pass reaches the identical object the identical way.** `002D1420`, the callback that runs the two
message-26 senders, does `002D14A5 mov rax, qword ptr [rcx + 0x38]` / `mov rcx, rax` and passes that as the senders'
**first argument** — which is the object the release is applied to (`002D2655` saves it; `002D285E` loads it back for
the `002D8BB0(x, 0)`). So the acquire and the release are the same field of the same widget, taken by two different
messages in two different bodies. **`+0x38` is the widget's drawing context**, and the clip suspension is raised
while that context is drawn under message 3 and lowered by whichever element answers message 26 non-zero.

*What is still not shown, and is not a static question:* that a given widget takes both messages, in that order,
within one frame. `0029A0A0` is one handler (arms `1, 2, 3, 4, 29`, registered by `0029BB40`), `002D1420` is taken by
address rather than called, and neither body fixes the other's instance. What the census does establish is that the
protocol is **cross-message by construction** — so the earlier finding that twelve of the thirteen message-26
handlers never touch `002D8BB0` was not evidence of a missing half, but of looking for it on the wrong side.

**The tidy reading would be that the handler pushes the clip while answering 26, and it is wrong.** Of the
**thirteen** handlers whose census row carries a 26 arm, **twelve never call `002D8BB0` at all**; only `00276D30`
does, and it makes both a push and a pop of its own. A release whose matching acquire is not in the sender and not in
twelve of the thirteen receivers is **not** a push/pop protocol between those two parties, so where the count is
raised is unresolved and 26 keeps its narrowed status. *Recorded because the inference was the obvious one and the
check that refuted it cost one census.*
*(Pointer 2026-10-01, SWE2-STRUCT for OPUS, DD batch 17: where the count is raised is answered in the paragraph headed
"Found" above: the message-3 arm of `0029A0A0` suspends at `0029A2F8` on the same `widget + 0x38`. 26 itself was
named on 2026-09-25, §10. Check P6.)*

**Message 53's sender is located.** `00279E20` at `0027A0B9` builds `{53, 0, 0, 0, 0}` and sends it to a different
object (`rdi`), but only after `00273A20` says the panel at `rbx + 0xC0 + i × 0x3010` is live (§9b) — the same two
panels the AB30 type declares. The receiver `rdi` is not resolved here, so 53 stays unnamed.
*(Pointer 2026-10-01, SWE2-STRUCT for OPUS, DD batch 17: §9e names 53 as a destroy request, from this sender and both
receivers, `00276D30` and `0027AA70`. Check P6.)*

### 9b. What `00273A20` decides — 2026-09-20 (FABLE, Claude Opus 5)

The nine-byte predicate that guards 81 call sites in the HUD and widget band — `xor eax,eax / cmp qword ptr [rcx], rax
/ setne al` — is already recorded elsewhere as "the null predicate". Joined to the two ends this page and the
constructor page already establish, it is more than that: it reads the **handler slot `+0x00`**, which the constructor
**never leaves null** (`0024662B`–`00246641`: a null handler argument is replaced by the folded `005C5230`) and which
**only the release clears** (`002483CE mov qword ptr [rdi], 0`, after message 24). So `00273A20(obj) == 1` means
exactly **"constructed and not yet released"** — a liveness latch, total on both ends, which is why the guarded-release
idiom is safe on embedded storage that has only ever been memset: such storage reads 0 and is skipped.

**The limit worth carrying:** it does **not** distinguish an active widget from one **kept** by teardown. A widget on
the bit-5 branch of `00245020` never reaches `002482E0`, so its `+0x00` still holds a handler and the latch still
answers 1 until the parity sweep reclaims it. A caller that needs "currently active" must test `+0x40`, not this.

`00246C20` first sends **`{25}`** (record `00915120`, `00246C4A`) to the handler, runs the property animation (§9a), then
reads the signed two-bit direction `+0x7C[5:4]`; zero returns 0. If the start tick `+0x74` lies beyond now
(`0208F570`) plus the duration it is reset to now (`00246FCD`–`00246FDD`); `now − start`, as an unsigned 32-bit value,
is scaled by the rate and truncated, and the animation completes when duration `+0x70` is not greater (signed,
`00246FFF`). Completion clears `+0x40` bit 9; a positive direction sets low state 3 and sends **`{19}`**, then clears
bit 15; a negative one sets state 1 and sends **`{20}`**, then clears bit 16; the direction bits are cleared after the
message and it returns 1 (`00247004`–`0024707D`). The message's padding dword is not initialised.

**This is what sends 18 after a deferred destroy.** `00244F00` sets bit 6 before choosing its path, and `00244DD0`'s
admitted tail sets `+0x7C` bits 4 and 5 — direction −1 — and sends 15. The completion pass later finishes that exit
toward state 1, sends **20**, re-reads state 1 and bit 6, and tail-calls `00245020`, which broadcasts **18**. A
message-20 callback that changes the state or bit 6 changes that outcome.

**Sibling order after a resort.** `002479B0` copies the children into 16-byte records
`{i32 priority = (i16) +0x44, i32 index, pointer}` in the scratch area `0208ED60` — 128 records up to the next
referenced global `0208F560`, with no check against the child count — sorts them with `00249CE0`, which partitions
until ranges of at most eleven remain and then tail-jumps to the insertion sort `00249680` over the whole array, using
comparator `00244610` (`b.priority − a.priority`, ties `a.index − b.index`), and relinks the first child and the
sibling links (`00247A51`–`00247AB1`). **So siblings end ordered by `+0x44` priority, highest first, ties in their
previous order** — a total order the partition step cannot disturb. It returns 1 in every case.

### Resource-ready — message 16 from the batch pool (2026-09-13)

`00249580(widget)` takes the first of **12 batch records of `0x20` bytes at `02090790`** with bit 0 clear, zeroes
it, sets bit 0 and `+8 = widget`; with all twelve active it returns 0. The three completion entries fix the layout —
`+0` flags (bit 0 active, bit 1 sealed), `+4` custom flag, `+8` widget, `+0x10` callback, `+0x18` u16 expected,
`+0x1A` u16 completed:

- `00249410(batch)` seals; `002494F0(batch, inc)` counts when `inc` is nonzero. Then, **if sealed and the counts are
  equal**: custom flag set → `call [batch+0x10]` with `rcx` still the batch, bit 0 left set; else **`{16}`** to the
  widget's handler and bit 0 cleared.
- `002495C0(member)` — the member pointer arrives as a sign-extended 32-bit `ecx` (`002495D9`) — calls the member's
  `+0x10` callback **first**, then counts in its batch `[member]` and applies the same test, except that its custom
  call does not reload `rcx` with the batch; it ends by clearing the member's `+0x20` bit 0.

None of the three tests bit 0 before notifying. **The load controller's resource setup `00582790` takes a batch for
itself** (`0058279D`, no null test before passing it to `00393460`), registers its requests through `00393460`,
`003933F0` and `00249210`, and tail-jumps to `00249410` (`00582850`); if the requests were already complete, message
16 arrives before `00582790` returns. **Equal counts mean the requests finished, not that their content is valid**;
what `00393460` and its siblings do natively is not read here.
*(Pointer 2026-10-01, SWE2-STRUCT for OPUS, DD batch 17: the resource pages own this and read it. On
[the typed-list page](../../02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md)
§7c, `00393460` registers the named kind-7 resource `dataface_c` through `002493D0` → `0024A4E0`, and `003933F0`
requests kind 7 id 111 through `00249320`. Check P4.)*

> **That is why the two shares differ.** Message 15 reaches only the widget being destroyed —
> 27.5 % of handlers care. Message 18 reaches its entire subtree, so **two thirds of all widgets in
> the game have something to undo when an ancestor goes away.**

### The cleanest demonstration: two 117-byte handlers

`0057E8D0` and `0057EB30` answer **only ids 1 and 18**, and differ only in which global they touch:

```c
void handler(Widget *self, Msg *m)
{
    if (m->id == 1) {                       /* construct */
        g_instance = self;                  /* 02CA99D0 / 02CA99D8 */
        self->+0xC8 = 0;
        self->+0xC0 = 0;
        Attach(*(void **)0x0208EA28, self); /* 00244960 */
        Sub_247870(self, 0);
        SetField44(self, 100);              /* 00247930 writes word [self+0x44] */
        return;
    }
    if (m->id == 18) {                      /* destroy */
        g_instance = NULL;
        return;
    }
    DefaultHandler(self, m);                /* 005C5230, reached by TAIL JUMP */
}
```

**A singleton widget that publishes itself on 1 and unpublishes on 18.** Nothing else. Two
independent handlers, byte-for-byte the same shape, is as close to a controlled experiment as static
analysis gets here.

It also names a helper: **`00247930(self, n)` writes `word [self+0x44] = n`** and sets bit `0x2000` on
the parent's flags. The widget-constructor document records `+0x44`'s low word being initialised to
`0x64` = 100; **this is the setter, and this handler passes exactly 100.** The Config screen passes
`0x6F` = 111 to the same helper.

## 10. Nine of thirty-two, and the twenty-three that remain (ten and twenty-two since 2026-09-13)

| named | how |
|---|---|
| **1, 2, 15, 18, 24** | this block — read from the sending function (24 added 2026-09-13) |
| 3, 4, 5 | the widget tree draw pass |
| 10, 12, 13 | the Config screen |
| **6, 11, 29, 30, 32, 34, 35, 37–42** | the world map screen (2026-09-15, [map page §6b](../Map-Screens/the-map-screens-and-their-shared-map-data.md)): 6 = *populate* (load data, fetch strings, install the label pane); 10/11 share the per-frame pad arm — `02F97368..71` carry the direction nibbles + confirm bit, `+0x100`/`+0x102` the cursor; 29 clears a record pointer, 30 relabels a child, 32 arms the `+0x154` open-transition counter, 34/42 set `+0x150` bits 2/7, 35 is an out-param read of `+0x172`, 37 confirm, 38 set-mode + confirm (`002901D0`→`0209BE80+0x10FA4`), 39 loads the exit mode, 40 self-sends 41, 41 builds/registers the children |

~~**22 ids remain unnamed** (23 before message 24 was placed), and the largest of them are `16` (16.1 % of handlers, 20 application
senders), `14` (22.7 %), `19` (11.4 %) and `20` (6.2 %).~~ ~~**16 remain unnamed since 2026-09-13**~~ ~~**14 remain unnamed** (recounted from the TSV, which has no 27 or 28), after
6, 7, 14, 16, 19, 20 and 25 were read from their framework senders on 2026-09-13 (§9, §4).~~ ~~**10 remain unnamed, 2026-09-20:**
`8`, `9`, `11`, `26`, `29`, `30`, `53`, `285`, `287`, `289` — after **17, 21, 22 and 23** were read from `00246C20`'s
three tween channels (§9a).~~ ~~**8 remain, later the same day:** `11`, `26`, `29`, `30`, `53`, `285`, `287`, `289` —
**8 and 9 are the focus switch** (§9c), and of the eight, **26** and **53** now have located senders and a shape
(§9d).~~ ~~**7 remain:** `11`, `26`, `29`, `30`, `285`, `287`, `289` — **53 is a destroy request** (§9e), named from
its sender and both of its receivers.~~ **3 remain:** `11`, `26`, `30` — `285`/`287`/`289` are dispositioned as a
family in §4 (private screen channels, not framework messages) and **29 is a self-sent "state changed"** (§9f).
`DL-1` stays open for the three, each with a named next step rather than a blank.
*(Pointer 2026-10-01, SWE2-STRUCT for OPUS, DD batch 17: all three are answered just below, on 2026-09-25. 11 and 26
are named, 30 is dispositioned, and `DL-1` is answered for the whole recount, §7. Checks P6, P8.)*

**Message 11 is named from its sender — 2026-09-25 (FABLE, Claude Opus 5.5): it is the per-frame input notice sent while a
transition is running on the focus chain.** Static; the bodies were read.
- **The sender.** It is `002481C0`, the focus notice, already quoted in §2 above. `rcx` = the focus top `[0208EBC0]`.
  The walk climbs the parent links `+0x10` while each node's `+0x40` has bits 0 and 3, and a node lacking either sends
  nothing. At the first node with **bit 9** it tail-jumps the focus top's handler with the `.rdata` record
  `009150F0` = `{11}` (`002481FE`–`0024820D`). If it reaches the root without one, it sends `009150D8` = `{10}` to the
  same widget (`002481EC`–`002481FB`).
- **What bit 9 is.** It is the transition-in-progress bit: the deferred-completion scheduler `00244DD0` sets it when it
  schedules a transition, and `00246C20` clears it on completion (above).
- **So 10 and 11 are one notice in two states.** 10 means *you have the input this frame*. 11 means the same *while you
  or an ancestor is mid-transition*.
- **The receivers agree.** The world-map page procedure takes 10 and 11 on one arm (its input arm, in
  [the map screens](../Map-Screens/the-map-screens-and-their-shared-map-data.md) §6b). For 11 it zeroes the three
  pad words it would otherwise read from the input snapshot (`cmp dword ptr [msg], 0xb`, then `02F97368`/`6A`/`6C`),
  so it ignores the pad while animating. The battle menu `002778C0` sends both ids to one
  arm, `00277A64`, and does not tell them apart.
- **Why three instruments missed it.** The record is in `.rdata`, but the sender reaches the handler by a tail
  `jmp rax`, not a `call`, and the `.rdata` instrument required an indirect call. A send-side census run today also
  finds no stack-record sender of 11 anywhere in the image: it starts from `lea rdx, [rsp|rbp ± X]` feeding a call,
  and its control, 8 and 9 at `00244830`, fires.

~~**2 remain: `26`, `30`.**~~

**Message 26 is a per-cell pre-draw hook — named 2026-09-25 (FABLE, Claude Opus 5.5) from its sender and a receiver.**
Static; the bodies were read.
- **The sender.** `002D2600` draws a grid list, one cell per item index below `+0xE8`, in rows and columns
  (`+0xEC` / `+0xF0`). Before placing each cell it sends `{26, (i64)index}` to the list's own handler, when the
  list's flag word `+0xE4` has bit 17 (`002D277F`–`002D279E`). It then places the cell at `+0x114` + column ×
  `+0xEA` and `+0x116` + row × `+0x100` (`002D27AB`–`002D27E7`), so what the handler does to those two words
  lands on that cell.
- **What the answer does.** It is not used before the draw. After the cell's draw callbacks, a non-zero answer
  makes the list call `002D8BB0(ctx, 0)` (`002D285A`–`002D2865`). That is the pop half of a clip push: `002D8BB0`
  keeps a depth at `ctx+0x5D`, lifts the scissor to full screen on the first push, and on the last pop restores
  the context's clip rectangle `ctx+0x48` through `00249FD0`. `00249FD0` is the scissor setter; it emits GS
  register `0x40`, `SCISSOR_1`, and uses the full screen `01E0C1D0` when given no rectangle. So a handler that
  lifted the clip for its cell returns non-zero, and the list puts the clip back.
- **One receiver read through.** The list panel `005651E0`, which the four `00563xxx` rows forward 26 to, runs a
  per-element slide. It steps the element's offset `+0x12` by 4 toward its target `+0x14` through states 1–4,
  writes the element's `+0x11` / `+0x12` into the list's `+0x114` / `+0x116`, and returns 0
  (`005653B7`–`005655A0`). So cells slide into place one by one, without touching the clip.

~~*Not read:* whether the other receivers (`002D2DB0`, `005691E0`) return non-zero.~~ *Corrected 2026-09-30
(SWE2-CONTRACT, DD batch 10, W4): both are read. `005691E0` hands 26 to `00568FE0`, which places the cell and returns
0 on both of its exits. `002D2DB0` forwards 26 to its `+0xC8` delegate and returns the delegate's answer, or 0 when it
has no delegate. So none of the five exact receivers lifts the clip by its own answer.* ~~**1 remains: `30`.**~~

**Message 30 is application-defined, not a framework message — dispositioned 2026-09-25 (FABLE, Claude Opus 5.5).**
Static; the bodies were read.
- **The census.** It starts from the send: every `lea rdx, [rsp|rbp ± X]` that feeds a call, back to the store into
  the record's first word. Its control, 8 and 9 at `00244830`, fires. It finds five immediate senders of 30,
  `00276D30`, `00279E20`, `0029A0A0`, and one each in the map-data band (`003Cxxxx`) and the world-map band (`0055xxxx`), plus the battle menu `002778C0`, which builds
  `{30}` at `[rbp − 9]`. **None is in the framework band `0024xxxx`**, and no framework function takes a `.rdata`
  `{30}` record.
- **The shapes differ by screen.**
  - Most senders broadcast a zeroed `{30}` down their own subtree: `00279E20` through the recursive broadcast
    `002753F0` (the widget, then children at `+0x18` and siblings at `+0x20`), and the two band senders
    through a second broadcast helper. Two of them follow it at once with `{32}`.
  - The battle menu broadcasts `{30}` with a 16-byte block from `00915BC0`.
  - `0029A0A0` sends `{30, value, text state}` to a delegate at `+0x120`, and draws that text state only on a
    non-zero answer (`0029A11A`–`0029A1AF`).
- **The receivers' meaning differs too.** On the world-map page, 30 relabels the `+0x160` child from the payload
  word, and 32 arms the open-transition timer
  ([the map screens](../Map-Screens/the-map-screens-and-their-shared-map-data.md) §6b).

So, like the `285`–`289` band (§4), the id carries no framework-wide meaning: each screen family defines its
payload and its answer. **Of this box's original list, nothing remains unnamed or undispositioned.** The ids
`31`–`52` of OPUS's 56-id recount (above) were never on this list and are not covered here.

**Ids `31`–`52` are screen-family messages, not framework messages — dispositioned the same day (FABLE, Claude Opus
5.5).** Two censuses, each with a control that fires, find no framework sender for any of them.
- **The send-side census over the whole image** (control: 8 and 9 at `00244830`). It finds 44 stack-record sends of
  ids 31–49 in 27 functions, and **none in the framework band `0024xxxx`–`0025xxxx`**. No send of 46, 50, 51 or 52
  turned up.
- **The `.rdata` record census over the framework band.** A `lea` onto a record whose first dword is the id finds
  the framework's own records for 10, 11, 18, 24 and 25 as the control, and **nothing for 31–52**.
- **Every sender belongs to one of two screen families.**
  - **The map screens** use 31–36, 38, 39 and 41–43: the track and location maps (`002B6xxx`–`002BDxxx`), the
    field-time map (`003CAxxx`–`003CBxxx`) and the world map (`0055xxxx`). Their meanings are read on
    [the map screens](../Map-Screens/the-map-screens-and-their-shared-map-data.md) (§2.3a, §6b); for example 35 is
    the world map's mode query.
  - **The AB30 panel family** (`0027xxxx`, the level-up UI) uses 37–40, 44, 45 and 47–49.

So, like 30 and the `285`–`289` band, these are ids a screen family defines for its own widgets, and their
meaning is the family's rather than the protocol's.

*Two notes on that list.* `11`, `29` and `30` are named in §10's table above **from the world-map screen's arms**, which
is a receiver, not a framework sender; ~~`DL-1` keeps them open on purpose and this recount does not close them.~~ *(superseded 2026-09-26 (FABLE, Claude Opus 5.5): **DL-1** was answered on 2026-09-25, and every id of the 56-id recount, 11, 29 and 30 included, is named or dispositioned.)* And the
senders were found with a **static** instrument — `lea reg, [rip+d]` onto a record whose first dword is a small id, in a
function that also makes an indirect call, with the section-aware reader — so **an id whose record is built on the
stack is invisible to it**. Its control is messages 18 and 24 at their known records and senders; the first version of
the scan used a `.text`-only offset formula for `.rdata` reads and silently failed that control, which is why the
control is now part of the script.

**A third instrument was built, returned nothing, and its empty result is uninformative — which a control proved
rather than hid (2026-09-20).** The declared blind spot of the other two is an id that reaches the record **through a
register**, so a scan was written for exactly that. It found **zero** sites, for any id. Before reporting that as
"no register-path senders exist", the population itself was measured: a stack slot written **from a register** and
then `lea`-d into an indirect call occurs **116 times in 73 functions**, against **158** sites written from an
immediate. A register-path scan finding zero against a population of 116 is a **broken scan**, not an absent
population, and the number is in this page rather than the result.

**The reason it is hard turns out to be better than the scan: some senders compute the id.** `002473F0` is the worked
example — `0024740E neg eax` / `00247412 sbb ecx, ecx` / `00247418 add ecx, 7` / `0024741B mov dword ptr [rsp+0x20],
ecx` — which yields **6** when the boolean argument is non-zero and **7** when it is zero, with **no id literal
anywhere in the function**. Every scan that looks for an id constant is blind to that class by construction, and no
amount of widening fixes it. For `DL-1`'s remaining `11`, the concrete next instrument is therefore not "find the
literal" but "find a record slot fed by arithmetic whose range covers 11" — an `add <reg>, k` or `sbb`-style
construction for `k` near 11, checked at the store into the record.

**That instrument was built, with `002473F0`'s `add ecx, 7` as its positive control, and the control passes — it
finds exactly ONE site in the whole image, `002473F0` itself.** So the computed-id form is a **one-off, not a
family**, and message 11 is now a **controlled negative on three instruments with three distinct passing controls**:
`.rdata` records (control: 18 and 24 at their known records), stack immediates (control: message 1 in the
constructor) and arithmetic ids (control: `002473F0`). The fourth, the register path, is the broken one, and its
population is the 116 sites above. *What is left is named rather than open-ended:* 11's record is built somewhere
none of these model — a slot not based on `rsp`/`rbp`, a record that is a **field of an object** rather than a stack
local, or a **forwarder** re-sending a record built elsewhere, which is exactly the shape `00247490` already shows
for 6 and 7. Its two `exact` receivers remain the proof that a sender exists.
*(Pointer 2026-10-01, SWE2-STRUCT for OPUS, DD batch 17: the sender is `002481C0`, found on 2026-09-25, above. Its
record is in `.rdata`, and it reaches the handler by a tail `jmp`, a shape none of the three instruments modelled.
Check P6.)*

*That gap is now closed by a second instrument, and it is where 8, 9, 26 and 53 came from.* It looks for
`mov dword ptr [rsp+D], <small imm>` followed — with the slot not overwritten in between — by `lea reg, [rsp+D]` and
an indirect call. Its control is **message 1 built on the stack in the constructor `002465F0`**, which the first
version of *that* scan also failed, with a 40-instruction window: the constructor writes the id at `0024660A` and
takes the address at `00246740`, far outside it. Both instruments remain blind to a record whose id is written from a
**register** rather than an immediate.

**Still not claimed:** any ordering guarantee. Nothing here establishes whether 15 always precedes
18, only that `00244F00` sends them in that order on the path it takes. *Narrowed 2026-09-13:* its second path,
`00244DD0` (301 B, taken when `flags & 0x21 == 0x21`), is read — it neither broadcasts 18 nor calls the teardown. It
sets the rate `+0xB8`, then by `+0x40` bit 0 and the signed low nibble of `+0x7C`: bit 0 clear → state 1; bit 0 set with
state 0 or 3 → an exit-animation descriptor at `+0x68` and state 4; state 2 → timestamp adjusted, state 4; any other
state returns. The admitted tail sets `+0x7C` bits 4 and 5 and sends **15** (record `01E0C0F8`). So the deferred path
is an exit-animation request with a conditional 15. ~~What later sends 18 on that path, and when, is the open part of
**`DL-3`**.~~ **`DL-3` answered 2026-09-13 (FABLE): the order is not guaranteed.** On the deferred path 18 comes from the
completion pass after the exit's message 20 (§9, *Completion*). But **teardown `00245020` is called directly from 63
functions (74 sites), and 44 of those functions neither call `00244F00` nor reference the `{15}` record `00915058`** —
the router widget's own `0027FD62` among them — so a widget torn down that way receives 18 with no 15; descendants
reached by the broadcast receive 18 and no 15 from it; and a message-20 callback can cancel the deferred 18. What holds is narrower: on each of
`00244F00`'s two paths, the 15 it sends precedes the 18 that path leads to. (The census tests only a direct call or
record reference; a caller building `{15}` on the stack would be missed.)

## 10. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment.)*

### The 24-byte record, confirmed from the data side

§2 takes the record's shape from the draw pass. Read straight out of `.rdata`:

| address | `id` | `a` | `b` |
|---|--:|--:|--:|
| `009151C0` | **3** | 0 | 0 |
| `009151D8` | **4** | 0 | 0 |
| `009151F0` | **5** | 0 | 0 |

The three ids are exactly as stated, and **the addresses are `0x18` apart** — so the 24-byte size
and the `id`-at-`+0x00` layout are visible in the spacing of the constants themselves, without the
draw pass. Two routes to one shape.

*(They sit `0x28` past `00915198`, the fixed table pointer the constructor writes to every widget's
`+0x48` — [the widget constructor](the-widget-constructor-and-object-sizes.md) §2.2.)*

### The population reproduces, and it splits

Scanning every function body for calls to the three constructors, taking the handler from the
register each one uses:

| | page | measured |
|---|--:|--:|
| constructor call sites | 280 | **280** |

| constructor | sites | share |
|---|--:|--:|
| `00244F50` (handler in `rdx`) | **231** | 82.5 % |
| `00245000` (handler in `r8`) | **40** | 14.3 % |
| `002465F0` (handler in `r8`) | **9** | 3.2 % |

**`00244F50` builds five widgets in six** — which
[the widget constructor](the-widget-constructor-and-object-sizes.md) §2.2 asserts in words
(*"most widgets are built through `00244F50`"*) and neither page counts.

> **And the split closes the other page's census.** That page counts **49** sites because it looks
> only at direct `00245000` / `002465F0` calls. **40 + 9 = 49.** So `280 = 231 + 49`: the two
> populations are not two measurements, they are one population seen from two sides, and the
> arithmetic between them holds exactly. Neither page says so.

### A method note, against this pass rather than the page

Recovering the handler with a **twenty-instruction** window gives **238** distinct handlers and
leaves **6** sites unrecovered, against §3's then-**239 confirmed** and **4**. `widget_messages.py` has
the better rule; the shortfall is this pass's window, not a disagreement. §3's own account of *why*
candidates exist — the backward branch at `0023C0CD` into the call at `0023BFFF` — is the same class
of limitation, stated there first.

*(2026-09-15, regenerated: the call-only figures above still hold — the regenerated census counts
**297 transfer sites = 280 `call` + 17 `jmp`**, and §3's population is now **267**, not 251.)*

**Not claimed:** §4's id decoding, the EXACT / UPPER BOUND split and the 32 distinct ids were **not**
re-derived — that needs the chain-and-switch decoder, and this pass did not rebuild it. §8's sender
pass is untouched. Nothing was executed or observed live.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

Uncited residuals neighbouring this protocol page, read at call-signature level:

| function | size | role |
|---|---:|---|
| `002856B0` | 491 | five-step poll/settle loop on `[rdi+0x60]`/`[rbx+0x10]`: alternating `002DDC50`/`00254A00` ×5 |
| `0028B860` | 666 | widget-lookup dispatcher (jump table present, not decoded): `0035D460` context getter ×3, `00271AB0` array search ×2, `00245020`/`00244DD0`/`002735E0`, `0028B700`; reads `[rbx+0x10]`/`[rcx+0x10]`/`[+0x44]` |
| `005651E0` | 1028 | license-screen widget helper — called from `005636F0`/`00563930`/`00563B10`/`00563D20` (the license-board family): `[rdi+0xD8]`/`+0xE0`/`+0x180`, `002445C0`/`002D45C0`/`002470C0`, `002527B0` ×2, `00293110`, plus `00563DC0`/`00564650`/`00563F10`/`00565720`; interior read 2026-09-17 (SWE2-FRONTIER): `00564C80` first at [`00565218`](../../_index/ADDRESS-INDEX.md), `002D45C0` at `00565238` |
| `005771F0` | 758 | **already placed** — quest-list pane helper, [the quest-list screen](../Quest-List/the-quest-list-screen.md) (`a3bf73bb`) |
| `0057E6D0` | 499 | save/load pane geometry — called by `0057EFE0`: `[rcx+0xC8]`/`+0xD0`, `[rbx+0x98..0xCA]`, `[r8+0x20]`/`+0x39`/`+0xA`, `00247870` ×2 + `00394800` |

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Movement — CLIENT.** `WorldActor_UpdateRuntimeAndScriptExecutionState`, owned by that layer, calls `001EDDA0` on this page. That caller is the per-body runtime and script-execution update: it skips when `byte[rec+0x18] == 1`, needs the kind bits `byte[rec+3] & 0xE0 == 0x60`, and then runs a dispatch loop that consults the scheduling predicates at `001EDDA0` and `001EDE80` and resolves pointers through the image-base helper; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT and MECHANICAL (SWE2-CONTRACT 2026-09-15, 55 edges measured).** The widget
bodies this page cites are *driven* by the render layer's UI state machines —
`00579420` (`Presentation.UI.Quest.ListScreenSelectionStateMachine`, 5 edges; interior read 2026-09-17, SWE2-FRONTIER: `002432B0` first at [`00579490`](../../_index/ADDRESS-INDEX.md), `00394720` next),
`002BAF80`/`002B7B80` (`Presentation.UI.InputConsumerStateMachine`) call `00244DD0`/`002470D0`/
`00247870`/`00249410`/`00249580` — and the message path's text side sits in the shared
`Presentation.Text.*` family (`00366110` brace-tag markup, `003649A0` glyph-run emission,
`caseD_0`/`caseD_1` of `00505E00`/`00505570` on `00254A00`/`002DDC50`). The remaining ~40 edges are
the `001EDDA0` frame helper's Presentation fan-in — mechanical. The crossing is the widgets' place
inside the render layer's message pump, not a second owner.

**ActorEntity — CLIENT (4 edges, both neighbour bodies read).** Three functions cited here resolve a
packed handle before they do anything with it: `002B7B80`, `00505570` `caseD_1` and `00505E00`
`caseD_0` all call `ActorHandle_ResolveRegistryEntryByPackedId` `003588B0` (interior verified
2026-09-17, SWE2-FRONTIER — `00505E00`'s call is [`00505EAF`](../../_index/ADDRESS-INDEX.md),
`00505570`'s is `005056A9`, each with `002EA0E0`/`00203080`/`002DDC50`/`00254A00` around it), and
`002B7B80` follows it
with `Actor_GetWorldPosition` `00265020`. Both of those **answer nothing rather than answering
wrongly**: `003588B0` returns null the instant the packed id is zero, before touching the registry;
`00265020` writes three zeros into its out-parameters for a null body and for any body whose kind
nibble — `byte[+3] >> 5` — is not 1 or 3. So a widget that asks about something that is not there is
told nothing, not told the origin of the world. The crossing is those two calls. Read from the
shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — MECHANICAL.** The record-driver helper `00282FA0`, cited by this
page's `002C1800`, is also called by the PlatformOnlineAchievements bodies `003162E0`/`00316760` —
a shared leaf, not an achievements service the protocol invokes. The page owns the widget message
protocol; what that layer asks of the same leaf is not claimed.

**CoreRuntimeScheduling — CLIENT (FABLE, Claude Opus 5.5, 2026-09-24).** §2a cites the pause getter
`0017E4E0` because the per-frame UI pass `00250540` consults it to choose which roots to walk
(`00250570`). Its other readers are the scheduling layer's own frame bodies: the frame dispatcher's
prologue `0022A580` mirrors it every frame, and the field frame `0022A770` runs only the pause step
while it is set. Its writer is the pause-menu handler, through `0017E720`
([the game-application page](../../00-Engine-Core-Runtime/Application-Root/game-application.md), BE-2).
The crossing is that one read. The widget framework neither sets nor clears the pause flag; it only
narrows its walk to `[0208EA48]` while the flag is up.

**Input — CLIENT (SWE2-EC7-157, 39 edges).** Batch-122's `0027E810` calls `001E0E30`, whose Input-layer neighbours (`001986D0`/`00198790` callees, `00250130` among `00229DF0`'s callers) share the slot-table family — the protocol consults them, not owns them.

**Save/load settings — CLIENT (34 edges).** The save/load layer's settings bodies call the widget helpers this page cites: `00583D60` calls `003271D0` (the focus-slot resolver `00282FC0` consults), and `00582860`, `0057E4D0` and `005819F0` reach `001EDEC0`/`00244960` — settings screens driving widget state, not a widget dependency on settings data. Edge count from `edges.tsv`. (SWE2-EC7 batch 152, shipping bytes.)
**Resource — CONSULTED BOTH DIRECTIONS (SWE2-EC7, batch 168, 47 edges).** The batch-168 `00244500` clock-window easing calculator names caller `00242C90` and lerp `00248F40`, both adjacent to Resource bodies (`00249180`, `0032E400`, `0032E620`): the message layer drives widget state from Resource-side records and Resource callers consult the same clock helpers - shared machinery, no shared ownership.

**Combat — CLIENT (SWE2-EC7, batch 170, 1 edge).** The `+0x698` child resolver `00263E30` the batch-170 `0031AB80` gate rides is also called by Combat-filed `003206E0` - the mode object's accessor is shared, fan-in only.

**CombatAI — CLIENT (SWE2-EC7, batch 170, 4 edges).** The same `00263E30` accessor answers CombatAI callers `003247F0`/`00324F20`, and `0046B1A0`/`0046B240` are consulted by `00321190` on that layer - the protocol's resolve chain shares helpers with the combat-AI family; no shared ownership.

**Status_Periodic_Terminal — CLIENT (SWE2-EC7, batch 170, 1 edge).** `00263E30` is also called by `00386860` on that layer - the same shared child resolver, one more fan-in arm.
- **Items_Equipment_Shops_License - SERVICE (16 edges).** `002C2320`, `003FF360`, `00557DB0`, `0055C740` (+2 more) reach bodies filed to Items_Equipment_Shops_License: Equipment_BuildRecommendedLoadoutForMappedStats (`002F9F20`), BattleStats_ClearAllEquipmentSlotsByMappedId (`0031A300`), BattleStats_SetEquipmentSlotsByMappedId (`0031A710`), Equipment_CheckPrimarySecondaryPairReasonByStatsIndex (`003231F0`) (+7 more) - shared machinery across the layer boundary, no shared ownership.

## The `00244970` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`00244970` is a five-byte thunk tail-jumping to `00244980` (151 B), the
recursive completion pass. With `[rcx+0x40]` bit 0 set (`0024498C`), a set bit
13 runs `002479B0` and clears `0x2000` on a nonzero return
(`00244990`–`0024499F`); `00246C20(rbx)` must return nonzero
(`002449A9`); `[rbx+0x7C] & 0xF == 1` gates the tail dispatch: `[+0x40] &
0x40` → tail `00245020` (`002449CB`), `& 0x20` → `002473F0(rbx, 0)` + clear
bit 1 (`002449D9`–`002449DE`), else clear bit 1 only (`002449E8`). When bit 0
is clear the function walks the `[rbx+0x18]`/`[rbx+0x20]` child chain and
recurses on each node (`002449F4`–`00244A0F`).

| member | role | interior |
| --- | --- | --- |
| `00244980` (151 B) | the recursive completion pass the five-byte root tail-jumps to — the bit-13/`002479B0` arm, the `00246C20` gate, the `[+0x7C]&0xF==1` tail dispatch to `00245020`/`002473F0`, and the `[+0x18]`/`[+0x20]` child-chain self-recursion described above | [`0024498C`](../../_index/ADDRESS-INDEX.md) |
| `00246C20` (1,178 B) | the per-node completion visit — first act is `call qword[01F44830]` with the `{25}` record `00915120` (`00246C4A`–`00246C51`), then property animation via `00229DF0`/`00229EA0` with `xmm6 = 1.0f` (`00246C5D`), `0208F570` reads and `00248F40` record-submit ×4 (tags `00915138`/`150`/`168`/`180`), `{19}`/`{20}` finish forwards through the same `[01F44830]` slot (`00247039`/`0024706B`), `00808C40` cleanup (`002470AF`) | [`00246C26`](../../_index/ADDRESS-INDEX.md) |
| `002479B0` (303 B) | the sibling resort — reads `[01F44830]`, builds 16-byte records from the child list at `0208ED60`–`0208ED78` (`002479EA`–`00247A75`), matches `00244610`, `00249CE0`/`00861EC0`/`00808C40` helpers | [`002479BD`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `002473F0`, `00245020`, `00249CE0`,
`00248F40`, `00229DF0`, `00229EA0`, `00861EC0`, `00808C40`.

## Interior citation — frontier hub `00247870` (2026-09-17, SWE2-EC7)

`00247870` — 89 B, 47 frontier callers at census; the flag-write half of the accessor pair the
heap-release path uses. Interior verified: [`00247887`](../../_index/ADDRESS-INDEX.md) is
`test cl, 0x20` on `dword[rcx+0x40]` — the body is a **null-guarded bit-1 setter with a
propagation callback**: `rcx==0` returns early; when the `+0x40` flags already carry `0x20`, an
`edx` set forces `|= 2` and then calls `002473F0` (the root-state propagation helper) with
`rcx` intact, clearing `& ~2` after the call when `edx==0`; when `0x20` is absent the bit is
merged in place (`(edx*2 ^ flags) & 2 ^ flags`) and no callback fires.

NOT claimed: what `+0x40` bit 0x20 arms (a hierarchy-visible-state precondition per the
`002473F0` callee name — "root state bit propagation with callback token" — but the bit's own
author is not traced here).

*Pointer 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17, checks B1–B3): the author is read on this page, in "Kept,
then reclaimed" above.* The root procedure `002445D0` sets `+0x40 |= 0x23` (bits 0, 1 and 5) on message 1
(`002445D8`). Attach `00248220` copies bit 5 from parent to child (`0024826B`, `00248271`) and pushes it through the
child's subtree with the visitor `002418E0`, which sets bit 5 from its argument. Teardown `00245020` tests it
(`00245072`): a bit-5 widget is kept rather than released. So bit 5 marks a root and every widget attached under one.

## Interior citation — frontier hub `00249410` (2026-09-17, SWE2-EC7)

`00249410` — 133 B, 27 frontier callers at census; the "resource batch complete" seal this page's
message-16 row names. Interior verified: `or [rcx],2` sets the sealed bit; if it was **already**
sealed and `word [+0x18] == word [+0x1A]` (counts meet at
[`00249430`](../../_index/ADDRESS-INDEX.md)) it dispatches completion — `dword [+4] != 0` calls
`[rcx+0x10]` directly, else it vcalls `*[rcx+8]` with a `{0x10,0,0,0}` arg block. Exit clears bit
0 (`and [rbx],~1`). Exactly the seal-and-count gate §16 describes, now anchored inside the body.


## Interior citation — frontier hub `002445C0` (2026-09-18, SWE2-EC7)

`002445C0` — 13 B, 22 callers; the `0208F570`→`0208ED54` state-dword publish the
license-screen helper above invokes. Interior verified: `mov eax, [0208F570]` /
`mov [0208ED54], eax` at [`002445C0`/`002445C6`](../../_index/ADDRESS-INDEX.md) — a straight
copy of the shared state word into the widget-visible cell.


## Interior citation — frontier hub `002DDC50` (2026-09-18, SWE2-EC7)

`002DDC50` — 24 B, 11 callers; the availability predicate the widget handlers consult.
Interior verified: `call 0053DD10` at [`002DDC54`](../../_index/ADDRESS-INDEX.md) then
`cmp eax, 1; sete` — it is `0053DD10() == 1`, and `0053DD10` (measured batch 9) is the
hard-wired `return 1`, so the predicate is constant-true in the shipped image.

## SWE2-EC7-20 update (2026-09-18) — dispatch-side fragment set: `0057A2D0`, `00561F20`, `0055B960`

`0057A2D0` (38 B) is a `00249210`-resolve wrapper: it stages `dword[rsp+0x20]=1`,
forwards `r9d=r8d`, keys the lookup with `r8d = edx+0x31` and `edx=7`
(`0057A2D7`..`0057A2E3`), calls `00249210` (`0057A2E8`), and returns
`[rax+8]` (`0057A2ED`) — the `+0x31`-biased record fetch the protocol's
callers run per widget kind. Callers `00558FB0`/`00561390`/`00572E10` — the
screen-load path this protocol's widgets sit under.

`00561F20` (57 B) is a word-pair range clamp: it pulls `ax` from `[rcx+8]` and
`[rcx+0xA]` as upper bounds (`00561F20`/`00561F2E`), stores `min([rcx+0x10], ax)`
and `min([rcx+0x12], ax)` (`00561F2A`/`00561F38`), then pulls `[rcx+0xC]` and
`[rcx+0xE]` as lower bounds storing `max` (`00561F3C`..`00561F54`). The result
clamps `+0x10` into `[[+0xC], [+0x8]]` and `+0x12` into `[[+0xE], [+0xA]]` — the
extent fix-up the message handlers run after a resize. Callers
`0055CD40`/`0055E9E0`/`0055F3E0` — the widget message handlers.

`0055B960` (338 B) is the scroll-extent computer the dispatch handlers share:
it sign-extends the `+0x550..+0x555` byte triple and the `+0x50C..+0x512` bound
words (`0055B978`..`0055B9A8`), forms `edi = s8[+0x550]*s8[+0x554]` and
`esi = s8[+0x551]*s8[+0x555]` — the column/row counts — plus `edx = s16[+0x50C]
− s16[+0x51C]` and `r9d = s16[+0x50E] − s16[+0x51E]` content extents, adds
`ecx = s16[+0x510]`/`r8d = s16[+0x512]` view sizes, and biases both products by
half of `[01F2CACC]` and half of `s8[+0x554]` (`0055B9B0`..`0055B9F0`). The
clamp half derives `r10d`/`r9d` as the non-negative scroll ranges — `max(0,
edx−edi)` / `max(0, r9d−esi)` selected against the view sizes
(`0055B9F8`..`0055BA2A`) — before the dispatch tail consumes them. Callers
`0055C740`/`0055CD40`/`0055E9E0`/`0055F3E0` — the dispatch cluster.

## SWE2-EC7-21 update (2026-09-18) — `0023DFC0` kind→string selector

`0023DFC0` (95 B) is a `0x2E0`-tagged packet submit the widget record readers
use: it packs `{byte cl, byte dl, qword r8, dword 0, qword &rsp+0x20, qword 0}`
into a `rsp+0x20` record (`0023DFD6`..`0023E008`), passes `rdx = 0023E020` as the
continuation and `ecx = 0x2E0` as the tag (`0023DFE8`/`0023DFF9`), and posts
through `00244F50` (`0023E008`) — cookie-guarded, returns after the security
check (`0023E00D`..`0023E01E`). The `0023E020` continuation is the dispatch
body that re-reads `[rdx]` kinds 1/2/0xC/0xF. Callers `0023BD40`/`0023C5C0`/
`0023CE10`/`0023FBE0` — the config/widget record readers.

## SWE2-EC7-26 update (2026-09-18) — `002735E0` kind-indexed record address

`002735E0` (19 B) sign-extends `ecx`, computes `rcx = rax * 5`, and
returns `[009158C0] + rcx * 8` — the 40-byte-stride record address the
message-protocol callers index by widget kind. Interior anchor
`002735E3` (the `*5` compose).
## SWE2-EC7-31 update (2026-09-18) — `00249CE0` introsort partition + `002481C0` focus notice

`00249CE0` (507 B) is the sort this page's child-list paragraph
names: a stack-machine quicksort — `rdx` is an explicit (lo,hi)
dword stack (pairs `+0`/`+0x30`, `rcx` the depth), `r12d` the
element size, `r13` the comparator called as `(elem, pivot)`.
Each partition median-scans from both ends (`edi`/`esi` indexes,
`elem = base + idx*r12d`), swaps bytewise when `edi < esi`, and
spills sub-ranges over 10 elements back onto the stack; at the
cutoff it tail-jmps `00249680` — the insertion pass — with the
remaining range. Interior anchor `00249D8F` (the `call r13`
comparator).

`002481C0` (81 B) is the focus notice the phase paragraph names:
the `0208EBC0` chain is walked (`rax = [rax+0x10]`) for the first
node whose `dword[+0x40]` carries both bits `0x1` and `0x8`; bit
`0x200` there selects the `009150F0` arm (the `0xB` message),
otherwise the walk continues and an exhausted chain tail-calls the
head's `qword[rcx]` vfunc with `009150D8` (the `0xA` message).
Interior anchor `0024820D` (the `jmp rax` vfunc tail).

## SWE2-EC7-33 update (2026-09-19) - `002C13C0`

`002C13C0` (998 B) is the protocol's record driver - `002D8910`/`00254A10`/`00861EC0`/`005C5230`/`002D8530`/`002D6620`/`002C1800`. Interior anchor `002C171C` (a `002D8910` call).

## SWE2-EC7-34 update (2026-09-19) - `00285290`

`00285290` (964 B) is a widget message dispatcher - `[rdx]-1` kind switch `<=0x13` through the `00120000` jump table, `002432B0`/`002478D0`/`00244F50`/`00244960`/`0020E600`. Interior anchor `0028530D` (an `002432B0` call).

## SWE2-EC7-34 update (2026-09-19) - `002C3560`

`002C3560` (841 B) is a widget message handler - `[rdx]` switch `{1, 2, 0xC}` arms, `002C38B0`/`002C3B90`/`002C388F`/`00247870` plus `005C5230`/`00368360`/`002D4930`. Interior anchor `002C35CA` (an `002C38B0` call).

## SWE2-EC7-35 update (2026-09-19) - `002C4460`

`002C4460` (697 B) is a widget message body - `0209AC30`/`00916CB8`, `00808C40`/`005C5230`/`00368360`/`002D4930`/`002C53B0`/`002C4720`/`00247930`. Interior anchor `002C449D` (an `00808C40` call).

## SWE2-EC7-36 update (2026-09-19) - `0028B860`

`0028B860` (666 B) is a widget message body - `00915E10`/`0208F570`, `0035D460` quadruple plus `0028B700`/`00271AB0`/`005C5230`/`00808C40`. Interior anchor `0028B8A3` (a `0035D460` call).

## SWE2-EC7-36 update (2026-09-19) - `00565720`

`00565720` (656 B) is a widget dispatch - `0057CF20`/`003697F0`/`002D47C0`/`002D1820`. Interior anchor `0056573C` (a `0057CF20` call).

## SWE2-EC7-36 update (2026-09-19) - `003EF830`

`003EF830` (610 B) is a widget message body - `00D11C88`/`00D11CA0`/`01E0C1D8`/`01E0C1DC`, `00244F50` pair plus `005C5230`/`003EFAA0`/`003EF770`/`00808C40`. Interior anchor `003EF872` (a `00244F50` call).

## SWE2-EC7-38 update (2026-09-19) - `0057E6D0`

`0057E6D0` (499 B) is the save/load pane geometry body the page names - `[rcx+0xC8]`/`+0xD0`, `[rbx+0x98..0xCA]`, `[r8+0x20]`/`+0x39`/`+0xA`, `00D23EA8`, `00247870` pair plus `00394800`. Interior anchor `0057E71C` (a `00247870` call).

## SWE2-EC7-38 update (2026-09-19) - `002856B0`

`002856B0` (491 B) is a widget message body - `0209AC30`, `002DDC50`/`00254A00` quintuples. Interior anchor `0028570B` (a `002DDC50` call).

## SWE2-EC7-41 update (2026-09-19) - `0028B700`

`0028B700` (340 B) is a widget-message body - `002D8C80` single call. Interior anchor `0028B812` (the `002D8C80` call).

## SWE2-EC7-42 update (2026-09-19) - `002CF740`

`002CF740` (303 B) is a widget-message body - `00916F58`/`01F44830`/`0208EA28`/`0209AC30`, `005C5230`/`002432B0`/`003200A0`/`0035D330`/`002B58B0`/`0020E620`/`00247570`/`00246AD0`/`00808C40`. Interior anchor `002CF76B` (a `005C5230` call).

## SWE2-EC7-42 update (2026-09-19) - `00249680`

`00249680` (299 B) is a widget-message body - `00861EBA` triple. Interior anchor `002496E9` (an `00861EBA` call).

## SWE2-EC7-43 update (2026-09-19) - `00564650`

`00564650` (296 B) is a widget-message body - `00295D50`/`00368830`/`00368A60`/`00567690`. Interior anchor `00564739` (a `00295D50` call).

## SWE2-EC7-44 update (2026-09-19) - `00407590`

`00407590` (273 B) is one of the `00407590`/`004079A0` widget pair the page names - `001EDEC0`/`003946B0`/`00407450`/`004076B0`/`00407B70`/`00407F90`/`00861EC0`. Interior anchor `004075E6` (an `001EDEC0` call).

## SWE2-EC7-45 update (2026-09-19) - `0027E3E0`

`0027E3E0` (250 B) is one of the `0027D700`/`0027D740`/`0027E3E0` no-constructor group - `00249C60`/`0027D740`/`00290490`/`002D47C0`/`00808C40` plus a `call rax` vcall. Interior anchor `0027E401` (a `00249C60` call).

## SWE2-EC7-45 update (2026-09-19) - `00563DC0`

`00563DC0` (243 B) is a body - `00293110`/`002D45C0`/`00564380`. Interior anchor `00563E2C` (a `00293110` call).

## SWE2-EC7-46 update (2026-09-19) - `00563B10`

`00563B10` (225 B) is a body - `00244960`/`003FCCC0`/`00564010`. Interior anchor `00563B8D` (a `00244960` call).

## SWE2-EC7-47 update (2026-09-19) - `005636F0`

`005636F0` (222 B) is a body - `00244960`/`003FCCC0`/`00564010`. Interior anchor `0056376A` (a `00244960` call).

## SWE2-EC7-50 update (2026-09-19) - `00564B90`

`00564B90` (186 B) is a body - `00564AC0` single call. Interior anchor `00564C34` (the `00564AC0` call).

## SWE2-EC7-51 update (2026-09-19) - `00563F10`

`00563F10` (173 B) is a body - `002445C0`/`00293110`/`00564380`. Interior anchor `00563F53` (a `002445C0` call).

## SWE2-EC7-52 update (2026-09-19) - `0057CF20`

`0057CF20` (1524 B) is the widget-dispatch worker - `0057CE10`/`002FAD30`/`002497E0`/`00861EC0`/`0020E620`/`0020E600` (60 direct calls). Interior anchor `0057CF64` (a `0057CE10` call).

## SWE2-EC7-53 update (2026-09-19) - `002C1800`

`002C1800` (477 B) is a widget-protocol record body - `00282FA0`/`002C9B30`/`002DD7E0` plus `0209AC30`. Interior anchor `002C1855` (a `00282FA0` call).


## SWE2-EC7-53 update (2026-09-19) - `00407F90`

`00407F90` (421 B) is a widget procedure sibling of `004079A0`/`00407590` - `00247870`/`00394660`/`00394690` plus `02B62D80`. Interior anchor `00408070` (a `00394660` call).

## SWE2-EC7-56 update (2026-09-19) - `003EF770`

`003EF770` (190 B) is a widget message body - `00244F50`/`00808C40` plus `01F44830` cookie. Interior anchor `003EF7B0` (a `00808C40` call).

## SWE2-EC7-57 update (2026-09-19) - `003200A0`

`003200A0` (187 B) is a widget-message body - `00303E90`-`00304670` family plus `00313590`/`003135E0`. Interior anchor `003200C5` (a `003135E0` call).


## SWE2-EC7-57 update (2026-09-19) - `0057CE10`

`0057CE10` (172 B) is a call-free jump-table leaf - `jmp rcx` into ~13 `lea` arms returning `00D239A0`-family constants. Interior anchor `0057CE31` (the first `lea` arm).

## SWE2-EC7-59 update (2026-09-19) - `00564C80`

`00564C80` (162 B) is a license-screen widget helper - `00564D30`/`00564E10`. Interior anchor `00564CA3` (a `00564D30` call).

## SWE2-EC7-60 update (2026-09-19) - `00564E10`

`00564E10` (885 B) is a license-screen widget body - `002445C0`/`00247950`/`00249C60`/`002527B0`/`00295D50`/`002D3900`/`002D45C0` plus `02F97368`-`02F9736C`. Interior anchor `00564EE2` (a `005665B0` call).


## SWE2-EC7-60 update (2026-09-19) - `00564D30`

`00564D30` (219 B) is a license-screen widget helper - `00249C60`/`002D3900`/`00565BD0` plus `01E0C2A0`/`01E0C2A4`/`02F9736A`. Interior anchor `00564D65` (a `00249C60` call).

## SWE2-EC7-61 update (2026-09-19) - `00565BD0`

`00565BD0` (241 B) is a license-screen widget helper - `002530E0`/`00564380` plus `00D23960`. Interior anchor `00565C18` (a `00564380` call).


## SWE2-EC7-61 update (2026-09-19) - `005665B0`

`005665B0` (202 B) is the `ConfirmWindow`/`ItemSort` widget body the protocol table names - `00244F50`/`00808C40` plus `01F44830`/`0209AC30`. Interior anchor `00566655` (a `00244F50` call).

## SWE2-EC7-62 update (2026-09-19) - `002530E0`

`002530E0` (344 B) is a widget-protocol body - `0016D6A0`/`0020E600` plus `02092760`/`020927C0`. Interior anchor `00253116` (a `0016D6A0` call).


## SWE2-EC7-62 update (2026-09-19) - `00563930`

`00563930` (149 B) is a widget-protocol body - `00564010` single call. Interior anchor `0056399F` (a `00564010` call).


## SWE2-EC7-62 update (2026-09-19) - `00563D20`

`00563D20` (149 B) is a widget-protocol body - `00564010` single call. Interior anchor `00563D8F` (a `00564010` call).



## SWE2-EC7-64 update (2026-09-19) - `002494F0`

`002494F0` (138 B) is a message-admission body - `00808C40` single call plus `01F44830` and two vcalls. Interior anchor `00249530` (a `00808C40` call).


## SWE2-EC7-67 update - `002C3B90`

`002C3B90` (128 B) is a widget-message body - `002D4840` single call plus `0209AC30`. Interior anchor `002C3BAD` (a `002D4840` call).

## SWE2-EC7-71 update (2026-09-19) - `00293110` mode-gated helper measured

Measured on `the-shop-screens.md` (PARTIAL - non-bearing); mirrored here
where the widget-protocol callers live.

`00293110` (93 B) is the gate the shop/license widget bodies run before
`00293170`: `ecx == 0 && edx == 0` tails it as `00293170(0, 1, 0)`;
otherwise it walks `[0209AC30] -> +0x2F8 -> +0xC0 -> dword[+0x40] & 1`
and tails `00293170(ecx, 0, flag)` with the UI-mode bit as the third
argument, a dead link producing `00293170(ecx, 0, 0)`.
Interior anchor `00293146` (the `& 1` test).

## SWE2-EC7-72 update (2026-09-19) - `00564380` mode translator measured

`00564380` (143 B) is the mode translator the widget helpers call:
`movsx byte[+0x17E]` selects one of eight arms through the jump table at
`00120000 + 0x444410`; six arms return constants 1-7, and the payload
arm indexes `byte[+0xF7 + ((dword[+0x180] << 6) >> 0x1B)*8]` - `0xF`
maps to 9, otherwise 5.
Interior anchor `005643A4` (the `jmp rdx` table dispatch).

## SWE2-EC7-74 update (2026-09-19) - `00393900` + `003933F0` + `0036FD70` widget helpers measured

`00393900` (70 B) is the bounded array visit: for `rbx` under `edx`,
`0024A680([rsi + rbx*8], 1)` runs on each pointer element - the
widget family's per-element apply with mode 1.
Interior anchor `00393929` (the `0024A680` call).

`003933F0` (104 B) is the translate-table build: for `rbx` under `r9d`,
`00249320(rbp, 7, [rsi + rbx*4])` resolves each index element and the
result lands at `[r14 + rbx*8]` - the mode-7 lookup into a qword table.
Interior anchor `0039342C` (the `00249320` call).

`0036FD70` (12 B) is the `02AD9E00` flag clear: stores 0 then tails
`003696D0` - the clear-and-forward the widget callers use.
Interior anchor `0036FD77` (the `jmp 003696D0` tail).

## SWE2-EC7-80 update (2026-09-20) - `005790D0` + `00577E10` + `005674B0` measured

`005790D0` (93 B) is the three-child cleanup on `[02CA9748]`:
`00244F00` runs on `+0x118` and `+0x128` when each is non-NULL, then
`00247510([+0xC8], 0xF, 0xF)` tails - the release pass the widget
callers share.
Interior anchor `005790E7` (the first `00244F00` call).

`00577E10` (227 B) is the position write-and-commit on the same
object: `00579230([+0x118], byte[[+0x128]+0xC1], &pair)` fetches the
pair; `ebx` picks the source (the fetched pair, or the object's own
`+0xC4`/`+0xC6`) and stores it to `[+0x128]+0x98`/`+0x9A`; then
`002468A0([+0x128], pair, 1, 0xC8)` commits.
Interior anchor `00577E4B` (the `00579230` fetch).

`005674B0` (468 B) is the element layout pass: `byte[rcx+0x150]`
elements from the `[rcx+0xC8]` pointer array each get a
`word[+0x98..+0x9E]` position quad written from the running `r15d`/
`r14d` span values (computed from `+0x148`/`+0x150` flags and the
`+0x152` byte), `00247870(elem, 1)` commits each, and elements whose
`+7` byte matches `word[+0xD4]` get `002D04F0(elem, 0x80)` plus
`00566B70([rcx+0xC0], idx, x, 1, 0x64)`; `00566FE0` tails the pass.
Interior anchor `005674F4` (the `bt r8d, 0x1C` flag test).

## SWE2-EC7-81 update (2026-09-20) - `005655F0` + `0055A1F0` element passes measured

`005655F0` (295 B) is the element materialize the widget callers
run: `[+0x180] << 6 >> 27` indexes the `+0xF6` byte row; `003697F0`
releases a live `[+0xE0]`; `byte[+0x17F]` picks the `0057D5E0` arm
(`0x20` -> ecx 1, `0x13` -> ecx 0); `0057CF20(word[rsi+6],
bp << 16 | al, 0, &stack)` builds the object stored back to
`+0xE0`; the `[+0x60]` table's `[+0x180]`-indexed record takes
`002F9860` -> `+0x18` and `0020E620` -> `+0x20`; `002D48C0([+0xD8],
flag)` and `00565A00(rcx, flag, r14)` tail.
Interior anchor `00565639` (the `003697F0` release).

`0055A1F0` (336 B) is the four-slot select-activate on `[+0x140]`:
the slot matching `byte[+0x55D]` gets `+0xD0` =
`[+0x120] + 0x38 * ([+0x550] + [+0x551]*[+0x559])`, `+0xD8` =
`[+0x160]`, a `00282DF0` fetch, `00559E30`, `+0x40 |= 0x400000`,
the bit23 toggle folded from `[+0xD0]+0x18`, `00247680`, the bit15
toggle from `r12d << 15` and `00246AD0([0208EA28])`; unselected
slots take `00244DD0` each.
Interior anchor `0055A28A` (the `00282DF0` call).

## SWE2-EC7-86 update (2026-09-20) - `00402230` + `003FCCC0` measured

`00402230` (27 B) is the ancestor walk for flag bit 0 the widget
callers run: from `rcx` it follows the `+0x60` parent chain until
a node has `byte[+0x28] & 1` set, returning that ancestor - or
`rcx` itself when none is flagged (the no-parent case included).
Interior anchor `00402238` (the `+0x28` bit-0 test).

`003FCCC0` (83 B) is the 0xC0-record builder the message-protocol
callers run: under a stack cookie it packs `ecx`/`edx` into a
stack descriptor and calls `00244F50(0xC0, 003FCD20, &desc)` so
the `003FCD20` callback constructs the record.
Interior anchor `003FCCFC` (the `00244F50` builder call).

## SWE2-EC7-99 update (2026-09-20) - `002D4D60` + `002D1820` + `002CF8B0` + `002CD470` measured

`002D4D60` (423 B) is the paged-cursor step `002D47C0` and
`002D4840` call: `word[+0x100]` and `word[+0xEA]` are the
vertical/horizontal page pitches, `word[+0x9E] -
dword[+0x13C] - 1` and `word[+0x9C] - 1` divide into the
current page indices, a zero `word[+0xE8]` clears `+0xF2`
and returns 1 (nothing to scroll), otherwise the
`(edx, edi)` step clamps against `word[+0xE8]`, divides
by cell pitch `byte[+0xEC]`, and writes the new
`+0xF2`/`+0xF4` cursor plus the `+0xED`/`+0xEE` edge
flags - the grid-scroll advance the message arms drive.
Interior anchor `002D4E0C` (the `+0xED` write).

`002D1820` (75 B) is the page-index getter `002778C0`,
`00565720`, `00565A00` and `005713C0` call: a non-null
`rdx` receives `(word[+0x9E] - dword[+0x13C] - 1 + pageY)
/ pageY` and a non-null `r8` receives `(word[+0x9C] - 1 +
pageX) / pageX` - the same index arithmetic `002D4D60`
and `002D4B70` internalize, exposed as an out-parameter
pair.
Interior anchor `002D1867` (the `*r8` store).

`002CF8B0` (131 B) is the conditional post `00280DE0`
calls: when `0209AC30`'s `+0x278` object is null it posts
command `0xC8` with record `{0, movsxd(ecx), 0}` and code
`002CF940` through `00244F50`; when the object exists and
its `byte[+0x7C]` bit 5 is set, `0208EA28` goes to
`00246AD0` instead - the occupied/free fork the message
posts share.
Interior anchor `002CF8F8` (the `00244F50` call).

`002CD470` (52 B) is the keyed scan `00280CA0`, `00280DE0`
and `00565E00` call: `word[rcx]` entries of the `[rcx+8]`
table walk in `0x20` strides comparing `dword[entry]` to
`r9d`, a hit returns the index, and exhaustion returns 0
when `r8d == 1` else -1 - the not-found encoding the
lookup arms distinguish on.
Interior anchor `002CD488` (the compare loop head).

## SWE2-EC7-100 update (2026-09-20) - `002C9F30` + `002C9E80` + `002C41F0` + `002C2F60` measured

`002C9F30` (80 B) is the keyed-find-and-write `00280DE0`
and `002C2320` call: the `word[rcx]`-counted `[rcx+8]`
table scans `0x20` strides for `dword[entry] == r9d`
(default index 0), and a non-null `[entry+8]` object takes
`r11d` at `+0xE4` - the field write the message arms apply
through the shared scan.
Interior anchor `002C9F67` (the `edx * 0x20` index).

`002C9E80` (41 B) is the out-pair getter `00280DE0` and
`00565E00` call: `r9 = [rcx+8]`, a non-null `rdx` receives
`movsx word[r9+0xEC]`, a non-null `r8` receives `movsx
word[r9+0xEE]` - the two-word fetch the scroll records
expose.
Interior anchor `002C9E8E` (the `+0xEC` read).

`002C41F0` (38 B) and `002C2F60` (38 B) are the twin
post-if-absent arms `00280DE0` and `002D70F0` call:
`002C41F0` posts command `0x7B0` with code `002C4460`
through `00244F50` only while `0209AC30`'s `+0x128` slot
is empty; `002C2F60` posts `0xAF8` with code `002C3560`
only while `+0x120` is empty - the two guarded
registrations the protocol keeps on the shared table.
Interior anchors `002C420B` and `002C2F7B` (the `ecx`
loads).

## SWE2-EC7-101 update (2026-09-20) - `0029F5D0` measured

`0029F5D0` (269 B) is the indexed emit `002435C0`,
`00243C00`, `00276D30` and `003C5910` call:
`word[rcx+0xA]` selects an `8`-stride record in
`[rcx+0x20]`, its two `0xFFF` nibbles stage with
`+0xC`/`+0xE` positions offset by `r8w`/`r9w`,
`byte[+0x39]`'s high nibble indexes the `[rbx+0x18]+0x30`
block's `word[+0x12]` table and the low nibble adds into
`byte[rdx+0x5C]`, then `002D8D10` emits the staged
record - the index-fetch-compose-emit the protocol's
widget arms share.
Interior anchor `0029F6CD` (the `002D8D10` call).

## SWE2-EC7-103 update (2026-09-20) - `00281A50` measured

`00281A50` (135 B) is the gated teardown sequence
`00280DE0` and `002D70F0` call: when
`byte[rcx + 0x40]` bit 6 is set it runs
`00291D40`, `00295CE0`, `00244F00` on
`[0209AC30]+0xF8`, `002CF870`, `005112A0`,
`002CF6F0`, `002C2D80`, `002C3D50`, `002C1300`,
then `00244F00` on `[0209AC30]+0x318` and clears
that slot, `00567750`, and tails `0027F2E0` - the
ordered shutdown the widget arms run. A clear bit
returns early.
Interior anchor `00281A77` (the first `00244F00`
call).

## SWE2-EC7-107 update (2026-09-20) - `00247260` + `00244700` measured

`00247260` (58 B) is the wrapper
`002778C0`, `002A69E0` and
`002C0BE0` call: it forwards
`[rsp + 0x68]` to `00247130`, and
only on a nonzero result rewrites
bits `0x3C00` of `dword[rcx + 0x80]`
from `[rsp + 0x60] & 0xF` - the
guarded nibble publish the widget
arms share.
Interior anchor `0024727E` (the
`0xFFFFC3FF` mask).

`00244700` (284 B) is the
`0208EAC0` table compaction
`002446E0`, `002448D0` and
`00245020` run: the `0208EBC8`-
counted pointer array is scanned in
reverse for `rcx`, each hit
shift-deletes and decrements the
count (`edx != 0` removes every
occurrence, else just the last),
then a forward pass deletes any
entry equal to its successor - the
remove-and-dedup pass the widget
tables share.
Interior anchor `00244740` (the
reverse-scan compare).

## SWE2-EC7-110 update (2026-09-20) - `001B23E0` measured

`001B23E0` (41 B) is the
five-dword setter `00184460`
and `001D76A0` run: `edx`,
`r8d`, `r9d` land at
`[+0x3AE8]`/`[+0x3AEC]`/
`[+0x3AF0]` and the two stack
arguments (`[rsp + 0x28]`,
`[rsp + 0x30]` at entry) land
at `[+0x3AF4]`/`[+0x3AF8]` -
the contiguous five-word
parameter block the widget
message record carries.
Interior anchor `001B23F4`
(the `+0x3AE8` store).

## SWE2-EC7-114 update (2026-09-21) - `0057CD40` / `0057C380` / `0057C340` / `00567690` measured

`0057CD40` (142 B) is the
record apply `00566680` and
`0057C480` run: null `rcx`
returns early, else
`00246AD0(qword[+0xD0])` and
`002470D0(rcx)` run, and when
`dword[+0x630]` carries bit
`0x4000` a `0x4000000040000000`
pair goes through `002CCCA0`
(keyed on `word[[+0x48]+2]`)
with the result parked at
`qword[+0xD8]` before
`002CD150(word[+0x44] + 1)`.
GS-cookie framed.
Interior anchor `0057CD77`
(the `+0x630` flag test).

`0057C380` (93 B) is the
registration shim `002CDF20`,
`002CE370` and `00566680`
call: a three-field stack
record (`0`, `rcx`, `edx`)
plus the `0057C480` body -
itself a `0057CD40` caller -
goes to `00244F50` under id
`0x640`, and the answer is
`qword[[0209AC30] + 0x328]` -
a table lookup of the
0x640-keyed entry.
Interior anchor `0057C3C4`
(the `+0x328` read).

`0057C340` (63 B) is the
release half `002CDF20`,
`002CE370` and `00566680`
run: when `dword[+0x630]`
carries `0x4000`,
`002CCB30(word[[+0x48]+0x16])`
frees the keyed resource and
`qword[+0xD8]` zeroes;
`00244F00(rcx)` then runs
unconditionally - the same
`+0x630` bit `0057CD40` sets
up behind.
Interior anchor `0057C366`
(the `+0xD8` clear).

`00567690` (180 B) is the
per-subrecord apply
`00564650`, `00566680` and
`0056C490` run: for each of
`byte[+0x150]` entries at
`+0xC8 + i*8`, a non-null
`rdx` parameter drives
`002D04F0` on the entry with
`edx` = `0x40` or `0x80`
selected by
`movsx byte[rdx+7]` against
`word[entry+0xD4]` (r8 = r9 =
1, stack arg `0x64`); the
tail then calls
`005670F0(qword[+0xC0],
rdx != 0)` - a list apply
that flags whether the
parameter was live.
Interior anchor `005676F1`
(the `+0xD4` compare).

`00579FA0` (150 B) is the three-counter clamp `00579230`/`00579420`/`00579AF0` share: maps `ecx` 0/1/2 -> 0/1/2 (anything else returns 0), then reads `0037E760(mode,4)`, `(mode,2)`, `(mode,0)` into `b`/`s`/`a`; returns `s+b` when `s+b <= a`, else `a` when `a >= s`, else `a+b` — a piecewise index bound over the mode's three counters.

Interior anchor `00579FDD` (function `00579FA0`).

`00579230` (186 B) is the row-position compute `00577E10` runs: `edi = [+0xC8]`'s `+0xF2 * +0xEC + +0xEE + +0xED` (pitch x count + margins); when `+0xC4` mode is not 1 the selected row is `00579FA0(mode) - edx - 1`; `00243260(this+0x50, 0, out)` resolves the base pair, then `out[0] += [this+0x98]` and `out[1] += [this+0x9A] + row*[[+0xC8]+0x100]` — writes the two output words of a list item's anchored position.

Interior anchor `0057928D` (function `00579230`).

`005791B0` (119 B) is the kind-mapped lookup `00579420` calls: when `+0xC4` mode is not 1 the index becomes `[[+0xC8]+0xE8] - edx - 1`; mode maps 0/1/2 -> 0/1/2 else `0xFF`, then `0037EAA0(idx, mapped)` -> `0037E5B0(result, &rec)` and the record's `+0xC` word is returned (0 when the lookup fails).

Interior anchor `00579203` (function `005791B0`).

`0037EAA0` (206 B) is the `[02AED490]+0xC8` table lookup `005791B0`/`00579420`/`00577C30` share: returns -1 when the table is absent; otherwise it walks the 8-stride entry array under the `[tbl+0xA]` count — an entry matches when its low byte equals `edx` (or `edx` is `0xFF`) and its `([ent] >> 8) & 0x3FF` key is accepted by `0046B1A0`, falling back to `0046B240`; `ecx` picks which match ordinal to stop at, and the hit's index is returned. (The `0046B1A0`/`0046B240` key predicates also serve the combat AI layer — shared fan-in on the test pair, not a widget relationship.)

Interior anchor `0037EB11` (function `0037EAA0`).

`00292B70` (993 B) is the measure core `0057BEE0`/`00564430`/`00293170` call: the `{kind, arg}` input must have `kind` in 1..0xE — kind 3 resolves `0035D330(6, arg << 16)`'s object, gates on `002CCA00([obj+0x38])`, and maps the `[+0x4C]` subkind to handler slots 1..5; kind 6 requires `002CCB00(arg >> 16)` and lands on slot 7; kind 0xA passes when `(arg >> 16) + 0x7FA0 <= 0x19F`. The `01E0C490[kind]` handler is invoked with `00295C20(kind)` plus a zeroed 36-entry qword array and a 0x200-byte scratch buffer it fills, the array is compacted, the caller context is marshalled through stack home space, and the tail `002B4090` extent is compared against `arg` — `0016D6A0(0x20000)` reports the overflow case. Returns 1 on success.

Interior anchor `00292D08` (function `00292B70`).

`0055FAA0` (64 B) is the `002D70F0` post arm for the board pair: a live `[0209AC30]+0x320` (the `0055CD40` view record) tail-enters `00247510(obj, 0x8002, 1)`, else a live `+0x158` takes `00247510(obj, 0x8002, 0)` — the close-teardown message the post-if-absent arm sends to whichever board object exists.

Interior anchor `0055FAC8` (function `0055FAA0`).

`00243860` (923 B) is the per-slot body `002D28E0` runs: `word[rdx+0x58]` gates the arm, `dword[rcx] & 0x3FFFC` and `al & 1` test the slot flags, `0029FE20`, `00249FD0`, `00364980`, `0020E600`, `002B3400`, `002B0280` and `002D8530` run the slot's emit under the cookie check - the shared record-walk's flagged per-slot step.

Interior anchor `00243AB3` (function `00243860`).

`00297880` (906 B) is the message body `0029A0A0` calls: `00247870` runs fifteen times across the frame - a single-callee field iterator over the widget record, cookie-checked - the protocol's densest `00247870` caller.

Interior anchor `00297969` (function `00297880`).

`00284EC0` (709 B) is the command battery the dispatcher `00285290` runs: `word[+0x120]`/`+0x11C` bitmask arms, `0209AC30`'s `+0xD8` object's `+0x40` bit 0x80000 cleared, then `002C1A80`, `00285A10` x2, `00249C60` x3, `002445A0` x2, `002470C0`/`002470D0`, `002C9EB0`, `00285B20`, `00284C90`, `001E0A10`, `0027E810`, `00285190` x2 - the message's widest arm fan-out.

Interior anchor `00284F3A` (function `00284EC0`).

`00285A10` (271 B) is the slot-select the command battery `00284EC0` and the dispatcher's siblings `00285190`/`00285290`/`00285B20` call: on `0209AC30`'s `+0xF8` object it clears bit 0 of `+0xFC` on the nine slots `+0xC0`..`+0x100` plus the prior `byte[+0x117]` selection, then for `ecx >= 0` writes `+0x117` = cl, `or`s `+0xFC` bit 0 on slot `rdi`, runs `002527B0(6, ...)`, stores `word[+0x114]` and `word[0209AC30+0xDE0]`, and ends in `0027F210` - the object's select-and-mark-dirty.

Interior anchor `00285AF5` (function `00285A10`).

`002445A0` (19 B) is the two-global publish `00281ED0`, `00284EC0` and `00285B20` all call: `0208F570` -> `0208ED54`, `ecx` -> `0208ED50` - the smallest shared-state copy in the batch, call-free.

Interior anchor `002445AC` (function `002445A0`).

`00243C00` (648 B) is the kind-dispatch walk `002D28E0` runs per element: `word[rdx+0x58]` gates the arm and `dword[rcx] & 0x3FFFC` counts the loop; each element's `dword[+8] >> 2 & 0xF` selects 2/4/7/9 to `002D9C40` (a word-field table fill on the stack record), `0029ED30`, `0029ED50` or `0029F5D0`, with `002D9380`/`002D9B00` finishing - the shared record-walk's per-element emitter.

Interior anchor `00243CA6` (function `00243C00`).

`0029ED30` (13 B) is the virtual tail-call `002435C0` and `00243C00` make through the record's `+0x18` slot - a non-null pointer is jumped, else straight `ret`.

Interior anchor `0029ED39` (function `0029ED30`).

`0029B1C0` (625 B) is the ratio-scaled emit `0029A0A0` calls: `rcx+0x60` -> `+0xE8` -> `+0x18` resolves the target record, `xmm8 = xmm11/12.0` and `xmm9 = xmm10/xmm8` clamped >= 1.0 derive the repeat scale, `0x80808080` and `0208F570` seed the emit record, then the `00808C40`/`00861F0E` loop lays out the scaled copies - the widget's proportional fill.

Interior anchor `0029B29F` (function `0029B1C0`).

`00284C90` (508 B) is the eligibility gate `00284EC0` calls: `[rdx+0xC0]` selects `0209AC30`'s `+0xAC8` table entry `rsi`, `word[rsi+0x60]` sign, `byte[rsi] & 2`, `0209AC30+0xD3C` bits 4/8 against `[rbx+0xFC]` bits 0x20/8, and `dword[rsi] & 0x20000` all veto before `[rbx+0xC8]` walks into `002468A0`/`00249C60`/`002D04F0` - the widget's visibility test.

Interior anchor `00284D58` (function `00284C90`).

`002994E0` (500 B) is the flag-gated emit `0029A0A0` calls: `[rdx+0xD8] & 0x20` and `[rdx+0xC0]` non-null gate, `[rdx+0xDC] - 1` dispatches against `ebx = 1`/`r8d = 3` building `{0x10000, 0x30002, ..}` words on the stack, then `00271AB0`/`271DB0`/`2998D0`/`35D460`/`00808C40` run - the widget's kind-stamped emit.

Interior anchor `002995A0` (function `002994E0`).

`002830A0` (464 B) is the call-free table scan `00284C90` uses: `0209AC30`'s `+0xD3C` bit 3 gates, `[+0xF8]` gives `r11`, a 9-entry loop over `+0xAC8` tests each `word[+0x60] >= 0`, `byte & 2` clear, `[r10+0xFC] & 8` set, `dword[+0x44] & 0x80000003` nonzero; then `byte[r11+0x117]`-indexed `+0xC0` slot's `+0xFC` bits 8/0x10 pick the final arm - the protocol's eligibility sweep.

Interior anchor `002830F0` (function `002830A0`).

`0027E810` (441 B) is the slot-table scan `00284EC0` calls: `001E0E30` returns a base, `0209AC28` counts and `0209AC30`'s `+0xF8` object gives `r11`; `byte[r11+0x117]` zero gates on `ebp`, `byte[r11+0x118]` (signed) indexes the `+0xC0` slots, and the loop walks them - the protocol's indexed-slot sweep.

Interior anchor `0027E828` (function `0027E810`).

`002996E0` (429 B) is the gated handler arm `0029A0A0` calls: `byte[rdx+0xD8] & 0x40` and `[rdx+0xC8] != 0` gate, `word[rdx+0x116]`/`word[rdx+0x11A]`/`word[rcx+0x58]` carry the counters, `009162D8` supplies a bound, and `00271AB0`/`00271DB0`/`0035D460`/`002998D0` run the arm - the protocol's counted-message path.

Interior anchor `00299768` (function `002996E0`).

`002998D0` (350 B) is the packed-field decoder `002996E0`/`002994E0` call: `word[rbx+0x32]` selects a `word[rbx+rax*2+0x14]` entry whose `byte[r10+r11*8+7]` nibbles index `byte[rdx+rax]`, `al + low-nibble` writes `byte[rcx+0x5C]`, `word[r10+r11*8]` masks `0xFFF`/`0x7FF`, then `002D8C80` runs - the protocol's nibble-table decode.

Interior anchor `00299A14` (function `002998D0`).

`00271DB0` (156 B) is the call-free rect union `002996E0`/`002994E0` call: four signed word pairs `[rdx]`/`[+2]`/`[+4]`/`[+6]` vs `[r8]` merge by `cmovl`/`cmovge` min/max into `[rsi]`..`[+6]` - the protocol's bounds-merge primitive.

Interior anchor `00271DF4` (function `00271DB0`).

`00285CB0` (421 B) is the id-dispatch `00285190`/`00285290`/`00285B20` call: `movsxd [rcx+0xC0]` indexes `0209AC30`'s `+0xAC8` 8-stride table into `rbx`, `[[r8+0xD8]+0x268]` gives the message id, `0x4B3`/`0x4B4`/`0x4B6`/`0x4B9` pick the arm, and `002F9860(0xCED)`/`002F9860(0xCE0)`-family string fetches with `00291D80`/`00291D70` run each - the protocol's four-id handler.

Interior anchor `00285D15` (function `00285CB0`).

`00285B20` (397 B) is the dispatcher `00284EC0` calls: `rbx = [0209AC30 + 0xF8]` (the active widget), `word[rbx + 0x110] = cx`, and `ecx` switches five arms run by `002445A0`/`002470D0`/`002C9EB0`/`002470C0`/`00285A10` - one arm calls `00285CB0` (the `0x4B3`/`0x4B4`/`0x4B6`/`0x4B9` handler) - the protocol's outer dispatch.

Interior anchor `00285B8F` (function `00285B20`).

`003EEBD0` (388 B) is the frame normalizer `003EE420` calls: `[01DFE0B4] * 0x2580` divided by 100 (magic `0x10624DD3`, `shr 6`), `cvtsi2ss` then `1.0f / count` gives the step, `[rcx + 0x1D0]` adds or subtracts it by `edx`, `minss` clamps to 1.0f - the 9600-tick rate conversion the icon path uses.

Interior anchor `003EEBF4` (function `003EEBD0`).

`00293170` (381 B) is the record builder `00293100`/`00293110` call: `[0209AC30 + 0x2F8]` non-null gates, `00861EC0` clears the `0x270` frame, and `00247570` x3, `00244DD0`, `00292B70`, `00244F50`, `00247510`, `00246AD0` fill it - the protocol's counted message-record constructor.

Interior anchor `002931C8` (function `00293170`).

`00297710` (361 B) is the tier setter `0029A0A0` calls: `r8d` clamps to `[rdx + 0x28]`, `< 0x64` -> 1, `>= 0x3E8` -> 3 else 2; unchanged `byte[rcx + 0xDC]` returns 0, else the tier is stored and nine `00247870` calls propagate it - the protocol's rate-class update.

Interior anchor `00297776` (function `00297710`).

`003EED60` (340 B) is the scaled decrement `003EE420` calls: `[rdx + 0x88]` float > 0 gates; `word[r8 + 0x58]` through `cvtdq2ps`, x `xmm3` x `xmm1`, `cvttss2si` back into `[r8 + 0x58]`; `r9 = rdx + 0xA0`, `002D8650` x2 and `002B3120` - the widget's scaled field tick.

Interior anchor `003EEDF4` (function `003EED60`).

`00297FE0` (321 B) is the flag commit `0029A0A0` calls: clears bit0 of `dword[rax+8]` on the `[rcx+0x60]+0x30` node, writes `[rdx+0x44]` into `rcx+0xF0`, runs the status cycler `00272F60`->`00272F80` over `rcx+0xF0` with period `0x1E` (`edx`, frames per step - not a posted message), then the `rsi+0x100` presence XORs with `rbx` and, when present, `002F9860` on `dword[rax+0x98]+0x46B7` resolves the label - the widget's show-state publish. (Corrected 2026-09-27, GA-1: `0x1E` is the cycler's period argument, not a message id.)

Interior anchor `00298036` (function `00297FE0`).

`0029AFE0` (319 B) is the alpha ramp `0029A0A0` calls: `byte[rdx]&0x80` arms the ticker - `r8d` nonzero sets `word[rcx+0xD8] |= 0x100` and `word[+0xDA]=0x80`; otherwise the `0x200` bit selects fade-in (`+0xDA -= 0x40`, floor `0x80`) or fade-out (`+0xDA += 0x40`, cap `0xFF` clearing `0xFDFF` bits off `+0xD8`), with `r9 = [rcx+0x60]+0xB8` as the write target - the widget fade the message protocol drives.

Interior anchor `0029B061` (function `0029AFE0`).

`00247130` (303 B) is the ramp setter `00247260` calls: `byte[rcx+0x80]&0xD` or `(sword[+0x9C], sword[+0x9E]) == (edx, r8d)` early-outs; else `+0x80 |= 2`, `&= ~0x300`, `(r9d&3)<<8` merges in and `bts 0xA` arms it; `word[+0x88]`/`+0x8A` take the old endpoints, `+0x84`/`+0x86` the accumulated sums, `+0x8C`/`+0x8E` the deltas, and `dword[rsp+0x50] x 0x3C` magic-divides (`0x10624DD3`/`sar 6`, ms -> 60 fps frames) - the widget's endpoint-interp arm beside `0029AFE0`'s ticker.

Interior anchor `002471C5` (function `00247130`).

`00297D10` (251 B) is the rescale-and-forward `0029A0A0` runs: `edx` mismatched against `[rcx+0xE0]` (or `[rcx+0x108]` non-null) proceeds - `00271FB0` byte-tests `r8d`, the `0x80808080`/`0x40`/`0x80` path rescales the three-byte `[rsp+0x48]` triple by `al x (0x40|0x80) >> 7` per lane, then `byte[rdi+0xDC]` picks an s16 of `00916300` whose `x8` row of `[[rdi+0xC0]+0x60]` becomes `rsi` for `0029F6E0(rsi, +0xDC + 1, 0)` - `1` when forwarded, `0` on the early-out.

Interior anchor `00297D62` (function `00297D10`).

`00271FB0` (320 B) is the 32-row bitmask aggregate `00297D10` runs first: `0035D490(ecx)` resolves the context and `edx - 1` picks one of its `+0x1500`/`+0x1700`/`+0x1600`/`+0x1800` 32-entry pointer tables; per row `bt edi, [rdx+0x98]` gates (index `0x1D` additionally requires bit `0x10`), a `ebx - 1`-selected byte of `+0x21`/`+0x23`/`+0x22`/`+0x24` must differ from `0xFF`, and `byte[+0x25]`'s `& 2`/`& 4`/`& 8` bits are folded through `cmove`-or-`1/4/8` pairs into the `esi` mask - the capability word the rescale test consults.

Interior anchor `00271FCD` (function `00271FB0`).

`00297C10` (244 B) is the `0209BFBE`-bank lookup `0029A0A0` runs: rows stride `0xC0` from `0209BFBE` to `0209C2BE`, a row qualifies when its `-0x58`/`+0` flags carry bit `2` and `dword[+0x32] == [rsi+4]`; the hit path pairs `003F89C0` with `0028F590`, then `003F8A50` with `0028F590`, and commits `[rdi+0x48] = rsi`, `[rdi+0xA0] = rsi`, `[rdi+0xB0] = ecx` - the static-table widget resolve.

Interior anchor `00297C9A` (function `00297C10`).

`00285190` (241 B) is the `0209AC30`-object indexed fetch `00284EC0` runs: `[+0xF8]` non-null gates, `movsx byte[+0x117]` (bit `0x10` of `dx`/`cx` walks it down or swaps to `+0x118`) indexes `[r8 + rax*8 + 0xC0]`, and the non-null pointer earns `002445C0` then `00285A10`/`00285CB0`/`00249C60` in sequence - the counted-slot dereference the protocol calls.

Interior anchor `0028523E` (function `00285190`).

`00297E70` (238 B) is the s16-table row commit `0029A0A0` runs: `[rcx+0x100]` non-null, `dword[rcx+0xE4] == edx` with `edx >= 0xA`, and `r8d` zero all gate the early-out; otherwise `byte[rcx+0xDC] + 1` selects a `00916308` four-s16 row (`0004 0003 0002 0000` at the head) whose fields pair with the `+0x100` object for `0029F6E0` - `1` on commit, `0` when gated.

Interior anchor `00297F44` (function `00297E70`).

`00394690` (28 B) is the row-array reader the widget procedures share: `u16([rcx+0x50] >> 2)` bounds the index and `qword[[rcx+0x60] + rdx*8]` returns row `edx` (0 on overflow) - the object's child-row fetch.

Interior anchor `0039469D` (function `00394690`).

`00394660` (41 B) is the filtered row read paired with `00394690`: the same `+0x50`/`+0x60` bounds and array, then only rows whose `byte[+8] & 0x3C` equals `4` return `qword[row+0x18]` - the flagged-payload fetch `00407F90`'s family runs.

Interior anchor `00394674` (function `00394660`).

`002B6AE0` (99 B) is the paired-clamp setter: `word[+0xC8]`/`word[+0xCC]` copy to the stack, `002B69B0(&w1, &w2, rcx, edx)` clamps the pair against the record, the sign-extended results write back to `+0xC8`/`+0xCC` and `edx` lands `+0xD4` - the cursor-pair commit.

Interior anchor `002B6B17` (function `002B6AE0`).

`002B7210` (578 B) is the scroll-window adjust: `+0xC8`/`+0xCC` copy into `+0xE8`/`+0xEA`, `002B69B0` clamps `+0xE4`/`+0xE6`, then `0x51EB851F` (/100) scaling turns `word[+0xD0]`/`+0xD2`/`+0x9C`/`+0x9E` into half-extents floored at `0x18`; the `+0xF8`..`+0x104` rect re-centres on the cursor with edge flags in bits 0-3, and the result merges into `dword[+0xE0]` (bit 3 = cursor off-centre, bit 0 = position changed) beside `+0xDA`/`+0xDC` copies and `+0xD8 = 0x100` when the target moved - the list viewport reconcile.

Interior anchor `002B725F` (function `002B7210`).

`002481A0` (18 B) is the paired flag poke three widget/settings callers run: `dword[0208ED5C]` xors with 1 and `dword[0208F560]` sets to 1 - the two-global toggle that flips a widget state bit and marks the paired word dirty in one call.

Interior anchor `002481A7` (function `002481A0`).

`002904D0` (36 B) is the null-gated forward off the `0209BE80` singleton: `qword[[0209BE80] + 0x10F78]` loads the manager sub-object (returns 0 when unset), then tail-jumps `00297170(obj, rcx_arg, edx_arg)` - the guarded `+0x10F78` lane dispatch.

Interior anchor `002904E9` (function `002904D0`).

`002907F0` (76 B) is the widget-list notify sweep: `rbx = qword[[0209BE80] + 0x10F20]` heads the list, each node whose `dword[+0x980]` differs from the caller's `edi` receives `003F3080(node, 1)`, and the walk advances through `qword[+0x9B0]` - the skip-self broadcast across the `+0x10F20` widget chain.

Interior anchor `00290810` (function `002907F0`).

`00290CD0` (21 B) is the thin `0209BE80` lane forward: `rcx = qword[[0209BE80] + 0x10F40]`, the caller's `ecx` moves to `edx`, and the body tail-jumps `003F35A0` - the `+0x10F40` object dispatch.

Interior anchor `00290CD9` (function `00290CD0`).

`002CCA00` (12 B) is the kind-window predicate `00292B70`'s measure core gates on: returns 1 iff `(ecx - 0x17)` unsigned `<= 3` - `ecx` in `0x17..0x1A` - else 0.

Interior anchor `002CCA05` (function `002CCA00`).

`00243E90` (80 B) is the element-flag sync pass over a counted pointer array: `([rcx] >> 2) & 0xFFFF` counts the entries at `qword[+0x10]`, and each element's `dword[+8]` bit 0 is rewritten to match bit 28 of `dword[[elem]]` - the per-row class-bit replication the layout and widget callers run after a rebuild.

Interior anchor `00243EB0` (function `00243E90`).

`00249320` (43 B) is the class-3 node factory: `00249210(rcx, rdx, r8, 3, 0)` builds the node, `00249660` installs at `qword[+0x10]` as its dispatch slot, and `qword[+8]` returns - the fixed-vtable-3 create the widget caller `003933F0` and the title-asset consumer `00393FF0` share.

Interior anchor `00249337` (function `00249320`).

`0028F590` (18 B) is the `0209BE80` singleton's `+0x80` accessor: returns `qword[[0209BE80]] + 0x80` when the manager is live, 0 otherwise - the two-instruction guarded lane the HP write and the widget caller share.

Interior anchor `0028F59D` (function `0028F590`).

`002B6950` (95 B) is the 24px-cell rect builder: writes `{x = edx - r9d - 0x18, y = r8d - arg5 - 0x18, w = 0x18, h = 0x18}` to `rcx`, then when a raw span exceeds 24 it re-centres on the halved edge pair (`(edx>>1) - (r9d>>1)` / `(r8d>>1) - (arg5>>1)`) so the cell sits mid-line - the icon-cell geometry the two widget callers share.

Interior anchor `002B6972` (function `002B6950`).

`002B69B0` (301 B) is the percent-position pair: each axis computes `((word[r8+0x9C or 0x9E] >> 1) - dword[+0xC8 or +0xCC]) * 100 / dword[+0xD4]` then scales by `r9d` through the `0x66666667` magic-divide by 10 with round-half-up on the remainder (the `*q - q*10 >= 5` bump); the centred residual words land at `[rsi]` and `[rdi]` - the percent-to-pixel converter the two widget callers share.

Interior anchor `002B69E4` (function `002B69B0`).

`00403600` (51 B) is the metric-pair copy: `dword[rcx]` clears, `word[+4]` takes the `qword[rdx+0x20]` record's `+0x14`, and `word[+6]` takes `trunc(word[+0x16] * 1.75)` - the row-height emit the two widget callers share.

Interior anchor `00403622` (function `00403600`).

`0027B880` (646 B) is the menu-command executor inside `002778C0`'s loop: an empty `[rcx+0x40]` runs the reset chain `00290CD0`/`003C94F0`/`0035C080`/`002907F0`; otherwise the `[rbx]` tag dispatches through the 22-case jump table at `0027BB08` - flag-gated cases pull the per-slot u16 at `[rbx + idx*8 + 0x50]` into `0035D330` lookups (categories 0x14, 0x15, 0x18 and 4 by case), and every live arm tails into the `0035C140`/`0027C150` -> `002F9860`/`0035C150` + `00290C60`/`00290C80` chains that push the resolved record back to the widget.

Interior anchor `0027B95E` (function `0027B880`).

`0028E840` (27 B) is the singleton widget forwarder both `0027B880`'s menu-command dispatch and the layout-parameter system reach: it passes the caller's value on in `edx` and tail-jumps to `002BE090` with `rcx = [0209BE80] + 0x8FA0` - a silent no-op while the singleton is absent.

Interior anchor `0028E84C` (function `0028E840`).

`00407B70` (279 B) is the position-delta apply `00407590` runs: two `00394690` lookups fetch the source and target records, `003C5FB0` decides their order (a true result swaps them so `rbx` is the effective base), the `+0xC`/`+0xE` signed shorts diff into a local pair delivered through `002E04E0`, the receiver `[rbp+0xC8]` gets `+0x98`/`+0x9A` stamped, and when `0208EA28`'s `+0x44` flags read `& 0x180000 == 0x100000` the same deltas accumulate into that object's `+0x54`/`+0x56`-biased `+0x98`/`+0x9A` before a `[rdx+0x18]` chain walks `00407C90` per link

Interior anchor `00407BEF` (function `00407B70`).

`003F89C0` (99 B) is the registry-entry initializer `00296360` and `00297C10` run: `00861EC0` zeroes the `0x58`-byte record, `+0x26` gains bit `0`, the caller's fifth argument (a function pointer) lands at `+0x38`, `r8d` at `+0x40`, `r9` at `+0x48` - and a non-null `+0x38` callback is invoked immediately as `fn(record, 0, edx)`

Interior anchor `003F89FB` (function `003F89C0`).

`003F8A30` (23 B) is the head unlink `002962D0` and `00296360` run on the `+0x28`-chained list: when the list head `[rcx]` is `rdx` it is first popped to `[rdx+0x28]`, then the body tails `003F8BF0` on `rdx` - head-pointer repair plus per-node teardown in the callee

Interior anchor `003F8A3C` (function `003F8A30`).

`003F8A50` (58 B) is the tail append `00296360` and `00297C10` run on the `+0x28`-chained list: an empty `[rcx]` takes `rdx` as head, otherwise the chain is walked to its tail which `+0x28`-links `rdx` and leaves the old tail at `rdx+0x30`; both paths set the new node's `+0x26` bit `1` - the enqueue counterpart to `003F8A30`'s unlink

Interior anchor `003F8A70` (function `003F8A50`).

`00282FC0` (217 B) is the two-pass flag sweep `00285290` runs over the `0209AC30 + 0xAC8` nine-slot widget table: pass one marks `+0xFC |= 0x10` on the `+0xF8`-based record of any live slot whose `+0x60` s16 equals `003271D0()`'s result; pass two marks `+0xFC |= 0x20` on live slots whose `*slot` has bit `1` clear and bit `0xA` set - focused-widget highlight and arm flags in one sweep

Interior anchor `0028301D` (function `00282FC0`).

`00274BD0` (206 B) is the bounded unlink pass the battle-menu dispatcher `002778C0` runs over a node list: it walks `[node+0x18]` links up to `r8d` steps, calls each node's `[node]` thunk with `[node+8]`, and on `== 1` splices the node out (prev's `+0x18` / next's `+0x10`, then both cleared) while remembering the first non-matching node as the fallback return - the 'drop handled nodes' sweep

Interior anchor `00274C3C` (function `00274BD0`).

`003EF680` (201 B) is the `dl == 3` initialiser `003EF830` dispatches to: it `00244F00`s the `[rcx+0xE0]` child, `00250C50`/`00251EA0`-arms the `[rdi+0xD8]` record with `+0xC8 = 4`, `+0xCC = 0xB4`; if the `[rdi+0xD0]` record's `+0xC4` bit 0 is clear it runs `002DEC00`/`002DEE50`/`003611F0`/`003634B0` and stamps `+0xC0 = 6`, `+0xC8 = 0xF0`; it always ends with `[rdi+0xC4] = 0x3C`, `[rdi+0xC0] = 5`

Interior anchor `003EF6CA` (function `003EF680`).

`00271EF0` (192 B) is the pulsing-highlight colour `00297D10` computes for a flagged message: `cl & 0x18` unset returns flat `0x80808080`; set, it converts the `0208F570` tick to a sine via `00861F0E` (`tick * pi / 30`), scales `* 32.0 + 128.0` into the amplitude byte `edi`, picks base colour `0xB5` or `0xB6` through `002DD7E0` by `cl & 0x10` versus `cl & 8`, then rescales each channel `* edi >> 7` - a time-driven brightness modulation for highlighted rows

Interior anchor `00271F0A` (function `00271EF0`).

`0029B490` (187 B) is the clamped palette pick `0029A0A0` runs on a widget: it materialises the six-entry byte table `{0x04, 0x16, 0x19, 0x05, 0x19, 0x05}` on the stack, resolves the `[rcx+0x60] -> +0xE0 -> +0x18 -> +0x60 -> [0]` chain into the target record `r8`, adjusts `[rcx+0x128]` - `edx` nonzero increments it, saturating at `0xB`, else decrements floored at 0 - halves the result, and writes the picked byte into `[r8+0x2C]`: a saturating counter driving a six-step brightness ramp

Interior anchor `0029B4F1` (function `0029B490`).

`00244640` (149 B) is the focus-stack push `002470D0` runs on `0208EAC0`/`0208EBC8` (this page's L974 accounting): when the depth word is `0x20` it first compacts - seven `0x20`-entry shifts drop the oldest record, depth decrements to `0x1F` and `0208EBB8` clears - then `rcx` lands at `0208EAC0 + depth*8` and `0208EBC8` increments; a 32-deep bounded qword stack with drop-oldest eviction.

Interior anchor `002446CA` (function `00244640`).

`00244500` (146 B) is the clock-window easing calculator `00242C90` runs over the `0208F570` message clock: `0208ED50` armed, delta `0208F570 - 0208ED54` in `[8, 0x50)` lerps `cl/2` by `(0x50 - delta)` through `00248F40`, `[0x54, 0x9C)` runs the second arm on `cl/2` with `r8 = delta - 0x54`, `>= 0x9C` resets `0208ED54` to the clock, and everything else returns `cl` - the ramp shape the message protocol's `0208F570` arithmetic already describes.

Interior anchor `0024453F` (function `00244500`).

`0029AE50` (145 B) is the child-select `00297170`'s lane dispatch uses: `edx` bounds-checks against `dword[[rcx+0xB50]+0x40]`, reads `dword[+0x50 + edx*8]` as the target id, then scans `0035BB60`/`0035BB00`-sized sibling slots for a matching element; the found index `bl` lands at `byte[rdi+0xB48]` and sets bit 2 of `word[+0x318 + bl*0x160]` - on any miss `+0xB48` is cleared - the index-resolve that turns a selector arg into a lane mark.

Interior anchor `0029AE77` (function `0029AE50`).

`0027DC10` (144 B) is the guarded submit `002778C0` calls: `edx` must be non-zero, `00290CD0(edx)` validates it, `0031AB80(edi, ebx, bp, &rsp+0x20)` must come back non-negative with `dword[out+8] == 1` and `esi == 0`, then `00273710(ebx)` non-null releases `0028EA20(ebx, dword[out], xmm2)` - the five-condition hand-off the protocol's submit path enforces.

Interior anchor `0027DC56` (function `0027DC10`).

`00296FB0` (143 B) is the easing calculator `0029A0A0` calls: `00229DF0` gates it, `00229E70`'s result reciprocates into `xmm1` (1.0 on the miss arm), then `(float)dword[0208F570] * xmm1 - (float)r8d`, `* 3.14159` (`01CEBC50`), `/ 00916314`, through `00861F0E`, `* (float)ecx`, `+ edx` - the `0208F570`-clocked angular ease the widget frames consume, sibling to `00244500`'s clock-window read.

Interior anchor `00297008` (function `00296FB0`).

`0031AB80` (88 B) is the mode-gated resolver `0027BD80`/`0027DC10`/`002778C0` call ahead of `0031AA30`: `byte[02089340] & 0x10` is required, then `003588B0` resolves the mode object and `00263E30` walks it to its `+0x698` child; a complete chain tail-jumps `0031AA30(child, 0, edi, rbx)`, while any missing link or the flag clear returns `0xFFFFFFFF` - the battle-mode-gated hand-off the widget submit family shares with the ladder's availability gate.

Interior anchor `0031ABAE` (function `0031AB80`).

## DD batch 10: the three unparsed rows and the last two receivers of 26 (SWE2-CONTRACT for OPUS)

*For the player:* nothing changes on screen. Every menu object's reaction to every message the game sends is now
read: three objects forward everything to the "do nothing" default or to a shared base, and no list lifts its clip by
its own answer to message 26. The checks are in
[`b10_checks.py`](../../_index/candidates/swe2contract-ddres-b10-0930/b10_checks.py) (W1–W4), static, on the shipping
image.

- **The table (W1).** `widget-message-handlers.tsv` holds 267 rows: 264 `exact`, 3 `unparsed`, and no upper-bound
  row. The status line's "24 UNPARSED" was the 2026-09-15 regeneration's count (§3).
- **The three unparsed rows (W2–W3).**
  - `005C5230` is `33 C0 C3`, which returns 0 and does nothing. It is the default arm of every other row.
  - `0017CDE0` is `jmp 005C5230`.
  - `002985C0`, planted by `lea` in `00298250` (`0029848B`), is `jmp 003EE420`. `003EE420` (1,171 B) is not a row
    of the table. Its id chain (`003EE42D`–`003EE452`) answers **1, 2 and 4** and tail-jumps every other id to
    `005C5230`. The same chain decoder reproduces the table's ids for `002D2DB0` (1, 2, 4, 5, 26) and `0027AD70`
    (1, 4, 12, 18), and those are its controls. `0027AD70` also reaches `003EE420` by tail jump
    (`0027ADBF`, `0027AE55`, `0027AE5A`), so `003EE420` is a shared base procedure as well as `002985C0`'s body.
- **Message 26's last two receivers (W4).**
  - `002D2DB0` takes 26 on its chain (`002D2DFF`). It loads its `+0xC8` delegate and, when that delegate has a
    handler, calls it with the same message and returns its answer (`002D2E11`–`002D2E2D`). With no delegate it
    returns 0 (`002D38C9`).
  - `005691E0`'s jump-table arm for 26 (`00569ED4`) calls `00568FE0(self, msg.b, (int)msg.a)`. That function
    writes the cell position into the list's `+0x114` / `+0x116` and returns 0 on both of its exits (`0056902E` /
    `0056903A`, `005691C8` / `005691D4`).

| claim | evidence | tier |
|---|---|---|
| 264 exact, 0 upper bound, 3 unparsed | W1 (the TSV) | 1 |
| the three unparsed bodies; `003EE420` answers 1, 2, 4 | W2–W3, two decoder controls | 1 |
| 26 at `002D2DB0` is the delegate's answer; at `005691E0` it is 0 | W4 | 1 |

## DD batch 17: the body's remaining residue sentences (SWE2-STRUCT for OPUS)

*For the player:* nothing changes on screen, but five behaviours are now read. A menu slide always lands, whatever
easing curve it uses. A window told it has the focus also learns whether it took the focus or got it back when the
window above it closed. A map window's "re-read your fields" notice makes it rebuild its cursor box and keep the
cursor inside it. A list that lays its cells out with the per-cell hook places each cell where its owner said. And
the "load finished" message is sent from seventeen functions in the game's screens besides the framework. The checks are in
[`b17_checks.py`](../../_index/candidates/swe2struct-ddres-b17-0930/b17_checks.py) (125 PASS, FAILS 0), static, on
the shipping image. The record is
[`swe2struct-ddres-b17-0930`](../../_index/candidates/swe2struct-ddres-b17-0930/README.md).

**Message 16's seventeen application senders (C2–C5).**

| sender | receiver | record |
|---|---|---|
| `002A1FB0`, `00553F40`, `00558FB0`, `00561390` | the sender's own widget | `{16, 0, 0}` |
| `003CB0C0` | the `0x1E0` child it has just built at its own `+0xC0` and linked | `{16, 0, 0}` |
| `002B6570`, `002BA040` | `[0209E5C0]`, `[0209E5F0]`, after setting their `+0x179D2` bits 0–1 | `{16, 0, 0}` |
| `003C2100` | the object at its argument's `+8` | `{16, 0, 0}` |
| `00577BD0` | `[02CA9730]` | `{16, 0, 0}` |
| `0037F1F0`, `00577180` | the object at `+0xC0` | `{16, 1, 0}` (record `00915BB0`) |
| `0037F340` | the object at `+0xC0` | `{16, 8, 0}` (record `00D111C0`) |
| `0037F4D0` | the object at `+0xC0` | `{16, 9, 0}` (record `00D111D0`) |
| `0037E4F0(w)` | `w`, which it also stores at `[02AED490] + 0xC0` | `{16, 9, 0}` (record `00D111D0`), or `{16, 10, 0}` (record `00D111E0`) when `[02AED490] + 0xE0` bit 7 is set |
| `003BC3E0(w, code)`, `005770A0(w, code)` | the widget passed in | `{16, code, 0}` |
| `0037F190(w, rec)` | the widget passed in | `{16, rec[1], word rec[4] when rec[1] is 2, else 0}` |

So the framework's "batch complete" is `{16, 0, 0}`, and screens reuse the id for their own completion notices, some
with a code. The field-map container is one reader of such codes (0x100–0x102, from its loader through `003BC3E0`;
[`swe2struct-residue3-0930`](../../_index/candidates/swe2struct-residue3-0930/README.md) W3–W5). What a non-zero
code means is each receiving screen's, as for 30.

| claim | evidence | tier |
|---|---|---|
| no curve kind decides whether channel 0 finishes: `00248F40` returns exactly 1.0 at or past the duration, before reading the kind | E1–E4 | 1 |
| 8's flag: 1 from the teardown pop (focus returned), 0 from the push (focus taken) | F1–F3 | 1 |
| `002B6DB0` is `002B7B80`'s base procedure; its id-14 arm sends 29, and its id-29 arm re-clamps the cursor | S1–S4 | 1 |
| 26's receivers write into the grid list that sends 26: their `+0xD8` is the list their layout built, whose delegate they are | L1–L9 | 1 |
| 16: 20 sites, 3 framework and 17 application; 16 is still the most widely sent application id | C1–C5 (control: 163 sites and 49 ids) | 1 |
| `+0x40` bit 5 is set by the root procedure and copied down at attach | B1–B3 | 1 |

## Interior citations for the entry-cited functions (OPUS, 2026-10-01)

*Functions this page named only at their entry. Each was read from the certified image; the sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`widgetmsg_interior.py`](../../_index/candidates/opus-widgetmsg-interior-1001/widgetmsg_interior.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001E9F00` | 42 B | stores `edx`, `r8d` and `r9d` in dwords `+0x13A0`, `+0x13A4` and `+0x13A8`, the fifth argument in `+0x13AC` and the sixth argument's low byte, zero-extended, in `+0x13B0` | `001E9F04`, `001E9F0F`, `001E9F15`, `001E9F1B`, `001E9F22` |
| `002418E0` | 14 B | copies bit 0 of `edx` into bit 5 of dword `+0x40` | `002418E4`, `002418E7`, `002418EA` |
| `00244610` | 13 B | compares two dword pairs: returns dword `[rdx]` minus dword `[rcx]` when that is non-zero, else dword `rcx+4` minus dword `rdx+4` | `00244612`, `00244614`, `00244616`, `00244619` |
| `002446E0` | 32 B | calls `002448D0(rcx)`, then tail-calls `00244700(rcx, 1)` | `002446E9`, `002446EE`, `002446FB` |
| `002478D0` | 78 B | for a non-null `rcx`, copies bit 0 of `edx` into bit 18 of dword `+0x40`, then calls itself with the same `edx` on each child, starting at qword `+0x18` and following qword `+0x20` | `002478DA`, `002478F1`, `002478F4`, `00247905`, `0024790A` |
| `00250C50` | 65 B | when qword `020927F0` is non-null, writes into that object: byte `+0x129` = `cl`, word `+0xE6` = 7, dword `+0x12C` = dword `0208F570`, word `+0x12A` = `dx`, dword `+0x124` = 0 | `00250C61`, `00250C68`, `00250C76`, `00250C7D`, `00250C85` |
| `00251EA0` | 57 B | when qword `020927F0` is non-null, writes into that object: float `+0x134` = `xmm0`, dword `+0x13C` = dword `0208F570`, word `+0x13A` = `dx`, dword `+0x130` = 0, byte `+0x138` = `r8b` | `00251EB2`, `00251EBA`, `00251EC0`, `00251EC7`, `00251ED1` |
| `0027BD80` | 91 B | calls `0031AB80(rcx, 0, dx, &out)` with a stack record `out`; returns its float `+0x10` when the call returns a non-negative value and its dword `+8` is 1, else 0.0 | `0027BD97`, `0027BD9E`, `0027BDBC`, `0027BDC3` |
| `0027C150` | 112 B | maps `ecx` 7 to 27 through a 21-entry jump table: 7 to 0xC92, 8 to 0xC94, 9 to 0xC95, 10 to 0xC96, 11 to 0xC93, 12 to 0xC91, 14 to 0xC90, 22 to 0xC8A, 23 to 0xC8B, 24 to 0xC8D, 25 to 0xC8F, 26 to 0xC98, 27 to 0xC99; every other value to -1 | `0027C153`, `0027C156`, `0027C16C`, `0027C1BC` |
| `0027D700` | 54 B | calls `0027B200(rcx)` first when `r8d` is 0, then tail-calls `0027B770(rcx, dword +0x510 + 8*r8d, r8d)` | `0027D710`, `0027D715`, `0027D71A`, `0027D731` |
| `0027E4E0` | 72 B | returns 0 when `0027B770(rcx, r8d, -1)` returns 0; otherwise calls `0027AF00(rcx, rdx)` and returns 1 | `0027E4F2`, `0027E4F9`, `0027E513`, `0027E51D` |
| `0027E7B0` | 89 B | returns 0 when bit 15 of dword `+0x1528` is set; otherwise calls `0027B200(rcx)` when `r9d` is non-zero and returns 1 when `0027B770(rcx, dword +0x510 + 8*r8d, r8d)` is non-zero, else 0 | `0027E7BA`, `0027E7DE`, `0027E7E3`, `0027E7F0`, `0027E7FE` |
| `00290C60` | 27 B | when qword `0209BE80` is non-null, tail-calls `002BE270(it + 0x8FA0, ecx)` | `00290C62`, `00290C6E`, `00290C75` |
| `0029BB40` | 316 B | for slots 0-3: when `00273A20` on the 0x160-byte record `+0x240 + 0x160*slot` returns 0, reads byte `+0xB44 + slot`; for a value 1-3 it builds a node with `00245000(that record, 0x160, 0029A0A0, &{0, slot, value})`, stores `rcx` in the node's qword `+0x120`, calls `00244960(rcx, node)` and `00246AC0(node)` and clears the byte; otherwise, when `0035BB20(slot)` returns a record with word `+0x60` and dword `+4` not negative, sets the byte to 2 when bit 1 of its dword `+0` is set, else to 3 or 1 by its bit 2, and the result becomes 1. Returns 0 when no slot took that last path | `0029BB95`, `0029BBDA`, `0029BBE8`, `0029BC09`, `0029BC35` |
| `002C9B30` | 116 B | clamps `ecx` to 0-6 and selects the 16-byte record `009170C0 + 16*ecx`; by `edx` through a 9-entry jump table returns its signed byte `+0` to `+5` (0-5), its float `+8` truncated to an integer (6), its signed byte `+0xC` (7) or the low dword of the record's address (8); 0 for any other `edx` | `002C9B34`, `002C9B3E`, `002C9B44`, `002C9B6B`, `002C9B90` |
| `002D1420` | 180 B | by the kind in dword `[rdx]`: 1 returns 0. 4 calls `002D2600(qword rcx+0x38, rcx)` when bit 25 of dword `+0xE0` of qword `+0x10` of `rcx` (of address 0 when `rcx` is null) is clear, else `002D28E0` with the same arguments, then zeroes dword `02CA8F30` and returns 0. 17 clears bit 27 of dword `+0xE4` of that object when qword `rdx+8` is 1, and returns 0. Any other kind sets dword `02CA8F30` to 1 and tail-jumps to `005C5230` with the same arguments | `002D1437`, `002D143F`, `002D1477`, `002D14AE`, `002D14C1` |
| `002E04E0` | 95 B | clamps `ecx` to 0-7 and selects the 0x68-byte record `0215F200 + 0x68*ecx`; when its dword `+0x60` is 0, adds `dx` to its word `+0x10` and `r8w` to `+0x12`, adds them to words `+0x98`/`+0x9A` of the object at its qword `+0` when that is non-null, and sets `+0x60` to 1 | `002E04F3`, `002E0501`, `002E0507`, `002E0518`, `002E052A` |
| `00303E90` | 33 B | tail-calls `0031E860(3)` when `0030D9A0()` returns 2; otherwise returns 0 | `00303E94`, `00303E99`, `00303E9E`, `00303EA5` |
| `00313590` | 33 B | tail-calls `0031E860(3)` when `0030D9A0()` returns 1; otherwise returns 0 | `00313594`, `00313599`, `0031359E`, `003135A5` |
| `0037F340` | 106 B | when qword `+0xC0` is non-null and its first qword is non-null, calls that function pointer with (the object, &{dword 0x10, the 16 bytes at `00D111C0`: 8, 0, 0, 0}); then sets bit 0 of dword `+0xE0` and byte `+0xE5` to 2 | `0037F358`, `0037F367`, `0037F387`, `0037F389`, `0037F390` |
| `003C5FB0` | 64 B | returns 1 when `00254A50()` returns 0, `00377750()` is non-zero, `0053DD10(WorldTransition_GetActiveOrPendingFieldId())` is non-zero and `00264790()` is not above 0; otherwise 0 | `003C5FB4`, `003C5FBD`, `003C5FCD`, `003C5FD6`, `003C5FDD` |
| `003CB0C0` | 134 B | builds a node with `00245000(rcx + 0xC0, 0x1E0, 003CB150, 0)`, calls `00244960(rcx, node)`, and when the node and its first qword are non-null calls that function pointer with (the node, &{dword 0x10, 16 zero bytes}) | `003CB0DC`, `003CB0F2`, `003CB100`, `003CB12B` |
| `003F35A0` | 29 B | for `rcx` and each object along qword `+0x70`: when dword `+0x6C` differs from `edx`, clears bit 0 of dword `+0x50` and zeroes `+0x6C` | `003F35A7`, `003F35AC`, `003F35B0`, `003F35B3` |
| `003F8BF0` | 108 B | calls the function pointer at qword `+0x38`, when set, with (`rcx`, 5, 0); unlinks `rcx` from its neighbours (the object at qword `+0x30` gets qword `+0x28` in its `+0x28`, the object at `+0x28` gets `+0x30` in its `+0x30`), zeroes qwords `+0x28`/`+0x30` and word `+0x26`; then tail-calls `+0x38`, when set, with (`rcx`, 6, 0) | `003F8C09`, `003F8C18`, `003F8C29`, `003F8C37`, `003F8C53` |
| `003FCD20` | 187 B | by the kind in dword `[rdx]`: 1 reads the 20-byte entry `dword rdx+0x10` of `0020E600(dword +0x20 of qword rdx+8)`, gets `r = 002432B0(rcx + 0x50, qword +0x48 of [0209AC30], 0xD, rcx)`, and when `rcx` is non-null stores words `r+4` plus entry `+4`, `r+6` plus entry `+6`, `r+8` and `r+0xA` in words `+0x98` to `+0x9E`; then calls `003FCDE0(rcx)`, clears bit 11 of dword `+0x40` and returns 0. 18 returns 0. Any other kind tail-jumps to `005C5230` with the same arguments | `003FCD56`, `003FCD7B`, `003FCDA1`, `003FCDC2`, `003FCDC7` |
| `00406A60` | 865 B | by the kind in dword `[rdx]`. 1: stores `rcx` in qword `02B62D88`; zeroes `+0xC0`, `+0xE8`, `+0xD8`, bytes `+0xE3`/`+0xE1`; sets dword `+0xC8` to 0x10 and qword `+0xD0` to `0051EDC0(3)`; copies its byte `+0x24` count to byte `+0xE0`; for a non-zero count, allocates `8*count` bytes with `00393590` into `+0xD8` and fills each slot from the 12-byte entries of `0020E600(dword +0x28 of it)`: `0024A440(o + 0x10, o, 2)` with `o = 0020E600(entry dword +8)` for an entry whose dword `+0` is 1, else null; sets dword `+0x98` to 0 and words `+0x9C`/`+0x9E` from dwords `01E0C1D8`/`01E0C1DC`, and calls `00244960` with the qword read from `0208EA28` and `rcx`. 2: by dword `+0xC8`, bit 1 calls `004050C0`; bit 0, when `02B62D88` is set, calls `004050C0`, stores `00405100()` in byte `+0xE1`, clears bit 3 (or, when it was clear, checks the 24-byte entries at `[+0xE8]`, count byte `+0xE3`); when that byte is not 0xFF it posts `00244F50(0xD8, 00405310, &record)`, then calls `00244960`/`00247870` on `[+0xC0]` (bit 2) or `00246AD0`, and clears bit 0 and sets bit 1 of `+0xC8`. 4: when `02B62D88` is set, stores `0031B690([02B62D88] + 0xE8)` in its byte `+0xE3`. 18: calls `0024A680(slot, 0)` on each non-null slot of `+0xD8`, frees the array with `003697F0` and clears `+0xD8`. These return 0; any other kind returns `005C5230(rcx, rdx)` | `00406AE2`, `00406B27`, `00406C36`, `00406C86`, `00406CF3` |
| `004076B0` | 105 B | a step counter: returns -1 when dword `+4` (the step count) is 0; otherwise increments dword `+0` and, below the count, stores t = step/count in float `+0x14` and `(int)(dword +0xC * t + dword +8)` in dword `+0x10`, returning it; at the count, stores `+8 + +0xC` in `+0x10`, zeroes `+4`, stores 1.0 in `+0x14` and returns the sum | `004076B7`, `004076BB`, `004076E2`, `004076FA`, `00407707` |
| `00407C90` | 127 B | when dword `+0x44` masked by `0x180000` equals `0x100000`, stores word `+0x54` (plus dword `[rdx]` when `rdx` is non-null) in word `+0x98` and word `+0x56` (plus dword `rdx+4`) in `+0x9A` (skipped when `rcx` is null); then calls itself on each child from qword `+0x18`, following each call's return value, and returns qword `+0x20` | `00407CAB`, `00407CD0`, `00407CF6`, `00407D00` |
| `0057E8D0` | 117 B | by the kind in dword `[rdx]`: 1 stores `rcx` in qword `02CA99D0`, zeroes qword `+0xC8` and dword `+0xC0`, calls `00244960` with the qword read from `0208EA28` and `rcx`, `00247870(rcx, 0)` and `00247930(rcx, 100)` and returns 0; 18 zeroes `02CA99D0` and returns 0; any other kind tail-jumps to `005C5230` with the same arguments | `0057E8E6`, `0057E8F4`, `0057E903`, `0057E921`, `0057E938` |
| `0057EB30` | 117 B | by the kind in dword `[rdx]`: 1 stores `rcx` in qword `02CA99D8`, zeroes qword `+0xC8` and dword `+0xC0`, calls `00244960` with the qword read from `0208EA28` and `rcx`, `00247870(rcx, 0)` and `00247930(rcx, 100)` and returns 0; 18 zeroes `02CA99D8` and returns 0; any other kind tail-jumps to `005C5230` with the same arguments | `0057EB46`, `0057EB54`, `0057EB63`, `0057EB81`, `0057EB98` |
