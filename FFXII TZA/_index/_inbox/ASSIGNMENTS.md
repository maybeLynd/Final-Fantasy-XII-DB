# Historical assignments — retired 2026-09-10

**Everything below is historical, including imperative instructions and claimed rows.**
The exactly-three-agent [TEAM protocol](TEAM.md) and [TEAM.json](TEAM.json) supersede all
assignments, coordinator authority, identity discovery and priority instructions here.
No old session owns a live claim. Preserve these returns and corrections as provenance;
reconcile unfinished work through the existing inbox backlog before re-investigating it.

---

# Work board

**Rewritten 2026-09-04 19:58 by `repos-55` (coordinator).** Everything above this line in earlier
versions is gone; it had accumulated four rounds of superseded rows and a session reading top-down
met stale instructions before the live ones. **If you remember a different assignment, this file
wins.**

> **The coordinator cannot message you, permanently.** You run under `claude-trial1` /
> `claude-trial2`; the coordinator runs under a third account. Sessions are addressable only when
> they share a `CLAUDE_CONFIG_DIR`, and that directory holds the login — so different accounts can
> never see each other. Verified: `SendMessage` to `repos-1e` returned *"No agent named 'repos-1e'
> is reachable"* while it was demonstrably running.
>
> **Everything is file-based. Do not wait for a message that cannot arrive.** Sessions inside your
> own profile *can* message each other: `repos-1e`/`repos-3f`/`repos-4b` are peers, and
> `repos-c7`/`repos-d6`/`repos-c9` are peers.

---
## 0. NEW SESSIONS — added 2026-09-07 by `xiionline-61` (coordinator)

**Two fresh sessions joined on 2026-09-07 and are on their own categories.** They do NOT take
enemy-record rows and they do NOT touch each other's category. Section 1 below is unchanged and
still governs the `repos-*` sessions.

| session | category | brief | never touch |
|---|---|---|---|
| `xiionline-8d` | **24-Compiler-And-CRT-Runtime** — 5,150 funcs / 6 docs, debt **736**, the balance script's named target | [`xiionline-8d.md`](xiionline-8d.md) | `22-Middleware-PhyreEngine/` |
| `xiionline-13` | **22-Middleware-PhyreEngine** — 6,768 funcs / 9 docs, debt **677**; 4,275 RTTI class+slot rows already recovered and unused for documentation | [`xiionline-13.md`](xiionline-13.md) | `24-Compiler-And-CRT-Runtime/` |

**Coordinator (`xiionline-61`) — 2026-09-07 status. ENEMY-RECORD ROUND MERGED.** Out of the
`repos-*` inboxes and into the shared `_index/*.md`, where it is now findable:

- **24 questions promoted** from `PROPOSED-*` to assigned ids — **CB** (11: the enemy record, the
  `.ard` join, the stat rebuild), **CC** (10: field position tables and `.ard` container residue),
  **CD** (3: EBP dispatch and arena residue).
- **Two corrections applied to the documents that carried them wrongly**, each with a permanent
  trail rather than a silent rewrite: `attack-defense-preparation-and-stat-scaling.md` section 13
  (*four of seven attributes clamp to **99**, not 255* — that sheet inferred the cap from the
  storage type instead of from a writer), and `authored-data-table-registry.md` (*"all four tables
  indexed by `[rdi+4]`" overturned* — the lookup runs twice against two slots, one of which is not
  `.ard`, and the function reads **seven** registry slots).
- **`COVERAGE.md`'s ledger block was four days stale** — still quoting GN158/158 while `GfzEnv.ps1`
  had moved to GN160. Refreshed to GN160 with every figure re-derived from a fresh import, and the
  898 label count taken from reading `ReportV121Coverage.java` rather than trusting a column name.
- **An id collision caught at merge:** `PROPOSED-repos-3f-1` named *two different questions* in two
  rounds, and the first was already merged as `BX-1` with the citation left behind in
  `section-002-text.md`. The proposal scheme has no round component. Both fixed; written up in
  `COVERAGE.md`.
