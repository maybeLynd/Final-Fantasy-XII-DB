# Homing pack: `03-World-Area-Field/Weather/weather-probability-and-transition-roll.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-weather-probability-and-transition-roll.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001817D0 (37 B, extent 001817D0-001817F5)

Entered from (direct sites whose caller this page cites): `003C5910` + 0x9B (call; `003C5910` is cited on this page)
Other direct sites: none

Host context: "odies reaching '003148F0' on this page. 'FUN_003c80c0' is the worked example - it is a 230-byte lazy creator: when '[02B476B0]' is empty it makes a **'0xC8'-byte** object around the '.text' callback '003C5910' and caches it there. '003C5910' interior read 2026-09-17 (SWE2-FRONTIER): 1,159 B — '002432B0' first at ['003C5959'](../../_index/ADDRESS-INDEX.md), '003C5720'/'002DD7E0'/'0029F5D0' ×2. The crossing is **one shared subject with 5 "

```
001817D0  sub      rsp, 0x38
001817D4  movaps   xmmword ptr [rsp + 0x20], xmm6
001817D9  movaps   xmm6, xmm0
001817DC  call     0x1b1c00  ; -> 001B1C00 fn
001817E1  mov      rcx, rax
001817E4  movaps   xmm1, xmm6
001817E7  movaps   xmm6, xmmword ptr [rsp + 0x20]
001817EC  add      rsp, 0x38
001817F0  jmp      0x1b1ff0  ; -> 001B1FF0 fn
```

## 003ED7B0 (54 B, extent 003ED7B0-003ED7E6)

Entered from (direct sites whose caller this page cites): `0026E8D0` + 0x81 (jmp; `0026E8D0` is cited on this page)
Other direct sites: none

Host context: "re-run.** '0025ACA0' has **exactly one direct caller**, '002620E0', and **zero** functions reach it by any route that does not pass that latch. **Movement reconfiguration cannot be reached either.** '0026E8D0' has two direct callers, '00379290' and '00379630'; the only thing that reaches *those* is the same latch. Its entire reverse cone within 8 hops is **12 functions** and contains **one** route. **But APPLY is different, and this is "

```
003ED7B0  mov      rdx, qword ptr [rip + 0x2ace039]  ; -> 02EBB7F0
003ED7B7  test     rdx, rdx
003ED7BA  je       0x3ed7e5  ; -> 003ED7E5
003ED7BC  movsxd   rax, ecx
003ED7BF  lea      rcx, [rax + rax*2]
003ED7C3  shl      rcx, 7
003ED7C7  mov      eax, dword ptr [rcx + rdx + 0x10]
003ED7CB  mov      dword ptr [rip + 0x2ace027], eax  ; -> 02EBB7F8
003ED7D1  mov      eax, dword ptr [rcx + rdx + 0x14]
003ED7D5  mov      dword ptr [rip + 0x2ace021], eax  ; -> 02EBB7FC
003ED7DB  mov      eax, dword ptr [rcx + rdx + 0x1c]
003ED7DF  mov      dword ptr [rip + 0x2ace01f], eax  ; -> 02EBB804
003ED7E5  ret      
```

## 003FFF70 (128 B, extent 003FFF70-003FFFF0)

Entered from (direct sites whose caller this page cites): `003C5910` + 0x440 (call; `003C5910` is cited on this page)
Other direct sites: none

Host context: "odies reaching '003148F0' on this page. 'FUN_003c80c0' is the worked example - it is a 230-byte lazy creator: when '[02B476B0]' is empty it makes a **'0xC8'-byte** object around the '.text' callback '003C5910' and caches it there. '003C5910' interior read 2026-09-17 (SWE2-FRONTIER): 1,159 B — '002432B0' first at ['003C5959'](../../_index/ADDRESS-INDEX.md), '003C5720'/'002DD7E0'/'0029F5D0' ×2. The crossing is **one shared subject with 5 "

```
003FFF70  sub      rsp, 0xf8
003FFF77  mov      rax, qword ptr [rip + 0x1b448b2]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003FFF7E  xor      rax, rsp
003FFF81  mov      qword ptr [rsp + 0xe0], rax
003FFF89  call     0x35bad0  ; -> 0035BAD0 fn
003FFF8E  test     eax, eax
003FFF90  jne      0x3fffb4  ; -> 003FFFB4
003FFF92  mov      ecx, 1
003FFF97  call     0x3c53e0  ; -> 003C53E0 fn
003FFF9C  mov      rcx, qword ptr [rsp + 0xe0]
003FFFA4  xor      rcx, rsp
003FFFA7  call     0x808c40  ; -> 00808C40 fn
003FFFAC  add      rsp, 0xf8
003FFFB3  ret      
003FFFB4  lea      r8, [rsp + 0x20]
003FFFB9  mov      edx, eax
003FFFBB  xor      ecx, ecx
003FFFBD  call     0x272e10  ; -> 00272E10 fn
003FFFC2  test     eax, eax
003FFFC4  je       0x3fff92  ; -> 003FFF92
003FFFC6  mov      edx, dword ptr [rsp + 0x28]
003FFFCA  mov      ecx, 1
003FFFCF  test     edx, edx
003FFFD1  je       0x3fff97  ; -> 003FFF97
003FFFD3  call     0x3c5400  ; -> 003C5400 fn
003FFFD8  mov      rcx, qword ptr [rsp + 0xe0]
003FFFE0  xor      rcx, rsp
003FFFE3  call     0x808c40  ; -> 00808C40 fn
003FFFE8  add      rsp, 0xf8
003FFFEF  ret      
```
