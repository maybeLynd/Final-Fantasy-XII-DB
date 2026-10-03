---
system: The six VFX display layers - where in a frame effects are drawn, by the names the engine's own markers give them
category: 17-Presentation-Rendering
status: DOCUMENTED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the layer pass 00258EE0 (307 B) disassembled from the authority image and read whole, 2026-09-19; its six-entry
    jump table at 00259014 and its five marker strings read out of the image
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-vfx-layers-falsification-pass-1
  note: written by FABLE for FRONTIER-REQ-FABLE-LAST-96-UNCITED-BODIES; static. Scope is this one body - which layers
    exist, what they are called, and what brackets each. The grouped pass it calls for five of the six layers, the
    routines of the third layer's own path and the callers that decide WHEN each layer runs were not read; pending first
    review
---

# The six VFX display layers

Effects are not drawn in one go. The frame asks for them **six times, at six different points**, and each request names a
layer. One body, `00258EE0` (307 B), serves all six; it takes the layer number and the engine's own graphics-debug
markers say what each one is.

## 1. The layers

| layer | marker text in the image | what the body does |
|---:|---|---|
| 1 | `display VFX [layer : first]` | marker, grouped pass, one follow-up call, end marker |
| 2 | `display VFX [layer : after BG]` | the same |
| 3 | `display VFX [layer : TsEffMan_Layer_AfterOBJ]` | **its own path** - section 2 |
| 4 | `display VFX [layer : in EFF]` | marker; a state call with `0x3C00`; one extra call unless the 21-byte mode getter answers non-zero; grouped pass; the state call again with `0x3700`; follow-up; end marker |
| 5 | `display VFX [layer : after EFF & MENU]` | one extra call unless the same getter answers non-zero; then marker, grouped pass, end marker |
| 6 | the same text as 5 | marker, grouped pass, end marker |

Every layer begins with a call that takes `(0, layer)` and ends with its counterpart. Layers outside 1-6 do only that
pair.

**The grouped pass - `00259030` (179 B, read whole the same day, after this page was first published).** It opens a
bracket, waits on bit 8 of the dword `02EAF6D8`, runs two routines of the effect emit module, and then **draws the
layer's effect groups in a fixed order - 2, 3, 5, 6, 9, 1, 7, 4** - eight calls of one routine with `(layer, group)`;
there is no group 0 or 8. Then it calls **`003A3740`, the drain of the depth-sorted display list**
([the Gi render command family](../Gi-Render-Commands/gi-render-command-family.md) reads it: sort, then walk), makes a
call to an empty function, waits on the same bit again and closes the bracket. **So the sorted, blended primitives of
the effect elements come out at the end of every layer's pass.** *The wait is odd: its loop jumps back to the test,
not to the load, so a bit found set on entry would never be seen to clear. Recorded as seen.*

**`TsEffMan` is the effect manager's own name for itself**, preserved in the third marker; "after OBJ" - after the
objects, which is to say after the characters and props - is where the third layer sits. The order the six names
suggest is: first, after the background, after the objects, inside the effect pass, after effects and menu. *When each
layer is actually requested is decided by this body's callers, which were not read; the order is the names', not a
measurement.*

## 1a. What a group draw is - `0024D370` (367 B, read whole 2026-09-19, FABLE)

The routine the grouped pass calls with `(layer, group)` is **a walk over the effect containers of one group**.

1. The head of the group's container list comes from the table `020910F0` (one pointer per group); an empty group
   returns at once.
2. **The group gate `0024D4E0` (94 B, read whole).** Group 8 is refused outright. Groups 1-4 and 7 need their bit
   (`group - 1`) set in the AND of three enable words, `02092162`, `02092164` and `02092166`. Group 2 also needs bit 0 of
   `02F8F29E` clear, and group 5 needs bit 0 of `02EBEF68` clear. Groups 6 and 9 always pass. *Who writes the three words
   and the two bytes was not read.*
3. The group number is published at `02092700` for the duration, and put back to -1 at the end.
4. For each container (next pointer at `+0x348`) **three conditions decide whether it is drawn**: its word `+0x3A8` must
   equal the current mode (the 21-byte getter of section 1); **the top nibble of its word `+0x378` must equal the layer**
   - so the layer an effect belongs to is authored there; and the per-container gate of section 1b must pass.
