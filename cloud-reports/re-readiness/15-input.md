# Reconstruction readiness — `FFXII TZA/15-Input/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-RE-READINESS-INPUT-AUDIO-1001` |
| Date | 2026-10-01 |
| Snapshot | this repo's text snapshot only; no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. |

Citation form: `page:line` (path relative to `FFXII TZA/`) plus the section heading. "Not stated" means the
15-Input pages (and the one 16-UI section they defer to) say nothing on the point.

## Pages read

| page | status line as the page states it |
|---|---|
| `15-Input/README.md` | category index; lists six systems and the subsystem contract (`15-Input/README.md:11-19`) |
| `15-Input/CONTRACT-input-subsystem.md` | `readiness: CONTRACT READY # the ordering and the shared object are STATIC; no live capture of the frame order` (`:6`) |
| `15-Input/how-a-gamepad-becomes-a-controller-object.md` | `status: AUDITED` (`:4`) |
| `15-Input/Input-Stack/input-stack-device-channel-and-bindings.md` | `status: DOCUMENTED — all eight registered residues are answered (AP-4..AP-6, SD-5..SD-9)…` (`:4`); the body still opens "**PARTIAL.**" (`:32`) |
| `15-Input/Binding-Profiles/CONTRACT-binding-profiles.md` | `readiness: CONTRACT READY # the READ path is RUNTIME VALIDATED (EXP-005, EXP-006); assignment is not` (`:6`) |
| `15-Input/Binding-Profiles/binding-profiles-remapping-and-control-state.md` | `status: AUDITED — BP-5 / UQ-140 closed 2026-09-18 as NO ADMISSIBLE SOURCE…` (`:4`) |
| `15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md` | `status: AUDITED` (`:4`) |
| `15-Input/Input-Name-Registry/CONTRACT-input-name-registry.md` | `readiness: RUNTIME VALIDATED and DIFFERENTIAL TESTED` (`:6`) |
| `15-Input/Input-Name-Registry/the-input-name-registry-and-channel-aliases.md` | `status: AUDITED`, `readiness: DIFFERENTIAL TESTED` (`:4`, `:8`) |
| `15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md` | `status: DOCUMENTED - was REOPENED; both reopening triggers are resolved…` (`:4`) |
| `15-Input/Modal-Toggles/r2-force-fight-toggle.md` | `status: DOCUMENTED — every register row is closed…` (`:4`); the body still opens "**PARTIAL, deliberately.**" (`:32`) |
| `16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md` §6 | read only because the subsystem contract defers the snapshot field map to it (`15-Input/CONTRACT-input-subsystem.md:62-66`) |

The `.tsv` member files were not needed for any item below.

---

## 1. Interface

The system has five layers, which the pages describe in this order from the device up: **device objects** →
**backend control-code arrays** → **binding translation** (the input manager) → **channel layer** (history,
transitions, repeat, feedback) → **published gameplay snapshot** → **arbitration and the capability gate**.

### 1.1 Entry points

#### Startup

| entry | callers | what it does | cite |
|---|---|---|---|
| `InputManager_CreateSingleton` `00198750` | `0017D4C0` (Engine Core Runtime startup) | owner transition into Input; calls `InputManager_Initialize` | `Binding-Profiles/keymap-ini-file-format-and-default-controls.md:694-703` (§5) |
| `InputManager_Initialize` `00195060` (153 B) | `00198750` (call at `0019877E`) | `memset(01F80F90,0,0x150)`, build path, load ini, validate twice, then publish (`00195DF0`) if both validators return 0, else install defaults (`00198B60`) | `…/keymap-ini…md:106-118` (§2); `Input-Stack/input-stack-device-channel-and-bindings.md:395-403` (§3b) |
| `InputManager_BuildKeymapPath` `00197EE0` | `00195060` | `<Documents>\My Games\FINAL FANTASY XII THE ZODIAC AGE\<SteamID64>\keymap.ini` into buffer `01F80D90` | `…/keymap-ini…md:83-104` |
| `InputManager_LoadKeymapIni` `00198000` (1,644 B) | `00195060` | line parser, name→slot lookup through `01DF11E0` | `…/keymap-ini…md:120-194` |
| `InputManager_ValidateBindingUniqueness` `00196550` | `00195060` | returns 1 on any duplicate non-zero code in 84 slots or any reserved code | `…/keymap-ini…md:634-646` |
| `InputManager_ValidateBindingIdRanges` `001965E0` | `00195060` | see Gaps G-C1x: the pages disagree on what it checks | `…/keymap-ini…md:648-662`; `Input-Stack/…md:301` |
| publisher `00195DF0` (GFZ name `RestoreDefaultBindingProfiles`, backwards) | `00195060`; `001E1050`; `001E0F70` | `0x70` authored profile → `0x15C` runtime record, Circle/Cross swap, copy to `01F80130`, set `mgr[0x3B]=1` | `Binding-Profiles/CONTRACT-binding-profiles.md:258-313` (§7a) |
| defaults installer `00198B60` (GFZ name `MaterializeRuntimeBindingProfiles`, backwards) | `00195060`; `001E0F70` | installs `01DF09C0` / `01DF0A80` / `01DF1470` over `01F80F90` and the records | `…/keymap-ini…md:780-800` |
| CRT bank initialisers `0015BD30`, `0015C0D0`, `0015BF20`, `0015C280` | CRT (before `main`) | build banks `01F80130`, `01F80550`, `01F80970` and bank-A record 1 | `Binding-Profiles/binding-profiles-remapping-and-control-state.md:1482-1499`; `…/keymap-ini…md:928` (UQ-143) |
| name-registry inserts `00879570` (channels), `00876C80` (keys) | one CRT static initialiser per name (`lea rcx,[node]; call; lea rcx,[dtor]; jmp atexit`) | push-front into a string-keyed list with duplicate rejection | `Input-Name-Registry/CONTRACT-input-name-registry.md:44-68`, `:119-122` (§2, §6) |
| DirectInput start-up `00797910` | not stated | Steam controller interface, `DirectInput8Create`, `EnumDevices` with callback `00796230` | `how-a-gamepad-becomes-a-controller-object.md:33-38` (§1) |
| keyboard device creation `007973D0` | not stated | `CreateDevice`, `SetDataFormat(01CC7150)`, `SetCooperativeLevel(hwnd,6)`, `Acquire` | `Input-Stack/…md:183-190` (§2) |

