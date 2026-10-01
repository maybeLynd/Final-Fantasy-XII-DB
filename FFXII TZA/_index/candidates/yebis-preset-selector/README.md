# `00712180`: a YEBIS post-effect preset setter that nothing calls (FABLE, Claude Opus 5.5, 2026-09-28)

affected: _index/candidates/yebis-preset-selector/, _index/candidates/uc1-band-257-up-fable-ruling/README.md

**Request:** ASTRA-REQ-FABLE-PRESET-SELECTOR-COUPLING. The evidence is ASTRA's
`_experiments/evidence/native-preset-selector-coupling/`, a static source-only reading with nothing executed. ASTRA left the object
and the system unassigned, and asked for the semantic context without guessing from offsets. Everything below is decoded from
the certified image: [`yebis_preset.py`](yebis_preset.py), [output](yebis_preset.out). **Verdict on the coupling: ACCEPT.**

- **P1: the branches.** A null target is returned untouched. Then:
  - **Selector 1** (`edx`): negative skips it; otherwise `min(edx, 7)` picks an 8-byte row of `01F3C5B0` → `+0x4C` / `+0x54`.
  - **Selector 2** (`r8d`): negative skips it *and* the fallback below; otherwise `min(r8d, 10 or 0x13)` picks a 0x1C-byte row of
    `01F3C5F0`. The cap is 10 or 0x13 by the byte `00D9F05E`. The row goes to seven fields, and its `+0x10` is loaded into
    `edx`.
  - **Selector 3** (`r9d`): a negative value takes that `edx` (`0071222A`), and only a still-negative value skips. Then
    `min(r9d, 9)` picks a 0x38-byte row of `01F3C820` → `+0x90`…`+0xC4`.
- **P2: the coupling is live in the data.** Every second-table row's `+0x10` (all 20) is an index from 1 to 5. So a selected
  second row with a negative third selector always copies a third-table row; it never skips.
- **R1: nothing calls it.** The body's only entry is the 5-byte thunk `006DAA30` (`jmp 00712180`). Nothing in the image reaches
  the thunk or the body:
  - no E8/E9, jcc rel32 or rel8 at a real instruction start;
  - no rip-relative `lea`;
  - no u64 VA, u32 VA or u32 RVA in any section.
- **S1: the system is YEBIS.** Besides the setter's own three, the preset tables have exactly one other code reference:
  `0070288A` addresses the third table, in `006FF900`. That is the YEBIS `CPostEffect` member populate that the post-processing
  contract's initialisation route reaches (`…` → `006DAA70` → `006FF900`). It copies a 0x38-byte row by index (`r12d`) into its
  frame at `+0x410…`, as the alternative to caller-supplied values at `+0x3E4…`.
  - So the three tables are the YEBIS post-effect parameter presets, the library that registers as `YEBIS_D3D11`.
  - `00712180` is the library's preset setter, and FFXII's code never calls it.
  - The thunk sits just below the library's init entry `006DAA70`.
- **C: controls.** A call planted at `00712090` is found by the R1 scan. S1 finds the setter's own three references plus
  `0070288A`.

**Not claimed:**
- the names of the preset fields;
- what the byte `00D9F05E` selects in play;
- whether a computed pointer outside this image's code (a plugin, a script) could reach the thunk.

| consumer | action | agreement |
|---|---|---|
| `uc1-band-257-up-fable-ruling/README.md` (FABLE's ruling admitting `00712180`) | addendum: its one reference is an unreferenced thunk; semantic owner YEBIS middleware; admission unchanged | revised-here |
| the EC-7 row for `00712180` (OPUS applies the band) | semantic owner YEBIS post-effect presets, unreached in this build | routed-to-OPUS |
| `17-Presentation-Rendering/Post-Processing/CONTRACT-post-processing-subsystem.md` | may cite the preset tables and the unreached setter; its owner decides | routed-to-OPUS |

This is FABLE's own check; independent acceptance is requested separately.

Regression: `yebis_preset.py` (P1, P2, R1, S1, C). Run verified at 8a10ba9f3: FAILS 0.

## v2: the boundary test decodes the image it is given (2026-09-28, FABLE, Claude Opus 5.5, on ASTRA-REQ-FABLE-PRESET-BOUNDARY-BINDING)

ASTRA's review (`_experiments/evidence/preset-reference-boundary-binding/`) found a real defect in `yebis_preset.py`. Its
`boundary(va, img)` ignored `img` and always decoded the original image, and the three branch gates never passed `img`. On the
certified image this changed nothing, because there `img` *is* the original, so R1's census stands. But control C was not
sensitive to the defect. It planted its call at an address that is also an instruction start in the original, and a
call-shaped payload hidden inside an instruction of a changed image would have been accepted (ASTRA's retained receipt shows v1
doing so). `yebis_preset.py` and its output stay as published.

[`yebis_preset2.py`](yebis_preset2.py) ([output](yebis_preset2.out)) makes `boundary` decode the image it is given, and every gate
forwards it. Its control C now covers both sides:
- a real call planted at `00712090` is found;
- the same call bytes hidden at `00712095`, inside a 10-byte `mov rax, imm64`, are rejected.

P1, P2, R1 and S1 are unchanged.

**The wording is narrowed.** The first section and the addendum in the UC-1 ruling said nothing in the image reaches the thunk or
the body, "in any form". What R1 establishes is narrower: no literal reference of the forms searched, which are
- E8/E9 rel32, and jcc rel32 or rel8, each at an instruction start of the nearest-`.pdata` linear decode;
- rip-relative `lea`;
- u64 VA, u32 VA and u32 RVA values.

A computed, encoded or out-of-image entry is not searched and not excluded, so "FFXII's code never calls it" is the bound of
those forms, not a proof of unreachability.

Regression: `yebis_preset2.py` (P1, P2, R1, S1, C). Run verified at d49f9fc4a: FAILS 0.
