# F homing pack: `16-UI/Widget-Object-Model/the-widget-message-protocol.md`

Generated 2026-10-02 21:16 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 24. No bearing page cites them and no documented function calls them directly.

## 0023BB20 (407 B, extent 0023BB20-0023BCB7)

Documented callee on this page: `0029FE20`

```
0023BB20  push     rbp
0023BB22  push     rsi
0023BB23  push     rdi
0023BB24  push     r14
0023BB26  push     r15
0023BB28  sub      rsp, 0x20
0023BB2C  mov      rdi, rdx
0023BB2F  movsxd   rbp, r9d
0023BB32  mov      edx, 0x18
0023BB37  mov      r14, rcx
0023BB3A  nop      word ptr [rax + rax]
0023BB40  mov      rax, qword ptr [rdi + 0x10]
0023BB44  mov      r8, qword ptr [rdx + rax - 0x18]
0023BB49  and      dword ptr [r8 + 8], 0xfffffffe
0023BB4E  mov      rax, qword ptr [rdi + 0x10]
0023BB52  mov      rcx, qword ptr [rdx + rax - 0x10]
0023BB57  and      dword ptr [rcx + 8], 0xfffffffe
0023BB5B  mov      rax, qword ptr [rdi + 0x10]
0023BB5F  mov      rcx, qword ptr [rdx + rax - 8]
0023BB64  and      dword ptr [rcx + 8], 0xfffffffe
0023BB68  mov      rax, qword ptr [rdi + 0x10]
0023BB6C  mov      rcx, qword ptr [rdx + rax]
0023BB70  and      dword ptr [rcx + 8], 0xfffffffe
0023BB74  mov      rax, qword ptr [rdi + 0x10]
0023BB78  mov      rcx, qword ptr [rdx + rax + 8]
0023BB7D  and      dword ptr [rcx + 8], 0xfffffffe
0023BB81  mov      rax, qword ptr [rdi + 0x10]
0023BB85  mov      rcx, qword ptr [rdx + rax + 0x10]
0023BB8A  add      rdx, 0x30
0023BB8E  and      dword ptr [rcx + 8], 0xfffffffe
0023BB92  cmp      rdx, 0xa0
0023BB99  jle      0x23bb40  ; -> 0023BB40
0023BB9B  xor      r8d, r8d
0023BB9E  lea      rcx, [rbp*4]
0023BBA6  add      rcx, rbp
0023BBA9  lea      r15, [rip + 0x6d8b60]  ; -> 00914710
0023BBB0  mov      eax, r8d
0023BBB3  lea      rsi, [rcx*4]
0023BBBB  nop      dword ptr [rax + rax]
0023BBC0  mov      rcx, qword ptr [rdi + 0x10]
0023BBC4  mov      rdx, qword ptr [rax + rcx]
0023BBC8  cmp      dword ptr [rsi + r15 + 8], r8d
0023BBCD  jne      0x23bbd5  ; -> 0023BBD5
0023BBCF  or       dword ptr [rdx + 8], 1
0023BBD3  jmp      0x23bbd9  ; -> 0023BBD9
0023BBD5  and      dword ptr [rdx + 8], 0xfffffffe
0023BBD9  inc      r8d
0023BBDC  add      rax, 8
0023BBE0  cmp      rax, 0x88
0023BBE6  jle      0x23bbc0  ; -> 0023BBC0
0023BBE8  cmp      dword ptr [rsi + r15 + 4], 0
0023BBEE  jne      0x23bc46  ; -> 0023BC46
0023BBF0  movsxd   rax, dword ptr [rsi + r15 + 8]
0023BBF5  lea      r8, [rsp + 0x50]
0023BBFA  mov      rcx, qword ptr [rdi + 0x10]
0023BBFE  lea      rdx, [rsp + 0x68]
0023BC03  mov      rcx, qword ptr [rcx + rax*8]
0023BC07  call     0x29fe20  ; -> 0029FE20 fn
0023BC0C  mov      rax, qword ptr [rdi + 0x10]
0023BC10  mov      rdx, qword ptr [rax + 0x70]
0023BC14  mov      rcx, qword ptr [rdx]
0023BC17  movzx    eax, word ptr [rcx + 4]
0023BC1B  add      ax, word ptr [rsp + 0x68]
0023BC20  mov      word ptr [rdx + 0xc], ax
0023BC24  movzx    eax, word ptr [rcx + 8]
0023BC28  sub      ax, word ptr [rsp + 0x68]
0023BC2D  or       dword ptr [rdx + 8], 1
0023BC31  mov      word ptr [rdx + 0x10], ax
0023BC35  mov      eax, 1
0023BC3A  add      rsp, 0x20
0023BC3E  pop      r15
0023BC40  pop      r14
0023BC42  pop      rdi
0023BC43  pop      rsi
0023BC44  pop      rbp
0023BC45  ret      
0023BC46  movsxd   rdx, dword ptr [rsi + r15 + 8]
0023BC4B  mov      rax, qword ptr [rdi + 0x10]
0023BC4F  mov      ecx, dword ptr [rsi + r15 + 0xc]
0023BC54  mov      qword ptr [rsp + 0x58], rbx
0023BC59  mov      rbx, qword ptr [rax + rdx*8]
0023BC5D  call     0x2f9860  ; -> 002F9860 fn
0023BC62  xor      ecx, ecx
0023BC64  mov      qword ptr [rbx + 0x18], rax
0023BC68  call     0x20e620  ; -> 0020E620 fn
0023BC6D  mov      dword ptr [rbx + 0x20], eax
0023BC70  movsxd   rcx, dword ptr [rsi + r15 + 8]
0023BC75  mov      rax, qword ptr [rdi + 0x10]
0023BC79  mov      rbx, qword ptr [rax + rcx*8]
0023BC7D  mov      ecx, ebp
0023BC7F  mov      eax, 1
0023BC84  shl      rax, cl
0023BC87  mov      rcx, qword ptr [r14 + 0x720]
0023BC8E  and      rcx, rax
0023BC91  neg      rcx
0023BC94  sbb      ecx, ecx
0023BC96  and      ecx, 2
0023BC99  call     0x2dd7e0  ; -> 002DD7E0 fn
0023BC9E  mov      dword ptr [rbx + 0x24], eax
0023BCA1  mov      eax, 1
0023BCA6  mov      rbx, qword ptr [rsp + 0x58]
0023BCAB  add      rsp, 0x20
0023BCAF  pop      r15
0023BCB1  pop      r14
0023BCB3  pop      rdi
0023BCB4  pop      rsi
0023BCB5  pop      rbp
0023BCB6  ret      
```

## 0023CD20 (236 B, extent 0023CD20-0023CE0C)

Documented callee on this page: `0029FE20`

```
0023CD20  mov      qword ptr [rsp + 0x10], rbx
0023CD25  mov      qword ptr [rsp + 8], rcx
0023CD2A  push     rdi
0023CD2B  sub      rsp, 0x20
0023CD2F  movsxd   rax, r9d
0023CD32  mov      rdi, rdx
0023CD35  lea      rdx, [rip + 0x1e519a4]  ; -> 0208E6E0
0023CD3C  lea      rcx, [rax + rax*4]
0023CD40  lea      rcx, [rcx*4]
0023CD48  mov      eax, dword ptr [rcx + rdx + 4]
0023CD4C  test     eax, eax
0023CD4E  je       0x23cd93  ; -> 0023CD93
0023CD50  dec      eax
0023CD52  cmp      eax, 3
0023CD55  ja       0x23cdfc  ; -> 0023CDFC
0023CD5B  mov      rax, qword ptr [rdi + 0x10]
0023CD5F  mov      rbx, qword ptr [rax + 0x18]
0023CD63  or       dword ptr [rbx + 8], 1
0023CD67  mov      ecx, dword ptr [rcx + rdx + 8]
0023CD6B  call     0x2f9860  ; -> 002F9860 fn
0023CD70  xor      ecx, ecx
0023CD72  mov      qword ptr [rbx + 0x18], rax
0023CD76  call     0x20e620  ; -> 0020E620 fn
0023CD7B  mov      dword ptr [rbx + 0x20], eax
0023CD7E  mov      rax, qword ptr [rdi + 0x10]
0023CD82  mov      rcx, qword ptr [rax + 0x10]
0023CD86  and      dword ptr [rcx + 8], 0xfffffffe
0023CD8A  mov      rax, qword ptr [rdi + 0x10]
0023CD8E  mov      rcx, qword ptr [rax]
0023CD91  jmp      0x23cdf8  ; -> 0023CDF8
0023CD93  mov      rax, qword ptr [rdi + 0x10]
0023CD97  mov      ecx, dword ptr [rcx + rdx + 8]
0023CD9B  mov      rbx, qword ptr [rax]
0023CD9E  call     0x2f9860  ; -> 002F9860 fn
0023CDA3  xor      ecx, ecx
0023CDA5  mov      qword ptr [rbx + 0x18], rax
0023CDA9  call     0x20e620  ; -> 0020E620 fn
0023CDAE  or       dword ptr [rbx + 8], 1
0023CDB2  lea      r8, [rsp + 0x30]
0023CDB7  lea      rdx, [rsp + 0x48]
0023CDBC  mov      dword ptr [rbx + 0x20], eax
0023CDBF  mov      rcx, rbx
0023CDC2  call     0x29fe20  ; -> 0029FE20 fn
0023CDC7  mov      rax, qword ptr [rdi + 0x10]
0023CDCB  mov      rdx, qword ptr [rax + 0x10]
0023CDCF  mov      rcx, qword ptr [rdx]
0023CDD2  movzx    eax, word ptr [rcx + 4]
0023CDD6  add      ax, word ptr [rsp + 0x48]
0023CDDB  mov      word ptr [rdx + 0xc], ax
0023CDDF  movzx    eax, word ptr [rcx + 8]
0023CDE3  sub      ax, word ptr [rsp + 0x48]
0023CDE8  or       dword ptr [rdx + 8], 1
0023CDEC  mov      word ptr [rdx + 0x10], ax
0023CDF0  mov      rax, qword ptr [rdi + 0x10]
0023CDF4  mov      rcx, qword ptr [rax + 0x18]
0023CDF8  and      dword ptr [rcx + 8], 0xfffffffe
0023CDFC  mov      eax, 1
0023CE01  mov      rbx, qword ptr [rsp + 0x38]
0023CE06  add      rsp, 0x20
0023CE0A  pop      rdi
0023CE0B  ret      
```

## 00241D00 (59 B, extent 00241D00-00241D3B)

Documented callee on this page: `002D8910`