5. **The container is made current - `0024ED80` (132 B, read whole).** It publishes the container at `02F97348` and its
   resource (`+0x340`) at `02F97340`, and eight more pointers: into the resource, `+0x18`, `+0x38`, `+0x840`, **`+0x848`
   at `02EBEF90`** and `+0x850`; into the container, `+0x120`, `+0x130` and **`+0x1B8` at `02EBEF88`**; then tail-calls a
   routine that, among other things, writes the texture-index base. *These are the globals the element code reads:
   `02F97348` is the "container being drawn" of
   [how a position becomes a single number](../Position-To-Scalar/how-a-position-becomes-a-single-number.md), and
   `02EBEF90` is the sub-resource table the child-spawn slots index
   ([an effect element, frame by frame](an-effect-element-frame-by-frame.md)).*
6. Container flag byte `+0x36A`: **bit 0** asks for a commit step first - an optional call with the container's pointer
   `+0x380`, then a routine whose zero result **skips this container**; **bit 1** opens a scoped guard and raises bit 0
   of `02F8F310`.
7. Then the per-container transform composer, the walk of the container's instance list (which reaches the element
   walks - [the dispatch page](effect-element-type-dispatch.md)), and a closing state query.

**So the workbench matrices the element code uses are composed once per container, inside the draw loop** - not once per
frame. With six layers and eight groups this routine runs up to forty times a frame (layer 3 runs no groups).

## 1b. The per-container gate - `0024D770` (431 B, read whole 2026-09-19, FABLE)

Step 4 of section 1a ends in this gate. **A container whose word `+0x364` is non-zero is never drawn.** Otherwise bit 0
of its flag word `+0x36A` is raised and the gate switches on the container's **kind byte** (`+0`; a jump table at
`0024D920` covers kinds 2-9, and any other kind is drawn).

| kind | drawn when |
|---|---|
| 2 | the container's words `+4` and `+6` index two byte tables (`02F8F23C`, `02F8F27C`) and **bit 1 is up in both** |
| 3 | **the character-bound container.** The low six bits of dword `+4` pick an entry of the 64-entry, `0x38`-stride handle table `02EBD480` - the table a character's render record reaches its effect container through ([how a character fades](../Character-Render-Records/how-a-character-fades-the-ten-channels.md)). The entry's flag byte `+0x30` is a **per-frame handshake**: bit 1 is "my owner asked for me" - required, unless container flag bit 3 is up, in which case a missing bit 1 only clears the entry's bit 2 - and the gate **clears bit 1 when it is called to consume** (the group draw does). The entry's bit 2 is then copied into container flag bit 0, and the container's byte `+0x39B` must be non-zero |
| 4 | an object looked up from the container exists and bit 0 of its `+0x20` is clear |
| 5, 6, 9 | bit `kind - 1` of the AND of the three enable words of section 1a is up, **or** a record looked up by dword `+4` has bits 1-2 of its byte `+0x13` equal to 2. Then: container flag bit 4 also demands enable bit 0; and with container flag bit 15, **while bit 11 of the screen-effect flag word `020926E4` is up** and a predicate answers 0, only the container whose dword `+4` equals a query's answer is drawn |
| 7, 8 | always |

**Who renews the permission (added the same day).** The character side is on
[how a character fades](../Character-Render-Records/how-a-character-fades-the-ten-channels.md): each frame a root
record's distance-fade callback raises bit 1 - and sets bit 2, *which the fade page shows (2026-09-19) is constant 0
in this build, so the container flag bit 0 copied from it is too* - only when the record *and every ancestor up its parent
chain* is flagged shown.

**What this gives a reimplementation:** an effect bound to a character does not decide by itself whether it is drawn;
its owner renews a one-frame permission in the handle table, and an owner that stops asking makes the effect vanish
without anyone destroying it. *The lookups of kinds 4, 5, 6 and 9, the predicate and the query were not read; nor was
what raises bit 11 of `020926E4` (the screen-effect page has the word, not this bit).*

## 2. Layer 3 is different

Layer 3 does not call the grouped pass. It opens its marker, makes the opening call, runs two routines of the effect
emit module (the band that holds the point, line and quad emitters of
[the element types 0x00-0x0A](the-element-types-00-0a.md)), then **chooses one of two pairs of calls on bit 2 of the
byte `02F8F310`**, runs one routine from the band that holds the display list's drain, makes a call to an empty function (a compiled-out hook - see
[image hardening](../../24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md),
section 9a), closes, and ends its marker. `02F8F310` sits beside the depth-sorted display list's count and base
([the Gi render command family](../Gi-Render-Commands/gi-render-command-family.md)).

