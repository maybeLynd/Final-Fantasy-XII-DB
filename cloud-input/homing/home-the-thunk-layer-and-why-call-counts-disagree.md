# Homing pack: `24-Compiler-And-CRT-Runtime/Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-thunk-layer-and-why-call-counts-disagree.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0028C4C0 (42 B, extent 0028C4C0-0028C4EA)

Entered from (direct sites whose caller this page cites): `0028E290` + 0x98 (call; `0028E290` is cited on this page)
Other direct sites: none

Host context: "after         'AUDITSEM-CONTRA-FABLE-BU3-A0-USERS': the first list matched '0xa0' as a substring and took in two '+0xA0D0' sites*:          | caller | site | callee |         |---|---|---|         | '0028E290' (the gate) | '0028E4BF' | '003F8EC0' |         | '0028EAB0' | '0028EBD4' | '003F8C70' |         | '0028FA70' | '0028FA80' | '003F8EA0' |         | '0028FAF0' | '0028FB11' | '003F8EC0' |         | '0028FB40' | '0028FB47' | '003F8D2"

```
0028C4C0  test     rcx, rcx
0028C4C3  je       0x28c4e9  ; -> 0028C4E9
0028C4C5  push     rbx
0028C4C6  sub      rsp, 0x20
0028C4CA  mov      rbx, rcx
0028C4CD  nop      dword ptr [rax]
0028C4D0  mov      rcx, rbx
0028C4D3  call     0x28bb50  ; -> 0028BB50 fn
0028C4D8  mov      rbx, qword ptr [rbx + 0xd70]
0028C4DF  test     rbx, rbx
0028C4E2  jne      0x28c4d0  ; -> 0028C4D0
0028C4E4  add      rsp, 0x20
0028C4E8  pop      rbx
0028C4E9  ret      
```

## 0029CF10 (23 B, extent 0029CF10-0029CF27)

Entered from (direct sites whose caller this page cites): `00253780` + 0x61 (call; `00253780` is cited on this page)
Other direct sites: none

Host context: "003F8D20' |          '0028E43D' (→ '003F80D0') and '0029045E' (→ '003F80E0') address **'+0xA0D0'**, a different member.       - **What the element does.**         - '0028FB40' → '003F8D20' runs from '00253780' for a message whose '+8' is '0xF' ('0025381A'–'00253825'). Unless flag '+0x52C6'           bit 0 is set, it loads the resource named by '[01E0C208]', the string **'partytop_8_c'** ('003F8D45'–'003F8D51',           handle at '+0x52"

```
0029CF10  sub      rsp, 0x28
0029CF14  call     0x2b3480  ; -> 002B3480 fn
0029CF19  call     0x16d6a0  ; -> 0016D6A0 fn
0029CF1E  add      rsp, 0x28
0029CF22  jmp      0x2dd840  ; -> 002DD840 fn
```
