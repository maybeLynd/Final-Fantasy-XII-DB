# Homing pack: `00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md`

Generated 2026-10-03 13:52 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h13-what-the-console-tunes.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0019B400 (115 B, extent 0019B400-0019B473)

Entered from (direct sites whose caller this page cites): `00202930` + 0x19F (call; `00202930` is cited on this page)
Other direct sites: `0019B480` + 0x44 (call); `0019B500` + 0xF (call)

Host context: "-15 ('bshape.py'):  | cluster | members | role | |---|---|---| | '008FAxxx' twin builders | '001C7360', '001C7520' (446 B each, identical shape: '001FF740' ×4 + '00200BE0'/'001FEE10'/'001EDF00' ×2 + '00202930', '[rax+0x10]'/'[rax+0x18]' indirect, templates '008FA338'/'008FA350' vs '008FA368'/'008FA388') | two near-identical record materializers — a command-pair pattern (same builder, adjacent template blocks) | | command-arm bodies | '0"

```
0019B400  push     rbx
0019B402  sub      rsp, 0x30
0019B406  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0019B40F  mov      rbx, rcx
0019B412  lea      rax, [rip + 0x758aaf]  ; -> 008F3EC8
0019B419  mov      qword ptr [rcx], rax
0019B41C  cmp      qword ptr [rcx + 0x80], 0
0019B424  je       0x19b455  ; -> 0019B455
0019B426  mov      rcx, qword ptr [rcx + 0x18]
0019B42A  lea      rax, [rbx + 0x70]
0019B42E  cmp      qword ptr [rcx], rax
0019B431  jne      0x19b455  ; -> 0019B455
0019B433  mov      r8, qword ptr [rbx + 0x90]
0019B43A  mov      rdx, qword ptr [rbx + 0x88]
0019B441  mov      qword ptr [rcx], rdx
0019B444  mov      rax, qword ptr [rbx + 0x38]
0019B448  mov      qword ptr [rax], rdx
0019B44B  sub      r8d, edx
0019B44E  mov      rax, qword ptr [rbx + 0x50]
0019B452  mov      dword ptr [rax], r8d
0019B455  cmp      byte ptr [rbx + 0x7c], 0
0019B459  je       0x19b464  ; -> 0019B464
0019B45B  mov      rcx, rbx
0019B45E  call     0x19b8c0  ; -> 0019B8C0 fn
0019B463  nop      
0019B464  mov      rcx, rbx
0019B467  add      rsp, 0x30
0019B46B  pop      rbx
0019B46C  jmp      qword ptr [rip + 0x72732d]  ; -> 008C27A0 [u64 0x0000000001CCDA9C]
```

## 0019B8C0 (127 B, extent 0019B8C0-0019B93F)

Entered from (direct sites whose caller this page cites): `00202930` + 0x150 (call; `00202930` is cited on this page)
Other direct sites: `0019B400` + 0x5E (call)

Host context: "-15 ('bshape.py'):  | cluster | members | role | |---|---|---| | '008FAxxx' twin builders | '001C7360', '001C7520' (446 B each, identical shape: '001FF740' ×4 + '00200BE0'/'001FEE10'/'001EDF00' ×2 + '00202930', '[rax+0x10]'/'[rax+0x18]' indirect, templates '008FA338'/'008FA350' vs '008FA368'/'008FA388') | two near-identical record materializers — a command-pair pattern (same builder, adjacent template blocks) | | command-arm bodies | '0"

