# Homing pack: `22-Middleware-PhyreEngine/Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md`

Generated 2026-10-03 13:52 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h13-the-cluster-header-and-what-the-loader-rejects.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0063BC80 (623 B, extent 0063BC80-0063BEEF)

Entered from (direct sites whose caller this page cites): `0063BEF0` + 0x7B (jmp; `0063BEF0` is cited on this page)
Other direct sites: `0062FC90` + 0x8E (call)

Host context: "[rcx]' and returns 0 when that is non-null, else 0x13 | Interior anchor '00638A70'; Interior anchor '00638A93'; Interior anchor '00638AAF'; Interior anchor '00638AC4'; Interior anchor '00638AC7' | | '0063BEF0' | 141 B | returns 0 when 'rdx' is null; otherwise calls '00637440()', hashes the zero-terminated byte string at 'rdx' (start 0x7B5, then times 0x21 plus the byte AND 0x1F per byte) and calls '0063BEF0+0x53(00637440 result, &stack "

```
0063BC80  push     r13
0063BC82  sub      rsp, 0x40
0063BC86  mov      r8d, dword ptr [rcx + 0x10]
0063BC8A  mov      r13, rdx
0063BC8D  mov      eax, dword ptr [rdx + 0xec]
0063BC93  btr      r8d, 0x1f
0063BC98  cmp      eax, r8d
0063BC9B  jae      0x63bcb1  ; -> 0063BCB1
0063BC9D  shl      rax, 5
0063BCA1  add      rax, qword ptr [rcx + 0x18]
0063BCA5  je       0x63bcb1  ; -> 0063BCB1
0063BCA7  mov      eax, dword ptr [rax + 0x10]
0063BCAA  add      rsp, 0x40
0063BCAE  pop      r13
0063BCB0  ret      
0063BCB1  mov      rax, qword ptr [rdx + 0x78]
0063BCB5  test     rax, rax
0063BCB8  je       0x63bcd2  ; -> 0063BCD2
0063BCBA  nop      word ptr [rax + rax]
0063BCC0  cmp      dword ptr [rax + 0xec], 0
0063BCC7  jge      0x63bcdb  ; -> 0063BCDB
0063BCC9  mov      rax, qword ptr [rax + 0x78]
0063BCCD  test     rax, rax
0063BCD0  jne      0x63bcc0  ; -> 0063BCC0
0063BCD2  xor      eax, eax
0063BCD4  add      rsp, 0x40
0063BCD8  pop      r13
0063BCDA  ret      
0063BCDB  mov      edx, dword ptr [rax + 0xec]
0063BCE1  mov      qword ptr [rsp + 0x58], rbp
0063BCE6  mov      qword ptr [rsp + 0x30], r12
0063BCEB  xor      r12d, r12d
0063BCEE  mov      qword ptr [rsp + 0x20], r15
0063BCF3  mov      r15d, r12d
0063BCF6  cmp      edx, r8d
0063BCF9  jae      0x63bd07  ; -> 0063BD07
0063BCFB  mov      ebp, edx
0063BCFD  shl      rbp, 5
0063BD01  add      rbp, qword ptr [rcx + 0x18]
0063BD05  jmp      0x63bd0a  ; -> 0063BD0A
0063BD07  mov      rbp, r12
0063BD0A  mov      qword ptr [rsp + 0x28], r14
0063BD0F  mov      rax, rbp
0063BD12  test     rbp, rbp
0063BD15  je       0x63bd21  ; -> 0063BD21
0063BD17  mov      r14d, dword ptr [rbp + 0x18]
0063BD1B  add      rbp, 0x20
0063BD1F  jmp      0x63bd25  ; -> 0063BD25
0063BD21  or       r14d, 0xffffffff
0063BD25  test     rax, rax
0063BD28  je       0x63bed1  ; -> 0063BED1
0063BD2E  mov      qword ptr [rsp + 0x38], rdi
0063BD33  mov      rdi, qword ptr [rax]
0063BD36  cmp      rdi, rax
0063BD39  cmove    rdi, r12
0063BD3D  cmp      rdi, rbp
0063BD40  jne      0x63bd63  ; -> 0063BD63
0063BD42  cmp      dword ptr [rbp + 0x18], r14d
0063BD46  jg       0x63bd4d  ; -> 0063BD4D
0063BD48  mov      rdi, r12
0063BD4B  jmp      0x63bd5a  ; -> 0063BD5A
0063BD4D  mov      rax, qword ptr [rdi]
0063BD50  cmp      rax, rdi
0063BD53  cmove    rax, r12
0063BD57  mov      rdi, rax
0063BD5A  add      rbp, 0x20
0063BD5E  cmp      rdi, rbp
0063BD61  je       0x63bd42  ; -> 0063BD42
0063BD63  test     rdi, rdi
0063BD66  je       0x63becc  ; -> 0063BECC
0063BD6C  mov      qword ptr [rsp + 0x50], rbx
0063BD71  mov      qword ptr [rsp + 0x60], rsi
0063BD76  nop      word ptr [rax + rax]
0063BD80  mov      rcx, qword ptr [rdi + 0x18]
0063BD84  mov      rax, rcx
0063BD87  test     rcx, rcx
0063BD8A  je       0x63be81  ; -> 0063BE81
0063BD90  cmp      rax, r13
0063BD93  je       0x63bda3  ; -> 0063BDA3
0063BD95  mov      rax, qword ptr [rax + 0x78]
0063BD99  test     rax, rax
0063BD9C  jne      0x63bd90  ; -> 0063BD90
0063BD9E  jmp      0x63be81  ; -> 0063BE81
0063BDA3  mov      esi, dword ptr [rcx + 0x38]
0063BDA6  mov      rcx, qword ptr [rdi + 0x28]
0063BDAA  mov      ebx, dword ptr [rdi + 0x3c]
0063BDAD  mov      r9, qword ptr [rdi - 0x28]
0063BDB1  mov      qword ptr [rsp], rcx
0063BDB5  mov      qword ptr [rsp + 8], r9
0063BDBA  test     ebx, ebx
0063BDBC  je       0x63be81  ; -> 0063BE81
0063BDC2  cmp      rcx, r9
0063BDC5  jne      0x63bde4  ; -> 0063BDE4
0063BDC7  nop      word ptr [rax + rax]
0063BDD0  mov      r9, qword ptr [r9]
0063BDD3  add      rcx, rsi
0063BDD6  cmp      rcx, r9
0063BDD9  je       0x63bdd0  ; -> 0063BDD0
0063BDDB  mov      qword ptr [rsp], rcx
0063BDDF  mov      qword ptr [rsp + 8], r9
0063BDE4  mov      r11d, dword ptr [rsp]
0063BDE8  mov      r10d, ebx
0063BDEB  cmp      rcx, r9
0063BDEE  jae      0x63bdfe  ; -> 0063BDFE
0063BDF0  mov      eax, dword ptr [rsp + 8]
0063BDF4  xor      edx, edx
0063BDF6  sub      eax, r11d
0063BDF9  div      esi
0063BDFB  mov      r10d, eax
0063BDFE  add      r15d, r10d
0063BE01  mov      r8d, esi
0063BE04  imul     r8d, r10d
0063BE08  add      rcx, r8
0063BE0B  test     r9, r9
0063BE0E  je       0x63be72  ; -> 0063BE72
0063BE10  cmp      rcx, r9
0063BE13  jbe      0x63be4e  ; -> 0063BE4E
0063BE15  mov      eax, dword ptr [rsp + 8]
0063BE19  xor      edx, edx
0063BE1B  sub      eax, r11d
0063BE1E  mov      rcx, r9
0063BE21  div      esi
0063BE23  sub      ebx, eax
0063BE25  sub      r10d, eax
0063BE28  nop      dword ptr [rax + rax]
0063BE30  mov      r9, qword ptr [r9]
0063BE33  add      rcx, rsi
0063BE36  cmp      rcx, r9
0063BE39  je       0x63be30  ; -> 0063BE30
0063BE3B  mov      qword ptr [rsp], rcx
0063BE3F  mov      qword ptr [rsp + 8], r9
0063BE44  test     r10d, r10d
0063BE47  je       0x63be79  ; -> 0063BE79
0063BE49  mov      r11d, ecx
0063BE4C  jmp      0x63be01  ; -> 0063BE01
0063BE4E  sub      ebx, r10d
0063BE51  mov      qword ptr [rsp], rcx
0063BE55  cmp      rcx, r9
0063BE58  jne      0x63be79  ; -> 0063BE79
0063BE5A  nop      word ptr [rax + rax]
0063BE60  mov      r9, qword ptr [r9]
0063BE63  add      rcx, rsi
0063BE66  cmp      rcx, r9
0063BE69  je       0x63be60  ; -> 0063BE60
0063BE6B  mov      qword ptr [rsp + 8], r9
0063BE70  jmp      0x63be75  ; -> 0063BE75
0063BE72  sub      ebx, r10d
0063BE75  mov      qword ptr [rsp], rcx
0063BE79  test     ebx, ebx
0063BE7B  jne      0x63bde4  ; -> 0063BDE4
0063BE81  test     rdi, rdi
0063BE84  je       0x63bec2  ; -> 0063BEC2
0063BE86  mov      rax, qword ptr [rdi]
0063BE89  cmp      rax, rdi
0063BE8C  cmove    rax, r12
0063BE90  mov      rdi, rax
0063BE93  cmp      rax, rbp
0063BE96  jne      0x63beb9  ; -> 0063BEB9
0063BE98  cmp      dword ptr [rbp + 0x18], r14d
0063BE9C  jg       0x63bea3  ; -> 0063BEA3
0063BE9E  mov      rdi, r12
0063BEA1  jmp      0x63beb0  ; -> 0063BEB0
0063BEA3  mov      rax, qword ptr [rdi]
0063BEA6  cmp      rax, rdi
0063BEA9  cmove    rax, r12
0063BEAD  mov      rdi, rax
0063BEB0  add      rbp, 0x20
0063BEB4  cmp      rdi, rbp
0063BEB7  je       0x63be98  ; -> 0063BE98
0063BEB9  test     rdi, rdi
0063BEBC  jne      0x63bd80  ; -> 0063BD80
0063BEC2  mov      rsi, qword ptr [rsp + 0x60]
0063BEC7  mov      rbx, qword ptr [rsp + 0x50]
0063BECC  mov      rdi, qword ptr [rsp + 0x38]
0063BED1  mov      r14, qword ptr [rsp + 0x28]
0063BED6  mov      eax, r15d
0063BED9  mov      r15, qword ptr [rsp + 0x20]
0063BEDE  mov      r12, qword ptr [rsp + 0x30]
0063BEE3  mov      rbp, qword ptr [rsp + 0x58]
0063BEE8  add      rsp, 0x40
0063BEEC  pop      r13
0063BEEE  ret      
```
