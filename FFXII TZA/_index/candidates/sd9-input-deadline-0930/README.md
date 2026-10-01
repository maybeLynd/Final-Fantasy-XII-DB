# SD-9: the deadline arithmetic in `0035E7A0` paces nothing in the shipping build (OPUS, 2026-09-30)

Register row SD-9 was registered by SWE2-DATA (`f7a3292bd`, input-stack-device-channel-and-bindings.md §5, AP-7). It
asks how the constants `0x13A` / `0x108` in `0035E7A0` become the input worker's deadline. This record is static,
over the certified image. The checker is `sd9_input_deadline.py` (output `sd9_input_deadline.out`, `FAILS 0`). It uses
`Tools/analysis-kit/gfz-scripts/retool.py`.

## The arithmetic (OPUS, F1-F2)

With `acc = [022CA5C4] += [022CA5D0]` and a period `P`, `0035E7A0` returns:

| condition | result |
|---|---|
| `acc < P` and dispatcher mode (`00229EA0` = `[02064AD3]`) is 3 | `P − acc` |
| `acc < P`, any other mode | `2P − acc` |
| `acc ≥ P` | `⌈acc / P⌉ · P − acc`: the distance to the next multiple of `P` (`0035E7F0`–`0035E7FE`, an `idiv` round-up) |

`P` is `0x13A` (314) unless `00290180()` returns 2, in which case it is `0x108` (264).

## What the shipping build does with it (OPUS, F1, F3-F6)

1. **`P` is always 264.** `00290180` is `mov eax, 2; ret`, so the `0x13A` branch is never taken.
2. **`acc` is always 0.** The step `[022CA5D0]` is zero-initialised and nothing writes it: its only two references are
   the reads at `0035E7B0` and `0035EBF3`. The accumulator starts at 0, adds that zero step, and the worker `0035EB70`
   clears it on every pass (`0035EC65`, `r8d` = 0).
3. **So the result is the constant 528**, or 264 when the dispatcher is in mode 3.
4. **Nothing reads the result.** It is stored at `[022CA5DC]` (`0035EC11`, after the call at `0035EC05`) and `acc` at
   `[022CA5D8]`. Both have stores only (`0035E820` initialises them), and no base-pointer route reaches them:
   - no stored pointer names `022CA5C0`–`022CA5E0`;
   - the objects addressed just below end before `022CA5C4` (`022CA520` is cleared as `0x98` bytes at `0035D361`).

**Answer:** the two constants choose a period, but in this build the choice is fixed, the accumulated time never moves,
and the resulting "deadline" is stored and never used. The input worker is not paced by this arithmetic.

**An inference, kept separate and not claimed:** 264 and 314 match the NTSC and PAL field line counts (262.5 / 312.5).
This is consistent with a PS2-era video-timing routine left in the port with its timebase disconnected. The code does
not say so.

## Limits (OPUS)

- **Static only.** A read of `022CA5DC` through a pointer computed with no `lea` / `rip` reference into the block would
  not be seen.
- **Pacing.** What does pace the input worker is not answered here. AP-7 on the page names what it schedules.

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
