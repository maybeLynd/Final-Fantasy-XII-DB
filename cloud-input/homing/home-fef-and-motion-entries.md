# Homing pack: `17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-fef-and-motion-entries.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0025C130 (51 B, extent 0025C130-0025C163)

Entered from (direct sites whose caller this page cites): `0034B310` + 0xC (call; `0034B310` is cited on this page)
Other direct sites: none

Host context: "0') - shared machinery across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (2 edges).** '0026BE90', '002E8220' are called by bodies filed to Script_VM_Native_Bridge: '0034B310', '0034D8D0' - shared machinery across the layer boundary, no shared ownership. - **World - SERVICE (1 edge).** '0022A0B0' reaches bodies filed to World: '00266D10' - shared machinery across the layer boundary, no shared ownership."

```
0025C130  mov      eax, ecx
0025C132  cdq      
0025C133  and      edx, 7
0025C136  add      eax, edx
0025C138  mov      r8d, eax
0025C13B  and      eax, 7
0025C13E  sub      eax, edx
0025C140  sar      r8d, 3
0025C144  mov      ecx, eax
0025C146  mov      edx, 1
0025C14B  movsxd   rax, r8d
0025C14E  shl      dl, cl
0025C150  lea      rcx, [rip + 0x1e3e149]  ; -> 0209A2A0
0025C157  test     byte ptr [rax + rcx], dl
0025C15A  mov      eax, 0
0025C15F  setne    al
0025C162  ret      
```

## 003CD7F0 (34 B, extent 003CD7F0-003CD812)

Entered from (direct sites whose caller this page cites): `00504BC0` + 0x59 (call; `00504BC0` is cited on this page)
Other direct sites: none

Host context: "80C0', and the binder's callback '00478270'. - It finds '+0x230' written once ('005049A7') and read nowhere. Its two other hits are loop aliases: '005049E0''s   twenty-dword reset from '+0x194', and '00504BC0''s sixteen-dword read from '+0x140'. No record pointer escapes to   memory on those routes. - Control: the same census finds batch 10's three readers of '+0x218' / '+0x21C': '005044D0', '00504D30' and   '0053AB50'. It finds them on"

```
003CD7F0  movzx    r8d, cl
003CD7F4  shl      r8, 6
003CD7F8  add      r8, qword ptr [rip + 0x2779f91]  ; -> 02B47790
003CD7FF  cmp      dword ptr [r8 + 4], ecx
003CD803  jne      0x3cd811  ; -> 003CD811
003CD805  and      byte ptr [r8 + 1], 0x7f
003CD80A  shl      dl, 7
003CD80D  or       byte ptr [r8 + 1], dl
003CD811  ret      
```

## 00422FD0 (120 B, extent 00422FD0-00423048)

Entered from (direct sites whose caller this page cites): `00423B10` + 0x13F (call; `00423B10` is cited on this page)
Other direct sites: none

Host context: "E580 and its resolver 00409FE0, the EFX dispatch     003B38B0 -> 003EDAD0, the motion-descriptor init 0041BEE0, the     presentation-entry init binding at 0041D2C5-0041D374 and the motion starter     00423B10 disassembled from the authority image; the authored layouts then     re-parsed out of all 1,066 .cm and all 3,164 .ca files in the archive     (members/fef_motion_entry_census.py, 8 checks, FAILS 0), 2026-09-28 last_reviewed: 2026-"

```
00422FD0  mov      qword ptr [rsp + 8], rbx
00422FD5  push     rdi
00422FD6  sub      rsp, 0x20
00422FDA  mov      ebx, r8d
00422FDD  mov      rdi, rcx
00422FE0  test     rdx, rdx
00422FE3  je       0x42303b  ; -> 0042303B
00422FE5  mov      rcx, rdx
00422FE8  call     0x3ab7f0  ; -> 003AB7F0 fn
00422FED  mov      ecx, ebx
00422FEF  and      ecx, 0xf000
00422FF5  cmp      ecx, 0x5000
00422FFB  mov      rcx, rax
00422FFE  jne      0x423004  ; -> 00423004
00423000  xor      edx, edx
00423002  jmp      0x42300c  ; -> 0042300C
00423004  and      ebx, 0xfff
0042300A  mov      edx, ebx
0042300C  call     0x408f80  ; -> 00408F80 fn
00423011  test     rax, rax
00423014  je       0x42303b  ; -> 0042303B
00423016  test     dword ptr [rdi + 0x284], 0x10000
00423020  je       0x42303b  ; -> 0042303B
00423022  test     dword ptr [rax + 4], 0x30000
00423029  je       0x42303b  ; -> 0042303B
0042302B  mov      eax, 1
00423030  mov      rbx, qword ptr [rsp + 0x30]
00423035  add      rsp, 0x20
00423039  pop      rdi
0042303A  ret      
0042303B  xor      eax, eax
0042303D  mov      rbx, qword ptr [rsp + 0x30]
00423042  add      rsp, 0x20
00423046  pop      rdi
00423047  ret      
```
