---
system: The scripted camera player — named shots, channels, and the CAM7 command stream
category: 17-Presentation-Rendering
status: AUDITED
owner_layer: CodeDomain:Presentation.Camera
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation delta - every function this document cites whose record differs between the stamped snapshot and GN161's gained a plate comment and tags ONLY (empty comment before, tag set a subset, checked field by field), and this document makes no uncorrected absence claim about any of them; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 1 cited address(es) among the 128 records changed across GN158..GN161; each differs only in comment and tags; 0 live absence claims (check_stranded_absence.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-DELTA-RELIANCE-BASIS; re-measured and applied for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708, on SNAPSHOT-IDENTITY - replaced rather than re-targeted because that basis is FALSE for this document, which cites a record that changed
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-scripted-camera-player-pass-1
  crossref_clean: false
  reopened_count: 0
---

# The scripted camera player

> Plays the authored camera shots a map or event script names: it walks each shot's key/segment
> command stream frame by frame, interpolates the eye, target, roll and field of view, and hands
> the result to the engine's camera-record stack as priority record 5.

**Extents read**: `00258350` 1,942 B complete (ends `ret` at `00258A8E`, tail to `00258AE1`);
`00256960` 828 B and `00256CA0` 694 B complete for their field reads; `00255410` 195 B, `002554E0`
191 B, `00255E80` 353 B, `00257230` 167 B, `002572E0` 570 B, `003DA050` 302 B, `003DA400` 206 B,
`003DA330` 59 B, `002567E0` 384 B, `003CC5F0` 196 B, `003CC740` 321 B, `003CC890` 218 B,
`00257B50`, `00258090`, `00257BF0`, `00257D10`, `00257E40`, `00257F60`, `002555D0`, `00258190`
complete. ~~Not read: `00255850` (961 B) and `00257520` (731 B) beyond their calls into record 5 —~~
~~see §5.~~ *(answered: see BY-9, answered 2026-09-14; 2026-10-02, OPUS)*

## 1. What the player sees

Every directed camera move in FFXII — the pan across the Royal City when Vaan first looks up at
it, the swing round to a treasure chest, the crane shot as an Esper lands, the slow push-in on two
characters talking — is **a named shot stored in the map's or event's script file**, and this
system is what flies the camera along it.

A shot is a short list of **key poses** (where the camera is, what it looks at, how far it is
tilted, how wide the lens is) joined by **moves**. A move says how long to take and how to travel:
straight across, or **swinging round** the thing being looked at, or **turning on the spot** to
look somewhere else. Each part of a move can have its own **ease curve**, so the camera can start
slowly and settle gently, and either end of the camera can **ride along a smooth authored path**
instead of a straight line. A shot can also be **pinned to a character**, so that the camera
follows someone who is walking, and the scene still frames them.

Scripts can run up to **four shots at once** per script owner and switch which one the screen
shows, change a shot's **playback speed**, **wait** for a shot to finish, **stop** it, or **ask
whether a shot would pass through a wall** before committing to it. When the script owner is
flagged to skip, a running shot is **fast-forwarded to its last pose** rather than cut off
mid-move, so the camera ends where the shot would have ended.

While any shot is playing on the main screen, the directed camera **outranks the ordinary follow
camera**; when the last one stops, control falls back to the camera below it.

## 2. Native mechanism

### 2.1 Where the data comes from

A shot lives in two sections of the script container:
[`section_009`](../../25-EBP-Script-Container/Sections/section-009.md) (`CAM7`) holds the shot
records and two pools of shared data — **timing curves** (array B) and **paths** (array C) — and
[`section_008`](../../25-EBP-Script-Container/Sections/section-008.md) (`CML1`) is the list a script
indexes. The loader `002561C0` keeps the section resident and builds three pointer arrays per
**script-owner slot** (the five actor-manager slots): one 0x40-byte entry per shot, one pointer
per timing curve, one per path. **The script's number selects a `CML1` entry, and the entry's
authored `+0x04` selects the shot** — no name is compared at run time (the resolver that would do
so is dead in the shipped build; `BY-3`).

At manager runtime initialisation, `002572E0` decodes each shot's **attachment word** (record
`+0x20`, §4.2): it finds the n-th kind-3 actor of the owner (`00257AD0`) for the eye and for the
target, stores the actor pointers in the entry at `+0x20` / `+0x28`, and unpacks the mode and flag
bits into entry bytes `+0x34`–`+0x3D`.

### 2.2 Starting, stopping and switching shots

Each actor-manager slot has **four camera channels** (`ActorManagerSlot +0x110`, 24 bytes each)
and a two-entry **frame owner** table at `+0x18`: frame 0 is the main frame and frame 1 the sub
frame — the verbs `getcameramainframe` (`0050F100`) and `getcamerasubframe` (`0050D1C0`) return 0
and 1 — and each entry holds the channel that drives that frame. A frame number above 1 is stored
unchecked and writes past the table (`003DA4B9`; one shipped call passes 110 — see the
[slot entry contract](../../04-Actor-Entity/CONTRACT-manager-slot-entry-tables.md) §14.3); the tick
only reads frames 0 and 1, so such a channel never publishes.

| verb | handler | backend | effect |
|---|---|---|---|
| `camerastart(entry)` | `0034FE00` | → `camerastart_7e(0, entry)` | play on channel 0, frame 0 |
| `camerastart_7e(ch, entry)` | `0034F930` | `003DA400` | play on `ch`, frame 0 |
| `camerastart_7d(ch, entry, frame)` | `0034F2F0` | `003DA400` | play on `ch`, the given frame (scripts pass `getcamerasubframe()`) |
| `camerastop()` (channel 0) / `camerastop_54(ch)` | `00350660` / `003502E0` | `003DA4D0` | channel state ← 0 |
| `camerachange(ch)` | `00351C00` | `003DA570` | the channel's frame is driven by `ch` |
| `cameraclear()` | `00351540` | `003DA000` | both frames unowned, all four channels idle |
| `cameraratio(rate)` / `cameraratio_115(ch, rate)` | `00351190` / `00350B00` | `003DA2D0` | channel `+0x10` rate |
| `camerahitcheck(entry)` / `camerahitcheck_33c` | `0034EDB0` / `0034E9B0` | `003DA330` → `002567E0` | dry-run the shot; 1 if a probe hits |

The entry number is the low 24 bits of the script operand (`and edi, 0xFFFFFF` at `0034F976`;
scripts write `0x02000000 | n`). `003DA400` rejects a channel above 3, a missing `CML1` list or an
entry number outside `[0, count)`, then fills the channel (§4.5), calls `00257230` to reset the
per-channel player state and point it at the shot's command stream, and records the channel as its
frame's owner (`003DA4B9`).

### 2.3 The per-frame tick

`003DA050` runs per actor-manager slot:

*Added 2026-09-19 (FABLE):* the slot holds a second set of four channels of the same shape, at `+0x170` over a bank
behind `+0xF0` - **camera shake**, driven by `003DCFB0`, which the same caller runs next. It is described on
[how a camera reaches the renderer](how-a-camera-reaches-the-renderer.md) section 4a.


```c
for (f = 0; f < 2; f++) {                          // 003DA092..003DA0C3
    ch = slot->frameOwner[f];
    if (ch >= 0 && slot->channel[ch].state != 0)
        player[slot][ch].frame = f;                // 002563C0 -> channel +0x184
}
for (ch = 0; ch < 4; ch++) {                       // 003DA0E0..003DA15C
    c = &slot->channel[ch];
    if (c->state == 0) continue;
    if (c->state != 2) {
        step = *(float*)0x02B4E4B0 * c->rate * 1.0f;   // <- corrected 2026-10-02, OPUS - the third factor is float [01DFE0BC] (003DA050+0xB0), 1.0 in the image and 0.5 on the 60 fps arm
        if (c->clockRunning) c->clock += step;     // the first positive step only arms the clock
        if (step > 0) c->clockRunning = 1;
    }
    if (slot->skipToEnd /* byte +0x201 via 00267300; its setter was not traced */)
        CAM7_RunToEnd(slot, c->shot, ch);          // 00257A00
    else
        CAM7_Evaluate(slot, c->shot, c->clock, ch, /*mode*/0);  // 002555A0 -> 00258350
    if (player[slot][ch].state == 2) c->state = 2; // 002567B0 reads +0x180
}
```

`CAM7_RunToEnd` steps the same evaluator by each command's own length — 1 frame for a key, the
segment duration for a segment (`00258AF0`) — until the end marker, so a skip lands on the final
pose with every intermediate segment completed.

### 2.4 Evaluating a shot — the command stream

The player state for (slot, channel) is a 0x2E0-byte record at `02092830 + slot·0xBB0 + ch·0x2E0`

> **⚠ Corrected 2026-09-14 (OPUS), pass 13 — independent re-derivation.** The function table's summary
> for `CAM7_ResetSlot` read *"clear four players"*; the body `memset`s **one** `0x2E0` record, at the
> address this very line gives. The three pointers it frees (`003697F0` on `+0x10`, `+0x18`, `+0x20`,
> each nulled after) live in the **slot header** at `02092800 + slot·0xBB0`, which is why a slot is
> `0x30 + 4·0x2E0 = 0xBB0` rather than `4·0x2E0`. It also writes `-1` to record `+0x184` and calls
> `003CBFF0` on the sub-object at `+0x210`. **This line and the layout table were right; only the
> one-line summary was wrong**, and it was wrong in the direction that makes a reconstruction clear
> four records instead of one.
(§4.5). `00258350(slot, shot, time, ch, mode, actor, out)`:

1. **Delta and attachments.** `+0x10 = time − +0x0C`, `+0x0C = time`. If the shot's entry has an
   eye attachment (entry `+0x20`) and the slot is live (`002671F0`), `00258190` builds the
   attachment transform into `+0x190` — the actor's yaw rotation when the rotate flag is set,
   translated to the actor's position or joint; with a hold flag the height or ground position
   keeps the value from the frame before (`002582A2`, `00258284`, gated on `+0x189`, set after the
   first build) — and likewise the target into `+0x1D0`. Without an attachment the matrix is
   identity (`00203170` copies the four rows `008C5F80`/`008C5F90`/`008C5FB0`/`008C5FD0` at
   `00203177`/`00203181`/`0020318C`/`00203197` — the same identity rows the dyngeo page dumps
   as `{1,0,0,0}`…).
2. **Walk commands** from the stream pointer `+0x178` (`00258567`–`00258582`):
   - **key (type 1)**: copy eye `+0x04`, target `+0x14`, roll `+0x24`, fov `+0x28`, and the
     three path-follow scalars `+0x2C`, `+0x30`, `+0x38` into the current pose `+0xA0`–`+0xD0`;
     remember the key at `+0xE0`; advance `0x40`; state 1; **continue walking**.
   - **segment (type 2)**: add the delta to the segment clock `+0x08`; compute the 13 channel
     progresses (§2.5), the two path offsets (§2.6), and the interpolated pose between the key
     at `+0xE0` and the key that follows the segment (`+0xE8 = segment + 0x2C`). If
     `clock >= duration` (`+0x22`), advance `0x2C`, subtract the duration and **continue**;
     otherwise stop walking.
   - **end (0xFF)**: state 2; stop.
