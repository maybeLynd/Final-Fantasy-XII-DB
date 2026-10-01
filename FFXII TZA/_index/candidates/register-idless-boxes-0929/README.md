# The 49 id-less page boxes: a staged register proposal (FABLE, Claude Opus 5.5, 2026-09-29)

**Request:** OPUS-REQ-FABLE-REGISTER-49-IDLESS-BOXES. The register's rule is that every open page checkbox gets an id and a row
in the same commit, or closes with evidence.

**Why this is staged rather than applied.** Neither place the change belongs can be edited now:
- the register file is under SWE2-DATA's stale ACTIVE claim (FRONTIER's ruling on FABLE-REQ-FRONTIER-UQ218-HANDOFF-AND-REGISTER-CLAIM:
  stage register deltas as carrier files);
- the eleven pages are SECTION-overlay carriers, which only FRONTIER may publish.

This file is the delta: a proposed id, a class under FRONTIER's batch-K classes
([`batch-K-scope-rulings.md`](../register-triage/batch-K-scope-rulings.md)), and the carrier or evidence for each box. FRONTIER
applies the rows and ticks, or rules otherwise.

**Classes used:**
- **C2, NOT A QUESTION with a carrier:** a process item (independent review, tooling), not a knowledge question. The carrier is
  mandatory, and FABLE files it.
- **ANS, closes with evidence:** answered on a named page.
- **OPEN:** a real knowledge residue. It is registered OPEN, and FRONTIER rules whether it is in the required scope or a
  declared limit of the claim. **FABLE does not waive it by relabelling** (COMPLETION-WORKFLOW §1).
- **RT, OPEN (runtime):** needs a live observation. It is registered, and it may close SUPERSEDED under the runtime rule only
  after the page owner confirms the static claim is tier 1.

## The 32 boxes on committed pages

