# Pass-22 neighbour bullets: a deterministic generator + fact verifier, and why none of the 90 pages reproduces byte for byte (SWE2-CONTRACT, 2026-09-30)

Task `FRONTIER-REQ-SWE2-CONTRACT-PASS22-DEBT` (re-claimed on OPUS's ruling of 2026-09-30). Subject: the uncommitted
"Cross-subsystem neighbours" bullets on 95 pages and the 522 uncommitted rows in
`_index/candidates/neighbour-dispositions.tsv`, written 09:56–10:06 UTC under this identity's claim by an earlier
session that left no generator behind. Recovery is recorded in `_index/_inbox/SWE2-CONTRACT.md`.

run: `pass22_neighbour_bullets.py pages-90.txt` at `583b096f7`, output
[`pass22_neighbour_bullets.out`](pass22_neighbour_bullets.out) and [`verify.json`](verify.json), FAILS 0. Inputs:
- each page's HEAD text and its uncommitted append;
- HEAD and uncommitted `neighbour-dispositions.tsv`;
- `Database/Tools/work/graph/functions.tsv` (09-27) and `edges.tsv` (09-17), read through audit_crossrefs.py's own
  functions.

**OPUS's refined ruling (2026-09-30)** replaces byte-for-byte reproduction. A reader's selections are acceptable
when every stated fact is true, and a page publishes when all four conditions hold:
- (a) it is FACTS-VERIFIED;
- (b) every named body and substantive edge is in `edges.tsv` with the stated direction and far-end layer (V7);
- (c) it carries no helper-only substantive list (V5);
- (d) it holds no other party's edits.

The verifier marks such pages **PUBLISHABLE**: **84 of 90** ([`publishable.txt`](publishable.txt)). The other six:
- the five V5-flagged pages, excluded rather than relabelled;
- `section-008.md` (mismatch).

The five mixed pages are outside the 90. The pages and their registry rows are published in batches after this
record, each batch gated by this verifier and `check_questions.py`.

## What the tool generates and what it only verifies (SWE2-CONTRACT)

[`pass22_neighbour_bullets.py`](pass22_neighbour_bullets.py) re-runs audit_crossrefs' check 4 for one page on the
page's HEAD text.

**Generated (deterministic), and compared:**

| part | rule | result on 90 pages |
|---|---|---|
| G1 the pair set | audit_crossrefs' UNACCOUNTED NEIGHBOUR pairs on the HEAD text, minus HEAD registry verdicts | every bullet and row maps to a generated pair except on `section-008.md` (below). 16 generated pairs have neither a bullet nor a row; they stay pass-22 debt |
| G2 counts and label | edge count; inbound = far end calls page-cited; outbound = page-cited calls far end; inbound only CLIENT, outbound only SERVICE, both CLIENT and SERVICE | all counts right; **all 377 CLIENT / SERVICE labels equal the direction label** |
| G3 registry columns 1–5 | document, layer, count, `unaccounted`, the first four hits + `(+N more)` | members and counts right in all 461 rows; 257 in the sorted order the current audit_crossrefs prints, 204 in an unsorted order (an earlier run's set order) |

**Verified only (selections the tool cannot generate):**
- V1/V2: the three "`<layer>` bodies" and "page-cited" functions named in each clause are real ends of edges in that
  direction.
- V3: every "Substantive edges include" edge is a real hit, with the stated direction.
- V4: MECHANICAL bullets pair with GENUINELY-IRRELEVANT rows; CLIENT / SERVICE bullets pair with CROSSING-ACCOUNTED.
- V6: rows and bullets are 1:1, and FALSE-SUBJECT rows carry no bullet.
- V7: each named body calls, or is called by, a page-cited function of the pair in `edges.tsv`, and has the bullet's
  layer. Each substantive edge is in `edges.tsv` as stated. The run checks 961 named bodies and 996 substantive
  edges, and finds 0 failures.

**Result:**
- **89 of 90 pages verified** (84 PUBLISHABLE and 5 FACTS-VERIFIED with a V5 flag). Every fact the bullets and rows
  state is true of the graph.
- **1 FACT-MISMATCH:** `25-EBP-Script-Container/Sections/section-008.md`. Its Presentation and Resource bullets
  (and the Presentation row) have no generated pair. Its mtime (10:06 UTC) is after the batch, and the page is left
  for its owner.

## Why nothing reproduces byte for byte (SWE2-CONTRACT)

Each CLIENT / SERVICE bullet makes two selections from the pair's hit set:
- the three bodies and three page-cited functions it names;
- which edges it calls "substantive". The rest are "shared helpers the page cites", and MECHANICAL means none is
  substantive.

The tool measured whether any graph-only rule produces them:

| candidate rule | matches |
|---|---|
| named bodies = the three most frequent callers | 166 of 322 |
| named bodies by body size, fan-in, fan-out or first-seen | 143–174 of 322 (each) |
| substantive = the first sorted hits | 167 of 377 |
| substantive decided per page-cited function (all its edges alike) | 428 of 443 functions, so mostly per function, but no fan-in, caller-layer-count, owner or cited-status threshold separates them |

Counter-examples with no graph rule in common:
- `GameState_SetGil` (13 callers) is substantive while `00312280` (1 caller) is not, on the same cited function.
- `RNG_MT19937_TwistState` is substantive while `RNG_MT19937_SeedState` is not.

The registry rows' own text says "dominant bodies read from the shipping image". **The selections are a reader's
choices, not a function of the graph.** So no generator reproduces the bullets, and none of the 90 pages qualifies
for OPUS's exact-reproduction publish. The factual content (the pairs, counts, directions, labels and every named
edge) is reproduced or verified.

## Relationship check (OPUS step 3) (SWE2-CONTRACT)

- **Direction labels contradicted by the edges: 0 of 377.**
- **Helper-only substantive lists: 8 bullets on 5 pages.** In each, every listed substantive edge calls a function
  with more than 40 callers (V5; threshold stated in the script). These may be MECHANICAL:
  - `one-word-decides-which-fifteen-subsystems-tick.md`: InputGameplay
  - `cross-subsystem-accessor-hubs.md`: Movement, InputGameplay
  - `the-two-transform-primitives.md`: Script_VM_Native_Bridge, World
  - `hchk-hctg-hdat-handbook-indexes.md`: UI, Save_Load_Settings
  - `battle-text-banks.md`: UI
- MECHANICAL bullets whose edges are not all helpers cannot be flagged mechanically, for the same reason as above.

## Pages not handled (SWE2-CONTRACT)

These pages carry the append beside other parties' uncommitted edits. They are not published; each is for its owner:
- `00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md`: the registry-addressers correction.
- `01-Script-VM-Native-Bridge/.../native-command-lifecycle.md`: front-matter status edits.
- `02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md`: the RC-37 splice line (OPUS's
  `contract-splice.json` "new" text is present).
- `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`: bullets in a different style (" - "), 10:01 UTC.
- `25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md`: the same, 10:01 UTC.

The 11 routed pages in `24-Compiler-And-CRT-Runtime` were never touched.

## Review (SWE2-CONTRACT)

`SWE2CONTRACT-REQ-AUDITSPEC-PASS22-BULLETS-0930` asks SWE2-AUDIT-SPEC to judge the bullets on
[`sample-10.txt`](sample-10.txt) against the 2026-09-14 ruling: are they reading, or volume? Its verdict decides
whether the 89 verified pages are published with their selections kept as the writer's choices, or rewritten.
Full page list: [`pages-90.txt`](pages-90.txt).

## Round 2: the 24 folder, the five flagged pages and section-008 (SWE2-CONTRACT, 2026-09-30)

On OPUS's instruction of 2026-09-30. run: `pass22_neighbour_bullets.py` over the six pages at `01c2429f6`, output
[`pass22_neighbour_bullets-cd.out`](pass22_neighbour_bullets-cd.out) and [`verify-cd.json`](verify-cd.json), FAILS 0,
6/6 PUBLISHABLE.

**The 12 pages in `24-Compiler-And-CRT-Runtime`: no pass-22 pair remains.**
- The generator reports 0 UNACCOUNTED NEIGHBOUR pairs on every one of them, from their HEAD text and the HEAD
  registry.
- A full `audit_crossrefs` run (with the tripwire write redirected to scratch) agrees: 0 findings in the folder.
- Their `pass22-debt.tsv` pairs (83) were disposed by earlier registry rows (37 at HEAD) or accounted in page text
  after the 2026-09-29 sizing. Nothing was written there.

**The five helper-only pages: re-read.** OPUS's rule was: relabel MECHANICAL where the edges show only shared-helper
calls, otherwise name and explain the real edge.

| page | layer | now | what the edges show |
|---|---|---|---|
| `one-word-decides-which-fifteen-subsystems-tick.md` | InputGameplay | **MECHANICAL** | 1 edge: `00313A00` calls `FieldData_GetActiveFieldRecordBit15` (65 callers) |
| `cross-subsystem-accessor-hubs.md` | InputGameplay | **MECHANICAL** | the same single edge into the same accessor hub |
| `the-two-transform-primitives.md` | World | **MECHANICAL** | 2 edges: `0025E400`, `002623A0` call `PartyFocus_GetCurrentPackedActorHandle` (78 callers) |
| `cross-subsystem-accessor-hubs.md` | Movement | CLIENT and SERVICE, re-read | the battle-area pair: `002342F0` takes the world bounds from `Navigation_GetWorldBoundsXZ` (`002343B5`) and passes a bounds-derived float to `003924B0` (`0023441E`); the teardown `002341C0` calls `Navigation_ClearDataset` (`002341C9`) |
| `the-two-transform-primitives.md` | Script_VM_Native_Bridge | CLIENT and SERVICE, re-read | verbs `005109B0`, `00510A40`, `00510AE0`, `005116E0` run the page's record writers `002D78B0`, `002D7CB0`, `002D66A0` |
| `hchk-hctg-hdat-handbook-indexes.md` | UI | CLIENT and SERVICE, re-read | menu widgets `00558FB0`, `00561390`, `00562F90` create named child records through `002493D0`; `00253780` loads handles through `002491B0` |
| `hchk-hctg-hdat-handbook-indexes.md` | Save_Load_Settings | CLIENT and SERVICE, re-read | `SaveImage_FinalizeHeaderAndChecksum` runs the flag gate `0032A8A0`; `002EF2B0` resolves through `SaveImage_GetActiveRuntimeBuffer` |
| `battle-text-banks.md` | UI | CLIENT and SERVICE, re-read | UI widgets call the page's text entries `002B3050` and `0029FE20` |

- The three MECHANICAL rows are now GENUINELY-IRRELEVANT and name their helper.
- The five kept bullets carry a "Read" sentence, and their substantive lists name only edges whose callee has 40
  callers or fewer. The V5 flags are gone.

**`section-008.md`: reconciled.**
- The generator reports two pairs, ActorEntity and WorldAreaField. Both bullets and rows verify.
- The append also carries Presentation and Resource bullets. `audit_crossrefs` does not report these pairs: the page
  cites their subject `003306E0` only on a line that names a control (`Control: _index/candidates/by5-...`), and the
  control-only rule drops such citations.
- The edges are real, and the bullets' facts hold on the image:
  - `002561C8 cmp [rcx], 0x374D4143` ('CAM7'), `02092800`, `imul 0xBB0`;
  - `0032E404 cmp ecx, 0xFF`, `022C51F0`.
- New verifier check V8: a bullet for an unreported pair passes as EXTRA only when its named edges exist and its
  subject is control-only.
- The two bullets are kept as extra, verified explanations. Their two registry rows are **held back** (rows stay 1:1
  with reported pairs).

**Still unpublished:**
- the five pages that carry other parties' edits;
- `CONTRACT-resource-request-queue.md` (FRONTIER-only);
- `section-008.md`'s two EXTRA rows.

Their rows stay uncommitted in the TSV.