```
00241D00  push     rbx
00241D02  sub      rsp, 0x30
00241D06  xor      ecx, ecx
00241D08  mov      rbx, rdx
00241D0B  test     r8d, r8d
00241D0E  setne    cl
00241D11  add      ecx, 0x3e8
00241D17  call     0x2f9860  ; -> 002F9860 fn
00241D1C  mov      r9, rax
00241D1F  mov      qword ptr [rsp + 0x20], 0
00241D28  xor      r8d, r8d
00241D2B  xor      edx, edx
00241D2D  mov      rcx, rbx
00241D30  call     0x2d8910  ; -> 002D8910 fn
00241D35  add      rsp, 0x30
00241D39  pop      rbx
00241D3A  ret      
```

## 00242A80 (264 B, extent 00242A80-00242B88)

Documented callee on this page: `002D8C80`

```
00242A80  mov      qword ptr [rsp + 0x10], rbx
00242A85  mov      qword ptr [rsp + 0x18], rbp
00242A8A  push     rsi
00242A8B  push     rdi
00242A8C  push     r14
00242A8E  sub      rsp, 0x30
00242A92  mov      rax, qword ptr [rip + 0x1e4bff7]  ; -> 0208EA90
00242A99  mov      r14, rcx
00242A9C  mov      ecx, 0xfff
00242AA1  mov      esi, r8d
00242AA4  mov      edi, edx
00242AA6  mov      ebp, r9d
00242AA9  mov      rbx, qword ptr [rax + 0x20]
00242AAD  movzx    eax, word ptr [rbx + 0x44]
00242AB1  add      rbx, 0x30
00242AB5  movzx    r11d, word ptr [rbx + rax*2 + 0x24]
00242ABB  movzx    r10d, word ptr [rbx + 0x10]
00242AC0  add      r10, rbx
00242AC3  movzx    eax, word ptr [r10 + r11*8]
00242AC8  mov      word ptr [rsp + 0x20], ax
00242ACD  movzx    eax, word ptr [r10 + r11*8 + 2]
00242AD3  mov      word ptr [rsp + 0x22], ax
00242AD8  movzx    eax, word ptr [r10 + r11*8 + 4]
00242ADE  and      ax, cx
00242AE1  mov      word ptr [rsp + 0x24], ax
00242AE6  mov      eax, dword ptr [r10 + r11*8 + 4]
00242AEB  shr      eax, 0xc
00242AEE  and      ax, cx
00242AF1  mov      ecx, 0x65
00242AF6  mov      word ptr [rsp + 0x26], ax
00242AFB  movzx    r8d, byte ptr [r10 + r11*8 + 7]
00242B01  movzx    edx, word ptr [rbx + 0x12]
00242B05  mov      eax, r8d
00242B08  shr      eax, 4
00242B0B  and      r8b, 0xf
00242B0F  movzx    eax, al
00242B12  add      rax, rbx
00242B15  movzx    eax, byte ptr [rdx + rax]
00242B19  add      al, r8b
00242B1C  mov      byte ptr [r14 + 0x5c], al
00242B20  call     0x2dd7e0  ; -> 002DD7E0 fn
00242B25  mov      dword ptr [r14 + 0x90], eax
00242B2C  mov      edx, 1
00242B31  movzx    eax, word ptr [rsp + 0x70]
00242B36  mov      rcx, r14
00242B39  mov      word ptr [rsp + 0x56], ax
00242B3E  mov      word ptr [rsp + 0x50], di
00242B43  mov      word ptr [rsp + 0x52], si
00242B48  mov      word ptr [rsp + 0x54], bp
00242B4D  call     0x2d8bb0  ; -> 002D8BB0 fn
00242B52  mov      rdx, qword ptr [rip + 0x1e4bf37]  ; -> 0208EA90
00242B59  lea      r9, [rsp + 0x50]
00242B5E  lea      r8, [rsp + 0x20]
00242B63  mov      rcx, r14
00242B66  call     0x2d8c80  ; -> 002D8C80 fn
00242B6B  xor      edx, edx
00242B6D  mov      rcx, r14
00242B70  call     0x2d8bb0  ; -> 002D8BB0 fn
00242B75  mov      rbx, qword ptr [rsp + 0x58]
00242B7A  mov      rbp, qword ptr [rsp + 0x60]
00242B7F  add      rsp, 0x30
00242B83  pop      r14
00242B85  pop      rdi
00242B86  pop      rsi
00242B87  ret      
```

## 00276770 (80 B, extent 00276770-002767C0)

Documented callee on this page: `002753F0`

```
00276770  sub      rsp, 0x58
00276774  mov      rax, qword ptr [rip + 0x1cce0b5]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0027677B  xor      rax, rsp
0027677E  mov      qword ptr [rsp + 0x40], rax
00276783  xor      edx, edx
00276785  mov      dword ptr [rsp + 0x28], 0x2d
0027678D  mov      dword ptr [rsp + 0x20], edx
00276791  lea      rax, [rsp + 0x20]
00276796  mov      qword ptr [rsp + 0x38], rdx
0027679B  lea      rdx, [rsp + 0x28]
002767A0  mov      qword ptr [rsp + 0x30], rax
002767A5  call     0x2753f0  ; -> 002753F0 fn
002767AA  mov      eax, dword ptr [rsp + 0x20]
002767AE  mov      rcx, qword ptr [rsp + 0x40]
002767B3  xor      rcx, rsp
002767B6  call     0x808c40  ; -> 00808C40 fn
002767BB  add      rsp, 0x58
002767BF  ret      
```

## 0027F1A0 (100 B, extent 0027F1A0-0027F204)

Documented callee on this page: `002B58B0`

```
0027F1A0  push     rdi
0027F1A2  sub      rsp, 0x20
0027F1A6  xor      eax, eax
0027F1A8  mov      rdi, rcx
0027F1AB  mov      qword ptr [rcx], rax
0027F1AE  mov      qword ptr [rcx + 8], rax
0027F1B2  mov      qword ptr [rcx + 0x10], rax
0027F1B6  mov      qword ptr [rcx + 0x18], rax
0027F1BA  mov      eax, 0xffff
0027F1BF  mov      word ptr [rcx + 8], dx
0027F1C3  cmp      dx, ax
0027F1C6  je       0x27f1fe  ; -> 0027F1FE
0027F1C8  shl      edx, 0x10
0027F1CB  mov      ecx, 1
0027F1D0  mov      qword ptr [rsp + 0x30], rbx
0027F1D5  call     0x35d330  ; -> 0035D330 fn
0027F1DA  xor      edx, edx
0027F1DC  mov      rbx, rax
0027F1DF  mov      rcx, qword ptr [rax + 0x18]
0027F1E3  call     0x2b58b0  ; -> 002B58B0 fn
0027F1E8  mov      qword ptr [rdi], rax
0027F1EB  movzx    ecx, byte ptr [rbx + 0x2c]
0027F1EF  mov      byte ptr [rdi + 0xa], cl
0027F1F2  movzx    eax, byte ptr [rbx + 0x38]
0027F1F6  mov      rbx, qword ptr [rsp + 0x30]
0027F1FB  mov      byte ptr [rdi + 0xb], al
0027F1FE  add      rsp, 0x20
0027F202  pop      rdi
0027F203  ret      
```

## 00283620 (103 B, extent 00283620-00283687)

Documented callee on this page: `002527B0`

```
00283620  sub      rsp, 0x28
00283624  mov      r8, qword ptr [rip + 0x1e17605]  ; -> 0209AC30
0028362B  xor      r9d, r9d
0028362E  mov      edx, r9d
00283631  add      r8, 0xac8
00283638  nop      dword ptr [rax + rax]
00283640  mov      rax, qword ptr [r8]
00283643  movzx    r10d, word ptr [rax + 0x60]
00283648  test     r10w, r10w
0028364C  js       0x283656  ; -> 00283656
0028364E  movsx    eax, r10w
00283652  cmp      eax, ecx
00283654  je       0x28366d  ; -> 0028366D
00283656  inc      r9d
00283659  inc      rdx
0028365C  add      r8, 8
00283660  cmp      rdx, 9
00283664  jl       0x283640  ; -> 00283640
00283666  xor      eax, eax
00283668  add      rsp, 0x28
0028366C  ret      
0028366D  mov      edx, 4
00283672  mov      r8d, r9d
00283675  lea      ecx, [rdx + 2]
00283678  call     0x2527b0  ; -> 002527B0 fn
0028367D  mov      eax, 1
00283682  add      rsp, 0x28
00283686  ret      
```

## 00283BB0 (647 B, extent 00283BB0-00283E37)

Documented callee on this page: `00368360`

