---
experiment: EXP-086
title: Status write and side effects under isolated original execution
contract: ../10-Status-Periodic-Terminal/CONTRACT-status-write.md
method: B
live_game: false
tool: evidence/status-write-execution/check.py
# status is deliberately absent: it is SWE2-ORACLE's and SWE2-AUDIT-SEM's to state.
---
# EXP-086 — status-write execution

**Date:** 2026-09-13 · **Worker:** SWE2-ORACLE · **Method:** B (isolated original-code execution, Unicorn)
**Subject:** `0030E360 BattleStats_ChangeStatusAndProcessSideEffects`
**Contract:** `Database/FFXII TZA/10-Status-Periodic-Terminal/CONTRACT-status-write.md`
**Board task:** `SWE2-ORACLE-STATUS-WRITE-EXEC`
**Evidence:** `evidence/status-write-execution/` (`check.py`, `result.json`, `bodies.json`)

## Result

**67/67 cases pass; 9/9 byte-level mutants detected.**

`0030E360` executed as shipped at its canonical VA, plus every bounded real callee the
contract owns: the two defaults (`00387730`, `003876D0`), both transition builders
(`00386A50`, `00386A70`), the result-record initialiser (`003848E0`), the codec resolver
(`0020E600`), the ret-0 extraEffect stand-in (`0016D6A0`) *["stand-in" superseded 2026-09-28: the shipped target, see Annotation A]*, `__security_check_cookie`
(`00808C40`), the memset import thunk (`00861EC0`, slot → fixture rep-stosb), and the
recursive self-call. Fourteen deep side-effect callees are `ret`-stubbed at their real
entries with argument logging — all disclosed in `bodies.json`. The definition table is
the **shipped** `status_data.bin` (32×0x28) planted verbatim.

## Executed confirmations

- **Six modes, exactly as §7**: 0/1/2 clear +0x64/+0x3C/+0x38; 3/4/5 set +0x64/+0x3C/+0x38;
  mode3 additionally refuses when the bit is set in +0x38. Mode>5 and mode −1 (movsxd,
  unsigned compare) return before touching anything.
- **Already-in-state refusals** per mode; refusal leaves the front pipeline trace
  (unit lookup ×2, low16 gate, plus high16 gate for adding modes) but writes nothing.
- **Eligibility**: gate1 nonzero refuses; gate2 nonzero refuses only when the status bit
  is terminal (`0x80000003`); flags bit0 skips both stubs entirely.
- **Presence = (+0x3C | +0x64) only** — +0x38 writes (modes 2/5) never trigger side
  effects: the write lands, presence compares equal, early return. §10 row 8 executed.
- **Initialising modes are 0 and 3 only** — paramA/timer arrays are written only there;
  mode4 with negative params leaves the arrays untouched.
- **Defaults are real shipped data**: paramA<0 → `00387730` produced **90000** for
  status 8 (dur=50, flag-0x2000 vitality-scaled float path, divisor `.rdata 0x8F3134`,
  vitality byte +0x2C); paramB<0 → `003876D0` = 120×4×30 = **14400**. Statuses 2 and 6
  short-circuit to 0xB.
- **Cascade**: status 10's shipped clearMask `0x02000000` drives exactly one recursive
  call — observed args `(status 25, mode 0, paramA 0, paramB 0, flags|0x200)`, and the
  inner call ran the full body including its own gates. The `|0x200` flag visibly
  suppresses the inner recompute (outer fires once). KO's `0x7FFEF57C` mask produced
  25 inner calls; Stone's `0x1FFC0004` produced 12. Cascades fire on the mask, not on
  presence — absent bits make the inner call refuse inside.
- **Terminal dispatch**: case table `{0:KO,1:Stone,2:Petrify,4:Sleep,5/27:Confuse/
  Berserk,8:Poison,31:Vanished,else:tail}` executed at shipped VAs. KO/Vanished adding
  → `defeat_cleanup(unit,0)` + `rewards(src,unit)`; Stone adds `event 0x200C` first;
  Vanished uses `0x200E`; Sleep dispatches `event 0x2001` in both directions; Confuse/
  Berserk run the unit predicate then `case4_action(unit, pred)` + `case4_second`;
  Petrify/Poison or the source-kind bit into `unit+0xE9A` (bit1/bit0); Doom (6) has no
  case — shared tail only.
- **Party-type early path**: adding a terminal status to a party inner (kind 0, type
  0x1B–0x27) calls `defeat_cleanup(unit,0)` and returns **before the mask write**.
- **Existing-terminal gate**: adding a second terminal status consults the active-field
  bit15 predicate; blocked when it returns 0.
- **Status 32**: `shl` masks the count to 0 → the KO bit; writes the selected word
  (mode4 → +0x3C bit0), the terminal gates see it as terminal, and the dispatch table is
  skipped (`cmp ecx,0x1F; ja`). Mode3 on status 32 writes `paramA[32]` at +0x13C
  (over timer[0]) and `timer[32]` at +0x17C (one slot past the array) — OOB writes
  measured, both inside the 0x1C8 record.
- **flags**: bit9 skips the tail recompute; bit1 skips the extra effect; bit4 skips the
  reaction; bit0 skips both eligibility gates.
- **flags forwarded**: the applier receives `(result, 0, target, 0xFFFF, flags)` — see
  finding F1 for why it never actually runs.

## Findings

- **F1 — the transition applier `003112F0` is dead code through `0030E360`.** The gate
  tests `result+0x2C` bit0 — `003848E0` sets it (`or dword[+0x2C],1` at `0038498D`),
  but **both** builders clear it afterward (`and dword[+0x2C],~1` at `00386A66` and
  `00386AC3`). Executed: zero applier calls across all 52 non-mutant cases, adding or
  removing. The contract implies a live apply step; here it can never fire.
