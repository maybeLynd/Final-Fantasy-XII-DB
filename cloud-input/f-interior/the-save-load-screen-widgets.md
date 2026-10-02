# F-interior pack: `19-Save-Load-Settings/the-save-load-screen-widgets.md`

Generated 2026-10-02 10:27 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-save-load-screen-widgets.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

## 003BB2C0 (38 B, extent 003BB2C0-003BB2E6)

Page context: "s 0; otherwise the card is gone — it closes the popup in states 2, 3, 5, 6, 7, '0xA', '0xC', '0xE' and enters '0xD' with popup 0, *No memory card found*. On retail PC the status is always 0, because '003BB2C0' zeroes the status dword '02B40E18' along with the busy word and the storage machine never runs the command; the only other source is '0017E470''s developer override. **'0xD'** ('00580B40'), save mode ('+0xEA == 0'): status 0 → *sa"

```
003BB2C0  xor      eax, eax
003BB2C2  mov      dword ptr [rip + 0x2785b50], 5  ; -> 02B40E1C
003BB2CC  mov      dword ptr [rip + 0x2785bee], eax  ; -> 02B40EC0
003BB2D2  mov      dword ptr [rip + 0x2785d0c], eax  ; -> 02B40FE4
003BB2D8  mov      qword ptr [rip + 0x2785b35], rax  ; -> 02B40E14
003BB2DF  mov      dword ptr [rip + 0x2785b2b], eax  ; -> 02B40E10
003BB2E5  ret      
```

## 0057E610 (184 B, extent 0057E610-0057E6C8)

Page context: "from the table at 005807B8 for the slot screen and from the cumulative subtract chains for the other six, and every named arm address is where the page puts it; ONE FALSIFIED and corrected in place - 0057E610 answers id 1 with a full construct arm, so "answers no message ids" was wrong   crossref_clean: false   reopened_count: 0 addresses:   - "0057FE80"   - "0057E4D0"   - "0057F360"   - "0057EDB0"   - "0057E8D0"   - "0057EB30"   - "005"

```
0057E610  push     rbx
0057E612  sub      rsp, 0x20
0057E616  cmp      dword ptr [rdx], 1
0057E619  mov      rbx, rcx
0057E61C  je       0x57e628  ; -> 0057E628
0057E61E  add      rsp, 0x20
0057E622  pop      rbx
0057E623  jmp      0x5c5230  ; -> 005C5230 fn
0057E628  mov      rdx, qword ptr [rdx + 8]
0057E62C  mov      r9, rbx
0057E62F  mov      r8d, 7
0057E635  mov      rax, qword ptr [rdx]
0057E638  mov      qword ptr [rcx + 0xc0], rax
0057E63F  movzx    eax, byte ptr [rdx + 8]
0057E643  mov      byte ptr [rcx + 0xc8], al
0057E649  mov      qword ptr [rcx + 0xd0], 0
0057E654  add      rcx, 0x50
0057E658  mov      rdx, qword ptr [rdx + 0x10]
0057E65C  call     0x2432b0  ; -> 002432B0 fn
0057E661  movzx    edx, word ptr [rax + 8]
0057E665  movsx    ecx, word ptr [rax + 6]
0057E669  movzx    r9d, word ptr [rax + 0xa]
0057E66E  movzx    r8d, word ptr [rax + 4]
0057E673  mov      word ptr [rbx + 0x9a], cx
0057E67A  mov      rcx, rbx
0057E67D  mov      word ptr [rbx + 0x9c], dx
0057E684  mov      edx, 0x64
0057E689  mov      word ptr [rbx + 0x98], r8w
0057E691  mov      word ptr [rbx + 0x9e], r9w
0057E699  mov      word ptr [rbx + 0xca], r8w
0057E6A1  call     0x247930  ; -> 00247930 fn
0057E6A6  mov      rcx, qword ptr [rbx + 0xc0]
0057E6AD  mov      rdx, rbx
0057E6B0  call     0x244960  ; -> 00244960 fn
0057E6B5  xor      eax, eax
0057E6B7  mov      qword ptr [rbx + 0xd0], 0
0057E6C2  add      rsp, 0x20
0057E6C6  pop      rbx
0057E6C7  ret      
```

## 0057E950 (238 B, extent 0057E950-0057EA3E)

Page context: "d by | |---:|---|---|---| | 3 | '0057EBB0' (acts only for queue kind 3) | the **card-presence poll**: queue kind 3 → storage command 5 | '0057EC60' — every state that waits on the player | | '0xD' | '0057E950' (queue kinds 4 and 5) | the **device check**: kind 4 → command 4, then in save mode kind 5, the name probe through '003BAC90' | '0057EA40' — state 1 | | '0xF' | '00581B70' | the **save transaction** finished ([how a manual save is"