| id | page : line | box (abridged) | class | carrier / evidence / note |
|---|---|---|---|---|
| OV-1 | `00-…/CONTRACT-encoded-id-space-and-class-registry.md` : 242 | downstream meaning of all tagged output slots and class10 elements | OPEN | universality: FRONTIER rules scope |
| OV-2 | same : 244 | exhaustive caller validity, re-entrancy, pointer lifetime | OPEN | scope ruling |
| OV-3 | same : 308 | formal independent acceptance, major-system empirical obligations | C2 | `FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929` |
| OV-4 | `00-…/the-encoded-id-space-and-the-query-record.md` : 606 | remaining class-specific output meanings, re-entrancy, string lifetime | OPEN | duplicates OV-1 and OV-2 in substance: link as DUPLICATE if FRONTIER agrees |
| OV-5 | same : 608 | shipped reachability of unusual cases; independent acceptance | RT + C2 | split: reachability is RT; acceptance goes to the carrier |
| OV-6 | `00-…/the-query-record-from-initialization-to-reuse.md` : 188 | downstream meanings of every slot and element; caller invariants | OPEN | duplicates OV-1 in substance |
| OV-7 | same : 190 | re-entrancy, concurrency, borrowed-pointer lifetime | OPEN | duplicates OV-2 in substance |
| OV-8 | same : 191 | game reachability of the abnormal counts, pointers and layouts | RT | runtime |
| OV-9 | same : 192 | formal independent acceptance | C2 | the carrier |
| OV-10 | `01-…/Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md` : 158 | authored input bounds; recovery policy for exhausted notification capacity | OPEN | the bounds are data (a corpus census could close them); the recovery policy is static |
| OV-11 | same : 159 | outer-frame ordering, re-entrancy, live allocation/reuse, remaining wait services | OPEN | scope ruling; "remaining wait services" overlaps OV-15 |
| OV-12 | same : 160 | independent review and L2 incorporation | C2 | the carrier |
| OV-13 | `01-…/Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md` : 134 | complete the other opcode families, actor-call/return, request-arming | **ANS** | BF-1 (71859306c): all 100 interpreter opcodes read; call/return and arming are on the actor-request page. Close with those links |
| OV-14 | same : 135 | the other wait kinds; non-empty external service behaviour | OPEN | wait kinds are partly on the interpreter page (REQWAIT kind 3); the rest is open |
| OV-15 | same : 136 | trace the control-byte producers and their native meaning | OPEN | specific; answerable statically |
| OV-16 | same : 137 | live scheduling, synchronisation, re-entrancy, allocation identity | RT | runtime/scope |
| OV-17 | same : 138 | bytecode, label and constant resource lifetime; authored input constraints | OPEN | specific |
| OV-18 | same : 139 | independent acceptance; L2 consequences | C2 | the carrier |
| OV-19 | `02-…/the-external-source-owner-and-borrowed-view-lifetime.md` : 189 | actual IO issuance/completion, outer recovery, callback single delivery | RT + OPEN | the IO timing is runtime; the recovery path is static |
| OV-20 | same : 190 | non-empty PRF/@FEF registration and specialised consumers | **ANS, pending** | answered by the untracked page `the-nonempty-prf-registration-and-specialized-relocation.md` once FRONTIER publishes it; related: `uq218-residue-fable` (a20f0a985) E/C on the `+0x44` ticket consumers |
| OV-21 | same : 191 | loaded-state reachability of rejection, bank exhaustion, competing owners | RT | runtime |
| OV-22 | same : 192 | full consumer scheduling/re-entrancy | OPEN | scope ruling (same as OV-2) |
| OV-23 | same : 193 | peer review; incorporation | C2 | the carrier |
| OV-24 | `02-…/the-resource-owner-from-copy-or-borrow-to-disposal.md` : 164 | whole-schedule/re-entrant safety, including specialised child walks | OPEN | scope ruling |
| OV-25 | same : 167 | the indexed owner's producer/error recovery; other external-owner families | OPEN, partly ANS pending | partly answered by the untracked pages `the-indexed-source-request-from-arm-to-terminal-pump.md` and `the-source-block-mover-and-separate-consumer-refresh.md` once published; "other families" stays open |
| OV-26 | same : 170 | authored format bounds, shipped alignment and index guarantees, allocation failure | OPEN | the data bounds are census-answerable |
| OV-27 | same : 171 | connect other text/widget/audio consumers only where proven | OPEN | a method constraint phrased as work; FRONTIER may rule it a limit |
| OV-28 | same : 172 | formal independent acceptance | C2 | the carrier |
| OV-29 | `16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md` : 171 | live asset IO/callback timing and cancellation | RT | runtime |
| OV-30 | same : 172 | repair and test the upstream receiver-census producer; revalidate declarations | C2 | tooling: `FABLE-CARRIER-TOOLING-AND-CHECKER-PROPOSALS-0926` (the existing batch-K tooling carrier) |
| OV-31 | same : 173 | remaining field/representation obligations; common-header integration | C2 | type-store work: `FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929` lists it for SWE2-STRUCT |
| OV-32 | same : 174 | independent review; type/system readiness | C2 | the carrier |

**Summary:**
- C2: 9 carrier items (OV-3, 9, 12, 18, 23, 28, 30, 31, 32), plus OV-5's acceptance half;
- ANS: 1 now (OV-13), plus 1–2 pending FRONTIER's publication of the untracked pages (OV-20, part of OV-25);
- RT: 5 (OV-8, 16, 21, 29, and OV-5's reachability half);
- OPEN: the rest.
- **Four OPEN rows duplicate each other in substance.** OV-4 and OV-6 ≈ OV-1; OV-7 and OV-22 ≈ OV-2. Linked as DUPLICATE, they
  count once.

## The 17 boxes on untracked `02` pages

These are `the-indexed-source-request-from-arm-to-terminal-pump.md` (6), `the-nonempty-prf-registration-and-specialized-relocation.md`
(6) and `the-source-block-mover-and-separate-consumer-refresh.md` (5). They are not classified here: the pages are not
committed, and their boxes can change before FRONTIER publishes them. The same classes apply at publication, in the same
commit.

## What FABLE files with this record

- The carrier task `FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929` (C2): an independent review for each overlay section named
  above, plus OV-31's type-store work.
- A request to FRONTIER: apply the rows and ticks (the register and carrier pages), rule the OPEN rows' scope, and publish the
  untracked pages.
