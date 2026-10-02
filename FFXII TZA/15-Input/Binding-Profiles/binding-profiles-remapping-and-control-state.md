---
system: Binding profiles, remapping and control-state translation
category: 15-Input
status: AUDITED — BP-5 / UQ-140 closed 2026-09-18 as NO ADMISSIBLE SOURCE, kind (b): codes 0 and 4-10 have no storage in any of the three device models, so why the numbering leaves the gap is an authoring fact (proposed FABLE, reviewed and signed OPUS)
owner_layer: PrimaryOwner:Input
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-12
audit:
  passes: 2
  last_pass: 2026-09-08
  last_pass_state: GN160-xiionline-61-translator-body
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# Binding profiles, remapping and control-state translation

> The table that says which physical control does which thing in FFXII — how it is stored, what
> happens when you assign a button that is already taken, and how it becomes the per-frame answer
> to "is this action being pressed?"

## 1. What the player sees

Open the config screen and reassign a button. Two things happen that this system decides.

**Assigning a button that is already in use does not steal it — it trades.** The control that had
that button gets the one you just took it from. Nothing is ever left unbound by a reassignment, so
you cannot accidentally strand an action with no button by shuffling things around. If the game is
set to refuse instead, the assignment is simply rejected and nothing moves.

**Some controls cannot be reassigned at all.** There is a fixed list of thirty-five control
identifiers the game will not accept as a new binding, and an attempt to use one is turned away
before anything changes.

The bindings are also grouped, and the groups are different sizes: a main group of sixteen, a second
of eight, and a third of four — twenty-eight slots in total per profile, and the game keeps three
profiles.

One more thing a player might notice without knowing why: **the game can swap Circle and Cross.**
It publishes its binding table, checks one platform setting, and if that setting is not zero it
exchanges those two entries. That is the Japanese-versus-Western confirm/cancel convention, and the
**same** setting also exchanges the two button masks the whole front end reads — one option, two
consequences. Proven 2026-09-02; see §8.

## 2. Native mechanism

### Where bindings live

Bindings are plain 32-bit control identifiers in a flat array at `01F80F90`. **That address has no
file backing at all** — it sits beyond the raw data of `.data`, which ends at VA `01F7E400` — so the
array is zero when the process starts and is filled at runtime.

**That does not mean the defaults are unreadable from the executable.** They are authored constants
in three separate tables (`01DF09C0`, `01DF0A80`, `01DF1470`) and are decoded in full by
[the keymap document](keymap-ini-file-format-and-default-controls.md) §4, which matches all 84 of
them against the file a player actually gets. Corrected in §10.

The array is three profiles of twenty-eight `u32` slots each — 84 slots, 336 bytes — and each
profile is internally divided into three groups. The divisions are proven by the range checks in the
assigner rather than by any header: group 0 rejects a slot index above 15, group 1 above 7, group 2
above 3, and the three group base addresses are exactly 16 and 24 dwords apart.

### Assigning a binding

`00198A00` is the only writer, and it is a policy function, not a store. In order:

1. **Group select.** A group id of 0, 1 or 2 picks the base and the slot limit. Anything else
   returns `3`.
2. **Range check.** Slot index above the group's limit returns `2`.
3. **Reserved-id rejection.** The new control id is compared against a fixed 35-entry table at
   `01DF13E0`. A match returns `2`. This runs *before* any conflict logic, so a reserved id can
   never displace an existing binding.
4. **Clear.** A control id of `0` writes `0` into the slot and returns `0`.
5. **Conflict scan.** The whole 84-slot array is scanned for another slot already holding this id,
   skipping the target's own flat index.
6. **Resolution.** No conflict → write and return `0`. Conflict with replacement disabled → return
   `1` and change nothing. Conflict with replacement enabled → **swap**: the conflicting slot
   receives the target slot's previous value, then the target receives the new id.

That swap is the mechanism behind the player-facing behaviour in §1. It is a genuine exchange, and
it is why remapping cannot silently unbind something.

### Turning bindings into a per-frame answer

`00197160` walks a profile and asks the input backend whether each bound control is currently
active. Which backend query it uses depends on **which band the control id falls in**, and the bands
are exact ranges tested with the standard unsigned subtract-and-compare idiom:

| Band | Test | Backend query |
|---|---|---|
| 1–3 | `(code - 1) < 3` | `InputBackend_IsPrimaryControlCode1To3Active(backend, code)` |
| 11–27 | `(code - 0x0B) < 0x11` | `InputBackend_IsControlCode11To27ActiveAnyDevice(backend, code)` |
| 28–152 | `(code - 0x1C) < 0x7D` | `InputBackend_IsControlCode28To283ActiveForBank(backend, code, 0)` |
| anything else | — | skipped entirely |

The band difference is real and meaningful: the middle band is satisfied by **any** device, while the
upper band is queried **per bank** with an explicit bank argument of `0`. Codes `4`–`10` and `0`
fall through every test and are never polled.

The result is written into a bitmask, and the polarity is the counter-intuitive part:

```c
if (controlIsActive)
    mask[i >> 3] &= ~(1 << (i & 7));      /* ACTIVE clears the bit */
```

An active control **clears** its bit. The caller must therefore hand in a mask pre-filled with ones,
and what comes back is "controls that are *not* active". Reading this as a pressed-mask inverts every
result.

The first loop covers exactly **16** slots — group 0. The walk then advances 18 dwords and runs a
second loop over `(kind, code)` pairs, taking the code only when the kind field equals `1`.

### Default profiles and the platform pair swap

`00195DF0` assembles a default profile record at `01DF1738`, then calls
`InputBinding_ShouldKeepAuthoredPairOrderForPlatformState` (`001DFA70`) — a three-instruction leaf:

```asm
CMP dword ptr [RCX + 0x64], 0x0
SETZ AL
RET
```

When that field is **non-zero** the function returns false and two adjacent dwords in the record,
at record offsets `+0x34` and `+0x38`, are **exchanged** before the record is bulk-copied out to
`01F80130`. So exactly one pair of neighbouring bindings is order-dependent on one platform state
value, and everything else is copied verbatim.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00198A00` | `InputManager_AssignBindingWithConflictPolicy` | 349 B | the only binding writer: group/range/reserved checks, conflict scan, swap-or-reject |
| `00197160` | `InputManager_TranslateBindingProfileToControlState` | 1,406 B | per-frame: band-dispatch each bound code to the backend, build the inverted control mask |
| `00195DF0` | GFZ: `InputManager_RestoreDefaultBindingProfiles` — **the name is backwards; this is the PUBLISHER** | 526 B | reads the **editable** array `01F80F90` (what the file loaded, or the player just remapped), applies the platform pair swap, publishes to `01F80130` |
| `00198000` | `InputManager_LoadKeymapIni` | 1,644 B | authored keymap load |
| `00198B60` | GFZ: `InputManager_MaterializeRuntimeBindingProfiles` — **the name is backwards; this is the DEFAULTS-INSTALLER** | 782 B | reads the authored constants at `01DF09C0`/`01DF0A80`/`01DF1470` and installs the shipped defaults over both the array and the records |
| `001DFA70` | `InputBinding_ShouldKeepAuthoredPairOrderForPlatformState` | 8 B | `cmp **dword** [rcx+0x64],0 / sete al / ret` — **a 32-bit test**; "`state[0x64] == 0`" reads as a byte one and a reimplementation that tests one byte swaps Circle and Cross backwards whenever `+0x65`..`+0x67` are non-zero *(corrected 2026-09-08 from the differential harness)* |
| `0035F690` | `InputControl_AdvanceChannelTimingState` | 205 B | per-channel hold timers and the ±546 ramp |

Addresses are Ghidra image base `0x00120000`. **Every row above is a function**, and its body size is
an exact-current body extent.

### Data addresses cited by this document

**Data, not functions** — no body extent. Listed separately so a cross-reference audit does not read
them as functions that have gone missing.

| Address | Name | Kind | Contents |
|---|---|---|---|
| `01F80F90` | binding array | `u32` array, 336 bytes | 3 profiles × 28 slots — **all zero in the shipped image**, filled at runtime |
| `01DF13E0` | reserved control ids | `u32` array, 35 entries | control ids the assigner refuses outright |
| `01DF1738` | live keyboard profile records | **not a staging buffer** | `01DF1480 + 2 x 0x15C` — records 2, 3 and 4 of a **five-record bank polled every frame** by `00196FF0`. The three keyboard profiles live here permanently. |
| `01F80130` | published runtime profiles | copy destination | what the rest of the game reads |
| `01F82D20` | platform/input state object | object pointer | its `+0x64` drives the pair swap (**BP-1**) |

## 4. Data structures and formulas

### Binding array layout

```
BindingProfile — 28 u32 (112 bytes); 3 profiles, 84 slots, 336 bytes total at 01F80F90

  dword  0 .. 15   group 0   (16 slots)   base 01F80F90
  dword 16 .. 23   group 1   ( 8 slots)   base 01F80FD0
  dword 24 .. 27   group 2   ( 4 slots)   base 01F80FF0
```

Flat index arithmetic, exactly as the assigner computes it:

```c
group 0:  flat = profile * 0x1C + slot;          reject slot > 0x0F
group 1:  flat = profile * 0x1C + slot + 0x10;   reject slot > 0x07
group 2:  flat = profile * 0x1C + slot + 0x18;   reject slot > 0x03
```

Note `0x1C` = 28 dwords = 112 bytes; group 2's base is stepped in **bytes** (`profile * 0x70`),
which is the same stride expressed differently — 0x70 = 112.

The conflict scan bound is `flat <= 0x53` (83), i.e. all 84 slots.

### Reserved control ids — the exact 35 entries at `01DF13E0`

```
2, 81, 82, 84, 85, 88, 89, 90, 119, 122, 123, 125, 130, 131, 132, 133, 134, 135,
136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152
```

(stored in the order `2, 81, 82, 84, 85, 88, 89, 90, 123, 119, 122, 130, 125, 131, 132, …, 152` —
the first thirteen are not sorted, the tail `131…152` is contiguous). The largest entry, **152**, is
exactly the top of the 28–152 polling band, which is a useful consistency check on both readings.

### Assignment result codes

```
0  assigned (or cleared)
1  conflict, and replacement was not permitted — nothing changed
2  slot index out of range for the group, OR the id is reserved
3  unknown group id
```

### Conflict swap — the exact exchange

```c
if (conflictingFlatIndex >= 0) {
    if (!allowReplace) return 1;
    bindings[conflictingFlatIndex] = target[slot];   /* old value moves to the conflicting slot */
}
target[slot] = newId;
return 0;
```

### Control-code band dispatch

```c
if      ((unsigned)(code - 0x0B) < 0x11)  active = IsControlCode11To27ActiveAnyDevice(be, code);
else if ((unsigned)(code - 0x1C) < 0x7D)  active = IsControlCode28To283ActiveForBank(be, code, 0);
else if ((unsigned)(code - 0x01) < 0x03)  active = IsPrimaryControlCode1To3Active(be, code);
else                                       /* not polled at all */;

if (active) mask[i >> 3] &= ~(1 << (i & 7));   /* active CLEARS the bit */
```

The backend handle is reached as `*(void **)(FUN_00796E20() + 0xDF8)` at every call site.

### Channel timing state — the fields and the constants

Record fields used by `0035F690`:

```
  +0x09  u8    flags        bit 4 (0x10) selects the held branch
  +0x10  s16   phaseCounter
  +0x12  s16   holdTimer    clamped to 1790
  +0x14  s16   subCounter   clamped to 180
  +0x16  s16   accumulator  clamped to [0, 16384]
  +0x18  s16   rate         signed per-tick delta added to the accumulator
```

The tail runs unconditionally:

```c
accumulator += rate;
if (accumulator < 0)      accumulator = 0;
if (accumulator > 16384)  accumulator = 16384;
```

Held branch (`flags & 0x10` set):

```c
holdTimer++;
if (holdTimer > 1759) rate = -546;            /* 0xFDDE as a signed short */
if (holdTimer > 1790) {
    phaseCounter++; subCounter++;
    holdTimer = 1790; accumulator = 0; rate = 0;
    if (subCounter   >= 180) subCounter = 180;
    if (phaseCounter >= 180) { phaseCounter = 0; holdTimer = 0; rate = +546; subCounter = 0; }
} else subCounter = 0;
```

Not-held branch:

```c
if (holdTimer > 0) { holdTimer++; if (holdTimer > 1790) holdTimer = 1790; }
subCounter++;
if (subCounter >= 180) { holdTimer = 0; subCounter = 180; accumulator = 16384; rate = 0; }
```

**This answers AP-3 as posed.** The **thresholds** are `1790` (hold-timer ceiling), `1760`
(the trigger to begin ramping down), `180` (the phase length for both counters) and `16384`
(the accumulator ceiling). The **rate** is `±546`, stored at `+0x18` and added once per tick.
`16384 / 546 ≈ 30` ticks to traverse the full accumulator range in either direction.

## 5. Call chain

```
config screen assigns a control
  -> InputManager_AssignBindingWithConflictPolicy  00198A00   [the only writer]
     -> reserved-id table 01DF13E0
     -> conflict scan over all 84 slots of 01F80F90

