# SWE2-STRUCT — inbox and handoff

**Structure and layout recovery.** Field offsets, widths, lifetimes, and the readers and writers that prove them. One of the eleven fixed production identities (2026-09-13 migration; the
generic `SWE2` became `SWE2-CONTRACT` and seven lanes were added beside it). The board, the claim
rules and every existing record are unchanged.

## Start here

1. **Read [`TEAM.md`](TEAM.md) first**, and treat it — not a session summary — as the operating
   record. It carries the completion rule, the live-game authorization and the EC-7 ownership split.
2. **[`REVIEW-POLICY.md`](REVIEW-POLICY.md)** defines the tier this lane's packages are reviewed at
   and who audits them.
3. **[`../EVIDENCE-STANDARD.md`](../EVIDENCE-STANDARD.md)** is binding. The amendments at the end are
   the expensive lessons; two bite offline work hardest — **a zero is a property of the filter until
   a positive control says otherwise**, and **a value inside a code range is not a pointer**.
4. **Claim before writing**, through `team.py` transactions only:
   `python team.py apply --agent SWE2-STRUCT --file op.json`. Never edit `TEAM.json` by hand.
5. **Commit explicit reviewed paths** with `publish_paths.sh <message-file> <path> …`. It refuses a
   directory argument on purpose: `git add` on a directory stages every changed file under it,
   including a peer's.

## What this lane is for

A field row is a claim about **both** ends. An offset with a writer and no reader is half a fact. Widths come from the instruction that moves the bytes, not from what the value looks like; where a census and a citation disagree on width and the disagreement is intended, the row carries `WIDTH DELIBERATE` and says why. `types_index.py --store <p> --validate` must pass before publication, and undeclared gaps are reported rather than hidden.

## Review

**Default auditor: `SWE2-AUDIT-SPEC`.** T1 packages need producer self-falsification plus that
auditor; T2 — family claims, ABI or type ownership, contract definition, a universal or negative
claim, or bulk EC-7 — additionally need FABLE or OPUS adjudication; T3 runtime-dependent questions
are prepared as an exact question and routed to ASTRA. See [`REVIEW-POLICY.md`](REVIEW-POLICY.md).

**While awaiting review, take separate non-dependent work.** A package in review is not a reason to
idle, and it is not a reason to start something that depends on its outcome.


## Two standing limits

- **A stub is not proof of its native effects.** Disclose injected state, stubs and entry
  boundaries; omitted initialisation, scheduling and effects stay open.
- **Agreement between a reconstruction and its own fixture is not evidence.** The control has to
  come from the shipping image or from the documents, never from recollection.

## Resume

**LATEST 2026-10-01 (DD batch 21, SWE2-STRUCT for OPUS):** board task `SWE2STRUCT-DD-B21-1001` added (rev 44403), claimed (44404) and
finished (44434). Record `_index/candidates/swe2struct-ddres-b21-1001/` (README, `b21_checks.py` 78 PASS
FAILS 0, `documented_rule.out` READY + READY-WITH-POINTER). Page edits are UNCOMMITTED for OPUS to publish:
`12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md` (5 notes) and
`05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` (8 notes), both pure CRLF, additive only
(edit script `Database/Tools/work/SWE2-STRUCT/b21/apply_b21.py`, idempotent). Proposed for OPUS: one runtime
row P1 (L-13 live-only residue, no carrier) and both status lines. Owned dirty paths: those two pages and the
record directory, until OPUS publishes. Current claims: none ACTIVE. NEXT: none queued for this lane; fallback
as below.

**2026-09-29 - RUN BY OPUS's CLAUDE SUBAGENT UNDER THE SWE2-STRUCT IDENTITY** (session
`OPUS-claude-struct-0929`; OPUS temporarily covering four Devin/SWE2 lanes through Claude
subagents; not a new identity).

UPDATE 2026-09-29 (later the same session): the register was clean, so the OV-31 row (ANSWERED, named residue)
and the page box annotation were published together as c1254ee2e (PUB `SWE2-STRUCT-PUB-OV31-REG-0929`).
`FRONTIER-REQ-SWE2-STRUCT-OV31-TYPE-STORE` is finished with dcdd159f0, 448d82b7e and c1254ee2e. The register
items under "OPEN / NEXT ACTION" below are therefore DONE. What stays open for this lane:
- the SWE2-AUDIT-SPEC review;
- the P3 `FRONTIER-REQ-SWE2-STRUCT-PASS22-DEBT` (not started).

LATEST TASK: `FRONTIER-REQ-SWE2-STRUCT-OV31-TYPE-STORE` (P2), the type-store work for the title-asset
widget `WidgetSingleton02AEE4C0`. Record:
`_index/candidates/ov31-title-asset-type-store-0929/` (README, `ov31_title_asset.py` with checks S P J X
C O K all PASS and self-test fires, and the idempotent `apply_ov31.py` / `unapply_reg_ov31.py`).

- `dcdd159f0` (PUB `SWE2-STRUCT-PUB-OV31-0929`, DONE) published the `_types` rows. Changes:
  - allocation `HEAP` -> `MIXED` (pool first, heap fallback at `00244FB2`);
  - ctor: attach to UI root `*(0208EA28)`, and the default stub `005C5230`;
  - dtor: external release via `00244F00` from `00394400` (the `00582860` msg-18 arm) and `00394130`
    (msg-18 arm), then `00245020` {18}, then `002482E0`;
  - `+0xC0` widths plus the script consumer `fsttl_initialize` (poll `00511EC0` -> `00394500`);
  - `+0xC4` retyped `u8[4]`: still unread, bounded, with a positive control;
  - `+0xC8`/`+0xD0`: both ends enumerated.
- `448d82b7e` (PUB `SWE2-STRUCT-PUB-OV31-PAGE-0929`, DONE) published page section 8 without the box flip.

OPEN / NEXT ACTION:

- THE REGISTER ROW AND THE BOX ARE NOT YET PUBLISHED. At publication time `_index/OPEN-QUESTIONS.md` carried a peer's
  unpublished UQ-206 edit (the SWE2-DATA lane; board `OPUS-REQ-DATA-UQ206-RELEASE-LABEL` is READY and
  unclaimed). My OV-31 cell was withdrawn from the worktree (`unapply_reg_ov31.py`), so a peer's
  whole-file publish cannot sweep it in. At 19:22 the register was clean again, so the flip is unblocked
  and is the very next action.
- Next, once `git diff -- _index/OPEN-QUESTIONS.md` is empty:
  1. add and claim a PUB task with `@publication` plus the page and the register;
  2. run `python apply_ov31.py` (it flips the box and writes the ANSWERED row);
  3. run `check_questions`, and require "questions consistent";
  4. publish both paths;
  5. re-claim the BLOCKED FRONTIER-REQ task and finish it with result_refs for dcdd159f0, 448d82b7e and the register commit.
- `FRONTIER-REQ-SWE2-STRUCT-OV31-TYPE-STORE` is BLOCKED (rev 40605) for that reason only, with resume_when set to that condition.
- Review filed to SWE2-AUDIT-SPEC: `SWE2-STRUCT-REQ-AUDITSPEC-REVIEW-OV31-TYPE-STORE-0929` (commit 448d82b7e, record the candidate README) (never route it to SWE2-AUDIT-SEM, which OPUS operates).
- `FRONTIER-REQ-SWE2-STRUCT-PASS22-DEBT` (P3) was NOT started. Getting its per-pair edge lists needs an
  `audit_crossrefs.py --json` run, which regenerates the shared `pass22-tripwires.tsv`. Do not run it
  unless that file is restored afterwards.

Current claims: none ACTIVE after this handoff publish (the FRONTIER-REQ task is BLOCKED). Owned dirty paths: none. The box and register edits are re-applied by `apply_ov31.py`, never left in the worktree.
Board lock contention was heavy on 2026-09-29 (about 15 min per `team.py apply`). Retry loops must not
stack.

State as of 2026-09-21 (board rev ~25114): working tree validates
470/4323/0/0; committed store carries the landed OPUS Phyre package
(~471 types) and still fails the union check until my staged fields.tsv
edits publish. FIVE OPUS REQs processed this pass, all edits STAGED in
the working tree - _types/{fields,types}.tsv + README carry ~420 lines
of parked peer rows, so they cannot publish without sweeping them; all
five tasks stay ACTIVE until the peer's publish frees the files:

1. PTR-ROUTE: removed ` | PTR 0x022C7CD0` from RenderModelInstanceContainer's
   route - the slot is a RenderResourceRoot field (modelInstanceContainerSlot
   +0xDA0, PROVEN) and gen_ptr_census seeds on rip-relative refs that the row
   itself records as zero. Route is now EMBED +0xF0 | STATIC 0x022C7020.
2. TYPE-NAME: ManagerSub0209AC30_00C0 -> ManagerSub0209AC60_02F8_00C0
   (0209AC30 is a pointer cell; 0209AC60 is the static manager; the peer's
   in-flight route correction already settled CHAIN _02F8 +0xC0).
3. ONE-ARRAY-TWO-TYPES: folded VmResultEntry into ActorWaitSlot - same
   CHAIN ActorStorageRecord +0xA8 stride=0x28; ActorWaitSlot is the richer
   authoritative map; CONTRACT already declares VmResultEntry a retired alias.
4. CANNOT-DECLARE-A-UNION: OVERLAY marker mechanism - the overlapping row's
   meaning opens with `OVERLAY ` naming the overlaid arm + tag; types_index.py
   honors it (unmarked overlaps still error). Worked instance:
   EncodedIdQueryRecord id +0x06 overlays rowIndex +0x04 (tag classId +0x00).
   types_index.py publishable alone (diff is mine only).
5. NO-SPELLING-FOR-A-KNOWN-WIDTH-VARIANT-SLOT: ruling documented in README
   OVERLAY section - distinct arms get OVERLAY rows with real ctypes;
   one-field-varying-meaning keeps the fact in the meaning cell; UNRESOLVED
   was a hold for the missing mechanism. Worked instance: BattleStatsRecord
   +0x088 gambitBlockByKind split into gambitBlockParty (GambitConfig) +
   gambitBlockSpawned (u8[52], OVERLAY, tag kindByte +0x05).

UPDATE 2026-09-21, board rev ~25222: THE INTERLEAVE RESOLVED. OPUS filed
OPUS-REQ-STRUCT-OUR-UNCOMMITTED-WORK-IS-INTERLEAVED-IN-THE-SAME-TSVS
offering either-direction wholesale publish; I took it - 2bc46df59
committed all three _types files carrying BOTH staged sets (message
itemizes each; PUBLISH_ALLOW_FOREIGN_HEADERS=1 covered their three
README headings; my OVERLAY heading carries my id). All five REQs +
the interleave REQ are DONE. Committed store: 472/4342/0/0 - the union
error is resolved.

THEN: OPUS-REQ-STRUCT-TWO-HEADER-ROWS-DUPLICATE-REGISTERED-CLASSES
adjudicated - registered class names canonical. Verified: ILH pair
9/9 identical; PhyreClusterHeader = base 18 + D3D11's 3 flattened.
Merged 30 evidence-rich Phyre* field rows into canonical rows
(meaning+evidence unions, TYPE RESOLVED/PROVEN), retired both Phyre*
types with ALIAS notes preserving file-format provenance. PUBLISHED
1bccaddbf. CONTRACT-phyre-cluster-header.md pointer fix parked behind
a peer's EC7-117 section in the same file - leaves with their publish.

THEN: FABLE-REQ-STRUCT-IS-THE-26-SENDER-SELF-THE-RECEIVER-0XD8-RECORD
answered YES at instance level (DONE, rev 25330). Element->+0xD8 IS the
002D14E0-built 0x150 grid widget: filler 0029F930 stores it at
elemRecord+0x18 (0x29F9B6), 00564010 binds element+0xD8 to it mutually,
and the senders' self is the same widget via child+0x10=parent
(0x2D1493, link at 0x248267). Message 26 is a real layout handshake:
element writes its grid origin into its own grid widget's +0x114/+0x116;
the widget's 002D1420 child drives the senders that read it back.

THEN: RenderResourceEntryBank containment RESOLVED, PUBLISHED
c3080eb5c. The bare 0x60 descriptor at render root +0x00 is also the
+0x00 prefix of RenderStrideC0Bank (root +0x60) and
RenderModelInstanceContainer (root +0xF0) - the row's own evidence
already called it THE BARE SHARED DESCRIPTOR and routed the expression
decision. Answer: two EMBED route alternatives on the bank row +
instance cell + evidence note. The containers KEEP their tiled rows -
~30 carry instance-specific evidence. check_duplicate_declarations: 0
unexplained. Published via surgical private-index commit (patched
types.tsv line only - peer's parked ArenaBlockHeader/NavRunStateBlock/
GlyphRunWidget1498 rows untouched); CONTRACT pointer fix and this
resume rode the same commit.

FABLE RULED on SWE2-STRUCT-REQ-FABLE-A-B-PREFIXED-NAMES (rev ~25340):
ARTICLE, not convention - measured: 2 of 32 f32[4] carry a, 5 of 442
u8 carry b; a local habit on two types, and aPathInitByte14 is a u8
which breaks a=array on its own example. APPLIED + PUBLISHED
b3c41a2e4 (surgical, four cells only): afPersistedWorldPosition,
candidateStateSecondary, pathInitByte14; plus the fourth flagged name
countedSubstructRef -> countPrefixedSubstructRef (verb-initial
participle; no live doc citations). check_name_artifacts: 0 findings -
first time fully clean. b* names stay (FABLE explicitly did not rule;
internally consistent, doc-cited). Doc-side follow filed to FABLE at
rev 25390 (spawn-placement-and-retirement.md + field-map cite the old
spelling). check_nowriter_claims green (eaf7bd29e). AUDIT-LOG still
carries parked peer sections - no local appends.

THEN: OPUS-REQ-STRUCT-SHOULD-30-AUTHORED-TABLES-GET-SIZED-SHELLS ruled
YES-with-condition (DONE, rev ~25443; convention published 5686d3224
in _types/README.md 'Sized shells for proven authored extents').
Declare a sized shell where the extent is closed arithmetically
(file size == header + count*stride, or the registry descriptor's
measured product): DISCOVERED / extent-PROVEN, unobservedSpan interior,
DYNAMIC route via registry slot or file+index, name from the bound
file/registry identity. Where arithmetic does not close: UNRESOLVED +
lower bound (EquipmentDefinitionRecord precedent). Contested counts
inherited, not smoothed. The three precedents already in the store:
LicenseNodeRecord (shell), StatusDefinitionRecord (measured stride),
EquipmentDefinitionRecord (lower bound). OPUS executes the ~30
declarations.

THEN (post-sweep over peer landings, rev ~25480): four gate findings
audited. (a) check_name_coordinates 10 rows on ManagerSub0209BE80_* -
ALREADY ADJUDICATED by OPUS (names carry parent coords deliberately;
rename would dangle cross-lane citations; documented in-row). (b)
check_embed_parent_fields -16 delta on MapScreenContainer
pageSlots01B0 - FIXED: declared MapScreenPageSlot (0xBC10 = page
0xBC08 + 8B unestablished tail), re-ctyped the row, re-parented
MapScreenPage's route to EMBED slot +0x00 (hierarchical, kills a
double-claim check_storage_class caught mid-edit). Gates green:
252/252 ctype agreement, 0 storage hard failures. STAGED pending
@publication (surgical patch prepared, /tmp equiv $TEMP/surgical_slot.sh).
(c) check_route_collisions ActorRecordPool SLOTPTR vs ActorManagerSlot
ARRAY - NOT a defect: pool_i = *(slot_i + 0x08), the recordPool field;
first SPARSE SLOTPTR trips the checker's documented N*S span model.
Filed SWE2-STRUCT-REQ-OPUS-SPARSE-SLOTPTR-SPAN-MODEL (rev 25544) -
cell-granular spans vs adjudicated overlap is OPUS's call (their row,
their checker's deliberate model). (d) check_surface_figures -
COVERAGE-DIMENSIONS.md 4 stale cells refreshed to authoritative
(4505/4502, GAME 155, engine 334, GAME fields 3348, offsets 1793 +
prose twin); doc's dated ### subsections preserved (regen alone would
destroy them - generator emits only the numbered skeleton). Staged
pending @publication. BOTH PUBLISHED: MapScreenPageSlot fix 3dba1a71e
(surgical private-index, 4 field lines + 3 type lines exactly),
coverage refresh 4609c3534.

