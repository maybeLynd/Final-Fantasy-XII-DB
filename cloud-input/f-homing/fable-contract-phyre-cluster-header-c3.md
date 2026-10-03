# F homing pack (FABLE): `22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md`

Generated 2026-10-03 06:31 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 6. No bearing page cites them and no documented function calls them directly.

## 001C1A60 (158 B, extent 001C1A60-001C1AFE)

Documented callee on this page: `001C22A0`

```
001C1A60  mov      qword ptr [rsp + 8], rbx
001C1A65  mov      qword ptr [rsp + 0x10], rsi
001C1A6A  push     rdi
001C1A6B  sub      rsp, 0x20
001C1A6F  mov      rbx, r8
001C1A72  mov      rdi, rdx
001C1A75  mov      rsi, rcx
001C1A78  cmp      rdx, rcx
001C1A7B  je       0x1c1aeb  ; -> 001C1AEB
001C1A7D  nop      dword ptr [rax]
001C1A80  sub      rdi, 0x230
001C1A87  sub      rbx, 0x230
001C1A8E  lea      rdx, [rdi + 0x108]
001C1A95  mov      r8, rdi
001C1A98  sub      r8, rbx
001C1A9B  mov      r9d, 0x80
001C1AA1  mov      eax, dword ptr [rdi]
001C1AA3  lea      rcx, [rbx + 8]
001C1AA7  mov      dword ptr [rbx], eax
001C1AA9  mov      eax, dword ptr [rdx - 0x104]
001C1AAF  mov      dword ptr [rbx + 4], eax
001C1AB2  nop      dword ptr [rax]
001C1AB6  nop      word ptr [rax + rax]
001C1AC0  movzx    eax, byte ptr [r8 + rcx]
001C1AC5  mov      byte ptr [rcx], al
001C1AC7  movzx    eax, byte ptr [r8 + rcx + 1]
001C1ACD  mov      byte ptr [rcx + 1], al
001C1AD0  lea      rcx, [rcx + 2]
001C1AD4  sub      r9, 1
001C1AD8  jne      0x1c1ac0  ; -> 001C1AC0
001C1ADA  lea      rcx, [rbx + 0x108]
001C1AE1  call     0x1c22a0  ; -> 001C22A0 fn
001C1AE6  cmp      rdi, rsi
001C1AE9  jne      0x1c1a80  ; -> 001C1A80
001C1AEB  mov      rsi, qword ptr [rsp + 0x38]
001C1AF0  mov      rax, rbx
001C1AF3  mov      rbx, qword ptr [rsp + 0x30]
001C1AF8  add      rsp, 0x20
001C1AFC  pop      rdi
001C1AFD  ret      
```

## 001C2230 (104 B, extent 001C2230-001C2298)

Documented callee on this page: `001C22A0`

```
001C2230  push     rbx
001C2232  sub      rsp, 0x20
001C2236  mov      eax, dword ptr [rdx]
001C2238  lea      r8, [rcx + 8]
001C223C  mov      dword ptr [rcx], eax
001C223E  mov      r9, rdx
001C2241  mov      eax, dword ptr [rdx + 4]
001C2244  mov      rbx, rcx
001C2247  mov      dword ptr [rcx + 4], eax
001C224A  sub      r9, rcx
001C224D  mov      r10d, 0x80
001C2253  nop      dword ptr [rax]
001C2257  nop      word ptr [rax + rax]
001C2260  movzx    eax, byte ptr [r9 + r8]
001C2265  mov      byte ptr [r8], al
001C2268  movzx    eax, byte ptr [r9 + r8 + 1]
001C226E  mov      byte ptr [r8 + 1], al
001C2272  lea      r8, [r8 + 2]
001C2276  sub      r10, 1
001C227A  jne      0x1c2260  ; -> 001C2260
001C227C  add      rdx, 0x108
001C2283  add      rcx, 0x108
001C228A  call     0x1c22a0  ; -> 001C22A0 fn
001C228F  mov      rax, rbx
001C2292  add      rsp, 0x20
001C2296  pop      rbx
001C2297  ret      
```

## 006305A0 (157 B, extent 006305A0-0063063D)

Documented callee on this page: `0063CE80`

