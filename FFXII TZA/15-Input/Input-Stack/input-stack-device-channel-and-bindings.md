---
system: Input stack — device, channels and bindings
category: 15-Input
status: DOCUMENTED — all eight registered residues are answered (AP-4..AP-6, SD-5..SD-9); SD-7 closed statically (2026-09-30, SWE2-STRUCT for OPUS: GameApplication slot 15 is called nowhere, so the +0x39 poll gate is set only by 001989D0), the page's residue prose carried by SWE2-CONTRACT's DD batch 19 (owner re-status 2026-10-01, OPUS; documented_rule READY).
owner_layer: PrimaryOwner:Input
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `0032C650`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 7
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# Input stack — device, channels and bindings

> Three layers between a button and the game: the device state, a per-frame channel with **sixteen
> frames of history**, and a rebindable keymap loaded from an `.ini`.

~~**PARTIAL.**~~ *(Superseded 2026-10-01, OPUS: the status line reads DOCUMENTED and every residue named below is answered.)* The three families, their call structure, the channel record's shape and the history
ring are read. ~~Most individual bodies are not, and the binding format itself is not decoded.~~
*(Corrected 2026-09-30, SWE2-DATA: the binding format is decoded (AP-5, 2026-09-08), and the poll, the three
channel builders, the bridge and the keyboard path are read (§2, §5). What stays open is registered as SD-5 to
SD-9.)* *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19): all five have answers now. SD-5, SD-6, SD-8 and
SD-9 are ANSWERED 2026-09-30 (OPUS). SD-7 is answered by the record published in `59ec09a95`, and its register row
is not yet restated. See §5.)*

## 1. What the player sees

Rebinding a control in the options menu, a held direction repeating at a steady rate, an analog stick
that ignores a small nudge, and a controller that rumbles — all four are this stack, and they are
three separate layers doing three separate jobs.

The one a player would never guess: the engine keeps **sixteen frames of input history per channel**,
not just the current frame. Anything that needs to know what you pressed *recently* rather than
*now* reads backwards through that ring.

## 2. Native mechanism

### Three families, 49 functions

| Family | Functions | Bytes | Job |
|---|---:|---:|---|
| `InputBackend_*` | 7 | 4,079 | resolved **device** state, per bank |
| `InputControl_*` | 28 | 5,116 | per-frame **channels**, history, repeat, feedback |
| `InputManager_*` | 14 | 6,065 | **keymap and bindings** |

### The manager: keymap in, control state out

```
InputManager_CreateSingleton
  -> Initialize
       -> BuildKeymapPath
       -> LoadKeymapIni                     (1,644 B — the largest in the family)
       -> RestoreDefaultBindingProfiles
       -> MaterializeRuntimeBindingProfiles
       -> ValidateBindingIdRanges
       -> ValidateBindingUniqueness

InputManager_PollAndBuildControlState
  -> RefreshBoundControlCodeBackendStates -> Backend_CopyControlCodeState130To30AllBanks
  -> TranslateBindingProfileToControlState (1,406 B)
       -> Backend_GetFilteredAnalogAxisValue
       -> Backend_IsPrimaryControlCode1To3Active
       -> Backend_IsControlCode11To27ActiveAnyDevice
       -> Backend_IsControlCode28To283ActiveForBank
```

**Bindings are loaded from an `.ini` file, validated twice** — once for id range, once for
uniqueness — and defaults are restored before the runtime profiles are materialised. A binding that
fails either check does not reach the runtime.

`InputManager_GetSingleton` has **46 callers outside these families**: it is the engine's front door
to input.

### Control codes come in three bands

The three backend predicates split the code space, and their names give the boundaries:

| band | query |
|---|---|
| **1 – 3** | `IsPrimaryControlCode1To3Active` |
| **11 – 27** | `IsControlCode11To27ActiveAnyDevice` — *any* device |
| **28 – 283** | `IsControlCode28To283ActiveForBank` — a **specific** bank |

The middle band is checked across all devices while the upper band is per-bank, so the same physical
control means different things depending on which range its code falls in. What distinguishes the
bands is established as of 2026-09-02 — see AP-1 in §7 and the corrected 28–152 bound.

### The channel layer keeps sixteen frames of history

```
InputControl_UpdateFrame
  -> UpdateRegisteredChannels
       -> GetRegisteredChannelUpdateMode
       -> AdvanceChannelTimingState
       -> CarryForwardHistoryWithAvailabilityState
       -> UpdateChannelByIndex -> PollAndBuildChannelHistory
            -> ConvertButtonMaskToTransitions       -> FilterTransitionMaskWithRepeatState
            -> NormalizeAnalogAndComputeTransitions -> FilterTransitionMaskWithRepeatState
            -> UpdateDeviceFeedbackOutput
```

`GetHistoryLookbackCount` gives the stride in five instructions:

```c
return *(byte *)(0x022CAE98 + channel * 0x294);      /* = record + 8 */
```

*(Its base is eight bytes above the one the other nine accessors use — see section 10.)*

and the accessors add the rest:

```
channel record @ 0x022CAE90 + channel * 0x294      (660 bytes, 2 channels)
  +0x01        byte    ring cursor
  +0x08        byte    history lookback count
  +0x44        history ring: 16 frames x 36 bytes

  frame +0x00 .. +0x03     4 bytes    header: +0x00 channel index, +0x02 raw mask        (AP-9)
  frame +0x04 .. +0x13     8 x u16    mask fields  (GetHistoryMaskOffset04..12)
       +0x04,+0x06,+0x0C,+0x10        written by BOTH transition builders
       +0x0E,+0x12                    written by the analog builder only
       +0x08,+0x0A                    written by the repeat filter 0035FBD0 (AP-8)
  frame +0x14 .. +0x23    16 bytes    one byte per button, written by the poll 0035F420 (AP-9)

  36 bytes per frame;  0x44 + 16*36 + 16 = 660 = 0x294   — exact
```

*(Corrected 2026-09-30, SWE2-DATA: this block read `+0x08,+0x0A written by NEITHER (AP-8)`,
`+0x14 .. +0x1B 8 bytes analog values (analog builder)` and `+0x1C .. +0x23 8 bytes unaccounted (AP-9)`. AP-8 and
AP-9 were answered on 2026-09-12 (§5): the repeat filter writes `+0x08` / `+0x0A`, and the poll writes sixteen
per-button bytes at `+0x14`–`+0x23`. The full record is in §3a.)*

channels: 2 (every accessor tests `cmp ecx, 2 ; jl`); ring: 16 frames, index wrapped with
`ecx & 15` after adding the caller's lookback to the cursor. Section 8 derives this from the
accessors' indexing arithmetic; an earlier revision placed the mask offsets in the record header
rather than inside a frame.

So: **two channels, sixteen frames deep, eight mask fields per frame.** A lookback of *n* reads
`cursor + n` wrapped into 0–15 — negative lookbacks are folded up by the `+0x10` adjustment, so
reading backwards past the start of the ring wraps rather than failing.

`GetHistoryAnalogByteByIndex` returns **`0x80`** for an invalid channel. `0x80` is the midpoint of a
byte, which is the natural neutral for an unsigned analog axis — *that reading is an inference from
the value, not from a comment* (**AP-2**).

### Transitions and repeat

Button state becomes **transitions** (`ConvertButtonMaskToTransitions`) and analog becomes
transitions after normalisation (`NormalizeAnalogAndComputeTransitions`, 856 B). **Both** then pass
through `FilterTransitionMaskWithRepeatState` — one repeat filter serving digital and analog alike,
which is why a held stick direction repeats like a held button.

`InputControl_AdvanceChannelTimingState` carries the timing constants **16384, 1760, 1790, 180, 546**;
which of them are thresholds and which are rates is established as of 2026-09-02 — see AP-3 in §7.

### ~~The two stacks do not meet~~ The two stacks meet through a bridge

`InputManager_*` and `InputControl_*` share **no call edge in either direction**. ~~The manager reaches
the backend directly; the channel layer reaches the backend through its own path. They are two
consumers of one device layer, not a pipeline. Whether one is legacy is open (**AP-4**).~~

**AP-4 ANSWERED 2026-09-13 (FABLE): they are one pipeline, joined through a bridge — which is why no direct edge exists.** `InputControl_PollAndBuildChannelHistory` `0035F420` initialises a device-slot index (`InputBridge_InitializeDeviceSlotIndexInvalid` `00862660`) and hands **its own buffer `022CB680`** to `InputBridge_PollControlState` `00862670` (`0035F45B`–`0035F467`), an 8-byte shim that jumps to `InputAPI_PollControlState` `001E09B0`, which fetches `InputManager_GetSingleton` and tail-jumps into **`InputManager_PollAndBuildControlState` `00196FF0` with that buffer** (`001E09B9`–`001E09D3`). The manager fills the channel layer's control state by pointer — so the two families share no global either (a capstone census of their rip-relative `.data` operands finds 0 addresses shared between them among the 76 that the `InputManager_*`, `InputControl_*` and `InputBackend_*` families touch). The second bridge call, `00862680` → `001E09E0` with `022CB6C0` (`0035F46C`–`0035F473`), fetches the singleton and ends in the folded `ret 0` `0016D6A0`: that input is no longer supplied. Feedback runs the same bridge the other way: `InputControl_UpdateDeviceFeedbackOutput` `0035F590` → `InputFeedbackBridge_DispatchTwoBytePair` `008628F0` → `InputFeedback_DispatchViaManagerGate` `001E1120` → `InputManager_DispatchFeedbackToDeviceById` `00198E80`. **The dependency is one-directional:** a direct-call walk from `InputManager_*` visits 357 functions to depth 8 and reaches no `InputControl_*` body, while `InputControl_*` reaches `InputManager_*` in three hops. So `InputControl_*` is the game-facing channel layer (history, transitions, repeat, feedback) and `InputManager_*` the PC binding / device layer beneath it; neither supersedes the other. The bridge functions sit together at `00862600`–`008629C0`, among other small adapters whose callers are game code.

### The keyboard byte array: who writes it, and when the keyboard is polled (2026-09-13, FABLE)

*Read for ASTRA-REQ-FABLE-TITLE-KEYBOARD-POLL. Runtime work reads the keyboard through
`*(02EA5368) → +0xDF8 → +0x118 → +0x30`; this section names each link and the code behind it.*

**The objects.** `[02EA5368]` is the Phyre application object (constructor `00792350`, which stores it at `00792550`),
not the input manager — `InputManager_GetSingleton` returns `[01F7FFE0]` (`00198790`). Its `+0xDF8` is the input backend
(the `this` of `InputBackend_UpdateResolvedDeviceState` `007A2440`). `FUN_0079E3D0` fills the backend's `+0x118`–`+0x148` with the first seven
registered devices whose kind method (vtable `+0x08`) returns 1 (`0079E411`–`0079E45A`). Kind 1 is
`PFramework::PInputDeviceKeyboard` (vtable `01CB2430`, `0x338` bytes, constructor `007927C0`). `007973D0` creates it:
`CreateDevice`, `SetDataFormat` with `01CC7150` (256 objects, 256 data bytes), `SetCooperativeLevel(hwnd [02EA5248], 6)`
(`00797410`–`00797420`; `6` = `DISCL_NONEXCLUSIVE | DISCL_BACKGROUND`), then `Acquire`. **Window focus therefore does not
gate the keyboard read.**

**Three 256-byte arrays in the keyboard object, three writers:**

| offset | meaning | written by |
|---|---|---|
| `+0x231` | **the polled level**, one byte per key | `DirectInputKeyboard_PollState` `007A1640` (slot 5): `GetDeviceState(256)` into a stack buffer, then `level[i] = remap[i] != 0 && state[remap[i]] & 0x80` (`007A1712`–`007A1758`), then `InputDevice_FinalizeButtonTransitions` |
| `+0x130` | the level as of the previous backend pass | `FUN_0079D010` (`0079D08E`), every pass, for every key |
| `+0x30` | **a transition latch** — the byte every game-side keyboard query reads | `FUN_0079D010` (`0079D079`) when the level differs from `+0x130`. It also calls the application's vtable `+0xC8` with `edx = 0` to report the change. |

`remap` is the table at `01F3DAB0`: index → DirectInput key code (`DIK_*`, 124 non-zero entries). Index 0 = `0x1E` `DIK_A`,
36 = `0x01` `DIK_ESCAPE`, 49 = `0x1C` `DIK_RETURN`, 65 = `0xC8` `DIK_UP`, 80 = `0x48` `DIK_NUMPAD8`.
**The array follows the scan code, not the virtual key.** `EXP-006`'s "Up → code 108" is index 80, `DIK_NUMPAD8`: the
non-extended scan code `0x48` its `SendInput` carried, where `DIK_UP` would be index 65. On a failed `GetDeviceState`, the poll
zeroes `+0x231`, `+0x30` and `+0x130` and clears `+0x230` when the application's `+0x58` is 0 (`007A169F`–`007A16E2`). It then
retries `Acquire` while the result is `0x8007001E` (`DIERR_INPUTLOST`).

