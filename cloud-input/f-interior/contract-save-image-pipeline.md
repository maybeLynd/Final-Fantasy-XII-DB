# F-interior pack: `19-Save-Load-Settings/CONTRACT-save-image-pipeline.md`

Generated 2026-10-02 10:27 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/contract-save-image-pipeline.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

## 002DF060 (8 B, extent 002DF060-002DF068)

Page context: "ed by the field pass; neither touches a save buffer, so neither bears on SV-1 to SV-6.  **Audio — SERVICE (9 edges).** The teardown body '003601D0' - the only caller of the bare clear (SV-5) - calls '002DF060', '002DF0F0', '002DF370' (the group-mask setter), '00360D70', '00362850', '003633B0', '003636A0', '00363750' and '00363E40'. That body unwinds audio state before it discards the active buffer; the audio calls are part of the teardo"

```
002DF060  or       ecx, 0xffffffff
002DF063  jmp      0x1dbe40  ; -> 001DBE40 fn
```

## 002EF890 (120 B, extent 002EF890-002EF908)

Page context: "ing hold, if anything.~~ — **resolved 2026-09-23   (SWE2-CONTRACT): for the backup buffer the tail is NOT padding** — a live record sits at   '0x22BDD50' ('backup + 0x56690'), accessed by '002EF840'/'002EF890'/'002EF910'/'002EFA70' and   a 'subsd' reader at '001C3227'; it is the head of whatever follows the buffer array by   allocation, not slack. The other three tails ('0x21BA910', '0x2210F90', '0x2267660') have   zero references of an"

```
002EF890  mov      qword ptr [rsp + 8], rbx
002EF895  mov      qword ptr [rsp + 0x10], rbp
002EF89A  mov      qword ptr [rsp + 0x18], rsi
002EF89F  mov      qword ptr [rsp + 0x20], rdi
002EF8A4  push     r14
002EF8A6  sub      rsp, 0x20
002EF8AA  xor      esi, esi
002EF8AC  lea      r14, [rip + 0x1fce4ad]  ; -> 022BDD60
002EF8B3  mov      ebx, esi
002EF8B5  lea      ebp, [rsi + 6]
002EF8B8  test     ebx, ebx
002EF8BA  jns      0x2ef8c0  ; -> 002EF8C0
002EF8BC  mov      eax, esi
002EF8BE  jmp      0x2ef8c7  ; -> 002EF8C7
002EF8C0  cmp      ebx, ebp
002EF8C2  mov      eax, ebx
002EF8C4  cmovg    eax, ebp
002EF8C7  cdqe     
002EF8C9  lea      rdi, [rax + rax*2]
002EF8CD  add      rdi, rdi
002EF8D0  mov      ecx, dword ptr [r14 + rdi*8]
002EF8D4  test     ecx, ecx
002EF8D6  je       0x2ef8e6  ; -> 002EF8E6
002EF8D8  call     0x24cff0  ; -> 0024CFF0 fn
002EF8DD  mov      dword ptr [r14 + rdi*8], esi
002EF8E1  mov      byte ptr [r14 + rdi*8 + 4], sil
002EF8E6  inc      ebx
002EF8E8  cmp      ebx, 7
002EF8EB  jl       0x2ef8b8  ; -> 002EF8B8
002EF8ED  mov      rbx, qword ptr [rsp + 0x30]
002EF8F2  mov      rbp, qword ptr [rsp + 0x38]
002EF8F7  mov      rsi, qword ptr [rsp + 0x40]
002EF8FC  mov      rdi, qword ptr [rsp + 0x48]
002EF901  add      rsp, 0x20
002EF905  pop      r14
002EF907  ret      
```

## 00349B30 (40 B, extent 00349B30-00349B58)

Page context: "Native_Bridge — CLIENT (10 edges).** Script verbs call the table past the backup buffer - '003559B0', '00355EB0', '00356270', '00356650', '00356A50' and '00356FE0' call the entry starter '002EFA70', '00349B30' and '0034A050' call the one-slot release '002EF840', and '00355350' calls the all-slots release '002EF890' - and '0050F540' calls the selector '00236760'. Scripts start and release entries in the seven-slot table §14 found living "

