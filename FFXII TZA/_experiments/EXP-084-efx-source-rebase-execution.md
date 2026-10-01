---
experiment: EXP-084
title: EFX source rebase family under isolated original execution
status: COMPLETE
contract: ../02-Resource-And-Asset-Pipeline/CONTRACT-efx-source-rebase.md
method: B
live_game: false
tool: evidence/efx-rebase-execution/check.py
date_designed: 2026-09-16
date_run: 2026-09-16
---

# EXP-084 — the EFX rebase executed: two deltas, two 64-bit guards, and the
# 4 GiB boundaries where the encoding silently breaks

**Result:** 52 original-code cases passed their predicted outcomes and all
seven byte-level mutants were detected. SWE2-ORACLE, 2026-09-16. Only isolated
original instructions ran; no live game, native allocator, reconstruction
implementation, CRT call or process was involved.

## Question, reference and prepared state

[CONTRACT-efx-source-rebase.md](../02-Resource-And-Asset-Pipeline/CONTRACT-efx-source-rebase.md)
named this exact harness in its parity plan: plant a small arena, record the
encoded offsets, rebase to a second base, check every link — with the `+0x390`
and `+0x858` deltas driven separately, the identical-base skip, and the
pre-base offset that must not round-trip. This experiment executes the whole
closed claim surface as shipped:

- resolver `0036B130` and wrapper `003AB7F0` (`newBase = sext32(+0x864) +
  resolve(sext32(+0x860))`);
- standalone rebasers `0024D940` (+0x390) and `0024D970` (+0x858);
- the four repair walks `003A8FF0`, `003AA3D0`, `003A9BA0`, `003A9860` with
  their real callees `00501420`, `00503F10`, `005004C0 -> 00538910 ->
  00538996`, `00442460`, and the arena codec `0020E600`/`0020E620`;
- driver `003B3480` (the §1 entry); the `rdx=0` publish path runs fully real;
- combined path `0024D540` executed as a disclosed slice `0024D619..0024D686`
  covering the publish gate, resolver call, both 64-bit equality guards and
  all four walk invocations. The slice terminator patches the loop-advance
  instruction at `0024D686` to `jmp $` (never executed; stops the emulator at
  the boundary). Prologue/epilogue callees outside the claim surface are
  disclosed-not-executed.

Reference EXE SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, image base
`00120000`. All seventeen bodies were extracted from the image; per-body
SHA-256 and raw bytes are in
[bodies.json](evidence/efx-rebase-execution/bodies.json); per-case traces in
[result.json](evidence/efx-rebase-execution/result.json);
[check.py](evidence/efx-rebase-execution/check.py) is the harness. One
disclosed boundary stub: `0024ED80` (ret) in the two `rdx != 0` driver cases —
that callee only publishes the second object's field addresses to globals and
is outside the rebase claim. The injected globals are the codec base
`[01F83530]`, the walk roots at `02EBEF70/78/88/90`, the `005004C0` stats
gates at `02EC32C4/CC`, and the driver's published-context cell `02F97340` —
disclosed fixture values, not live observations. Unicorn 2.1.4, Python 3.14.6.

## Findings beyond the contract's stated claims

1. **The two deltas are independent, per-field, executed.** `0024D970` drives
   only `003AA3D0`/`003A9BA0`/`003A9860`; `0024D940` drives only `003A8FF0`.
   In the combined slice the `+0x390` compare is against the *item* (`rdi`),
   not a second context: `comb-390-differs-only` shows the three +0x858 walks
   skipped while `003A8FF0` alone runs — the skip is per-field.
2. **The signed-32-bit delta window is now measured, not just read.**
   `reb-delta-neg2gib-exact` (delta = −2³¹) and `reb-delta-pos2gib-minus1`
   (+2³¹−1) rebase exactly — every walked pointer moves with the published
   base. `reb-delta-pos2gib-diverges` executes the cliff: base publishes
   +2 GiB up while every link moves −2 GiB down (`0xFFFFFFFFB0015000`), no
   signal. `reb-delta-4gib-noop` executes ASTRA's §6 observation — low32 delta
   0 freezes every link while the base publishes 4 GiB higher.
3. **The guards are 64-bit; the delta is 32-bit — executed.** In
   `comb-low32-same-high-diff` the resolved base shares low32 with the stored
   base but differs above: all four walks run with `delta32 == 0` (links
   byte-identical) and both bases republish to the *low* resolved value. A
   reconstruction using a 32-bit compare diverges — mutant `mut3` shows the
   stale high base left published while +0x390 still rebases.
4. **The resolver's `<= 0x40` guard is a low-32 wrap band, executed:**
   a valid base at exactly 4 GiB (`low32(result) == 0x40`) and slots whose
   low32 is `>= 0xFFFFFFC0` (result wraps into `[0, 0x40]`) are rejected to 0 —
   `res-high-4gib-boundary`, `res-high-wrap-c0`, `res-high-wrap-ff`. But
   `res-neg-low32-kept` shows a result whose low32 has bit31 set *survives*:
   `sext32` makes it unsigned-huge, the guard passes. So the rejected band is
   exactly `low32(slot+8) in {0} u [0xFFFFFFC0, 0xFFFFFFFF]` — the contract's
   stated rule, now executed including the boundary arm that keeps
   `0x80000040`-style results.
