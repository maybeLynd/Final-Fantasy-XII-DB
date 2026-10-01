# S-41: the positive dispatch over a bank loaded from the shipped `se000.seb` (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**

**The gap.** S-41's runtime residual (AUDIT-SEM): *"the loaded-bank positive dispatch arm (EXP-105's fork ran under
stubs)"*. The earlier closers ran the sound request with **no bank loaded**.

## What was run

`check.py` runs the sound-request closer's world (`../s41-opus-replay-sound-request-stub-free/check.py`), executed first from
its own source. Its cases are unchanged, and its `result.json` (md5 `a94fad40…`) is not rewritten. Then it builds what a loaded
bank needs, **by the game's own code**:

- **The audio driver manager** `[01FD4138]` is built by its lazy initialiser `002216B0(0x400, 0x400)`, the constants its only
  caller `00210760` passes. That runs `operator new` and the constructor `0021E570`.
- **The audio file loader** `[01FD36A8]` is built by its lazy initialiser `002125A0` (`operator new(0x158)`, constructor
  `00211840`).
  - **Its worker thread is not run.** `CreateThread` and the thread-attribute calls are bridged by name and return handles,
    so the thread body never executes.
  - **That is the recorded boundary: the loader's file I/O.**
- **The shipped `ps2data/sound/se/block/se000.seb`** (sha256 `40d50fc1…`) is copied to memory. These are the bytes the kind-32
  load delivers.
  - The bytes are handed to `002DEF00(0, blob)`, the registration's own call (`003A1650` → `002DEF00(slot & 0x3F, blob)`).
  - That runs `001DBD20` → the Seb controller's load `0021B430` → the `SebAudioBank` initialiser `00223AD0`. The slot map is
    filled from the file and the `.sab` load is queued.
  - `strcpy_s` is bridged by name with library semantics; it copies the path into the request.

**No application stub.** Four functions reached through vtables or indirect calls are admitted to the allowed set: `00218920`,
`0021B150`, `00212810` (the controller's slots) and `0019C590` (`free`). `Sleep` is bridged by name and returns.

**4 / 4 pass; `result.json` is byte-identical over two runs (md5 `b2b4908b…`).**

| case | observed |
|---|---|
| `L1_seb_bank_loaded_from_the_shipped_file` | a `SebAudioBank` (vtable `00907D80`) is spliced into the controller's list. Its map root `+0x70` is set from the file's slots, `+0x3C` = 0 (block 0's bucket), and **`+0x30` = 1 (loading)**. The queued path is **`PS2Data/sound/se/sead_data_win/se000/se000.win.sab`** |
| `D1_receipt_before_walk_match_and_play` | `0021B5B0(controller, id 1, pan 0x40, vol 0x7F)` mints the receipt (`00212950` at `0021B5E2`) **before** the walk. It then matches the loaded bank on `id / 512 = 0` at `+0x3C` and calls the Seb play `00224540` with it. This is the contract's *"Seb calls RCAL 00212950 at 0021B5E2, before it walks the list"*, on a bank built from shipped data |
| `D2_play_waits_on_the_loading_fence_forever` | with `+0x30 == 1`, the play enters the spin fence (`0022459E` / `005CCB80`) and keeps yielding. That is **about 50,000 fence and `Sleep` rounds** before the instruction budget stops it. `+0x30` never changes, because only the unrun loader thread completes the load. This is the contract's *"the spin fence runs only when `elem+0x30 == 1`"*, executed |
| `D3_no_matching_bank_no_play_receipt_still_minted` | control: id `0x201` (bucket 1) matches no bank. There is no play call, and a receipt is still minted |

## Not covered

- **Anything past the fence**: the slot tree lookup, the reuse test, the volume clamp and the voice. Getting there needs the
  `.sab` I/O, and the voice is contract-declared live-only.
- The Sep dispatch over a loaded bank.
- A live game.
