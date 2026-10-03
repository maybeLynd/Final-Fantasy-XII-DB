# Homing pack: `22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-animation-channel-binding-and-transform-composition.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0059FC20 (126 B, extent 0059FC20-0059FC9E)

Entered from (direct sites whose caller this page cites): `005C0820` + 0x11F (call; `005C0820` is cited on this page)
Other direct sites: none

Host context: "he same class-descriptor system documented in ['../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md'](../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md).  '005C0820' walks that path. For each binding descriptor it splits the name on ''.'' ('strchr(name, 0x2e)'), looks each segment up as a member of the current class descriptor, and accumulates a byte offset as it descends. When the path runs o"

```
0059FC20  mov      qword ptr [rsp + 8], rbx
0059FC25  push     rdi
0059FC26  sub      rsp, 0x20
0059FC2A  mov      rbx, r8
0059FC2D  mov      rax, rdx
0059FC30  mov      rdi, rcx
0059FC33  test     rdx, rdx
0059FC36  je       0x59fc8e  ; -> 0059FC8E
0059FC38  test     rbx, rbx
0059FC3B  je       0x59fc8e  ; -> 0059FC8E
0059FC3D  cmp      rbx, rdx
0059FC40  jae      0x59fc52  ; -> 0059FC52
0059FC42  mov      eax, 5
0059FC47  mov      rbx, qword ptr [rsp + 0x30]
0059FC4C  add      rsp, 0x20
0059FC50  pop      rdi
0059FC51  ret      
0059FC52  sub      ebx, eax
0059FC54  mov      rcx, rax
0059FC57  lea      edx, [rbx + 1]
0059FC5A  call     0x5994a0  ; -> 005994A0 fn
0059FC5F  mov      rdx, rax
0059FC62  test     rax, rax
0059FC65  jne      0x59fc75  ; -> 0059FC75
0059FC67  lea      eax, [rdx + 0xd]
0059FC6A  mov      rbx, qword ptr [rsp + 0x30]
0059FC6F  add      rsp, 0x20
0059FC73  pop      rdi
0059FC74  ret      
0059FC75  mov      rcx, rdi
0059FC78  mov      byte ptr [rbx + rax], 0
0059FC7C  call     0x59fbe0  ; -> 0059FBE0 fn
0059FC81  xor      eax, eax
0059FC83  mov      rbx, qword ptr [rsp + 0x30]
0059FC88  add      rsp, 0x20
0059FC8C  pop      rdi
0059FC8D  ret      
0059FC8E  mov      eax, 1
0059FC93  mov      rbx, qword ptr [rsp + 0x30]
0059FC98  add      rsp, 0x20
0059FC9C  pop      rdi
0059FC9D  ret      
```

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
