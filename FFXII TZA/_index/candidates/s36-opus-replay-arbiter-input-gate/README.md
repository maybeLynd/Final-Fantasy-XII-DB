# S-36: R-4's arbiter half, where its input comes from and where it stops (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), with disclosed OS, pad and descriptor models. `live_game: false`.**

**The gap.** S-36's runtime is MIXED. One residual is *"R-4's arbiter half (`00253C70`→`00253FE3` runtime consumption —
census-verified only, needs input state not planted)"*. The arbiter tests the latch `02092734` at `00253FE3` only on a frame
whose snapshot words carry a qualifying button (`00253FB3 test r14b, 0xA0`). So the question is whether shipped code can
produce such input in replay without planting it.

## What was run

`check.py` runs over block 332's world (`../s21-opus-replay-applier-stub-free/check.py`, whose cases run first and whose
result is unchanged). The input stack is built by shipped code, from the bottom up.

| layer | built by |
|---|---|
| CRT stdio options | the pre-C initialiser `00808D4C`, an entry of the table at `008C5690`. Block 332 runs only `00809124` of it. It sets the legacy wide-specifier bit the wide printf path needs |
| application object `01F7E350`, input backend `[02EA5368]`, device table `+0xDF8` | its C++ static initialiser `0015BC40`, an entry of the initialiser table at `008C31F0` (block 332's zero block is reset to the image value 0 first) |
| mode object `[01F81268]` | ensure-singleton `001C1940` |
| input manager `[01F7FFE0]` | ensure-singleton `00198750`: keymap path built, `keymap.ini` absent, default bindings (zero block reset to 0 first) |
| channel layer | `003692D0` (boot `0022A3AD`) |
| an XInput controller | built as the per-device body `00797690` builds one: `00584740(0x470)`, then `00792CB0(obj, descriptor, [02EA9500])`. Its base constructor puts it on the device list `01F401E8` |

**Models (disclosed):**
- **`os_model.py`**: a fresh install. The user's Documents folder, no configuration file, the platform answers, a Steam
  context with no interfaces, and no key down.
- **`msvcp_wide.py`**: msvcp140's wide stream members, fail-closed. `getline`/`seekg`/`tellg` refuse, because they run only
  on an open file.
- **The DirectInput descriptor** is a model (`0x244` bytes, type `0x15` gamepad); DirectInput enumeration is not run.
- **The pad**: `XInputGetState(0)` answers `ERROR_SUCCESS` with `wButtons = 0x0010` (START held); the other users are not
  connected.

**Each frame, in order:**
1. the backend's device update `007A3110` (a vtable method at `01CB2468`/`01CB2480`);
2. the application frame `0079C140`;
3. the input frame `0035EC90`.

After the frames come the gameplay snapshot `002498B0` and then the arbiter.

**6 / 6 pass; `result.json` is byte-identical over two runs (md5 `8a85be46…`).**

| case | observed |
|---|---|
| `W1` | every builder returns. `[02EA5368]` = `01F7E350` with `+0xDF8` = `+0xE00`; the controller's vtable is `01CB2678` |
| `I1` | every frame runs with no stop. The backend puts the controller in device-table slot 0 (`0079AF20`). The input frame polls it (`InputManager` → `InputSystem_UpdateRegisteredDevices` → `007A2140` → `XInputGetState(0)`), and START is decoded into the controller's byte `+0x445` (`007A2371`) |
| `G1` **the gate** | every application frame calls its first-frame initialiser (vtable `+0x48`, at `0079C1F1`: the game's override `0017D0C0`, which stores the window size at `00189120()+0xAD8`/`+0xADC` and tail-jumps to the framework's `007A05D0`; *wording corrected 2026-09-26 (OPUS), was "`+0x48` = `007A05D0`"*). That returns `0x15` from **`006278B0`, the renderer's back-buffer resize**. So `0079C140` leaves at `0079C1F6`: its frame counter `+0x64` stays 0, and its per-code device update `0079D010` is never entered. The controller's per-code state (`+0x30…`, what the binding query `0079E650` reads) stays 0 |
| `G2` | downstream everything stays 0. The control state's pressure bytes are 0; channel 0's history marks all 16 buttons present (`0xFFFF`) with pressure 0; the snapshot leaves the arbiter's words `02F97368`/`02F9736A` at 0 |
| `G3` | run with the latch 0 and then 1, the arbiter returns 0 both times, and neither the button test `00253FB3` nor the latch test `00253FE3` executes. In this world it leaves even earlier, at `00253D19`, because `00265680` ("every manager slot ready") is 0 without a loaded field. Disclosed; the input words would stop it at `00253FB3` regardless |
| `S1` static | see below |

**S1 (byte-verified).**
- **The only live per-code writer sits behind the gate.** `0079D010`'s only caller is `0079C140` (`0079C260`), after the
  first-frame gate `0079C1E2`–`0079C1F6`.
- **The per-code writers in the input backend (`00790000`–`007A4000`)** are:
  - `0079D010`;
  - the clears `0079AE40` and `0079AE90`;
  - the bank copy `007A0B50`, from `+0x130`, which only `0079D010`'s first loop fills;
  - `0079A120`, reached from `00796490`, the input script's `Frames` command;
  - `00797EE0`/`00797F20`/`00797F60`, the input script's `KeyDown`/`KeyUp`/`Keypress`.
- **The input-script facility is dead in this build.** `007A0180` registers those commands only on the runner that
  `0079F150` creates when `[02EA5220]` is non-null. `[02EA5220]` has exactly one reference image-wide: its read at
  `0079F1D0`. Nothing writes it.
- **The snapshot band `02F97360`–`02F97398` has one producer, `002498B0`.** Every instruction image-wide that stores to it
  (rip-relative) or takes its address:
  - is inside `002498B0`;
  - or zeroes it: `002284F0`'s eight-store wipe; `002A329B`, `r12 = 0`; and the arbiter's own `di = 0` clears;
  - or only reads bytes: `00249860`/`00249880`.

## What this settles, and what it does not

**R-4's arbiter half is device-gated.**
- The input the arbiter tests comes only from the application frame's per-code update. It then passes through shipped
  layers executed here: device poll and decode, backend table, binding translation, channel history and snapshot. That update runs only after the application's first-frame initialiser succeeds, and in this world
  the initialiser stops at the renderer's back-buffer resize.
- The one alternative writer family, the input-script commands, can never be created in this build.
- So without a device there is no unplanted input that reaches `00253FE3`. This is the same class of boundary AUDIT-SEM
  ruled on for S-37's `002A9F00` re-entry (`AUDITSEM-REQ-OPUS-409`).

**R-4's two static halves are unchanged.** The latch's three readers and three writers are the S-36 census (`r45.py`, C4);
the router half is executed (L4, D0–DM).

**Not covered:**
- the arbiter's latch test itself (`00253FE3`) with real input, which needs the renderer;
- the manager-slot readiness gate `00265680`, which needs a loaded field;
- a live capture.
