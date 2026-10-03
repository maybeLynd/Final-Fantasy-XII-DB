# C9 runtime exclusions read against the registry subject (SWE2-DATA, 2026-10-03)

*Request `OPUS-REQ-DATA-RUNTIME-EXCLUSIONS-C9-1003`. Independent re-score lane (SWE2-DATA, Claude stand-in for the
rate-limited Devin session). Rule applied: L2-VERDICTS "Amendment — an exclusion may not drop registry-subject material"
(OPUS, 2026-10-03). The registry subject is `important-subsystems.tsv` column 3 plus the pages in column 5. Nothing in
`L2-VERDICTS.md`, any page or any tool was edited. The parent applies [`edits.json`](edits.json).*

## Outcome (SWE2-DATA)

`checkpoint_consistency.py` at HEAD printed, copied from its output:

```
STALE C9  runtime exclusions scored before the amendment, to be re-read against the registry subject: S-05, S-06, S-08, S-11, S-13, S-22, S-23, S-26, S-36, S-37, S-40, S-42
```

All 12 rows were read. **5 are CITE** (verdict kept, each excluded item named, amendment cited). **7 are RE-SCORE to
MIXED**, because the subject names an item the cell left without evidence. **4 L2 cells change MET → NOT MET** (S-06,
S-26, S-37, S-40). S-08, S-22 and S-36 were already L2 NOT MET for other cells. Measured by `build_edits.py` with
`progress_report.parse_verdicts` on a patched copy, copied from its output:

```
L2 MET before: 31 of 52
L2 MET after:  27 of 52
left MET: ['S-06', 'S-26', 'S-37', 'S-40']
runtime column before: {'MET': 45, 'MIXED': 5, 'LIVE': 2}
runtime column after:  {'MET': 38, 'MIXED': 12, 'LIVE': 2}
C9 after  (late, stale): ([], [])
```

| row | excluded items | named by the subject? | disposition | L2 effect |
|---|---|---|---|---|
| S-05 | TW-1..TW-6 (static census) | the area yes; the census facts are counted and evidenced statically, so nothing is dropped | CITE | none (MET) |
| S-06 | 63 of 282 commands stop at unplanted objects or imports; I-4 (constant census) | **yes**: "282 commands", and the page catalogues every arm | **MIXED** | **MET → NOT MET** |
| S-08 | file layer; kind `0xFF` raw-path request | **yes, both**. The file layer is covered by the contract SCOPE-SHORT; kind `0xFF` is not | **MIXED** | none (already NOT MET) |
| S-11 | `<0x1FF` item-grant arm in `0046A9D0`/`0046AB10`; TP-7 (census) | no: the page disclaims what `0046A9D0` does. TP-7 is counted statically | CITE | none (MET) |
| S-13 | live-game capture | no (a tier, not material) | CITE | none (MET) |
| S-22 | what the 152 step-target bodies do | **yes**: "calculator slots" | **MIXED** | none (already NOT MET) |
| S-23 | revive respawn chain `00386A70` → `00301140`; the twelve callees; live capture | no for the respawn chain. The callees, `00469BB0` among them, ran real (EXP-093). Live capture is a tier | CITE | none (MET) |
| S-26 | L-1 read side (id-39 MP pin); recovery tail past `00238BF0`; credit effects; live capture | **yes** for the id-39 MP pin (two-layer page §12); no for the rest | **MIXED** | **MET → NOT MET** |
| S-36 | arbiter unreached (device gate): its request posts, R-4's arbiter half; dead input-script writers; live capture | **yes** for the arbiter's request posts (router page §8, C-4) | **MIXED** | none (already NOT MET) |
| S-37 | `002A9F00` emit-side re-entry (device gate) | **yes**: the language page's mutual recursion through the emitter | **MIXED** | **MET → NOT MET** |
| S-40 | frame half: setters, `ApplyEffects`, the run call (device gate); I-3/I-4 static | **yes**: the catalogue page's "frame half" section | **MIXED** | **MET → NOT MET** |
| S-42 | MC-1, MC-2 (static census, tail jump) | counted and evidenced statically; nothing dropped | CITE | none (MET) |

**Edits: 23** — 12 runtime cells, 4 L2 cells, and 7 binding-gap cells. The gap cells strike the stale "runtime MET"
statement on each re-scored row, or append to it (S-36). They are optional for C9, but without them the gap column
contradicts the runtime column.

## Reading used for static and tier items (SWE2-DATA)

The amendment lists "a contract's own disclosed static scope" among the exclusions that may not drop subject material.
I read it as applying to **behaviour that could be executed but rests static**: S-26's id-39 arm, S-40's setters,
S-35's assignment path. It does not apply to **an image census or structure fact** (TW-1..6, TP-7, MC-1/MC-2, I-4's
constant table). No execution can observe such a fact. Each one is byte-verified at tier 1, so it is counted in the
denominator and covered statically, not excluded. This agrees with SWE2-AUDIT-SPEC's item 2 ("static-structure
denominator rulings are sound where the invariant is itself a census claim"). Live capture is likewise a tier above
stub-free replay, not material. **If OPUS reads "static scope" to include census facts, S-05, S-11 and S-42 would move
to MIXED as well and could never return to MET.** That result is absurd, which is why I did not take that reading.

**Where this re-read disagrees with SWE2-AUDIT-SPEC's item 2:**
- **S-11.** SPEC called the item grant "a consequence the subject names". The trigger-point page says the opposite in
  its own "What this document does not claim": "what `0046A9D0` does with the chosen one".
- **S-26, S-36, S-37, S-40.** SPEC ruled these "stands with narrowing" or "sound as bounded rulings". They were judged
  before the amendment existed. Read against the subject pages, each leaves a named, executable item without evidence.

## Applying the edits (SWE2-DATA)

- The `old` texts are the cells split on unescaped `|` and stripped, exactly as `cells.py` prints them.
- Replace the cell content in place. S-42's row has a separator without a leading space (`…d**| MET`), so an applier
  that rejoins cells with `" | "` would also normalise that spacing on S-42's line.
- Re-scored cells keep the old text struck. When the old cell already held a struck span, each unstruck stretch is
  struck on its own and the existing span is kept (`~~A Superseded:~~ ~~B~~ **MIXED …**`), because nested `~~` would
  break `CELL_STRUCK`. The script checks that removing the added markers rebuilds the original byte for byte, and that
  `_cell_verdict` reads the intended verdict.
