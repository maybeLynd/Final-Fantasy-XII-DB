# Homing pack: `18-Audio/the-spatial-audio-object-model.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-spatial-audio-object-model.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00219BC0 (122 B, extent 00219BC0-00219C3A)

Entered from (direct sites whose caller this page cites): `00210BE0` + 0x19 (jmp; `00210BE0` is cited on this page)
Other direct sites: none

Host context: "very anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*  | function | size | entered from | what the body does | interior anchors | |---|---|---|---|---| | '00210BE0' | 30 B | '001DBE00' + 0x35 | moves the arguments down one place ('edx' = 'r8d', 'r8' = 'r9') and, when the incoming 'edx' is zero, tail-jumps ('00210BE0' + 0x10) with 'rcx' = qword 'rcx+8', otherwise tail-jumps ('00210BE0' + 0x19)"

```
00219BC0  mov      qword ptr [rsp + 8], rbx
00219BC5  mov      qword ptr [rsp + 0x10], rbp
00219BCA  mov      qword ptr [rsp + 0x18], rsi
00219BCF  push     rdi
00219BD0  push     r14
00219BD2  push     r15
00219BD4  sub      rsp, 0x20
00219BD8  mov      rbx, qword ptr [rcx + 8]
00219BDC  lea      rsi, [rcx + 8]
00219BE0  xor      edi, edi
00219BE2  mov      r15, r8
00219BE5  mov      ebp, edx
00219BE7  cmp      rbx, rsi
00219BEA  je       0x219c01  ; -> 00219C01
00219BEC  nop      dword ptr [rax]
00219BF0  mov      rdi, qword ptr [rbx + 0x10]
00219BF4  cmp      dword ptr [rdi + 0x38], ebp
00219BF7  je       0x219c01  ; -> 00219C01
00219BF9  mov      rbx, qword ptr [rbx]
00219BFC  cmp      rbx, rsi
00219BFF  jne      0x219bf0  ; -> 00219BF0
00219C01  call     0x212950  ; -> 00212950 fn
00219C06  mov      r14d, eax
00219C09  cmp      rbx, rsi
00219C0C  je       0x219c21  ; -> 00219C21
00219C0E  mov      r9, r15
00219C11  mov      r8d, ebp
00219C14  mov      edx, eax
00219C16  mov      rcx, rdi
00219C19  call     0x223030  ; -> 00223030 fn
00219C1E  mov      eax, r14d
00219C21  mov      rbx, qword ptr [rsp + 0x40]
00219C26  mov      rbp, qword ptr [rsp + 0x48]
00219C2B  mov      rsi, qword ptr [rsp + 0x50]
00219C30  add      rsp, 0x20
00219C34  pop      r15
00219C36  pop      r14
00219C38  pop      rdi
00219C39  ret      
```
