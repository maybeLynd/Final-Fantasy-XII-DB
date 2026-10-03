# F homing pack (FABLE): `22-Middleware-PhyreEngine/Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 9. No bearing page cites them and no documented function calls them directly.

## 005A9DF0 (97 B, extent 005A9DF0-005A9E51)

Documented callee on this page: `006803D0`

```
005A9DF0  push     rdi
005A9DF2  sub      rsp, 0x30
005A9DF6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005A9DFF  mov      qword ptr [rsp + 0x40], rbx
005A9E04  mov      rdi, rcx
005A9E07  mov      rdx, qword ptr [rdi + 0x18]
005A9E0B  cmp      rdx, rdi
005A9E0E  je       0x5a9e20  ; -> 005A9E20
005A9E10  test     rdx, rdx
005A9E13  je       0x5a9e20  ; -> 005A9E20
005A9E15  mov      rcx, rdi
005A9E18  call     0x67fe20  ; -> 0067FE20 fn
005A9E1D  nop      
005A9E1E  jmp      0x5a9e07  ; -> 005A9E07
005A9E20  lea      rcx, [rdi + 0x30]
005A9E24  call     0x6803d0  ; -> 006803D0 fn
005A9E29  nop      
005A9E2A  lea      rcx, [rdi + 0x30]
005A9E2E  call     0x680030  ; -> 00680030 fn
005A9E33  nop      
005A9E34  mov      rcx, rdi
005A9E37  call     0x67f580  ; -> 0067F580 fn
005A9E3C  nop      
005A9E3D  mov      rcx, rdi
005A9E40  call     0x67f580  ; -> 0067F580 fn
005A9E45  nop      
005A9E46  mov      rbx, qword ptr [rsp + 0x40]
005A9E4B  add      rsp, 0x30
005A9E4F  pop      rdi
005A9E50  ret      
```

## 005CC050 (152 B, extent 005CC050-005CC0E8)

Documented callee on this page: `005A6670`

```
005CC050  mov      qword ptr [rsp + 0x18], rbx
005CC055  push     rdi
005CC056  sub      rsp, 0x20
005CC05A  mov      rbx, r9
005CC05D  mov      r9, rdx
005CC060  mov      rdi, r8
005CC063  mov      r11, rcx
005CC066  test     rdx, rdx
005CC069  je       0x5cc0db  ; -> 005CC0DB
005CC06B  mov      r10, qword ptr [rsp + 0x50]
005CC070  mov      qword ptr [rsp + 0x30], rsi
005CC075  add      qword ptr [r10], 8
005CC079  mov      rax, qword ptr [r10]
005CC07C  mov      edx, dword ptr [rax - 8]
005CC07F  add      rax, 8
005CC083  mov      qword ptr [r10], rax
005CC086  mov      r8, qword ptr [rax - 8]
005CC08A  movsxd   rax, dword ptr [rcx + 0x10]
005CC08E  lea      rcx, [r9 - 8]
005CC092  add      rcx, rax
005CC095  call     qword ptr [r11 + 8]
005CC099  mov      esi, eax
005CC09B  test     rbx, rbx
005CC09E  je       0x5cc0c9  ; -> 005CC0C9
005CC0A0  call     0x5a6670  ; -> 005A6670 fn
005CC0A5  cmp      rdi, rax
005CC0A8  jne      0x5cc0c9  ; -> 005CC0C9
005CC0AA  mov      dword ptr [rbx + 8], esi
005CC0AD  mov      eax, 1
005CC0B2  mov      rsi, qword ptr [rsp + 0x30]
005CC0B7  mov      qword ptr [rbx], 0
005CC0BE  mov      rbx, qword ptr [rsp + 0x40]
005CC0C3  add      rsp, 0x20
005CC0C7  pop      rdi
005CC0C8  ret      
005CC0C9  xor      eax, eax
005CC0CB  mov      rsi, qword ptr [rsp + 0x30]
005CC0D0  mov      rbx, qword ptr [rsp + 0x40]
005CC0D5  add      rsp, 0x20
005CC0D9  pop      rdi
005CC0DA  ret      
005CC0DB  xor      eax, eax
005CC0DD  mov      rbx, qword ptr [rsp + 0x40]
005CC0E2  add      rsp, 0x20
005CC0E6  pop      rdi
005CC0E7  ret      
```

