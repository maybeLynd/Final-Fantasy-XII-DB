# SWE2-AUDIT-SPEC review: OPUS interior rows (opus-the-input-name-registry-and-channel-alia-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-INPUT-NAME-REGISTRY-AND-CHANNEL-ALIA-EE` · Package: `_index/candidates/opus-the-input-name-registry-and-channel-alia-ee-1003/` (request at `693d650d4`, reviewed at HEAD `8fabf1300`) · Page: `15-Input/Input-Name-Registry/the-input-name-registry-and-channel-aliases.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 5 rows (25 anchors) were read clause by clause against the bytes. The package has fewer than 15 rows, so every row was checked. No defect was found.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `interior_applier.py` without `--apply` only verifies (source lines 8, 99-106). It was run in place with `-B` under the analysis venv python: `VERIFY 5 functions, 25 anchors` / `ALREADY` / `FAILS 0`, exit 0. This is identical to the committed `.out`. The run left the package and the page unchanged.
- **Page text.** Each row's `text` occurs exactly once on the live page, in the row for its function (132 B and 222 B sizes match the disr extents 0x84 and 0xde).
- **Method.** Each function was disassembled with `disr.py`. Neither extent has a jump table, and the last instruction of each listing is a `ret` or `jmp` back into the body (no truncation). Siblings were then compared instruction by instruction with every rip target masked and branch targets made entry-relative.
- **Name-list insert rows (3).**
  - `008760A0`: **exact.**
    - `+04 mov r10,[rcx+8]`, then `test r10,r10` / `jne` at `008760AE`. On null, `lea eax,[r10+0x11]` = 0x11 is returned.
    - The head is loaded from qword `02EB8260` (`008760BD`). The loop at `008760D0` takes the node string from qword `[r9+8]`, compares `movzx` bytes with the name (`008760E0`/`E3`, `sub` at `008760E8`) and stops on a difference or on the name's terminating zero (`test ecx,ecx`).
    - An equal string takes `je 0x876116` (`008760F5`) to `mov eax,0x12`. Otherwise the link is followed at `+0x10` (`008760F7`).
    - At the end of the list (or with an empty list, through `008760CA`), the old head is stored to `[r11+0x10]`, where r11 = the incoming rcx (`00876100`). `eax` is zeroed and rcx is stored to `02EB8260` (`0087610A`).
  - `00876490` (head `02EB82D8`, load `008764AD`, store `008764FA`) and `008768A0` (head `02EB8348`, load `008768BD`, store `0087690A`): **exact.** Their masked bodies are identical to `008760A0` in 40 of 40 instructions. The anchors sit at the same entry offsets +0E/+48/+55/+60/+6A.
- **List-to-array rows (2).**
  - `00876D80`: **exact.**
    - The count loop starts from qword `02EB83B8` (`00876D8F`) and follows `[rcx+0x10]` (`00876DA5`).
    - `cmp ebx,[rdx]` at `00876DB5`; equal counts take `je 0x876e27` straight to the fill.
    - A zero count takes `je 0x876dfc` with rbp = 0 (the null array).
    - Otherwise `rcx = count<<3`, `edx = 8`, then `call 0017D260` (`00876DCC`). A null result takes `je` at `00876DD7` to `00876DF8`, where the count is non-zero, and `mov eax,0xd` is returned with no store. A success is cleared with `rep stosq` over `count` qwords.
    - The free at `00876E15` (`call 00584730`, rcx = old qword `[rsi+8]`) is skipped when old == new (`00876E03`), when dword `[rsi]` has its sign bit set (`shr eax,0x1f` / `not al` / `test al,1` / `je`), or when old is null (`00876E13`).
    - Stores: `[rsi+8]` = new array, then `[rsi]` = count. The head is re-read, and the fill loop at `00876E30` writes each node pointer in list order. It returns 0 (`00876E40`). rsi = the incoming rdx (`00876D98`).
  - `00879670` (head `02EB9D80`, at `0087967F` and `00879710`): **exact.** Its masked body is identical to `00876D80` in 71 of 71 instructions, with the same callees `0017D260` and `00584730`.
- **Anchors.** All 25 are instruction boundaries carrying the recorded mnemonics. Each lies on the clause it supports: the null test, the byte compare, the equal-string exit, the tail store and the head store; and the count compare, the allocation call, the failed-allocation branch, the free call and the fill store.

## SWE2-AUDIT-SPEC narrowing / notes

No narrowing.

Notes (non-blocking):
- The rows say `[rdx]` / `[rdx+8]` where the body addresses `[rsi]` / `[rsi+8]`. rsi is a copy of the incoming rdx taken at `00876D98` and is never reassigned, so the wording is correct.
- The README's "Limits" line holds: these are body statements, and the applier verifies only anchors and mnemonics. This review is the sentence check.