```
0057E950  push     rbx
0057E952  sub      rsp, 0xe0
0057E959  mov      rax, qword ptr [rip + 0x19c5ed0]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0057E960  xor      rax, rsp
0057E963  mov      qword ptr [rsp + 0xd0], rax
0057E96B  mov      ebx, r8d
0057E96E  sub      ecx, 4
0057E971  je       0x57e997  ; -> 0057E997
0057E973  cmp      ecx, 1
0057E976  jne      0x57ea25  ; -> 0057EA25
0057E97C  mov      rax, qword ptr [rip + 0x272b03d]  ; -> 02CA99C0
0057E983  mov      dword ptr [rsp + 0x80], 0xd
0057E98E  test     rax, rax
0057E991  jne      0x57e9f0  ; -> 0057E9F0
0057E993  mov      al, 0xff
0057E995  jmp      0x57e9f7  ; -> 0057E9F7
0057E997  test     edx, edx
0057E999  jne      0x57e97c  ; -> 0057E97C
0057E99B  test     byte ptr [rbx + 0xc0], 2
0057E9A2  je       0x57e97c  ; -> 0057E97C
0057E9A4  mov      edx, 0x40
0057E9A9  lea      rcx, [rsp + 0x90]
0057E9B1  call     0x393630  ; -> 00393630 fn
0057E9B6  mov      rcx, qword ptr [rip + 0x272b003]  ; -> 02CA99C0
0057E9BD  test     rcx, rcx
0057E9C0  je       0x57ea25  ; -> 0057EA25
0057E9C2  mov      dword ptr [rsp + 0x20], 5
0057E9CA  xor      eax, eax
0057E9CC  nop      dword ptr [rax]
0057E9D0  movzx    edx, byte ptr [rsp + rax + 0x90]
0057E9D8  mov      byte ptr [rsp + rax + 0x28], dl
0057E9DC  lea      rax, [rax + 1]
0057E9E0  test     dl, dl
0057E9E2  jne      0x57e9d0  ; -> 0057E9D0
0057E9E4  lea      rdx, [rsp + 0x20]
0057E9E9  call     0x582540  ; -> 00582540 fn
0057E9EE  jmp      0x57ea25  ; -> 0057EA25
0057E9F0  movzx    eax, byte ptr [rax + 0x39a]
0057E9F7  mov      rcx, qword ptr [rbx + 0xc8]
0057E9FE  lea      r8, [rsp + 0x80]
0057EA06  mov      dword ptr [rsp + 0x88], edx
0057EA0D  mov      edx, 0x1d
0057EA12  mov      byte ptr [rsp + 0x84], al
0057EA19  call     0x247510  ; -> 00247510 fn
0057EA1E  and      dword ptr [rbx + 0xc0], 0xfffffffe
0057EA25  mov      rcx, qword ptr [rsp + 0xd0]
0057EA2D  xor      rcx, rsp
0057EA30  call     0x808c40  ; -> 00808C40 fn
0057EA35  add      rsp, 0xe0
0057EA3C  pop      rbx
0057EA3D  ret      
```

## 0057EDB0 (552 B, extent 0057EDB0-0057EFD8)

Page context: "place - 0057E610 answers id 1 with a full construct arm, so "answers no message ids" was wrong   crossref_clean: false   reopened_count: 0 addresses:   - "0057FE80"   - "0057E4D0"   - "0057F360"   - "0057EDB0"   - "0057E8D0"   - "0057EB30"   - "0057E610" ---  # The save/load screen widgets  **Status:** ~~PARTIAL~~ DOCUMENTED *(corrected 2026-10-02, OPUS: the front matter says 'status: DOCUMENTED', GI-13 answered 2026-09-29)* — the seven"