## 005CC0F0 (142 B, extent 005CC0F0-005CC17E)

Documented callee on this page: `005A6670`

```
005CC0F0  mov      qword ptr [rsp + 0x18], rbx
005CC0F5  push     rdi
005CC0F6  sub      rsp, 0x20
005CC0FA  mov      rbx, r9
005CC0FD  mov      rdi, r8
005CC100  mov      r9, rdx
005CC103  mov      r8, rcx
005CC106  test     rdx, rdx
005CC109  je       0x5cc171  ; -> 005CC171
005CC10B  mov      rax, qword ptr [rsp + 0x50]
005CC110  mov      qword ptr [rsp + 0x30], rsi
005CC115  add      qword ptr [rax], 8
005CC119  mov      rax, qword ptr [rax]
005CC11C  mov      rdx, qword ptr [rax - 8]
005CC120  movsxd   rax, dword ptr [rcx + 0x10]
005CC124  lea      rcx, [r9 - 8]
005CC128  add      rcx, rax
005CC12B  call     qword ptr [r8 + 8]
005CC12F  mov      esi, eax
005CC131  test     rbx, rbx
005CC134  je       0x5cc15f  ; -> 005CC15F
005CC136  call     0x5a6670  ; -> 005A6670 fn
005CC13B  cmp      rdi, rax
005CC13E  jne      0x5cc15f  ; -> 005CC15F
005CC140  mov      dword ptr [rbx + 8], esi
005CC143  mov      eax, 1
005CC148  mov      rsi, qword ptr [rsp + 0x30]
005CC14D  mov      qword ptr [rbx], 0
005CC154  mov      rbx, qword ptr [rsp + 0x40]
005CC159  add      rsp, 0x20
005CC15D  pop      rdi
005CC15E  ret      
005CC15F  xor      eax, eax
005CC161  mov      rsi, qword ptr [rsp + 0x30]
005CC166  mov      rbx, qword ptr [rsp + 0x40]
005CC16B  add      rsp, 0x20
005CC16F  pop      rdi
005CC170  ret      
005CC171  xor      eax, eax
005CC173  mov      rbx, qword ptr [rsp + 0x40]
005CC178  add      rsp, 0x20
005CC17C  pop      rdi
005CC17D  ret      
```

## 005CC5F0 (134 B, extent 005CC5F0-005CC676)

Documented callee on this page: `005A6670`

```
005CC5F0  mov      qword ptr [rsp + 0x18], rbx
005CC5F5  push     rsi
005CC5F6  sub      rsp, 0x20
005CC5FA  mov      rbx, r9
005CC5FD  mov      rsi, r8
005CC600  mov      r9, rdx
005CC603  mov      r8, rcx
005CC606  test     rdx, rdx
005CC609  je       0x5cc669  ; -> 005CC669
005CC60B  mov      rax, qword ptr [rsp + 0x50]
005CC610  mov      rcx, r9
005CC613  mov      qword ptr [rsp + 0x30], rdi
005CC618  add      qword ptr [rax], 8
005CC61C  mov      rax, qword ptr [rax]
005CC61F  mov      rdx, qword ptr [rax - 8]
005CC623  call     qword ptr [r8 + 8]
005CC627  mov      edi, eax
005CC629  test     rbx, rbx
005CC62C  je       0x5cc657  ; -> 005CC657
005CC62E  call     0x5a6670  ; -> 005A6670 fn
005CC633  cmp      rsi, rax
005CC636  jne      0x5cc657  ; -> 005CC657
005CC638  mov      dword ptr [rbx + 8], edi
005CC63B  mov      eax, 1
005CC640  mov      rdi, qword ptr [rsp + 0x30]
005CC645  mov      qword ptr [rbx], 0
005CC64C  mov      rbx, qword ptr [rsp + 0x40]
005CC651  add      rsp, 0x20
005CC655  pop      rsi
005CC656  ret      
005CC657  xor      eax, eax
005CC659  mov      rdi, qword ptr [rsp + 0x30]
005CC65E  mov      rbx, qword ptr [rsp + 0x40]
005CC663  add      rsp, 0x20
005CC667  pop      rsi
005CC668  ret      
005CC669  xor      eax, eax
005CC66B  mov      rbx, qword ptr [rsp + 0x40]
005CC670  add      rsp, 0x20
005CC674  pop      rsi
005CC675  ret      
```

