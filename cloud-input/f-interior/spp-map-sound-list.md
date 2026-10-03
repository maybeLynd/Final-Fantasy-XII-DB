# F-interior pack: `18-Audio/Sound-Bank-And-Voice-Formats/spp-map-sound-list.md`

Generated 2026-10-03 02:49 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/spp-map-sound-list.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: cd6bd7f58	SWE2-DATA consolidated publish: progress-report cluster (generation store, R3 semantics, DB_GOAL, me; d0fd168a2	SWE2-DATA: batch-5 review corrections (clamping page's .data vf00 cell restored, SD-190 gate on the ; inbox mentions: FABLE.md, SWE2-DATA.md, SWE2-FRONTIER.md). OPUS read these before packing.

## 00363410 (113 B, extent 00363410-00363481)

Page context: "00379290', '00378120' (+1 more) - shared machinery across the layer boundary, no shared ownership. ## SWE2-EC7-98 update (2026-09-20) - '002DF190' measured  '002DF190' (16 B) is the argument-shuffle '00363410', '00363B40' and '00363E40' call: 'r9d = edx', 'r8d = ecx', 'edx = 0', 'ecx = 1', then tail 'jmp 001DBF50' - the (1,0)-repack into the shared sound-list helper. Interior anchor '002DF19B' (the '001DBF50' tail jmp).  ## SWE2-DATA up"

```
00363410  push     rbx
00363412  sub      rsp, 0x20
00363416  mov      ebx, ecx
00363418  test     ecx, ecx
0036341A  je       0x363438  ; -> 00363438
0036341C  movzx    eax, byte ptr [rip + 0x1f6870a]  ; -> 022CBB2D
00363423  cmp      eax, ecx
00363425  je       0x363475  ; -> 00363475
00363427  call     0x363840  ; -> 00363840 fn
0036342C  mov      byte ptr [rip + 0x1f686fb], bl  ; -> 022CBB2D
00363432  add      rsp, 0x20
00363436  pop      rbx
00363437  ret      
00363438  cmp      dword ptr [rip + 0x1f68631], 0  ; -> 022CBA70
0036343F  je       0x36345a  ; -> 0036345A
00363441  test     edx, edx
00363443  jle      0x363452  ; -> 00363452
00363445  mov      ecx, dword ptr [rip + 0x1f68631]  ; -> 022CBA7C
0036344B  call     0x2df190  ; -> 002DF190 fn
00363450  jmp      0x36346b  ; -> 0036346B
00363452  mov      edx, dword ptr [rip + 0x1f68624]  ; -> 022CBA7C
00363458  jmp      0x363464  ; -> 00363464
0036345A  mov      edx, dword ptr [rip + 0x1f6861c]  ; -> 022CBA7C
00363460  test     edx, edx
00363462  je       0x36346b  ; -> 0036346B
00363464  xor      ecx, ecx
00363466  call     0x2df0f0  ; -> 002DF0F0 fn
0036346B  mov      dword ptr [rip + 0x1f685fb], 0  ; -> 022CBA70
00363475  mov      byte ptr [rip + 0x1f686b2], bl  ; -> 022CBB2D
0036347B  add      rsp, 0x20
0036347F  pop      rbx
00363480  ret      
```

## 003DF550 (82 B, extent 003DF550-003DF5A2)

Page context: "arithmetic, not record bytes. Sixteen sites take the kind from an argument or a record word ('00249210''s family is the menu set, kind 7 at every resolved caller; '003DDA70' words '+0x10' / '+0x12'; '003DF550' words '+0x2C' / '+0x2E'; '003E9EF0''s word table; '003A13F0''s record dwords '+0x18' / '+0x20'; the wrappers '0032EB40', '0051ED10', '00330310', '00378030'), and a data-section scan for '(1, 24)' and '(1, 58)' in those record shap"

```
003DF550  push     rbx
003DF552  sub      rsp, 0x60
003DF556  mov      eax, dword ptr [rcx + 0x34]
003DF559  mov      rbx, rcx
003DF55C  movsx    edx, word ptr [rcx + 0x2e]
003DF560  movsx    ecx, word ptr [rcx + 0x2c]
003DF564  mov      dword ptr [rsp + 0x30], eax
003DF568  lea      rax, [rip - 0x2af]  ; -> 003DF2C0
003DF56F  mov      r9d, dword ptr [rbx + 0x30]
003DF573  mov      r8, qword ptr [rbx + 0x18]
003DF577  mov      qword ptr [rsp + 0x40], rax
003DF57C  lea      rax, [rsp + 0x30]
003DF581  mov      qword ptr [rsp + 0x20], rax
003DF586  mov      qword ptr [rsp + 0x48], 0
003DF58F  mov      dword ptr [rsp + 0x38], ebx
003DF593  call     0x32e620  ; -> 0032E620 fn
003DF598  mov      byte ptr [rbx + 0x10], 3
003DF59C  add      rsp, 0x60
003DF5A0  pop      rbx
003DF5A1  ret      
```
