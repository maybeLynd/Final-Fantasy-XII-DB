# Level-0 run receipt: recon_depgraph.py first increment (SWE2-CONTRACT, 2026-10-03)

A dated snapshot of one run on the live inputs, taken to show what the design's section 5 predicted. It is a planning aid
and **not a metric**. Re-run: `python Database/Tools/analysis-kit/gfz-scripts/recon_depgraph.py build --out <prefix>`, then
`... check <prefix>.tsv` (CURRENT or STALE). The full TSV/JSON are not committed. This page records only the summary.

## Run (SWE2-CONTRACT)

- HEAD at run: `050fd9350`; generator sha256 `be1afd0001b86ef3`.
- Rebuilt at HEAD `c49f03691` with identical output; `recon_depgraph.py check` reported CURRENT, and the 8 fixture tests pass.
- Input fingerprints (sha256, CRLF-normalised, first 16):
  - `dispositions` `0b660b7d729a0ff4`
  - `edges` `7ce750a4485cc14d`
  - `field_access` `aa6016e111786d1b`
  - `functions` `5ddfe85af1e859a5`
  - `owner_map` `a15bd9f1830fd127`
  - `types` `7d4ff6752ffa591f`
  - `verbs` `b162fa7b61f09e68`
- Aggregated rows: **1385**, of which hard 1135 and sequencing 250.

| kind | basis | rows |
|---|---|---:|
| hard | call | 197 |
| hard | call-dispositioned | 877 |
| hard | type-layout | 61 |
| sequencing | call | 57 |
| sequencing | call-dispositioned | 190 |
| sequencing | script-binding | 3 |

Flags on rows (a row can carry several): `ambiguous` 421, `owner-conflict` 309, `unresolved-endpoint` 258.

## Result (SWE2-CONTRACT)

- Largest SCC of the hard subgraph (base layer 00/22/23/24 and `ambiguous`/`unresolved-endpoint` rows excluded): **21 nodes**.
- Topological layers of the condensation: 2. layer 0 = {14} + {21}; layer 1 = {01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 25, 26}.
- Weakly connected components: 1.

Read this as the design says: at category level one fact per pair is enough to tie the game into one co-reconstruction
cluster, so independent packages must come from level 1 (contracts via S5, completion packages via S6), which is the
next increment. The flagged rows are listed in the TSV; the generator resolves none of them.

## A gap the run found, not in the design note (SWE2-CONTRACT)

258 rows carry `unresolved-endpoint`. Apart from `99-Unresolved-Residual` (31 endpoint hits) and the unmapped owner token
`Story_Event_Quest_Hunt` (38; design §10), most come from **S2's far-layer column**. When the far body has no owner,
that column holds an `audit_crossrefs.subsystem_of` CodeDomain family rather than an owner token: `Gameplay` 69,
`Platform` 35, `World` 23, `SaveLoad` 18, `Application` 13, `Developer` 10, `InputGameplay` 8, `StoryEvent` 8, `Actor` 4,
`Combat` 2. `CODEDOMAIN-OWNER-MAP.tsv` maps chain labels to owner tokens, not CodeDomain families to folders, so those
endpoints stay unresolved and are kept out of the components. The generator already resolves a far end from the far
body's own ledger owner first and falls back to the S2 label. That changes none of the 258, because these far bodies
are unowned in the ledger too, which is why S2 printed a family for them. Resolving them needs a CodeDomain-family ->
folder mapping. None exists, and choosing one is a classification ruling for the owner-map and ledger owners, not
something this generator may invent.
