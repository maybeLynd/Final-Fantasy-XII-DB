# F-interior pack: `17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/gi-render-command-family.json`.

Functions: 12. Each is cited on the page only at its entry and is still in the F frontier.

## 0018AA10 (23 B, extent 0018AA10-0018AA27)

Page context: "call).  ## SWE2-EC7-35 update (2026-09-19) - '0020E6C0'  '0020E6C0' (811 B) is the third sibling beside the '0020E600'/'0020E620' image-pointer pair - the '008C5F80'-'008C5FD0' rdata run, '001EE650'/'0018AA10'/'0016D6A0'/'00808C40'. Interior anchor '0020E6F6' (an '00808C40' call).  ## SWE2-EC7-36 update (2026-09-19) - '00188730'  '00188730' (651 B) is a gi-render CRT-formatter body - '0060D4F0'/'005DC190' septuples, '0016D6A0' quintuple"

```
0018AA10  movzx    eax, r9b
0018AA14  movzx    edx, dl
0018AA17  lea      r9, [rax + rdx*2]
0018AA1B  movsxd   rax, r8d
0018AA1E  lea      rax, [rax + r9*4]
0018AA22  mov      rax, qword ptr [rcx + rax*8]
0018AA26  ret      
```

## 001E5270 (31 B, extent 001E5270-001E528F)

Page context: "lots | frontier | |---|---|---:|---:| | 'RenderObject' | '00906D10' | 2 | 1 (slot 0 '00212C90', scalar-deleting dtor; slot 1 shares a covered body) | | 'MapRenderObject' | '009012C0' | 2 | 1 (slot 1 '001E5270' → '0018B4E0'/'0018AFF0') | | 'CharacterRenderObject' | '00903B68' | 31 | 27 |  'CharacterRenderObject' is the family's real surface: slot 1 '001F89B0' is the same '0018B4E0'/'0018AFF0' event-pair entry as 'MapRenderObject''s; slot"

```
001E5270  push     rbx
001E5272  sub      rsp, 0x20
001E5276  mov      rbx, rcx
001E5279  call     0x18b4e0  ; -> 0018B4E0 fn
001E527E  mov      rdx, qword ptr [rbx + 0x10]
001E5282  mov      rcx, rax
001E5285  add      rsp, 0x20
001E5289  pop      rbx
001E528A  jmp      0x18aff0  ; -> 0018AFF0 fn
```

## 001EE650 (362 B, extent 001EE650-001EE7BA)

Page context: "s (the §12b '(prepare, execute)' contract's first half) | 'ret' folded stub | | 1 | **execute** — the command body proper; every class implements it | e.g. 'DynGeoUIInstance' '00215440' → '001EE7C0'/'001EE650' device pair | | 2 | scalar-deleting destructor — **only on DynGeo classes**; the 16 'Gi*' commands have no slot 2 at all (the §14 no-destructor result, now with the RTTI reason: 'GeometryInstance' declares exactly two virtuals) | "

