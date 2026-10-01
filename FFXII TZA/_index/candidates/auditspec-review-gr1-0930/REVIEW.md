# SWE2-AUDIT-SPEC review of GR-1 (gr1-wait-slot-settled-0930 at 72657b7ca): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
OPUS's `72657b7ca` (the record's only commit), [README](../gr1-wait-slot-settled-0930/README.md),
`gr1_settled_check.py`, and the kit tool `structflow.py` it publishes. Measured at HEAD 48de14c6b (a parked draft
started at 9b6c5bc93; its outputs reproduce identically). Static, certified image (sha256 asserted by [img.py](img.py)).

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-GR1-0930 | gr1-wait-slot-settled-0930 | `72657b7ca` | ACCEPT-WITH-NARROWING |

The answer stands: no code reads `+0x27` as the settled flag, and every handler read of the scratch window is
preceded by the same command's own write. But S4's rule does not prove that last sentence. My stricter check proves
it for 24 of the 38 command-reads. The other 14 hold only through a guard flag that I read by hand.

**Re-run.** [rerun_gr1_settled_check.out](rerun_gr1_settled_check.out) is identical to the committed `.out` (CR
ignored): S1-S5 PASS, `FAILS 0`, 19 s. `git status --porcelain --ignored` on the package directory shows nothing. All
my runs used `python -B`.

**Re-derived independently** ([gr1_indep.py](gr1_indep.py) / [.out](gr1_indep.out); pefile + capstone, no retool).
- **Table install.** `003DC2D0` fills the 16-qword pointer array `02B57EF0` with the default table `01F26720`, then sets
  family 0 = `01EED700`, 3 = `01F281B0`, 5 = `01F29418` and 7 = `01F29440`.
  - All three getters bound the index with `cmp edx, [tbl]` / `jge`.
  - begin `003DC270` reads entry `+8`, poll `003DC240` reads `+0x10`, and result `003DC2A0` reads `(N+1)*32`, which
    is `+0x20`. The package's `{8, 0x10, 0x20}` decode is right.
- **The 1,960 / 1,886 decode.** The tables hold 212 + 1496 + 147 + 1 + 104 = **1960** commands and **1886** unique
  non-null handlers. Every non-null slot is DIR64-relocated, and no entry's `+0x18` qword is used.
  - 336 commands have a begin, 290 a poll and 1651 a result. 1620 have a poll or result but no begin.
- **Other installers.** The only code references to the array are `003DC2D0`'s own and two loop-end `lea`s
  (`003DAB87`, `003DAC35`). No stored pointer to the array or to any table.
- **A1 residual, now typed.** `006A62D4 movss xmm0, [rax+0x24]` in `006A6180`: here `[rbx+0xA8]` points to twelve
  floats read at `+0x00`..`+0x2C` (a 3x4 transform), not a stride-0x28 slot array. `006A6180` has no rel32 caller and
  no stored pointer.

**The S4 pairing, re-checked strictly** ([gr1_pairs.py](gr1_pairs.py) / [.out](gr1_pairs.out); [gr1_strict.py](gr1_strict.py) /
[.out](gr1_strict.out)).
- I used the package's structflow per handler to list the accesses, then applied a must-write check on each
  function's CFG with my own decode. Covered means every path to the read passes a covering write, or a call to a
  function that writes on every path.
- The 17 credited writes are all plain `mov`/`movss` stores, so none is a read-modify-write.
- Of 38 command-reads:
  - **5** are covered inside their own function. `00357918` follows `call 00357DE0` at `00357900`, and `00357DE0`
    stores `[rsi+0xC]` unconditionally at `00357E82`. `0050D6CA` follows `0050D6B8`.
  - **19** are covered because the command's begin writes on every path.
  - **14** have a begin that writes on only one path. Each is guarded by a flag or sign the begin always sets, which I
    read by hand:
    - `00343A30` (commands 0/1051, and 0/1052 and 0/1053 through the tail jumps at `00344D80` and `00345AE0`): it
      writes `[r8+0xC]` and sets `[r8+5] = 1`, or sets `[r8+5] = 0`. Poll `00344200` skips when `[r8+5] == 0`.
    - `00343B00` (0/512): it writes and sets `[r8+8] = 1`, or sets `[r8+8] = 0`. Result `00344550` skips when
      `[r8+8] == 0`.
    - `0050CA40` (def/43, 44, 87, 93, 94): it always stores eax at `[r8]` and writes `[r8+8]` only when eax >= 0. Each
      of `0050CB00`, `0050CBD0`, `0050CD80` and `0050CF20` skips the read when `[r8] < 0`.
