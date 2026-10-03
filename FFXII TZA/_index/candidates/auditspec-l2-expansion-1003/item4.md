# Item 4 findings (SWE2-AUDIT-SPEC helper, 2026-10-03)

## Part (i) cannot-fail (item 4) (SWE2-AUDIT-SPEC)

**Instrument:** `_index/candidates/auditspec-l2-expansion-1003/cantfail_scan.py`. Output `cantfail.tsv`: 41 hits plus 1
row that names no package, over the 48 MET/LIVE runtime cells. The hits break down as:

| pattern | hits |
|---|---:|
| PRINT_ONLY | 22 |
| SELF_COMPARE | 6 |
| NO_COMPARE | 5 |
| SINGLE_THREAD | 4 |
| LITERAL_PASS | 3 |

Every hit is a candidate only. Hand-reading shows most are false positives:
- NO_COMPARE: the case variable is computed earlier with comparisons.
- SELF_COMPARE: these are NaN tests (`f == f`) and the `b & M == M` mask idiom.
- PRINT_ONLY: the `observed` key is asserted through `record(..., all(...))` / `eq(...)`.

**Agreement with SWE2-DATA (one line each):**
- S-22 `loop_early_exit_observed`: I agree with DATA. MET stands; the case should become an assertion.
- S-39 `G_handshake_I10`: I agree with DATA. MET stands; I-10's premise should be named as static.

**Judged hits (13, across 11 rows; rows outside DATA, AUDIT-SEM and the sample first):**

| # | row | site | pattern | discriminates? | judgment |
|---|---|---|---|---|---|
| 1 | S-06 | `s06-opus-replay-console-arms/check.py:263` `record("I4_float_steps_observed", True, …)` | LITERAL_PASS | **No.** It records the step values and asserts nothing. | I-4 (contract L121–) is a **static operand census**: "every RIP-relative operand of addss/subss/movss/mulss", 0.01 ×88. The runtime cell lists "I-1..I-4" as executed. The record corroborates the census (`result.json`: 0.01 is written by 56 arms). It also shows arms writing 0.005556, 0.52 and 1.1, which are not in I-4's table as printed. **MET stands, with a narrowing:** the cell should name I-4 as static (census) with corroborating execution, not as executed. The contract owner (FABLE) should list the full constant set or state that the table is truncated. |
| 2 | S-06 | `check.py:248` `record("postcondition_observed", True, …)` | LITERAL_PASS | **No.** | The postcondition text was struck (the cell says so: "what an arm wrote depends on the arm"), so it is not in the denominator. **No action**; the cell already discloses this. |
| 3 | S-34 | `s34-opus-replay-six-entries/check.py:222-230` `results["schedule_negative_index_observed"]` | PRINT_ONLY | **No.** It is observed and never asserted, and the harness comment says "observed, not decoded by the contract". | The cell says the 47,740-case schedule `00377970` is executed "**incl. the negative-index arm**", and counts it under "6/6 cases". The negative arm is not one of the 6 asserted cases. It is not a contract invariant either, so it is outside the denominator. **MET stands, with a narrowing:** drop "incl. the negative-index arm" or say it is recorded, not asserted. |
| 4 | S-32 | runtime cell text "on one thread the two resolves cannot disagree" (scan: SINGLE_THREAD) | SINGLE_THREAD | n/a (a static argument) | §14's LU divergence question is answered statically: `0020E600` is pure, with only reads between `0030C6F2` and `0030C706`. The argument is explicitly scoped to one thread. **MET stands, with a narrowing:** the cell should state that cross-thread writes to `[01F83530]` were not examined. Lead: this lane's own note records a neighbour's signed index (GiSetTexture) writing `01F83530`, so the single-thread premise is worth one sweep. |
| 5 | S-03 | `s03-opus-replay-mode-setters/check.py:125` `S_capture_layout…` | NO_COMPARE | **Yes.** `cap_ok` (L115) compares `rec[8:0x18]==blockA`, `rec[0x18:0x28]==blockB` and the flags word `==6`. The planted blocks are distinct byte ramps, so a swapped layout fails. | False positive. Stands. |
| 6 | S-41 | `s41-opus-replay-sound-request-stub-free/check.py:105` `no_fence_no_fault_in_any_run` | NO_COMPARE | **Yes** (`ok_all` at L104 is computed per run). | False positive. Stands. |
| 7 | S-29 | `s29-opus-replay-inventory-storage/check.py:97` `P3_image_pointers_null_for_all_15_classes` | NO_COMPARE | **Partly.** `unbound` checks the fixture's starting state, which is a precondition check, not behaviour. The behavioural P3 claims are L98–99. L99 uses `< 0x3000000` as "inside the image", a coarse bound. | Stands. Minor: L99's bound should be the image's real end. |
| 8 | S-38 | `s38-opus-replay-render-object/r4.py:123` `C_census_17_reads_16_functions_2_writes` | NO_COMPARE | n/a. It is a static census, labelled as such in the cell ("the latch census re-derived"). | Stands; it is static by nature. |
| 9 | S-37 | `s37-opus-replay-text-interpreter/i5_i9_i13.py:212` `I11_…` | NO_COMPARE | **Yes.** `i11` is built with `&=` over 3 thunks × 4 byte values, comparing `third()` to `want(b)`. | False positive. Stands. |
| 10 | S-32 | `s32-opus-replay-gil-storage/check.py:123` `meter_counters_observed` | PRINT_ONLY | **Yes** (`all(meter_effect.values())`). | False positive. Stands. |
| 11 | S-47 | `s47-opus-crt-memcpy-overlap/overlap_complete.py:93` `eq("overlap_copy_boundary_observed_once",copy_hits,1)` | PRINT_ONLY | **Yes** (an `eq` assertion). | False positive. Stands. |
| 12 | S-52 | runtime cell: "the two live debts are now discharged **statically** over the shipped-script domain" | (read) | n/a | The MET runtime cell rests partly on a **static census** (`s52-opus-slot-and-lookup-census`) for two former live debts. That is allowed only where the contract attributes those claims to static authority. Otherwise the criterion caps the cell at MIXED ("an invariant asserting execution behaviour with neither runtime evidence nor a contract static-attribution caps the cell at MIXED"). **Not judged here**; it goes to SPEC item 2 / DATA as a denominator-type ruling to check against the contract's words. |
| 13 | S-07/S-09/S-17 | `receipts/…` | SELF_COMPARE/PRINT_ONLY | n/a | Scan artefact: a generic directory named `receipts` matched the cell text. Not a replay of those rows. |