3. **Compose.** `eye = pathOffset[0] + (absolute ? 0 : pose.eye)`, `target = pathOffset[1] +
   (absolute ? 0 : pose.target)` (`+0x124`, from segment `+0x25`), each transformed by its
   attachment matrix (`00202B70` — ~~`call 00217060` returns the matrix, `movups` copies its~~
   ~~first 16 B at `00202B83`/`00202B86`~~ *`00217060` transforms the point through the matrix into a private
   temporary at `rsp + 0x20` (four stores, `002170CE`-`0021713D`), and `movups` copies that 4-float result to the
   caller's output at `00202B83`/`00202B86`; `rax` is left naming the dead temporary, so no caller-owned pointer is
   returned. Corrected 2026-09-27 (FABLE, Claude Opus 5.5; bytes re-read), on OPUS-NOTICE-FABLE-CAMERA-MXVW-RETURN
   and ASTRA's [matrix-buffer-alias](../../_experiments/evidence/matrix-buffer-alias/README.md)*), written to the
   output view `02096370 + frame·0x40`:
   eye `+0x00`, target `+0x10`, fov `+0x24` = `pose.fov · π / 180 + attachFov`, roll `+0x20` =
   `pose.roll − attachRoll` (or 0 in path-follow kind 5).
4. **Build the view** into `+0x210` — `003CC000` in path-follow (up vector `+0x110`), else
   `003CC080` (`003CC970` only when `+0x188` is set, which only the `debug_cameraescape` verb
   does, `0050CD30` → `00257AA0`; no shipped script uses it) — and store `fov`, `1 / tan(fov / 2)`.

In **mode 1** (the hit check) step 4 is replaced by a probe `00230B60(actor, eye, target)`;
`*out = 1` when it returns non-negative. `002567E0` runs the shot on the scratch player
`02096520` from time 0 in 1-frame steps and returns 1 at the first hit.

**A segment interpolates from whatever key the channel last passed.** `00257230` does not reset
`+0xE0`. The one shipped stream that begins with a segment, `dst_a07` shot 2, is started on channel
0 straight after shot 1 (`dst_a07.txt`: `camerastart(0x02000001)` … `camerastart(0x02000002)`), so
it blends out of shot 1's last pose. Started on a fresh channel, `+0xE0` is zero from the reset and
`00255E80` dereferences it at `00255EBA`.

### 2.5 Timing: 13 channels of progress

`00255410` computes, for each of the segment's 13 timing words `+0x04`–`+0x1C`:

```c
if (word & 0x8000)                                   // an ease curve from array B
    running[i] = Curve_Evaluate(curves[word & 0x7FFF], clock, &progress[i]);   // 003CC5F0
else {                                               // plain frames: linear
    running[i] = (float)word >= clock;
    progress[i] = clock / (float)word;
}
```

`progress` is `+0x128 + 4i`, `running` is `+0x15C + i`. **A component whose `running` byte is 0
is not interpolated this frame** — it keeps its last value. The components (from the readers):

| i | drives | read at |
|---:|---|---|
| 0, 1, 2 | eye x, y, z — or, in kinds 1/2, the eye's orbit (0 = yaw/pitch/distance, 1 = height in kind 2) | `00257B50`, `00257BF0`, `00257D10` |
| 3, 4, 5 | target x, y, z — or the target's turn in kinds 3/4 | `00258090`, `00257E40`, `00257F60` |
| 6 | roll | `00258788` |
| 7 | field of view | `002587B3` |
| 8, 9 | progress along the eye path and the target path | `002554E0` (`+0x148`, `+0x14C`) |
| 10, 11, 12 | the three path-follow scalars (key `+0x2C`, `+0x30`, `+0x38`) | `002587DE`, `00258809`, `00258834` |

**Ease curve** (array B record, §4.3), `003CC5F0`:

```c
if (n == 0)             { out = endValue;  return 0; }
if (clock <= start)     { out = startValue; return 1; }
if (clock == end)       { out = endValue;  return 1; }
if (clock >  end)       { out = endValue;  return 0; }
u = clock / end;                               // normalised by the END time, not (clock-start)
for (k = 0, acc = 0; acc + key[k].span <= u; k++) acc += key[k].span;   // spans sum to 1.0
v = (u - acc) / key[k].span;
out = key[k].a*v*v*v + key[k].b*v*v + key[k].c*v + key[k].d;
```

The span walk has no bound; it relies on the spans summing to 1.0, which all 15,350 shipped curves
do (census).

### 2.6 Paths: two additive offsets

`002554E0` evaluates the segment's two path words `+0x1E` (eye) and `+0x20` (target):

```c
if (!(word & 0x8000)) offset = (0,0,0);
else if (word & 0x4000) offset = Path_AtDistance(paths[word & 0x3FFF], progress[8 + j]);          // 003CC710
else                    offset = Path_AtDistance(p, progress[8 + j] * p->arc[p->m - 1].distance); // 003CC6C0
// Path_AtDistance: distance -> parameter through the arc table (003CC890, binary search + lerp),
// then the cubic segments (003CC740); param <= 0 -> start, >= 1 -> end.
```

So a plain path word runs the whole path over the progress 0→1 at constant speed; bit 14 treats
the progress as an absolute distance.

### 2.7 Interpolation kinds (segment `+0x24`)

`00255E80` seeds a start pose (from `+0xE0`) and an end pose (from `+0xE8`) and, for kinds 1–4,
converts each to polar form:

| kind | eye | target | polar form (`00255E80`) | shipped segments |
|---:|---|---|---|---:|
| 0 | linear per axis (`00257B50`) | linear per axis (`00258090`) | — | 3,406 |
| 1 | **orbits the target**: yaw, pitch, distance (`00257BF0`, progress 0) | linear | `003CC130(target, eye)` | 116 |
| 2 | **orbits in the horizontal plane**: yaw and ground distance by progress 0, height by progress 1 (`00257D10`) | linear | `003CC270(target, eye)` | 57 |
| 3 | linear | **turns around the eye**: yaw, pitch, distance (`00257E40`, progress 3) | `003CC130(eye, target)` | 67 |
| 4 | linear | turns in the horizontal plane (`00257F60`) | `003CC270(eye, target)` | 8 |
| 5, 6 | **path-follow**: sample the eye path around the current progress and aim along it (`00256960`, `00256CA0`) | | — | **0** |

Angles take the short way round: the yaw difference is wrapped into `[−π, π]` before interpolation
(`00257C2D`–`00257C57`). Kinds 5 and 6 read path-follow scalars from the key (`+0x2C`, `+0x30`,
`+0x38`) and set the path-follow flag `+0x120` (kind 5); **no shipped segment uses them** — the
scalars are `0, 0, 1` in 7,609 of 7,614 keys.

### 2.8 Handing the view to the camera stack

`002555D0`, per frame, walks every player (5 slots × 4 channels). For each with a frame
(`+0x184 != -1`) it calls `0025A3B0(frame, 5, &player.view)`: frame 0 copies the view into
**camera record 5** (`CameraRecord_CopyViewState`, `0025A2C0`; records at `02097300`, stride
`0x110`) and sets its mode to 3 (`0025A500`); frame 1 copies into a separate view at `02097B80`
(`0025A3D0`; ~~what consumes it was not traced~~ *(answered: see how-a-camera-reaches-the-renderer.md §2 - `00259970` submits the static default view at priority `0x14`; 2026-10-02, OPUS)*). Two other producers also write record 5 — `00257520` and `00255850` (not read here).
Finally `CameraSystem_SetCameraActive(5, any)` sets bit 5 of the active mask `02098DEC` if any
player had a frame or either other producer submitted, and clears it otherwise; `CameraSystem_SelectAndPublishActiveView` (`00259820`) publishes **the highest set
bit**, so record 5 outranks records 0–4 and yields to 6–7.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00258350` | `CAM7_Evaluate` | 1942 B | the command-stream interpreter (§2.4) |
| `002555A0` | `CAM7_EvaluateSubmit` | 35 B | calls it with mode 0 |
| `00257A00` | `CAM7_RunToEnd` | 151 B | skip: step to the end marker |
| `002567E0` | `CAM7_HitCheck` | 384 B | dry run on the scratch player |
| `00257230` | `CAM7_BindShotToChannel` | 167 B | reset player state, point at the stream |
| `002566E0` | `CAM7_ResetSlot` | 193 B | ~~clear four players~~ **clear ONE `(slot, channel)` player**, free the slot's three pointer arrays |
| `002556F0` | `CAM7_InitAll` | 277 B | clear every slot and the scratch player |
| `002572E0` | `CAM7_BindAttachments` | 570 B | decode record `+0x20` into entry `+0x20`–`+0x3D` |
| `00257AD0` | `Manager_FindNthKind3Actor` | 116 B | attachment actor lookup |
| `00258190` | `CAM7_BuildAttachTransform` | 433 B | actor or joint transform, lock flags, roll/fov offsets |
| `00255410` | `CAM7_ComputeProgress` | 195 B | 13 timing words (§2.5) |
| `002554E0` | `CAM7_ComputePathOffsets` | 191 B | two path words (§2.6) |
| `00255E80` | `CAM7_SeedPose` | 353 B | start/end pose and polar form |
| `00257B50` | `CAM7_LerpEye` | 156 B | kind ≠ 1, 2 |
| `00258090` | `CAM7_LerpTarget` | 156 B | kind ≠ 3, 4 |
| `00257BF0` | `CAM7_OrbitEye` | 281 B | kind 1 |
| `00257D10` | `CAM7_OrbitEyeFlat` | 304 B | kind 2 |
| `00257E40` | `CAM7_TurnTarget` | 281 B | kind 3 |
| `00257F60` | `CAM7_TurnTargetFlat` | 304 B | kind 4 |
| `00256960` | `CAM7_FollowPath5` | 828 B | kind 5 |
| `00256CA0` | `CAM7_FollowPath6` | 694 B | kind 6 |
| `00258AF0` | `CAM7_CurrentCommandLength` | 88 B | 1 / duration / 0 |
| `00258B50` | `CAM7_PlayerClock` | 51 B | player `+0x0C` |
| `002563C0` | `CAM7_SetPlayerFrame` | 35 B | player `+0x184` |
| `002567B0` | `CAM7_PlayerState` | 46 B | player `+0x180` |
| `00257AA0` | `CAM7_SetViewBuilderFlag` | 35 B | player `+0x188`; debug verb only |
| `003CC5F0` | `Curve_Evaluate` | 196 B | array-B ease curve |
| `003CC6C0` | `Path_AtProgress` | 72 B | scale by total arc length |
| `003CC710` | `Path_AtDistanceDirect` | 45 B | bit-14 form |
| `003CC890` | `Path_DistanceToParam` | 218 B | arc table search |
| `003CC740` | `Path_EvaluateCubic` | 321 B | segment cubic |
| `003CC130` | `Polar_FromPoints` | 317 B | yaw / pitch / distance |
| `003CC270` | `Polar_FromPointsFlat` | 114 B | yaw / ground distance |
| `003CC2F0` | `Polar_ToPoint` | 199 B | inverse of `003CC130` |
| `003CC3C0` | `Polar_ToPointFlat` | 178 B | inverse of `003CC270` |
| `003DA050` | `CameraChannels_Tick` | 302 B | §2.3 |
| `003DA400` | `CameraChannels_Start` | 206 B | §2.2 |
| `003DA330` | `CameraChannels_HitCheck` | 59 B | |
| `003DA4D0` | `CameraChannels_Stop` | 33 B | |
| `003DA570` | `CameraChannels_Change` | 36 B | |
| `003DA000` | `CameraChannels_Clear` | 70 B | |
| `003DA2D0` | `CameraChannels_SetRate` | 17 B | |
| `002555D0` | `CAM7_PublishAll` | 279 B | §2.8 |
| `0025A3B0` | `CameraRecord_SubmitForFrame` | 24 B | frame 0 → record, 1 → sub-view |
| `0025A3D0` | `CameraSubView_CopyViewState` | 207 B | |
| `0025A500` | `CameraRecord_SetMode` | 21 B | record `+0xF0` |

Addresses are Ghidra image base `0x00120000`. Working names are proposals; none is applied in the
project.

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02092800` | `g_cam7Slots` | `.bss`, 5 × `0xBB0` | per slot: `+0x08` section, `+0x10` entries, `+0x18` curve pointers, `+0x20` path pointers, `+0x30` four players |
| `02096520` | `g_cam7ScratchPlayer` | `.bss`, `0x2E0` | channel `-1`: the hit-check player |
| `02096370` | `g_cam7FrameViews` | `.bss`, 2 × `0x40` | eye, target, roll, fov per frame |
| `02097300` | `g_cameraRecords` | `.bss`, 8 × `0x110` | the camera-record stack |
| `02098DEC` | `g_cameraActiveMask` | `.bss`, u32 | bit n = record n active |
| `02097B80` | `g_cameraSubView` | `.bss` | the sub-frame view state |
| `02B4E4B0` | frame step | `.bss`, f32 | the clock step `003DA0F3` reads (not traced) |

## 4. Data structures and formulas

### 4.1 A shot record's command stream

A record (`section_009` §2) is `+0x00` zero, `+0x04` length, `+0x08` name, `+0x20` attachment word,
`+0x24` / `+0x26` joint words, then from `+0x28` **a stream of commands ending in `0xFF` and three
pad bytes**. Every one of the 3,942 shipped records parses this way and ends exactly at its length.

```struct Cam7Key base=record size=0x40
+0x00  u8        type        1
+0x01  byte[3]   _pad0       0
+0x04  f32[3]    eye         world position
+0x10  f32       eyeW        1.0 in 7,614 of 7,614 -- not read
+0x14  f32[3]    target      world position
+0x20  f32       targetW     1.0 in 7,614 of 7,614 -- not read
+0x24  f32       roll        radians; 0 in 6,607 keys
+0x28  f32       fovDegrees  40, 38, 45 most common; x pi/180 at 002586A5
+0x2C  f32       followA     path-follow scalar -> pose +0xC8
+0x30  f32       followB     path-follow scalar -> pose +0xCC
+0x34  f32       _unread0    0 in 7,614 -- not read
+0x38  f32       followLead  path-follow look-ahead -> pose +0xD0; 1.0 in 7,609
+0x3C  f32       _unread1    0 in 7,614 -- not read
```

```struct Cam7Segment base=record size=0x2C
+0x00  u8        type        2
+0x01  byte[3]   _pad0       0 in all 3,654
+0x04  u16[13]   timing      bit 15 = ease curve (array B index & 0x7FFF); else duration in frames
+0x1E  u16       eyePath     bit 15 = array C index & 0x3FFF; bit 14 = progress is a distance
+0x20  u16       targetPath  as eyePath
+0x22  u16       duration    frames; never 0 in the corpus
+0x24  u8        kind        0-6, section 2.7
+0x25  u8        absolute    nonzero = path offsets replace the pose (+0x124)
+0x26  byte[6]   _pad1       0 in all 3,654
```

Stream shapes in the corpus: `K S K E` 3,421 · `K E` 421 · `K S K S K E` 59 · longer chains to 12
segments · `K S K K …` (a key straight after a key, a cut) 18 · `S K E` 1. Record lengths are
therefore `0x2C + 0x40·keys + 0x2C·segments`: 108 = one key, 216 = key-move-key, 152 = the one
segment-first record — which is why `section_009` §5 saw 11 distinct lengths and "one record
where `+0x28` is 2".

### 4.2 The attachment word, record `+0x20` (`002572E0`)

```c
eyeActor    = (w & 0x1FF)       ? NthKind3Actor(slot, (w & 0x1FF) - 1)         : NULL; // entry +0x20
targetActor = (w >> 16 & 0x1FF) ? NthKind3Actor(slot, ((w >> 16) & 0x1FF) - 1) : NULL; // entry +0x28
// only decoded when the id is nonzero:
entry+0x34 = (w >> 13) & 3;   entry+0x35 = (w >> 29) & 3;   // attach mode: 0 actor position, 1 002E7F10, 2 002ED430
entry+0x36 = (w >> 15) & 1;   entry+0x37 = (w >> 31) & 1;   // rotate with the actor (00265200 yaw)
entry+0x38 = (w >> 11) & 1;   entry+0x3A = (w >> 27) & 1;   // hold height after the first frame
entry+0x39 = (w >> 12) & 1;   entry+0x3B = (w >> 28) & 1;   // hold ground x/z after the first frame
entry+0x3C = (w >>  9) & 1;   entry+0x3D = (w >> 10) & 1;   // eye only: roll / fov offset from the joint record
// record +0x24 -> entry +0x30 and +0x26 -> entry +0x32: the joint number for modes 1 and 2
```

Slot 4 resolves actors through `02096504` and writes `020956D0`, and only when that slot is live.
Shipped words: `80008000` in 3,730 records (no attachment); 180 eye and 181 target attachments;
modes 1 and 2 in 39 / 67 records.

### 4.3 Array B — ease curves (`003CC5F0`)

```struct Cam7Curve base=record
+0x00  u32       length      0x18 + 0x24 * keyCount, all 15,350
+0x04  u32       keyCount    1-30
+0x08  f32       startTime
+0x0C  f32       startValue
+0x10  f32       endTime     the normaliser
+0x14  f32       endValue
+0x18  byte[36]  key0        repeated keyCount times, layout below
```

```struct Cam7CurveKey base=record size=0x24
+0x00  byte[16]  _unread     not read by 003CC5F0
+0x10  f32       a           cubic
+0x14  f32       b           square
+0x18  f32       c           linear
+0x1C  f32       d           constant
+0x20  f32       span        normalised; the spans of a curve sum to 1.0 in all 15,350
```

### 4.4 Array C — paths (`003CC740`, `003CC890`)

```struct Cam7Path base=record
+0x00  u16       length        0x20 + 0x38 * segmentCount + 8 * arcCount, all 1,682
+0x02  u16       _unread       0 in 1,679 -- not read by the evaluators
+0x04  u16       segmentCount
+0x06  u16       arcCount      10 * segmentCount + 1 in the common shapes; 0 in 47
+0x08  f32[3]    start         returned for param <= 0
+0x14  f32[3]    end           returned for param >= 1
+0x20  byte[56]  segment0      repeated segmentCount times, then arcCount 8-byte pairs
```

```struct Cam7PathSegment base=record size=0x38
+0x00  f32[4]    x           a b c d
+0x10  f32[4]    y           a b c d
+0x20  f32[4]    z           a b c d
+0x30  f32       span        parameter span
+0x34  f32       _unread     not read by 003CC740
```

Each arc pair is `{f32 distance, f32 param}`; the first is `(0, 0)` and the last param is 1.0 in
all 1,635 paths that have a table.

**Every curve and every path is referenced by exactly one timing or path word** (15,350 / 15,350,
1,682 / 1,682): the pools are not shared between shots or segments.

### 4.5 Runtime records

```struct ActorManagerSlotEntry base=record size=0x18
+0x00  u32       shot          the CAM7 record index from CML1 entry +0x04 (003DA456)
+0x04  i32       frame         0 main, 1 sub (clamped >= 0, not bounded above); indexes the frame-owner table
+0x08  u16       state         0 idle, 1 playing, 2 finished (003DA14E)
+0x0A  u16       entry         the CML1 entry number the script passed
+0x0C  f32       clock         frames since start, advanced by the tick
+0x10  f32       rate          1.0 at start; cameraratio
+0x14  u8        clockRunning  0 at start; 1 after the first positive step
+0x15  u8[3]     unread15      nothing observed reads or writes this span (unknown span, not padding)
```

The shake channels at `ActorManagerSlot +0x170` share this layout (builder `003DD230`)~~; their tick~~
~~is not read here~~. *(answered: see how-a-camera-reaches-the-renderer.md §4a, the shake chain; 2026-10-02, OPUS)*

```struct Cam7Player base=record size=0x2E0
+0x08  f32       segClock      time inside the current segment
+0x0C  f32       lastTime
+0x10  f32       delta
+0x14  u8[12]    unread14      not observed accessed; ends at the 16-aligned startPose block
+0x20  byte[64]  startPose     eye, target, roll, fov, follow scalars, polar form
+0x60  byte[64]  endPose       same layout
+0xA0  byte[52]  pose          eye +0xA0, target +0xB0, roll +0xC0, fov +0xC4, follow +0xC8..+0xD0
+0xD4  u8[12]    unreadD4      not observed accessed; ends at the 8-aligned lastKey
+0xE0  u64       lastKey       not reset between shots
+0xE8  u64       nextKey
+0xF0  f32[4]    eyeOffset     path
+0x100 f32[4]    targetOffset  path
+0x110 f32[4]    up            path-follow
+0x120 u32       followMode
+0x124 u32       absolute
+0x128 f32[13]   progress
+0x15C u8[13]    running
+0x169 u8[15]    unread169     not observed accessed; between the running array tail and stream   <- corrected 2026-10-02, OPUS - +0x16C / +0x170 are the cached yaw / pitch (00256960+0x19E, +0x305, +0x30D; 00256CA0+0x199, +0x287; section 7a)
+0x178 u64       stream        command pointer
+0x180 u32       state         1 running, 2 at the end marker
+0x184 i32       frame         -1 until a frame owns the channel
+0x188 u8        viewBuilder   debug verb only
+0x189 u8        eyeAttachSeen
+0x18A u8        targetAttachSeen
+0x18B u8[5]     unread18B     not observed accessed; ends at the 16-aligned eyeAttach matrix
+0x190 byte[64]  eyeAttach     matrix
+0x1D0 byte[64]  targetAttach  matrix
+0x210 byte[208] view          copied to camera record 5
```

**Two debug verbs write camera record 1 directly (added 2026-09-19, FABLE; four bodies read whole).** `0025A4A0`
(42 B) stores three floats and `w` = 1.0 at a camera record's `+0x00` - the **source eye** - and `0025A4D0` (43 B) does
the same at `+0x10`, the **source target**; both index `g_cameraRecords` by their first argument. Each has exactly
one caller, a script verb handler that pops three numbers and tail-jumps with **the record index fixed at 1**:
`0050E5B0` for the eye and `0050E530` for the target (83 B each). The handlers sit in the default dispatch table
`01F26720` at `result(0x13)` and `result(0x12)`, read by the accessor frame of
[the dispatch table](../../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md); the bundled catalogue's
family 2 names those ids **`debug_camerasrc`** and **`debug_cameradst`**. *No decompiled field script was searched
for them; they are debug verbs by name, and nothing else in the image writes those two fields this way.*

## 5. Call chain

```
script verb camerastart* (0034FE00 / 0034F930 / 0034F2F0)
  -> CameraChannels_Start 003DA400          reads CML1 entry +0x04 (the binding)
     -> CAM7_BindShotToChannel 00257230
per frame, per actor-manager slot:
  CameraChannels_Tick 003DA050
     -> CAM7_Evaluate 00258350  (or CAM7_RunToEnd 00257A00 on skip)
        -> 00255410 / 002554E0 / 00255E80 / kind handlers / 003CC5F0 / 003CC740
        -> view object +0x210
per frame:
  CAM7_PublishAll 002555D0
     -> CameraRecord_CopyViewState(5) 0025A2C0, CameraSystem_SetCameraActive(5)
        -> CameraSystem_SelectAndPublishActiveView 00259820 (highest active record wins)
```

**Upstream:** the zone or event script. **Owner transition:** `003DA400` — the one place a script
number becomes a shot. **Downstream:** camera record 5 and the sub-frame view.

**Do not confuse with:** the camera **shake** (`section_010`/`011`, `camerashakestart*`,
`003DD230`), which shares the channel layout but not this player; the behind (follow) camera verbs
(`lockbehindcamera`, `resumebehindcamera`), which feed lower records; the two other producers of
record 5 named in §2.8.

## 6. Modding notes

- **Best intervention point:** the data. A shot is fully described by its record, its curves and
  its paths; nothing in code special-cases a shot.
- **Which shot plays is `section_008`'s index column**, not the name (`BY-3`). Renaming a shot
  changes nothing; renumbering the column re-points the script.
- **A segment needs a key before it on the same channel.** A shot that begins with a segment
  borrows the previous shot's last key; on a fresh channel it faults (§2.4).
- **Curve spans must sum to 1.0** or the curve walk runs off the record (§2.5).
- **Kinds 5 and 6 are live code with no shipped user** — an authored path-follow shot would be the
  first exercise of `00256960` / `00256CA0`.
- **Multiplayer / XIIOnline:** everything here is derived from script and authored data and runs
  identically on every client; a mirror should never suppress it (the zone-script rule). The one
  local input is the frame step at `02B4E4B0`, so a desynchronised frame rate desynchronises the
  shot's progress, not its path.

## 7. What is not known

- [x] **BY-6.** What a path with no arc table produces. 47 of 1,682 paths have `arcCount = 0`, referenced by
      both word forms, yet both evaluators index the table. `BY-6`.
      **Narrowed 2026-09-14 (OPUS) — the mechanism is fully read, and half the premise is corrected:
      `003CC6C0`'s read is IN BOUNDS.** Layout from the bytes: a segment is **0x38** bytes
      (`imul r9, rax, 0x38`, `rax = word[rec+4]` = segment count `n`), the arc table starts at
      `rec + 0x20 + 0x38n`, and an arc entry is an **8-byte pair** — key at `+0x00`, value at `+0x04`.
      - **`003CC6C0`** indexes `7n + (m − 1)` with an 8-byte stride, so `m = 0` addresses `7n − 1`:
        the last 8-byte word of the last segment, **inside the record**. It multiplies `xmm1` by it.
        Not a fault — a defined read of the wrong field.
      - **`003CC890` is a binary search with two clamps**, and it is the one that leaves the record:
        it reads `arc[0].key` and returns **0.0** if that exceeds the query; compares against
        `arc[m − 1].key` and returns **1.0** (`01CEBBA8`) if the query exceeds it; else bisects. For
        `m = 0` that is `arc[0]` (the first 8 bytes **past** the segment table), `arc[−1]` (in bounds),
        and in the degenerate tail `arc[0].value` and `arc[1].value` — **three reads past the table
        and one inside it**.
      - So the pair is a distance-to-parameter remap clamped to [0, 1], and **a zero-arc path is not a
        handled special case — it is unguarded**: neither body branches on `m = 0`.
      - **Still open, and it is a DATA question:** what those bytes are for the 47 zero-arc paths.
        That needs the shipped array-C buffer; the executable cannot answer it.
      **ANSWERED 2026-09-27 (OPUS):** the bytes past a zero-arc record are the NEXT array-C record, because the loader keeps the section resident and points into it (`0025637C movzx eax, word [rbx]` / `add rbx, rax`). Over the 47 shipped zero-arc paths (the census extension reproduces its own 423 / 3,942 / 15,350 / 1,682 control): `arc[-1].key`, the last segment's `+0x30` word, is 1.0 in all 47, and `arc[0].key` is the next record's header read as a float, a positive denormal below 1e-30. So `003CC890` returns 0.0 for a query at or below about 0 and 1.0 above 1.0, and for 0 < q <= 1 it skips the bisect (`r10d = m - 1 = -1`) and returns the float32 line through `arc[0]` and `arc[1]` - the next record's header and its start-vector floats. At q = 1 that gives -1.42 to 10.53 over the 47 (median 0.040): 37 inside [0, 1], 9 negative, 1 above 1, and none equal to 1.0. So a zero-arc path's remap is a line set by unrelated bytes, not the path's parameterisation, and it reaches the end parameter only by the > 1.0 clamp. The tail reads FOUR words past the table, not three - `arc[1].key` at `003CC939` as well. Not claimed: how often play queries such a path or what the camera shows. Control `_index/candidates/by6-zero-arc-paths/by6_check.py`.
- [x] **BY-7.** ~~What attachment modes 1 and 2 compute (`002E7F10`, `002ED430` with the joint word)~~ —
      **answered 2026-09-15 (§11):** mode 1 is a joint-liveness probe, mode 2 a joint resolve-and-apply
      through `003A6DF0`/`00422050`. Still open: what the
      joint record's `+0x198` / `+0x194` values that bits 9 and 10 add to roll and fov are
      (`002ED130` → `002EA890` resolves the record; the field semantics are `002ED610`'s return type,
      outside the subtree). `BY-7`.
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): the "joint record" is a skeleton BONE record, and `+0x194` /
      `+0x198` are two of the three angles of the bone's added rotation.** So bit 9 subtracts the attached bone's third
      angle from the camera's roll, and bit 10 adds its second angle to the fov. Static.
      - **The record is a bone.** `002ED610` walks the actor's `0x740` record to its resource entry and returns element
        `word` of the `0x290`-byte array at the entry's `+0x84`. `0x290` is the skeleton bone-record stride. The image's
        other `imul …, 0x290` sites are all in the skeleton and motion code: `Skeleton_ComposeFinalPose`,
        `Skeleton_UpdateFinalPoseAndCombatLook`, `AddMotion_ApplyBonePose`, `RelationLook_ApplyBoneMatrices`, and
        others around them.
      - **The two fields.** `AddMotion_ApplyBonePose` stores an add-motion record's three angles, degrees converted to
        radians, at bone `+0x190` / `+0x194` / `+0x198`, and builds the bone's Euler rotation from them
        ([the ADM tables](../Model-And-Motion-Formats/adm-add-motion-tables.md) §10). Two other setters write the same
        three floats together.
      - **The camera reads them.** With bit 9 it takes `+0x198` (`002582FD`), and with bit 10 it takes `+0x194`
        (`0025830C`), each into its own out-value, which the root applies to roll and to fov.
      - **So a camera attached to a bone can have its roll and field of view driven by that bone's add-motion.** An
        angle keyed on the bone's third axis turns the camera, and one keyed on its second axis widens or narrows the
        view. `002ED610` is reached only through `002EA890` (a `jne`, found by the conditional-jump sweep), and that only
        from this root. Which cutscenes set bits 9 and 10 is a data question the executable does not answer.
