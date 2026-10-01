---
system: The post-result events — how a resolved result becomes a battle message, and the table the messages come from
category: 07-Combat-Action
status: AUDITED
owner_layer: PrimaryOwner:CombatAction
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: 00385BA0, 00469EC0, 0046AB10, 00469570, 0046A870, 0046AC90 and the argument-building half of
    005369C0 read to their rets from the shipping EXE with every RIP target computed by a tool;
    battle_message.bin (us) extracted from the archive and decoded with the VBF page's heap layout and
    charset; every event id the code posts matched to the row and text at that index
last_reviewed: 2026-09-11
registry_slots:
  - "0x02EBF018"
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-post-result-events-pass-1
  last_pass_kind: authored
  crossref_clean: true
  reopened_count: 0
---

# The post-result events and the battle message table

> After every resolved action result, one dispatcher looks at the result record and the action id and
> posts zero or more **event ids**. An event id is a row of a 102-row authored table — the file
> `battle_message.bin` — whose text is the line the battle log shows ("Vaan's steal failed", "Fran has
> fallen", "Reserve members' HP are restored"). The poster between them rate-limits repeats per
> unit, and a small filter decides whether a message about an off-screen actor is shown at all.

## 1. What the player sees

The scrolling battle log: a steal that fails says whose steal failed and that the target has nothing
left; a technick names what it did to whom; a character who dies "has fallen", one turned to stone
"turns to stone"; an item used from the menu reports that HP was partially or fully restored, or
that the reserve members were healed. Every one of those lines is one row of one table, chosen by
one function from the result record, and formatted from up to four argument slots the same row
declares.

## 2. Native mechanism

### 2.1 Who calls the dispatcher, and with what

`BattleFormula_ApplyResultMetadata` (`00385BA0`, 250 B) — step 1 of
[the applier](../applying-a-result-to-a-target.md) — does four things and then dispatches:

| site | what |
|---|---|
| `00385BAF`–`00385BEA` | result `+0x138` (byte) and `+0x13C` (dword), when not `-1`, are written to the battle-state block's `+0x5B0E` / `+0x5B00` (`02EBF190`) |
| `00385BF0`–`00385C6B` | result bytes `+0x34` / `+0x33` / `+0x32` non-zero → the target unit's spawn record `+0x14` bit 2 / 1 / 0 cleared (the same bits [the applier](../applying-a-result-to-a-target.md) step 4 clears, but under a different condition. *Restated 2026-09-25 (FABLE, Claude Opus 5.5), on `OPUS-REQ-FABLE-POSTRESULT-AVAILABILITY-CONDITION`:* here the result byte alone decides, with only the unit and its `+0x6A0` block null-checked. The applier's `btr` at `0031146C`, in the loop `00311420`–`0031148B`, runs only when the target record's byte `+5` is `1` (`0031141B`) **and** the slot's id word `[+0xE60] + 0x32 + 2i` is not `0xFFFF` (`00311441`), right after the inventory add grants the item. Both use the same unit: the applier resolves it from the target stats at `0031132C`, and this step is its only caller (`0031137A`, before the loop). This step therefore always clears the bit first. The applier's `btr` finds it already clear and does not change the byte. The bit's state after the call depends on the result byte alone; the kind and id tests gate only the item grant) |
| `00385C6F`–`00385C85` | result byte `+0x1C == 1` (the resolver's "resolved" mark, `00386855`) → `BattleFormula_DispatchPostResultEvents` (`00469EC0`)`(actionId = 02AEDFD4, sourceStats, targetStats, result)` |

So the dispatcher runs once per resolved result, with the action id from the formula scratch word
`02AEDFD4` that `BattleFormula_ResolveTargetResult` (`00385F60`) stored at `00385FE4`.

### 2.2 The dispatcher — two worlds, selected by whether the target has a battle unit

`BattleFormula_DispatchPostResultEvents` (`00469EC0`, 1,904 B) first builds the **event context**
it will hand to every post (`[rbp-0x48]`, `00469ED8`–`00469F37`):

```
ctx  +0x00  sourceStats        +0x14  |result.dw_24|  (the HP delta, magnitude)
     +0x08  targetStats        +0x18  status id (filled only for events 0x18 / 0x1A)
     +0x10  result.dw_08       +0x1C  source.b_1C2 (level), 0 if no source
     +0x20  result.dw_38       +0x28  action id
```

Then, in order:

**(a) Technick notices from result `+0x140`** (`00469F68`–`00469FDB`), posted for the source:

| bit | event | text (us) |
|---|---|---|
| 8 | `0x36` | "… uses …. Technick failed. Character must be blind." |
| 9 | `0x38` | "…'s poach failed. … must be further weakened to be poached." |
| 11 | `0x3A` | "… uses …. Technick failed. Not enough gil." |
| 10 | `0x3D` | "… uses Shift. …'s elemental weakness has changed" |

**(b) The branch** (`00469FE5`–`00469FF9`): if the target stats are null **or have an owning battle
unit** (`BattleStats_FindOwningBattleUnit`, `0031B860`) → **(d)**. Only a target stats record **with
no unit behind it** reaches **(c)**.

**(c) The no-unit world — HP / MP / status outcomes** (`00469FFF`–`0046A3BF`). The texts these ids
carry are the menu's ("…'s HP is partially restored", "Reserve members' …"), which is what a stats
record without a unit is: a party member the field has not spawned. The numbers first: `[rbp+0x58]`
= new HP (`result.dw_24`, or target `+0x48 + result.dw_24` when result `+0x2C` bit 3 is clear),
`[rbp+0x50]` = new MP likewise from `+0x2A` / target `+0x4C` (bit 4); the HP cap `r13d` = target
`+0x48` (at least 1) when the merged flags `+0x64 | +0x3C` have bit 16, else target `+0x24`, doubled
when they have bit 28 (`0046A0C5`–`0046A0F0`); `[rbp-0x50]` = target `+0x28` unless bytes `+0x6C` /
`+0x7C` are negative. Then the "is the target the one the source is acting on" test: the source
unit's `+0x6B9` slot index → `BattleStats_GetByBattleSlotIndex` (`00320A40`) when its `+0x6B6` is
set, else its `+0x710` focus handle → `BattleStats_ResolveByActorHandle` (`00320A70`), compared with
the target (`0046A10C`–`0046A183`):

| condition | event | text (us) |
|---|---|---|
| result kind `+4 == 6` and the resolved member is the target | `0x1D` | "{action} had no effect." |
| resolved == target, action `0` / `4` | `0x1E` | (blank row) |
| resolved == target, action `0xB` | `0x1F` | "Reserve members' HP are restored." |
| resolved == target, action `0xD` | `0x20` | "Reserve members' status effects have been dispelled." |
| resolved == target, action `0xE` | `0x21` | "Reserve members' HP are fully restored." |
| resolved == target, action `0x10` | `0x22` | "Reserve members are cured of various status effects." |
| resolved == target, action `0x67` | `0x23` | "Reserve members' HP and MP are fully restored." |
| otherwise, action in {`0`, `4`, `0xB`, `0xD`, `0xE`, `0x10`} (mask `0x16811`, `0046A1F0`) or `0x67` | — | nothing more |
| result `+0x58` bit 0 | `0x1C` | "… regains consciousness." |
| `+0x2C` has `0x4100`, HP ≥ cap, MP ≥ cap, `+0x28` ≠ 0 | `0x17` | "…'s HP and MP are fully restored." |
| `+0x2C` has both of `0x500` | `0x14` / `0x13` | HP fully / partially restored (`0046A276`–`0046A287`; `ctx +0x14` = \|delta\|) |
| `+0x2C` has both of `0x14000` | `0x16` / `0x15` | MP fully / partially restored (`0046A2C5`–`0046A2D6`; `ctx +0x14` = \|`+0x2A`\|); `0x1D` "had no effect" when the target's `+0x6C` / `+0x7C` are negative or `+0x28` is 0 |
| statuses in the remove mask `+0x58` whose row in the status table `02EBF118` has word `+6` bit 13 | one → `0x18` "… is cured of {status}" (`ctx +0x18` = the status), two or more → `0x19` "… is cured of various status effects." (`0046A2E9`–`0046A396`) |
| statuses in `+0x58` without that bit | one → `0x1A` "{status} fades from …", two or more → `0x1B` "Various status effects fade from …." (`0046A39B`–`0046A3BF`) |

**(d) The unit world — technick messages** (`0046A3C4`–`0046A617`), posted for the source:

| condition | event | text (us) |
|---|---|---|
| action `0xA9` (Steal) and kind `6`, result `+0x2C` bit 23 **set** | `0x33` | "…'s steal failed. … has nothing to steal." |
| action `0xA9` and kind `6`, bit 23 **clear** | `0x34` | "… couldn't steal from …." |
| kind `0` and the action row's byte `+0x1E` is `2` or `7` (`02EBF138`, `0046A3FF`–`0046A480`), then by action id: | | |
| `0xA1` / `0xA2` | `0x27` / `0x28` | "… uses …. …'s status effects spread to …" / "… has a new elemental weakness" |
| `0xA6` / `0xA7` | `0x29` / `0x2A` | "…, lowering …'s strength" / "…'s magick power" |
| `0xAB` / `0xAC` | `0x2B` / `0x2C` | "…, lowering …'s defense" / "…'s magick resist" |
| `0xA9` | `0046A870` | the stolen-goods messages, §2.6 |
| `0xAD` | `0x35` | "… uses …. … switches sides" |
| `0xB2` | `0x37` | "… poached …, winning …" |
| `0xA4` | `0x3C` | "… uses …, sacrificing MP to change …'s HP." |
| `0x116` / `0x117` | `0x44` (blank) / `0x45` | "… loses a massive amount of MP" |
| `0x13F` | `0x46` | "…'s level doubles" |
| `0x17F` | `0x47` | "… loses all MP" |
| `0x119` | `0x48` | "…'s HP and MP are inverted" |
| `0x144` / `0x145` | `0x49` / `0x4A` | "… feeds on …, grow…" / "… calls for help" |
| `0x1A1` / `0x1A0` | `0x4B` / `0x4C` | "… splits in two" / "… summons the undead" |
| `0x1A7` | `0x4D` | "… feeds on the energy conduit" |
| kind `0`, target present, action `0xB1` (Libra) (`0046A5FE`–`0046A617`) | `0x3B` | "… uses …. Additional target information now available." |

Every id above is an immediate in this function (`mov edx, N` or `lea edx, [rax - K]` with `rax`
the action id); the texts are the rows at those indices in §2.5, and they agree with the code's
condition in every case — which is what binds the table to the file (§2.5).

### 2.3 The poster — one ring, a rate limit, a visibility filter

`0046AB10` (371 B) is `post(stats, eventId, ctx)`; every message in the game goes through it (48
call sites in 18 functions, §2.7). In order:

| step | site | what |
|---|---|---|
| drop | `0046AB19` | `ctx.dw_28 ≥ 0x1FF` — the dispatcher's action id; actions `0x1FF`–`0x21E` never post |
| drop | `0046AB42`–`0046AB56` | the global flags word `02089340` has `0x3080`, or the unit behind `ctx.q_08` has byte `+4` bit 5 |
| filter | `0046AB65` | `00469570(eventId, ctx.q_00, ctx.q_08)` returned 0 (§2.4) |
| rate limit | `0046ABB3`–`0046ABF5` | if the event's row byte `+4` bit 0 is set: scan the ten ring entries; one with the same `(event, stats)` whose `dw_04 + 0x1C2 × [01DFE0B4]` is still ahead of `GameClock_GetRawTickCounter` (`0032A150`) suppresses the post |
| record | `0046AC00`–`0046AC5D` | ring entry `02EBB560 + 32 × [02EBB54C]` ← `{ w_00 = event, dw_04 = tick, q_08 = stats, rest 0 }`; `02EBB54C = (i + 1) mod 10` |
| realise | `0046AC66` | `005369C0(stats, eventId, ctx)` (§2.5) |

### 2.4 The filter

`00469570` (303 B): if the event's row byte `+3` has bit 7 → **always show** (`004695F9`). Otherwise
the message is shown only if `002FA3B0(actor)` says so for the **source's** unit (`ctx.q_00` →
unit `+0x10`), or, when the source has none, the **target's** (`00469603`–`00469683`); a pair with
no unit at all is shown. `002FA3B0` is the gate the HP page and the status page already meet in
front of their reaction enqueues ([the HP write](../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md)
§2, [the status write](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md) §2) —
a per-actor visibility predicate — **answered 2026-09-12 (`EY-5`): true when the actor is within 24.0
units, horizontally, of the party leader** (the HP page §2.4). So a battle line about a fight far from
the leader is dropped unless its row sets bit 7.