```
00283BB0  mov      qword ptr [rsp + 0x18], rbx
00283BB5  push     rdi
00283BB6  sub      rsp, 0x50
00283BBA  mov      rax, qword ptr [rip + 0x1cc0c6f]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00283BC1  xor      rax, rsp
00283BC4  mov      qword ptr [rsp + 0x40], rax
00283BC9  mov      rbx, rcx
00283BCC  mov      rdi, rdx
00283BCF  mov      ecx, dword ptr [rdx]
00283BD1  sub      ecx, 1
00283BD4  je       0x283dac  ; -> 00283DAC
00283BDA  sub      ecx, 1
00283BDD  je       0x283ce7  ; -> 00283CE7
00283BE3  sub      ecx, 1
00283BE6  je       0x283c9c  ; -> 00283C9C
00283BEC  cmp      ecx, 1
00283BEF  je       0x283bfe  ; -> 00283BFE
00283BF1  mov      rcx, rbx
00283BF4  call     0x5c5230  ; -> 005C5230 fn
00283BF9  jmp      0x283e1f  ; -> 00283E1F
00283BFE  movzx    eax, word ptr [rbx + 0xf0]
00283C05  test     ax, ax
00283C08  jle      0x283c49  ; -> 00283C49
00283C0A  mov      ecx, 5
00283C0F  cmp      ax, word ptr [rbx + 0xf2]
00283C16  jg       0x283c1d  ; -> 00283C1D
00283C18  mov      ecx, 4
00283C1D  call     0x2dd7e0  ; -> 002DD7E0 fn
00283C22  mov      r9d, eax
00283C25  mov      edx, 4
00283C2A  mov      rax, qword ptr [rbx + 0x60]
00283C2E  lea      r8d, [rdx - 1]
00283C32  mov      rcx, qword ptr [rax + 0x120]
00283C39  movsx    eax, word ptr [rbx + 0xf0]
00283C40  mov      dword ptr [rsp + 0x20], eax
00283C44  call     0x29f6e0  ; -> 0029F6E0 fn
00283C49  movzx    eax, word ptr [rbx + 0xf4]
00283C50  test     ax, ax
00283C53  jle      0x283e1d  ; -> 00283E1D
00283C59  mov      ecx, 5
00283C5E  cmp      ax, word ptr [rbx + 0xf6]
00283C65  jg       0x283c6c  ; -> 00283C6C
00283C67  mov      ecx, 4
00283C6C  call     0x2dd7e0  ; -> 002DD7E0 fn
00283C71  mov      r9d, eax
00283C74  mov      edx, 3
00283C79  mov      rax, qword ptr [rbx + 0x60]
00283C7D  mov      r8d, edx
00283C80  mov      rcx, qword ptr [rax + 0x178]
00283C87  movsx    eax, word ptr [rbx + 0xf4]
00283C8E  mov      dword ptr [rsp + 0x20], eax
00283C92  call     0x29f6e0  ; -> 0029F6E0 fn
00283C97  jmp      0x283e1d  ; -> 00283E1D
00283C9C  test     byte ptr [rbx + 0xfc], 1
00283CA3  je       0x283e1d  ; -> 00283E1D
00283CA9  mov      eax, 0x12
00283CAE  mov      byte ptr [rsp + 0x38], 0
00283CB3  mov      word ptr [rsp + 0x30], ax
00283CB8  mov      rcx, rbx
00283CBB  movsx    eax, word ptr [rbx + 0x9e]
00283CC2  cdq      
00283CC3  mov      dword ptr [rsp + 0x3a], 0x60001
00283CCB  sub      eax, edx
00283CCD  lea      rdx, [rsp + 0x30]
00283CD2  sar      eax, 1
00283CD4  sub      ax, 8
00283CD8  mov      word ptr [rsp + 0x32], ax
00283CDD  call     0x368360  ; -> 00368360 fn
00283CE2  jmp      0x283e1d  ; -> 00283E1D
00283CE7  mov      rax, qword ptr [rbx + 0x60]
00283CEB  xor      r8d, r8d
00283CEE  cmp      word ptr [rbx + 0xf0], r8w
00283CF6  mov      edx, r8d
00283CF9  setg     dl
00283CFC  mov      rcx, qword ptr [rax + 0x140]
00283D03  and      dword ptr [rcx + 8], 0xfffffffe
00283D07  or       dword ptr [rcx + 8], edx
00283D0A  mov      rax, qword ptr [rbx + 0x60]
00283D0E  mov      rcx, qword ptr [rax + 0x120]
00283D15  and      dword ptr [rcx + 8], 0xfffffffe
00283D19  or       dword ptr [rcx + 8], edx
00283D1C  mov      rax, qword ptr [rbx + 0x60]
00283D20  mov      rcx, qword ptr [rax + 0x128]
00283D27  and      dword ptr [rcx + 8], 0xfffffffe
00283D2B  or       dword ptr [rcx + 8], edx
00283D2E  mov      rax, qword ptr [rbx + 0x60]
00283D32  mov      rcx, qword ptr [rax + 0x130]
00283D39  and      dword ptr [rcx + 8], 0xfffffffe
00283D3D  or       dword ptr [rcx + 8], edx
00283D40  mov      rax, qword ptr [rbx + 0x60]
00283D44  mov      rcx, qword ptr [rax + 0x138]
00283D4B  and      dword ptr [rcx + 8], 0xfffffffe
00283D4F  or       dword ptr [rcx + 8], edx
00283D52  mov      rax, qword ptr [rbx + 0x60]
00283D56  cmp      word ptr [rbx + 0xf4], r8w
00283D5E  setg     r8b
00283D62  mov      rcx, qword ptr [rax + 0x190]
00283D69  and      dword ptr [rcx + 8], 0xfffffffe
00283D6D  or       dword ptr [rcx + 8], r8d
00283D71  mov      rax, qword ptr [rbx + 0x60]
00283D75  mov      rcx, qword ptr [rax + 0x178]
00283D7C  and      dword ptr [rcx + 8], 0xfffffffe
00283D80  or       dword ptr [rcx + 8], r8d
00283D84  mov      rax, qword ptr [rbx + 0x60]
00283D88  mov      rcx, qword ptr [rax + 0x180]
00283D8F  and      dword ptr [rcx + 8], 0xfffffffe
00283D93  or       dword ptr [rcx + 8], r8d
00283D97  mov      rax, qword ptr [rbx + 0x60]
00283D9B  mov      rcx, qword ptr [rax + 0x188]
00283DA2  and      dword ptr [rcx + 8], 0xfffffffe
00283DA6  or       dword ptr [rcx + 8], r8d
00283DAA  jmp      0x283e1d  ; -> 00283E1D
00283DAC  and      dword ptr [rbx + 0x40], 0xfffff7ff
00283DB3  lea      rcx, [rbx + 0x50]
00283DB7  mov      rax, qword ptr [rip + 0x1e16e72]  ; -> 0209AC30
00283DBE  mov      r9, rbx
00283DC1  mov      r8d, 0xe
00283DC7  mov      rdx, qword ptr [rax + 0x30]
00283DCB  call     0x2432b0  ; -> 002432B0 fn
00283DD0  movzx    r8d, word ptr [rax + 0xa]
00283DD5  movzx    edx, word ptr [rax + 8]
00283DD9  movsx    ecx, word ptr [rax + 6]
00283DDD  movzx    eax, word ptr [rax + 4]
00283DE1  mov      word ptr [rbx + 0x98], ax
00283DE8  mov      word ptr [rbx + 0x9a], cx
00283DEF  mov      word ptr [rbx + 0x9c], dx
00283DF6  mov      word ptr [rbx + 0x9e], r8w
00283DFE  movzx    eax, byte ptr [rdi + 0x10]
00283E02  mov      byte ptr [rbx + 0xf8], al
00283E08  mov      eax, dword ptr [rdi + 8]
00283E0B  shl      eax, 6
00283E0E  xor      eax, dword ptr [rbx + 0xfc]
00283E14  and      eax, 0x40
00283E17  xor      dword ptr [rbx + 0xfc], eax
00283E1D  xor      eax, eax
00283E1F  mov      rcx, qword ptr [rsp + 0x40]
00283E24  xor      rcx, rsp
00283E27  call     0x808c40  ; -> 00808C40 fn
00283E2C  mov      rbx, qword ptr [rsp + 0x70]
00283E31  add      rsp, 0x50
00283E35  pop      rdi
00283E36  ret      
```

## 00284450 (400 B, extent 00284450-002845E0)

Documented callee on this page: `00242C90`

```
00284450  push     rbx
00284452  sub      rsp, 0x30
00284456  mov      rbx, rcx
00284459  mov      ecx, dword ptr [rdx]
0028445B  sub      ecx, 1
0028445E  je       0x284581  ; -> 00284581
00284464  sub      ecx, 1
00284467  je       0x284519  ; -> 00284519
0028446D  sub      ecx, 1
00284470  je       0x2844c7  ; -> 002844C7
00284472  sub      ecx, 0xe
00284475  je       0x28448d  ; -> 0028448D
00284477  cmp      ecx, 1
0028447A  je       0x2845d8  ; -> 002845D8
00284480  mov      rcx, rbx
00284483  add      rsp, 0x30
00284487  pop      rbx
00284488  jmp      0x5c5230  ; -> 005C5230 fn
0028448D  cmp      qword ptr [rdx + 8], 1
00284492  jne      0x2845d8  ; -> 002845D8
00284498  test     rbx, rbx
0028449B  jne      0x2844b1  ; -> 002844B1
0028449D  xor      ecx, ecx
0028449F  xor      r8d, r8d
002844A2  xor      edx, edx
002844A4  call     0x247510  ; -> 00247510 fn
002844A9  xor      eax, eax
002844AB  add      rsp, 0x30
002844AF  pop      rbx
002844B0  ret      
002844B1  mov      rcx, qword ptr [rbx + 0x10]
002844B5  xor      r8d, r8d
002844B8  xor      edx, edx
002844BA  call     0x247510  ; -> 00247510 fn
002844BF  xor      eax, eax
002844C1  add      rsp, 0x30
002844C5  pop      rbx
002844C6  ret      
002844C7  mov      rcx, qword ptr [rbx + 0xd8]
002844CE  test     rcx, rcx
002844D1  je       0x2845d8  ; -> 002845D8
002844D7  test     byte ptr [rcx + 0xfc], 1
002844DE  je       0x2845d8  ; -> 002845D8
002844E4  movsx    eax, word ptr [rcx + 0x9e]
002844EB  xor      r8d, r8d
002844EE  movsx    r9d, word ptr [rcx + 0x9c]
002844F6  xor      ecx, ecx
002844F8  mov      qword ptr [rsp + 0x28], rcx
002844FD  sub      r9d, 0x20
00284501  mov      dword ptr [rsp + 0x20], eax
00284505  lea      edx, [rcx + 0x20]
00284508  mov      rcx, qword ptr [rbx + 0x38]
0028450C  call     0x242c90  ; -> 00242C90 fn
00284511  xor      eax, eax
00284513  add      rsp, 0x30
00284517  pop      rbx
00284518  ret      
00284519  mov      rcx, qword ptr [rbx + 0xd8]
00284520  test     rcx, rcx
00284523  je       0x284571  ; -> 00284571
00284525  test     byte ptr [rcx + 0xfc], 0x30
0028452C  mov      rax, qword ptr [rbx + 0x60]
00284530  mov      r8, qword ptr [rax + 0x30]
00284534  jne      0x28454b  ; -> 0028454B
00284536  and      dword ptr [r8 + 8], 0xfffffffe
0028453B  mov      rcx, rbx
0028453E  call     0x2d0410  ; -> 002D0410 fn
00284543  xor      eax, eax
00284545  add      rsp, 0x30
00284549  pop      rbx
0028454A  ret      
0028454B  or       dword ptr [r8 + 8], 1
00284550  mov      edx, dword ptr [rcx + 0xfc]
00284556  mov      rax, qword ptr [r8 + 0x20]
0028455A  shr      edx, 5
0028455D  and      edx, 1
00284560  movsxd   rcx, edx
00284563  movzx    ecx, byte ptr [rax + rcx*8 + 7]
00284568  mov      byte ptr [r8 + 0x39], cl
0028456C  mov      word ptr [r8 + 0xa], dx
00284571  mov      rcx, rbx
00284574  call     0x2d0410  ; -> 002D0410 fn
00284579  xor      eax, eax
0028457B  add      rsp, 0x30
0028457F  pop      rbx
00284580  ret      
00284581  mov      rax, qword ptr [rip + 0x1e166a8]  ; -> 0209AC30
00284588  lea      rcx, [rbx + 0x50]
0028458C  mov      r9, rbx
0028458F  mov      r8d, 0x10
00284595  mov      rdx, qword ptr [rax + 0x30]
00284599  call     0x2432b0  ; -> 002432B0 fn
0028459E  movzx    ecx, word ptr [rax + 0xa]
002845A2  movzx    edx, word ptr [rax + 8]
002845A6  movsx    r8d, word ptr [rax + 6]
002845AB  test     rbx, rbx
002845AE  je       0x2845d1  ; -> 002845D1
002845B0  movzx    eax, word ptr [rax + 4]
002845B4  mov      word ptr [rbx + 0x98], ax
002845BB  mov      word ptr [rbx + 0x9a], r8w
002845C3  mov      word ptr [rbx + 0x9c], dx
002845CA  mov      word ptr [rbx + 0x9e], cx
002845D1  and      dword ptr [rbx + 0x40], 0xfffff7ff
002845D8  xor      eax, eax
002845DA  add      rsp, 0x30
002845DE  pop      rbx
002845DF  ret      
```

