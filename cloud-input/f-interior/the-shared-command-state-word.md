# F-interior pack: `17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-shared-command-state-word.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

## 00181AB0 (102 B, extent 00181AB0-00181B16)

Page context: "EC0'/'00863430'. Interior anchor '00863703' (an '0016D6A0' call).  ## SWE2-EC7-45 update (2026-09-19) - '0022BEB0'  '0022BEB0' (238 B) is the 'VFXSystem_RenderLayerPass' root - '0017F2F0'/'0017F370'/'00181AB0'/'00181C10'/'00181C70'/'00181DD0'/'00181E30'. Interior anchor '0022BEB4' (an '0017F2F0' call).  ## SWE2-EC7-54 update (2026-09-19) - '001AE550'  '001AE550' (347 B) is a shared-command-state body - '001A4BF0'/'001AEC30'/'001EDF00' p"

```
00181AB0  push     rdi
00181AB2  sub      rsp, 0x30
00181AB6  call     0x1eba40  ; -> 001EBA40 fn
00181ABB  mov      rdi, qword ptr [rax + 0x270]
00181AC2  call     0x189120  ; -> 00189120 fn
00181AC7  test     rax, rax
00181ACA  je       0x181b10  ; -> 00181B10
00181ACC  mov      qword ptr [rsp + 0x40], rbx
00181AD1  call     0x189120  ; -> 00189120 fn
00181AD6  mov      rcx, rax
00181AD9  xor      edx, edx
00181ADB  call     0x186910  ; -> 00186910 fn
00181AE0  cmp      byte ptr [rax + 8], 0
00181AE4  jne      0x181aeb  ; -> 00181AEB
00181AE6  mov      rbx, qword ptr [rax]
00181AE9  jmp      0x181aed  ; -> 00181AED
00181AEB  xor      ebx, ebx
00181AED  call     0x18ca40  ; -> 0018CA40 fn
00181AF2  mov      rcx, rax
00181AF5  mov      byte ptr [rsp + 0x20], 0
00181AFA  mov      r9d, 4
00181B00  mov      r8, rdi
00181B03  mov      rdx, rbx
00181B06  call     0x18b8b0  ; -> 0018B8B0 fn
00181B0B  mov      rbx, qword ptr [rsp + 0x40]
00181B10  add      rsp, 0x30
00181B14  pop      rdi
00181B15  ret      
```

## 001C5040 (123 B, extent 001C5040-001C50BB)

Page context: "d copied to '01FD3B00' / '01FD3B04' / '01FD3B14'; flag bytes '01FD3AE4' / 'AE5' / 'AE0' / 'AE1' / 'AE2' / 'AE3' each arm a one-shot notify through '001CC920' / '001CC800' / '001C61F0' / '001C7290' / '001C5040', with float pairs '01FD3ACC'/'AD0' and '01FD3AD8'/'ADC' staged into '01FD3AF4'/'AF8' and '01FD3B08'/'B0C' when 'dword[01FD3AE8]' is nonzero. '001EC560()' vetoes the active paths. A per-slot byte/dword table at '01EB3AE0' (bounds '"

```
001C5040  sub      rsp, 0x28
001C5044  mov      rax, qword ptr [rip + 0x1dbc25d]  ; -> 01F812A8
001C504B  cmp      rax, qword ptr [rip + 0x1dbc25e]  ; -> 01F812B0
001C5052  je       0x1c5065  ; -> 001C5065
001C5054  mov      byte ptr [rax], 0
001C5057  mov      rax, qword ptr [rip + 0x1dbc24a]  ; -> 01F812A8
001C505E  mov      qword ptr [rip + 0x1dbc24b], rax  ; -> 01F812B0
001C5065  movsxd   rcx, dword ptr [rip + 0x1dbc38c]  ; -> 01F813F8
001C506C  lea      rax, [rip + 0x1dbc335]  ; -> 01F813A8
001C5073  shl      rcx, 4
001C5077  add      rcx, rax
001C507A  call     0x202880  ; -> 00202880 fn
001C507F  movsxd   rcx, dword ptr [rip + 0x1dbc372]  ; -> 01F813F8
001C5086  lea      rax, [rip + 0x1dbc34b]  ; -> 01F813D8
001C508D  shl      rcx, 4
001C5091  add      rcx, rax
001C5094  call     0x202880  ; -> 00202880 fn
001C5099  movsxd   rax, dword ptr [rip + 0x1dbc358]  ; -> 01F813F8
001C50A0  lea      rcx, [rip + 0x1dbc359]  ; -> 01F81400
001C50A7  mov      dword ptr [rcx + rax*4], 0xffffffff
001C50AE  mov      dword ptr [rcx + rax*4 + 8], 0xffffffff
001C50B6  add      rsp, 0x28
001C50BA  ret      
```