```
006305A0  mov      qword ptr [rsp + 8], rbx
006305A5  mov      qword ptr [rsp + 0x10], rsi
006305AA  push     rdi
006305AB  sub      rsp, 0x40
006305AF  mov      eax, dword ptr [rip + 0x26c7cf3]  ; -> 02CF82A8
006305B5  lea      rsi, [rip + 0x26c7cb4]  ; -> 02CF8270
006305BC  mov      dword ptr [rsp + 0x24], eax
006305C0  mov      dword ptr [rsp + 0x20], 0
006305C8  mov      qword ptr [rsp + 0x28], rcx
006305CD  mov      byte ptr [rsp + 0x30], 1
006305D2  nop      dword ptr [rax]
006305D6  nop      word ptr [rax + rax]
006305E0  lea      rdi, [rsi + 0x80]
006305E7  mov      rbx, qword ptr [rdi]
006305EA  cmp      rbx, rdi
006305ED  je       0x630624  ; -> 00630624
006305EF  test     rbx, rbx
006305F2  je       0x630624  ; -> 00630624
006305F4  add      rbx, -8
006305F8  je       0x630624  ; -> 00630624
006305FA  nop      word ptr [rax + rax]
00630600  mov      rdx, rbx
00630603  lea      rcx, [rsp + 0x20]
00630608  call     0x63ce80  ; -> 0063CE80 fn
0063060D  mov      rax, qword ptr [rbx + 8]
00630611  cmp      rax, rdi
00630614  je       0x630624  ; -> 00630624
00630616  test     rax, rax
00630619  je       0x630624  ; -> 00630624
0063061B  lea      rbx, [rax - 8]
0063061F  test     rbx, rbx
00630622  jne      0x630600  ; -> 00630600
00630624  mov      rsi, qword ptr [rsi + 0x78]
00630628  test     rsi, rsi
0063062B  jne      0x6305e0  ; -> 006305E0
0063062D  mov      rbx, qword ptr [rsp + 0x50]
00630632  mov      rsi, qword ptr [rsp + 0x58]
00630637  add      rsp, 0x40
0063063B  pop      rdi
0063063C  ret      
```

## 006306E0 (157 B, extent 006306E0-0063077D)

Documented callee on this page: `0063CE80`

```
006306E0  mov      qword ptr [rsp + 8], rbx
006306E5  mov      qword ptr [rsp + 0x10], rsi
006306EA  push     rdi
006306EB  sub      rsp, 0x40
006306EF  mov      eax, dword ptr [rip + 0x26c7db3]  ; -> 02CF84A8
006306F5  lea      rsi, [rip + 0x26c7d74]  ; -> 02CF8470
006306FC  xor      edx, edx
006306FE  mov      dword ptr [rsp + 0x24], eax
00630702  test     rcx, rcx
00630705  mov      dword ptr [rsp + 0x20], edx
00630709  lea      rax, [rcx + 0x30]
0063070D  mov      byte ptr [rsp + 0x30], 1
00630712  cmove    rax, rdx
00630716  mov      qword ptr [rsp + 0x28], rax
0063071B  nop      dword ptr [rax + rax]
00630720  lea      rdi, [rsi + 0x80]
00630727  mov      rbx, qword ptr [rdi]
0063072A  cmp      rbx, rdi
0063072D  je       0x630764  ; -> 00630764
0063072F  test     rbx, rbx
00630732  je       0x630764  ; -> 00630764
00630734  add      rbx, -8
00630738  je       0x630764  ; -> 00630764
0063073A  nop      word ptr [rax + rax]
00630740  mov      rdx, rbx
00630743  lea      rcx, [rsp + 0x20]
00630748  call     0x63ce80  ; -> 0063CE80 fn
0063074D  mov      rax, qword ptr [rbx + 8]
00630751  cmp      rax, rdi
00630754  je       0x630764  ; -> 00630764
00630756  test     rax, rax
00630759  je       0x630764  ; -> 00630764
0063075B  lea      rbx, [rax - 8]
0063075F  test     rbx, rbx
00630762  jne      0x630740  ; -> 00630740
00630764  mov      rsi, qword ptr [rsi + 0x78]
00630768  test     rsi, rsi
0063076B  jne      0x630720  ; -> 00630720
0063076D  mov      rbx, qword ptr [rsp + 0x50]
00630772  mov      rsi, qword ptr [rsp + 0x58]
00630777  add      rsp, 0x40
0063077B  pop      rdi
0063077C  ret      
```

## 00630BE0 (157 B, extent 00630BE0-00630C7D)

Documented callee on this page: `0063CE80`

