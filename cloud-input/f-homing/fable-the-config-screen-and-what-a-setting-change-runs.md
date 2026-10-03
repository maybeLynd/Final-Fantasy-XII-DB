# F homing pack (FABLE): `16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 6. No bearing page cites them and no documented function calls them directly.

## 003CAED0 (490 B, extent 003CAED0-003CB0BA)

Documented callee on this page: `002726C0`

```
003CAED0  mov      qword ptr [rsp + 0x10], rbx
003CAED5  mov      qword ptr [rsp + 0x18], rbp
003CAEDA  mov      qword ptr [rsp + 0x20], rsi
003CAEDF  push     rdi
003CAEE0  sub      rsp, 0x70
003CAEE4  mov      rax, qword ptr [rip + 0x1b79945]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003CAEEB  xor      rax, rsp
003CAEEE  mov      qword ptr [rsp + 0x68], rax
003CAEF3  mov      rdi, rcx
003CAEF6  lea      rdx, [rsp + 0x30]
003CAEFB  xor      ecx, ecx
003CAEFD  call     0x3200a0  ; -> 003200A0 fn
003CAF02  mov      eax, dword ptr [rdi + 0x1d0]
003CAF08  xor      ebp, ebp
003CAF0A  test     eax, eax
003CAF0C  je       0x3cafc7  ; -> 003CAFC7
003CAF12  mov      edx, dword ptr [rsp + 0x44]
003CAF16  cmp      edx, eax
003CAF18  jae      0x3cafc7  ; -> 003CAFC7
003CAF1E  lea      ecx, [rax - 1]
003CAF21  imul     rax, rcx, 0x58
003CAF25  lea      rsi, [rdi + 0xc0]
003CAF2C  add      rsi, rax
003CAF2F  mov      eax, dword ptr [rsi + 0x48]
003CAF32  test     al, 2
003CAF34  jne      0x3cafc1  ; -> 003CAFC1
003CAF3A  or       eax, 0xe
003CAF3D  mov      dword ptr [rsp + 0x28], 0xd9
003CAF45  lea      r9d, [rbp - 0x80]
003CAF49  mov      dword ptr [rsi + 0x48], eax
003CAF4C  xor      r8d, r8d
003CAF4F  mov      dword ptr [rsp + 0x20], 0x5c
003CAF57  mov      edx, 0x80
003CAF5C  mov      rcx, rsi
003CAF5F  call     0x2726c0  ; -> 002726C0 fn
003CAF64  lea      edx, [rbp + 0x20]
003CAF67  mov      rcx, rsi
003CAF6A  call     0x2727c0  ; -> 002727C0 fn
003CAF6F  mov      edx, 0x80
003CAF74  mov      dword ptr [rsp + 0x28], 0xd9
003CAF7C  mov      r8d, edx
003CAF7F  mov      dword ptr [rsp + 0x20], 0x5c
003CAF87  lea      r9d, [rbp - 0x80]
003CAF8B  lea      rcx, [rsi + 0x20]
003CAF8F  call     0x2726c0  ; -> 002726C0 fn
003CAF94  lea      edx, [rbp + 0x10]
003CAF97  mov      dword ptr [rsi + 0x28], 0xbf0
003CAF9E  lea      rcx, [rsi + 0x20]
003CAFA2  mov      dword ptr [rsi + 0x2c], 0xff0
003CAFA9  mov      dword ptr [rsi + 0x30], 0xbf0
003CAFB0  call     0x2727c0  ; -> 002727C0 fn
003CAFB5  mov      word ptr [rsi + 0x14], bp
003CAFB9  mov      word ptr [rsi + 0x34], bp
003CAFBD  mov      edx, dword ptr [rsp + 0x44]
003CAFC1  mov      dword ptr [rdi + 0x1d0], edx
003CAFC7  mov      esi, ebp
003CAFC9  lea      rbx, [rdi + 0xc0]
003CAFD0  mov      ecx, dword ptr [rbx + 0x48]
003CAFD3  mov      eax, ecx
003CAFD5  and      eax, 3
003CAFD8  cmp      al, 3
003CAFDA  jne      0x3cb088  ; -> 003CB088
003CAFE0  test     cl, 4
003CAFE3  je       0x3cb024  ; -> 003CB024
003CAFE5  mov      rcx, rbx
003CAFE8  call     0x272710  ; -> 00272710 fn
003CAFED  cmp      eax, 1
003CAFF0  jne      0x3caff8  ; -> 003CAFF8
003CAFF2  and      dword ptr [rbx + 0x48], 0xfffffffb
003CAFF6  jmp      0x3cb024  ; -> 003CB024
003CAFF8  movsx    edx, word ptr [rbx + 0x14]
003CAFFC  mov      rcx, rbx
003CAFFF  call     0x271960  ; -> 00271960 fn
003CB004  mov      edx, ebp
003CB006  mov      r8, rbp
003CB009  nop      dword ptr [rax]
003CB010  mov      rcx, qword ptr [rbx + 0x40]
003CB014  lea      r8, [r8 + 4]
003CB018  inc      edx
003CB01A  mov      byte ptr [rcx + r8 + 0x27], al
003CB01F  cmp      edx, 4
003CB022  jb       0x3cb010  ; -> 003CB010
003CB024  test     byte ptr [rbx + 0x48], 8
003CB028  je       0x3cb076  ; -> 003CB076
003CB02A  lea      rcx, [rbx + 0x20]
003CB02E  call     0x272710  ; -> 00272710 fn
003CB033  cmp      eax, 1
003CB036  jne      0x3cb03e  ; -> 003CB03E
003CB038  and      dword ptr [rbx + 0x48], 0xfffffff7
003CB03C  jmp      0x3cb076  ; -> 003CB076
003CB03E  movsx    edx, word ptr [rbx + 0x34]
003CB042  lea      rcx, [rbx + 0x20]
003CB046  call     0x271960  ; -> 00271960 fn
003CB04B  mov      r8d, ebp
003CB04E  mov      rdx, rbp
003CB051  mov      rcx, qword ptr [rbx + 0x40]
003CB055  lea      rdx, [rdx + 4]
003CB059  inc      r8d
003CB05C  mov      byte ptr [rdx + rcx + 0x24], al
003CB060  mov      rcx, qword ptr [rbx + 0x40]
003CB064  mov      byte ptr [rdx + rcx + 0x25], al
003CB068  mov      rcx, qword ptr [rbx + 0x40]
003CB06C  mov      byte ptr [rdx + rcx + 0x26], al
003CB070  cmp      r8d, 4
003CB074  jb       0x3cb051  ; -> 003CB051
003CB076  test     byte ptr [rbx + 0x48], 0xc
003CB07A  jne      0x3cb088  ; -> 003CB088
003CB07C  mov      rax, qword ptr [rbx + 0x40]
003CB080  and      dword ptr [rax + 8], 0xfffffffe
003CB084  and      dword ptr [rbx + 0x48], 0xfffffffe
003CB088  inc      esi
003CB08A  add      rbx, 0x58
003CB08E  cmp      esi, 3
003CB091  jb       0x3cafd0  ; -> 003CAFD0
003CB097  mov      rcx, qword ptr [rsp + 0x68]
003CB09C  xor      rcx, rsp
003CB09F  call     0x808c40  ; -> 00808C40 fn
003CB0A4  lea      r11, [rsp + 0x70]
003CB0A9  mov      rbx, qword ptr [r11 + 0x18]
003CB0AD  mov      rbp, qword ptr [r11 + 0x20]
003CB0B1  mov      rsi, qword ptr [r11 + 0x28]
003CB0B5  mov      rsp, r11
003CB0B8  pop      rdi
003CB0B9  ret      
```

