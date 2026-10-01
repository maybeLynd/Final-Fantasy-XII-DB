# S-18: the ten facing-and-steering entries executed as shipped code over their whole closure (OPUS, 2026-09-25, block 308)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
- The contract is `06-Movement-And-Navigation/CONTRACT-facing-and-steering.md`. Its §13 covers only the angle wrap
  (`diff_angle_wrap.py`); the other entries have not been executed.
- This is a narrow OPUS harness, not an ORACLE EXP.

## What was run

`check.py`:
- **Image.** It maps the whole SHA-asserted image. **No application stub.**
- **Allowed set.** The union of the ten entries' static closures over `edges.tsv`: **68 functions**, all running as
  shipped code. Entering anything else fails a case.
- **Three import bridges**, through their real IAT slots: `atan2f` (`008C2BD0`), `cosf` (`008C2BA8`) and `sinf`
  (`008C2BB0`). Only the pop and mode-0 paths reach them.
- **Two stop boundaries** (not stubs; the run ends there and the arguments are recorded): `004288B0` and `003B3CA0`,
  the calls inside `003EC260`'s commit block.
- **Fixtures** are planted data only: the actor, the movement context with both `SteeringRecord`s, the secondary
  context, the render-record base `[022C6F28]` with one record, and `[01DFE0B4]`.
- **Method.** Each case snapshots the world, runs, and compares the **changed addresses and values** with the
  contract's claims.

**9 / 9 pass, and `result.json` is byte-identical over three runs.**

| case | n | contract claim | observed |
|---|---|---|---|
| `select_slot_00269F90` | 256 selector values | §4 "0 or 1 and nothing else", fail-open | 0 / 1 set the cursor to `+0x120` / `+0x1A0`; **2–255 leave it standing**; nothing else is written |
| `facing_kind_dispatch` | 8 kinds × 3 headings × 4 entries | §6 / §10 kind dispatch | kind 1 → exactly `ctx+0x38` and `+0x48`. Kind 3 → exactly the cursor record's `+0x34` (`0026C090`). **Every other kind writes nothing** |
| `rewrap_idempotent` | 4,103 headings in [−8, 8] plus crossings | §4 "wraps again … idempotent, so harmless" | **holds**: the stored kind-1 heading is `wrap³(h)`, equal to `wrap(h)` on all 4,103. The fmod wrap is not the identity (`wrap(1.0) = 1.0000002`, §10 DY-1), ~~but it is idempotent on its own output~~ **and it is NOT idempotent at the exact antipodes (qualified 2026-09-28, see below)** |
| `kind3_steering_record_write` | 4 | §6 the kind-3 arm (`002E5FB0` → `002E5E10`) | `+0xA8` and the `+0x50` / `+0x60` / `+0x70` sub-records' `+8` receive `wrap³`. `actor+0x0D` bit 5 skips `+0x60` / `+0x70`. A body adds `body+0xF8` plus `003DAF20`'s `+0x40` / `+0x48` / `+0x4C`. `dword [ctx2] == −1` skips `003EC260` |
| `ED2_commit_block_003EC260` | 10 | §2 ED-2, stage vs. stage-and-commit | see below |
| `set_steering_mode_0026AE90` | 8 kinds × 7 modes × 3 enables | §7 / §10 | kind gate. Modes 2–4 collapse to 1 when `+0x2C == 0.0`, **`−0.0` included**. The mode byte is record **`+0x29`**. Mode 0 clears `actor+0x0D` bit 4, runs `002E55C0` and zeroes `+0x7C` |
| `set_movement_mode_0026C120` | 31 | §7 table, §12 | kind gate; `+0x28` = mode. Modes 2 / 3 write `π/20` and `π` exactly, with the direction bit `0x40` per the sign of the **loop-normalised** difference (target 3.0 vs heading −3.0 reads negative: the short way round). Mode 0 with the teardown gate runs `002EBE50` + `002E8EE0` + `002E6300`; without it, only `002E6300` |
| `push_pop_002EAB80_002EAAA0` | 18 | §6 / §10 | refusals (`+0x18 == 1`, kind ≠ 3, wrong depth) write nothing, and a second push changes nothing. Push clones slot 0 → 1 and leaves slot 0 intact. Pop replays shape 0 via `002EC2C0` and shape 1 via `002EBFA0`; **shapes 2–7 replay nothing**; `002EC3F0` + `002E8EE0` always run |
| `normalise_loop_003A1C50` | 5 | §2 closed at both ends | `−π` and `+π` are returned unchanged |