THEN (rev ~25610): OPUS-NOTE-FIELDS-TSV-CARRIES-A-SWE2STRUCT-ROW asked
whether the uncommitted MapScreenContainer row was mine to land or
theirs to sweep. ANSWERED: nothing uncommitted - the row was already
in HEAD via 3dba1a71e. What their diff caught was the stale-index
phantom: surgical private-index commits never update the repository
index, so index-based diffs (git status, git diff with no HEAD) show
committed content as uncommitted. Repair applied at the source:
`git read-tree HEAD` re-synced the index - 27 remaining status
entries are honest worktree-vs-HEAD parked-peer diffs. Checkpointed
the answer + the diff-against-HEAD caveat to the NOTE (OPUS closes).

THEN (rev ~25639, same pass): sweep over the new landings (store now
490/4523). initDwordAA44 on ManagerSub0209BE80_A0D0 +0x974 is one of
OPUS's twelve adjudicated stay-red coordinate names (in-row ruling).
NEW finding: check_duplicate_declarations UNEXPLAINED pair -
PPhysicsTaperedCapsule vs PPhysicsTaperedCylinder, identical 4-field
maps, both 0x88 SIGNATURE RESOLVED (b3ffc2b5c, OPUS's). Filed
SWE2-STRUCT-REQ-OPUS-PPHYSICS-TAPERED-DUPLICATE (rev 25639): base
class relation via baseClass_ if RTTI says so, else recorded
sibling-identity ruling. Coverage cells refreshed again (GAME 156,
GAME fields 3354, recorded/named 4523/4520) pending publish.
ManagerSingleton0209BE80 census note is MOOT - peer landed
manager-singleton-0209be80-accesses.tsv + all 8 sub-object censuses.

THEN (rev ~25688): all three returns consumed. SLOTPTR REQ - OPUS
agreed on all three points, FIXED the checker (43d04ddf3): span is
now cell-granular, verified by positive containment (every cell must
land on a declared pointer field), nine-case control shipped;
check_route_collisions 0 partial overlaps, prints the containment as
verified. The row was never wrong. PPHYSICS-TAPERED REQ - genuinely
sibling registrations (distinct descriptors, shared PPhysicsShape
parent; identical schema is a fact of the tapered variants, and the
CapsuleBase/CylinderBase contrast proves shared parent != forced
shared schema). Ruling recorded in-row; pair now EXPLAINED. FABLE's
return carried a real correction: aCandidate_state_secondary snake_case
spellings existed that my camelCase-keyed sweep missed - and any doc
spelling that matches no store name is invisible to
check_field_citations. Offset-keyed sweep run over all four renames:
two residue hits fixed (battle-record-kind-byte.md +0x60 cite,
_types/README route-verb table), published c621b886c; the remaining
aAfCurrentNavigationPosition in spawn-placement is a non-store
locomotion field, not one of my renames. NOTE closed (answer was
checkpoint). Store green: 490/4523/0/0, collisions 0, duplicates 0
unexplained, name-artifacts 0, surface figures agree.

THEN (rev ~26840): OPUS-NOTICE-...-MOVEMENTCONTEXT-0X5C - the strided
attribution OVERTURNED at +0x50's W lane, ACCEPTED after verifying
all three anchors on the image (0025BE63 rbx=[rdx+0xB8] reads +0x50
movss AND +0x5C/+0x5D bytes in one body; ctor byte-1 at 0026647C,
mask-0xF8 at 002663BA; dword bounded 0x0000XX01 = always denormal,
the 003DA6ED addss inert). My settlement's load-bearing claim (real
access, not misattribution) survives; the 'five distinct 16B fields'
frame and the OTHER-context mechanism do not - the read is on THIS
type's own +0x50 W lane. Corrected: +0x5C row carries the acceptance,
all 8 census annotations rewritten (quad frame survives at
+0x10/+0x30/+0x40/+0x70; +0x60 X-lane kind1SlotMask-as-movss flagged
as parallel, unadjudicated, OPUS's to scope). Published 67cd03aed.
Store now 517/4718 after heavy peer landings, still 0/0.

THEN (rev ~28695, board clear): sweep over ~1800 revs of peer work
(store now 592 types / 7257 fields). Findings: (a) two ANCHOR hard
failures in check_storage_class - ManagerSub8FA0SlotRecord02B8 and
HelpMessageWidget0500 spelled their routes `ARRAY <Type>+0xOFF`,
a form the grammar does not have; converted to
`EMBED ManagerSub0209BE80_8FA0 +0xAC0`/`+0xC0` with the same stride/count -
semantics identical, parent fields (helpMessageRing, slotRecords0AC0)
corroborate the extents to the byte. Hard failures 0. (b)
check_duplicate_declarations UNEXPLAINED pair LuaCClosure contained
in LuaLClosure - shared ClosureHeader prefix, diverges at +0x18;
filed SWE2-STRUCT-REQ-OPUS-LUA-CLOSURE-HEADER-PAIR (rev 28691):
declare LuaClosureHeader + baseClass_ rows, or record a sibling
ruling. (c) TYPE-COVERAGE.md regenerated wholesale (it is pure
generated content - the numbered-skeleton hazard applies only to
COVERAGE-DIMENSIONS); COVERAGE-DIMENSIONS four cells refreshed
(257/335/7257-7254/5896). Published a1d609537. The
check_census_widths 'ALL evidence dropped' lines on
SpawnRecord/BattleMenuPanelWidget3010 are the documented SIMD-rule
cost - unchecked rows, not failures; no action.

THEN (rev ~28844): the kind1SlotMask parallel I had flagged for
OPUS turned out to resolve on the row's own evidence without
waiting - the kind-union was already declared: kind 1 keeps a
party-slot mask bounded 1<<index (always denormal, so the
003DA7C1 movss addend is inert - the CON-143 shape), kind 3 has
the lane block-copied from a +0x50-style float pair (the read is
real there). Appended the disposition to the +0x060 row, published
f4b086c42. No correction needed - unlike +0x50, nothing reads +0x60
as byte and float in one body.

Since the five-item package (f66c93d66) and the two peer-type gap
closures (7038a0d67, 32f65cf9b):

- 34a7fb7fd: MessageWindowRecord's freshly declared spans already contained
  the record's own dispatcher fields - 002A6190's case arms touch +0x38/
  +0x7C/+0x9A/+0x9C/+0x9E/+0xB4/+0x1A8/+0x3B8/+0x3BB/+0x3C4/+0x3E8/+0x3F0;
  six spans split into 24 rows.
- 0db0fa967: new sweep axis - offsets cited in types.tsv evidence cells vs
  declared spans. Six real declarations after auditing 34 hits: MWR
  dispatchProc +0x00, AMS resolvedUnitPtr +0x30, NBE subResourceIdB/C
  +0x34/+0x38, CRO embeddedDestroyedSubObject3E0 (0x40 extent floor), SDR
  blockingStatusMask + four armCopiedBytes, BootSingleton
  cameraOverrideFov/Aspect/Scale (UQ-12). Rejected on the binary: +0xC0C
  and +0xC10..+0xC18 live on OTHER objects ([01F81428], the console's
  camera) - not on the singleton.

FIVE-ITEM CLAIMED PACKAGE CLOSED (commit f66c93d66):

1. FABLE-NOTICE-MOVCTX-RADIUS-BAND - VERIFIED on the binary and applied:
   +0x50/+0x54 = scaledRadiusW/D (kind-2 scaled-out of 003DA860, feeds
   movement-body +0xF0/+0xF4 radii via 00268380; kind-1 alternates: talkang
   angle at +0x50, wrapped-angle pair at +0x54/+0x58 - per-kind union),
   +0x80/+0x84 = defaultRadiusW/D (unscaled-out), +0xFC = meanScaledRadius
   (floor is 0.01 not 0.05 - 008F30E4 low dword 3C23D70A, FABLE's correction
   confirmed), +0x70 = meanScaledRadiusOrScaledBX (kind-1 mean lane),
   +0x58 = pairedAngle58.
2. SECONDARYCONTEXT-IS-A-SIX-ELEMENT-ARRAY - declared SecondaryContextElement
   (0x30, 15 member rows factored from the flat element-0 rows);
   SecondaryContext.elements = SecondaryContextElement[6] at +0x00; tail
   +0x120+ preserved. Types 260->261, fields 2724->2651.
3. NAME-ARTIFACTS-SEVENTEEN - the 13 repeats dissolved with the flat rows;
   check_name_artifacts now reports exactly the 4 heuristic false positives
   (aAfPersistedWorldPosition, aCandidateStateSecondary, aPathInitByte14 are
   GFZ-derived names; countedSubstructRef is a participle misread as verb).
   No renames.
4. PRESENTATION-CONTAINER-SIZE-IS-A-HEADER - ruled for the full footprint:
   size 0x30->0xC30 with nodes = PresentationEntryReferenceNode[64] at +0x30.
   check_storage_class: 0 hard failures (was the store's one containment
   failure).
5. 32C4-BITMAP-EXTENT - already resolved by OPUS's b2e8cc2e9 (achievement
   StateBitmapA = 8 bytes, two-sided bound: callers reach 5, next array caps
   at 8). Verified and closed.

Gates: validator 0 errors/0 gaps, surface figures agree, census-width 0
disagreements, storage-class 0 hard failures, name-artifacts 4 (documented
false positives), name-reservations 0 violations.

Next action (rev ~28893): BLIND-CENSUS PACKAGE COMPLETE, published
this pass. check_census_writers went 16 blind entries across 13
types to ZERO - every declared constructor now appears in its own
census. What it took: a base-tracking scanner
(%TEMP%\ctor_base_scan.py - mid-function base adoption, lea/add
bias, pointer-field-derived bases, rep stos, negative stack bias)
because the blind bodies adopt their receiver from a computed load,
which argument-seeded tools cannot see; plus
%TEMP%\emit_ctor_rows.py for row emission. 187 census rows appended
across 11 files. THE ACTOR CLUSTER WAS INVERTED: 00266530's six
'record +0x138..+0x152' writes go through rax=[rbx+0xC0] =
SecondaryContext, not MovementContext - the real context/steering
initialiser is 00265FF0 (119 context rows, 31 steering rows, plants
+F0=slot0); 00266AD0 only plants record pointer slots. types.tsv
ctor cells corrected: MovementContext->00265FF0, SecondaryContext->
00266530, SteeringRecord->00265FF0, BattleSystemState->002370C0
(002342F0 only orchestrates), SpawnRecord->none (alloc-only, read-
verified; EXPECTED_ABSENCE filed for 00236957), SavePayload->none
(002EF5F0 is a bulk memset; measurement moved to evidence). Two
WIDTH DELIBERATE markers added (initDword28, initByte106) - the
ctor's qword/word zeroing stores were always wider than the fields.
Checker gained mappings for actor-manager-slot(-entry) censuses.
Pitfall learned: python open(w) writes CRLF on Windows and breaks
newline='' readers (route\r KeyError) - write bytes or newline=''.
Pending: Lua closure-header REQ still OPUS's. Fallback: re-run the
structural sweep when peers land - coverage figures and
duplicate/span/collision/anchor findings are the recurring
residuals. When diffing shared TSVs, use HEAD as the base -
private-index publishes leave the repository index stale (repaired
once via git read-tree HEAD, rev ~25610; surgical publishes
afterwards re-create it - publish_paths.sh's private index never
touches .git/index).