## 00408830 (48 B, extent 00408830-00408860)

Documented callee on this page: `004073B0`

```
00408830  mov      rax, qword ptr [rip + 0x275a549]  ; -> 02B62D80
00408837  mov      edx, ecx
00408839  test     rax, rax
0040883C  je       0x408858  ; -> 00408858
0040883E  test     byte ptr [rax + 0xc8], 2
00408845  jne      0x40885f  ; -> 0040885F
00408847  test     rax, rax
0040884A  je       0x408858  ; -> 00408858
0040884C  mov      rcx, qword ptr [rax + 0xc0]
00408853  jmp      0x4073b0  ; -> 004073B0 fn
00408858  xor      ecx, ecx
0040885A  jmp      0x4073b0  ; -> 004073B0 fn
0040885F  ret      
```

## 00512140 (27 B, extent 00512140-0051215B)

Documented callee on this page: `00295D80`

```
00512140  sub      rsp, 0x28
00512144  call     0x280120  ; -> 00280120 fn
00512149  test     eax, eax
0051214B  jne      0x512156  ; -> 00512156
0051214D  add      rsp, 0x28
00512151  jmp      0x295d80  ; -> 00295D80 fn
00512156  add      rsp, 0x28
0051215A  ret      
```

## 0056CBC0 (389 B, extent 0056CBC0-0056CD45)