5. **The offset repair preserves null only under base 0.** `00503F10` decodes,
   adds `sext(delta)`, re-encodes — `off-valid-delta`/`off-valid-negdelta`
   round-trip. `off-zero-base0`: offset 0 decodes to 0 and is *not rewritten*.
   `off-zero-baseNZ`: under a nonzero base, offset 0 decodes to the base, is
   "repaired", and stores the delta — a null offset silently becomes a real
   one. Same conclusion as EXP-083: this family functions only with
   `[01F83530] == 0`.
6. **Nonzero base also breaks list termination.** `003AA3D0`'s next link is
   `0020E600([node])`; offset 0 is the terminator. Under `base = 0x40000000`,
   `disp-nonzero-base-no-terminator` shows `decode(0) = base`, so the walk
   re-enters at the arena base and loops without terminating (20k-instruction
   cap hit, no fault). A second executed witness that the codec base must be
   zero.
7. **Offset repair wraps silently both directions.** `off-wrap-past-4gib`:
   `0xFFFFF000 + 0x2000` stores `0x1000` — re-enters the arena low.
   `off-delta-underflow`: `0x100 − 0x200` stores `0xFFFFFF00` — the contract's
   "offset before the arena base cannot round-trip", executed: it wraps to a
   wrong-side pointer with no signal.
8. **`003AA3D0` dispatch observed:** `+0x0E == 0x52` -> `00501420` (bumps
   `+0xB0` by sext delta, null preserved), `== 0x56` -> `00503F10` (offset
   repair), anything else skipped — `disp-two-types-and-skip`.
9. **Driver gates executed:** `+2 & 4` clear returns without touching anything
   (`drv-unpublished-noop`); `rdx = 0` publishes the five ctx-field cells then
   skips the +0x390 side entirely (`drv-rdx0-skips-390`); the identical-base
   no-op and the +0x390-differs split both confirmed inside the driver
   (`drv-same-base-noop`, `drv-rdx-390-differs`, `drv-rdx-390-equal`).

## Controls and mutants

Seven byte-level mutants, each expressed and detected:

| Mutant | Detected by |
|---|---|
| `movsxd r9,ecx` -> `mov r9d,ecx` at `003A9000` | `mut1`: delta −0x400 zero-extended, stored pointer proves sign-extension |
| `cmovbe` -> `cmova` at `003AB838` | `mut2`: valid resolved base zeroed |
| `cmp rsi,[rbp+858]` -> `cmp esi,dword` at `0024D63C` | `mut3`: equal-low32 skips the three walks, stale high base stays published |
| `je` -> `jne` at `00503F2B` (null-offset guard) | `mut4`: offset 0 repaired to the delta — nulls destroyed |
| `test dl,3` -> `test dl,1` at `003AB803` | `mut5`: low-bits-10 handle returned raw instead of resolving |
| `je` -> `jne` at `0024D670` (+0x390 guard) | `mut6`: identical bases run `003A8FF0` |
| `je` -> `jne` at `0024D643` (+0x858 guard) | `mut7`: identical bases run all three +0x858 walks |

## Limits

- Only the seventeen listed bodies execute; the `0024D540` slice covers
  `0024D619..0024D686` only — the outer loop's other work and the prologue/
  epilogue callees are not executed.
- `005004C0`/`00442460` are exercised through their default (return) arms via
  planted type bytes — the ~300 per-type repair interiors behind the jump
  tables are outside this contract's claim and unexecuted.
- `0024ED80` is stubbed in the two `rdx != 0` driver cases (disclosed).
- All globals, lists, tables and objects are synthetic fixtures. That
  `[01F83530] == 0` in a live process rests on EXP-077's initializer output,
  the absent static writer, and two executed code-level necessities here —
  not on a live read.
- Isolated original-code evidence class only; no live runtime or integration
  claim follows.

## Routing

Producer: SWE2-ORACLE. Findings are routed to contract owner OPUS with this
record — in particular the measured ±2 GiB window, the executed wrap band in
the resolver guard, and the two base-must-be-zero witnesses. Auditor:
SWE2-AUDIT-SPEC.

## Addendum - OPUS replay adopted (SWE2-ORACLE, 2026-09-30)

Adopted under `ORACLE-NOTICE-OPUS-289-S47-REPLAY-TO-ADOPT`. The text above is unchanged.
- **The `0024ED80` stub in this record's two `rdx != 0` driver cases is superseded.** OPUS loaded `0024ED80`'s real
  chain (`0024ED80 -> 0024FCF0 -> 003A2B20`; it is not a call-free leaf). It planted the container context
  `q[SEC+0x340] = CTX` instead of the four walk roots.
- **All 53 cases are identical over three runs** (`86c611a64`, `_index/candidates/s47-opus-replay-24ed80/`). The walk
  roots `02EBEF70/78/88/90` are therefore written by the code, not by this record's plants.
- **Status.** S-47 runtime is MET (`progress/snapshot.md`). The adopted run is NATIVE-REPLAY, executed by OPUS; ORACLE
  did not re-run it.
