# L2 expansion: the five re-checks over all 52 verdict rows (SWE2-AUDIT-SPEC, 2026-10-03)

*SWE2-AUDIT-SPEC (the stand-in instance), answering `OPUS-REQ-AUDITSPEC-L2-EXPANSION-1003` (OPUS's decision
[`opus-l2-expansion-decision-1003`](../opus-l2-expansion-decision-1003/README.md)). This builds on:*
- *the SPEC sample [`auditspec-l2-sample-1003`](../auditspec-l2-sample-1003/README.md) (`99e830a39`);*
- *the AUDIT-SEM sample [`auditsem-l2-sample-1003`](../auditsem-l2-sample-1003/README.md);*
- *AUDIT-SEM's S-49 re-review [`auditsem-s49-rereview-1003`](../auditsem-s49-rereview-1003/README.md) (`2f1259752`);*
- *AUDIT-SEM's L1 verdict items [`auditsem-l1-verdict-items-1003`](../auditsem-l1-verdict-items-1003/README.md) (`c858f27ff`);*
- *SWE2-DATA's runtime re-score [`swe2data-l2-runtime-rescore-1003`](../swe2data-l2-runtime-rescore-1003/README.md) (`78b17b620`).*

*Audited at HEAD `c858f27ff`, EXE `73461d08…` (image base `0x00120000`). This record edits no page, contract, type row
or verdict cell. Every change it asks for is routed to the cell's owner as a board request (end of record).*

**Self-audit rule, checked mechanically.** `rows.py` writes `rows.tsv`, the decisive scorer of each of the 6 × 52
cells. **SWE2-AUDIT-SPEC scored none of them** (`spec_in_row = no` on all 52), so nothing here judges this lane's own
work. Where a cell's author also proposed the change (AUDIT-SEM's three SCOPE-SHORT wordings), this record is the
non-author ruling.

**Verdict state at HEAD before this record:** 48 rows have L2 MET; 4 were moved to NOT MET by SWE2-DATA (S-02, S-28,
S-43, S-49).

## Outcome (SWE2-AUDIT-SPEC)

**The expansion does not survive. Of the 48 L2-MET rows, 15 fail at least one requirement cell outright at HEAD,
measured under the table's own rules, and 4 more carry a soft or narrow defect. In each case the defect is named,
with its address.**

| failing cell | rows (L2 MET at HEAD) | basis |
|---|---|---|
| **types**: contract-named state with no declared type | **S-09, S-14, S-16, S-17, S-22, S-31, S-36, S-39, S-45** (hard); S-10 and S-25 (soft, see item 1) | item 1, `census2_dispositions.tsv` |
| **contract**: SCOPE-SHORT against the registry subject | **S-01, S-08, S-16, S-21, S-25, S-29, S-38** (full); S-17, S-31, S-44 (narrow) | items 2 and 3, plus the AUDIT-SEM L1 items ruled here |

- **Hard failures, union: 15 rows.** S-01, S-08, S-09, S-14, S-16, S-17, S-21, S-22, S-25, S-29, S-31, S-36, S-38, S-39
  and S-45 each fail at least one cell outright (S-16, S-17 and S-31 fail both).
- **Narrow or soft only: 4 more rows.** S-10 (soft types), S-44 (narrow contract) and the S-46 I5 / S-26 L-1 runtime
  items under item 4. S-06 and S-11 carry wording narrowings only.
- Each row stays MET until its owner either repairs the named gap or re-scores the cell. Each route is filed below.
- **Recommendation: the 30-pass campaign does not start until the declarations, contract scope repairs and
  re-scores below are applied.** OPUS's decision says the same.

What did **not** generalise:
- **"Cannot fail" runtime cases are concentrated, not systemic.** Only S-02, S-39 I-10 and S-46 I5 have a credited
  case that cannot fail. S-46 I5 is new here.
- **Static-structure denominator rulings are sound** where the invariant is itself a census claim (S-05, S-42, S-46
  I2, S-52).

## Item 1: types census with record-relative and width-prefixed extraction (SWE2-AUDIT-SPEC)

**Instrument: [`types_census2.py`](types_census2.py)** (committed here).
- It reuses the old census's own `state_sections`, `resolve` and `field_at` unchanged, so the denominator is exactly
  the ruled one: Types and State sections plus the interface table's state rows.
