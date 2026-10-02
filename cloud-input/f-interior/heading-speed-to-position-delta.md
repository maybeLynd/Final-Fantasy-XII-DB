# F-interior pack: `06-Movement-And-Navigation/heading-speed-to-position-delta.md`

Generated 2026-10-02 18:33 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/heading-speed-to-position-delta.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 0022DE60 (1240 B, extent 0022DE60-0022E338)

Page context: "0' twice commits the normalized pair into the block - the cell solver's scale install.  Interior anchor '0022EF95' (function '0022EF20').  '00381D90' (288 B) is the three-kind transformer '0022D7E0'/'0022DE60'/'00232160' call: '00202B70' reads 'rcx+0x50' into 'rsp+0x20', then 'dword[rdi]' dispatches - kind 0 normalises the vector ('x^2+y^2+z^2' into '00861F14', '[rbx+0xC] = 1.0f'), kinds 1/2 run '00380EB0'/'00380E00' on 'rbx'; all paths"

```
0022DE60  mov      r11, rsp
0022DE63  push     rbp
0022DE64  push     rbx
0022DE65  push     r14
0022DE67  push     r15
0022DE69  lea      rbp, [r11 - 0x5f]
0022DE6D  sub      rsp, 0xb8
0022DE74  mov      rax, qword ptr [rip + 0x1d169b5]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0022DE7B  xor      rax, rsp
0022DE7E  mov      qword ptr [rbp - 0x39], rax
0022DE82  mov      r15, qword ptr [rcx + 8]
0022DE86  xor      r14d, r14d
0022DE89  mov      rbx, rcx
0022DE8C  cmp      r14w, word ptr [rcx + 0x14]
0022DE91  jge      0x22e31e  ; -> 0022E31E
0022DE97  mov      qword ptr [r11 + 0x18], rdi
0022DE9B  mov      edx, 0x5000
0022DEA0  mov      qword ptr [r11 + 0x20], r12
0022DEA4  lea      r12, [rip + 0x1e6c425]  ; -> 0209A2D0
0022DEAB  mov      qword ptr [r11 - 0x28], r13
0022DEAF  mov      r13d, 0x4000
0022DEB5  movaps   xmmword ptr [r11 - 0x78], xmm10
0022DEBA  movss    xmm10, dword ptr [rip + 0x1abdce5]  ; -> 01CEBBA8 [f32 1]
0022DEC3  movaps   xmmword ptr [rsp + 0x50], xmm11
0022DEC9  movss    xmm11, dword ptr [rip + 0x6d241a]  ; -> 009002EC [f32 -0.001]
0022DED2  mov      qword ptr [r11 + 0x10], rsi
0022DED6  movaps   xmmword ptr [r11 - 0x38], xmm6
0022DEDB  movaps   xmmword ptr [r11 - 0x48], xmm7
0022DEE0  movaps   xmmword ptr [r11 - 0x58], xmm8
0022DEE5  movaps   xmmword ptr [r11 - 0x68], xmm9
0022DEEA  nop      word ptr [rax + rax]
0022DEF0  movsx    eax, word ptr [rbx + 0x12]
0022DEF4  add      eax, r14d
0022DEF7  movsxd   rcx, eax
0022DEFA  mov      rax, qword ptr [r15 + 0x28]
0022DEFE  movzx    edi, word ptr [rax + rcx*2]
0022DF02  cmp      di, dx
0022DF05  jge      0x22e2c3  ; -> 0022E2C3
0022DF0B  cmp      di, r13w
0022DF0F  jl       0x22e05a  ; -> 0022E05A
0022DF15  movsx    eax, di
0022DF18  sub      eax, r13d
0022DF1B  cdqe     
0022DF1D  lea      rsi, [rax + rax*8]
0022DF21  shl      rsi, 4
0022DF25  add      rsi, qword ptr [r15 + 0x18]
0022DF29  mov      ecx, dword ptr [rsi + 4]
0022DF2C  shr      ecx, 0xd
0022DF2F  and      ecx, 0x1f
0022DF32  add      ecx, 0x20
0022DF35  mov      r8d, ecx
0022DF38  mov      ecx, dword ptr [r12 + rcx*8 + 0x110]
0022DF40  mov      edx, ecx
0022DF42  mov      eax, dword ptr [r12 + r8*8 + 0x114]
0022DF4A  not      edx
0022DF4C  and      edx, dword ptr [rsi + 4]
0022DF4F  and      eax, ecx
0022DF51  or       edx, eax
0022DF53  cmp      edx, 0x80000000
0022DF59  jae      0x22e2be  ; -> 0022E2BE
0022DF5F  mov      r8, qword ptr [rbx + 0x20]
0022DF63  lea      rdx, [rbp - 0x49]
0022DF67  mov      rcx, rsi
0022DF6A  call     0x381d90  ; -> 00381D90 fn
0022DF6F  mov      rax, qword ptr [rbx + 0x18]
0022DF73  movss    xmm4, dword ptr [rbp - 0x49]
0022DF78  movss    xmm2, dword ptr [rbp - 0x41]
0022DF7D  movaps   xmm0, xmm4
0022DF80  movss    xmm6, dword ptr [rbp - 0x45]
0022DF85  movaps   xmm1, xmm2
0022DF88  mulss    xmm0, dword ptr [rax]
0022DF8C  movaps   xmm5, xmm6
0022DF8F  mulss    xmm5, dword ptr [rax + 4]
0022DF94  movaps   xmm3, xmm6
0022DF97  mulss    xmm1, dword ptr [rax + 8]
0022DF9C  mulss    xmm3, dword ptr [rax + 0x14]
0022DFA1  addss    xmm5, xmm0
0022DFA5  mulss    xmm6, dword ptr [rax + 0x24]
0022DFAA  movaps   xmm0, xmm4
0022DFAD  mulss    xmm0, dword ptr [rax + 0x10]
0022DFB2  mulss    xmm4, dword ptr [rax + 0x20]
0022DFB7  addss    xmm5, xmm1
0022DFBB  addss    xmm3, xmm0
0022DFBF  movaps   xmm1, xmm2
0022DFC2  mulss    xmm2, dword ptr [rax + 0x28]
0022DFC7  mulss    xmm1, dword ptr [rax + 0x18]
0022DFCC  addss    xmm6, xmm4
0022DFD0  mulss    xmm5, xmm5
0022DFD4  addss    xmm3, xmm1
0022DFD8  addss    xmm6, xmm2
0022DFDC  mulss    xmm3, xmm3
0022DFE0  mulss    xmm6, xmm6
0022DFE4  addss    xmm5, xmm3
0022DFE8  addss    xmm5, xmm6
0022DFEC  movaps   xmm0, xmm5
0022DFEF  call     0x861f14  ; -> 00861F14 fn
0022DFF4  mov      rdx, qword ptr [rbx + 0x20]
0022DFF8  mov      rcx, rsi
0022DFFB  movaps   xmm6, xmm0
0022DFFE  call     0x3810b0  ; -> 003810B0 fn
0022E003  comiss   xmm6, xmm0
0022E006  jbe      0x22e2be  ; -> 0022E2BE
0022E00C  subss    xmm6, xmm0
0022E010  comiss   xmm6, dword ptr [rbx + 0x30]
0022E014  jbe      0x22e01f  ; -> 0022E01F
0022E016  movss    dword ptr [rbx + 0x30], xmm6
0022E01B  mov      word ptr [rbx + 0x34], di
0022E01F  movss    xmm2, dword ptr [rbp - 0x49]
0022E024  movss    xmm0, dword ptr [rbp - 0x45]
0022E029  movss    xmm1, dword ptr [rbp - 0x41]
0022E02E  mov      rcx, qword ptr [rbx + 0x28]
0022E032  mulss    xmm2, xmm6
0022E036  mulss    xmm0, xmm6
0022E03A  movss    dword ptr [rbp - 0x49], xmm2
0022E03F  mulss    xmm1, xmm6
0022E043  movss    dword ptr [rbp - 0x45], xmm0
0022E048  movss    dword ptr [rbp - 0x41], xmm1
0022E04D  addss    xmm2, dword ptr [rcx]
0022E051  movss    dword ptr [rcx], xmm2
0022E055  jmp      0x22e29a  ; -> 0022E29A
0022E05A  mov      r9, qword ptr [r15 + 0x10]
0022E05E  movsx    rsi, di
0022E062  shl      rsi, 5
0022E066  mov      eax, dword ptr [rsi + r9 + 0xc]
0022E06B  mov      ecx, eax
0022E06D  and      cl, 7
0022E070  cmp      cl, 1
0022E073  jne      0x22e0a9  ; -> 0022E0A9
0022E075  mov      ecx, eax
0022E077  shr      ecx, 0xd
0022E07A  and      ecx, 0x1f
0022E07D  add      ecx, 0x20
0022E080  mov      r8d, ecx
0022E083  mov      ecx, dword ptr [r12 + rcx*8 + 0x110]
0022E08B  mov      edx, ecx
0022E08D  not      edx
0022E08F  and      edx, eax
0022E091  mov      eax, dword ptr [r12 + r8*8 + 0x114]
0022E099  and      eax, ecx
0022E09B  or       edx, eax
0022E09D  cmp      edx, 0x80000000
0022E0A3  jae      0x22e2be  ; -> 0022E2BE
0022E0A9  mov      rax, qword ptr [rbx + 0x18]
0022E0AD  movss    xmm3, dword ptr [rsi + r9]
0022E0B3  movss    dword ptr [rbp - 0x49], xmm3
0022E0B8  movss    xmm6, dword ptr [rsi + r9 + 4]
0022E0BF  movss    dword ptr [rbp - 0x45], xmm6
0022E0C4  movaps   xmm2, xmm6
0022E0C7  movss    xmm4, dword ptr [rsi + r9 + 8]
0022E0CE  movaps   xmm5, xmm6
0022E0D1  movss    dword ptr [rbp - 0x41], xmm4
0022E0D6  movaps   xmm1, xmm4
0022E0D9  movss    xmm0, dword ptr [rsi + r9 + 0xc]
0022E0E0  movss    dword ptr [rbp - 0x3d], xmm0
0022E0E5  movaps   xmm0, xmm3
0022E0E8  mulss    xmm2, dword ptr [rax + 0x14]
0022E0ED  mulss    xmm0, dword ptr [rax]
0022E0F1  mulss    xmm5, dword ptr [rax + 4]
0022E0F6  mulss    xmm1, dword ptr [rax + 8]
0022E0FB  mulss    xmm6, dword ptr [rax + 0x24]
0022E100  addss    xmm5, xmm0
0022E104  movaps   xmm0, xmm3
0022E107  mulss    xmm3, dword ptr [rax + 0x20]
0022E10C  mulss    xmm0, dword ptr [rax + 0x10]
0022E111  addss    xmm5, xmm1
0022E115  movaps   xmm1, xmm4
0022E118  mulss    xmm1, dword ptr [rax + 0x18]
0022E11D  addss    xmm6, xmm3
0022E121  mulss    xmm4, dword ptr [rax + 0x28]
0022E126  addss    xmm2, xmm0
0022E12A  mulss    xmm5, xmm5
0022E12E  addss    xmm6, xmm4
0022E132  addss    xmm2, xmm1
0022E136  mulss    xmm6, xmm6
0022E13A  mulss    xmm2, xmm2
0022E13E  addss    xmm2, xmm5
0022E142  addss    xmm2, xmm6
0022E146  movaps   xmm0, xmm2
0022E149  call     0x861f14  ; -> 00861F14 fn
0022E14E  mov      rcx, qword ptr [r15 + 0x10]
0022E152  movaps   xmm9, xmm0
0022E156  mov      r8, qword ptr [rbx + 0x20]
0022E15A  movsx    rax, word ptr [rsi + rcx + 0x10]
0022E160  movss    xmm1, dword ptr [r8]
0022E165  movss    xmm6, dword ptr [r8 + 4]
0022E16B  movss    xmm0, dword ptr [r8 + 8]
0022E171  shl      rax, 4
0022E175  add      rax, qword ptr [r15 + 8]
0022E179  subss    xmm6, dword ptr [rax + 4]
0022E17E  subss    xmm1, dword ptr [rax]
0022E182  subss    xmm0, dword ptr [rax + 8]
0022E187  mulss    xmm6, dword ptr [rsi + rcx + 4]
0022E18D  mulss    xmm1, dword ptr [rsi + rcx]
0022E192  mulss    xmm0, dword ptr [rsi + rcx + 8]
0022E198  addss    xmm6, xmm1
0022E19C  addss    xmm6, xmm0
0022E1A0  comiss   xmm6, xmm11
0022E1A4  jbe      0x22e2be  ; -> 0022E2BE
0022E1AA  comiss   xmm9, xmm6
0022E1AE  jbe      0x22e2be  ; -> 0022E2BE
0022E1B4  lea      r9, [rbp - 0x59]
0022E1B8  movzx    edx, di
0022E1BB  mov      rcx, r15
0022E1BE  call     0x22eac0  ; -> 0022EAC0 fn
0022E1C3  test     eax, eax
0022E1C5  je       0x22e2be  ; -> 0022E2BE
0022E1CB  movss    xmm0, dword ptr [rbp - 0x59]
0022E1D0  movss    xmm1, dword ptr [rbp - 0x55]
0022E1D5  movss    xmm2, dword ptr [rbp - 0x51]
0022E1DA  mulss    xmm0, xmm0
0022E1DE  mulss    xmm1, xmm1
0022E1E2  mulss    xmm2, xmm2
0022E1E6  addss    xmm0, xmm1
0022E1EA  addss    xmm0, xmm2
0022E1EE  call     0x861f14  ; -> 00861F14 fn
0022E1F3  comiss   xmm9, xmm0
0022E1F7  jbe      0x22e2be  ; -> 0022E2BE
0022E1FD  comiss   xmm0, xmm6
0022E200  jbe      0x22e20e  ; -> 0022E20E
0022E202  movaps   xmm6, xmm0
0022E205  movaps   xmm0, xmmword ptr [rbp - 0x59]
0022E209  movdqa   xmmword ptr [rbp - 0x49], xmm0
0022E20E  subss    xmm9, xmm6
0022E213  comiss   xmm9, dword ptr [rbx + 0x30]
0022E218  jbe      0x22e224  ; -> 0022E224
0022E21A  movss    dword ptr [rbx + 0x30], xmm9
0022E220  mov      word ptr [rbx + 0x34], di
0022E224  movss    xmm8, dword ptr [rbp - 0x49]
0022E22A  movss    xmm6, dword ptr [rbp - 0x45]
0022E22F  movaps   xmm0, xmm8
0022E233  movss    xmm7, dword ptr [rbp - 0x41]
0022E238  movaps   xmm1, xmm6
0022E23B  mulss    xmm0, xmm8
0022E240  movaps   xmm2, xmm7
0022E243  mulss    xmm1, xmm6
0022E247  mulss    xmm2, xmm7
0022E24B  addss    xmm0, xmm1
0022E24F  addss    xmm0, xmm2
0022E253  call     0x861f14  ; -> 00861F14 fn
0022E258  mov      rcx, qword ptr [rbx + 0x28]
0022E25C  movaps   xmm1, xmm10
0022E260  divss    xmm1, xmm0
0022E264  mulss    xmm8, xmm9
0022E269  mulss    xmm6, xmm9
0022E26E  mulss    xmm8, xmm1
0022E273  mulss    xmm7, xmm9
0022E278  movss    dword ptr [rbp - 0x49], xmm8
0022E27E  mulss    xmm6, xmm1
0022E282  mulss    xmm7, xmm1
0022E286  movss    dword ptr [rbp - 0x45], xmm6
0022E28B  movss    dword ptr [rbp - 0x41], xmm7
0022E290  addss    xmm8, dword ptr [rcx]
0022E295  movss    dword ptr [rcx], xmm8
0022E29A  movss    xmm0, dword ptr [rbp - 0x45]
0022E29F  addss    xmm0, dword ptr [rcx + 4]
0022E2A4  movss    dword ptr [rcx + 4], xmm0
0022E2A9  movss    xmm1, dword ptr [rbp - 0x41]
0022E2AE  addss    xmm1, dword ptr [rcx + 8]
0022E2B3  movss    dword ptr [rcx + 8], xmm1
0022E2B8  mov      eax, dword ptr [rcx + 0xc]
0022E2BB  mov      dword ptr [rcx + 0xc], eax
0022E2BE  mov      edx, 0x5000
0022E2C3  movsx    eax, word ptr [rbx + 0x14]
0022E2C7  inc      r14d
0022E2CA  cmp      r14d, eax
0022E2CD  jl       0x22def0  ; -> 0022DEF0
0022E2D3  movaps   xmm11, xmmword ptr [rsp + 0x50]
0022E2D9  movaps   xmm10, xmmword ptr [rsp + 0x60]
0022E2DF  movaps   xmm9, xmmword ptr [rsp + 0x70]
0022E2E5  movaps   xmm8, xmmword ptr [rsp + 0x80]
0022E2EE  movaps   xmm7, xmmword ptr [rsp + 0x90]
0022E2F6  movaps   xmm6, xmmword ptr [rsp + 0xa0]
0022E2FE  mov      r13, qword ptr [rsp + 0xb0]
0022E306  mov      r12, qword ptr [rsp + 0xf8]
0022E30E  mov      rdi, qword ptr [rsp + 0xf0]
0022E316  mov      rsi, qword ptr [rsp + 0xe8]
0022E31E  mov      rcx, qword ptr [rbp - 0x39]
0022E322  xor      rcx, rsp
0022E325  call     0x808c40  ; -> 00808C40 fn
0022E32A  add      rsp, 0xb8
0022E331  pop      r15
0022E333  pop      r14
0022E335  pop      rbx
0022E336  pop      rbp
0022E337  ret      
```