```
001EE650  mov      qword ptr [rsp + 8], rbx
001EE655  mov      qword ptr [rsp + 0x10], rsi
001EE65A  mov      qword ptr [rsp + 0x18], rdi
001EE65F  mov      edx, ecx
001EE661  lea      rdi, [rip + 0x7140e8]  ; -> 00902750
001EE668  shr      edx, 2
001EE66B  mov      r11d, ecx
001EE66E  and      edx, 3
001EE671  and      r11d, 3
001EE675  mov      r9, rcx
001EE678  mov      esi, 0x10
001EE67D  lea      eax, [r11 + r11*2]
001EE681  add      edx, eax
001EE683  mov      eax, ecx
001EE685  shr      eax, 4
001EE688  and      eax, 3
001EE68B  lea      edx, [rdx + rdx*2]
001EE68E  add      edx, eax
001EE690  mov      eax, ecx
001EE692  mov      rcx, qword ptr [rsp + 0x28]
001EE697  shr      eax, 6
001EE69A  and      eax, 3
001EE69D  lea      ebx, [rdx + rdx*2]
001EE6A0  add      ebx, eax
001EE6A2  lea      rdx, [rcx + 4]
001EE6A6  mov      r10d, ebx
001EE6A9  add      r10, r10
001EE6AC  mov      eax, dword ptr [rdi + r10*8 + 4]
001EE6B1  mov      dword ptr [rcx + 8], eax
001EE6B4  mov      r8d, dword ptr [rdi + r10*8 + 8]
001EE6B9  mov      dword ptr [rcx], r8d
001EE6BC  mov      eax, dword ptr [rdi + r10*8 + 0xc]
001EE6C1  mov      dword ptr [rdx], eax
001EE6C3  cmp      r8d, 6
001EE6C7  jne      0x1ee6d1  ; -> 001EE6D1
001EE6C9  mov      dword ptr [rcx], 0x11
001EE6CF  jmp      0x1ee6f9  ; -> 001EE6F9
001EE6D1  cmp      r8d, 7
001EE6D5  jne      0x1ee6df  ; -> 001EE6DF
001EE6D7  mov      dword ptr [rcx], 0x12
001EE6DD  jmp      0x1ee6f9  ; -> 001EE6F9
001EE6DF  cmp      r8d, 2
001EE6E3  jne      0x1ee6ed  ; -> 001EE6ED
001EE6E5  mov      dword ptr [rcx], 0xf
001EE6EB  jmp      0x1ee6f9  ; -> 001EE6F9
001EE6ED  cmp      r8d, 3
001EE6F1  mov      eax, r8d
001EE6F4  cmove    eax, esi
001EE6F7  mov      dword ptr [rcx], eax
001EE6F9  mov      r8d, dword ptr [rdx]
001EE6FC  cmp      r8d, 6
001EE700  jne      0x1ee70a  ; -> 001EE70A
001EE702  mov      dword ptr [rdx], 0x11
001EE708  jmp      0x1ee732  ; -> 001EE732
001EE70A  cmp      r8d, 7
001EE70E  jne      0x1ee718  ; -> 001EE718
001EE710  mov      dword ptr [rdx], 0x12
001EE716  jmp      0x1ee732  ; -> 001EE732
001EE718  cmp      r8d, 2
001EE71C  jne      0x1ee726  ; -> 001EE726
001EE71E  mov      dword ptr [rdx], 0xf
001EE724  jmp      0x1ee732  ; -> 001EE732
001EE726  cmp      r8d, 3
001EE72A  mov      eax, r8d
001EE72D  cmove    eax, esi
001EE730  mov      dword ptr [rdx], eax
001EE732  cmp      dword ptr [rdi + r10*8], 1
001EE737  jne      0x1ee749  ; -> 001EE749
001EE739  test     r11d, r11d
001EE73C  mov      rax, rcx
001EE73F  cmovne   rax, rdx
001EE743  mov      dword ptr [rax], 1
001EE749  cmp      byte ptr [rsp + 0x30], 0
001EE74E  mov      eax, dword ptr [rdi + r10*8]
001EE752  mov      dword ptr [rcx + 0x1c], eax
001EE755  je       0x1ee767  ; -> 001EE767
001EE757  cmp      ebx, 0xa
001EE75A  mov      r8d, 5
001EE760  cmove    eax, r8d
001EE764  mov      dword ptr [rcx + 0x1c], eax
001EE767  mov      eax, dword ptr [rcx + 0x1c]
001EE76A  xor      r8d, r8d
001EE76D  sub      eax, 3
001EE770  test     eax, 0xfffffffd
001EE775  jne      0x1ee780  ; -> 001EE780
001EE777  mov      dword ptr [rcx], 1
001EE77D  mov      dword ptr [rdx], r8d
001EE780  mov      rbx, qword ptr [rsp + 8]
001EE785  mov      rsi, qword ptr [rsp + 0x10]
001EE78A  mov      rdi, qword ptr [rsp + 0x18]
001EE78F  shr      r9, 0x20
001EE793  movzx    eax, r9b
001EE797  mov      dword ptr [rcx + 0x18], r8d
001EE79B  movd     xmm0, eax
001EE79F  cvtdq2ps xmm0, xmm0
001EE7A2  divss    xmm0, dword ptr [rip + 0x6d7396]  ; -> 008C5B40 [f32 255]
001EE7AA  movss    dword ptr [rcx + 0xc], xmm0
001EE7AF  movss    dword ptr [rcx + 0x10], xmm0
001EE7B4  movss    dword ptr [rcx + 0x14], xmm0
001EE7B9  ret      
```

