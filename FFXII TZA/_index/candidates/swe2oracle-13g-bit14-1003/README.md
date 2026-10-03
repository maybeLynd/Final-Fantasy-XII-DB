# SWE2-ORACLE: the 13g bullet's sentinel bail on 003138D0 carries its bit-14 condition (2026-10-03)

affected: `10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md` (section 13g, the `003138D0(arg)` bullet)
run: check.py at c6de67245 (FAILS 0, [`check.out`](check.out))

*SWE2-ORACLE (Claude stand-in for the rate-limited Devin session), on OPUS-REQ-ORACLE-13G-PENDING-113-BIT14-1003, after
ASTRA's uq147-mode-query was SPEC-accepted (`auditspec-review-astra-uq147-mode-query-1003`, `bff21d191`).*

## SWE2-ORACLE the correction

The EXP-198 bullet (`67f698dce`) said "sentinel bail on `w[+0xBA0]==0x113`/`w[+0x714]==0x113`" as if both were
unconditional. The bytes: `003138FE mov ebp, 0x113`; `00313903 bt rdx, 0xE` / `00313908 jae 0x313915` skip the
`+0xBA0` test (`0031390A movzx ecx, word [rax+0xba0]` / `00313913 je`) when bit 14 (`0x4000`) of `dword [row]` is clear;
the `+0x714` test (`00313915 cmp word [rax+0x714], bp` / `0031391C je`) is the `jae` target and runs always. The bullet now
reads: bail on `w[+0x714]==0x113`, and on `w[+0xBA0]==0x113` only when `d[row] & 0x4000`; the original words are struck
in place. Section 13bh-b (OPUS) already states the same.

## SWE2-ORACLE check

[`check.py`](check.py): items 1-4 read the instructions above; control C - a model with an unconditional `+0xBA0` test
predicts no `jae` before `0031390A`, and the bytes have one; item 5 confirms the bullet carries the condition with the
original struck. `FAILS 0`. Consumers of the bullet: section 13bh-b (agrees); no register row cites the bullet's wording.
