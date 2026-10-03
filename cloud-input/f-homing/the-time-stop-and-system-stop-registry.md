# F homing pack: `00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md`

Generated 2026-10-02 21:17 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 9. No bearing page cites them and no documented function calls them directly.

## 002F18D0 (121 B, extent 002F18D0-002F1949)

Documented callee on this page: `003756B0`

```
002F18D0  push     rbx
002F18D2  sub      rsp, 0x30
002F18D6  mov      eax, dword ptr [rcx + 4]
002F18D9  xorps    xmm1, xmm1
002F18DC  add      eax, dword ptr [rip + 0x1b0c7d2]  ; -> 01DFE0B4 [u32 0x00000001]
002F18E2  mov      rbx, rcx
002F18E5  test     byte ptr [rcx + 0x28], 4
002F18E9  movd     xmm0, dword ptr [rcx]
002F18ED  movaps   xmmword ptr [rsp + 0x20], xmm6
002F18F2  cvtsi2ss xmm1, rax
002F18F7  cvtdq2ps xmm0, xmm0
002F18FA  movaps   xmm6, xmm1
002F18FD  subss    xmm6, xmm0
002F1901  divss    xmm6, xmm1
002F1905  mulss    xmm6, dword ptr [rip + 0x5d4233]  ; -> 008C5B40 [f32 255]
002F190D  je       0x2f1929  ; -> 002F1929
002F190F  mov      ecx, 1
002F1914  call     0x3587b0  ; -> 003587B0 fn
002F1919  mov      edx, dword ptr [rbx + 0x38]
002F191C  mov      r8d, 2
002F1922  xor      ecx, ecx
002F1924  call     0x374d40  ; -> 00374D40 fn
002F1929  mov      ecx, dword ptr [rbx + 0x30]
002F192C  cvttss2si edx, xmm6
002F1930  call     0x3756b0  ; -> 003756B0 fn
002F1935  mov      ecx, 1
002F193A  movaps   xmm6, xmmword ptr [rsp + 0x20]
002F193F  add      rsp, 0x30
002F1943  pop      rbx
002F1944  jmp      0x182610  ; -> 00182610 fn
```

## 00344120 (32 B, extent 00344120-00344140)

Documented callee on this page: `002ED020`

```
00344120  push     rbx
00344122  sub      rsp, 0x20
00344126  mov      rbx, rdx
00344129  xor      edx, edx
0034412B  mov      rcx, rbx
0034412E  call     0x2ece00  ; -> 002ECE00 fn
00344133  mov      rcx, rbx
00344136  add      rsp, 0x20
0034413A  pop      rbx
0034413B  jmp      0x2ed020  ; -> 002ED020 fn
```

## 0034E530 (66 B, extent 0034E530-0034E572)

Documented callee on this page: `0035A720`

```
0034E530  mov      qword ptr [rsp + 8], rbx
0034E535  push     rdi
0034E536  sub      rsp, 0x20
0034E53A  mov      rcx, r9
0034E53D  mov      rbx, r9
0034E540  call     0x267e10  ; -> 00267E10 fn
0034E545  mov      rcx, rbx
0034E548  mov      edi, eax
0034E54A  call     0x267e10  ; -> 00267E10 fn
0034E54F  mov      edx, 1
0034E554  mov      ecx, eax
0034E556  mov      r8d, edx
0034E559  call     0x359ca0  ; -> 00359CA0 fn
0034E55E  mov      edx, edi
0034E560  mov      rcx, rax
0034E563  mov      rbx, qword ptr [rsp + 0x30]
0034E568  add      rsp, 0x20
0034E56C  pop      rdi
0034E56D  jmp      0x35a720  ; -> 0035A720 fn
```

## 003531A0 (51 B, extent 003531A0-003531D3)

Documented callee on this page: `002E2440`

```
003531A0  sub      rsp, 0x28
003531A4  mov      rcx, r9
003531A7  call     0x267e10  ; -> 00267E10 fn
003531AC  xor      edx, edx
003531AE  lea      ecx, [rdx + 1]
003531B1  call     0x2e2440  ; -> 002E2440 fn
003531B6  mov      edx, 3
003531BB  xor      ecx, ecx
003531BD  call     0x2e1c40  ; -> 002E1C40 fn
003531C2  mov      edx, 3
003531C7  lea      ecx, [rdx - 2]
003531CA  add      rsp, 0x28
003531CE  jmp      0x2e1c70  ; -> 002E1C70 fn
```

## 003535F0 (53 B, extent 003535F0-00353625)

Documented callee on this page: `002E2440`

```
003535F0  sub      rsp, 0x28
003535F4  mov      rcx, r9
003535F7  call     0x267e10  ; -> 00267E10 fn
003535FC  mov      edx, 1
00353601  mov      ecx, edx
00353603  call     0x2e2440  ; -> 002E2440 fn
00353608  mov      edx, 3
0035360D  xor      ecx, ecx
0035360F  call     0x2e1c40  ; -> 002E1C40 fn
00353614  mov      edx, 3
00353619  lea      ecx, [rdx - 2]
0035361C  add      rsp, 0x28
00353620  jmp      0x2e1c70  ; -> 002E1C70 fn
```