## 00296A10 (86 B, extent 00296A10-00296A66)

Documented callee on this page: `0029AE50`

```
00296A10  test     rcx, rcx
00296A13  je       0x296a65  ; -> 00296A65
00296A15  push     rbx
00296A16  sub      rsp, 0x20
00296A1A  mov      rbx, rcx
00296A1D  mov      qword ptr [rcx + 0xb50], rdx
00296A24  call     0x29aef0  ; -> 0029AEF0 fn
00296A29  movsx    rax, byte ptr [rbx + 0xb48]
00296A31  imul     rcx, rax, 0x160
00296A38  movzx    eax, word ptr [rcx + rbx + 0x318]
00296A40  test     al, 1
00296A42  je       0x296a56  ; -> 00296A56
00296A44  or       ax, 4
00296A48  mov      word ptr [rcx + rbx + 0x318], ax
00296A50  add      rsp, 0x20
00296A54  pop      rbx
00296A55  ret      
00296A56  xor      edx, edx
00296A58  mov      rcx, rbx
00296A5B  call     0x29ae50  ; -> 0029AE50 fn
00296A60  add      rsp, 0x20
00296A64  pop      rbx
00296A65  ret      
```

## 00299AC0 (196 B, extent 00299AC0-00299B84)

Documented callee on this page: `002735E0`

```
00299AC0  push     rbx
00299AC2  sub      rsp, 0x20
00299AC6  mov      rbx, rcx
00299AC9  mov      ecx, dword ptr [rdx]
00299ACB  sub      ecx, 1
00299ACE  je       0x299b0d  ; -> 00299B0D
00299AD0  cmp      ecx, 0x10
00299AD3  mov      rcx, rbx
00299AD6  je       0x299ae2  ; -> 00299AE2
00299AD8  add      rsp, 0x20
00299ADC  pop      rbx
00299ADD  jmp      0x5c5230  ; -> 005C5230 fn
00299AE2  cmp      qword ptr [rdx + 8], 1
00299AE7  jne      0x299afb  ; -> 00299AFB
00299AE9  mov      edx, 7
00299AEE  call     0x247930  ; -> 00247930 fn
00299AF3  xor      eax, eax
00299AF5  add      rsp, 0x20
00299AF9  pop      rbx
00299AFA  ret      
00299AFB  mov      edx, 8
00299B00  call     0x247930  ; -> 00247930 fn
00299B05  xor      eax, eax
00299B07  add      rsp, 0x20
00299B0B  pop      rbx
00299B0C  ret      
00299B0D  mov      rax, qword ptr [rip + 0x1e0111c]  ; -> 0209AC30
00299B14  lea      rcx, [rbx + 0x50]
00299B18  mov      r9, rbx
00299B1B  mov      r8d, 0x33
00299B21  mov      rdx, qword ptr [rax + 8]
00299B25  call     0x2432b0  ; -> 002432B0 fn
00299B2A  movzx    ecx, word ptr [rax + 0xa]
00299B2E  movzx    edx, word ptr [rax + 8]
00299B32  movsx    r8d, word ptr [rax + 6]
00299B37  test     rbx, rbx
00299B3A  je       0x299b5d  ; -> 00299B5D
00299B3C  movzx    eax, word ptr [rax + 4]
00299B40  mov      word ptr [rbx + 0x98], ax
00299B47  mov      word ptr [rbx + 0x9a], r8w
00299B4F  mov      word ptr [rbx + 0x9c], dx
00299B56  mov      word ptr [rbx + 0x9e], cx
00299B5D  mov      edx, 7
00299B62  mov      rcx, rbx
00299B65  call     0x247930  ; -> 00247930 fn
00299B6A  xor      ecx, ecx
00299B6C  call     0x2735e0  ; -> 002735E0 fn
00299B71  mov      rdx, rax
00299B74  mov      rcx, rbx
00299B77  call     0x247570  ; -> 00247570 fn
00299B7C  xor      eax, eax
00299B7E  add      rsp, 0x20
00299B82  pop      rbx
00299B83  ret      
```

## 0029B120 (147 B, extent 0029B120-0029B1B3)

Documented callee on this page: `00247930`

```
0029B120  mov      qword ptr [rsp + 0x10], rbx
0029B125  mov      qword ptr [rsp + 0x18], rbp
0029B12A  push     rsi
0029B12B  sub      rsp, 0x20
0029B12F  xor      ebx, ebx
0029B131  mov      ebp, edx
0029B133  mov      rsi, rcx
0029B136  cmp      byte ptr [rcx + 0xb42], bl
0029B13C  jbe      0x29b1a3  ; -> 0029B1A3
0029B13E  mov      qword ptr [rsp + 0x30], rdi
0029B143  movsxd   rdi, ebx
0029B146  lea      rcx, [rsi + 0x240]
0029B14D  imul     rax, rdi, 0x160
0029B154  add      rcx, rax
0029B157  cmp      ebx, ebp
0029B159  jne      0x29b16c  ; -> 0029B16C
0029B15B  mov      edx, 2
0029B160  call     0x247930  ; -> 00247930 fn
0029B165  mov      edx, 3
0029B16A  jmp      0x29b17b  ; -> 0029B17B
0029B16C  mov      edx, 4
0029B171  call     0x247930  ; -> 00247930 fn
0029B176  mov      edx, 5
0029B17B  imul     rax, rdi, 0xd8
0029B182  lea      rcx, [rsi + 0x7c0]
0029B189  add      rcx, rax
0029B18C  call     0x247930  ; -> 00247930 fn
0029B191  movzx    eax, byte ptr [rsi + 0xb42]
0029B198  inc      ebx
0029B19A  cmp      ebx, eax
0029B19C  jl       0x29b143  ; -> 0029B143
0029B19E  mov      rdi, qword ptr [rsp + 0x30]
0029B1A3  mov      rbx, qword ptr [rsp + 0x38]
0029B1A8  mov      rbp, qword ptr [rsp + 0x40]
0029B1AD  add      rsp, 0x20
0029B1B1  pop      rsi
0029B1B2  ret      
```

## 0029B700 (143 B, extent 0029B700-0029B78F)

Documented callee on this page: `002735E0`

```
0029B700  push     rbx
0029B702  sub      rsp, 0x20
0029B706  cmp      dword ptr [rdx], 1
0029B709  mov      rbx, rcx
0029B70C  je       0x29b718  ; -> 0029B718
0029B70E  add      rsp, 0x20
0029B712  pop      rbx
0029B713  jmp      0x5c5230  ; -> 005C5230 fn
0029B718  mov      rax, qword ptr [rip + 0x1dff511]  ; -> 0209AC30
0029B71F  add      rcx, 0x50
0029B723  mov      r9, rbx
0029B726  mov      r8d, 0x31
0029B72C  mov      rdx, qword ptr [rax + 8]
0029B730  call     0x2432b0  ; -> 002432B0 fn
0029B735  movzx    ecx, word ptr [rax + 0xa]
0029B739  movzx    edx, word ptr [rax + 8]
0029B73D  movsx    r8d, word ptr [rax + 6]
0029B742  test     rbx, rbx
0029B745  je       0x29b768  ; -> 0029B768
0029B747  movzx    eax, word ptr [rax + 4]
0029B74B  mov      word ptr [rbx + 0x98], ax
0029B752  mov      word ptr [rbx + 0x9a], r8w
0029B75A  mov      word ptr [rbx + 0x9c], dx
0029B761  mov      word ptr [rbx + 0x9e], cx
0029B768  xor      ecx, ecx
0029B76A  call     0x2735e0  ; -> 002735E0 fn
0029B76F  mov      rdx, rax
0029B772  mov      rcx, rbx
0029B775  call     0x247570  ; -> 00247570 fn
0029B77A  mov      edx, 0xa
0029B77F  mov      rcx, rbx
0029B782  call     0x247930  ; -> 00247930 fn
0029B787  xor      eax, eax
0029B789  add      rsp, 0x20
0029B78D  pop      rbx
0029B78E  ret      
```

## 0029C850 (379 B, extent 0029C850-0029C9CB)

Documented callee on this page: `002468A0`

