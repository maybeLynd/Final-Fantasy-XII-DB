# F-interior pack: `02-Resource-And-Asset-Pipeline/Standard-Formats/shipped-standard-formats.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/shipped-standard-formats.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

## 00225C40 (127 B, extent 00225C40-00225CBF)

Page context: "th are shared CRT/runtime plumbing: the crossing is that Platform uses them, not a shared responsibility. - **Audio — CLIENT and SERVICE (10 edges).** 5 inbound (Audio bodies '002125A0', '006794D0', '00225C40' call page-cited '00584740', '005CD330', '005CD700'); 5 outbound (page-cited '00679A50', '006794D0', '0067A480' call Audio bodies '007A4930', '00881830', '00882200'). Substantive edges include '0067A480' calls '006794D0'; the remai"

```
00225C40  push     rdi
00225C42  sub      rsp, 0x30
00225C46  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00225C4F  mov      qword ptr [rsp + 0x48], rbx
00225C54  mov      qword ptr [rsp + 0x50], rsi
00225C59  mov      rbx, rdx
00225C5C  mov      rdi, rcx
00225C5F  xor      esi, esi
00225C61  mov      ecx, esi
00225C63  cmp      qword ptr [rdi + 0x210], rcx
00225C6A  sete     cl
00225C6D  call     0x16d6a0  ; -> 0016D6A0 fn
00225C72  lea      ecx, [rsi + 0x50]
00225C75  call     0x584740  ; -> 00584740 fn
00225C7A  mov      qword ptr [rsp + 0x40], rax
00225C7F  test     rax, rax
00225C82  je       0x225c8f  ; -> 00225C8F
00225C84  mov      rcx, rax
00225C87  call     0x597a20  ; -> 00597A20 fn
00225C8C  mov      rsi, rax
00225C8F  mov      qword ptr [rdi + 0x210], rsi
00225C96  mov      byte ptr [rsi + 0x38], 2
00225C9A  sub      rdi, rbx
00225C9D  nop      dword ptr [rax]
00225CA0  movzx    eax, byte ptr [rbx]
00225CA3  mov      byte ptr [rdi + rbx + 0x10], al
00225CA7  lea      rbx, [rbx + 1]
00225CAB  test     al, al
00225CAD  jne      0x225ca0  ; -> 00225CA0
00225CAF  mov      rbx, qword ptr [rsp + 0x48]
00225CB4  mov      rsi, qword ptr [rsp + 0x50]
00225CB9  add      rsp, 0x30
00225CBD  pop      rdi
00225CBE  ret      
```
