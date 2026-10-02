# Consumer check: ASTRA's SD194 stale-name slice, presentation-index domain and mode-summon tail returns consumed (OPUS, 2026-10-02)

Board returns ASTRA-RETURN-OPUS-SD194-STALE-NAME-SLICE-1001, -PRESENTATION-INDEX-DOMAIN-1001 and -MODE-SUMMON-TAIL-1001 (each SWE2-AUDIT-SPEC ACCEPT). Every consumed fact was re-read at the image (`astra3_check.py`). Each edit is a dated qualification after the statement it narrows; nothing is struck. Premises and open items are kept: no natural reachability, fault or effect is claimed beyond the accepted scope. The natural equal-branch admission of `00309230` is routed to FABLE as a dependency.

The pass drafted 15 edits (`apply_astra3.py`). OPUS applies the 9 on its own lines (`apply_by_owner.py OPUS`).

- 3 go to FABLE (`apply_by_owner.py FABLE`).
- 1 go to SWE2-FRONTIER (`apply_by_owner.py FRONTIER`).
- 1 go to SWE2-DATA (`apply_by_owner.py SWE2-DATA`).
- 1 go to SWE2-EC7 (`apply_by_owner.py SWE2-EC7`).

- **Affected:** 00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md, 01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md, 03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md, 04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md, 11-Party/Battle-State-Block/the-battle-state-block-field-map.md, 17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the OPUS-led pages listed above (OPUS lines) | revised-here |
  | CONTRACT-battle-state-block.md, battle-command-availability-and-reason-codes.md, the-battle-stats-record-field-map.md | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 3 edits) |
  | the-map-ctrl-pack.md | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py FRONTIER`, 1 edits) |
  | efx-and-efb-effect-containers.md | routed-to-SWE2-DATA (request with `apply_by_owner.py SWE2-DATA`, 1 edits) |
  | battle-runtime-mode-ladder.md | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 1 edits) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-astra-returns-consume-1002/astra3_check.py, verified at f4da4b816: 5 instructions decode as cited, FAILS 0 ([`astra3_check.out`](astra3_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (9), FAILS 0.

**Pass-22 neighbours.** Other layers' functions in NEW text are named by role or ledger name; `check_page_neighbours.py` shows no new hit on any edited page.