- [x] ~~**BY-8.** The geometry of path-follow kinds 5 and 6 beyond their field reads — the three samples, the
      constant 5.0 at `00256B43`, and how `+0xC8`/`+0xCC`/`+0xD0` shape the aim.~~ `BY-8`.
      **ANSWERED 2026-09-15 (OPUS), both bodies read in full — §7a.**
      - **The three samples are one path at three positions**, `base ± {−1, 0, p}` from `[pose+0x08]`, the
        sign being the only difference in the sampling half: kind 5 adds, kind 6 subtracts.
      - **`+0xD0` is an output** — the interpolated progress `start + (end − start)·t`, published, not an
        aim input.
      - **`+0xC8`/`+0xCC` are an authored angular offset in the path's frame**: the forward vector is
        rotated by them first and by the path direction second.
      - **The 5.0 is a look-at distance** — the target is placed that far ahead of the eye along the aim
        (1.0 in kind 6), and the view builder takes a point and a direction. Whether anything reads the
        eye→target magnitude is NOT established, and it is the only way 5.0 versus 1.0 could show.
      - Kind 6 also aims flat (`Polar_FromPointsFlat`, pitch forced 0) and writes no up vector.
      - **No shipped segment uses either kind**, unchanged.
- [x] ~~**BY-9.** What the other two producers of camera record 5, `00257520` and `00255850`, are.~~ `BY-9`.
  **ANSWERED 2026-09-14 (FABLE): the two script-driven, eased camera blends.**
  - **`00257520` is the "resume behind camera" blend.**
    - Script verb `0x1E4` `resumebehindcamera` (`003442D0`, [the verb table](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv)) pops its floats and tail-jumps
      `003DA370`, which tail-jumps the starter `00257830` (`003DA3F8`).
    - The starter stores the duration `020963F8`, zeroes the elapsed time `020963FC`, selects a 64-byte source
      record from `02096370` (index `r9d`) into `020963F0`, and stores two modes, `02096400` and the easing
      `02096404` (`00257830`–`00257875`).
    - Per frame, while elapsed < duration, `00257520` takes the progress `elapsed / duration` through the easing
      `00256650` and blends the source record's position fields toward the live camera record (`002593A0`)
      (`00257583`–`00257618`). It wraps the yaw difference into `[−π, π]` (`00257654`–`00257691`).
    - Verb `0x1E5` `resumebehindcamerasync` (`003445E0`) polls completion through `00257800`, or advances the blend
      through `002578B0`.
  - **`00255850` is the "behind to event camera" blend,** the same machine on its own globals
    (`02096270`–`02096290`). Verb `0x34F` `behindtoeventcamera` (`00349FA0`) reaches the starter `00255C50` through
    `003DA300`. The sync verb `0x350` (`0034A530`) polls it through `00255CB0` / `00255C20`, and it uses the same
    easing function.
  - **The easing function `00256650`** maps progress `t`:
    - mode 0: `(sin(πt − π/2) + 1) / 2`, ease in and out;
    - mode 1: `sin(πt/2 − π/2) + 1`, ease in;
    - mode 2: `sin(πt/2)`, ease out;
    - any other mode: linear.

  So record 5 is shared by three producers: the scripted-camera players, and these two transitions between the
  behind camera and an event camera.

