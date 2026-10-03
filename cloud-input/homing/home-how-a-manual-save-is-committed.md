# Homing pack: `19-Save-Load-Settings/how-a-manual-save-is-committed.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-how-a-manual-save-is-committed.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003BB2F0 (48 B, extent 003BB2F0-003BB320)

Entered from (direct sites whose caller this page cites): `00582040` + 0x1B8 (call; `00582040` is cited on this page)
Other direct sites: none

Host context: "0 and     005826D0, the asset-name builder 005837F0 and the storage layer's delete routine 00862130 disassembled from the     authority image and read whole, 2026-09-19; the queue's per-kind dispatch 00582040 and the storage machine's     command dispatch in 003BB790 read for the three kinds this transaction uses; the CRT imports resolved by name from     the import table last_reviewed: 2026-09-29 audit:   passes: 1   last_pass: 2026-09"

```
003BB2F0  xor      eax, eax
003BB2F2  mov      dword ptr [rip + 0x2785b20], 7  ; -> 02B40E1C
003BB2FC  xor      ecx, ecx
003BB2FE  mov      dword ptr [rip + 0x2785bbc], eax  ; -> 02B40EC0
003BB304  mov      dword ptr [rip + 0x2785b0e], eax  ; -> 02B40E18
003BB30A  mov      dword ptr [rip + 0x2785cd4], eax  ; -> 02B40FE4
003BB310  mov      qword ptr [rip + 0x2785af5], 1  ; -> 02B40E10
003BB31B  jmp      0x3ba5f0  ; -> 003BA5F0 fn
```

## 003BB380 (38 B, extent 003BB380-003BB3A6)

Entered from (direct sites whose caller this page cites): `00582040` + 0x1C2 (call; `00582040` is cited on this page)
Other direct sites: `0050C5E0` + 0x0 (jmp)

Host context: "0 and     005826D0, the asset-name builder 005837F0 and the storage layer's delete routine 00862130 disassembled from the     authority image and read whole, 2026-09-19; the queue's per-kind dispatch 00582040 and the storage machine's     command dispatch in 003BB790 read for the three kinds this transaction uses; the CRT imports resolved by name from     the import table last_reviewed: 2026-09-29 audit:   passes: 1   last_pass: 2026-09"

```
003BB380  xor      eax, eax
003BB382  mov      dword ptr [rip + 0x2785a90], 3  ; -> 02B40E1C
003BB38C  mov      dword ptr [rip + 0x2785b2e], eax  ; -> 02B40EC0
003BB392  mov      dword ptr [rip + 0x2785c4c], eax  ; -> 02B40FE4
003BB398  mov      qword ptr [rip + 0x2785a75], rax  ; -> 02B40E14
003BB39F  mov      dword ptr [rip + 0x2785a6b], eax  ; -> 02B40E10
003BB3A5  ret      
```

## 003BB3B0 (38 B, extent 003BB3B0-003BB3D6)

Entered from (direct sites whose caller this page cites): `00582040` + 0xC9 (call; `00582040` is cited on this page)
Other direct sites: `0050C950` + 0x0 (jmp)

Host context: "0 and     005826D0, the asset-name builder 005837F0 and the storage layer's delete routine 00862130 disassembled from the     authority image and read whole, 2026-09-19; the queue's per-kind dispatch 00582040 and the storage machine's     command dispatch in 003BB790 read for the three kinds this transaction uses; the CRT imports resolved by name from     the import table last_reviewed: 2026-09-29 audit:   passes: 1   last_pass: 2026-09"

```
003BB3B0  xor      eax, eax
003BB3B2  mov      dword ptr [rip + 0x2785a60], 4  ; -> 02B40E1C
003BB3BC  mov      dword ptr [rip + 0x2785afe], eax  ; -> 02B40EC0
003BB3C2  mov      dword ptr [rip + 0x2785c1c], eax  ; -> 02B40FE4
003BB3C8  mov      qword ptr [rip + 0x2785a45], rax  ; -> 02B40E14
003BB3CF  mov      dword ptr [rip + 0x2785a3b], eax  ; -> 02B40E10
003BB3D5  ret      
```

## 003BB6A0 (133 B, extent 003BB6A0-003BB725)

Entered from (direct sites whose caller this page cites): `00582040` + 0xFF (call; `00582040` is cited on this page)
Other direct sites: none

Host context: "0 and     005826D0, the asset-name builder 005837F0 and the storage layer's delete routine 00862130 disassembled from the     authority image and read whole, 2026-09-19; the queue's per-kind dispatch 00582040 and the storage machine's     command dispatch in 003BB790 read for the three kinds this transaction uses; the CRT imports resolved by name from     the import table last_reviewed: 2026-09-29 audit:   passes: 1   last_pass: 2026-09"

```
003BB6A0  sub      rsp, 0x28
003BB6A4  cmp      ecx, 0xc7
003BB6AA  ja       0x3bb71e  ; -> 003BB71E
003BB6AC  mov      rax, qword ptr [rdx]
003BB6AF  lea      r10, [rip + 0x278510a]  ; -> 02B407C0
003BB6B6  movsxd   r9, ecx
003BB6B9  lea      rdx, [rip + 0x2785768]  ; -> 02B40E28
003BB6C0  sub      rdx, r8
003BB6C3  mov      qword ptr [r10 + r9*8], rax
003BB6C7  nop      word ptr [rax + rax]
003BB6D0  movzx    eax, byte ptr [r8]
003BB6D4  mov      byte ptr [rdx + r8], al
003BB6D8  lea      r8, [r8 + 1]
003BB6DC  test     al, al
003BB6DE  jne      0x3bb6d0  ; -> 003BB6D0
003BB6E0  mov      dword ptr [rip + 0x2784e72], ecx  ; -> 02B40558
003BB6E6  xor      ecx, ecx
003BB6E8  mov      dword ptr [rip + 0x27857d2], ecx  ; -> 02B40EC0
003BB6EE  mov      dword ptr [rip + 0x2785724], ecx  ; -> 02B40E18
003BB6F4  mov      dword ptr [rip + 0x27858ea], ecx  ; -> 02B40FE4
003BB6FA  mov      dword ptr [rip + 0x2785718], 8  ; -> 02B40E1C
003BB704  mov      qword ptr [rip + 0x2785701], 1  ; -> 02B40E10
003BB70F  call     0x3ba720  ; -> 003BA720 fn
003BB714  mov      eax, 1
003BB719  add      rsp, 0x28
003BB71D  ret      
003BB71E  xor      eax, eax
003BB720  add      rsp, 0x28
003BB724  ret      
```
