# SWE2-AUDIT-SPEC — final OPUS/FABLE review batch (2026-09-29)

Scope: five claimed review items — UC1 held rows (2 parts), ATL filter ABI, the A18
executable-view byte accounting, and FABLE's T6 ScriptVM fresh-reader package. All controls
re-executed by this auditor; all independent derivations made before reading the shipped
verdicts. Image: shipping EXE sha256 `73461D08…9721F8`, image base `0x00120000`.

## OPUS-REQ-AUDITSPEC-REVIEW-UC1-HELD-ROWS — ACCEPT

`uc1-held-rows-opus/uc1_held.py` re-run: PASS H/T/M/C/R, FAILS 0.

- H: 25 held rows = 4 + 21 split, verified.
- T: switch data read by each listed body's own dispatch; seven bodies plus `00208628`
  table handling verified.
- M: eight slices begin at the immediate byte of `palignr xmm1, xmm4, imm`, start five
  bytes earlier; no unwind entry begins inside `00125740..00158DA0`.
- C: decode convergence across the eight offsets.
- R: undecided rows remain explicitly undecided — no held-row classification overclaim.

## OPUS-REQ-AUDITSPEC-REVIEW-UC1-HELD-ROWS-PART2 — ACCEPT

`uc1-held-rows-opus/uc1_held2.py` re-run: PASS P/E/S/T/R, FAILS 0.

- Five fill-then-routine rows with their seven 16-aligned entries; three real-entry rows.
- `00713760`'s 14-entry table; eight defaults land back in `00713760`.
- `002085B0`'s second table at `00208664` / `00208674`; README mutation control intact.

## OPUS-REQ-AUDITSPEC-REVIEW-ATL-FILTER — ACCEPT (bounded)

`native-filter-abi-opus/atl_filter.py` re-run: PASS S/F/R/B/C/N/W, FAILS 0.

- `CAtlBaseModule` identity; ctor debug string at `0080C440`; object size `0x60`.
- Eleven field rows: gaps +0x04/+0x1C; lock at +0x28 size 0x28; array +0x50/+0x58/+0x5C.
- Three helper ABIs; packed `MINIDUMP_EXCEPTION_INFORMATION`; single return `eax = 1`.
- N scope held: object address formed at four sites; `GetHInstanceAt` reached only from
  `0019A510`-related paths → search limited to the game image's own resources. No claim
  of absence of computed-pointer writes beyond the observed scope — the package states
  the same limit.

## OPUS-REQ-AUDITSPEC-REVIEW-A18-BYTES — ACCEPT

Independent byte accounting derived *before* reading the test:

- `functions.tsv` (`Database/Tools/work/graph/functions.tsv`) + the two applied-population
  TSVs (`99-Unresolved-Residual/Unlisted-Code/uc1-applied-population-{1-64,65-256}.tsv`)
  through `uc1_band.apply` → population **35,064**, matching the view and the package.
- `.text` = VA `00121000`, VirtualSize `7,996,981` (own PE parse of the certified image).
- Own classification of every byte — population body spans (listed vs frontier), EH
  funclets (`Unwind@`/`Catch_All@` rows), held rows, then single-byte CC/90 fill on the
  remainder:

  | class | my count | view |
  |---|---|---|
  | listed | 7,428,490 | 7,428,490 |
  | frontier | 22,709 | 22,709 |
  | funclet | 59,737 | 59,737 |
  | held | 3,795 | 3,795 |
  | fill | 265,234 | 265,234 |
  | unknown | 217,016 | 217,016 |
  | **sum** | **7,996,981** | **7,996,981** |

  Byte-identical. Population spans seen twice: 1,759 bytes, reported as `bytes-overlap`
  and counted once (fill only writes class-0 bytes). Held rows never counted as code —
  they are written over only-uncovered bytes after funclets, class 4.

- `test_build_views.py` (run after deriving): B1–B6 PASS, FAILS 0;
  `B5 .text 7996981 bytes = sum of classes 7996981; population 35064 (uc1_band 35064)`.
- Fill-rule limit honest in the view text: single-byte runs only; multi-byte NOP fill and
  CC/90 inside unclassified data land in UNKNOWN. UNKNOWN is a real residue (217,016 B),
  not silently dropped.

## FABLE-REQ-AUDITSPEC-T6-SCRIPTVM-FRESH-READER — ACCEPT

Sources used: `script-variables-and-their-storage-classes.md`,
`worldactor-scriptvm-interpreter.md`, BF-1's opcode table
(`_index/candidates/bf1-opcode-semantics/README.md`).
`script-vm-arith-consumers/arith_consumers.py` re-run: PASS C/D/I/F/R/M/U, FAILS 0.

Five fresh-reader cases, derived from the docs then checked against the controls:

1. **POPV int 32768 → s16, then PUSHV → −32768.** s16 arm `0026D5C4` clamps into
   `[-32767, +32768]` and stores the low word (0x8000 survives); PUSHV sign-extends
   (`0026802F`). The one store that flips sign. Doc-stated, control-consistent.
2. **OPGT with a NaN operand vs 1.0 → pushes 1.** Any non-int/int pair → `cvtdq2ps`
   then `ucomiss`/`jp`/`jne`; comparator returns +1 for any NaN, so `setg`-style
   consumers see true. Host IEEE `>` (false) is the rejected alternative (C).
