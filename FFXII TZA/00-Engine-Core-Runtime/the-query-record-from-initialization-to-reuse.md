---
system: Encoded-ID query initialization, tagged outputs and reuse
category: 00-Engine-Core-Runtime
status: PARTIAL
owner_layer: native
evidence_tier: 1
readiness: BEHAVIORALLY UNDERSTOOD
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: "SECTION-05 selected original bodies; 200 bounded native assertions and retained EXP-143 reconciliation. No fresh live session or current Ghidra import."
last_reviewed: 2026-09-22
production_acceptance: "local checks passed; formal peer acceptance pending"
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-query-record-falsification-pass-1
---

# The query record, from initialization to reuse

This is the current reconstruction-oriented specification of the shared request/result mechanism.
It corrects the older universal-input, unwritten-tail and no-+54-writer claims without discarding
historical authored-table or caller surveys. See the [contract](CONTRACT-encoded-id-space-and-class-registry.md)
and [production review](../_experiments/evidence/continuation-section05-encoded-query/REVIEW.md).

## 1. There are three registries/representations, not one universal ID test

The fifteen-row inventory registry at `01EEBCC0` has 0x58-byte records. Its class field is +38;
`00309440` indexes the same field from the pre-biased base `01EEBCF8`. Neither representation moves
the true record origin. The shipped class word is nibble+5 for nibbles0..E; F maps to -1.
Thus `(nibble<<12)|index` encodes an inventory ID. `(class<<12)|index` is wrong.

The class validator at `00322C50` instead accepts 32 class tags. Most bounds come from loaded
row-descriptor count+4, not the inventory registry’s +3C. Three bounds are compiled constants;
class13 sums four descriptors; class1 derives a subclass from low16 but range-checks the original
full32 argument. The query filler has a separate 32-arm table and is not required to implement every
validator-admitted operation.

The third layer is `0031C5D0`'s tagged input: WORD+6 for classes1,5..11,13..18,30,31; DWORD+4 for
2..4,19..29,32; class12 reads neither. +6 overlaps the high half of +4. A wrapper only writes its
lane; it does not change the arm's interpretation. In particular class1’s rewrite to class19 does
not convert the existing WORD to a DWORD request. The synthetic word-form E000 fails with -2;
a direct correctly formed class19 DWORD E000 validates and returns -1.

## 2. Registry initialization includes a reset, not just pointer rebasing

`0030B6A0` visits all fifteen rows. At offsets00/18/28 it tests a QWORD for zero and, if nonzero,
computes the corresponding pointer at08/20/30 with a DWORD load and 32-bit addition. A zero slot
leaves its destination unchanged. An offset with only a nonzero high half still selects the write
and produces low32(state), not a null or a full64 sum.

The same loop writes each +40 exclusive prefix sum of earlier +3C counts, wrapping at32bits.
All shipped +40 cells are zero on disk; the cumulative values are runtime products. Current shipped
counts sum to6892. The function then clears512 bytes at state+57C8 and ANDs128 bytes at state+59C8
withF8. These final operations use the FULL state pointer, not the truncated pointer-lane base.

The two-address fixture maps a high state and its low alias separately. It verifies pointer
truncation, full-width reset, exact boundaries, zero-offset preservation, prefix overflow, and repeat
invocation. Repeating the call recomputes from source offsets and resets derived state again.
This is synthetic execution, not evidence that the installed game places its state above4GiB.

## 3. Success is a partial write; failure depends on which interface was called

`0031C5F0` clears QWORD+18 before dispatch. It does not clear the rest of the record. Selected
classes then write different outputs; some validate and succeed with only that common clear.

`0035D330` returns `022CA520`; `0035D380` returns `022CA480`. The first writes DWORD+4, the second
WORD+6. Both write the tag and call the filler. A negative return invokes the original `ret0` stub
and imported memset for all 0x98 bytes, then returns the record pointer. A successful call leaves
unassigned prior bytes intact. The name slot is cleared even when a direct fill rejects, and tag1
may already have rewritten the tag. A null name therefore does not uniquely encode failure.

A saved wrapper pointer is not a result snapshot. Further calls to the same wrapper alias it;
other wrapper calls use the other record. The next successful class can preserve fields from an
unrelated prior class. The fixture compares full sentinel-filled buffers, both failure paths and
successive calls, and verifies the untouched peer buffer.

Returned string pointers reference separate descriptor/text storage. The query does not allocate,
copy or free those strings. Their lifetime across resource unload/rebinding, and shared-record
thread/reentrancy constraints, remain separate unanswered obligations.

## 4. Query-class producer behavior

All rows below include the common name clear. Rows with data may additionally resolve a name through
their own row/text path; availability of a name is not identical to validity. DWORD stores from BYTE
or WORD sources widen the value unless a BYTE/WORD store is explicitly noted. These are current
producer distinctions, not assertions that every field's downstream purpose is understood.