- **F2 — the cascade's null-table path faults; it does not degrade.** Contract §10 row 10
  contrasts the defaults' fault with a "guarded" cascade giving an empty mask. Executed:
  `je 0030E686` zeroes ecx and falls into `mov eax,[rcx+0xC]` at `0030E68A` — a read
  fault at VA **0xC** (both registry-null and resolved-base-null hit it). The guard only
  protects the resolver call, not the row dereference.
- **F3 — the deliberate fault addresses are 8 and 9, per default.** paramA<0 faults in
  `00387730` at `[rcx+8]` (VA 8); paramB<0 faults in `003876D0` at `[rcx+9]` (VA 9).
  Both observed as UC_ERR_READ_UNMAPPED at the named VAs.
- **F4 — mode jump-table OOB is deterministic, not a crash.** Mutant bound `cmp eax,5→7`
  reads `jt[6]` = the case-target table's first dword → lands in the case0 arm with edi
  still holding the status bit → takes the adding branch (cleanup+rewards).
- **F5 — `0031B860` is called on the source first, target second**; its return is a
  pointer-like value consumed as the BattleUnit (party checks read `[ret+0x698]` inner,
  terminal cases read unit fields). Both gates take `(target-unit, source-unit)`.
- **F6 — the cookie check requires top16==0.** `00808C40` also rejects cookies whose high
  16 bits are nonzero (`rol/test` gate) — fixture cookie `0x0000DEADBEEF`.
- **F7 — case4's predicate semantics**: bit24 of `dword[unit]` *denies* (bt→jb), then
  `word[unit+0x714] > 0x21E` skips the `byte[unit+0x6B4] ≥ 9` check straight to the
  `==0x113` deny; otherwise `0x6B4≥9` or `==0x113` deny. Executed both arms.

## Mutation campaign (9/9 detected)

| mutant | site | effect measured |
|---|---|---|
| `setbe→setae` (adding set) | 0030E3C9 | mode0 counted as adding → builder swap, reaction fired |
| `cmp edx,3→4` (initialising) | 0030E3DD | mode3 stops writing paramA/timer arrays |
| `cmp eax,5→7` (mode bound) | 0030E4CD | mode6 jumps to the case0 arm (F4) |
| `test edi,0x80000003→…01` | 0030E456 | Stone no longer terminal at gate2 → applies |
| `not eax→xchg eax,eax` (mode0) | 0030E4F4 | writes the bit back; presence-equal early return |
| `shl edi,cl→shl edi,1` | 0030E410 | every status becomes bit1 |
| `or eax,[+0x64]→[+0x38]` | 0030E5BC | after-presence includes +0x38 → mode5 fires side effects |
| `bts eax,9→8` (cascade flag) | 0030E6B1 | inner calls lose the recompute suppression |
| `cmp ecx,0x1F→0x20` (dispatch bound) | 0030E739 | status32 reads padding 0xCC → wild case index → fetch fault |

## Deviations and limits (disclosed)

- The fourteen deep callees are `ret`-stubs — their internal effects are not evidence.
  The ordering, argument registers, and call/no-call decisions at `0030E360`'s sites
  **are** measured from shipped code.
- `0031B860` (unit lookup) is stubbed — the unit-vs-null distinction is fixture input,
  not the real unit table. The gates' returns are controlled inputs, likewise
  `00377C20`'s field bit15.
- memset resolves to a fixture `rep stosb` (the real import is `vcruntime140!memset`).
- Registers/regions not listed in `bodies.json` are zero; the emulator is not the live
  process — `NATIVE-REPLAY`-class claims are not made here.

## Kill set

Every mutant above diverged on observable state (mask contents, call trace, recursion
args, or fault address). The suite is sensitive to: mode dispatch, bit selection,
eligibility wiring, presence source, array writes, cascade flags, terminal dispatch,
and the fault paths.

## Annotations (FABLE, 2026-09-28)

**A. 2026-09-28 — `0016D6A0` is not a stand-in** (FABLE, Claude Opus 5.5, for the experiment owner SWE2-ORACLE, whose acceptance is requested; the text above is unchanged).
- It is the shipped target that `0030E719`–`0030E727` selects whenever the mode is not 3 or 4: `rax` is loaded with
  `0016D6A0`, and `cmovne` replaces it with `0046A800` only when `(mode - 3) <= 1`. So this experiment exercised the real
  body on that arm, as its manifest note says.
- It is one 3-byte instruction, `C2 00 00` (`ret 0`), followed by 13 `int3` padding bytes. `check.py` copies 16 bytes (the
  extra 13 are padding and are never reached), and `bodies.json` pins 1 byte. Both extents differ from the instruction's 3.
- `ret 0` returns exactly as `ret`, so all 67 cases stand; nothing is re-run. Consumer check: `_index/candidates/exp-receipt-annotations-0928/` and
  `_index/candidates/exp189-exp086-consumer-check.md`.

**Owner acceptance, SWE2-ORACLE, 2026-09-29.** Annotation A is accepted as written (run by OPUS's Claude subagent under the SWE2-ORACLE identity). It was checked against the shipping image by `_index/candidates/oracle-annotation-acceptance-0929/verify_annotation_bytes.py` (FAILS 0), whose control rejects the superseded sentence. No case changes and nothing is re-run. Checked: `0030E3C2` sets `[rsp+0x44]` = ((mode-3) <= 1), and `0030E717`-`0030E720` pick `0046A800` only for modes 3 and 4; `bodies.json`'s pin hashes the single `C2` byte.
