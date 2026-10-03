---
system: One word decides which subsystems tick — sixteen gated groups over fifteen distinct bits
category: 00-Engine-Core-Runtime
status: AUDITED — the other fourteen groups (UQ-28, ten by mechanism and four by call shape) and the node type (UQ-25, the target-line object) answered 2026-09-17; UQ-27 and UQ-29 closed earlier
owner_layer: PrimaryOwner:CoreRuntimeScheduling (the pump) — the fifteen callees are owned elsewhere
evidence_tier: 1
readiness: SEMANTICALLY IDENTIFIED
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 72 addresses cited - 21 data, 40 entry, 11 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
falsification_passes: 2
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-frame-gate-pass-1
  crossref_clean: true
  reopened_count: 1
---

# One word decides which fifteen subsystems tick — sixteen gated groups over fifteen distinct bits

> **Count restated 2026-09-11 (OPUS-FRAMEGATE-16TH):** the word has fifteen distinct bits in use, but bit `0x0002` gates **two** groups, so a reimplementer counting groups needs **sixteen** — the sixteenth (`0x0800`) reached by the tail jump this page's §3 note already records. "Fifteen" below counts bits unless it says groups.

## 1. What the player sees

Nothing, when it works. **A single ~~16-bit~~ 32-bit word *(corrected 2026-10-02, OPUS: eight of its sixteen tests are `test dword`, e.g. `0028E290+0x16F`, and it ships `FF FF FF FF`; only its low sixteen bits are tested)* decides, every frame, which sixteen groups of
updates run at all** (over fifteen distinct bits) — and a bit that is clear does not slow a subsystem down or degrade it. The
subsystem simply does not happen that frame: no movement, no redraw, no reaction.

That is the shape of a subsystem-disable facility — and **in this build there is no hand on the
switch** (2026-09-11, OPUS-CONTRA-GATEWORD, §10). The word ships in `.data` as `FF FF FF FF`;
nothing in the executable stores to it, takes its address or encodes it anywhere; so every one of
the sixteen groups runs on every frame the pump runs. Loading screens, pauses, cutscenes and menus
do not act through this word — their mechanisms are elsewhere ([the world-tick page](../Battle-Frame/the-world-tick-and-the-field-frame.md)
for the tick modes and the battle-state word). What the word records is a development control
compiled to always-on: sixteen unconditional tests against a constant.

## 2. The pump, and where the switch sits

```
CoreRuntimeScheduling
  -> 0022A580 -> 0022A770 ┐
  -> 0022B7E0             ├-> 002507C0 -> 0028E290      the fan-out
                          ┘
0028E290
    test byte [01E0C464], <mask>   x15   <- corrected 2026-10-02, OPUS - 16 tests: 8 test byte (masks below 0x100) and 8 test dword (0x100-0x8000), 0028E290+0x4 to +0x2BE
    je   <skip this group>
    call <the group's update>
```

**`01E0C464` is one enable word and every gate reads it.** Sixteen `test` sites, fifteen distinct
masks — never a different global, never a computed index. So the whole fan-out is one bitfield.

**The duplicated mask is `0x0002`**, tested at `0028E2B7` and again at `0028E3AE`; that is what makes
sixteen sites out of fifteen masks. The two sites gate different calls, so bit 1 controls two
separate groups at two points in the frame.

**The sites are not all the same width, and the earlier wording here — *"every one is `test byte`"* —
was wrong for half of them.** Re-derived with a tool: **8 are `test byte`** and **8 are
`test dword`**.

| access | bits it can reach | sites |
|---|---|---:|
| `test byte ptr [01E0C464], imm8` | `0x0001`-`0x0080` | 8 |
| `test dword ptr [01E0C464], imm32` | `0x0100`-`0x8000` | 8 |

A byte test cannot reach past bit 7, so the high half of the word **must** be read wider. A
reimplementation that took the old sentence literally and made the enable a `uint8_t` would lose
eight of the fifteen groups.

**Bit 4 (`0x0010`) is absent, and it is the only absentee.** **Fifteen** distinct bits are used —
every bit of the low 16 except `0x0010`, which appears nowhere in the function. Whether it is
retired, reserved, or handled elsewhere is **not established** *(answered: see section 7, UQ-26, NO ADMISSIBLE SOURCE, signed 2026-09-16; 2026-10-02, OPUS)*. *(This paragraph previously said
"fourteen consecutive bits", which undercounted by one and described a contiguous run that does not
exist: the used set has a hole at `0x0010`.)*

## 3. The sixteen groups — fifteen distinct masks, `0x0002` used twice

| bit | calls made when the bit is set | owner |
|---:|---|---|
| `0x0001` | `00289970` (35 B) | — |
| `0x0002` | `001EDE80` (61 B), `003F8B40`, `00291B90`, `003F6100`, `003F24D0`, `003F24A0` | CoreRuntimeScheduling, Presentation |
| **`0x0004`** | `002917E0` (930 B), **`0028C4C0`**, `0028C4B0` → `0028D1C0` | **UI** |
| `0x0008` | `003F6BB0` (1,051 B), `003F7050` | UI |
| `0x0020` | `003F9F40` (536 B) | — |
| `0x0040` | `003F80D0` (14 B) | — |
| `0x0080` | `00296860` (223 B) | — |
| `0x0100` | `003F8EC0` (284 B) | UI |
| `0x0200` | `003F31B0` (164 B) | — |
| `0x0400` | `003FA790` (143 B) | UI |
| **`0x0800`** | **`0028C870`** (197 B) — a **tail call**, `jmp` not `call`, on `[0209BE80] + 0x7EA0` | — |
| `0x1000` | `00273900` → `0030C300` | — |
| `0x2000` | `00290CF0` (243 B) | UI |
| `0x4000` | `00290EB0` (319 B) | — |
| `0x8000` | `002C6180` (295 B) | — |

> **CORRECTION 2026-09-08 — the table was missing a group, and the reason is instructive.**
> It listed **fourteen** rows while the prose above it counted **fifteen** masks, and nothing
> reconciled the two. The missing group is **`0x0800`**, tested at `0028E54E`.
>
> It was missed because **it is the one group reached by `jmp` rather than `call`**. It sits at the
> very end of the function and tail-jumps to `0028C870` after loading `[0209BE80] + 0x7EA0`:
>
> ```text
> 0028E54E  test dword ptr [01E0C464], 0x800
> 0028E558  je   0028E56F                      ; skip the group
> 0028E55A  lea  rcx, [rbx + 0x7EA0]           ; rbx = [0209BE80]
> 0028E56A  jmp  0028C870                      ; the group's update
> ```
>
> **A census that looks for `call` after a `test` finds fourteen and reports fifteen.** This is the
> mission prompt's four-instrument rule failing inside this database's own pages: `E8 call` alone
> was the instrument, and the one `E9 jmp` group fell out of the table while the count above it
> stayed right. The masks are now enumerated by resolving every RIP-relative operand with a tool,
> not by reading the listing.

