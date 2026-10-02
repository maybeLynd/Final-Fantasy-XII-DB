# SWE2-DATA readiness publish consumer-check — 2026-10-02

Per-lane record for the SWE2-DATA consolidated publish (pass-22 dispositions +
readiness edits + authored corrections). The fleet's batch records cover every
lane's files at once, which a single-lane publish cannot satisfy; this record
declares only the files this publish actually touches.

Consumer agreement: each edit was decided at the shipping image by OPUS's
readiness pass and routed to SWE2-DATA as the owning lane; the batch records
`opus-scriptvm-readiness-fixes-1002`, `opus-phyre-readiness-fixes-1002`,
`opus-ebp-readiness-fixes-1002`, `opus-movement-readiness-fixes-1002`,
`opus-world-readiness-fixes-1002` and `opus-party-readiness-fixes-1002` carry
the per-edit deciding addresses and the consumer agreement. The ASTRA/OPUS
authored-page narrowings cite their records inline (`sd194-stale-name-slice`,
`sd140`, the namespace-name-copy return).

Files this publish corrects — the set below is the complete declared affected
list, all touched by the commit:

- affected: `01-Script-VM-Native-Bridge/ATEL-Control-Modules/the-ctrl-module-debug-companions.md` — seven strike edits (C-V50, C-V56..C-V58 census counts and companions lines) plus the SN-1 "0-based" strike.
- affected: `03-World-Area-Field/choosing-the-field-environment-variant.md` — MWeather bit base includes the slot bias at `003777F9`.
- affected: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/how-a-class-registers-its-array-members-and-annotations.md` — two strike edits (lazy member-descriptor build; initialiser classification).
- affected: `25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md` — `REQALL`/`REQIALL` channel-pop strike at line 497.
- affected: `22-Middleware-PhyreEngine/Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md` — two strike edits (NS-1 w7 loader flag, unexplained mark).
- affected: `22-Middleware-PhyreEngine/the-camera-state-snapshot.md` — strike edit on the record scope.
- affected: `06-Movement-And-Navigation/clamping-a-point-into-a-volume.md` — outcode history reader is `0025C830`.
- affected: `06-Movement-And-Navigation/the-unit-shape-distance-primitives.md` — D5A0 shape helper's fourth output lane is horizontal distance.
- affected: `17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md` — three SD-140 narrowings (`+0x40` is the draw-parameter block; `+0x28` unblended under `+0x1F1` bit 4; §22.5 BI-3a wording).
- affected: `17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md` — SD-194 stale-name slice §2c.
- affected: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md` — `ResourcePath_Copy` signed-limit narrowing.

Non-marker data rows in the same commit (no prose correction): five
`party-roster-slots-accesses.tsv` writer rows annotated out of route
resolution (array `0209A210`), and three `fields.tsv` PhyreClassDescriptor
rows (`+0xC8`/`+0xD0` byte-mask pointers, `+0xF4`/`+0xF8` running sums).

Regressions that measure them — each control was run this session, FAILS 0:

- run verified at commit 1f193fec9: `opus-scriptvm-readiness-fixes-1002/scriptvm_check.py` — FAILS 0.
- run verified at commit 0adae56fa: `opus-phyre-readiness-fixes-1002/phyre_check.py` — FAILS 0.
- run verified at commit 8ccd3aad3: `opus-ebp-readiness-fixes-1002/ebp_check.py` — FAILS 0.
- run verified at commit c8a281ba1: `opus-movement-readiness-fixes-1002/movement_check.py` — FAILS 0.
- run verified at commit 185789b98: `opus-world-readiness-fixes-1002/world_check.py` — FAILS 0.
- the census regeneration is controlled by `gen_req_channel_census.py` itself (10036 files, 237662 scripts, 530028 sites, 0 anomalies).

Agreement: SWE2-DATA agrees with each routed edit and applied only the edits
assigned to SWE2-DATA by `apply_by_owner.py SWE2-DATA` in each batch; no other
lane's lines were touched.