## 001F3210 (80 B, extent 001F3210-001F3260)

Page context: "iable | | 'GiTransNz' | '00862EC0' | variable | | 'GiNormal' | '008651A0' | variable | | 'GiResetRenderTargetObj' | '001F3260' | **not a reservation** — see §16 | | 'GiResetDefaultRenderTargetObj' | '001F3210' | **not a reservation** — see §16 |  Also: 'GiSetTexture' → 'FUN_00210570'; 'GiPolyGT4T' slot 0 resolves through 'FUN_002D7FA0' / 'FUN_002D7EE0'; shape-C slot 1 calls 'FUN_00609710', 'FUN_00600A60', 'FUN_00188730', 'FUN_005FEFD0'."

```
001F3210  mov      qword ptr [rsp + 8], rbx
001F3215  push     rdi
001F3216  sub      rsp, 0x20
001F321A  mov      rcx, rdx
001F321D  mov      rbx, rdx
001F3220  call     0x609710  ; -> 00609710 fn
001F3225  movzx    edi, al
001F3228  test     al, al
001F322A  je       0x1f3239  ; -> 001F3239
001F322C  mov      edx, 3
001F3231  mov      rcx, rbx
001F3234  call     0x600a60  ; -> 00600A60 fn
001F3239  call     0x189120  ; -> 00189120 fn
001F323E  mov      rcx, rax
001F3241  call     0x188730  ; -> 00188730 fn
001F3246  test     dil, dil
001F3249  je       0x1f3255  ; -> 001F3255
001F324B  xor      edx, edx
001F324D  mov      rcx, rbx
001F3250  call     0x5fefd0  ; -> 005FEFD0 fn
001F3255  mov      rbx, qword ptr [rsp + 0x30]
001F325A  add      rsp, 0x20
001F325E  pop      rdi
001F325F  ret      
```

## 001F3260 (80 B, extent 001F3260-001F32B0)

Page context: "| | 'GiPrim' | '00863D80' | **a field** — variable | | 'GiTrans' | '00862D40' | variable | | 'GiTransNz' | '00862EC0' | variable | | 'GiNormal' | '008651A0' | variable | | 'GiResetRenderTargetObj' | '001F3260' | **not a reservation** — see §16 | | 'GiResetDefaultRenderTargetObj' | '001F3210' | **not a reservation** — see §16 |  Also: 'GiSetTexture' → 'FUN_00210570'; 'GiPolyGT4T' slot 0 resolves through 'FUN_002D7FA0' / 'FUN_002D7EE0'; s"

```
001F3260  mov      qword ptr [rsp + 8], rbx
001F3265  push     rdi
001F3266  sub      rsp, 0x20
001F326A  mov      rcx, rdx
001F326D  mov      rbx, rdx
001F3270  call     0x609710  ; -> 00609710 fn
001F3275  movzx    edi, al
001F3278  test     al, al
001F327A  je       0x1f3289  ; -> 001F3289
001F327C  mov      edx, 3
001F3281  mov      rcx, rbx
001F3284  call     0x600a60  ; -> 00600A60 fn
001F3289  call     0x189120  ; -> 00189120 fn
001F328E  mov      rcx, rax
001F3291  call     0x1893c0  ; -> 001893C0 fn
001F3296  test     dil, dil
001F3299  je       0x1f32a5  ; -> 001F32A5
001F329B  xor      edx, edx
001F329D  mov      rcx, rbx
001F32A0  call     0x5fefd0  ; -> 005FEFD0 fn
001F32A5  mov      rbx, qword ptr [rsp + 0x30]
001F32AA  add      rsp, 0x20
001F32AE  pop      rdi
001F32AF  ret      
```

## 00214830 (45 B, extent 00214830-0021485D)

