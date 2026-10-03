# Homing pack: `18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-how-a-sound-request-becomes-a-voice.json`.

Bodies: 9. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002085B0 (120 B, extent 002085B0-00208628)

Entered from (direct sites whose caller this page cites): `002081A0` + 0x9 (call; `002081A0` is cited on this page)
Other direct sites: none

Host context: "0') and tail-jumps to '00209530' with 'rcx' unchanged | Interior anchor '00207F5C'; Interior anchor '00207F6F'; Interior anchor '00207FA1'; Interior anchor '00207FA4'; Interior anchor '00207FAB' | | '002081A0' | 114 B | '00206430' + 0x207 | returns 'al' = 0 when the call at '002081A0' + 0x9 on 'rcx' returns zero 'al'; otherwise stores the sign-extended byte 'rcx+0x78' to dword 'rcx+0x74', then, when qword '[rcx]' differs from qword 'rcx"

```
002085B0  mov      edx, dword ptr [rcx + 0x80]
002085B6  movsx    eax, byte ptr [rcx + 0x78]
002085BA  bt       edx, 0x16
002085BE  jae      0x2085ea  ; -> 002085EA
002085C0  add      eax, -0x44
002085C3  cmp      eax, 0x33
002085C6  ja       0x2085e7  ; -> 002085E7
002085C8  lea      r8, [rip - 0xe85cf]  ; -> 00120000 (image base)
002085CF  cdqe     
002085D1  movzx    eax, byte ptr [r8 + rax + 0xe8630]
002085DA  mov      ecx, dword ptr [r8 + rax*4 + 0xe8628]  ; image base + 0xe8628 = 00208628
002085E2  add      rcx, r8
002085E5  jmp      rcx
002085E7  mov      al, 1
002085E9  ret      
002085EA  add      eax, -0x22
002085ED  cmp      eax, 0x5b
002085F0  ja       0x208625  ; -> 00208625
002085F2  lea      r8, [rip - 0xe85f9]  ; -> 00120000 (image base)
002085F9  cdqe     
002085FB  movzx    eax, byte ptr [r8 + rax + 0xe8674]
00208604  mov      ecx, dword ptr [r8 + rax*4 + 0xe8664]  ; image base + 0xe8664 = 00208664
0020860C  add      rcx, r8
0020860F  jmp      rcx
00208611  shr      edx, 0x17
00208614  and      edx, 1
00208617  movzx    eax, dl
0020861A  ret      
0020861B  shr      edx, 0x18
0020861E  and      edx, 1
00208621  movzx    eax, dl
00208624  ret      
00208625  xor      al, al
00208627  ret      
```

## 00218DC0 (88 B, extent 00218DC0-00218E18)

Entered from (direct sites whose caller this page cites): `002109F0` + 0x22 (call; `002109F0` is cited on this page)
Other direct sites: none

Host context: "'; it then calls '00209530(rcx)' and returns 'al' = 1 | Interior anchor '002081A9'; Interior anchor '002081B9'; Interior anchor '002081F4'; Interior anchor '002081FD'; Interior anchor '00208202' | | '002109F0' | 67 B | '001DBAC0' + 0x35 | when dword 'rcx+0x30' differs from 'r8d', 'edx' is not negative and 'r9d' is nonzero, it calls the site '002109F0' + 0x22 with qword '[rcx]' in 'rcx' and 'edx', 'r8d', 'r9d' passed through; on every pa"

```
00218DC0  mov      qword ptr [rsp + 8], rbx
00218DC5  mov      qword ptr [rsp + 0x10], rbp
00218DCA  mov      qword ptr [rsp + 0x18], rsi
00218DCF  push     rdi
00218DD0  sub      rsp, 0x20
00218DD4  mov      rbx, qword ptr [rcx + 8]
00218DD8  lea      rsi, [rcx + 8]
00218DDC  mov      ebp, r8d
00218DDF  mov      edi, edx
00218DE1  cmp      rbx, rsi
00218DE4  je       0x218e03  ; -> 00218E03
00218DE6  mov      rcx, qword ptr [rbx + 0x10]
00218DEA  cmp      edi, -1
00218DED  je       0x218df4  ; -> 00218DF4
00218DEF  cmp      dword ptr [rcx + 0x50], edi
00218DF2  jne      0x218dfb  ; -> 00218DFB
00218DF4  mov      edx, ebp
00218DF6  call     0x222ad0  ; -> 00222AD0 fn
00218DFB  mov      rbx, qword ptr [rbx]
00218DFE  cmp      rbx, rsi
00218E01  jne      0x218de6  ; -> 00218DE6
00218E03  mov      rbx, qword ptr [rsp + 0x30]
00218E08  mov      rbp, qword ptr [rsp + 0x38]
00218E0D  mov      rsi, qword ptr [rsp + 0x40]
00218E12  add      rsp, 0x20
00218E16  pop      rdi
00218E17  ret      
```

