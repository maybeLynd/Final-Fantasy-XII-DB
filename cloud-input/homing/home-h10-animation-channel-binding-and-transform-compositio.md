# Homing pack: `22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-animation-channel-binding-and-transform-compositio.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 005E3040 (150 B, extent 005E3040-005E30D6)

Entered from (direct sites whose caller this page cites): `005C9F30` + 0x3F (call; `005C9F30` is cited on this page)
Other direct sites: `005C9270` + 0x2F (call); `0060C3F0` + 0x2D (call)

Host context: "PAnimationChannelTargetBindShaderParameter''s binder '005C1160' writes kind 1 at '005C1274' and the destination at '005C127A')*.  **Do not confuse with:**  - **'PAnimationBlenderController' slot 12 ('005C9F30') is not this function.** It resizes a pointer   array (count at '+0x18' with bit 31 as an ownership flag, data at '+0x20'). It shares a *slot   number* with 'PAnimationTargetBlenderController' slot 12 ('005C72A0'), and nothing els"

```
005E3040  mov      qword ptr [rsp + 0x10], rbx
005E3045  mov      qword ptr [rsp + 0x18], rbp
005E304A  push     rsi
005E304B  sub      rsp, 0x20
005E304F  mov      ebp, r8d
005E3052  mov      rbx, rdx
005E3055  mov      esi, ecx
005E3057  test     ecx, ecx
005E3059  je       0x5e30c4  ; -> 005E30C4
005E305B  mov      ecx, esi
005E305D  mov      edx, 8
005E3062  shl      rcx, 3
005E3066  call     0x17d260  ; -> 0017D260 fn
005E306B  mov      r9, rax
005E306E  test     rax, rax
005E3071  je       0x5e30b4  ; -> 005E30B4
005E3073  mov      qword ptr [rsp + 0x30], rdi
005E3078  mov      rcx, rax
005E307B  test     ebp, ebp
005E307D  je       0x5e309d  ; -> 005E309D
005E307F  mov      edi, ebp
005E3081  mov      rdx, rcx
005E3084  add      rcx, 8
005E3088  test     rdx, rdx
005E308B  je       0x5e3097  ; -> 005E3097
005E308D  mov      rax, qword ptr [rbx]
005E3090  add      rbx, 8
005E3094  mov      qword ptr [rdx], rax
005E3097  sub      rdi, 1
005E309B  jne      0x5e3081  ; -> 005E3081
005E309D  sub      esi, ebp
005E309F  je       0x5e30ac  ; -> 005E30AC
005E30A1  lea      rdi, [r9 + rbp*8]
005E30A5  mov      ecx, esi
005E30A7  xor      eax, eax
005E30A9  rep stosq qword ptr [rdi], rax
005E30AC  mov      rdi, qword ptr [rsp + 0x30]
005E30B1  mov      rax, r9
005E30B4  mov      rbx, qword ptr [rsp + 0x38]
005E30B9  mov      rbp, qword ptr [rsp + 0x40]
005E30BE  add      rsp, 0x20
005E30C2  pop      rsi
005E30C3  ret      
005E30C4  mov      rbx, qword ptr [rsp + 0x38]
005E30C9  xor      eax, eax
005E30CB  mov      rbp, qword ptr [rsp + 0x40]
005E30D0  add      rsp, 0x20
005E30D4  pop      rsi
005E30D5  ret      
```
