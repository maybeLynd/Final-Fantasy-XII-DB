# Homing pack: `99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-cutscene-name-slots-and-the-depth-of-field-sidecar.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002E4150 (377 B, extent 002E4150-002E42C9)

Entered from (direct sites whose caller this page cites): `0034E6D0` + 0x35 (jmp; `0034E6D0` is cited on this page)
Other direct sites: `00267D40` + 0x3C (call)

Host context: "2DA0' is called by '003413E0'; '001EC500' is called by '00352F00'; '001EC520' is called by '003526F0'; '001EC540' is called by '00352B30'; '001EC620' is called by '0034C7E0'; '002260E0' is called by '0034E6D0'; '00229EA0' is called by '00354D00'; '00265860' is called by '0034D790'; '00265880' is called by '0034CF90'; '002B5B60' is called by '00341030'; '002B5C90' is called by '003413E0'; '002E1290' is called by '0034B290'; '002E12B0' is"

```
002E4150  mov      qword ptr [rsp + 8], rbx
002E4155  mov      qword ptr [rsp + 0x10], rbp
002E415A  mov      qword ptr [rsp + 0x18], rsi
002E415F  mov      qword ptr [rsp + 0x20], rdi
002E4164  push     r12
002E4166  push     r14
002E4168  push     r15
002E416A  sub      rsp, 0x20
002E416E  mov      r15d, edx
002E4171  mov      r12d, ecx
002E4174  xor      r14d, r14d
002E4177  mov      ecx, r14d
002E417A  call     0x263ff0  ; -> 00263FF0 fn
002E417F  mov      rbp, rax
002E4182  test     byte ptr [rax + 0x10], 1
002E4186  je       0x2e429d  ; -> 002E429D
002E418C  movzx    edi, word ptr [rax + 0x1de]
002E4193  movzx    esi, word ptr [rax + 0x1d6]
002E419A  add      esi, edi
002E419C  test     r12d, r12d
002E419F  je       0x2e425a  ; -> 002E425A
002E41A5  cmp      r12d, 1
002E41A9  jne      0x2e429d  ; -> 002E429D
002E41AF  cmp      edi, esi
002E41B1  jae      0x2e429d  ; -> 002E429D
002E41B7  nop      word ptr [rax + rax]
002E41C0  mov      edx, edi
002E41C2  mov      rcx, rbp
002E41C5  call     0x358940  ; -> 00358940 fn
002E41CA  mov      rdx, rax
002E41CD  test     r14d, r14d
002E41D0  jne      0x2e41e5  ; -> 002E41E5
002E41D2  movzx    ecx, byte ptr [rax + 3]
002E41D6  xor      r8d, r8d
002E41D9  and      cl, 0x1f
002E41DC  cmp      cl, 6
002E41DF  setne    r8b
002E41E3  jmp      0x2e41eb  ; -> 002E41EB
002E41E5  mov      r8d, 1
002E41EB  xor      eax, eax
002E41ED  test     r15d, r15d
002E41F0  cmovne   eax, r8d
002E41F4  test     eax, eax
002E41F6  je       0x2e424e  ; -> 002E424E
002E41F8  cmp      byte ptr [rdx + 0x18], 1
002E41FC  je       0x2e424e  ; -> 002E424E
002E41FE  mov      rax, qword ptr [rdx + 0xc0]
002E4205  test     rax, rax
002E4208  je       0x2e424e  ; -> 002E424E
002E420A  cmp      dword ptr [rax], -1
002E420D  je       0x2e424e  ; -> 002E424E
002E420F  movzx    ecx, word ptr [rax]
002E4212  cmp      cx, -1
002E4216  jne      0x2e421c  ; -> 002E421C
002E4218  xor      eax, eax
002E421A  jmp      0x2e4246  ; -> 002E4246
002E421C  movsx    rax, cx
002E4220  imul     rcx, rax, 0x740
002E4227  add      rcx, qword ptr [rip + 0x1fe2cfa]  ; -> 022C6F28
002E422E  jne      0x2e4234  ; -> 002E4234
002E4230  xor      eax, eax
002E4232  jmp      0x2e4246  ; -> 002E4246
002E4234  cmp      dword ptr [rcx + 0x284], 0
002E423B  jne      0x2e4241  ; -> 002E4241
002E423D  xor      eax, eax
002E423F  jmp      0x2e4246  ; -> 002E4246
002E4241  call     0x3e6da0  ; -> 003E6DA0 fn
002E4246  mov      rcx, rax
002E4249  call     0x3e0860  ; -> 003E0860 fn
002E424E  inc      edi
002E4250  cmp      edi, esi
002E4252  jl       0x2e41c0  ; -> 002E41C0
002E4258  jmp      0x2e429d  ; -> 002E429D
002E425A  cmp      edi, esi
002E425C  jae      0x2e429d  ; -> 002E429D
002E425E  nop      
002E4260  mov      edx, edi
002E4262  mov      rcx, rbp
002E4265  call     0x358940  ; -> 00358940 fn
002E426A  test     rax, rax
002E426D  je       0x2e4297  ; -> 002E4297
002E426F  mov      rbx, qword ptr [rax + 0xc0]
002E4276  test     rbx, rbx
002E4279  je       0x2e4297  ; -> 002E4297
002E427B  cmp      dword ptr [rbx], -1
002E427E  je       0x2e4297  ; -> 002E4297
002E4280  test     r15d, r15d
002E4283  je       0x2e4293  ; -> 002E4293
002E4285  cmp      byte ptr [rbx + 0x11], 0x80
002E4289  jb       0x2e4293  ; -> 002E4293
002E428B  movzx    ecx, word ptr [rbx]
002E428E  call     0x426520  ; -> 00426520 fn
002E4293  and      byte ptr [rbx + 0x11], 0x7f
002E4297  inc      edi
002E4299  cmp      edi, esi
002E429B  jl       0x2e4260  ; -> 002E4260
002E429D  inc      r14d
002E42A0  cmp      r14d, 3
002E42A4  jl       0x2e4177  ; -> 002E4177
002E42AA  mov      rbx, qword ptr [rsp + 0x40]
002E42AF  mov      rbp, qword ptr [rsp + 0x48]
002E42B4  mov      rsi, qword ptr [rsp + 0x50]
002E42B9  mov      rdi, qword ptr [rsp + 0x58]
002E42BE  add      rsp, 0x20
002E42C2  pop      r15
002E42C4  pop      r14
002E42C6  pop      r12
002E42C8  ret      
```