`FUN_0079D010` runs from `PApplication` slot 28 `0079C140` (`0079C260`), only when the application bytes `+0x1E`, `+0x1F`,
`+0x20`, `+0x21` and `+0x29` are all zero (`0079C240`–`0079C257`). Those are one-shot display requests: the same function
services them and clears them later in the pass (`0079C4AB`–`0079C5BF`). Whether one can stay set across frames is not read.
*Registered 2026-09-30 (SWE2-DATA) as **SD-5**, static.* *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19):
SD-5 is ANSWERED 2026-09-30 (OPUS `ce2b4380d`, [record](../../_index/candidates/sd5-display-requests-0930/README.md)).
Only a failed resize leaves a display request set. See §5.)*
The same loop covers the 18 pad slots at `+0x88` for codes 11–27 (previous level at `+0x41`) and the mouse at `+0x150`.

**Who reads `+0x30`, and who clears it.** `InputBackend_IsControlCode28To283ActiveForBank` `0079E6A0` is a read
(`cmp byte [rax+rcx+0x30], 0`, `0079E6C0`). Its callers are the binding translator `00197160` (four sites), `0017DDC0`,
`0017DE10`, `0017DEA0` (three sites), `0017DFC0`, `001E0E70`, and a tail jump from `00197990`. Two functions clear the byte
and return whether it was set:
- `InputBackend_ClearControlCodeState30ForBank` `0079AE90`, called by `0017DE60`, `00196C40`, `00196DF0`, `00196EE0` and `001EC060`
- `FUN_0079AE40`, called by `001E0920` (which clears codes 28–152) and `001E0C50` (which clears the first set code); `0023C5C0` calls both

`InputBackend_CopyControlCodeState130To30AllBanks` `007A0B50` copies `+0x130` back over `+0x30` for the bound codes - *precisely, for the four left-stick half-axis codes of each of
the three profiles and no others (2026-09-19, FABLE;
[binding profiles](../Binding-Profiles/binding-profiles-remapping-and-control-state.md))*. It runs
only when the input manager's `+0x3B` one-shot is set (`00197032`). A fourth writer, `FUN_0079A120`, stores `+0x30` directly
from recorded input events (log format `INPUT:%d:%s:%d:%d:%d @ frame=%d`; 0x98-byte records at `[02EA5488]`, count
`02EA5480`). Whether that table is ever filled in retail is ~~not read~~ **answered: never** *(2026-09-30, OPUS, static —
[`sd6-recorded-input-0930`](../../_index/candidates/sd6-recorded-input-0930/README.md), `sd6_input_source.py` FAILS 0)*.
~~Registered 2026-09-30 (SWE2-DATA) as
**SD-6**, static: the table's pointer and count are written only by `00796490`, the function that calls this
recorder.~~ Corrected: `00796490` only **clears** it (four zero-stores after the free); the filler is `0079FB10`,
an input-log file loader called only by the harness command `InputSource` — and command players are built only when
`[02EA5220]` or `[02EA5230]` is non-null, both zero-initialised globals that nothing writes. The shipping game has
no way to turn the record/replay harness on. **So `+0x30` holds the level recorded at the last
transition, unless a clearer consumed it. The level itself is `+0x231`.**

**When the keyboard is polled.** Every call chain to the device poll passes through one gated path:

```
0022A580 frame dispatcher      mode byte 02064AD3 in {2,3,5}  (0022A600-0022A657; see the between-two-frames page)
  -> InputControl_QueueWorkerDeadlineAndMarkDirty 0035E9B0   0022A670; also 0022A700 when 01FD4A84 != 0 and 00184950() == 2
       releases semaphore 022CA610
InputControl_WorkerDeadlineLoop 0035EA40 (thread)            waits on 022CA610 (0035EAC1), then on its deadline
  -> 003691B0(0)                                              0035EB25; gate 022CA5F8 = 1, set once at 0035E84D
vsync-callback thread 00369100                               waits on semaphore 022CFEEC[0], calls 022CFF10[0]
  -> InputControl_UpdateFrame 0035EC90                       slot 0, stored by 00369070 at 0035E943
       inc qword [022CA5E0]                                   0035EC94: one increment per poll
  -> InputControl_UpdateRegisteredChannels 0035FCA0          unconditional call, 0035ED2B
  -> InputControl_PollAndBuildChannelHistory 0035F420        channel 0 on every tick (the skip bit is set only on an availability value the always-1 stub never returns)
  -> bridge 00862670 -> 001E09B0 -> InputManager_PollAndBuildControlState 00196FF0
       gate: InputManager +0x39 != 0                          0019701D
  -> InputSystem_UpdateRegisteredDevices 007999E0            its only caller (0019702D); vtable +0x28 over the list 01F401E8
  -> DirectInputKeyboard_PollState 007A1640                  +0x231
```

Both threads loop only while `0017D3E0` returns non-zero, i.e. while byte `+0xD07` of the settings singleton (`001D50D0`) is
set. That byte is console arm 208, **"60fps input"**. The constructor stores 1 (`001CCEF0`); the only other store is the arm
itself (`001D3CB2`), which no retail code issues ([FK-3](../../08-Combat-Formula/Steal/the-steal-roll.md)). With the byte at 0,
the callback thread would release `022CFEF0` after each callback for the synchronous path in `0035EB70`. That path does not run
in retail. The input manager's `+0x39` starts at 1 (`InputManager_Initialize` stores the word `0x100` at `+0x38`,
`0019506D`). Its only setter `001989D0` is called by `GameApplication` slot 15 `0017D1A0`, which passes its argument, and by
`001E0FB0`. Two widget message-`0x8100` arms call `001E0FB0` with 0, each after a fade request: `002292AD` in `00228C70` and
`00393D33` in `003939B0`. The caller of slot 15 is not identified. *Registered 2026-09-30 (SWE2-DATA) as **SD-7**,
static.* *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19): there is no caller to identify. The record
published in `59ec09a95` ([`sd7-sd107-closure-0930`](../../_index/candidates/sd7-sd107-closure-0930/README.md)) finds
slot 15 called nowhere in the image. See the SD-7 note in §5.)*

**What this settles, and what it does not.**
- The game-side keyboard state is exactly `+0x30`. The binding translator reads it on every poll, and reading does not clear it.
- The poll runs once per dispatcher frame in modes 2, 3 and 5, and not at all in modes 0, 1, 4 and 6 or after `+0x39` is
  cleared. The pointer chain stays unchanged in every one of those states.
- **Not read statically:** which mode the title menu runs in. *Registered 2026-09-30 (SWE2-DATA) as **SD-8**,
  static: the value the title state leaves in the dispatcher mode byte `02064AD3`.* `EXP-006` moved 18 bytes at the title with 350 ms holds, so that
  title state did poll. *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19): SD-8 is ANSWERED 2026-09-30
  (OPUS, static, `sd8-dispatcher-mode-0930`). The title chooses no mode: `02064AD3` is the dispatcher's own state
  machine, it rests in 2, 3 or 5 after boot, and the keyboard poll runs in all three. See §5.)*
- A delivery that carries no scan code cannot move a byte, even while polling runs.
- **Live corroboration (ASTRA, 2026-09-13, [recovered input route](../../_experiments/evidence/input-registration-live-title/reuse/README.md)).**
  The run used `EXP-031`'s sender: virtual key plus scan code, held about 354 ms. It observed:
  - held index **49** for Enter at the title, at load selection, at load dismissal and at the field menu, each paired with the
    visible transition. 49 is `DIK_RETURN` in `01F3DAB0`.
  - held index **2** for C, which closed the menu. 2 is `0x2E` `DIK_C`.

  So that title state polls, and a scan-code-bearing delivery reaches the latch. The earlier all-zero title capture stays
  inconclusive. Its brief tool-sent Return differs from this run in hold length and in whether it carried a scan code, and
  the static path is sensitive to both: a press shorter than one poll interval, or with no scan code, moves no byte. **Not
  isolated.**

## 3. Key addresses