## 0021D640 (109 B, extent 0021D640-0021D6AD)

Entered from (direct sites whose caller this page cites): `00211220` + 0x8 (jmp; `00211220` is cited on this page)
Other direct sites: none

Host context: "qword 'rcx+8' and 'edx'; returns 1 when either call returned nonzero 'al', else 0 | Interior anchor '00210AA3'; Interior anchor '00210AAE'; Interior anchor '00210AB6'; Interior anchor '00210AC9' | | '00211220' | 13 B | '001DC240' + 0x35 | replaces 'rcx' with qword 'rcx+0x18', zero-extends 'r9b' into 'r9d', and tail-jumps at '00211220' + 0x8 with 'edx' and 'r8' passed through | Interior anchor '00211224'; Interior anchor '00211228' | | '"

```
0021D640  mov      qword ptr [rsp + 8], rbx
0021D645  mov      qword ptr [rsp + 0x10], rbp
0021D64A  mov      qword ptr [rsp + 0x18], rsi
0021D64F  mov      qword ptr [rsp + 0x20], rdi
0021D654  push     r14
0021D656  sub      rsp, 0x20
0021D65A  mov      rbx, qword ptr [rcx + 8]
0021D65E  lea      rsi, [rcx + 8]
0021D662  mov      ebp, r9d
0021D665  mov      r14d, r8d
0021D668  mov      edi, edx
0021D66A  cmp      rbx, rsi
0021D66D  je       0x21d692  ; -> 0021D692
0021D66F  nop      
0021D670  mov      rcx, qword ptr [rbx + 0x10]
0021D674  test     edi, edi
0021D676  js       0x21d67d  ; -> 0021D67D
0021D678  cmp      dword ptr [rcx + 0x38], edi
0021D67B  jne      0x21d68a  ; -> 0021D68A
0021D67D  mov      r9d, ebp
0021D680  mov      r8d, r14d
0021D683  mov      edx, edi
0021D685  call     0x225280  ; -> 00225280 fn
0021D68A  mov      rbx, qword ptr [rbx]
0021D68D  cmp      rbx, rsi
0021D690  jne      0x21d670  ; -> 0021D670
0021D692  mov      rbx, qword ptr [rsp + 0x30]
0021D697  mov      rbp, qword ptr [rsp + 0x38]
0021D69C  mov      rsi, qword ptr [rsp + 0x40]
0021D6A1  mov      rdi, qword ptr [rsp + 0x48]
0021D6A6  add      rsp, 0x20
0021D6AA  pop      r14
0021D6AC  ret      
```

## 00220DA0 (52 B, extent 00220DA0-00220DD4)

Entered from (direct sites whose caller this page cites): `002228A0` + 0x113 (call; `002228A0` is cited on this page)
Other direct sites: none

Host context: "') is the music cross-fade: if a bank with the requested id (or any bank, for -1) is already playing ('00222A20', bank state 2) it returns at once; otherwise the bank with that id is started through '002228A0' with a frame count ('r9') and every other bank is faded out over the same count through '00222A80', whose frames divide by 60.0 into seconds.  Interior anchor '00218B41' (function '00218AE0').  '00218C10' (43 B; forwarder '0021099"

```
00220DA0  mov      qword ptr [rsp + 8], rbx
00220DA5  push     rdi
00220DA6  sub      rsp, 0x20
00220DAA  mov      rdi, rcx
00220DAD  movsxd   rbx, edx
00220DB0  xor      ecx, ecx
00220DB2  cmp      ebx, 0xff
00220DB8  setbe    cl
00220DBB  call     0x16d6a0  ; -> 0016D6A0 fn
00220DC0  movss    xmm0, dword ptr [rdi + rbx*4 + 0x3d8]
00220DC9  mov      rbx, qword ptr [rsp + 0x30]
00220DCE  add      rsp, 0x20
00220DD2  pop      rdi
00220DD3  ret      
```

## 00221100 (51 B, extent 00221100-00221133)

Entered from (direct sites whose caller this page cites): `002228A0` + 0xBB (call; `002228A0` is cited on this page)
Other direct sites: none

