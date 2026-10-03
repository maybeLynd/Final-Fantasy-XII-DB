# Homing pack: `19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-game-settings-ini-and-runtime-config.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00158F60 (124 B, extent 00158F60-00158FDC)

Entered from (direct sites whose caller this page cites): `00159340` + 0x66 (call; `00159340` is cited on this page)
Other direct sites: `00158FE0` + 0x1A (call); `001590B0` + 0x1A (call); `00159180` + 0x2B (call); `00159270` + 0x21 (call)

Host context: "ed  '006253D0' (1,106 B) is the display-adapter enumeration the settings callers drive: the '01F44830' config flag gates the early arm; '008C2A90'/'008C29A0' (CRT entries) and '0065E5D0'/'0065E580'/ '00159340' run the setup; '005CDAA0' formats against the '00D553A0' 'NvAPI_*'/'00D553C8'/'00D553F8' strings with '0080F2CE'/'0080F2C2' environment reads; the record's '+0x38'/'+0x10' virtuals enumerate adapters, '02CF2544'/'02CF2540'/'02CED8"

```
00158F60  mov      qword ptr [rsp + 8], rbx
00158F65  mov      qword ptr [rsp + 0x10], rbp
00158F6A  mov      qword ptr [rsp + 0x18], rsi
00158F6F  push     rdi
00158F70  sub      rsp, 0x20
00158F74  lea      rbp, [rip - 0x38f7b]  ; -> 00120000 (image base)
00158F7B  movsxd   rsi, ecx
00158F7E  xor      ebx, ebx
00158F80  cmp      byte ptr [rsi + rbp + 0x2d8e120], bl
00158F87  je       0x158fac  ; -> 00158FAC
00158F89  nop      dword ptr [rax]
00158F90  mov      ecx, 0x64
00158F95  call     qword ptr [rip + 0x769215]  ; -> 008C21B0 [u64 0x0000000001CCC316]
00158F9B  inc      ebx
00158F9D  cmp      ebx, 0xa
00158FA0  jae      0x158fc0  ; -> 00158FC0
00158FA2  cmp      byte ptr [rsi + rbp + 0x2d8e120], 0
00158FAA  jne      0x158f90  ; -> 00158F90
00158FAC  cmp      qword ptr [rbp + rsi*8 + 0x2d8e100], 0  ; image base + 0x2d8e100 = 02EAE100
00158FB5  jne      0x158fc5  ; -> 00158FC5
00158FB7  mov      ecx, esi
00158FB9  call     0x158ec0  ; -> 00158EC0 fn
00158FBE  jmp      0x158fc7  ; -> 00158FC7
00158FC0  or       eax, 0xffffffff
00158FC3  jmp      0x158fc7  ; -> 00158FC7
00158FC5  xor      eax, eax
00158FC7  mov      rbx, qword ptr [rsp + 0x30]
00158FCC  mov      rbp, qword ptr [rsp + 0x38]
00158FD1  mov      rsi, qword ptr [rsp + 0x40]
00158FD6  add      rsp, 0x20
00158FDA  pop      rdi
00158FDB  ret      
```

## 002287A0 (41 B, extent 002287A0-002287C9)

Entered from (direct sites whose caller this page cites): `002507C0` + 0x2F (call; `002507C0` is cited on this page)
Other direct sites: `00210930` + 0xA (call)

Host context: "ore a     script 'fadein' ([the fade page](../../17-Presentation-Rendering/Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md)).     The constructor writes it once ('001D947B').    So '002507C0' presents at interval 2 unless a map jump is under way.   Census: every write to '+0x88' in '001D9000'–'001DB200' plus the getter's call sites and the   methods they pass it to. - [x] ~~**UQ-268.** **Whether a shipped installation'"

```
002287A0  sub      rsp, 0x28
002287A4  call     0x229ea0  ; -> 00229EA0 fn
002287A9  cmp      eax, 6
002287AC  je       0x2287bf  ; -> 002287BF
002287AE  call     0x229ea0  ; -> 00229EA0 fn
002287B3  cmp      eax, 5
002287B6  je       0x2287bf  ; -> 002287BF
002287B8  xor      eax, eax
002287BA  add      rsp, 0x28
002287BE  ret      
002287BF  mov      eax, 1
002287C4  add      rsp, 0x28
002287C8  ret      
```