| Address | Size | Role |
|---|---:|---|
| `0x022CAE90` | — | channel array base, stride `0x294` (660 B), **2 channels** *(nine of ten accessors; `GetHistoryLookbackCount` uses `0x022CAE98` = base+8)* |
| `00198000` | 1,644 B | `InputManager_LoadKeymapIni` |
| `00197160` | 1,406 B | `InputManager_TranslateBindingProfileToControlState` |
| `00198B60` | 782 B | `InputManager_MaterializeRuntimeBindingProfiles` — *the name is backwards: the defaults installer* |
| `00195DF0` | 526 B | `InputManager_RestoreDefaultBindingProfiles` — *the name is backwards: the publisher (DD-1)* |
| `00195060` | 153 B | `InputManager_Initialize` — load, validate, then publish or install defaults (§3b) |
| `00196550` | 135 B | `InputManager_ValidateBindingUniqueness` — returns 1 on a duplicate code |
| `001965E0` | 159 B | `InputManager_ValidateBindingIdRanges` — ~~returns 1 when no profile is fully in range~~ returns 1 unless profile 1 is fully in range: the outer pass repeats the same scan of profile 1 three times (`r11` is loaded once with `01F80F94` at `001965EB` and never advanced), so profiles 2 and 3 are range-checked by nothing *(corrected 2026-10-01, OPUS, from the 15-Input reconstruction-readiness map, re-read at the bytes; the keymap page's validator section had it right)* |
| `00198A00` | 349 B | `InputManager_AssignBindingWithConflictPolicy` |
| `00198790` | 8 B | `InputManager_GetSingleton` — **46 external callers** |
| `007A2440` | 3,269 B | `InputBackend_UpdateResolvedDeviceState` — largest in the stack |
| `0079D1D0` | 327 B | `InputBackend_GetFilteredAnalogAxisValue` |
| `0035F760` | 856 B | `InputControl_NormalizeAnalogAndComputeTransitions` |
| `0035FBD0` | 194 B | `InputControl_FilterTransitionMaskWithRepeatState` |
| `0035F420` | 360 B | `InputControl_PollAndBuildChannelHistory` |
| `0035F690` | 205 B | `InputControl_AdvanceChannelTimingState` |
| `0035F130` | 22 B | `InputControl_GetHistoryLookbackCount` |
| `0035EEB0` | 94 B | `InputControl_GetHistoryAnalogByteByIndex` |
| `0035EA40` | 291 B | `InputControl_WorkerDeadlineLoop` |
| `007A1640` | 331 B | `DirectInputKeyboard_PollState` — the only `GetDeviceState` for the keyboard; writes `+0x231` |
| `0079D010` | 444 B | backend transition pass — writes `+0x130` and the latch `+0x30` |
| `007999E0` | 158 B | `InputSystem_UpdateRegisteredDevices` — only caller `00196FF0` |
| `0022A580` | — | frame dispatcher; releases the input worker in modes 2, 3, 5 |
| `01F3DAB0` | 256 B | keyboard index → `DIK_*` remap table |
| `022CA5E0` | 8 B | poll counter, `+1` per `InputControl_UpdateFrame` |

## 3a. Data structures (SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-DATA) from the answered rows this page carries (§5, AP-3 / AP-6 / AP-8 / AP-9) and §2; every
field below is cited there to its instructions.*

```
channel record  @ 022CAE90 + channel * 0x294        2 channels, 660 bytes each               §2, §10
  +0x01        u8        ring cursor (every mask accessor)
  +0x08        u8        history lookback count (GetHistoryLookbackCount, base + 8)
  +0x44        frame[16] history ring, 36 bytes per frame
  (the builders' parameter bytes - repeat delays, stick threshold, dead zone, scale factors, the
   stick-as-D-pad flag - and the timing state are given in section 5, AP-3 / AP-6 / AP-8, relative
   to the record pointer each builder receives; they are not restated here)

history frame (36 bytes)
  +0x00  u16   channel index          +0x02  u16   raw button mask                        AP-9
  +0x04  u16   held, set 0            +0x06  u16   held, set 1                            AP-6
  +0x08  u16   auto-repeat, set 0     +0x0A  u16   auto-repeat, set 1   (repeat filter)   AP-8
  +0x0C  u16   newly pressed, set 0   +0x0E  u16   newly pressed, set 1                   AP-6
  +0x10  u16   released, set 0        +0x12  u16   released, set 1                        AP-6
  +0x14  u8[16] one byte per button: its control-state byte when down, else 0x80 (i < 4) / 0   AP-9

control-state buffer 022CB680 (filled by InputManager_PollAndBuildControlState through the bridge)
  +0x02 + remap[i]   the per-button bytes the poll copies, remap at 01EF9238                  AP-9
device slot 022CB640: dword set to -1 by 00862660 (AP-6); the poll reads the raw
  16-bit button word at 022CB642 / 022CB643                                                   AP-9

keyboard object (PFramework::PInputDeviceKeyboard, 0x338 bytes)                              §2
  +0x30   u8[256]  transition latch - the byte game code reads
  +0x130  u8[256]  level at the previous backend pass
  +0x231  u8[256]  polled level
```

Set 0 is the digital pad (or the stick standing in for it when flag bit 1 is set); set 1 is the union of buttons,
stick directions and the physical D-pad (AP-6).

**One base (SWE2-DATA, 2026-09-30).** Every channel-record offset on this page is from R = `022CAE90` + channel × `0x294`. The updater `0035FCA0` walks R itself and passes it to the poll `0035F420` (`0035FD8A`). The poll passes it unchanged to both builders (`0035F514`, `0035F526`), and the repeat filter receives it from them. The mask accessors form R (`0035EF25`), and `GetHistoryLookbackCount`'s `022CAE98` is R+8. The one exception is the initialiser `0035F260`, which loads `rdi` = `022CAE91` = R+1 (`0035F2A8`; `rbx` = `rdi` − 1 = R, `0035F2E3`). Its `[rdi+k]` is therefore R+(k+1). In R terms the header is:

```
  +0x00  u8   write cursor: the frame the poll fills; the updater steps it mod 16 (0035FCE0-0035FCEE)
  +0x01  u8   read cursor: the ring cursor every mask accessor adds its lookback to; the per-frame cursor step moves it (B4)
  +0x02  u8   channel index (read by the poll at 0035F43A; initialiser [rdi+1])
  +0x03  u8   stick direction threshold [record+0x03] (0035F8AE); initialised 0x68 ([rdi+2])
  +0x04  u8   repeat initial delay, initialised 0x0C  } one dword 0x50C at [rdi+3] (0035F312);
  +0x05  u8   repeat rate, initialised 0x05           } the repeat filter reloads its countdowns from them
  +0x08  u8   history lookback count: the per-frame cursor step stores the write-to-read distance here (B4)
  +0x09  u8   flags; bit 1 = the stick stands in for the D-pad, cleared at init ([rdi+8], 0035F34B)
  +0x0B  u8   [record+0x0B], initialised 0x90   } one word 0x0090 at [rdi+0xA] (0035F31D)
  +0x0C  u8   [record+0x0C], initialised 0x00   }
  +0x0D  u8   dead-zone radius (0035F7BD), initialised 0x20 ([rdi+0xC], 0035F323)
  +0x24  u8[] repeat countdowns at +0x24 + set + 2i;   +0x34  u16[8]  the button-group words
```

Control: `_index/candidates/dd-leftovers-0930/in_channel_base.py` (B1–B8, C1–C3; FAILS 0). C3 checks that the initialiser's own R-based frame store uses the same `+0x58` displacement as the analog builder, so the one-byte shift applies only to its `rdi`-based stores.

## 3b. Call chain (SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-DATA). Every edge is a raw call / jmp site, checked by
[`in_dd_checks.py`](../../_index/candidates/dd-data-0930/in_dd_checks.py) CC (FAILS 0; controls CC+ / CC-).*

```
poll (vsync-callback slot 0, released by the dispatcher in modes 2, 3 and 5 - section 2)
  InputControl_UpdateFrame 0035EC90
    -> InputControl_UpdateRegisteredChannels 0035FCA0           0035ED2B
       -> InputControl_AdvanceChannelTimingState 0035F690       0035FD8D
       -> InputControl_PollAndBuildChannelHistory 0035F420      0035FD85
          -> bridge 00862670                                    0035F467
             -> InputAPI_PollControlState 001E09B0              00862673 (jmp)
                -> InputManager_PollAndBuildControlState 00196FF0   001E09D3 (jmp)
                   -> InputSystem_UpdateRegisteredDevices 007999E0  0019702D -> device vtable -> 007A1640 (keyboard)
          -> InputControl_ConvertButtonMaskToTransitions 0035FAC0   0035F517 (first)
             -> InputControl_FilterTransitionMaskWithRepeatState 0035FBD0   0035FBB8 (set 0)
          -> InputControl_NormalizeAnalogAndComputeTransitions 0035F760 0035F529 (second)
             -> 0035FBD0                                        0035FA6B (set 1)
          -> InputControl_UpdateDeviceFeedbackOutput 0035F590   0035F548

bindings (boot)
  InputManager_CreateSingleton -> InputManager_Initialize 00195060      0019877E
    -> InputManager_BuildKeymapPath 00197EE0                     001950B2
    -> InputManager_LoadKeymapIni 00198000                       001950BA
    -> InputManager_ValidateBindingUniqueness 00196550           001950C2   (returns 1 on a duplicate)
    -> InputManager_ValidateBindingIdRanges 001965E0             001950CE   (returns 1 unless profile 1 is fully in range - profiles 2 and 3 are not checked; see the table above)
    -> either returned 1: 00198B60, the defaults installer       001950EB
       both returned 0:   00195DF0, the publisher                001950DA
```

**Upstream:** the devices (DirectInput keyboard, pads, mouse) and the keymap `.ini`. **Downstream:** the gameplay
input snapshot `02F97360` (the eight masks in the order §5 AP-6 gives) and every game-side query of the keyboard latch
`+0x30` (§2). The two GFZ names of the binding pair are backwards: `00198B60` installs the shipped defaults and
`00195DF0` publishes the loaded keymap
([the binding-profiles contract](../Binding-Profiles/CONTRACT-binding-profiles.md)).

## 4. Modding notes

- **Bindings come from an `.ini`.** `BuildKeymapPath` + `LoadKeymapIni` is the entry point for
  anything that wants to change controls without patching code.
- **Two validation gates.** A binding must pass id-range *and* uniqueness checks before it becomes a
  runtime profile; an edited keymap that fails either is silently replaced by defaults. *(Anchored 2026-09-30,
  SWE2-DATA: `InputManager_Initialize` `00195060` branches to the defaults installer `00198B60` when either
  validator returns 1 (`001950C9`, `001950D5`, `001950EB`), and publishes the loaded keymap through `00195DF0` only
  when both return 0 (`001950DA`); [`in_dd_checks.py`](../../_index/candidates/dd-data-0930/in_dd_checks.py) IV1–IV3.)*
- **Sixteen frames of history, two channels.** Anything reading input history is bounded by that
  ring — a longer combo window is not expressible without enlarging the record.
- **One repeat filter for digital and analog.** Changing repeat behaviour changes both.
- **Control-code band matters.** Codes 11–27 are polled across all devices; 28–283 are per-bank. A
  binding moved across that boundary changes which devices can trigger it.
- **XIIOnline:** input is per-client and never authoritative. Synchronise the *actions* a binding
  produces, never the control state — two clients with different keymaps must still agree on
  outcomes.

## 5. What is not known

- [x] What distinguishes control-code bands 1–3, 11–27 and 28–283. **AP-1 ANSWERED 2026-09-02** — three unsigned subtract-and-compare tests in `00197160`; any-device vs per-bank confirmed. **Correction: the upper band at that call site is 28–152, not 28–283** (`0x7D` = 125). See `../Binding-Profiles/binding-profiles-remapping-and-control-state.md`.
- [x] ~~Whether `0x80` is the analog neutral.~~ **AP-2 ANSWERED 2026-09-08 — yes, and a constant does
      confirm it.** `InputManager_TranslateBindingProfileToControlState` computes
      `out = (v + 1.0) * 128.0 + (currentByte - 128.0)`, with **`128.0` a literal at `008F3A2C`**
      used both as the centre of the axis map and as the reference the digital contribution is
      measured from. See `../Binding-Profiles/binding-profiles-remapping-and-control-state.md`.
- [x] What `AdvanceChannelTimingState`'s constants 16384, 1760, 1790, 180, 546 are. **AP-3 ANSWERED 2026-09-02** — thresholds 1790 / 1760 / 180 / 16384; rate ±546 (`0xFDDE` is −546 signed). See `../Binding-Profiles/binding-profiles-remapping-and-control-state.md`.
- [x] ~~Why `InputManager_*` and `InputControl_*` never call each other. Two consumers of one device
      layer, or one superseding the other.~~ **AP-4 ANSWERED 2026-09-13:** neither — one pipeline through the bridge at `00862670` / `001E09B0` (§2, *The two stacks meet through a bridge*).
- [x] ~~The binding profile format itself — `TranslateBindingProfileToControlState` is 1,406 B and
      unread.~~ **AP-5 ANSWERED 2026-09-08.** Body read and record derived: **`+0x00` sixteen `int`
      digital codes, `+0x40` sixteen 16-byte entries `{mode, axisId, codeA, codeB}`, 0x140 bytes
      total.** Three modes, the **active-low** mask, and the analog formula are documented.
      **⚠ This is the runtime record the translator walks, and it is NOT the `0x70`-byte `.ini`
      profile** at `01F80F90` that `keymap-ini-file-format-and-default-controls.md` derives — two
      different structures ~~and the conversion between them is unread (`DD-1`)~~ — **`DD-1`
      ANSWERED**: `00195DF0` is the converter, read in full in
      [the binding-profiles contract](../Binding-Profiles/CONTRACT-binding-profiles.md) §7a, and
      both shapes are now type rows (`InputBindingProfile` `0x70`, `InputBindingRecord` `0x15C`
      with a `0x140` read extent). **The two structures remain distinct** — editing one still does
      not edit the other, which is the part a remapping tool must respect.
- [x] What the eight u16 mask fields hold. **LOCATION ANSWERED, WRITERS IDENTIFIED 2026-09-02** —
      frame-relative `+0x04`–`+0x12`; four written by **both** transition builders, two by the analog
      builder only, two by neither. Contents still open. Sections 8 and 9. **AP-6.**
      *Narrowed 2026-09-14 (FABLE), not answered:* **the eight fields are two sets of four — held, newly pressed,
      released, press-with-repeat.**
      - **Set 0.** Both builders store it the same way (`0035FB92`–`0035FBB4`, `0035FA49`–`0035FA67`): held
        `cur` at `+0x04`, `(prev ^ cur) & cur` at `+0x0C` and `(prev ^ cur) & prev` at `+0x10`. The repeat
        filter writes `+0x08` (`AP-8`).
      - **Set 1.** The analog builder stores `cur | r12` at `+0x06`, pressed at `+0x0E` and released at `+0x12`
        (`0035FA84`–`0035FA9F`); the repeat filter writes `+0x0A`. The digital builder also stores its held
        mask at `+0x06` (`0035FBBD`).
      - **Which builder owns set 0** follows channel byte `+9` bit 1: the digital builder writes set 0 when it is
        clear (`0035FB88`), the analog builder when it is set (`0035FA37`).
      - **In the gameplay snapshot** `02F97360` these are, in order, `+0x06`, `+0x0E`, `+0x0A`, `+0x12`, `+0x04`,
        `+0x0C`, `+0x08`, `+0x10` (`002498B0`, `00249940`–`002499AC`; [the Config screen](../../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md) §6).
      - **Residue:** what physical inputs `r12` and the analog set carry, and the call order of the two builders
        within one poll, which decides whose `+0x06` survives.
      **ANSWERED 2026-09-18 (FABLE) — the eight masks, both sets, read from the three builders and the poll.** Frame-relative, from the slot base `+0x44`: `+0x04` / `+0x06` **held**, `+0x08` / `+0x0A` **auto-repeat**, `+0x0C` / `+0x0E` **newly pressed**, `+0x10` / `+0x12` **released** — the first of each pair is **set 0**, the second **set 1**. *The poll* `0035F420` writes the device-slot dword `022CB640` to −1 (`00862660` is `mov dword [rdx], -1`, so its name is right and the value is an all-ones eligibility mask), polls the control state into `022CB680` (`00862670`), and copies sixteen per-button bytes into the slot at `+0x58` .. `+0x67` through the index table `01EF9238` (`00 01 02 03 06 04 07 05 0E 0F 0C 0D 08 09 0A 0B`: button bit *i* takes control-state byte `2 + table[i]`), with `0x80` for bits 0–3 when not down (`0035F4D0`–`0035F508`). *The transitions builder* `0035FAC0` runs **first** (`0035F517`): held = the `022CB640` word AND NOT the control-state word (`0035FB50`–`0035FB64`, the buttons are **active-low**), with the D-pad opposites cancelled (`0x50` = up+down, `0xA0` = right+left, `0035FB6D`–`0035FB82`; the bits are the SCE order, up `0x10`, right `0x20`, down `0x40`, left `0x80`); when record `+0x09` bit 1 is **clear** it writes set 0 — `+0x04` held, `+0x0C` pressed = `(prev ^ held) & held`, `+0x10` released = `(prev ^ held) & prev` — and calls `0035FBD0` for `+0x08`; it always writes `+0x06` (`0035FBBD`). *The analog builder* `0035F760` runs **second** (`0035F529`), so its stores are the ones that survive: it snaps the two stick pairs (slot `+0x5A` / `+0x5B` and `+0x58` / `+0x59`, centre `0x80`) to centre inside the dead zone `[record+0x0D]` (`0035F7BD`–`0035F876`), zeroes the four D-pad bytes `+0x5C` .. `+0x5F` whose bit is not held, and derives direction bits from stick A beyond the threshold `[record+0x03]` (`0035F8D5`–`0035F901`: down `0x40`, right `0x20`, up `0x10`, left `0x80`, each clearing its opposite). **`r12` is the physical D-pad nibble**: when record `+0x09` bit 1 is **set**, bits 4–7 of the held word are set aside in `r12` and the stick's directions replace them (`0035F8C0`–`0035F8CA`), set 0 is written from that stick-as-D-pad word (`0035FA3D`–`0035FA6B`) and the stick and D-pad bytes are rewritten as scaled magnitudes with `[record+0x0C]` and `[record+0x0B]` (`0035F90D`–`0035FA33`); otherwise `r12` is 0. Then `ebx = ebx OR r12` restores the nibble and **set 1 is the union** of digital buttons, stick directions and the physical D-pad: `+0x06` held, `+0x0E` pressed, `+0x12` released (`0035FA79`–`0035FA9F`), and `0035FBD0(record, frame, prev, 1)` fills `+0x0A`. *The repeat builder* `0035FBD0` keeps eight countdown bytes at record `+0x24 + set + 2i`, one per button-group word at record `+0x34 + 2i`, reloaded from record `+0x04` (initial delay) or `+0x05` (repeat rate), and emits the group's held bits into `frame + 8 + 2·set` when its counter runs out (`0035FBF9`–`0035FC87`). ~~The record initialiser `0035F260` sets the thresholds `+0x0A` / `+0x0B` = `0x0090`, `+0x0C` = `0x20` (`0035F31D`–`0035F323`) and never writes `+0x0D`, so the dead-zone radius is 0 unless a caller sets it.~~ *(Corrected 2026-09-30, SWE2-DATA: those are the initialiser's own displacements from `rdi` = R+1 (`022CAE91`), the one site that addresses the record one byte in. In the base the builders use, the word `0x0090` lands at `+0x0B`–`+0x0C` (`+0x0B` = `0x90`, `+0x0C` = 0) and the byte `0x20` at `+0x0D`. So the dead-zone radius `[record+0x0D]` starts at `0x20`, not 0. The same initialiser sets the threshold `[record+0x03]` to `0x68` (`0035F319`) and clears flag bit 1 (`0035F34B`). §3a states the one base; control `_index/candidates/dd-leftovers-0930/in_channel_base.py` B5, B7, B8.)* So the two sets are the same four masks over two button words: **set 0 = the digital pad (or the stick standing in for the D-pad when flag bit 1 is set), set 1 = everything at once.** Static: the poll, the three builders and the initialiser, read whole.
- [x] ~~What writes frame fields `+0x08` and `+0x0A` — neither transition builder does.~~ **AP-8
      ANSWERED 2026-09-12 (FABLE): the repeat filter does.**
      `InputControl_FilterTransitionMaskWithRepeatState(channel, frame, previousFrame, index)`
      (`0035FBD0`) walks the sixteen button bits of the frame's mask word `+0x04 + 2·index` against
      the previous frame's (`0035FBF9`–`0035FC03`), keeps a per-button repeat countdown byte at
      `channel + 0x24 + index + 2·bit` (`0035FC09`–`0035FC66`; reloaded from the channel's bytes
      `+4` / `+5`, the initial and repeat delays), and ORs into `r10w` every bit that is newly set
      or whose countdown expired while held — then stores that word at **`frame + 0x08 + 2·index`**
      (`0035FC87`). The digital builder calls it with index 0 and the analog builder with index 1,
      so **`+0x08` is the repeat-filtered digital press mask and `+0x0A` the repeat-filtered analog
      one**: the "fires this frame" words behind key repeat. **AP-8.**
- [x] ~~What frame bytes `+0x1C`–`+0x23` hold. Neither builder writes them; an earlier revision
      labelled them analog by filling leftover space.~~ **AP-9 ANSWERED 2026-09-12 (FABLE): the poll
      writes them — one byte per button, sixteen buttons.** `InputControl_PollAndBuildChannelHistory`
      (`0035F420`) reads the backend's raw 16-bit button word (`022CB642` / `022CB643`), builds the
      frame's mask word `+0x02` bit by bit, and for each bit `i` (0–15) stores at **`frame + 0x14 + i`**
      either the backend control-state byte `022CB680 + 2 + remap[i]` when the button is down — the
      per-button pressure / analog value, with `remap = 0 1 2 3 6 4 7 5 14 15 12 13 8 9 10 11` at
      `01EF9238` — or the rest value **`0x80` for `i < 4` and `0` otherwise** (`0035F4A2`–`0035F508`;
      the initialiser seeds the same rest values, `0035F3A0`–`0035F3AD`). So `+0x1C`–`+0x23` are the
      bytes of buttons 8–15, and the earlier "sixteen analog axes" reading was sixteen *buttons*: the
      first four rest at centre, the rest at zero. The frame's header is `+0x00` the channel index
      (`0035F572`) and `+0x02` the raw mask. **AP-9.**
- [x] ~~What `WorkerDeadlineLoop` / `QueueWorkerDeadlineAndMarkDirty` schedule~~ — the stack has its own
      deadline worker. **Answered 2026-09-13 (FABLE)**; the ledger row is ANSWERED (task FABLE-LEDGER-AP7-EU1): the worker schedules vsync-callback slot 0, which is
      `InputControl_UpdateFrame` and so the whole keyboard / pad poll. It waits on semaphore `022CA610`, which
      `QueueWorkerDeadlineAndMarkDirty` releases. That function's only callers are the frame dispatcher `0022A580`'s two
      sites, which run in modes 2, 3 and 5. The worker then waits out the queued deadline (doubles −16.0 / 17.0 at
      `00908D60` / `00908D58`) and releases the callback thread's semaphore (§2, *The keyboard byte array*). Not read: the
      deadline arithmetic in `0035E7A0` (constants `0x13A` / `0x108`). **AP-7.** *Registered 2026-09-30 (SWE2-DATA) as
      **SD-9**, static — answered the same day (OPUS, static): the arithmetic yields the constant 528 (264 in
      dispatcher mode 3), stored at `022CA5DC` and never read; it paces nothing.*
- [x] **SD-5.** Whether one of the application's one-shot display requests (bytes `+0x1E`–`+0x21`, `+0x29`) can stay
      set across frames and so hold back the keyboard transition pass (§2). *Registered 2026-09-30 (SWE2-DATA), static.* *(SD-5 answered 2026-09-30 by OPUS `ce2b4380d`, [record](../../_index/candidates/sd5-display-requests-0930/README.md).)*
- [x] ~~**SD-6.**~~ Whether the recorded-input table at `[02EA5488]` is ever filled in retail — **no; only the
      harness `InputSource` command fills it and the shipping build never builds a player** (§2; OPUS, static,
      `sd6-recorded-input-0930`).
- [x] **SD-7.** Who calls `GameApplication` slot 15 (`0017D1A0`), the setter of the input manager's `+0x39` poll gate
      (§2). *Narrowed 2026-09-30 (OPUS, static, `sd7-slot15-callers-0930`): no caller on the framework,
      window-procedure, static-object or own-method routes; the residue is game code calling through a stored
      application pointer.*
      *Answer note 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19): answered 2026-09-30 by SWE2-STRUCT for OPUS,
      published in `59ec09a95`, [record `sd7-sd107-closure-0930`](../../_index/candidates/sd7-sd107-closure-0930/README.md)
      (`sd7_sd107_closure.py`, FAILS 0). **Slot 15 is called nowhere.** The record types all 34 remaining
      `[vtable+0x78]` sites, and none dispatches on the application: they act on the D3D11 render context, a Steam
      interface, Bullet shapes and worlds, PPFX GPU interfaces and a resolved resource handle. No register call loads its
      target from `[reg+0x78]`. The only image qword equal to `0017D1A0` is its own vtable slot `008C57D8`, which is
      `GameApplication` slot 15. So the stored-pointer residue is empty. The setter `001989D0`'s other caller, `001E0FB0`,
      is called only at `002292AD` and `00393D33`, both with 0. With slot 15 unused, every traced call into the setter
      therefore turns the poll off; none turns it back on. In player terms, the second switch on the pad-poll gate is
      wired but never thrown. Rechecked independently in this batch:
      [`b19_checks.py`](../../_index/candidates/swe2contract-ddres-b19-0930/b19_checks.py) A1-A7. The box is ticked
      when SWE2-DATA restates the register row.* *(SD-7 answered 2026-09-30 by SWE2-STRUCT for OPUS `59ec09a95`, [record](../../_index/candidates/sd7-sd107-closure-0930/README.md); register restated 2026-10-01 by OPUS for SWE2-DATA: no caller - GameApplication slot 15 is called nowhere, so the +0x39 poll gate is set only by 001989D0.)*
- [x] ~~**SD-8.**~~ Which dispatcher mode (`02064AD3`) the title menu runs in — **the title chooses none;
      `02064AD3` is the dispatcher's own state machine, resting in 2/3/5 after boot, and the keyboard poll runs in
      all three** (OPUS, static, `sd8-dispatcher-mode-0930`).
- [x] ~~**SD-9.**~~ The deadline arithmetic in `0035E7A0` (constants `0x13A` / `0x108`) ~~that paces the input
      worker~~ — **paces nothing: the result is the constant 528 (264 in mode 3), stored at `022CA5DC` and never
      read** (OPUS, static, `sd9-input-deadline-0930`). The dispatcher's queue machinery is now fully bound — the enqueue `0035E9B0` tails the dirty-mark `0035FF80`, and the same frame drains it through `00360080` → `00369170` → `00369080` ([the `0022A580` subtree census](../../00-Engine-Core-Runtime/Application-Root/game-application.md)).

## 6. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 49 functions across three families, with sizes | `functions.tsv`, prefixes `InputManager_`, `InputControl_`, `InputBackend_` | 1 |
| The call structure of all three layers | intra- and cross-family edges from `edges.tsv`, every pair listed in section 2 | 1 |
| Channel array base and 660-byte stride | `imul rcx, rax, 0x294` + `lea rax, [rip+…]` in `GetHistoryLookbackCount`, machine-resolved; the same `imul 0x294` appears in the other accessors | 1 |
| Exactly two channels | `cmp ecx, 2 ; jl` guarding every accessor, returning 0 (or `0x80`) otherwise | 1 |
| Sixteen-frame ring | `cmp ecx, 0x10` and `and eax, 0xFFFFFFF0` in `GetHistoryMaskOffset04` | 1 |
| ~~Lookback count at `+0`, cursor at `+1`~~ **Lookback count at `+0x08`, read cursor at `+0x01`, write cursor at `+0`** *(corrected 2026-09-30, SWE2-DATA; §10, §3a)* | ~~`GetHistoryLookbackCount` reads `rec[0]`;~~ `GetHistoryLookbackCount` reads `022CAE98` + channel × `0x294` = R+8; the mask accessors read `rec[1]` and add the caller's lookback | 1 |
| Eight u16 mask fields at 2-byte spacing | the eight `GetHistoryMaskOffset04/06/08/0A/0C/0E/10/12` functions | 2 |
| Digital and analog share one repeat filter | both `ConvertButtonMaskToTransitions` and `NormalizeAnalogAndComputeTransitions` call `FilterTransitionMaskWithRepeatState` | 1 |
| Bindings are validated twice before use | `Initialize` calls `ValidateBindingIdRanges` and `ValidateBindingUniqueness` | 1 |
| ~~The two upper layers never call each other~~ **One pipeline through a bridge** *(corrected 2026-09-30, SWE2-DATA; AP-4)* | ~~no edge in either direction between `InputManager_*` and `InputControl_*`~~ the bridge `00862670` → `001E09B0` → `00196FF0` (§2, §3b) | 1 |
| The eight masks: held, auto-repeat, pressed, released, in two sets | the poll and the three builders, §5 AP-6 / AP-8 | 1 |
| Frame `+0x14`–`+0x23`: one byte per button | the poll `0035F420`, §5 AP-9 | 1 |
| A failed validator installs the defaults | `00195060` at `001950C9` / `001950D5` / `001950EB`, §3b | 1 |
| `GetSingleton` has 46 external callers | caller census over `edges.tsv` | 1 |

**Scope honesty:** the *structure* is read — families, call graph, record layout, ring size. ~~The
binding format, the timing constants and the meaning of the mask fields are all listed above as
unknown rather than guessed. The `0x80` neutral is explicitly an inference.~~ *(Corrected 2026-09-30, SWE2-DATA:
all four were answered since — the binding format AP-5, the timing constants AP-3, the mask fields AP-6 / AP-8,
and the `0x80` neutral AP-2 (a literal at `008F3A2C`), §5. What stays open is SD-5 to SD-9.)* *(Pointer 2026-10-01
(SWE2-CONTRACT for OPUS, DD batch 19): SD-5, SD-6, SD-8 and SD-9 are ANSWERED 2026-09-30. SD-7 is answered by the
record published in `59ec09a95`, and its register row is not yet restated. See §5.)*

## 7. Related

- [`../Gameplay-Capability-Policy/capability-inhibition-policy.md`](../Gameplay-Capability-Policy/capability-inhibition-policy.md) — what may be *done* with an input once it is resolved
- [`../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md`](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) — `InputGameplay_ArbitrateDigitalInputAndModalState` consumes the mode this stack feeds

## 8. Falsification pass 2026-09-02 — AP-6, and the record layout was wrong

**Attack chosen.** The document asserted a channel record layout with "eight u16 mask fields at
`+4`–`+0x13`" and listed their meaning as unknown (**AP-6**). Field *positions* asserted without
reading the indexing arithmetic are exactly the kind of claim that looks measured and is not — so the
accessors were read to the last instruction.

### CORRECTED: the masks are per-frame, not record header fields

The index arithmetic is unambiguous:

```
lea  rcx, [rax + rax*8]                 ; rax * 9
movzx eax, word ptr [rdx + rcx*4 + D]   ; rdx + frame*36 + D
```

`rax*9` scaled by 4 is a **36-byte frame stride**, and the eight accessors use displacements
`0x48, 0x4A, 0x4C, 0x4E, 0x50, 0x52, 0x54, 0x56`. Subtracting the ring's base gives frame-relative
`+0x04 … +0x12` — which is where the function *names* came from all along.

**The document placed those offsets in the record header.** They are offsets **inside a history
frame**. The names were right; my reading of what they were offsets *from* was wrong.

### The corrected layout, and it fits exactly

```
channel record @ 0x022CAE98 + channel * 0x294        (660 bytes, 2 channels)
  +0x00        byte    history lookback count
  +0x01        byte    ring cursor
  +0x44        history ring: 16 frames x 36 bytes

  frame +0x00 .. +0x03     4 bytes    header (not touched by these accessors)
  frame +0x04 .. +0x13     8 x u16    mask fields
  frame +0x14 .. +0x23    16 bytes    analog axis bytes, indexed by axis
```

`GetHistoryAnalogByteByIndex` reads `[record + axis + frame*36 + 0x58]` — frame-relative `+0x14`,
offset by the axis index, giving **sixteen analog axes per frame**.

**The arithmetic closes with nothing left over:**

```
4 + 16 + 16            = 36    the frame
0x44 + 16*36 + 16      = 660   = 0x294, the record
```

A layout that accounts for every byte of a stride recovered independently is about as strong as a
structural claim gets short of a symbol.

### AP-6 half-answered

**Where** the eight masks live is now exact. **What they hold** is still unknown — eight parallel
16-bit masks per frame is the shape of "one mask per input category", but nothing read here says
which. That half stays open. *(Answered since: AP-6, 2026-09-18, §5.)*

### Also confirmed

The 16-frame wrap: `ecx - ((ecx >> 4) << 4)` is `ecx & 15`, applied after adding the caller's
lookback to the cursor — so a lookback past the ring start wraps rather than clamping or failing.

### Not changed

Two channels, the 660-byte stride, ~~the lookback count at `+0`, the cursor at `+1`,~~ *(corrected 2026-09-30, SWE2-DATA: §10 moved the base to `022CAE90`, with the cursor at `+0x01` and the lookback count at `+0x08`; §3a)* the three-layer
call structure and the binding validation all stand.

## 9. Falsification pass 2026-09-02 (second) — the writers, and I made the same mistake twice

**Attack chosen.** Pass 8 fixed *where* the eight mask fields live and left *what they hold* open,
with a note that "one mask per input category" was the tempting reading and would not be adopted
without the writers. This pass reads the writers. They refute a hypothesis I had not yet written
down — and refute part of what I had.

### The two transition builders overlap; they do not divide the fields

| writer | frame offsets written |
|---|---|
| `ConvertButtonMaskToTransitions` | `+0x04`, `+0x06`, `+0x0C`, `+0x10` |
| `NormalizeAnalogAndComputeTransitions` | `+0x04`, `+0x06`, `+0x0C`, **`+0x0E`**, `+0x10`, **`+0x12`** |

**Four fields are written by both.** The digital and analog paths are not two halves of the frame —
they are two producers writing into a **shared** set of masks, with the analog path owning two extra.
A "buttons here, sticks there" split would have been a natural guess and is wrong.

**And two fields are written by neither**: `+0x08` and `+0x0A`. Whatever fills them is somewhere
else, or they are derived on read. **AP-8.**

### CORRECTED: eight analog bytes are written, not sixteen

Pass 8 recorded `frame +0x14 .. +0x23   16 bytes  analog axis bytes`. The analog writer covers
**`+0x14` … `+0x1B` — eight bytes**. The remaining eight, `+0x1C` … `+0x23`, are written by neither
builder and are **unaccounted**.

I did not measure sixteen. I had a 36-byte frame, 4 header bytes and 16 bytes of masks accounted
for, and **filled the remaining sixteen with the label already in hand**. The accessor indexes by
axis from `+0x14` and says nothing about the array's extent.

**This is the fourth-time-plus-one of the failure written into
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) two passes earlier** — and the first time
it happened *after* writing the rule. Leftover space is not evidence of what occupies it. The
standard's corollary already covers it exactly: *a structure's shape constrains what it could be;
only its writes say what it is.* Knowing the rule did not stop me applying the label; **reading the
writer did.**