Host context: "') is the music cross-fade: if a bank with the requested id (or any bank, for -1) is already playing ('00222A20', bank state 2) it returns at once; otherwise the bank with that id is started through '002228A0' with a frame count ('r9') and every other bank is faded out over the same count through '00222A80', whose frames divide by 60.0 into seconds.  Interior anchor '00218B41' (function '00218AE0').  '00218C10' (43 B; forwarder '0021099"

```
00221100  mov      qword ptr [rsp + 8], rbx
00221105  push     rdi
00221106  sub      rsp, 0x20
0022110A  mov      rdi, rcx
0022110D  movsxd   rbx, edx
00221110  xor      ecx, ecx
00221112  cmp      ebx, 0xff
00221118  setbe    cl
0022111B  call     0x16d6a0  ; -> 0016D6A0 fn
00221120  movzx    eax, byte ptr [rbx + rdi + 0x7d8]
00221128  mov      rbx, qword ptr [rsp + 0x30]
0022112D  add      rsp, 0x20
00221131  pop      rdi
00221132  ret      
```

## 00221280 (134 B, extent 00221280-00221306)

Entered from (direct sites whose caller this page cites): `002228A0` + 0x126 (call; `002228A0` is cited on this page)
Other direct sites: `00218CE0` + 0x17 (jmp)

Host context: "') is the music cross-fade: if a bank with the requested id (or any bank, for -1) is already playing ('00222A20', bank state 2) it returns at once; otherwise the bank with that id is started through '002228A0' with a frame count ('r9') and every other bank is faded out over the same count through '00222A80', whose frames divide by 60.0 into seconds.  Interior anchor '00218B41' (function '00218AE0').  '00218C10' (43 B; forwarder '0021099"

```
00221280  mov      qword ptr [rsp + 8], rbx
00221285  mov      qword ptr [rsp + 0x10], rsi
0022128A  push     rdi
0022128B  sub      rsp, 0x20
0022128F  xor      ebx, ebx
00221291  movsxd   rsi, edx
00221294  mov      rdi, rcx
00221297  test     edx, edx
00221299  jns      0x2212d8  ; -> 002212D8
0022129B  mov      eax, ebx
0022129D  lea      rdx, [rcx + 0x3d8]
002212A4  nop      dword ptr [rax]
002212A8  nop      dword ptr [rax + rax]
002212B0  mov      dword ptr [rdx], ebx
002212B2  lea      rdx, [rdx + 4]
002212B6  mov      byte ptr [rcx + rax + 0x7d8], bl
002212BD  inc      rax
002212C0  cmp      rax, 0x100
002212C6  jl       0x2212b0  ; -> 002212B0
002212C8  mov      rbx, qword ptr [rsp + 0x30]
002212CD  mov      rsi, qword ptr [rsp + 0x38]
002212D2  add      rsp, 0x20
002212D6  pop      rdi
002212D7  ret      
002212D8  cmp      esi, 0x100
002212DE  mov      ecx, ebx
002212E0  setl     cl
002212E3  call     0x16d6a0  ; -> 0016D6A0 fn
002212E8  mov      dword ptr [rdi + rsi*4 + 0x3d8], ebx
002212EF  mov      byte ptr [rsi + rdi + 0x7d8], bl
002212F6  mov      rbx, qword ptr [rsp + 0x30]
002212FB  mov      rsi, qword ptr [rsp + 0x38]
00221300  add      rsp, 0x20
00221304  pop      rdi
00221305  ret      
```

## 00223060 (110 B, extent 00223060-002230CE)

Entered from (direct sites whose caller this page cites): `00219E30` + 0x3D (call; `00219E30` is cited on this page)
Other direct sites: none

Host context: "nd the 'SepAudioController' second: it sets bit 31 of the fourth argument unless the second argument is non-zero, calls '0021B540' on the Seb controller ('+0x08'), and only when that returns 0 calls '00219E30' on the Sep controller ('+0x10') with the same arguments.  Interior anchor '00210BAA' (function '00210B70').  ## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)  *Functions no page cited u"