```
0029C850  mov      qword ptr [rsp + 0x18], rsi
0029C855  push     rdi
0029C856  sub      rsp, 0x30
0029C85A  lea      rsi, [rcx + 0xc0]
0029C861  mov      rdi, rcx
0029C864  mov      rcx, rsi
0029C867  call     0x273a20  ; -> 00273A20 fn
0029C86C  test     eax, eax
0029C86E  je       0x29c923  ; -> 0029C923
0029C874  test     byte ptr [rdi + 0xb4a], 8
0029C87B  jne      0x29c8d1  ; -> 0029C8D1
0029C87D  xor      ecx, ecx
0029C87F  test     rsi, rsi
0029C882  je       0x29c8bc  ; -> 0029C8BC
0029C884  mov      eax, dword ptr [rsi + 0x7c]
0029C887  mov      edx, ecx
0029C889  and      al, 0xf
0029C88B  cmp      al, 1
0029C88D  sete     dl
0029C890  test     edx, edx
0029C892  je       0x29c8a9  ; -> 0029C8A9
0029C894  mov      rcx, rsi
0029C897  call     0x245020  ; -> 00245020 fn
0029C89C  xor      eax, eax
0029C89E  mov      rsi, qword ptr [rsp + 0x50]
0029C8A3  add      rsp, 0x30
0029C8A7  pop      rdi
0029C8A8  ret      
0029C8A9  test     rsi, rsi
0029C8AC  je       0x29c8bc  ; -> 0029C8BC
0029C8AE  mov      eax, dword ptr [rsi + 0x7c]
0029C8B1  and      al, 0xf
0029C8B3  cmp      al, 4
0029C8B5  sete     cl
0029C8B8  test     ecx, ecx
0029C8BA  jne      0x29c89c  ; -> 0029C89C
0029C8BC  mov      rcx, rsi
0029C8BF  call     0x244f00  ; -> 00244F00 fn
0029C8C4  xor      eax, eax
0029C8C6  mov      rsi, qword ptr [rsp + 0x50]
0029C8CB  add      rsp, 0x30
0029C8CF  pop      rdi
0029C8D0  ret      
0029C8D1  movsxd   rax, dword ptr [rdi + 0xb58]
0029C8D8  mov      r9d, 1
0029C8DE  movsx    edx, word ptr [rdi + 0x158]
0029C8E5  imul     rcx, rax, 0x160
0029C8EC  mov      rax, qword ptr [rdi + 0x298]
0029C8F3  mov      dword ptr [rsp + 0x20], 0xc8
0029C8FB  movsx    r8d, word ptr [rcx + rdi + 0x2da]
0029C904  movsx    ecx, word ptr [rax + 6]
0029C908  mov      rax, qword ptr [rdi + 0x118]
0029C90F  sub      r8d, ecx
0029C912  movsx    ecx, word ptr [rax + 6]
0029C916  add      r8d, ecx
0029C919  mov      rcx, rsi
0029C91C  call     0x2468a0  ; -> 002468A0 fn
0029C921  jmp      0x29c991  ; -> 0029C991
0029C923  xor      r9d, r9d
0029C926  mov      qword ptr [rsp + 0x48], rbx
0029C92B  lea      r8, [rip - 0x2e72]  ; -> 00299AC0
0029C932  mov      edx, 0xc0
0029C937  mov      rcx, rsi
0029C93A  call     0x245000  ; -> 00245000 fn
0029C93F  movsxd   rcx, dword ptr [rdi + 0xb58]
0029C946  mov      rbx, rax
0029C949  imul     rdx, rcx, 0x160
0029C950  mov      rcx, qword ptr [rdi + 0x298]
0029C957  movzx    r8d, word ptr [rdx + rdi + 0x2da]
0029C960  mov      rdx, rax
0029C963  sub      r8w, word ptr [rcx + 6]
0029C968  mov      rcx, qword ptr [rdi + 0x118]
0029C96F  add      r8w, word ptr [rcx + 6]
0029C974  mov      rcx, rdi
0029C977  mov      word ptr [rdi + 0x15a], r8w
0029C97F  call     0x244960  ; -> 00244960 fn
0029C984  mov      rcx, rbx
0029C987  call     0x246ac0  ; -> 00246AC0 fn
0029C98C  mov      rbx, qword ptr [rsp + 0x48]
0029C991  mov      edx, dword ptr [rdi + 0xb58]
0029C997  mov      rcx, rdi
0029C99A  call     0x29b120  ; -> 0029B120 fn
0029C99F  mov      rcx, rsi
0029C9A2  call     0x273a20  ; -> 00273A20 fn
0029C9A7  mov      rsi, qword ptr [rsp + 0x50]
0029C9AC  mov      ecx, 0xfffb
0029C9B1  and      word ptr [rdi + 0xb4a], cx
0029C9B8  mov      eax, 1
0029C9BD  or       word ptr [rdi + 0xb4a], 8
0029C9C5  add      rsp, 0x30
0029C9C9  pop      rdi
0029C9CA  ret      
```

## 0029D550 (1067 B, extent 0029D550-0029D97B)

Documented callee on this page: `002D8910`