~~So layer 3 is where the sorted, blended primitives of the effect elements come out.~~ ***Withdrawn the same day.**
That was a reading from a flag byte's neighbourhood, and the grouped pass, once read, contradicts it: every layer
drains the sorted list at the end of its own pass (section 1). What is different about layer 3 is that it **draws no
groups** - it goes from the two emit-module routines straight to a list routine of its own, which is not the drain
the other layers call and was not read.*

## 3. What a reimplementation must keep

- Six layer requests per frame, not one; an effect belongs to a layer and is drawn when that layer is asked for.
- Inside a layer the groups go out in the order 2, 3, 5, 6, 9, 1, 7, 4, and the sorted list is drained after them.
- Layer 4 brackets its pass with two state values (`0x3C00` before, `0x3700` after).
- Layers 4 and 5 make an extra preparatory call except in the mode the getter reports.

**Not read:** the lookups the per-container gate makes for kinds 4, 5, 6 and 9; the commit step and the transform composer the group draw
calls; the writers of the group-enable words; the bracket pair; the five emit-module
and list routines of layer 3; the state call and its two values;
the mode getter's meaning; the callers.

| body | anchors |
|---|---|
| `00259030` grouped pass (179 B) | `00259036`, `00259040`, `00259045`, `00259050`, `00259056`, `0025905B`, `00259067`, `00259073`, `0025907F`, `0025908B`, `00259097`, `002590A3`, `002590AF`, `002590BB`, `002590C0`, `002590C5`, `002590CA`, `002590DE` |
| `0024D370` group draw (367 B) | `0024D382`, `0024D38B`, `0024D3A8`, `0024D3B8`, `0024D3C0`, `0024D3C7`, `0024D3CC`, `0024D3DB`, `0024D3E2`, `0024D3F5`, `0024D405`, `0024D40A`, `0024D419`, `0024D422`, `0024D441`, `0024D448`, `0024D451`, `0024D45E`, `0024D463`, `0024D471`, `0024D476`, `0024D494`, `0024D499`, `0024D49E`, `0024D4AC`, `0024D4B1`, `0024D4CF` |
| `0024D770` per-container gate (431 B) | `0024D77A`, `0024D799`, `0024D7A3`, `0024D7AB`, `0024D7C0`, `0024D7CD`, `0024D7DC`, `0024D7FC`, `0024D809`, `0024D813`, `0024D81D`, `0024D828`, `0024D82E`, `0024D83C`, `0024D849`, `0024D860`, `0024D865`, `0024D87B`, `0024D88F`, `0024D898`, `0024D8A7`, `0024D8B5`, `0024D8B9`, `0024D8D7`, `0024D8DE`, `0024D8F7`, `0024D905`, `0024D90F` |
| `0024ED80` make a container current (132 B) | `0024ED87`, `0024ED8E`, `0024ED99`, `0024EDA4`, `0024EDB2`, `0024EDC0`, `0024EDCE`, `0024EDDC`, `0024EDEA`, `0024EDF8`, `0024EDFF` |
| `00258EE0` VFX layer pass (307 B) | `00258EE8`, `00258EED`, `00258EFD`, `00258F04`, `00258F09`, `00258F0E`, `00258F17`, `00258F26`, `00258F35`, `00258F3A`, `00258F3F`, `00258F52`, `00258F5A`, `00258F6C`, `00258F76`, `00258F78`, `00258F86`, `00258F8B`, `00258FA8`, `00258FB4`, `00258FC0`, `00258FD0`, `00258FD5`, `00258FE3`, `00258FF1`, `00258FFF` |

## Cross-subsystem neighbours

None named: every routine this body calls is described by role, and none is cited by address.

**Core runtime scheduling - CLIENT.** `001B2530`, the tail target of the forwarder `00862C10` now named on
this page, calls `0017D980` in that layer's census. The VFX-layer bodies consult the scheduler through that
forwarder; they do not own it. MECHANICAL accounting (SWE2-EC7, 2026-09-19).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Movement — SERVICE, OUT-OF-SCOPE (1 edge).** `MainLoop_Draw` (`0022B0B0`), cited here as a caller of the layer pass, calls `00357780`, a 7-byte getter of the dword at `022C7F80`, right after its layer-6 pass (`0022B694`) as one of the conditions for a further draw call. The frame's draw consults a movement-side value; it is not part of any display layer this page describes.

