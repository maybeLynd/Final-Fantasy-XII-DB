# SD-6: the recorded-input table `[02EA5488]` is never filled in the shipping game (OPUS, 2026-09-30)

Register row SD-6 was registered by SWE2-DATA (`f7a3292bd`, input-stack-device-channel-and-bindings.md §5). It asks
whether the table of `0x98`-byte recorded input events at `[02EA5488]` (count `[02EA5480]`) is ever filled in retail.
This record is static, over the certified image, with no execution and no live run. The checker is
`sd6_input_source.py` (output `sd6_input_source.out`, `FAILS 0`). It re-derives every fact below and asserts it.

## The answer (OPUS)

**No. The table is filled only by the Phyre test harness's `InputSource` command, which the shipping game can never
run.** The run loop `00796490` replays the table each frame, but the count is always 0, so nothing is replayed.

The chain:
1. **The table's writers** (F1, F1b).
   - The run loop `00796490` only reads the table, replaying `count` records through `0079A120`. Its four stores all
     write zero after freeing it (`007965C4`/`007965CB`, `007965FD`/`00796604`).
   - The teardown `008B7B90` also frees it and stores zero (`008B7BBD`–`008B7BC6`).
   - The only filler is `0079FB10`, which passes the table's address to `007A0540` (`0079FC78`).
   - *Correction to the page:* "written only by `00796490`" is not right. `00796490` only clears it, and the filler is
     `0079FB10`.
2. **`0079FB10` is an input-log file loader** (F2). It logs `"Error opening : %s"` when the file does not open, skips
   `#` lines, parses `INPUT:` lines and grows the table.
3. **Its only caller is the handler of the harness command `InputSource`** (F3). `00797A20` cuts its argument at the
   first comma and loads that file. `007A0180` registers it under the name `InputSource`, alongside the harness's
   other commands: `Frames`, `Timestep`, `Framerate`, `Keypress`, `Buttonpress`, `Mousepress`, `Expect`, `Echo` and
   `Quit`.
4. **Command players are built in one function, behind two gates** (F4, F5, F6).
   - The registrar `007A0180` is called only by `00792760` and `0079F150`, and `00792760`'s one caller is `0079F150`.
   - `0079F150` builds a player only when `[02EA5220]` (a script path, logged as `"Trying to run %s"`) or
     `[02EA5230]` is non-null. `[02EA5230]` is an input-source file name, for which it writes the script
     `"InputSource(%s)\nFrames(%06i)\n"`.
5. **Neither gate can open** (F7, F8).
   - Both globals are zero-initialised: they lie beyond `.data`'s raw bytes.
   - Each has exactly one reference in the image, the read at the gate.
   - No stored pointer names either one.
   - No code writes, or takes an address, anywhere in `02EA4100`–`02EA522F`, apart from the window procedure's byte
     `02EA5213`. That byte is control C1, and it shows the reference scan sees writes in this block.

**For the player and for modding:** the engine carries Phyre's input record/replay harness, but the shipping build has
no way to turn it on. The file name it would need is never set. Enabling it would take a write to `02EA5230` (or
`02EA5220`) before `0079F150` runs; the harness would then read an `INPUT:` log and play it back.

## Limits (OPUS)

- **Static only.** An outside process or an injected module writing `02EA5230` is outside the image, and outside this
  answer.
- **The scan's coverage:** the reference scan covers the v4 extents plus the UC-1 frontier bodies, as in
  `Tools/analysis-kit/gfz-scripts/retool.py`. A store through a register holding an address computed without any
  `lea`/`rip` reference into `02EA4100`–`02EA5238` would not be seen. None is known.

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
