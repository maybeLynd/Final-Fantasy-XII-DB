# F-interior pack: `04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-actor-manager-record-field-map.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 00263AC0 (118 B, extent 00263AC0-00263B36)

Page context: "ads the old value, stores its slot, does its work and stores the old value back. They are '0025AFC0',   'ActorManager_RunFieldRuntimePass' '0025D9E0', '0025E400', '002623A0', '00263050', '00263230', '00263AC0', '00264050' (binds   its argument, or slot 0 '02098E10' when null, and restores on each of three exits), '0026C3E0', '0026C5D0' (two pairs),   'ActorSystem_InitializeManagerRuntime' '0026CE60' and '0026E060'. The bind itself ('002"

```
00263AC0  push     rdi
00263AC2  sub      rsp, 0x20
00263AC6  mov      rdi, rcx
00263AC9  test     rcx, rcx
00263ACC  je       0x263b2e  ; -> 00263B2E
00263ACE  mov      qword ptr [rsp + 0x30], rbx
00263AD3  movzx    ebx, byte ptr [rcx + 0xf]
00263AD7  cmp      ebx, 2
00263ADA  jne      0x263b21  ; -> 00263B21
00263ADC  lea      rax, [rip + 0x1e3532d]  ; -> 02098E10
00263AE3  mov      qword ptr [rsp + 0x38], rsi
00263AE8  mov      rsi, qword ptr [rip + 0x1e36281]  ; -> 02099D70
00263AEF  mov      qword ptr [rip + 0x1e3627a], rax  ; -> 02099D70
00263AF6  call     0x3590d0  ; -> 003590D0 fn
00263AFB  test     eax, eax
00263AFD  je       0x263b08  ; -> 00263B08
00263AFF  mov      ecx, eax
00263B01  call     0x3588b0  ; -> 003588B0 fn
00263B06  jmp      0x263b0a  ; -> 00263B0A
00263B08  xor      eax, eax
00263B0A  cmp      rdi, rax
00263B0D  mov      qword ptr [rip + 0x1e3625c], rsi  ; -> 02099D70
00263B14  mov      rsi, qword ptr [rsp + 0x38]
00263B19  mov      ecx, 1
00263B1E  cmove    ebx, ecx
00263B21  mov      eax, ebx
00263B23  mov      rbx, qword ptr [rsp + 0x30]
00263B28  add      rsp, 0x20
00263B2C  pop      rdi
00263B2D  ret      
00263B2E  xor      eax, eax
00263B30  add      rsp, 0x20
00263B34  pop      rdi
00263B35  ret      
```

## 002A26A0 (122 B, extent 002A26A0-002A271A)

Page context: " against 'ebx' / 'edi' (×4: '003E9588'/'003E95F0'/'003E9650'/'003E969F'), 'byte[r9+0x3F3]' gate ('003E9605'), 'xmm3 = [rbx+4]' / 'xmm2 = [rbx]' with 'divss xmm0, [01DFE0BC]' ('003E96BB'–'003E96C7'), '002A26A0' ('003E96DE').  | member | role | interior | | --- | --- | --- | | '002A3600' (71 B) | the null-'+0xB8' tail — 'lea 0209C510' buffer ('002A3609'), '001814F0(edx)' ('002A3622'), 'byte[rax]' → 'byte[[rbx+8]]' copy ('002A362C'–'002A36"

