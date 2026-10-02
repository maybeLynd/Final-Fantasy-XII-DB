# F-interior pack: `17-Presentation-Rendering/Character-Render-Records/the-focus-point-of-a-character.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-focus-point-of-a-character.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ). OPUS read these before packing.

## 0040A210 (28 B, extent 0040A210-0040A22C)

Page context: "esource bodies: 'ResourceTable_ResolveEntryByIndex' ('002ED570'), 'ResourceEntry_GetResolvedBasePointer' ('00409600'), 'ResourceEntry_FindSectionIndexAndOffset' ('00409780'), '00409A60', '00409FE0', '0040A210', '0051FBB0', '0051FCF0', '0051FE30' and '0051FF30'. Kind 1 of the focus point reads its frame chunk out of the character's resource through the resource layer's own chunk finder and handle resolver; the resource layer owns the fil"

```
0040A210  push     rbx
0040A212  sub      rsp, 0x20
0040A216  mov      rbx, rcx
0040A219  mov      rcx, qword ptr [rcx + 0x30]
0040A21D  call     0x3ab7f0  ; -> 003AB7F0 fn
0040A222  mov      qword ptr [rbx + 0x38], rax
0040A226  add      rsp, 0x20
0040A22A  pop      rbx
0040A22B  ret      
```

## 00423510 (85 B, extent 00423510-00423565)

Page context: "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: the per-frame body 003E43D0, its four helpers (003E5ED0, 003E5FA0, 003E6070, 0046FAA0), the two chunk     lookups (004234B0, 00423510) and one getter (003E5810) disassembled whole; the ease table and the smoothing constant read from the image;     consumers found by a displacement sweep of record +0x670..+0x688 and a raw call sweep of the getter family last_revie"

```
00423510  push     rbx
00423512  sub      rsp, 0x20
00423516  mov      rcx, rdx
00423519  call     0x3ab7f0  ; -> 003AB7F0 fn
0042351E  mov      rbx, rax
00423521  test     rax, rax
00423524  je       0x42355d  ; -> 0042355D
00423526  xor      r8d, r8d
00423529  mov      edx, 0x4d524640
0042352E  mov      rcx, rax
00423531  call     0x408f90  ; -> 00408F90 fn
00423536  cmp      eax, -1
00423539  je       0x42355d  ; -> 0042355D
0042353B  mov      edx, eax
0042353D  mov      rcx, rbx
00423540  call     0x408f80  ; -> 00408F80 fn
00423545  movsxd   rcx, eax
00423548  add      rcx, 0x30
0042354C  je       0x42355d  ; -> 0042355D
0042354E  mov      eax, dword ptr [rcx + 0xc]
00423551  test     eax, eax
00423553  je       0x42355d  ; -> 0042355D
00423555  add      eax, ecx
00423557  add      rsp, 0x20
0042355B  pop      rbx
0042355C  ret      
0042355D  xor      eax, eax
0042355F  add      rsp, 0x20
00423563  pop      rbx
00423564  ret      
```

## 004288E0 (87 B, extent 004288E0-00428937)

Page context: "ntity if the record has none). Otherwise, and always for kind 0, it is the record's own world matrix at '+0x180'.  ## 3. One frame - '003E43D0' (814 B)  *Who runs it (added 2026-09-19; read whole):* '004288E0' (87 B), a system phase that walks the active-record list - head index at the record system's '+0x48800', next at each record's word '+4' - and calls this body on every record whose '+0x290' bit 1 is clear.  1. Offset and kind from"

```
004288E0  sub      rsp, 0x28
004288E4  mov      rdx, qword ptr [rip + 0x1e9e63d]  ; -> 022C6F28
004288EB  mov      eax, dword ptr [rdx + 0x48800]
004288F1  cmp      eax, -1
004288F4  je       0x428932  ; -> 00428932
004288F6  mov      qword ptr [rsp + 0x20], rbx
004288FB  nop      dword ptr [rax + rax]
00428900  movsxd   rcx, eax
00428903  imul     rbx, rcx, 0x740
0042890A  lea      rcx, [rbx + rdx]
0042890E  test     byte ptr [rcx + 0x290], 2
00428915  jne      0x428923  ; -> 00428923
00428917  call     0x3e43d0  ; -> 003E43D0 fn
0042891C  mov      rdx, qword ptr [rip + 0x1e9e605]  ; -> 022C6F28
00428923  movsx    eax, word ptr [rbx + rdx + 4]
00428928  cmp      eax, -1
0042892B  jne      0x428900  ; -> 00428900
0042892D  mov      rbx, qword ptr [rsp + 0x20]
00428932  add      rsp, 0x28
00428936  ret      
```