#### Per frame / per poll

| entry | callers | what it does | cite |
|---|---|---|---|
| frame dispatcher `0022A580` | not stated (frame driver) | in modes 2, 3, 5 of byte `02064AD3` releases the input worker via `0035E9B0` | `Input-Stack/…md:237-254` |
| `InputControl_WorkerDeadlineLoop` `0035EA40` (thread) | thread start | waits on semaphore `022CA610`, then releases the vsync-callback thread | `Input-Stack/…md:243-245`, `:493-501` (AP-7) |
| `InputControl_UpdateFrame` `0035EC90` | vsync-callback thread `00369100`, slot 0 | `inc qword [022CA5E0]`, then `UpdateRegisteredChannels` | `Input-Stack/…md:246-248`; `:380-393` (§3b) |
| `InputControl_UpdateRegisteredChannels` `0035FCA0` | `0035EC90` at `0035ED2B` | per channel: timing (`0035F690`), poll + build history (`0035F420`) | `Input-Stack/…md:382-384` |
| `InputControl_PollAndBuildChannelHistory` `0035F420` | `0035FCA0` at `0035FD85` | bridge poll into `022CB680`; per-button bytes; transitions builder, analog builder, feedback | `Input-Stack/…md:384-393`; `:469` (AP-6) |
| `InputManager_PollAndBuildControlState` `00196FF0` (356 B) | bridge `00862670` → `001E09B0` (tail-jumps) | gate `mgr[+0x39]`; `InputSystem_UpdateRegisteredDevices`; translator over bank A (5 records), B (3, gated), C (3, gated) | `Binding-Profiles/CONTRACT-binding-profiles.md:213-256` (§7); `Input-Stack/…md:176` |
| `InputManager_TranslateBindingProfileToControlState` `00197160` (1,406 B) | `00196FF0` | one record → accumulates into the 18-byte control frame | `Binding-Profiles/CONTRACT-binding-profiles.md:371-418` (§12) |
| `InputSystem_UpdateRegisteredDevices` `007999E0` | `00196FF0` at `0019702D` (only caller) | hot-plug re-enumeration if `02EA5363`, then device vtable `+0x28` over list `01F401E8` | `Input-Stack/…md:252`; `Binding-Profiles/binding-profiles…md:1661-1676` |
| `DirectInputKeyboard_PollState` `007A1640` | device vtable slot 5 | `GetDeviceState(256)`, writes level `+0x231` through remap `01F3DAB0` | `Input-Stack/…md:196` |
| backend transition pass `0079D010` | `PApplication` slot 28 `0079C140` (at `0079C260`) | writes `+0x130` and latch `+0x30`; mouse `+0x1E0/+0x1E3`; pads `+0x88` | `Input-Stack/…md:197-213` |
| `InputGameplay_RebuildFrameSnapshotFromChannelHistory` `002498B0` | `call` at `0022A7F6` (`0022A770`), `0022B908` (`0022B8C0`), `0022BC50` (`0022BC20`); tail-`jmp` at `00249C4D` (`00249C30`) — mutually exclusive per frame | zeroes `02F97360..02F97398`, ORs channel history masks back in | `CONTRACT-input-subsystem.md:158-202` (I-1), `:355-369` (GG-2) |
| reconciler `00313A00` (289 B) | `00234590` (once per slot iteration, at `00234624`); `00313DB0` | writes capability row 2 | `CONTRACT-input-subsystem.md:97-105`; `Gameplay-Capability-Policy/capability-inhibition-policy.md:278-281` |
| arbiter `InputGameplay_ArbitrateDigitalInputAndModalState` `00253C70` (1,599 B) | only `00253C50` (at `00253C56`), reached only via thunk `002E0D90` from `00314020` | once per tick, after the reconcile loop | `CONTRACT-input-subsystem.md:120-152` (§4) |
| on-demand binding predicates `0017DDC0` (L2), `0017DE10` (R2), `0017DEA0` (Speed1/2/3), `0017DFC0` (WalkMode) | arbiter (`002541D4` → `0017DE10`); `0022A770` (`0017DEA0`); `003594E0` (`0017DFC0`); others not stated | `GetBinding(profile index 0, group, slot)` → `0079E6A0(be, code, 0)` | `…/keymap-ini…md:254-286`, `:731-747` |
| mouse-button accessor `001E0E00(i)` | battle text banks (cited there) | `0079E6D0(be, i+1)` | `Input-Name-Registry/the-input-name-registry…md:186-205` |
| feedback `InputControl_UpdateDeviceFeedbackOutput` `0035F590` | `0035F420` at `0035F548` | motor bytes `022CB5C0` → `008628F0` → `001E1120` → `00198E80` | `Input-Stack/…md:176`; `Binding-Profiles/binding-profiles…md:365` (BP-4) |

#### Player configuration (options screen)

| entry | callers | cite |
|---|---|---|
| `InputConfig_AssignBindingAndRepublish` `001E1050` → assigner `00198A00` → publisher `00195DF0` | three sites in widget proc `0023C5C0` (messages 13 and 10) | `Binding-Profiles/binding-profiles…md:779-791` |
| `InputConfig_ResetBindingsToShippedDefaults` `001E0F70` (Materialize then Restore) | not stated | `…/keymap-ini…md:722-729`, `:792-798` |
| `InputConfig_SaveKeymap` `001E0F40` → writer `001993B0` | not stated | `…/keymap-ini…md:196-211`, `:728-729` |
| generic getters `001E0BD0`, `001E0AA0` | 10 callers / 15 sites (`001E0BD0`) | `…/keymap-ini…md:281`, `:396-397` |

