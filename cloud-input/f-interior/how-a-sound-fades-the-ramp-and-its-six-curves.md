# F-interior pack: `18-Audio/Audio-Boundary/how-a-sound-fades-the-ramp-and-its-six-curves.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/how-a-sound-fades-the-ramp-and-its-six-curves.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

## 00222B70 (95 B, extent 00222B70-00222BCF)

Page context: "e negative: the tick difference is > converted as unsigned ('jns' / 'addsd 2^64', '007A546C'). Ramp durations are therefore seconds, and the game-side callers convert from sixtieths with '/ 60.0' > ('00222B70'; [the music-change page](../how-the-music-changes-when-you-change-area.md) §7).  > **Answered 2026-09-14 (FABLE, 'DQ-1'): it cannot, because the advancer clamps.** The per-update ramp step is '007AA770', > called from '007AAEA0'. "

```
00222B70  mov      qword ptr [rsp + 8], rbx
00222B75  mov      qword ptr [rsp + 0x10], rsi
00222B7A  push     rdi
00222B7B  sub      rsp, 0x20
00222B7F  lea      rbx, [rcx + 0x38]
00222B83  mov      edi, r9d
00222B86  mov      rcx, rbx
00222B89  mov      esi, r8d
00222B8C  call     0x7a7010  ; -> 007A7010 fn
00222B91  test     eax, eax
00222B93  je       0x222bbf  ; -> 00222BBF
00222B95  movd     xmm2, esi
00222B99  or       r9d, 0xffffffff
00222B9D  movd     xmm1, edi
00222BA1  mov      rcx, rbx
00222BA4  cvtdq2ps xmm2, xmm2
00222BA7  cvtdq2ps xmm1, xmm1
00222BAA  divss    xmm2, dword ptr [rip + 0x6d41a2]  ; -> 008F6D54 [f32 60]
00222BB2  divss    xmm1, dword ptr [rip + 0x6e3e8a]  ; -> 00906A44 [f32 127]
00222BBA  call     0x7a81f0  ; -> 007A81F0 fn
00222BBF  mov      rbx, qword ptr [rsp + 0x30]
00222BC4  mov      rsi, qword ptr [rsp + 0x38]
00222BC9  add      rsp, 0x20
00222BCD  pop      rdi
00222BCE  ret      
```
