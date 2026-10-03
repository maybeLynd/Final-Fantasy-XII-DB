# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-contract-ppfx-effect-creation-ee-1003-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-PPFX-EFFECT-CREATION-EE-1003-26CFC` · Package: `_index/candidates/opus-contract-ppfx-effect-creation-ee-1003-2/` (reviewed at HEAD `e06561376`) · Page: `17-Presentation-Rendering/Post-Processing/CONTRACT-ppfx-effect-creation.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 9 rows. All 9 were read clause by clause against a raw capstone decode of the certified image (SHA256 `73461D08...21F8`), and all 9 are exact. That includes the five guard-byte clauses OPUS corrected after a re-read: each block runs while the byte is non-zero and then clears it.

## SWE2-AUDIT-SPEC checks

- **Applier re-run (verify-only).** `interior_applier.py` with the venv python printed `VERIFY 9 functions, 45 anchors` / `ALREADY` / `FAILS 0`, exit 0. The page holds two 2026-10-03 blocks. These 9 rows are the second block, headed `... opus-contract-ppfx-effect-creation-ee-1003-2)` at line 328, with rows ending at line 342. The page is clean in the working tree.
- **Extents.** Extents come from `.pdata`. Where `.pdata` splits a function into chained fragments (`007157A0` + `007157F7`), I took the extent to the final `ret` before int3 padding. All 45 anchors are instruction boundaries with the recorded mnemonic.
- **Helpers read**, because the rows state their behaviour:
  - `007157A0` builds a string from a C string.
  - `00715CC0` sets the length: it truncates, or pads with 0x20.
  - `007198A0` appends a C string.
  - `00719460` forms the string plus a C string into an output.
  - `00719380` concatenates two strings into an output.
  - `007182F0` assigns a string.
  - `00718350` assigns a C string.
  - `00715360` resets a string to empty.
  - `00715C70` frees the buffer unless it is null or `02EA1720`.
  - `007153B0` reserves capacity and keeps the length.
  - `0017D2E0` is `sprintf` in the function table, and its body forwards to the CRT import `__stdio_common_vsprintf` (IAT slot `008C2F08`).
  - `0078A4F0` decrements a refcount at `+8`.
  - The IAT slots `008C2A68` and `008C2BB0` resolve to `memcpy` and `sinf`.

Per row:

