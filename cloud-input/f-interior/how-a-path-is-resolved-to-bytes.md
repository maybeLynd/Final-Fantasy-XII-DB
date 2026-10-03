# F-interior pack: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md`

Generated 2026-10-03 00:36 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/how-a-path-is-resolved-to-bytes.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 001D6B70 (27 B, extent 001D6B70-001D6B8B)

Page context: "pied into the cache** ('0059A9B0' at '0059F1B7'). The copy is armed only on the path     that tried route 1 and missed. There, if '001D6B90()' returns zero or the selector is 5, it is armed when     '001D6B70()' is positive **or the selector is not 1** ('0059EFAB'–'0059EFCE'). Otherwise it is not armed.     - **So selector 1 is the one value that does not fill the cache on a miss** (unless '001D6B70''s flag is set),       which is what "

```
001D6B70  sub      rsp, 0x28
001D6B74  call     0x1dada0  ; -> 001DADA0 fn
001D6B79  xor      ecx, ecx
001D6B7B  cmp      byte ptr [rax + 0x88], cl
001D6B81  setne    cl
001D6B84  mov      eax, ecx
001D6B86  add      rsp, 0x28
001D6B8A  ret      
```

## 001D6D20 (79 B, extent 001D6D20-001D6D6F)

Page context: "hing**; **selector 0 logs '[FFXII_data]'**; **anything else logs '[FFXII_data_notcache]'**.  ## 5. Route 1 - an uppercased key and a 31-bit multiplicative hash  Taken when the resolver's gates pass. '001D6D20' fetches a manager and calls '0020C1B0', which builds a key, hashes it, and searches a tree:  1. **'0020C440' builds the key.** It copies the path, then **skips leading non-alphanumerics** -    the loop advances while the character"

```
001D6D20  mov      qword ptr [rsp + 8], rbx
001D6D25  mov      qword ptr [rsp + 0x10], rbp
001D6D2A  mov      qword ptr [rsp + 0x18], rsi
001D6D2F  push     rdi
001D6D30  sub      rsp, 0x30
001D6D34  mov      rbx, r9
001D6D37  mov      rdi, r8
001D6D3A  mov      esi, edx
001D6D3C  mov      rbp, rcx
001D6D3F  call     0x20c700  ; -> 0020C700 fn
001D6D44  mov      rcx, rax
001D6D47  mov      qword ptr [rsp + 0x20], rbx
001D6D4C  mov      r9, rdi
001D6D4F  mov      r8d, esi
001D6D52  mov      rdx, rbp
001D6D55  call     0x20c1b0  ; -> 0020C1B0 fn
001D6D5A  mov      rbx, qword ptr [rsp + 0x40]
001D6D5F  mov      rbp, qword ptr [rsp + 0x48]
001D6D64  mov      rsi, qword ptr [rsp + 0x50]
001D6D69  add      rsp, 0x30
001D6D6D  pop      rdi
001D6D6E  ret      
```

## 001DB050 (394 B, extent 001DB050-001DB1DA)

Page context: "at bypasses the cache.     - 3–5 are silent and cacheable.   - **The resolver can force 5 itself** ('0059EEF1'). With the cache enabled, it does so when '00865390(path)' is true.     That predicate ('001DB050') matches a path beginning 'PS2Data\obj_finish\in\chara\c10\<name>\' for four names,     'c1004', 'c1005', 'c1006' and 'c1019'. These four character folders are always resolved as selector 5.   - **The two helpers** ('b8' S6):     "

