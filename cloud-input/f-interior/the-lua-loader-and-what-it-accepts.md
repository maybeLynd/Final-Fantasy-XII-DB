# F-interior pack: `23-Third-Party-Libraries/Lua-Core/the-lua-loader-and-what-it-accepts.md`

Generated 2026-10-03 03:15 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-lua-loader-and-what-it-accepts.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 6075e3017	SWE2-FRONTIER for FABLE: pass-22 unattributed appends - the other 11 PUBLISHABLE pages (batch 2, 21/). OPUS read these before packing.

## 005928F0 (109 B, extent 005928F0-0059295D)

Page context: "02CAB088' is then -1, fills the node at '02CAB058': qwords '+0'/'+8'/'+0x10' = the node, qword '+0x18' = the '0062FF50()' result and '+0x20' = the '00630030()' result (called first), qword '+0x28' = '005928F0', registers '00808B90(008A8400)' and closes with '0080929C(02CAB088)'; on every path it then sets bit '0x1' of qword '+0x10', sets '+0'/'+8' to '01F2CDA0', and walks the tree from the root qword '01F2CDB8' comparing (qword '+0x18',"

```
005928F0  mov      qword ptr [rsp + 8], rbx
005928F5  mov      qword ptr [rsp + 0x10], rdi
005928FA  mov      rax, qword ptr [r9 + 8]
005928FE  movzx    r10d, byte ptr [r8 + 0xc]
00592903  mov      ebx, dword ptr [r8 + 4]
00592907  test     r10b, r10b
0059290A  mov      edi, dword ptr [r8 + 8]
0059290E  mov      r11d, dword ptr [rax + 8]
00592912  mov      rax, qword ptr [r9 + 0x10]
00592916  mov      r8d, dword ptr [r8]
00592919  mov      r9d, dword ptr [rax + 0x48]
0059291D  mov      eax, r9d
00592920  cmovne   eax, r11d
00592924  add      rcx, rax
00592927  test     r10b, r10b
0059292A  cmovne   r11d, r9d
0059292E  mov      eax, r11d
00592931  add      rdx, rax
00592934  test     r8d, r8d
00592937  je       0x592952  ; -> 00592952
00592939  nop      dword ptr [rax]
00592940  movsx    eax, byte ptr [rcx]
00592943  add      rcx, rbx
00592946  mov      word ptr [rdx], ax
00592949  add      rdx, rdi
0059294C  sub      r8, 1
00592950  jne      0x592940  ; -> 00592940
00592952  mov      rbx, qword ptr [rsp + 8]
00592957  mov      rdi, qword ptr [rsp + 0x10]
0059295C  ret      
```

## 00595C00 (108 B, extent 00595C00-00595C6C)

Page context: ")' and, when '02CAB018' is then -1, fills the node at '02CAAFE8': qwords '+0'/'+8'/'+0x10' = the node, qword '+0x18' = the second and '+0x20' = the first of two '0062FF50()' results, qword '+0x28' = '00595C00', registers '00808B90(008A83E0)' and closes with '0080929C(02CAB018)'; on every path it then sets bit '0x1' of qword '+0x10', sets '+0'/'+8' to '01F2CDA0', and walks the tree from the root qword '01F2CDB8' comparing (qword '+0x18',"

```
00595C00  mov      qword ptr [rsp + 8], rbx
00595C05  mov      qword ptr [rsp + 0x10], rdi
00595C0A  mov      rax, qword ptr [r9 + 8]
00595C0E  movzx    r10d, byte ptr [r8 + 0xc]
00595C13  mov      ebx, dword ptr [r8 + 4]
00595C17  test     r10b, r10b
00595C1A  mov      edi, dword ptr [r8 + 8]
00595C1E  mov      r11d, dword ptr [rax + 8]
00595C22  mov      rax, qword ptr [r9 + 0x10]
00595C26  mov      r8d, dword ptr [r8]
00595C29  mov      r9d, dword ptr [rax + 0x48]
00595C2D  mov      eax, r9d
00595C30  cmovne   eax, r11d
00595C34  add      rcx, rax
00595C37  test     r10b, r10b
00595C3A  cmovne   r11d, r9d
00595C3E  mov      eax, r11d
00595C41  add      rdx, rax
00595C44  test     r8d, r8d
00595C47  je       0x595c61  ; -> 00595C61
00595C49  nop      dword ptr [rax]
00595C50  movzx    eax, byte ptr [rcx]
00595C53  add      rcx, rbx
00595C56  mov      byte ptr [rdx], al
00595C58  add      rdx, rdi
00595C5B  sub      r8, 1
00595C5F  jne      0x595c50  ; -> 00595C50
00595C61  mov      rbx, qword ptr [rsp + 8]
00595C66  mov      rdi, qword ptr [rsp + 0x10]
00595C6B  ret      
```
