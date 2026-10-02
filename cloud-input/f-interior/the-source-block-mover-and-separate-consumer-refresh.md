# F-interior pack: `02-Resource-And-Asset-Pipeline/the-source-block-mover-and-separate-consumer-refresh.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-source-block-mover-and-separate-consumer-refresh.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 60d2dd1cf	SWE2-FRONTIER: pass 22 - the two Presentation pairs on the Resource pages read and accounted (batch ; e1522398e	SWE2-FRONTIER: pass 22 - 5 more FRONTIER pairs accounted on two Resource pages (batch 4)). OPUS read these before packing.

## 00369C60 (133 B, extent 00369C60-00369CE5)

Page context: "lated text pointers to this owner or claim a safe complete game schedule.  ## 1. Interface and identities  | Operation | Original body | Relevant input/result | |---|---|---| | Explicit compaction | '00369C60' | arena ID and repeat flag; returns completed-move count | | Allocation-pressure retry | '0036BFE0' | current arena/request extent; may move existing allocations before retry | | Equal-size selector | '0036AAD0' | arena and repeat"

```
00369C60  push     rsi
00369C62  sub      rsp, 0x20
00369C66  mov      eax, dword ptr [rip + 0x1f6ed4c]  ; -> 022D89B8
00369C6C  mov      esi, edx
00369C6E  bt       eax, ecx
00369C71  jb       0x369c7b  ; -> 00369C7B
00369C73  xor      eax, eax
00369C75  add      rsp, 0x20
00369C79  pop      rsi
00369C7A  ret      
00369C7B  mov      qword ptr [rsp + 0x30], rbx
00369C80  xor      ebx, ebx
00369C82  mov      qword ptr [rsp + 0x38], rdi
00369C87  cmp      ecx, 0xe
00369C8A  ja       0x369ca2  ; -> 00369CA2
00369C8C  movsxd   rax, ecx
00369C8F  imul     rdi, rax, 0xa8
00369C96  lea      rax, [rip + 0x1f6e333]  ; -> 022D7FD0
00369C9D  add      rdi, rax
00369CA0  jmp      0x369ca5  ; -> 00369CA5
00369CA2  mov      rdi, rbx
00369CA5  cmp      qword ptr [rdi + 0x50], rbx
00369CA9  je       0x369cd3  ; -> 00369CD3
00369CAB  mov      rcx, rdi
00369CAE  call     0x36aad0  ; -> 0036AAD0 fn
00369CB3  mov      ebx, eax
00369CB5  mov      rcx, rdi
00369CB8  call     0x36abe0  ; -> 0036ABE0 fn
00369CBD  test     eax, eax
00369CBF  je       0x369cc7  ; -> 00369CC7
00369CC1  inc      ebx
00369CC3  test     esi, esi
00369CC5  jne      0x369cb5  ; -> 00369CB5
00369CC7  test     ebx, ebx
00369CC9  je       0x369cd3  ; -> 00369CD3
00369CCB  mov      byte ptr [rdi + 2], 1
00369CCF  mov      byte ptr [rdi + 0x62], 1
00369CD3  mov      rdi, qword ptr [rsp + 0x38]
00369CD8  mov      eax, ebx
00369CDA  mov      rbx, qword ptr [rsp + 0x30]
00369CDF  add      rsp, 0x20
00369CE3  pop      rsi
00369CE4  ret      
```

## 00369CF0 (51 B, extent 00369CF0-00369D23)

Page context: "rch selector | '0036ABE0' | arena; at most one selected move per invocation | | Actual mover | '0036A2A0' | arena record, selected free header, selected source header | | Movement latch read/clear | '00369CF0' / '003697C0' | arena ID; reads/clears arena '+0x62' | | Deferred child request | '003E6AA0' | render record and index, stored in five bits | | Bound-container child entry | '003B3C00' | full container ticket and signed index | | E"

```
00369CF0  mov      eax, dword ptr [rip + 0x1f6ecc2]  ; -> 022D89B8
00369CF6  bt       eax, ecx
00369CF9  jb       0x369cfe  ; -> 00369CFE
00369CFB  xor      eax, eax
00369CFD  ret      
00369CFE  cmp      ecx, 0xe
00369D01  ja       0x369d1c  ; -> 00369D1C
00369D03  movsxd   rax, ecx
00369D06  imul     rcx, rax, 0xa8
00369D0D  lea      rax, [rip + 0x1f6e2bc]  ; -> 022D7FD0
00369D14  add      rcx, rax
00369D17  movzx    eax, byte ptr [rcx + 0x62]
00369D1B  ret      
00369D1C  xor      ecx, ecx
00369D1E  movzx    eax, byte ptr [rcx + 0x62]
00369D22  ret      
```

## 003A3A00 (74 B, extent 003A3A00-003A3A4A)

Page context: "nder records are both sides of the separate consumer refresh this page reads. 'MainLoop_Draw' ('0022B0B0') calls the container walk '0024D540', which calls ten render bodies in its walk ('003A3740', '003A3A00' and peers). On the consumer side, 'RenderRecords_ProcessDirtyState' ('00427DE0') is cited here for its skip rule ('record+0x288 == -1'). It calls 52 render bodies and the bound-container child entry '003B3C00', and is called by 'R"

```
003A3A00  mov      r8, qword ptr [rip + 0x2beb901]  ; -> 02F8F308
003A3A07  mov      eax, dword ptr [rip + 0x2beb8b3]  ; -> 02F8F2C0
003A3A0D  cdq      
003A3A0E  mov      qword ptr [rip + 0x2beb8bb], r8  ; -> 02F8F2D0
003A3A15  and      edx, 0xf
003A3A18  add      eax, edx
003A3A1A  sar      eax, 4
003A3A1D  movsxd   rcx, eax
003A3A20  xor      eax, eax
003A3A22  shl      rcx, 4
003A3A26  mov      word ptr [rip + 0x2beb899], ax  ; -> 02F8F2C6
003A3A2D  add      rcx, r8
003A3A30  mov      byte ptr [rip + 0x2beb88f], al  ; -> 02F8F2C5
003A3A36  mov      eax, 0xfffe
003A3A3B  and      word ptr [rip + 0x2beb8ce], ax  ; -> 02F8F310
003A3A42  mov      qword ptr [rip + 0x2beb88f], rcx  ; -> 02F8F2D8
003A3A49  ret      
```