**UI — CLIENT (1 edge).** The UI-filed 1,500-byte body `0024B9B0` calls `0024ED80`, the make-current step of section 1 item 5, after testing the container's byte `+0x370`. A UI-side walker also makes an effect container current, so it publishes the same "container being drawn" globals the element code reads; the layer draw does not depend on that caller.

## SWE2-EC7-71 update (2026-09-19) - `00862C30` + `00862C10` singleton forwarders measured

`00862C30` (12 B) loads the `01F7F4D8` singleton into `rcx` and
tail-jumps `001B2600` - the no-arg forwarder.

`00862C10` (17 B) is the arg-swapping sibling: `001B2530(global, edx,
ecx)` - the singleton prepended, the two caller args reversed.
Interior anchors `00862C37` (the `jmp 001B2600` tail) and `00862C1C`
(the `jmp 001B2530` tail).

## SWE2-EC7-99 update (2026-09-20) - `002D7E00` measured

`002D7E00` (47 B) is the slot retire `001B2530` calls:
`002D7E30` runs the notify with ~~`(ecx, 0, 0)`~~ **the id, the caller's `rdx` and `r8`, and `r9` = 0**, then
~~`qword[0209F6C0 + movsxd(ecx) * 48]`~~ **`qword[0209E6C0 + movsxd(ecx) * 48]`** is zeroed (corrected 2026-09-29, OPUS falsification pass 1, `CON-180`: the `lea` at `002D7E1A` resolves to
`0209E6C0`, and the body sets neither `edx` nor `r8d`) - the
48-stride table entry's head pointer cleared after the
layer machinery is told.
Interior anchor `002D7E21` (the head-pointer clear).

## SWE2-EC7-106 update (2026-09-20) - `0024C640` measured

`0024C640` (97 B) is the layer-table
reset `00258EE0` and `002590F0` run:
rows `1..9` (row `8` skipped) of the
`020910A0` table are visited and each
row's `[+8]`
chain gets `word[+0x32] = 0` written
through every node, then `00861EC0`
clears `0x1800` bytes at `02F8DA00`
and `0x1800` bytes at `02F8C200` -
the full quiesce the effect layers
run ~~on reload~~ **after the grouped pass of layers 1, 2 and 4, on every such request - its one call site in
`00258EE0` is the shared tail `00258F8B` - and in `002590F0` (corrected 2026-09-29, OPUS falsification pass 1, `CON-180`)**.
Interior anchor `0024C661` (the
`word[+0x32]` clear).

## SWE2-EC7-112 update (2026-09-20) - `00183060` measured

`00183060` (10 B) is the
global flag latch `0022B0B0`
and `0024D370` run:
`byte[01F7F50E] = (ecx !=
0)` - one byte of shared
state, nothing else.
Interior anchor `00183062`
(the `01F7F50E` store).
`0022B0B0`'s own fan-out is
mechanical and recorded
here: it reaches the
Movement domain - a
shared-service edge, not a
display-layer subject.

`0036F550` (1172 B) is the per-layer record emit `00258EE0` drives: `003B5340` gates the pass, `02AD9DF4 - 02AD9DF0` divides by three via the `0x55555556` magic into the count fields, `02AE9658`/`02AE965C`/`02AE9668`/`02AE9680` seed the float state, a `0x80`-descending `movups` block copies the `[r9+0x40]`.. row set into the `02AE9600` record, and `003A35E0` submits it with callback `004758E0` and arg `0x438` - the layer draw-list emitter behind the six-layer pass.

Interior anchor `0036F9DA` (function `0036F550`).

`003B5340` (113 B) is the state-byte reader `0036F550` gates on: `byte[02B40518]` folds its own bit-0 into the test, `02B4050A == 1` and `02B40512 == 1` select between the `02B40508` and `02B40510` qwords through `cmove`/`cmovb` on `02B40511`, a `-1` high dword fails to zero, else the low byte of the selected word returns - the two-deep flag chain in front of the layer emit, call-free.

Interior anchor `003B5392` (function `003B5340`).

`0036F9F0` (438 B) is the layer-record reset `00258EE0` calls: `003B5340` counts, `dec` + `rax * 5` (`0x14` stride) index `02AD9B60` records, then a float-default flood writes `02AE9658`..`02AE9910` (`300.0`/`256.0`/`500.0`/`224.0` heads) with `0039D3F0`/`003A35E0` finishing - the display layers' reseed.

Interior anchor `0036F9F4` (function `0036F9F0`).