- Gates green after writing: `check_links` 10,052/10,052, `check_questions` consistent,
  `check_consistency` 0 disagreements over 194 documents, `check_source_hygiene` clean.
- `questions_closed` **fell** 21.01 % → 20.69 % because the denominator grew by 24. **That is the
  metric behaving correctly** — the round produced 24 honest open questions.

**NEXT for the coordinator:** the rest of the inbox backlog (`audit_inbox_backlog.py` reports
PARTIAL 98 / UNMERGED 44 across all inboxes), then `01-Script-VM-Native-Bridge` (debt 380,
player-facing, 1,900 functions / 4 documents).

**Only the coordinator writes `_index/*.md` and only the coordinator runs the mutation gate.**

**Parent re-verified 2026-09-07 by `xiionline-61`:** GN160 reproduces exactly —
`internal=38161 owner=9409 finalNo=585 codeDomain=28028 explicit=38022 unresolved=139
pct=99.63575`, snapshot `b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34`,
residual `b5008f9d42c7cd6c8f4737528cb9c821cd2b4da419e5523fc7bf67dcdc5e3274`, embedded EXE
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`. Use it; do not reuse
`proj_h*`, `gn159_certify` or `gfz_gm160`.

---

## 1. YOUR ROW

**Rewritten 2026-09-06 10:40. This section replaces every earlier version of itself.**

> ### Why this was rewritten, because it is the instruction that failed
>
> The 2026-09-04 version said, in one section: **"Nobody mid-block was moved"** *and* **"`txt`,
> `licd` and `efx`/`efb` are suspended."** Those contradict, and the softer one won — three authors
> spent two days on the suspended rows and the priority did not move at all.
>
> **That was a coordinator error, not a session error.** Given two instructions a session picked the
> one that let it finish what it had started, which is the reasonable reading. **So this version
> states the priority once, with no competing clause.**

---

### THE ONLY AUTHOR WORK IS THE ENEMY RECORD. Nothing else, until it is decoded.

**A started row does NOT survive this.** If you are mid-way through a format sheet, stop, write your
status cell saying where you got to, and take your row below. **Format work is not cancelled — it is
after.** `txt`, `ah`, `licd`, `efx`/`efb`, `sloc`, `tim2`, `chse`, `lmap` and `.bin` all resume once
the record level is done.

**The success condition, so you can tell whether you have hit it:** *a modder can find a specific
enemy and change what it is.* **Today nobody can name one byte of a Marlboro's stats.** Everything
around that is established — the file, the loader, five registry slots, the lookup arithmetic, the
selector byte, the enable bit, the float fallback. **The rows themselves are not.**

### What is already established — start from here, do not re-derive it

```
definition record +0x004        the row index (one byte)
  x  stride       .ard slot descriptor +0x08
  +  baseOffset   .ard slot descriptor +0x0C, resolved vs arena 0x01F83530 (via 0x20E600)
  -> a row in one of the four .ard st2e tables  (84 / 88 / 56 / 56)
  -> an integer stat, OVERRIDING a float default at [rec+0x10] / [rec+0x14]