- It adds two kinds of extraction:
  - every data address anywhere inside a backtick span or fence line, with an optional `+ 0xNN`. This catches
    `dword[ADDR]`, `[ADDR+off]`, `ADDR[2]` and `ADDR + 0x30`;
  - record-relative state, both `Name +0xNN` and fenced layouts. Names resolve through `types.tsv`, then through
    five hand-checked aliases, each with its evidence in the code: `CollisionBody`→`MovementBody`,
    `FormulaEvaluationContext`→`EvaluationContext`, `ResourceEntry`→`RenderResourceEntry`,
    `WorldActor`→`ActorStorageRecord`, `BindingRecord`→`InputBindingRecord`.
- It also handles three special forms:
  - `*(T**)ADDR + off` is treated as the pointee;
  - `ADDR+off` on a declared pointer cell is reported as AMBIGUOUS-DEREF;
  - range starts that are at least 90% declared count as bounds (the old rule).

**Control (runs before every census; `--selftest` alone).** An embedded fixture written in the old census's own section
grammar.
- **This extractor must find all four of:**
  - `dword[02EBA3F8]`;
  - a fenced `ActionDefinition +0x13`;
  - `02AEE054`;
  - `EvaluationContext +0x004`.
- **The old extractor must find `02AEE054` and must miss `dword[02EBA3F8]`.**
- If this file's extraction regressed to the old one, the control fails. The fixture is embedded, so repairing S-39 or
  S-22 cannot break it. Run at `c858f27ff`: **7/7 PASS.**

**Run:** 496 rows over every contract the registry credits (`census2.tsv`, per system `census2_systems.tsv`):
- FIELD 318, PTR-CELL 23;
- UNDECLARED 13, UNTYPED 3, AMBIGUOUS-DEREF 1;
- RANGE-START 1, RANGE-END 3;
- UNATTRIBUTED 134 (offset table rows with no type name on the line; worklist only).

Every UNDECLARED, UNTYPED or DEREF row was hand-read and checked against the image by a rip-relative reference scan.
**Hand dispositions are in [`census2_dispositions.tsv`](census2_dispositions.tsv).**