- So every read is covered. The package's rule cannot show it for those 14, because it credits "any write in begin"
  regardless of order or path.
- One of the "46 handlers" hits is a flow artefact. `00342910` loops `mov byte [rdi-1], cl` with `rdi = r8+4..`, and
  that writes slot `+0x1C..+0x1F`. structflow's offset lattice widens around the loop and reports `+0x27`. It is a
  write, so it over-reports and hides nothing.

**Begin before poll/result** ([gr1_phase.py](gr1_phase.py) / [.out](gr1_phase.out)). structflow with field `+0x15`
from the seven functions finds 27 writes (the same at depth 5), and the handlers write it nowhere:
- the slot reset `0025D460`, which zeroes bytes `+0x00..+0x16`;
- 10 wait-arming word stores, `0x106` ×9 and `0x107` (these set `+0x15 = 1`);
- 11 byte clears in `0025E4C0`;
- `002621D0` pending = 1 (`0026230B`) and complete = 0 (`00262382`);
- the VMResult writers `002651A0`, `0026B4E0` (= 2) and `0026B4C0` (= 3), which handlers call (`002651A0` from
  `00342B03`).

The only handler-side hit is the `00342910` artefact.

The interpreter reaches `002621D0` at `002619B6`, `00261A19` and `00261AD4`. It backs the script pc up while the
command is pending, so the same opcode re-enters with `+0x15 = 1`. Every non-zero `+0x15` is therefore set inside the
current opcode and cleared when it completes, or by the reset. The one case not traced is an opcode abandoned
mid-execution (the script redirected while `+0x15 != 0`). That is a static interpreter question, not a runtime one.

**Controls and depth.**
- structflow at depth 5 from the seven functions gives the same 12 writes and 0 reads of `+0x27` (P1).
- Handlers at depth 4 give the same 22 read sites and 17 write sites as at depth 2 (P2).
- Transfers structflow does not follow with a slot tag in an argument register ([gr1_transfers.py](gr1_transfers.py) /
  [.out](gr1_transfers.out)):
  - 133 distinct depth-0 calls and 33 depth-0 tail jumps at the S4 depth. Moving to depth 4 adds no read.
  - 8 conditional tail calls (7 targets). Entering each target with `r8 = slot+0x18` at depth 2 and 4 gives no `+0x27`
    access, unknown or escape ([gr1_jcc.py](gr1_jcc.py) / [.out](gr1_jcc.out)).
  - S3's one depth-0 call (`00809662`, r9) gives the same empty result.
- The package's positive control (S3 re-finds the 12 known writes) is sensitive to missing a direct write, and the
  S4 table decode is exact. The pairing rule's own sensitivity is the defect below.

**Citations checked.**
- `00342770` → `00342807 mov dword [rdi+0xC], 0`, then result `00342F80` reads at `00342FB5` / `00342FE6`: supports
  the sentence.
- `0050D660` / `0050D710` / `0050D810` on the qword: supports the sentence.
- S5: `0017D280` spills rcx..r9 and calls the IAT slot `008C2F28` with `ecx = 1`, so r8 is a variadic argument.
  `00244F00` makes `call rax` from `[rcx]` with rdx set. Both support the sentence.

**Defects in the package's own gate (S4).**
1. The pairing rule credits any write in the begin handler, with no order or path check. That is exact for 19
   command-reads, and it is the wrong reason for 14.
2. "Earlier in the same handler" compares addresses across functions (hits from callees).
3. A read-modify-write would count as a write. There are none in this image.
4. `lea_tbl` is computed and never checked (dead code).

None of these changes this image's result.

**Correction wording** (the producer applies):
1. In S4, replace "Every read has a covering write in its command's begin handler or earlier in the same handler"
   with: "Every read is preceded by the same command's own write. For 24 of the 38 command-reads the write is on every
   path (in the reading function, or in a begin that writes on every path). For the other 14 (0/512, 0/1051-0/1053,
   def/43, 44, 87, 93 and 94), the begin writes on one path only and records it in a guard: `[r8+5]` for `00343A30`,
   `[r8+8]` for `00343B00`, the sign of `[r8]` for `0050CA40`. The reader tests the guard first."
2. Limits, "Begin before poll/result": add "The phase byte `+0x15` is written only by the interpreter (wait arming /
   clears), the slot reset `0025D460`, `002621D0` and the VMResult writers. The handlers never write it. So a command
   starts at phase 0 unless an opcode is abandoned mid-execution, which is not traced here."
3. S4 "46 handlers touch the window": add "(one, `00342910`, is a loop-widening artefact: its byte stores reach slot
   `+0x1C..+0x1F`)".
