# Homing pack: `15-Input/Binding-Profiles/binding-profiles-remapping-and-control-state.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-binding-profiles-remapping-and-control-state.json`.

Bodies: 5. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0017E500 (31 B, extent 0017E500-0017E51F)

Entered from (direct sites whose caller this page cites): `002284F0` + 0xB4 (call; `002284F0` is cited on this page)
Other direct sites: none

Host context: "0 and '[0] != 1' always holds**. > - **'00228480'** would matter only when field 0 is 1. It returns whether the widget pointer '01FD4948' is set. '00228490' >   creates that '0xD0'-byte widget (proc '002284F0', '002284CD'–'002284D2') when '0017E4C0()' — the input backend's byte >   '+0x27' — is 0 ('0022839B'–'002283AE'), and the proc's message-18 arm clears the pointer ('00228526'). > - **Consequences:** >   - every binding is polled: '"

```
0017E500  xor      r8d, r8d
0017E503  mov      edx, 0x8002
0017E508  test     ecx, ecx
0017E50A  mov      rcx, qword ptr [rip + 0x2d26d37]  ; -> 02EA5248
0017E511  setne    r8b
0017E515  xor      r9d, r9d
0017E518  jmp      qword ptr [rip + 0x7442e9]  ; -> 008C2808 [u64 0x0000000001CCC7BE]
```

## 001E0980 (36 B, extent 001E0980-001E09A4)

Entered from (direct sites whose caller this page cites): `002284F0` + 0x160 (call; `002284F0` is cited on this page)
Other direct sites: none

Host context: "0 and '[0] != 1' always holds**. > - **'00228480'** would matter only when field 0 is 1. It returns whether the widget pointer '01FD4948' is set. '00228490' >   creates that '0xD0'-byte widget (proc '002284F0', '002284CD'–'002284D2') when '0017E4C0()' — the input backend's byte >   '+0x27' — is 0 ('0022839B'–'002283AE'), and the proc's message-18 arm clears the pointer ('00228526'). > - **Consequences:** >   - every binding is polled: '"

```
001E0980  sub      rsp, 0x28
001E0984  call     0x198790  ; -> 00198790 fn
001E0989  test     rax, rax
001E098C  je       0x1e099f  ; -> 001E099F
001E098E  call     0x198790  ; -> 00198790 fn
001E0993  mov      rcx, rax
001E0996  add      rsp, 0x28
001E099A  jmp      0x196710  ; -> 00196710 fn
001E099F  add      rsp, 0x28
001E09A3  ret      
```

## 002498A0 (12 B, extent 002498A0-002498AC)

Entered from (direct sites whose caller this page cites): `001EC060` + 0xEF (call; `001EC060` is cited on this page)
Other direct sites: none

Host context: "' with dl the active flag and r8b the slot id 2..7 (or 0) - the profile's code-to-binding lookup.  Interior anchor '001E0767' (function '001E0650').  '001EBDD0' (448 B) is the profile record builder '001EC060' calls: '001EB4B0' constructs a record from 'rcx+0x214' against '01DFE0A0'/'01F82E28', xmm constant blocks '008C5F80'/'008C5F90' load, '[rdi+0x22C]' carries a float into the stack frame, and '00182EE0'/'00185100' finish - the bindi"

```
002498A0  mov      eax, dword ptr [rip + 0x2d4dabe]  ; -> 02F97364
002498A6  and      eax, 0x800
002498AB  ret      
```

## 002E2570 (63 B, extent 002E2570-002E25AF)

Entered from (direct sites whose caller this page cites): `002284F0` + 0xA4 (jmp; `002284F0` is cited on this page); `002284F0` + 0x1AC (jmp; `002284F0` is cited on this page)
Other direct sites: none

