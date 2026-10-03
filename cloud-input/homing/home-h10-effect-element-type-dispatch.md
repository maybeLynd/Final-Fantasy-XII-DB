# Homing pack: `17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-effect-element-type-dispatch.json`.

Bodies: 6. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00265380 (14 B, extent 00265380-0026538E)

Entered from (direct sites whose caller this page cites): `0034C630` + 0x4F (call; `0034C630` is cited on this page)
Other direct sites: `0034B350` + 0x38 (call)

Host context: "rwise it tail-jumps (at '00343E20' + 0x1e) with 'rcx' = that result and 'edx' = 0 | Interior anchor '00343E24'; Interior anchor '00343E2B'; Interior anchor '00343E33'; Interior anchor '00343E3E' | | '0034C630' | 111 B | calls '002640C0' with the incoming registers unchanged (result 'P'), calls '00267E10(r9)' twice (results 'a' then 'b') and '00358940(P, b)'; when that returns non-null it stores the result of the call at '0034C630' + 0x4"

```
00265380  cmp      byte ptr [rdx + 0x18], 1
00265384  jne      0x265389  ; -> 00265389
00265386  xor      eax, eax
00265388  ret      
00265389  jmp      0x2652d0  ; -> 002652D0 fn
```

## 00290840 (126 B, extent 00290840-002908BE)

Entered from (direct sites whose caller this page cites): `00473B30` + 0xF (jmp; `00473B30` is cited on this page)
Other direct sites: none

Host context: "'0x2' of dword '[rcx]'; a non-null result is returned | Interior anchor '0046E95F'; Interior anchor '0046E967'; Interior anchor '0046E974'; Interior anchor '0046E977'; Interior anchor '0046E97B' | | '00473B30' | 20 B | calls '003589B0' with the incoming registers unchanged and tail-jumps (at '00473B30' + 0xf) with 'ecx' = its dword result | Interior anchor '00473B34'; Interior anchor '00473B39'; Interior anchor '00473B3F' | "

```
00290840  mov      rdx, qword ptr [rip + 0x1e0b639]  ; -> 0209BE80
00290847  test     rdx, rdx
0029084A  jne      0x290852  ; -> 00290852
0029084C  mov      eax, 1
00290851  ret      
00290852  mov      r8d, dword ptr [rdx + 0x10f68]
00290859  test     r8b, 0x20
0029085D  jne      0x29084c  ; -> 0029084C
0029085F  mov      rax, qword ptr [rdx + 0x10f10]
00290866  test     rax, rax
00290869  je       0x2908b1  ; -> 002908B1
0029086B  nop      dword ptr [rax + rax]
00290870  cmp      dword ptr [rax + 0x810], ecx
00290876  je       0x290891  ; -> 00290891
00290878  mov      rax, qword ptr [rax + 0x868]
0029087F  test     rax, rax
00290882  jne      0x290870  ; -> 00290870
00290884  mov      eax, dword ptr [rdx + 0x10f68]
0029088A  shr      eax, 5
0029088D  and      eax, 1
00290890  ret      
00290891  movzx    ecx, word ptr [rax + 0x842]
00290898  shr      ecx, 3
0029089B  xor      ecx, r8d
0029089E  and      ecx, 0x20
002908A1  xor      ecx, r8d
002908A4  mov      dword ptr [rdx + 0x10f68], ecx
002908AA  mov      rdx, qword ptr [rip + 0x1e0b5cf]  ; -> 0209BE80
002908B1  mov      eax, dword ptr [rdx + 0x10f68]
002908B7  shr      eax, 5
002908BA  and      eax, 1
002908BD  ret      
```

## 003A7AE0 (112 B, extent 003A7AE0-003A7B50)

Entered from (direct sites whose caller this page cites): `003ED8A0` + 0x167 (call; `003ED8A0` is cited on this page)
Other direct sites: none

Host context: "–'00538939'). '003A9A70' writes that byte and then calls it ('003A9A8F', '003A9AAD'). Its other callers are '003A99F0' (after a 'memcpy') and '003A9BA0', reached from the EFX data parse '003EDAD0' / '003ED8A0' and from ~~instance creation~~ the context rebase arms of the per-frame effect pass '0024D540' ('0024D540'+0x114) and of '0024D970' ('0024D970'+0x26), which pass the relocation delta *(corrected 2026-10-02, OPUS: '003A9BA0' adds t"

