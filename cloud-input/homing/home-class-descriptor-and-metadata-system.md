# Homing pack: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-class-descriptor-and-metadata-system.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 006AAA20 (17 B, extent 006AAA20-006AAA31)

Entered from (direct sites whose caller this page cites): `005A9480` + 0x14 (call; `005A9480` is cited on this page)
Other direct sites: `006A97C0` + 0x10 (call); `006ADE00` + 0x2A (call); `006AFDC0` + 0x27 (call); `006CDF00` + 0x2A (call)

Host context: "wn** vtable, and excluding the descriptor   constructor, the known destructor and anything that also sits in a vtable slot, leaves a   candidate for only **44** classes — and at least one candidate ('005A9480') is shared between   'PAnimatableComponent' and 'PAnimationTargetBlenderController', so even those are not per-class.  **So the cells stay empty.** Two thirds of these classes are non-polymorphic and have no vtable to install, whi"

```
006AAA20  xor      eax, eax
006AAA22  mov      qword ptr [rcx], rax
006AAA25  mov      qword ptr [rcx + 8], rax
006AAA29  mov      rax, rcx
006AAA2C  mov      qword ptr [rcx + 0x10], rdx
006AAA30  ret      
```

## 006B6820 (114 B, extent 006B6820-006B6892)

Entered from (direct sites whose caller this page cites): `00661A70` + 0x7A (call; `00661A70` is cited on this page); `006D5810` + 0x7A (call; `006D5810` is cited on this page)
Other direct sites: `005A65B0` + 0x7A (call); `005D8BE0` + 0x7A (call); `0062CC80` + 0x7A (call); `006B6B60` + 0x7A (call); `006BEAC0` + 0x7A (call); `006C0C90` + 0x7A (call); `006CD270` + 0x7A (call); `006D94E0` + 0x7A (call); `006D98D0` + 0x7A (call); `00875F00` + 0x7A (call); `008762F0` + 0x7A (call); `008766D0` + 0x7A (call); `00876AE0` + 0x7A (call); `00876EC0` + 0x7A (call); `008793D0` + 0x7A (call)

Host context: "body constructs no class descriptor. X is a static data-member object in 15 rows ('PClassDataMember*<…>'), a 'PTypeDefault<unsigned int>' in '006315B0', and a 'PNamedSemanticDescriptorForType<…>' in '00661A70' and '006D5810'. ['fam_rows.py'](../../_index/candidates/opus-ee-guarded-registration-1003/fam_rows.py) re-derives every row and compares it with the committed ['rows.tsv'](../../_index/candidates/opus-ee-guarded-registration-1003/" / " no class descriptor. X is a static data-member object in 15 rows ('PClassDataMember*<…>'), a 'PTypeDefault<unsigned int>' in '006315B0', and a 'PNamedSemanticDescriptorForType<…>' in '00661A70' and '006D5810'. ['fam_rows.py'](../../_index/candidates/opus-ee-guarded-registration-1003/fam_rows.py) re-derives every row and compares it with the committed ['rows.tsv'](../../_index/candidates/opus-ee-guarded-registration-1003/rows.tsv). Two "

```
006B6820  mov      r10, rcx
006B6823  lea      rax, [rcx + 8]
006B6827  mov      qword ptr [rax], rax
006B682A  xor      ecx, ecx
006B682C  mov      qword ptr [rax + 8], rax
006B6830  mov      qword ptr [rax + 0x10], rax
006B6834  mov      dword ptr [rax + 0x18], ecx
006B6837  mov      qword ptr [rax + 0x20], rcx
006B683B  lea      rcx, [r10 + 0x50]
006B683F  mov      rax, qword ptr [rsp + 0x28]
006B6844  mov      qword ptr [r10 + 0x40], rax
006B6848  mov      rax, qword ptr [rsp + 0x30]
006B684D  mov      qword ptr [r10 + 0x48], rax
006B6851  lea      rax, [rip + 0x6ca118]  ; -> 00D80970
006B6858  mov      qword ptr [r10 + 0x30], rdx
006B685C  lea      rdx, [rip + 0x1878355]  ; -> 01F2EBB8
006B6863  mov      dword ptr [r10 + 0x38], r8d
006B6867  mov      dword ptr [r10 + 0x3c], r9d
006B686B  mov      qword ptr [rcx], rcx
006B686E  mov      qword ptr [rcx + 8], rcx
006B6872  mov      qword ptr [r10], rax
006B6875  mov      rax, qword ptr [rip + 0x187833c]  ; -> 01F2EBB8 [u64 0x0000000001F2EBB8]
006B687C  mov      qword ptr [rcx], rax
006B687F  mov      qword ptr [rcx + 8], rdx
006B6883  mov      qword ptr [rip + 0x187832e], rcx  ; -> 01F2EBB8 [u64 0x0000000001F2EBB8]
006B688A  mov      qword ptr [rax + 8], rcx
006B688E  mov      rax, r10
006B6891  ret      
```

