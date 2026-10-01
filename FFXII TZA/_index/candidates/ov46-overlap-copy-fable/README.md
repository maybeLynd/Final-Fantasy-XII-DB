# OV-46 (and OV-43's copy half): the deployed CRT's memcpy is overlap-safe (FABLE, Claude Opus 5.5, 2026-09-29)

**The question.** OV-46 (box on `02-Resource-And-Asset-Pipeline/the-source-block-mover-and-separate-consumer-refresh.md`) reads: "Verify overlapping-copy results against the exact deployed Windows CRT dependency, not a host approximation."

The mover's adjacent-hole control reaches the original `memcpy` import with overlapping source and destination, and the page stops there. OV-43's "actual Windows overlapping-copy behavior" half, on the nonempty-registration page, asks the same question.

**Answer (host measurement on the exact dependency, `overlap.py` D O K, FAILS 0).**
- **D, the dependency.** The certified image imports `memcpy` from `VCRUNTIME140.dll`, and the install ships none beside `FFXII_TZA.exe`. So the loader takes the machine's `C:\Windows\System32\vcruntime140.dll`: version 14.51.36247.0, 178,616 bytes, sha256 `d1f4225df2cd877dbf130d5668a021dce3f94118455ff5ec952061c30afc9ce7`.
- **O, the measurement.** That DLL's `memcpy` was driven through ctypes over **31,784 overlapping cases**:
  - the destination below and above the source;
  - every overlap shift from 1 to 64, plus powers of two up to 1 MiB;
  - sizes from 1 byte to 4 MiB, covering the small, vector and large paths;
  - source misalignment from 0 to 15.

  **None differs from an overlap-safe copy.** `memcpy` and `memmove` are separate exports in this DLL, but `memcpy` behaves as `memmove` on every tested overlap. With the destination 8 bytes above the source, it copies 0..31 intact, where a naive forward copy would repeat 0..7.
- **K, sensitivity.** The comparison flags a naive forward copy on a destination-above-source overlap, the defect OV-46 guards against.

**So** the mover's overlapping move produces the `memmove` result on this deployment. A reimplementation should give the copy `memmove` semantics.

**Not claimed.**
- **Other machines.** The dependency is the machine's redistributable, not pinned by the game, so another machine's `vcruntime140.dll` is a different dependency. This record names the one measured.
- **The game process.** No game process was run, so the result is of the DLL's function, not an observed in-game move.

**Proposed register disposition.**
- OV-46 → **ANSWERED** (host-measured on the named dependency).
- OV-43 → **ANSWERED** for its copy half by the same record; its scheduling-universality half stays superseded under OV-2, per the row.

Both boxes sit on SECTION carriers, so FRONTIER applies the rows and boxes.