Page context: "r 'DynGeoFontTextSpecial*' classes share bodies almost entirely — slots 0–5 and 7–9 are identical across all four (execute '00213FE0', '+0xF8'/'+0x100' setters '002146F0'/'002148E0', 'arg[0]' getter '00214830'). The variants differ only at slot 6 (Final '00213B40' vs the others' '00213D10'), slot 10 (four distinct bodies '00214210'/'002142A0'/'002143E0'/'00214540'), slot 11, and partially slot 2.  Per-class × per-slot rows with interior"

```
00214830  mov      eax, dword ptr [rdx]
00214832  mov      dword ptr [rcx + 0x108], eax
00214838  mov      eax, dword ptr [rdx + 4]
0021483B  mov      dword ptr [rcx + 0x10c], eax
00214841  mov      eax, dword ptr [rdx + 8]
00214844  mov      dword ptr [rcx + 0x110], eax
0021484A  mov      eax, dword ptr [rdx + 0xc]
0021484D  mov      dword ptr [rcx + 0x114], eax
00214853  mov      eax, dword ptr [rdx + 0x10]
00214856  mov      dword ptr [rcx + 0x118], eax
0021485C  ret      
```

## 003B0940 (52 B, extent 003B0940-003B0974)

Page context: "002105C0'/'0024D140' plus '01CCFB08'/'01F7F4C0'. Interior anchor '008647D7' (a '0016D6A0' call).  ## SWE2-EC7-62 update (2026-09-19) - '0024D140'  '0024D140' (453 B) is a Gi-render body - '0017FE10'/'003B0940'/'003B33D0'/'00862C40' plus '008F3134'/'01E0C290'/'02092710'/'02F97340'. Interior anchor '0024D155' (a '00862C40' call).    ## SWE2-EC7-63 update (2026-09-19) - '00863060'  '00863060' (146 B) is the 'GiSetTexture' row body - '0016D"

```
003B0940  lea      r9, [rip + 0x2b0e2b9]  ; -> 02EBEC00
003B0947  xor      edx, edx
003B0949  mov      rax, r9
003B094C  lea      r8, [rip + 0x2b0e60d]  ; -> 02EBEF60
003B0953  cmp      dword ptr [rax], ecx
003B0955  je       0x3b0966  ; -> 003B0966
003B0957  inc      edx
003B0959  add      rax, 0x18
003B095D  cmp      rax, r8
003B0960  jl       0x3b0953  ; -> 003B0953
003B0962  or       eax, 0xffffffff
003B0965  ret      
003B0966  movsxd   rax, edx
003B0969  lea      rcx, [rax + rax*2]
003B096D  movzx    eax, byte ptr [r9 + rcx*8 + 0x10]
003B0973  ret      
```

## 003B33D0 (35 B, extent 003B33D0-003B33F3)

Page context: "0024D140' plus '01CCFB08'/'01F7F4C0'. Interior anchor '008647D7' (a '0016D6A0' call).  ## SWE2-EC7-62 update (2026-09-19) - '0024D140'  '0024D140' (453 B) is a Gi-render body - '0017FE10'/'003B0940'/'003B33D0'/'00862C40' plus '008F3134'/'01E0C290'/'02092710'/'02F97340'. Interior anchor '0024D155' (a '00862C40' call).    ## SWE2-EC7-63 update (2026-09-19) - '00863060'  '00863060' (146 B) is the 'GiSetTexture' row body - '0016D6A0'/'001A1"

```
003B33D0  mov      eax, ecx
003B33D2  and      eax, 0x3f
003B33D5  imul     rdx, rax, 0x38
003B33D9  lea      rax, [rip + 0x2b099a0]  ; -> 02EBCD80
003B33E0  add      rdx, rax
003B33E3  mov      eax, dword ptr [rdx]
003B33E5  xor      eax, ecx
003B33E7  test     al, 0x3f
003B33E9  je       0x3b33ef  ; -> 003B33EF
003B33EB  or       eax, 0xffffffff
003B33EE  ret      
003B33EF  mov      eax, dword ptr [rdx + 0x30]
003B33F2  ret      
```

## 00629CB0 (25 B, extent 00629CB0-00629CC9)

