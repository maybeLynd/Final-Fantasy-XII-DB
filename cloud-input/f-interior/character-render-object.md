# F-interior pack: `17-Presentation-Rendering/Character-Rendering/character-render-object.md`

Generated 2026-10-02 18:33 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/character-render-object.json`.

Functions: 6. Each is cited on the page only at its entry and is still in the F frontier.

## 001890A0 (97 B, extent 001890A0-00189101)

Page context: "chor '006337E1' (the 'vtable[+0x38]' call).  ## SWE2-EC7-122 update (2026-09-21) - '00628570' measured  '00628570' (77 B) is the '+0x9C0' sub-object's variant of the '006285C0' parameter-write idiom '001890A0', '001F5C20' and '00607410' call: '+0x9EC = 1'; '+0x9F4' takes '0061C010(r8d)' when 'dl' holds, else 8; '[+0x9C0] |= 4'. Interior anchor '0062858A' (the '0061C010' call).  ## SWE2-EC7-124 update (2026-09-21) - '0060DEA0' measured  "

```
001890A0  mov      qword ptr [rsp + 8], rbx
001890A5  push     rdi
001890A6  sub      rsp, 0x40
001890AA  mov      rdi, qword ptr [rcx]
001890AD  xor      edx, edx
001890AF  mov      rbx, qword ptr [rcx + 0x10]
001890B3  mov      rcx, rdi
001890B6  lea      r8d, [rdx + 1]
001890BA  call     0x628570  ; -> 00628570 fn
001890BF  xor      eax, eax
001890C1  lea      r9, [rbx + 0x40]
001890C5  mov      qword ptr [rsp + 0x30], rax
001890CA  mov      r8, rbx
001890CD  mov      dword ptr [rsp + 0x28], 4
001890D5  mov      rcx, rdi
001890D8  mov      qword ptr [rsp + 0x20], rax
001890DD  lea      edx, [rax + 1]
001890E0  call     0x6215a0  ; -> 006215A0 fn
001890E5  mov      r8d, 1
001890EB  mov      rcx, rdi
001890EE  movzx    edx, r8b
001890F2  mov      rbx, qword ptr [rsp + 0x50]
001890F7  add      rsp, 0x40
001890FB  pop      rdi
001890FC  jmp      0x628570  ; -> 00628570 fn
```

## 001AD470 (20 B, extent 001AD470-001AD484)

Page context: "WE2-EC7-53 update (2026-09-19) - '001ABF50'  '001ABF50' (1084 B) is the character-render record op the page names ('+0x3C0'/'+0x3D0' at 16-byte stride) - '00861F14' pair, '001AB0F0', '001AA3D0' plus '001AD470' text target. Interior anchor '001AC08C' (a '00861F14' call).  ## SWE2-EC7-54 update (2026-09-19) - '001AB0F0'  '001AB0F0' (462 B) is a character-render record helper - '001EDF00' single call plus three vcalls, '008C2A40' import. I"

```
001AD470  mov      rax, qword ptr [rdx]
001AD473  mov      r8, qword ptr [rcx]
001AD476  movss    xmm0, dword ptr [rax + 0x34]
001AD47B  comiss   xmm0, dword ptr [r8 + 0x34]
001AD480  setbe    al
001AD483  ret      
```

## 001BD840 (244 B, extent 001BD840-001BD934)

Page context: "ty.         - On a **miss** it constructs a new object and runs slot 2 with the id and entry.         - Either way the object is appended to the pool's active vector and returned.       - **Release ('001BD840').** It finds the object in the active vector and keys it by         '[[object + 0x488] + 0x2A0]'. It appends '{object, 3}' to that key's list in the tree, creating the node         if needed, and removes the object from the vector"

```
001BD840  mov      qword ptr [rsp + 0x18], rbx
001BD845  push     rsi
001BD846  push     rdi
001BD847  push     r14
001BD849  sub      rsp, 0x30
001BD84D  mov      rsi, rcx
001BD850  xor      r14d, r14d
001BD853  mov      rcx, qword ptr [rcx]
001BD856  mov      ebx, r14d
001BD859  mov      rdi, qword ptr [rsi + 8]
001BD85D  sub      rdi, rcx
001BD860  sar      rdi, 3
001BD864  test     edi, edi
001BD866  je       0x1bd907  ; -> 001BD907
001BD86C  nop      dword ptr [rax]
001BD870  mov      eax, ebx
001BD872  cmp      qword ptr [rcx + rax*8], rdx
001BD876  je       0x1bd883  ; -> 001BD883
001BD878  inc      ebx
001BD87A  cmp      ebx, edi
001BD87C  jb       0x1bd870  ; -> 001BD870
001BD87E  jmp      0x1bd907  ; -> 001BD907
001BD883  mov      rcx, rdx
001BD886  mov      qword ptr [rsp + 0x58], rbp
001BD88B  mov      qword ptr [rsp + 0x20], rdx
001BD890  mov      dword ptr [rsp + 0x28], 3
001BD898  call     0x1f6e60  ; -> 001F6E60 fn
001BD89D  lea      rcx, [rsi + 0x20]
001BD8A1  mov      qword ptr [rsp + 0x50], rax
001BD8A6  lea      rdx, [rsp + 0x50]
001BD8AB  call     0x1bce30  ; -> 001BCE30 fn
001BD8B0  mov      r9, qword ptr [rax + 0x10]
001BD8B4  xor      r8d, r8d
001BD8B7  mov      rbp, rax
001BD8BA  lea      rcx, [rax + 0x10]
001BD8BE  lea      edx, [r8 + 0x20]
001BD8C2  call     qword ptr [r9 + 0x10]
001BD8C6  mov      rdx, rax
001BD8C9  add      rax, 0x10
001BD8CD  je       0x1bd8d7  ; -> 001BD8D7
001BD8CF  movups   xmm0, xmmword ptr [rsp + 0x20]
001BD8D4  movups   xmmword ptr [rax], xmm0
001BD8D7  mov      qword ptr [rdx], rbp
001BD8DA  mov      rcx, qword ptr [rbp + 8]
001BD8DE  mov      qword ptr [rdx + 8], rcx
001BD8E2  mov      rax, qword ptr [rbp + 8]
001BD8E6  mov      qword ptr [rax], rdx
001BD8E9  lea      eax, [rdi - 1]
001BD8EC  mov      qword ptr [rbp + 8], rdx
001BD8F0  mov      r8, qword ptr [rsi]
001BD8F3  mov      rbp, qword ptr [rsp + 0x58]
001BD8F8  mov      edx, ebx
001BD8FA  mov      rax, qword ptr [r8 + rax*8]
001BD8FE  mov      qword ptr [r8 + rdx*8], rax
001BD902  add      qword ptr [rsi + 8], -8
001BD907  mov      rax, qword ptr [rsi + 8]
001BD90B  lea      rdx, [rip + 0x73bc0e]  ; -> 008F9520 [str "Can't find character object when try to remove it!"]
001BD912  sub      rax, qword ptr [rsi]
001BD915  sar      rax, 3
001BD919  cmp      eax, edi
001BD91B  setne    r14b
001BD91F  mov      ecx, r14d
001BD922  mov      rbx, qword ptr [rsp + 0x60]
001BD927  add      rsp, 0x30
001BD92B  pop      r14
001BD92D  pop      rdi
001BD92E  pop      rsi
001BD92F  jmp      0x16d6a0  ; -> 0016D6A0 fn
```

## 001E6E70 (220 B, extent 001E6E70-001E6F4C)

Page context: "1) - '0060DEA0' measured  '0060DEA0' (8 B) is the two-field setter '001EE1D0' calls: '+0 = rdx', '+8 = r8', return. Interior anchor '0060DEA3' (the '+8' store).  '001EF060' (315 B) is the matrix arm '001E6E70'/'001FB080' call: when 'rdx' nonnull it reads the nine floats at 'rdx+0'..'+0x34' (rows 0-2 plus '+0x10','+0x14','+0x20','+0x24','+0x30','+0x38') into xmm2-xmm11, XORs each against the '0x80000000' sign mask ('01CEBDA0'), and write"

```
001E6E70  mov      qword ptr [rsp + 8], rbx
001E6E75  mov      qword ptr [rsp + 0x10], rbp
001E6E7A  mov      qword ptr [rsp + 0x18], rsi
001E6E7F  push     rdi
001E6E80  sub      rsp, 0x30
001E6E84  xor      eax, eax
001E6E86  mov      rsi, rdx
001E6E89  mov      qword ptr [rsp + 0x20], rax
001E6E8E  mov      dword ptr [rsp + 0x28], eax
001E6E92  test     rdx, rdx
001E6E95  je       0x1e6ea8  ; -> 001E6EA8
001E6E97  movss    xmm0, dword ptr [rdx + 0x30]
001E6E9C  movss    xmm1, dword ptr [rdx + 0x34]
001E6EA1  movss    xmm2, dword ptr [rdx + 0x38]
001E6EA6  jmp      0x1e6eba  ; -> 001E6EBA
001E6EA8  movss    xmm2, dword ptr [rsp + 0x28]
001E6EAE  movss    xmm1, dword ptr [rsp + 0x24]
001E6EB4  movss    xmm0, dword ptr [rsp + 0x20]
001E6EBA  ucomiss  xmm0, dword ptr [rcx + 0x244]
001E6EC1  jp       0x1e6edb  ; -> 001E6EDB
001E6EC3  jne      0x1e6edb  ; -> 001E6EDB
001E6EC5  ucomiss  xmm1, dword ptr [rcx + 0x248]
001E6ECC  jp       0x1e6edb  ; -> 001E6EDB
001E6ECE  jne      0x1e6edb  ; -> 001E6EDB
001E6ED0  ucomiss  xmm2, dword ptr [rcx + 0x24c]
001E6ED7  jp       0x1e6edb  ; -> 001E6EDB
001E6ED9  je       0x1e6efa  ; -> 001E6EFA
001E6EDB  movss    dword ptr [rcx + 0x244], xmm0
001E6EE3  movss    dword ptr [rcx + 0x248], xmm1
001E6EEB  movss    dword ptr [rcx + 0x24c], xmm2
001E6EF3  mov      byte ptr [rcx + 0x240], 1
001E6EFA  mov      rbx, qword ptr [rcx + 0x18]
001E6EFE  xor      edi, edi
001E6F00  mov      rbp, qword ptr [rcx + 0x20]
001E6F04  sub      rbp, rbx
001E6F07  add      rbp, 7
001E6F0B  shr      rbp, 3
001E6F0F  cmp      rbx, qword ptr [rcx + 0x20]
001E6F13  cmova    rbp, rdi
001E6F17  test     rbp, rbp
001E6F1A  je       0x1e6f37  ; -> 001E6F37
001E6F1C  nop      dword ptr [rax]
001E6F20  mov      rcx, qword ptr [rbx]
001E6F23  mov      rdx, rsi
001E6F26  call     0x1ef060  ; -> 001EF060 fn
001E6F2B  inc      rdi
001E6F2E  lea      rbx, [rbx + 8]
001E6F32  cmp      rdi, rbp
001E6F35  jne      0x1e6f20  ; -> 001E6F20
001E6F37  mov      rbx, qword ptr [rsp + 0x40]
001E6F3C  mov      rbp, qword ptr [rsp + 0x48]
001E6F41  mov      rsi, qword ptr [rsp + 0x50]
001E6F46  add      rsp, 0x30
001E6F4A  pop      rdi
001E6F4B  ret      
```

## 001F4C00 (80 B, extent 001F4C00-001F4C50)

Page context: "nt rather than a silence.  ## SWE2-EC7-34 update (2026-09-19) - '001F57E0'  '001F57E0' (928 B) is the render-object init - '0x2AAAAAAAAAAAAAAB' divide-by-six magic, a '[rbx+rbx*2]*8' 24-byte stride, '001F4C00'/'00215310'/'001F5B61'/'001F5A24'. Interior anchor '001F58A6' (an '001F4C00' call).  ## SWE2-EC7-35 update (2026-09-19) - '001F5330'  '001F5330' (698 B) is a hash-keyed lookup - the '0xa57eb50295fad40b' hash constant, '001F4B30'/'0"

```
001F4C00  cmp      rcx, rdx
001F4C03  je       0x1f4c4c  ; -> 001F4C4C
001F4C05  mov      r9, r8
001F4C08  lea      rax, [rcx + 0x10]
001F4C0C  sub      r9, rcx
001F4C0F  lea      r10, [rip + 0x70c4a2]  ; -> 009010B8
001F4C16  lea      r11, [rip + 0x70ed23]  ; -> 00903940
001F4C1D  nop      dword ptr [rax]
001F4C20  test     r8, r8
001F4C23  je       0x1f4c3b  ; -> 001F4C3B
001F4C25  mov      qword ptr [r8], r10
001F4C28  mov      rcx, qword ptr [rax - 8]
001F4C2C  mov      qword ptr [r9 + rax - 8], rcx
001F4C31  movzx    ecx, byte ptr [rax]
001F4C34  mov      byte ptr [r9 + rax], cl
001F4C38  mov      qword ptr [r8], r11
001F4C3B  add      rax, 0x18
001F4C3F  add      r8, 0x18
001F4C43  lea      rcx, [rax - 0x10]
001F4C47  cmp      rcx, rdx
001F4C4A  jne      0x1f4c20  ; -> 001F4C20
001F4C4C  mov      rax, r8
001F4C4F  ret      
```

## 001F6E60 (15 B, extent 001F6E60-001F6E6F)

Page context: "not vtable slots.** 'functions.tsv' lists 47 entries there and         30 are slots. The seventeen are '001F5330' '001F55F0' '001F57E0' '001F5B80' '001F5C20'         '001F5D70' '001F68E0' '001F6E00' '001F6E60' '001F7790' '001F86F0' '001F87B0' '001F8860'         **'001F89E0'** '001F8A70' '001F8B30' '001FAD50' - so the two this row guessed at,         '001F5D70' and '001FAD50', are both in.       - **The caller census splits them three wa"

```
001F6E60  mov      rax, qword ptr [rcx + 0x488]
001F6E67  mov      rax, qword ptr [rax + 0x2a0]
001F6E6E  ret      
```
