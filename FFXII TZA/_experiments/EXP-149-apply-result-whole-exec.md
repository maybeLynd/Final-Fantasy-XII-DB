---
experiment: EXP-149
title: Apply-result-to-target — whole-applier execution of 003112F0 with
  the REAL callee layer (numeric setters 00300530/00300520/00300CE0/
  00300C90/00300BC0 and the six-mode status engine 0030E360), closing
  EXP-060's stubbed-setter gap
contract: ../07-Combat-Action/CONTRACT-apply-result-to-target.md
method: B
live_game: false
tool: evidence/apply-result-whole-exec/check.py
---
# EXP-149 — apply-result-to-target: whole applier, real callees

> **SECTION-01 correction/consumption (2026-09-22):** all 36 retained assertions
> replay, but that does not validate every interpretation below. Direct parameter
> copy-through exists; dirty records selected branches, not callee success; input
> pointers are stats, and `0031B860` resolves their owning units. Original producer
> code/results remain unchanged as historical evidence. This record's corrected
> wording and unresolved harness issues are detailed in the
> [review](evidence/continuation-section01-result-install/REVIEW.md).

**Contract:** `../07-Combat-Action/CONTRACT-apply-result-to-target.md`
**Scope:** the full applier `003112F0` (0x7F8) including the numeric
dispatch `00311608–00311777`, plus the contract's two remaining
unexecuted entries `0030E360` and `00300530` — now run as shipped
bytes instead of EXP-060's no-op setter stubs. EXP-148's callees
(`30E130`, `30FED0`, `30C650`, `3008A0`, `316A50`) also run real.
**Method:** NATIVE-REPLAY — shipped bytes under Unicorn; fixtures are
disclosed MODEL-PROVEN plantings of BSS/descriptor state. No EXE bytes
modified.
**Harness:** `evidence/apply-result-whole-exec/check.py`
**Result:** `evidence/apply-result-whole-exec/result.json` —
36/36 cases, 0 failures, stable across 3 processes.

Scripted boundaries (entry-intercepted, args + stack dwords recorded,
disclosed): `0031B860` (per-input unit→record map), `0030B9B0`,
`0030B8E0`, `00377C20`, `003283D0`, `0028F1F0`, `00316D70`,
`00469BB0`, `0032A150`, `00306F00`, `003299B0`, `0030B770`,
`0030B7F0`, `0030E060`, `002FA540`, `00385BA0`, `003A1180`,
`002DF220`, `00253770`, `00253690`, `00254EE0`, `00300FC0`,
`003105D0`, `00319E30`, `00387730`, `003876D0`, `00386A50`,
`00386A70`, `00386AE0`, `0046A720`, `0046A790`, `0046A690`,
`0035D8C0`, `002EACD0`, `00329210`, `0031E9A0`, `00323890`,
`002FEF30`, `003165C0`, `00315E90`, `00316BF0`, `008632B0`,
`00309F30`, `0030EA40`, `003279B0`, `00808C40` (canary),
`00300140`, `00301140`, `00307D10`, `003284D0`, `0046A800`,
`0016D6A0`, `00312280`, and **nested** `003112F0` re-entry (not driven: notify structs stay clear;
the harness entry shortcut precedes its nominal nested-entry intercept, so that
intercept is not evidence of tested recursion handling). `00861EC0` (memset) is implemented in the hook.

## 003112F0 — applier `(rcx=record, rdx=sourceStats, r8=targetStats, r9w=actionId, [arg5]=callerFlags)`

Executed structure, in order:

1. `r15 = 31B860(src)`, `rsi = 31B860(tgt)` — source/target **owning units**.
   The stored fixture names `trec`/`srec` mean owners; `tgt`/`src` mean stats.
   `[rsp+0xA0]` = arg5 (extended flags).
2. `arg5 bit0` clear → `30B9B0(tgtRec, srcRec)` aborts on nonzero
   (executed `ap-gate-block`; `arg5|1` skips it entirely).
3. `385BA0(actionId, sourceStats, targetStats, record)` metadata/event boundary.
4. `rec+0x2C` bit19 → `b[tgtRec+0xE9A] |= 8`; bit14 → `3A1180(0x34)` →
   `2DF220(0x40, ret, 0x7F)` → `b[tgtRec+0xE9A] |= 4`.
5. `b[rec+0x11C]/+0x11D != 0xFF` → `30C650(tgt|src, movsx level, 0)`.
6. **Steal loop** (member targets): `q[tgtRec+0x698]` → member,
   `b[member+5]==1` required; slots `i<3`: `b[rec+0x32+i]` nonzero and
   `w[q[tgtRec+0xE60] + 0x32 + 2i] != 0xFFFF` → `3008A0(item,1,0,1,0)`
   → `btr b[q[tgtRec+0x6A0]+0x14], i` → `253770(i+3, 1)`.
   **The `lea r12d,[rax+0x31]` folds the clobbered `movzx eax,b[rax+5]`
   result (always 1) into the constant** — the steal table base is
   `q[rec+0xE60]+0x32`, i.e. `+0xE60` on the resolved record is a
   POINTER to the block holding the three steal words. (Earlier
   static reads mis-modelled it as `member+0x31`.)