**Six of the fifteen masks' groups are `UI`-owned** (counting by mask; the two `0x0002` groups share a row above), which is the strongest signal here about what this
fan-out is for. It is not the whole engine tick — the actor, battle and script systems are not in
this list.

**The pump's wider neighbourhood is what a tick dispatcher should look like.** Its parents and
the groups themselves reach the layers the word selects between: **Input** on 14 edges
(`0017D4C0` → `00198750`; `0022A580` → `00360080`/`0035E9B0`; `0022A770` → `0036FDxx`…),
**resource** loading on 6 (`0017D4C0` → `001DB1E0`/`001A11B0`; `0022A770` → `003245xx`;
`001D1660` → `002EEEE0`), **audio** on 3 (`001D1660` → `002DEBA0`/`001DBB00`; `0022A770` →
`0036F460`), plus single edges into **combat-formula** (`0030C300` → `00320AB0`), **party**
(`0022A770` → `00358BB0`), **platform** (`0022A770` → `00316930`) and **RNG** (`0022B7E0` →
`00379CD0`). A word that chooses which subsystems tick necessarily has edges into them — these
rows are the thesis, not findings against it.

## 4. Bit `0x0004` walks a list, and its per-node update is the largest function in the database that nothing had ever cited

`0028C4C0` (42 B) is a list walk and nothing else:

```c
void ForEachNode(Node *n)            /* 0028C4C0 */
{
    while (n) {
        FUN_0028BB50(n);             /* the per-node update */
        n = n->next_D70;
    }
}
```

**The link is at `+0xD70`, so a node is at least `0xD78` bytes.** A null head is handled — the
function's first instruction is `test rcx, rcx`.

### `0028BB50` — 2,387 bytes, one caller, and it is angle arithmetic

Four instruments, controls positive for each: **`E8` = 1** (`0028C4D3`, the walk above), **`E9` =
0**, **code memory-operand = 0**. One caller, no address-taken reference.

**It was the largest function in this database that no document had ever cited** — the head of
`DT-1`'s list of 112.

**The constants say what the arithmetic is**, every one resolved with a tool:

```
008C5F68 = 0.017453292      pi / 180        degrees -> radians
00915FD4 = 0.00017453294    pi / 180000     thousandths of a degree -> radians
008C5F70 = 1.5707964        +pi/2
00915FE4 = -1.5707964       -pi/2
01CEBC50 = 3.1415927        +pi        00915620 = -pi
01CEBC78 = 6.2831855        2pi        00915624 = -2pi
00915FD8 = 0.22222222       2/9
01DFE0B8 = 1.0    01DFE0BC = 1.0       the FrameLimit time-base pair
```

and `00861F02` is **`atan2f`**, called twice.

> **So this is a per-frame angular update, scaled by the frame-rate time base**, on a list of large
> nodes. `01DFE0B8` is the same `FrameLimit` scale the
> [game settings config](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)
> documents — `1.0f` at 30 fps, `2.0f` at 60 — so **whatever this drives moves at the same rate at
> either frame-rate setting.**

**Two units appear, and they are a thousand apart.** `pi/180` and `pi/180000` both convert to
radians; the second takes thousandths of a degree. **Which field uses which is not established** *(answered: see section 7, UQ-27 ANSWERED 2026-09-17 (FABLE): no field is in thousandths of a degree; 2026-10-02, OPUS)*.

### The node's own shape, as far as the arithmetic shows

```
node +0x0D50   a mode: == 1 selects sub-block 0x4E0, otherwise 0x3C0
node +0x0D4C   flags; bit 0x40 tested at 0028BC00
node +0x0D40   f32
node +0x0D70   -> the next node
                 ...so a node is at least 0xD78 bytes

sub-block base = node + (mode == 1 ? 0x4E0 : 0x3C0),  and 0xAB0 is loaded as a third offset
```

The busiest displacements are `+0x0D34` (14 sites), `+0x0D4C` (10), `+0x0D54` (8), `+0x0D28` (8).

## 5. What this is not

**It is not `Phyre::PCameraPerspective`.** That singleton is recovered at `01F81218` with object
size **`0xBB8`** (`BE-6`), and this node is **at least `0xD78`** — too large to be one. The angle
maths invites the guess and the size refuses it.

**No name is proposed for the node type.** *(answered: see section 7, UQ-25 ANSWERED 2026-09-17 (FABLE): the target-line object; 2026-10-02, OPUS)* Degrees, `atan2f`, a UI-gated list and a frame-rate
scale are consistent with a minimap, a compass, a targeting reticle or a 3D-positioned UI element,
and **consistent-with is not evidence**. `DZ-1`.

## 6. Modding notes

- **`01E0C464` is a single switch board.** Clearing a bit stops a whole group for as long as it is
  clear — there is no partial or degraded mode in this fan-out.
- **Bit `0x0004` is the one that owns the list walk.** Anything hooking `0028BB50` should expect it
  once per node per frame, not once per frame.
- **The walk has no cycle guard.** `n = n->next_D70` runs until it hits null; a list made circular
  by a mod hangs the frame.

## 7. What is not known

- [x] ~~**UQ-25.** **What the node type is.** **§10: RTTI cannot answer it from this path** — no indirect~~
      call and no `[reg + 0]` load in any of the three functions, so there is no vtable to
      follow. Needs the allocator or a string. `DZ-1`.
      ***ANSWERED 2026-09-17 (FABLE): the node is the target-line object, a `0xD80`-byte plain structure with no vtable, drawn from the image named `targetline_p`.** The allocator was the path, as the box said. The list head is `[0209BE80] + 0x10F00` (`0028E315`..`0028E328`), and the only builder is the group function itself, `002917E0`: when the list is short it takes `0xD80` bytes from the HUD object's allocator `+0x10FC0` through `00273A30(0, allocator, 0xD80)` (`00291981`..`00291997`), zeroes them with `00275550` (`002919B0`, `002919BD`), installs no vtable and calls no constructor, and links the block at the head or after the last `+0xD70` (`00291B17`..`00291B33`); the release is `0028FA50`, a tail-jump to `00273B40` on the same allocator. The block's fields: `+0xD00` the image asset, looked up by name through `0024A5A0(01E0C1E0)` (`002919E7`..`00291A01`), and `01E0C1E0` is entry 0 of the 22-entry image-name block [the typed-list page](../../02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md) cites, the string `targetline_p` (its neighbours are `battle_4_c`, `battle_4_p`, `icons_c`, `partytop_4_c`); the asset's sub-image table is then set up by the format-`0x13` builders `00181250` and `00181000` (`00291A2D`, `00291A5E`). `+0xD2C` the actor id the line points at, taken from `+0x10F6C` of the HUD object, which `00290370(id, 0, 3)` sets from `002BF0E0` (`002BF1D1`..`002BF1D9`) together with `+0x10F70 = 0`, `+0x10F72 = 3` and bit 3 of `+0x10F68`; `+0xD14`/`+0xD18` the angle, `00272F30(id)` resolving the actor through `003588B0` and scaling `002645D0(actor)` by `[00901B34]` (`00291AE2`..`00291AF7`); `+0xD44` ~~a timer bounded by the per-kind constants at `00916028`/`0091602C` with the kind byte from `00916010` (`002918A8`..`002918DD`)~~ the radian field `0028BB50` decays (below): the builder adds `[01DFE0BC]` × `[00916028]` (π/10) and caps it at `[01DFE0BC]` × `[0091602C]` (2π/15) *(corrected 2026-10-02, OPUS: `002917E0+0xC8`–`+0xFD`; the two constants are single floats, not per-kind, and the kind byte from `00916010` goes to `+0xD7C`, `002917E0+0xB3`–`+0xBB`)*; `+0xD48` a variant word, `0x6040003` or `0x6040004` (`00291AA3`, `00291AAF`); `+0xD4C` flag bits `0x2`/`0x40`; `+0xD54` a state word (1 live, 5 marked for the reaper `0028D1C0`, which unlinks and releases it); `+0xD68` prev and `+0xD70` next; `+0xC70`..`+0xCAF` four vectors copied by `00202C90`; `+0xBB0` a sub-object handed to `00271650`. So the per-node update `0028BB50`'s angle arithmetic is the line's orientation toward its actor, and its `atan2f` is the bearing. Static, builder, reaper and release read; the image name read from the block.*
