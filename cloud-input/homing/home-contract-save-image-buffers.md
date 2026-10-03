# Homing pack: `19-Save-Load-Settings/CONTRACT-save-image-buffers.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-save-image-buffers.json`.

Bodies: 5. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 005DE310 (63 B, extent 005DE310-005DE34F)

Entered from (direct sites whose caller this page cites): `00616CC0` + 0x58 (jmp; `00616CC0` is cited on this page)
Other direct sites: `00610EC0` + 0x54 (call)

Host context: "rs of 'rcx' in order: '006167C0(rcx+0x568)'; for 'rcx+0x218' '0062C100' only when '00625F20' returns non-zero, then '00616D20'; for 'rcx+0x188' '0062BF40' only when '00625F10' returns non-zero, then '00616CC0'; for 'rcx' itself '0062BCB0' only when '00625F00' returns non-zero, then '00616C60' | '005DDBCE', '005DDBDB', '005DDC06', '005DDC2D', '005DDC43' | "

```
005DE310  push     rbx
005DE312  sub      rsp, 0x30
005DE316  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005DE31F  mov      rbx, rcx
005DE322  cmp      byte ptr [rcx + 8], 0
005DE326  je       0x5de33a  ; -> 005DE33A
005DE328  lea      rdx, [rip + 0x76d021]  ; -> 00D4B350
005DE32F  mov      ecx, 3
005DE334  call     0x5cdaa0  ; -> 005CDAA0 fn
005DE339  nop      
005DE33A  mov      rcx, qword ptr [rbx + 0x20]
005DE33E  test     rcx, rcx
005DE341  je       0x5de349  ; -> 005DE349
005DE343  call     0x6108c0  ; -> 006108C0 fn
005DE348  nop      
005DE349  add      rsp, 0x30
005DE34D  pop      rbx
005DE34E  ret      
```

## 005DE390 (63 B, extent 005DE390-005DE3CF)

Entered from (direct sites whose caller this page cites): `00616D20` + 0x58 (jmp; `00616D20` is cited on this page)
Other direct sites: `00612B20` + 0x54 (call)

Host context: ", '001AA1D1', '001AA203', '001AA208' | | '005DDBB0' | 164 B | tears down four members of 'rcx' in order: '006167C0(rcx+0x568)'; for 'rcx+0x218' '0062C100' only when '00625F20' returns non-zero, then '00616D20'; for 'rcx+0x188' '0062BF40' only when '00625F10' returns non-zero, then '00616CC0'; for 'rcx' itself '0062BCB0' only when '00625F00' returns non-zero, then '00616C60' | '005DDBCE', '005DDBDB', '005DDC06', '005DDC2D', '005DDC43' | "

```
005DE390  push     rbx
005DE392  sub      rsp, 0x30
005DE396  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005DE39F  mov      rbx, rcx
005DE3A2  cmp      byte ptr [rcx + 8], 0
005DE3A6  je       0x5de3ba  ; -> 005DE3BA
005DE3A8  lea      rdx, [rip + 0x76cfa1]  ; -> 00D4B350
005DE3AF  mov      ecx, 3
005DE3B4  call     0x5cdaa0  ; -> 005CDAA0 fn
005DE3B9  nop      
005DE3BA  mov      rcx, qword ptr [rbx + 0x20]
005DE3BE  test     rcx, rcx
005DE3C1  je       0x5de3c9  ; -> 005DE3C9
005DE3C3  call     0x6108c0  ; -> 006108C0 fn
005DE3C8  nop      
005DE3C9  add      rsp, 0x30
005DE3CD  pop      rbx
005DE3CE  ret      
```

## 00616140 (89 B, extent 00616140-00616199)

Entered from (direct sites whose caller this page cites): `00162370` + 0x21 (call; `00162370` is cited on this page)
Other direct sites: `005CFF00` + 0x33 (call)

Host context: "e '00D54348' vtable ('006160F4'/'006160FB'); '+0x30' then marks state 1 ('006160FF'), '+0xB8' and '+0x90..+0xB0' zero ('00616106'..'0061612B'), and 'rax=rbx' returns the object ('00616132'). Callers '00162370'/'0017E8E0'/'0017F3B0'/'00183A00'/'00183C60'/ '00183EE0'/'00184140'/'00184380'/'001B6D90'/'005D38D0'/'006123F0'/'00615840'/ '00874350' — the same '0017Exxx'/'00183xxx' save-buffer caller cluster as '0061E200'/'0062C360'.  ## SWE2-E"