## 006389C0 (133 B, extent 006389C0-00638A45)

Documented callee on this page: `00637440`

```
006389C0  mov      qword ptr [rsp + 8], rbx
006389C5  mov      qword ptr [rsp + 0x10], rsi
006389CA  push     rdi
006389CB  sub      rsp, 0x30
006389CF  xor      esi, esi
006389D1  mov      rbx, rdx
006389D4  mov      rdi, rcx
006389D7  test     rdx, rdx
006389DA  jne      0x6389e0  ; -> 006389E0
006389DC  mov      edx, esi
006389DE  jmp      0x638a27  ; -> 00638A27
006389E0  call     0x637440  ; -> 00637440 fn
006389E5  movzx    ecx, byte ptr [rbx]
006389E8  mov      edx, 0x7b5
006389ED  mov      qword ptr [rsp + 0x28], rbx
006389F2  test     ecx, ecx
006389F4  je       0x638a13  ; -> 00638A13
006389F6  nop      word ptr [rax + rax]
00638A00  and      ecx, 0x1f
00638A03  imul     edx, edx, 0x21
00638A06  lea      rbx, [rbx + 1]
00638A0A  add      edx, ecx
00638A0C  movzx    ecx, byte ptr [rbx]
00638A0F  test     ecx, ecx
00638A11  jne      0x638a00  ; -> 00638A00
00638A13  mov      dword ptr [rsp + 0x20], edx
00638A17  mov      rcx, rax
00638A1A  lea      rdx, [rsp + 0x20]
00638A1F  call     0x6311d0  ; -> 006311D0 fn
00638A24  mov      rdx, rax
00638A27  mov      rbx, qword ptr [rsp + 0x40]
00638A2C  test     rdx, rdx
00638A2F  mov      eax, 0x13
00638A34  mov      qword ptr [rdi], rdx
00638A37  cmovne   eax, esi
00638A3A  mov      rsi, qword ptr [rsp + 0x48]
00638A3F  add      rsp, 0x30
00638A43  pop      rdi
00638A44  ret      
```

## 00638A50 (133 B, extent 00638A50-00638AD5)

Documented callee on this page: `00637440`

```
00638A50  mov      qword ptr [rsp + 8], rbx
00638A55  mov      qword ptr [rsp + 0x10], rsi
00638A5A  push     rdi
00638A5B  sub      rsp, 0x30
00638A5F  xor      esi, esi
00638A61  mov      rbx, rdx
00638A64  mov      rdi, rcx
00638A67  test     rdx, rdx
00638A6A  jne      0x638a70  ; -> 00638A70
00638A6C  mov      edx, esi
00638A6E  jmp      0x638ab7  ; -> 00638AB7
00638A70  call     0x637440  ; -> 00637440 fn
00638A75  movzx    ecx, byte ptr [rbx]
00638A78  mov      edx, 0x7b5
00638A7D  mov      qword ptr [rsp + 0x28], rbx
00638A82  test     ecx, ecx
00638A84  je       0x638aa3  ; -> 00638AA3
00638A86  nop      word ptr [rax + rax]
00638A90  and      ecx, 0x1f
00638A93  imul     edx, edx, 0x21
00638A96  lea      rbx, [rbx + 1]
00638A9A  add      edx, ecx
00638A9C  movzx    ecx, byte ptr [rbx]
00638A9F  test     ecx, ecx
00638AA1  jne      0x638a90  ; -> 00638A90
00638AA3  mov      dword ptr [rsp + 0x20], edx
00638AA7  mov      rcx, rax
00638AAA  lea      rdx, [rsp + 0x20]
00638AAF  call     0x6311d0  ; -> 006311D0 fn
00638AB4  mov      rdx, rax
00638AB7  mov      rbx, qword ptr [rsp + 0x40]
00638ABC  test     rdx, rdx
00638ABF  mov      eax, 0x13
00638AC4  mov      qword ptr [rdi], rdx
00638AC7  cmovne   eax, esi
00638ACA  mov      rsi, qword ptr [rsp + 0x48]
00638ACF  add      rsp, 0x30
00638AD3  pop      rdi
00638AD4  ret      
```

