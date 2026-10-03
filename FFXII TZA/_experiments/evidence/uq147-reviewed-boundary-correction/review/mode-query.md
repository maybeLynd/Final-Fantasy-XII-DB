# SWE2-AUDIT-SPEC review: ASTRA UQ147 read-only mode query and qualified Dismiss early return

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not ASTRA) · 2026-10-03 · Task: `ASTRA-REQ-SPEC-UQ147-MODE-QUERY-1003` (reviews `ASTRA-PUBLISH-UQ147-MODE-QUERY-1003`) · commit reviewed `ecbfeb64134bd55186cf0f4c784048489026c852`, at HEAD `a19ddeadd`
Package: `_experiments/evidence/uq147-mode-query/` (unchanged since `ecbfeb641`). Image pin `73461d08…21f8`, base `0x120000`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

The helper chain `377C20→3148F0→2EF2B0→2EF640` (133 B) is closed. It has no memory write of any kind, stack included, and no opaque call. The field cell, the descriptor, the bit-15 arithmetic and the two non-atomic mode reads in `30D9A0` are as stated.

Under the stated premises, `3138D0(0)` returns before `311CF0` and before its own `[battle+5AD0]` write. The premises are a stable readable mode word giving 1, the field helper returning false, and normal ABI with a private stack and no interference. The early returns are:

- an empty roster slot or actor;
- pending `+BA0`==113 with flag bit 14 set;
- committed `+714`==113.

This refutes an *unconditional* cleanup guarantee at local implementation scope only. It says nothing about naturally initialized summoner-KO reachability, which the package itself states.

## SWE2-AUDIT-SPEC identity and integrity

- `manifest.json` hashes to `f6d762b35072e327ba67f46b48a87a88cf83dbca60faf90981d400d40dd7bf0e`, as named. It lists 60 members, and all match size and sha256 (0 mismatches). The only unlisted files are `.gitattributes` and the manifest.
- The drivers are:
  - current producer `prove-mode-query-boundary.py` `e83a3f7b3e717c41f9a5b8292684d59c04c82e242d01c0df2d978f185cc9f9f0`;
  - failed first producer `…v1.preimage.py` `07640581e4e902856593ba58c34e35920a5dbc69e18f254d815282df122f316d`;
  - status control `control-mode-query-status.py` `7c0fc97578fc3cd593f0ce70b609017ce2e6dfac7c2e94554352597af9f93d7b`.
- `source-mode-query-01.json` is `2218c4f0…3651`. `source-boundary-01.json` and `source-selector-01.json` are byte-identical to the `6d74079f` predecessor's copies.
- Receipts (each `terminal: true`, `exception: null`):

  | receipt | driver | exit | output |
  |---|---|---|---|
  | `prove-mode-query-02` | `e83a3f7b…` | 0 | stdout `Closed read-only mode query; conditional Dismiss early returns refute unconditional cleanup guarantee. Natural UQ147 remains OPEN.` |
  | `prove-mode-query-01` | `07640581…` | **1** | stderr ends `ValueError: extra/uncovered helper instruction`, no result |
  | `control-mode-query-status-01` | `7c0fc975…` | 0 | stdout `Actual failed-upstream CLI refused exit1/no result; retained positive complete. No FF12 execution.` |
  | `capture-mode-query-01` | `05173bed…` | 0 | spans 78 / 27 / 20 / 8 B |

- The only difference between v1 and the current producer is `37`→`38` plus an added explicit pin for `377C29 mov r8,[rip+27654D0h]`, which is the descriptor load.

## SWE2-AUDIT-SPEC reproduction

The drivers use ASTRA's work-root layout, with the validator in `P.parent`. I rebuilt that layout in scratch (validator `7c4ea9f6…5f13`) and used venv python 3.14.6 with capstone 5.0.7.

- `prove-mode-query-boundary.py result-mode-query-02.json`: exit 0, same stdout. The output is **byte-identical** to the retained `result-mode-query-02.json` (`e1c1d5cd…4bfa`).
- `control-mode-query-status.py` (on a fresh copy without its output dir): exit 0, same stdout. The child's final stderr line is `ValueError: required upstream capture failed/incomplete`, with exit 1 and no `must-not-exist.json`. `result.json` is **byte-identical** to the retained one.
- `prove-mode-query-boundary.v1.preimage.py v1-rerun.json`: exit 1, `ValueError: extra/uncovered helper instruction`. The retained failure reproduces.

## SWE2-AUDIT-SPEC physical byte correspondence (independent of the producer)

- All four ranges of `source-mode-query-01.json` equal the image bytes.
- `377C20-377C6E` (78 B), `3148F0-31490B` (27 B) and `2EF2B0-2EF2C4` (20 B) each have a single `.pdata` root.
- `2EF640-2EF648` (8 B) has **no** covering row; it is a leaf.
- The total is 133 B.
- Instruction counts from the disassembly are 23 + 8 + 5 + 2 = 38, as the corrected guard says.

## SWE2-AUDIT-SPEC re-derivation from the shipping image (`disr.py`)

