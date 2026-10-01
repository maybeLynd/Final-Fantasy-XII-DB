# Pass 22 debt routing — SWE2-FRONTIER, 2026-09-29

Owner assignment for `pass22-debt.tsv` (OPUS-REQ-FRONTIER-PASS22-DEBT-ROUTING-0929).
Routing rule: the lane named by `created_by` owns its rows; unattributed `folder:*`
rows go to the lane whose remit fits the folder's content. Each owner reads each pair
and writes a crossing section naming the far end + relationship class
(SERVICE / CLIENT / DEPENDENCY / MECHANICAL / OUT-OF-SCOPE), or a registry verdict in
`../neighbour-dispositions.tsv`. Semantic-hard pairs escalate to FABLE. One task per
lane; the TSV rows are the worklist, not the verdict.

| group | pairs | pages | owner | board task |
|---|---:|---:|---|---|
| OPUS | 167 | 27 | OPUS | FRONTIER-REQ-OPUS-PASS22-DEBT-OWN |
| FABLE | 348 | 58 | FABLE | FRONTIER-REQ-FABLE-PASS22-DEBT-OWN |
| FRONTIER | 58 | 14 | SWE2-FRONTIER | SWE2-FRONTIER-PASS22-DEBT-OWN |
| DATA / SWE2-DATA | 68 | 15 | SWE2-DATA | (folded into SWE2-DATA bundle) |
| EC-2 / EXP-189 | 22 | 2 | SWE2-EC7 | (folded into SWE2-EC7 bundle) |
| folder:00-Engine-Core-Runtime | 262 | 42 | SWE2-CONTRACT | FRONTIER-REQ-SWE2-CONTRACT-PASS22-DEBT |
| folder:01-Script-VM-Native-Bridge | 82 | 17 | SWE2-CONTRACT | same |
| folder:02-Resource-And-Asset-Pipeline | 123 | 24 | SWE2-CONTRACT | same |
| folder:24-Compiler-And-CRT-Runtime | 71 | 11 | SWE2-CONTRACT | same |
| folder:25-EBP-Script-Container | 54 | 14 | SWE2-CONTRACT | same |
| folder:26-PKFL-Package-Container | 5 | 1 | SWE2-CONTRACT | same |
| folder:03-World-Area-Field | 112 | 12 | SWE2-EC7 | FRONTIER-REQ-SWE2-EC7-PASS22-DEBT |
| folder:05-Spawn-Encounter-Lifecycle | 89 | 7 | SWE2-EC7 | same |
| folder:06-Movement-And-Navigation | 74 | 12 | SWE2-EC7 | same |
| folder:11-Party | 51 | 6 | SWE2-EC7 | same |
| folder:12-Items-Equipment-Shops-License | 55 | 10 | SWE2-EC7 | same |
| folder:14-Story-Event-Quest-Hunt | 30 | 3 | SWE2-EC7 | same |
| folder:99-Unresolved-Residual | 118 | 20 | SWE2-EC7 | same |
| folder:04-Actor-Entity | 144 | 16 | FABLE | FRONTIER-REQ-FABLE-PASS22-DEBT-UNATTRIBUTED |
| folder:07-Combat-Action | 90 | 11 | FABLE | same |
| folder:08-Combat-Formula | 71 | 15 | FABLE | same |
| folder:09-Combat-AI-And-Gambits | 21 | 2 | FABLE | same |
| folder:10-Status-Periodic-Terminal | 47 | 7 | FABLE | same |
| folder:13-Rewards-Progression-Economy | 67 | 9 | FABLE | same |
| folder:15-Input | 73 | 6 | SWE2-DATA | FRONTIER-REQ-SWE2-DATA-PASS22-DEBT |
| folder:16-UI | 66 | 16 | SWE2-STRUCT | FRONTIER-REQ-SWE2-STRUCT-PASS22-DEBT |
| folder:17-Presentation-Rendering | 99 | 21 | SWE2-STRUCT | same |
| folder:18-Audio | 103 | 17 | SWE2-DATA | FRONTIER-REQ-SWE2-DATA-PASS22-DEBT |
| folder:19-Save-Load-Settings | 44 | 8 | SWE2-DATA | same |
| folder:20-Platform-Online-Achievements | 19 | 2 | SWE2-DATA | same |
| folder:21-RNG-And-Determinism | 59 | 4 | SWE2-STRUCT | same |
| folder:22-Middleware-PhyreEngine | 63 | 13 | SWE2-STRUCT | same |
| folder:23-Third-Party-Libraries | 18 | 3 | SWE2-STRUCT | same |

**Totals per lane:** FABLE 788 (348 own + 440 unattributed), SWE2-EC7 551 (529 + 22
EXP-189), SWE2-CONTRACT 597, SWE2-DATA 307 (239 + 68 own), SWE2-STRUCT 305, OPUS 167,
SWE2-FRONTIER 58. Total 2,773 pairs / 445 pages — matches the record.

**Remit rationale:** CONTRACT takes the engine/pipeline/compiler folders — crossing
sections there are canonical reference linking (its remit). FABLE takes the
semantics-heavy gameplay folders (actor/combat/status/rewards) where the relationship
class is a mechanism judgement, plus escalation of semantic-hard pairs from any lane.
EC7 takes world/lifecycle/content folders and 99-Unresolved-Residual (its uncovered-
code/family remit) plus the two EXP-189 pages (EC-2 is its predecessor identity).
STRUCT takes middleware/presentation/UI/RNG/third-party (structural/layout analysis).
DATA takes input/audio/save-load/platform (its obligation-links/coverage remit) plus
its own 68. OPUS and FRONTIER keep their own pages.
