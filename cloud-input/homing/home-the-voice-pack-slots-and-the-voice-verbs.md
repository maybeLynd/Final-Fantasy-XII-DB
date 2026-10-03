# Homing pack: `18-Audio/the-voice-pack-slots-and-the-voice-verbs.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-voice-pack-slots-and-the-voice-verbs.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003EA2C0 (107 B, extent 003EA2C0-003EA32B)

Entered from (direct sites whose caller this page cites): `00351EB0` + 0x1E (jmp; `00351EB0` is cited on this page)
Other direct sites: none

Host context: "e and writes −1 to the slot's '+0x08' word; a pending cue without a handle is re-asked through '003E9A10' and dropped when the stream says no.  ### 2.4 Stop, pan, dispose  - **'voicestop'** ('0088', '00351EB0' → '003EA2C0(slot, cue)'): waits for the cue's handle   ('003EA3E0' polls '002DEE90', yielding through '0035EA30'), closes the stream ('002DF690') and   clears the pending bit and both words. - **'voicepan'** ('00B1', '00352E80' → "

```
003EA2C0  mov      qword ptr [rsp + 8], rbx
003EA2C5  push     rdi
003EA2C6  sub      rsp, 0x20
003EA2CA  movsxd   rbx, ecx
003EA2CD  lea      rax, [rip + 0x2772ddc]  ; -> 02B5D0B0
003EA2D4  shl      rbx, 6
003EA2D8  add      rbx, rax
003EA2DB  mov      edi, edx
003EA2DD  call     0x2debb0  ; -> 002DEBB0 fn
003EA2E2  cmp      byte ptr [rbx + 4], 3
003EA2E6  movsxd   rcx, eax
003EA2E9  mov      r8, qword ptr [rbx + rcx*8 + 0x20]
003EA2EE  mov      qword ptr [rbx + 0x30], r8
003EA2F2  jne      0x3ea320  ; -> 003EA320
003EA2F4  test     r8, r8
003EA2F7  je       0x3ea320  ; -> 003EA320
003EA2F9  cmp      dword ptr [r8 + 4], edi
003EA2FD  jbe      0x3ea320  ; -> 003EA320
003EA2FF  mov      ebx, edi
003EA301  shl      rbx, 4
003EA305  add      rbx, r8
003EA308  mov      edx, dword ptr [rbx + 0x10]
003EA30B  mov      ecx, dword ptr [rbx + 0x14]
003EA30E  call     0x3ea3e0  ; -> 003EA3E0 fn
003EA313  xor      eax, eax
003EA315  and      dword ptr [rbx + 8], 0x7fffffff
003EA31C  mov      qword ptr [rbx + 0x10], rax
003EA320  mov      rbx, qword ptr [rsp + 0x30]
003EA325  add      rsp, 0x20
003EA329  pop      rdi
003EA32A  ret      
```