`001B2530` (201 B) is the emit-layer writer `00862C10` tail-jumps into: it stores `!00182560()` at `[rsi+0x98]`, refreshes through `00182250`/`001823E0(3)`, ~~picks `0017FEE0`/`0017FE60` on `edi > 5` for three `002D7E00` emits (ids 0xE00, 0xDFF, 0)~~ **makes three `002D7E00`
calls (ids 0xE00, 0xDFF, 0). The first takes `0017FEE0` or `0017FE60`, picked by `0017D980`'s answer (`001B2583`), with
`edi > 5` as their argument; the second always takes `0017FEE0`, the third `0017FDE0` (corrected 2026-09-29, OPUS falsification pass 1, `CON-180`)**, stores `+0x90 = ebp` and `+0x94 = edi & ~0x10`, then tail-jumps `001FBD80`

Interior anchor `001B259E` (function `001B2530`).

`0039CFF0` (198 B) is the ensure-allocated emit `00258EE0` runs ~~per layer record~~ **only in layer 4, twice, as the
section-1 "state call" with the ids `0x3C00` and `0x3700` (`00258FBB`, `00258FDC`; corrected 2026-09-29, OPUS falsification pass 1, `CON-180`)**: `002D7FA0` resolves the row and when its `+0x18`/`+0x10`/`+0` chain is empty a default object is allocated via `00182B40` at 0.5f scale; under the `001FBE30`/`001FBE50` lock pair it `00376320`s and `00182A60`s the object with `r14d`, and when the result differs from `[rdi+0x10]` it `002D7D90`-reallocates the row ~~to `0xE0 + [rsp+0x20]` entries~~ **with the fixed pair `r8` = `0x100`
(`lea r8d, [r9 + 0x20]`) and `r9` = `0xE0` and a fifth argument of 1 (corrected 2026-09-29, OPUS falsification pass 1, `CON-180`)**

Interior anchor `0039D042` (function `0039CFF0`).

`00376320` (47 B) is the lane-class normaliser `0039CFF0` (and the mip-budget code `0039D0C0`) consult before sizing an emit: `cl` of 0-2 or 5 maps through the channel byte `dl` (`dl == 1` returns 1, `dl == 2` returns 2, anything else 0), `cl` 3 or 4 returns 3 unconditionally, and every other `(kind, channel)` pair returns 0 - the three-way class that decides whether a layer row takes the 1-, 2- or 3-lane layout

Interior anchor `00376338` (function `00376320`).

## Falsification pass 1 — 2026-09-29 (OPUS): the layers, groups and gates survive; four appended notes do not

**Attack.** Sections 1, 1a, 1b and 2 were turned into checks at their instructions, and so was every appended note that
names an instruction. Script: `Tools/analysis-kit/gfz-scripts/falsify_vfx_layers.py`, output `falsify_vfx_layers.out`,
image `73461d08…`, 0 BROKEN, exit 0. Still not read, as the page says: layer 3's list routine, the lookups for kinds 4,
5, 6 and 9, the group-enable writers, and the callers that decide when each layer runs.

| # | Clause attacked | Result |
|---|---|---|
| V9 | SWE2-EC7-99: `0209F6C0`, notify `(ecx, 0, 0)` | **refuted** (`CON-180`). The table is `0209E6C0`. The notify gets the caller's `rdx` / `r8` and `r9` = 0 |
| V10 | the `001B2530` note: "picks `0017FEE0`/`0017FE60` on `edi > 5`" | **refuted** (`CON-180`). `0017D980`'s answer picks. `edi > 5` is the argument. Emits 2 and 3 are fixed |
| V11 | the `0039CFF0` note: "runs per layer record", "`0xE0 + [rsp+0x20]` entries" | **refuted** (`CON-180`). Only layer 4 calls it, twice (`0x3C00`, `0x3700`). The reallocation passes `0x100` / `0xE0` / 1 |
| V12 | SWE2-EC7-106: `0024C640` "run on reload" | **refuted** (`CON-180`). It runs from the shared tail `00258F8B` after layers 1, 2 and 4 on every request, and from `002590F0` |
| V0 | sizes | **survives**: all nineteen |
| V1 | section 1: the layer table | **survives**: the six-entry table and the five marker texts. Layer 4 has the `0x3C00` / `0x3700` bracket and its extra call; layer 5's extra call comes before its marker. Every path closes through `00862C30` |
| V2 | section 1: the grouped pass | **survives**: the order 2, 3, 5, 6, 9, 1, 7, 4; the drain `003A3740`; both waits loop to the test |
| V3 | section 1a: the group draw | **survives**: `020910F0`, the gate, `02092700` set and reset to -1, `+0x348` / `+0x3A8` / `+0x378 >> 12`, `0024D770(c, 1)`, `0024ED80`, the `+0x36A` bits |
| V4 | section 1a: the group gate | **survives** |
| V5 | section 1a: make current | **survives**: ten stores, including `+0x848` to `02EBEF90` and `+0x1B8` to `02EBEF88`, and the tail-jump |
| V6 | section 1b: the per-container gate | **survives**: `+0x364`; the kind table 2..9; the two byte tables; the handle entry with its bit handshake and `+0x39B`; the `+0x13` lookup; flag bits 4 and 15; `020926E4` bit 11 |
| V7 | section 2: layer 3 | **survives**: the bit-2 test of `02F8F310`. It makes no grouped-pass call and calls `003A3990`, not `003A3740` |
| V8 | the notes that name an instruction and hold | **survives**: the forwarders, `0024C640`'s body, the latch, `00376320`, `0036F550`'s submit, `0036F9F0`'s records, `001B2530`'s stores |