- [x] ~~**UQ-26.** **What bit `0x0010` was.** Absent from the fan-out, and no substitute was found.~~
      **NO ADMISSIBLE SOURCE — reviewed and signed 2026-09-16 (OPUS, reviewer; FABLE, author),
      under EVIDENCE-STANDARD addendum 2026-09-15bk.**
      *The mechanism is established at tier 1 and it is the mechanism that makes the question
      unanswerable rather than a gap in it: `01E0C464` has **16 references image-wide, every one a
      `test`, all inside `0028E290`**, carrying exactly fifteen masks — `0x1 0x2 0x4 0x8 0x20 0x40
      0x80 0x100 0x200 0x400 0x800 0x1000 0x2000 0x4000 0x8000` — and **`0x10` is not among them**.
      `01E0C460` reads `16 00 00 00 ff ff ff ff`, so the word ships `0xFFFFFFFF` with bit `0x10`
      **set and never read**. The source that would answer it is a removed feature's purpose, which
      no executable carries, and **it is not a live-run question** — addendum 15bk's kind (c) —
      because a run cannot reveal a bit no instruction reads. The negative was widened past this
      function to the whole image and to the two addressing forms that hide references here: the
      image-base table returns **zero**, and no `lea`'d constant lands on the word or within `0x40`
      bytes of it. OPUS **re-derived requirements 1 and 3** rather than accepting them; requirement 4
      is that signature, the author being FABLE.*
      *Recorded because rejecting it is the point: the duplicate `0x0002` test at `0028E3AE` sits
      immediately after the `0x20` test, exactly where `0x0010`'s group would fall **if** the tests
      ran in bit order. They do not — `0x1000` is tested before `0x40` — so the adjacency proves
      nothing, and this page's own warning that "consistent-with is not evidence" applies to it.*
- [x] ~~**What sets and clears `01E0C464`.** **§10 measured it: 16 references image-wide, all
      reads.** No instruction stores to it by name; the only plausible route is the pointer
      registry `001AF470` builds, whose owner is unidentified.~~ **DZ-2 ANSWERED 2026-09-11:**
      nothing in the executable — the registry route is closed too, since `001AF470` takes the
      addresses of `01E0C444` … `01E0C460` and stops before this word; it ships as `FF FF FF FF`
      and stays so (§10).
- [x] ~~**UQ-27.** **Which of the two degree units each field uses**, `pi/180` or `pi/180000`.~~
      **ANSWERED 2026-09-17 (FABLE): no field is in thousandths of a degree - both constants act on the SAME radian field, `node+0xD44`, as a floor and a minimum step.** `0028BC4E`–`0028BCAF`: `floor = [01DFE0BC] × pi/180` (one degree, scaled by the frame-rate time base); if `+0xD44` is above it, the field is decremented by `max(pi/180000, +0xD44 / (11 × [01DFE0B8]))` - an eleventh of itself per frame, never less than a thousandth of a degree - and then clamped back up to the floor if the step overshot. So `pi/180` is where a 1° floor is stated in degrees, `pi/180000` is where a 0.001° minimum step is, and the field they act on is radian-valued (it is compared with one degree in radians). The constants beside them are the decay's shape: `00915B9C = 11.0` (the divisor), and on the sibling block for `+0xD34`, `008C5F6C = 0.1` × the time base as its floor and `00915FDC = 1.25`. `pi/180` is also used by `0033CEF0`, `00538B80`, `0085EA40` on other objects; `pi/180000` has this ONE reference in the image (`ripscan`, control: the pi/180 sites), so the thousandth-of-a-degree unit exists nowhere but this clamp.
