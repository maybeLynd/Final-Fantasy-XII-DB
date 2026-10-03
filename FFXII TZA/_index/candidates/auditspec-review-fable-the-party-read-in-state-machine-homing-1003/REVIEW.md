# SWE2-AUDIT-SPEC review: FABLE interior citations (fable-the-party-read-in-state-machine-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-PARTY-READ-IN-STATE-MACHINE-HOMING` · Package: `_index/candidates/fable-the-party-read-in-state-machine-homing-1003/` · Page: `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md` (commit `c29c5b85e`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 14 functions, 64 anchors` / `ALREADY` / `FAILS 0` (exit 0).
- `rows.json`: 14 rows, 64 anchors. **All 14** sentences were read clause by clause against raw capstone output of the
  certified image (SHA256 73461D08...). Every relative call (`fn`+0xNN) was resolved to its target.
  - `002E3E90` exact:
    - two list walks, `0215FD58` and then `0215FD78`, through `+8` on dword `+0x14` == `ecx`;
    - `shr 4` / `and 1` on byte `+0x19` returns;
    - signed `jg` on word `+0x1C` returns (`cx` is 0 there);
    - `test dl, 3` leads to the word-0 store at `002E3EF7`, and otherwise to `jmp 002EAEB0`.
  - `00344550` exact:
    - the two guards;
    - `002EBC90(rdx, movsx [r8+9] + 4, 1)`;
    - `002E3110(rdx, 3, movsx [r8+9], 002E97C0([r8+4]), [r8+0xC])`.
  - `00345A60` exact: `002EBC90(rdx, 3, 1)`, then `002E3110(rdx, 2, 0, 002E97C0([r8+4]), 0)`.
  - `00345F60` exact:
    - `00359CA0(00267E10(r9), 1, 1)` is called at +0x1F;
    - its result goes to `002EA6A0`;
    - `cmove` zero, then the store to `[r8]`.
  - `003463F0` exact: `003EB190(movsx [r8+6], 002E97C0([r8+8]), movsx [r8+4], movsx word [r8])`, with `movsx word [r8+2]`
    as the fifth argument.
  - `00354990` exact: two `00267E10(r9)` calls, then `jmp 002EBD60(002E9A60(b), a)`.
  - `00354A40` exact:
    - zero `[r8]` returns 0;
    - a null `002E97C0` result leads to `002E9810(002EAE20([r8+4], [rdx+0x15]))` stored to `[r8]`, and 1;
    - otherwise `002E4C20`, then `00314D40(1)`, and 1.
  - `003EB200` exact:
    - `002EAE20(edx, 0)`;
    - a non-null result leads to `003EB190(ecx, ptr, r8d, r9d)`, with `[rsp+0x60]` passed on as the fifth argument.
  - `0050CB00` exact: a negative `[r8]` or a non-zero `002E4C20([r8+8])` returns 0; otherwise `00314D40(1)` and 1.
  - `0050CE70` exact: `003DCCF0(rdx, 00267E10(r9), 002E9C00(rdx))`, then `jmp 0026B4E0(rcx, result)`.
  - `0050D710` exact:
    - `002E97B0(rdx)`;
    - both `002E4C20(p)` and `002E4C30(p, 002E9C00(rdx))` non-zero leads to `002EAC90(rdx)` and 0;
    - otherwise `00314D40(1)` and 1.
  - `0050D860` exact:
    - `002640C0` is called with the incoming registers;
    - `00267E10(r9)` is replaced by word `[rdx]` on `jns` failure;
    - `00358940` follows, then the four guards (byte `+3` & 0xE0 == 0x60, `002EA6A0`, qword `+0xC0`);
    - then `0017D280(00D22A0C, movsx byte [ctx+0x14C])`.
  - `0050DB80` exact: `00358940(002640C0(...), 00267E10(r9))`, then `jmp 0026B4E0(rcx, 002EA6A0(ptr))`.
  - `0050E150` exact:
    - three `00267E10(r9)` calls;
    - `d` = `002E9A60(c)`;
    - `0017D280(00D22A10, d)`;
    - `a` to `[r8+4]` and `b` to `[r8]`;
    - `002EAE20(d, [rdx+0x15])` to qword `[r8+8]`.
- Advisory, not a defect: in `00345F60`, "stores that result" refers to the `00359CA0` result, which is the value stored.
  It does not refer to `002EA6A0`'s return, which only selects zero. Owners who want to remove the ambiguity can write
  "stores the `00359CA0` result".
- Note: `003EB200` is also homed on the persistent-flag-banks page (`fable-home-persistent-flag-banks-1003`). The two
  sentences agree.
- Limits hold: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this
  record is.
