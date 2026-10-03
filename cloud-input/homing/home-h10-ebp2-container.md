# Homing pack: `25-EBP-Script-Container/Container/ebp2-container.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-ebp2-container.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0029B440 (73 B, extent 0029B440-0029B489)

Entered from (direct sites whose caller this page cites): `00297640` + 0x63 (call; `00297640` is cited on this page)
Other direct sites: `0029BE50` + 0x256 (call)

Host context: "he shipping bytes 2026-09-14 (OPUS).  **UI — CLIENT (SWE2-EC7 batch-150).** The '0029AEF0' flag sweep runs on the shared '0035BB60'/'0035BB00' record accessors the UI layer calls heavily ('002737B0'/'00297640'/'002734F0'/'002964D0' among them), and '00297170' itself sits inside that layer's call neighbourhood ('002904D0'/'00273A20'/'0029AE50') - shared accessor fan-in over container records, not UI ownership of the container.  **Gamepla"

```
0029B440  push     rbx
0029B442  sub      rsp, 0x20
0029B446  mov      ebx, ecx
0029B448  mov      edx, ecx
0029B44A  mov      ecx, 2
0029B44F  call     0x2be080  ; -> 002BE080 fn
0029B454  xor      ecx, ecx
0029B456  call     0x290ca0  ; -> 00290CA0 fn
0029B45B  mov      edx, ebx
0029B45D  mov      ecx, 4
0029B462  call     0x35c150  ; -> 0035C150 fn
0029B467  mov      ecx, ebx
0029B469  call     0x3c93e0  ; -> 003C93E0 fn
0029B46E  call     0x2906d0  ; -> 002906D0 fn
0029B473  test     eax, eax
0029B475  je       0x29b483  ; -> 0029B483
0029B477  mov      ecx, ebx
0029B479  add      rsp, 0x20
0029B47D  pop      rbx
0029B47E  jmp      0x290680  ; -> 00290680 fn
0029B483  add      rsp, 0x20
0029B487  pop      rbx
0029B488  ret      
```

## 0035BC30 (13 B, extent 0035BC30-0035BC3D)

Entered from (direct sites whose caller this page cites): `00297640` + 0x8E (call; `00297640` is cited on this page)
Other direct sites: none

Host context: "he shipping bytes 2026-09-14 (OPUS).  **UI — CLIENT (SWE2-EC7 batch-150).** The '0029AEF0' flag sweep runs on the shared '0035BB60'/'0035BB00' record accessors the UI layer calls heavily ('002737B0'/'00297640'/'002734F0'/'002964D0' among them), and '00297170' itself sits inside that layer's call neighbourhood ('002904D0'/'00273A20'/'0029AE50') - shared accessor fan-in over container records, not UI ownership of the container.  **Gamepla"

```
0035BC30  mov      eax, dword ptr [rip + 0x1f6c42a]  ; -> 022C8060
0035BC36  shr      eax, 2
0035BC39  and      eax, 1
0035BC3C  ret      
```