- [x] ~~**UQ-28.** **The other fourteen groups.** Named and sized here, unread.~~
      ***ANSWERED 2026-09-17 (FABLE): the fourteen other groups are read, ten to their mechanism and four to their call shape.** `0x0001` `00289970(obj)`: `0028A550`, then `0028A350`, the per-tick body on the object's `+0x428` record (`002718E0`, `00275490`, the actor getter `003588B0`), then the tail `0028A620`: three passes over one actor-backed record. `0x0002`: `001EDE80` returns 1 under the ~~pause predicate~~ 60 fps half-rate test (`[01F82E38]` zero or `[01DFE0C0]` set) and otherwise the sum of the two ~~cutscene-name-slot counters~~ frame counters `0022A080()` and `0022A030()` *(corrected 2026-10-02, OPUS: `01F82E38` is set to 1 with `01DFE0B4 = 2` by the 60 fps arm, `001EDDC0+0x28`/`+0x32`; `0022A080` and `0022A030` read `02064AD8` and `02064AA8`, and `02064AD8` toggles every frame at `0022A580+0xC6`–`+0xCF`)*; its five companions are thin: `003F8B40` (gate `+0x26` bit 0, `00271960`, `00272710`), `00291B90` (`[0209BE80] + 0x850` compared with 5, then the HUD allocator's release `00273B40`), `003F6100` (`003F5CB0`), `003F24D0` (`0028FA50`) and `003F24A0` (`003F1E90`). `0x0004`: the target-line list (UQ-25). `0x0008` `003F6BB0(obj)` with `003F7050`: a per-frame update stepping by `[01DFE0BC]` under flag byte `+0x2EC` and the state word `+0x2F0` (compared with 3), through `002713E0` four times, `00203080`, `00270A10`, `002754E0`, `003F7BC0`, `003F7760` and `003F7610`, with the float constants at `00D11D34`..`00D11D40` and `008F8D80`; call shape only. `0x0020` `003F9F40(obj)`: on flag byte `+0x249C` bits 2, 4 and 0, after the free check `00273A20`, builds widgets (`00245000` then `00246AC0`) with the procedures `003FACF0` and `003FC3F0` and calls `003F9E50`; then on `+0xC4` bit 2 the bounded dword-table getter `002DD7E0` and `003FAAF0`, on bit 1 `00296F50`, and `0029F6E0`: a widget spawner keyed on request flags. `0x0040` `003F80D0(obj)`: `003F7E80` when `+0x984` bit 0 is set, nothing otherwise. `0x0080` `00296860(obj, n)`: for `n` entries of `0x110` bytes from `+0x104`, when the entry's flag at `-0x14` is set and `00273A20` allows, builds a `0xF0`-byte widget (`00245000`, `00246AC0`) with the level-up blink procedure `00299D10` and cycles the entry's three-slot ring (`002968AC`..`00296909`): the level-up blink spawner. `0x0100` `003F8EC0(obj)`: `0035BAD0`, `002713E0`, on `+0x52C6` bit 1 the vec4 copy `00202C90` and `00275490`, then `003F9720` twice under `[rax + 0x23C]` bit 1; call shape. `0x0200` `003F31B0(list, fn)`: walks the doubly linked list through `+0x70`/`+0x78`, calls `003F30D0` on each node and, for nodes with `+0x50` bit 1, unlinks them and calls `fn(node)` (`003F31E0`..`003F3235`): a list reaper. `0x0400` `003FA790(obj)`: two passes over the list at `+0x2490` linked by `+0x278`, first zeroing `+0x272` and calling `003FA4E0(obj)` for entries whose `+0x260` is 0, then `003FC510(entry)` and, when `001EDE80` is non-zero, `003FC170(entry + 0x20, entry)`. `0x0800` `0028C870(obj)` on `[0209BE80] + 0x7EA0`, tail-jumped: steps the word `+0x76` by `0x20 / [01DFE0B4]` toward `0x80` or toward 0 as `+0x74` bit 0 says (a fade level), advances the angle `+0x70` by `dt x [008F8180] x [01CEBC50] / [008F3138]` wrapped into one turn, then ~~`0028CD80` and~~ `0028CD80` on the object itself and `0028CE90` on the two `0x20`-byte lanes at `+0x30` and `+0x50` *(corrected 2026-10-02, OPUS: `0028C870+0x97` calls `0028CD80` with `rcx` unchanged, then `+0xA0`–`+0xB8` loops `0028CE90` over `obj + 0x30 + i × 0x20`, `i` below 2)*: a two-lane rotating fade. `0x1000` `00273900` to `0030C300`: scans party slots 0..8 through `00320AB0(slot, 1)`, collects into `022C1740` the members whose status words `+0x64` or `+0x3C` ~~carry `0x80000003` (KO, Stone, X-Zone) or whose field record bit 15 (`00377C20`) is set~~ carry none of `0x80000003` (KO, Stone, X-Zone), and those that do only when the field record bit 15 (`00377C20`) is set *(corrected 2026-10-02, OPUS: `0030C300+0x44`–`+0x58`)*, and returns 1 when any collected member has bit 30 set: a party incapacitation scan. `0x2000` `00290CF0`: `00254500` (the UI-request inhibit mask from the aggregate policy) and `00254550`, then under `[02092730]` `002DDD40`, `00276640`, `00273A20` and `00276650`, the constructor of the `0x61F0`-byte object whose handler is `00279E20`; call shape. `0x4000` `00290EB0(hud)`: when `+0x10F90` is not `-1` and `00273A20` allows, builds a widget with procedure `00290FF0` (`00245000`), `003F8010`, `003F8030`, the table `00915FE8`, `00247570` and `00247930` (attach under the shared root), then `00246AC0`: the spawner for the `+0x10F90` request. `0x8000` `002C6180(obj)`: flags at `+0x1D7A` and a frame-scaled timer at `+0x1D78` (two divisions by `[01DFE0B4]`) driving `002C8D60`, `002C6BE0`, `002C6B50`, `0028F5B0` and `002C8DF0` under `[02092730]`; call shape. Static, every body read; the four call-shape groups name their callees but not what those compute.*
- [x] ~~**UQ-29.** **The other 111 uncited residuals.** `DT-1`.~~
      **ANSWERED BY CITATION 2026-09-17 (FABLE): the population this row names no longer exists in that form.** The *111* is `DT-1`'s 112 less this page's one, and `DT-1` was re-measured on 2026-09-16 (`residual_crossref.py`, as its own page instructs): of the 139 residual functions **131 are cited by some page and 8 by none** - `005DC8D0`, `0032D820`, `001B0CE0`, `00407D10`, `005713C0`, `00287400`, `005C6A90`, `005C6770`. The 104 that left did so by pages being written, not by this page's groups being read; *cited* is not *understood*, and the 75 cited at their entry alone are `DT-1`'s restated residue, not this row's. Nothing here is this page's to do.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| one enable word, fifteen masks | 16 ~~`test byte [01E0C464], imm`~~ `test [01E0C464], imm` sites, 8 `test byte` for the masks below `0x100` and 8 `test dword` for `0x100`–`0x8000` *(corrected 2026-10-02, OPUS: `0028E290+0x4` to `+0x1C0` byte, `+0x16F` to `+0x2BE` dword)*, in `0028E290`, all the same global | 1 | PROVEN |
| bit `0x0010` is unused | no `test` with that mask anywhere in the function | 1 | PROVEN |
| `0028C4C0` is a list walk linked at `+0xD70` | its 42 bytes in full | 1 | PROVEN |
| `0028BB50` has exactly one caller | **four instruments**, `E8` 1 / `E9` 0 / operand 0, each with a positive control | 1 | PROVEN |
| the constants and `atan2f` | every RIP target resolved with a tool | 1 | PROVEN |
| the node is not `PCameraPerspective` | `0xBB8` from `BE-6` against a minimum `0xD78` here | 1 | VERY HIGH |
| what the node type is | ~~**not established**~~ **the target-line object: `0xD80` bytes, no vtable, image `targetline_p`** (UQ-25, 2026-09-17): allocation `00291981`..`00291997`, asset `002919E7`..`00291A01`, name read at `01E0C1E0` | 1 | PROVEN |
| any runtime observation | **none exists** | — | UNKNOWN |

## 9. Related

- [What happens between two frames](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md) — the engine-level frame
- [The game settings config](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md) — the `FrameLimit` time base at `01DFE0B8`
- [The unresolved 158](../../99-Unresolved-Residual/the-unresolved-158.md) — `DT-1` and the 112

## 10. Reopened 2026-09-08 — nothing writes the enable word, and the node is not dispatched through

§7 left two unknowns with no method attached. Both now have one, and neither is answered *(answered: see section 7, UQ-25 / DZ-1 ANSWERED 2026-09-17 (FABLE) and DZ-2 ANSWERED 2026-09-11; 2026-10-02, OPUS)*.

### `DZ-2` — there is no direct writer, and that is a measurement

`01E0C464` has **16 references in the entire image. All 16 are in `0028E290`, and all 16 are
`test`.** Operand instrument over every function body, control `02ADD0A8` positive at 3.

> **No instruction anywhere stores to it.** A word that fifteen update groups depend on, and
> the code that changes it is not addressing it by name.

