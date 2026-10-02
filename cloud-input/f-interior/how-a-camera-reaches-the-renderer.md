# F-interior pack: `17-Presentation-Rendering/Scripted-Camera/how-a-camera-reaches-the-renderer.md`

Generated 2026-10-02 09:51 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/how-a-camera-reaches-the-renderer.json`.

Functions: 10. Each is cited on the page only at its entry and is still in the F frontier.

## 001824E0 (72 B, extent 001824E0-00182528)

Page context: "working camera**. Eye, target and roll are treated identically in both, so the two matrices should agree; what the second field-of-view float is for was not established.  A field-of-view adjustment ('001824E0') is applied to the working camera and its projection scale recomputed; the projection is built with the aspect ratio of section 3.  **The small bodies under it, read so that naming them says something.** '003CBA50' '(camera, out, "

```
001824E0  mov      qword ptr [rsp + 8], rbx
001824E5  mov      qword ptr [rsp + 0x10], rsi
001824EA  push     rdi
001824EB  sub      rsp, 0x20
001824EF  mov      rbx, r8
001824F2  mov      rdi, rdx
001824F5  mov      rsi, rcx
001824F8  call     0x189120  ; -> 00189120 fn
001824FD  test     rax, rax
00182500  je       0x182518  ; -> 00182518
00182502  call     0x189120  ; -> 00189120 fn
00182507  mov      rcx, rax
0018250A  mov      r9, rbx
0018250D  mov      r8, rdi
00182510  mov      rdx, rsi
00182513  call     0x186ab0  ; -> 00186AB0 fn
00182518  mov      rbx, qword ptr [rsp + 0x30]
0018251D  mov      rsi, qword ptr [rsp + 0x38]
00182522  add      rsp, 0x20
00182526  pop      rdi
00182527  ret      
```

## 00182570 (33 B, extent 00182570-00182591)

Page context: "es those and recomputes '+0x10', writing the field of view to both '+8' and '+0xC'. '003B4150' (15 B) copies a matrix to '02B40470', a second classifier matrix beside the one the cull test installs. '00182570' (33 B) returns byte '+0x1C' of the render device object, and '001824E0' (72 B) forwards the address of the field of view and two zeros to a method of the same object.  Then, in order:  | matrix | how it is produced | what reads it"

```
00182570  sub      rsp, 0x28
00182574  call     0x189120  ; -> 00189120 fn
00182579  test     rax, rax
0018257C  je       0x18258c  ; -> 0018258C
0018257E  call     0x189120  ; -> 00189120 fn
00182583  movzx    eax, byte ptr [rax + 0x1c]
00182587  add      rsp, 0x28
0018258B  ret      
0018258C  add      rsp, 0x28
00182590  ret      
```

## 0034A370 (59 B, extent 0034A370-0034A3AB)

Page context: "A60') pop their arguments with 'VMValueStack_PopInt32CoerceFloat32' '00267E10' (and '00349730' pushes a result with 'VMValueStack_PushInt32' '00267F90') and call the start '003DD230'; '00349ED0' and '0034A370' call the stop '003DD320'; '0034B100' calls the clear '003DCF60'; '0034C7E0' calls '00358320', which returns the current draw index as a signed byte; '00357F00' calls '003DA190', a 3-byte function that returns its argument; and 20 "

```
0034A370  mov      qword ptr [rsp + 8], rbx
0034A375  push     rdi
0034A376  sub      rsp, 0x20
0034A37A  xor      edx, edx
0034A37C  mov      rcx, r9
0034A37F  mov      rdi, r9
0034A382  call     0x267f90  ; -> 00267F90 fn
0034A387  call     0x2640c0  ; -> 002640C0 fn
0034A38C  mov      rcx, rdi
0034A38F  mov      rbx, rax
0034A392  call     0x267e10  ; -> 00267E10 fn
0034A397  mov      edx, eax
0034A399  mov      rcx, rbx
0034A39C  mov      rbx, qword ptr [rsp + 0x30]
0034A3A1  add      rsp, 0x20
0034A3A5  pop      rdi
0034A3A6  jmp      0x3dd320  ; -> 003DD320 fn
```

## 00357F00 (414 B, extent 00357F00-0035809E)

Page context: "l the start '003DD230'; '00349ED0' and '0034A370' call the stop '003DD320'; '0034B100' calls the clear '003DCF60'; '0034C7E0' calls '00358320', which returns the current draw index as a signed byte; '00357F00' calls '003DA190', a 3-byte function that returns its argument; and 20 script bodies call the slot accessor '00263FF0', among them '0033F7F0', '00342490', '0034E460', '003574B0' and '0050D0C0'. Scripts start, stop and clear shakes "

```
00357F00  mov      qword ptr [rsp + 8], rbx
00357F05  mov      qword ptr [rsp + 0x10], rsi
00357F0A  push     rdi
00357F0B  sub      rsp, 0x30
00357F0F  mov      rcx, rdx
00357F12  mov      rsi, r8
00357F15  mov      rdi, rdx
00357F18  call     0x263f10  ; -> 00263F10 fn
00357F1D  mov      rcx, rdi
00357F20  mov      rbx, rax
00357F23  call     0x263f40  ; -> 00263F40 fn
00357F28  mov      rcx, rbx
00357F2B  mov      rdi, rax
00357F2E  call     0x2ea6a0  ; -> 002EA6A0 fn
00357F33  test     eax, eax
00357F35  jne      0x357f47  ; -> 00357F47
00357F37  mov      rbx, qword ptr [rsp + 0x40]
00357F3C  mov      rsi, qword ptr [rsp + 0x48]
00357F41  add      rsp, 0x30
00357F45  pop      rdi
00357F46  ret      
00357F47  movsx    rax, word ptr [rsi]
00357F4B  cmp      eax, 5
00357F4E  ja       0x358085  ; -> 00358085
00357F54  lea      rdx, [rip - 0x237f5b]  ; -> 00120000 (image base)
00357F5B  mov      ecx, dword ptr [rdx + rax*4 + 0x2380a0]  ; image base + 0x2380a0 = 003580A0
00357F62  add      rcx, rdx
00357F65  jmp      rcx
00357F67  mov      ebx, 1
00357F6C  mov      word ptr [rsi], bx
00357F6F  mov      eax, 2
00357F74  mov      word ptr [rsi], ax
00357F77  mov      rcx, rdi
00357F7A  call     0x2e71c0  ; -> 002E71C0 fn
00357F7F  test     eax, eax
00357F81  jne      0x358085  ; -> 00358085
00357F87  mov      eax, 3
00357F8C  jmp      0x358082  ; -> 00358082
00357F91  mov      rcx, rdi
00357F94  call     0x2e9b40  ; -> 002E9B40 fn
00357F99  cmp      byte ptr [rsi + 2], 0
00357F9D  mov      dword ptr [rsi + 8], eax
00357FA0  je       0x357fd2  ; -> 00357FD2
00357FA2  xorps    xmm1, xmm1
00357FA5  mov      rcx, rdi
00357FA8  call     0x2e5bc0  ; -> 002E5BC0 fn
00357FAD  mov      ecx, 4
00357FB2  xor      edx, edx
00357FB4  mov      word ptr [rsi], cx
00357FB7  lea      r8d, [rcx - 3]
00357FBB  mov      rcx, rdi
00357FBE  call     0x2ecf10  ; -> 002ECF10 fn
00357FC3  xor      edx, edx
00357FC5  mov      rcx, rdi
00357FC8  call     0x2e8540  ; -> 002E8540 fn
00357FCD  jmp      0x358085  ; -> 00358085
00357FD2  mov      ecx, 4
00357FD7  mov      ebx, 1
00357FDC  mov      word ptr [rsi], cx
00357FDF  mov      r8d, ebx
00357FE2  mov      rcx, rdi
00357FE5  mov      edx, ebx
00357FE7  call     0x2ecf10  ; -> 002ECF10 fn
00357FEC  mov      edx, ebx
00357FEE  mov      rcx, rdi
00357FF1  call     0x2e8540  ; -> 002E8540 fn
00357FF6  jmp      0x358085  ; -> 00358085
00357FFB  cmp      byte ptr [rsi + 2], 0
00357FFF  mov      rcx, rdi
00358002  je       0x35803e  ; -> 0035803E
00358004  call     0x2e71c0  ; -> 002E71C0 fn
00358009  test     eax, eax
0035800B  je       0x358047  ; -> 00358047
0035800D  mov      rcx, rdi
00358010  movaps   xmmword ptr [rsp + 0x20], xmm6
00358015  call     0x2e4e00  ; -> 002E4E00 fn
0035801A  mov      ecx, 0x10
0035801F  movaps   xmm6, xmm0
00358022  call     0x3da190  ; -> 003DA190 fn
00358027  movd     xmm1, eax
0035802B  cvtdq2ps xmm1, xmm1
0035802E  comiss   xmm6, xmm1
00358031  movaps   xmm6, xmmword ptr [rsp + 0x20]
00358036  jb       0x358085  ; -> 00358085
00358038  mov      byte ptr [rsi + 3], 1
0035803C  jmp      0x358047  ; -> 00358047
0035803E  call     0x2e71c0  ; -> 002E71C0 fn
00358043  test     eax, eax
00358045  jne      0x358085  ; -> 00358085
00358047  mov      eax, 5
0035804C  mov      word ptr [rsi], ax
0035804F  cmp      dword ptr [rsi + 4], 0
00358053  je       0x35807d  ; -> 0035807D
00358055  cmp      byte ptr [rsi + 3], 0
00358059  xorps    xmm3, xmm3
0035805C  je       0x35806f  ; -> 0035806F
0035805E  mov      ecx, 4
00358063  call     0x3da190  ; -> 003DA190 fn
00358068  movd     xmm3, eax
0035806C  cvtdq2ps xmm3, xmm3
0035806F  mov      r8d, dword ptr [rsi + 0xc]
00358073  xor      edx, edx
00358075  mov      rcx, rdi
00358078  call     0x3ddb40  ; -> 003DDB40 fn
0035807D  mov      eax, 7
00358082  mov      word ptr [rsi], ax
00358085  mov      rbx, qword ptr [rsp + 0x40]
0035808A  xor      eax, eax
0035808C  cmp      word ptr [rsi], 7
00358090  mov      rsi, qword ptr [rsp + 0x48]
00358095  setne    al
00358098  add      rsp, 0x30
0035809C  pop      rdi
0035809D  ret      
```

## 0037DB40 (35 B, extent 0037DB40-0037DB63)

Page context: "nd otherwise names the draw of the frame (0 or 1, [what happens between two frames](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md) section 4.3) the channel applies to. '0037DB40' '(record, channel, tag)' (35 B) stores a tag; '0037DCC0' '(record, channel)' (35 B) returns the dword just below it, the channel's status.  **The reset - '0037D890'** (209 B) stores -1 in all twenty draw tags, calls the setter wit"

```
0037DB40  movsxd   rax, ecx
0037DB43  imul     r9, rax, 0x3d0
0037DB4A  movsxd   rax, edx
0037DB4D  imul     rcx, rax, 0xf0
0037DB54  lea      rax, [rip + 0x275ff21]  ; -> 02ADDA7C
0037DB5B  add      r9, rcx
0037DB5E  mov      dword ptr [r9 + rax], r8d
0037DB62  ret      
```

## 0037DCC0 (35 B, extent 0037DCC0-0037DCE3)

Page context: "appens between two frames](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md) section 4.3) the channel applies to. '0037DB40' '(record, channel, tag)' (35 B) stores a tag; '0037DCC0' '(record, channel)' (35 B) returns the dword just below it, the channel's status.  **The reset - '0037D890'** (209 B) stores -1 in all twenty draw tags, calls the setter with zero vectors and zero scalars, and zeroes the two accum"

```
0037DCC0  movsxd   rax, ecx
0037DCC3  imul     r8, rax, 0x3d0
0037DCCA  movsxd   rcx, edx
0037DCCD  lea      rax, [rip + 0x275fda4]  ; -> 02ADDA78
0037DCD4  imul     rdx, rcx, 0xf0
0037DCDB  add      r8, rdx
0037DCDE  mov      eax, dword ptr [r8 + rax]
0037DCE2  ret      
```

## 00382080 (58 B, extent 00382080-003820BA)

Page context: "erior anchor '003CBE17' (a '00380190' call).   ## SWE2-EC7-53 update (2026-09-19) - '00233230'  '00233230' (524 B) is a Movement-owned helper the camera page names - '0022FF10'/'002324F0'/'00233050'/'00382080'/'00808C40'. Interior anchor '00233253' (a '00382080' call).  ## SWE2-EC7-54 update (2026-09-19) - '00380650'  '00380650' (427 B) is a call-free vector magnitude - 'x*x + y*y + z*z' mulss/addss chain on '[rcx]'/'[rcx+4]'/'[rcx+8]' "

```
00382080  xor      edx, edx
00382082  lea      rax, [rip + 0x2b3d1ef]  ; -> 02EBF278
00382089  lea      ecx, [rdx + 4]
0038208C  nop      dword ptr [rax]
00382090  mov      qword ptr [rax], rdx
00382093  mov      qword ptr [rax + 8], rdx
00382097  mov      qword ptr [rax + 0x10], rdx
0038209B  lea      rax, [rax + 0x40]
0038209F  mov      qword ptr [rax - 0x28], rdx
003820A3  mov      qword ptr [rax - 0x20], rdx
003820A7  mov      qword ptr [rax - 0x18], rdx
003820AB  mov      qword ptr [rax - 0x10], rdx
003820AF  mov      qword ptr [rax - 8], rdx
003820B3  sub      rcx, 1
003820B7  jne      0x382090  ; -> 00382090
003820B9  ret      
```

## 003CBA50 (114 B, extent 003CBA50-003CBAC2)

Page context: "pplied to the working camera and its projection scale recomputed; the projection is built with the aspect ratio of section 3.  **The small bodies under it, read so that naming them says something.** '003CBA50' '(camera, out, aspect, k)' (114 B) is the perspective projection: with 's = k x camera[+0x10]' it writes 'out[0][0] = s / aspect', 'out[1][1] = s', 'out[2][2] = -(near + far) / (far - near)', 'out[2][3] = -1', 'out[3][2] = -2 x ne"

```
003CBA50  mulss    xmm3, dword ptr [rcx + 0x10]
003CBA55  xor      eax, eax
003CBA57  movss    xmm1, dword ptr [rcx + 4]
003CBA5C  subss    xmm1, dword ptr [rcx]
003CBA60  movss    dword ptr [rdx + 0x14], xmm3
003CBA65  movaps   xmm0, xmm3
003CBA68  divss    xmm0, xmm2
003CBA6C  mov      qword ptr [rdx + 4], rax
003CBA70  mov      qword ptr [rdx + 0xc], rax
003CBA74  mov      qword ptr [rdx + 0x18], rax
003CBA78  mov      qword ptr [rdx + 0x20], rax
003CBA7C  movss    dword ptr [rdx], xmm0
003CBA80  movss    xmm0, dword ptr [rcx]
003CBA84  addss    xmm0, dword ptr [rcx + 4]
003CBA89  mov      dword ptr [rdx + 0x2c], 0xbf800000
003CBA90  mov      qword ptr [rdx + 0x30], rax
003CBA94  divss    xmm0, xmm1
003CBA98  xorps    xmm0, xmmword ptr [rip + 0x1920301]  ; -> 01CEBDA0 [f32x4 -0, -0, -0, -0]
003CBA9F  movss    dword ptr [rdx + 0x28], xmm0
003CBAA4  movss    xmm0, dword ptr [rcx]
003CBAA8  mulss    xmm0, dword ptr [rcx + 4]
003CBAAD  mov      dword ptr [rdx + 0x3c], eax
003CBAB0  mulss    xmm0, dword ptr [rip + 0x527690]  ; -> 008F3148 [f32 -2]
003CBAB8  divss    xmm0, xmm1
003CBABC  movss    dword ptr [rdx + 0x38], xmm0
003CBAC1  ret      
```

## 003CBC40 (91 B, extent 003CBC40-003CBC9B)

Page context: "[2][2] = -(near + far) / (far - near)', 'out[2][3] = -1', 'out[3][2] = -2 x near x far / (far - near)' and zeroes the rest - so **the camera record's '+0' is the near plane and '+4' the far plane**. '003CBC40' '(camera, fov, near, far)' (91 B) stores those and recomputes '+0x10', writing the field of view to both '+8' and '+0xC'. '003B4150' (15 B) copies a matrix to '02B40470', a second classifier matrix beside the one the cull test ins"

```
003CBC40  push     rbx
003CBC42  sub      rsp, 0x20
003CBC46  movss    dword ptr [rcx + 8], xmm1
003CBC4B  mov      rbx, rcx
003CBC4E  movss    dword ptr [rcx + 0xc], xmm1
003CBC53  mulss    xmm1, dword ptr [rip + 0x191ff15]  ; -> 01CEBB70 [f32 0.5]
003CBC5B  movss    dword ptr [rcx], xmm2
003CBC5F  movss    dword ptr [rcx + 4], xmm3
003CBC64  movaps   xmm0, xmm1
003CBC67  call     0x861f1a  ; -> 00861F1A fn
003CBC6C  movaps   xmm2, xmm0
003CBC6F  xorps    xmm1, xmm1
003CBC72  ucomiss  xmm2, xmm1
003CBC75  jp       0x3cbc84  ; -> 003CBC84
003CBC77  jne      0x3cbc84  ; -> 003CBC84
003CBC79  movss    dword ptr [rbx + 0x10], xmm1
003CBC7E  add      rsp, 0x20
003CBC82  pop      rbx
003CBC83  ret      
003CBC84  movss    xmm0, dword ptr [rip + 0x191ff1c]  ; -> 01CEBBA8 [f32 1]
003CBC8C  divss    xmm0, xmm2
003CBC90  movss    dword ptr [rbx + 0x10], xmm0
003CBC95  add      rsp, 0x20
003CBC99  pop      rbx
003CBC9A  ret      
```

## 003DA190 (3 B, extent 003DA190-003DA193)

Page context: "me it (1) sets the draw tags of the two channels named by the words at '+0x1C' and '+0x1E' (a negative word, or a driver whose state is 0, is skipped) from that driver's second dword (passed through '003DA190', which is three bytes and returns its argument); (2) for each of the four drivers whose state is non-zero, evaluates the channel at the driver's time with '0037D1F0' '(record, data id, time, channel)'; (3) reads the channel's stat"

```
003DA190  mov      eax, ecx
003DA192  ret      
```