**Pattern result:** across the 48 cells, a literal pass sits under a credited invariant in **two packages**:
- S-22 (handled by DATA);
- S-06's I-4, which is static by nature, so the fix is a narrowing.

The 3 LITERAL_PASS hits come from those two packages. The other three literal records AUDIT-SEM listed are S-02's
(`check.py:112`, `:86`), and S-02 is already MIXED (DATA). Cells that cannot fail and carry an execution-only
invariant: **none found beyond S-02 and S-39 (I-10).** "Cannot fail" is therefore concentrated, not systemic. The
systemic part is **cell wording that overstates which cases assert** (S-06 I-4, S-34 negative arm, S-22 RW-2).

**Added after the scan (hand read):**

| # | row | site | pattern | discriminates? | judgment |
|---|---|---|---|---|---|
| 14 | **S-46** | `s46-opus-replay-routing-strict/check.py:148-149`: `gfx_writes = {a for a in accesses if a[0]=="gfx" and a[1]=="w"}`, then `expect("I5", min(gfx_writes) >= GFX_STATE and max(gfx_writes) < GFX_STATE + 0x9C4)` | cannot fail (tautology) | **No.** The tag `"gfx"` is assigned only to addresses inside `[GFX_STATE, GFX_STATE+0x9C4)`: EXP-144 `_experiments/evidence/s46-generator-routing/check.py:167` `WATCHES ("gfx", GFX_STATE, GFX_STATE + 0x9C4)`, and `on_write` `:212-216` records only tagged addresses. So "all gfx writes lie in the span" holds by construction. Writes to the index cells at `+0x9C8` (refill count) fall under the separate `"gfx-book"` tag (`:168`) and are never examined. The only discriminating part is `gfx_writes` being non-empty. | The runtime cell credits "**I5** gfx write span `01F7F600..+0x9C0`" as executed. I5 was **corrected on 2026-09-29** (`67b19a522`, after the 09-26 cell): the generator keeps its index as a `u32*` cursor at `+0x9C0` and a refill count at `+0x9C8`, both written by the twist `0018EE20` (contract L49, L96, L116-121). The replay's span check cannot see the `+0x9C8` write the corrected I5 names. **Proposed: narrow I5 to static** (W8 census plus the byte reads at `0018EECD` and `00194855`-`00194862`). I5 then rests on the falsification pass, not on execution. If DATA reads the corrected I5's "the twist resets both" as execution behaviour without a static attribution, the criterion caps the cell at **MIXED**. **Repair (OPUS, replay package):** assert the writes under the `gfx-book` tag (`+0x9C0` qword and `+0x9C8` dword set by the twist), and drop the tautological span check. |

## Part (ii) stale cells (item 4) (SWE2-AUDIT-SPEC)

