# SWE2-DATA readiness publish consumer-check — round 3, 2026-10-02

Per-lane record for the third SWE2-DATA consolidated publish (render-A/B/C,
resource-B, residual and ASTRA-returns readiness lines, plus the SD-7
re-review incorporation). The fleet's batch records cover every lane's files
at once, which a single-lane publish cannot satisfy; this record declares only
the files this publish actually touches.

Consumer agreement: each line edit was decided at the shipping image by OPUS's
readiness pass and routed to SWE2-DATA as the owning lane; the batch records
`opus-render-a-readiness-fixes-1002`, `opus-render-b-readiness-fixes-1002`,
`opus-render-c-readiness-fixes-1002`, `opus-resource-b-readiness-fixes-1002`,
`opus-residual-readiness-fixes-1002` and `opus-astra-returns-consume-1002`
carry the per-edit deciding addresses and the consumer agreement. The SD-7
incorporation consumes the accepted review
`auditspec-review-sd7-oracle-0930/REVIEW-1002.md` (record `f6f51fba5`).

Files this publish corrects — the set below is the complete declared affected
list, all touched by the commit:

- affected: `17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md` — two render-A strikes (census check count, `@FMW` is a track-data record) plus render-B's fef line and two render-C lines.
- affected: `17-Presentation-Rendering/Model-And-Motion-Formats/fdm-and-for-entries.md` — four render-B strikes plus six render-C strikes (the 21 missing files are all weapons; `004201F0` is 143 insns; table A/B resolved 2026-09-29; sampled consumers partly read).
- affected: `17-Presentation-Rendering/Model-And-Motion-Formats/ftr-node-table.md` — one render-B strike.
- affected: `17-Presentation-Rendering/Model-And-Motion-Formats/fte-fct-texture-colour-tables.md` — two render-B strikes plus four render-C strikes (`1,972` header records over every `@FCT` entry; the `0x40` count is 36; `00504D20` has three call sites).
- affected: `17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md` — render-C: section 5 is read inline in `003E7210`.
- affected: `17-Presentation-Rendering/Model-And-Motion-Formats/README.md` — render-C: the `@FMN`/`@FMW` pair is name/track-data.
- affected: `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md` — render-C: the register row is SUPERSEDED as a duplicate of `BT-3`.
- affected: `17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md` — six render-C edits (`+0x28` census `155,916`; colour/UV labels answered by §8 SD-140; scope named on two census rows). The seventh routed edit, on the status line, was refused by the applier because the line was already rewritten by the earlier kind-54 residue publish (`9f0516954`) — superseded, no stale text remains.
- affected: `17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md` — one ASTRA-returns consume edit.
- affected: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/amap-menumap-area-table.md` — one resource-B strike.
- affected: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md` — one resource-B strike.
- affected: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/hchk-hctg-hdat-handbook-indexes.md` — five resource-B strikes.
- affected: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/gmap-menumap-guide-texts.md` — one resource-B strike.
- affected: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/the-dat-and-bin-extension-buckets.md` — two resource-B strikes.
- affected: `99-Unresolved-Residual/measuring-text-by-drawing-it-with-the-output-off.md` — one residual strike.
- affected: `15-Input/Input-Stack/input-stack-device-channel-and-bindings.md` — SD-7 incorporation: the accepted repair's partition (150 excluded / 42 remain, `sd7_app_pointer_sites.py` K1–K6+S1 FAILS 0) appended to the §5 row.
- affected: `_index/OPEN-QUESTIONS.md` — SD-7 register row updated with the re-accepted corrected partition (E1 125 not 133, PPFX residue 28 not 20; eight frame-pointer stack-slot reads unexcluded).

Regressions that measure them — each control was run this session, FAILS 0:

- run verified at commit f81176bae: `opus-render-a-readiness-fixes-1002/render_a_check.py` — FAILS 0.
- run verified at commit f81176bae: `opus-render-b-readiness-fixes-1002/render_b_check.py` — FAILS 0.
- run verified at commit f81176bae: `opus-render-c-readiness-fixes-1002/render_c_check.py` — FAILS 0.
- run verified at commit f81176bae: `opus-resource-b-readiness-fixes-1002/resource_b_check.py` — FAILS 0.
- run verified at commit f81176bae: `opus-residual-readiness-fixes-1002/residual_check.py` — FAILS 0.
- run verified at commit f81176bae: `opus-astra-returns-consume-1002/astra3_check.py` — FAILS 0.
- run verified at commit f81176bae: `sd7-stored-app-pointer-0930/sd7_app_pointer_sites.py` — FAILS 0 (K1–K6, S1; partition 125/13/2/10/42).

Agreement: SWE2-DATA agrees with each routed edit and applied only the edits
assigned to SWE2-DATA by `apply_by_owner.py SWE2-DATA` in each batch; no other
lane's lines were touched.
