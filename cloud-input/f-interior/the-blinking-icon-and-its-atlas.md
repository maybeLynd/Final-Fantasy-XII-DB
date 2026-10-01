# F-interior pack: `99-Unresolved-Residual/the-blinking-icon-and-its-atlas.md`

Generated 2026-10-01 15:28 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-blinking-icon-and-its-atlas.json`.

Functions: 23. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (inbox mentions: FABLE.md, SWE2-AUDIT-SPEC.md). OPUS read these before packing.

## 00250730 (130 B, extent 00250730-002507B2)

Page context: " record ([the millisecond page](../16-UI/Widget-Object-Model/starting-a-widget-animation-and-the-millisecond-that-becomes-frames.md), the writer table): the UI frame handlers '00250540', '002506D0', '00250730' and '002507C0' add '00184950()' to it once per presented frame, and that getter returns '[01F3DA18]', the DXGI present sync interval clamped to 1–3 ([game settings](../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-a"

```
00250730  mov      qword ptr [rsp + 8], rbx
00250735  push     rdi
00250736  sub      rsp, 0x20
0025073A  xor      edx, edx
0025073C  mov      eax, 2
00250741  div      dword ptr [rip + 0x1bad96d]  ; -> 01DFE0B4 [u32 0x00000001]
00250747  mov      edx, dword ptr [rip + 0x1e41fef]  ; -> 0209273C
0025074D  mov      ebx, ecx
0025074F  add      edx, -2
00250752  mov      edi, eax
00250754  test     edx, 0xfffffffd
0025075A  jne      0x250763  ; -> 00250763
0025075C  mov      ebx, 1
00250761  mov      edi, ebx
00250763  add      dword ptr [rip + 0x1e3ee07], eax  ; -> 0208F570
00250769  call     0x2481a0  ; -> 002481A0 fn
0025076E  mov      rcx, qword ptr [rip + 0x1e3e2b3]  ; -> 0208EA28
00250775  call     0x248030  ; -> 00248030 fn
0025077A  call     0x248190  ; -> 00248190 fn
0025077F  cmp      ebx, 1
00250782  jne      0x250789  ; -> 00250789
00250784  call     0x2481c0  ; -> 002481C0 fn
00250789  mov      rcx, qword ptr [rip + 0x1e3e298]  ; -> 0208EA28
00250790  call     0x244970  ; -> 00244970 fn
00250795  mov      rcx, qword ptr [rip + 0x1e3e2a4]  ; -> 0208EA40
0025079C  call     0x244970  ; -> 00244970 fn
002507A1  mov      ecx, edi
002507A3  mov      rbx, qword ptr [rsp + 0x30]
002507A8  add      rsp, 0x20
002507AC  pop      rdi
002507AD  jmp      0x367200  ; -> 00367200 fn
```

## 002DD810 (35 B, extent 002DD810-002DD833)

Page context: "e dwords are the face colours of 'fontcolor.bin'.** The array behind '0215E6C8' (count at '0215E6B8') is the 'fontcolor' blob '{u32 count, u64 pairs[count]}' that the kind-7 id-5 loader '0029CED0' → '002DD810' installs ([the loader-bound families](../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md), 'fontcolor'); each 'u64' is a colour pair, face and shadow, so '002DD7E0(id)' returns the face quad and "

```
002DD810  xor      eax, eax
002DD812  mov      qword ptr [rip + 0x1e80ea7], rax  ; -> 0215E6C0
002DD819  mov      qword ptr [rip + 0x1e80e98], rax  ; -> 0215E6B8
002DD820  mov      qword ptr [rip + 0x1e80ea1], rax  ; -> 0215E6C8
002DD827  mov      rax, qword ptr [rcx + 8]
002DD82B  mov      qword ptr [rip + 0x1e80e8e], rax  ; -> 0215E6C0
002DD832  ret      
```

## 002E9A30 (39 B, extent 002E9A30-002E9A57)

Page context: "he secondary context's record at '[[rcx+0xB8]]+0x224'. Interior anchor '0026A9A8' (the '+0x224' store).  ## SWE2-EC7-42 update (2026-09-19) - '0050F6E0'  '0050F6E0' (302 B) is a blinking-icon body - '002E9A30'/'0026A1A0'/'00267E10'/'00264010'/'00265020' pair/'003A19A0'/'00267F60'/'00267DB0'. Interior anchor '0050F6FC' (a '002E9A30' call).  ## SWE2-EC7-44 update (2026-09-19) - '002B9A20'  '002B9A20' (260 B) is a body - '002B8EE0' single "

```
002E9A30  cmp      byte ptr [rcx + 0x18], 1
002E9A34  jne      0x2e9a3c  ; -> 002E9A3C
002E9A36  mov      eax, 1
002E9A3B  ret      
002E9A3C  movzx    eax, byte ptr [rcx + 3]
002E9A40  and      al, 0xe0
002E9A42  cmp      al, 0x60
002E9A44  jne      0x2e9a36  ; -> 002E9A36
002E9A46  mov      rax, qword ptr [rcx + 0xc0]
002E9A4D  movzx    eax, byte ptr [rax + 0x11]
002E9A51  shr      eax, 1
002E9A53  and      eax, 1
002E9A56  ret      
```

## 0033F270 (127 B, extent 0033F270-0033F2EF)

Page context: "F0' and 30 more; 'VMValueStack_PushFloat32Bits' ('00267F60') is called by 'WorldActorScriptVM_InterpretBytecode' ('0025E4C0'), '00340480', '00340BE0', '00342040' and 30 more; '0026A1A0' is called by '0033F270', '0033F770', '0033FBA0', '00340480' and 25 more; 'Actor_GetWorldPosition' ('00265020') is called by '0033FD60', '00344AF0', '00345180', '00345830' and 19 more; '003A19A0' is called by '00345830', '003461B0', '0034BE50', '00357DE0'"

```
0033F270  mov      qword ptr [rsp + 8], rbx
0033F275  mov      qword ptr [rsp + 0x10], rbp
0033F27A  mov      qword ptr [rsp + 0x18], rsi
0033F27F  mov      qword ptr [rsp + 0x20], rdi
0033F284  push     r14
0033F286  sub      rsp, 0x20
0033F28A  mov      r14, rcx
0033F28D  mov      rdi, r9
0033F290  mov      rcx, r9
0033F293  mov      rsi, r8
0033F296  mov      rbp, rdx
0033F299  call     0x267e10  ; -> 00267E10 fn
0033F29E  mov      edx, 0x30b
0033F2A3  mov      rcx, rdi
0033F2A6  mov      ebx, eax
0033F2A8  call     0x267f90  ; -> 00267F90 fn
0033F2AD  mov      edx, ebx
0033F2AF  mov      rcx, rdi
0033F2B2  call     0x267f90  ; -> 00267F90 fn
0033F2B7  mov      edx, 1
0033F2BC  mov      rcx, rbp
0033F2BF  call     0x26a1a0  ; -> 0026A1A0 fn
0033F2C4  mov      r9, rdi
0033F2C7  mov      r8, rsi
0033F2CA  mov      rdx, rbp
0033F2CD  mov      rcx, r14
0033F2D0  mov      rbx, qword ptr [rsp + 0x30]
0033F2D5  mov      rbp, qword ptr [rsp + 0x38]
0033F2DA  mov      rsi, qword ptr [rsp + 0x40]
0033F2DF  mov      rdi, qword ptr [rsp + 0x48]
0033F2E4  add      rsp, 0x20
0033F2E8  pop      r14
0033F2EA  jmp      0x357b10  ; -> 00357B10 fn
```

## 0033F770 (124 B, extent 0033F770-0033F7EC)

Page context: "ore; 'VMValueStack_PushFloat32Bits' ('00267F60') is called by 'WorldActorScriptVM_InterpretBytecode' ('0025E4C0'), '00340480', '00340BE0', '00342040' and 30 more; '0026A1A0' is called by '0033F270', '0033F770', '0033FBA0', '00340480' and 25 more; 'Actor_GetWorldPosition' ('00265020') is called by '0033FD60', '00344AF0', '00345180', '00345830' and 19 more; '003A19A0' is called by '00345830', '003461B0', '0034BE50', '00357DE0' and 1 more;"

```
0033F770  mov      qword ptr [rsp + 8], rbx
0033F775  mov      qword ptr [rsp + 0x10], rbp
0033F77A  mov      qword ptr [rsp + 0x18], rsi
0033F77F  mov      qword ptr [rsp + 0x20], rdi
0033F784  push     r14
0033F786  sub      rsp, 0x20
0033F78A  mov      r14, rcx
0033F78D  mov      rdi, r9
0033F790  mov      rcx, r9
0033F793  mov      rsi, r8
0033F796  mov      rbp, rdx
0033F799  call     0x267e10  ; -> 00267E10 fn
0033F79E  mov      edx, 0x30b
0033F7A3  mov      rcx, rdi
0033F7A6  mov      ebx, eax
0033F7A8  call     0x267f90  ; -> 00267F90 fn
0033F7AD  mov      edx, ebx
0033F7AF  mov      rcx, rdi
0033F7B2  call     0x267f90  ; -> 00267F90 fn
0033F7B7  xor      edx, edx
0033F7B9  mov      rcx, rbp
0033F7BC  call     0x26a1a0  ; -> 0026A1A0 fn
0033F7C1  mov      r9, rdi
0033F7C4  mov      r8, rsi
0033F7C7  mov      rdx, rbp
0033F7CA  mov      rcx, r14
0033F7CD  mov      rbx, qword ptr [rsp + 0x30]
0033F7D2  mov      rbp, qword ptr [rsp + 0x38]
0033F7D7  mov      rsi, qword ptr [rsp + 0x40]
0033F7DC  mov      rdi, qword ptr [rsp + 0x48]
0033F7E1  add      rsp, 0x20
0033F7E5  pop      r14
0033F7E7  jmp      0x357ba0  ; -> 00357BA0 fn
```

## 0033FBA0 (127 B, extent 0033FBA0-0033FC1F)

Page context: "eStack_PushFloat32Bits' ('00267F60') is called by 'WorldActorScriptVM_InterpretBytecode' ('0025E4C0'), '00340480', '00340BE0', '00342040' and 30 more; '0026A1A0' is called by '0033F270', '0033F770', '0033FBA0', '00340480' and 25 more; 'Actor_GetWorldPosition' ('00265020') is called by '0033FD60', '00344AF0', '00345180', '00345830' and 19 more; '003A19A0' is called by '00345830', '003461B0', '0034BE50', '00357DE0' and 1 more; '003A1D30' "

```
0033FBA0  mov      qword ptr [rsp + 8], rbx
0033FBA5  mov      qword ptr [rsp + 0x10], rbp
0033FBAA  mov      qword ptr [rsp + 0x18], rsi
0033FBAF  mov      qword ptr [rsp + 0x20], rdi
0033FBB4  push     r14
0033FBB6  sub      rsp, 0x20
0033FBBA  mov      r14, rcx
0033FBBD  mov      rdi, r9
0033FBC0  mov      rcx, r9
0033FBC3  mov      rsi, r8
0033FBC6  mov      rbp, rdx
0033FBC9  call     0x267e10  ; -> 00267E10 fn
0033FBCE  mov      edx, 0x30b
0033FBD3  mov      rcx, rdi
0033FBD6  mov      ebx, eax
0033FBD8  call     0x267f90  ; -> 00267F90 fn
0033FBDD  mov      edx, ebx
0033FBDF  mov      rcx, rdi
0033FBE2  call     0x267f90  ; -> 00267F90 fn
0033FBE7  mov      edx, 1
0033FBEC  mov      rcx, rbp
0033FBEF  call     0x26a1a0  ; -> 0026A1A0 fn
0033FBF4  mov      r9, rdi
0033FBF7  mov      r8, rsi
0033FBFA  mov      rdx, rbp
0033FBFD  mov      rcx, r14
0033FC00  mov      rbx, qword ptr [rsp + 0x30]
0033FC05  mov      rbp, qword ptr [rsp + 0x38]
0033FC0A  mov      rsi, qword ptr [rsp + 0x40]
0033FC0F  mov      rdi, qword ptr [rsp + 0x48]
0033FC14  add      rsp, 0x20
0033FC18  pop      r14
0033FC1A  jmp      0x357ba0  ; -> 00357BA0 fn
```

## 00340480 (108 B, extent 00340480-003404EC)

Page context: "ore; '00264010' is called by '00341410', '00343D10', '00344390', '003448F0' and 30 more; 'VMValueStack_PushFloat32Bits' ('00267F60') is called by 'WorldActorScriptVM_InterpretBytecode' ('0025E4C0'), '00340480', '00340BE0', '00342040' and 30 more; '0026A1A0' is called by '0033F270', '0033F770', '0033FBA0', '00340480' and 25 more; 'Actor_GetWorldPosition' ('00265020') is called by '0033FD60', '00344AF0', '00345180', '00345830' and 19 more"

```
00340480  mov      qword ptr [rsp + 8], rbx
00340485  mov      qword ptr [rsp + 0x10], rbp
0034048A  mov      qword ptr [rsp + 0x18], rsi
0034048F  push     rdi
00340490  sub      rsp, 0x20
00340494  mov      rbp, rcx
00340497  mov      rbx, r9
0034049A  mov      rcx, rdx
0034049D  mov      rdi, r8
003404A0  mov      rsi, rdx
003404A3  call     0x2644e0  ; -> 002644E0 fn
003404A8  movaps   xmm1, xmm0
003404AB  mov      rcx, rbx
003404AE  call     0x267f60  ; -> 00267F60 fn
003404B3  xor      edx, edx
003404B5  mov      rcx, rsi
003404B8  call     0x26a1a0  ; -> 0026A1A0 fn
003404BD  xor      edx, edx
003404BF  mov      rcx, rsi
003404C2  call     0x26a1a0  ; -> 0026A1A0 fn
003404C7  mov      r9, rbx
003404CA  mov      r8, rdi
003404CD  mov      rdx, rsi
003404D0  mov      rcx, rbp
003404D3  mov      rbx, qword ptr [rsp + 0x30]
003404D8  mov      rbp, qword ptr [rsp + 0x38]
003404DD  mov      rsi, qword ptr [rsp + 0x40]
003404E2  add      rsp, 0x20
003404E6  pop      rdi
003404E7  jmp      0x357d10  ; -> 00357D10 fn
```

## 00340BE0 (111 B, extent 00340BE0-00340C4F)

Page context: "10' is called by '00341410', '00343D10', '00344390', '003448F0' and 30 more; 'VMValueStack_PushFloat32Bits' ('00267F60') is called by 'WorldActorScriptVM_InterpretBytecode' ('0025E4C0'), '00340480', '00340BE0', '00342040' and 30 more; '0026A1A0' is called by '0033F270', '0033F770', '0033FBA0', '00340480' and 25 more; 'Actor_GetWorldPosition' ('00265020') is called by '0033FD60', '00344AF0', '00345180', '00345830' and 19 more; '003A19A0'"

```
00340BE0  mov      qword ptr [rsp + 8], rbx
00340BE5  mov      qword ptr [rsp + 0x10], rbp
00340BEA  mov      qword ptr [rsp + 0x18], rsi
00340BEF  push     rdi
00340BF0  sub      rsp, 0x20
00340BF4  mov      rbp, rcx
00340BF7  mov      rbx, r9
00340BFA  mov      rcx, rdx
00340BFD  mov      rdi, r8
00340C00  mov      rsi, rdx
00340C03  call     0x2644e0  ; -> 002644E0 fn
00340C08  movaps   xmm1, xmm0
00340C0B  mov      rcx, rbx
00340C0E  call     0x267f60  ; -> 00267F60 fn
00340C13  mov      edx, 1
00340C18  mov      rcx, rsi
00340C1B  call     0x26a1a0  ; -> 0026A1A0 fn
00340C20  xor      edx, edx
00340C22  mov      rcx, rsi
00340C25  call     0x26a1a0  ; -> 0026A1A0 fn
00340C2A  mov      r9, rbx
00340C2D  mov      r8, rdi
00340C30  mov      rdx, rsi
00340C33  mov      rcx, rbp
00340C36  mov      rbx, qword ptr [rsp + 0x30]
00340C3B  mov      rbp, qword ptr [rsp + 0x38]
00340C40  mov      rsi, qword ptr [rsp + 0x40]
00340C45  add      rsp, 0x20
00340C49  pop      rdi
00340C4A  jmp      0x357d10  ; -> 00357D10 fn
```

## 00341410 (79 B, extent 00341410-0034145F)

Page context: "0358CB0').  **Script_VM_Native_Bridge — MECHANICAL, 199 edges.** 'VMResult_WriteFloat32' ('0026B4C0') is called by '00340B50', '00340E90', '00340F80', '00341250' and 48 more; '00264010' is called by '00341410', '00343D10', '00344390', '003448F0' and 30 more; 'VMValueStack_PushFloat32Bits' ('00267F60') is called by 'WorldActorScriptVM_InterpretBytecode' ('0025E4C0'), '00340480', '00340BE0', '00342040' and 30 more; '0026A1A0' is called by"

```
00341410  mov      qword ptr [rsp + 8], rbx
00341415  push     rdi
00341416  sub      rsp, 0x20
0034141A  mov      rcx, r9
0034141D  mov      rdi, r9
00341420  call     0x267e10  ; -> 00267E10 fn
00341425  mov      rcx, rdi
00341428  mov      ebx, eax
0034142A  call     0x267e10  ; -> 00267E10 fn
0034142F  test     ebx, ebx
00341431  je       0x34144c  ; -> 0034144C
00341433  mov      ecx, eax
00341435  call     0x264010  ; -> 00264010 fn
0034143A  mov      rcx, rax
0034143D  mov      rbx, qword ptr [rsp + 0x30]
00341442  add      rsp, 0x20
00341446  pop      rdi
00341447  jmp      0x2eda90  ; -> 002EDA90 fn
0034144C  xor      eax, eax
0034144E  mov      ecx, eax
00341450  mov      rbx, qword ptr [rsp + 0x30]
00341455  add      rsp, 0x20
00341459  pop      rdi
0034145A  jmp      0x2eda90  ; -> 002EDA90 fn
```

## 00343D10 (124 B, extent 00343D10-00343D8C)

Page context: "**Script_VM_Native_Bridge — MECHANICAL, 199 edges.** 'VMResult_WriteFloat32' ('0026B4C0') is called by '00340B50', '00340E90', '00340F80', '00341250' and 48 more; '00264010' is called by '00341410', '00343D10', '00344390', '003448F0' and 30 more; 'VMValueStack_PushFloat32Bits' ('00267F60') is called by 'WorldActorScriptVM_InterpretBytecode' ('0025E4C0'), '00340480', '00340BE0', '00342040' and 30 more; '0026A1A0' is called by '0033F270',"

```
00343D10  mov      qword ptr [rsp + 8], rbx
00343D15  mov      qword ptr [rsp + 0x10], rbp
00343D1A  mov      qword ptr [rsp + 0x18], rsi
00343D1F  push     rdi
00343D20  sub      rsp, 0x20
00343D24  mov      rbp, rcx
00343D27  mov      rdi, r9
00343D2A  mov      rcx, r9
00343D2D  call     0x267e10  ; -> 00267E10 fn
00343D32  mov      rcx, rdi
00343D35  mov      ebx, eax
00343D37  call     0x267e10  ; -> 00267E10 fn
00343D3C  mov      ecx, ebx
00343D3E  mov      edi, eax
00343D40  call     0x264010  ; -> 00264010 fn
00343D45  mov      ecx, edi
00343D47  mov      rsi, rax
00343D4A  call     0x264010  ; -> 00264010 fn
00343D4F  mov      rcx, rax
00343D52  call     0x265060  ; -> 00265060 fn
00343D57  mov      rcx, rsi
00343D5A  mov      rbx, rax
00343D5D  call     0x265060  ; -> 00265060 fn
00343D62  mov      rcx, rax
00343D65  mov      rdx, rbx
00343D68  call     0x3a1920  ; -> 003A1920 fn
00343D6D  movaps   xmm1, xmm0
00343D70  mov      rcx, rbp
00343D73  mov      rbx, qword ptr [rsp + 0x30]
00343D78  mov      rbp, qword ptr [rsp + 0x38]
00343D7D  mov      rsi, qword ptr [rsp + 0x40]
00343D82  add      rsp, 0x20
00343D86  pop      rdi
00343D87  jmp      0x26b4c0  ; -> 0026B4C0 fn
```

## 00344390 (124 B, extent 00344390-0034440C)

Page context: "Native_Bridge — MECHANICAL, 199 edges.** 'VMResult_WriteFloat32' ('0026B4C0') is called by '00340B50', '00340E90', '00340F80', '00341250' and 48 more; '00264010' is called by '00341410', '00343D10', '00344390', '003448F0' and 30 more; 'VMValueStack_PushFloat32Bits' ('00267F60') is called by 'WorldActorScriptVM_InterpretBytecode' ('0025E4C0'), '00340480', '00340BE0', '00342040' and 30 more; '0026A1A0' is called by '0033F270', '0033F770',"

```
00344390  mov      qword ptr [rsp + 8], rbx
00344395  mov      qword ptr [rsp + 0x10], rbp
0034439A  mov      qword ptr [rsp + 0x18], rsi
0034439F  push     rdi
003443A0  sub      rsp, 0x20
003443A4  mov      rbp, rcx
003443A7  mov      rdi, r9
003443AA  mov      rcx, r9
003443AD  call     0x267e10  ; -> 00267E10 fn
003443B2  mov      rcx, rdi
003443B5  mov      ebx, eax
003443B7  call     0x267e10  ; -> 00267E10 fn
003443BC  mov      ecx, ebx
003443BE  mov      edi, eax
003443C0  call     0x264010  ; -> 00264010 fn
003443C5  mov      ecx, edi
003443C7  mov      rsi, rax
003443CA  call     0x264010  ; -> 00264010 fn
003443CF  mov      rcx, rax
003443D2  call     0x265060  ; -> 00265060 fn
003443D7  mov      rcx, rsi
003443DA  mov      rbx, rax
003443DD  call     0x265060  ; -> 00265060 fn
003443E2  mov      rcx, rax
003443E5  mov      rdx, rbx
003443E8  call     0x4686d0  ; -> 004686D0 fn
003443ED  movaps   xmm1, xmm0
003443F0  mov      rcx, rbp
003443F3  mov      rbx, qword ptr [rsp + 0x30]
003443F8  mov      rbp, qword ptr [rsp + 0x38]
003443FD  mov      rsi, qword ptr [rsp + 0x40]
00344402  add      rsp, 0x20
00344406  pop      rdi
00344407  jmp      0x26b4c0  ; -> 0026B4C0 fn
```

## 00345180 (208 B, extent 00345180-00345250)

Page context: "0', '00340BE0', '00342040' and 30 more; '0026A1A0' is called by '0033F270', '0033F770', '0033FBA0', '00340480' and 25 more; 'Actor_GetWorldPosition' ('00265020') is called by '0033FD60', '00344AF0', '00345180', '00345830' and 19 more; '003A19A0' is called by '00345830', '003461B0', '0034BE50', '00357DE0' and 1 more; '003A1D30' is called by '00344AF0', '00345180', '00352F70'; '0050F6E0' calls 'VMValueStack_PopNumericDiscard' ('00267DB0')"

```
00345180  mov      qword ptr [rsp + 8], rbx
00345185  mov      qword ptr [rsp + 0x10], rsi
0034518A  push     rdi
0034518B  sub      rsp, 0x60
0034518F  movaps   xmmword ptr [rsp + 0x50], xmm6
00345194  mov      rsi, rcx
00345197  movaps   xmmword ptr [rsp + 0x40], xmm7
0034519C  mov      rcx, r9
0034519F  movaps   xmmword ptr [rsp + 0x30], xmm8
003451A5  mov      rbx, r9
003451A8  mov      rdi, rdx
003451AB  call     0x267db0  ; -> 00267DB0 fn
003451B0  mov      rcx, rbx
003451B3  movaps   xmm8, xmm0
003451B7  call     0x267db0  ; -> 00267DB0 fn
003451BC  mov      rcx, rbx
003451BF  movaps   xmm6, xmm0
003451C2  call     0x267db0  ; -> 00267DB0 fn
003451C7  lea      r9, [rsp + 0x24]
003451CC  mov      rcx, rdi
003451CF  lea      r8, [rsp + 0x28]
003451D4  movaps   xmm7, xmm0
003451D7  lea      rdx, [rsp + 0x20]
003451DC  call     0x265020  ; -> 00265020 fn
003451E1  subss    xmm7, dword ptr [rsp + 0x20]
003451E7  subss    xmm6, dword ptr [rsp + 0x28]
003451ED  subss    xmm8, dword ptr [rsp + 0x24]
003451F4  movss    dword ptr [rsp + 0x20], xmm7
003451FA  mulss    xmm7, xmm7
003451FE  movss    dword ptr [rsp + 0x28], xmm6
00345204  movss    dword ptr [rsp + 0x24], xmm8
0034520B  mulss    xmm6, xmm6
0034520F  mulss    xmm8, xmm8
00345214  addss    xmm7, xmm6
00345218  addss    xmm7, xmm8
0034521D  movaps   xmm0, xmm7
00345220  call     0x3a1d30  ; -> 003A1D30 fn
00345225  movaps   xmm1, xmm0
00345228  mov      rcx, rsi
0034522B  call     0x26b4c0  ; -> 0026B4C0 fn
00345230  mov      rbx, qword ptr [rsp + 0x70]
00345235  mov      rsi, qword ptr [rsp + 0x78]
0034523A  movaps   xmm6, xmmword ptr [rsp + 0x50]
0034523F  movaps   xmm7, xmmword ptr [rsp + 0x40]
00345244  movaps   xmm8, xmmword ptr [rsp + 0x30]
0034524A  add      rsp, 0x60
0034524E  pop      rdi
0034524F  ret      
```

## 00345430 (233 B, extent 00345430-00345519)

Page context: "180' calls '00265200', 'Actor_SetDesiredMovementHeading' ('0026A0D0'), '0026B0C0', 'Actor_SetFacingHeading_Variant1' ('0026B620') and 1 more; 'VMValueStack_PushFloat32Bits' ('00267F60') is called by '00345430', '003488B0', '00349680', '003548B0'; '0026A870' is called by '002EBFA0', '002EC140', '002EC1C0', '002EC2C0'; '003A1D30' is called by 'Movement_ComputeDeltaFromHeadingSpeed' ('002E4380'), 'Movement_UpdateSteeringTowardTarget' ('002"

```
00345430  mov      qword ptr [rsp + 0x18], rbp
00345435  push     rsi
00345436  push     r14
00345438  push     r15
0034543A  sub      rsp, 0x20
0034543E  mov      rsi, r9
00345441  mov      r14, r8
00345444  mov      r15, rcx
00345447  call     0x3590d0  ; -> 003590D0 fn
0034544C  mov      ecx, eax
0034544E  call     0x3588b0  ; -> 003588B0 fn
00345453  mov      rbp, rax
00345456  test     rax, rax
00345459  je       0x3454f3  ; -> 003454F3
0034545F  mov      qword ptr [rsp + 0x40], rbx
00345464  mov      rcx, rax
00345467  mov      qword ptr [rsp + 0x48], rdi
0034546C  call     0x264420  ; -> 00264420 fn
00345471  mov      rcx, rbp
00345474  mov      ebx, eax
00345476  call     0x30beb0  ; -> 0030BEB0 fn
0034547B  mov      edi, eax
0034547D  call     0x3590b0  ; -> 003590B0 fn
00345482  movaps   xmm1, xmm0
00345485  mov      rcx, rsi
00345488  call     0x267f60  ; -> 00267F60 fn
0034548D  mov      r8d, 2
00345493  mov      edx, ebx
00345495  mov      rcx, rbp
00345498  call     0x2ecf10  ; -> 002ECF10 fn
0034549D  mov      r9, rsi
003454A0  mov      r8, r14
003454A3  mov      rdx, rbp
003454A6  mov      rcx, r15
003454A9  call     0x357a20  ; -> 00357A20 fn
003454AE  mov      rcx, rbp
003454B1  call     0x263f40  ; -> 00263F40 fn
003454B6  mov      rcx, rax
003454B9  call     0x2eb430  ; -> 002EB430 fn
003454BE  mov      edx, 2
003454C3  mov      rcx, rbp
003454C6  call     0x26c120  ; -> 0026C120 fn
003454CB  mov      r8d, edi
003454CE  mov      edx, 1
003454D3  mov      rcx, rbp
003454D6  mov      rdi, qword ptr [rsp + 0x48]
003454DB  mov      rbx, qword ptr [rsp + 0x40]
003454E0  mov      rbp, qword ptr [rsp + 0x50]
003454E5  add      rsp, 0x20
003454E9  pop      r15
003454EB  pop      r14
003454ED  pop      rsi
003454EE  jmp      0x269d80  ; -> 00269D80 fn
003454F3  mov      rcx, rsi
003454F6  call     0x267db0  ; -> 00267DB0 fn
003454FB  mov      rcx, rsi
003454FE  call     0x267db0  ; -> 00267DB0 fn
00345503  mov      rcx, rsi
00345506  mov      rbp, qword ptr [rsp + 0x50]
0034550B  add      rsp, 0x20
0034550F  pop      r15
00345511  pop      r14
00345513  pop      rsi
00345514  jmp      0x267db0  ; -> 00267DB0 fn
```

## 00345830 (158 B, extent 00345830-003458CE)

Page context: "0', '00342040' and 30 more; '0026A1A0' is called by '0033F270', '0033F770', '0033FBA0', '00340480' and 25 more; 'Actor_GetWorldPosition' ('00265020') is called by '0033FD60', '00344AF0', '00345180', '00345830' and 19 more; '003A19A0' is called by '00345830', '003461B0', '0034BE50', '00357DE0' and 1 more; '003A1D30' is called by '00344AF0', '00345180', '00352F70'; '0050F6E0' calls 'VMValueStack_PopNumericDiscard' ('00267DB0'), 'VMValueSt"

```
00345830  mov      qword ptr [rsp + 8], rbx
00345835  mov      qword ptr [rsp + 0x10], rsi
0034583A  push     rdi
0034583B  sub      rsp, 0x50
0034583F  mov      rsi, rcx
00345842  movaps   xmmword ptr [rsp + 0x40], xmm6
00345847  mov      rcx, r9
0034584A  movaps   xmmword ptr [rsp + 0x30], xmm7
0034584F  mov      rbx, r9
00345852  mov      rdi, rdx
00345855  call     0x267db0  ; -> 00267DB0 fn
0034585A  mov      rcx, rbx
0034585D  movaps   xmm6, xmm0
00345860  call     0x267db0  ; -> 00267DB0 fn
00345865  lea      r9, [rsp + 0x20]
0034586A  mov      rcx, rdi
0034586D  lea      r8, [rsp + 0x28]
00345872  movaps   xmm7, xmm0
00345875  lea      rdx, [rsp + 0x24]
0034587A  call     0x265020  ; -> 00265020 fn
0034587F  movss    xmm1, dword ptr [rsp + 0x24]
00345885  ucomiss  xmm7, xmm1
00345888  movss    xmm0, dword ptr [rsp + 0x20]
0034588E  jp       0x34589e  ; -> 0034589E
00345890  jne      0x34589e  ; -> 0034589E
00345892  ucomiss  xmm6, xmm0
00345895  jp       0x34589e  ; -> 0034589E
00345897  jne      0x34589e  ; -> 0034589E
00345899  xorps    xmm0, xmm0
0034589C  jmp      0x3458a9  ; -> 003458A9
0034589E  movaps   xmm3, xmm7
003458A1  movaps   xmm2, xmm6
003458A4  call     0x3a19a0  ; -> 003A19A0 fn
003458A9  movaps   xmm1, xmm0
003458AC  mov      rcx, rsi
003458AF  call     0x26b4c0  ; -> 0026B4C0 fn
003458B4  mov      rbx, qword ptr [rsp + 0x60]
003458B9  mov      rsi, qword ptr [rsp + 0x68]
003458BE  movaps   xmm6, xmmword ptr [rsp + 0x40]
003458C3  movaps   xmm7, xmmword ptr [rsp + 0x30]
003458C8  add      rsp, 0x50
003458CC  pop      rdi
003458CD  ret      
```

## 003461B0 (141 B, extent 003461B0-0034623D)

Page context: "0', '0033F770', '0033FBA0', '00340480' and 25 more; 'Actor_GetWorldPosition' ('00265020') is called by '0033FD60', '00344AF0', '00345180', '00345830' and 19 more; '003A19A0' is called by '00345830', '003461B0', '0034BE50', '00357DE0' and 1 more; '003A1D30' is called by '00344AF0', '00345180', '00352F70'; '0050F6E0' calls 'VMValueStack_PopNumericDiscard' ('00267DB0'), 'VMValueStack_PopInt32CoerceFloat32' ('00267E10'), 'VMValueStack_PushF"

```
003461B0  mov      qword ptr [rsp + 8], rbx
003461B5  mov      qword ptr [rsp + 0x10], rsi
003461BA  push     rdi
003461BB  sub      rsp, 0x40
003461BF  mov      rsi, rcx
003461C2  mov      rdi, rdx
003461C5  mov      rcx, r9
003461C8  call     0x267e10  ; -> 00267E10 fn
003461CD  mov      ecx, eax
003461CF  call     0x264010  ; -> 00264010 fn
003461D4  lea      r9, [rsp + 0x2c]
003461D9  mov      rcx, rdi
003461DC  lea      r8, [rsp + 0x30]
003461E1  mov      rbx, rax
003461E4  lea      rdx, [rsp + 0x28]
003461E9  call     0x265020  ; -> 00265020 fn
003461EE  lea      r9, [rsp + 0x24]
003461F3  mov      rcx, rbx
003461F6  lea      r8, [rsp + 0x34]
003461FB  lea      rdx, [rsp + 0x20]
00346200  call     0x265020  ; -> 00265020 fn
00346205  movss    xmm3, dword ptr [rsp + 0x20]
0034620B  movss    xmm2, dword ptr [rsp + 0x24]
00346211  movss    xmm1, dword ptr [rsp + 0x28]
00346217  movss    xmm0, dword ptr [rsp + 0x2c]
0034621D  call     0x3a19a0  ; -> 003A19A0 fn
00346222  movaps   xmm1, xmm0
00346225  mov      rcx, rsi
00346228  call     0x26b4c0  ; -> 0026B4C0 fn
0034622D  mov      rbx, qword ptr [rsp + 0x50]
00346232  mov      rsi, qword ptr [rsp + 0x58]
00346237  add      rsp, 0x40
0034623B  pop      rdi
0034623C  ret      
```

## 003488B0 (101 B, extent 003488B0-00348915)

Page context: "00265200', 'Actor_SetDesiredMovementHeading' ('0026A0D0'), '0026B0C0', 'Actor_SetFacingHeading_Variant1' ('0026B620') and 1 more; 'VMValueStack_PushFloat32Bits' ('00267F60') is called by '00345430', '003488B0', '00349680', '003548B0'; '0026A870' is called by '002EBFA0', '002EC140', '002EC1C0', '002EC2C0'; '003A1D30' is called by 'Movement_ComputeDeltaFromHeadingSpeed' ('002E4380'), 'Movement_UpdateSteeringTowardTarget' ('002E45E0'), 'Mo"

```
003488B0  mov      qword ptr [rsp + 8], rbx
003488B5  mov      qword ptr [rsp + 0x10], rbp
003488BA  mov      qword ptr [rsp + 0x18], rsi
003488BF  push     rdi
003488C0  sub      rsp, 0x20
003488C4  mov      rsi, rcx
003488C7  mov      rbx, r9
003488CA  mov      rcx, rdx
003488CD  mov      rdi, r8
003488D0  mov      rbp, rdx
003488D3  call     0x2640e0  ; -> 002640E0 fn
003488D8  movaps   xmm1, xmm0
003488DB  mov      rcx, rbx
003488DE  call     0x267f60  ; -> 00267F60 fn
003488E3  mov      r9, rbx
003488E6  mov      r8, rdi
003488E9  mov      rdx, rbp
003488EC  mov      rcx, rsi
003488EF  call     0x357a20  ; -> 00357A20 fn
003488F4  mov      edx, 2
003488F9  mov      rcx, rbp
003488FC  mov      rbx, qword ptr [rsp + 0x30]
00348901  mov      rbp, qword ptr [rsp + 0x38]
00348906  mov      rsi, qword ptr [rsp + 0x40]
0034890B  add      rsp, 0x20
0034890F  pop      rdi
00348910  jmp      0x26c120  ; -> 0026C120 fn
```

## 00349680 (117 B, extent 00349680-003496F5)

Page context: "Actor_SetDesiredMovementHeading' ('0026A0D0'), '0026B0C0', 'Actor_SetFacingHeading_Variant1' ('0026B620') and 1 more; 'VMValueStack_PushFloat32Bits' ('00267F60') is called by '00345430', '003488B0', '00349680', '003548B0'; '0026A870' is called by '002EBFA0', '002EC140', '002EC1C0', '002EC2C0'; '003A1D30' is called by 'Movement_ComputeDeltaFromHeadingSpeed' ('002E4380'), 'Movement_UpdateSteeringTowardTarget' ('002E45E0'), 'Movement_Prepa"

```
00349680  mov      qword ptr [rsp + 8], rbx
00349685  mov      qword ptr [rsp + 0x10], rbp
0034968A  mov      qword ptr [rsp + 0x18], rsi
0034968F  push     rdi
00349690  sub      rsp, 0x20
00349694  mov      rsi, rcx
00349697  mov      rbx, r9
0034969A  mov      rcx, rdx
0034969D  mov      rdi, r8
003496A0  mov      rbp, rdx
003496A3  call     0x2640e0  ; -> 002640E0 fn
003496A8  movaps   xmm1, xmm0
003496AB  mov      rcx, rbx
003496AE  call     0x267f60  ; -> 00267F60 fn
003496B3  mov      r9, rbx
003496B6  mov      r8, rdi
003496B9  mov      rdx, rbp
003496BC  mov      rcx, rsi
003496BF  call     0x357a20  ; -> 00357A20 fn
003496C4  mov      rcx, rbp
003496C7  call     0x263f40  ; -> 00263F40 fn
003496CC  mov      rcx, rax
003496CF  call     0x2eb430  ; -> 002EB430 fn
003496D4  mov      edx, 2
003496D9  mov      rcx, rbp
003496DC  mov      rbx, qword ptr [rsp + 0x30]
003496E1  mov      rbp, qword ptr [rsp + 0x38]
003496E6  mov      rsi, qword ptr [rsp + 0x40]
003496EB  add      rsp, 0x20
003496EF  pop      rdi
003496F0  jmp      0x26c120  ; -> 0026C120 fn
```

## 00353530 (86 B, extent 00353530-00353586)

Page context: "Focus_IsCurrentPackedActorHandle' ('003273B0'); '00264010' calls 'PartyFocus_GetCurrentPackedActorHandle' ('003590D0'); '00264010' is called by 'VMPartyCommand_SetSecondaryFocusActorFromActorIndex' ('00353530'); 'ActorRuntime_GetClass3FloatPair' ('00265090') is called by '00303CC0'; '00303CC0' calls 'PartyRoster_GetActorBySlot' ('0031ABF0'); 'RNG_SharedGameplayLCG_NextU32' ('00328370') is called by 'BattleUnit_SeedPartyCombatStanceReche"

```
00353530  mov      qword ptr [rsp + 8], rbx
00353535  push     rdi
00353536  sub      rsp, 0x20
0035353A  mov      rcx, r9
0035353D  mov      rbx, r9
00353540  call     0x267e10  ; -> 00267E10 fn
00353545  mov      rcx, rbx
00353548  mov      edi, eax
0035354A  call     0x267e10  ; -> 00267E10 fn
0035354F  test     eax, eax
00353551  je       0x353573  ; -> 00353573
00353553  mov      ecx, edi
00353555  call     0x264010  ; -> 00264010 fn
0035355A  mov      rcx, rax
0035355D  call     0x3589b0  ; -> 003589B0 fn
00353562  mov      ecx, eax
00353564  mov      rbx, qword ptr [rsp + 0x30]
00353569  add      rsp, 0x20
0035356D  pop      rdi
0035356E  jmp      0x359410  ; -> 00359410 fn
00353573  xor      eax, eax
00353575  mov      ecx, eax
00353577  mov      rbx, qword ptr [rsp + 0x30]
0035357C  add      rsp, 0x20
00353580  pop      rdi
00353581  jmp      0x359410  ; -> 00359410 fn
```

## 00357C40 (193 B, extent 00357C40-00357D01)

Page context: "MValueStack_PopInt32CoerceFloat32' ('00267E10'), 'VMValueStack_PushFloat32Bits' ('00267F60'); 'MapRef_GetPersistenceGroupId' ('00264F90') is called by '00357450', '0050CDE0'; '002EC2C0' is called by '00357C40', '00357D10'; 'PersistentFlag_SetBank512Low' ('0032AD70') is called by '00353750', '00353BD0'; '00344AF0' calls 'VMValueStack_PopNumericDiscard' ('00267DB0'), 'VMResult_WriteFloat32' ('0026B4C0'); 'RNG_MT19937_NextU32_Thunk' ('0037"

```
00357C40  mov      qword ptr [rsp + 8], rbx
00357C45  push     rdi
00357C46  sub      rsp, 0x50
00357C4A  movaps   xmmword ptr [rsp + 0x40], xmm6
00357C4F  mov      rax, qword ptr [rip + 0x1becbda]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00357C56  xor      rax, rsp
00357C59  mov      qword ptr [rsp + 0x30], rax
00357C5E  movss    xmm0, dword ptr [rip + 0x1993f42]  ; -> 01CEBBA8 [f32 1]
00357C66  mov      rcx, r9
00357C69  movss    dword ptr [rsp + 0x2c], xmm0
00357C6F  mov      rbx, r9
00357C72  mov      rdi, rdx
00357C75  call     0x267db0  ; -> 00267DB0 fn
00357C7A  mov      rcx, rbx
00357C7D  movaps   xmm6, xmm0
00357C80  call     0x267db0  ; -> 00267DB0 fn
00357C85  mov      rcx, rdi
00357C88  movss    dword ptr [rsp + 0x28], xmm0
00357C8E  call     0x263d00  ; -> 00263D00 fn
00357C93  test     eax, eax
00357C95  jne      0x357ca1  ; -> 00357CA1
00357C97  mov      rcx, rbx
00357C9A  call     0x267db0  ; -> 00267DB0 fn
00357C9F  jmp      0x357ca4  ; -> 00357CA4
00357CA1  xorps    xmm0, xmm0
00357CA4  mov      rcx, rbx
00357CA7  movss    dword ptr [rsp + 0x24], xmm0
00357CAD  call     0x267db0  ; -> 00267DB0 fn
00357CB2  lea      rdx, [rsp + 0x20]
00357CB7  movss    dword ptr [rsp + 0x20], xmm0
00357CBD  mov      rcx, rdi
00357CC0  call     0x2ec2c0  ; -> 002EC2C0 fn
00357CC5  movaps   xmm2, xmm6
00357CC8  mov      edx, 2
00357CCD  mov      rcx, rdi
00357CD0  call     0x2ec380  ; -> 002EC380 fn
00357CD5  xor      r8d, r8d
00357CD8  mov      rcx, rdi
00357CDB  lea      edx, [r8 + 1]
00357CDF  call     0x2ebe50  ; -> 002EBE50 fn
00357CE4  mov      rcx, qword ptr [rsp + 0x30]
00357CE9  xor      rcx, rsp
00357CEC  call     0x808c40  ; -> 00808C40 fn
00357CF1  mov      rbx, qword ptr [rsp + 0x60]
00357CF6  movaps   xmm6, xmmword ptr [rsp + 0x40]
00357CFB  add      rsp, 0x50
00357CFF  pop      rdi
00357D00  ret      
```

## 00357D10 (206 B, extent 00357D10-00357DDE)

Page context: "PopInt32CoerceFloat32' ('00267E10'), 'VMValueStack_PushFloat32Bits' ('00267F60'); 'MapRef_GetPersistenceGroupId' ('00264F90') is called by '00357450', '0050CDE0'; '002EC2C0' is called by '00357C40', '00357D10'; 'PersistentFlag_SetBank512Low' ('0032AD70') is called by '00353750', '00353BD0'; '00344AF0' calls 'VMValueStack_PopNumericDiscard' ('00267DB0'), 'VMResult_WriteFloat32' ('0026B4C0'); 'RNG_MT19937_NextU32_Thunk' ('00379CD0') is ca"

```
00357D10  mov      qword ptr [rsp + 8], rbx
00357D15  push     rdi
00357D16  sub      rsp, 0x50
00357D1A  movaps   xmmword ptr [rsp + 0x40], xmm6
00357D1F  mov      rax, qword ptr [rip + 0x1becb0a]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00357D26  xor      rax, rsp
00357D29  mov      qword ptr [rsp + 0x30], rax
00357D2E  mov      rcx, r9
00357D31  mov      rbx, r9
00357D34  mov      rdi, rdx
00357D37  call     0x267db0  ; -> 00267DB0 fn
00357D3C  movss    xmm1, dword ptr [rip + 0x1993e64]  ; -> 01CEBBA8 [f32 1]
00357D44  mov      rcx, rbx
00357D47  movss    dword ptr [rsp + 0x2c], xmm1
00357D4D  movaps   xmm6, xmm0
00357D50  call     0x267db0  ; -> 00267DB0 fn
00357D55  mov      rcx, rdi
00357D58  movss    dword ptr [rsp + 0x28], xmm0
00357D5E  call     0x263d00  ; -> 00263D00 fn
00357D63  test     eax, eax
00357D65  jne      0x357d77  ; -> 00357D77
00357D67  mov      rcx, rbx
00357D6A  call     0x267db0  ; -> 00267DB0 fn
00357D6F  movss    dword ptr [rsp + 0x24], xmm0
00357D75  jmp      0x357d7f  ; -> 00357D7F
00357D77  mov      dword ptr [rsp + 0x24], 0
00357D7F  mov      rcx, rbx
00357D82  call     0x267db0  ; -> 00267DB0 fn
00357D87  movaps   xmm1, xmm6
00357D8A  movss    dword ptr [rsp + 0x20], xmm0
00357D90  mov      rcx, rdi
00357D93  call     0x26aad0  ; -> 0026AAD0 fn
00357D98  lea      rdx, [rsp + 0x20]
00357D9D  mov      rcx, rdi
00357DA0  call     0x2ec2c0  ; -> 002EC2C0 fn
00357DA5  xorps    xmm2, xmm2
00357DA8  xor      edx, edx
00357DAA  mov      rcx, rdi
00357DAD  call     0x2ec380  ; -> 002EC380 fn
00357DB2  xor      r8d, r8d
00357DB5  mov      rcx, rdi
00357DB8  lea      edx, [r8 + 1]
00357DBC  call     0x2ebe50  ; -> 002EBE50 fn
00357DC1  mov      rcx, qword ptr [rsp + 0x30]
00357DC6  xor      rcx, rsp
00357DC9  call     0x808c40  ; -> 00808C40 fn
00357DCE  mov      rbx, qword ptr [rsp + 0x60]
00357DD3  movaps   xmm6, xmmword ptr [rsp + 0x40]
00357DD8  add      rsp, 0x50
00357DDC  pop      rdi
00357DDD  ret      
```

## 00361170 (120 B, extent 00361170-003611E8)

Page context: "AL, 23 edges.** '00225580' is called by '00222740', '00222F20', '00223190', '00223DA0' and 6 more; '00362850' calls '002DF410', '002DF560', '00362C60', '00362D20' and 3 more; '00184950' is called by '00361170', '00361200'; 'Actor_GetWorldPosition' ('00265020') is called by '00362850'; '00362850' is called by '00363560'; '003A1D30' is called by '00361810'; '00581930' calls '00225580'.  **CombatFormula — MECHANICAL, 64 edges.** 'RNG_MT199"

```
00361170  mov      qword ptr [rsp + 8], rbx
00361175  mov      qword ptr [rsp + 0x10], rsi
0036117A  push     rdi
0036117B  sub      rsp, 0x20
0036117F  mov      esi, r8d
00361182  mov      ebx, edx
00361184  mov      edi, ecx
00361186  call     0x184950  ; -> 00184950 fn
0036118B  mov      r9d, eax
0036118E  mov      eax, ebx
00361190  cdq      
00361191  idiv     r9d
00361194  lea      ebx, [rax + 1]
00361197  test     edi, edi
00361199  js       0x3611d8  ; -> 003611D8
0036119B  call     0x2f16b0  ; -> 002F16B0 fn
003611A0  test     rax, rax
003611A3  je       0x3611d8  ; -> 003611D8
003611A5  lea      rcx, [rip - 0x12c]  ; -> 00361080
003611AC  mov      dword ptr [rax + 0x1c], 0x10001
003611B3  xor      edx, edx
003611B5  mov      qword ptr [rax + 8], rcx
003611B9  mov      ecx, edi
003611BB  mov      qword ptr [rax + 0x10], rdx
003611BF  mov      dword ptr [rax + 4], ebx
003611C2  mov      dword ptr [rax + 0x28], edi
003611C5  mov      dword ptr [rax + 0x30], esi
003611C8  mov      dword ptr [rax], edx
003611CA  call     0x361030  ; -> 00361030 fn
003611CF  test     rax, rax
003611D2  je       0x3611d8  ; -> 003611D8
003611D4  or       byte ptr [rax + 2], 2
003611D8  mov      rbx, qword ptr [rsp + 0x30]
003611DD  mov      rsi, qword ptr [rsp + 0x38]
003611E2  add      rsp, 0x20
003611E6  pop      rdi
003611E7  ret      
```

## 00363560 (96 B, extent 00363560-003635C0)

Page context: "alls '002DF410', '002DF560', '00362C60', '00362D20' and 3 more; '00184950' is called by '00361170', '00361200'; 'Actor_GetWorldPosition' ('00265020') is called by '00362850'; '00362850' is called by '00363560'; '003A1D30' is called by '00361810'; '00581930' calls '00225580'.  **CombatFormula — MECHANICAL, 64 edges.** 'RNG_MT19937_NextU32_Thunk' ('00379CD0') is called by 'BattleFormula_BuildCandidateStatusMask' ('003851F0'), '00387130', "

```
00363560  sub      rsp, 0x28
00363564  cmp      dword ptr [rip + 0x1f68505], 0  ; -> 022CBA70
0036356B  mov      edx, dword ptr [rip + 0x1f6850b]  ; -> 022CBA7C
00363571  jne      0x363577  ; -> 00363577
00363573  test     edx, edx
00363575  je       0x36357e  ; -> 0036357E
00363577  xor      ecx, ecx
00363579  call     0x2df0f0  ; -> 002DF0F0 fn
0036357E  mov      dword ptr [rip + 0x1f684e8], 0  ; -> 022CBA70
00363588  mov      byte ptr [rip + 0x1f6859e], 0  ; -> 022CBB2D
0036358F  mov      byte ptr [rip + 0x1f68598], 0  ; -> 022CBB2E
00363596  call     0x362850  ; -> 00362850 fn
0036359B  call     0x3636a0  ; -> 003636A0 fn
003635A0  call     0x363750  ; -> 00363750 fn
003635A5  call     0x362850  ; -> 00362850 fn
003635AA  or       ecx, 0xffffffff
003635AD  call     0x2df690  ; -> 002DF690 fn
003635B2  or       edx, 0xffffffff
003635B5  xor      ecx, ecx
003635B7  add      rsp, 0x28
003635BB  jmp      0x2df0f0  ; -> 002DF0F0 fn
```

## 0050CDE0 (91 B, extent 0050CDE0-0050CE3B)

Page context: "_PopNumericDiscard' ('00267DB0'), 'VMValueStack_PopInt32CoerceFloat32' ('00267E10'), 'VMValueStack_PushFloat32Bits' ('00267F60'); 'MapRef_GetPersistenceGroupId' ('00264F90') is called by '00357450', '0050CDE0'; '002EC2C0' is called by '00357C40', '00357D10'; 'PersistentFlag_SetBank512Low' ('0032AD70') is called by '00353750', '00353BD0'; '00344AF0' calls 'VMValueStack_PopNumericDiscard' ('00267DB0'), 'VMResult_WriteFloat32' ('0026B4C0')"

```
0050CDE0  mov      qword ptr [rsp + 8], rbx
0050CDE5  push     rdi
0050CDE6  sub      rsp, 0x20
0050CDEA  mov      rcx, r9
0050CDED  mov      rbx, r9
0050CDF0  call     0x267e10  ; -> 00267E10 fn
0050CDF5  mov      rcx, rbx
0050CDF8  mov      edi, eax
0050CDFA  call     0x267e10  ; -> 00267E10 fn
0050CDFF  mov      ecx, edi
0050CE01  mov      ebx, eax
0050CE03  call     0x264f10  ; -> 00264F10 fn
0050CE08  mov      edx, eax
0050CE0A  mov      ecx, ebx
0050CE0C  call     0x16d6a0  ; -> 0016D6A0 fn
0050CE11  mov      ecx, edi
0050CE13  call     0x264f40  ; -> 00264F40 fn
0050CE18  mov      edx, eax
0050CE1A  mov      ecx, ebx
0050CE1C  call     0x16d6a0  ; -> 0016D6A0 fn
0050CE21  mov      ecx, edi
0050CE23  call     0x264f90  ; -> 00264F90 fn
0050CE28  mov      edx, eax
0050CE2A  mov      ecx, ebx
0050CE2C  mov      rbx, qword ptr [rsp + 0x30]
0050CE31  add      rsp, 0x20
0050CE35  pop      rdi
0050CE36  jmp      0x16d6a0  ; -> 0016D6A0 fn
```