Host context: "0 and '[0] != 1' always holds**. > - **'00228480'** would matter only when field 0 is 1. It returns whether the widget pointer '01FD4948' is set. '00228490' >   creates that '0xD0'-byte widget (proc '002284F0', '002284CD'–'002284D2') when '0017E4C0()' — the input backend's byte >   '+0x27' — is 0 ('0022839B'–'002283AE'), and the proc's message-18 arm clears the pointer ('00228526'). > - **Consequences:** >   - every binding is polled: '" / "0 and '[0] != 1' always holds**. > - **'00228480'** would matter only when field 0 is 1. It returns whether the widget pointer '01FD4948' is set. '00228490' >   creates that '0xD0'-byte widget (proc '002284F0', '002284CD'–'002284D2') when '0017E4C0()' — the input backend's byte >   '+0x27' — is 0 ('0022839B'–'002283AE'), and the proc's message-18 arm clears the pointer ('00228526'). > - **Consequences:** >   - every binding is polled: '"

```
002E2570  mov      eax, 7
002E2575  test     ecx, ecx
002E2577  jns      0x2e25a2  ; -> 002E25A2
002E2579  xor      ecx, ecx
002E257B  cmp      ecx, eax
002E257D  cmovg    ecx, eax
002E2580  movsxd   rax, ecx
002E2583  imul     rcx, rax, 0x68
002E2587  lea      rax, [rip + 0x1e7cc72]  ; -> 0215F200
002E258E  mov      rax, qword ptr [rcx + rax]
002E2592  test     rax, rax
002E2595  je       0x2e25a1  ; -> 002E25A1
002E2597  and      dword ptr [rax + 0x40], 0xfffffffe
002E259B  and      edx, 1
002E259E  or       dword ptr [rax + 0x40], edx
002E25A1  ret      
002E25A2  cmp      ecx, eax
002E25A4  cmovg    ecx, eax
002E25A7  test     ecx, ecx
002E25A9  jns      0x2e257b  ; -> 002E257B
002E25AB  xor      ecx, ecx
002E25AD  jmp      0x2e2580  ; -> 002E2580
```

## 0035C100 (62 B, extent 0035C100-0035C13E)

Entered from (direct sites whose caller this page cites): `003C8B70` + 0x2FF (call; `003C8B70` is cited on this page); `003C8B70` + 0x364 (call; `003C8B70` is cited on this page)
Other direct sites: `0029BE50` + 0x1CB (call)

Host context: "D0' - shared machinery across the layer boundary, no shared ownership. - **UI - CLIENT and SERVICE (16 edges).** '002B4090', '0017DDC0', '00228480' are also called by bodies filed to UI: '00252030', '003C8B70', '00276D30' (+9 more); '0023CE10' reaches bodies filed to UI: '00291D80' - shared machinery across the layer boundary, no shared ownership. - **WorldAreaField - CLIENT (1 edge).** '00228480' is also called by bodies filed to world" / "D0' - shared machinery across the layer boundary, no shared ownership. - **UI - CLIENT and SERVICE (16 edges).** '002B4090', '0017DDC0', '00228480' are also called by bodies filed to UI: '00252030', '003C8B70', '00276D30' (+9 more); '0023CE10' reaches bodies filed to UI: '00291D80' - shared machinery across the layer boundary, no shared ownership. - **WorldAreaField - CLIENT (1 edge).** '00228480' is also called by bodies filed to world"

```
0035C100  push     rbx
0035C102  sub      rsp, 0x20
0035C106  cmp      qword ptr [rip + 0x1f6c2d2], 0  ; -> 022C83E0
0035C10E  mov      ebx, ecx
0035C110  je       0x35c138  ; -> 0035C138
0035C112  call     0x290b10  ; -> 00290B10 fn
0035C117  mov      rax, qword ptr [rip + 0x1f6c2c2]  ; -> 022C83E0
0035C11E  mov      dword ptr [rax + 0xc4], 0
0035C128  test     ebx, ebx
0035C12A  je       0x35c138  ; -> 0035C138
0035C12C  xor      ecx, ecx
0035C12E  add      rsp, 0x20
0035C132  pop      rbx
0035C133  jmp      0x3c53e0  ; -> 003C53E0 fn
0035C138  add      rsp, 0x20
0035C13C  pop      rbx
0035C13D  ret      
```
