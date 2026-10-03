# F-interior pack: `23-Third-Party-Libraries/third-party-middleware-inventory.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/third-party-middleware-inventory.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 001EA380 (64 B, extent 001EA380-001EA3C0)

Page context: "DB0', '00796E20', 'xmm0 = 1.0' ('01CEBBF0', '001D5300'), then fills rows: '001EA990' twice ('001D5366', '001D5423'), '001D0190' ('001D53C2'), 'esi == 9' vs '0xA' kind split ('001D53CB'– '001D53DE'), '001EA380' per row, 'rdi' bounded at '0x16' (22 rows, '001D540C'/'001D54DA'), '001EAEA0', '00808C40' cookie. Row strings include '"tent!!"', '"None content!!"' and a '<Inf…' format run at '008FF950'– '008FF95E' ('001D548E'–'001D54AC').  | me"

```
001EA380  push     rbx
001EA382  sub      rsp, 0x20
001EA386  mov      eax, dword ptr [rcx + 0x28]
001EA389  mov      rbx, rcx
001EA38C  btr      eax, 0x1f
001EA390  cmp      edx, eax
001EA392  jae      0x1ea3b3  ; -> 001EA3B3
001EA394  mov      rax, qword ptr [rcx + 0x30]
001EA398  mov      edx, edx
001EA39A  lea      rcx, [rax + rdx*8]
001EA39E  mov      rdx, r8
001EA3A1  call     0x1ead40  ; -> 001EAD40 fn
001EA3A6  mov      byte ptr [rbx + 0xe8], 1
001EA3AD  add      rsp, 0x20
001EA3B1  pop      rbx
001EA3B2  ret      
001EA3B3  mov      rdx, r8
001EA3B6  add      rsp, 0x20
001EA3BA  pop      rbx
001EA3BB  jmp      0x1ea1e0  ; -> 001EA1E0 fn
```

## 002B3950 (71 B, extent 002B3950-002B3997)

Page context: "vidence. **A shape match, not an   identification.** - **'002A3730'** — a state machine over a large record ('+0x44' masked '0x180000', a byte switch at   '+0x180', writes '+0x3c5', calls '002ABEC0'/'002B3950'). **Nothing in it is XML.**  > **CF-1 answered 2026-09-12 (FABLE): not libxml2 — nothing XML is in the image.** The four tagged > functions ('002A2C00' 1,113 B, '002A3250' 853 B, '002A3730' 220 B, '002B39A0' 34 B) reference **no >"

```
002B3950  and      dword ptr [rcx + 0xb0], 0xfff7ffff
002B395A  xor      eax, eax
002B395C  mov      word ptr [rcx + 0x88], ax
002B3963  mov      byte ptr [rcx + 0xb0], al
002B3969  movzx    eax, word ptr [rcx + 0x8c]
002B3970  mov      word ptr [rcx + 0x8e], ax
002B3977  inc      ax
002B397A  mov      word ptr [rcx + 0x8c], ax
002B3981  mov      word ptr [rcx + 0x90], ax
002B3988  mov      byte ptr [rcx + 0x9b], 1
002B398F  mov      byte ptr [rcx + 0x9d], 1
002B3996  ret      
```

## 00660570 (4 B, extent 00660570-00660574)

Page context: " are basic_streambuf-derived and carry JsonBox-specific bodies only at slot 0 (deleting destructors 001FF930/001FF870/001FF8D0) and slot 3 (the write overrides 002016F0/00201690/002016C0) - slot 6 is 00660570, ICF-folded across hundreds of Phyre descriptor vtables, and is NOT a member - plus the upstream Value.cpp error-literal pool 00904FE8-00905038 ('Expected '\"', got '', 'Expected a digit, '.', 'e' or 'E', got '') referenced only by"

```
00660570  or       eax, 0xffffffff
00660573  ret      
```

## 00887630 (459 B, extent 00887630-008877FB)

Page context: "00880BF0, each hop verified from edges.tsv, and 0067A480 is the movie player FR-1 names), not FFXII code: every census entry from 008800C0 up to 008958B0 (exclusive) less three A-measured entries and 00887630, which nothing references and no fingerprint identifies (18-Audio/members/select_audio_libraries.py). Identified by the 8-field codec registry at 01CEB070-01CEB190 whose three residue bundles share unpack / look / free_info / free_"

