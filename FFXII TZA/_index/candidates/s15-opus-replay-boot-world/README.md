# S-15: exit A and the interpreter arm, executed over shipped field scripts in a world the game's own start-up built (OPUS, 2026-09-26)

**Evidence classes: NATIVE-REPLAY (unicorn) and STATIC. `live_game: false`.**

**The gap.** S-15's runtime cell was MIXED. It named two arms never executed: **exit A** (`002620E0` called from
`0025DB7D`) and **the interpreter arm** (`0025E4C0`). Both need an actor bound from a real field script. The earlier
harnesses built their records from S-13's pool, which carries no script. This package executes both arms:
- over two **shipped** field scripts, `ttl_b01.ebp` and `byu_w01.ebp`;
- bound by the **real loader** (`00330310` → `003304A0` → `ActorManager_BindLoadedDefinition`);
- in a world the game's **own start-up code** built, not block 332's zero-planted singletons.

## How the world is built

`world_boot.py` uses block 332's emulator, with the whole image allowed and imports as the only boundary. It installs
disclosed process-start models (listed below), then runs the CRT's 3 pre-C and 1,172 C++ initialisers as shipped
(0 failures). `check.py` then runs the start-up in shipped order.

| step | what runs | where it stops |
|---|---|---|
| main `007980A0` | a prefix | in `GameSettingConfig_SerializeText`, at msvcp140's narrow `basic_ostream` constructor (not modelled), after the settings object `[01F82D20]` exists |
| app slot 2 `0017CEB0` | builds the job system and indexes `../FFXII_TZA.vbf` (`fread`, MD5 through CryptoAPI) | **`00624364`**: `001DD420`'s display-mode enumeration reads the DXGI adapter `[renderer+0x1880]`, which only device creation `006253D0` stores (`006256F2`, `00625749`) |
| the rest of `0017D6B0`, then `0017D4C0`'s 38 callees one by one | as shipped | two in the **render layer**: `001B7850` (render targets; loads `/GameData/D3D11/ArtData/shaders/video.fx.phyre`) and `001B1580` (an 8×8 texture filled through a map/lock). All others return |
| `002EF650` | the save-image reset, the call `0022B6E0` makes at `0022B78B` | returns; the battle block `[02EBF190]` is bound |
| message 16 to the UI system widget (handler `00253780`, created by the UI boot `00253970`) | its pack branch `00280980` fills the HUD context's MRP pointers from the mrppack blob | later in the branch, at `GetKeyboardLayout` (not needed) |
| two binds | `00330310`'s prefix to `003303E3`, the file's shipped bytes into its buffer (the I/O thread's work), then the real completion `003304A0` | both return |
| the field pass `0025D9E0` | once per frame for 4 frames per slot, the loader pump drained between | — |

**Other threads.** Where the main thread waits on another thread, that thread's shipped code runs as a *prefix* on a
side stack:
- **The input worker** `0035EA40` runs up to its ready-flag store `0035EA64`.
- **The job manager's worker loop** `001A1240` runs exactly one job, up to `001A12E9`. Its thread entry is `001A1230`,
  started by `001A0AF0`. It runs whenever the loader's status test `0046DFE0` finds a read in flight with a job queued.
  Boot's loads (`map_ref.bin`, `test_area_ref.bin`, `pc_skillmotion.bin` and others) are served this way from the real
  archive.

Nothing is planted in their place.

**The game's own stream buffer.** msvcp140's narrow stream members are modelled in `narrow_streams.py`. Where the
library would call the buffer's virtuals, the model runs the **game's** `basic_stringbuf` code instead (overflow
`001DFA80`, underflow `001E0390`, pbackfail `001DFCF0`), as guest calls on a side stack.

**Disclosed models.**
- **s36 `os_model`:** a fresh install.
- **`msvcp_wide`.**
- **`crt_bridge_boot`:** S-40's CRT bridge plus a full C `sscanf`.
- **`narrow_streams`.**
- **`file_bridge`:** read-only `fopen` / `fread` / `fseek` over the install folder.
- **`boot_model`:**
  - process start, with threads recorded but not run;
  - Steam fails;
  - a 1920×1080 display, en-US;
  - a fixed clock at 2025-09-26 00:00 UTC.
- **`mem_files`:** GameSetting.ini is created in memory only.
- **`sync_model`:** single-thread; a wait that needs another thread stops the run.
- **`boot_misc`:**
  - CryptoAPI MD5 with standard semantics;
  - sticky keys; a 16 GiB machine; timer caps;
  - `strcspn`, `toupper`;
  - `CoCreateInstance` of the audio endpoint (MMDeviceEnumerator) **fails**: the audio device is outside the world;
  - `GetCurrentThread`.

Each module's docstring states exactly what it answers.

## Cases

**6 / 6 pass; `result.json` is byte-identical over two runs (md5 `81f9a37e8f3c7f8968a07acc4d55981a`).**

| case | observed |
|---|---|
| `B1` | the start-up runs as shipped: CRT 3 + 1,172, 0 failures. Main stops in `SerializeText`'s ostream. Slot 2 stops at `00624364` on the DXGI adapter. The render-layer steps stop at `001B6C75` and at the memset in `001B1630`. Every other step returns. `006256F2` / `00625749` are the adapter's only stores (byte-checked) |
| `B2` | both binds complete. `ttl_b01.ebp` (namespace 5, index 39) goes into slot 1 and `byu_w01.ebp` (index 2736) into slot 2; the paths are read from the game's own path table `[0215F000]`. **Slot 1 `+0x12 = 0` and slot 2 `+0x12 = 1`.** The bind stores `(word [definition + 0x50] >= 0)` at `0026CD28` (`0026CD1A` / `0026CD25` byte-checked). The definition is the buffer + `0x80`; `ttl_b01`'s word is −1 and `byu_w01`'s is 0 |
| **`X1`** | **the interpreter arm, on a shipped script.** Slot 1, frame 0, takes the `+0x12 == 0` branch: audio, then the init core (return `0025DC2C`). The resolver `0025DF00` drives the record `ttl_b01` bound. Its wait entry (state 1) sends it into **`WorldActorScriptVM_InterpretBytecode` `0025E4C0`** (return `0025E0D8`), which runs the script's entries and native commands (`002621D0`) |
| **`X2`** | **exit A, on a shipped script's driven actor.** Slot 2 (`+0x12 = 1`) enters the drive loop.<br>• **Frame 0:** the driven actor (record 0) is driven through the interpreter and does not settle.<br>• **Frame 1:** its entries run out (`003DB6E0`, called twice from the interpreter) and `+0x14` bit 6 is set (`0x30` → `0x70`). The pass takes **exit A**: it stores `+0x12` and calls the init core from **`0025DB7D`** (return `0025DB82`).<br>• `+0x12` is 1 after frame 0 and 0 after frame 1: exit A clears it (`r12b` = 0).<br>• **Frame 2 onward:** the `+0x12 == 0` branch drives every record through the interpreter |
| `X3` | **the script drives the deferred arm.** In slot 1, frame 3, the interpreter's native lifecycle command (`002621D0` → `00353080`) calls `WorldSimulation_ProcessDeferredModeRequest` `0032FC30(1, 0x1AD)`. With the loader pool built, the request runs through `ActorResource_BeginManagerResource` `0032FCA0` and stops at `0020A800`'s **`std::regex` construction** (msvcp140 `locale::_Init`, not modelled) |
| `W` | every other-thread prefix and every guest call returns; the HUD context's `+0x08` is filled |

## Where the shipped start-up meets the device (static, byte-checked where marked)

- **`0079F150` (the app start-up) creates the device first.** It calls `006253D0` / `0079E4A0` before anything else of
  the game's.
  - `006253D0` runs `CreateDXGIFactory` and `D3D11CreateDevice` (feature level ≥ 11_0), then `00625830` →
    `D3D11CreateDeviceAndSwapChain`.
  - Any failure returns 9 through `0079F4D2` → `0079F517` → `0079F710`, before slot 2 (`0079F591`) and before the
    registrar, slot 3 (`0079F69A`). The registrar `0017CF30` is the only way the game-init job `0017D000` →
    `0017D4C0` is submitted.
- **The per-frame game update is slot `+0x20` = `0017CCD0`.** Its only reference is the vtable entry `008C5780`.
  - It is the field pass's only route in: `0025D9E0` ← `00314020` ← {`0022A770`, `0022B8C0`, `0022BC20`} ←
    `0022A580` ← `0022A490` ← `0017D6E0` ← `0017CCD0`. This is an image-wide reference census (rel32, pointer and
    rip-relative).
  - It is called at `0079C2D6`, after the first-frame gate `0079C1F1` (slot `+0x48` → `007A05D0`). S-36 showed that
    gate returns `0x15` at the renderer's back-buffer resize.
  - It does nothing until the init job sets `+0x113C`. The only store to that offset is `0017D074`, in `0017D000`.
- **In this world**, the steps after the device are run individually, in shipped order. The two render-layer steps
  stop where the table says.

## Corrections this package makes

- **Contract §3 and §6, `+0x12`.** The byte is raised by the bind from the definition's driven-actor ordinal, and
  cleared by exit A. It was not "written only on the settled exit", and exit A does not "publish the running
  conjunction". Consumer check: [`../s15-field-pass-plus12-consumer-check.md`](../s15-field-pass-plus12-consumer-check.md).
- **`s15-opus-replay-field-pass-stub-free` F3.** Its stop was the loader's free-slot wait `0032E870` spinning on an
  **empty** request free list, because that world never built the pool. It was not a "resource pipeline boundary". The
  README there is corrected in place.

## Not covered

- **The deferred arm past `0020A800`:** a `std::regex` construction in msvcp140; not modelled.
- **Slot 0's drive:** it additionally needs the map-ready word `[02ADD0D8]`, which only a field map load sets (the
  world transition, `003775D0`).
- **A live game.**

**Run:** `python check.py`, about 15 minutes. It needs:
- `pefile`, `capstone`, `unicorn`;
- the shipping EXE and `FFXII_TZA.vbf` at the install path in block 332's `world.py`;
- the extracted `ps2data` tree at `D:\FFXII_TZA_extract`;
- the sibling packages `s21-opus-replay-applier-stub-free` and `s36-opus-replay-arbiter-input-gate`.