## 0063BEF0 (141 B, extent 0063BEF0-0063BF7D)

Documented callee on this page: `00637440`

```
0063BEF0  mov      qword ptr [rsp + 8], rbx
0063BEF5  push     rdi
0063BEF6  sub      rsp, 0x30
0063BEFA  mov      rbx, rdx
0063BEFD  mov      rdi, rcx
0063BF00  test     rdx, rdx
0063BF03  je       0x63bf70  ; -> 0063BF70
0063BF05  call     0x637440  ; -> 00637440 fn
0063BF0A  movzx    r8d, byte ptr [rbx]
0063BF0E  mov      edx, 0x7b5
0063BF13  mov      qword ptr [rsp + 0x28], rbx
0063BF18  test     r8d, r8d
0063BF1B  je       0x63bf37  ; -> 0063BF37
0063BF1D  nop      dword ptr [rax]
0063BF20  and      r8d, 0x1f
0063BF24  imul     edx, edx, 0x21
0063BF27  lea      rbx, [rbx + 1]
0063BF2B  add      edx, r8d
0063BF2E  movzx    r8d, byte ptr [rbx]
0063BF32  test     r8d, r8d
0063BF35  jne      0x63bf20  ; -> 0063BF20
0063BF37  mov      dword ptr [rsp + 0x20], edx
0063BF3B  mov      rcx, rax
0063BF3E  lea      rdx, [rsp + 0x20]
0063BF43  call     0x6311d0  ; -> 006311D0 fn
0063BF48  test     rax, rax
0063BF4B  je       0x63bf70  ; -> 0063BF70
0063BF4D  mov      rdx, qword ptr [rax]
0063BF50  mov      rcx, rax
0063BF53  call     qword ptr [rdx + 8]
0063BF56  test     rax, rax
0063BF59  je       0x63bf70  ; -> 0063BF70
0063BF5B  mov      rdx, rax
0063BF5E  mov      rcx, rdi
0063BF61  mov      rbx, qword ptr [rsp + 0x40]
0063BF66  add      rsp, 0x30
0063BF6A  pop      rdi
0063BF6B  jmp      0x63bc80  ; -> 0063BC80 fn
0063BF70  xor      eax, eax
0063BF72  mov      rbx, qword ptr [rsp + 0x40]
0063BF77  add      rsp, 0x30
0063BF7B  pop      rdi
0063BF7C  ret      
```

## 006A6870 (114 B, extent 006A6870-006A68E2)

Documented callee on this page: `005A6670`

```
006A6870  mov      qword ptr [rsp + 0x18], rbx
006A6875  push     rsi
006A6876  sub      rsp, 0x20
006A687A  mov      rbx, r9
006A687D  mov      rsi, r8
006A6880  mov      rax, rcx
006A6883  test     rdx, rdx
006A6886  je       0x6a68d5  ; -> 006A68D5
006A6888  mov      rcx, rdx
006A688B  mov      qword ptr [rsp + 0x30], rdi
006A6890  call     qword ptr [rax + 8]
006A6893  mov      edi, eax
006A6895  test     rbx, rbx
006A6898  je       0x6a68c3  ; -> 006A68C3
006A689A  call     0x5a6670  ; -> 005A6670 fn
006A689F  cmp      rsi, rax
006A68A2  jne      0x6a68c3  ; -> 006A68C3
006A68A4  mov      dword ptr [rbx + 8], edi
006A68A7  mov      eax, 1
006A68AC  mov      rdi, qword ptr [rsp + 0x30]
006A68B1  mov      qword ptr [rbx], 0
006A68B8  mov      rbx, qword ptr [rsp + 0x40]
006A68BD  add      rsp, 0x20
006A68C1  pop      rsi
006A68C2  ret      
006A68C3  xor      eax, eax
006A68C5  mov      rdi, qword ptr [rsp + 0x30]
006A68CA  mov      rbx, qword ptr [rsp + 0x40]
006A68CF  add      rsp, 0x20
006A68D3  pop      rsi
006A68D4  ret      
006A68D5  xor      eax, eax
006A68D7  mov      rbx, qword ptr [rsp + 0x40]
006A68DC  add      rsp, 0x20
006A68E0  pop      rsi
006A68E1  ret      
```