| Class | Request lane | Distinguishing producer behavior |
|---|---|---|
| 1 | WORD+6 | Derives and stores subclass, redispatches without repacking input. |
| 2 | DWORD+4 | Party-name row; a decoded zero row base is tolerated on the tested path. |
| 3 | DWORD+4 | Name path through its descriptor. |
| 4 | DWORD+4 | Validator then0; no output beyond common name clear. |
| 5 | WORD+6 | Item price/source values, query modes0/1; row+0A must be readable when reached. |
| 6 | WORD+6 | Equipment row and subrecord, modes0/1, subtype fields, +54 bit0 replacement. |
| 7 | WORD+6 | Loot price/description/scalars and inventory query modes. |
| 8,9 | WORD+6 | Magick/technick row values and modes; class8 also consults its action row. |
| 10 | WORD+6 | Empty-string pointers08/10; QWORD zeros20/28; twelve strided DWORD sentinels38..90. |
| 11 | WORD+6 | Gambit conditions; +38 lookup indexed by row+10 BYTE, not row+3. |
| 12 | Neither | Immediate -2 at0031C650; no validator call or fallthrough. |
| 13 | WORD+6 | Three fixed key-item row intervals; +28=FFFFFFFF and modes0/1 even outside them when validation admits. |
| 14 | WORD+6 | Bundle fields including WORD views40/42; +20=0, +28=FFFFFFFF. |
| 15,30 | WORD+6 | First triple of WORDs from row0/2/4 into query38/3A/3C. |
| 16 | WORD+6 | +20=0; +28 from row DWORD0. |
| 17 | WORD+6 | Modes0/1 and +2C=FFFFFFFF. |
| 18 | WORD+6 | Bazaar row/pairs, price and flag-byte RMW; reads live good-state binding. |
| 19 | DWORD+4 | Valid E000..EFFE -> -1; other requests -> -2. No class row output. |
| 20 | DWORD+4 | Text pointers08/10; two bits from rowDWORD0C; conditional24/28 and BYTE30. |
| 21 | DWORD+4 | Command text pointer08, not10. |
| 22,23 | DWORD+4 | Constant-bound validation, then0 with only name clear. |
| 24 | DWORD+4 | School text pointer08 as well as its name path. |
| 25 | DWORD+4 | Licence byte/WORD views, description10, masked ownership bit24. |
| 26 | DWORD+4 | Status byte views; updates low5bits of25 while retaining high3. |
| 27 | DWORD+4 | Element-name path. |
| 28 | DWORD+4 | Category name and description10; not name-only. |
| 29 | DWORD+4 | Augment name and description10. |
| 31 | WORD+6 | Second triple of WORDs from row6/8/A, unlike classes15/30. |
| 32 | DWORD+4 | Alternate licence view with BYTE36; leaves description10 unassigned. |

The packet contains the exact 32 jump targets and one returned0x98-byte snapshot per class.
These snapshots are value observations under the fixture, not exhaustive write traces or proof
that all branch paths/authored rows were reached.

## 5. Bit54 and the tail: two false absence proofs replaced

The equipment arm reads row+7, derives bit1, and uses XOR/AND/XOR to replace query+54 bit0:

```asm
0031CA42 xor al, byte ptr [rbx+54]
0031CA45 and al, 1
0031CA47 xor byte ptr [rbx+54], al
```

This preserves upper7bits. Omitting read-modify-write instructions from a store census created the
incorrect 'read and never written' conclusion. Sentinel controls test both setting and clearing the
low bit; category variations confirm this write occurs before the subtype-dependent tail behavior.

Class10 has a different layout. It writes `FFFFFFFF` DWORDs at:

`38,40,48,50,58,60,68,70,78,80,88,90`.

The loop starts from query+3A, writes[RBX-2], and advances8 for12 iterations. Each intervening four
bytes remain unchanged; final94..97 are untouched by that loop. It does not touch54, but it DOES
write beyond64. These facts are compatible, not contradictory. Whole0x98 comparison rejects a
six-iteration mutant that would escape a prefix-only check.

## 6. Strings, row pointers and selected output semantics

The general decoder `0020E600` computes full64 `zero_extend(encodedDWORD)+relocationBase`. Query
row-stride operations then often use EAX and truncate that high half. The test gives the decoder
an extra4GiB but keeps a valid low alias: the original item row reads the low alias. Do not replace
all of these steps with one 64-bit pointer formula.

A synthetic two-name bank exercises the real nested encoded-pointer reads. The same query obtains
first one string then the other; the old string bytes remain separate. A missing text bank can yield
success with nullname. That does not establish allocated lifetime or all string error paths.