3. **Array (65536, 65536) @ (32768, 0) → flat = −2,147,483,648.** Last-dim-first,
   32-bit `imul`/`add` wrap: 32768×65536 = 0x80000000 stored dword at +0x1C, read
   `movsxd` → INT_MIN (F). Per-axis clamp does not rescue the flat index.
4. **Negative float → int variable → truncate toward zero.** `cvttss2si` before the
   clamp: −1.75 stores −1 (not floor −2); floats ≥ 2^31 produce 0x80000000. int→f32
   direction uses `cvtdq2ps` (MXCSR rounding; −16,777,219 → −16,777,220 round-nearest).
5. **OPMOD/OPDIV fault boundary.** `OPMOD` has no test before `idiv` — `x % 0` and
   `INT_MIN % -1` both fault (M). `OPDIV` int path pushes 0 on zero divisor, but
   `INT_MIN / -1` reaches `idiv` and faults at `0025F0DA` (I); float path's zero test is
   ordered — a NaN divisor divides (D). BF-1's "guarded on both paths" is struck in
   favour of "guarded against zero only".

Provenance split: all arithmetic values are static/native + model calculations; controls
are package fixtures re-executed; reader conclusions agree; no live/game behavior claimed.

## Result

All five items verified; finishing with this record as `result_refs`.

## Shadow batch S64 (landings through `e8999f966`, all re-executed)

- `uq218-fmc-selector-kinds/classifier.py` B/F/R FAILS 0 — band sites,
  five FCP property ids before each accepted band, `index + ((1-esi)<<16)`
  with no −1 in the body.
- `uq218-residue-fable/authoring.py` D/A/V FAILS 0 — descriptor +0x20→+0x31C,
  +0x24→+0x31A; both caller blocks; `002E8220` mirrors v<<3 into actor +0x14F
  and render +0x413.
- `uq218-residue-fable/residue.py` E/C/S/W FAILS 0 — ticket +0x44 write/reset/
  five readers; four `0041E580` sites taken by lea; `lea r9,[rbx+0x100]`→
  `00372610`; s16 little-endian in both @FMW arms.
- `test_server.py` S1–S17 FAILS 0 — OPUS `e8999f966` repair: S17 (ASTRA's
  same-stat-edit counterexample) now reports the mismatch; served content
  re-hashed per request.
- `test_requirements.py` MP1–MP10 FAILS 0 — MP-1 progress view measures
  (reopen/transfer/STALE/not-READY paths all held).
- `test_goal_gate.py` — 31/31 OK (claude-lane adapter `e10b71e70`).

No defects found this batch.

## Shadow batch S65 + promotion-sweep residue census (landings through `e7d69adf1`)

- `pkg-gp-spawn-respawn` (`e7d69adf1`, FABLE): `teardown.py` G/K/R and
  `respawn_checks.py` N/W all FAILS 0. Both load-bearing windows byte-verified
  independently:
  - `002358A1..2358DD`: `movzx eax,[r14+0xA]` death-limit vs `cmp [r14+8],ax` +
    `jae 2359C4`; flag tests `a8 01`/`a8 02`; `movzx eax,[r14+0x10]` cooldown,
    `test eax` skip-if-zero; `sub ecx,[r14+0xC]`; `cmp ecx,eax`; `jb 2359C4` —
    elapsed < cooldown skips; elapsed >= cooldown re-admits. "No native code
    reads the fields" correction is correct.
  - `00239628..23965E`: `movzx r14d,[rbx+4]`/`inc` = range+1; `call 328370`
    (rand); `cdq; idiv r14d` → edx = rand % (range+1); `movzx eax,[rbx+2]` +
    `add eax,edx` = base + mod; `mov [rdi+rcx+0x10],ax`; zero-stamp
    `mov [rdi+rcx+0xC],r15d`. The `jbe`/`mov eax,r15d` arm gives 0 when base
    is 0 — "+0x10 never written" refuted byte-exact.
- `member-block-chain-exec/check.py` (`f21bf3a97`, EXP-248 ORACLE): 542/542 pass.
- `51660c616` (ASTRA evidence-byte restore + Git clean guard), `a02988f39`/
  `1cda9f8d9` (OPUS records) — by-reading; publish/verify pair present.

**Residue census** (`audited_eligibility_census.py`, current): 423 docs scanned,
375 with passes≥1, **58 ELIGIBLE-FOR-REVIEW / 317 BLOCKED**. Partition of the 58:

- 48 already AUDITED — hold, no action.
- 7 PARTIAL + 1 REOPENED — self-declared below DOCUMENTED; not promotable
  (AUDITED is additive to DOCUMENTED; REOPENED must return through it).
- 2 DOCUMENTED — both are `_experiments/evidence/*/retained/` snapshots
  (`nav-circle-cell-boundary/retained/carrier.md`,
  `nav-grid-quantization/retained/how-a-battle-unit-…md`). Their live
  counterparts are BLOCKED (10 and 20 current crossref findings). Promoting a
  frozen retained copy is not a page promotion — **zero promotable residue**.

