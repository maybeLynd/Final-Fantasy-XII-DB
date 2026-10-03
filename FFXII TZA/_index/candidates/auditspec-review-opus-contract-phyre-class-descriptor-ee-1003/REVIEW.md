# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-contract-phyre-class-descriptor-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-PHYRE-CLASS-DESCRIPTOR-EE-10-A5FF7` · Package: `_index/candidates/opus-contract-phyre-class-descriptor-ee-1003/` · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md` (commit 6a9eb7555)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 3 functions, 15 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 3 rows, 15 anchors; rejected 0, missing 0; mode `ee`, no family (the family-declaring-page rule does not apply).
- Semantic pass: **every row** (3 of 3) read clause by clause against a capstone decode of the certified image (SHA256 73461D08...); each extent is a single .pdata entry equal to the kit's function size:
  - `00617E60` (543 B) exact:
    - Calls `006388C0(02CF1540)` at `00617E7B`.
    - `rbx` = `gs:[0x58]`[dword `02EAED3C`] + 4. Each guard (`02CF65B8`, `02CF6618`, `02CF6678`, `02CF66D8`, all .data) is compared with `[rbx]` (`jle` skips), then goes through `008092FC` and a `-1` re-test.
    - Each of the four `00632960` calls has `rcx` = member (`02CF6560` / `02CF65C0` / `02CF6620` / `02CF6680`), `rdx` = `02CF1540`, `r8` = the getter result (`00613E80` / `00613A30` / `00613800` / `0062FFC0`) and `r9` = name. The .rdata strings are `00D54C08 'm_rasterDesc'`, `00D54C18 'm_depthDesc'`, `00D54C28 'm_blendDesc'` and `00D54C38 'm_stencilRef'`.
    - The stack arguments are `[rsp+0x20]` = 4 / 0x2C / 0x60 / 0x188, `[rsp+0x28]` = 0x10, dword `[rsp+0x30]` = 0 and qword `[rsp+0x38]` = 0.
    - The exits `008AEDB0`, `008AECE0`, `008AEC60` and `008AEE10` go to `00808B90`, each followed by `0080929C`.
    - It ends with `jmp 00639450` with `rcx` = `02CF1540`.
  - `006318A0` (440 B) exact:
    - The guard `02CF94EC` is compared against the TLS epoch, and `jg` goes to the init block.
    - The init block stores `01F2E330`/`338` = `01F2E330`, `01F2E340`/`348` = `01F2E340`, dword `01F2E350` = 0 and `01F2E358`/`360` = `01F2E358`, then calls `00808B90(008AF490)`.
    - Self-linked pairs are at `+0x50`, `+0x60`, `+0x80`, `+0x90`, `+0xA0` and `+0xB0`. A triple is at `+8`, with `[rax+0x18]` / `[rax+0x20]` landing at `+0x20` (dword) and `+0x28` (qword).
    - `+0x30` = `00D58400 'PBase'` (.rdata), dwords `+0x38` and `+0x3C` = 1, and `+0x40`, `+0x48`, `+0x78` and `+0xC0`..`+0xE0` = 0.
    - `+0x70` = `01F2E330`; `+0xE8` = `02CF8260`, then `inc` at `006319B5`; `+0xEC` = -1; `+0xF0` and `+0xF8` = 0.
    - `[o]` = `00D581C0`, then `00D58248`, and it returns `rbx`.
  - `00635980` (507 B) exact:
    - The guard `02CF94E4` covers `005A0470(02CF8980, 00D58838 'GetGlobalNamespace')`. On a zero result it appends the node `01F2E290` (`[node]` = `02CF8A20`, `[node+8]` = old tail, `[old tail]` = node, tail `02CF8A28` = node), and the exit is `008AF1C0`.
    - Unconditionally it stores `01F2E2C0` = `00D58FE0`, `01F2E2C8` = `006373D0` and `01F2E2B8` = `01F2E2C0`.
    - The guard `02CF94E8` covers the same pattern with `005A7A40(..., 00D58850 'getClassDescriptor')`, the node `01F2E2E0`, the list `02CF8A10` / tail `02CF8A18` and the exit `008AF3D0`.
    - `movups` copies 16 bytes from `[rsp+0x28]`: qword `0063BA10`, dword 0 at `+0x30`, and `+0x34` never written. This confirms "last dword from an unwritten stack slot".
    - It calls `00639160([02CF89F0], 02CF8980)`.
    - `bts eax, 0x1e` sets 0x40000000. `test al, 1` on the stored value: when set, it self-links `02CF8988`/`90`/`98`, zeroes dword `02CF89A0` and qword `02CF89A8`, and jumps to `006388C0`; otherwise it does `ret`.
  - All 15 anchors (`00617E7B`, `00617EF2`, `00617F65`, `00617FD8`, `0061804B` call; `006318D7` cmp, `00631A04` mov, `00631904` lea, `006319B5` inc, `006319BB` mov; `006359E3` call, `00635A10` mov, `00635A8A` call, `00635B22` call, `00635B2D` bts) are strictly inside their extents with those mnemonics.
- Limits hold: body statements only, static evidence. OPUS's re-read is not independent review; this record is.