### The corrected frame

```
frame +0x00 .. +0x03    4 bytes   header
frame +0x04 .. +0x13    8 x u16   masks
                          +0x04, +0x06, +0x0C, +0x10   written by BOTH builders
                          +0x0E, +0x12                 written by the analog builder only
                          +0x08, +0x0A                 written by NEITHER          (AP-8)
frame +0x14 .. +0x1B    8 bytes   analog values, written by the analog builder
frame +0x1C .. +0x23    8 bytes   unaccounted                                       (AP-9)
```

The 36-byte total and the 660-byte record are unchanged — those came from the stride arithmetic, not
from labelling. *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19): both gaps in this frame are answered.
AP-8 (ANSWERED 2026-09-12): the repeat filter `0035FBD0` writes `+0x08` / `+0x0A` (`0035FC87`). AP-9 (ANSWERED
2026-09-12): the poll `0035F420` writes one byte per button at `+0x14`–`+0x23`. The current frame is in §3a.)*

### Also identified

`PollAndBuildChannelHistory` calls three bridge functions before building anything:
`InputBridge_InitializeDeviceSlotIndexInvalid` (`00862660`), **`InputBridge_PollControlState`**
(`00862670`) and a thunk. It also calls `0016D6A0` — **the same bare `ret 0` no-op** seen in the
formula step table and the command tables, appearing in a third unrelated subsystem.

