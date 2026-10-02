# F-interior pack: `02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-authored-table-row-lookup.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (inbox mentions: FABLE.md, SWE2-FRONTIER.md, SWE2-ORACLE.md). OPUS read these before packing.

## 00249670 (13 B, extent 00249670-0024967D)

Page context: "-source-rebase.md)**, here in an index rather than a delta. No shipped count is claimed to reach that value; the boundary is recorded, not exercised.  **Carried forward as ASTRA's, not re-derived:** '00249670' → '0024A1D0''s format 13/14 preparation and the observation that **other formats also set flag 6**; '0024A4E0' being a **64 × 48 partial-reset pool rather than a fresh zeroed object**; format 14's reordering of 64-byte groups into"

```
00249670  mov      rdx, qword ptr [rcx + 8]
00249674  mov      rcx, qword ptr [rcx + 0x18]
00249678  jmp      0x24a1d0  ; -> 0024A1D0 fn
```

## 002A1A80 (119 B, extent 002A1A80-002A1AF7)

Page context: "x+8]                 ; first row's field 002A0145  ecx = [rbx] 002A0147  add ecx, ebp                     ; <-- TABLE-BASE-relative 002A0150  lea rbx, [rbx+0xC]               ; stride 0xC '''  '''asm 002A1A80                                   ; table A 002A1AC3  lea rdx, [rcx+rcx*4]             ; index * 5 002A1AC7  ecx = [r14 + rdx*4 + 0x10]       ; base + index*0x14 + 0x10 002A1ACC  lea rbx, [r14 + rdx*4]           ; <-- the ROW 002A1"

```
002A1A80  mov      qword ptr [rsp + 0x10], rsi
002A1A85  mov      qword ptr [rsp + 0x18], rdi
002A1A8A  push     r14
002A1A8C  sub      rsp, 0x20
002A1A90  mov      rsi, rcx
002A1A93  mov      ecx, dword ptr [rcx + 0x20]
002A1A96  add      ecx, esi
002A1A98  call     0x20e620  ; -> 0020E620 fn
002A1A9D  mov      ecx, eax
002A1A9F  mov      dword ptr [rsi + 0x20], eax
002A1AA2  call     0x20e600  ; -> 0020E600 fn
002A1AA7  xor      edi, edi
002A1AA9  mov      r14, rax
002A1AAC  cmp      dword ptr [rsi + 0x1c], edi
002A1AAF  jbe      0x2a1ae6  ; -> 002A1AE6
002A1AB1  mov      qword ptr [rsp + 0x30], rbx
002A1AB6  nop      word ptr [rax + rax]
002A1AC0  movsxd   rcx, edi
002A1AC3  lea      rdx, [rcx + rcx*4]
002A1AC7  mov      ecx, dword ptr [r14 + rdx*4 + 0x10]
002A1ACC  lea      rbx, [r14 + rdx*4]
002A1AD0  add      ecx, ebx
002A1AD2  call     0x20e620  ; -> 0020E620 fn
002A1AD7  inc      edi
002A1AD9  mov      dword ptr [rbx + 0x10], eax
002A1ADC  cmp      edi, dword ptr [rsi + 0x1c]
002A1ADF  jb       0x2a1ac0  ; -> 002A1AC0
002A1AE1  mov      rbx, qword ptr [rsp + 0x30]
002A1AE6  mov      rsi, qword ptr [rsp + 0x38]
002A1AEB  mov      rdi, qword ptr [rsp + 0x40]
002A1AF0  add      rsp, 0x20
002A1AF4  pop      r14
002A1AF6  ret      
```

## 002D7FC0 (138 B, extent 002D7FC0-002D804A)

Page context: " 'GiSetTexture' records are built only by the factory '00863060', whose two callers take the id from the texture pool: - The allocator '002D81D0' hands out ids between '[02F8F20C]' and '[02F8F208]'. '002D7FC0' sets   those to '0x3B00 + d' and '0x3C00 + d', where 'd = (W − 0x200) × 21' when the PS2 frame width   'W = [022D8EAC]' exceeds 512, and 0 otherwise. - 'W''s only rip-relative writer stores the constant '0x200' ('0036D286'), so **"

