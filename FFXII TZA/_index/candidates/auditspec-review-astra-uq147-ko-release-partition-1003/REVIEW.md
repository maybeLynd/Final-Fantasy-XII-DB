# SWE2-AUDIT-SPEC review: ASTRA's KO cleanup partition - target release and action restoration (uq147-ko-release-partition)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not ASTRA; independent of FABLE's separate review) · 2026-10-03 · Task: `ASTRA-REQ-SPEC-UQ147-KO-RELEASE-PARTITION-1003` · Candidate commit reviewed: `d02293770e149fae885dbf77c8282b8f7ed1399d` (scientific content only - its publication receipt is adjudicated separately in `swe2frontier-interrupted-publish-receipt-1003`, REFLOG-ATTESTED, terminal status unrecorded) · Package: `_experiments/evidence/uq147-ko-release-partition/`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Every claim of the bounded result holds at the shipping bytes, the producer re-runs byte-identical, and the stated limits
bound it (no natural KO / Esper pending-0x113 admission, no transitive helper effects, lifetime or scheduling, no full UQ147
closure). The consumer contradiction ASTRA identified is real and is routed to its owner below.

## SWE2-AUDIT-SPEC identity and reproduction

- `manifest.json` sha256 `ff4cd43a997cb98df7007fdd1e8b2fd73ffc317fee4abcf0fa6e3f7310ac2458`, as named.
- Producer `prove-ko-release-partition.py` sha256 `aac8b52c…` in both the package and ASTRA's working copy, matching
  `prove-ko-release-partition-02.status.json` (`driver_sha256` `aac8b52c…`, terminal, exit 0).
- Re-run from ASTRA's working copy to a fresh scratch path: exit 0, stdout `Original bit22 set skips relation
  bookkeeping; separate set-bit restore can replace committed714. No natural/transitive closure.`; output
  **byte-identical** to `result-ko-release-partition-02.json`.
- The recorded failed-upstream CLI control (`control-ko-release-status-01`) prints `Actual failed upstream exits1/no result;
  existing positive02 reused, no native/game run.` - a fail-closed path, not a positive result.

## SWE2-AUDIT-SPEC the claims at the bytes (`disr.py`, image 73461D08…, base 0x120000)

`00310780` (`BattleUnit_ReleaseTargetRelationAndActionState`, 0xE1 B):
- Admission: receiver non-null (`00310780 test rcx,rcx` / `je`), stats `q[+0x698]` non-null (`0031078E` / `00310799 je`),
  target `0031B7E0(d[+0x710])` non-null (`003107BA je`), **`003107BE bt rcx, 0x16` / `003107C3 jb 0x310803` - bit 22 SET
  skips**, then the target mask bit `1 << b[+0xEA9]` in `d[target+0xEA4]` present (`003107D9 test` / `003107DB je`).
- Direct object writes, exactly four: `003107DD dec byte [rdi+0xEA8]` and `003107EA mov dword [rdi+0xEA4], edx` (target),
  `0031080B and qword [rbx], 0xFFFFFFFFEFFFFFDF` (acting flags bits 5 and 28 cleared), `00310825 mov byte [rbx+0x694], 0xFF`.
  `+0x714` is only read (`0031084D cmp word [rbx+0x714], 0x414E`); there is no direct `+0xBA0` or battle-mode store.
  The callees (`00313B30`, `002FEAD0`, `00308270`, `0030C970`, `00319420`, `00319140`, `00317E50`) are not effect-free -
  as the result states.

`00308270` (0x78 B), called at `00310806`:
- **`0030827B bt rax, 0x16` / `00308280 jae 0x3082E2` - bit 22 CLEAR skips restoration.** SET: `+0x28 = 0`,
  `0030C970(b[+0x695])` then `+0x695 = 0xFF`, the `022C1DB0` row copy to `+0xDC8`/`+0xE58`, **`003082C6 call 0x30EDA0`**
  (`BattleUnit_RestoreSuspendedActionState`), then `+0x690 = 0` and `and qword [rbx], 0xFFFFBFFFFFBFFFFF`.
- Bit 22 is read at `003107BE` and again at `0030827B` with three calls between (`00313B30`, `002FEAD0` on the admitted
  path) - the "no atomic invariance" qualification is correct.

## SWE2-AUDIT-SPEC consumers (routed, not edited by this record)

The reversed predicate is in the current text of two owned documents, and a stale copy bound in a third:
- EXP-198 L67-68 ("iff nonnull AND `q[obj]` bit22 set AND ...") and the auto-status contract section 13g L716 (same
  predicate) - both from `67f698dce` (SWE2-ORACLE). The bytes admit the bookkeeping only with bit 22 **clear**.
- EXP-231 L30: the `0030EDA0` snapshot copy is stated as 0x480 bytes at `obj+0x730..0xBAF`; the accepted copy bound
  (`d7500f9f`, independent `49d0564f2`) is `[+0x6B0, +0xBA0)`.
These are owner corrections (additive, raw results preserved, no experiment re-run), as `consumer-correction.json` says.

## SWE2-AUDIT-SPEC limits

Static, bounded, Method A. No native, live or emulator run was made or credited; the accepted copy proof is reused, not
re-run. Natural KO / Esper pending-0x113 admission, transitive helper effects, lifetime, scheduling and full UQ147 stay
open, as the result states.