Documented callee on this page: `00392FC0`

```
0056CBC0  push     rbp
0056CBC2  push     r14
0056CBC4  sub      rsp, 0x38
0056CBC8  mov      rax, qword ptr [rcx + 0xc8]
0056CBCF  mov      r14, rdx
0056CBD2  test     rax, rax
0056CBD5  je       0x56cd09  ; -> 0056CD09
0056CBDB  mov      r8d, dword ptr [rcx + 0xe4]
0056CBE2  mov      qword ptr [rsp + 0x50], rbx
0056CBE7  xor      ebx, ebx
0056CBE9  mov      qword ptr [rsp + 0x58], rsi
0056CBEE  mov      qword ptr [rsp + 0x60], rdi
0056CBF3  mov      edi, dword ptr [rsp + 0x20]
0056CBF7  movsxd   rsi, r9d
0056CBFA  shl      rsi, 5
0056CBFE  add      rsi, rax
0056CC01  mov      qword ptr [rsp + 0x30], r15
0056CC06  mov      eax, r8d
0056CC09  lea      r15d, [rbx + 4]
0056CC0D  xor      eax, edi
0056CC0F  and      eax, 3
0056CC12  xor      edi, eax
0056CC14  test     r8b, 2
0056CC18  je       0x56cc55  ; -> 0056CC55
0056CC1A  mov      rcx, qword ptr [rcx + 0xc0]
0056CC21  movsx    eax, word ptr [rcx + 0xf2]
0056CC28  movsx    edx, word ptr [rcx + 0xf4]
0056CC2F  add      edx, eax
0056CC31  movzx    eax, byte ptr [rcx + 0xec]
0056CC38  imul     edx, eax
0056CC3B  movsx    eax, byte ptr [rcx + 0xee]
0056CC42  add      edx, eax
0056CC44  movsx    eax, byte ptr [rcx + 0xed]
0056CC4B  add      edx, eax
0056CC4D  mov      eax, r15d
0056CC50  cmp      edx, r9d
0056CC53  je       0x56cc57  ; -> 0056CC57
0056CC55  mov      eax, ebx
0056CC57  and      edi, 0xfffffffb
0056CC5A  or       edi, eax
0056CC5C  call     0x253690  ; -> 00253690 fn
0056CC61  mov      edx, eax
0056CC63  mov      ebp, 1
0056CC68  test     dil, 2
0056CC6C  je       0x56cc79  ; -> 0056CC79
0056CC6E  mov      ebx, edi
0056CC70  shr      ebx, 1
0056CC72  not      ebx
0056CC74  and      ebx, 2
0056CC77  jmp      0x56ccb6  ; -> 0056CCB6
0056CC79  test     bpl, dil
0056CC7C  je       0x56cca2  ; -> 0056CCA2
0056CC7E  cmp      dword ptr [rsi + 0x10], 0x80000000
0056CC85  mov      eax, 8
0056CC8A  movsx    edx, word ptr [rsi + 0xc]
0056CC8E  cmovb    eax, ebx
0056CC91  mov      ecx, eax
0056CC93  cmp      edx, -1
0056CC96  je       0x56ccb1  ; -> 0056CCB1
0056CC98  or       ecx, 2
0056CC9B  test     edx, edx
0056CC9D  cmovne   ecx, eax
0056CCA0  jmp      0x56ccb1  ; -> 0056CCB1
0056CCA2  mov      eax, dword ptr [rsi + 0x10]
0056CCA5  mov      ecx, ebx
0056CCA7  btr      eax, 0x1f
0056CCAB  cmp      eax, edx
0056CCAD  cmova    ecx, r15d
0056CCB1  test     ecx, ecx
0056CCB3  cmovne   ebx, ebp
0056CCB6  mov      edx, ebx
0056CCB8  mov      rcx, r14
0056CCBB  call     0x392fc0  ; -> 00392FC0 fn
0056CCC0  lea      r8, [rip + 0x7b68a1]  ; -> 00D23568
0056CCC7  mov      rdx, r14
0056CCCA  mov      rcx, rsi
0056CCCD  call     0x56d870  ; -> 0056D870 fn
0056CCD2  mov      r15, qword ptr [rsp + 0x30]
0056CCD7  mov      eax, ebp
0056CCD9  mov      rsi, qword ptr [rsp + 0x58]
0056CCDE  mov      rbx, qword ptr [rsp + 0x50]
0056CCE3  test     bpl, dil
0056CCE6  jne      0x56ccfc  ; -> 0056CCFC
0056CCE8  mov      rcx, qword ptr [r14 + 0x10]
0056CCEC  shr      edi, 2
0056CCEF  and      edi, ebp
0056CCF1  mov      rdx, qword ptr [rcx + 0x18]
0056CCF5  and      dword ptr [rdx + 8], 0xfffffffe
0056CCF9  or       dword ptr [rdx + 8], edi
0056CCFC  mov      rdi, qword ptr [rsp + 0x60]
0056CD01  add      rsp, 0x38
0056CD05  pop      r14
0056CD07  pop      rbp
0056CD08  ret      
0056CD09  mov      rax, qword ptr [rdx + 0x10]
0056CD0D  mov      rcx, qword ptr [rax]
0056CD10  and      dword ptr [rcx + 8], 0xfffffffe
0056CD14  mov      rax, qword ptr [rdx + 0x10]
0056CD18  mov      rcx, qword ptr [rax + 8]
0056CD1C  and      dword ptr [rcx + 8], 0xfffffffe
0056CD20  mov      rax, qword ptr [rdx + 0x10]
0056CD24  mov      rcx, qword ptr [rax + 0x10]
0056CD28  and      dword ptr [rcx + 8], 0xfffffffe
0056CD2C  mov      rax, qword ptr [rdx + 0x10]
0056CD30  mov      rcx, qword ptr [rax + 0x18]
0056CD34  mov      eax, 1
0056CD39  and      dword ptr [rcx + 8], 0xfffffffe
0056CD3D  add      rsp, 0x38
0056CD41  pop      r14
0056CD43  pop      rbp
0056CD44  ret      
```

