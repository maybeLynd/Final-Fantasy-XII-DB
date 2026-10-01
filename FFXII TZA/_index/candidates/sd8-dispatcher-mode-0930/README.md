# SD-8: the dispatcher mode the title runs in, and whether the title polls the keyboard (OPUS, 2026-09-30)

Register row SD-8 was registered by SWE2-DATA (`f7a3292bd`, input-stack-device-channel-and-bindings.md §5). The keyboard
poll runs only in dispatcher modes 2, 3 and 5, and "the value the title state writes to `02064AD3` is not read". This
record is static, over the certified image. The checker is `sd8_dispatcher_mode.py` (output `sd8_dispatcher_mode.out`,
`FAILS 0`). It uses the shared lookup tool `Tools/analysis-kit/gfz-scripts/retool.py`.

## The answer (OPUS)

**The title does not choose a mode. `02064AD3` is the frame dispatcher's own state machine. After the two boot modes it
rests only in 2, 3 or 5, and the keyboard poll runs in all three. So once boot finishes, the title polls the keyboard.**

| mode | handler (table `0022A754`, F1) | next mode (F3) |
|---|---|---|
| 0 | `0022B6E0` | 1 (`0022B74E`), once `0032E520(1)` is idle and `[0209273C]` is 5 |
| 1 | `0022B7E0` | 2 (`0022B85B`), once `0032E520(1)` and `0037C2E0()` both return 0. Otherwise it stays in 1. |
| 2 | `0022A770` | the steady per-frame handler; left only on an outside request |
| 3 | `0022B8C0` | 2 (`0022BB81`) |
| 4 | `001E0580` then `0022AF50` | 3 (`0022AFF2`) |
| 5 | `0022BC20` | 2 (`0022BDC5`), once the mode is no longer 5 at `0022BDB2` |
| 6 | `001E0580` then `0022B000` | 5 (`0022B097`) |

- **Writers** (F2). Every store to `02064AD3` is one of the eight in the table above: the initialiser `0022A0B0` stores
  0 (`0022A1A0`), and there is the outside setter `00229F00`.
- **The outside setter** (F4). It is called only with 4 (`002E09A0`, at `002E0D39`), 6 or 2 (`002E2240`, at `002E2257` /
  `002E2274`). Each of those modes returns to 2 through 3 or 5.
- **The poll gate** (F5, `0022A600`–`0022A657`). Modes 4 and 6 clear the poll flag, and so do modes outside 2..5 and
  mode 4. So `0035E6F0` is called in modes 2, 3 and 5 only.

**For the player:** the keyboard is polled on the title screen as in play. It stops only for the one-frame hand-offs
(modes 4 and 6) and during the boot wait (modes 0 and 1). This agrees with the live observation the page cites
(`EXP-006` moved the cursor at the title). That observation is kept separate: this record is static.

## Limits (OPUS)

- **When the title appears.** That the title screen is first shown after mode 1 has exited is not proved from the
  image. It rests on mode 1 waiting for the loader queue (`0032E520`) and `0037C2E0`, and on EXP-006 observing input at
  the title. If the title were drawn during the boot wait, it would not poll until the wait ends.
- **Static only.** What `0032E520` and `0037C2E0` report on a given boot is not measured here.

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