```
00616140  mov      qword ptr [rsp + 8], rcx
00616145  push     rbx
00616146  sub      rsp, 0x30
0061614A  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00616153  mov      rbx, rcx
00616156  call     0x5dcc10  ; -> 005DCC10 fn
0061615B  nop      
0061615C  lea      rcx, [rbx + 0x38]
00616160  mov      dword ptr [rcx], 0
00616166  mov      edx, 1
0061616B  call     0x627750  ; -> 00627750 fn
00616170  mov      qword ptr [rbx + 0x88], 0
0061617B  xor      eax, eax
0061617D  mov      qword ptr [rbx + 0x68], rax
00616181  mov      qword ptr [rbx + 0x70], rax
00616185  mov      qword ptr [rbx + 0x78], rax
00616189  mov      qword ptr [rbx + 0x80], rax
00616190  mov      rax, rbx
00616193  add      rsp, 0x30
00616197  pop      rbx
00616198  ret      
```

## 006161A0 (102 B, extent 006161A0-00616206)

Entered from (direct sites whose caller this page cites): `00162370` + 0x2E (call; `00162370` is cited on this page)
Other direct sites: `005D6870` + 0x33 (call); `00612D00` + 0x1F (call)

Host context: "e '00D54348' vtable ('006160F4'/'006160FB'); '+0x30' then marks state 1 ('006160FF'), '+0xB8' and '+0x90..+0xB0' zero ('00616106'..'0061612B'), and 'rax=rbx' returns the object ('00616132'). Callers '00162370'/'0017E8E0'/'0017F3B0'/'00183A00'/'00183C60'/ '00183EE0'/'00184140'/'00184380'/'001B6D90'/'005D38D0'/'006123F0'/'00615840'/ '00874350' — the same '0017Exxx'/'00183xxx' save-buffer caller cluster as '0061E200'/'0062C360'.  ## SWE2-E"

```
006161A0  mov      qword ptr [rsp + 8], rcx
006161A5  push     rbx
006161A6  sub      rsp, 0x30
006161AA  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006161B3  mov      rbx, rcx
006161B6  call     0x5dcc40  ; -> 005DCC40 fn
006161BB  nop      
006161BC  lea      rcx, [rbx + 0x30]
006161C0  mov      dword ptr [rcx], 0
006161C6  mov      edx, 1
006161CB  call     0x627800  ; -> 00627800 fn
006161D0  mov      qword ptr [rbx + 0xa0], 0
006161DB  xor      eax, eax
006161DD  mov      qword ptr [rbx + 0x78], rax
006161E1  mov      qword ptr [rbx + 0x80], rax
006161E8  mov      qword ptr [rbx + 0x88], rax
006161EF  mov      qword ptr [rbx + 0x90], rax
006161F6  mov      qword ptr [rbx + 0x98], rax
006161FD  mov      rax, rbx
00616200  add      rsp, 0x30
00616204  pop      rbx
00616205  ret      
```

## 00623E70 (57 B, extent 00623E70-00623EA9)

Entered from (direct sites whose caller this page cites): `0062B1E0` + 0x29 (call; `0062B1E0` is cited on this page); `0062B1E0` + 0x43 (call; `0062B1E0` is cited on this page)
Other direct sites: none

Host context: "rologues** — save 'rbx', push 'r14', 'sub rsp,0x20', 'mov rbx,rcx', one 'call', 'mov rcx,[rbx+0x20]', 'xor r14d,r14d', then the clearing store — differing only in the callee ('0062B100', '0062B170', '0062B1E0', themselves **'0x70' apart and 112 bytes each**, so a parallel family of three) and in the displacement cleared. The register stored is provably zero: 'xor r14d, r14d' immediately precedes each store.  **So the guard and the handl" / "rologues** — save 'rbx', push 'r14', 'sub rsp,0x20', 'mov rbx,rcx', one 'call', 'mov rcx,[rbx+0x20]', 'xor r14d,r14d', then the clearing store — differing only in the callee ('0062B100', '0062B170', '0062B1E0', themselves **'0x70' apart and 112 bytes each**, so a parallel family of three) and in the displacement cleared. The register stored is provably zero: 'xor r14d, r14d' immediately precedes each store.  **So the guard and the handl"

```
00623E70  mov      eax, dword ptr [rcx + 0x30]
00623E73  btr      eax, 0x1f
00623E77  cmp      eax, 1
00623E7A  jbe      0x623e8e  ; -> 00623E8E
00623E7C  mov      rcx, qword ptr [rcx + 0x38]
00623E80  mov      eax, edx
00623E82  shl      rax, 6
00623E86  add      rax, 0x20
00623E8A  add      rax, rcx
00623E8D  ret      
00623E8E  add      rcx, 0x38
00623E92  xor      r8d, r8d
00623E95  test     eax, eax
00623E97  mov      eax, edx
00623E99  cmove    rcx, r8
00623E9D  shl      rax, 6
00623EA1  add      rax, 0x20
00623EA5  add      rax, rcx
00623EA8  ret      
```
