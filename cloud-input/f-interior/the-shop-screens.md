# F-interior pack: `16-UI/Shop-Screens/the-shop-screens.md`

Generated 2026-10-02 19:59 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-shop-screens.json`.

Functions: 13. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 85a2ae3ee	GI DD re-status: repair the audit-sem REJECT of c97af7156; 65f4854dd	SWE2-STRUCT pass-22 debt + OV31 narrowing: 77 crossing bullets across 21 docs (5 lane folders now re). OPUS read these before packing.

## 00282EE0 (37 B, extent 00282EE0-00282F05)

Page context: "elpers ('00367820'/'00368010'/'003687C0'/'003688E0'/'00368940', '0027F210'/'00285F20'/'0028E8B0'/'002BE020'), the '0028xxxx'/'0029xxxx' format-and-character helpers ('002699D0'/'0027ED10'/'0027F360'/'00282EE0'/'00282F80'/'00283840'/'00292140'/'002922F0'/ '00293170'/'002A1D20'/'002A1DC0') and the encoded-message formatters '002B4810'/'002B49F0', '003933B0'/'00394790'/'003948B0'/'003949B0'/'003985B0'/'00398910'/'003938B0' stock gates and "

```
00282EE0  mov      rdx, qword ptr [rip + 0x1e17d49]  ; -> 0209AC30
00282EE7  add      rdx, 0x408
00282EEE  xor      eax, eax
00282EF0  cmp      ecx, edx
00282EF2  je       0x282f04  ; -> 00282F04
00282EF4  inc      eax
00282EF6  add      rdx, 0xc0
00282EFD  cmp      eax, 9
00282F00  jl       0x282ef0  ; -> 00282EF0
00282F02  xor      eax, eax
00282F04  ret      
```

## 00292190 (120 B, extent 00292190-00292208)

Page context: "57B687' 'test rdx,rdx' | | '0057B6F0' | gil/price text — '002FA920'/'002FAD30' + '0030B4B0'/'0030B630' | '0057B715' 'call 002FAD30' | | '0057B780' | construct init — '002491B0'/'00249580'/'002920C0'/'00292190'/'002CBD50'/'002F8040'/'003933F0' | '0057B78D' 'call 00249580' | | '0057B890' | the menu-list proc — §above | '0057B8A6' 'lea rcx,[rip-0x45b8ad]' | | '0057BD40' | header/column repaint — '002C9F20'/'002CD420'/'002DD7E0'/'002F9860' "

```
00292190  push     rbx
00292192  sub      rsp, 0x20
00292196  mov      rbx, rcx
00292199  mov      ecx, 0xa
0029219E  call     0x2f8040  ; -> 002F8040 fn
002921A3  test     eax, eax
002921A5  jne      0x2921b2  ; -> 002921B2
002921A7  lea      edx, [rax + 0xa]
002921AA  mov      rcx, rbx
002921AD  call     0x2491b0  ; -> 002491B0 fn
002921B2  mov      ecx, 0x14
002921B7  call     0x2f8040  ; -> 002F8040 fn
002921BC  test     eax, eax
002921BE  jne      0x2921cb  ; -> 002921CB
002921C0  lea      edx, [rax + 0x14]
002921C3  mov      rcx, rbx
002921C6  call     0x2491b0  ; -> 002491B0 fn
002921CB  mov      ecx, 0xe
002921D0  call     0x2f8040  ; -> 002F8040 fn
002921D5  test     eax, eax
002921D7  jne      0x2921e4  ; -> 002921E4
002921D9  lea      edx, [rax + 0xe]
002921DC  mov      rcx, rbx
002921DF  call     0x2491b0  ; -> 002491B0 fn
002921E4  mov      ecx, 0x10
002921E9  call     0x2f8040  ; -> 002F8040 fn
002921EE  test     eax, eax
002921F0  jne      0x292202  ; -> 00292202
002921F2  lea      edx, [rax + 0x10]
002921F5  mov      rcx, rbx
002921F8  add      rsp, 0x20
002921FC  pop      rbx
002921FD  jmp      0x2491b0  ; -> 002491B0 fn
00292202  add      rsp, 0x20
00292206  pop      rbx
00292207  ret      
```

## 002A2620 (39 B, extent 002A2620-002A2647)

Page context: "ebuilds the panel.  ## '0056D370' — the trade panel  Dispatches ids 1, 2, 12, 18 ('0056D399'–'0056D3B3'):  - **id 1** '0056D66A': construct - **id 2** '0056D5C7': reconcile — when '+0xE4 & 0x10' and '002A2620' is ready, clears the bit and the parent's '+0xE0 & 0xE3FFFF' mask ('0056D5F3'), then branches on '+0xE4 & 0x3FC0': '0x2C0' → '0057A480' ('0056D61E'); else if '003933D0' passes → '0057A980' + '002CC4F0' ('0056D648') - **id 12** '00"

```
002A2620  mov      rax, qword ptr [rip + 0x1df9ea1]  ; -> 0209C4C8
002A2627  test     rax, rax
002A262A  je       0x2a2641  ; -> 002A2641
002A262C  test     byte ptr [rax + 0xc0], 3
002A2633  je       0x2a2638  ; -> 002A2638
002A2635  xor      eax, eax
002A2637  ret      
002A2638  cmp      byte ptr [rax + 0xf2], 0xff
002A263F  jg       0x2a2635  ; -> 002A2635
002A2641  mov      eax, 1
002A2646  ret      
```

## 002CB850 (84 B, extent 002CB850-002CB8A4)

Page context: "entative members: the '002Cxxxx' menu controls and '002Dxxxx' text/list draws (the same families the gambit screens use — '002CA3B0'/'002CA5C0'/'002CA5D0'/'002CAFE0'/'002CB1F0'/'002CB360'/'002CB790'/'002CB850'/ '002CB8B0'/'002CBA50'/'002CBC20'/'002CBC50'/'002CC5F0'/'002CC630'/'002CC660'/'002CC780'/ '002CCB10'/'002CCCA0'/'002CCD40'/'002CD150'/'002CF890'/'002D14E0'/'002D8B00'), the '002Fxxxx' string fetchers and resource helpers ('002F83E"

```
002CB850  sub      rsp, 0x28
002CB854  mov      rax, qword ptr [rip + 0x1dcf3d5]  ; -> 0209AC30
002CB85B  mov      edx, ecx
002CB85D  mov      rcx, qword ptr [rax + 0x2e0]
002CB864  test     rcx, rcx
002CB867  je       0x2cb89f  ; -> 002CB89F
002CB869  test     edx, edx
002CB86B  jne      0x2cb87e  ; -> 002CB87E
002CB86D  or       dword ptr [rcx + 0x168], 0x20000
002CB877  mov      edx, 1
002CB87C  jmp      0x2cb88a  ; -> 002CB88A
002CB87E  and      dword ptr [rcx + 0x168], 0xfffdffff
002CB888  xor      edx, edx
002CB88A  mov      rcx, qword ptr [rcx + 0xc0]
002CB891  call     0x247870  ; -> 00247870 fn
002CB896  add      rsp, 0x28
002CB89A  jmp      0x2cc2a0  ; -> 002CC2A0 fn
002CB89F  add      rsp, 0x28
002CB8A3  ret      
```

## 002CCB00 (15 B, extent 002CCB00-002CCB0F)

Page context: " '+0x4C' into 'edi' ∈ {0,1,2,3,4,5} ('00292C9A'–'00292D03' — 'edi=2' at '00292CC7' behind the '002CCA00' predicate, 'edi=0' via the 'mov edi, r14d' fallback at '00292CE9'); kind 6 becomes 7 behind a '002CCB00' predicate ('00292C79'– '00292C98'); kind 0xA first range-checks the param's high word against '0x8060'–'0x81FF' ('00292C2B'–'00292C4A'). Before the call it fetches the handler's record with '00295C20(edi)' ('00292D21') and passes "

```
002CCB00  xor      eax, eax
002CCB02  add      ecx, 0xffffc000
002CCB08  cmp      ecx, 0x17
002CCB0B  setbe    al
002CCB0E  ret      
```

## 002EC5D0 (89 B, extent 002EC5D0-002EC629)

Page context: "at answers the script rather than just acting. '0034C730' is two instructions, 'mov rcx, rdx / jmp 002E42D0', handing the context straight through. '00351000' calls '002E42D0' and then tail-jumps to '002EC5D0'. '00352250' pops one integer and tail-jumps to '008632B0'.  Two are worth stating exactly. '0034E1F0' **takes no argument at all** — it calls '00313550' and '00314D40' with a literal '1' before tail-jumping to '0037CA80', so the v"

```
002EC5D0  test     rcx, rcx
002EC5D3  je       0x2ec628  ; -> 002EC628
002EC5D5  push     rbx
002EC5D6  sub      rsp, 0x20
002EC5DA  mov      rax, qword ptr [rcx + 0xc0]
002EC5E1  mov      rbx, rcx
002EC5E4  test     rax, rax
002EC5E7  je       0x2ec623  ; -> 002EC623
002EC5E9  cmp      dword ptr [rax], -1
002EC5EC  je       0x2ec623  ; -> 002EC623
002EC5EE  movzx    ecx, word ptr [rax]
002EC5F1  cmp      cx, -1
002EC5F5  je       0x2ec619  ; -> 002EC619
002EC5F7  movsx    rax, cx
002EC5FB  imul     rcx, rax, 0x740
002EC602  add      rcx, qword ptr [rip + 0x1fda91f]  ; -> 022C6F28
002EC609  je       0x2ec619  ; -> 002EC619
002EC60B  cmp      dword ptr [rcx + 0x284], 0
002EC612  je       0x2ec619  ; -> 002EC619
002EC614  call     0x426e20  ; -> 00426E20 fn
002EC619  mov      dword ptr [rbx + 0xec], 0
002EC623  add      rsp, 0x20
002EC627  pop      rbx
002EC628  ret      
```

## 00351000 (30 B, extent 00351000-0035101E)

Page context: "Stack_PushInt32' — it is the only one of the six that answers the script rather than just acting. '0034C730' is two instructions, 'mov rcx, rdx / jmp 002E42D0', handing the context straight through. '00351000' calls '002E42D0' and then tail-jumps to '002EC5D0'. '00352250' pops one integer and tail-jumps to '008632B0'.  Two are worth stating exactly. '0034E1F0' **takes no argument at all** — it calls '00313550' and '00314D40' with a lite"

```
00351000  push     rbx
00351002  sub      rsp, 0x20
00351006  mov      rcx, rdx
00351009  mov      rbx, rdx
0035100C  call     0x2e42d0  ; -> 002E42D0 fn
00351011  mov      rcx, rbx
00351014  add      rsp, 0x20
00351018  pop      rbx
00351019  jmp      0x2ec5d0  ; -> 002EC5D0 fn
```

## 003933D0 (24 B, extent 003933D0-003933E8)

Page context: "ile — when '+0xE4 & 0x10' and '002A2620' is ready, clears the bit and the parent's '+0xE0 & 0xE3FFFF' mask ('0056D5F3'), then branches on '+0xE4 & 0x3FC0': '0x2C0' → '0057A480' ('0056D61E'); else if '003933D0' passes → '0057A980' + '002CC4F0' ('0056D648') - **id 12** '0056D3E5': sub-commands '0xF', '0x8000', '0x8001', '0x8002' — '0x8001' ('0056D42B') requires '+0xC8' set, then when '+0xE4 & 2' computes 'count × price' — 'imul' of '[+0xD"

```
003933D0  sub      rsp, 0x28
003933D4  call     0x2fabd0  ; -> 002FABD0 fn
003933D9  xor      ecx, ecx
003933DB  cmp      eax, 3
003933DE  setbe    cl
003933E1  mov      eax, ecx
003933E3  add      rsp, 0x28
003933E7  ret      
```

## 003F4060 (337 B, extent 003F4060-003F41B1)

Page context: "rtyBlackBandGradH', 'PartyBlackBandTime' | the party band's gradient → 'edx', anim ms → 'ecx', 'r8d' = 1 → '002C99A0' — the shared party-band animation call ('0057B82D', '0057B839') | | '003F3E40' (→'003F4060', a shop child widget) | 'PartyBlackBandGradH', 'BlackBandAnimTime' | gradient → 'edx', anim ms → 'r8d' ('ecx'/'edx' zeroed at the other site) → '002C9060' — the shop child's band build ('003F3FCB', '003F3EB4') |  ## What this scre"

```
003F4060  push     rbx
003F4062  sub      rsp, 0x20
003F4066  mov      rbx, rcx
003F4069  mov      ecx, dword ptr [rdx]
003F406B  sub      ecx, 1
003F406E  je       0x3f410f  ; -> 003F410F
003F4074  sub      ecx, 1
003F4077  je       0x3f40af  ; -> 003F40AF
003F4079  cmp      ecx, 0x10
003F407C  je       0x3f408b  ; -> 003F408B
003F407E  mov      rcx, rbx
003F4081  add      rsp, 0x20
003F4085  pop      rbx
003F4086  jmp      0x5c5230  ; -> 005C5230 fn
003F408B  mov      rcx, qword ptr [rbx + 0xe8]
003F4092  test     rcx, rcx
003F4095  je       0x3f41a9  ; -> 003F41A9
003F409B  xor      r8d, r8d
003F409E  lea      edx, [r8 + 0x12]
003F40A2  call     0x247510  ; -> 00247510 fn
003F40A7  xor      eax, eax
003F40A9  add      rsp, 0x20
003F40AD  pop      rbx
003F40AE  ret      
003F40AF  mov      ecx, dword ptr [rbx + 0xb4]
003F40B5  call     0x1edec0  ; -> 001EDEC0 fn
003F40BA  test     eax, eax
003F40BC  je       0x3f41a9  ; -> 003F41A9
003F40C2  cmp      byte ptr [rbx + 0xe1], 4
003F40C9  jne      0x3f40da  ; -> 003F40DA
003F40CB  call     0x2a2bf0  ; -> 002A2BF0 fn
003F40D0  test     eax, eax
003F40D2  je       0x3f41a9  ; -> 003F41A9
003F40D8  jmp      0x3f40ef  ; -> 003F40EF
003F40DA  dec      word ptr [rbx + 0xe2]
003F40E1  cmp      word ptr [rbx + 0xe2], 0
003F40E9  jg       0x3f41a9  ; -> 003F41A9
003F40EF  mov      rcx, rbx
003F40F2  call     0x3f3e40  ; -> 003F3E40 fn
003F40F7  test     eax, eax
003F40F9  jne      0x3f41a9  ; -> 003F41A9
003F40FF  mov      rcx, rbx
003F4102  call     0x244f00  ; -> 00244F00 fn
003F4107  xor      eax, eax
003F4109  add      rsp, 0x20
003F410D  pop      rbx
003F410E  ret      
003F410F  mov      r10, qword ptr [rdx + 8]
003F4113  xor      r9d, r9d
003F4116  mov      rax, qword ptr [r10]
003F4119  mov      qword ptr [rbx + 0xc0], rax
003F4120  mov      rax, qword ptr [r10 + 8]
003F4124  mov      qword ptr [rbx + 0xc8], rax
003F412B  mov      rax, qword ptr [r10 + 0x10]
003F412F  mov      qword ptr [rbx + 0xe8], rax
003F4136  mov      rax, qword ptr [r10]
003F4139  movzx    ecx, byte ptr [rax + 0xa]
003F413D  mov      byte ptr [rbx + 0xe0], cl
003F4143  test     cl, cl
003F4145  je       0x3f4183  ; -> 003F4183
003F4147  mov      edx, 0x1c
003F414C  lea      r8, [rbx + 0xd0]
003F4153  nop      dword ptr [rax]
003F4157  nop      word ptr [rax + rax]
003F4160  mov      rax, qword ptr [r10]
003F4163  lea      rdx, [rdx + 2]
003F4167  inc      r9d
003F416A  lea      r8, [r8 + 4]
003F416E  movzx    ecx, word ptr [rax + rdx - 2]
003F4173  mov      dword ptr [r8 - 4], ecx
003F4177  movzx    eax, byte ptr [rbx + 0xe0]
003F417E  cmp      r9d, eax
003F4181  jl       0x3f4160  ; -> 003F4160
003F4183  mov      rcx, rbx
003F4186  mov      byte ptr [rbx + 0xe1], 0
003F418D  call     0x3f3e40  ; -> 003F3E40 fn
003F4192  test     eax, eax
003F4194  je       0x3f40ff  ; -> 003F40FF
003F419A  mov      rcx, qword ptr [rip + 0x1c9a887]  ; -> 0208EA28
003F41A1  mov      rdx, rbx
003F41A4  call     0x246ad0  ; -> 00246AD0 fn
003F41A9  xor      eax, eax
003F41AB  add      rsp, 0x20
003F41AF  pop      rbx
003F41B0  ret      
```

## 003F47E0 (95 B, extent 003F47E0-003F483F)

Page context: " descriptor** on the stack — flags 3, that style byte, the byte '01E0C3CC', a word of '−1', and the two procedures '0057B6A0' and '0057C010' ('0057A593'–'0057A5D3') — and creates the element through '003F47E0(twinResult, &+0xC0, descriptor, [02CA9790]+0x158)', which is a thin wrapper that calls the widget factory '00244F50' with procedure '003F4840' and a '0x130'-byte record; finally it registers with '0208EA28' ('00244960'). **Id 2** a"

```
003F47E0  mov      r11, rsp
003F47E3  sub      rsp, 0x68
003F47E7  mov      rax, qword ptr [rip + 0x1b50042]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003F47EE  xor      rax, rsp
003F47F1  mov      qword ptr [rsp + 0x58], rax
003F47F6  mov      qword ptr [r11 - 0x48], rcx
003F47FA  lea      rax, [r11 - 0x48]
003F47FE  xor      ecx, ecx
003F4800  mov      qword ptr [r11 - 0x40], rdx
003F4804  mov      dword ptr [rsp + 0x40], ecx
003F4808  lea      rdx, [rip + 0x31]  ; -> 003F4840
003F480F  mov      qword ptr [r11 - 0x18], rcx
003F4813  mov      ecx, 0x130
003F4818  mov      qword ptr [r11 - 0x38], r8
003F481C  lea      r8, [r11 - 0x28]
003F4820  mov      qword ptr [r11 - 0x30], r9
003F4824  mov      qword ptr [r11 - 0x20], rax
003F4828  call     0x244f50  ; -> 00244F50 fn
003F482D  mov      rcx, qword ptr [rsp + 0x58]
003F4832  xor      rcx, rsp
003F4835  call     0x808c40  ; -> 00808C40 fn
003F483A  add      rsp, 0x68
003F483E  ret      
```

## 0056DD00 (67 B, extent 0056DD00-0056DD43)

Page context: " of one step | | 10 | '0056E259' | '0056DED0' — directional-input helper | | 12 | '0056E269' | '00293110', '00244F00' (mark-delete), '0056E5D0' | | 14 | '0056E212' | '002470D0' | | 15 | '0056E322' | '0056DD00' gate, then '00247510(self+0x188, 0xF, (self+0x194)>>2 & 1)' ('0056E322'–'0056E355') | | 18 | '0056E374' | '00247510', '003697F0' — deferred free | | 19 | '0056E222' | '0056E5D0' | | 20 | '0056E356' | '0056DD00' gate, then '002CFCF"

```
0056DD00  push     rbx
0056DD02  sub      rsp, 0x20
0056DD06  mov      rbx, rcx
0056DD09  call     0x57a960  ; -> 0057A960 fn
0056DD0E  test     eax, eax
0056DD10  je       0x56dd1a  ; -> 0056DD1A
0056DD12  xor      eax, eax
0056DD14  add      rsp, 0x20
0056DD18  pop      rbx
0056DD19  ret      
0056DD1A  test     byte ptr [rbx + 0x194], 4
0056DD21  je       0x56dd2e  ; -> 0056DD2E
0056DD23  mov      eax, 1
0056DD28  add      rsp, 0x20
0056DD2C  pop      rbx
0056DD2D  ret      
0056DD2E  call     0x57a440  ; -> 0057A440 fn
0056DD33  xor      ecx, ecx
0056DD35  cmp      eax, 2
0056DD38  setne    cl
0056DD3B  mov      eax, ecx
0056DD3D  add      rsp, 0x20
0056DD41  pop      rbx
0056DD42  ret      
```

## 0056DED0 (617 B, extent 0056DED0-0056E139)

Page context: "0x194 & ~6', '+0x40 & ~0x80', zeroes '+0x190'/'+0x198'/'+0xC0'/'+0x188' | | 8, 9 | '0056E2B4' / '0056E2F6' | same call pair '002D45C0' + '002445C0' — two directions of one step | | 10 | '0056E259' | '0056DED0' — directional-input helper | | 12 | '0056E269' | '00293110', '00244F00' (mark-delete), '0056E5D0' | | 14 | '0056E212' | '002470D0' | | 15 | '0056E322' | '0056DD00' gate, then '00247510(self+0x188, 0xF, (self+0x194)>>2 & 1)' ('0056"

```
0056DED0  mov      qword ptr [rsp + 8], rbx
0056DED5  mov      qword ptr [rsp + 0x10], rsi
0056DEDA  mov      qword ptr [rsp + 0x18], rdi
0056DEDF  push     r14
0056DEE1  sub      rsp, 0x20
0056DEE5  mov      rsi, qword ptr [rcx + 0xc0]
0056DEEC  mov      rbx, rcx
0056DEEF  movzx    edx, word ptr [rip + 0x2a29472]  ; -> 02F97368
0056DEF6  movzx    r9d, word ptr [rip + 0x2a2946c]  ; -> 02F9736A
0056DEFE  movzx    r8d, word ptr [rip + 0x2a29466]  ; -> 02F9736C
0056DF06  test     byte ptr [rsi + 0xe4], 2
0056DF0D  je       0x56df39  ; -> 0056DF39
0056DF0F  mov      rcx, rsi
0056DF12  call     0x56ca60  ; -> 0056CA60 fn
0056DF17  mov      rcx, qword ptr [rbx + 0xd8]
0056DF1E  call     0x2d3900  ; -> 002D3900 fn
0056DF23  mov      rbx, qword ptr [rsp + 0x30]
0056DF28  mov      rsi, qword ptr [rsp + 0x38]
0056DF2D  mov      rdi, qword ptr [rsp + 0x40]
0056DF32  add      rsp, 0x20
0056DF36  pop      r14
0056DF38  ret      
0056DF39  mov      edi, dword ptr [rcx + 0x180]
0056DF3F  mov      ecx, edi
0056DF41  shl      ecx, 0xb
0056DF44  sar      ecx, 0x1b
0056DF47  cmp      ecx, 2
0056DF4A  jl       0x56df17  ; -> 0056DF17
0056DF4C  shl      edi, 6
0056DF4F  and      edx, 0xca0
0056DF55  sar      edi, 0x1b
0056DF58  movsxd   rax, edi
0056DF5B  lea      r14, [rbx + rax*8]
0056DF5F  cmp      edx, 0x400
0056DF65  jne      0x56df7b  ; -> 0056DF7B
0056DF67  test     edx, r8d
0056DF6A  jne      0x56df88  ; -> 0056DF88
0056DF6C  cmp      edx, 0x800
0056DF72  jne      0x56dfa9  ; -> 0056DFA9
0056DF74  test     edx, r8d
0056DF77  jne      0x56dfb3  ; -> 0056DFB3
0056DF79  jmp      0x56dfcb  ; -> 0056DFCB
0056DF7B  cmp      edx, 0x80
0056DF81  jne      0x56df6c  ; -> 0056DF6C
0056DF83  test     r8b, r8b
0056DF86  jns      0x56df6c  ; -> 0056DF6C
0056DF88  test     edi, edi
0056DF8A  jle      0x56df96  ; -> 0056DF96
0056DF8C  mov      rcx, rbx
0056DF8F  call     0x563ec0  ; -> 00563EC0 fn
0056DF94  jmp      0x56dfcb  ; -> 0056DFCB
0056DF96  test     r9d, 0x480
0056DF9D  je       0x56dfcb  ; -> 0056DFCB
0056DF9F  mov      rcx, rbx
0056DFA2  call     0x563ec0  ; -> 00563EC0 fn
0056DFA7  jmp      0x56dfcb  ; -> 0056DFCB
0056DFA9  cmp      edx, 0x20
0056DFAC  jne      0x56dfcb  ; -> 0056DFCB
0056DFAE  test     dl, r8b
0056DFB1  je       0x56dfcb  ; -> 0056DFCB
0056DFB3  lea      eax, [rcx - 1]
0056DFB6  cmp      edi, eax
0056DFB8  jl       0x56dfc3  ; -> 0056DFC3
0056DFBA  test     r9d, 0x820
0056DFC1  je       0x56dfcb  ; -> 0056DFCB
0056DFC3  mov      rcx, rbx
0056DFC6  call     0x564300  ; -> 00564300 fn
0056DFCB  mov      eax, dword ptr [rbx + 0x180]
0056DFD1  shl      eax, 6
0056DFD4  sar      eax, 0x1b
0056DFD7  cmp      eax, edi
0056DFD9  je       0x56df17  ; -> 0056DF17
0056DFDF  mov      r8, qword ptr [rsi + 0xc8]
0056DFE6  test     r8, r8
0056DFE9  je       0x56e02c  ; -> 0056E02C
0056DFEB  mov      rcx, qword ptr [rbx + 0xd8]
0056DFF2  movsx    eax, word ptr [rcx + 0xf2]
0056DFF9  movsx    edx, word ptr [rcx + 0xf4]
0056E000  add      edx, eax
0056E002  movzx    eax, byte ptr [rcx + 0xec]
0056E009  imul     edx, eax
0056E00C  movsx    eax, byte ptr [rcx + 0xee]
0056E013  add      edx, eax
0056E015  movsx    eax, byte ptr [rcx + 0xed]
0056E01C  add      eax, edx
0056E01E  cdqe     
0056E020  shl      rax, 5
0056E024  movzx    eax, word ptr [rax + r8 + 8]
0056E02A  jmp      0x56e031  ; -> 0056E031
0056E02C  mov      eax, 0xffff
0056E031  mov      word ptr [r14 + 0xf0], ax
0056E039  mov      rdx, qword ptr [rbx + 0xd8]
0056E040  movsx    ecx, word ptr [rdx + 0xf2]
0056E047  movsx    eax, byte ptr [rdx + 0xee]
0056E04E  movzx    r8d, byte ptr [rdx + 0xec]
0056E056  imul     r8d, ecx
0056E05A  add      r8w, ax
0056E05E  movsx    eax, byte ptr [rdx + 0xed]
0056E065  add      r8w, ax
0056E069  mov      word ptr [r14 + 0xf2], r8w
0056E071  mov      r9, qword ptr [rbx + 0xd8]
0056E078  movzx    edx, word ptr [r9 + 0xf4]
0056E080  add      dx, word ptr [r9 + 0xf2]
0056E088  movzx    eax, byte ptr [r9 + 0xec]
0056E090  movsx    r8d, dx
0056E094  imul     r8d, eax
0056E098  movsx    eax, byte ptr [r9 + 0xee]
0056E0A0  add      r8w, ax
0056E0A4  movsx    eax, byte ptr [r9 + 0xed]
0056E0AC  add      r8w, ax
0056E0B0  mov      word ptr [r14 + 0xf4], r8w
0056E0B8  mov      eax, dword ptr [rbx + 0x180]
0056E0BE  shl      eax, 6
0056E0C1  movsxd   rcx, eax
0056E0C4  sar      rcx, 0x1b
0056E0C8  add      rcx, 0x1e
0056E0CC  lea      rdx, [rbx + rcx*8]
0056E0D0  mov      rcx, qword ptr [rbx + 0xc8]
0056E0D7  call     0x5674b0  ; -> 005674B0 fn
0056E0DC  mov      eax, dword ptr [rbx + 0x180]
0056E0E2  shl      eax, 6
0056E0E5  movsxd   rcx, eax
0056E0E8  sar      rcx, 0x1b
0056E0EC  movsx    ecx, byte ptr [rbx + rcx*8 + 0xf7]
0056E0F4  call     0x56dc30  ; -> 0056DC30 fn
0056E0F9  mov      r8d, dword ptr [rbx + 0x194]
0056E100  mov      rcx, rbx
0056E103  and      r8d, 1
0056E107  movzx    edx, al
0056E10A  mov      byte ptr [rbx + 0x191], al
0056E110  call     0x56c950  ; -> 0056C950 fn
0056E115  mov      rcx, rbx
0056E118  call     0x56e410  ; -> 0056E410 fn
0056E11D  mov      edx, 1
0056E122  mov      rcx, rbx
0056E125  call     0x56e5d0  ; -> 0056E5D0 fn
0056E12A  mov      ecx, 0xa
0056E12F  call     0x249c60  ; -> 00249C60 fn
0056E134  jmp      0x56df23  ; -> 0056DF23
```

## 0057B6A0 (78 B, extent 0057B6A0-0057B6EE)

Page context: "hooses the style byte '01E0C3D0' or '01E0C3DC'; it then builds a **0x18-byte element descriptor** on the stack — flags 3, that style byte, the byte '01E0C3CC', a word of '−1', and the two procedures '0057B6A0' and '0057C010' ('0057A593'–'0057A5D3') — and creates the element through '003F47E0(twinResult, &+0xC0, descriptor, [02CA9790]+0x158)', which is a thin wrapper that calls the widget factory '00244F50' with procedure '003F4840' and "

```
0057B6A0  sub      rsp, 0x28
0057B6A4  call     0x2ca110  ; -> 002CA110 fn
0057B6A9  mov      rcx, qword ptr [rip + 0x272e0e8]  ; -> 02CA9798
0057B6B0  test     rcx, rcx
0057B6B3  je       0x57b6ba  ; -> 0057B6BA
0057B6B5  call     0x244dd0  ; -> 00244DD0 fn
0057B6BA  xor      edx, edx
0057B6BC  xor      ecx, ecx
0057B6BE  call     0x291d80  ; -> 00291D80 fn
0057B6C3  xor      edx, edx
0057B6C5  xor      ecx, ecx
0057B6C7  call     0x293110  ; -> 00293110 fn
0057B6CC  call     0x5112a0  ; -> 005112A0 fn
0057B6D1  mov      rcx, qword ptr [rip + 0x272e0b8]  ; -> 02CA9790
0057B6D8  or       dword ptr [rcx + 0x150], 4
0057B6DF  call     0x244dd0  ; -> 00244DD0 fn
0057B6E4  mov      eax, 0xc
0057B6E9  add      rsp, 0x28
0057B6ED  ret      
```
