# Homing pack: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/as7-menu-graphics-containers.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-as7-menu-graphics-containers.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00292050 (55 B, extent 00292050-00292087)

Entered from (direct sites whose caller this page cites): `00292390` + 0x152 (call; `00292390` is cited on this page); `00292390` + 0x31C (call; `00292390` is cited on this page)
Other direct sites: none

Host context: "x98'–'0xA1' ('itemgra_c.tm2', 'Item_Clut.bin', 'Item_Gra00'–'07.as7') through '0024AB90' and '0032E620', filling 16-byte slots of the table at '0209BEA0'; '00291D90' copies them into its object; and '00292390' picks one 1,024-byte 'Item_Clut' palette per item graphic by 'id >> 6'. That the 64 payloads of sheet *n* are the ids '64n..64n+63', drawn as 8-bit indexed pixels against that palette, fits both counts and is **not claimed** — the" / "x98'–'0xA1' ('itemgra_c.tm2', 'Item_Clut.bin', 'Item_Gra00'–'07.as7') through '0024AB90' and '0032E620', filling 16-byte slots of the table at '0209BEA0'; '00291D90' copies them into its object; and '00292390' picks one 1,024-byte 'Item_Clut' palette per item graphic by 'id >> 6'. That the 64 payloads of sheet *n* are the ids '64n..64n+63', drawn as 8-bit indexed pixels against that palette, fits both counts and is **not claimed** — the"

```
00292050  mov      rax, qword ptr [rip + 0x1e08bd9]  ; -> 0209AC30
00292057  mov      rdx, qword ptr [rax + 0x300]
0029205E  test     rdx, rdx
00292061  je       0x292084  ; -> 00292084
00292063  mov      eax, 1
00292068  shl      eax, cl
0029206A  movzx    eax, ax
0029206D  test     dword ptr [rdx + 0x168], eax
00292073  je       0x292084  ; -> 00292084
00292075  movsxd   rax, ecx
00292078  add      rax, 0xd
0029207C  add      rax, rax
0029207F  mov      rax, qword ptr [rdx + rax*8]
00292083  ret      
00292084  xor      eax, eax
00292086  ret      
```

## 003DF7B0 (89 B, extent 003DF7B0-003DF809)

Entered from (direct sites whose caller this page cites): `002628B0` + 0x133 (call; `002628B0` is cited on this page)
Other direct sites: `003546C0` + 0x1D (jmp); `00354B00` + 0x1A (jmp)

Host context: " loaders 'ActorResource_BeginManagerResourceSetLoad' ('0032FCA0', reached from '0032FC30'), 'ActorResource_BeginPrimaryPayloadLoad' ('00330310') and '003306E0' call them, along with their own calls ('002628B0', '0032ED80', '00263FF0', '003304A0', and '003306E0''s calls to '002561C0', '002566E0' and '0037DC30'). The field loaders 'MapRef_BeginLoadResources' ('00268750'), '003319D0', '00378030', '00379A10' and 'AreaArd_LoadOrUnloadFieldRe"

```
003DF7B0  sub      rsp, 0x28
003DF7B4  mov      eax, dword ptr [rip + 0x277a55e]  ; -> 02B59D18
003DF7BA  test     edx, edx
003DF7BC  je       0x3df7c3  ; -> 003DF7C3
003DF7BE  btr      eax, ecx
003DF7C1  jmp      0x3df7c6  ; -> 003DF7C6
003DF7C3  bts      eax, ecx
003DF7C6  mov      dword ptr [rip + 0x277a54c], eax  ; -> 02B59D18
003DF7CC  test     eax, eax
003DF7CE  jne      0x3df7d9  ; -> 003DF7D9
003DF7D0  add      rsp, 0x28
003DF7D4  jmp      0x3df810  ; -> 003DF810 fn
003DF7D9  xor      r9d, r9d
003DF7DC  xor      r8d, r8d
003DF7DF  xor      edx, edx
003DF7E1  xor      ecx, ecx
003DF7E3  call     0x29cab0  ; -> 0029CAB0 fn
003DF7E8  xor      eax, eax
003DF7EA  mov      qword ptr [rip + 0x277a50f], rax  ; -> 02B59D00
003DF7F1  mov      qword ptr [rip + 0x277a510], rax  ; -> 02B59D08
003DF7F8  mov      dword ptr [rip + 0x277a512], eax  ; -> 02B59D10
003DF7FE  mov      dword ptr [rip + 0x277a510], eax  ; -> 02B59D14
003DF804  add      rsp, 0x28
003DF808  ret      
```
