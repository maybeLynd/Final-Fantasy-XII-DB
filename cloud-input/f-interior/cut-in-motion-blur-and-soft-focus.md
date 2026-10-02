# F-interior pack: `17-Presentation-Rendering/Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md`

Generated 2026-10-02 09:51 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/cut-in-motion-blur-and-soft-focus.json`.

Functions: 12. Each is cited on the page only at its entry and is still in the F frontier.

## 003DE240 (91 B, extent 003DE240-003DE29B)

Page context: "ading ('moveblurfade(frames)', 'moveblurclearfade(frames)', 'moveblurfadesync()').** Both fade verbs scale the frame count by the frame-rate word; **a result of 0 plays ('003DE2A0', 98 B) or clears ('003DE240', 91 B) at once**. Otherwise, if no fade is running, they take a scheduled-task record, remember it at '02B58C48', and give it a tick callback '003DE160' (129 B), an end callback '003DE1F0' (22 B), the duration, and a direction at "

```
003DE240  push     rbx
003DE242  sub      rsp, 0x20
003DE246  call     0x265860  ; -> 00265860 fn
003DE24B  mov      ebx, eax
003DE24D  test     eax, eax
003DE24F  jne      0x3de25b  ; -> 003DE25B
003DE251  add      rsp, 0x20
003DE255  pop      rbx
003DE256  jmp      0x24eb20  ; -> 0024EB20 fn
003DE25B  cmp      qword ptr [rip + 0x277a9e5], 0  ; -> 02B58C48
003DE263  jne      0x3de295  ; -> 003DE295
003DE265  call     0x2f16b0  ; -> 002F16B0 fn
003DE26A  lea      rcx, [rip - 0x111]  ; -> 003DE160
003DE271  mov      qword ptr [rip + 0x277a9d0], rax  ; -> 02B58C48
003DE278  mov      qword ptr [rax + 0x10], rcx
003DE27C  lea      rcx, [rip - 0x93]  ; -> 003DE1F0
003DE283  mov      qword ptr [rax + 8], rcx
003DE287  mov      dword ptr [rax + 4], ebx
003DE28A  mov      dword ptr [rax + 0x28], 1
003DE291  mov      byte ptr [rax + 0x20], 0
003DE295  add      rsp, 0x20
003DE299  pop      rbx
003DE29A  ret      
```

## 003DE2A0 (98 B, extent 003DE2A0-003DE302)

Page context: "rs are the frame page's.  **Fading ('moveblurfade(frames)', 'moveblurclearfade(frames)', 'moveblurfadesync()').** Both fade verbs scale the frame count by the frame-rate word; **a result of 0 plays ('003DE2A0', 98 B) or clears ('003DE240', 91 B) at once**. Otherwise, if no fade is running, they take a scheduled-task record, remember it at '02B58C48', and give it a tick callback '003DE160' (129 B), an end callback '003DE1F0' (22 B), the "

```
003DE2A0  push     rbx
003DE2A2  sub      rsp, 0x20
003DE2A6  call     0x265860  ; -> 00265860 fn
003DE2AB  mov      ebx, eax
003DE2AD  test     eax, eax
003DE2AF  jne      0x3de2c2  ; -> 003DE2C2
003DE2B1  lea      rcx, [rip + 0x277a980]  ; -> 02B58C38
003DE2B8  add      rsp, 0x20
003DE2BC  pop      rbx
003DE2BD  jmp      0x24ec00  ; -> 0024EC00 fn
003DE2C2  cmp      qword ptr [rip + 0x277a97e], 0  ; -> 02B58C48
003DE2CA  jne      0x3de2fc  ; -> 003DE2FC
003DE2CC  call     0x2f16b0  ; -> 002F16B0 fn
003DE2D1  lea      rcx, [rip - 0x178]  ; -> 003DE160
003DE2D8  mov      qword ptr [rip + 0x277a969], rax  ; -> 02B58C48
003DE2DF  mov      qword ptr [rax + 0x10], rcx
003DE2E3  lea      rcx, [rip - 0xfa]  ; -> 003DE1F0
003DE2EA  mov      qword ptr [rax + 8], rcx
003DE2EE  mov      dword ptr [rax + 4], ebx
003DE2F1  mov      dword ptr [rax + 0x28], 0
003DE2F8  mov      byte ptr [rax + 0x20], 0
003DE2FC  add      rsp, 0x20
003DE300  pop      rbx
003DE301  ret      
```

## 003DE360 (51 B, extent 003DE360-003DE393)

Page context: "-|---| | '+0' byte | 'moveblurpresettype(n)' ('003DE400') | preset: 'n' = 1 -> 2, 2 -> 3, anything else 1. Chooses one of three constant sets in '003AAA50' | 1 | | '+1' byte | 'moveblurcluttype(n)' ('003DE360', 51 B) | mask: 'n' = 1 -> 2, 2 -> 3, 3 -> 0, anything else 1. 1-3 are three 256-entry tables embedded at '01EFACA0', '01EFB0A0', '01EFB4A0' (created once into '02B3F420..30'); 0 means a caller-supplied table, which no path here su"

```
003DE360  test     ecx, ecx
003DE362  je       0x3de38b  ; -> 003DE38B
003DE364  sub      ecx, 1
003DE367  je       0x3de383  ; -> 003DE383
003DE369  sub      ecx, 1
003DE36C  je       0x3de37b  ; -> 003DE37B
003DE36E  cmp      ecx, 1
003DE371  jne      0x3de38b  ; -> 003DE38B
003DE373  mov      byte ptr [rip + 0x277a8bf], 0  ; -> 02B58C39
003DE37A  ret      
003DE37B  mov      byte ptr [rip + 0x277a8b7], 3  ; -> 02B58C39
003DE382  ret      
003DE383  mov      byte ptr [rip + 0x277a8af], 2  ; -> 02B58C39
003DE38A  ret      
003DE38B  mov      byte ptr [rip + 0x277a8a7], 1  ; -> 02B58C39
003DE392  ret      
```

## 003DE3A0 (51 B, extent 003DE3A0-003DE3D3)

Page context: "try tables embedded at '01EFACA0', '01EFB0A0', '01EFB4A0' (created once into '02B3F420..30'); 0 means a caller-supplied table, which no path here supplies | 1 | | '+2' byte | 'moveblurnoisetype(n)' ('003DE3A0', 51 B) | 0..3 stored as is, anything else 0. **Copied into the request and never read by '003AAA50'** | 0 | | '+3' byte | 'moveblurscreentype(n)' ('003DE430') | 'n' = 1 -> 2, anything else 1. Play returns *without raising the bit*"

```
003DE3A0  test     ecx, ecx
003DE3A2  je       0x3de3cb  ; -> 003DE3CB
003DE3A4  sub      ecx, 1
003DE3A7  je       0x3de3c3  ; -> 003DE3C3
003DE3A9  sub      ecx, 1
003DE3AC  je       0x3de3bb  ; -> 003DE3BB
003DE3AE  cmp      ecx, 1
003DE3B1  jne      0x3de3cb  ; -> 003DE3CB
003DE3B3  mov      byte ptr [rip + 0x277a880], 3  ; -> 02B58C3A
003DE3BA  ret      
003DE3BB  mov      byte ptr [rip + 0x277a878], 2  ; -> 02B58C3A
003DE3C2  ret      
003DE3C3  mov      byte ptr [rip + 0x277a870], 1  ; -> 02B58C3A
003DE3CA  ret      
003DE3CB  mov      byte ptr [rip + 0x277a868], 0  ; -> 02B58C3A
003DE3D2  ret      
```

## 003DE400 (38 B, extent 003DE400-003DE426)

Page context: "s centre.  ## 4. Motion blur  **Staging block '02B58C38'**, copied by play to '02092678':  | offset | verb | meaning | 'resetmoveblurparam' | |---|---|---|---| | '+0' byte | 'moveblurpresettype(n)' ('003DE400') | preset: 'n' = 1 -> 2, 2 -> 3, anything else 1. Chooses one of three constant sets in '003AAA50' | 1 | | '+1' byte | 'moveblurcluttype(n)' ('003DE360', 51 B) | mask: 'n' = 1 -> 2, 2 -> 3, 3 -> 0, anything else 1. 1-3 are three 2"

```
003DE400  test     ecx, ecx
003DE402  je       0x3de41e  ; -> 003DE41E
003DE404  sub      ecx, 1
003DE407  je       0x3de416  ; -> 003DE416
003DE409  cmp      ecx, 1
003DE40C  jne      0x3de41e  ; -> 003DE41E
003DE40E  mov      byte ptr [rip + 0x277a823], 3  ; -> 02B58C38
003DE415  ret      
003DE416  mov      byte ptr [rip + 0x277a81b], 2  ; -> 02B58C38
003DE41D  ret      
003DE41E  mov      byte ptr [rip + 0x277a813], 1  ; -> 02B58C38
003DE425  ret      
```

## 003DE430 (24 B, extent 003DE430-003DE448)

Page context: " | | '+2' byte | 'moveblurnoisetype(n)' ('003DE3A0', 51 B) | 0..3 stored as is, anything else 0. **Copied into the request and never read by '003AAA50'** | 0 | | '+3' byte | 'moveblurscreentype(n)' ('003DE430') | 'n' = 1 -> 2, anything else 1. Play returns *without raising the bit* for any other stored value; the builder uses the pair of thresholds '0x200' / '0x1C0' for 2 and '0x100' / '0xE0' for 1 | 1 | | '+4' bit 0 | 'moveblurcaptureo"

```
003DE430  test     ecx, ecx
003DE432  je       0x3de440  ; -> 003DE440
003DE434  mov      byte ptr [rip + 0x277a800], 2  ; -> 02B58C3B
003DE43B  cmp      ecx, 1
003DE43E  je       0x3de447  ; -> 003DE447
003DE440  mov      byte ptr [rip + 0x277a7f4], 1  ; -> 02B58C3B
003DE447  ret      
```

## 003DF950 (27 B, extent 003DF950-003DF96B)

Page context: "' | 'cutinlinewidth(w)' ('003DF9B0') | line width | 2.0 | | '+0x14', '+0x18' | 'cutinuv(u, v)' ('003DFA30') | origin of the picture's texture rectangle | 0, 0 | | '+0x1C' | 'cutincolor(a, b, c, d)' ('003DF950') | four bytes in argument order - the picture's colour | '80 80 80 80' | | '+0x20' | 'cutinlinecolor(a, b, c, d)' ('003DF970') | four bytes in argument order - the line colour | '00 00 00 80' |  'resetcutinparam' is '003DF900' (79"

```
003DF950  mov      byte ptr [rip + 0x277a3e6], cl  ; -> 02B59D3C
003DF956  mov      byte ptr [rip + 0x277a3e1], dl  ; -> 02B59D3D
003DF95C  mov      byte ptr [rip + 0x277a3db], r8b  ; -> 02B59D3E
003DF963  mov      byte ptr [rip + 0x277a3d5], r9b  ; -> 02B59D3F
003DF96A  ret      
```

## 003DF970 (27 B, extent 003DF970-003DF98B)

Page context: "cture's texture rectangle | 0, 0 | | '+0x1C' | 'cutincolor(a, b, c, d)' ('003DF950') | four bytes in argument order - the picture's colour | '80 80 80 80' | | '+0x20' | 'cutinlinecolor(a, b, c, d)' ('003DF970') | four bytes in argument order - the line colour | '00 00 00 80' |  'resetcutinparam' is '003DF900' (79 B) and 'cutinplay' is '003DF8F0', which passes the staging block to '0024CF50'. **Play only allocates if the effect is not al"

```
003DF970  mov      byte ptr [rip + 0x277a3ca], cl  ; -> 02B59D40
003DF976  mov      byte ptr [rip + 0x277a3c5], dl  ; -> 02B59D41
003DF97C  mov      byte ptr [rip + 0x277a3bf], r8b  ; -> 02B59D42
003DF983  mov      byte ptr [rip + 0x277a3b9], r9b  ; -> 02B59D43
003DF98A  ret      
```

## 003DF990 (23 B, extent 003DF990-003DF9A7)

Page context: ")' ('003DF9F0', 64 B) | type: 'n' = 0..4 stored as is, anything else 2. **Type 0 is "no cut-in"**: the per-frame body returns at once while this byte is 0 | 2 | | '+1' bit 0 | 'cutinlinefade(flag)' ('003DF990') | clears the alpha of the second copy of the line colour | 0 | | '+4', '+8' | 'cutinpos(x, y)' ('003DF9C0') | position | 0, 0 | | '+0xC' | 'cutinrotate(angle)' ('003DF9E0') | rotation, radians (the literal values in the scripts a"

```
003DF990  movzx    eax, byte ptr [rip + 0x277a38a]  ; -> 02B59D21
003DF997  test     ecx, ecx
003DF999  setne    cl
003DF99C  and      al, 0xfe
003DF99E  or       cl, al
003DF9A0  mov      byte ptr [rip + 0x277a37b], cl  ; -> 02B59D21
003DF9A6  ret      
```

## 003DF9C0 (17 B, extent 003DF9C0-003DF9D1)

Page context: "rame body returns at once while this byte is 0 | 2 | | '+1' bit 0 | 'cutinlinefade(flag)' ('003DF990') | clears the alpha of the second copy of the line colour | 0 | | '+4', '+8' | 'cutinpos(x, y)' ('003DF9C0') | position | 0, 0 | | '+0xC' | 'cutinrotate(angle)' ('003DF9E0') | rotation, radians (the literal values in the scripts are 0.524, 0.698 and -1.65: 30, 40 and about -94.5 degrees) | 0 | | '+0x10' | 'cutinlinewidth(w)' ('003DF9B0'"

```
003DF9C0  movss    dword ptr [rip + 0x277a35c], xmm0  ; -> 02B59D24
003DF9C8  movss    dword ptr [rip + 0x277a358], xmm1  ; -> 02B59D28
003DF9D0  ret      
```

## 003DF9F0 (64 B, extent 003DF9F0-003DFA30)

Page context: "aging block '02B59D20'** - and, after 'cutinplay', the live copy at '02092640' with the same offsets:  | offset | verb | meaning | 'resetcutinparam' | |---|---|---|---| | '+0' byte | 'cutintype(n)' ('003DF9F0', 64 B) | type: 'n' = 0..4 stored as is, anything else 2. **Type 0 is "no cut-in"**: the per-frame body returns at once while this byte is 0 | 2 | | '+1' bit 0 | 'cutinlinefade(flag)' ('003DF990') | clears the alpha of the second c"

```
003DF9F0  test     ecx, ecx
003DF9F2  je       0x3dfa28  ; -> 003DFA28
003DF9F4  sub      ecx, 1
003DF9F7  je       0x3dfa20  ; -> 003DFA20
003DF9F9  sub      ecx, 1
003DF9FC  je       0x3dfa18  ; -> 003DFA18
003DF9FE  sub      ecx, 1
003DFA01  je       0x3dfa10  ; -> 003DFA10
003DFA03  cmp      ecx, 1
003DFA06  jne      0x3dfa18  ; -> 003DFA18
003DFA08  mov      byte ptr [rip + 0x277a311], 4  ; -> 02B59D20
003DFA0F  ret      
003DFA10  mov      byte ptr [rip + 0x277a309], 3  ; -> 02B59D20
003DFA17  ret      
003DFA18  mov      byte ptr [rip + 0x277a301], 2  ; -> 02B59D20
003DFA1F  ret      
003DFA20  mov      byte ptr [rip + 0x277a2f9], 1  ; -> 02B59D20
003DFA27  ret      
003DFA28  mov      byte ptr [rip + 0x277a2f1], 0  ; -> 02B59D20
003DFA2F  ret      
```

## 003DFA30 (17 B, extent 003DFA30-003DFA41)

Page context: "iteral values in the scripts are 0.524, 0.698 and -1.65: 30, 40 and about -94.5 degrees) | 0 | | '+0x10' | 'cutinlinewidth(w)' ('003DF9B0') | line width | 2.0 | | '+0x14', '+0x18' | 'cutinuv(u, v)' ('003DFA30') | origin of the picture's texture rectangle | 0, 0 | | '+0x1C' | 'cutincolor(a, b, c, d)' ('003DF950') | four bytes in argument order - the picture's colour | '80 80 80 80' | | '+0x20' | 'cutinlinecolor(a, b, c, d)' ('003DF970') "

```
003DFA30  movss    dword ptr [rip + 0x277a2fc], xmm0  ; -> 02B59D34
003DFA38  movss    dword ptr [rip + 0x277a2f8], xmm1  ; -> 02B59D38
003DFA40  ret      
```