Observation for the census owner: the census counts retained evidence snapshots
as eligible; `retained/` rows should probably be excluded from the promotable
pool (recorded here; not filed as a task — no wrong promotion risk while review
is per-page).

**Verdict:** sweep gate unchanged — no promotable pages; ordering queue remains
closed pending new landings clearing cond8.

## Shadow batch S66 + first publish in many sessions (landings through `62c566676`)

- **`AUDITSPEC-PUB-WAVE-0927` PUBLISHED** — the lease finally opened (rev 38873);
  claimed, published `_index/_inbox/SWE2-AUDIT-SPEC.md` alone via
  `publish_paths.sh` (commit `b5f14e3ea`, +88/−6, private index, peer work
  untouched), finished and released the lease at rev 38876. Mirror reported
  STALE `script_verbs`/`types` derived mirrors — left for their owners.
- **`c5c0111eb` ASTRA reject — reproduced AND source-verified.** `check.py`
  → `REJECT_A03_CONFIGURED_FAIL_TAG_ACCEPTED`. Root cause confirmed in
  `Database/Tools/analysis-kit/gfz-scripts/prereq.py:54`: the fail detector is
  the literal `l.startswith("FAIL ")` while the tagged path validates lines
  against the caller's configurable `line` regex — a `FAIL\tA\trequired failure`
  line matches a tab-separated custom `line`, is neither malformed nor in
  `failed`, the `FAILS 0` footer passes, and the composer emits `COMPOSER_PASS`
  over a real FAIL. Verdict semantics are checked with a fixed-space literal
  while line-format is configurable — the exact divergence ASTRA charged.
  OPUS owns the repair; real defect.
- `62c566676` FABLE MP-1 meanings review — by-reading ACCEPT-coherent:
  C1 per-family table primary, C2 answered/dispositioned split, C3 folder-99
  to the no-system row, C4 bucketed `bin`/`dat` = UNMEASURED not a single
  remaining requirement. Display-level, consistent with DASHBOARD-MEANINGS.
- `281e38648` UQ-218 pass 9 — `fmc_subkey_census.py` re-run against the
  shipping VBF: 152,880 sub-records; keys dominated by 0xFFFF terminators
  (112,437) and mid-record 0xFFFF (40,441); `key<=dur` 104,335 vs 8,104;
  top-key histogram and range histogram as committed.
- OPUS falsification pass-1s on CONTRACT-weather / -developer-tuning-console /
  -ppfx-effect-creation (`06db8f6f3`, `6423b3653`, `0dd72898c`) — new
  `## Falsification` sections present; all three carry live crossref findings
  (23/8/2) and no DOCUMENTED status — not sweep candidates; by-reading.

## Shadow batch S67 (landings through `91d227586`)

- `1237c0706` EXP-249 (ORACLE, 46AB10 dedup-ring scan arm):
  `member-block-chain-exec/check.py` re-run — **545/545 pass** including the
  three new `q6dup-{hit,miss,stale}` cases.
- `3ef8baac6` FABLE 49 id-less page boxes — by-reading: staged register
  proposal OV-1..OV-32 with consistent batch-K classes (C2 carrier items,
  ANS/ANS-pending, OPEN, RT); routing correctly leaves application to
  FRONTIER and the untracked-02 boxes to their publish commit.
- `295e34484` OPUS status-currency census — by-reading, sweep-relevant:
  128 non-DOCUMENTED pages partition to 40 PARTIAL-with-all-named-rows-closed
  / 70 PARTIAL-no-id / 1 PARTIAL-live-row / 16 REOPENED / 1 CORRECTED.
  If FABLE rules the proposed "answered/dispositioned rows close page residue"
  rule, up to 40 pages could re-status DOCUMENTED → enlarging the promotable
  pool. Routed as `OPUS-REQ-FABLE-STATUS-CURRENCY-RULE` (READY, unclaimed);
  sweep stays gated until the ruling + re-census.
- `9ad755589`, `d9595b0e8` — two more OPUS falsification pass-1s
  (render-command-list, text-control-codes); same pattern as S66's three;
  by-reading.
- `91d227586` FABLE resume checkpoint — by-reading.

## FABLE-REQ-AUDITSPEC-T6B-PUSHP-FRESH-READER — ACCEPT (the fifth case)

**Asked:** from the storage page's PUSHP row alone, predict the packed reference
word for `02FFFFFF`+1 and `02000000`−1; check against `arith_consumers.py` R;
record any page gap.

**Fresh-reader derivation (page only, before any control):**
§2.2 gives bits 0..23 offset, 24..26 class, 28..31 width. The PUSHP row says:
offset is masked to 24 bits, the scaled index is added by a plain unmasked
32-bit `add`, class bits are re-OR'd in (`and r9d,0x7000000`/`or r8d,r9d`), the
width nibble is forced to 7 (`or 0x70000000`), nothing masks before the store
(`00268194`), and `+0x44` keeps the original width.

- `02FFFFFF` +1: offset 0xFFFFFF + 1 = 0x1000000 carries into bit 24 →
  `|0x02000000|0x70000000` → **`0x73000000` — class 3, width 7** (the carry
  silently flips class 2 local → 3).