startup / restore defaults
  -> InputManager_RestoreDefaultBindingProfiles    00195DF0
     -> InputBinding_ShouldKeepAuthoredPairOrderForPlatformState  001DFA70
     -> publishes to 01F80130
  -> InputManager_MaterializeRuntimeBindingProfiles 00198B60     (same predicate)
  -> InputManager_LoadKeymapIni                    00198000      (authored keymap)

per frame
  -> InputManager_TranslateBindingProfileToControlState  00197160
     -> InputBackend_IsPrimaryControlCode1To3Active        (band 1-3)
     -> InputBackend_IsControlCode11To27ActiveAnyDevice    (band 11-27, any device)
     -> InputBackend_IsControlCode28To283ActiveForBank     (band 28-152, bank 0)
     -> control mask, ACTIVE = bit CLEARED
```

**Upstream:** the config screen (assignment) and startup (defaults, keymap). The **owner
transition** into gameplay is `00197160` — above it a binding is an authored id, below it a bit in
a per-frame mask.

**Downstream:** the capability policy in
[`../Gameplay-Capability-Policy/capability-inhibition-policy.md`](../Gameplay-Capability-Policy/capability-inhibition-policy.md),
which decides whether an intent is *allowed*, separately from whether it is *pressed*.

**Do not confuse with:**

- **The control mask is inverted.** Active clears. Every other mask in the input stack that this
  document's neighbours describe is positive-logic; this one is not.
- **`InputControl_*` and `InputManager_*` are different layers of one pipeline.** They share no direct call edge
  (*AP-4 answered 2026-09-13:* the channel layer calls `InputBridge_PollControlState` `00862670` → `InputAPI_PollControlState`
  `001E09B0` → `InputManager_PollAndBuildControlState`, which fills the channel layer's buffer `022CB680`), and the timing
  record in §4 belongs to `InputControl_*`, not to the binding profiles.
- **`01F80F90` is not the published profile.** `01F80130` is. The former is the editable table.

## 6. Modding notes

- **Best intervention point:** `01F80F90` itself. It is a flat `u32` array with no header, no
  checksum and no packing, and `00198A00` is its only writer. Writing a slot directly bypasses the
  reserved-id list and the conflict scan — which is exactly what you want if you are deliberately
  binding a reserved control, and exactly what will corrupt the user's config if you are not.
- **Regenerates itself:** the published copy at `01F80130` is rebuilt from the defaults path. Edit
  `01F80F90` and let the normal path publish; do not write `01F80130` and expect it to persist.
- **Breaks if:**
  - You read `01F80F90` out of the executable expecting defaults. It is 336 zero bytes at rest.
  - You treat the control mask as positive logic. Active clears the bit.
  - You bind a control id in `4`–`10`, or `0`, or above `152`. Nothing rejects it at assign time if
    you write the slot directly, but `00197160` will never poll it — the control silently does
    nothing.
  - You assume group sizes are uniform. They are 16, 8 and 4.
- **Multiplayer / XIIOnline:** bindings are **local input configuration** and must never be
  replicated. What crosses the wire is the resulting intent, not which button produced it. Two
  players with different remaps must produce identical gameplay effects; if binding state ever
  reaches the wire, a remap becomes a gameplay difference.
- **Mod compatibility:** the keymap INI read by `00198000` is authored data and the right surface for
  a mod to change. Two mods that both write `01F80F90` directly will silently overwrite each other
  because there is no versioning or ownership in the array.

## 7. What is not known

- [x] ~~**What the platform pair swap actually swaps, in player terms.** The mechanism is exact — one
      value at `state + 0x64`, two dwords at record `+0x34`/`+0x38` exchanged when it is non-zero —
      but the meaning is not established. A confirm/cancel (○/×) convention swap is the obvious
      hypothesis and is **not asserted here**; the GFZ's own annotation likewise declines to label
      it. **Killer observation:** find what writes `state + 0x64` on the object at `01F82D20`. If it
      is set from a region, locale or system button-assignment query, the hypothesis is supported;
      if it is set from anything else, it is refuted.~~ **Answered 2026-09-02 (§8 correction 3, `BP-1`): it swaps `Circle` and `Cross`**, the `DecideButton` setting (index 25, `+0x64` of the settings record at `01F82D20`); box ticked 2026-09-12 — the item never carried its ledger id, so the consistency check could not see it.
- [x] ~~What the 35 reserved control ids *are*. They are consistent with either Windows virtual-key
      codes or the game's own control-code space; the value `2` and the run `131`–`152` fit both
      readings, so the table alone does not decide it.~~ **Answered 2026-09-07 (`BP-2`, the extension section below): a bind blacklist in the game's own control-code space** (`PInputKeySemantic − 1`); box ticked 2026-09-12.
- [x] ~~The meaning of the `(kind, code)` pair walk in the second half of `00197160`, and why the walk
      advances 18 dwords when a profile is 28.~~ **`BP-3` answered 2026-09-12 by propagation from `DC-1` / `AP-5` (the translator-body section below):** `00197160` walks the **`0x140`-byte runtime record**, not the `0x70` authored profile — sixteen digital codes, then sixteen 16-byte entries `{mode, axisId, codeA, codeB}` from `+0x40`. The second loop's pointer starts at int 18 (`+0x48`, entry 0's `codeA`) and steps four ints; the "kind" it tests against 1 is the entry's `mode` (1 = a digital code drives an axis). "18 dwords when a profile is 28" compared against the wrong structure.
- [x] ~~What the channel timing accumulator at `+0x16` drives. The arithmetic is exact and the
      constants are classified as thresholds vs rate (**AP-3 answered**), but nothing here shows what
      consumes a 0–16384 triangle ramp.~~ **`BP-4` answered 2026-09-12 (FABLE): the vibration gain.** Its only reader, `InputControl_UpdateDeviceFeedbackOutput` (`0035F590`, called from `InputControl_PollAndBuildChannelHistory`), writes the two motor bytes at `022CB5C0` while record `+0x09` bit 2 is set: motor 0 = `strength(+0x07) × accumulator >> 14` (`0035F5E3`–`0035F5FA`), motor 1 = bit 7 of `strength(+0x06) × accumulator >> 14`, an on/off motor (`0035F61B`–`0035F639`). With the timing rules above, **a vibration held continuously fades to nothing after 1,760 channel updates over about 30 more, and is restored to full strength once it has been released for 180 updates** — a built-in cut-off for sustained rumble. The update rate per second is not read here.
- [x] **`UQ-140` / `BP-5` — CLOSED 2026-09-18, `NO ADMISSIBLE SOURCE`, kind (b)** (proposed by FABLE, reviewed and signed by OPUS; the signature and its evidence are the section below). Why codes `4`–`10` and `0` exist in the id space but are polled by no band. **There is no storage for them in any of the three device models**, so the remaining question is why the numbering leaves a gap — an authoring decision the executable cannot testify to.
- [x] ~~The binding profile *file* format — `00198000` (`LoadKeymapIni`) is still unread.~~
      **CLOSED:** read in full and `AUDITED` in
      [keymap-ini-file-format-and-default-controls.md](keymap-ini-file-format-and-default-controls.md).
      This document still covers the in-memory form only, which is a scope statement rather than an
      open question.


## `BP-5` closed — the reviewer's signature, and a stronger negative than the row asked for (2026-09-18, OPUS)

**Signed** under [`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) addendum 2026-09-15bk,
**kind (b)** — an intent question about shipped code. Bar 4 takes a reviewer who is not the author;
FABLE proposed the closure, and **one of its three standing legs is my own earlier work** (the
2026-09-15 reading of the shipped default profile), which is disclosed here rather than counted as
independent corroboration.

**The row named the step nobody had taken, and it was right to.** It said the answer *"depends on the
range `00197710` and `00197800` can return, which nobody has measured"*. That measurement is no
longer the question, because **the three backends each refuse `4`–`10` on their OWN guard**, whatever
any caller hands them — banded reader, unbanded caller, or a value straight out of the binding table:

| backend | its own bound, read from the body | accepts |
|---|---|---|
| `0079E650` | `lea ecx, [rdx - 0xb]` / `cmp ecx, 0x11` / `jae` (`0079E66D`) | **11–27** |
| `0079E6A0` | `lea eax, [rdx - 0x1c]` / `cmp eax, 0x100` / `jae` (`0079E6B6`) | **28–283** |
| `0079E6D0` | `lea eax, [rdx - 1]` / `cmp eax, 3` / `jae` (`0079E6DC`) | **1–3** |

Code `0` fails all three the same way, by wrapping below zero. **The guard is the backend's, not the
ladder's**, which is the distinction this page drew and then had to leave open.

### And the bound is the size of the array, which is what makes this structural rather than a census

Each backend indexes a byte array sized exactly to its range — `[code-0x0B + slot + 0x30]` over 17
bytes, `[code-0x1C + bank + 0x30]` over 256, `[code-1 + dev + 0x1E0]` over 3. **The three bytes after
the primary device's button array are already in use as something else.**
`0079D010` — the mouse reader this page already cites — loops `r13` over `0`–`2`
(`0079D19C inc r13d` / `cmp r13d, 3` / `jb`), polls channels `11`–`13` (`lea edx, [r13 + 0xb]`), and
keeps **two parallel three-byte arrays on the same object at `[rsi+0x150]`**: it compares the new
state against `[rax + r13 + 0x1E3]` (`0079D15B`), publishes the change to `[rax + r13 + 0x1E0]`
(`0079D16F`) and then writes the new value back to `[rax + r13 + 0x1E3]` (`0079D194`). **`+0x1E0` is
the current state of codes 1–3 and `+0x1E3` is their previous state**, for edge detection.

> **Had `0079E6D0`'s guard read `cmp eax, 6` instead of `cmp eax, 3`, codes 4–6 would have returned
> the PREVIOUS state of the mouse buttons** — stale input reported as a live control. The bound is
> not a stylistic choice; it is the edge of the array, and the byte after it belongs to another one.

*(`+0x1E6` on a device object in the same family is a poll-enable flag — `007A1816
cmp byte ptr [rbx + 0x1e6], 1` in `DirectInputMouse_PollState`. Consistent with the button array
ending at three; the two bases were not traced to the same object, so it is offered as consistency
and not as proof.)*

### What is therefore established, and what is left

**Established: `0` and `4`–`10` have no storage in any of the three device models.** The primary
device holds three button bytes then its own shadow copy; the slot devices hold seventeen bytes
beginning at code `11`; the banks hold two hundred and fifty-six beginning at code `28`. There is no
byte anywhere that a code in `4`–`10` addresses. That is a stronger statement than *"no reader is
known"* and it does not depend on any census being complete.

**Left: why the numbering leaves the gap.** An id space with a range nothing implements is an
authoring decision, and no byte of this executable, no authored table and no live run can produce the
reason. That is precisely kind (b), and it is what the closure says.

*Method note: an earlier version of this review swept all 38,161 `.text` bodies for memory operands
at `+0x1E0`–`+0x1E9` and got 355 sites at `+0x1E0` alone, across unrelated structures. **A
displacement is not a structure**, and that sweep could never have proved an absence — what it was
good for was surfacing `0079D010`'s `+0x1E3` traffic, which is what turned the answer structural.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 3 profiles × 28 slots; groups of 16 / 8 / 4; flat-index arithmetic | complete exact-current body of `00198A00`: three group bases 16 and 24 dwords apart, three distinct slot limits, scan bound `0x53` | 1 |
| Conflict resolution is a **swap**, not an overwrite | complete body of `00198A00` — the conflicting slot is assigned the target's previous value before the target is written | 1 |
| Result codes 0/1/2/3 and their exact causes | complete body of `00198A00` | 1 |
| The 35 reserved ids and their values | raw read of `01DF13E0`, 140 bytes, and the loop bound `< 0x23` in the body | 1 |
| The binding array is zero **at load** | `01F80F90` lies **beyond `.data`'s raw size** — the section's raw data ends at VA `01F7E400`, so the image contains no bytes there at all. Corrected in §10: the original row cited a 336-byte raw read that cannot have happened | 1 |
| Band boundaries 1–3, 11–27, 28–152 and their distinct backend queries | complete exact-current body of `00197160` — three unsigned subtract-and-compare tests | 1 |
| Active **clears** the mask bit | complete body of `00197160`: `mask[i>>3] &= ~(1 << (i&7))` under `if (active)` | 1 |
| The platform predicate is `state[0x64] == 0` | complete 3-instruction disassembly of `001DFA70`: `CMP dword ptr [RCX+0x64],0x0 / SETZ AL / RET` | 1 |
| One adjacent dword pair is exchanged when the predicate is false | complete body of `00195DF0` | 1 |
| Timing thresholds 1790 / 1760 / 180 / 16384 and rate ±546 | complete exact-current body of `0035F690`; `0xFDDE` read as a **signed** short is −546 | 1 |
| Body extents | `DumpFullCoverageGraph.java` regenerated at the GN checkpoint | 1 |