```
0057EDB0  push     rdi
0057EDB2  sub      rsp, 0x70
0057EDB6  mov      rax, qword ptr [rip + 0x19c5a73]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0057EDBD  xor      rax, rsp
0057EDC0  mov      qword ptr [rsp + 0x50], rax
0057EDC5  mov      rdi, rcx
0057EDC8  mov      ecx, dword ptr [rdx]
0057EDCA  sub      ecx, 1
0057EDCD  je       0x57ee17  ; -> 0057EE17
0057EDCF  sub      ecx, 0xe
0057EDD2  je       0x57edfb  ; -> 0057EDFB
0057EDD4  cmp      ecx, 3
0057EDD7  je       0x57edf4  ; -> 0057EDF4
0057EDD9  mov      rcx, rdi
0057EDDC  call     0x5c5230  ; -> 005C5230 fn
0057EDE1  mov      rcx, qword ptr [rsp + 0x50]
0057EDE6  xor      rcx, rsp
0057EDE9  call     0x808c40  ; -> 00808C40 fn
0057EDEE  add      rsp, 0x70
0057EDF2  pop      rdi
0057EDF3  ret      
0057EDF4  mov      edx, 0x12
0057EDF9  jmp      0x57ee00  ; -> 0057EE00
0057EDFB  mov      edx, 0xf
0057EE00  mov      rcx, qword ptr [rdi + 0xc0]
0057EE07  mov      r8d, 5
0057EE0D  call     0x247510  ; -> 00247510 fn
0057EE12  jmp      0x57efc3  ; -> 0057EFC3
0057EE17  mov      qword ptr [rsp + 0x90], rbx
0057EE1F  lea      rcx, [rdi + 0x50]
0057EE23  mov      qword ptr [rsp + 0x98], rbp
0057EE2B  mov      r9, rdi
0057EE2E  xor      ebp, ebp
0057EE30  mov      qword ptr [rsp + 0x68], rsi
0057EE35  mov      qword ptr [rsp + 0x60], r14
0057EE3A  mov      r14, qword ptr [rdx + 8]
0057EE3E  lea      r8d, [rbp + 2]
0057EE42  mov      rax, qword ptr [r14]
0057EE45  mov      qword ptr [rdi + 0xc0], rax
0057EE4C  mov      qword ptr [rdi + 0x100], rbp
0057EE53  mov      rdx, qword ptr [r14 + 8]
0057EE57  call     0x2432b0  ; -> 002432B0 fn
0057EE5C  movzx    edx, word ptr [rax + 8]
0057EE60  movsx    ecx, word ptr [rax + 6]
0057EE64  movzx    r8d, word ptr [rax + 0xa]
0057EE69  movzx    eax, word ptr [rax + 4]
0057EE6D  mov      word ptr [rdi + 0x9a], cx
0057EE74  mov      rcx, rdi
0057EE77  mov      word ptr [rdi + 0x9c], dx
0057EE7E  xor      edx, edx
0057EE80  mov      word ptr [rdi + 0x98], ax
0057EE87  mov      word ptr [rdi + 0x9e], r8w
0057EE8F  call     0x394700  ; -> 00394700 fn
0057EE94  lea      edx, [rbp + 0x63]
0057EE97  mov      rcx, rdi
0057EE9A  call     0x247930  ; -> 00247930 fn
0057EE9F  mov      rcx, qword ptr [rdi + 0xc0]
0057EEA6  mov      rdx, rdi
0057EEA9  call     0x246ad0  ; -> 00246AD0 fn
0057EEAE  lea      edx, [rbp + 1]
0057EEB1  mov      rcx, rdi
0057EEB4  call     0x394660  ; -> 00394660 fn
0057EEB9  test     rax, rax
0057EEBC  jne      0x57eec2  ; -> 0057EEC2
0057EEBE  mov      ebx, ebp
0057EEC0  jmp      0x57eec9  ; -> 0057EEC9
0057EEC2  mov      rax, qword ptr [rax + 0x60]
0057EEC6  mov      rbx, qword ptr [rax]
0057EEC9  mov      ecx, 0x875
0057EECE  call     0x2f9860  ; -> 002F9860 fn
0057EED3  xor      ecx, ecx
0057EED5  mov      qword ptr [rbx + 0x18], rax
0057EED9  call     0x20e620  ; -> 0020E620 fn
0057EEDE  mov      edx, 2
0057EEE3  mov      dword ptr [rbx + 0x20], eax
0057EEE6  mov      rcx, rdi
0057EEE9  call     0x394660  ; -> 00394660 fn
0057EEEE  mov      rbx, rax
0057EEF1  test     rax, rax
0057EEF4  jne      0x57eefb  ; -> 0057EEFB
0057EEF6  mov      rsi, rbp
0057EEF9  jmp      0x57ef03  ; -> 0057EF03
0057EEFB  mov      rax, qword ptr [rax + 0x60]
0057EEFF  mov      rsi, qword ptr [rax + 8]
0057EF03  mov      ecx, 0x876
0057EF08  call     0x2f9860  ; -> 002F9860 fn
0057EF0D  xor      ecx, ecx
0057EF0F  mov      qword ptr [rsi + 0x18], rax
0057EF13  call     0x20e620  ; -> 0020E620 fn
0057EF18  mov      dword ptr [rsi + 0x20], eax
0057EF1B  test     rbx, rbx
0057EF1E  jne      0x57ef25  ; -> 0057EF25
0057EF20  mov      rbx, rbp
0057EF23  jmp      0x57ef2d  ; -> 0057EF2D
0057EF25  mov      rax, qword ptr [rbx + 0x60]
0057EF29  mov      rbx, qword ptr [rax + 0x18]
0057EF2D  mov      ecx, 0x877
0057EF32  call     0x2f9860  ; -> 002F9860 fn
0057EF37  xor      ecx, ecx
0057EF39  mov      qword ptr [rbx + 0x18], rax
0057EF3D  call     0x20e620  ; -> 0020E620 fn
0057EF42  mov      dword ptr [rbx + 0x20], eax
0057EF45  xor      edx, edx
0057EF47  mov      rcx, rdi
0057EF4A  mov      qword ptr [rdi + 0x100], rbp
0057EF51  call     0x247870  ; -> 00247870 fn
0057EF56  mov      ebx, ebp
0057EF58  lea      rsi, [rdi + 0xc8]
0057EF5F  nop      
0057EF60  lea      rax, [rsp + 0x20]
0057EF65  mov      dword ptr [rsp + 0x38], ebp
0057EF69  mov      qword ptr [rsp + 0x40], rax
0057EF6E  lea      r8, [rsp + 0x38]
0057EF73  mov      rax, qword ptr [r14 + 8]
0057EF77  lea      rdx, [rip - 0x96e]  ; -> 0057E610
0057EF7E  mov      ecx, 0xd8
0057EF83  mov      qword ptr [rsp + 0x30], rax
0057EF88  mov      qword ptr [rsp + 0x48], rbp
0057EF8D  mov      qword ptr [rsp + 0x20], rdi
0057EF92  mov      byte ptr [rsp + 0x28], bl
0057EF96  call     0x244f50  ; -> 00244F50 fn
0057EF9B  inc      ebx
0057EF9D  mov      qword ptr [rsi], rax
0057EFA0  lea      rsi, [rsi + 8]
0057EFA4  cmp      ebx, 7
0057EFA7  jl       0x57ef60  ; -> 0057EF60
0057EFA9  mov      r14, qword ptr [rsp + 0x60]
0057EFAE  mov      rsi, qword ptr [rsp + 0x68]
0057EFB3  mov      rbp, qword ptr [rsp + 0x98]
0057EFBB  mov      rbx, qword ptr [rsp + 0x90]
0057EFC3  xor      eax, eax
0057EFC5  mov      rcx, qword ptr [rsp + 0x50]
0057EFCA  xor      rcx, rsp
0057EFCD  call     0x808c40  ; -> 00808C40 fn
0057EFD2  add      rsp, 0x70
0057EFD6  pop      rdi
0057EFD7  ret      
```

