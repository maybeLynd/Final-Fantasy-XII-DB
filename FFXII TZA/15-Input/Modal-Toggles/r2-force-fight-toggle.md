---
system: The R2 modal toggle and its force-fight output
category: 15-Input
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS): what the FLEEING state changes for enemy units (SD-1) answered 2026-09-30 (combos, engagement, the AI distance threshold and movement divisors); the label widget draws the word FLEEING letter by letter (SD-2) answered 2026-09-30; the FLEEING label's driver and same-frame ordering (FM-1) answered 2026-09-25; the sound at bank-local 0x52 (UQ-149) answered 2026-09-18 (slot 82 of se000.seb); the refusal predicates (UQ-150), the two feature-enable bytes (AN-1) and the third override DAT_020927CC (UQ-151) answered 2026-09-17
owner_layer: PrimaryOwner:Input (the arbiter and its private state) — output consumed by Combat, Movement and UI
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
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# The R2 modal toggle and its force-fight output

> One button flips one bit, once per press. That bit's only job is to drive **force fight mode** —
> and the area you are standing in can pin it.

**PARTIAL, deliberately.** The input, the latch, the pin, the polarity and the output are all read
at tier 1. **What the mode looks like on screen is not established**, and this document says so
rather than attaching a plausible label — see §7. It was written from
[the field record table](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md)
§11, which found this consumer while dispositioning a crossref finding.

## 1. What the player sees

A button that changes how the party behaves, and that stops working in towns.

Press it and a mode turns on; press it again and it turns off — one flip per press, however long
you hold the button. Walk into a town, a shop, an aerodrome or one of the game's story rooms and
the mode is quietly pinned: whatever you had chosen outside is reset, and pressing the button
there does not change it back. Step out into the field and the button works again.

The mode itself is the engine's **force fight mode** — the same state a cutscene script raises with
its own verb when a fight is not optional in the ordinary way. ~~**What that looks like on screen is
documented elsewhere and is not fully known**~~ **On screen it is the `FLEEING` label** — observed
2026-09-10 in a fresh field ([`EXP-025`](../../_experiments/EXP-025-r2-visual-toggle.md)): the first
press puts `FLEEING` on the HUD and it stays after the key is released (toggle `1`, flag `0`); the
second press removes it (toggle `0`, flag `1`). So the button *clears* force fight mode and the game
calls that state fleeing; what fleeing does to enemies, routes or commands is **not** established
by that observation. *(Established since, 2026-09-30, OPUS, statically: [`SD-1`](../../_index/candidates/sd1-force-fight-enemy-consumers-0930/README.md).
With `FLEEING` on, every unit without Confuse or Berserk stops chaining combos, enemies included. A spawned unit's
status change clears its engaged state. Enemy AI order checks use the other distance threshold, and enemy movement
takes the other step divisors. The stance and the availability reason `0x24` change only for the party. And
[`SD-2`](../../_index/candidates/sd2-r2-label-element-0930/README.md): the label is drawn one letter at a time,
F-L-E-E-I-N-G, while the one-second arming counter runs.)* What is established here is that the player has a button on it, and that the
map decides whether the button is listened to. **And the label does not follow the press at once**:
the output lags the first press by about one second, for a reason §2g reads out of the bytes.

## 2. Native mechanism

### 2a. The input: group 0, slot 9 — R2

`FUN_0017DE10` (67 B, Input) is the whole test:

```c
int InputQuery_IsR2Held(void)
{
    obj = FUN_00796E20();  dev = *(void **)(obj + 0xDF8);
    mgr = InputManager_GetSingleton();
    code = GetBinding(mgr, /*profile*/ 0, /*group*/ 0, /*slot*/ 9);   /* 00197710 */
    return InputBackend_IsControlCode28To283ActiveForBank(dev, code, 0) != 0;
}
```

`00197710` is the binding read surface documented in
[the keymap format](../Binding-Profiles/keymap-ini-file-format-and-default-controls.md): group
selects one of three tables (`+0x00` sixteen buttons, `+0x40` eight axes, `+0x60` four PC extras)
at base `01F80F90`, stride `0x1C` dwords per profile. The name table at `01DF11E0` gives group 0's
sixteen slots in order, and **slot 9 is `R2`**:

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | **9** | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Select | L3 | R3 | Start | Up | Right | Down | Left | L2 | **R2** | L1 | R1 | Triangle | Circle | Cross | Square |

The name's index *is* the slot index — that is the keymap document's own finding, and it is what
makes this a lookup rather than an inference. `InputQuery_IsR2Held` returns a **level**, not an edge; the
edge is made in software, below.

### 2b. The latch: one flip per press

`InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`, 1,599 B) owns three globals, and
**owns them alone** — a full-image sweep for rip-relative references finds all four sites of
`DAT_01E0C2B4`, all five of `DAT_020927E0` and both of `DAT_020927E4` inside this one body:

```c
if (InputQuery_IsR2Held() == 0) {                          /* released */
    if ((DAT_02F97360 & 0x200) == 0) {             /* input-snapshot bit 9 clear */
        if (DAT_01E0C2B4 == 1 || FieldData_GetActiveFieldRecordBit15() != 0)
            DAT_020927E0 = 0;                      /* <- the area pins the toggle */
    } else if (FUN_00862CF0() != 1) {
        DAT_020927E0 = 1;  DAT_01E0C2B4 = 1;  goto emit;
    }
    if (DAT_01E0C2B4 != 0) goto emit;
    latch = 0;
} else {                                            /* held */
    DAT_01E0C2B4 = 0;
    if ((~DAT_020927E4 & 1) != 0)
        DAT_020927E0 = (DAT_020927E0 == 0);         /* the flip */
    latch = 1;
}
DAT_020927E4 = latch;
emit:
FUN_00252B60(DAT_020927E0, 0);
```

- `DAT_020927E0` — the toggle, `0` or `1`.
- `DAT_020927E4` — the edge latch. Set while the button is held, cleared when released, so the
  flip happens on the transition and **not** once per frame.
- `DAT_01E0C2B4` — a sticky override. While set, the release path pins the toggle to `0` and skips
  the normal emit.

### 2c. The pin: the field record

`FieldData_GetActiveFieldRecordBit15` is the per-area bit documented in
[the field record table](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md).
It is set on **193 of the game's 1,154 areas — the towns, villages, shop interiors, plazas,
aerodromes, airship interiors and story rooms**. In any of them the release path forces the toggle
to `0` every frame the button is not held, so a press flips it and the very next release resets it.

That is the direct route. There is also an indirect one, and it lands on the same behaviour: the
same bit drives **capability policy row 2, bit 10**
([capability policy](../Gameplay-Capability-Policy/capability-inhibition-policy.md) §2), and the
applier below forces the toggle off when that bit is set. **Two independent paths, one outcome** —
which is why the pin is not defeated by holding the button.

### 2d. The applier and the policy gates

`FUN_00252B60(state, flag)` (280 B) re-decides the state against the aggregate capability mask
before passing it on:

```c
policy = FUN_002E0FA0();                       /* the 16x32 aggregate */
if ((_DAT_02F97362 & 0x200) != 0) return;      /* input snapshot high word: refuse entirely */
if ((policy & 0x40) == 0) {                    /* policy bit 6 clear */
    if ((policy & 0x200) != 0) { state = 0; flag = 1; FUN_00366950(); goto apply; }   /* bit 9 */
    if (((policy >> 10 & 1) == 0) && (FUN_00237260() == 0)) goto apply;               /* bit 10 */
}
state = 0;  flag = 1;                          /* every other case: forced off */
apply:
if (DAT_020927CC == 1) { state = 0; flag = 1; }
/* ... register transitions on DAT_022C83EC bits 2-3 ... */
if (FUN_003603B0() == 0 && FUN_003603C0() == 0) {
    if (state == 0) FUN_003667E0();            /* release the repeating sound */
    else            FUN_00366870();            /* acquire bank-local sound index 0x52, advance counter */
}
FUN_00252C80(state, flag);
```