**Corrections to a neighbouring document.** `../Input-Stack/input-stack-device-channel-and-bindings.md`
describes the upper control-code band as **28–283**. At the `00197160` call site the test is
`(unsigned)(code - 0x1C) < 0x7D`, which is **28–152**. The callee's GFZ name
(`IsControlCode28To283ActiveForBank`) may still reflect what the callee accepts; what this document
claims is only what this caller routes. That neighbour is flagged for re-audit, not overwritten.

**Superseded readings — three corrections, 2026-09-02, all from a peer session working the file format.**

1. **Two function names were exactly backwards, and this document propagated them from the GFZ.**
   `00195DF0` ("RestoreDefaultBindingProfiles") reads the **editable** array and **publishes** it;
   `00198B60` ("MaterializeRuntimeBindingProfiles") reads the authored constants and **installs the
   shipped defaults**. Settled **without reading either body**: `001E0F70` (reset to defaults) calls
   *Materialize then Restore*, which is incoherent unless Materialize is the defaults-installer, and
   `001E1050` (assign one binding) calls *Restore alone*, which is the publish. **Call order settled
   what two function names asserted wrongly** — and this document had repeated the names because they
   were plausible, which is the error the evidence standard's "the GFZ can be wrong" rule exists for.

2. **`01DF1738` is not a staging buffer.** It is `01DF1480 + 2 × 0x15C` — records 2, 3 and 4 of a
   five-record bank that `00196FF0` polls every frame. The three keyboard profiles live there
   permanently, so this document's "assembled before the pair swap" framing was wrong about the
   object's lifetime, not just its name.

3. **The platform pair swap is Circle ↔ Cross, and §1 originally declined to say so.** That caution
   was right at the time — the hypothesis was unproven and the GFZ also declined to label it — but it
   is now proven by three independent agreements, the load-bearing one being that the name table at
   `01DF11E0` gives index 13 = `Circle` and index 14 = `Cross`, which are exactly the two dwords
   exchanged at record `+0x34`/`+0x38`. **The proof came from a name table, not from the "obvious"
   ○/× inference this document deliberately refused to make.**

## 9. Related

- [`../Input-Stack/input-stack-device-channel-and-bindings.md`](../Input-Stack/input-stack-device-channel-and-bindings.md) — the device/channel layer beneath this; **its 28–283 band bound is corrected above**
- [`../Gameplay-Capability-Policy/capability-inhibition-policy.md`](../Gameplay-Capability-Policy/capability-inhibition-policy.md) — whether an intent is permitted, as opposed to pressed
- [`../../16-UI/Request-Router/`](../../16-UI/Request-Router/) — where confirmed inputs become UI requests

## 10. Falsification pass 2026-09-03 (repos-2d)

