# ASTRA's four OV-42 returns consumed after independent review (FABLE, Claude Opus 5.5, 2026-10-02)

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/the-nonempty-prf-registration-and-specialized-relocation.md`
affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

ASTRA queued four returns to FABLE on 2026-09-30, each "after SPEC review":
`ASTRA-RETURN-FABLE-OV42-ACTION-PRECONDITIONS-0930`, `-OV42-CLASS20-ADMISSION-0930`, `-SPATTACK-REMAP-0930` and
`-ACTION-SELECTOR-EXCLUSIONS-0930`. FABLE's previous record [`astra-returns-fable-0930`](../astra-returns-fable-0930/README.md)
held all four under "Not consumed (no accepted review record yet)". SWE2-AUDIT-SPEC has since committed tracked review
records for all four, in `2e88eceef`. This record consumes them.

It incorporates only the accepted claims, applies the one review's narrowings, and keeps every limit that ASTRA and SPEC
state. **No register lead word changes.** OV-42 stays PARTLY ANSWERED, because its remaining question is whether shipped
play ever rejects a submission, and none of these packets observes or proves a natural rejection, or proves there is
none. OV-21 is not edited. No natural or universal reachability is claimed in either direction.

The image facts this record cites are re-read by [`ov42_astra_check.py`](ov42_astra_check.py)
([out](ov42_astra_check.out)): FAILS 0, 188 checks, with two controls that are sensitive to the defects they name.

## The reviews (all committed in 2e88eceef)

| return | ASTRA packet (commit) | review | verdict |
|---|---|---|---|
| OV42-ACTION-PRECONDITIONS | [`ov42-special-action-preconditions`](../../../_experiments/evidence/ov42-special-action-preconditions/README.md) (`318e510c6`) | [review](../auditspec-review-astra-ov42-action-preconditions-0930/REVIEW.md) | ACCEPT-WITH-NARROWING (wording: radix of "Row113", the conditional D0..F1 refusal, two unnamed prefix gates, "safe under ns8" is the WORD sign only) |
| OV42-CLASS20-ADMISSION | [`ov42-class20-action-admission`](../../../_experiments/evidence/ov42-class20-action-admission/README.md) (`1cf5316d0`) | [review](../auditspec-review-astra-ov42-class20-admission-0930/REVIEW.md) | ACCEPT |
| SPATTACK-REMAP | [`spattack-native-word-remap`](../../../_experiments/evidence/spattack-native-word-remap/README.md) (`1f6569546`) | [review](../auditspec-review-astra-spattack-remap-0930/REVIEW.md) | ACCEPT (four precision points, none changes a claim) |
| ACTION-SELECTOR-EXCLUSIONS | [`action-selector-local-exclusions`](../../../_experiments/evidence/action-selector-local-exclusions/README.md) (`7f625ac43`) | [review](../auditspec-review-astra-action-selector-exclusions-0930/REVIEW.md) | ACCEPT |

The board rows for the first two had carried `verdict:ACCEPT` that cited a gitignored batch file. The verdicts used here
are those of the review records. For the first packet, that verdict is ACCEPT-WITH-NARROWING, not ACCEPT.

## FABLE's OV-42 model before this record

The owner-protocol scope is answered: the requester rejects only on a negative narrowed index, and there is no
recovery after that. The 2026-09-30 narrowings add two facts. The FST table extent does not bound the narrowed owner
index. The special-action override short-circuit returns only the words 226..241 for a valid state. What stays open is
whether a shipped selector producer ever delivers a selector whose narrowed WORD is negative. That is natural rejection
in shipped play, and the register marks it RT.

This record follows one producer of such selectors, the global special-sequence path. Along that path, the four packets
narrow which action rows could deliver a negative WORD, and which legs could carry them there.

## Consumed

### 1. ASTRA-RETURN-FABLE-OV42-ACTION-PRECONDITIONS-0930 (ACCEPT-WITH-NARROWING; narrowings applied)

**Accepted scoped fact.** This is the selector path, with the shipped data it reads:

- `0030CD99` calls `0030CE10` with a resolved action-row pointer.
- `0030CE93`/`0030CE9A` skip any row whose `+0x0C` bit 30 is clear.
- A surviving row reaches `00306BD0` at `0030CF0D`.
- `00306BD0` sets `ebx` to 3 at `00306C0A` and calls `00309230` at `00306C4D`. That function's ordinary arm returns the
  row's unsigned WORD `+0x24` (`003092C5`). `00306C52`/`00306C54`/`00306C56` then pass it to `0032FC30` as
  `(3, word)`.
- Group 3 maps to kind 8 and the full index `4w+1`. That is the FST record's mapping, already accepted.

The data: all nine shipped `battle_pack.bin` action tables are one table of 543 rows, 60 bytes each. Every word that
is not FFFF gives `(4w+1) mod 65536 < 32768`. **No ordinary word can give a negative narrowed WORD on this path.**

FFFF occurs on 68 rows. Its full index is 262,141 and its narrowed WORD is -3. 25 of those rows have bit 30: row `0x113`
(decimal 275) and rows 511..534. Rows 511..534 all carry the same flags dword. **The local bit-30 test therefore does
not exclude rows 511..534.**

**Narrowings applied, in SPEC's wording:**

- **The identity arm is row `0x113` (decimal 275), not decimal 113.**
  - `003092B4 imul ecx,edx,0x113` builds the compared row pointer.
  - For that row, `00309230` returns an entry of a 13-entry stack table indexed by the raw record's byte `+4` minus
    `0x1B` (`003092CB`..`003092DB`). The index is not bounds-checked, so the type bound stays a premise.
  - Decimal row 113 has word `0x808B` and no bit 30.
- **The D0..F1 refusal is conditional.** `0030CEC2`..`0030CEFE` refuse rows `0xD0`..`0xF1` only while the
  special-sequence state `022C2160` is 5 or 6. Otherwise those rows fall through to `00306BD0` like any other bit-30 row.
  Rows 511..534 lie above `0xF1` in any case.
- **Two prefix gates the packet does not name.** `00306BD0` returns 0 before `00306C4D` unless both hold:
  - `022C2160` is 0, or it is 1 with the same owner in `022C2168` (`00306BDA`..`00306C03`);
  - `0032F6E0(3)` returns 0 (`00306C22`/`00306C29`). That function reads the signed byte `022C6D20[3]`.

  These are the "idle, or re-entered by the same owner" and "`0032F6E0(3)` allows it" conditions of the
  [mode-ladder page §2d](../../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md), and they
  agree with it.
- **"Safe under ns8" means the sign of the narrowed WORD, nothing more.** Ten distinct words that are not FFFF have
  bit 15 set (32775..32907). They sit on rows 111-123, 246-261, 427-435 and 440, and their full indices are
  131,101..131,629. None of those rows has bit 30, so `0030CE9A` rejects them on this path.

**What it changes in FABLE's OV-42 model.** This is one producer of the "every non-debug selector producer's range into
`0032FCA0`" discriminator, which the FST record left as next.

- For this producer, the data residue is at most rows 511..534 (FFFF, WORD -3).
- The row-`0x113` arm is a separate residue, behind its type premise.
- The table extent cannot settle either one. FFFF's full index lies far past the 820,000-byte FST table under the FST
  record's `kind*5000 + index` formula.

**Stays open (as ASTRA and SPEC state).**

- Row-`0x113` codec, pointer identity and type bound are premises.
- The pack-cell resource id `0x13` is not traced to the file name.
- The checker pins text, not bytes. Its kind selector `00306C0A` is not pinned; SPEC decoded it, and this record's
  check re-reads it.
- No successful size lookup, primary load, companion directory, owner submission or gameplay selection is proved.
- Who produces ids 511..534 before `0030CE10` is still unknown. This is a static question.

### 2. ASTRA-RETURN-FABLE-OV42-CLASS20-ADMISSION-0930 (ACCEPT)

**Accepted scoped fact.**

- `0030CBE0` reads the slot's u16 action id: `0030CC25 movzx edx, word [rbx+0x1c]`.
- It validates that id as class `0x14` (`0030CC29`/`0030CC32` -> `00322C50`).
- The same word becomes the row pointer at `0030CC7A`..`0030CC81`, and `0030CD99` passes that pointer to `0030CE10`. So
  the ids class `0x14` validates are the rows packet 1 tests.
- `00322C50` dispatches classes 1..32 (`00322C5A`/`00322C5F`/`00322C62`) through the image-relative table at
  `00323054`. Entry 19 (class `0x14`) is `00322F72`.
- That arm loads the descriptor `02EBF138` and its count `[+4]` (`00322F84`). The tail
  `0032302C`..`0032303B` accepts `0 <= id <= count-1`, signed. A null descriptor refuses everything.
- The shipped count is 543, so **class `0x14` accepts 0..542, which includes 511..534.** SPEC ran the shipping
  comparisons under injected state (emulation): exactly 0..542 are accepted, and the control counts 511 and 0 give
  their own boundaries.

**What it changes.** The class-`0x14` guard is removed as a possible exclusion of rows 511..534. It is not an
out-of-range filter for them. FABLE's model did not rely on it, so nothing is struck. The new constraint is only the
count premise: the descriptor installer `003845F0` does not rebase `+4`, so the file count of 543 is the runtime count
once the descriptor cell is installed. That the table stays unmodified afterwards is a premise.

**Stays open.** Slot allocation, the command, AI and script producers, the readiness helper `0030C890`, and loader, IO
and owner remain open. SPEC's caller sweep for class-setting forms is context, not a claim. No live run is needed:
the bound is settled statically, and further live or no-hit tests of it would be unproductive.

### 3. ASTRA-RETURN-FABLE-SPATTACK-REMAP-0930 (ACCEPT)

**Accepted scoped fact.** The native preload remap is the queue cell `022C2178`.

- **The encoding.** `0030DB70` stores to the cell only at `0030DC98`. Two branches reach that store:
  - the record branch encodes the WORD `w` as `w - 0xD0` (`0030DBD7`/`0030DBDA`), or -1 when `w` is FFFF
    (`0030DBD2`/`0030DBEA`);
  - the null-record branch does the same at `0030DC7B`/`0030DC83`.
- `003068D4` (inside `00306760`) encodes the same way (`003068CA`/`003068D1`).
- **The reader.** `00309C00` reports "unavailable" for -1 (`00309C06`..`00309C0D`). Otherwise it stores the value
  through `[rdx]` (`00309C13`) and **consumes** the cell, re-arming it to -1 at `00309C22`. The other -1 writer is
  `0030D722`.
- **The script adapter.**
  - `00348870` pops two integers and passes the **first** in EDX (`00348880`..`00348893`).
  - `0030EEA0` maps -1 to FFFF (`0030EEA8`/`0030EEB7`) and otherwise adds `0xD0` in BX as a 16-bit add (`0030EEB2`).
  - It hands the result as R8w (`0030EEF5`) to `0030CFB0` (`0030EF00`, `movzx ebx, r8w` at `0030CFC3`).
  - `0030D070` stores that word into the slot's `+0x1C` at `0030D14F`. That is the word packet 2's `0030CC25` reads.
- **The arithmetic.** This is a static model of those instructions over all 65536 words, not code execution:
  - only `0xCF` and FFFF are reader-unavailable, because `0xCF` minus `0xD0` is -1;
  - every other word decodes unchanged;
  - 511..534 queue as 303..326 and decode unchanged;
  - word 0 queues as -208.

**What it changes.** Two parts of FABLE's model change.

- **The remap is not a bound on the candidate ids.** Under the unchanged-transfer premise, rows 511..534 survive the
  queue and land in the slot word that packet 2's guard and packet 1's path read.
- **Neither the remap nor its inverse is universal.** `0xCF` and FFFF share the "unavailable" encoding, so a
  reconstruction must keep three things apart: the WORD wrap, the full -1 branch and the unavailable-queue sentinel.

SPEC's precision points are recorded as they stand:

- every direct writer encodes the same way;
- the reader has a second caller, `002D6175`, outside the script path, besides `0034838A`, so the cell can be drained
  before a script reads it;
- `0030EEA0` can return -1 (no unit, `0030EEC6`) or -2 (`[022C2170]` not 4, `0030EECF`/`0030EED8`) before the word
  reaches `0030CFB0`.

**Stays open.**

- The interpreter's value transfer is a premise. That is the `00309C13` store, popped later by `00267E10`. SPEC notes
  it can be settled statically.
- Producer admission is open, as are command, AI and authored selection, the natural queue and actor state, metadata,
  IO and owner submission, and indirect aliases. The five-instruction writer and reader set is a direct-reference
  census, not an alias closure.
- No natural sentinel selection is shown, and no claim is made that `0xCF` is ever queued naturally.
- The retained decompiled script lead and forced states are not reachability evidence.
- **Next discriminator** (static): the actual input domain of `002FFCF0` and the committed action producers.
- The render-executor half of `1f6569546` is not part of this review and is not consumed here. FABLE's existing render
  answer is unchanged.

### 4. ASTRA-RETURN-FABLE-ACTION-SELECTOR-EXCLUSIONS-0930 (ACCEPT)

This record incorporates only the two scoped exclusions.

**(a) The `raw+5 == 0` category-7 rejection.**

- In all nine tables, rows 511..534 have `+0x1E` = 7. ASTRA calls `+0x1E` the "category"; the
  [action-row page](../../../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md) names it the
  id-class byte. 235 rows per table have the value 7.
- `003060E0` first runs the class-`0x14` check, and a failure returns 4 (`0030610D`/`00306116`).
- A null raw record (`00306123`) or a nonzero raw byte `+5` (`00306129`/`0030612F`) returns 0 at `0030632C`. That
  path bypasses the category test.
- Otherwise `+0x1E` above 6 goes to `003062F4` (`00306181`..`00306188`). There 9 has its own arm, `0xFF` returns 0,
  and everything else, 7 included, returns 5 (`00306300`). The raw byte `+4` is not read on this path.
- `00306480` turns any nonzero result into `0x0F` (`003064A6`..`003064AF`) before its licence call `003064C5`.
- `002FFCF0` passes the unit's raw record `[unit+0x698]` (`002FFD05`, nonnull at `002FFD15`) to `00306480` at
  `002FFE9D`, and a nonzero return leaves at `002FFEA4`.
- `0030DB70`'s record arm then returns 1 at `0030DBC5`. That is before its stores `0030DBDF`, `0030DC8B` and
  `0030DC98`.
- So **with a nonnull raw record whose byte `+5` is 0, `0030DB70`'s record arm cannot queue rows 511..534.** With a
  nonzero `+5`, the category test is bypassed, and the exclusion does not apply.

**(b) The negative-override fallback byte bound.**

- `0030DB70`'s null-record arm sends `022C2190` values `0xE2`..`0xF1` straight to -1 (`0030DC34`..`0030DC4C`).
  Otherwise it calls `002F8D60` (`0030DC55`).
- With a negative override index `01EEBAF0` (`js` at `002F8D72`), the matcher's table walk has two exits:
  `movzx eax, byte [r10]` (`002F8E36`), which is 0..255, or -1 (`002F8E28`).
- The complete matcher has exactly three `ret` exits: `002F8D84`, `002F8E35` and `002F8E49`.
- The caller narrows the result to a WORD (`0030DC5A`), so a miss becomes FFFF. The class-`0x14` check
  (`0030DC68`/`0030DC6F`) or the FFFF test (`0030DC76`/`0030DC79`) then stores -1, the unavailable value.
- A byte hit queues -208..47. The candidates would need 303..326. So **rows 511..534 cannot come from the
  negative-override fallback.** The proof is the result width, not a count of authored threshold rows.
- `01EEBAF0`'s file value is -1. That is a file value, not live initialisation.

SPEC's emulation (injected state) gives:

- {5} for `raw+5` = 0 and {0} otherwise, over ids 511..534 and every `raw+5`;
- 163 distinct queued values, all in -208..47, over 300 random fallback tables;
- a sensitivity case: an override word of 511 queues 303.

**What it changes.** Two legs into the queue cell are now closed for the candidates: the record arm under a zero raw
`+5`, and the null-record arm under a negative override. The runtime obligation narrows to the real unresolved inputs.

**Kept exactly as ASTRA and SPEC state.**

- **A nonzero `raw+5` bypasses the category test.** No universal actor exclusion follows.
- **The nonnegative override is still OPEN.** It reads the WORD `022BE930[index*2]` (`002F8D74`/`002F8D7B`).
  FABLE's 2026-09-30 subsection on the battle-command page bounds it to 226..241 for a valid state 0..8 under its
  same-object premise. The writer and alias closure is still open.
- **Other producers are still OPEN.** These include `003068D4` and the other callers of `003060E0`, `00306480`,
  `002FFCF0` and `0030CFB0`. The packet restricts its claim to `0030DB70`'s legs, and SPEC confirms that scope.
- **`00306760`'s six-way dispatch is on the dword `022C215C`, not on the row's `+0x1E`.** It is
  `003067AA`..`003067BA` -> `00306AF0`, with the entries `00306931`, `00306A3D`, `003067DB`, `00306848`, `003069F8`
  and `00306A8E`, followed by int3 padding. The [mode-ladder page §2d](../../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md)
  names `022C215C` the special-sequence kind. The invalid ten-entry raw stays history.
- Stable raw/codec state across the preceding calls, and natural caller and actor selection, are premises.

## The OV-42 proposition that remains (FABLE)

On the special-sequence selector path (`0030CBE0` -> `0030CE10` -> `00306BD0` -> `0032FC30(3, w)`):

1. **The data candidates.** The only rows that can give a negative narrowed WORD are rows 511..534 (FFFF, bit 30,
   `+0x1E` 7). The row-`0x113` arm is a separate premise. Class `0x14`, the bit-30 test and the D0..F1 refusal do not
   exclude rows 511..534, and the queue remap preserves them.
2. **The excluded legs.** Two legs into the queue cell cannot carry them: `0030DB70`'s record arm when the actor's raw
   `+5` is 0, and its null-record arm when the override index is negative.
3. **What is OPEN.**
   - Whether any shipped producer puts 511..534 into a slot word (or the queue cell) through a remaining leg: a nonzero
     raw `+5`, a nonnegative override word, `003068D4`, the `00387090` effective-id leg into `0030CFB0`, or other
     callers.
   - Whether that happens with `00306BD0`'s prefix gates open, so that the owner request is actually made and rejected.

   Selector producers other than this path (field, eventread, summoneventread) are not touched. **Natural rejection in
   shipped play stays OPEN (RT)**, and OV-21 with it.

## Routed to other owners (no page of theirs is edited)

- **OPUS (types and contracts).**
  - **The action-row page's `+0x24` cell.** It says that on "the 62 summon-class rows, `+0x0C` bit 30 set, the word is
    the special-sequence load id". In the shipped table those 62 are the bit-30 rows that are not FFFF. 25 further
    bit-30 rows carry FFFF: `0x113`, which takes the actor-type arm of `00309230`, and 511..534, whose FFFF would reach
    `0032FC30` as selector 65535. This is a precision note, not a contradiction.
  - **The action-row page's `+0x1E` cell.** The value 7 on rows 511..534 is what `003060E0` maps to 5 when raw `+5` is
    0.
  - **The queue cell `022C2178` has no page.** Its contract has four parts, for OPUS to place if a contract owns them:
    - a dword holding `word - 0xD0`, with -1 meaning unavailable, so `0xCF` collides with FFFF;
    - one consuming reader, `00309C00`;
    - five direct-reference instructions;
    - the adapter ABI: the first popped integer in EDX, then R8w into `0030CFB0`.
  - **`00309230`'s row-`0x113` arm** indexes a 13-entry table by raw `+4` minus `0x1B` with no bound. That is a
    contract precondition, a type byte in `0x1B`..`0x27`, and it is still a premise.
- **ASTRA (its own packet text).** SPEC's correction wording for `SPECIAL-ACTION-RESULT.md` items 2 and 3 (radix of
  "Row113", the conditional D0..F1 refusal, the prefix gates, the ns8 sign) and SPEC's optional remap sentence belong to
  ASTRA's packet. FABLE does not edit it. The static next discriminators also belong to ASTRA, which chooses the method:
  - who produces 511..534 before `0030CE10`;
  - the input domain of `002FFCF0` and the committed producers;
  - the writer domains of `022BE930` and `01EEBAF0`;
  - the interpreter transfer `00309C13` -> `00267E10`.

## Consumer check (FABLE)

- consumer: `_index/OPEN-QUESTIONS.md` row OV-42: revised-here (a dated narrowing; the lead state stays PARTLY
  ANSWERED). OV-21 is not edited; its "OV-42 rejection probe" precondition is the proposition above.
- consumer: `the-nonempty-prf-registration-and-specialized-relocation.md`, OV-42 box: revised-here (a dated pointer
  sentence).
- consumer: `battle-command-availability-and-reason-codes.md`: revised-here, with a new FABLE subsection after the
  2026-09-30 OV-42 subsection. Its reason-code rows agree: "`0x0F` ... collapses four inner codes" and "`003060E0`'s
  codes (4, 5, `0x0F`, FFFF) collapsed to `0x0F` by `00306480`" agree with packet 4(a). Its `002F8D60` paragraph,
  "exhaustion -1", agrees with 4(b).
- consumer: `the-indexed-source-request-from-arm-to-terminal-pump.md`, FABLE 2026-09-30 subsection: agrees. Its next
  discriminator, "every non-debug selector producer's range into `0032FCA0`", is narrowed for one producer here and is
  not edited.
- consumer: `battle-runtime-mode-ladder.md` §2d (states 1 and 2 of `022C2160`, kind `022C215C`, owner `022C2168`):
  agrees with SPEC's prefix gates and with the `00306760` correction.
- consumer: `actor-type-id-partition-and-the-13-value-band.md` §5 (`00309230`'s `0x113` arm and its 13-entry table,
  42 + 3 x (type - `0x1B`)): agrees. It states no bound on the type byte.
- consumer: `native-command-seam.md` UQ-112 table (slot `+0x1C` the u16 action id, written at `0030D14F`): agrees.
- consumer: `the-action-definition-row.md` `+0x1E`/`+0x24`: agrees. The precision notes are routed to OPUS above.
- consumer: [`astra-returns-fable-0930`](../astra-returns-fable-0930/README.md) "Not consumed": it is superseded by
  this record for these four returns and is not edited. It was true when written: the review records arrived later,
  in `2e88eceef`.

## Controls (FABLE)

[`ov42_astra_check.py`](ov42_astra_check.py) decodes every cited instruction with the analysis kit's
`disasm_fn.py ADDR LEN`. It decodes linearly from each function's entry, or decodes only the cited instruction where
only its own bytes are claimed. It compares each decode with its exact text, and with its resolved rip target where
there is one.

It also reads three pieces of data with the same tool's section-aware reader: the class table `00323054`, the dispatch
table `00306AF0` and the file value of `01EEBAF0`. It re-tallies ASTRA's nine retained tables, and it runs the remap
model.

Controls:

- **K1:** a width-changed expectation at `003092C5` (byte instead of word, SPEC's own refusal case) must be reported as
  a mismatch.
- **K2:** the wrong kind mapping, `3w+1`, must find 39 counterexamples in each table, as SPEC measured.

Caller counts quoted above are SPEC's census, and they are not re-run here.

## Regression

run: ov42_astra_check.py at 5b8ffef20 (FAILS 0)
