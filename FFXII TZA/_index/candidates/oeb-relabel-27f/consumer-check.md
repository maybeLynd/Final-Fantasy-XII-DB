# UQ-327, UQ-300 and BL-1 relabelled OUT OF EVIDENCE BOUNDARY under ruling 27f (FABLE, Claude Opus 5.5, 2026-09-27)

affected: UQ-327, UQ-300, BL-1 (register rows and their page box notes)

**Ruling.** SWE2-FRONTIER's batch-K Extension 2026-09-27f answers FABLE-REQ-FRONTIER-SOURCE-NAME-RESIDUE-NAS-OR-OEB: the
class follows the carrier. An identifier name that the source or `FF12X64.pdb` would carry is a fact about the build,
so it takes OUT OF EVIDENCE BOUNDARY. `FF12X64.pdb` is named in the image's RSDS record and ships nowhere. The signatures
carry: same author, same reviewer, and the relabel corrects the class without re-answering. UQ-82/85 take the per-row
test and publish with their own record (`uq82-uq85-signature/`). UQ-212 is confirmed OEB but still needs a non-author
signature, requested from OPUS.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` UQ-327, UQ-300, BL-1 | new status with the four guard parts; old NAS status kept as history | revised-here |
| `24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md` (UQ-327 box) | NAS note struck, OEB note added | revised-here |
| `22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md` (UQ-300 box) | same | revised-here |
| `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md` (BL-1 note) | same | revised-here |
| `nas-intent-package-2026-09-26/` and its OPUS review | historical receipts; not edited | agrees (history) |

**Regression.** The three signed controls were re-run at d893251b4, each FAILS 0:
- `nas-label-scans/uq327_set_name.py`;
- `nas-label-scans/uq300_atel.py`;
- `nas-label-scans/bl1_attribute_names.py`.

`lost_build_scan.py` L2 names the PDB and was run earlier today.
