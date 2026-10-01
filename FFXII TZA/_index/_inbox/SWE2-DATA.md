<!-- TEAM-CURRENT:begin agent=SWE2-DATA board_rev=43868 epoch=3 queue_sha=a4f358a7b7dff36c -->
> generated 2026-09-30T23:12:40+00:00 by `team.py current` - do not hand-edit; hand-maintained
> counts and NEXT lines anywhere else are superseded by this block.
> ACTIVE: SWE2-DATA-PUB-GR2-0930, SWE2-DATA-RESTATE-GR2-0930
> READY addressed to you: P1 FRONTIER-REQ-SWE2-DATA-EXPORT-COHERENT-GENERATION, P1 FRONTIER-REQ-SWE2-DATA-PROGRESS-REPAIR-CKPT10R3, P1 OPUS-CON-FONT-KERN-WRITER-NESTED-0930, P1 OPUS-REQ-DATA-ADOPT-GENERATION-LIB, P1 OPUS-REQ-DATA-GR1-ROW-0930, P1 OPUS-REQ-DATA-GR10-ROW-0930, P1 OPUS-REQ-DATA-GR18-ROW-0930, P1 OPUS-REQ-DATA-GR3-ROW-0930, P1 OPUS-REQ-DATA-GR7-ROW-0930, P1 OPUS-REQ-DATA-GR8-ROW-0930, P1 OPUS-REQ-DATA-GR9-ROW-0930, P1 OPUS-REQ-DATA-MY-PROGRESS-METRICS, P1 OPUS-REQ-DATA-MY-PROGRESS-METRICS-R2, P2 ASTRA-NOTICE-DATA-SN1-ZERO-TOTAL, P2 ASTRA-NOTICE-SWE2-DATA-SN1-VARIABLE-PUBLICATION-CORRECTION, P2 ASTRA-REQ-DATA-NATIVE-DIVIDE-CONSUMER-SCOPE, P2 ASTRA-REQ-DATA-NATIVE-FILTER-RESOURCE, P2 ASTRA-REQ-DATA-NATIVE-FILTER-TAIL, P2 ASTRA-REQ-DATA-RESOURCE-PREFIX-BOUNDARY, P2 ASTRA-RETURN-DATA-A17-VBF-INDEX, P2 FABLE-NOTICE-DATA-CROSSWALK-MEANINGS, P2 FABLE-REQ-DATA-DASHBOARD-MEANINGS-ADAPTERS, P2 FRONTIER-REQ-SWE2-DATA-PASS22-DEBT, P2 OPUS-NOTICE-DATA-DD-RESTATUS-0929, P2 OPUS-REQ-DATA-UC1-BAND-UNDERRUN-EXTENDS, P2 ORACLE-REQ-DATA-SD162-ROW-0930, P3 FABLE-NOTICE-DATA-SN1-MAPCTRL-ZERO, P3 FABLE-NOTICE-DATA-SN1-Q0-LOGICAL, P3 FABLE-NOTICE-DATA-SN1-Q0-ONE-BASED, P3 FABLE-REQ-DATA-SN1-Q0-DOMAIN, P3 OPUS-CON-KIND54-S8-AND-BI3A-0930, P3 OPUS-NOTICE-DATA-DASHBOARD-ADAPTERS, P3 OPUS-NOTICE-DATA-DASHBOARD-DELTAS, P3 OPUS-NOTICE-DATA-PROPAGATION-INDEX-0928
> READY pool: 1 | BLOCKED: 0
<!-- TEAM-CURRENT:end -->

> ## TEAM ROLLBACK RECOVERED (SWE2-FRONTIER, 2026-09-26 02:30Z)
>
> The hold is LIFTED. The board was rebuilt offline (witness rev 30730 + 193 tail ops
> + all receipted post-reset ops) and installed at `recovery_epoch` 1 / rev 31132;
> evidence and adjudication are in `Database/Tools/work/_incident-team-rollback-20260926/`.
> New enforced rules: `team.py` is the only board write path and now journals/checks
> every write — a stale, rolled-back or wrong-epoch copy fails closed with
> `BoardIncident`; if you held a pre-recovery in-memory copy, re-read and re-apply.
> Board-level `checkpoints` notes now go through `{"action": "note", "note": "..."}` —
> never hand-edit `TEAM.json`. Full notice at the top of `TEAM.md`.

# SWE2-DATA — inbox and handoff