Run against snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`,
parent `2ed8affb…`, embedded EXE `73461d08…`.

**Disclosure first.** This session used the *sibling* keymap document twice as a source and has now
audited it. The check for whether any of that borrowed context lives **here** was run rather than
assumed: no document of mine cites this one, and the three things borrowed — `00197710`'s
signature, the `01DF11E0` name table, and the name-index-is-slot-index rule — are all claims of the
keymap document, each re-derived in its pass. **Nothing was borrowed from here**, so this pass is
an ordinary audit rather than a self-check.

### SURVIVED — the mask polarity, which is the document's most counter-intuitive claim

§2 says an active control **clears** its bit, and that reading it as a pressed-mask inverts every
result. The encoding:

```asm
00197218  call 0079E6D0          ; the band backend query
0019721D  test al, al
0019721F  je   0x197244          ; NOT active -> leave the bit alone
00197221  mov  edx, ebx
00197225  and  edx, 7            ; i & 7
00197232  sar  eax, 3            ; i >> 3
00197238  movzx eax, byte ptr [rcx + r14]
0019723D  btr  eax, edx          ; bit test and RESET  <- active clears
00197240  mov  byte ptr [rcx + r14], al
0019724A  cmp  ebx, 0x10         ; the first loop is 16 slots = group 0
```

`btr` is *bit test and reset*. The claim is exact, including the 16-slot bound and the
`mask[i>>3] &= ~(1 << (i&7))` rendering.

### SURVIVED — the three bands and their three distinct backends

`cmp eax, 2 / ja`, `cmp eax, 0x10 / ja`, `cmp eax, 0x7c / ja` after the corresponding subtracts —
i.e. `< 3`, `< 0x11`, `< 0x7D`, giving **1–3**, **11–27**, **28–152** — each dispatching to a
different backend (`0079E650`, `0079E6A0`, `0079E6D0`). Codes 4–10 match no test. Exact.

### The ladder in one body, and 131 codes the backend answers for that nothing asks about

*Added 2026-09-15 (FABLE), while checking a register sentence that said this body has no third
band. It has three, this document has always said three, and here is the cleanest form of it.*

The four fall-through chains in `00197160` are not the only place the ladder appears.
**`00197990` is the entire three-band ladder in 134 bytes**, and it reaches each backend by
**tail-jump rather than call** — so a call-edge census does not see it as a caller of any of the
three:

```asm
001979AB  lea  eax, [rbx - 0x0B] / cmp eax, 0x10 / ja   ; 11..27
001979C6  jmp  0079E650
001979CB  lea  eax, [rbx - 0x1C] / cmp eax, 0x7C / ja   ; 28..152
001979E9  jmp  0079E6A0
001979EE  lea  eax, [rbx - 1]    / cmp eax, 2    / ja   ; 1..3
00197A09  jmp  0079E6D0
00197A0E  xor  al, al                                    ; everything else is false
```

Covered: **`1`–`3`**, **`11`–`27`**, **`28`–`152`**. Uncovered below 152: **`0`** and **`4`–`10`**,
which is `BP-5`'s set, now readable in one body instead of assembled from four chains.

**The three backends are three different device models, not three ranges of one.** Read whole:

| backend | how it scopes the device | where the state byte is |
|---|---|---|
| `0079E650` | loops **18 slots** from `[rcx+0x88]` — *any* device | `[code-0x0B + slot + 0x30]` |
| `0079E6A0` | indexes **one bank**, `r8d < 7`, at `[rcx + bank*8 + 0x118]` | `[code-0x1C + bank + 0x30]` |
| `0079E6D0` | one pointer at `[rcx+0x150]` — a single primary device | `[code-1 + dev + 0x1E0]` |

That is consistent with `DM-2`'s reading of codes 1–3 as the mouse buttons: the band with its own
single-device pointer is the band with three codes in it.

**And the middle backend's own domain is wider than the ladder's guard — but the guard is the
ladder's, not the backend's callers'.** `0079E6A0` bounds itself with `lea eax, [rdx - 0x1C]` /
`cmp eax, 0x100` / `jae`, accepting **`28`–`283`** (`0x1C`–`0x11B`). Both banded readers —
`00197160` at four sites and `00197990` — stop at `cmp eax, 0x7C`, which is **`28`–`152`**.

**That is as far as it goes, because five other callers apply no band test at all.**
`0017DDC0`, `0017DE10`, `0017DEA0` and `0017DFC0` each resolve a binding through `00197710` and pass
the result **straight into `edx`** — there is no `lea`/`cmp` pair anywhere in any of them.
`001E0E70` bounds its own *input* at `cmp ecx, 0x80`, maps it through `00197800`, and then sends the
result to `0079E6D0` when it is `1` or `3` and to `0079E6A0` otherwise, again with no band test on
what it sends. So:

> Whether any code above `152` is ever queried is **not decided in the readers**. It is decided by
> what `00197710` and `00197800` can return, which is a property of the binding table and **is not
> measured here**.

**NOT CLAIMED, and this is a narrowing of what I first wrote on this page:** that `153`–`283` is an
unqueried region. The first version of this subsection said it was — *"131 codes the backend answers
for that nothing asks about"* — and that was read off the two banded readers while five unguarded
callers were sitting in the same caller list I had already printed. What is established is the
arithmetic of two bounds and the fact that only two of seven callers impose the narrower one.

**What this does and does not do to `BP-5`.** It does not answer it: the row asks *why* codes exist
that nothing polls, and this does not explain `4`–`10`. What it adds is that the band structure is
**the ladder's**, not the input system's — the backend accepts a wider range than the ladder offers
it, and most of its callers do not use the ladder at all. `4`–`10` is a hole in one reader's
dispatch, not necessarily a hole in the id space, and that distinction is available to the row.

**Two instrument notes, because both are the same lesson.** First: `00197990` reaches all three
backends and calls none of them. It was found by listing the backends' callers with a scan that
counted `jmp` as well as `call`; the `call`-only version of the same scan returns `00197160` and
stops. A tail-jump is a call that a call-edge census cannot see, and it is the third kind of
invisible edge this database has met this month, after the image-base idiom and the folded base.

Second, and it cost a correction above rather than a discovery: the caller list that produced
`00197990` *also* contained the five unguarded callers, in the same printout, at the same time. I
read the two that confirmed the band structure and generalised from them. **A caller list is not a
finding until every entry in it has been read**, and the entries that do *not* match the pattern are
the ones that bound the claim.

### SURVIVED — `01DF1738` is **not** a staging buffer, and this document is the one that is right

`01DF1738 - 01DF1480 = 0x2B8 = 2 × 0x15C` **exactly**, so it is record 2 of the five-record bank —
precisely what §3 and §8 already say. See the correction below: the *neighbour* that claimed
otherwise about this document was the one out of date.

Also re-verified in the sibling's pass and unchanged here: the reserved table is exactly **35**
dwords to `01DF146C`, and `001DFA70` is `CMP [RCX+0x64],0 / SETZ AL / RET` at 8 bytes. The group
bases are 16 and 24 dwords from the array base (`01F80FD0`, `01F80FF0`).

### CORRECTED — an evidence row citing a read that cannot have happened

§8 carried: *"The binding array is all zero in the shipped image — raw read of `01F80F90`, 336
bytes, every byte zero."*

**There are no 336 bytes there to read.** `.data` begins at VA `01DF0000` with a raw size of
`0x18E400`, so its file-backed data ends at VA **`01F7E400`** — and `01F80F90` is beyond it. The
address is uninitialised data with **no file backing at all**.

The *conclusion* is right: the array is zero when the process starts. The *evidence* was not a read
of the image; it was a read of a tool's zero-fill for a region the image does not contain. This is
the standard's own rule — **a zero from a tool that did not read anything looks exactly like a zero
from a tool that read zeros** — reaching a published evidence row. The row now cites the section
layout, which is what actually establishes it.

### CORRECTED — a consequence drawn from that, and it was false

§2 continued: *"It is filled at runtime, **which is why you cannot read the game's default controls
straight out of the executable**."*

You can, and the sibling document does. The defaults are authored constants at `01DF09C0`,
`01DF0A80` and `01DF1470`; all **84** were decoded from the image and matched byte for byte against
the `keymap.ini` a player actually gets. The premise (this *array* is empty in the image) is true;
the consequence (the *defaults* are unreadable from the image) does not follow, because the defaults
do not live in this array.

### CORRECTED — a stale open item, and a stale claim in the other direction

§7 listed *"the binding profile file format — `00198000` is still unread"*. It is read in full and
`AUDITED` in the sibling document. Closed.

**And the same staleness runs the other way.** The keymap document's §8 said this document *"calls
`01DF1738` a staging buffer"* — but this document says the **opposite**, explicitly, with the same
arithmetic. That sentence was already out of date when it was written, and it survived that
document's two falsification passes because **both passes attacked its claims about the binary and
neither attacked its claims about the corpus.** Corrected there, by me, with the reason recorded.

The document still carrying "staging" for `01DF1738` is the input-stack document's §11, which is
where the keymap document's Related list already points.

> **Two documents each described the other as it used to be.** Neither document's own gates can
> catch that: `audit_crossrefs` compares documents to the *binary*, never to each other. A claim
> about a neighbour is the one kind of claim in this database that nothing re-checks.

### Status

`audit.passes` 0 → 1. **Status stays `PARTIAL`**: §7 still carries five genuine unknowns —
the meaning of the platform pair swap's target, what the 35 reserved ids are, the `(kind, code)`
walk and its 18-dword stride, what consumes the timing ramp, and why codes 4–10 exist unpolled.
Those are open questions, not unattacked claims.

### What was not attacked

The channel timing state (`0035F690`, its thresholds and the ±546 rate), the assignment result-code
paths beyond their enumeration in §2, and the second `(kind, code)` loop in `00197160` were not
re-derived. They are the three areas a second pass should take.

## `00198A00` opened — the rebinding conflict policy

`InputManager_AssignBindingWithConflictPolicy` (`00198A00`, 349 B) was the last-but-two entry on the
*leaned on and never opened* cut, cited by three documents by name only.

**Extent checked**: 98 instructions, ends `ret` at `00198B5C`, no `jmp` leaves the extent.

### Three device classes tile one 28-slot row

```asm
00198AA5  cmp r10b, 0x10     ; class 0 -> 16 slots, index = slot
00198A75  cmp r10b, 8        ; class 1 ->  8 slots, index = slot + 0x10
00198A49  cmp r10b, 4        ; class 2 ->  4 slots, index = slot + 0x18
00198A28  mov eax, 3         ; class >= 3 -> reject
```

**16 + 8 + 4 = 28 = `0x1C`**, and the three classes' base offsets — `0`, `0x10`, `0x18` — place them
end to end with no gap and no overlap. **The profile stride is `0x70` = 112 bytes = 28 dwords**, which
is the same 28. **Every number in the geometry agrees with every other**, which is the strongest kind of
confirmation available for a layout.

### Conflict detection is global across profiles, not per profile

```asm
00198B00  cmp rax, 0x54      ; the scan bound
```

**`0x54` = 84 = 3 × 28**, and the scan walks the class-0 base — **so it covers three profiles' worth of
bindings in one sweep.**

> **A key already bound in a different profile is a conflict.** The binding array is one flat 84-entry
> space and the search does not stop at a profile boundary — so the three profiles are not independent
> keymaps, they are three regions of one.

### Four outcomes, and the caller chooses whether a conflict is fatal

| return | meaning |
|---:|---|
| `0` | assigned |
| `1` | **conflict, refused** — another slot already holds this code |
| `2` | slot index out of range for the class, **or the code is reserved** |
| `3` | device class `>= 3` |

**The sixth argument is a swap flag.** On a conflict:

```asm
00198B1B  cmp  byte ptr [rsp + 0x30], 0
00198B20  jne  swap
00198B22  mov  eax, 1                        ; refuse
...
00198B32  mov  eax, dword ptr [r9 + r11*4]   ; the target's current code
00198B39  mov  dword ptr [rdi + rcx*4], eax  ; ...into the conflicting slot
00198B3C  mov  dword ptr [r9 + r11*4], r8d   ; ...and the new code into the target
```

> **With the flag clear the assignment is refused; with it set the two bindings trade places.** The
> engine implements both remapping policies and the choice is the caller's, not a setting.

**Assigning code `0` clears the slot** and returns `0` without any conflict scan.

### Thirty-five codes cannot be bound at all

A table at `01DF13E0`, **35 entries**, checked before anything else; a match returns `2`:

```
02  51 52 54 55 58 59 5A  77 7A 7B 7D 82
83 84 85 86 87 88 89 8A 8B 8C 8D 8E 8F 90 91 92 93 94 95 96 97 98
```

**Twenty-two of the thirty-five are the contiguous run `0x83`–`0x98`**, and the remaining thirteen are
scattered singles. The dword after the table is `0`, so the bound of 35 is confirmed by the data as
well as by the loop.

**What these codes are is not established** — this function only refuses them. They are recorded as a
list because *"which inputs the game will not let you rebind"* is answerable from it once the code
space is named.

### What is not established

- [x] ~~What the three device classes are. Their **slot counts** (16, 8, 4) are exact; their identities
      are not read here.~~ **Answered on this page (the 28-slot profile section below):** kind 0 = the sixteen pad buttons (`Select` … `Square`, names at `01DF11E0`), kind 1 = the eight stick half-axes (`RX_P` … `LY_N`, `01DF1260`), kind 2 = the four specials `Speed1`, `Speed2`, `Speed3`, `WalkMode` (`01DF12E0`); box ticked 2026-09-12.
- [x] ~~What input-code space `01DF13E0` is expressed in.~~ **Answered by `BP-2` (below): the game's own control-code space**, settled by the adjacent default table `01DF1470` = F1, F2, F3, Left Shift; box ticked 2026-09-12.
- [x] ~~**UQ-141.** Whether all three profiles are simultaneously live, or whether cross-profile conflict is a
      deliberate policy rather than a consequence of one flat array.~~
      **ANSWERED 2026-09-15 (FABLE): both, and the question's *rather than* is the part that is wrong.**
      `00196550` settles it in 135 bytes:

      ```asm
      00196558  lea  r11, [rip + 0x1DEAA31]   ; r11 = 01F80F90, the profile array
      0019655F  lea  r10, [rip + 0x1DEAB7A]   ; r10 = 01F810E0, one past the LAST profile
      00196566  lea  rbx, [rip + 0x1C5AE73]   ; 01DF13E0, the reserved list
      0019656D  lea  r9,  [rip + 0x1C5AEF8]   ; 01DF146C, its end
      00196580  lea  rax, [r8*4]              ; outer index, in DWORDS
      0019658B  mov  ecx, [rax + r11]
      0019658F  cmp  r8, 0x54                 ; 84 iterations
      001965A4  cmp  ecx, [rax]               ; inner: every LATER element
      001965AC  cmp  rax, r10 / jl            ; ... to the end of the THIRD profile
      ```

      **The bound is the arithmetic that answers the row.** `01F810E0 - 01F80F90` = `0x150`, and
      `0x150 / 4` = **84** = `0x54`, the outer bound. So the scan treats
      `01F80F90`–`01F810DF` — **all three `0x70` profiles** — as **one flat run of 84 dwords with no
      profile stride anywhere in it**, and compares every element against every later one.

      **So all three profiles are live at once, and the flat array is not an accident that permits
      cross-profile conflict — it is the thing a dedicated function scans for it.** A duplicate in
      profile 0 and profile 2 is found by the same `cmp` that finds two in profile 0. The row offers
      *deliberate policy* and *consequence of one flat array* as alternatives; the code has both,
      because the flat array is the **mechanism** and the 84-dword scan over it is the **policy**.
      `00196550` then checks the same values against the reserved list at `01DF13E0`–`01DF146C`, which
      this page already documents as 35 dwords — so one function refuses a binding for either reason.

      **What is still not established** is what `00196550` does on a hit (`001965CF`) and who calls it;
      neither is needed for this row, and neither is claimed.
- [x] ~~Which callers pass the swap flag set.~~ **Answered 2026-09-12 (FABLE):** the binding writer
      `00198A00` has one caller, the wrapper `001E1050`, which turns its fourth argument into the flag
      (`001E1084`–`001E1096`) and, on any result but a refusal, republishes the profiles through `00195DF0`
      (`001E10C8`–`001E10D0`). The wrapper's three call sites are all in one widget message procedure, `0023C5C0`
      (loaded by `lea` in `0023CE10`; its message switch `0023C5D5`–`0023C5FE`, unhandled messages to the base
      procedure `005C5230`): the message-13 notify arm with command `0x2CA1` passes **1** (`0023C625`); the message-10 arm
      (the per-frame input sample) passes **0** when the widget is capturing a key (`+0xEC` set: `001E0C50` reads the
      pressed code, `0023C716`–`0023C74A`), and **1** when it is not capturing, input bit 15 (`0x8000`) is down and the row
      cursor `+0xE8` is 0 (`0023C8AF`–`0023C8F5`, after `005841B0`). Not capturing, the Decide mask `01E0C2A0` starts a
      capture (`0023C80C`–`0023C830`) and the other two tested bits move the cursor. So **a key captured for a slot refuses
      one already bound elsewhere, while the notify and the bit-15 path swap it.** ~~the message-2 arm passes **1** …~~
      *(an arm misattributed in the first version of this answer, corrected the same day)*. Which screen `0023CE10`
      builds, and what `0x2CA1` and row 0 are, are not read.

> **Crossing into Audio — FINAL-AUDIT pass 22 (FABLE, 2026-09-14).** `0023CE10`, the builder that loads the procedure
> above, is this page's one edge into the Audio subsystem. It calls the gated sound-request wrapper `00249C60` three
> times, with cue slots `3` (`0023D277`), `0x25` (`0023D3D1`) and `2` (`0023D3F3`). `00249C60` returns `-1` without a
> sound while the global gate `02091098` is set; otherwise it resolves the bank-local slot and plays it with `(0x40, 0x7F)`
> ([the sound request contract](../../18-Audio/Audio-Boundary/CONTRACT-sound-request.md) §2).
> These are the screen's own feedback sounds. Nothing in the binding writer `00198A00` or the conflict policy reaches
> Audio, and which on-screen events the three slots accompany is not read.

## Extension 2026-09-07 — `BP-2` answered: the 35 reserved codes are a bind-blacklist

`xiionline-61`, GN160 `fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708`.
Both readers of `01DF13E0` read in full.

### What a player sees

Some keys cannot be assigned to anything. In the remapping screen they will not take; edited into
`keymap.ini` by hand they are refused and the slot keeps whatever it had. **And when you assign a key
that is already doing another job, the game does not silently double-book it** — it either refuses,
or it *swaps*, handing the old key to the control you took it from. Which of the two happens is a
flag the caller passes, not a property of the key.

### `BP-2` — they are in the game's own control-code space, not Windows virtual-key codes

The question recorded that the value `2` and the run `131`–`152` fit either reading. **The adjacent
table settles it.** Immediately past the reserved list sits a four-dword table at `01DF1470`, read by
`InputManager_MaterializeRuntimeBindingProfiles` with a single `movups`:

```
01DF1470:  65, 66, 67, 118
```

Under the code mapping this document already established (**`PInputKeySemantic − 1`**; 65–76 = F1–F12,
117–122 = modifiers) that is **F1, F2, F3, Left Shift** — *exactly* the shipped `Speed1`, `Speed2`,
`Speed3`, `WalkMode` defaults recovered independently from `keymap.ini` under `BP-6`. **Two tables,
one encoding, and the second was decoded without reference to the first.** Windows VK codes would
give `A`, `B`, `C`, `F7`, which is not a coherent default set.

### What the reserved list *does* — from both of its readers

**`InputManager_ValidateBindingUniqueness` (`00196550`, 135 B)** walks the whole binding array and
returns *invalid* on two conditions:

```c
for (i = 0; i < 0x54; i++) {                    /* 84 = 3 profiles x 28 slots, at 01F80F90 */
    code = binding[i];
    for (j = i + 1; j < 0x54; j++)              /* (a) duplicate anywhere in all 84 */
        if (code != 0 && code == binding[j]) return 1;
    for (p = 01DF13E0; p < 01DF146C; p++)       /* (b) code appears in the reserved list */
        if (code == *p) return 1;
}
return 0;
```

`01DF146C − 01DF13E0 = 0x8C = 35 dwords`, so **the "35 reserved ids" count is the loop bound itself**,
not a count of a run that looked like it stopped. Code `0` is exempt from the duplicate test and is
not in the reserved list, so **`0` means "unbound" and any number of slots may hold it**.

**`InputManager_AssignBindingWithConflictPolicy` (`00198A00`, 349 B)** is the single-assignment path,
and it checks the same list *before* anything else:

```c
assign(profile, kind, slot, code, swapOnConflict):
    kind 0 (buttons):  base = 01F80F90 + profile*0x1C,  slot < 16   else return 2
    kind 1 (axes):     base = 01F80FD0 + profile*0x1C,  slot <  8   else return 2
    kind 2 (special):  base = 01F80FF0 + profile*0x70,  slot <  4   else return 2
    otherwise return 3

    for (k = 0; k < 0x23; k++)                  /* 35 -- the reserved list */
        if (code == 01DF13E0[k]) return 2;      /* REFUSED */

    if (code == 0) { base[slot] = 0; return 0; }        /* unbind always succeeds */

    find j in all 84 slots (excluding this one) with binding[j] == code
    if none                       -> base[slot] = code; return 0;
    if (!swapOnConflict)          -> return 1;                   /* refuse */
    binding[j] = base[slot];                                     /* SWAP */
    base[slot] = code;  return 0;
