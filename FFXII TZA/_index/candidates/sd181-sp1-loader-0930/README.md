# SD-181 closed: `02ADD060` is slot 16 of the map's `.mpk`, stored by the pack's completion (OPUS, 2026-09-30)

Register row SD-181 asks which shipped file carries the emitter volume records that the base `022CBAF0` points into.
[clamping-a-point-into-a-volume.md](../../../06-Movement-And-Navigation/clamping-a-point-into-a-volume.md) cites it
from its call chain.

**Where it stood.** It was narrowed at `1dbac71de` (`sd180-181-emitter-walk-0930`). The base's one non-zero writer is
`003635C0`, fed from `[02ADD060]` by `003775D0`. SWE2-AUDIT-SEM's DD-owner-read-5 review (C3) and the row left one
question open: what fills `02ADD060`, and so which file.

This record is static, from the certified image. The checker is `sd181_check.py` (output `sd181_check.out`,
`FAILS 0`).

## The answer (OPUS)

**`02ADD060` holds slot 16 of the current map's map_ctrl pack.** The file is
`ps2data/plan_master/map_ctrl/<area>/<map>/bin/<map>.mpk`, and its slot 16 is the `SP1` sound-emitter section
([the map_ctrl pack page](../../../03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md), §2.3 and the slot table).

- **L1.** `00378030` submits the pack load with completion `00378BC0` (`003780B1`). That `lea` is the completion's only
  reference, and nothing calls it directly. This is the page's §3.1.
- **L2.** The completion splits the loaded block into 32 slot pointers on its stack: `0036B970(block & ~3,
  rsp + 0x20, 32)` (`00378BDD`–`00378BF3`). This is the page's §3.2 split through `0036B980`.
- **L3.** It then stores `[rsp + 0xA0]` into `02ADD060` (`00378E95` / `00378E9D`). `rsp + 0xA0` is
  `slots[(0xA0 − 0x20) / 8]` = **`slots[16]`**.
- **L4, a control on the same arithmetic.** The same function copies `slots[24..27]` (`rsp + 0xE0 + 8i`) to
  `02ADD010 + 8i` (`00378C40` / `00378C48`). The page's slot table maps the four map pictures (slots 24–27) to exactly
  that address.
- **L5, the rest of the chain.** Two functions write `02ADD060`: `00378BC0` (slot 16) and the teardown `00378230`,
  which frees and zeroes it. Its one reader outside the teardown is `003775D0`, which passes it to `003635C0`, the
  emitter base's writer (B1 of the earlier record).

So the emitter records the walk reads are the `SP1` section of the map's `.mpk`. That is the page's slot-table row 16
(`02ADD060 → 003635C0`), now traced instruction by instruction.

## Limits (OPUS)

- **Static.** The file identity (which `.mpk` the request names) rests on the map_ctrl page's §3.1 and its 550 / 550
  census, whose layout test is the loader's own. This record adds the slot-to-global store and its control, not a new
  file census.