## 10. Falsification pass 2026-09-02 (third) — the record base was eight bytes off

**Attack chosen.** Not an attack at first: this pass built `struct_map.py`, a tool to report which
bytes of a structure the code actually reads and writes, so that "leftover space" could never again
be labelled by hand (pass 9's error). Its **first run, on this document's own channel record, came
back nearly empty** — three offsets out of a 660-byte stride.

A tool that finds nothing where a document claims a full layout is either broken or right. It was
both: it missed a taint path *and* the thing it missed exposed a wrong assumption.

### The accessors do not share one base

Machine-resolving the `lea [rip+…]` in each accessor:

| accessor | base constant |
|---|---|
| `GetHistoryLookbackCount` | **`0x022CAE98`** |
| all eight `GetHistoryMaskOffset*` | **`0x022CAE90`** |
| `GetHistoryAnalogByteByIndex` | **`0x022CAE90`** |

Nine of ten use `0x022CAE90`. This document published `0x022CAE98` — the odd one out — as *the*
record base, because it came from the first accessor read.

### CORRECTED: the base, and both header fields

Taking `0x022CAE90` as the record base, the fields land at:

```
channel record @ 0x022CAE90 + channel * 0x294        (660 bytes, 2 channels)
  +0x01     byte    ring cursor            (read as [rec+1] by every mask accessor)
  +0x08     byte    history lookback count (GetHistoryLookbackCount's base is rec+8, disp 0)
  +0x44     history ring, 16 frames x 36 bytes
```

Previously recorded as base `0x022CAE98` with the lookback at `+0x00` and the cursor at `+0x01` —
which cannot both be right, since those two accessors use bases eight bytes apart. **The lookback
count is at `+0x08`, not `+0x00`.**

**Everything frame-relative is unchanged**, because it was all derived from the `0x022CAE90`
accessors: masks at frame `+0x04`–`+0x12`, analog at frame `+0x14`, ring at record `+0x44`, 36-byte
frames, 660-byte record. Only the two header fields and the base address move.

### Why the error survived two passes

Pass 8 read `GetHistoryLookbackCount` first, took its `lea` target as the record base, and then read
the mask accessors for *offsets* without re-checking their base. Each reading was correct in
isolation; combining them silently assumed a shared origin. **When several accessors describe one
structure, the base each of them uses is part of the measurement, not a given.**

### The tool, and what it now does

`struct_map.py` reports every offset with read/write counts, flags offsets **read but never
written**, and lists byte ranges inside the stride that **nothing touches** as `UNACCOUNTED`, with
the line *"an unaccounted range is a QUESTION, not a label."*

Its first run was near-empty because the base can arrive in the **index** register
(`lea rax,[rip+BASE]` then `[rcx + rax]`), which it did not follow. Fixed in the same pass — and the
near-empty result is exactly the failure mode a tool should have: **it under-reports rather than
inventing coverage.**

## 11. The binding profile table, and how defaults are restored (2026-09-02)

This document recorded that "defaults are restored before the runtime profiles are materialised" and
that the binding format is not decoded. The table itself can now be located, and its shape given.

### The live table

```
binding profile table   base 0x01F80130
                        3 profiles, stride 0x15C
                        profiles at 0x01F80130, 0x01F8028C, 0x01F803E8
```

**Two independent routes write it with the same shape**, which is what fixes the layout:

| route | when | source |
|---|---|---|
| `0015BD30`, a CRT initializer | before `main` | authored prototype at `0x01DF09C0` / `0x01DF0A80` |
| `00195DF0` `InputManager_RestoreDefaultBindingProfiles` | on demand | authored records at `0x01F80F90` |

The startup initializer writes exactly three records at `0x01F80130`, `+0x15C`, `+0x2B8` — the same
three addresses the restore function walks. **A stride derived twice, by different code, at the same
base.**

### What `RestoreDefaultBindingProfiles` actually does

```c
for (i = 0; i < 3; i++) {                      /* rdi 0x01F80FD8 .. 0x01F81128 step 0x70 */
    staging = 0x01DF1738 + i*0x15C;            /* scratch, inside the 01DF15DC cluster */
    copy 0x40 bytes  from authored record  -> staging      /* two movups + scalar dwords */
    *(u64*)(staging + 0x20) = 0;
    *(u128*)(staging + 0x40) = {2, 4};         /* four 16-byte pairs, all {2,4} */
    *(u128*)(staging + 0x50) = {2, 4};
    *(u128*)(staging + 0x60) = {2, 4};
    *(u128*)(staging + 0x70) = {2, 4};

    if (!InputBinding_ShouldKeepAuthoredOrder())          /* 0x001DFA70 */
        swap(*(u32*)(staging + 0x34), *(u32*)(staging + 0x38));   /* TWO ADJACENT DWORDS */

    copy 0x15C bytes  staging -> 0x01F80130 + i*0x15C;    /* into the live table */
}
manager->byte_0x3B = 1;                        /* flag set on the manager object */
```

~~**`0x01DF15DC` is a staging buffer, not the authored defaults.**~~ *(Corrected 2026-10-01, OPUS: `0x01DF15DC` and `0x01DF1738` are records 1 and 2 of the five-record bank the poll walks every frame - `00197089` loads `01DF1480`, five rounds, `add rsi, 0x15c` at `001970BB` - so the publisher writes records 2-4 of that live bank, not a scratch area. The keymap and binding-profile pages say the same. The rest of this paragraph is kept as written history.)* The prototype-copy census
(see [static initialization order](../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md)
section 11) flagged that cluster as a destination of authored bytes and this document's own lead read
it as "the default control scheme". **It is the scratch area the defaults are assembled *in*.** The
authored records are at **`0x01F80F90`**, three of them, stride `0x70`.

### The two-dword swap

The most interesting instruction in the function is conditional:

```asm
00195F03  call  0x1DFA70                 ; InputBinding_ShouldKeepAuthoredOrder
00195F08  test  al, al
00195F0A  jne   skip
00195F0C  mov   ecx, [staging + 0x34]
00195F14  mov   eax, [staging + 0x38]
00195F1C  mov   [staging + 0x34], eax    ; swapped
00195F24  mov   [staging + 0x38], ecx
```

**Two adjacent 4-byte binding fields are exchanged when a runtime predicate says not to keep the
authored order.** That is measured. Two adjacent controls whose order flips on a build- or
region-dependent test is the shape of the **confirm/cancel button convention** — the difference
between circle-confirms and cross-confirms — but the predicate's body is not read here and the fields
are not identified. **AU-1: read `0x001DFA70`.** *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19):
read in §12 below, and AU-1 is ANSWERED. `001DFA70` is `cmp dword [rcx+0x64], 0` / `sete al`. The field is the
confirm/cancel setting `DecideButton` (AU-5 and AV-6, ANSWERED 2026-09-26; see §12).)*

### Not claimed

- That the three profiles correspond to three players, three devices or three presets. Three records
  is measured; what distinguishes them is not. **AU-2.**
- That `{2, 4}` written into four consecutive 16-byte slots is analog configuration. The constants are
  measured, the meaning is not. **AU-3.**
- The live table region `0x01F80130`-`0x01F80C68` is **2,872 bytes** but three profiles account for
  only `3 x 0x15C = 1,044`. The rest is written by other initializers and is unaccounted. **AU-4.**

*(All three answered since, 2026-09-30 pointer by SWE2-DATA: AU-2 — the three keyboard layouts of the keymap
`.ini`, 2026-09-25; AU-3 — the default keyboard layout's two-key axes, 2026-09-25; AU-4 — three blocks of three
records, 2026-09-26. See the register rows and
[the keymap page](../Binding-Profiles/keymap-ini-file-format-and-default-controls.md).)*

## 12. AU-1: the swap is decided by one dword on a shared global (2026-09-02)

The predicate is eight bytes:

```asm
001DFA70  InputBinding_ShouldKeepAuthoredPairOrderForPlatformState   (8 B, owner Input)
   cmp   dword ptr [rcx + 0x64], 0
   sete  al
   ret
```

**One dword decides it.** The pair order is kept when the field is zero and the two binding fields
are swapped when it is non-zero. Two callers, and they are the two profile builders:
`00195DF0 RestoreDefaultBindingProfiles` and `00198B60 MaterializeRuntimeBindingProfiles` — so the
same swap applies on both paths that construct a profile.