```
002A26A0  movzx    eax, byte ptr [rcx + 0x3f3]
002A26A7  test     al, al
002A26A9  js       0x2a2719  ; -> 002A2719
002A26AB  or       al, 8
002A26AD  mov      byte ptr [rcx + 0x3f3], al
002A26B3  movsxd   rax, edx
002A26B6  lea      rdx, [rax + rax*2]
002A26BA  shl      rdx, 5
002A26BE  add      rdx, qword ptr [rcx + 0x3f8]
002A26C5  mov      ecx, dword ptr [rsp + 0x30]
002A26C9  test     ecx, ecx
002A26CB  jne      0x2a26dc  ; -> 002A26DC
002A26CD  and      dword ptr [rdx + 8], 0xffffffef
002A26D1  movss    dword ptr [rdx + 0x24], xmm2
002A26D6  movss    dword ptr [rdx + 0x28], xmm3
002A26DB  ret      
002A26DC  or       dword ptr [rdx + 8], 0x10
002A26E0  movzx    eax, word ptr [rsp + 0x28]
002A26E5  mov      word ptr [rdx + 0x5c], ax
002A26E9  xor      eax, eax
002A26EB  movss    xmm0, dword ptr [rdx + 0x24]
002A26F0  movss    xmm1, dword ptr [rdx + 0x28]
002A26F5  subss    xmm2, xmm0
002A26F9  movss    dword ptr [rdx + 0x48], xmm0
002A26FE  subss    xmm3, xmm1
002A2702  movss    dword ptr [rdx + 0x50], xmm1
002A2707  movss    dword ptr [rdx + 0x4c], xmm2
002A270C  movss    dword ptr [rdx + 0x54], xmm3
002A2711  mov      word ptr [rdx + 0x58], ax
002A2715  mov      word ptr [rdx + 0x5a], cx
002A2719  ret      
```

## 00345CD0 (336 B, extent 00345CD0-00345E20)

Page context: "pt_VM_Native_Bridge — MECHANICAL (SWE2-EC7-170, 207 edges).** The '0046BD60' enumeration's helpers '00263FF0', '00358940' and '002EA6A0' are consumed across the bridge layer ('0033F7F0', '0025E4C0', '00345CD0', '00267420', '0050D5E0', +202 more) — the '0026xxxx'/'0035xxxx' accessor family's fan-in, no bridge relationship to the record map. Edge list from 'edges.tsv' 2026-09-22.  *Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per"

```
00345CD0  mov      qword ptr [rsp + 0x18], rbp
00345CD5  push     rsi
00345CD6  push     r14
00345CD8  push     r15
00345CDA  sub      rsp, 0x50
00345CDE  movaps   xmmword ptr [rsp + 0x40], xmm6
00345CE3  mov      r15, rcx
00345CE6  movaps   xmmword ptr [rsp + 0x30], xmm7
00345CEB  mov      rcx, r9
00345CEE  movaps   xmmword ptr [rsp + 0x20], xmm8
00345CF4  mov      rsi, r9
00345CF7  mov      r14, r8
00345CFA  call     0x267db0  ; -> 00267DB0 fn
00345CFF  mov      rcx, rsi
00345D02  movaps   xmm6, xmm0
00345D05  call     0x267db0  ; -> 00267DB0 fn
00345D0A  mov      rcx, rsi
00345D0D  movaps   xmm7, xmm0
00345D10  call     0x267db0  ; -> 00267DB0 fn
00345D15  mov      rcx, rsi
00345D18  movaps   xmm8, xmm0
00345D1C  call     0x267e10  ; -> 00267E10 fn
00345D21  mov      edx, 1
00345D26  mov      ecx, eax
00345D28  mov      r8d, edx
00345D2B  call     0x359ca0  ; -> 00359CA0 fn
00345D30  mov      rbp, rax
00345D33  test     rax, rax
00345D36  je       0x345dfe  ; -> 00345DFE
00345D3C  mov      rcx, rax
00345D3F  call     0x2ea6a0  ; -> 002EA6A0 fn
00345D44  test     eax, eax
00345D46  je       0x345dfe  ; -> 00345DFE
00345D4C  mov      qword ptr [rsp + 0x70], rbx
00345D51  mov      rcx, rbp
00345D54  mov      qword ptr [rsp + 0x78], rdi
00345D59  call     0x264420  ; -> 00264420 fn
00345D5E  mov      rcx, rbp
00345D61  mov      ebx, eax
00345D63  call     0x30beb0  ; -> 0030BEB0 fn
00345D68  xor      edx, edx
00345D6A  mov      rcx, rbp
00345D6D  mov      edi, eax
00345D6F  call     0x35a720  ; -> 0035A720 fn
00345D74  mov      r8d, 2
00345D7A  mov      edx, ebx
00345D7C  mov      rcx, rbp
00345D7F  call     0x2ecf10  ; -> 002ECF10 fn
00345D84  movaps   xmm1, xmm8
00345D88  mov      rcx, rsi
00345D8B  call     0x267f60  ; -> 00267F60 fn
00345D90  movaps   xmm1, xmm7
00345D93  mov      rcx, rsi
00345D96  call     0x267f60  ; -> 00267F60 fn
00345D9B  movaps   xmm1, xmm6
00345D9E  mov      rcx, rsi
00345DA1  call     0x267f60  ; -> 00267F60 fn
00345DA6  call     0x3590b0  ; -> 003590B0 fn
00345DAB  movaps   xmm1, xmm0
00345DAE  mov      rcx, rsi
00345DB1  call     0x267f60  ; -> 00267F60 fn
00345DB6  mov      r9, rsi
00345DB9  mov      r8, r14
00345DBC  mov      rdx, rbp
00345DBF  mov      rcx, r15
00345DC2  call     0x357a20  ; -> 00357A20 fn
00345DC7  mov      rcx, rbp
00345DCA  call     0x263f40  ; -> 00263F40 fn
00345DCF  mov      rcx, rax
00345DD2  call     0x2eb430  ; -> 002EB430 fn
00345DD7  mov      edx, 2
00345DDC  mov      rcx, rbp
00345DDF  call     0x26c120  ; -> 0026C120 fn
00345DE4  mov      r8d, edi
00345DE7  mov      edx, 1
00345DEC  mov      rcx, rbp
00345DEF  call     0x269d80  ; -> 00269D80 fn
00345DF4  mov      rdi, qword ptr [rsp + 0x78]
00345DF9  mov      rbx, qword ptr [rsp + 0x70]
00345DFE  mov      rbp, qword ptr [rsp + 0x80]
00345E06  movaps   xmm6, xmmword ptr [rsp + 0x40]
00345E0B  movaps   xmm7, xmmword ptr [rsp + 0x30]
00345E10  movaps   xmm8, xmmword ptr [rsp + 0x20]
00345E16  add      rsp, 0x50
00345E1A  pop      r15
00345E1C  pop      r14
00345E1E  pop      rsi
00345E1F  ret      
```