```
0029D550  push     rdi
0029D552  push     r15
0029D554  sub      rsp, 0x48
0029D558  mov      eax, dword ptr [rdx]
0029D55A  mov      rdi, rcx
0029D55D  dec      eax
0029D55F  cmp      eax, 0x13
0029D562  ja       0x29d96c  ; -> 0029D96C
0029D568  lea      rcx, [rip - 0x17d56f]  ; -> 00120000 (image base)
0029D56F  cdqe     
0029D571  mov      r8d, dword ptr [rcx + rax*4 + 0x17d97c]  ; image base + 0x17d97c = 0029D97C
0029D579  add      r8, rcx
0029D57C  jmp      r8
0029D57F  mov      edx, dword ptr [rip + 0x1b6effb]  ; -> 01E0C580 [u32 0x00000014]
0029D585  mov      eax, dword ptr [rip + 0x1b6efdd]  ; -> 01E0C568 [u32 0x00000008]
0029D58B  lea      ecx, [rdx + rax*2]
0029D58E  test     rdi, rdi
0029D591  je       0x29d5b0  ; -> 0029D5B0
0029D593  xor      r15d, r15d
0029D596  mov      word ptr [rdi + 0x9e], cx
0029D59D  mov      eax, 0xb4
0029D5A2  mov      dword ptr [rdi + 0x98], r15d
0029D5A9  mov      word ptr [rdi + 0x9c], ax
0029D5B0  mov      byte ptr [rdi + 0xd2], 0
0029D5B7  lea      rdx, [rip + 0x678d9a]  ; -> 00916358
0029D5BE  mov      dword ptr [rdi + 0xc0], 0
0029D5C8  mov      rcx, rdi
0029D5CB  movss    xmm0, dword ptr [rip + 0x1b6efa1]  ; -> 01E0C574 [f32 1]
0029D5D3  movss    dword ptr [rdi + 0xc8], xmm0
0029D5DB  movss    xmm1, dword ptr [rip + 0x1b6ef95]  ; -> 01E0C578 [f32 0.88]
0029D5E3  mov      byte ptr [rdi + 0x140], 0
0029D5EA  and      dword ptr [rdi + 0x140], 0xfffffcff
0029D5F4  movss    dword ptr [rdi + 0xcc], xmm1
0029D5FC  call     0x247570  ; -> 00247570 fn
0029D601  mov      edx, 0x54
0029D606  mov      rcx, rdi
0029D609  call     0x247930  ; -> 00247930 fn
0029D60E  and      dword ptr [rdi + 0x40], 0xffffff7f
0029D615  xor      eax, eax
0029D617  add      rsp, 0x48
0029D61B  pop      r15
0029D61D  pop      rdi
0029D61E  ret      
0029D61F  mov      r8d, dword ptr [rdi + 0x140]
0029D626  bt       r8d, 9
0029D62B  jae      0x29d65f  ; -> 0029D65F
0029D62D  mov      rax, qword ptr [rip + 0x1dfee64]  ; -> 0209C498
0029D634  movzx    ecx, word ptr [rax + 0xcc]
0029D63B  mov      eax, 0x10624dd3
0029D640  imul     edx, ecx, 0x3c
0029D643  imul     edx
0029D645  sar      edx, 6
0029D648  mov      eax, edx
0029D64A  shr      eax, 0x1f
0029D64D  add      edx, eax
0029D64F  mov      eax, dword ptr [rdi + 0x13c]
0029D655  sub      eax, edx
0029D657  add      eax, dword ptr [rip + 0x1df1f13]  ; -> 0208F570
0029D65D  jmp      0x29d665  ; -> 0029D665
0029D65F  mov      eax, dword ptr [rip + 0x1df1f0b]  ; -> 0208F570
0029D665  btr      r8d, 9
0029D66A  mov      dword ptr [rdi + 0x138], eax
0029D670  bts      r8d, 8
0029D675  mov      dword ptr [rdi + 0x140], r8d
0029D67C  xor      eax, eax
0029D67E  add      rsp, 0x48
0029D682  pop      r15
0029D684  pop      rdi
0029D685  ret      
0029D686  mov      byte ptr [rdi + 0x140], 0x80
0029D68D  and      dword ptr [rdi + 0x140], 0xfffffeff
0029D697  xor      eax, eax
0029D699  add      rsp, 0x48
0029D69D  pop      r15
0029D69F  pop      rdi
0029D6A0  ret      
0029D6A1  mov      r8d, dword ptr [rdi + 0x140]
0029D6A8  bt       r8d, 8
0029D6AD  jae      0x29d6e1  ; -> 0029D6E1
0029D6AF  mov      rax, qword ptr [rip + 0x1dfede2]  ; -> 0209C498
0029D6B6  movzx    ecx, word ptr [rax + 0xce]
0029D6BD  mov      eax, 0x10624dd3
0029D6C2  imul     edx, ecx, 0x3c
0029D6C5  imul     edx
0029D6C7  sar      edx, 6
0029D6CA  mov      eax, edx
0029D6CC  shr      eax, 0x1f
0029D6CF  add      edx, eax
0029D6D1  mov      eax, dword ptr [rdi + 0x13c]
0029D6D7  sub      eax, edx
0029D6D9  add      eax, dword ptr [rip + 0x1df1e91]  ; -> 0208F570
0029D6DF  jmp      0x29d6e7  ; -> 0029D6E7
0029D6E1  mov      eax, dword ptr [rip + 0x1df1e89]  ; -> 0208F570
0029D6E7  btr      r8d, 8
0029D6EC  mov      dword ptr [rdi + 0x138], eax
0029D6F2  bts      r8d, 9
0029D6F7  mov      dword ptr [rdi + 0x140], r8d
0029D6FE  xor      eax, eax
0029D700  add      rsp, 0x48
0029D704  pop      r15
0029D706  pop      rdi
0029D707  ret      
0029D708  mov      byte ptr [rdi + 0x140], 0
0029D70F  and      dword ptr [rdi + 0x140], 0xfffffdff
0029D719  xor      eax, eax
0029D71B  add      rsp, 0x48
0029D71F  pop      r15
0029D721  pop      rdi
0029D722  ret      
0029D723  mov      ecx, dword ptr [rdi + 0x7c]
0029D726  mov      eax, ecx
0029D728  and      eax, 0xfffffff0
0029D72B  shl      eax, 0x1a
0029D72E  test     eax, eax
0029D730  jle      0x29d76b  ; -> 0029D76B
0029D732  mov      r8d, dword ptr [rip + 0x1df1e37]  ; -> 0208F570
0029D739  mov      rax, qword ptr [rip + 0x1dfed58]  ; -> 0209C498
0029D740  sub      r8d, dword ptr [rdi + 0x138]
0029D747  mov      dword ptr [rdi + 0x13c], r8d
0029D74E  movzx    ecx, word ptr [rax + 0xcc]
0029D755  mov      eax, 0x10624dd3
0029D75A  imul     edx, ecx, 0x3c
0029D75D  imul     edx
0029D75F  sar      edx, 6
0029D762  mov      eax, edx
0029D764  shr      eax, 0x1f
0029D767  add      edx, eax
0029D769  jmp      0x29d7b1  ; -> 0029D7B1
0029D76B  test     cl, 0x20
0029D76E  je       0x29d962  ; -> 0029D962
0029D774  mov      r9d, dword ptr [rip + 0x1df1df5]  ; -> 0208F570
0029D77B  mov      rax, qword ptr [rip + 0x1dfed16]  ; -> 0209C498
0029D782  sub      r9d, dword ptr [rdi + 0x138]
0029D789  mov      dword ptr [rdi + 0x13c], r9d
0029D790  movzx    ecx, word ptr [rax + 0xce]
0029D797  mov      eax, 0x10624dd3
0029D79C  imul     edx, ecx, 0x3c
0029D79F  imul     edx
0029D7A1  sar      edx, 6
0029D7A4  mov      eax, edx
0029D7A6  shr      eax, 0x1f
0029D7A9  add      edx, eax
0029D7AB  mov      r8d, edx
0029D7AE  sub      r8d, r9d
0029D7B1  mov      ecx, 1
0029D7B6  call     0x248f40  ; -> 00248F40 fn
0029D7BB  mulss    xmm0, dword ptr [rip + 0x656269]  ; -> 008F3A2C [f32 128]
0029D7C3  cvttss2si rax, xmm0
0029D7C8  mov      byte ptr [rdi + 0x140], al
0029D7CE  xor      eax, eax
0029D7D0  add      rsp, 0x48
0029D7D4  pop      r15
0029D7D6  pop      rdi
0029D7D7  ret      
0029D7D8  mov      rax, qword ptr [rip + 0x1dfecb9]  ; -> 0209C498
0029D7DF  mov      qword ptr [rsp + 0x38], r13
0029D7E4  mov      r13, qword ptr [rdi + 0x38]
0029D7E8  test     byte ptr [rax + 0xc8], 1
0029D7EF  jne      0x29d95d  ; -> 0029D95D
0029D7F5  movzx    r9d, byte ptr [rdi + 0xd2]
0029D7FD  test     r9b, r9b
0029D800  je       0x29d95d  ; -> 0029D95D
0029D806  mov      r8d, dword ptr [rip + 0x1b6ed73]  ; -> 01E0C580 [u32 0x00000014]
0029D80D  movsx    eax, r8w
0029D811  mov      qword ptr [rsp + 0x68], rbp
0029D816  mov      qword ptr [rsp + 0x70], rsi
0029D81B  movzx    esi, word ptr [rdi + 0x9e]
0029D822  movzx    ecx, r9b
0029D826  dec      cx
0029D829  mov      qword ptr [rsp + 0x40], r12
0029D82E  movzx    r12d, word ptr [rip + 0x1b6ed2e]  ; -> 01E0C564 [u16 0x0010]
0029D836  movsx    edx, cx
0029D839  imul     edx, eax
0029D83C  movzx    eax, byte ptr [rdi + 0xc2]
0029D843  sub      si, dx
0029D846  movzx    edx, r9b
0029D84A  sub      si, ax
0029D84D  sub      si, word ptr [rip + 0x1b6ed14]  ; -> 01E0C568 [u16 0x0008]
0029D854  test     r9b, r9b
0029D857  je       0x29d875  ; -> 0029D875
0029D859  lea      rax, [rdi + 0xe8]
0029D860  mov      ecx, edx
0029D862  test     byte ptr [rax], 4
0029D865  je       0x29d86b  ; -> 0029D86B
0029D867  add      si, r8w
0029D86B  add      rax, 0x18
0029D86F  sub      rcx, 1
0029D873  jne      0x29d862  ; -> 0029D862
0029D875  xor      r15d, r15d
0029D878  mov      ebp, r15d
0029D87B  test     r9b, r9b
0029D87E  je       0x29d940  ; -> 0029D940
0029D884  mov      qword ptr [rsp + 0x30], r14
0029D889  mov      ecx, 0x4000
0029D88E  lea      r14, [rdi + 0xe8]
0029D895  mov      qword ptr [rsp + 0x60], rbx
0029D89A  nop      word ptr [rax + rax]
0029D8A0  movzx    eax, word ptr [r14]
0029D8A4  test     al, 4
0029D8A6  jne      0x29d921  ; -> 0029D921
0029D8A8  test     cx, ax
0029D8AB  jne      0x29d91d  ; -> 0029D91D
0029D8AD  mov      r8, r13
0029D8B0  lea      rdx, [r14 - 0x10]
0029D8B4  mov      rcx, rdi
0029D8B7  call     0x29d9d0  ; -> 0029D9D0 fn
0029D8BC  mov      ecx, 0x467c
0029D8C1  call     0x2f9860  ; -> 002F9860 fn
0029D8C6  mov      rdx, qword ptr [rip + 0x1dfebcb]  ; -> 0209C498
0029D8CD  mov      r8, rax
0029D8D0  mov      rax, qword ptr [r14 - 8]
0029D8D4  add      rdx, 0xd8
0029D8DB  mov      r9, qword ptr [r14 - 0x10]
0029D8DF  mov      ecx, 0x80
0029D8E4  mov      qword ptr [rsp + 0x20], rax
0029D8E9  call     0x2b4090  ; -> 002B4090 fn
0029D8EE  mov      r9, qword ptr [rip + 0x1dfeba3]  ; -> 0209C498
0029D8F5  mov      rcx, r13
0029D8F8  add      r9, 0xd8
0029D8FF  movsx    r8d, si
0029D903  movsx    edx, r12w
0029D907  mov      qword ptr [rsp + 0x20], r15
0029D90C  call     0x2d8910  ; -> 002D8910 fn
0029D911  mov      r8d, dword ptr [rip + 0x1b6ec68]  ; -> 01E0C580 [u32 0x00000014]
0029D918  mov      ecx, 0x4000
0029D91D  add      si, r8w
0029D921  movzx    eax, byte ptr [rdi + 0xd2]
0029D928  inc      ebp
0029D92A  add      r14, 0x18
0029D92E  cmp      ebp, eax
0029D930  jl       0x29d8a0  ; -> 0029D8A0
0029D936  mov      r14, qword ptr [rsp + 0x30]
0029D93B  mov      rbx, qword ptr [rsp + 0x60]
0029D940  xor      ecx, ecx
0029D942  call     0x2dd7e0  ; -> 002DD7E0 fn
0029D947  mov      r12, qword ptr [rsp + 0x40]
0029D94C  mov      rsi, qword ptr [rsp + 0x70]
0029D951  mov      rbp, qword ptr [rsp + 0x68]
0029D956  mov      dword ptr [r13 + 0x90], eax
0029D95D  mov      r13, qword ptr [rsp + 0x38]
0029D962  xor      eax, eax
0029D964  add      rsp, 0x48
0029D968  pop      r15
0029D96A  pop      rdi
0029D96B  ret      
0029D96C  mov      rcx, rdi
0029D96F  add      rsp, 0x48
0029D973  pop      r15
0029D975  pop      rdi
0029D976  jmp      0x5c5230  ; -> 005C5230 fn
```

## 0029D9D0 (151 B, extent 0029D9D0-0029DA67)

Documented callee on this page: `002DD7E0`

```
0029D9D0  mov      qword ptr [rsp + 8], rbx
0029D9D5  mov      qword ptr [rsp + 0x10], rsi
0029D9DA  push     rdi
0029D9DB  sub      rsp, 0x20
0029D9DF  movzx    eax, word ptr [rdx + 0x10]
0029D9E3  mov      rbx, r8
0029D9E6  mov      rdi, rdx
0029D9E9  mov      rsi, rcx
0029D9EC  test     al, 1
0029D9EE  je       0x29d9f7  ; -> 0029D9F7
0029D9F0  mov      ecx, 3
0029D9F5  jmp      0x29da0f  ; -> 0029DA0F
0029D9F7  test     al, 2
0029D9F9  je       0x29da02  ; -> 0029DA02
0029D9FB  mov      ecx, 7
0029DA00  jmp      0x29da0f  ; -> 0029DA0F
0029DA02  test     al, 8
0029DA04  je       0x29da0d  ; -> 0029DA0D
0029DA06  mov      ecx, 0x106
0029DA0B  jmp      0x29da0f  ; -> 0029DA0F
0029DA0D  xor      ecx, ecx
0029DA0F  call     0x2dd7e0  ; -> 002DD7E0 fn
0029DA14  mov      dword ptr [rbx + 0x90], eax
0029DA1A  cmp      word ptr [rdi + 0x10], 0
0029DA1F  movzx    eax, byte ptr [rbx + 0x93]
0029DA26  jge      0x29da44  ; -> 0029DA44
0029DA28  shl      eax, 7
0029DA2B  sar      eax, 7
0029DA2E  mov      byte ptr [rbx + 0x93], al
0029DA34  mov      rbx, qword ptr [rsp + 0x30]
0029DA39  mov      rsi, qword ptr [rsp + 0x38]
0029DA3E  add      rsp, 0x20
0029DA42  pop      rdi
0029DA43  ret      
0029DA44  movzx    ecx, byte ptr [rsi + 0x140]
0029DA4B  mov      rsi, qword ptr [rsp + 0x38]
0029DA50  imul     ecx, eax
0029DA53  shr      ecx, 7
0029DA56  mov      byte ptr [rbx + 0x93], cl
0029DA5C  mov      rbx, qword ptr [rsp + 0x30]
0029DA61  add      rsp, 0x20
0029DA65  pop      rdi
0029DA66  ret      
```

## 0029E7D0 (110 B, extent 0029E7D0-0029E83E)

Documented callee on this page: `002432B0`

