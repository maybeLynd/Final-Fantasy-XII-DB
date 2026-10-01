# S-33: the pickup create with presentation op 1 real (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**

**The gap.** S-33's runtime is MIXED on one named exposure. EXP-141 scripted presentation op 1 (`003FA160`), so the
`+0x58` handle CREATE stores was a stub's value. The real body faulted over the bound world: its sprite records were
not bound. The residual was *"op-1's real run and what the `+0x58` handle is — an asset-layer dependency, replay-reachable
if the resource binds"*.

## What was run

`check.py` runs over block 332's world (`../s21-opus-replay-applier-stub-free/check.py`, whose cases run first and whose
result is unchanged).

**Built by shipped code:**
- **The pickup visual sub-object `mgr+0x57E0`.** Block 332 plants the HUD manager `[0209BE80]` as a zero block. That is
  what the HUD constructor `00291750` leaves after its own memset (`00291765`). The sub-object is then initialised by
  `003FA760`, the call `00291750` makes at `002917C9`.
- **The HUD sprite registry `0208F580`.** The shipped registrar `00280750` registers its ten records. It runs as a prefix
  that stops at `0028083B`, before its file request `00249180`; the loader's I/O is not emulated.
- **The two records op 1 looks up, `partytop_8_c` and `partytop_4_c`** (records 6 and 5). They are bound by the shipped
  binder `0024A1D0` from the shipped bundle the request names: file `(7, 0xD7)`, which the path installer `002DF9A0`
  resolves to `PS2Data/image/FF12/myoshiok/in_sdver/PackFiles/tex2pack_ys.bin` (sha256 `df45f07c…`). The binder gets the
  offsets the completion `00280670` would pass (`[bundle + 4k]`). Each binder run is a prefix that stops at `0024A25E`,
  its first render-layer call (`00181520`, the texture manager on `[01F811E8]`). By then the record's sprite header
  (`+0x18`/`+0x20`) and format bits are stored.
- **The pool.** It is initialised by `00319B10`. Every create is the shipped CREATE `00319CA0` with item `0x0101` ×1 at
  (5, 6, 7). The dispatcher `0028F000` and op 1 run as shipped.

**No application stub.**

**Disclosed.** The GS `TEX0` word (record `+0x30`) is laid out later by `0024A710` through the GS command buffers, so it
is 0 here. op 1's UV floats are therefore computed for a 1×1 texture. They are presentation values, and no case reads them.

**8 / 8 pass; `result.json` is byte-identical over two runs (md5 `7932681c…`).**

| case | claim | observed |
|---|---|---|
| `R1` | the world is built by shipped code | `003FA760` leaves `+0x249A = 0xFFFF` on the zeroed sub-object. The ten names are registered in `00280750`'s order. Both partytop records get `+0x18` = bundle + offset and `+0x20` = `+0x18 + 0x10`. `+0x30` is 0 and no render call is entered |
| `R2` | op 1, real | `0028F000(0, 1, payload)` → `003FA160(mgr+0x57E0, payload, tier 2, 0)`. op 1 looks up `partytop_8_c`, then `partytop_4_c`, into its cache (`+0x2690`/`+0x2698`) and takes visual slot 0 (`sub+0x270`). It sets `+0x272 = 1`, phase `+0x260 = 1`, `+0x264 = −0.25`, `+0x268` = the tier, makes the slot the list head `+0x2490`, and requests sound `0x50` (`00249C60`). It returns the slot's address, and **CREATE stores its low 32 bits at node `+0x58`** (`00319E05 mov [rbx+0x58], eax`). **The handle is a truncated pointer to the pickup's visual slot** |
| `R3` | later creates | slots 1 and 2 follow in order, linked at the tail (`+0x278`/`+0x280`), with no further record lookups |
| `R4` | the handle resolves | the shipped TICK `00319600` looks each state-1 node up through `0028EFE0` → `003FA730`. Every lookup finds its slot on the list and returns phase 1, and no node changes state |
| `R5` | retirement keeps the slot | an eviction retires the head's visual through `003FA820(handle, 0)`. That sets flag bit 1 and **keeps bit 0: the slot stays occupied**. With ten nodes and thirteen slots, the 14th create (the fourth eviction) finds every slot occupied: op 1 returns 0 and CREATE stores **handle 0**. This is EXP-141's scripted `c-op1ret0`, here reached by shipped code |
| `R6` | **bounded finding** | TICK then looks up handle 0, and `003FA730`'s first instruction `test byte [rdx+0x272], 1` (no null test) faults at address `0x272` |
| `R7` | how long a retired visual holds its slot | the per-frame visual update `003FA790` (called by the HUD update `0028E290`) frees the five retired slots together on its **51st** call, and no live slot. A probe that retired a visual after three updates saw 48 |
| `S1` | static | the 32-bit store `00319E05`; the unguarded lookup `003FA730`; the manager's allocation chain (below) |

## What this settles

- **op 1 runs for real, and its return is the `+0x58` handle.** The handle is the address of the pickup's visual slot
  inside the HUD manager's pickup sub-object, truncated to 32 bits by `00319E05`.
- **Where the manager comes from (UQ-137's static half).** `0028F8B0` allocates the manager through `00271420(0x10FD0)`.
  That call selects arena 3 (`0036C1D0` with `ecx = 0xF − 0xC`). Boot backs arena 3 with `0036D240(0xD20100)`, a CRT
  `malloc` (`0022A1E6`, registered `0022A2C0`–`0022A2CB`). So the requirement that the handle survive truncation is a
  requirement on where the CRT puts that 13 MiB boot block. That part is live, and it stays open.
- **A zero handle is reachable by shipped code, and it faults the tick's lookup.** op 1 returns 0 when all thirteen visual
  slots are occupied. Retired visuals keep their slots for about fifty visual updates (R7). So four new drops within that
  window, while ten pickups lie on the field, store handle 0, and the next pool tick dereferences `+0x272` of a null
  object. **Whether that happens in play is live.** It depends on drop timing and on the visual update's cadence, and the
  question is routed to ASTRA. Nothing here claims an observed crash.

## Not covered

- The texture half of the records: `0024A1D0` past `0024A25E`, and `0024A710`'s `TEX0` layout. Both are render layer, the
  boundary ruled for S-37.
- The loader's I/O, and a live capture.