## 001CC920 (117 B, extent 001CC920-001CC995)

Page context: ")' + '0018D5F0(out, &rec)' produce a 0x14-byte record copied to '01FD3B00' / '01FD3B04' / '01FD3B14'; flag bytes '01FD3AE4' / 'AE5' / 'AE0' / 'AE1' / 'AE2' / 'AE3' each arm a one-shot notify through '001CC920' / '001CC800' / '001C61F0' / '001C7290' / '001C5040', with float pairs '01FD3ACC'/'AD0' and '01FD3AD8'/'ADC' staged into '01FD3AF4'/'AF8' and '01FD3B08'/'B0C' when 'dword[01FD3AE8]' is nonzero. '001EC560()' vetoes the active paths."

```
001CC920  sub      rsp, 0x28
001CC924  test     edx, edx
001CC926  jne      0x1cc995  ; -> 001CC995
001CC928  movsxd   rax, dword ptr [rip + 0x1c31add]  ; -> 01DFE40C [u32 0xFFFFFFFF]
001CC92F  cmp      eax, 4
001CC932  ja       0x1cc995  ; -> 001CC995
001CC934  lea      rdx, [rip + 0x1db6975]  ; -> 01F832B0
001CC93B  cmp      dword ptr [rdx + rax*4], 0
001CC93F  jle      0x1cc995  ; -> 001CC995
001CC941  mov      qword ptr [rsp + 0x20], rbx
001CC946  lea      rax, [rip + 0x1db4a5b]  ; -> 01F813A8
001CC94D  xor      ebx, ebx
001CC94F  lea      rdx, [rip + 0x1db4a02]  ; -> 01F81358
001CC956  test     cl, cl
001CC958  movsxd   rcx, dword ptr [rip + 0x1db4a99]  ; -> 01F813F8
001CC95F  setne    bl
001CC962  shl      rcx, 4
001CC966  add      rcx, rax
001CC969  call     0x1ff6b0  ; -> 001FF6B0 fn
001CC96E  mov      rcx, rax
001CC971  lea      rdx, [rip + 0x72dae8]  ; -> 008FA460 [str "EnableDof"]
001CC978  call     0x1ff740  ; -> 001FF740 fn
001CC97D  mov      rcx, rax
001CC980  mov      edx, ebx
001CC982  mov      rbx, qword ptr [rsp + 0x20]
001CC987  add      rsp, 0x28
001CC98B  jmp      0x202820  ; -> 00202820 fn
001CC990  mov      rbx, qword ptr [rsp + 0x20]
```

## 001EC5A0 (31 B, extent 001EC5A0-001EC5BF)

Page context: "7F303' (the '+0x230' clear).  ## SWE2-EC7-113 update (2026-09-21) - '001B7D20' measured  '001B7D20' (8 B) is the 'dword[+4] == 3' kind predicate '0017F6B0' runs mid-dispatch ('00180170', '001E03F0', '001EC5A0' run it too): 'cmp'/'sete'/'ret' and nothing else - one field of the record answering whether it carries the kind-3 shape. Interior anchor '001B7D24' (the 'sete').  '00863520' (31 B) is the window-half helper '00368C10', '00368C80'"

```
001EC5A0  sub      rsp, 0x28
001EC5A4  call     0x1b7f20  ; -> 001B7F20 fn
001EC5A9  mov      rcx, rax
001EC5AC  call     0x1b7d20  ; -> 001B7D20 fn
001EC5B1  xor      ecx, ecx
001EC5B3  test     al, al
001EC5B5  setne    cl
001EC5B8  mov      eax, ecx
001EC5BA  add      rsp, 0x28
001EC5BE  ret      
```

## 0036D7E0 (40 B, extent 0036D7E0-0036D808)

Page context: " a store to '02EBA3F8' lands between its two loads, which needs a writer on another core. > The eight writer functions (the three publishers, the clearer, the reset burst, both effect-capture draws, '0036D7E0') > all run on the main thread, and no thread start reaches any of them ('CG-3', §7). So on every path both spins are two > loads and a compare that agree on the first pass, and the second spin is redundant rather than protective. "

```
0036D7E0  movsxd   rax, dword ptr [rip + 0x1f6b6c1]  ; -> 022D8EA8
0036D7E7  mov      dword ptr [rip + 0x2b4cc07], 0  ; -> 02EBA3F8
0036D7F1  lea      rcx, [rax + rax*4]
0036D7F5  lea      rax, [rip + 0x1f6b654]  ; -> 022D8E50
0036D7FC  lea      rax, [rax + rcx*8]
0036D800  mov      qword ptr [rip + 0x1f6b699], rax  ; -> 022D8EA0
0036D807  ret      
```
