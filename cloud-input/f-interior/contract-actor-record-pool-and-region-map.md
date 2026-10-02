# F-interior pack: `04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-actor-record-pool-and-region-map.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ). OPUS read these before packing.

## 0026ADF0 (49 B, extent 0026ADF0-0026AE21)

Page context: "character turns](../06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md).   So '(entry+0x08, entry+0x06)' is the same actor-reference pair 'Movement_SetSteeringTargetActorRef'   ('0026ADF0') stores as '(+0x04, +0x00)', and the house name for this half is already 'ordinal'   ('ActorWaitSlot +0x24 targetOrdinal'). **'0x8000' is the "no actor" sentinel**: the free-list build   seeds the dword at '+0x04' with '0x80000000"

```
0026ADF0  movzx    eax, byte ptr [rcx + 3]
0026ADF4  and      al, 0xe0
0026ADF6  cmp      al, 0x60
0026ADF8  jne      0x26ae20  ; -> 0026AE20
0026ADFA  mov      rcx, qword ptr [rcx + 0xb8]
0026AE01  mov      rax, qword ptr [rcx + 0xf0]
0026AE08  mov      dword ptr [rax], edx
0026AE0A  mov      rax, qword ptr [rcx + 0xf0]
0026AE11  mov      dword ptr [rax + 4], r8d
0026AE15  mov      rax, qword ptr [rcx + 0xf0]
0026AE1C  mov      byte ptr [rax + 0x2a], 1
0026AE20  ret      
```

## 0030BFB0 (96 B, extent 0030BFB0-0030C010)

Page context: "by   '00319F50'/'00325260' — battle-side fan-in on the shared apply and reducer helpers. - **Gameplay — CLIENT and SERVICE (4 edges).** '0025D9E0' calls '00234150'; the '00268530'   apply-pass calls '0030BFB0', which itself reaches '00308040'; '003589B0' is also called by   '0031ADB0'. Shared-helper traffic in both directions. - **Movement — CLIENT and SERVICE (19 edges).** The pool helpers are movement-adjacent:   '0025D9E0' calls '002"

```
0030BFB0  sub      rsp, 0x28
0030BFB4  call     0x31b760  ; -> 0031B760 fn
0030BFB9  mov      rcx, rax
0030BFBC  test     rax, rax
0030BFBF  je       0x30c009  ; -> 0030C009
0030BFC1  test     byte ptr [rax], 0x10
0030BFC4  je       0x30c009  ; -> 0030C009
0030BFC6  mov      rdx, qword ptr [rax + 0x698]
0030BFCD  mov      eax, dword ptr [rdx + 0x64]
0030BFD0  or       eax, dword ptr [rdx + 0x3c]
0030BFD3  test     eax, 0x8000201b
0030BFD8  je       0x30bfe8  ; -> 0030BFE8
0030BFDA  mov      eax, dword ptr [rcx]
0030BFDC  shr      rax, 0x17
0030BFE0  and      eax, 1
0030BFE3  add      rsp, 0x28
0030BFE7  ret      
0030BFE8  test     rdx, rdx
0030BFEB  je       0x30bffe  ; -> 0030BFFE
0030BFED  movzx    eax, byte ptr [rdx + 5]
0030BFF1  test     eax, eax
0030BFF3  jne      0x30bffe  ; -> 0030BFFE
0030BFF5  add      rsp, 0x28
0030BFF9  jmp      0x308130  ; -> 00308130 fn
0030BFFE  xor      edx, edx
0030C000  add      rsp, 0x28
0030C004  jmp      0x308040  ; -> 00308040 fn
0030C009  xor      eax, eax
0030C00B  add      rsp, 0x28
0030C00F  ret      
```

## 003DC0D0 (93 B, extent 003DC0D0-003DC12D)

Page context: "easing" — right   about the branch, silent about the value. The value is an **actor ordinal**. '003DB366'–'003DB37F'   gates on 'cmp word [rdi+6], 0x8000' *and* 'byte [rdi+0x10] == 3' before calling '003DC0D0', which   passes 'word [entry+6]' as argument 2 and 'dword [entry+8]' as argument 1 to the resolver   '003587C0'. That resolver is 'movsxd rbx, edx' / '00263FF0' / 'mov rcx, [rax+8]' / reject   negative / reject '>= [rcx]' / 'mov r"

```
003DC0D0  push     rbx
003DC0D2  sub      rsp, 0x40
003DC0D6  mov      rbx, rdx
003DC0D9  movzx    edx, word ptr [rdx + 6]
003DC0DD  mov      ecx, dword ptr [rbx + 8]
003DC0E0  call     0x3587c0  ; -> 003587C0 fn
003DC0E5  test     rax, rax
003DC0E8  je       0x3dc127  ; -> 003DC127
003DC0EA  movzx    ecx, byte ptr [rbx + 3]
003DC0EE  lea      rdx, [rsp + 0x20]
003DC0F3  mov      byte ptr [rsp + 0x22], cl
003DC0F7  mov      r8d, 1
003DC0FD  mov      ecx, dword ptr [rbx + 0xc]
003DC100  mov      dword ptr [rsp + 0x30], ecx
003DC104  mov      ecx, dword ptr [rbx + 8]
003DC107  mov      dword ptr [rsp + 0x2c], ecx
003DC10B  mov      rcx, rax
003DC10E  mov      word ptr [rsp + 0x20], 0x402
003DC115  mov      dword ptr [rsp + 0x24], 0x80000000
003DC11D  mov      byte ptr [rsp + 0x28], 1
003DC122  call     0x3dbcf0  ; -> 003DBCF0 fn
003DC127  add      rsp, 0x40
003DC12B  pop      rbx
003DC12C  ret      
```