So the toggle is overridden by **capability policy bits 6, 9 and 10** — and bit 10 is the
field-record contribution again.

> **CORRECTED 2026-09-11 (FABLE, for ASTRA-REQ-FABLE-R2-HELD-LAG).** The pseudo-code above elided
> two substitutions that sit between the policy gates and the write, and one of them is why the
> output lags the toggle. Read from `00252BC4`–`00252C63`:
>
> - **the mode register branch** — when `022C83EC` has bits 2–3 set, `state` is *replaced* by input
>   snapshot bit 9 (`02F97360`, unless policy bit 10), bit 2 is shifted into bit 3 and both are
>   cleared when that state is 0 (`00252BC4`–`00252C0C`); when bit 0 is set, `state` = register
>   bit 1 (`00252C13`–`00252C25`). EXP-025 sampled the register at 0, so neither ran there.
> - **the repeating-sound substitution** — after the acquire / release, `if (state != 0) state =
>   003669F0()` (`00252C54`–`00252C5D`): the state handed to `00252C80` is **bit 2 of the sound
>   state word `022CBE1A`**, not the toggle. §2g.

### 2e. The output: force fight mode, with the polarity written out

`FUN_00252C80` (134 B) is the **second writer** of the force-fight flag `01E0C2B8` — the one
[the force fight mode document](../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md)
records as unread (its open questions **AN-2** and **AN-5**). Its complete body:

```c
u32 old = *(u32 *)0x01E0C2B8;
u32 next = 0;
if (flag == 0 && (FUN_003603B0() != 0 || FUN_003603C0() != 0))
    return 0;                                   /* refuse: no write at all */
if (state == 0) {
    if (old != 0 && flag == 0) return 0;         /* already set, not forced: no write */
    *(u32 *)0x01E0C2B8 = 1;                      /* transient */
    next = (FUN_003BA2E0() != 0);                /* the feature enable decides */
} else if (old == 0 && flag == 0) {
    return 0;                                    /* already clear, not forced: no write */
}
*(u32 *)0x01E0C2B8 = next;
return 1;
```

**The first argument is inverted with respect to the flag.** `state == 0` *sets* force fight mode
(subject to the enable); `state != 0` *clears* it. Read the toggle accordingly:

| `DAT_020927E0` | meaning | `01E0C2B8` becomes |
|---:|---|---|
| `0` | the pinned / default value, and what a town forces | `FUN_003BA2E0() ? 1 : 0` |
| `1` | what a press in the field produces | `0` |

So the button's job in the field is to **clear** force fight mode, and the area pin restores the
engine's default. Anyone reading `state` as "the mode is on" has it exactly backwards — the same
warning the force-fight document gives about its own predicate, one level up.

### 2g. Why the output lags the first press by one second — the arming counter

While the toggle is `1`, every frame's `00252B60` calls `00366870` (the acquire) and then replaces
`state` with `003669F0()` = bit 2 of `022CBE1A`. The acquire (`00366870`, read to its ret) is a
small state machine on that word, with a counter at `022CBE18` and a threshold at `022CBE08`:

| step | site | what |
|---|---|---|
| gate | `00366874`–`0036687B` | nothing while the mode register `022C83EC` has bit 0 |
| first frame | `0036688D`–`003668C2` | no handle yet (bit 4 clear): `003A1180(0x52)` resolves the bank-local index, `002DF220(id, 0x40, 0x7F)` starts the repeating sound, the handle goes to `022CBE1C`, bit 4 is set, the counter starts at 0 |
| every frame | `003668F0`–`003668FA` | `022CBE18 += 1` |
| the threshold | `00366902`–`0036691C` | when the counter reaches **`022CBE08`**, bit 2 (**engaged**) is set — bit 3 as well on the first crossing — and the counter is clamped there |
| always | `0036691C`–`00366928` | bit 6 cleared, bit 0 (**on**) set |