## 7a. Path-follow kinds 5 and 6, decoded — `BY-8` answered (OPUS, 2026-09-15)

**Both bodies read in full from the shipping image** at the authority hash
`73461d08…9721f8`, image base `0x120000`: `00256960` (828 B, kind 5) and `00256CA0`
(694 B, kind 6). Every address below is decoded from the bytes. **No shipped segment uses
either kind**, which §2.7 already records and this does not change.

**They are the same routine twice, and the differences are three.** Kind 6 samples the path in
the opposite direction, aims flat, and looks one unit ahead instead of five.

### The progress the section publishes — and what `+0xD0` is

```
p = pose.start + (pose.end − pose.start) · t      ; [+0x50], [+0x90], t = [+0x158]
[+0xD0] = p                                       ; 002569BF–002569CC (kind 5)
                                                  ; 00256CFF–00256D0C (kind 6)
```

**`+0xD0` is an output, not an input to the aim** — the interpolated progress, published for
whoever reads it, and kept in a local for the third sample below. That is the `+0xD0` half of
`BY-8`.

### The three samples: one path, three positions

The loop runs exactly three times (`r15 = 3`, `002569DD`), re-reading the **same** two key words
each time and stepping three deltas held in a local array at `rbp−0x79`:

| i | delta | kind 5 position | kind 6 position |
|---:|---|---|---|
| 0 | `−1.0` (`002569A6`, `00256CDE`) | `base − 1` | `base + 1` |
| 1 | `0` | `base` | `base` |
| 2 | `p` | `base + p` | `base − p` |

`base` is `[pose + 0x08]`. **Kind 5 adds the delta (`00256A01`, `00256A2D`); kind 6 subtracts it
(`00256D3A`, `00256D68`)** — the only difference in the sampling half, and it is what makes 6 the
reverse-facing follow.

Each sample takes two selector words from the key record:

- **`word[key + 4]` — the parameter.** Bit 15 set: index `& 0x7FFF` into the curve table at
  `[shot + 0x18]` and call `Curve_Evaluate` with `base ± delta` (`002569F6`–`00256A0A`). Bit 15
  clear: the word is a **count**, and the parameter is `(base ± delta) / count`, with a flag
  recording `count ≥ (base ± delta)` (`00256A1E`–`00256A3A`).
- **`word[key + 0x1E]` — the point.** Bit 15 set: index `& 0x3FFF` into the path table at
  `[shot + 0x20]` and call `Path_AtProgress` into the sample's 16-byte slot
  (`00256A61`–`00256A72`). Bit 15 clear: the slot is written `{0, 0, 0}` with `w = 1.0`
  (`00256A4E`–`00256A58`).

