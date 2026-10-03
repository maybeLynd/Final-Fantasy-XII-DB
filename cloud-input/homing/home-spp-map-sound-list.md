# Homing pack: `18-Audio/Sound-Bank-And-Voice-Formats/spp-map-sound-list.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-spp-map-sound-list.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00210D90 (114 B, extent 00210D90-00210E02)

Entered from (direct sites whose caller this page cites): `001DBF50` + 0x32 (call; `001DBF50` is cited on this page)
Other direct sites: none

Host context: "-EC7-98 update (2026-09-20) - '002DF190' measured  '002DF190' (16 B) is the argument-shuffle '00363410', '00363B40' and '00363E40' call: 'r9d = edx', 'r8d = ecx', 'edx = 0', 'ecx = 1', then tail 'jmp 001DBF50' - the (1,0)-repack into the shared sound-list helper. Interior anchor '002DF19B' (the '001DBF50' tail jmp).  ## SWE2-DATA update (2026-09-27) — the bands are '.sab' folders; the split is namespace, not dispatch  **The id is the fi"

```
00210D90  mov      qword ptr [rsp + 8], rbx
00210D95  mov      qword ptr [rsp + 0x10], rbp
00210D9A  mov      qword ptr [rsp + 0x18], rsi
00210D9F  push     rdi
00210DA0  sub      rsp, 0x20
00210DA4  mov      eax, dword ptr [rsp + 0x50]
00210DA8  mov      ebx, r9d
00210DAB  or       ebx, 0x80000000
00210DB1  mov      esi, r8d
00210DB4  test     edx, edx
00210DB6  mov      rbp, rcx
00210DB9  mov      rcx, qword ptr [rcx + 8]
00210DBD  mov      edi, 1
00210DC2  cmovne   ebx, r9d
00210DC6  mov      edx, esi
00210DC8  test     eax, eax
00210DCA  mov      r8d, ebx
00210DCD  cmovne   edi, eax
00210DD0  mov      r9d, edi
00210DD3  call     0x21b800  ; -> 0021B800 fn
00210DD8  test     al, al
00210DDA  jne      0x210ded  ; -> 00210DED
00210DDC  mov      rcx, qword ptr [rbp + 0x10]
00210DE0  mov      r9d, edi
00210DE3  mov      r8d, ebx
00210DE6  mov      edx, esi
00210DE8  call     0x21a250  ; -> 0021A250 fn
00210DED  mov      rbx, qword ptr [rsp + 0x30]
00210DF2  mov      rbp, qword ptr [rsp + 0x38]
00210DF7  mov      rsi, qword ptr [rsp + 0x40]
00210DFC  add      rsp, 0x20
00210E00  pop      rdi
00210E01  ret      
```

## 003DF360 (122 B, extent 003DF360-003DF3DA)

Entered from (direct sites whose caller this page cites): `003DF2C0` + 0x83 (call; `003DF2C0` is cited on this page)
Other direct sites: none

Host context: "B' | | '003DF550' | 82 B | calls '0032E620(signed word +0x2c, signed word +0x2e, qword +0x18, dword +0x30, &s)' with a stack record 's' holding dword '+0x34' at '+0', the low dword of 'rcx' at '+8', '003DF2C0' at qword '+0x10' and 0 at qword '+0x18', then stores byte 3 at '+0x10' | '003DF564', '003DF577', '003DF58F', '003DF593', '003DF598' | "

```
003DF360  cmp      edx, 7
003DF363  ja       0x3df3d9  ; -> 003DF3D9
003DF365  mov      qword ptr [rsp + 0x10], rbx
003DF36A  push     rdi
003DF36B  sub      rsp, 0x20
003DF36F  movsxd   rax, edx
003DF372  mov      rdi, r9
003DF375  mov      qword ptr [rsp + 0x30], rsi
003DF37A  mov      rbx, r8
003DF37D  movsxd   rcx, ecx
003DF380  lea      rcx, [rax + rcx*8]
003DF384  imul     rsi, rcx, 0x38
003DF388  lea      rax, [rip + 0x2779fd1]  ; -> 02B59360
003DF38F  add      rsi, rax
003DF392  je       0x3df3ca  ; -> 003DF3CA
003DF394  test     rbx, rbx
003DF397  je       0x3df3ca  ; -> 003DF3CA
003DF399  mov      qword ptr [rsi + 8], rbx
003DF39D  test     r9, r9
003DF3A0  jne      0x3df3a9  ; -> 003DF3A9
003DF3A2  mov      edi, dword ptr [r8 + 0xc]
003DF3A6  add      rdi, rbx
003DF3A9  or       ecx, 0xffffffff
003DF3AC  call     0x2dee90  ; -> 002DEE90 fn
003DF3B1  mov      edx, dword ptr [rbx + 8]
003DF3B4  mov      rcx, rdi
003DF3B7  call     0x2df070  ; -> 002DF070 fn
003DF3BC  or       ecx, 0xffffffff
003DF3BF  mov      dword ptr [rsi], eax
003DF3C1  call     0x2dee90  ; -> 002DEE90 fn
003DF3C6  mov      byte ptr [rsi + 0x10], 4
003DF3CA  mov      rsi, qword ptr [rsp + 0x30]
003DF3CF  mov      rbx, qword ptr [rsp + 0x38]
003DF3D4  add      rsp, 0x20
003DF3D8  pop      rdi
003DF3D9  ret      
```