- After applying: C3 will FAIL until `PROGRESS.md` is regenerated (31 → 27 of 52). C4 has no summary tables at HEAD.
  C9 goes to PASS (CITE cells carry "exclusion may not drop"; MIXED cells are outside C9's MET/LIVE filter).
- Scripts: `Database/Tools/work/SWE2-DATA/c9scratch/build_edits.py` (builds and validates) and `s06b.py` (the 63 S-06
  stops). The patched preview `L2-VERDICTS.patched-preview.md` is in the same folder.

## S-05 — CITE (SWE2-DATA)

Subject (col 3): "Shared transform workbench — the matrix area four subsystems pass arguments through"; page
`the-shared-transform-workbench.md`. Excluded: TW-1..TW-6 of `CONTRACT-shared-transform-workbench.md`. All six are
census or ownership facts: L68 "no static bytes", L73 46 aligned addresses, L78 the one `003970A0` copy, L86 267/249/18,
L102 no owner, L110 the `022D94B0`/`B4` table. Evidence rows L197–202 are tier 1, and falsification pass 1 W1–W5 reproduce
every count. The executable material the page names (the deposits and the save/restore) is executed by
`s05-opus-replay-transform-contracts`. **CITE.**

**Proposed runtime cell (full replacement text):**

```text
**MET — re-scored 2026-09-26 (SWE2-AUDIT-SEM): `s05-opus-replay-transform-contracts/check.py` runs all runtime-named invariants stub-free, zero application stubs / no stop boundary / no bridged imports (9/9, identical ×2, reproduced md5 `034006f3`): primitives inv.1 (the `w` lane is the live vf00 load `[01EF93FC]`, byte-exact `movss`@`0039A026` — in.w irrelevant), inv.2 (no perspective divide), inv.3 (aliasing safe), §4 compose order `b×a`, §5 four deposits (rip-relative stores to `022D91A0`/`022D9300`/`022D8F90` byte-verified; input verbatim at `022D9300` = `movaps xmm6,[rcx]`), save/restore run-notes 1-2 + §4 + §7 + §10 (`0036D930` variadic — pointers `02EC0A00+i*8`, rows `02EC0800+i*16`, depth `022D8F08`, all `lea` byte-exact; inner-save-overwrites-outer and restore idempotency executed). `CONTRACT-shared-transform-workbench.md` TW-1..TW-6 ruled static census invariants (the contract's own §4: "every invariant below is a code measurement and not a data one") — outside the runtime denominator per the static-structure ruling. Every named runtime invariant covered** **Exclusions named under the exclusion amendment (L2-VERDICTS "Amendment — an exclusion may not drop registry-subject material", OPUS, 2026-10-03); re-read 2026-10-03 by SWE2-DATA, independent hand, request `OPUS-REQ-DATA-RUNTIME-EXCLUSIONS-C9-1003`, record `swe2data-c9-exclusions-1003`:** TW-1..TW-6 of `CONTRACT-shared-transform-workbench.md` are counted, not excluded. Each is an image census fact (no static bytes, 46 aligned row addresses, the one `003970A0` matrix copy, the 267 / 249 / 18 toucher census, no owner, the `022D94B0`/`022D94B4` record table) about the area the registry subject names ("the matrix area four subsystems pass arguments through"). No execution can observe a census, and each carries tier-1 byte evidence (contract §15; falsification pass 1, W1-W5), so it is covered statically. No executable behaviour the subject or its page names is outside the executed set.
```

## S-06 — RE-SCORE (SWE2-DATA)

Subject: "Developer tuning console — 282 commands over the render-settings block"; page
`the-282-command-parameter-console.md`. §2 "What the arms actually do, counted rather than sampled" classifies all 226
real arms (110 stepping, 63 calling out to a subsystem, 31 other, 21 byte or flag writes, 1 float store). §10 is "The arm
catalogue, and the block it tunes". In `s06-opus-replay-console-arms/result.json` (`per_id`), 63 ids are stopped
(`s06b.py`; for example id 20 'Load chr:' stops at `00000008`, id 25 'Shadow Level:' at `001EF280`, id 28 'Use PS2
lighting:' at `000002D4`). The package README says: "of the 282 ids, 219 complete under the fixture … 63 stop at an
unplanted object or a trapped import". These are named commands whose effects are not observed. The contract's
postcondition "what an arm wrote depends on the arm" does not remove them, because the amendment says "whatever the
contract's wording says". I-4 (contract L121) is a constant census, counted statically. Its three runtime steps
missing from the table are a contract wording issue, already recorded. **RE-SCORE MIXED; L2 NOT MET.**

**Proposed runtime cell (full replacement text):**

```text
~~**MET — re-worded 2026-10-03 (SWE2-DATA, independent hand; `AUDITSPEC-REQ-SWE2-DATA-L2EXP-REPAIRS-1003`, record `swe2data-l2exp-repairs-1003`), named coverage:** The dispatch and I-1..I-3 are executed for all 282 ids in both directions (blocks 291/315; every call takes exactly one table arm or the out-of-range exit `001D1696`). I-4 is a static constant census in the contract's own words, not executed: the replay's `I4_float_steps_observed` is a literal pass that records the steps (0.005556, 0.52 and 1.1 are observed but missing from I-4's table, a contract fix for its owner). 63 of the 282 command arms stop at unplanted loader, iostream or object boundaries, and their effects are not L2-covered. Superseded:~~ ~~**MET — re-scored 2026-09-26 (SWE2-AUDIT-SEM) on `AUDITSEM-REQ-OPUS-393`, under the 380 precedent and the contract's own denominator: blocks 291/315 execute the dispatch for all 282 ids both directions — every call takes exactly one table arm or the out-of-range exit (`001D1696` observed), which is the contract's whole named runtime claim (I-1..I-4 + 'exactly one arm ran or none'). (1) The 63 arms that stop inside unplanted loaders/iostreams/objects are the tuned subsystems' own contract families — no invariant of this contract names an arm's internals (the same shape as S-11's item-grant arm inside the delivery callee); out of this denominator per invariant granularity. (2) The section-16 INTEGRATION row survives only as a parity-plan test dimension — its postcondition text was struck and replaced with 'what an arm wrote depends on the arm' (FABLE 2026-09-25); not in the denominator. Every named runtime invariant covered**~~ **MIXED — re-scored 2026-10-03 (SWE2-DATA, independent hand, on the exclusion amendment (L2-VERDICTS "Amendment — an exclusion may not drop registry-subject material", OPUS, 2026-10-03); request `OPUS-REQ-DATA-RUNTIME-EXCLUSIONS-C9-1003`, record `swe2data-c9-exclusions-1003`): the registry subject is "282 commands over the render-settings block", and its page catalogues every arm (§2 "What the arms actually do", over all 226 real arms;§10 the arm catalogue). 63 of the 282 commands stop at an unplanted object or a trapped import in `s06-opus-replay-console-arms` (`result.json` per_id; for example id 25 'Shadow Level:' and id 28 'Use PS2 lighting:'). Their effects carry no runtime evidence, the subject names them, and no contract cell records a SCOPE-SHORT for them. Executed and kept: the dispatch and I-1..I-3 for all 282 ids in both directions (blocks 291/315), 219 of the 282 completing under the fixture. I-4 is an image constant census, covered statically. Restored to MET by planting the objects those 63 arms reach (or bridging their imports) and observing their writes.**
```

**Proposed L2 cell:**

```text
~~**MET**~~ **NOT MET — the runtime cell is MIXED (re-scored 2026-10-03, SWE2-DATA, independent hand, on the exclusion amendment; record `swe2data-c9-exclusions-1003`): 63 of the 282 commands the registry subject names stop before their effect**
```

**Proposed binding-gap cell:**

```text
types MET; ~~runtime MET 2026-09-26 — all 282 dispatches + I-1..I-4 executed stub-free; I-5..I-7 static-discharged; arm internals and section-16's integration row ruled out-of-denominator (393)~~ **runtime MIXED (re-scored 2026-10-03, SWE2-DATA, on the exclusion amendment): 63 of the 282 commands stop at unplanted objects or trapped imports; closes when their writes are observed**
```

## S-08 — RE-SCORE (SWE2-DATA)

Subject: "The resource request queue and file layer — 64 slots, the file-size table, loose files then the
archive, the BigFile index". (1) The file layer is named. The amendment accepts the contract cell's SCOPE-SHORT in its
place ("until that material carries evidence or the contract cell records a SCOPE-SHORT"), and OPUS recorded that
SCOPE-SHORT on 2026-10-03. (2) The kind `0xFF` raw-path request is named by the queue page (L145 in §2.3:
"kind `0xFF` → `002DF6C0(index, dest, offset)`, where `index` **is a path pointer**"; L344 in the key-address table;
L461 in §6 "`kind 0xFF` loads a path directly"). The contract names it too: its §7 state-1 row (L176, "Kind-FF nonzero
submit result revisits the same head") and §8 (L199). The cell itself says it "is not executed and is not a named
invariant". It is in a credited contract and on the page, and the SCOPE-SHORT (the file layer) does not cover it.
**RE-SCORE MIXED; L2 already NOT MET.**

**Proposed runtime cell (full replacement text):**

```text
~~**MET — re-worded 2026-10-03 (SWE2-DATA, independent hand; `AUDITSPEC-REQ-SWE2-DATA-L2EXP-REPAIRS-1003`, record `swe2data-l2exp-repairs-1003`), named coverage:** `pump_states.py` executes every section 7 state row and I1-I7 stub-free, as before. Scope: the file layer (FST sizing, loose then archive, the BigFile index, the `0215EFF4` status producer) is not executed; the absent-entry plant returns at `002DF7B9`. The registry subject names the file layer, so whether this row may exclude it is the contract-scope question SWE2-AUDIT-SPEC escalated to OPUS (`auditspec-l2-expansion-1003` item 2), not a runtime denominator ruling. The kind `0xFF` path (section 8) is not executed and is not a named invariant. Superseded:~~ ~~**MET — re-scored 2026-09-26 (SWE2-AUDIT-SEM) on `AUDITSEM-REQ-OPUS-387`: `pump_states.py` (8/8 + inherited, reproduced md5 `32bc3d9c`; `i2i3` `14d42040`/`i5` `08d9f1ce` kept) executes every §7 state row stub-free — S1 issue (`0046E030`=`call 002DF780; mov eax,1` byte-exact: acceptance reported regardless of the file layer's result), S2/S3 stamp+wait, S5 delivered callback+recycle, S6 failed reports only on part=-1, S4 cancel zeroes count only with a callback, C1 requeue (state 1, min-cap, 0x800-aligned offset, accumulator 0) then rides 1→2→3→5, C2 re-probe without subtraction, C3 re-subtraction, CE terminal. Device-status helpers byte-exact (`0046DFE0` returns 2 iff `[0215EFF4]`=-1; `002DF7B9` `cmp -1;je` absent-entry early return verified). Contract §7 explicitly files 'external read behavior' as separate and §14 names the real read/file/archive layer an unresolved boundary — out of this contract's runtime denominator. Every named invariant I-1..I-7 + all §7 rows covered**~~ **MIXED — re-scored 2026-10-03 (SWE2-DATA, independent hand, on the exclusion amendment (L2-VERDICTS "Amendment — an exclusion may not drop registry-subject material", OPUS, 2026-10-03); request `OPUS-REQ-DATA-RUNTIME-EXCLUSIONS-C9-1003`, record `swe2data-c9-exclusions-1003`): the registry subject ("The resource request queue and file layer — 64 slots, the file-size table, loose files then the archive, the BigFile index") names both items this row left unexecuted. (1) The file layer (FST sizing, loose then archive, the BigFile index, the `0215EFF4` status producer) is recorded as SCOPE-SHORT in the contract cell (OPUS, 2026-10-03), which the amendment accepts in place of evidence. (2) The kind `0xFF` raw-path request is named by the queue page (§2.3 state 1: "kind `0xFF` → `002DF6C0(index, dest, offset)`, where `index` is a path pointer", `0032E105`–`0032E118`; §6 "`kind 0xFF` loads a path directly") and by the contract's own §7 state-1 row ("Kind-FF nonzero submit result revisits the same head") and §8. It is not executed, and no SCOPE-SHORT covers it. Executed and kept: `pump_states.py` runs every §7 state row except state 1's kind-FF clause, and I-1..I-7, stub-free. Restored to MET by a kind-`0xFF` request through the pump: the issue, the revisit on a nonzero submit, and the sign-extended free.**
```

**Proposed binding-gap cell:**

```text
types MET; ~~runtime MET 2026-09-26 — I-1..I-7 + every §7 pump state executed stub-free; file/archive layer is contract-excluded (§7/§14 boundary)~~ **runtime MIXED (re-scored 2026-10-03, SWE2-DATA, on the exclusion amendment): the kind `0xFF` raw-path request the queue page and §7 name is unexecuted; the file layer is the contract cell's SCOPE-SHORT**
```

## S-11 — CITE (SWE2-DATA)

Subject: "Field records and area transition — `navimapdata.bin`, trigger points, the environment variant". The
item-grant arm sits inside `0046A9D0`/`0046AB10`. The trigger-point page names only the hand-off: L91–92 "hand the
chosen value to the acting unit (`0046A9D0`)". Then L130: "**What this document does not claim:** what the two outcome
values are, what `0046A9D0` does with the chosen one". `0046A9D0` appears nowhere on the field-record or
environment-variant page (grep: only L92 and L130 of the trigger page). TP-7 (contract L121: "one of exactly TWO
functions in the image that both draw the generator and write a persistent flag") is an image census, tier 1 (L210).
Not an exclusion: EV-4 "in part". Block 303's extraction calls execute the `(selector + 1) × 4` offset, and only a
separate assertion is missing (`s11-opus-replay-environment-variant` "Not covered"). **CITE.**

**Proposed runtime cell (full replacement text):**

```text
**MET — re-worded 2026-10-03 (SWE2-DATA, independent hand; `AUDITSPEC-REQ-SWE2-DATA-L2EXP-REPAIRS-1003`, record `swe2data-l2exp-repairs-1003`), named coverage:** Accessors (9/9), trigger points TP-1/3/4/5/6 and env-variant EV-1/2/5/6 execute stub-free. TP-2, corrected to 'both heights are zeroed', is executed and asserted by `s11-opus-replay-trigger-points` `TP2_height_is_ignored`: a unit 1.0 above a point 1.0 away fires, because `002F8150` zeroes the unit's height. The earlier 'contradicted by execution' is answered by that correction. EV-3, now a skip flag rather than a latch, matches `s12-opus-replay-weather-apply` (L177-181). EV-4 is covered in part. TP-7 is static-structure. Not executed, and named: the `<0x1FF` item-grant arm inside the delivery callee `0046A9D0`/`0046AB10`, since every tested outcome is `>= 0x200`, which `0046AB19` refuses. Superseded: ~~**MET — accessors (9/9, no boundary), trigger-points (TP-1/3/4/5/6) and env-variant execute stub-free — EV-1 (tail call, four zero args), EV-2/3 (clamp + latch via `s12-opus-replay-weather-apply`, same body `0026D910`), EV-5 band, EV-6 pre-clear + stale-retention all measured; EV-4 in part. Not covered: TP-7, the item-grant branch (all observed outcomes ≥ 0x200) — and **TP-2 was contradicted by execution** (routed to FABLE) — re-scored 2026-09-25 (SWE2-AUDIT-SEM) under the `runtime` criterion ruling**; TP-7 ruled static-structure on REQ-360 (one-of-two census is an image fact, not execution behaviour) — the item-grant branch remains** — *re-ruled 2026-09-26 (SWE2-AUDIT-SEM) on `AUDITSEM-REQ-OPUS-380`: the `<0x1FF` grant arm sits inside the delivery callee `0046A9D0`/`0046AB10`, not in this contract — no TP invariant names it; TP-4's named claim is 'delivers the chosen outcome' and that call is executed (the `>=0x1FF` refusal at `0046AB19` observed). Out of the runtime denominator per invariant granularity*~~ **Exclusions named under the exclusion amendment (L2-VERDICTS "Amendment — an exclusion may not drop registry-subject material", OPUS, 2026-10-03); re-read 2026-10-03 by SWE2-DATA, independent hand, request `OPUS-REQ-DATA-RUNTIME-EXCLUSIONS-C9-1003`, record `swe2data-c9-exclusions-1003`:** (1) The `<0x1FF` item-grant arm inside the delivery callee `0046A9D0`/`0046AB10` is outside the registry subject. The trigger-point page names the hand-off ("hand the chosen value to the acting unit (`0046A9D0`)"), which is executed (TP-4's delivery call, the `>=0x1FF` refusal at `0046AB19` observed). It then states, in its own "What this document does not claim", that it does not claim "what `0046A9D0` does with the chosen one". Neither the field-record page nor the environment-variant page cites `0046A9D0`. (2) TP-7 ("exactly TWO functions in the image that both draw the generator and write a persistent flag") is an image census, counted and covered by its tier-1 sweep (contract §15), not excluded.
```

## S-13 — CITE (SWE2-DATA)

Subject: "Actor storage, manager slots and the unit pool — the record behind every actor, the five manager
slots, the battle-unit slot pool and actor class". The cell's only exclusion is "Residual: live only". The package's
"Not covered" list leaves only "a live game" after R1 and R2 executed (`s13-opus-replay-record-pool-stub-free` README
L75–78). Live capture is a tier, not material, and the region map was observed live in `EXP-026` (contract §13, L423).
**CITE.**

**Proposed runtime cell (full replacement text):**

```text
**MET — re-scored 2026-09-26 (SWE2-AUDIT-SEM) on `AUDITSEM-REQ-OPUS-418`: `s13-opus-replay-record-pool-stub-free/residuals.py` (3/3, identical twice, reproduced md5 `aa917ce4`; the published `check.py` run and `f11ac855` unchanged — variants by environment only) discharges every named residual. R1: one record in each of the eight groups (kinds 0-7) — all 11 base cases pass, every layout class 0-3 carved including class 2 (groups 3/4: `+0xA0` at `+0x140`, `+0xB8` at `+0x120`, `+0xC0` = 0), so ctor kinds 3/4/6 now run. R2: `w[desc]=0xA` — the `>=0xA` gate `002668E7` (`cmp eax,0xA`/`jb`, byte-exact) admits site 1 `002668EC` on every one of the six ctor calls; the default-4 arm never ran. R3 STATIC: the caller-supplied allocator arm resolves to the default anyway — `0026C8C0`'s sole caller `0032F850` passes `r8 = lea [rip-0xC8031]` at `0032F95A` = `00267930` itself (byte-verified), so the `cmovne r12,r8` at `0026C8FA` substitutes the allocator `check.py` already ran. Residual: live only — outside the L2 denominator per the ruled criterion** **Exclusions named under the exclusion amendment (L2-VERDICTS "Amendment — an exclusion may not drop registry-subject material", OPUS, 2026-10-03); re-read 2026-10-03 by SWE2-DATA, independent hand, request `OPUS-REQ-DATA-RUNTIME-EXCLUSIONS-C9-1003`, record `swe2data-c9-exclusions-1003`:** One item: live-game capture. It is an evidence tier above stub-free replay, not material of the registry subject ("the record behind every actor, the five manager slots, the battle-unit slot pool and actor class"); R1 and R2 are executed, and R3's allocator arm resolves statically to the allocator `check.py` runs. The region map is in any case observed live in `EXP-026` (`CONTRACT-actor-record-pool-and-region-map.md` §13).
```

## S-22 — RE-SCORE (SWE2-DATA)

Subject: "The formula step table and calculator slots — recipes, the preparation family, the evaluation
context, the scratch block, elemental and weather scaling". The step-table page says the slots are the calculators:
L438 "Calculator slots take `(source stats, target stats, &ctx)`", the §"152 distinct targets, and 42 slots that do
nothing" (L101), and per-target rows such as L212 for `0038EFB0`. Contract §14 L174 reads "What 125 of the 152 targets
do." The current cell calls this "the contract-scope question … not a runtime exclusion". Under the amendment that
route needs a contract SCOPE-SHORT, and S-22's contract cell is MET. **RE-SCORE MIXED; L2 already NOT MET.**

**Proposed runtime cell (full replacement text):**

```text
~~**MET — re-worded 2026-10-03 (SWE2-DATA, independent hand; `AUDITSPEC-REQ-SWE2-DATA-L2EXP-REPAIRS-1003`, record `swe2data-l2exp-repairs-1003`), named coverage:** WE-1 is executed by `we1.py` (stage order 94 before 95 in all seven dual recipes; the read hook on the action row's `+0x13` discriminates the offset read). The RW-2 cut-short is recorded in `result.json` (cases 6 and 2 stop the step after the flag goes to 1), but recorded, not asserted. WE-2, amended 2026-10-02 to a shared environment and terrain multiply (`0038B3E1`-`0038B424`), is covered by `s22-opus-replay-steps-and-element-scaling`'s executed rule table (6 elements x 4 environments x 3 weather classes x 4 terrains through `0038B220`). Its recorded multipliers never exceed one factor of 1.2 or 0.5 per rule pair: Water, x1.2 'when environment 3 or terrain 0', never records 1.44. Also recorded, not asserted. Not covered: what the 152 step-target bodies (the calculator slots the registry subject names) do. That is the contract-scope question SWE2-AUDIT-SPEC escalated to OPUS (`auditspec-l2-expansion-1003` item 2), not a runtime exclusion. Superseded:~~ ~~**MET — re-scored 2026-09-26 (SWE2-AUDIT-SEM) on `AUDITSEM-REQ-OPUS-405`: `we1.py` (4/4, identical ×2, reproduced md5 `5680857b`; block-316 cases run first, result unchanged) executes WE-1's stage order through the real resolver `00385F60` — step ids 94=`0038B220` / 95=`0038B6A0` adjacent at `01EFA5C0+94*8`/`+95*8` (byte-verified), all seven shipped dual-recipes (7, 14, 37, 63, 83, 105, 106) order 94 before 95, five executed with both functions reading the action row `+0x13`; recipes 14/37 stop early on `[02AEDFB8]` — the committed-list cut-short RW-2 names. Ruling (denominator): 'step-target bodies with no tested recipe calls' is a coverage statement over 152 targets, not a named invariant — none of S-22's four contracts names per-target execution — out of the runtime denominator (380 precedent). Every named runtime invariant covered**~~ **MIXED — re-scored 2026-10-03 (SWE2-DATA, independent hand, on the exclusion amendment (L2-VERDICTS "Amendment — an exclusion may not drop registry-subject material", OPUS, 2026-10-03); request `OPUS-REQ-DATA-RUNTIME-EXCLUSIONS-C9-1003`, record `swe2data-c9-exclusions-1003`): the registry subject is "The formula step table and calculator slots — recipes, the preparation family, the evaluation context, the scratch block, elemental and weather scaling". The step-table page says the slots are the calculators ("Calculator slots take `(source stats, target stats, &ctx)`"; "152 distinct targets, and 42 slots that do nothing") and catalogues what named targets do. What the 152 step-target bodies do is not executed beyond the recipes and steps the replays run (contract §14 still lists "What 125 of the 152 targets do"). No contract cell records that shortfall as SCOPE-SHORT, so the material stays in the denominator without evidence. Executed and kept: WE-1 (`we1.py`), WE-2's rule table (`s22-opus-replay-steps-and-element-scaling`) and RW-2's cut-short, the last two recorded and not asserted. Restored to MET by executing the step-target bodies the subject names, or by a SCOPE-SHORT on the contract cell.**
```

**Proposed binding-gap cell:**

```text
**types PARTIAL (2026-10-03, SWE2-AUDIT-SEM, on SWE2-AUDIT-SPEC's independent finding; record `auditsem-types-rescore-1003`): `ActionDefinition +0x13` (element mask) has no declared type; closes with OPUS's declaration (`AUDITSPEC-REQ-OPUS-L2EXP-REPAIRS-1003`).** ~~types MET~~; ~~runtime MET 2026-09-26 — RW-5 gate, WE-3, WE-1 stage order executed; ST-1/2/6 static-ruled; step-target coverage ruled a coverage statement, not an invariant~~ **runtime MIXED (re-scored 2026-10-03, SWE2-DATA, on the exclusion amendment): the step-target bodies are the calculator slots the registry subject names; closes with their execution or a contract SCOPE-SHORT**
```

## S-23 — CITE (SWE2-DATA)

Subject: "The HP write and the lethal transition". The revive arm (page L196–199) is one status call that
clears KO "and return", executed by EXP-093's cases `revive` and `revive-smallest`
(`_experiments/evidence/hp-write-execution/check.py` L689–694). The respawn chain `00386A70` → `00301140` → the spawn
keep (`s23-opus-replay-hp-second-store` README L52) runs inside the status layer. The page cites `00301140` only in its
Status_Periodic_Terminal crossing (L549), as the status layer's body. The twelve callees, `00469BB0` (lethal step 1,
page L216 and L239) among them, ran as shipped code under EXP-093 (contract §13a: "all twelve real, 64 bodies, 64/64
cases"). **CITE.**

**Proposed runtime cell (full replacement text):**

```text
**MET — re-scored 2026-09-26 (SWE2-AUDIT-SEM) on `AUDITSEM-REQ-OPUS-407`: `ey.py` (7/7, identical ×2, reproduced md5 `b131fd68`; block-334 cases run first) executes EY-4's variant selection stub-free — the source unit's target-buffer `entryFlags` bit 8 for the target (key `+0x10`, `00316D70` on source `+0x778`) selects alive `0x2005`/`0x2006` and dead `0x2008`/`0x2007` (the §9 inversion), no entry → variant 0, call-flags bit 8 → `0x200E` — and EY-1's Bubble cap doubling (bit 28: 480+400→500 stored, 480+900→1000 with cap raised) with the presentation calls `0028F1F0`/`003283D0` run as shipped. With block 334 the HP-write contract's §4 is fully stub-free; the twelve callees (incl. `00469BB0`) already ran real under EXP-093 and are outside this contract's subject (§13); the revive-respawn chain is callee-depth. Every named runtime invariant covered** **Exclusions named under the exclusion amendment (L2-VERDICTS "Amendment — an exclusion may not drop registry-subject material", OPUS, 2026-10-03); re-read 2026-10-03 by SWE2-DATA, independent hand, request `OPUS-REQ-DATA-RUNTIME-EXCLUSIONS-C9-1003`, record `swe2data-c9-exclusions-1003`:** (1) The revive path's respawn chain (`00386A70` → `00301140` → the spawn keep) is outside the registry subject ("The HP write and the lethal transition"). The page's revive arm is the one status call that clears KO "and return" (`0030075C`–`0030077A`, executed by EXP-093's cases `revive` and `revive-smallest`), and the page cites `00301140` only in its Status_Periodic_Terminal crossing, as the status layer's recovery body. (2) The twelve callees are not excluded: `00469BB0`, lethal step 1, is named by the page, and EXP-093 ran all twelve as shipped code (contract §13a). Live capture is a tier, not subject material.
```

## S-26 — RE-SCORE (SWE2-DATA)

Subject: "The status write and the two-layer effect model". The two-layer page §12 table (L363) gives
effect **39** (`+0x6C` / `+0x7C`, mask `0x80`) as "**pins MP to zero** — the capacity becomes 0, so no path can raise
the value", and L366 adds "Every one is tested as `(layer0[k] & m) || (layer1[k] & m)`". The cell says "L-1's read side rests
static: the id-39 reads at `0031050B`/`00310541` that zero the MP and `+0x06` clamp bounds ran only on the not-taken
path". That is executable behaviour the subject page names, without evidence. The recovery tail is not named: the
status-write page's terminal table (L248) names the call "removing → `BattleUnit_RecoverFromTerminalStatusSetIfClear`
(`00301140`)", which `row3.py` E4 enters, and nothing on either page describes `00301140`'s body. Rewards `00312280`
is entered (E2). What it credits, the page's crossing (L717) files to Rewards_Progression_Economy.
**RE-SCORE MIXED; L2 NOT MET.**

**Proposed runtime cell (full replacement text):**

```text
~~**MET — re-worded 2026-10-03 (SWE2-DATA, independent hand; `AUDITSPEC-REQ-SWE2-DATA-L2EXP-REPAIRS-1003`, record `swe2data-l2exp-repairs-1003`), named coverage:** The section 10 row 3 exception and the KO chain are executed stub-free (`row3.py`, block 345). L-1 as corrected on 2026-09-29 ('never WRITES the mutable layer') is executed and asserted (`s26-opus-replay-effect-layers` `L1_rebuild_never_writes_the_mutable_layer`: every write lands in `+0x78` through `0030E130` mode 3). L-1's read side rests static: the id-39 reads at `0031050B`/`00310541` that zero the MP and `+0x06` clamp bounds ran only on the not-taken path (the planted layer holds ids 2 and 16). Unexecuted, and named: the recovery tail past `BattleUnit_RefreshActorRuntimeFromDefinition` `00238BF0` and the credit effects. Superseded:~~ ~~**MET — re-scored 2026-09-26 (SWE2-AUDIT-SEM) on `AUDITSEM-REQ-OPUS-419`: `s26-opus-replay-status-write/row3.py` (5/5, identical twice, reproduced md5 `677c0267`; block-345 cases first, `49662471` unchanged) runs the §10-row-3 exception stub-free over a world with real owning units — the band is byte-exact at `0030E467`-`0030E49C`: `movzx byte[unit+5]`/`test`/`jne` (kind == 0), `movzx byte[unit+4]`/`sub al,0x1B`/`cmp al,0xC`/`ja` (type in `0x1B`-`0x27`, the 13 Esper rows 27-39), `test edi,0x80000003` (terminal), then `call 00300FC0` at `0030E497` and `jmp` out before any mask write. E1 Esper rows: defeat cleanup only, masks untouched; E2 non-Esper terminal: the full KO chain reaction `003284D0` - defeat `00300FC0` - rewards `00312280` with the KO bit in `+0x64`; E3 non-terminal on an Esper row writes plainly; E4 removing KO clears the bit then enters recovery `00301140`, which stops at `BattleUnit_RefreshActorRuntimeFromDefinition` `00238BF0` — a recorded fixture boundary (the unit's actor runtime is zeroed, not built). Every contract-named leaf is now entered with real code; the remaining depth (`003299B0`, recovery past `00238BF0`) is callee-depth inside those leaves, not a named invariant — the S-23 precedent. Disclosed: the recovery tail and credit effects are unexecuted beyond the fixture boundary; live capture remains outside the L2 denominator**~~ **MIXED — re-scored 2026-10-03 (SWE2-DATA, independent hand, on the exclusion amendment (L2-VERDICTS "Amendment — an exclusion may not drop registry-subject material", OPUS, 2026-10-03); request `OPUS-REQ-DATA-RUNTIME-EXCLUSIONS-C9-1003`, record `swe2data-c9-exclusions-1003`): the registry subject is "The status write and the two-layer effect model", and the two-layer page names the effect this cell left static: its §12 row for effect id 39 (`+0x6C` / `+0x7C`, mask `0x80`) "pins MP to zero — the capacity becomes 0", tested on either layer. The rebuild's id-39 reads at `0031050B`/`00310541` ran only on the not-taken path (the planted layer holds ids 2 and 16). So the MP pin and the `+0x06` clamp bound carry no runtime evidence, and no contract cell records a SCOPE-SHORT for them. Outside the subject, and named: the recovery tail past `BattleUnit_RefreshActorRuntimeFromDefinition` `00238BF0` (the status-write page names only the call, removing → `BattleUnit_RecoverFromTerminalStatusSetIfClear` (`00301140`), which is entered), and the credit effects, read here as what the entered rewards call `00312280` credits (the page's Rewards crossing files that work to Rewards_Progression_Economy). Live capture is a tier. Executed and kept: the section 10 row 3 exception and the KO chain (`row3.py`, block 345), and L-1's write side (`L1_rebuild_never_writes_the_mutable_layer`). Restored to MET by a run with id 39 planted in either layer that observes the MP capacity and the `+0x06` bound go to zero.**
```

**Proposed L2 cell:**

```text
~~**MET**~~ **NOT MET — the runtime cell is MIXED (re-scored 2026-10-03, SWE2-DATA, independent hand, on the exclusion amendment; record `swe2data-c9-exclusions-1003`): the id-39 MP pin the two-layer page names rests static**
```

**Proposed binding-gap cell:**

```text
types MET (2026-09-25 census sweep); ~~runtime MIXED — status-write invariants 1-5 stub-free; residual: invariant-2 §10-row-3 defeat-cleanup exception (00300FC0, needs an owning unit)~~ ~~**reconciled 2026-09-29 (SWE2-AUDIT-SEM, FABLE-NOTICE-AUDITSEM-S26-VERDICT-RESIDUE): runtime MET — `row3.py` E1/E2 did execute `00300FC0` over real owning units (band byte-verified `0030E467`–`0030E49C`); the residual is the disclosed fixture boundary only — recovery tail past `00238BF0` unexecuted, live capture outside the L2 denominator**~~ **runtime MIXED (re-scored 2026-10-03, SWE2-DATA, on the exclusion amendment): the id-39 MP pin the two-layer page names (`0031050B`/`00310541`, taken path) is unexecuted**
```

## S-36 — RE-SCORE (SWE2-DATA)

Subject: "The widget object model, its message protocol and the request router". The router page's §8
Evidence has the rows "Triangle -> request 2 | exact disassembly in `00253C70`" and "Decide/Square -> request 1 |
`00253C70` tests `01E0C2A0 \| 0x8000`" (L674–675). Its C-4 answer (L456–462) gives request 2 with parameter `0x21`,
posted at `00253EE6` and `00253F53` inside `InputGameplay_ArbitrateDigitalInputAndModalState`. The cell says "the
arbiter is never reached" under the device gate. No `_experiments` record cites `00253C70` (grep). R-4's arbiter half
is a contract invariant (L292–300) in the same unreached body. **RE-SCORE MIXED; L2 already NOT MET.**

**Proposed runtime cell (full replacement text):**

```text
~~**MET — re-scored 2026-09-26 (SWE2-AUDIT-SEM, `AUDITSEM-REQ-OPUS-428`): `s36-opus-replay-arbiter-input-gate` (6/6, md5 `8a85be46`, reproduced) runs the whole input stack on shipped code — CRT pre-C init `00808D4C`, app object `001C1940`, input manager `00198750` (fresh-install OS model, default bindings), channel layer `003692D0`, an XInput controller built as `00797690` builds one (disclosed models: OS answers, wide-stream fails closed, DirectInput descriptor, pad = START held). Measured: device poll `007A2140` → START decoded into `+0x445` → backend table → binding translation → channel history → snapshot — all stub-free. R-4's arbiter half is device-gated (the named residual discharged): the app frame's first-frame initialiser `007A05D0` (vtable `+0x48` call at `0079C1F1` byte-verified) returns `0x15` on the renderer's back-buffer resize, so `0079C140` leaves at `0079C1F6`, `0079D010` is never entered (sole caller `0079C260` verified), the per-code words stay 0, and the arbiter is never reached — past that it would also exit at `00253D19` (manager slots not ready, disclosed). The input-script writer family is dead in this build (`[02EA5220]` has one read and no writer image-wide); the snapshot band's only producer is `002498B0`. Prior cells stand: R-1/2/3/6 + R-4's router half and the `02092734` census (3R/3W byte-exact) executed under `dfbdc1d9`; widget ctor stub-free**~~ **MIXED — re-scored 2026-10-03 (SWE2-DATA, independent hand, on the exclusion amendment (L2-VERDICTS "Amendment — an exclusion may not drop registry-subject material", OPUS, 2026-10-03); request `OPUS-REQ-DATA-RUNTIME-EXCLUSIONS-C9-1003`, record `swe2data-c9-exclusions-1003`): the registry subject is "The widget object model, its message protocol and the request router", and the router page names the input arbiter's request posts as router material (§8 Evidence: "Triangle -> request 2" and "Decide/Square -> request 1", both read in `00253C70`; the C-4 answer: request 2 with parameter `0x21`, posted at `00253EE6` and `00253F53`). This cell's device-gate exclusion leaves the arbiter unreached (`0079D010` is never entered, and past it the manager-slot exit is at `00253D19`). So those posts carry no runtime evidence, and neither does R-4's arbiter half (the latch test at `00253FE3`) in the same body. No contract cell records a SCOPE-SHORT for them. Not material, and named: the input-script writer family (dead in this build: `[02EA5220]` has one read and no writer) and live capture (a tier). Executed and kept: the input stack to the snapshot (`s36-opus-replay-arbiter-input-gate`), R-1/2/3/6, R-4's router half and the `02092734` census, and the widget constructor. Restored to MET by executing the arbiter's request posts (a planted resize outcome and manager-slot readiness), or by live capture of them.**
```

**Proposed binding-gap cell:**

```text
**types PARTIAL (2026-10-03, SWE2-AUDIT-SEM, on SWE2-AUDIT-SPEC's independent finding; record `auditsem-types-rescore-1003`): the global tick `0208F570` (and the router state `0215F1A0..0215F1AB`, `020927D8`) has no declared type; closes with OPUS's declaration (`AUDITSPEC-REQ-OPUS-L2EXP-REPAIRS-1003`).** device/live residuals preserved: the arbiter's latch test `00253FE3` with real input needs the renderer resize to complete (device boundary); the manager-slot readiness gate `00265680` needs a loaded field; live capture. The corrected types note stands — category 16's concrete widget classes remain the large coverage gap (informational, not a gate item — c3 MET under the contract-state criterion) **runtime MIXED (re-scored 2026-10-03, SWE2-DATA, on the exclusion amendment): the arbiter's request posts the router page names are unexecuted behind the device gate, so they count**
```

## S-37 — RE-SCORE (SWE2-DATA)

Subject: "Text rendering and the control-code language, DynGeo drawing". The language page L270–273 says
"`002B2150` and `002A9F00` are both callers *and* callees of this function … The interpreter and the measure/emit
passes are mutually recursive, which is how a code that inserts text (a name, a number) gets that text measured and drawn
by the same machinery that is currently interpreting it." The code `.` (L222) and the code `8` (L224) insert "through the
nested measure/emit". The cell excludes the `002A9F00` emit-side re-entry as device-gated and names it a "live
residual" with no live record. EXP-215 runs `002A9F00` real on synthetic fixtures, with the render submit, glyph-quad
builder and glyph emit scripted. That is disclosed-stub tier, and the cell does not cite it. A ruling that planting the
font object is data and not the device would let EXP-215's route restore MET. **RE-SCORE MIXED; L2 NOT MET.**

**Proposed runtime cell (full replacement text):**

```text
~~**MET — re-scored 2026-09-26 (SWE2-AUDIT-SEM) on `AUDITSEM-REQ-OPUS-409` (the render-layer boundary ruling): I-4's remaining `002A9F00` emit-side re-entry is PROVABLY device-gated — `font_boundary.py` (4/4, reproduced md5 `2d671f3b`) shows the font object `[02AEE800]` is cached at `0039C2AA` (`mov qword[02AEE800],rax` byte-verified) only after the glyph sheet's render enqueue (`0017FBC0` → `001B6510` → `001BA860` command pool), and the measure `002AC2F0` calls render state `0017FD30` straight after the getter; the graphics-context getter `001B5FA0` = `mov rax,[01F811F8]; ret` byte-exact — the context exists only with a real device. Ruling: the PhyreEngine render layer is a device-side boundary OUTSIDE the NATIVE-REPLAY denominator — the same class as S-08's file/archive layer; planting the context would be planting the device. With `i4.py`'s `002B2150` half executed (interpreter↔measure↔interpreter nested to depth 4, every level returning) and I-1..I-3/I-5..I-13 covered, every replay-reachable named invariant is executed; the device-side tail is a named live residual**~~ **MIXED — re-scored 2026-10-03 (SWE2-DATA, independent hand, on the exclusion amendment (L2-VERDICTS "Amendment — an exclusion may not drop registry-subject material", OPUS, 2026-10-03); request `OPUS-REQ-DATA-RUNTIME-EXCLUSIONS-C9-1003`, record `swe2data-c9-exclusions-1003`): the registry subject is "Text rendering and the control-code language, DynGeo drawing", and the language page names the emit side of I-4 as its mechanism: "`002B2150` and `002A9F00` are both callers and callees of this function ... The interpreter and the measure/emit passes are mutually recursive, which is how a code that inserts text (a name, a number) gets that text measured and drawn by the same machinery that is currently interpreting it". The inserting codes `.` and `8` run "through the nested measure/emit". This cell excludes the `002A9F00` emit-side re-entry as device-gated, so that named half carries no stub-free or live evidence: EXP-215 runs `002A9F00` only on synthetic fixtures with scripted render boundaries, a disclosed-stub tier. No contract cell records a SCOPE-SHORT for it. Executed and kept: `i4.py`'s `002B2150` half (interpreter, measure and interpreter nested to depth 4), and I-1..I-3 and I-5..I-13. Restored to MET by executing the emit re-entry with the font object planted, if a ruling holds that planting it is planting data and not the device, or by live capture.**
```

**Proposed L2 cell:**

```text
~~**MET**~~ **NOT MET — the runtime cell is MIXED (re-scored 2026-10-03, SWE2-DATA, independent hand, on the exclusion amendment; record `swe2data-c9-exclusions-1003`): the emit-side re-entry of I-4 the language page names is device-gated and not executed**
```

**Proposed binding-gap cell:**

```text
~~runtime MET 2026-09-26 — I-4's 002B2150 half executed; the 002A9F00 emit-side re-entry is device-gated (font object exists only after the render enqueue) — named live residual, outside the replay denominator~~ **runtime MIXED (re-scored 2026-10-03, SWE2-DATA, on the exclusion amendment): the `002A9F00` emit-side re-entry is named by the language page and is unexecuted; closes with its execution or live capture**
```

## S-40 — RE-SCORE (SWE2-DATA)

Subject: "Post-processing — the Yebis effect catalogue"; its one page carries "The frame half: what the game
hands the library every post-processed frame" (L918–986). That section covers steps 3–8, the Glare and DepthofField
setters ("Both calls run in either case"), `006CC090`'s lens setting and divide by 1000, and the run call. "Which
families can run at all" (L988–1042) names `ApplyEffects`. The section bounds itself: "Static; read from the image".
In the cell, all of it sits "behind `00193DFC` and therefore behind the immediate-context test at `006FFC56` —
device-gated". No live record exists (grep of `_experiments` for `00193DA0`, `006FFC56`, `CPostEffect`: none).
**RE-SCORE MIXED; L2 NOT MET.**

**Proposed runtime cell (full replacement text):**

```text
~~**MET — re-scored 2026-09-26 (SWE2-AUDIT-SEM, `AUDITSEM-REQ-OPUS-426`): `s40-opus-replay-post-process-init` (8/8, md5 `5d726159`, reproduced) runs the frame `00193DA0` with the library's own code — allocator `02E5BDE0` built by shipped static init `00167990` (CRT init-table entry `008C44D8` byte-verified to hold `00167990`), shipped licence `00D86C00` accepted by library reader `0071CD10` through fail-closed CRT bridges. Executed: I-1's empty-object half (teardown `006CC2F0` null-guarded, returns through `00193DFC`); I-2 — route `0065E5A0`→`006CBD20`→`006DAA70(3,5,0x20001)`→`Initialize`, flags stored `+0x208`/`+0x20C` read back, feature bits 0x800/0x40000/0x4000000/0x8000000 all clear; I-5 bounded and demonstrated — a refused init (`0x80070057`, 'Device context must be immediate context.') is logged via `005CDAA0` and creation continues, then `006DB4C0`→`00708110` faults at `00708186` dereferencing null `CPostEffect+0x108`. S1 byte-verified: `+0x108` zeroed by ctor `006FF68E`, written only at `007009BB`; `+0x147` only at `00700083` under flag `0x800` (absent from `0x20001`); the setters/`ApplyEffects`/frame-run sit behind `00193DFC` and therefore behind the immediate-context test at `006FFC56` — device-gated, the same render-layer boundary as the 409 ruling, so I-1's uniqueness half, I-3's pass exclusion and I-4 remain their byte-verified static claims**~~ **MIXED — re-scored 2026-10-03 (SWE2-DATA, independent hand, on the exclusion amendment (L2-VERDICTS "Amendment — an exclusion may not drop registry-subject material", OPUS, 2026-10-03); request `OPUS-REQ-DATA-RUNTIME-EXCLUSIONS-C9-1003`, record `swe2data-c9-exclusions-1003`): the registry subject is "Post-processing — the Yebis effect catalogue", and its one page carries "The frame half: what the game hands the library every post-processed frame". That section gives the per-frame order (steps 3-8), the Glare and DepthofField setters on both branches ("Both calls run in either case"), `006CC090`'s lens setting and its divide by 1000, and the one run call per frame; the feature-flag section adds `ApplyEffects`. This cell excludes all of it as device-gated past `00193DFC` and the immediate-context test at `006FFC56`. No live record covers it (the section's own bound: "Static; read from the image"), and no contract cell records a SCOPE-SHORT for it. Executed and kept (`s40-opus-replay-post-process-init`): I-1's empty-object half, I-2's init route and flags, and I-5's refused init with creation continuing. Restored to MET by executing the frame half (a library object past `00193DFC`), or by live capture.**
```

**Proposed L2 cell:**

```text
~~**MET — re-scored 2026-09-26 (SWE2-AUDIT-SEM, `AUDITSEM-REQ-OPUS-426`): all five requirement cells pass; the licensed-library layer's named invariants are discharged — I-1/I-2/I-5 executed at NATIVE-REPLAY up to the device boundary, I-3/I-4 contract-filed static (feature bits absent from `0x20001`, both option branches call the setters), the device-gated remainder is the render-layer boundary per the 409 ruling**~~ **NOT MET — the runtime cell is MIXED (re-scored 2026-10-03, SWE2-DATA, independent hand, on the exclusion amendment; record `swe2data-c9-exclusions-1003`): the frame half the catalogue page names is device-gated and not executed**
```

**Proposed binding-gap cell:**

```text
~~device/live boundary preserved, not counted: `Initialize` with a real immediate context, the §4 setters, `ApplyEffects` and its HRESULT, and the live capture — all sit past `006FFC56`/`00193DFC`, reachable only through the device side of the render boundary~~ **runtime MIXED (re-scored 2026-10-03, SWE2-DATA, on the exclusion amendment): that frame half is named by the catalogue page, so it counts; closes with its execution or live capture**
```

## S-42 — CITE (SWE2-DATA)

Subject: "Field music selection — the area's ladder, the mode overrides, the bank file". MC-1 (contract L70,
qualified at L74: one writer, invocation count not claimed) and MC-2 (L78, the tail jump, `00379D32` per L75) are image
facts, tier 1 (L207), and falsification pass 1 reproduces both. `mc3.py` runs the loader `003EAB60` as shipped code.
**CITE.**

**Proposed runtime cell (full replacement text):**

```text
**MET — re-scored 2026-09-26 (SWE2-AUDIT-SEM): `s42-opus-replay-music-control/mc3.py` executes MC-3 stub-free over block 325's world (boot music loader `003EAB60` real; `003EAB78` publish-store to `02B5E0D0` byte-verified `mov [rip]->02B5E0D0`; kind-9 queue `0032E620`; 4/4 identical x2); MC-1/MC-2 ruled static-structure on REQ-360 (one-writer census + tail-jump reachability are image facts, not execution behaviour); MC-4..MC-8 already executed — every named runtime invariant covered** **Exclusions named under the exclusion amendment (L2-VERDICTS "Amendment — an exclusion may not drop registry-subject material", OPUS, 2026-10-03); re-read 2026-10-03 by SWE2-DATA, independent hand, request `OPUS-REQ-DATA-RUNTIME-EXCLUSIONS-C9-1003`, record `swe2data-c9-exclusions-1003`:** MC-1 (`02B5E0D0` has exactly one writer, as qualified 2026-09-27) and MC-2 (the loader is reached by a tail jump, `00379D32`) are image facts the music page states. They are counted and covered by their tier-1 census and disassembly (contract §15; falsification pass 1), not excluded; no execution can show either. The loader `003EAB60` itself runs as shipped code in `mc3.py`. Nothing the registry subject ("the area's ladder, the mode overrides, the bank file") names is outside the executed set.
```