```

**Return codes:** `0` assigned · `1` conflict refused · `2` slot out of range **or code reserved** ·
`3` bad kind.

> **A reserved code and an out-of-range slot are the same error.** Nothing distinguishes *"that key is
> not allowed"* from *"that slot does not exist"* to the caller, which is why a hand-edited
> `keymap.ini` using a reserved code fails without saying why.

### The 28-slot profile, confirmed from a second direction

The three `kind` cases give slot limits **16, 8 and 4**, and the three name tables hold exactly
**16, 8 and 4** entries:

| kind | base | slots | names at | contents |
|---:|---|---:|---|---|
| 0 | `01F80F90` | 16 | `01DF11E0` | `Select L3 R3 Start Up Right Down Left L2 R2 L1 R1 Triangle Circle Cross Square` |
| 1 | `01F80FD0` | 8 | `01DF1260` | `RX_P RX_N RY_P RY_N LX_P LX_N LY_P LY_N` |
| 2 | `01F80FF0` | 4 | `01DF12E0` | `Speed1 Speed2 Speed3 WalkMode` |

**16 + 8 + 4 = 28**, the profile stride (`0x1C` dwords), and 3 × 28 = **84**, the validator's `0x54`.
`BP-6` derived 28 from the *file*; this derives it from the *assignment code*. **Two independent
routes to the same layout**, and the name tables are UTF-16, which is why an 8-bit read of them
returns only first letters.

Indices 13 and 14 of the button table are `Circle` and `Cross` — the pair `BP-1` proved the platform
swap exchanges.

### The reserved codes themselves

```
2 · 81 82 84 85 88 89 90 · 119 122 123 · 125 130 · 131 132 133 … 152
```

Against the bands this document established: **81–90 is punctuation** (with 83, 86 and 87 *absent* —
those three remain bindable), **117–122 is modifiers** (119 and 122 reserved, 123 just past the
band), and **131–152 is a contiguous run of 22 above every documented band.** The value `2` sits below
the A–Z band at 28, in the low region `BP-5` already flags as polled by nothing.

**What is not established:** *why* each is reserved. The contiguous 131–152 tail reads as enum values
with no keyboard behind them, and the punctuation exclusions read as layout-dependent keys — but
neither is proven, and the function only tells us that they are refused, never why.

### Modding notes

- **Binding a reserved code fails with the same error as a bad slot index.** If a hand-edited
  `keymap.ini` line silently does not take, check the code against the 35 above before anything else.
- **`0` unbinds and is always legal.** It is the only value exempt from the duplicate rule.
- **The swap is the caller's choice.** The same assignment either refuses or steals the key from its
  previous owner depending on one flag, so a mod that drives this function directly decides which.
- **Duplicate detection spans all three profiles**, not one — a key used in `[Keyboard1]` cannot be
  reused in `[Keyboard3]`.

## The translator body, read — 2026-09-08: `AP-2` answered, `AP-5` advanced

`InputManager_TranslateBindingProfileToControlState` (`00197160`, 1,406 B) was the largest unread
function in this category. **It is the whole per-frame path from a binding profile to the bytes the
game acts on**, and it settles two open questions.

### ⚠ The control mask is active-LOW

For each of the **sixteen** digital slots:

```c
code = slot[i];
if (deviceGate()) {
    if      ((unsigned)(code - 11) < 17)  active = IsControlCode11To27ActiveAnyDevice(backend, code);
    else if ((unsigned)(code - 28) < 125) active = IsControlCode28To283ActiveForBank(backend, code, 0);
    else if ((unsigned)(code -  1) <  3)  active = IsPrimaryControlCode1To3Active(backend, code);
    else                                  continue;          /* codes 4-10: polled by nothing */
    if (active)
        mask[i >> 3] &= ~(1 << (i & 7));                     /* CLEAR the bit */
}
```

> **A pressed control clears its bit; an unpressed control leaves it set.** The mask is written by
> `AND NOT`, never by `OR` — so **a byte of `0xFF` means nothing is held**, and reading the mask as
> "1 = pressed" inverts every control.
>
> Sixteen slots, one bit each, packed eight to a byte: **the digital state is two bytes.**

The three band tests appear in the order 11–27, 28–152, 1–3, and `(unsigned)(code - 28) < 125`
confirms the corrected upper band of **28–152** rather than 28–283, as `AP-1` recorded.

### `AP-2` answered — `0x80` is the analog neutral, and it is a literal

The axis path multiplies out to, with every constant read from the image:

```c
v = GetFilteredAnalogAxisValue(backend, axisId);      /* nominally -1.0 .. +1.0 */
if (axisId == 2) { v *= -1.0; if (invertX) v *= -1.0; }
if (axisId == 3) { v *= -1.0; if (invertY) v *= -1.0; }
if (deviceMode == 1) v = 0.0;
else if (v != 0.0) analogUsedFlag = 1;

out = (v + 1.0) * 128.0 + ((float)currentByte - 128.0);
out = clamp(out, 0.0, 255.0);
```

| constant | address | value |
|---|---|---|
| the centre | `008F3A2C` | **128.0** |
| the bias | `01CEBBA8` | 1.0 |
| the clamp maximum | `008C5B40` | 255.0 |
| the inversion multiplier | `01CEBC9C` | **−1.0** |
| loaded, unused on this path | `008F3A28` | 120.0 |

> **`(v + 1.0) * 128.0` maps a stick range of −1 … +1 onto 0 … 256, centred on 128.** The same
> `128.0` is subtracted from the current byte, so a byte already sitting at 128 contributes nothing.
> **`0x80` is the neutral, and it is not an inference from "the midpoint of a byte" — it is the
> literal `128.0` at `008F3A2C`, used twice.** `AP-2` is answered **yes**.

**And the invert setting un-inverts.** Axes 2 and 3 are multiplied by −1.0 **unconditionally**, and
multiplied by −1.0 **again** when the per-axis flag at `DAT_01F7FFE0 + 8` / `+ 9` is set. **The engine
inverts those two axes by default; the option restores them.**

`DAT_01F7FFE0 + 0x38` is set to 1 whenever a non-zero axis value arrives — a *"the stick has been
touched"* flag, distinct from any binding.

### Three binding modes, from the mode word

Group-1 entries carry a mode at `entry[-2]`:

| mode | meaning |
|---:|---|
| **1** | digital → axis: if the bound code is active, the axis byte is written **`0xFF`** outright |
| **2** | **two digital codes synthesised into one axis** |
| **3** | a real analog axis, the formula above |

**Mode 2 is how a keyboard drives an analog axis.** The first code contributes **−0x7F** and the
second **+0x80**, both added to the byte's current value, then clamped to `[0, 255]`:

```c
axis = currentByte;
if (active(codeA)) axis += invert ? +0x7F : -0x7F;
if (active(codeB)) axis += invert ? -0x80 : +0x80;
axis = clamp(axis, 0, 255);
```

> **From the 128 neutral this gives 1 for full negative and 255 for full positive** — deliberately
> asymmetric by one, because the contributions are −127 and +128 rather than ±127.5. **Stated as the
> code computes it rather than rounded to "0 to 255".**
>
> The same per-axis flags invert mode 2, and for axes 2–3 the sign is forced positive regardless.

### What this leaves open

**`AP-5` is advanced, not closed.** The *translation* is now read; the **profile record layout** it
walks is still only known from the outside — group 0 is sixteen `int` codes, group 1 entries are at
least `{mode, axisId, codeA, codeB}` reached at `param_1 + 0x12`, and the stride between group-1
entries has **not** been derived. `DC-1`.

The device gate `FUN_001C1990()[0] != 1 || FUN_00228480()` is unread, and it decides whether any
binding is polled at all. `DC-2`.

> **`DC-2` answered 2026-09-14 (FABLE): in the shipped image the gate never closes, because its first term is always true.**
> - **`001C1990`** returns `[01F81268]`. That global has exactly three rip-relative references (`tools/ripscan.py`):
>   the ensure-singleton `001C1940` tests it and stores it (`001C194F`, `001C197F`), and the getter reads it.
>   - `001C1940` allocates a **4-byte** object, writes its only field **`= 0`** (`001C1970`) and publishes it.
>   - 10 of the getter's 11 call sites only **compare** field 0: five sites in `InputManager_TranslateBindingProfileToControlState`
>     `00197160`, `00197998`, `001A9F78`, `001BDBD9`, `001EC117`, `0018829D`.
>   - The eleventh, `0018832A`, passes the pointer to `0016D6A0`, the folded empty function.
>   - Nothing stores into the object after construction, so **field 0 stays 0 and `[0] != 1` always holds**.
> - **`00228480`** would matter only when field 0 is 1. It returns whether the widget pointer `01FD4948` is set. `00228490`
>   creates that `0xD0`-byte widget (proc `002284F0`, `002284CD`–`002284D2`) when `0017E4C0()` — the input backend's byte
>   `+0x27` — is 0 (`0022839B`–`002283AE`), and the proc's message-18 arm clears the pointer (`00228526`).
> - **Consequences:**
>   - every binding is polled: `001971B7`–`001971C3` never takes the skip to `00197244`;
>   - the mode-3 path that forces the axis to neutral (`00197431`–`0019743A`, `movaps xmm6, xmm8`) never runs;
>   - the three `je` sites (`001A9F80`, `001BDBE1`, `001EC11F`) always fall through to their other checks.
> - **Limits.** A writer in unlisted code, or one reached through a computed address, is not excluded; the listed image has
>   none. What the value 1 was meant to signal is not in the image.

`008F3A28` = 120.0 is loaded into a register on every iteration of the first loop and **not used on
any path read here** — either a deadzone for a branch not taken in this reading, or a hoisted load
for the section of the body beyond the third mode. `DC-3`.

> **`DC-3` answered 2026-09-14 (FABLE): it is `WHEEL_DELTA`, used by a fourth binding mode that reads the mouse wheel.** The
> load is hoisted once after the first loop (`00197253`). Its only use is `00197383 divss xmm0, xmm12` in the second loop's
> **mode-4** arm.
> - **The dispatch.** The second loop switches on the group-1 entry's mode `[rbp−8]`: 1 → `0019760E`, 2 → `0019748E`,
>   3 → `001973E5`, **4 → `001972C7`** (`001972A0`–`001972C1`). So the translator has four modes, not three.
> - **The mode-4 arm, when `[rbp−4]` is 4.**
>   - Codes `0xB` / `0xD` / `0xC` test the backend mouse-button bytes `+0x170` / `+0x171` / `+0x172` (`001972D1`–`00197320`).
>   - **Code 3** takes the mouse device at backend `+0x150` (type 0, the device behind control codes 1–3,
>     [the input name registry](../Input-Name-Registry/the-input-name-registry-and-channel-aliases.md)). It asks that device's
>     slot `+0x20` for **channel 3** (`00197355`–`00197379`), divides by **120.0**, truncates to an integer
>     (`00197383`–`00197388`) and hands it to `00196480(inputManager, n)`.
>   - It adds `n` to `[01F7FFE0]+0x0C` and stores it at `+0x10` (`0019738E`–`001973A4`). When `n` is non-zero it calls the
>     backend's slot `+0xC8` (`001973AF`–`001973BC`).
> - **Why this is the wheel.** 120 is Win32's `WHEEL_DELTA`, the raw delta of one wheel notch, and the arm turns the raw
>   channel value into whole notches, accumulated in one field and kept for the current frame in the other. The channel
>   number and the constant fit a mouse Z axis; the device driver was not read to confirm channel 3.

### `DC-1` answered — the record the translator walks

The two loops give the layout exactly. Loop 1 runs `while (i + 1 < 0x10)` over `int`s from the base;
loop 2 starts at `param_1 + 0x12` **ints**, advances `param_1 += 4` **ints**, and returns when
`0xF < i + 1` — **sixteen entries of four `int`s each.**

Because loop 2 reads `param_1[-2]` and `param_1[-1]`, the pointer sits on each entry's **third**
field, so the first entry begins at `+0x40`:

```
+0x00   int[16]    sixteen digital binding codes   -> control-mask bits 0..15
+0x40   entry[16]  sixteen 16-byte entries:
                     +0x00  int  mode      1 = digital->axis, 2 = two codes -> axis, 3 = analog axis
                     +0x04  int  axisId    passed to GetFilteredAnalogAxisValue; 2 and 3 are inverted
                     +0x08  int  codeA     mode 2: the negative direction (-0x7F)
                     +0x0C  int  codeB     mode 2: the positive direction (+0x80)