## 00232760 (104 B, extent 00232760-002327C8)

Page context: "hen '0046BFA0' + '00808C40' + '00861F14' run the magnitude/normalise pass - the heading delta's length arm.  Interior anchor '003814E2' (function '00381450').  '0022F250' (471 B) is the nearest-scan '00232760'/'002327D0' call: stack-cookie prologue, 'dword[020891E4]' bounds a loop over the '020891F0' table, each entry's 'movss'/'subss' against '[rbx]'/'[rbx+4]' builds the delta vector on '[rsp+0x20]', and '00202B70'/'00202B90'/'00808C40"

```
00232760  mov      qword ptr [rsp + 8], rbx
00232765  push     rdi
00232766  sub      rsp, 0x20
0023276A  mov      rbx, rdx
0023276D  mov      rdi, rcx
00232770  call     0x233110  ; -> 00233110 fn
00232775  mov      rcx, rbx
00232778  call     0x22ef20  ; -> 0022EF20 fn
0023277D  movsx    r9d, word ptr [rbx + 0x52]
00232782  xor      ecx, ecx
00232784  mov      dword ptr [rip + 0x1e56a56], ecx  ; -> 020891E0
0023278A  mov      eax, r9d
0023278D  test     r9d, r9d
00232790  js       0x2327a2  ; -> 002327A2
00232792  mov      dword ptr [rip + 0x1e56848], eax  ; -> 02088FE0
00232798  mov      dword ptr [rip + 0x1e56a3e], 1  ; -> 020891E0
002327A2  mov      dword ptr [rip + 0x1e56a3c], ecx  ; -> 020891E4
002327A8  mov      r8, rbx
002327AB  mov      rcx, rdi
002327AE  mov      rdx, rbx
002327B1  call     0x22f9b0  ; -> 0022F9B0 fn
002327B6  mov      rcx, rbx
002327B9  mov      rbx, qword ptr [rsp + 0x30]
002327BE  add      rsp, 0x20
002327C2  pop      rdi
002327C3  jmp      0x22f250  ; -> 0022F250 fn
```