- `02000000` −1: 0 − 1 wraps to 0xFFFFFFFF → **`0xFFFFFFFF` — class 7,
  width 15**.

**Verified:** the PUSHP body re-decoded byte-exact — `268166 add r8d,edx`,
`268169 or r8d,r9d`, `26816C or r8d,0x70000000`, `268185` stores the original
width byte at `+0x44`, `268194` unmasked dword store of `r8d`. Control R's own
model outputs the same two words (`73000000` (3,7), `FFFFFFFF` (7,15)).

**Page gap: none for these cases** — the row (as qualified 2026-09-28) already
states the no-mask add *and* literally carries both worked answers. The one
nuance a reader could miss — that the +1 carry does not merely truncate but
*changes the class field* (2→3) — is stated ("packs as `73000000`, class 3").
No correction needed.

## Shadow batch S68 (landings through `d13779c8e`)

- **`1f11830e9` OPUS `prereq.py` repair — verified at source and behavior.**
  The fix makes `_failed(l)` read the verdict through the configured `line`
  regex's group(1), keeping the literal `FAIL `/`FAIL\t` prefixes as a floor —
  exactly the S66 divergence closed. Exercised the repaired helper myself: the
  ASTRA tab-FAIL counterexample now returns
  `exited 0 but printed FAIL lines: FAIL\tA\trequired failure` (refused), and
  the default-format PASS path still composes. Defect class closed at source;
  `OPUS-REQ-ASTRA-REVERIFY-A03-PREREQ` remains ASTRA's call.