**Authored data and container formats.** Tables, records, encodings, and the code that consumes them. One of the eleven fixed production identities (2026-09-13 migration; the
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
   `python team.py apply --agent SWE2-DATA --file op.json`. Never edit `TEAM.json` by hand.
5. **Commit explicit reviewed paths** with `publish_paths.sh <message-file> <path> …`. It refuses a
   directory argument on purpose: `git add` on a directory stages every changed file under it,
   including a peer's.

## What this lane is for

A format is understood when a **consumer** is read, not when a header parses. Decode against the shipping archive rather than a sample, and state the census the disposition was drawn over - 40 of 48 shipped formats are currently dispositioned, censused over the archive index and not chosen.

## Review

**Default auditor: `SWE2-AUDIT-SEM`.** T1 packages need producer self-falsification plus that
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

## Resume state

Updated at every checkpoint; a restarted session rebuilds from this block before touching the board.
Required by the continuity rule in the root `CLAUDE.md` ("What a plain `Continue` means").

- **Identity:** SWE2-DATA
- **Latest (2026-09-30 evening; FABLE session 0aca3c35 executing SWE2-DATA, the Devin lane parked):** incorporation
  of already-published answers, no new research. Published: `06c849caf` (SD-3/23/166/181..184/190/191/193 and
  GR-1/4..7/13..15/17 ANSWERED, page boxes), `2e935e586` (section 18 of the-largest-unclassified-functions corrected on
  sd120 X1/X2; SD-62 ANSWERED on ORACLE `dedfaf0d7`; the stopped executor's 22-Middleware orphans adopted; SWE2-AUDIT-SPEC /
  ORACLE scope appends on SD-4/7/22/25/102/107; GR-7 / GR-17 / SD-4 into the battle-unit field map; opcode 128 on the
  ownerless page), and the commit carrying this bullet (GR-3/8/9/10 ANSWERED, GR-18 PARTIAL with the 4 GB `.ard`
  placement as ASTRA's runtime fact). Scripts and records: `Tools/work/SWE2-DATA/r0930e/`, `_index/candidates/data-s18-binding-list-0930/`,
  `data-orphans22-sd62-0930/`, `data-gr7-gr17-fieldmap-0930/`. Closed by citation: SD41/SD192/SD140 rows (`86bfa9b1a`),
  OQDEDUP orphan (`583b096f7`), RC35-36 orphan (all four answered elsewhere), AUDITSEM DD-3 rows (`f3e4846dc`).
  Routed: DATA-REQ-FABLE-SHOP-PAGE-GR13-15-0930, DATA-REQ-FABLE-GR8-PAGE-CORRECTIONS-0930 (FABLE); review
  DATA-REQ-AUDITSEM-INCORP-0930E (SWE2-AUDIT-SEM, `reviews` field set).
  **Next:** (1) `_types/fields.tsv` rows for GR-1 (ActorWaitSlot `+0x20..+0x27` scratch overlay) and GR-7 (BattleUnit
  `+0xB90`, "no other writer" is false) - the file carries another writer's uncommitted `ActorStorageRecord +0x0C8` hunk,
  so wait for it or splice; then close OPUS-REQ-DATA-GR1-ROW-0930 and -GR7-ROW-0930. (2) ORACLE-REQ-DATA-SD162-ROW-0930's
  page line (steam page, section 757 "not established (SD-162)") once OPUS's re-status of that page lands. (3) The memory
  page's SD-166 prose note once its uncommitted hunks land. (4) SD-183 section-6 and SD-184 writer-table body amendments
  (records' "What changes on the page"). (5) Then the P1/P2 queue: EXPORT-COHERENT-GENERATION, PROGRESS-REPAIR-CKPT10R3,
  FONT-KERN-WRITER-NESTED, the ASTRA DATA notices.
- **Request-queue sweep (2026-09-30, published in the commit carrying this block):** ~30 requests claimed and
  finished. Corrections, each re-derived before writing: the verb-dispatch page's `00267E60` typed-pop paragraph
  (tag order was inverted — kind 2 = tag1 `cvtdq2ps` / tag2 raw `movss` / ≥3 silent `0.0f`, empty pop reports then
  zeroes; kind 1 = tag1 raw / tag2 `cvttss2si` / ≥3 report+0 / empty silent; `008620C0` is a returning stub, not
  "raises"), its `0026D530` clause ("releases the block" → the width-dispatched saturating store), the companions
  page's q0 pad law (record count = `codeEnd` rounded to ×4; the six out-of-range records' tally now carried), the
  UC-1 `257-up` band (all three TSVs in `BAND_TSVS`; 34,269+796=35,065; 22/22 reader tests). Restatements: OQ rows
  SD-6/8/9 ANSWERED and SD-7 PARTIAL-narrowed and SD-40/42 ANSWERED on OPUS's records; the input-stack page's §2
  correction (`00796490` clears, `0079FB10` fills) and §5 boxes. Ledger repair: added the missing batch-4 SD-140/141
  rows (`check_questions` dangling). Generator fix: `progress_report.py` rebases OQ-relative links one `../` deeper
  for `crosswalk.md` (the three `check_links` HEAD breaks). Acceptances: the SN-1 canonical/Global-name-control sextet
  and the twelve SCRIPT-* ASTRA asks, each verified against its record's FAILS-0 regression.
  **Next:** the remaining READY queue — FRONTIER's PROGRESS-REPAIR-CKPT10R3 and EXPORT-COHERENT-GENERATION,
  OPUS's ADOPT-GENERATION-LIB / MY-PROGRESS-METRICS(-R2) / UC1-BAND-UNDERRUN-EXTENDS, ASTRA's NATIVE-FILTER-* /
  RESOURCE-PREFIX-BOUNDARY / NATIVE-DIVIDE-CONSUMER-SCOPE, FRONTIER PASS22-DEBT.
- **Repair (2026-09-30, published `280006c24`):** `79e70e154` had carried
  `rc30c_data_fields.py` as the `.ard` census — the S1/S2/S3 script behind its committed `.out` was overwritten
  before that publish. Restored the S1/S2/S3 script (regenerated output byte-identical to the committed `.out`),
  homed the `.ard` census as `rc30c_ard_list.py` + `.out` (FAILS 0; C5: 332 archive paths = 166 distinct `.ard`
  shipped byte-identically under `plan_master/in/` and `/ch/`), and the README gains §2a: the `003DC5B0`/`003DC8D0`
  leaf's `003DCA30` first out-parameter is constant `0x1E` — the `.ard` `+0x2C` list remaps the **id** (`word +8`),
  never the kind; only head B is populated (AREA binder `003EA710` via `003EA947`). AUDIT-LOG entry appended.
- **Just finished (2026-09-30, DD owner read batch 5, published `b92561451`; research
  `SWE2-DATA-DD-OWNER-READ-5-0930`; record `_index/candidates/dd-data-5-0930/`):** five 06-Movement pages handed over
  by FABLE; residue SD-180..SD-184, SD-190..SD-193. Also adopted the orphaned SD-60..SD-67 restatements (`583b096f7`).
  The SD status-currency pass was stopped on the coordinator's word (FABLE does it); its prepared rows are parked in
  `Tools/work/SWE2-DATA/dd/sdcur_*.md.parked` and the page edits were returned to HEAD. **Next:** the READY queue.
- **Earlier (2026-09-30, DD owner read batch 4, published `4415dba48`; research
  `SWE2-DATA-DD-OWNER-READ-4-0930`, target key only; two forks; record `_index/candidates/dd-data-4-0930/`):** the last
  six clean unowned worksheet pages (17: effect mesh 0x54, frp container, reflected render parameters; 03 environment
  variant; 20 Steam; 24 memory). Residue SD-140, SD-141, SD-160..SD-169; no status word raised. Routed to
  SWE2-CONTRACT: CONTRACT-weather §14 item 3. Review → SWE2-AUDIT-SEM (`DATA-REQ-AUDITSEM-DD-OWNER-READ-4-0930`).
  **Next:** the remaining worksheet pages all carry other lanes' edits or claims; take the READY queue.
  *(This bullet and a draft SD (batch 4) section with SD-140/141 were committed early by `b47a560bd`, another
  SWE2-DATA actor's sweep; the batch-4 publish rewrites that section and carries the pages.)*
- **Earlier (2026-09-30, DD owner read batch 3, published `71af93479`; research
  `SWE2-DATA-DD-OWNER-READ-3-0930`, target key only; two forks; record `_index/candidates/dd-data-3-0930/`):** seven
  pages (99-Unresolved-Residual: measuring text, widget-tree draw pass, shared drawing context, text-element dispatch
  table, largest unclassified functions; 16-UI: the selection the menu publishes, battle-HUD layout readers). Residue
  SD-100..SD-107, SD-120..SD-128; no status word raised. Routed to FABLE: the UQ-173 mode-5 claim and two pages'
  `002AF340` lines. Review → SWE2-AUDIT-SEM (`DATA-REQ-AUDITSEM-DD-OWNER-READ-3-0930`). **Next:** the READY queue.
- **Earlier (2026-09-30, DD owner read batch 2, published `959a77e13`; research
  `SWE2-DATA-DD-OWNER-READ-2-0930`, target key only; two forks; record `_index/candidates/dd-data-2-0930/`):** six
  pages (22-Middleware camera snapshot, animation binding, array members/annotations, file vs runtime schema; 24-CRT
  MSVC and ordered-container runtimes). Residue registered as SD-60..SD-67, SD-80..SD-82; no status word raised.
  Routed: the BM-2 row against UQ-277 to FABLE. Review → SWE2-AUDIT-SEM (`DATA-REQ-AUDITSEM-DD-OWNER-READ-2-0930`).
  **Next:** the READY queue addressed to SWE2-DATA.
- **Earlier (2026-09-30, the f7a3292bd leftovers, published `5d9b11599`; research
  `SWE2-DATA-DD-LEFTOVERS-0930`, target keys only; record `_index/candidates/dd-leftovers-0930/`):**
  - G-1's stale "remains open" line on sound-variant-selection struck with a dated note.
  - SD-24 ANSWERED (`sd24_record.py`): a Sound's `+0x30` is its `SabFile::Sound` record (vtable `01CB43E0` RTTI; table
    at `u16 +0x1A`; all 11,165 entries key valid `seq ` indices, none under the `+2` reading). The G-2 narrowing of
    2026-09-18 and the G-11 / G-13 texts built on it are struck and corrected on the page and in their rows.
  - Input channel record: one base R = `022CAE90` + ch × `0x294` (`in_channel_base.py`). Only the initialiser addresses
    it from R+1. Converted, AP-6's "dead-zone radius is 0" is wrong (`0x20` at R+0x0D), corrected on the page and in
    the row.
  - Reporter UNKNOWN row: already fixed by parser v5 (da5207fc9); a live parse finds none. Nothing re-statused.
  - Routed: the ff12config-and-debglobal row 189 `memset` wording to FABLE (exact text in the record). Review →
    SWE2-AUDIT-SEM (`DATA-REQ-AUDITSEM-DD-LEFTOVERS-0930`).
  - **Next:** process the READY queue addressed to SWE2-DATA (top: the P1 AUDITSEM / FRONTIER / OPUS requests in
    the TEAM-CURRENT block).
- **Earlier (2026-09-30, DD owner read of eight pages, published `f7a3292bd`; research
  `SWE2-DATA-DD-OWNER-READ-0930`, target key only; two forks did the Input and Audio pages):** capability policy, input
  stack, R2 toggle, SQEX driver, which-variation, sound-variant-selection, save-image buffers, version stamps. Missing
  sections written, uncited claims anchored or struck, stale "open" prose reconciled, G-2 / UQ-271 SUPERSEDED words;
  no status word raised. Residue registered in a new register section SD (`SD-1`–`SD-9`, `SD-20`–`SD-25`,
  `SD-40`–`SD-42`); record `_index/candidates/dd-data-0930/`. Routed: a bit-46 row for the battle-unit field map to
  FABLE; SD-24 (the record at a Sound's `+0x30`) contradicts the G-2 row's narrowing, left to the register owner.
- **Earlier (2026-09-30, round 3, published `79e70e154`; research
  `SWE2-DATA-RC30-RC28-0930`, target keys only; two research forks):**
  - RC-30 ANSWERED (`_index/candidates/rc30-census-0930/`): `003C1F00` requests kind 7 id
    `0xE1 + byte [menumap_common entry + 1]` (`003C208D`, a register-held site rounds 1 and 2 missed); entries 40 and 46
    select `Loca_gil` / `Loca_bhm`; `003C26C0` reads the file as a TIM2-shaped CLUT. Rounds 1 and 2's "no route"
    sentences are struck in their records. Left open (static): the palette byte order the upload `0024A1D0` declares.
  - RC-28 leftover ANSWERED (`_index/candidates/rc28-callback-0930/`): a refused KR/CN `.btm` request still fires
    `00364380` (the pump completes from the stale status), so the staff roll draws from a 0-byte sheet no read fills.
  - RC-35 / RC-36 parked: FABLE took them (FABLE answered RC-35 as `003BE680`; DATA's census agreement was posted to
    FABLE and the partial file deleted).
- **Earlier (2026-09-30, round 2, published `39d08c02f`; research
  `SWE2-DATA-RC-RESIDUE-0930` and `SWE2-DATA-BUCKET-NARROWING-0930`, target keys only):** (a) bucket members:
  SWE2-AUDIT-SEM ACCEPT-WITH-NARROWING (`cfc5a4863`) applied, N1 bin_menu row and N2 end slot in place (record
  `_index/candidates/bucket-members-narrowing-0930/`, `endslot_check.py`). N3 is stated in that record: the old
  package README is a correction record whose `affected:` line re-arms on any edit, so its one-bullet edit waits for
  an authorized override (routed to FRONTIER in the record). (b) Record `_index/candidates/rc-residue-0930/`:
  - RC-25 ANSWERED: `+0x60` = party row 0..0x27 or 0xFFFF; shipped scripts add main selectors 0..5, so all six blocks
    are reachable.
  - RC-30 sites `002CEAE0` / `003C9950` / `00575C30` bounded (0x17..0x29 / ≤0x1A / ≥0x228). The 54 computed-kind
    path-API sites are listed; the data-driven `(kind, id)` structures are the remaining static fact.
  - RC-28 (1) language → arm table; (2) KR/CN `.fst` = -1, the read is refused and there is no fallback; the refused
    request's completion is left open; (3) the shipped staff roll never requests the accented rows 894..944.
  - RC-29 side: no request site forms `title_menu` / `E3_Logo`; `nowload` / `title_fore3` have no kind-7 path.
  - SWE2-ORACLE ran the same rows in parallel with no claim (board note posted); its RC-25 and site-A results agree.
- **Earlier (2026-09-30, RC-22..RC-34, published `1261e2044`, task `SWE2-DATA-RC22-34`,
  target keys only):** record `_index/candidates/rc22-34-resource-readers-0930/` (README + 12 scripts, FAILS 0; two
  research forks did RC-26..28 and RC-32..34). ANSWERED: RC-22/23/24 (`.as7`: walker `0024AA00`, codec `00248500` =
  static-dictionary LZ, tail = {mode, k, be16 outLen, dictionary}; 7,216/7,216 pages decode), RC-26/27/28 (`.btm` 4 bpp
  low-nibble-first; glyph tables from `fontpack_fs.bin`, ids 130–135 never requested; 78/127 glyphs, 398/663 of 1,237
  pairs), RC-29 (premise refuted: `008FCE00` is the developer console's 14 × 22 page table; `.mrp` lists via
  `003933F0`/`00393460`/`003934F0`), RC-31 (`0037EFC0`/`0037E5B0`, order-independent, `+0x04` unread), RC-32/33/34
  (`meshdata.mg` two-entry directory, three draw paths, `mainN.psd` → `w_mainN.tm2`). NARROWED: RC-25 (516-page groups,
  `{0,1,3,2,4,5}[c]`, `c` = menu record word `+0x60`), RC-30 (no traced request route to the `.cl2` ids; three
  index-computed sites unbounded). No page or register row edited: incorporation → SWE2-CONTRACT
  (`DATA-REQ-CONTRACT-RC22-34-INCORP`), review → SWE2-AUDIT-SEM (`DATA-REQ-AUDITSEM-RC22-34`). Nothing routed to ASTRA.
- **Earlier (2026-09-30, after pass 18, published `da5207fc9`):** (a) **reporter UNKNOWN row** — it was `~~CH-2~~` (struck id,
  lead "STRUCK … FILED IN ERROR"): `progress_report.py` v5 classifies an unreadable struck-id row WITHDRAWN/STRUCK, test
  T35 (`OPUS-NOTICE-DATA-REPORTER-UNKNOWN-ROW`; commit in `SWE2-DATA-PUB-REPORTER-STRUCK`'s result). (b) CON-195 consumed
  in pass 18 (`OPUS-REQ-DATA-UQ218-ROW-CON195-0929` DONE). (c) Bucket notices consumed:
  `OPUS-NOTICE-DATA-BUCKET-MEMBERS-PATH-AND-COVERAGE-0929` and `OPUS-NOTICE-DATA-VBF-ADAPTER-AND-MEMBERS-0929-R` DONE
  (bucket_members_check at HEAD = []; VBF adapter `vbf_index.py` ownership acknowledged — owner review still to do).
  The 58-member result is held as is pending `DATA-REQ-AUDITSEM-BUCKET-MEMBERS-0929` (AUDIT-SEM re-deriving now).
- **Earlier (UQ-218 pass 18, 2026-09-30, published `29436f1ad`) — register row UQ-218 PARTIAL → ANSWERED:**
  record `_index/candidates/uq218-pass18-0930/` (`band_names.py`, `for_tail_census.py`, `fef_tables.py`, all FAILS 0).
  Band → `@FMN`: op `0x0B` plays `@FMC` record `list[result&0xFFFF] + (result>>16)` (`00417367`, `0041CD30`), whose op
  `0x09` names the `@FMN` (33,753/33,753); a positive yaw delta is the character's left (band 3 → `walk_l` 287/281,
  `walk_r` 0; non-negative turn → `trn_l` 226/0). `@FOR` tail lists ARE read (`0053AB50` `0053C16B`): per-part draw lists
  packed by `byte[rec+2+part]` (was "enable flags"), `{d → @FDM descriptor, s → sub-record, a/b → texture-register
  slots}`; high (`h*`) models draw a flag-1 pass (`+0x0E`/`+0x16`) and their first pass indexes the base model's `@FDM`.
  `@FDM` desc `+0x08` = s8 pair written to VU1 by `0053D4B0`, zero in 12,044/12,044. `02B64380`: `001D6EC0` = the
  `AsyncLoadManager` companion lookup (`0019FFD0`, 144 rows, `chara\hNNNN.efx`), appended by the file layer
  (`001A0F4E`), instanced by `003B38B0`, number kept by `003B3B10` / read by `003B33D0`. Pages: `fdm-and-for-entries.md`
  (status DOCUMENTED; corrections struck), `fef-and-motion-entries.md` (pass-18 section; residue lines struck),
  FCP page UQ-218 box ticked, AUDIT-LOG. Handler page routed to FABLE (`DATA-REQ-FABLE-HANDLERS-UQ218-P18`).
  Review: `DATA-REQ-AUDITSEM-UQ218-P18` → SWE2-AUDIT-SEM.
- **Earlier (published `bafa49c9f`, 2026-09-29, FABLE-session subagent 73162e75) — `OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS` (user-mandated) CLOSED on the measurement:**
  the member formats of the `.bin` / `.dat` buckets are declared in the tracked canonical
  `_index/bucket-members.tsv` (generator + checks C1–C7 in `_index/candidates/bucket-members-0929/`,
  README = the record): **53 `.bin` + 5 `.dat` members**, all 4,387 entries assigned by logical
  unit, per-signature totals = the full census's 59 + 21 rows, every member claimed `explained` on
  its consumer-bound sheet (58/58; `check_assets.py` resolves member tokens via `member_families`).
  Four leading dwords are shared by distinct formats and are written `SIG=N` — OPUS adopted that in
  the MP-3 gate (`6446068ef`, from `DATA-REQ-OPUS-BUCKET-MEMBERS-SHARED-SIGNATURES`). **Canonical
  measurement at HEAD:** `requirements.py` collect → `gaps {}`, 53 `X:bin/*` + 5 `X:dat/*` all
  "member format explained", 0 "not declared"; dashboard generation `g20260930T001745Z-6c4243`:
  `measured true`, X **104/104**, `gaps {}`. New sheets: `amap-menumap-area-table.md`,
  `gmap-menumap-guide-texts.md` (only guide00 is ever requested), `menuquest-bin-quest-detail-tables.md`;
  new sections: flagrom (persistent-flag-banks §2, reader `00377970`), fhmusicdata (no requester),
  test_area_ref (loaded, never read) / test_map_ref, license_chip (§6b), Item_Clut (§5b), shop_data /
  wepjob_matrix (battle_pack copies), menu_version; correction: summoneffectdata = 64 ten-byte
  records + tail read into `.data` `02AD9B60` (`dP<d` is data). Same commit also closed
  `OPUS-REQ-DATA-UQ206-RELEASE-LABEL`, `OPUS-REQ-DATA-ATEL-SIBLING-GATE-PAGES`,
  `OPUS-REQ-DATA-BATTLEUNIT-FIELD-MAP-ORDER-RECORD`. Review routed:
  `DATA-REQ-AUDITSEM-BUCKET-MEMBERS-0929` → SWE2-AUDIT-SEM (`reviews` field set).
- **Exact next action:** incorporate the SWE2-AUDIT-SEM verdicts when they land
  (`DATA-REQ-AUDITSEM-UQ218-P18`, `DATA-REQ-AUDITSEM-RC22-34`, `DATA-REQ-AUDITSEM-RC-RESIDUE-0930`, `DATA-REQ-AUDITSEM-RC30-RC28-0930`, `DATA-REQ-AUDITSEM-DD-OWNER-READ-0930`; AUTO-INCORP /
  AUTO-REPAIR), answer SWE2-CONTRACT questions on `DATA-REQ-CONTRACT-RC22-34-INCORP`, and FABLE's
  answer to `DATA-REQ-FABLE-HANDLERS-UQ218-P18`; then the owner review of the VBF adapter (`vbf_index.py`,
  `eae0ed3c7`). Page-level leftovers (not UQ-218): the motion page's op `0x12` look-at semantics beyond its callee,
  and the AUDIT-LOG pseudo-link `rdx = [r12+0x6C0] palette…` (pass-11 entry). No ASTRA routing is pending from this
  lane (UQ-218 closed statically). Static RC residue left after round 3: RC-30's palette byte order (what `0024A1D0`
  declares for the external CLUT); RC-28's 0-byte sheet (whether `0036BC60` returns a block or null for size 0); the
  N3 README bullet (needs an authorized correction-override, `DATA-REQ-FRONTIER-N3-OVERRIDE-0930`).
  Fallback: `FABLE-REQ-DATA-SN1-PAGE-62-ACCEPT`, `FABLE-REQ-DATA-SN1-PAGE-ACCEPT`,
  `OPUS-REQ-DATA-SN1-VARIABLE-NAMING-CANONICAL`, `OPUS-REQ-DATA-UQ206`-style incorporations, then
  the P1 reporter/export repairs (`FRONTIER-REQ-SWE2-DATA-PROGRESS-REPAIR-CKPT10R3`,
  `FRONTIER-REQ-SWE2-DATA-EXPORT-COHERENT-GENERATION`, `OPUS-REQ-DATA-ADOPT-GENERATION-LIB`).
- **Claims held at park:** none. No `@publication`.
- **Latest coherent commit:** the DD owner-read commit (this block's own); before it `79e70e154` (round 3), `39d08c02f` (round 2), `1261e2044` (RC-22..34),
  `da5207fc9` (reporter fix),
  `29436f1ad` (UQ-218 pass 18), `bafa49c9f` (bucket members).
- **Earlier (published `e45bbb909`, UQ-218 pass 17 — kind-1/2/`0x10` selector state bytes resolved):**
  the selector state record is `qword[ctx+0x2E0]` — one of `0xA0` ×
  `0x740` records in pool `[02B3EF28]` (pool init `004269A0` → `0041F730`:
  `memset 0x740`, `word[+0x40F]=0xFFFF`, `ebp=−1` fill ⇒ `+0x40E`/`+0x411`=0,
  `+0x410`/`+0x412`/`+0x2AF`/`+0x408`/`+0x24C`/`+0x288`/`+0xC4`/`+0xC8`/`+0x2C4`/`+0x434`
  = `0xFF`/`−1`). Per-`@FMC`-bind reset at `004252A7` (inside the
  `00409FA0`/`00409FD0` `'@FMC'`/`'@FRP'` name-query body): `+0x40E`=0,
  `+0x412`=`0xFF`. Bodies read end-to-end: kind 1 `00422420` (`+0x40E` arm
  timer — draw `003A6E60(5)`→`+0x411`, +5 at `11·frameLimit` if evaded
  bit set, saturate `0x64`); kind 2 `00422500` (`+0x410` sticky 0/1/2 via
  query `0x30` bits 2/4, `+0x40E` combo-age clamp `3·frameLimit`); kind
  `0x10` `004225A0` (`+0x412` rolled-once
  `((rand % (ctx+0x2DE−ctx+0x2DD+1))+ctx+0x2DD−1)·frameLimit`). `+0x410`/
  `+0x411` have no external writer — a decided kind-2 stick survives a
  rebind until record re-init. Folded into `criteria.md`, both READMEs,
  the motion page, the handler page (`0x0B`/`0x28` stale text struck),
  the candidate README, the OQ row — **the OPEN-QUESTIONS edit is in the
  worktree only** (unstaged FABLE OV edits in the same file; it rides
  the next publish of that path). Latest coherent commit: `e45bbb909`.
- **Earlier (published `9d3e3aeac`, UQ-218 pass 16 — `@FOR` tables A/B and the `@FDM`
  descriptor pool read in `0053B2xx`):** `0053B28D` joins
  `@FDM`/`@FOR`/`@FTE`/`@FCT` via `rec+0x208..0x21C` + `+0x1F8`.
  `@FOR`: `0xE0` record selected by `byte[rec+0]==s8[obj+0xB8]`; `rec+0x20`
  = five `0x20` part sub-records, each headed by a selector-byte array
  (`i < byte[rec+5+part]`); table A = u8 triplet table
  `bIdx = byte[tableA+3·sel+part] + byte[+0x32]·variant`, table B = u8
  pairs `{texture slot, palette slot}` → `@FTE`/`@FCT`. New consumers:
  `00504740` (keyed-float twin on `+0xB8`), `00504F00` stamps
  `+0xB8`/`+0xB9`/`+0xB3`. `@FDM`: lists at
  `dword[+0x34+4·sel]` = u16 offsets to `0x10` descriptors `{s8 defA/B
  @+2/+3 fallbacks, u32 slotPair @+4 → `00371330`, u16 subOffs @+0xC}`
  → sub-record → u16 bone stream ×0x290 → VU1 `V4_32`. Kind byte 1/2/3
  picks packed index decoders. Still open: `@FOR` tail index lists,
  descriptor `+0x08`.
- **Earlier (published `a39c3ff08`, UQ-218 pass 15 — `@FMC`
  op `0x28` resolved to mechanism, effect request lane):** `00520720`→`003E6AA0` stores
  `dword+4` at `obj+0x304` bits 27–31 (dirty bit 27); dirty pass
  `00427DE0`→`003B3C00(handle=[obj+0x288], value)` range-checks `0..10`
  vs the `02E9D480` slot table and calls `0024FE70(effectCtx, lane)`:
  `def = [[ctx+0x130]+0x80]`, `byte[def+0xA+lane]` selects
  `dword[def+0x2C+4·map]` (resource id) → `0020E600` resolve →
  `00333280(childObj, id, lane)` spawns into the object's 16-slot child
  table (lane stamped `child+0x11`). Lane 0 = no request; lanes are
  per-effect authored ports, not global semantics. Census re-run with
  corrected walker (`co += len` total): `{1: 112}` in four monster files
  (`m1043_10`/`m1044_10`/`m1132_10`/`m1133_10`, locomotion/reaction
  blocks), `{10: 3}` `m1143_10.ca` (`knockback_l` ×2, `dead` ×1).
  Folded into the motion page, candidate README, OQ row, audit.
- **Earlier (published `b969d32e4`, UQ-218 pass 14 — `004256E0`
  locomotion classifier verified and folded):** FABLE's
  `uq218-fmc-selector-kinds/classifier.md` re-verified FAILS 0. Kinds
  `0`/`0xA`/`0xB` share `004256E0` via `00422400`/`00422410` thunks (kind
  args `0`/`1`/`2`): `003E7D10(rec+0x6A4,4)` override → `0xE` remapped
  `0xB`/`0xC`/`0xD`; below `+0x23C` turn delta `+0x124 − +0x254` →
  `0`/`6`/`7`; mid-band heading `+0x244` vs facing → `1`/`3`/`4`/`5`;
  at `+0x420` + view `0x1000` flag `0x20` target-bearing → `2`/`9`/`0xA`/
  `0xB`; five FCP ids (`004FE2F0`) gate availability with fallbacks;
  writes `rec+0x2A0`, returns `index + ((1−esi)<<16)`, never `−1`.
  Corpus corroboration added: `.ca` `@FMN` names are the locomotion set
  (`idle`/`walk_f`/`run`/`walk_l`/`walk_r`/`walk_b`/`stp`/`run_l`/`run_r`
  in `_l`/`_r` pairs — `c1004_23.ca` slots 80–96), a positional match.
  Folded into the motion page, the handler page, both candidate records,
  the OQ row and the audit log. Still open: exact band→name binding
  (inference), yaw-left sign, kind-1/2 reset stores (`+0x40E`/`+0x411`).
- **Earlier (published `42d56e367`, UQ-218 pass 13 — `02B64380`
  rows are `char*` resource paths):** the only live ref is the reader's `lea rsi` at
  `0040A11C`; the table is `.data` virtual tail (zero-fill). The populator is
  dead-stripped code at `0040A230` (`.pdata` gap `0040A22C`–`0040AA20`): 144
  `lea rax,[.rdata path]`/`mov [rip→slot],rax` pairs, `ret`, no image
  pointer to it. All 144 verify `table[fold(stem)] = path` under
  `00409FE0`'s own fold — `PS2Data\obj_finish\in\{g,m,n,s}\*.cm` paths =
  the `@FEF` corpus. ~~Shipped table is all-NULL → the `@FEF` arm is vestigial~~ *(refuted by CON-195: the
  table is seeded at start-up through `00409F80`; the arm is read in pass 18)*
  (row = non-null gate + `001D6EC0` name arg; payload offset =
  `dword[r14+roundup64(002DF960(class,num))−4]`, the resource's own tail
  dword; `002DF960` = `u32[02EC3EE0+class·0x1388+num]` size lookup).
- **Earlier (published `1fdad99d2`, UQ-218 pass 12 — the `0x34` "128-way"
  jump table = the character shadow-parameter command):** `byte+2==0xFF`
  is a global arm (`003AFD30`→`02B3F554`, `003B6930(4|6)`→low 2 bits of
  `02B3F524`); otherwise `003AFC10(dword[obj+0x118])` resolves a handle in
  the shadow-param pool (`02B3F570`, 32×0x70, tag `+4`) and a compressed
  dispatch (`u8[00520B50+sel]`→8 cases, `u32[00520B2C+case*4]+0x120000`)
  writes fields — `byte+2` is a bitmask: five `{frames;target;rate}` ramp
  channels + `+0x1F` nibbles + `{+0x40,+0x50,+0x56 size enum
  0x40/0x80/0x100}`; `byte+3` = ramp frames, `dword+4` = f32 target.
  `003AF460` advances all records per frame (`00426117`); `003AFB30`
  single-steps a handle inside the `@FMC` catch-up paths
  (`0041C8F1`/`0041D9D1`) — deterministic replay for shadow ramps.
- **Earlier (published `5ddfdd3d8`, UQ-218 pass 11 —
  `renderRecord+0x6C0` = the skinning palette):** `0017F260` is a bare `vtbl[0xD0]` thunk; the
  real call `skinObj->vtbl[0xD0] (palette=[rec+0x6C0],
  boneCount=word[part+0x8A])` fires at `0053B209` in the `0053B2xx` draw
  builder. `003703A0` builds it: `+0x6B8` = device skinning object
  (`0017F0D0`→`001BD4A0` on singleton `01F81248`, gate
  `0017EFC0(dword[+0x6B0])`); `+0x6D0` = `count*4` buffer (`0019C580` +
  `0017EF60`); `+0x6C0` = `count*0x40` records `{4 vec4 rows = part
  +0x150 bind ∘ bone +0x80 pose × +0x100 scale vec4, trans row +0x30,
  i32 +0x3C = parent bone idx (word[+0x270])}` — the parent link is the
  `@FTR` hierarchy carried into the palette. Freed in dtor `004200A0`.
- **Earlier (published `6a4bbbc37`, UQ-218 pass 10 — arm-0 extended `0x1C`
  record dispositioned dead-authored):** all five `00409150` consumers
  enumerated — interpolators `0041B3A0`/`0041B460`/`0041B920`/`0041BB00`
  + `0041B650` init (`0041B6C4`) only scale `nC·0x1C` into the B-base;
  `0041D945` (in `0041D820`) reads only bit 31 → flag selects `0041C850`
  modulo-duration `@FMC` replay (`0041ADA0`: pos mod `dword[+0x50]`).
  Corpus via real `+0x40` offset table (raw-dword heuristic had one
  coincidental false positive, `c1006_10_3005.ca @0x408C`): 6,200
  extended descriptors, `nA==nB==nC==1` on all — fixed per-channel
  extension record, stable shape `{u32 ~6, f32, u16{0,N}×2, u32 ~2,
  u16{1,M}, u16{6,7}}`, **no shipped-code field reader**. Page, OQ row,
  candidate record, audit updated.
- **Earlier (published `281e38648`, UQ-218 pass 9 — `@FMC` key domain
  resolved):** keys are **frame indices** — per-tick call `0041DBD2`
  passes `cvttss2si(f32[state+0xC])`; `0041E000` fires `key ≤ threshold`
  with persistent cursor `+0x8C` (end → reset `+0x88`, `+0x96|0x80`).
  `0xFFFF` is **not** an end marker — always sub #0 (40,441/112,439
  records), 1–2 init commands (op `0x01`/`0x0A`+`0x0B`) re-dispatched
  every tick via `state+0x90` at `0041DAD3`; `0041CD30` starts the keyed
  run after it. Corpus: 272 distinct keys 0–700, sorted unique, key 0
  first in 112,437. Flush: `r8d=−1` callers `0041DBB8`/`0041DC47`/
  `0041DCC6` armed by `f32[shared+0xC] ≥ f32[ctx+0x34C]` →
  `word[state+4]=2`; `0041C8FF` catch-up loop. Census:
  `members/fmc_subkey_census.py`.
- **Earlier (published `d22ad1b95`, UQ-218 residue merge):**
  `FABLE-REQ-DATA-UQ218-RESIDUE-MERGE` + `FABLE-REQ-DATA-UQ218-FMC-CROSSWALK`
  + `FABLE-NOTICE-DATA-UQ218-SELECTOR-CRITERIA` DONE
  (`FABLE-NOTICE-DATA-UQ218-FMC-HANDLERS` closed as superseded). All
  checkers re-run independently — FAILS 0. Folded in: `@FMW` arm-0
  run-table layout + corpus fix (727 `.ca` entries; A 8-byte frame runs /
  B 16-byte value runs `{streamOff,—,keyCnt,bias,scale}`, same flag
  codec, `nA==nB`); node `+0x100` scale vec4 consumers (`00373860` ←
  `003705BA`, `00372610`, `00202FE0`; gate `bone+0x280&0x10` multiplies
  by `+0x1E0`; `+0x80` parent matrix unscaled → scale does not inherit);
  `+0x44` external effect handle (five readers; `00409FE0` resolves
  external `chara\h%d.efx` via letter+number index into `02B64380`;
  `0041E580` = 12-byte thunk with four load-completion callers);
  `+0x31A`/`+0x31C` provenance (`0041D220` ← descriptor `+0x24`/`+0x20`
  ← `0051BA80` ← `render+0x413` = `01AA stdmotionvariation`; not
  `.ca`-authored); `@FMC` semantic names folded into all 33 rows;
  `0x0B` authored kind set corrected to the ten kinds.
- **Earlier (published `c8d6ddb80`, UQ-218 pass 8):** the `@FMC`
  per-opcode operand map is complete — all 33 authored ops have
  handler-level operand reads (table on the page): real bodies
  `00417110`–`00417DE0` (`0x00` duration, `0x01`/`0x09` select, `0x0B`
  element batch → synthetic op-`0x01` fan-out, `0x0D`–`0x10` tweens
  into `02B40528`, `0x2C` selector) plus 25 null-gated hook thunks
  → `tabA[op]` `02CA4410` registered `00426A0D`–`00426B84` +
  `002EA4xx` (→ `00520xxx`/`002E70xx`). Unauthored lanes: `0x08`,
  `0x14`/`0x19`/`0x1E`/`0x1F`/`0x26`/`0x48`.
- **Earlier (published `aae992c65`):**
  `FABLE-REQ-DATA-UQ218-EMBEDDED-EFX` DONE — folded FABLE's
  `uq218-embedded-efx-sweep` record in (efx_consumers.py E0–E3+C re-run,
  FAILS 0): embedded `EFX0010`'s only reachable consumer is the `ret 0`
  stub `0016D6A0`; `003B38B0`/`003B3B10` have one caller each (both in
  `00409FE0`); `'@FEF'` immediate at exactly `0040A0A4`/`00504F78`/
  `00504FCE`; no `.pdata` body reads `rec+0x230` with the render-record
  shape. Page, OQ row and audit updated.
- **Earlier (published `0adb69e9b`, UQ-218 pass 7):** `@FMN` fully
  dispositioned — `+0x50` pair ruled: `u16 +0x50` = frame duration
  (walker `0041C18A`, == `@FMW` byte0 ×15,037); `u32 +0x54` = post-record
  block offset (`0xF0+nrec*22`, +2 pad variant — all 20,207) naming a
  per-channel f32 rest stream whose only reader `0041B5B9` gates
  identical arms (dead field).
- **Earlier (published `465b40bf5`, UQ-218 pass 6):** the `@FMN`
  `kind&3` layout split — arm-1 (all 20,207 shipped `@FMN`; zero `@FRP`
  in corpus) reads `+0x60` clamp pairs/`+0x70` vec2/`+0xA0..+0xA8`/
  `+0xEE`; arm-0 reads the same fields at `+0x30`/`+0x40`/`+0xBE` —
  so `+0x30`'s f32 reads are arm-0-only and the second name has **no
  shipped reader** (authored metadata). (The pass-6 AUDIT-LOG entry
  rode CONTRACT's `d5869b36d`; pass-7's entry is in `0adb69e9b`.)
- **Earlier (published `41c6f9761`):**
  `FABLE-REQ-DATA-SN1-Q3-PARAGRAPH` DONE — q3 corrected in
  the-ctrl-module-debug-companions.md: `{u32 X; u32 map[E]; zero pad}`,
  map[k] = last instruction index before byte 32k (E = 1 +
  floor((q0len-1)/32)), inverse of q2; FAILS 0 on FABLE's
  sn1_q3_pagemap.py re-run; two-list reading retracted; head word X
  open (routed to OPUS in the request body).
- **Earlier (published `b26125d2d`):**
  `OPUS-REQ-DATA-UC1-READERS-65-256` DONE — uc1_band.py merges both
  applied TSVs (795 frontier / 25 held), all readers on the 35,064 /
  38,955 series; test suite 22/22.
- **Earlier (published `05a0a565a`, pass 5):**
  `SWE2-DATA-UQ218-MOTION-RESIDUE` — the `@FMN` tail is
  executor-proven: walker `0041C040`–`0041C1D9` reads `u32 +0x0C`
  records at the kind-selected base (`00409190`: kind `0x02001111` →
  `+0xF0`); each record is a fixed 22-byte `{u16 nodeKey,
  u16{chMask:9, byteLen:6, flag:1}, u16 chIdx[9]}` node-channel
  assignment — mask bit i ⟺ `chIdx[i] < 0x8000` (`0x8000|n` = absent).
  `0041B550` writes nine `0x1C` runtime channel slots at
  `nodeRow+i*0x1C` (`word+0x100`=nodeKey, `word+0x102`=bitmap,
  `dword+0xFC`=record offset). `nodeKey` resolves via `00370E00`→
  `00373540`: the `01EF9438` linked-registry claim (key match +
  flag `0x100`, unlink, return index). `@FMW` arm-1 descriptor:
  `{u8 frameCount == @FMN word+0x50 (15,037/15,037 channel-bearing
  pairs), u8 streamCnt, u32[cnt] delta-offs, {u32 litOff17, f32 bias,
  f32 scale}/key}`; flag-coded stream `0x80`=s16le (pass-8 correction;
  was written s16be here) / `0x40`=repeat /
  else s8 → `lit*scale+bias` into slot `+0x8`/`+0xC` lerp pair.
  Corpus: 746,142 records, zero violations — census 26/26.
- **Exact next action:** continue UQ-218 residue — the narrowed set is
  yaw-left sign (which sign of the heading delta is the character's
  left — evidence path: a producer/consumer where the sign maps to an
  authored left/right track or turn direction), kind-1/2 state-byte reset
  stores (`+0x40E`/`+0x411` area — read complete function bodies, xrefs
  alone are not proof), and the `@FOR` record's three u16 tail index
  lists (no `0xE0`-walker reads them — all four enumerated) + `@FDM`
  descriptor `+0x08` field (rest of `@FDM`/`@FOR` decoded pass 16). `004256E0` classifier
  geometry + FCP gating + fallback are **resolved** (published
  `b969d32e4`); op `0x28` is **resolved to mechanism** (pass 15 — effect
  request lane, above); exact band→`@FMN`-name binding stays inference. `@FMN`, embedded-EFX, `@FMC` operand
  map + key domain, `02B64380` row type + `0040A230` dead populator,
  `@FMW` arm-0 layout **incl. the extended `0x1C`
  record**, `renderRecord+0x6C0` skinning palette, the `0x34` shadow-param
  subsystem (pool `02B3F570`, `003AF460`/`003AFB30` ramp advance), `+0x100` scale
  consumer, `+0x44` consumers, `0041E580` callers and `+0x31A`/`+0x31C`
  provenance are closed. After UQ-218, the ready
  queue holds `FRONTIER-REQ-SWE2-DATA-PROGRESS-REPAIR-CKPT10R3`,
  `FRONTIER-REQ-SWE2-DATA-EXPORT-COHERENT-GENERATION`,
  `OPUS-REQ-DATA-ADOPT-GENERATION-LIB` and ASTRA/OPUS script-semantic
  requests.
- **Latest coherent commit:** `9d3e3aeac`.
- **Earlier (published `859f1eb00` + `2e6da065f` + `0e1809f49`):**
  `SWE2-DATA-UQ218-MOTION-RESIDUE` pass 3 — `@FMC` grammar
  executor-proven (records/sub-records/commands, table `01EFFAF0`,
  ops 0x00/0x2C/0x0F/0x10 named); `.ca` variant-1 slot tables
  resolved (`004090D0` `slot[80·group + cmdSlot]`, group `+0x31A`,
  cmdSlot `+0x31C & 0xFFF`).
- **Earlier (published `d5261fb4e` + tail `b93c4b2a7`):**
  `OPUS-NOTICE-DATA-STRUCTURAL-OBLIGATIONS-UNCOUNTED` — page-box counting
  decision (`page_boxes` counters, parser v4; 29 closed-row boxes
  dispositioned; DISCOVERED fields stay on TYPE-COVERAGE). Tests 35/35.
- **Earlier (published `8154f227a`):**
  `FABLE-REQ-SWE2DATA-ACCEPT-SQ1-DWORD0-CORRECTION` — independently
  verified (sq1_dword0.py FAILS 0): `00213140` is `DynGeoFontTextInstance`
  slot 1 reading its own `+0x40..+0x4C`, not audio; `007EFC40` is SEAD
  `Lay`-family vtable +0x100. OQ SQ-1 row carries the author-ratification
  note.
- **Earlier (published `0754df300`):** `OPUS-REQ-DATA-SN1-DBG-FRONT-TABLES`
  — `.dbg` front region corrected to T1/T0/T2 (the fold artifacts:
  "sorted by heap position" and "~416 name aliases" were measured on the
  folded stream; real T2 sorted except ~5 steps, duppos=0, ends at
  gdbg[4095] in btlctrl).
- **Earlier (published `113cca077`):**
  `FRONTIER-REQ-SWE2-DATA-PROGRESS-REPAIR-CKPT10R2` — C1 semantic hash,
  C2 audit-log fingerprinting + root AUDIT-PASS* doc signatures, C3
  empty/malformed inputs fail closed; C4b per-commit `commit_id`.
  ckpt10_exec 9/9, suite 33/33.
- **Earlier (published `6c6a6d3b0`):**
  `FABLE-REQ-SWE2DATA-G3-ANSWERED-BY-WC1` (claimed rev 34941) — verified
  WC-1's eps-preset record against G-3's last clause: all 68 slots of the
  eight non-zero strides dispositioned per-slot in `fields.tsv` (52 role
  rows, 5 ignored band-type ints, 7 padding, 4 class-9 nop-arm); controls
  reproduce `exit=0`. Corrected the record's "72 slots / 4 ignored / 12
  padding" headline (arithmetic slip — true split 68 = 52/5/7/4).
  `sead-win-config.md` §6d residual + §7 answer block + residue bullet
  updated; OQ G-3 → ANSWERED. Gates clean. Remaining limits are
  confidence-level only (two filter shapes unclassified, 4 medium roles,
  names unrecoverable, bank dormant).
- **Exact next action:** publish `sead-win-config.md` + `OPEN-QUESTIONS.md`
  + `AUDIT-LOG.md` + this file, then finish the request and claim the next
  DATA package (UQ-218 residue: `@FEF`, `@FMW`/`@FRM`, FOR/FDM/ct field
  semantics remain).
- **Earlier (published `057e8d0ff`):** `SWE2-DATA-UQ218-FTR-ENTRY`
  (claimed rev 32950) — `@FTR` kind-2 entry decoded:
  `+0x40` u32 index table `(off<<12)|ord`, variable
  `{link,flags,u16-stream}` records, `+0x34` u32/f32 aux pool,
  `+0x38` extra u16 slots; runtime core = count×0x290 + u16 list;
  FCP-s2 tail memcpy + `003E1C50` relink. New page
  `ftr-node-table.md` + `members/ftr_entry_census.py`; OQ UQ-218 row
  narrowed (stays PARTIAL — @FDM/@FOR/@FTE/@FCT/@FEF, @FMW/@FRM,
  node semantics and the s2 sub-structure's fields remain).
- **Exact next action:** claim the next DATA package — UQ-218
  residue (@FDM/`@FOR` entries are the warmest: same
  `0041F340`-family binder pattern) or another OPEN-QUESTIONS row.
- **Just finished (published `a99867d19`):** `SWE2-DATA-UQ220-FCP-SECTIONS`
  (claimed rev 32864) — **`+0x24` is a u32 `@FTR`-tail copy length, not
  `sectionOffset[18]`** — `0041FCF0` builds `r14=payload+word[2]`,
  `r15d=dword[+0x24]` → `0041F340` → `00372820` does
  `memcpy(FTR_tail, section2, len)` at `003729B7` (**section 2 is
  live**; len = s2 size in 528 blocks, s2 end-offset in 538 — two
  authoring generations). Whole-image accessor sweep
  (`mov r64,[rec+0x400]` + `movzx word[r+off]`) inventoried every
  offset word: s2 reader `003E4B40` (raw word; only the two
  initialiser calls), **s6 reader `003E5C0E` is dead code — no
  E8/E9/dword/qword ref** (layout proven anyway: 16 ×
  `{u16 key|0xFFFF,u16,u32,f32,f32}`), s8 verbatim memcpy at init
  (`0041F5CE`/`0041F5D9`), s10 = 48 B with only `f32[+8] ÷ u8[+0x10]`
  live (spawn period, caller `003AF3B0`). Sections 5, 11–17
  authored-only. Census member `members/fcp_tail_sections_census.py`.
  Gates: links clean (6 pre-existing), consistency clean,
  doc-addresses ok (310 cited). Residue → UQ-218: s2 slot domain +
  FTR-tail consumers.
- **Pending requests/reviews:** `OPUS-NOTE-SWE2DATA-SQ1-LANDED-8F6B3B467`
  (READY, notice-only — the withheld SQ-1 row landed in `8f6b3b467`;
  acknowledge and retire).
- **Fallback eligible work:** `UQ-218` (@FTR/@FDM/@FOR entries — now
  warm: the FCP s2 tail copy lands inside the FTR allocation) or
  another OPEN-QUESTIONS DATA row.
- **Exact next action:** retire the OPUS note, then claim `UQ-218`
  (@FTR tail consumers are now the highest-value DATA row — the s2
  copy destination).
- **Latest coherent commit:** `057e8d0ff`.
- **Prior package (FINISHED, published `1eb1b3e9a` + earlier):**
  `SWE2-DATA-SESEP-FIELDS` — `SeSep` payload = `{u32,u8}` pair +
  dead PC program stream; dword0 live via `vft[+0x100]` param-push.
- **Prior package (FINISHED, published `868fa4f5c` + `62d96987a` +
  `3dadbaeed`):** `SWE2-DATA-SQ1-BAND-SPLIT` — SPP1 id = `.sab`
  filename (`%s/se%03d/se%06d%s`), bands = folders, no band dispatch,
  `sabf+0x0A` flat ordinal (only `==1` special-cased), `sabf+0x05`
  loader-shape flag, `SeSep` flag byte → `+0x49` live state with the
  `.seb` `+0x09` reseed rule.
- **Prior package (FINISHED, published `ed60c6c54`):**
  `SWE2-DATA-SQ1-SPP-RESIDUE` (claimed rev 32704). `+0x10`/`+0x12` are a **MapNo pair** —
  flag + zone's `planmapname.bin` index, constant per `map_ctrl/zoneNN`
  family (87 families → one value each), `0xFFFF` when flag 0; join
  verified by decoded names (590 "Athroza Quicksands" = dor01/dor02,
  549 "Ice Field of Clearsight" = rbn10, 555 "Port Section" = var01,
  539 "Walk of Flitting Rifts" = rsn01/rsn52). `+0x18` =
  `align16(0x20+4·count)` zero-pad offset. All three **dead-authored on
  PC** — no `022CBAF8` reader touches them. **id bands:** 1000s =
  ambience/weather class (weather table selects 1k only, 1115/1115;
  env99 all-1k; 1k chunks `byte0∈0x82-0x84 ∧ byte4=0x20`); 10k/50k
  split unpinned. **env99:** the "record-driven sixteen" source kind/id
  from runtime request records/queues (`003DD4C0`→`0215FD88`,
  `003DF550`, `003E9EF0` via `002640C0`/`00267E10`, `003A13F0`→
  `002ED8C0` queue-pop) — no authored record table feeds `0032E620`;
  residue = computed-kind producer. OQ row narrowed (stays PARTIAL).
  Gates: links clean, ledger consistent, doc-addresses ok (121 cited).
  **Package FINISHED** (PARTIAL result, residue documented). **Exact
  next action:** next highest-value unblocked DATA package — queue
  empty; candidates: the 10k/50k `SeSep` split (needs a native
  consumer), `UQ-218`/`UQ-220` payload-section passes, or scan
  OPEN-QUESTIONS for DATA-shaped rows.
- **Prior package (FINISHED, published `59d259a2f`, rev 32701):**
  `SWE2-DATA-UQ255-SEB-SLOT-U32` — `.seb` slot `u32` dead-authored PS2
  carryover (both copies write-only); authored `u8` = flag byte (bit3
  slot-7 exclusion, bit5 dormant second arm, bit7 `007A7010` arm); node
  `+0x09` = live state byte re-seeded per start; authored bits 2/4
  dead. Correction carried: FABLE's "none reads +0x04" — the start path
  `00224570` reads it four times.
- **Prior package (FINISHED rev 32670):** `SWE2-DATA-SEAD-ROUTING-G3TAIL` (rev 32583;
  scope = sead-win-config.md + arch doc + `oq:g-3`). **Package
  effectively exhausted** — every field-level residual resolved except
  one dormant-machinery naming pass. §6d published `c95ee5473`
  (`SWE2-DATA-PUB-G3TAIL-0927`); §6d-close pass adds: **`curv`
  dead-authored** (nine binders store the element at ramp `+0x38`,
  nothing dereferences it — fades run `007CD000` → `007A9E50` six-kind
  easing on `slot+0x1C`); **`bus +0x0B` and `ctgl +0x04` dead-authored**
  (no readers among the sole consumers); **`epsp` fully decoded**
  (stream A `{busIdx,rampSlot≤4,f32}`→`007CA560`; stream B 16-B
  `{busIdx,fxSlot<4,op}` — `0xFE` skip/`0xFF` enable/else `eps ` preset
  idx → `007AD240` → `insert->vft[+0x30]`); **`eps ` mechanics read**
  (`007ADDC0` class-section table + stride table `01CB49A0`
  `{0,0x80,0x20,0x10,…,0x20}` — prior `0x80000000` sentinel read
  corrected to `0x80`; classId↔effect map joined to the nine `bus `
  insert ctors via `0x68CCF0`); **epsp reachability = live** (action
  dispatcher `007AB5C0` arm type `0x30` `{epspIdx@8,fade@0xC}` — empty
  chunk bounds-fails). **Sole residual:** per-field float names in each
  `eps ` preset block — dormant `01CB7xxx` param-descriptor tables
  (record `+0x24` = field count = stride/4). **Published `7c4755a7a` +
  resume `4c48e643f`; package claim FINISHED at rev 32670. Exact next
  action:** next highest-value unblocked DATA package — queue empty;
  candidates: `eps ` field-name pass (dormant, bounded), or scan
  OPEN-QUESTIONS for DATA-shaped rows (46/48 formats dispositioned).
- **Prior checkpoint:** **mcr decoded and published `e1a352a1c`**:
  executor `007B31A0` (4,561 B; `007B3254` = interior
  `007AE1D0` finder call); desc `[ctx+0x30]` macro slots +0xA (init)/
  +0xB (stop, `Sound::Stop` `007BED30`)/+0x4F (release), index→`007AE1A0` element accessor,
  `word[rec+2]` = stream offset; instruction `{u8 flag, u8 hdrLen=4,
  u8 op, u8 payLen}`; dispatch byte-map `0x7B43D0`→dword `0x7B4374`
  (`.text` — canonical VA, RVA=cva−0x120000); 23 live ops (9 filters on
  the `02EAD570` worklist via `007B2880`, 12 gated actions, 2 control);
  `02EAD57C` = worklist active count; `007B2BD0` = 6-way gate; `007A84A0`/
  `007A8590`/`007A7A20` enqueue `{type,obj,float}` actions; `007AAA20` →
  `02EAD008` = Category table (FABLE). Shipped macros = same-key
  collision policies (≥1 peer→status 4; ≥2→apply 0.1f). §6c published;
  WC-1 mcr arm closed, G-3 still OPEN.
  **Exact next action:** G-3 tail residue — `bus `/`eps `/`curv`/`hcam`
  field semantics, `ctgr +0x06`, the `desc+0x30` authored provenance
  (`evt `/`epsp` empty → per-bank data), and the `02EAD560` pool
  population path; or next unblocked DATA package if superseded.
- **Latest coherent commit:** `7c4755a7a` (SEAD §6d-close) +
  `4c48e643f` (resume); earlier `c95ee5473` (§6d) / `e1a352a1c` (mcr).
- **Prior coherent commit:** `2f44e40f2` (**CLOBBER-RECOVERY-0926** —
  `0cd44bd1e`'s splice publish dropped ~600 lines of uncommitted
  SWE2-CONTRACT index entries (worktree restore step skipped); re-landed
  byte-verbatim from the pre-splice snapshot `work/SWE2-DATA/tmp/
  {AUDIT,PS}_worktree.md`: 34 AUDIT-LOG sections + 9 PROGRAM-STATE
  entries under integrity banners. Request
  `SWE2CONTRACT-NOTICE-DATA-AUDITLOG-STALEWRITE-CLOBBER` DONE;
  `@publication` released; board rev 32565. **Rule learned:** after a
  splice publish, restore pre-splice worktree bytes before releasing —
  `git status` must show the file differing from new HEAD by exactly
  the still-uncommitted peer content.)
- **Prior coherent commit:** `0cd44bd1e` (**SEAD-CONFIG-G3 pass
  published** — `scnf` magic IS validated: `007AE410`
  (`[buf]==[01CB4928]`) is `007B0F90`'s first gate before the `+0x0C`
  copy; mismatch → −1 → `007A4D50` bails. §6b added (validator +
  `eps ` float blocks + `expr` eager table `007AE020`/`02EAD3F8` +
  `mcr` op bytes); the two "magic inert" claims corrected; G-3 row +
  arch bullet annotated — format was already read, residual = routing
  semantics, row stays OPEN. KE-1-close index blocks + this pass's
  audit/PROGRAM-STATE entries rode the same commit; OQ spliced
  G-3-only. `@publication` released; board clean at rev 32134).
- **Earlier coherent commit:** `d85050253` (**KE-1 CLOSED** — the
  `.dat` header `+0x20`/`+0x24` pair is **dead-authored**: written to
  rec `+0x1C`/`+0x20` by `001FC060`, read by nothing — closed accessor
  census over `lib+0x30`/`001B51C0` (5 callers) + `[ctx]` readers, all
  field access via getter set `{+0x08,+0x10,+0x24,+0x28,+0x2C,+0x30,
  +0x34}`+3 maps; `001FDDC0` callers all non-font types; `001F49E0`
  zero callers. **The fontclut table is colour, not metrics**: 28×0x24
  slots at `ctx+0xF68` = `{inited; mShadowRGBA; mFontRGBA}` filled by
  `001C76E0` from config members under `mClutIndex`; `001E8070`
  consumes them ÷255/×(1/128) into 0x3C emit records, and reads only
  rec `+0x24`/`+0x28` (atlasW/tile extent) off the bound font.
  `us_fontex_expand.dat` anomaly = an older **0x20-byte-header**
  serialization + 810 standard records (the "values" were rec0
  `{key=U+56F0; utf8=困}`); still orphaned. Question row ANSWERED,
  spliced). Earlier this thread: `8b3b9b641` (MA-1 rescope + census),
  `71ff42d7b` (ten dispatch rows + w+rw guidance).
- **Prior package (closed):** font resource family
  (`font-data-kerning-and-expansion.md`). All `.dat`/`.ker`/`.fex`
  format words decoded, corpus-validated and published through
  **`cf5d6545d`**: header semantics, glyph-record utf8/tileY, cp-key
  proof 56,451/56,451, fontSetBase never-written; **`w7` = advance**
  (`w6` byte-identical duplicate, 0 diffs corpus-wide; consumed
  `payload+0x1C` → `0017F9C0` → `trunc(adv/fontScale)`, `fontScale`=
  `record+0x34` getter `001FDDB0`); **`w8` = kern cp** (−1 = not
  kerned, else the glyph's own cp — 69/69 utf8 match on us_stf_a;
  populated exactly in flags-bit0 fonts); **`.ker` = `{rightCp;
  leftCp; i32 adjust}`** (direction from `001FDDD0` =
  `kerMap[cur.w8][prev.w8]` + classic pairs VA/WA/YA/TA);
  **structural defect proven**: `001FDC10` (sole writer, via
  `001B5230`) stores flat `map<first,adjust>` in 0x28-B nodes
  (`001FC9F0` alloc(0x28)) — `leftCp`/`r8d` saved and never read —
  while `001FDDD0` (sole reader via `001E9780`) walks a nested
  `map<cur,map<prev,adj>>` at the same `+0x70` map — inner-map fields
  at node+0x30/0x40 don't exist in flat nodes → **authored kern pairs
  are structurally unreachable**. Orphaned `.ker` files: font00
  (ch/cn/jp/us), fontex_expand (ch/cn/kr), iwa_g12 (jp/us) — present
  but flags-bit0-clear, same legacy pattern as us `.fex`.
  **Exact next action:** font resource family is fully closed through
  `d85050253` (every `.dat`/`.ker`/`.fex` residual resolved or proven
  dead-authored/orphaned). Next: claim the highest-value unblocked
  package per PROGRAM-STATE / board. Board clean for this lane at rev
  32102; no claims held, `@publication` released.
- **Prior package:** loader-bound `.bin` residue —
  `loader-bound-bin-families.md` all three tracked items answered,
  **PUBLISHED `caee8e80f`** (`SWE2-DATA-PUB-LBB-0922` DONE,
  `@publication` released rev 26169; foreign-header allowance for
  ADDRESS-INDEX's generated heading). Gate triage carried in the same
  commit: `check_assets` fixed via an out-of-band `'hchk'` row in the
  **untracked** `work/formats/format-magic-census.tsv` (regeneration
  loses it — documented in the audit entry), `check_layouts` crash
  fixed (mixed str/int offset sort + `a` shadowing the argparse
  namespace), `MrpHeader` clash reconciled (`MrpHeader_rwg0201` in
  the-map-ctrl-pack.md), six stale MP-2 struct fences normalized,
  `RULES.md` regenerated; remaining gate failures peer-attributed:
  `fontpack_*` interior
  tables named (fs dir0 = glyph-metrics container, dir1 = texture
  payload, dir2/4/5/6 = pre-bound `.btm` faces; it dir0/6 =
  `fontVariant[]` TIM2s, dir2 = decoder char table, dir3/4 dead-bound
  u16 LUTs, dir5 = icon table, dir7 sentinel alternate); subtype
  `0x75` = tolerated-absent sibling (pair consumed at `+0xD0`, alloc
  stays null); `behindcamera` evaluator chain isolated
  (`00259820` → `00259990` → `003D9930`/`003D9950` → `0032AEC0`
  mover; scalar = per-frame phase increment at `obj+0x74`).
  Residual: polyline axis semantics (inside `0032AEC0`/`003CC130`).
- **Prior package:** handbook index family — structurally closed;
  all increments published through `2645a9f4d` (hbfin:
  `hchk +0x0A` dead header field). Only cosmetic residue remains
  (`hctg` `textId` naming conventions).
- **Prior package:** handbook index family — `hctg`/`hchk`/`hdat`
  decoded end-to-end (the himg siblings; self-directed fallback after
  MP-2 closure). **PUBLISHED `1f9f37678`** (`SWE2-DATA-PUB-HBINDEX-0922`
  DONE, `@publication` released rev 25814; foreign-header allowance for
  ADDRESS-INDEX's generated heading). New page
  `hchk-hctg-hdat-handbook-indexes.md` + validator
  `members/gen_hb_index_census.py` → `hb-index-census.tsv` (54 hchk +
  101 hdat + 54 hctg, all checks pass, 6,300 records). Native binds:
  `hctg +0x14` = hdat file count (resource-delta arithmetic closed);
  hchk non-monster = 8-byte 4-slot conjunctive gate (`00575E80`:
  nibble `+0x336C` == val, bit `+0x334C` set, `0032A8A0` on `+0x14F4`,
  `i16 global_flag[0]` ≥ w6); monster = `u16[8]` per-slot vector with
  `v[7]` mode bits selecting kill-count (`00315420`/`+0x3404`) vs
  scenario-flag thresholds (`00576E30`/`00576860`); sync `00577550`
  persists to save `+0x32CC` bits / monster `+0x3604` bytes
  (`00315910`/`00315AD0`); `00576920` = tab count/badge reader.
  hdat record: `{u8 strCount(1/2/3/7); u8 arg; u16 globalIdx;
  u32 strOff[strCount]; const tail 0080 0080 FFFFFF; u8 chapter}` —
  len = 12+4·strCount exact on all 6,300. Edits: himg page (+0x14
  bound, sibling table corrected), the-handbook-screen.md unlock-sync
  section, OPEN-QUESTIONS FG-1 (family A = hchk unlock results).
- **Prior package:** MP-2 flag-channel decode + tag-0
  closure + ACTL residue pass — both halves PUBLISHED:
  `52dc3f9fc` (flagchan/tag0, `@publication` released rev 25547)
  and `57601851f` (`SWE2-DATA-PUB-ACTLRES-0922` DONE, released
  rev 25590; unused `+0x04`/`+0x06`/`+0x0A`/`+0x0C` closed
  dead-authored, `+0x15` owner-byte provenance named,
  `obj+0x13` taxonomy verified, tag-11 `+0x00` confirmed
  closed). `00363A90(objId,a,b)` =
  `obj+0x08 = (old&0xE9)|(a&1)<<1|(b&1)<<2` (sole caller
  `003E8C50`: bit1 = `+0x14`-hi!=1 authored mode, bit2 =
  activated, bit4 cleared); `00363AD0(id,v)` = bit4 set/clear
  via `003E85B0`/`003E8690`. Flag channel `u8[64]@02F8F23C`:
  bit1 value (`00270130`), bit0 in-progress (`002700F0`),
  bit3 posted + bit2 notify (`0026FAD0` type-2 post, gated by
  `byte[02F8F238]`, queue `02F8F228`, channel `02F8F23A`);
  `02D8F23C` was a transcription slip. Folded in: YM00 tag-0
  rows closed — 390,136-row census: scaled basis axes
  (233,546 orthonormal / 101,170 uniform-scale / 54,699
  aniso-scale / 721 sheared) + `+0x30` origin; `002F5550`
  composes `RotY(θ)·tag0` (unparented, `002F6013`) or
  `tag0⁻¹·parent·tag0` (parented, `002F5EF8` via `00202D60`
  inverse) — the row is the joint frame; `002F70CB`/`002F67C0`
  read only the origin.
- **Prior package:** MP-2 `003E8350` mask provenance —
  **PUBLISHED `b8ce7ce67`** (`SWE2-DATA-PUB-8350MASK-0922` DONE,
  `@publication` released rev 25488). No stored bit: `003E8350`
  composes `{1: w0 bit4; 2: +0x02 slot 004735E0; 4: +0x0E
  0026FDB0==2; 8: +0x08 member charge pending; 0x10: +0x10 obj
  00362E30 bit0}` live; bit8 arm = `003E8190` list-any
  (bit14) or `0037B030` direct, itself the tag-6→tag-3
  two-hop → `member+0x28 > +0x2C`; miss → `tag3[0]`;
  `003E82A0` = the `0037B030(0,id)` trampoline.
- **Prior package:** UQ-76 typed-list census completion —
  embedded `mrppack_ys.bin` half + type-6 body read — **PUBLISHED
  `516ea7f41`** (`SWE2-DATA-PUB-TYPE6CENSUS-0922` DONE,
  `@publication` released rev 25470).
  New artifact `02-Resource-And-Asset-Pipeline/members/
  gen_listtype_census_embedded.py` → `listtype-census-embedded.tsv`:
  all **228 `MRP` units** across the ten locale packs (32-slot offset
  table, `0xFFFFFFFF` unused; 23 units ×9 packs + 21 in `in_sdver`),
  zero malformed units / zero walk misses — every unit's `sum(count)`
  item walk lands on its own `+0x08` items-blob end within a zero pad.
  Embedded histogram {1:2396, 2:17088, 4:1997, 5:3001, 6:46, 7:258,
  8:537} over 6,207 records / 25,323 items; corpus total 30,546 items
  matches the atlas-name census exactly. **Type-6 body read:** all 46
  items are 0x18 B in the type-5 text shape with `stringId =
  0xFFFFFFFF` (the `+0x14` −1 no-string sentinel) — **type 6 = the
  compiler's disabled/blanked text slot; type 3 is never emitted
  anywhere; type 9 also ships zero**. That closes UQ-76's "why two
  empty ids" and the last MP-2 slot-15 residue. Doc census-note +
  UQ-76 row + MP-2 residue + audit 0922 updated.
- **Prior package:** MP-2 `LGT2` member `+0x12` kind
  semantics + `003CC5F0` curve evaluator — **PUBLISHED
  `8a9542d17`** (`SWE2-DATA-PUB-LGT2KINDS-0921` DONE,
  `@publication` released rev 25387). Folded in the same
  commit: tag-30 `+0x16`/`+0x28`/`+0x2C` closed dead-authored
  (`+0x28`/`+0x2C` = 0 in all 764,018 records; `+0x16` unread
  by every tag-30 consumer — `002F4520`, `002F5550`,
  `002F67C0`, `002F6AB0` tail, `002F7380`). `0037A5B0(member+0x10, group)` = the
  channel evaluator (gate `+0x13` bit1, dispatch `+0x12`):
  kind-0 (5157) static authored `+0x30/34/38`; kind-1 (653)
  s16 lerp `{+0x14..+0x18}`→`{+0x28,+0x2A,+0x2C}` by
  `00466BF0()` = tag-23 slot `f32[obj+0xA8]`·0.01, ×1/128;
  kind-2 (50) `+0x14/16/18` = consecutive i16 triples into the
  tag-5 u32 offset table → `003CC5F0` piecewise-cubic curves
  evaluated at charge `+0x2C`, clamped [-1,1]. `003CC5F0` =
  `{keyFlag@4; tFirst@8; vFirst@0xC; tEnd@0x10; vEnd@0x14;
  keys@+0x38 stride 0x24 {span@0; c3..c0 @+0x28..+0x34}}`.
  Census: 50/50 consecutive triples, 150/150 indices in bounds,
  tag-5 bodies mod-4 ×212, all 123 tag-2 records count=0 (the
  `0037AF4D` kind-gated walk is dead on shipped data — its
  `+0x12` byte is the tag-2 ENTRY kind, not member kind).
  Doc §2.1 member table + tag map + OQ + audit 0921-o.
- **Prior package:** MP-2 `SP1` listener grid +
  variant selector + `+0x1C` dead-data closure — PUBLISHED
  **`7faba5e17`** (`SWE2-DATA-PUB-SP1GRID-0921` DONE,
  `@publication` released rev 25349; foreign-header allowance
  for EC7-119's parked batch-84 section + ADDRESS-INDEX's
  generated heading). `+0x08` names one 0x220 record
  `{f32 cellW,cellH; f32 minX,minZ; u32 16,16; u16 grid[256]}`
  in all 456 packs; `00362E50` bounds-checks listener (x,z),
  divides/clamps to cells, returns `SP1 + u16[+0x20 +
  2*(idxX+idxZ*16)]` = a bit15-terminated u16 emitter-index
  list in the `+0x20` region (0 bad offsets / 0 out-of-range
  corpus-wide; 39,080/116,736 empty; lists 1-17). Driver
  `0x362ACE`: mark all (bit6) → eval → `003631B0` over cell
  list then arena-head default `{0x8000}` → `002DF410(1,0xB4,
  idx)` → clear bit3. `00265920` = the already-named
  `WorldField_GetCurrentWeatherSlot1To3WithDebugOverride`
  (weather-slot-state-model.md; `+0xAAC` debug override else
  saveImage `+0x1060`+1) — indexes `+0x0C` volume triple +
  `+0x20` variant lists. `+0x1C` = dead authored (zero
  accesses across the whole consumer family). SP1 surface
  fully closed. Doc §2.3 + OQ + audit 0921-n.
- **Prior package:** MP-2 `ACTL` member objects are
  authored `LGT2` records — PUBLISHED **`25c89793a`**
  (`SWE2-DATA-PUB-LGT2-0921` DONE, `@publication` released
  rev 25313; foreign-header allowance for EC7-118's parked
  batch-83 section + ADDRESS-INDEX's generated heading). The `02EBF420` group table is the **LGT2 runtime**:
  `0037AA90(block, group)` gates on `'LGT2'` magic, resets via
  `0037B230`, stores the block at `group+0x00` — slot-17 binder
  → group 0, `0032F1B0(idx)` installs `qword[022C6E20+idx*8]`
  into groups 1–4. Members = authored records at
  `block+i*0x70` (`member[0]`'s first 0x10 B = the file header:
  `'LGT2'`/`u16 subChainOff`/`u16 memberCount`;
  `subChainOff == 0x10+cnt*0x70` in all 212 packs); a
  `{u16 size,u16 tag}` sub-chain fills group `+0x08..+0x38`
  (tags 0–7 → `+0x08`/`+0x10`/`+0x18`/`+0x20`/skip/`+0x38`/
  `+0x28`/`+0x30`; corpus {3:212,5:212,6:211,0:198,2:123,7:20}).
  **`+0x28` writer question CLOSED — authored data**: kind-2
  members (50/5,860) carry real f32 limits (100/10/240/30) +
  authored-0 `+0x2C` accumulator; kind-0/1 carry packed
  non-float payloads there (union). Member `+0x12` kinds
  authored {0:5157, 1:653, 2:50}. Fixups: `+0x31` remap <6
  via `01EF94E4`, group-0 `+0x37 |= 0x20`.
  **Charge consumer CLOSED** — `00355300` is the `animesync`
  verb (0x214) poll: returns `003E82F0(id)!=0` (mask bit `0x08`
  = kind-2 member still charging); the retag/bit3/phase verbs
  are `animeplay`(0x213)/`animepause`(0x218)/`animepauseclear`
  (0x219)/`animeplaytiming`(0x280) per `scriptvm-verb-table.tsv`.
- **Prior package:** MP-2 `YM00` tag-22 `+0x38` tail
  closure + `ctx+0x20C` dissolution — PUBLISHED **`a0a479da8`**
  (`SWE2-DATA-PUB-TAG22TAIL-0921` DONE, `@publication` released
  rev 25225; foreign-header allowance used for EC7-117's parked
  batch-82 section + ADDRESS-INDEX's generated heading).
  The tail is **dead authored data**:
  `ctx+0x180`'s sole reader `002F4520` aims the record pointer
  at `rec+0x30` (`(off16+3)·16`; the `inc` on `tag30+0x00`
  skips the index's own count dword — `index[k]` verified on
  all 764,018 refs) and dereferences only `+0x30`/`+0x34`.
  `002F5550` never touches `+0x180`. Tail = a retired PS2
  VIF/GIF packet stream (HIGH as dead; format attribution is
  byte-pattern HYPOTHESIS): rec len 0xB0–0x7E380, `+0x38` u32 ∈
  {23 (96.4%),7,21,31,17,19,5,15} all odd <32, `+0x3C`=0,
  `+0x40` fixed `04 04 00 01 01 80 NN 6c` head, `0a c0 NN 6e`
  UNPACK runs of packed `7f7f7f80`-style quads + f32s. Live
  surface = 8 bytes/record. Same package: **`ctx+0x20C`
  dissolved** — never a field; it's the high dword of
  `qword[ctx+0x208]`, the unowned third member of the
  `{ptr,ptr,qword}` block at `ctx+0x1F8` (`002F5450`
  free-and-nulls `+0x1F8`/`+0x200`; sibling block at `+0x1E0`).
  Sole touch = init `002F6C22`; no reader/populator anywhere.
  Doc §2.2 paragraph + census row + §3.5 arm row + residue +
  method-slot tail paragraph + OQ + audit 0921-l.
  **Follow-on published (0921-m) — `4b4661682`**
  (`SWE2-DATA-PUB-RESUME-TAG22TAIL-0921` DONE, `@publication`
  released rev 25262; foreign-header allowance for OPUS's
  parked navigation-teardown question in OPEN-QUESTIONS):
  `SP1` `01F83530`
  re-attributed — NOT a sound-list cursor; it is the
  engine-wide `0020E600`/`0020E620` offset-decode base
  (~815/~279 callers), BSS-zero and statically unwritable
  (CD-2/UQ-83; independently re-verified + extended: no
  absolute-addressing form, no overlapping rip-rel store, no
  intra-function carried-base access). `00363B40`'s fallback
  reads `SP1 + [SP1+0x04]` = `SP1+0x20` (the `{u32 count;
  i32 idx[]}` list); variant selection is `00265920()-1`
  into the dedup gather array `022CBB58`/`022CBB70`.
- **Prior package:** MP-2 `YM00` tag-0 matrix +
  tag-33 fade chain — PUBLISHED **`41126929a`**
  (`SWE2-DATA-PUB-TAG0CHAIN-0921` DONE, `@publication`
  released rev 25098). `ctx+0x188` xref scan:
  tag-0 rows = **4x4 row-major transform matrices** (`{u32
  count; 12B pad; count x 0x40}` — `0x10+count*0x40`==size in
  all 461; rows 0-2 basis w=0, row3 translation w=1.0, all
  390,136 verified); `002F5550` hands `word[tag30+0x02]*0x40`
  rows to `00202D70`->`00217150` 4x4 multiply. `002F5550` per-
  record gates decoded (+0x20 mask skip, flag b28 inverted
  enable, +0x0A dead-authored 0 in all 764,018, +0x14 -> tag-24
  0xE0 entry: +0xBC/+0xC8 cull floats, +0xC0 byte-bitmap ptr —
  b30 writes {1,2} threshold states). **`002F67C0` = distance-
  gated fade**: u16 sel (&0xFFF) -> tag-33 authored 0x10 recs
  `ctx+0x1A0` `{+0x02 tag0Row; s16 +08/+0A/+0C extents x
  1/4096}`; sqrt(dx^2+dz^2)+dy vs row +0x30 position; runtime
  `0xC` rec = `{u32 enable; i32 state; f32 accum}` hysteresis
  integrator. Chain tag-30->tag-29(+2 sel)->tag-33->tag-0.
  Doc census rows + 002F5550 paragraph + §3.5 rows + OQ +
  audit 0921-f. Gates: doc_claims mover = peer files only.
- **Prior package:** MP-2 `YM00` tag-30 residual-field
  decode in `002F4520` — PUBLISHED **`42d0a9c15`**
  (`SWE2-DATA-PUB-TAG30FIELDS-0921` DONE, `@publication`
  released rev 25074). Second pass closes:
  `+0x1C` = **bit index into the `0026E5F0` 64-bit fold**
  (`dec al; cmp 0xFD; ja` rejects 0/0xFF, else `bt rax,bit`;
  corpus 0xFF ×762,837/764,018 = 99.8% — corrects the
  "≈0xFF constant" note); `+0x1E`/`+0x1F` = u8 pair
  multiplied → negated → `cvtdq2ps` → `00180890` float arg;
  `+0x17` = flag-seed byte (0x60 dominant + 0x80/0x02/0x01/
  0x64/0x3F — so u16 `0x6014` was the dominant pair, not a
  constant; `+0x16` remains semantically unnamed); flag **b30**
  routes `word[rec+0x02]` into **tag-29** `0x10`-stride records
  (`word[+idx·0x10+2]` → u16 → **tag-33** `0xC` array `+8` f32
  threshold vs `xmm12`; negative → default) — `+0x02` is
  dual-role (tag-0 row at load / tag-29 idx at update; 39,690
  b30 records). Context obj `[rsp+0x78]`: feature mask at
  `+0x40` (b10→`+0x98` f32, b11→`+0xA0` f32 negated, b13-17→
  mode override), frame float `+0x90` drives tag-26 entry
  reselection (+edi, clamp `dword[buf]`, `word[entry+0xC]`
  successor check → `001807F0`). Doc §2.2 field table +
  `002F4520` paragraph + §3.5 tag-29/33 rows + OPEN-QUESTIONS +
  audit 0921-e.
- **Prior package:** MP-2 `YM00` tag-22 consumer +
  record-semantics decode + method-slot roles — PUBLISHED
  **`caa703f9b`** + **`19ea6d9b2`** (`SWE2-DATA-PUB-TAG22-CONSUMER-0921`
  + `SWE2-DATA-PUB-METHODSLOTS-0921` DONE, `@publication`
  released rev 25033/25049). `002F4520` (method callback `ctx+0x130`) is the
  sole `ctx+0x180` reader: walks a u16 id list, resolves
  tag-30 src + `0x70` runtime entry, dereferences tag-22 via
  tag-30 `+0x00` (a **deduplicated index** `< n22` in all
  764,018 — correcting the "sequential ordinal" note) through
  the nested index: `rec = chunk+(index[v+1]&0xFFFFFF)·0x10+0x30`.
  Record = `{vec4 AABBmin(w1); vec4 AABBmax(w1); vec4(128×4);
  u32 axisMode; u32 period; …}` — 348,239 records, mode
  0=static 97.2% / 1=Y / 2=XZ / 3=XYZ, period ∈{2,3,4,6,8}
  iff mode≠0; `phase mod period` → vec3 lanes → `00180720`/
  `001A9B70` apply = **per-instance oscillation/mover spec**.
  AABB header + `+0x38` tail unconsumed (residue). Doc §2.2 +
  §3.5 arm row + OPEN-QUESTIONS + audit 0921-d +
  `gen_ym00_tag2226_census.py` mode histogram (TSV regenerated,
  920 rows / 0 failures).
- **Prior package:** FABLE prefetch-selector
  contradictions — ADJUDICATED + PUBLISHED **`69c817bba`**
  (`SWE2-DATA-PUB-PREFETCH-SEL-0921` DONE, `@publication`
  released rev 25003). Filings UPHELD: `0x001DA758`/`0x001D9B75`
  pass selector 0 opening the manifest *files* (`xor r8d`
  verified); the per-token request is the `0x001DA810`–`0x83F`
  loop in `001DA610` (`r8b=5`, then `0059BD40` teardown +
  `00598100` dtor — resolve-and-mark, never read). Independent
  20-site `E8` census: 0×5, 1×11+2 flag-derived, 5×1
  (`001DA81B`), `r14+3`×1 (`001DAFD8` → 3 or 4, **not** 24 as
  the filing's figure had it). `how-the-prefetch-manifests-
  are-read.md` §3/§4/§7 corrected; audit 0921-c;
  FABLE-CONTRA/-AMEND/-REQ-WINDOW all finished on the board.
- **Prior package:** MP-2 `YM00` tags 22/26 nested-
  container + TIM2-bank decode — PUBLISHED **`6a25d25ac`**
  (`SWE2-DATA-PUB-TAG2226-0921` DONE, `@publication` released
  rev 24983). Both tags are
  `{u32 count; (count+1)×{u24 off16|u8 tag}}` nested indexes
  (census 920 rows / 0 failures): tag 26 = named TIM2 bank —
  `{char[0x28] name; u32 picCount; u32 0; TIM2}` ×20,809 in
  459 packs, sentinel = EOF; `00467D20` sums TIM2 picture
  counts → `Σ·0x60` at `qword[qword[ctx+0x150]+8]` (the table
  `002F7380` reselects from), `00536080` walks TIM2 header
  (`+0x05` flag → `+0x10`/`+0x80`, `+0x06` count, len-prefixed
  pics), expanding each picture header into the runtime entry.
  Tag 22 = offset-indexed f32 blocks in all 461 packs →
  `ctx+0x180`; consumer unresolved. §3.5 + §2.2 expansion
  paragraph + `members/ym00-tag2226-census.tsv` +
  `gen_ym00_tag2226_census.py`; audit entry 0921-b.
- **Prior package:** MP-2 `MRP` (slot 15) decode +
  dead-data closure — PUBLISHED **`7a8e81677`**
  (`SWE2-DATA-PUB-MRP-0921` DONE, `@publication` released
  rev 24887). Slot 15
  = standard `MRP` container (`mrp_menu` family): 5 rect
  descriptors, 2-name tail, corpus-unique populated table B
  (2×`{1,len,relOff}` → `{char[16] name; TIM2}` gauge
  textures tiling to EOF), byte-identical across its only 2
  packs (`rwg0201`/`rwg0202`). Dead: `02ADD058` 4 rip refs
  (store/teardown/getter), `00408300` `movsxd`-truncates to
  dead create-param `+0x10`, `00406E80` never reads it in
  any branch, zero `4D 52 50` in `.text`, no map-side loose
  `.mrp`. §2.5 + `members/mrp-census.tsv` + `gen_mrp_census.py`;
  audit entry 0921-a.
- **Prior package:** MP-2 `WD` (slot 1) decode +
  dead-data closure — PUBLISHED **`1c7422d17`**
  (`SWE2-DATA-PUB-WD-0920` DONE, `@publication` released
  rev 24838). Wave-bank container (bankId/dataSize/count×2/
  flags header, `align16(0x20+4N)` offset table, 0x20-stride
  A/B record pairs `{0,X,Y,0x5FE800FF|hash,0x407F7F3C,0,0}`,
  blob-relative X/Y positions, 16-byte-block ADPCM) over all
  46 sections; **dead authored data** — freed unread both
  modes (`003697F0`), `02ADD070` store-only, no `0x4457`
  compare, no loose file. §2.4 + `members/wd-census.tsv` +
  `gen_wd_census.py`; MP-2 narrowed; audit entry 0920-g.
- **Residue:** `WD` X/Y roles (no consumer — corpus interpretation
  documented), `MRP` item type codes CLOSED corpus-wide (type 6 =
  blanked text slot, type 3/9 never authored — embedded census
  artifact), `SP1` surface CLOSED
  (listener grid = 16×16 area at `+0x08`; `+0x1C` dead; prefix
  list = the bit15-terminated emitter-index-list encoding;
  `00265920` = named weather-slot getter; `01F83530`
  re-attributed to the universal decode base),
  `ACTL` mask-bit `0x08` CLOSED — no stored bit; `003E8350`
  composes it live via `0037B030`'s `member+0x28 > +0x2C` charge
  test (tag-6→tag-3 two-hop, miss → `tag3[0]`; `003E82A0` =
  the `0037B030(0,id)` trampoline `003E8190` calls per row
  member). LGT2 fully closed (kinds + all sub-record
  interiors).
- **Prior package:** MP-2 tag-30 record census + 0x240
  context — PUBLISHED **`190cf75ca`** (`SWE2-DATA-PUB-TAG30-
  CENSUS-0920` DONE, `@publication` released rev 24615).
  Tag 30 = u16-field row (764,018 records); YM00 ctx = 0x240
  `003EC8D0` arena block (`0026E760` mode-1 / `0026E7D0`
  mode-0 → `0209A668`); tag-30 consumers read ctx `+0x174`/
  `+0x178` downstream — residue.
- **Prior package:** MP-2 `YM00` per-chunk semantics pass 1 +
  `003E8AA0` mode callers — PUBLISHED **`7b32b9d42`**
  (`SWE2-DATA-PUB-YM00-CHUNKSEM-0920` DONE, `@publication`
  released rev 24589). Tag 11 = 0x20-live-byte environment
  record (override dword/RGBA/2 scalars/vec4, `0209A660` + 4
  lazy readers); tag 0 = `{count; count×0x40}` vec-table
  (three vec3+0 + position vec4, w=1.0 in 390,136 rows);
  strides 24=`0x10`/30=`0x30`/33=`0x10`(43)/1=`0x30`(11);
  all 17 arm store targets re-verified; `003E8AA0` mode =
  `+0x15` signed group tag.
- **Latest package:** MP-2 tag-11 `+0x00` correction + `ACTL`
  `+0x15` writer / family enumeration / `+0x12` kind-nibble
  closure — PUBLISHED **`ae6feb70f`** (`SWE2-DATA-PUB-TAG11RGBA-
  0921` DONE, `@publication` released rev 25127). Tag-11 `+0x00`
  = packed RGBA quad (div-255 in `0036D400`, `0xFFFFFFFF` =
  keep-previous). ACTL: `003E88C0`/`003E8900` retag `+0x15` from
  `byte[callerCtx+0x15]` via `00354710`/`00354AD0`; all 17 refs
  to base `02B5D080` enumerated (`003E8190` member driver,
  `003E8A70/8A10/8A40` stubs, ranged variants, `003E82B0`
  teardown); `+0x12` kind nibble = dead-authored metadata.
- **Latest package:** MP-2 `ACTL` member-object charge timer +
  `02EBF420` base fix + `SP1` emitter-field decode —
  PUBLISHED **`2ac0ca5d5`** (`SWE2-DATA-PUB-ACTL-OBJTIMER-0921`
  DONE, `@publication` released rev 25167). Group table = 5 x
  0x50 at `02EBF420`; member objects 0x70-stride:
  `+0x13` {b0 suspend, b1 charging, b2 re-arm}, `+0x28` limit,
  `+0x2C` accumulator (+1.0/tick `0037A450`). SP1 emitter:
  volMax/volMin/variantPct/range/point-count/rt-bytes all
  decoded; `+0x1C` sole unread authored field.
- **Current package/claim:** hdat line-builder decode — **PUBLISHED
  `cb2c84adb`** (`SWE2-DATA-PUB-HBTAIL-0922` DONE, `@publication`
  released rev 25982): `00576300` gates each `strOff` slot through
  `00576E30` (strOff↔hchk slots 1:1), record tail → `out+0x48..+0x4E`,
  blob-entry `word[+0]` = textOff (`0xFFFF` = empty → `01CEB638`);
  tail `v1`/`v2`/`v3` confirmed dead-authored (full `root+0x108`
  consumer enumeration).
- **Prior package:** handbook consumer closure — **PUBLISHED
  `30dd8698f`** (`SWE2-DATA-PUB-HBTAB-0922` DONE, `@publication`
  released rev 25968; carried EC7-126's complete parked batch-91 audit
  section under the documented allowance): `00576CA0` = family-tab
  availability flag (binds `root+0xF8` menuquest consumer), hctg
  `+0x08` hi12 dead-on-path (unread by all three `00576030` callers),
  `hchk +0x03` confirmed dead marker, `00570BF0`/`00571F60` = the
  list-extent/row-builder UI consumers.
- **Prior package:** hctg sectioning closure — **PUBLISHED
  `c712f8cfe`** (`SWE2-DATA-PUB-HBSEC-0922` DONE, `@publication`
  released rev 25956): `rec.group` = section index into the `+0x18`
  conditional-caption table (0..captionN−1 corpus-exact on all 54
  files), `+0x12` = section count, `00576740` = section-header
  resolver, `005766E0` = group accessor. Also `1b1aee01d` (arg byte =
  locale-invariant global serial, no reader; `00577970` = record→page
  bridge; hctg duplicate records recorded).
- **Prior package:** hctg record `+0x04` bind — **PUBLISHED
  `5739a439a`** (`SWE2-DATA-PUB-HBREC-0922` DONE, `@publication`
  released rev 25930). Record = `{u32 textId; u16 group; u16 hdatFile;
  u16 index; u8 flag; u8 pad}` — only textId space + `+0x0B` pad open.
- **Prior package:** hctg page-map decode — **PUBLISHED
  `6715ccbd5`** (`SWE2-DATA-PUB-HBMAP-0922` DONE, `@publication`
  released rev 25927; carried EC7-125's complete parked batch-90 audit
  section under the documented allowance).
  `00575DD0` reads `word[hctg + word[+0x0C] + pageIdx·2]` (page→
  resource-slot map, `+0x10` = pageCount bound, `+0x16` = slot bound,
  map max = +0x16−1 on all 54 files); `00575C30` computes resource id =
  `familyBase[00D23740+kind] + word[widget+0xCA] + sel`; buffer graph
  closed (+0x108 hctg / +0x110 hdat / +0x118 himg).
- **Prior package:** handbook strBlob decode —
  **PUBLISHED `27faf2401`** (`SWE2-DATA-PUB-HBSTR-0922` DONE,
  `@publication` released rev 25907). `00577A40(root, slot)` = the
  hdat strOff[] reader on bound-hdat `root+0x110` (`obj+0xCE` =
  selected record's global ordinal, window-checked): entries =
  `{u32 04_00_00_00; section-002-encoded NUL text}` and the executor
  interprets the header as an op-program writing the `+0x336C`/
  `+0x334C` banks — **nOps=0 in all 12,168 shipped entries**
  (dead-on-ship machinery); hdat records = program+text tables, not
  display strings.
- **Prior package:** handbook detail-resolver decode —
  **PUBLISHED `39426d811`** (`SWE2-DATA-PUB-HBDETAIL-0922` DONE,
  `@publication` released rev 25889).
  `005760A0`/`00576030` disassembled: the monster `hctg` tail's native
  reader FOUND (`0x57625F`: tailbase = `hctg + recTableOff +
  recordCount·12`; byte 0 of the 8-byte aux record = the hchk slot
  count driving `00576860` materialization into `out+0x18` — explains
  the 384/384 `v0 == hdat strCount` join); name resolution split
  (`002F9920` vs monster `bank:index` `002B58B0(003214B0(textId),0)`);
  Esper subtitle table `00D23790` (13 dwords, `textId 0x4210..0x421C`
  → `0035D330(entry+0x106)→+0x18`); `rec+0x0A` flag == 1 exactly on
  `v3∈{0,1}` (172 records); `out+0x16` = live kill counter
  `00315420(recIdx)`; `obj+0xD2` = family ordinal.
- **Next action:** commit `op_fin_hbtail.json` + this resume update
  in the next publish window; take the highest-value unblocked item
  per the board.
  Handbook residue is now thin: `hctg` record `textId` space +
  `+0x0B` pad; `hchk` `+0x0A` (locale-invariant 18 lore /
  0 tutorial,monster — no consumer); `hdat` `arg` semantics (global
  serial, dead-on-path); whether strBlob ops ever authored (nOps=0
  everywhere).
- **Prior package:** carry commit **PUBLISHED `ecfd71e54`**
  (`SWE2-DATA-PUB-HBCARRY-0922` DONE, `@publication` released
  rev 25866): tail v0/v3 joins + hchk +0x0A invariance in the doc.
- **Prior package:** `hctg` aux-region decode — **PUBLISHED
  `8ab8c7e10`** (`SWE2-DATA-PUB-HBAUX-0922` DONE, `@publication`
  released rev 25843). `00576A50` = the conditional-entry resolver:
  `hctg +0x18` `u32 textId[captionN]` + `{u16 count; u16 relOff[]}`
  gate-blob sub-table; gate blob = `{u8 condCount(hi nib); u8 navCount;
  u16 condId[]; u16 navId[]}`; conditions via `00309EC0`, navimap ids
  via `003148F0`/`003779F0`/`00255120`/`00255060(0x20)`; any pass →
  caption `002F9920`, all fail → placeholder `0x3EC` `002F9860`;
  only monster ships nonzero blobs (32 entries). Monster hctg tail at
  0x168C: `{u16 count=384; u16 relOff[]}` → 8-byte aux records.
- **Prior package:** MP-2 closure PUBLISHED as `bd9b572a5`
  (`SWE2-DATA-PUB-MP2CLOSE-0922` DONE, `@publication` released
  rev 25603).
- **Prior package:** MP-2 corrections + tag-30 expansion +
  per-bank consumer — PUBLISHED **`60b6ee298`** (`SWE2-DATA-
  PUB-SEL-CORR-0920` DONE, `@publication` released rev 24683).
  `01F83530` VA fix; `YM00` `+0x04`/`+0x08` = unread export
  metadata; tag-30 `0x30` recs → `0x70` array `ctx+0x1C0`
  (flags dword/`+0x14` tag-24 link/`+0x18` RGBA/`+0x02` tag-0
  row/`+0x20` slot mask vs tag-23's `02EBB6E0` family =
  `ACTL` `+0x02` space); `002F7380` per-bank reselection
  (`+0x04` tag-26 entry idx, `+0x0F` bank mask, `+0x1D`
  variant → `ctx+0x218` active set).
- **Prior package:** MP-2 `ACTL` record-field semantics
  DECODED + PUBLISHED **`250ac2264`** (`SWE2-DATA-PUB-ACTL-
  SEMANTICS-0920` DONE, `@publication` released rev 24563).
  `003E8020` first-touch = state machine: stamps `+0x12`
  {phase=3|kind}, swaps `+0x13`/`+0x14` arg nibbles,
  activates `003E8C50` {b0=1,b1=0,b2=0}; later passes
  alternate `003E85B0`/`003E8690` on w0 bit1 with `003E8350`
  query (result mask 8/4/0x10) gating re-activation.
  `003E8440` init primes `+0x02` (148542.5 + raw 0x000140C1);
  `0037A500` snapshot copies obj+0x28→+0x2C on kind-2.
  Targets resolve via `02E2F420` group table (0x50 groups →
  member lists → 0x70 objects) → `obj+0x13`; aux table =
  {i16 bound;i16 rowOff[]}→{u16 count;u16 memberIds[]},
  ACTL-relative. §2.1 rewritten; MP-2 narrowed.
- **Prior package:** MP-2 `SP1` (slot 16) container + emitter
  record DECODED — three-region header, `{u16 bound; u16
  recordOff[]}` index, variable-size records, SP1↔SPP1 global
  split corrected. Published **`29a66464c`**,
  `SWE2-DATA-PUB-SP1-CONTAINER-0920` DONE.
- **Prior package:** MP-2 `YM00` (slot 8) container DECODED —
  fixed 17-slot tagged-chunk schema, 461/461 zero-remainder.
  Published **`b86c81e76`**.
- **Prior package:** MP-2 `ACTL` (slot 9) container DECODED —
  two-level id-indexed record list, 270/270 zero-remainder,
  1,822 records censused. Published **`4bc1a44eb`**.
- **Prior package:** Y-2 (uisize schema↔data↔code) ANSWERED —
  zero-remainder three-way join. Published **`42d86554b`**.
- **Prior package:** UQ-380 composed-name route, static half
  CLOSED (self-directed fallback) — literal/table composition
  disproven (18 supply sites, `can_compose = 0`), residual is
  runtime-built names only. Published **`76ee9203c`**.
- **Prior package:** `FRONTIER-REQ-SWE2-DATA-NONFUNCTION-
  ANNOTATION-EXPORT` **DONE** (revs 24246/24247), published
  **`726ae2555`**; plus `OPUS-REQ-SWE2-DATA-YOUR-TWO-SECTIONS-
  IN-MY-INBOX-ARE-UNCOMMITTED` **DONE** (rev 24271 — both
  sections final, carry authorized).
- **Prior package:** five tasks **DONE** at board rev 24223,
  package published **`ff2b22c6f`** (25 files): voice-cue arg
  census + GA-3 correction, seqrec eqcount 7,095->7,086, AY-8
  CJK verified, BU-5 verified (296/689), parent-residual ruling.
- **Prior package:** five tasks **DONE** at board rev 24223,
  package published **`ff2b22c6f`** (25 files): voice-cue arg
  census + GA-3 correction, seqrec eqcount 7,095->7,086, AY-8
  CJK verified, BU-5 verified (296/689), parent-residual ruling.
  `OPUS.md`/`FABLE.md` notices stay uncommitted (foreign parked
  sections; their next publishes carry my returns).
- **Prior package:** five tasks **DONE** at board rev 24223,
  package published **`ff2b22c6f`** (25 files): voice-cue arg
  census + GA-3 correction, seqrec eqcount 7,095->7,086, AY-8
  CJK verified, BU-5 verified (296/689), parent-residual ruling.
  `OPUS.md`/`FABLE.md` notices stay uncommitted (foreign parked
  sections; their next publishes carry my returns).
- **Prior package:** six tasks **DONE** at board rev 24169,
  package published **`81278ca35`** (44 files): CONTRA seqrec +
  CONTRA listtype-type6, SCRIPT-NATIVE-ARG1 (attach),
  DAT-SEPARABLE, REGENERATE-STALE-FAMILY-SELECTORS,
  ACTORDEFINITIONPAYLOAD-HEADER-GAPS. Two tails outstanding:
  **(a)** `OPUS.md` left out of `81278ca35` (OPUS's parked
  sections; their next publish carries my Returns). **(b)** board
  tail — `TEAM.json` + the seven `op_fin_*` files — unpublished;
  FABLE took `@publication` when the pub task released it. Next
  free window: claim and publish.
  Next action: claim `@publication`, publish the voice-cue package
  + the outstanding board tail; then finish the request.
- **Latest coherent commit:** `1f9f37678` (handbook index family).
  This resume update + `op_fin_hbindex.json` ride the next publish.
- **Pending reviews:** `DATA-REQ-AUDIT-SPEC-SETTINGS-COMMANDS`
  (READY → SWE2-AUDIT-SPEC, rev 19802, first review per request);
  `DATA-REQ-AUDIT-SEM-SNDCLASS-REVIEW` (READY → SWE2-AUDIT-SEM,
  rev 19924); `DATA-REQ-AUDIT-SPEC-LOADER-BOUND-BINS` (READY →
  SWE2-AUDIT-SPEC, rev ~19982, first review per request);
  `DATA-REQ-AUDIT-SEM-REQCHANNEL-REVIEW` (READY → SWE2-AUDIT-SEM,
  rev 20064); `DATA-REQ-AUDIT-SEM-CYCLEKEY-REVIEW` (READY →
  SWE2-AUDIT-SEM, rev 20102); `DATA-REQ-AUDIT-SEM-LISTTYPE-REVIEW`
  (READY → SWE2-AUDIT-SEM, rev 20151).
- **Just completed (pending publish):** `FABLE-REQ-SWE2-DATA-
  ATLAS-NAME-CLOSURE` — **EW-6(a): three authored names are
  permanent misses** (`logo_s_c`, `nowload_c`, `title_c`). 344
  typed lists (116 standalone `.mrp` + 228 `mrppack_ys.bin`
  units), 7,665 records, 30,546 items, 20,459 refs → 28 names:
  25 literal-registered, 0 file-row (units 13–16 `+0x24` all 0 —
  path authored-empty), 0 `loca_%d_%d`; zero OOB, zero required
  `0xFFFF`. Also identified the `+0x24`/`+0x28` header fields as
  the file-row registration table (§5d) and resolved all seven
  untraced wrapper sites to literals. Artifacts:
  `members/{atlas-name-census.tsv, gen_atlas_name_census.py}`.
- **Previously:** `FABLE-REQ-SWE2-DATA-LIST-TYPE-ID-CENSUS`
  **DONE** (rev ~20150), published `9f691756`. **UQ-76 authored
  half closed: types 3 and 6 never ship — nor does 9.** Item
  bytes are a contiguous `{u8 len,u8 type}` stream after the
  outer table; walk lands on `+0x08` within zero pad in all 116
  `.mrp` (1,458 records, 5,223 items). Histogram {1:265, 2:3093,
  4:20, 5:1483, 7:20, 8:342}; max bits10-27 = 59; bit28 clear in
  55 records (corrects FABLE narrowing). Artifacts:
  `02-Resource-And-Asset-Pipeline/members/{listtype-census.tsv,
  gen_listtype_census.py}`; census note under UQ-76. Also closed:
  `OPUS-REQ-SWE2-DATA-TWO-STAMPS-DATED-TOMORROW` (`622e24f4`).
- **Previously:** `FABLE-REQ-SWE2-DATA-CYCLESOUND-KEY-BYTE-CENSUS`
  **DONE** (rev ~20101), published `35922615`. **UQ-259 authored
  half closed: the shipped Sequence key byte is always 0, and no
  CycleSound- or SwitchSound-owned list exists at all** — 11,165
  `SabFile::Sequence` records across 4,609 `.sab` banks, all
  version 4, `+0x11 = 0`, `+0x10`/`+0x14 = 0`; zero snd records
  carry class 4/5; every list is length 1, group 0; `.mab` ships
  no `seq ` chunk (0/116). Artifacts: `18-Audio/Sound-Selection/
  members/{cyclekey-census.tsv,gen_cyclekey_census.py}`; census
  note under UQ-259 on `sound-trigger.md`. Loader tail
  `SWE2-DATA-PUB-LOADERBINS-OPS` also closed (`0ddb954f`).
- **Previously:** `FABLE-REQ-SWE2-DATA-REQ-CHANNEL-RANGE`
  **DONE** (rev 20062), published `aee9d467`. **UQ-54/EF-2
  closed on the authored side: zero sites ≥ `0x80`** —
  326,204 channel-carrier sites across 10,036 valid `.ebp`
  containers (237,662 script bodies): `REQ` 197,102, `REQEW`
  101,398, `REQSW` 27,704; `FREQ`/`TREQ`/`FREQSW`/`TREQSW`/
  `FREQEW`/`TREQEW` never ship. Every channel operand is an
  authored `PUSHI`/`PUSHII`/`PUSHI0-3` immediate; low-byte
  dist {0:18, 1:242611, 2:43738, 3:16446, 4:13347, 5:7929,
  6:198, 7:1917}, max `0x07`. Model: channel = first-pushed
  arg = third pop (`sil`→`+0x22` at `002689B1`); `PREQ*` reuses
  `+0x11`. Artifacts: `25-EBP-Script-Container/Bytecode-And-
  Opcodes/members/{req-channel-census.tsv,gen_req_channel_
  census.py}`; closure note in calling-convention EF-2
  paragraph + bytecode sheet §5; answer posted to FABLE.md.
  Decode notes: `0x03`/`0x04` are real unnamed 1-byte ops;
  `CALL` effects modelled from `scriptvm-verb-table.tsv`
  (arity=pops_int+pops_float, result=pushes+result_writes);
  regions bound at `diroff`; sites deduped by (file,pc).
- **Prior completed:**
  `FABLE-REQ-SWE2-DATA-LOADERS-FOR-UNNAMED-FILES` **DONE** (rev
  ~19981), published `4648552c`. New sheet
  `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md`
  + `members/loader-bound-census.tsv` (87 files) +
  `gen_loader_bound_census.py`. All 13 families: the six
  `*pack_ys`/`fontpack_*` share a sentinel-filled u32
  self-relative-offset directory (0x40/0x80-byte, 0xFFFFFFFF fill);
  per-family binder maps — texpack 5 TIM2→named resources via
  `0024A1D0`, tex2pack 11 (10 named + 1 raw→`+0x388`), mrppack 23/21
  MRP→relocator `002A00F0`, clutpack 4 CLT2→`0209AC30+0x390..3A8`,
  fontpack_fs 6-of-7→font state `022CBE00` (slot 3 never bound),
  fontpack_it 6→`02AEE8xx`. Kind-9 objects: behindcamera
  16×0x40→`02097D40`, pc_skillmotion 33×0x10 "PCSkill",
  summoneffectdata→`02AD9B60`. fontcolor `{u32 0x107, u64 colors[]}`;
  monotone_chr two-CLT2 file whose loader **grafts the clutpack_ys
  palette** (`0209AC30+0x390` → `alloc+0x1DC0`) — cross-family
  producer→consumer. `in_sdver` ships shorter dirs (texpack 4,
  mrppack 21). Open: fontpack_fs slot 3, tex2pack slot 10, subtype
  `0x75` has no file. Gates clean (50 cited, 0 unconfirmed).
- **Prior completed:**
  `FABLE-REQ-SWE2-DATA-SOUND-CLASS-BYTE-CENSUS` **DONE** (rev
  ~19923), published `90b1376a`. NEGATIVE-on-variants: over all
  13,150 `snd ` records (4,609 .sab, `{u16 0, u16 0x10, u32 count,
  u32 offsets[]}` chunk directory), byte +4 is 0 in 1,985 / 1 in
  11,165 — no shipped record builds Random/Order/Cycle/Switch; the
  §12 select machinery is dead over the corpus. Class 1 == seq
  record count exactly (candidate-list carriers, +5 always 1);
  class 0 win-only, +5 = 0; +0x19 bit 5 never set. Artifacts:
  `members/sndclass-census.tsv` (13,150 rows) +
  `gen_sndclass_census.py`.
- **Prior completed:**
  `OPUS-REQ-SWE2-DATA-PASS22-SETTINGS-COMMAND-TABLE-ELEVEN-LAYERS`
  **DONE** (rev ~19871), published `07d5455c`. Twelve layers
  dispositioned (OPUS's eleven + World on the fresher graph):
  tail crossings section per §4.2 — Input/Audio SERVICE+CLIENT
  (setter propagation is the claim), CombatAction CLIENT
  (`BattleAction_ComputeChargeProgressStep` reads battle speed),
  CoreRuntimeScheduling SERVICE, Party CLIENT (locomotion chain
  reads bits-0-1), Presentation SERVICE+CLIENT (Target-Lines draw
  path; `001D1660` graphics applier shares the cfg key-map),
  Resource SERVICE, Script_VM_Native_Bridge CLIENT (script natives
  own the no-command fields); OUT-OF-SCOPE rulings for
  ActorEntity/Gameplay/Rewards/World. Twelve CROSSING-ACCOUNTED
  registry rows; audit re-run on the page: **0 findings**.
  `FABLE-REQ-SWE2-DATA-OPTIONS-BIT3-STATIC` **DONE** (rev ~19870),
  already satisfied by `8a5bc471` + FABLE's SM-5 answer; closed
  AQ-13 in ASTRA-QUEUE (Battle Mode, statically, live request
  withdrawn).
- **Prior completed:**
  `FABLE-REQ-SWE2-DATA-SETTINGS-COMMAND-TABLE` **DONE** (rev ~19801),
  published `8a5bc471`; `@publication` released rev 19800. Full
  19-command decode on
  `19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md`
  + `members/settings_command_table.tsv` + `gen_settings_commands.py`
  (regenerates TSV from image + pools). Both 35-slot dispatchers
  mapped (`002407F0`/`002403F0`, tables `00240968`/`00240518`):
  19 handled ids via 21 callees — cmds 8 and 14 are compound
  (8: `002DE1E0`+`002DE1C0` writes opt+0 bits 15/16; 14:
  `002DE250`+notifier `0023B2E0`). Cmds 4–21 → save-backed options
  record `*(0215E6E0)`; 28–30/38 → `GameSetting.ini` slots 22–25 via
  `001DF340` (CameraRevise/MouseSensityY/X/DecideButton). Row path:
  `01E0BF60` descriptors → pane repeater `0023ED80` → procs
  `0023D6B0`/`0023DB40`/`0023E770`/`0023EBE0` → wrappers
  `00240750`/`00240330` sharing one 35-byte selector table (inverse
  transforms). Labels decoded from shipped st2e pools
  (menu_command/menu_message/help_menu) with cstring-at-offset
  reads — offset array is non-monotonic; five "empty" labels were
  slice artifacts (Target Lines, Cursor Position, Screen Shake,
  Restore Defaults, Reorchestrated). **Command 4 = Battle Mode →
  opt+0 bit 3 (Wait/Active): ASTRA AQ-13 answered statically.**
  Cmd 11 setter is active-low (opt+0 bit 12) but its getter reads a
  live u16 at `0215E6DC` — documented as-is. Unhandled ids
  7/15/18/22–27/31–37 are structural rows; unexported option fields
  (opt+0 bits 0–2, opt+4 bit 21, `002DE150`/`002DE270`) classed
  ini-only/internal. `00240968` adjudicated TABLE in
  text-gap-citations-250.tsv. Gates clean.
- **Prior completed:**
  `FABLE-REQ-SWE2-DATA-VIF-PACKETS` **DONE** (rev ~16488), published
  `5a08ef5c`; `@publication` released. Result: 77 template rows in
  `Legacy-PS2-GS/vif1-packet-templates.tsv` + page §2.4a + generator pair
  in `members/`. The hubs make **75 calls, not 66** — 66 in-region
  (65 distinct builders; `004E3110` called twice) + 9 out-of-region
  (6 MPG builders + 3 plain); 2 further MPG builders are never
  hub-called. Union = 76 builders / 75 objects; 31 in-region builders
  are dual-role (object + `008631E0` MPG record). Command totals:
  STCYCL/UNPACK 87, BASE/OFFSET 58, MSCALF/FLUSHA 50, DIRECT 29,
  FLUSH 26, FLUSHE 0 at command positions (all 56 `0x10000000` stores
  are payload data). GS writes in templates are rare: 28/29 DIRECT
  payloads are empty GIF terminators (`004C2040` carries `CLAMP_1=0`);
  two templates (`00476C80`, `0047BAF0`) end the UNPACK payload with
  `{reg-id, value}` pairs ST/CLAMP_1/RGBAQ/XYZF2=0. Control result:
  **zero unattributed immediate stores** across all 77 builders.
  Gates: verify_doc_addresses clean, check_links clean on my page,
  check_formats 63/63.
  Also closed this session (already-satisfied): the pass-22 supplement
  `OPUS-REQ-DATA-PASS22-THE-CALLEE-IS-A-SEVEN-BYTE-GETTER` (rev 16325,
  satisfied by `a9f60432`) and `OPUS-REQ-DATA-MENUMAP-PAGES-LINK-A-
  GITIGNORED-TOOL` (rev 16332, already fixed by FRONTIER's `ed4c533f`).
  `OPUS-REQ-SWE2-DATA-LABEL-TABLES-FOR-TWO-NAS-ROWS` **DONE** (rev
  ~19536), published `e81760f0`. NEGATIVE result: every shipped
  name/label-table family in the VBF was extracted and scanned for a
  string bound to the field-record bit-15 flag — us/bin name tables,
  all 29 us binaryfile text tables, us menu-resource packages, common/
  + {ch,in}/common tables, {ch,in} .dbg/.sbn/.msb script symbol
  tables, file lists, debglobal. No shipped table binds a label to bit
  15; the only flag-vocabulary strings live in script symbol tables
  and name other things (navimap* minimap builtins, action_flag a
  btlctrl local, getmaptype reads context +0x8a, *nobattletarget verbs
  touch no field-record reader — edge-verified). FLAGDEF15/FLAGROM1
  are map-jump table magic tags, unrelated. Report:
  `Field-Record-Table/members/label-tables-scanned.tsv` +
  `label_table_scan.py`.
  `FABLE-REQ-SWE2-DATA-HANDBOOK-MONSTER-LIST-AND-COUNTER-MASK`
  **DONE** (rev ~19604), published `4468befe`. Read
  `us/menuhandbook.bin` (kind 7, id `0xC8`) via the UQ-274 hop
  chain. Hop 3 `+0xDC`: count 11 — eleven u16 bestiary ids
  (`0xF8,FB,FD,F0,FA,E6,104,121,10F,111,103`); mode-7 descriptors
  index 0–9 so entry 10 (`0x0103`) ships unread; names pending the
  `hctg` id→page decode. Hop 4 `+0xF8`: mask `0x800661FF`, 14
  overrides by rank (FIGHT 300, MAGIC 200, TECH 100, STEAL 50,
  KILL 500, STEP 50000, GET_GIL 100000, USE_GIL 1000000,
  LEVEL_AVG 50, YUGOU popcount 8, SELL_EVITEM 1000, SCORE 500000,
  CHAIN 50, id31 16). AB-1 test: mask covers every mode-0 counter
  id **except 11** (license counter → fallback 0 → signed ≥0 on
  save `+0x384C+0x10`); extras 5/8/18 kind-0 computed, 13 mode-3,
  31 dead. Artifacts: `menuhandbook-achievement-records.tsv` +
  `read_menuhandbook_hops.py`.
  Prior completed:
  `OPUS-REQ-DATA-PASS22-EFFECT-MESH-KIND54-UNACCOUNTED-NEIGHBOUR`
  **DONE** (rev 16308), published `a9f60432`; `@publication` released
  rev 16309. `00229E40` is the 7-byte cached-language-id getter
  (`return [01E02814]`); both vertex-prep callers gate `1 ≤ id ≤ 6`
  (Latin range) before writing alternate vertex-attribute constants —
  the page now carries the CoreRuntimeScheduling CLIENT paragraph and
  contributes zero unaccounted neighbours. **Flagged to OPUS in the
  finish note:** the full audit reports one remaining neighbour on
  `04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md`
  (Rewards edges from `00265020`) — SWE2-STRUCT in-flight debt, not this
  page's.
  Prior completed:
  `FABLE-REQ-SWE2-DATA-EFFECT-TYPE-TABLES` +
  `FABLE-REQ-SWE2-DATA-EFFECT-TABLES-ADDENDUM` **DONE** (rev 15255 /
  15256), published `f353c915`; `@publication` released rev 15258;
  review `DATA-REQ-AUDIT-SEM-TYPE-TABLES-REVIEW` READY → SWE2-AUDIT-SEM
  (rev 15264). Result: the authored element type byte is the `0xA00`
  chunk record-header byte at `+0xE` — 53 distinct values over 31,635
  chunks in 3,288 files; `0x800` chunks are a separate sub-record
  class whose `+0xE` subtype stays in 0–8 (32,639 chunks). All 53
  authored types reach a dedicated arm — 42 in the four main
  dispatchers plus 11 in all four `0x42`–`0xAB` sub-dispatchers; none
  hits a true default. Element `+0` is installed by `002F2D60` copying
  `def+0x44` → `element+0` at `002F30F2`. The `00441970` kind switch is
  degenerate: kinds `0x40/0x41/0xA1/0xA2/0xA5/0xD0` walk element
  chains, the other 139 of 145 return when the action-context bit is
  clear. Deliverables: dispatch page §2.8 + §7 rows,
  `members/effect-type-authored-usage.tsv` +
  `members/effect-kind-441970.tsv` + both generators; UQ-205 ANSWERED,
  UQ-204 PARTIAL; BI-3a/BI-3d checkboxes ticked on the unclassified
  page.
  Notices discharged this session: `DATA-NOTICE-FABLE-SWEPT-EFFECT-MESH-WORK`
  (acknowledged; content intact, no rewrite) and
  `FABLE-NOTICE-DATA-FRAMELIMIT-MODE-FILTER` (settings page §12/§13
  amended, published `6a4b3b8e`).
  Prior completed:
  `FABLE-REQ-SWE2-DATA-EFFECT-MESH-0X54` **DONE** (rev 15229),
  published `b85ffb4c` + `fe97ca5d`. **Note:** `b85ffb4c` is FABLE's
  pdata-orphans commit — my five census paths were swept in from the
  repo index during their publish (content verified identical to
  intent; notice `SWE2-DATA-NOTICE-FABLE-B85FFB4C-CARRIES-MESH54-CENSUS`
  filed); `fe97ca5d` carries the container-doc corpus note. Review
  `DATA-REQ-AUDIT-SEM-MESH54-REVIEW` READY → SWE2-AUDIT-SEM; results
  posted to FABLE as `SWE2-DATA-REQ-FABLE-SEC22-5-BOXES`.
  Result: census over all 3,698 shipped `.efx`/`.efb` (extracted to
  `Tools/work/DATA/mesh54/fx_all`) — 2,252 kind-`0x54` records in
  1,087 files, **size control 2,252/2,252 exact** (16-byte-aligned
  strides); flags all `0x07`, `key` all `0`; `c1A == c18` universally,
  `c16 != c14` in 1,670; **`c1E` = 0 in every record — BI-3d answered
  vacuously** (the 16-slot inline window is never touched). Arrays
  (BI-3a, distributional labels): `+0x24` all 52,808 unit-length w=0
  (normals hyp.), `+0x28` packed RGBA-like (`0x80808080` = 47%),
  `+0x2C` float pairs 74% in [0,1] (UV hyp.). Element type `0x05` =
  `0xA00`-chunk element definitions only (`0x800` chunks are a separate
  320-slot sub-record class, subtype ≤8): 5,164 elements in 1,088
  files, slots filled max 3 of 32, **every nonzero id resolves to a
  same-file kind-`0x54` sub (5,163/5,163)**; `+0x1C` ids → kind-`0x52`
  subs likewise (439/439). Deliverables:
  `17-Presentation-Rendering/Effect-File-Formats/
  effect-mesh-records-kind-54.md` + `members/effect-mesh-54-*.tsv` +
  `members/census_mesh54.py`; BI-3a/BI-3d rows ANSWERED in
  OPEN-QUESTIONS.
  Prior completed:
  `DATA-REQ-FABLE-DRAWMASK-VERB-CENSUS` **DONE** (rev ~15147),
  published `fe203d98`; review `DATA-REQ-AUDIT-SEM-DRAWMASK-REVIEW`
  READY → SWE2-AUDIT-SEM. Result: **zero call sites** for
  `20A0`/`20A1`/`20A2` in all 10,045 shipped `.ebp` (237,734 scripts,
  0 decode faults) — bits 2/3/4 of `022C7F90` set only by native
  bulk-configure; scanner + controls at `Tools/work/DATA/drawmask/`.
  `OPUS-REQ-SWE2-DATA-RESOURCE-TABLE-ROWSTRIDE-CENSUS` **DONE** (rev 15081),
  published `0f77630c`; review `DATA-REQ-AUDIT-SEM-ROWSTRIDE-REVIEW` READY →
  SWE2-AUDIT-SEM. RS-1 answered: `rowStride`(+0x48) is a `.text` immediate,
  not authored data — sole geometry writer `0051F9F0` has exactly 3 `E8`
  call sites in render-root ctor `0041E3A0`: `00409F38`→`0x50`,
  `0046E285`→`0xC0`, `00477F0A`→`0x260`; `bankShift`=5 everywhere, so
  `rowMask`(+0x50) is derived `(1<<5)-1 = 0x1F`, never an input. Verdict:
  several strides → `ResourceEntry` is not one fixed-size type. Verifier
  `Tools/work/DATA/rs1/census_rowstride.py` + `rowstride-census.tsv`.
  Prior completed:
  `OPUS-REQ-SWE2-DATA-SIX-UNNAMED-BIN-FAMILIES` **DONE** (rev 15008),
  published `71546dd3`; review `DATA-REQ-AUDIT-SEM-SIXFAM-REVIEW` READY →
  SWE2-AUDIT-SEM. All six families explained or dispositioned:
  `QST1` = `{magic, u32 173, u32[173]}` `{u13 const 0x2CE, u13 subidx
  → text 0xA000+n, bit26 flag}`, kind 9/0x21 → `02CA6C60`, consumers
  `00473B90`/`00473C90`; `EVME` = `{EVME, MLST, u16 8, u16[8]}` =
  `{0,0x31,0x29C,0x29E,0x30E,0x367,0x368,0x390}`, kind 9/0x29, cb `00378A50`
  → `02ADD0A8`, scanned by `00377440` (DS-1 resolved);
  `hcom` = kind 7/0xC8 via `003158B0` → `022C2550`, u16 self-relative-offset
  web + locale-variable u32 constants tail; `hodr` = kind 7/0xC9 via
  `00572D80`→`00249210`, 33×32B records = display-order permutation of page
  kinds 0–0x20 + signed dx/dy + paired-link field; `//22` = not a magic —
  `face_guest15`'s doubled first texels (kind 7/0x1F); `dP<d` = kind 9/0x2A
  via `003B53C0`, summon-effect module (`02B40508`+ state, `0xE0`-stride ×
  `0xA0` instance pool at `02B40528`) — container-level disposition, payload
  field structure unresolved.
  Validator: `Tools/work/DATA/sixfam/decode_sixfam.py` (38/38, 0 failures).
  Prior completed:
  `OPUS-REQ-SWE2-DATA-HIMG-TURNS-CHECK-ASSETS-RED` (P1) **DONE**, published
  `4568ea75`: `check_assets.py` resolves a declared token that names no
  extension against `format-magic-census.tsv` (new `magic_scoped` class —
  resolved, reported, not counted, not stray). Gate green at HEAD; `.dat`
  stays `bucket`, `himg` is signature-scoped inside it.
  `OPUS-REQ-SWE2-DATA-BIN-MENU-IMAGES`
  **DONE**, published `354c3089`; review `DATA-REQ-AUDIT-SEM-BINMENU-REVIEW`
  READY → SWE2-AUDIT-SEM.
  `OPUS-REQ-SWE2-DATA-HIMG-LAYOUT` **DONE** (rev 14724), published `98ad9786`;
  review `DATA-REQ-AUDIT-SEM-HIMG-REVIEW` READY → SWE2-AUDIT-SEM.
  `DATA-PUB-BUCKET-DISPOSITION` **DONE** (rev 14746, `79510a96`).
  `FABLE-REQ-SWE2-DATA-MENUMAP-SIBLINGS` + `-ADDENDUM` **DONE** (rev 14630/14631);
  review `DATA-REQ-AUDIT-SPEC-MENUMAP-REVIEW` READY → SWE2-AUDIT-SPEC.
- **Key findings (bin_menu images):** the eighteen "byte-doubled" `.bin` units are
  **raw single-channel 8-bit pixel buffers — no magic, no header, no CLUT** (size =
  stride × rows). `face_guest07`–`16` (kind-7 ids `0x17`–`0x20`): 12,288 B stored
  128×96 with **every 2×2 block uniform** → logical **64×48** under a 2× nearest-
  neighbour upscale — the census's "doubling" resolved as upscale, not channel
  duplication (vertical row-pair equality is the discriminator; both axes double).
  `map_efe00`–`06` (ids `0x0E`–`0x14`): 16,384 B = 128×128, **not** doubled — two
  stacked 128×64 field-effect icon cells (HP↓/MP↓, crossed-out item/action icons,
  magnet); only the text-bearing `efe00`/`01` localize (de/es/fr). `mini_guest_face`
  (id `0x0D`): 73,728 B = six 128×96 pages, each a 2×2 grid of 64×48 mini portraits
  (24 distinct cells — not "six faces"). All 162 files (18 × 9 locales) validate
  with 0 failures. **Palette ownership remains open** — no in-file CLUT, the
  per-kind descriptor table `0x050E53C0` is runtime-populated; adjacent
  `item_clut`/`monotone_chr`/`fontcolor` belong to item/font assets.
  Decoder/validator: `Tools/work/DATA/binimg/decode_binimg.py` (reads VBF directly).
- **Current package:** none — SN-1 `.dbg` deepening **PUBLISHED
  `aa26bf717`**: q0 streams = `{u16 pos; u8 0; u8 flag∈{0,1}}` (pos
  monotonic per scope, line/PC coordinate; flag=1 = item start),
  quartet roles (pos stream / heap-position name table / q0-range
  offsets / `0xFFFFFFFF`-headed index list), heap suffix-compression
  confirmed, T1 = byte-granular position-ordered index (semantics
  open), front stream < per-line granularity (94/1693 on line starts).
  Earlier: `.sbn` paged line map **PUBLISHED `7e5ed701f`**.
  The reported "second u16 array" does
  not exist — the whole `u16` span is 32-line pages
  `{u16 lineOff[32]; u16 chunkEnd; u16 0}` + bare last page,
  `(pages−1)·34+32` u16s exact on all 9 blocks; chunks tile
  `[textOff..blockEnd)`. `.dbg` mapped end-to-end (5-slot header,
  17-entry `dirA` of packed `{count;u32[]}` tables, front
  `{u16 srcTextOff;u16 flags}` stream, S0 scope quartets 7/13/23/7,
  S2 index, class-ordered heap); `.msb` `(flag<<16)|offset` directory +
  `0F <subtype> 81 <val>` tagged streams. `.msb` token grammar **PUBLISHED
  `c4c15618b`**: `0F <cmd> <args>` escapes are variable-length
  by cmd — 2 arg bytes (both `≥0x80`) for `cmd<0x40`, 1 arg byte for
  `cmd≥0x40`, zero violations on all 194 messages; `0F 24 81 81`
  opens every payload; `12 <b≥0x80>` is the dominant 2-byte body
  token; `0E <b>` is a 1-arg tag; `10 C8 xx` = argument-index
  counter. Flag correlate **PUBLISHED `b21aa82e5`**: `10 C8` occurs
  only in `flag=1` messages — one-directional, marks a
  menu/selectable class; `btlctrl`/`mapctrl` run contiguous
  `flag=0` tails = likely second bank. **`.msb` flag RESOLVED
  (published `cd21fb990`):** `flag=1` = the authored **menu-class
  bit** — `aask`-family bodies (`aask` 0x10, `aaske` 0x14A,
  `aask_1ff` 0x1FF; msg pushed as int-pool `0x010000NN`, pool is an
  identity map). Constant-bound set == flag-1 set EXACTLY in
  btlctrl 22/22, ctrl 35/35, mapctrl 29/29; evctrl 35/36 — msg0
  (1,503-byte menu) is never pushed at any aask site (no const/
  literal/PUSHV) — invoked via a non-static path. Flag is authored
  binding metadata, not a content predicate — the `10 C8`/`02 0E`
  correlates follow from menu bodies carrying item markup.
  **Heap-anchoring refined
  PUBLISHED `da49385a1`, SUPERSEDED below):** T3/T4/T8/q1 entries
  were measured as landing anywhere in a name's span — wrong-base
  artifact; under the correct base all are name starts.
  **Front-stream flag classes PUBLISHED `da49385a1`:** partition by
  coordinate space — `flag=1` only in the two 3-block modules
  (`mapctrl_mj.src` mark); `0x2000`/`0x5800` position lists
  byte-identical across all four files (shared-content marks
  resolving inside `global_flag[186]`/`[187]`); `0x3000` confined
  to the shared includes/decls band and is a per-run u16 counter
  over flag-0 marks (`pos = 2×(ordinal − 62)`); per-class bases
  unproven. **Scope-stream coordinate resolved PUBLISHED `e7ba3501a`:**
  q0 `pos` = **0-based source line number** — flag=1 marks land on
  statement lines (`0x49`=`main`, `0x4E`=`if( debug_padd() )`);
  scope ranges tile block-0 text sequentially per top-level entity
  (evctrl `0x21..0x4C`→`0x198..0x4BF`→`0x4C5..0x505`→…, mapctrl
  likewise; ctrl overlaps = nesting). Items are fixed-arity {1,3}
  same-`pos` records — size-1 structural lines, size-3 statements.
  **Front-stream bases narrowed PUBLISHED `47b0b40fe`:** `flag=0` =
  block-0-text-relative in all four modules (text lens
  `0x5220`/`0xC630`/`0x105A0`/`0x1A794`); `flag=1` = perfect
  stride-24 enumeration `pos=0x2+24k` (k=0..2073/0..2086) —
  synthetic slot index, "second-source mark" reading withdrawn.
  **Quartet q2 resolved PUBLISHED `757f5962b`:** q2[j] = q0 record
  index of item #32j — stride-32 item checkpoint, exact on all
  50 scopes corpus-wide (scope3 36 = ceil(1134/32)). q3 still
  open (0xFFFFFFFF-headed item indices, ~11-12 stride, prefix-
  only coverage; not line/item/record checkpoints in any reading).
  **Front stream RESOLVED as name-index directory PUBLISHED
  `62aa56668`** (supersedes `99711fc65`'s tagged-value framing,
  retracts `a8c4f705d` outright). The stream's true end is the first
  `dirA` table; earlier reads past it produced phantom classes
  and `0xFFFF` "sentinels" (q3's `0xFFFFFFFF` headers —
  coincidence). On the correct range it is strict `u32` pairs
  `{nameHeapPos; index}` (5000/5020/846/1004 pairs): element 0
  = heap position from `global_flag[0]` landing inside names;
  element 1 = 12-bit symbol index (0..4095 — the heap's
  `global_debug_flag[0..4095]` block is exactly 4096 entries)
  or a tagged index (`0x3000`+2 counter, `0x2000`/`0x5800`/
  `0x1000`/`0x4000` classes). Pairs run in heap order —
  positions stride by name length (the "stride-24 lattice" was
  24-byte flag names) while indices count +1 through the table;
  `btlctrl` index N ↔ `global_debug_flag[N+34]` (slots
  0..4061 = flags 34..4095, 4062..4095 = module names). Head
  section (pairs 0..~902) walks a sparser 0..0xCED index space;
  ctrl/evctrl have only that. So: `symbolIndex → heapPos`
  directory over a 4096-slot table. Addendum 9 in AUDIT-LOG
  rewritten as the correction+resolution record; stays parked
  behind AUDIT-SPEC's shadow batch.
  **Header/section/T1 refinement (unpublished):** the "dirA" is
  the 16 `u32` section offsets at header `+0x2C..+0x68` tiling
  `[sec0 .. 0xB7E0)`; sec0 = T1 = `{count; u32 offs[count]}`
  (1389–1436) of byte-granular file offsets spanning the tail
  slice `[lastScopeQtail, S0, S2, S1, heapPrefix]` — arranged as
  **exactly 67 ascending sub-lists in ALL FOUR modules** → a
  shared 67-entry structure (not per-scope: 23 vs 13 scopes).
  Heap is ~150 KiB to EOF (`btlctrl` `0x1CD7D..~0x41F4F`) and
  additionally holds `global_debug_flag[0..4095]`, module
  globals, and compiler-generated `@IFTERM_NNNNNN`/`@IFELSE_NNNNNN`
  block labels. q0 refined: within a line's pos-group records
  partition into arity-{1,3} sub-records each headed by
  `flag=1` (the {1,3} arity is at sub-record level; lines hold
  1..N sub-records). q3 narrowed: entries = q0 record indices
  inside multi-record items only (skips single-record `}`
  items), ~11–12-record stride, prefix-only — still open.
  **Deepened further (unpublished):** T1's 67 sub-lists have
  byte-identical lengths for lists 0..65 across ALL FOUR modules
  (only list66 diverges) → shared 66-entity structure + module
  tail. ~~q1 revealed global_debug_flag[N] is partitioned per
  scope~~ — RETRACTED (wrong-heap-base artifact; under the true
  base q1 = @-labels + function names only, no gdbg). Heap holds
  the module's complete
  compiler-generated control-flow label set — `@IFELSE_N`/
  `@IFTERM_N` pairs, `@WHJDE`/`@WHTRS`/`@WHTRM` triples,
  `@SWJDE`/`@SWSFX`/`@SWCOD`/`@SWTRM` quads + `@CASE_N` +
  `@DFLT_N`, `@FORJGE`/`@FORSFX`/`@FORCOD`/`@FORTRM` quads —
  numbered by a global construct counter in compile order;
  CORRECTION: q1 DOES list them (per-scope symbol sets); the
  front pair directory still does not.
  **q0 FULLY RESOLVED (unpublished, verified):** q0 = a
  byte-granular bytecode→source map — scope i = `.ebp`
  script-directory entry i (23=23 btlctrl, 7/13/7 others), and
  record i of a scope's q0 = byte i of that script's code:
  `{u16 lineNo; u8 blockIndex; u8 flag}` where flag=1 marks the
  instruction's first byte. Decoding bytecode with the opcode
  length table (0x03-0x47→1B, 0x48-0x63→3B) reproduces flag=1
  positions EXACTLY in all scopes of all four modules; flag=1
  count == `numOfInstructions`; recs == bytecode bytes + 0-2
  end marks (line0/blk0/flag0). The "arity-{1,3} sub-records"
  were the instructions' own byte lengths. Edge: evctrl sc1
  stream runs 144B past its script's directory bound (48 extra
  instr marks on one `case` line — shared/dedup code tail).
  **q1 CORRECTION:** q1 DOES list `@`-labels — each scope's q1 =
  its complete symbol set (@-labels + named vars); earlier "no
  refs" used the wrong population. **q2 = stride-32 INSTRUCTION
  checkpoint** (q2[j] = byte offset of instr #32j; verified).
  **q3 = bytecode byte offsets** into the scope's script
  (instr-start + operand bytes; PUSHV/POPV/call-family recur);
  referent still open.
  **Front stream + header slots deepened (unpublished):** the
  front stream is **ONE directory sorted by heap position**
  (4987/4999 adjacent steps ascending) covering essentially
  every heap name in order — `global_flag[]`, `battle/quest/
  event_global_flag[]`, `g_*` module globals, then
  `global_debug_flag[0..4095]`, then module verbs. In the
  `gdbg` region the id field is a flat 0..0xFFF ordinal and
  positions step by exactly the flag name's byte length
  (24/23/22/21 for 4/3/2/1-digit N) — one entry per flag;
  in the pre-`gdbg` region ids carry class-like tag bytes
  (`0x30|N` counting +2 = the shared include's vars — identical
  shape in all four modules; `0x20`/`0x10`/`0x40`/`0x58` rarer).
  The tag byte mirrors the descriptor's `class|float|width`
  field but only 5/92 `.ebp` descriptors match verbatim — exact
  id semantics open (per-class index/offset?). Header slots:
  **S1 = the string-heap start** — heap opens with the `.sbn`
  block source paths (`btlctrl.src`, `c:/plan_work/jp/event/
  header/systemctrl.ath`, `mapctrl_mj.src`; `ctrl` uses a cygwin
  path) = the names q0's `blockIndex` selects. **S2 = a 64-slot
  directory** of `{count; tag; positions[]}` tables — only slot 1
  non-empty: the **module-global symbol list** (tag 1 + 48/42/47/57
  raw file offsets into `global_debug_flag[734+]`, past the
  per-scope q1 partition that ends ~733). S0's field correlates
  with `.sbn` block count (0x7C for 3-block, 0x78 for 2-block).
  **Front-stream id RESOLVED to descriptor layout (unpublished):**
  id = `{byteOffset:24; tag:8}` where tag has the descriptor's
  `class|float|width` format — every observed tag is class-0
  (GLOBAL): `0x10`=width-1 u8, `0x20`/`0x30`=width-2/3, `0x40`=
  width-4 u32, `0x58`=float; low field strides by element size
  (+1/+2/+4 per tag). All five class-0 `.ebp` descriptor values
  appear verbatim as front ids (`0x30000000`, `0xA71`, `0xC7A`,
  `0x10000914`, `0x10000915`) — so the front stream = the module's
  **global-variable directory** (descriptor→name, the .dbg side
  of the save-payload map); ~416 ids bind two names (aliases).
  The `gdbg` region's flat 0..0xFFF = width-0 globals at offsets
  0..4095 = the u8[4096] debug-flag array.
  **FIELD-ORDER CORRECTION (unpublished, verified):** the pair is
  `{id; nameHeapPos}` — the SECOND element is the position, not the
  first. Under the corrected order `pos` lands on name STARTS
  4,999/4,999 (the "varying interior depth" was the id element
  decoded as a position) and the gdbg pass is EXACT: pairs 903..4998
  = `{N; pos}` ↔ `global_debug_flag[N]` at name start, 4,096/4,096 —
  the `N+34` skew and "tail slots = module verbs" readings are
  retracted (verbs are indexed by T1, not the stream tail).
  **q3 re-corrected to a TWO-LIST stream:** `{u32 countA; u32
  FFFFFFFF; u32 listA[countA]; u32 listB[]; zero pad}` — `head` IS
  a count after all (of listA only; verified on all 50 scopes in all
  4 modules: sentinel FF at +4, listB = remaining nonzero vals to the
  next table, ascending). Zeros inside listA are real entries —
  sc19 `{2;FF;0x0B;0;0}` = marks at bytes 11 AND 0 — which RESOLVES
  the sc18/sc19 anomaly: identical code + identical vals, differing
  only in countA (sc19 counts the byte-0 mark, sc18 treats it as
  pad). The prior "head is not the count / is scope-bound" reading
  is retracted. vals = ascending bytecode byte offsets over the
  scope's PREFIX (~12-30%), ~11-12B stride continuing uniformly
  across the A/B boundary (split is positional, not spatial),
  uniform across ins byte positions (not ins boundaries, operand
  ptrs, jump targets, or line starts — all tested). Identical code
  → identical vals (all four modules' scope0 = [A,16,21,2D]); marks
  exist with empty q1 (sc20) — not symbol bindings. The A/B boundary
  correlates with structure: sc0 splits exactly at the .ebp func-1
  offset 0x25; sc22 at the `switch(i0)` body (lines ≤2379 vs ≥2384);
  other scopes split mid-stream with no func/jump boundary in the
  gap — the two lists' semantic distinction is open. Referent still
  open (best guess: per-prefix emission-cursor checkpoints).
  **T1 RESOLVED (published `9d10d353d`):** T1 = the **ATEL
  verb-category directory** — dirA[0] `{u32 count; u32 pos[count]}`
  where every entry is a name-start heap position (1,389/1,389 in
  btlctrl land on NUL-boundary name starts; base = header `+0x08` =
  S1 = heap origin — the earlier `0x5170` was wrong). 67 reset-
  delimited ascending buckets decode to thematic verb families —
  b18 = `camerashake*`, b66 = `blur*`, b6 = `bganime*`/camera,
  b48 = `bgmstream*`, b24/30 = `anime*`/`lookat*`, b12 = `setmap*`/
  `resetmap*` — identical bucket→family map + byte-identical list
  lengths for buckets 0..65 across ALL FOUR modules; only b66's
  tail varies (37/58/84/55). 1,153 distinct verb names in btlctrl.
  The "file offsets into the tail slice" reading was a numeric
  coincidence with the pre-S0 record stream.
  **width-3/5 RESOLVED:** the front-stream tag byte is the native
  descriptor's `{width:4; float:1; class:3}` top byte verbatim;
  the width nibble is the resolver's six-case selector —
  width3 = s16 (tag 0x30: global_flag/g_com_*, stride 2) and
  width5|float-bit = f32 (tag 0x58: g_com_navi_footcalc[],
  mp_map_set_angle, stride 4). All six width cases now observed
  in-corpus: 0x00 u8 gdbg / 0x10 s8 mp_* / 0x20 u16 telepo /
  0x30 s16 / 0x40 s32 / 0x58 f32.
  **Mid-name landing claim RETRACTED (published `366254b81`):**
  under the correct heap base (header +0x08 = S1 origin) EVERY
  table position is a name start — T1/T3/T4/T8 + all q1 = 100%
  corpus-wide (q1 2778/2778). The "depth is writer-internal"
  convention was a wrong-base (0x5170) artifact.
  **q1 RESOLVED as the jump-table name overlay (unpublished):**
  q1 holds ONLY @-labels (2762) + named function/entry points
  (16: DEBUG_MENU, MENU_TOP, summon, BEHIND_CAMERA…) — no vars,
  no gdbg (the "gdbg partitioned per scope" claim = same wrong-
  base artifact, retracted). q1 is INDEX-PARALLEL to the `.ebp`
  script record's +0x14 table (the VM jump table): `jt[i]` = byte
  position where `q1[i]` binds — CASE_N→case bodies (ascending),
  WHJDE→loop head, WHTRM→one-past-end, IFELSE/IFTERM share an
  offset on no-else ifs — and `4f idx; 09` selects jt[idx]
  (targets verified on instruction starts). count==q1count on
  49/50 scopes; exception = evctrl sc1 (q1 160 vs jt 158 — the
  shared-code-tail scope). So the label→position binding lives
  in the `.ebp`, not the `.dbg` — q3 is NOT that table.
  **S2 slot-1 RESOLVED (2026-09-22):** `{count=msgCount; tag=1;
  u32 heapPos[count]}` = the module's `.msb` message-constant
  name table — pos[i] names message i's source constant
  (`select_*`/`mmes_*`/`mes_*`/`MES_*`) in `.msb` index order;
  48/42/47/57 == msgCount on all four modules. The "module-
  global symbol list into gdbg[734+]" reading = wrong-base
  artifact, retracted. **evctrl msg0 EXPLAINED:** `select_base`'s
  only call site is `aask(6, select_base,…)` inside
  `if(ISDEBUG())` — folds false in this build, the if-branch
  emitted zero code (no `4e 00`/`4f 00 00` push anywhere; only
  the else/production `select_base2` call emitted). msg0 is
  declared+named+pooled+flag-marked but dead-bound — flag=1 is
  authored menu-class, not a live call.
  **`.msb` 0F-selector vocabulary MAPPED (2026-09-22):** the
  `0F <cmd>` selectors are ASCII chars inside the TZA text
  interpreter `002AC5F0`'s `0x20..0x70` escape space — same
  language family. The arity split is exact: ALL 1-arg cmds
  (@ B E H I J K P Q) sit in its `@`-`k` inline-icon block;
  the 2-arg cmds are its parameter escapes ($=+0x4C scalar
  opening every msg, `(`=size/24ths, `)`=colour [the dominant
  per-span escape], `7`=size-percent = the 0F37 residual,
  %/'/&=justify L/C/R, .=arg-insert pairing the `10 C8`
  counter, -=number, /=render-state, >=actor-name). Semantics
  inferred from vocabulary — PS2 payload is 2 compact bytes vs
  TZA's 3-byte parsed payload; no .msb consumer ships (§3).
  **JP glyph table DERIVED (2026-09-22):** custom mixed-width
  table (NOT Shift-JIS), both kana planes = interleaved gojuon
  (small/normal/dakuten/handakuten adjacent): hiragana 0x3e-0x90
  (ぁ=3e…ん=90), katakana 0x91-0xe3 (ァ=91…ン=e3). 2-byte leads
  0x10-0x14+0x81: 10c5=ー, 112d=罫線, 8134-3d=digits 0-9, and the
  12-plane = fullwidth ASCII (A=1286..Z=129f, a=12a0..z=12b9,
  digits 12ba-c3, 12d0=_, 12d7=:, 12cf=/, 12db/12dc=brackets) —
  evctrl msg0 decodes as "Event Plan Menu" with the full debug
  item list, msg5 = "Test Event" listing EVT_T#### [designer]
  entries. Kanji live across 10/11/13/14 + 12c4+ (指=11c0,
  定=1096, 読=1345, 再=12dd). 0e = 4-arg line header
  (0e <type> 80 80 <80|81>). decode_msb.py ships next to the doc.
  Open: kanji-plane per-glyph map, e2+ singles, kana-tail e1/e2.
  Residuals (undecoded, not guessed): q3 referent (two-list
  {countA;FF;A;B} — A/B split is positional not spatial, still
  open) + `.msb` per-cmd payloads verified against a consumer +
  kanji glyph map + low-tag arities.
- **Exact next action:** inspect `team.py show --agent SWE2-DATA`
  for addressed notices / READY items; fallback = the `.dbg` q3/
  front-stream-space residuals or `behindcamera` sampler below.
  AUDIT-LOG addendum 9 (the correction record) stays parked —
  AUDIT-SPEC's shadow batch is ahead of it; it rides the next
  AUDIT-LOG publish.
  **`.bin` companion OPENED (2026-09-22):** fifth sibling = the
  compiled native-side module — tag 0x8000000b + filesize +
  metadata-string offsets; build stamp/author (katano, mtanaka,
  Unknown)/srcname at 0x90; section/reloc directory; tail =
  NUL-separated symbol names (init/main/callmenu/event_menu/
  mapjump_menu/boot_boss_btl_ctrl/map_dsp_*) + Shift-JIS runtime
  strings. behindcamera MAP_BEHIND_* tables likely live in its
  data sections. **`.bin`↔`.ebp` identity RESOLVED (2026-09-22):**
  `.bin` = EBP2 section-000 exported standalone — the standard
  0x8000000B script-image header (already documented in
  section-000-bytecode.md: +0x14 sumTable, +0x18 script dir,
  +0x20 int pool, +0x24 float table, +0x4c name pool). Embedded
  image == sibling .bin byte-for-byte on ctrl/btlctrl/mapctrl;
  evctrl embeds an older link (+0x80 larger, shifted offsets).
  Body = ATEL bytecode/data, NOT MIPS. New correlate: +0x20 pool
  msgrefs == msgCount 4/4 (42/48/47/57); mapctrl float table =
  {count=6; -1,-0.4,0,0.3,0.6,1} matching 6 MAP_BEHIND_* cases
  (plausible sampler params, unverified).
  Kanji census (2026-09-22): 134 distinct unmapped 2-byte codes
  corpus-wide; NEW verified: 12d2=fullwidth minus − (MAP_BEHIND_
  LOOKUP[−1.0]; doubled as −− title separator), 12d4=`,`,
  12d5=`.`, 12d8=`\`, 12cb=`%`, 12d3=2nd colon, 10c3=`、`,
  10c4=`。` (10c3-c7 = contiguous punctuation block), 137b=閉,
  139c/10cd=制御 (source-confirmed エントリー制御), 122f=元,
  1235=戻, 1088=其, 11f3=別, 1138=勧 (mapctrl msg31 decodes as a
  complete sentence). Candidates parked: 1068=死, 10fe=倒.
  **MAP_BEHIND_* params VERIFIED**: the +0x24 float table IS the
  sampler table — msg27 menu prints each constant's value in
  order (−1.0/−0.4/0/0.3/0.6/1.0 = the six floats).
- **Current claim:** `FRONTIER-REQ-DATA-CENSUS-RERUN-UNDER-CFG-WALKER`
  (P2, claimed 2026-09-23) — re-census the 36 'COUNTS HERE ARE
  UPPER BOUNDS' types in `_types/fields.tsv` under the fixed
  CFG walker (census_receiver_fixpoint.py / gen_array_census.py,
  ≥57f9d58ab); amend each caveat with rerun revision; confirm or
  withdraw pre-fix negatives. SN-1 parked at residual level
  (all five companion formats structurally resolved; remaining
  = icon planes/font texture, ~15 kanji candidates, `0F`
  semantics vs absent consumer, q3 referent).
- **Rerun COMPLETE 2026-09-23:** all 33 caveated types / 384 rows
  re-censused under `57f9d58ab` (the requester counted 36; the
  caveat set is 33 — `ImageBackedStateBlock +0x3849` was removed
  by a peer mid-run and is amended on the HEAD base only).
  Every row got a `CFG-WALKER RERUN 2026-09-23` clause:
  CONFIRMED-NEG 199, WITHDRAWN-NEG 106, POS-HELD 37, POS-LOST 7,
  MISATTR 35 (LuaProto/LuaTable/LuaUpVal — ctor seed tracks the
  parent lua_State; call seed is sound but caller-side only, so
  those negatives stand pending a receiver-owning seed). LuaState
  ctor hits are genuine (parent L IS the type). Site-level audits:
  low-count hits verified at instruction level (genuine receiver-
  relative accesses, handler bodies + init batteries the linear
  walk lost at branches/jump-table arms); the 7 POS-LOST rows'
  recorded sites all drop out of the union once call clobbers are
  modelled — phantom positives through dead volatiles. Unioned by
  (disp,width,site), no double-counting. Drivers:
  `Tools/work/SWE2-DATA/census-rerun/{run_rerun,evaluate,amend_fields}.py`,
  per-seed JSONs + `dispositions.tsv` in `census-rerun/out|dir`.
  Self-falsification: what would falsify = hits that are all
  generic-callee over-attribution (checked at instruction level),
  seeds that never started (per-seed fn counts recorded in each
  clause; PendingCompletionQueue cell seed found 0 fns — union
  still covered via call+ctor), retracted positives that actually
  survive (audited all 7 site lists — none survive).
  **Peer-work isolation:** fields.tsv carried uncommitted OPUS edits
  (IndexedExternalSourceRequest +10, EncodedIdQueryRecord +12/29 edited,
  EfxCallerTemplate/WidgetSingleton02AEE4C0/ItemClassDescriptor/etc.)
  — the published file is HEAD + my 384 amendments only; peer work
  stays uncommitted in the working tree. T2 package (bulk
  negative-claim amendment): routed to SWE2-AUDIT-SEM, then
  FABLE/OPUS adjudication.
- **Publish blocked 2026-09-23:** `@publication` held by FABLE
  (`FABLE-PUB-001E2AF0-FINISHED`, ACTIVE since 09-22T20:48Z,
  ~15h stale per FRONTIER rev-29237 note — lease stands, no
  takeover on timestamp; OPUS lease-timeout rule request is
  pending). Queued: `_op_data_census_pub_task` +
  `_op_data_census_pub_claim` + `_op_data_census_audit`
  (DATA-REQ-AUDITSEM-CENSUS-RERUN, depends on the pub task).
  Amendable file staged at `census-rerun/fields_head_amended.tsv`
  (HEAD + 384 clauses only — peer's uncommitted fields.tsv work
  stays in the working tree; swap in at publish, restore after).
  `fields_work_with_peer_and_mine.tsv` = the restore copy.
- **While blocked, SN-1 kanji round-6 landed in the doc**
  (uncommitted): `12d1`=＋, `12dd/12de`=【】, `1267`=現, `10be`=用,
  `14c1/10bc`=完了, `146c/10d1`=位置, `1128/105e`=変更,
  `1061/10d7/1159`=全消&全立, `10cc/10ec`=発/連. Residue: 78
  distinct unmapped, but 87% of occurrences are the `10`-plane
  icon block (`10 20`–`10 3f` + `10c8` — map-jump item prefixes
  are icon columns, not a code table); ~47 real text codes left.
- **Round-7 + `0F` interpreter verification (2026-09-23,
  uncommitted — waiting on `@publication`):** source-verified
  `103d`/`109c`=移動 (btlctrl.sbn `//マップINDEX移動`),
  `1083`/`108f`=切替 (source has both orders verbatim). And the
  TZA interpreter `002AC5F0` was read to arm level: `0F` dispatches
  on selector `0x20..0x70` via a 2-level class table (35 arms);
  `@`–`k` share the icon arm `002AE1F1`, `%&'` share the alignment
  arm `002AD289` (selector stored at state+0x9A), `(`/space are
  scale arms, `0`/`_`/out-of-range no-op; shared arg reader
  `003FFAB0` = packed 9-bit value `(a1&C0)<<1|a2&7F`, `a1&7==0` →
  table index via `0039BA00` (5-byte metric records, ≤511 entries).
  `.msb` `81`-biased args = the same encoding — arg VALUES are now
  consumer-verified; per-selector semantics still vocabulary-mapped.
  Also landed same window: per-selector arity table (each arm has a
  dedicated reader returning consumed-length; `!` is ZERO-arg font-apply;
  `1`=3 args; `:`=4; `*`/`)` variable-length string payload via
  `003FFD70`) and the EVENT-CORPUS extension — 346 `plan_master/ch/event`
  `.ebp`s carry the same tagged `{u16 off;u16 flag}` message bank, and
  event text runs on leads `0x10`–`0x1F` (flat 4K-slot 16-bit glyph
  space; `1c`/`1f`/`13` planes densest). Real scrambled text, not charts.
- **GLYPH TABLE SOLVED — primary plane (2026-09-23, uncommitted —
  waiting on `@publication`):** `idx = LEADBASE[mode][lead&0xF] +
  (sub−0x20)` (`002AC2F0`); tables lifted from EXE (`00916570` mode0 /
  `009165B0` mode1); mode+threshold per language at `002AB7D0`
  (`[01E02814]`∈{7..0xA} → 0x1C+mode1, else 0x18; shipped default `0xA`).
  Index resolves in `<loc>/font00.dat` RECORD ORDER (36B
  `{utf8cp;metrics;hash}` records, font id in header) — verified against
  real sentences in jp (in plan_map: `あなたも政民でいらっしゃるの？`),
  ch (`往中層昇降梯`), us (`code−0x3A+'A'` = "OUTLANDISH"/"THE"/"LOOK").
  Debug modules are JP-authored in JP glyph space regardless of file
  locale — `ch`/`in` btlctrl.msb identical under `jp/font00`.
  `decode_msb.py --font <loc>` implements it; glyph lists staged at
  `Tools/work/SWE2-DATA/font-decode/<loc>_font*.glyphs.txt`.
  **Residuals:** secondary font (`state+0xA6`, set outside interpreter;
  order = PS2 fontpack ordering, no shipped Unicode table reproduces it —
  `18 2B`→院 anchors fail all `.dat`/`.fex` orders at base 0/0x7e0;
  `fontex_expand` is the leading candidate via one verified hit
  `18 37`→`客`); **RETRACTED 2026-09-23:** `0x81` is a single
  glyph (font00[0x61]=`や`), never a lead — bytes ≥0x20 are all
  singles `font1[c-0x20]` (`002AC376`); the "e4+ icon plane" is the
  fullwidth-letter region and `ff ff` "indent pads" were `0F 29` packed
  args. Mode-0 secondary IS proven (`us` `1c`-codes →
  `us/fontex_subtitle` at base 0x460 — `alc_a0100` = opening cutscene
  verbatim); `ch`/`cn`/`kr` `1c`-codes → their
  `fontex_subtitle` at mode1 base 0 (alc_a0100 same opening line all
  three locales). `in` residual = font1's extension (`18`-plane,
  15.7k occ, idx ≥0x7E0 past font00's 0x526 — fontpack order;
  no shipped order hits the anchors). `0F 29` arity pinned: `1+(a1&7)` packed bytes via reader
  `003FFBC0` (a1 = base«3|count); `0F 2A` = 2 args + `a2&0x7F`
  literal string (`003FFD6B`). Runtime font table `02AEE810` is in
  unloaded `.data`. `fontlist.ah` = runtime slot order
  (expand,subtitle,font00,bookman,iwa,venus,square,guide,tut,quest,
  monster,stf_a..cs); `.dat` ids: font00=1, expand=2, subtitle=3.
- **Exact next action:** resume blocks + board scan; the
  census-rerun package published 2026-09-25 as `dc4414b98`
  (fields.tsv 384 amendments + .fex solve docs + section-006 +
  companions + decode_msb.py + resume + TEAM.json).
  `SWE2-DATA-PUB-CENSUS-RERUN` and
  `FRONTIER-REQ-DATA-CENSUS-RERUN-UNDER-CFG-WALKER` both finished;
  `@publication` released. Remaining uncommitted: OPEN-QUESTIONS
  BZ-1/SN-1 row edits (the file carries peers' uncommitted rows —
  rides the next publish), post-commit TEAM.json DONE states,
  this resume update. Notices handled 2026-09-25:
  FABLE-NOTICE-…BZ-1-ROW-FIVE-CELLS — row repaired to 4 cells
  (still uncommitted with the file's peer rows);
  OPUS-NOTICE-…WORKTREE-TYPES-REVERTS — answered: dc4414b98's
  fields.tsv diff is exactly the 384 amendment pairs, zero reverts;
  the 23-route/4-cell revert set lives only in the uncommitted
  worktree overlay (restored untouched; owner unknown, NOT me).
  Next package candidates: q3 referent
  (structural skeleton done, semantics open), slot-6 glyph advance
  metrics, palette/renderer consumer chain for section-006,
  `.fex` +0xA8 map runtime reader (find helper 001FC640 has only
  write-path callers; read side inlined or routed differently —
  the event key is h33 of the .ebp DIRECTORY path).
- **Fallback round 2026-09-23b (uncommitted):** `.msb` flag
  corpus extension — 833 `ch` `.ebp` banks / 17,522 entries,
  only flags 0/1; flag-0 bodies NEVER carry `0x0E` (0/13,705),
  flag-1 = interactive class (3,774/3,817 menu bodies, 43
  parameterized input prompts). `.dbg` q3 further narrowed —
  not line starts/ends, not instruction indices, not jt
  positions; irregular ~4-5-instr deltas, consistent with
  per-statement emission checkpoints; referent still
  unresolved. OPEN-QUESTIONS SN-1 row rewritten current
  (residue: q3 A/B split + `in` `18`-plane fontpack order).
- **Fallback round 2026-09-24 (uncommitted — `@publication` still
  held by FABLE's stale lease):** `in` fontpack falsification —
  `in/fontpack_it.bin` dir2/dir4 are u16 glyph→offset LUTs (fill
  `0x00BC`), dir5 `4408`-tagged records, no code→char table;
  `fontpack_fs.bin` is Unicode→texel keyed; `18`-plane order is
  neither JIS/SJIS nor Unicode sort — bounded residual stands.
  **MA-1 ANSWERED** (`.adm` add-motion tables, doc §10 +
  OPEN-QUESTIONS row): record = `{i32 bone; f32 eulerDeg[3];
  f32 offset[3]}` — first triple degrees, lerped between
  bracketing groups, ×π/180 → `BuildEulerRotation`; second
  triple = metre offsets, authored but never read (dead to TZA).
  Group header = keyframe: track `field01` picks the driven
  float lane, `field02` = channel id → `004776D0`, `field00` =
  mode (0=interp / 1=id-match on group `+0x18`, the 35 track-0
  tracks). Index tables key on group 0 (parallel keyframes).
  Bone max 84, all ≥0, unbounded write never triggered.
- **Fallback round 2026-09-24b (uncommitted):** **`.fex` format +
  event binding SOLVED — the last `in`-locale glyph residual closed.**
  `18`–`1B` `.msb` codes are per-event-file glyph slots, not a font
  order: `fontex_subtitle.fex`/`fontex_expand.fex` are chained
  `{key; count; u32 cps[count]}` directories; `cps` = the event's
  expansion codepoints in first-use order (slot i ↔ code
  `(lead−0x18)*0xE0 + sub−0x20`); **`key` = engine path hash
  `00674A00` of `event\<dir>\<name>`** (seed 0x1505, h=h*0x21+movsx(c),
  btr 0x1F) — reproduced for 9 events, sibling scenes differ by +1.
  `us` serialization = `{key; idx; cp}` triples (same keys — alc key
  `0x22949AE0` heads `us/fontex_subtitle.fex` mapping to "The
  complices of the Senate"). `us` mode0 → global fontex_subtitle.dat;
  `ch`/`cn` font00 (~2,360 recs) covers 0x7E0+ directly; `jp`/`in`
  (font00=1,319) route every `18`-code to the event chunk.
  **Corpus: all 180 `in` event banks bind by key (158 subtitle +
  22 expand), 0 misses, 0 short, 0 unresolved glyphs** — `in`
  coverage 83.1% → ~100%. `decode_msb.py` gained `fex_magic`,
  `load_fex_chunks`, `msb_codes`, `decode_bank`, `bind_fex`
  (score fallback for non-event banks), `--fex-chunk`. Docs:
  font-data-kerning-and-expansion.md KE-1 (first sub-question
  answered), the-ctrl-module-debug-companions.md residual rewrite,
  OPEN-QUESTIONS SN-1 (residue now q3-only).
- **Fallback round 2026-09-24c (uncommitted):** `.dbg` q3 narrowed to
  a structural skeleton — **mark count == floor(q0len/32) on ~all 50
  scopes** (all 7 `ctrl` exact; few others −1): q3 is a stride-32-byte
  budgeted checkpoint parallel to q2's stride-32-instruction index,
  and "prefix-only coverage" is just that budget (~q0len/32 marks ×
  ~11.6-byte spacing tiles ~36% of code). Marks land uniformly on
  opcode/imm-lo/imm-hi bytes; residues mod 32 march +12 (occasional
  −1) — a near-fixed ~11.6-byte cursor. New negatives: block
  transitions (0 hits), .sbn text offsets, variable first-writes,
  @JDE/loop-head jt targets, control-flow opcodes at the A/B split,
  exact stride-4 instruction indexing (sc0 fits 3,7,11,15 only). A/B
  split ~47–80% through the run (near median; coincides with func1
  entry in sc0, switch body in sc22, mid-stream elsewhere) — likely a
  writer-side two-bucket partition. Two live readings: per-emitting-
  line position sample vs flat periodic cursor. Doc + SN-1 updated.
- **Fallback round 2026-09-24d (uncommitted):** closed BZ-1 —
  `section_006` TIM2 IS reached through the `.ebp` directory:
  `003304A0` gates `slotCount>6`, reads `dir[6]` at `[RDI+0x28]`,
  `FUN_00330060` binds it to `022C6CF0[mgr]` → `FUN_0026C860` →
  `FUN_0029CAC0` refcounted cache → tail `FUN_0039BEC0` registrar
  (the registrar is the path's tail, not an alternative; already in
  the section doc §3, row was stale). NEW DATA finding: the `in`/
  CJK slot-6 TIM2s are **per-event expansion-glyph sheets** — the
  bitmap half of the `18`-code system solved in round-24b. Cell
  capacity at ~10px/glyph bounds the event's `.fex` chunk count
  corpus-wide (alc 66↔~66 cells, dor_a0100 forces <20px pitch:
  64 cells < 65 cps at 20px); `fontex_expand`-bound events fit
  ~20px cells exactly (alc_a0280 14↔280px). Supersedes the "caption
  strip" reading for CJK trees. Section-006 doc §5 addendum + BZ-1
  row closed.
- **Fallback round 2026-09-25 (uncommitted):** slot-6 cell↔slot
  order RESOLVED — subtitle-sheet glyphs pack at ~10 px each in
  `.fex` record order (what reads as one inked 20 px cell = two
  glyphs): `inked20pxCells == ceil(fexCount/2)` on every event
  measured; `alc_a0100` cells render 元/一 head and 事実 tail in
  order (640×23 + 24×23 = 664 px ≈ 66 glyphs ↔ 66 records);
  `byu_b0101` 30↔30 exact; `bhm_d0101` 257 records slack-filled in
  ~320 slots. `fontex_expand` sheets keep ~20 px pitch (alc_a0280
  14↔280 px). Per-glyph advance source (fixed ~10 px vs companion
  table) open; TIM2 header carries no metrics. Section-006 §5 +
  font doc updated.
  **q3 further narrowed (24d):** the A/B split is a CLEAN
  POSITIONAL CUT of one ordered mark stream — both lists ascending,
  max(listA) < min(listB), stride seamless across the cut; cut sits
  at ~48–55% of the marked byte span (≈median mark index) and lands
  at construct boundaries (mapctrl sc1: `break`/`case` seam in
  mapctrl_mj.src ~line 170). blkIndex and even/odd splits falsified;
  last-scope listB garbage was a parse artifact (true end = next
  table). Residual: the ~2-count asymmetry leaves a (begin,end)
  nested-intervals reading unproven.
- **Fallback round 2026-09-25b (uncommitted):** **the `.fex`
  `+0xA8` runtime READER is found** — the two-sided contract closes.
  "font" in `001B4C00` is the text singleton `ctx @ 0x1F811F8`
  (0x2380 B, lazy-built by `001B5F10`), reached via release-cb
  `001B6030`. `ctx+0x30` = `map<fileId→r15>` (write `001B4C00`,
  getter `001B51C0`); r15 (0x120, ctor `001FC060`) holds `+0xA8` =
  `map<eventKey→vector<u32> cps>` (sentinel +0xB0/root +0xC0) and
  `+0x40` = `map<cp→glyph-record>` (the slot-6 TIM2 side). READ:
  `001E9D20(ctx, eax, r8d, r9d)` per source change —
  `ctx+0xF38` `map<u64{eax,r8d}→session>` → `[sess+4]`=fileId(1-31)
  → `001B51C0` → r15; `[sess+8]`=eventKey → **`001FDD60(r15,ek)` =
  the mapA8 find → `ctx+8` = the cp vector**; `ctx+0` = r15,
  `ctx+0x10` = `(fileId*32+slot)` 0x38-B metric slot (the advance
  source — `006B5C70`/`005C5310`). Sessions created by
  `001B58E0(ctx,key)` (refcounted, vfn `001B6229`, `+0x10`=r15,
  `+0x20`=vector copy via `001FDF10`/`001A1E40`, linked into
  `ctx+0x68`/`+0x98`). Walker `002AC2F0`: two-byte `18`-`1B` codes →
  `esi = tbl[lead&0xF] + sub - 0x20` — **two parallel 16-entry
  tables `0x916570`/`0x9165B0` flag-selected by `0x209CC38`** (…5B0
  gives 0x7E0-0xA80 = the CJK/in model; …570 gives 0-0x2A0 = us-style
  global); `lead >= [0x1E0CDF8]` → expansion arm prefers bound
  `[rdi+0x68]`; `001E9860(ctx,esi)` = `ctx+8` bound-checked vector
  remap → `001FDEC0(ctx->r15+0x40)` cp→record. `.fex` blob free
  unregisters via `ctx+0xD0` registry (`002124C0`). Residual: the
  `{eax,r8d}` pair identity; who writes session `+8` (eventKey);
  `18`-code `esi≥0x7E0` vs short-vector semantics — likely the
  `[rdi+0x68]` bound-record arm covers it.
- **Contra repair 2026-09-25c (uncommitted):** FABLE's EC-2
  counter-evidence verified instruction-for-instruction and the
  "dead feeder" verdict **retracted** — `0020AC30`/`0020AF10` are
  reachable via thunk hops `001EC660`/`001EC6A0` (E8/E9 census blind
  spot; `rawcalls.py` follows them) called from
  `0032FCA0`/`0026B750`/`00354B20`/`00354E80`; `\plan_master\<X>\event\`
  `<X>` is the locale (image's own `g_pathTables` `0215F000` via
  `002DF980`, not a dev tree); flags `01F832E8/9` consumed by
  script driver `0025DF00` (`0025E0F0`/`0025E100`), not console-only.
  Rewrote the event-slot page (live feeder + thunk-blind-spot
  methodology note), EC-2 register row via register_row.py,
  PROGRAM-STATE §6. check_questions 0 mismatches. Reply filed to
  SWE2-FRONTIER (task assigned to them).
- **Fallback round 2026-09-25d (uncommitted):** the `.fex` binding
  **producer** traced — session `+8` eventKey = `00674A00(path)` of
  the event's own canonical path. `001E7F90(ctx, sel, fileIdComp,
  eventKey, plane)` files 16-B records from pool `ctx+0xE70` into
  `ctx+0xF38` keyed `(plane<<32)|sel` — so `001E9D20(eax,r8d)` =
  {fontSel, plane}. Three registrars: `0017FC00` (init, plane 2,
  ek=0), `001B6470` (obj+0x278 slot install, ek=0), `001B4590`
  (event-bound — validates `mapA8[ek]` via `001FDD60` FIRST, then
  files). Queue `ctx+0x250` (+0x258 end/+0x260 cap/+0x270 found):
  `001B6350(ctx,sel,flag,pathStr)` pool-allocs `{sel,flag,ek=h33,
  arg4}` and enqueues; `001B47A0` drains → `001B4590`; `001B6430`/
  `001B5330` find/erase. Feeders: `0017FA90` thunk ← `00332250`
  (resolves path via `002DF980` g_pathTables ← `00330310`/`003306E0`
  resource registration) + `00575710` (queue/find/erase driver) +
  `003304A0` (.ebp dir dispatcher, clears pending binds). Plane 2 =
  default bindings; planes 0/1 = live text-source planes via
  `0017FD30`. Residual: per-resource sel/flag/srcId values at the
  `00332250` call sites; `esi≥0x7E0` reach (ctx+8 vs [rdi+0x68]);
  `.dat` header words + `0x24` records.
- **Package round 2026-09-26 (FINISHED rev 29990):**
  `OPUS-REQ-DATA-GLOBAL-REFS-AND-FIELDS-DIRECTION` — access-direction
  repair of the global-refs producer chain. (1) `rip_data_refs.tsv`'s
  producer was unrecorded (the request's own missing-information);
  wrote `gfz-scripts/gen_rip_data_refs.py` — capstone walk of all
  38,161 functions, per-operand direction via `RT.op_kind` (SDM
  mnemonic tables before capstone flags, `?`→other never a guess).
  (2) Regenerated `work/h78/rip_data_refs.tsv`: 164,489 rows, same
  population, **exactly the 5,227 sites of OPUS's iced measurement
  relabelled** — 4,040 read→write (movups/movq/setns stores), 1,100
  write→rw, 19 read→rw (lock cmpxchg), 68 other→read (test); 0 added,
  0 dropped; `--check` prints the pair census. New `rw` kind carries
  the RMW class the file lacked. (3) `gen_array_census.py` — both
  positional `w if oi==0` sites → `RT.op_kind`; ActorManagerSlot regen
  **byte-identical** to OPUS's block-222 relabelled file (112 r, 1 rw).
  (4) Consumers: `knowledge_db.py` writers/readers-of-global now
  `kind IN ('write','rw')/('read','rw')`; `globals_index.py` shows an
  `rw` bucket and counts rw into writers/rank. Sibling notice
  `OPUS-NOTICE-DATA-FIELDS-PART-DONE-BY-OPUS` acknowledged+closed —
  fields.tsv 50-row scope was OPUS's own, left untouched.
- **Fallback round 2026-09-26d (uncommitted):** `.dat` closure pass —
  `001FC060` decodes the full 0x120-B font record: header `+0x00`→
  rec+0x00, `+0x04`→+0x18, `+0x08`..`+0x14`→+0x24/+0x28/+0x2C/+0x30,
  `+0x20`/`+0x24`→+0x1C/+0x20, float→+0x34; three EASTL maps at
  rec+0x38 (glyph recs) / +0x70 (the `.ker` pair map) / +0xA8
  (mapA8 event→cp vec); strings +0xE0/+0x100. Flag arms resolved:
  `001B5750`/`001B5480` are identical twins — require `ctx+0x30[fileId]`
  filed, alloc a node from `ctx+0xD0` (`001BA860`), mint a type-4
  request {cb, node, name[0x100]} queued via `001A0BB0` — only the
  completion + extension differ: `01DF6E10`→`".ker"`/`001B6080`,
  `01DF6E18`→`".fex"`/`001B6030`. `.data` `01DF6DF8`..`01DF6E18` =
  the five ext strings `.dds.phyre`/`_shadow.dds.phyre`/`.dat`/`.ker`/
  `.fex`; `001B31E0` appends ext to the base name. `001B4D70` tail
  files the rec into `ctx+0x28` keyed fileId via `0020B5F0`. The
  `.dat`→`.fex` coupling is authored: flag bit1 = "this font has an
  expansion file".
- **Rerun state 2026-09-23:** self-test PASS at 147 displacements
  (corrected-walker control). 33 distinct types carry the caveat
  (384 rows: ~230 measured `FOR THIS SPAN` verdicts incl. ~195 ZERO
  negatives, ~44 retracted-negs-now-positive, rest unmeasured/boilerplate).
  Seed table rebuilt from each type's own recorded anchors
  (`call`/`cell`/`slots`/`static`/`vtable`/`ctor` + embeds; unioned per
  (disp,width,site) via `EMIT_JSON`); `gen_array_census` covers the two
  ARRAY types (SpawnGroupLedger, PartyFormationSlot). Driver +
  evaluator: `Tools/work/SWE2-DATA/census-rerun/run_rerun.py` and
  `evaluate.py`; per-seed JSONs land in `census-rerun/out/`.
- **Fallback round 2026-09-26b (uncommitted):** `.fex` walker-mode
  resolution — `esi≥0x7E0` residual **narrowed to a closed form**.
  `002AB7D0` (the language boot init already documented for msb mode)
  writes the two walker globals *together* from `00229E40()` =
  `[0x1E02814]` (language id, shipped default `0xA`): id ∈
  **{7,8,0xB}** — mask `(id-7)&~5==0` minus `0xC`, CORRECTED from the
  older `{7..0xA}` claim in both debug-companions.md and
  decode_msb.py — → `0x209CC38=1` + `0x1E0CDF8` bound = `0x1C`; else
  bound `0x18`. So CJK mode moves event expansion to leads `1C-1F`
  (bases `0,0xE0,0x1C0,0x2A0` — same ~0x33F low window the ≤342-entry
  `.fex` vectors cover, measured all 5 locales) and promotes planes
  `18-1B` (`0x7E0..0xA80`) to ordinary font planes resolved by the
  normal arm. `001E9860` semantics fixed: `esi<size(ctx+8)` →
  `ctx+8[esi]`; `ctx+8==NULL` → raw `esi` key; else **return 0**
  (walker falls back to `[r14]>>32&0x1F` pitch bits — NOT a raw-key
  fallback; earlier draft had it wrong). `0x2B0280` = second flag
  reader (line-layout walker). **ctx+8 residual CLOSED**: `001E9D20`
  stores `ctx+8 = 001FDD60(r15,sess.eventKey)` = NULL on miss; the
  `sel 7|0` default sessions carry `eventKey=0` (filed by
  `0017FC00`/`001B6470` without `001B4590`'s validation) and `mapA8[0]`
  never exists (0 zero-magic keys in 2,476 `.fex` chunks corpus-wide)
  → default binds always raw-key `r15+0x40` by compiled index
  (the verified font00.dat record order) — `esi≥0x7E0` needs no
  vector. Only validated event-bound sessions get a remap vector.
- **Fallback round 2026-09-26c (uncommitted):** `.dat` section decoded
  — `001B4D70` header 0x28 B `{fileId; capacity; 6 ctor words; float
  metric @0x18 (→r15+0x34); flags @0x1C (&1→001B5750, &2→001B5480)}`
  then 0x24-B records `{u32 key; 32-B payload}` filed by `001FDCC0`
  into `r15+0x40` map (single caller; `.fex` never touches it);
  `001FDEC0` returns `node+0x24` = payload ptr. `.fex` chunk format
  confirmed `{u32 eventKey; u32 count; u32 cps[count]}*` via
  `001B4C00` — raw cps, asserts fileId's r15 exists. **Key-space
  model unified**: `font00.dat` rec[0] = compiled index (raw-esi arm),
  fontex `.dat` rec[0] = cp (VERY HIGH — required for the find;
  corpus record not yet read). `00332250` mechanics done:
  `002DF980` → `g_pathTables[kind][id]` = `PS2Data\plan_master\<loc>\
  event\<dir>\<name>\<name>.<ext>` (6 seps); backward-sep cut
  `path[r10+1..r9-1]` gives kinds 8/0x25 → `event\<dir>\<name>` (the
  verified chunk key), kind 5 → `<loc>\event\<dir>` (locale+dir key);
  other kinds never queue. Feeders: `00330310` flag=1 sel=r15d|r14d;
  `003306E0` flag=0 sel=r8d|eax (flag=0 is what `001B47A0` drains).
  Open: sel composite semantics; the 6 ctor words;
  `001B5750`/`001B5480` sub-handlers.
- **Pending uncommitted:** `scan_ctx.py` + this resume edit. Rounds
  09-26c/d/e PUBLISHED `b1e48c934` + `64dc0f528` (`001FC060` record
  map, `.ker`/`.fex` flag arms, `001B4590` drain mechanics, sel =
  desc-slot resolution, **0x1F81200 font-lib vs 0x1F811F8 text-ctx
  split**). PROGRAM-STATE §6 EC-2 paragraph published; peers'
  overlay preserved in worktree.
- **Residual closure round 2026-09-26e (uncommitted):** all three
  `.dat` residuals closed by direct corpus read — the `.dat` files
  extracted from `FFXII_TZA.vbf` (`font-decode/` work dir, 102 files).
  **`fontSetBase` = never-written**: 0 hits on direct
  `[0x1F81200]` stores, getter-`[rax]` writes, and
  rip-load→offset-0-write scans; every shipped fileId is `1`–`22`
  (members of set 0) — `base*32+member` degenerates to the authored
  id. **fontex `.dat` cp-key PROVEN**: every cp in every listed
  `.fex` chunk hits a sibling `.dat` record key — 56,451/56,451
  (100%) across jp/kr/ch/cn expand+subtitle; fontex `.dat` key
  ranges are real cp runs (jp expand `U+2015`–`U+FF5E`).
  **Header semantics decoded**: `+0x08` atlas width
  (0x800/0x400/0x200), `+0x0C` used tile extent
  `ceil(n/floor(atlasW/cellH))×cellH` (reproduces on 6 fonts),
  `+0x10`/`+0x14` cell W/H (repeated per-record), `+0x18` scale,
  `+0x20`/`+0x24` line-metric pair. **Glyph record** `{u32 key;
  u32 utf8; u32 tileY; u32 0; u32 cellW; u32 cellH; u32 advA; u32
  advB; i32 −1}` — `utf8` = the glyph's UTF-8 bytes (`困`→`E5 9B B0`,
  `≦`→`E2 89 A6`), `tileY` walks `cellH`-steps down
  `floor(2048/cellH)`-row columns (column-major atlas tiling).
  us `fontex_expand.dat`/`.fex` are **orphan legacy data** — absent
  from `us/fontlist.ah` (which lists only `fontex_subtitle`), and
  the us `.fex` triples can't be consumed by `001B4C00` anyway
  (previously documented). Remaining open cells: the `+0x20`/`+0x24`
  line-metric pair's exact roles and per-glyph `advA`/`advB` vs
  `w8=-1` sentinel semantics — cosmetic.
  BZ-1/SN-1/EC-2 rows PUBLISHED `e772807d7`; PROGRAM-STATE §6
  EC-2 correction still in worktree under peers' overlays.
- **Latest coherent commit:** `64dc0f528` (drain mechanics +
  lib/ctx object split; 2026-09-26). `@publication` released rev
  30060.
  Prior: `b1e48c934` (.dat record layout +
  flag-arm closure + PROGRAM-STATE EC-2 paragraph; 2026-09-26).
  `@publication` released rev 30053.
  Prior: `e772807d7` (FABLE-requested EC-2
  publish: EC-2 row with behaviour corrections + verbatim thunk call
  sites + `members/event_slot_setter_replay.{py,json}` as authored;
  BZ-1/SN-1 rows rode along; HEAD+rows swap kept peers'
  OPEN-QUESTIONS overlays unpublished; `@publication` released rev
  30048, request finished rev 30047; replay re-verified 8/8).
  Prior: `6ae73592b` (.fex walker language-mode
  resolution + ctx+8 NULL-binding closeout + {7,8,0xB} mask
  correction; 2026-09-26).
  Prior: `82eeb2448` (.fex consumer+producer
  chains, EC-2 feeder repair, access-direction package; 2026-09-25).
  Prior: `dc4414b98` (census-rerun publish —
  fields.tsv 384 caveat amendments, .fex event-hash solve docs,
  section-006 glyph-sheet + BZ-1 chain, .dbg q3 A/B narrowing,
  decode_msb.py fex support, resume; 2026-09-25).
  Prior: `bafd30594` (kanji round-5 —
  倒/死/同/上/下/強/後/受/指 context-verified; btlctrl msg10
  reaction list decodes). Pending uncommitted:
  op_finpub_kanji5 (rides next publish).
  Prior: `c59416b29` (low-tag census +
  e2+ singles — `01`=field separator verified by SE/Voice
  toggles, `e4`-`fe`=single-byte icon plane parallel to
  `10 20`-`3f`, `ff`=indent pad). Pending uncommitted:
  op_finpub_lowtag (rides next publish).
  Prior: `eb6721da4` (`.ebp` RESOLVED — slot2
  == `.msb` byte-for-byte 3/4, evctrl older revision; slot6 = TIM2
  icon sheet; earlier `{u16;u16}` tail = msb directory mis-parsed,
  retracted. Container = envelope + section-000 + msb + TIM2).
  Pending uncommitted: op_finpub_ebpmsb (rides next publish).
  Prior: `bf6062b9e` (kanji round-4 —
  他/盗/融合技/込/初期設定/成功/率/定/読 + `12d3`=`:`;
  `12dd` corrected to bracket-pair open, was misread as 再;
  icon block `10 20`-`10 3f` = 66% of remaining unknowns).
  Prior published: `efd0e92b5` (kanji round-3 —
  `12d9`=`'` possessive verified ~7 contexts; evctrl msgs 31-40
  decode as the COMPLETE authored event list w/ IDs+EN titles;
  `817e`=first-item bullet; `10c8`=item marker). Pending
  uncommitted: op_finpub_kanji3 (rides next publish).
  Prior: `6444300ac` (kanji round-2 + MAP_BEHIND float table
  VERIFIED as the sampler's param table via msg27).
  Prior: `3ed96741f` (`.bin` RESOLVED =
  EBP2 section-000 exported standalone — byte-identical embed
  3/4, evctrl older link; standard 0x90-byte section-000 header
  per section-000-bytecode.md; +0x20 pool msgrefs==msgCount 4/4).
  Prior: `158c7c81a` (`.bin` section map +
  +0x20 constant-pool decode — msgrefs==msgCount 4/4; float-6
  curve; symbol tail). Prior: `781f3227b` (10-plane symbol anchors +
  unified `(lead-0x10)<<8|low` table note). Prior: `f6c6ed898` (`.bin` companion decode +
  mapctrl third-module charset check). Prior: `7ec9e650f` (12-plane = fullwidth
  ASCII verified — evctrl "Event Plan Menu"/"Test Event" decodes).
  Prior: `8eaaeb284` (decode_msb.py tool +
  10c8/ASCII/icon-plane corrections). Prior: `91b5d635f` (JP glyph table DERIVED —
  interleaved-gojuon kana planes + kanji leads; msgs decode to real
  JP; 0e = 4-arg line header). Prior: `6b7ce363b` (bootstrap anchors).
  Prior: `3c4b29a73` (`.msb` 0F-selectors
  = TZA escape-language vocabulary — 1-arg cmds all sit in the
  `@`-`k` icon block, 2-arg cmds are the parameter escapes).
  Prior: `d027c4bb7` (q3 byte-periodic
  stride data + `.msb` 0F-command positional census). Prior:
  `d85974868` (S2 slot-1 = `.msb`
  message-constant name table — `{count=msgCount; tag=1; pos[]}`
  naming each message's `select_*`/`mmes_*`/`mes_*` constant in
  index order, 4/4 modules; evctrl msg0 resolved — `select_base`
  called only under compile-time-false `if(ISDEBUG())`, dead-
  branch eliminated). Prior: `b861edcf7` (front-stream tag byte
  = native descriptor `{width:4;float:1;class:3}` top byte
  verbatim; width3=s16, width5|float=f32 — all six width cases
  in-corpus; width-3/5 residual closed). Prior: `7c59ba5b9` (q3 re-corrected to a
  two-list stream `{countA; FF; listA[countA]; listB[]; pad}` —
  head IS listA's count; zeros in listA are real marks; the
  sc18/sc19 anomaly resolves to a byte-0 mark sc19 counts).
  Prior: `1fbd3d2c5` (front-stream field
  order corrected — pairs are `{id; nameHeapPos}`; gdbg ordinal
  `N ↔ global_debug_flag[N]` exact 4,096/4,096; N+34 skew and
  tail-verbs readings retracted). Prior: `9d10d353d` (T1 = the ATEL
  verb-category directory — 67 fixed buckets of name-start heap
  positions, identical bucket→family map in all four modules).
  Prior: `2a86bc5dc` (q3 marks = interior
  bytes of flag=1 ins at ≈4-ins stride over the scope's code
  prefix; +3/+4 drift where 1B ops intervene). Prior:
  `e60df4de6` (q3 correction — head
  field is NOT the entry count; vals = ascending bytecode-offset
  sample over scope prefix, uniform across ins byte positions,
  present with empty q1; head is scope-bound). Prior:
  `095884f0b` (front id = descriptor byte3 + byte offset →
  global-variable directory); `3c1572ac0` (front stream = ONE
  heap-position-sorted `{pos;id}` directory over all heap names;
  gdbg block uses flat 0..0xFFF ordinal at name-length strides,
  pre-gdbg ids carry class-like tag bytes resembling the
  descriptor class|float|width field — 5/92 ebp descriptor match,
  id semantics open; S1 = heap start holding the .sbn block source
  paths; S2 = 64-slot directory, slot1 = module-global symbol list
  of file offsets into global_debug_flag[734+]; S0 field tracks
  .sbn block count). Prior `c293aa785` (q0 FULLY RESOLVED as
  byte-granular bytecode→source map; q2 = stride-32 instruction
  checkpoint; q1 corrected to per-scope symbol set incl.
  `@`-labels; q3 narrowed to bytecode byte offsets),
  `04c7759e1`: T1 shared-66-list
  structure + q1 per-scope flag partition + heap @-label census;
  prior `7b2433098` `.dbg` header = 16-entry
  section dir at `+0x2C`; T1 = 67 ascending sub-lists identical across
  all four modules → shared-structure index; heap ~150 KiB to EOF incl.
  `@IFTERM`/`@IFELSE` labels; q0 items = arity-{1,3} sub-records headed
  by `flag=1`; q3 lands inside multi-record items only, 809/810).
  Prior `62aa56668` (front-stream pair directory), `757f5962b`
  (q2 stride-32 checkpoint) remain valid.
- **Pending requests/reviews:** `DATA-REQ-AUDIT-SEM-TYPE-TABLES-REVIEW` →
  SWE2-AUDIT-SEM; `DATA-REQ-AUDIT-SEM-MESH54-REVIEW` → SWE2-AUDIT-SEM;
  `DATA-REQ-AUDIT-SEM-DRAWMASK-REVIEW` →
  SWE2-AUDIT-SEM; `DATA-REQ-AUDIT-SEM-ROWSTRIDE-REVIEW` →
  SWE2-AUDIT-SEM; `DATA-REQ-AUDIT-SEM-HIMG-REVIEW` → SWE2-AUDIT-SEM;
  `DATA-REQ-AUDIT-SEM-BINMENU-REVIEW` → SWE2-AUDIT-SEM;
  `DATA-REQ-AUDIT-SEM-SIXFAM-REVIEW` → SWE2-AUDIT-SEM;
  `DATA-REQ-AUDIT-SPEC-MENUMAP-REVIEW` → SWE2-AUDIT-SPEC (first review);
  `DATA-REQ-AUDIT-SPEC-SETTINGS-COMMANDS` → SWE2-AUDIT-SPEC (first review).
- **Fallback eligible work:** loader-bound residue — `behindcamera`
  polyline axis semantics narrowed further post-`caee8e80f`:
  `baseScalar` confirmed = follow-target **height offset** (`003D9950`
  adds it to `ctx640.y`; `003D9930` routes it to `mover+0x11C`, added to
  `target.y` by `0032B1C0`, ctor default 1.3 = record 0); `003D99B0`
  bakes record-0's exact `{x,y}` curve from `.rdata 01EFE998` as the
  compiled-in default; `02098DE9`/`02098DEA`/`02098DEB` = transition
  flag + countdowns (`0025A540` seeds `obj+0x00`); `ctx+0x850` = pose
  blend `t` (`0025A620`/`0025A6A0`/`00259510`). Still open: the per-frame
  `{x,y,segFrac}` triple sample — ~22 routines inspected across camera +
  mover modules (movers `0032AEC0`/`B1C0`/`B600`/`B900`/`C5E0`/`D000`/
  `DF40`/`C910`, segment/basis `003CC080`/`CBD60`/`C130`, camera
  `00259990`/`00259510`/`0025A540`/`0025A620`/`0025A6A0`, ctors
  `003D99B0`/`9B80`/`9C40`, verb chain `0030F4B0`); `0032DF40` = eased
  channel-key installer (smoothstep poly), mover works on single keys —
  triples remain write-only among traced code. Handbook residue — `hctg`
  `textId` naming conventions (cosmetic).
  `hchk +0x0A` closed dead (no reader, no trailing region; published
  `2645a9f4d`); `hchk +0x03`/`hdat arg`/strBlob ops/monster tail v1-v3
  all closed dead-on-path earlier.
  **Board artifact:** all six READY items addressed to SWE2-DATA are
  stale DONE+READY duplicate pairs (DONE copies carry closure
  checkpoints at `a9f60432` etc.); finish/claim on the READY ghosts
  returns invalid transition — do not re-chase.
- **Latest coherent commit/checkpoint:** `47b0b40fe` (sn1dbg:
  front-stream flag bases — flag-0 text-relative corpus-wide,
  flag-1 = stride-24 slot enumeration); `e7ba3501a` (sn1dbg:
  `.dbg` scope-stream `pos` = 0-based source line number —
  flag=1 marks on statement lines, scopes tile the file per
  top-level entity, items fixed-arity {1,3});
  `da49385a1` (sn1dbg:
  `.dbg` heap-span membership + front-stream flag classes —
  enclosing-name-span referent, `flag=1` = second-source mark,
  `0x2000`/`0x5800` shared-content marks, `0x3000` = per-run u16
  counter); `b21aa82e5` (sn1msb: `.msb`
  flag correlate — `10 C8` items only in flag=1 messages);
  `c4c15618b` (sn1msb: `.msb`
  token grammar — variable-length `0F` escapes + `12`/`0E` tokens
  verified corpus-wide); `aa26bf717` (sn1dbg: `.dbg`
  q0 scope streams + quartet roles + suffix-compressed heap; FABLE's
  parked GF-1 row rode along in OPEN-QUESTIONS, advisory reservation);
  `7e5ed701f` (sn1pg: `.sbn`
  paged 32-line map fully decoded — "aux array" retracted as a
  misdrawn boundary; `.sbn` closed, residual = `.dbg`/`.msb` payload
  grammars); `6785d23b6` (sn1: ATEL
  debug-companion layouts — `.sbn` textOff resolved, `.dbg` mapped,
  `.msb` envelope; payload grammars open); `4409ba387` (bcscalar:
  behindcamera scalar = target height offset, record-0 baked default);
  `caee8e80f` (LBB: loader-bound
  .bin package + gate triage — check_layouts crash fix, MrpHeader
  clash reconcile, MP-2 fence normalization, RULES.md regen);
  `2645a9f4d` (hbfin: hchk
  +0x0A dead field); `cb2c84adb` (hbtail:
  00576300 line builder); `30dd8698f` (hbtab:
  00576CA0 + dead-field confirmations); `c712f8cfe` (hbsec:
  sectioning closed); `1b1aee01d` (hbarg: arg serial + 00577970);
  `5739a439a` (hbrec: record +0x04); `6715ccbd5` (hbmap:
  page-map/resource-slot decode);
  `27faf2401` (hbstr: strBlob op-programs); `39426d811` (hbdetail:
  tail reader + descriptor); `ecfd71e54` (hbcarry: tail v0/v3
  joins); `8ab8c7e10` (hctg aux decode);
  `1f9f37678` (HBINDEX package); `9f691756` (listtype census);
  earlier `622e24f4` (stamp fix), `35922615` (cyclekey census);
  earlier `0ddb954f` (loader tail), `aee9d467` (req-channel census),
  `4648552c` (loader-bound bin
  families); earlier `90b1376a` (snd class census), `07d5455c` (pass-22),
  `8a5bc471` (settings command
  table); earlier `4468befe` (handbook hops), `e81760f0` (label-table scan),
  `5a08ef5c` (VIF packet templates), `a9f60432` (pass-22 neighbour
  fix); earlier `f353c915` (effect type tables), `fe97ca5d` + `b85ffb4c` (mesh-0x54 census),
  `6a4b3b8e` (framelimit notice), `fe203d98`, `0f77630c`, `71546dd3`,
  `4568ea75`, `354c3089`, `98ad9786`, `d0436824` + `79510a96`;
  board rev ~16311.

## Checkpoints

Append below, newest last. Record corrected facts and remaining work, not file growth.

## 2026-09-14 — DATA-FMT-PS2IMG-TAIL: all six sheets published, 40 → 46/48

Six format sheets written under `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/`,
`check_assets.py` now reads 46/48 — the declared ceiling (`.bin`/`.dat` are extension buckets;
the `bucket` disposition is routed to SWE2-AUDIT-SPEC, not scored from this lane).

Corrected facts this package surfaced:

- **`.mrp` is a relocated-pointer table container**, not a fixed-header blob. The relocator
  `002A00F0` (via `00249660`, installed by `00249320`) rewrites `+0x08`/`+0x20`/`+0x28` offsets to
  pointers in place and flips magic byte `+3` to 1 as the already-relocated flag — which is why
  `MRP\0` has zero `.text` hits. The `+0x0C..+0x2F` run is five `{count, offset}` table slots;
  three ship empty parked at EOF. An earlier "three file-size fields" reading was an emptiness
  coincidence and is corrected in the sheet.
- **`.as7` "two variants" = one format** — `A7` + u16be count (64 vs 3,096) + u32be tailOff +
  count × u32be file-absolute offsets; `offsets[0] == 8 + 4*count` on all 18.
- **`.btm` has no header at all** — the leading zero dwords are glyph pixel data; the format
  contract is the external glyph table's `pixelOffset` indexing `022CBE00+0x110+slot*8`, bound by
  `00365810` (12-id table `00D10C98`, ready bits `+0x240`).
- **`.lst`**: `qstl` + capacity 100 + `dataOff` 0x220 + 66-entry `{questId, dataRel, kind}`
  directory over NUL-terminated encoded strings; kind is a u32 ∈ {0,3,4}; ids are distinct but
  shipped non-sorted (172 before 168).
- **`.cl2`**: `CLT2` + const `0x00010004` + `{dataSize+0x30, dataSize, count}` + `count×4B`
  palette with **0..255 alpha, not PS2 0..128**.
- **`.mg`**: header `{version, offIdxA, offSectionB, sizeSectionB, offVerts, …}` + 4-slot
  `mainN.psd` directory + vec4 corner block; `0x2D0 + 0x3280 == 0x3550` makes `+0x0C` a size, not
  an offset (an earlier draft had it wrong).

OPUS-HANDOVER-SWE2-DATA-LST-CL2-BTM folded in — three numeric disagreements checked against the
bytes, all confirmed as OPUS-addresses-`+4`-shifted or OPUS-correct (kind u32, alpha byte, mg size
field). FABLE-REQ-SWE2-DATA-MESHDATA-MG's readers (`00562F90`, `00561390`) cited and the sheet
linked from `16-UI/Map-Screens`.

## 2026-09-15 — DATA-FMT-PS2IMG-TAIL: correction pass before publish

Two real errors found by re-running every corpus check against `extract/manifest.tsv`
(authoritative) instead of the on-disk walk:

- **`.cl2` field offsets were all one dword too low.** Raw bytes on `us/loca_bhm.cl2`: `+0x10` =
  `0x830` (endOff = dataSize+0x30), `+0x14` = `0x800` (dataSize = fileSize−0x40), `+0x1C`/`+0x1E`
  = the `0x30`/`0x0200` u16 pair, `+0x22`/`+0x23` = `03`/`05`. The previous revision's
  reconciliation note had it backwards — **OPUS's +4-higher numbering was correct**; the earlier
  pass verified `+0x04` only and never re-read the upper fields. Sheet corrected (frontmatter,
  layout, loader table, falsification, open-questions) and all 20 files re-verified.
- **`.mrp` "120 of 120" was a walk artifact.** The extract dir held 4 stale root-level probes
  (`e3_logo`, `loca`, `party_book`, `title` — all byte-identical to `us/` entries). The manifest
  has 116 rows; all 116 verify clean (`MRP\0`, `descOff=0x30`, `tailOff+16*tailCount==fileSize`,
  three parked `{0,fileSize}` slots, `ref` in-bounds 1,458/1,458). Sheet counts corrected;
  descriptor total is 1,458 not 1,533.

`.lst`, `.as7`, `.btm`, `.mg` re-verified unchanged (lst ids/kinds `{0:21,3:44,4:1}` + monotonic
rels; as7 `A7`+u16be count+u32be tailOff+offsets at +0x08; btm headerless; mg section-B closure
`0x2D0+0x3280==0x3550`).

## SWE2-FRONTIER (planner) — 2026-09-15: please narrow DATA-FMT-PS2IMG-TAIL's resources

`FABLE-REQ-FRONTIER-STALE-REGISTER-LOCK`: your claim has held `file:_index/open-questions.md` and
`file:_index/audit-log.md` since 2026-09-13T21:12 with no checkpoint. Both are shared publish-time
surfaces — three deliveries are queued behind them (FABLE-LEDGER-AP7-EU1,
OPUS-REQ-FABLE-REGISTER-PROSE-ANSWERS, FABLE-REQ-SWE2-FRONTIER-ORPHAN-QUESTION-IDS).
`OPUS-CONTRA-DATA-INDEX-LOCK-SCOPE` (READY, assigned to you) is the same defect in contra form.

Requested action: checkpoint `DATA-FMT-PS2IMG-TAIL` and drop the two index files from its
resources until you are actually publishing — claim them per-commit under `@publication` like
everyone else. If the claim is parked, say so in its checkpoint so the planner can rotate it.

### Resume — 2026-09-28 (post-UC-1; CKPT10R2 next) (SWE2-DATA)

- **Done this session:** REQENABLE exec-half `d77b4b587`; SN-1
  corrections `d61e25653`; UQ-218 residue incorporation `f67421173`; G-3
  close-out `6c6a6d3b0`+`becdc9a48`; UQ-213 hub-call correction
  `51de740cc`; UQ-218 slice 1 `bbcaeb95a`; progress-repair
  `b7db7b874`+`efbff7cc7`+`62480dc78`; FABLE route-gaps `98b6b8bd7`;
  UQ-218 motion pass 2 `7d8111938`; **UC-1 population readers
  `6d475a02d`** (every reader on 34,269+696=34,965 / 38,856; uc1_band.py,
  13 guarded own-loaders, program_coverage authored 29,356,
  `test_uc1_band_readers.py` 22/22, request finished rev 36279);
  **denominator-synonym repair `36b445739`** (contra closed rev 36349 —
  SERIES_SYNONYMS collapse {34269,34270}/{38160,38161}, decimal-NUM
  guard, caption-stated local denominators; self-test extended, live
  scan 0 undeclared).
- **Active claim:** `SWE2-DATA-UQ218-MOTION-RESIDUE` (P2 research).
- **Next work — P1 first:** `FRONTIER-REQ-SWE2-DATA-PROGRESS-REPAIR-CKPT10R2`
  (READY, P1) — progress_report.py C1 (snapshot.json semantic tamper
  undetected — bind semantic contents to the validated generation, not
  just fp), C2 (AUDIT-LOG.md consumed by terminal_receipts but not
  fingerprinted — every consumed source must be fingerprinted), C3
  (empty-but-present required input regenerates clean CURRENT —
  distinguish schema-valid cleared register from empty/truncated input);
  preserve the six passing controls.
- **Then READY:** `OPUS-REQ-DATA-SN1-DBG-FRONT-TABLES` (P2 — .dbg front
  tables T1/T0/T2 corrections in the-ctrl-module-debug-companions.md s2),
  `FABLE-REQ-SWE2DATA-ACCEPT-SQ1-DWORD0-CORRECTION` (P2 — accept/amend
  struck dword0 paragraph in spp-map-sound-list.md),
  `OPUS-NOTICE-DATA-STRUCTURAL-OBLIGATIONS-UNCOUNTED` (P2 — decide how
  page-only boxes + DISCOVERED fields count).
- **Then resume UQ-218 residue:** `@FMC` payload grammar, `@FMN` second
  name/u16 tail, `@FMW` channel→component map, `.ca` variant-1 slots,
  embedded-EFX sweep, `+0x44` handle consumers, `0041E580` callers.
- **Latest commit:** `113cca077`.

**Workflow adoption — FF12-WORKFLOW-MIGRATION-20260928-01 (dispatched by SWE2-FRONTIER, 2026-09-28, at next safe checkpoint).**

The user approved a completion-driven workflow migration. Preserve your current identity, active work and ownership. Read the adopted _index/workflow/COMPLETION-WORKFLOW.md and its revision at your next safe checkpoint. OPUS now owns technical migration delivery; ASTRA/SOL independent engineering verification; FABLE connected mechanism completion; FRONTIER operations, safe deployment and capacity allocation. Existing specialist roles remain. This supersedes older operative instructions assigning sole migration architecture to FRONTIER or categorically forbidding useful new tools; it does not supersede full L1+L2 requirements, independent review, safety, game-state protection or history. Do not stop useful work merely to re-plan. Respond through current checked records, self-check changes, consume review, update authorized canonical files and select the next eligible task without user relay. Honour explicit stops and limits. Report a real policy/ownership conflict instead of silently overriding it.

Read the adopted _index/workflow/COMPLETION-WORKFLOW.md, current evidence policy and checked task state. Preserve your existing lane identity, history and peer work. OPUS owns technical delivery, FRONTIER assignments/deployment, SOL independent engineering verification, FABLE completion semantics. Complete your assigned contribution through its required canonical changes and review; a request alone is not package closure. Use existing task IDs and exclusive paths; do not create a competing implementation or direct-edit TEAM. If capped or blocked, checkpoint for a supported handoff and do eligible independent work, without evading limits.

SWE2-DATA: implement OPUS's assigned reporter, obligation and dashboard components in the existing backend. Preserve the prior repairs and complete the remaining R3 cases: complete consumed-input fingerprints, schema-valid empty inputs, full page/register/carrier crosswalk, retained last-good generation, final guarded cutover and coherent export. Bind every semantic output and exact source version without self-hash cycles. Mark absent host comparison as SKIP/UNMEASURED, not PASS.

Build the local read-only live interface and source adapters according to the brief. Import all actual game categories and the VBF browser's real taxonomy; no invented extension-only substitute. Link mechanics to instructions/fields/assets/evidence/reviews. Label physical, semantic and runtime coverage separately with versioned denominators and unknown populations. Use deterministic events/incremental updates, not LLM polling. Keep user-visible outcomes and exact remaining actions prominent. Supply source/config/tests and portable snapshots inside the database. You are not a permanent gatekeeper: authorized handoffs can allow another worker to finish an assigned consumer safely.

Self-check and record exact source/driver/input/result identities and limits. Use a qualified non-author for independent acceptance of your production. A required upstream failure or missing result is not PASS. Preserve historical receipts and relevant regressions; run impacted checks during development, broader campaigns only at governing gates. Update the actual tool/consumer path and persistent procedure so the same defect is caught next time. Use fresh preimages, supported writes, short publication claims and meaningful commits. Keep contribution DONE separate from parent acceptance and whole L1+L2 completion. Respond through the existing board and continue eligible work without user message relay; honour explicit stops and real limits.

**PRIORITY DISPATCH (SWE2-FRONTIER, 2026-09-29, user-directed).** Please take `OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS` at your next checkpoint — the user asked for it directly. The UNMEASURED figure stays UNMEASURED until `Database/Tools/work/formats/bucket-members.tsv` declares the member formats of the bucketed `.bin`/`.dat` extensions (FABLE ruling mp1-meanings-review C4: a bucketed extension is not an accepted disposition — the members are the requirements). Your UQ-218 claim stays yours; checkpoint it if you context-switch, per the checkpoint-or-narrow request already in your queue.
