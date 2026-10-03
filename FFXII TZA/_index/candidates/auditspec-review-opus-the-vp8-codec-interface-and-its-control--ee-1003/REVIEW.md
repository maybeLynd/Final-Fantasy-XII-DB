# SWE2-AUDIT-SPEC review: OPUS interior rows (opus-the-vp8-codec-interface-and-its-control--ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-VP8-CODEC-INTERFACE-AND-ITS-CONTROL-EE` · Package: `_index/candidates/opus-the-vp8-codec-interface-and-its-control--ee-1003/` (request at `693d650d4`, reviewed at HEAD `8fabf1300`) · Page: `23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 5 rows. The request asks for at least 15 rows, so all 5 were checked. Each was checked clause by clause against an independent decode (`disr.py`, image base `00120000`). Every clause holds, and every anchor is an instruction boundary inside its body with the recorded mnemonic, on the clause it supports. No row changes.

## SWE2-AUDIT-SPEC checks

- **Applier re-run (verify-only).** I read the source first: without `--apply` it writes nothing. `interior_applier.py` was run under the analysis venv with `-B`. Output: `VERIFY 5 functions, 25 anchors` / `ALREADY` / `FAILS 0`, exit 0. `ALREADY` means the page's 2026-10-03 block is byte-equal to a render of `rows.json`. The page is clean in the working tree, and the block is present in `HEAD`, so the applied text equals the reviewed rows.
- **Extents.** Every listing ends in `ret`. Every branch target lies inside the listing, and there is no jump table, so the `disr.py` body window is complete for all 5.

| fn | verdict | decisive bytes |
|---|---|---|
| `0016E070` | exact | `0016E079`/`0016E07E` `mov ecx,0x347; call [008C2B40]`. Null goes to `0016E0FD` (`eax=1`). `0016E090`/`0016E09A` `lea rbx,[rax+0x17]; and rbx,-0x10`. `0016E0A1` stores `p` at `[rbx-8]`. `0016E0A5` is `memset(rbx,0,0x330)`. `0016E0AA`-`0016E0B1`: `[rdi+0x30]=rbx`, `[rbx+8]=dword [rdi+0x20]`. `+0x108`/`+0x110` are zeroed and `+0xe4`=0x10. `0016E0D7`-`0016E0EC`: an 8-byte `movsd` plus a dword go to `rbx+0xd8`, and `[rdi+0x28]` is repointed. `0016E0F0` returns 0. |
| `0016E290` | exact | `0016E2A9`-`0016E2C1`: `mov eax,edx` (zero-extends), `add rax,r10; cmp rax,r10; ja`. Not-above returns 8. The fifth argument is `[rsp+0x80]` (2 pushes + 0x48 + 0x28). `0016E2E4` `cmova r9d,eax` gives min(edx,10). `0016E2EB` makes the buffer the source. `0016E2F3` zeroes `[r8+0xc]`. `0016E2F7`/`0016E2FC` (`jb`, `test byte [r10],1`) return 5. `0016E302` stores 1. `0016E309`-`0016E31C` test 0x9d/0x01/0x2a. Words 6 and 8 `& 0x3fff` go to `[r8+4]`/`[r8+8]`. `0016E350`/`0016E355` (`or`, `cmovne eax,0`) give 0 when either is non-zero and 5 otherwise. `0016E368` is the cookie check `00808C40`. |
| `0016E3C0` | exact | `0016E3E2` zeroes `[r9]`. `0016E3D5`/`0016E3FE`: `memset(rcx+0x2c0,0,0x6c)` runs when `[+0x2bc]==0`. With `+0x2b8` non-zero and `rdx`/`r8d` both zero, `0016E45A` reaches `0016E482` (returns 1). The append is at `0016E41C`/`0016E42A`, then `inc` at `0016E431`. `0016E437`/`0016E43E` `cmp 9; jbe`. Past 9, the index is reset, `[r9]=8` and the function returns -1 (`0016E440`-`0016E44D`); otherwise `0016E456` returns 0. With `+0x2b8` zero and both zero, the function returns 0 (`0016E465`→`0016E456`). Otherwise it stores slot 0 and `[+0x2bc]=1` (`0016E46B`-`0016E478`) and returns 1. |
| `0016EC20` | exact | `0016EC30`/`0016EC3D` return 8 on a null record or non-zero `[rcx+0x1a8]`. Stack block (all 15 stores matched): `+0x20`→`rsp+0x20/0x28`, `+0x24`→`0x24/0x2c`, `+0x58`→`0x30`, (`+0x20`+1)>>1→`0x34/0x3c`, (`+0x24`+1)>>1→`0x38/0x40`, `+0x5c`→`0x44`, qwords `+0x38/+0x40/+0x48`→`0x58/0x60/0x68`. (`+0x58`−`+0x20`)>>1 at `0016EC71`-`0016EC82` goes to `0x84`. The call at `0016ECC1` is `0016F450([rcx+0x1b0], dword [r], rsp+0x20)`. |
| `0016F450` | exact | `0016F456` sets `rbx=rcx+0x12c0`. The selector at `0016F460`-`0016F481` maps 1/2/4 to `0x9d4/0x9d8/0x9dc`. Any other value goes to `0016F52F` (`01CEB6B8` "Invalid reference frame") and `0016F53E` `0016DE20(b,1,..)`. The entry offset is `k*0x90` (`lea rcx,[rax+rax*8]; add rcx,rcx`, scaled by 8). Compares at `0016F499`-`0016F4CA` cover `+4,+0,+0x18,+0x14`; a mismatch goes to `01CEB6D0` "Incorrect buffer dimensions". `0016F4CF` gets `j`. `0016F4D7` is the `dec`. `0016F4ED` `jle` (signed, so positive only) guards the second `dec`. `0016F4F7` stores `j`, `0016F4FA` is the `inc`, and `0016F519` calls `00173FA0(r8, b+0x780+j*0x90)`. Both exits load `eax,[rbx]`. |

**5 of 5 exact.** All 25 anchors were checked against the decode.

## SWE2-AUDIT-SPEC narrowing / notes

No narrowing.

Notes (non-blocking, not row defects):
- In `0016E3C0`, the single `memset` of 0x6c bytes clears both arrays: 9 qwords at `+0x2c0` and 9 dwords at `+0x308`. The index is tested only after the store (`> 9`), so a store at index 9 writes the qword at `+0x308`, over the first two dword slots. The row says "at index `[rcx+0x2bc]`" without an array length, so it stays exact. A reader should not infer 10 slots per array from "exceeds 9".
- The applier verifies anchors and mnemonics only, as the README says. This review is the sentence check.
