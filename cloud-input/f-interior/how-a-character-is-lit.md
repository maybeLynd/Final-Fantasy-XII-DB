# F-interior pack: `17-Presentation-Rendering/Character-Rendering/how-a-character-is-lit.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/how-a-character-is-lit.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ; inbox mentions: FABLE.md, SWE2-EC7.md). OPUS read these before packing.

## 003477E0 (26 B, extent 003477E0-003477FA)

Page context: "FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*  **Script_VM_Native_Bridge — CLIENT (22 edges).** Two script verb bodies drive this page's flag write directly: '003477E0' and '00347D60' each fetch the current record, take its manager index at '+0x28' and tail into '003DDC20' with 1 and with 0, so one verb sets and the other clears bit 6 of the record's byte '+0x17'. Twenty more Script VM bodies (26"

```
003477E0  sub      rsp, 0x28
003477E4  call     0x2640c0  ; -> 002640C0 fn
003477E9  mov      edx, 1
003477EE  mov      ecx, dword ptr [rax + 0x28]
003477F1  add      rsp, 0x28
003477F5  jmp      0x3ddc20  ; -> 003DDC20 fn
```

## 00347D60 (23 B, extent 00347D60-00347D77)

Page context: "debt): one paragraph per layer the audit still reported for this page.*  **Script_VM_Native_Bridge — CLIENT (22 edges).** Two script verb bodies drive this page's flag write directly: '003477E0' and '00347D60' each fetch the current record, take its manager index at '+0x28' and tail into '003DDC20' with 1 and with 0, so one verb sets and the other clears bit 6 of the record's byte '+0x17'. Twenty more Script VM bodies (26 to 157 bytes; "

```
00347D60  sub      rsp, 0x28
00347D64  call     0x2640c0  ; -> 002640C0 fn
00347D69  xor      edx, edx
00347D6B  mov      ecx, dword ptr [rax + 0x28]
00347D6E  add      rsp, 0x28
00347D72  jmp      0x3ddc20  ; -> 003DDC20 fn
```

## 003AED20 (45 B, extent 003AED20-003AED4D)

Page context: "gh the object at record '+0x108' and walks it. Its entries are the   same block without the pool header. Their scope is simpler - kind 1 sub 2 needs the id to match; **kind 3 tests a   group mask**: '003AED20(id)' gives the character's group bits, sub 7 needs them to meet the target and sub 6 needs them   not to. Ambient entries are handled as below, with the per-character scale switched off around the evaluator;   the rest are appended"

```
003AED20  cmp      cx, -1
003AED24  jne      0x3aed29  ; -> 003AED29
003AED26  xor      eax, eax
003AED28  ret      
003AED29  movsx    rax, cx
003AED2D  imul     rcx, rax, 0x740
003AED34  add      rcx, qword ptr [rip + 0x1f181ed]  ; -> 022C6F28
003AED3B  je       0x3aed26  ; -> 003AED26
003AED3D  cmp      dword ptr [rcx + 0x284], 0
003AED44  je       0x3aed26  ; -> 003AED26
003AED46  mov      eax, dword ptr [rcx + 0x28c]
003AED4C  ret      
```

## 003DD6C0 (113 B, extent 003DD6C0-003DD731)

Page context: "red  '003DDC20' (38 B) is the bit-6 flag write the lighting callers run: '00263FF0(rcx)' resolves the record, 'byte[+0x17]' is cleared of '0x40' then OR-ed with '(edx != 0) << 6', and the body tails '003DD6C0' - one flag bit by argument. Interior anchor '003DDC41' (the '003DD6C0' tail).  ## SWE2-EC7-113 update (2026-09-21) - '00862910' measured  '00862910' (31 B) is the float4-to-int4 conversion '004FD4B0' runs: four 'cvttss2si' reads t"

```
003DD6C0  mov      qword ptr [rsp + 8], rbx
003DD6C5  mov      qword ptr [rsp + 0x10], rsi
003DD6CA  push     rdi
003DD6CB  sub      rsp, 0x20
003DD6CF  xor      edi, edi
003DD6D1  mov      ebx, edi
003DD6D3  lea      esi, [rdi + 1]
003DD6D6  mov      ecx, ebx
003DD6D8  call     0x263ff0  ; -> 00263FF0 fn
003DD6DD  test     byte ptr [rax + 0x10], sil
003DD6E1  je       0x3dd6ea  ; -> 003DD6EA
003DD6E3  test     byte ptr [rax + 0x17], 0x40
003DD6E7  cmovne   edi, esi
003DD6EA  inc      ebx
003DD6EC  cmp      ebx, 5
003DD6EF  jl       0x3dd6d6  ; -> 003DD6D6
003DD6F1  test     edi, edi
003DD6F3  je       0x3dd71a  ; -> 003DD71A
003DD6F5  call     0x37b330  ; -> 0037B330 fn
003DD6FA  test     eax, 0xfffffffd
003DD6FF  jne      0x3dd721  ; -> 003DD721
003DD701  mov      ecx, 2
003DD706  mov      rbx, qword ptr [rsp + 0x30]
003DD70B  mov      rsi, qword ptr [rsp + 0x38]
003DD710  add      rsp, 0x20
003DD714  pop      rdi
003DD715  jmp      0x37b450  ; -> 0037B450 fn
003DD71A  xor      ecx, ecx
003DD71C  call     0x37b490  ; -> 0037B490 fn
003DD721  mov      rbx, qword ptr [rsp + 0x30]
003DD726  mov      rsi, qword ptr [rsp + 0x38]
003DD72B  add      rsp, 0x20
003DD72F  pop      rdi
003DD730  ret      
```