### 1.2 Inputs and outputs (data read and written, with record layouts)

**Device objects.** Base controller constructor `00792940`: list node `+8` into `01F401E8`, DirectInput device
`+0x28`, two 17-byte button arrays `+0x30` (now) / `+0x41` (before), sticks/triggers to `+0xA8`, four
`0x48`-byte sub-objects at `+0xB0`, state words `+0x414..+0x450`, `0x244`-byte descriptor copy at `+0x1D0`
(instance GUID `+0x1D4`). Sizes: DirectInput `0x458`, XInput `0x470` (user index `+0x458`), Steam `0x458`
(`how-a-gamepad-becomes-a-controller-object.md:83-95`, §4). Precedence (corrected): XInput or DirectInput
exclusively, Steam additive and suppressing only DirectInput, at most four XInput pads (`:115-121`, §7;
`:229`, G5).

**Keyboard object** `PFramework::PInputDeviceKeyboard`, `0x338` B: `+0x30` u8[256] transition latch (what game
code reads), `+0x130` u8[256] previous level, `+0x231` u8[256] polled level; index = keymap code − 28, mapped
to `DIK_*` through `01F3DAB0` (`Input-Stack/…md:192-205`, §2; `:346-349`, §3a).

**Backend control-code bands** (the three predicates' own guards and arrays):

| codes | backend | device / array | cite |
|---|---|---|---|
| 1–3 (mouse) | `0079E6D0` | `[be+0x150]` device, byte `+0x1E0+(code−1)`; previous `+0x1E3` | `Binding-Profiles/binding-profiles…md:385-406` |
| 11–27 (pad, any device) | `0079E650` | 18 slots at `[be+0x88]`, byte `[code−0x0B+slot+0x30]` | same, and `:547-553` |
| 28–283 (keyboard, per bank) | `0079E6A0` | bank `r8d<7` at `[be+bank*8+0x118]`, byte `[code−0x1C+bank+0x30]` | same; the binding ladder routes only 28–152 (`:95-109`) |

Codes 0 and 4–10 have no storage in any device model (`Binding-Profiles/binding-profiles…md:417-423`). Code 27 is a
DirectInput pad's 17th button (`…/keymap-ini…md:883-887`).

**Authored binding profile** — `01F80F90`, 3 profiles × 28 u32 (stride `0x70`), groups 0/1/2 = 16/8/4 slots at
`+0x00/+0x40/+0x60`; zero at load; slot names and order in `…/keymap-ini…md:489-531` (§4).

**Runtime binding record** — stride `0x15C`, translator reads `0x140`:
`+0x000` int[16] digital codes → mask bits 0–15; `+0x040` 16 × `{kind/mode, subKind/axisId, codeA, codeB}`;
`+0x140..+0x15B` "zeroed by the defaults path" (`Binding-Profiles/CONTRACT-binding-profiles.md:88-101`, §3.2;
`…/keymap-ini…md:675-690`; kinds 1–4 in `…/keymap-ini…md:952`, UQ-144).

**Banks polled each frame** (`Binding-Profiles/CONTRACT-binding-profiles.md:213-235`, §7; contents from
`…/keymap-ini…md:926-949`, UQ-143):

| bank | records | gate | contents |
|---|---:|---|---|
| A `01DF1480` | 5 | none beyond `mgr[+0x39]` | rec 0 gamepad, rec 1 mouse, recs 2–4 the three keyboard layouts |
| B `01F80550` | 3 | `mgr[+0x3A] & 2` | head `Z`→Select, `X`→R3; `+0x40` from zero block `01F7FFF0` |
| C `01F80970` | 3 | `mgr[+0x3A] & 5` | same heads |

**Control frame** (output of `00196FF0`), 18 bytes: `+0x00` u16 digital mask, **active-low**, initialised
`0xFFFF`; `+0x02` 16 axis bytes, axes 0–3 initialised `0x80`, 4–15 `0`; the translator **accumulates** across
records (`Binding-Profiles/CONTRACT-binding-profiles.md:108-126`, §3.3; `:243-256`, §7). Formula and mode
arithmetic: `:371-418` (§12).

**Channel record** `R = 022CAE90 + channel*0x294` (2 channels, 660 B): header `+0x00` write cursor, `+0x01`
read cursor, `+0x02` channel index, `+0x03` stick threshold (init `0x68`), `+0x04`/`+0x05` repeat initial
delay / rate (init `0x0C`/`0x05`), `+0x08` lookback count, `+0x09` flags (bit 1 stick-as-D-pad; bit 2 feedback
enable; bit 4 timing "held" branch), `+0x0B`/`+0x0C` scale bytes (init `0x90`/`0x00`), `+0x0D` dead-zone (init
`0x20`), `+0x24..` repeat countdowns, `+0x34` u16[8] button-group words, `+0x44` 16 frames × 36 B
(`Input-Stack/…md:355-372`, §3a; flags bits 2 and 4 from
`Binding-Profiles/binding-profiles…md:243`, `:365`). Timing state `+0x10` phase, `+0x12` hold timer, `+0x14`
sub-counter, `+0x16` accumulator, `+0x18` rate (`Binding-Profiles/binding-profiles…md:238-283`).

**History frame** (36 B): `+0x00` channel index, `+0x02` raw mask, `+0x04/+0x06` held (set 0 / set 1),
`+0x08/+0x0A` auto-repeat, `+0x0C/+0x0E` newly pressed, `+0x10/+0x12` released, `+0x14` u8[16] per-button bytes
(`0x80` rest for i<4, else 0) (`Input-Stack/…md:333-339`, §3a; semantics `:469`, AP-6).

**Published gameplay snapshot** `02F97360..02F9739B` (0x3C B). Channel-0 words, in order: `+0x06`,
`+0x0E`, `+0x0A`, `+0x12`, `+0x04`, `+0x0C`, `+0x08`, `+0x10` of the history frame
(`Input-Stack/…md:465-466`), i.e. `02F97368` held, `02F9736A` newly pressed (edge, consumed),
`02F9736C` repeat, `02F9736E` released (`CONTRACT-input-subsystem.md:58-81`, §2;
`16-UI/Config-Screen/…md:196-210`). For the rest of the band see Gaps G-A1.

**Capability policy** `0215F1C0..0215F1FF`, 16 rows × u32; aggregate `002E0FA0` = OR of all rows, then clear
bit 19 if `00360360(0x10) != 0` (`Gameplay-Capability-Policy/capability-inhibition-policy.md:288-322`).
Primitives `002E1C20(row,bit)` set, `002E1CA0` clear, `002E1020(row)` read, `002E1CD0(on,row)` mask `0x139203`
(clears when `ecx != 0`, corrected) (`:52-58`, `:484-505`, `:1018-1028`). Projection table `01E0C2C0`
u32[22] policy bit → UI request mask, applied by `00254500` (`:78-102`). Row 2 bits 0–8, 10, 11, 12, 20 by
`00313A00` (`:1056-1063`, F3); row 1 bit 21 by Save/Load and others (`:472-526`, SD-3 at `:231-242`).

**Confirm / cancel masks** `01E0C2A0` (confirm) / `01E0C2A4` (cancel) = `0x2000`/`0x4000`, exchanged by
`DecideButton` (`GameSetting+0x64`, read as a **dword** by `001DFA70`)
(`CONTRACT-input-subsystem.md:248-255`; `Binding-Profiles/CONTRACT-binding-profiles.md:130-138`).

**Arbiter reads and writes** — table in `CONTRACT-input-subsystem.md:126-138` (§4): reads aggregate
`002E0FA0`, `02F9736A`, `02F97392`, `02F97360` bit `0x200`, live binding `0017DE10`, field bit `00377C20`;
writes `02F9736A ← 0` at five sites and calls the UI request router `00254B50`. R2 toggle globals `020927E0`
(toggle), `020927E4` (edge latch), `01E0C2B4` (sticky) are owned by the arbiter alone, and the force-fight
flag `01E0C2B8` is written through `00252B60` → `00252C80`
(`Modal-Toggles/r2-force-fight-toggle.md:93-124`, `:178-210`, `:322-354`).

**On-demand slots and their outputs**: speed mode `01FD4A98` → scalar `02064AC4 = {1.0,2.0,4.0}[mode]` when
`02064AD2` set; walk flag `022C800C` toggled on rising edge (`…/keymap-ini…md:288-344`).

**Name registry nodes** (32 B): `+0x00` vtable, `+0x08` name, `+0x10` next, `+0x18` value (= keymap code, no
offset); heads `02EB9D80` (143 channel names, 113 channels, 16 alias groups) and `02EB83B8` (97 key names)
(`Input-Name-Registry/CONTRACT-input-name-registry.md:70-82`; `Input-Name-Registry/the-input-name-registry…md:336-358`).

**File I/O**: `keymap.ini`, ASCII, LF, 87 lines, grammar at `…/keymap-ini…md:461-487`; written only on the
options-screen save (`:728-729`).

### 1.3 State (globals and objects, with lifetime)

| state | lifetime / initial value | cite |
|---|---|---|
| input manager `[01F7FFE0]`; `+0x08/+0x09` axis-invert bytes; `+0x0C/+0x10` wheel accumulators; `+0x38` stick-touched; `+0x39` poll gate (init 1, word `0x100` at `+0x38`); `+0x3A` mode bits; `+0x3B` dirty one-shot | created at startup by `00198750`; `+0x39` only ever cleared afterwards (SD-7); `+0x3A` set/cleared by system-stop slot arms, reset to `0x100` on field transition; `+0x3B` set by publisher, consumed by the poll | `Input-Stack/…md:256-266`, `:507-522`; `…/keymap-ini…md:892-903`, `:928-939`; `Binding-Profiles/CONTRACT-binding-profiles.md:164-170` |
| application object `[02EA5368]`, `+0xDF8` backend, backend `+0x118..+0x148` seven device pointers, `+0x150` mouse | built by `00792350`; device list filled by `0079E3D0` | `Input-Stack/…md:183-190`; `Binding-Profiles/binding-profiles…md:1456-1467` |
| registered-device list `01F401E8` | grows on start-up and every device arrival; nothing removes an object | `how-a-gamepad-becomes-a-controller-object.md:108-113` |
| hot-plug byte `02EA5363`, XInput count `02EA9500`, sticky XInput byte `02EA5379`, Steam handles `02EA95A0`/`02EA9510`/`02EA9590` | set by window proc / enumeration; Steam handles rewritten by every Steam object | `how-a-gamepad-becomes-a-controller-object.md:55-58`, `:66-69`, `:97-106`, `:233` |
| authored profiles `01F80F90` | zero-filled (beyond `.data` raw end `01F7E400`), cleared again by `00195060`, filled by ini or defaults, edited by `00198A00` | `Binding-Profiles/binding-profiles…md:58-62`, `:608-621` |
| runtime banks `01DF1480`, `01F80130`, `01F80550`, `01F80970` | CRT initialisers before `main`; republished by `00195DF0`; reinstalled by `00196680` when `+0x3B` set | `Binding-Profiles/binding-profiles…md:1337-1343`, `:1482-1499` |
| channel records `022CAE90` ×2 | initialiser `0035F260` (caller not stated); updated per poll | `Input-Stack/…md:355-372` |
| poll counter `022CA5E0`; worker semaphores `022CA610`, `022CFEEC`; gate `022CA5F8` | `+1` per poll; gate set once at `0035E84D` | `Input-Stack/…md:240-248`, `:317` |
| "60fps input" byte (settings `+0xD07`) | constructor stores 1; only other store is console arm 208 | `Input-Stack/…md:256-259` |
| snapshot `02F97360..9B` | rebuilt each frame; wiped also by `002284F0` msg 2 and `002A3250` | `CONTRACT-input-subsystem.md:212-227` |
| capability table `0215F1C0` | initial value: see Gaps G-B2 | `Gameplay-Capability-Policy/…md:317-322` |
| R2 toggle `020927E0`, latch `020927E4`, sticky `01E0C2B4`, suppress latch `020927CC`, play-clock pause `020927C8` | `020927CC` set on field-slot-0 unload (`00252DE0`), cleared on field UI rebuild (`00253A30`) | `Modal-Toggles/r2-force-fight-toggle.md:304-320`, `:496-516` |
| arming block `022CBE18` (counter), `022CBE1A` (state word), `022CBE08` (threshold `30 × [01DFE0B4]`), `022CBE1C` (sound handle) | threshold written by widget construct arm `00366B80`; widget rebuilt with each area's UI | `Modal-Toggles/r2-force-fight-toggle.md:212-256`, `:427-439` |
| speed mode `01FD4A98`, latch `01F7F4E9`, scalar `02064AC4`, enable `02064AD2`; walk flag `022C800C`, latch `022C7FF9` | as stated at the cite | `…/keymap-ini…md:446-453` |
| name lists `02EB9D80`, `02EB83B8` | built before `main` in CRT order (`Empty` first, then descending value); unlink in destructor | `Input-Name-Registry/CONTRACT-input-name-registry.md:173-182`, `:124-132` |

### 1.4 Order (what runs when in a frame, and what triggers it)

1. **Device poll (worker thread).** The dispatcher `0022A580` releases `0035EA40` in modes 2, 3, 5; the
   vsync-callback thread `00369100` runs `0035EC90` → `0035FCA0` → per channel `0035F690` (timing) and
   `0035F420` (poll → bridge → `00196FF0` → `007999E0` → device polls; then transitions builder `0035FAC0`
   **first**, analog builder `0035F760` **second**, feedback `0035F590`)
   (`Input-Stack/…md:237-254`, `:380-393`; builder order `:469`). No poll in modes 0, 1, 4, 6 or once
   `+0x39` is cleared (`:270-271`).
2. **Within `00196FF0`:** gate `+0x39`; device update; if `+0x3B`, `00196680` reinstalls profiles and
   re-latches left-stick keys; init frame; bank A ×5, then B, then C; copy 18 bytes out
   (`Binding-Profiles/CONTRACT-binding-profiles.md:213-235`; `Binding-Profiles/binding-profiles…md:1337-1343`).
3. **Main frame:** `0022B908` publish snapshot (`002498B0`) → … → `0022BA23` world tick `00314020`
   → reconcile loop (`00313A00` per slot; slots 3–4 in battle mode, 0–4 in field mode) → once, arbiter
   `00253C70` (`CONTRACT-input-subsystem.md:83-118`, §3). The same publish-then-tick shape holds on all four
   frame paths (`:171-181`).
4. **Field frame `0022A770`:** rebuild < pause step < UI focus delivery `002507C0(1)` at `0022AB83` (gated)
   < world tick < `002507C0(1)` at `0022AC17`; one reader (`00277ACD`) is so ordered
   (`CONTRACT-input-subsystem.md:337-354`, GG-1). Speed keys polled in `0022A770`
   (`…/keymap-ini…md:290`).
5. **Arbiter internal order (R2):** latch → `00252B60` gates → acquire counter → engaged bit → `00252C80`
   flag write; the label widget reads after, in the UI walk (`Modal-Toggles/r2-force-fight-toggle.md:453-466`).
6. **Mid-frame wipes:** `002284F0` message 2 (pause-menu cancel-to-close guard, sent by walker `00248030`) and
   `002A3250` (message-window opener) zero snapshot words (`CONTRACT-input-subsystem.md:236-258`, `:400-415`).

Triggers: device arrival (`02EA5363`), options-screen assign/reset/save, system-stop slot holds (bank gates),
area change (R2 suppress latch), `DecideButton` change.

### 1.5 Dependencies (on other systems)

| system | dependency | cite |
|---|---|---|
| 00 Engine Core Runtime | frame dispatcher `0022A580`, main loop, world tick `00314020`, system-stop registry (bank gates), startup `0017D4C0` | `CONTRACT-input-subsystem.md:443-451`, `:483-485`; `…/keymap-ini…md:928-939` |
| 03 World/Area/Field | field record bit 15 via `00377C20` (arbiter, row 2 bit 10, R2 pin) | `Gameplay-Capability-Policy/…md:160-183`; `CONTRACT-input-subsystem.md:532` |
| 07 Combat Action | `02089350` selected unit and ring `022BEDA4` feed the reconciler | `Gameplay-Capability-Policy/…md:137-155` |
| 11 Party | reads history via `0035EEB0`; WalkMode via `0017DFC0`; leader suppression `0023B040` | `Input-Stack/…md:970-975`; `…/keymap-ini…md:330-344`; `Gameplay-Capability-Policy/…md:528-646` |
| 14 Story | persistent flag query `0032A8A0` in the arbiter | `CONTRACT-input-subsystem.md:467-469` |
| 16 UI | request router `00254B50`; widget walker `00248030`; config screen proc `0023C5C0`; snapshot field map §6 | `CONTRACT-input-subsystem.md:62-66`, `:487-490`; `Binding-Profiles/binding-profiles…md:779-791` |
| 18 Audio | `00229AF0` reads aggregate bit 21; R2 toggle acquires repeating SE 82 of `se000.seb`; config screen sound slots via `00249C60` | `CONTRACT-input-subsystem.md:462-466`; `Modal-Toggles/r2-force-fight-toggle.md:476-484`; `Binding-Profiles/binding-profiles…md:793-799` |
| 19 Save/Load/Settings | `GameSetting.ini` `DecideButton` (`+0x64`), `FrameLimit`; Save/Load writes row 1 bit 21 | `…/keymap-ini…md:226-239`; `Gameplay-Capability-Policy/…md:427-445` |
| 20 Platform | Steam user id in the keymap path; Steam Input action set `Global` | `…/keymap-ini…md:96-101`; `how-a-gamepad-becomes-a-controller-object.md:97-106` |
| 22 PhyreEngine / OS | DirectInput 8, XInput (`xinput1_3.dll` ordinal 100), Steam API, Phyre `PInputs` semantics | `how-a-gamepad-becomes-a-controller-object.md:232`; `Input-Name-Registry/CONTRACT-input-name-registry.md:81-82` |
| 24 CRT | static-initialiser order for name registration and bank initialisers | `Input-Name-Registry/CONTRACT-input-name-registry.md:173-182` |
| 00 Force-fight mode | `01E0C2B8` consumers | `Modal-Toggles/r2-force-fight-toggle.md:371-387` |

---

## 2. Gaps

### 2.1 Gaps the pages state themselves (open or live-only)

| id | gap | cite |
|---|---|---|
| G-L1 | **No frame order observed live.** "Readiness is `CONTRACT READY`, not `RECONSTRUCTION READY`." | `CONTRACT-input-subsystem.md:416-417` |
| G-L2 | **GG-1: 50 of the snapshot's 51 readers are not placed** relative to the arbiter; also unknown whether the focus proc is reached through the arbiter's callees, and the live values of the `0022AB83` gates (bit 3 of `022C7F92`, the `02064AC0` float, MXCSR.DAZ). | `CONTRACT-input-subsystem.md:333-354` (`:351-352`) |
| G-L3 | **GG-3 residue:** `002284F0`'s behaviour inside a live widget tree, and which frames reach the walk in play. | `CONTRACT-input-subsystem.md:392-396` |
| G-L4 | **Assignment, conflict swap, publication, pair swap, three-bank poll order and channel timing never observed live**; no experiment drove `00198A00` or saw `01F80130` change. | `Binding-Profiles/CONTRACT-binding-profiles.md:478-479`, `:568` |
| G-L5 | **Translator `00197160` and assigner `00198A00` not reimplemented / differential-tested** (only `00195DF0` is). | `Binding-Profiles/CONTRACT-binding-profiles.md:647-649` |
| G-L6 | **Gamepad kinds' poll methods, the `EnumObjects` callback, the mouse and keyboard enumeration arms, and removal behaviour: "Not read."** Whether duplicate Steam objects double input "depends on each kind's poll, which is still not read." | `how-a-gamepad-becomes-a-controller-object.md:111-113`, `:123`, `:243` |
| G-L7 | **AU-4: number of sub-profiles in blocks 2 and 3** (`01F80550`, `01F80970`) is open; references show what is touched, not what is reserved. | `Binding-Profiles/binding-profiles…md:1515-1520` |
| G-L8 | **UQ-146:** whether `001F3ED0`'s dangling stack-buffer return is clobbered depends on the installed `ucrtbase.dll`; live half carried by `FABLE-REQ-ASTRA-UQ146-IN-PROCESS-FORMATTER-READ`. A re-implementer cannot know which folder the real game writes `keymap.ini` into when the CRT misbehaves. | `…/keymap-ini…md:964-1024` |
| G-L9 | **UQ-147 live remainder:** the mode-1 counterpart unit's role and the scheduling/initialisation of its selection in `0023B040`; `FABLE-REQ-ASTRA-LEADER-STATS-NULL`. | `Gameplay-Capability-Policy/…md:707-714`, `:1098-1100` |
| G-L10 | **Name registry INTEGRATION**: only the insert is reconstructed; destructor, two lookups and the enumerator are "understood and not reimplemented"; runtime registrations from data are not ruled out. | `Input-Name-Registry/the-input-name-registry…md:331-333`, `:400-402` |
| G-L11 | **Analog semantics are absent from the name registries** ("Every name recovered is a button or a key"). | `Input-Name-Registry/the-input-name-registry…md:403-404` |
| G-L12 | **`0023C5C0`'s screen, command `0x2CA1` and row 0 are not read** — the caller of the assigner's swap flag is only partly identified. | `Binding-Profiles/binding-profiles…md:790-791` |
| G-L13 | **`001967D0`**: what it does with a 1–3 code in the Circle/Cross slot "was not read in this pass". | `…/keymap-ini…md:250-252` |
| G-L14 | **`001E0C10`'s eleven callers (`00276AF6` … `00393C6E`) "were not each read".** | `…/keymap-ini…md:902-903` |
| G-L15 | **Mouse wheel** is inferred from `WHEEL_DELTA` (120.0); "the device driver was not read to confirm channel 3". Consumers of `[01F7FFE0]+0x0C`/`+0x10` are not stated. | `Binding-Profiles/binding-profiles…md:1047-1062` |
| G-L16 | **Feedback update rate per second "is not read here"**, so the rumble cut-off (1,760 updates, 180-update recovery) has no wall-clock duration. | `Binding-Profiles/binding-profiles…md:365` |
| G-L17 | **Which game mode each `+0x3A` bit stands for** rests on stop-slot names, "not from a live observation". | `…/keymap-ini…md:939`, `:948-949` |
| G-L18 | **UQ-152 bound:** thread cones are direct-call only; an indirect call from a thread into the force-fight surface would not appear. | `Modal-Toggles/r2-force-fight-toggle.md:514-515` |

### 2.2 Gaps found while mapping the interface (not registered on the pages)

**A. Snapshot and arbitration**

| id | gap | where it shows |
|---|---|---|
| G-A1 | **The snapshot's field map is incomplete.** Only channel 0's eight words are named. The band is `0x3C` bytes; the Config page says the rebuilder ORs "for each of the two channels (a 0x14-byte record)", which accounts for `0x28`. Channel 1's words, the 20-byte per-index records read by `00249860`/`00249880` (`byte[02F97370+20·i]`, `byte[02F97371+20·i]`), and `02F97392` (the "filtered word" the arbiter reads, written by `002498B0`) have **no stated meaning**. | `CONTRACT-input-subsystem.md:62-66`, `:130`, `:283`, `:296-300`; `16-UI/Config-Screen/…md:199-210` |
| G-A2 | **How many history frames the rebuilder ORs** ("over the lookback frames") and whether it uses the lookback count at `R+0x08`: not stated. The per-frame cursor step that writes `+0x08` is cited only as "(B4)" to an external control. | `16-UI/Config-Screen/…md:200-201`; `Input-Stack/…md:359`, `:364` |
| G-A3 | **The arbiter's decision logic is not written down.** The contract lists its reads, its five clear sites and two router calls (`002540D2`, `002541C7`), but not which button press raises which UI request, under which modal state; the page with the arbiter as its subject is a contract that "deliberately restates none" of that. A re-implementer cannot write `00253C70` (1,599 B) from 15-Input. | `CONTRACT-input-subsystem.md:120-152`, `:44-45` |
| G-A4 | **The story flag the arbiter queries** (`0032A8A0` at `00253F21`, `002540AF`): "Which flag, and what it gates, is not read here and is not claimed." | `CONTRACT-input-subsystem.md:467-469` |
| G-A5 | **`0035EF10(0, 0)`**, the value the I-5 swallow compares the held mask with, is named but not described; nor is the precondition object `[[0209AC30]+0x308]`. | `CONTRACT-input-subsystem.md:243-246` |
| G-A6 | **Producer/consumer threading.** The channel records are written on the vsync-callback thread (`00369100`); the snapshot is rebuilt on the frame path (`0022B908`). No page states how the two are synchronised, or whether the rebuild can see a half-written frame. | `Input-Stack/…md:240-254`; `CONTRACT-input-subsystem.md:89-93` |
| G-A7 | **Field-arm dead branch:** the per-slot gate `00267310` is "never reached from this body"; whether other callers of the tick pass a non-zero `r13d` is not stated (the contract reads one body). | `CONTRACT-input-subsystem.md:113-118` |

**B. Capability policy**

| id | gap | where it shows |
|---|---|---|
| G-B1 | **Aggregate bit 19 and its clear predicate `00360360(0x10)`**: neither the bit's meaning nor the predicate's body is stated. | `Gameplay-Capability-Policy/…md:311-322` |
| G-B2 | **Initial value of the 16 rows at `0215F1C0`** and who resets them on boot/area change: not stated. | `Gameplay-Capability-Policy/…md:317-322` |
| G-B3 | **Complete row-ownership map.** The page names row 2 (`00313A00`), row 1 bit 21 (Save/Load plus the movie player, `0023FBE0`, `002CEB40`, `003939B0`), row 0 (`00394070`), rows 0/3/6 via `002E1CD0`, and "the rows 2/8 restore loop `00229510`"; the full census of "all 77 set/clear call sites" is in an external record, not on the page. Owners and bits of rows 4, 5, 7, 9–15 are not stated. | `Gameplay-Capability-Policy/…md:219-223`, `:236-242` |
| G-B4 | **Meaning of aggregate bits read directly by gameplay** — the page lists bits 0, 4, 5, 6, 9, 10, 11, 18, 21 as tested, and gives readers for 4, 5, 10, 18, 21; the behavioural meaning of bits 0–3, 6, 8, 9 outside the UI projection, and of bit 18 (`003C8B70`) and bit 5 (`00283270`), is not stated. | `Gameplay-Capability-Policy/…md:118-119`, `:224-230` |
| G-B5 | **UI requests 14 and 21** are "valid-but-unnamed slots". | `Gameplay-Capability-Policy/…md:100-102` |
| G-B6 | **`00237260`** ("policy-side predicate, 126 B, ORs with policy bit 10") is named only. | `Modal-Toggles/r2-force-fight-toggle.md:150`, `:291` |

**C. Channel layer and feedback**

| id | gap | where it shows |
|---|---|---|
| G-C1 | **Who sets the channel feedback inputs** — flags `+0x09` bit 2 (feedback enable) and bit 4 (timing "held" branch), and strengths `+0x06`/`+0x07` — is not stated; only the initialiser's clear of bit 1 is. There is no stated game-side "start rumble" entry. | `Binding-Profiles/binding-profiles…md:243`, `:365`; `Input-Stack/…md:365` |
| G-C2 | **Channel 1.** The poll runs channel 0 "on every tick (the skip bit is set only on an availability value the always-1 stub never returns)"; what channel 1 is, and when it is polled, is not stated. | `Input-Stack/…md:249` |
| G-C3 | **Caller and timing of the channel initialiser `0035F260`**: not stated. | `Input-Stack/…md:355` |
| G-C4 | **`InputBackend_UpdateResolvedDeviceState` `007A2440`** (3,269 B, "largest in the stack") and **`InputBackend_GetFilteredAnalogAxisValue` `0079D1D0`** (327 B, the analog filter kind-3 bindings call) are listed with sizes but **no body is described**: the stick dead-zone/filter at the backend is not stated. | `Input-Stack/…md:303-304`; `…/keymap-ini…md:952` |
| G-C5 | **Deadline constants** `−16.0`/`17.0` at `00908D60`/`00908D58`: what the worker waits for in wall time is not stated (SD-9 settles only `0035E7A0`). | `Input-Stack/…md:496-501` |

**D. Bindings**

| id | gap | where it shows |
|---|---|---|
| G-D1 | **Kind-3 analog scaling.** UQ-144 says the value is "scaled by the sensitivity constant and doubled again by the invert bytes"; the contract's §12 formula has no sensitivity factor. The constant and its value are not stated. | `…/keymap-ini…md:952`; `Binding-Profiles/CONTRACT-binding-profiles.md:401-409` |
| G-D2 | **Kind-4 mouse-axis gate** "while `GetForegroundWindow` (`001973DA`) and the singleton byte `+0xC35` allow" — which singleton and what sets `+0xC35`: not stated. | `…/keymap-ini…md:952` |
| G-D3 | **`InputConfig_*` callers** (`001E0F40`, `001E0F70`) and which screen action issues them: not stated. | `…/keymap-ini…md:722-729` |
| G-D4 | **Bytes `+0x140..+0x15B` of the runtime record** — "zeroed by the defaults path"; whether anything reads them is not stated (contract lists it as open). | `…/keymap-ini…md:685`; `Binding-Profiles/CONTRACT-binding-profiles.md:502` |
| G-D5 | **Hot-plug enumeration failure** "returns 9 and skips that frame's poll"; what the caller does with 9 is not stated. | `how-a-gamepad-becomes-a-controller-object.md:234` |

**E. Modal toggle (R2)**

| id | gap | where it shows |
|---|---|---|
| G-E1 | **`00862CF0`** gates the release-path set of the toggle (`FUN_00862CF0() != 1`) and is not described anywhere in 15-Input. | `Modal-Toggles/r2-force-fight-toggle.md:104` |
| G-E2 | **Mode register `022C83EC`** bits 0–3: their effect on the applier is read, but who else writes them and what each mode is: partly stated (bit 0 gates the battle-menu build, `0028E5F0` stores bit 1). | `Modal-Toggles/r2-force-fight-toggle.md:166-176`, `:314`, `:441` |

### 2.3 Contradictions between pages (a re-implementer would have to choose)

| id | contradiction | cites |
|---|---|---|
| G-C1x | **What `ValidateBindingIdRanges` `001965E0` checks.** Input stack: "returns 1 when no profile is fully in range". Keymap page: it checks **profile 1 only**, three times on the same base; profiles 2 and 3 "are range-checked by nothing". | `Input-Stack/…md:301`, `:400`; `…/keymap-ini…md:375`, `:648-662` |
| G-C2x | **`00196290` copies how many records.** Keymap key-address table: "copies 2 records `01F80130` → `01DF1738`". Binding prose: copies out of the profiles "for all three bases"; `00196680` "reinstalls the three published profiles". | `…/keymap-ini…md:383`; `Binding-Profiles/binding-profiles…md:1302`, `:1329-1331`, `:1339` |
| G-C3x | **Sign convention of a two-code axis entry.** Contract and DC-1: `codeA` = negative direction (−0x7F), `codeB` = positive (+0x80). AU-3 and the publisher pseudo-code: records are "positive code, then negative", and the publisher fills `codeA` from the `_P` slot. Both cannot be read as the on-screen direction without the axis convention, which is not stated. | `Binding-Profiles/CONTRACT-binding-profiles.md:96-97`, `:280-282`; `Binding-Profiles/binding-profiles…md:1076-1079`, `:1443`; `…/keymap-ini…md:952` |
| G-C4x | **`01DF1738` "staging buffer".** Input stack §11 still calls it staging / "the scratch area the defaults are assembled in"; binding prose and keymap say it is records 2–4 of the polled bank. The keymap page notes the stale §11. | `Input-Stack/…md:776-797`; `Binding-Profiles/binding-profiles…md:598-602`; `…/keymap-ini…md:1082-1085` |
| G-C5x | **Binding contract §14 / §17 list items as open that other pages answer**: `DC-2`, `DC-3`, `BP-3`, `BP-4`, `BP-5`, records 0 and 1 of bank A (UQ-143), group 2's consumer (`00197710` callers), the axis entry's `+0x04` (UQ-144 sub-kind), and the bank writers. A reader of the contract alone would think these are unknown. | `Binding-Profiles/CONTRACT-binding-profiles.md:489-503`, `:655-668`; answers at `Binding-Profiles/binding-profiles…md:361-366`, `:1025-1062`; `…/keymap-ini…md:254-286`, `:926-952` |
| G-C6x | **Name-registry contract §14 keeps `DM-1` and `DM-3` open**; the system page answers both (2026-09-22). The system page's own §7 still has an unstruck `DM-1` bullet. | `Input-Name-Registry/CONTRACT-input-name-registry.md:294-298`; `Input-Name-Registry/the-input-name-registry…md:156-160`, `:336-397`, `:398-399` |
| G-C7x | **Capability C-7 register row** still repeats "all but 1 / 5 / 10"; the page corrected it and routed the row to the register owner. | `Gameplay-Capability-Policy/…md:1065-1067` |
| G-C8x | **Status banners vs status lines.** Input-stack and R2 pages open with "PARTIAL" in the body while the front matter says DOCUMENTED. | `Input-Stack/…md:4`, `:32`; `Modal-Toggles/r2-force-fight-toggle.md:4`, `:32` |
| G-C9x | **Profile numbering.** The R2 page writes `GetBinding(mgr, /*profile*/ 0, …)`; the keymap page calls the same read "profile 1" (1-based, as in `[Keyboard1]`). Not a factual conflict, but a re-implementer must normalise it. | `Modal-Toggles/r2-force-fight-toggle.md:74`; `…/keymap-ini…md:272-273` |

---

## 3. Rating

**MOSTLY.**

What is ready. The bottom and the edges of the stack can be written from the database alone:
- the keymap file (path, grammar, parser quirks, writer, validators, shipped defaults);
- the authored and runtime binding layouts, assignment (result codes, global conflict scan, swap), the
  publisher (already differential-tested), and the translator's arithmetic for kinds 1–4;
- the channel record, the history frame, the transition, repeat and timing rules;
- the keyboard latch path and the band backends;
- the name registry (differential-tested and runtime-validated);
- the R2 toggle end to end;
- the capability primitives, the aggregate, the projection table and the row-2 reconciler.

Ordering, the snapshot and the six cross-operation invariants are stated with falsifiers.

Why it is not READY. These gaps are named, not structural, but two of them block whole functions:
1. **The arbiter `00253C70`** — the one body that joins the three operations — is specified only by its reads,
   writes and invariants, not by its decision logic (G-A3, G-A4, G-A5).
2. **The device poll bodies** — the three controller kinds' polls, `007A2440` and the analog filter
   `0079D1D0` — are not read (G-L6, G-C4). Only the keyboard path is complete.

Also open: the snapshot's field map past channel 0 (G-A1, G-A2), feedback request inputs (G-C1),
cross-thread synchronisation (G-A6), and nothing in the frame order has been observed live (G-L1, G-L4). The
contradictions in §2.3 are small, but G-C1x (which profiles are range-checked) and G-C3x (axis sign) change
observable behaviour and must be settled before anyone writes code.