`022CBE08` is written once, at `003670B7` in the sound object's initialiser `00366B80`: **`30 ×
[01DFE0B4]`** — thirty times [the time-base word](../../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md)
(`1` at 30 fps, `2` at 60), i.e. **one second of frames**. Until the counter gets there, bit 2 is
clear, so `00252C80(0, 0)` is called — and with the flag already `1` and `forced == 0` that is the
"already set, not forced: **no write**" exit (`00252CC8`–`00252CCE`). The flag therefore keeps its old value
for one second after the first press and flips to `0` on the frame the counter reaches the
threshold: EXP-025's 94 samples of `(toggle 1, latch 1, sticky 0, flag 1)` over 0.97 s, then
`(1, 1, 0, 0)`. The release (`003667E0`) clears bits 0, 2, 3, 5, 6 and stops the handle at once, so
the second press — `state = 0` — writes `1` on its first frame, exactly as observed. The toggle
stays `1` after the key is released, so the acquire keeps running and bit 2 stays set: the lag is
a **one-time arming delay per activation**, not a hold requirement.

**Live 2026-09-11 ([`EXP-028`](../../_experiments/EXP-028-r2-arming-control.md), sampled, non-atomic
reads).** A 0.15-second press in a fresh field: the counter read 1 at the first activation sample,
9 at the last held sample, **13 at the first released sample and kept climbing after release**; at
game frame 1499 it read 59 with the word `0x11` (bits 0 and 4: on, handle held) and the flag `1`;
at frame 1500 it read **60 = the threshold** with the word `0x15` (bit 2 engaged) and the flag `0`,
about 10.7 ms apart; `022CBE08` read 60 and `01DFE0B4` read 2 throughout; `FLEEING` was on screen
after release. A second short press left the word `0x02` (the release path's bit 1), the flag `1`,
the counter at 60 and the handle at 9 — the release clears bits, not the counter. That is the
progression §2g predicts, at sample precision; instruction ordering inside the frame and the
label's driver remain unmeasured (`FM-1`).

The word's other clients: `00366960(n)` sets the engaged state directly (counter = threshold, word
= `0x25`) or resets the counter; `00366940` resets the counter; `003667B0(n)` sets or clears bit 7;
`003669D0` (UI) returns `0` / `1` / `2` for off / arming / engaged and has seven readers
(`00253C70`, `00273950`, `0028E5F0`, `002C64C0`, `0035D660`, `003C87B0`, `003C8B70`) — the
`FLEEING` label's driver ~~is among them or behind the flag, not read here~~ (**FM-1**).
*(Corrected 2026-09-30, SWE2-DATA: FM-1 was answered on 2026-09-25 in §7 — the label is a widget of its own,
`00366B80`, that reads the state word through a pointer it was built with; it is neither one of these readers nor
the flag.)*

### 2f. AN-5 answered: the "gameplay on, UI off" state is not reachable here either

`FUN_003BA2E0` is a feature enable: two adjacent byte globals `02B4053C` / `02B4053D`, both
required non-zero. The force-fight document asks whether the flag can be `1` while that enable is
false — a state in which gameplay would act on force fight mode while the UI reported it off — and
notes the setter cannot produce it but this writer "is not so constrained."

**It is constrained.** The final store is `enable ? 1 : 0`, exactly like the setter's. The only
window in which the flag is `1` with the enable false is *inside the call to `FUN_003BA2E0`
itself*, between the transient store and the final one — and that function reads only its own two
bytes, never the flag. **No consumer on this thread can observe it.** Cross-thread observability is
not established statically and is left open in §7.

The two enable bytes are written by `FUN_003BA300` and `FUN_003BA310`, called from
`FUN_00266D10` (a field/area initialisation routine that sets **both**), `FUN_002628B0`
(ActorEntity) and `FUN_0050C910` (Script VM native bridge, which pops one int and writes one of
them). So the enable is configured per area and by script — not a compile-time dev switch.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00253C70` | `InputGameplay_ArbitrateDigitalInputAndModalState` | 1,599 B | owns the toggle, the latch and the sticky override *(ledger name)* |
| `0017DE10` | `InputQuery_IsR2Held` | 67 B | reads binding group 0 slot 9 and asks the device |
| `00197710` | `GetBinding` | 99 B | the binding read surface, three group tables |
| `00198790` | `InputManager_GetSingleton` | 8 B | supplies the manager pointer *(ledger name)* |
| `0079E6A0` | `InputBackend_IsControlCode28To283ActiveForBank` | 44 B | level, not edge *(ledger name)* |
| `00252B60` | `ForceFightToggle_ApplyWithCapabilityGates` | 280 B | re-decides against the policy mask |
| `00252C80` | `ForceFightMode_SecondWriter` | 134 B | **closes AN-2** — sets/clears `01E0C2B8` |
| `003BA2E0` | force-fight feature enable | 27 B | two bytes, both required |
| `003BA300` / `003BA310` | enable-byte setters | 7 B each | one byte each |
| `00253B90` | `flag == 0` predicate | 12 B | the raw reader, 15 consumers |
| `003603B0` / `003603C0` | two refusal predicates | 8 B each | read `022CB728` / `022CB726` |
| `00237260` | policy-side predicate | 126 B | ORs with policy bit 10 |
| `002E0FA0` | aggregate capability reader | 126 B | OR-reduce 16 rows |
| `00377C20` | `FieldData_GetActiveFieldRecordBit15` | 78 B | the area pin *(ledger name)* |
| `00366870` / `003667E0` | repeating-sound acquire / release | 196 / 135 B | driven by the toggle state |
| `0035C6F0` / `0035C880` | mode-register read / masked write | 7 / 17 B | `022C83EC` |
| `0035BC50` | battle-menu list build | 1,014 B | runs only when register bit 0 is clear |
| `00266D10` | field/area initialisation | 1,185 B | sets both enable bytes |
| `0050C910` | script-side enable setter | 23 B | pops one int, writes `02B4053C` |
| `003669F0` | engaged query | 14 B | bit 2 of `022CBE1A` — **what `00252B60` really passes as `state`** |
| `00366B80` | sound object initialiser | 1,420 B | writes the threshold `022CBE08 = 30 × [01DFE0B4]` at `003670B7` |
| `00366960` / `00366940` / `003667B0` | engaged setter / counter reset / bit 7 | 43 / 12 / 42 B | the word's other writers |
| `003669D0` | off / arming / engaged (UI) | 27 B | `0` / `1` / `2` from bits 0 and 2; seven readers |

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `020927E0` | the toggle | `.data` u32 | `0` or `1`; five accesses, all in `00253C70` |
| `020927E4` | the edge latch | `.data` u8 | set while held, cleared on release |
| `01E0C2B4` | sticky override | `.data` u32 | while set, the release path pins the toggle |
| `01E0C2B8` | the force-fight flag | `.data` u32 | the output; documented in 00-Engine-Core-Runtime |
| `02B4053C` / `02B4053D` | feature-enable bytes | `.data` u8 ×2 | both required non-zero |
| `02F97360` | input frame snapshot | `.data` u32 | bit 9 read here; high word at `02F97362` |
| `022C83EC` | UI mode register | `.data` u32 | bit 0 gates the battle-menu build; bits 2-3 written here |
| `01DF11E0` | binding name table | `.rdata` ptr[16]×3 | group 0 slot 9 = `R2` |
| `01F80F90` | binding profile array | `.data` | `0x1C` dwords per profile |
| `022CBE1A` | repeating-sound state word | `.data` u16 | bit 0 on, bit 2 engaged, bit 3 first crossing, bit 4 handle held, bit 6 / bit 7 flags |
| `022CBE18` | arming counter | `.data` u16 | frames since the acquire started; clamped at the threshold |
| `022CBE08` | arming threshold | `.data` u32 | `30 × [01DFE0B4]` — one second |
| `022CBE1C` | the repeating-sound handle | `.data` u32 | from `002DF220` |

## 4. Data structures and formulas

```
toggle  = DAT_020927E0        u32   0 or 1
latch   = DAT_020927E4        u8    1 while the button is held
sticky  = DAT_01E0C2B4        u32   pins the toggle to 0 while non-zero
flag    = DAT_01E0C2B8        u32   force fight mode (the output)
enable  = *(u8*)02B4053C && *(u8*)02B4053D
```

The complete decision, composed:

```c
/* per frame, in 00253C70 */
if (R2_held) { if (!latch) toggle = !toggle;  latch = 1;  sticky = 0; }
else         { if (sticky == 1 || FieldRecordBit15()) toggle = 0;  latch = 0; }

/* in 00252B60 */
state = toggle;
if ((policy & 0x40) || (policy & 0x200) || (policy & 0x400) || FUN_00237260() || DAT_020927CC == 1)
        state = 0, forced = 1;

/* in 00252B60, after the gates (§2g) */
if (state) { acquire(); state = engaged; }         /* engaged = bit 2 of 022CBE1A */
else       { release(); }                          /* clears the word, stops the handle */
/* acquire: counter 022CBE18 += 1 per frame; engaged when counter >= 022CBE08 = 30 * [01DFE0B4] */

/* in 00252C80 */
flag = (state == 0) ? (enable ? 1 : 0) : 0;      /* note the inversion; no write when unchanged and not forced */
```

Reproduced by hand: in a bit-15 area with the button untouched, `toggle = 0`, `state = 0`, so
`flag = enable`. In an ordinary area after one press, `toggle = 1`, `state = 1`, so `flag = 0`.

## 5. Call chain

```
per-frame input arbitration
  -> 00253C70  InputGameplay_ArbitrateDigitalInputAndModalState        [OWNER of the toggle]
     -> 0017DE10 -> 00197710 GetBinding(profile 0, group 0, slot 9 = R2)
     -> 00377C20 FieldData_GetActiveFieldRecordBit15   (twice: direct, and via thunk 00313F60)
     -> 00252B60
        -> 002E0FA0 aggregate capability policy  (bits 6, 9, 10)
        -> 0035C880 / 0035C6F0  mode register 022C83EC bits 2-3
        -> 00366870 | 003667E0  repeating sound, bank-local index 0x52
        -> 00252C80 -> 01E0C2B8               [DECISION SETTLES, not a subsystem transition]
                       -> 003BA2E0 feature enable
```

**Upstream:** the player's R2 binding; the active field's record bit 15; the capability policy.

**Downstream:** everything that reads `01E0C2B8` — 15 consumers through `00253B90` and its thunk,
predominantly Movement (`BattleLocomotion_ComputeStepDistance` alone accounts for three) plus
combat action availability and party stance; and two UI readers through the effective-value reader
`00253BA0`.

**Do not confuse with:**

- **`setforcefightmode`, the script verb** (call id `0x0334`, handler `003444D0` → setter
  `00254EA0`). That is the *other* writer of the same flag. A script raising the mode and the
  player's button clearing it are two authorities over one dword; nothing arbitrates between them
  beyond last-writer-wins.
