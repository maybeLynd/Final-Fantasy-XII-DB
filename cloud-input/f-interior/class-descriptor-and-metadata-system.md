# F-interior pack: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`

Generated 2026-10-02 12:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/class-descriptor-and-metadata-system.json`.

Functions: 18. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 1f52825ce	SWE2-EC7: accounting-state ruling points 2-4 - UC-1 callers visible, declared bodies qualify by pred; 17a959c94	SWE2-EC7: DD re-status A-drift, batch B1 - zlib and JsonBox rows repaired (middleware inventory); th; inbox mentions: ASTRA-QUEUE.md, FABLE.md, SWE2-EC7.md, repos-94.md). OPUS read these before packing.

## 00219C40 (90 B, extent 00219C40-00219C9A)

Page context: "ller set is from 'edges.tsv'; both bodies below are read, not inferred.*  - **Audio — CLIENT.** Eleven edges reach '005CD4F0' from the Audio layer, including '00212050',   '002120E0', '00212300' and '00219C40'. **'005CD4F0' is a nine-byte second-argument rebasing   thunk** — 'lea rdx, [rcx + 0x20]' then 'jmp 005CD450' ('005CD4F0'/'005CD4F4') — so it supplies   the '+0x20' sub-object as the acquire's second argument while 'rcx' stays the"

```
00219C40  mov      qword ptr [rsp + 8], rbx
00219C45  mov      qword ptr [rsp + 0x10], rsi
00219C4A  push     rdi
00219C4B  sub      rsp, 0x20
00219C4F  mov      rsi, rcx
00219C52  mov      rbx, rdx
00219C55  add      rcx, 0xb8
00219C5C  call     0x5cd4f0  ; -> 005CD4F0 fn
00219C61  sub      dword ptr [rbx + 0x58], 1
00219C65  mov      eax, dword ptr [rbx + 0x58]
00219C68  jne      0x219c7f  ; -> 00219C7F
00219C6A  mov      rax, qword ptr [rbx]
00219C6D  mov      rcx, rbx
00219C70  call     qword ptr [rax + 0x10]
00219C73  lea      rcx, [rsi + 0x20]
00219C77  mov      rdx, rbx
00219C7A  call     0x219d80  ; -> 00219D80 fn
00219C7F  lea      rcx, [rsi + 0xb8]
00219C86  mov      rbx, qword ptr [rsp + 0x30]
00219C8B  mov      rsi, qword ptr [rsp + 0x38]
00219C90  add      rsp, 0x20
00219C94  pop      rdi
00219C95  jmp      0x5cd820  ; -> 005CD820 fn
```

## 005A3E50 (79 B, extent 005A3E50-005A3E9F)

Page context: " the 298 restamped tables, what moved:**  - '+0x18' and '+0x38' differ on all 298, and '+0x50' on 296. - '+0x58' differs on 4: exactly the four 'Header' classes. Their destroy slot is member-wise   ('005A3E50': dispatch the descriptor's '+0x78' over the instance), not 'mov al,1; ret'. - '+0x20', '+0x28', '+0x30', '+0x40', '+0x48', '+0x60' and '+0x68' do not move, so every control   below that joins on those slots stands.  The generator "

```
005A3E50  push     rdi
005A3E52  sub      rsp, 0x40
005A3E56  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005A3E5F  mov      qword ptr [rsp + 0x50], rbx
005A3E64  mov      rbx, rdx
005A3E67  mov      rdi, rcx
005A3E6A  call     0x6372b0  ; -> 006372B0 fn
005A3E6F  mov      qword ptr [rsp + 0x30], rax
005A3E74  lea      rax, [rip + 0x789495]  ; -> 00D2D310
005A3E7B  mov      qword ptr [rsp + 0x28], rax
005A3E80  mov      rax, qword ptr [rdi]
005A3E83  lea      r8, [rsp + 0x28]
005A3E88  mov      rdx, rbx
005A3E8B  mov      rcx, rdi
005A3E8E  call     qword ptr [rax + 0x78]
005A3E91  nop      
005A3E92  mov      al, 1
005A3E94  mov      rbx, qword ptr [rsp + 0x50]
005A3E99  add      rsp, 0x40
005A3E9D  pop      rdi
005A3E9E  ret      
```

## 005CB140 (9 B, extent 005CB140-005CB149)

Page context: " by the type's size '+0x38' and calls **type vtable slot 0**         on each.       - **What slot 0 does.** For the scalar type objects it is a byte swap in place:         - 'PUInt32' ('00D311B0') → '005CB140': 'mov eax, [rdx] ; bswap eax ; mov [rdx], eax';         - 'PInt32' → '0063E050': the same by shifts;         - 'double' → '0063E0D0': eight bytes reversed;         - 'bool' → '0061ECF0': 'mov al, 1 ; ret', since one byte has nothi"

```
005CB140  mov      eax, dword ptr [rdx]
005CB142  bswap    eax
005CB144  mov      dword ptr [rdx], eax
005CB146  mov      al, 1
005CB148  ret      
```

## 005CE120 (95 B, extent 005CE120-005CE17F)

Page context: "nothing on disk*, because the offset is past the section's 'SizeOfRawData'. The values above come from the initialiser that writes them, not from the image.  ### What the callers do with it  '''asm ; 005CE120 = Phyre::PClassDescriptorWithoutDefaultConstructor<PMeshInstanceAttachPoint>, vtable slot 10 005CE12A  lea  rcx, [rip + …] ; -> 02E404B0   (the PWorldMatrix descriptor) 005CE134  call 0x63bc00 005CE139  lea  rcx, [rip + …] ; -> 02C"

```
005CE120  mov      qword ptr [rsp + 8], rbx
005CE125  push     rdi
005CE126  sub      rsp, 0x20
005CE12A  lea      rcx, [rip + 0x287237f]  ; -> 02E404B0
005CE131  mov      rbx, rdx
005CE134  call     0x63bc00  ; -> 0063BC00 fn
005CE139  lea      rcx, [rip + 0x26e8d40]  ; -> 02CB6E80
005CE140  mov      rdi, rax
005CE143  call     0x63bc00  ; -> 0063BC00 fn
005CE148  test     rdi, rdi
005CE14B  je       0x5ce172  ; -> 005CE172
005CE14D  test     rax, rax
005CE150  je       0x5ce172  ; -> 005CE172
005CE152  test     rbx, rbx
005CE155  je       0x5ce165  ; -> 005CE165
005CE157  mov      qword ptr [rbx], rdi
005CE15A  mov      qword ptr [rbx + 8], rax
005CE15E  mov      dword ptr [rbx + 0x10], 0
005CE165  mov      al, 1
005CE167  mov      rbx, qword ptr [rsp + 0x30]
005CE16C  add      rsp, 0x20
005CE170  pop      rdi
005CE171  ret      
005CE172  xor      al, al
005CE174  mov      rbx, qword ptr [rsp + 0x30]
005CE179  add      rsp, 0x20
005CE17D  pop      rdi
005CE17E  ret      
```

## 005D18C0 (115 B, extent 005D18C0-005D1933)

Page context: " | | **member-wise** | **4** (new) | the four 'Header' classes: fetch a magic static ('006372B0') and dispatch the descriptor's own '+0x78' over the instance ('005A3E50', 79 B); 'PParameterBuffer''s '005D18C0' then frees '[inst+0x18]' through '005F03A0'. Counted with *bespoke* by the generator, which reports **35** unreduced |  **The control is a cross-tabulation against RTTI, which knows nothing about descriptors.** Whether a class is "

```
005D18C0  push     rdi
005D18C2  sub      rsp, 0x40
005D18C6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005D18CF  mov      qword ptr [rsp + 0x50], rbx
005D18D4  mov      rdi, rdx
005D18D7  mov      rbx, rcx
005D18DA  call     0x6372b0  ; -> 006372B0 fn
005D18DF  mov      qword ptr [rsp + 0x30], rax
005D18E4  lea      rax, [rip + 0x75ba25]  ; -> 00D2D310
005D18EB  mov      qword ptr [rsp + 0x28], rax
005D18F0  mov      rax, qword ptr [rbx]
005D18F3  lea      r8, [rsp + 0x28]
005D18F8  mov      rdx, rdi
005D18FB  mov      rcx, rbx
005D18FE  call     qword ptr [rax + 0x78]
005D1901  nop      
005D1902  mov      edx, dword ptr [rdi + 0x10]
005D1905  mov      eax, edx
005D1907  shr      eax, 0x1f
005D190A  not      al
005D190C  test     al, 1
005D190E  je       0x5d191d  ; -> 005D191D
005D1910  btr      edx, 0x1f
005D1914  mov      rcx, qword ptr [rdi + 0x18]
005D1918  call     0x5f03a0  ; -> 005F03A0 fn
005D191D  xor      eax, eax
005D191F  mov      qword ptr [rdi + 0x18], rax
005D1923  mov      dword ptr [rdi + 0x10], eax
005D1926  mov      al, 1
005D1928  mov      rbx, qword ptr [rsp + 0x50]
005D192D  add      rsp, 0x40
005D1931  pop      rdi
005D1932  ret      
```

## 006132E0 (65 B, extent 006132E0-00613321)

Page context: "l has none.** A form read off the thunk and a fact read off RTTI agree on all 315 — once three classes are held out rather than counted: 'PPhysicsRigidBodyBullet' ('00689FC0'), 'PSamplerStateD3D11' ('006132E0') and 'PScriptableComponent' ('0063FC60') make an indirect call while RTTI records no vtable for them. The first two are bespoke bodies whose indirect call may not be a destructor dispatch at all; **the third shares the standard '-"

```
006132E0  push     rbx
006132E2  sub      rsp, 0x30
006132E6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006132EF  mov      rbx, rdx
006132F2  mov      rcx, qword ptr [rdx + 0x20]
006132F6  test     rcx, rcx
006132F9  je       0x613309  ; -> 00613309
006132FB  mov      rax, qword ptr [rcx]
006132FE  call     qword ptr [rax + 0x10]
00613301  mov      qword ptr [rbx + 0x20], 0
00613309  and      dword ptr [rbx + 0x1c], 0xffffff7f
00613310  mov      rcx, rbx
00613313  call     0x16d6a0  ; -> 0016D6A0 fn
00613318  nop      
00613319  mov      al, 1
0061331B  add      rsp, 0x30
0061331F  pop      rbx
00613320  ret      
```

## 00633240 (93 B, extent 00633240-0063329D)

Page context: "VC static-teardown / destructor-thunk idiom. PROVED BY BYTES, NOT BY THE TAG: all 853 bodies are exactly 12 bytes and mask to ONE distinct byte image. Shape: lea rcx, [<static metadata object>] ; jmp 00633240. THE BOUNDARY: the member installs a constant and tail-calls; it has no logic of its own, and a reconstruction that instantiates the same templates gets these from its own compiler. NOT dispositioned: 00633240, the shared implement"

```
00633240  push     rdi
00633242  sub      rsp, 0x30
00633246  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0063324F  mov      qword ptr [rsp + 0x40], rbx
00633254  mov      rbx, rcx
00633257  lea      rax, [rip + 0x724e52]  ; -> 00D580B0
0063325E  mov      qword ptr [rcx], rax
00633261  lea      rdi, [rcx + 8]
00633265  cmp      qword ptr [rdi], rdi
00633268  je       0x633278  ; -> 00633278
0063326A  mov      rcx, qword ptr [rcx + 0x18]
0063326E  mov      rax, qword ptr [rcx]
00633271  mov      rdx, rbx
00633274  call     qword ptr [rax + 0x48]
00633277  nop      
00633278  lea      rcx, [rbx + 0x38]
0063327C  call     0x6b6700  ; -> 006B6700 fn
00633281  nop      
00633282  test     byte ptr [rdi + 0x20], 1
00633286  je       0x633292  ; -> 00633292
00633288  mov      rcx, qword ptr [rdi + 0x18]
0063328C  call     0x584730  ; -> 00584730 fn
00633291  nop      
00633292  mov      rbx, qword ptr [rsp + 0x40]
00633297  add      rsp, 0x30
0063329B  pop      rdi
0063329C  ret      
```

## 006332A0 (93 B, extent 006332A0-006332FD)

Page context: "VC deleting-destructor idiom over PClassDataMember, sibling of the PClassDescriptorForType family already declared here; 2 byte images collapse to ONE form. CONTROL: three shared targets, each x138 - 006332A0 the base destructor, 00584730 operator delete, and 0016D6A0. THE BOUNDARY: each member is a fixed shape around a varying constant or target, and a reconstruction that writes the same declarations gets it from its own toolchain. NOT"

```
006332A0  push     rdi
006332A2  sub      rsp, 0x30
006332A6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006332AF  mov      qword ptr [rsp + 0x40], rbx
006332B4  mov      rbx, rcx
006332B7  lea      rax, [rip + 0x724df2]  ; -> 00D580B0
006332BE  mov      qword ptr [rcx], rax
006332C1  lea      rdi, [rcx + 8]
006332C5  cmp      qword ptr [rdi], rdi
006332C8  je       0x6332d8  ; -> 006332D8
006332CA  mov      rcx, qword ptr [rcx + 0x18]
006332CE  mov      rax, qword ptr [rcx]
006332D1  mov      rdx, rbx
006332D4  call     qword ptr [rax + 0x48]
006332D7  nop      
006332D8  lea      rcx, [rbx + 0x38]
006332DC  call     0x6b6700  ; -> 006B6700 fn
006332E1  nop      
006332E2  test     byte ptr [rdi + 0x20], 1
006332E6  je       0x6332f2  ; -> 006332F2
006332E8  mov      rcx, qword ptr [rdi + 0x18]
006332EC  call     0x584730  ; -> 00584730 fn
006332F1  nop      
006332F2  mov      rbx, qword ptr [rsp + 0x40]
006332F7  add      rsp, 0x30
006332FB  pop      rdi
006332FC  ret      
```

## 0063E050 (52 B, extent 0063E050-0063E084)

Page context: "    - **What slot 0 does.** For the scalar type objects it is a byte swap in place:         - 'PUInt32' ('00D311B0') → '005CB140': 'mov eax, [rdx] ; bswap eax ; mov [rdx], eax';         - 'PInt32' → '0063E050': the same by shifts;         - 'double' → '0063E0D0': eight bytes reversed;         - 'bool' → '0061ECF0': 'mov al, 1 ; ret', since one byte has nothing to swap.       - **What recursion reaches.** A class-typed field recurses, be"

```
0063E050  mov      ecx, dword ptr [rdx]
0063E052  mov      r8d, ecx
0063E055  and      r8d, 0xff00
0063E05C  mov      eax, ecx
0063E05E  shl      eax, 0x10
0063E061  or       r8d, eax
0063E064  mov      eax, ecx
0063E066  sar      eax, 8
0063E069  and      eax, 0xff00
0063E06E  shl      r8d, 8
0063E072  or       r8d, eax
0063E075  sar      ecx, 0x18
0063E078  movzx    eax, cl
0063E07B  or       r8d, eax
0063E07E  mov      al, 1
0063E080  mov      dword ptr [rdx], r8d
0063E083  ret      
```

## 0063FC60 (31 B, extent 0063FC60-0063FC7F)

Page context: "olumn | | **through the object's own vtable** (~~slot 0~~) | 111 | adjust the pointer (113 of the 114 by '-8'), then 'mov rax,[rcx] ; call [rax + 8k]' - ~~'call [rax]' for all~~ slot 0 for the 87 on '0063FC60', **slot 3** ('call [rax + 0x18]') for the 23 physics shapes on '0068C4E0', **slot 2** for 'PScheduler' on '00680910' (corrected 2026-09-28, OPUS, '_index/candidates/phyre-virtual-destroy-slot/virtual_slot.py') | | **bespoke** | 31"

```
0063FC60  sub      rsp, 0x28
0063FC64  xor      eax, eax
0063FC66  lea      rcx, [rdx - 8]
0063FC6A  test     rdx, rdx
0063FC6D  cmove    rcx, rax
0063FC71  xor      edx, edx
0063FC73  mov      rax, qword ptr [rcx]
0063FC76  call     qword ptr [rax]
0063FC78  mov      al, 1
0063FC7A  add      rsp, 0x28
0063FC7E  ret      
```

## 00657140 (3 B, extent 00657140-00657143)

Page context: " another family, not UC-1. CONTROLS: positive - all 108 already-explained bodies of the same RTTI population (30 A, 78 declared in seven other rows) pass the shape half; negative - the xor al,al stub 00657140 that sits at +0x50 on the abstract classes is refused by the shape; 15 census bodies outside the RTTI population also pass the shape and none is admitted, so the RTTI slot is the discriminator. 123 members, 12-124 B in 67 distinct "

```
00657140  xor      al, al
00657142  ret      
```

## 00660570 (4 B, extent 00660570-00660574)

Page context: "er registrar. **The second control**: followed through its thunk it reproduces 'phyre-field-schema.tsv''s 'caller' column on **173 of 173** covered classes, **0 disagreements** | | '+0x68' | **2** — '00660570' × 314 | shared |  > **WITHDRAWN 2026-09-25 (OPUS) — the two blocks below and the paragraph after them were measured > on the Abstract base table** (see "The table the object carries" above), and their conclusions > do not survive:"

```
00660570  or       eax, 0xffffffff
00660573  ret      
```

## 00674BE0 (93 B, extent 00674BE0-00674C3D)

Page context: "at the zero at '+0x10' counts, and which caller invokes slot 10 (no '[vtable + 0x50]' call site was traced). Fifteen distinct slot-10 bodies among the 38 classes call '0063BC00'. 'PAssetReference''s '00674BE0' first fetches its descriptor from '006372A0'. These are the fifteen RTTI-identified callers of 'DK-1'. The script is ['members/wdc_slot10.py'](members/wdc_slot10.py).  > ### A number that matches, and is not yet a finding > > '006"

```
00674BE0  mov      qword ptr [rsp + 0x10], rdx
00674BE5  push     rdi
00674BE6  sub      rsp, 0x30
00674BEA  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00674BF3  mov      qword ptr [rsp + 0x40], rbx
00674BF8  mov      rbx, rdx
00674BFB  call     0x6372a0  ; -> 006372A0 fn
00674C00  mov      rcx, rax
00674C03  call     0x63bc00  ; -> 0063BC00 fn
00674C08  mov      rdi, rax
00674C0B  test     rax, rax
00674C0E  je       0x674c32  ; -> 00674C32
00674C10  mov      qword ptr [rsp + 0x50], rbx
00674C15  test     rbx, rbx
00674C18  je       0x674c30  ; -> 00674C30
00674C1A  call     0x6372a0  ; -> 006372A0 fn
00674C1F  mov      r9, rax
00674C22  mov      r8, rdi
00674C25  xor      edx, edx
00674C27  mov      rcx, rbx
00674C2A  call     0x6753a0  ; -> 006753A0 fn
00674C2F  nop      
00674C30  mov      al, 1
00674C32  mov      rbx, qword ptr [rsp + 0x40]
00674C37  add      rsp, 0x30
00674C3B  pop      rdi
00674C3C  ret      
```

## 00676F50 (216 B, extent 00676F50-00677028)

Page context: "hor '006B6803' (the '+0x18' compare).  ## SWE2-EC7-119 update (2026-09-21) - the asset-reference registrations measured  '00675DA0' (333 B) is one '005A08E0' registration block: '0063DC90' binds the '00676F50'/'00677470' method pair on '02D3E780', then '00632960' fields '"m_id"' (type 0x10, offset 8) and '"m_targetAssetType"' (0x12, 0) under the '02EAED3C'-indexed TLS counter guard, tailing '00639450'. Interior anchor '00675E4B' (the '""

```
00676F50  mov      qword ptr [rsp + 8], rbx
00676F55  mov      qword ptr [rsp + 0x10], rsi
00676F5A  mov      qword ptr [rsp + 0x18], rdi
00676F5F  push     r14
00676F61  sub      rsp, 0x20
00676F65  mov      rbx, qword ptr [r9 + 8]
00676F69  mov      rsi, r8
00676F6C  mov      r14, rdx
00676F6F  mov      rdi, rcx
00676F72  test     rbx, rbx
00676F75  jne      0x676fe1  ; -> 00676FE1
00676F77  mov      rax, qword ptr [r9]
00676F7A  test     rax, rax
00676F7D  je       0x676fbd  ; -> 00676FBD
00676F7F  mov      edx, dword ptr [rax]
00676F81  xor      ecx, ecx
00676F83  and      edx, 0x7fffffff
00676F89  jbe      0x676fbd  ; -> 00676FBD
00676F8B  lea      r8, [rax + 8]
00676F8F  lea      r10, [rip + 0x26c77ea]  ; -> 02D3E780
00676F96  cmp      edx, 1
00676F99  jbe      0x676fa0  ; -> 00676FA0
00676F9B  mov      rbx, qword ptr [r8]
00676F9E  jmp      0x676fa8  ; -> 00676FA8
00676FA0  xor      ebx, ebx
00676FA2  test     edx, edx
00676FA4  cmovne   rbx, r8
00676FA8  mov      rbx, qword ptr [rbx + rcx*8]
00676FAC  test     rbx, rbx
00676FAF  je       0x676fb7  ; -> 00676FB7
00676FB1  cmp      qword ptr [rbx + 0x50], r10
00676FB5  je       0x676fd8  ; -> 00676FD8
00676FB7  inc      ecx
00676FB9  cmp      ecx, edx
00676FBB  jb       0x676f96  ; -> 00676F96
00676FBD  mov      eax, 7
00676FC2  mov      rbx, qword ptr [rsp + 0x30]
00676FC7  mov      rsi, qword ptr [rsp + 0x38]
00676FCC  mov      rdi, qword ptr [rsp + 0x40]
00676FD1  add      rsp, 0x20
00676FD5  pop      r14
00676FD7  ret      
00676FD8  mov      qword ptr [r9 + 8], rbx
00676FDC  test     rbx, rbx
00676FDF  je       0x676fbd  ; -> 00676FBD
00676FE1  mov      edx, 2
00676FE6  mov      ecx, edx
00676FE8  call     0x17d260  ; -> 0017D260 fn
00676FED  mov      rcx, rax
00676FF0  test     rax, rax
00676FF3  je       0x677024  ; -> 00677024
00676FF5  sub      rdi, qword ptr [rbx + 0x58]
00676FF9  movabs   rax, 0x2aaaaaaaaaaaaaab
00677003  imul     rdi
00677006  sar      rdx, 2
0067700A  mov      rax, rdx
0067700D  shr      rax, 0x3f
00677011  add      rdx, rax
00677014  rol      dx, 8
00677018  mov      word ptr [rcx], dx
0067701B  mov      qword ptr [r14], rcx
0067701E  mov      dword ptr [rsi], 0x80000002
00677024  xor      eax, eax
00677026  jmp      0x676fc2  ; -> 00676FC2
```

## 00677470 (175 B, extent 00677470-0067751F)

Page context: "03' (the '+0x18' compare).  ## SWE2-EC7-119 update (2026-09-21) - the asset-reference registrations measured  '00675DA0' (333 B) is one '005A08E0' registration block: '0063DC90' binds the '00676F50'/'00677470' method pair on '02D3E780', then '00632960' fields '"m_id"' (type 0x10, offset 8) and '"m_targetAssetType"' (0x12, 0) under the '02EAED3C'-indexed TLS counter guard, tailing '00639450'. Interior anchor '00675E4B' (the '"m_id"' '006"

```
00677470  mov      qword ptr [rsp + 8], rbx
00677475  mov      qword ptr [rsp + 0x10], rdi
0067747A  movzx    r11d, word ptr [rdx]
0067747E  mov      r10, r9
00677481  mov      rdx, qword ptr [r9 + 8]
00677485  mov      rbx, rcx
00677488  rol      r11w, 8
0067748D  test     rdx, rdx
00677490  jne      0x6774f6  ; -> 006774F6
00677492  mov      rax, qword ptr [r9]
00677495  test     rax, rax
00677498  je       0x6774dd  ; -> 006774DD
0067749A  mov      r8d, dword ptr [rax]
0067749D  xor      ecx, ecx
0067749F  and      r8d, 0x7fffffff
006774A6  jbe      0x6774dd  ; -> 006774DD
006774A8  lea      r9, [rax + 8]
006774AC  lea      rdi, [rip + 0x26c72cd]  ; -> 02D3E780
006774B3  cmp      r8d, 1
006774B7  jbe      0x6774be  ; -> 006774BE
006774B9  mov      rdx, qword ptr [r9]
006774BC  jmp      0x6774c7  ; -> 006774C7
006774BE  xor      edx, edx
006774C0  test     r8d, r8d
006774C3  cmovne   rdx, r9
006774C7  mov      rdx, qword ptr [rdx + rcx*8]
006774CB  test     rdx, rdx
006774CE  je       0x6774d6  ; -> 006774D6
006774D0  cmp      qword ptr [rdx + 0x50], rdi
006774D4  je       0x6774ed  ; -> 006774ED
006774D6  inc      ecx
006774D8  cmp      ecx, r8d
006774DB  jb       0x6774b3  ; -> 006774B3
006774DD  mov      eax, 7
006774E2  mov      rbx, qword ptr [rsp + 8]
006774E7  mov      rdi, qword ptr [rsp + 0x10]
006774EC  ret      
006774ED  mov      qword ptr [r10 + 8], rdx
006774F1  test     rdx, rdx
006774F4  je       0x6774dd  ; -> 006774DD
006774F6  mov      rdi, qword ptr [rsp + 0x10]
006774FB  movzx    eax, r11w
006774FF  lea      rcx, [rax + rax*2]
00677503  mov      rax, qword ptr [rdx + 0x58]
00677507  lea      rdx, [rax + rcx*8]
0067750B  mov      rax, qword ptr [rax + rcx*8 + 0x10]
00677510  mov      qword ptr [rbx], rax
00677513  xor      eax, eax
00677515  mov      qword ptr [rdx + 0x10], rbx
00677519  mov      rbx, qword ptr [rsp + 8]
0067751E  ret      
```

## 00680910 (32 B, extent 00680910-00680930)

Page context: "'mov rax,[rcx] ; call [rax + 8k]' - ~~'call [rax]' for all~~ slot 0 for the 87 on '0063FC60', **slot 3** ('call [rax + 0x18]') for the 23 physics shapes on '0068C4E0', **slot 2** for 'PScheduler' on '00680910' (corrected 2026-09-28, OPUS, '_index/candidates/phyre-virtual-destroy-slot/virtual_slot.py') | | **bespoke** | 31 | 43 to 102 bytes, not reduced to one of the three | | **member-wise** | **4** (new) | the four 'Header' classes: fe"

```
00680910  sub      rsp, 0x28
00680914  xor      eax, eax
00680916  lea      rcx, [rdx - 8]
0068091A  test     rdx, rdx
0068091D  cmove    rcx, rax
00680921  xor      edx, edx
00680923  mov      rax, qword ptr [rcx]
00680926  call     qword ptr [rax + 0x10]
00680929  mov      al, 1
0068092B  add      rsp, 0x28
0068092F  ret      
```

## 00689FC0 (102 B, extent 00689FC0-0068A026)

Page context: "ass destroyed directly or not at all has none.** A form read off the thunk and a fact read off RTTI agree on all 315 — once three classes are held out rather than counted: 'PPhysicsRigidBodyBullet' ('00689FC0'), 'PSamplerStateD3D11' ('006132E0') and 'PScriptableComponent' ('0063FC60') make an indirect call while RTTI records no vtable for them. The first two are bespoke bodies whose indirect call may not be a destructor dispatch at all;"

```
00689FC0  push     rbx
00689FC2  sub      rsp, 0x30
00689FC6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00689FCF  mov      rbx, rdx
00689FD2  mov      rcx, qword ptr [rdx + 0x118]
00689FD9  test     rcx, rcx
00689FDC  je       0x689fe9  ; -> 00689FE9
00689FDE  mov      rax, qword ptr [rcx]
00689FE1  mov      edx, 1
00689FE6  call     qword ptr [rax + 8]
00689FE9  mov      rcx, qword ptr [rbx + 0x120]
00689FF0  test     rcx, rcx
00689FF3  je       0x689fff  ; -> 00689FFF
00689FF5  mov      rax, qword ptr [rcx]
00689FF8  mov      edx, 1
00689FFD  call     qword ptr [rax]
00689FFF  xor      eax, eax
0068A001  mov      qword ptr [rbx + 0x120], rax
0068A008  mov      qword ptr [rbx + 0x118], rax
0068A00F  mov      qword ptr [rbx + 0xc8], rax
0068A016  mov      rcx, rbx
0068A019  call     0x691d40  ; -> 00691D40 fn
0068A01E  mov      al, 1
0068A020  add      rsp, 0x30
0068A024  pop      rbx
0068A025  ret      
```

## 0068C4E0 (32 B, extent 0068C4E0-0068C500)

Page context: "the pointer (113 of the 114 by '-8'), then 'mov rax,[rcx] ; call [rax + 8k]' - ~~'call [rax]' for all~~ slot 0 for the 87 on '0063FC60', **slot 3** ('call [rax + 0x18]') for the 23 physics shapes on '0068C4E0', **slot 2** for 'PScheduler' on '00680910' (corrected 2026-09-28, OPUS, '_index/candidates/phyre-virtual-destroy-slot/virtual_slot.py') | | **bespoke** | 31 | 43 to 102 bytes, not reduced to one of the three | | **member-wise** | "

```
0068C4E0  sub      rsp, 0x28
0068C4E4  xor      eax, eax
0068C4E6  lea      rcx, [rdx - 8]
0068C4EA  test     rdx, rdx
0068C4ED  cmove    rcx, rax
0068C4F1  xor      edx, edx
0068C4F3  mov      rax, qword ptr [rcx]
0068C4F6  call     qword ptr [rax + 0x18]
0068C4F9  mov      al, 1
0068C4FB  add      rsp, 0x28
0068C4FF  ret      
```