### 2.5 The table — `battle_message.bin`, and how a row becomes a line

`005369C0` (1,000 B) turns an event into a formatted line. It fills **four 16-byte argument slots**
from the row's bytes `+0`, `+1`, `+2` and `+5` (`00536A51`–`00536BBC`):

| slot kind | argument |
|---|---|
| 1 | the source's name (`00536310(ctx.q_00)`), plus a byte from its actor (`00263A10`: word `+0x100` when `+0x102 ≥ 0`) |
| 2 | the target's name, likewise |
| 3 / 4 / 5 / 6 / 7 / 8 / 9 | `ctx +0x10` / `+0x14` / `+0x18` / `+0x1C` / `+0x20` / `+0x28` / `+0x24` |

It also takes the row's byte `+3` bits 2–6 as a five-bit category (`00536C6F`–`00536C78`), marks
events `0x24`–`0x25` (`00536C7C`–`00536C84`), resolves both names again through `00536280`, and
hands everything to `00536410` (1,420 B, `0x180`-byte request) and `0035B990` — the formatter and
the poster on the presentation side.

**The last mile, read 2026-09-11 (`FL-1`, narrowed).** `0035B990(request)` first turns the request
into text with `00393740(request, buffer, 0x180)`, which only serves a request whose dword `+0`
is **7** and whose qword `+0x28` (the source string) is non-null (`0039375F`–`00393771`; two
bounded copies through `003937C0`, `00393781`–`00393790`), else returns null. Then one of two
paths: if the request's word `+0x30` is non-zero, the text is copied into a `0x180`-byte stash at
`+0x568` of the record `022CA430` points at (zeroed first, `0035B9D2`–`0035B9F5`, `00254F30`);
otherwise, when `00254A10()` returns 0 and the request's word `+0x32` is non-zero, the string is
measured (`002B5680`, `002B3050`, `0035BA1E`–`0035BA47`; a width above `0x17E` sends the
unmeasured original instead, `0035BA4C`–`0035BA65`) and **posted to the HUD** by
`0028E110(text, request byte +0x1F, 0, 0)` (`0035BA68`–`0035BA75`): `002BDB20` turns the byte
into two style words, the colour defaults to `0x80808080` when no colour pointer is given, and
`002BDB00` writes the line into the HUD object at `[02098E80] + 0x8FA0` (`0028E150`–`0028E178`).
~~How long the line stays is inside that HUD object, unread. `00536410` — the slot formatter — is
bounded but not read.~~ **Both read 2026-09-12 (FABLE); `FL-1` closed.**

**The slot formatter** `00536410(request, out, capacity)` re-reads the message row's four kind
bytes (`+0` / `+1` / `+2` for slots 0–2, `+5` for slot 3; `00536490`–`0053654C`) and turns each
16-byte slot into one argument for the format string — an 8-way jump table at `0053699C` on
`kind − 1`, kinds 3 and 6 and anything above 8 taking the slot's raw int (`00536856`):

| kind | argument built from the slot | where |
|---|---|---|
| 1, 2 | **a name plus its letter**: `00536280(slot.b_00, slot.w_08)` — the name by id through `0026DEA0(id, 1)` when `b_00` is set, else text-bank `[02EBF170]` entry `w_08` (bank `>> 11`, index `& 0x7FF`), `0xFFFF` = the empty string `01CEB638` — copied into a `0xA0`-byte slot buffer (`00254F30`); then, when `slot.b_01` (the actor's word `+0x100`, §2.5) is non-zero, `002B58F0` appends **control byte `06` and the glyph `A` + (`b_01` − 1) mod 26** from the glyph table `0039C4A0()` `+0x18` / `+0x14` (`002B5969`–`002B59D0`) — the "Wolf A / Wolf B" suffix | `00536568`–`005365E7` |
| 4 | **a number in the row's colour**: `002B4090(0x20, buf, fmt99, …)` formats the slot's int with the sub-format at message-table entry 99 (`[02EBF018] +0x14 → +4 → +0x190`) — *that sub-format is empty, so the slot's argument is an empty string and the int is never printed (`PE-1`, 2026-09-14)* and four style values from `0035D400` / `0035D430` — not name resolvers but **palette lookups**: the table `00D10C60` `{18 19, 1A 1B, 14 15, 16 17, 1D 1D, 1C 1C, 1E 1E, 1F 1F}` indexed by `form × 2 + {0, 1}` gives a palette id, `002DD7E0` its colour (`[0215E6C8] + id × 8`, `0x80808080` outside `[0215E6B8]`) and `002DD7B0` its byte `+4`. The **form** is `00536190(bit 15, id)`: row byte `+3 & 3` = 1 → `bit15 ? 2 : 0`, 2 → `bit15 ? 3 : 1`, 3 → `bit15 ? 5 : 4`, 0 → 7; bit 15 of the request's id word is `002FA390(source)` — the source unit's one-hot category from `002F8E90` being 1, 2 or 4 (`& 7`; the predicate the lethal step is gated by, [the HP-write page](../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md)) — xor'd in by the realiser (`00536A1B`–`00536A43`) | `0053668C`–`0053673D` |
| 5 | **a status name**: status row `[02EBF118]` × slot int, word `+0` → text bank | `005365EC`–`00536687` |
| 7 | **an item or ability name, or a plain number**: `(v & 0xF000) == 0xE000` → the number `v − 0xE000`; else the `{class 1, id}` query record through `0031C5D0` (`00309E70` when `00254A10()` says so, inline otherwise) | `00536742`–`005367BA` |
| 8 | **an action name**: action row `[02EBF138]` × slot int, word `+0x34` → text bank (`00536280` when `00254A10()`) | `005367BF`–`00536850` |

`00254A10()` is true when the state word `[01E07814]` (`00229E40`, called at `00254A14`) is
in `{0, 7, 8, 10, 11}` (`cmp 0xB` bound at `00254A19`, `bt ecx, eax` with `ecx = 0xD81` at
`00254A1E`–`00254A26`); it chooses between the two format engines for the whole line — `002B4090` → `002B49F0`
(the `0x0F`-escape engine) when true, `002B40C0` otherwise — with the row's own format string
(`[02EBF018] +0x14 → +4 → +(id × 4 + 4)`, the heap layout of "The file" below; `battle-message-rows.tsv`
shows the `<8n>` slot references) and the four arguments (`00536889`–`0053696D`). The engines'
escape grammar is not read here.

**The line's lifetime** is in the log widget `[[02098E80] + 0x8FA0] + 0x1058` (a `0x40C0`-byte
object: 40 line nodes of `0x198` from `+0xD8` — text `0x180`, colour `+0x180`, **duration
`+0x184`**, flags `+0x186`, half-height `+0x187`, next/prev `+0x188`/`+0x190` — a pending list
`+0x4098`, the displayed chain `+0x40A0`, a free list `+0x40A8`, alpha `+0x40B4`, flags `+0x40B6`,
a hold counter `+0x40B8`, an elapsed counter `+0x40BA`, a threshold `+0x40BC`; reset by `002BED30`).
`002BDB20` gives every line **`G × 150` ticks** (`002BDB20`–`002BDB2A`; `G` = `[01DFE0B4]`, the
frame base — 1 at 30 fps, 2 at 60, [the boot-fixes page](../../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md)), stored at the node's `+0x184` by `002BE8D0`
(`002BE9BA`–`002BE9BF`; the style value it also computes — a `020BE610` table byte for styles
1–5, else `G × 30` — is passed but never stored). A post takes a free node, or **the oldest
*pending* line when the pool is empty** (`002BF480`, `002BE95B`), and appends it to the pending
list. The tick `002BEAC0` (from the HUD tick `00291750` through `002BE450`) then runs:

