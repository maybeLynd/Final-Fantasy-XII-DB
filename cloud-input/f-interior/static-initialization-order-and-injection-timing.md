# F-interior pack: `24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/static-initialization-order-and-injection-timing.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (inbox mentions: repos-94.md, xiionline-8d.md). OPUS read these before packing.

## 00163DB0 (122 B, extent 00163DB0-00163E2A)

Page context: "its writer.  > **But all nine bodies are a single translation unit, and that changes the answer.** They occupy > **slots 356–365** of the table *and* a **contiguous run of '.text' — nine bodies from '00163DB0' > to '00164180' with zero other functions between them.** MSVC emits one compiland's initializers > contiguously in both places. **Order within a translation unit is guaranteed by declaration > order**, so this is not the fragile "

```
00163DB0  sub      rsp, 0x28
00163DB4  mov      r8d, 8
00163DBA  lea      rdx, [rip + 0x2b948bf]  ; -> 02CF8680
00163DC1  lea      rcx, [rip + 0x2b945a8]  ; -> 02CF8370
00163DC8  call     0x631a60  ; -> 00631A60 fn
00163DCD  mov      eax, dword ptr [rip + 0x2b94699]  ; -> 02CF846C
00163DD3  lea      rcx, [rip + 0x2b950a6]  ; -> 02CF8E80
00163DDA  mov      qword ptr [rip + 0x2b9464f], rcx  ; -> 02CF8430
00163DE1  or       eax, 2
00163DE4  lea      rcx, [rip + 0x2b950f5]  ; -> 02CF8EE0
00163DEB  and      eax, 0xfffffffd
00163DEE  mov      qword ptr [rip + 0x2b94643], rcx  ; -> 02CF8438
00163DF5  or       eax, 8
00163DF8  lea      rcx, [rip + 0x2b95141]  ; -> 02CF8F40
00163DFF  mov      dword ptr [rip + 0x2b94667], eax  ; -> 02CF846C
00163E05  mov      qword ptr [rip + 0x2b94634], rcx  ; -> 02CF8440
00163E0C  lea      rcx, [rip + 0xbf2cc5]  ; -> 00D56AD8
00163E13  mov      qword ptr [rip + 0x2b94556], rcx  ; -> 02CF8370
00163E1A  lea      rcx, [rip + 0x74b26f]  ; -> 008AF090
00163E21  add      rsp, 0x28
00163E25  jmp      0x808b90  ; -> 00808B90 fn
```

## 00163E30 (108 B, extent 00163E30-00163E9C)

Page context: "mpiland, not two (FABLE, 2026-09-22)  The clearest chain looks at first like exactly what 'T-4' asks about. '00164180' **constructs** an object at '02CF8270' and installs a function pointer into it; '00163E30' then calls '00631C40(dest = 02CF8470, src = 02CF8270, 0x30)' — **deriving its own object from that one** — and five more initializers read '02CF8270' the same way. '02CF8470' is in turn read by '00163EA0', so it is a **two-level c"

```
00163E30  sub      rsp, 0x28
00163E34  mov      r8d, 0x30
00163E3A  lea      rdx, [rip + 0x2b9442f]  ; -> 02CF8270
00163E41  lea      rcx, [rip + 0x2b94628]  ; -> 02CF8470
00163E48  call     0x631c40  ; -> 00631C40 fn
00163E4D  or       dword ptr [rip + 0x2b94718], 2  ; -> 02CF856C
00163E54  lea      rax, [rip + 0x2b94105]  ; -> 02CF7F60
00163E5B  mov      qword ptr [rip + 0x2b946ce], rax  ; -> 02CF8530
00163E62  lea      rcx, [rip + 0x74b247]  ; -> 008AF0B0
00163E69  lea      rax, [rip + 0x2b941f0]  ; -> 02CF8060
00163E70  mov      qword ptr [rip + 0x2b946c1], rax  ; -> 02CF8538
00163E77  lea      rax, [rip + 0x2b942e2]  ; -> 02CF8160
00163E7E  mov      qword ptr [rip + 0x2b946bb], rax  ; -> 02CF8540
00163E85  lea      rax, [rip + 0xbf28dc]  ; -> 00D56768
00163E8C  mov      qword ptr [rip + 0x2b945dd], rax  ; -> 02CF8470
00163E93  add      rsp, 0x28
00163E97  jmp      0x808b90  ; -> 00808B90 fn
```

## 00163EA0 (119 B, extent 00163EA0-00163F17)