```
003A7AE0  mov      qword ptr [rsp + 8], rbx
003A7AE5  mov      qword ptr [rsp + 0x10], rbp
003A7AEA  mov      qword ptr [rsp + 0x18], rsi
003A7AEF  push     rdi
003A7AF0  sub      rsp, 0x20
003A7AF4  movzx    esi, byte ptr [rcx + 1]
003A7AF8  mov      rdi, rcx
003A7AFB  movzx    ecx, byte ptr [rcx]
003A7AFE  movsxd   rbp, edx
003A7B01  call     0x3a78a0  ; -> 003A78A0 fn
003A7B06  test     rax, rax
003A7B09  je       0x3a7b39  ; -> 003A7B39
003A7B0B  movzx    edx, sil
003A7B0F  mov      rcx, rax
003A7B12  call     0x334000  ; -> 00334000 fn
003A7B17  test     rax, rax
003A7B1A  je       0x3a7b39  ; -> 003A7B39
003A7B1C  mov      ecx, dword ptr [rdi + 4]
003A7B1F  lea      rdx, [rdi + 8]
003A7B23  mov      dword ptr [rax], ecx
003A7B25  lea      rcx, [rax + 4]
003A7B29  movzx    r8d, byte ptr [rax + 2]
003A7B2E  call     0x861eba  ; -> 00861EBA fn
003A7B33  lea      rax, [rdi + rbp]
003A7B37  jmp      0x3a7b3b  ; -> 003A7B3B
003A7B39  xor      eax, eax
003A7B3B  mov      rbx, qword ptr [rsp + 0x30]
003A7B40  mov      rbp, qword ptr [rsp + 0x38]
003A7B45  mov      rsi, qword ptr [rsp + 0x40]
003A7B4A  add      rsp, 0x20
003A7B4E  pop      rdi
003A7B4F  ret      
```

## 003A8340 (79 B, extent 003A8340-003A838F)

Entered from (direct sites whose caller this page cites): `003A8AE0` + 0xF1 (call; `003A8AE0` is cited on this page)
Other direct sites: none

Host context: " (~~frame~~ birth step *(corrected 2026-10-02, OPUS: §2.1)*) | '00441B30' only ('00441E71') | | '002F3910' (update) | '0043EF40' ('0043EFBA'), '00442310' ('00442354') | | '00441B30' (element loop) | '003A8AE0' ('003A8C19'), '0043EF40' ('0043F1DB') | | '003A8AE0' | '003A8950', '003A8DD0', '0046EFD0' ('0046F218'), '00538820' ('005388D6') | | '0043EF40' | '003A8390', '0043F450' |  '0046EFD0' and '00538820' belong to the **sub-resource inst"

```
003A8340  mov      rax, qword ptr [rip + 0x2b16c41]  ; -> 02EBEF88
003A8347  add      rax, 0x18
003A834B  xor      r9d, r9d
003A834E  nop      
003A8350  mov      r10d, dword ptr [rax]
003A8353  cmp      r10d, ecx
003A8356  jne      0x3a8362  ; -> 003A8362
003A8358  movzx    r8d, byte ptr [rax + 4]
003A835D  cmp      r8d, edx
003A8360  je       0x3a8377  ; -> 003A8377
003A8362  cmp      r10d, -1
003A8366  je       0x3a837c  ; -> 003A837C
003A8368  inc      r9d
003A836B  add      rax, 8
003A836F  cmp      r9d, 0x20
003A8373  jge      0x3a838e  ; -> 003A838E
003A8375  jmp      0x3a8350  ; -> 003A8350
003A8377  inc      word ptr [rax + 6]
003A837B  ret      
003A837C  and      byte ptr [rax + 5], 0xfe
003A8380  mov      dword ptr [rax], ecx
003A8382  mov      ecx, 1
003A8387  mov      word ptr [rax + 6], cx
003A838B  mov      byte ptr [rax + 4], dl
003A838E  ret      
```

## 003A9AD0 (198 B, extent 003A9AD0-003A9B96)

Entered from (direct sites whose caller this page cites): `003A99F0` + 0x22 (call; `003A99F0` is cited on this page)
Other direct sites: none

Host context: " ('0050050B'–'0050052F'), with a sub-range partner '00538910' for '0x42'–'0xAB' ('00538910'–'00538939'). '003A9A70' writes that byte and then calls it ('003A9A8F', '003A9AAD'). Its other callers are '003A99F0' (after a 'memcpy') and '003A9BA0', reached from the EFX data parse '003EDAD0' / '003ED8A0' and from ~~instance creation~~ the context rebase arms of the per-frame effect pass '0024D540' ('0024D540'+0x114) and of '0024D970' ('0024D"