```
0019B8C0  mov      qword ptr [rsp + 8], rbx
0019B8C5  mov      qword ptr [rsp + 0x10], rsi
0019B8CA  push     rdi
0019B8CB  sub      rsp, 0x20
0019B8CF  cmp      qword ptr [rcx + 0x80], 0
0019B8D7  mov      rbx, rcx
0019B8DA  jne      0x19b8e2  ; -> 0019B8E2
0019B8DC  xor      edi, edi
0019B8DE  mov      esi, edi
0019B8E0  jmp      0x19b905  ; -> 0019B905
0019B8E2  call     0x19b580  ; -> 0019B580 fn
0019B8E7  mov      rcx, qword ptr [rbx + 0x80]
0019B8EE  xor      edi, edi
0019B8F0  test     al, al
0019B8F2  mov      rsi, rbx
0019B8F5  cmove    rsi, rdi
0019B8F9  call     qword ptr [rip + 0x727601]  ; -> 008C2F00 [u64 0x0000000001CCECE2]
0019B8FF  test     eax, eax
0019B901  cmovne   rsi, rdi
0019B905  mov      rcx, rbx
0019B908  mov      byte ptr [rbx + 0x7c], 0
0019B90C  mov      byte ptr [rbx + 0x71], 0
0019B910  call     qword ptr [rip + 0x726e9a]  ; -> 008C27B0 [u64 0x0000000001CCDB24]
0019B916  mov      qword ptr [rbx + 0x80], rdi
0019B91D  mov      rax, rsi
0019B920  mov      rcx, qword ptr [rip + 0x1de5819]  ; -> 01F81140
0019B927  mov      rsi, qword ptr [rsp + 0x38]
0019B92C  mov      qword ptr [rbx + 0x74], rcx
0019B930  mov      qword ptr [rbx + 0x68], rdi
0019B934  mov      rbx, qword ptr [rsp + 0x30]
0019B939  add      rsp, 0x20
0019B93D  pop      rdi
0019B93E  ret      
```

## 0019B990 (311 B, extent 0019B990-0019BAC7)

Entered from (direct sites whose caller this page cites): `00202930` + 0xFA (call; `00202930` is cited on this page)
Other direct sites: none

Host context: "-15 ('bshape.py'):  | cluster | members | role | |---|---|---| | '008FAxxx' twin builders | '001C7360', '001C7520' (446 B each, identical shape: '001FF740' ×4 + '00200BE0'/'001FEE10'/'001EDF00' ×2 + '00202930', '[rax+0x10]'/'[rax+0x18]' indirect, templates '008FA338'/'008FA350' vs '008FA368'/'008FA388') | two near-identical record materializers — a command-pair pattern (same builder, adjacent template blocks) | | command-arm bodies | '0"