Class20 writes both the first resolved text to08 and the second to10. Its two-bit field at20 comes
from `(DWORD(row+0C)>>8)&3`, not the name word at34. It writes only BYTE30 from row13. If row0A is
zero, both24 and28 remain stale; otherwise type5/6 writes28 and other tested types write24.

Class25/32 WORD+2A comes from row+0C, not a duplicate of row+0A. Class32 adds BYTE36 and does not
assign description10. Status class26 replaces only low5bits of BYTE25. These concrete width and
preservation distinctions are tested separately from semantic names.

## 7. Inventory state is an input, not an immutable property of the ID

The original mode dispatchers read the current descriptor and its selected handler. For packed
classes the WORD has low10 total and high6 reserved. Mode0 returns total-reserved and mode1 total;
a synthetic over-reservation yields a negative result. Bitset modes return a tested ownership bit.
A missing query handler returns zero, even though four shipped classes have nonnull mutate handlers.
Full mutation/derived-index behavior remains on the historical mechanism page and is not rerun here.

Class13 further shows why a valid request does not imply a fully assigned record. Its validator sums
four descriptors, but the filler selects only 8000..803F,8040..805F,8060..81FF. The six endpoints
select their correct rows. With a nonzero fourth count, synthetic8200 validates and returns0 while
leaving row-derived fields untouched; +28 and modes are still assigned. Shipped reachability of that
fourth interval is not proven by this fixture.

## 8. Evidence and remaining obligations

The review pins19 original bodies and9 data ranges; native200/200, repeat identical, seven intended
code mutants rejected. No application callees are substituted. The original memset thunk remains
and only its import target is bridged. Counts and row contents are synthetic. Two null-row faults
occur only in disposable child processes at the original instruction addresses.

Retained EXP-143 review separately checks246 observed probe records and4 summary-only returns,
32 original jump entries and15 registry class words, with8 negative controls. The producer's173
counter mixes outer groups with individual probes; it is not a uniform execution count.

- [x] ~~Complete downstream meanings of every class-specific slot/strided element, and exact required
  caller invariants. No broad 'unused forever' conclusion follows from absent census hits.~~ *SUPERSEDED 2026-09-29 (SWE2-FRONTIER): duplicate of OV-1 - the same ask in substance; OV-1 carries it. Register OV-6.*
- [x] ~~Reentrancy, concurrency and borrowed-pointer lifetime across resource replacement.~~ *SUPERSEDED 2026-09-29 (SWE2-FRONTIER): duplicate of OV-2 - the same ask in substance; OV-2 carries it. Register OV-7.*
- [ ] **OV-8.** Actual game reachability of the deliberately abnormal counts/pointers/state layouts.
- [x] ~~Formal independent acceptance and claim-specific remaining major-system empirical coverage.~~ *NOT A QUESTION 2026-09-29 (SWE2-FRONTIER) under the class-2 ruling: an independent-acceptance/process item, carried by board task FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929. Register OV-9.*

The next architectural work is resource ownership/retention/release, not another repetition of
these query baselines. No L2 verdict, TEAM ownership, completion score or reconstruction source is
changed by this local production section.

## Falsification pass 1 — 2026-09-29 (OPUS): every structural clause survives

**Attack.** §1-§5's structural clauses became checks that fail if the shipping image says otherwise. The checks decode every
listed body in `.text`. Script: `Tools/analysis-kit/gfz-scripts/falsify_query_record.py`, output `falsify_query_record.out`,
image `73461d08…`, 0 BROKEN. The per-class value snapshots of §4 are EXP-143's and are not re-run.

| # | Clause attacked | Result |
|---|---|---|
| Q0 | §1 fifteen `0x58` records; class = nibble + 5; F → -1 | **survives**: the `+0x38` words are 5-19; `00309440` reads `01EEBCF8 + n·0x58` for n ≤ `0xE`, else `-1` |
| Q1 | §2 the initializer | **survives**: rows `01EEBCC0`-`01EEC1E8`; three 32-bit adds for `08/20/30`; `+40` the running sum of `+3C`; 512 bytes cleared at `+57C8` through the full pointer; `0x80` bytes ANDed with `0xF8` at `+59C8` |
| Q2 | §3 the two wrappers and the failure path | **survives**: `0035D330` writes the tag and DWORD `+4` of `022CA520`; `0035D380` writes the tag and WORD `+6` of `022CA480`. On a negative return, both call the `ret 0` stub `0016D6A0`, then memset `0x98` bytes |
| Q3 | §3 / §4 dispatch, class 1, class 12 | **survives**: QWORD `+18` cleared before the 32-arm table at image + `0x1FE598`; class 1 re-derives through `00309440` from WORD `+6` and redispatches; class 12's arm is the `-2` at `0031C650` |
| Q4 | §5 `+54` bit 0 | **survives**: `xor al, [rbx+54] / and al, 1 / xor [rbx+54], al` at `0031CA42` |
| Q5 | §5 class 10's tail | **survives**: twelve `FFFFFFFF` at `+38`..`+90`, step 8, from `rbx + 0x3A`; one string pointer at `+08` and `+10`; zeros at `+20` and `+28` |
| Q6 | §3 "the original `ret0` stub" | **survives**: `0016D6A0` is `ret 0`, three bytes, with 2,868 call sites. [The loader-bound sheet](../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md) called the same call an allocation; it is corrected there (`CON-166`) |

