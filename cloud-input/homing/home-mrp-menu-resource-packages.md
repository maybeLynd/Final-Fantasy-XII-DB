# Homing pack: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/mrp-menu-resource-packages.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-mrp-menu-resource-packages.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002E1630 (43 B, extent 002E1630-002E165B)

Entered from (direct sites whose caller this page cites): `002628B0` + 0x391 (call; `002628B0` is cited on this page)
Other direct sites: `00345E20` + 0xF (call)

Host context: " loaders 'ActorResource_BeginManagerResourceSetLoad' ('0032FCA0', reached from '0032FC30'), 'ActorResource_BeginPrimaryPayloadLoad' ('00330310') and '003306E0' call them, along with their own calls ('002628B0', '0032ED80', '00263FF0', '003304A0', and '003306E0''s calls to '002561C0', '002566E0' and '0037DC30'). The field loaders 'MapRef_BeginLoadResources' ('00268750'), '003319D0', '00378030', '00379A10' and 'AreaArd_LoadOrUnloadFieldRe"

```
002E1630  sub      rsp, 0x28
002E1634  call     0x290180  ; -> 00290180 fn
002E1639  test     eax, eax
002E163B  je       0x2e1653  ; -> 002E1653
002E163D  sub      eax, 1
002E1640  je       0x2e164c  ; -> 002E164C
002E1642  cmp      eax, 1
002E1645  jne      0x2e164c  ; -> 002E164C
002E1647  add      rsp, 0x28
002E164B  ret      
002E164C  xor      eax, eax
002E164E  add      rsp, 0x28
002E1652  ret      
002E1653  or       eax, 0xffffffff
002E1656  add      rsp, 0x28
002E165A  ret      
```

## 002E2300 (9 B, extent 002E2300-002E2309)

Entered from (direct sites whose caller this page cites): `002628B0` + 0x105 (call; `002628B0` is cited on this page)
Other direct sites: `003406E0` + 0x12 (jmp)

Host context: " loaders 'ActorResource_BeginManagerResourceSetLoad' ('0032FCA0', reached from '0032FC30'), 'ActorResource_BeginPrimaryPayloadLoad' ('00330310') and '003306E0' call them, along with their own calls ('002628B0', '0032ED80', '00263FF0', '003304A0', and '003306E0''s calls to '002561C0', '002566E0' and '0037DC30'). The field loaders 'MapRef_BeginLoadResources' ('00268750'), '003319D0', '00378030', '00379A10' and 'AreaArd_LoadOrUnloadFieldRe"

```
002E2300  mov      edx, ecx
002E2302  xor      ecx, ecx
002E2304  jmp      0x16d6a0  ; -> 0016D6A0 fn
```

## 003F4690 (330 B, extent 003F4690-003F47DA)

Entered from (direct sites whose caller this page cites): `003F4840` + 0x196 (call; `003F4840` is cited on this page)
Other direct sites: none

Host context: "er to the relocator.  | screen / loader | '.mrp' | kind-7 id | site | |---|---|---:|---| | title '00393FF0' | 'title.mrp' | '0x3A' | '00394048' via '00249320'; also manifest list '008FD010' | | shop '003F4840' | 'shop_new.mrp' | '0x96' | '003F492D' via '00249320' | | location map '00404060' | 'Loca.mrp' | '0xBF' | '00404107' via '00249320'; also manifest list '008FCF60' | | world map '00562F90' | 'w_menu.mrp' | '0xA6' | '00563048' via '"