= 0x140 bytes
```

**Sixteen digital slots and sixteen axis entries — 320 bytes per record.**

### ⚠ This is not the `.ini` profile layout, and the difference is load-bearing

[`keymap-ini-file-format-and-default-controls.md`](keymap-ini-file-format-and-default-controls.md)
derives a **`0x70`-byte** per-profile stride at `0x01F80F90`, with groups of **16, 8 and 4** slots.
**The translator's record is `0x140` bytes with groups of 16 and 16.** They are different shapes and
neither derivation is wrong: that document also records the translator being run **five times over a
bank at `0x01DF1480`**, which is not `0x01F80F90`.

> **So there are two structures: the authored profile as stored from the `.ini` (`0x70`), and the
> runtime record the per-frame translator walks (`0x140`).** A remapping tool must not assume editing
> one edits the other.
>
> ~~**The conversion between them is not established** — nothing read here writes the `0x140`
> record, and the stride between the five banked records is not derived either.~~ **Both are
> established now — `DD-1` is ANSWERED.** The converter is `00195DF0`, read in full in
> [the contract](CONTRACT-binding-profiles.md) §7a, and the stride is `0x15C`, derived from the
> poll loop's own three `add reg, 0x15C` sites and recorded as the `InputBindingRecord` type row.
> The sentence is kept struck through because the reasoning that produced it is what §`DD-1` below
> corrects.

### The frame the translator fills, and the fill that proves the last two findings

`InputManager_PollAndBuildControlState` (`00196FF0`, 356 B) is the **only** function in the image that
references the record bank at `0x01DF1480`. It builds a control-state frame **on the stack** and then
runs the translator over the bank five times.

The initialisation, before any binding is examined:

```asm
00197085  or      rax, -1
00197089  lea     rsi, [01DF1480]              ; the binding-record bank
00197090  mov     word ptr [rbx], ax           ; +0x00..+0x01 = 0xFFFF
00197093  movabs  rax, 0x8080808080808080
0019709D  mov     dword ptr [rbx + 2], eax     ; +0x02..+0x05 = 0x80 0x80 0x80 0x80
001970A0  xor     eax, eax
001970A2  mov     qword ptr [rbx + 6], rax     ; +0x06..+0x0D = 0
001970A6  mov     dword ptr [rbx + 0xe], eax   ; +0x0E..+0x11 = 0
001970A9  lea     r14d, [rax + 5]              ; five records
```

**The frame is 18 bytes:**

| offset | size | contents |
|---|---|---|
| `+0x00` | 2 | the **digital mask** — sixteen bits, one per slot |
| `+0x02` | 16 | sixteen **axis bytes**, written by the translator at `+2 + i` |

> **Two independent confirmations of the previous two blocks, from the producer rather than the
> consumer:**
>
> **The mask is initialised to `0xFFFF`.** The translator only ever clears bits
> (`&= ~(1 << ...)`), so all-ones is *nothing held*. **Active-low, proven twice from opposite ends:
> the initialiser sets every bit and the consumer only clears them.**
>
> **The first four axis bytes are filled with `0x80`** by a `movabs 0x8080808080808080`. `AP-2` asked
> whether `0x80` is the analog neutral; the translator answers it with the literal `128.0` at
> `008F3A2C`, and **the initialiser answers it again by writing `0x80` into the axes before anything
> touches them.** Two different functions, two different encodings of the same constant.

**And an asymmetry worth having:** only axes **0–3** get the `0x80` neutral. **Axes 4–15 are
initialised to zero** — `qword [rbx+6]` and `dword [rbx+0xe]`. So the first four axis bytes are
centred quantities and the remaining twelve are not, which is what one would expect of two sticks
plus twelve slots that are digital-derived or unused. **Which of the twelve are actually written by
any shipped profile is not established here.**

### `DD-1` — the direction was settled here, and the writer was found afterwards

`0x01DF1480` has **one** reference in the whole image, and it is this `lea` — **the bank is read, not
written, on this path.** The five records are the translator's *input*; the output is the stack
frame.

> **Corrected 2026-09-08 — the conclusion drawn from that was wrong.** This section went on to infer
> that the writer *"does not name the bank's address directly, so it reaches it through a pointer."*
> **It does not.** `00195DF0` writes records 2–4 by naming **`01DF1738`** — an address `0x2B8` bytes
> inside the same bank — through an **image-base register** (`lea r15, [rip-0x75e23]`; `[r15 +
> 0x1cd1738]`). Not a pointer: a different offset into the same object, invisible to a
> RIP-relative scan. Full derivation in
> [the binding-profiles contract](CONTRACT-binding-profiles.md) §7a and §14a; `DD-1` and `DD-3` are
> answered.

**So the `.ini` profile at `01F80F90` and the runtime bank at `01DF1480` are touched by disjoint
function sets under a RIP-relative scan** — six functions reference the former, one references the
latter, and no function references both.

> ~~**Nothing found so far converts one into the other**, and `DD-1` stays open with a sharper
> shape: the writer does not name the bank's address directly, so it reaches it through a
> pointer.~~
>
> **Struck 2026-09-10. This paragraph sat *after* the correction block above and contradicted it**
> — a reader got the answer and then the stale conclusion. `DD-1` is **ANSWERED**: `00195DF0`
> converts the `0x70` authored profile into the `0x15C` runtime record, and it reaches the bank
> through an **image-base register**, not a pointer. "Disjoint function sets" was true only of the
> instrument: a RIP-relative scan cannot see `[r15 + 0x1cd1738]`.
>
> The two shapes are now type rows — `InputBindingProfile` (`0x70`) and `InputBindingRecord`
> (`0x15C`, of which the translator reads `0x140`) — so the distinction a remapping tool must
> respect is carried by the store rather than by this prose.

## Runtime validation — 2026-09-08

**The chain in this document was resolved in a live process** and every link held.
[`EXP-005`](../../_experiments/EXP-005-driving-the-input-state.md).

```
[0x02EA5368]                  ->  0x01F7E350   the input manager
manager + 0xDF8               ->  0x01F7F150   the backend        (as this document states)
backend + device*8 + 0x118    ->  a HEAP block; it moves between launches
block + 0x30 + (code - 0x1C)  ->  one byte per input, non-zero means held
```

> **Corrected 2026-09-13 (FABLE), statically; the live links above still hold.**
> - `[0x02EA5368]` is the **Phyre application object** (constructor `00792350`, store `00792550`), not the input manager.
>   The input manager is `[01F7FFE0]`.
> - The "block" is the `PFramework::PInputDeviceKeyboard` object.
> - `+0x30` is not a held level. It is a **transition latch**: `0079D010` writes it when the polled level changes, and
>   `0079AE90` / `0079AE40` clear it when a caller consumes it. The level itself is `+0x231`, written by
>   `DirectInputKeyboard_PollState` `007A1640` from `GetDeviceState` through the `DIK_*` remap table `01F3DAB0`.
>
> The writers, readers, clearers and the gated poll path are in
> [the input-stack page](../Input-Stack/input-stack-device-channel-and-bindings.md), §2 *The keyboard byte array*.

**Device 0 is the only non-null of the seven** at the title screen — 1 through 6 are `NULL`,
which is what a machine with no gamepad attached should look like. **The 256-byte array is all
zero when nothing is held.**

### The index is `code - 28`, and this is now MEASURED — [`EXP-006`](../../_experiments/EXP-006-the-array-is-written-on-transition.md)

The earlier reading *inferred* `index = keymap_value - 28` from the minimum code being 28 and
the query subtracting `0x1C`. **Eighteen keys were then pressed for real and every one moved
exactly one byte**, with the game verifiably foreground and a clean no-key control:

| key | index | code (`index + 28`) | `GameSetting.ini` name |
|---|---:|---:|---|
| Escape | 36 | 64 | **Start** |
| Space | 52 | 80 | **Circle** |
| Tab | 51 | 79 | **L3** |
| LControl | 89 | 117 | **R2** |
| LShift | 90 | 118 | **WalkMode** |

**Five named bindings land on their own codes**, so the claim is `PROVEN` rather than `HIGH`.

> **The array is indexed by PHYSICAL KEY, not by game action.** The other thirteen keys land
> on codes no binding names — `A`→28, `D`→31, `Z`→53, `Up`→108, `Enter`→77. The
> `[Keyboard1]` section is a binding **out of** this space, and most of the space is unbound.
>
> **Annotation 2026-09-13 (FABLE):** "physical key" means **DirectInput scan code**. The index maps to a `DIK_*` code
> through `01F3DAB0`. `Up`→108 is index 80, `0x48` `DIK_NUMPAD8`: the harness's `SendInput` carried the arrow's scan
> code without the extended flag. `DIK_UP` (`0xC8`) is index 65. A key event with no scan code cannot move any byte.

### The game writes a byte only when the key's state CHANGES

```text
hold Escape for real  ->  the game sets index 36 to 1
write 0 over it, keep holding
    -> 000000000000000     fifteen polls, 300 ms, the game NEVER restores the 1
```

**A per-frame snapshot would have restored it on the next frame.** It did not, so this array
is a **transition-written cache of key state** — not a per-frame snapshot, and not a command
buffer. Writing a level into it produces no change for anything downstream to consume, which
is why `EXP-005`'s written byte both persisted and did nothing.

> **2026-09-13 (FABLE): the mechanism is confirmed, but the last sentence does not follow from the code.**
> - **Confirmed.** `0079D010` compares the polled level `+0x231` with `+0x130` and writes `+0x30` only when they differ, so a
>   written value persists until the next physical change.
> - **Not supported.** "Nothing downstream to consume" does not hold. The binding translator `00197160` reads `+0x30` on every
>   poll through `0079E6A0` (a plain `cmp`, no clear). A `1` written to a bound code in the translator's band (28–152) is
>   therefore read as held, and the channel layer sees it as a new press. `EXP-005`'s writes were checked only against entity
>   slots, `st2e` and area id, which cannot show a menu cursor move.
> - **Open.** Why that write produced no visible response. The candidates are that the poll did not run in that frame mode
>   (see the input-stack page's gated path) or that the indicators were too coarse.

**Real input does drive the game.** Four presses through `SendInput` with the window
foreground moved area id `12` → `306` and filled a save buffer that had been all zero —
**17,584 NEW bytes against a 31-byte reversal**, where the same instrument scored a symmetric
319-against-311 when the game was not focused.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Resource — CLIENT.** An 8-byte function this page cites is called by a 597-byte Resource body.
- **Developer — CLIENT, not read.** The same 8-byte function is called by a 1,046-byte Developer-labelled body.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Party — CLIENT.** `PartyControl_BuildAnalogMovementVectorFromInputHistory` (`003594E0`), owned by
that layer, calls `0017DFC0` on this page. That caller is a **461-byte analog-movement vector
builder**: it loads a float pair constant from `01EF9220`, takes an early arm that zeroes the global
at `022C800C`, and otherwise consults this page's binding resolver at `00359518` before building the
vector. **The crossing is that the Party layer consults one of this page's four binding resolvers,
not that this page owns anything in Party** — the resolver family is described in this document's own
section on `00197710`. Its own callees are not named, per the 2026-09-16 refinement of the crossing
rule. Read from the shipping bytes 2026-09-16 (FABLE), closing one of the five pass-22 findings
`OPUS` measured RED at `HEAD`.

**CoreRuntimeScheduling — CLIENT.** `FUN_0017d4c0`, owned by that layer, calls `001C1940` on this page. That caller is a 387-byte setup that takes a **`0x20`-byte allocation** and initialises it, carrying on with a null result rather than failing; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT (SWE2-EC7-158, 17 edges).** Batch-123's `00182EE0` names `001DDAB0`, whose callers include the presentation layer (`001CD0..`), and `00195820`/`001C1990` reach `00865EC0`/`00187950`/`001BDAC0` there — the profile layer consults shared helpers, not a second owner.
- **Application - CLIENT (1 edge).** `00792350` is also called by bodies filed to application: `0015BC40` - shared machinery across the layer boundary, no shared ownership.
- **Platform - CLIENT and SERVICE (3 edges).** `005CC8A0` is also called by bodies filed to platform: `0061F200`; `00196480`, `00792350` reach bodies filed to platform: `005CC930`, `005CD0A0` - shared machinery across the layer boundary, no shared ownership.
- **PlatformOnlineAchievements - CLIENT (1 edge).** `00796E20` is also called by bodies filed to platform/online achievements: `008655A0` - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - SERVICE (1 edge).** `00866200` reaches bodies filed to save/load: `00865AE0` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT (2 edges).** `003936B0`, `00583FD0` are also called by bodies filed to save/load/settings: `005823B0`, `0057E4D0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT and SERVICE (16 edges).** `002B4090`, `0017DDC0`, `00228480` are also called by bodies filed to UI: `00252030`, `003C8B70`, `00276D30` (+9 more); `0023CE10` reaches bodies filed to UI: `00291D80` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT (1 edge).** `00228480` is also called by bodies filed to world area: `00314020` - shared machinery across the layer boundary, no shared ownership.
## `AU-2` / `AU-3` — the initialiser found, and the `{2, 4}` head explained (OPUS, 2026-09-14)

`AU-2` asks what distinguishes the three profiles at `01F80130` (stride `0x15C`); `AU-3` asks what
the four consecutive 16-byte `{2, 4}` constants configure. Both are answerable from the static
initialiser, which nobody had named. Read from the shipping image at the authority hash
`73461D08…9721F8`.

### One function INITIALISES all three profiles — and it is not the only one that touches them

> **CORRECTED 2026-09-14 (OPUS), on `AUDITSPEC-AU23-15BD30-NOT-EXCLUSIVE`.** This section was
> published claiming `FUN_0015BD30` holds **24 of the 24** rip-relative references into
> `01F80130`–`01F80544`. **It holds 15.** SWE2-AUDIT-SPEC's all-bodies census is right and the
> published exclusivity claim is withdrawn; a recount with the same instrument gives **15 / 3 / 6**:
>
> | function | refs | what it does |
> |---|---:|---|
> | `FUN_0015BD30` | **15** | the initialiser described below |
> | `FUN_00196290` (488 B) | **3** | **reads the profiles out** — `lea rdx, [01F80130]` / `[01F8028C]` / `[01F803E8]`, then a `0x80`-per-iteration `movups` copy **from** the profile **into** `01DF1738` |
> | `FUN_00198960` (109 B) | **6** | **a second writer** — `+0x34` / `+0x38` of each profile |
>
> **How the error was made, because it is the same shape twice in one day.** The count of 24 was
> measured over the address range; the 15 were read inside one body; and the two numbers were put in
> one sentence without the sweep that would have joined them. Nothing checked that the body's
> references *were* the range's references. That is the `FE-1` defect wearing different clothes — a
> census asserted rather than enumerated — and it is why the recount instrument now exists.
>
> **`FUN_00198960` is a SWAP, and that matters more than the count.** For each profile it loads a
> pair of words from `.data`, **writes them back exchanged**, and mirrors the exchanged pair into the
> profile's `+0x34` / `+0x38`:
>
> ```
> 00198960  mov ecx, [01DF176C]          ; source pair, word A
> 00198966  mov eax, [01DF1770]          ;              word B
> 0019896C  mov [01DF176C], eax          ; EXCHANGED IN PLACE
> 00198972  mov [01DF1770], ecx
> 00198978  mov [01F80164], eax          ; profile 1 +0x34 = B
> 00198984  mov [01F80168], ecx          ; profile 1 +0x38 = A
> ```
>
> and again for `01DF18C8` / `01DF18CC` → `01F802C0` / `01F802C4`, and `01DF1A24` / `01DF1A28` →
> `01F8041C` / `01F80420` — **a distinct source pair per profile**. Running it twice restores the
> original, so it is a **toggle of one binding pair across all three profiles at once**, which is
> exactly the shape a remapping page should want and is not initialisation at all.
>
> **`FUN_00196290` is the consumer lead `AU-2` said was missing.** It copies **out of** the profiles
> into `01DF1738`, `0x80` bytes per iteration, for all three bases. So `01DF09C0` / `01DF0A80` are the
> authored defaults, `01F80130`+ is the live set, and `01DF1738` is a working copy taken from it.
>
> **What survives unchanged:** everything below about what `FUN_0015BD30` itself writes, the `0x15C`
> stride, and the `{2, 4}` record head. The initialiser reading was never in question; the word
> *"all"* was, and it is withdrawn.