Consumer record: none needed, since nothing here was corrected. The regression is `falsify_query_record.py`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **ActorEntity — MECHANICAL (5 edges).** 5 ActorEntity-side calls into shared helper(s) the page cites (`BattleEncodedId_IsValidForClass` (00322C50)) - the helpers' general call surface, not a ActorEntity relationship of this page's subjects.
- **CombatAI — MECHANICAL (10 edges).** 10 CombatAI-side calls into shared helper(s) the page cites (`BattleEncodedId_IsValidForClass` (00322C50)) - the helpers' general call surface, not a CombatAI relationship of this page's subjects.
- **CombatAction — MECHANICAL (7 edges).** 7 CombatAction-side calls into shared helper(s) the page cites (`BattleEncodedId_IsValidForClass` (00322C50)) - the helpers' general call surface, not a CombatAction relationship of this page's subjects.
- **CombatFormula — MECHANICAL (1 edge).** 1 CombatFormula-side calls into shared helper(s) the page cites (`BattleEncodedId_IsValidForClass` (00322C50)) - the helpers' general call surface, not a CombatFormula relationship of this page's subjects.
- **Gameplay — CLIENT and SERVICE (10 edges).** 4 inbound (Gameplay bodies `0031C5D0`, `BattleEncodedId_IsValidForClass` (00322C50), `BattleSlotMap_ResolveMappedBattleSlot` (0031B9F0) call page-cited `00309440`, `BattleEncodedId_IsValidForClass` (00322C50)); 6 outbound (page-cited `0031C5D0`, `0035D330`, `0035D380` call Gameplay bodies `0031C5D0`, `BattleEncodedId_IsValidForClass` (00322C50), `BattleEncodedId_QueryMode0Positive` (0030B0E0)). Substantive edges include `00309440` is called by `0031C5D0`; `0031C5D0` calls `BattleEncodedId_QueryMode0Positive` (0030B0E0); `0031C5D0` calls `BattleEncodedId_DispatchQueryMode1` (0030AE30); `0031C5D0` calls `BattleEncodedId_DispatchQueryMode0Value` (00309EC0); the remaining edges run through shared helpers the page cites.
- **Items_Equipment_Shops_License — MECHANICAL (13 edges).** 13 Items_Equipment_Shops_License-side calls into shared helper(s) the page cites (`BattleEncodedId_IsValidForClass` (00322C50)) - the helpers' general call surface, not a Items_Equipment_Shops_License relationship of this page's subjects.
- **Movement — MECHANICAL (2 edges).** 2 Movement-side calls into shared helper(s) the page cites (`BattleEncodedId_IsValidForClass` (00322C50)) - the helpers' general call surface, not a Movement relationship of this page's subjects.
- **Party — MECHANICAL (9 edges).** 9 Party-side calls into shared helper(s) the page cites (`BattleEncodedId_IsValidForClass` (00322C50)) - the helpers' general call surface, not a Party relationship of this page's subjects.
- **Presentation — MECHANICAL (2 edges).** 2 Presentation-side calls into shared helper(s) the page cites (`0035D330`) - the helpers' general call surface, not a Presentation relationship of this page's subjects.
- **Save_Load_Settings — CLIENT (1 edge).** 1 inbound (Save_Load_Settings bodies `SaveRuntime_RebindImageBackedGameplayState` (00238A80) call page-cited `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` (0030B6A0)). Substantive edges include `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` (0030B6A0) is called by `SaveRuntime_RebindImageBackedGameplayState` (00238A80).
- **Status_Periodic_Terminal — MECHANICAL (3 edges).** 3 Status_Periodic_Terminal-side calls into shared helper(s) the page cites (`BattleEncodedId_IsValidForClass` (00322C50)) - the helpers' general call surface, not a Status_Periodic_Terminal relationship of this page's subjects.
- **UI — CLIENT (23 edges).** 23 inbound (UI bodies `00273E30`, `0027B880`, `0035D380` call page-cited `0035D330`, `0031C5D0`, `BattleEncodedId_IsValidForClass` (00322C50)). Substantive edges include `0031C5D0` is called by `0035D380`; `0031C5D0` is called by `002BFD20`; `0031C5D0` is called by `00273E30`; `0035D380` is called by `0027B880`; the remaining edges run through shared helpers the page cites.
