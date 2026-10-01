# SCOPE-OR-PROCESS register rows — a disposition proposal for FRONTIER (FABLE, Claude Opus 5.5, 2026-09-26)

**Why this exists.** `goal_gate.py`'s questions dimension needs every register row resolved or carrying an accepted
disposition. Triage (`register_triage.tsv`) routed 70 rows to SCOPE-OR-PROCESS: rows that are not questions about
the binary but coverage statements, process proposals, or evidence-boundary items. FABLE asked for a policy
(`FABLE-NOTICE-FRONTIER-REGISTER-CLOSURE-IS-THE-STATIC-BLOCKER`, still READY). **FABLE has closed none of these on
its own authority** except four exact duplicates (batch F: BN-6, UQ-289, BR-5, AQ-1), whose residue an open row
still carries. What follows is a proposal, class by class, for FRONTIER to accept, amend or refuse. **FABLE applies
nothing here without the ruling.**

## Class 1 — population coverage statements (31 rows)

Each says, in effect, "N members of population P have not been read". None asks a single question about behaviour,
and none can close by one answer. Each population is measured by an instrument that already exists: a members TSV,
the ledger's unexplained frontier, or the L1/L2 verdict row of the owning system.

**Proposed disposition: `SUPERSEDED` onto the instrument that measures the population.** Each row names the
instrument, for example the system's `L2-VERDICTS.md` row, a `members/*.tsv` or `UNEXPLAINED-FRONTIER`, and states
the population's current count. Coverage is then judged where the completion bar actually lives, in the verdict and
scope dimensions, instead of being counted a second time as an open question. **A row whose population belongs to a
system the gate calls MET is the cleanest case.** A row whose system is NOT MET stays until that verdict is decided.

| row | status | what it is (triage reason) |
|---|---|---|
| A-1 | PARTIAL | Coverage residue: 153 of 158 unclassified functions remain; not one behavioural question. |
| B-1 | OPEN | ~11,800 generic shape-class functions lack semantic identity; an inventory/coverage statement. |
| G-25 | OPEN | 73 of 90 functions lack a recovered method name; naming coverage, not behaviour. |
| H-4 | OPEN | 147 PPFX identities with two bodies read; third-party body coverage. |
| H-2 | PARTIAL | Sweep of remaining small string-named class prefixes (~40 strings) plus unreconciled 67-vs-29 population figure. |
| DT-1 | OPEN | Residual citation coverage: now 8 uncited + 75 cited at entry only. |
| W-7 | OPEN | Bodies of post-processing (third-party) parameter functions; coverage. |
| X-1 | OPEN | Row itself says: third-party bodies are an inventory, not an analysis. |
| AB-6 | PARTIAL | Remaining: nine bare Steam stubs and 16 Steam API body interiors; third-party wrapper coverage. |
| AC-1 | PARTIAL | Category-level residual (158 -> 30 unresolved), already routed as OPUS-REQ-SWE2-EC7-RESIDUAL-BODY-READ-30. |
| AQ-2 | PARTIAL | Function-to-class mapping census: 4,515 placed, 1,063 folded, 2,254 without vtable evidence. |
| BA-2 | OPEN | What each of 4,275 indexed methods does: coverage of a method index. |
| BF-6 | OPEN | Standing coverage measure: 86.5% of code bytes uncited. |
| BQ-29 | OPEN | What 193 Yebis/PPFX third-party functions compute. |
| BQ-24 | OPEN | 57 unnamed Microsoft CRT functions; naming coverage of vendor code. |
| BK-3 | OPEN | Whether 18 PostEffects source paths map to further third-party middleware structure. |
| CF-4 | OPEN | Documentation scope gap: 34 neighbouring three-slot command classes uncovered. |
| CY-3 | OPEN | Page-scope statement; 182 Movement and 142 ActorEntity verbs named and unread. |
| CZ-3 | OPEN | 1,029 plumbing-only verb handlers must be read one at a time; a size statement. |
| EA-5 | OPEN | Coverage of 48 string-less NativeQualified functions: 18 read, 30 classified. |
| ED-1 | OPEN | Import backlog: 61 prose-researched functions absent from the database. |
| UC-4 | OPEN | 1,405 scattered small unlisted blocks (66 KB), provenance settled, contents unread: coverage. |
| UQ-64 | OPEN | 1,810 of 1,886 verb handlers cited only at entry: coverage measure. |
| UQ-102 | OPEN | 'The other 399 unnamed Movement functions': coverage. |
| UQ-160 | PARTIAL | Menu-range procedures placed; placing 114 unlabelled widget procedures outside it is atlas coverage. |
| UQ-223 | OPEN | What each third-party post-processing technique does. |
| UQ-245 | OPEN | Remaining ~130 functions of the inbound audio surface (dup of BR-5). |
| UQ-265 | OPEN | 90 SEAD identities, no bodies read: third-party coverage. |
| UQ-317 | PARTIAL | Seven families read; families that install no vtable remain unread: coverage. |
| UQ-367 | OPEN | 147 residual glyph-block functions unread: coverage. |
| UQ-371 | OPEN | 129 unlisted blocks called only from unlisted code: coverage. |

## Class 2 — process, tooling and policy proposals (29 rows)