- **`2EF640`:** `lea rax,[rip+1E74C39h]` (= `02164280`) / `ret`.
- **`2EF2B0`:** `call 2EF640` / `add rax,200h`.
- **`3148F0`:** `call 2EF2B0` / `xor ecx,ecx` / `mov eax,[rax+1044h]` / `test` / `cmovs eax,ecx`.
  - So the field id is DWORD `02164280+200h+1044h` = **`021654C4`**, and a negative value clamps to 0.
- **`377C20`:**
  - `call 3148F0`, then `r8 = [02ADD100]`;
  - NULL→`377C5F` gives `0xFFF>>15` = **0**;
  - `cmp eax,[r8+4] / jae` (unsigned) gives 0;
  - otherwise `edx = (byte[r8+3*id+9]<<8) + byte[r8+3*id+8]`, `>>15`, which is **bit 15** (byte 9, bit 7).

  None of the four bodies has a memory-destination operand.
- **`30D9A0`:**
  - `rax=[02EBF190]` / `ecx=[rax+5B04h]`;
  - bit 3→5, bit 2→4;
  - `call 377C20`, nonzero→3;
  - **re-load** `rax=[02EBF190]` / `ecx=[rax+5B04h]`;
  - bit 1→2;
  - else `cl&1`.

  The pointer and the mode word are each read twice and not atomically. So "mode 1" means: low nibble `0001` at both reads (bits 3 and 2 clear on the first read, bit 1 clear and bit 0 set on the second), with the helper false.
- **`3138D0(0)`:**
  - `esi=ecx` (=0) / `call 30D9A0` / `cmp eax,1 / jne 31398D` / `lea ecx,[rax+2]` (=3) / `call 31B8C0` / `test rax,rax / je 31398D`. The NULL roster/unit case returns.
  - `edx=[rax]` / `mov [rsp+48h],rbp` / `ebp=113h` / `bt rdx,0Eh / jae 313915` / `cmp word [rax+0BA0h],bp / je 313988`. Pending 113 returns only when bit 14 is set.
  - `313915 cmp word [rax+714h],bp / je 313988`. Committed 113 returns; it is reached when bit 14 is clear or pending != 113.
  - The main path continues to `31B7E0`, `31395D call 311CF0` and `313981 xor word [rcx+5AD0h],ax`, which sets bit 0 of `+5AD0` to `si`=0.
  - Both early-return targets (`313988`, `31398D`) lie after `313981`, so both skip `311CF0` and the `5AD0` write. **Holds.**
  - The only store on the early paths is `[rsp+48h]` = entry RSP+10h, the shadow-space slot that the ABI gives the callee. It falls under the package's private-stack premise.

## SWE2-AUDIT-SPEC control sensitivity

I name the defect each control guards and check that the refusal comes from the matching detector. All five re-ran with their markers required.

| control | defect | first refusing check | sensitive? |
|---|---|---|---|
| `closed-helper-call-changed` (`3148F4`→`call 311CF0`) | opaque call in the query chain | `closed()` call-chain check, `helper call chain changed` | yes |
| `fieldcell-offset-changed` (`3148FB` disp→`0x1048`) | different field cell, text kept | `mem()`, `required memory effect/address changed` | yes. The text pin passes |
| `image-base-changed` (`2EF640` `rip_target`→`0x2164480`) | different reference buffer | `mem()` | yes |
| `committed-action-offset-changed` (`313915` disp→`0x718`) | wrong committed-action field | `mem()` | yes |
| `early-return-branch-changed` (`31391C` args→`0x31391e`) | the early return no longer exits | text pin, `required instruction/transfer changed` | yes. `3138D0` is not run through `closed()`, so the text pin is the detector, and that is appropriate |

The **positive detectors** are the `313981` `rw` `[rcx+5AD0h]` annotation and the `31395D call 311CF0` presence check. They show that the producer can see the cleanup write and the request when they exist, so the early-return "absence" is not a property of the filter.

The **actual CLI control** runs the unchanged current producer with a labelled `exit:1` capture status. It refuses with exit 1 and no output, a real fail-closed invocation and not an in-process check.

The **retained failed-count control** reproduces. The v1 guard (37) rejects the complete 38-instruction chain, and the correction only adds a pin.

## SWE2-AUDIT-SPEC claims audit

- "No normal helper call or write in the query chain": **holds** (no memory writes at all; CALL/RET are premises).
- Reference image `02164280`→`+200`→`+1044` = `021654C4`, with the signed clamp, the descriptor NULL/`>=count`→0, the stride-3 bytes 8/9 and bit 15: **holds**.
- `30D9A0` reads twice, not atomically, in the order first bits 3/2, then the helper, then second bits 1/0: **holds**.
- The Dismiss early returns before `311CF0`/`5AD0` under the stated premises: **holds**.
- The package keeps natural state, lifetime, scheduling and whole UQ147 OPEN, and claims no native, emulator or game execution. "Semantic effects under constructed premises distinct from normal gameplay" is stated. **No overclaim.**

## SWE2-AUDIT-SPEC notes (non-blocking)

- **Wording precision for consumers.** Write "both mode reads 1" as "the low nibble of DWORD `[[02EBF190]+5B04h]` is `0001` at both reads". The two reads test different bits, so this is the exact condition.
- `closed()` recognises transfers by `mnemonic=='call'`/`startswith('j')`, the same prefix-form gap noted in the gauge transfer review. The 38 retained instructions contain no prefixed forms, so nothing here depends on it.