## 0029FAD0 (115 B, extent 0029FAD0-0029FB43)

Entered from (direct sites whose caller this page cites): `0023B6F0` + 0x312 (call; `0023B6F0` is cited on this page)
Other direct sites: `0023CAF0` + 0x177 (call)

Host context: "X-6.** - [x] ~~*When* the graphics-apply callback runs.~~ **ANSWERED** — when the player pushes left or right       on a row of the in-game Config screen, and nowhere else in the image. '0023B330' / '0023B6F0' are       the **procs of two row objects**, not registered callbacks; 'FUN_0023BD40' is the screen's own proc.       [the Config screen](../../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md). **AX-6a.** - "

```
0029FAD0  mov      qword ptr [rsp + 0x18], rbx
0029FAD5  push     rdi
0029FAD6  sub      rsp, 0x30
0029FADA  mov      ebx, dword ptr [rcx + 8]
0029FADD  xor      eax, eax
0029FADF  mov      rdi, rcx
0029FAE2  shl      ebx, 0x10
0029FAE5  mov      ecx, dword ptr [rcx + 0x20]
0029FAE8  sar      ebx, 0x16
0029FAEB  mov      word ptr [rsp + 0x40], ax
0029FAF0  mov      word ptr [rsp + 0x48], ax
0029FAF5  call     0x20e600  ; -> 0020E600 fn
0029FAFA  mov      r8, qword ptr [rdi + 0x18]
0029FAFE  lea      rdx, [rsp + 0x48]
0029FB03  mov      r9, rax
0029FB06  mov      dword ptr [rsp + 0x20], ebx
0029FB0A  lea      rcx, [rsp + 0x40]
0029FB0F  call     0x2d8b00  ; -> 002D8B00 fn
0029FB14  movsx    eax, word ptr [rsp + 0x40]
0029FB19  mov      rbx, qword ptr [rsp + 0x50]
0029FB1E  movd     xmm0, eax
0029FB22  cvtdq2ps xmm0, xmm0
0029FB25  mulss    xmm0, dword ptr [rdi + 0x28]
0029FB2A  cvttss2si eax, xmm0
0029FB2E  mov      word ptr [rdi + 0xa], ax
0029FB32  and      dword ptr [rdi + 8], 0xffff003f
0029FB39  or       byte ptr [rdi + 0x2d], 4
0029FB3D  add      rsp, 0x30
0029FB41  pop      rdi
0029FB42  ret      
```

## 00441EE0 (40 B, extent 00441EE0-00441F08)

Entered from (direct sites whose caller this page cites): `002F2530` + 0x6EF (call; `002F2530` is cited on this page)
Other direct sites: none

Host context: "float thresholds '81.5', '95.5', '301.0' … | per-case frame adjustments | '0' | | '001EDAD0()' | '003D9150' | 'sum_j0001' loaded, state 7, odd slot counter '01F832C4' | '1' | '0' | | '001EDBB0(…)' | '002F2530' (effect frame advance — **interior read 2026-09-17, SWE2-FRONTIER**: '001EDDA0' ×2 over '02EBEF88', '003A8950'/'002F31C0' arms at ['002F25CD'](../../_index/ADDRESS-INDEX.md), then a π/2- and −0.5-scaled SSE stage writing the '022D"

```
00441EE0  test     rcx, rcx
00441EE3  je       0x441eff  ; -> 00441EFF
00441EE5  mov      rax, qword ptr [rcx + 0x118]
00441EEC  test     rax, rax
00441EEF  je       0x441eff  ; -> 00441EFF
00441EF1  cmp      rax, rdx
00441EF4  je       0x441f02  ; -> 00441F02
00441EF6  mov      rax, qword ptr [rax + 0x30]
00441EFA  test     rax, rax
00441EFD  jne      0x441ef1  ; -> 00441EF1
00441EFF  xor      eax, eax
00441F01  ret      
00441F02  mov      eax, 1
00441F07  ret      
```