The three slots are the locals at `rbp−0x69`, `rbp−0x59` and `rbp−0x49`.

### The eye is the middle sample; the aim is a chord between samples

```
[+0xF0] [+0xF4] [+0xF8] = sample1            ; 00256AA6–00256AB6 / 00256DE1–00256DF1
```

Then, comparing componentwise (`ucomiss`, so a NaN takes the same branch as "different"):

| test | aim source |
|---|---|
| sample1 ≠ sample2 | **sample1 → sample2** (`00256B22`) |
| sample1 = sample2, sample0 ≠ sample2 | **sample0 → sample2** (`00256B1C`) |
| all three equal | **reuse the cached angles** and skip the polar call entirely (`00256AFE`–`00256B1A`) |

The degenerate arm is why the angles are cached at all: a stationary path would otherwise have no
direction to aim along.

### The 5.0, and how `+0xC8` / `+0xCC` shape the aim

`003CC130` `Polar_FromPoints` gives kind 5 **yaw, pitch and distance**; kind 6 calls
`003CC270` `Polar_FromPointsFlat` and gets **yaw only**, then passes **pitch = 0**
(`xorps xmm0` at `00256EBA`). That is kind 6's second difference: it is flat by construction.

Both then rotate fixed vectors twice — first by the pose angles, then by the path angles — through
the angle-pair rotation builder `003CC480(yaw, pitch, 0, &rot)` and the vector transform
`00202B70(dst, &rot, src)`. *(Neither callee is read here; they are named by their call shape and
by the roles §2.8 and the helper table already give them.)*

| | kind 5 | kind 6 |
|---|---|---|
| forward vector | `(0, 0, **5.0**)` (`00256B43`, `00256B5A`) | `(0, 0, **1.0**)` (`00256E8D`) |
| up vector | `(0, 1, 0, 1)` rotated with it (`00256B90`) | none |
| first rotation | pose `[+0xC8]` yaw, `[+0xCC]` pitch (`00256B4F`–`00256B98`) | same (`00256E66`–`00256E95`) |
| second rotation | the path angles | the path yaw, pitch 0 |
| target | `[+0x100]`/`[+0x104]`/`[+0x108]` = eye + rotated forward | same |
| up out | `[+0x110]`, 16 B (`00256C58`) | not written |
| cached angles | `[+0x16C]` yaw, `[+0x170]` pitch | `[+0x16C]` yaw only |

**So `+0xC8`/`+0xCC` are an authored angular OFFSET applied in the path's own frame**: the
forward vector is turned by the pose angles first and by the path direction second, so the shot
can look off-path by a fixed yaw and pitch while following it. That is the `+0xC8`/`+0xCC` half
of `BY-8`.

**And the 5.0 is a look-at distance, not a scale.** The target is placed five units ahead of the
eye along the aimed direction (one unit in kind 6), and §2.8's view builder takes eye, target and
the `+0x110` up vector — a direction and a point, where the magnitude cancels. **What is NOT
established:** whether anything downstream reads the eye→target distance itself, which is the only
way the 5.0 versus 1.0 difference could be observable.

### One dead computation, in both bodies

The per-sample flag from the count form is stored to `rbp−0x39`/`−0x35`/`−0x31`, and only the
middle one is read again: `neg` / `sbb eax, eax` / `and eax, 0x3F` at `00256C15`–`00256C32`
(kind 5) and `00256EE9`–`00256F06` (kind 6). **The result is never stored in either body.** It is
computed and discarded — recorded because a reader looking for what the flag gates will not find
a consumer here.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The command grammar, record lengths, key and segment layouts | complete bodies of `00258350` (dispatch `00258567`–`00258582`, key copy `00258930`–`002589AE`, segment advance `002588FD`–`00258923`), `00258AF0`; corpus census 3,942 / 3,942 | 1 |
| Timing words and ease curves | `00255410`, `003CC5F0` complete; census 15,350 curves, sizes and span sums | 1 |
| Path words and paths | `002554E0`, `003CC6C0`, `003CC710`, `003CC740`, `003CC890` complete; census 1,682 paths | 1 |
| Interpolation kinds | `00255E80` jump arms `00255F4B`–`00255FCC`; `00257B50`, `00258090`, `00257BF0`, `00257D10`, `00257E40`, `00257F60` | 1 |
| Attachment word | `002572E0` complete (`00257341`–`002574DB`); `00258190` field reads | 1 |
| Channels, frames and verbs | `003DA400`, `003DA050`, `003DA4D0`, `003DA570`, `003DA000`, `003DA2D0`, the verb handlers; verb table rows 0052–007F, 0114/0115, 033B/033C | 1 |
| Publication to record 5 | `002555D0`, `0025A3B0`, `0025A2C0`, `0025A500`, `0025A520`, `00259820` | 1 |
| `dst_a07` shot 2 follows shot 1 on channel 0 | decompiled `dst_a07` script, and its `CML1` indices 0–3 identity | 1 |
| `+0x188` only from the debug verb | the one writer `00257AA0`, its one caller `0050CD30` (`debug_cameraescape`, 0 shipped uses) | 1 |
| path-follow kinds 5 and 6: three samples at `base ± {−1,0,p}`, pose `+0xC8`/`+0xCC` as an angular offset, the 5.0 as a look-at distance, kind 6 flat and reversed | both bodies decoded from the image: `002569BF`–`00256C58` and `00256CFF`–`00256F09`; §7a | 1 |

Census: [`census.py`](../../_experiments/evidence/cam7-path-commands/census.py) →
[`census.out.txt`](../../_experiments/evidence/cam7-path-commands/census.out.txt), positive control
= the published section totals.

**Superseded readings:** `section_009` called record `+0x20`/`+0x22` "NOT read by the loader" —
true of `002561C0`, but `002572E0` reads them as the attachment word; it called `+0x28` `subCount`
— it is the first command's type byte; and it left the payload "not decoded" (`BY-1`).

## 9. Related

- [`section_009` — the `CAM7` camera table](../../25-EBP-Script-Container/Sections/section-009.md) — the file format and loader.
- [`section_008` — the `CML1` camera name list](../../25-EBP-Script-Container/Sections/section-008.md) — the index a script passes.
- [`section_010` — the shake name list](../../25-EBP-Script-Container/Sections/section-010.md) — the shake twin sharing the channel layout.
- [Character transform publish](../CONTRACT-character-transform-publish.md) — cites `CameraSystem_SelectAndPublishActiveView`.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

This page rests on two legs — 46 sized function bodies in the EXE, and a census over the shipped
script corpus. Both were re-derived from their own sources.

| claim | measured |
|---|---|
| the 46 stated body sizes in §3 | **46 of 46 exact** |
| 13 timing words at `+0x04`–`+0x1C` | `(0x1C − 0x04) / 2 + 1` = **13**, and `progress` at `+0x128 + 4i` spans `+0x128`–`+0x158`, `running` at `+0x15C + i` spans `+0x15C`–`+0x168` — all three agree on 13 |
| the corpus census | **reproduces exactly** — see below |

### The census reproduces from a corpus extracted in this session

Checking a page against the evidence file published beside it tests transcription, not the claim. So
**all 1,115 `us` `.ebp` containers were extracted from `FFXII_TZA.vbf` again** and
[`census.py`](../../_experiments/evidence/cam7-path-commands/census.py) re-run against them.

**Every number in [`census.out.txt`](../../_experiments/evidence/cam7-path-commands/census.out.txt)
came back identical**, including its own published control:

| | |
|---|---|
| control | **423 files · 3,942 records · 15,350 array-B curves · 1,682 array-C paths** |
| interpolation kinds `+0x24` | **0 → 3,406 · 1 → 116 · 2 → 57 · 3 → 67 · 4 → 8** |
| kinds 5 and 6 | **absent from the corpus entirely** — §2.7's "no shipped segment uses them" is a negative established over all 3,654 segments, not a sample |
| key `+0x38` | **7,609 of 7,614** at `1.0`, the other five at `0.0` |
| timing words | **32,152 plain frames · 15,350 curve references** |
| command streams | 3,942 of 3,942 parse as key/segment/end, `KSKE` 3,421 · `KE` 421, and **exactly one stream starts with a segment** (`dst_a07.ebp`) |

That is the strongest form this page's corpus claims can take: the same numbers out of a corpus this
session produced, against a control the census states in advance.

### The evidence artefact is not byte-reproducible, and should be (`BY-4`, new)

Re-running produced **three diffs against the published output, and every one is ordering, not
value**:

- `streams:` — the twelve entries are identical, but the count-1 tail comes back in a different order
  (`SKE` moves four places);
- `timing words: {…}` — `{'frames': 32152, 'curve': 15350}` versus `{'curve': 15350, 'frames': 32152}`;
- `path words … per slot` — the second slot's dict prints `none` and `path-unscaled` swapped.

All three are `Counter.most_common()` breaking ties by insertion order, and dicts printing in
insertion order. The counts never changed.

**This matters for an evidence artefact specifically.** A published `.out.txt` earns its keep by
being diffable against a re-run — that is what makes it evidence rather than a screenshot. As it
stands a reader who re-runs it sees three differences and has to check by eye that none of them is a
number, which is exactly the work the artefact exists to save. Sorting the tie-break (`sorted(c.items(),
key=lambda kv: (-kv[1], str(kv[0])))` in place of `most_common()`, and `sorted(d.items())` for the
plain dicts) makes the output byte-stable. **Routed to its author rather than edited here** —
`census.py` and its output are FABLE's.

> **Resolved 2026-09-13 (FABLE).** `census.py` now sorts every tie (`mc()`: count descending, then key
> text; `sd()`: dicts in key order) and walks the corpus in sorted directory order; `census.out.txt` was
> regenerated from it. Only ordering changed — every count is the one published before — and two
> consecutive runs are byte-identical. **The label in this heading is not a ledger id:** `BY-4` already
> names "the four camera channels per manager" in `OPEN-QUESTIONS.md`, so this item was handled as the
> ticket `OPUS-REQ-FABLE-BY4-CENSUS-STABLE` and registers no question.

**Not claimed:** nothing here was executed or observed live. The census was re-run, not rewritten, so
this confirms that `census.py` applied to the shipped corpus yields the published numbers — it does
not independently re-derive the record grammar that `census.py` encodes. The interpreter bodies
behind that grammar (`00258350`'s dispatch and the segment readers) were not re-read in this pass;
only their sizes were checked.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — CLIENT.** `BattleAction_FindApproachGeometryAroundTarget`, owned by that layer, calls `00203170` on this page. That caller is the approach-geometry search: a `0x160`-byte frame with a stack cookie, working from the caller's `[rcx]` and `[rcx+8]` pair; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — CLIENT (9 edges through 4 of this page's functions).** The Party layer reaches this page at `00265200`, `002671F0`, `0025A520`, `0025A500`. `FUN_00304180` is the worked example, read in full - it is a 639-byte pass that starts from selector `3` and abandons everything when either the lookup or the config query comes back empty; **3 of the 7 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Spawn_Encounter_Lifecycle — CLIENT.** `Spawn_TrySelectCandidatePosition`, owned by that layer, calls `00265200` on this page. That caller is the spawn candidate-position search, working in a `0x100`-byte frame with three saved SSE registers; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Movement — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 39 edges).** A scripted camera steers the
followed actor: the player bodies `002567E0`/`003CC970` call `0026E500` and `00230B60`, and
`00258350`/`003CC970` call `00230B60`. The inbound half is shared-accessor fan-in — locomotion
bodies (`PartyFollow_SolveFormation`, `BattleLocomotion_*`, `Navigation_*`) call this page's
`00203170`/`00265200`/`003CC130`/`003CC2F0` helpers — the camera's position queries are the same
accessors locomotion uses, not a second authority.