```
0019B990  push     rdi
0019B992  sub      rsp, 0x40
0019B996  mov      qword ptr [rsp + 0x38], 0xfffffffffffffffe
0019B99F  mov      qword ptr [rsp + 0x58], rbx
0019B9A4  mov      qword ptr [rsp + 0x60], rsi
0019B9A9  mov      eax, r8d
0019B9AC  mov      r10, rdx
0019B9AF  mov      rbx, rcx
0019B9B2  cmp      qword ptr [rcx + 0x80], 0
0019B9BA  jne      0x19bab5  ; -> 0019BAB5
0019B9C0  mov      r8d, r9d
0019B9C3  mov      edx, eax
0019B9C5  mov      rcx, r10
0019B9C8  call     qword ptr [rip + 0x726bfa]  ; -> 008C25C8 [u64 0x0000000001CCDC76]
0019B9CE  mov      rdi, rax
0019B9D1  test     rax, rax
0019B9D4  je       0x19bab5  ; -> 0019BAB5
0019B9DA  mov      byte ptr [rbx + 0x7c], 1
0019B9DE  mov      byte ptr [rbx + 0x71], 0
0019B9E2  mov      rcx, rbx
0019B9E5  call     qword ptr [rip + 0x726dc5]  ; -> 008C27B0 [u64 0x0000000001CCDB24]
0019B9EB  xor      esi, esi
0019B9ED  mov      qword ptr [rsp + 0x50], rsi
0019B9F2  mov      qword ptr [rsp + 0x20], rsi
0019B9F7  mov      qword ptr [rsp + 0x28], rsi
0019B9FC  lea      r9, [rsp + 0x28]
0019BA01  lea      r8, [rsp + 0x20]
0019BA06  lea      rdx, [rsp + 0x50]
0019BA0B  mov      rcx, rdi
0019BA0E  call     qword ptr [rip + 0x72740c]  ; -> 008C2E20 [u64 0x0000000001CCEEC8]
0019BA14  mov      rax, qword ptr [rsp + 0x50]
0019BA19  mov      qword ptr [rbx + 0x18], rax
0019BA1D  mov      qword ptr [rbx + 0x20], rax
0019BA21  mov      rax, qword ptr [rsp + 0x20]
0019BA26  mov      qword ptr [rbx + 0x38], rax
0019BA2A  mov      qword ptr [rbx + 0x40], rax
0019BA2E  mov      rax, qword ptr [rsp + 0x28]
0019BA33  mov      qword ptr [rbx + 0x50], rax
0019BA37  mov      qword ptr [rbx + 0x58], rax
0019BA3B  mov      qword ptr [rbx + 0x80], rdi
0019BA42  mov      rax, qword ptr [rip + 0x1de56f7]  ; -> 01F81140
0019BA49  mov      qword ptr [rbx + 0x74], rax
0019BA4D  mov      qword ptr [rbx + 0x68], rsi
0019BA51  lea      rdx, [rsp + 0x28]
0019BA56  mov      rcx, rbx
0019BA59  call     qword ptr [rip + 0x726d49]  ; -> 008C27A8 [u64 0x0000000001CCDAD8]
0019BA5F  nop      
0019BA60  mov      rcx, rax
0019BA63  call     0x19b2f0  ; -> 0019B2F0 fn
0019BA68  mov      rdi, rax
0019BA6B  mov      rcx, rax
0019BA6E  call     qword ptr [rip + 0x726bc4]  ; -> 008C2638 [u64 0x0000000001CCCE5A]
0019BA74  test     al, al
0019BA76  je       0x19ba7e  ; -> 0019BA7E
0019BA78  mov      qword ptr [rbx + 0x68], rsi
0019BA7C  jmp      0x19ba8c  ; -> 0019BA8C
0019BA7E  mov      qword ptr [rbx + 0x68], rdi
0019BA82  mov      rcx, rbx
0019BA85  call     qword ptr [rip + 0x726d25]  ; -> 008C27B0 [u64 0x0000000001CCDB24]
0019BA8B  nop      
0019BA8C  mov      rcx, qword ptr [rsp + 0x30]
0019BA91  test     rcx, rcx
0019BA94  je       0x19bab0  ; -> 0019BAB0
0019BA96  mov      rax, qword ptr [rcx]
0019BA99  call     qword ptr [rax + 0x10]
0019BA9C  test     rax, rax
0019BA9F  je       0x19bab0  ; -> 0019BAB0
0019BAA1  mov      r8, qword ptr [rax]
0019BAA4  mov      edx, 1
0019BAA9  mov      rcx, rax
0019BAAC  call     qword ptr [r8]
0019BAAF  nop      
0019BAB0  mov      rax, rbx
0019BAB3  jmp      0x19bab7  ; -> 0019BAB7
0019BAB5  xor      eax, eax
0019BAB7  mov      rbx, qword ptr [rsp + 0x58]
0019BABC  mov      rsi, qword ptr [rsp + 0x60]
0019BAC1  add      rsp, 0x40
0019BAC5  pop      rdi
0019BAC6  ret      
```

## 001EF540 (25 B, extent 001EF540-001EF559)

Entered from (direct sites whose caller this page cites): `001AC7C0` + 0x38 (jmp; `001AC7C0` is cited on this page)
Other direct sites: none

Host context: "cell, '01F812C8', is filled by the   static initializer '0015CC00' from '001F0850' and read by the scene-config loaders '001C3D50' and '001C7940', and   three getters return the pointer ('0015CC00', '001AC7C0', '001FB310'). ORACLE's flow, not bounded by hop count,   follows that cell and those getters and **still finds only the constructor writing '+0x13C'**, so the conclusion   stands. Its stated assumption: code given an element point"

```
001EF540  test     dl, dl
001EF542  je       0x1ef54c  ; -> 001EF54C
001EF544  xor      dword ptr [rcx + 0x130], 2
001EF54B  ret      
001EF54C  mov      eax, dword ptr [rcx + 0x134]
001EF552  mov      dword ptr [rcx + 0x130], eax
001EF558  ret      
```