```
0029E7D0  push     rbx
0029E7D2  sub      rsp, 0x20
0029E7D6  cmp      dword ptr [rdx], 1
0029E7D9  mov      rbx, rcx
0029E7DC  je       0x29e7e8  ; -> 0029E7E8
0029E7DE  add      rsp, 0x20
0029E7E2  pop      rbx
0029E7E3  jmp      0x5c5230  ; -> 005C5230 fn
0029E7E8  mov      r8d, dword ptr [rdx + 0x10]
0029E7EC  add      rcx, 0x50
0029E7F0  mov      rdx, qword ptr [rdx + 8]
0029E7F4  mov      r9, rbx
0029E7F7  call     0x2432b0  ; -> 002432B0 fn
0029E7FC  movzx    ecx, word ptr [rax + 0xa]
0029E800  movzx    edx, word ptr [rax + 8]
0029E804  movsx    r8d, word ptr [rax + 6]
0029E809  test     rbx, rbx
0029E80C  je       0x29e82f  ; -> 0029E82F
0029E80E  movzx    eax, word ptr [rax + 4]
0029E812  mov      word ptr [rbx + 0x98], ax
0029E819  mov      word ptr [rbx + 0x9a], r8w
0029E821  mov      word ptr [rbx + 0x9c], dx
0029E828  mov      word ptr [rbx + 0x9e], cx
0029E82F  or       dword ptr [rbx + 0x40], 0x40000
0029E836  xor      eax, eax
0029E838  add      rsp, 0x20
0029E83C  pop      rbx
0029E83D  ret      
```

## 002B6CE0 (202 B, extent 002B6CE0-002B6DAA)

Documented callee on this page: `002432B0`

```
002B6CE0  push     rbx
002B6CE2  sub      rsp, 0x20
002B6CE6  mov      rbx, rcx
002B6CE9  mov      ecx, dword ptr [rdx]
002B6CEB  sub      ecx, 1
002B6CEE  je       0x2b6d11  ; -> 002B6D11
002B6CF0  cmp      ecx, 0xe
002B6CF3  je       0x2b6d02  ; -> 002B6D02
002B6CF5  mov      rcx, rbx
002B6CF8  add      rsp, 0x20
002B6CFC  pop      rbx
002B6CFD  jmp      0x5c5230  ; -> 005C5230 fn
002B6D02  or       dword ptr [rbx + 0xc0], 1
002B6D09  xor      eax, eax
002B6D0B  add      rsp, 0x20
002B6D0F  pop      rbx
002B6D10  ret      
002B6D11  mov      rdx, qword ptr [rdx + 8]
002B6D15  lea      rcx, [rbx + 0x50]
002B6D19  mov      r9, rbx
002B6D1C  mov      r8d, 3
002B6D22  call     0x2432b0  ; -> 002432B0 fn
002B6D27  movzx    ecx, word ptr [rax + 0xa]
002B6D2B  movzx    edx, word ptr [rax + 8]
002B6D2F  movsx    r8d, word ptr [rax + 6]
002B6D34  test     rbx, rbx
002B6D37  je       0x2b6d64  ; -> 002B6D64
002B6D39  movzx    eax, word ptr [rax + 4]
002B6D3D  mov      word ptr [rbx + 0x98], ax
002B6D44  mov      rax, qword ptr [rbx + 0x60]
002B6D48  mov      word ptr [rbx + 0x9a], r8w
002B6D50  mov      word ptr [rbx + 0x9c], dx
002B6D57  mov      word ptr [rbx + 0x9e], cx
002B6D5E  mov      rax, qword ptr [rax + 0x10]
002B6D62  jmp      0x2b6d66  ; -> 002B6D66
002B6D64  xor      eax, eax
002B6D66  mov      rax, qword ptr [rax + 0x18]
002B6D6A  lea      rcx, [rip - 0xf1]  ; -> 002B6C80
002B6D71  lea      rdx, [rip + 0x65fad8]  ; -> 00916850
002B6D78  mov      qword ptr [rax + 0x120], rcx
002B6D7F  mov      rcx, rbx
002B6D82  mov      qword ptr [rax + 0xd8], rbx
002B6D89  mov      qword ptr [rax + 0xc8], rbx
002B6D90  call     0x247570  ; -> 00247570 fn
002B6D95  mov      edx, 0x62
002B6D9A  mov      rcx, rbx
002B6D9D  call     0x247930  ; -> 00247930 fn
002B6DA2  xor      eax, eax
002B6DA4  add      rsp, 0x20
002B6DA8  pop      rbx
002B6DA9  ret      
```

## 002BC310 (202 B, extent 002BC310-002BC3DA)

Documented callee on this page: `002432B0`

```
002BC310  push     rbx
002BC312  sub      rsp, 0x20
002BC316  mov      rbx, rcx
002BC319  mov      ecx, dword ptr [rdx]
002BC31B  sub      ecx, 1
002BC31E  je       0x2bc341  ; -> 002BC341
002BC320  cmp      ecx, 0xe
002BC323  je       0x2bc332  ; -> 002BC332
002BC325  mov      rcx, rbx
002BC328  add      rsp, 0x20
002BC32C  pop      rbx
002BC32D  jmp      0x5c5230  ; -> 005C5230 fn
002BC332  or       dword ptr [rbx + 0xc0], 1
002BC339  xor      eax, eax
002BC33B  add      rsp, 0x20
002BC33F  pop      rbx
002BC340  ret      
002BC341  mov      rdx, qword ptr [rdx + 8]
002BC345  lea      rcx, [rbx + 0x50]
002BC349  mov      r9, rbx
002BC34C  mov      r8d, 3
002BC352  call     0x2432b0  ; -> 002432B0 fn
002BC357  movzx    ecx, word ptr [rax + 0xa]
002BC35B  movzx    edx, word ptr [rax + 8]
002BC35F  movsx    r8d, word ptr [rax + 6]
002BC364  test     rbx, rbx
002BC367  je       0x2bc394  ; -> 002BC394
002BC369  movzx    eax, word ptr [rax + 4]
002BC36D  mov      word ptr [rbx + 0x98], ax
002BC374  mov      rax, qword ptr [rbx + 0x60]
002BC378  mov      word ptr [rbx + 0x9a], r8w
002BC380  mov      word ptr [rbx + 0x9c], dx
002BC387  mov      word ptr [rbx + 0x9e], cx
002BC38E  mov      rax, qword ptr [rax + 0x10]
002BC392  jmp      0x2bc396  ; -> 002BC396
002BC394  xor      eax, eax
002BC396  mov      rax, qword ptr [rax + 0x18]
002BC39A  lea      rcx, [rip - 0x1d51]  ; -> 002BA650
002BC3A1  lea      rdx, [rip + 0x65a6a0]  ; -> 00916A48
002BC3A8  mov      qword ptr [rax + 0x120], rcx
002BC3AF  mov      rcx, rbx
002BC3B2  mov      qword ptr [rax + 0xd8], rbx
002BC3B9  mov      qword ptr [rax + 0xc8], rbx
002BC3C0  call     0x247570  ; -> 00247570 fn
002BC3C5  mov      edx, 0x62
002BC3CA  mov      rcx, rbx
002BC3CD  call     0x247930  ; -> 00247930 fn
002BC3D2  xor      eax, eax
002BC3D4  add      rsp, 0x20
002BC3D8  pop      rbx
002BC3D9  ret      
```

## 002BD680 (502 B, extent 002BD680-002BD876)

Documented callee on this page: `002D3900`

```
002BD680  push     rbx
002BD682  sub      rsp, 0x40
002BD686  mov      rax, qword ptr [rip + 0x1c871a3]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002BD68D  xor      rax, rsp
002BD690  mov      qword ptr [rsp + 0x38], rax
002BD695  mov      rbx, rcx
002BD698  mov      r8, rdx
002BD69B  mov      ecx, dword ptr [rdx]
002BD69D  lea      eax, [rcx - 1]
002BD6A0  cmp      eax, 0xe
002BD6A3  ja       0x2bd858  ; -> 002BD858
002BD6A9  lea      r9, [rip - 0x19d6b0]  ; -> 00120000 (image base)
002BD6B0  cdqe     
002BD6B2  mov      edx, dword ptr [r9 + rax*4 + 0x19d878]  ; image base + 0x19d878 = 002BD878
002BD6BA  add      rdx, r9
002BD6BD  jmp      rdx
002BD6BF  lea      rdx, [rip + 0x659512]  ; -> 00916BD8
002BD6C6  mov      rcx, rbx
002BD6C9  call     0x247570  ; -> 00247570 fn
002BD6CE  mov      edx, 0x62
002BD6D3  mov      rcx, rbx
002BD6D6  call     0x247930  ; -> 00247930 fn
002BD6DB  xor      ecx, ecx
002BD6DD  call     0x29e6d0  ; -> 0029E6D0 fn
002BD6E2  xor      eax, eax
002BD6E4  mov      rcx, qword ptr [rsp + 0x38]
002BD6E9  xor      rcx, rsp
002BD6EC  call     0x808c40  ; -> 00808C40 fn
002BD6F1  add      rsp, 0x40
002BD6F5  pop      rbx
002BD6F6  ret      
002BD6F7  mov      rcx, rbx
002BD6FA  call     0x2470d0  ; -> 002470D0 fn
002BD6FF  xor      eax, eax
002BD701  mov      rcx, qword ptr [rsp + 0x38]
002BD706  xor      rcx, rsp
002BD709  call     0x808c40  ; -> 00808C40 fn
002BD70E  add      rsp, 0x40
002BD712  pop      rbx
002BD713  ret      
002BD714  test     rbx, rbx
002BD717  jne      0x2bd739  ; -> 002BD739
002BD719  xor      eax, eax
002BD71B  mov      rcx, qword ptr [rax + 0x18]
002BD71F  call     0x2d3900  ; -> 002D3900 fn
002BD724  xor      eax, eax
002BD726  mov      rcx, qword ptr [rsp + 0x38]
002BD72B  xor      rcx, rsp
002BD72E  call     0x808c40  ; -> 00808C40 fn
002BD733  add      rsp, 0x40
002BD737  pop      rbx
002BD738  ret      
002BD739  mov      rax, qword ptr [rbx + 0x60]
002BD73D  mov      rax, qword ptr [rax + 0x10]
002BD741  mov      rcx, qword ptr [rax + 0x18]
002BD745  call     0x2d3900  ; -> 002D3900 fn
002BD74A  xor      eax, eax
002BD74C  mov      rcx, qword ptr [rsp + 0x38]
002BD751  xor      rcx, rsp
002BD754  call     0x808c40  ; -> 00808C40 fn
002BD759  add      rsp, 0x40
002BD75D  pop      rbx
002BD75E  ret      
002BD75F  cmp      word ptr [rbx + 0x3da], 0
002BD767  jne      0x2bd843  ; -> 002BD843
002BD76D  mov      dword ptr [rsp + 0x20], 0x27
002BD775  xorps    xmm0, xmm0
002BD778  movdqu   xmmword ptr [rsp + 0x28], xmm0
002BD77E  mov      rcx, qword ptr [rbx + 0x3c0]
002BD785  test     rcx, rcx
002BD788  je       0x2bd843  ; -> 002BD843
002BD78E  mov      rax, qword ptr [rcx]
002BD791  test     rax, rax
002BD794  je       0x2bd843  ; -> 002BD843
002BD79A  lea      rdx, [rsp + 0x20]
002BD79F  call     rax
002BD7A1  xor      eax, eax
002BD7A3  mov      rcx, qword ptr [rsp + 0x38]
002BD7A8  xor      rcx, rsp
002BD7AB  call     0x808c40  ; -> 00808C40 fn
002BD7B0  add      rsp, 0x40
002BD7B4  pop      rbx
002BD7B5  ret      
002BD7B6  mov      rax, qword ptr [r8 + 8]
002BD7BA  sub      rax, 0x8000
002BD7C0  je       0x2bd7e5  ; -> 002BD7E5
002BD7C2  cmp      rax, 2
002BD7C6  jne      0x2bd843  ; -> 002BD843
002BD7C8  mov      rcx, rbx
002BD7CB  call     0x244f00  ; -> 00244F00 fn
002BD7D0  xor      eax, eax
002BD7D2  mov      rcx, qword ptr [rsp + 0x38]
002BD7D7  xor      rcx, rsp
002BD7DA  call     0x808c40  ; -> 00808C40 fn
002BD7DF  add      rsp, 0x40
002BD7E3  pop      rbx
002BD7E4  ret      
002BD7E5  mov      rax, qword ptr [r8 + 0x10]
002BD7E9  mov      dword ptr [rsp + 0x20], 0x25
002BD7F1  lea      rcx, [rax + rax*2]
002BD7F5  movsx    rax, word ptr [rbx + rcx*8 + 0xc8]
002BD7FE  mov      qword ptr [rsp + 0x28], rax
002BD803  movsx    rax, word ptr [rbx + rcx*8 + 0xca]
002BD80C  mov      qword ptr [rsp + 0x30], rax
002BD811  jmp      0x2bd77e  ; -> 002BD77E
002BD816  mov      ecx, 1
002BD81B  mov      word ptr [rbx + 0x3da], cx
002BD822  call     0x29e6d0  ; -> 0029E6D0 fn
002BD827  mov      dword ptr [rsp + 0x20], 0x26
002BD82F  jmp      0x2bd775  ; -> 002BD775
002BD834  xor      eax, eax
002BD836  cmp      ecx, 8
002BD839  sete     al
002BD83C  mov      ecx, eax
002BD83E  call     0x27fb50  ; -> 0027FB50 fn
002BD843  xor      eax, eax
002BD845  mov      rcx, qword ptr [rsp + 0x38]
002BD84A  xor      rcx, rsp
002BD84D  call     0x808c40  ; -> 00808C40 fn
002BD852  add      rsp, 0x40
002BD856  pop      rbx
002BD857  ret      
002BD858  mov      rdx, r8
002BD85B  mov      rcx, rbx
002BD85E  call     0x5c5230  ; -> 005C5230 fn
002BD863  mov      rcx, qword ptr [rsp + 0x38]
002BD868  xor      rcx, rsp
002BD86B  call     0x808c40  ; -> 00808C40 fn
002BD870  add      rsp, 0x40
002BD874  pop      rbx
002BD875  ret      
```