**Audio / CombatFormula / Rewards_Progression_Economy / Resource — SHARED HELPER (SWE2-FRONTIER
2026-09-15).** Two helpers the `00258190` subtree names are cross-lane shared callees, not
exclusive members: `00265020` (the root's mode-0 out-vector reader) is also called by Audio's
`00362850`, CombatFormula's `00384F40`, and Rewards' `002FB150`/`00312280`; `002ED570` (the
`00422050` entry fetch) is also called by Resource's `00409CA0`/`00409D60`/`00409F50`/`00409FE0`
family. The crossing is the shared helper itself — each layer consults the same bodies, and this
page owns nothing in those layers.
- **Input - CLIENT (2 edges).** `00263FF0` is called by bodies filed to Input: `00226BE0`, `002E09A0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (112 edges).** `00203170`, `00255C20`, `00255CB0`, `00257800` (+20 more) are called by bodies filed to Script_VM_Native_Bridge: `0033F7F0`, `0033FD60`, `00341AB0`, `00342490` (+71 more); `003442D0`, `00349FA0`, `0034E9B0`, `0034EDB0` (+13 more) reach bodies filed to Script_VM_Native_Bridge: VMValueStack_PopNumericDiscard (`00267DB0`), VMValueStack_PopInt32CoerceFloat32 (`00267E10`), VMValueStack_PushFloat32Bits (`00267F60`), VMValueStack_PushInt32 (`00267F90`) (+2 more) - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (12 edges).** `00203170`, Actor_GetWorldPosition (`00265020`), `00265200`, `002E9D10` are called by bodies filed to UI: `00247AE0`, `002729A0`, `00272B40`, `0027BED0` (+7 more) - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (1 edge).** `002556F0` is called by bodies filed to World: `00266D10` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (7 edges).** `0025A500`, `00362850` are called by bodies filed to WorldAreaField: WorldPersistence_ResetBanksForFieldTransition (`0026DB30`), World_UpdateSimulationTick (`00314020`); CameraRecord_CopyViewState (`0025A2C0`), `0025A3D0`, `00304180`, BattleUnit_ProcessDefeatRewardsAndLoot (`00312280`) (+1 more) reach bodies filed to WorldAreaField: FieldData_GetActiveFieldRecordBit15 (`00313F60`), FieldData_GetActiveFieldRecordBit15 (`00377C20`), `00377DB0` - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - MECHANICAL (8 edges).** all 8 edges are combat-AI bodies (`BattleEnmity_*` `00321850`/`00321B00`/`00321D30`, `BattleUnit_RebuildPerceptionCandidateCache` `003247F0`, `BattlePerception_RefreshCandidateCacheGeneration` `00324F20`, `003014C0` and two more) calling the shared accessors `00313F60`/`00377C20` - fan-in, not a per-caller relationship.
- **CoreRuntimeScheduling - CLIENT and SERVICE (6 edges).** core bodies `0022A0B0`, `0022A770`, `0022BC20` and `MainLoop_UpdateAndRenderFrame` (`0022B8C0`) call `00266D10`/`00314020`, while `00247AE0`/`002E09A0` reach `00229DA0`/`00229F00`.
- **Items_Equipment_Shops_License - MECHANICAL (2 edges).** both edges are item bodies (`00309FB0`, `0030FD10`) calling `FieldData_GetActiveFieldRecordBit15` (`00377C20`) - accessor fan-in.
- **Status_Periodic_Terminal - CLIENT (7 edges).** status bodies call this page's subjects: `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`) calls `Loot_FindOverlappingPickupIndex` (`002FB150`), `BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`) calls `00312280` and `00377C20`, `0030F690` calls `00377C20`, and `00320450`/`00329A20` call `00313F60`.
- **PlatformOnlineAchievements - SERVICE (2 edges).** `0022A770` reaches `00316930` and `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`) reaches `00316A50` - platform-layer calls on the rewards path.
- **RNG_Random_Selection - SERVICE (3 edges).** `0022A0B0` seeds `RNG_MT19937_Seed` (`00379CF0`); `AiOrder_EvaluateAndResolveActionTarget` (`003014C0`) reaches `BattleData_ResolveWeightedId` (`00308EC0`) and `RNG_SharedGameplayLCG_NextU32` (`00328370`).
- **Save_Load_Settings - CLIENT and SERVICE (3 edges).** `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (`00584210`) calls `RNG_MT19937_Seed` (`00379CF0`); `00266D10`/`0026DB30` reach `002EF2D0` and `SaveImage_GetPersistentPayloadBase` (`002EF2B0`).
- **Story_Event_Quest_Hunt - MECHANICAL and SERVICE (13 edges).** twelve persistent-flag bodies (`PersistentFlag_Query*`/`PersistentFlag_Set*`, the `0032A8A0`-`0032ADF0` block) call `SaveImage_GetPersistentPayloadBase` (`002EF2B0`) - fan-in on the payload-base accessor; `002EF2D0` also reaches `00379160`.

## 10. The `00258350` exclusive subtree — all 9 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns nine functions to `CAM7_Evaluate` (`00258350`), and every one
is already documented on this page — §2.5–§2.7 read each extent complete when the command grammar
was decoded. This section binds the census to those reads: each member was re-disassembled from the
shipping image for this binding, and each interior citation is an instruction inside the member's
declared extent.

| member | role (§) | interior |
| --- | --- | --- |
| `00255410` `CAM7_ComputeProgress` | 195 B — per-channel eased progress over the segment's 13 timing words (§2.5) | [`0025546A`](../../_index/ADDRESS-INDEX.md) |
| `002554E0` `CAM7_ComputePathOffsets` | 191 B — the two path words `+0x1E`/`+0x20`: bit-15 path-lookat vs bit-14 `Path_AtDistance` (§2.6) | [`0025554F`](../../_index/ADDRESS-INDEX.md) |
| `00256CA0` `CAM7_FollowPath6` | 694 B — kind-6 eye path-follow: samples the eye path and aims along it (§2.7) | [`00256E61`](../../_index/ADDRESS-INDEX.md) |
| `00257B50` `CAM7_LerpEye` | 156 B — kind ∉ {1,2} linear eye lerp (§2.7) | [`00257B65`](../../_index/ADDRESS-INDEX.md) |
| `00257D10` `CAM7_OrbitEyeFlat` | 304 B — kind-2 eye orbit in the horizontal plane (§2.7) | [`00257DCC`](../../_index/ADDRESS-INDEX.md) |
| `00257E40` `CAM7_TurnTarget` | 281 B — kind-3 target turn around the eye (§2.7) | [`00257F38`](../../_index/ADDRESS-INDEX.md) |
| `00257F60` `CAM7_TurnTargetFlat` | 304 B — kind-4 target turn in the horizontal plane (§2.7) | [`0025801C`](../../_index/ADDRESS-INDEX.md) |
| `00258090` `CAM7_LerpTarget` | 156 B — kind ∉ {3,4} linear target lerp (§2.7) | [`002580A5`](../../_index/ADDRESS-INDEX.md) |
| `003CC710` `Path_AtDistanceDirect` | 45 B — the bit-14 path-word form: `003CC890` resolve + `003CC740` sample (§2.6) | [`003CC720`](../../_index/ADDRESS-INDEX.md) |

Shared callees with other callers are excluded from the census — the ease/path family
`003CC5F0`/`003CC270`/`003CC480`/`003CC740`/`003CC890`/`003CC6C0`/`003CC3C0`/`003CC2F0`, the
dispatch helpers `00255E80`/`00258190`/`00257BF0`/`00256960` (cited elsewhere on this page),
`00202B70`/`00230B60`/`003CC000`/`003CC080`/`003CC970`, and the CRT `00808C40`/`00861F1A`.

## 11. The `00258190` exclusive subtree — all 6 members bound (SWE2-FRONTIER, followup queue)

`CAM7_BuildAttachTransform` owns **6 frontier functions** — the joint-word machinery its
`+0xC`-mode dispatch and bits-9/10 (`+0x20`/`+0x24`) field adds run. This answers most of **BY-7**:
modes 1 and 2 are the two ways a joint word becomes a transform source. Every member was
disassembled from the shipping image; interior cites are one instruction inside each extent.

| member | role | interior |
| --- | --- | --- |
| `002E7F10` (91 B) | **attach mode 1 — the joint-liveness probe**: `ctx+0xC0` context → `dword[+0] != -1` → `word[+0] != -1` indexes the `0x740`-stride record table at `022C6F28`; live iff `[rec+0x284]` is set and `00426770(rec)` returns non-null. Returns 1/0 | [`002E7F37`](../../_index/ADDRESS-INDEX.md) |
| `002ED430` (56 B) | **attach mode 2 — joint resolve + apply**: same `+0xC0`/`dword[+0] != -1` guard, then `003A6DF0(word[+0], out)`; returns whether the chain produced a record | [`002ED44D`](../../_index/ADDRESS-INDEX.md) |
| `003A6DF0` (107 B) | the word→record hop under mode 2: `word != -1` → `0x740`-record at `022C6F28` gated on `[+0x284]`, `00426650(rec, &obj, &word2)` resolves it, and a non-`0xFFFF` second word forwards to `00422050(obj, word2, out)` | [`003A6E03`](../../_index/ADDRESS-INDEX.md) |
| `00422050` (150 B) | the apply: `obj+0x18` index `!= -1` → `0020E600([+0x10])` resolves the container, `[container+0xD98]` + index → `002ED570` fetches the entry, then `003710E0` writes the transform out with a `{0, 0, 1.0f}` tail word | [`0042208A`](../../_index/ADDRESS-INDEX.md) |
| `002ED130` (70 B) | the bits-9/10 joint-word resolver the root calls under `+0x20`/`+0x24`: same `+0xC0`/`dword`/`0x740`-record/`+0x284` chain, tails `00421D70` for the record's word — returns `0xFFFF` on any dead link | [`002ED153`](../../_index/ADDRESS-INDEX.md) |
| `002EA890` (31 B) | the object hop after it: `ctx+0xC0` → `dword[+0] != -1` → tails `002ED610`, which resolves the word to the record whose `+0x194`/`+0x198` the root reads into the roll/fov outs | [`002EA8A1`](../../_index/ADDRESS-INDEX.md) |

~~What BY-7 still owes: the *meaning* of the resolved record's `+0x194`/`+0x198` fields~~ *(answered: see BY-7, answered 2026-09-26 - two of the three angles of the bone's added rotation; 2026-10-02, OPUS)* (the roll/fov
adds). `002ED610`'s return type is outside this subtree. `00426770`/`00426650`/`00421D70`/`002ED610`,
`0020E600`, `002ED570`, `003710E0`, `00265200`/`003CC480`/`00203170`/`00265020` and the CRT cookie
`00808C40` are shared callees — deliberately not census members.

## 12. The `003DA050` exclusive subtree — all 5 members bound (SWE2-FRONTIER, followup queue)

`CameraChannels_Tick` (`003DA050`, 302 B) owns the five small members §2.3's pseudocode
already names; this section binds the census with member-level reads. Every body was
re-disassembled from the shipping image; each interior cite sits inside the named extent.

The root is the per-frame sequencer for the four camera channels. It reads `[+0xD8]` and
returns early when null (`003DA072`), samples the skip flag through `00267300()`
(`003DA06A`), then runs two loops over the object's embedded tables:

- **Binding pass** (`003DA092`–`003DA0C3`): two u16 shot slots at `+0x18`/`+0x1A`; each
  non-negative shot `s` whose track-record mode word `word[+0x118 + s*0x18]` is nonzero
  gets `CAM7_SetPlayerFrame(slot = [+0x28], s, ch)` (`003DA0B5`).