## 006C7D00 (178 B, extent 006C7D00-006C7DB2)

Entered from (direct sites whose caller this page cites): `0060F2D0` + 0x58 (call; `0060F2D0` is cited on this page)
Other direct sites: `0060F680` + 0x1E (jmp); `006C68B0` + 0x6A (call)

Host context: "| | '005D7060' | 39 B | calls '006388C0' with the address '02CB7CA0', ORs 0x20 into dword '02CB7D9C' and tail-jumps to '00639450' with the address '02CB7CA0' | '005D706B', '005D7070', '005D7082' | | '0060F2D0' | 116 B | calls '00630180' with the incoming registers and then slot '+8' of the returned object's vtable; when 'rdx' equals 'rcx' + 8, 'r8d' is 1 and that slot's result is non-null it calls '00639850(result, rcx + 8, 1)', otherwi"

```
006C7D00  mov      qword ptr [rsp + 0x18], rbx
006C7D05  push     rdi
006C7D06  sub      rsp, 0x20
006C7D0A  mov      rdi, rdx
006C7D0D  mov      rbx, rcx
006C7D10  test     r8d, r8d
006C7D13  jns      0x6c7d25  ; -> 006C7D25
006C7D15  mov      eax, 5
006C7D1A  mov      rbx, qword ptr [rsp + 0x40]
006C7D1F  add      rsp, 0x20
006C7D23  pop      rdi
006C7D24  ret      
006C7D25  mov      eax, dword ptr [rcx]
006C7D27  btr      eax, 0x1f
006C7D2B  mov      qword ptr [rsp + 0x30], rsi
006C7D30  mov      qword ptr [rsp + 0x38], r14
006C7D35  cmp      eax, 1
006C7D38  jbe      0x6c7d40  ; -> 006C7D40
006C7D3A  mov      rcx, qword ptr [rcx + 8]
006C7D3E  jmp      0x6c7d4c  ; -> 006C7D4C
006C7D40  test     eax, eax
006C7D42  je       0x6c7d4a  ; -> 006C7D4A
006C7D44  add      rcx, 8
006C7D48  jmp      0x6c7d4c  ; -> 006C7D4C
006C7D4A  xor      ecx, ecx
006C7D4C  mov      esi, r8d
006C7D4F  bts      esi, 0x1f
006C7D53  cmp      r8d, 1
006C7D57  jne      0x6c7d6e  ; -> 006C7D6E
006C7D59  lea      rdx, [rbx + 8]
006C7D5D  test     rdx, rdx
006C7D60  je       0x6c7d66  ; -> 006C7D66
006C7D62  mov      eax, dword ptr [rdi]
006C7D64  mov      dword ptr [rdx], eax
006C7D66  mov      rdi, rdx
006C7D69  mov      esi, 1
006C7D6E  lea      r14, [rbx + 8]
006C7D72  cmp      rcx, rdi
006C7D75  je       0x6c7d91  ; -> 006C7D91
006C7D77  cmp      rcx, r14
006C7D7A  je       0x6c7d91  ; -> 006C7D91
006C7D7C  mov      eax, dword ptr [rbx]
006C7D7E  shr      eax, 0x1f
006C7D81  not      al
006C7D83  test     al, 1
006C7D85  je       0x6c7d91  ; -> 006C7D91
006C7D87  test     rcx, rcx
006C7D8A  je       0x6c7d91  ; -> 006C7D91
006C7D8C  call     0x584730  ; -> 00584730 fn
006C7D91  cmp      rdi, r14
006C7D94  je       0x6c7d99  ; -> 006C7D99
006C7D96  mov      qword ptr [r14], rdi
006C7D99  mov      r14, qword ptr [rsp + 0x38]
006C7D9E  xor      eax, eax
006C7DA0  mov      dword ptr [rbx], esi
006C7DA2  mov      rsi, qword ptr [rsp + 0x30]
006C7DA7  mov      rbx, qword ptr [rsp + 0x40]
006C7DAC  add      rsp, 0x20
006C7DB0  pop      rdi
006C7DB1  ret      
```