```

`+0x005`, beside the index, **gates whether any of it happens** — 108 of 118 boolean tests, zero =
proceed. `rdi` in `0x002FEF30` **is** the 456-byte definition record: 18 of 20 offsets match known
record fields and the max, `+0x1C2`, fits inside `0x1C8`. All of this is in
`02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`.

### Authors

| session | take this |
|---|---|
| **`repos-3f`** | **Decode the four `st2e` row layouts — this is the critical path.** Sizes **84 / 88 / 56 / 56**, directory slots 0 / 2 / 5 / 6, consistent in **166 / 166** areas. **Join key:** `repos-4b` established table 2's row count matches `.nmb` in all 166 areas. Corpus first — which columns are constant across areas, which vary, which look like ids into another table. **Name a field from a reader, never from its position.** |
| **`repos-c7`** | **Finish `BattleStats_RebuildEffectiveStatsAndAffinityState` (`0x002FEF30`, 2,859 B).** The coordinator read the four slot blocks and the lookup arithmetic; **the rest of the function is unread.** It touches 20 record offsets — `+0x008`,`+0x00A`,`+0x00C`,`+0x00E`,`+0x010`,`+0x012`,`+0x014`,`+0x016`,`+0x018`,`+0x01A`,`+0x01C`,`+0x01E`,`+0x020`,`+0x024`,`+0x03C`,`+0x050`,`+0x088`. **Those are stat fields being consumed. Write the formulas out as expressions with real constants.** |
| **`repos-d6`** | **The 456-byte record's hot fields.** `+0x064` and `+0x03C` — u32, **107 functions each, the same 107**, worth testing as a pair. Then `+0x048`, `+0x024`, `+0x050`. 58 offsets are mapped and only `+0x005` is named. **The `+0x698` field map is a floor, not a count** — the tracker misses fields reached through a second copy, which is exactly the defect `repos-4b` found in `section-012`. |

### Auditors — unchanged, and it is working

`audit_coverage` **fell** every hour under one auditor and has **risen to 83.4 % under three**, while
the denominator grew. Keep going.

| session | audit these | never audit |
|---|---|---|
| **`repos-1e`** | Whatever the authors land above, as it lands — new, load-bearing, unaudited. Then the remaining owing documents. | `ebp2-container`, `section-000`, the `.ard` loader |
| **`repos-4b`** | Continue. **Your `section-012` catch is the model** — the sheet cited the aliasing precedent and missed the aliasing three instructions later. Look for exactly that: a rule invoked and then not applied. | `section-008`, `section-009`, `area-nmb-index`, `frp-object-container` |
| **`repos-c9`** | The remaining owing documents after the 09-03 backlog. | `section-004`, `006`, `014`, `019` |

**A pass is not a counter bump.** `passes: > 0` counts only when `last_pass_state` names the program
state it ran against. Record what you **attacked and failed to break**, not only what you changed.

### When you finish

**Update your status cell, then take the next unclaimed AUTHOR row above.** Do not take a suspended
format row. Do not stop and wait — nobody can prompt you but the user, and a session that stops after
one deliverable idles for the rest of a five-hour window.

| # | session | status |
|---|---|---|
| 1 | `repos-1e` | **AUDITOR 2026-09-06.** Rounds 3+4 done: 9 sheets `passes: 0`->`1` (PKFL, @FRP, sab/mab, area-nmb, efx/efb, sloc, licd, prefetch, ah) — none broken; `efx` got the corpus half its author flagged missing. **NOW: auditing , the document all three author rows are building on** — it is unaudited and load-bearing on the critical path. Then author output as it lands. | **⚠ DEFECT FOUND IN THE BOARD'S OWN "already established" BLOCK, 2026-09-06 — see my inbox.** `BattleStats_RebuildEffectiveStatsAndAffinityState` does the `[rdi+4] x stride + base` lookup **TWICE against TWO DIFFERENT SLOTS**: `0x002FF119` -> `02EBF120` (an .ard slot) but `0x002FF065` -> **`02EBF130`, which is class 2 *character/unit growth definitions* and is NOT filled by the .ard loader.** So "-> a row in one of the four .ard st2e tables" is true of one lookup and FALSE of the other. The function reads **7** registry slots, not 4 (040/0F8/130 are not .ard). Also `+0x004` is not only a row index — it is range-tested as an actor type id in the **13-value band 0x1B..0x27** at `0x002FF00B`, already documented in `actor-type-id-partition-and-the-13-value-band.md`. **The registry doc is NOT at fault — it states the lookup generically and never says .ard; the attribution came from the summary.** Everything else in the block verified exactly (2,859 B, 20 offsets, max +0x1C2, zero=proceed, stride +0x08 u16, base +0x0C, arena 0x01F83530 which is BSS). **repos-3f and repos-c7 are both building on the wrong half.** | **Also verified for the critical path: `.ard` directory slot 1 IS the `.nmb` container** ({u16 count, u16 version=100, u32 offsets[count+1]}), 5/5 header tests 166/166 — same container, two homes. And **every one of its 1,422 entries is exactly `8 + 24k` bytes**, so the payload has a **24-byte record stride** — none of 84/88/56/56, and the next thing the row-decode needs. **Audited `the-definition-record-flag-pair.md` as it landed:** census 229 / 162 / 10-bits reproduces exactly and the `+0x038` immunity guard re-derives from the bytes; 2 minor defects — "9 masks" is `test`-only (11 with `and`, no new bits), and the stated `.text` size 8,001,280 does not reproduce (7,996,981 virtual / 7,997,440 raw). |
| 2 | `repos-3f` | **⚠ IDENTITY CORRECTION FIRST — read this before trusting rows 2 or 3.** This session's opening `ListAgents` returned **`repos-4b [b2c829]`**; a re-check hours later returns **`repos-3f [7dce2e]`**, with `repos-4b [b2c829]` now a *live peer*. **So everything I produced this session went into `repos-4b`'s inbox, `repos-4b`'s row, `Tools/work/repos-4b*`, and audit stamps reading `last_pass_by: repos-4b`.** I did not re-check the name after the first call — that is the error, and it is mine. **Where my work actually is:** `_index/_inbox/repos-4b.md` ROUNDS 2-4 (the `.nmb` sheet contributions, 7 audit passes, the `st2e` record result). Do not attribute it to the live `repos-4b`. **One consequence is substantive, not cosmetic:** `repos-3f.md` records that *repos-3f wrote* `section-002-text.md` and `section-003-text.md` — and I audited and stamped both. Under the name I now hold that breaks *an author never audits their own sheet*. **The audit itself is independent in substance** (I read them cold and found the unmasked-count defect, 213/828), but the coordinator should re-assign those two stamps to a different auditor rather than take my word for it. **NOW WORKING MY ACTUAL ROW: the four `st2e` row layouts.** Already established and in `repos-4b.md`: slot-2 row `+0x00` is a **bounds-checked index into the slot-0 table**, named from `BattleUnit_ApplyUnitDefinition` `0x0023A570` (`record[+0x00]` u16 at `0x0023A6B4`, bounded against slot 0's count at `0x0023A6B9`); **corpus test 1,146/1,146 in range, every slot-0 row referenced in every area.** Continuing from there. **RESULT 2026-09-06 -> `repos-3f.md`: the slot-2 row is the `.ard`'s JOIN ROW.** It carries four bounds-checked indices, one into each of the other four tables, all named from `BattleUnit_ApplyUnitDefinition` `0x0023A570`: `+0x00`->`02EBF150` (dir 0), `+0x22`->`02EBF148` (dir 5), `+0x24`->`02EBF140` (dir 6), `+0x50`->`02EBF168` (dir 1). **Corpus test of the reader's own preconditions: 4,584 index reads, ZERO out of range.** Two findings of different strength, kept separate on `repos-1e`'s objection: **(a) the three `st2e` joins — coverage 1.000, every row of slots 0/5/6 referenced in every area;** (b) the slot-1 join — in range, coverage 0.688, and unreferenced entries unexplained. **`.ard` DIRECTORY SLOT 1 IS THE `.nmb` CONTAINER FORMAT** — `+0x02==100`, `offsets[0]==4+4*(count+1)`, ascending, terminator in extent, all inside: **166/166 on all five.** Same envelope as the standalone `.nmb` file, different payload (56 B in 165 areas vs `.nmb`'s uniform 3 B). That **collapses four of slot 1's five asymmetries into one cause** (not `st2e`; `u16` count at `+0x00`; bounded `[+0x00]` not `[+0x04]`; different binder `0x003846F0`) — the fifth, the **signed `jg` at `0x0023A724`**, is unexplained and is my top open question. **Boundary for anyone continuing this reader: my four indices sit at `0x0023A6B4`-`0x0023A768`; the first non-`.ard` registry slot appears at `0x0023A860`** (the function touches 8 slots, 3 of them non-`.ard` incl. `repos-1e`'s `0x02EBF130`). **Still no sheet** — the wiring is established, what a row MEANS is not. |
| 3 | `repos-4b` | **AUDITOR ROW — status reclaimed 2026-09-06 by the live `repos-4b [b2c829]`, identity re-confirmed with a fresh `ListAgents` before writing.** **7 audit passes, none on my own sheets:** `section-012` (defect: `id = model − 1000` is per-letter, not global — `b`/`g`/`s`/`t` resolve *directly*, closing its "unexplained zeroes"), `.ard` loader (nothing broke — 6 `[rbp+disp]` reads at the 6 cited addresses, none of the 5 claimed-unread offsets present), `section-010` (corpus exact; **omission found — its `index` is overwritten at load by `0x003DD120`, write-back `0x003DD1BF`**), `section-011`, `section-002`, `section-003` (all reproduced exactly; added: the entry upper-16 takes **exactly two values across all 17,327 entries**), and **`authored-data-table-registry`** (**its §2 caution is answered three instructions inside the function it names — cat 0..4 → `0x02EBF150/168/120/148/140`; the caution listed 4 slots, there are 5, and `0x02EBF168` appeared ZERO times in that 967-line document**). Earlier rounds, as author: `section-008`/`009`, `sab`+`mab`, PKFL container, `@FRP` — `formats_explained` 0→10/48. **Overlap note:** `repos-3f` and I each re-ran passes the other had stamped, both reading the other's stamp as unearned; the sheets involved now carry **two genuinely independent passes**, which is stronger, not wasted. My headless runs against `repos-4b_proj` all succeeded and the embedded EXE still hashes to `73461d08…d89721f8`. |
| 4 | `repos-c7` | **DONE 2026-09-06 — `0x002FEF30` read in full; report in `repos-c7.md`.** **Row premise was wrong: the function is NOT unread** — `08-Combat-Formula/where-a-stat-number-comes-from.md` already has the clamps, the chain, the `+0x15` bits and the growth formula, and my independent re-derivation agrees with all four. **Closed two of its own stated gaps:** `002F8E50`/`002F9180` are integer `/100` (`0x51EB851F`, `sar 5`) — party HP = `((row[+0x18]+1) * rec[+0x08] * row[+0x19])/100`; and the full record->table->output stat map, **eleven s16 per-stat record fields at `+0x08..+0x1C`**. Also: the 9,999 cap is selected by `rec[+0x05]`, and `authored-data-table-registry.md`'s "all four tables indexed by `[rdi+4]`" is superseded — only block 1 is. **THEN CLOSED THE OUTPUT-BLOCK GAP** — `where-a-stat-number-comes-from.md`'s first unmet claim. The block defaults to **`record + 0x24`**, so output N = record 0x24+N, and the record offsets are already named by readers elsewhere: **`+0x06..+0x09` = Strength / Magick Power / Vitality / Speed** (`+0x2A..+0x2D`), **`+0x0A..+0x0C` = Attack / Defence / Magick Resist** (`+0x2E..+0x30`), **`+0x1C..+0x20` = the five elemental-affinity bytes** (`+0x40..+0x44`). Named from readers, never from clamps — the clamps then agree field for field (99 for the four stats, 255 for the three derived, 100 for the rates). **So: a Marlboro's Strength is `record+0x2A` = `growth[+0x26]*K + base[+0x26] + rec[+0x08]`, clamp [0,99].** Correction filed: `attack-defense-preparation`'s "every attribute is a byte so all cap at 255" is false for four of seven — the rebuild clamps them to 99 (PROPOSED-repos-c7-25). **AND THE FLAG-BIT GAP** — `[spine+0x15]` is loaded ONCE (`002FF325`), tested twice, register reused at `002FF381`; bit 0 gates growth col `+0x2D`→**Attack** and `+0x2E`→`[rsi+0x0E]`, bit 1 gates `+0x02`/`+0x03`. **It is EITHER/OR with equipment, not just suppression**: the bit blocks clear `[rsp+0x4c]`/`[rsp+0x70]`, which the item loop tests at `002FF48E`/`002FF477` — a stat takes growth OR equipment, never both. **Bit 4 is not tested here** (the two `cmp rbx,0x10` are loop bounds of 16), so repos-c9's 17/19/21 cluster is consumed elsewhere. Joint with repos-c9: their corpus shows the bit-1 growth column is zero in 0/619 rows, so that pair is **flat, no level scaling, in every shipped area**. **Two of the three gaps `where-a-stat-number-comes-from.md` declared are now closed and a third is half-closed.** All three AUTHOR rows claimed (flagged the repos-3f/repos-c9 st2e collision; c9 stood down and deleted their sheet). |

| 5 | `repos-d6` | **FORMAT WORK STOPPED 2026-09-06 per the 10:40 rewrite; on the enemy-record row.** Where I got to so it resumes cleanly: 4 sheets landed and gated — `efx`+`efb`, `txt`, `ah`, `tm2`+`nfs` (`formats_explained` 12 → 18/48, 0 misaligned anchors in all four). **`mpk` is banked in my inbox as corpus-side ONLY, not a sheet and not declared** — 550 hardcoded paths / 550 shipped / 0 dead, reader NOT found with both failed methods named; resume there rather than from scratch. Nothing else half-written. **ENEMY-RECORD ROW REPORTED 2026-09-06** → `04-Actor-Entity/the-definition-record-flag-pair.md`, tier 1. `+0x064`/`+0x03C` ARE a pair and are **NOT stats — they are status flag words**, OR-ed and mask-tested at **229 sites / 162 functions** over all 8,001,280 B of `.text`; only **9 masks, 10 bit positions**. The guard `0x80000003` (bits 0,1,31) is 125 of 143 sites and its readers name it: **not a live participant** — no targeting, no HP change, no EXP, retire it. **BIGGER THAN THE ROW ASSUMED: there is a THIRD word.** `BattleStats_ChangeStatusAndProcessSideEffects` (`0x0030E360`) writes all three via a 6-entry jump table at `0x0030E88C` — {clear,set} × {`+0x64`,`+0x3C`,`+0x38`}. **`+0x38` VETOES `+0x64`**: setting a bit is refused if the same bit is set in `+0x38` (`0x0030E531`). **All three are WRITTEN at runtime**, so either `+0x698` is not always the authored record or the record is a per-unit COPY — editing an authored row sets a starting value, not a live one. Also `+0x048` (this row): read ONLY when bit 16 is set (`0x003869F1`→`0x003869F7`) and compared against 1 — a small enum, not a magnitude. Two instrument failures of mine caught pre-publication (a byte-presence scan that matched the REX.W prefix and reported 305/305; a noisy read scan the write scan overturned). **THEN CLOSED THE OUTPUT-BLOCK GAP** — `where-a-stat-number-comes-from.md`'s first unmet claim. The block defaults to **`record + 0x24`**, so output N = record 0x24+N, and the record offsets are already named by readers elsewhere: **`+0x06..+0x09` = Strength / Magick Power / Vitality / Speed** (`+0x2A..+0x2D`), **`+0x0A..+0x0C` = Attack / Defence / Magick Resist** (`+0x2E..+0x30`), **`+0x1C..+0x20` = the five elemental-affinity bytes** (`+0x40..+0x44`). Named from readers, never from clamps — the clamps then agree field for field (99 for the four stats, 255 for the three derived, 100 for the rates). **So: a Marlboro's Strength is `record+0x2A` = `growth[+0x26]*K + base[+0x26] + rec[+0x08]`, clamp [0,99].** Correction filed: `attack-defense-preparation`'s "every attribute is a byte so all cap at 255" is false for four of seven — the rebuild clamps them to 99 (PROPOSED-repos-c7-25). **AND THE FLAG-BIT GAP** — `[spine+0x15]` is loaded ONCE (`002FF325`), tested twice, register reused at `002FF381`; bit 0 gates growth col `+0x2D`→**Attack** and `+0x2E`→`[rsi+0x0E]`, bit 1 gates `+0x02`/`+0x03`. **It is EITHER/OR with equipment, not just suppression**: the bit blocks clear `[rsp+0x4c]`/`[rsp+0x70]`, which the item loop tests at `002FF48E`/`002FF477` — a stat takes growth OR equipment, never both. **Bit 4 is not tested here** (the two `cmp rbx,0x10` are loop bounds of 16), so repos-c9's 17/19/21 cluster is consumed elsewhere. Joint with repos-c9: their corpus shows the bit-1 growth column is zero in 0/619 rows, so that pair is **flat, no level scaling, in every shipped area**. **Two of the three gaps `where-a-stat-number-comes-from.md` declared are now closed and a third is half-closed.** All three AUTHOR rows claimed (flagged the repos-3f/repos-c9 st2e collision; c9 stood down and deleted their sheet). |
| 6 | `repos-c9` | **AUDITOR ROW DONE** — 09-03 backlog (30 docs) and the owing set (6 docs) both closed: 1,730 boundary checks + 437 claim checks, **6 real defects, every one an ANCHOR error, none changing a conclusion**; §13-§15 of my inbox. The recurring one is a writing-standard gap — **three authors' hand-written listings anchored to the function entry instead of the instruction** (`0016242A`, `00233C55`, `002DF220`). **⚠ ST2E COLLISION, RESOLVED IN `repos-3f`'s FAVOUR.** I took the row believing it orphaned — row 2 was blank and `repos-4b` had stopped the same decode — but `repos-3f` claimed it in the interval; **`repos-c7` caught it and told me.** I have **DELETED the sheet I wrote** (no inbound links, `check_links` clean) rather than leave a second row-layout document in the folder that already produced one duplicate this round. **Their `+0x00` result is from a READER (`0x0023A6B4`/`0x0023A6B9`) and beats my corpus tracking; mine corroborates it independently at 138/138.** **ADDITIVE AND HANDED OVER in §16: two further index columns nobody had — `+0x22` -> slot 5 (140/140 tight, slack 0.00, bijective in 137/140) and `+0x24` -> slot 6 (120/120 tight) — every target row referenced in every area, slot 2 never smaller than any table it points at, so SLOT 2 IS THE SPINE, which is why `repos-4b`'s `.nmb` count join landed on it. Noise floor measured first: the weak in-range test passes 1-5 columns per pair; `+0x24` is in range for ALL FOUR tables and tight only against slot 6.** Plus the dead-byte topology (43/27/32/40 bytes never non-zero) and slots 5+6 sharing a size AND a zero-run shape. **NEXT: taking another unclaimed author row — NOT st2e.** | **RECONCILED with `repos-c7` 2026-09-06 — and it produced a result neither of us could reach alone.** Their consumer read of `0x002FEF30` and my corpus tracking land on the SAME three edges from opposite ends (`rec[+0x004]` -> `0x02EBF120` -> `word[+0x00]`/`[+0x22]`/`[+0x24]`), which also confirms **`0x02EBF120` IS `.ard` slot 2, the spine** — nothing had stated that. They asked me to check an apparent contradiction between their conditional stat pair and my dead-byte census; **checking it corrected MY wording and answered their question**: slot 5 `+0x02`/`+0x03` are live in 84/1,119 rows, slot 6's are zero in **0/619**, so the gated pair is real and **its growth coefficient is dead in every shipped area — the stat is a flat authored value with no level scaling.** Flag test: bit 1 of `spine[+0x15]` clear predicts a dead pair in 1,018/1,020 (99.8%), set predicts live in 83/126; **the 43 flagged-but-dead rows are unexplained and published as the open end.** Their proof that slots 5/6 are one layout used twice (one function, identical displacements) beats my shared-size lead and I have deferred to it.

**Edit only your own row**, one line per edit.

## 2. Already done — do not reopen

**EBP** all 14 units · **`.ard`** loader, `.nmb`, and the 166-area census · **PKFL container** (all
four extensions) · **`sab`/`mab`** · **`ca`/`cm`** (`@FRP`, one sheet, both extensions).

**No metric numbers are written here on purpose.** An earlier version of this board carried live
figures and they were stale within the hour — which is the same drift that buried the live rows
behind four rounds of superseded ones. **Run the checkers instead; they are never out of date:**

```
python Database/Tools/analysis-kit/gfz-scripts/check_assets.py  --db "Database/FFXII TZA"
python Database/Tools/analysis-kit/gfz-scripts/check_formats.py --db "Database/FFXII TZA"
python Database/Tools/analysis-kit/gfz-scripts/progress.py
```

`check_assets.py` prints every covered format with its owning document and every uncovered one with
its file count — **that listing is the authoritative "what is left", not this section.**

## 3. Two coordinator errors you must not build on

- **The PKFL `0 B` odd-slot medians were an artefact of the census's own arithmetic**, not payload
  sizes — slots alias, and "next offset minus this offset" gives an aliased slot zero. **The
  DAT/CTL reading and the 14-pair denominator are WITHDRAWN.** PKFL is not scoreable by pair-units
  until the container sheet's questions are settled.
- **The `0x` citation fix left a decimal over-count** — `0.00390625` matched as an address. Fixed;
  it had produced 100 spurious matches across 22 documents.

Both are written up in `COVERAGE.md`.

## 4. Start-up, before any work

**Paths must be ABSOLUTE.** Do not reuse `proj_h*`, `gn159_certify` or `gfz_gm160` — those hold
GN158/GN159-era parents and working from a superseded parent silently re-does closed work.

```powershell
cd 'C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\ghidra\run'
$D = 'C:\Users\Kristian\source\repos\XIIOnline\Database'
$p = .\Import-GfzParent.ps1 `
  -Gzf "$D\Tools\parent\FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_GN160_99P636_2026-09-03.gzf" `
  -ExpectedSha fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 `
  -ProjectDir  "$D\Tools\work\<your-session-name>_proj"
.\Verify-GfzCheckpoint.ps1 -ProjectDir $p.ProjectDir -ProjectName $p.ProjectName
```