## 0056CD50 (446 B, extent 0056CD50-0056CF0E)

Documented callee on this page: `00392FC0`

```
0056CD50  mov      qword ptr [rsp + 0x20], rbp
0056CD55  push     r14
0056CD57  sub      rsp, 0x30
0056CD5B  mov      rax, qword ptr [rcx + 0xc8]
0056CD62  mov      r14, rdx
0056CD65  test     rax, rax
0056CD68  je       0x56cec2  ; -> 0056CEC2
0056CD6E  mov      r8d, dword ptr [rcx + 0xe4]
0056CD75  mov      qword ptr [rsp + 0x40], rbx
0056CD7A  mov      ebx, dword ptr [rsp + 0x20]
0056CD7E  mov      qword ptr [rsp + 0x48], rsi
0056CD83  xor      esi, esi
0056CD85  mov      qword ptr [rsp + 0x50], rdi
0056CD8A  movsxd   rdi, r9d
0056CD8D  shl      rdi, 5
0056CD91  add      rdi, rax
0056CD94  mov      eax, r8d
0056CD97  xor      eax, ebx
0056CD99  and      eax, 3
0056CD9C  xor      ebx, eax
0056CD9E  test     r8b, 2
0056CDA2  je       0x56cddf  ; -> 0056CDDF
0056CDA4  mov      rcx, qword ptr [rcx + 0xc0]
0056CDAB  movsx    eax, word ptr [rcx + 0xf2]
0056CDB2  movsx    edx, word ptr [rcx + 0xf4]
0056CDB9  add      edx, eax
0056CDBB  movzx    eax, byte ptr [rcx + 0xec]
0056CDC2  imul     edx, eax
0056CDC5  movsx    eax, byte ptr [rcx + 0xee]
0056CDCC  add      edx, eax
0056CDCE  movsx    eax, byte ptr [rcx + 0xed]
0056CDD5  add      edx, eax
0056CDD7  lea      eax, [rsi + 4]
0056CDDA  cmp      edx, r9d
0056CDDD  je       0x56cde1  ; -> 0056CDE1
0056CDDF  mov      eax, esi
0056CDE1  and      ebx, 0xfffffffb
0056CDE4  or       ebx, eax
0056CDE6  call     0x253690  ; -> 00253690 fn
0056CDEB  mov      edx, eax
0056CDED  mov      ebp, 1
0056CDF2  test     bl, 2
0056CDF5  je       0x56ce02  ; -> 0056CE02
0056CDF7  mov      edx, ebx
0056CDF9  shr      edx, 1
0056CDFB  not      edx
0056CDFD  and      edx, 2
0056CE00  jmp      0x56ce57  ; -> 0056CE57
0056CE02  test     bpl, bl
0056CE05  je       0x56ce2b  ; -> 0056CE2B
0056CE07  cmp      dword ptr [rdi + 0x10], 0x80000000
0056CE0E  mov      eax, 8
0056CE13  movsx    edx, word ptr [rdi + 0xc]
0056CE17  cmovb    eax, esi
0056CE1A  mov      ecx, eax
0056CE1C  cmp      edx, -1
0056CE1F  je       0x56ce50  ; -> 0056CE50
0056CE21  or       ecx, 2
0056CE24  test     edx, edx
0056CE26  cmovne   ecx, eax
0056CE29  jmp      0x56ce50  ; -> 0056CE50
0056CE2B  cmp      word ptr [rdi + 0xe], bp
0056CE2F  mov      ecx, esi
0056CE31  mov      eax, dword ptr [rdi + 0x10]
0056CE34  cmovae   ecx, ebp
0056CE37  btr      eax, 0x1f
0056CE3B  cmp      eax, edx
0056CE3D  jbe      0x56ce50  ; -> 0056CE50
0056CE3F  or       ecx, 4
0056CE42  nop      dword ptr [rax]
0056CE46  nop      word ptr [rax + rax]
0056CE50  test     ecx, ecx
0056CE52  mov      edx, esi
0056CE54  cmovne   edx, ebp
0056CE57  mov      rcx, r14
0056CE5A  call     0x392fc0  ; -> 00392FC0 fn
0056CE5F  lea      r8, [rip + 0x7b66ea]  ; -> 00D23550
0056CE66  mov      rdx, r14
0056CE69  mov      rcx, rdi
0056CE6C  call     0x56d870  ; -> 0056D870 fn
0056CE71  test     bpl, bl
0056CE74  jne      0x56cea5  ; -> 0056CEA5
0056CE76  cmp      word ptr [rdi + 0xe], si
0056CE7A  mov      rax, qword ptr [r14 + 0x10]
0056CE7E  setne    sil
0056CE82  shr      ebx, 2
0056CE85  and      ebx, ebp
0056CE87  mov      rdx, qword ptr [rax + 0x20]
0056CE8B  mov      ecx, dword ptr [rdx + 8]
0056CE8E  and      ecx, 0xfffffffe
0056CE91  or       esi, ecx
0056CE93  mov      dword ptr [rdx + 8], esi
0056CE96  mov      rcx, qword ptr [r14 + 0x10]
0056CE9A  mov      rdx, qword ptr [rcx + 0x28]
0056CE9E  and      dword ptr [rdx + 8], 0xfffffffe
0056CEA2  or       dword ptr [rdx + 8], ebx
0056CEA5  mov      rsi, qword ptr [rsp + 0x48]
0056CEAA  mov      eax, ebp
0056CEAC  mov      rbx, qword ptr [rsp + 0x40]
0056CEB1  mov      rdi, qword ptr [rsp + 0x50]
0056CEB6  mov      rbp, qword ptr [rsp + 0x58]
0056CEBB  add      rsp, 0x30
0056CEBF  pop      r14
0056CEC1  ret      
0056CEC2  mov      rax, qword ptr [rdx + 0x10]
0056CEC6  mov      rbp, qword ptr [rsp + 0x58]
0056CECB  mov      rcx, qword ptr [rax]
0056CECE  and      dword ptr [rcx + 8], 0xfffffffe
0056CED2  mov      rax, qword ptr [rdx + 0x10]
0056CED6  mov      rcx, qword ptr [rax + 8]
0056CEDA  and      dword ptr [rcx + 8], 0xfffffffe
0056CEDE  mov      rax, qword ptr [rdx + 0x10]
0056CEE2  mov      rcx, qword ptr [rax + 0x10]
0056CEE6  and      dword ptr [rcx + 8], 0xfffffffe
0056CEEA  mov      rax, qword ptr [rdx + 0x10]
0056CEEE  mov      rcx, qword ptr [rax + 0x20]
0056CEF2  and      dword ptr [rcx + 8], 0xfffffffe
0056CEF6  mov      rax, qword ptr [rdx + 0x10]
0056CEFA  mov      rcx, qword ptr [rax + 0x28]
0056CEFE  mov      eax, 1
0056CF03  and      dword ptr [rcx + 8], 0xfffffffe
0056CF07  add      rsp, 0x30
0056CF0B  pop      r14
0056CF0D  ret      
```