THEN (rev ~28987): UNMAPPED-CENSUS PACKAGE COMPLETE, published
0c7b2497f. The writers checker's standing 43-file UNMAPPED list went
to zero: 42 mapped to their store type (filename convention, each
census's disp range verified against the declared extent first),
locomotion-angle-accesses.tsv mapped to None - no store type exists
for it and mapping it would be guessing. Every newly testable cell
was dispositioned by body-read, not by label: six REAL constructors
got rows (SpawnGroupLedger 00307090 - 12 rows, the 64x0x18 reset
unrolled four per iteration with rax=ledger+0x10;
InputBindingRecord 0015C0D0 - 12 rip rows, bank-B init;
FrameMarkerSingleton01F82C80 001D62D0 - 11 inline writes;
Widget 00244F50 - 3 pool-scan/acquire rows; GambitConfig 00328140 -
2 config reads + 1 addr; LegacyPs2GsTextureContext 002F6AB0 - 87
rows). Seven alloc/orchestrator sites filed EXPECTED_ABSENCE with
body-read reasons: 0028F8CF (writes only +0xAA44/+0x10F68, inside
other subs' spans), 00189034, 001BDA80, 0026E79E, 00210EC0 (malloc
thunk), 00477EE0 (arg-plumbing only), 00D10460 (the .rdata table
itself, not code). Five ctor cells reworded to prose where the
cited address sat inside a DOES-NOT-REACH/orchestrator statement:
ManagerSub0209BE80_00A0 (parent ctor measured: zero displacements
in +0xA0..+0x5380), BattleTargetBuffer, BattleTargetResultEntry,
SpawnKeepImage (bulk zero-fill, SavePayload precedent),
ImageBackedStateBlock. TRAP CAUGHT: my first emits for the ledger
and frame-marker files were drafted from the summary's abbreviated
instruction listing and did not match the bodies - always emit
census rows from disasm_fn output, never from memory. Gates: 0
blind, 0 unmapped, widths 0, storage 0, routes 0, validator
592/7257/0/0. NOTE: @publication was held by SWE2-EC7 when the
commit landed; the publish reservation task
SWE2-STRUCT-PUB-UNMAPPED-CENSUS stays READY and should be claimed+
finished once the lock frees. Pending: Lua closure-header REQ still
OPUS's. Fallback unchanged: re-run the structural sweep when peers
land.

THEN (rev ~29036): LUA POINTEE DECLARATIONS, published a448dfc7f.
The structural sweep's four dangling ctypes went to one. Three
types declared from MEASURED strides, no Lua-source reliance:
LuaLocVar 0x10 (LoadDebug 0082DCE0: shl r9,4 into luaM at
0082E103, published to LuaProto+0x30, fill loop steps 0x10 -
varname/+0x08 startpc/+0x0C endpc); LuaUpvaldesc 0x10
(LoadUpvalues 0082E790: shl r9,4 at 0082E7CB, published to +0x38,
bytes instack+0x08/idx+0x09, +0x0A..+0x0F padding); LuaNode 0x28
(hash accessor 0081F890: lea [idx+idx*4]*8 indexing + add/sub 0x28
chain walks - value TValue 16, key TValue 16, next ptr at +0x20;
node vector via luaM in resize body 0081F9B0, dummynode planted by
luaH_new). Routes CHAIN LuaProto +0x30/+0x38, CHAIN LuaTable +0x20
with measured strides and symbolic counts. LuaClosure stays
dangling BY INTENT - the C/L closure shared-header question is
SWE2-STRUCT-REQ-OPUS-LUA-CLOSURE-HEADER-PAIR, OPUS's ruling.
Coverage figures caught up (595 types / 7267 fields / 260 GAME).
Validator 595/7267/0/0, all gates green. TRAP CAUGHT: fields.tsv
had no trailing newline - the first appended row glued onto the
previous last line and the validator reported a phantom gap.
Always check the file ends with a newline before appending TSVs.
Next action: when OPUS rules the closure header, declare
LuaClosure (or rename the ctype) - that retires the last dangling
ctype and the last unexplained duplicate in one ruling. Fallback
unchanged.

THEN (rev ~29057): LCG SAME-BASE DUPLICATE FOLDED, published
d44de5467. LcgState022C256C (OPUS's 2026-09-21 types-MET
declaration) and SharedGameplayLcgState were two rows for one
four-byte static at 0x022C256C - same multiplier, same sites.
Canonical = SharedGameplayLcgState (semantic name, mapped census,
ctor cell, the three-step-draw contract). The folded row's unique
measurements moved into the canonical field's evidence: 17
references (8 reads / 9 writes, all 4-byte) and three
imul-immediate sites the canonical list lacked (00317FC1,
0031844A, 00318540 + writebacks 0031800C/00318496/0031858B), plus
the S-46/types-MET provenance. TYPE-COVERAGE per-type row removed;
figures caught up (594 types / 7266 fields / 259 GAME).

SWEEP STATE AFTER THE FOLD - what the advisory mass actually is:
the ~100-row check_instance_aliases overlap list is the PHYRE
DESCRIPTOR-ANCHOR class - instance cells name a class-descriptor
static while size carries the INSTANCE size from the ctor's r9d,
so the computed span is meaningless. Already routed and answered:
OPUS-REQ-FABLE-IS-AN-INSTANCE-ROUTE-KNOWABLE-FOR-ENGINE-BUILT-
PHYRE-OBJECTS (DONE). NOT actionable store debt - leave it. The
three alignment advisories verified correct-as-declared:
FieldRecord 0x3 is a packed stride-3 record (i*2+i addressing);
RenderResourceEntryBuffer 0x1C an embedded buffer header;
AppBootStatic01F7F480 0x124 a census-measured floor. Standing:
LuaClosure dangling ctype + LuaCClosure-in-LuaLClosure unexplained
duplicate - both resolve on OPUS's header ruling. Gates:
validator 594/7266/0/0, writers 0 blind/0 unmapped, widths 0,
storage 0 hard failures, surface figures agree.

THEN (rev ~29082): CLOSURE HEADER RESOLVED BY MEASUREMENT,
published de630e72a. The REQ's factual question answered itself:
both size expressions prove a fixed 0x20 outer frame (C:
(n+2)*16 at 0081ECA6-0081ECB4; L: n*8+0x20 at 0081ECE6) and the
kind member sits at +0x18 in BOTH (f / proto), so the shared
header is exactly +0x00..+0x17 = 0x18. Declared LuaClosure (0x18:
next/tt/marked/nupvalues/pad/gclist); both closures' six
duplicated header rows folded into baseClass_LuaClosure - the
store's own mechanism, same as the Phyre base/derived rows.
LuaCClosure +0x18 named f: OBSERVED - lua_pushcclosure 00810470
stores the fn pointer at 008104DE right after the luaF_newCclosure
call (the ctor itself writes only nupvalues at 0081ECC5). Result:
dangling ctypes 4->0, unexplained duplicates 1->0, LuaProto+0x40
cache ctype resolves. SWE2-STRUCT-REQ-OPUS-LUA-CLOSURE-HEADER-PAIR
stays READY on OPUS - the measurement is applied but the ruling
(their question, their veto) is theirs to close. Gates: validator
595/7262/0/0, all clean. LANE IS NOW EMPTY of live struct-lane
findings: 0 dangling ctypes, 0 unexplained duplicates, 0 blind or
unmapped censuses, 0 width disagreements. Remaining advisories are
all previously-dispositioned classes (Phyre descriptor anchors,
measured-floor alignments). Next action: a plain Continue should
re-run the sweep over new peer landings and then take the next
unblocked package - if none exists, the frontier work queues are
the fallback.

THEN (rev ~29242): TWO FIXES STAGED IN THE WORKTREE, PUBLISH
BLOCKED ON FABLE'S STALE @publication LEASE (~23h at 19:30Z
2026-09-23; FRONTIER already filed FRONTIER-REQ-OPUS-PUBLICATION-
LEASE-TIMEOUT-RULE and recorded 'lease stands, no takeover on
timestamp - the only present path is a user-side FABLE restart').
My changes sit uncommitted in the shared worktree:
1. EncodedIdQueryRecord.id +0x06 gained the OVERLAY marker over
   rowIndex's tail (tag: classId +0x00) - a peer's UNCOMMITTED
   SECTION-05 rewrite introduced the tagged-view overlap in prose
   but not the marker; the validator error is worktree-only and
   now cleared. CAUTION: fields.tsv also carries that peer's
   parked EncodedIdQueryRecord rewrite AND a WidgetSingleton02AEE4C0
   restructure (25->23 rows) - DO NOT publish fields.tsv as mine;
   whoever publishes it next carries all three changes.
2. ImageBackedStateBlock +0x3848: imageByte3848 + unobservedSpan3849
   merged into flagBitmap3848 u8[4] - check_array_heads was right:
   the indexed byte read (00315805, rcx=id>>3, id<0x1E) reaches
   +0x3848..+0x384B, and a setter RMWs it (00315B50: bts/btr by a
   flag arg at 00315C9A/00315C9F). A second bit-per-id bitmap beside
   firedBitmap at +0x3844; which flag (claimed/notified/seen) is
   NOT established.
Validator on the worktree: 596/7281/0/0.
Next action on resume: check whether the lease cleared; if a peer
already published fields.tsv, verify my two rows survived; else
wait - the lease rule is OPUS's to ratify.

THEN (same rev, lease still held ~24h): ALL FOUR
check_route_verb_against_image FINDINGS DISPOSITIONED BY BODY
READ - none are store defects.
1. BattleUnit SLOTPTR 022C1788 'CONTRADICTED' (lea=17/load=0) is a
   CHECKER FALSE POSITIVE: rip-relative addressing cannot encode an
   index register, so an indexed table can only ever be entered via
   lea base + [base+i*8] - lea=17 IS the mandatory indexed-table
   signature, and 00300230 mov [r15+rdi*8],rbp (rdi bound <4 at
   0030022A) stores BattleUnit* into it. SLOTPTR correct. The
   instrument's DEREF rule (needs a base-address load) is unsound
   for indexed tables; a checker fix is a possible future package.
2. ActorRecordPool SLOTPTR 02098E18 'untestable' is STRUCTURAL:
   02098E18 = ActorManagerSlot array base 02098E10 + 0x08 - a
   strided pointer field inside the 0x288-stride records; every
   access indexes off the array base (53 lea at 98E10), never the
   field address. Correct as declared.
3. ScriptNativeDispatchRecord ARRAY 01EED708 'untestable' CONFIRMED
   BY LAYOUT: the one nearby ref, lea rax,[01EED700] at 003DC2F0,
   publishes {count,records} - qword at 01EED700 = 0x5D8 = 1496 =
   declared count; records begin at +0x08 = declared base. Correct.
4. RenderModelInstanceContainer STATIC 022C7020 'untestable':
   zero rip-relative refs in +-0xA0; reached via the EMBED
   RenderResourceRoot +0xF0 primary route and the 0051F9F0
   subcontainer accessor's computed base. Secondary route only.
Store still 596/7281/0/0 on the worktree. Lane remains empty of
live findings; publish queued behind the FABLE lease.

THEN (rev ~29400): SURFACE FIGURES RESYNCED to the worktree store.
TYPE-COVERAGE.md regenerated via types_index.py --coverage (the
file's own instruction) - carries the five flagged rows plus
IndexedExternalSourceRequest (new peer type) and WidgetSingleton's
SIGNATURE RESOLVED upgrade. COVERAGE-DIMENSIONS.md hand-edited:
GAME 260->261, fields 7262/7259 -> 7281/7278, GAME-fields
5901->5920. TRAP RECORDED: program_coverage.py --out REGENERATES
ONLY ITS ~111 MEASURED LINES and silently drops ~400 lines of
appended prose sections (6a/6b OPUS essays, status tallies) - the
'Generated by' header is stale relative to the current generator.
Hand-edit COVERAGE-DIMENSIONS cells; never --out it. check_surface_
figures now reports agreement. Remaining advisories all
dispositioned classes: ItemClassDescriptor text-band (extent
doubly-proven), FieldRecord stride-3 (i*2+i addressing), three
'no bound evidence' counts, symbolic-count lower bounds.
FABLE lease still held (~24h, checkpoint-request unanswered);
publish queue unchanged.

THEN: check_width_blind_spans PACKAGE APPLIED (21 flagged spans ->
0 defects, staged in fields.tsv). The checker is right that each
row's REASON ('no censused access') was false - every span is
covered by a wider censused access - and right that coverage is no
licence to name a field. Three dispositions:
1. 18 rows: reason rewritten 'no censused access' -> 'no
   FIELD-LOCAL access - CARRIED by <instr> at <site>; carried, not
   read for its own sake'. All covering accesses are init/copy
   idioms (movups/movdqa/movsd block copies, packed qword stores)
   whose field boundary is narrower than the store width - the
   adjudication initDword28's row already carries ('a
   constructor's store width is not a field width').
2. LegacyPs2GsTextureContext +0x230 SPLIT, not reworded: the
   route-seeded ctor census (002F6AB0) holds DIRECT dword stores
   at +0x230 (mov dword,1 at 002F6EF3) and +0x234 (r14d at
   002F72C0) - field-local writes, declared as dword0230/dword0234
   DISCOVERED; residual unobservedSpan0238 u8[8]. The span row's
   own evidence shows why the fixpoint missed them: a PTR-seeded
   receiver closure cannot see ctor-internal writes.
3. Two rows already honest, left untouched: SpawnRecord
   unobservedSpan001A ('no access to any specific byte' is precise
   - a block copy is not one) and EvaluationContext
   unobservedTail02A (already discloses the qword clear).
The checker still lists the 20 covered rows - coverage is a fact,
not a verdict; the report is advisory by design.
Figures resynced: 596 types / 7283 fields / GAME 261 /
GAME-fields 5922 (TYPE-COVERAGE regenerated, DIMENSIONS cells
hand-edited). Validator 596/7283/0/0.

THEN: check_uninformative_widths PACKAGE DONE - the checker's 81
unevidenced-width rows: 72 already carried OPUS's 'WIDTH RESTS ON
NO INFORMATION' marker; the 14 new ones (incl. my own dword0234 -
r14d was zero there) got category-specific annotations (ZERO /
ALL-ONES / REPEATS/2 / UNDETERMINED wording). Advisory only - no
widths changed.

THEN: check_unread_vs_census PACKAGE APPLIED (33 flagged spans ->
9, all nine now disclosed classes). The route-seeded censuses see
inside spans the PTR-fixpoint could not. Declarations where the
census holds FIELD-LOCAL accesses:
- LegacyPs2GsTextureContext rebuilt +0x040..+0x224: qword0040
  (cmp-read + 2 leas), qword0128/0140, the +0x158..+0x170 block
  (2 qwords + 3 dwords), qword0180, qword0190/0198,
  qword01A8/01B0/01B8, qword01C8, recordArray01D0 (base of the
  stride-0xE0 array bounded by entryCount220), dword0220 ->
  entryCount220. THE BIG ONE: +0x1E0 is a 2-element array of
  0x18-byte slot-class banks - NEW TYPE LegacyPs2GsSlotClassBank
  {idBank void*, bitBank void*, pad u8[4], count u32}, walked
  rbx=+0x1E8 step 0x18 x2 by the alloc loop 002F722A-002F727C;
  descriptor bit14 selects the bank whose count incs (002F7016).
  bitmap0210 is a third standalone bitmap alloc'd 002F72A9.
- ManagerSub0209BE80_AB30: qword0010/0018/0028/0068, dword0070/
  0074 (the sub-pair), dword0078.
- ManagerSub0209BE80_00A0: qword52B0 (null-tested ptr, 5 acc).
- ManagerSub0209BE80_57E0: qword25A8/qword25B0 (projected through
  subAddr24B0 callee), nibbleLowRow26A7 + nibbleHighRow26AD u8[6]
  (the 6-iter loop at 003FA2A0 splits a summed byte's nibbles into
  two parallel rows), byte26B3. addrTaken26AE folded - its lea is
  the rows' walking cursor, not a datum. (OPUS's float4 arrays and
  ptr2690/2698 were already declared - untouched.)
- ManagerSub0209BE80_8FA0: qword1050.
- MessageWindowRecord: qword0010, word0044, qword0048, dword0080.
- ActorStorageRecord: channelWordCA/DA/E6 - band slots with their
  own movzx reads (00266530), matching the channelWord convention.
- RenderModelInstance: indexSlot1F8 i32 read by 00504758/00504D60
  out of the old padBlock1F0.
- CharacterRenderObject: floatBlock0088 float[32] - eight 16-byte
  movups lanes written through a +0x80 cursor in 001F4DA0.
Annotated-not-declared (address-taken or misfiled): the four
BattleMenuPanelWidget3010 element+0x10 spans (projected lea
rbx+0x28 over the stride-0x40 element array), CharacterRenderRecord
span06E4 (register lea eax,[rdx-1] - census misfile), the two
WidgetSingleton02B47758_0460 spans (leas), LegacyPs2Gs span00A8
(lea + carried qword-init). PendingCompletionQueue +0x20 already
disclosed its lea.
ALSO: LuaClosure allocation_site prefixed INTERIOR (its bytes are
the two closures' shared head) - storage-class advisory cleared.
check_array_heads ActorWaitSlot candidate is a FALSE POSITIVE:
[rax+r8*8+0xC] is rax=[rcx+0xA8] slot-array base, r8=index*5 ->
index*0x28 element addressing landing on the declared 'value'
field, not an inner 8-byte array.
Figures: 597 types / 7326 fields / GAME 262 / GAME-fields 5965;
validator 597/7326/0/0; surface figures agree. FABLE lease still
held; publish queue grows.
TAIL: two of the new rows (57E0 qword25A8, 8FA0 qword1050) were
themselves register-store-only widths - annotated WIDTH RESTS ON
NO INFORMATION. All 88 unevidenced rows now carry the marker.

UPDATE 2026-09-22 (check_span_access lane CLOSED): the instrument's
36-span ranking is fully dispositioned. ONE real find applied:
PDeferredLightingD3D11 +0x41D8 (6.37x enrichment, 85% coherent) -
the "unobserved" 344B tail above baseClass_PDeferredLightingBase is
the derived class's own region: releasedPointerBank41D8 void*[13]
(ctor 00645BC0 zeroes, dtor 00646600 passes each to teardown-helper
006505A0), qword4240/4248 (teardown helper 0065D310), qword4250/4258
(accessor 00650D40), namedLookupBank4260 void*[21] (member 006568D0
stores 22 string-name->object lookups at +0x4260..+0x4300), word4308
(ctor mov word,1), residual unobservedSpan430A u8[6] (only vp8-codec
collisions), qword4310/4318/4320/4328 (+0x4328 is the 22nd lookup).
Attribution proven by phyre-function-class-map NativeQualified rows
for ctor+dtor. Everything else on the list is a foreign-collision or
no-signal row, each now carrying a 'SPAN-ACCESS LEAD FOLLOWED' note:
ImageBackedStateBlock+0x386C was already dismissed by OPUS (disjoint
census); all 12 Manager0209AC60 spans share one rip-referrer that
never touches the bands; BootSingleton+0x0D19's in-band accesses ride
the object returned by trivial accessor 00796E20, not the singleton;
WidgetSingleton02CA99C0+0x0403's overlap fn writes sibling 02CA99B8;
EeVu0RegisterBank+0x0490's route-touching fn reaches the bank only
via rip at +0x000..+0x33C; the census-covered spans (BattleUnit,
PaneListWidget, BMCW, MSub7FB0, FrameMarker, SavePayload) have zero
census overlap. check_dangling_type_names had silently broken on the
store's CRLF worktree files - normalized both TSVs to LF (matches
eol=lf attr; FUTURE WRITES must use newline='\n' or bytes - python
text-mode writes produced the CRLF). Validator 597/7337/0/0; surface
figures agree (PDeferredLightingD3D11 row 2/2 -> 13/13). FABLE lease
still held; publish queue grows.

THEN (same rev, sweep continued): check_evidence_widths 4
CONTRADICTED -> 0 (24 stated exceptions), all adjudicated as
WIDTH DELIBERATE annotations rather than redeclarations:
ManagerSub8FA0SlotRecord02B8+0x280 u16 (byte cite = partial read of
bit0; word or/movzx establish the width), MapScreenPage+0x128 u16
(qword cite = packed 4-lane block write from a callee-built stack
qword, readers take per-lane), LuaTable+0xA u8 (word cite packs the
byte as low lane), LuaCallInfo+0x30 8B (w4 cite = the
continuation-arm union overlay already documented). Route
uniqueness: the two seedable shared routes (FN 0x2ED570+0:
RenderStrideC0Element/RenderResourceEntry; FN 0x2EF640+0x200:
PersistentFlagPayload/SavePayload) already carry restriction prose
on all four types - verified, no mutation.