```
00630BE0  mov      qword ptr [rsp + 8], rbx
00630BE5  mov      qword ptr [rsp + 0x10], rsi
00630BEA  push     rdi
00630BEB  sub      rsp, 0x40
00630BEF  mov      eax, dword ptr [rip + 0x26c76b3]  ; -> 02CF82A8
00630BF5  lea      rsi, [rip + 0x26c7674]  ; -> 02CF8270
00630BFC  mov      dword ptr [rsp + 0x24], eax
00630C00  mov      dword ptr [rsp + 0x20], 0
00630C08  mov      qword ptr [rsp + 0x28], rcx
00630C0D  mov      byte ptr [rsp + 0x30], 0
00630C12  nop      dword ptr [rax]
00630C16  nop      word ptr [rax + rax]
00630C20  lea      rdi, [rsi + 0x80]
00630C27  mov      rbx, qword ptr [rdi + 8]
00630C2B  cmp      rbx, rdi
00630C2E  je       0x630c64  ; -> 00630C64
00630C30  test     rbx, rbx
00630C33  je       0x630c64  ; -> 00630C64
00630C35  add      rbx, -8
00630C39  je       0x630c64  ; -> 00630C64
00630C3B  nop      dword ptr [rax + rax]
00630C40  mov      rdx, rbx
00630C43  lea      rcx, [rsp + 0x20]
00630C48  call     0x63ce80  ; -> 0063CE80 fn
00630C4D  mov      rax, qword ptr [rbx + 0x10]
00630C51  cmp      rax, rdi
00630C54  je       0x630c64  ; -> 00630C64
00630C56  test     rax, rax
00630C59  je       0x630c64  ; -> 00630C64
00630C5B  lea      rbx, [rax - 8]
00630C5F  test     rbx, rbx
00630C62  jne      0x630c40  ; -> 00630C40
00630C64  mov      rsi, qword ptr [rsi + 0x78]
00630C68  test     rsi, rsi
00630C6B  jne      0x630c20  ; -> 00630C20
00630C6D  mov      rbx, qword ptr [rsp + 0x50]
00630C72  mov      rsi, qword ptr [rsp + 0x58]
00630C77  add      rsp, 0x40
00630C7B  pop      rdi
00630C7C  ret      
```

## 00630D20 (157 B, extent 00630D20-00630DBD)

Documented callee on this page: `0063CE80`

```
00630D20  mov      qword ptr [rsp + 8], rbx
00630D25  mov      qword ptr [rsp + 0x10], rsi
00630D2A  push     rdi
00630D2B  sub      rsp, 0x40
00630D2F  mov      eax, dword ptr [rip + 0x26c7773]  ; -> 02CF84A8
00630D35  lea      rsi, [rip + 0x26c7734]  ; -> 02CF8470
00630D3C  xor      edx, edx
00630D3E  mov      dword ptr [rsp + 0x24], eax
00630D42  test     rcx, rcx
00630D45  mov      dword ptr [rsp + 0x20], edx
00630D49  lea      rax, [rcx + 0x30]
00630D4D  mov      byte ptr [rsp + 0x30], dl
00630D51  cmove    rax, rdx
00630D55  mov      qword ptr [rsp + 0x28], rax
00630D5A  nop      word ptr [rax + rax]
00630D60  lea      rdi, [rsi + 0x80]
00630D67  mov      rbx, qword ptr [rdi + 8]
00630D6B  cmp      rbx, rdi
00630D6E  je       0x630da4  ; -> 00630DA4
00630D70  test     rbx, rbx
00630D73  je       0x630da4  ; -> 00630DA4
00630D75  add      rbx, -8
00630D79  je       0x630da4  ; -> 00630DA4
00630D7B  nop      dword ptr [rax + rax]
00630D80  mov      rdx, rbx
00630D83  lea      rcx, [rsp + 0x20]
00630D88  call     0x63ce80  ; -> 0063CE80 fn
00630D8D  mov      rax, qword ptr [rbx + 0x10]
00630D91  cmp      rax, rdi
00630D94  je       0x630da4  ; -> 00630DA4
00630D96  test     rax, rax
00630D99  je       0x630da4  ; -> 00630DA4
00630D9B  lea      rbx, [rax - 8]
00630D9F  test     rbx, rbx
00630DA2  jne      0x630d80  ; -> 00630D80
00630DA4  mov      rsi, qword ptr [rsi + 0x78]
00630DA8  test     rsi, rsi
00630DAB  jne      0x630d60  ; -> 00630D60
00630DAD  mov      rbx, qword ptr [rsp + 0x50]
00630DB2  mov      rsi, qword ptr [rsp + 0x58]
00630DB7  add      rsp, 0x40
00630DBB  pop      rdi
00630DBC  ret      
```