**After a binding change only the left stick's keys are re-latched (added 2026-09-19, FABLE; one body read whole).**
`00196680` (131 B) runs once from the input poll when the manager's one-shot byte `+0x3B` is set. It reinstalls the
three published profiles into the polled bank (`FUN_00196290`, above), then for each editable profile hands four
codes to the backend's level-to-latch copy - the dwords at `01F80FE0 + profile x 0x70`, which are **group 1's slots
4-7: `LX_P`, `LX_N`, `LY_P`, `LY_N`**. So a movement key held across a rebind keeps its true level in the latch the
game reads; the sixteen buttons and the right stick are not touched. Interior: `0019668A`, `0019668F`, `00196696`,
`001966A5`, `001966AF`, `001966B9`, `001966CC`, `001966E0`, `001966EF`.

### What `FUN_0015BD30` writes

**`FUN_0015BD30`** (484 B, `Runtime.StaticLifetimeInfrastructure`) holds **15 of the 24**
rip-relative references into `01F80130`–`01F80544`. It writes each profile in two parts:

```
0015BD30  movaps xmm0, [01DF09C0]        ; four 16-byte constants, from .data
0015BD3E  movaps xmm1, [01DF09D0]
0015BD4C  movaps [01F80130], xmm0        ; -> profile +0x00
0015BD53  mov    edx, 2
0015BD62  movaps [01F80140], xmm1        ; -> profile +0x10
0015BD70  movaps [01F80150], xmm0        ; -> profile +0x20
0015BD77  movaps [01F80160], xmm1        ; -> profile +0x30
0015BD80  lea    rax, [rax + 0x80]       ; then a 0x80-per-iteration copy loop
0015BD87  movups xmm0, [rcx]             ;   from 01DF0A80 into profile +0x40 onward
```

The same shape repeats at `01F8028C` and `01F803E8` — **exactly `0x15C` apart**, confirming the row's
stride and its count of three.

### `AU-3`: ~~the `{2, 4}` is the head of every 16-byte record in the source table~~ `field0` is a per-record CODE COUNT

> **REFUTED 2026-09-16 (OPUS) on `FABLE-CONTRA-OPUS-AU3-THE-2-4-IS-A-COUNT-NOT-A-HEAD`. THE THREE
> RECORDS QUOTED BELOW ARE THE WHOLE OF THE ERROR — they are records 0–2, and only FOUR of the
> table's sixteen begin with a 2.** Dumped as four `int32` per 16-byte record from `01DF0A80` to the
> first all-zero record at `01DF0B80`: **16 records**, `field0` is **2 in four and 1 in twelve**.
> **`field1 == 4` is the only value constant across all sixteen**, and the rule is exact —
> **`field0 == 1` if and only if `field3 == 0`, 16 of 16 with no violations** — so **`field0` counts
> the trailing codes**: `{2, 4, 0x5C, 0x5B}` carries two, `{1, 4, 0x27, 0x00}` carries one.
>
> **The `{kind, class, primary, alternate}` reading below therefore loses its premise**, because that
> reading explained "the constant head" and there is no constant head. The DIK-scancode inference is
> untouched and still unproven for want of a consumer; what changes is that the table has **one-code
> and two-code entries**, which is the shape a reimplementation has to honour and which a head
> reading concealed.
>
> **The sample was quoted and the table was not.** Three consecutive records were shown as if they
> established a universal, and they were the unrepresentative head of a sorted table.

`01DF0A80`, the bulk copy source, is an array of 16-byte records ~~and every one begins `{2, 4}`~~ whose first four are the only ones beginning `{2, 4}`:

```
01DF0A80  02 00 00 00  04 00 00 00  5c 00 00 00  5b 00 00 00
01DF0A90  02 00 00 00  04 00 00 00  5e 00 00 00  5d 00 00 00
01DF0AA0  02 00 00 00  04 00 00 00  1f 00 00 00  1c 00 00 00
01DF0AB0  02 00 00 00  04 00 00 00  2e 00 00 00  32 00 00 00
```

**So `2` and `4` are not two constants among four — they are the CONSTANT HEAD of a
`{2, 4, code, code}` record**, and what varies is the trailing pair. `mov edx, 2` / `mov r8d, edx` in
the initialiser passes the same `2` as an argument, so it is a kind or class selector rather than a
datum.

The four 16-byte constants written at `+0x00`–`+0x3F` are pure quadruples with no `{2, 4}` head:

| | |
|---|---|
| `01DF09C0` | `0x28 0x4F 0x23 0x40` |
| `01DF09D0` | `0x24 0x27 0x26 0x25` |
| `01DF09E0` | `0x37 0x75 0x36 0x38` |
| `01DF09F0` | `0x2D 0x50 0x1E 0x21` |

### What the trailing values look like, marked as an inference

Every varying value across both tables falls in **`0x1C`–`0x75`**, and the set includes `0x1C`,
`0x1E`, `0x1F`, `0x21`, `0x2D`, `0x2E`, `0x32`, `0x4F`, `0x50`. **That is the range and shape of DIK
scancodes**, and a `{kind, class, primary, alternate}` record would explain both ~~the constant head~~
**a constant `field1`** and the paired tail. **This is a reading of value ranges and is NOT proven
here** — no consumer was read, and a table of small integers in that range could be several things.
*(Corrected 2026-09-16: there is no constant head. `field0` is a per-record code count — 2 in four
records, 1 in twelve, with `field0 == 1` iff `field3 == 0` across all sixteen — so a
`{count, class, primary, alternate}` shape fits the bytes where `{kind, class, …}` does not. The
scancode range reading stands and is still an inference.)*

### What is established, and what each row still owes

- **Established:** one initialiser writes all three profiles; the stride and the count of three are
  confirmed from its own stores; the `{2, 4}` is a record head rather than configuration; the source
  tables are `01DF09C0` (four quadruples) and `01DF0A80` (the `{2,4,…}` array).
- ~~**`AU-2` still owes** what distinguishes the three — the initialiser writes all three from `.data`
  sources, so the distinction is in the source content and needs a consumer read, not a data read.~~
  **`AU-2` ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5), by the consumer read:** the three are the keymap's
  `[Keyboard1]`–`[Keyboard3]` layouts, and they are **active simultaneously**, not alternatives. Every poll,
  `00196FF0` runs the translator over all five records of the `01DF1480` bank into one control frame
  (`001970A9`–`001970C6`, five iterations, no condition). The three profiles are records 2–4 (§3), and the
  translator only clears bits of the active-low mask. The only distinction is authored content: main, numpad and
  the short Q/E/Z/X-and-mouse layout of [the keymap page](keymap-ini-file-format-and-default-controls.md). The
  Confirm Button exchange (`BP-1`) applies to all three at once.