THEN (same rev): check_cited_site_widths 5 DISAGREED -> 0. One real
find, four annotations. ManagerSub7EA0Entry SPLIT: its
unobservedTail0016's 'no access' claim was refuted by a cited site -
`cmp word ptr [rcx+0x16], ax` at 0028D513 is a real field-local read.
Attribution airtight: 0028C970 drives the 2-entry array
(`lea rcx,[rdi+0x30]; shl rax,5`, ebx 0..1) -> 0028D8A0 -> 0028D460
with rcx=rbx=entry, rdx=the 7EA0 region (parent census route-seeds
rdx at +0x70/+0x76). Declared word0010 i16 (movzx+movsx->cvtdq2ps),
byte0013 u8 (imul multiplier), word0016 u16 (equality vs word0010);
residuals unobservedSpan0000 u8[16], unobservedByte0012,
unobservedTail0018 u8[8]. The other four: ImageAddressHandleSlot
nextSlotIndex (w4 cite = arena-init packed store 0xffff0001 covering
two u16 lanes), LuaCallInfo nresults (w8 cite is on LUA_STATE -
rbx=L, +0x20 is L->ci, same-displacement collision), LuaNode
value/key (16B TValues read by halves, w8 cite = leading half).
Validator 597/7341/0/0; surface figures resynced (7341/7338,
GAME-fields 5969, ManagerSub7EA0Entry 3/3 -> 7/7).

THEN (2026-09-23): check_clear_exhaustion PACKAGE - 218 types with
unanswered spans -> 15 (all SKIPPED, no addresses in their columns,
instrument-blind by construction). 974 span rows annotated with the
LIFETIME token across 197 types, each verdict adjudicated by reading
the named site, NOT mass-trusting the candidate list:

- ZERO-INITIALISED (widget group, 78): 002465F0 = Widget ctor runs
  memset(this,0,size) at 00246626, size = declared extent per caller.
- TEMPLATE-INITIALISED (Phyre group, 79): NOT zero - PCluster::create
  0063A990 loops 0063C910 per element; 0063C974 memcpy's the
  descriptor's stored default image (desc+0xC0, len desc+0x38 = the
  element stride) over each element. New verdict wording; the checker's
  'CANDIDATE ZERO' label was a false lead here.
- ZERO per-type: A0D0 (parent memset), MapScreenMarkerNode0B0
  (00402B3A element memset 0xB0), ActorManagerSlot (00266EFC slot loop
  0x288), CharacterRenderRecord (0041F754 0x740), ActorStorageRecord
  (00267A8B whole block), EncodedIdQueryRecord (wrapper memsets
  0035D36A/0035D3BB 0x98), 57E0ArrayRecord (claim memset 003FA3A5 +
  helper 00333048), Manager0209AC60 (ctor col documents 002800F0
  memset 0xE00 - the checker's 00247CED cite clears FOREIGN static
  0208EAC0), NavGridParams (.bss at load; 0039267E clears the heap
  cell block it POINTS AT), ManagerSub5380PoolA/B/C (parent's 0x10FD0
  clear; A-entry's 003EFD82 memset is a 0x20 SPACE-FILL, claim-time),
  ManagerSub7EA0Entry byte0012 (parent clear), BattleResultRecord
  (CALLER stack - each caller memsets the 0x148 scratch).
- UNDEFINED/not-zero: the 27 exhaustion-negative types (worded per
  storage class: RESOURCE = authored file content; IMAGE = image
  bytes; HEAP/CALLER = no clear found), PLUS the refuted positives:
  LegacyPs2GsTextureContext+SlotClassBank (003ED3F0 runs on r14 =
  source descriptor, never this), CharacterRenderObject (001BC635 is
  a dx-bounded memcpy, not a clear), PendingCompletionQueue (all 3
  literal-0x108 sites are stack scratch), ResourceRequestSlot (all 36
  literal-0x80 sites scanned - stack buffers/foreign objects only;
  ctor writes named fields), RenderStrideC0Element (004E2CE1 memset
  is a reuse-time reset via 0037E17F, not construction),
  RenderStrideC0Bank (embed-in-static; no on-type literal site),
  LuaState (00881CC2 is off the newthread path - 00881C40 called only
  from 00881839).
Validator 597/7341/0/0; all gates green; LF preserved. FABLE lease
still held; publish queue grows.

THEN (same rev): SKIPPED residue closed - the 15 instrument-blind
types adjudicated from their own rows (10 empty-column Phyre classes
inherit the descriptor-image verdict; A0D0 parent clear;
PDeferredLightingSlot0080 default-buffer copy per its own row;
ImageBackedStateBlock .bss backing; MapRefFieldRow/WeatherLane
authored). check_clear_exhaustion now reports ZERO unanswered spans.
Also fixed 6 ctype-cells-holding-prose flagged by check_store_artifacts
(WorldLootPickupNode objectHandle -> u32, suppressDestroyFlag -> u16,
featureLevelFlag060 -> u8, menuObjectPtr 'void *' -> 'void*',
LuaUpVal u union{LuaTValue;UpValLinks} -> LuaTValue with the union
detail staying in meaning - UpValLinks is not a declared type,
WorldLootPresenceRecord position -> float[4]). 0 wrong-kind columns.
check_default_instance_writers confirms the descriptor default buffers
are themselves built by memset/memcpy in 00639A60/0063CB80 -
consistent with TEMPLATE wording, not a contradiction.

THEN (same rev): check_gap_debt's one TOUCHED defect closed.
LegacyPs2GsTextureContext unobservedSpan00A8 claimed 'no access' over
+0x110..+0x113, which the ctor's qword store at 002F6AEF carries (its
high half is declared dword0114). Split: the span shrank to 104 B
(+0xA8..+0x10F, genuinely untouched; the +0xA8 lea stays disclosed)
and a new unobservedDword0110 u8[4] row carries the CARRIED verdict -
the granularity name matches the store's own unobservedDword/Qword
convention, and only unobservedSpan* rows are census-accounted, so the
name is the honest fix, not an evasion. TOUCHED now 0. Validator
597/7342/0/0; surface figures resynced (7342/7339, GAME 5970,
LegacyPs2GsTextureContext 44/44).

THEN (same rev): check_store_behind_page queue closed - all 331
candidates triaged. The checker is a lead generator: identical
offset tokens across a type's own page mean DRIFT only when the
receiver is the same object. Dispositions: ~140 Phyre rows proven
clean mechanically against phyre_schema.tsv (no registered member
inside any declared gap); ~20 CONFIRMATIONS (the page itself
documents the span as undeclared/untouched - BattleStatsRecord's
surviving gaps, PhyreNamespaceBuffer +0x04 'one undeclared dword',
ActorStorageRecord +0x23/+0x8A, BattleSystemState +0x5AA2 the pad
after map 4); the rest COINCIDENCES (same offset on a different
record - the map widget +0x80/+0xC8 hits are page-slot objects,
EfxCallerTemplate +0x06 is an effect-file chunk header, the 02F8_00C0
rec+0x08/+0x18 copies are the transition record of
SaveTransitionMetadata_CaptureToRecord, WidgetSingleton02AEE4C0 +0xC4
is the separate 0x1D0 consumer, MessageWindowRecord +0xB8 is the
embedded 208-byte text-state block - whose own census REQ
FABLE-REQ-SWE2-STRUCT-TEXT-STATE-208-FIELD-MAP is already DONE).
ONE GENUINE DRIFT fixed: NameRegistryNode - the page's typedef
(vtable +0x00, name +0x08, next +0x10, value +0x18, stride 0x20)
was declared PROVEN while the store held unresolved spans at +0x00
and +0x18; declared vtable void* / value int32 and split the tail
(unobservedTail001C u8[4] - the page notes +0x1C is not read).
One annotation: AuthoredTableHeader unobservedSpan000 gained a
VARIANT NOTE - member table 02EBF020 reads +0x00 as its count
(0032A26D), a documented non-uniform variant, not a shared field.
One width artifact: the checker decoded the name-compare loop's
disp-0 string-byte read against the new vtable row - WIDTH
DELIBERATE note added (the pointer width rests on the RTTI-locator
resolution). Validator 597/7343/0/0; cited-site widths 0
disagreed/5 stated exceptions; surface figures resynced
(7343/7340, GAME 5971, NameRegistryNode 5/5); LF preserved.

THEN 2026-09-23 (board rev ~29245): check_lifetime_column's open-
destructor debt adjudicated 84 -> 15. Built a write-census over all
66 open PTR/SLOTPTR cells (data_xref_scan, control 0x02B47758 = 9
refs; 65/66 cells referenced - the unreferenced one is the
ActorRecordPool SLOTPTR base, reached by indexed addressing the
scanner cannot see, so no absence claim). Then a free-flow pass:
for every body referencing a cell, tracked whether the cell's
pointer reaches rcx/rdi at a call to the release fns 00244F00 /
003697F0 / 00245020. RESULTS:
- 25 POSITIVES - object release proven at the instruction. Singles:
  0208E6C0 (0023BD40), 0208E6C8 (00240AD0 arm), 0208E6D0 (0023CE10),
  0209AC18 (002878E0), 0209C300 (002970C0), 0209C380 (0029D210),
  0209C498 (0029E110), 0209E5F8+0209E600 (002B9B30), 022CA428
  (0035BB70), 022CBE20 (00366A00 via 00245020), 02AED490 (0037E4F0),
  02B5F1F8 (003F4B40), 02B62D80 (00408200: member@C0 then object then
  cell zeroed), 02B62D88 (00404F20), 02CA6C80 (00474040 via 00245020),
  02CA9718 (0056EF60). Shared teardowns: Widget0209CC18 - all three
  cells freed (002A7F70/002A8100/002A8220); 02B457E0 - members
  @D8/E0/E8/F8 via 003697F0 plus object via 00245020; MapScreenContainer
  - cell 02B47760 freed via 00245020 and the 0209E5C0/5F0 containers'
  selected +0x1B0 elements via 00244F00; 00582860 is a jump-table
  dispatch teardown freeing sibling cells 02CA99C0/D0/D8 in arms.
- ~24 ESTABLISHED NEGATIVES - cell only ever installed into, never
  cleared, and no referencing body loads it into a release arg;
  several free siblings but never the cell itself (0208E6D8 compare-
  read only; 02CA99E0 read-only in the teardown that frees C0/D0/D8).
- 2 PARTIALS recorded honestly: 02B62D78 (un-published at 00406AF7,
  release unestablished), 02CA9738 (members @108/@110 freed, object
  not). GlyphRunWidget1498 member@C0 freed, object not.
- 10 EMBED ManagerSub/pool children got the interior convention.
- 15 more: FrameMarkerSingleton01F82C80 (install-only), 5 CD3D11 POD
  descriptors, 5 GC-managed Lua types, LuaTValue interior, the two
  CHAIN lookup tables (interior in image-resident slots).
