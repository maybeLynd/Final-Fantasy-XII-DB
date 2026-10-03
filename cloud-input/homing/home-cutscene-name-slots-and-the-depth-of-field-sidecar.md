# Homing pack: `99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md`

Generated 2026-10-03 08:08 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-cutscene-name-slots-and-the-depth-of-field-sidecar.json`.

Bodies: 8. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002E4FE0 (74 B, extent 002E4FE0-002E502A)

Entered from (direct sites whose caller this page cites): `003490F0` + 0x50 (jmp; `003490F0` is cited on this page)
Other direct sites: none

Host context: "0348A90' + 0x40 with it and 'maxss(0.0, a)' in 'xmm1' | Interior anchor '00348AAC'; Interior anchor '00348ABC'; Interior anchor '00348AC4'; Interior anchor '00348ACC'; Interior anchor '00348AD0' | | '003490F0' | 85 B | takes float 'a' from the call at '003490F0' + 0x11 (with 'rcx' = 'r9') and 'id' = '00267E10(r9)', calls '0016D6A0(id)', takes 'P' = '003EB720(id)' without a null check, multiplies 'a' by the float returned by the call at "

```
002E4FE0  sub      rsp, 0x28
002E4FE4  test     rcx, rcx
002E4FE7  je       0x2e5023  ; -> 002E5023
002E4FE9  cmp      dword ptr [rcx], -1
002E4FEC  je       0x2e5023  ; -> 002E5023
002E4FEE  movzx    eax, word ptr [rcx]
002E4FF1  cmp      ax, -1
002E4FF5  je       0x2e5019  ; -> 002E5019
002E4FF7  movsx    rax, ax
002E4FFB  imul     rcx, rax, 0x740
002E5002  add      rcx, qword ptr [rip + 0x1fe1f1f]  ; -> 022C6F28
002E5009  je       0x2e5019  ; -> 002E5019
002E500B  cmp      dword ptr [rcx + 0x284], 0
002E5012  je       0x2e5019  ; -> 002E5019
002E5014  call     0x427300  ; -> 00427300 fn
002E5019  mov      eax, 1
002E501E  add      rsp, 0x28
002E5022  ret      
002E5023  xor      eax, eax
002E5025  add      rsp, 0x28
002E5029  ret      
```

## 002E95B0 (66 B, extent 002E95B0-002E95F2)

Entered from (direct sites whose caller this page cites): `003490F0` + 0x37 (call; `003490F0` is cited on this page)
Other direct sites: `003DD980` + 0x3E (call)

Host context: "0348A90' + 0x40 with it and 'maxss(0.0, a)' in 'xmm1' | Interior anchor '00348AAC'; Interior anchor '00348ABC'; Interior anchor '00348AC4'; Interior anchor '00348ACC'; Interior anchor '00348AD0' | | '003490F0' | 85 B | takes float 'a' from the call at '003490F0' + 0x11 (with 'rcx' = 'r9') and 'id' = '00267E10(r9)', calls '0016D6A0(id)', takes 'P' = '003EB720(id)' without a null check, multiplies 'a' by the float returned by the call at "

```
002E95B0  test     rcx, rcx
002E95B3  je       0x2e95ee  ; -> 002E95EE
002E95B5  cmp      dword ptr [rcx], -1
002E95B8  je       0x2e95ee  ; -> 002E95EE
002E95BA  movzx    eax, word ptr [rcx]
002E95BD  cmp      ax, -1
002E95C1  jne      0x2e95cc  ; -> 002E95CC
002E95C3  movss    xmm0, dword ptr [rip + 0x60f7b5]  ; -> 008F8D80 [f32 30]
002E95CB  ret      
002E95CC  movsx    rax, ax
002E95D0  imul     rcx, rax, 0x740
002E95D7  add      rcx, qword ptr [rip + 0x1fdd94a]  ; -> 022C6F28
002E95DE  je       0x2e95c3  ; -> 002E95C3
002E95E0  cmp      dword ptr [rcx + 0x284], 0
002E95E7  je       0x2e95c3  ; -> 002E95C3
002E95E9  jmp      0x423280  ; -> 00423280 fn
002E95EE  xorps    xmm0, xmm0
002E95F1  ret      
```

## 002EC630 (74 B, extent 002EC630-002EC67A)

Entered from (direct sites whose caller this page cites): `003498D0` + 0x31 (jmp; `003498D0` is cited on this page)
Other direct sites: none

Host context: ", and tail-jumps at '00349460' + 0x26 with 'rcx' = '003EB720(id)' (no null check) | Interior anchor '00349469'; Interior anchor '00349472'; Interior anchor '00349479'; Interior anchor '00349486' | | '003498D0' | 54 B | takes 'id' = '00267E10(r9)', calls '0016D6A0(id)', takes 'P' = '003EB720(id)' without a null check, passes 'P' to the call at '003498D0' + 0x24, then tail-jumps at '003498D0' + 0x31 with 'rcx' = 'P' | Interior anchor '003"

```
002EC630  sub      rsp, 0x28
002EC634  test     rcx, rcx
002EC637  je       0x2ec673  ; -> 002EC673
002EC639  cmp      dword ptr [rcx], -1
002EC63C  je       0x2ec673  ; -> 002EC673
002EC63E  movzx    eax, word ptr [rcx]
002EC641  cmp      ax, -1
002EC645  je       0x2ec669  ; -> 002EC669
002EC647  movsx    rax, ax
002EC64B  imul     rcx, rax, 0x740
002EC652  add      rcx, qword ptr [rip + 0x1fda8cf]  ; -> 022C6F28
002EC659  je       0x2ec669  ; -> 002EC669
002EC65B  cmp      dword ptr [rcx + 0x284], 0
002EC662  je       0x2ec669  ; -> 002EC669
002EC664  call     0x426e20  ; -> 00426E20 fn
002EC669  mov      eax, 1
002EC66E  add      rsp, 0x28
002EC672  ret      
002EC673  xor      eax, eax
002EC675  add      rsp, 0x28
002EC679  ret      
```

## 002EC890 (26 B, extent 002EC890-002EC8AA)

Entered from (direct sites whose caller this page cites): `0034C900` + 0x39 (call; `0034C900` is cited on this page)
Other direct sites: none

Host context: "the site at '0034BF40' + 0x39 with it and 'edx' = 'v' | Interior anchor '0034BF50'; Interior anchor '0034BF5A'; Interior anchor '0034BF6A'; Interior anchor '0034BF72'; Interior anchor '0034BF79' | | '0034C900' | 73 B | calls '00267E10(r9)' twice, keeping the first result 'v' and the second 'id', calls '0016D6A0(id)' and '003EB720(id)', and only when that result is non-null calls the site at '0034C900' + 0x39 with it and 'edx' = 'v' | In"

```
002EC890  test     rcx, rcx
002EC893  je       0x2ec8a9  ; -> 002EC8A9
002EC895  cmp      dword ptr [rcx], -1
002EC898  je       0x2ec8a9  ; -> 002EC8A9
002EC89A  and      byte ptr [rcx + 0x11], 0xf7
002EC89E  test     edx, edx
002EC8A0  setne    al
002EC8A3  shl      al, 3
002EC8A6  or       byte ptr [rcx + 0x11], al
002EC8A9  ret      
```

## 002EC900 (54 B, extent 002EC900-002EC936)

Entered from (direct sites whose caller this page cites): `00348580` + 0x6C (call; `00348580` is cited on this page)
Other direct sites: none

Host context: "at '0034A290' + 0x2B with 'rcx' = 'rdx' and 'edx' = 2 | Interior anchor '0034A299'; Interior anchor '0034A2A1'; Interior anchor '0034A2A9'; Interior anchor '0034A2AE'; Interior anchor '0034A2BB' | | '00348580' | 129 B | takes floats 'a' and 'b' from the calls at '00348580' + 0x16 and '00348580' + 0x21 (each with 'rcx' = 'r9') and 'id' = '00267E10(r9)', calls '0016D6A0(id)' and '003EB720(id)', and returns at once when that result 'P' is "

```
002EC900  push     rbx
002EC902  sub      rsp, 0x20
002EC906  xorps    xmm0, xmm0
002EC909  mov      rbx, rcx
002EC90C  comiss   xmm1, xmm0
002EC90F  jbe      0x2ec921  ; -> 002EC921
002EC911  cvttss2si ecx, xmm1
002EC915  call     0x3da190  ; -> 003DA190 fn
002EC91A  movd     xmm1, eax
002EC91E  cvtdq2ps xmm1, xmm1
002EC921  test     rbx, rbx
002EC924  je       0x2ec930  ; -> 002EC930
002EC926  cmp      dword ptr [rbx], -1
002EC929  je       0x2ec930  ; -> 002EC930
002EC92B  movss    dword ptr [rbx + 0x1c], xmm1
002EC930  add      rsp, 0x20
002EC934  pop      rbx
002EC935  ret      
```

## 002EC9C0 (54 B, extent 002EC9C0-002EC9F6)

Entered from (direct sites whose caller this page cites): `00348580` + 0x61 (call; `00348580` is cited on this page)
Other direct sites: none

Host context: "at '0034A290' + 0x2B with 'rcx' = 'rdx' and 'edx' = 2 | Interior anchor '0034A299'; Interior anchor '0034A2A1'; Interior anchor '0034A2A9'; Interior anchor '0034A2AE'; Interior anchor '0034A2BB' | | '00348580' | 129 B | takes floats 'a' and 'b' from the calls at '00348580' + 0x16 and '00348580' + 0x21 (each with 'rcx' = 'r9') and 'id' = '00267E10(r9)', calls '0016D6A0(id)' and '003EB720(id)', and returns at once when that result 'P' is "

```
002EC9C0  push     rbx
002EC9C2  sub      rsp, 0x20
002EC9C6  xorps    xmm0, xmm0
002EC9C9  mov      rbx, rcx
002EC9CC  comiss   xmm1, xmm0
002EC9CF  jbe      0x2ec9e1  ; -> 002EC9E1
002EC9D1  cvttss2si ecx, xmm1
002EC9D5  call     0x3da190  ; -> 003DA190 fn
002EC9DA  movd     xmm1, eax
002EC9DE  cvtdq2ps xmm1, xmm1
002EC9E1  test     rbx, rbx
002EC9E4  je       0x2ec9f0  ; -> 002EC9F0
002EC9E6  cmp      dword ptr [rbx], -1
002EC9E9  je       0x2ec9f0  ; -> 002EC9F0
002EC9EB  movss    dword ptr [rbx + 0x18], xmm1
002EC9F0  add      rsp, 0x20
002EC9F4  pop      rbx
002EC9F5  ret      
```

## 002ECCB0 (54 B, extent 002ECCB0-002ECCE6)

Entered from (direct sites whose caller this page cites): `00348A90` + 0x40 (call; `00348A90` is cited on this page)
Other direct sites: none

Host context: "ite at '00348580' + 0x6C with 'P' and 'a' (in 'xmm1') | Interior anchor '003485AC'; Interior anchor '003485BC'; Interior anchor '003485C7'; Interior anchor '003485D4'; Interior anchor '003485EC' | | '00348A90' | 80 B | takes float 'a' from the call at '00348A90' + 0x11 (with 'rcx' = 'r9') and 'id' = '00267E10(r9)', calls '0016D6A0(id)' and '003EB720(id)', and only when that result is non-null calls the site at '00348A90' + 0x40 with it "

```
002ECCB0  push     rbx
002ECCB2  sub      rsp, 0x20
002ECCB6  xorps    xmm0, xmm0
002ECCB9  mov      rbx, rcx
002ECCBC  comiss   xmm1, xmm0
002ECCBF  jbe      0x2eccd1  ; -> 002ECCD1
002ECCC1  cvttss2si ecx, xmm1
002ECCC5  call     0x3da190  ; -> 003DA190 fn
002ECCCA  movd     xmm1, eax
002ECCCE  cvtdq2ps xmm1, xmm1
002ECCD1  test     rbx, rbx
002ECCD4  je       0x2ecce0  ; -> 002ECCE0
002ECCD6  cmp      dword ptr [rbx], -1
002ECCD9  je       0x2ecce0  ; -> 002ECCE0
002ECCDB  movss    dword ptr [rbx + 0x14], xmm1
002ECCE0  add      rsp, 0x20
002ECCE4  pop      rbx
002ECCE5  ret      
```

## 002ED3F0 (53 B, extent 002ED3F0-002ED425)

Entered from (direct sites whose caller this page cites): `0034B0A0` + 0x3E (jmp; `0034B0A0` is cited on this page); `0034B710` + 0x4B (jmp; `0034B710` is cited on this page); `0034BAB0` + 0x48 (jmp; `0034BAB0` is cited on this page)
Other direct sites: none

Host context: "then tail-jumps at '003498D0' + 0x31 with 'rcx' = 'P' | Interior anchor '003498D9'; Interior anchor '003498E2'; Interior anchor '003498E9'; Interior anchor '003498F4'; Interior anchor '00349901' | | '0034B0A0' | 67 B | calls '00267E10(r9)' twice, keeping the first result 'v' and the second 'id', calls '0016D6A0(id)' and tail-jumps at '0034B0A0' + 0x3E with 'rcx' = '003EB720(id)' (no null check) and 'edx' = 'v' | Interior anchor '0034B0B" / "rcx' = '003EB720(id)' (no null check) and 'edx' = 'v' | Interior anchor '0034B0B0'; Interior anchor '0034B0BA'; Interior anchor '0034B0C3'; Interior anchor '0034B0CA'; Interior anchor '0034B0DE' | | '0034B710' | 80 B | calls '00267F90(r9, 1)', then calls '00267E10(r9)' twice, keeping the first result 'v' and the second 'id', calls '0016D6A0(id)' and tail-jumps at '0034B710' + 0x4B with 'rcx' = '003EB720(id)' (no null check) and 'edx' = "

```
002ED3F0  test     rcx, rcx
002ED3F3  je       0x2ed424  ; -> 002ED424
002ED3F5  cmp      dword ptr [rcx], -1
002ED3F8  je       0x2ed424  ; -> 002ED424
002ED3FA  movzx    eax, word ptr [rcx]
002ED3FD  cmp      ax, -1
002ED401  je       0x2ed424  ; -> 002ED424
002ED403  movsx    rax, ax
002ED407  imul     rcx, rax, 0x740
002ED40E  add      rcx, qword ptr [rip + 0x1fd9b13]  ; -> 022C6F28
002ED415  je       0x2ed424  ; -> 002ED424
002ED417  cmp      dword ptr [rcx + 0x284], 0
002ED41E  jne      0x429020  ; -> 00429020 fn
002ED424  ret      
```
