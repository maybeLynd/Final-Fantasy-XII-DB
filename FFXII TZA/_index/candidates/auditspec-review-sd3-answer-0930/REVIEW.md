# SWE2-AUDIT-SPEC review — `sd3-bit21-pause-0930` (answer record)

Task: `AUDITSPEC-REQ-ORACLE-SD3-ANSWER` — independent review of
`_index/candidates/sd3-bit21-pause-0930/` (policy-bit-21 controls pause:
immediate / deferred / refused).

Evidence class: **NATIVE/STATIC** — every claim below was re-derived against
the certified image `Tools/work/exe/FFXII_TZA.exe` (sha256
`73461D08…9721F8`), using linear disassembly of the named bodies plus an
image-wide opcode census. No trust placed in the package's own catalogue.

## Verdict

**ACCEPT** — the routing contract, modal identity, deferred-gate mechanics,
and the writer table are all correct. One wording imprecision flagged below
(non-blocking).

## Package checker

`sd3_pause.py` re-run on this host: `PASS P1..P5`, `PASS W1`, `FAILS 0`,
committed output byte-identical.

## Independent verification

### Modal identity (P1–P4 anchors)

- `002282F0` is the pause-menu builder: `ecx=0xD0` → factory `00244F50`;
  `lea rdx,[rip+0x125B]` at `0022832E` resolves to handler `00229590`;
  result stored at `rip+0x1DAC5E7` (`00228352`) = `01FD4940`. Early-exit if
  `01FD4940` non-null (`00228303`/`je 00228321`).
- `00229590` is the handler: decoded RIP-relative references confirm the
  `"PauseMenu Create"` (`00908B78`, loaded at `0022995D`) and
  `"PauseMenu Open"` (`00908B90`, loaded at `00229867`) strings.
  `00229590` itself is referenced from `00228331`'s operand window — the
  builder's `lea`.
- `00228380` (the bit-21 consumer) has exactly **one** image-wide E8/E9
  reference — call site `00253C70` — matching the record's single-caller
  claim.

### Three-way routing (P5)

`00228380` body, `002283DA`–`0022843B`:

```
0022838F  call 002E0FA0          ; esi = aggregate mask
002283DA  bt   esi, 0x15         ; aggregate bit 21
002283DE  jae  002283EF          ; clear  -> ebx stays 1  -> flag 1 (immediate)
002283E0  mov  ecx, ebx(=1) / call 002E1020   ; row-1 mask query
002283E7  bt   eax, 0x15         ; row-1 bit 21
002283EB  jae  0022843A          ; clear  -> xor eax,eax; ret   (refused)
002283ED  xor  ebx, ebx          ; set    -> flag 0        (deferred)
00228420  test edi,edi           ; menu object exists?
00228435  jmp  002282F0          ; build menu, ecx=ebx=flag
```

Exactly the record's table: aggregate-clear → immediate (flag 1);
aggregate-set + row-1-set → deferred (flag 0); aggregate-set + row-1-clear
→ refused (return 0). `00228450` is the deferred-release helper comparing
the `+0xC8` flag cell, consistent with the widget flag offset.

### Deferred gate `01FD4954` (P6)

- `00229AE0` = `mov [rip+…], ecx; ret` — the sole writer body.
- Reachers (E8 **and** E9 — this was the census discrepancy, see below):
  - `001B7690`: `mov ecx,1` → `jmp 00229AE0` (tail) — writes **1** (movie bring-up)
  - `001B7F30`: `mov ecx,1` → `call` at `001B80AE` — writes **1** (movie start)
  - `001B82A0`: `xor ecx,ecx` → `call` at `001B82B1` — writes **0** (movie end)
  - `001B8400`: `mov ecx,1` → `jmp 00229AE0` (tail at `001B84D7`, only reached
    from the `[rbx+4]==5` teardown arm) — writes **1**
  - `002CEB40`: `mov ecx,1` → `call` at `002CEBA9` — writes **1**
- The earlier "third `01FD4954` rip-reference at `003B534E`" is a
  byte-straddling false positive — the aligned instruction at that site
  targets `02B40518`; `01FD4954` only appears if a 4-byte window is opened
  one byte early. The gate has exactly the menu-tick read and the setter
  write. False positive retired.

### Writer census (W1) — the 35/37 vs 77 discrepancy, resolved

A raw image-wide scan of **E8 only** found 35 sites to `002E1C20` (set) and
37 to `002E1CA0` (clear) — three and two short of the record's 38/39.
Adding **E9 tail-jumps** closes it exactly:

- set tail sites: `001B82E4` (in `001B82A0`), `002548DA`, `0035CF41`
- clear tail sites: `003C8A0A`, `003C8AF2`

38 + 39 = **77 — the record's census is correct; E8-only scans under-count
primitive call sites.** This is a general audit lesson: any callee with a
single-exit `add rsp;pop;jmp` epilogue is invisible to `E8`-only xrefs.

Writer-table spot checks (row from `rcx`, bit from `rdx`):

| Claimed site | Verified |
|---|---|
| `001B7690` clear row1 | `edx=0x15; ecx=rdx-0x14=1` → `call 002E1CA0` |
| `001B7F30` clear row1 | same pattern at `001B80A4` |
| `001B8400` clear row1 | same pattern at `001B84BE` |
| `001B82A0` set row1 | tail `jmp 002E1C20` at `001B82E4`, `edx=0x15; ecx=1` |
| `0023FBE0` set row1 | `xor edi,edi` → `edx=rdi+0x15=21; ecx=rdi+1=1` |
| `0023FBE0` clear row1 | `edx=0x15; ecx=1` at `0024024B` (same root) |
| `002CEB40` set+clear row1 | set at `002CEDE5` (`edx=0x15;ecx=1`); clear earlier in root |
| `003939B0` set+clear row1 | `xor ebx,ebx` → `edx=rbx+0x15; ecx=rbx+1` |
| `00394070` set+clear row0 | `edx=0x15; xor ecx,ecx` at `003940CB`/`00394112` — **row 0** as claimed |
| `005823B0` set+clear row1 | `xor edi,edi` at `0023E4` arm → `rdx=rdi+0x15/rcx=rdi+1` at `005823F8`/`0058252C` |
| `00582860` set+clear row1 | `edx=0x15; ecx=1` at `005828B4` |

### Restore loop (`00229510`)

`esi` (row) gated to `cmp esi,2 / cmp esi,8`; `edi` (bit) loops 0..0x15;
each iteration does `ecx=esi; edx=edi; call 002E1CA0` then
`test [rbp],ebx(=1<<edi)` and `call 002E1C20` only when the saved mask bit
is set. Rows **2 and 8**, bits 0..21 — exactly as claimed.

## Non-blocking imprecision

- The record describes `001B8400`'s setter contact as "stores its own
  argument". The body sets `mov ecx,1` at `001B84C3` before the tail — a
  constant **1**, not a forwarded parameter. Direction (gate→1) is the
  same as the other movie arms; only the wording over-describes the
  mechanism.

## Limits

- W1's semantic classification (which site means "set bit 21") relies on
  `regval.py` constant propagation; the 11 sampled sites above were
  verified manually. The remaining ~60 primitive sites target other
  rows/bits and were not individually classified — consistent with the
  record's claim that W1 enumerates *bit-21-relevant* writers, not all
  primitive callers.
- `01FD4954`'s consumer side was verified via the two aligned references
  (tick + setter); no attempt made to prove gate-cleared-on-open beyond
  what P3/P4 already cover.