## 0056D1B0 (446 B, extent 0056D1B0-0056D36E)

Documented callee on this page: `00392FC0`

```
0056D1B0  mov      qword ptr [rsp + 0x20], rbp
0056D1B5  push     r14
0056D1B7  sub      rsp, 0x30
0056D1BB  mov      rax, qword ptr [rcx + 0xc8]
0056D1C2  mov      r14, rdx
0056D1C5  test     rax, rax
0056D1C8  je       0x56d322  ; -> 0056D322
0056D1CE  mov      r8d, dword ptr [rcx + 0xe4]
0056D1D5  mov      qword ptr [rsp + 0x40], rbx
0056D1DA  mov      ebx, dword ptr [rsp + 0x20]
0056D1DE  mov      qword ptr [rsp + 0x48], rsi
0056D1E3  xor      esi, esi
0056D1E5  mov      qword ptr [rsp + 0x50], rdi
0056D1EA  movsxd   rdi, r9d
0056D1ED  shl      rdi, 5
0056D1F1  add      rdi, rax
0056D1F4  mov      eax, r8d
0056D1F7  xor      eax, ebx
0056D1F9  and      eax, 3
0056D1FC  xor      ebx, eax
0056D1FE  test     r8b, 2
0056D202  je       0x56d23f  ; -> 0056D23F
0056D204  mov      rcx, qword ptr [rcx + 0xc0]
0056D20B  movsx    eax, word ptr [rcx + 0xf2]
0056D212  movsx    edx, word ptr [rcx + 0xf4]
0056D219  add      edx, eax
0056D21B  movzx    eax, byte ptr [rcx + 0xec]
0056D222  imul     edx, eax
0056D225  movsx    eax, byte ptr [rcx + 0xee]
0056D22C  add      edx, eax
0056D22E  movsx    eax, byte ptr [rcx + 0xed]
0056D235  add      edx, eax
0056D237  lea      eax, [rsi + 4]
0056D23A  cmp      edx, r9d
0056D23D  je       0x56d241  ; -> 0056D241
0056D23F  mov      eax, esi
0056D241  and      ebx, 0xfffffffb
0056D244  or       ebx, eax
0056D246  call     0x253690  ; -> 00253690 fn
0056D24B  mov      edx, eax
0056D24D  mov      ebp, 1
0056D252  test     bl, 2
0056D255  je       0x56d262  ; -> 0056D262
0056D257  mov      edx, ebx
0056D259  shr      edx, 1
0056D25B  not      edx
0056D25D  and      edx, 2
0056D260  jmp      0x56d2b7  ; -> 0056D2B7
0056D262  test     bpl, bl
0056D265  je       0x56d28b  ; -> 0056D28B
0056D267  cmp      dword ptr [rdi + 0x10], 0x80000000
0056D26E  mov      eax, 8
0056D273  movsx    edx, word ptr [rdi + 0xc]
0056D277  cmovb    eax, esi
0056D27A  mov      ecx, eax
0056D27C  cmp      edx, -1
0056D27F  je       0x56d2b0  ; -> 0056D2B0
0056D281  or       ecx, 2
0056D284  test     edx, edx
0056D286  cmovne   ecx, eax
0056D289  jmp      0x56d2b0  ; -> 0056D2B0
0056D28B  cmp      word ptr [rdi + 0xe], bp
0056D28F  mov      ecx, esi
0056D291  mov      eax, dword ptr [rdi + 0x10]
0056D294  cmovae   ecx, ebp
0056D297  btr      eax, 0x1f
0056D29B  cmp      eax, edx
0056D29D  jbe      0x56d2b0  ; -> 0056D2B0
0056D29F  or       ecx, 4
0056D2A2  nop      dword ptr [rax]
0056D2A6  nop      word ptr [rax + rax]
0056D2B0  test     ecx, ecx
0056D2B2  mov      edx, esi
0056D2B4  cmovne   edx, ebp
0056D2B7  mov      rcx, r14
0056D2BA  call     0x392fc0  ; -> 00392FC0 fn
0056D2BF  lea      r8, [rip + 0x7b6272]  ; -> 00D23538
0056D2C6  mov      rdx, r14
0056D2C9  mov      rcx, rdi
0056D2CC  call     0x56d870  ; -> 0056D870 fn
0056D2D1  test     bpl, bl
0056D2D4  jne      0x56d305  ; -> 0056D305
0056D2D6  cmp      word ptr [rdi + 0xe], si
0056D2DA  mov      rax, qword ptr [r14 + 0x10]
0056D2DE  setne    sil
0056D2E2  shr      ebx, 2
0056D2E5  and      ebx, ebp
0056D2E7  mov      rdx, qword ptr [rax + 0x18]
0056D2EB  mov      ecx, dword ptr [rdx + 8]
0056D2EE  and      ecx, 0xfffffffe
0056D2F1  or       esi, ecx
0056D2F3  mov      dword ptr [rdx + 8], esi
0056D2F6  mov      rcx, qword ptr [r14 + 0x10]
0056D2FA  mov      rdx, qword ptr [rcx + 0x20]
0056D2FE  and      dword ptr [rdx + 8], 0xfffffffe
0056D302  or       dword ptr [rdx + 8], ebx
0056D305  mov      rsi, qword ptr [rsp + 0x48]
0056D30A  mov      eax, ebp
0056D30C  mov      rbx, qword ptr [rsp + 0x40]
0056D311  mov      rdi, qword ptr [rsp + 0x50]
0056D316  mov      rbp, qword ptr [rsp + 0x58]
0056D31B  add      rsp, 0x30
0056D31F  pop      r14
0056D321  ret      
0056D322  mov      rax, qword ptr [rdx + 0x10]
0056D326  mov      rbp, qword ptr [rsp + 0x58]
0056D32B  mov      rcx, qword ptr [rax]
0056D32E  and      dword ptr [rcx + 8], 0xfffffffe
0056D332  mov      rax, qword ptr [rdx + 0x10]
0056D336  mov      rcx, qword ptr [rax + 8]
0056D33A  and      dword ptr [rcx + 8], 0xfffffffe
0056D33E  mov      rax, qword ptr [rdx + 0x10]
0056D342  mov      rcx, qword ptr [rax + 0x10]
0056D346  and      dword ptr [rcx + 8], 0xfffffffe
0056D34A  mov      rax, qword ptr [rdx + 0x10]
0056D34E  mov      rcx, qword ptr [rax + 0x18]
0056D352  and      dword ptr [rcx + 8], 0xfffffffe
0056D356  mov      rax, qword ptr [rdx + 0x10]
0056D35A  mov      rcx, qword ptr [rax + 0x20]
0056D35E  mov      eax, 1
0056D363  and      dword ptr [rcx + 8], 0xfffffffe
0056D367  add      rsp, 0x30
0056D36B  pop      r14
0056D36D  ret      
```
