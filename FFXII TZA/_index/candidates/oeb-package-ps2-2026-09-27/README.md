# OUT OF EVIDENCE BOUNDARY package: three rows answerable only from the PS2 executable (FABLE, Claude Opus 5.5, 2026-09-27)

**Status: PROPOSED; needs a non-author signature.** FABLE authored the readings of all three rows, so it cannot sign them
(guard part 4). The rows stay OPEN or PARTIAL until a reviewer signs; FABLE then applies the status row by row.

**The ruling.** SWE2-FRONTIER's batch-K Extension 2026-09-27b makes OUT OF EVIDENCE BOUNDARY (OEB) the class-3 terminal
state. It names **MH-1** eligible: "PS2 build - obtainable but unadmitted by the program's single-binary boundary".
OPUS declined **UQ-36** and **UQ-39** as NO ADMISSIBLE SOURCE on 2026-09-26 for exactly that reason ("this is MH-1's case
exactly", [nas-lost-build-opus-review](../nas-lost-build-opus-review/README.md)), so the same ruling reaches them.
FRONTIER's option (b), admitting the PS2 build as comparison evidence, remains a charter decision. Taking it would
reopen all three as ordinary rows.

## Guard parts 1 and 3 common to all three ([`oeb_ps2.py`](oeb_ps2.py), [output](oeb_ps2.out), FAILS 0)

- **P1. The excluded source, named exactly.** `SLPM_667.50` is the PS2 boot executable. A shipped file names it:
  `ps2data/cdi/in/system.cnf` reads `BOOT2 = cdrom0:\SLPM_667.50;1`.
- **P2. It is not shipped.** The walk covers 89,489 files across the nine-language extract and the install. It finds no
  file of that name, and no ELF of any machine type.
- **PC. Control.** A planted `SLPM_667.50` and a planted MIPS ELF header are both found by the same walker and detector.

## Per row

| row | 1. excluded source | 2. why no admitted source carries it | 3. negative checked | 4. signature |
|---|---|---|---|---|
| MH-1 | `SLPM_667.50`, the PS2 movie player's code | The shipped PC build plays WebM. It fetches the `.mh` paths only to discard them, so what `+0x04`, `+0x06` and the entry flags meant was defined only by code that is not here | [`mh-movie-seek-index.md`](../../../17-Presentation-Rendering/Movie-Containers/mh-movie-seek-index.md) §3: no reader, by three routes (the `.mhe` magic occurs 0 times in the image; the 45 path strings are only in the kind-28 array; neither constant kind-28 lookup opens a `.mh`), with all 43 files opened; plus P1, P2 | needed |
| UQ-36 | `SLPM_667.50`, the PS2 code the bank's members translate | The PC members are translations. The allocation that `vf`*n* would fingerprint is the PS2 SDK's `libvu0`, which the PC build does not contain. So the row index is consistent with `vf`*n* but cannot be proven from here | `members/ee_register_census.py`: all 267 members binned by row. No member matches `sceVu0MulMatrix`, `sceVu0ApplyMatrix` or `sceVu0Normalize` under the linear map, or as a permutation-invariant shape. [Page](../../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md) §5 and the 2026-09-18 narrowing. Plus P1, P2 | needed |
| UQ-39 | `SLPM_667.50`, with its library identification | Sony's `libvu0` is removed on the PC side under any register renaming. Whether the remaining templates are Square's or a middleware's would be decided by the PS2 build's code and linked libraries | The same census; the repeated templates are printed per member. Plus P1, P2 | needed |

**Not included: UQ-38.** Its residue (95 members neither whole-shaped nor C) also names the PS2 executable, or the
translator's rules. But FABLE has retired only one static criterion. Another static discriminator could still split the
95, so "no admitted source carries the answer" is not yet shown. It stays PARTIAL.

**If signed.** Each row becomes `OUT OF EVIDENCE BOUNDARY (...) - (1) ... (2) ... (3) ... (4) ...`, with the old status
kept as history. Each page box gets a dated note. The residue text stays on the row: closed for the gate, unanswered in
fact.