### `rcx` is not the input manager

At the call site in `00195DF0`, `rcx` last came from `00195E42`:

```asm
mov rcx, qword ptr [rip + 0x1DECED7]      ; -> the global pointer at 0x01F82D20
```

**`0x01F82D20` is a shared singleton, not an input object.** It is referenced by roughly 150
instructions across `Input`, `Presentation`, `PlatformOnlineAchievements`, `CoreRuntimeScheduling`,
`Resource` and much unowned code, and its pointer is stored exactly once, at `00798261` inside
`007980A0`.

It has a family of one-line field accessors:

| accessor | reads | callers |
|---|---|---:|
| `0017E210` | `glob->dword_0x64` — **the field this swap tests** | 4 |
| `0017E260` | `glob->dword_0x58` | 9 |
| `0017E270` | `glob->dword_0x00`, used as an **index into a table of string pointers**, then byte-compared | 5 |

A field at `+0x00` that indexes a string table is the shape of a locale selector — **and it is one.**
The table at `0x01DF0030` holds `jp en fr de it es kr ch cn none`, and `0017E270` maps the selected
code to an internal language id. See
[language selection and locale ids](../../19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md).

**So the binding-swap flag at `+0x64` and the language index at `+0x00` live on the same object.**

> **CONFIRMED 2026-09-02.** `+0x64` has a second consequence found independently: in `0022A0B0` it
> **exchanges two button bit masks between two globals** — `0x01E0C2A0` and `0x01E0C2A4` receive
> `0x2000` and `0x4000` in one order or the other depending on the field. **A locale field that swaps
> two button masks is the confirm/cancel convention**, which makes the binding-pair swap here the
> same setting acting on the binding table. See
> [language selection and locale ids](../../19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md)
> section 6.
>
> ~~Still open: which mask is confirm (**AV-6**), and what writes `+0x64` (**AU-5**).~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): both are answered. **AV-6**: `0x01E0C2A0` is CONFIRM and `0x01E0C2A4` is CANCEL. **AU-5**: `+0x64` is `DecideButton` in `GameSetting.ini`, written by the defaults copy, the ini parser and a runtime setter, so the player can change it.*

### The writer was not found, and the reason is a known instrument limit

No writer of `glob->+0x64` exists anywhere reachable by a scan that taints the global pointer and
follows `[reg + 0x64]`. The singleton's constructor `007980A0` never touches `+0x64` either.

That is the **same blind spot recorded in `struct_map.py`**: a structure written through a pointer
*passed as an argument* is invisible to a base-taint scan, and most structures are written that way.
So this is **"no writer found by this instrument"**, not "no writer". ~~**AU-5** — the field is most
likely set from the settings file or a platform query, and finding it needs the argument-passing path
rather than the global.~~ *(AU-5 is answered: the field is `DecideButton` from `GameSetting.ini`; see the note above.)*

**What is settled:** the mechanism, the deciding field, both consumers, and that the decision is
global rather than per-device or per-profile. ~~**What is not:** what sets it, and therefore whether a
player can change it.~~ *(Both are settled by AU-5: the ini's `DecideButton` sets it, and the player can change it.)*

## Cross-subsystem neighbours — disposition (audit pass, repos-2d, 2026-09-03)

`audit_crossrefs.py` against `Tools/work/graph_gn` (38,161 functions, 90,525 edges) reported **10
UNACCOUNTED NEIGHBOUR** findings for this document. **Eight of them arrive through one citation**,
and that citation is substrate rather than a relationship.

**Platform - MECHANICAL (SWE2-EC7-173, 26 edges).** The batch-138 arm sections newly name
`005CDAA0`, `0061EE30`, `006234A0`, `00629620`, `00607410` and `00602760`: `005CDAA0` is a shared
helper the engine arms call whose callers include Platform bodies `00625830`, `006242C0`,
`006253D0`, `00797690`, `00798FF0`, `007A1CD0`; `0061EE30` and `00629620` call `00808C40`,
`006234A0` calls `005CC930`, `00607410` calls `006234A0` and `00602760` calls `005CDAA0`, with the
standing `007980A0`/`00808B90`/`0080929C`/`008092FC` edges to `007A0810` completing the count.
Shared-helper fan-in across the engine's arm layer, not a platform relationship this page owns.

**Presentation - MECHANICAL (SWE2-EC7-173, 44 edges).** Most of the count is the `0016D6A0` stub
fan-in this section already dispositions; the batch-138 sections add `00629AA0` (callees
`0061DBE0`/`0061DCA0`/`0061DD60`/`0061DFE0`, itself called by `00608F20` and `00608DD0`),
`00629C70` (callee `0061DE20`) and `005CDAA0`'s Presentation callers `00639A60`, `001D1660`,
`0067C260`, `0062A0A0`, `001946E0`, `00600F30`, `0061DBE0`/`0061DCA0`/`0061DD60`/`0061DFE0`.
Shared-helper fan-in, not a presentation relationship this page owns.
- **ActorEntity - SERVICE (3 edges).** `0022A0B0`, `00266D10`, `00358A20` reach bodies filed to actor entity: `002368D0`, `003B6ED0`, `003588B0` - shared machinery across the layer boundary, no shared ownership.
- **Application - CLIENT (1 edge).** `00792350` is also called by bodies filed to application: `0015BC40` - shared machinery across the layer boundary, no shared ownership.
- **Audio - CLIENT and SERVICE (25 edges).** `00225690`, `00184950`, `00229EA0` are also called by bodies filed to audio: `00361170`, `00361200`, `00221F40` (+11 more); `00228C70`, `003939B0`, `00266D10` reach bodies filed to audio: `00225690`, `00249CA0`, `002DEE70` (+6 more) - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - SERVICE (1 edge).** `002368D0` reaches bodies filed to combat action: `0030CF40` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT and SERVICE (34 edges).** `0017DE60`, `00184950`, `002498B0` are also called by bodies filed to core runtime scheduling: `0022A0B0`, `0022A770`, `0022A580` (+7 more); `0022A580`, `001EC060`, `00228C70` reach bodies filed to core runtime scheduling: `001EDE70`, `0022BDF0`, `001E0560` (+10 more) - shared machinery across the layer boundary, no shared ownership.
- **Developer - CLIENT (1 edge).** `00796E20` is also called by bodies filed to developer: `001C2F50` - shared machinery across the layer boundary, no shared ownership.
- **Movement - SERVICE (4 edges).** `00266D10`, `002368D0` reach bodies filed to movement: `00383A20`, `00263560`, `002EBE40` (+1 more) - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (5 edges).** `0017DFC0`, `00358A20`, `003594E0` are also called by bodies filed to party: `003594E0`, `00358CB0`; `003594E0` reaches bodies filed to party: `00358A20` - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (1 edge).** `0022A0B0` reaches bodies filed to random selection: `00379CF0` - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (13 edges).** `0017E270`, `005CD1E0`, `00796E20` are also called by bodies filed to resource: `001D9400`, `001DAAC0`, `001A7A50`; `0022A0B0`, `0079FB10`, `002368D0` reach bodies filed to resource: `00259DF0`, `002DF9A0`, `0032EAE0` (+7 more) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - SERVICE (3 edges).** `007980A0`, `00266D10` reach bodies filed to save/load/settings: `002EF2D0`, `001DE050`, `001DED50` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (3 edges).** `00229EA0`, `00290180` are also called by bodies filed to script VM / native bridge: `00354D00`, `003423E0`; `00266D10` reaches bodies filed to script VM / native bridge: `003DC2D0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT and SERVICE (7 edges).** `00229EA0`, `0017DDC0`, `00228480` are also called by bodies filed to UI: `0018EEE0`, `003C8B70`, `00276D30` (+2 more); `00228C70` reaches bodies filed to UI: `0029DBE0` - shared machinery across the layer boundary, no shared ownership.
- **World - SERVICE (1 edge).** `0022A0B0` reaches bodies filed to world: `00266D10` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (8 edges).** `00228480` is also called by bodies filed to world area: `00314020`; `00266D10` reaches bodies filed to world area: `002342F0`, `00268750`, `0026D910` (+4 more) - shared machinery across the layer boundary, no shared ownership.
### Eight of ten come from citing the CFG guard stub

This document cites `0016D6A0`. That is `_guard_check_icall`, the Control Flow Guard check stub —
**2,479 distinct callers across 16 owner subsystems**, ~~because every indirect call in the image
passes through it~~ *- corrected 2026-09-19 (FABLE): no indirect call passes through it. A guard check goes through the
pointer slot `008C31C0`, which one CRT thunk alone references; these callers reach `0016D6A0` **directly**, and are calls
to empty functions folded onto the same bytes -
[image hardening](../../24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md),
section 9a. The count and its consequence for citing the address stand.* Citing it therefore imports most of the binary:

| Owner | Callers of the stub |
|---|---:|
| *(no owner)* | 2,138 |
| Audio | 135 |
| Script VM / Native Bridge | 68 |
| Input | 37 |
| Presentation | 28 |
| Resource | 27 |
| Core runtime scheduling | 11 |
| UI | 11 |
| Save/Load/Settings | 6 |
| World/Area/Field | 5 |

Every finding of the form `0016D6A0 caller <X>` — the **Audio** (135 edges), **Application**,
**Combat Action**, **Developer**, **Items/Equipment/Shops/License**, **Movement**,
**Rewards/Progression/Economy** findings, three of the four **Actor/Entity** edges and one of the
two **World** edges — is a caller of the guard stub and nothing more. **None of them is an input
relationship**, and enumerating them would say only that the executable uses CFG.

*Disposition: substrate. Not a relationship of this or any system.*

**Instrument note for whoever maintains the checker.** `audit_crossrefs.py` already knows about
substrate — it skips a neighbour whose owner is in `SUBSTRATE` — but it applies that test to the
**neighbour** side only, never to the **cited** side. A document citing `_guard_check_icall`,
`memset` or `__security_check_cookie` therefore inherits the whole image. Excluding substrate as a
*subject* as well as a *neighbour* would remove eight findings here without weakening the check,
because none of the eight can ever be informative.

### The two that are not the guard stub

**`0022A0B0` (Core runtime scheduling, 978 B)** — cited here for its input role. The flagged edges
are its own callees: `BattleStorage_InitializeWorkArrays` (`002368D0`, Actor/Entity) and the
area-initialisation routine `00266D10` (World). Both are host-frame and area-setup work belonging
to that function's own subsystem. *Irrelevant to the input stack, with the reason stated.*

**`0035EEB0` `InputControl_GetHistoryAnalogByteByIndex` ← `003594E0` (Party)** — this one is a
real relationship and is worth naming rather than dismissing: **Party reads the raw analog input
history through this accessor.** Its sibling `PartyControl_ComputeAnalogMovementScale`
(`00358A20`) does the same job on the other side of the boundary. So the input stack's history
buffer is not consumed only by Input: the party movement layer reads it directly, which is why a
change to the history format would surface as a movement bug rather than an input one.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `0032C650` | 692 | input-record lookup on `[rcx+0x30]`/`+0x3C`/`+0xF0`: single call `0017E260`; caller `0032B390` |

## The `006106A0` exclusive subtree — a third input-side thread (SWE2-FRONTIER, thunk-roots addendum)

The exclusive-callee census roots the address-taken thunk `005FE1F0` at its target **`006106A0`**
(322 B, `Boundary.Input` tagged) and assigns it **48 frontier functions**, all in the
`0x5Fxxxx`–`0x6Cxxxx` Phyre-middleware band. Signature-swept 2026-09-15; roles are measured shapes
and CodeDomain tags, not yet behaviour. *(Boundary note 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19): these
members are the render command stream's work items, resolved 2026-09-22 in the next section. Their behaviour belongs
to [the `Gi` render command family](../../17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md)
§20, not to the input stack.)*

`006106A0` is a **third thread alongside `0035EA40`/`00369100`** (§"when the keyboard is polled"):
it stores `GetCurrentThreadId` at `[this+0x298C]`, makes two `005C5230` registrations against
`[this+0x20]` and `01F2ED08`, then runs a **256-entry × 40-byte work ring** — `[this+0x2830]` is a
mod-`0x100` cursor, each record waits (`005CD840`/`005CD500`), a mode byte `[this+0x28]` selects
three arms, and records dispatch through `[rec+0x38]`/`[rec+0x30]` handlers into the engine
`0060A410`. No direct caller exists; `005FE1F0` is address-taken, so the start address is installed
through a table — the installer is not yet located. *(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19):
located 2026-09-22 (FABLE, next section). `FUN_00607D20` takes the start address at `00607DA8` and creates the
thread directly, not through a table.)*

| cluster | members | role |
|---|---|---|
| pump + dispatch engine | `006106A0` (322 B — ring pump above), `0060A410` (1,703 B — the dispatch engine: `00602760` ×2, `00608F20` ×2, `00608DD0` ×2, `00607410`, `005FDEA0`/`005FE010`/`005FFFE0`, `00621F80`/`00621FA0`, `006223D0`, `006225D0`, plus `00615BC0`/`00624670`/`00615D50`/`00616700`, IND `[rbx-0x68]`) | the thread's main loop and the dispatcher each work record enters |
| worker arms | `005FDEA0`/`005FE010` (356/330 B **twins** — `00608DD0` + `00670E00` + `00662EA0` + `00584730` shape, differing only in the `0062xxxx` tails: `005FDEA0` calls three — `00621F80`/`00622350`/`006224E0` — `005FE010` two — `00622450`/`006226D0`), `005FFFE0` (133 B — `0061ECD0` + IND `[r8+0x38]`), `005FEF80` (65 B — `005C5230`), `00602760` (724 B — DynamicGeometryProcess-tagged; `00662EA0` ×2 + `00584730` ×2, `00D4A6F0`), `00607410` (1,235 B — `0060D760` ×9 + ~30 distinct callees — the largest fan-out), `00608F20` (390 B), `00621FA0`/`006223D0`/`006225D0` (70/124/248 B — `0061ED00` + vtable calls `[rax+0x150]`/`+0x140`/`+0x138]`, `01F2DEF0`), `0061EBE0`/`0061ED70` (234/181 B — computed-dispatch pair, `[rax+0x198]`/`[rbx+0x188]`), `00615D50` (44 B leaf) | the per-record arms the engine invokes |
| heavy job bodies | `00621C00` (760 B — vtables `008C5F80`–`008C5FD0` + `01CEBBA8`), `0062AB00` (750 B — StretchBlit-tagged, `01CEBBA8` + `00D55438`/`00D554F8`), `00622BA0` (482 B → `006CA8D0`), `0061D490` (1,211 B — `0061E6B0` ×6 over `02CEDA20`–`02CF0A90` tables), `006CA8D0` (613 B — `01F2DE90`–`01F2DEF0` globals + ten indirect calls: seven `rip`-indirect, three `[rax+N]` vtable), `0062A920` (183 B — `0061C150` ×6 + `0061C010` ×2), `0060D4A0`/`0060DB10` (77/52 B pair) | the substantial work-item bodies — Phyre middleware / render ops (StretchBlit, dynamic geometry, buffer upload) |
| leaf/helper band | `0061C690` (164 B SIMD leaf), `0061C740` (339 B), `0061ECD0` (22 B), `00623B10` (251 B — D3D11 dynamic vertex/index buffer upload tagged), `00623F00` (65 B), `00626010` (76 B), `00626CE0` (175 B — `0017D260` aligned-heap + `00584730`), `00626D90` (41 B), `00627640` (258 B), `00627E50` (176 B), `00627F10`/`00627F80` (102/112 B — `0061BF40` ×2/×4), `006281A0` (113 B, `00D11104` ref), `00628220` (39 B), `00628250` (170 B SIMD), `00628300`/`00628310`/`00628320` (9/7/85 B — member-field setters), `006283E0`/`00628630` (141/96 B — `005DC1B0` + `0016D6A0` folded-stub pair), `006284B0` (103 B), `00628600` (23 B), `00629540` (27 B), `00629580` (160 B → `0062BA30`), `0062AA80` (35 B) | SIMD/bitfield/field-setter leaves and small adapters under the job bodies |

The family is Phyre middleware work-processing — the arms the pump runs are render-side bodies
(StretchBlit, dynamic geometry, D3D11 buffer upload), not bindings or channel code. What queues
records into the ring, and which subsystem the thread serves, stays open: the InputBoundary tag
comes from the address-taken install context, and the `[rbx-0x68]`/`[r8+0x38]` indirect calls are
the arms' real dispatch — resolving them needs the record type.
*(Pointer 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 19): both are answered 2026-09-22 (FABLE, next section;
BG-11). The producer is `FUN_00600D20`, slot 2 of `PRendererBase`. A record is a `[start, end)` range of
`0x80`-byte command blocks, and the thread consumes the render command stream.)*

## `006106A0` resolved — installer, record type and subsystem (2026-09-22, FABLE)

The subtree section above ends by naming three things it could not settle. All three are answered
here, and its own judgement was right on the part that mattered: **the arms are render-side, and
the `Boundary.Input` tag is an artefact of the address-taken install context.**

**1. The installer.** `FUN_00607D20` — the constructor of the `02CE4720` block queue — creates the
thread itself:

```asm
00607DA8  lea rdx, [rip -> 005FE1F0]              ; the start address, taken here
00607DD5  [rsp+0x28] = 0x10000                    ; 64 KB stack
00607DEF  005CD1E0(rcx = queue, rdx = descriptor) ; -> CreateThread; the PARAMETER is the queue
```

It is not installed “through a table”: it is a direct `lea` into a thread descriptor eight
instructions before the create. The same body makes the ring's two semaphores
(`005CD160` = `CreateSemaphoreA`, at `queue+0x2840` with 256 and `queue+0x2850` with 1) and loops
**256 times** over `005CD0E0` = `CreateEventA` to give every slot its own event.

**2. The record type.** The ring record is `R(i) = queue + 0x30 + 0x28*i` with **`+0x00` start,
`+0x08` end, `+0x10` the per-slot event, `+0x20` a completion object** — so `[rec+0x30]`/`[rec+0x38]`
in the section above are `R(i)`'s start and end, and the pair is a **`[start, end)` range of
`0x80`-byte command blocks**, not a work item. The producer is `FUN_00600D20`, vtable slot 2 of
`Phyre::PRendering::PRendererBase` (`00D498F0`).

**3. `[rbx-0x68]` is not the arms' dispatch — it is a command block's callback.** Inside
`FUN_0060A410`, `rbx = rsi + 0x70` where `rsi` is the current block (`0060A5B3`), so
**`[rbx-0x68]` is `block+0x08` and `[rbx-0x60]` is `block+0x10`**: a function pointer and its
argument, written by the producer `FUN_005FEA50`. The engine reads `dword [rsi]` as an opcode
(`0060A5C0`), switches 47 ways through the two-level table at `0060AAD8`/`0060AAB8` — **eight arms
only**, `0x01`–`0x06` and `0x2F`, with `0x07`–`0x2E` all defaulting to `0060A9C6` — and advances by
`0x80` (`0060A9D9 sub rsi, -0x80`).

**4. Which subsystem the thread serves: the render command stream.** The `0x2F` arm (`0060A899`)
builds a three-qword frame `{context, &local, block+0x10}` and calls `block+0x08` with it. For the
`Gi` render commands that callback is `FUN_001F4A10`, which turns the frame's context into the
drawing device and invokes the command's execute slot. The context is the magic-static singleton
`02CC0410` (`FUN_005FD050`), and the device is `02CC0410 + 0x18C0` — a **`PrimitiveRendererD3D11`**
(vtable `00D86960`, 45 slots). So this thread is the **consumer of the render command stream**, and
the StretchBlit / dynamic-geometry / D3D11-upload shape the section already observed in the arms is
the subsystem itself, not a coincidence of tagging.

Full derivation, with the block producer and the `Gi` side:
[the `Gi` render command family](../../17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md)
§20 (`BG-11`).

*Not claimed here:* what opcodes `0x01`–`0x06` carry — their arms were not read — and nothing about
the other two threads the section names. *(Disposition 2026-09-30, SWE2-DATA: the opcodes belong to the
render-command thread, which [the `Gi` render command family](../../17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md)
owns and which records the same limit; not an input question.)*

## The `00862680` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00862680` (`thunk_FUN_001e09e0`, 5 B) — `jmp 001E09E0`.