Corrected in place: the four notes. The consumer record is `_index/candidates/vfx-layers-falsification-pass-1-0929/`.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-six-vfx-display-layers-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0017FDE0` | 38 B | passes the pointer the 8-byte getter of qword `01F7F598` returns to a 15-byte helper as `rcx`; when byte `+0x8` of the record that call returns is zero it returns that record's qword `+0x0`, otherwise it returns 0 | `0017FDE4`, `0017FDEC`, `0017FDF1`, `0017FDF7`, `0017FDFF` |
| `0017FE60` | 57 B | when `ecx` is non-zero calls a 66-byte helper, otherwise a 93-byte helper, each with the pointer the 8-byte getter of qword `01F7F598` returns; when byte `+0x8` of the returned record is zero it returns that record's qword `+0x0`, otherwise it returns 0 | `0017FE64`, `0017FE70`, `0017FE7F`, `0017FE84`, `0017FE8A` |
| `0017FEE0` | 57 B | when `ecx` is non-zero calls a 33-byte helper, otherwise a 75-byte helper, each with the pointer the 8-byte getter of qword `01F7F598` returns; when byte `+0x8` of the returned record is zero it returns that record's qword `+0x0`, otherwise it returns 0 | `0017FEE4`, `0017FEF0`, `0017FEFF`, `0017FF04`, `0017FF0A` |
| `001B2600` | 44 B | calls a 157-byte helper (`rcx`); then, when byte `+0x98` of `rcx` is non-zero, tail-jumps a 38-byte helper with 3, otherwise returns | `001B2609`, `001B260E`, `001B2617`, `001B2621` |
| `003A3990` | 97 B | when dword `02AEF414` is non-zero, calls a 63-byte helper (qword, 2) for each qword of the array at `02AEF420` while the index stays unsigned-below dword `02AEF414` (re-read every pass), then zeroes dword `02AEF414`; when that dword is zero it returns without work | `003A3994`, `003A39C9`, `003A39D0`, `003A39E2` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-the-six-vfx-display-layers-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `001868A0` | 66 B | `0017FE60` + 0x10 | calls the site `001868A0` + 0x9 and, only when it returns non-zero, the site `001868A0` + 0x12; then returns qword `rcx+0xB50+i*8` when byte `rcx+0xDBB` is non-zero and qword `rcx+0xB48+i*8` when it is 0, where `i` is dword `rcx+0xDD0` (the incoming `rcx`, kept in `rbx`) | Interior anchor `001868A9`; Interior anchor `001868B2`; Interior anchor `001868B7`; Interior anchor `001868C6`; Interior anchor `001868D4` |
| `00186A50` | 33 B | `0017FEE0` + 0x10 | returns qword `rcx+0xB50+i*8` when byte `rcx+0xDBB` is non-zero and qword `rcx+0xB48+i*8` when it is 0, where `i` is dword `rcx+0xDD0` | Interior anchor `00186A57`; Interior anchor `00186A5D`; Interior anchor `00186A5F`; Interior anchor `00186A68` |
| `00862C00` | 14 B | `003A3740` + 0xF2 | returns dword `+0x90` of the object whose pointer is the qword at `01F7F4D8` | Interior anchor `00862C07` |
