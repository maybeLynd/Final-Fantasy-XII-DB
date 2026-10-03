# Homing pack: `16-UI/Shop-Screens/the-shop-screens.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-the-shop-screens.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00243580 (49 B, extent 00243580-002435B1)

Entered from (direct sites whose caller this page cites): `003FCFE0` + 0x4D (call; `003FCFE0` is cited on this page); `003FDDE0` + 0x4D (call; `003FDDE0` is cited on this page)
Other direct sites: `00563560` + 0x2F (call); `005637D0` + 0x2F (call); `005639D0` + 0x2F (call); `00563C00` + 0x29 (call); `00568AA0` + 0x1A (call); `00568BB0` + 0x41 (call)

Host context: "xc1'; 0xf stores word '0x507' at '+0xc0' and byte 3 at '+0xc2'; all these return 0, and any other value tail-jumps to '005C5230(rcx)' | '003C974F', '003C9819', '003C96EC', '003C9611', '003C95F4' | | '003FCFE0' | 494 B | takes 'D' = qword '+8' of '[rdx+0x10]' and 's' = '002DD7E0(0)'; when qword 'rcx+0xe0' is null it calls '00243580(rdx, 0, byte rcx+0x180)', sets bit '0x1' of 'D' dword '+8', calls '002B4090(0x80, 02B5F220, 002F9860(0x867)" / "rcx+0x10]', or returns 0 when 'rcx', that qword or the pointer is null; 0x12 returns 0; any other value tail-jumps to '005C5230(rcx)' | '003FD1E8', '003FD216', '003FD28F', '003FD29D', '003FD2A7' | | '003FDDE0' | 508 B | takes 'D' = qword '+8' of '[rdx+0x10]' and 's' = '002DD7E0(0)'; when qword 'rcx+0xe0' is null it calls '00243580(rdx, 0, byte rcx+0x180)', sets bit '0x1' of 'D' dword '+8', calls '002B4090(0x80, 02B5F220, 002F9860(0x867)"

```
00243580  xor      edx, edx
00243582  mov      r9, rcx
00243585  test     dword ptr [rcx], 0x3fffc
0024358B  jbe      0x2435b0  ; -> 002435B0
0024358D  mov      r8d, edx
00243590  mov      rax, qword ptr [r9 + 0x10]
00243594  lea      r8, [r8 + 8]
00243598  inc      edx
0024359A  mov      rcx, qword ptr [r8 + rax - 8]
0024359F  and      dword ptr [rcx + 8], 0xfffffffe
002435A3  mov      eax, dword ptr [r9]
002435A6  shr      eax, 2
002435A9  movzx    eax, ax
002435AC  cmp      edx, eax
002435AE  jb       0x243590  ; -> 00243590
002435B0  ret      
```

## 0057A960 (22 B, extent 0057A960-0057A976)

Entered from (direct sites whose caller this page cites): `0056DD00` + 0x9 (call; `0056DD00` is cited on this page)
Other direct sites: none

Host context: " of one step | | 10 | '0056E259' | '0056DED0' — directional-input helper | | 12 | '0056E269' | '00293110', '00244F00' (mark-delete), '0056E5D0' | | 14 | '0056E212' | '002470D0' | | 15 | '0056E322' | '0056DD00' gate, then '00247510(self+0x188, 0xF, (self+0x194)>>2 & 1)' ('0056E322'–'0056E355') | | 18 | '0056E374' | '00247510', '003697F0' — deferred free | | 19 | '0056E222' | '0056E5D0' | | 20 | '0056E356' | '0056DD00' gate, then '002CFCF"

```
0057A960  xor      eax, eax
0057A962  cmp      qword ptr [rip + 0x272ee27], rax  ; -> 02CA9790
0057A969  je       0x57a975  ; -> 0057A975
0057A96B  cmp      qword ptr [rip + 0x272ee2e], rax  ; -> 02CA97A0
0057A972  setne    al
0057A975  ret      
```
