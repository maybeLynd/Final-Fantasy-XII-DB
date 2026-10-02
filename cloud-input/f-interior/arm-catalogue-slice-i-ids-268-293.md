# F-interior pack: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-I-ids-268-293.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/arm-catalogue-slice-i-ids-268-293.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 807950d2a	SWE2-CONTRACT: pass-22 debt batch A - 37 Engine-Core-Runtime pages' cross-subsystem neighbour bullet; inbox mentions: repos-78.md). OPUS read these before packing.

## 0017D9C0 (14 B, extent 0017D9C0-0017D9CE)

Page context: "8690' (called from '00625E7C') asks the D3D11 device, vtable slot 30         ('CheckMultisampleQualityLevels'), about 'DXGI_FORMAT_R8G8B8A8_UNORM' ('0x1C') for sample counts 2 to 32. Through         '0017D9C0' → '001DF2B0' ('bts') it sets bit 1 for 2×, bit 2 for 4×, bit 3 for 8×, bit 4 when 8× reports more         than 16 quality levels, and bit 5 for 16×. Bit 0 is the constructor's '1', so "off" is always available.       - **Bit 5 can"

```
0017D9C0  mov      edx, ecx
0017D9C2  mov      rcx, qword ptr [rip + 0x1e05357]  ; -> 01F82D20
0017D9C9  jmp      0x1df2b0  ; -> 001DF2B0 fn
```

## 001DF2B0 (16 B, extent 001DF2B0-001DF2C0)

Page context: " from '00625E7C') asks the D3D11 device, vtable slot 30         ('CheckMultisampleQualityLevels'), about 'DXGI_FORMAT_R8G8B8A8_UNORM' ('0x1C') for sample counts 2 to 32. Through         '0017D9C0' → '001DF2B0' ('bts') it sets bit 1 for 2×, bit 2 for 4×, bit 3 for 8×, bit 4 when 8× reports more         than 16 quality levels, and bit 5 for 16×. Bit 0 is the constructor's '1', so "off" is always available.       - **Bit 5 cannot be select"

```
001DF2B0  mov      eax, dword ptr [rcx + 0x44c]
001DF2B6  bts      eax, edx
001DF2B9  mov      dword ptr [rcx + 0x44c], eax
001DF2BF  ret      
```

## 001E04F0 (83 B, extent 001E04F0-001E0543)

Page context: "at 0:** it stores '-1.0' ('009010A8') at '01DFDDF8' and '0.0' at '01F82D28', and returns 0 (never skip);       - **otherwise:** it runs '001E03F0', asks '00187540' on the '01F7F598' singleton, calls '001E04F0', and returns whether         the accumulated double at '01F82D28' has reached the returned threshold ('comisd' / 'setae', '001E063A'–'001E0648').        So clearing the byte turns the skip decision off and resets its accumulator. "

```
001E04F0  sub      rsp, 0x38
001E04F4  movaps   xmmword ptr [rsp + 0x20], xmm6
001E04F9  call     0x17fe30  ; -> 0017FE30 fn
001E04FE  mov      r8d, eax
001E0501  mov      eax, 0xcccccccd
001E0506  mul      r8d
001E0509  shr      edx, 3
001E050C  lea      ecx, [rdx + rdx*4]
001E050F  add      ecx, ecx
001E0511  cmp      r8d, ecx
001E0514  jne      0x1e0520  ; -> 001E0520
001E0516  movsd    xmm6, qword ptr [rip + 0x720b82]  ; -> 009010A0 [f64 0.01666666667]
001E051E  jmp      0x1e0528  ; -> 001E0528
001E0520  movsd    xmm6, qword ptr [rip + 0x71fe50]  ; -> 00900378 [f64 0.01668333333]
001E0528  call     0x184950  ; -> 00184950 fn
001E052D  movd     xmm0, eax
001E0531  cvtdq2pd xmm0, xmm0
001E0535  mulsd    xmm0, xmm6
001E0539  movaps   xmm6, xmmword ptr [rsp + 0x20]
001E053E  add      rsp, 0x38
001E0542  ret      
```