- **Channel pass** (`003DA0E0`–`003DA15C`): four `0x18`-stride track records at `+0x110`
  (shot dword `+0x110`, mode word `+0x118`, clock float `+0x11C`, rate `+0x120`, latch
  byte `+0x124`). Mode 0 skips; mode 2 skips the advance. The tick delta is
  ~~`float[0264E4B0] × rate × float[01DFE0BC]`~~ `float[02B4E4B0] × rate × float[01DFE0BC]` *(corrected 2026-10-02, OPUS: `003DA050`+0xA3 `movss xmm1, dword ptr [02B4E4B0]`)* (`003DA0F3`–`003DA100`); once the latch byte
  is set the clock accrues it, and a positive delta sets the latch (`003DA0EF`–`003DA11A`
  — the clock therefore starts one tick after the rate first goes positive). The record is
  then evaluated: skip mode takes `CAM7_RunToEnd(slot, shot, ch)` (`003DA12C`), otherwise
  `CAM7_EvaluateSubmit(slot, shot, clock, ch)` (`003DA13A`). Finally
  `002567B0(slot, ch)` is re-queried and a return of 2 stamps the mode word to 2 —
  self-completing the channel (`003DA144`–`003DA14E`).

| member | role | interior |
| --- | --- | --- |
| `002555A0` `CAM7_EvaluateSubmit` (35 B) | arg-frame adapter: builds `{dword 0, qword 0, &out}` on the stack and forwards `(slot, shot, clock, ch)` to `00258350` | [`002555B9`](../../_index/ADDRESS-INDEX.md) |
| `002563C0` `CAM7_SetPlayerFrame` (35 B) | writes the channel index into the player array: `dword[slot×0xBB0 + shot×0x2E0 + 020929B4] = ch` — record `+0x184` | [`002563DE`](../../_index/ADDRESS-INDEX.md) |
| `00257A00` `CAM7_RunToEnd` (151 B) | the skip path: steps `002567B0(slot, shot)` until it returns 2, each step summing `CAM7_CurrentCommandLength` + `CAM7_PlayerClock` into the eval argument and calling `00258350` — a skip lands on the segment the running total reaches | [`00257A6A`](../../_index/ADDRESS-INDEX.md) |
| `00258AF0` `CAM7_CurrentCommandLength` (88 B) | reads the current command's type byte via `rec+0x178`: type 2 → its `+0x22` word (the segment duration), type `0xFF` → 0 (end marker), anything else → 1; a negative shot selects the default record at `02096520` | [`00258B3D`](../../_index/ADDRESS-INDEX.md) |
| `00258B50` `CAM7_PlayerClock` (51 B) | `float[player rec +0xC]` for `slot×0xBB0 + shot×0x2E0` at base `02092830`; a negative shot returns the default record's `float[0209652C]` | [`00258B72`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00267300` (the skip-mode query), `002567B0` (channel
status), `00258350` itself (root of the §10 subtree), `002E9D10` and the CRT cookie
`00808C40`. The player array's `[N][4]` geometry — `0xBB0` per slot, `0x2E0` per shot,
base `02092830` — is the same indexing §2.3 gives for `player[slot][shot]`.

## The `002572E0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`002572E0` = `CAM7_BindAttachments` (570 B): the shot table at
`02092800` is indexed `r14 + r12` (`002572F6`/`00257304`), record
`dword[rax+0x1C]` seeds `rdi` (`00257309`), `esi` mode dispatch vs 5
and 4 (`0025730F`/`00257350`), member `00257AD0` evaluates the
attachment (`00257359`, `0025738A`) with `dword[rdi+0x20]` the record
field (`00257341`), `002671F0` on `02096504` (`00257370`), result
stored `qword[rbx + rcx + 0x20]` (`00257363`/`00257396`) or `r15`
zero via `[020956D0]` (`0025739D`), and `byte[rbx+rax+0x34]`/`+0x36`
byte stores complete the entry (`002573B7`/`002573C9`).

