# Item 3 - bare-MET contract cells and N/A script/data cells (SWE2-AUDIT-SPEC helper, 2026-10-03)

Rule: 2026-09-20 scope ruling (L2-VERDICTS.md L14-22). One section per row, appended as finished.

### S-01 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "Application root and boot — the VBF mount, the startup latch, what boot fixes and loads".
- Finding A (bare contract cell). Credited contract `00-Engine-Core-Runtime/CONTRACT-boot-fixups.md` (`scope: subsystem`, `implements: what-the-engine-fixes-at-boot.md`) contracts *"fix the engine's constants before any content loads - seed the generator..., derive the frame-base constant..., allocate the memory budget"*. Two of the three title mechanisms are absent: `grep -c "0017CEB0\|113C"` on the contract = **0**.
  - VBF mount: `GameApplication` slot 2 `0017CEB0` opens `'../FFXII_TZA.vbf'` (`Application-Root/game-application.md` §2 "The archive mount (slot 2)", L57-61, L108).
  - Startup latch `+0x113C`: one writer `0017D074 mov byte [rbx+0x113c],1`, three readers `0017CCD6` (slot 4), `0017CE77` (slot 7), `0017D094` (slot 8) (same page L69-80). The latch orders slots 4/7/8 after startup — a cross-operation ordering the fixups contract leaves unstated.
- Verdict: **SCOPE-SHORT**.
- Proposed cell text: "SCOPE-SHORT — `CONTRACT-boot-fixups.md` states the boot constants only; the VBF mount (slot 2 `0017CEB0`) and the `+0x113C` startup latch (writer `0017D074`, readers `0017CCD6`/`0017CE77`/`0017D094`) are documented on `game-application.md` §2 and in no contract."
- Owner: contract cell is bare; the S-01 section is OPUS's (`### S-01 — application boot (OPUS)`) → OPUS (cell), contract author for the repair (contract or a new GameApplication contract).

### S-08 (item 3) (SWE2-AUDIT-SPEC)
- Already decided in `_index/candidates/auditspec-l2-sample-1003/README.md` (S-08 point 1): **SCOPE-SHORT** against the registry subject — the file layer (FST sizing, `002DF780`/`002DF6C0` issue, BigFile index, `0215EFF4` producer) has no contract; `CONTRACT-resource-request-queue.md` §7/§14 exclude it. OPUS to choose split-the-row vs SCOPE-SHORT. SWE2-DATA (78b17b620) left the runtime cell standing and routed the scope question to the contract column (OPUS).
- Verdict: **SCOPE-SHORT** (or REASON-SUPPLIED for a narrowed registry subject "the resource request queue" if OPUS splits the row: "subsystem contract `02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md`").
- Owner: OPUS (section `### S-08 — the resource request queue (OPUS)`).

### S-23 (item 3, both tasks) (SWE2-AUDIT-SPEC)
- Task A: contract `CONTRACT-hp-write-and-lethal-transition.md` is `scope: transition`, `level: L1`. Registry subject is exactly "The HP write and the lethal transition" — one operation (`00300530`, `00300520`), so no cross-operation invariant can be left unstated. **REASON-SUPPLIED**: "adequately covered by `08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md` — the subject is one transition (`00300530`/`00300520`); `scope: transition` is the whole system". Note the frontmatter `level: L1` / `BEHAVIORALLY UNDERSTOOD` still needs reconciling (sample SF-4c).
- Task B: **N/A-FALSE** (sample README S-23 point 5). Proposed text: "MET (linked): script-only HP floor (`005105E0` → `00239820`, store `00239832`; contract §14.1 L499-500), the `SpawnRecord.death_count` script reader `VM_SpawnEntry_GetDeathCount`, battle-message row 0x10 ("… has fallen.")".
- Owner: contract cell bare (section `### S-43, S-09, S-23, S-05 — judged by contract SUBJECT (OPUS)`) → OPUS; script/data cell bare → OPUS.

### S-49 (item 3) (SWE2-AUDIT-SPEC)
- Already REJECTED by SWE2-AUDIT-SEM (`auditsem-l2-sample-1003`, D1) and moved to L2 NOT MET by SWE2-DATA (`78b17b620`, runtime MIXED). Not re-worked here. Its contract cell (three subsystem contracts: Phyre cluster header, packed namespace, class descriptor) is bare; AUDIT-SEM finding 6 names the deserialiser as a page-only mechanism with no contract → treat as **SCOPE-SHORT pending OPUS's S-49 repairs** (`opus-s49-repairs-1003`).
- Owner: OPUS (Phyre contracts, section `### S-47 to S-50 (OPUS)`).