SIX-ROW ROUTE-DEFECT FINDING, filed
SWE2-STRUCT-REQ-OPUS-SIX-PTR-ROUTES-ARE-DWORD-BYTE-FLAGS (rev 29245):
WidgetSingleton01EFAC10, Widget02CA8F30, WidgetSingleton02CA9678,
WidgetSingleton02CA972C, Widget02CA99B0, Widget02CA99E8 - the named
cells are dword/byte STATE FLAGS written by the object's own handler,
never pointers; OPUS's 'self-publication' story is disproven at the
instruction (e.g. 00394600 gates on cmp byte [cell],2; 002D1513 is a
call, not a slot test). Two of the six still have proven releases via
handler `this` (00393EA0->00244F00; 0057E4D0->00245020); the objects'
fields are fine - only the route/publication story is wrong.
TOOLING FIX: check_absence_claims.load_pe returns a 5-field section
tuple different from ext_string_probe.sections - a scratch disasm
helper must use ext_string_probe.sections or it reads wrong file
offsets (decoded mulss where a mov [cell],0 actually sits).
Remaining 14 OPEN are honestly bounded: OPUS's deliberately-open math
types + PArray/PSharray, two LegacyPs2Gs BOUNDED rows, and
ActiveLogWidget40C8 (held at manager +0x1058; a whole-binary scan
found no body loading the member into a release call - it presumably
rides the widget hierarchy's recursive teardown). FOLLOW-UPS in the
same pass: PaneListWidget0B68 turned POSITIVE - lazily created by
0028FD70 into the manager's +0x10F78 slot and released by 00290E10
through 00244F00 at 00290E57; PendingCompletionQueue01F81248
sharpened to an established negative (installed once by 001BDA50,
never cleared, readers release nothing). 00244F00 reads as a deferred
release-request (marks +0x40|=0x40, calls 00244DD0+00245020 when the
flag bits resolve). Final column: 293 positive / 289 negative / 14
open. Validator 597/7343/0/0; all gates green; provenance consistent;
surface figures agree; LF preserved.
Publish still queued behind FABLE-PUB-001E2AF0-FINISHED's stale
@publication lease (FABLE filed an answer claiming release but the
lease row still names FABLE at checkpoint 2026-09-22T20:48).

INCIDENT + RECOVERY 2026-09-24: the session-resume checkpoint restore
rewrote _types/{types,fields}.tsv to the ~2026-09-23 20:32 snapshot
(SWE2-DATA's sanctioned CFG-WALKER census rerun, 383/384 caveat
amendments, is preserved - it had landed at 20:31 and IS the
checkpoint's tip). Everything I edited after that checkpoint was
uncommitted and is now recovered from transcript history + Temp
scripts: the 63-cell destructor verdict map plus the 9 tail-jmp /
direct-00244DD0 corrections, the unread-vs-census span package
(merged WITH the rerun clauses - qword0040/qword00A8 now declared
from the rerun's 0026E9CB/0026E9E3 reads; CharacterRenderObject's
+0x80 span is the ctor's movups block-copy, kept as floatBlock0088/
block0118 honest names), the six ctype fixes, NameRegistryNode's
0x20 split + 00876C00 dtor, the AuthoredTableHeader variant note,
the LegacyPs2GsTextureContext TOUCHED split (unobservedDword0110
re-added - the rerun superseded the planned shape and
check_gap_debt again reports TOUCHED: none), the AppBootStatic
alignment annotation, the 18 storage-class prefixes, VmValueStack
restored to HEAD's committed CALLER adjudication (the checkpoint
row predated it), ActorWaitSlot's prose ctype -> u64, and the
LIFETIME package re-adjudicated from a fresh check_clear_exhaustion
run: 1401 unobserved/unread span rows now all carry a LIFETIME
clause - widget-memset (00246626), Phyre default-buffer template
(0063C974), singleton-parent 0x10FD0 clear (00291765), verified
per-site clears (0023BE44/0023FC93/00266EFC/00402B3A/0039267E/
003EFD82/0041F754/00267A8B), frame-clear (BattleResultRecord),
ctor buffer-copy (CharacterRenderObject), IMAGE/AUTHORED storage,
or an honest UNDEFINED with the refuted-candidate note where the
checker's site clears a different object (LegacyPs2GsTextureContext
003ED43F clears the source descriptor r14, never this context).
Seven literal-clear candidates needed the destination read; two
bulk mechanisms were shared (the widget memset and the descriptor
template copy). Destructor column: 301 positive / 279 negative /
15 open, the opens all deliberately bounded (math types,
PArray/PSharray, two LegacyPs2Gs BOUNDED, ActiveLogWidget40C8,
Widget02CA99B4 pending the route-defect REQ). Validator
596/7325/0/0; surface figures re-agreed (the index docs quoted the
lost lineage's 7343 fields); store artifacts clean; gap debt
TOUCHED: none. DURABLE BACKUP: stash@{0} 29401124 holds the whole
working tree in the object store against the next restore.
Publish STILL queued behind the same stale FABLE lease.

FOLLOW-ON 2026-09-24 (second pass): the same checkpoint restore
explains FRONTIER-REQ-OPUS-STALE-ROUTE-REVERTS-IN-WORKTREE. HEAD
carries the 2026-09-24 route-vocabulary sweep (second `|`-joined
alternatives: FN/VTABLE/CHAIN/PKREF/PTABLE/PTR/SLOTPTR-parent) that
the checkpoint base predates, so a per-cell HEAD-vs-worktree triage
over all differing type rows found and restored 23 route cells
(PApplication, AchievementState, ImageBackedStateBlock - the REQ's
three - plus 20 more of the same signature). No intentional revert
exists; the mechanism is the session checkpoint restore, and the
rows now carry HEAD's committed routes again. The same restore had
reverted check_storage_class.py's VERBS past the PKREF/PTABLE/
VTABLE grammar - VERBS extended, symbolic SLOTPTR parents and the
PKREF resolver/parent anchor shape added; hard failures 12 -> 0.
Two standing DEREF notes (RenderResourceRoot PTR 0x022C6F20,
Manager0209AC60 PTR 0x0209AC30) are adjudicated: the pointer cells
do reach image-resident storage, so PTR route + IMAGE class are
both true and the note is a checker-model limit, not a defect.
Also consumed OPUS-REQ-STRUCT-RELABEL-AND-SWAPPED-SITES (finished,
rev 29364): 39 w->rw relabels applied and spot-verified against the
image, and the four swapped spawn-group-ledger sites re-derived -
SpawnGroup_ResetLifecycleLedger unrolls a 0x60-stride ledger of
four 0x18 sub-slots {qword,+8 qword,+0x10 flag}: 003070BF=
[rax+0x28] disp 0x8, 003070C3=[rax+0x20] disp 0x0, 003070C7=
[rax+0x40] disp 0x8, 003070CB=[rax+0x38] disp 0x0.
field_disp_scan._kind agrees with reg_tracking.op_kind on all 43
patch sites; documented divergences elsewhere: prefetch/nop 'r' vs
'addr', and exotic stores (fstp/xsave/sgdt/pop/stos/movs) use the
table here vs capstone flags there.
OPEN for OPUS (unchanged): the six PTR-route flag-cell REQ
(29245) + the seventh (Widget02CA99B4, 29246) and the
LuaClosure/LuaLClosure header-pair REQ.

PASS 3, 2026-09-25 - PUBLISHED as commit 7abc4cad5 (durable;
checkpoint restores can no longer take it). The commit carries the
whole recovery + rulings: OPUS's seven-flag-cells ruling applied to
all seven rows (routes -> DYNAMIC; publication prose withdrawn from
instance/evidence; dtor markers -> RULED), the
derived-route-parent-roots determinations applied (PDeferredLightingBase
VTABLE 0x00D61EA0|0x00D61F40; AuthoredTableHeader 41 registrar-proven
PTR slots; ActorDefinitionPayload/AuthoredExpressionBlock/
PaneListWidget0B68 recorded ARG-rooted pending FRONTIER's grammar
ruling; Lua types UNROUTABLE BY DESIGN), 12 CFG-WALKER clauses merged
in from HEAD before publish so dc4414b98's rerun content rides along.
OPUS-NOTICE-STRUCT-YOUR-WORKTREE-TYPES-TSV-REVERTS-23-F6-ROUTES
finished (rev 29425). SWE2-STRUCT-PUB-EQR-OVERLAY finished (rev
29447) - the EQR overlay was already declared. Gates re-green after
every step: validator 596/7325/0/0, storage 0 hard failures / 347
route alternatives, gap debt TOUCHED none. @publication released.
OPEN for OPUS now: only the LuaClosure/LuaLClosure header-pair REQ.

FIELD-ACCESS REGEN (FRONTIER-REGEN-FIELD-ACCESS-AFTER-RERUN claimed,
rev 29450): inputs stable at 7abc4cad5 + dc4414b98, regenerated
_types/field-access-index.tsv under the corrected op_kind: 22,913
rows over 154 types (kinds addr 904 / r 14,170 / rw 1,740 / w 6,099).
Delta +2,763 vs HEAD's 20,150, fully attributed to the newly rooted
routes applied in the same commit: AuthoredTableHeader +2,281 (41
registrar PTR seeds), PDeferredLightingBase +340 and
PDeferredLightingSlot0080 +93 (VTABLE seeds), IndexedExternalSource-
Request +49. Verified: every store-form movups/movaps/movdqu/movdqa/
movq/movd/mov row is w or rw (0 mislabeled), all 2,117 test/cmp/bt
rows are r, 1,740 rw rows reach writer queries. Publish queued on
@publication (OPUS-PUB-188-OWNER-MAP holding at claim time).

2026-09-28 - OPUS-REQ-STRUCT-ROUTE-002ED570-BANK-GENERIC-0927 DONE
(instrument repair). Route grammar extended: `FN 0xADDR+0xOFF
bank=0xD` - the qualifier names the parent slot whose load fed rcx,
and seeding marks rax only at sites classify_slot_resolver_sites.
site_slot_map (now the shared engine for both the standalone report
and the census gate) attributes to exactly {(fld,disp)}; ambiguous
and unresolved sites seed nothing. Attribution: 86 sites +0xD98, 11
+0xD90 (2 direct to 002ED570, 9 through the dedicated tail-jmp
getter 00409F50 - carried as RES's second route alternative), 4
+0xDA0, 23 excluded. Store: RenderStrideC0Element `bank=0xD98`,
RenderResourceEntry `bank=0xD90 | FN 0x00409F50+0x0 bank=0xD90`.
New regression check_route_collisions.py groups FN alternatives by
(address,delta,bank) and refuses different-sized sharing;
FN 0x002EF640+0x200 (PersistentFlagPayload/SavePayload) is the one
documented KNOWN exception, still unjudged. Regenerated
field-access-index.tsv: 28,883 rows/205 types; C0 = 433 rows/70 fns
max +0xB0, RES = 64/17 max +0x44, 005049E0 excluded everywhere (its
site is genuinely unproven), 0041F340 legitimately in both (it
calls the +0xD90 getter and resolves through +0xD98).
route_collision.py C3-C5 now assert the repaired invariants, all
PASS. Gates: validator 789/8224/0/0, collision check PASS,
consistency/links/questions/doc-addresses clean, ADDRESS-INDEX
regenerated. PUBLISHED as commit ffe018a49; board REQ finished rev
34844, pub task SWE2-STRUCT-PUB-BANK-KEYED-ROUTE finished rev
34858, @publication released. One incident folded in: my
route-append had re-left a mid-cell CR on both repaired rows,
truncating them to 11 cols and silently excluding both types from
the whole index sweep - fixed at byte level; row-width audit
confirms 0 malformed rows.
OPEN/queued: only the LuaClosure/LuaLClosure header-pair REQ awaits
OPUS; PersistentFlagPayload/SavePayload prefix-overlap judgment
still deferred to OPUS (documented exception, not silently kept).

2026-09-27 - FRONTIER-REQ-SWE2-STRUCT-BB1-3B0-CORRECTION-0927 DONE
(owner correction). BB-1 verified right against the image: at
001FA423-38, r9=+0x3B0 is arg4 and 001ABF50 only reads it (subss
001AC075/7B/E6/EC); the out-params are r8=+0x3C0 and rdx=+0x3D0
(head-fill 0/4 at 001ABF6E/74, indexed stores 001AC33C/350/354).
character-render-object.md corrected in the table (+0x3B0 ->
submitInVec, bracketed note) and the +0x1037 scan-control prose.
Doc verify: 354 citations, all resolve.

## OPUS-CONTRA-SWE2-STRUCT-32C4-BITMAP-EXTENT-IS-NOT-ESTABLISHED — the layout half is measured, 2026-09-18 (OPUS)

**Your ruling is easier than the contradiction made it look: the extent was the wrong claim, and the
two byte rows stand.**

Routed is not resolved, so I took the part inside OPUS scope — bounding the index — and it settles
the conflict without needing a convention call.

**Nineteen call sites, all accounted for.** Neither accessor bounds its `u16` index, so the extent
has to come from the callers, and every one of them hands a compile-time constant:

- `0023F8B0` and `002405F0` each run a switch whose arms load `0x1E`, `0x1F`, `0x20`, `0x21`, `0x22`,
  `0x23` into a shared `movzx ecx, ax`.
- `002CDAE0` has sixteen arms — thirteen `mov ecx, imm`, and three of the form `lea ecx, [rax + imm]`
  under a `test eax, eax` / `jne` guard that makes `rax` zero on the path reaching the call, so those
  are constants too.
- The one writer, `002E23E0`, tail-jumps to `00254E00` with the index from the translator `002E13C0`,
  whose ten jump-table arms and out-of-range default yield `0x00`, `0x01`, `0x09`, `0x12`–`0x16`,
  `0x1D`, `0x1E`.

**Union: `0x00`–`0x06`, `0x08`–`0x16`, `0x1D`–`0x23`.** Nothing hands `0x07` or `0x17`–`0x1C`.
Highest index `0x23`, highest byte **4** — the accessors reach `+0x32C4..+0x32C8`, **five bytes**.

**So `imageByte32CC` would have been bitmap byte 8 and `imageByte330C` byte 72, and both are outside
the five.** Your two rows are right; the `0x80` was the wrong one.

**Where the `0x80` probably came from.** The page that propagated this row has had `0x80` struck
**twice already** — both group persistent banks, corrected to `0x200` on 2026-09-11. And the nearest
`0x80` in the code is the memset at `00253B56`, whose base is `+0x3244` and which therefore ends
exactly where this bitmap begins. Three instances of one wrong default on one page.

**What I did NOT do, deliberately:** consume `+0x32C9`..`+0x3344` into the bitmap, or give it a new
number. **Five bytes reached is a floor on the object, not a proof of its end**, and the row now says
the upper bound is not established rather than trading one unsupported figure for another.

Corrected in `_types/fields.tsv` (+0x32C4) and in `the-save-payload-field-map.md` in both places the
`0x80` appeared. The instrument is `Tools/work/OPUS/bitmap_bound.py`; it **refuses to print a bound**
while any call site fails to resolve to a constant, which it did three times while I was building it.

2026-09-28 - two ASTRA nav REQs consumed (claimed rev 37736/37738).

ASTRA-REQ-STRUCT-NAV-GRID-CLEAR-ROUTE: verified the route in-image
myself - 00392710 loads cellBitsetArray (02AEE0A0 = NavGridParams
+0x40), null-guards release through 003844F0 (jmp 003697F0, the
raw-pointer release front) and tail-jmps the memset import
(00861EC0 = jmp [008C2A60]) on [02AEE060, 02AEE4C0). The only rows
contradicted are NavGridParams' four unobserved-span LIFETIME
verdicts ("not engine-cleared") - struck and amended scoped: birth
bytes remain the image's, the four-route negative stands scoped to
the birth/init procedure it enumerated, teardown-vs-rebuild
ordering unexamined. NavSlotPointerArray carries no LIFETIME
verdict; nothing else in range. OPUS had already consumed the type
rows (dtor release route, PRECONDITION clauses). The four
specific-route negatives elsewhere NOT retracted (per REQ).

ASTRA-REQ-STRUCT-NAV-TRAILER-GETTER-ALIAS: the correction was
procedural, mostly already landed by OPUS's re-cut (field rows +
NavRunStateBlock +0x24/+0x28 carry the scoped struck history). My
remainder: NavTrailerRecord28 TYPE evidence still asserted "No
code reads this table" flatly - now struck to scoped history with
the getter-alias mechanism named (00383840 = mov rax,[02AEDFB0];ret
-> mov r15,rax in consumers; verified 00392740's cmp/cmovb
[rax+0x24] + mov ecx,[r15+0x28];call 0020E600). Nav doc's +0x28
line updated. Procedure fix: ABSENCE-CLAIM-GATE blind spot 13
added - a call-return alias is invisible to cell-seeded census,
one-instruction `mov rax,[rip];ret` getters are the marker; named
in trackscan.py's declared limits too. Standing debt recorded:
other cell-seeded "no consumer" verdicts exposed, not re-tested.

Also fixed: check_storage_class.py fld["width"] -> fld["size"]
(latent at HEAD; newly triggered by peer's PrimitiveRendererD3D11
sized-by-argument EMBED). Gates: validator 820/9053/0/0,
storage-class 0 hard failures / 599 alternatives, type-refs 0
dangling, census-widths 0 disagreements, consistency clean, doc
addresses resolve on both edited docs.

Follow-up same day - the blind-spot-13 standing debt is now
MEASURED, not open-ended: .text holds 69 `mov rax,[rip];ret`
one-instruction getters over 68 cells, 11 anchoring PTR routes
(enumerated in ABSENCE-CLAIM-GATE). Read back, the exposed rows'
negatives already name their instrument - no amendments needed.
The remaining open item is a transitive return-propagating
consumer census, a different instrument, recorded not approximated.

2026-09-29 | getter-seeded stale-name package: the blind-spot-13
re-test's residual defect was in the STORE, not the image - 13 rows
carried unobserved*/unknown names while their own evidence recorded
accesses. Fixed in two classes:

CLASS A (name-vs-evidence contradiction, 9 rows + the four seed rows):
renamed/split to what the census lines actually measured -
PApplication +0x001D -> flagByte001D (setne store at 008655CD via
getter 00796E20), +0x0D50 -> dword0D50 (5 read sites), +0x84 ->
byte0084+residue, +0x9C -> dword009C, +0xD68 -> dword0D68+dword0D6C,
+0x10D0 -> word10D0+residue; BootSingleton +0xCF0 -> dword0CF0+
qword0CF8+residue, +0xDA8 -> dword0DA8 (write-only), +0x3 ->
unobservedByte0003+dword0004, +0xAF4 -> qword0AF8+residues, +0xB80 ->
qword0B80+byte0B88+residue, +0xD19 -> byte0D48+residues;
MessageWindowRecord +0x3F2 -> byte3F2 (1r/1w). Site texts verified
against the image (all 18 addresses disassembled before naming).
CLASS B (misplaced type-level refutation, 4 rows): CharacterRenderRecord
+0x62/+0x458, ManagerSingleton0209BE80 +0xAB24, PApplication +0x10F0 -
the CFG-walker rerun's 'no censused access no longer holds here' clause
was applied per-row where the same run still measures ZERO for that
span; clause replaced in-place with the scoped form, unobserved names
stand on their own measurement.

check_unread_vs_census.py gained a second pass reading name-vs-EVIDENCE
(the census-file pass sees only the 74 mapped types): flags unread-named
rows whose FOR THIS SPAN line records a positive - caught all of the
above, now reports 0. Regex note: requires the count/site at clause
start; the "398 access triples" caveat text is a known false-positive
shape, kept out by anchoring.

Gates: validator 821/9076/0/0, type-refs 0 dangling, census-widths 0,
storage-class 0 hard failures / 600 alternatives, route collisions PASS,
consistency clean, questions clean, ADDRESS-INDEX regenerated.
Commit 89edb9a6c (published via SWE2-STRUCT-PUB-STALE-NAME-0929, rev 37917).

2026-09-29 | blind-spot-13 second bound (measured): widened the
getter enumeration from `mov rax,[rip];ret` (69) to the <=3-mid-
instruction envelope, every candidate body disassembled and
classified by rax-at-ret: object-alias surface 98 sites (69 MOVRET
+ 11 OBJFRAME + 17 conditional mutator hybrids + 0039C4A4
object-or-fallback); ~20 member-pointer getters (alias the MEMBER -
0028F570->[+0x9FE8], 0028F6F0->[+0x10F50], 0037EB70->[+0xD8],
0028F590->obj+0x80 interior); ~100 scalar-field accessors (not
alias exposure); 0 lea-forms. Re-test: SEED=call fixpoint on all
42 typed sites -> only 0028F570/0028F590 produced tracked pairs,
all hits on already-named regions, ZERO debt-span hits. The 40
zero-pair results are an instrument bound not "no callers"
(0037EB70 has 4 E8 callers whose member ptr leaves via rdx/arg2,
outside the tracked rcx set) - recorded as the named residue in
ABSENCE-CLAIM-GATE. Lane sweep on newest landings: validator
821/9076/0/0, all gates clean.

2026-09-29 | 002EF640+0x200 deferred judgment CLOSED: the route
collision exception between PersistentFlagPayload (0x1538) and
SavePayload (0x56490) is adjudicated - the store already ruled it:
OPUS's 2026-09-20 clauses record CONTAINMENT (SavePayload declares
+0x000 persistentFlagPayloadRegion, a typed deferral of exactly
0x1538; seed by EXTENT not route) and OPUS-CONTRA-SAVENEST was
dispositioned+executed. check_route_collisions.py's KNOWN entry
still said "candidate - unjudged": updated to record the judgment;
the exemption stays so the pair stays visible rather than
re-flagged. No route-column change - OPUS's `EMBED SavePayload
+0x0` observation stays an observation, not mine to land on
another agent's declared row.

2026-09-30 | blind-spot-13 residue MEASURED + instrument widened:
arm-following enumeration (any arm to ret within 8 ins) found 202
object-returning + 18 member-pointer sites over 420 mov rax,[rip]
loads; across 1,740 direct call sites the caller's first copy of
rax goes to rcx 734, non-arg reg 103, non-rcx ARG reg 22 (rdx 20,
r9 2; ~1.3%). census_receiver_fixpoint.py extended: ARGREGS=1
enqueues callees on rdx/r8/r9 and seeds each pair on the arg reg
the caller used - (fn,base,arg) pairs, default off so published
numbers are unchanged. Verified: 0037EB70 seed goes 0->4 pairs
and reaches 0029CD00 via mov rdx,rax @003BE9BB; self-test 147
unchanged. Recorded in ABSENCE-CLAIM-GATE blind spot 13.
2026-09-30 | publish PENDING lease: 4-file package ready
(census_receiver_fixpoint.py, ABSENCE-CLAIM-GATE.md, this file,
AUDIT-LOG.md); SWE2STRUCT-PUB-ARGREGS-ENQUEUE queued at rev 38160.
@publication held by stale OPUS-PUB-SEAD-CATEGORY-LIST (holder has
no live session; ASTRA's stale lease was adjudicated after board
note at rev 38162). Next action: retry claim, publish, finish.

2026-09-28 | FRONTIER-REQ-STRUCT-BOARD-WRITE-PATH-REPAIR done:
writer identified as session-side inline RMW of a stale
in-memory TEAM.json copy (ORACLE's recovery note admits it; no
script file writes the board - audited). _write_board gained a
bounded WinError5/32 retry at os.replace. test_team_rollback
+3 (37/37 pass). Named on board at task finish.

**Workflow adoption — FF12-WORKFLOW-MIGRATION-20260928-01 (dispatched by SWE2-FRONTIER, 2026-09-28, at next safe checkpoint).**

The user approved a completion-driven workflow migration. Preserve your current identity, active work and ownership. Read the adopted _index/workflow/COMPLETION-WORKFLOW.md and its revision at your next safe checkpoint. OPUS now owns technical migration delivery; ASTRA/SOL independent engineering verification; FABLE connected mechanism completion; FRONTIER operations, safe deployment and capacity allocation. Existing specialist roles remain. This supersedes older operative instructions assigning sole migration architecture to FRONTIER or categorically forbidding useful new tools; it does not supersede full L1+L2 requirements, independent review, safety, game-state protection or history. Do not stop useful work merely to re-plan. Respond through current checked records, self-check changes, consume review, update authorized canonical files and select the next eligible task without user relay. Honour explicit stops and limits. Report a real policy/ownership conflict instead of silently overriding it.

Read the adopted _index/workflow/COMPLETION-WORKFLOW.md, current evidence policy and checked task state. Preserve your existing lane identity, history and peer work. OPUS owns technical delivery, FRONTIER assignments/deployment, SOL independent engineering verification, FABLE completion semantics. Complete your assigned contribution through its required canonical changes and review; a request alone is not package closure. Use existing task IDs and exclusive paths; do not create a competing implementation or direct-edit TEAM. If capped or blocked, checkpoint for a supported handoff and do eligible independent work, without evading limits.

SWE2-STRUCT: work assigned implementation-relevant structural questions and controls under the selected completion package. Verify receiver/base identity, widths, offsets, extents, ownership and aliases against primary evidence. Preserve variable-size rules and distinct native/serialized layouts. A zero from a bounded detector is not universal absence; shared address does not identify the active occupant.

Reuse shared reviewed access adapters; repair only the bounded producer path and its affected consumers when evidence supports it. Do not write a new generic scanner or treat a complete layout as understood purpose. Supply exact evidence, claim-level limits and page/register links. If assigned a cross-lane independent review, do not review your own contributed code or claims. Accept useful scoped work without forcing unrelated exhaustive campaigns.

Self-check and record exact source/driver/input/result identities and limits. Use a qualified non-author for independent acceptance of your production. A required upstream failure or missing result is not PASS. Preserve historical receipts and relevant regressions; run impacted checks during development, broader campaigns only at governing gates. Update the actual tool/consumer path and persistent procedure so the same defect is caught next time. Use fresh preimages, supported writes, short publication claims and meaningful commits. Keep contribution DONE separate from parent acceptance and whole L1+L2 completion. Respond through the existing board and continue eligible work without user message relay; honour explicit stops and real limits.

2026-09-28 | ARGREGS cohort re-test (33 types, 53 seeds replayed from
the SWE2-DATA rerun registry, Tools/work/SWE2-STRUCT/census-argregs/):
ZERO unread/debt rows gained an access - the rcx-only limit hid no
debt consumers in this cohort. Yield is on factory/member-result
call seeds: 0081ED30 0->78 pairs (all four Lua types), 002EF640
9->33 fns, 001BDAB0 23->30, 00189120 69->81 fns. Two named bounds:
5 hub seeds (0209BE80/022C6F28) truncate at CAP=400 under the wider
pair space - prefix, not verdict; converged losses vs the recorded
run reproduce under ARGREGS=0 = the 6b6a423db kill-set fix, not
the option. Tool doc records the CAP interaction. Durable artifacts:
rerun.sh + evaluate.py + out/ under census-argregs/.

2026-09-28 | ARGREGS cohort re-test COMPLETED: the five hub seeds
that truncated at CAP=400 converge at CAP=8000 (0209BE80: 1463
pairs/149 fns; 022C6F28: 717 pairs/369 fns, +42 fns over rcx-only).
Full-cohort verdict now holds without the prefix bound: ZERO
unread/debt rows gained an access under ARGREGS=1. Committed
e52f9bc03 covers the truncated-prefix version; the converged
figures amend ABSENCE-CLAIM-GATE + tool doc in the next publish.

2026-09-28 | indexed-access limit made MEASURED: census_receiver_
fixpoint now counts [tracked + idx*scale + disp] sites whose
displacement could land in-extent (deduped per site, printed after
totals, emitted as EMIT_JSON indexed_skips). Control Manager0209AC60
skips 70 such sites - the measured shape is embedded sub-arrays
(member pointer tables at [base+idx*8+N], per-index flag bytes at
[base+idx+N]). Recorded behavior unchanged: 147 displacements PASS.

2026-09-28 | ctor-seeded sweep ADJUDICATED and landed (artifacts:
Tools/work/SWE2-STRUCT/ctor-sweep/ - jobs.json, out/, hits.json).
61 fixed-size exclusive-ctor jobs ran (3 variable-size types
unseedable); 134 span hits -> 54 plain / 112 enumerated-only.
Plain hits all verified in the native bodies; fields.tsv amended
21 rows across 11 types:
- LuaState +0x46 -> counterWord0046 (inc/add/movzx/mov word;
  the 5.2.1 nCcalls prediction is now OBSERVED); +0x28 ->
  qword0028 (pointer-valued, CallInfo-path); +0x4A split into
  counterDword004C + counterDword0050 + 2 unobserved residues.
- CorridorNavAgent +0x50 split: dword0060/64/68 confirmed as the
  lea'd out-param slots the row itself predicted; two movss-read
  (likely float). ARGREGS callee reach did the work.
- HandleSlotRecord +0x18 split: float0018 + dword001C - refutes
  the row's "not written by the issuer".
- BattleMenuPanelWidget3010Block +0x28 -> qword0028 (ptr read).
- CPostEffect +0x420/+0x430 -> dword0420/dword0430 (+0x420 is the
  low half of a wider qword pair store, recorded as such).
- DevConsole +0xA94 split: dword0A98 (init 6) + qword0AA0 (init
  0, read 4x); +0xE68 clause-only (32 enumerated sites).
- RenderContext{PassStateBlock,Record18,Record28} +0x0 ->
  ctorZeroQwords0000 (xor-verified zero-init heads).
- LuaUpVal +0x0A: hits resolve to LuaState `status` via the
  luaF_newupval entry-rcx=L misattribution the row itself flagged
  - clause appended, padding name retained.
- 112 enumerated-only sites recorded as clause-only candidates
  (PTextureCubeMapD3D11 680B loop-clear, DevConsole +0xE68,
  UnitStatusView, Render{Dyn,Uav}Buffers58, LegacyPs2Gs x3) -
  NONE promoted to fields, per the enumerated-sites rule.

2026-09-28 | ENUMERATED-ONLY ctor hits ADJUDICATED natively (all 7
clusters, 112 sites): the honest yield is 1 partial promotion + 6
refutations.
- DevConsole +0xE68: the 001CCF90 nested loop really writes two
  48B dword blocks (+0xE68..+0xE97, +0xF88..+0xFB7, ecx=0xC inner,
  ebp=0) inside the 576B span - split into initDwordBlock0E68/
  initDwordBlock0F88 + two residues. (rdi=this at 001CCB42.)
- PTextureCubeMapD3D11 +0xA8 (63 sites): REFUTED - element-init
  helper 0061CFA0 called once from ctor via 00627800 with edx=1,
  in-place arm writes +0x38..+0x68 only; all +0xB8.. hits are
  induction-window artifacts of a 1-iteration loop.
- CPostEffect +0x420/+0x430 enum site 006FF790: REFUTED - -1 fill
  bounded rbx=7 ends +0x3EF. Earlier clause corrected.
- RenderDynamic/UavBuffers58 +0x20/28: REFUTED - sites are
  cmp [rdi]/[rdi+0x10] with rdi=this; phantom bases.
- UnitStatusView +0x8E/8F: REFUTED - delta-pointer copy loop
  (rdx=rdi-r14, rcx=r14+0x68, r8=4) writes this+0x4C..+0x5B.
- LegacyPs2Gs x3: consistent with existing NO-REAL-ACCESS rulings.
Method note for the store: induction-window enumeration produces
dp lists for loop bodies at trip values the bound never reaches;
verify the loop bound + base provenance before promoting.

2026-09-30 | `FRONTIER-REQ-SWE2-STRUCT-PASS22-DEBT` DISPOSITIONED: all live
UNACCOUNTED NEIGHBOUR pairs on the lane's five folders (16-UI,
17-Presentation-Rendering, 21-RNG-And-Determinism, 22-Middleware-PhyreEngine,
23-Third-Party-Libraries) are cleared. Fresh `audit_crossrefs.py` reports ZERO
findings on the folder set (audit run after final write: 862 findings total,
none in the five folders).

- The 09-29 worklist (305 rows / 57 pages) was a snapshot; the live set
  re-measured at 344 pairs / 65 docs on today's tree. Peers cleared ~293 with
  semantic crossing sections while this session ran; the residue - 51 pairs on
  19 docs, then R6-cascade rounds of 16, 8, 3 and 2 - was dispositioned here.
- Method: edge enumeration replicated exactly from the audit module
  (same `cited_addresses`/substrate/hub/R6 filters); every pair's edges were
  read in `functions.tsv`/`edges.tsv` before classing. Class vocabulary:
  SERVICE (doc subject reaches layer bodies), CLIENT (layer bodies call doc
  subjects), MECHANICAL (all edges are fan-in on one shared accessor - e.g.
  `PartyFocus_GetCurrentPackedActorHandle` 78 callers,
  `SaveImage_GetPersistentPayloadBase`, `BattleEncodedId_IsValidForClass`,
  `RNG_MT19937_NextU32_Thunk` 53 formula callers).
- 77 bullets appended under `**Layer - CLASS (N edges).**` style with named
  functions; `neighbour-dispositions.tsv` carries a CROSSING-ACCOUNTED row per
  pair with direction counts.
- Recurring cascade noted: dispositioning one accessor promotes its own
  neighbours to subjects (R6), so the audit must be re-run until the folder
  set is clean - four sweep rounds were needed.
- OV31 page edit (AUDITSPEC-REQ-STRUCT-OV31-NARROWING-0929) is also in the
  worktree and ships in the same publish: the broad message-16 claim is
  narrowed to the enumerated owner-notify sites and the residue named; the
  00582EB5 release path is gated on `+0xC4` bit-0x10.

NEXT: none queued for this lane. Fallback: sweep newest landings, then the
next unblocked package.

## OPUS-REQ-STRUCT-OV58D-RESIDUE-BOUNDS-0930 — completion record written, 2026-09-30 (SWE2-STRUCT)

P1 layout request claimed at rev 42109. Every function in the OV-5/8(d) residue census
(`commit:a67cad059`) read in the shipping binary; the record is
`_index/candidates/ov58d-pointer-flow-0930/RESIDUE-BOUNDS-0930.md`.

- All 12 INDEXED-UNKNOWN bases identified: `003266C0`/`0030B180`/`003279B0`/`002370C0`-class
  state writers are all above `+0x4F10`; `00252D40`/`00254E00`/`00252E60`/`00252610`/`002527B0`
  write the `image + 0x8200` head (`[020927C0]`, = `state − 0x4648C`); `00583D60` writes the
  `image + 0x20..0x43` header table (9-slot loop); `003112F0` is a bounded record-to-record
  delta copy; `0030B6A0` writes inventory descriptor nodes.
- 5 RECORD-INDEXED: four in-record (`0030E130` fixed fields; `0030FED0` stack + record fields;
  `0030EA40` index `≤ 7` via authored byte; `0031A630` slot validated by `00317930`). The one
  **named reach** is `0030E360`: `rec + 0xBC + 4·id` and `rec + 0x13C + 2·id` with `id` an
  unbounded byte arg — region A reachable for `k = 38` at `id ≥ 0xB5`, `k = 39` at `id ≥ 0x43`,
  or any `id` if a caller passes a `k ≥ 40` "record". `003112F0`'s copy loops show the
  container contract is 32 slots (id `0..0x1F`).
- 65 INDEXED-BELOW (38 base < +0x8, 27 with min-base inside the record array — the residue's
  "31" counts four dual-class functions twice): all bounded. Notable mechanisms — the
  `002536A0`/`020927C0` family writes `image + 0x8200` bitfields (28 fns); the `0032AB*`/`0046B*`
  family writes `002EF2B0()` = `image + 0x200` payload flag arrays with `cmp`-bounded ids;
  `003236F0`/`00323740` are unbounded in `cl` but the `0x1C8` stride lands every store either
  in-record or at `≥ state + 0x4FED`, skipping region A; `00328990`'s authored-word index is
  bounded by its sole caller `00328BD0` (record kind `≤ 5` → max `state + 0x2B3B`);
  `00327CB0`/`00234ED0` terminate on `0xFFFF` sentinels.
- Census limits (437 depth cuts, 15 indirect calls, 26 escapes) unchanged — out of scope.

NEXT: DONE — published `8972515f0`, task finished and the result posted to OPUS.
Fallback: sweep newest landings, then the next unblocked package.

## OV58D follow-on — `0030E360` caller-cone audit, 2026-09-30 (SWE2-STRUCT)

Unproctored continuation of the residue work: the named reach's deferred question —
"does any caller pass an out-of-contract `id`?" — answered by reading every call site
in `edges.tsv` plus the two forwarder layers.

- **Two sites falsify the `id ≤ 0x1F` contract.** `002FDDA0` (message switch on
  `word[unit+0x714]`, jump table `0x2FE534` for `dx ∈ 0x4046..0x4091`) has single-value arms
  `dx=0x4049` → `lea r8d,[rdx-0x51]` → `r8b=0xF8` and `dx=0x404A` → `r8b=0xD9`. Both write
  outside the record for every `k`, and into region A for `k ∈ {38,39}`.
- All other sites bounded `id ≤ 0x1F`: literals `0`, `4`, `5`, `0x18`, `0x1F`; bit-index
  loops `cmp ebx/edi/ebp,0x20` in `0030E8F0`/`002394C0`/`0030F690`/`0030FED0`; `0030E360`'s
  self-call forwards its own `r8b`. `0030E990`/`0030EAE0` are transparent forwarders.
- Stale edges noted: `00318A00`/`00318A90` listed as `0030E990`/`0030EAE0` callers but their
  bodies contain no such call/`jmp` (they call `0030E9C0`).
- Remaining unknown (runtime, not static): whether any unit's `qword[unit+0x698]` stats
  record is index 38/39 when messages `0x4049`/`0x404A` arrive. `002FDDA0`'s own caller is
  an indirect/cut edge.
- Record: `_index/candidates/ov58d-pointer-flow-0930/CALLER-CONE-0030E360-0930.md`;
  `RESIDUE-BOUNDS-0930.md` §2 carries a pointer amendment.

NEXT: DONE — published `a129411cc`, task `SWE2STRUCT-PUB-OV58D-CALLERCONE-0930` finished,
`@publication` released. Queue is empty for this lane — fallback: sweep newest landings, then
the next unblocked package.

## OV58D `0030E360` — allocation half traced, 2026-09-30 (SWE2-STRUCT)

Second pass on the residual. The `unit+0x698` assignment is `0023A570` @`0023ABFA`:
`r15 = [02EBF190] + 8 + 0x1C8·r12`, `r12 = byte[spawn_row+0x23]`, gated only by
`00322C50` kind-2 (`[[02EBF130]+4]` = `battle_pack.bin` party-definition table row count =
40). Record index = party-def row; **38/39 are the last two Esper slots** — real, not exotic.
The open question is now only whether an Esper-class unit can receive message
`0x4049`/`0x404A` (the `002FDDA0` dispatch edge is indirect/cut). Also noted: the `imul` is
unclamped, so `r12 ≥ 40` would install an out-of-array record pointer outright.

NEXT: DONE — published `07dee22b4`.

## OV58D `0030E360` — indirect edge resolved, runtime request filed, 2026-09-30 (SWE2-STRUCT)

Third pass. The "indirect/cut edge" is resolved: `002FDDA0` is a `.data` handler-table
entry. `00307BE0` → `00305080` does `rdx = qword[0x01EEC460 + (msgid−0x4000)*8]`,
`jmp rdx(rcx=unit)` — the order-handler dispatch table (358 entries, msgid `0x4000..0x4165`).
Byte-verified: `msgid 0x4049` → `@01EEC6A8 = 002FDDA0`, `0x404A` → `@01EEC6B0 = 002FDDA0`.
The tick path (`00233F70` → `00308610` → `00307BE0`) has **no unit-class filter**, so an
Esper-slotted unit runs `002FDDA0` whenever those msgids are queued on it. No static
`0x4049`/`0x404A` producer exists in `.text` immediates or the `.data` message records —
sender is plausibly script/ordered-action data → runtime question filed to ASTRA as
`SWE2STRUCT-REQ-ASTRA-OV58D-ESPER-ORDER-0930` (rev 43459). Peer landing `089f55128`
(FABLE T3b repair) carries this reach as the named limit of its region-A claim — consistent
with this record.

NEXT: DONE — published `feed29fe9` (task `SWE2STRUCT-PUB-OV58D-DISPATCH-0930` finished).

## `check_gap_debt` receiver-foreign fix — the lone TOUCHED row adjudicated, 2026-09-30 (SWE2-STRUCT)

Queue-empty fallback ran `check_gap_debt.py` and found one defect-class row:
`BattleStatsRecord unobservedSpan005C` (`+0x5C..+0x64`) flagged TOUCHED by three sites in
`00386C70` (`BattleFormula_AdvanceStatusTimersAndBuildResult`): `00386E43`, `00386E56`,
`00386EEC` — all `[r14 + r12 − 0x60]`. The fields row already adjudicated them (FE-4
store, OPUS 2026-09-27): `r14 = target + 0xBC + 4i`, `r12 = result − target`, so the
effective address is `result + 0x5C + 4i` = `BattleResultRecord.parameterA[i]`, a
different receiver. Re-verified in the binary (`00386C90 lea r14,[rcx+0xbc]`,
`00386CC6 sub r12,rsi`).

Root cause: census *site-level* receiver misattribution — `r12` is a receiver delta,
not an index, but the census records the residual `0x5C` disp against this type and
the checker counts numeric displacement only. Fix (published `feed29fe9` successor,
this publish): the three census rows carry `receiver-foreign:BattleResultRecord` in
their `note` column (rows kept — the scanner did see the sites), and
`check_gap_debt.py` skips `receiver-foreign`-tagged rows in both
`census_displacements` (TOUCHED/AMBIGUOUS) and `census_functions` (INHERITED).
`fields.tsv` +0x5C row's FE-4 clause names `parameterA[i]` and the tag.

Result: `TOUCHED = 0` — every censused gap is again a measured absence. This is the
fourth defect class the checker's use has forced: unwrap-AND, addr-sites, and now
receiver-foreign. Open debt unchanged: 838 UNMEASURED rows (35,519 B) across
uncensused types; the transitive getter-alias census remains the standing known
limitation.

NEXT: DONE — published `9b6c5bc93` (task `SWE2STRUCT-PUB-GAPDEBT-RCVFOREIGN-0930` finished). Queue-empty fallback continues.

## Route-seeded census batch + width-gate adjudication, 2026-09-30 (SWE2-STRUCT)

Queue-empty fallback burned down UNMEASURED gap debt. `gen_route_seeded_census.py`
fixed twice: a stale 3-tuple unpack in the `--with-children` path (the `types` dict
yields three values since the ctor column), and fail-closed behaviour — an
unseedable route now prints `UNSEEDABLE` and returns 2 instead of emitting an
empty census that reads as a measured zero.

Fourteen type censuses generated and registered in `check_census_widths.py`:
Manager0209AC60, ManagerSub0209AC60_02F8_00C0, ManagerSub8FA0SlotRecord02B8,
ShadowSettings01F82EA8, CPostEffect, Vu1RegisterBank02064B00,
BattleMenuChildRecord1E0, WidgetSingleton0208E6C0/0208E6D0/0208E6D8/0209C498/
02CA99C0, Widget02CA6C80, Widget02CA9790. DeveloperConsoleSettings and
TextPainter produced genuinely empty censuses and are deliberately unregistered;
the two VP8 decoder types are UNSEEDABLE (routes bottom out in
VpxVp8DecoderContext) and stay UNMEASURED.

The CPostEffect census falsified 13 "unobserved" gap rows — real TOUCHED defects,
not misattribution. Re-cut per convention: observed bytes carved into named rows
(+0x58C/+0x5A0/+0x5BC/+0x5E0/+0x660/+0x680/+0x71C/+0x73C/+0xADC/+0xCE6/+0xD26/
+0xD2F) with census+instrument provenance, residual spans shrunk.
WidgetSingleton0209C498's gap split around the observed +0xD8/+0xD9 tag pair.

Width gate adjudicated all 16 resulting mismatches — every one a legitimate
mixed-width case the `WIDTH DELIBERATE:` marker exists for: SIMD movups/movsd/
qword-clear bulk ops over element-declared floats, writer/reader width splits
(dword store vs movsx-word reads at Manager0209AC60+0x3E0), packed qword vs
per-byte access (02CA99C0+0xC0), byte tests of a declared dword flag. Each row's
marker cites the sustaining sites. 0 mismatches.

`types_index.py --validate`: 11 peer OPUS type rows carried
`SEMANTICALLY IDENTIFIED - <prose>` in the ladder-only readiness column; trimmed
to the rung (prose already lived in instance/evidence; AB30's moved to evidence).
Validator now 0 errors.

Gate state after this batch: gap debt `TOUCHED 0 / AMBIGUOUS 2 / UNMEASURED
631 rows (25,282 B)`; width checker clean; validator clean. Remaining debt is
the uncensused tail plus the two AMBIGUOUS CPostEffect spans (5F0/670).

NEXT: DONE — published `903420ec7` (task `SWE2STRUCT-PUB-ROUTECENSUS-0930`
finished). Fallback continues: 631 UNMEASURED rows / 25,282 B remain, plus two
AMBIGUOUS CPostEffect spans (+0x5F0/+0x670).

## Route-seeded census batch 2 — the whole seedable remainder, 2026-09-30 (SWE2-STRUCT)

`sweep_route_seeded_census.py` gained the same fail-closed guard as the
single-type tool (it crashed `len(None)` on the first unseedable route; the
UNSEEDABLE path prints and skips, and child-projections guard their own
accumulator). A full sweep over all 422 routed types showed **zero refuted gap
rows** — the CPostEffect wave had already caught everything the instrument
falsifies — and 25 UNSEEDABLE routes.

Drove `gen_route_seeded_census.py` in-process (shared Image/call_maps) over
every non-empty unregistered seedable type: **143 census files emitted** and
registered. Three produced nothing (WorldLootPickupList EMPTY, two
UNSEEDABLE). Consequences adjudicated the same pass:

- 4 TOUCHED rows re-cut, finer than the sweep's ≥256-byte gap filter sees:
  ManagerSub7EA0Entry +0x000→`vector000` float[4] + `word0010`/`byte0013` carves
  (20 sites over +0x0..+0x13); MapLightingTuning +0xAC/+0xBC → named floats
  (1.0f/0.1f init writes); PDeferredLightingBase +0x4110..+0x4127 →
  `dword4114`/`qword4118`/`qword4120` (~90 compare/load sites).
- 38 `WIDTH DELIBERATE:` markers on the resulting width mismatches — all
  legitimate mixed-width (qword pair-inits over named floats, byte bit-tests on
  flag dwords, scalar movss reads of float4 elements, packed writes over
  byte rows); each marker cites the sustaining sites.

Gates after: `check_census_widths` 0 mismatches; `check_gap_debt` TOUCHED 0 /
AMBIGUOUS 2 / INHERITED 1 (both non-defect classes); `types_index --validate`
0 errors. UNMEASURED gap debt: **448 rows / 23,818 bytes** — down from
838 / 35,519 at session start. Remaining: unrouted types and the five orphan
bases the sweep printed (GroupPersistentBank +0x80, RampChannelRecord +0x120,
ResourceKindOverrideTable +0x40, SeparationCellMasks +0x40,
TransformWorkbenchSavedValue +0x10 — candidate sub-objects).

NEXT: DONE — published `1bd0d2d6` (task `SWE2STRUCT-PUB-ROUTECENSUS2-0930`
finished, lease released rev 44681). All seedable routed types now have
censuses. Fallback: investigate the five orphan bases named above as
candidate sub-object declarations, then unrouted-type coverage.


## 2026-10-01 — SWE2-STRUCT: SD-141 receiver/consumer trace (OPUS-REQ-STRUCT-SD141-CONSUMERS-1001)

Verified OPUS's `sd141-gpu-consumers-1001` chain and completed the CPU-side census it left open.

- `r14` in `00604750` = mapped CPU view of a D3D11 ring-buffer slot
  (`006097B0` busy-wait + `00626060` map; commit `0062C300`); record =
  `this+0x4A8 + cursor*80`. Per UQ-22: `SceneWideParameterConstantBuffer`,
  `+0x5D4`/`+0x5DC` = `mShadowFlyingFadeSpeed`/`mShadowFlyingFadeRange`.
- `r14` is write-only on CPU (291 stores, 0 non-lea loads); consumers are
  GPU-side only (517 lit-shader blobs per OPUS's blob census).
- The two staged slots (`this+0x4E0`/`+0xA78`, parity-indexed by `+0x4D8`)
  take the pair bytes at `+0x550`/`+0x554` in whole-struct copies, but **no
  CPU reader exists** — `00604750` is the only `imul ×0x598` site and no
  same-receiver operand hits `+0x1030`/`+0x15C8`/`+0x1034`/`+0x15CC`.
  Write-only staging for the pair bytes.
- `00604750` entry is indirect (a `.rdata` rva32 jump-table arm at
  `0x6048D0`); both raw rel32 caller candidates decode mid-instruction.

Record: `_index/candidates/swe2struct-sd141-receiver-1001/` — checker
`sd141_receiver.py` FAILS 0 (C1..C10).

NEXT: DONE — `OPUS-REQ-STRUCT-SD141-CONSUMERS-1001` finished (rev 44768),
published `911aff55b`.

## 2026-10-01 — SWE2-STRUCT: the five sweep "orphan bases" resolved — all register-bias artifacts

Each orphan folded back inside an already-declared row via a biased base
register (disp column already carries the folded offset):

- GroupPersistentBank base+0x80: `[rax-0x80..rax]` movups import/export loop
  tiles the 512B blob (eff +0x00..+0x70 inside `bytes`).
- RampChannelRecord base+0x120: `003B68E2 and byte [rax-0xE0],0xFE` →
  elem+0x40 = `field040` (PARRAY stride 0xE0).
- ResourceKindOverrideTable / SeparationCellMasks base+0x40: zeroclear qword
  loops with `[rax-0x28..-8]` → +0x18..+0x38 inside the blob rows.
- TransformWorkbenchSavedValue base+0x10: `[r9-0x10]` → +0x00 inside
  `savedBytes[16]`.

No candidate sub-objects exist among them — the `report_bases` orphan list is
exhausted. Fallback continues: unrouted-type coverage (types with no route
column cannot be census-seeded) and the standing transitive-return consumer
limitation.

## 2026-10-01 — SWE2-STRUCT: derived-route census batch — RenderContext subtree unlocked

`RenderContext02CC0410` gained `STATIC 0x02CC0410` (ctor 005FD050 lea's the
.bss static in place), which seeded the whole EMBED/CHAIN subtree already
declared on the children:

- `render-context-02cc0410-accesses.tsv`: 649 accesses / 414 offsets / 23 fns,
  0 gap-rows hit, every base resolves to a declared row. Driven in-process —
  the size is a range (AT MOST 0x22200), outside `store()`'s sized map.
- `render-primitive-pass-1e8-accesses.tsv`, `render-context-pass-state-block-accesses.tsv`,
  `primitive-renderer-d3d11-accesses.tsv` (184/168/5, also via the ranged-size
  driver at AT MOST 0x20940).
- `p-shader-pass-state-d3d11-accesses.tsv` (EMBED RenderPrimitivePass1E8 +0x058).
- `p-post-effect-base-accesses.tsv` (CHAIN PDeferredLightingBase +0x000;
  VTABLE-routed parent).
- `PFXAAD3D11` (EMBED PFXAA +0x000): empty — no displacement reached. Not
  registered.
- `NameRegistryNode` (CHAIN InputNameRegistryHeadCell +0x000): 242 accesses,
  all generic `mov [reg],reg` stub propagation — a true containment fact but
  a FALSE census. Route kept, census deleted.

Eight `WIDTH DELIBERATE` markers: seven RenderContext ctor bulk stores
(word/qword merges over byte/dword fields) and `PPostEffectBase +0x48`
(declared 8 to the type end; all five routed accesses dword — the row
already recorded the split).

Gates: `check_census_widths` 0 mismatches; `check_gap_debt` TOUCHED=0,
INHERITED grew to 7 (parent/child shared-code reads — the expected class);
`types_index --validate` 0 errors. UNMEASURED now **411 rows / 23,423 B**.

NEXT: DONE — published `8cc4b2781` (task SWE2STRUCT-PUB-ROUTECENSUS3-1001,
rev 44852). A first invocation with swapped `publish_paths.sh` args produced
`efdf7f714` (adds only `_pub3_msg.txt`) — superseded, harmless.

Continue unrouted-type coverage — remaining tractable work is thin; most of
the 350+ unrouted types are caller-owned / interior / engine-allocated with
no honest root. Standing limitation: transitive getter-alias consumer census.

## 2026-10-01 — SWE2-STRUCT: ARG route form implemented + piloted, ruling requested

`ARG <reg> 0xFUNC` (object provably in <reg> at FUNC entry — the grammar
proposed in `derived-route-parent-roots.md`, FRONTIER's to accept or refuse)
is now implemented in `gen_route_seeded_census.py`: `R_ARG` parse, `ARG` in
`SEEDABLE`, `hosts_for` returns the named function, walker seeds
`W.ARG_REGS[idx]` at offset 0 — the VTABLE shape with a named register.

Pilot (in-process driver, routes injected to the store map — `types.tsv`
untouched pending the ruling):

- `ActorDefinitionPayload` `ARG rdx 0x0026C8C0`: 7 offsets — the binder's own
  field reads.
- `AuthoredExpressionBlock` `ARG rcx 0x0042FDB0`: 21 offsets — re-derives the
  four-record layout + mode byte.
- `AuthoredExpressionRecord` EMBED child: 6 offsets (redundant — parent census
  already covers the same bytes).
- `ActorDefinitionCountedU16Section` RELOFF child: 0 offsets — the
  parent+*(int32*)(parent+off) combine is not modelled under ARG; not emitted.
- `PaneListWidget0B68`/`PaneSlotWidget0160`: already censused — not run.

Record: `_index/candidates/arg-route-form-pilot-1001/README.md`. Board:
`SWE2STRUCT-REQ-FRONTIER-ARG-ROUTE-RULING-1001` (rev 44929) requests the
accept/refuse verdict; on acceptance the three `DYNAMIC - ... ARG proposed`
rows gain real routes and the two pilot censuses publish.

NEXT: awaiting FRONTIER ruling on ARG. Fallback meanwhile: unrouted-type
coverage remains thin (caller-owned / interior / engine-allocated dominate);
transitive getter-alias consumer census remains unsupported/known debt.

## 2026-10-01 — SWE2-STRUCT: seedable frontier probed to closure

Drove all **152 direct-seedable types lacking a registered census** through an
in-process driver (cached `Image`/`call_maps`, every SEEDABLE rule per row):
**0 produced a non-empty census.** The batch-2/3 emitters already captured
every type the current grammar can actually measure; the remaining seedable
rows are objects whose code reaches them only through bases the walker cannot
prove (rip-addressed reads outside marked registers, or no displaced access
at all). No route pruning — an empty census doesn't falsify the root; the
route rows stay as provenance.

Frontier state after `2609c0d85`:

- Gates: widths 0 mismatches; gap-debt TOUCHED=0 / AMBIGUOUS=2 (non-defect) /
  INHERITED=7; types_index 0 errors. UNMEASURED 411 rows / 23,423 B.
- The remaining UNMEASURED debt sits in unrouted/unseedable types (VP8, Lua
  GC objects, caller-owned/interior/engine-allocated) — no honest root under
  the current grammar.
- Pending external: `SWE2STRUCT-REQ-FRONTIER-ARG-ROUTE-RULING-1001` (the only
  untried lever — argument-register roots); `ASTRA-RETURN-STRUCT-OV58D-ORDER-
  SWITCH-1001` gated on `ASTRA-REQ-SPEC-OV58D-ORDER-SWITCH-1001` (still READY).

NEXT: awaiting the ARG ruling — if accepted, apply the three routes and
publish the two pilot censuses. Standing limitation: transitive getter-alias
consumer census remains unsupported/known debt. Queue otherwise empty for
this lane; monitor the board.

## 2026-10-01 — SWE2-STRUCT: ARG routes applied under the ruling

FRONTIER ruled `SWE2STRUCT-REQ-FRONTIER-ARG-ROUTE-RULING-1001` DONE —
**ACCEPT-WITH-CONDITIONS**: cite the in-body instruction per row, caller-side
binding stays prose, rcx/rdx/r8/r9 only, zero-yield child combines not
emitted, no retro-labelling. Applied:

- `ActorDefinitionPayload`: `ARG rdx 0x0026C8C0` (cites 0026C8F7 `mov r15,rdx`
  / 0026C95A `mov [rdi],rdx` → ActorManagerSlot +0x00). Census
  `actor-definition-payload-accesses.tsv`: 7 accesses / 7 offsets / 1 fn —
  the binder's own field reads, all base+0.
- `AuthoredExpressionBlock`: `ARG rcx 0x0042FDB0` (cites 0042FDC1
  `movzx ecx,[rcx+0x40]` + four `call 004314E0` on rcx+0x00..+0x30); size
  UNRESOLVED → `AT LEAST 0x41` (the body's own reach). Census
  `authored-expression-block-accesses.tsv`: 76 accesses / 21 offsets / 5 fns —
  all rows `exposed` (the decoder family is widely-called), so reachability
  evidence only, no width evidence.
- `AuthoredExpressionRecord`: rides the parent's ARG through its declared
  EMBED — 25 accesses / 6 offsets, all `exposed`. Registered.
- `ActorDefinitionCountedU16Section` RELOFF child: 0 offsets under ARG — not
  emitted, per condition 4.
- `PaneListWidget0B68`: route adopted `ARG rcx 0x0029BE50` (cites the pool
  allocator's handler argument 00296502). Verification run reproduces the
  registered census as a near-superset (108 vs 21 offsets); registered file
  stands.
- `check_route_verb_against_image.py`: ARG operand now checked as a function
  extent (`ARG VERBS NAMING NO FUNCTION` — silent zero-host typo guard). All
  three rows pass.

Gates: widths 0 mismatches; gap-debt TOUCHED=0 / AMBIGUOUS=2 / INHERITED=7 /
UNMEASURED **408 rows / 23,371 B** (was 411/23,423 — the three censused types'
gap rows moved to measured); types_index 0 errors; verb check 374 supported /
1 baseline-contradicted (BattleUnit SLOTPTR, pre-existing) / ARG all resolved.

NEXT: OV58D return still gated on ASTRA-REQ-SPEC-OV58D-ORDER-SWITCH-1001
(ACTIVE under AUDIT-SPEC — dependency may clear soon). Seedable frontier
closed; remaining UNMEASURED sits in unrouted types. Standing limitation:
transitive getter-alias consumer census.

## 2026-10-01 — SWE2-STRUCT: OV58D order-switch repair applied

`ASTRA-RETURN-STRUCT-OV58D-ORDER-SWITCH-1001` — ASTRA's accepted packet
(`_experiments/evidence/ov58d-order-switch/`, SPEC review ACCEPT) refuted my
caller-cone's one-stage switch decode. Repaired additively (strike +
correction, originals preserved):

- `CALLER-CONE-0030E360-0930.md`: the `0x4049`/`0x404A → 002FDF18/5A →
  r8b=0xF8/0xD9 → OUT OF CONTRACT` claims struck. Correct two-stage decode
  recorded (selector byte `002FE54C+idx`, arm RVA `002FE534+4·sel` — verified
  byte-wise here: 0x4049/4A → sel 1 → `002FDE7B`, a 29-byte local arm with no
  call). Real status-arm domains: `0x4051–0x4070`/`0x4071–0x4090` → `id 0..31`.
- `RESIDUE-BOUNDS-0930.md`: the "contract falsified twice" update struck;
  net state = every identified caller passes `id ≤ 31`, the named reach
  stands only as callee-level code fact (index unmasked).
- Independent rechecks: selector/arm tables read from the image; `002FDE7B`
  disassembled (no `0030E360` call — matches the packet).
- Scope kept per the task: no generic `0030E360`/all-caller/lifetime safety
  claim; if another unbounded caller is later found, its provenance goes into
  the record first. Frozen vendored copy under `status-recursion-index-bound/
  dependencies/` intentionally left (dependency preimage).
- Consumers: FABLE's T3b named-reach exception and OPUS's bounded-arg use are
  their own RETURN tasks; OPEN-QUESTIONS OV-5/OV-8 wording is FABLE's.
- Also landed this round: `OPUS-REQ-STRUCT-AWNB-TYPES-1001` at `6bec973bb`
  (types.tsv = HEAD + TS-2/TS-3; the 21-row CSV quoting rewrite reverted —
  all cells unquoted byte-identical to HEAD, plain-split readers dominate).

NEXT: publish the record repairs, finish the RETURN task. Seedable frontier
closed; ARG routes committed at `05cf6d3b5`. Standing limitation: transitive
getter-alias consumer census remains unsupported/known debt.

## 2026-10-02 — SWE2-STRUCT: interior-offset leads 21->0

`OPUS-REQ-STRUCT-INTERIOR-OFFSET-LEADS-21-1001` — all 20 still-open leads
ruled (PhyreClassDescriptor +0xF4 dropped out: a peer split it into
parentChainOffsetSum/Clamped/flags before the task landed). Verdicts per
site-level read of every flagged access:

- PER-PATH UNION (8): EncodedIdQueryRecord +0x04/+0x20/+0x24/+0x28/+0x2C/
  +0x30/+0x38 (tagged per-class views; the WORD+6 `id` overlay row already
  existed), WidgetSingleton02CA99C0 +0xD0 (qword store vs dword reads —
  pointer-ness not established).
- RULED FALSE (1): MapRefWeatherBlock +0x0 — the interior byte is
  MapRefWeatherLane.publishedByte, already declared on the nested type.
- SPLITS (11): Manager0209AC60 +0x3E0 -> word03E0 i16 + word03E2 u16
  (movsx/movzx reads, no dword reader); ManagerSub0209AC60_02F8 +0xC8 ->
  byte00C8 i8 + byte00C9 u8 (zero word-width accesses); MapScreenContainer
  +0xA1 -> byte00A1 + byte00A2; PApplication +0xD38 -> modeDword38/3C
  (+0xD3C takes 001DE570's return at 0079856F); PpfxInitDescriptor six u64
  rows -> dword pairs (readers address the dwords individually);
  WidgetSingleton02AED490 +0xE6 -> byte00E6 + byte00E7 + word00E8.
- WIDTH DELIBERATE prose carried on every split row whose base still takes
  a wider covering store (qword/dword/word bulk init).
- Gates: check_interior_offsets exit 0 (15 adjudicated, 0 open, control
  holds); types_index --validate 0 errors/0 gaps/0 reviews; leads file
  regenerated. check_census_widths shows 1 baseline mismatch
  (RenderResourceEntryBank pageHead — peer row from a73cdc0cf, owner's call).

NEXT: DONE — published `149926294` (tasks SWE2STRUCT-PUB-INTERIOR-LEADS-1002 +
OPUS-REQ-STRUCT-INTERIOR-OFFSET-LEADS-21-1001 finished, revs 46944/46945).
Unrouted-type frontier unchanged; board check for the next unblocked package.

## Resume state - SWE2-STRUCT, 2026-10-03 09:08Z, Claude stand-in for Devin

- **STAND-IN CHECKPOINT 2026-10-03 17:00Z (Claude stand-in for Devin, session bb063a3a; read this first; supersedes the 16:15Z bullet).** Since 16:15Z: `f945d05b2` SpawnCandidateRecord (0x30; mode +0x00, position +0x10) - the format-class-0 candidate record CONTRACT-spawn-placement section 3 names, read through 003DFD00 / 00234AF0 / 002374E0. The store is clean at HEAD (the peer overlay was committed). Open: none. Queue watcher `Tools/work/SWE2-FRONTIER/standin1003/queue_watch.py`; fleet plan holds all 8 lanes until Devin starts (release with `hold_plan.py ""` in the stand-in scratchpad). Publish tools per lane: `Tools/work/<LANE>/standin1003/` (bop.py, mkpub.py, pub_runner.py); splices: `Tools/work/SWE2-FRONTIER/standin1003/splice_pub.py` (one dirty path) or `splice_pub_multi.py` ("PATH1;PATH2"; apply your edit to the worktree first - the saved copy is restored).

Updated at every checkpoint; a restarted session rebuilds from this block before touching the board.
**Written by a Claude session standing in for the Devin SWE2-STRUCT session (fish-jupiter) while Devin was
rate-limited (2026-10-03 ~00:18Z-07:39Z). Everything below is DONE and on the board - do not redo any of it.**

- **Identity:** SWE2-STRUCT (fixed).
- **Before the stand-in:** the interior-offset leads batch was already published at `149926294`
  (SWE2STRUCT-PUB-INTERIOR-LEADS-1002 + OPUS-REQ-STRUCT-INTERIOR-OFFSET-LEADS-21-1001 DONE). SWE2-CONTRACT's held
  AUDIT-LOG section landed after it (`097a3a739`), so nothing of STRUCT's was parked.
- **Published by the stand-in: `b9b821cda`** (13 files, one lease, PUB task SWE2STRUCT-PUB-SUSPCOPY-1003 DONE):
  - `OPUS-REQ-STRUCT-SUSPEND-COPY-CENSUS-ROWS-1001` DONE, under `SWE2-STRUCT-SUSPCOPY-CENSUS-1003` DONE. All 14 copy-loop
    tail rows in battle-unit-accesses.tsv were re-filed from +0x730..+0x790 to +0xB30..+0xB90 (OPUS named 2), and
    the 18 loop rows annotated "loop pass 0 of 9" (loop unfollowed). The BattleTargetBuffer (-4) and
    BattleTargetResultEntry (+12) censuses were regenerated with project_embed_census.py. fields.tsv
    +0x746/+0x75A/+0x760/+0xB94 were re-cited. Record + regression: `_index/candidates/swe2struct-suspcopy-census-1003/`
    (loop_attribution_check.py --check FAILS 0; FAILS 2 on the old census).
  - `OPUS-REQ-STRUCT-ACTOR-READINESS-LINES-1002` (2 edits), `OPUS-REQ-STRUCT-RESOURCE-A-READINESS-LINES-1002` (7) and
    `OPUS-REQ-STRUCT-RENDER-A-READINESS-LINES-1002` (8) are DONE: OPUS's edits were applied unchanged after each
    deciding address was re-read at the bytes, and none is disputed. Record:
    `_index/candidates/swe2struct-readiness-apply-1003/README.md`.
  - AUDIT-LOG section "2026-10-03 SWE2-STRUCT - suspend/restore copy loop census rows re-attributed".
- **Routed by the stand-in (waiting on others, nothing for STRUCT to do):**
  `SWE2STRUCT-REQ-OPUS-FIELDMAP-SUSPCOPY-SITES-1003` -> OPUS (the field map's +0x730..+0x790 rows still cite the
  tail sites; exact replacements are in the request). `SWE2STRUCT-REQ-FRONTIER-CORRECTION-GATE-TSV-AFFECTED-1003`
  -> SWE2-FRONTIER (publish_correction_gate counts only .md files as touched, so a record's `affected:` line naming
  a touched TSV is always refused; the stand-in's record lists its TSVs in prose as a workaround).
- **Design note (user task via FABLE, 2026-10-03):** per-package and integration readiness views (addendum §12/§13/
  §16 P2 item 15), `_index/candidates/swe2struct-design-readiness-views-1003/README.md`, published in the commit whose
  subject starts "SWE2-STRUCT: design note - readiness views". The sha was sent to FABLE. It is design only, not
  implemented; it lists the open points for FABLE (§6 criteria) and DATA (adapter) - nothing for STRUCT to redo.
- **FABLE ruled on the design note (ACCEPT + refinement) and asked for the build - DONE (stand-in):** amendment section 11 + build
  `Database/Tools/analysis-kit/gfz-scripts/readiness_view.py` + `test_readiness_view.py` (10 OK) + `HOOK.md`, published in the
  commit whose subject starts "SWE2-STRUCT: readiness view built". Hook routed to SWE2-FRONTIER as
  SWE2STRUCT-REQ-FRONTIER-READINESS-VIEW-HOOK-1003; STRUCT does not edit the dashboard code. Nothing to redo.
- **OPUS-REQ-STRUCT-SYSTEMSTOP-08-1003 - DONE (stand-in):** the SystemStopRecord +0x08 type row was corrected (builder 00227680 stores it in
  both records; qword08 uint64 TYPE RESOLVED), record `_index/candidates/swe2struct-systemstop08-1003/`, published in the commit
  whose subject starts "SWE2-STRUCT: SystemStopRecord +0x08".
- **OPUS's hygiene items + the census bank-B gap - DONE (stand-in, coordinator's instruction not to defer):** 48 Widget-base copy rows,
  14 rung-lag field rows + type RenderResourceEntry (`_index/candidates/swe2struct-type-hygiene-1003/`), and the EMBED element-fold
  fix in gen_route_seeded_census.py with the SystemStopRecord census regenerated (`_index/candidates/swe2struct-census-embed-fold-1003/`),
  published in the commit whose subject starts "SWE2-STRUCT: type-store hygiene". FOLLOW-UP for STRUCT (not urgent): regenerate the
  other EMBED-array censuses this generator writes and diff each (impact table in the census record).
- **Current package/claim:** none - every STRUCT task the stand-in touched is DONE; no STRUCT claim is ACTIVE.
- **Exact next action:** query the board (`team.py show --agent SWE2-STRUCT`) for new requests. If an answer to the
  routed OPUS request comes back disputed, re-check it against `loop_attribution_check.py`. Otherwise take fallback work.
- **Pending requests/reviews:** none addressed to STRUCT at 2026-10-03 02:20Z.
- **Fallback eligible work:** the unrouted-type frontier (unchanged); census width-blind spans
  (`check_width_blind_spans.py`: 38 covered spans fleet-wide, rows whose REASON should say CARRIED).
- **Latest coherent commit:** `b9b821cda`.