```
00887630  mov      qword ptr [rsp + 8], rbx
00887635  mov      qword ptr [rsp + 0x10], rbp
0088763A  mov      qword ptr [rsp + 0x18], rsi
0088763F  mov      qword ptr [rsp + 0x20], rdi
00887644  movsxd   rsi, dword ptr [rsp + 0x30]
00887649  movaps   xmm0, xmm2
0088764C  addss    xmm0, dword ptr [rsp + 0x38]
00887652  xorps    xmm1, xmm1
00887655  movaps   xmm4, xmm2
00887658  xor      r8d, r8d
0088765B  mov      r10, rcx
0088765E  cvtss2sd xmm1, xmm0
00887662  movd     xmm0, esi
00887666  subsd    xmm1, qword ptr [rip + 0x14645da]  ; -> 01CEBC48 [f64 30]
0088766E  cvtdq2ps xmm0, xmm0
00887671  mulsd    xmm1, qword ptr [rip + 0x1464537]  ; -> 01CEBBB0 [f64 0.1000000015]
00887679  cvttsd2si eax, xmm1
0088767D  movd     xmm1, r9d
00887682  test     eax, eax
00887684  cvtdq2ps xmm1, xmm1
00887687  cmovg    r8d, eax
0088768B  mov      eax, 7
00887690  cmp      r8d, eax
00887693  cmovl    eax, r8d
00887697  cdqe     
00887699  mov      rbp, qword ptr [rdx + rax*8]
0088769D  mov      eax, esi
0088769F  sar      eax, 1
008876A1  movss    xmm3, dword ptr [rbp]
008876A6  movaps   xmm2, xmm3
008876A9  subss    xmm2, dword ptr [rip + 0x14645d3]  ; -> 01CEBC84 [f32 16]
008876B1  mulss    xmm2, xmm0
008876B5  movd     xmm0, eax
008876B9  cvttss2si eax, xmm3
008876BD  cvtdq2ps xmm0, xmm0
008876C0  movsxd   rdx, eax
008876C3  addss    xmm2, xmm1
008876C7  cvttss2si eax, dword ptr [rbp + 4]
008876CC  subss    xmm2, xmm0
008876D0  movsxd   rbx, eax
008876D3  cvttss2si edi, xmm2
008876D7  cmp      rdx, rbx
008876DA  jge      0x8877e6  ; -> 008877E6
008876E0  mov      rax, rbx
008876E3  sub      rax, rdx
008876E6  cmp      rax, 4
008876EA  jl       0x8877ae  ; -> 008877AE
008876F0  movsxd   r11, dword ptr [rsp + 0x28]
008876F5  lea      r8, [rdx*4 + 0x10]
008876FD  add      r8, rbp
00887700  movsxd   rcx, edi
00887703  test     rcx, rcx
00887706  jle      0x88771e  ; -> 0088771E
00887708  movaps   xmm0, xmm4
0088770B  addss    xmm0, dword ptr [r8 - 8]
00887711  comiss   xmm0, dword ptr [r10 + rcx*4]
00887716  jbe      0x88771e  ; -> 0088771E
00887718  movss    dword ptr [r10 + rcx*4], xmm0
0088771E  add      rcx, rsi
00887721  cmp      rcx, r11
00887724  jge      0x8877e6  ; -> 008877E6
0088772A  test     rcx, rcx
0088772D  jle      0x887745  ; -> 00887745
0088772F  movaps   xmm0, xmm4
00887732  addss    xmm0, dword ptr [r8 - 4]
00887738  comiss   xmm0, dword ptr [r10 + rcx*4]
0088773D  jbe      0x887745  ; -> 00887745
0088773F  movss    dword ptr [r10 + rcx*4], xmm0
00887745  add      rcx, rsi
00887748  cmp      rcx, r11
0088774B  jge      0x8877e6  ; -> 008877E6
00887751  test     rcx, rcx
00887754  jle      0x88776b  ; -> 0088776B
00887756  movaps   xmm0, xmm4
00887759  addss    xmm0, dword ptr [r8]
0088775E  comiss   xmm0, dword ptr [r10 + rcx*4]
00887763  jbe      0x88776b  ; -> 0088776B
00887765  movss    dword ptr [r10 + rcx*4], xmm0
0088776B  add      rcx, rsi
0088776E  cmp      rcx, r11
00887771  jge      0x8877e6  ; -> 008877E6
00887773  test     rcx, rcx
00887776  jle      0x88778e  ; -> 0088778E
00887778  movaps   xmm0, xmm4
0088777B  addss    xmm0, dword ptr [r8 + 4]
00887781  comiss   xmm0, dword ptr [r10 + rcx*4]
00887786  jbe      0x88778e  ; -> 0088778E
00887788  movss    dword ptr [r10 + rcx*4], xmm0
0088778E  add      rcx, rsi
00887791  lea      edi, [rdi + rsi*4]
00887794  cmp      rcx, r11
00887797  jge      0x8877e6  ; -> 008877E6
00887799  add      rdx, 4
0088779D  lea      rax, [rbx - 3]
008877A1  add      r8, 0x10
008877A5  cmp      rdx, rax
008877A8  jl       0x887703  ; -> 00887703
008877AE  cmp      rdx, rbx
008877B1  jge      0x8877e6  ; -> 008877E6
008877B3  movsxd   r8, dword ptr [rsp + 0x28]
008877B8  movsxd   rax, edi
008877BB  test     rax, rax
008877BE  jle      0x8877d6  ; -> 008877D6
008877C0  movaps   xmm0, xmm4
008877C3  addss    xmm0, dword ptr [rbp + rdx*4 + 8]
008877C9  comiss   xmm0, dword ptr [r10 + rax*4]
008877CE  jbe      0x8877d6  ; -> 008877D6
008877D0  movss    dword ptr [r10 + rax*4], xmm0
008877D6  add      rax, rsi
008877D9  cmp      rax, r8
008877DC  jge      0x8877e6  ; -> 008877E6
008877DE  inc      rdx
008877E1  cmp      rdx, rbx
008877E4  jl       0x8877bb  ; -> 008877BB
008877E6  mov      rbx, qword ptr [rsp + 8]
008877EB  mov      rbp, qword ptr [rsp + 0x10]
008877F0  mov      rsi, qword ptr [rsp + 0x18]
008877F5  mov      rdi, qword ptr [rsp + 0x20]
008877FA  ret      
```
