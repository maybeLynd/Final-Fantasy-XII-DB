# Affected-consumer check: UQ-22, the 80 staged tunables named through the SceneWide cbuffer (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**The ruling** (control: `_index/candidates/uq22-scenewide-cbuffer/uq22_scenewide_map.py`; output `map.tsv`,
`result.json`):

- **Staging.** `006084B0` copies the tunables block into `00604750`'s local snapshot at `rbp+0x270`.
  - Block `+X` lands at snapshot `+0x110+X`.
  - The snapshot is 0x598 bytes, change-checked by a 0x598-byte `memcmp` and double-buffered at owner `+0x4E0`.
- **Translation.** `00604750` writes the GPU-layout buffer through `r14`, field by field from that snapshot. The map
  covers 294 store offsets with 0 conflicts. 11 stores are computed camera/screen values, not block fields.
- **The layout.** The store offsets are the compiled `SceneWideParameterConstantBuffer`: one layout (0x5F0 B, 154
  variables) in 4,799 shader blobs across `phyrechrshader.fx` and `phyredefaultlitshader.fx`, read from their DXBC
  RDEF chunks.
- **Controls:**
  - **K1:** block `+0x190..` lands on `mShadowCascadeProjection0..7`.
  - **K2:** the loader-keyed `chrFresnelSpecular*` land on the same-named variables.
  - **K3:** no conflicts.
  - **K4:** 80 of 80 of UQ-22's population map.
- **The three out-of-block tunables** (`01DFE1AC`, `01F82ED0`, `01F82EE4`) are touched only by the console
  `001D1660` and the menu renderer `001CD0E0`. This holds for rip-relative access and for a base formed within
  0x400 below them.

**What this corrects.** The tunes page's "the whole range is one shader constant buffer, staged in CPU memory" stands
as a statement about where the values end up. A reader could take it to mean that the staging offsets are the
cbuffer offsets, and they are not. A note now says so. Nothing is struck.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` UQ-22 | PARTIAL → ANSWERED, prior status kept | revised-here |
| `00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md` UQ-22 box | ticked, answer appended | revised-here |
| `00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md` §4 | snapshot-vs-cbuffer note added | revised-here |
| `00-Engine-Core-Runtime/Developer-Tuning-Console/members/scenewide-cbuffer-map.tsv` | new member table, generated from the control | revised-here |
| `members/console-tunables-consumers.tsv` (FABLE's) | untouched; the map joins it by address | agrees |

**Regression.** The control fails in any of these cases:
- the shipped layout count differs from 1;
- the shadow matrices or the Fresnel keys move;
- two stores disagree;
- any of the 80 loses its variable.

Run receipt: `uq22_scenewide_map.py` executed at 9bbd3fdb3 (controls_pass true).
