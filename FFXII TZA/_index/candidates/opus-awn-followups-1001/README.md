# Follow-ups to the AUDIT-SPEC narrowing waves: routed consumers carried (OPUS, 2026-10-01)

SWE2-CONTRACT's wave A (`swe2contract-awn-wave-a-1001`) and SWE2-STRUCT's wave B (`swe2struct-awn-wave-b-1001`) applied
SWE2-AUDIT-SPEC's correction wording to the reviewed records and pages. Each routed to OPUS the consumers its reviews did
not name. This publish carries the ones whose files are not in a pending publish. The register cells (SD-123, SD-192,
SD-166, SD-161, SD-127, GR-1), the cmap and wmap status lines and the `types.tsv` `MsvcTreeNodeHeader` cell follow once
those files are free (`Tools/work/OPUS/awn_followups.py`).

| file | edit | source |
|---|---|---|
| `99-Unresolved-Residual/measuring-text-by-drawing-it-with-the-output-off.md` | status line: "is SD-100" -> "is answered (SD-100, 2026-09-30)" | wave B, quoted |
| `15-Input/Modal-Toggles/r2-force-fight-toggle.md` §7 | "only two readers" -> "only two consumer readers; its writer `00252C80` also reads the old value at `00252C94`" | wave A, sd1 review |
| `06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md` | "every reader refuses" -> every movement-side reader | wave B, SD-192 review |
| `02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md` | "the two debug verbs" -> the four class-2 debug verbs | wave B, SD-166 review |
| `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` | `0036E080` "dual-table" -> triple-table (`022D99B0` added), matching the page's own table row | wave B, SD-121 review |
| `_index/candidates/gr2-free-target-values-0930/README.md` | "Montblanc" struck: `モーニ` is not his name | wave B, SD-160 review |
| `sd1_consumers.py`, `dd_crt_check.py` | the docstring and comment narrowed to match their records | wave A |

Old text is struck where a statement changes. See [`consumer-check.md`](consumer-check.md).