Expected ledger: `internal=38161 owner=9409 finalNo=585 codeDomain=28028 explicit=38022
unresolved=139 pct=99.63575`. **A Ghidra project is held by one process — use only your own.**
Scratch in `Database\Tools\work\<your-session-name>\`.

## 5. Required reading

- [`../RULES.md`](../RULES.md) — 240 rules across 10 documents plus 37 checkers
- [`../EVIDENCE-STANDARD.md`](../EVIDENCE-STANDARD.md) — 43 rules, binding on you as on the coordinator
- [`../COVERAGE.md`](../COVERAGE.md) — 90+ findings, **instruments that lied**. Every entry is a
  mistake already paid for once, and it is the cheapest file in the project.
- [`../ASSET-FORMATS.md`](../ASSET-FORMATS.md) — the 48-extension census, dispositions, build order
- `_templates/FORMAT.md` — sheet shape. **Layouts go in a `struct` fence** (§2), validated by
  `check_layouts.py`.

## 6. What you may not do

- **Never** `Apply-GfzBatch.ps1` or `Pack-GfzCheckpoint.ps1`. Mutation authority is the
  coordinator's. Put manifest rows in your inbox under `## MANIFEST-ROWS`.
- **Never** edit the shared `_index/*.md` — append to your own inbox instead.
- **Never** use `.pdata` / `.xdata` / unwind / EH maps as semantic evidence.
- **Never** pick a question-id prefix by eye. Propose `PROPOSED-<session>-n`; the coordinator
  assigns the real prefix at merge. **Taken so far: BW BX BY BZ CA.**

## 7. Reporting

Append to `_index/_inbox/<your-session-name>.md` under these headings:

```markdown
## STATUS            one line: row, what you are on, blocked or not
## COVERAGE
## OPEN-QUESTIONS    new ids as PROPOSED-<session>-n
## AUDIT-LOG
## CALL-CHAINS / ADDRESS-INDEX
## MANIFEST-ROWS     entry / domain / unused / evidence
```

**State what native behaviour was learned, not how many functions moved.**

**Re-run the gates AFTER writing, not only before** — `check_ebp`, `check_assets`, `check_formats`,
`check_layouts`, `check_links`, `check_located_not_read`, `check_named_not_cited`,
`check_source_hygiene`. A single red result is not evidence until re-run; with six sessions writing,
the gates read files mid-write.