```
003A9AD0  mov      qword ptr [rsp + 0x10], rbx
003A9AD5  mov      qword ptr [rsp + 0x18], rbp
003A9ADA  push     rsi
003A9ADB  sub      rsp, 0x20
003A9ADF  mov      rax, qword ptr [rip + 0x2b15492]  ; -> 02EBEF78
003A9AE6  test     ecx, ecx
003A9AE8  movsxd   rbx, ecx
003A9AEB  mov      esi, r8d
003A9AEE  mov      ebp, edx
003A9AF0  mov      rcx, qword ptr [rax]
003A9AF3  je       0x3a9b62  ; -> 003A9B62
003A9AF5  mov      qword ptr [rsp + 0x30], rdi
003A9AFA  lea      rdi, [rbx*8]
003A9B02  mov      rcx, qword ptr [rdi + rcx]
003A9B06  test     rcx, rcx
003A9B09  je       0x3a9b22  ; -> 003A9B22
003A9B0B  call     0x3697f0  ; -> 003697F0 fn
003A9B10  mov      rax, qword ptr [rip + 0x2b15461]  ; -> 02EBEF78
003A9B17  mov      rcx, qword ptr [rax]
003A9B1A  mov      qword ptr [rdi + rcx], 0
003A9B22  mov      rdi, qword ptr [rsp + 0x30]
003A9B27  mov      ecx, esi
003A9B29  call     0x36a100  ; -> 0036A100 fn
003A9B2E  mov      r8, rax
003A9B31  test     rax, rax
003A9B34  je       0x3a9b84  ; -> 003A9B84
003A9B36  mov      byte ptr [rax + 0x44], bpl
003A9B3A  mov      word ptr [rax + 0x42], bx
003A9B3E  mov      rax, qword ptr [rip + 0x2b15433]  ; -> 02EBEF78
003A9B45  movsxd   rdx, ebx
003A9B48  mov      rcx, qword ptr [rax]
003A9B4B  mov      rax, r8
003A9B4E  mov      qword ptr [rcx + rdx*8], r8
003A9B52  mov      rbx, qword ptr [rsp + 0x38]
003A9B57  mov      rbp, qword ptr [rsp + 0x40]
003A9B5C  add      rsp, 0x20
003A9B60  pop      rsi
003A9B61  ret      
003A9B62  mov      ebx, 1
003A9B67  nop      word ptr [rax + rax]
003A9B70  movsxd   rax, ebx
003A9B73  cmp      qword ptr [rcx + rax*8], 0
003A9B78  je       0x3a9b27  ; -> 003A9B27
003A9B7A  inc      ebx
003A9B7C  cmp      ebx, 0x300
003A9B82  jl       0x3a9b70  ; -> 003A9B70
003A9B84  mov      rbx, qword ptr [rsp + 0x38]
003A9B89  xor      eax, eax
003A9B8B  mov      rbp, qword ptr [rsp + 0x40]
003A9B90  add      rsp, 0x20
003A9B94  pop      rsi
003A9B95  ret      
```

## 00441EE0 (40 B, extent 00441EE0-00441F08)

Entered from (direct sites whose caller this page cites): `002F2530` + 0x6EF (call; `002F2530` is cited on this page)
Other direct sites: none

Host context: "--- system: Effect element type dispatch — the switch tables behind an effect's per-frame work category: 17-Presentation-Rendering status: DOCUMENTED — the last open box, what 002F2530 does beyond its entry (UQ-206: the shared motion integrator), answered 2026-09-17; §2.8 census re-walked and the step's role corrected 2026-09-29 (FABLE, GI-8 / GI-9) owner_layer: CodeDomain:Presentation (effects) — no PrimaryOwner"

```
00441EE0  test     rcx, rcx
00441EE3  je       0x441eff  ; -> 00441EFF
00441EE5  mov      rax, qword ptr [rcx + 0x118]
00441EEC  test     rax, rax
00441EEF  je       0x441eff  ; -> 00441EFF
00441EF1  cmp      rax, rdx
00441EF4  je       0x441f02  ; -> 00441F02
00441EF6  mov      rax, qword ptr [rax + 0x30]
00441EFA  test     rax, rax
00441EFD  jne      0x441ef1  ; -> 00441EF1
00441EFF  xor      eax, eax
00441F01  ret      
00441F02  mov      eax, 1
00441F07  ret      
```