## 005812B0 (85 B, extent 005812B0-00581305)

Page context: "al error | the caller's popup: 0 "No memory card …", 1 "Insufficient disk space. …", 3 "Failed to read memory card …", 4 "Failed to format …", 5 "Save failed.", 6 "Load failed." | closes the screen ('005812B0') | | '0xE' | slot error | the caller's popup: 7 "Corrupt save data. …", 8 "The selected file is in use by another game. …", 9 "Unable to overwrite other game data. …", '0xA' "Unable to load. Save data is corrupted." | '005812B0', "

```
005812B0  push     rbx
005812B2  sub      rsp, 0x20
005812B6  mov      rbx, qword ptr [rip + 0x272870b]  ; -> 02CA99C8
005812BD  test     rbx, rbx
005812C0  je       0x5812ff  ; -> 005812FF
005812C2  mov      rcx, qword ptr [rbx + 0xf0]
005812C9  mov      qword ptr [rsp + 0x30], rdi
005812CE  xor      edi, edi
005812D0  mov      qword ptr [rbx + 0xd4], 0xffff
005812DB  mov      qword ptr [rbx + 0xdc], rdi
005812E2  mov      dword ptr [rbx + 0xc8], edi
005812E8  test     rcx, rcx
005812EB  je       0x5812f4  ; -> 005812F4
005812ED  xor      edx, edx
005812EF  call     0x225580  ; -> 00225580 fn
005812F4  mov      dword ptr [rbx + 0xfc], edi
005812FA  mov      rdi, qword ptr [rsp + 0x30]
005812FF  add      rsp, 0x20
00581303  pop      rbx
00581304  ret      
```