### ED-2: what `003EC260` actually does

The contract says flag 0 "stages the new triple into `+0x120`–`+0x128` and returns", and flag 1 "additionally shifts
the triple into `+0x250`–`+0x258` and calls `004288B0(slot, −1)` (slot bit `0x20000` clear) or `003B3CA0`".
Measured (record = `[022C6F28] + id × 0x740`):

| case | `+0x120` | `+0x250` | boundary |
|---|---|---|---|
| flag 0, triple changed | new | **the OLD triple** (flag 0 writes `+0x250` too) | none |
| flag 1, triple changed | new | new | `004288B0(rec, −1)` |
| flag 1, bit `0x20000` set, `[+0x288]` = 7 | new | new | `003B3CA0(7, 0x1E)` |
| flag 1, bit set, `[+0x288]` = −1 | new | new | none; the run completes |
| flag 0, same triple | unchanged | unchanged | none; **nothing written** |
| flag 1, same triple | unchanged | new | `004288B0` |
| `word [rec+6] != −1` (either flag) | **reset to `{0, 0, 0}`, `+0x12C` = 1.0** | unchanged | none; **the flag is ignored** |
| … and `+0x284` bit `0x8000000` | unchanged | unchanged | none |
| `+0x284 == 0` | unchanged | unchanged | none (**`cmove` treats the record as absent**) |

- **`004288B0` is followed, not replaced, by `003B3CA0`.** The run stops at the first boundary. Statically, after
  `004288B0` returns, the body reaches the `[+0x288]` test at `003EC3A3`. So the contract's "or" is "and then".

## What the execution adds to the contract

1. **ED-2's arms are wider than stated** (table above): flag 0 writes `+0x250` when the triple changes; a reset arm
   ignores the flag; `+0x284 == 0` means "no record"; `004288B0` and `003B3CA0` are sequential.
2. **Mode 4's completion compare is unsigned** (`ja` on a sign-extended countdown). `(int16)countdown = −1` never
   completes at either FrameLimit. Measured: limit 1 completes for countdowns 0 and 1; limit 2 for 0, 1 and 2.
3. **The kind-3 arm of `0026B6A0` writes nothing when `[actor+0xC0]` is null** (`002E5E5F`). §6 lists the kind-3
   write unconditionally.
4. **A push / pop round trip is not byte-identical on slot 0.** Pop's always-run tail changes slot 0 `+0x6A`.
   §6's "slot 0 was never overwritten — it IS the saved pre-push state" holds for the push, not for the whole cycle.
5. **§4's idempotence holds** as measured, which answers the doubt DY-1's non-identity could raise.

## Not covered

- the callees beyond the two boundaries (`004288B0`, `003B3CA0`);
- the callers (`003DBDC0` / `003DB2A0` interruption routes);
- a live game.

## The rewrap row, qualified (OPUS, 2026-09-28)

ASTRA's `facing-wrap-antipode` (`ASTRA-RETURN-OPUS-FACING-WRAP-ANTIPODE`) was re-run and reports
PASS_SOURCE_COUNTEREXAMPLE. At the exact antipodes the wrap `0026C090` is a **two-cycle**: `+pi -> -pi -> +pi` and
`-pi -> +pi -> -pi`. It is not idempotent on its own output.

**What this replay measured still stands, for a different reason.**
- The stored kind-1 heading is `wrap^3(h)`, and the sweep includes `PI` and `NPI`.
- Three is odd, so on a two-cycle `wrap^3 = wrap`. The "equal to a single wrap on all 4,103" result holds because of
  the wrap count, not because of idempotence.
- A path with an **even** number of wraps differs at the antipodes. The kind-3 target this replay models as
  `wrap(wrap(h))` stores `+pi` for `h = +pi`, where a single wrap gives `-pi`.
- Both values are the same geometric direction. No visible or downstream consequence is claimed.

**Consumer routing.** The facing contract's "idempotent, so harmless" (§4 and the closing line) and the ED-3 answer
belong to their owner and are routed to FABLE (`OPUS-REQ-FABLE-FACING-WRAP-ANTIPODE`) with this per-path count.