- `df5fe8763` EXP-250 — `member-block-chain-exec/check.py` re-run at HEAD:
  **546/546 pass** (matches ORACLE's "stable x3").
- `622c0866d` MP-2 (FABLE's C1–C4 applied) — `test_requirements.py` MP1–MP12
  FAILS 0; MP11 exercises the `bin`/`dat` member-format gap → UNMEASURED and
  MP12 the Q split + F-excluded union; MP9's MP-0→MP-2 definition bump is
  honest versioning.
- `1157fb709` FABLE spawn-respawn P7 residue — by-reading (coordinator
  `003B8670` posts kind 6 when authored-event +4 is 1); DATA UQ-218 pass 10
  (`6a4bbbc37`/`d13779c8e`) — by-reading.


## S69 — OV-ACCEPTANCE-0929 six-section review (FRONTIER carrier)

```json
{
  "task": "FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929",
  "reviewer": "SWE2-AUDIT-SPEC",
  "method": "byte-exactness of all retained disassemblies vs certified image sha 73461d08; semantic re-read of load-bearing anchors; executed checks where host permits",
  "evidence_integrity": {
    "continuation-section09-owner-producer": "7341/7341 retained instructions byte-exact",
    "continuation-section10-nonempty-registration": "6738/6738 byte-exact",
    "continuation-section07-source-movement": "5665/5665 byte-exact",
    "continuation-section04-widget-receiver": "1081/1081 byte-exact"
  },
  "executed_checks": {
    "receiver_audit.py (s04)": "16/16 pass on Windows",
    "test_overlay.py (s07)": "pass on Windows",
    "test_overlay.py (s09,s10)": "BLOCKED WinError 1314 symlink privilege - host limitation, not a content failure",
    "run_review.py (all four)": "Linux x86-64 gated - UNMEASURED on this host; producer retained results assert Linux execution",
    "verify_overlay.py": "all six pages show CONFLICT vs frozen postimages - expected: FABLE's 2026-09-29 correction wave and OV-row dispositions landed after retention; conflicts are on the page bodies, not the evidence"
  },
  "anchors_verified": {
    "OV-23": "003DD7E0 init = 5 groups x 16 records x 0x1C at 02B581A0 (loop counters + stride byte-exact)",
    "OV-38": "003DDA20 arm: accepts only state0 (cmp [..+4],0; jne ret0), stores annotation +8, writes state2, sets 1<<i in mask at 02B58A60, returns 1",
    "OV-28": "003A75C9 test byte[rax+3],1 selects bulk 0x800-stride teardown vs individual arm releasing nonnull entries regardless; 0024F410 context unlink present",
    "OV-44": "004096C0 guards NULL/-1 then unguarded add eax,ebx + cdqe - valid mode sum can wrap to NULL; 003A9A70 specialized relocation mutates backing via call 005004C0",
    "OV-49": "0036A2A0 order: header store 0036A364 -> release call 0036A397 -> copy call 004746F0 0036A3A7 -> claim call 0036BC60 0036A3BB -> generation store 0036A461",
    "OV-32": "mov ecx,0xd8 + handler 00394070 vs mov ecx,0x1d0 + handler 003939B0 through allocator 0x244f50 - two distinct objects as claimed"
  },
  "reviews": {
    "OV-23 the-external-source-owner-and-borrowed-view-lifetime SECTION-09": "ACCEPT",
    "OV-28 the-resource-owner-from-copy-or-borrow-to-disposal SECTION-10": "ACCEPT",
    "OV-38 the-indexed-source-request-from-arm-to-terminal-pump SECTION-09": "ACCEPT",
    "OV-44 the-nonempty-prf-registration-and-specialized-relocation SECTION-10": "ACCEPT",
    "OV-49 the-source-block-mover-and-separate-consumer-refresh SECTION-07": "ACCEPT",
    "OV-32 the-title-asset-singleton-and-its-distinct-consumer SECTION-04": "ACCEPT"
  },
  "verdict": "ACCEPT",
  "limitations": [
    "native fixture replays (run_review.py) are Linux-gated and UNMEASURED on this host; acceptance rests on byte-exact retained bodies + semantic re-read + the Windows-runnable instrument checks",
    "acceptance covers the named sections' claims only; the pages remain PARTIAL with open OV obligations",
    "no live-game, real-IO, Windows-CRT, or whole-census claim is made or accepted"
  ]
}
```


## S70 — ASTRA 0929 evidence wave (30 packages, all checkers re-executed by this reviewer)

Method: every package `check.py`/probe re-executed from repo root or its own dir as required;
verdicts reproduced first-hand, not trusted from task prose. Native-anchor packages got direct
byte re-reads against the certified image (sha 73461d08). Package limits preserved verbatim;
NO package result was promoted to full migration/dashboard/database acceptance.

| task | package | reproduced result | disposition |
|---|---|---|---|
| TRANSITION-ADMISSION | migration-transitions-independent | REJECT_TRANSITION_ADMISSION_FULL_APPLY_INCOMPLETE | REJECTION VERIFIED: pinned pre-repair src c545ed76 checked truthiness/membership only (commit format, record path, reviewer!=author all unvalidated); current transitions.py carries the repair; valid ACCEPT lost to 20 s deadline, private incorporation cannot substitute the caller receipt |
| GENERATION-BOUNDARY | migration-generation-independent | REJECT_GENERATION_ARCHIVE_CERTIFICATION | REJECTION ACCEPTED |
| MY-PROGRESS | migration-my-progress-independent | REJECT_PROGRESS_TERMINAL_ADMISSION_BOUNDED_CONTROLS_COMPLETE | REJECTION ACCEPTED |
| GENERATION-CERT-R2 | migration-generation-cert-r2 | REJECT_UNRECOGNIZED_INPUT_STATE_SCOPED_REPAIRS_PRESERVED | REJECTION ACCEPTED (scoped repairs preserved) |
| TRANSITIONS-R2 | migration-transitions-r2 | ACCEPT_SCOPED_ADMISSION | ACCEPT scoped |
| ACTIVITY-ATTRIBUTION | migration-activity-deltas-independent | REJECT_ACTIVITY_WRITER_ATTRIBUTION | REJECTION ACCEPTED |
| FIXTURE-PRODUCER-GUARD | migration-fixture-placement | SCOPED_PRODUCER_GUARD_AND_READER_CORRECTION | ACCEPT scoped |
| GENERATION-CERT-R3 | migration-generation-cert-r3 | ACCEPT_SCOPED_UNKNOWN_STATE_REPAIR | ACCEPT scoped |
| MY-PROGRESS-R3 | migration-my-progress-r3 | ACCEPT_SCOPED_FIXED_TERMINAL_REQUIREMENT | ACCEPT scoped |
| POISON-Q6 | poison-q6-independent | SCOPED_Q6_SUPPORTED; NO_LIVE_OR_SINK_CLOSURE; OWN_ACCEPTANCE_PENDING | ACCEPT scoped |
| TRANSITION-LINE-BOUNDARY | transition-line-boundary | REJECT_EXACT_FIELD_ADMISSION; TRAILING_LF_ACCEPTED; PRIOR_NAMED_CASES_RETAINED | REJECTION ACCEPTED (exact-field), trailing-LF accepted |
| TRANSITION-WRITER-STATUS | transition-writer-status | REJECT_REQUIRED_WRITER_NONZERO_SWALLOWED; SUBSTITUTED_CHILD_SCOPE_ONLY | REJECTION ACCEPTED |
| DASHBOARD-SHELL | dashboard-shell-reconciliation | ACCEPT_SCOPED_SELECTED_VIEW_HTTP; RETAIN_RENDERING_AND_DEPLOYMENT_GAPS | ACCEPT scoped |
| ACTIVITY-ATTRIBUTION-R2 | activity-attribution-r2 | ACCEPT_SCOPED_WRITER_ATTRIBUTION_REPAIR; SYNTHETIC_CLASSIFICATION_ONLY | ACCEPT scoped |
| DELTA-BASELINE | delta-baseline-selection | REJECT_SAME_PRIOR_AT_VERIFIED_MISSING_VIEW_BOUNDARY | REJECTION ACCEPTED |
| TRANSITIONS-R3 | migration-transitions-r3 | ACCEPT_SCOPED_EXACT_FIELDS_AND_CALLER_STATUS_R3; NO_REAL_WRITER_PARITY | ACCEPT scoped |
| BOARD-STALE-REVISION | board-stale-revision-writer | full_A13 NOT_ACCEPTED (healthy-prefix/changed-checkpoint controls accepted) | ACCEPT scoped |
| PENDING-STATE-BINDING | board-pending-state-binding | healthy_prefix accepted and healed | ACCEPT scoped |
| DELTA-ONE-BASIS-R2 | delta-one-basis-r2 | ACCEPT scoped to exact 17d6 selectors/change-expr/annotator | ACCEPT scoped |
| RENDERED-NAVIGATION | dashboard-rendered-navigation | navigation Progress->Overview->Activity observed; 2 refused inputs; owned tab cleaned | ACCEPT scoped |
| TEXT-OVERLAP | text-overlap-boundary | REJECT scoped unique-overlap measure at exact original source | REJECTION ACCEPTED |
| TRANSITION-ACTUAL-WRITE | transition-actual-write | ACCEPT scoped real transition/writer integration; no A14/A16 | ACCEPT scoped |
| UC1-DEPENDENCY-BINDING | uc1-dependency-binding | SCOPED_DEPENDENCY_BINDING_GAP | ACCEPT scoped (gap is the honest result) |
| TYPED-POP-REPORT-BOUNDARY | EXP-013-vm-pop-boundaries | OBSERVED_MATCHING_BOUNDARIES 14 cases | ACCEPT scoped (model-observed only) |
| HEADING-ALIAS-EXTENT | heading-passthrough-alias-boundary | first-40B leaf/no-calls basis REFUTED (catalog 963B; 21 full-body call sites); consumer change prescribed | REJECTION OF BASIS ACCEPTED; owner must re-prove or narrow |
| OVERLAP-HELPER-REVIEW | overlap-helper-repair-review | ACCEPT scoped overlap/helper repair; bound/missing-begin refuse | ACCEPT scoped |
| DASHBOARD-RENDERED-RETURN | dashboard-rendered-return | one return, STALE->PARTIAL during setup, tab3 cleaned; limits honest | ACCEPT scoped |
| HEADING-EXTENT-REVIEW | heading-extent-repair-review | ACCEPT scoped semantic repair; CLI exit-0-on-BROKEN gap retained for OPUS | ACCEPT scoped + retained producer gap |
| HEADING-STATUS-REPAIR | heading-status-repair-review | ACCEPT scoped 2366027d9 H8 CLI/gated-count repair | ACCEPT scoped |
| HEADING-CLASS-EFFECTS-SLICE | heading-class-effects-slice | STATIC_EFFECT_BOUNDARIES_VALID_NOT_CLASS_CLOSURE; class_stability OPEN | ACCEPT scoped; class stability stays OPEN |
| SPAWN-PENDING-LATCH (earlier claim) | spawn-pending-latch | checks pass; 00332130 `and ebx,0xFFFFFFFE` + store + test-of-remaining-bits byte-verified; 0032F6F0 rejected-lead retained | ACCEPT scoped |

Wave-level note: all REJECT dispositions mean the ASTRA rejection stands under independent
re-execution — the failed campaigns/controls are preserved immutably per policy; no unchanged
retry was run or endorsed.


## S71 — heading-source-consumers review + 0929 shadow batch

**ASTRA-REQ-SPEC-HEADING-SOURCE-CONSUMERS — ACCEPT scoped (STATIC_ONLY).**
Independently byte-verified all load-bearing anchors against the certified image:
- arg5=0 chain: `002E4735 xor ebx,ebx` -> `002E474D mov [rsp+0x20],ebx` -> callee
  `0026B014 cmp dword [rsp+0x80],0` (caller +0x20 arg slot = callee +0x80 stack arg).
  Predicate `002E4739 je 0x2E4756` skips the call at `002E4751` — verified.
- Reader steps (adjacent body after each setter):
  `529D50` cmp/mov `[rbx+0x3d4],r13d` (compare/write);
  `52A8B0` cmp `[rbx+0x434],0` + mov `=0` (compare/zero);
  `52B5E0` cmp `[rbx+0x3f8],0` + je + `call 0052BBD0` (compare/gated call);
  `45FD10` (56 B) zero direct +0x3D8 operands, calls 0x2F2530/0x4607C0 — bounded rejection.
- RCX->RBX provenance (`mov rbx,rcx`) verified at each step entry; continuity rests on
  nonvolatile-ABI — stated, not overstated. hit counts [0,2,2,1] reproduced.
- Limits honest: sqrtf = static IAT decl not observed module; class stability OPEN.

**Shadow landings:**
- `147ebaa6d` OPUS consume of the four commit tails into CONTRACT-heading-speed-to-position-
  delta: faithful — records only the two-instruction stores, keeps flag meanings/readers/
  lifetime/class-stability OPEN, strikes only the consumed part of the open item.
- `6c43f86d5` apply_pass.py damage repair — VERIFIED at source and output: lighting page
  diff vs c59ee3ed0^ is stamp+pass-section only (+24, no body loss); external_production key
  restored on CONTRACT-resource-section-addressing (lines 27-30); stamper now uses an
  EOL-tolerant fence regex, preserves post-audit frontmatter keys, and guards whole-body
  survival — both defect classes closed at source.
- falsify_character_lighting G0-G5 FAILS 0; falsify_staged_look L4-L6, falsify_rig_controllers
  R3-R5, falsify_bone_trails B2-B4, falsify_presentation_track T7-T9, falsify_fade_channels
  C3-C5, falsify_status_look H4-H6, falsify_effect_element E13-E15 — all FAILS 0.
  E13/E15 productively REFUTE earlier claims (48 call sites on 0044B960 => shared helper;
  release labels corrected to 002F31C0) — falsification working as intended.


## S72 — promotion sweep: FIRST REAL PROMOTIONS (commit 9828cd746)

Post-ruling census re-run: 435 docs, 402 passes, 73 cond7+8 eligible
(up from 58 — the OPUS falsification wave added candidates).

Partition of the 73: 55 already-AUDITED + 12 PARTIAL + 2 REOPENED + 4 DOCUMENTED.
Of the 4 DOCUMENTED: two are `_experiments/*/retained/` snapshots (never promotable —
live counterparts carry 10/20 crossref findings), and **two are live pages**:

- `17-Presentation-Rendering/Character-Render-Records/the-staged-look-command.md`
  falsify_staged_look.py re-executed FAILS 0 (L0-L6 all survive, "No correction");
  5 classified neighbour edges (SHARED RECORD/SERVICE/INCIDENTAL); 0 open boxes;
  FABLE-authored + OPUS-falsified -> reviewer rule holds.
- `17-Presentation-Rendering/Effect-File-Formats/an-effect-element-frame-by-frame.md`
  falsify_effect_element.py re-executed FAILS 0; E10-E13/E15 refuted BUT corrected
  in place with strike+attribution (verified: ~~four~~->five steps at :225,
  002F31C0 named release, 0044B960 reclassified shared-helper 48-sites);
  2 classified neighbour edges; 0 open boxes; no standing killer.

Both flipped DOCUMENTED -> AUDITED in commit `9828cd746` (status + audit.note
receipt + crossref_clean/reopened_count; last_reviewed already 2026-09-29).
Audit.note "pending first review" replaced by the promotion receipt.

Post-promotion residue: zero promotable live DOCUMENTED pages. Remaining blockers:
12 PARTIAL (own residue), 2 REOPENED, 2 frozen snapshots. Sweep stays ACTIVE-gated
on future re-statuses (status-currency ruling consumption may lift PARTIALs).
Board checkpoint recorded at rev 40250.


## S73 — shadow: OV apply batch + three falsification landings

- `e222ec17d` FRONTIER OV apply: nine register rows + five box ticks + the Q2
  `+0x17C` rename. Verified consistent with my OV-acceptance review — the three
  indexed-request boxes (OV-34/35/36) ticked with FABLE-record attributions;
  consumer-check record documents row-for-row agreement; OV-42 applied at the
  corrected owner-protocol scope only. Independently ran check_questions.py:
  0 box/table mismatches, 0 cell-count drift — the claimed regression reproduces.
  The +0x17C-as-effect-slot-timers correction cross-confirms the poison-package
  reading (stage 3 owns +0x17C; stage 2 owns the 32 statuses' +0xBC/+0x13C).
- `e36c9bf0e` falsify_pose_sequencer Q7-Q10 FAILS 0 (Q10's note honestly flags
  the omitted +0x24 x [01DFE0BC] time factor).
- `ee21b57cb` falsify_ftr_node_table N7-N10 FAILS 0 — N8/N10 productively REFUTE
  (kind!=2 path corrected; "71 functions stride 0x290" narrowed to 55 imul users,
  16 others use 0x290 otherwise).
- `56feea579` falsify_vfx_layers V9-V12 FAILS 0 — four productive refutations
  (zeroed-table addressing, emitter selection, call-site scoping, reload timing).
- `9d3e3aeac` DATA UQ-218 pass 16 + `b9ae7828d` AUDIT-SEM wave-2 verdicts — by-reading.


## S74 — heading-node-followup + A23-current-release reviews

**ASTRA-REQ-SPEC-HEADING-NODE-FOLLOWUP (ce6fccd87) — ACCEPT scoped STATIC_ONLY.**
check.py reproduced: STATIC_ONLY_CONDITIONAL_SOURCE. All four native anchors
byte-verified on the certified image:
- `00460ACA`: `cmp dword [rbx+0x3d8], r12d; je` — the type-67 read against
  zeroed R12D with the clear on the unequal arm.
- `0052BBF7`: `mov dword [rcx+0x3f8], ebx` where `xor ebx,ebx` sits two
  instructions earlier at `0052BBF5` inside 0052BBD0's prologue — a genuine
  clear BEFORE the first nested call (no intervening call between xor and store).
- `0052BF21..4C`: `mov ebx,0x20` + `lea rcx,[rdi+0x280]` + `lea r8d,[r9+1]`
  (r8d=1, r9d=0) + `call 0054B1F0` + `sub rbx,1/jne` — the 0x20 installer loop
  with node+0x280 base exactly as claimed.
- `002F2530` 2094-byte extent scanned: zero disp32 accesses to +0x3D8 —
  the bounded negative verified (correctly not claimed image-wide).

**ASTRA-REQ-SPEC-A23-CURRENT-RELEASE-EVIDENCE (f85ed4623) — ACCEPT scoped.**
check.py reproduced: A23_EVIDENCE_SLICE_VALID_NOT_ACCEPTED. Inspected
capture.json + raw-http/ five retained bodies: actual deployed HTTP GETs at
127.0.0.1:8765 on stable generation g20260929T184345Z-92fe9f with before/after
generation equality (no mutation), reader_not_stale, source-identity naming
checkout files only, and a real verify-zip success on the OLDER
g20260929T075521Z-fbf2f8 (explicitly not binding to the served generation).
No overstatement found — the package itself concludes A23 INCOMPLETE/NOT_ACCEPTED
with the named FRONTIER ask for release/export/identity/adoption evidence.


## S75 — shadow: three more falsification landings

- `3790fc504` falsify_fte_fct X5-X8 FAILS 0 — X5 refutes the count source
  (multiplier is the target's +0xB9 byte loaded at 0053AB9F, not "count").
- `e89f8f0e3` falsify_cutin_blur_softfocus Z8-Z11 FAILS 0 — Z10 refutes the
  sweep bound (zero key -> early ret, ends at first empty of 36); Z11 refutes
  the arg order (rcx=00186AA0 width-first, rdx=00186A90 — note was reversed).
- `0bb5c75d5` falsify_fdm_for M5-M8 FAILS 0 (all survive).
- `098204632` DATA pass-16 resume hash — by-reading.


## S76 — shadow: three falsification landings

- `b731f0162` falsify_battle_party_verbs B4-B7 FAILS 0 (B7 precision note:
  setbattlemember raises the flag before its first pop).
- `b7d92a38b` falsify_event_slot_panel S3-S6 FAILS 0 — S5 refutes
  (cmova bounds to 4, not min(slot,4)); S6 refutes "three sites"
  (counter read at four sites).
- `612e3e5a7` falsify_camera_renderer W9-W12 FAILS 0 — W11 refutes
  (01A2 handler pushes nothing, pops the draw; no upper bound);
  W12 refutes the label (00229D20 asks the device object = aspect).
- `e45bbb909` DATA UQ-218 pass 17 — by-reading.


## S77 — shadow: team.py binding fix + OV 0929c + anim-move-turn

- `57274cbd0` team.py pending-intent binding — the fix for the
  board-pending-state-binding defect I reviewed in the S70 wave.
  Verified at source: transaction() now binds the post-apply board
  sha into the intent record; the pending branch heals only when the
  on-disk file matches the intended write (else BoardIncident, fail
  closed); pre-binding intents heal as bound=received-legacy —
  explicit, never silent. Retire guard also hardened: requires
  unclaimed AND request-shape (requester/question), closing both the
  peer-BLOCKED-retire and plain-research-row gaps test_j has asserted
  since 03a785a39. Combined suite re-run: rollback 42 + team 13 =
  55/55 green on this host.
- `0045a28fa` FRONTIER OV apply 0929c — bundle-B rows+boxes, OV-42/33/
  19/26 residue refinements, exp-curve fix (12k^2, level 2 = 51).
  Independently re-ran check_questions.py: 0 mismatches, 0 cell-count
  drift, table/checklists agree (1648 rows, 1461/1471 boxes ticked).
- `3485ca1a6` falsify_anim_move_turn A0-A6 FAILS 0 — A6 productively
  refutes "either switch": the take 003AED70 tests only 02B3F53C
  (with list +0x28/+0); 02B3F540 gates the consumer 003AEF90.


## S78 — shadow: A17 VBF archive-index discriminator

- `7b73151a5` ASTRA A17-VBF-ARCHIVE-INDEX — re-ran
  `a17-vbf-archive-index-check.py` first-hand against the installed
  `FFXII_TZA.vbf` (31,196,932,183 B, Sep-8 mtime) and the dashboard's
  retained `vbf_list.txt` (Sep-2, sha f38f5796...): INDEX_MATCH —
  89,414 entries, 0 missing-from-archive, 0 missing-from-listing,
  0 size mismatches, 58,894,815,547 uncompressed bytes; the SRYK
  parser's bounds/UTF-8/terminator/duplicate controls and both
  same-count mutation controls all fire. Scope honestly bounded:
  verifies the index population for THIS installed archive (the
  cited 9dd38f89 whole-file sha belongs to a different test-client
  path and is not equated); no payload hash, decompression, or
  resource binding; A17 stays not-accepted and the dashboard PARTIAL.
  Confirms the Sep-2 listing still describes the Sep-8 archive's
  name/size table — a genuine staleness check, not an assumption.


## S79 — shadow: ASTRA My Progress independent check

- `d4f0eaa8f` MY-PROGRESS-INDEPENDENT-REVIEW — verified three ways:
  (1) non-author re-execution: MP1-MP13 PASS / FAILS 0 on files I
  sha-verified byte-identical to the doc's citations (requirements
  02cd6ce8..., test 507f48f7...); (2) retained live evidence
  consistent: root.html.gz decompresses to 20,446 B and contains
  the real minified `let cur="progress"` form — the invalid first
  selector's failure mechanism is genuine and the invalid run is
  preserved separately; (3) live result record: one generation
  g20260929T200945Z-fd7195, all 25 named checks true. Verdict held
  at bounded scope — checkout SHAs named as checkout identity not
  loaded-module proof; view stays PARTIAL, coverage UNMEASURED,
  goal NOT_MET, terminal 0/30. The scoped ACCEPT does not overreach.
- `182b158b7` ASTRA checkpoint (A17 + My Progress scoped evidence)
  — inbox bookkeeping, by-reading.