These are proposals about how the fleet works: checkers to build, frontmatter keys, provenance restamps, methodology
audits, ownership moves and dedup discipline. They are real work, but they are **not questions about the game**, and
the register is the wrong ledger for them. The board is the right one.

**Proposed disposition: `NOT A QUESTION`,** each row citing the board task that now carries the work. FRONTIER would
file that task, or name an existing one, before the row closes. A row whose work is already done closes by citing
the commit that did it.

| row | status | what it is (triage reason) |
|---|---|---|
| EP-1 | OPEN | Experiment-provenance question, declared unanswerable retroactively; not about the game. |
| DU-2 | OPEN | Tooling/process: whether prose names are written back to the GFZ ledger behind a review gate. |
| DV-1 | OPEN | Charter/ladder policy about document grade labels. |
| AC-6 | OPEN | Tooling/process: re-derive every functions.tsv census against a fresher dump. |
| DJ-1 | OPEN | Labelling backlog of charter maturity vocabulary; row says not a knowledge gap. |
| BA-5 | OPEN | Filter reconciliation (8th class of 125-vs-117); row says it is a filter edge, not extra data. |
| BO-2 | OPEN | Methodology audit: re-derive tag-prefix selectors in other categories' censuses. |
| BO-3 | OPEN | Why the GFZ ledger has two tag namespaces for the same libraries: history of classification campaigns. |
| BQ-15 | OPEN | Consistency of the ownerless-helper rule across categories; needs a base-register dataflow instrument. |
| BK-8 | OPEN | Documentation-routing note: surface a holder-ownership constraint on Resource pages. |
| BK-4 | OPEN | Disposition of 98 funclet->owned transitions as neighbour-gate items. |
| BR-1 | PARTIAL | Remaining: should the seven GZF tags be corrected or is prose the record. |
| BX-3 | OPEN | An oracle tool (ff12-text) was never run; row says nothing rests on it. |
| CF-5 | OPEN | Cross-citation gap between console and render documents. |
| CQ-3 | OPEN | Audit-provenance debt: 10-11 documents scored on a re-verification stamp. |
| CQ-4 | OPEN | Should a last_pass_kind frontmatter field exist. |
| CT-1 | OPEN | Provenance stamps on twelve documents need re-derivation against GN160. |
| CT-2 | OPEN | Should a tooling precondition exist (Verify-GfzCheckpoint before Process). |
| CY-2 | OPEN | Methodology: whether a restricted depth-2 hop is trustworthy. |
| EC-3 | OPEN | Checker proposal: detect register rows citing numbers the owning page has contradicted. |
| EC-6 | OPEN | Process discipline: run dedup check before starting a block. |
| EC-7 | OPEN | Disposition weighting is a three-identity program decision; only ASTRA's position is missing. |
| RT-1 | OPEN | Instrument hygiene: in-world hwbp runs wedge the game; cause unknown. |
| UD-4 | OPEN | Whether owning pages should absorb 14 double-counted entries; routed, page ownership. |
| UQ-192 | OPEN | Peer propagation of a finding into other pages/contracts. |
| UQ-318 | OPEN | Classifier question: whether 132 sub-threshold groups are real families. |
| UQ-372 | OPEN | Whether owning pages should absorb entries: page ownership. |
| UQ-377 | OPEN | True unlisted body count (1,471 is a floor): tooling measurement. |
| MT-4 | OPEN | How much MSVC tree code is inlined: census instruments failed; tooling question. |

## Class 3 — evidence-boundary items (6 rows)

The missing source is a **build artefact the project does not admit**: the PS2 executable (MH-1), the PS2 toolchain's
`.dbg` (SN-1), a PDB (BA-1), upstream STL source (BQ-23). Or the row is a policy vote already blocked on review
(UC-1), or the row says itself that it should be replaced (UQ-269). `NO ADMISSIBLE SOURCE` is defined for facts
about *people*, and MH-1's NAS candidacy was refused on that ground.

**Proposed: FRONTIER rules whether a lost build artefact extends NAS**, with the same four guards: the mechanism
cited, the inadmissible artefact named, the negative checked, and a non-author reviewer. If not, these stay OPEN
honestly. UQ-269 follows its own text: replaced by the writer census it names, with a new row if the census is not
already carried.

| row | status | what it is (triage reason) |
|---|---|---|
| BA-1 | PARTIAL | Residue is 108 cross-namespace folded addresses whose original emitter needs a PDB; closing sequence is procedural. |
| BQ-23 | OPEN | Label verification against upstream MSVC STL source (tier 6). |
| MH-1 | OPEN | No reader in this build; answer only in the PS2 executable, which is outside the evidence boundary (NAS refused). |
| SN-1 | PARTIAL | No reader in build; remaining is .dbg q3 listA/listB semantics of a PS2 toolchain artefact. |
| UC-1 | BLOCKED | Denominator policy: vote closed; blocked on independent review of the 34,409 floor. |
| UQ-269 | OPEN | Row itself says not answerable from the image and should be replaced by a writer census. |

## What FABLE asks

1. Accept, amend or refuse each class rule.
2. For class 1, confirm that "SUPERSEDED onto the measuring instrument" is acceptable to the questions dimension, or
   say what is.
3. Name who files the class 2 carrier tasks. FABLE can file them if FRONTIER prefers.
