# F-interior pack: `18-Audio/how-the-music-changes-when-you-change-area.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/how-the-music-changes-when-you-change-area.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 00218E50 (45 B, extent 00218E50-00218E7D)

Page context: "Answered 2026-09-14 (FABLE)       for the outgoing-track fade: sixtieths of a second of real time, so '0x78' is 2.0 s.** '002DEE50' →       '001DBCA0' → the registry's music controller ('00210A50' → '00218E50') → '00222B70'. That function converts       the length with '(float)len / 60.0' ('008F6D54') and the volume with '/ 127.0' ('00906A44'), then calls SEAD's       'SetVolume' '007A81F0'. SEAD advances every ramp by a 'dt' it measure"

```
00218E50  mov      rax, qword ptr [rcx + 8]
00218E54  lea      r10, [rcx + 8]
00218E58  cmp      rax, r10
00218E5B  je       0x218e7c  ; -> 00218E7C
00218E5D  nop      dword ptr [rax]
00218E60  mov      rcx, qword ptr [rax + 0x10]
00218E64  cmp      edx, -1
00218E67  je       0x218e77  ; -> 00218E77
00218E69  cmp      dword ptr [rcx + 0x50], edx
00218E6C  je       0x218e77  ; -> 00218E77
00218E6E  mov      rax, qword ptr [rax]
00218E71  cmp      rax, r10
00218E74  jne      0x218e60  ; -> 00218E60
00218E76  ret      
00218E77  jmp      0x222b70  ; -> 00222B70 fn
00218E7C  ret      
```

## 003473A0 (30 B, extent 003473A0-003473BE)

Page context: "attle-data.md)       records as reading the area trailer's '{selector, mask}' list. So the non-music path schedules       the per-area actor flag-mask pass. '0037C910' has three callers: '00261F90', '003473A0' and '00359800'.       ~~**Not read:** the eleven states themselves, and what argument 1 selects in them.~~        ***ANSWERED 2026-09-21 (FABLE) — the argument is a pass count, and '1' buys a third source.***       Read complete o"

```
003473A0  sub      rsp, 0x28
003473A4  call     0x37b4a0  ; -> 0037B4A0 fn
003473A9  xor      ecx, ecx
003473AB  call     0x37c910  ; -> 0037C910 fn
003473B0  mov      ecx, 1
003473B5  add      rsp, 0x28
003473B9  jmp      0x314d40  ; -> 00314D40 fn
```

## 003614C0 (28 B, extent 003614C0-003614DC)

Page context: "sfade is one duration and one volume  | constant | where | meaning | |---|---|---| | '0x78' = 120 | passed as the duration argument at three sites | a fade length | | '0x7F' = 127 | hardcoded inside '003614C0', and passed directly at one site | **full volume** | | '0x00' | passed where '0x7F' otherwise goes | **silence** |  '0x7F' is the same full-scale value the mixer boundary uses — the volume path divides by 127, so **'0x7F' is 1.0**"

```
003614C0  sub      rsp, 0x38
003614C4  mov      r9d, 0x7f
003614CA  mov      dword ptr [rsp + 0x20], 0
003614D2  call     0x3614e0  ; -> 003614E0 fn
003614D7  add      rsp, 0x38
003614DB  ret      
```

## 003EB0D0 (41 B, extent 003EB0D0-003EB0F9)

Page context: "the allocated buffer, was read as far as its gate:  '''c g_currentSelector = selector;        /* 0x022C51D8 */ g_currentIndex    = index;           /* 0x022C51DC */ if (index < 0) return -1; if (!FUN_003EB0D0()) goto alternate; /* 0x0032E742 */ /* then a 0x28-byte descriptor is copied in from the caller's stack struct */ '''  **'FUN_003EB0D0' (41 B) is a presence check**, not a loader:  '''asm 003EB0D2  lea  rax, [02B5E111]      ; a byt"

```
003EB0D0  xor      ecx, ecx
003EB0D2  lea      rax, [rip + 0x2773038]  ; -> 02B5E111
003EB0D9  nop      dword ptr [rax]
003EB0E0  cmp      byte ptr [rax], 0
003EB0E3  jne      0x3eb0f3  ; -> 003EB0F3
003EB0E5  inc      ecx
003EB0E7  add      rax, 0x38
003EB0EB  cmp      ecx, 1
003EB0EE  jl       0x3eb0e0  ; -> 003EB0E0
003EB0F0  xor      eax, eax
003EB0F2  ret      
003EB0F3  mov      eax, 1
003EB0F8  ret      
```