## 00353A60 (52 B, extent 00353A60-00353A94)

Documented callee on this page: `002E2400`

```
00353A60  sub      rsp, 0x28
00353A64  mov      rcx, r9
00353A67  call     0x267e10  ; -> 00267E10 fn
00353A6C  mov      ecx, 1
00353A71  call     0x2e2400  ; -> 002E2400 fn
00353A76  mov      edx, 3
00353A7B  lea      ecx, [rdx - 2]
00353A7E  call     0x2e1c40  ; -> 002E1C40 fn
00353A83  mov      edx, 3
00353A88  lea      ecx, [rdx - 2]
00353A8B  add      rsp, 0x28
00353A8F  jmp      0x2e1c70  ; -> 002E1C70 fn
```

## 00354300 (106 B, extent 00354300-0035436A)

Documented callee on this page: `002E2440`

```
00354300  push     rbx
00354302  sub      rsp, 0x20
00354306  movzx    ecx, byte ptr [rdx + 0x15]
0035430A  mov      rbx, r9
0035430D  call     0x267310  ; -> 00267310 fn
00354312  mov      rcx, rbx
00354315  test     eax, eax
00354317  je       0x354348  ; -> 00354348
00354319  call     0x267e10  ; -> 00267E10 fn
0035431E  mov      edx, 1
00354323  mov      ecx, edx
00354325  call     0x2e2440  ; -> 002E2440 fn
0035432A  mov      edx, 3
0035432F  xor      ecx, ecx
00354331  call     0x2e1c40  ; -> 002E1C40 fn
00354336  mov      edx, 3
0035433B  lea      ecx, [rdx - 2]
0035433E  add      rsp, 0x20
00354342  pop      rbx
00354343  jmp      0x2e1c70  ; -> 002E1C70 fn
00354348  call     0x267e10  ; -> 00267E10 fn
0035434D  mov      edx, 1
00354352  xor      ecx, ecx
00354354  call     0x2e2440  ; -> 002E2440 fn
00354359  mov      edx, 3
0035435E  xor      ecx, ecx
00354360  add      rsp, 0x20
00354364  pop      rbx
00354365  jmp      0x2e1c40  ; -> 002E1C40 fn
```

## 00354800 (101 B, extent 00354800-00354865)

Documented callee on this page: `002E2400`

```
00354800  push     rbx
00354802  sub      rsp, 0x20
00354806  movzx    ecx, byte ptr [rdx + 0x15]
0035480A  mov      rbx, r9
0035480D  call     0x267310  ; -> 00267310 fn
00354812  mov      rcx, rbx
00354815  test     eax, eax
00354817  je       0x354847  ; -> 00354847
00354819  call     0x267e10  ; -> 00267E10 fn
0035481E  mov      ecx, 1
00354823  call     0x2e2400  ; -> 002E2400 fn
00354828  mov      edx, 3
0035482D  lea      ecx, [rdx - 2]
00354830  call     0x2e1c40  ; -> 002E1C40 fn
00354835  mov      edx, 3
0035483A  lea      ecx, [rdx - 2]
0035483D  add      rsp, 0x20
00354841  pop      rbx
00354842  jmp      0x2e1c70  ; -> 002E1C70 fn
00354847  call     0x267e10  ; -> 00267E10 fn
0035484C  xor      ecx, ecx
0035484E  call     0x2e2400  ; -> 002E2400 fn
00354853  mov      edx, 3
00354858  lea      ecx, [rdx - 2]
0035485B  add      rsp, 0x20
0035485F  pop      rbx
00354860  jmp      0x2e1c40  ; -> 002E1C40 fn
```

## 0042D740 (88 B, extent 0042D740-0042D798)

Documented callee on this page: `003E55B0`

```
0042D740  push     rbx
0042D742  sub      rsp, 0x20
0042D746  mov      rbx, rdx
0042D749  call     0x3e55b0  ; -> 003E55B0 fn
0042D74E  mov      r8, rax
0042D751  test     rax, rax
0042D754  je       0x42d792  ; -> 0042D792
0042D756  mov      ecx, dword ptr [rbx + 0x5c]
0042D759  shl      ecx, 4
0042D75C  xor      ecx, dword ptr [rax + 0x244]
0042D762  and      ecx, 0x10
0042D765  xor      dword ptr [rax + 0x244], ecx
0042D76B  mov      ecx, dword ptr [rax + 0x244]
0042D771  mov      edx, dword ptr [rbx + 0x60]
0042D774  shl      edx, 5
0042D777  xor      edx, ecx
0042D779  and      edx, 0x20
0042D77C  xor      edx, ecx
0042D77E  mov      dword ptr [rax + 0x244], edx
0042D784  movzx    eax, byte ptr [rbx + 0x8c]
0042D78B  mov      byte ptr [r8 + 0xbc], al
0042D792  add      rsp, 0x20
0042D796  pop      rbx
0042D797  ret      
```