## 002EC960 (15 B, extent 002EC960-002EC96F)

Entered from (direct sites whose caller this page cites): `003417F0` + 0x3A (call; `003417F0` is cited on this page)
Other direct sites: none

Host context: "'0026D6D0').  **Script_VM_Native_Bridge — MECHANICAL, 136 edges.** '00267310' is called by '0033F330', '00340260', '00340FA0', '00341590' and 52 more; '003EB720' is called by '0033FAD0', '00340530', '003417F0', '00347B00' and 15 more; '002EFA70' is called by '003559B0', '00355EB0', '00356270', '00356650' and 2 more; 'WorldActor_UpdateRuntimeAndScriptExecutionState' ('0025DF00') calls 'WorldActorScriptVM_InterpretBytecode' ('0025E4C0'), "

```
002EC960  test     rcx, rcx
002EC963  je       0x2ec96e  ; -> 002EC96E
002EC965  cmp      dword ptr [rcx], -1
002EC968  je       0x2ec96e  ; -> 002EC96E
002EC96A  mov      word ptr [rcx + 0x2a], dx
002EC96E  ret      
```

## 003DD980 (147 B, extent 003DD980-003DDA13)

Entered from (direct sites whose caller this page cites): `00347B00` + 0x95 (call; `00347B00` is cited on this page)
Other direct sites: none

Host context: "  **Script_VM_Native_Bridge — MECHANICAL, 136 edges.** '00267310' is called by '0033F330', '00340260', '00340FA0', '00341590' and 52 more; '003EB720' is called by '0033FAD0', '00340530', '003417F0', '00347B00' and 15 more; '002EFA70' is called by '003559B0', '00355EB0', '00356270', '00356650' and 2 more; 'WorldActor_UpdateRuntimeAndScriptExecutionState' ('0025DF00') calls 'WorldActorScriptVM_InterpretBytecode' ('0025E4C0'), 'ScriptVM_Wa"

```
003DD980  mov      qword ptr [rsp + 8], rbx
003DD985  mov      qword ptr [rsp + 0x10], rbp
003DD98A  mov      qword ptr [rsp + 0x18], rsi
003DD98F  push     rdi
003DD990  sub      rsp, 0x30
003DD994  movsxd   rbx, edx
003DD997  mov      rdi, rcx
003DD99A  mov      r10, rbx
003DD99D  movsxd   rsi, r8d
003DD9A0  shl      r10, 4
003DD9A4  lea      rcx, [rip + 0x277a7f9]  ; -> 02B581A4
003DD9AB  add      r10, rsi
003DD9AE  mov      ebp, r9d
003DD9B1  imul     rax, r10, 0x1c
003DD9B5  cmp      dword ptr [rax + rcx], 4
003DD9B9  jne      0x3dd9fe  ; -> 003DD9FE
003DD9BB  mov      rcx, rdi
003DD9BE  call     0x2e95b0  ; -> 002E95B0 fn
003DD9C3  movaps   xmm1, xmm0
003DD9C6  mov      rcx, rdi
003DD9C9  call     0x2e4fa0  ; -> 002E4FA0 fn
003DD9CE  xor      edx, edx
003DD9D0  mov      rcx, rdi
003DD9D3  call     0x2e81d0  ; -> 002E81D0 fn
003DD9D8  movss    xmm0, dword ptr [rsp + 0x60]
003DD9DE  xor      r9d, r9d
003DD9E1  shl      ebx, 4
003DD9E4  mov      rdx, rdi
003DD9E7  or       ebx, esi
003DD9E9  movss    dword ptr [rsp + 0x20], xmm0
003DD9EF  shl      ebx, 0x10
003DD9F2  xor      ecx, ecx
003DD9F4  or       ebx, ebp
003DD9F6  mov      r8d, ebx
003DD9F9  call     0x2eb0d0  ; -> 002EB0D0 fn
003DD9FE  mov      rbx, qword ptr [rsp + 0x40]
003DDA03  mov      rbp, qword ptr [rsp + 0x48]
003DDA08  mov      rsi, qword ptr [rsp + 0x50]
003DDA0D  add      rsp, 0x30
003DDA11  pop      rdi
003DDA12  ret      
```