## 00380FA0 (263 B, extent 00380FA0-003810A7)

Page context: "es the delta step and '00861F14' copies under the cookie check - the cell solver's second per-element move.  Interior anchor '0022E8E8' (function '0022E7D0').  '00381450' (477 B) is the delta helper '00380FA0' and '003810B0' call: '[r8] - [rdx]' takes the four-component difference into xmm3/xmm0/xmm2/xmm1, then '0046BFA0' + '00808C40' + '00861F14' run the magnitude/normalise pass - the heading delta's length arm.  Interior anchor '00381"

```
00380FA0  push     rbx
00380FA2  push     rbp
00380FA3  push     rsi
00380FA4  push     rdi
00380FA5  push     r14
00380FA7  sub      rsp, 0x60
00380FAB  mov      rax, qword ptr [rip + 0x1bc387e]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00380FB2  xor      rax, rsp
00380FB5  mov      qword ptr [rsp + 0x50], rax
00380FBA  mov      r14, rdx
00380FBD  mov      rsi, rcx
00380FC0  add      rdx, 0x50
00380FC4  lea      rcx, [rsp + 0x30]
00380FC9  mov      rdi, r9
00380FCC  mov      rbp, r8
00380FCF  call     0x202b70  ; -> 00202B70 fn
00380FD4  mov      r8, rdi
00380FD7  lea      rdx, [r14 + 0x50]
00380FDB  lea      rcx, [rsp + 0x20]
00380FE0  call     0x202b70  ; -> 00202B70 fn
00380FE5  mov      ecx, dword ptr [r14]
00380FE8  test     ecx, ecx
00380FEA  je       0x381026  ; -> 00381026
00380FEC  sub      ecx, 1
00380FEF  je       0x381010  ; -> 00381010
00380FF1  cmp      ecx, 1
00380FF4  jne      0x381087  ; -> 00381087
00380FFA  lea      r8, [rsp + 0x20]
00380FFF  lea      rdx, [rsp + 0x30]
00381004  lea      rcx, [rsp + 0x40]
00381009  call     0x381450  ; -> 00381450 fn
0038100E  jmp      0x38103a  ; -> 0038103A
00381010  lea      r8, [rsp + 0x20]
00381015  lea      rdx, [rsp + 0x30]
0038101A  lea      rcx, [rsp + 0x40]
0038101F  call     0x381630  ; -> 00381630 fn
00381024  jmp      0x38103a  ; -> 0038103A
00381026  lea      r8, [rsp + 0x20]
0038102B  lea      rdx, [rsp + 0x30]
00381030  lea      rcx, [rsp + 0x40]
00381035  call     0x381ac0  ; -> 00381AC0 fn
0038103A  test     eax, eax
0038103C  je       0x381087  ; -> 00381087
0038103E  lea      rdx, [r14 + 0x10]
00381042  mov      rcx, rsi
00381045  lea      r8, [rsp + 0x40]
0038104A  call     0x202b70  ; -> 00202B70 fn
0038104F  movss    xmm2, dword ptr [rsi]
00381053  movss    xmm0, dword ptr [rsi + 4]
00381058  subss    xmm0, dword ptr [rbp + 4]
0038105D  subss    xmm2, dword ptr [rbp]
00381062  movss    xmm1, dword ptr [rsi + 8]
00381067  subss    xmm1, dword ptr [rbp + 8]
0038106C  mulss    xmm0, xmm0
00381070  mulss    xmm2, xmm2
00381074  mulss    xmm1, xmm1
00381078  addss    xmm0, xmm2
0038107C  addss    xmm0, xmm1
00381080  call     0x861f14  ; -> 00861F14 fn
00381085  jmp      0x38108f  ; -> 0038108F
00381087  movss    xmm0, dword ptr [rip + 0x196ac0d]  ; -> 01CEBC9C [f32 -1]
0038108F  mov      rcx, qword ptr [rsp + 0x50]
00381094  xor      rcx, rsp
00381097  call     0x808c40  ; -> 00808C40 fn
0038109C  add      rsp, 0x60
003810A0  pop      r14
003810A2  pop      rdi
003810A3  pop      rsi
003810A4  pop      rbp
003810A5  pop      rbx
003810A6  ret      
```