## 006ACAC0 (237 B, extent 006ACAC0-006ACBAD)

Documented callee on this page: `0067F700`

```
006ACAC0  mov      qword ptr [rsp + 0x10], rbx
006ACAC5  mov      qword ptr [rsp + 0x18], rsi
006ACACA  push     rdi
006ACACB  sub      rsp, 0x20
006ACACF  cmp      qword ptr [rcx + 8], 0
006ACAD4  lea      rsi, [rip + 0x1882065]  ; -> 01F2EB40
006ACADB  mov      rdi, rdx
006ACADE  mov      rbx, rcx
006ACAE1  je       0x6acaef  ; -> 006ACAEF
006ACAE3  lea      rdx, [rcx + 0x10]
006ACAE7  mov      rcx, rsi
006ACAEA  call     0x67fe20  ; -> 0067FE20 fn
006ACAEF  mov      qword ptr [rbx + 8], rdi
006ACAF3  test     rdi, rdi
006ACAF6  je       0x6acb96  ; -> 006ACB96
006ACAFC  lea      rdx, [rbx + 0x10]
006ACB00  test     rdx, rdx
006ACB03  je       0x6acb1c  ; -> 006ACB1C
006ACB05  mov      qword ptr [rdx], rdx
006ACB08  mov      qword ptr [rdx + 8], rdx
006ACB0C  mov      qword ptr [rdx + 0x10], rdx
006ACB10  mov      qword ptr [rdx + 0x18], rdi
006ACB14  mov      qword ptr [rdx + 0x20], 0
006ACB1C  mov      qword ptr [rbx + 0x30], rbx
006ACB20  lea      r10, [rip + 0x1882031]  ; -> 01F2EB58
006ACB27  movzx    eax, byte ptr [rdx + 0x10]
006ACB2B  xor      cl, cl
006ACB2D  and      eax, 1
006ACB30  neg      eax
006ACB32  cdqe     
006ACB34  inc      rax
006ACB37  add      qword ptr [rdx + 0x10], rax
006ACB3B  mov      qword ptr [rdx], rsi
006ACB3E  mov      qword ptr [rdx + 8], rsi
006ACB42  mov      r8, qword ptr [rip + 0x188200f]  ; -> 01F2EB58 [u64 0x0000000001F2EB40]
006ACB49  cmp      r8, rsi
006ACB4C  je       0x6acb79  ; -> 006ACB79
006ACB4E  mov      r9, qword ptr [rdx + 0x18]
006ACB52  mov      rax, qword ptr [r8 + 0x18]
006ACB56  mov      r10, r8
006ACB59  cmp      rax, r9
006ACB5C  jbe      0x6acb65  ; -> 006ACB65
006ACB5E  mov      ecx, 1
006ACB63  jmp      0x6acb6a  ; -> 006ACB6A
006ACB65  jae      0x6acba6  ; -> 006ACBA6
006ACB67  or       ecx, 0xffffffff
006ACB6A  shr      ecx, 0x1f
006ACB6D  movzx    eax, cl
006ACB70  mov      r8, qword ptr [r8 + rax*8]
006ACB74  cmp      r8, rsi
006ACB77  jne      0x6acb52  ; -> 006ACB52
006ACB79  movzx    eax, byte ptr [rdx + 0x10]
006ACB7D  and      eax, 1
006ACB80  add      rax, r10
006ACB83  mov      qword ptr [rdx + 0x10], rax
006ACB87  movzx    eax, cl
006ACB8A  mov      qword ptr [r10 + rax*8], rdx
006ACB8E  mov      rcx, rsi
006ACB91  call     0x67f700  ; -> 0067F700 fn
006ACB96  mov      rbx, qword ptr [rsp + 0x38]
006ACB9B  mov      rsi, qword ptr [rsp + 0x40]
006ACBA0  add      rsp, 0x20
006ACBA4  pop      rdi
006ACBA5  ret      
006ACBA6  test     r8, r8
006ACBA9  jne      0x6acb96  ; -> 006ACB96
006ACBAB  jmp      0x6acb8e  ; -> 006ACB8E
```