- **`007157A0`** (`007157A0`-`0071589F`): exact. `007157BC`-`007157CE`: strlen, or 0 for a null `rdx`, goes to dword `[s]`. `007157D6`-`007157E0`: for `n`=0, qword 0 and `02EA1720`. `007157FC`-`00715831`: 0x40 below 0x20, 0x80 below 0x40, else `jg` (signed) on 2n+2 > 0x400000 picks n+0x400001 or 2n+0x11. Only that arm takes `and 0xfffffff0`, because the two constants jump past it to `00715831`. `0071583B` stores dword `[s+4]`. `00715834`-`00715854`: `006DA880([01F3BA68], c+8, '..\src\GPU\TinyEffect\TFXString.cpp', 0x61, 0)`. `0071585E`/`00715861` store `c` to the first qword, buffer = +8, 0 on null. `0071586E` stores `[s+8]`, then `memcpy` at `00715872`. `00715877`-`00715889` terminate only when `[s+4]` is non-zero.
- **`0071A380`** (`0071A380`-`0071A4BF`): exact. `0071A3C3`-`0071A3D2`: `jns`, otherwise `00718400(&t,'-')` and `neg`. `0071A3DE`: `d`=1000000000. `0071A3E3` `cmp ebx,esi; jle` (signed). On `d` <= `v` it sets the seen flag (`ebp`=1), calls `007153B0(&t,len+1,1)`, stores `'0'+v/d` (`idiv`) and keeps `v` = remainder (`0071A418`-`0071A44B`). On `d` > `v` with the flag set, it reserves and stores `'0'` (`0071A3EB`-`0071A40F`). Without the flag it skips. `0071A454`-`0071A46A`: signed /10 by the 0x66666667 multiply, looping while `d` > 1. `0071A470`-`0071A47C`: `00719560(&t, r14=rcx, '0'+v)`. I read `00719560`: it builds the output from `t` and does not modify `t`, so the cached buffer `rdi` is still valid for the free at `0071A489`-`0071A49E`. `0071A4A4` returns `rcx`.
- **`0072DAC0`** (`0072DAC0`-`0072DCE3`): exact. `0072DAED` `cmp byte [01F3CD60],0; je`, `0072DAFA` clears it, and 22 stores follow, `02EA2250`-`02EA22F8`, in the stated order. The first is `00D9F05B`, whose first byte is 0, so it is the empty string. `0072DC43` builds `S`. The 0x16-iteration loop runs `0072DC60`-`0072DCB6`: `00715CC0(&S, origlen)` and `007198A0(&S, [rdi])`, then `call [vtbl+0x60]` with `rdx`=`S` text (`0072DC85`). `0072DC8A` stores `[rbx]`. When it is 0, `ebp`=0x80004005, otherwise `[vtbl+0xc8](obj, v)`, and `js` stores 0. `0072DCBD` frees, and `0072DCC2` returns `ebp`.
- **`0072DCF0`** (`0072DCF0`-`0072DFBE`): exact. `0072DD37`-`0072DD48` take `N` = `S(r8)` cut to len-1. `0072DD55`/`0072DD57` skip the loop for a non-positive `r9d`. `i` starts at 1 (`r13d`). `0072DD94` calls `sprintf('%s%d', N, i)`. The guard at `0072DD99` and the clear at `0072DDA6` sit inside the `i` loop, followed by 22 stores (the first four from the registers loaded with '', `_REINHARDRGB_RGB`, `_REINHARDRGB_RGBFAST` and `_RGB_REINHARDRGB`, the last `_ALPHA_RGB`). Per `i`, `ebp` is reset at `0072DEC5`, and the 22-suffix loop runs `0072DEF0`-`0072DF49` with `rbx` advancing across `i`. `0072DF55`/`0072DF57`: `test ebp; cmovs r12d,ebp`, so any 0x80004005 sticks. Cookie checked at `0072DF9E`.
- **`0072DFD0`** (`0072DFD0`-`0072E2A1`): exact. `N` is cut to len-3 (`0072E01E`). `a` (`r12d`) runs 0..7 (`0072E24B`) and `b` (`ebp`) runs 0..7 (`0072E231`). `sprintf('%s%d_%d', N, a, b)` at `0072E06F`, with `b` as the stack argument. The guard is at `0072E074`/`0072E081`. The 22-suffix loop is `0072E1D0`-`0072E220`, and `rdi`=`rbx` carries across pairs. On zero `v`, `0072E1FC` `je` skips the `+0xc8` call. On a negative result it stores 0 (`0072E211`). `0072E274` returns 0. Cookie checked.
- **`0072E5B0`** (`0072E5B0`-`0072E732`): exact. `N` is len-1. `i` = 1..`r9d` (`0072E613`/`0072E630`). The guard byte `01F3CD63` (`0072E64C`/`0072E655`) fills `02EA23B8`=`00D9F10F` (first byte 0) and `02EA23C0`=`_USNORM`. Per suffix, `00719460` runs at `0072E69D`, then `0072E2B0(r12=rcx, rdi, text)` at `0072E6AE`, and `rdi += 0x268` at `0072E6C2`. `cmovs ebx` (per `i`) feeds `cmovs r15d`, so the result is the last negative. `0072E704` returns `r15d`.
- **`0072E940`** (`0072E940`-`0072EB10`): exact. The guard `01F3CD64` (`0072E96B`/`0072E974`) fills seven stores `02EA23C8`-`02EA23F8` in the stated order. `0072E9E5` builds `S` and `0072E9F5` copies it to `B` (`00715A00`). `c` runs 0..0x7F (`0072EA69` `cmp ebp,0x80; jb`). For each `c`, `00715CC0(&B, len)`, then a seven-step bit loop (`ebx` rotates through 1..0x40, `test ebp,ebx`) appending `[rdi]`. `0072E740(r13, r15=rdx+0x40*c, B text)` at `0072EA58`, with `cmovs r14d`. The copy pass `0072EA90`-`0072EADA`: `(c & 0xC) == 8`, then for k = 0..15, a non-zero dword goes to `[rdx + ((c|4)<<4 + k)*4]`. Both strings are freed, and the saved last-negative is returned (`0072EAF1`).
- **`0072EC00`** (`0072EC00`-`0072EDEC`): exact. `0072EC4C` builds `S`, and `0072EC67` calls `00717650(&S,'[]',0,-1)`. `0072EC77`/`0072EC85` create the empty `A` and `B`. For `k` > 0 (`test ebx; jle`, signed): `007182F0` + `00715CC0` give `A`, and `00718350(&B, S text + k)` gives `B`. The loop over `i` < `r8d` runs `sprintf('%d')`, then `007157A0` to `I`. With `k` > 0 the name is (`A`+`I`)+`B` (two `00719380` calls). Otherwise it is `S`+`I`. `0072ED75` calls `[vtbl+0x48](obj, 0, text)`, `0072ED78` stores `[rsi]`, and `0072ED81` `cmove edi,0x80004005`. Everything is freed, `0072EDC3` returns `edi`, and the cookie is checked.
- **`0078A120`** (`0078A120`-`0078A231`): exact. Argument 5 is `[rsp+0x70]` (entry +0x28) and argument 7 is the byte `[rsp+0x80]`. A null value returns 0x80070057. `0078A15A` writes `*pp`=0. `0078A16D` calls `007906C0(rdx, [rcx+0x30], byte7)`, and null returns 0x80004005. `0078A1A2` allocates 0xE8 with `GPUInterfaceEffect.cpp` and 0x55C. `0078A1B7` calls `00789900(block, rcx)`, skipped on null so `rbx`=0. `0078A1BF` stores `*pp`. `0078A1C8` calls `007897D0(e, s)`, and `0078A1D2` calls `0078A4F0(s)`, a refcount release. Non-negative returns 0. The gates `01F3BA80` and `01F3BA90` use `cmp 1; jb` (unsigned). The two `006DF480` calls (`00DAEEC0`, 0x563, then `00DAEF10` with `r` and `0071B3C0(r)`) log the message, and `0078A216` returns `r`.

**9 of 9 exact.** All 45 anchors were checked.

## SWE2-AUDIT-SPEC limits

- Body statements were checked against the bytes. What the effect interface's vtable slots `+0x48`, `+0x60` and `+0xC8` do is not stated by the rows, and was not checked.
- `0072E2B0`, `0072E740`, `007906C0`, `00789900`, `007897D0` and `00717650` are named only by call shape and return use. Their bodies were not reviewed.
- `v` = INT_MIN in `0071A380` (where `neg` leaves it negative) is outside what the row states, and was not explored.