### S-06 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "Developer tuning console — 282 commands over the render-settings block".
- Finding A. `CONTRACT-developer-tuning-console.md`, `scope: subsystem`, `implements:` all three console pages (the 282-command page, `console-command-names.md`, and the third console page). Contract line 2: *"dispatch a developer console command id to one of 282 arms, keep three per-id tables aligned on one id space, and let an arm nudge the render-settings block the frame is about to read"*. Line 56: *"one indirect jump, `jmp r9` at `001D16AE`, through a 282-entry table … at `001D4C1C`"*. The subject (dispatch, per-id tables, render-settings writes) is the contract's own subject. The table at L2-VERDICTS L2708 already records "MET, subsystem — three per-id tables on one id space; the alignment is an invariant no single page states".
- Verdict: **REASON-SUPPLIED**.
- Proposed cell text: "subsystem contract `00-Engine-Core-Runtime/Developer-Tuning-Console/CONTRACT-developer-tuning-console.md` — implements all three console pages; the three-table alignment is stated as a cross-operation invariant".
- Owner: bare cell; scope table L2708 → OPUS.

### S-10 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "The authored expression evaluator — how an authored number gets its randomness" (one page).
- Finding A. `CONTRACT-authored-expression-evaluation.md`, `scope: subsystem`, implements the single registry page. Its I1–I7 cover operand kinds, the six operators, the scaling law `trunc(v×B−B)`, the seven-step cost, the draw count, the mode gate on `022D9138` and signedness (contract L60–104). This is the whole subject.
- Verdict: **REASON-SUPPLIED**.
- Proposed cell text: "subsystem contract `02-Resource-And-Asset-Pipeline/Authored-Expressions/CONTRACT-authored-expression-evaluation.md` — implements the system's one page; I1–I7 state the operand, operator, scaling, step-count and draw-count rules together".
- Note: AUDIT-SEM's census output names `01EF93FC` as UNDECLARED in this row's contracts (item 1 territory, not item 3).
- Owner: bare cell; section `### S-10 (OPUS)` → OPUS.

### S-12 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "Weather — the slot state model, the probability roll, the apply".
- Finding A. `03-World-Area-Field/CONTRACT-weather.md`, `scope: subsystem`, implements all three pages (slot model, probability roll, apply). §1: *"This contract specifies that whole path — decide, commit, materialise — as one operation with one set of invariants."* P-1/P-2 and I-1..I-7 (L130–180) include *"I-7 — THE APPLY IS NOT SLOT-ATOMIC … the subsystem's load-bearing invariant"*. The scope table at L2704 records "MET, subsystem — the decide/commit/materialise invariants belong to none of the three operations alone".
- Verdict: **REASON-SUPPLIED**.
- Proposed cell text: "subsystem contract `03-World-Area-Field/CONTRACT-weather.md` — implements all three weather pages; P-1/P-2, I-1..I-7 state the decide/commit/materialise ordering".
- Owner: bare cell; scope table L2704 → OPUS.

### S-03 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "Battle runtime mode ladder — who owns the party (script, area, combat, UI)" (one page).
- Finding A. `Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md`, `scope: subsystem`, implements the single page.
  - Contract line 2: *"Reduce the battle runtime to a mode 0..5, and the four authorities that set it"*.
  - Entries cover the ladder `0030D9A0`/`00377C20` and the setter pairs `00303EE0`/`00303D90`, `003135E0`/`00313550`, `003072E0`/`00307240`, `003072A0`/`00307200`.
  - §4 carries preconditions (unchecked `*(0x02EBF190)`), postconditions ("the ladder writes nothing") and an **Invariants** block.
  - §7 *"The setters' side effects, which are not symmetric"* states the cross-setter relation.
  - The existing per-system section already argues the contract cell as MET (`L2-VERDICTS.md` L1483: *"Contract — MET. `CONTRACT-battle-runtime-mode.md` is `scope: subsystem`…"*), but the table cell does not carry the reason.
- Verdict: **REASON-SUPPLIED**.
- Proposed cell text: "subsystem contract `00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md` — the ladder and all four authorities' setters, with the asymmetric setter side effects (§7)".
- Owner: bare cell; section `### S-03 (OPUS)` → OPUS.

### S-04 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "Encoded-id space and class registry — the fifteen inventory classes behind `id >> 12`, the query record" (two pages).
- Finding A. `CONTRACT-encoded-id-space-and-class-registry.md`, `scope: subsystem`. `implements:` names only page 1 (`the-encoded-id-space-and-the-query-record.md`), but the contract's subject spans both pages:
  - line 2: *"decode a 16-bit encoded id into its class and row, validate it against that class's registry descriptor, and fill a query record"*;
  - §3: *"`ItemClassDescriptor`, 0x58, static table at `01EEBCC0`, fifteen rows"*;
  - §2 L49: *"`0030B6A0` … updates fifteen registry rows"*.
  - The registry page's dispatch and descriptor table is therefore contracted by subject. `implements:` is provenance only, per OPUS's own correction at L1430ff.
  - I1–I6 (L85–109) state the cross-operation lane, domain and lifetime rules.