Page context: "E30' then calls '00631C40(dest = 02CF8470, src = 02CF8270, 0x30)' — **deriving its own object from that one** — and five more initializers read '02CF8270' the same way. '02CF8470' is in turn read by '00163EA0', so it is a **two-level chain**. Every reader runs after its writer.  > **But all nine bodies are a single translation unit, and that changes the answer.** They occupy > **slots 356–365** of the table *and* a **contiguous run of '"

```
00163EA0  sub      rsp, 0x28
00163EA4  xor      r8d, r8d
00163EA7  lea      rdx, [rip + 0x2b945c2]  ; -> 02CF8470
00163EAE  lea      rcx, [rip + 0x2b946cb]  ; -> 02CF8580
00163EB5  call     0x631e20  ; -> 00631E20 fn
00163EBA  mov      eax, dword ptr [rip + 0x2b947bc]  ; -> 02CF867C
00163EC0  lea      rcx, [rip + 0x2b93c19]  ; -> 02CF7AE0
00163EC7  mov      qword ptr [rip + 0x2b94772], rcx  ; -> 02CF8640
00163ECE  or       eax, 2
00163ED1  lea      rcx, [rip + 0x2b93d48]  ; -> 02CF7C20
00163ED8  and      eax, 0xfffffffd
00163EDB  mov      qword ptr [rip + 0x2b94766], rcx  ; -> 02CF8648
00163EE2  or       eax, 8
00163EE5  lea      rcx, [rip + 0x2b93e74]  ; -> 02CF7D60
00163EEC  mov      dword ptr [rip + 0x2b9478a], eax  ; -> 02CF867C
00163EF2  mov      qword ptr [rip + 0x2b94757], rcx  ; -> 02CF8650
00163EF9  lea      rcx, [rip + 0xbf2fd0]  ; -> 00D56ED0
00163F00  mov      qword ptr [rip + 0x2b94679], rcx  ; -> 02CF8580
00163F07  lea      rcx, [rip + 0x74b1c2]  ; -> 008AF0D0
00163F0E  add      rsp, 0x28
00163F12  jmp      0x808b90  ; -> 00808B90 fn
```

## 00164180 (56 B, extent 00164180-001641B8)

Page context: "nitializer and read by a different one** | **8** |  ### The ordered dependencies are one compiland, not two (FABLE, 2026-09-22)  The clearest chain looks at first like exactly what 'T-4' asks about. '00164180' **constructs** an object at '02CF8270' and installs a function pointer into it; '00163E30' then calls '00631C40(dest = 02CF8470, src = 02CF8270, 0x30)' — **deriving its own object from that one** — and five more initializers read "

```
00164180  sub      rsp, 0x28
00164184  lea      rcx, [rip + 0x2b940e5]  ; -> 02CF8270
0016418B  call     0x6318a0  ; -> 006318A0 fn
00164190  lea      rax, [rip + 0xbf4139]  ; -> 00D582D0
00164197  mov      dword ptr [rip + 0x2b94107], 0  ; -> 02CF82A8
001641A1  lea      rcx, [rip + 0x74afe8]  ; -> 008AF190
001641A8  mov      qword ptr [rip + 0x2b940c1], rax  ; -> 02CF8270
001641AF  add      rsp, 0x28
001641B3  jmp      0x808b90  ; -> 00808B90 fn
```

## 001E0F70 (49 B, extent 001E0F70-001E0FA1)

Page context: ".  **Input — CLIENT, four edges.** - 'InputManager_RestoreDefaultBindingProfiles' ('00195DF0'), named in T-3 as the copy from the 1,108-byte static   cluster, is called by 'InputManager_Initialize', '001E0F70' and '001E1050'. - It asks 'InputBinding_ShouldKeepAuthoredPairOrderForPlatformState'.  **Presentation — MECHANICAL, four edges.** - '001FE8B0' is called by '001C5750', '001C6E20' and '001CCB20'. - The 28-lazy-static body '005AD8F0"

```
001E0F70  sub      rsp, 0x28
001E0F74  call     0x198790  ; -> 00198790 fn
001E0F79  test     rax, rax
001E0F7C  je       0x1e0f9c  ; -> 001E0F9C
001E0F7E  call     0x198790  ; -> 00198790 fn
001E0F83  mov      rcx, rax
001E0F86  call     0x198b60  ; -> 00198B60 fn
001E0F8B  call     0x198790  ; -> 00198790 fn
001E0F90  mov      rcx, rax
001E0F93  add      rsp, 0x28
001E0F97  jmp      0x195df0  ; -> 00195DF0 fn
001E0F9C  add      rsp, 0x28
001E0FA0  ret      
```