| member | role | interior |
| --- | --- | --- |
| `001E09E0` | the real input-channel body | [`001E09E0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Evidence-only read — frontier hub `00615BC0` (2026-09-18, SWE2-EC7)

`00615BC0` — 197 B, 7 A-measured callers; the blocking wait the channel init runs. Read
against the shipping image (page stays PARTIAL — evidence-only): a magic-static guard —
`gs:[0x58]` TLS slot + `_Init_thread_header`/`_Init_thread_footer` (`008092FC`/`0080929C`)
at `00615BD7`–`00615C2F` plus an `atexit`-family register (`00808B90`) — then a poll loop on
`005CD720(&flag, 1000)` at [`00615C40`](../../_index/ADDRESS-INDEX.md): while the wait times out, the indirect
callback `[02E2D990]`/`[02E2D984]` pair is invoked and the loop repeats; on success
`005FCF20()` + `00225690() == 1` gates a `005FD050` singleton touch before returning the
caller `rdi` — init-wait with a 1 s pump, not a spin.

`00607410` (1235 B) is the 40-arm dispatcher the `0060A410` engine's second-level switch lands in: `dword[r8] - 7` bounds-checks `0x27` and jumps through the image-base-relative table at `006078E4`; each arm forwards `[r8+8]`/`+0x10`/`+0x14`/`+0x18` on `rbx` to its `0061xxxx`/`0062xxxx`/`0060xxxx` handler (`0061EA80`, `005FEF80`, `00628220`, `006281A0`, `00628250`, `00628300`/`00628310`, `0060D4A0`, `0060DB10`, `0061EE30`, `0062AA80`, `00629620`, `00622BA0`, `006234A0`, ...) - the largest fan-out the engine's record arms feed.

Interior anchor `0060745B` (function `00607410`).

`00602760` (724 B) is the DynamicGeometryProcess-tagged worker arm `0060A410` dispatches: `dword[r14]` selects the 1-or-2 path over `[rsi-0x10]` (null-rejected), `word[rsi+0x50]` seeds the stage, and `00584730`, `005CDAA0`, `00626D90`, `00662EA0` x2, `00670E00` carry the geometry pass on `00D4A6F0`-adjacent state - the dynamic-geometry work item of the arm table.

Interior anchor `00602998` (function `00602760`).

`00608F20` (390 B) is the ring-slot enqueue `0060A410` runs: counter `02CB7FC8` (toggled `(n-1) & 1`) `x 0x70` indexes the `02CBC590` ring; the slot takes `+0x28 = rdx`, `+0x20 = r9` and `r8`'s `0x20` bytes at `+0x38..+0x50`, then `005C5230`, `0060B860`, `0060EC80`, `00623180`, `00627140`, `00629AA0`, `00629C70` carry the publish - the record hand-off the engine posts per dispatch.

Interior anchor `00609031` (function `00608F20`).

`005FDEA0` (356 B) is the first of the twin drain arms `0060A410` runs: it reads `r8`'s `+0x30`, `+0x60`, `word[+0x6A]` and `[[+0x28]+0x18]`, calls `00608DD0` for the slot rebind, then `00670E00([rdi+8], word[+0x68])` with `00584730`, `00662EA0` and the `00621F80`/`00622350`/`006224E0` tails - the drain half of the worker pair.

Interior anchor `005FDEE8` (function `005FDEA0`).

`005FE010` (330 B) is the twin of `005FDEA0` - same `+0x30`/`+0x60`/`word+0x6A` reads, `00608DD0` rebind and `00670E00` call, plus `dword[r8+0x70]` staged and the `00622450`/`006226D0` tails in place of its sibling's three - the second drain arm `0060A410` alternates with.

Interior anchor `005FE058` (function `005FE010`).

`00608DD0` (324 B) is the slot rebind both drain twins run first: when `[rcx]` is null it installs `[rbp+0x20]`/`[+0x30]` into `+0x18`/`+0x28` and `rdi` into `+0x20`; otherwise it compares `[r8+0x28]` against `rdi` and falls through to `005C5230`, `0060B860`, `0060EC80`, `00623180`, `00627140`, `00629AA0`, `00629C70` - the pointer fix-up the ring slots take.

Interior anchor `00608E9F` (function `00608DD0`).

`0060B750` (265 B) is the probe ladder `0060A410` runs: `005C5230` then `00627160` then `005C5230`/`00627160` again, each round with `r9d = eax + 1`, until one returns nonzero - the step-retry validator on the same `rcx`/`rdx`/`r8` triple.

Interior anchor `0060B76B` (function `0060B750`).

`0061EE30` (576 B) is the vtable-sequence arm `00607410` dispatches: `btr eax, 0x1F` on the mode word picks the `call [rax+0x50]`/`[+0x28]`/`[+0x1C8]`/`[+0x178]`/`[+0x70]` ladder, a 4-read/3-write byte repack loop (`rcx` -> `rbx`, `x 3` per `x 4` source) rebuilds the payload, then `call [rax+0x78]` on `[rdi+0x110]` and conditional `call [rax+0x10]` releases on the saved objects - the multi-method arm of the engine's table.

Interior anchor `0061EEC8` (function `0061EE30`).

`00622BA0` (482 B) is the flag-gated slot sweep `00607410` runs: `edx` bit 2 sets the round count (`1` or `2`), bit 0 the start index, and per `0x18`-stride row at `[rdi + (i + 0x3A) * 0x18]` a null-`+0x28`-and-`+0x18` entry is handed to `00620F60`, with `00624270`/`00624090` and `call [rbp+0x1C8]`/`call [rax+0x1B0]` on the live entries - the conditional prune arm.

Interior anchor `00622C1E` (function `00622BA0`).

`0061EA80` (338 B) is the quad-gate arm `00607410` runs: `[rcx+0x1864]`/`+0x186C`/`+0x1868`/`+0x1870` must pairwise match and `+0x185C`/`+0x1860` be zero, then `sil` bit 0 walks `[rbx + i*8 + 0x648]` for `i < dword[rbx+0x6D0]` calling `[rax+0x190]` on the `[rbx+0x110]` object per non-null entry, and `0061E760` with `xmm0 = [rbx+0x7D0]` closes - the reconcile arm's consistency gate.

Interior anchor `0061EBBC` (function `0061EA80`).

`00627640` (258 B) is the indexed vtable arm `00607410` runs: `[rcx+0x110]` null-rejects, `[rdx+0x18]` (sign-cleared via `btr 0x1F`) bounds `r9d`, the count `> 1` picks `[rdx+0x20]`'s table else the inline `rdx+0x20`, and slot `r9 x 0x28` with non-null `+0x10` earns `call [rax+0x220]` - `0` on success, `5` on every rejection.

Interior anchor `006276F5` (function `00627640`).

`006225D0` (248 B) is the command-build arm `0060A410` runs: `0061C1C0` gates, on pass `01F2DEF8` is compared-and-stored and the `01F2DEF0` vtable `00616F00` is called, then `byte[rbx+0xC] == 8` selects `0x2A` over `0x39`, `[rbx+0x68]` supplies the arg and `byte[rbx+0x6C]` bit 0 routes into the `[rdx+0x18]`-counted table walk ending in `call [rax+0x138]` on `[rsi+0x110]` - `1` on success, early-out otherwise.

Interior anchor `006225EA` (function `006225D0`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-01)

*Functions this page named only at their entry. Each was read from the certified image; the sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`inputstack_interior.py`](../../_index/candidates/opus-inputstack-interior-1001/inputstack_interior.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0017D3E0` | 43 B | returns 1 when byte `+0xD07` of the object `001D50D0()` returns is non-zero, else 0 (also 0 when there is none) | `0017D3E4`, `0017D3F3`, `0017D3FE` |
| `00198E80` | 79 B | looks up `0079D620(qword +0xDF8 of 00796E20(), edx)` and, when found, calls `007A1080(it, r9b, r8b)` | `00198E97`, `00198EA5`, `00198EBA` |
| `001E1120` | 107 B | tail-calls `00198E80(00198790(), ecx, edx, r8d)` when `00198790()` is non-null, `00197780` on it is non-zero and `00228480()` returns 0; otherwise tail-calls `00198E80(00198790(), ecx, 0, 0)` | `001E1148`, `001E1151`, `001E116C`, `001E1186` |
| `0035E7A0` | 109 B | adds dword `022CA5D0` to dword `022CA5C4` and stores the sum S there; with P = 0x108 when `00290180()` returns 2, else 0x13A: when S < P returns P - S if `00229EA0()` returns 3, else 2P - S; otherwise returns ceil(S/P)*P - S | `0035E7B6`, `0035E7CE`, `0035E7DA`, `0035E7DF`, `0035E7F7` |
| `005DC1B0` | 16 B | zeroes qwords `+0` and `+8` and dword `+0x10`; returns `rcx` | `005DC1B5`, `005DC1B9`, `005DC1BC` |
| `005FEF80` | 65 B | returns 0 when `005C5230(rcx + 8)` is non-zero; otherwise sets bit 0 of dword `+4` and tail-calls `0061D490(rcx, edx)` | `005FEF8F`, `005FEF93`, `005FEFA9`, `005FEFBC` |
| `0060D4A0` | 77 B | for slot `r8d`: with `rdx` non-null, copies 24 bytes from `rdx` to `+8 + 24*slot` and sets bit `slot` of byte `+0xE0`; with `rdx` null, clears that bit; then tail-jumps to `006283E0` | `0060D4AF`, `0060D4C8`, `0060D4DE`, `0060D4E8` |
| `0060DB10` | 52 B | with `rdx` non-null, copies 24 bytes from `rdx` to `+0xC8` and sets byte `+0xE1` to 1; with `rdx` null, sets it to 0; then tail-jumps to `00628630` | `0060DB18`, `0060DB2C`, `0060DB38`, `0060DB3F` |
| `006106A0` | 322 B | stores `005CC920()` in dword `+0x298C`, calls `005C5230(rcx + 0x20, "RenderThread" at 00D4A760, 0x2000)` and `005C5230(01F2ED08, rcx + 0x20)`, then loops: each pass takes the ring index dword `+0x2830` (0 to 255, 40-byte entries) and calls `005CD840` on the entry's `+0x40`; by dword `+0x28`, 0 calls `005CD500` and `005CDAA0(1, "Render thread running without initialize" at 00D4A770)`, 1 calls `005CD500` and `0060A410(rcx, entry qword +0x30, entry qword +0x38)`, clears entry qwords `+0x30`, `+0x38` and `+0x50` and calls `005CD650(old +0x50, 1, 0)` when it was set, and 2 ends the loop after the pass; every pass ends with `005CD650(rcx + 0x2840, 1, 0)`. After the loop it calls `005C5230(01F2ED08, rcx + 0x20)` and returns 0 | `006106CC`, `00610700`, `00610724`, `00610753`, `006107A3` |
| `00615D50` | 44 B | stores `rdx` in qword `+0`, zeroes dword `+8` and qwords `+0x10` to `+0x48`; returns `rcx` | `00615D52`, `00615D55`, `00615D74`, `00615D78` |
| `0061C150` | 75 B | maps `ecx` through an 8-entry jump table: 0 to 1, 1-4 to 2-5, 5 to 7, 6 to 8, 7 to 6, and any value above 7 (unsigned) to 1 | `0061C153`, `0061C15F`, `0061C169`, `0061C195` |
| `0061D490` | 1211 B | collects up to two qwords into the array at `+0x648` from the two 24-byte entries at `+0x570` and one into `+0x688` from the entry at `+0x630`, by the kind byte `+8` of each entry's object and the flag bits in dword `+0x18` of that object's first qword, requiring every accepted entry to share dwords `+0x28`/`+0x2C` and byte `+9` (it returns 0 on a mismatch, or when `00620F60` fails for an entry whose qwords `+0x18` and `+0x28` are 0); the count goes to dword `+0x6D0`. With none accepted it falls back to `+0x4A0`/`+0x4A8`, `+0x4E0`/`+0x4E8` and the sizes of the object at `+0x480`. It stores the sizes in dwords `+0x186C`/`+0x1870`, calls `0061E6B0` six times, calls virtual `+0x108` of qword `+0x110` with (the count, the array or null, qword `+0x688`), then `0061D3D0` and `0061EA80(rcx, edx)`, whose result it returns | `0061D50D`, `0061D5B7`, `0061D71F`, `0061D80D`, `0061D906` |
| `0061ECD0` | 22 B | tail-calls `00623B10(rcx + 0x708, qword +0x110, edx)` | `0061ECD3`, `0061ECDA`, `0061ECE1` |
| `0061ED00` | 102 B | around a stack object built by `00615BC0`: calls virtual `+0x178` of qword `+0x110` of `005FD050()` with qwords `+8` and `+0x10` of `rcx`, calls `005FD050()` again when `00225690(005FCF20())` returns 1, then calls `005CD7D0(005FCF20())` | `0061ED17`, `0061ED34`, `0061ED43`, `0061ED5A` |
| `00621FA0` | 70 B | when byte `+0x20` of `rdx` is set, calls `0061ED00(rdx)` and clears it; then calls virtual `+0x150` of qword `+0x110` with (qword `+8` of `rdx`, 0); returns 0 | `00621FAA`, `00621FBD`, `00621FC2`, `00621FD3` |
| `00622350` | 121 B | with `r9d` non-zero, maps `edx` through `0061C1C0`; for a non-zero result: when it differs from dword `01F2DEF8`, stores it there and calls the function pointer in `01F2DEF0` with (qword `+0x110`, the result); then calls virtual `+0x68` of qword `+0x110` with (`r9d`, `r8d`). Returns 0 when `0061C1C0` gives 0, else 1 | `0062236F`, `00622388`, `0062239F`, `006223B4` |
| `006223D0` | 124 B | maps `edx` through `0061C1C0`; for a non-zero result: when it differs from dword `01F2DEF8`, stores it there and calls the function pointer in `01F2DEF0` with (qword `+0x110`, the result); when byte `+0x20` of `r8` is set, calls `0061ED00(r8)` and clears it; then calls virtual `+0x140` of qword `+0x110` with (qword `+8` of `r8`, 0). Returns 1, or 0 when `0061C1C0` gives 0 | `006223E2`, `00622407`, `00622423`, `00622439` |
| `00623B10` | 251 B | for slot `r8d`, twice (byte counts dword `+0x20`/`+0x28` + 4*slot, targets qword `+0`/`+0x10` + 8*slot, sources qword `+0x38`/`+0x48` + 8*slot): when the count is non-zero, calls virtual `+0x70` of `rdx` with (target, 0, 4, 0, &out), copies the count of bytes from the source to the pointer in `out` with `00861EBA`, and calls virtual `+0x78` with (target, 0); returns 0, or 9 when the `+0x70` call returns negative or leaves a null pointer | `00623B2D`, `00623B5A`, `00623B7B`, `00623B8D`, `00623C04` |
| `00623F00` | 65 B | returns qword `+0` of 40-byte element `edx` of an array whose count is dword `+0x18` without bit 31 (at qword `+0x20` when the count is above 1, inline at `+0x20` when it is 1); 0 when `edx` is not below the count | `00623F03`, `00623F0C`, `00623F22`, `00623F27`, `00623F37` |
| `00626D90` | 41 B | stores `edx` in dword `+0x6F0` and zeroes the dwords at index `edx` of `+0x728`, `+0x730`, `+0x780` and `+0x788`; returns 0 | `00626D92`, `00626D9A`, `00626DAF`, `00626DB6` |
| `00627F10` | 102 B | zeroes dword `+0xA24`; stores `dl` in `+0xA28`, `0061BF40(r8d)` in `+0xA2C`, `0061BF40(r9d)` in `+0xA30`, 5 in `+0xA38` and 6 in `+0xA3C`; sets bit 1 of `+0x9C0`; returns 0 | `00627F1A`, `00627F36`, `00627F43`, `00627F53`, `00627F67` |
| `00627F80` | 112 B | zeroes dword `+0xA24`; stores `dl` in `+0xA28` and `0061BF40` of `r8d`, `r9d`, the fifth and the sixth argument in `+0xA2C`, `+0xA30`, `+0xA38` and `+0xA3C`; sets bit 1 of `+0x9C0`; returns 0 | `00627F8A`, `00627FA6`, `00627FC2`, `00627FD1`, `00627FE1` |
| `006281A0` | 113 B | unpacks `edx` as four bytes, each multiplied by 1/255 (`00D11104`): bits 16-23 into float `+0x7C0`, 8-15 into `+0x7C4`, 0-7 into `+0x7C8` and 24-31 into `+0x7CC` | `006281AD`, `006281C4`, `006281DE`, `006281F4`, `00628208` |
| `00628220` | 39 B | stores `xmm1`, `xmm2`, `xmm3` and the fifth (stack) float in floats `+0x7C0`, `+0x7C4`, `+0x7C8` and `+0x7CC` | `00628226`, `0062822E`, `00628236`, `0062823E` |
| `00628320` | 85 B | sets bit 1 of dword `+0x9C0` and stores in byte `+0xA44` a mask whose bits 0-3 say which of `dl`, `r8b`, `r9b` and the fifth argument's low byte are non-zero; returns 0 | `00628325`, `0062832D`, `00628344`, `00628356`, `0062836B` |
| `006283E0` | 141 B | returns 5 when `r8d` is 8 or above; otherwise copies 24 bytes from `rdx` to `+0x570 + 24*r8d` and returns 0. With `rdx` null the source is a stack record zeroed by `005DC1B0`, which is passed to `0016D6A0` afterwards | `006283F0`, `006283F6`, `00628416`, `00628437`, `00628447` |
| `006284B0` | 103 B | sets bit 0 of dword `+0x9C0` and zeroes dword `+0x9CC`; for `edx` 0, 1 or 2 also stores `edx + 1` in dword `+0x9C8` (other values leave it); returns 0 | `006284BE`, `006284C6`, `006284E4`, `006284F9`, `00628503` |
| `00628600` | 23 B | sets bit 2 of dword `+0x9C0` and stores 1 in dword `+0x9F0` when `dl` is non-zero, else 0; returns 0 | `00628604`, `00628607`, `0062860E` |
| `00628630` | 96 B | copies 24 bytes from `rdx` to `+0x630` and returns 0. With `rdx` null the source is a stack record zeroed by `005DC1B0`, which is passed to `0016D6A0` afterwards | `00628643`, `0062864F`, `00628662`, `0062866F`, `00628683` |
| `00629540` | 27 B | sets bit 0 of dword `+0x9C0` and stores 2 in dword `+0x9C4` when `edx` is 1, else 3; returns 0 | `00629545`, `00629548`, `0062954F`, `00629552` |
| `00629620` | 94 B | calls virtual `+0x168` of qword `+0x110` with (1, &{`edx`, `r8d`, `r9d + edx`, fifth argument + `r8d`}) | `0062963E`, `00629642`, `0062965A`, `00629666` |
| `007927C0` | 166 B | makes `+8` and `+0x18` self-linked list heads, stores `rdx` in qword `+0x28`, links the `+8` node in before the list head `01F401E8` (updating its back pointer at `01F401F0`), sets qword `+0` to `01CB23C0` and then `01CB2430`, zeroes the 0x100 bytes at `+0x231`, `+0x30` and `+0x130` with `00861EC0`, clears byte `+0x230` and sets byte `+0x331` to 0xFF; returns `rcx` | `007927DB`, `007927E9`, `00792815`, `00792822`, `00792859` |