**The route it must take is visible one address away.** `01E0C464` sits in a cluster with
`01E0C460`, `01E0C470`, `01E0C478` and `01E0C480`, and **`001AF470` (3,179 B) takes the
address of two of them** and stores each into a consecutive 8-byte slot of an object:

```asm
001AF5C0  lea rax, [01E0C460] ; mov [rcx + 0x3BC8], rax
001AFDE6  lea rax, [01E0C470] ; mov [rcx + 0x4048], rax
```

That function is a long run of exactly this shape — **a registry of pointers to globals**. **A
write through such a table is invisible to every address-keyed scan**, which is a sufficient
explanation for 16 reads and no writes, and it names where to look next.

> **What is NOT claimed:** that `001AF470` is the developer console's binding. This database
> documents a [282-command parameter console](../Developer-Tuning-Console/the-282-command-parameter-console.md)
> whose dispatcher is `001D1660` and whose block is a render-tuning object — **a different
> object from the one `001AF470` fills**, and no evidence here connects them. The registry is
> named; its owner is not. `DZ-2`.

**Closed 2026-09-11 (OPUS-CONTRA-GATEWORD, confirmed independently).** The registry route does not
reach the word: `001AF470` takes the addresses of the eight tunables before it — `01E0C444`,
`01E0C448` … `01E0C460`, the last at `001AF5C0` into `[rcx + 0x3BC8]` — and **not `01E0C464`**; the
next address it takes is `01E0C470`. Beyond the rip-relative census (sixteen reads, all in
`0028E290`), no 32-bit absolute encoding and no 64-bit pointer to `01E0C464` exists anywhere in
`.text`, `.rdata` or `.data`, so no register can come to hold its address by any route the image
records. And the word's initial bytes are `FF FF FF FF`, between the tunables `0x17` and `0x16`
and a run of zeros. **So: every bit is set at build time, and nothing in the executable turns one
off** — the switch is real and compiled always-on. Two routes remain outside this measurement, and
neither is the game: a write from outside the executable, and a consumer of the registered pointer
to `01E0C460` that writes four bytes past it — the registry's consumers are unread (its owner is the
object `001B1580` builds, from `0017D4C0`, whose three constructors it calls in turn).

### `DZ-1` — RTTI cannot name the node from this path

**Neither `0028BB50`, `0028C4C0` nor `0028E290` contains a single indirect call or a
`[reg + 0]` qword load.** The node is never dispatched through in the read path, so there is no
vtable to follow and **RTTI is not available from here**.

> **That is a bounded negative, not a conclusion.** It does not show the type is
> non-polymorphic — only that these three functions never use it that way. It is the same shape
> as `BE-6`'s *“eight have no vtable at all”*, and it means naming the node needs **its
> allocator or a string**, not the call graph. `DZ-1`.

## 11. Falsification pass 1 — 2026-09-13 (OPUS)

The page carried two corrections of mine from 2026-09-11 (`OPUS-CONTRA-GATEWORD`,
`OPUS-FRAMEGATE-16TH`) and a §10 reopening, but **no falsification pass** — `audit_coverage` was
right to exclude it. This is that pass, and **everything it could reach reproduces.**

| claim | measured |
|---|---|
| the word ships as `FF FF FF FF` | `01E0C464` = **`ffffffff`** in `.data` |
| "sixteen `test` sites" | **16** |
| "never a different global" | all 16 resolve to `01E0C464`, **no other address** |
| "fifteen distinct masks" | **15** |
| "`0x0002` used twice" | **`0028E2B7`** and **`0028E3AE`** — the only repeated mask |
| §2's width split, 8 byte-sites and 8 dword-sites | `0x01`–`0x80` as `test byte ptr` × **8**; `0x100`–`0x8000` as `test dword ptr` × **8** |
| "bit 4 (`0x0010`) is absent, and it is the only absentee" | `0x10` appears **nowhere**; the 15 masks are every other bit of the low 16 |
| the whole fan-out is one function | all 16 sites are in **`0028E290`**, and in no other function in the image |

### The "nothing writes it" claim, and why this scan can carry it

§1 says *"nothing in the executable stores to it, takes its address or encodes it anywhere."* A
whole-image sweep of every function body for a rip-relative operand resolving to `01E0C464` returns
**sixteen references and every single one is a `test`** — no `mov`, no `or`, no `and`, no `lea`.

> **That is a negative with its own control built in.** The same instrument, on the same address,
> found sixteen things; it is not silent. A scan that returned nothing at all would prove nothing
> either way — this one distinguishes *reads exist, writes do not*, which is exactly the claim.

### Nothing to add, and that is the finding