## 002C34F0 (97 B, extent 002C34F0-002C3551)

Documented callee on this page: `002DD7E0`

```
002C34F0  mov      qword ptr [rsp + 8], rbx
002C34F5  push     rdi
002C34F6  sub      rsp, 0x20
002C34FA  mov      rax, qword ptr [rdx + 0x10]
002C34FE  movsxd   rbx, r9d
002C3501  shl      rbx, 5
002C3505  add      rbx, rcx
002C3508  mov      rdi, qword ptr [rax]
002C350B  mov      rax, qword ptr [rdi]
002C350E  movzx    ecx, word ptr [rax + 4]
002C3512  mov      word ptr [rdi + 0xc], cx
002C3516  xor      ecx, ecx
002C3518  mov      rax, qword ptr [rbx]
002C351B  mov      qword ptr [rdi + 0x18], rax
002C351F  call     0x20e620  ; -> 0020E620 fn
002C3524  mov      dword ptr [rdi + 0x20], eax
002C3527  test     dword ptr [rbx + 0x18], 0x20000
002C352E  jne      0x2c3537  ; -> 002C3537
002C3530  mov      ecx, 2
002C3535  jmp      0x2c3539  ; -> 002C3539
002C3537  xor      ecx, ecx
002C3539  call     0x2dd7e0  ; -> 002DD7E0 fn
002C353E  mov      rbx, qword ptr [rsp + 0x30]
002C3543  mov      dword ptr [rdi + 0x24], eax
002C3546  mov      eax, 1
002C354B  add      rsp, 0x20
002C354F  pop      rdi
002C3550  ret      
```

## 002C4400 (86 B, extent 002C4400-002C4456)

Documented callee on this page: `002DD7E0`

```
002C4400  mov      qword ptr [rsp + 8], rbx
002C4405  push     rdi
002C4406  sub      rsp, 0x20
002C440A  mov      rax, qword ptr [rdx + 0x10]
002C440E  movsxd   rbx, r9d
002C4411  shl      rbx, 5
002C4415  add      rbx, rcx
002C4418  xor      ecx, ecx
002C441A  mov      rdi, qword ptr [rax]
002C441D  mov      rax, qword ptr [rbx]
002C4420  mov      qword ptr [rdi + 0x18], rax
002C4424  call     0x20e620  ; -> 0020E620 fn
002C4429  mov      dword ptr [rdi + 0x20], eax
002C442C  test     dword ptr [rbx + 0x18], 0x20000
002C4433  jne      0x2c443c  ; -> 002C443C
002C4435  mov      ecx, 2
002C443A  jmp      0x2c443e  ; -> 002C443E
002C443C  xor      ecx, ecx
002C443E  call     0x2dd7e0  ; -> 002DD7E0 fn
002C4443  mov      rbx, qword ptr [rsp + 0x30]
002C4448  mov      dword ptr [rdi + 0x24], eax
002C444B  mov      eax, 1
002C4450  add      rsp, 0x20
002C4454  pop      rdi
002C4455  ret      
```

## 002CA2E0 (202 B, extent 002CA2E0-002CA3AA)

Documented callee on this page: `00248F40`

```
002CA2E0  push     rbx
002CA2E2  sub      rsp, 0x20
002CA2E6  test     byte ptr [rcx + 0xc0], 3
002CA2ED  mov      rbx, rcx
002CA2F0  je       0x2ca3a4  ; -> 002CA3A4
002CA2F6  movsx    rdx, word ptr [rcx + 0xc6]
002CA2FE  mov      rax, qword ptr [rcx + 0x60]
002CA302  mov      r8d, dword ptr [rip + 0x1dc5267]  ; -> 0208F570
002CA309  sub      r8d, dword ptr [rcx + 0xd0]
002CA310  mov      ecx, dword ptr [rcx + 0xc0]
002CA316  shr      ecx, 2
002CA319  mov      qword ptr [rsp + 0x30], rdi
002CA31E  and      ecx, 0xf
002CA321  mov      rdi, qword ptr [rax + rdx*8]
002CA325  mov      edx, dword ptr [rbx + 0xcc]
002CA32B  call     0x248f40  ; -> 00248F40 fn
002CA330  ucomiss  xmm0, dword ptr [rip + 0x1a21871]  ; -> 01CEBBA8 [f32 1]
002CA337  jp       0x2ca354  ; -> 002CA354
002CA339  jne      0x2ca354  ; -> 002CA354
002CA33B  movzx    eax, byte ptr [rbx + 0xc8]
002CA342  add      al, byte ptr [rbx + 0xc4]
002CA348  mov      byte ptr [rdi + 0x3b], al
002CA34B  and      dword ptr [rbx + 0xc0], 0xfffffffc
002CA352  jmp      0x2ca37f  ; -> 002CA37F
002CA354  movsx    eax, word ptr [rbx + 0xc8]
002CA35B  movd     xmm1, eax
002CA35F  movsx    eax, word ptr [rbx + 0xc4]
002CA366  cvtdq2ps xmm1, xmm1
002CA369  mulss    xmm1, xmm0
002CA36D  movd     xmm0, eax
002CA371  cvtdq2ps xmm0, xmm0
002CA374  addss    xmm1, xmm0
002CA378  cvttss2si eax, xmm1
002CA37C  mov      byte ptr [rdi + 0x3b], al
002CA37F  movzx    eax, byte ptr [rdi + 0x3b]
002CA383  mov      ecx, eax
002CA385  shl      ecx, 8
002CA388  or       ecx, eax
002CA38A  shl      ecx, 8
002CA38D  or       ecx, eax
002CA38F  bts      ecx, 0x1f
002CA393  mov      dword ptr [rdi + 0x34], ecx
002CA396  mov      dword ptr [rdi + 0x30], ecx
002CA399  mov      dword ptr [rdi + 0x2c], ecx
002CA39C  mov      dword ptr [rdi + 0x28], ecx
002CA39F  mov      rdi, qword ptr [rsp + 0x30]
002CA3A4  add      rsp, 0x20
002CA3A8  pop      rbx
002CA3A9  ret      
```

## 002CA430 (89 B, extent 002CA430-002CA489)

Documented callee on this page: `0035D330`

```
002CA430  sub      rsp, 0x28
002CA434  shl      ecx, 0x10
002CA437  mov      edx, ecx
002CA439  mov      ecx, 1
002CA43E  call     0x35d330  ; -> 0035D330 fn
002CA443  mov      edx, dword ptr [rax + 0x38]
002CA446  sub      edx, 7
002CA449  je       0x2ca47f  ; -> 002CA47F
002CA44B  sub      edx, 1
002CA44E  je       0x2ca475  ; -> 002CA475
002CA450  sub      edx, 1
002CA453  je       0x2ca46b  ; -> 002CA46B
002CA455  cmp      edx, 8
002CA458  je       0x2ca461  ; -> 002CA461
002CA45A  xor      eax, eax
002CA45C  add      rsp, 0x28
002CA460  ret      
002CA461  mov      eax, 0x1a
002CA466  add      rsp, 0x28
002CA46A  ret      
002CA46B  mov      eax, 0x19
002CA470  add      rsp, 0x28
002CA474  ret      
002CA475  mov      eax, 0x18
002CA47A  add      rsp, 0x28
002CA47E  ret      
002CA47F  mov      eax, 0x17
002CA484  add      rsp, 0x28
002CA488  ret      
```