```
00349B30  push     rbx
00349B32  sub      rsp, 0x20
00349B36  mov      rcx, r9
00349B39  call     0x267e10  ; -> 00267E10 fn
00349B3E  lea      rcx, [rip + 0x9c70db]  ; -> 00D10C20
00349B45  mov      ebx, eax
00349B47  call     0x17db70  ; -> 0017DB70 fn
00349B4C  mov      ecx, ebx
00349B4E  add      rsp, 0x20
00349B52  pop      rbx
00349B53  jmp      0x2ef840  ; -> 002EF840 fn
```

## 0034A050 (53 B, extent 0034A050-0034A085)

Page context: " CLIENT (10 edges).** Script verbs call the table past the backup buffer - '003559B0', '00355EB0', '00356270', '00356650', '00356A50' and '00356FE0' call the entry starter '002EFA70', '00349B30' and '0034A050' call the one-slot release '002EF840', and '00355350' calls the all-slots release '002EF890' - and '0050F540' calls the selector '00236760'. Scripts start and release entries in the seven-slot table §14 found living in the backup b"

```
0034A050  push     rbx
0034A052  sub      rsp, 0x20
0034A056  xor      edx, edx
0034A058  mov      rcx, r9
0034A05B  mov      rbx, r9
0034A05E  call     0x267f90  ; -> 00267F90 fn
0034A063  mov      rcx, rbx
0034A066  call     0x267e10  ; -> 00267E10 fn
0034A06B  lea      rcx, [rip + 0x9c6bae]  ; -> 00D10C20
0034A072  mov      ebx, eax
0034A074  call     0x17db70  ; -> 0017DB70 fn
0034A079  mov      ecx, ebx
0034A07B  add      rsp, 0x20
0034A07F  pop      rbx
0034A080  jmp      0x2ef840  ; -> 002EF840 fn
```

## 003633B0 (88 B, extent 003633B0-00363408)

Page context: "6.  **Audio — SERVICE (9 edges).** The teardown body '003601D0' - the only caller of the bare clear (SV-5) - calls '002DF060', '002DF0F0', '002DF370' (the group-mask setter), '00360D70', '00362850', '003633B0', '003636A0', '00363750' and '00363E40'. That body unwinds audio state before it discards the active buffer; the audio calls are part of the teardown, and the contract's claim about it is only which clear it takes.  **CoreRuntimeSc"

```
003633B0  push     rbx
003633B2  sub      rsp, 0x20
003633B6  mov      ebx, ecx
003633B8  test     ecx, ecx
003633BA  je       0x3633d8  ; -> 003633D8
003633BC  movzx    eax, byte ptr [rip + 0x1f6876a]  ; -> 022CBB2D
003633C3  cmp      eax, ecx
003633C5  je       0x3633fc  ; -> 003633FC
003633C7  call     0x363840  ; -> 00363840 fn
003633CC  mov      byte ptr [rip + 0x1f6875b], bl  ; -> 022CBB2D
003633D2  add      rsp, 0x20
003633D6  pop      rbx
003633D7  ret      
003633D8  cmp      dword ptr [rip + 0x1f68691], 0  ; -> 022CBA70
003633DF  mov      edx, dword ptr [rip + 0x1f68697]  ; -> 022CBA7C
003633E5  jne      0x3633eb  ; -> 003633EB
003633E7  test     edx, edx
003633E9  je       0x3633f2  ; -> 003633F2
003633EB  xor      ecx, ecx
003633ED  call     0x2df0f0  ; -> 002DF0F0 fn
003633F2  mov      dword ptr [rip + 0x1f68674], 0  ; -> 022CBA70
003633FC  mov      byte ptr [rip + 0x1f6872b], bl  ; -> 022CBB2D
00363402  add      rsp, 0x20
00363406  pop      rbx
00363407  ret      
```