**Instrument:** `stale_cells.py` produced `stale.tsv` with 68 rows over the MET/LIVE runtime cells. Each row is an invariant definition ADDED, AMENDED or REMOVED in a credited contract on or after the cell's scoring date. Of the 68:
- **Same-day rows (ordering unknown):** S-07, S-09, S-21, S-37 I-10, S-41 AC-6/7, S-42 MC-1.
  - S-07 was already handled by DATA (agree).
  - S-21: the contract change `a3707ab82` (04:33) precedes the cell's re-score commit `12412035c` (09:07), so it is not stale.
  - S-09: the cell is LIVE and already names AB-7 as a static remainder.
  - S-37 I-10: `405b26be6` is the execution package itself.
  - S-41 AC-6/7 were restated by FABLE from the executed dispatch.
  - S-42 MC-1 is ruled static-structure in the cell.
  - None of these needs a re-score.
- **Falsification-table rows read as ids (instrument artefact):** `V0`..`V10` in S-11, S-26 and S-32 are "claim | survives" rows from OPUS's 09-29 falsification passes, not invariants. Not stale.
- **Real post-cell changes (13), read by hand:**

| row | contract / id | commit, date | change | covered after the change? | proposed |
|---|---|---|---|---|---|
| **S-46** | which-generator I5 | `67b19a522`, 09-29 | **semantic correction**: the index is a cursor and a count, both reset by the twist | the replay's I5 check is tautological (Part (i) #14) | **narrow I5 to static, or MIXED** (DATA decides) |
| **S-22** | env-scaling WE-2 | `56d353a3a`, 10-01 (text says 10-02) | **semantic**: "three independent inputs multiplied in sequence" becomes "tested in sequence; an environment rule and a terrain rule for the same element share one multiply (`0038B3E1`-`0038B424`)" | DATA's S-22 review predates this and does not name WE-2. `s22-opus-replay-steps-and-element-scaling` was not checked for a same-element environment+terrain case | **DATA to check** whether a replay case drives the shared multiply. If none, and WE-2 carries no static attribution, the criterion caps the WE-2 share at MIXED |
| **S-26** | effect-layers L-1 | `075e2c653`, 09-29 | **semantic**: "never touches" becomes "never WRITES" the mutable layer. New behaviour: the rebuild reads mutable `+0x6C` and derived `+0x7C` (id 39), which gate the MP and `+0x06` clamps (`0031050B`, `00310541`, ...) | the runtime cell (09-26) credits row-3 and leaf entries; no cited case drives the id-39 gate | the corrected L-1 is a census reading (static by its own words: "Counting every byte..."). **Narrowing:** the cell should name L-1's read side as static; the MP-clamp gate by id 39 is unexecuted |
| **S-11** | env-variant EV-3 | `dae5bb6d9`, 10-02 | **semantic inversion**: "first-writer-wins latch released on exit" becomes "a skip flag this body only clears; setters `0026D8F0`/`00268320`" | `s12-opus-replay-weather-apply/check.py:177-181` plants the gate and asserts "gate armed -> request discarded, gate cleared once", which **matches the corrected text**. The old two-caller claim was never executed | **MET stands. Narrowing:** the cell's "clamp + latch" should become "clamp + skip-flag clear (single call); the setters are static" |
| S-18 | heading LD-5a | `9ca3df0ac`, 09-29 (text 09-30) | **ADDED precondition**: the pass-through assumes no input/output alias | ASTRA's `heading-passthrough-alias-boundary` is **method A, "no original machine-code execution"**, so it is static. The contract scopes it to the exact-alias case | **MET stands.** LD-5a is a static precondition, accepted by AUDIT-SEM (`64db6a9ef`). The cell should cite it as static |
| S-18 | turn-limiter BL-6 | `dae5bb6d9`, 10-02 | **precision**: the snap applies to unlatched steps (<=120 deg); above 120 deg the step is `cur +/- rate` with no snap | the 21,120-call grid passed; a snap within rate above 120 deg needs rate > 120 deg, outside the grid's domain | MET stands; the cell's BL-6 phrase should follow the new wording |
| S-31 | licence I1 | `9d6d954a3`, 09-29 | **count**: 3 exits become 4. In the same pass, CON-159 found two entrants (equipment kind 0) and CON-160 withdrew I4's "early exit is load-bearing" | I-1..I-5 are `[page]`, so static by the contract's words (the cell says so). `i1i2.py` drove kind 1 only ("543 shipped abilities kind1+slot7") | MET stands. **Narrowing:** the cell's "named exits" should say the 4th exit and the kind-0 (equipment) entrant `00323C60` are static only |
| S-01 | boot-fixups I3 | `5b49942c3`, 09-29 | **semantic**: "evaluated once" becomes "re-evaluated on area change (`002628B0`->`002695A0`) and settable by script (`mainloopallsyncv` 0x018F -> `0026DB10`)" | `[page]`-tagged, so static | the runtime cell is unaffected. The **contract and script/data cells** should carry the new script writer (item 3) |
| S-37 | text I-1 | `d9595b0e8`, 09-28 | narrowing: five callers loop on it, two use only the cursor | a static caller census | no runtime action |
| S-32 | defeat-rewards DR-5 | `1305be85a`, 10-01 | naming: "status id 12" becomes "**effect** id 12" (the test offsets `+0x69`/`+0x79` are unchanged) | the replay plants bytes at the tested offsets, so it is unaffected | the cell's wording follows the new name |
| S-41 | bank family AC-3, AC-6 | `af392a926`, 10-01 | AC-3 semantic (a member-object thunk, not a second base: static); AC-6 count 5 -> 6 (the bit list was already six) | cosmetic for runtime | none |
| S-39 | I-6, I-1 | `9ad755589` 09-28; `c7667382f` 10-02 | I-6 address `0018C934`->`0018C933` (citation fix); I-1 "every enqueue" becomes "the 36 owner-side enqueues" (`001E5270`, `001F89B0` push to the ordered list only) | S-39 handled by DATA/SPEC. The I-1 change bears on SPEC's section-10.1 null-path finding: the four ordered-only appenders do not push onto the owner list | no runtime action; noted for the S-39 repair |
| S-07 | lifecycle N-5, interpreter I1-I8/V-1..V-8 | same day, 09-26 | the SECTION-11/12 rewrite | DATA: "S-07 stands" | agree |

