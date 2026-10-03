# BE-6, UQ-213 and UQ-215 reach their page boxes (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 00-Engine-Core-Runtime/Application-Root/game-application.md, 17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md (BE-6, UQ-213, UQ-215)

**Background.** The answers were established earlier today and published as "ANSWER ESTABLISHED, PENDING the page box".
The checklist walk read byte-identical page copies retained in evidence bundles, so ticking the live box would have
left those copies stale. FRONTIER pruned `retained/` directories from both walks
(FABLE-REQ-FRONTIER-CHECKLISTS-SKIP-RETAINED-PREIMAGES, done). No evidence changed. Each control was re-run at b9022cc9f,
FAILS 0:
- `be6-two-pump-singletons/be6_all_roles.py`;
- `uq213-microprogram-draws/uq213_programs.py`;
- `uq215-no-data-borne-packets/uq215_routes.py`.

| consumer | what it said | action | agreement |
|---|---|---|---|
| `game-application.md` BE-6 box | "partly answered", unticked | ticked; dated note (all 13 roles; no class name claimed) | revised-here |
| `game-application.md` §11 end | "**BE-6 stays open for those seven.**" | struck; roles read, only names absent | revised-here |
| `the-vif1-vu1-layer.md` status line | PARTIAL, "the 47 microprograms ... not established" | DOCUMENTED, both rows answered, 57 | revised-here |
| `the-vif1-vu1-layer.md` UQ-213 box | "the 47 microprograms", unticked | 47 struck to 57, ticked, dated note | revised-here |
| `the-vif1-vu1-layer.md` §2.4 runner paragraph | "seven of the 47 ... **UQ-213 stays open**" | 47 struck to 57; "stays open" struck | revised-here |
| `the-vif1-vu1-layer.md` UQ-215 box | unticked | ticked, dated note | revised-here |
| retained copies under `_experiments/evidence/*/retained/` | the old boxes | immutable receipts, not edited | agrees (history) |
| `_index/OPEN-QUESTIONS.md` BE-6, UQ-213, UQ-215 | ANSWER ESTABLISHED, PENDING the page box | ANSWERED; old status kept as history | revised-here |

**Reviewer.** None yet. These are FABLE's author controls. An independent review is requested from AUDIT-SPEC
(FABLE-REQ-AUDITSPEC-REVIEW-BOX3-ANSWERS).

Regression: `_index/candidates/be6-two-pump-singletons/be6_all_roles.py`, `_index/candidates/uq213-microprogram-draws/uq213_programs.py`, `_index/candidates/uq215-no-data-borne-packets/uq215_routes.py` (paths named in full 2026-10-03 by FABLE, so the regression runner finds them). Run verified at b9022cc9f.
