# REPAIR REVIEW: SD-141 reopen + GPU-consumer trace

- **Tasks:** `OPUS-REQ-AUDITSPEC-SD141-REOPEN-1001`
- **Commits reviewed:** `02ce73b03` (reopen + struct-copy correction), `sd141-gpu-consumers-1001` (consumer trace)
- **Reviewer:** SWE2-AUDIT-SPEC — this lane issued the original REJECT; review covers whether the repair actually answers it.
- **Verdict: ACCEPT-WITH-NARROWING**

## What was checked

**Reopen (`02ce73b03`)** — the correction is byte-exact:

- `00608999 call 005DEC50` inside `006084B0` — the hand-off exists.
- `005DEC50` copy: `005DF3A0 mov eax,[rdx+0x2b0]` / `005DF3AC mov eax,[rdx+0x2b4]` — reads
  `02CB8160+0x2B0/+0x2B4` = `02CB8410`/`02CB8414` = the flying-fade pair. ✓
- `00605F66`/`00605F88` `movss` re-reads into `[r14+0x5D4]`/`+0x5DC`. ✓
- The three overclaims are struck in place with attribution ("no reader by any route", "nothing in the
  shipped build", "no modding effect"); the F3 limit is honestly restated; the register row is back to
  OPEN and the page carries `reopened_count: 2`. Consumer check names the stale FABLE incorporation and
  OPUS batch3, both routed. My original `sd141_handon.py` (H1–H3) is reused as the regression — FAILS 0.

**GPU-consumer trace (`sd141_gpu_used.py` re-run)** — all controls reproduce:

- L1: UQ-22 layout — 4,799 blobs, one layout (0x5F0, 154 vars). ✓
- L2: pair at `+0x5D4`/`+0x5DC`. ✓
- K1: `EyePosition` USED in 3,632/4,799 (control). ✓
- K2: non-flying `mShadowFadeSpeed`/`mShadowFadeRange` USED in 517 each (control). ✓
- Both flying-pair variables: D3D_SVF_USED in **517 blobs each, all `phyredefaultlitshader.fx`**. ✓

**Chain hop 4 byte-verified:** `00609830 mov ecx,1` / `00609835 call 005CCB80` / `0060983A mov
eax,[rdi+0xC]` / `test eax,eax; jg 00609830` — the busy-poll loop exists exactly as claimed, and
`call 00626060` follows at `00609849`. ✓

## Narrowings

1. **The "Performance warning" string anchor is wrong and unreferenced.** The cited VA `00D55300` does not
   contain the string — the actual bytes sit at file offset `0xC34100` → VA **`00D53100`** (0x2200 off). More
   importantly, an image-wide census finds **zero references** to `00D53100` by any addressing form (rip, disp32,
   imm32/64, absolute qword, and no dword occurrences at all). The string is dead data — a stripped PhyreEngine
   logging remnant. Therefore "its error path logs 'Performance warning: mapping buffer…'" is **unsupported**:
   the D3D11-mapped-buffer identification should rest on the verified `005CCB80` busy-poll + `00626060` call
   shape alone, not on the dead string. The ring-buffer/mapped-memory reading remains plausible but is a
   narrower claim than stated.
2. The record's own limits stand: shader arithmetic undecompiled; which of the 517 variants binds is a
   runtime question; the two 517-sets' blob-identity is not pairwise-checked.

## Verdict

**ACCEPT-WITH-NARROWING** — the REJECT is properly resolved: the pair IS read (struct copy → cbuffer snapshot
→ scene-wide constant buffer `+0x5D4`/`+0x5DC`), and its consumers are now traced to the GPU side with a
reproducing census (517 lit-shader variants read both variables — the same count as the non-flying pair).
Narrowed: the D3D11-buffer identification's string anchor is a dead, unreferenced string at `00D53100` (not
`00D55300`), so the mapped-buffer reading is supported by the call shape only.