## 00381630 (1168 B, extent 00381630-00381AC0)

Page context: "00202B70'/'00202B90'/'00808C40'/'00861F14' score it - the delta family's table search.  Interior anchor '0022F2FA' (function '0022F250').  '0046BFA0' (294 B) is the projection coefficient '00381450'/'00381630' call: 'd = rcx - r9' (three 'subss'), '00861F14' consumes '|rdx|^2', then 'xmm3 = -(rdx.d) / (r8.d)' computes the ratio and 'xmm0 = |rdx|^2 x xmm3' returns the scaled coefficient - the length arm's numerator/denominator pass.  Int"

```
00381630  mov      rax, rsp
00381633  mov      qword ptr [rax + 0x18], rbx
00381637  push     rbp
00381638  push     rsi
00381639  push     rdi
0038163A  lea      rbp, [rax - 0x5f]
0038163E  sub      rsp, 0xf0
00381645  movaps   xmmword ptr [rax - 0x28], xmm6
00381649  movaps   xmmword ptr [rax - 0x38], xmm7
0038164D  movaps   xmmword ptr [rax - 0x48], xmm8
00381652  movaps   xmmword ptr [rax - 0x58], xmm9
00381657  movaps   xmmword ptr [rax - 0x68], xmm10
0038165C  movaps   xmmword ptr [rax - 0x78], xmm11
00381661  movaps   xmmword ptr [rax - 0x88], xmm12
00381669  movaps   xmmword ptr [rsp + 0x70], xmm13
0038166F  mov      rax, qword ptr [rip + 0x1bc31ba]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00381676  xor      rax, rsp
00381679  mov      qword ptr [rbp - 0x59], rax
0038167D  movss    xmm7, dword ptr [r8]
00381682  mov      rsi, r8
00381685  subss    xmm7, dword ptr [rdx]
00381689  movss    xmm1, dword ptr [r8 + 0xc]
0038168F  mov      rdi, rdx
00381692  movss    xmm8, dword ptr [r8 + 8]
00381698  mov      rbx, rcx
0038169B  subss    xmm8, dword ptr [rdx + 8]
003816A1  movss    xmm10, dword ptr [r8 + 4]
003816A7  movss    xmm6, dword ptr [rdx + 4]
003816AC  movaps   xmm0, xmm10
003816B0  subss    xmm0, xmm6
003816B4  movss    dword ptr [rbp - 0x7d], xmm1
003816B9  movaps   xmm1, xmm7
003816BC  movss    dword ptr [rsp + 0x20], xmm7
003816C2  mulss    xmm1, xmm7
003816C6  movaps   xmm2, xmm8
003816CA  mulss    xmm2, xmm8
003816CF  movss    dword ptr [rsp + 0x24], xmm0
003816D5  mulss    xmm0, xmm0
003816D9  movss    dword ptr [rsp + 0x28], xmm8
003816E0  addss    xmm0, xmm1
003816E4  addss    xmm0, xmm2
003816E8  call     0x861f14  ; -> 00861F14 fn
003816ED  movss    xmm9, dword ptr [rip + 0x196a4b2]  ; -> 01CEBBA8 [f32 1]
003816F6  movaps   xmm13, xmm0
003816FA  comiss   xmm6, xmm9
003816FE  xorps    xmm11, xmm11
00381702  jbe      0x3817cf  ; -> 003817CF
00381708  comiss   xmm9, xmm10
0038170C  jbe      0x3818a8  ; -> 003818A8
00381712  lea      r9, [rip + 0x98fb67]  ; -> 00D11280
00381719  mov      rcx, rdi
0038171C  lea      r8, [rip + 0x98fb5d]  ; -> 00D11280
00381723  lea      rdx, [rsp + 0x20]
00381728  call     0x46bfa0  ; -> 0046BFA0 fn
0038172D  comiss   xmm0, xmm11
00381731  jbe      0x3817c2  ; -> 003817C2
00381737  comiss   xmm13, xmm0
0038173B  jbe      0x3817c2  ; -> 003817C2
00381741  movss    xmm7, dword ptr [rsp + 0x20]
00381747  movss    xmm8, dword ptr [rsp + 0x28]
0038174E  movaps   xmm6, xmm7
00381751  movss    xmm12, dword ptr [rsp + 0x24]
00381758  movaps   xmm10, xmm8
0038175C  divss    xmm0, xmm13
00381761  mulss    xmm6, xmm0
00381765  mulss    xmm10, xmm0
0038176A  addss    xmm6, dword ptr [rdi]
0038176E  mulss    xmm12, xmm0
00381773  addss    xmm10, dword ptr [rdi + 8]
00381779  addss    xmm12, dword ptr [rdi + 4]
0038177F  movaps   xmm1, xmm6
00381782  mulss    xmm1, xmm6
00381786  movaps   xmm0, xmm10
0038178A  mulss    xmm0, xmm10
0038178F  addss    xmm0, xmm1
00381793  call     0x861f14  ; -> 00861F14 fn
00381798  comiss   xmm9, xmm0
0038179C  jbe      0x3817cf  ; -> 003817CF
0038179E  movss    xmm0, dword ptr [rbp - 0x7d]
003817A3  mov      eax, 1
003817A8  movss    dword ptr [rbx], xmm6
003817AC  movss    dword ptr [rbx + 4], xmm12
003817B2  movss    dword ptr [rbx + 8], xmm10
003817B8  movss    dword ptr [rbx + 0xc], xmm0
003817BD  jmp      0x381a79  ; -> 00381A79
003817C2  movss    xmm8, dword ptr [rsp + 0x28]
003817C9  movss    xmm7, dword ptr [rsp + 0x20]
003817CF  movaps   xmmword ptr [rsp + 0x60], xmm14
003817D5  movss    xmm14, dword ptr [rip + 0x196a4be]  ; -> 01CEBC9C [f32 -1]
003817DE  comiss   xmm14, dword ptr [rdi + 4]
003817E3  jbe      0x3818bc  ; -> 003818BC
003817E9  movss    xmm0, dword ptr [rsi + 4]
003817EE  comiss   xmm0, xmm14
003817F2  jbe      0x381a71  ; -> 00381A71
003817F8  lea      r9, [rip + 0x98fa91]  ; -> 00D11290
003817FF  mov      rcx, rdi
00381802  lea      r8, [rip + 0x98fa87]  ; -> 00D11290
00381809  lea      rdx, [rsp + 0x20]
0038180E  call     0x46bfa0  ; -> 0046BFA0 fn
00381813  comiss   xmm0, xmm11
00381817  jbe      0x3818af  ; -> 003818AF
0038181D  comiss   xmm13, xmm0
00381821  jbe      0x3818af  ; -> 003818AF
00381827  movss    xmm7, dword ptr [rsp + 0x20]
0038182D  movss    xmm8, dword ptr [rsp + 0x28]
00381834  movaps   xmm6, xmm7
00381837  movss    xmm12, dword ptr [rsp + 0x24]
0038183E  movaps   xmm10, xmm8
00381842  divss    xmm0, xmm13
00381847  mulss    xmm6, xmm0
0038184B  mulss    xmm10, xmm0
00381850  addss    xmm6, dword ptr [rdi]
00381854  mulss    xmm12, xmm0
00381859  addss    xmm10, dword ptr [rdi + 8]
0038185F  addss    xmm12, dword ptr [rdi + 4]
00381865  movaps   xmm1, xmm6
00381868  mulss    xmm1, xmm6
0038186C  movaps   xmm0, xmm10
00381870  mulss    xmm0, xmm10
00381875  addss    xmm0, xmm1
00381879  call     0x861f14  ; -> 00861F14 fn
0038187E  comiss   xmm9, xmm0
00381882  jbe      0x3818bc  ; -> 003818BC
00381884  movss    xmm0, dword ptr [rbp - 0x7d]
00381889  movss    dword ptr [rbx], xmm6
0038188D  movss    dword ptr [rbx + 4], xmm12
00381893  movss    dword ptr [rbx + 8], xmm10
00381899  movss    dword ptr [rbx + 0xc], xmm0
0038189E  mov      eax, 1
003818A3  jmp      0x381a73  ; -> 00381A73
003818A8  xor      eax, eax
003818AA  jmp      0x381a79  ; -> 00381A79
003818AF  movss    xmm8, dword ptr [rsp + 0x28]
003818B6  movss    xmm7, dword ptr [rsp + 0x20]
003818BC  movss    xmm0, dword ptr [rdi]
003818C0  movaps   xmm10, xmm7
003818C4  movss    xmm1, dword ptr [rdi + 8]
003818C9  movaps   xmm12, xmm8
003818CD  movss    dword ptr [rbp - 0x79], xmm0
003818D2  mulss    xmm10, xmm7
003818D7  mov      dword ptr [rbp - 0x75], 0
003818DE  mulss    xmm12, xmm8
003818E3  mov      dword ptr [rbp - 0x6d], 0x3f800000
003818EA  movaps   xmm0, xmm10
003818EE  movss    dword ptr [rbp - 0x71], xmm1
003818F3  addss    xmm0, xmm11
003818F8  addss    xmm0, xmm12
003818FD  call     0x861f14  ; -> 00861F14 fn
00381902  movss    xmm1, dword ptr [rip + 0x587506]  ; -> 00908E10 [u32 0x358637BD]
0038190A  comiss   xmm1, xmm0
0038190D  jbe      0x381915  ; -> 00381915
0038190F  movaps   xmm2, xmm11
00381913  jmp      0x38191d  ; -> 0038191D
00381915  movaps   xmm2, xmm9
00381919  divss    xmm2, xmm0
0038191D  movaps   xmm1, xmm2
00381920  mov      dword ptr [rbp - 0x5d], 0x3f800000
00381927  mulss    xmm1, xmm11
0038192C  lea      r8, [rbp - 0x79]
00381930  lea      rdx, [rbp - 0x69]
00381934  movaps   xmm0, xmm7
00381937  lea      rcx, [rip + 0x98f932]  ; -> 00D11270
0038193E  mulss    xmm0, xmm2
00381942  movss    dword ptr [rbp - 0x65], xmm1
00381947  movaps   xmm1, xmm8
0038194B  mulss    xmm1, xmm2
0038194F  movss    dword ptr [rbp - 0x69], xmm0
00381954  movss    dword ptr [rbp - 0x61], xmm1
00381959  call     0x46bf60  ; -> 0046BF60 fn
0038195E  addss    xmm10, xmm11
00381963  movaps   xmm6, xmm0
00381966  addss    xmm10, xmm12
0038196B  movaps   xmm0, xmm10
0038196F  call     0x861f14  ; -> 00861F14 fn
00381974  movaps   xmm12, xmm0
00381978  movaps   xmm10, xmm6
0038197C  divss    xmm10, xmm12
00381981  movaps   xmm0, xmm10
00381985  mulss    xmm7, xmm10
0038198A  mulss    xmm0, xmm11
0038198F  addss    xmm7, dword ptr [rbp - 0x79]
00381994  mulss    xmm8, xmm10
00381999  addss    xmm0, dword ptr [rbp - 0x75]
0038199E  addss    xmm8, dword ptr [rbp - 0x71]
003819A4  mulss    xmm7, xmm7
003819A8  mulss    xmm0, xmm0
003819AC  mulss    xmm8, xmm8
003819B1  addss    xmm0, xmm7
003819B5  addss    xmm0, xmm8
003819BA  call     0x861f14  ; -> 00861F14 fn
003819BF  mov      rcx, rdi
003819C2  movaps   xmm7, xmm0
003819C5  call     0x382020  ; -> 00382020 fn
003819CA  test     eax, eax
003819CC  jne      0x3819f4  ; -> 003819F4
003819CE  mov      rcx, rsi
003819D1  call     0x382020  ; -> 00382020 fn
003819D6  test     eax, eax
003819D8  jne      0x3819f4  ; -> 003819F4
003819DA  comiss   xmm7, xmm9
003819DE  ja       0x381a71  ; -> 00381A71
003819E4  comiss   xmm11, xmm10
003819E8  ja       0x381a71  ; -> 00381A71
003819EE  comiss   xmm10, xmm9
003819F2  ja       0x381a71  ; -> 00381A71
003819F4  movaps   xmm0, xmm7
003819F7  call     0x861f56  ; -> 00861F56 fn
003819FC  call     0x861f0e  ; -> 00861F0E fn
00381A01  movss    xmm2, dword ptr [rsp + 0x20]
00381A07  subss    xmm6, xmm0
00381A0B  movss    xmm0, dword ptr [rbp - 0x7d]
00381A10  movss    xmm3, dword ptr [rsp + 0x24]
00381A16  movss    xmm1, dword ptr [rsp + 0x28]
00381A1C  movss    dword ptr [rbx + 0xc], xmm0
00381A21  divss    xmm6, xmm12
00381A26  mulss    xmm2, xmm6
00381A2A  mulss    xmm3, xmm6
00381A2E  movss    dword ptr [rbx], xmm2
00381A32  mulss    xmm1, xmm6
00381A36  movss    dword ptr [rbx + 4], xmm3
00381A3B  movss    dword ptr [rbx + 8], xmm1
00381A40  addss    xmm2, dword ptr [rdi]
00381A44  movss    dword ptr [rbx], xmm2
00381A48  addss    xmm3, dword ptr [rdi + 4]
00381A4D  comiss   xmm3, xmm9
00381A51  movss    dword ptr [rbx + 4], xmm3
00381A56  addss    xmm1, dword ptr [rdi + 8]
00381A5B  movss    dword ptr [rbx + 0xc], xmm0
00381A60  movss    dword ptr [rbx + 8], xmm1
00381A65  ja       0x381a71  ; -> 00381A71
00381A67  comiss   xmm14, xmm3
00381A6B  jbe      0x38189e  ; -> 0038189E
00381A71  xor      eax, eax
00381A73  movaps   xmm14, xmmword ptr [rsp + 0x60]
00381A79  mov      rcx, qword ptr [rbp - 0x59]
00381A7D  xor      rcx, rsp
00381A80  call     0x808c40  ; -> 00808C40 fn
00381A85  lea      r11, [rsp + 0xf0]
00381A8D  mov      rbx, qword ptr [r11 + 0x30]
00381A91  movaps   xmm6, xmmword ptr [r11 - 0x10]
00381A96  movaps   xmm7, xmmword ptr [r11 - 0x20]
00381A9B  movaps   xmm8, xmmword ptr [r11 - 0x30]
00381AA0  movaps   xmm9, xmmword ptr [r11 - 0x40]
00381AA5  movaps   xmm10, xmmword ptr [r11 - 0x50]
00381AAA  movaps   xmm11, xmmword ptr [r11 - 0x60]
00381AAF  movaps   xmm12, xmmword ptr [r11 - 0x70]
00381AB4  movaps   xmm13, xmmword ptr [r11 - 0x80]
00381AB9  mov      rsp, r11
00381ABC  pop      rdi
00381ABD  pop      rsi
00381ABE  pop      rbp
00381ABF  ret      
```
