# F-interior pack: `18-Audio/Audio-Boundary/what-the-engine-calls-to-make-a-sound.md`

Generated 2026-10-03 02:40 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/what-the-engine-calls-to-make-a-sound.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: cd6bd7f58	SWE2-DATA consolidated publish: progress-report cluster (generation store, R3 semantics, DB_GOAL, me; d0fd168a2	SWE2-DATA: batch-5 review corrections (clamping page's .data vf00 cell restored, SD-190 gate on the ; inbox mentions: repos-2d.md, repos-78.md, repos-9e.md). OPUS read these before packing.

## 00212A90 (68 B, extent 00212A90-00212AD4)

Page context: "E0' (324 B) is a sound-call body - '01F44830', '00271140'/'00808C40'. Interior anchor '003F13DC' (a '00271140' call).  ## SWE2-EC7-48 update (2026-09-19) - '00210FF0'  '00210FF0' (204 B) is a body - '00212A90'/'00212AE0'/'00212B30'/'00212BD0'. Interior anchor '00211019' (a '00212A90' call).  ## SWE2-EC7-92 update (2026-09-20) - '00379E30' drain loop measured  '00379E30' (46 B) is the bounded drain the '003DEC90'/'003DEE10' sound callers"

```
00212A90  mov      qword ptr [rsp + 8], rbx
00212A95  mov      qword ptr [rsp + 0x10], rsi
00212A9A  push     rdi
00212A9B  sub      rsp, 0x20
00212A9F  mov      rbx, qword ptr [rcx + 8]
00212AA3  lea      rdi, [rcx + 8]
00212AA7  mov      esi, edx
00212AA9  cmp      rbx, rdi
00212AAC  je       0x212ac4  ; -> 00212AC4
00212AAE  nop      
00212AB0  mov      rcx, qword ptr [rbx + 0x10]
00212AB4  mov      edx, esi
00212AB6  mov      rax, qword ptr [rcx]
00212AB9  call     qword ptr [rax + 0x20]
00212ABC  mov      rbx, qword ptr [rbx]
00212ABF  cmp      rbx, rdi
00212AC2  jne      0x212ab0  ; -> 00212AB0
00212AC4  mov      rbx, qword ptr [rsp + 0x30]
00212AC9  mov      rsi, qword ptr [rsp + 0x38]
00212ACE  add      rsp, 0x20
00212AD2  pop      rdi
00212AD3  ret      
```

## 00212AE0 (68 B, extent 00212AE0-00212B24)

Page context: " is a sound-call body - '01F44830', '00271140'/'00808C40'. Interior anchor '003F13DC' (a '00271140' call).  ## SWE2-EC7-48 update (2026-09-19) - '00210FF0'  '00210FF0' (204 B) is a body - '00212A90'/'00212AE0'/'00212B30'/'00212BD0'. Interior anchor '00211019' (a '00212A90' call).  ## SWE2-EC7-92 update (2026-09-20) - '00379E30' drain loop measured  '00379E30' (46 B) is the bounded drain the '003DEC90'/'003DEE10' sound callers run: while"

```
00212AE0  mov      qword ptr [rsp + 8], rbx
00212AE5  mov      qword ptr [rsp + 0x10], rsi
00212AEA  push     rdi
00212AEB  sub      rsp, 0x20
00212AEF  mov      rbx, qword ptr [rcx + 8]
00212AF3  lea      rdi, [rcx + 8]
00212AF7  mov      esi, edx
00212AF9  cmp      rbx, rdi
00212AFC  je       0x212b14  ; -> 00212B14
00212AFE  nop      
00212B00  mov      rcx, qword ptr [rbx + 0x10]
00212B04  mov      edx, esi
00212B06  mov      rax, qword ptr [rcx]
00212B09  call     qword ptr [rax + 0x18]
00212B0C  mov      rbx, qword ptr [rbx]
00212B0F  cmp      rbx, rdi
00212B12  jne      0x212b00  ; -> 00212B00
00212B14  mov      rbx, qword ptr [rsp + 0x30]
00212B19  mov      rsi, qword ptr [rsp + 0x38]
00212B1E  add      rsp, 0x20
00212B22  pop      rdi
00212B23  ret      
```

## 00212B30 (68 B, extent 00212B30-00212B74)

Page context: "-call body - '01F44830', '00271140'/'00808C40'. Interior anchor '003F13DC' (a '00271140' call).  ## SWE2-EC7-48 update (2026-09-19) - '00210FF0'  '00210FF0' (204 B) is a body - '00212A90'/'00212AE0'/'00212B30'/'00212BD0'. Interior anchor '00211019' (a '00212A90' call).  ## SWE2-EC7-92 update (2026-09-20) - '00379E30' drain loop measured  '00379E30' (46 B) is the bounded drain the '003DEC90'/'003DEE10' sound callers run: while '00379E60("

```
00212B30  mov      qword ptr [rsp + 8], rbx
00212B35  mov      qword ptr [rsp + 0x10], rsi
00212B3A  push     rdi
00212B3B  sub      rsp, 0x20
00212B3F  mov      rbx, qword ptr [rcx + 8]
00212B43  lea      rdi, [rcx + 8]
00212B47  mov      esi, edx
00212B49  cmp      rbx, rdi
00212B4C  je       0x212b64  ; -> 00212B64
00212B4E  nop      
00212B50  mov      rcx, qword ptr [rbx + 0x10]
00212B54  mov      edx, esi
00212B56  mov      rax, qword ptr [rcx]
00212B59  call     qword ptr [rax + 0x28]
00212B5C  mov      rbx, qword ptr [rbx]
00212B5F  cmp      rbx, rdi
00212B62  jne      0x212b50  ; -> 00212B50
00212B64  mov      rbx, qword ptr [rsp + 0x30]
00212B69  mov      rsi, qword ptr [rsp + 0x38]
00212B6E  add      rsp, 0x20
00212B72  pop      rdi
00212B73  ret      
```

## 00212BD0 (67 B, extent 00212BD0-00212C13)

Page context: "- '01F44830', '00271140'/'00808C40'. Interior anchor '003F13DC' (a '00271140' call).  ## SWE2-EC7-48 update (2026-09-19) - '00210FF0'  '00210FF0' (204 B) is a body - '00212A90'/'00212AE0'/'00212B30'/'00212BD0'. Interior anchor '00211019' (a '00212A90' call).  ## SWE2-EC7-92 update (2026-09-20) - '00379E30' drain loop measured  '00379E30' (46 B) is the bounded drain the '003DEC90'/'003DEE10' sound callers run: while '00379E60(ecx)' repor"

```
00212BD0  mov      qword ptr [rsp + 8], rbx
00212BD5  mov      qword ptr [rsp + 0x10], rsi
00212BDA  push     rdi
00212BDB  sub      rsp, 0x20
00212BDF  mov      rbx, qword ptr [rcx + 8]
00212BE3  lea      rdi, [rcx + 8]
00212BE7  mov      esi, edx
00212BE9  cmp      rbx, rdi
00212BEC  je       0x212c03  ; -> 00212C03
00212BEE  nop      
00212BF0  mov      rcx, qword ptr [rbx + 0x10]
00212BF4  mov      edx, esi
00212BF6  mov      rax, qword ptr [rcx]
00212BF9  call     qword ptr [rax]
00212BFB  mov      rbx, qword ptr [rbx]
00212BFE  cmp      rbx, rdi
00212C01  jne      0x212bf0  ; -> 00212BF0
00212C03  mov      rbx, qword ptr [rsp + 0x30]
00212C08  mov      rsi, qword ptr [rsp + 0x38]
00212C0D  add      rsp, 0x20
00212C11  pop      rdi
00212C12  ret      
```

## 0035D030 (28 B, extent 0035D030-0035D04C)

Page context: " and say which of the two readings its numbers use. Both partitions are defensible; publishing one without its definition is not.  ### Overturned 2 — "no callers at all: 51" is 50 against the bytes  '0035D030' is counted among the 51 and is reached through a five-byte thunk:  ''' 002E22F0  thunk_FUN_0035d030  --JMP-->  0035D030 '''  A thunk is a sink in the call graph, so the edge out of it is not recorded and the target's caller list o"

```
0035D030  sub      rsp, 0x28
0035D034  mov      ecx, 1
0035D039  call     0x28e940  ; -> 0028E940 fn
0035D03E  mov      ecx, 4
0035D043  add      rsp, 0x28
0035D047  jmp      0x249c60  ; -> 00249C60 fn
```
