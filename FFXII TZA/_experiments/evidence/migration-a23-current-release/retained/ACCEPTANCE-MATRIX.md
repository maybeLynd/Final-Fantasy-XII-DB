# Migration acceptance matrix

Status of every item when this package was created: **NOT RUN**. This is a test specification, not evidence that the tests or migration pass.

Use existing test tools and project acceptance rules. OPUS owns engineering delivery; SOL derives and executes independent challenges for code it did not author. Other qualified non-authors review SOL-authored changes. FABLE validates knowledge/completion semantics, and a non-author reviews packages FABLE writes. FRONTIER proves deployment through the actual supported host paths. Mocked cases establish only the mocked boundary.

| ID | Required observation/test | Pass condition | Primary delivery / independent verification |
|---|---|---|---|
| A01 | Bootstrap on current canonical repository with active peers and dirty files | Brief revision/startup links recorded; live task/history/claims preserved; no forced global clean tree, duplicate identities or old-board replay | FRONTIER / SOL or audit lane |
| A02 | True and false package completion | Complete only after required final claims, canonical consumers and non-author receipts agree; sent review/DONE contribution alone cannot close parent | OPUS + FABLE / non-author semantic reviewer |
| A03 | Producer failure, malformed/missing prerequisite, timeout and valid baseline | Actual downstream path propagates required failures and passes valid input; no suppressed exit converted to scientific PASS | Implementing owner / SOL or other non-author |
| A04 | Same-count result edit; missing case; new cumulative run | Old cited receipt remains unchanged and valid; altered run receives new identity; mismatched evidence cannot gain execution credit | ORACLE / SOL or AUDIT-SEM |
| A05 | Config, parser, protocol, file-set and late-page changes | Every consumed relevant input invalidates dependent view; unchanged inputs skip correctly; binary fingerprints remain exact | DATA + OPUS / SOL |
| A06 | Missing, zero-byte, nonempty malformed and legitimately empty required source | Distinct validated states; unavailable/corrupt cannot become zero CURRENT or PASS; accepted empty state follows explicit schema/provenance | DATA + OPUS / SOL |
| A07 | Tamper machine snapshot, Markdown, crosswalk or output membership | All semantic outputs are bound to one generation and mismatch is rejected, without circular self-hashing | DATA + OPUS / SOL |
| A08 | Edit source between build and cutover; fail second output; crash mid-publication | Old complete generation survives, new partial is not current, failure status is separate, success history records only a committed generation | DATA + OPUS / SOL |
| A09 | Refresh during supported ZIP export; inspect raw manual mixed ZIP | Supported export freezes/verifies one generation and declared inputs; inconsistent raw ZIP is detected and labelled, not certified | FRONTIER + DATA / SOL |
| A10 | Page-only required question, carried residue, duplicate alias, legitimate reopen | Route lists stable locators/owners/next action; required debt stays visible after transfer; duplicates do not inflate totals; reopens invalidate affected completion | DATA + FABLE / non-author reviewer |
| A11 | All 52 scoped systems MET but required unresolved item remains elsewhere | Full database goal remains NOT_MET; schema labels or a shortened register cannot hide it | OPUS + completion owner / FABLE or independent audit lane |
| A12 | Historical audit files, declared counters, valid/invalid terminal receipts | Only the actual governing revision-bound sequence counts; no source heading, self-written counter or old partial audit awards terminal acceptance | Existing gate owner / independent audit lane |
| A13 | Stale checkpoint note, concurrent writers, removed legacy lock, legitimate update | Actual supported writer/caller preserves journal/lineage; bypass path is removed or prevented; no stale overwrite; failure tests use isolated state | FRONTIER + writer owner / SOL |
| A14 | Duplicate wakeup, capped owner, stale ownership, user cancel and recovery | One authorized owner/session; no quota evasion; idempotent task transition; cancellation prevents relaunch; safe current-state handoff | FRONTIER / SOL |
| A15 | Real host continuation, compaction/pause and successor boundary | Exact installed interfaces exercised; meaningful work resumes where supported, NOT_MET survives a session limit, no repeated veto storm; unsupported step stays unverified with precise manual boundary | FRONTIER + OPUS / SOL |
| A16 | Review rejection/repair/incorporation and next-task transition | One real package completes through existing records without user message relay; real or labelled synthetic defect is repaired and re-reviewed; next eligible task begins | Completion owner + FRONTIER / non-author reviewers |
| A17 | Dashboard data and navigation | Working local read-only interface, not screenshot mockup; all game-category tabs and actual VBF taxonomy accounted for; drill-down leads to real source/evidence and unresolved items | DATA / FABLE for meanings, SOL for implementation |
| A18 | Coverage accounting | Versioned population; unique range totals; held/unknown regions visible; citation != semantic proof; one executed branch != all branches; original source lines not fabricated | Coverage adapter owner / OPUS or qualified non-author |
| A19 | Live updates, no-change skip, source failure, application restart and offline export | Actual event/timer receipts show operating path; last-success/freshness visible; no LLM polling; failed source is not zero; portable summary verifies from supplied inputs | FRONTIER + DATA / SOL |
| A20 | Tool lesson adoption and parked runtime attempt | New producer uses corrected adapter via actual invocation; relevant wrong case rejected; spent setup budget survives session/task change and unchanged denied attempt is not repeated | Tool owner + ASTRA / non-author reviewer |
| A21 | Evidence-rich technical pilot and recognizable gameplay specification pilot | Connected readable specifications, exact limits, known downstream consequences and required acceptance; no new L3 engine required and no broader scope erased | FABLE + package owners / independent auditors |
| A22 | Fresh-agent sufficiency and ongoing adaptation | Fresh context finds accepted spec, inputs, dependencies and test method from database alone; instruction adoption verified; useful next task chosen without new user goal | FRONTIER + package owners / non-author reviewer |
| A23 | Release and rollback | Deployed source/tool versions, dashboard launch, matching portable snapshot, tests and independent receipts delivered; rollback changes feature code/config, never accepted research history | OPUS + FRONTIER / SOL and relevant auditors |

## Recording results

For each item retain the actual implementation commit and content hashes; test/driver revision; relevant input/environment identities; observed outputs and status; limitation; reviewer identity and independence; and the consumer or deployment entry point exercised. Use existing receipt storage, not another parallel acceptance database.

States: NOT_RUN, PASS at stated scope, FAIL, BLOCKED, or UNSUPPORTED/UNMEASURED as applicable. A dependency absent from an export is not equivalent to a broken host, and neither is it evidence of PASS. Reuse prior verified results only when their scope and relevant dependencies match.

**Passing this matrix accepts the workflow migration, not the entire FF12 database.** Full database acceptance remains governed by the existing L1+L2 requirements and terminal protocol. After M5 the agents continue that work without asking for a routine new prompt.
