# Homing pack: `16-UI/Handbook/the-handbooks-monster-viewer.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-handbooks-monster-viewer.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003A2C80 (251 B, extent 003A2C80-003A2D7B)

Entered from (direct sites whose caller this page cites): `004781A0` + 0x31 (call; `004781A0` is cited on this page)
Other direct sites: none

Host context: "falsification   last_pass_state: opus-monster-viewer-falsification-pass-1   crossref_clean: true   reopened_count: 0   note: written by FABLE. Started from two of FRONTIER's uncited bodies (004781E0, 004781A0) and one flag nobody had     named (render record +0x6E0). Static. Corrects the 2026-09-12 Y-7 answer of mine that the gallery file's reader was     "not found", and answers the settings page's residue "what that handle is". Not re"

```
003A2C80  mov      qword ptr [rsp + 0x10], rbx
003A2C85  mov      qword ptr [rsp + 0x18], rbp
003A2C8A  mov      qword ptr [rsp + 0x20], rsi
003A2C8F  push     r14
003A2C91  sub      rsp, 0x20
003A2C95  mov      r10, qword ptr [rip + 0x2bec634]  ; -> 02F8F2D0
003A2C9C  lea      eax, [r8 + 0xf]
003A2CA0  mov      rbp, rdx
003A2CA3  mov      r11d, r9d
003A2CA6  cdq      
003A2CA7  mov      esi, r8d
003A2CAA  and      edx, 0xf
003A2CAD  add      eax, edx
003A2CAF  sar      eax, 4
003A2CB2  movsxd   rbx, eax
003A2CB5  test     r8d, r8d
003A2CB8  je       0x3a2cd1  ; -> 003A2CD1
003A2CBA  mov      r9, rbx
003A2CBD  shl      r9, 4
003A2CC1  add      r9, r10
003A2CC4  cmp      r9, qword ptr [rip + 0x2bec60d]  ; -> 02F8F2D8
003A2CCB  jae      0x3a2d65  ; -> 003A2D65
003A2CD1  movzx    r8d, word ptr [rip + 0x2bec5ed]  ; -> 02F8F2C6
003A2CD9  mov      rax, qword ptr [rip + 0x2bec618]  ; -> 02F8F2F8
003A2CE0  mov      qword ptr [rsp + 0x30], rdi
003A2CE5  lea      rdx, [r8 + r8*4]
003A2CE9  inc      r8w
003A2CED  lea      rdi, [rax + rdx*8]
003A2CF1  mov      word ptr [rip + 0x2bec5cd], r8w  ; -> 02F8F2C6
003A2CF9  mov      eax, dword ptr [rsp + 0x50]
003A2CFD  mov      qword ptr [rdi], r10
003A2D00  mov      dword ptr [rdi + 8], eax
003A2D03  mov      byte ptr [rdi + 0xb], r11b
003A2D07  mov      dword ptr [rdi + 0xc], esi
003A2D0A  mov      qword ptr [rdi + 0x10], rcx
003A2D0E  call     0x24e460  ; -> 0024E460 fn
003A2D13  test     eax, eax
003A2D15  jne      0x3a2d23  ; -> 003A2D23
003A2D17  cmp      dword ptr [rip + 0x274c6fb], eax  ; -> 02AEF418
003A2D1D  jne      0x3a2d23  ; -> 003A2D23
003A2D1F  xor      ecx, ecx
003A2D21  jmp      0x3a2d28  ; -> 003A2D28
003A2D23  mov      ecx, 1
003A2D28  mov      eax, dword ptr [rip + 0x274c6ee]  ; -> 02AEF41C
003A2D2E  add      eax, eax
003A2D30  or       eax, ecx
003A2D32  add      eax, eax
003A2D34  mov      dword ptr [rdi + 0x20], eax
003A2D37  mov      rdi, qword ptr [rsp + 0x30]
003A2D3C  test     esi, esi
003A2D3E  je       0x3a2d65  ; -> 003A2D65
003A2D40  mov      rcx, qword ptr [rip + 0x2bec589]  ; -> 02F8F2D0
003A2D47  mov      eax, ebx
003A2D49  shl      eax, 4
003A2D4C  mov      rdx, rbp
003A2D4F  movsxd   r8, eax
003A2D52  call     0x861eba  ; -> 00861EBA fn
003A2D57  mov      rax, rbx
003A2D5A  shl      rax, 4
003A2D5E  add      qword ptr [rip + 0x2bec56b], rax  ; -> 02F8F2D0
003A2D65  mov      rbx, qword ptr [rsp + 0x38]
003A2D6A  mov      rbp, qword ptr [rsp + 0x40]
003A2D6F  mov      rsi, qword ptr [rsp + 0x48]
003A2D74  add      rsp, 0x20
003A2D78  pop      r14
003A2D7A  ret      
```

## 00504700 (51 B, extent 00504700-00504733)

Entered from (direct sites whose caller this page cites): `00477F20` + 0xE6 (call; `00477F20` is cited on this page)
Other direct sites: none

Host context: "ods 001EB7B0, 001EB9C0 and     001EB940, the staged loader 002EE430 with its request 002EE9C0, close 002EEB20, hand-over 002EED80 and per-tick tail     002EF050, and the model-instance container pass 00477F20 with its two callbacks disassembled from the authority     image and read whole, 2026-09-19; the entry reader 001C6320 read at its head, its tail and every call in between     (the light arithmetic 001C65A0..001C6940 by its calls o"

```
00504700  push     rbx
00504702  sub      rsp, 0x20
00504706  test     byte ptr [rcx + 0x244], 0x10
0050470D  mov      rbx, rcx
00504710  je       0x50471f  ; -> 0050471F
00504712  mov      edx, 1
00504717  mov      r8d, edx
0050471A  call     0x53d780  ; -> 0053D780 fn
0050471F  xor      r8d, r8d
00504722  mov      rcx, rbx
00504725  lea      edx, [r8 + 1]
00504729  add      rsp, 0x20
0050472D  pop      rbx
0050472E  jmp      0x53d780  ; -> 0053D780 fn
```
