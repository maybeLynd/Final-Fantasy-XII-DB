# Homing pack: `17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md`

Generated 2026-10-03 09:39 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-effect-element-type-dispatch.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

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