**Undated cells:** none remain after the fallback (S-11 -> 2026-09-25, S-34 -> 2026-09-25, S-38 -> 2026-09-26). S-34 and S-38 have no invariant changes since their dates.

**Pattern result (S-28 pattern 1, "cells go stale after contract growth"):**
- It **holds, beyond the sample**. Four rows outside DATA's 11 had semantic invariant changes after their runtime cell:
  - S-46 I5;
  - S-22 WE-2 (S-22 is a DATA row, but WE-2 is new since DATA's read);
  - S-26 L-1;
  - S-11 EV-3.
- In one (S-11) the executed case happens to match the corrected text.
- In one (S-46) the executed case cannot see the corrected claim.
- Two (S-26, S-22) need a coverage decision.
- No cell was marked for re-review by any of these commits (EVIDENCE-POLICY rule 8).

## Per-row action table (item 4) (SWE2-AUDIT-SPEC)

| system | finding | proposed runtime-cell action | owner (cell scorer -> repair) |
|---|---|---|---|
| S-46 | I5's replay span check is tautological; I5 corrected after the cell | narrow I5 to static, or **MIXED** if the corrected I5 is read as execution behaviour | SWE2-AUDIT-SEM scored the cell -> **SWE2-DATA** re-score; **OPUS** replay repair (assert the `gfx-book` writes) |
| S-22 | WE-2 amended 10-01/02 (shared env+terrain multiply), unchecked against the replays | check for a driving case; MIXED share if none and no static attribution | SWE2-DATA (re-score); OPUS (replay or contract attribution) |
| S-26 | L-1 corrected 09-29: the read side and the id-39 clamp gate are unexecuted | narrowing (L-1 read side static) | SWE2-DATA; contract author (`CONTRACT-effect-layers`: FABLE, falsification pass by OPUS) |
| S-11 | EV-3 inverted 10-02; the replay matches the new text | MET stands; reword "latch" | SWE2-AUDIT-SEM cell wording -> SWE2-DATA |
| S-06 | I-4 credited as executed through a literal-pass record; it is a static census. Observed step values 0.005556/0.52/1.1 are missing from I-4's table | MET stands; name I-4 static | SWE2-DATA (wording); FABLE (contract table completeness) |
| S-34 | "incl. the negative-index arm" counted, but it is print-only and not a contract claim | MET stands; drop or qualify the phrase | SWE2-DATA (wording) |
| S-32 | LU divergence answered "on one thread"; cross-thread writers of `[01F83530]` unexamined (a neighbour's signed-index writer is known) | MET stands; state the single-thread scope | SWE2-DATA (wording); FABLE/OPUS (one sweep for writers of `01F83530`) |
| S-52 | MET partly rests on a static census for two former live debts | route to the item-2/denominator check | SWE2-AUDIT-SPEC item 2 / SWE2-DATA |
| S-31 | I1 now 4 exits, kind-0 entrant: static only (I-1..I-5 `[page]`) | MET stands; narrowing | SWE2-DATA (wording) |
| S-18 | LD-5a added (static, ASTRA method A); BL-6 precision | MET stands; cite LD-5a as static | SWE2-DATA (wording) |
| S-01 | I3: a script writer and an area recompute added (static) | runtime unaffected; carry to the contract/script cells | item 3 (script/data cell) |
| S-22 / S-39 | as DATA (agree): RW-2 assertion; I-10 premise static | - | per DATA |
