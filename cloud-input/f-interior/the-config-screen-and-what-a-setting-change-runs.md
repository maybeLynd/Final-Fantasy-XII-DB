# F-interior pack: `16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md`

Generated 2026-10-02 18:33 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-config-screen-and-what-a-setting-change-runs.json`.

Functions: 7. Each is cited on the page only at its entry and is still in the F frontier.

## 0017E050 (25 B, extent 0017E050-0017E069)

Page context: "4'–'0023E24E'). The screen forwards that to child 5, so the   size row re-reads its value ('0023C4A2'–'0023C4C7'). - Kinds '0x27' and '0x28' on '0x8100' write the settings file ('0017E530') and call '0017E050'; they post   nothing to the row.  While a kind-5 row has a pending change, message 10 also passes a pending flag of 1 to the cursor routine '00240DE0' ('0023C243'–'0023C27F'). What that flag does to cursor movement is not read her"

```
0017E050  mov      rcx, qword ptr [rip + 0x2d271f1]  ; -> 02EA5248
0017E057  xor      r9d, r9d
0017E05A  lea      edx, [r9 + 0x10]
0017E05E  lea      r8d, [r9 + 4]
0017E062  jmp      qword ptr [rip + 0x7447b7]  ; -> 008C2820 [u64 0x0000000001CCC7CE]
```

## 0024C600 (56 B, extent 0024C600-0024C638)

Page context: "89340 & 0x10' flag-gate the arms, 'byte[rax+4]' seeds the step, '0030A880', '003590D0', '003588B0', '00263E30', '0031B770' x2, '00313F60' x4, '003003F0' x2, '00311F70', '00236850' x2, '00236820' and '0024C600' drive the rebuild - the setting-change path's flagged worker; its '00263E30', '00236820'/'00236850', '00313F60' and '00311F70' helpers are shared with Combat-, Spawn_Encounter_Lifecycle- and Status_Periodic_Terminal-side callers. "

```
0024C600  test     ecx, ecx
0024C602  je       0x24c637  ; -> 0024C637
0024C604  mov      qword ptr [rsp + 8], rbx
0024C609  push     rdi
0024C60A  sub      rsp, 0x20
0024C60E  mov      ebx, edx
0024C610  mov      edi, ecx
0024C612  test     edx, edx
0024C614  je       0x24c62d  ; -> 0024C62D
0024C616  call     0x2fbfa0  ; -> 002FBFA0 fn
0024C61B  mov      edx, ebx
0024C61D  mov      ecx, edi
0024C61F  call     0x3b0190  ; -> 003B0190 fn
0024C624  mov      edx, ebx
0024C626  mov      ecx, edi
0024C628  call     0x3b14f0  ; -> 003B14F0 fn
0024C62D  mov      rbx, qword ptr [rsp + 0x30]
0024C632  add      rsp, 0x20
0024C636  pop      rdi
0024C637  ret      
```

## 002726C0 (79 B, extent 002726C0-0027270F)

Page context: "dy - '00246AD0' single call plus '02B62D88'. Interior anchor '004060E5' (a '00246AD0' call).  ## SWE2-EC7-55 update (2026-09-19) - '002973E0'  '002973E0' (247 B) is a config-screen body - '00271960'/'002726C0'/'00272730'/'002727C0'. Interior anchor '00297414' (a '00271960' call).  ## SWE2-EC7-56 update (2026-09-19) - '002413E0'  '002413E0' (197 B) is a config-screen body - '002D3BA0'/'002D45C0' plus one vcall. Interior anchor '00241408'"

```
002726C0  shl      edx, 4
002726C3  mov      dword ptr [rcx], edx
002726C5  shl      r8d, 4
002726C9  mov      dword ptr [rcx + 4], r8d
002726CD  sub      r8d, edx
002726D0  movsxd   r10, r8d
002726D3  movsxd   rax, r9d
002726D6  imul     rax, r10
002726DA  sar      rax, 8
002726DE  add      eax, edx
002726E0  mov      dword ptr [rcx + 8], eax
002726E3  movsxd   rax, dword ptr [rsp + 0x28]
002726E8  imul     rax, r10
002726EC  sar      rax, 8
002726F0  add      eax, dword ptr [rcx]
002726F2  mov      dword ptr [rcx + 0xc], eax
002726F5  movsxd   rax, dword ptr [rsp + 0x30]
002726FA  imul     rax, r10
002726FE  sar      rax, 8
00272702  add      eax, dword ptr [rcx]
00272704  mov      dword ptr [rcx + 0x10], eax
00272707  mov      dword ptr [rcx + 0x14], 0x400
0027270E  ret      
```

## 002727C0 (39 B, extent 002727C0-002727E7)

Page context: " call plus '02B62D88'. Interior anchor '004060E5' (a '00246AD0' call).  ## SWE2-EC7-55 update (2026-09-19) - '002973E0'  '002973E0' (247 B) is a config-screen body - '00271960'/'002726C0'/'00272730'/'002727C0'. Interior anchor '00297414' (a '00271960' call).  ## SWE2-EC7-56 update (2026-09-19) - '002413E0'  '002413E0' (197 B) is a config-screen body - '002D3BA0'/'002D45C0' plus one vcall. Interior anchor '00241408' (a '002D45C0' call). "

```
002727C0  test     edx, edx
002727C2  mov      r9d, 1
002727C8  mov      r8d, r9d
002727CB  mov      eax, 0x400
002727D0  cmovg    r8d, edx
002727D4  cdq      
002727D5  idiv     r8d
002727D8  mov      word ptr [rcx + 0x16], ax
002727DC  test     ax, ax
002727DF  jne      0x2727e6  ; -> 002727E6
002727E1  mov      word ptr [rcx + 0x16], r9w
002727E6  ret      
```

## 0029B790 (57 B, extent 0029B790-0029B7C9)

Page context: "7); this line printed 1,325 B, a wrong literal in the batch-33 append — the body is 1,304 B per the function list*) is the gambit-adjacent screen driver - '0035BB60'/'002DD7E0'/'00247930'/'0035BB00'/'0029B790'/'002973E0' plus the '00861F0E' trig call. Interior anchor '0029AA96' (a '002DD7E0' call).  ## SWE2-EC7-33 update (2026-09-19) - '003FB3E0'  '003FB3E0' (**1,292 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,134 B, a w"

```
0029B790  sub      rsp, 0x28
0029B794  mov      rax, qword ptr [rcx + 0xb20]
0029B79B  test     rax, rax
0029B79E  jne      0x29b7aa  ; -> 0029B7AA
0029B7A0  mov      eax, 1
0029B7A5  add      rsp, 0x28
0029B7A9  ret      
0029B7AA  movsx    r9d, byte ptr [rcx + 0xb48]
0029B7B2  mov      rcx, qword ptr [rcx + 0xb30]
0029B7B9  call     rax
0029B7BB  xor      ecx, ecx
0029B7BD  test     eax, eax
0029B7BF  setne    cl
0029B7C2  mov      eax, ecx
0029B7C4  add      rsp, 0x28
0029B7C8  ret      
```

## 002CD8A0 (81 B, extent 002CD8A0-002CD8F1)

Page context: "'[+0]' — a request id in '0x4B3'–'0x53A' — is dispatched through a second byte-mapped table ('00281111'–'00281125', map '00281458', RVA table '0028144C') that ends by writing '+0xC0 = 3' ('002CDE20'/'002CD8A0'/'002CE2F0' path, '00281127'–'0028114B') or '+0xC0 = 1' ('0028114D').  **'+0xC0' is the state dword of '00281ED0'** (1697 B — all accesses are 32-bit: 'mov eax, dword[rcx+0xC0]' at '00281ED7', 'mov dword[…+0xC0], 3/1' on the arms),"

```
002CD8A0  add      ecx, 0xfffffb4d
002CD8A6  cmp      ecx, 9
002CD8A9  ja       0x2cd8eb  ; -> 002CD8EB
002CD8AB  movsxd   rax, ecx
002CD8AE  lea      rdx, [rip - 0x1ad8b5]  ; -> 00120000 (image base)
002CD8B5  mov      ecx, dword ptr [rdx + rax*4 + 0x1ad8f4]  ; image base + 0x1ad8f4 = 002CD8F4
002CD8BC  add      rcx, rdx
002CD8BF  jmp      rcx
002CD8C1  mov      eax, 0x11
002CD8C6  ret      
002CD8C7  mov      eax, 0x12
002CD8CC  ret      
002CD8CD  mov      eax, 0x13
002CD8D2  ret      
002CD8D3  mov      eax, 0x14
002CD8D8  ret      
002CD8D9  mov      eax, 0x15
002CD8DE  ret      
002CD8DF  mov      eax, 0x16
002CD8E4  ret      
002CD8E5  mov      eax, 0x17
002CD8EA  ret      
002CD8EB  mov      eax, 0x10
002CD8F0  ret      
```

## 00408190 (100 B, extent 00408190-004081F4)

Page context: "00000' tail record lands at 'r8 + ((n + 6) << 4)', and the return is the block's '+0x10'-biased length  Interior anchor '003F5C72' (function '003F5BE0').  '00407150' (233 B) is the bit-1 flag setter '00408190'/'004088A0'/'004088B0' call on the row object: 'dword[rcx+0xC8]' bit 1 is compared against 'edx' and xor-replaced only when it differs; the child 'rbx = [rcx+0xC0]' then either (a) when 'byte[+0xC0]' is clear, commits '+0x118' into"

```
00408190  mov      qword ptr [rsp + 8], rbx
00408195  push     rdi
00408196  sub      rsp, 0x20
0040819A  mov      rcx, qword ptr [rip + 0x275abdf]  ; -> 02B62D80
004081A1  xor      edi, edi
004081A3  test     rcx, rcx
004081A6  je       0x4081b1  ; -> 004081B1
004081A8  mov      rbx, qword ptr [rcx + 0xc0]
004081AF  jmp      0x4081b4  ; -> 004081B4
004081B1  mov      rbx, rdi
004081B4  xor      edx, edx
004081B6  call     0x407150  ; -> 00407150 fn
004081BB  test     rbx, rbx
004081BE  je       0x4081e9  ; -> 004081E9
004081C0  mov      rax, qword ptr [rip + 0x275abb9]  ; -> 02B62D80
004081C7  test     rax, rax
004081CA  je       0x4081d3  ; -> 004081D3
004081CC  mov      rdi, qword ptr [rax + 0xc0]
004081D3  mov      rcx, rdi
004081D6  call     0x244dd0  ; -> 00244DD0 fn
004081DB  and      dword ptr [rbx + 0xd8], 0xfffffffb
004081E2  or       dword ptr [rbx + 0xd8], 8
004081E9  mov      rbx, qword ptr [rsp + 0x30]
004081EE  add      rsp, 0x20
004081F2  pop      rdi
004081F3  ret      
```
