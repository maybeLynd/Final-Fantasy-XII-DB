# Homing pack: `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`

Generated 2026-10-03 11:24 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h9-the-battle-unit-field-map.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0026B940 (46 B, extent 0026B940-0026B96E)

Entered from (direct sites whose caller this page cites): `00239370` + 0x4D (call; `00239370` is cited on this page)
Other direct sites: `00356390` + 0x1C (jmp)

Host context: "erior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*  | function | size | what the body does | interior anchors | |---|---|---|---| | '00239370' | 104 B | compares the floats 'xmm3', 'xmm2' and 'xmm1' with 0.0 in that order and, for each one not below 0.0 (comiss, so NaN also skips), calls with ('rcx', that float): '0026BB50' for 'xmm3', the call at '00239370' + 0x3D for '"

```
0026B940  movzx    edx, byte ptr [rcx + 3]
0026B944  shr      edx, 5
0026B947  sub      edx, 1
0026B94A  je       0x26b961  ; -> 0026B961
0026B94C  cmp      edx, 2
0026B94F  jne      0x26b96d  ; -> 0026B96D
0026B951  mov      rax, qword ptr [rcx + 0xb8]
0026B958  movss    dword ptr [rax + 0xbc], xmm1
0026B960  ret      
0026B961  mov      rax, qword ptr [rcx + 0xb8]
0026B968  movss    dword ptr [rax + 0x50], xmm1
0026B96D  ret      
```

## 0026BA00 (87 B, extent 0026BA00-0026BA57)

Entered from (direct sites whose caller this page cites): `00239370` + 0x3D (call; `00239370` is cited on this page)
Other direct sites: `0034CAC0` + 0x1F (call)

Host context: "erior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*  | function | size | what the body does | interior anchors | |---|---|---|---| | '00239370' | 104 B | compares the floats 'xmm3', 'xmm2' and 'xmm1' with 0.0 in that order and, for each one not below 0.0 (comiss, so NaN also skips), calls with ('rcx', that float): '0026BB50' for 'xmm3', the call at '00239370' + 0x3D for '"

```
0026BA00  movzx    edx, byte ptr [rcx + 3]
0026BA04  mov      r8, rcx
0026BA07  shr      edx, 5
0026BA0A  sub      edx, 1
0026BA0D  je       0x26ba37  ; -> 0026BA37
0026BA0F  cmp      edx, 2
0026BA12  jne      0x26ba4f  ; -> 0026BA4F
0026BA14  mov      rdx, qword ptr [rcx + 0xb8]
0026BA1B  xorps    xmm0, xmm0
0026BA1E  comiss   xmm0, xmm1
0026BA21  movss    dword ptr [rdx + 0xc8], xmm1
0026BA29  seta     al
0026BA2C  mov      byte ptr [rdx + 0xdd], al
0026BA32  jmp      0x268380  ; -> 00268380 fn
0026BA37  mov      rcx, qword ptr [rcx + 0xb8]
0026BA3E  xorps    xmm0, xmm0
0026BA41  comiss   xmm0, xmm1
0026BA44  movss    dword ptr [rcx + 0x68], xmm1
0026BA49  seta     al
0026BA4C  mov      byte ptr [rcx + 0x5c], al
0026BA4F  mov      rcx, r8
0026BA52  jmp      0x268380  ; -> 00268380 fn
```