- ~~**`AU-3` still owes** what the two trailing codes mean, which is the scancode inference above.~~
  **`AU-3` ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): the codes are keyboard control codes, and the sixteen
  records are the default keyboard bindings. The four `{2, 4}` records at `+0x40`–`+0x70` are the two-key axes.**
  Static plus a decode of the shipping bytes.
  - **The codes are control codes, not raw scancodes.** Every code lies in `0x1C`–`0x76` (28–118). That is inside
    the keyboard band 28–152 of [the keymap page](keymap-ini-file-format-and-default-controls.md), and the band's
    first value, 28, is the smallest.
  - **Mapped to keys.** `DirectInputKeyboard_PollState` (`007A1640`) turns such a code into a DirectInput scancode
    through the 125-byte table at `01F3DAB0`, indexed by code − 28 (the keymap page's DM-2 note). Put through that
    table, the sixteen records are:
    - records 0–3, kind 2 (an axis: positive code, then negative): `{0x5C, 0x5B}` → **Right / Left**, `{0x5E, 0x5D}` → **Down / Up**, `{0x1F, 0x1C}` →
      **D / A**, `{0x2E, 0x32}` → **S / W**. `UQ-144` reads the kind-2 arm.
    - records 4–15, kind 1 (one code): **L**, **J**, **I**, **K**, **R**, **Space**, **C**, **F**, **1**, **3**, **Tab** and
      **Left Shift**.
  - **The controls.** The scancode names are the DirectInput standard (`DIK_` values). The decode yields a coherent
    layout — WASD, the arrow cluster and an IJKL diamond — and no code falls outside the table.

  *Not established:* which stick or pad function each axis and key drives, which needs the profile's consumer
  read; the constant `4` is the sub-kind, which only the mouse kind reads (`UQ-144`).

*(Read by OPUS 2026-09-14. Both rows narrowed; neither closed.)*


## The `00792350` exclusive subtree — all 6 members bound (SWE2-FRONTIER, followup queue)

`00792350` — the Phyre application-object constructor this page names (store `00792550` →
`[02EA5368]`) — owns **6 frontier functions**. Every member was disassembled from the
shipping image; interior cites are one instruction inside each declared extent. The root
(832 B) builds the ~0x10E0-byte object: two vtables (`01CB2508`, `00D497E0`), a
zero-initialised field run through `+0xE0`, sub-object ctors at `+0xE8` (`005DC2F0`),
`+0x310` (`00874320`), `+0x380` (`00874350`), `+0xD70` (`005CC8A0` then `005CD0A0`),
`+0xDA0` (`005DBF80`), `+0xDC8` (`006331A0`) and `+0xE00` (`00792DD0`), a refcounted
singleton install at `+0x10C8` via `001C26B0(01CB2BA0)`/`00584730`, the
`+0xDB0 = 0x400000` / `+0xDB4 = 0x100000` defaults, and finally eight guarded
`[rip]+8` vtable calls on registered sub-objects (each skipped when its flag byte is set).

| member | size | role | interior |
|---|---:|---|---|
| `005DBF50` | 15 B | clears a 0x14-byte struct (`+0`/`+8`/`+0x10`) — the `00874350` `+0x18` child | `005DBF52` |
| `005DBFB0` | 12 B | clears a 0x10-byte struct (`+0`/`+8`) — the `00874350` `+8` child | `005DBFB2` |
| `005DC2F0` | 267 B | the `+0xE8` sub-object ctor: vtable `00D49930`, a 0xA8-byte field zero-run, `00874D60(+0x130)`, then `00808FE4(+0x140, 8, 0x18, 005DC1B0)` — an 8-entry container init with a callback | `005DC386` |
| `006331A0` | 20 B | intrusive-list head init: `+0`/`+8` self-links, `+0x10`/`+0x18` zeroed — the `+0xDC8` child | `006331A2` |
| `00874320` | 37 B | zeroes seven qword pairs (0x70 bytes) — the `+0x310` child | `00874330` |
| `00874350` | 308 B | the `+0x380` sub-object ctor: two head structs (`005DBFB0(+8)`, `005DBF50(+0x18)`), then five `0x1D8`-stride children at `+0x30`/`+0x208`/`+0x3E0`/`+0x5B8`/`+0x790`, each `006160B0(child)` + `00615C90(child+0x188, child)`, and a `+0x968`–`+0x988` tail zero-run | `008743A0` |

`005CC8A0`, `005CD0A0`, `005DBF80`, `00792DD0`, `00874D60`, `00808FE4`, `006160B0`,
`00615C90`, `001C26B0` and `00584730` are shared callees with other callers — deliberately
not census members.

## `AU-4` narrowed — the region is THREE BLOCKS at stride `0x420`, each with its own publisher (OPUS, 2026-09-16)

`AU-4` asks what writes and uses the 2,872 bytes of `01F80130`–`01F80C68` when *"3 profiles account
for only 1,044"*. **Nothing is missing: 1,044 is one block, and there are three of them.**

Every RIP-relative operand and every image-base access in `.text` landing inside the region, taken
from the whole image and attributed through the function list, falls into three clusters:

| block | initialiser | consumers |
|---|---|---|
| `01F80130` | `FUN_0015BD30` (484 B) | `FUN_00196290`, `InputManager_RestoreDefaultBindingProfiles` |
| `01F80550` | `FUN_0015C0D0` (420 B) | `FUN_00196DF0`, `InputManager_PollAndBuildControlState` |
| `01F80970` | `FUN_0015BF20` (420 B) | `FUN_00196C40`, `FUN_00196EE0`, `InputManager_PollAndBuildControlState`, `FUN_00197870` |

The three initialisers are **siblings** — two are byte-for-byte the same length and the third is 64
bytes longer — and each opens with the same `movaps` run writing `+0x00`, `+0x10`, `+0x20`, `+0x30`,
`+0x40` of its own block. The spacing is `0x420` twice over: `0x550 − 0x130 = 0x420` and
`0x970 − 0x550 = 0x420`.

**`0x15C` reappears INSIDE each block, which is what ties this to `AU-2`.** Collecting the distinct
target addresses per block and expressing them as block-relative offsets:

```
01F80130   +0x0 +0x10 +0x20 +0x30 +0x34 +0x38 +0x40 +0x15C +0x190 +0x194 +0x19C +0x2B8 +0x2EC +0x2F0
01F80550   +0x0 +0x10 +0x20 +0x30 +0x40 +0x15C
01F80970   +0x0 +0x10 +0x20 +0x30 +0x40 +0x15C
```

`+0x0`, `+0x15C` and `+0x2B8` are `0x15C × {0, 1, 2}`. So the profile stride `AU-2` measured is the
stride WITHIN a block, and `3 × 0x15C = 0x414`, which is `0x420` less twelve bytes of padding. The
first block shows all three sub-profiles because its publisher touches all three; the other two show
the first two, because theirs do not reach further.

**What this does not settle.** The three blocks at `0x420` would span `0xC60` from `01F80130`, and the
region as `AU-4` states it ends at `01F80C68`, which is `0xB38` — so the third block has `0x2F8` (760)
bytes, room for two sub-profiles and not three. Either the region's end is approximate or the last
block is genuinely short, and **no reference observed here distinguishes those**: references show what
is touched, never what is reserved. The count of sub-profiles in blocks 2 and 3 is therefore still
open, and `AU-4` is narrowed rather than closed.

**Instrument.** `Database/Tools/analysis-kit/gfz-scripts/range_refs.py` — every RIP-relative operand and every
image-base access whose target lands in a VA range, attributed to its containing function. It is the
same sweep `disp_image_census.py` uses, filtered by target rather than by displacement, so the same
limits apply: an address formed at run time, or reached through a pointer loaded from data, is
invisible to it.


## The slot/bit correspondence, confirmed against the instructions (FABLE, 2026-09-16)

**THE CORRESPONDENCE IS STRUCTURAL, NOT EXTRAPOLATED - 2026-09-16 (FABLE).** The caution was that slot *n* maps to bit *n* is *only shown for bits 13/14*, so bit 10 being `L1` is a lead. **It is shown for every slot in the range, by the loop that builds the mask.** **Read from the body of `InputManager_TranslateBindingProfileToControlState` `00197160`.** At `0019721D`–`0019724D`: `ebx` is the loop counter, incremented at `00197244` and bounded by `cmp ebx, 0x10` / `jb 001971B0`. Inside, `edx = ebx AND 7` and `eax = ebx >> 3` (with the signed-correction branch `lea eax, [rbx + 7]` / `sub edx, 8` that a compiler emits for a signed divide by 8), then `movzx eax, byte ptr [rcx + r14]`, **`btr eax, edx`**, and the byte is stored back. **That is exactly `mask[i >> 3] &= ~(1 << (i AND 7))` for `i = 0..15`, with no special cases** - the pseudocode this page already carries, now confirmed against the instructions. **So the mapping is produced by a uniform loop over the slot index**, and bit 10 corresponds to slot 10 for the same reason bits 13 and 14 correspond to slots 13 and 14. **The 13/14 evidence was never the general case; it was two instances of it.** **One site sits outside the loop and uses the same arithmetic**: `00197322`–`00197342` applies `AND 7` / `>> 3` / `btr` to the computed index `rsi + 4` rather than to a loop counter. Same rule, one special-cased slot. *The bound, and it matters.* **The loop stops at `0x10`, so this establishes the correspondence for slots 0–15 only** - not for all 28 binding slots the format defines. **Bit 10 is inside that range, so the row's lead is now a finding**; anything about slots 16 and above is not covered by this loop and I did not look for where those are built.

## SWE2-EC7-42 update (2026-09-19) - `00792DD0`

`00792DD0` (317 B) is a binding-profile body - `00874D60` pair. Interior anchor `00792E0E` (an `00874D60` call).

## SWE2-EC7-48 update (2026-09-19) - `0035F690`

`0035F690` (205 B) is `InputControl_AdvanceChannelTimingState` - call-free per-channel hold timers: `+0x9` bit `0x10` gate, `+0x12` counter, thresholds `0x6E0`/`0x6FE`, `0xFDDE` ramp into `+0x18`, `+0x14` clamp `0xB4`. Interior anchor `0035F69F` (the `+0x12` increment).


## SWE2-EC7-64 update (2026-09-19) - `001E0C50`

`001E0C50` (138 B) is the `+0xEC` capture-flag reader - `00197980`/`00198790`/`00796E20`/`0079AE40`/`0079AEE0`. Interior anchor `001E0C60` (a `00198790` call).


## SWE2-EC7-80 update (2026-09-20) - `005841B0` four-arm command map measured

`005841B0` (85 B) is the id->command translator the binding callers
run: `edx` 1..4 maps to `0x1B`/`0x1C`/`0x1D`/`0x1E`, each tail-jumping
`00583FD0(cmd, rdx = original rcx, 0)`; any other `edx` returns
without a call - a four-entry dispatch feeding the shared message
sender.
Interior anchor `005841C4` (the `0x1E` arm).

## SWE2-EC7-81 update (2026-09-20) - `00583FD0` command-table dispatcher measured

`00583FD0` (473 B) is the sender `005841B0` tail-jumps into:
`003936B0()` fetches the id, `(eax + 0x3FF) >> 10` derives `esi`,
`ebx` clamps the `00D23DA0` descriptor index to 0x1F, and
`002F9860` pulls two strings (`0x49A` vs `0x49C` on the flag). The
descriptor's `+4` byte (1..4) picks the `002B4090` 0x200-buffer
write arm; `+5` bit4 skips `00249C60`; `+5` bit0 arms the
`00861EC0` stack fill and the `003948B0` commit with `+5` bit1
folding the flag word (`0x2020001`/`0x20200D1` + `bts 0xC`) and
`+5` bit5 setting `| 5`; otherwise `00394A90`/`003949B0` commit by
`r14d`. `+5` bit3 ends with `002470C0` on the result.
Interior anchor `00583FF9` (the `003936B0` call).

## SWE2-EC7-110 update (2026-09-20) - `001DFA70` measured

`001DFA70` (8 B) is the
empty-predicate `00195DF0`
and `00198B60` run against a
binding/control record:
`dword[rcx + 0x64] == 0`
answers sete-true - the
single-field occupancy check
the profile lookup uses before
taking the populated path.
Interior anchor `001DFA74`
(the `sete al` answer).

## SWE2-EC7-111 update (2026-09-20) - `00196A50` measured

`00196A50` (110 B) is the
2-byte-element aligned
deallocate `00195290`,
`00195820`, `00198000` and
`00866200` run - the wide-char
twin of `001A5A80`:
`r8 * 2 >= 0x1000` selects the
aligned path, `rdx & 0x1F`,
the `qword[rdx - 8]` block
base, and the `8..0x27` delta
window all validate before the
`00210EB0` tail; each failure
dies on the `008C2DA8` fault
IAT.
Interior anchor `00196A82`
(the `[rdx - 8]` block-base
recovery).

`00196140` (325 B) is the
wide-string resize/assign
`00198000` and `00866200`
run: an argument pointer
landing inside
`[buffer, buffer + size * 2)`
detects self-assignment, folds
to an element offset
(`(rsi - buffer) >> 1`), and
tails `00196000` - the
insert-from-self path. Else
`rdi` is the target length:
`> 0x7FFF...FE` throws
`"string too long"` through
`008C2618`, `qword[+0x18] <
rdi` grows through `00195820`,
`00861EBA` copies `rdi * 2`
bytes, `[+0x10] = rdi`, and
`word[buffer + rdi * 2]` gets
the terminator.
Interior anchor `001961EB`
(the `00195820` grow call).

## SWE2-EC7-113 update (2026-09-21) - `008628F0` measured

`008628F0` (20 B) is the
byte-pair unpack `0035F590`
runs: the fifth stack
argument is a pointer whose
`byte[+0]` and `byte[+1]`
load into `r8d` and `edx`,
`ecx` takes the incoming
`edx`, and the tail jumps
`001E1120` - a two-byte
record decoded into
registers for the real body.
Interior anchor `008628F7`
(the `byte[+0]` read).

## SWE2-EC7-114 update (2026-09-21) - `007A0B50` measured

`007A0B50` (265 B) is the
seven-table byte copy
`00196680` runs: for each
live pointer at `+0x118`
through `+0x148` (stride 8),
an index `edx - 0x1C` below
`0x100` copies
`byte[base + i + 0x130]` to
`byte[base + i + 0x30]` -
defaults pushed into live
slots across seven parallel
`0x100`-row banks, each
guarded independently.
Interior anchor `007A0B75`
(the first `+0x30` store).

## SWE2-EC7-115 update (2026-09-21) - `007999E0` measured

`007999E0` (158 B) is the
one-shot `00196FF0` runs:
when `byte[02EA5363]` is
set it clears the flag and
calls `vtable[+0x20]` on
`[02EA5370]` with
`r8 = 00798A40` and a stack
arg of 1 - a negative
answer returns 9; the clear
path walks the `01F401E8`
list invoking `vtable[+0x28]`
on every node.
Interior anchor `00799A12`
(the `vtable[+0x20]` call).

`001E0650` (544 B) is the call-free code map `001E1050` (and `001E0AA0`) call: `ecx-2` bounds 0..0x1E into a `00120C70`-relative jump table at `+0xC0870`, each arm returns `eax = (dl << 16) | r8b` with dl the active flag and r8b the slot id 2..7 (or 0) - the profile's code-to-binding lookup.

Interior anchor `001E0767` (function `001E0650`).

`001EBDD0` (448 B) is the profile record builder `001EC060` calls: `001EB4B0` constructs a record from `rcx+0x214` against `01DFE0A0`/`01F82E28`, xmm constant blocks `008C5F80`/`008C5F90` load, `[rdi+0x22C]` carries a float into the stack frame, and `00182EE0`/`00185100` finish - the binding profile's record fill.

Interior anchor `001EBE2D` (function `001EBDD0`).

`00182EE0` (39 B) is the resolve-or-empty shim `001EBDD0`/`001B76E0`/`002DD910` (and two uncited callers) share: `001DDAB0` resolves the global twice - the first result gates, the second is tail-passed to `001DD120` - and a null returns an `xorps`-zeroed struct - the profile path's presence check.

Interior anchor `00182EE4` (function `00182EE0`).

`00196000` (306 B) is the wide-string append `00196140` calls: MSVC `std::wstring` bounds - `[rdx+0x10] < r8` throws 'invalid string position', capacity past `0x7FFFFFFFFFFFFFFE` throws 'string too long'; the `rbx==rsi` self arm writes the new `+0x10` count, picks heap vs SSO on `+0x18 >= 8`, null-terminates the wide slot and commits through `00196B90` - the profile's name-buffer append.

Interior anchor `0019607D` (function `00196000`).

`001EB3D0` (216 B) is the 3x3-times-vec3 transform `001EC060` runs: `rcx`'s three `0x10` rows are the matrix, `r8` the vector - each output lane is the row's dot product built from `shufps 0x55`/`0xAA` broadcasts and `mulss`/`addss`, stored to `rdx+0`/`+4`/`+8` - the stick/basis rotation the binding layer applies to raw input

Interior anchor `001EB42A` (function `001EB3D0`).

`002EF100` (174 B) is the three-arm slot emit `001EC060` runs per remapped control: `edi` gains bit `0x2000`, `003EC580(bx)` resolves and `004230A0(rec, edi)` gates; then when `bx != -1` the `022C6F28 + bx*0x740` row is armed three times over `+0x284` - `00427320(rec, edi)`, `00427860(rec)`, `004272A0(rec, 1)`

Interior anchor `002EF15D` (function `002EF100`).

`00196B90` (171 B) is `wstring::erase(pos, len)` the profile-name path runs: `[rcx+0x10]` bounds-checks `rdx` with the `invalid string position` throw on violation, a full-range or zero-length erase just truncates at `rdx`, otherwise `memmove` (IAT `008C2A40`) slides the tail over `r9` chars, `[rcx+0x10]` shortens, and the SSO buffer (`+0x18 >= 8` selects the heap pointer) gets its NUL word

Interior anchor `00196C0E` (function `00196B90`).
