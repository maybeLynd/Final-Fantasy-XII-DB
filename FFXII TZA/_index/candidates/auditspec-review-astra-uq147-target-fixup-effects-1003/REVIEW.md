# SWE2-AUDIT-SPEC review: ASTRA's conditional target-fixup effects and the EXP091 producer gap (uq147-target-fixup-effects)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not ASTRA) · 2026-10-03 · Task: `ASTRA-REQ-SPEC-UQ147-TARGET-FIXUP-EFFECTS-1003` · Commit reviewed: `f49bb402137d2c20aadd03b21e2fd7495c63ca6d` · Package: `_experiments/evidence/uq147-target-fixup-effects/`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The bounded effect closure holds at the bytes, the producer re-runs byte-identical, and the producer-gap finding about
EXP091 is correct and correctly scoped: it removes EXP091's support for one branch, it does not invalidate the other cases.
The repair is routed (ASTRA-REQ-ORACLE-EXP091-RESOLVER-BASE-CONTROL-1003, which waits on this verdict).

## SWE2-AUDIT-SPEC identity and reproduction

- `manifest.json` sha256 `edabefc1b03719c4dde4dfe4c6ca1db199d72e8e6bc3ec1e508645c69a40f398`, as named (48 members).
- Producer `prove-target-fixup-effects.py` `31bd50f7…` in both the package and ASTRA's working copy, matching
  `prove-target-fixup-effects-02.status.json` (terminal, exit 0). Re-run to a fresh scratch path: exit 0, stdout
  `Conditional target-fixup closure writes only flag52; legacy EXP091 initializes resolver base at wrong address, with no
  retained action-row positive control.`; output **byte-identical** to `result-target-fixup-effects-02.json`.
- Qualifier: run 02 exit 1 (failed, preserved), run 03 `c1c798f6` exit 0; the current CLI control `613fc4f3` records the
  producer refusing the failed qualifier (exit 1, no result) - a fail-closed path.

## SWE2-AUDIT-SPEC the effect closure at the bytes (`disr.py`, image 73461D08…, base 0x120000)

`002FEAD0` (0xAC B):
- Every write is to `dword [rbx+4]`, six of them in three and/or pairs (`002FEB0C`/`002FEB1B`, `002FEB54`/`002FEB5E`,
  `002FEB69`/`002FEB73`), each `and 0xFFEFFFFF` then `or (c << 20)` - bit 20 of that dword, i.e. bit 52 of the qword at
  `+0`. No `+0x714`, `+0xBA0` or battle-mode store in this body.
- The contributor loop runs `edx` 0..31 (`002FEB4F cmp edx, 0x20` / `jl`) over `d[+0xEA4]`, comparing with `b[+0xEA9]` and
  `b[+0x6B6]` - the 32-contributor bound.
- `002FEB03 call 0x30C0E0` is made with whatever `rcx` holds (the stats pointer or `00377C20`'s leftover).

`0030C0E0` (0x122 B) - the incoming-RCX independence:
- `rcx` is never read: the body starts `xor edi, edi`, calls `00236850` (slot count) and then `mov ecx, edi` before
  `00236820` - so the argument is overwritten before first use. It walks the global roster from index 0 to the count,
  testing each unit (`[rax] & 0x10`, stats `+0x698`, the `0x80000003` mask / `00377C20`, `+0x6B6 == 0`, the focus target via
  `0031B7E0(d[+0x710])`, the target's kind byte `+5 == 0`, `w[+0x714] <= 0x21E`), then resolves `[02EBF138]+0xC` through
  `0020E600`. Any qualifying party-kind-0 target satisfies it - as the result states.

## SWE2-AUDIT-SPEC the EXP091 producer gap

- `0020E600` is `mov eax, ecx` / `add rax, [01F83530]` / `ret`. EXP091's harness
  (`_experiments/evidence/commit-callees-exec/check.py` L154) plants the stored base at `G_IMGB = 0x1F85D30`, 0x2800 above the
  cell the shipping code reads; the bazaar harness (`bazaar-callees-exec/check.py` L90-91) already uses `0x1F83530` and notes
  the difference.
- The retained EXP091 result (`result.json`) and bodies contain **zero** `imgadd` (the harness's label for `0x20E600`)
  events: no retained case reached the action-row branch, so its 87 baseline PASS + 10 mutants cannot qualify that branch.
  This does not invalidate the cases that never reach `0020E600` (bit 22, the copy cases, the mutations), as the request
  says.

## SWE2-AUDIT-SPEC limits

Static and bounded; no native case or mutation was re-run or credited. The helpers before `002FEAD0` on the KO path
(`00313B30` and others) are not closed by this package; natural KO / Esper pending-0x113 admission, time, lifetime and
scheduling stay open. Producer integrity and the old native PASS are not semantic acceptance - this record is the
semantic review.
