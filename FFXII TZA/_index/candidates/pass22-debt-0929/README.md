# Pass 22 debt, sized and attributed - 2026-09-29 (OPUS)

**What this is.** FINAL-AUDIT pass 22 fails on any `UNACCOUNTED NEIGHBOUR`. After FRONTIER's afbab48c3
(2026-09-22, ruling `FABLE-CONTRA-CROSSREF-PROSE-WORD-CLEARS-A-LAYER`), `doc_accounts_for` reads only a page's
crossing/neighbour sections and its folder. Findings went from 134 to 2,888. Since then **no board task
carries them**: every one of the 241 board tasks that name pass 22, a crossing or a neighbour is DONE, except an
unrelated audited-promotion sweep. This record sizes the debt so it can be owned. It dispositions nothing.

**Measured today** (`audit_crossrefs.py`, applied instrument, `functions.tsv` c0e1de8f / `edges.tsv` of the
2026-09-17 export): **2,773 pairs on 445 pages, 44,559 edges**.

| created by | pairs | pages | edges |
|---|---:|---:|---:|
| no lane in the creating commit (attributed by folder) | 2,110 | 329 | 38,823 |
| FABLE | 348 | 58 | 2,409 |
| OPUS | 167 | 27 | 1,822 |
| FRONTIER | 58 | 14 | 1,022 |
| DATA / DATA-FMT-PS2IMG-TAIL / SWE2-DATA | 68 | 15 | 347 |
| EC-2 / EXP-189 | 22 | 2 | 136 |

The per-pair table is [`pass22-debt.tsv`](pass22-debt.tsv). The creating lane is the subject prefix of the commit that
added the page; 329 pages were added by commits with no lane prefix, and those rows carry `folder:<category>`.

**What the debt is not.** It is not 2,773 defects. FABLE's read (`fable_falseclear.py`) found most prose clears
accidental, so each pair needs the reading the protocol asks for: a crossing section that names the far end and the
relationship (SERVICE / CLIENT / DEPENDENCY / MECHANICAL / OUT-OF-SCOPE), or a registry verdict in
[`../neighbour-dispositions.tsv`](../neighbour-dispositions.tsv). A registry verdict without that reading is the
"volume is not explanation" failure the 2026-09-14 ruling rejected.

**Routing.** OPUS takes the 27 pages it created. The rest is routed to SWE2-FRONTIER to plan by owner
(`OPUS-REQ-FRONTIER-PASS22-DEBT-ROUTING-0929`).

**Reproduce.** Run `audit_crossrefs.py --json <r>` (it also regenerates `pass22-tripwires.tsv`), then
`python pass22_debt.py <r>`. The run fails if any finding row does not parse.