Page context: "00608DD0' and '00608F20' run on a changed-lane mask: for each set bit of arg4 (lanes 0-3) it calls '00629970' for the lane and '00629CD0' for the lane plus its bit index, lane 3 additionally running '00629CB0' - the first nonzero return aborts the sweep, 0 means every armed lane validated.  Interior anchor '0060ED16' (function '0060EC80').  '00662EA0' (151 B) is the per-element release the '0x88'-stride array sweeps ('005FDEA0', '005FE0"

```
00629CB0  sub      rsp, 0x28
00629CB4  mov      rcx, qword ptr [rdx + 0x30]
00629CB8  test     rcx, rcx
00629CBB  je       0x629cc2  ; -> 00629CC2
00629CBD  call     0x629e50  ; -> 00629E50 fn
00629CC2  xor      eax, eax
00629CC4  add      rsp, 0x28
00629CC8  ret      
```

## 006C9B00 (27 B, extent 006C9B00-006C9B1B)

Page context: "t, while '+0x80' → 'FUN_0060D760' is 'mov eax, 0x17 ; ret' — a constant-returning query rather than a state change. Scene bracket: '+0x130' → '006CA7B0' (sets flags at '+0x208F0/F3/931'), '+0x128' → '006C9B00'.  > **Still not proven.** Nobody has shown that '[ctx]' at 'FUN_001F4A10' is the same container whose > '+0x18C0' was traced. **That single step is BG-11 and it would close BG-1 properly**, and the > identification is not asserted"

```
006C9B00  push     rbx
006C9B02  sub      rsp, 0x20
006C9B06  mov      rbx, rcx
006C9B09  call     0x6c9b20  ; -> 006C9B20 fn
006C9B0E  mov      rcx, rbx
006C9B11  add      rsp, 0x20
006C9B15  pop      rbx
006C9B16  jmp      0x6c88b0  ; -> 006C88B0 fn
```

## 006CA760 (41 B, extent 006CA760-006CA789)

Page context: "ains inferred from the call site and   the streaming that follows it — exactly as unconfirmed as before.**~~ BG-6. *(Answered 2026-09-26 (FABLE, Claude Opus 5.5):   §20e names the vtable, and slot 0 '006CA760' is read. It overwrites the count register before reading it, and it   returns this '+ 0x10880' (the index cell '+0x18860' is touched only by its own read and reset). So it is a fixed   staging area, not a reservation. See the corr"

```
006CA760  mov      eax, dword ptr [rcx + 0x18860]
006CA766  imul     rdx, rax, 0x7fe0
006CA76D  lea      rax, [rcx + 0x10880]
006CA774  mov      dword ptr [rcx + 0x18860], 0
006CA77E  add      rax, rdx
006CA781  mov      qword ptr [rcx + 0xb8], rax
006CA788  ret      
```

## 006CB540 (69 B, extent 006CB540-006CB585)

Page context: "es.~~       **ANSWERED 2026-09-22 (FABLE), §20e: it holds exactly 45 slots.** The device is       'PrimitiveRendererD3D11', vtable '00D86960' (locator '01D380D0'), 45 entries ending at slot 44       '006CB540'; the highest slot 'Gi*' calls is 39 ('+0x138'), and all twenty recovered offsets       resolve to that class's methods. **BG-2.** - [x] Why the two reset commands alone own a destructor, and what their slot 2 does. **BG-3.**   *An"

```
006CB540  push     rbx
006CB542  sub      rsp, 0x20
006CB546  mov      rax, qword ptr [rcx + 0x848]
006CB54D  mov      rbx, rcx
006CB550  xor      r8d, r8d
006CB553  mov      rcx, qword ptr [rax + 0x110]
006CB55A  mov      edx, dword ptr [rbx + 0xb0]
006CB560  mov      rax, qword ptr [rcx]
006CB563  mov      rdx, qword ptr [rbx + rdx*8 + 0xa8]
006CB56B  call     qword ptr [rax + 0x78]
006CB56E  mov      rax, qword ptr [rbx + 0xc0]
006CB575  mov      dword ptr [rbx + 0xb0], 0
006CB57F  add      rsp, 0x20
006CB583  pop      rbx
006CB584  ret      
```