- nothing displayed and something pending → the oldest pending line becomes the displayed chain,
  elapsed 0, threshold = its `+0x184`, hold 256 if the widget was invisible else 0, and it **fades
  in at `0x10` alpha per tick to `0x80`** (`002BEC6E`–`002BECD1`);
- displayed and showing: the hold counter climbs by `0x20 / G` per tick to 256, and on reaching it
  **the oldest displayed line is dropped** when two or more are up (`002BF010`); once held, the
  elapsed counter advances one per tick **while fully faded in and no transition is running**
  (`0036D830` → `00226BA0`, [the world-tick page](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md); `002BEBA8`–`002BEBB1`), capped at `G × 150`; when it reaches
  the threshold and a line is pending, that line **joins the chain** (elapsed 0, hold 0, threshold
  = its duration; `002BEC00`–`002BEC4D`); when it reaches `G × 150` with nothing pending, showing
  is cleared and the chain **fades out at `0x10` per tick** (`002BEC60`, `002BECDA`);
- displayed, not showing, alpha 0 → the chain is released to the free list (`002BEE00`).

So a line stays **five seconds** at either frame rate (150 or 300 ticks), plus an 8-tick fade
either side, and a burst of lines scrolls through at most two at a time.

**The file.** `ps2data/image/ff12/test_battle/<lang>/binaryfile/battle_message.bin` is an `st2e`
table — `us`: 102 rows × 8 B, header 32, heap at `+0x350` with `{1, 12, 5819, 102}` and 103
offsets, text at `heap + 12 + offset[i]` in the custom charset
([the VBF page](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) §7).
The row is exactly what the code reads:

```
+0  u8  slot 0 kind      (1 source name, 2 target name, 3-9 a context number, 0 none)
+1  u8  slot 1 kind
+2  u8  slot 2 kind
+3  u8  bit 7 = always show (bypass 00469570); bits 2-6 = category
+4  u8  bit 0 = rate-limited per (event, unit)
+5  u8  slot 3 kind
+6  u16 0
```

Every populated byte in the 102 rows falls in those fields and no other; the slot kinds match the
texts (row `0x04` = `01 06`: "{source} is now level {level}"; row `0x1D` = `08`: "{action} had no
effect."; row `0x18` = `02 05`: "{target} is cured of {status}"; rows `0x33`–`0x34` = `02 01` with
`{31}` slot references `<81>` / `<80>`). Rows `0x05`–`0x0C` and `0x4F`–`0x62` are the rate-limited
ones; rows `0x0D`–`0x0F`, `0x27`–`0x2C`, `0x33`–`0x35`, `0x39`–`0x3A`, `0x3C`–`0x4C` have byte `+3`
bit 7 clear and so pass through the visibility filter.

