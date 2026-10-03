# Homing pack: `16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`

Generated 2026-10-03 00:35 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-numeric-formatting-and-character-mapping.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0028F810 (19 B, extent 0028F810-0028F823)

Entered from (direct sites whose caller this page cites): `002A5520` + 0x12 (call; `002A5520` is cited on this page)
Other direct sites: `0029BC80` + 0xFE (call); `0029BC80` + 0x10B (call); `0029BC80` + 0x11E (call); `0029BC80` + 0x15A (call); `0029BC80` + 0x167 (call); `003FACF0` + 0x1B8 (call); `003FAF10` + 0x45E (call); `003FC3F0` + 0xB1 (call)

Host context: "ths the reads and adds fall on absolute low addresses | Interior anchor '002A4032'; Interior anchor '002A405E'; Interior anchor '002A4062'; Interior anchor '002A40A1'; Interior anchor '002A40A6' | | '002A5520' | 109 B | '002A70B0' + 0x40D | takes 'v' = '002A5520' + 0x12('rcx'), replaced by 0x1C0 ('01E0C1DC') when negative, and calls '002A5520' + 0x25 with bit 11 of dword 'rcx+0x114'; returns the truncated integer of float('v' minus 5 ti"

```
0028F810  mov      rcx, qword ptr [rip + 0x1e0c669]  ; -> 0209BE80
0028F817  mov      rcx, qword ptr [rcx + 0x10f78]
0028F81E  jmp      0x296450  ; -> 00296450 fn
```

## 00406DD0 (167 B, extent 00406DD0-00406E77)

Entered from (direct sites whose caller this page cites): `004052A0` + 0x9 (jmp; `004052A0` is cited on this page); `004052B0` + 0xC (jmp; `004052B0` is cited on this page)
Other direct sites: `00404E10` + 0x38 (call)

Host context: "0 ('00902708') times the float from '002A5520' + 0x48 | Interior anchor '002A5532'; Interior anchor '002A554C'; Interior anchor '002A555F'; Interior anchor '002A5572'; Interior anchor '002A557E' | | '004052A0' | 14 B | '003EC810' + 0xD | tail-jumps to '004052A0' + 0x9 with qword '02B62D88' in 'rcx' and 0 in 'edx' | Interior anchor '004052A7'; Interior anchor '004052A9' | | '004052B0' | 17 B | '003EC830' + 0xD | tail-jumps to '004052B0' " / "anchor '002A557E' | | '004052A0' | 14 B | '003EC810' + 0xD | tail-jumps to '004052A0' + 0x9 with qword '02B62D88' in 'rcx' and 0 in 'edx' | Interior anchor '004052A7'; Interior anchor '004052A9' | | '004052B0' | 17 B | '003EC830' + 0xD | tail-jumps to '004052B0' + 0xC with qword '02B62D88' in 'rcx' and 1 in 'edx' | Interior anchor '004052B7'; Interior anchor '004052BC' | | '00574770' | 390 B | '005742D0' + 0x10D | takes 'r' = '00574770'"

```
00406DD0  test     rcx, rcx
00406DD3  je       0x406e76  ; -> 00406E76
00406DD9  push     rsi
00406DDA  sub      rsp, 0x20
00406DDE  mov      esi, edx
00406DE0  mov      edx, dword ptr [rcx + 0xc8]
00406DE6  mov      eax, edx
00406DE8  shr      eax, 5
00406DEB  and      eax, 1
00406DEE  cmp      esi, eax
00406DF0  je       0x406e71  ; -> 00406E71
00406DF2  mov      eax, esi
00406DF4  mov      qword ptr [rsp + 0x30], rbx
00406DF9  shl      eax, 5
00406DFC  mov      ebx, 0xc8
00406E01  xor      eax, edx
00406E03  mov      qword ptr [rsp + 0x38], rdi
00406E08  and      eax, 0x20
00406E0B  xor      eax, edx
00406E0D  mov      dword ptr [rcx + 0xc8], eax
00406E13  xor      edi, edi
00406E15  mov      rax, qword ptr [rip + 0x275bf6c]  ; -> 02B62D88
00406E1C  nop      dword ptr [rax]
00406E20  test     rax, rax
00406E23  je       0x406e57  ; -> 00406E57
00406E25  mov      rcx, qword ptr [rax + 0xc0]
00406E2C  test     rcx, rcx
00406E2F  je       0x406e57  ; -> 00406E57
00406E31  cmp      rdi, 2
00406E35  jge      0x406e57  ; -> 00406E57
00406E37  mov      rcx, qword ptr [rbx + rcx]
00406E3B  test     rcx, rcx
00406E3E  je       0x406e57  ; -> 00406E57
00406E40  test     byte ptr [rcx + 0x130], 0x10
00406E47  je       0x406e57  ; -> 00406E57
00406E49  mov      edx, esi
00406E4B  call     0x406770  ; -> 00406770 fn
00406E50  mov      rax, qword ptr [rip + 0x275bf31]  ; -> 02B62D88
00406E57  inc      rdi
00406E5A  add      rbx, 8
00406E5E  cmp      rbx, 0xd8
00406E65  jl       0x406e20  ; -> 00406E20
00406E67  mov      rdi, qword ptr [rsp + 0x38]
00406E6C  mov      rbx, qword ptr [rsp + 0x30]
00406E71  add      rsp, 0x20
00406E75  pop      rsi
00406E76  ret      
```
