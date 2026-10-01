# Consumer-check record — DD content work on seven PARTIAL pages (FABLE, Claude Opus 5.5, 2026-09-30)

One block per page with corrections. Every struck sentence was on the page at HEAD 9aac223bf (unchanged through 9a4cd5784). Each correction carries a dated "Corrected 2026-09-30 (FABLE)" note. Consumers outside the seven pages are not edited: they are marked routed-to-<owner> and listed again in the batch README. Installed by apply.py at `_index/candidates/dd-content-fable-0930/consumer-check-0930-dd7.md`, beside the evidence scripts the pages cite.

## gambit-evaluation-and-enmity.md - three corrections (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`

### C1. Section 6: "a gambit that should fire but doesn't is usually failing at commit"

The modding bullet contradicted the page's own section 2 correction of 2026-09-26 and the gambit-walk contract
§7 (OPUS, measured 6/6): over the shipped action table, a line whose condition matched is never refused by the
commit. The bullet is struck and replaced. It now says the failure is inside the evaluate step: the eligibility
gate, the preconditions or percent chance (`0030160F`-`00301637`), or a selector that finds nobody.

- consumer: `09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md` §7 - agrees (it is the source of the correction).
- consumer: this page, section 2 (the 2026-09-26 strike at "This is why a gambit with a satisfied condition can
  still visibly do nothing") - agrees.
- consumer: no other page repeats the phrase (grep "failing at commit" / "usually failing" over the database,
  `_experiments/evidence` excluded: this page only).

### C2. Section 8k: the return window as "`30 × g_nSpawnKeepReturnWindow` raw ticks"

The comparison is `(int)(01DFE0B8 × 30.0) × window` (`002337DE`-`00233801`), so the factor is 30 only at
FrameLimit 30. The expression is struck and replaced; the "300 seconds" figure stands (the window's native value
is written at `00236A0D`; L-2 establishes the unit).

- consumer: register row L-2 - agrees (it states `(int)(DAT_01DFE0B8 × 30.0) × g_nSpawnKeepReturnWindow`).
- consumer: `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` - agrees in its code block (line 350
  carries the scalar); its prose (lines 370-371, "within `30 × window` raw ticks ... `30 × 300 = 9,000` ticks") gives the FrameLimit-30 value. Not
  edited here: routed-to-owner of the spawn page as a wording note, no register row (the value it states is right
  at the default frame limit and its own code block carries the full expression).

### C3. Section 8l: "the three entries run in index order, each narrowing the candidate set"

Read from the whole of `003014C0` (`00301681`-`003017BF`). The 512-byte copy is entry `i`'s own result, not the
starting list. Entries narrow the set only when bit `i` and bit `i+1` are both set (`003016E2`-`00301746`).
Otherwise the next entry filters the original list (`00301753`) into its own buffer (`00301750`-`00301768`). The
final pick reads only the first buffer (`003017B7`). Every non-empty entry must find someone (`003016AF`). The
sentence and the "not read here" residue are struck and replaced.

- consumer: `09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md` §14 item 2 ("one bit per target-selector entry -
  keep the intermediate candidate set") - agrees: keeping the intermediate set is the chained case.
- consumer: this page, section 8g's Z-19 table row for `0x08` / `0x10` / `0x20` ("keep the intermediate
  candidate set") - agrees.
- consumer: register row Z-19 - agrees (it names the shifted test, not a narrowing order).
- consumer: `_index/_inbox/repos-78.md` line 1748 (the 2026-09-03 inbox transcript this section was built from) -
  routed-to-none: a historical inbox record, not a published claim; left as the history of the reading.

run: gambit_gen.py at 4407f8484 (the edits are cut from the HEAD blob, which is unchanged since 9aac223bf); the
three readings are disassembly by `Database/Tools/work/FABLE/pub140-scratch/disr.py` of `003014C0`, `00233780`
and the contract, and `tools/rawcalls.py` / `tools/ripscan.py` for the caller and reference sets

## Consumer check — active party, reserve and the leader change: three corrections (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/11-Party/active-party-reserve-and-the-moment-the-leader-changes.md`

### What changed

1. **§2, the class-`0x17` check.** "An index is also skipped if `BattleEncodedId_IsValidForClass(0x17, index)` fails" was
   said of both readers. It is true of the roster read `0031B510` (`0031B553`/`0031B555` skip). The reserve probe
   `00321100` sends a failed check to the same exit as its `0xFF` hit (`0032112E`/`00321130` and `00321139`/`0032113D`,
   both to `00321158`) and returns that index. Struck and replaced.
2. **§4, the teardown's copy.** "snapshots a 0x90-byte block of the manager's `0x860`-stride record from `+0x7A0` to
   `+0x6F0` (`0025A6CB`–`0025A743`, the rest unread)": the copy is `0xB0` bytes (`0025A6FC`–`0025A763`, eleven `movups`
   pairs), and the record is one of two `0x860`-byte camera contexts at `02097D20`, not a manager record. Struck and
   replaced; §9 now reads the whole body.
3. **§6, the data block.** It named `+0x5A7E` as the configuration and `+0x5A48` as "a parallel nine-entry, 2-byte array
   scanned for de-duplication on add". §2's own 2026-09-03 correction, §2b and the five-maps page's 2026-09-14
   correction already have map 0 at `+0x5A48` as the configuration and `+0x5A7E` as map 3, rebuilt from it. The block
   is rewritten, with a dated note under the fence naming the old text.

### Consumers

- `CONTRACT-party-focus-and-control-suppression.md` §5 and §14 already say "two `0xB0` blocks": **agrees** with (2). Its
  §5 "the manager record the teardown snapshots" uses the word this page struck; **routed-to-owner** (OPUS, the
  contract's owner), not edited here.
- `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md` (the two `0x860` camera
  contexts, the `0xB0` pose blocks at `+0x6F0`/`+0x7A0`): **agrees** with (2). Separately, it says the dispatcher's
  `desc+0xF0 == 2` arm calls `00259990`; this read found the arm that calls `00259990` is kind **1** (`002598AA`
  `mov ecx, [rbx+0xF0]`, `002598B0` `sub ecx, 1`, `002598B3` `je 00259916`). **routed-to-owner**, not edited here.
- `the-five-parallel-slot-maps.md` "SWE2-EC7-95 update": says `00321100` returns "the first index whose byte ... is not
  `0xFF`". The bytes say the opposite (`00321139` `cmp ..., 0xFF` / `0032113D` `je 00321158` returns the index when the
  selector IS `0xFF`). **routed-to-owner** (SWE2-EC7's note), not edited here. Its 2026-09-14 correction (map 0 is the
  configuration) **agrees** with (3).
- Register row O-5 ("the nine selectors at the battle-state block's `+0x5A48` are one array, 0–3 the roster and 4–8 the
  reserve"): **agrees** with (3).
- This page's §10 evidence row "Nine 2-byte records; 0–3 roster, 4–8 reserve" (the `0x5A7E` / `0x5A86` bases): unchanged
  and still true of map 3; **agrees**.

### Regression

run: disr.py at d20226c17 (pub140-scratch, whole bodies of `0031B510`, `00321100`, `003170E0`, `00320800`, `0025A6A0`,
`0025A180`, `00259510`, `00359410`, `00259820`; the page blob is unchanged from 9aac223bf)

## Equipment slots and the single stat rebuild — two corrections (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md`

### What changed

1. **§6 called `stats[+4]` "the party slot".** It is the record's type id, the party-table row
   (`actor-type-id-partition-and-the-13-value-band.md` §8; for the main roster, rows 0–6, the two coincide).
   Struck and replaced; the §8 evidence row that said "the slot at `+4`" is struck the same way. The band
   `(uint8)(stats[+4] - 0x1B) <= 0x0C` is the thirteen Espers, not "a band of slot indices".
2. **"The contribution formula is not read"** (status line, lead, §6 end, §7) is struck: `002FEF30` was read whole
   (`002FEF30`–`002FFA5A`) and §6.1 now gives the formula term by term with instruction anchors. The §10 / §11
   "not read" lists are struck with dated answers (`00324470`, `00324380`, `0034A300`, the `N = 5` census); the
   battle-menu actions `0x9C` / `0x9D` stay open as a new register row (`FD-n30`).

### Consumers

- `08-Combat-Formula/where-a-stat-number-comes-from.md` — **agrees** on the stages, the category pairs, the caps and
  the Esper second store. Two statements there differ from the body as read today and are **routed-to-the stat
  page's owner** (not edited here): "two helpers that take the **level** at `+0x08`" — `+0x08` is the party record's
  base-HP stat (the field map's row `+0x008`), and the helper computes `(row.b18 + 1) * stats.u32_08 * row.b19 / 100`;
  and "every clamp is two-sided … written as 0" — the max-HP clamp floors at **1** (`r15d = 1`, `002FF5A7`, compared
  at `002FF7B1`), as `CONTRACT-stat-derivation.md` §14 already re-measured.
- `08-Combat-Formula/CONTRACT-stat-derivation.md` — **agrees** (band = Espers, floor 1, cap selection by `+0x05`).
- `08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md` — **agrees**: `+0x04` type id, `+0x08`
  base HP, `+0x10`–`+0x1C` the four f32 base stats on the party side; §6.1's output names are taken from it.
- `12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md` §2 — calls `unit[4]` "the party
  slot" in its early-exit block; the same field. **routed-to-the licence page's owner** (not edited here); the gate it
  documents (`cmp byte ptr [rsi + 4], 6` / `ja`) is unaffected by the name.
- `04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md` — **agrees** (it is the source).
- Register: no row cites the struck sentences. `FD-n30` is new (new_rows.tsv).

### Regression

run: documented_rule.py at 9aac223bf (export `C:/x/dd/b/exp`, patched page): READY before and after with the placeholder
unread; PARTIAL (live `FD-n30`) once the row is registered (simulated OPEN, `eq_rule_with_ids.py`).
run: verify_doc_addresses.py at 9aac223bf (export): ok before (111 cited) and after (221 cited: 9 data, 74 entry, 135 interior,
1 literal, 2 text-data; no unadjudicated .text gap citation).
run: audit_crossrefs.py via check_publish_neighbours.findings at 9aac223bf (export): 0 findings on the page before and after
(1,264 corpus-wide both times). check_links.py --raw: no broken link from the page.

## the-shop-table-and-its-stock-gates.md — five corrections (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md`

### What changed

1. **§4 pseudocode.** `shop_first_open_entry` returned an index and ended `return s->count; /* nothing offered */`. The
   function returns an entry pointer, and when every gate fails it returns the last entry. `rbx` is zeroed at
   `002FAD4F`, set per entry at `002FADB0`/`002FADBF`, and returned by the only exit, `002FAE2D`; `002FAD75` leaves the
   loop with the last entry still in `rbx`. The block is rewritten, and a dated note quotes the old two lines. §2.5 and
   SG-2 already said this; only the code block disagreed.
2. **§7 countB.** "tests it against a mask from `002536A0` — the same block-state function §5 already cites" is struck.
   `002536A0` is an 8-byte getter of the block pointer `qword [020927C0]`. The mask is `1 << (i & 7)`
   (`003166B7`–`003166C1`), and §2.4 is the section that cites the getter, not §5.
3. **§7 predicates.** "Not established: what `0046B1A0` accepts, and what the `+0x3844` byte and the `002536A0` mask
   mean" is struck. FG-1 (ANSWERED 2026-09-27, OPUS) answers it: the quest-clear bit, the quest count over the
   `menuhandbook.bin` node, and the 30-bit award bitmap. The page now cites FG-1.
4. **The list-kind section, bit 31.** "*Still not read:* what consumes either form of the bit, and what `0057DAD0`'s `+4`
   would carry" is struck. The `+4` half was answered by the page's own bit-3 bullet. For layout-A rows the consumer is
   the transaction driver `0056D370`, which clears the bit (`0056D468`). The layout-B half is registered as FD-n40.
5. **Crossings.** "Whether any purchase path re-checks them is not read here" is answered: none does, bound by direct
   calls (§5). "PlatformOnlineAchievements — … not read" is struck and the edges are read: the achievement-counter
   family, reached through the clan rank.

Added without striking anything: §2.4 ties `00321190` (the operand resolver) to the gate by instruction; §5 gains
upstream, downstream and the purchase path; §3 gains six function rows; §8 gains six evidence rows; and the "not
establishable by this method" bound on the price reader gains a note, because a reader was found by following the
purchase (FD-n41 is what stays open).

### Consumers

- register row SG-2 (ANSWERED, "the fallback is observable"): **agrees**. It states the last-entry fallback that the
  corrected pseudocode now shows.
- `CONTRACT-shop-stock-ladders.md` SG-1 and SG-2 (one evaluation carried by pointer; last entry, or null for an empty
  section): **agrees**. The corrected block returns a pointer, returns null for an empty section, and cites both.
- register row FG-1 and `the-save-payload-field-map.md` §7 (the rank's `+4` and `+5` minima): **agrees**. The page now
  cites them, and it states nothing about the predicates that FG-1 does not.
- `20-Platform-Online-Achievements/CONTRACT-achievement-counters.md` (`+0x3844`, the award bitmap, set-only): **agrees**.
  The page's older line quotes this contract as leaving the two counters "named and bounded". That quote is left as
  it stands: it is history, and the new paragraph below it says what FG-1 settled.
- `16-UI/Widget-Object-Model/the-widget-message-protocol.md` (L328, L369, L1001: `+0x10` carries the price whole or
  halved; the `0x20`-byte list `00565720` rebuilds): **agrees**. Nothing it says is changed. FD-n41 asks the question
  of order its message-26 arm raises.
- register rows UQ-132 and UQ-133: **agrees**. Their text is not touched, and the status line still names them as
  answered.
- other pages that link the shop page (the encoded-id page, the authored-data registry, the VBF page, the category
  README): **agrees**. They cite the binding and the name reader, which did not change.

### Regression

run: documented_rule.py at d20226c17 (on the export `C:/x/dd/b/exp`, a `git archive` of 9aac223bf; this page is
unchanged between the two), PARTIAL: three open boxes FD-n40..FD-n42, which is the intended state until they close;
FG-1, UQ-132 and UQ-133 answered; no unknown ids.
run: verify_doc_addresses.py at d20226c17 on the patched copy: 0 unresolved; entry 77 -> 83, interior 221 -> 269,
data 10 -> 11 (`020927C0`). The same four `.text` table addresses as before are flagged for confirmation in context.
run: xlayer_full.py at d20226c17, before and after: UNACCOUNTED 6 and 6, with identical edge tokens for all six layers.
The two layers the new citations reach are named in crossings: Rewards_Progression_Economy is new; PlatformOnlineAchievements
was already there.

## The three reward pages — six corrections (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md`
affected: `Database/FFXII TZA/13-Rewards-Progression-Economy/experience-and-license-point-award.md`

The third page, `how-experience-is-computed-and-divided.md`, gains the NOTE structure, anchors, and a Limits section
that gives the register ids. None of its claims is struck.

### What changed

1. **The name of `00312280`** (death page lead). `…AndRetire` is struck for the function table's `…AndLoot`, the name
   the page's own crossings already used. PKG-GP-HP-LETHAL G5 had let the label pair stand as a label.
2. **Counter `0x11`'s amount** (death page step 6). The old text, "the reward row's word +0 times the level span
   (`00317090` → `00316A50`)", is struck. `00317090` (78 B, read whole) computes
   `span × perLevelRow.u16[+0] + baseRow.u16[+0]` (`003170AA`–`003170D1`) and tail-jumps through the thunk `00253770`
   with `ecx = 0x11` (`003170D3`, `003170D8`).
3. **"Status id 12"** (death page, the LP-to-gil section). `+0x69` / `+0x79` are byte 1 of the 16-byte effect layers
   `+0x68` / `+0x78`, so bit 4 is effect id 12, not status 12. Status 12 is Reverse. The effect's shipped help text is
   "Convert all license points earned to gil.", and its one rebuild-category carrier is the Cat-ear Hood `0x117F`
   (`augment12.py`, `augment12_equipment.py`, with the 27 / 28 control).
4. **"Its wrapper `003171C0`"** (death page crossings). It is a callee: `00312280` calls it at `003122D5`.
5. **`00319CA0` "~227 B"** (death page, SWE2-FRONTIER's subtree section). It is 394 B (`0x18A`). 227 B (`0xE3`) is the
   member `00319A20`.
6. **"Live confirmation queued"** (award page §9). Nothing is queued, and the claim is tier-1 static
   (`002F8D26`–`002F8D3E`, `002F914B`–`002F9155`).

Two further changes reconcile wording without striking a claim:
- the level walk's "threshold table returning zero" is now explained as the curve `002F8F20` returning −1 above level
  98;
- the text now avoids the contract's invariant label, which failed the unknown-id check, and names that invariant in
  words.

### Consumers

- `CONTRACT-defeat-rewards-sequence.md` §2: "[the death page] calls it `…AndRetire`" becomes stale once (1) lands.
  Its §3 and DR-5 say "status id 12" (3). DR-1 lists "→ retirement". DR-3 repeats "a threshold table returning zero
  terminates the walk".
  **routed-to-FABLE** (the contract is FABLE's S-32 page). It is not edited here: the working tree carries a peer's
  uncommitted edit to it (`git status` ` M`), and it is outside this batch.
- `the-chain-and-its-sticky-coin.md` L32: "…in `BattleUnit_ProcessDefeatRewardsAndRetire`" (1).
  **routed-to-FABLE** (the page owner), a label fix.
- `04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md` §4: "word `+0` into game counter
  `0x11` (`00317090` → `00253770(0x11, n)`)" **agrees** with (2). The same sentence says LP is "doubled by effect id
  12 in either layer", which is wrong: the LP computer doubles on `+0x6B` / `+0x7B` bit `0x10`, effect id 28
  (`002F914B`–`002F9157`). Effect id 12 is the defeat body's conversion (3).
  **routed-to-the page owner**.
- `20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md` (AB-7 / AB-8 narrowings) and
  register row AB-8 (SUPERSEDED 2026-09-26 on "no native body feeds counter 17"): **contradicted** by (2). Counter 17,
  `ACH_COUNT_SCORE` / Record Breaker, has two feeders that reach `00316A50` by tail jump through the thunk `00253770`,
  which the census's direct-call scan did not follow:
  - `00317090`, per defeated enemy (`003170D3 mov ecx, 0x11`, `003170D8 jmp`);
  - `002E2380`, a 12-byte wrapper (`002E2382 mov ecx, 0x11`, `002E2387 jmp`), reached by tail jump from `003403E0`.
  The raw call index lists six sites on `00253770`, two of them `jmp`.
  **routed-to-FABLE** (AB-8's author and the catalogue page). The register row needs reopening or a SUPERSEDED
  correction, and this batch does not edit the register.
- `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`, the `00312280` phase list: **agrees** on the caps, the
  level walk's −1 stop, the LP redirect and the NULL recompute. It is wrong in two places:
  - "Member `003171C0` then fires the licence-notification battery unconditionally". It fires counter 4 and the
    species tally, and only for an enemy-kind record (`003171D9`).
  - "`00236780` is the shared RNG/roll helper" (the note closing that phase list). It is the 17-byte New Game Minus flag getter.
  **routed-to-the page owner**.
- `20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md`, the pass-22 crossing: "`003171C0`,
  the wrapper that fires counter 4" (4). **routed-to-FABLE**, a wording note.
- `19-Save-Load-Settings/.../version-stamps-and-what-loading-normalises.md` (FV-2, "the two sibling bits": set by
  `btlAtelResetNgPlus` / `btlAtelResetNgMinus`) **agrees** with the new New Game Minus section. It names only the
  verbs, and the raw call index also shows a native caller of each request setter, from the state handler `0023FBE0`
  (`00240182`, `0024018C`). That is a note for its owner, not a correction. **routed-to-FABLE**.
- `world-loot-pickups-the-ten-slot-pool-and-the-despawn.md` §3 (`00319CA0` 394 B): **agrees** with (5).
- Register rows N-2 and N-3: **agree**. N-2's accessories and N-3's "status words `+0x3C` / `+0x64`, effect layers
  `+0x68` / `+0x78`" are what (3) and (6) rest on.
- `CONTRACT-experience-and-licence-award.md`: **agrees**. It carries none of the struck sentences.

### Regression

run: disr.py at 9aac223bf (pub140-scratch; whole bodies of `00312280`, `00317090`, `003171C0`, `00236780`, `002F8F20`,
`002F8BB0`, `002F90C0`, `00319490`, `00239960`, `0030C650`, and `003377C0` for FD-n53; `tools/rawcalls.py` one target
per command for `00312280`, `00317090`, `003171C0`, `00253770`, `00238A50`; `tools/ripscan.py 02089344 02089348`;
`tools/blk4_writers.py 02EBF190 4`), with the page blobs unchanged through 9a4cd5784.
run: augment12.py at 9aac223bf: row 12 → 13012 → "Convert all license points earned to gil."; control rows 27 / 28 read
"Doubles EXP earned." / "Doubles license points earned.". augment12_equipment.py: controls `0x1168` / `0x116F` /
`0x1171` = 27 / 28 / 29 at category 21; `+0x1A == 12` on `0x1000` Unarmed (category 0) and `0x117F` Cat-ear Hood
(category 22).