```
003F4690  push     rbx
003F4692  sub      rsp, 0x70
003F4696  mov      rax, qword ptr [rip + 0x1b50193]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003F469D  xor      rax, rsp
003F46A0  mov      qword ptr [rsp + 0x60], rax
003F46A5  mov      rbx, rcx
003F46A8  movzx    ecx, byte ptr [rcx + 0xc0]
003F46AF  test     ecx, ecx
003F46B1  je       0x3f46cd  ; -> 003F46CD
003F46B3  cmp      ecx, 1
003F46B6  je       0x3f46e3  ; -> 003F46E3
003F46B8  xor      eax, eax
003F46BA  mov      rcx, qword ptr [rsp + 0x60]
003F46BF  xor      rcx, rsp
003F46C2  call     0x808c40  ; -> 00808C40 fn
003F46C7  add      rsp, 0x70
003F46CB  pop      rbx
003F46CC  ret      
003F46CD  lea      rcx, [rbx + 0xd0]
003F46D4  test     byte ptr [rcx], 1
003F46D7  jne      0x3f4750  ; -> 003F4750
003F46D9  cmp      word ptr [rbx + 0xd8], 0
003F46E1  jne      0x3f4750  ; -> 003F4750
003F46E3  cmp      word ptr [rbx + 0xda], 0
003F46EB  je       0x3f46b8  ; -> 003F46B8
003F46ED  lea      rcx, [rsp + 0x20]
003F46F2  mov      qword ptr [rsp + 0x30], rbx
003F46F7  lea      rax, [rbx + 0xd0]
003F46FE  mov      qword ptr [rsp + 0x50], rcx
003F4703  mov      qword ptr [rsp + 0x20], rax
003F4708  lea      r8, [rsp + 0x48]
003F470D  lea      rax, [rbx + 0xf8]
003F4714  mov      ecx, 0xf0
003F4719  mov      qword ptr [rsp + 0x28], rax
003F471E  lea      rdx, [rip - 0x6c5]  ; -> 003F4060
003F4725  xor      eax, eax
003F4727  mov      dword ptr [rsp + 0x48], eax
003F472B  mov      qword ptr [rsp + 0x58], rax
003F4730  call     0x244f50  ; -> 00244F50 fn
003F4735  mov      rdx, rax
003F4738  mov      qword ptr [rbx + 0x118], rax
003F473F  mov      rcx, rbx
003F4742  call     0x246ad0  ; -> 00246AD0 fn
003F4747  mov      byte ptr [rbx + 0xc0], 2
003F474E  jmp      0x3f47c2  ; -> 003F47C2
003F4750  mov      rax, qword ptr [rbx + 0xc8]
003F4757  lea      r8, [rsp + 0x48]
003F475C  mov      qword ptr [rsp + 0x20], rax
003F4761  lea      rdx, [rip - 0x438]  ; -> 003F4330
003F4768  mov      qword ptr [rsp + 0x28], rcx
003F476D  lea      rax, [rbx + 0xf8]
003F4774  mov      qword ptr [rsp + 0x30], rax
003F4779  lea      rcx, [rsp + 0x20]
003F477E  mov      rax, qword ptr [rbx + 0x128]
003F4785  mov      qword ptr [rsp + 0x40], rax
003F478A  xor      eax, eax
003F478C  mov      qword ptr [rsp + 0x50], rcx
003F4791  mov      ecx, 0x128
003F4796  mov      dword ptr [rsp + 0x48], eax
003F479A  mov      qword ptr [rsp + 0x58], rax
003F479F  mov      qword ptr [rsp + 0x38], rbx
003F47A4  call     0x244f50  ; -> 00244F50 fn
003F47A9  mov      rdx, rax
003F47AC  mov      qword ptr [rbx + 0x110], rax
003F47B3  mov      rcx, rbx
003F47B6  call     0x246ad0  ; -> 00246AD0 fn
003F47BB  mov      byte ptr [rbx + 0xc0], 1
003F47C2  mov      eax, 1
003F47C7  mov      rcx, qword ptr [rsp + 0x60]
003F47CC  xor      rcx, rsp
003F47CF  call     0x808c40  ; -> 00808C40 fn
003F47D4  add      rsp, 0x70
003F47D8  pop      rbx
003F47D9  ret      
```
