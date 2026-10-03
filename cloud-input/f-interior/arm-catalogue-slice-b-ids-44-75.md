# F-interior pack: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-B-ids-44-75.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/arm-catalogue-slice-b-ids-44-75.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

## 001EE180 (79 B, extent 001EE180-001EE1CF)

Page context: "6-09-15: '005CC930' is called by 'Application' '00799980' (1 edge) — same platform-leg shape as slice A.)*  ## SWE2-EC7-49 update (2026-09-19) - '00188DA0'  '00188DA0' (192 B) is a body - '00193D50'/'001EE180'/'001F16C0'/'00610330' plus a 'call [rax+0x10]' vcall. Interior anchor '00188DB4' (an '00193D50' call).  ## SWE2-EC7-49 update (2026-09-19) - '001A97F0'  '001A97F0' (190 B) is a body - '001867B0'/'00189120'/'001AC720'/'001AD440'. I"

```
001EE180  test     rcx, rcx
001EE183  je       0x1ee1ce  ; -> 001EE1CE
001EE185  mov      qword ptr [rsp + 0x10], rbx
001EE18A  push     rsi
001EE18B  sub      rsp, 0x20
001EE18F  cmp      byte ptr [rcx + 8], 0
001EE193  mov      esi, edx
001EE195  mov      rbx, rcx
001EE198  jne      0x1ee1c4  ; -> 001EE1C4
001EE19A  mov      qword ptr [rsp + 0x30], rdi
001EE19F  mov      rdi, qword ptr [rcx]
001EE1A2  test     rdi, rdi
001EE1A5  je       0x1ee1bf  ; -> 001EE1BF
001EE1A7  mov      rcx, rdi
001EE1AA  call     0x625f00  ; -> 00625F00 fn
001EE1AF  test     al, al
001EE1B1  je       0x1ee1bb  ; -> 001EE1BB
001EE1B3  mov      rcx, rdi
001EE1B6  call     0x62bcb0  ; -> 0062BCB0 fn
001EE1BB  mov      byte ptr [rbx + 9], sil
001EE1BF  mov      rdi, qword ptr [rsp + 0x30]
001EE1C4  mov      rbx, qword ptr [rsp + 0x38]
001EE1C9  add      rsp, 0x20
001EE1CD  pop      rsi
001EE1CE  ret      
```

## 0024B100 (29 B, extent 0024B100-0024B11D)

Page context: "-indexed fan-out '001D1660' and '0022A0B0' run: the byte is captured in 'bl', '001B24B0()' runs first with its result dropped, then '0024B120(bl)' and '00248410(bl)' take the byte and the tail jumps '0024B100' - one slot byte driving three downstream calls. Interior anchor '00184671' (the '0024B120' call). '0022A0B0''s own fan-out is mechanical and recorded here: it reaches the ActorEntity and RNG_Random_Selection domains - shared-servi"

```
0024B100  movzx    eax, word ptr [rip + 0x1bc10d1]  ; -> 01E0C1D8 [u16 0x0200]
0024B107  mov      word ptr [rip + 0x1bc10c6], ax  ; -> 01E0C1D4 [u16 0x0200]
0024B10E  movzx    eax, word ptr [rip + 0x1bc10c7]  ; -> 01E0C1DC [u16 0x01C0]
0024B115  mov      word ptr [rip + 0x1bc10ba], ax  ; -> 01E0C1D6 [u16 0x01C0]
0024B11C  ret      
```

## 0024B120 (46 B, extent 0024B120-0024B14E)

Page context: "0062BA20' (the '+0x1C' bit-7 clear).  '00184660' (40 B) is the 'cl'-indexed fan-out '001D1660' and '0022A0B0' run: the byte is captured in 'bl', '001B24B0()' runs first with its result dropped, then '0024B120(bl)' and '00248410(bl)' take the byte and the tail jumps '0024B100' - one slot byte driving three downstream calls. Interior anchor '00184671' (the '0024B120' call). '0022A0B0''s own fan-out is mechanical and recorded here: it reac"

```
0024B120  test     ecx, ecx
0024B122  je       0x24b139  ; -> 0024B139
0024B124  mov      dword ptr [rip + 0x1bc10aa], 0x780  ; -> 01E0C1D8 [u32 0x00000200]
0024B12E  mov      dword ptr [rip + 0x1bc10a4], 0x438  ; -> 01E0C1DC [u32 0x000001C0]
0024B138  ret      
0024B139  mov      dword ptr [rip + 0x1bc1095], 0x200  ; -> 01E0C1D8 [u32 0x00000200]
0024B143  mov      dword ptr [rip + 0x1bc108f], 0x1c0  ; -> 01E0C1DC [u32 0x000001C0]
0024B14D  ret      
```
