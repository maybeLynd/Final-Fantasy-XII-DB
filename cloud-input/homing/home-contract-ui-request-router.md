# Homing pack: `16-UI/CONTRACT-ui-request-router.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-ui-request-router.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0037E8A0 (47 B, extent 0037E8A0-0037E8CF)

Entered from (direct sites whose caller this page cites): `003F4E70` + 0xB1 (call; `003F4E70` is cited on this page)
Other direct sites: none

Host context: "ent in '02092734', and '00254B50+0x2A' refuses every id while it is 1; callers passing 1 include request 3 '0035D980+0xCA', request 24's widget '0035D6B0+0x175', '0027EFA0+0x35', '0035C960+0xA9' and '003F4E70+0x19C')* | | **R-b** | the **policy**: the requested bit is set in the inhibit mask | '00254BC1 bt' | the game currently forbids this operation | | **R-c** | the **root is busy**: '*(0209AC30) + 0xB8' or '+ 0xC0' is non-null | '002"

```
0037E8A0  mov      rax, qword ptr [rip + 0x276ebe9]  ; -> 02AED490
0037E8A7  mov      rdx, qword ptr [rax + 0xc8]
0037E8AE  test     rdx, rdx
0037E8B1  jne      0x37e8bb  ; -> 0037E8BB
0037E8B3  lea      rax, [rip + 0x196cd7e]  ; -> 01CEB638
0037E8BA  ret      
0037E8BB  movzx    eax, word ptr [rdx + 0xa]
0037E8BF  cmp      ecx, eax
0037E8C1  jge      0x37e8b3  ; -> 0037E8B3
0037E8C3  movsxd   rax, ecx
0037E8C6  mov      ecx, dword ptr [rdx + rax*8 + 0xc]
0037E8CA  jmp      0x2f9920  ; -> 002F9920 fn
```

## 0037F3B0 (134 B, extent 0037F3B0-0037F436)

Entered from (direct sites whose caller this page cites): `003F4E70` + 0x1A4 (call; `003F4E70` is cited on this page)
Other direct sites: none

Host context: "ent in '02092734', and '00254B50+0x2A' refuses every id while it is 1; callers passing 1 include request 3 '0035D980+0xCA', request 24's widget '0035D6B0+0x175', '0027EFA0+0x35', '0035C960+0xA9' and '003F4E70+0x19C')* | | **R-b** | the **policy**: the requested bit is set in the inhibit mask | '00254BC1 bt' | the game currently forbids this operation | | **R-c** | the **root is busy**: '*(0209AC30) + 0xB8' or '+ 0xC0' is non-null | '002"

```
0037F3B0  sub      rsp, 0x58
0037F3B4  mov      rax, qword ptr [rip + 0x1bc5475]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0037F3BB  xor      rax, rsp
0037F3BE  mov      qword ptr [rsp + 0x48], rax
0037F3C3  cmp      qword ptr [rip + 0x276e0c5], 0  ; -> 02AED490
0037F3CB  jne      0x37f422  ; -> 0037F422
0037F3CD  lea      rax, [rsp + 0x20]
0037F3D2  mov      qword ptr [rsp + 0x28], rcx
0037F3D7  mov      ecx, 0x5f0
0037F3DC  mov      qword ptr [rsp + 0x38], rax
0037F3E1  lea      r8, [rsp + 0x30]
0037F3E6  mov      dword ptr [rsp + 0x30], 0
0037F3EE  lea      rdx, [rip + 0xdb]  ; -> 0037F4D0
0037F3F5  mov      qword ptr [rsp + 0x40], 0
0037F3FE  mov      dword ptr [rsp + 0x20], 0x10000
0037F406  call     0x244f50  ; -> 00244F50 fn
0037F40B  mov      eax, 1
0037F410  mov      rcx, qword ptr [rsp + 0x48]
0037F415  xor      rcx, rsp
0037F418  call     0x808c40  ; -> 00808C40 fn
0037F41D  add      rsp, 0x58
0037F421  ret      
0037F422  xor      eax, eax
0037F424  mov      rcx, qword ptr [rsp + 0x48]
0037F429  xor      rcx, rsp
0037F42C  call     0x808c40  ; -> 00808C40 fn
0037F431  add      rsp, 0x58
0037F435  ret      
```

## 003EBD70 (78 B, extent 003EBD70-003EBDBE)

Entered from (direct sites whose caller this page cites): `002628B0` + 0x1CD (call; `002628B0` is cited on this page)
Other direct sites: `003444C0` + 0x0 (jmp)

Host context: "ed the same completion path the router drives; shared machinery, no shared ownership.  **ActorEntity — SERVICE (SWE2-EC7, batch 168, 13 edges).** '00252DE0'/'0026A5F0'/'0026DB30' answer callers like '002628B0'/'0025D9E0'/'0026C8Cx', and '00253C70' forwards to '0025B4C0' - actor-side bodies consume the router's request helpers; service crossing, not ownership.  **CoreRuntimeScheduling — SERVICE (SWE2-EC7, batch 168, 7 edges).** '00253C70"

```
003EBD70  sub      rsp, 0x28
003EBD74  mov      rcx, qword ptr [rip + 0x2772eed]  ; -> 02B5EC68
003EBD7B  mov      qword ptr [rip + 0x2772eda], 0  ; -> 02B5EC60
003EBD86  test     rcx, rcx
003EBD89  je       0x3ebd9b  ; -> 003EBD9B
003EBD8B  call     0x3697f0  ; -> 003697F0 fn
003EBD90  mov      qword ptr [rip + 0x2772ecd], 0  ; -> 02B5EC68
003EBD9B  xor      eax, eax
003EBD9D  mov      qword ptr [rip + 0x2772ecc], rax  ; -> 02B5EC70
003EBDA4  mov      qword ptr [rip + 0x2772ecd], rax  ; -> 02B5EC78
003EBDAB  mov      qword ptr [rip + 0x2772ece], rax  ; -> 02B5EC80
003EBDB2  mov      qword ptr [rip + 0x2772ecf], rax  ; -> 02B5EC88
003EBDB9  add      rsp, 0x28
003EBDBD  ret      
```