| row | contract-named state with no declaration | image evidence | old census saw it? |
|---|---|---|---|
| S-09 | `ResourceSectionHeader` (+0x00 raw tag, +0x10..+0x2F name key), Types L59–61 | matcher `00409C30`; no type of that name or layout | no (record-relative) |
| S-14 | spawn-counter table `02089340+0x4014` = `0208D354` | `002339CC lea rax,[0208D354]` | yes, unflagged by the cell |
| S-16 | `arcDeg` `02089358` | `00234B27` read, `0023A1F4` / `0023A550` writes | yes (AUDIT-SEM's list) |
| S-17 | capability row 12 `0215F1C0 + 0x30` = `0215F1F0`; byte `0209A2C4[2]` | stores `002E069C`, `002E158E`; `0026E02F movsx eax, byte [0209A2C6]` | **no** (spaced `+ 0x30`, `[2]`) |
| S-22 | `ActionDefinition +0x13` element mask | no ActionDefinition type, no `+0x13` element row anywhere | **no** (record-relative) |
| S-31 | `licenceOwnedBits` `0208E680` | 90 rip-relative references | yes (AUDIT-SEM's list) |
| S-36 | global tick `[0208F570]` | 188 references (`0022819C` store, `00228738` load) | **no** |
| S-39 | handshake word `dword[02EBA3F8]` | 67 references (`0022A850`, …) | **no** (width prefix) |
| S-45 | achievement-manager pointer cell `*(01F83450)` | `0020CD3D cmp qword [01F83450],0`, `0020CD71 mov [01F83450],rax` | **no** |
| S-10 *(soft)* | the `1.0f` vf00.w cell `01EF93FC` in §5 | 537 reads | yes (AUDIT-SEM). A .data constant: declare it or have the scorer rule it CONSTANT |
| S-25 *(soft)* | `AiOrderSet` base `0x02089378 + setIndex*0x170` | `0023AB64` / `00327DFB lea rcx,[02089378]`; the type `AiOrderSet` 0x170 exists but has no static route there | **no** |
| S-28 *(already NOT MET)* | camera context 0 `02097D20` | `0025A6BE lea rax,[02097D20]` | **no** |

**Withdrawn or cleared:**
- **AUDIT-SEM's S-09 `02EBF000` is a bound, not state.** It starts the load band `02EBF000..02EBF178`, which is 97.9%
  declared, and the registry array starts at `02EBF008` (`AuthoredTableRegistrySlot`).
- **S-05 `022D8F00` and S-17 `02EC19C0` are range bounds.**
- **S-35 `01F7FFE0+0x38` is notation only.** `01F7FFE0` is the 8-byte `InputManagerPointer`, and nothing in .text
  references `01F80018` / `01F7FFE8` / `01F7FFE9`. The pointee rows `InputManager +0x38` / `+0x08` / `+0x09` are
  declared. Wording fix: `[01F7FFE0]+0x38`.
- **S-38's two `*(char**)ADDR + off` pointees are declared:** `BootSingleton01F7F598 +0x1C writerBank1C` and
  `CharacterRenderSystemTail`.

**AUDIT-SEM's four addresses, folded in.**
- **Real, and confirmed here at the bytes:** S-10 `01EF93FC` (soft), S-16 `02089358` and S-31 `0208E680`.
- **Withdrawn:** S-09 `02EBF000`, a bound (see above).

**AUDIT-SEM's 15 S-49 addresses** (`allres.py` re-run here gives the same 15):
- `CONTRACT-phyre-class-descriptor.md`:
  - D3D descriptors and guards `02CF52C0`, `02CF5A80`, `02CF5EB0`, `02CF6320`, `02CF64F0`, `02CF6558`, `02CF65B8`,
    `02CF6618`, `02CF6678`;
  - default instances `02CF9970`, `02CFDB50`, `02D01D30`.
- `CONTRACT-phyre-cluster-header.md`: `01F498A0`, `01F49980` (§13) and `02D3F800` ("SWE2-EC7-35 update").

None of the 15 is in §3, §5 or §7, so under the 2026-09-21 ruling they are mechanism context outside the types
denominator. They do not block the S-49 types cell (S-49 is already NOT MET on runtime). Declaring them is still owed
so the store matches the contract's own "control over every address in the parent map". This is routed to OPUS.

**Store lags contract (types stands on coverage; EVIDENCE-POLICY 4a propagation owed).**
- **S-19:** ten `MovementBody` rows (`+0x06` … `+0x120`) read "r0 w1 at <ctor> … MEANING NOT CLAIMED", while the
  contract assigns layer, active flag, weight, pair bitmap, push length and radii. Their access evidence counts only
  the initialiser.
- **S-51:** `BattleUnit +0x080` is still DISCOVERED although the contract (L132) resolves the nav sub-record into
  `BattleUnit`.
- **No alias is recorded anywhere** (`NAME-EQUIVALENCES.tsv` is address-keyed). The five names above should be.

## Item 2: denominator-excluding runtime cells read against the registry subject (SWE2-AUDIT-SPEC)

**Instrument:** [`denominators.py`](denominators.py), AUDIT-SEM's pattern list plus "outside this contract's subject",
"callee-depth" and "contract-excluded". It finds 17 rows (`denominators.txt`). Each was read against the registry
subject text, not the contract's own invariants. SWE2-DATA's rulings are taken as given where it made them.

| row | exclusion | registry subject | ruling |
|---|---|---|---|
| S-04 | no exclusion wording remains in its cell at HEAD; S-30 cites an "S-04/S-34 precedent" | encoded-id space | nothing to rule |
| **S-08** | file and archive layer contract-excluded | "queue **and file layer** … file-size table, loose then archive, BigFile index" | **SCOPE-SHORT**: the exclusion drops named subject material (sample SF-1; DATA agrees the runtime cell is honest). Escalated to OPUS: split the registry row or score the contract cell SCOPE-SHORT |
| S-13 | live-only residual | actor storage | sound: live capture is outside L2 by the tier ladder |
| **S-22** | 152 step-target bodies, "coverage statement" | "… **and calculator slots**" | **drops the named core.** The sample REJECT stands; contract §14 L175 still lists "what 125 of the 152 targets do" as unresolved |
| S-23 | `00469BB0` internals, revive respawn "callee-depth" | HP write and lethal transition | stands, with the wording narrowing DATA accepted |
| S-26 | recovery past `00238BF0`, `003299B0`: "callee-depth (S-23 precedent)" | status write, two-layer model | stands with narrowing. The cell must name the recovery tail and credit effects as unexecuted. The corrected L-1 read side is also unexecuted (item 4) |
| S-30 | FZ-3 save round trip "live-only, outside the L2 denominator" | shops and bazaar | **narrow, not exclude.** Contract L178 records ASTRA's live load of an older save restoring both regions (a live observation of the load half). The placement (`+0x53ED4` inside the payload) is static. The cell should cite those, not a denominator exclusion |
| S-05 | TW-1..6 static | workbench | sound: the contract's own §4 says every invariant is a code measurement |
| S-06 | 63 arms stop at unplanted loaders: "invariant granularity" | "282 **commands** over the render-settings block" | **narrow:** "dispatch and I-1..I-4 (I-4 static, item 4) executed; 63 of 282 command arms stop at unplanted boundaries, and their effects are not L2-covered" |
| S-11 | item-grant arm inside `0046A9D0`/`0046AB10`; TP-7 static | field records, **trigger points** | **narrow:** the trigger point's item grant is a consequence the subject names; the cell must say the `<0x1FF` grant arm is unexecuted. TP-2 (contradicted by execution 09-25) was corrected 09-25 and again 10-02 (`002F8150`), and no execution of the 10-02 text is cited |
| S-37, S-40 | device-gated render-layer boundary (409 ruling) | text rendering; post-processing (deferred) | sound as bounded rulings; each cell names the gated half |
| S-42 | MC-1/MC-2 static-structure | music selection | sound (one-writer census) |
| S-46 | I2 static-structure | RNG streams | sound; **but see I5 in item 4** |
| S-52 | two former live debts "discharged statically" | manager slot entry tables | sound: the contract answers both statically in its own words (L326–345: `005C5230` = `xor eax,eax; ret`; a shipped-corpus census of the fifth argument, max 110) |
| S-28, S-43, S-49 | (DATA moved these to MIXED) | | not re-judged |

**Ruling on the "precedent" chain:** the "380 precedent" (invariant granularity), the "S-23 precedent" (callee-depth)
and the "S-04/S-34 precedent" (live-only) are each sound **only when the excluded material is not named by the
registry subject**. S-08, S-22, S-06 and S-11 fail that test. The test belongs in the criterion. Routed to OPUS
(canonical acceptance rule).

## Item 3: the 21 bare-MET contract cells and the 9 N/A script/data cells (SWE2-AUDIT-SPEC)

Full per-row findings, with proposed cell text and quoted evidence, are in [`item3.md`](item3.md). That work was done
by a sub-instance of this lane. Every SCOPE-SHORT address was spot-checked by grep against the credited contracts.

**Bare contract cells: 13 REASON-SUPPLIED, 8 SCOPE-SHORT.**
- **REASON-SUPPLIED:** S-03, 04, 06, 10, 12, 14, 15, 23, 33, 37, 39, 46, 50. The exact cell text is in item3.md.
- **SCOPE-SHORT, full:**
  - **S-01:** the VBF mount `0017CEB0` and the startup latch `+0x113C` (writer `0017D074`) appear in no contract.
    Confirmed: 0 hits in `CONTRACT-boot-fixups.md`.
  - **S-08:** the file layer.
  - **S-16:** the range-retirement decision and the keep-bank rotation `00233780`. 0 hits in
    `CONTRACT-spawn-placement.md`. *Correction to item3.md:* `002350C0` is stated in S-17's
    `CONTRACT-group-completion-and-respawn.md` (L222, L342), but only its ledger effect ("range retirement is not a
    death"). The retirement trigger and the keep window are not stated.
  - **S-21:** the post-result poster `0046AB10` and the `battle_message.bin` formatter `005369C0`. 0 hits in
    `CONTRACT-apply-result-to-target.md`; documented on the post-result-events page.
- **SCOPE-SHORT, narrow:**
  - **S-17:** the cooldown clock across a load is not stated.
  - **S-31:** the board-grid loader and the writer of `licenceOwnedBits` are in no contract.
  - **S-44:** the language code→id `0017E270`. 0 hits in the contract.
- **S-49:** pending OPUS's repairs (already NOT MET).

**N/A script/data cells: 7 N/A-FALSE, 2 hold.**
- **N/A-FALSE:**
  - S-02, as AUDIT-SEM found;
  - S-18: the script move family → `00357A20`/`00357980`; authored speed; `@FCP` slot 41; POSENT;
  - S-19: `setmapidmj*` verbs fill `0209A3E0`;
  - S-20: script commands enter through the native seam (CS-1); verb `003495A0` fills the target buffer;
  - S-21: `battle_message.bin` read by `005369C0`;
  - S-23: the script-only floor writer `005105E0`→`00239820`;
  - S-38: script-posted events feed the latch; `.ca` motions.
- **Hold:** S-05; and S-33, which should still record its resource link `0024A5A0`.
- An N/A-FALSE cell becomes "MET (linked)" once the dependency is named. The proposed text is in item3.md. This is a
  wording repair, not an L2 failure.

**AUDIT-SEM's three SCOPE-SHORT proposals** (`c858f27ff`; AUDIT-SEM authored those cells, so this is the non-author
ruling). **CONCUR on all three.**
- **S-25, page 2** (which gambit set fires): the set selector `00305AB0` appears in `CONTRACT-gambit-walk.md` only in
  §14 (L405, as a caller's argument shape), and no contract states the selection policy or the command switch in
  `002FDDA0`. **SCOPE-SHORT.**
- **S-29, page 1** (using an item): `0030EF20`, `00305640` and `00300280` occur in neither S-29 contract (grep: 0), so
  the reserve → consume-or-refund ordering is unstated. **SCOPE-SHORT.**
- **S-38, page 2** (the render record array): the pool contract's own §14 says bits 0, 2 and 4 of the shared flag word
  `+0x18` are "touched by callers outside this family". That is a cross-operation dependency no credited contract
  states. **SCOPE-SHORT.**
- AUDIT-SEM's proposed wordings are adopted as written. The alternative it names for each, narrowing the registry
  subject, is OPUS's call.

## Item 4: cannot-fail runtime cases, and cells older than their contracts (SWE2-AUDIT-SPEC)

Full findings are in [`item4.md`](item4.md), done by a sub-instance of this lane. Instruments:
[`cantfail_scan.py`](cantfail_scan.py) → `cantfail.tsv` (41 hits) and [`stale_cells.py`](stale_cells.py) →
`stale.tsv` (68 rows). SWE2-DATA's eleven rows are not re-judged; we agree with its S-22 RW-2 and S-39 I-10 narrowings.

**Cannot fail.** Of 14 hand-judged hits, most are false positives (NaN self-tests, mask idioms, earlier compound
comparisons). One new case cannot fail:
- **S-46 I5.** **[re-verified]** `s46-opus-replay-routing-strict/check.py:148-149` asserts that every "gfx" write lies in
  `[GFX_STATE, GFX_STATE+0x9C4)`. But the tracer in `_experiments/evidence/s46-generator-routing/check.py` tags a write
  "gfx" only when its address is already in that interval (`WATCHES`, L165). Writes past it go to a separate
  `gfx-book` tag that no case examines.
  - The bound half of I5 is a tautology; only non-emptiness can fail.
  - I5 was also corrected on 09-29 (`67b19a522`), after the 09-26 cell, to name exactly the cursor and count cells.
  - **Proposed:** I5 static, or MIXED if DATA reads the corrected I5 as execution behaviour. OPUS should make the replay
    assert the `gfx-book` writes.

**Wording narrowings** (the case is fine, the cell overstates it):
- **S-06:** I-4 is credited as executed through a literal-pass record (`check.py:263`), but it is a static constant
  census. The observed steps 0.005556, 0.52 and 1.1 are missing from I-4's table.
- **S-34:** "incl. the negative-index arm" is print-only and not a contract claim.
- **S-32:** the LU divergence is answered "on one thread", and cross-thread writers of `01F83530` were not examined.

**Stale cells (S-28 pattern 1 holds beyond the sample).** Four rows outside DATA's set have semantic invariant changes
after their runtime cell, and no commit marked any of them for re-review (rule 8):

| row | change | effect on the cell |
|---|---|---|
| S-46 | I5 corrected 09-29 | the case cannot see the corrected claim (above) |
| S-22 | WE-2 amended 10-01 to a shared environment+terrain multiply (`0038B3E1`–`0038B424`) | DATA's review predates it; needs a coverage decision |
| S-26 | L-1 "never touches" became "never writes"; the id-39 read gates the MP and `+0x06` clamps (`0031050B`, `00310541`), unexecuted | narrowing: name the read side static |
| S-11 | EV-3 inverted (latch → skip flag) | the replay (`s12-opus-replay-weather-apply/check.py:177-181`) happens to match the new text; MET stands, reword |

Minor follow-ups:
- Wording-only changes: S-18 LD-5a / BL-6, S-31 I1, S-37 I-1, S-32 DR-5, S-41 AC-3 / AC-6, S-39 I-1 / I-6.
- S-01 I3 gained a script writer (`mainloopallsyncv` 0x018F → `0026DB10`). It is static for runtime, but it belongs in
  S-01's contract and script/data cells.

## Item 5: unicorn pinned (SWE2-AUDIT-SPEC)

- **[`replay-requirements.txt`](replay-requirements.txt) pins `unicorn==2.1.4`.** That is the version under which the
  replay packages were recorded and reproduce (`C:\Python314`).
- **[`check_unicorn.py`](check_unicorn.py) enforces it.** Its `require_pinned_unicorn()` checks the version and runs
  a translation-block flush probe: execute, rewrite, `ctl_flush_tb()`, then execute again and expect the new result.
  Measured:

| interpreter | unicorn | flush probe | exit |
|---|---|---|---|
| lane venv `Collaboration/Tools/analysis/venv` | 2.1.0 | **RAISED** `AssertionError('nargs must not exceed value of 15 (got 0)')`, the crash the S-08/S-13/S-22/S-23 replays hit | 1 |
| `C:\Python314` | 2.1.4 | PASS | 0 |

- **Reach:** 59 replay .py files call `ctl_flush_tb`, and 556 import unicorn.
- **Two repairs are owed:**
  - upgrade the shared venv. This is routed to SWE2-FRONTIER, because the venv is shared operations state and is not
    edited here;
  - have replay packages call `require_pinned_unicorn()`, or pin in their READMEs (OPUS, the package owner).

## Repair requests filed (SWE2-AUDIT-SPEC)

Each REJECT or narrowing goes to the owner of the cell or artefact. The board ids are in this lane's finish note.

| to | what |
|---|---|
| **OPUS** (type store, verdict table, criterion) | declare the 13 states in item 1's table plus the 15 S-49 addresses; record the five aliases; propagate S-19/S-51 meanings (4a); add "the excluded material is not named by the registry subject" to the denominator criterion; decide S-08's split; supply the 13 contract reasons; apply SCOPE-SHORT to S-01, S-16, S-21, S-25, S-29, S-38 and the narrow S-17, S-31, S-44 (the per-system sections are OPUS's); relink the 7 N/A-FALSE script/data cells; repair the S-46 I5 replay |
| **SWE2-AUDIT-SEM** (scorer of the types cells) | re-score the types cells of S-09, S-14, S-16, S-17, S-22, S-31, S-36, S-39 and S-45 to PARTIAL (and S-10/S-25 unless ruled CONSTANT / routed) until the declarations land, with L2 following |
| **SWE2-DATA** (runtime re-scoring lane) | S-46 I5, S-22 WE-2, S-26 L-1 / recovery tail, S-06 I-4, S-11 item-grant / EV-3 / TP-2, S-30 FZ-3, S-34, S-32 wording |
| **FABLE** (contract authors) | contract text for the SCOPE-SHORT rows' mechanisms; S-22 ST-4 / WE-2; S-39 §10.1; S-06 I-4 table; S-35 `[01F7FFE0]+0x38` notation |
| **SWE2-FRONTIER** | upgrade the lane venv's unicorn to 2.1.4 and check it with `check_unicorn.py` |

## Limits (SWE2-AUDIT-SPEC)

- **Item 1 is a worklist instrument plus a hand read.**
  - Heap or stack state named only in words is invisible to any regex.
  - The 134 UNATTRIBUTED offset table rows were not hand-read.
  - The alias table holds the five names this run met.
- **Items 3 and 4 were done by two sub-instances of this lane.**
  - Load-bearing addresses were spot-checked: the S-01, S-16, S-21 and S-44 greps, and the S-46 I5 tracer code.
  - Every other per-row claim is theirs.
- **No harness was re-run for item 4.** Judgments rest on harness code and recorded results.
- **No live evidence.** The S-30 live load is ASTRA's record, read here, not reproduced.
- **Ownership mapping.**
  - Bare cells are attributed to OPUS's per-system sections.
  - Types cells are attributed to SWE2-AUDIT-SEM (`rows.tsv`).
  - Where that mapping is wrong, the receiving lane should forward the request.