- **The `WalkMode` binding** (group 2 slot 3). A different, PC-only binding in a different group.
- **`state` and the flag.** They are inverted with respect to each other — §2e.
- **The two refusal predicates.** `003603B0`/`003603C0` suppress the write entirely; they are not
  the toggle.

## 6. Modding notes

- **Best intervention point:** `DAT_020927E0` is only ever written by `00253C70`; the flag
  `01E0C2B8` has four write sites in two functions. To change what the button does, change
  `00252C80`'s inversion, not the toggle.
- **Rebinding is authored, not code.** The button is whatever `keymap.ini` maps to group 0 slot 9;
  the code reads slot 9, never a key code.
- **The area pin is map data.** To let the mode survive in a town, clear bit 15 in that field's
  `navimapdata.bin` record — but that bit also waives the KO/Stone/Vanished action gate and drives
  capability bit 10, so it is not a free switch. See the field record document's §6.
- **The feature enable is per-area and script-writable.** If `02B4053C`/`02B4053D` are not both
  non-zero the button can only ever clear the flag, never set it.
- **XIIOnline:** `01E0C2B8` is one dword of authoritative shared battle state with **two**
  authorities — a script and a local button press. A client whose player presses R2 diverges from
  one whose player does not, with no script event to replay. Synchronise the flag, not the button.

## 7. What is not known

- [x] **What the mode looks like on screen.** *(Residue moved 2026-09-30 to the next box.)* ~~The output is force fight mode, whose consumers are
      documented, but no player-facing description of the R2 press has been established from the
      binary or authored data. Deliberately unnamed.~~ **Narrowed 2026-09-11:** the visible identity
      is the HUD's **`FLEEING`** label, present with flag `0` and absent with flag `1`
      ([`EXP-025`](../../_experiments/EXP-025-r2-visual-toggle.md), one field, stationary). Still
      open: ~~what the label's driver reads (`003669D0` or the flag) and~~ what fleeing changes in
      enemy behaviour — no renaming of the flag follows from one label. **PROPOSED-repos2d-7.**
      *(2026-09-30, SWE2-DATA: the driver half is answered below (FM-1, 2026-09-25). What is left is
      registered in the next box: which of the force-fight flag's consumers act on enemy units. The consumers the
      [force-fight page](../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md) reads gate party
      behaviour — the availability cascade's kind-0 test and the combo gate (AN-4); whether any of them, or the
      engagement and distance-threshold consumers, changes an enemy unit is not read.)*
- [x] **SD-1.** Which of the force-fight flag's consumers act on enemy units, and so what the `FLEEING` state changes
      for enemies. *(Registered 2026-09-30, SWE2-DATA; static; supersedes PROPOSED-repos2d-7.)* *(SD-1 answered 2026-09-30 by OPUS `473de1075`, [record](../../_index/candidates/sd1-force-fight-enemy-consumers-0930/README.md).)*
