# F-interior pack: `24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/exception-funclets-and-lazy-static-guards.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (inbox mentions: repos-94.md). OPUS read these before packing.

## 001DAAC0 (112 B, extent 001DAAC0-001DAB30)

Page context: "io caller '00212130' reaches the SEH-filter parent '005CD1E0'.    None is an establisher frame; the sound pages own what they do. - **Resource — MECHANICAL, two edges.** '005CD1E0' is also called by '001DAAC0', and the catch-funclet example's parent   '008098D4' by '001F4250'. - **CoreRuntimeScheduling and Presentation — MECHANICAL, one edge each.** The magic-static example '00189CE0' is   reached from the frame step '0017D6E0', and the"

```
001DAAC0  push     rbx
001DAAC2  sub      rsp, 0x60
001DAAC6  mov      rbx, rcx
001DAAC9  lea      rdx, [rip + 0x2e0]  ; -> 001DADB0
001DAAD0  lea      rcx, [rsp + 0x20]
001DAAD5  call     0x5cc8c0  ; -> 005CC8C0 fn
001DAADA  lea      rax, [rip + 0x725b07]  ; -> 009005E8 [str "FileCachePrefetchManager"]
001DAAE1  mov      dword ptr [rsp + 0x38], 3
001DAAE9  mov      edx, 0x7c
001DAAEE  mov      qword ptr [rsp + 0x40], rax
001DAAF3  lea      rcx, [rsp + 0x20]
001DAAF8  mov      dword ptr [rsp + 0x4c], 0xfffffffe
001DAB00  mov      dword ptr [rsp + 0x28], 0xf000
001DAB08  call     0x16d6a0  ; -> 0016D6A0 fn
001DAB0D  mov      qword ptr [rsp + 0x30], rbx
001DAB12  lea      rdx, [rsp + 0x20]
001DAB17  mov      rcx, rbx
001DAB1A  mov      dword ptr [rbx + 0x20], 1
001DAB21  call     0x5cd1e0  ; -> 005CD1E0 fn
001DAB26  mov      byte ptr [rbx + 0x18], 1
001DAB2A  add      rsp, 0x60
001DAB2E  pop      rbx
001DAB2F  ret      
```

## 00896270 (2 B, extent 00896270-00896272)

Page context: "gure alone does not suggest. Named '_guard_check_icall' across the database because the load config is the only source that gives these three bytes an identity; the folding is real but nameless. | | '00896270' | '_guard_dispatch_icall' | 2 B | CFG dispatch, per the load-config slot; sits immediately below the funclet block | | '006DA980' | stripped ppfx diagnostic reporter | 3 B ('ret') | called by **99** funclets, still passed '__FILE_"

```
00896270  jmp      rax
```

## 0089BEF0 (18 B, extent 0089BEF0-0089BF02)

Page context: "osoft.MSVCCRT_STL_Runtime.Support' | byte-identical to both |  **The seven SEH filters** (six of which carry no 'CompilerGeneratedEH' tag):  | Address | Parent | Tagged? | Body | |---|---|---|---| | '0089BEF0' | '005CD1E0' | no | 'return 0xFFFFFFFF' | | '008A5AD0' | '005CCBA0' | no | 'FUN_005ccbf0()' | | '008A5B7C' | '00808A54' | no | 'return *(int*)*p == 0xC0000005' | | '008A5B94' | '00808D78' | no | '_seh_filter_exe(code, p)' | | '008"

```
0089BEF0  push     rbp
0089BEF2  sub      rsp, 0x40
0089BEF6  mov      rbp, rdx
0089BEF9  or       eax, 0xffffffff
0089BEFC  add      rsp, 0x40
0089BF00  pop      rbp
0089BF01  ret      
```

## 008A5B7C (23 B, extent 008A5B7C-008A5B93)

Page context: "y no 'CompilerGeneratedEH' tag):  | Address | Parent | Tagged? | Body | |---|---|---|---| | '0089BEF0' | '005CD1E0' | no | 'return 0xFFFFFFFF' | | '008A5AD0' | '005CCBA0' | no | 'FUN_005ccbf0()' | | '008A5B7C' | '00808A54' | no | 'return *(int*)*p == 0xC0000005' | | '008A5B94' | '00808D78' | no | '_seh_filter_exe(code, p)' | | '008A5BB2' | '00808FE4' | no | guarded '__ArrayUnwind' | | '008A5BDE' | '00809054' | no | guarded '__ArrayUnwin"

```
008A5B7C  push     rbp
008A5B7E  mov      rbp, rdx
008A5B81  mov      rax, qword ptr [rcx]
008A5B84  xor      ecx, ecx
008A5B86  cmp      dword ptr [rax], 0xc0000005
008A5B8C  sete     cl
008A5B8F  mov      eax, ecx
008A5B91  pop      rbp
008A5B92  ret      
```

## 008A5C0A (64 B, extent 008A5C0A-008A5C4A)

Page context: "== 0xC0000005' | | '008A5B94' | '00808D78' | no | '_seh_filter_exe(code, p)' | | '008A5BB2' | '00808FE4' | no | guarded '__ArrayUnwind' | | '008A5BDE' | '00809054' | no | guarded '__ArrayUnwind' | | '008A5C0A' | '008090C0' | **yes** ('ExceptionFilter') | '__ArrayUnwind''s own filter |  ---  ## 4. Data structures and formulas  ### The funclet ABI  '''c // cleanup / unwind funclet void  __fastcall Unwind_XXXXXXXX(void *ignored_rcx, char *"

```
008A5C0A  push     rbp
008A5C0C  sub      rsp, 0x20
008A5C10  mov      rbp, rdx
008A5C13  mov      qword ptr [rbp + 0x40], rcx
008A5C17  mov      qword ptr [rbp + 0x30], rcx
008A5C1B  mov      rax, qword ptr [rbp + 0x30]
008A5C1F  mov      rcx, qword ptr [rax]
008A5C22  mov      qword ptr [rbp + 0x38], rcx
008A5C26  mov      rax, qword ptr [rbp + 0x38]
008A5C2A  cmp      dword ptr [rax], 0xe06d7363
008A5C30  je       0x8a5c3e  ; -> 008A5C3E
008A5C32  mov      dword ptr [rbp + 0x20], 0
008A5C39  mov      eax, dword ptr [rbp + 0x20]
008A5C3C  jmp      0x8a5c44  ; -> 008A5C44
008A5C3E  call     0x862052  ; -> 00862052 fn
008A5C43  nop      
008A5C44  add      rsp, 0x20
008A5C48  pop      rbp
008A5C49  ret      
```
