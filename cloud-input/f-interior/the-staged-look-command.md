# F-interior pack: `17-Presentation-Rendering/Character-Render-Records/the-staged-look-command.md`

Generated 2026-10-02 09:51 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-staged-look-command.json`.

Functions: 21. Each is cited on the page only at its entry and is still in the F frontier.

## 00372350 (84 B, extent 00372350-003723A4)

Page context: "tion 3 is an offset into that object) and the **eye object is slot '+0x28'** (request bits 27 to 29 go there).  'CharacterRender_RebindCombatLookAndSkeletonResources' ('003E3D70', 961 B; one caller, '00372350') shows the whole rig, because it resets every slot in turn:  | rig offset | reset called | what is known of the slot | |---|---|---| | '+0x00' | '0040F390', then '0040B5D0' with mode 1 (mode 4 when the global '02B59D64' is non-zer"

```
00372350  mov      qword ptr [rsp + 8], rbx
00372355  push     rdi
00372356  sub      rsp, 0x20
0037235A  cmp      dword ptr [rcx + 0x90], 0
00372361  mov      edi, edx
00372363  mov      rbx, rcx
00372366  jle      0x372399  ; -> 00372399
00372368  mov      ecx, dword ptr [rcx + 0x94]
0037236E  call     0x20e600  ; -> 0020E600 fn
00372373  test     rax, rax
00372376  je       0x372399  ; -> 00372399
00372378  mov      ecx, dword ptr [rbx + 0x94]
0037237E  call     0x20e600  ; -> 0020E600 fn
00372383  mov      dword ptr [rax + 0x68], edi
00372386  mov      ecx, dword ptr [rbx + 0x94]
0037238C  call     0x20e600  ; -> 0020E600 fn
00372391  mov      rcx, rax
00372394  call     0x3e3d70  ; -> 003E3D70 fn
00372399  mov      rbx, qword ptr [rsp + 0x30]
0037239E  add      rsp, 0x20
003723A2  pop      rdi
003723A3  ret      
```

## 003E0B20 (19 B, extent 003E0B20-003E0B33)

Page context: "h by branch, and matched to the builder that sets each bit:  | request bit | value / payload | what the applier does | staged by | |---|---|---|---| | 0 | bit 22 | '003E0910' '(controller, value)' | '003E0B20' - verb **'denybonephysical'** | | 1 | bit 23 | controller '+0x1C' bit 0 := value; value 1 calls 'RelationLook_SetAcceptedRelationState', value 0 'RelationLook_BeginNeutralReturn' - **look on / look off** | '003E33E0' | | 2 | bit 2"

```
003E0B20  shl      edx, 0x16
003E0B23  xor      edx, dword ptr [rcx]
003E0B25  and      edx, 0x400000
003E0B2B  xor      edx, dword ptr [rcx]
003E0B2D  or       edx, 1
003E0B30  mov      dword ptr [rcx], edx
003E0B32  ret      
```

## 003E2800 (7 B, extent 003E2800-003E2807)

Page context: " y, z)' | '003E29D0' - verb **'eyemove_381'** | | 28 | same | '003E28F0' | '003E29B0' - verb **'eyemovediff_383'** | | 29 | - | zeroes '+0x2C', '+0x14', '+0x18' of the object at controller '+0x28' | '003E2800' - verb **'eyemovereset'** | | 30 | bit 31 | '003E3720' '(controller, value)': bit 5 of controller '+0x1C' := value; if it is now up and bit 0 (look on) is down, 'RelationLook_BeginNeutralReturn' | '003E37A0' |  Bits 15 to 20 are o"

```
003E2800  or       dword ptr [rcx], 0x20000000
003E2806  ret      
```

## 003E29B0 (28 B, extent 003E29B0-003E29CC)

Page context: "ender_BeginRelationLookBlendWithMinimumDuration' | '003E33A0' | | 27 | floats '+0x40'..'+0x48' | '003E2810' '(controller, x, y, z)' | '003E29D0' - verb **'eyemove_381'** | | 28 | same | '003E28F0' | '003E29B0' - verb **'eyemovediff_383'** | | 29 | - | zeroes '+0x2C', '+0x14', '+0x18' of the object at controller '+0x28' | '003E2800' - verb **'eyemovereset'** | | 30 | bit 31 | '003E3720' '(controller, value)': bit 5 of controller '+0x1C' "

```
003E29B0  and      dword ptr [rcx], 0xf7ffffff
003E29B6  or       dword ptr [rcx], 0x10000000
003E29BC  movss    dword ptr [rcx + 0x40], xmm1
003E29C1  movss    dword ptr [rcx + 0x44], xmm2
003E29C6  movss    dword ptr [rcx + 0x48], xmm3
003E29CB  ret      
```

## 003E29D0 (28 B, extent 003E29D0-003E29EC)

Page context: "ntroller, frames)' | '003E33C0' | | 20 | float '+4' | 'CharacterRender_BeginRelationLookBlendWithMinimumDuration' | '003E33A0' | | 27 | floats '+0x40'..'+0x48' | '003E2810' '(controller, x, y, z)' | '003E29D0' - verb **'eyemove_381'** | | 28 | same | '003E28F0' | '003E29B0' - verb **'eyemovediff_383'** | | 29 | - | zeroes '+0x2C', '+0x14', '+0x18' of the object at controller '+0x28' | '003E2800' - verb **'eyemovereset'** | | 30 | bit 31"

```
003E29D0  mov      eax, dword ptr [rcx]
003E29D2  btr      eax, 0x1c
003E29D6  movss    dword ptr [rcx + 0x40], xmm1
003E29DB  bts      eax, 0x1b
003E29DF  movss    dword ptr [rcx + 0x44], xmm2
003E29E4  mov      dword ptr [rcx], eax
003E29E6  movss    dword ptr [rcx + 0x48], xmm3
003E29EB  ret      
```

## 003E30A0 (122 B, extent 003E30A0-003E311A)

Page context: "0x30' | controller '+0x50', '+0x54'; '+0x5C' := 1 | '003E36C0', the same two values as above | | 15 | floats '+4', '+8', '+0xC' | '003E2FD0' '(controller, frames, a, b)' | '003E31E0' | | 17 | same | '003E30A0' - the same, with a minimum duration | '003E3120' | | 16 | same | '003E3200' '(controller, frames, a, b)' | '003E3320' | | 18 | same | '003E3140' - the same as 16, with a minimum duration | '003E31C0' | | 19 | float '+4' | 'Charact"

```
003E30A0  mov      qword ptr [rsp + 8], rbx
003E30A5  push     rdi
003E30A6  sub      rsp, 0x50
003E30AA  movaps   xmmword ptr [rsp + 0x40], xmm6
003E30AF  mov      rbx, rcx
003E30B2  mov      ecx, dword ptr [rcx + 8]
003E30B5  movaps   xmm6, xmm3
003E30B8  movaps   xmmword ptr [rsp + 0x30], xmm7
003E30BD  movaps   xmm7, xmm2
003E30C0  movaps   xmmword ptr [rsp + 0x20], xmm8
003E30C6  movaps   xmm8, xmm1
003E30CA  call     0x20e600  ; -> 0020E600 fn
003E30CF  mov      ecx, dword ptr [rbx + 8]
003E30D2  mov      rdi, rax
003E30D5  call     0x20e600  ; -> 0020E600 fn
003E30DA  test     rax, rax
003E30DD  je       0x3e30ff  ; -> 003E30FF
003E30DF  movss    xmm1, dword ptr [rip + 0x1a1afd1]  ; -> 01DFE0B8 [f32 1]
003E30E7  movaps   xmm3, xmm6
003E30EA  mulss    xmm1, dword ptr [rdi + 0x18]
003E30EF  movaps   xmm2, xmm7
003E30F2  mov      rcx, rbx
003E30F5  maxss    xmm1, xmm8
003E30FA  call     0x3e2fd0  ; -> 003E2FD0 fn
003E30FF  mov      rbx, qword ptr [rsp + 0x60]
003E3104  movaps   xmm6, xmmword ptr [rsp + 0x40]
003E3109  movaps   xmm7, xmmword ptr [rsp + 0x30]
003E310E  movaps   xmm8, xmmword ptr [rsp + 0x20]
003E3114  add      rsp, 0x50
003E3118  pop      rdi
003E3119  ret      
```

## 003E3140 (122 B, extent 003E3140-003E31BA)

Page context: "ntroller, frames, a, b)' | '003E31E0' | | 17 | same | '003E30A0' - the same, with a minimum duration | '003E3120' | | 16 | same | '003E3200' '(controller, frames, a, b)' | '003E3320' | | 18 | same | '003E3140' - the same as 16, with a minimum duration | '003E31C0' | | 19 | float '+4' | 'CharacterRender_BeginRelationLookBlend(controller, frames)' | '003E33C0' | | 20 | float '+4' | 'CharacterRender_BeginRelationLookBlendWithMinimumDuratio"

```
003E3140  mov      qword ptr [rsp + 8], rbx
003E3145  push     rdi
003E3146  sub      rsp, 0x50
003E314A  movaps   xmmword ptr [rsp + 0x40], xmm6
003E314F  mov      rbx, rcx
003E3152  mov      ecx, dword ptr [rcx + 8]
003E3155  movaps   xmm6, xmm3
003E3158  movaps   xmmword ptr [rsp + 0x30], xmm7
003E315D  movaps   xmm7, xmm2
003E3160  movaps   xmmword ptr [rsp + 0x20], xmm8
003E3166  movaps   xmm8, xmm1
003E316A  call     0x20e600  ; -> 0020E600 fn
003E316F  mov      ecx, dword ptr [rbx + 8]
003E3172  mov      rdi, rax
003E3175  call     0x20e600  ; -> 0020E600 fn
003E317A  test     rax, rax
003E317D  je       0x3e319f  ; -> 003E319F
003E317F  movss    xmm1, dword ptr [rip + 0x1a1af31]  ; -> 01DFE0B8 [f32 1]
003E3187  movaps   xmm3, xmm6
003E318A  mulss    xmm1, dword ptr [rdi + 0x18]
003E318F  movaps   xmm2, xmm7
003E3192  mov      rcx, rbx
003E3195  maxss    xmm1, xmm8
003E319A  call     0x3e3200  ; -> 003E3200 fn
003E319F  mov      rbx, qword ptr [rsp + 0x60]
003E31A4  movaps   xmm6, xmmword ptr [rsp + 0x40]
003E31A9  movaps   xmm7, xmmword ptr [rsp + 0x30]
003E31AE  movaps   xmm8, xmmword ptr [rsp + 0x20]
003E31B4  add      rsp, 0x50
003E31B8  pop      rdi
003E31B9  ret      
```

## 003E33C0 (19 B, extent 003E33C0-003E33D3)

Page context: "er, frames, a, b)' | '003E3320' | | 18 | same | '003E3140' - the same as 16, with a minimum duration | '003E31C0' | | 19 | float '+4' | 'CharacterRender_BeginRelationLookBlend(controller, frames)' | '003E33C0' | | 20 | float '+4' | 'CharacterRender_BeginRelationLookBlendWithMinimumDuration' | '003E33A0' | | 27 | floats '+0x40'..'+0x48' | '003E2810' '(controller, x, y, z)' | '003E29D0' - verb **'eyemove_381'** | | 28 | same | '003E28F0' "

```
003E33C0  mov      eax, dword ptr [rcx]
003E33C2  and      eax, 0xffe87fff
003E33C7  movss    dword ptr [rcx + 4], xmm1
003E33CC  bts      eax, 0x13
003E33D0  mov      dword ptr [rcx], eax
003E33D2  ret      
```

## 003E3400 (57 B, extent 003E3400-003E3439)

Page context: "'RelationLook_BeginNeutralReturn' - **look on / look off** | '003E33E0' | | 2 | bit 24 | low nibble of controller '+0x1D' := value | '003E3440'. *The immediate, unstaged writer of the same nibble is '003E3400' (57 B, read whole 2026-09-19): it resolves the controller from the encoded pointer at '+8' of its first argument and replaces the nibble at once, doing nothing when the controller does not resolve* | | 4 | bit 26 | low nibble of c"

```
003E3400  mov      qword ptr [rsp + 8], rbx
003E3405  push     rdi
003E3406  sub      rsp, 0x20
003E340A  mov      rdi, rcx
003E340D  mov      ebx, edx
003E340F  mov      ecx, dword ptr [rcx + 8]
003E3412  call     0x20e600  ; -> 0020E600 fn
003E3417  test     rax, rax
003E341A  je       0x3e342e  ; -> 003E342E
003E341C  mov      ecx, dword ptr [rdi + 8]
003E341F  call     0x20e600  ; -> 0020E600 fn
003E3424  and      bl, 0xf
003E3427  and      byte ptr [rax + 0x1d], 0xf0
003E342B  or       byte ptr [rax + 0x1d], bl
003E342E  mov      rbx, qword ptr [rsp + 0x30]
003E3433  add      rsp, 0x20
003E3437  pop      rdi
003E3438  ret      
```

## 003E3570 (17 B, extent 003E3570-003E3581)

Page context: "t - and each of their builders clears the others. Bits 27 and 28 exclude each other the same way. Two builders stage bits the applier never tests: '003E36A0' (bit 7, floats at '+0x10' / '+0x14') and '003E3570' (bit 8, floats at '+0x18' / '+0x1C'), both called only from the bind path '002E28E0'; their reader, if any, is not this applier.  **The angle setters.** '003E2FD0' stores the two angles at controller '+0x50' / '+0x54' and sets bot"

```
003E3570  or       dword ptr [rcx], 0x100
003E3576  movss    dword ptr [rcx + 0x18], xmm1
003E357B  movss    dword ptr [rcx + 0x1c], xmm2
003E3580  ret      
```

## 003E36A0 (17 B, extent 003E36A0-003E36B1)

Page context: " the order 15, 17, 16, 18, 19, 20 and takes the first - and each of their builders clears the others. Bits 27 and 28 exclude each other the same way. Two builders stage bits the applier never tests: '003E36A0' (bit 7, floats at '+0x10' / '+0x14') and '003E3570' (bit 8, floats at '+0x18' / '+0x1C'), both called only from the bind path '002E28E0'; their reader, if any, is not this applier.  **The angle setters.** '003E2FD0' stores the two"

```
003E36A0  or       dword ptr [rcx], 0x80
003E36A6  movss    dword ptr [rcx + 0x10], xmm1
003E36AB  movss    dword ptr [rcx + 0x14], xmm2
003E36B0  ret      
```

## 003E36C0 (46 B, extent 003E36C0-003E36EE)

Page context: " three dwords at '+0x20' | controller '+0x60', '+0x64', '+0x68'; source kind '+0x6C' := 0 | '003E36F0' (bits only) | | 9 with 11 | two dwords at '+0x20' | controller '+0x60', '+0x64'; '+0x6C' := 1 | '003E36C0' - verb **'lookatsrcboneid'** | | 12 with 13 | three dwords at '+0x30' | controller '+0x50', '+0x54', '+0x58'; source kind '+0x5C' := 0 | '003E36F0' (bits only) | | 12 with 14 | two dwords at '+0x30' | controller '+0x50', '+0x54'; "

```
003E36C0  mov      eax, dword ptr [rcx]
003E36C2  test     edx, edx
003E36C4  jne      0x3e36da  ; -> 003E36DA
003E36C6  btr      eax, 0xa
003E36CA  mov      dword ptr [rcx + 0x20], r8d
003E36CE  or       eax, 0xa00
003E36D3  mov      dword ptr [rcx + 0x24], r9d
003E36D7  mov      dword ptr [rcx], eax
003E36D9  ret      
003E36DA  btr      eax, 0xd
003E36DE  mov      dword ptr [rcx + 0x30], r8d
003E36E2  or       eax, 0x5000
003E36E7  mov      dword ptr [rcx + 0x34], r9d
003E36EB  mov      dword ptr [rcx], eax
003E36ED  ret      
```

## 003E36F0 (48 B, extent 003E36F0-003E3720)

Page context: "*'_unlock'** | | 5 / 6 | - | controller '+0x8C' := 1 / := 0 | no builder among the eighteen | | 9 with 10 | three dwords at '+0x20' | controller '+0x60', '+0x64', '+0x68'; source kind '+0x6C' := 0 | '003E36F0' (bits only) | | 9 with 11 | two dwords at '+0x20' | controller '+0x60', '+0x64'; '+0x6C' := 1 | '003E36C0' - verb **'lookatsrcboneid'** | | 12 with 13 | three dwords at '+0x30' | controller '+0x50', '+0x54', '+0x58'; source kind '"

```
003E36F0  mov      eax, dword ptr [rcx]
003E36F2  test     edx, edx
003E36F4  jne      0x3e370b  ; -> 003E370B
003E36F6  or       eax, 0x600
003E36FB  btr      eax, 0xb
003E36FF  mov      dword ptr [rcx], eax
003E3701  movaps   xmm0, xmmword ptr [r8]
003E3705  movdqa   xmmword ptr [rcx + 0x20], xmm0
003E370A  ret      
003E370B  or       eax, 0x3000
003E3710  btr      eax, 0xe
003E3714  mov      dword ptr [rcx], eax
003E3716  movaps   xmm0, xmmword ptr [r8]
003E371A  movdqa   xmmword ptr [rcx + 0x30], xmm0
003E371F  ret      
```

## 003E3720 (115 B, extent 003E3720-003E3793)

Page context: "same | '003E28F0' | '003E29B0' - verb **'eyemovediff_383'** | | 29 | - | zeroes '+0x2C', '+0x14', '+0x18' of the object at controller '+0x28' | '003E2800' - verb **'eyemovereset'** | | 30 | bit 31 | '003E3720' '(controller, value)': bit 5 of controller '+0x1C' := value; if it is now up and bit 0 (look on) is down, 'RelationLook_BeginNeutralReturn' | '003E37A0' |  Bits 15 to 20 are one group - the applier tests them in the order 15, 17, "

```
003E3720  mov      qword ptr [rsp + 8], rbx
003E3725  mov      qword ptr [rsp + 0x10], rsi
003E372A  push     rdi
003E372B  sub      rsp, 0x20
003E372F  mov      rdi, rcx
003E3732  movzx    ebx, dx
003E3735  mov      ecx, dword ptr [rcx + 8]
003E3738  call     0x20e600  ; -> 0020E600 fn
003E373D  mov      ecx, dword ptr [rdi + 8]
003E3740  mov      rsi, rax
003E3743  call     0x20e600  ; -> 0020E600 fn
003E3748  test     rax, rax
003E374B  je       0x3e3783  ; -> 003E3783
003E374D  shl      bl, 5
003E3750  xor      bl, byte ptr [rsi + 0x1c]
003E3753  and      bl, 0x20
003E3756  xor      bl, byte ptr [rsi + 0x1c]
003E3759  mov      byte ptr [rsi + 0x1c], bl
003E375C  test     bl, 0x20
003E375F  je       0x3e3783  ; -> 003E3783
003E3761  test     bl, 1
003E3764  jne      0x3e3783  ; -> 003E3783
003E3766  mov      ecx, dword ptr [rdi + 8]
003E3769  call     0x20e600  ; -> 0020E600 fn
003E376E  test     rax, rax
003E3771  je       0x3e3783  ; -> 003E3783
003E3773  mov      ecx, dword ptr [rdi + 8]
003E3776  call     0x20e600  ; -> 0020E600 fn
003E377B  mov      rcx, rax
003E377E  call     0x513150  ; -> 00513150 fn
003E3783  mov      rbx, qword ptr [rsp + 0x30]
003E3788  mov      rsi, qword ptr [rsp + 0x38]
003E378D  add      rsp, 0x20
003E3791  pop      rdi
003E3792  ret      
```

## 003E37A0 (27 B, extent 003E37A0-003E37BB)

Page context: "' - verb **'eyemovereset'** | | 30 | bit 31 | '003E3720' '(controller, value)': bit 5 of controller '+0x1C' := value; if it is now up and bit 0 (look on) is down, 'RelationLook_BeginNeutralReturn' | '003E37A0' |  Bits 15 to 20 are one group - the applier tests them in the order 15, 17, 16, 18, 19, 20 and takes the first - and each of their builders clears the others. Bits 27 and 28 exclude each other the same way. Two builders stage bit"

```
003E37A0  mov      eax, dword ptr [rcx]
003E37A2  movzx    r8d, dx
003E37A6  and      eax, 0x3fffffff
003E37AB  shl      r8d, 0x1f
003E37AF  or       r8d, eax
003E37B2  bts      r8d, 0x1e
003E37B7  mov      dword ptr [rcx], r8d
003E37BA  ret      
```

## 003E37C0 (21 B, extent 003E37C0-003E37D5)

Page context: "om the encoded pointer at '+8' of its first argument and replaces the nibble at once, doing nothing when the controller does not resolve* | | 4 | bit 26 | low nibble of controller '+0x1E' := value | '003E37C0' - verbs **'lookat_maxangle_limit_lock'** / **'_unlock'** | | 5 / 6 | - | controller '+0x8C' := 1 / := 0 | no builder among the eighteen | | 9 with 10 | three dwords at '+0x20' | controller '+0x60', '+0x64', '+0x68'; source kind '+"

```
003E37C0  movzx    eax, dx
003E37C3  shl      eax, 0x1a
003E37C6  xor      eax, dword ptr [rcx]
003E37C8  and      eax, 0x4000000
003E37CD  xor      eax, dword ptr [rcx]
003E37CF  or       eax, 0x10
003E37D2  mov      dword ptr [rcx], eax
003E37D4  ret      
```

## 0042D970 (72 B, extent 0042D970-0042D9B8)

Page context: "entry does not resolve, in which case the record is skipped.) It does the same for the record's first child ('+8'), then walks that child's two chains ('+8' and '+0xA') depth-first with the callback '0042D970' (72 B: the same busy test, controller fetch and apply, taking the command from the owner passed in its context), so the same command reaches every record it visits. **An attached piece looks where its owner looks.**  **Clear.** '0"

```
0042D970  mov      qword ptr [rsp + 8], rbx
0042D975  push     rdi
0042D976  sub      rsp, 0x20
0042D97A  mov      rdi, rdx
0042D97D  mov      rbx, rcx
0042D980  mov      rdx, qword ptr [rdx + 8]
0042D984  call     0x426220  ; -> 00426220 fn
0042D989  test     eax, eax
0042D98B  jne      0x42d9ad  ; -> 0042D9AD
0042D98D  mov      rcx, rbx
0042D990  call     0x3e6da0  ; -> 003E6DA0 fn
0042D995  test     rax, rax
0042D998  je       0x42d9ad  ; -> 0042D9AD
0042D99A  mov      rdx, qword ptr [rdi + 8]
0042D99E  mov      rcx, rax
0042D9A1  add      rdx, 0x580
0042D9A8  call     0x3e37f0  ; -> 003E37F0 fn
0042D9AD  mov      rbx, qword ptr [rsp + 0x30]
0042D9B2  add      rsp, 0x20
0042D9B6  pop      rdi
0042D9B7  ret      
```

## 004712F0 (24 B, extent 004712F0-00471308)

Page context: "5B0' | - | | '+0x20' | '005173B0', then '00517590' | - | | '+0x24' | '005175F0' | - | | '+0x28' | '00518E60' | **the eye object** | | '+0x2C' | '00519730', then '00519870' | - | | '+0x30', '+0x34' | '004712F0', '004719F0' | - | | '+0x38' | '00519A30', then '0051A320' | **bone physics**, the other slot 'denybonephysical' restarts | | '+0x3C', '+0x40' | '00472820', '0051B870' | - |  *Named further 2026-09-19:* [the rig of seventeen contro"

```
004712F0  movups   xmm0, xmmword ptr [rip + 0x1a880f9]  ; -> 01EF93F0 [f32x4 0, 0, 0, 1]
004712F7  xor      eax, eax
004712F9  mov      word ptr [rcx + 2], ax
004712FD  movups   xmmword ptr [rcx + 0x20], xmm0
00471301  mov      byte ptr [rcx], al
00471303  mov      qword ptr [rcx + 0x18], rax
00471307  ret      
```

## 004715B0 (23 B, extent 004715B0-004715C7)

Page context: "al' restarts | | '+0x08' | 'RelationLook_ResetControllerState' | **the look controller** | | '+0x0C' | '00515DA0' | - | | '+0x14' | '0051AFD0', then '0051B110' | - | | '+0x18', '+0x1C' | '00471660', '004715B0' | - | | '+0x20' | '005173B0', then '00517590' | - | | '+0x24' | '005175F0' | - | | '+0x28' | '00518E60' | **the eye object** | | '+0x2C' | '00519730', then '00519870' | - | | '+0x30', '+0x34' | '004712F0', '004719F0' | - | | '+0x3"

```
004715B0  movups   xmm0, xmmword ptr [rip + 0x1a87e39]  ; -> 01EF93F0 [f32x4 0, 0, 0, 1]
004715B7  xor      eax, eax
004715B9  mov      word ptr [rcx], 0
004715BE  mov      qword ptr [rcx + 0x10], rax
004715C2  movups   xmmword ptr [rcx + 0x20], xmm0
004715C6  ret      
```

## 00471660 (49 B, extent 00471660-00471691)

Page context: "nybonephysical' restarts | | '+0x08' | 'RelationLook_ResetControllerState' | **the look controller** | | '+0x0C' | '00515DA0' | - | | '+0x14' | '0051AFD0', then '0051B110' | - | | '+0x18', '+0x1C' | '00471660', '004715B0' | - | | '+0x20' | '005173B0', then '00517590' | - | | '+0x24' | '005175F0' | - | | '+0x28' | '00518E60' | **the eye object** | | '+0x2C' | '00519730', then '00519870' | - | | '+0x30', '+0x34' | '004712F0', '004719F0' |"

```
00471660  movups   xmm0, xmmword ptr [rip + 0x1a87d89]  ; -> 01EF93F0 [f32x4 0, 0, 0, 1]
00471667  xor      eax, eax
00471669  mov      byte ptr [rcx + 3], 0
0047166D  mov      qword ptr [rcx + 0x14], rax
00471671  mov      dword ptr [rcx + 0x10], eax
00471674  movups   xmmword ptr [rcx + 0x20], xmm0
00471678  mov      word ptr [rcx], 0
0047167D  mov      dword ptr [rcx + 4], 0x3f800000
00471684  movzx    eax, byte ptr [rip + 0x1ab0d1d]  ; -> 01F223A8 [u8 0x1E]
0047168B  dec      al
0047168D  mov      byte ptr [rcx + 2], al
00471690  ret      
```

## 005175F0 (23 B, extent 005175F0-00517607)

Page context: " controller** | | '+0x0C' | '00515DA0' | - | | '+0x14' | '0051AFD0', then '0051B110' | - | | '+0x18', '+0x1C' | '00471660', '004715B0' | - | | '+0x20' | '005173B0', then '00517590' | - | | '+0x24' | '005175F0' | - | | '+0x28' | '00518E60' | **the eye object** | | '+0x2C' | '00519730', then '00519870' | - | | '+0x30', '+0x34' | '004712F0', '004719F0' | - | | '+0x38' | '00519A30', then '0051A320' | **bone physics**, the other slot 'denybo"

```
005175F0  and      byte ptr [rcx + 1], 0xf
005175F4  xor      eax, eax
005175F6  mov      dword ptr [rcx + 0x10], eax
005175F9  mov      dword ptr [rcx + 0x40], eax
005175FC  mov      dword ptr [rcx + 0x4c], eax
005175FF  mov      byte ptr [rcx + 2], 0
00517603  mov      byte ptr [rcx], 0
00517606  ret      
```