```
00223060  mov      qword ptr [rsp + 8], rbx
00223065  push     rdi
00223066  sub      rsp, 0x20
0022306A  mov      edi, r9d
0022306D  test     edx, edx
0022306F  je       0x2230a4  ; -> 002230A4
00223071  call     0x221ed0  ; -> 00221ED0 fn
00223076  mov      rbx, rax
00223079  test     rax, rax
0022307C  je       0x2230c1  ; -> 002230C1
0022307E  mov      rcx, rax
00223081  call     0x225680  ; -> 00225680 fn
00223086  test     eax, eax
00223088  je       0x2230c1  ; -> 002230C1
0022308A  xor      r8d, r8d
0022308D  mov      edx, edi
0022308F  mov      rcx, rbx
00223092  call     0x2256f0  ; -> 002256F0 fn
00223097  mov      al, 1
00223099  mov      rbx, qword ptr [rsp + 0x30]
0022309E  add      rsp, 0x20
002230A2  pop      rdi
002230A3  ret      
002230A4  cmp      dword ptr [rcx + 0x38], r8d
002230A8  jne      0x2230c1  ; -> 002230C1
002230AA  xor      r8d, r8d
002230AD  mov      edx, edi
002230AF  call     0x222490  ; -> 00222490 fn
002230B4  mov      al, 1
002230B6  mov      rbx, qword ptr [rsp + 0x30]
002230BB  add      rsp, 0x20
002230BF  pop      rdi
002230C0  ret      
002230C1  xor      al, al
002230C3  mov      rbx, qword ptr [rsp + 0x30]
002230C8  add      rsp, 0x20
002230CC  pop      rdi
002230CD  ret      
```

## 00223EE0 (91 B, extent 00223EE0-00223F3B)

Entered from (direct sites whose caller this page cites): `0021B540` + 0x3D (call; `0021B540` is cited on this page)
Other direct sites: none

Host context: "DBD60') is a registry-level request that tries the 'SebAudioController' first and the 'SepAudioController' second: it sets bit 31 of the fourth argument unless the second argument is non-zero, calls '0021B540' on the Seb controller ('+0x08'), and only when that returns 0 calls '00219E30' on the Sep controller ('+0x10') with the same arguments.  Interior anchor '00210BAA' (function '00210B70').  ## Homed frontier bodies called from this "

```
00223EE0  mov      qword ptr [rsp + 8], rbx
00223EE5  push     rdi
00223EE6  sub      rsp, 0x20
00223EEA  mov      edi, r9d
00223EED  test     edx, edx
00223EEF  je       0x223ef8  ; -> 00223EF8
00223EF1  call     0x221ed0  ; -> 00221ED0 fn
00223EF6  jmp      0x223f00  ; -> 00223F00
00223EF8  mov      edx, r8d
00223EFB  call     0x221e60  ; -> 00221E60 fn
00223F00  mov      rbx, rax
00223F03  test     rax, rax
00223F06  je       0x223f2e  ; -> 00223F2E
00223F08  mov      rcx, rax
00223F0B  call     0x225680  ; -> 00225680 fn
00223F10  test     eax, eax
00223F12  je       0x223f2e  ; -> 00223F2E
00223F14  xor      r8d, r8d
00223F17  mov      edx, edi
00223F19  mov      rcx, rbx
00223F1C  call     0x2256f0  ; -> 002256F0 fn
00223F21  mov      al, 1
00223F23  mov      rbx, qword ptr [rsp + 0x30]
00223F28  add      rsp, 0x20
00223F2C  pop      rdi
00223F2D  ret      
00223F2E  xor      al, al
00223F30  mov      rbx, qword ptr [rsp + 0x30]
00223F35  add      rsp, 0x20
00223F39  pop      rdi
00223F3A  ret      
```

## 00225400 (52 B, extent 00225400-00225434)

Entered from (direct sites whose caller this page cites): `0021D920` + 0x46 (call; `0021D920` is cited on this page)
Other direct sites: none

Host context: "more than a forwarder: it loads the 'StreamAudioController' (registry slot '+0x18'), masks the fourth argument to 7 bits ('and r9d, 0x7F', the volume width the play path also uses) and tail-jumps to '0021D920'.  Interior anchor '002112C4' (function '002112C0').  '00210B70' (105 B; from '001DBD60') is a registry-level request that tries the 'SebAudioController' first and the 'SepAudioController' second: it sets bit 31 of the fourth argum"

```
00225400  mov      qword ptr [rsp + 8], rbx
00225405  push     rdi
00225406  sub      rsp, 0x20
0022540A  xor      edx, edx
0022540C  mov      ebx, r9d
0022540F  mov      edi, r8d
00225412  call     0x221e60  ; -> 00221E60 fn
00225417  test     rax, rax
0022541A  je       0x225429  ; -> 00225429
0022541C  mov      r8d, edi
0022541F  mov      edx, ebx
00225421  mov      rcx, rax
00225424  call     0x2257e0  ; -> 002257E0 fn
00225429  mov      rbx, qword ptr [rsp + 0x30]
0022542E  add      rsp, 0x20
00225432  pop      rdi
00225433  ret      
```