## 00537BA0 (117 B, extent 00537BA0-00537C15)

Page context: "struction fragment  '004FF0D0' (56 B) is the '+0xC2' kind dispatcher the '003Axxxx' manager-record getters reach: 'rax = [rcx+0xE0]' fetches the record, 'byte[rax+0xC2]' selects four tail arms — 0 → '00537BA0', 1 → '00537CC0', 2 → '00537FF0', 3 → '005383B0' — with any other value returning 0. Interior anchor '004FF0D7' (the '+0xC2' kind read). Callers '003A4290'/'003A56F0'/'003A7EE0'/'003A8290' — the record-getter cluster this page's fi"

```
00537BA0  mov      qword ptr [rsp + 0x18], rbx
00537BA5  push     rdi
00537BA6  sub      rsp, 0x40
00537BAA  mov      rax, qword ptr [rip + 0x1a0cc7f]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00537BB1  xor      rax, rsp
00537BB4  mov      qword ptr [rsp + 0x30], rax
00537BB9  mov      rdi, qword ptr [rcx + 0xe0]
00537BC0  mov      rbx, rcx
00537BC3  call     0x4fe930  ; -> 004FE930 fn
00537BC8  test     eax, eax
00537BCA  je       0x537bf8  ; -> 00537BF8
00537BCC  lea      r8, [rbx + 0x110]
00537BD3  mov      rdx, rbx
00537BD6  lea      rcx, [rdi + 0xd0]
00537BDD  lea      r9, [rsp + 0x20]
00537BE2  call     0x3a56c0  ; -> 003A56C0 fn
00537BE7  test     eax, eax
00537BE9  je       0x537bfd  ; -> 00537BFD
00537BEB  lea      rdx, [rsp + 0x20]
00537BF0  mov      rcx, rbx
00537BF3  call     0x4fead0  ; -> 004FEAD0 fn
00537BF8  mov      eax, 1
00537BFD  mov      rcx, qword ptr [rsp + 0x30]
00537C02  xor      rcx, rsp
00537C05  call     0x808c40  ; -> 00808C40 fn
00537C0A  mov      rbx, qword ptr [rsp + 0x60]
00537C0F  add      rsp, 0x40
00537C13  pop      rdi
00537C14  ret      
```