```
001DB050  mov      qword ptr [rsp + 8], rbx
001DB055  mov      qword ptr [rsp + 0x18], rbp
001DB05A  push     rsi
001DB05B  push     rdi
001DB05C  push     r14
001DB05E  sub      rsp, 0x230
001DB065  mov      rax, qword ptr [rip + 0x1d697c4]  ; -> 01F44830 [u64 0x00002B992DDFA232]
001DB06C  xor      rax, rsp
001DB06F  mov      qword ptr [rsp + 0x220], rax
001DB077  mov      rsi, rdx
001DB07A  lea      rdi, [rip + 0x1c21f67]  ; -> 01DFCFE8 [str "c1004"]
001DB081  xor      ebp, ebp
001DB083  lea      r14, [rip + 0x1c21f86]  ; -> 01DFD010 [str "PS2Data\obj_finish\in\chara\c10\"]
001DB08A  nop      word ptr [rax + rax]
001DB090  xor      edx, edx
001DB092  lea      rcx, [rsp + 0x20]
001DB097  mov      r8d, 0x100
001DB09D  call     0x861ec0  ; -> 00861EC0 fn
001DB0A2  xor      ecx, ecx
001DB0A4  nop      dword ptr [rax]
001DB0A8  nop      dword ptr [rax + rax]
001DB0B0  movzx    eax, byte ptr [rcx + r14]
001DB0B5  mov      byte ptr [rsp + rcx + 0x20], al
001DB0B9  lea      rcx, [rcx + 1]
001DB0BD  test     al, al
001DB0BF  jne      0x1db0b0  ; -> 001DB0B0
001DB0C1  lea      rax, [rsp + 0x20]
001DB0C6  dec      rax
001DB0C9  nop      dword ptr [rax]
001DB0D0  cmp      byte ptr [rax + 1], 0
001DB0D4  lea      rax, [rax + 1]
001DB0D8  jne      0x1db0d0  ; -> 001DB0D0
001DB0DA  xor      edx, edx
001DB0DC  nop      dword ptr [rax]
001DB0E0  movzx    ecx, byte ptr [rdi + rdx]
001DB0E4  mov      byte ptr [rax + rdx], cl
001DB0E7  lea      rdx, [rdx + 1]
001DB0EB  test     cl, cl
001DB0ED  jne      0x1db0e0  ; -> 001DB0E0
001DB0EF  lea      rcx, [rsp + 0x20]
001DB0F4  dec      rcx
001DB0F7  nop      word ptr [rax + rax]
001DB100  cmp      byte ptr [rcx + 1], 0
001DB104  lea      rcx, [rcx + 1]
001DB108  jne      0x1db100  ; -> 001DB100
001DB10A  movzx    eax, word ptr [rip + 0x72019f]  ; -> 008FB2B0 [u16 0x005C]
001DB111  or       rbx, 0xffffffffffffffff
001DB115  mov      word ptr [rcx], ax
001DB118  lea      rax, [rsp + 0x20]
001DB11D  nop      dword ptr [rax]
001DB120  inc      rbx
001DB123  cmp      byte ptr [rax + rbx], 0
001DB127  jne      0x1db120  ; -> 001DB120
001DB129  or       rax, 0xffffffffffffffff
001DB12D  nop      dword ptr [rax]
001DB130  inc      rax
001DB133  cmp      byte ptr [rsi + rax], 0
001DB137  jne      0x1db130  ; -> 001DB130
001DB139  cmp      rax, rbx
001DB13C  jbe      0x1db197  ; -> 001DB197
001DB13E  xor      edx, edx
001DB140  lea      rcx, [rsp + 0x120]
001DB148  mov      r8d, 0x100
001DB14E  call     0x861ec0  ; -> 00861EC0 fn
001DB153  mov      r8, rbx
001DB156  lea      rcx, [rsp + 0x120]
001DB15E  mov      rdx, rsi
001DB161  call     qword ptr [rip + 0x6e7e09]  ; -> 008C2F70 [u64 0x0000000001CCEF16]
001DB167  lea      rax, [rsp + 0x20]
001DB16C  lea      r8, [rsp + 0x120]
001DB174  sub      r8, rax
001DB177  nop      word ptr [rax + rax]
001DB180  movzx    edx, byte ptr [rax]
001DB183  movzx    ecx, byte ptr [rax + r8]
001DB188  sub      edx, ecx
001DB18A  jne      0x1db193  ; -> 001DB193
001DB18C  inc      rax
001DB18F  test     ecx, ecx
001DB191  jne      0x1db180  ; -> 001DB180
001DB193  test     edx, edx
001DB195  je       0x1db1d3  ; -> 001DB1D3
001DB197  add      rbp, 6
001DB19B  add      rdi, 6
001DB19F  cmp      rbp, 0x18
001DB1A3  jb       0x1db090  ; -> 001DB090
001DB1A9  xor      eax, eax
001DB1AB  mov      rcx, qword ptr [rsp + 0x220]
001DB1B3  xor      rcx, rsp
001DB1B6  call     0x808c40  ; -> 00808C40 fn
001DB1BB  lea      r11, [rsp + 0x230]
001DB1C3  mov      rbx, qword ptr [r11 + 0x20]
001DB1C7  mov      rbp, qword ptr [r11 + 0x30]
001DB1CB  mov      rsp, r11
001DB1CE  pop      r14
001DB1D0  pop      rdi
001DB1D1  pop      rsi
001DB1D2  ret      
001DB1D3  mov      eax, 1
001DB1D8  jmp      0x1db1ab  ; -> 001DB1AB
```

## 001F47D0 (109 B, extent 001F47D0-001F483D)

Page context: "er. All three resolved from the   import directory. - The sixteen bytes are carried as **two quadwords** and looked up in each mounted package's own   **red-black tree keyed on the 128-bit digest** ('001F47D0' compares '+0x18' then '+0x20'). - **On failure the resolver logs '[FFXII_ERROR] Big file open failed' and returns 10**; success   returns 0.  That error tag is the engine's own word for the archive [the BigFile index page](how-the"

```
001F47D0  mov      r8, qword ptr [rdx]
001F47D3  lea      r10, [rcx + 8]
001F47D7  mov      r9, qword ptr [rdx + 8]
001F47DB  xor      r11d, r11d
001F47DE  mov      rdx, qword ptr [r10 + 0x18]
001F47E2  cmp      rdx, r10
001F47E5  je       0x1f481e  ; -> 001F481E
001F47E7  mov      rax, qword ptr [rdx + 0x18]
001F47EB  cmp      rax, r8
001F47EE  jl       0x1f480c  ; -> 001F480C
001F47F0  jg       0x1f47f8  ; -> 001F47F8
001F47F2  cmp      qword ptr [rdx + 0x20], r9
001F47F6  jl       0x1f480c  ; -> 001F480C
001F47F8  cmp      r8, rax
001F47FB  jl       0x1f4805  ; -> 001F4805
001F47FD  jg       0x1f4821  ; -> 001F4821
001F47FF  cmp      r9, qword ptr [rdx + 0x20]
001F4803  jge      0x1f4821  ; -> 001F4821
001F4805  mov      eax, 1
001F480A  jmp      0x1f4811  ; -> 001F4811
001F480C  mov      eax, 0xffffffff
001F4811  shr      rax, 0x1f
001F4815  mov      rdx, qword ptr [rdx + rax*8]
001F4819  cmp      rdx, r10
001F481C  jne      0x1f47e7  ; -> 001F47E7
001F481E  mov      rdx, r11
001F4821  test     rdx, rdx
001F4824  lea      rax, [rdx + 0x28]
001F4828  cmove    rax, r11
001F482C  test     rax, rax
001F482F  je       0x1f4839  ; -> 001F4839
001F4831  mov      rdx, qword ptr [rax]
001F4834  jmp      0x1f4250  ; -> 001F4250 fn
001F4839  mov      rax, r11
001F483C  ret      
```