7. `d[rec+0x38] != -1` → `3008A0(item, 1, 0, 1, 0)` item write.
8. `d[rec+0x54]` SET mask → per set bit `E360(tgt, srcUnit, bit,
   r9d=d[rec+0x5C+bit*4] duration, stack: w[rec+0xDC+bit*2] word,
   flags2-derived, mode=3)`. `d[rec+0x58]` CLEAR mask → same with
   mode=0. So `+0x5C/+0xDC` are the per-bit duration/word ARGS of the
   E360 calls. **After the loops the applier itself also copies each nonnegative
   dword/word to `targetStats+0xBC/+0x13C`, even when both masks are zero**
   (`003115B6..00311606`). The existing `ap-copythrough` sets a status bit as well,
   so it does not distinguish those two writers; SECTION-01 adds that control.
9. **Numeric dispatch** (`d[rec+0x2C]` flag word):
   - bit8 → target HP: `edx=d[rec+0x24]`; bit3 → `300520` absolute
     shim, else `300530` delta. Setter flags are input bit19→output8, bit10→output5,
     inverted bit18→output6, inverted bit6→output4. There is no unconditional
     `0x400`; input presence alone produces `0x50`.
   - bit14 → target MP: `edx=movsx w[rec+0x2A]`; bit4 → `300C90`,
     else `300CE0`.
   - `b[rec+0x1D] != 0` → `300BC0(tgt, movsx w[tgt+0x28] * movsx b1d,
     flags)` — clamped inside 300BC0 to `[0, w[tgt+0x28]]`.
   - **bit7** → source HP: `edx=d[rec+0x20]`; bit1 → `300520`, else
     `300530` on src. (The discarded working assumption used bit31; EXP-060's published dispatch already used bit7.)
   - **bit13** → source MP: `edx=movsx w[rec+0x28]`; bit2 → `300C90`,
     else `300CE0`. The call's flags word is
     `(~(d[+0x2C]>>7)&0x10)|((d[+0x2C]>>10)&0x20)` — bit 7 enters
     **inverted** as `0x10`, bit 10 as `0x20` (`00311753`–`0031176A`;
     owner verdict, EXP-149 consumption).
10. `b[rec+0x3C..0x3D]` (≠0xFF) → `E130(tgt, byte, 0, flags, mode=2)`
    sets the bit in `b[tgt+0x68+bit>>3]`; `b[rec+0x3E..0x41]` → mode=0
    clears in the same `+0x68` array.
11. `w[rec+0x42..0x50]` (skip negatives) → `w[tgt+0x17C..0x18A]`.
12. Member adds `w[rec+0x11E..0x125]` → `w[tgt+8/0xA/0x12/0x14] += val-1`
    per non-0xFFFF entry (member units only).
13. Effect bytes `b[rec+0x128..0x12B]` OR into `flagobj+0x7B,0x79,
    0x78,0x7A`; `b[rec+0x12C..0x12F]` AND-clear the same;
    `d[flagobj] |= 0x80`.
14. Gil: `253690()` → `254EE0(?, max(0, gil - d[rec+8]))`.
15. Tail: `b[tgtRec+0xE9A] &= 0xF3`; `FED0(tgt, 0)` iff tgt exists,
    `arg5` bit9 clear, **and** `r14d` dirty — set by selected E360/E130 calls and
    foe stat/effect branches even if a callee makes no change. Direct parameter
    copies, numeric writes and `+0xE9A` marker branches do not set it. Executed: `ap-dmg`
    (pure damage) fires no FED0; `ap-copythrough`/status cases do.

## 00300530 — HP setter `(rcx=targetStats, edx=delta, r8=sourceStats, r9d=flags)`

- `rbx=31B860(unit)`, `rbp=31B860(src)`; `30B9B0(rbx,rbp)` aborts.
- **delta<0 && `(d64|d3c) & 0x80000003`** → `377C20` can-die consult;
  0 aborts the entire setter. (Observed in isolated replay `ap-full`: the
  status-SET mask lands KO bit0 in `d64` *before* the HP dispatch, so
  a negative delta there consults 77C20.)
- `newHP = oldHP + delta`; floor `d[tgtRec+0x48]`; cap `d[unit+0x24]`
  doubled when `bt(d64|d3c, 0x1C)`; **bit16 (`0x10000`) set → cap =
  max(oldHP,1) — the no-heal freeze** (executed `ap-cap-freeze`).
- Notify: `3283D0` when `r13d`; `28F1F0(d[tgtRec+8], newHP)` damage
  number; `316D70(srec+0x778, q[srec+0x10])` provoke lookup → `r13d`.
- Store gate: store `d[unit+0x48]=newHP` when the stored flag spill is
  set, OR delta>0, OR `30B8E0()==0`.
- **delta>0 && secondary gate ≤0 → `E360(unit, src, bit0, 0,0,flags,
  mode=0)` — the revive path** (clears KO from `d64`).
- **delta≤0 && newHP ≤ floor → lethal**: optional `469BB0` pre-death
  hook, then `E360(unit, src, bit0, -1,-1, flags, mode=3)` — **KO is
  bit0 of `d64`** (mode3's set field; EXP-060 stubbed the setters and established no KO field). Then `d[tgtRec+0x30] = d[srcRec+8]` killer id (executed:
  0xBEEF landed); `q[tgtRec+0x698]` member `b5==1` →
  `inc w[q[tgtRec+0x6A0]+8]` kill counter (executed: 0→1) → `32A150`
  → `f[01EAE0B7]*f[00908D80]` → `d[flagobj+0xC] = remainder`; then
  `306F00` gate → `3299B0(tgtRec, edx, killerid)` credit message,
  `edx = 0x200E` if flags bit8 else `0x2008 - (provoke!=0)`.
- Non-lethal negative delta → `3299B0(tgtRec, r13d+0x2005, killerid)`.

`00300520` is the absolute→delta shim (`edx -= d[unit+0x48]`, falls
into 300530). `00300CE0`/`00300C90` are the MP analogues
(`w[unit+0x4C]`, cap `w[unit+0x28]`, `30B770`/`30B7F0` gates, gain
spillover → `300BC0`, decrease → `2FA540`). `00300BC0` adds into
`w[unit+6]` clamped `[0, w[unit+0x28]]`.

## 0030E360 — six-mode status engine

`(rcx=unit, rdx=srcCtx, r8d=bit, r9d=duration, stack: word, flags, mode)`

- Resolves stats via `31B860`; `30B9B0`/`30B8E0` gates; `377C20`
  consult on the KO-bit path.
- **Mode table (jump table verified at ship bytes):**
  0 → clear `d64` · 1 → clear `d3c` · 2 → clear `d38` ·
  3 → set `d64` (requires bit absent from BOTH `d64` and `d38` —
  executed `ap-st-d38lock` refuses) · 4 → set `d3c` · 5 → set `d38`.
  The earlier assumption "mode3 → d3c" was wrong.
- Set arms store `d[stats+0xBC+bit*4]` duration (via `387730` when the
  arg is -1) and `w[stats+0x13C+bit*2]` (via `3876D0`).
- Linked bits: `q[02EBF118]` table → element `+0xC` mask → recursive
  `E360` with **mode 0 + flags|0x200** (exclusivity).
- Per-bit arm dispatch (executed): bit0 → `301140` + `300FC0` +
  `312280` (KO kill/notify — **not** `299B0`, which is bit3's arm);
  bits4/27 → `300140`+`307D10`; bit3 → `299B0`; bit2/bit8 → `e9a`
  flag-byte writes; bit31 → `30E85E`; others → no-op.
- Notify block: `memset` 0x148-byte struct; set-modes → `386A50` +
  `3284D0` + `46A800`; clear-modes → `386A70` + `16D6A0`; a set
  `b[struct+0x2C]` bit would re-enter `3112F0` (boundary'd).
- Tail `FED0(unit, flags)` unless flags bit9. Idempotent set exits
  before the notify block (executed — no `memset` in trace).

## Boundary honesty

Replay over synthetic fixtures: the descriptor cells, unit/member/
record blocks, steal/gil state are planted. This proves the applier's
and callees' executed semantics at shipped bytes — dispatch bits,
clamps, KO/kill-counter/killer-id chain, FED0 gating — but does not
prove the in-engine call sites initialise the same state, and the
scripted helpers' own bodies remain their own scopes.

## Addendum - OPUS replay adopted (SWE2-ORACLE, 2026-09-30)

Adopted under `ORACLE-NOTICE-OPUS-288-S21-REPLAY-TO-ADOPT`. The text above is unchanged.
- **`00385BA0`, scripted here, has since run as shipped code** inside the whole applier, in a copy of this harness
  (`6f1c17e98`, `_index/candidates/s21-opus-replay-385ba0/`). All 39 cases are identical over three runs.
- **The three new cases held the prediction:** `b14` = `0x02` / `0x02` / `0x00`. The last is `ap-steal-empty-meta-real`,
  where a set record byte on an empty (`0xFFFF`) steal slot clears the availability bit. The scripted boundary gives
  `0x02`, so `ap-steal` in this record could not tell the two apart.
- **The claim this corrects.** Read "the applier's own `btr` requires id != `0xFFFF`" as the applier alone.
  `00385BA0` clears `spawn+0x14` bit i with no steal-id test.
- **Status.** S-21 runtime is MET (`12412035c`). The adopted run is NATIVE-REPLAY, executed by OPUS; ORACLE did not
  re-run it.