- [x] **What drives the `FLEEING` label**, ~~and the live check of the arming delay — sample
      `022CBE1A` (bits 0 / 2), `022CBE18`, `022CBE08` and `01DFE0B4` through one press: the flag
      should flip on the frame the counter reaches the threshold~~ (the live check is done:
      [`EXP-028`](../../_experiments/EXP-028-r2-arming-control.md) saw the counter cross 59 → 60 with
      the engaged bit and the flag flipping in the same bracket, §2g). Still open: the label's
      ~~driver (`003669D0`'s seven readers or the flag) and same-frame ordering.~~ **FM-1.**
      **Driver answered 2026-09-25 (FABLE, Claude Opus 5.5): neither. The label is a widget of its own that reads the
      toggle state word through a pointer it was built with.** Static; the bodies were read.
      - **The widget.** `00366740` builds a `0xE0`-byte widget with procedure `00366B80`, passes it the address of
        the toggle block `022CBE18` as its argument, and publishes it at `022CBE20` (`0036675F`–`0036678D`). Its one
        caller is the field-time UI rebuild `00253A30` (`00253A57`), so the widget is rebuilt with each area's UI.
      - **Its construction.** The construct arm stores that pointer at `+0xC8` (`0036709A`). It also writes the
        arming threshold `022CBE08` = 30 × `[01DFE0B4]` and the fade step divisors `022CBE0C` / `022CBE14`
        (`003670A6`–`003670D6`); the threshold is the one §2g measured. It looks up its layout sheet by name,
        `battle_4_c`, through the engine's by-name layout lookup (`003670C6`–`003670E1`).
      - **What it reads.** The tick reads the state word `022CBE1A` as `[+0xC8] + 2`. A visibility level `+0xD0`
        rises one step per frame while bit 0 is set and falls while bit 1 is set, and `+0xD8` is zeroed while bit 2
        (engaged) is clear (`00366FA6`–`0036703F`). The draw arm runs while either is non-zero (`00366BD0`,
        `00366BDE`).
      - **What it does not read.** The force-fight flag `01E0C2B8` has only two ~~readers~~ consumer readers, both under the battle frame (UQ-152 below); its writer `00252C80` also reads the old value at `00252C94` (narrowed 2026-10-01, OPUS, on SWE2-AUDIT-SPEC's review [`auditspec-review-sd1-0930`](../../_index/candidates/auditspec-review-sd1-0930/REVIEW.md))
        (UQ-152 below). Of `003669D0`'s readers, the three read here only gate or set UI mode bits (`0028E5F0` stores bit 1 of `022C83EC` through
        `0035C880`; `00273950` and `002C64C0` gate on it); none of them builds or draws the label.
      - **Where the state word is touched.** A RIP census of `022CBE18`–`022CBE1B` finds only the toggle module
        `00366740`–`003669F0`; the widget's pointer is the one route out of it.

      ~~*So the label follows the toggle state directly, which is why EXP-025 saw it before the flag moved.*~~
      *Corrected the same day:* EXP-025's screenshots were taken after release and do not time the label against
      the flag. What the code predicts is that the label starts to fade in while arming, because bit 0 is set
      before bit 2, and that is before the flag moves. Neither experiment observed it.
      ~~**Still open:** same-frame ordering, meaning whether the widget's tick runs before or after the applier
      `00252B60` writes the flag in a given frame.~~

      **Same-frame ordering answered the same day (FABLE, Claude Opus 5.5): the applier writes first, and the label
      reads afterwards in the same field frame.** Static; the bodies were read.
      - **The applier's order.** The arming counter is called from inside the applier (`00252C43`), before the
        applier reads the engaged bit and writes the flag through `00252C80` (`00252C63`). So bit 2 and the flag
        change in one call.
      - **Where the applier runs.** The applier runs in the input arbiter (`00254258`). The world tick calls the
        arbiter once per tick, at sub-step 0 of field mode, through the thunk `002E0D90`; the order is on
        [the world-tick page](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md).
      - **Where the label reads.** The label widget registered on root `0208EA28`, and it reads the state in its
        message-2 arm (`00366EFB`). The only walk of that root is the UI walk. The field frame runs it after the
        world tick on a running frame, and in place of the world tick on a frame whose step is zero.

      So on any frame where the flag flips, the label already sees the new state word in that frame. What shows
      on screen still lags by the fade: one level step per frame, with the step divisor from `022CBE0C`.

      *The identification of the widget as the `FLEEING` sprite is static:* it is the only widget built on the
      toggle block, and its timing matches EXP-025 / EXP-028. No live capture tied the sprite to it.
      *(Registered 2026-09-30, SWE2-DATA, as **SD-2**, static: which element of the layout sheet `battle_4_c`
      the widget's draw arm selects, and whether that element's image is the `FLEEING` text. The sheet and the
      arm are both in the image and the archive, so no live capture is needed.)* *(SD-2 answered 2026-09-30 by
      OPUS `7573a1b87`, [record](../../_index/candidates/sd2-r2-label-element-0930/README.md): the widget binds
      record 12 of `mrppack_ys` unit 1, whose seven items are cells `0 1 2 2 5 6 7` of `battle_4_c`, the letters of
      `FLEEING`, revealed one by one as the arming counter rises.)*
- [x] **UQ-149.** *(answered 2026-09-18, at the end of this item)* What the sound at **bank-local index** `0x52` is — acquired by `00366870` while the toggle
      is `1`, released by `003667E0`. **Corrected 2026-09-03:** this said "sound id", which was
      wrong and understated the work. `003A1180` resolves a **bank-local index** to
      `bankSlot * 512 + index`, so identifying the sound needs the **runtime bank slot** as well as
      the `sead` bank data. Established by the falsification pass on
      [the audio boundary](../../18-Audio/Audio-Boundary/what-the-engine-calls-to-make-a-sound.md).
      **PROPOSED-repos2d-8.**
      ***NARROWED 2026-09-18 (FABLE): the bank is one of three, and only one of them has a sound at that index.** The current slot `02AEF3FC` has exactly two writers: the boot reset `003A13F0` stores -1 (`003A14BE`, `003A153D`), and the completion `003A1390` stores the handle `003A1650` returns for a just-loaded bank (`003A139F`..`003A13A4`) and marks its row ready (`003A13D8`). `003A1390` is reachable by one route, as the completion `003A13F0` attaches (`003A14E9`) to the three bank loads it submits at boot, kind 32 ids 0, 1 and 3 from `002ED8C0` (`003A14AD`, `003A152C`, `003A15AB`); no field or script bank load (`003A0F80`) passes through it, so from boot onward the current slot is the last of those three to complete, and never a field's bank. The kind-32 array on [the SE block page](../../18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md) names them: `se000.seb`, `se007.seb`, `se002.seb`, sizes 24,968, 1,852 and 4,716 in the archive and the size table. Read from the archive with the page's layout (`i32[128]` slot offsets at `+0x10`, -1 empty), slot 82 is filled only in `se000.seb` (block 0, 123 slots, chunk at `+0x4151`); `se007.seb` (4 slots) and `se002.seb` (28 slots) leave it empty. So the toggle's sound is SE id 82 (block 0, slot 82, the id rule `block << 9 + slot`) of `se000.seb` when block 0's completion was the last, and no sound at all when `se007` or `se002` completed last. What remains live is only that completion order; the three loads are submitted in the order 0, 1, 3. DATA from the archive; the setter and completion static.*
      ***CORRECTED AND ANSWERED 2026-09-18 (FABLE, later the same day): the bank is always `se000.seb`; the narrowing above misread the boot routine.** It said one completion, `003A1390`, is attached to all three boot loads, so the current slot would be whichever finished last. The boot routine `003A13F0` submits three kind-32 loads and gives **each its own completion**: SE id 0 (`se000.seb`, path-array entry 0) completes through `003A1390`, which stores the handle in `02AEF3FC` (`003A14E9`, `003A13A4`); SE id 1 (`se007.seb`, entry 1) through `003A1330` into `02AEF400` (`003A1568`, `003A1344`); SE id 2 (`se002.seb`, entry 3, the mapper `002ED8C0` sends 2 to 3) through `003A12D0` into `02AEF404` (`003A15E7`, `003A12E4`). Those three stores and the boot resets are the only rip-relative writes to the three handles, and each completion's only reference in the image is its `lea` in the boot routine (no direct call or jump reaches one), so no field or script bank load passes through them. The toggle's resolver reads `02AEF3FC`, so its bank is `se000.seb` regardless of completion order, and nothing is left to observe live: the sound is **slot 82 of `se000.seb`** (block 0, chunk at `+0x4151`), SE id 82. The archive reading above stands and now serves as a control - slot 82 is empty in the other two banks. The same correction answers UQ-243 on [the sound-request page](../../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md), whose census finds all 37 immediate indices in the image filled in `se000.seb`. Static plus archive data.*
- [x] ~~**UQ-150.** What `022CB728` / `022CB726` are — the two refusal predicates behind `003603B0` /~~
      `003603C0`. **PROPOSED-repos2d-9.**
      **Partly answered 2026-09-14 (FABLE).**
      **`022CB726` is the flag "a skip reset is in effect".** It belongs to a small block `022CB720`–`022CB72B` with the following references (RIP census):
      - **Boot reset.** `00360370` zeroes the block and writes `0x5A` at `+4`.
      - **Request bytes.** `003603D0` sets `+0xA`; it is reached through a 5-byte thunk in the script-verb range. `003603E0` sets `+0xB`; its callers are the UI request router's destination-`0xC` route, `00280140` and `00354EF0`.
      - **Per-frame check.** `00360120`, run by the field frame and mode 5, checks the block. While `+0` is 0 and either request byte is set, it runs `003601D0`, the screen-fade page's skip-family handler. That handler stops sound, resets the time scales and actor-manager flags, sets **`022CB726 = 1`** and clears the request bytes (`003602A4`–`003602B7`).
      - **Clear.** `00360110` resets `022CB726` to 0, and its one caller is `ActorManager_BindLoadedDefinitionPayload`, so the flag lasts until the next definition payload binds.
      - **Readers.** `003603C0` reads the flag for 15 functions (17 raw sites): the field frame, the field runtime pass, the area unload, the play entry `002DF220` (which refuses while it is set, `002DF23B`–`002DF244`), six more sound entries in `002DEF40`–`002DF560`, and five others.
      **`022CB728` is narrowed, not answered.** Its only RIP-relative writer is the boot zeroing (`0036037E`), so `003603B0` returns 0 unless something writes the word through a pointer into the block. Pointer writes were not excluded.
      ***ANSWERED 2026-09-17 (FABLE): `022CB728` is a dead predicate in this build; the `022CB726` half was answered 2026-09-14.** The word at `022CB728` has exactly one writer, the boot zeroing in `00360370` (`0036037E`), and one reader, `003603B0`, which returns it as a `u16`. A reference census of the whole block `022CB720`..`022CB72B` finds only rip-relative reads and writes, from `00360100`, `00360110`, `00360120`, `003601B0`, `003601C0`, `003601D0`, `00360370` and the four accessors, and no `lea` of any byte of the block, so no pointer-relative write can reach the word either. `003603B0` therefore always returns 0 and its three callers' refusal arms never fire: `ForceFightToggle_ApplyWithCapabilityGates` (`00252B60`, test at `00252C28`, where a non-zero would jump to `00252C5F` ahead of the skip-reset test `003603C0`), `00252C80` (`00252CA4`, the same pair of tests) and `002287D0` (`002287ED`, an early return of 0). The word is a second refusal predicate kept beside the skip-reset flag, with a place in the block and a boot value but nothing that ever raises it in the shipped executable. Static, whole-block census.*
- [x] ~~**UQ-151.** What `DAT_020927CC` is — a third override in the applier.~~ **PROPOSED-repos2d-10.**
      **Narrowed 2026-09-14 (FABLE): the mechanism is exact; the player-facing window is not named.** RIP census, three references:
      - **Set.** `00252DE0` (67 B) is the only function that stores 1 (`00252E0B`). It also sets its neighbour `020927C8` to 1 and zeroes `02092730` / `02092734`. Before those stores it makes three calls, one of them the UI body `003C5E50`; after them it calls `00366A00`, then tail-jumps into a drain of the `+0x7C70` queue on `[0209BE80]` (`0028F2A0`). Its one caller is a 1,689-byte actor body, right after `00238B00(0)` (`00262DC9`–`00262DCE`).
      - **Cleared.** `00253A30` stores 0 into both words (`00253A5E`–`00253A64`), after rebuilding the field-time UI (including `003CB410` / `003CB440`, the field-time container of [the map screens](../../16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md)), and ends in the same drain. Its one caller is `ActorSystem_InitializeManagerRuntime`, when that function's argument is 0 (`0026D36F`–`0026D374`).
      - **Read.** It has one reader: the applier's `cmp [020927CC], 1` (`00252BB6`). While the word is 1, the toggle is forced off (`state = 0`, `flag = 1`), after the policy gates and before the sound acquire and release.
      **So it latches "force-fight suppressed" from the `00252DE0` transition until the next manager-runtime initialisation rebuilds the field-time UI.** What that transition is in play, and ~~the role of `020927C8` (which also has a 15-caller setter and a separate reader), is not read here.~~ *(the transition is answered below, 2026-09-17.)*
      *Answered 2026-09-30 (SWE2-DATA, [`in_dd_checks.py`](../../_index/candidates/dd-data-0930/in_dd_checks.py) PC0–PC2): `020927C8` pauses
      the play clock.* Its one reader is `00254CC0` (`00254CC4`), which advances the play-clock counters only while
      the word is 0 (`00254CCB` jumps to the epilogue otherwise). The clock itself is on
      [the save-image page](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md)
      (*What the header records at save time*). Five rip-relative references and no other read: the area-change
      setter `00252DE0` and a boot-time initialiser set it to 1, the field-time UI rebuild `00253A30` clears it, and
      a one-store setter takes its argument. So the play clock stops over an area change, the same window as the
      force-fight latch beside it.
- [x] ~~What the two feature-enable bytes represent (this is the force-fight document's **AN-1**,
      not re-opened here).~~ *Answered 2026-09-17 (FABLE) on [the force-fight page](../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md) §5: `02B4053C` is the script-side `debug_setfightstatusbyevent` enable, reset to 1 at boot (`00266D10`) and at every area unload (`002628B0`), `02B4053D` its boot-set companion that nothing clears; the verb occurs in none of the 1,115 `us` event containers, so the enable is true from boot onward in the shipped game.*
- [x] **UQ-152.** Whether the one-instruction window in which `01E0C2B8` is `1` with the enable false is
      observable from another thread. Not establishable statically.
      **NARROWED 2026-09-16 (FABLE) - *not establishable statically* is too strong, and what is left is one much smaller question.** Observing the window means **reading the datum**, so the question is bounded by who reads it. **Exactly four functions touch `01E0C2B8`** - overlapping-byte-range census over all 38,161 listed bodies. **Two write it:** `00252C80` (sets 1 at `00252CD0`, overwrites at `00252CE4`) and `00254EA0` (same shape at `00254EB1`/`00254EC5`). **Two read it:** `00253B90` (`cmp`) and `00253BA0` (`cmovne`). **Nothing else in the image touches it at all.** **Each side has a named origin.** `00254EA0`'s reverse cone is **one function**: `003444D0`, which `scriptvm-verb-table.tsv` names as the handler for **`setforcefightmode`, call id `0334`, arity 1** - so one writer is a **script verb**. `00252C80`'s cone is three, rooted at `00253C50`. The reader `00253B90` has a cone of 373 containing `MainLoop_UpdateAndRenderFrame`, and its direct callers are the **battle-frame family**: `BattleAction_CheckActionAvailabilityReason`, `BattleUnit_UpdateEngagementStateFlag`, `BattleUnit_ComputePartyBattleStance`, `BattleUnit_UpdateCombatFrame`, `BattleRuntime_GetModeDependentDistanceThreshold`. **So the residue is one question, not a race.** A single thread cannot interleave with itself, so the window is observable **only if the script VM and the combat frame run on different threads**. That is a topology question the database has already begun - `CG-3` answered *the main thread, and no other party* for the graphics handshake, and the thread enumeration was corrected from nine to thirteen on 2026-09-12. **`UQ-152` should be restated as: do the script VM and the battle frame share a thread?** - which is a far cheaper thing to settle, and may already be settled elsewhere. *Bounds.* Direct-call graph and rip-relative census; an indirect call into any of the four, or a read through a register-held base, would not appear. **And I did not extract the thirteen thread start routines**, so I have not shown that none of them reaches these four - I have shown only that the reader set is two functions and both sit under the battle frame.
      **ANSWERED 2026-09-16 (FABLE), same day as the narrowing: NO.** I said the residue was *do the script VM and the battle frame share a thread*. Settled by enumerating the threads. **Every thread this image spawns through the imports.** The IAT slots are `008C21C8` (`CreateThread`) and `008C2D70` (`_beginthreadex`); over all listed bodies there are **nine call sites**, and each one's start routine is supplied by a `lea` a few instructions earlier: `00171370 thread_decoding_proc`, `005CCAB0`, `005CCBA0`, `007A5550` **(two sites - `007A5232` in `FUN_007A4D50` and `007B6FE4` in `FUN_007B6F70`)**, `007A5E50`, `007DD950`, `007DEC40`, and `00863500`, the engine's own thread-API entry. **None of them reaches the force-fight surface.** Forward direct-call cones from all eight start routines are **1 to 57 functions**, and **not one contains** `00252C80`, `00253B90`, `00253BA0` or `00254EA0` - nor `003444D0`, the `setforcefightmode` handler, nor `MainLoop_UpdateAndRenderFrame`, nor `BattleUnit_UpdateCombatFrame`. The spawned threads are narrow specialised workers: video decode and audio. **So both writers and both readers run on the thread that runs `main`, and a thread cannot interleave with itself.** The window is not observable from another thread. **A COUNT CORRECTION WHILE I WAS THERE.** The shared-command-state page's §10 says *all nine thread procedures*. There are **nine call SITES but eight distinct PROCEDURES** - `007A5550` is the start routine at two of them. The refutation that section rests on is unaffected; the count is not. *The bound, stated plainly.* These are **direct-call** cones, and they are small because indirect calls dominate this image - `BJ-1` measured direct-call closure from every boot root at **6.3%** of listed bodies. **An indirect call from inside a thread cone into one of the four would not appear here.** What the answer does not lean on is cone size: observing the window requires executing `00253B90` or `00253BA0`, and every direct caller of those is a battle-frame function.
      ***ANSWERED 2026-09-17 (FABLE): the latch marks the field slot's unload, so the toggle is held off from the moment an area's field manager is torn down until the next area's manager runtime rebuilds the field-time UI.** `00252DE0` has one caller, the manager-slot unload `002628B0`, and only on its slot-0 branch (`00262DB7`..`00262DCE`: slot 3 takes `00263660`, the other slots skip, slot 0 first calls `00238B00(0)` and then this setter). The setter runs three resets (`002B6260`, `003C5E50`, `003BBCF0`), stores 1 to `020927C8`, zeroes `02092730` and `02092734`, stores 1 to `020927CC`, calls `00366A00` and tail-jumps to `0028F2A0` (`00252DE4`..`00252E1E`). The clear is the field-time UI rebuild `00253A30`, which `ActorSystem_InitializeManagerRuntime` runs when the next area's managers come up. So the in-play transition is the area change: force fight cannot be switched on between leaving one field and the next field's UI being rebuilt, and `020927C8`, set beside it, marks the same window for its own readers. Static, both bodies read.*

- [x] **SD-1.** Which of the force-fight flag's consumers act on enemy units, and so what the `FLEEING` state
      changes for enemies. *Registered 2026-09-30 (SWE2-DATA), static.* *(SD-1 answered 2026-09-30 by OPUS `473de1075`, [record](../../_index/candidates/sd1-force-fight-enemy-consumers-0930/README.md).)*
- [x] **SD-2.** Which element of the layout sheet `battle_4_c` the label widget `00366B80` draws, and whether it is
      the `FLEEING` text. *Registered 2026-09-30 (SWE2-DATA), static.* *(SD-2 answered 2026-09-30 by OPUS `7573a1b87`, [record](../../_index/candidates/sd2-r2-label-element-0930/README.md).)*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The input is binding group 0, slot 9 | complete body of `0017DE10`; `r9b = 9`, `r8d = 0`, `edx = 0` at the call | 1 |
| `00197710` is `GetBinding(mgr, profile, group, slot)` | its complete 99-byte body: group dispatch to `+0x00` / `+0x40` / `+0x60` off base `01F80F90`, profile stride `0x1C` dwords — matching the keymap document's independently derived signature | 1 |
| Slot 9 of group 0 is `R2` | the sixteen wide-string pointers at `01DF11E0`, read from the image; the keymap document proves name index = slot index | 1 + 2 |
| One flip per press | `DAT_020927E4` set only on the held path, cleared on the released path, and tested before the flip | 1 |
| The three globals belong to `00253C70` alone | full-image rip-relative sweep: 4 / 5 / 2 sites, all inside it. **Positive control:** the same sweep found all 6 sites of `DAT_02F97360`, which is genuinely shared | 1 |
| The area pins the toggle | the release path's `DAT_020927E0 = 0` under `FieldRecordBit15()`, plus policy bit 10 in `00252B60` | 1 |
| The output is the force-fight flag | complete body of `00252C80`; the target `01E0C2B8` is identified by the force fight mode document from the script verb `setforcefightmode` | 1 + 2 |
| The first argument is inverted | `state == 0` takes the branch that stores `enable`, `state != 0` falls to the store of `0` — read from both the decompilation and the raw encoding at `00252CD0`/`00252CE4` | 1 |
| **AN-5: not reachable here** | the final store is `enable ? 1 : 0`; the transient `1` spans only the call to `003BA2E0`, which reads two byte globals and not the flag | 1 |
| The enable is set per area and by script | callers of `003BA300` / `003BA310`: `00266D10` (both), `002628B0`, `0050C910` (Script VM, pops one int) | 1 |
| The state written is the engaged bit, not the toggle | `00252C54`–`00252C5D` (`if state: state = 003669F0()`); `003669F0` = bit 2 of `022CBE1A` | 1 |
| The engaged bit needs `30 × [01DFE0B4]` frames | `00366870`: counter `003668F0`–`003668FA`, threshold test `00366902`, bit 2 at `00366918`; threshold written at `003670B7` (`imul ecx, r8d, 0x1e` on `[01DFE0B4]`) | 1 |
| The lag is what EXP-025 measured | 94 held samples with the flag unchanged over 0.97 s, then the flip; the second press writes on its first frame — both predicted by the no-write exit `00252CC8`–`00252CCE` and the release path | 1 + live (EXP-025) |
| The visible identity is `FLEEING` | EXP-025 screenshots after the first and second release, one field, stationary | live (EXP-025) |
| The arming counter runs to the threshold after release and the flag flips on that frame | EXP-028: counter 13 at the first released sample, 59 / word `0x11` / flag `1` at frame 1499, 60 / word `0x15` / flag `0` at frame 1500; threshold 60, time base 2 | live (EXP-028), sampled |

**Superseded readings:** none — this is the first document on this mechanism. The force fight mode
document's `00252C80` row said "unread"; it is now read, and its **AN-2** and **AN-5** are answered
above. That document is owned by another category and has **not** been edited from here; the
closures are filed for its owner.

## 9. Related

- [`../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md`](../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md) — the flag this toggle writes; **AN-2 and AN-5 answered here**
- [`../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md`](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md) — the area pin, and where this consumer was found
- [`../Gameplay-Capability-Policy/capability-inhibition-policy.md`](../Gameplay-Capability-Policy/capability-inhibition-policy.md) — the aggregate mask that overrides the toggle; its row 2 bit 10 is the same field-record bit
- [`../Binding-Profiles/keymap-ini-file-format-and-default-controls.md`](../Binding-Profiles/keymap-ini-file-format-and-default-controls.md) — the binding tables and the name-index-is-slot-index rule this document depends on
- [`../../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md`](../../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md) — the bit itself, whose open question C-12 this closes

## 10. Cross-subsystem neighbours — disposition

`audit_crossrefs.py` against `Tools/work/graph_gn` reported **9 UNACCOUNTED NEIGHBOUR** findings for
this document on its first pass. Every one is hub import: this document cites four functions with
large neighbourhoods, and citing them pulls in everything they touch.

### The force-fight predicate's census, stated here rather than deferred

`00253B90` is cited above. The force fight mode document gives its consumer *count* and the method,
and characterises the thunk's callers by subsystem — but it does not enumerate them, so pointing at
it would be a deferral, not a disposition. The census, from the current graph:

| Route | Distinct callers | Owners |
|---|---:|---|
| direct `00253B90` | 7 | CombatAction 2 (`BattleAction_CheckActionAvailabilityReason`, `FUN_0030C010`), CombatAI 1 (`BattleUnit_UpdateCombatFrame`), Presentation 1 (`BattleUnit_ComputePartyBattleStance`), ~~unowned 3~~ **unowned 2** (`BattleUnit_UpdateEngagementStateFlag`, `BattleRuntime_GetModeDependentDistanceThreshold`) + **InputGameplay 1** (`FUN_00313A00`) — *corrected 2026-09-14: the certified parent classifies `00313A00` as `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`. The route total of 7 is unchanged; only the owner split moves* |
| via thunk `0030C0D0` | 6 | Movement 5 (`BattleLocomotion_BuildSolverContext`, `BattleLocomotion_ComputeStepDistance`, `FUN_0033A720`, `FUN_0033C310`, `FUN_0033CEF0`), WorldAreaField 1 (`BattleSystem_RunFieldFrameOrchestrator`) |
| **union** | **13 distinct functions** | **6 owners** |

**A note on that number.** The force fight mode document says "15 consumers", counted as `.text`
call sites (7 + 8). Both figures are right and they answer different questions: **15 call sites
across 13 distinct functions**, the difference being that `BattleLocomotion_ComputeStepDistance`
calls it more than once. This document means distinct functions wherever it says callers.

That census accounts for the `CombatAI`, `CombatFormula` and `Presentation` findings that arrive
through `00253B90`.

### The field-record predicate: disposition by reference

`00377C20` and its thunk `00313F60` reach **110 distinct functions across 15 subsystems**, fully
enumerated in
[the field record table](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md)
§3 and in
[the bit 15 document](../../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md)
§9, which gives the complete owner breakdown. The `Spawn_Encounter_Lifecycle`
(`002350C0`, `00234DA0`), `Items_Equipment_Shops_License` (`00309FB0`, `0030FD10`),
`Rewards_Progression_Economy` (`00312280`), `CombatFormula` (`00300530`, `00384F40`) and remaining
`CombatAI` edges are that predicate's neighbours, not this toggle's. *Valid deferral — the census
is in those documents.*

One edge arrives at a second remove: `00312280` `BattleUnit_ProcessDefeatRewardsAndLoot`, named
just above as one of that predicate's callers, itself calls `00316A50`
(`PlatformOnlineAchievements`). That is the defeat path reaching achievement bookkeeping, recorded
and explicitly **not** characterised in the field record document's §11. It is two removes from
this toggle and belongs to neither.

### The two enable-setter callers: irrelevant, with the reason

`002628B0` (ActorEntity) and `00266D10` (field/area initialisation) are cited **only** as two of
the three callers of the enable-byte setters `003BA300` / `003BA310`. They are large initialisation
routines with roughly 130 and 70 callees between them, and those callees — the `Audio`,
`Presentation`, `Resource` and `Save_Load_Settings` findings — are what an area initialiser does.
None of them touches the toggle, the latch, the flag or the enable bytes. **Irrelevant to this
system; cited for one edge each and nothing more.**

If a later pass wants those two functions explained, they need their own document; naming them here
as callers of a 7-byte setter does not make this document responsible for area initialisation.

**Audit state.** `audit_crossrefs.py` against `Tools/work/graph_gn` (38,161 functions, 90,525
edges): **9** findings on the first pass, **0** after the dispositions above, against that graph
state. `check_links.py` passes; `verify_doc_addresses.py` resolves all 52 cited addresses
(37 function entries, 13 data, 2 interior) with no `.text` non-function citations.
~~**No falsification pass has been run** — `audit.passes: 0`, and the status is `PARTIAL` because §7's
first entry is the question the document is named for.~~ *(Corrected 2026-09-30, SWE2-DATA: pass 1 ran on
2026-09-03 — the section below — and the front matter records `audit.passes: 1`. The status stays `PARTIAL`
on SD-1 and SD-2.)*

## Falsification pass 1 — 2026-09-03, by a session that did not write this document

Program state: GZF `2ed8affb…`, snapshot `46f02e26…`, EXE `73461d08…`.

**Nothing was overturned.** Three of the document's own load-bearing claims were re-derived
independently and all three hold; two are recorded below as *stronger* than the document had them.

### The load-bearing step: group 0 slot 9 is R2 — and the whole table says so

Everything above the input rests on one lookup, so it was read from the bytes rather than taken from
the body that computes it. The name table at `01DF11E0` holds **UTF-16LE** strings, and group 0's
sixteen slots read:

```
0 Select   1 L3    2 R3     3 Start
4 Up       5 Right 6 Down   7 Left
8 L2       9 R2   10 L1    11 R1
12 Triangle 13 Circle 14 Cross 15 Square
```

**Slot 9 is `R2`, confirmed.** And the strengthening: the document cites slot 9 alone, where a single
name could be a coincidence of indexing. **All sixteen are present, in the DualShock digital-button
order**, which no off-by-one or mis-based read produces. The identification is safe.

*(Instrument note: an ASCII reader truncates every one of these at the first byte — slot 9 reads as
`'R'`. The first pass of this check reported `'R'` and had to be redone as UTF-16.)*

### The inversion, from the raw encoding

Confirmed at exactly the two addresses §8 cites, with `ebp` = `state`, `esi` = the flag's current
value at `01E0C2B8`, `ebx` = 0 from the prologue:

```asm
00252CBA  test ebp, ebp ; je 0x252CC8     ; state == 0 -> the SET path
00252CC8  test esi, esi ; je 0x252CD0
00252CD0  mov dword [01E0C2B8], 1         ; <- state == 0 STORES 1
00252CDA  call 003BA2E0                   ;    feature enable
00252CE4  mov dword [01E0C2B8], ebx       ; <- state != 0 STORES 0
```

**`state == 0` sets force fight mode; `state != 0` clears it.** The document's polarity claim is
exactly right, and the two store sites are where it says they are.

### The corrected sound id was corrected correctly

`00366870` passes its index to the resolver, not to the play call:

```asm
00366892  mov  ecx, 0x52
00366897  call 003A1180        ; bankSlot*512 + index -- the world-live resolver
0036689F  je   ...             ; -1 -> nothing plays
003668A1  mov  edx, 0x40       ; pan
003668A8  lea  r8d, [rdx+0x3f] ; volume 0x7F
          -> 002DF220
```

So `0x52` is a **bank-local index**, as the document's own correction says, and this is the same
gate → resolve → play seam documented in
[the audio boundary](../../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md). The
correction reached the right answer and the right reason.

### Two bare names identified, and they are audio gates

The condition `FUN_003603B0() == 0 && FUN_003603C0() == 0` guards the sound. Both are 8-byte reads of
adjacent globals in the audio gate block:

| function | body | reads |
|---|---|---|
| `003603B0` | `movzx eax, word ptr [rip+…]` | the **word** at `022CB728` |
| `003603C0` | `movsx eax, byte ptr [rip+…]` | the **byte** at `022CB726` — the audio boundary's *second gate*, the one that makes `002DF220` return 0 |

So the toggle does not merely decline to *request* the sound when audio is gated — it consults the
same gate the play call itself consults, one level earlier. Cross-checked against the audio boundary
document, which reaches `022CB726` from the other side.

### Attacked and confirmed

- **All 17 body sizes in the document's tables: exact.**
- The polarity, the slot-9 lookup and the bank-local index: all three re-derived, all three hold.

### What I tried that failed to break it

- Attacked the body sizes first because I had **fabricated seven of them myself** in another document
  earlier the same day. 17 of 17 correct here.
- Attacked the slot-9 identification expecting an off-by-one, since the document rests everything on
  it and cites only one slot. The full sixteen-name table refutes that possibility outright.
- Attacked the "corrected once" claim by checking whether the *same* shape recurred elsewhere in the
  document — a raw id treated as global when the resolver makes it bank-local. `0x52` is the only
  sound id it cites, and it is correctly qualified in all four places it appears.
- Ran the neighbour check first: 53 cited addresses shared with **21** other documents, three of them
  with the audio boundary — which is how the two gate functions were identified rather than left as
  `FUN_` names.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Developer — CLIENT, ~~not read~~ identified 2026-09-30 (SWE2-DATA).** An 8-byte function this page cites is called by a 1,046-byte Developer-labelled body.
  The 8-byte function is the framework-object getter `00796E20` of §2a, and the Developer body is the
  `MultipleDebugDisplay` initialiser named on
  [the game-application page](../../00-Engine-Core-Runtime/Application-Root/game-application.md), one of the getter's
  many callers. It is fan-in to a shared static getter and does not touch the toggle, the latch, the flag or the
  enable bytes.
- **UI — SERVICE and CLIENT (FABLE, Claude Opus 5.5, 2026-09-25, for FM-1).** The toggle's timing and its label live
  in the UI layer. That covers the toggle module `00366740`–`003669F0`: its state word `022CBE1A`, the arming counter
  `00366870`, and the label widget `00366B80`. It also covers the UI mode word `022C83EC`, with setter `0035C880` and
  getter `0035C6F0`.
  - **Input calls into it (SERVICE).** This page's applier `00252B60` calls into both, as does the area-change latch
    setter `00252DE0`, which also runs the UI resets and the queue drain `0028F2A0`.
  - **UI calls back (CLIENT).** The field-time UI rebuild `00253A30` builds the label widget and clears the latch.

  The relationship is an input toggle driving UI state, which UI then displays. The rest of the UI edges are fan-in
  to shared widget helpers.
- **WorldAreaField and World — CLIENT (FABLE, Claude Opus 5.5, 2026-09-25).** The toggle is gated and reset by area
  state, as this page's evidence table records.
  - The input arbiter `00253C70` consults field-record predicates (`00313F60`, `00265270`, `00377C20`) that pin
    the toggle per area.
  - The area reset `00266D10` re-arms the two feature-enable bytes through `003BA300` / `003BA310`, at boot and at
    area unload.
  - The manager-slot unload `002628B0` runs the area-change latch setter `00252DE0` on its slot-0 branch.

  The crossing is area lifecycle driving the toggle's gates. The other edges in these layers, and the
  Spawn_Encounter_Lifecycle ones, are fan-in: shared field predicates such as `00313F60`, which the spawn-placement
  bodies call too.