```
002D7FC0  sub      rsp, 0x28
002D7FC4  xor      edx, edx
002D7FC6  lea      rcx, [rip + 0x2cb5a33]  ; -> 02F8DA00
002D7FCD  mov      r8d, 0x1800
002D7FD3  call     0x861ec0  ; -> 00861EC0 fn
002D7FD8  xor      edx, edx
002D7FDA  lea      rcx, [rip + 0x2cb421f]  ; -> 02F8C200
002D7FE1  mov      r8d, 0x1800
002D7FE7  call     0x861ec0  ; -> 00861EC0 fn
002D7FEC  mov      eax, dword ptr [rip + 0x2000eba]  ; -> 022D8EAC
002D7FF2  mov      dword ptr [rip + 0x2cb721c], eax  ; -> 02F8F214
002D7FF8  cmp      eax, 0x200
002D7FFD  jbe      0x2d800f  ; -> 002D800F
002D7FFF  add      eax, 0xfffffe00
002D8004  imul     edx, eax, 0x540
002D800A  shr      edx, 6
002D800D  jmp      0x2d8011  ; -> 002D8011
002D800F  xor      edx, edx
002D8011  lea      eax, [rdx + 0x3b00]
002D8017  mov      dword ptr [rip + 0x2cb71df], 0x3b00  ; -> 02F8F200
002D8021  lea      ecx, [rdx + 0x3c00]
002D8027  mov      dword ptr [rip + 0x2cb71df], eax  ; -> 02F8F20C
002D802D  lea      eax, [rdx + 0x2a00]
002D8033  mov      dword ptr [rip + 0x2cb71d7], ecx  ; -> 02F8F210
002D8039  mov      dword ptr [rip + 0x2cb71c5], eax  ; -> 02F8F204
002D803F  mov      dword ptr [rip + 0x2cb71c3], ecx  ; -> 02F8F208
002D8045  add      rsp, 0x28
002D8049  ret      
```

## 0050DAD0 (174 B, extent 0050DAD0-0050DB7E)

Page context: "lectorsAndReconcileRoster' walk the slots, and '00239960' sets 'PartyConfiguration_SetDefinitionSelectorForIndex'.  **Script_VM_Native_Bridge — CLIENT, seven edges.** The script adapters '0050D8F0', '0050DAD0', '0050DF70' and '0050DFE0' use the arena pair, the rebase and the request path.  **Input and RNG_Random_Selection — MECHANICAL, four edges through the boot.** - The bootstrap '0017D4C0' → '0022A0B0' (cited as the frame the STATIC "

```
0050DAD0  mov      qword ptr [rsp + 8], rbx
0050DAD5  mov      qword ptr [rsp + 0x10], rbp
0050DADA  mov      qword ptr [rsp + 0x18], rsi
0050DADF  push     rdi
0050DAE0  push     r14
0050DAE2  push     r15
0050DAE4  sub      rsp, 0x20
0050DAE8  mov      rsi, r9
0050DAEB  mov      rbx, rdx
0050DAEE  mov      r15, rcx
0050DAF1  call     0x2640c0  ; -> 002640C0 fn
0050DAF6  mov      r14, qword ptr [rbx + 0x40]
0050DAFA  mov      rcx, rsi
0050DAFD  mov      rbp, qword ptr [rax]
0050DB00  call     0x267e10  ; -> 00267E10 fn
0050DB05  mov      rcx, rsi
0050DB08  mov      edi, eax
0050DB0A  call     0x267e10  ; -> 00267E10 fn
0050DB0F  mov      rcx, rsi
0050DB12  mov      ebx, eax
0050DB14  call     0x267e10  ; -> 00267E10 fn
0050DB19  mov      edx, edi
0050DB1B  mov      ecx, ebx
0050DB1D  mov      esi, eax
0050DB1F  call     0x36c1d0  ; -> 0036C1D0 fn
0050DB24  mov      ecx, 5
0050DB29  call     0x36c1a0  ; -> 0036C1A0 fn
0050DB2E  mov      edx, dword ptr [r14]
0050DB31  mov      rcx, rbp
0050DB34  call     0x263e40  ; -> 00263E40 fn
0050DB39  mov      ecx, esi
0050DB3B  mov      rbx, rax
0050DB3E  call     0x36b160  ; -> 0036B160 fn
0050DB43  mov      r8d, esi
0050DB46  mov      rdx, rbx
0050DB49  mov      ecx, eax
0050DB4B  mov      edi, eax
0050DB4D  call     0x36c6c0  ; -> 0036C6C0 fn
0050DB52  call     0x36c110  ; -> 0036C110 fn
0050DB57  call     0x36c140  ; -> 0036C140 fn
0050DB5C  mov      edx, edi
0050DB5E  mov      rcx, r15
0050DB61  mov      rbx, qword ptr [rsp + 0x40]
0050DB66  mov      rbp, qword ptr [rsp + 0x48]
0050DB6B  mov      rsi, qword ptr [rsp + 0x50]
0050DB70  add      rsp, 0x20
0050DB74  pop      r15
0050DB76  pop      r14
0050DB78  pop      rdi
0050DB79  jmp      0x26b4e0  ; -> 0026B4E0 fn
```