| member | role | interior |
| --- | --- | --- |
| `00257AD0` (116 B) | the attachment evaluator — `00263C30` (`00257AEF`), `esi` = result (`00257AF6`) | [`00257AEF`](../../_index/ADDRESS-INDEX.md) |
| `00358960` (51 B) | indexed record byte getter — `00263FF0` (`00358969`), `ebx` vs `dword[rcx]` bound (`0035897D`), `rax = [rcx + rbx*8 + 8]` → `byte[rax+3]` (`00358981`/`00358986`) | [`00358981`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00263C30`, `00263FF0`, `002671F0`.
~~`00257AD0` is the same playhead evaluator `003DA050`'s track loop~~
~~calls — the camera-shot and attachment paths share it.~~ `00257AD0` finds the Nth kind-3 member and is not called by `003DA050` *(corrected 2026-10-02, OPUS: `003DA050`+0xDC calls `00257A00`; `00257AD0`+0x3A `cmp eax, 3`)*.


### Interior citation — frontier hub `003CC130` (2026-09-18, SWE2-EC7)

`003CC130` — 317 B, 13 callers: the delta-decompose the orbit rows invoke as
`003CC130(target, eye)` / `(eye, target)`. Read from the shipping image:
`d = b - a` per lane; `sqrtf` (`00861F14`) of the squared length lands in
`[rbx]` at [`003CC1BF`](../../_index/ADDRESS-INDEX.md); `atan2f`-family
`00861F02` over `(dz, dx)` then `(dy, dz)` produces the two angles stored to
`[rdi]` and `[rsi]`; `005068C0`/`00202B70` run the normalise pair mid-body.
Returns `(distance, yaw, pitch)` through the three out-pointers.

### Interior citation — frontier hub `00426770` (2026-09-18, SWE2-EC7)

`00426770` — 242 B, 8 callers: the two-hop linked-record property walk the
camera rows ride. `word[rcx]` (`-1` = none) resolves a `0x740` record off
`022C6F28`; `00421E20` reads its property page at
[`004267B7`](../../_index/ADDRESS-INDEX.md); then `word[+8]` and `word[+0xA]`
link fields are each followed through a second resolve, with `0042EF90`
invoked on `&0042DA00` + the out-block per live link. The chain the script
state hangs properties from.
## SWE2-EC7-22 update (2026-09-18) — the camera's curve/trig cluster

`003CC480` (359 B) is the three-angle trig composer: six alternating
`00861F0E`/`00861F08` calls (the LUT sin/cos pair) over `xmm6`/`xmm7`/`xmm8`,
staged into `xmm4`/`xmm9`/`xmm10`/`xmm11` — the rotation basis the camera
path builder assembles. Interior anchor `003CC4B8` (the first `00861F0E`).

`003CC2F0` (199 B) is the rotate+translate combine: cookie-prologue,
`call 003CC480` for the basis, then a staged `[rsp+0x20]` four-float record
through `00202B70`, `[rdi]`/`[+4]`/`[+8]` accumulated into `[rbx]` — the
local-to-world step the camera track applies. Interior anchor `003CC32D`.

`003CC5F0` (196 B) is the parametric segment evaluator: `[rcx+4] == 0` ->
`[r8] = [rcx+0x14]` ret 0; `xmm1` below `[rcx+8]` -> `[r8] = [rcx+0xC]` ret 1;
equal to `[rcx+0x10]` -> `[r8] = [rcx+0x14]` ret 1; else `divss` the
normalized `t` and walks the `[rdx+0x38]` segment table accumulating
`xorps xmm1` — the keyframe locator/interpolator behind the camera's scalar
curves. Interior anchor `003CC605` (the lower-bound load).

`003CC6C0` (72 B) is the weighted-index marshal: `(word[rcx+6]-1) +
word[rcx+4]*7` -> `r9`, `xmm1 *= [rcx + r9*8 + 0x20]`, `call 003CC890` then
tail `jmp 003CC740` — the element-select + two-call chain the curve
evaluators share. Interior anchor `003CC6E4` (the table multiply).

## SWE2-EC7-23 update (2026-09-18) — `003CC080`/`003CC000` vector-record initializers

`003CC080` (97 B) is the two-vector record writer: `[rdx]`'s four fields to
`[rcx+0x90..0x9C]`, `[r8]`'s four to `+0xA0..0xAC`, `xmm3` to `+0xC4`, `+0xC0 =
2` kind tag, tail `jmp 003CBD60` — the kind-2 variant of the camera's param
record initializers. Interior anchor `003CC082`.

`003CC000` (128 B) is the kind-3 sibling: the same two-vector copy plus `[r9]`'s
four fields to `+0xB0..0xBC` — the three-source record init. Interior anchor
`003CC002`. Both feed the `003Cxxxx` curve/cluster this page documents.

## SWE2-EC7-24 update (2026-09-18) — `003710E0` mode-1/2 parameter halver

`003710E0` (239 B) resolves `[rcx+0x84]` through `0020E600`, indexes `edx` by
`0x290` stride, and when `r9` supplies an output record: `edi-1` mode selects —
mode 1 (`[rsi+0x9C]==2` via `00373640`, else 0.0) adds `xmm0` to `[rbx]` then
halves `[rbx]`/`[rbx+4]`/`[rbx+8]`; mode 2 runs the same halve on the
`00373640` result alone. Interior anchor `0037110A` (the `imul 0x290`).
## SWE2-EC7-31 update (2026-09-18) — `0025A500` camera-mode setter

`0025A500` (21 B) is `CameraRecord_SetMode`, the writer the staged
commit names: `dword[020973F0 + ecx*0x110] = edx` — `ecx` picks the
0x110-stride record of the `020973F0` camera bank and `edx` lands
in its mode field, unguarded. Interior anchor `0025A511` (the
indexed store).

## SWE2-EC7-34 update (2026-09-19) - `00255850`

`00255850` (961 B) is the camera playback tick - a `comiss` gate on `02096270`/`02096274`, `020963F0` object, `ucomiss` zero check, `00256650`/`003CC130`/`003CC2F0`/`003CC080`/`002593A0`. Interior anchor `002558E8` (an `00256650` call).

## SWE2-EC7-39 update (2026-09-19) - `00409D60`

`00409D60` (431 B) is the Resource entry-removal path the page names - `0020E600` sextuple/`0020E620` quadruple plus `0051FE30`/`002ED570`/`003B37E0`/`00409730`/`0051FCF0` over `022C6F28`. Interior anchor `00409D79` (a `0051FE30` call).

## SWE2-EC7-40 update (2026-09-19) - `005068C0`

`005068C0` (380 B) is a scripted-camera body - `01CEBBA8`, `00861F0E`/`00861F08`. Interior anchor `005068FC` (an `00861F0E` call).

## SWE2-EC7-42 update (2026-09-19) - `003CC740`

`003CC740` (321 B) is `Path_EvaluateCubic` - call-free: `comiss` param against 0 and `01CEBBA8` (1.0f) clamps endpoints (three-dword copies to `r8`), else `movzx r10d, word[rcx+4]` walks `u16 n` cubic segments. Interior anchor `003CC781` (the segment-count read).

## SWE2-EC7-43 update (2026-09-19) - `002556F0`

`002556F0` (277 B) is `CAM7_InitAll` - `02092810`/`02096280`/`020963F8`/`020964F0`-`02096508`/`01CEBBA8` slot-clear quad, `003CBFF0`/`00861EC0`. Interior anchor `0025574F` (a `003CBFF0` call).

## SWE2-EC7-43 update (2026-09-19) - `002555D0`

`002555D0` (279 B) is a scripted-camera body - `02092A40`/`02095874`/`02096290`/`02096410`, `00255850`/`00257520`/`0025A2C0`/`0025A3B0`/`0025A500`/`0025A520`. Interior anchor `0025562B` (a `00255850` call).

## SWE2-EC7-44 update (2026-09-19) - `003CC970`

`003CC970` (253 B) is a scripted-camera player body - `debug_cameraescape`-gated per the page, `00230B60`/`0026E500`/`003CBD60`/`00808C40`. Interior anchor `003CC9A2` (a `00230B60` call).

## SWE2-EC7-46 update (2026-09-19) - `0025A2C0`

`0025A2C0` (235 B) is `CameraRecord_CopyViewState` (camera record 5) - `00377DB0` single call; records at `02097300` per the page. Interior anchor `0025A359` (the `00377DB0` call).

## SWE2-EC7-47 update (2026-09-19) - `003CC890`

`003CC890` (218 B) is `Path_DistanceToParam` - call-free arc-table binary search + lerp: `word[rcx+4]`*0x38 base, `word[rcx+6]` count, `+0x20`/`+0x24` float pairs. Interior anchor `003CC8D2` (the search loop head).

## SWE2-EC7-48 update (2026-09-19) - `0025A3D0`

`0025A3D0` (207 B) is a camera-record sibling - `00377DB0` single call. Interior anchor `0025A456` (the `00377DB0` call).

## SWE2-EC7-49 update (2026-09-19) - `002566E0`

`002566E0` (193 B) is `CAM7_ResetSlot` - clears one `(slot, channel)` player: `003697F0`/`003CBFF0`/`00861EC0`. Interior anchor `00256728` (a `003697F0` call).

## SWE2-EC7-51 update (2026-09-19) - `003CC3C0`

`003CC3C0` (178 B) is a body - `00202B70`/`003CC480`/`00808C40`. Interior anchor `003CC3F8` (a `00202B70` call).

## SWE2-EC7-54 update (2026-09-19) - `0051FCF0`

`0051FCF0` (308 B) is the camera-player body the lifetime page orders - `0020E620`/`003AB7F0`/`0051F880`. Interior anchor `0051FD13` (a `003AB7F0` call).

## SWE2-EC7-55 update (2026-09-19) - `0051F880`

`0051F880` (357 B) is a camera-player body - `003AB7F0` single call. Interior anchor `0051F89E` (a `003AB7F0` call).

## SWE2-EC7-56 update (2026-09-19) - `003B37E0`

`003B37E0` (197 B) is the `003B37E0(id)` pre-`00409730` call the camera-player page orders - `0024F410`/`0024F4D0`/`003B39E0` plus `02EBCD80`/`02EBDB80`-`02EBDB90`. Interior anchor `003B3817` (a `0024F4D0` call).

## SWE2-EC7-57 update (2026-09-19) - `003B39E0`

`003B39E0` (183 B) is the `003B39E0(id)` management-record recycle the camera-player page names - call-free `0x38`-stride slot unlink relinking `[rcx+0x20]`/`[rcx+0x28]` and the `02EBDB98`/`02EBDBA8`/`02EBDBA0` heads. Interior anchor `003B3A2C` (the `+0x20` unlink).

## SWE2-EC7-61 update (2026-09-19) - `00230B60`

`00230B60` (154 B) is the mode-1 hit-check probe the scripted-camera page names - `0022F430`/`00808C40` plus `01F44830`. Interior anchor `00230BD8` (a `0022F430` call).

## SWE2-EC7-62 update (2026-09-19) - `0022F430`

`0022F430` (1021 B) is the scripted-camera body the probe wraps - `0022D0D0`/`00233050`/`0026E500`/`00808C40`/`00861F14` plus one vcall, `008C5F6C`/`00900308`/`00908DF8`/`00908E18`. Interior anchor `0022F461` (a `0026E500` call).



## SWE2-EC7-63 update (2026-09-19) - `0022D0D0`

`0022D0D0` (987 B) is a scripted-camera body - `00861F14` single call plus `01CEBB60`/`01CEBBA8`/`01CEBC9C`/`01CEBDA0`. Interior anchor `0022D191` (a `00861F14` call).



## SWE2-EC7-63 update (2026-09-19) - `00256650`

`00256650` (144 B) is the camera state-writer callee - `00861F0E` single call plus `008C5F70`/`01CEBB70`/`01CEBBA8`/`01CEBC50`. Interior anchor `002566A1` (a `00861F0E` call).



## SWE2-EC7-63 update (2026-09-19) - `002ED610`

`002ED610` (144 B) is a scripted-camera field-semantics body - `0020E600`/`002ED570` plus `022C6F28`. Interior anchor `002ED653` (a `0020E600` call).



## SWE2-EC7-65 update (2026-09-19) - `00373640`

`00373640` (136 B) is a scripted-camera mode-1 body - `0020E600`/`00409270` (`[rsi+0x9C]==2` gate, `xmm0` add to `[rbx]`). Interior anchor `0037366F` (a `0020E600` call).



## SWE2-EC7-65 update (2026-09-19) - `00349FA0`

`00349FA0` (134 B) is the `behindtoeventcamera` verb `0x34F` body - `002640C0`/`00267DB0`/`00267E10`/`003DA300` plus `01DFE0B8`. Interior anchor `00349FBC` (a `002640C0` call).


## SWE2-EC7-87 update (2026-09-20) - `003CC270` distance-angle pair measured

`003CC270` (114 B) is the polar pair the camera callers run:
`[rdx+8]-[rcx+8]` and `[rdx]-[rcx]` give the two deltas;
`00861F14(dx^2 + dz^2)` writes the distance to `[r9]` and
`00861F02(dx, dz)` writes the angle to `[r8]`.
Interior anchor `003CC2B5` (the `00861F14` call).

## SWE2-EC7-93 update (2026-09-20) - `00372800` kind-2 gate measured

`00372800` (18 B) is the kind gate `00421D70` runs before the camera
work: `[rcx+0x9C] == 2` tails `003737C0`; anything else returns -1.
Interior anchor `00372807` (the `je` into the tail arm).

## SWE2-EC7-105 update (2026-09-20) - `002567B0` measured

`002567B0` (46 B) is the two-dimensional
indexed read `00257A00` and `003DA050`
call: `edx >= 0` answers
`dword[020929B0 + ecx * 0xBB0 + edx * 0x2E0]`
- outer stride `0xBB0`, inner stride
`0x2E0` - while `edx < 0` answers
`dword[020966A0]` - the
camera-table / fallback-default split the
player consults.
Interior anchor `002567B7` (the `0xBB0`
multiply).

`00217060` (235 B) is the vec4-by-mat4 multiply `00202B70` runs: `r8`'s four floats are each `mulss`-paired against one column of the `rdx` 4x4 (`+0`, `+0x10`, `+0x20`, `+0x30` for `x`; `+4`/`+0x14`/`+0x24`/`+0x34` for `y`; `+8`/`+0x18`/`+0x28`/`+0x38` for `z`; `+0xC`/`+0x1C`/`+0x2C`/`+0x3C` for `w`), the four sums landing in `[rcx]`..`+0xC` - the call-free transform product the camera player applies.

Interior anchor `00217075` (function `00217060`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-scripted-camera-player-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00255C20` | 40 B | returns 1 when float `02096274` is at least float `02096270` (`comiss`) or float `02096270` equals 0.0, else 0 (also when `02096270` is NaN) | `00255C28`, `00255C30`, `00255C38`, `00255C42` |
| `00255C50` | 92 B | stores the fifth (stack) argument at dword `0209627C`, `ecx` at `02096284`, `edx` at `02096280`, `r9d` at `02096278`, the float `xmm2` at `02096270`, 0.0 at `02096274` and word 0 at `02096360`; calls `003CBFF0(02096290)` and stores the address `02096370` in qword `020963F0` | `00255C5B`, `00255C77`, `00255C7F`, `00255C94`, `00255CA0` |
| `00255CB0` | 53 B | returns without work when float `02096274` is at least float `02096270` (`comiss`) or `02096270` equals 0.0; otherwise stores float `02096270` minus 1.0 (`01CEBBA8`) at `02096274` and tail-jumps `00255850` | `00255CC0`, `00255CC8`, `00255CCF`, `00255CD7`, `00255CDF` |
| `00257800` | 40 B | returns 1 when float `020963FC` is at least float `020963F8` (`comiss`) or float `020963F8` equals 0.0, else 0 (also when `020963F8` is NaN) | `00257808`, `00257810`, `00257818`, `00257822` |
| `002578B0` | 53 B | returns without work when float `020963FC` is at least float `020963F8` (`comiss`) or `020963F8` equals 0.0; otherwise stores float `020963F8` minus 1.0 (`01CEBBA8`) at `020963FC` and tail-jumps `00257520` | `002578C0`, `002578C8`, `002578CF`, `002578D7`, `002578DF` |
| `00257AA0` | 35 B | stores the byte `r8b` at `020929B8` plus sign-extended `ecx` times `0xBB0` plus sign-extended `edx` times `0x2E0` | `00257AA3`, `00257AAD`, `00257AB4`, `00257ABE` |
| `0025A3B0` | 24 B | tail-jumps `0025A2C0(edx, r8)` when `ecx` is zero, otherwise `0025A3D0(r8, edx)` | `0025A3B2`, `0025A3BB`, `0025A3C3` |
| `0025A4A0` | 42 B | indexes the `0x110`-byte records at `02097300` by sign-extended `ecx` and stores the floats `xmm1`, `xmm2`, `xmm3` at `+0`, `+4`, `+8` and the dword `0x3F800000` (1.0) at `+0xC` | `0025A4A3`, `0025A4AA`, `0025A4B4`, `0025A4BD`, `0025A4C2` |
| `0025A4D0` | 43 B | indexes the `0x110`-byte records at `02097300` by sign-extended `ecx` and stores the floats `xmm1`, `xmm2`, `xmm3` at `+0x10`, `+0x14`, `+0x18` and the dword `0x3F800000` (1.0) at `+0x1C` | `0025A4D3`, `0025A4DA`, `0025A4E4`, `0025A4EE`, `0025A4F3` |
| `00341AB0` | 99 B | passes the float `00267DB0(r9)` returns through `003A1C50`, calls `0026C090(rdx, value)` and `0026C290(rdx, 00265200(rdx))`, stores the value as a float at `[r8]` and tail-jumps `0026C120(rdx, 3)` | `00341ACD`, `00341ADB`, `00341AEE`, `00341AF8`, `00341B0E` |
| `003445E0` | 48 B | calls `00267310(byte +0x15 of rdx)`; when that is non-zero calls `002578B0()` and returns 0, otherwise returns 1 when `00257800()` returns 0 and 0 when it returns non-zero | `003445E4`, `003445E8`, `003445F1`, `003445FD`, `00344606` |
| `0034A530` | 48 B | calls `00267310(byte +0x15 of rdx)`; when that is non-zero calls `00255CB0()` and returns 0, otherwise returns 1 when `00255C20()` returns 0 and 0 when it returns non-zero | `0034A534`, `0034A538`, `0034A541`, `0034A54D`, `0034A556` |
| `00350660` | 59 B | calls `00267F90(r9, 0)`, then tail-jumps `003DA4D0(002640C0(), 00267E10(r9))` | `00350672`, `00350677`, `00350682`, `00350696` |
| `00350B00` | 73 B | calls `002640C0()`, then pops a float with `00267DB0(r9)` and an int with `00267E10(r9)`, and tail-jumps `003DA2D0(first result, int)` with the float in `xmm2` | `00350B12`, `00350B1D`, `00350B28`, `00350B2D`, `00350B44` |
| `00351190` | 109 B | converts the int `00267E10(r9)` to float (`cvtdq2ps`), calls `00267F90(r9, 0)` and `00267F60(r9, that float)`; then calls `002640C0()`, pops a float with `00267DB0(r9)` and an int with `00267E10(r9)` and tail-jumps `003DA2D0(002640C0 result, int)` with the popped float in `xmm2` | `003511A5`, `003511B3`, `003511C1`, `003511D1`, `003511F8` |
