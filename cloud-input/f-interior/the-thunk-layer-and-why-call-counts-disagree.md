# F-interior pack: `24-Compiler-And-CRT-Runtime/Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md`

Generated 2026-10-02 18:33 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-thunk-layer-and-why-call-counts-disagree.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 002C9040 (21 B, extent 002C9040-002C9055)

Page context: "rior anchor '00249196' (the '[+0x10]' write).  '002C8EE0' (348 B) is the builder '00253780' calls: loops filling 7-wide stack records ('edx = rdi + 0x74', '0024AB90' per entry) into '0209E640', with '002C9040' taken by address and '00249810'/'0032E620' finishing - the thunk-adjacent record constructor.  Interior anchor '002C8F2F' (function '002C8EE0').  '0017D260' (12 B) is the '_aligned_malloc' call-site shim: 'r9d = -1', 'r8d = 0', ta"

```
002C9040  movsxd   rax, ecx
002C9043  lea      rcx, [rip + 0x1dd55ee]  ; -> 0209E638
002C904A  add      rax, rax
002C904D  mov      dword ptr [rcx + rax*8], 0
002C9054  ret      
```

## 002CEAE0 (82 B, extent 002CEAE0-002CEB32)

Page context: "rior anchor '00273B6C' (the relink).  ## SWE2-EC7-106 update (2026-09-20) - '00249180' measured  '00249180' (35 B) is the forwarding thunk '002467A0', '00253780', '00280750', '002808D0', '0029DC90', '002CEAE0', '003158B0', '0035C5B0' and '003C1F00' call: it moves '[rsp + 0x60]' into the argument stack and calls '00249210', then writes the second incoming stack argument '[rsp + 0x68]' into '[rax + 0x10]' and answers 'qword[rax + 8]' - th"

```
002CEAE0  sub      rsp, 0x38
002CEAE4  mov      rax, qword ptr [rip + 0x1dcc145]  ; -> 0209AC30
002CEAEB  test     byte ptr [rax + 0xd3c], 2
002CEAF2  je       0x2ceb2d  ; -> 002CEB2D
002CEAF4  movzx    r8d, byte ptr [rax + 0xb2d]
002CEAFC  mov      edx, 7
002CEB01  add      r8d, 0x10
002CEB05  mov      qword ptr [rsp + 0x28], 0
002CEB0E  mov      dword ptr [rsp + 0x20], 1
002CEB16  lea      r9d, [rdx - 5]
002CEB1A  call     0x249180  ; -> 00249180 fn
002CEB1F  mov      rcx, qword ptr [rip + 0x1dcc10a]  ; -> 0209AC30
002CEB26  mov      qword ptr [rcx + 0x3c0], rax
002CEB2D  add      rsp, 0x38
002CEB31  ret      
```

## 0037B2C0 (41 B, extent 0037B2C0-0037B2E9)

Page context: "t) | interior | | --- | --- | --- | | '002EA880' | '003D8D60' | ['002EA880'](../../_index/ADDRESS-INDEX.md) | | '002EAA50' | '003B5440' | ['002EAA50'](../../_index/ADDRESS-INDEX.md) | | '002ECE40' | '0037B2C0' | ['002ECE40'](../../_index/ADDRESS-INDEX.md) |  ## The '003DD220'/'00473B20' exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)  | root | member (target) | role | interior | | --- | --- | --- | --- | | '003"

```
0037B2C0  cmp      ecx, 5
0037B2C3  jge      0x37b2e8  ; -> 0037B2E8
0037B2C5  movsxd   rax, ecx
0037B2C8  lea      rcx, [rax + rax*4]
0037B2CC  add      rcx, rcx
0037B2CF  lea      rax, [rip + 0x2b4414a]  ; -> 02EBF420
0037B2D6  movss    dword ptr [rax + rcx*8 + 0x40], xmm1
0037B2DC  movss    dword ptr [rax + rcx*8 + 0x44], xmm2
0037B2E2  movss    dword ptr [rax + rcx*8 + 0x48], xmm3
0037B2E8  ret      
```

## 003B5440 (37 B, extent 003B5440-003B5465)

Page context: " is 5 B, and its census member is the target body:  | root | member (target) | interior | | --- | --- | --- | | '002EA880' | '003D8D60' | ['002EA880'](../../_index/ADDRESS-INDEX.md) | | '002EAA50' | '003B5440' | ['002EAA50'](../../_index/ADDRESS-INDEX.md) | | '002ECE40' | '0037B2C0' | ['002ECE40'](../../_index/ADDRESS-INDEX.md) |  ## The '003DD220'/'00473B20' exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)  | r"

```
003B5440  movzx    edx, byte ptr [rip + 0x278b0d1]  ; -> 02B40518
003B5447  mov      eax, edx
003B5449  and      eax, 1
003B544C  cmp      eax, ecx
003B544E  je       0x3b5464  ; -> 003B5464
003B5450  movzx    eax, dl
003B5453  xor      al, cl
003B5455  and      al, 1
003B5457  xor      dl, al
003B5459  mov      byte ptr [rip + 0x278b0b9], dl  ; -> 02B40518
003B545F  jmp      0x3b4fd0  ; -> 003B4FD0 fn
003B5464  ret      
```