Two things this pass was ready to offer as new were **already on the page**, found by searching
before claiming, per [`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s 2026-09-13
amendment:

- **bit 4's absence** — §2 already states it, files it as an open question, and lists it in §8's
  evidence table;
- **the mixed access width** — §2's own table already splits the sixteen sites 8 byte / 8 dword.

Recorded because the amendment exists precisely to make that check a step, and twice today it was
not one.

**Not claimed:** the sixteen gated callees in §3, their owners, §4's list walk and the largest-uncited
function it names were **not** re-read — this pass tested the gate, not what it gates. §10's
reopening stands as written. Nothing was executed or observed live.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `0028A350` | 499 | per-tick body on `[rcx+0x428]` record: `[rbx+0xC..0x18]` fields, `002718E0`, `00275490`, `003588B0` getter; caller `00289970` |

*(Pass 22 live-graph completion, 2026-09-15: the gate-frame's callees keep spreading —
`00320AB0` is called by `Items_Equipment_Shops_License` bodies `0030FAA0`/`0030FD10`/`0030A4E0`
and two more (5), by `Rewards_Progression_Economy` `002F8BB0`/`00312280`, with `00379CD0`
called by `002F9B20` (4), and calls `Gameplay` `0031B9F0` (1). Ten more edges of the same
thesis: the frame's work touches the item, economy and gameplay layers it ticks.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** Cited functions are called by `BattleStats_ChangeStatusAndProcessSideEffects`, `BattleUnit_RunPeriodicCombatMaintenance` and `BattleFormula_AdvanceStatusTimersAndBuildResult`.

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**CombatAI — SERVICE, and it is this page's own subject being asked.** Three CombatAI bodies call
`FieldData_GetActiveFieldRecordBit15` (`00377C20`, 78 B) at **six** sites between them:
`AiOrder_EvaluateAndResolveActionTarget` (`003014C0`) at `00301538`;
`AiOrder_EvaluateTargetSelector` (`00301AD0`) at `00301D4E` and `00302738`;
`BattleUnit_SelectAndCommitNextAction` (`00305AB0`) at `00305B3C`, `00305B5D` and `00305BB2`.
**~~That getter is the one word this page is named for~~**~~, so the crossing is the AI layer reading~~
~~the same gate as the fifteen subsystems~~ That getter is not this page's word *(corrected 2026-10-02, OPUS: `00377C20` returns bit 15 of a record in the `[02ADD100]` table, `00377C20+0x9`–`+0x35`; `01E0C464` is read only by the sixteen tests in `0028E290`)*, so the AI layer reads field data here rather than owning anything here. Six sites in three
bodies is also the answer to how hard the gate is leaned on from that side.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — CLIENT.** `BattleUnit_TryTriggerNearbyAuthoredFieldAction`, owned by that layer, calls `00379CD0` on this page. That caller is the nearby-trigger attempt, a `0x98`-byte frame with a stack cookie carrying three arguments through to the test; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT (FABLE, Claude Opus 5.5, 2026-09-25).** Gate group 7's worker `0030C300` calls `BattleStats_GetByMappedBattleSlot` `00320AB0` once per battle slot 0-8 and reads each record's status words `+0x3C`/`+0x64` for the terminal mask and Libra (last section). The crossing is that read: the gate consumes combat-formula state to set one bit of its own flag word, and writes nothing in that layer.

**UI — PROVIDER (FABLE, Claude Opus 5.5, 2026-09-25).** The target-information widget builder `002BFD20` reads the Libra bit this page's group 7 maintains, through the getter `00290100`, and writes its own widget word `+0x282`. The gate provides state; the widget owns what it shows.

**Presentation — MECHANICAL (FABLE, Claude Opus 5.5, 2026-09-25).** The group bodies this page cites (`002917E0`, `00291010`, `00291320` and their callees) reach shared Presentation helpers, among them the image-slot format builders `00181000`/`00181250` (format `0x13`, [the typed-list page](../../02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md)), to prepare the HUD pieces they update. That is shared-helper fan-in; no Presentation state is owned here.

**ActorEntity — CLIENT (FABLE, Claude Opus 5.5, 2026-09-25).** Group callees such as `002713E0`, `002718E0` and `00272F30` resolve packed actor ids through `ActorHandle_ResolveRegistryEntryByPackedId` `003588B0` before reading the actor they decorate. The gate consults the actor registry and never writes it.
- **InputGameplay — MECHANICAL (1 edge).** 1 InputGameplay-side call into a shared helper the page cites: `00313A00` calls `FieldData_GetActiveFieldRecordBit15` (00377C20), the active-field bit-15 accessor that 65 bodies across the image call; the helper's population, not an InputGameplay relationship of this page (re-read 2026-09-30, SWE2-CONTRACT).
- **Movement — CLIENT and SERVICE (34 edges).** 31 inbound (Movement bodies `0026C3E0`, `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00), `BattleLocomotion_FinalizeHeadingState` (0033BFB0) call page-cited `00203080`, `FieldData_GetActiveFieldRecordBit15` (00377C20), `001EDE80`); 3 outbound (page-cited `002718E0`, `BattleUnit_ProcessDefeatRewardsAndLoot` (00312280) call Movement bodies `00265470`, `00263940`, `00319490`). Substantive edges include `001EDE80` is called by `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00); `002718E0` calls `00265470`; `002718E0` calls `00263940`; `PartyFocus_CommitPendingPackedActorHandle_Thunk` (00358BB0) is called by `0026C3E0`; the remaining edges run through shared helpers the page cites.
- **Save_Load_Settings — CLIENT and SERVICE (4 edges).** 1 inbound (Save_Load_Settings bodies `00581930` call page-cited `002DD7E0`); 3 outbound (page-cited `0017D4C0` call Save_Load_Settings bodies `SaveloadManager_RefreshDisableAutosaveList` (001C1710), `SaveloadManager_GetSingleton` (001C18E0), `SaveloadManager_EnsureSingleton` (001C18A0)). Substantive edges include `0017D4C0` calls `SaveloadManager_RefreshDisableAutosaveList` (001C1710); `0017D4C0` calls `SaveloadManager_GetSingleton` (001C18E0); `0017D4C0` calls `SaveloadManager_EnsureSingleton` (001C18A0); `002DD7E0` is called by `00581930`.
- **Script_VM_Native_Bridge — CLIENT and SERVICE (15 edges).** 14 inbound (Script_VM_Native_Bridge bodies `003497B0`, `0050FED0`, `0050FE20` call page-cited `BattleStats_GetByMappedBattleSlot` (00320AB0), `FieldData_GetActiveFieldRecordBit15` (00377C20), `RNG_MT19937_NextU32_Thunk` (00379CD0)); 1 outbound (page-cited `003419D0` call Script_VM_Native_Bridge bodies `VMValueStack_PopInt32CoerceFloat32` (00267E10)). Substantive edges include `Equipment_UnequipEncodedItemFromActiveRoster` (0030FD10) is called by `003497B0`; `FieldData_GetActiveFieldRecordBit15` (00377C20) is called by `00352FA0`; `FieldData_GetActiveFieldRecordBit15` (00377C20) is called by `00355680`; `FieldData_GetActiveFieldRecordBit15` (00377C20) is called by `00344740`; the remaining edges run through shared helpers the page cites.
- **WorldAreaField — CLIENT and SERVICE (11 edges).** 5 inbound (WorldAreaField bodies `0057FB00`, `World_UpdateSimulationTick` (00314020), `BattleSystem_InitializeAreaState` (002342F0) call page-cited `RNG_MT19937_NextU32_Thunk` (00379CD0), `0029FB50`, `002DEBA0`); 6 outbound (page-cited `0022A770`, `0030C300`, `Equipment_UnequipEncodedItemFromActiveRoster` (0030FD10) call WorldAreaField bodies `FieldData_GetActiveFieldRecordBit15` (00377C20), `WorldTransition_GetActiveOrPendingFieldId` (003148F0), `World_UpdateSimulationTick` (00314020)). Substantive edges include `0022A770` calls `World_UpdateSimulationTick` (00314020); `002DEBA0` is called by `World_UpdateSimulationTick` (00314020); `FieldData_GetActiveFieldRecordBit15` (00377C20) is called by `BattleSystem_InitializeAreaState` (002342F0); the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT and SERVICE (15 edges).** 14 inbound (Script_VM_Native_Bridge bodies `003497B0`, `0050FED0`, `0050FE20` call page-cited `BattleStats_GetByMappedBattleSlot` (00320AB0), `FieldData_GetActiveFieldRecordBit15` (00377C20), `RNG_MT19937_NextU32_Thunk` (00379CD0)); 1 outbound (page-cited `003419D0` call Script_VM_Native_Bridge bodies `VMValueStack_PopInt32CoerceFloat32` (00267E10)). Substantive edges include `Equipment_UnequipEncodedItemFromActiveRoster` (0030FD10) is called by `003497B0`; `FieldData_GetActiveFieldRecordBit15` (00377C20) is called by `00352FA0`; `FieldData_GetActiveFieldRecordBit15` (00377C20) is called by `00355680`; `FieldData_GetActiveFieldRecordBit15` (00377C20) is called by `00344740`; the remaining edges run through shared helpers the page cites.
## The `0028C4B0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0028C4B0` (5 B) — `jmp 0028D1C0` thunk.

| member | role | interior |
| --- | --- | --- |
| `0028D1C0` (154 B) | null-gated per-frame body (`0028D1C9`/`0028D1CC`) | [`0028D1C9`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The `obj` each group handler takes is a named sub-object of the singleton (2026-09-18, OPUS)

§3 reads the group handlers and records the offsets they touch — `003F8EC0` on `+0x52C6`,
`003F80D0` on `+0x984`, `003F9F40` on `+0x249C`, `003FA790` on the list at `+0x2490`, `00296860`
on the `0x110`-byte entries from `+0x104`. It calls the argument `obj` throughout, because from
inside those bodies that is all it is.

The type store has seven `ManagerSub0209BE80_*` types, EMBED children of the `0209BE80` singleton,
together **the largest unknown mass in the database** at roughly 20 kB and about 99 % unknown.
Nobody had connected the two. **They are the same objects**, and this page's own offsets are the
evidence, because every one of them falls inside the child its handler is passed.

Measured by tainting the singleton pointer through the **136 bodies that load the slot `0209BE80`**
(it has no one-instruction accessor — the shape that hid 160 bytes of `BootSingleton01F7F598`
does not apply here) and recording each `lea rcx,[singleton+d]` that survives to a call:

| group | handler | receives | child size | offset §3 records | inside? |
|---|---|---|---|---|---|
| `0x0100` | `003F8EC0` | `_00A0` (`+0xA0`) | `0x52E0` | `+0x52C6` | yes, 26 B from the end |
| `0x0020` | `003F9F40` | `_57E0` | `0x26C0` | `+0x249C` | yes |
| `0x0400` | `003FA790` | `_57E0` | `0x26C0` | `+0x2490` | yes |
| — | `003FA4E0` | `_57E0` | `0x26C0` | `+0x2490` (§3, via `003FA790`) | yes |
| `0x0080` | `00296860` | `_7FB0` | `0xFF0` | `+0x104` | yes |
| `0x0040` | `003F80D0` | `_A0D0` | `0x990` | `+0x984` | yes, 12 B from the end |
| `0x0800` | `0028C870` | `_7EA0` | `0x110` | already stated in §3 | yes |

**Two of these were already the controls in `arg_extent_scan.py`** — `003F80D0` → `+0x984` and
`003F8EC0` → `+0x52C6` — recorded there as arbitrary known-good extents long before anyone asked
what their argument was. They land 12 and 26 bytes short of their child's declared end. Neither
number was derived from the other, so the child extents in the type store and the reach of the
handlers in this page **corroborate each other independently**, and that is the part worth having:
the sizes were declared from the layout, and the code agrees with them.

Re-measured for the `_57E0` owners: `003FA790` reaches `+0x2490` and `003F9F40` `+0x24A2`, against
a declared `0x26C0`. Both fit.

**`0028C870` does not appear in the handoff scan and should not** — §3 records that it is reached
by a **tail `jmp`**, not a `call` (`0028E55A lea rcx,[rbx + 0x7EA0]`), and the scan only inspects
argument registers at `call`. The page had already read it; the absence is the scan behaving
correctly, not a miss.

**What this does NOT do is explain a single one of those 20 kB.** It names the owner of four
children and confirms a fifth, which converts *"a 9,920-byte blob at 99.4 % unknown"* into *"the
argument of `003F9F40` / `003FA790` / `003FA4E0`, whose bodies §3 has already read to call shape"*.
That is a reading order, not a layout. ~~`_5380` (`0x460`) and `_8FA0` (`0x1130`) are handed to
nothing at all and still have no owner.~~ *Refuted 2026-09-25 (FABLE, Claude Opus 5.5): both are handed over - `add rcx, 0x5380` / `add rcx, 0x8fa0`; see the last section.*

### Interior citation — frontier hub 0029FB50 (2026-09-18, SWE2-EC7)

**0029FB50** (126 B, 4 A-measured callers) — the fixed-width decimal digit writer ~~the `0x0020`-group widget spawner reaches through `0028BB50`~~ *(corrected 2026-10-02, OPUS: `0028BB50` is not in the `0x0020` group: its only caller is `0028C4C0+0x13`, run by `0028E290+0x98` under mask `0x04`, and neither it nor its callee `0028CF80` calls `0029FB50` directly)*. Extracts a signed 6-bit digit (`[rcx+8] << 0x10 >> 0x16` — the signed shift pair pulls a packed nibble-field), `0020E600` resolves the slot, `002D8B00` emits the two-word record, then `mulss xmm0, [rdi+0x28]` scales and the word at `+0xA` plus flag byte `+0x2D` (`& 0xD7 | 0x10`) update the entry. This is the leaf the per-entry refresh calls once per digit. In-scope: shift-pair extract [`0029FB70`](../../_index/ADDRESS-INDEX.md); `002D8B00` emit [`0029FB8F`](../../_index/ADDRESS-INDEX.md) — 4 callers, all A.

## The tail of the HUD object is a row of mailboxes (2026-09-19, FABLE, on `OPUS-REQ-FABLE-REPRESENTATION-UNDECIDABLE-ROWS`)

The type store has nine fields between `+0x10F60` and `+0x10FA8` whose representation no instruction reveals: every
access is a plain move, or a compare with zero. **That is what a mailbox looks like.** Each is parked by one system and
collected whole by another; nothing in between computes with it. Purpose, found by following each field to its
setter's caller and to its one consumer (an image-wide sweep of the displacements; static):

| field | what it is | how it is known |
|---|---|---|
| `+0x10F6C` dword | **the actor a target line points at** - a packed actor handle | `00290370` (89 B, read whole) stores it with `+0x10F70`, `+0x10F72` and flag bit 3; on the next pump the gate hands the three to the target-line builder `002917E0`, which only ever *compares* it with a node's `+0xD2C` (section 7, `UQ-25`) |
| `+0x10F70` word | the builder's second argument - **always zero** | the same setter stores a constant 0; its own second argument is a boolean that takes a different path when non-zero |
| `+0x10F72` word | **the line kind** - an index into the signed-byte table at `00916010` | the builder indexes that table with it; the one caller passes 1 or 3 |
| `+0x10FA2` byte, `+0x10FA6` word, `+0x10FA8` dword | **the arguments of the world-map opener** | `0028E790` (161 B, read whole): the mode byte and the word go to the opener - the word is zeroed first unless the mode is 3 - then flag bit 12, then `+0x10FA8` as the dword at `+8` of a sixteen-byte block, then the open call. The dword's setter is called from world-map UI code with a value read out of the menu singleton |
| `+0x10FA0` word | **the intervention menu's tutorial mode** | script verb `0x45C`, which the bundled catalogue names `set_interventionmenu_tutorialmode`: its handler `003419D0` (23 B, read whole) pops one integer and tail-jumps through a thunk to the one-store setter. `0028F970` (112 B, read whole) clears it, together with flag bits 4 and 10, unless flag bit 13 is up. *Nothing in the sweep reads it back; the reader must reach it another way* |
| `+0x10F74` dword | **a handle, zero meaning none** | the teardown tests it, releases it through a one-argument release routine, and zeroes it; no other access in the sweep |
| `+0x10F60` word | a **write-only latch** stored together with flag bit 4 | two setters, `0028E940` and `0028FD50` (46 and 31 B, read whole); the battle-mode consumer `0035D030` (28 B, read whole) passes 1. Never read in the sweep |
| `+0x10F90` dword | reset to -1 wherever the pointer `+0x10F88` is released | three writes of -1, no read |

**For the type store:** the handle and the two ids are opaque 32-bit values (compare-only); the kind and the mode are
small unsigned enumerations; `+0x10F70` and the two write-only words carry no information a reader could depend on.
*Not covered: the three sub-object rows of the same request (`+0x24` of the `+0x7EA0` sub-object, `+0x974` of `+0xA0D0`,
`+0xC8` of `+0x57E0`).*

| body | anchors |
|---|---|
| `0028E790` world-map open from the HUD object (161 B) | `0028E7A3`, `0028E7AF`, `0028E7BA`, `0028E7C8`, `0028E7CF`, `0028E7D6`, `0028E7E2`, `0028E7EE`, `0028E806`, `0028E815`, `0028E81A` |

## All sixteen groups reach singleton state — groups 2 and 7 completed (2026-09-25, FABLE, Claude Opus 5.5)

**Why this was needed.** OPUS's join in
[the L2 verdicts](../../_index/L2-VERDICTS.md) (S-02, "the join is now made", 2026-09-20) pairs
every mask test in `0028E290` with the instruction that writes `rcx` before its call. It accounts
for all sixteen groups as seven named sub-regions, four whole-object calls and three tail pointers.
Groups 2 and 7 it records as **"no receiver"**, because nothing writes `rcx` before their calls.
Both are true of the call and both stop one instruction short. Each group's *first* call is a
query, and the **state it drives comes after it**.

**Group 2 (`0x0002`, the half-rate walker).**
- `001EDE80` takes no argument and is a pure predicate. It returns 1 unless half-rate is on
  (`[01F82E38] != 0` and `[01DFE0C0] == 0`). Under half-rate it returns the sum of the two frame
  counters `[02064AD8]` and `[02064AA8]`.
- When the result is non-zero, the gate calls **`003F8B40(singleton + 0x80)`** (`0028E2C5`–`0028E2D4`;
  the `sub rcx, -0x80` is an add). `003F8B40` walks an **intrusive list of callback nodes** whose head
  is the qword at `+0x80` (next pointer at node `+0x28`). Per node it:
  1. calls the node's callback `+0x38` with `(node, 2, 0)`;
  2. unless node flag `+0x26` bit 0 is set, runs `00272710`, folds its low bit into `+0x26` and
     stores `00271960(node, +0x14)` into `+0x50`;
  3. calls the callback with 4 if bit 0 is now set;
  4. always calls it with 3.
- The store's `clearedBlock0080` (`0x18` bytes, cleared by `004FE3C0`) is this list's owner. Its
  first qword is the head, and nothing here needs more than those three qwords.

**Group 7 (`0x1000`, Libra).**
- `00273900` → `0030C300` also takes no argument. It collects the members of battle slots 0–8
  through `BattleStats_GetByMappedBattleSlot` into a nine-entry array at `022C1740`. A member
  carrying a terminal status (`statusWord1|statusWord2 & 0x80000003`: KO, Stone, X-Zone) is kept
  only when `FieldData_GetActiveFieldRecordBit15` holds.
- It returns 1 if any collected member has **status bit 30**, which
  [the thirty-two statuses](../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md) name as
  **Libra**.
- The gate writes that result into **bit 1 of the singleton's `+0x10F68`** (`0028E41C`–`0028E427`:
  `flags ^= (flags ^ (r << 1)) & 2`).
- The only reader of that bit is the one-line getter `00290100` (`(word >> 1) & 1`). Its only caller
  is `002BFD20`, the target-information widget builder that copies the unit display record into its
  widget at `+0xC0`. On all three call sites (`002BFDC8`, `002BFE4A`, `002BFF38`) a true result makes
  it write **`0x100` to widget `+0x282`**.

**So Libra on any live party member is recomputed once per frame by the update gate, and the target
window reads it from the singleton.** What `+0x282 = 0x100` shows on screen is not read here.

**The binding, now 16 of 16 to state:**
- 8 to a named sub-region: OPUS's seven, plus `+0x80` for group 2;
- 4 to the whole object;
- 3 through a tail pointer;
- group 7 to one bit of the root's flag word.

The groups that act on state **outside** the singleton do so in addition: group 7's `022C1740` array
and group 2's frame counters.

**Correction to this page's 2026-09-18 section above.** It ends: *"`_5380` (`0x460`) and `_8FA0`
(`0x1130`) are handed to nothing at all and still have no owner."* **Both halves are false against
the image:**
- `_5380` is group 1's receiver. The gate forms it with `add rcx, 0x5380` (`0028E2AB`), a form that
  scan's `lea`-only pattern could not see. OPUS's 2026-09-20 join records this.
- `_8FA0` is handed over by `add rcx, 0x8fa0` in `0028E070`, `0028E0C0` and `0028E1D0` (to
  `002BDB60` / `002BDC00`, gated on `+0x10F68` bit 6), and by the pump at `002917AA` / `002917B6`.

The sentence is struck in place and kept as history.

## SWE2-EC7-220 update (2026-10-03) - `get_interventionmenu_status` reads flag bits 13 and 4 of `+0x10F68`

The flag dword `+0x10F68` of the object at qword `0209BE80` carries the flag bits the `+0x10FA0` row of the mailbox table above names. `0028F970` (112 B, read whole) returns without a write when bit 13 is set (`bt ecx, 0xd`) and otherwise clears bits 4 and 10 and word `+0x10FA0`. The two bodies below read bits 13 and 4 of the same dword. Offsets and widths only; the verb name is the script's.

| function | size | verbs | what the body does | interior anchors |
|---|---|---|---|---|
| `002E2340` | 60 B | `get_interventionmenu_status` `0x0457` (its handler writes the return value as the verb's integer result) | calls `0028F6A0` and returns 0 when that returns 0, 1 for 1, 2 for 2 and 3 for any other value. `0028F6A0` returns only 0, 1 or 2, so the 3 arm is not reached through this call | Interior anchor `002E2344`; Interior anchor `002E234D`; Interior anchor `002E2352`; Interior anchor `002E2357`; Interior anchor `002E2361` |
| `0028F6A0` | 80 B | - (called by `002E2340`) | returns 0 when qword `0209BE80` is null, when bit 13 (`0x2000`) of its dword `+0x10F68` is set, or when `00273A20(object + 0xAB30)` returns 0 (`00273A20` is the 9-byte test that the qword at `rcx` is non-null). Otherwise it reloads `0209BE80` and returns 1 when bit 4 (`0x10`) of byte `+0x10F68` is set and 2 when it is clear (`and cl, 0x10`, `neg cl`, `sbb eax, eax`, `add eax, 2`) | Interior anchor `0028F6B7`; Interior anchor `0028F6C3`; Interior anchor `0028F6CA`; Interior anchor `0028F6DA`; Interior anchor `0028F6E6` |