**The binding `02EBF018` ↔ `battle_message.bin`** — registry slot 7, unnamed until now
([the registry](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)) — rests on
that agreement: every event id the code posts, under the condition the code tests, is a row whose
text says that condition (23 pairs in §2.2 alone, plus `0x10` "has fallen" on the lethal path,
`0x11` "is cast into the void" and `0x12` "turns to stone" for Vanished and Stone, `0x04` "is now
level" from the level-up poster).

**FL-2 narrowed 2026-09-15 (FABLE): the load is now traced, and the binding no longer rests on
content agreement alone.** The sentence above used to end *"the loader that fills slot 7 is not
read"*. It is read now, in five steps, every one from the shipped bytes:

1. **The request.** `BattleStorage_InitializeWorkArrays` (`002368D0`) frees the old blob, zeroes the
   pack pointer `0208E680` with a **qword** store (`002369B4`), and issues
   `003843F0(0x13, 00238850, "STATIC")` at `002369CE`. `00236C30`'s release arm re-issues the
   identical request at `00236C6B`. Resource kind `0x13` is the battle pack.
2. **The completion callback.** `00238850` (36 B) is that request's `rdx`. It calls
   `003846F0(&0208E680, blob, 0)` and then tail-jumps to `00236C30(1)`.
3. **The bind.** `00236C30`'s `ecx != 0` arm takes `rcx = [0208E680]` and calls
   `AreaData_BindAndRebaseSectionDescriptor` (`003845F0`) once per slot with a directory dword.
   For this slot that is `00236C7B`–`00236C86`: `rdx = (i32)[pack + 0xC]`, `rcx = &02EBF018`. The
   binder stores the descriptor into the slot (`003845F4`) and then rebases the descriptor's own
   `+0xC` / `+0x10` / `+0x18` … offsets by adding its address, skipping any that are zero.
4. **Which entry `+0xC` is.** The directory is `{u32 count; u32 offset[count]}`, so `+4 + 4k` is
   entry *k* and `+0xC` is **entry 2**. The manifest at `01E4D830` names entry 2
   `PS2Data\image\FF12\test_battle\in\BinaryFile\battle_message.bin` — read from `.rdata`, not
   inferred ([the registry](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md), `UQ-80`,
   `UQ-73`).
5. **The entry is the file.** In **all nine** shipped languages, `battle_pack.bin` entry 2 begins with
   the **exact bytes** of the sibling `battle_message.bin`; the entry's span runs 4–8 bytes longer,
   which is padding to the next directory offset. `us` carries the header `+4 == 102`, `+8 == 8`,
   `+0xC == 32` that `FL-2` predicted — and the count is **102 only in the Latin-script builds**
   (`us`, `de`, `es`, `fr`, `it`) against **100** in `ch`, `cn`, `in`, `kr`, so 102 is the `us` figure
   and not a property of the table.

**One thing the trace exposes, and it is not about this table.** `003846F0` stores the blob through
`RuntimePointer_EncodeImageAddress` (`0020E620`), which subtracts the base at `01F83530`, and readers
resolve it with `ImageAddress_ResolveRuntimePointer` (`0020E600`), which adds it back. **That base
ships as `0`**, and a rip-relative scan of `.text` finds **only those two accesses, both reads** — no
rip-relative writer. Bounded that way (a store through a computed pointer would not be seen), the
encode/decode pair are **identities in the shipped build**, which is why a 32-bit store into
`0208E680` can be read back as a 64-bit pointer at `00236C36`.

**What stays open, and it is the whole point of the row: the live half.** Nothing above reads
`[02EBF018]` in a running process, and the steal producing ring entries `0x33` / `0x34` at
`02EBB560` is unobserved. The file half and the load are static facts about the shipped image; the
runtime confirmation is still owed (`FL-2`).

The full text of the rows the code reaches is in [`battle-message-rows.tsv`](battle-message-rows.tsv)
(id, row bytes, decoded `us` text; `{nn}` = inline escape, `<8n>` = argument slot n).

### 2.6 The stolen-goods messages

`0046A870` (343 B), reached for a successful Steal (kind 0, action `0xA9`): for each result byte
`+0x32` / `+0x33` / `+0x34` that is set, it adds the enemy row's item word `+0x32` / `+0x34` /
`+0x36` to a three-entry `{ item, count }` list at `02EBB540` through `0046AC90` (a repeated item
increments its count, `0046ACF9`–`0046AD03`), then posts one event per entry (`0046A940`–`0046A9A2`):
first entry — gil (`item & 0xF000 == 0xE000`) `0x31`, count 1 `0x2E`, more `0x2D`; later entries
`0x32` / `0x30` / `0x2F`. In the `us` table rows `0x2D`, `0x2E`, `0x2F`, `0x31` are **blank** and
`0x30` ("{source} stole {item} from {target}") and `0x32` ("… stole {n} gil from …") carry the text —
so a single stolen item prints nothing here; the "Added … to inventory" line (`0x65`) comes from the
inventory side.

### 2.7 The other posters

The 17 other functions that call `0046AB10`, with the event ids they carry as immediates:

| function | events | text (us) |
|---|---|---|
| `004697C0` | `0x06` | "Action interrupted. … cancels …." |
| `00469A50` | `0x08` | "…'s target is too far from the party leader." |
| `00469AF0` | `0x0D` | "… begins casting …." |
| `00469BB0` (the lethal path, `EY-3`) | `0x10` | "… has fallen." |
| `0046A800` (Stone / Vanished, `FA-3`) | `0x11` / `0x12` | "… is cast into the void." / "… turns to stone." |
| `0046A690` | `0x04` | "… is now level {level}" (`ctx +0x1C` = the unit's `+0x1C2`) |
| `0046A630` | `0x24` / `0x25` | "You obtain {item}{count}" (`0x25` when the count is 1) |
| `00469E80` | `0x26` | "You obtain {n} gil" |
| `00469E30` | `0x4E` (`8 + 0x46`) when `002F8E90() == 8` | "… steals your loot" |
| `0046A6E0` | `0x5D + n` | the Magick Pot / Zalera lines `0x5D`–`0x62` |
| `0046A720` / `0046A790` | `0x3F` / `0x41` / `0x43` and `0x3E` / `0x40` / `0x42` | Paling / Magick Shield / White Wind rise and fall |
| `0046AA70` | `0x24` / `0x25` / `0x26` | obtain item (`0x25` when the count is 1) / gil — read 2026-09-12 (§7) |
| `0046A9D0` | `0x00`–`0x03` | "… triggered … trap" and its three variants — kind `0x104` heal, `0x105` energize, `0x103` gil loss, else plain (read 2026-09-12, §7) |
| `00469C00` | `0x4F`–`0x5C` | the seven magick fields' begin (`0x4F + 2i`) and end (`0x50 + 2i`) lines, against the active mask `022C314C` — `set_field_effect` / `clear_field_effect` (read 2026-09-12, §7) |
| `004698C0`, `00469E80`, `0046A870` | see §2.6 and the TSV | |

## 3. Key addresses

| address | size | what |
|---|---:|---|
| `00385BA0` | 250 B | `BattleFormula_ApplyResultMetadata` — block `+0x5B00` / `+0x5B0E`, spawn-record steal bits, the dispatch |
| `00469EC0` | 1,904 B | `BattleFormula_DispatchPostResultEvents` |
| `0046AB10` | 371 B | the battle event poster — ring `02EBB560` (10 × 32 B, index `02EBB54C`), rate limit, filter, realise |
| `00469570` | 303 B | the visibility filter — row byte `+3` bit 7, else `002FA3B0(actor)` |
| `005369C0` | 1,000 B | the realiser — four argument slots from row bytes `+0` / `+1` / `+2` / `+5`, then `00536410`, `0035B990` |
| `00536410` | 1,420 B | the slot formatter — eight slot kinds by the row's kind bytes, then one of two format engines (§2.5, read 2026-09-12) |
| `002BE8D0` | 356 B | the log widget's post — a `0x198`-byte node, duration `G × 150` at `+0x184`, pending list `+0x4098` |
| `002BEAC0` | 576 B | the log widget's tick — fade in, hold, elapsed against the duration, fade out, release |
| `0046A870` | 343 B | the stolen-goods messages; `0046AC90` (131 B) the `{item, count}` list at `02EBB540` |
| `02EBF018` | | registry slot 7 — `battle_message.bin` (102 × 8 B, `us`) by content agreement |
| `02EBB560` / `02EBB54C` | | the ten-entry event ring and its write index |
| `02AEDFD4` | | the formula scratch action id the dispatch is keyed by |

## 4. Data structures and formulas

```
post(stats, event, ctx):
  drop if ctx.dw_28 >= 0x1FF | (02089340 & 0x3080) | unit(ctx.q_08).b_04 & 0x20 | !filter(event, ctx.q_00, ctx.q_08)
  if row[event].b_04 & 1:  drop if ring has (event, stats) with dw_04 + 0x1C2*[01DFE0B4] > tick
  ring[idx] = {event, tick, stats}; idx = (idx+1) % 10
  realise(stats, event, ctx)

filter(event, src, tgt) = row[event].b_03 & 0x80 ? 1 : 002FA3B0(unit(src).p_10) ?: 002FA3B0(unit(tgt).p_10) ?: 1

ring entry (32 B): +0 u16 event, +4 u32 tick, +8 stats*, +0x10..+0x1F 0

line node (0x198 B): +0 text[0x180], +0x180 u32 colour, +0x184 u16 duration = G*150, +0x186 u8 flags, +0x187 u8 halfHeight, +0x188 next, +0x190 prev
widget tick (002BEAC0), G = [01DFE0B4]:
  no chain & pending  -> chain = pop(pending); elapsed = 0; threshold = chain.duration; hold = alpha ? 0 : 256; showing = 1
  showing:  hold < 256 ? hold += 0x20/G, drop oldest displayed when it reaches 256 and two are up
            : (fully faded in & no transition) ? elapsed++ ;  elapsed = min(elapsed, G*150)
              pending & elapsed >= threshold -> append pop(pending); elapsed = 0; hold = 0; threshold = its duration
              !pending & elapsed >= G*150     -> showing = 0
  alpha += showing ? +0x10 (cap 0x80) : -0x10 (floor 0);  chain & !showing & alpha == 0 -> release chain
```

## 5. Call chain

```
BattleFormula_ApplyTargetResult 003112F0 -> BattleFormula_ApplyResultMetadata 00385BA0
  -> (result +0x1C == 1) BattleFormula_DispatchPostResultEvents 00469EC0(02AEDFD4, source, target, result)
     -> ctx {source, target, result+8, |delta|, status, level, result+0x38, action}
     -> +0x140 bits 8-11 -> 0x36/0x38/0x3A/0x3D
     -> target without a unit: HP/MP/status/reserve events 0x13-0x23
     -> target with a unit: 0xA9 & kind 6 -> 0x33/0x34 (bit 23) ; kind 0 & row +0x1E in {2,7} -> per-action ids ; 0xB1 -> 0x3B
        -> 0046A870 -> 0046AC90 list 02EBB540 -> 0x2D-0x32
  -> 0046AB10(stats, event, ctx) -> 00469570 -> ring 02EBB560 -> 005369C0 -> 00536410 / 0035B990 (presentation)
  rows: [02EBF018] = battle_message.bin (102 x 8 B + heap)
```

## 6. Modding notes

- **A message is a row and a text**: adding a line for an action means a row in
  `battle_message.bin` (slot kinds in bytes `+0`–`+2`, `+5`; bit 7 of `+3` to bypass the visibility
  filter; bit 0 of `+4` to rate-limit) *and* an immediate in the dispatcher — the action-to-event
  map is code, not data.
- **Actions `0x1FF` and above are silent** by the poster's first test, whatever the table says.
- **The rate limit is per `(event, unit)` for `0x1C2` frames** scaled by the frame factor at
  `01DFE0B4`; only rows with `+4` bit 0 are limited (`0x05`–`0x0C`, `0x4F`–`0x62`).
- **The steal messages are keyed to action `0xA9` by an immediate**: a second steal-like action
  (recipe 49 on another record) rolls but never reports.
- **Four blank rows are real**: `0x2D`, `0x2E`, `0x2F`, `0x31` — the single-item and gil-first
  steal lines print nothing in the `us` table; a mod that wants "stole a Potion" fills those rows.

## 7. What is not known

- [x] ~~**The battle-log line's lifetime and the slot formatter**~~ **FL-1 ANSWERED 2026-09-12
  (FABLE)** — §2.5 "the last mile": eight slot kinds (names with the A/B letter suffix,
  form-coloured numbers, status / item / action names), the format engine chosen by `00254A10`, and
  the widget's `G × 150`-tick life with `0x10`-per-tick fades and a 40-node pool that recycles the
  oldest pending line. **Residue (narrower):** the escape grammar of the two format engines
  (`002B49F0`, `002B40C0`), the runtime-filled style table `020BE610` and palette `0215E6C8`.
- [x] **FL-2.** **The live check of the binding**: `[02EBF018]` header `+4 == 102`, `+8 == 8`, and one steal *(closed — the register row is WITHDRAWN.)*
  producing ring entries `0x33` / `0x34` at `02EBB560`. **FL-2.**
  *Narrowed 2026-09-15 (FABLE) — the STATIC half is closed, the live half is untouched.* §2.5 now traces
  the load in five steps from `002368D0`'s `003843F0(0x13, 00238850, "STATIC")` to
  `003845F0(&02EBF018, (i32)[pack + 0xC])`, with the manifest `01E4D830` naming directory entry 2
  `battle_message.bin` and the entry proved byte-identical to the sibling file in all nine languages.
  **The row stays open**: no process was read, and the steal's ring entries are unobserved. That is a
  runtime question and it is queued for whoever holds `@runtime`.
- [x] **UQ-113.** **Which situations hand the dispatcher a target with no owning unit** — the menu on reserve
  members is what the texts say; the caller that does it is not read. **FL-3.** *Narrowed
  2026-09-12 (FABLE):* the dispatcher is reached only through `BattleFormula_ApplyTargetResult`
  (`003112F0`), whose callers are `Battle_ProcessActionTarget` (from the two timeline-event
  handlers), the periodic maintenance, and the two status modifiers `0030E130` / `0030E360`.
  The status modifiers are what the **script status verbs** reach — `setcharbattlestatus` /
  `clearcharbattlestatus` (`01F0` / `01F1`, `01FC` / `01FD`) through `004737D0` / `00473690` →
  `00318A90`, `setpartybattlestatus` / `clearpartybattlestatus` (`04E8` / `04E9`) through
  `00473820` / `004736D0` → `00318A00`, and `btlAtelSetStatus` (`3002`) through `005103B0` →
  `002394C0` — each resolving a member's stats record from a script handle, reserve members
  included; ~~so a script status change on a reserve member is one proven unit-less path~~. The field
  menu's own item use is **not** among the applier's callers, so which of these (or what else)
  posts the menu's reserve lines is the remainder.
  **ANSWERED 2026-09-14 (FABLE).** This is a static read, and it corrects the narrowing above.
  - **The status verbs never reach the dispatcher.** `BattleFormula_ApplyResultMetadata` dispatches only when
    result byte `+0x1C == 1` (`00385C6F`).
    - `0030E130` / `0030E360` build their records with `00386A50` / `00386A70` / `00386AE0`. All three start
      from `BattleFormula_InitializeResultRecord` (`003848E0`), which memsets `+0x08`–`+0x147`.
    - None of the three writes `+0x1C`, and between the build and the apply call the callers only test
      (`0030E2BE`, `0030E610`).
    - Nothing is called between the build and the apply (`0030E2BC`–`0030E2DA`, `0030E60E`–`0030E638`).
    - A displacement census of every write to `+0x1C` in the executable finds four byte-`1` stores. The
      resolver's, at `00386855`, is the only one in battle code; the others are `00185A1D`, `0079238F` and
      `007D0A10`.
    - So a script status change on a reserve member applies, but posts nothing.
  - **The applier's resolver-backed call sites.** Four of its seven call sites apply a record that
    `BattleFormula_ResolveTargetResult` produced:
    - `00307ABD` (resolved at `00307577`) and `003110AB` (resolved at `0031108C`) target a unit's own
      `+0x698`, so they always go to (d).
    - `00307436` (resolved at `00307419`) targets `BattleStats_GetByBattleSlotIndex` of each byte in the
      source unit's list `+0x6B9`, count `+0x6B6` (`003073D7`–`00307449`).
    - `0031126C` (resolved at `0031124D`) is the pickup service.
  - **The reserve route — a command issued to a slot, not to an actor:**
    1. **Menu.** `BattleMenu_UpdateCommandSelectionAndDispatch`, in target mode `0xF`, calls the fan-out
       issuer with **target handle 0** and the chosen list entry's slot byte `[menu + i·8 + 0x510]`
       (`0027866C`–`0027869B`). Mode `0xF` is category `0x12` in the mode table `01E0C398`, set at
       `0027E122`–`0027E12C`. The issuer's other caller, `00311CD0` (five call sites), always passes slot 0, and
       the defeat step `003138D0` passes a handle.
    2. **Issue.** `BattleUnit_IssueCommand` sees handle 0. It sets `+0x6B0` bit 1 and parks the slot at
       `022C1DB8[unit +0xEA9 × 12]` (`00311D8C`–`00311DA5`).
    3. **Commit.** `BattleUnit_CommitAction` finds bit 1, copies the parked slot to `+0x6B9` and sets
       `+0x6B6 = 1` (`0030F865`–`0030F894`).
    4. **Target set.** `Battle_BuildActionTargetSet` enters with `+0x6B6` set.
       - If the action row's area byte `+6` is non-zero (`0030D20E`), it replaces the list with the stats
         slot bytes of class-3 map indices 4–8 — [the reserve](../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md)
         (`0030D217`–`0030D249`).
       - Otherwise the single slot stands (`0030D211`).
    5. **Dispatch.** `Battle_ProcessActionTarget` resolves and applies each listed slot. A slot with no
       unit reaches (c).
    6. **Which line.** The "resolved member" (c) compares against is `+0x6B9[0]` (`0046A120`–`0046A14B`).
       - A single-target command posts its reserve line for the chosen member.
       - An area command posts it once, for the first reserve member in map order. The rest match
         "nothing more" for the listed actions.
  - **The pickup service** (`00311146`–`0031126C`) is the only other unit-less route.
    - It runs action `0xF5` with **no source** on each class-1 map member of indices 0–8 whose stats pass
      the `0x80000003` gate. For pickup kinds 3 and 5 it keeps only the picker's own member.
    - A member without a unit reaches (c). With a null source the resolved member is null (`0046A17D`),
      so only the general HP / MP / consciousness lines can post.
    - Whether class 1 ever lists a member without a unit is not read here.
  - **Not claimed:**
    - Nothing was executed.
    - Which menu entries carry category `0x12` is not read.
    - Block copies of a result record are not excluded by the census. Every apply site's record, though, is
      a local that is memset and built immediately before the call.
- [x] ~~**The remaining posters' conditions** — ~~`004698C0` (390 B),~~ `00469C00` (549 B), `0046A9D0`,
  `0046AA70` — read only for their event ids here.~~ **All three read 2026-09-12 (FABLE):**
  **`0046A9D0(_, kind)`** — the trap line, keyed by the authored field-action kind its one caller
  `BattleUnit_TryTriggerNearbyAuthoredFieldAction` passes: kind `0x104` → `0x01` ("… healing
  nearby allies"), `0x105` → `0x02` ("… energizing nearby allies"), `0x103` → `0x03` ("… Your pockets
  feel lighter"), anything else → `0x00` (the plain "triggered a trap"), `0046A9F8`–`0046AA60`.
  **`0046AA70(unit, _, _, item, count, gil)`** — the combined obtain poster: `0x25` when `count ==
  1`, `0x24` otherwise, only for an item that is not `0xFFFF` with a non-zero count
  (`0046AAC0`–`0046AAE0`); then `0x26` when `gil` is non-zero (`0046AAE5`–`0046AAF6`); callers
  `0035DF40` / `0035E070` (UI). **`00469C00(mask, begin)`** — the seven **magick fields**: for each
  set bit *i* of `mask` (0–6) it tests the active-field word `022C314C` through `0031A900` and posts
  the begin line `0x4F + 2i` when `begin` and the field is not yet active, or the end line
  `0x50 + 2i` when `!begin` and it is (`00469C30`–`00469D1F`, `00469D2A`–). The wrappers set or
  clear the word afterwards — `0031A910(mask)` (**`set_field_effect`**, `04F5`) and `0031A8C0(mask)`
  (**`clear_field_effect`**, `04F6`), both also reached from
  `BattleUnit_ExecuteDirectStateCommandOrder`. The seven bits, from the rows: 0 HP drain, 1 MP
  drain, 2 no Attack, 3 no Magicks, 4 no Technicks, 5 no Items, 6 the magnetic field. `004698C0` read 2026-09-11: it builds a
  `{sourceUnit, targetStats, gil = result +0x08, …, actionId}` context and posts through
  `0046AB10(unit, id, &ctx)` only for action `0xB5` on a kind-2 / 7 row — id `0x3A` ("Technick
  failed. Not enough gil.") when result flag C bit 11 is set, `0x39` otherwise (`004699F5`–
  `00469A26`); it also parks the source unit / owner in three globals (`004698F1`, `00469918`,
  `00469944`) before the post. **FL-4 ANSWERED** (all four posters read; ledger closed 2026-09-12).
- [x] **UQ-114.** **What a kind-4 slot renders against its empty sub-format** (message entry 99, the falsification note
  below), and whether any shipped row carries slot kind 4. **PE-1.**
  **ANSWERED 2026-09-14 (FABLE):** an empty string, and no shipped `us` row carries kind 4. See the answer under
  "The kind-4 sub-format is the empty string" below.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The dispatch condition and arguments | `00385C6F`–`00385C85`; `02AEDFD4` stored at `00385FE4` | 1 | PROVEN |
| The two worlds | `00469FE5`–`00469FF9` | 1 | PROVEN |
| Every event id and its condition (§2.2) | `00469F68`–`0046A617`, all immediates | 1 | PROVEN |
| The poster's drop, filter, rate limit, ring | `0046AB19`–`0046AC66` | 1 | PROVEN |
| The filter | `00469584`–`00469685` | 1 | PROVEN |
| The row layout the realiser reads | `00536A51`–`00536BBC`, `00536C6F`–`00536C84` | 1 | PROVEN |
| The file's rows and texts | `battle_message.bin` (`us`, 6,668 B) decoded; `in` and `kr` copies have 100 rows and other glyph sets | 1 (authored data) | PROVEN |
| `02EBF018` is filled from `battle_message.bin` | content agreement on every id the code posts, **and now the load**: `002368D0` → `003843F0(0x13, 00238850, "STATIC")` → `00238850` → `003846F0(&0208E680, blob, 0)` + `00236C30(1)` → `003845F0(&02EBF018, (i32)[pack+0xC])`, directory entry 2, which the manifest `01E4D830` names `battle_message.bin`; pack entry 2 is byte-identical to the sibling file in all nine languages | 1 + 2 + 9 | TRACED statically; the live read is still owed (`FL-2`) |
| The slot formatter's eight kinds and the two engines | `00536410` read whole; jump table at `0053699C` `{00536568, 00536568, 00536856, 0053668C, 005365EC, 00536856, 00536742, 005367BF}`; `00536190`, `00536280`, `002B58F0`, `0035D400` / `0035D430`, `00D10C60` bytes | 1 | PROVEN |
| The line's `G × 150`-tick life, the fades and the pool | `002BDB20`–`002BDB2A`; `002BE8D0`; `002BEAC0` read whole; `002BF010`, `002BEE00`, `002BF480`, `002BED30` | 1 | PROVEN (static) |
| What the line looks like on screen | the engines' escape grammar and the runtime palette are not read | — | PARTIAL |

## 9. Related

- [`../applying-a-result-to-a-target.md`](../applying-a-result-to-a-target.md) — step 1 is the metadata applier.
- [`../../08-Combat-Formula/Steal/the-steal-roll.md`](../../08-Combat-Formula/Steal/the-steal-roll.md) — where bit 23 and the kind come from.
- [`../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md`](../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md) — `00469BB0` posts `0x10`.
- [`../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md`](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md) — `0046A800` posts `0x11` / `0x12`.
- [`../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md`](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) — the heap layout and charset.
- [`../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md) — slot 7.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

This page rests on two different kinds of evidence — function bodies in the EXE, and a file inside
the archive — so both were re-derived from their own sources. **`battle_message.bin` (us) was
extracted from `FFXII_TZA.vbf` again and decoded from its header down**, rather than read out of the
published TSV: checking prose against its own evidence file only tests transcription.

| claim | measured |
|---|---|
| the table has **102** rows | **102**, two independent ways — `(0x350 − 0x20) / 8` from the header's own offsets, and the text sub-header's own `count` field |
| the published `battle-message-rows.tsv` | **all 102 eight-byte row records agree with the archive, byte for byte** |
| `0x10` / `0x11` / `0x12` | decoded from the charset: **"… has fallen."** / **"… is cast into the void."** / **"… turns to stone."** |
| `005369C0` **1,000 B**, `00536410` **1,420 B**, `0046AB10` **371 B** | all three exact |
| `0046AB10` has **48** sites, and **17 other functions** call it | **48 sites in 18 functions**, zero tail jumps — 17 others plus `0046A800` |
| `00254A10` is true for state `{0, 7, 8, 10, 11}` | `cmp eax, 0xb` / `mov ecx, 0xd81` / `bt ecx, eax` — **bits 0, 7, 8, 10, 11** |
| the palette table `00D10C60` | **`18 19 1A 1B 14 15 16 17 1D 1D 1C 1C 1E 1E 1F 1F`** — all sixteen bytes |
| the ring is **10 × 32 B** at `02EBB560`, index `02EBB54C` | **confirmed twice**: the scan's own bounds `02EBB560`…`02EBB6A0` are `0x140` = 10 × 32, and the wrap at `0046AC43`–`0046AC5B` is `(index + 1) mod 10` |
| the poster drops when `context.dw_28 ≥ 0x1FF` | `0046AB19 cmp dword ptr [r8+0x28], 0x1ff` / `jge` |
| the kind-4 sub-format is at **entry 99** via `+0x14 → +4 → +0x190` | the chain is exactly that, three `ImageAddress_ResolveRuntimePointer` calls, and `+0x190` lands on **offset-table slot 99** |

### The poster's caller set is closed in both directions

§2.7 names **17 distinct functions** across its 15 rows — two rows carry more than one, which is why
a row count and a function count differ here. Checked against the image:

- **every one of the 17 is a real caller** — none listed that does not call `0046AB10`;
- **exactly one caller is missing from the list**, and it is `00469EC0`
  `BattleFormula_DispatchPostResultEvents` — **the dispatcher itself**, which is precisely what
  "the *other* posters" excludes.

So the 18 calling functions are **17 other posters + the dispatcher**, and the 48 sites are
**10 in the dispatcher + 38 across the seventeen**. Nothing listed is spurious and nothing unlisted
is unexplained: the census is closed, which is a stronger claim than the totals alone.

### The code reads the file's own header fields

Two numbers the file states about itself turn out to be the two numbers the code reads:

- `[02EBF018] + 0xC` is the **row array's offset** — and `battle_message.bin`'s header holds `0x20`
  at `+0x0C`, which is where the rows are;
- `movzx ecx, word ptr [rcx+8]` at `0046ABA6` is the **row stride** — and the file's header holds
  **8** at `+8`, which is the row size.

So the 8-byte row and the `0x20` base are not conventions read off a hex dump; they are fields the
loader and the poster both consult. A reconstruction that changes either must change the header.

### The rate limit is live for 28 of the 102 events, not all of them

The dedup scan runs only when the event's row has **`+4` bit 0**. Across the whole table that bit is
set in **28 rows** — ids `0x05`–`0x0C` and `0x4F`–`0x62` — and clear in the other **74**, which post
unconditionally. Neither dead code nor a universal rule.

The window itself is `imul ecx, [01DFE0B4], 0x1c2`, and `01DFE0B4` is **the frame base** — the word
the boot path sets from the frame rate ([the periodic tick](../../10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md)
§5). The image initialises it to **1**, and across the whole image it has **212 references and
exactly one writer**: `001EDDF2 mov dword ptr [rip], 2`, inside `001EDDC0`, on that function's
`ecx != 0` branch.

So the dedup window is `0x1C2 × base` — **450 frames at 30 fps and 900 at 60: the same wall-clock
wait either way**, exactly like every other authored duration. And it is the *same* word that scales
the status beat timer (`003876D0`, × 30) and every status duration: **one global, one writer, 212
readers, standing in front of three unrelated subsystems' timings.**

> **Corrected later the same day (OPUS).** An earlier draft of this section called it "a tuning slot
> currently unity", which reads as a constant. It is not — it is 2 at 60 fps.

### Two bytes of every row are always zero

Over all 102 rows, `+6` and `+7` are **zero without exception**, and `+5` — slot 3's kind — is
non-zero in only **6**. The record is eight bytes wide and the shipped data uses six of them.

### The kind-4 sub-format is the empty string (`PE-1`, new)

The pointer chain is exactly as §2.5 describes it and lands on **entry 99**. Entry 99's row is
**all zeros and its text is empty** — in this decode and in the published TSV alike. So
`002B4090(0x20, buf, fmt99, …)` formats a kind-4 number against an **empty format string**. The page
names the entry without saying what is in it, and what an empty format does inside `002B4090` was not
traced here. Recorded as a question rather than resolved: **`PE-1` — what a kind-4 slot renders when
its sub-format is empty, and whether any shipped message actually uses kind 4.**

**Answered 2026-09-14 (FABLE).** This is a static read of the shipping image and the published TSV. Nothing was
executed.
- **A kind-4 slot renders nothing.**
  - `002B4090` (37 B) passes its varargs as a `va_list` to `002B49F0`.
  - That engine's first test is `cmp byte [fmt], 0` (`002B4A53`). On an empty format it jumps to `002B4BB0`,
    stores `0` at `buf[0]` and returns −1 (`002B4BB0`–`002B4BDB`), without reading an argument.
  - `00536410` ignores the return value. It hands the slot the address of that buffer (`00536728`–`0053673D`,
    stored at `00536859`).
  - So the slot's argument is an empty string. The slot's int and the four colour values are gathered and dropped.
- **Which byte holds which slot's kind**, from the code:
  - Slot 3 (`cmp r13d, 3` at `00536497`) reads `[row + 5]` (`005364E2` / `005364F1`).
  - Slots 0–2 read `[row + slot]` (`00536547`).
  - Any kind above 8 fails the bound at `00536551`–`00536554` and takes the raw-int default `00536856`.
- **No shipped row selects kind 4.** Counted over the 102 rows of `battle-message-rows.tsv` (kind: rows):

  | byte | slot | kinds present |
  |---|---|---|
  | `+0` | 0 | 0: 29 · 1: 33 · 2: 34 · 3: 1 · 7: 4 · 8: 1 |
  | `+1` | 1 | 0: 57 · 1: 2 · 5: 2 · 6: 1 · 7: 6 · 8: 30 · 9: 4 |
  | `+2` | 2 | 0: 80 · 1: 2 · 2: 13 · 3: 1 · 7: 1 · 8: 1 · 9: 4 |
  | `+5` | 3 | 0: 96 · 1: 6 |

  No kind byte in any row is 4. Kind 9 appears in eight slots, and those take the raw-int default.
- **Scope.**
  - This covers the `us` table the TSV was decoded from. The other language files' row bytes were not decoded.
  - No runtime writer of the loaded table's row bytes was searched.
  - "No message uses kind 4" is therefore a claim about the shipped `us` rows. It says nothing about what the
    formatter can do.

**Not claimed:** nothing here was executed or observed live. `002B4090`, `00536280` and the
presentation side were not re-read; the charset decode covers the letters, digits, space and the
punctuation these rows use, not the whole table.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `00571710` | 488 | post-result UI body (caller `00571900`): `005722E0`, `005723C0`, `002DD7E0`/`002DD7B0`, `00254A10`, `0020E620`, `0029FF60` |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings (the image-address resolver, the audio request chain) are recorded in the registry, not here.*

- **Movement — CLIENT.** The battle event poster `0046AB10` is called by a 160-byte poster client, and that client is
  itself called by `BattleLocomotion_SolveDefaultStep`. **Locomotion can post battle messages.** Which messages it posts
  is not read. Two locomotion bodies look up stats owners, and the frame-base setup `001EDDC0` (the `timeBeginPeriod`
  body) calls a 71-byte movement helper.
- **Gameplay — SERVICE and CLIENT.**
  - `002FA3B0` is called by `BattleUnit_SubmitResultReactionMode`. It measures the party leader's distance with the
    3-D distance helper.
  - `00309E70`, `0035E070` and `00536410` call the 8,136-byte id-query body.
  - The status paths dispatch presentation events, update the engagement flag and ask the id-validity query.
- **RNG_Random_Selection — SERVICE.** The status-add tail `002394C0` draws the **shared gameplay LCG** before
  `BattleStats_AddStatusMode3`. **A script-added status roll is on the loot stream**
  ([which roll](../../21-RNG-And-Determinism/which-roll-is-on-which-generator.md), §3 challenge).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Rewards_Progression_Economy — SERVICE.** `0030E360` on this page calls `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer. What it reaches is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — SERVICE (SWE2-CONTRACT 2026-09-15, 2 edges).** `0030E130` calls `GambitConfig_AdjustAvailableEntryCountByStatsRecord` `003279B0` — the post-result pass adjusts the gambit layer's available entries; `BattleUnit_TrySelectAndCommitAiOrderFromSet` shares `004697C0`. One real call plus fan-in.

**CoreRuntimeScheduling — SERVICE (SWE2-CONTRACT 2026-09-15, 21 edges).** Pointer-codec fan-in: fifteen
cited bodies decode through `ImageAddress_ResolveRuntimePointer` `0020E600`, three encode through
`RuntimePointer_EncodeImageAddress` `0020E620`, and `0046AB10` also reads
`GameClock_GetRawTickCounter` `0032A150`; plus `001EDDC0`←`0022BDF0` and `00254A10`→`00229E40`.
The post-result pass encodes and decodes payload pointers through the runtime helpers —
mechanical, not shared ownership.

**PlatformOnlineAchievements — CLIENT.** `003160C0`, owned by that layer, calls `003148F0` —
`WorldTransition_GetActiveOrPendingFieldId`, the transition accessor this page names; the
achievements layer asks the same question when firing its own events. Fan-in, not shared ownership.
Read from `edges.tsv` 2026-09-17 (SWE2-FRONTIER).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. This page cites the dispatch chain, the poster, the realiser and formatter, the `battle_message.bin` load path, and (through the interior-citation and SWE2-EC7 notes above) many small text-engine helpers; each paragraph says which of those the crossing goes through.*

**ActorEntity — SERVICE and CLIENT (27 edges).** The visibility predicate `002FA3B0` calls `Actor_GetWorldPosition` `00265020` (the 24-unit distance to the party leader, section 2.4); `002F8E90` calls `ActorRuntime_GetClassNibble` `00263C20` (the source's one-hot category); `00318A90` and `BattleStats_ResolveByActorHandle` `00320A70` call `ActorWork_GetBattleUnitRaw` `00263E30` and `ActorHandle_ResolveRegistryEntryByPackedId` `003588B0`; the owner lookup `0031B860` calls `BattleUnit_GetBySlotIndex` `00236820` and `BattleUnit_GetSlotCount` `00236850`; the status-add tail `002394C0` calls `ActorWork_GetBattleUnit` `0031B760`; the `clearcharbattlestatus` bodies `00473690` and `004737D0` call `ActorHandle_EncodeRegistryEntry` `003589B0`; `ScriptVM_WaitList_HasAnyActorChannelActive` `00267420` calls `ActorManager_GetRecordByOrdinal` `00358940` and `ActorResource_IsChannelBitActive` `003DB640`; the status write `0030E360` calls the defeat-condition check `00300FC0`, which calls `003138D0`. In the other direction `BattleStorage_InitializeWorkArrays` `002368D0` issues the battle-pack request `003843F0` that loads `battle_message.bin`; `00263E30` is called by `ActorSystem_ReleaseBattleUnitSlotForActor` `00234200`, `0031B760`, `0031FCF0`, `0031FD20`, `00322080` and `BattleGroup_RefreshFourActorDefinitions` `003266C0`; `00263A10` (the actor's `+0x100` word when `+0x102` is non-negative) by `00272C80` and `00272CE0`; `002394C0` by the `btlAtelSetStatus` body `005103B0`; `003148F0` by `ActorManager_RunFieldRuntimePass` `0025D9E0` and `BattleSlotMap_InitializeMappingClasses` `00329CC0`. The post-result paths resolve units, handles, positions and class nibbles through the actor layer, and the actor layer's battle-storage init is what requests the message table; the remaining actor callers use the same small accessors for their own work.

**CombatFormula — SERVICE and CLIENT (102 edges).** The dispatch chain on this page is filed to the formula layer: `BattleFormula_ResolveTargetResult` `00385F60` (which stores the action id the dispatcher reads) calls `BattleFormula_BuildEvaluationContext` `003847C0`, `BattleFormula_InitializeResultRecord` `003848E0`, `BattleFormula_ResetScratchState` `003849B0` and four more; the applier `003112F0` calls the numeric setters and `BattleFormula_ApplyResultMetadata` `00385BA0`, which calls `BattleFormula_DispatchPostResultEvents` `00469EC0`; the status writes `0030E360` / `0030E130` build a transition result (`00386A50`, `00386A70`, `00386AE0`) and apply it through `003112F0`; the filter `00469570`, the posters `004698C0`, `0046A870` and `0046AB10`, `002F8E90`, the slot resolver `00536310` and the realiser `005369C0` call `BattleStats_FindOwningBattleUnit` `0031B860`, `BattleStats_GetByBattleSlotIndex` `00320A40` or `00320A70`; the lethal-line poster `00469BB0` is called by `BattleStats_ModifyHPAndProcessLethalState` `00300530`. `0031B860` is also called by 35 formula bodies in all, `002F8E90` by five formula bodies (among them `00389370` and `0038BC00`), and `BattleStatus_ComputeDefaultShortTimer` `003876D0` by `BattleFormula_AppendStatusAddOperation` `00387BB0`. A resolved result reaches the message ring through the formula layer's own resolve → apply → metadata → dispatch chain (section 2.1), and every poster maps a stats record to its unit with the formula layer's owner lookups; the other formula callers use those lookups for their own resolution.

**Items and Items_Equipment_Shops_License — CLIENT and SERVICE (11 edges).** The gil-message poster `00469E80` (event `0x26`) is called by `InventoryBundleClass09_ApplyGilAndNestedItems` `002FD530`, `Shop_CommitPurchaseItemAndGil` `002FEEB0` and `Shop_CommitSaleItemAndGil` `00310870`; the item-message poster `0046A630` (events `0x24` / `0x25`) by `InventoryPackedCountClass_MutateChannels` `002FD150` and `InventoryBitsetClass_MutateState` `002FD420`; the applier `003112F0` calls the item writer `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` `003008A0`; the equipment and licence setters `0031A410`, `0031A510`, `0031A630` and `00323910` call `0031B860`; and the pack bind `00236C30` calls the battle-data table helper `00238660` (label `Items`), which rebases one section pointer of the bound pack. The "You obtain" item and gil lines are posted by the inventory and shop bodies themselves through two of section 2.7's posters, so the inventory layer is a direct client of the message ring.

**Resource — SERVICE (3 edges).** `BattleStorage_InitializeWorkArrays` `002368D0` and the release arm of `00236C30` call `003843F0` with kind `0x13`, the completion callback `00238850` and the tag STATIC; `003843F0` calls `00384420`. Kind `0x13` is the battle pack, and this is the resource request whose completion callback binds `battle_message.bin` (section 2.5, steps 1–3).

**Save_Load_Settings — CLIENT and SERVICE (4 edges).** `SaveSlotMetadata_BuildSubmissionDescriptor` `005832B0` calls the CJK-locale predicate `00254A10`; `00581930` calls the font-colour getter `002DD7E0`; `WorldTransition_GetActiveOrPendingFieldId` `003148F0` reads the field id at `+0x1044` of `SaveImage_GetPersistentPayloadBase` `002EF2B0` and is called by `SaveImage_FinalizeHeaderAndChecksum` `00583D60`. The realiser's field-id and locale / colour helpers are shared with the save layer: the current field id lives in the persistent save payload, and the save layer's slot-metadata builder and `00581930` use the same locale predicate and colour table.

**Spawn_Encounter_Lifecycle — CLIENT (4 edges).** `SpawnKeep_RotatePersistenceBanksForAreaTransition` `00233780` calls `003148F0` and `GameClock_GetRawTickCounter` `0032A150`; `Spawn_SelectAndPrepareAutomaticEntry` `00235720` and `SpawnEntry_GetElapsedTicksSinceLastDeath` `00235FB0` call `0032A150`. The spawn layer reads the same field id and the same tick counter the poster's rate limit uses (section 2.3); it posts no battle messages through these edges.

**UI — SERVICE and CLIENT (95 edges).** The realiser and formatter run on the UI text engine's helpers, which this page cites in its interior-citation and SWE2-EC7 notes: the format shim `002B4090` (called by nine UI bodies, among them `00292B70`, `002A86A0` and `002D66D0`), the width-context builder `002B3050` (five, among them the battle-menu command list `002C4720`), the text-code strip `002B5680` (`002C4720`, `0056B4D0`), the token sizer `002B1FB0` (the text-code interpreter `002AC5F0`), `002B24B0` (the line-layout pass `002AF340` and the measure pass `002B2150`), the glyph-table selector `0039C4A0` (`002AC5F0`, `002AE610`), the CJK-locale predicate `00254A10` and the locale word `00229E40` (`002AC5F0`, the numeric formatter `002A4430` and eleven more), the font-colour getter `002DD7E0` (twenty UI bodies, among them `00280DE0`, `0028B140` and `00565E00`), the bounded string copy `00254F30` (`002BFD20`, `003F92B0`), `00364980` (`00243860`, `002D66D0`), `0029FF60` (`00559E30`, `00560210`, `005618E0`) and the definition-resolution runtime `0031C5D0` (`00273E30`, `002BFD20`, `0035D380`). The same notes cite the UI's own child-presentation queue (`002BEAC0`, `002BEE00`, `002BF010`, `002BF480`, called by `002BE4F0` and `002BEAC0`) and the clear trampoline `0028A080` with its cited callers (`0028FA70`, `0028FB60`, `00291750`, `002BE450`, reaching `003F8A90`, `003F8EA0`, `0028CA30`, `002BE0A0`, `003FA760` and called by `003C5E50` and `0028F8B0`). Outside the text engine, `BattleMenu_BuildCommandEntryList` `0031EB20` calls `00263E30`; `BattleMenu_UpdateCommandSelectionAndDispatch` `002778C0` and `0027C3D0` call the issuer `00311CD0`; five UI bodies (`0029C530`, `003C5F00`, `003C80C0`, `003F92B0`, `003F9720`) call `003148F0`; and the achievement-gated transforms `005709E0` and `00571F60` call `005760A0`. A battle message becomes a line through the UI layer's text engine, which is why those helpers are cited here; their other UI callers are the rest of the menus and text, which use the same engine and are not about battle messages.

**World — SERVICE and CLIENT (3 edges).** The pack bind `00236C30` calls `003847B0`, and `003847B0` and `00238640` call `AreaData_BindAndRebaseSectionDescriptor` `003845F0`. These are the area layer's authored-data binding callbacks (domain `World.Area`); the message table is bound by the same section binder the area data uses.

**WorldAreaField — SERVICE and CLIENT (35 edges).** The load path binds the table through that layer: `00236C30` calls `003845F0` and `003846F0`, the completion callback `00238850` calls `00236C30` and `003846F0`, `003845F0` calls `003846F0` (which also calls itself), and `BattleData_SetAreaArdSectionCategory` `0023A160` calls both. The realiser `005369C0` calls `MapRef_GetAreaArdFieldResourceIndex` `00264ED0` (itself called by `AreaArd_RefreshForMapRefField` `003EA6E0`) and `003148F0`; `00571900` calls the conditional battle-id resolution `00576A50`, which calls `003148F0`; the status write `0030E360` calls `FieldData_GetActiveFieldRecordBit15` `00377C20`. `003148F0` is also called by twelve area bodies, among them `WorldField_InitializeCurrentFieldRuntimeParameters` `0026D910`, `WorldPersistence_ResetBanksForFieldTransition` `0026DB30`, `00377C20` and `00576A50`; `BattleSystem_InitializeAreaState` `002342F0` calls the removal shim `0030E990`, and `BattleSystem_RunFieldFrameOrchestrator` `00234590` calls `0032A150`. `battle_message.bin` is bound by the area layer's section binder, and the realiser asks the area layer for the current field id and map resource when it fills a line; the other area callers use the same getters for field setup and persistence.

## The `00536410` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

The slot formatter `00536410` (1,420 B exclusive): `00536190` resolves the
context (`00536463`), `01CEB638` is the empty-string fallback
(`00536485`), `r13d` vs 3 picks the arm (`00536497`), `[02EBF018]`
reads + `0020E600` ×3 (`005364A5`–`00536509`), `word[rcx+8]` /
`byte[rcx+5]` kind bytes (`005364C5`/`005364E2`/`005364F1`), and the
`lea 00120000` image-base args feed `0053654C`.

| member | role | interior |
| --- | --- | --- |
| `00536190` (229 B) | context resolver — `[02EBF018]` (`0053619F`), `dword[rax+0xC]` → `0020E600` ×2 (`005361B4`/`005361C8`) | [`005361B4`](../../_index/ADDRESS-INDEX.md) |
| `0035D400` (47 B) | bounded table-map — `ecx` vs 7 (`0035D404`), `byte[rdx + 00D10C60]` permutation map (`0035D417`–`0035D41E`), `002DD7B0` (`0035D422`) | [`0035D41E`](../../_index/ADDRESS-INDEX.md) |
| `0035D430` (35 B) | same map, tail — `ecx` vs 7, `00D10C60`, tail `002DD7E0` (`0035D44E`) | [`0035D44A`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0020E600`, `002DD7B0`, `002DD7E0`.
The `00D10C60` bytes (`18 19 1A 1B 14 15 16 17`) are the slot-kind
permutation the formatter applies before the engine call.

## The `005369C0` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

The realiser `005369C0` (~1,000 B): setup `003148F0` / `00264ED0` /
`002FA390` (`00536A0F`–`00536A23`), `[02EBF018]` context resolves
through `0020E600` (`00536A66`, `00536A7A`, `00536AB7`, `00536ACB`,
`00536C45`, `00536C59`), a `jmp rcx` dispatch (`00536B15`), per-slot
resolver `00536310` ×3 (`00536B1D`, `00536B65`, `00536CB1`),
`0031B860` (BattleStats_FindOwningBattleUnit) → `[02EBF188]` ×4
(`00536B38`, `00536C96`, `00536D0B`, `00536D52`), `00263A10` ×3,
`00536280` (the word→string dictionary helper) ×2 (`00536CBE`,
`00536D34`), then `00536410` (`00536C06`) and `0035B990` (`00536D79`).

| member | role | interior |
| --- | --- | --- |
| `00536310` (253 B) | argument-slot resolver — writes `byte[rdx]` (`00536327`), `[02EBF130]` context (`0053634A`), `dword[rax+0xC]` → `0020E600` (`00536359`), `byte[rcx+5]` kind compare (`00536345`) | [`00536359`](../../_index/ADDRESS-INDEX.md) |
| `00263B40` (8 B) | signed-word getter — `movsx eax, word[rcx+0x102]; ret` | [`00263B40`](../../_index/ADDRESS-INDEX.md) |
| `00267410` (13 B) | non-negative predicate on the same field — `word[rcx+0x102] >= 0` via `setge` (`00267412`) | [`00267412`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0020E600`, `0031B860`, `00263A10`,
`00536280`, `00536410`, `0035B990`, `003148F0`, `00264ED0`, `002FA390`.
The `+0x102` word the two tiny members read is the same field sibling
`00263B50` resolves through the `02098E10` actor records and sibling
`00267420` checks against `dword[rdx+4]` — both adjacent, both outside
this subtree.

## The `002BEAC0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`002BEAC0` (~200 B) — `byte[+0x40B6] & 1` early-out gate
(`002BEAC6`/`002BEAD0`).

| member | role | interior |
| --- | --- | --- |
| `002BEE00` | `qword[+0x40A0]` list walk — null → out (`002BEE00`/`002BEE10`) | [`002BEE00`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — frontier hub `00254F30` (2026-09-17, SWE2-EC7)

`00254F30` — 129 B, 10 A-measured callers at census; the "copied into a `0xA0`-byte slot buffer"
callee. Interior verified: a bounded string copy. If the source fits `r8d` it byte-copies
through the `0x00` terminator (loop at [`00254F50`](../../_index/ADDRESS-INDEX.md)–`00254F7C`)
and returns 0; when the source is longer it calls `00861EBA` (the bounded-copy thunk) with
`r8-1` then writes the terminator at `dst[r8-1]` and returns 1 — truncation is REPORTED, not
silent. Null dst/src return 0 with nothing written.

## Interior citation — frontier hubs `002B3050`, `0039C4A0` (2026-09-18, SWE2-EC7)

`002B3050` — 194 B, 8 A-measured callers; the width-context builder measured beside
`002B5680` above. Interior verified: a `0xA0`-byte stack context is initialised by
`002AC1E0` (`002B3082`), `0039BAD0(rcx)` returns the record kind byte at `002B309B`, and when
`00254A10()` is 0 and the kind is 7 the flag dword at `[rsp+0x64]` gains bit 11 and
`0039C4A0(bit11)` publishes the selected table pointer into `[rsp+0x80]` at
[`002B30C5`](../../_index/ADDRESS-INDEX.md); `002B3120(ctx, rdx, r8, r9)` then consumes the context at
`002B30EA`. Stack-cookie checked (`00808C40`).

`0039C4A0` — 24 B, 9 callers; the glyph-table selector the "Wolf A / Wolf B" suffix above
calls. Interior verified: [`0039C4AB`](../../_index/ADDRESS-INDEX.md)–`0039C4B7` — when `ecx` is non-zero and
`[03AEE808]` is non-null it returns `02AEE808`'s pointer, otherwise `02AEE800`'s; two
adjacent mode-selected globals, no locking, no mutation.


## Interior citation — frontier hub `002B4090` (2026-09-18, SWE2-EC7)

`002B4090` — 37 B, 34 callers; the format-engine shim that selects `002B49F0` for this
page's message-table rows. Interior verified: `r8`/`r9` spill to the caller's homing space
(`002B4090`–`002B4095`), a zeroed out-dword is built at `[rsp+0x20]`, `r9` is rebound to a
stack record (`lea r9, [rsp+0x58]`), and `call 002B49F0` runs at
[`002B40AB`](../../_index/ADDRESS-INDEX.md). The wrapper exists to attach the scratch record
the engine expects.


### Interior citation — frontier hub `002DD7B0` (2026-09-18, SWE2-EC7)

`002DD7B0` — 35 B, 6 callers. A bounds-checked byte getter: `ecx` must be
non-negative and below `dword[0215ECB8]`, the table pointer `[0215ECC0]` must be
non-null, then `byte[rdx + rax*8 + 4]` ([`002DD7CA`](../../_index/ADDRESS-INDEX.md))
is returned — the flag byte at `+4` of each 8-byte record. Any failure returns
`al = 0`.

### Interior citation — frontier hub `00320A70` (2026-09-18, SWE2-EC7)

`00320A70` — 55 B, 4 callers, `BattleStats_ResolveByActorHandle`: bit
`0x10` of `byte[02089340]` gates the lookup — `003588B0()` then
`00263E30(rax)`, returning `[rax+0x698]` at
[`00320A94`](../../_index/ADDRESS-INDEX.md) or 0 on any failed step.
## SWE2-EC7-21 update (2026-09-18) — `004697C0` message-table arm fragment

`004697C0` (251 B) is a deduplicated message-post for one of this page's table
rows: it word-captures `dx→edi`, `r8w→ebp`, `r9d→esi` into a five-qword stack
record (`004697C0`..`004697FB`) and runs `002F8E90(rbx)` as the precondition
(`004697FF`). When it returns 1 with `esi==4`, `bp < 0x21F`, and `di ∈
{0x4022, 0x4124}` (`00469809`..`0046982A`), the `02CA6028`/`02CA6030`
last-posted pair suppresses a repost (`0046982C`..`00469843`); otherwise the pair
is updated and `bp != 0x96` falls to `edx=6` → `0046AB10` (`00469894`..`004698A1`).
The alternate arm (`0046985F`) re-checks `002F8E90` for `di < 0x21F`, `di != 0x96`,
and maps `esi` 1/2/3 → `edx` 5/7/6 (`0046987B`..`00469899`) before the same
`0046AB10` post. The kind→code table feeding the `0x06`-family interrupt/cancel
messages this page names.

## SWE2-EC7-28 update (2026-09-18) — `002B5680` control-strip copy

`002B5680` (166 B) is the copy loop this page's `0xA0`-context measure
names: walks `r8` text, `002B1FB0` sizes each token, accumulates into
`r12` via `00861EBA` while `ebp + token < r13d` — but drops tokens
`== 0x02` and `0x0F 0x3C` ("<") from the output, still advancing the
source. NUL-terminates, returns `ebp` (0 on overflow). The
control-code strip the message width-measure runs. Interior anchor
`002B56C5` (the skip test).

## SWE2-EC7-38 update (2026-09-19) - `00571710`

`00571710` (488 B) is a post-result event body - `005722E0`/`005723C0`/`002DD7E0`/`002DD7B0`/`00254A10`/`0020E620`. Interior anchor `00571748` (a `005722E0` call).

## SWE2-EC7-41 update (2026-09-19) - `002B3120`

`002B3120` (348 B) is the `(ctx, rdx, r8, r9)` context consumer the page names - `009166EC`/`01F44830`, `002B24B0`/`00808C40`. Interior anchor `002B3233` (a `002B24B0` call).

## SWE2-EC7-42 update (2026-09-19) - `00571900`

`00571900` (322 B) is a post-result body - `00D236F0`/`00D236FA`/`01F44830`, `00576A50`/`005722E0` pair/`005723C0` pair/`0020E620`/`005760A0`/`00571710`/`00808C40`. Interior anchor `00571979` (a `00576A50` call).

## SWE2-EC7-42 update (2026-09-19) - `002B40C0`

`002B40C0` (297 B) is a post-result body - `01F44830`, `00861EC0`/`002B4810`/`002B49F0`/`00808C40`. Interior anchor `002B40FB` (an `00861EC0` call).

## SWE2-EC7-45 update (2026-09-19) - `003937C0`

`003937C0` (237 B) is the bounded-copy body - `00364980`/`00861EBA`. Interior anchor `003937F2` (a `00364980` call).

## SWE2-EC7-47 update (2026-09-19) - `005722E0`

`005722E0` (214 B) is a call-free byte-indexed flag applier - `rdx` bytes index the `[rcx+0x10]` pointer table (`0xFF` skips), `(slot+0x8) = (slot+0x8 & ~1) | (r8 & 1)` per named slot. Interior anchor `005722E5` (the first index load).

## SWE2-EC7-48 update (2026-09-19) - `002BED30`

`002BED30` (203 B) is a body - `00861EC0` single call. Interior anchor `002BED7F` (the `00861EC0` call).

## SWE2-EC7-49 update (2026-09-19) - `002BF010`

`002BF010` (197 B) is a call-free intrusive-list unlink/relink on `[rcx+0x40A0]` - `[+0x188]`/`[+0x190]` head/tail splice, `+0x40B8` = `0x100`. Interior anchor `002BF013` (the `+0x40A0` head load).

## SWE2-EC7-51 update (2026-09-19) - `00318A90`

`00318A90` (174 B) is a body - `00263E30`/`003588B0` plus a `call rax` indirect. Interior anchor `00318AAC` (a `00263E30` call).

## SWE2-EC7-62 update (2026-09-19) - `005723C0`

`005723C0` (149 B) is a call-free flag propagator - `byte[+7]`/`byte[+9]` indices (`0xFF`=none) into `[rbx+0x10]` pointer table, `&~1 | (r8d&1)` into `[+8]` bit 0 on up to 3 elements. Interior anchor `005723EA` (the `[+8]` bit-0 write).


## SWE2-EC7-74 update (2026-09-19) - `0030E990` forwarding shim measured

`0030E990` (35 B) is the shim the post-result bodies call: `r9d`
zeroed, `[rsp+0x78]` forwarded at `rsp+0x28`, two zero stack slots,
then `0030E360` - the arg-repack the message-table bodies share.
Interior anchor `0030E9A9` (the `0030E360` call).

## SWE2-EC7-91 update (2026-09-20) - `0039BAD0` table membership probe measured

`0039BAD0` (39 B) is the membership test the post-result
callers run: slots 1..7 of an 8-entry `rip` qword table are
scanned for `rdx` - returning the boolean of a hit.
Interior anchor `0039BAE7` (the compare).

## SWE2-EC7-100 update (2026-09-20) - `002BF480` measured

`002BF480` (101 B) is the head pop `002BE8D0` and
`002BEAC0` call on the `+0x4098` list: the head node's
`+0x188` link becomes the new head, `+0x190`/`+0x188`
back-links are patched on both neighbours, the node's two
links are zeroed, and the node returns - the standard
unlink the message table's queue drains through.
Interior anchor `002BF4A9` (the neighbour patch).

## SWE2-EC7-102 update (2026-09-20) - `0028A080` measured

`0028A080` (13 B) is the fixed-size clear
trampoline `0028FA70`, `0028FB60` and `00291750`
call: `00861EC0` tails a `0x440`-byte zero fill at
`rcx` - the shared memset the post-result and save
arms reach through.
Interior anchor `0028A082` (the `0x440`
constant).
