# Homing pack: `99-Unresolved-Residual/drawing-one-coloured-rectangle.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-drawing-one-coloured-rectangle.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001B2000 (174 B, extent 001B2000-001B20AE)

Entered from (direct sites whose caller this page cites): `001B0190` + 0x26 (call; `001B0190` is cited on this page)
Other direct sites: none

Host context: "idiom '002D9B00''s count-8 arm runs. Interior anchor '002DD584' (the first '0x10000000' store).  ## SWE2-EC7-110 update (2026-09-20) - '001B0100' measured  '001B0100' (132 B) is the slot-array reset '001B0190', '001B03D0' and '001B1910' run: 'edx' walks '0..dword[+0x3928]' bounded '<= 0x3F', and each 0x58 record at 'rcx + 0x2328 + edx * 0x58' resets - '[+0x40]' pulls '[+0x38]', '+0'/'+8'/'+0x20'/'+0x1C'/ '+0x28' zero, '+0x10'/'+0x14'/ '"

```
001B2000  push     rbx
001B2002  sub      rsp, 0x30
001B2006  movaps   xmmword ptr [rsp + 0x20], xmm6
001B200B  mov      rbx, rcx
001B200E  call     0x189120  ; -> 00189120 fn
001B2013  add      rbx, 0x3aa8
001B201A  lea      rdx, [rax + 0x6c8]
001B2021  mov      ecx, dword ptr [rdx]
001B2023  mov      dword ptr [rbx], ecx
001B2025  mov      ecx, dword ptr [rdx + 4]
001B2028  mov      dword ptr [rbx + 4], ecx
001B202B  mov      ecx, dword ptr [rdx + 8]
001B202E  mov      dword ptr [rbx + 8], ecx
001B2031  mov      ecx, dword ptr [rdx + 0xc]
001B2034  mov      dword ptr [rbx + 0xc], ecx
001B2037  mov      eax, dword ptr [rdx + 0x10]
001B203A  mov      dword ptr [rbx + 0x10], eax
001B203D  mov      eax, dword ptr [rdx + 0x14]
001B2040  mov      dword ptr [rbx + 0x14], eax
001B2043  mov      eax, dword ptr [rdx + 0x18]
001B2046  mov      dword ptr [rbx + 0x18], eax
001B2049  mov      eax, dword ptr [rdx + 0x1c]
001B204C  mov      dword ptr [rbx + 0x1c], eax
001B204F  mov      eax, dword ptr [rdx + 0x20]
001B2052  mov      dword ptr [rbx + 0x20], eax
001B2055  mov      eax, dword ptr [rdx + 0x24]
001B2058  mov      dword ptr [rbx + 0x24], eax
001B205B  mov      eax, dword ptr [rdx + 0x28]
001B205E  mov      dword ptr [rbx + 0x28], eax
001B2061  mov      eax, dword ptr [rdx + 0x2c]
001B2064  mov      dword ptr [rbx + 0x2c], eax
001B2067  mov      eax, dword ptr [rdx + 0x30]
001B206A  mov      dword ptr [rbx + 0x30], eax
001B206D  mov      eax, dword ptr [rdx + 0x34]
001B2070  mov      dword ptr [rbx + 0x34], eax
001B2073  mov      eax, dword ptr [rdx + 0x38]
001B2076  mov      dword ptr [rbx + 0x38], eax
001B2079  mov      eax, dword ptr [rdx + 0x3c]
001B207C  mov      dword ptr [rbx + 0x3c], eax
001B207F  call     0x189120  ; -> 00189120 fn
001B2084  movss    xmm6, dword ptr [rax + 0x754]
001B208C  call     0x189120  ; -> 00189120 fn
001B2091  movaps   xmm2, xmm6
001B2094  mov      rcx, rbx
001B2097  movss    xmm1, dword ptr [rax + 0x750]
001B209F  movaps   xmm6, xmmword ptr [rsp + 0x20]
001B20A4  add      rsp, 0x30
001B20A8  pop      rbx
001B20A9  jmp      0x678b50  ; -> 00678B50 fn
```

## 00403F00 (136 B, extent 00403F00-00403F88)

Entered from (direct sites whose caller this page cites): `002BC9C0` + 0x46 (call; `002BC9C0` is cited on this page)
Other direct sites: none

Host context: "ng it '0x10' twice - the rectangle's per-vertex colour publish.  Interior anchor '003C61F6' (function '003C6140').  '002B9BE0' (143 B) is the lazy singleton-pair installer for this page's '002BCA70'/'002BC9C0' callers: '0209E600' non-existent goes to '00244F50(0xC0, callback=002BCA70)' then '00246AD0' into the '0208EA20' manager; '0209E5F8' does the same with '002BC9C0'/0xC8 and takes '0209E5F0''s '+0x190' into its '+0xC0' before regist"

```
00403F00  mov      qword ptr [rsp + 0x10], rbx
00403F05  push     rdi
00403F06  sub      rsp, 0x20
00403F0A  mov      rdx, qword ptr [r8 + 0x20]
00403F0E  lea      r9, [rsp + 0x30]
00403F13  movzx    ebx, byte ptr [rcx + 0x5c]
00403F17  xor      eax, eax
00403F19  mov      dword ptr [rsp + 0x40], eax
00403F1D  mov      r10, r8
00403F20  lea      r8, [rsp + 0x40]
00403F25  mov      rdi, rcx
00403F28  movzx    eax, word ptr [rdx + 0x14]
00403F2C  mov      word ptr [rsp + 0x44], ax
00403F31  movzx    eax, word ptr [rdx + 0x16]
00403F35  mov      rdx, r10
00403F38  mov      word ptr [rsp + 0x46], ax
00403F3D  mov      rax, qword ptr [rsp + 0x40]
00403F42  mov      qword ptr [rsp + 0x30], rax
00403F47  movzx    eax, word ptr [rcx + 0x50]
00403F4B  neg      ax
00403F4E  mov      word ptr [rsp + 0x30], ax
00403F53  mov      word ptr [rsp + 0x32], ax
00403F58  movsx    eax, word ptr [rsp + 0x36]
00403F5D  movd     xmm0, eax
00403F61  cvtdq2ps xmm0, xmm0
00403F64  mulss    xmm0, dword ptr [rip + 0x90d86c]  ; -> 00D117D8 [f32 1.75]
00403F6C  cvttss2si eax, xmm0
00403F70  mov      word ptr [rsp + 0x36], ax
00403F75  call     0x2d8c80  ; -> 002D8C80 fn
00403F7A  mov      byte ptr [rdi + 0x5c], bl
00403F7D  mov      rbx, qword ptr [rsp + 0x38]
00403F82  add      rsp, 0x20
00403F86  pop      rdi
00403F87  ret      
```