- Verdict: **REASON-SUPPLIED**.
- Proposed cell text: "subsystem contract `00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md` — covers both pages by subject (decode, descriptor validation at `01EEBCC0` ×15, registry init `0030B6A0`, query fill); I1–I6 are the cross-operation rules".
- Owner: bare cell; section `### S-04` (unattributed, in OPUS's sweep) → OPUS.

### S-14 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "Battle-unit construction from its definition — the two tables, the two paths, every field the installer writes".
- Finding A. `Unit-Definition/CONTRACT-battle-unit-construction.md` is `scope: subsystem` and implements the construction page. The field-map page is the receiver's layout, cited from §3.
  - The two paths: *"I1 — class 0 is party, class 1 is enemy."*
  - The two tables (§3): *"class 0 uses `q[02EBF190]+8+row*0x1C8`; class 1 uses the particular SpawnRecord's embedded stats at `spawn+0x80`"*, with I4 *"the class fixes the stats' owner and location"*.
  - Cross-operation ordering: I2 (reset precedes the master-enable rejection), I3 (a 0 return can follow identity changes), I6 (spawn init and counting share the freshness gate).
  - "Every field the installer writes" is the field-map page plus §5. The types cell (AUDIT-SEM 09-25) reads all 7 census rows FIELD.
- Verdict: **REASON-SUPPLIED**.
- Proposed cell text: "subsystem contract `04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md` — both paths (I1), both stat tables (§3, I4) and the reset/reject/freshness ordering (I2/I3/I6); the written fields are the field-map page's".
- Owner: bare cell; section `### S-14` → OPUS.

### S-15 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "The field runtime pass — how one frame drives every actor's script" (one page).
- Finding A. `04-Actor-Entity/CONTRACT-field-runtime-pass.md` is `scope: subsystem`, implements the single page, and its contract line is *"Drive one manager slot's field actors for one frame"*. §6 *"The drive loop, and the two exits that are n[ot symmetric]"* and §7 *"Four loops, three shapes"* state the cross-loop ordering. The 2026-09-20 scope table (L1256) already records *"S-15 field runtime pass | 1 | 1 | MET — scope and system coincide"*.
- Verdict: **REASON-SUPPLIED**.
- Proposed cell text: "subsystem contract `04-Actor-Entity/CONTRACT-field-runtime-pass.md` — scope and system coincide (one page, one drive loop; §6/§7 state the loop ordering)".
- Owner: bare cell → OPUS (scope table L1256).

### S-16 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "Spawn placement, the keep window and retirement" (three pages).
- Finding A. `CONTRACT-spawn-placement.md` (`scope: subsystem`) contracts only *"choose where a spawn appears relative to the party leader"*. It also carries the return-window getter/setter (I1, `SpawnKeep_SetReturnWindow` → 300 on negative).
  - Retirement is absent: `grep -c 002350C0` on the contract = 0. The page documents `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` with its gate chain and *"two opposite senses"* (`spawn-placement-and-retirement.md` §2 "Retirement — two opposite senses" L231ff, and §8d Correction 4).
  - The keep banks are absent: `grep -c 00233780` = 0. The page documents `btlKeepCharWork1/2`, 64 × 0x250 entries, and the rotation `SpawnKeep_RotatePersistenceBanksForAreaTransition` `00233780` (§2 L340ff), plus the third registry page `Spawn-Record/the-spawn-keep-entry-field-map.md`.
  - No other contract states either mechanism. `CONTRACT-group-completion-and-respawn.md` L342 states only retirement's effect on the group ledger (*"Range retirement is not a death. `002350C0` unregisters the member"*). Every other `00233780` hit is a pass-22 neighbour line.
- Verdict: **SCOPE-SHORT**.
- Proposed cell text: "SCOPE-SHORT — `CONTRACT-spawn-placement.md` states placement and the return window; range retirement (`002350C0`, two modes) and the keep-bank rotation (`00233780`, `btlKeepCharWork1/2`) are documented on `spawn-placement-and-retirement.md` §2 and the keep-entry field map, and in no contract".
- Owner: bare cell; section `### S-16 (OPUS)` → OPUS.
- Item-1 note: AUDIT-SEM's census lists `02089358` UNDECLARED in this row's contract.

### S-17 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "Group completion and respawn — the dead-member ledger and the cooldown clock" (two pages).
- Finding A. `CONTRACT-group-completion-and-respawn.md` is `scope: subsystem` and implements page 1. Its contract line (*"the dead-member checklist and the cooldown clock"*) is the registry subject verbatim. The ledger, the per-frame consume (`00307030`, gated by `00233D20`) and the clock (`elapsed = 0208D45C / (int)(scale×30) − rec->u32_0C`, L375/L439) are all stated.
- Gap: page 2 `why-the-enemies-you-killed-come-back.md` §"What a load does to the two banks and the window" (L83–113) documents how a load treats the clock's inputs, and the contract does not cite that path. Cites in the contract: `02089374` 0, `02089370` 0, `0208E698` 0, `005843E0` 0, `00237DF0` 0.
  - The raw counter `0208D45C` is zeroed on the guard-mismatch path (`0032A160` from `00237E37`) while bank-1 record stamps are kept.
  - Bank 2 and the field history are restored only on a slot-0 load.
  - That is a cross-operation interaction between the clock and the load path.
- Verdict: **SCOPE-SHORT (narrow)**. Two repairs would discharge it: bound the load interaction in contract §14, or add it as an invariant.
- Proposed cell text: "adequately covered by `05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md` — ledger, consume gate and cooldown clock — EXCEPT the clock-across-load interaction (page 2 L83–113: `0208D45C` zeroed at `00237E37`, bank 2 restored only on slot 0), which the contract neither states nor bounds".
- Owner: bare cell; section `### S-17 (OPUS)` → OPUS.

### S-21 (item 3, both tasks) (SWE2-AUDIT-SPEC)
- Subject: "Result application and post-result events — the result record, the applier, the battle message table" (three pages).
- **Task A.**
  - `07-Combat-Action/CONTRACT-apply-result-to-target.md` (`scope: subsystem`) contracts only the applier: *"apply a result record to target and source stats using field-specific presence gates and an explicit outer recompute-dirty flag"*.
  - Its §8 mentions the events in one sentence (L201): *"`00385BA0` can dispatch post-result events"*.
  - The post-result-events page documents three mechanisms that no contract states:
    - the dispatcher's two worlds (§2.2);
    - the poster `0046AB10` (371 B, *"every message in the game goes through it (48 call sites in 18 functions)"*), with *"one ring, a rate limit, a visibility filter"* (§2.3–§2.4);
    - the table `battle_message.bin` and its formatter `005369C0` (1,000 B, four argument slots from row bytes `+0/+1/+2/+5`, `00536A51`–`00536BBC`; §2.5).
  - A repo-wide grep for "battle message" across `CONTRACT-*.md` finds no contract. `0046AB10` and `005369C0` are the same bodies EXP-093 stubbed inside `00469BB0` (S-23).
- **Verdict A: SCOPE-SHORT.**
- Proposed contract-cell text: "SCOPE-SHORT — `CONTRACT-apply-result-to-target.md` states the applier and the result record. The post-result events (dispatcher `00385BA0`, poster `0046AB10` with its ring/rate-limit/filter) and the battle message table (`battle_message.bin`, formatter `005369C0`) are documented on the post-result-events page §2.2–§2.5 and in no contract."
- **Task B.**
  - `N/A stated` is false. `battle_message.bin` is an authored data file whose rows the formatter reads byte-wise (page §2.5).
  - The registry subject names the table itself.
- **Verdict B: N/A-FALSE.**
- Proposed script/data text: "MET (linked): `battle_message.bin` rows read by `005369C0` (args from row `+0/+1/+2/+5`, page §2.5); the result record is constructed upstream by the formula steps (S-22)". Whether the table's decode is censused needs the page's §5/§7 read before MET; until then **N/A → PARTIAL**.
- Owner: contract cell bare and script/data bare; section `### S-21` (unattributed, OPUS sweep) → OPUS. The contract author is FABLE (pass-22 section) / OPUS.

### S-31 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "The licence board and the licence check" (pages: the check page, `license-board-grid-format.md`).
- Finding A. `CONTRACT-license-check.md` (`scope: subsystem`) contracts the check only. Contract line 2: *"decide whether a unit is licensed for an action - three exits before any board is read, a bitmask overlap…, and a counted gate for Quickenings"*.
  - The board appears only as data. §8 L151: *"The action rows and the board grid are authored data; the grid format has its own page"*.
  - The grid page carries its own §3 "The loader contract" and §3 "The boundary — what is NOT established". Neither is in any contract.
  - The writer of the bits the check reads (`BattleStatsRecord +0x194 licenceOwnedBits`, i.e. board purchase) is stated nowhere. The contract's own L198 calls it *"a question about the board-purchase rules"*, and repo-wide grep finds no page naming a purchase writer of `+0x194`.
  - The check-side reads are byte-verified (contract §3: `byte [rbx + rax + 0x194]`, validator `00322C50` class 1..32).
- Verdict: **SCOPE-SHORT (narrow)**, or REASON-SUPPLIED if OPUS reads "the licence board" as the data format only. In that case the cell needs the reason "the grid is an input format, loader stated on its page".
- Proposed cell text: "adequately covered by `12-Items-Equipment-Shops-License/CONTRACT-license-check.md` for the check — EXCEPT the board grid loader (`license-board-grid-format.md` §3) and the purchase path that writes `licenceOwnedBits` (+0x194), which no contract states; the check reads what purchase writes, so the pair has an unstated cross-operation dependency".
- Item-1 note: AUDIT-SEM's census flags `0208E680` UNDECLARED in this row's contract.
- Owner: bare cell; section `### S-31 (OPUS)` → OPUS.

### S-33 (item 3, both tasks) (SWE2-AUDIT-SPEC)
- Subject: "World loot pickups — the ten-slot pool, the blink, the despawn" (one page).
- **Task A.** `CONTRACT-world-loot-pickup-pool.md` (`scope: subsystem`) implements the one page, and its contract line is the subject: *"hold up to ten world loot pickups in a fixed pool on one FIFO list, age them through a blink ladder, and retire each one by a single shared sequence"*.
  - **Verdict A: REASON-SUPPLIED.**
  - Proposed text: "subsystem contract `13-Rewards-Progression-Economy/CONTRACT-world-loot-pickup-pool.md` — scope and system coincide (pool, blink ladder, shared retire sequence)".
- **Task B.** Contract §8: *"None directly. The drop buffer is produced upstream; the pool neither reads authored tables nor runs script."* I found no script-VM caller or authored-table read in the pool bodies.
  - One resource dependency is real: the pickup's visual create `003FA160` fetches its two visual objects by name from the 64-slot named-image table through `0024A5A0` (page L584). The presentation verbs go through `0028F000` (op 1–5 table, page L314–320).
  - The tier byte comes from the 4-entry `.data` table `01EED3A8`, a constant, not authored content.
  - **Verdict B: N/A-HOLDS for script/authored data**, but the resource link should be recorded.
  - Proposed text: "N/A stated — the pool reads no authored table and runs no script (contract §8); resource link: the visual create `003FA160` fetches its two objects by name from the named-image table (`0024A5A0`)".
- Owner: both cells bare; section `### S-33` → OPUS.

### S-37 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "Text rendering and the control-code language, DynGeo drawing" (two pages).
- Finding A. `16-UI/CONTRACT-text-control-codes-and-dyngeo-draw.md` (`scope: subsystem`) implements both pages. Its contract line: *"interpret the control codes embedded in game text - one interpreter for both measuring and drawing, with the cursor advanced by the parser's own return - and draw the result through the dynamic-geometry…"*. The scope table (L2706) records *"MET, subsystem — the boundary is the finding — nothing joins the two halves, and saying so is the contract's most useful sentence"*.
- Verdict: **REASON-SUPPLIED**.
- Proposed cell text: "subsystem contract `16-UI/CONTRACT-text-control-codes-and-dyngeo-draw.md` — implements both pages; the measure/draw single interpreter and the stated absence of a join between the halves are the cross-operation statements".
- Owner: bare cell → OPUS (scope table L2706).

### S-39 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "The render command list and the graphics-thread handshake" (two pages).
- Finding A. `17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md` (`scope: subsystem`) implements both pages. Its contract line: *"build a frame's render jobs…, run them in two masked parts, apply the deferred settings commands, destroy them, and kick the command stream through the one shared word the graphics handshake is made of"*. The scope table (L2705) records *"MET, subsystem — the frame ordering binds the list half to the handshake half"*.
- Verdict: **REASON-SUPPLIED** for the contract cell's scope.
- The sample's REJECT stands on other grounds: the types cell (undeclared `02EBA3F8`) and the §10.1 contract-text defect (`auditspec-l2-sample-1003`). Supplying the scope reason does not clear them.
- Proposed cell text: "subsystem contract `17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md` — implements both pages; the frame ordering binds the list half to the handshake half (I-1..I-10)".
- Owner: bare cell → OPUS (scope table L2705).

### S-44 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "Game settings and locale" (pages: the settings page, `Language-And-Locale/language-selection-and-locale-ids.md`).
- Finding A. `Game-Settings-Config/CONTRACT-game-setting-config.md` (`scope: subsystem`, `RUNTIME VALIDATED`) implements the settings page: *"The GameSetting.ini configuration object — construct, load, parse, apply, serialize"*.
  - The contract covers locale at the OS mapping: L243 *"Locale mapping (`001DE0C0`, primary id = `LANGID & 0x3F`)"* feeding `setting[0]`.
  - The locale page's own mechanism is **not** contracted: §3 *"Code to id — `0017E270`, read in full"*, the three-byte code comparison that returns the internal language id the engine uses. Its downstream use (page §6 "AV-4 answered: where the id goes") is not contracted either. `grep -c 0017E270` on the contract = 0, and no `CONTRACT-*.md` cites it.
  - The confirm/cancel swap is covered only as *"`DecideButton` selects Circle vs Cross at runtime and re-applies the masks immediately"* (L274). The masks' readers (page §7) are page-only.
- Verdict: **SCOPE-SHORT (narrow)**.
- Proposed cell text: "adequately covered by `19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md` for the settings object (construct/load/parse/apply/serialize, OS locale mapping `001DE0C0`) — EXCEPT the language code-to-id conversion `0017E270` and where that id goes (locale page §3, §6), which no contract states".
- Owner: bare cell; section `### S-44 (OPUS)` → OPUS.

### S-46 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "RNG streams and which roll is on which generator" (two pages).
- Finding A. Two contracts:
  - `CONTRACT-gameplay-generators.md` (`scope: family`, implements `rng-streams.md`): *"draw from the two gameplay-affecting generators, exactly"*.
  - `CONTRACT-which-generator-serves-which-roll.md` (`scope: subsystem`, implements the routing page): *"route every gameplay roll to one of four generators and keep their streams apart - which consumer draws from which, what reseeds each"*.
  - The routing contract carries the cross-operation invariants: I1 *"TWO MERSENNE TWISTERS, DISJOINT STATE"*, I3 *"ALL LCG CONSUMERS SHARE ONE STREAM"*, I4 the LCG seed, I5 the graphics-MT state address, I6 the correlation answer.
  - The family-scoped algorithm contract has no cross-operation content left unstated, because the subsystem contract owns the routing.
- Verdict: **REASON-SUPPLIED**.
- Proposed cell text: "subsystem contract `21-RNG-And-Determinism/CONTRACT-which-generator-serves-which-roll.md` (routing and stream separation, I1–I6) with `CONTRACT-gameplay-generators.md` adequately covering the per-generator algorithms — scope family is sufficient because every cross-generator invariant is in the routing contract".
- Owner: bare cell; section `### S-46 (OPUS)` → OPUS.

### S-50 (item 3) (SWE2-AUDIT-SPEC)
- Subject: "Lua core loader surface — the chunk loader and what it accepts" (one page).
- Finding A. `23-Third-Party-Libraries/Lua-Core/CONTRACT-lua-chunk-loader.md` (`scope: subsystem`) implements the one page: *"The Lua chunk loader — accept a buffer, fork on its first byte, produce a callable chunk"*. §1: *"`0x1B` runs the bytecode reader, anything else runs the full Lua source parser"*. §7 is "State transitions — the fork, with its compi[ler]". The subject is the contract's subject.
- Verdict: **REASON-SUPPLIED**.
- Proposed cell text: "subsystem contract `23-Third-Party-Libraries/Lua-Core/CONTRACT-lua-chunk-loader.md` — scope and system coincide (the first-byte fork, both readers, chunk production)".
- Owner: bare cell; section `### S-47 to S-50 (OPUS)` → OPUS.

### S-02 (item 3, task B) (SWE2-AUDIT-SPEC)
- Subject: "The world tick and the field frame — the per-frame order on the battle layer and the one-word update gate".
- Already found false by SWE2-AUDIT-SEM (`auditsem-l2-sample-1003` S-02 point 5). The links:
  - script verbs raise stop ids (`talkfadeout`, `settimestopmagic`, `maskopen`, `ucon`, `skipexec`; system-stop registry page §6 L235–262);
  - options bit 3 selects id 0's raiser (SM-5);
  - `skipexec`/`skipend` set the `+0x201` opt-in (`fields.tsv:100`).
- Not re-derived here; adopted with pointer.
- Verdict: **N/A-FALSE**.
- Proposed text (AUDIT-SEM's): "MET — linked, not N/A (stop-raising verbs, options bit 3, the `skipexec`/`skipend` opt-in)".
- Owner: bare cell → OPUS (section `### S-02 (OPUS)`). The row is now L2 NOT MET on runtime (SWE2-DATA `78b17b620`).

### S-05 (item 3, task B) (SWE2-AUDIT-SPEC)
- Subject: "Shared transform workbench — the matrix area four subsystems pass arguments through".
- All three credited contracts' §8 deny authored or script input, consistently:
  - `CONTRACT-transform-workbench-save-restore.md`: *"None."*
  - `CONTRACT-transform-primitives.md`: *"No script opcode reaches either directly, neither touches a resource, and neither raises an event. They are arithmetic the rest of the engine calls."*
  - `CONTRACT-shared-transform-workbench.md`: *"None. Nothing authored reaches this area."*
- The subject is a scratch matrix region and its arithmetic, so no authored-data or script dependence is plausible.
- Verdict: **N/A-HOLDS**.
- Proposed text: "N/A stated — a scratch matrix area and transform arithmetic; no authored table, script opcode or resource reaches it (all three contracts' §8)".
- Owner: bare cell → OPUS.

### S-18 (item 3, task B) (SWE2-AUDIT-SPEC)
- Subject: "Locomotion and steering — heading and speed to position, facing, movement mode, battle locomotion".
- The contracts' §8 each say "None directly", but the system is script- and data-driven:
  - **Script verbs drive steering.** `how-a-character-turns.md` L163–167: *"`VM_ActorSteerToPosition` (`00357A20`) and `VM_ActorSteerTowardActor` (`00357980`), and every `begin` handler of the move family ends in one of them — `move` / `rmove` / `cmove` / `rcmove` / `amove` / `ramove` / `ucmove` … (`0x003E`–`0x0045`, `0x0059`–`0x0060` …)"*.
  - **Authored speed.** `heading-speed-to-position-delta.md` L370–375: `Movement_SetRequestedSpeedScaled(actor, authored)` is *"the only place a global scalar touches authored speed"*.
  - **Authored model data.** `battle-locomotion-steering-and-recovery.md` L277–281: `locomotionFlags` bit 2 = the model's `@FCP` section-9 slot-41 dword, *"authored per model, non-zero in 360 of 723 files"*.
  - **Authored area records.** L773ff: the wander index is *"a POSENT record number — the area's authored position entries"* (EBP section 016).
- Verdict: **N/A-FALSE**.
- Proposed text: "MET (linked): the script move family (`0x003E`–`0x0045`, `0x0059`–`0x0060`) ends in `VM_ActorSteerToPosition` `00357A20` / `VM_ActorSteerTowardActor` `00357980`; authored speed via `Movement_SetRequestedSpeedScaled`; `@FCP` section-9 slot 41 (360/723 models) sets `locomotionFlags` bit 2; battle wander indexes POSENT records (EBP section 016)". Whether each link is censused is the cell scorer's check.
- Owner: bare cell → OPUS (section `### S-15, S-18, S-34, S-41 (OPUS)`).

### S-19 (item 3, task B) (SWE2-AUDIT-SPEC)
- Subject: "The movement body pool and the separation pass".
- Both contracts' §8 say "None", but script verbs read and write the body/cell attributes this system keys on (`the-movement-body-pool-and-the-separation-pass.md` L293–295):
  - Body `+0x86` (attribute bits 13..17) is read by `002E9890` for the verb `getmapid_48b` (handler `00347240`).
  - Body `+0x8A` is read by `002E9830` for `getmapgroundtype_48c` (handler `003476B0`).
  - The mask table at `0209A3E0`, indexed by the placement `003808A0` through `0x40 + ((attr>>3)&0xF)`, is filled only by the script's override verbs `setmapidmj` / `setmapidmj_103` / `setmapidmjground` / `resetmapidmj*` (writer `0026E880`; `00379430` adds 0x40).
  - The cell attributes come from the authored navimap.
- Verdict: **N/A-FALSE**.
- Proposed text: "MET (linked): script override verbs `setmapidmj*`/`resetmapidmj*` fill the `0209A3E0` mask table the placement `003808A0` indexes; `getmapid_48b`/`getmapgroundtype_48c` read body `+0x86`/`+0x8A`; cell attributes come from the authored navimap (S-11/S-51)".
- Owner: bare cell → OPUS.

### S-20 (item 3, task B) (SWE2-AUDIT-SPEC)
- Subject: "Command commit and action dispatch — the moment an action is committed, the native command seam, the handler table, availability and reason codes, combos".
- The S-20 contracts' own §8 contradict "N/A":
  - `CONTRACT-native-command-seam.md` §8: *"Script commands reach the funnel as issued commands, through the same seam as human and guest input (`CS-1`)."*
  - `CONTRACT-the-moment-an-action-is-committed.md` §8: *"Script commands arrive here as issued commands through the seam."*
  - `CONTRACT-battle-target-buffer.md` §8 (corrected 2026-10-02, OPUS): *"a script verb body reaches it — `003495A0` calls `00313120` (`003495B2`), which resets the buffer and appends to it at `0031325F` / `0031328C`"*.
  - `CONTRACT-battle-action-handler-table.md` §8: presentation events `0x2001`/`0x2010` are posted.
  - Action rows are authored data (the action definition rows read for availability and costs; see S-22's `ActionDefinition` finding).
- Verdict: **N/A-FALSE**.
- Proposed text: "MET (linked): script commands enter through the native command seam (CS-1) like human and guest input; script verb `003495A0` → `00313120` resets and fills the target buffer; the handler table posts `0x2001`/`0x2010`; availability reads the authored action rows". The action-row read needs the row type declared first (S-22 repair).
- Owner: bare cell → OPUS (section `### S-20`, the 2026-09-20 page-coverage analysis is OPUS's).

### S-38 (item 3, task B) (SWE2-AUDIT-SPEC)
- Subject: "Character rendering — the render object, the render record array, transform publish, the coast-down latch".
- The contracts' bodies read no authored table directly. But `CONTRACT-coast-down-latch.md` §8 (corrected 2026-09-27, OPUS) states the subtype it compares *"is the render record's current event, stored by `00424D80` (`00424FAB`) from posted events - posted by the engine (`0x200D`, `0x2010`, `0x4035`/`0x4036`) or by script verbs. What is authored is the motion each character's `.ca` holds at that slot."*
- `CONTRACT-character-render-object.md` §8: *"the object's contents come from the record array and material list it holds, which other systems fill"*. That is a resource dependency (the model/material resources).
- Verdict: **N/A-FALSE (linked through events and resources, not direct reads)**.
- Proposed text: "MET (linked): the coast-down latch compares the render record's event (`+0x0CC`, stored by `00424D80`) which script verbs as well as the engine post; the motion at each slot is authored in the character's `.ca`; the render object's records and materials are filled from loaded model resources".
- Owner: bare cell → OPUS.

## Summary (item 3) (SWE2-AUDIT-SPEC)

### Task A — 21 bare-MET contract cells (SWE2-AUDIT-SPEC)

| row | verdict | short reason |
|---|---|---|
| S-01 | **SCOPE-SHORT** | VBF mount `0017CEB0` and startup latch `+0x113C` are in no contract |
| S-03 | REASON-SUPPLIED | subsystem contract, ladder and all four setters |
| S-04 | REASON-SUPPLIED | subsystem contract covers both pages by subject |
| S-06 | REASON-SUPPLIED | subsystem contract implements all three console pages |
| S-08 | **SCOPE-SHORT** | file layer uncontracted (sample) |
| S-10 | REASON-SUPPLIED | one page, subsystem contract |
| S-12 | REASON-SUPPLIED | subsystem contract implements all three pages |
| S-14 | REASON-SUPPLIED | both paths and both tables in the subsystem contract |
| S-15 | REASON-SUPPLIED | scope and system coincide (L1256) |
| S-16 | **SCOPE-SHORT** | retirement `002350C0` and keep-bank rotation `00233780` uncontracted |
| S-17 | **SCOPE-SHORT (narrow)** | clock-across-load interaction (page 2 L83–113) unstated |
| S-21 | **SCOPE-SHORT** | post-result events, poster `0046AB10` and `battle_message.bin`/`005369C0` uncontracted |
| S-23 | REASON-SUPPLIED | one transition = whole subject (contract still `level: L1`) |
| S-31 | **SCOPE-SHORT (narrow)** | board grid loader and the `licenceOwnedBits` purchase writer uncontracted |
| S-33 | REASON-SUPPLIED | scope and system coincide |
| S-37 | REASON-SUPPLIED | subsystem contract implements both pages (L2706) |
| S-39 | REASON-SUPPLIED (scope only) | L2705; sample REJECT stands on types and §10.1 |
| S-44 | **SCOPE-SHORT (narrow)** | language code→id `0017E270` uncontracted |
| S-46 | REASON-SUPPLIED | routing subsystem contract carries every cross-generator invariant |
| S-49 | SCOPE-SHORT pending OPUS repairs | AUDIT-SEM REJECT; deserialiser uncontracted; now NOT MET |
| S-50 | REASON-SUPPLIED | scope and system coincide |

Totals: **13 REASON-SUPPLIED, 8 SCOPE-SHORT**. Of the 8, 4 are full (S-01, S-08, S-16, S-21), 3 are narrow (S-17, S-31, S-44), and 1 is pending (S-49).

### Task B — 9 `N/A stated` script/data cells (SWE2-AUDIT-SPEC)

| row | verdict | short reason |
|---|---|---|
| S-02 | **N/A-FALSE** | stop-raising verbs, options bit 3, `skipexec` opt-in (AUDIT-SEM) |
| S-05 | N/A-HOLDS | scratch matrix arithmetic; three contracts agree |
| S-18 | **N/A-FALSE** | script move family → `00357A20`/`00357980`; authored speed; `@FCP` slot 41; POSENT |
| S-19 | **N/A-FALSE** | `setmapidmj*` verbs fill `0209A3E0`; `getmapid`/`getmapgroundtype` read body fields |
| S-20 | **N/A-FALSE** | script commands via the seam (CS-1); verb `003495A0` fills the target buffer |
| S-21 | **N/A-FALSE** | `battle_message.bin` rows read by `005369C0` |
| S-23 | **N/A-FALSE** | script-only HP floor `005105E0`→`00239820`; `death_count` reader; message 0x10 |
| S-33 | N/A-HOLDS (+ resource link) | pool reads no authored table and runs no script; visual fetch `0024A5A0` |
| S-38 | **N/A-FALSE** | latch compares script-posted events; `.ca` motions; model resources |

Totals: **7 N/A-FALSE, 2 N/A-HOLDS**.

### Owner (SWE2-AUDIT-SPEC)

Every one of these 30 cells is bare (no scorer named in the cell). The per-system sections that produced them are OPUS's, so every repair routes to **OPUS** (verdict table). The contract repairs for the SCOPE-SHORT rows go to each contract's author.
